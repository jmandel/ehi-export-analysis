#!/usr/bin/env bun
/**
 * extract-structure-defs.ts
 *
 * Parses the extracted FHIR StructureDefinitions from the myhELO EHI export
 * documentation and produces a comprehensive field-level data dictionary.
 *
 * Input:
 *   ../structure-definitions.json  — StructureDefinitions extracted from the SPA JS bundle
 *   ../dataset-summaries.json      — Dataset overview/summary metadata
 *   ../fhir-metadata.json          — FHIR CapabilityStatement
 *   ../fhir-well-known.json        — API spec with example responses
 *
 * Output:
 *   ./ehi-export-full-dictionary.json  — Complete field-level data dictionary
 *   ./extraction-report-v2.json        — Accounting report
 */

import { readFileSync, writeFileSync, existsSync } from "fs";
import { join, dirname } from "path";

const baseDir = dirname(import.meta.path);
const downloadsDir = join(baseDir, "..");

interface ElementDefinition {
  path: string;
  short?: string;
  definition?: string;
  min: number;
  max: string;
  type?: string[];
  isModifier: boolean;
  isSummary: boolean;
  isUSCDI: boolean;
  binding?: {
    strength: string;
    valueSet?: string;
    description?: string;
  };
}

interface ResourceProfile {
  resourceType: string;
  profileId: string;
  profileUrl: string;
  title: string;
  brief: string;
  overview: string[];
  supportedProfiles: { name: string; url: string }[];
  elements: ElementDefinition[];
  elementCount: number;
}

interface FullDictionary {
  vendor: string;
  product: string;
  fhirVersion: string;
  exportFormat: string;
  baseUrl: string;
  collectionDate: string;
  exportDescription: string;
  resources: ResourceProfile[];
  summary: {
    totalResources: number;
    totalElements: number;
    uscdiElements: number;
    elementsWithBindings: number;
    requiredElements: number;
  };
}

function parseStructureDefinition(sd: any): ElementDefinition[] {
  const elements: ElementDefinition[] = [];

  if (!sd.snapshot?.element) return elements;

  for (const el of sd.snapshot.element) {
    // Skip the root element itself
    if (el.path === sd.type) continue;

    // Extract types
    const types: string[] = [];
    if (el.type) {
      for (const t of el.type) {
        types.push(t.code || "unknown");
      }
    }

    // Check if USCDI - look for "(USCDI)" in short or label
    const isUSCDI = !!(
      (el.short && el.short.includes("(USCDI)")) ||
      (el.label && el.label.includes("USCDI")) ||
      (el.mustSupport === true)
    );

    // Extract binding
    let binding: ElementDefinition["binding"];
    if (el.binding) {
      binding = {
        strength: el.binding.strength || "unknown",
        valueSet: el.binding.valueSet || undefined,
        description: el.binding.description || undefined,
      };
    }

    elements.push({
      path: el.path,
      short: el.short || undefined,
      definition: el.definition || undefined,
      min: el.min ?? 0,
      max: el.max || "*",
      type: types.length > 0 ? types : undefined,
      isModifier: el.isModifier === true,
      isSummary: el.isSummary === true,
      isUSCDI,
      binding,
    });
  }

  return elements;
}

function main() {
  const errors: string[] = [];

  // Load inputs
  const sdPath = join(downloadsDir, "structure-definitions.json");
  const summariesPath = join(downloadsDir, "dataset-summaries.json");
  const capPath = join(downloadsDir, "fhir-metadata.json");

  if (!existsSync(sdPath)) {
    console.error("ERROR: structure-definitions.json not found");
    process.exit(1);
  }

  const structureDefs: Record<string, any> = JSON.parse(readFileSync(sdPath, "utf-8"));
  const summaries: Record<string, any> = existsSync(summariesPath)
    ? JSON.parse(readFileSync(summariesPath, "utf-8"))
    : {};
  const cap = existsSync(capPath) ? JSON.parse(readFileSync(capPath, "utf-8")) : null;

  const resources: ResourceProfile[] = [];

  for (const [datasetName, sd] of Object.entries(structureDefs)) {
    const summary = summaries[datasetName] || {};

    try {
      const elements = parseStructureDefinition(sd);

      resources.push({
        resourceType: datasetName,
        profileId: sd.id || "",
        profileUrl: sd.url || "",
        title: summary.title || sd.title || datasetName,
        brief: summary.brief || sd.description || "",
        overview: summary.overview || [],
        supportedProfiles: summary.supported_profiles || [],
        elements,
        elementCount: elements.length,
      });
    } catch (e: any) {
      errors.push(`${datasetName}: ${e.message}`);
    }
  }

  // Build summary stats
  let totalElements = 0;
  let uscdiElements = 0;
  let elementsWithBindings = 0;
  let requiredElements = 0;

  for (const res of resources) {
    totalElements += res.elements.length;
    uscdiElements += res.elements.filter(e => e.isUSCDI).length;
    elementsWithBindings += res.elements.filter(e => !!e.binding).length;
    requiredElements += res.elements.filter(e => e.min > 0).length;
  }

  const dictionary: FullDictionary = {
    vendor: "myhELO, Inc.",
    product: "myhELO",
    fhirVersion: cap?.fhirVersion || "4.0.1",
    exportFormat: "FHIR R4 JSON",
    baseUrl: cap?.implementation?.url || "https://provider.myhelo.com/fhir",
    collectionDate: new Date().toISOString().split("T")[0],
    exportDescription: "The EHI Export for myhELO allows customers in the ambulatory setting to easily export clinical or healthcare data from patient records. The export format follows FHIR standards. Customers can choose to export all or selected myhELO EHI datasets for a single patient, multiple patients, or all patients in the practices.",
    resources: resources.sort((a, b) => a.resourceType.localeCompare(b.resourceType)),
    summary: {
      totalResources: resources.length,
      totalElements,
      uscdiElements,
      elementsWithBindings,
      requiredElements,
    },
  };

  // Write output
  const outPath = join(baseDir, "ehi-export-full-dictionary.json");
  writeFileSync(outPath, JSON.stringify(dictionary, null, 2));
  console.log(`Wrote full dictionary: ${outPath}`);
  console.log(`  Resources: ${dictionary.summary.totalResources}`);
  console.log(`  Total elements: ${dictionary.summary.totalElements}`);
  console.log(`  USCDI elements: ${dictionary.summary.uscdiElements}`);
  console.log(`  Elements with bindings: ${dictionary.summary.elementsWithBindings}`);
  console.log(`  Required elements: ${dictionary.summary.requiredElements}`);

  // Write extraction report
  const report = {
    inputFiles: {
      structureDefinitions: { path: sdPath, exists: true, size: readFileSync(sdPath).length },
      datasetSummaries: { path: summariesPath, exists: existsSync(summariesPath), size: existsSync(summariesPath) ? readFileSync(summariesPath).length : 0 },
      capabilityStatement: { path: capPath, exists: existsSync(capPath), size: existsSync(capPath) ? readFileSync(capPath).length : 0 },
    },
    outputFiles: [outPath],
    totalResourcesParsed: resources.length,
    parseFailures: errors,
    resourceList: resources.map(r => ({
      type: r.resourceType,
      profileId: r.profileId,
      elementCount: r.elementCount,
      uscdiElements: r.elements.filter(e => e.isUSCDI).length,
      requiredElements: r.elements.filter(e => e.min > 0).length,
      supportedProfiles: r.supportedProfiles.map(p => p.name),
    })),
  };

  const reportPath = join(baseDir, "extraction-report-v2.json");
  writeFileSync(reportPath, JSON.stringify(report, null, 2));
  console.log(`Wrote extraction report: ${reportPath}`);
}

main();
