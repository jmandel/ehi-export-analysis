#!/usr/bin/env bun
/**
 * Extracts structured JSON from Epic EHI Tables HTML documentation.
 * Parses all .htm files in the extracted ZIP using cheerio (lightweight),
 * producing a queryable JSON corpus of tables, columns, primary keys,
 * and descriptions.
 */

import { readdirSync, readFileSync, writeFileSync, createWriteStream } from "fs";
import { join, basename } from "path";
import * as cheerio from "cheerio";

const INPUT_DIR = join(
  __dirname,
  "..",
  "ehi-tables-extracted",
  "DocGen_su117s2p_2026-02-15_14.10.04"
);
const OUTPUT_FILE = join(__dirname, "ehi-tables.json");
const COVERAGE_FILE = join(__dirname, "extraction-coverage.json");

interface Column {
  ordinal: number;
  name: string;
  type: string;
  discontinued: boolean;
  description: string;
}

interface PrimaryKeyColumn {
  name: string;
  ordinal_position: number;
}

interface TableDef {
  table_name: string;
  source_file: string;
  description: string;
  primary_key: PrimaryKeyColumn[];
  columns: Column[];
}

function parseTableFile(filePath: string): TableDef | null {
  const html = readFileSync(filePath, "utf-8");
  const $ = cheerio.load(html);

  // Table name from Header2
  const tableName = $("table.Header2 td").first().text().trim() || basename(filePath, ".htm");

  // Description
  const description = $("table.KeyValue .T1Value").first().text().trim();

  // Primary Key - find the List table (not SubList) after "Primary Key" header
  const primaryKey: PrimaryKeyColumn[] = [];
  const subHeaders = $("table.SubHeader3 td");
  let foundPK = false;
  subHeaders.each((_, el) => {
    if ($(el).text().trim() === "Primary Key") foundPK = true;
  });

  if (foundPK) {
    // The PK table is table.List without .SubList class
    const pkTable = $("table.List").not(".SubList").first();
    pkTable.find("tr").each((_, row) => {
      const cells = $(row).find("td");
      if (cells.length >= 2) {
        const name = $(cells[0]).text().trim();
        const pos = parseInt($(cells[1]).text().trim(), 10);
        if (name && !isNaN(pos)) {
          primaryKey.push({ name, ordinal_position: pos });
        }
      }
    });
  }

  // Parse columns from table.SubList.List with "Name" header
  const columns: Column[] = [];
  let colTable: cheerio.Cheerio<cheerio.Element> | null = null;

  $("table.SubList.List").each((_, t) => {
    const $t = $(t);
    if ($t.find("th").toArray().some((th) => $(th).text().trim() === "Name")) {
      colTable = $t;
    }
  });

  if (colTable) {
    const rows = (colTable as cheerio.Cheerio<cheerio.Element>).children("tbody").children("tr");
    let currentColumn: Partial<Column> | null = null;

    rows.each((_, row) => {
      const $row = $(row);
      const headCells = $row.find("> td.T1Head");

      if (headCells.length >= 2) {
        if (currentColumn && currentColumn.name) {
          columns.push(currentColumn as Column);
        }
        currentColumn = {
          ordinal: parseInt($(headCells[0]).text().trim(), 10) || 0,
          name: $(headCells[1]).text().trim(),
          type: headCells.length >= 3 ? $(headCells[2]).text().trim() : "",
          discontinued: false,
          description: "",
        };
        // Check discontinued in non-T1Head cells
        $row.find("> td").not(".T1Head").each((_, cell) => {
          const text = $(cell).text().trim();
          if (text === "Yes") currentColumn!.discontinued = true;
          else if (text === "No") currentColumn!.discontinued = false;
        });
      } else if (currentColumn) {
        // Description row
        const descText = $row.find("table.SubList td").text().trim();
        if (descText) {
          currentColumn.description = currentColumn.description
            ? currentColumn.description + " " + descText
            : descText;
        }
      }
    });

    if (currentColumn && (currentColumn as Partial<Column>).name) {
      columns.push(currentColumn as Column);
    }
  }

  return {
    table_name: tableName,
    source_file: basename(filePath),
    description,
    primary_key: primaryKey,
    columns,
  };
}

// Main
const files = readdirSync(INPUT_DIR).filter(
  (f) => f.endsWith(".htm") && !f.startsWith("_")
);
const results: TableDef[] = [];
const failures: { file: string; error: string }[] = [];

console.log(`Found ${files.length} .htm files to parse`);

let processed = 0;
for (const file of files) {
  try {
    const result = parseTableFile(join(INPUT_DIR, file));
    if (result) {
      results.push(result);
    }
  } catch (e: any) {
    failures.push({ file, error: e.message });
  }
  processed++;
  if (processed % 500 === 0) {
    console.log(`  Processed ${processed}/${files.length}...`);
  }
}

// Sort by table name
results.sort((a, b) => a.table_name.localeCompare(b.table_name));

writeFileSync(OUTPUT_FILE, JSON.stringify(results, null, 2));

const totalColumns = results.reduce((s, t) => s + t.columns.length, 0);
const coverage = {
  total_files_discovered: files.length + 1, // +1 for _index.htm
  total_table_files: files.length,
  total_files_parsed: results.length,
  parse_failures: failures.length,
  failure_details: failures,
  total_tables: results.length,
  total_columns: totalColumns,
  tables_with_descriptions: results.filter((t) => t.description.length > 0).length,
  columns_with_descriptions: results.reduce(
    (s, t) => s + t.columns.filter((c) => c.description.length > 0).length,
    0
  ),
  tables_with_primary_keys: results.filter((t) => t.primary_key.length > 0).length,
  column_types: Object.fromEntries(
    [...new Map(
      results
        .flatMap((t) => t.columns)
        .reduce((m, c) => {
          m.set(c.type, (m.get(c.type) ?? 0) + 1);
          return m;
        }, new Map<string, number>())
    )].sort((a, b) => b[1] - a[1])
  ),
};

writeFileSync(COVERAGE_FILE, JSON.stringify(coverage, null, 2));

console.log(`\nParsed ${results.length} tables with ${totalColumns} columns`);
console.log(`Failures: ${failures.length}`);
if (failures.length > 0) {
  console.log("Failed files:", failures.slice(0, 10).map((f) => f.file).join(", "));
}
console.log(`Output: ${OUTPUT_FILE}`);
console.log(`Coverage: ${COVERAGE_FILE}`);
