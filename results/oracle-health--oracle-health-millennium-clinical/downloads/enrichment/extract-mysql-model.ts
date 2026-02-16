/**
 * Extracts structured JSON from Oracle Health Millennium MySQL Data Model HTML pages.
 * Parses table definitions, columns, data types, and relationships from the
 * HTML data model reports into a queryable JSON format.
 *
 * Usage: bun run extract-mysql-model.ts
 */

import { readdir, readFile, writeFile } from "fs/promises";
import { join } from "path";

const MODEL_DIR = join(import.meta.dir, "..", "mysql-model", "html");
const OUTPUT_FILE = join(import.meta.dir, "mysql-model-tables.json");
const COVERAGE_FILE = join(import.meta.dir, "mysql-model-coverage.json");

interface Column {
  name: string;
  type: string;
  nullable: boolean;
  definition: string;
}

interface Table {
  name: string;
  description: string;
  definition: string;
  table_type: string;
  subject_area: string;
  source_file: string;
  columns: Column[];
}

interface IndexEntry {
  table_name: string;
  target_file: string;
}

function parseIndexPages(html: string): IndexEntry[] {
  const entries: IndexEntry[] = [];
  const re = /<a\s+href="([^"]+)#([^"]+)"\s+target="_blank"\s+title\s*=\s*"Table Report">([^<]+)<\/a>/gi;
  let m: RegExpExecArray | null;
  while ((m = re.exec(html)) !== null) {
    entries.push({ table_name: m[3].trim(), target_file: m[1].trim() });
  }
  return entries;
}

function parseTableReport(html: string): Table[] {
  const tables: Table[] = [];

  // Extract subject area from filename context — will be set by caller
  // Split by table anchors
  const tableSections = html.split(/<h2><a\s+id="([^"]+)">/i);

  for (let i = 1; i < tableSections.length; i += 2) {
    const tableName = tableSections[i].trim();
    const section = tableSections[i + 1] || "";

    // Extract table-level details
    let description = "";
    let definition = "";
    let tableType = "";

    const descMatch = section.match(/<tr>\s*<td>Description:<\/td>\s*<td>\s*([\s\S]*?)\s*<\/td>\s*<\/tr>/i);
    if (descMatch) description = descMatch[1].replace(/<[^>]*>/g, "").trim();

    const defMatch = section.match(/<tr>\s*<td>Definition:<\/td>\s*<td>\s*([\s\S]*?)\s*<\/td>\s*<\/tr>/i);
    if (defMatch) definition = defMatch[1].replace(/<[^>]*>/g, "").trim();

    const typeMatch = section.match(/<tr>\s*<td>Table Type:<\/td>\s*<td>\s*([\s\S]*?)\s*<\/td>\s*<\/tr>/i);
    if (typeMatch) tableType = typeMatch[1].replace(/<[^>]*>/g, "").trim();

    // Extract columns
    const columns: Column[] = [];
    const colSectionMatch = section.match(/Column Detail[\s\S]*?<tbody>([\s\S]*?)<\/tbody>/i);
    if (colSectionMatch) {
      const colRows = colSectionMatch[1].split(/<tr>/i).slice(1);
      for (const row of colRows) {
        const cells = row.split(/<td[^>]*>/i).slice(1).map(c =>
          c.replace(/<\/td>[\s\S]*/i, "").replace(/<[^>]*>/g, "").trim()
        );
        if (cells.length >= 4) {
          columns.push({
            name: cells[0].trim(),
            type: cells[1].trim(),
            nullable: cells[2].trim() === "Y",
            definition: cells[3].trim(),
          });
        }
      }
    }

    tables.push({
      name: tableName,
      description,
      definition,
      table_type: tableType,
      subject_area: "", // set by caller
      source_file: "",  // set by caller
      columns,
    });
  }

  return tables;
}

async function main() {
  console.log("Reading MySQL model HTML files...");

  const files = (await readdir(MODEL_DIR)).filter(f => f.startsWith("dms_") && f.endsWith(".html")).sort();
  console.log(`Found ${files.length} dms_*.html files`);

  const allTables: Table[] = [];
  const failures: { file: string; error: string }[] = [];
  let totalFilesDiscovered = files.length;

  for (const file of files) {
    try {
      const html = await readFile(join(MODEL_DIR, file), "utf-8");
      const subjectArea = file.replace(/^dms_/, "").replace(/\d+\.html$/, "");
      const tables = parseTableReport(html);
      for (const t of tables) {
        t.subject_area = subjectArea;
        t.source_file = `mysql-model/html/${file}`;
      }
      allTables.push(...tables);
    } catch (err: any) {
      failures.push({ file, error: err.message });
    }
  }

  // Also parse index pages for cross-reference
  const indexFiles = (await readdir(MODEL_DIR)).filter(f => f.startsWith("dm_") && f.endsWith(".html") && !f.startsWith("dms_")).sort();

  console.log(`Parsed ${allTables.length} tables from ${files.length} files`);
  console.log(`Parse failures: ${failures.length}`);

  // Compute subject area summary
  const subjectAreas: Record<string, number> = {};
  for (const t of allTables) {
    subjectAreas[t.subject_area] = (subjectAreas[t.subject_area] || 0) + 1;
  }

  await writeFile(OUTPUT_FILE, JSON.stringify(allTables, null, 2));
  console.log(`Wrote ${allTables.length} tables to ${OUTPUT_FILE}`);

  const coverage = {
    total_files_discovered: totalFilesDiscovered,
    total_files_parsed: totalFilesDiscovered - failures.length,
    total_tables_extracted: allTables.length,
    total_columns_extracted: allTables.reduce((s, t) => s + t.columns.length, 0),
    subject_areas: Object.entries(subjectAreas).sort(([, a], [, b]) => b - a).map(([name, count]) => ({ name, table_count: count })),
    parse_failures: failures,
  };

  await writeFile(COVERAGE_FILE, JSON.stringify(coverage, null, 2));
  console.log(`Wrote coverage report to ${COVERAGE_FILE}`);
}

main().catch(console.error);
