#!/usr/bin/env bun
/**
 * Extracts table and column definitions from the NextGen Enterprise EHI
 * Data Dictionary PDF (pdftotext output).
 *
 * Input:  pdftotext plain-text dump of DD_Complete_EHI_20250627.pdf
 * Output: data-dictionary.json — array of { table, columns: [{ name, dataType, default, notNull }] }
 *         summary.json — coverage/accounting stats
 */

import { readFileSync, writeFileSync } from "fs";
import { execSync } from "child_process";
import { resolve, dirname } from "path";

const ENRICHMENT_DIR = dirname(new URL(import.meta.url).pathname);
const DOWNLOADS_DIR = resolve(ENRICHMENT_DIR, "..");
const PDF_PATH = resolve(DOWNLOADS_DIR, "DD_Complete_EHI_20250627.pdf");
const TXT_PATH = resolve(ENRICHMENT_DIR, "dd-raw.txt");

// Step 1: Extract text from PDF
console.log("Extracting text from PDF...");
execSync(`pdftotext "${PDF_PATH}" "${TXT_PATH}"`, { stdio: "inherit" });

const text = readFileSync(TXT_PATH, "utf-8");
const lines = text.split("\n");

interface Column {
  name: string;
  dataType: string;
  default: string | null;
  notNull: boolean;
}

interface Table {
  table: string;
  columns: Column[];
}

const tables: Table[] = [];
let currentTable: Table | null = null;
let inColumnSection = false;

// The PDF has a repeating structure per table:
//   "Table Name" line, followed by table name on same or next line
//   "Column Name" header line followed by "Data Type", "Default", "Not Null"
//   Then column rows until next "Table Name" or page footer

for (let i = 0; i < lines.length; i++) {
  const line = lines[i].trim();

  // Skip page footers and empty lines
  if (!line) continue;
  if (/^Thursday,/.test(line)) continue;
  if (/^Page \d+ of \d+/.test(line)) continue;
  if (/^Electronic Health Information/.test(line)) continue;
  if (/^\(EHI\) Data Dictionary/.test(line)) continue;
  if (/^for NextGen/.test(line)) continue;
  if (/^LEGAL NOTICE/.test(line)) continue;
  if (/^Although we exercised/.test(line)) continue;
  if (/^© 20\d\d/.test(line)) continue;
  if (/^The registered trademarks/.test(line)) continue;
  if (/^Our issued/.test(line)) continue;
  if (/^Tables and Columns/.test(line)) continue;

  // Detect table name - format: "Table Name    tablename_"
  // The table names in this PDF end with underscore
  if (line.startsWith("Table Name")) {
    const match = line.match(/Table Name\s+(\S+)/);
    if (match) {
      currentTable = { table: match[1], columns: [] };
      tables.push(currentTable);
      inColumnSection = false;
    }
    continue;
  }

  // Detect column header
  if (line === "Column Name" || line.startsWith("Column Name")) {
    inColumnSection = true;
    continue;
  }

  // Skip sub-headers
  if (line === "Data Type" || line === "Default" || line === "Not Null") continue;

  // Parse column rows - they appear as sequences of:
  // column_name (on one line) followed by data_type, possibly default, possibly checkbox
  // But pdftotext flattens these. We need to identify column names vs data types.
  
  if (currentTable && inColumnSection) {
    // Known SQL Server data types
    const dataTypes = [
      "char", "varchar", "nvarchar", "text", "ntext",
      "int", "smallint", "tinyint", "bigint", "float", "real", "numeric", "decimal", "money", "smallmoney",
      "datetime", "datetime2", "date", "time", "smalldatetime", "datetimeoffset",
      "bit", "binary", "varbinary", "image",
      "uniqueidentifier", "xml", "sql_variant", "timestamp",
    ];

    if (dataTypes.includes(line.toLowerCase())) {
      // This is a data type for the previous column
      if (currentTable.columns.length > 0) {
        const lastCol = currentTable.columns[currentTable.columns.length - 1];
        if (!lastCol.dataType) {
          lastCol.dataType = line.toLowerCase();
        }
      }
      continue;
    }

    // Default values like (getdate()), ((0)), etc.
    if (/^\(.*\)$/.test(line)) {
      if (currentTable.columns.length > 0) {
        const lastCol = currentTable.columns[currentTable.columns.length - 1];
        lastCol.default = line;
      }
      continue;
    }

    // Skip checkbox indicators (they don't appear well in text extraction)
    if (line === "✓" || line === "☐" || line === "☑") continue;

    // If it looks like a column name (contains letters/underscores, no spaces typically)
    if (/^[a-zA-Z_][a-zA-Z0-9_]*$/.test(line) && !dataTypes.includes(line.toLowerCase())) {
      currentTable.columns.push({
        name: line,
        dataType: "",
        default: null,
        notNull: false,
      });
    }
  }
}

// Post-process: try to pair columns with their data types using a second pass
// The pdftotext output interleaves column names and data types.
// Let's re-parse with a smarter approach.

const tables2: Table[] = [];
let currentTable2: Table | null = null;

const dataTypeSet = new Set([
  "char", "varchar", "nvarchar", "text", "ntext",
  "int", "smallint", "tinyint", "bigint", "float", "real", "numeric", "decimal", "money", "smallmoney",
  "datetime", "datetime2", "date", "time", "smalldatetime", "datetimeoffset",
  "bit", "binary", "varbinary", "image",
  "uniqueidentifier", "xml", "sql_variant", "timestamp",
]);

const skipLines = new Set([
  "Column Name", "Data Type", "Default", "Not Null",
  "Tables and Columns", "",
]);

// Collect all non-noise tokens in order per table
type Token = { type: "table", name: string } | { type: "col", name: string } | { type: "dtype", name: string } | { type: "default", value: string };

const tokens: Token[] = [];
let expectTableName = false;

for (let i = 0; i < lines.length; i++) {
  const line = lines[i].trim();
  if (!line) continue;
  if (/^Thursday,/.test(line)) continue;
  if (/^Page \d+ of \d+/.test(line)) continue;
  if (/^Electronic Health Information/.test(line)) continue;
  if (/^\(EHI\) Data Dictionary/.test(line)) continue;
  if (/^for NextGen/.test(line)) continue;
  if (/^LEGAL NOTICE/.test(line)) continue;
  if (/^Although we exercised/.test(line)) continue;
  if (/2025 NXGN/.test(line)) continue;
  if (/^The registered trademarks/.test(line)) continue;
  if (/^Our issued/.test(line)) continue;
  if (skipLines.has(line)) continue;

  // "Table Name" appears on its own line, followed by the actual table name on the next non-empty line
  if (line === "Table Name") {
    expectTableName = true;
    continue;
  }

  if (expectTableName) {
    tokens.push({ type: "table", name: line });
    expectTableName = false;
    continue;
  }

  if (dataTypeSet.has(line.toLowerCase())) {
    tokens.push({ type: "dtype", name: line.toLowerCase() });
    continue;
  }

  if (/^\(.*\)$/.test(line)) {
    tokens.push({ type: "default", value: line });
    continue;
  }

  if (/^[a-zA-Z_][a-zA-Z0-9_]*$/.test(line)) {
    tokens.push({ type: "col", name: line });
  }
}

// Now build tables from tokens
let tbl: Table | null = null;
for (const tok of tokens) {
  if (tok.type === "table") {
    tbl = { table: tok.name, columns: [] };
    tables2.push(tbl);
  } else if (tok.type === "col" && tbl) {
    tbl.columns.push({ name: tok.name, dataType: "", default: null, notNull: false });
  } else if (tok.type === "dtype" && tbl && tbl.columns.length > 0) {
    // Assign to last column without a data type
    for (let j = tbl.columns.length - 1; j >= 0; j--) {
      if (!tbl.columns[j].dataType) {
        tbl.columns[j].dataType = tok.name;
        break;
      }
    }
  } else if (tok.type === "default" && tbl && tbl.columns.length > 0) {
    const last = tbl.columns[tbl.columns.length - 1];
    last.default = tok.value;
  }
}

// Write outputs
const outputPath = resolve(ENRICHMENT_DIR, "data-dictionary.json");
writeFileSync(outputPath, JSON.stringify(tables2, null, 2));

const totalColumns = tables2.reduce((sum, t) => sum + t.columns.length, 0);
const tablesWithTypes = tables2.filter(t => t.columns.some(c => c.dataType));

const summary = {
  extractionDate: new Date().toISOString(),
  sourceFile: "DD_Complete_EHI_20250627.pdf",
  sourcePages: 10875,
  totalTables: tables2.length,
  totalColumns,
  tablesWithDataTypes: tablesWithTypes.length,
  columnsWithDataTypes: tables2.reduce((sum, t) => sum + t.columns.filter(c => c.dataType).length, 0),
  columnsWithDefaults: tables2.reduce((sum, t) => sum + t.columns.filter(c => c.default).length, 0),
  sampleTables: tables2.slice(0, 5).map(t => ({
    table: t.table,
    columnCount: t.columns.length,
    sampleColumns: t.columns.slice(0, 5).map(c => `${c.name} (${c.dataType})`),
  })),
  limitations: [
    "PDF text extraction may lose some formatting - checkbox (Not Null) values are not reliably captured",
    "Column-to-datatype pairing relies on sequential ordering in pdftotext output",
    "No field descriptions available - the source PDF only contains column names and data types",
    "Table relationships/foreign keys are not documented in the source PDF",
  ],
};

writeFileSync(resolve(ENRICHMENT_DIR, "summary.json"), JSON.stringify(summary, null, 2));

console.log(`Extracted ${tables2.length} tables with ${totalColumns} total columns`);
console.log(`Tables with data types: ${tablesWithTypes.length}`);
console.log(`Output: data-dictionary.json, summary.json`);
