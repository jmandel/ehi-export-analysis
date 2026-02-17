#!/usr/bin/env bun
/**
 * Extracts CSV data dictionary tables from MEDITECH EHI Export PDF files.
 *
 * Prerequisites: pdftotext (from poppler-utils) must be installed.
 *
 * Usage: bun run extract-csv-data-dictionaries.ts
 *
 * Input: Three PDF files in ../
 *   - 608ehiexportcsv.pdf (MPM 6.08 Ambulatory)
 *   - csacuteandambehiexportdrsolutionmerged.pdf (Client/Server Acute & Ambulatory)
 *   - mgehiexportdrsolutionmerged.pdf (MAGIC Acute & Ambulatory)
 *
 * Output: csv-data-dictionaries.json
 */

import { execSync } from "child_process";
import { resolve, dirname } from "path";
import { writeFileSync } from "fs";

const scriptDir = dirname(new URL(import.meta.url).pathname);
const downloadsDir = resolve(scriptDir, "..");

interface FieldEntry {
  field: string;
  table: string;
  column: string;
}

interface TableGroup {
  tableName: string;
  fields: FieldEntry[];
}

interface PdfResult {
  sourceFile: string;
  platform: string;
  lastUpdated: string;
  tables: TableGroup[];
  totalFields: number;
  totalTables: number;
  parseErrors: string[];
}

function extractTextFromPdf(pdfPath: string): string {
  return execSync(`pdftotext -layout "${pdfPath}" -`, {
    encoding: "utf-8",
    maxBuffer: 10 * 1024 * 1024,
  });
}

function parseCsvDataDictionary(text: string, sourceFile: string): PdfResult {
  const lines = text.split("\n");
  const parseErrors: string[] = [];

  // Extract metadata from header
  let platform = "";
  let lastUpdated = "";
  for (const line of lines.slice(0, 15)) {
    const trimmed = line.trim();
    if (trimmed.startsWith("Platform:")) {
      platform = trimmed.replace("Platform:", "").trim();
    }
    if (trimmed.startsWith("Last Updated:")) {
      lastUpdated = trimmed.replace("Last Updated:", "").trim();
    }
  }

  // Find the header row "Field ... Table ... Column"
  let dataStartIdx = -1;
  for (let i = 0; i < lines.length; i++) {
    const trimmed = lines[i].trim();
    if (/^Field\s+Table\s+Column\s*$/.test(trimmed)) {
      dataStartIdx = i + 1;
      break;
    }
  }

  if (dataStartIdx === -1) {
    parseErrors.push("Could not find 'Field Table Column' header row");
    return {
      sourceFile,
      platform,
      lastUpdated,
      tables: [],
      totalFields: 0,
      totalTables: 0,
      parseErrors,
    };
  }

  const tables: TableGroup[] = [];
  let currentTable: TableGroup | null = null;

  for (let i = dataStartIdx; i < lines.length; i++) {
    const line = lines[i];
    const trimmed = line.trim();

    // Skip blank lines, page numbers, and repeated headers
    if (!trimmed) continue;
    if (/^\d+$/.test(trimmed)) continue; // page number
    if (/^MEDITECH$/i.test(trimmed)) continue;
    if (/EHI Export Data in CSV File/i.test(trimmed)) continue;
    if (/Last Updated:/i.test(trimmed)) continue;
    if (/^Field\s+Table\s+Column\s*$/.test(trimmed)) continue; // repeated header

    // Detect table header lines: a single word/phrase with no whitespace-separated columns
    // Table headers appear alone on a line, left-aligned, with no other columns
    // A data row has at least two whitespace-separated segments
    const segments = trimmed.split(/\s{2,}/);

    if (segments.length === 1) {
      // This is a table header (or a continuation line — we'll treat single-segment as header)
      // But check: could it be a data row where field, table, column happen to be the same word?
      // In practice, table headers are PascalCase identifiers like "AdmEmployers"
      const name = segments[0];
      currentTable = { tableName: name, fields: [] };
      tables.push(currentTable);
    } else if (segments.length === 2) {
      // Two segments: could be table + column (field missing), or field + table (column missing)
      // Looking at the data, this pattern is: Table, Column (field name is the same as table header)
      if (currentTable) {
        currentTable.fields.push({
          field: segments[0],
          table: currentTable.tableName,
          column: segments[1],
        });
      } else {
        parseErrors.push(`Line ${i + 1}: Two-segment line without active table: "${trimmed}"`);
      }
    } else if (segments.length >= 3) {
      // Standard row: Field, Table, Column
      const field = segments[0];
      const table = segments[1];
      const column = segments.slice(2).join(" "); // column might have spaces
      if (currentTable && table !== currentTable.tableName) {
        // Table changed mid-section without a header — create new table
        currentTable = { tableName: table, fields: [] };
        tables.push(currentTable);
      } else if (!currentTable) {
        currentTable = { tableName: table, fields: [] };
        tables.push(currentTable);
      }
      currentTable.fields.push({ field, table, column });
    }
  }

  // Deduplicate tables by name (merge fields)
  const tableMap = new Map<string, TableGroup>();
  for (const t of tables) {
    const existing = tableMap.get(t.tableName);
    if (existing) {
      existing.fields.push(...t.fields);
    } else {
      tableMap.set(t.tableName, { ...t });
    }
  }
  const mergedTables = Array.from(tableMap.values());

  const totalFields = mergedTables.reduce((sum, t) => sum + t.fields.length, 0);

  return {
    sourceFile,
    platform,
    lastUpdated,
    tables: mergedTables,
    totalFields,
    totalTables: mergedTables.length,
    parseErrors,
  };
}

// Process all three PDFs
const pdfs = [
  { file: "608ehiexportcsv.pdf", label: "MPM 6.08 Ambulatory" },
  { file: "csacuteandambehiexportdrsolutionmerged.pdf", label: "Client/Server Acute & Ambulatory" },
  { file: "mgehiexportdrsolutionmerged.pdf", label: "MAGIC Acute & Ambulatory" },
];

const results: PdfResult[] = [];
const stats = {
  totalFilesDiscovered: pdfs.length,
  totalFilesParsed: 0,
  parseFailures: [] as { file: string; error: string }[],
};

for (const pdf of pdfs) {
  const pdfPath = resolve(downloadsDir, pdf.file);
  try {
    console.log(`Processing ${pdf.file}...`);
    const text = extractTextFromPdf(pdfPath);
    const result = parseCsvDataDictionary(text, pdf.file);
    results.push(result);
    stats.totalFilesParsed++;
    console.log(`  Platform: ${result.platform}`);
    console.log(`  Tables: ${result.totalTables}, Fields: ${result.totalFields}`);
    if (result.parseErrors.length > 0) {
      console.log(`  Parse errors: ${result.parseErrors.length}`);
    }
  } catch (e: any) {
    stats.parseFailures.push({ file: pdf.file, error: e.message });
    console.error(`  FAILED: ${e.message}`);
  }
}

const output = {
  extractionDate: new Date().toISOString().split("T")[0],
  description: "CSV data dictionaries extracted from MEDITECH EHI Export PDF files. Each entry documents the tables and columns included in the EHI Export Patient Data CSV files for a specific MEDITECH platform.",
  stats,
  dictionaries: results,
};

const outPath = resolve(scriptDir, "csv-data-dictionaries.json");
writeFileSync(outPath, JSON.stringify(output, null, 2));
console.log(`\nOutput written to ${outPath}`);
console.log(`Total tables across all platforms: ${results.reduce((s, r) => s + r.totalTables, 0)}`);
console.log(`Total fields across all platforms: ${results.reduce((s, r) => s + r.totalFields, 0)}`);
