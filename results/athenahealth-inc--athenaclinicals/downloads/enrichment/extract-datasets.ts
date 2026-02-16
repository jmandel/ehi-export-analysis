#!/usr/bin/env bun
/**
 * Extracts structured dataset information from the athenahealth EHI Export
 * documentation API JSON files (Contentful rich text format).
 *
 * Input: ../api-*.json files (Contentful freeformPage entries)
 * Output: datasets.json — structured dataset catalog with fields, links, and metadata
 *         coverage.json — accounting of files parsed and any errors
 */

import { readFileSync, writeFileSync, readdirSync } from "fs";
import { join, dirname } from "path";

const downloadsDir = join(dirname(import.meta.dir));

interface RichTextNode {
  nodeType: string;
  value?: string;
  data?: {
    uri?: string;
    target?: {
      fields?: Record<string, any>;
      sys?: { contentType?: { sys?: { id?: string } } };
    };
  };
  content?: RichTextNode[];
  marks?: Array<{ type: string }>;
}

interface DatasetEntry {
  name: string;
  specUrl: string | null;
  includesAttachments: boolean | null;
  source: string;
  category: string;
}

interface FieldSpec {
  name: string;
  type: string;
  description: string;
}

interface DatasetSpec {
  datasetName: string;
  category: string;
  source: string;
  inputParameters: FieldSpec[];
  outputParameters: FieldSpec[];
}

interface ExportType {
  id: string;
  title: string;
  urlAlias: string;
  category: string;
  format: string;
  datasets: DatasetEntry[];
  inlineSpecs: DatasetSpec[];
  headings: string[];
  downloadPdfUrl: string | null;
}

// Extract plain text from a rich text node
function extractText(node: RichTextNode): string {
  if (node.nodeType === "text") return node.value || "";
  let result = "";
  for (const child of node.content || []) {
    result += extractText(child);
  }
  return result;
}

// Extract headings
function extractHeadings(node: RichTextNode, results: Array<{ level: string; text: string }> = []): typeof results {
  if (node.nodeType?.startsWith("heading-")) {
    results.push({ level: node.nodeType, text: extractText(node).trim() });
  }
  for (const child of node.content || []) {
    extractHeadings(child, results);
  }
  return results;
}

// Extract links from a cell
function getCellInfo(cell: RichTextNode): { text: string; links: Array<{ text: string; url: string }> } {
  const texts: string[] = [];
  const links: Array<{ text: string; url: string }> = [];

  function walk(n: RichTextNode) {
    if (n.nodeType === "text") {
      const t = (n.value || "").trim();
      if (t) texts.push(t);
    } else if (n.nodeType === "hyperlink") {
      const uri = n.data?.uri || "";
      let lt = "";
      for (const c of n.content || []) {
        if (c.nodeType === "text") lt += c.value || "";
      }
      links.push({ text: lt.trim(), url: uri });
      texts.push(lt.trim());
    }
    for (const c of n.content || []) {
      walk(c);
    }
  }
  walk(cell);
  return { text: [...new Set(texts)].join(" "), links };
}

// Parse table rows into field specs (3-column: Name, Type, Description)
function parseFieldTable(table: RichTextNode): FieldSpec[] {
  const fields: FieldSpec[] = [];
  for (const row of table.content || []) {
    if (row.nodeType !== "table-row") continue;
    const cells = row.content || [];
    if (cells.length >= 3) {
      const name = extractText(cells[0]).trim();
      const type = extractText(cells[1]).trim();
      const description = extractText(cells[2]).trim();
      if (name && name !== "Name" && name !== " ") {
        fields.push({ name, type, description });
      }
    }
  }
  return fields;
}

// Parse dataset table (handles both 2-column and S.No+Name formats)
function parseDatasetTable(table: RichTextNode, category: string, source: string): DatasetEntry[] {
  const datasets: DatasetEntry[] = [];
  const rows = table.content || [];
  if (rows.length === 0) return datasets;

  // Detect table format from header row
  const headerCells = rows[0]?.content || [];
  const headerTexts = headerCells.map((c: RichTextNode) => extractText(c).trim());
  const hasSNo = headerTexts.some((t: string) => t === "S.No");
  const nameColIdx = hasSNo ? 1 : 0;
  const attachColIdx = headerTexts.findIndex((t: string) => t.includes("attachment") || t.includes("Includes"));

  for (const row of rows) {
    if (row.nodeType !== "table-row") continue;
    const cells = row.content || [];
    if (cells.length < 2) continue;

    const nameCell = cells[nameColIdx];
    if (!nameCell) continue;
    const nameInfo = getCellInfo(nameCell);

    // Skip header row
    if (nameInfo.text.includes("Dataset Name") || nameInfo.text.includes("S.No")) continue;
    // Skip if name is just a number (S.No column misread)
    if (/^\d+$/.test(nameInfo.text.trim())) continue;

    const name = nameInfo.links.length > 0 ? nameInfo.links[0].text : nameInfo.text;
    const specUrl = nameInfo.links.length > 0 ? nameInfo.links[0].url : null;

    let includesAttachments: boolean | null = null;
    if (attachColIdx >= 0 && cells[attachColIdx]) {
      const attachText = extractText(cells[attachColIdx]).toLowerCase().trim();
      includesAttachments = attachText === "yes" ? true : attachText === "no" ? false : null;
    }

    if (!name || name === "" || name === " ") continue;

    datasets.push({
      name: name.replace(/\s+/g, " ").trim(),
      specUrl,
      includesAttachments,
      source,
      category,
    });
  }
  return datasets;
}

// Find the PDF download URL from embedded entries
function findPdfUrl(body: RichTextNode): string | null {
  let url: string | null = null;

  function walk(node: RichTextNode) {
    if (node.nodeType === "embedded-entry-block") {
      const target = node.data?.target;
      const fields = target?.fields;
      if (fields) {
        // Look for downloadableFile entries
        function searchForUrl(obj: any, path: string) {
          if (typeof obj === "object" && obj !== null) {
            for (const [k, v] of Object.entries(obj)) {
              if (typeof v === "string" && v.includes("ctfassets.net") && v.endsWith(".pdf")) {
                url = v.startsWith("//") ? "https:" + v : v;
              }
              searchForUrl(v, path + "." + k);
            }
          }
        }
        searchForUrl(fields, "fields");
      }
    }
    for (const c of node.content || []) {
      walk(c);
    }
  }

  walk(body);
  return url;
}

// Main processing
const apiFiles = readdirSync(downloadsDir)
  .filter((f) => f.startsWith("api-") && f.endsWith(".json") && !f.includes("navigation") && !f.includes("microsite"));

const categoryMap: Record<string, string> = {
  "api-ambulatory-clinical.json": "ambulatory-clinical",
  "api-ambulatory-collector.json": "ambulatory-collector",
  "api-inpatient-clinical.json": "inpatient-clinical",
  "api-inpatient-collector.json": "inpatient-collector",
  "api-welcome-exports.json": "overview",
  "api-release-notes.json": "release-notes",
};

const results: ExportType[] = [];
const errors: Array<{ file: string; error: string }> = [];

for (const file of apiFiles) {
  try {
    const filePath = join(downloadsDir, file);
    const raw = JSON.parse(readFileSync(filePath, "utf-8"));
    const entry = Array.isArray(raw) ? raw[0] : raw;
    const body: RichTextNode = entry.body;
    const title = entry.title || file;
    const urlAlias = entry.urlAlias || "";
    const category = categoryMap[file] || "unknown";

    // Determine format
    let format = "unknown";
    const bodyText = extractText(body).toLowerCase();
    if (bodyText.includes("newline delimited json")) format = "NDJSON";
    else if (bodyText.includes("html format")) format = "HTML";
    else if (category === "overview" || category === "release-notes") format = "N/A";

    // Find PDF download URL
    const downloadPdfUrl = findPdfUrl(body);

    // Walk top-level content to find dataset tables and inline specs
    const topContent = body.content || [];
    const datasets: DatasetEntry[] = [];
    const inlineSpecs: DatasetSpec[] = [];

    let inDatasetListSection = false;
    let inOtherSpecsSection = false;
    let currentSpecName: string | null = null;
    let currentInputParams: FieldSpec[] = [];
    let currentOutputParams: FieldSpec[] = [];
    let expectingParams: "input" | "output" | null = null;

    for (let i = 0; i < topContent.length; i++) {
      const node = topContent[i];
      const nt = node.nodeType;
      const text = extractText(node).trim();

      // Track sections
      if (nt === "heading-2") {
        if (text.includes("Dataset List") || text.includes("Data Sections")) {
          inDatasetListSection = true;
          inOtherSpecsSection = false;
        } else if (text.includes("Other Specifications") || text.includes("Specifications for Selected")) {
          inDatasetListSection = false;
          inOtherSpecsSection = true;
        } else if (text.includes("Folder Structure")) {
          // Save any pending spec
          if (currentSpecName) {
            inlineSpecs.push({
              datasetName: currentSpecName,
              category,
              source: file,
              inputParameters: [...currentInputParams],
              outputParameters: [...currentOutputParams],
            });
            currentSpecName = null;
            currentInputParams = [];
            currentOutputParams = [];
          }
          inOtherSpecsSection = false;
          inDatasetListSection = false;
        }
      }

      // Parse dataset tables
      if (inDatasetListSection && nt === "table") {
        const parsed = parseDatasetTable(node, category, file);
        datasets.push(...parsed);
      }

      // Parse inline specs
      if (inOtherSpecsSection) {
        if (nt === "heading-3") {
          // Save previous spec
          if (currentSpecName) {
            inlineSpecs.push({
              datasetName: currentSpecName,
              category,
              source: file,
              inputParameters: [...currentInputParams],
              outputParameters: [...currentOutputParams],
            });
          }
          currentSpecName = text;
          currentInputParams = [];
          currentOutputParams = [];
          expectingParams = null;
        } else if (nt === "paragraph") {
          const pText = text.toLowerCase();
          if (pText.includes("input param")) {
            expectingParams = "input";
          } else if (pText.includes("output param") || pText.includes("output")) {
            if (expectingParams === "input" || currentSpecName) {
              expectingParams = "output";
            }
          }
        } else if (nt === "table" && currentSpecName) {
          const fields = parseFieldTable(node);
          if (expectingParams === "input") {
            currentInputParams.push(...fields);
          } else if (expectingParams === "output") {
            currentOutputParams.push(...fields);
          } else {
            // Default: if no param section label, treat as output
            currentOutputParams.push(...fields);
          }
        }
      }
    }

    // Save last pending spec
    if (currentSpecName) {
      inlineSpecs.push({
        datasetName: currentSpecName,
        category,
        source: file,
        inputParameters: [...currentInputParams],
        outputParameters: [...currentOutputParams],
      });
    }

    const headings = extractHeadings(body).map((h) => `${h.level}: ${h.text}`);

    results.push({
      id: category,
      title,
      urlAlias,
      category,
      format,
      datasets,
      inlineSpecs,
      headings,
      downloadPdfUrl,
    });
  } catch (e: any) {
    errors.push({ file, error: e.message });
  }
}

// Write outputs
const outputDir = import.meta.dir;

writeFileSync(
  join(outputDir, "datasets.json"),
  JSON.stringify(
    {
      extractionDate: new Date().toISOString().split("T")[0],
      source: "https://docs.athenahealth.com/athenaone-dataexports/",
      totalApiFiles: apiFiles.length,
      totalExportTypes: results.length,
      totalDatasets: results.reduce((sum, r) => sum + r.datasets.length, 0),
      totalInlineSpecs: results.reduce((sum, r) => sum + r.inlineSpecs.length, 0),
      exportTypes: results,
    },
    null,
    2
  )
);

// Coverage
const coverage = {
  extractionDate: new Date().toISOString().split("T")[0],
  filesDiscovered: apiFiles.length,
  filesParsed: apiFiles.length - errors.length,
  parseFailures: errors,
  summary: {
    ambulatoryClinicalDatasets: results.find((r) => r.category === "ambulatory-clinical")?.datasets.length || 0,
    ambulatoryCollectorDatasets: results.find((r) => r.category === "ambulatory-collector")?.datasets.length || 0,
    inpatientClinicalDatasets: results.find((r) => r.category === "inpatient-clinical")?.datasets.length || 0,
    inpatientCollectorDatasets: results.find((r) => r.category === "inpatient-collector")?.datasets.length || 0,
    ambulatoryClinicalInlineSpecs: results.find((r) => r.category === "ambulatory-clinical")?.inlineSpecs.length || 0,
    ambulatoryCollectorInlineSpecs: results.find((r) => r.category === "ambulatory-collector")?.inlineSpecs.length || 0,
    inpatientClinicalInlineSpecs: results.find((r) => r.category === "inpatient-clinical")?.inlineSpecs.length || 0,
    inpatientCollectorInlineSpecs: results.find((r) => r.category === "inpatient-collector")?.inlineSpecs.length || 0,
  },
};

writeFileSync(join(outputDir, "coverage.json"), JSON.stringify(coverage, null, 2));

console.log("Extraction complete:");
console.log(`  Files parsed: ${coverage.filesParsed}/${coverage.filesDiscovered}`);
console.log(`  Parse failures: ${errors.length}`);
console.log(`  Export types: ${results.length}`);
console.log(`  Total datasets: ${results.reduce((sum, r) => sum + r.datasets.length, 0)}`);
console.log(`  Total inline specs: ${results.reduce((sum, r) => sum + r.inlineSpecs.length, 0)}`);
for (const r of results) {
  console.log(`  ${r.category}: ${r.datasets.length} datasets, ${r.inlineSpecs.length} inline specs, format=${r.format}, pdf=${r.downloadPdfUrl ? "yes" : "no"}`);
}
if (errors.length > 0) {
  console.log("Errors:");
  for (const e of errors) {
    console.log(`  ${e.file}: ${e.error}`);
  }
}
