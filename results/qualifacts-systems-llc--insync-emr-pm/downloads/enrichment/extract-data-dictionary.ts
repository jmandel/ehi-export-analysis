#!/usr/bin/env bun
/**
 * Extracts InSync EHI Export Data Dictionary from XLS into queryable JSON.
 *
 * Input:  ../InSync_EHI_Export_Data_Dictionary.xls
 * Output: data-dictionary.json  — all sections with fields
 *         extraction-stats.json — parse accounting
 */

import * as XLSX from "xlsx";
import { writeFileSync } from "fs";
import { resolve, dirname } from "path";

const scriptDir = dirname(new URL(import.meta.url).pathname);
const xlsPath = resolve(scriptDir, "../InSync_EHI_Export_Data_Dictionary.xls");
const wb = XLSX.readFile(xlsPath);

const SKIP_SHEETS = new Set(["Confidential Notice", "INDEX", "Changelogs"]);

interface Field {
  row_num: number;
  column_name: string;
  data_type: string;
  nullable: boolean;
  description: string;
  remarks: string;
}

interface Section {
  sheet_name: string;
  section_name: string;
  description: string;
  category: string;
  module: string;
  fields: Field[];
}

interface IndexEntry {
  row_num: number;
  section_name: string;
  category: string;
  module: string;
  details: string;
  remarks: string;
}

// Parse the INDEX sheet for category/module metadata
const indexSheet = wb.Sheets["INDEX"];
const indexData = XLSX.utils.sheet_to_json(indexSheet, {
  header: 1,
  defval: "",
}) as string[][];

const indexEntries: IndexEntry[] = [];
for (let i = 3; i < indexData.length; i++) {
  const row = indexData[i];
  if (!row[1]) continue;
  indexEntries.push({
    row_num: Number(row[0]) || i - 2,
    section_name: String(row[1]).trim(),
    category: String(row[2] || "").trim(),
    module: String(row[3] || "").trim(),
    details: String(row[4] || "").trim(),
    remarks: String(row[5] || "").trim(),
  });
}

// Build a lookup from sheet name prefix to index entry
function findIndexEntry(sheetName: string): IndexEntry | undefined {
  // Try exact match first, then prefix match (sheets are truncated at 31 chars)
  return (
    indexEntries.find(
      (e) => e.section_name.toLowerCase() === sheetName.toLowerCase()
    ) ||
    indexEntries.find((e) =>
      e.section_name.toLowerCase().startsWith(sheetName.toLowerCase())
    ) ||
    indexEntries.find((e) =>
      sheetName.toLowerCase().startsWith(e.section_name.toLowerCase().slice(0, 30))
    )
  );
}

// Parse the Changelogs sheet
const changelogSheet = wb.Sheets["Changelogs"];
const changelogData = XLSX.utils.sheet_to_json(changelogSheet, {
  header: 1,
  defval: "",
}) as any[][];

interface ChangelogEntry {
  row_num: number;
  changed_date: string;
  change_reason: string;
  changes_in_brief: string;
}

const changelogs: ChangelogEntry[] = [];
for (let i = 4; i < changelogData.length; i++) {
  const row = changelogData[i];
  if (!row[0] || !row[1]) continue;
  // Date might be a serial number
  let dateStr = String(row[1]);
  if (!isNaN(Number(row[1]))) {
    const d = XLSX.SSF.parse_date_code(Number(row[1]));
    dateStr = `${d.y}-${String(d.m).padStart(2, "0")}-${String(d.d).padStart(2, "0")}`;
  }
  changelogs.push({
    row_num: Number(row[0]),
    changed_date: dateStr,
    change_reason: String(row[2] || "").trim(),
    changes_in_brief: String(row[3] || "").trim(),
  });
}

// Parse each data sheet
const sections: Section[] = [];
const parseFailures: { sheet_name: string; error: string }[] = [];

for (const sheetName of wb.SheetNames) {
  if (SKIP_SHEETS.has(sheetName)) continue;

  try {
    const ws = wb.Sheets[sheetName];
    const data = XLSX.utils.sheet_to_json(ws, {
      header: 1,
      defval: "",
    }) as string[][];

    // Find the description (row 1, col 2)
    const description = String(data[1]?.[2] || "").trim();

    // Find the header row (contains "Name of the Column")
    let headerRowIdx = -1;
    for (let i = 0; i < Math.min(10, data.length); i++) {
      const row = data[i].map((c) => String(c).trim().toLowerCase());
      if (row.includes("name of the column")) {
        headerRowIdx = i;
        break;
      }
    }

    if (headerRowIdx === -1) {
      parseFailures.push({
        sheet_name: sheetName,
        error: "Could not find header row with 'Name of the Column'",
      });
      continue;
    }

    // Extract fields
    const fields: Field[] = [];
    for (let i = headerRowIdx + 1; i < data.length; i++) {
      const row = data[i];
      const colName = String(row[1] || "").trim();
      if (!colName) continue; // skip empty rows

      fields.push({
        row_num: Number(row[0]) || fields.length + 1,
        column_name: colName,
        data_type: String(row[2] || "").trim(),
        nullable: String(row[3] || "")
          .trim()
          .toLowerCase() === "yes",
        description: String(row[4] || "").trim(),
        remarks: String(row[5] || "").trim(),
      });
    }

    const indexEntry = findIndexEntry(sheetName);

    sections.push({
      sheet_name: sheetName,
      section_name: indexEntry?.section_name || sheetName,
      description,
      category: indexEntry?.category || "",
      module: indexEntry?.module || "",
      fields,
    });
  } catch (e: any) {
    parseFailures.push({
      sheet_name: sheetName,
      error: e.message || String(e),
    });
  }
}

// Build output
const output = {
  source: "InSync_EHI_Export_Data_Dictionary.xls",
  extracted_at: new Date().toISOString(),
  last_updated: "November 2025",
  changelogs,
  total_sections: sections.length,
  total_fields: sections.reduce((sum, s) => sum + s.fields.length, 0),
  sections,
};

const stats = {
  total_sheets: wb.SheetNames.length,
  skipped_sheets: Array.from(SKIP_SHEETS),
  sheets_parsed: sections.length,
  sheets_failed: parseFailures.length,
  parse_failures: parseFailures,
  total_fields: output.total_fields,
  sections_summary: sections.map((s) => ({
    section_name: s.section_name,
    sheet_name: s.sheet_name,
    category: s.category,
    module: s.module,
    field_count: s.fields.length,
  })),
};

writeFileSync(
  resolve(scriptDir, "data-dictionary.json"),
  JSON.stringify(output, null, 2)
);
writeFileSync(
  resolve(scriptDir, "extraction-stats.json"),
  JSON.stringify(stats, null, 2)
);

console.log(`Sections parsed: ${sections.length}`);
console.log(`Total fields: ${output.total_fields}`);
console.log(`Parse failures: ${parseFailures.length}`);
if (parseFailures.length > 0) {
  for (const f of parseFailures) {
    console.log(`  FAIL: ${f.sheet_name}: ${f.error}`);
  }
}
