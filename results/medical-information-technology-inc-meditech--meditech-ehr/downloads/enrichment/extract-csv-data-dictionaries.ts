#!/usr/bin/env bun
/**
 * Extracts structured data from MEDITECH EHI Export CSV data dictionary PDFs.
 * These PDFs contain Field/Table/Column mappings for the CSV export format
 * used in Configuration 2 (Client/Server, MAGIC, and 6.08 platforms).
 *
 * Usage: bun run extract-csv-data-dictionaries.ts
 * Input: ../csacuteandambehiexportdrsolutionmerged.pdf
 *        ../mgehiexportdrsolutionmerged.pdf
 *        ../608ehiexportcsv.pdf
 * Output: csv-data-dictionaries.json, extraction-stats.json
 */

import { $ } from "bun";

interface FieldMapping {
  field: string;
  table: string;
  column: string;
}

interface TableGroup {
  tableName: string;
  fields: FieldMapping[];
}

interface PlatformDictionary {
  platform: string;
  sourceFile: string;
  lastUpdated: string;
  tables: TableGroup[];
  totalFields: number;
  totalTables: number;
}

interface ExtractionStats {
  extractionDate: string;
  platforms: {
    platform: string;
    sourceFile: string;
    totalTables: number;
    totalFields: number;
    parseErrors: string[];
  }[];
  totalFiles: number;
  totalFilesParsed: number;
  totalTablesAcrossAll: number;
  totalFieldsAcrossAll: number;
}

const pdfs = [
  {
    file: "../csacuteandambehiexportdrsolutionmerged.pdf",
    platform: "Client/Server Acute & Ambulatory",
  },
  {
    file: "../mgehiexportdrsolutionmerged.pdf",
    platform: "MAGIC Acute & Ambulatory",
  },
  {
    file: "../608ehiexportcsv.pdf",
    platform: "MPM 6.08 Ambulatory",
  },
];

async function extractPdf(pdfPath: string): Promise<string> {
  const result = await $`pdftotext -layout ${pdfPath} -`.text();
  return result;
}

function parseDictionary(text: string, platform: string): { tables: TableGroup[]; errors: string[] } {
  const lines = text.split("\n");
  const tables: TableGroup[] = [];
  const errors: string[] = [];
  let currentTable: TableGroup | null = null;
  let headerSeen = false;

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    const trimmed = line.trim();

    // Skip empty lines, header lines, title lines
    if (!trimmed) continue;
    if (trimmed === "Field" || trimmed === "Field                          Table                     Column") continue;
    if (trimmed.startsWith("Field") && trimmed.includes("Table") && trimmed.includes("Column")) {
      headerSeen = true;
      continue;
    }
    if (trimmed.startsWith("EHI Export Patient Data")) continue;
    if (trimmed.startsWith("Platform:")) continue;
    if (trimmed.startsWith("The tables/columns below")) continue;
    if (trimmed === "MEDITECH") continue;
    if (trimmed.includes("EHI Export Data in CSV File")) continue;
    if (trimmed.startsWith("Last Updated:")) continue;
    if (/^\d+$/.test(trimmed)) continue; // page numbers

    // Detect table header: a line with a single word (no spaces in the core,
    // starts at column 0, and no Tab/Table/Column structure)
    // Table headers are lines that start at position 0 and have NO second/third column
    const hasMultipleColumns = /\S\s{2,}\S/.test(line);

    if (!hasMultipleColumns && trimmed.length > 0 && !trimmed.includes("  ")) {
      // This is a table header
      currentTable = { tableName: trimmed, fields: [] };
      tables.push(currentTable);
      continue;
    }

    // Parse field row: Field (col ~0-29), Table (col ~30-55), Column (col ~56+)
    // Use regex to split by 2+ spaces
    if (hasMultipleColumns && currentTable) {
      const parts = trimmed.split(/\s{2,}/);
      if (parts.length >= 3) {
        currentTable.fields.push({
          field: parts[0].trim(),
          table: parts[1].trim(),
          column: parts.slice(2).join(" ").trim(),
        });
      } else if (parts.length === 2) {
        // Sometimes column name runs into table name
        currentTable.fields.push({
          field: parts[0].trim(),
          table: parts[1].trim(),
          column: "",
        });
        errors.push(`Line ${i + 1}: Only 2 columns found: "${trimmed}"`);
      }
    } else if (hasMultipleColumns && !currentTable) {
      errors.push(`Line ${i + 1}: Field row found before any table header: "${trimmed}"`);
    }
  }

  return { tables, errors };
}

async function main() {
  const results: PlatformDictionary[] = [];
  const stats: ExtractionStats = {
    extractionDate: new Date().toISOString(),
    platforms: [],
    totalFiles: pdfs.length,
    totalFilesParsed: 0,
    totalTablesAcrossAll: 0,
    totalFieldsAcrossAll: 0,
  };

  for (const pdf of pdfs) {
    try {
      console.log(`Processing: ${pdf.file} (${pdf.platform})`);
      const text = await extractPdf(pdf.file);
      const { tables, errors } = parseDictionary(text, pdf.platform);

      const totalFields = tables.reduce((sum, t) => sum + t.fields.length, 0);
      const dict: PlatformDictionary = {
        platform: pdf.platform,
        sourceFile: pdf.file.replace("../", ""),
        lastUpdated: "October 2023",
        tables,
        totalFields,
        totalTables: tables.length,
      };
      results.push(dict);

      stats.platforms.push({
        platform: pdf.platform,
        sourceFile: pdf.file.replace("../", ""),
        totalTables: tables.length,
        totalFields,
        parseErrors: errors,
      });
      stats.totalFilesParsed++;
      stats.totalTablesAcrossAll += tables.length;
      stats.totalFieldsAcrossAll += totalFields;

      console.log(`  Tables: ${tables.length}, Fields: ${totalFields}, Errors: ${errors.length}`);
      if (errors.length > 0) {
        errors.forEach((e) => console.log(`    ${e}`));
      }
    } catch (err) {
      console.error(`Failed to process ${pdf.file}: ${err}`);
      stats.platforms.push({
        platform: pdf.platform,
        sourceFile: pdf.file.replace("../", ""),
        totalTables: 0,
        totalFields: 0,
        parseErrors: [`Fatal: ${err}`],
      });
    }
  }

  await Bun.write("csv-data-dictionaries.json", JSON.stringify(results, null, 2));
  await Bun.write("extraction-stats.json", JSON.stringify(stats, null, 2));

  console.log(`\nDone. Total: ${stats.totalFilesParsed}/${stats.totalFiles} files, ${stats.totalTablesAcrossAll} tables, ${stats.totalFieldsAcrossAll} fields`);
}

main();
