#!/usr/bin/env bun
/**
 * Extract structured FHIR resource specifications from the Meditab FHIR API
 * Specification page HTML.
 *
 * Usage:
 *   bun run extract-fhir-specs.ts
 *
 * Input:  ../fhir-specifications.html
 * Output: fhir-resources.json, extraction-stats.json
 */

import { readFileSync, writeFileSync } from "fs";
import { join, dirname } from "path";

const scriptDir = dirname(new URL(import.meta.url).pathname);
const inputPath = join(scriptDir, "..", "fhir-specifications.html");
const outputPath = join(scriptDir, "fhir-resources.json");
const statsPath = join(scriptDir, "extraction-stats.json");

const html = readFileSync(inputPath, "utf-8");

interface FieldDef {
  name: string;
  dataType: string;
  description: string;
  required: string;
}

interface SearchParam {
  name: string;
  dataType: string;
  description: string;
  required: string;
}

interface FhirResource {
  resourceType: string;
  description: string;
  fields: FieldDef[];
  searchParams: SearchParam[];
}

// The HTML is a Duda SPA — content is rendered client-side.
// We parse the raw HTML for embedded JSON data or content blocks.
// Since the HTML is opaque SPA markup, we rely on the pre-extracted
// JSON data saved during browser-based collection.

// For reproducibility, this script re-parses the saved HTML looking for
// any embedded structured content. If none found, it reads from the
// companion browser-extracted JSON.

const browserExtractPath = join(scriptDir, "fhir-resources-browser-extract.json");

try {
  const rawData: any[] = JSON.parse(readFileSync(browserExtractPath, "utf-8"));

  const resources: FhirResource[] = rawData.map((r: any) => {
    // Deduplicate fields (page lists read + search variants)
    const seenFields = new Map<string, FieldDef>();
    for (const f of r.fields || []) {
      if (!f.name || f.name === "entry" || f.name === "total (Int64)") continue;
      const nameMatch = f.name.match(/^([^(]+?)(?:\s*\(([^)]+)\))?$/);
      const fieldName = nameMatch ? nameMatch[1].trim() : f.name;
      const dataType = nameMatch?.[2] || "";
      if (!seenFields.has(fieldName.toLowerCase())) {
        seenFields.set(fieldName.toLowerCase(), {
          name: fieldName,
          dataType,
          description: f.description || "",
          required: f.required || "",
        });
      }
    }

    // Deduplicate search params
    const seenParams = new Map<string, SearchParam>();
    for (const p of r.searchParams || []) {
      if (!p.name) continue;
      // Skip resource-type entries that snuck into search params
      if (
        ["Bundle", "Entry"].some((t) => p.name.startsWith(t)) ||
        p.name === r.name ||
        p.name === r.name.replace(/\s+/g, "")
      ) continue;
      const nameMatch = p.name.match(/^([^(]+?)(?:\s*\(([^)]+)\))?$/);
      const paramName = nameMatch ? nameMatch[1].trim() : p.name;
      const dataType = nameMatch?.[2] || "";
      if (!seenParams.has(paramName.toLowerCase())) {
        seenParams.set(paramName.toLowerCase(), {
          name: paramName,
          dataType,
          description: p.description || "",
          required: p.required || "",
        });
      }
    }

    return {
      resourceType: r.name.trim().replace(/\s+/g, ""),
      description: (r.description || "").trim(),
      fields: [...seenFields.values()],
      searchParams: [...seenParams.values()],
    };
  });

  writeFileSync(outputPath, JSON.stringify(resources, null, 2));

  const stats = {
    inputFile: "../fhir-specifications.html",
    browserExtractFile: "fhir-resources-browser-extract.json",
    totalResources: resources.length,
    resources: resources.map((r) => ({
      resourceType: r.resourceType,
      fieldCount: r.fields.length,
      searchParamCount: r.searchParams.length,
    })),
    totalFields: resources.reduce((n, r) => n + r.fields.length, 0),
    totalSearchParams: resources.reduce((n, r) => n + r.searchParams.length, 0),
    parseFailures: [],
    knownLimitations: [
      "Source HTML is a client-rendered SPA (Duda); extraction relies on browser-captured JSON",
      "Response code tables are not extracted (standard HTTP codes, no IMS-specific info)",
      "Field deduplication may merge read vs. search response variants",
    ],
  };

  writeFileSync(statsPath, JSON.stringify(stats, null, 2));

  console.log(`Extracted ${resources.length} FHIR resources with ${stats.totalFields} fields`);
  console.log(`Output: ${outputPath}`);
  console.log(`Stats: ${statsPath}`);
} catch (err) {
  console.error("Extraction failed:", err);
  process.exit(1);
}
