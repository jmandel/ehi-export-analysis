#!/usr/bin/env bun
/**
 * Extracts structured data from VersaSuite EHI Export Data Dictionary HTML pages.
 *
 * Input:  ../data-dictionary/*.html (97 files including index.html)
 * Output: ./data-dictionary.json           — full structured extraction
 *         ./data-dictionary-summary.json   — coverage/accounting summary
 */

import { readdirSync, readFileSync, writeFileSync } from "fs";
import { join, basename } from "path";

const DATA_DIR = join(import.meta.dir, "..", "data-dictionary");
const OUT_DIR = import.meta.dir;

interface Column {
  original_name: string;
  expanded_name: string;
  description: string;
}

interface Table {
  file_name: string;
  table_name: string | null;        // inferred CSV table name (e.g. "HC_Pt")
  page_title: string | null;        // h1/h2 title text
  csv_file_name: string | null;     // explicit CSV file reference if found
  prefix: string | null;            // table prefix (AP_, HC_, VE_, etc.)
  domain_hint: string | null;       // inferred domain from prefix/title
  columns: Column[];
  column_count: number;
  has_patient_id: boolean;
  has_encounter_id: boolean;
  has_audit_fields: boolean;
  description_quality: "good" | "mixed" | "poor";
}

interface Summary {
  total_files_discovered: number;
  total_files_parsed: number;
  parse_failures: { file: string; error: string }[];
  index_file_skipped: boolean;
  tables_extracted: number;
  total_columns: number;
  columns_with_placeholder_descriptions: number;
  description_quality_distribution: Record<string, number>;
  prefix_distribution: Record<string, number>;
  domain_distribution: Record<string, number>;
  tables_with_patient_id: number;
  tables_with_encounter_id: number;
}

// Prefix to domain mapping
const PREFIX_DOMAINS: Record<string, string> = {
  AP_: "Administrative/Patient",
  AX_: "Accounting/Financial",
  HC_: "Healthcare/Clinical",
  EM_: "Encounter Management",
  FQ_: "Financial/Quality",
  VE_: "EHR Exam/Template",
};

function inferTableName(fileName: string): string | null {
  // Remove .html extension
  let name = fileName.replace(/\.html$/, "");
  // Try to extract a table-like name (AP_xxx, HC_xxx, etc.)
  const match = name.match(/\b(AP_\w+|AX_\w+|HC_\w+|EM_\w+|FQ_\w+|VE_\w+)\b/);
  if (match) return match[1];
  // Otherwise use cleaned file name
  return name;
}

function inferCsvName(html: string, fileName: string): string | null {
  // Look for "Documentation for X.csv" pattern
  const csvMatch = html.match(/Documentation for (\S+\.csv)/i);
  if (csvMatch) return csvMatch[1];
  // Look for table name references
  const tableMatch = html.match(/(?:AP|AX|HC|EM|FQ|VE)_\w+\.csv/);
  if (tableMatch) return tableMatch[0];
  return null;
}

function extractTitle(html: string): string | null {
  // Get first h1 or h2
  const h1Match = html.match(/<h1[^>]*>(.*?)<\/h1>/is);
  const h2Match = html.match(/<h2[^>]*>(.*?)<\/h2>/is);
  const title = h1Match?.[1] || h2Match?.[1] || null;
  if (title) return title.replace(/<[^>]*>/g, "").trim();
  return null;
}

function parseTable(html: string): Column[] {
  const columns: Column[] = [];
  // Match table rows (skip header)
  const rowRegex = /<tr[^>]*>\s*<td[^>]*>(.*?)<\/td>\s*<td[^>]*>(.*?)<\/td>\s*<td[^>]*>(.*?)<\/td>\s*<\/tr>/gis;
  let match;
  while ((match = rowRegex.exec(html)) !== null) {
    const original = match[1].replace(/<[^>]*>/g, "").trim();
    const expanded = match[2].replace(/<[^>]*>/g, "").trim();
    const desc = match[3].replace(/<[^>]*>/g, "").trim();
    if (original && original !== "Original Column Name") {
      columns.push({
        original_name: original,
        expanded_name: expanded,
        description: desc,
      });
    }
  }
  return columns;
}

function isPlaceholderDescription(desc: string): boolean {
  const lower = desc.toLowerCase();
  return (
    lower.startsWith("provides information related to") ||
    lower.startsWith("contains detailed information or identifiers for the corresponding") ||
    lower.startsWith("specifies the date associated with the") ||
    lower.startsWith("records the historical data or changes related to the") ||
    lower === ""
  );
}

function assessDescriptionQuality(columns: Column[]): "good" | "mixed" | "poor" {
  if (columns.length === 0) return "poor";
  const placeholderCount = columns.filter((c) =>
    isPlaceholderDescription(c.description)
  ).length;
  const ratio = placeholderCount / columns.length;
  if (ratio < 0.2) return "good";
  if (ratio < 0.6) return "mixed";
  return "poor";
}

function inferPrefix(tableName: string | null): string | null {
  if (!tableName) return null;
  const match = tableName.match(/^(AP_|AX_|HC_|EM_|FQ_|VE_)/);
  return match ? match[1] : null;
}

function inferDomain(prefix: string | null, title: string | null): string | null {
  if (prefix && PREFIX_DOMAINS[prefix]) return PREFIX_DOMAINS[prefix];
  if (title) {
    const lower = title.toLowerCase();
    if (lower.includes("billing") || lower.includes("statement") || lower.includes("charge"))
      return "Billing/Financial";
    if (lower.includes("clinical") || lower.includes("patient") || lower.includes("encounter"))
      return "Healthcare/Clinical";
    if (lower.includes("address") || lower.includes("contact") || lower.includes("phone"))
      return "Administrative/Patient";
    if (lower.includes("lab")) return "Laboratory";
    if (lower.includes("drug") || lower.includes("medication") || lower.includes("allergy"))
      return "Pharmacy/Medications";
  }
  return "Unknown";
}

// Main extraction
const allFiles = readdirSync(DATA_DIR).filter((f) => f.endsWith(".html"));
const tables: Table[] = [];
const failures: { file: string; error: string }[] = [];
let totalPlaceholderDescs = 0;

for (const file of allFiles) {
  if (file === "index.html") continue; // Skip index

  try {
    const html = readFileSync(join(DATA_DIR, file), "utf-8");
    const columns = parseTable(html);

    if (columns.length === 0) {
      failures.push({ file, error: "No table rows found" });
      continue;
    }

    const tableName = inferTableName(file);
    const title = extractTitle(html);
    const csvName = inferCsvName(html, file);
    const prefix = inferPrefix(tableName);
    const domain = inferDomain(prefix, title);
    const quality = assessDescriptionQuality(columns);

    const placeholderCount = columns.filter((c) =>
      isPlaceholderDescription(c.description)
    ).length;
    totalPlaceholderDescs += placeholderCount;

    tables.push({
      file_name: file,
      table_name: tableName,
      page_title: title,
      csv_file_name: csvName,
      prefix,
      domain_hint: domain,
      columns,
      column_count: columns.length,
      has_patient_id: columns.some(
        (c) => c.original_name === "PtID" || c.original_name === "PatientID"
      ),
      has_encounter_id: columns.some(
        (c) => c.original_name === "PtEncID" || c.original_name === "EncounterID"
      ),
      has_audit_fields: columns.some((c) => c.original_name.startsWith("ZU")),
      description_quality: quality,
    });
  } catch (err: any) {
    failures.push({ file, error: err.message });
  }
}

// Build summary
const prefixDist: Record<string, number> = {};
const domainDist: Record<string, number> = {};
const qualityDist: Record<string, number> = { good: 0, mixed: 0, poor: 0 };

for (const t of tables) {
  const p = t.prefix || "none";
  prefixDist[p] = (prefixDist[p] || 0) + 1;
  const d = t.domain_hint || "Unknown";
  domainDist[d] = (domainDist[d] || 0) + 1;
  qualityDist[t.description_quality]++;
}

const totalColumns = tables.reduce((s, t) => s + t.column_count, 0);

const summary: Summary = {
  total_files_discovered: allFiles.length,
  total_files_parsed: tables.length,
  parse_failures: failures,
  index_file_skipped: allFiles.includes("index.html"),
  tables_extracted: tables.length,
  total_columns: totalColumns,
  columns_with_placeholder_descriptions: totalPlaceholderDescs,
  description_quality_distribution: qualityDist,
  prefix_distribution: prefixDist,
  domain_distribution: domainDist,
  tables_with_patient_id: tables.filter((t) => t.has_patient_id).length,
  tables_with_encounter_id: tables.filter((t) => t.has_encounter_id).length,
};

// Write outputs
writeFileSync(
  join(OUT_DIR, "data-dictionary.json"),
  JSON.stringify(tables, null, 2)
);
writeFileSync(
  join(OUT_DIR, "data-dictionary-summary.json"),
  JSON.stringify(summary, null, 2)
);

console.log(`Extracted ${tables.length} tables with ${totalColumns} total columns`);
console.log(`Parse failures: ${failures.length}`);
if (failures.length > 0) {
  for (const f of failures) console.log(`  - ${f.file}: ${f.error}`);
}
console.log(`Description quality: good=${qualityDist.good}, mixed=${qualityDist.mixed}, poor=${qualityDist.poor}`);
console.log(`Placeholder descriptions: ${totalPlaceholderDescs}/${totalColumns} (${((totalPlaceholderDescs/totalColumns)*100).toFixed(1)}%)`);
console.log(`Tables with PtID: ${summary.tables_with_patient_id}/${tables.length}`);
console.log(`Tables with PtEncID: ${summary.tables_with_encounter_id}/${tables.length}`);
console.log(`\nPrefix distribution:`);
for (const [k, v] of Object.entries(prefixDist).sort((a, b) => b[1] - a[1])) {
  console.log(`  ${k}: ${v}`);
}
console.log(`\nDomain distribution:`);
for (const [k, v] of Object.entries(domainDist).sort((a, b) => b[1] - a[1])) {
  console.log(`  ${k}: ${v}`);
}
