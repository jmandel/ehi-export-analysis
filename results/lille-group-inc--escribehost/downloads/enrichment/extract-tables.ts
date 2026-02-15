#!/usr/bin/env bun
/**
 * Parses the escribeHOST EHI Export Format Documentation HTML into structured JSON.
 *
 * Input:  ../ehi-export-doc.html
 * Output: ./ehi-tables.json          — full structured data dictionary
 *         ./ehi-tables-summary.json   — table-level summary with column counts
 *         ./extraction-report.json    — parsing coverage/accounting
 */

import { readFileSync, writeFileSync } from "fs";
import { join, dirname } from "path";

const scriptDir = dirname(new URL(import.meta.url).pathname);
const inputPath = join(scriptDir, "..", "ehi-export-doc.html");
const html = readFileSync(inputPath, "utf-8");

interface Column {
  ordinal: number;
  name: string;
  isPrimaryKey: boolean;
  dataType: string;
  nullable: boolean;
  description: string;
  constraints: string[];
}

interface Table {
  name: string;
  description: string;
  columns: Column[];
}

interface ExtractionReport {
  inputFile: string;
  inputSizeBytes: number;
  totalTablesDiscovered: number;
  totalTablesParsed: number;
  totalColumns: number;
  parseFailures: { tableName: string; error: string }[];
  timestamp: string;
}

// Split HTML by <h2> sections
const h2Pattern = /<h2\s+id="([^"]+)"[^>]*>(.*?)<\/h2>/g;
const matches: { id: string; heading: string; startIndex: number }[] = [];
let m: RegExpExecArray | null;
while ((m = h2Pattern.exec(html)) !== null) {
  matches.push({
    id: m[1],
    heading: m[2].trim(),
    startIndex: m.index + m[0].length,
  });
}

const tables: Table[] = [];
const failures: { tableName: string; error: string }[] = [];

for (let i = 0; i < matches.length; i++) {
  const { id, heading, startIndex } = matches[i];
  const endIndex = i + 1 < matches.length ? matches[i + 1].startIndex - (html.slice(matches[i + 1].startIndex).search(/<h2/) > -1 ? 200 : 0) : html.length;
  // Simpler: just grab until next h2 tag or end of file
  const nextH2 = html.indexOf("<h2", startIndex + 1);
  const sectionHtml = html.slice(startIndex, nextH2 > 0 ? nextH2 : html.length);

  // Extract description from heading: "TABLE_NAME - Description text."
  const descMatch = heading.match(/^[A-Z_]+\s*-\s*(.*)/);
  const description = descMatch ? descMatch[1].trim() : heading;

  try {
    const columns = parseTableSection(sectionHtml);
    tables.push({ name: id, description, columns });
  } catch (e: any) {
    failures.push({ tableName: id, error: e.message });
  }
}

function parseTableSection(sectionHtml: string): Column[] {
  const columns: Column[] = [];

  // Find all <tr class="borderBottom"> — these are column definition rows
  // Each column row is followed by description row(s) and optional constraint row(s)
  // Pattern: <tr class="borderBottom">..column..</tr> then <tr><td colspan="2">desc</td></tr> then optionally <tr><td colspan="2" class="checkConstraints">...</td></tr>

  // Split into rows
  const rowPattern = /<tr[^>]*>([\s\S]*?)<\/tr>/g;
  const rows: { html: string; isBorderBottom: boolean; isConstraint: boolean }[] = [];
  let rm: RegExpExecArray | null;
  while ((rm = rowPattern.exec(sectionHtml)) !== null) {
    const fullTag = rm[0];
    const inner = rm[1];
    const isBorderBottom = fullTag.startsWith('<tr class="borderBottom"');
    const isConstraint = inner.includes('class="checkConstraints"');
    rows.push({ html: inner, isBorderBottom, isConstraint });
  }

  // Group: each borderBottom row starts a new column, followed by desc/constraint rows until next borderBottom
  let currentColumn: Partial<Column> | null = null;
  let descParts: string[] = [];
  let constraintParts: string[] = [];

  function flushColumn() {
    if (currentColumn && currentColumn.name) {
      columns.push({
        ordinal: currentColumn.ordinal ?? 0,
        name: currentColumn.name ?? "",
        isPrimaryKey: currentColumn.isPrimaryKey ?? false,
        dataType: currentColumn.dataType ?? "",
        nullable: currentColumn.nullable ?? false,
        description: descParts.join(" ").trim(),
        constraints: constraintParts.filter(c => c.trim()),
      });
    }
    currentColumn = null;
    descParts = [];
    constraintParts = [];
  }

  for (const row of rows) {
    if (row.isBorderBottom) {
      flushColumn();

      // Parse column name and data type from this row
      // <td class="column"><strong>1. COLUMN_NAME</strong> (PK) (nullable)</td>
      // <td class="column">DATA_TYPE</td>
      const tdPattern = /<td[^>]*>([\s\S]*?)<\/td>/g;
      const tds: string[] = [];
      let tdm: RegExpExecArray | null;
      while ((tdm = tdPattern.exec(row.html)) !== null) {
        tds.push(tdm[1]);
      }

      if (tds.length >= 2) {
        const nameTd = tds[0];
        const typeTd = tds[1];

        // Extract ordinal and name
        const stripped = nameTd.replace(/<[^>]*>/g, "").replace(/\s+/g, " ").trim();
        const nameMatch = stripped.match(/(\d+)\s*\.\s*([A-Z_][A-Z0-9_]*)/);
        const ordinal = nameMatch ? parseInt(nameMatch[1]) : 0;
        const name = nameMatch ? nameMatch[2] : stripped;
        const isPK = stripped.includes("(PK)");
        const isNullable = stripped.includes("(nullable)");
        const dataType = typeTd.replace(/<[^>]*>/g, "").trim();

        currentColumn = { ordinal, name, isPrimaryKey: isPK, dataType, nullable: isNullable };
      }
    } else if (row.html.includes('colspan="2"')) {
      // Description or constraint row
      const text = row.html.replace(/<[^>]*>/g, "").replace(/\s+/g, " ").trim();
      if (row.isConstraint) {
        constraintParts.push(text);
      } else if (text && text !== "Column Name" && text !== "Data Type") {
        descParts.push(text);
      }
    }
  }
  flushColumn();

  return columns;
}

// Write outputs
const report: ExtractionReport = {
  inputFile: "ehi-export-doc.html",
  inputSizeBytes: Buffer.byteLength(html),
  totalTablesDiscovered: matches.length,
  totalTablesParsed: tables.length,
  totalColumns: tables.reduce((sum, t) => sum + t.columns.length, 0),
  parseFailures: failures,
  timestamp: new Date().toISOString(),
};

// Full data dictionary
writeFileSync(join(scriptDir, "ehi-tables.json"), JSON.stringify(tables, null, 2));

// Summary
const summary = tables.map(t => ({
  name: t.name,
  description: t.description,
  columnCount: t.columns.length,
  primaryKeys: t.columns.filter(c => c.isPrimaryKey).map(c => c.name),
  foreignKeyHints: t.columns.filter(c => c.name.endsWith("_ID") && !c.isPrimaryKey).map(c => c.name),
}));
writeFileSync(join(scriptDir, "ehi-tables-summary.json"), JSON.stringify(summary, null, 2));

// Extraction report
writeFileSync(join(scriptDir, "extraction-report.json"), JSON.stringify(report, null, 2));

console.log(`Parsed ${tables.length} tables with ${report.totalColumns} total columns.`);
if (failures.length) {
  console.log(`Failures: ${failures.length}`);
  for (const f of failures) console.log(`  ${f.tableName}: ${f.error}`);
}
