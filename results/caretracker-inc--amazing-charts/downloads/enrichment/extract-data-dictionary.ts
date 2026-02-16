#!/usr/bin/env bun
/**
 * Extracts the Amazing Charts EHI Export data dictionary from the PDF text.
 * Parses Data Class names and their column headings into queryable JSON.
 *
 * Usage: bun run extract-data-dictionary.ts
 * Input:  ../Amazing-Charts-EHI-Export-Documentation-V1_0-1-1.pdf (via pdftotext)
 * Output: data-dictionary.json
 */

import { execSync } from "child_process";
import { writeFileSync } from "fs";
import { resolve, dirname } from "path";

const scriptDir = dirname(new URL(import.meta.url).pathname);
const pdfPath = resolve(scriptDir, "../Amazing-Charts-EHI-Export-Documentation-V1_0-1-1.pdf");

const rawText = execSync(`pdftotext "${pdfPath}" -`, { encoding: "utf-8" });

interface DataClass {
  name: string;
  columns: string[];
  column_count: number;
}

// Known data class names confirmed by visual inspection of the PDF pages.
// These are used as delimiters to split the text stream, avoiding the problem
// where pdftotext merges trailing column names with the next data class name.
const KNOWN_DATA_CLASSES = [
  "Addendum",
  "Advance Directives",
  "Alerts",
  "Allergies and Intolerances Pending",
  "Allergies and Intolerances",
  "Assesments",
  "Billing History",
  "Care Team Members",
  "Clinical Notes",
  "Demographic Immunization",
  "Email",
  "FamilyHistory",
  "FunctionalStatus",
  "Goals",
  "Health Concerns",
  "Health Insurance",
  "HM Rules Ignored",
  "HM Rules",
  "Immunizations",
  "Implantable device",
  "Imported Items",
  "Injections",
  "Lab Tests",
  "List Problem Pending",
  "List Problem",
  "Medications Pending",
  "Medications",
  "Next Of Kin",
  "Occupation and Industry History",
  "Orders",
  "Patient Demographics",
  "Patient Generated Data",
  "Patient Health Information Capture",
  "Patient Record Release",
  "Plan of Treatment",
  "Procedures",
  "Referrals",
  "Risk Factors",
  "Scheduling",
  "Smoking Statuses",
  "Tracked Data",
  "Travel History",
  "User Defined Fields",
  "Vital Signs",
];

// Clean lines: remove page headers, footers, page numbers
const lines = rawText.split("\n");
const cleanLines: string[] = [];
const pageHeader = /^Amazing Charts EHI Export:.*v1\.0$/;
for (const line of lines) {
  const t = line.trim();
  if (!t) continue;
  if (pageHeader.test(t)) continue;
  if (/^\d+$/.test(t)) continue;
  cleanLines.push(t);
}

// Find where the data dictionary table starts
const tableHeaderIdx = cleanLines.findIndex(l => l === "Column Headings");
if (tableHeaderIdx === -1) {
  console.error("Could not find 'Column Headings' header");
  process.exit(1);
}

// Work line-by-line: match data class names only at line boundaries to avoid
// false positives where short names like "Email" appear inside column names.
const dataLines = cleanLines.slice(tableHeaderIdx + 1);

// Sort known names by length descending so multi-word names match first.
const sortedNames = [...KNOWN_DATA_CLASSES].sort((a, b) => b.length - a.length);

// Try to match a data class name starting at line index `start`.
// A name may span 1 or 2 lines (e.g., "Occupation and Industry" + "History").
function matchDataClassName(start: number): { name: string; linesConsumed: number } | null {
  const line1 = dataLines[start].trim();
  // Try two-line match first
  if (start + 1 < dataLines.length) {
    const combined = line1 + " " + dataLines[start + 1].trim();
    for (const name of sortedNames) {
      if (combined.toLowerCase() === name.toLowerCase()) {
        return { name, linesConsumed: 2 };
      }
    }
  }
  // Single-line match
  for (const name of sortedNames) {
    if (line1.toLowerCase() === name.toLowerCase()) {
      return { name, linesConsumed: 1 };
    }
  }
  return null;
}

// First pass: identify data class name positions
const entries: { name: string; startLine: number; columnStartLine: number }[] = [];
let i = 0;
while (i < dataLines.length) {
  const match = matchDataClassName(i);
  if (match) {
    entries.push({
      name: match.name,
      startLine: i,
      columnStartLine: i + match.linesConsumed,
    });
    i += match.linesConsumed;
  } else {
    i++;
  }
}

// Second pass: extract columns between each entry's columnStartLine and the next entry's startLine
const dataClasses: DataClass[] = [];
const parseFailures: { name: string; reason: string }[] = [];

for (let e = 0; e < entries.length; e++) {
  const entry = entries[e];
  const endLine = e + 1 < entries.length ? entries[e + 1].startLine : dataLines.length;
  const columnText = dataLines.slice(entry.columnStartLine, endLine).join(" ").trim();

  if (!columnText) {
    parseFailures.push({ name: entry.name, reason: "No column text found after name" });
    continue;
  }

  const cols = columnText
    .split(",")
    .map(c => c.replace(/\s+/g, " ").trim())
    .filter(c => c.length > 0);

  if (cols.length === 0) {
    parseFailures.push({ name: entry.name, reason: "Column text present but no columns parsed" });
    continue;
  }

  dataClasses.push({
    name: entry.name,
    columns: cols,
    column_count: cols.length,
  });
}

// Build output
const output = {
  source: "Amazing-Charts-EHI-Export-Documentation-V1_0-1-1.pdf",
  version: "v1.0",
  export_formats: ["csv", "json", "xml"],
  extraction_date: new Date().toISOString().split("T")[0],
  total_data_classes: dataClasses.length,
  total_columns: dataClasses.reduce((sum, dc) => sum + dc.column_count, 0),
  expected_data_classes: KNOWN_DATA_CLASSES.length,
  parse_failures: parseFailures,
  data_classes: dataClasses,
};

const outPath = resolve(scriptDir, "data-dictionary.json");
writeFileSync(outPath, JSON.stringify(output, null, 2));

console.log(`Extracted ${dataClasses.length}/${KNOWN_DATA_CLASSES.length} data classes with ${output.total_columns} total columns`);
if (parseFailures.length > 0) {
  console.log(`Parse failures: ${parseFailures.length}`);
  for (const f of parseFailures) {
    console.log(`  ${f.name}: ${f.reason}`);
  }
}
console.log(`Output: ${outPath}`);

console.log("\nData classes:");
for (const dc of dataClasses) {
  console.log(`  ${dc.name}: ${dc.column_count} columns`);
}
