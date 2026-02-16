#!/usr/bin/env bun
/**
 * Extracts Nextech EHI Export data dictionaries from XLSX files into queryable JSON.
 * Parses all three platform data dictionaries: ICP, SRSPro, and NexCloud/Select.
 *
 * Usage: bun run extract-data-dictionaries.ts
 */

import XLSX from "xlsx";
import { writeFileSync, statSync } from "fs";
import { join, basename } from "path";

const DOWNLOADS_DIR = join(import.meta.dir, "..");
const OUTPUT_DIR = import.meta.dir;

interface Field {
  field_name: string;
  description: string;
  note: string | null;
}

interface DataEntity {
  entity_name: string;
  export_format: string; // e.g., "JSON", "CSV", "XML", "PDF", "TXT"
  field_count: number;
  fields: Field[];
}

interface PlatformDictionary {
  platform: string;
  source_file: string;
  source_file_size_bytes: number;
  sheet_count: number;
  entity_count: number;
  total_field_count: number;
  entities: DataEntity[];
}

interface EnrichmentOutput {
  extraction_date: string;
  total_files_discovered: number;
  total_files_parsed: number;
  parse_failures: { file: string; error: string }[];
  platforms: PlatformDictionary[];
  summary: {
    total_entities: number;
    total_fields: number;
    entities_by_platform: Record<string, number>;
    fields_by_platform: Record<string, number>;
    export_formats_used: string[];
  };
}

function parseExportFormat(sheetName: string): string {
  const match = sheetName.match(/\(([^)]+)\)\s*$/);
  if (match) {
    const fmt = match[1].toUpperCase().trim();
    // Normalize multi-format indicators
    if (fmt.includes("JSON") && fmt.includes("CSV")) return "JSON/CSV";
    return fmt;
  }
  // Default: unknown
  return "unknown";
}

function parseEntityName(sheetName: string): string {
  // Strip the format suffix like "(JSON)", "(CSV)", "(XML)", etc.
  return sheetName.replace(/\s*\([^)]*\)\s*\d*$/, "").trim();
}

function parseSheet(ws: XLSX.WorkSheet, sheetName: string): DataEntity {
  const data = XLSX.utils.sheet_to_json<string[]>(ws, { header: 1 });
  const fields: Field[] = [];

  // Determine header row: find first row with "Field" or "Description" in it
  let startRow = 0;
  for (let i = 0; i < Math.min(5, data.length); i++) {
    const row = data[i];
    if (row && row.some((cell) => typeof cell === "string" && /field|description/i.test(cell))) {
      startRow = i + 1; // Data starts after header
      break;
    }
  }

  // If no header found, start from row 0
  if (startRow === 0 && data.length > 0) {
    // Check if first row looks like data (not a header)
    const firstRow = data[0];
    if (firstRow && firstRow.length >= 2) {
      startRow = 0;
    }
  }

  for (let i = startRow; i < data.length; i++) {
    const row = data[i];
    if (!row || row.length === 0) continue;

    const fieldName = row[0]?.toString().trim();
    if (!fieldName) continue;

    // Skip sub-headers that appear in some sheets (e.g., "JSON", "CSV" dividers)
    if (fieldName === "JSON" || fieldName === "CSV") continue;

    const description = row[1]?.toString().trim() || "";
    const note = row[2]?.toString().trim() || null;

    fields.push({
      field_name: fieldName,
      description,
      note,
    });
  }

  return {
    entity_name: parseEntityName(sheetName),
    export_format: parseExportFormat(sheetName),
    field_count: fields.length,
    fields,
  };
}

function parseWorkbook(filePath: string, platformName: string): PlatformDictionary {
  const wb = XLSX.readFile(filePath);
  const stat = statSync(filePath);
  const entities: DataEntity[] = [];

  for (const sheetName of wb.SheetNames) {
    const ws = wb.Sheets[sheetName];
    const entity = parseSheet(ws, sheetName);
    entities.push(entity);
  }

  const totalFields = entities.reduce((sum, e) => sum + e.field_count, 0);

  return {
    platform: platformName,
    source_file: basename(filePath),
    source_file_size_bytes: stat.size,
    sheet_count: wb.SheetNames.length,
    entity_count: entities.length,
    total_field_count: totalFields,
    entities,
  };
}

// Main
const files = [
  {
    path: join(DOWNLOADS_DIR, "nextech-ehr-icp-ehi-data-dictionary.xlsx"),
    platform: "IntelleChartPRO (ICP)",
  },
  {
    path: join(DOWNLOADS_DIR, "srspro-ehi-data-dictionary.xlsx"),
    platform: "SRSPro",
  },
  {
    path: join(DOWNLOADS_DIR, "nextech-select-nexcloud-ehi-data-dictionary.xlsx"),
    platform: "Nextech Select/NexCloud",
  },
];

const output: EnrichmentOutput = {
  extraction_date: new Date().toISOString().split("T")[0],
  total_files_discovered: files.length,
  total_files_parsed: 0,
  parse_failures: [],
  platforms: [],
  summary: {
    total_entities: 0,
    total_fields: 0,
    entities_by_platform: {},
    fields_by_platform: {},
    export_formats_used: [],
  },
};

const formatSet = new Set<string>();

for (const { path, platform } of files) {
  try {
    const result = parseWorkbook(path, platform);
    output.platforms.push(result);
    output.total_files_parsed++;
    output.summary.entities_by_platform[platform] = result.entity_count;
    output.summary.fields_by_platform[platform] = result.total_field_count;
    output.summary.total_entities += result.entity_count;
    output.summary.total_fields += result.total_field_count;
    for (const e of result.entities) {
      formatSet.add(e.export_format);
    }
  } catch (err: any) {
    output.parse_failures.push({
      file: basename(path),
      error: err.message,
    });
  }
}

output.summary.export_formats_used = [...formatSet].sort();

const outputPath = join(OUTPUT_DIR, "data-dictionaries.json");
writeFileSync(outputPath, JSON.stringify(output, null, 2));
console.log(`Written to ${outputPath}`);
console.log(`Platforms parsed: ${output.total_files_parsed}/${output.total_files_discovered}`);
console.log(`Total entities: ${output.summary.total_entities}`);
console.log(`Total fields: ${output.summary.total_fields}`);
console.log(`Parse failures: ${output.parse_failures.length}`);
if (output.parse_failures.length > 0) {
  for (const f of output.parse_failures) {
    console.log(`  FAILED: ${f.file} — ${f.error}`);
  }
}
