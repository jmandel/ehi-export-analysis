/**
 * Extract structured schema data from DrCloudEHR SchemaSpy XML export.
 *
 * Input:  ../drcloudehr.FHIR.xml  (SchemaSpy XML database documentation)
 * Output: schema.json             (queryable JSON with tables, columns, relationships)
 *         coverage-report.json    (accounting of parsed vs total entities)
 *
 * Usage:  bun run extract-schema.ts
 */

import { readFileSync, writeFileSync } from "fs";
import { join, dirname } from "path";

const scriptDir = dirname(new URL(import.meta.url).pathname);
const inputPath = join(scriptDir, "..", "drcloudehr.FHIR.xml");
const outputPath = join(scriptDir, "schema.json");
const coveragePath = join(scriptDir, "coverage-report.json");

// Use a streaming approach: split into table blocks, then parse
// columns that are direct children (not inside <index> blocks).
const xml = readFileSync(inputPath, "utf-8");

interface Column {
  name: string;
  type: string;
  size: string;
  nullable: boolean;
  autoUpdated: boolean;
  defaultValue: string | null;
  remarks: string;
  parents: { table: string; column: string }[];
  children: { table: string; column: string }[];
}

interface Index {
  name: string;
  unique: boolean;
  columns: string[];
}

interface Table {
  name: string;
  remarks: string;
  numRows: number;
  columns: Column[];
  primaryKey: string[];
  indexes: Index[];
}

interface Schema {
  databaseName: string;
  schemaName: string;
  databaseType: string;
  tables: Table[];
}

function parseAttrs(s: string): Record<string, string> {
  const result: Record<string, string> = {};
  const re = /(\w+)="([^"]*)"/g;
  let m: RegExpExecArray | null;
  while ((m = re.exec(s)) !== null) {
    result[m[1]] = decodeXml(m[2]);
  }
  return result;
}

function decodeXml(s: string): string {
  return s
    .replace(/&amp;/g, "&")
    .replace(/&lt;/g, "<")
    .replace(/&gt;/g, ">")
    .replace(/&quot;/g, '"')
    .replace(/&apos;/g, "'")
    .replace(/&#(\d+);/g, (_, n) => String.fromCharCode(parseInt(n)))
    .replace(/&#x([0-9a-fA-F]+);/g, (_, n) => String.fromCharCode(parseInt(n, 16)));
}

// Parse database attributes
const dbMatch = xml.match(/<database\s+([^>]+)>/);
const dbAttrs = parseAttrs(dbMatch?.[1] ?? "");

// Split XML into table blocks
const tableBlocks = xml.match(/<table\s[^>]*>[\s\S]*?<\/table>/g) ?? [];

const tables: Table[] = [];
const parseErrors: { table: string; error: string }[] = [];

for (const block of tableBlocks) {
  try {
    const tAttrs = parseAttrs(block.match(/<table\s+([^>]+)>/)?.[1] ?? "");
    const tableName = tAttrs.name ?? "unknown";

    // Remove index blocks so we only parse top-level column elements
    const withoutIndexes = block.replace(/<index\s[^>]*>[\s\S]*?<\/index>/g, "");

    // Parse columns — match self-closing (/>) and open/close (>...</column>) forms separately
    // The combined regex is unreliable because /> ends with > and the alternation confuses them.
    const selfClosing = withoutIndexes.match(/<column\s[^>]*\/>/g) ?? [];
    const openClose = withoutIndexes.match(/<column\s[^>]*[^/]>[\s\S]*?<\/column>/g) ?? [];
    const colBlocks = [...selfClosing, ...openClose];
    const columns: Column[] = [];

    for (const colBlock of colBlocks) {
      const cAttrs = parseAttrs(colBlock);

      // Parse parent refs
      const parents: { table: string; column: string }[] = [];
      const parentMatches = colBlock.match(/<parent\s[^>]*\/>/g) ?? [];
      for (const pm of parentMatches) {
        const pAttrs = parseAttrs(pm);
        if (pAttrs.table && pAttrs.column) {
          parents.push({ table: pAttrs.table, column: pAttrs.column });
        }
      }

      // Parse child refs
      const children: { table: string; column: string }[] = [];
      const childMatches = colBlock.match(/<child\s[^>]*\/>/g) ?? [];
      for (const cm of childMatches) {
        const chAttrs = parseAttrs(cm);
        if (chAttrs.table && chAttrs.column) {
          children.push({ table: chAttrs.table, column: chAttrs.column });
        }
      }

      columns.push({
        name: cAttrs.name ?? "",
        type: cAttrs.type ?? "Unknown",
        size: cAttrs.size ?? "",
        nullable: cAttrs.nullable === "true",
        autoUpdated: cAttrs.autoUpdated === "true",
        defaultValue: cAttrs.defaultValue === "null" ? null : (cAttrs.defaultValue ?? null),
        remarks: cAttrs.remarks ?? "",
        parents,
        children,
      });
    }

    // Parse primary key
    const pkMatches = block.match(/<primaryKey\s[^>]*\/>/g) ?? [];
    const primaryKey = pkMatches.map((pk) => parseAttrs(pk).column).filter(Boolean);

    // Parse indexes
    const indexBlocks = block.match(/<index\s[^>]*>[\s\S]*?<\/index>/g) ?? [];
    const indexes: Index[] = [];
    for (const ib of indexBlocks) {
      const iAttrs = parseAttrs(ib.match(/<index\s+([^>]+)>/)?.[1] ?? "");
      const idxCols = (ib.match(/<column\s[^>]*\/>/g) ?? []).map((c) => parseAttrs(c).name).filter(Boolean);
      indexes.push({
        name: iAttrs.name ?? "",
        unique: iAttrs.unique === "true",
        columns: idxCols,
      });
    }

    tables.push({
      name: tableName,
      remarks: tAttrs.remarks ?? "",
      numRows: parseInt(tAttrs.numRows ?? "0", 10),
      columns,
      primaryKey,
      indexes,
    });
  } catch (e: any) {
    const tName = block.match(/name="([^"]+)"/)?.[1] ?? "unknown";
    parseErrors.push({ table: tName, error: e.message });
  }
}

const schema: Schema = {
  databaseName: dbAttrs.name ?? "unknown",
  schemaName: dbAttrs.schema ?? "unknown",
  databaseType: dbAttrs.type ?? "unknown",
  tables,
};

writeFileSync(outputPath, JSON.stringify(schema, null, 2));

// Coverage report
const totalColumns = tables.reduce((sum, t) => sum + t.columns.length, 0);
const columnsWithRemarks = tables.reduce(
  (sum, t) => sum + t.columns.filter((c) => c.remarks.length > 0).length,
  0
);
const tablesWithRemarks = tables.filter((t) => t.remarks.length > 0).length;
const totalRelationships = tables.reduce(
  (sum, t) => sum + t.columns.reduce((s2, c) => s2 + c.parents.length + c.children.length, 0),
  0
);

const coverage = {
  extraction_date: new Date().toISOString(),
  input_file: "drcloudehr.FHIR.xml",
  total_tables: tables.length,
  total_columns: totalColumns,
  tables_with_remarks: tablesWithRemarks,
  columns_with_remarks: columnsWithRemarks,
  columns_without_remarks: totalColumns - columnsWithRemarks,
  remark_coverage_pct: Math.round((columnsWithRemarks / totalColumns) * 100 * 10) / 10,
  total_relationships: totalRelationships,
  parse_failures: parseErrors,
  output_files: ["schema.json", "coverage-report.json"],
};

writeFileSync(coveragePath, JSON.stringify(coverage, null, 2));

console.log(`Extracted ${tables.length} tables, ${totalColumns} columns`);
console.log(`Remarks coverage: ${coverage.remark_coverage_pct}% of columns have remarks`);
console.log(`Relationships: ${totalRelationships} total`);
console.log(`Parse errors: ${parseErrors.length}`);
if (parseErrors.length > 0) {
  for (const e of parseErrors) {
    console.log(`  ${e.table}: ${e.error}`);
  }
}
