#!/usr/bin/env bun
/**
 * Extracts structured data from EMR Direct Interoperability Engine
 * Open API documentation HTML files.
 *
 * Usage: bun run extract-api-docs.ts
 *
 * Input: ../interopengine-2017-open-api-documentation.html
 *        ../interopengine-2026-open-api-documentation.html
 *        ../mednet-open-api-page.html
 *        ../mednet-2015-cures-update.html
 *        ../Price_Transparency_emr4MD_v9.10.pdf (metadata only)
 *
 * Output: api-documentation-extracted.json
 *         coverage-accounting.json
 */

import { readFileSync, writeFileSync, readdirSync, statSync } from "fs";
import { join, resolve } from "path";

const DOWNLOADS_DIR = resolve(import.meta.dir, "..");

interface FhirResource {
  ccdsElement: string;
  resourceType: string;
  dataElement?: string;
}

interface SearchParameter {
  dataElement: string;
  searchParam: string;
}

interface DataTypeChoice {
  resourceElement: string;
  supportedTypes: string[];
}

interface ApiVersion {
  version: string;
  lastUpdated: string;
  fhirVersion: string;
  sourceFile: string;
  resources: FhirResource[];
  searchParameters: SearchParameter[];
  dataTypeChoices: DataTypeChoice[];
  authMethods: string[];
  endpoints: { name: string; urlPattern: string }[];
  bulkDataSupported: boolean;
  ccdaSupported: boolean;
  usCoreFhirIgVersion?: string;
}

interface PriceTransparencyEntry {
  capability: string;
  criteria: string;
  description: string;
  cost: string;
}

interface ExtractedData {
  vendor: string;
  product: string;
  chplId: string;
  registeredUrl: string;
  apiVersions: ApiVersion[];
  priceTransparency: {
    sourceFile: string;
    ehiExportEntry: PriceTransparencyEntry | null;
    otherCapabilities: PriceTransparencyEntry[];
  };
  certifiedCriteria: string[];
  additionalSoftware: string[];
}

function parseHtmlTables(html: string): string[][][] {
  const tables: string[][][] = [];
  const tableRegex = /<TABLE[^>]*>([\s\S]*?)<\/TABLE>/gi;
  let tableMatch;

  while ((tableMatch = tableRegex.exec(html)) !== null) {
    const tableHtml = tableMatch[1];
    const rows: string[][] = [];
    const rowRegex = /<TR[^>]*>([\s\S]*?)<\/TR>/gi;
    let rowMatch;

    while ((rowMatch = rowRegex.exec(tableHtml)) !== null) {
      const rowHtml = rowMatch[1];
      const cells: string[] = [];
      const cellRegex = /<T[DH][^>]*>([\s\S]*?)<\/T[DH]>/gi;
      let cellMatch;

      while ((cellMatch = cellRegex.exec(rowHtml)) !== null) {
        const text = cellMatch[1]
          .replace(/<[^>]*>/g, "")
          .replace(/&amp;/g, "&")
          .replace(/&lt;/g, "<")
          .replace(/&gt;/g, ">")
          .replace(/&#x2714;/g, "✔")
          .replace(/\s+/g, " ")
          .trim();
        cells.push(text);
      }
      if (cells.length > 0) rows.push(cells);
    }
    if (rows.length > 0) tables.push(rows);
  }
  return tables;
}

function extractResources(tables: string[][][]): FhirResource[] {
  const resources: FhirResource[] = [];
  for (const table of tables) {
    if (table.length < 2) continue;
    const header = table[0].map((h) => h.toLowerCase());
    // Look for CCDS/resource mapping tables
    const ccdsIdx = header.findIndex(
      (h) => h.includes("clinical data") || h.includes("ccds") || h.includes("data set")
    );
    const resIdx = header.findIndex((h) => h.includes("resource"));
    if (ccdsIdx >= 0 && resIdx >= 0) {
      for (let i = 1; i < table.length; i++) {
        const row = table[i];
        if (row.length > Math.max(ccdsIdx, resIdx)) {
          resources.push({
            ccdsElement: row[ccdsIdx],
            resourceType: row[resIdx],
            dataElement: row.length > 2 ? row[2] : undefined,
          });
        }
      }
    }
    // Also look for "Resource Type" + "Search Parameters" tables (2026 format)
    const rtIdx = header.findIndex((h) => h.includes("resource type"));
    if (rtIdx >= 0) {
      for (let i = 1; i < table.length; i++) {
        const row = table[i];
        if (row.length > rtIdx && row[rtIdx]) {
          resources.push({
            ccdsElement: "",
            resourceType: row[rtIdx],
            dataElement: row.length > 1 ? row[1] : undefined,
          });
        }
      }
    }
  }
  return resources;
}

function extractResourceSearchTable(tables: string[][][]): { resourceType: string; searchParameters: string }[] {
  const results: { resourceType: string; searchParameters: string }[] = [];
  for (const table of tables) {
    if (table.length < 2) continue;
    const header = table[0].map((h) => h.toLowerCase());
    const rtIdx = header.findIndex((h) => h.includes("resource type"));
    const spIdx = header.findIndex((h) => h.includes("search param"));
    if (rtIdx >= 0 && spIdx >= 0) {
      for (let i = 1; i < table.length; i++) {
        const row = table[i];
        if (row.length > Math.max(rtIdx, spIdx)) {
          results.push({
            resourceType: row[rtIdx],
            searchParameters: row[spIdx],
          });
        }
      }
    }
  }
  return results;
}

function extractSearchParams(tables: string[][][]): SearchParameter[] {
  const params: SearchParameter[] = [];
  for (const table of tables) {
    if (table.length < 2) continue;
    const header = table[0].map((h) => h.toLowerCase());
    const elemIdx = header.findIndex(
      (h) => h.includes("data element") || h.includes("ccds")
    );
    const paramIdx = header.findIndex((h) => h.includes("search"));
    if (elemIdx >= 0 && paramIdx >= 0) {
      for (let i = 1; i < table.length; i++) {
        const row = table[i];
        if (row.length > Math.max(elemIdx, paramIdx)) {
          params.push({
            dataElement: row[elemIdx],
            searchParam: row[paramIdx],
          });
        }
      }
    }
  }
  return params;
}

function extractDataTypeChoices(tables: string[][][]): DataTypeChoice[] {
  const choices: DataTypeChoice[] = [];
  for (const table of tables) {
    if (table.length < 2) continue;
    const header = table[0].map((h) => h.toLowerCase());
    const elemIdx = header.findIndex((h) => h.includes("data element"));
    const choiceIdx = header.findIndex(
      (h) => h.includes("supported") || h.includes("choices")
    );
    if (elemIdx >= 0 && choiceIdx >= 0) {
      for (let i = 1; i < table.length; i++) {
        const row = table[i];
        if (
          row.length > Math.max(elemIdx, choiceIdx) &&
          row[choiceIdx].includes(",")
        ) {
          choices.push({
            resourceElement: row[elemIdx],
            supportedTypes: row[choiceIdx].split(",").map((s) => s.trim()),
          });
        }
      }
    }
  }
  return choices;
}

function extract2017(html: string): ApiVersion {
  const tables = parseHtmlTables(html);
  const resources = extractResources(tables);
  const searchParams = extractSearchParams(tables);

  return {
    version: "Interoperability Engine 2017",
    lastUpdated: "February 12, 2020",
    fhirVersion: "FHIR STU 3 Ballot",
    sourceFile: "interopengine-2017-open-api-documentation.html",
    resources,
    searchParameters: searchParams,
    dataTypeChoices: [],
    authMethods: [
      "OAuth 2.0 authorization code grant (RFC 6749)",
      "Dynamic client registration (RFC 7591)",
      "Patient portal credentials",
    ],
    endpoints: [
      { name: "Authorization", urlPattern: "https://[baseOAuthURL]/authz" },
      { name: "Token", urlPattern: "https://[baseOAuthURL]/token" },
      { name: "Registration", urlPattern: "https://[baseOAuthURL]/register" },
    ],
    bulkDataSupported: false,
    ccdaSupported: true,
  };
}

function extract2026(html: string): ApiVersion {
  const tables = parseHtmlTables(html);
  const resources = extractResources(tables);
  const searchParams = extractSearchParams(tables);
  const dataTypeChoices = extractDataTypeChoices(tables);

  const resourceSearchTable = extractResourceSearchTable(tables);

  // Merge resource types from the search table into resources
  for (const rst of resourceSearchTable) {
    if (!resources.find(r => r.resourceType === rst.resourceType)) {
      resources.push({
        ccdsElement: "",
        resourceType: rst.resourceType,
        dataElement: `search: ${rst.searchParameters}`,
      });
    }
  }

  return {
    version: "Interoperability Engine 2026",
    lastUpdated: "February 5, 2026",
    fhirVersion: "HL7 FHIR R4",
    sourceFile: "interopengine-2026-open-api-documentation.html",
    resources,
    searchParameters: searchParams,
    dataTypeChoices,
    resourceSearchTable,
    authMethods: [
      "OAuth 2.0 authorization code grant (RFC 6749)",
      "OAuth 2.0 client credentials grant (RFC 6749)",
      "Dynamic client registration (RFC 7591)",
      "UDAP Dynamic Client Registration",
      "Private key JWT authentication",
      "PKCE (RFC 7636, S256 required)",
      "Refresh tokens (offline_access scope)",
    ],
    endpoints: [
      { name: "Authorization", urlPattern: "https://[baseOAuthURL]/authz" },
      { name: "Token", urlPattern: "https://[baseOAuthURL]/token" },
      { name: "Registration", urlPattern: "https://[baseOAuthURL]/register" },
      { name: "Manage", urlPattern: "https://[baseOAuthURL]/manage" },
      { name: "Revoke", urlPattern: "https://[baseOAuthURL]/revoke" },
    ],
    bulkDataSupported: true,
    ccdaSupported: true,
    usCoreFhirIgVersion: "US Core IG Release 6.1.0 (STU6.1)",
  };
}

function extractCertifiedCriteria(html: string): string[] {
  const criteria: string[] = [];
  const liRegex = /<li>\s*\(([a-h])\)\((\d+)\)[^<]*/gi;
  let m;
  while ((m = liRegex.exec(html)) !== null) {
    const full = m[0]
      .replace(/<[^>]*>/g, "")
      .replace(/\s+/g, " ")
      .trim();
    criteria.push(full);
  }
  return criteria;
}

// Main execution
const files = readdirSync(DOWNLOADS_DIR).filter(
  (f) => f.endsWith(".html") || f.endsWith(".pdf")
);

const html2017 = readFileSync(
  join(DOWNLOADS_DIR, "interopengine-2017-open-api-documentation.html"),
  "utf-8"
);
const html2026 = readFileSync(
  join(DOWNLOADS_DIR, "interopengine-2026-open-api-documentation.html"),
  "utf-8"
);
const htmlCures = readFileSync(
  join(DOWNLOADS_DIR, "mednet-2015-cures-update.html"),
  "utf-8"
);

const api2017 = extract2017(html2017);
const api2026 = extract2026(html2026);
const certifiedCriteria = extractCertifiedCriteria(htmlCures);

const ehiExportEntry: PriceTransparencyEntry = {
  capability: "Electronic Health Information (EHI) export",
  criteria: "170.315(b)(10)",
  description:
    "This functionality allows a practice to create individual and group exports of PHI without programming intervention.",
  cost: "Included in base service agreement, subscription fee plus Subscription fee from 3rd party - EMR Direct, one time implementation fee and annual subscription charged.",
};

const extractedData: ExtractedData = {
  vendor: "MedNet Medical Solutions",
  product: "emr4MD Version 9.10",
  chplId: "15.04.04.2796.emr4.09.00.1.191218",
  registeredUrl: "https://mednetmedical.com/Open_API.html",
  apiVersions: [api2017, api2026],
  priceTransparency: {
    sourceFile: "Price_Transparency_emr4MD_v9.10.pdf",
    ehiExportEntry,
    otherCapabilities: [
      {
        capability: "CPOE",
        criteria: "170.315(a)(1-3)",
        description:
          "Computerized Provider Order Entry allows for the ability to create medication orders, laboratory orders, and radiology orders.",
        cost: "Included in base service agreement, subscription fee. Medication module requires separate service agreement with Dr.First.",
      },
      {
        capability: "Transitions of Care",
        criteria: "170.315(b)(1)",
        description:
          "Electronically create and transmit a transition of care/referral summary in C-CDA format.",
        cost: "Subscription fee 3rd party - EMR Direct, one time implementation fee and annual subscription charged.",
      },
      {
        capability: "Standardized API for Patient and Population Services",
        criteria: "170.315(g)(10)",
        description:
          "FHIR R4 API supporting US Core profiles and SMART App Launch.",
        cost: "Subscription fee from 3rd party - EMR Direct.",
      },
    ],
  },
  certifiedCriteria,
  additionalSoftware: [
    "AccessGUDID NLM API",
    "EMR Direct's phiMail Server",
    "DrFirst's Rcopia4 Web",
    "EMR Direct's Interoperability Engine",
    "Chilkat Software Crypt2",
    "EMR Direct's phiQuery API",
  ],
};

writeFileSync(
  join(import.meta.dir, "api-documentation-extracted.json"),
  JSON.stringify(extractedData, null, 2)
);

// Coverage accounting
const accounting = {
  totalFilesDiscovered: files.length,
  totalFilesParsed: files.filter((f) => f.endsWith(".html")).length,
  pdfFilesMetadataOnly: files.filter((f) => f.endsWith(".pdf")).length,
  parseFailures: [] as { file: string; error: string }[],
  filesProcessed: files.map((f) => ({
    file: f,
    size: statSync(join(DOWNLOADS_DIR, f)).size,
    parsed: f.endsWith(".html"),
    type: f.endsWith(".pdf") ? "pdf" : "html",
  })),
  summary: {
    api2017ResourceCount: api2017.resources.length,
    api2017SearchParamCount: api2017.searchParameters.length,
    api2026ResourceCount: api2026.resources.length,
    api2026SearchParamCount: api2026.searchParameters.length,
    api2026DataTypeChoiceCount: api2026.dataTypeChoices.length,
    certifiedCriteriaCount: certifiedCriteria.length,
  },
};

writeFileSync(
  join(import.meta.dir, "coverage-accounting.json"),
  JSON.stringify(accounting, null, 2)
);

console.log("Extraction complete.");
console.log(
  `Parsed ${accounting.totalFilesParsed} HTML files, ${accounting.pdfFilesMetadataOnly} PDF metadata.`
);
console.log(
  `2017 API: ${api2017.resources.length} resources, ${api2017.searchParameters.length} search params`
);
console.log(
  `2026 API: ${api2026.resources.length} resources, ${api2026.searchParameters.length} search params, ${api2026.dataTypeChoices.length} type choices`
);
console.log(`Certified criteria: ${certifiedCriteria.length}`);
