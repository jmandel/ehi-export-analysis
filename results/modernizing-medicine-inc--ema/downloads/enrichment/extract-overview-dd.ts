#!/usr/bin/env bun
/**
 * Extract structured table-level inventory from the ModMed EMA EHI Export
 * Data Dictionary overview PDF (the first/main PDF, 96 pages).
 *
 * Input:  ../overview-dd-xml.xml  (pdftohtml -xml output)
 * Output: overview-table-inventory.json
 *
 * The "Database Tables" section (pages 5-77) lists every table with:
 *   IDX, Grouping, Table, Description, Relationships,
 *   Longitudinal Tracking, Product/Vertical, Financial Priority Delivery,
 *   Refresh Frequency
 *
 * Run:  bun run extract-overview-dd.ts
 */

import { readFileSync, writeFileSync } from "fs";
import { resolve, dirname } from "path";

const scriptDir = dirname(new URL(import.meta.url).pathname);
const xmlPath = resolve(scriptDir, "../overview-dd-xml.xml");
const outPath = resolve(scriptDir, "overview-table-inventory.json");

// Column boundaries for the table inventory pages
const COL_BOUNDS = {
  idxGrouping:       { min: 30,  max: 210 },
  table:             { min: 210, max: 410 },
  description:       { min: 410, max: 620 },
  relationships:     { min: 620, max: 820 },
  longitudinal:      { min: 820, max: 920 },
  productVertical:   { min: 920, max: 1000 },
  financialPriority: { min: 1000, max: 1070 },
  refreshFrequency:  { min: 1070, max: 1200 },
} as const;

type ColName = keyof typeof COL_BOUNDS;

interface TableEntry {
  idx: number;
  grouping: string;
  table: string;
  description: string;
  relationships: string[];
  longitudinalTracking: string;
  productVertical: string;
  financialPriority: string;
  refreshFrequency: string;
}

const xml = readFileSync(xmlPath, "utf-8");
const pageRegex = /<page\s+number="(\d+)"[^>]*>([\s\S]*?)<\/page>/g;

interface TextEl {
  globalTop: number;
  left: number;
  text: string;
  font: string;
}

const allElements: TextEl[] = [];
let totalPages = 0;
let pageMatch: RegExpExecArray | null;

while ((pageMatch = pageRegex.exec(xml)) !== null) {
  const pageNum = parseInt(pageMatch[1], 10);
  totalPages++;

  // Only process pages 5-77 (the table inventory section)
  if (pageNum < 5 || pageNum > 77) continue;

  const pageContent = pageMatch[2];
  const textRegex =
    /<text\s+top="(\d+)"\s+left="(\d+)"\s+width="(\d+)"\s+height="(\d+)"\s+font="(\d+)">(.*?)<\/text>/g;

  let m: RegExpExecArray | null;
  while ((m = textRegex.exec(pageContent)) !== null) {
    const font = m[5];
    const top = parseInt(m[1], 10);
    if (top > 830 || top < 100) continue;

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
      font,
    });
  }
}

allElements.sort((a, b) => a.globalTop - b.globalTop || a.left - b.left);

function classifyCol(left: number): ColName | null {
  for (const [name, { min, max }] of Object.entries(COL_BOUNDS)) {
    if (left >= min && left < max) return name as ColName;
  }
  return null;
}

function parseIdxGrouping(text: string): { idx: number; grouping: string } | null {
  const m = text.match(/^(\d+)\s+(.*)/);
  if (!m) return null;
  return { idx: parseInt(m[1], 10), grouping: m[2].trim() };
}

interface PendingRow {
  idx: number;
  grouping: string;
  cells: Record<string, string[]>;
}

function newCells() {
  return {
    table: [] as string[],
    description: [] as string[],
    relationships: [] as string[],
    longitudinal: [] as string[],
    productVertical: [] as string[],
    financialPriority: [] as string[],
    refreshFrequency: [] as string[],
  };
}

const rows: PendingRow[] = [];
let cur: PendingRow | null = null;

for (const el of allElements) {
  // Skip bold header rows
  if (el.font === "1") continue;

  const col = classifyCol(el.left);
  if (!col) continue;

  if (col === "idxGrouping") {
    const parsed = parseIdxGrouping(el.text);
    if (parsed) {
      if (cur) rows.push(cur);
      cur = { idx: parsed.idx, grouping: parsed.grouping, cells: newCells() };
      continue;
    }
    // Could be continuation of grouping text for multiline groupings like "Document Management"
    if (cur) {
      cur.grouping += " " + el.text.trim();
    }
    continue;
  }

  if (!cur) continue;
  cur.cells[col]?.push(el.text);
}
if (cur) rows.push(cur);

console.log(`Parsed ${rows.length} table entries from ${totalPages} pages`);

// Convert to entries
const entries: TableEntry[] = rows.map((row) => ({
  idx: row.idx,
  grouping: row.grouping.replace(/\s+/g, " ").trim(),
  table: row.cells.table.join("").trim(),
  description: row.cells.description.join(" ").replace(/\s+/g, " ").trim(),
  relationships: row.cells.relationships
    .join(" ")
    .split(/\s+/)
    .filter(Boolean)
    .filter((r) => r !== "N" && r !== "Y" && r !== "L" && r !== "S"),
  longitudinalTracking: row.cells.longitudinal.join(" ").trim(),
  productVertical: row.cells.productVertical.join(" ").trim(),
  financialPriority: row.cells.financialPriority.join(" ").trim(),
  refreshFrequency: row.cells.refreshFrequency.join(" ").trim(),
}));

// Propagate grouping
let lastG = "";
for (const e of entries) {
  if (e.grouping) lastG = e.grouping;
  else e.grouping = lastG;
}

// Stats
const groupCounts: Record<string, number> = {};
for (const e of entries) {
  groupCounts[e.grouping] = (groupCounts[e.grouping] || 0) + 1;
}

const output = {
  source: "ModMed-EMA-EHI-Export-Data-Dictionary.pdf (pages 5-77)",
  extractedAt: new Date().toISOString(),
  stats: {
    totalPages,
    totalTables: entries.length,
    groupCounts,
  },
  tables: entries,
};

writeFileSync(outPath, JSON.stringify(output, null, 2));
console.log(`Wrote ${entries.length} tables to ${outPath}`);
console.log("Groups:", groupCounts);
