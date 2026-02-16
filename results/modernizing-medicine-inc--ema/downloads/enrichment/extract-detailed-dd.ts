#!/usr/bin/env bun
/**
 * Extract structured field-level data from the ModMed EMA Detailed Data Dictionary PDF.
 *
 * Input:  ../detailed-dd-xml.xml  (pdftohtml -xml output)
 * Output: detailed-data-dictionary.json
 *
 * The PDF is a tabular spreadsheet (originally .xlsx exported via Google Sheets).
 * Every data row has an IDX number in the first column.
 *
 * IMPORTANT parsing note: pdftohtml sometimes merges the IDX and Grouping cells
 * into a single <text> element (e.g., "2533 eLab"). The parser must handle both
 * split and merged cases.
 *
 * Run:  bun run extract-detailed-dd.ts
 */

import { readFileSync, writeFileSync } from "fs";
import { resolve, dirname } from "path";

const scriptDir = dirname(new URL(import.meta.url).pathname);
const xmlPath = resolve(scriptDir, "../detailed-dd-xml.xml");
const outPath = resolve(scriptDir, "detailed-data-dictionary.json");

// Column left-position boundaries (determined empirically).
// The IDX column starts around left=34-43; Grouping around left=68+
// But they often merge into one <text> element starting at left=34.
const COL_BOUNDS = {
  // idx+grouping combined region
  idxGrouping:        { min: 30,  max: 153 },
  table:              { min: 153, max: 267 },
  column:             { min: 267, max: 404 },
  description:        { min: 404, max: 768 },
  dataType:           { min: 768, max: 830 },
  nullable:           { min: 830, max: 895 },
  fieldLength:        { min: 895, max: 993 },
  valuesCodingSchema: { min: 993, max: 1200 },
} as const;

type ColName = keyof typeof COL_BOUNDS;

interface FieldEntry {
  idx: number;
  grouping: string;
  table: string;
  column: string;
  description: string;
  dataType: string;
  nullable: boolean | null;
  fieldLength: number | null;
  valuesCodingSchema: string;
}

// ── Parse XML ──────────────────────────────────────────────────────

const xml = readFileSync(xmlPath, "utf-8");
const pageRegex = /<page\s+number="(\d+)"[^>]*>([\s\S]*?)<\/page>/g;

interface TextEl {
  globalTop: number;
  left: number;
  text: string;
}

const allElements: TextEl[] = [];
let totalPages = 0;
let pageMatch: RegExpExecArray | null;

while ((pageMatch = pageRegex.exec(xml)) !== null) {
  const pageNum = parseInt(pageMatch[1], 10);
  totalPages++;
  const pageContent = pageMatch[2];

  const textRegex =
    /<text\s+top="(\d+)"\s+left="(\d+)"\s+width="(\d+)"\s+height="(\d+)"\s+font="(\d+)">(.*?)<\/text>/g;

  let m: RegExpExecArray | null;
  while ((m = textRegex.exec(pageContent)) !== null) {
    const font = m[5];
    const top = parseInt(m[1], 10);
    // Skip header rows (font=1, bold) and page numbers / titles
    if (font === "1") continue;
    if (font === "0") continue; // title and page numbers use font 0
    if (top > 870 || top < 100) continue;

    const text = m[6]
      .replace(/<\/?b>/g, "")
      .replace(/<\/?i>/g, "")
      .replace(/<\/?a[^>]*>/g, "")
      .replace(/&amp;/g, "&")
      .replace(/&lt;/g, "<")
      .replace(/&gt;/g, ">")
      .replace(/&#(\d+);/g, (_, code: string) =>
        String.fromCharCode(parseInt(code))
      )
      .trim();
    if (!text) continue;

    allElements.push({
      globalTop: pageNum * 10000 + top,
      left: parseInt(m[2], 10),
      text,
    });
  }
}

// Sort by position
allElements.sort((a, b) => a.globalTop - b.globalTop || a.left - b.left);

// ── Build rows ─────────────────────────────────────────────────────
// A new row starts when we encounter text in the idxGrouping zone that
// begins with a number (the IDX).

interface PendingRow {
  idx: number;
  grouping: string;
  cells: Record<string, string[]>;
}

function newCells() {
  return {
    table: [] as string[],
    column: [] as string[],
    description: [] as string[],
    dataType: [] as string[],
    nullable: [] as string[],
    fieldLength: [] as string[],
    valuesCodingSchema: [] as string[],
  };
}

function classifyCol(left: number): ColName | null {
  for (const [name, { min, max }] of Object.entries(COL_BOUNDS)) {
    if (left >= min && left < max) return name as ColName;
  }
  return null;
}

// Parse "2533 eLab" or just "1" or "4223 PM Financials" etc.
function parseIdxGrouping(text: string): { idx: number; grouping: string } | null {
  const m = text.match(/^(\d+)\s*(.*)/);
  if (!m) return null;
  return { idx: parseInt(m[1], 10), grouping: m[2].trim() };
}

const rows: PendingRow[] = [];
let cur: PendingRow | null = null;

for (const el of allElements) {
  const col = classifyCol(el.left);
  if (!col) continue;

  if (col === "idxGrouping") {
    // Try to parse as start of new row
    const parsed = parseIdxGrouping(el.text);
    if (parsed) {
      if (cur) rows.push(cur);
      cur = { idx: parsed.idx, grouping: parsed.grouping, cells: newCells() };
      continue;
    }
    // If not a new row, could be a continuation of grouping text
    if (cur && !cur.grouping) {
      cur.grouping = el.text.trim();
    }
    continue;
  }

  if (!cur) continue;
  cur.cells[col]?.push(el.text);
}
if (cur) rows.push(cur);

console.log(`Parsed ${rows.length} raw rows from ${totalPages} pages`);

// ── Convert to typed entries ───────────────────────────────────────

function joinParts(parts: string[], noSpace = false): string {
  if (noSpace) return parts.join("").trim();
  return parts.join(" ").replace(/\s+/g, " ").trim();
}

const entries: FieldEntry[] = [];

for (const row of rows) {
  const table = joinParts(row.cells.table, true);
  const column = joinParts(row.cells.column, true);
  const description = joinParts(row.cells.description);
  const dataType = joinParts(row.cells.dataType);
  const nullableStr = joinParts(row.cells.nullable).toLowerCase();
  const fieldLengthStr = joinParts(row.cells.fieldLength);
  const valuesCodingSchema = joinParts(row.cells.valuesCodingSchema);

  if (!table && !column) continue;

  let nullable: boolean | null = null;
  if (nullableStr === "true") nullable = true;
  else if (nullableStr === "false") nullable = false;

  const fieldLength = fieldLengthStr ? parseInt(fieldLengthStr, 10) : null;

  entries.push({
    idx: row.idx,
    grouping: row.grouping,
    table,
    column,
    description,
    dataType,
    nullable,
    fieldLength: isNaN(fieldLength as number) ? null : fieldLength,
    valuesCodingSchema,
  });
}

// ── Propagate grouping/table ───────────────────────────────────────

let lastGrouping = "";
let lastTable = "";
for (const e of entries) {
  if (e.grouping) lastGrouping = e.grouping;
  else e.grouping = lastGrouping;
  if (e.table) lastTable = e.table;
  else e.table = lastTable;
}

// ── Statistics ─────────────────────────────────────────────────────

const tableSet = new Set(entries.map((e) => e.table).filter(Boolean));
const groupings: Record<string, number> = {};
for (const e of entries) {
  groupings[e.grouping || "(empty)"] = (groupings[e.grouping || "(empty)"] || 0) + 1;
}
const tableFieldCounts: Record<string, number> = {};
for (const e of entries) {
  tableFieldCounts[e.table] = (tableFieldCounts[e.table] || 0) + 1;
}

const stats = {
  totalPages,
  totalFields: entries.length,
  totalTables: tableSet.size,
  groupings,
  tableFieldCounts,
  parseFailures: [] as string[],
};

// ── Write ──────────────────────────────────────────────────────────

const output = {
  source: "ModMed-EMA-Detailed-Data-Dictionary.pdf",
  extractedAt: new Date().toISOString(),
  stats,
  tables: [...tableSet].sort(),
  fields: entries,
};

writeFileSync(outPath, JSON.stringify(output, null, 2));
console.log(`Wrote ${entries.length} fields across ${tableSet.size} tables`);
console.log("Groupings:", Object.entries(groupings).sort((a, b) => b[1] - a[1]).slice(0, 25));
