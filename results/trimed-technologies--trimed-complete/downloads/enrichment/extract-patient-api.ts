#!/usr/bin/env bun
/**
 * extract-patient-api.ts
 *
 * Parses the TriMed Patient Data API single-page HTML documentation and
 * extracts structured JSON for every API method: request parameters,
 * response parameters, underlying SQL, and sample XML bodies.
 *
 * Input:  ../patientapi-homepage.html
 * Output: patient-api-methods.json, patient-api-database-schema.json
 */

import { readFileSync, writeFileSync } from "fs";
import { join, dirname } from "path";

const ROOT = dirname(new URL(import.meta.url).pathname);
const INPUT = join(ROOT, "..", "patientapi-homepage.html");
const html = readFileSync(INPUT, "utf-8");

// ── helpers ──────────────────────────────────────────────────────────────

function textOf(fragment: string): string {
  return fragment
    .replace(/<[^>]+>/g, " ")
    .replace(/&lt;/g, "<")
    .replace(/&gt;/g, ">")
    .replace(/&amp;/g, "&")
    .replace(/&quot;/g, '"')
    .replace(/&#39;/g, "'")
    .replace(/\s+/g, " ")
    .trim();
}

interface Param {
  name: string;
  type: string;
  required?: string;
  description: string;
}

interface ApiMethod {
  id: string;
  name: string;
  endpoint: string;
  httpVerb: string;
  requestParams: Param[];
  responseParams: Param[];
  responseCodes: { code: string; meaning: string }[];
  sampleRequestXml: string | null;
  sampleResponseUrl: string | null;
  underlyingSql: string | null;
}

// ── parse sections ──────────────────────────────────────────────────────

// Identify all div sections by id
const sectionIds = [
  "divPatLookup",
  "divGetPatientData",
  "divGetPatientAllergy",
  "divGetPatientProblemList",
  "divGetPatientMedication",
  "divGetPatientImmunization",
  "divGetPatientLabResult",
  "divGetPatientEncounter",
  "divGetPatientEncompassingEncounter",
  "divGetPatientVitals",
];

const methods: ApiMethod[] = [];
const dbTables = new Set<string>();
const dbColumns: Record<string, Set<string>> = {};

for (const sectionId of sectionIds) {
  const startPattern = `id="${sectionId}"`;
  const startIdx = html.indexOf(startPattern);
  if (startIdx === -1) continue;

  // Find the end of this section (next sibling div or end)
  const sectionStart = html.lastIndexOf("<div", startIdx);
  let depth = 0;
  let pos = sectionStart;
  let sectionEnd = html.length;
  const tag = /<\/?div[\s>]/gi;
  tag.lastIndex = pos;
  let match;
  while ((match = tag.exec(html))) {
    if (match[0].startsWith("</")) {
      depth--;
      if (depth === 0) {
        sectionEnd = match.index + match[0].length;
        break;
      }
    } else {
      depth++;
    }
  }
  const sectionHtml = html.slice(sectionStart, sectionEnd);

  // Extract method name from heading
  const nameMatch = sectionHtml.match(/<h1[^>]*>(.*?)<\/h1>/is);
  const methodName = nameMatch ? textOf(nameMatch[1]) : sectionId.replace("div", "");

  // Extract sample request XML
  const xmlMatch = sectionHtml.match(
    /<code[^>]*class="[^"]*xml[^"]*"[^>]*>([\s\S]*?)<\/code>/i
  );
  let sampleXml: string | null = null;
  if (xmlMatch) {
    sampleXml = textOf(xmlMatch[1]).trim();
  } else {
    // Try pre tag
    const preMatch = sectionHtml.match(
      /Sample Request[\s\S]*?<pre[^>]*>([\s\S]*?)<\/pre>/i
    );
    if (preMatch) sampleXml = textOf(preMatch[1]).trim();
  }

  // Extract request parameters table
  const reqParams: Param[] = [];
  const reqTableMatch = sectionHtml.match(
    /Request Parameters[\s\S]*?<table[^>]*>([\s\S]*?)<\/table>/i
  );
  if (reqTableMatch) {
    const rows = reqTableMatch[1].match(/<tr[^>]*>([\s\S]*?)<\/tr>/gi) || [];
    for (const row of rows.slice(1)) {
      // skip header
      const cells = (row.match(/<td[^>]*>([\s\S]*?)<\/td>/gi) || []).map((c) =>
        textOf(c)
      );
      if (cells.length >= 3) {
        reqParams.push({
          name: cells[0],
          type: cells[1],
          required: cells[2] || undefined,
          description: cells[3] || "",
        });
      }
    }
  }

  // Extract response codes
  const resCodes: { code: string; meaning: string }[] = [];
  const resCodeMatch = sectionHtml.match(
    /Response [Cc]odes[\s\S]*?<table[^>]*>([\s\S]*?)<\/table>/i
  );
  if (resCodeMatch) {
    const rows = resCodeMatch[1].match(/<tr[^>]*>([\s\S]*?)<\/tr>/gi) || [];
    for (const row of rows.slice(1)) {
      const cells = (row.match(/<td[^>]*>([\s\S]*?)<\/td>/gi) || []).map((c) =>
        textOf(c)
      );
      if (cells.length >= 2) {
        resCodes.push({ code: cells[0], meaning: cells[1] });
      }
    }
  }

  // Extract response parameters table
  const resParams: Param[] = [];
  const resTableMatch = sectionHtml.match(
    /Response Parameters[\s\S]*?<table[^>]*>([\s\S]*?)<\/table>/i
  );
  if (resTableMatch) {
    const rows = resTableMatch[1].match(/<tr[^>]*>([\s\S]*?)<\/tr>/gi) || [];
    for (const row of rows.slice(1)) {
      const cells = (row.match(/<td[^>]*>([\s\S]*?)<\/td>/gi) || []).map((c) =>
        textOf(c)
      );
      if (cells.length >= 2) {
        resParams.push({
          name: cells[0],
          type: cells[1],
          description: cells[2] || "",
        });
      }
    }
  }

  // Extract sample response URL
  const sampleRespMatch = sectionHtml.match(
    /Click to view Sample Response[\s\S]*?href="([^"]+)"/i
  );
  const sampleResponseUrl = sampleRespMatch ? sampleRespMatch[1] : null;

  // Extract underlying SQL
  let underlyingSql: string | null = null;
  // Find the SQL section with id ending in "Query"
  const queryDivId = sectionId.replace("div", "div") + "Query";
  const queryIdx = html.indexOf(`id="${queryDivId}"`);
  if (queryIdx !== -1) {
    const sqlStart = html.indexOf("Underlying SQL", queryIdx);
    if (sqlStart !== -1) {
      const codeStart = html.indexOf("<code", sqlStart);
      const codeEnd = html.indexOf("</code>", codeStart);
      if (codeStart !== -1 && codeEnd !== -1) {
        underlyingSql = textOf(html.slice(codeStart, codeEnd)).trim();
      }
    }
  }
  // Fallback: look in section itself
  if (!underlyingSql) {
    const sqlInSection = sectionHtml.match(
      /Underlying SQL[\s\S]*?<code[^>]*>([\s\S]*?)<\/code>/i
    );
    if (sqlInSection) {
      underlyingSql = textOf(sqlInSection[1]).trim();
    }
  }

  // Parse SQL for table and column names
  if (underlyingSql) {
    // Extract table names from FROM/JOIN clauses
    const fromMatches = underlyingSql.match(
      /(?:FROM|JOIN)\s+(pr1_\w+)/gi
    );
    if (fromMatches) {
      for (const m of fromMatches) {
        const tbl = m.replace(/(?:FROM|JOIN)\s+/i, "").trim();
        dbTables.add(tbl);
        if (!dbColumns[tbl]) dbColumns[tbl] = new Set();
      }
    }

    // Extract column references (table.column patterns)
    const colMatches = underlyingSql.match(
      /(\w+)\.(\w+)/g
    );
    if (colMatches) {
      for (const m of colMatches) {
        const [alias, col] = m.split(".");
        // Map aliases to table names based on FROM clause
        const aliasMap: Record<string, string> = {};
        const aliasMatches = underlyingSql.match(
          /(pr1_\w+)\s+(\w)(?:\s|,|$)/gi
        );
        if (aliasMatches) {
          for (const am of aliasMatches) {
            const parts = am.trim().split(/\s+/);
            if (parts.length >= 2) {
              aliasMap[parts[1].replace(/,/, "")] = parts[0];
            }
          }
        }
        const tableName = aliasMap[alias] || alias;
        if (tableName.startsWith("pr1_") || tableName.startsWith("PR1_")) {
          if (!dbColumns[tableName]) dbColumns[tableName] = new Set();
          dbColumns[tableName].add(col);
        }
      }
    }
  }

  methods.push({
    id: sectionId,
    name: methodName,
    endpoint: "https://svcs-ccd.trimed.cloud/PatientAPI.asmx",
    httpVerb: "POST",
    requestParams: reqParams,
    responseParams: resParams,
    responseCodes: resCodes,
    sampleRequestXml: sampleXml,
    sampleResponseUrl,
    underlyingSql,
  });
}

// ── build database schema from SQL ──────────────────────────────────────

const dbSchema = Object.fromEntries(
  [...dbTables].sort().map((table) => [
    table,
    [...(dbColumns[table] || [])].sort(),
  ])
);

// ── write outputs ───────────────────────────────────────────────────────

const apiOutput = {
  source: "https://patientapi.trimedtech.com/",
  apiVersion: "1.3",
  format: "SOAP/XML returning C-CDA",
  baseEndpoint: "https://svcs-ccd.trimed.cloud/PatientAPI.asmx",
  methodCount: methods.length,
  methods,
};

writeFileSync(
  join(ROOT, "patient-api-methods.json"),
  JSON.stringify(apiOutput, null, 2)
);

const schemaOutput = {
  source: "Underlying SQL queries from Patient Data API documentation",
  note: "These table and column names were extracted from SQL queries embedded in the API documentation. They represent a partial view of the database schema — only tables/columns used in the API's data retrieval are visible.",
  tableCount: Object.keys(dbSchema).length,
  tables: dbSchema,
};

writeFileSync(
  join(ROOT, "patient-api-database-schema.json"),
  JSON.stringify(schemaOutput, null, 2)
);

// ── summary ─────────────────────────────────────────────────────────────

console.log(`Parsed ${methods.length} API methods`);
console.log(
  `Extracted ${Object.keys(dbSchema).length} database tables from SQL`
);
console.log(`Output: patient-api-methods.json, patient-api-database-schema.json`);

const parseFailures: string[] = [];
for (const id of sectionIds) {
  if (!methods.find((m) => m.id === id)) {
    parseFailures.push(id);
  }
}
if (parseFailures.length > 0) {
  console.log(`Parse failures: ${parseFailures.join(", ")}`);
}

console.log("\n=== Coverage ===");
console.log(`Total section IDs targeted: ${sectionIds.length}`);
console.log(`Total sections parsed: ${methods.length}`);
console.log(`Parse failures: ${parseFailures.length}`);
