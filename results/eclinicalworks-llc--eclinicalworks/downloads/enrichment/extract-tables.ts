#!/usr/bin/env bun
/**
 * Parses eClinicalWorks EHI Export Schema HTML table pages into queryable JSON.
 * Input: ../tables/*.html (1466 HTML files, each documenting one database table)
 * Output: tables.json (array of table definitions with columns)
 *         summary.json (coverage/accounting stats)
 */

import { readdir, readFile, writeFile } from "fs/promises";
import { join } from "path";

const TABLES_DIR = join(import.meta.dir, "..", "tables");
const OUT_DIR = import.meta.dir;

interface Column {
  name: string;
  dataType: string;
  description: string;
}

interface Table {
  name: string;
  description: string;
  columns: Column[];
  sourceFile: string;
}

interface Summary {
  totalFilesDiscovered: number;
  totalFilesParsed: number;
  totalParseFailures: number;
  parseFailures: Array<{ file: string; error: string }>;
  totalTables: number;
  totalColumns: number;
  avgColumnsPerTable: number;
  tablesWithDescriptions: number;
  columnsWithDescriptions: number;
}

function parseTableHtml(html: string, filename: string): Table {
  // Format 1: class-based (majority of files)
  let nameMatch = html.match(
    /<td class="table-name"><strong>([^<]+)<\/strong><\/td>/
  );
  // Format 2: inline-style based (ip_rh_* files)
  if (!nameMatch) {
    nameMatch = html.match(
      /<th>Table<\/th><td[^>]*>([^<]+)<\/td>/
    );
  }
  const name = nameMatch ? nameMatch[1].trim() : filename.replace(".html", "");

  // Extract table description - format 1
  let descMatch = html.match(
    /<td class="tab-header"><strong>Description<\/strong><\/td>\s*<td class="tab-description">([\s\S]*?)<\/td>/
  );
  // Format 2
  if (!descMatch) {
    descMatch = html.match(
      /<th>Description<\/th><td[^>]*>([\s\S]*?)<\/td>/
    );
  }
  const description = descMatch ? descMatch[1].trim() : "";

  // Extract columns - format 1
  const columns: Column[] = [];
  const colRegex1 =
    /<td class="col-name"><strong>([^<]+)<\/strong><\/td>\s*<td class="tab-description">([^<]*)<\/td>\s*<td class="tab-description">([\s\S]*?)<\/td>/g;
  let match;
  while ((match = colRegex1.exec(html)) !== null) {
    columns.push({
      name: match[1].trim(),
      dataType: match[2].trim(),
      description: match[3].trim().replace(/\s+/g, " "),
    });
  }

  // Format 2: inline-style columns (ip_rh_* files have malformed HTML with extra quotes)
  if (columns.length === 0) {
    const colRegex2 =
      /<td\s+style="[^"]*font-weight: bold[^"]*"[^>]*>([^<]+)<\/td>\s*<td[^>]*>([^<]+)<\/td>\s*<td[^>]*>([\s\S]*?)<\/td>/g;
    while ((match = colRegex2.exec(html)) !== null) {
      columns.push({
        name: match[1].trim(),
        dataType: match[2].trim(),
        description: match[3].trim().replace(/\s+/g, " "),
      });
    }
  }

  return { name, description, columns, sourceFile: `tables/${filename}` };
}

async function main() {
  const files = (await readdir(TABLES_DIR)).filter((f) => f.endsWith(".html"));
  files.sort();

  const tables: Table[] = [];
  const failures: Array<{ file: string; error: string }> = [];

  for (const file of files) {
    try {
      const html = await readFile(join(TABLES_DIR, file), "utf-8");
      const table = parseTableHtml(html, file);
      if (table.columns.length === 0 && !table.description) {
        failures.push({ file, error: "No columns or description extracted" });
      }
      tables.push(table);
    } catch (e: any) {
      failures.push({ file, error: e.message });
    }
  }

  const totalColumns = tables.reduce((s, t) => s + t.columns.length, 0);
  const tablesWithDesc = tables.filter((t) => t.description.length > 0).length;
  const colsWithDesc = tables.reduce(
    (s, t) => s + t.columns.filter((c) => c.description.length > 0).length,
    0
  );

  const summary: Summary = {
    totalFilesDiscovered: files.length,
    totalFilesParsed: tables.length,
    totalParseFailures: failures.length,
    parseFailures: failures,
    totalTables: tables.length,
    totalColumns,
    avgColumnsPerTable: Math.round((totalColumns / tables.length) * 10) / 10,
    tablesWithDescriptions: tablesWithDesc,
    columnsWithDescriptions: colsWithDesc,
  };

  await writeFile(join(OUT_DIR, "tables.json"), JSON.stringify(tables, null, 2));
  await writeFile(
    join(OUT_DIR, "summary.json"),
    JSON.stringify(summary, null, 2)
  );

  console.log(`Parsed ${tables.length} tables, ${totalColumns} columns`);
  console.log(`Parse failures: ${failures.length}`);
  if (failures.length > 0) {
    console.log("Failed files:", failures.map((f) => f.file).join(", "));
  }
}

main();
