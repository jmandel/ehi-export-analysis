#!/usr/bin/env bun
/**
 * Extracts structured schema information from the RevolutionEHR OpenAPI
 * EHI export data dictionary (openapiServices.json).
 *
 * Outputs:
 *   - schemas.json: All schemas with fields, types, descriptions, and relationships
 *   - coverage-accounting.json: Parse statistics
 */

import { readFileSync, writeFileSync } from "fs";
import { join, dirname } from "path";

const scriptDir = dirname(new URL(import.meta.url).pathname);
const inputPath = join(scriptDir, "..", "openapiServices.json");
const outputDir = scriptDir;

interface FieldInfo {
  name: string;
  type: string;
  format?: string;
  description: string;
  required: boolean;
  isArray: boolean;
  refSchema?: string;
  itemType?: string;
}

interface SchemaInfo {
  name: string;
  description: string;
  fieldCount: number;
  fields: FieldInfo[];
  referencedBy: string[];
  references: string[];
}

interface ExportStructure {
  title: string;
  description: string;
  exportEndpoint: string;
  exportMethod: string;
  rootSchema: string;
  schemas: SchemaInfo[];
  totalSchemas: number;
  totalFields: number;
  schemaRelationships: Array<{ from: string; to: string; field: string; isArray: boolean }>;
}

const raw = readFileSync(inputPath, "utf-8");
const spec = JSON.parse(raw);

const schemas = spec.components?.schemas ?? {};
const schemaNames = Object.keys(schemas);

// Track references
const referencedBy: Record<string, string[]> = {};
for (const name of schemaNames) referencedBy[name] = [];

const allSchemas: SchemaInfo[] = [];
const relationships: ExportStructure["schemaRelationships"] = [];
let totalFields = 0;

for (const [schemaName, schemaDef] of Object.entries(schemas) as [string, any][]) {
  const requiredFields = new Set(schemaDef.required ?? []);
  const properties = schemaDef.properties ?? {};
  const fields: FieldInfo[] = [];

  for (const [fieldName, fieldDef] of Object.entries(properties) as [string, any][]) {
    const isArray = fieldDef.type === "array";
    let type = fieldDef.type ?? "object";
    let format = fieldDef.format;
    let refSchema: string | undefined;
    let itemType: string | undefined;

    if (fieldDef.$ref) {
      refSchema = fieldDef.$ref.replace("#/components/schemas/", "");
      type = refSchema;
    } else if (isArray && fieldDef.items) {
      if (fieldDef.items.$ref) {
        refSchema = fieldDef.items.$ref.replace("#/components/schemas/", "");
        itemType = refSchema;
      } else {
        itemType = fieldDef.items.type ?? "unknown";
      }
    }

    if (refSchema) {
      relationships.push({
        from: schemaName,
        to: refSchema,
        field: fieldName,
        isArray,
      });
      if (referencedBy[refSchema]) {
        referencedBy[refSchema].push(schemaName);
      }
    }

    fields.push({
      name: fieldName,
      type,
      ...(format ? { format } : {}),
      description: fieldDef.description ?? "",
      required: requiredFields.has(fieldName),
      isArray,
      ...(refSchema ? { refSchema } : {}),
      ...(itemType ? { itemType } : {}),
    });
  }

  totalFields += fields.length;

  allSchemas.push({
    name: schemaName,
    description: schemaDef.description ?? "",
    fieldCount: fields.length,
    fields,
    referencedBy: [],
    references: [],
  });
}

// Fill in cross-references
for (const schema of allSchemas) {
  schema.referencedBy = referencedBy[schema.name] ?? [];
  schema.references = relationships
    .filter((r) => r.from === schema.name)
    .map((r) => r.to);
}

// Extract endpoint info
const paths = spec.paths ?? {};
const firstPath = Object.keys(paths)[0] ?? "";
const firstMethod = Object.keys(paths[firstPath] ?? {})[0] ?? "";

const exportStructure: ExportStructure = {
  title: spec.info?.title ?? "",
  description: (spec.info?.description ?? "").replace(/[#*]/g, "").trim(),
  exportEndpoint: firstPath,
  exportMethod: firstMethod.toUpperCase(),
  rootSchema: "Patient",
  schemas: allSchemas,
  totalSchemas: allSchemas.length,
  totalFields,
  schemaRelationships: relationships,
};

writeFileSync(
  join(outputDir, "schemas.json"),
  JSON.stringify(exportStructure, null, 2)
);

// Coverage accounting
const accounting = {
  inputFile: "../openapiServices.json",
  totalSchemasDiscovered: schemaNames.length,
  totalSchemasParsed: allSchemas.length,
  parseFailures: [] as Array<{ schema: string; error: string }>,
  totalFieldsExtracted: totalFields,
  schemaNames: schemaNames.sort(),
  rootSchemaFields: allSchemas
    .find((s) => s.name === "Patient")
    ?.fields.map((f) => ({
      name: f.name,
      type: f.isArray ? `${f.refSchema ?? f.itemType ?? f.type}[]` : f.type,
    })) ?? [],
};

writeFileSync(
  join(outputDir, "coverage-accounting.json"),
  JSON.stringify(accounting, null, 2)
);

console.log(`Extracted ${allSchemas.length} schemas with ${totalFields} total fields`);
console.log(`Relationships: ${relationships.length}`);
console.log(`Output: schemas.json, coverage-accounting.json`);
