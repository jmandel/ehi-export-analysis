#!/usr/bin/env bun
/**
 * Extracts FHIR JSON examples from the Althea EHI Documentation PDF.
 *
 * The PDF is structured as: section headings followed by FHIR JSON objects.
 * We extract the text with pdftotext, then parse out JSON blocks and their
 * associated section headings.
 *
 * Usage: bun run extract-fhir-examples.ts
 * Input: ../AltheaEHIDocumentation.pdf
 * Output: fhir-examples.json, extraction-summary.json
 */

import { $ } from "bun";

const PDF_PATH = new URL("../AltheaEHIDocumentation.pdf", import.meta.url).pathname;
const OUTPUT_DIR = new URL(".", import.meta.url).pathname;

// Known section headings in the PDF (in document order)
const SECTION_HEADINGS = [
  "Patient",
  "Allergies and Intolerances",
  "Care Plan",
  "Care Team",
  "Condition",
  "Health Concern",
  "Implantable Device",
  "Diagnostic Report",
  "Document Reference",
  "Goal",
  "Immunization",
  "Medication Request",
  "Smoking Status Observation",
  "Pediatric Weight for Height Observation Tests",
  "Laboratory Result Observation",
  "Pediatric BMI for Age Observation",
  "Pulse Oximetry Tests",
  "Pediatric Head Occipital-frontal Circumference Percentile",
  "Observation Body Height",
  "Observation Body Temperature",
  "Observation Blood Pressure",
  "Observation Body Weight",
  "Observation Heart Rate",
  "Observation Respiratory Rate",
  "Procedure",
  "Claims",
  "Coverage",
  "Explanation of Benefits",
];

interface FhirExample {
  section: string;
  resourceType: string;
  id: string | null;
  json: Record<string, unknown>;
}

interface ExtractionSummary {
  input_file: string;
  total_sections: number;
  total_examples_extracted: number;
  resource_type_counts: Record<string, number>;
  sections_with_examples: Array<{
    section: string;
    example_count: number;
    resource_types: string[];
  }>;
  parse_failures: Array<{ section: string; error: string }>;
}

async function main() {
  // Extract text from PDF, stripping form-feed (page break) characters
  const rawText = await $`pdftotext ${PDF_PATH} -`.text();
  const text = rawText.replace(/\f/g, "\n");

  // Strategy: find all JSON blocks in the entire document first,
  // then assign each to the nearest preceding section heading.

  // First, find all section heading positions in the text.
  // Skip the TOC by looking for the "Resources" section marker which comes
  // after the TOC and introduction.
  const resourcesMarker = "Below sections list the supported FHIR resources";
  const contentStart = text.indexOf(resourcesMarker);
  if (contentStart === -1) {
    console.error("Could not find content start marker");
    process.exit(1);
  }

  const contentText = text.slice(contentStart);

  // Find heading positions in the content area
  const headingPositions: Array<{ heading: string; position: number }> = [];

  for (const heading of SECTION_HEADINGS) {
    // Search for heading on its own line (to avoid matching substrings in JSON)
    const pattern = new RegExp(`(?:^|\\n)${escapeRegex(heading)}\\s*\\n`, "g");
    let match;
    while ((match = pattern.exec(contentText)) !== null) {
      headingPositions.push({
        heading,
        position: match.index,
      });
    }
  }

  // Also find the end marker
  const endMarker = "Export Current CCD";
  const endPos = contentText.indexOf(endMarker);

  // Sort by position
  headingPositions.sort((a, b) => a.position - b.position);

  // For each heading, extract text until the next heading (or end marker)
  const examples: FhirExample[] = [];
  const failures: Array<{ section: string; error: string }> = [];

  for (let i = 0; i < headingPositions.length; i++) {
    const { heading, position } = headingPositions[i];
    const nextPos = i + 1 < headingPositions.length
      ? headingPositions[i + 1].position
      : (endPos !== -1 ? endPos : contentText.length);

    const sectionText = contentText.slice(position, nextPos);

    // Extract all JSON blocks from this section
    const jsonBlocks = extractJsonBlocks(sectionText);

    let sectionExamples = 0;
    for (const block of jsonBlocks) {
      try {
        const parsed = JSON.parse(block);
        const extracted = extractResources(parsed, heading);
        for (const ex of extracted) {
          examples.push(ex);
          sectionExamples++;
        }
      } catch {
        // Skip unparseable blocks
      }
    }

    if (sectionExamples === 0) {
      failures.push({ section: heading, error: "No valid FHIR resources extracted" });
    }
  }

  // Deduplicate: same resourceType + id + section
  const seen = new Set<string>();
  const deduped: FhirExample[] = [];
  for (const ex of examples) {
    const key = `${ex.section}::${ex.resourceType}/${ex.id}`;
    if (!seen.has(key)) {
      seen.add(key);
      deduped.push(ex);
    }
  }

  // Build summary
  const resourceTypeCounts: Record<string, number> = {};
  for (const ex of deduped) {
    resourceTypeCounts[ex.resourceType] = (resourceTypeCounts[ex.resourceType] || 0) + 1;
  }

  const sectionSummaries = new Map<string, { count: number; types: Set<string> }>();
  for (const ex of deduped) {
    if (!sectionSummaries.has(ex.section)) {
      sectionSummaries.set(ex.section, { count: 0, types: new Set() });
    }
    const s = sectionSummaries.get(ex.section)!;
    s.count++;
    s.types.add(ex.resourceType);
  }

  const summary: ExtractionSummary = {
    input_file: PDF_PATH,
    total_sections: SECTION_HEADINGS.length,
    total_examples_extracted: deduped.length,
    resource_type_counts: resourceTypeCounts,
    sections_with_examples: Array.from(sectionSummaries.entries()).map(([section, data]) => ({
      section,
      example_count: data.count,
      resource_types: Array.from(data.types),
    })),
    parse_failures: failures,
  };

  // Write outputs
  await Bun.write(
    `${OUTPUT_DIR}/fhir-examples.json`,
    JSON.stringify(deduped, null, 2)
  );
  await Bun.write(
    `${OUTPUT_DIR}/extraction-summary.json`,
    JSON.stringify(summary, null, 2)
  );

  console.log(`Extracted ${deduped.length} FHIR examples across ${Object.keys(resourceTypeCounts).length} resource types`);
  console.log("Resource type counts:", JSON.stringify(resourceTypeCounts, null, 2));
  console.log(`Parse failures: ${failures.length}`);
  for (const f of failures) {
    console.log(`  - ${f.section}: ${f.error}`);
  }
}

/**
 * Extract FHIR resources from a parsed JSON object. Handles:
 * - Direct resources: { "resourceType": "Patient", ... }
 * - Bundle entries: { "resource": { "resourceType": ... } }
 * - Objects with link+resource (PDF format): { "link": [...], "resource": {...} }
 */
function extractResources(parsed: any, section: string): FhirExample[] {
  const results: FhirExample[] = [];

  if (parsed.resourceType) {
    // Direct resource
    results.push({
      section,
      resourceType: parsed.resourceType,
      id: parsed.id || null,
      json: parsed,
    });

    // Also check if it's a Bundle with entries
    if (parsed.entry && Array.isArray(parsed.entry)) {
      for (const entry of parsed.entry) {
        if (entry.resource?.resourceType) {
          results.push({
            section,
            resourceType: entry.resource.resourceType,
            id: entry.resource.id || null,
            json: entry.resource,
          });
        }
      }
    }
  } else if (parsed.resource?.resourceType) {
    // Bundle entry format
    results.push({
      section,
      resourceType: parsed.resource.resourceType,
      id: parsed.resource.id || null,
      json: parsed.resource,
    });
  }

  return results;
}

/**
 * Extract JSON object blocks from text. Looks for opening braces and tries
 * to find matching closing braces. Handles nested objects/arrays and strings.
 */
function extractJsonBlocks(text: string): string[] {
  const blocks: string[] = [];
  let i = 0;

  while (i < text.length) {
    if (text[i] === "{") {
      const result = findMatchingBrace(text, i);
      if (result !== -1) {
        const block = text.slice(i, result + 1);
        // Quick validation: likely JSON if it has "resourceType" or "resource"
        if (block.includes('"') && block.includes(":") && block.length > 20) {
          blocks.push(block);
          i = result + 1;
          continue;
        }
      }
    }
    i++;
  }

  // Filter to only top-level blocks (not nested within others)
  // Sort by start position (they should already be in order)
  // Remove blocks that are substrings of earlier blocks
  const filtered: string[] = [];
  let lastEnd = -1;

  // Actually, since we advance past the end of each found block,
  // we already get non-overlapping blocks. But some might be very small
  // fragments. Filter by size and content.
  for (const block of blocks) {
    if (block.length > 50 && (block.includes("resourceType") || block.includes("resource"))) {
      filtered.push(block);
    }
  }

  return filtered;
}

/**
 * Find the matching closing brace for an opening brace at position start.
 * Returns the index of the closing brace, or -1 if not found.
 * Handles strings (skips braces inside quotes).
 */
function findMatchingBrace(text: string, start: number): number {
  let depth = 0;
  let inString = false;
  let escape = false;

  for (let i = start; i < text.length; i++) {
    const ch = text[i];

    if (escape) {
      escape = false;
      continue;
    }

    if (ch === "\\") {
      if (inString) {
        escape = true;
      }
      continue;
    }

    if (ch === '"') {
      inString = !inString;
      continue;
    }

    if (inString) continue;

    if (ch === "{" || ch === "[") {
      depth++;
    } else if (ch === "}" || ch === "]") {
      depth--;
      if (depth === 0) return i;
    }
  }

  return -1;
}

function escapeRegex(str: string): string {
  return str.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
}

main().catch(console.error);
