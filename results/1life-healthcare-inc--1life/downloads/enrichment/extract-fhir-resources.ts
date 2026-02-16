#!/usr/bin/env bun
/**
 * Extracts structured data from One Medical FHIR resource HTML documentation pages.
 * Parses field tables, extensions info, and page metadata into queryable JSON.
 *
 * Usage: bun run extract-fhir-resources.ts
 * Input: ../fhir/resources/*.html, ../fhir/extensions.html, ../fhir/terminology.html,
 *        ../ehi-export-overview.html, ../ccda/patient-continuity-of-care-document.html
 * Output: fhir-resources.json, ehi-export-summary.json, extraction-report.json
 */

import { readdir, readFile, writeFile } from "fs/promises";
import { join, basename } from "path";

const DOWNLOADS_DIR = join(import.meta.dir, "..");
const OUTPUT_DIR = import.meta.dir;

interface Field {
  name: string;
  type: string;
  cardinality: string;
  description: string;
}

interface FhirResource {
  resourceType: string;
  sourceFile: string;
  sourceUrl: string;
  tables: { fields: Field[] }[];
  totalFields: number;
}

interface EhiExportSummary {
  description: string;
  formats: {
    json: { description: string; resourceTypes: string[] };
    xml: { description: string; ccdaSections: string[] };
  };
}

interface ExtractionReport {
  extractedAt: string;
  totalFilesDiscovered: number;
  totalFilesParsed: number;
  parseFailures: { file: string; error: string }[];
  resourceSummary: { resourceType: string; fieldCount: number; tableCount: number }[];
}

function stripHtml(html: string): string {
  return html.replace(/<[^>]+>/g, "").replace(/&amp;/g, "&").replace(/&lt;/g, "<")
    .replace(/&gt;/g, ">").replace(/&quot;/g, '"').replace(/&#34;/g, '"')
    .replace(/&rsquo;/g, "'").replace(/&ldquo;/g, '"').replace(/&rdquo;/g, '"')
    .replace(/&ndash;/g, "–").replace(/&mdash;/g, "—").replace(/&#39;/g, "'")
    .replace(/&nbsp;/g, " ").trim();
}

function extractTables(html: string): { fields: Field[] }[] {
  const tables: { fields: Field[] }[] = [];
  const tableRegex = /<table[^>]*>([\s\S]*?)<\/table>/gi;
  let tableMatch;

  while ((tableMatch = tableRegex.exec(html)) !== null) {
    const tableHtml = tableMatch[1];
    const rows: Field[] = [];
    const rowRegex = /<tr[^>]*>([\s\S]*?)<\/tr>/gi;
    let rowMatch;
    let isHeader = true;

    while ((rowMatch = rowRegex.exec(tableHtml)) !== null) {
      const cellRegex = /<t[dh][^>]*>([\s\S]*?)<\/t[dh]>/gi;
      const cells: string[] = [];
      let cellMatch;
      while ((cellMatch = cellRegex.exec(rowMatch[1])) !== null) {
        cells.push(stripHtml(cellMatch[1]));
      }

      if (isHeader) {
        isHeader = false;
        continue; // Skip header row
      }

      if (cells.length >= 4) {
        rows.push({
          name: cells[0],
          type: cells[1],
          cardinality: cells[2],
          description: cells[3],
        });
      } else if (cells.length === 2) {
        // Some tables (like EHI overview) have 2-column layout
        rows.push({
          name: cells[0],
          type: "",
          cardinality: "",
          description: cells[1] || "",
        });
      }
    }

    if (rows.length > 0) {
      tables.push({ fields: rows });
    }
  }

  return tables;
}

function extractEhiExportSummary(html: string): EhiExportSummary {
  const text = stripHtml(html);

  // Extract FHIR resource types from the JSON section table
  const jsonResourceTypes: string[] = [];
  const resourceTypeMatch = html.match(
    /Resource Type<\/th>[\s\S]*?<\/table>/i
  );
  if (resourceTypeMatch) {
    const tdRegex = /<td[^>]*>([\s\S]*?)<\/td>/gi;
    let m;
    while ((m = tdRegex.exec(resourceTypeMatch[0])) !== null) {
      const val = stripHtml(m[1]);
      if (val) jsonResourceTypes.push(val);
    }
  }

  // Extract C-CDA sections
  const ccdaSections: string[] = [];
  const ccdaMatch = html.match(
    /C-CDA Section<\/th>[\s\S]*?<\/table>/i
  );
  if (ccdaMatch) {
    const tdRegex = /<td[^>]*>([\s\S]*?)<\/td>/gi;
    let m;
    while ((m = tdRegex.exec(ccdaMatch[0])) !== null) {
      const val = stripHtml(m[1]);
      if (val) ccdaSections.push(val);
    }
  }

  return {
    description:
      "The EHI export contains the electronic health information available for a single patient or multiple patients in computable file formats. The export(s) can be downloaded as a zip file containing a .json and a .xml file.",
    formats: {
      json: {
        description:
          "FHIR bundle with all resources on record belonging to the patient",
        resourceTypes: jsonResourceTypes,
      },
      xml: {
        description:
          "Patient Continuity of Care Document formatted in accordance with the C-CDA version 2.1 specification",
        ccdaSections,
      },
    },
  };
}

function extractCcdaInfo(html: string): Record<string, unknown> {
  const text = html;

  // Extract API endpoint info
  const sections: string[] = [];
  const sectionMatch = text.match(/C-CDA Section<\/th>[\s\S]*?<\/table>/i);
  if (sectionMatch) {
    const rowRegex = /<tr[^>]*>([\s\S]*?)<\/tr>/gi;
    let m;
    let isFirst = true;
    while ((m = rowRegex.exec(sectionMatch[0])) !== null) {
      if (isFirst) { isFirst = false; continue; }
      const cells = [...m[1].matchAll(/<td[^>]*>([\s\S]*?)<\/td>/gi)];
      if (cells.length >= 2) {
        sections.push(
          `${stripHtml(cells[0][1])} (date_range_applies: ${stripHtml(cells[1][1])})`
        );
      }
    }
  }

  // Extract request parameters
  const params: Record<string, unknown>[] = [];
  const paramMatch = text.match(/Parameter<\/th>[\s\S]*?<\/table>/i);
  if (paramMatch) {
    const rowRegex = /<tr[^>]*>([\s\S]*?)<\/tr>/gi;
    let m;
    let isFirst = true;
    while ((m = rowRegex.exec(paramMatch[0])) !== null) {
      if (isFirst) { isFirst = false; continue; }
      const cells = [...m[1].matchAll(/<td[^>]*>([\s\S]*?)<\/td>/gi)];
      if (cells.length >= 4) {
        params.push({
          parameter: stripHtml(cells[0][1]),
          required: stripHtml(cells[1][1]),
          type: stripHtml(cells[2][1]),
          description: stripHtml(cells[3][1]),
        });
      }
    }
  }

  return {
    endpoint: "GET https://production.app.1life.com/api/ccda",
    authentication: "Basic Auth (registration required)",
    requestParameters: params,
    sections,
  };
}

function extractExtensions(html: string): Record<string, unknown>[] {
  const extensions: Record<string, unknown>[] = [];

  // Hugo generates headings like: <h4 id=race>Race\n<a ...>...</a></h4>
  // Split into sections by h3/h4 headings
  const sectionRegex =
    /<h[34][^>]*>([\s\S]*?)<\/h[34]>([\s\S]*?)(?=<h[34]|<h[23]|<footer|$)/gi;
  let m;
  while ((m = sectionRegex.exec(html)) !== null) {
    const title = stripHtml(m[1]).replace(/\s+/g, " ").trim();
    const content = m[2];

    // Extract URL — Hugo wraps it in <a> tags after "URL:</strong>"
    const urlMatch = content.match(
      /URL:[\s\S]*?href=([^\s>"]+)/i
    ) || content.match(
      /URL:[\s\S]*?(https?:\/\/[^\s<"&#]+)/i
    );
    // Extract "Currently used in"
    const usedInMatch = content.match(
      /Currently used in:[\s\S]*?<\/strong>\s*(?:<[^>]*>)*\s*([^<\n]+)/i
    ) || content.match(
      /Currently used in:\s*(?:<[^>]*>)*\s*([^<\n]+)/i
    );

    if (urlMatch || usedInMatch) {
      extensions.push({
        name: title,
        url: urlMatch ? urlMatch[1] : null,
        usedIn: usedInMatch ? stripHtml(usedInMatch[1]) : null,
        description: stripHtml(content).substring(0, 500).replace(/\s+/g, " ").trim(),
      });
    }
  }

  return extensions;
}

function extractTerminology(html: string): Record<string, unknown>[] {
  const terms: Record<string, unknown>[] = [];

  // Strategy: find each table, then look backwards for the nearest h2 heading
  const tableRegex = /<table[^>]*>([\s\S]*?)<\/table>/gi;
  let tableMatch;
  while ((tableMatch = tableRegex.exec(html)) !== null) {
    const tableHtml = tableMatch[1];
    const beforeTable = html.substring(0, tableMatch.index);

    // Find the last h2 heading before this table
    const headingMatches = [...beforeTable.matchAll(/<h2[^>]*>([\s\S]*?)<\/h2>/gi)];
    if (headingMatches.length === 0) continue;
    const lastHeading = headingMatches[headingMatches.length - 1];
    const sectionName = stripHtml(lastHeading[1]).replace(/\s+/g, " ").trim();

    // Skip navigation and generic headings
    if (sectionName === "Navigation" || sectionName === "Terminology") continue;

    const rowRegex = /<tr[^>]*>([\s\S]*?)<\/tr>/gi;
    let rowMatch;
    let isFirst = true;
    while ((rowMatch = rowRegex.exec(tableHtml)) !== null) {
      if (isFirst) { isFirst = false; continue; }
      const cells = [...rowMatch[1].matchAll(/<td[^>]*>([\s\S]*?)<\/td>/gi)];
      if (cells.length >= 2) {
        terms.push({
          resource: sectionName,
          code: stripHtml(cells[0][1]),
          description: stripHtml(cells[1][1]),
          system: "http://onemedical.com/terminology",
        });
      }
    }
  }

  return terms;
}

async function main() {
  const report: ExtractionReport = {
    extractedAt: new Date().toISOString(),
    totalFilesDiscovered: 0,
    totalFilesParsed: 0,
    parseFailures: [],
    resourceSummary: [],
  };

  // 1. Parse all FHIR resource pages
  const resourceDir = join(DOWNLOADS_DIR, "fhir", "resources");
  const resourceFiles = (await readdir(resourceDir)).filter((f) =>
    f.endsWith(".html")
  );
  report.totalFilesDiscovered += resourceFiles.length;

  const resources: FhirResource[] = [];

  for (const file of resourceFiles) {
    try {
      const html = await readFile(join(resourceDir, file), "utf-8");
      const resourceType = basename(file, ".html");
      const tables = extractTables(html);
      const totalFields = tables.reduce((sum, t) => sum + t.fields.length, 0);

      resources.push({
        resourceType:
          resourceType.charAt(0).toUpperCase() + resourceType.slice(1),
        sourceFile: `fhir/resources/${file}`,
        sourceUrl: `https://apidocs.onemedical.io/fhir/resources/${resourceType}/`,
        tables,
        totalFields,
      });

      report.totalFilesParsed++;
      report.resourceSummary.push({
        resourceType:
          resourceType.charAt(0).toUpperCase() + resourceType.slice(1),
        fieldCount: totalFields,
        tableCount: tables.length,
      });
    } catch (e: unknown) {
      report.parseFailures.push({
        file: `fhir/resources/${file}`,
        error: e instanceof Error ? e.message : String(e),
      });
    }
  }

  // 2. Parse EHI export overview
  const additionalFiles = [
    "ehi-export-overview.html",
    "fhir/extensions.html",
    "fhir/terminology.html",
    "fhir/overview.html",
    "fhir/capability-statement.html",
    "ccda/patient-continuity-of-care-document.html",
  ];
  report.totalFilesDiscovered += additionalFiles.length;

  let ehiSummary: EhiExportSummary | null = null;
  let extensionsData: Record<string, unknown>[] = [];
  let terminologyData: Record<string, unknown>[] = [];
  let ccdaData: Record<string, unknown> = {};

  for (const file of additionalFiles) {
    try {
      const html = await readFile(join(DOWNLOADS_DIR, file), "utf-8");
      report.totalFilesParsed++;

      if (file === "ehi-export-overview.html") {
        ehiSummary = extractEhiExportSummary(html);
      } else if (file === "fhir/extensions.html") {
        extensionsData = extractExtensions(html);
      } else if (file === "fhir/terminology.html") {
        terminologyData = extractTerminology(html);
      } else if (file === "ccda/patient-continuity-of-care-document.html") {
        ccdaData = extractCcdaInfo(html);
      }
    } catch (e: unknown) {
      report.parseFailures.push({
        file,
        error: e instanceof Error ? e.message : String(e),
      });
    }
  }

  // Write outputs
  await writeFile(
    join(OUTPUT_DIR, "fhir-resources.json"),
    JSON.stringify(resources, null, 2)
  );

  await writeFile(
    join(OUTPUT_DIR, "ehi-export-summary.json"),
    JSON.stringify(
      {
        ehiExport: ehiSummary,
        ccda: ccdaData,
        extensions: extensionsData,
        terminology: terminologyData,
      },
      null,
      2
    )
  );

  await writeFile(
    join(OUTPUT_DIR, "extraction-report.json"),
    JSON.stringify(report, null, 2)
  );

  console.log(`Extraction complete:`);
  console.log(`  Files discovered: ${report.totalFilesDiscovered}`);
  console.log(`  Files parsed: ${report.totalFilesParsed}`);
  console.log(`  Parse failures: ${report.parseFailures.length}`);
  console.log(`  FHIR resources extracted: ${resources.length}`);
  console.log(
    `  Total fields across all resources: ${resources.reduce((s, r) => s + r.totalFields, 0)}`
  );
}

main().catch(console.error);
