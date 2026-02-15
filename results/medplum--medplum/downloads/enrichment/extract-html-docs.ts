/**
 * extract-html-docs.ts
 *
 * Parses downloaded Medplum FHIR resource documentation HTML pages
 * and extracts structured field definitions, search parameters, and
 * resource descriptions into queryable JSON.
 *
 * Input:
 *   - ../fhir-resources/*.html   (146 resource doc pages)
 *   - ../fhir-datatypes/*.html   (41 data type doc pages)
 *
 * Output:
 *   - html-docs.json             (parsed documentation for all pages)
 *   - html-docs-coverage.json    (accounting: parse stats)
 */

import { readFileSync, readdirSync, writeFileSync } from "fs";
import { join, basename } from "path";

const downloadsDir = join(import.meta.dir, "..");

interface ParsedField {
  name: string;
  required: boolean;
  type: string;
  description: string;
}

interface ParsedSearchParam {
  name: string;
  type: string;
  description: string;
  expression: string;
}

interface ParsedDoc {
  name: string;
  category: "resource" | "datatype";
  description: string;
  fields: ParsedField[];
  searchParams: ParsedSearchParam[];
  sourceFile: string;
  sourceUrl: string;
}

function stripHtml(html: string): string {
  return html.replace(/<[^>]*>/g, " ").replace(/\s+/g, " ").trim();
}

function extractTextContent(html: string): string {
  // Remove script and style tags
  let cleaned = html.replace(/<script[^>]*>[\s\S]*?<\/script>/gi, "");
  cleaned = cleaned.replace(/<style[^>]*>[\s\S]*?<\/style>/gi, "");
  return stripHtml(cleaned);
}

function parseResourcePage(
  html: string,
  filename: string,
  category: "resource" | "datatype"
): ParsedDoc | null {
  const name = basename(filename, ".html");

  // Extract title
  const titleMatch = html.match(/<title[^>]*>([^<]*)/);
  const title = titleMatch ? titleMatch[1].replace(" | Medplum", "").trim() : name;

  // Extract description from the first paragraph after <h1>
  let description = "";
  const h1Match = html.match(/<h1[^>]*>([\s\S]*?)<\/h1>/i);
  if (h1Match) {
    const afterH1 = html.substring(html.indexOf(h1Match[0]) + h1Match[0].length);
    const firstParaMatch = afterH1.match(/<p[^>]*>([\s\S]*?)<\/p>/i);
    if (firstParaMatch) {
      description = stripHtml(firstParaMatch[1]);
    }
  }

  // Extract Elements table
  // The table structure is: Name | Required | Type | Description
  const fields: ParsedField[] = [];
  const searchParams: ParsedSearchParam[] = [];

  // Find tables by looking for table elements
  const tableMatches = [...html.matchAll(/<table[^>]*>([\s\S]*?)<\/table>/gi)];

  for (const tableMatch of tableMatches) {
    const tableHtml = tableMatch[1];
    const rows = [...tableHtml.matchAll(/<tr[^>]*>([\s\S]*?)<\/tr>/gi)];

    if (rows.length < 2) continue;

    // Check header row to determine table type
    const headerCells = [
      ...rows[0][1].matchAll(/<t[hd][^>]*>([\s\S]*?)<\/t[hd]>/gi),
    ].map((m) => stripHtml(m[1]).toLowerCase());

    if (
      headerCells.includes("name") &&
      headerCells.includes("type") &&
      headerCells.includes("description")
    ) {
      const hasExpression = headerCells.includes("expression");
      const hasRequired = headerCells.includes("required");

      for (let i = 1; i < rows.length; i++) {
        const cells = [
          ...rows[i][1].matchAll(/<td[^>]*>([\s\S]*?)<\/td>/gi),
        ].map((m) => stripHtml(m[1]));

        if (cells.length < 3) continue;

        if (hasExpression) {
          // Search Parameters table: Name | Type | Description | Expression
          searchParams.push({
            name: cells[0] ?? "",
            type: cells[1] ?? "",
            description: cells[2] ?? "",
            expression: cells[3] ?? "",
          });
        } else {
          // Elements table: Name | Required | Type | Description
          // or: Name | Type | Description (if no Required column)
          if (hasRequired) {
            fields.push({
              name: cells[0] ?? "",
              required: (cells[1] ?? "").includes("✓"),
              type: cells[2] ?? "",
              description: cells[3] ?? "",
            });
          } else {
            fields.push({
              name: cells[0] ?? "",
              required: false,
              type: cells[1] ?? "",
              description: cells[2] ?? "",
            });
          }
        }
      }
    }
  }

  const urlPath =
    category === "resource"
      ? `https://www.medplum.com/docs/api/fhir/resources/${name}`
      : `https://www.medplum.com/docs/api/fhir/datatypes/${name}`;

  return {
    name: title,
    category,
    description,
    fields,
    searchParams,
    sourceFile: `fhir-${category === "resource" ? "resources" : "datatypes"}/${basename(filename)}`,
    sourceUrl: urlPath,
  };
}

// Process all resource pages
const resourceDir = join(downloadsDir, "fhir-resources");
const datatypeDir = join(downloadsDir, "fhir-datatypes");

const docs: ParsedDoc[] = [];
const failures: { file: string; reason: string }[] = [];

let totalDiscovered = 0;
let totalParsed = 0;

for (const dir of [
  { path: resourceDir, category: "resource" as const },
  { path: datatypeDir, category: "datatype" as const },
]) {
  let files: string[];
  try {
    files = readdirSync(dir.path).filter((f) => f.endsWith(".html"));
  } catch {
    console.error(`Directory not found: ${dir.path}`);
    continue;
  }

  totalDiscovered += files.length;

  for (const file of files) {
    try {
      const html = readFileSync(join(dir.path, file), "utf-8");
      const doc = parseResourcePage(html, file, dir.category);
      if (doc) {
        docs.push(doc);
        totalParsed++;
      } else {
        failures.push({ file: join(dir.path, file), reason: "parse returned null" });
      }
    } catch (e: any) {
      failures.push({ file: join(dir.path, file), reason: e.message });
    }
  }
}

// Sort by name
docs.sort((a, b) => a.name.localeCompare(b.name));

// Write output
writeFileSync(
  join(import.meta.dir, "html-docs.json"),
  JSON.stringify(docs, null, 2)
);

const coverageReport = {
  extraction_date: new Date().toISOString(),
  input_directories: [
    "../fhir-resources/",
    "../fhir-datatypes/",
  ],
  results: {
    total_files_discovered: totalDiscovered,
    total_files_parsed: totalParsed,
    total_fields_extracted: docs.reduce((sum, d) => sum + d.fields.length, 0),
    total_search_params_extracted: docs.reduce(
      (sum, d) => sum + d.searchParams.length,
      0
    ),
    parse_failures: failures.length,
    parse_failure_details: failures,
  },
  per_category: {
    resources: {
      count: docs.filter((d) => d.category === "resource").length,
      total_fields: docs
        .filter((d) => d.category === "resource")
        .reduce((sum, d) => sum + d.fields.length, 0),
    },
    datatypes: {
      count: docs.filter((d) => d.category === "datatype").length,
      total_fields: docs
        .filter((d) => d.category === "datatype")
        .reduce((sum, d) => sum + d.fields.length, 0),
    },
  },
};

writeFileSync(
  join(import.meta.dir, "html-docs-coverage.json"),
  JSON.stringify(coverageReport, null, 2)
);

console.log(`Parsed ${totalParsed}/${totalDiscovered} files`);
console.log(
  `  Resources: ${coverageReport.per_category.resources.count} (${coverageReport.per_category.resources.total_fields} fields)`
);
console.log(
  `  Data Types: ${coverageReport.per_category.datatypes.count} (${coverageReport.per_category.datatypes.total_fields} fields)`
);
console.log(`  Parse failures: ${failures.length}`);
console.log("Output: html-docs.json, html-docs-coverage.json");
