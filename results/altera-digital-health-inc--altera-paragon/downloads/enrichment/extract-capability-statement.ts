#!/usr/bin/env bun
/**
 * Extracts structured data from the Paragon EHI Export CapabilityStatement.json
 * and Extension-Details.xlsx into queryable JSON.
 *
 * Usage: bun run extract-capability-statement.ts
 * Input: ../paragon-25-1/CapabilityStatement.json, ../paragon-25-1/Extension-Details.xlsx
 * Output: capability-statement-extracted.json, extension-details-extracted.json, coverage-summary.json
 */

import * as fs from "fs";
import * as path from "path";
import XLSX from "xlsx";

const BASE = path.resolve(__dirname, "..");
const CS_PATH = path.join(BASE, "paragon-25-1", "CapabilityStatement.json");
const EXT_PATH = path.join(BASE, "paragon-25-1", "Extension-Details.xlsx");

interface ExtractedResource {
  type: string;
  standardElements: string[];
  customExtensions: Array<{
    url: string;
    name: string;
    isCustom: boolean;
  }>;
  searchParams: Array<{ name: string; type: string }>;
  totalElements: number;
}

interface ExtensionDetail {
  resource: string;
  key: string;
  extensionName: string;
  definition: string;
}

// Extract CapabilityStatement
const cs = JSON.parse(fs.readFileSync(CS_PATH, "utf-8"));
const resources: ExtractedResource[] = [];

for (const resource of cs.rest[0].resource) {
  const rType = resource.type;
  const standardElements: string[] = [];
  const customExtensions: Array<{
    url: string;
    name: string;
    isCustom: boolean;
  }> = [];

  for (const ext of resource.extension || []) {
    const url: string = ext.url || "";
    const name: string = ext.valueString || "";
    const isCustom =
      url.includes("alterahealth.com") || url.includes("paragon");

    if (isCustom) {
      customExtensions.push({ url, name, isCustom: true });
    } else {
      standardElements.push(name);
    }
  }

  const searchParams = (resource.searchParam || []).map(
    (sp: { name: string; type: string }) => ({
      name: sp.name,
      type: sp.type,
    })
  );

  resources.push({
    type: rType,
    standardElements,
    customExtensions,
    searchParams,
    totalElements: standardElements.length + customExtensions.length,
  });
}

const csOutput = {
  sourceFile: "paragon-25-1/CapabilityStatement.json",
  fhirVersion: cs.fhirVersion,
  title: cs.title,
  name: cs.name,
  description: cs.description,
  totalResources: resources.length,
  resources,
  summary: {
    resourceTypes: resources.map((r) => r.type),
    totalStandardElements: resources.reduce(
      (s, r) => s + r.standardElements.length,
      0
    ),
    totalCustomExtensions: resources.reduce(
      (s, r) => s + r.customExtensions.length,
      0
    ),
    resourcesWithCustomExtensions: resources
      .filter((r) => r.customExtensions.length > 0)
      .map((r) => ({
        type: r.type,
        customExtensionCount: r.customExtensions.length,
      })),
  },
};

fs.writeFileSync(
  path.join(__dirname, "capability-statement-extracted.json"),
  JSON.stringify(csOutput, null, 2)
);
console.log(
  `Extracted ${resources.length} resources from CapabilityStatement`
);

// Extract Extension Details
const wb = XLSX.readFile(EXT_PATH);
const ws = wb.Sheets[wb.SheetNames[0]];
const rows = XLSX.utils.sheet_to_json<{
  Resource: string;
  Key: string;
  Extension: string;
  Definition: string;
}>(ws);

const extensions: ExtensionDetail[] = rows.map((row) => ({
  resource: row.Resource || "",
  key: row.Key || "",
  extensionName: row.Extension || "",
  definition: row.Definition || "",
}));

const extByResource: Record<string, ExtensionDetail[]> = {};
for (const ext of extensions) {
  if (!extByResource[ext.resource]) extByResource[ext.resource] = [];
  extByResource[ext.resource].push(ext);
}

const extOutput = {
  sourceFile: "paragon-25-1/Extension-Details.xlsx",
  totalExtensions: extensions.length,
  resourcesWithExtensions: Object.keys(extByResource).length,
  extensionsByResource: extByResource,
};

fs.writeFileSync(
  path.join(__dirname, "extension-details-extracted.json"),
  JSON.stringify(extOutput, null, 2)
);
console.log(`Extracted ${extensions.length} extension definitions`);

// Coverage summary
const coverageSummary = {
  extractionDate: new Date().toISOString(),
  sources: {
    capabilityStatement: CS_PATH,
    extensionDetails: EXT_PATH,
  },
  fhirVersion: cs.fhirVersion,
  exportFormat: "FHIR R4 NDJSON (via Bulk Data-style export)",
  totalResourceTypes: resources.length,
  resourceTypes: resources.map((r) => ({
    type: r.type,
    standardElementCount: r.standardElements.length,
    customExtensionCount: r.customExtensions.length,
    totalFields: r.totalElements,
  })),
  dataDomainMapping: {
    clinical: [
      "AllergyIntolerance",
      "Condition",
      "Procedure",
      "Observation",
      "DiagnosticReport",
      "CarePlan",
      "CareTeam",
      "Goal",
      "Immunization",
      "MedicationRequest",
      "MedicationAdministration",
      "MedicationDispense",
      "MedicationStatement",
      "Medication",
      "FamilyMemberHistory",
      "NutritionOrder",
      "ServiceRequest",
      "Communication",
      "CommunicationRequest",
      "DetectedIssue",
      "GuidanceResponse",
      "Consent",
    ],
    billing: [
      "Account",
      "Claim",
      "ChargeItem",
      "ChargeItemDefinition",
      "Coverage",
      "CoverageEligibilityRequest",
      "CoverageEligibilityResponse",
      "PaymentNotice",
      "PaymentReconciliation",
    ],
    patient: ["Patient", "RelatedPerson", "Person"],
    encounter: ["Encounter", "Appointment", "AppointmentResponse"],
    documents: ["DocumentReference", "Media"],
    imaging: ["ImagingStudy"],
    lab: ["Specimen", "DiagnosticReport", "Observation"],
    infrastructure: [
      "Device",
      "Endpoint",
      "Location",
      "Organization",
      "Practitioner",
      "PractitionerRole",
      "BodyStructure",
    ],
  },
  parsing: {
    totalFilesParsed: 2,
    totalFilesDiscovered: 2,
    failures: [],
  },
};

fs.writeFileSync(
  path.join(__dirname, "coverage-summary.json"),
  JSON.stringify(coverageSummary, null, 2)
);
console.log("Coverage summary written");
console.log("\nDone. Output files:");
console.log("  - capability-statement-extracted.json");
console.log("  - extension-details-extracted.json");
console.log("  - coverage-summary.json");
