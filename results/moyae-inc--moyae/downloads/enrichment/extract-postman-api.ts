#!/usr/bin/env bun
/**
 * Extracts structured data from the Moyae FHIR API Postman collection.
 *
 * Input:  ../moyae-fhir-api-postman-collection.json
 * Output: postman-api-summary.json — structured summary of all endpoints,
 *         resource types, operations, search parameters, and descriptions.
 */

import { readFileSync, writeFileSync } from "fs";
import { join, dirname } from "path";

const BASE = dirname(import.meta.path);
const INPUT = join(BASE, "..", "moyae-fhir-api-postman-collection.json");
const OUTPUT = join(BASE, "postman-api-summary.json");

interface PostmanItem {
  name: string;
  item?: PostmanItem[];
  request?: {
    method?: string;
    url?: string | { raw?: string };
    description?: string;
    header?: { key: string; value: string }[];
    auth?: { type: string };
  };
  response?: unknown[];
  description?: string;
}

interface EndpointSummary {
  name: string;
  method: string;
  url: string;
  hasDescription: boolean;
  descriptionSnippet: string;
  hasExampleResponse: boolean;
  headerKeys: string[];
  authType: string | null;
}

interface ResourceFolder {
  name: string;
  endpoints: EndpointSummary[];
  subfolders: ResourceFolder[];
}

function extractEndpoint(item: PostmanItem): EndpointSummary {
  const req = item.request ?? {};
  const method = (typeof req === "string" ? "?" : req.method) ?? "?";
  let url = "";
  if (typeof req !== "string") {
    if (typeof req.url === "string") url = req.url;
    else if (req.url && typeof req.url === "object") url = req.url.raw ?? "";
  }
  const desc = typeof req !== "string" ? req.description ?? "" : "";
  const headerKeys = (typeof req !== "string" ? req.header ?? [] : []).map(
    (h: any) => h.key
  );
  const authType =
    typeof req !== "string" && req.auth ? req.auth.type ?? null : null;
  const hasExampleResponse =
    Array.isArray(item.response) && item.response.length > 0;

  return {
    name: item.name,
    method,
    url,
    hasDescription: desc.length > 0,
    descriptionSnippet: desc.slice(0, 300),
    hasExampleResponse,
    headerKeys,
    authType,
  };
}

function extractFolder(item: PostmanItem): ResourceFolder {
  const folder: ResourceFolder = {
    name: item.name,
    endpoints: [],
    subfolders: [],
  };
  for (const child of item.item ?? []) {
    if (child.item) {
      folder.subfolders.push(extractFolder(child));
    } else {
      folder.endpoints.push(extractEndpoint(child));
    }
  }
  return folder;
}

// --- Main ---
const raw = JSON.parse(readFileSync(INPUT, "utf-8"));
const collectionName = raw.info?.name ?? "unknown";
const collectionDescription = raw.info?.description ?? "";

const topLevelFolders: ResourceFolder[] = [];
const standaloneEndpoints: EndpointSummary[] = [];

for (const item of raw.item ?? []) {
  if (item.item) {
    topLevelFolders.push(extractFolder(item));
  } else {
    standaloneEndpoints.push(extractEndpoint(item));
  }
}

// Derive resource type list
const resourceTypes = topLevelFolders
  .filter(
    (f) =>
      !["Authentication", "MFA", "Export", "CCDA"].includes(f.name) &&
      f.endpoints.length > 0
  )
  .map((f) => f.name);

// Count totals
let totalEndpoints = 0;
function countEndpoints(folders: ResourceFolder[]) {
  for (const f of folders) {
    totalEndpoints += f.endpoints.length;
    countEndpoints(f.subfolders);
  }
}
countEndpoints(topLevelFolders);
totalEndpoints += standaloneEndpoints.length;

const summary = {
  collectionName,
  collectionDescriptionLength: collectionDescription.length,
  totalTopLevelFolders: topLevelFolders.length,
  totalEndpoints,
  totalStandaloneEndpoints: standaloneEndpoints.length,
  resourceTypeFolders: resourceTypes.length,
  resourceTypes,
  exportEndpoints: topLevelFolders
    .filter((f) => f.name === "Export")
    .flatMap((f) => f.endpoints),
  ccdaEndpoints: topLevelFolders
    .filter((f) => f.name === "CCDA")
    .flatMap((f) => f.endpoints),
  folders: topLevelFolders,
  standaloneEndpoints,
};

writeFileSync(OUTPUT, JSON.stringify(summary, null, 2));
console.log(`Wrote ${OUTPUT}`);
console.log(`  Collection: ${collectionName}`);
console.log(`  Total folders: ${topLevelFolders.length}`);
console.log(`  Total endpoints: ${totalEndpoints}`);
console.log(`  Resource type folders: ${resourceTypes.length}`);
