#!/usr/bin/env bun
/**
 * Extracts structured data from CharmHealth FHIR API documentation HTML.
 *
 * Parses the single-page API doc to extract:
 * - FHIR resources and their operations (list, get, search)
 * - Query/path parameters for each operation
 * - Sample request/response examples
 * - OAuth scopes
 * - Bulk export and CCDA API details
 */

import { readFileSync, writeFileSync } from "fs";
import { join } from "path";

const INPUT_FILE = join(import.meta.dir, "..", "fhir-api-documentation.html");
const OUTPUT_FILE = join(import.meta.dir, "fhir-api-extracted.json");

const html = readFileSync(INPUT_FILE, "utf-8");

// Simple HTML text extractor
function stripHtml(s: string): string {
  return s.replace(/<[^>]+>/g, " ").replace(/\s+/g, " ").trim();
}

// Extract text between two patterns
function extractBetween(content: string, startPattern: RegExp, endPattern: RegExp): string {
  const startMatch = content.match(startPattern);
  if (!startMatch) return "";
  const startIdx = startMatch.index! + startMatch[0].length;
  const rest = content.slice(startIdx);
  const endMatch = rest.match(endPattern);
  if (!endMatch) return rest;
  return rest.slice(0, endMatch.index);
}

// Parse table rows into array of objects
function parseTables(section: string): Array<Record<string, string>> {
  const rows: Array<Record<string, string>> = [];
  const tableMatch = section.match(/<table>([\s\S]*?)<\/table>/);
  if (!tableMatch) return rows;

  const tableHtml = tableMatch[1];

  // Extract headers
  const headerMatch = tableHtml.match(/<thead>([\s\S]*?)<\/thead>/);
  if (!headerMatch) return rows;

  const headers: string[] = [];
  const thRegex = /<th[^>]*>([\s\S]*?)<\/th>/g;
  let thMatch;
  while ((thMatch = thRegex.exec(headerMatch[1])) !== null) {
    headers.push(stripHtml(thMatch[1]).toLowerCase());
  }
  // Also check for <td> in thead (some tables use td for headers)
  if (headers.length === 0) {
    const tdRegex = /<td[^>]*>([\s\S]*?)<\/td>/g;
    let tdMatch;
    while ((tdMatch = tdRegex.exec(headerMatch[1])) !== null) {
      headers.push(stripHtml(tdMatch[1]).toLowerCase());
    }
  }

  // Extract body rows
  const bodyMatch = tableHtml.match(/<tbody>([\s\S]*?)<\/tbody>/);
  if (!bodyMatch) return rows;

  const trRegex = /<tr[^>]*>([\s\S]*?)<\/tr>/g;
  let trMatch;
  while ((trMatch = trRegex.exec(bodyMatch[1])) !== null) {
    const cells: string[] = [];
    const tdRegex2 = /<td[^>]*>([\s\S]*?)<\/td>/g;
    let tdMatch2;
    while ((tdMatch2 = tdRegex2.exec(trMatch[1])) !== null) {
      cells.push(stripHtml(tdMatch2[1]));
    }
    if (cells.length > 0 && headers.length > 0) {
      const row: Record<string, string> = {};
      headers.forEach((h, i) => {
        if (i < cells.length) row[h] = cells[i];
      });
      rows.push(row);
    }
  }

  return rows;
}

// Extract code blocks
function extractCodeBlocks(section: string): string[] {
  const blocks: string[] = [];
  const codeRegex = /<code[^>]*>([\s\S]*?)<\/code>/g;
  let match;
  while ((match = codeRegex.exec(section)) !== null) {
    const text = stripHtml(match[1]).trim();
    if (text.length > 10) blocks.push(text);
  }
  return blocks;
}

// Known FHIR resources from the page
const RESOURCE_NAMES = [
  "AllergyIntolerance", "Appointment", "CarePlan", "CareTeam", "Condition",
  "Device", "DiagnosticReport", "DocumentReference", "Encounter",
  "FamilyMemberHistory", "Goal", "Immunization", "Location",
  "MedicationAdministration", "MedicationRequest", "Medication",
  "Observation", "Organization", "Patient", "Practitioner", "Procedure",
  "Provenance", "QuestionnaireResponse", "RelatedPerson"
];

interface Operation {
  name: string;
  type: "list" | "get" | "search";
  apiUrl: string | null;
  parameters: Array<Record<string, string>>;
  requestExample: string | null;
  responseExample: string | null;
}

interface Resource {
  name: string;
  usCorProfile: string | null;
  description: string | null;
  operations: Operation[];
}

// Parse resources
const resources: Resource[] = [];

for (const resourceName of RESOURCE_NAMES) {
  const lowerName = resourceName.toLowerCase();

  // Find the resource header section
  const headerPattern = new RegExp(`<h1\\s+id="${lowerName}"[^>]*>[\\s\\S]*?</h1>`);
  const headerMatch = html.match(headerPattern);
  if (!headerMatch) continue;

  const headerIdx = headerMatch.index!;

  // Find description and US Core profile link
  const nextSection = html.slice(headerIdx, headerIdx + 2000);
  const descMatch = nextSection.match(/<p>([\s\S]*?)<\/p>/);
  const description = descMatch ? stripHtml(descMatch[1]) : null;

  const profileMatch = nextSection.match(/href="(http[^"]*us[/-]core[^"]*StructureDefinition[^"]*)"/i);
  const usCorProfile = profileMatch ? profileMatch[1] : null;

  // Find operations for this resource
  const operations: Operation[] = [];

  for (const opType of ["list", "get", "search"] as const) {
    const opId = `${opType}-${lowerName}`;
    const opPattern = new RegExp(`<h2\\s+id="${opId}"[^>]*>`);
    const opMatch = html.match(opPattern);
    if (!opMatch) continue;

    const opIdx = opMatch.index!;
    // Find the next h1 or h2 to delimit the section
    const opRest = html.slice(opIdx + opMatch[0].length);
    const nextHeadingMatch = opRest.match(/<h[12]\s/);
    const opSection = nextHeadingMatch
      ? opRest.slice(0, nextHeadingMatch.index)
      : opRest.slice(0, 5000);

    // Extract API URL
    const urlMatch = opSection.match(/<code>\s*((?:GET|POST|DELETE|PUT)\s+\/[^<]+)<\/code>/);
    const apiUrl = urlMatch ? stripHtml(urlMatch[1]) : null;

    // Extract parameters table
    const parameters = parseTables(opSection);

    // Extract code examples
    const codeBlocks = extractCodeBlocks(opSection);
    const requestExample = codeBlocks.find(b => b.includes("curl")) || null;
    const responseExample = codeBlocks.find(b => b.includes("resourceType") || b.includes("HTTP/1.1")) || null;

    operations.push({
      name: `${opType} ${resourceName}`,
      type: opType,
      apiUrl,
      parameters,
      requestExample,
      responseExample,
    });
  }

  // Special case for Medication which only has "get"
  if (resourceName === "Medication" && operations.length === 0) {
    const opPattern = /id="get-medication"/;
    const opMatch = html.match(opPattern);
    if (opMatch) {
      const opIdx = opMatch.index!;
      const opRest = html.slice(opIdx);
      const nextH = opRest.match(/<h[12]\s/);
      const opSection = nextH ? opRest.slice(0, nextH.index) : opRest.slice(0, 3000);

      const urlMatch = opSection.match(/<code>\s*(GET\s+\/[^<]+)<\/code>/);
      operations.push({
        name: "get Medication",
        type: "get",
        apiUrl: urlMatch ? stripHtml(urlMatch[1]) : null,
        parameters: parseTables(opSection),
        requestExample: null,
        responseExample: null,
      });
    }
  }

  resources.push({
    name: resourceName,
    usCorProfile,
    description,
    operations,
  });
}

// Extract OAuth scopes
const scopeSections = html.match(/<h3[^>]*id="patient-scope"[\s\S]*?<\/table>/);
const patientScopes = scopeSections ? parseTables(scopeSections[0]) : [];

const userScopeSections = html.match(/<h3[^>]*id="user-scope"[\s\S]*?<\/table>/);
const userScopes = userScopeSections ? parseTables(userScopeSections[0]) : [];

const systemScopeSections = html.match(/<h3[^>]*id="system-scope"[\s\S]*?<\/table>/);
const systemScopes = systemScopeSections ? parseTables(systemScopeSections[0]) : [];

// Extract Bulk Export info
const bulkExportSection = extractBetween(html, /<h1\s+id="bulk-export"/, /<\/div>\s*<div class="dark-box">/);
const bulkExportOps: { name: string; apiUrl: string | null; parameters: Array<Record<string, string>>; description: string | null }[] = [];

for (const op of [
  { id: "start-export", name: "Start Bulk Export" },
  { id: "get-status", name: "Get Bulk Export Status" },
  { id: "delete-export", name: "Delete Bulk Export Request" }
]) {
  const opPattern = new RegExp(`<h2\\s+id="${op.id}"[^>]*>`);
  const opMatch = html.match(opPattern);
  if (!opMatch) continue;

  const opIdx = opMatch.index!;
  const opRest = html.slice(opIdx + opMatch[0].length);
  const nextH = opRest.match(/<h[12]\s/);
  const opSection = nextH ? opRest.slice(0, nextH.index) : opRest.slice(0, 3000);

  const urlMatch = opSection.match(/<code>\s*((?:GET|POST|DELETE)\s+\/[^<]+)<\/code>/);
  const descMatch = opSection.match(/<p>([^<]*(?:export|Fetches|Deletes)[^<]*)<\/p>/i);

  bulkExportOps.push({
    name: op.name,
    apiUrl: urlMatch ? stripHtml(urlMatch[1]) : null,
    parameters: parseTables(opSection),
    description: descMatch ? stripHtml(descMatch[1]) : null,
  });
}

// Extract CCDA section
const ccdaSection = extractBetween(html, /<h1\s+id="ccda"/, /<h1\s+id="bulk-export"/);
const ccdaUrlMatch = ccdaSection.match(/<code>\s*(GET\s+\/[^<]+)<\/code>/);
const ccdaParams = parseTables(ccdaSection);

// Build output
const output = {
  source: "https://www.charmhealth.com/resources/fhir/index.html",
  extractionDate: new Date().toISOString().split("T")[0],
  fhirVersion: "4.0.1",
  baseUrl: "https://ehr2.charmtracker.com/api/ehr/v2/fhir",
  summary: {
    totalResources: resources.length,
    resourceNames: resources.map(r => r.name),
    totalOperations: resources.reduce((sum, r) => sum + r.operations.length, 0),
    resourcesWithUsCorProfile: resources.filter(r => r.usCorProfile).length,
  },
  resources,
  oauthScopes: {
    patient: patientScopes,
    user: userScopes,
    system: systemScopes,
  },
  bulkExport: {
    description: "Exports data of more than one resource of the group of patients in NDJSON format",
    operations: bulkExportOps,
  },
  ccda: {
    description: "Export medical records of a patient in HL7 CCDA format",
    apiUrl: ccdaUrlMatch ? stripHtml(ccdaUrlMatch[1]) : null,
    parameters: ccdaParams,
  },
  parsingStats: {
    inputFile: "fhir-api-documentation.html",
    inputSizeBytes: html.length,
    resourcesParsed: resources.length,
    resourcesExpected: RESOURCE_NAMES.length,
    parseFailures: RESOURCE_NAMES.filter(n => !resources.find(r => r.name === n)).map(n => ({
      resourceName: n,
      reason: "Header not found in HTML"
    })),
  }
};

writeFileSync(OUTPUT_FILE, JSON.stringify(output, null, 2));
console.log(`Extracted ${resources.length} resources with ${output.summary.totalOperations} operations`);
console.log(`Output written to: ${OUTPUT_FILE}`);
console.log(`Parse failures: ${output.parsingStats.parseFailures.length}`);
