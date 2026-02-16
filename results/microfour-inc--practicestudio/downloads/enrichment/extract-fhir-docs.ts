#!/usr/bin/env bun
/**
 * Extracts structured data from PracticeStudio FHIR API documentation HTML pages.
 * Parses resource documentation pages to extract parameters, terminology,
 * example responses, and request patterns.
 */

import { readdir, readFile, writeFile } from "fs/promises";
import { join } from "path";

const FHIR_DOCS_DIR = join(import.meta.dir, "..", "fhir-api-docs");
const OUTPUT_FILE = join(import.meta.dir, "fhir-docs-extracted.json");
const EXPORT_PAGE = join(import.meta.dir, "..", "ExportProcess.html");
const INTEROP_PAGE = join(import.meta.dir, "..", "Interoperability.html");

interface FhirResourceDoc {
  resourceType: string;
  sourceFile: string;
  fileSizeBytes: number;
  description: string;
  sections: string[];
  parameters: Array<{ name: string; type: string; description: string }>;
  exampleEndpoints: string[];
  hasExampleResponse: boolean;
}

interface ExtractionResult {
  extractionDate: string;
  exportProcessContent: string;
  ccdSections: string[];
  fhirResources: FhirResourceDoc[];
  coverage: {
    totalFiles: number;
    parsedFiles: number;
    parseFailures: Array<{ file: string; error: string }>;
  };
}

function stripHtml(html: string): string {
  return html.replace(/<[^>]+>/g, " ").replace(/\s+/g, " ").trim();
}

function extractSections(html: string): string[] {
  const sections: string[] = [];
  const headingMatches = html.matchAll(/<h[1-6][^>]*>(.*?)<\/h[1-6]>/gi);
  for (const m of headingMatches) {
    const text = stripHtml(m[1]).trim();
    if (text) sections.push(text);
  }
  return sections;
}

function extractParameters(html: string): Array<{ name: string; type: string; description: string }> {
  const params: Array<{ name: string; type: string; description: string }> = [];
  // Look for table rows with parameter info
  const tableMatches = html.matchAll(/<tr[^>]*>(.*?)<\/tr>/gis);
  for (const m of tableMatches) {
    const cells = [...m[1].matchAll(/<td[^>]*>(.*?)<\/td>/gis)].map(c => stripHtml(c[1]));
    if (cells.length >= 2) {
      params.push({
        name: cells[0] || "",
        type: cells[1] || "",
        description: cells.slice(2).join(" ").trim(),
      });
    }
  }
  return params;
}

function extractEndpoints(html: string): string[] {
  const endpoints: string[] = [];
  const matches = html.matchAll(/(?:GET|POST|PUT|DELETE)\s+[\w/\{\}?&=]+/g);
  for (const m of matches) {
    endpoints.push(m[0].trim());
  }
  // Also look for URL patterns in code blocks
  const codeMatches = html.matchAll(/<code[^>]*>(.*?)<\/code>/gis);
  for (const m of codeMatches) {
    const text = stripHtml(m[1]);
    if (text.includes("/") && (text.includes("Patient") || text.includes("fhir"))) {
      endpoints.push(text);
    }
  }
  return [...new Set(endpoints)];
}

function extractResourceType(filename: string): string {
  return filename
    .replace("Documentation", "")
    .replace(".html", "");
}

async function extractExportPage(): Promise<string> {
  try {
    const html = await readFile(EXPORT_PAGE, "utf-8");
    const paraMatch = html.match(/In the case where a user needs to export.*?each patient\./is);
    if (paraMatch) return stripHtml(paraMatch[0]);
    return "Export content not found";
  } catch {
    return "Export page not available";
  }
}

async function extractCcdSections(): Promise<string[]> {
  try {
    const html = await readFile(INTEROP_PAGE, "utf-8");
    const match = html.match(/following sections:[\s\S]*?HL7 FHIR/i);
    if (match) {
      const items = [...match[0].matchAll(/<li[^>]*>(.*?)<\/li>/gis)];
      return items.map(m => stripHtml(m[1])).filter(Boolean);
    }
    return [];
  } catch {
    return [];
  }
}

async function main() {
  const result: ExtractionResult = {
    extractionDate: new Date().toISOString(),
    exportProcessContent: "",
    ccdSections: [],
    fhirResources: [],
    coverage: { totalFiles: 0, parsedFiles: 0, parseFailures: [] },
  };

  result.exportProcessContent = await extractExportPage();
  result.ccdSections = await extractCcdSections();

  let files: string[];
  try {
    files = (await readdir(FHIR_DOCS_DIR)).filter(f => f.endsWith(".html"));
  } catch {
    console.error("FHIR docs directory not found");
    files = [];
  }

  result.coverage.totalFiles = files.length;

  for (const file of files) {
    try {
      const filepath = join(FHIR_DOCS_DIR, file);
      const html = await readFile(filepath, "utf-8");
      const stat = (await Bun.file(filepath).stat?.()) ?? { size: html.length };

      const doc: FhirResourceDoc = {
        resourceType: extractResourceType(file),
        sourceFile: `fhir-api-docs/${file}`,
        fileSizeBytes: typeof stat === "object" && "size" in stat ? (stat as any).size : html.length,
        description: "",
        sections: extractSections(html),
        parameters: extractParameters(html),
        exampleEndpoints: extractEndpoints(html),
        hasExampleResponse: html.includes('"resourceType"') || html.includes("Example Response"),
      };

      // Extract description from first paragraph after resource name
      const descMatch = html.match(new RegExp(`${doc.resourceType}[\\s\\S]*?<p[^>]*>(.*?)<\\/p>`, "i"));
      if (descMatch) {
        doc.description = stripHtml(descMatch[1]).substring(0, 200);
      }

      result.fhirResources.push(doc);
      result.coverage.parsedFiles++;
    } catch (e: any) {
      result.coverage.parseFailures.push({ file, error: e.message });
    }
  }

  await writeFile(OUTPUT_FILE, JSON.stringify(result, null, 2));
  console.log(`Extracted ${result.coverage.parsedFiles}/${result.coverage.totalFiles} files`);
  console.log(`CCD sections: ${result.ccdSections.length}`);
  console.log(`FHIR resources documented: ${result.fhirResources.length}`);
  console.log(`Parse failures: ${result.coverage.parseFailures.length}`);
  console.log(`Output: ${OUTPUT_FILE}`);
}

main().catch(console.error);
