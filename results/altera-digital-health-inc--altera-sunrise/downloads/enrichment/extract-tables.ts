/**
 * Extracts table/column definitions from Sunrise EHI WebERDiagram HTML files
 * into queryable JSON. Targets the PR38 (latest) export documentation.
 *
 * Usage: bun run extract-tables.ts
 */

import { readdir, readFile, writeFile, stat } from "fs/promises";
import { join, relative, basename } from "path";

const BASE_DIR = join(import.meta.dir, "..", "extracted", "pr38-weberdiagram", "EHI WebERDiagram 22.1 PR38");
const OUTPUT_DIR = import.meta.dir;

interface Column {
  name: string;
  domain: string;
  datatype: string;
  nullable: boolean;
  isPrimaryKey: boolean;
  definition: string;
}

interface KeyInfo {
  name: string;
  type: string;
  columns: string;
}

interface Table {
  schema: string; // FS, IMG, MNC, SCM
  qualifiedName: string; // dbo.TableName
  tableName: string;
  definition: string;
  columns: Column[];
  keys: KeyInfo[];
  sourceFile: string;
}

interface ParseResult {
  table: Table | null;
  error: string | null;
}

function cleanText(s: string): string {
  return s
    .replace(/&nbsp;/g, " ")
    .replace(/&amp;/g, "&")
    .replace(/&lt;/g, "<")
    .replace(/&gt;/g, ">")
    .replace(/&quot;/g, '"')
    .replace(/&#\d+;/g, "")
    .replace(/<[^>]*>/g, "")
    .trim();
}

function parseTableHtml(rawHtml: string, schema: string, filePath: string): ParseResult {
  const html = rawHtml.replace(/\r\n/g, "\n").replace(/\r/g, "\n");
  try {
    // Extract table name from TITLE
    const titleMatch = html.match(/<TITLE>([^<]+)<\/TITLE>/i);
    if (!titleMatch) return { table: null, error: "No TITLE tag found" };
    const tableName = titleMatch[1].trim();

    // Extract qualified name (dbo.xxx) from first header
    const qualNameMatch = html.match(/dbo\.(\w+)/);
    const qualifiedName = qualNameMatch ? `dbo.${qualNameMatch[1]}` : `dbo.${tableName}`;

    // Extract definition
    const defMatch = html.match(
      /Definition[^<]*<\/FONT><\/B><\/TD>\s*<TD><FONT[^>]*>([^<]*(?:<[^>]*>[^<]*)*?)<\/FONT><\/TD>/i
    );
    const definition = defMatch ? cleanText(defMatch[1]) : "";

    // Extract columns from the columns table
    // Pattern: rows with 5 cells (ColumnName, Domain, Datatype, NULL, Definition)
    const columns: Column[] = [];
    const pkColumns = new Set<string>();

    // First, find PK columns by looking for pk.gif
    const pkMatches = html.matchAll(/<A HREF[^>]*>([^<]+)<\/A><img src="[^"]*pk\.gif"/gi);
    for (const m of pkMatches) {
      pkColumns.add(cleanText(m[1]));
    }

    // Parse column rows - match rows with 5 TD cells after the header row
    const columnSectionMatch = html.match(
      /ColumnName[\s\S]*?Definition[\s\S]*?<\/TR>([\s\S]*?)(?:<\/TABLE>)/i
    );

    if (columnSectionMatch) {
      const rowRegex = /<TR>\s*<TD[^>]*>\s*<FONT[^>]*>(?:<A[^>]*>)?([^<]+)(?:<\/A>)?(?:<img[^>]*>)?[^<]*<\/FONT><\/TD>\s*<TD[^>]*>\s*<FONT[^>]*>([^<]*)<\/FONT><\/TD>\s*<TD[^>]*>\s*<FONT[^>]*>([^<]*)<\/FONT><\/TD>\s*<TD[^>]*>\s*<FONT[^>]*>([^<]*)<\/FONT><\/TD>\s*<TD[^>]*>\s*<FONT[^>]*>([\s\S]*?)<\/FONT><\/TD>/gi;

      let match;
      while ((match = rowRegex.exec(columnSectionMatch[1])) !== null) {
        const colName = cleanText(match[1]);
        columns.push({
          name: colName,
          domain: cleanText(match[2]),
          datatype: cleanText(match[3]),
          nullable: cleanText(match[4]).toUpperCase() === "YES",
          isPrimaryKey: pkColumns.has(colName),
          definition: cleanText(match[5]),
        });
      }
    }

    // Extract keys
    const keys: KeyInfo[] = [];
    const keySectionMatch = html.match(
      /Key Name.*?Keys.*?<\/TR>([\s\S]*?)(?:<\/TABLE>)/i
    );
    if (keySectionMatch) {
      const keyRowRegex =
        /<TR>\s*<TD[^>]*>\s*<FONT[^>]*>([^<]*)<\/FONT><\/TD>\s*<TD[^>]*>\s*<FONT[^>]*>([^<]*)<\/FONT><\/TD>\s*<TD[^>]*>\s*<FONT[^>]*>([^<]*)<\/FONT><\/TD>/gi;
      let km;
      while ((km = keyRowRegex.exec(keySectionMatch[1])) !== null) {
        keys.push({
          name: cleanText(km[1]),
          type: cleanText(km[2]),
          columns: cleanText(km[3]),
        });
      }
    }

    return {
      table: {
        schema,
        qualifiedName,
        tableName,
        definition,
        columns,
        keys,
        sourceFile: filePath,
      },
      error: null,
    };
  } catch (e: any) {
    return { table: null, error: e.message };
  }
}

async function findTableFiles(dir: string): Promise<string[]> {
  const files: string[] = [];
  const entries = await readdir(dir, { recursive: true });
  for (const entry of entries) {
    const full = join(dir, entry);
    if (basename(full).startsWith("Tbl_") && !basename(full).includes("_Attr") && full.endsWith(".htm")) {
      files.push(full);
    }
  }
  return files;
}

async function main() {
  const schemas = ["FS", "IMG", "MNC", "SCM"];
  const allTables: Table[] = [];
  const failures: { file: string; error: string }[] = [];
  let totalDiscovered = 0;
  let totalParsed = 0;

  for (const schema of schemas) {
    const contentDir = join(BASE_DIR, `${schema} WebERDiagram 22.1 PR38`, "Content");
    try {
      await stat(contentDir);
    } catch {
      console.log(`Skipping ${schema}: directory not found`);
      continue;
    }

    const tableFiles = await findTableFiles(contentDir);
    totalDiscovered += tableFiles.length;
    console.log(`${schema}: found ${tableFiles.length} table files`);

    for (const file of tableFiles) {
      const html = await readFile(file, "utf-8");
      const relPath = relative(join(import.meta.dir, ".."), file);
      const result = parseTableHtml(html, schema, relPath);

      if (result.table) {
        allTables.push(result.table);
        totalParsed++;
      } else {
        failures.push({ file: relPath, error: result.error || "unknown error" });
      }
    }
  }

  // Write main output
  const output = {
    extractionDate: new Date().toISOString(),
    sourceVersion: "EHI WebERDiagram 22.1 PR38",
    product: "Altera Sunrise (Acute Care / Ambulatory Care)",
    summary: {
      totalFilesDiscovered: totalDiscovered,
      totalFilesParsed: totalParsed,
      parseFailures: failures.length,
      tablesBySchema: {} as Record<string, number>,
      totalColumns: allTables.reduce((sum, t) => sum + t.columns.length, 0),
    },
    tables: allTables,
    parseFailures: failures,
  };

  for (const schema of schemas) {
    output.summary.tablesBySchema[schema] = allTables.filter(
      (t) => t.schema === schema
    ).length;
  }

  await writeFile(
    join(OUTPUT_DIR, "tables.json"),
    JSON.stringify(output, null, 2)
  );

  // Write summary CSV for quick querying
  const csvLines = ["schema,table_name,definition,column_count,has_pk"];
  for (const t of allTables) {
    const hasPk = t.columns.some((c) => c.isPrimaryKey) || t.keys.length > 0;
    const def = t.definition.replace(/"/g, '""');
    csvLines.push(
      `${t.schema},"${t.tableName}","${def}",${t.columns.length},${hasPk}`
    );
  }
  await writeFile(join(OUTPUT_DIR, "tables-summary.csv"), csvLines.join("\n"));

  // Write columns CSV
  const colCsvLines = [
    "schema,table_name,column_name,datatype,nullable,is_pk,definition",
  ];
  for (const t of allTables) {
    for (const c of t.columns) {
      const def = c.definition.replace(/"/g, '""');
      colCsvLines.push(
        `${t.schema},"${t.tableName}","${c.name}","${c.datatype}",${c.nullable},${c.isPrimaryKey},"${def}"`
      );
    }
  }
  await writeFile(join(OUTPUT_DIR, "columns.csv"), colCsvLines.join("\n"));

  console.log("\n=== Extraction Complete ===");
  console.log(`Tables discovered: ${totalDiscovered}`);
  console.log(`Tables parsed: ${totalParsed}`);
  console.log(`Parse failures: ${failures.length}`);
  console.log(
    `Total columns: ${output.summary.totalColumns}`
  );
  console.log(`By schema: ${JSON.stringify(output.summary.tablesBySchema)}`);
  if (failures.length > 0) {
    console.log("\nFailures:");
    for (const f of failures.slice(0, 10)) {
      console.log(`  ${f.file}: ${f.error}`);
    }
    if (failures.length > 10) {
      console.log(`  ... and ${failures.length - 10} more`);
    }
  }
}

main().catch(console.error);
