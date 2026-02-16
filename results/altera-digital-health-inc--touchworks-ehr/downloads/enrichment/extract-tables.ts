#!/usr/bin/env bun
/**
 * Extracts structured table/column metadata from Altera TouchWorks EHI Export
 * Definition HTML files into queryable JSON.
 *
 * Input: ../twehr-2026.1/Touchworks/User_databases/.../*.html
 * Output: tables.json, coverage.json
 */

import { readdir, readFile, writeFile, stat } from "fs/promises";
import { join, relative, basename, dirname } from "path";

const INPUT_DIR = join(import.meta.dir, "..", "twehr-2026.1");
const OUTPUT_DIR = import.meta.dir;

interface Column {
  name: string;
  dataType: string;
  maxLengthBytes: string;
  nullability: string;
  default: string;
  description: string;
  isPrimaryKey: boolean;
  hasForeignKey: boolean;
  foreignKeyTarget: string | null;
  indexCount: number;
}

interface Table {
  database: string;
  schema: string;
  tableName: string;
  fullName: string;
  description: string;
  columns: Column[];
  foreignKeys: ForeignKey[];
  indexes: Index[];
  sourceFile: string;
}

interface ForeignKey {
  name: string;
  columns: string;
  referencedTable: string;
}

interface Index {
  name: string;
  columns: string;
  type: string;
}

interface Coverage {
  totalFilesDiscovered: number;
  totalTableFiles: number;
  totalTablesParsed: number;
  parseFailures: { file: string; error: string }[];
  databases: { name: string; tableCount: number }[];
  totalColumns: number;
  columnsWithDescriptions: number;
  columnsWithForeignKeys: number;
}

async function findHtmlFiles(dir: string): Promise<string[]> {
  const results: string[] = [];
  const entries = await readdir(dir, { withFileTypes: true });
  for (const entry of entries) {
    const fullPath = join(dir, entry.name);
    if (entry.isDirectory()) {
      results.push(...(await findHtmlFiles(fullPath)));
    } else if (entry.name.endsWith(".html")) {
      results.push(fullPath);
    }
  }
  return results;
}

function extractText(html: string, start: number, end: number): string {
  return html.slice(start, end).replace(/<[^>]*>/g, "").trim();
}

function parseTableHtml(html: string, filePath: string): Table | null {
  // Extract table name from title
  const titleMatch = html.match(/<title>([^<]+)<\/title>/);
  if (!titleMatch) return null;
  const fullName = titleMatch[1];

  // Parse schema.table from fullName (e.g., "dbo.Allergy")
  const parts = fullName.split(".");
  const schema = parts.length > 1 ? parts[0] : "dbo";
  const tableName = parts.length > 1 ? parts.slice(1).join(".") : parts[0];

  // Extract database from path
  const relPath = relative(INPUT_DIR, filePath);
  const pathParts = relPath.split("/");
  // Pattern: Touchworks/User_databases/{database}/Tables/{file}.html
  const dbIdx = pathParts.indexOf("User_databases");
  const database = dbIdx >= 0 && dbIdx + 1 < pathParts.length ? pathParts[dbIdx + 1] : "unknown";

  // Extract MS_Description
  const descMatch = html.match(/<a name="description">MS_Description<\/a>[\s\S]*?<div class="panel-body">([\s\S]*?)<\/div>/);
  const description = descMatch ? descMatch[1].replace(/<[^>]*>/g, "").trim() : "";

  // Extract columns from the columns table
  const columns: Column[] = [];
  const columnsSection = html.match(/<a name="columns">Columns<\/a>[\s\S]*?<table[\s\S]*?<\/table>/);
  if (columnsSection) {
    const rows = columnsSection[0].match(/<tr>[\s\S]*?<\/tr>/g);
    if (rows) {
      // Skip header row
      for (let i = 1; i < rows.length; i++) {
        const cells = rows[i].match(/<td>[\s\S]*?<\/td>/g);
        if (!cells) continue;

        const keyCell = cells[0] || "";
        const isPrimaryKey = keyCell.includes("pkcluster") || keyCell.includes("pknocluster");
        const hasForeignKey = keyCell.includes("fk.png");
        const indexImgs = keyCell.match(/class="Index"/g);
        const indexCount = indexImgs ? indexImgs.length : 0;

        // Extract FK target
        let foreignKeyTarget: string | null = null;
        const fkMatch = keyCell.match(/Foreign Keys [^:]+: ([^"]+)/);
        if (fkMatch) foreignKeyTarget = fkMatch[1];

        // Determine column count based on header
        const hasDefault = html.includes("<th>Default</th>");
        let nameIdx = 1, typeIdx = 2, lengthIdx = 3, nullIdx = 4, defaultIdx = -1, descIdx = 5;
        if (hasDefault) {
          defaultIdx = 5;
          descIdx = 6;
        }

        const getName = (idx: number) => cells[idx] ? cells[idx].replace(/<[^>]*>/g, "").trim() : "";

        columns.push({
          name: getName(nameIdx),
          dataType: getName(typeIdx),
          maxLengthBytes: getName(lengthIdx),
          nullability: getName(nullIdx),
          default: defaultIdx >= 0 && cells[defaultIdx] ? getName(defaultIdx) : "",
          description: cells[descIdx] ? getName(descIdx) : "",
          isPrimaryKey,
          hasForeignKey,
          foreignKeyTarget,
          indexCount,
        });
      }
    }
  }

  // Extract foreign keys
  const foreignKeys: ForeignKey[] = [];
  const fkSection = html.match(/<a name="foreignkeys">Foreign Keys<\/a>[\s\S]*?<table[\s\S]*?<\/table>/);
  if (fkSection) {
    const rows = fkSection[0].match(/<tr>[\s\S]*?<\/tr>/g);
    if (rows) {
      for (let i = 1; i < rows.length; i++) {
        const cells = rows[i].match(/<td>[\s\S]*?<\/td>/g);
        if (!cells || cells.length < 3) continue;
        const getName = (idx: number) => cells[idx] ? cells[idx].replace(/<[^>]*>/g, "").trim() : "";
        foreignKeys.push({
          name: getName(0),
          columns: getName(1),
          referencedTable: getName(2),
        });
      }
    }
  }

  // Extract indexes
  const indexes: Index[] = [];
  const idxSection = html.match(/<a name="indexes">Indexes<\/a>[\s\S]*?<table[\s\S]*?<\/table>/);
  if (idxSection) {
    const rows = idxSection[0].match(/<tr>[\s\S]*?<\/tr>/g);
    if (rows) {
      for (let i = 1; i < rows.length; i++) {
        const cells = rows[i].match(/<td>[\s\S]*?<\/td>/g);
        if (!cells || cells.length < 2) continue;
        const getName = (idx: number) => cells[idx] ? cells[idx].replace(/<[^>]*>/g, "").trim() : "";
        indexes.push({
          name: getName(0),
          columns: getName(1),
          type: cells.length > 2 ? getName(2) : "",
        });
      }
    }
  }

  return {
    database,
    schema,
    tableName,
    fullName,
    description,
    columns,
    foreignKeys,
    indexes,
    sourceFile: relative(INPUT_DIR, filePath),
  };
}

async function main() {
  console.log("Finding HTML files...");
  const allFiles = await findHtmlFiles(INPUT_DIR);
  console.log(`Total HTML files discovered: ${allFiles.length}`);

  // Filter to table-level files (inside Tables/ directories, excluding Tables.html and index.html)
  const tableFiles = allFiles.filter(
    (f) =>
      f.includes("/Tables/") &&
      !basename(f).match(/^(Tables|index)\.html$/)
  );
  console.log(`Table HTML files: ${tableFiles.length}`);

  const tables: Table[] = [];
  const failures: { file: string; error: string }[] = [];

  for (const file of tableFiles) {
    try {
      const html = await readFile(file, "utf-8");
      const table = parseTableHtml(html, file);
      if (table) {
        tables.push(table);
      } else {
        failures.push({ file: relative(INPUT_DIR, file), error: "Could not parse table structure" });
      }
    } catch (e: any) {
      failures.push({ file: relative(INPUT_DIR, file), error: e.message });
    }
  }

  console.log(`Tables parsed: ${tables.length}`);
  console.log(`Parse failures: ${failures.length}`);

  // Build coverage stats
  const dbCounts = new Map<string, number>();
  let totalColumns = 0;
  let columnsWithDescriptions = 0;
  let columnsWithForeignKeys = 0;

  for (const t of tables) {
    dbCounts.set(t.database, (dbCounts.get(t.database) || 0) + 1);
    totalColumns += t.columns.length;
    columnsWithDescriptions += t.columns.filter((c) => c.description.length > 0).length;
    columnsWithForeignKeys += t.columns.filter((c) => c.hasForeignKey).length;
  }

  const coverage: Coverage = {
    totalFilesDiscovered: allFiles.length,
    totalTableFiles: tableFiles.length,
    totalTablesParsed: tables.length,
    parseFailures: failures,
    databases: Array.from(dbCounts.entries())
      .map(([name, tableCount]) => ({ name, tableCount }))
      .sort((a, b) => b.tableCount - a.tableCount),
    totalColumns,
    columnsWithDescriptions,
    columnsWithForeignKeys,
  };

  // Write outputs
  await writeFile(join(OUTPUT_DIR, "tables.json"), JSON.stringify(tables, null, 2));
  await writeFile(join(OUTPUT_DIR, "coverage.json"), JSON.stringify(coverage, null, 2));

  console.log("\nCoverage Summary:");
  console.log(`  Databases: ${coverage.databases.length}`);
  for (const db of coverage.databases) {
    console.log(`    ${db.name}: ${db.tableCount} tables`);
  }
  console.log(`  Total columns: ${totalColumns}`);
  console.log(`  Columns with descriptions: ${columnsWithDescriptions} (${((columnsWithDescriptions / totalColumns) * 100).toFixed(1)}%)`);
  console.log(`  Columns with foreign keys: ${columnsWithForeignKeys}`);
  if (failures.length > 0) {
    console.log(`  Parse failures:`);
    for (const f of failures) {
      console.log(`    ${f.file}: ${f.error}`);
    }
  }

  console.log("\nDone. Output: tables.json, coverage.json");
}

main();
