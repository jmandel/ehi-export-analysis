#!/usr/bin/env bun
/**
 * extract-fhir-api.ts
 *
 * Parses the TriMed FHIR CapabilityStatement and OpenAPI spec to produce
 * structured JSON describing supported FHIR resources, search parameters,
 * and operations.
 *
 * Input:  ../fhir-capability-statement.json, ../swagger-api-spec.json
 * Output: fhir-resources.json, fhir-api-coverage.json
 */

import { readFileSync, writeFileSync } from "fs";
import { join, dirname } from "path";

const ROOT = dirname(new URL(import.meta.url).pathname);

// ── Parse CapabilityStatement ───────────────────────────────────────────

const csPath = join(ROOT, "..", "fhir-capability-statement.json");
const cs = JSON.parse(readFileSync(csPath, "utf-8"));

interface FhirResource {
  type: string;
  profile: string | null;
  interactions: string[];
  searchParams: { name: string; type: string }[];
}

const resources: FhirResource[] = [];

if (cs.rest) {
  for (const rest of cs.rest) {
    if (rest.resource) {
      for (const r of rest.resource) {
        resources.push({
          type: r.type,
          profile: r.profile || null,
          interactions: (r.interaction || []).map(
            (i: { code: string }) => i.code
          ),
          searchParams: (r.searchParam || []).map(
            (p: { name: string; type: string }) => ({
              name: p.name,
              type: p.type,
            })
          ),
        });
      }
    }
  }
}

// Bulk data support
const bulkOps: string[] = [];
if (cs.rest) {
  for (const rest of cs.rest) {
    if (rest.operation) {
      for (const op of rest.operation) {
        bulkOps.push(op.name);
      }
    }
  }
}

const fhirOutput = {
  source: "https://fhir.trimed.cloud/metadata",
  fhirVersion: cs.fhirVersion,
  software: cs.software,
  instantiates: cs.instantiates || [],
  formats: cs.format || [],
  securityScheme:
    cs.rest?.[0]?.security?.extension?.[0]?.extension?.find(
      (e: any) => e.url === "token"
    )?.valueUri || "OAuth2",
  resourceCount: resources.length,
  resources: resources.sort((a, b) => a.type.localeCompare(b.type)),
  systemOperations: bulkOps,
};

writeFileSync(
  join(ROOT, "fhir-resources.json"),
  JSON.stringify(fhirOutput, null, 2)
);

// ── Parse OpenAPI spec ──────────────────────────────────────────────────

const swaggerPath = join(ROOT, "..", "swagger-api-spec.json");
const swagger = JSON.parse(readFileSync(swaggerPath, "utf-8"));

const endpoints: {
  path: string;
  methods: string[];
  params: { name: string; in: string; type: string }[];
}[] = [];

for (const [path, methods] of Object.entries(swagger.paths || {})) {
  const methodNames: string[] = [];
  const params: { name: string; in: string; type: string }[] = [];

  for (const [method, spec] of Object.entries(methods as Record<string, any>)) {
    methodNames.push(method.toUpperCase());
    if (spec.parameters) {
      for (const p of spec.parameters) {
        params.push({
          name: p.name,
          in: p.in,
          type: p.schema?.type || "unknown",
        });
      }
    }
  }

  endpoints.push({ path, methods: methodNames, params });
}

const apiCoverage = {
  source: "https://fhir.trimed.cloud/swagger/v1/swagger.json",
  openApiVersion: swagger.openapi,
  title: swagger.info?.title,
  endpointCount: endpoints.length,
  uniqueResourcePaths: [
    ...new Set(endpoints.map((e) => e.path.split("/")[1]).filter(Boolean)),
  ].sort(),
  endpoints: endpoints.sort((a, b) => a.path.localeCompare(b.path)),
};

writeFileSync(
  join(ROOT, "fhir-api-coverage.json"),
  JSON.stringify(apiCoverage, null, 2)
);

// ── Summary ─────────────────────────────────────────────────────────────

console.log(`FHIR Resources: ${resources.length}`);
console.log(`Resource types: ${resources.map((r) => r.type).join(", ")}`);
console.log(`System operations: ${bulkOps.join(", ") || "none"}`);
console.log(`OpenAPI endpoints: ${endpoints.length}`);
console.log(
  `Unique resource paths: ${apiCoverage.uniqueResourcePaths.join(", ")}`
);
console.log(`Output: fhir-resources.json, fhir-api-coverage.json`);
