#!/usr/bin/env bun
/**
 * Extracts EHI export data mappings from the Hospital EHI Export Guide HTML page.
 * Parses the resource mapping table and CapabilityStatement JSON.
 */

import { readFileSync, writeFileSync, readdirSync } from "fs";
import { join, dirname } from "path";

const baseDir = dirname(import.meta.dir);
const enrichmentDir = import.meta.dir;

// --- Parse hospital_export.html for resource mappings ---
const exportHtml = readFileSync(join(baseDir, "hospital_export.html"), "utf-8");

// Extract content div
const contentMatch = exportHtml.match(/<div id="content"[^>]*>([\s\S]*?)<\/div>\s*<script/);
if (!contentMatch) throw new Error("Could not find content div in hospital_export.html");

const content = contentMatch[1];

// Parse the mapping table rows
const rowRegex = /<div class="row[^"]*">\s*<div[^>]*>(.*?)<\/div>\s*<div[^>]*>(.*?)<\/div>\s*<div[^>]*>(.*?)<\/div>\s*<\/div>/g;
const mappings: Array<{
  ehr_concept: string;
  fhir_resource: string;
  notes: string;
}> = [];

let match;
while ((match = rowRegex.exec(content)) !== null) {
  const concept = match[1].replace(/<[^>]+>/g, "").trim();
  const resource = match[2].replace(/<[^>]+>/g, "").trim();
  const notes = match[3].replace(/<[^>]+>/g, "").trim();

  // Skip header row
  if (concept === "EHR Concept" || concept === "Platform") continue;

  if (concept && resource) {
    mappings.push({
      ehr_concept: concept,
      fhir_resource: resource,
      notes: notes || "",
    });
  }
}

// --- Parse CapabilityStatement ---
const csJson = JSON.parse(
  readFileSync(join(baseDir, "capability-statement-hospital.json"), "utf-8")
);

const rest = csJson.rest?.[0] || {};
const resources = (rest.resource || []).map((r: any) => ({
  type: r.type,
  interactions: (r.interaction || []).map((i: any) => i.code),
  operations: (r.operation || []).map((o: any) => o.name),
  searchParams: (r.searchParam || []).map((s: any) => ({
    name: s.name,
    type: s.type,
  })),
}));

// --- Inventory all downloaded files ---
const allFiles = readdirSync(baseDir);
const inventory = {
  total_files: allFiles.length,
  html_pages: allFiles.filter((f) => f.endsWith(".html")),
  json_files: allFiles.filter((f) => f.endsWith(".json")),
  screenshots: allFiles.filter((f) => f.endsWith(".png")),
  other: allFiles.filter(
    (f) =>
      !f.endsWith(".html") &&
      !f.endsWith(".json") &&
      !f.endsWith(".png") &&
      f !== "enrichment"
  ),
};

// --- Build output ---
const output = {
  extraction_date: new Date().toISOString(),
  source: "https://dev.azaleahealth.com/hospital/export",
  product: "ChartAccess (Azalea Hospital)",
  chpl_id: 11140,

  export_format: {
    format: "NDJSON (Newline Delimited JSON)",
    standard: "HL7 FHIR R4",
    file_naming: "{resource}_{identifier}.ndjson",
    scope: "Patient compartment + Location, Practitioner, Binary",
    unstructured_data:
      "Binary resources with base64-encoded content; DocumentReference may contain inline base64 data",
  },

  ehr_to_fhir_mappings: mappings,

  capability_statement: {
    fhir_version: csJson.fhirVersion,
    software: csJson.software,
    supported_resources: resources,
    total_resource_types: resources.length,
    instantiates: csJson.instantiates,
    bulk_export_operation:
      "Patient/$export (export-resource operation on Patient)",
  },

  coverage_analysis: {
    mapped_ehr_concepts: mappings.length,
    fhir_resource_types_in_cs: resources.length,
    unique_fhir_resources_in_mappings: [
      ...new Set(mappings.map((m) => m.fhir_resource)),
    ],
    resources_in_mappings_not_in_cs: [
      ...new Set(mappings.map((m) => m.fhir_resource)),
    ].filter((r) => !resources.find((res: any) => res.type === r)),
    resources_in_cs_not_in_mappings: resources
      .map((r: any) => r.type)
      .filter(
        (t: string) =>
          !mappings.find((m) => m.fhir_resource === t) &&
          !["CapabilityStatement", "StructureDefinition", "Provenance"].includes(t)
      ),
  },

  file_inventory: inventory,

  parse_results: {
    total_files_discovered: allFiles.length,
    total_files_parsed: 2, // hospital_export.html + capability-statement
    parse_failures: [] as string[],
  },
};

writeFileSync(
  join(enrichmentDir, "export-mappings.json"),
  JSON.stringify(output, null, 2)
);

console.log(`Extracted ${mappings.length} EHR-to-FHIR mappings`);
console.log(
  `CapabilityStatement has ${resources.length} resource types`
);
console.log(`Output written to enrichment/export-mappings.json`);
