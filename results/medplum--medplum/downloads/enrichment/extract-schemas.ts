/**
 * extract-schemas.ts
 *
 * Extracts resource type schemas from the Medplum CapabilityStatement and OpenAPI spec
 * into a queryable JSON format.
 *
 * Input:
 *   - ../capability-statement.json  (FHIR CapabilityStatement)
 *   - ../openapi.json               (OpenAPI 3.1 spec)
 *
 * Output:
 *   - resources.json   (all resource types with fields, search params, interactions)
 *   - coverage.json    (accounting: parse stats and coverage info)
 */

import { readFileSync, writeFileSync } from "fs";
import { join } from "path";

const downloadsDir = join(import.meta.dir, "..");

// Load inputs
const cs = JSON.parse(
  readFileSync(join(downloadsDir, "capability-statement.json"), "utf-8")
);
const oa = JSON.parse(
  readFileSync(join(downloadsDir, "openapi.json"), "utf-8")
);

interface FieldDef {
  name: string;
  type: string;
  description: string;
  isArray: boolean;
  required: boolean;
}

interface SearchParamDef {
  name: string;
  type: string;
  documentation?: string;
}

interface ResourceDef {
  resourceType: string;
  description: string;
  fields: FieldDef[];
  searchParams: SearchParamDef[];
  interactions: string[];
  inPatientCompartment: boolean;
  patientCompartmentParams: string[];
  sourceUrl: string;
}

// FHIR R4 Patient Compartment definition
// Resources that have a search parameter linking to Patient
// Source: https://hl7.org/fhir/R4/compartmentdefinition-patient.html
const patientCompartmentMap: Record<string, string[]> = {
  Account: ["subject"],
  AdverseEvent: ["subject"],
  AllergyIntolerance: ["patient", "recorder", "asserter"],
  Appointment: ["actor"],
  AppointmentResponse: ["actor"],
  AuditEvent: ["patient"],
  Basic: ["patient", "author"],
  BodyStructure: ["patient"],
  CarePlan: ["patient", "performer"],
  CareTeam: ["patient", "participant"],
  ChargeItem: ["subject"],
  Claim: ["patient", "payee"],
  ClaimResponse: ["patient"],
  ClinicalImpression: ["subject"],
  Communication: ["subject", "sender", "recipient"],
  CommunicationRequest: ["subject", "sender", "recipient", "requester"],
  Composition: ["subject", "author", "attester"],
  Condition: ["patient", "asserter"],
  Consent: ["patient"],
  Coverage: ["policy-holder", "subscriber", "beneficiary", "payor"],
  CoverageEligibilityRequest: ["patient"],
  CoverageEligibilityResponse: ["patient"],
  DetectedIssue: ["patient"],
  DeviceRequest: ["subject", "performer"],
  DeviceUseStatement: ["subject"],
  DiagnosticReport: ["subject"],
  DocumentManifest: ["subject", "author", "recipient"],
  DocumentReference: ["subject", "author"],
  Encounter: ["patient"],
  EnrollmentRequest: ["subject"],
  EpisodeOfCare: ["patient"],
  ExplanationOfBenefit: ["patient", "payee"],
  FamilyMemberHistory: ["patient"],
  Flag: ["patient"],
  Goal: ["patient"],
  Group: ["member"],
  GuidanceResponse: ["patient"],
  ImagingStudy: ["patient"],
  Immunization: ["patient"],
  ImmunizationEvaluation: ["patient"],
  ImmunizationRecommendation: ["patient"],
  Invoice: ["subject", "patient", "recipient"],
  List: ["subject", "source"],
  MeasureReport: ["patient"],
  Media: ["subject"],
  MedicationAdministration: ["patient", "performer", "subject"],
  MedicationDispense: ["subject", "patient", "receiver"],
  MedicationRequest: ["subject"],
  MedicationStatement: ["subject"],
  MolecularSequence: ["patient"],
  NutritionOrder: ["patient"],
  Observation: ["subject", "performer"],
  Patient: ["{def}"],
  Person: ["patient"],
  Procedure: ["patient", "performer"],
  Provenance: ["patient"],
  QuestionnaireResponse: ["subject", "author"],
  RelatedPerson: ["patient"],
  RequestGroup: ["subject", "participant"],
  ResearchSubject: ["individual"],
  RiskAssessment: ["subject"],
  Schedule: ["actor"],
  ServiceRequest: ["subject", "performer"],
  Specimen: ["subject"],
  SupplyDelivery: ["patient"],
  SupplyRequest: ["requester"],
  Task: ["owner", "requester"],
  VisionPrescription: ["patient"],
};

// Extract from CapabilityStatement
const restResources = cs.rest?.[0]?.resource ?? [];
const csResourceMap = new Map<
  string,
  { interactions: string[]; searchParams: SearchParamDef[] }
>();

for (const r of restResources) {
  csResourceMap.set(r.type, {
    interactions: (r.interaction ?? []).map((i: any) => i.code),
    searchParams: (r.searchParam ?? []).map((sp: any) => ({
      name: sp.name,
      type: sp.type,
      documentation: sp.documentation,
    })),
  });
}

// Extract from OpenAPI schemas
const schemas = oa.components?.schemas ?? {};
const resources: ResourceDef[] = [];
let parseFailures: { name: string; reason: string }[] = [];

for (const [name, schema] of Object.entries(schemas) as [string, any][]) {
  // Only process top-level resource types (have "resourceType" property or are in CapabilityStatement)
  if (!schema.properties?.resourceType && !csResourceMap.has(name)) {
    continue;
  }

  try {
    const fields: FieldDef[] = [];
    const properties = schema.properties ?? {};
    const required = new Set(schema.required ?? []);

    for (const [fieldName, fieldSchema] of Object.entries(properties) as [
      string,
      any,
    ][]) {
      if (fieldName === "resourceType") continue;

      const isArray = fieldSchema.type === "array";
      const itemSchema = isArray ? fieldSchema.items ?? {} : fieldSchema;
      let type = itemSchema.$ref
        ? itemSchema.$ref.replace("#/components/schemas/", "")
        : itemSchema.type ?? "unknown";

      // Handle oneOf / anyOf
      if (itemSchema.oneOf || itemSchema.anyOf) {
        const options = (itemSchema.oneOf || itemSchema.anyOf) as any[];
        type = options
          .map((o: any) =>
            o.$ref ? o.$ref.replace("#/components/schemas/", "") : o.type
          )
          .join(" | ");
      }

      fields.push({
        name: fieldName,
        type,
        description: fieldSchema.description ?? "",
        isArray,
        required: required.has(fieldName),
      });
    }

    const csData = csResourceMap.get(name);
    const compartmentParams = patientCompartmentMap[name] ?? [];

    resources.push({
      resourceType: name,
      description: schema.description ?? "",
      fields,
      searchParams: csData?.searchParams ?? [],
      interactions: csData?.interactions ?? [],
      inPatientCompartment: compartmentParams.length > 0,
      patientCompartmentParams: compartmentParams,
      sourceUrl: `https://www.medplum.com/docs/api/fhir/resources/${name.toLowerCase()}`,
    });
  } catch (e: any) {
    parseFailures.push({ name, reason: e.message });
  }
}

// Sort by resource type name
resources.sort((a, b) => a.resourceType.localeCompare(b.resourceType));

// Write resources.json
writeFileSync(
  join(import.meta.dir, "resources.json"),
  JSON.stringify(resources, null, 2)
);

// Coverage stats
const totalSchemas = Object.keys(schemas).length;
const totalCapabilityResources = restResources.length;
const totalExtracted = resources.length;
const inCompartment = resources.filter((r) => r.inPatientCompartment).length;
const withInteractions = resources.filter(
  (r) => r.interactions.length > 0
).length;

const coverage = {
  extraction_date: new Date().toISOString(),
  source_files: {
    capability_statement: {
      path: "../capability-statement.json",
      fhir_version: cs.fhirVersion,
      server_version: cs.version,
      total_resource_types: totalCapabilityResources,
    },
    openapi_spec: {
      path: "../openapi.json",
      openapi_version: oa.openapi,
      total_schemas: totalSchemas,
      total_paths: Object.keys(oa.paths ?? {}).length,
    },
  },
  results: {
    total_resource_types_extracted: totalExtracted,
    in_patient_compartment: inCompartment,
    with_server_interactions: withInteractions,
    parse_failures: parseFailures.length,
    parse_failure_details: parseFailures,
  },
  patient_compartment_resources: resources
    .filter((r) => r.inPatientCompartment)
    .map((r) => ({
      resourceType: r.resourceType,
      compartmentParams: r.patientCompartmentParams,
      fieldCount: r.fields.length,
    })),
};

writeFileSync(
  join(import.meta.dir, "coverage.json"),
  JSON.stringify(coverage, null, 2)
);

console.log(`Extracted ${totalExtracted} resource types`);
console.log(`  - In Patient Compartment: ${inCompartment}`);
console.log(`  - With server interactions: ${withInteractions}`);
console.log(`  - Parse failures: ${parseFailures.length}`);
console.log("Output: resources.json, coverage.json");
