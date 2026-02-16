/**
 * Extracts table definitions from the PrimeSuite EHI Export Data Dictionary HTML
 * into structured JSON.
 *
 * Input:  ../PrimeSuiteEHIExport_Data_Dictionary.html
 * Output: data-dictionary.json
 *         extraction-stats.json
 *
 * Run: bun run extract-data-dictionary.ts
 */

import { readFileSync, writeFileSync } from "fs";
import { join, dirname } from "path";

const scriptDir = dirname(new URL(import.meta.url).pathname);
const inputPath = join(scriptDir, "..", "PrimeSuiteEHIExport_Data_Dictionary.html");
const outputPath = join(scriptDir, "data-dictionary.json");
const statsPath = join(scriptDir, "extraction-stats.json");

interface Column {
  name: string;
  dataType: string;
  nullable: boolean;
  description: string;
}

interface Table {
  name: string;
  description: string;
  columns: Column[];
}

const html = readFileSync(inputPath, "utf-8");

// The data dictionary HTML structure:
// <h3 id= TableName>TableName</h3><p>Description</p><table>..rows..</table>
// Each table row: <tr><td>ColumnName</td><td>DataType</td><td>Nullable</td><td>Description</td></tr>

const tables: Table[] = [];
const failures: { context: string; error: string }[] = [];

// Split on h3 tags that represent table definitions (not alphabetical navigation)
const tablePattern = /<h3 id=\s*(?!list-starts-with)(\w+)>([^<]+)<\/h3>/g;
let match: RegExpExecArray | null;
const positions: { name: string; heading: string; index: number }[] = [];

while ((match = tablePattern.exec(html)) !== null) {
  positions.push({
    name: match[1].trim(),
    heading: match[2].trim(),
    index: match.index,
  });
}

for (let i = 0; i < positions.length; i++) {
  const pos = positions[i];
  const nextIndex = i + 1 < positions.length ? positions[i + 1].index : html.length;
  const section = html.slice(pos.index, nextIndex);

  try {
    // Extract description: text in <p> tag(s) between h3 and first <table>
    const tableStart = section.indexOf("<table");
    let description = "";
    if (tableStart > 0) {
      const beforeTable = section.slice(0, tableStart);
      const pMatches = beforeTable.match(/<p[^>]*>([\s\S]*?)<\/p>/gi);
      if (pMatches) {
        description = pMatches
          .map((p) => p.replace(/<[^>]*>/g, "").trim())
          .filter(Boolean)
          .join(" ");
      }
    }

    // Extract columns from <table>
    const columns: Column[] = [];
    const tableMatch = section.match(/<table[\s\S]*?<\/table>/i);
    if (tableMatch) {
      const rows = tableMatch[0].match(/<tr[\s\S]*?<\/tr>/gi);
      if (rows) {
        // Skip header row
        for (let r = 1; r < rows.length; r++) {
          const cells = rows[r].match(/<td[^>]*>([\s\S]*?)<\/td>/gi);
          if (cells && cells.length >= 4) {
            const cellTexts = cells.map((c) =>
              c.replace(/<[^>]*>/g, "").trim()
            );
            columns.push({
              name: cellTexts[0],
              dataType: cellTexts[1],
              nullable: cellTexts[2].toUpperCase() === "YES",
              description: cellTexts[3],
            });
          }
        }
      }
    }

    tables.push({
      name: pos.name,
      description,
      columns,
    });
  } catch (err: any) {
    failures.push({
      context: pos.name,
      error: err.message || String(err),
    });
  }
}

writeFileSync(outputPath, JSON.stringify(tables, null, 2));

const stats = {
  input_file: "PrimeSuiteEHIExport_Data_Dictionary.html",
  total_tables_discovered: positions.length,
  total_tables_parsed: tables.length,
  total_columns_extracted: tables.reduce((sum, t) => sum + t.columns.length, 0),
  tables_with_no_columns: tables.filter((t) => t.columns.length === 0).length,
  tables_with_no_description: tables.filter((t) => !t.description).length,
  parse_failures: failures.length,
  failure_details: failures,
};

writeFileSync(statsPath, JSON.stringify(stats, null, 2));

console.log(`Extracted ${tables.length} tables with ${stats.total_columns_extracted} total columns`);
console.log(`Tables with no columns: ${stats.tables_with_no_columns}`);
console.log(`Tables with no description: ${stats.tables_with_no_description}`);
console.log(`Parse failures: ${failures.length}`);
console.log(`Output: ${outputPath}`);
console.log(`Stats: ${statsPath}`);
