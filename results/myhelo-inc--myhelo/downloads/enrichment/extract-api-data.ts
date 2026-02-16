#!/usr/bin/env bun
/**
 * extract-api-data.ts
 *
 * Parses the myhELO FHIR well-known config and CapabilityStatement
 * to produce a queryable JSON summary of the EHI export data dictionary.
 *
 * Input files:
 *   ../fhir-well-known.json   - API spec with example responses
 *   ../fhir-metadata.json     - FHIR CapabilityStatement
 *   ../api-docs.html          - Rendered API documentation page
 *
 * Output:
 *   ./ehi-export-data-dictionary.json
 *   ./extraction-report.json
 */

import { readFileSync, writeFileSync, existsSync } from "fs";
import { join, dirname } from "path";

const baseDir = dirname(import.meta.path);
const downloadsDir = join(baseDir, "..");

interface FieldDefinition {
  name: string;
  type: string;
  cardinality: string;
  description: string;
  isModifier: boolean;
  isSummary: boolean;
  isUSCDI: boolean;
  binding?: {
    name: string;
    url: string;
    strength: string;
  };
}

interface ResourceDefinition {
  resourceType: string;
  description: string;
  profiles: { name: string; url: string }[];
  fields: FieldDefinition[];
  apiEndpoints: {
    read?: string;
    search?: string;
    export?: string;
  };
  searchParams: { name: string; type: string; required: boolean }[];
  exampleResponse?: object;
}

interface DataDictionary {
  vendor: string;
  product: string;
  fhirVersion: string;
  exportFormat: string;
  baseUrl: string;
  collectionDate: string;
  resources: ResourceDefinition[];
  summary: {
    totalResources: number;
    totalFields: number;
    uscdiFields: number;
    resourcesWithExamples: number;
  };
}

// Parse the CapabilityStatement
function parseCapabilityStatement(path: string) {
  if (!existsSync(path)) return null;
  const raw = readFileSync(path, "utf-8");
  return JSON.parse(raw);
}

// Parse the well-known JSON (API spec with examples)
function parseWellKnown(path: string) {
  if (!existsSync(path)) return null;
  const raw = readFileSync(path, "utf-8");
  return JSON.parse(raw);
}

// Parse API docs HTML for search parameters
function parseApiDocsHtml(path: string): Map<string, { searchParams: { name: string; type: string; required: boolean }[]; exampleResponse?: object }> {
  const result = new Map();
  if (!existsSync(path)) return result;

  const html = readFileSync(path, "utf-8");

  // Extract resource sections using regex on rendered HTML
  // Each resource has h2 heading, then read/search/export sections with h3
  const resourcePattern = /<h2[^>]*>(.*?)<\/h2>/g;
  let match;
  const resourceNames: string[] = [];

  while ((match = resourcePattern.exec(html)) !== null) {
    const name = match[1].replace(/<[^>]*>/g, '').trim();
    if (name !== 'PRODUCT' && name !== 'COMPANY') {
      resourceNames.push(name);
    }
  }

  return result;
}

// Main extraction
function main() {
  const capPath = join(downloadsDir, "fhir-metadata.json");
  const wellKnownPath = join(downloadsDir, "fhir-well-known.json");
  const apiDocsPath = join(downloadsDir, "api-docs.html");

  const cap = parseCapabilityStatement(capPath);
  const wellKnown = parseWellKnown(wellKnownPath);

  const errors: string[] = [];
  const resources: ResourceDefinition[] = [];

  // Extract from CapabilityStatement
  if (cap && cap.rest) {
    for (const rest of cap.rest) {
      for (const res of rest.resource || []) {
        const resourceDef: ResourceDefinition = {
          resourceType: res.type,
          description: "",
          profiles: [],
          fields: [],
          apiEndpoints: {},
          searchParams: [],
        };

        // Extract interactions
        for (const interaction of res.interaction || []) {
          if (interaction.code === "read") {
            resourceDef.apiEndpoints.read = `GET /${res.type}/:id`;
          }
          if (interaction.code === "search-type") {
            resourceDef.apiEndpoints.search = `GET /${res.type}?:parameters`;
          }
        }

        // Extract search params
        for (const sp of res.searchParam || []) {
          resourceDef.searchParams.push({
            name: sp.name,
            type: sp.type || "string",
            required: false, // CapabilityStatement doesn't indicate required
          });
        }

        resources.push(resourceDef);
      }
    }
  }

  // Enrich from well-known JSON (example responses and search params)
  if (wellKnown) {
    for (const [displayName, resourceData] of Object.entries(wellKnown as Record<string, any>)) {
      // Map display names to FHIR resource types
      const typeMap: Record<string, string> = {
        "Allergy Intolerance": "AllergyIntolerance",
        "Care Plan": "CarePlan",
        "Care Team": "CareTeam",
        "Condition": "Condition",
        "Device": "Device",
        "Diagnostic Report": "DiagnosticReport",
        "Document Reference": "DocumentReference",
        "Encounter": "Encounter",
        "Goal": "Goal",
        "Group": "Group",
        "Immunization": "Immunization",
        "Location": "Location",
        "Medication Request": "MedicationRequest",
        "Observation": "Observation",
        "Organization": "Organization",
        "Patient": "Patient",
        "Practitioner": "Practitioner",
        "Procedure": "Procedure",
        "Provenance": "Provenance",
      };

      const fhirType = typeMap[displayName] || displayName;
      let existing = resources.find(r => r.resourceType === fhirType);

      if (!existing) {
        existing = {
          resourceType: fhirType,
          description: "",
          profiles: [],
          fields: [],
          apiEndpoints: {},
          searchParams: [],
        };
        resources.push(existing);
      }

      // Extract example responses
      if (resourceData.read?.response) {
        existing.exampleResponse = resourceData.read.response;
        existing.apiEndpoints.read = `${resourceData.read.method} /${fhirType}/:id`;

        // Extract fields from example response
        extractFieldsFromExample(existing, resourceData.read.response, fhirType);
      }

      if (resourceData.search) {
        existing.apiEndpoints.search = `${resourceData.search.method} /${fhirType}?:parameters`;

        // Extract search parameters
        if (resourceData.search.parameters) {
          for (const [paramName, paramData] of Object.entries(resourceData.search.parameters as Record<string, any>)) {
            const existingParam = existing.searchParams.find(p => p.name === paramName);
            if (existingParam) {
              existingParam.type = paramData.type || existingParam.type;
              existingParam.required = paramData.required === true || paramData.required === "true";
            } else {
              existing.searchParams.push({
                name: paramName,
                type: paramData.type || "string",
                required: paramData.required === true || paramData.required === "true",
              });
            }
          }
        }
      }

      if (resourceData.export) {
        existing.apiEndpoints.export = `${resourceData.export.method} /${fhirType}/:id/$export`;
      }
    }
  }

  // Build summary
  let totalFields = 0;
  let uscdiFields = 0;
  let resourcesWithExamples = 0;

  for (const res of resources) {
    totalFields += res.fields.length;
    uscdiFields += res.fields.filter(f => f.isUSCDI).length;
    if (res.exampleResponse) resourcesWithExamples++;
  }

  const dataDictionary: DataDictionary = {
    vendor: "myhELO, Inc.",
    product: "myhELO",
    fhirVersion: cap?.fhirVersion || "4.0.1",
    exportFormat: "FHIR R4 JSON",
    baseUrl: cap?.implementation?.url || "https://provider.myhelo.com/fhir",
    collectionDate: new Date().toISOString().split("T")[0],
    resources: resources.sort((a, b) => a.resourceType.localeCompare(b.resourceType)),
    summary: {
      totalResources: resources.length,
      totalFields: totalFields,
      uscdiFields: uscdiFields,
      resourcesWithExamples: resourcesWithExamples,
    },
  };

  // Write output
  const outPath = join(baseDir, "ehi-export-data-dictionary.json");
  writeFileSync(outPath, JSON.stringify(dataDictionary, null, 2));
  console.log(`Wrote data dictionary: ${outPath}`);
  console.log(`  Resources: ${dataDictionary.summary.totalResources}`);
  console.log(`  Fields extracted from examples: ${dataDictionary.summary.totalFields}`);
  console.log(`  Resources with examples: ${dataDictionary.summary.resourcesWithExamples}`);

  // Write extraction report
  const report = {
    inputFiles: {
      capabilityStatement: { path: capPath, exists: existsSync(capPath), size: existsSync(capPath) ? readFileSync(capPath).length : 0 },
      wellKnown: { path: wellKnownPath, exists: existsSync(wellKnownPath), size: existsSync(wellKnownPath) ? readFileSync(wellKnownPath).length : 0 },
      apiDocs: { path: apiDocsPath, exists: existsSync(apiDocsPath), size: existsSync(apiDocsPath) ? readFileSync(apiDocsPath).length : 0 },
    },
    outputFiles: [outPath],
    totalResourcesParsed: resources.length,
    parseFailures: errors,
    resourceList: resources.map(r => ({
      type: r.resourceType,
      fieldsFromExample: r.fields.length,
      hasExample: !!r.exampleResponse,
      searchParams: r.searchParams.length,
      endpoints: Object.keys(r.apiEndpoints),
    })),
  };

  const reportPath = join(baseDir, "extraction-report.json");
  writeFileSync(reportPath, JSON.stringify(report, null, 2));
  console.log(`Wrote extraction report: ${reportPath}`);
}

function extractFieldsFromExample(resource: ResourceDefinition, example: any, prefix: string, depth = 0) {
  if (!example || typeof example !== "object" || depth > 3) return;

  for (const [key, value] of Object.entries(example)) {
    if (key === "resourceType") continue;

    const fieldName = depth === 0 ? `${prefix}.${key}` : key;
    let type = "unknown";
    let isUSCDI = false;

    if (typeof value === "string") type = "string";
    else if (typeof value === "number") type = "number";
    else if (typeof value === "boolean") type = "boolean";
    else if (Array.isArray(value)) {
      type = "array";
      // Check first element
      if (value.length > 0 && typeof value[0] === "object") {
        if (value[0].coding) type = "CodeableConcept[]";
        else if (value[0].reference) type = "Reference[]";
        else type = "BackboneElement[]";
      }
    } else if (typeof value === "object") {
      if ((value as any).coding) type = "CodeableConcept";
      else if ((value as any).reference) type = "Reference";
      else type = "object";
    }

    // Known USCDI elements
    const uscdiElements = [
      "clinicalStatus", "verificationStatus", "code", "patient", "subject",
      "status", "intent", "category", "text", "name", "birthDate", "gender",
      "address", "telecom", "identifier", "vaccineCode", "occurrenceDateTime",
      "medicationCodeableConcept", "dosageInstruction", "reaction",
    ];
    if (uscdiElements.includes(key)) isUSCDI = true;

    resource.fields.push({
      name: fieldName,
      type,
      cardinality: Array.isArray(value) ? "0..*" : "0..1",
      description: "",
      isModifier: false,
      isSummary: false,
      isUSCDI,
    });
  }
}

main();
