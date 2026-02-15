#!/usr/bin/env bun
/**
 * Extract structured API documentation from Medi-EHR's Swagger UI HTML.
 *
 * Input:  ../API_Document.html  (pre-rendered Swagger UI page)
 * Output: api-docs.json          (structured API endpoints, parameters, responses)
 *
 * Run:  cd results/medi-ehr-llc/downloads/enrichment && bun run extract-api-docs.ts
 */

import { readFileSync, writeFileSync } from "fs";
import { join } from "path";

const inputPath = join(__dirname, "..", "API_Document.html");
const outputPath = join(__dirname, "api-docs.json");

const html = readFileSync(inputPath, "utf-8");

interface Parameter {
  name: string;
  type: string;
  required: boolean;
  description: string;
}

interface Endpoint {
  method: string;
  path: string;
  summary: string;
  contentType: string;
  parameters: Parameter[];
  responseSections: string[];
  responseFormat: string;
}

interface ApiDoc {
  title: string;
  version: string;
  description: string;
  serverUrl: string;
  endpoints: Endpoint[];
  errorCodes: { code: string; text: string }[];
  extractedFrom: string;
  extractionDate: string;
}

// Extract title
const titleMatch = html.match(/<h2 class="title">\s*(?:<!--[^>]*-->)?\s*([^<]+)/);
const title = titleMatch ? titleMatch[1].trim() : "Unknown";

// Extract server URL
const serverMatch = html.match(
  /<option value="(https:\/\/proda\.mediemr\.net[^"]+)">/
);
const serverUrl = serverMatch ? serverMatch[1] : "Unknown";

// Extract endpoints by finding opblock sections
const endpoints: Endpoint[] = [];

// Pattern: find each operation block
const opblockPattern =
  /<div class="opblock opblock-post is-open"[^>]*id="[^"]*">([\s\S]*?)(?=<div class="opblock opblock-post is-open"|<\/span>\s*<\/div>\s*<\/div>\s*<\/span>\s*$)/g;

// Simpler approach: find each endpoint by its button label
const endpointMatches = html.matchAll(
  /<button[^>]*aria-label="(post)\s+[^"]*"[^>]*>[\s\S]*?<span class="medi-php-endpoint">\u200B\/([^<]+)<\/span>[\s\S]*?<div class="opblock-summary-description">([^<]+)<\/div>/g
);

const endpointPaths: string[] = [];
for (const m of endpointMatches) {
  endpointPaths.push(m[2]);
}

// Deduplicate: we have mediehrlogintest.php, mediehrgetpatient.php, mediehrrotatetokens.php, mediehrgetpatientdata.php
const uniquePaths = [...new Set(endpointPaths)];

// Now extract parameters for each endpoint section
// Split HTML by operation blocks
const sections = html.split(
  /(?=<div class="opblock opblock-post is-open")/
);

for (const section of sections) {
  // Get endpoint path
  const pathMatch = section.match(
    /<span class="medi-php-endpoint">\u200B\/([^<]+)<\/span>/
  );
  if (!pathMatch) continue;

  const path = "/" + pathMatch[1];

  // Get summary
  const summaryMatch = section.match(
    /<div class="opblock-summary-description">([^<]+)<\/div>/
  );
  const summary = summaryMatch ? summaryMatch[1].trim() : "";

  // Extract parameters from table rows
  const params: Parameter[] = [];
  const paramMatches = section.matchAll(
    /<tr class="parameters" data-property-name="([^"]+)">[\s\S]*?<div class="parameter__name">\s*(?:<!--[^>]*-->)?\s*([^<\n]+?)(?:\s*<!--[^>]*-->)?\s*<\/div>\s*<div class="parameter__type">\s*(?:<!--[^>]*-->)?\s*(\w+)/g
  );

  for (const pm of paramMatches) {
    const name = pm[1].trim();
    const displayName = pm[2].trim();
    const type = pm[3].trim();
    const required = displayName.endsWith("*");

    // Find description for this parameter
    const descPattern = new RegExp(
      `data-property-name="${name}"[\\s\\S]*?<div class="renderedMarkdown">\\s*<p>([^<]+)</p>`,
      "m"
    );
    const descMatch = section.match(descPattern);
    const description = descMatch ? descMatch[1].trim() : "";

    params.push({
      name,
      type,
      required,
      description,
    });
  }

  // Detect response format
  let responseFormat = "unknown";
  if (section.includes("ClinicalDocument")) {
    responseFormat = "C-CDA 2.1 XML";
  } else if (section.includes("<tokens>")) {
    responseFormat = "XML (tokens)";
  } else if (section.includes("<patient>")) {
    responseFormat = "XML (patient demographics)";
  } else if (section.includes("Logged In")) {
    responseFormat = "Success/Error status";
  }

  // Extract C-CDA section names if present
  const responseSections: string[] = [];
  if (path.includes("getpatientdata")) {
    const sectionNames = [
      "Allergies",
      "Medications",
      "Problems",
      "Encounters",
      "Immunizations",
      "Vitals",
      "Social History",
      "Procedures",
      "Labs",
      "Implantable Devices",
      "Goals",
      "Functional Status",
      "Cognitive Status",
      "Referrals",
      "Assessment",
      "Care Team",
      "Health Concerns",
      "Plan of Treatment",
      "Diagnostic and Imaging Reports",
    ];
    responseSections.push(...sectionNames);
  }

  endpoints.push({
    method: "POST",
    path,
    summary,
    contentType: "multipart/form-data",
    parameters: params,
    responseSections,
    responseFormat,
  });
}

// Extract error codes table
const errorCodes: { code: string; text: string }[] = [];
const errorTableMatch = html.match(
  /<table[^>]*id="medi-error-table"[^>]*>([\s\S]*?)<\/table>/
);
if (errorTableMatch) {
  const rows = errorTableMatch[1].matchAll(
    /<tr>\s*<td[^>]*>(\d+)<\/td>\s*<td[^>]*>([\s\S]*?)<\/td>\s*<\/tr>/g
  );
  for (const row of rows) {
    errorCodes.push({ code: row[1], text: row[2].replace(/\s+/g, ' ').trim() });
  }
}
if (errorCodes.length === 0) {
  // Fallback: hardcode from manual inspection
  const errorPairs = [
    { code: "10", text: "Internal Error occured" },
    { code: "20", text: "Username or email not correct for the given office" },
    {
      code: "30",
      text: "Error Invalid Login - Access and Refresh tokens Removed",
    },
    {
      code: "40",
      text: "Either the FirstName or LastName or MRN or SSN required",
    },
    { code: "50", text: "No patients found with the given details" },
    {
      code: "60",
      text: "More than one patients found with the given information please include some more details to narrow down the search",
    },
    { code: "70", text: "Start date is required" },
    { code: "90", text: "Patient MRN is required" },
  ];
  errorCodes.push(...errorPairs);
}

// Deduplicate endpoints (the token rotate endpoint appears twice in the HTML)
const deduped: Endpoint[] = [];
const seenPaths = new Set<string>();
for (const ep of endpoints) {
  // Use path + summary as key to handle the duplicate mediehrrotatetokens block
  // that is actually mediehrgetpatientdata
  const key = ep.path + "|" + ep.summary;
  if (!seenPaths.has(key)) {
    seenPaths.add(key);
    deduped.push(ep);
  }
}

const apiDoc: ApiDoc = {
  title,
  version: title.match(/v([\d.]+)/)?.[1] || "2.1",
  description:
    "MediEHR Patient Access API - proprietary REST API for patient data retrieval in C-CDA 2.1 format",
  serverUrl,
  endpoints: deduped,
  errorCodes,
  extractedFrom: "API_Document.html",
  extractionDate: new Date().toISOString().split("T")[0],
};

writeFileSync(outputPath, JSON.stringify(apiDoc, null, 2));

// Print summary
console.log("=== Extraction Summary ===");
console.log(`Title: ${apiDoc.title}`);
console.log(`Server: ${apiDoc.serverUrl}`);
console.log(`Endpoints found: ${deduped.length}`);
for (const ep of deduped) {
  console.log(
    `  ${ep.method} ${ep.path} — ${ep.summary} (${ep.parameters.length} params)`
  );
}
console.log(`Error codes: ${errorCodes.length}`);
console.log(`Output: ${outputPath}`);
