#!/usr/bin/env bun
/**
 * Extracts EHI export data mappings from Azalea Health's developer portal HTML pages.
 * Parses ambulatory and hospital export guides for EHR concept → FHIR resource mappings,
 * and extracts resource definitions from capability statements.
 */

import { readFileSync, writeFileSync, readdirSync } from "fs";
import { join } from "path";

const DOWNLOADS_DIR = join(import.meta.dir, "..");
const OUTPUT_DIR = import.meta.dir;

interface ExportMapping {
  ehrConcept: string;
  fhirResource: string;
  notes: string;
}

interface ResourceInfo {
  type: string;
  interactions: string[];
  operations: string[];
  searchParams: string[];
}

interface ParseResult {
  file: string;
  platform: string;
  mappings?: ExportMapping[];
  resources?: ResourceInfo[];
  error?: string;
}

function decodeHtml(s: string): string {
  return s.replace(/<[^>]*>/g, "").replace(/&quot;/g, '"').replace(/&amp;/g, "&").replace(/&lt;/g, "<").replace(/&gt;/g, ">").replace(/&#039;/g, "'").trim();
}

function extractExportMappings(html: string): ExportMapping[] {
  const mappings: ExportMapping[] = [];
  // Azalea uses Bootstrap grid divs: col-md-2 (concept), col-md-4 (resource), col-md-6 (notes)
  // Each row is a parent div containing these three children
  const rowRegex = /<div[^>]*class="[^"]*col-md-2[^"]*"[^>]*>(.*?)<\/div>\s*<div[^>]*class="[^"]*col-md-4[^"]*"[^>]*>(.*?)<\/div>\s*<div[^>]*class="[^"]*col-md-6[^"]*"[^>]*>(.*?)<\/div>/gis;
  let match;
  while ((match = rowRegex.exec(html)) !== null) {
    const concept = decodeHtml(match[1]);
    const resource = decodeHtml(match[2]);
    const notes = decodeHtml(match[3]);
    if (concept && resource && concept !== "EHR Concept") {
      mappings.push({ ehrConcept: concept, fhirResource: resource, notes });
    }
  }
  return mappings;
}

function extractCapabilityResources(jsonPath: string): ResourceInfo[] {
  try {
    const cs = JSON.parse(readFileSync(jsonPath, "utf-8"));
    const resources = cs.rest?.[0]?.resource ?? [];
    return resources.map((r: any) => ({
      type: r.type,
      interactions: (r.interaction ?? []).map((i: any) => i.code),
      operations: (r.operation ?? []).map((o: any) => o.name),
      searchParams: (r.searchParam ?? []).map((s: any) => s.name),
    }));
  } catch (e: any) {
    return [];
  }
}

const results: ParseResult[] = [];
const errors: { file: string; error: string }[] = [];

// Parse export guide HTMLs
const exportFiles = [
  { file: "ambulatory-export.html", platform: "Ambulatory" },
  { file: "hospital-export.html", platform: "Hospital" },
];

for (const { file, platform } of exportFiles) {
  const path = join(DOWNLOADS_DIR, file);
  try {
    const html = readFileSync(path, "utf-8");
    const mappings = extractExportMappings(html);
    results.push({ file, platform, mappings });
  } catch (e: any) {
    errors.push({ file, error: e.message });
    results.push({ file, platform, error: e.message });
  }
}

// Parse capability statements
const csFiles = [
  { file: "ambulatory-capability-statement.json", platform: "Ambulatory" },
  { file: "hospital-capability-statement.json", platform: "Hospital" },
];

for (const { file, platform } of csFiles) {
  const path = join(DOWNLOADS_DIR, file);
  try {
    const resources = extractCapabilityResources(path);
    results.push({ file, platform, resources });
  } catch (e: any) {
    errors.push({ file, error: e.message });
  }
}

// Parse all HTML files for additional content
const allHtmlFiles = readdirSync(DOWNLOADS_DIR).filter(f => f.endsWith(".html"));

// Output
const output = {
  extractedAt: new Date().toISOString(),
  summary: {
    totalFilesDiscovered: allHtmlFiles.length + csFiles.length,
    totalFilesParsed: results.filter(r => !r.error).length,
    parseFailures: errors,
  },
  ambulatoryExportMappings: results.find(r => r.file === "ambulatory-export.html")?.mappings ?? [],
  hospitalExportMappings: results.find(r => r.file === "hospital-export.html")?.mappings ?? [],
  ambulatoryCapabilityResources: results.find(r => r.file === "ambulatory-capability-statement.json")?.resources ?? [],
  hospitalCapabilityResources: results.find(r => r.file === "hospital-capability-statement.json")?.resources ?? [],
  fileInventory: allHtmlFiles.map(f => ({
    file: f,
    sizeBytes: readFileSync(join(DOWNLOADS_DIR, f)).length,
  })),
};

writeFileSync(join(OUTPUT_DIR, "export-mappings.json"), JSON.stringify(output, null, 2));
console.log(`Extracted ${output.ambulatoryExportMappings.length} ambulatory mappings`);
console.log(`Extracted ${output.hospitalExportMappings.length} hospital mappings`);
console.log(`Extracted ${output.ambulatoryCapabilityResources.length} ambulatory resources`);
console.log(`Extracted ${output.hospitalCapabilityResources.length} hospital resources`);
console.log(`Parse failures: ${errors.length}`);
console.log(`Output: enrichment/export-mappings.json`);
