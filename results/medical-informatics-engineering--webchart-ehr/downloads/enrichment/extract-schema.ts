#!/usr/bin/env bun
/**
 * Extracts a queryable schema from the WebChart EHI Export documentation.
 *
 * Inputs:
 *   - ../ehi-export-technical-details.md  (markdown source with DRS table + sample JSON)
 *   - ../sample-single-patient-export.json (the sample export JSON)
 *
 * Outputs:
 *   - drs-data-dictionary.json   — object names + descriptions from the DRS table
 *   - export-schema.json         — field-level schema inferred from the sample export
 *   - extraction-report.json     — coverage/accounting output
 */

import { readFileSync, writeFileSync } from "fs";
import { join, dirname } from "path";

const BASE = dirname(import.meta.path);
const DOWNLOADS = join(BASE, "..");

// ─── 1. Parse the DRS data dictionary table from markdown ───

const md = readFileSync(join(DOWNLOADS, "ehi-export-technical-details.md"), "utf-8");

interface DRSObject {
  object_name: string;
  description: string;
}

function parseDRSTable(markdown: string): DRSObject[] {
  const objects: DRSObject[] = [];

  // The DRS table is in HTML format: <tr><td>name</td><td>description</td></tr>
  const tableStart = markdown.indexOf("## Designated Record Set Content");
  const tableEnd = markdown.indexOf("## Example Export Files");
  if (tableStart === -1 || tableEnd === -1) {
    throw new Error("Could not find DRS table boundaries");
  }

  const tableSection = markdown.slice(tableStart, tableEnd);

  // Parse <tr><td>...</td><td>...</td></tr> pairs
  const rowRegex = /<tr>\s*<td>(.*?)<\/td>\s*<td>(.*?)<\/td>\s*<\/tr>/gs;
  let match;
  while ((match = rowRegex.exec(tableSection)) !== null) {
    const name = match[1].replace(/<[^>]*>/g, "").trim();
    const desc = match[2].replace(/<[^>]*>/g, "").trim();
    // Skip the header row
    if (name === "**Object**" || name === "Object") continue;
    objects.push({ object_name: name, description: desc });
  }

  return objects;
}

const drsObjects = parseDRSTable(md);
console.log(`Parsed ${drsObjects.length} DRS objects from markdown table`);

writeFileSync(
  join(BASE, "drs-data-dictionary.json"),
  JSON.stringify(drsObjects, null, 2)
);

// ─── 2. Infer field-level schema from sample export JSON ───

const sampleExport = JSON.parse(
  readFileSync(join(DOWNLOADS, "sample-single-patient-export.json"), "utf-8")
);

interface FieldSchema {
  name: string;
  type: "string" | "number" | "boolean" | "null" | "object" | "array" | "mixed";
  sample_value?: string;
  /** For objects: nested field schemas */
  fields?: FieldSchema[];
  /** For arrays: schema of array items */
  item_schema?: FieldSchema[];
  /** Number of items in sample (for arrays) */
  sample_count?: number;
}

interface ObjectSchema {
  object_name: string;
  description: string;
  relationship_key: string; // e.g. "pat_id" for "accommodations.pat_id"
  fields: FieldSchema[];
  sample_record_count: number;
}

interface ExportSchema {
  format: string;
  top_level_keys: string[];
  request_pattern: string;
  patient_fields: FieldSchema[];
  nested_objects: ObjectSchema[];
}

function inferType(value: unknown): FieldSchema["type"] {
  if (value === null) return "null";
  if (Array.isArray(value)) return "array";
  return typeof value as FieldSchema["type"];
}

function truncateSample(value: unknown): string {
  const s = JSON.stringify(value);
  if (s.length > 100) return s.slice(0, 97) + "...";
  return s;
}

function inferFieldSchema(key: string, value: unknown, maxDepth = 2): FieldSchema {
  const type = inferType(value);
  const schema: FieldSchema = { name: key, type };

  if (type === "string" || type === "number" || type === "boolean") {
    schema.sample_value = truncateSample(value);
  } else if (type === "null") {
    schema.sample_value = "null";
  } else if (type === "object" && value !== null && maxDepth > 0) {
    schema.fields = Object.entries(value as Record<string, unknown>).map(
      ([k, v]) => inferFieldSchema(k, v, maxDepth - 1)
    );
  } else if (type === "array" && maxDepth > 0) {
    const arr = value as unknown[];
    schema.sample_count = arr.length;
    if (arr.length > 0 && typeof arr[0] === "object" && arr[0] !== null) {
      schema.item_schema = Object.entries(arr[0] as Record<string, unknown>).map(
        ([k, v]) => inferFieldSchema(k, v, maxDepth - 1)
      );
    }
  }

  return schema;
}

// Build the drsObjectMap for descriptions
const drsMap = new Map(drsObjects.map((o) => [o.object_name, o.description]));

const patient = sampleExport.db[0];
const patientScalarFields: FieldSchema[] = [];
const nestedObjects: ObjectSchema[] = [];

for (const [key, value] of Object.entries(patient)) {
  if (key.includes(".")) {
    // This is a nested object like "accommodations.pat_id"
    const [objectName, relKey] = key.split(".");
    const arr = value as unknown[];
    const fields: FieldSchema[] = [];
    if (arr.length > 0 && typeof arr[0] === "object" && arr[0] !== null) {
      for (const [fk, fv] of Object.entries(arr[0] as Record<string, unknown>)) {
        fields.push(inferFieldSchema(fk, fv, 2));
      }
    }
    nestedObjects.push({
      object_name: objectName,
      description: drsMap.get(objectName) || "",
      relationship_key: relKey,
      fields,
      sample_record_count: arr.length,
    });
  } else if (Array.isArray(value)) {
    // Top-level array (shouldn't happen for patient but handle it)
    patientScalarFields.push(inferFieldSchema(key, value, 1));
  } else if (typeof value === "object" && value !== null) {
    // Inline object like "revised_by"
    patientScalarFields.push(inferFieldSchema(key, value, 2));
  } else {
    patientScalarFields.push(inferFieldSchema(key, value));
  }
}

const exportSchema: ExportSchema = {
  format: "JSON",
  top_level_keys: Object.keys(sampleExport),
  request_pattern: sampleExport.request,
  patient_fields: patientScalarFields,
  nested_objects: nestedObjects,
};

console.log(`Extracted ${patientScalarFields.length} patient scalar fields`);
console.log(`Extracted ${nestedObjects.length} nested object schemas`);

writeFileSync(
  join(BASE, "export-schema.json"),
  JSON.stringify(exportSchema, null, 2)
);

// ─── 3. Generate extraction report ───

const drsObjectNames = new Set(drsObjects.map((o) => o.object_name));
const exportObjectNames = new Set(nestedObjects.map((o) => o.object_name));

// Objects in DRS table but not seen as nested objects in sample export
const inDRSNotExport = [...drsObjectNames].filter((n) => !exportObjectNames.has(n));
// Objects in sample export but not in DRS table
const inExportNotDRS = [...exportObjectNames].filter((n) => !drsObjectNames.has(n));

// Some DRS objects may be present as top-level patient fields or in other contexts
// "patients" is the top-level object, check special cases
const topLevelMappings = ["patients"]; // patients maps to the patient record itself
const lookupTables = drsObjects
  .filter(
    (o) =>
      o.object_name.endsWith("_types") ||
      o.object_name === "users" ||
      o.object_name === "locations" ||
      o.object_name === "storage_types" ||
      o.object_name === "relation_types" ||
      o.object_name === "observation_codes" ||
      o.object_name === "order_list" ||
      o.object_name === "insurance_plans" ||
      o.object_name === "document_types" ||
      o.object_name === "extended_value_names"
  )
  .map((o) => o.object_name);

const report = {
  extraction_date: new Date().toISOString(),
  inputs: {
    markdown_file: "ehi-export-technical-details.md",
    markdown_size_bytes: Buffer.byteLength(md),
    sample_json_file: "sample-single-patient-export.json",
    sample_json_size_bytes: Buffer.byteLength(JSON.stringify(sampleExport)),
  },
  outputs: {
    drs_data_dictionary: "drs-data-dictionary.json",
    export_schema: "export-schema.json",
    extraction_report: "extraction-report.json",
  },
  parsing_results: {
    drs_objects_in_table: drsObjects.length,
    drs_objects_with_description: drsObjects.filter((o) => o.description).length,
    drs_objects_without_description: drsObjects.filter((o) => !o.description).length,
    patient_scalar_fields: patientScalarFields.length,
    nested_objects_in_sample: nestedObjects.length,
    nested_objects_with_data: nestedObjects.filter((o) => o.sample_record_count > 0).length,
    nested_objects_empty_in_sample: nestedObjects.filter((o) => o.sample_record_count === 0).length,
  },
  coverage: {
    drs_objects_not_in_sample_export: inDRSNotExport,
    sample_objects_not_in_drs_table: inExportNotDRS,
    lookup_reference_tables: lookupTables,
    notes: [
      "'patients' is the top-level record, not a nested object",
      "Lookup/reference tables (e.g. apt_types, body_part_types) may be included inline rather than as separate nested arrays",
      "Some escript_* tables lack descriptions in the DRS table",
      "Objects without descriptions: " +
        drsObjects
          .filter((o) => !o.description)
          .map((o) => o.object_name)
          .join(", "),
    ],
  },
  parse_failures: [],
};

console.log(`\nExtraction report:`);
console.log(`  DRS objects: ${report.parsing_results.drs_objects_in_table}`);
console.log(`  With descriptions: ${report.parsing_results.drs_objects_with_description}`);
console.log(`  Without descriptions: ${report.parsing_results.drs_objects_without_description}`);
console.log(`  Patient scalar fields: ${report.parsing_results.patient_scalar_fields}`);
console.log(`  Nested objects: ${report.parsing_results.nested_objects_in_sample}`);
console.log(`  Objects in DRS table not in sample: ${inDRSNotExport.length}`);
console.log(`  Objects in sample not in DRS table: ${inExportNotDRS.length}`);

writeFileSync(
  join(BASE, "extraction-report.json"),
  JSON.stringify(report, null, 2)
);

console.log("\nDone. Output files:");
console.log("  - drs-data-dictionary.json");
console.log("  - export-schema.json");
console.log("  - extraction-report.json");
