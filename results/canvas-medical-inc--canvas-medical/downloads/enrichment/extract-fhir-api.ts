#!/usr/bin/env bun
/**
 * Extract structured FHIR API resource definitions from Canvas Medical
 * documentation HTML pages.
 *
 * Input: ../api-pages/*.html
 * Output: fhir-api-resources.json
 *
 * Run: bun run extract-fhir-api.ts
 */

import { readdirSync, readFileSync, writeFileSync } from "fs";
import { join } from "path";

const API_DIR = join(import.meta.dir, "..", "api-pages");
const OUTPUT = join(import.meta.dir, "fhir-api-resources.json");

interface FhirField {
  name: string;
  type: string;
  required: boolean;
  description: string;
  valueOptions?: string[];
}

interface FhirOperation {
  method: string;
  path: string;
  summary: string;
  description: string;
  attributes: FhirField[];
}

interface FhirResource {
  name: string;
  sourceFile: string;
  sourceUrl: string;
  lastUpdated: string | null;
  description: string;
  endpoints: { method: string; path: string }[];
  operations: FhirOperation[];
  totalFields: number;
}

interface ExtractionResult {
  extractionDate: string;
  totalFiles: number;
  totalParsed: number;
  parseFailures: { file: string; error: string }[];
  resources: FhirResource[];
  summary: {
    totalResources: number;
    totalOperations: number;
    totalFields: number;
  };
}

function stripHtml(html: string): string {
  return html
    .replace(/<[^>]+>/g, " ")
    .replace(/&amp;/g, "&")
    .replace(/&lt;/g, "<")
    .replace(/&gt;/g, ">")
    .replace(/&quot;/g, '"')
    .replace(/&#39;/g, "'")
    .replace(/&nbsp;/g, " ")
    .replace(/\s+/g, " ")
    .trim();
}

function parseApiPage(
  filename: string,
  content: string
): FhirResource | null {
  // Skip non-resource pages
  const skipPages = [
    "introduction",
    "service-base-urls",
    "quickstart",
    "authentication-best-practices",
    "customer-authentication",
    "conditional-requests",
    "pagination",
    "date-filtering",
    "errors",
    "software-requirements",
  ];
  if (skipPages.includes(filename.replace(".html", ""))) {
    return null;
  }

  // Extract resource name from title
  const titleMatch = content.match(
    /<h1 class="article__title"[^>]*>(.*?)<\/h1>/s
  );
  const resourceName = titleMatch
    ? stripHtml(titleMatch[1])
    : filename.replace(".html", "");

  // Extract last updated date
  const dateMatch = content.match(
    /<time[^>]*>\s*Last updated:\s*(.*?)\s*<\/time>/
  );
  const lastUpdated = dateMatch ? dateMatch[1].trim() : null;

  // Extract resource description from the first apidoc__info__description
  const descMatch = content.match(
    /class="apidoc__info__description">\s*(.*?)\s*<\/div>/s
  );
  const description = descMatch ? stripHtml(descMatch[1]) : "";

  // Extract endpoints from the endpoint list
  const endpoints: { method: string; path: string }[] = [];
  const epPattern =
    /class="apidoc__endpoint__method\s+apidoc__endpoint__method__(\w+)">\s*(\w+)\s*<\/span>\s*<div class="apidoc__endpoint__url">(.*?)<\/div>/gs;
  let m;
  while ((m = epPattern.exec(content)) !== null) {
    endpoints.push({
      method: stripHtml(m[2]).toUpperCase(),
      path: stripHtml(m[3]),
    });
  }

  // Split the content by operation sections using apidoc__gridrow
  // Each operation starts with an apidoc__info block that has method + url + summary
  const operations: FhirOperation[] = [];

  // Find all operation info blocks
  const opInfoPattern =
    /<div id="(\w+)" class="apidoc__info">\s*<span class="apidoc__info__method\s+apidoc__info__method__(\w+)">\s*(\w+)\s*<\/span>\s*<div class="apidoc__info__url">(.*?)<\/div>\s*<h4 class="apidoc__info__summary">(.*?)<\/h4>\s*<div class="apidoc__info__description">(.*?)<\/div>/gs;

  const opPositions: {
    id: string;
    method: string;
    path: string;
    summary: string;
    description: string;
    startIndex: number;
  }[] = [];

  while ((m = opInfoPattern.exec(content)) !== null) {
    opPositions.push({
      id: m[1],
      method: stripHtml(m[3]).toUpperCase(),
      path: stripHtml(m[4]),
      summary: stripHtml(m[5]),
      description: stripHtml(m[6]),
      startIndex: m.index,
    });
  }

  // For each operation, extract the fields that follow it until the next operation
  for (let i = 0; i < opPositions.length; i++) {
    const op = opPositions[i];
    const nextStart =
      i + 1 < opPositions.length
        ? opPositions[i + 1].startIndex
        : content.length;
    const opSection = content.substring(op.startIndex, nextStart);

    // Extract fields from apidoc__object blocks in this section
    const fields: FhirField[] = [];
    const fieldPattern =
      /<div class="apidoc__object">\s*<div class="apidoc__object__name">\s*(.*?)\s*<\/div>/gs;

    // Use a more comprehensive approach: find all objects with their attributes
    // by scanning for the apidoc__object blocks
    const objectBlocks = opSection.split(
      /<div class="apidoc__object">/
    );

    for (let j = 1; j < objectBlocks.length; j++) {
      const block = objectBlocks[j];

      // Name
      const nameMatch = block.match(
        /<div class="apidoc__object__name">\s*(.*?)\s*<\/div>/s
      );
      const name = nameMatch ? stripHtml(nameMatch[1]) : "";

      // Type
      const typeMatch = block.match(
        /<div class="apidoc__object__type">\s*(.*?)\s*<\/div>/s
      );
      const type = typeMatch ? stripHtml(typeMatch[1]) : "";

      // Required
      const required = block.includes(
        'class="apidoc__object__required"'
      );

      // Description (may have multiple description divs - concat them)
      const descMatches = [
        ...block.matchAll(
          /<div class="apidoc__object__description">\s*(.*?)\s*<\/div>/gs
        ),
      ];
      const desc = descMatches
        .map((dm) => stripHtml(dm[1]))
        .filter((d) => d.length > 0)
        .join(" ");

      // Value options from enum_options
      const enumMatch = block.match(
        /<div class="apidoc__object__enum_options">\s*(.*?)\s*<\/div>/s
      );
      let valueOptions: string[] | undefined;
      if (enumMatch) {
        const enumText = stripHtml(enumMatch[1]);
        if (enumText.length > 0) {
          valueOptions = enumText
            .split(/\s+/)
            .filter((v) => v.length > 0);
        }
      }

      if (name) {
        fields.push({
          name,
          type,
          required,
          description: desc,
          ...(valueOptions && valueOptions.length > 0
            ? { valueOptions }
            : {}),
        });
      }
    }

    operations.push({
      method: op.method,
      path: op.path,
      summary: op.summary,
      description: op.description,
      attributes: fields,
    });
  }

  const totalFields = operations.reduce(
    (sum, op) => sum + op.attributes.length,
    0
  );

  return {
    name: resourceName,
    sourceFile: filename,
    sourceUrl: `https://docs.canvasmedical.com/api/${filename.replace(".html", "")}/`,
    lastUpdated,
    description,
    endpoints,
    operations,
    totalFields,
  };
}

// Main
const files = readdirSync(API_DIR).filter((f) => f.endsWith(".html"));
const result: ExtractionResult = {
  extractionDate: new Date().toISOString(),
  totalFiles: files.length,
  totalParsed: 0,
  parseFailures: [],
  resources: [],
  summary: { totalResources: 0, totalOperations: 0, totalFields: 0 },
};

for (const file of files) {
  try {
    const content = readFileSync(join(API_DIR, file), "utf-8");
    const resource = parseApiPage(file, content);
    if (resource) {
      result.resources.push(resource);
      result.totalParsed++;
    }
  } catch (err: any) {
    result.parseFailures.push({ file, error: err.message });
  }
}

result.summary = {
  totalResources: result.resources.length,
  totalOperations: result.resources.reduce(
    (sum, r) => sum + r.operations.length,
    0
  ),
  totalFields: result.resources.reduce((sum, r) => sum + r.totalFields, 0),
};

writeFileSync(OUTPUT, JSON.stringify(result, null, 2));
console.log(
  `Extracted ${result.resources.length} resources from ${result.totalFiles} files`
);
console.log(
  `Total operations: ${result.summary.totalOperations}, Total fields: ${result.summary.totalFields}`
);
console.log(`Parse failures: ${result.parseFailures.length}`);
if (result.parseFailures.length > 0) {
  for (const f of result.parseFailures) {
    console.log(`  ${f.file}: ${f.error}`);
  }
}
for (const r of result.resources) {
  const ops = r.operations.length;
  const fields = r.totalFields;
  const eps = r.endpoints.map((e) => `${e.method} ${e.path}`).join(", ");
  console.log(`  ${r.name}: ${ops} ops, ${fields} fields [${eps}]`);
}
