#!/usr/bin/env node
'use strict';

const fs = require('node:fs');
const path = require('node:path');

const scriptDir = __dirname;
const templatePath = path.join(scriptDir, 'ehi-dashboard.template.html');
const resultsPath = path.join(scriptDir, 'ehi-grading-results.json');
const outputPath = path.join(scriptDir, 'ehi-dashboard.html');

const template = fs.readFileSync(templatePath, 'utf8');
const resultsRaw = fs.readFileSync(resultsPath, 'utf8');
const results = JSON.parse(resultsRaw);

const ABSTRACTION_VENDOR_ID = '__abstraction__';
const MARKER_GRADING_JSON = '__EHI_GRADING_JSON__';
const MARKER_SOURCE_BUNDLE = '__EHI_SOURCE_BUNDLE__';
function escapeInlineScriptJson(payload) {
  const raw = JSON.stringify(payload);
  return raw.replace(/<\/(script)/gi, '<\\/$1');
}
const SOURCE_TEXT_EXTS = new Set([
  '',
  '.md',
  '.markdown',
  '.txt',
  '.json',
  '.jsonl',
  '.yml',
  '.yaml',
  '.html',
  '.htm',
  '.css',
  '.js',
  '.ts',
  '.xml',
  '.log',
  '.ini',
  '.cfg',
  '.conf',
  '.toml',
  '.csv',
]);
const BINARY_EXTS = new Set([
  '.png',
  '.jpg',
  '.jpeg',
  '.gif',
  '.pdf',
  '.zip',
  '.xlsx',
  '.xls',
  '.ppt',
  '.pptx',
  '.doc',
  '.docx',
  '.webp',
  '.mp4',
  '.mp3',
  '.mov',
  '.pyc',
]);
const MAX_TEXT_BYTES = 300_000;

function toPosix(p) {
  return p.split(path.sep).join('/');
}

function isBinaryLikely(buffer) {
  for (let i = 0; i < buffer.length; i += 1) {
    if (buffer[i] === 0) return true;
  }
  return false;
}

function shouldIncludeFile(filePath, ext, buffer) {
  if (BINARY_EXTS.has(ext)) return false;
  if (buffer.length > MAX_TEXT_BYTES) return false;
  if (isBinaryLikely(buffer)) return false;
  if (SOURCE_TEXT_EXTS.has(ext)) return true;
  if (!ext && buffer.length < 40_000) return true;
  return false;
}

function inferFileType(ext) {
  if (ext === '.md' || ext === '.markdown') return 'markdown';
  if (ext === '.json' || ext === '.jsonl') return 'json';
  if (ext === '.csv') return 'csv';
  if (ext === '.html' || ext === '.htm') return 'html';
  if (ext === '.xml') return 'xml';
  return 'text';
}

function walkVendorFiles(absVendorRoot, relVendorRoot) {
  const files = [];

  if (!fs.existsSync(absVendorRoot)) {
    return files;
  }

  function walk(currentAbs, currentRel) {
    const entries = fs.readdirSync(currentAbs, { withFileTypes: true });
    entries.sort((a, b) => a.name.localeCompare(b.name));

    for (const entry of entries) {
      const nextRel = currentRel ? `${currentRel}/${entry.name}` : entry.name;
      const nextAbs = path.join(currentAbs, entry.name);
      if (entry.isDirectory()) {
        walk(nextAbs, nextRel);
        continue;
      }

      const ext = path.extname(entry.name).toLowerCase();
      const relPath = `${relVendorRoot}/${nextRel}`;
      const buffer = fs.readFileSync(nextAbs);
      if (!shouldIncludeFile(relPath, ext, buffer)) {
        continue;
      }

      files.push({
        path: toPosix(relPath),
        name: entry.name,
        ext,
        size: buffer.length,
        type: inferFileType(ext),
        content: buffer.toString('utf8'),
      });
    }
  }

  walk(absVendorRoot, '');
  return files;
}

function buildSourceBundle(results, repoRoot) {
  const reportVendorToId = new Map();
  const vendors = [];
  const recordFileIndex = {};

  for (const record of results.records || []) {
    const reportPath = record?.reportPath;
    if (!reportPath || reportVendorToId.has(reportPath)) {
      continue;
    }

    const vendorId = toPosix(reportPath).split('/')[1];
    reportVendorToId.set(reportPath, vendorId);
    const vendorDir = vendorId;
    const absVendorRoot = path.join(repoRoot, path.dirname(toPosix(reportPath)));
    const files = walkVendorFiles(absVendorRoot, path.dirname(toPosix(reportPath)));

    vendors.push({
      id: vendorId,
      vendor: record.vendor || vendorId,
      reportPath,
      path: path.dirname(toPosix(reportPath)),
      isVirtual: false,
      files,
    });
  }

  vendors.sort((a, b) => a.vendor.localeCompare(b.vendor));

  const abstractionFiles = [];
  const allResultsPath = '__abstraction__/ehi-grading-results.json';
  const allResultsContent = JSON.stringify(results, null, 2);
  abstractionFiles.push({
    path: allResultsPath,
    name: 'ehi-grading-results.json',
    ext: '.json',
    size: Buffer.byteLength(allResultsContent, 'utf8'),
    type: 'json',
    isVirtual: true,
    content: allResultsContent,
  });

  (results.records || []).forEach((record, index) => {
    const vendorId = reportVendorToId.get(record?.reportPath) || '__unknown__';
    const filePath = `__abstraction__/records/record-${index}-${vendorId}.json`;
    const recordContent = JSON.stringify(record, null, 2);
    recordFileIndex[index] = filePath;
    abstractionFiles.push({
      path: filePath,
      name: `${vendorId}-record-${index}.json`,
      ext: '.json',
      size: Buffer.byteLength(recordContent, 'utf8'),
      type: 'json',
      isVirtual: true,
      recordIndex: index,
      content: recordContent,
    });
  });

  vendors.push({
    id: ABSTRACTION_VENDOR_ID,
    vendor: 'Abstraction Artifacts',
    isVirtual: true,
    reportPath: null,
    path: '__abstraction__',
    files: abstractionFiles,
  });

  return {
    generatedAt: new Date().toISOString(),
    vendors,
    recordFileIndex,
  };
}

const sourceBundle = buildSourceBundle(results, path.resolve(scriptDir, '..'));

if (!template.includes(MARKER_GRADING_JSON)) {
  throw new Error(`Template marker ${MARKER_GRADING_JSON} not found in ${templatePath}`);
}
if (!template.includes(MARKER_SOURCE_BUNDLE)) {
  throw new Error(`Template marker ${MARKER_SOURCE_BUNDLE} not found in ${templatePath}`);
}

const output = template
  .replace(MARKER_GRADING_JSON, escapeInlineScriptJson(results))
  .replace(MARKER_SOURCE_BUNDLE, escapeInlineScriptJson(sourceBundle));
fs.writeFileSync(outputPath, output, 'utf8');
console.log(`Wrote ${path.relative(process.cwd(), outputPath)}`);
