#!/usr/bin/env bun
/**
 * Parses the Sevocity FHIR API OpenAPI spec (multi-file YAML)
 * and extracts structured JSON with resource schemas, fields,
 * API endpoints, and examples.
 */

import { readFileSync, readdirSync, writeFileSync, existsSync } from "fs";
import { join, basename, relative } from "path";
import { parse as parseYaml } from "yaml";

const BASE_DIR = join(import.meta.dir, "..", "fhir-api-docs");
const OUTPUT_DIR = import.meta.dir;

interface FieldInfo {
  name: string;
  type: string;
  isArray: boolean;
  children?: FieldInfo[];
}

interface ResourceSchema {
  resourceType: string;
  schemaFile: string;
  variant: "read" | "search";
  fields: FieldInfo[];
  fieldCount: number;
}

interface ApiEndpoint {
  path: string;
  method: string;
  resourceType: string;
  summary?: string;
  description?: string;
  parameters: { name: string; in: string; description?: string; required?: boolean }[];
  isCertified: boolean; // marked with * in the spec
  pathFile: string;
}

interface ExampleData {
  resourceType: string;
  exampleFile: string;
  content: unknown;
}

interface EnrichmentOutput {
  extractionDate: string;
  sourceSpec: string;
  specTitle: string;
  specDescription: string;
  servers: { url: string; description: string }[];
  resources: ResourceSchema[];
  endpoints: ApiEndpoint[];
  examples: ExampleData[];
  coverage: {
    totalSchemaFiles: number;
    totalPathFiles: number;
    totalExampleFiles: number;
    parsedSchemaFiles: number;
    parsedPathFiles: number;
    parsedExampleFiles: number;
    parseFailures: { file: string; error: string }[];
  };
}

function parseYamlFile(filePath: string): unknown {
  const content = readFileSync(filePath, "utf-8");
  return parseYaml(content);
}

function extractFields(schema: any, depth = 0): FieldInfo[] {
  if (!schema || !schema.properties) return [];
  const fields: FieldInfo[] = [];
  for (const [name, prop] of Object.entries(schema.properties) as [string, any][]) {
    const isArray = prop.type === "array";
    const innerSchema = isArray ? prop.items : prop;
    const fieldType = isArray
      ? `array<${innerSchema?.type || "unknown"}>`
      : prop.type || "unknown";
    const field: FieldInfo = { name, type: fieldType, isArray };
    if (depth < 4 && innerSchema?.properties) {
      field.children = extractFields(innerSchema, depth + 1);
    }
    fields.push(field);
  }
  return fields;
}

function countFields(fields: FieldInfo[]): number {
  let count = 0;
  for (const f of fields) {
    count++;
    if (f.children) count += countFields(f.children);
  }
  return count;
}

function inferResourceType(filename: string): string {
  let name = basename(filename, ".yml").replace(/\.YML$/i, "");
  name = name.replace(/^(READ|SEARCH|Search)/, "");
  // Handle plurals
  if (name === "DEVICES") name = "Device";
  if (name === "GOALS") name = "Goal";
  if (name === "ALLENDPOINTS") name = "Endpoint";
  return name.charAt(0).toUpperCase() + name.slice(1).replace(/([A-Z]+)/g, (m) => m);
}

function inferVariant(filename: string): "read" | "search" {
  const name = basename(filename).toUpperCase();
  return name.startsWith("SEARCH") ? "search" : "read";
}

// Main extraction
const output: EnrichmentOutput = {
  extractionDate: new Date().toISOString(),
  sourceSpec: "https://fhirapi-docs.sevocity.com/openAPIDocs.yml",
  specTitle: "",
  specDescription: "",
  servers: [],
  resources: [],
  endpoints: [],
  examples: [],
  coverage: {
    totalSchemaFiles: 0,
    totalPathFiles: 0,
    totalExampleFiles: 0,
    parsedSchemaFiles: 0,
    parsedPathFiles: 0,
    parsedExampleFiles: 0,
    parseFailures: [],
  },
};

// Parse main spec
try {
  const mainSpec = parseYamlFile(join(BASE_DIR, "..", "openAPIDocs.yml")) as any;
  output.specTitle = mainSpec.info?.title || "";
  output.specDescription = mainSpec.info?.description || "";
  output.servers = (mainSpec.servers || []).map((s: any) => ({
    url: s.url,
    description: s.description,
  }));

  // Extract certified resource types from tags
  const certifiedResources = new Set<string>();
  for (const tag of mainSpec.tags || []) {
    if (tag.description?.includes("*")) {
      certifiedResources.add(tag.name);
    }
  }

  // Parse schema files
  const schemasDir = join(BASE_DIR, "components", "schemas");
  if (existsSync(schemasDir)) {
    const schemaFiles = readdirSync(schemasDir).filter(
      (f) => f.endsWith(".yml") || f.endsWith(".YML")
    );
    output.coverage.totalSchemaFiles = schemaFiles.length;

    for (const file of schemaFiles) {
      try {
        const schema = parseYamlFile(join(schemasDir, file)) as any;
        const resourceType = inferResourceType(file);
        const variant = inferVariant(file);
        const fields = extractFields(schema);
        output.resources.push({
          resourceType,
          schemaFile: `components/schemas/${file}`,
          variant,
          fields,
          fieldCount: countFields(fields),
        });
        output.coverage.parsedSchemaFiles++;
      } catch (e: any) {
        output.coverage.parseFailures.push({
          file: `components/schemas/${file}`,
          error: e.message,
        });
      }
    }
  }

  // Parse path files
  const pathsDir = join(BASE_DIR, "paths");
  if (existsSync(pathsDir)) {
    const pathFiles = readdirSync(pathsDir).filter((f) => f.endsWith(".yml"));
    output.coverage.totalPathFiles = pathFiles.length;

    for (const file of pathFiles) {
      try {
        const pathData = parseYamlFile(join(pathsDir, file)) as any;
        for (const [method, details] of Object.entries(pathData) as [string, any][]) {
          if (!details || typeof details !== "object") continue;
          const tags = details.tags || [];
          const resourceType = tags[0] || inferResourceType(file);
          const params = (details.parameters || [])
            .filter((p: any) => p && !p.$ref)
            .map((p: any) => ({
              name: p.name,
              in: p.in,
              description: p.description,
              required: p.required,
            }));
          output.endpoints.push({
            path: file.replace(/_id/g, "/{id}").replace(/_export/, "/$export").replace(".yml", ""),
            method: method.toUpperCase(),
            resourceType,
            summary: details.summary,
            description: details.description,
            parameters: params,
            isCertified: certifiedResources.has(resourceType),
            pathFile: `paths/${file}`,
          });
        }
        output.coverage.parsedPathFiles++;
      } catch (e: any) {
        output.coverage.parseFailures.push({
          file: `paths/${file}`,
          error: e.message,
        });
      }
    }
  }

  // Parse example files
  const examplesDir = join(BASE_DIR, "examples");
  if (existsSync(examplesDir)) {
    const exampleFiles = readdirSync(examplesDir).filter(
      (f) => f.endsWith(".yml") || f.endsWith(".YML")
    );
    output.coverage.totalExampleFiles = exampleFiles.length;

    for (const file of exampleFiles) {
      try {
        const example = parseYamlFile(join(examplesDir, file)) as any;
        const content = example?.value || example;
        const rt =
          content?.resourceType ||
          content?.resource?.resourceType ||
          inferResourceType(file);
        output.examples.push({
          resourceType: rt,
          exampleFile: `examples/${file}`,
          content,
        });
        output.coverage.parsedExampleFiles++;
      } catch (e: any) {
        output.coverage.parseFailures.push({
          file: `examples/${file}`,
          error: e.message,
        });
      }
    }
  }
} catch (e: any) {
  console.error("Failed to parse main spec:", e.message);
  process.exit(1);
}

// Write output
writeFileSync(
  join(OUTPUT_DIR, "sevocity-fhir-api-extracted.json"),
  JSON.stringify(output, null, 2)
);

// Summary
console.log("Extraction complete:");
console.log(`  Resources: ${output.resources.length} schemas`);
console.log(`  Endpoints: ${output.endpoints.length} API operations`);
console.log(`  Examples: ${output.examples.length} example files`);
console.log(
  `  Schema files: ${output.coverage.parsedSchemaFiles}/${output.coverage.totalSchemaFiles}`
);
console.log(
  `  Path files: ${output.coverage.parsedPathFiles}/${output.coverage.totalPathFiles}`
);
console.log(
  `  Example files: ${output.coverage.parsedExampleFiles}/${output.coverage.totalExampleFiles}`
);
console.log(`  Parse failures: ${output.coverage.parseFailures.length}`);
if (output.coverage.parseFailures.length > 0) {
  for (const f of output.coverage.parseFailures) {
    console.log(`    - ${f.file}: ${f.error}`);
  }
}
