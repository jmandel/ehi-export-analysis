#!/usr/bin/env bun
/**
 * Extract structured SDK data model definitions from Canvas Medical
 * documentation HTML pages. These represent the internal data models
 * of the Canvas platform.
 *
 * Input: ../sdk-data-pages/data-*.html
 * Output: sdk-data-models.json
 *
 * Run: bun run extract-sdk-models.ts
 */

import { readdirSync, readFileSync, writeFileSync } from "fs";
import { join } from "path";

const SDK_DIR = join(import.meta.dir, "..", "sdk-data-pages");
const OUTPUT = join(import.meta.dir, "sdk-data-models.json");

interface SdkField {
  name: string;
  type: string;
}

interface SdkModel {
  name: string;
  fields: SdkField[];
}

interface EnumValue {
  value: string;
  label: string;
}

interface SdkEnum {
  name: string;
  values: EnumValue[];
}

interface SdkDataPage {
  pageName: string;
  sourceFile: string;
  sourceUrl: string;
  lastUpdated: string | null;
  introduction: string;
  models: SdkModel[];
  enums: SdkEnum[];
  filterableFields: string[];
}

interface ExtractionResult {
  extractionDate: string;
  totalFiles: number;
  totalParsed: number;
  parseFailures: { file: string; error: string }[];
  dataPages: SdkDataPage[];
}

function stripHtml(html: string): string {
  return html
    .replace(/<[^>]+>/g, "")
    .replace(/&amp;/g, "&")
    .replace(/&lt;/g, "<")
    .replace(/&gt;/g, ">")
    .replace(/&quot;/g, '"')
    .replace(/&#39;/g, "'")
    .replace(/&nbsp;/g, " ")
    .replace(/\s+/g, " ")
    .trim();
}

function parseSdkPage(filename: string, content: string): SdkDataPage | null {
  // Extract title
  const titleMatch = content.match(
    /<h1 class="article__title"[^>]*>(.*?)<\/h1>/s
  );
  const pageName = titleMatch
    ? stripHtml(titleMatch[1])
    : filename.replace(".html", "");

  // Skip the index page
  if (filename === "data.html") return null;

  // Extract last updated
  const dateMatch = content.match(
    /<time[^>]*>\s*Last updated:\s*(.*?)\s*<\/time>/
  );
  const lastUpdated = dateMatch ? dateMatch[1].trim() : null;

  // Extract article body
  const bodyMatch = content.match(
    /itemprop="articleBody">(.*?)<\/div>\s*<\/div>\s*<\/div>\s*<\/article>/s
  );
  if (!bodyMatch) return null;
  const body = bodyMatch[1];

  // Extract introduction (text before first h2 after Introduction heading)
  const introMatch = body.match(
    /<h2[^>]*id="introduction"[^>]*>.*?<\/h2>(.*?)(?=<h2)/s
  );
  const introduction = introMatch ? stripHtml(introMatch[1]) : "";

  // Extract tables - these contain the model attributes
  const models: SdkModel[] = [];
  const enums: SdkEnum[] = [];

  // Split by h2/h3 headings to find sections
  const sections = body.split(/<h[23][^>]*>/);

  let currentSectionName = "";

  for (const section of sections) {
    // Get the section heading text
    const headingEndMatch = section.match(/^(.*?)<\/h[23]>/s);
    if (headingEndMatch) {
      currentSectionName = stripHtml(headingEndMatch[1]);
    }

    // Find tables in this section
    const tableMatch = section.match(/<table>(.*?)<\/table>/s);
    if (!tableMatch) continue;

    const tableContent = tableMatch[1];
    const rows = [...tableContent.matchAll(/<tr>(.*?)<\/tr>/gs)];

    if (rows.length < 2) continue; // Need header + at least one data row

    // Check header to determine if this is a model table or enum table
    const headerCells = [
      ...rows[0][1].matchAll(/<th>(.*?)<\/th>/gs),
    ].map((m) => stripHtml(m[1]));

    if (
      headerCells.length >= 2 &&
      headerCells[0] === "Field Name" &&
      headerCells[1] === "Type"
    ) {
      // This is a model attributes table
      const fields: SdkField[] = [];
      for (let i = 1; i < rows.length; i++) {
        const cells = [...rows[i][1].matchAll(/<td>(.*?)<\/td>/gs)].map((m) =>
          stripHtml(m[1])
        );
        if (cells.length >= 2) {
          fields.push({
            name: cells[0],
            type: cells[1],
          });
        }
      }
      if (fields.length > 0) {
        models.push({
          name: currentSectionName.replace(/ #$/, "").trim(),
          fields,
        });
      }
    } else if (
      headerCells.length >= 2 &&
      headerCells[0] === "Value" &&
      headerCells[1] === "Label"
    ) {
      // This is an enum table
      const values: EnumValue[] = [];
      for (let i = 1; i < rows.length; i++) {
        const cells = [...rows[i][1].matchAll(/<td>(.*?)<\/td>/gs)].map((m) =>
          stripHtml(m[1])
        );
        if (cells.length >= 2) {
          values.push({
            value: cells[0],
            label: cells[1],
          });
        }
      }
      if (values.length > 0) {
        enums.push({
          name: currentSectionName.replace(/ #$/, "").trim(),
          values,
        });
      }
    }
  }

  // Extract filterable fields from the Filtering section
  const filterableFields: string[] = [];
  const filterMatch = body.match(
    /<h2[^>]*id="filtering"[^>]*>.*?<\/h2>(.*?)(?=<h2|$)/s
  );
  if (filterMatch) {
    const filterItems = [
      ...filterMatch[1].matchAll(
        /<code class="language-plaintext highlighter-rouge">(.*?)<\/code>/g
      ),
    ];
    for (const fi of filterItems) {
      const field = stripHtml(fi[1]);
      if (field && !field.includes("=") && !field.includes("(")) {
        filterableFields.push(field);
      }
    }
  }

  return {
    pageName,
    sourceFile: filename,
    sourceUrl: `https://docs.canvasmedical.com/sdk/${filename.replace(".html", "")}/`,
    lastUpdated,
    introduction,
    models,
    enums,
    filterableFields,
  };
}

// Main
const files = readdirSync(SDK_DIR).filter(
  (f) => f.endsWith(".html") && f.startsWith("data")
);
const result: ExtractionResult = {
  extractionDate: new Date().toISOString(),
  totalFiles: files.length,
  totalParsed: 0,
  parseFailures: [],
  dataPages: [],
};

for (const file of files) {
  try {
    const content = readFileSync(join(SDK_DIR, file), "utf-8");
    const page = parseSdkPage(file, content);
    if (page) {
      result.dataPages.push(page);
      result.totalParsed++;
    }
  } catch (err: any) {
    result.parseFailures.push({ file, error: err.message });
  }
}

writeFileSync(OUTPUT, JSON.stringify(result, null, 2));
console.log(
  `Extracted ${result.dataPages.length} data model pages from ${result.totalFiles} files`
);
console.log(`Parse failures: ${result.parseFailures.length}`);
if (result.parseFailures.length > 0) {
  for (const f of result.parseFailures) {
    console.log(`  ${f.file}: ${f.error}`);
  }
}

// Summary stats
let totalModels = 0;
let totalFields = 0;
let totalEnums = 0;
for (const page of result.dataPages) {
  totalModels += page.models.length;
  totalFields += page.models.reduce((sum, m) => sum + m.fields.length, 0);
  totalEnums += page.enums.length;
}
console.log(
  `Total models: ${totalModels}, fields: ${totalFields}, enums: ${totalEnums}`
);
