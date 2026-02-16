/**
 * Extracts the b10_data_dictionary.xlsx into structured JSON files.
 *
 * Usage: bun run extract-data-dictionary.ts
 *
 * Input:  ../b10_data_dictionary.xlsx
 * Output: data-dictionary.json          — full structured extraction
 *         summary.json                  — coverage/accounting stats
 */

import * as XLSX from "xlsx";
import { writeFileSync } from "fs";
import { join, dirname } from "path";

const scriptDir = dirname(new URL(import.meta.url).pathname);
const inputPath = join(scriptDir, "..", "b10_data_dictionary.xlsx");
const outputDir = scriptDir;

interface Column {
  column_name: string;
  data_type: string;
  data_length: number | null;
  data_precision: number | null;
  data_scale: number | null;
  char_used: string | null;
  column_desc: string | null;
}

interface Table {
  table_name: string;
  table_desc: string | null;
  source_sheet: string;
  columns: Column[];
}

interface OntadaHealthField {
  field_name: string;
  data_type: string;
  description: string | null;
  notes: string | null;
}

interface OntadaHealthCollection {
  collection_name: string;
  source_sheet: string;
  fields: OntadaHealthField[];
}

interface DataDictionary {
  extraction_date: string;
  source_file: string;
  sheets: string[];
  tables: Table[];
  ontada_health_collections: OntadaHealthCollection[];
  stats: {
    total_sheets: number;
    total_tables: number;
    total_columns: number;
    tables_by_sheet: Record<string, number>;
    columns_by_sheet: Record<string, number>;
  };
}

// Read workbook
const wb = XLSX.readFile(inputPath);
console.log(`Loaded workbook with sheets: ${wb.SheetNames.join(", ")}`);

const tables: Table[] = [];
const ontadaCollections: OntadaHealthCollection[] = [];
const tablesBySheet: Record<string, number> = {};
const columnsBySheet: Record<string, number> = {};
let totalColumns = 0;

// --- Sheet 1: iKnowMed ---
{
  const ws = wb.Sheets["iKnowMed"];
  const rows: any[] = XLSX.utils.sheet_to_json(ws);
  const byTable = new Map<string, { desc: string | null; cols: Column[] }>();

  for (const row of rows) {
    const tableName = String(row.TABLE_NAME || "").trim();
    if (!tableName) continue;

    if (!byTable.has(tableName)) {
      byTable.set(tableName, {
        desc: row.TABLE_DESC ? String(row.TABLE_DESC).trim() : null,
        cols: [],
      });
    }

    byTable.get(tableName)!.cols.push({
      column_name: String(row.COLUMN_NAME || "").trim(),
      data_type: String(row.DATA_TYPE || "").trim(),
      data_length: row.DATA_LENGTH != null ? Number(row.DATA_LENGTH) : null,
      data_precision: null,
      data_scale: null,
      char_used: null,
      column_desc: row.COLUMN_DESC ? String(row.COLUMN_DESC).trim() : null,
    });
  }

  for (const [tableName, { desc, cols }] of byTable) {
    tables.push({
      table_name: tableName,
      table_desc: desc,
      source_sheet: "iKnowMed",
      columns: cols,
    });
  }

  tablesBySheet["iKnowMed"] = byTable.size;
  columnsBySheet["iKnowMed"] = rows.length;
  totalColumns += rows.length;
  console.log(`  iKnowMed: ${byTable.size} tables, ${rows.length} columns`);
}

// --- Sheet 2: VBC ---
{
  const ws = wb.Sheets["VBC"];
  const rows: any[] = XLSX.utils.sheet_to_json(ws);
  const byTable = new Map<string, Column[]>();

  for (const row of rows) {
    const tableName = String(row.table_name || "").trim();
    if (!tableName) continue;

    if (!byTable.has(tableName)) {
      byTable.set(tableName, []);
    }

    byTable.get(tableName)!.push({
      column_name: String(row.column_name || "").trim(),
      data_type: String(row.data_type || "").trim(),
      data_length: null,
      data_precision: null,
      data_scale: null,
      char_used: null,
      column_desc: null,
    });
  }

  for (const [tableName, cols] of byTable) {
    tables.push({
      table_name: tableName,
      table_desc: null,
      source_sheet: "VBC",
      columns: cols,
    });
  }

  tablesBySheet["VBC"] = byTable.size;
  columnsBySheet["VBC"] = rows.length;
  totalColumns += rows.length;
  console.log(`  VBC: ${byTable.size} tables, ${rows.length} columns`);
}

// --- Sheet 3: Patient History ---
{
  const ws = wb.Sheets["Patient History"];
  const rows: any[] = XLSX.utils.sheet_to_json(ws);
  const byTable = new Map<string, Column[]>();

  for (const row of rows) {
    const tableName = String(row.TABLE_NAME || "").trim();
    if (!tableName) continue;

    if (!byTable.has(tableName)) {
      byTable.set(tableName, []);
    }

    byTable.get(tableName)!.push({
      column_name: String(row.COLUMN_NAME || "").trim(),
      data_type: String(row.DATA_TYPE || "").trim(),
      data_length: row.DATA_LENGTH != null ? Number(row.DATA_LENGTH) : null,
      data_precision: row.DATA_PRECISION != null ? Number(row.DATA_PRECISION) : null,
      data_scale: row.DATA_SCALE != null ? Number(row.DATA_SCALE) : null,
      char_used: row.CHAR_USED ? String(row.CHAR_USED).trim() : null,
      column_desc: null,
    });
  }

  for (const [tableName, cols] of byTable) {
    tables.push({
      table_name: tableName,
      table_desc: null,
      source_sheet: "Patient History",
      columns: cols,
    });
  }

  tablesBySheet["Patient History"] = byTable.size;
  columnsBySheet["Patient History"] = rows.length;
  totalColumns += rows.length;
  console.log(`  Patient History: ${byTable.size} tables, ${rows.length} columns`);
}

// --- Sheet 4: Ontada Health ---
{
  const ws = wb.Sheets["Ontada Health"];
  const rows: any[] = XLSX.utils.sheet_to_json(ws);
  const byCollection = new Map<string, OntadaHealthField[]>();

  for (const row of rows) {
    const collName = String(row.Collection || "").trim();
    if (!collName) continue;

    if (!byCollection.has(collName)) {
      byCollection.set(collName, []);
    }

    byCollection.get(collName)!.push({
      field_name: String(row["Field Name"] || "").trim(),
      data_type: String(row["Data Type"] || "").trim(),
      description: row.Description ? String(row.Description).trim() : null,
      notes: row.Notes ? String(row.Notes).trim() : null,
    });
  }

  for (const [collName, fields] of byCollection) {
    ontadaCollections.push({
      collection_name: collName,
      source_sheet: "Ontada Health",
      fields,
    });
  }

  tablesBySheet["Ontada Health"] = byCollection.size;
  columnsBySheet["Ontada Health"] = rows.length;
  totalColumns += rows.length;
  console.log(`  Ontada Health: ${byCollection.size} collections, ${rows.length} fields`);
}

const totalTables = tables.length + ontadaCollections.length;

const dataDictionary: DataDictionary = {
  extraction_date: new Date().toISOString().split("T")[0],
  source_file: "b10_data_dictionary.xlsx",
  sheets: wb.SheetNames,
  tables,
  ontada_health_collections: ontadaCollections,
  stats: {
    total_sheets: wb.SheetNames.length,
    total_tables: totalTables,
    total_columns: totalColumns,
    tables_by_sheet: tablesBySheet,
    columns_by_sheet: columnsBySheet,
  },
};

// Write full data dictionary
const ddPath = join(outputDir, "data-dictionary.json");
writeFileSync(ddPath, JSON.stringify(dataDictionary, null, 2));
console.log(`\nWrote ${ddPath}`);

// Write summary
const summary = {
  extraction_date: dataDictionary.extraction_date,
  source_file: dataDictionary.source_file,
  total_sheets: dataDictionary.stats.total_sheets,
  total_tables: dataDictionary.stats.total_tables,
  total_columns: dataDictionary.stats.total_columns,
  tables_by_sheet: dataDictionary.stats.tables_by_sheet,
  columns_by_sheet: dataDictionary.stats.columns_by_sheet,
  parse_failures: [],
  table_list: tables.map((t) => ({
    name: t.table_name,
    sheet: t.source_sheet,
    column_count: t.columns.length,
    desc: t.table_desc,
  })),
  ontada_health_collection_list: ontadaCollections.map((c) => ({
    name: c.collection_name,
    sheet: c.source_sheet,
    field_count: c.fields.length,
  })),
};

const summaryPath = join(outputDir, "summary.json");
writeFileSync(summaryPath, JSON.stringify(summary, null, 2));
console.log(`Wrote ${summaryPath}`);

console.log(`\nDone. ${totalTables} entities, ${totalColumns} fields total.`);
