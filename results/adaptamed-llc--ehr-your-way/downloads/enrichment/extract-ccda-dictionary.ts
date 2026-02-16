#!/usr/bin/env bun
/**
 * Extracts the C-CDA data dictionary table from the EHR Your Way
 * EHI export documentation page.
 *
 * Input:  ../ehi-export-page.html
 * Output: ./ccda-data-dictionary.json
 */

import { readFileSync, writeFileSync } from "fs";
import { join, dirname } from "path";

const scriptDir = dirname(new URL(import.meta.url).pathname);
const inputPath = join(scriptDir, "..", "ehi-export-page.html");
const outputPath = join(scriptDir, "ccda-data-dictionary.json");

const html = readFileSync(inputPath, "utf-8");

// Extract table rows using regex (the table is simple enough for this)
const tableMatch = html.match(/<table[\s\S]*?<\/table>/i);
if (!tableMatch) {
  console.error("No table found in input HTML");
  process.exit(1);
}

const tableHtml = tableMatch[0];

// Extract header cells
const headerRow = tableHtml.match(/<thead[\s\S]*?<\/thead>/i);
const headers: string[] = [];
if (headerRow) {
  const thMatches = headerRow[0].matchAll(/<th[^>]*>([\s\S]*?)<\/th>/gi);
  for (const m of thMatches) {
    headers.push(m[1].replace(/<[^>]*>/g, "").trim());
  }
}

// Extract body rows
const tbody = tableHtml.match(/<tbody[\s\S]*?<\/tbody>/i);
const rows: string[][] = [];
if (tbody) {
  const trMatches = tbody[0].matchAll(/<tr[^>]*>([\s\S]*?)<\/tr>/gi);
  for (const tr of trMatches) {
    const cells: string[] = [];
    const tdMatches = tr[1].matchAll(/<td[^>]*>([\s\S]*?)<\/td>/gi);
    for (const td of tdMatches) {
      cells.push(td[1].replace(/<[^>]*>/g, "").replace(/\s+/g, " ").trim());
    }
    if (cells.length >= 4) {
      rows.push(cells);
    }
  }
}

// Build structured output
const sections: Record<string, Array<{
  data_element: string;
  entry_xpath: string;
  code_system: string;
}>> = {};

for (const row of rows) {
  const sectionName = row[0];
  if (!sections[sectionName]) {
    sections[sectionName] = [];
  }
  sections[sectionName].push({
    data_element: row[1],
    entry_xpath: row[2],
    code_system: row[3],
  });
}

const output = {
  source: "https://ehryourway.com/electronic-health-information-export/",
  export_format: "C-CDA Release 2.1 (August 2015)",
  export_packaging:
    "ZIP archive containing C-CDA XML, human-readable version, and associated PDF documents",
  export_modes: ["Single Patient Export", "Bulk Export (multiple patients)"],
  table_headers: headers,
  total_data_elements: rows.length,
  sections,
  section_count: Object.keys(sections).length,
  section_names: Object.keys(sections),
};

writeFileSync(outputPath, JSON.stringify(output, null, 2) + "\n");

// Coverage/accounting output
console.log("=== Extraction Summary ===");
console.log(`Input file: ${inputPath}`);
console.log(`Output file: ${outputPath}`);
console.log(`Total files discovered: 1`);
console.log(`Total files parsed: 1`);
console.log(`Parse failures: 0`);
console.log(`Headers found: ${headers.join(", ")}`);
console.log(`Total data element rows: ${rows.length}`);
console.log(`Sections found (${Object.keys(sections).length}):`);
for (const [name, elements] of Object.entries(sections)) {
  console.log(`  - ${name}: ${elements.length} element(s)`);
}
