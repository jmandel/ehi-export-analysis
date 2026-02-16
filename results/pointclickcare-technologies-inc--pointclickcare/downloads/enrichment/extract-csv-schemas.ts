#!/usr/bin/env bun
/**
 * extract-csv-schemas.ts
 *
 * Parses the MDS.html and NonMDS.html pages from the PointClickCare EHI Export IG
 * and extracts the CSV schema definitions into queryable JSON.
 */

import { readFile, writeFile } from "fs/promises";
import { join } from "path";

const SITE_DIR = join(import.meta.dir, "..", "site");
const OUTPUT_FILE = join(import.meta.dir, "csv-schemas.json");

interface CsvColumn {
  name: string;
  type: string;
  nullable: boolean;
  description: string;
}

interface CsvSchema {
  fileName: string;
  source: string; // "mds" or "non_mds"
  sourcePage: string;
  columns: CsvColumn[];
}

function extractTablesFromHtml(html: string, source: string, sourcePage: string): CsvSchema[] {
  const schemas: CsvSchema[] = [];

  // Find all h3 headings that indicate a CSV file schema
  const h3Regex = /<h3\s+id="([^"]+)"[^>]*>([^<]*\.csv)<\/h3>/gi;
  let match;

  while ((match = h3Regex.exec(html)) !== null) {
    const csvName = match[2].trim();

    // Find the table that follows this heading
    const afterHeading = html.substring(match.index);
    const tableMatch = afterHeading.match(/<table>([\s\S]*?)<\/table>/);
    if (!tableMatch) continue;

    const tableHtml = tableMatch[1];
    const columns: CsvColumn[] = [];

    // Extract rows from tbody
    const rowRegex = /<tr>\s*<td>([^<]*)<\/td>\s*<td>([^<]*)<\/td>\s*<td>([^<]*)<\/td>\s*<td>([^<]*)<\/td>\s*<\/tr>/gi;
    let rowMatch;
    while ((rowMatch = rowRegex.exec(tableHtml)) !== null) {
      columns.push({
        name: rowMatch[1].trim(),
        type: rowMatch[2].trim(),
        nullable: rowMatch[3].trim().toLowerCase() === "yes",
        description: rowMatch[4].trim(),
      });
    }

    if (columns.length > 0) {
      schemas.push({
        fileName: csvName,
        source,
        sourcePage,
        columns,
      });
    }
  }

  return schemas;
}

async function main() {
  const schemas: CsvSchema[] = [];
  const failures: { file: string; error: string }[] = [];

  // Parse MDS.html
  try {
    const mdsHtml = await readFile(join(SITE_DIR, "MDS.html"), "utf-8");
    const mdsSchemas = extractTablesFromHtml(mdsHtml, "mds", "MDS.html");
    schemas.push(...mdsSchemas);
    console.log(`MDS.html: extracted ${mdsSchemas.length} CSV schemas`);
  } catch (e: any) {
    failures.push({ file: "MDS.html", error: e.message });
  }

  // Parse NonMDS.html
  try {
    const nonMdsHtml = await readFile(join(SITE_DIR, "NonMDS.html"), "utf-8");
    const nonMdsSchemas = extractTablesFromHtml(nonMdsHtml, "non_mds", "NonMDS.html");
    schemas.push(...nonMdsSchemas);
    console.log(`NonMDS.html: extracted ${nonMdsSchemas.length} CSV schemas`);
  } catch (e: any) {
    failures.push({ file: "NonMDS.html", error: e.message });
  }

  const output = {
    extractionDate: new Date().toISOString().split("T")[0],
    description: "CSV schema definitions for MDS and non-MDS assessment exports in the PointClickCare EHI Export",
    schemas,
    accounting: {
      totalSchemas: schemas.length,
      totalColumns: schemas.reduce((sum, s) => sum + s.columns.length, 0),
      parseFailures: failures,
    },
  };

  await writeFile(OUTPUT_FILE, JSON.stringify(output, null, 2));
  console.log(`\nTotal: ${schemas.length} CSV schemas, ${output.accounting.totalColumns} columns`);
  for (const s of schemas) {
    console.log(`  ${s.source}/${s.fileName}: ${s.columns.length} columns`);
  }
}

main().catch(console.error);
