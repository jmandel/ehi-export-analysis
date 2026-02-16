#!/usr/bin/env bun
/**
 * extract-tables.ts
 *
 * Parses all Intergy EHI data dictionary HTML pages (viewer/Contracts/*.htm)
 * and extracts structured JSON with table definitions, fields, and relationships.
 *
 * Usage: bun run extract-tables.ts
 *
 * Input:  ../viewer/Contracts/*.htm  (261 table HTML files)
 *         ../viewer/Contracts/include/DBDescriptions.js (table descriptions)
 * Output: ./tables.json             (full structured data dictionary)
 *         ./tables-summary.json     (compact summary with table/field counts)
 *         ./coverage-report.json    (accounting of parse results)
 */

import { readdir, readFile, writeFile } from "fs/promises";
import { join, basename } from "path";

const CONTRACTS_DIR = join(import.meta.dir, "..", "viewer", "Contracts");
const OUTPUT_DIR = import.meta.dir;

interface Field {
  name: string;
  datatype: string;
  default_value: string | null;
  null_option: string; // MANDATORY | OPTIONAL
  comment: string;
}

interface Relationship {
  table: string;
  join_phrase: string;
  on_delete: string;
}

interface TableDef {
  name: string;
  description: string;
  last_updated: string | null;
  intergy_version: string | null;
  fields: Field[];
  parent_tables: Relationship[];
  child_tables: Relationship[];
}

interface ParseResult {
  success: boolean;
  table?: TableDef;
  error?: string;
  file: string;
}

function extractText(html: string): string {
  return html
    .replace(/<br\s*\/?>/gi, " ")
    .replace(/<[^>]*>/g, " ")
    .replace(/&nbsp;/g, " ")
    .replace(/&amp;/g, "&")
    .replace(/&lt;/g, "<")
    .replace(/&gt;/g, ">")
    .replace(/&quot;/g, '"')
    .replace(/&#39;/g, "'")
    .replace(/\s+/g, " ")
    .trim();
}

function parseTablePage(html: string, filename: string): TableDef {
  const tableName = basename(filename, ".htm");

  // Extract metadata
  const lastUpdatedMatch = html.match(/Last Updated:\s*([^<]+)/);
  const versionMatch = html.match(/Intergy Version:\s*([^<]+)/);
  const descMatch = html.match(/<h3>\s*Description:\s*(.*?)<\/h3>/is);

  const lastUpdated = lastUpdatedMatch ? lastUpdatedMatch[1].trim() : null;
  const intergyVersion = versionMatch ? versionMatch[1].trim() : null;
  const description = descMatch ? extractText(descMatch[1]) : "";

  // Extract fields from table definition
  const fields: Field[] = [];

  // Find the main table definition section (first table after "Table Definition")
  const tableDefSection = html.split(/<a name="parentrel">/i)[0] || html;

  // Match rows in the table definition
  const rowRegex =
    /<tr>\s*<td[^>]*>([^<]*)<\/td>\s*<td[^>]*>([^<]*)<\/td>\s*<td[^>]*>([\s\S]*?)<\/td>\s*<td[^>]*>([^<]*)<\/td>\s*<td[^>]*>([\s\S]*?)<\/td>\s*<\/tr>/gi;
  let match: RegExpExecArray | null;
  while ((match = rowRegex.exec(tableDefSection)) !== null) {
    const fieldName = extractText(match[1]);
    const datatype = extractText(match[2]);
    const rawDefault = extractText(match[3]);
    const nullOption = extractText(match[4]);
    const comment = extractText(match[5]);

    if (fieldName && fieldName !== "Field") {
      // Skip header row
      fields.push({
        name: fieldName,
        datatype: datatype,
        default_value:
          rawDefault === "?" || rawDefault === "" ? null : rawDefault,
        null_option: nullOption,
        comment: comment,
      });
    }
  }

  // Extract parent tables
  const parentTables: Relationship[] = [];
  const parentSection = html.match(
    /<a name="parentrel"><\/a>[\s\S]*?<table[^>]*>([\s\S]*?)<\/table>/i
  );
  if (parentSection) {
    const relRowRegex =
      /<tr>\s*<td>\s*<a[^>]*>([^<]*)<\/a>\s*<\/td>\s*<td>([\s\S]*?)<\/td>\s*<td>([\s\S]*?)<\/td>\s*<\/tr>/gi;
    while ((match = relRowRegex.exec(parentSection[1])) !== null) {
      parentTables.push({
        table: extractText(match[1]),
        join_phrase: extractText(match[2]),
        on_delete: extractText(match[3]),
      });
    }
  }

  // Extract child tables
  const childTables: Relationship[] = [];
  const childSection = html.match(
    /<a name="childrel"><\/a>[\s\S]*?<table[^>]*>([\s\S]*?)<\/table>/i
  );
  if (childSection) {
    const relRowRegex =
      /<tr>\s*<td>\s*<a[^>]*>([^<]*)<\/a>\s*<\/td>\s*<td>([\s\S]*?)<\/td>\s*<td>([\s\S]*?)<\/td>\s*<\/tr>/gi;
    while ((match = relRowRegex.exec(childSection[1])) !== null) {
      childTables.push({
        table: extractText(match[1]),
        join_phrase: extractText(match[2]),
        on_delete: extractText(match[3]),
      });
    }
  }

  return {
    name: tableName,
    description,
    last_updated: lastUpdated,
    intergy_version: intergyVersion,
    fields,
    parent_tables: parentTables,
    child_tables: childTables,
  };
}

// Also parse descriptions from DBDescriptions.js
async function loadDescriptions(): Promise<Map<string, string>> {
  const descMap = new Map<string, string>();
  try {
    const jsContent = await readFile(
      join(CONTRACTS_DIR, "include", "DBDescriptions.js"),
      "utf-8"
    );
    const descRegex = /new Table\('([^']+)'\s*,\s*"([^"]*)"\)/g;
    let m: RegExpExecArray | null;
    while ((m = descRegex.exec(jsContent)) !== null) {
      descMap.set(m[1], m[2]);
    }
  } catch {
    console.warn("Could not load DBDescriptions.js");
  }
  return descMap;
}

async function main() {
  const files = (await readdir(CONTRACTS_DIR)).filter(
    (f) =>
      f.endsWith(".htm") && f !== "DBTOC.htm" && !f.startsWith("include")
  );

  console.log(`Found ${files.length} table files to parse`);

  const descriptions = await loadDescriptions();
  const results: ParseResult[] = [];
  const tables: TableDef[] = [];

  for (const file of files.sort()) {
    try {
      const html = await readFile(join(CONTRACTS_DIR, file), "utf-8");
      const table = parseTablePage(html, file);

      // Supplement description from DBDescriptions.js if empty
      if (!table.description && descriptions.has(table.name)) {
        table.description = descriptions.get(table.name)!;
      }

      tables.push(table);
      results.push({ success: true, table, file });
    } catch (err: any) {
      results.push({ success: false, error: err.message, file });
    }
  }

  // Write full data dictionary
  await writeFile(
    join(OUTPUT_DIR, "tables.json"),
    JSON.stringify(tables, null, 2)
  );

  // Write compact summary
  const summary = tables.map((t) => ({
    name: t.name,
    description: t.description,
    field_count: t.fields.length,
    parent_count: t.parent_tables.length,
    child_count: t.child_tables.length,
    fields: t.fields.map((f) => f.name),
  }));
  await writeFile(
    join(OUTPUT_DIR, "tables-summary.json"),
    JSON.stringify(summary, null, 2)
  );

  // Write coverage report
  const successful = results.filter((r) => r.success);
  const failed = results.filter((r) => !r.success);
  const zeroFields = successful.filter(
    (r) => r.table && r.table.fields.length === 0
  );

  const coverageReport = {
    total_files_discovered: files.length,
    total_files_parsed: successful.length,
    parse_failures: failed.map((r) => ({
      file: r.file,
      error: r.error,
    })),
    zero_field_tables: zeroFields.map((r) => r.file),
    total_tables: tables.length,
    total_fields: tables.reduce((sum, t) => sum + t.fields.length, 0),
    total_relationships: tables.reduce(
      (sum, t) => sum + t.parent_tables.length + t.child_tables.length,
      0
    ),
    field_count_distribution: {
      "0_fields": tables.filter((t) => t.fields.length === 0).length,
      "1-10_fields": tables.filter(
        (t) => t.fields.length >= 1 && t.fields.length <= 10
      ).length,
      "11-30_fields": tables.filter(
        (t) => t.fields.length >= 11 && t.fields.length <= 30
      ).length,
      "31-50_fields": tables.filter(
        (t) => t.fields.length >= 31 && t.fields.length <= 50
      ).length,
      "51+_fields": tables.filter((t) => t.fields.length > 50).length,
    },
  };
  await writeFile(
    join(OUTPUT_DIR, "coverage-report.json"),
    JSON.stringify(coverageReport, null, 2)
  );

  console.log(`\nResults:`);
  console.log(`  Parsed: ${successful.length}/${files.length} files`);
  console.log(`  Failed: ${failed.length}`);
  console.log(
    `  Total fields: ${tables.reduce((s, t) => s + t.fields.length, 0)}`
  );
  console.log(
    `  Total relationships: ${tables.reduce((s, t) => s + t.parent_tables.length + t.child_tables.length, 0)}`
  );
  if (zeroFields.length > 0) {
    console.log(
      `  Tables with 0 fields: ${zeroFields.length} (${zeroFields.map((r) => r.file).join(", ")})`
    );
  }
  if (failed.length > 0) {
    console.log(`  Failures:`);
    failed.forEach((r) => console.log(`    ${r.file}: ${r.error}`));
  }
}

main().catch(console.error);
