/**
 * Extract Nextech Select/NexCloud EHI Export Data Dictionary from XLSX
 * to queryable JSON format.
 *
 * Usage: bun run extract-data-dictionary.ts
 */

import * as XLSX from "xlsx";
import { writeFileSync } from "fs";
import { resolve, dirname } from "path";

const SCRIPT_DIR = dirname(new URL(import.meta.url).pathname);
const INPUT_FILE = resolve(
  SCRIPT_DIR,
  "../Nextech_Select_NexCloud_EHI_Export_Data_Dictionary_2025.xlsx"
);
const OUTPUT_FILE = resolve(SCRIPT_DIR, "data-dictionary.json");
const SUMMARY_FILE = resolve(SCRIPT_DIR, "extraction-summary.json");

interface Field {
  field_name: string;
  description: string;
  note: string | null;
}

interface ExportEntity {
  sheet_name: string;
  export_format: string; // "CSV" or "PDF" or other
  export_filename: string | null; // e.g. "Charges.csv"
  field_count: number;
  fields: Field[];
}

interface DataDictionary {
  source_file: string;
  extraction_date: string;
  entities: ExportEntity[];
  total_fields: number;
  total_entities: number;
}

interface ExtractionSummary {
  source_file: string;
  extraction_date: string;
  total_sheets_discovered: number;
  total_sheets_parsed: number;
  parse_failures: Array<{ sheet: string; error: string }>;
  entities: Array<{
    sheet_name: string;
    export_format: string;
    field_count: number;
  }>;
  total_fields: number;
}

function main() {
  const wb = XLSX.readFile(INPUT_FILE);
  const entities: ExportEntity[] = [];
  const failures: Array<{ sheet: string; error: string }> = [];

  for (const sheetName of wb.SheetNames) {
    try {
      const ws = wb.Sheets[sheetName];
      const rows: Record<string, string>[] = XLSX.utils.sheet_to_json(ws);

      // Parse format from sheet name, e.g. "Charges (CSV)" => "CSV"
      const formatMatch = sheetName.match(/\((\w+)\)\s*$/);
      const exportFormat = formatMatch ? formatMatch[1] : "Unknown";

      // Parse filename, e.g. "Charges (CSV)" => "Charges.csv"
      const baseName = sheetName.replace(/\s*\(\w+\)\s*$/, "").trim();
      const ext = exportFormat.toLowerCase();
      const exportFilename =
        ext !== "unknown" ? `${baseName}.${ext}` : baseName;

      const fields: Field[] = rows.map((row) => ({
        field_name: String(row["Field Name"] || "").trim(),
        description: String(row["Description"] || "").trim(),
        note: row["Note"] ? String(row["Note"]).trim() : null,
      }));

      entities.push({
        sheet_name: sheetName,
        export_format: exportFormat,
        export_filename: exportFilename,
        field_count: fields.length,
        fields,
      });
    } catch (err: any) {
      failures.push({ sheet: sheetName, error: err.message });
    }
  }

  const totalFields = entities.reduce((s, e) => s + e.field_count, 0);

  const dictionary: DataDictionary = {
    source_file:
      "Nextech_Select_NexCloud_EHI_Export_Data_Dictionary_2025.xlsx",
    extraction_date: new Date().toISOString().slice(0, 10),
    entities,
    total_fields: totalFields,
    total_entities: entities.length,
  };

  const summary: ExtractionSummary = {
    source_file:
      "Nextech_Select_NexCloud_EHI_Export_Data_Dictionary_2025.xlsx",
    extraction_date: new Date().toISOString().slice(0, 10),
    total_sheets_discovered: wb.SheetNames.length,
    total_sheets_parsed: entities.length,
    parse_failures: failures,
    entities: entities.map((e) => ({
      sheet_name: e.sheet_name,
      export_format: e.export_format,
      field_count: e.field_count,
    })),
    total_fields: totalFields,
  };

  writeFileSync(OUTPUT_FILE, JSON.stringify(dictionary, null, 2));
  writeFileSync(SUMMARY_FILE, JSON.stringify(summary, null, 2));

  console.log(`Extracted ${totalFields} fields across ${entities.length} entities`);
  console.log(`Output: ${OUTPUT_FILE}`);
  console.log(`Summary: ${SUMMARY_FILE}`);
  if (failures.length > 0) {
    console.log(`Failures: ${failures.length}`);
    failures.forEach((f) => console.log(`  - ${f.sheet}: ${f.error}`));
  }
}

main();
