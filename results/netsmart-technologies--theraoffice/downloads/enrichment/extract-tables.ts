#!/usr/bin/env bun
/**
 * Extract table and column definitions from the TheraOffice EHI Export PDF.
 *
 * Usage:
 *   bun run extract-tables.ts
 *
 * Input:  ../ehi_tables/EHI Export All Tables - May 2024 (TheraOffice).pdf
 *         (via pdftotext)
 * Output: tables-catalog.json   — structured table/column definitions
 *         coverage-accounting.json — parse statistics
 */

import { $ } from "bun";

const PDF_PATH = decodeURIComponent(new URL(
  "../ehi_tables/EHI Export All Tables - May 2024 (TheraOffice).pdf",
  import.meta.url
).pathname);

const OUT_DIR = decodeURIComponent(new URL(".", import.meta.url).pathname);

// Extract text from PDF using pdftotext
const raw = await $`pdftotext ${PDF_PATH} -`.text();

interface Column {
  name: string;
  data_type: string;
  max_length: number;
}

interface Table {
  name: string;
  columns: Column[];
  total_columns: number;
}

// Parse the PDF text into table structures.
// The format is:
//   TABLE_NAME
//   Columns
//   Name    Data type    Max length
//   COL1    type1        len1
//   ...
//   Total: N column(s)

const lines = raw.split("\n");
const tables: Table[] = [];
let currentTable: Table | null = null;
let inColumns = false;
let headerSeen = false;

// Known table names from the TOC
const knownTables = new Set([
  "PAT_PROFILE",
  "PAT_PROFILE_CORE",
  "PAT_PROFILE_CORE_ETHNICITY",
  "PAT_PROFILE_CORE_GENDER",
  "PAT_PROFILE_CORE_RACE",
  "PAT_PROFILE_USCDI_ALLERGIES",
  "PAT_PROFILE_USCDI_FAMILY_HISTORY",
  "PAT_PROFILE_USCDI_FAMILY_MEMBER",
  "PAT_PROFILE_USCDI_GOALS",
  "PAT_PROFILE_USCDI_IMMUNIZATIONS",
  "PAT_PROFILE_USCDI_IMMUNIZATIONS_ACKNOWLEDGEMENT",
  "PAT_PROFILE_USCDI_IMPLANTDEVS",
  "PAT_PROFILE_USCDI_LABS",
  "PAT_PROFILE_USCDI_MEDICATIONS",
  "PAT_PROFILE_USCDI_PROBLEMS",
  "PAT_PROFILE_USCDI_PROCEDURES",
  "PAT_PROFILE_USCDI_PROGRAM_ADMISSION",
  "PAT_PROFILE_USCDI_VITALSIGNS",
  "PTCASE",
]);

// SQL Server data types we expect
const sqlTypes = new Set([
  "int",
  "varchar",
  "smalldatetime",
  "datetime",
  "tinyint",
  "smallint",
  "bit",
  "decimal",
  "char",
  "uniqueidentifier",
]);

for (let i = 0; i < lines.length; i++) {
  const line = lines[i].trim();

  // Skip empty lines and copyright footers
  if (!line || line.startsWith("Confidential.") || /^\d+$/.test(line)) continue;

  // Detect table name
  if (knownTables.has(line)) {
    if (currentTable) {
      tables.push(currentTable);
    }
    currentTable = { name: line, columns: [], total_columns: 0 };
    inColumns = false;
    headerSeen = false;
    continue;
  }

  // Detect start of columns section
  if (line === "Columns" && currentTable) {
    inColumns = true;
    continue;
  }

  // Skip the header row
  if (inColumns && !headerSeen && line.startsWith("Name")) {
    headerSeen = true;
    continue;
  }

  // Detect total line
  const totalMatch = line.match(/^Total:\s+(\d+)\s+column/);
  if (totalMatch && currentTable) {
    currentTable.total_columns = parseInt(totalMatch[1]);
    inColumns = false;
    continue;
  }

  // Parse column definitions. In the extracted text, each column's fields
  // appear on separate lines: NAME, then data_type, then max_length.
  // We handle both same-line (tab/space-separated) and multi-line formats.
  if (inColumns && headerSeen && currentTable) {
    // Check if this is a data type on its own line (follows a column name)
    if (sqlTypes.has(line)) {
      // This is a data type for the last column that doesn't have one yet
      const lastCol = currentTable.columns[currentTable.columns.length - 1];
      if (lastCol && !lastCol.data_type) {
        lastCol.data_type = line;
      }
      continue;
    }

    // Check if this is a max_length on its own line
    if (/^\d+$/.test(line)) {
      const lastCol = currentTable.columns[currentTable.columns.length - 1];
      if (lastCol && lastCol.max_length === 0) {
        lastCol.max_length = parseInt(line);
      }
      continue;
    }

    // Check for very large max_length values (like 2147483647)
    if (/^\d{5,}$/.test(line)) {
      const lastCol = currentTable.columns[currentTable.columns.length - 1];
      if (lastCol && lastCol.max_length === 0) {
        lastCol.max_length = parseInt(line);
      }
      continue;
    }

    // This should be a column name (all-caps identifier)
    if (/^[A-Z][A-Z0-9_]+$/.test(line)) {
      currentTable.columns.push({
        name: line,
        data_type: "",
        max_length: 0,
      });
      continue;
    }
  }
}

// Push the last table
if (currentTable) {
  tables.push(currentTable);
}

// Build the catalog
const catalog = {
  source: "EHI Export All Tables - May 2024 (TheraOffice).pdf",
  extracted: new Date().toISOString().split("T")[0],
  tables: tables.map((t) => ({
    name: t.name,
    documented_column_count: t.total_columns,
    parsed_column_count: t.columns.length,
    columns: t.columns,
  })),
};

// Coverage accounting
const totalDocumented = tables.reduce((s, t) => s + t.total_columns, 0);
const totalParsed = tables.reduce((s, t) => s + t.columns.length, 0);
const missingDataType = tables.flatMap((t) =>
  t.columns.filter((c) => !c.data_type).map((c) => `${t.name}.${c.name}`)
);

const accounting = {
  source_file: "EHI Export All Tables - May 2024 (TheraOffice).pdf",
  tables_expected: knownTables.size,
  tables_parsed: tables.length,
  tables_missing: [...knownTables].filter(
    (n) => !tables.find((t) => t.name === n)
  ),
  total_columns_documented: totalDocumented,
  total_columns_parsed: totalParsed,
  columns_missing_data_type: missingDataType,
  parse_failures: [] as string[],
};

// Verify column counts match
for (const t of tables) {
  if (t.total_columns !== t.columns.length) {
    accounting.parse_failures.push(
      `${t.name}: documented ${t.total_columns} columns but parsed ${t.columns.length}`
    );
  }
}

await Bun.write(
  `${OUT_DIR}/tables-catalog.json`,
  JSON.stringify(catalog, null, 2)
);
await Bun.write(
  `${OUT_DIR}/coverage-accounting.json`,
  JSON.stringify(accounting, null, 2)
);

console.log(`Tables parsed: ${tables.length}/${knownTables.size}`);
console.log(`Columns parsed: ${totalParsed}/${totalDocumented}`);
if (accounting.parse_failures.length > 0) {
  console.log("Parse issues:");
  for (const f of accounting.parse_failures) {
    console.log(`  - ${f}`);
  }
}
if (missingDataType.length > 0) {
  console.log(`Columns missing data_type: ${missingDataType.length}`);
}
console.log("Done. Output: tables-catalog.json, coverage-accounting.json");
