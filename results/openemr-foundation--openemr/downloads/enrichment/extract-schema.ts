#!/usr/bin/env bun
/**
 * Extracts the OpenEMR EHI Export SchemaSpy XML into queryable JSON.
 *
 * Input:  ../openemr.openemr.xml  (SchemaSpy XML export)
 * Output: schema.json             (full structured schema)
 *         coverage.json           (parsing accounting)
 *
 * Run:  cd enrichment && bun run extract-schema.ts
 */

import { readFileSync, writeFileSync } from "fs";
import { join } from "path";

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------

interface Column {
  id: number;
  name: string;
  type: string;
  typeCode: number;
  size: number;
  digits: number;
  nullable: boolean;
  autoUpdated: boolean;
  defaultValue: string | null;
  remarks: string;
  children: ForeignKeyRef[];
  parents: ForeignKeyRef[];
}

interface ForeignKeyRef {
  catalog: string;
  table: string;
  column: string;
  foreignKey: string;
  implied: boolean;
  onDeleteCascade: boolean;
}

interface Index {
  name: string;
  unique: boolean;
  columns: { name: string; ascending: boolean }[];
}

interface Table {
  name: string;
  catalog: string;
  schema: string;
  type: string;
  numRows: number | null;
  remarks: string;
  columns: Column[];
  primaryKey: { column: string; sequenceNumberInPK: number }[];
  indexes: Index[];
}

interface Schema {
  databaseName: string;
  databaseSchema: string;
  databaseType: string;
  tables: Table[];
}

// ---------------------------------------------------------------------------
// Minimal XML helpers (no external deps)
// ---------------------------------------------------------------------------

function attr(el: string, name: string): string {
  const m = el.match(new RegExp(`${name}="([^"]*)"`));
  return m ? m[1] : "";
}

function boolAttr(el: string, name: string): boolean {
  return attr(el, name) === "true";
}

function intAttr(el: string, name: string): number {
  const v = attr(el, name);
  return v ? parseInt(v, 10) : 0;
}

function intAttrOrNull(el: string, name: string): number | null {
  const v = attr(el, name);
  return v ? parseInt(v, 10) : null;
}

// ---------------------------------------------------------------------------
// Parse
// ---------------------------------------------------------------------------

const xmlPath = join(import.meta.dir, "..", "openemr.openemr.xml");
const xml = readFileSync(xmlPath, "utf-8");

// Database root
const dbMatch = xml.match(/<database\s+([^>]+)>/);
if (!dbMatch) throw new Error("Could not find <database> element");
const dbAttrs = dbMatch[1];

const schema: Schema = {
  databaseName: attr(dbAttrs, "name"),
  databaseSchema: attr(dbAttrs, "schema"),
  databaseType: attr(dbAttrs, "type"),
  tables: [],
};

// Split into table blocks. Tables can be self-closing or have children.
// Strategy: match from <table to the next </table> or self-closing />
const tableBlocks: string[] = [];
const tableRegex = /<table\s+[^>]*?(?:\/>|>[\s\S]*?<\/table>)/g;
let tm: RegExpExecArray | null;
while ((tm = tableRegex.exec(xml)) !== null) {
  tableBlocks.push(tm[0]);
}

const parseFailures: { table: string; error: string }[] = [];

for (const block of tableBlocks) {
  try {
    const openTag = block.match(/<table\s+([^>\/]*)/);
    if (!openTag) continue;
    const ta = openTag[1];

    const table: Table = {
      name: attr(ta, "name"),
      catalog: attr(ta, "catalog"),
      schema: attr(ta, "schema"),
      type: attr(ta, "type"),
      numRows: intAttrOrNull(ta, "numRows"),
      remarks: attr(ta, "remarks"),
      columns: [],
      primaryKey: [],
      indexes: [],
    };

    // Columns
    const colRegex = /<column\s+([^>]*?)(?:\/>|>([\s\S]*?)<\/column>)/g;
    let cm: RegExpExecArray | null;
    while ((cm = colRegex.exec(block)) !== null) {
      const ca = cm[1];
      const colBody = cm[2] || "";

      const col: Column = {
        id: intAttr(ca, "id"),
        name: attr(ca, "name"),
        type: attr(ca, "type"),
        typeCode: intAttr(ca, "typeCode"),
        size: intAttr(ca, "size"),
        digits: intAttr(ca, "digits"),
        nullable: boolAttr(ca, "nullable") || attr(ca, "nullable") === "true",
        autoUpdated: boolAttr(ca, "autoUpdated"),
        defaultValue: attr(ca, "defaultValue") || null,
        remarks: attr(ca, "remarks"),
        children: [],
        parents: [],
      };

      // child refs
      const childRegex = /<child\s+([^>]*?)\/>/g;
      let chm: RegExpExecArray | null;
      while ((chm = childRegex.exec(colBody)) !== null) {
        col.children.push({
          catalog: attr(chm[1], "catalog"),
          table: attr(chm[1], "table"),
          column: attr(chm[1], "column"),
          foreignKey: attr(chm[1], "foreignKey"),
          implied: boolAttr(chm[1], "implied"),
          onDeleteCascade: boolAttr(chm[1], "onDeleteCascade"),
        });
      }

      // parent refs
      const parentRegex = /<parent\s+([^>]*?)\/>/g;
      let pm: RegExpExecArray | null;
      while ((pm = parentRegex.exec(colBody)) !== null) {
        col.parents.push({
          catalog: attr(pm[1], "catalog"),
          table: attr(pm[1], "table"),
          column: attr(pm[1], "column"),
          foreignKey: attr(pm[1], "foreignKey"),
          implied: boolAttr(pm[1], "implied"),
          onDeleteCascade: boolAttr(pm[1], "onDeleteCascade"),
        });
      }

      table.columns.push(col);
    }

    // Primary keys
    const pkRegex = /<primaryKey\s+([^>]*?)\/>/g;
    let pkm: RegExpExecArray | null;
    while ((pkm = pkRegex.exec(block)) !== null) {
      table.primaryKey.push({
        column: attr(pkm[1], "column"),
        sequenceNumberInPK: intAttr(pkm[1], "sequenceNumberInPK"),
      });
    }

    // Indexes
    const idxRegex = /<index\s+([^>]*?)>([\s\S]*?)<\/index>/g;
    let im: RegExpExecArray | null;
    while ((im = idxRegex.exec(block)) !== null) {
      const idxCols: { name: string; ascending: boolean }[] = [];
      const icRegex = /<column\s+([^>]*?)\/>/g;
      let icm: RegExpExecArray | null;
      while ((icm = icRegex.exec(im[2])) !== null) {
        idxCols.push({
          name: attr(icm[1], "name"),
          ascending: boolAttr(icm[1], "ascending"),
        });
      }
      table.indexes.push({
        name: attr(im[1], "name"),
        unique: boolAttr(im[1], "unique"),
        columns: idxCols,
      });
    }

    schema.tables.push(table);
  } catch (e: any) {
    const name = attr(block, "name") || "unknown";
    parseFailures.push({ table: name, error: e.message });
  }
}

// ---------------------------------------------------------------------------
// Write outputs
// ---------------------------------------------------------------------------

const outDir = import.meta.dir;

writeFileSync(join(outDir, "schema.json"), JSON.stringify(schema, null, 2));

// Coverage accounting
const totalColumns = schema.tables.reduce((s, t) => s + t.columns.length, 0);
const tablesWithRemarks = schema.tables.filter((t) => t.remarks.length > 0).length;
const columnsWithRemarks = schema.tables.reduce(
  (s, t) => s + t.columns.filter((c) => c.remarks.length > 0).length,
  0
);
const relationships = schema.tables.reduce(
  (s, t) =>
    s +
    t.columns.reduce(
      (cs, c) => cs + c.parents.length + c.children.length,
      0
    ),
  0
);

const coverage = {
  xml_file: xmlPath,
  total_tables: schema.tables.length,
  total_columns: totalColumns,
  tables_with_remarks: tablesWithRemarks,
  columns_with_remarks: columnsWithRemarks,
  total_relationships: relationships,
  parse_failures: parseFailures.length,
  parse_failure_details: parseFailures,
  tables_by_type: Object.fromEntries(
    Object.entries(
      schema.tables.reduce((acc: Record<string, number>, t) => {
        acc[t.type || "unknown"] = (acc[t.type || "unknown"] || 0) + 1;
        return acc;
      }, {})
    )
  ),
};

writeFileSync(join(outDir, "coverage.json"), JSON.stringify(coverage, null, 2));

console.log("=== OpenEMR EHI Export Schema Extraction ===");
console.log(`Tables parsed:        ${schema.tables.length}`);
console.log(`Columns parsed:       ${totalColumns}`);
console.log(`Tables with remarks:  ${tablesWithRemarks}`);
console.log(`Columns with remarks: ${columnsWithRemarks}`);
console.log(`Relationships:        ${relationships}`);
console.log(`Parse failures:       ${parseFailures.length}`);
if (parseFailures.length > 0) {
  for (const f of parseFailures) {
    console.log(`  FAIL: ${f.table}: ${f.error}`);
  }
}
console.log(`\nOutput: schema.json, coverage.json`);
