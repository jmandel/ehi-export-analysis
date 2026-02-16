#!/usr/bin/env bun
/**
 * Extracts column-level comments from SchemaSpy HTML table pages.
 * These pages may contain additional commentary beyond the XML attributes.
 *
 * Input:  ../tables/*.html  (318 SchemaSpy table HTML pages)
 * Output: html-comments.json  (table → column → comment mappings)
 *         html-coverage.json  (parsing accounting)
 *
 * Run:  cd enrichment && bun run extract-html-comments.ts
 */

import { readFileSync, readdirSync, writeFileSync } from "fs";
import { join } from "path";

const tablesDir = join(import.meta.dir, "..", "tables");
const files = readdirSync(tablesDir).filter((f) => f.endsWith(".html"));

interface ColumnInfo {
  name: string;
  type: string;
  nullable: boolean;
  defaultValue: string;
  comments: string;
}

interface TableInfo {
  name: string;
  remarks: string;
  columns: ColumnInfo[];
  sourceFile: string;
}

const results: TableInfo[] = [];
const failures: { file: string; error: string }[] = [];

for (const file of files) {
  try {
    const html = readFileSync(join(tablesDir, file), "utf-8");
    const tableName = file.replace(".html", "");

    // Extract table description/remarks from the page
    // SchemaSpy puts the table comment in a specific section
    let remarks = "";
    const remarksMatch = html.match(
      /<div[^>]*id="description"[^>]*>([\s\S]*?)<\/div>/i
    );
    if (remarksMatch) {
      remarks = remarksMatch[1].replace(/<[^>]*>/g, "").trim();
    }
    // Alternative: look for the description heading pattern
    if (!remarks) {
      const altMatch = html.match(
        /<h4[^>]*>\s*Description\s*<\/h4>\s*<p[^>]*>([\s\S]*?)<\/p>/i
      );
      if (altMatch) {
        remarks = altMatch[1].replace(/<[^>]*>/g, "").trim();
      }
    }

    // Extract columns from the DataTable
    // SchemaSpy renders columns in a table with class "dataTable" or similar
    const columns: ColumnInfo[] = [];

    // Match table rows within the standard/column section
    // The HTML structure uses <tr> with <td> elements
    const rowRegex =
      /<tr[^>]*>\s*<td[^>]*>([\s\S]*?)<\/td>\s*<td[^>]*>([\s\S]*?)<\/td>\s*<td[^>]*>([\s\S]*?)<\/td>\s*<td[^>]*>([\s\S]*?)<\/td>\s*<td[^>]*>([\s\S]*?)<\/td>\s*<td[^>]*>([\s\S]*?)<\/td>/g;
    let rm: RegExpExecArray | null;
    while ((rm = rowRegex.exec(html)) !== null) {
      const stripTags = (s: string) =>
        s
          .replace(/<[^>]*>/g, "")
          .replace(/&nbsp;/g, " ")
          .replace(/&lt;/g, "<")
          .replace(/&gt;/g, ">")
          .replace(/&amp;/g, "&")
          .trim();

      const colName = stripTags(rm[1]);
      const colType = stripTags(rm[2]);
      const nullable = stripTags(rm[3]);
      const defaultVal = stripTags(rm[4]);
      // rm[5] might be children/parents
      const comments = stripTags(rm[6]);

      // Skip header rows
      if (
        colName === "Column" ||
        colName === "Name" ||
        !colName ||
        colName.startsWith("Showing")
      )
        continue;

      columns.push({
        name: colName,
        type: colType,
        nullable: nullable.toLowerCase() === "true" || nullable === "√",
        defaultValue: defaultVal,
        comments: comments,
      });
    }

    results.push({
      name: tableName,
      remarks,
      columns,
      sourceFile: file,
    });
  } catch (e: any) {
    failures.push({ file, error: e.message });
  }
}

// ---------------------------------------------------------------------------
// Output
// ---------------------------------------------------------------------------

writeFileSync(
  join(import.meta.dir, "html-comments.json"),
  JSON.stringify(results, null, 2)
);

const totalColumns = results.reduce((s, t) => s + t.columns.length, 0);
const tablesWithColumns = results.filter((t) => t.columns.length > 0).length;
const columnsWithComments = results.reduce(
  (s, t) => s + t.columns.filter((c) => c.comments.length > 0).length,
  0
);

const coverage = {
  total_files_discovered: files.length,
  total_files_parsed: results.length,
  tables_with_columns_extracted: tablesWithColumns,
  tables_without_columns: results.length - tablesWithColumns,
  total_columns_extracted: totalColumns,
  columns_with_comments: columnsWithComments,
  parse_failures: failures.length,
  parse_failure_details: failures,
};

writeFileSync(
  join(import.meta.dir, "html-coverage.json"),
  JSON.stringify(coverage, null, 2)
);

console.log("=== HTML Table Page Extraction ===");
console.log(`Files discovered:           ${files.length}`);
console.log(`Files parsed:               ${results.length}`);
console.log(`Tables with columns:        ${tablesWithColumns}`);
console.log(`Total columns extracted:    ${totalColumns}`);
console.log(`Columns with comments:      ${columnsWithComments}`);
console.log(`Parse failures:             ${failures.length}`);
console.log(`\nOutput: html-comments.json, html-coverage.json`);
