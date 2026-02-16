#!/usr/bin/env bun
/**
 * Extracts structured data from the Moyae FHIR CapabilityStatement.
 *
 * Input:  ../fhir-capability-statement.json
 * Output: capability-statement-summary.json — structured summary of
 *         supported resources, search parameters, operations, and security.
 */

import { readFileSync, writeFileSync } from "fs";
import { join, dirname } from "path";

const BASE = dirname(import.meta.path);
const INPUT = join(BASE, "..", "fhir-capability-statement.json");
const OUTPUT = join(BASE, "capability-statement-summary.json");

const raw = JSON.parse(readFileSync(INPUT, "utf-8"));

interface ResourceEntry {
  type: string;
  interactions: string[];
  searchParams: { name: string; type: string; documentation: string }[];
  versioning: string;
}

const rest = raw.rest?.[0] ?? {};
const resources: ResourceEntry[] = (rest.resource ?? []).map((r: any) => ({
  type: r.type,
  interactions: (r.interaction ?? []).map((i: any) => i.code),
  searchParams: (r.searchParam ?? []).map((sp: any) => ({
    name: sp.name,
    type: sp.type,
    documentation: sp.documentation ?? "",
  })),
  versioning: r.versioning ?? "unknown",
}));

const operations = (rest.operation ?? []).map((op: any) => ({
  name: op.name,
  definition: op.definition,
}));

const systemInteractions = (rest.interaction ?? []).map(
  (i: any) => i.code
);

const security = rest.security ?? {};
const securityServices = (security.service ?? []).flatMap((s: any) =>
  (s.coding ?? []).map((c: any) => c.code)
);

const smartExtension = (security.extension ?? []).find(
  (e: any) => e.url?.includes("oauth-uris")
);
const oauthUris: Record<string, string> = {};
if (smartExtension) {
  for (const ext of smartExtension.extension ?? []) {
    oauthUris[ext.url] = ext.valueUri;
  }
}

// Categorize resources by clinical relevance
const clinicalResources = resources.filter((r) =>
  [
    "Patient",
    "Condition",
    "Observation",
    "Procedure",
    "MedicationRequest",
    "MedicationStatement",
    "MedicationAdministration",
    "MedicationDispense",
    "AllergyIntolerance",
    "Immunization",
    "DiagnosticReport",
    "CarePlan",
    "CareTeam",
    "Goal",
    "Encounter",
    "DocumentReference",
    "Composition",
    "FamilyMemberHistory",
    "VisionPrescription",
    "ImagingStudy",
    "Media",
    "Device",
    "DeviceUseStatement",
    "Questionnaire",
    "QuestionnaireResponse",
    "ClinicalImpression",
    "RiskAssessment",
    "NutritionOrder",
    "Specimen",
    "Communication",
  ].includes(r.type)
);

const financialResources = resources.filter((r) =>
  [
    "Claim",
    "ClaimResponse",
    "ExplanationOfBenefit",
    "Coverage",
    "Account",
    "ChargeItem",
    "Invoice",
    "PaymentNotice",
    "PaymentReconciliation",
    "EnrollmentRequest",
    "EnrollmentResponse",
    "InsurancePlan",
  ].includes(r.type)
);

const adminResources = resources.filter((r) =>
  [
    "Organization",
    "Practitioner",
    "PractitionerRole",
    "Location",
    "HealthcareService",
    "RelatedPerson",
    "Person",
    "Endpoint",
    "Schedule",
    "Slot",
    "Appointment",
    "AppointmentResponse",
  ].includes(r.type)
);

const summary = {
  serverInfo: {
    name: raw.software?.name,
    version: raw.software?.version,
    fhirVersion: raw.fhirVersion,
    publisher: raw.publisher,
    formats: raw.format,
    date: raw.date,
  },
  security: {
    services: securityServices,
    oauthUris,
    cors: security.cors,
  },
  operations,
  systemInteractions,
  totalResourceTypes: resources.length,
  resourcesByCategory: {
    clinical: clinicalResources.map((r) => r.type),
    financial: financialResources.map((r) => r.type),
    administrative: adminResources.map((r) => r.type),
    other: resources
      .filter(
        (r) =>
          !clinicalResources.includes(r) &&
          !financialResources.includes(r) &&
          !adminResources.includes(r)
      )
      .map((r) => r.type),
  },
  resourceTypeCounts: {
    clinical: clinicalResources.length,
    financial: financialResources.length,
    administrative: adminResources.length,
    other:
      resources.length -
      clinicalResources.length -
      financialResources.length -
      adminResources.length,
  },
  resources,
};

writeFileSync(OUTPUT, JSON.stringify(summary, null, 2));
console.log(`Wrote ${OUTPUT}`);
console.log(`  FHIR version: ${raw.fhirVersion}`);
console.log(`  Total resource types: ${resources.length}`);
console.log(
  `  Clinical: ${clinicalResources.length}, Financial: ${financialResources.length}, Admin: ${adminResources.length}`
);
console.log(`  Operations: ${operations.map((o: any) => o.name).join(", ")}`);
