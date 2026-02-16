#!/usr/bin/env bun
/**
 * Extract structured data from the ModMed EMA EHI Export Data Dictionary PDF.
 *
 * Strategy: Use the non-layout pdftotext output and a state machine parser.
 * The PDF's table structure in non-layout text follows a predictable sequence:
 *   GroupingName → table_name → Description text → column_name lines → [Y|N|L|S]
 * Page breaks insert header lines (Grouping/Table/Description/Columns/Longitudinal/Tracking)
 * and page numbers + date footers that we strip in pass 1.
 *
 * Input: ../Data-Dictionary-for-ModMed-EMA-EHI-Export4.txt (pdftotext, no layout)
 * Output: data-dictionary.json, coverage-summary.json
 *
 * Run: cd downloads/enrichment && bun run extract-data-dictionary.ts
 */

import { readFileSync, writeFileSync } from "fs";
import { resolve, dirname } from "path";

const __dir = dirname(new URL(import.meta.url).pathname);
const inputPath = resolve(__dir, "../Data-Dictionary-for-ModMed-EMA-EHI-Export4.txt");
const outputPath = resolve(__dir, "data-dictionary.json");
const summaryPath = resolve(__dir, "coverage-summary.json");

const raw = readFileSync(inputPath, "utf-8");
const allLines = raw.split("\n");

interface TableDef {
  grouping: string;
  table_name: string;
  description: string;
  columns: string[];
  longitudinal_tracking: string;
}

const KNOWN_GROUPINGS = new Set([
  "Document Management",
  "Ophth Pretesting",
  "PM Financials",
  "Medical Lookup",
  "Office Flow",
  "Prescription",
  "Appointment",
  "Pathology",
  "Diagnosis",
  "Procedure",
  "Inventory",
  "Practice",
  "Patient",
  "CC/HPI",
  "Lookup",
  "Visit",
  "Exam",
  "MIPS",
  "eLab",
]);

// Also keep partial names for multiline groupings
const PARTIAL_GROUPINGS: Record<string, string> = {
  Ophth: "Ophth Pretesting",
  PM: "PM Financials",
  Document: "Document Management",
  Medical: "Medical Lookup",
  Office: "Office Flow",
};

// Find start of table data
let startIdx = 0;
for (let i = 0; i < allLines.length; i++) {
  if (allLines[i].startsWith("Database Tables & Columns:")) {
    startIdx = i + 1;
    break;
  }
}

// Pass 1: Strip page headers, page numbers, and date footers
const pageHeaderWords = new Set([
  "Grouping",
  "Table",
  "Description",
  "Columns",
  "Longitudinal",
  "Tracking",
]);

function isPageArtifact(line: string): boolean {
  const t = line.trim();
  if (t === "") return true;
  // Page numbers
  if (/^\d+$/.test(t) && parseInt(t) >= 2 && parseInt(t) <= 140) return true;
  // Date footer
  if (/^\d{1,2}\/\d{4}$/.test(t)) return true;
  // Page column headers
  if (pageHeaderWords.has(t)) return true;
  return false;
}

const cleanLines: string[] = [];
for (let i = startIdx; i < allLines.length; i++) {
  if (!isPageArtifact(allLines[i])) {
    cleanLines.push(allLines[i].trim());
  }
}

// Pass 2: Parse the clean sequence using a state machine
// Each table entry is:
//   GroupingName (matches KNOWN_GROUPINGS or is a partial)
//   table_name (snake_case)
//   Description (one or more lines of prose)
//   column_name (snake_case, one per line, may include description interleaved on same line from PDF)
//   Longitudinal tracking flag (Y, N, L, or S) — sometimes appears alone on a line

function isColumnName(s: string): boolean {
  return /^[a-z][a-z0-9_]+$/.test(s);
}

function isTableName(s: string): boolean {
  return /^[a-z][a-z0-9_]+$/.test(s);
}

function isTrackingFlag(s: string): boolean {
  return ["Y", "N", "L", "S"].includes(s);
}

function matchGrouping(line: string): string | null {
  if (KNOWN_GROUPINGS.has(line)) return line;
  if (PARTIAL_GROUPINGS[line]) return PARTIAL_GROUPINGS[line];
  return null;
}

const tables: TableDef[] = [];
let i = 0;

// Skip the "Pretesting" line if Ophth was already consumed
let skipPretesting = false;

while (i < cleanLines.length) {
  const line = cleanLines[i];

  // Try to match a grouping
  const grouping = matchGrouping(line);
  if (!grouping) {
    i++;
    continue;
  }

  // If this is a partial grouping ("Ophth"), skip the next line ("Pretesting")
  if (PARTIAL_GROUPINGS[line]) {
    const nextLine = cleanLines[i + 1]?.trim();
    // The second word might be on the next line
    if (nextLine === "Pretesting" || nextLine === "Financials" ||
        nextLine === "Management" || nextLine === "Lookup" || nextLine === "Flow") {
      i++; // skip the second part
    }
  }
  i++;

  // Now expect a table name
  while (i < cleanLines.length && !isTableName(cleanLines[i])) {
    // Skip any garbage between grouping and table name
    // But if we hit another grouping, back up
    if (matchGrouping(cleanLines[i])) break;
    i++;
  }
  if (i >= cleanLines.length || matchGrouping(cleanLines[i])) continue;

  const tableName = cleanLines[i];
  i++;

  // Now collect description lines and column names
  // The challenge: description text and column names are interleaved in the PDF extraction
  // because they come from different columns of the same visual row.
  //
  // Pattern from the text:
  // - Description text (non-snake_case, prose) comes first or interleaved
  // - Column names (snake_case) appear mixed in
  // - Finally a tracking flag (Y/N/L/S) or the next grouping signals end
  //
  // Strategy: collect all lines until we hit the next grouping or another table_name
  // that is preceded by a grouping. Separate columns from description by pattern.

  const descParts: string[] = [];
  const columns: string[] = [];
  let tracking = "";

  while (i < cleanLines.length) {
    const cl = cleanLines[i];

    // Is this the start of a new table entry?
    // Check if this line is a grouping followed by a table name
    if (matchGrouping(cl)) {
      // Look ahead: is the next non-empty line a table name?
      let ahead = i + 1;
      // Skip partial grouping continuations
      if (PARTIAL_GROUPINGS[cl]) ahead++;
      while (ahead < cleanLines.length && cleanLines[ahead] === "") ahead++;
      if (ahead < cleanLines.length && isTableName(cleanLines[ahead])) {
        // This is a new table entry, stop collecting for current table
        break;
      }
      // Otherwise this might be a grouping that appears in the middle somehow
      // (e.g., "Patient" could be a word in description)
      // Check: if the line is ONLY a grouping name and nothing else, it's likely a new entry
      if (KNOWN_GROUPINGS.has(cl) && isTableName(cleanLines[i + 1] || "")) {
        break;
      }
    }

    // Tracking flag
    if (isTrackingFlag(cl)) {
      if (!tracking) tracking = cl;
      i++;
      continue;
    }

    // Column name
    if (isColumnName(cl)) {
      columns.push(cl);
      i++;
      continue;
    }

    // Description text (or mixed content)
    // Some lines have a column name embedded at the start followed by description,
    // or description followed by column name
    // e.g. "Eyeglass prescriptions. One entry for each prescription, zero glasses_rx_id"
    // We need to split these

    // Check if line ends with what looks like a column name
    const words = cl.split(/\s+/);
    const lastWord = words[words.length - 1];
    if (words.length > 1 && isColumnName(lastWord)) {
      // Last word is a column name, rest is description
      columns.push(lastWord);
      const descPart = words.slice(0, -1).join(" ");
      if (descPart && !isTrackingFlag(descPart.trim())) {
        descParts.push(descPart);
      }
      i++;
      continue;
    }

    // Check if line starts with a column name followed by description
    const firstWord = words[0];
    if (words.length > 1 && isColumnName(firstWord)) {
      columns.push(firstWord);
      const descPart = words.slice(1).join(" ");
      if (descPart && !isTrackingFlag(descPart.trim())) {
        // This might be description continuation or could be noise
        // Only add if it looks like real description
        if (descPart.length > 10) {
          descParts.push(descPart);
        }
      }
      i++;
      continue;
    }

    // Pure description text
    descParts.push(cl);
    i++;
  }

  // Deduplicate columns and remove false positives
  // These words appear as column-like tokens but are actually description fragments
  const falsePositives = new Set([
    "information", "transaction", "table", "associated", "entry", "log",
    "code", "excluded",
  ]);
  const uniqueCols = [...new Set(columns)].filter(c => !falsePositives.has(c));

  tables.push({
    grouping,
    table_name: tableName,
    description: descParts.join(" ").replace(/\s+/g, " ").trim(),
    columns: uniqueCols,
    longitudinal_tracking: tracking,
  });
}

// Output
writeFileSync(outputPath, JSON.stringify(tables, null, 2));

// Summary
const groupingCounts: Record<string, number> = {};
let totalColumns = 0;
for (const t of tables) {
  groupingCounts[t.grouping] = (groupingCounts[t.grouping] || 0) + 1;
  totalColumns += t.columns.length;
}

const summary = {
  source_file: "Data-Dictionary-for-ModMed-EMA-EHI-Export4.pdf",
  extraction_date: new Date().toISOString().split("T")[0],
  total_tables: tables.length,
  total_columns: totalColumns,
  declared_but_empty_groupings: ["Lookup", "MIPS", "Medical Lookup"],
  groupings: Object.entries(groupingCounts)
    .sort((a, b) => b[1] - a[1])
    .map(([g, count]) => ({
      grouping: g,
      table_count: count,
      tables: tables
        .filter((t) => t.grouping === g)
        .map((t) => ({
          name: t.table_name,
          column_count: t.columns.length,
          longitudinal: t.longitudinal_tracking,
        })),
    })),
  parse_notes: [
    "Parsed from pdftotext (non-layout) output of the 131-page PDF",
    "Two-pass: strip page headers/footers, then state-machine parse",
    "Column names identified by snake_case pattern",
    "Description text separated from columns by pattern matching",
    "Duplicate columns removed",
  ],
};

writeFileSync(summaryPath, JSON.stringify(summary, null, 2));

console.log(`Extracted ${tables.length} tables with ${totalColumns} total columns`);
console.log("Grouping breakdown:");
for (const [g, count] of Object.entries(groupingCounts).sort(
  (a, b) => b[1] - a[1]
)) {
  const cols = tables
    .filter((t) => t.grouping === g)
    .reduce((s, t) => s + t.columns.length, 0);
  console.log(`  ${g}: ${count} tables, ${cols} columns`);
}
