#!/usr/bin/env bun
/**
 * Extracts CureMD EHI Export DRS (Designated Record Set) data dictionary
 * from the XLSX file into queryable JSON.
 *
 * Input:  ../EHI_Export_DRS.xlsx
 * Output: drs-data-dictionary.json, drs-summary.json, extraction-log.json
 */

import * as XLSX from "xlsx";
import { writeFileSync } from "fs";
import { join, dirname } from "path";

const scriptDir = dirname(new URL(import.meta.url).pathname);
const inputPath = join(scriptDir, "..", "EHI_Export_DRS.xlsx");
const outputDir = scriptDir;

const wb = XLSX.readFile(inputPath);

// --- Extract "EHI Export" overview sheet ---
const overviewSheet = wb.Sheets["EHI Export"];
const overviewData = XLSX.utils.sheet_to_json(overviewSheet, { header: 1 }) as any[][];
const overviewText = overviewData
  .map((row) => row.filter((c) => c != null).join(" "))
  .filter((line) => line.trim().length > 0)
  .join("\n");

// --- Extract "DRS" data dictionary sheet ---
const drsSheet = wb.Sheets["DRS"];
const drsRaw = XLSX.utils.sheet_to_json(drsSheet, { header: 1 }) as any[][];

interface Field {
  name: string;
  dataType: string;
  description: string;
}

interface DataClass {
  name: string;
  fields: Field[];
}

const dataClasses: DataClass[] = [];
let currentClass: DataClass | null = null;

// Row 0 is headers: Data Class | Data Elements | Data Type | Description
for (let i = 1; i < drsRaw.length; i++) {
  const row = drsRaw[i];
  const classCell = row[0] != null ? String(row[0]).trim() : "";
  const fieldName = row[1] != null ? String(row[1]).trim() : "";
  const dataType = row[2] != null ? String(row[2]).trim() : "";
  const description = row[3] != null ? String(row[3]).trim() : "";

  if (classCell) {
    currentClass = { name: classCell, fields: [] };
    dataClasses.push(currentClass);
  }

  if (currentClass && fieldName) {
    currentClass.fields.push({ name: fieldName, dataType, description });
  }
}

// --- Build outputs ---
const totalFields = dataClasses.reduce((sum, dc) => sum + dc.fields.length, 0);

const dataDictionary = {
  source: "CureMD EHI_Export_DRS.xlsx",
  extractedAt: new Date().toISOString(),
  sheets: wb.SheetNames,
  overview: overviewText,
  dataClasses,
};

const summary = {
  source: "CureMD EHI_Export_DRS.xlsx",
  extractedAt: new Date().toISOString(),
  totalDataClasses: dataClasses.length,
  totalFields,
  dataClassSummary: dataClasses.map((dc) => ({
    name: dc.name,
    fieldCount: dc.fields.length,
    fieldNames: dc.fields.map((f) => f.name),
    dataTypes: [...new Set(dc.fields.map((f) => f.dataType))],
  })),
};

const log = {
  extractedAt: new Date().toISOString(),
  inputFile: "EHI_Export_DRS.xlsx",
  sheetsFound: wb.SheetNames,
  totalRawRows: drsRaw.length,
  totalDataClasses: dataClasses.length,
  totalFields,
  parseFailures: [] as string[],
  notes: [
    "Row 0 is header row, skipped",
    "Data class name is in column A, carried forward for rows where it is blank",
    "Two sheets: 'EHI Export' (overview) and 'DRS' (data dictionary)",
  ],
};

writeFileSync(
  join(outputDir, "drs-data-dictionary.json"),
  JSON.stringify(dataDictionary, null, 2)
);
writeFileSync(join(outputDir, "drs-summary.json"), JSON.stringify(summary, null, 2));
writeFileSync(join(outputDir, "extraction-log.json"), JSON.stringify(log, null, 2));

console.log(`Extracted ${dataClasses.length} data classes with ${totalFields} total fields`);
console.log(`Output: drs-data-dictionary.json, drs-summary.json, extraction-log.json`);
