#!/usr/bin/env bun
/**
 * Extracts key facts from the iPatientCare EHI export documentation
 * into a queryable JSON structure.
 *
 * Input: ../fhir-capability-statement.json, ../smart-configuration.json, ../fhir-endpoints-bundle.json
 * Output: ./export-summary.json
 */

import { readFileSync, writeFileSync } from "fs";
import { join, dirname } from "path";

const base = join(dirname(import.meta.path), "..");

// Parse CapabilityStatement
const capStmt = JSON.parse(readFileSync(join(base, "fhir-capability-statement.json"), "utf-8"));
const resources = capStmt.rest?.[0]?.resource?.map((r: any) => ({
  type: r.type,
  profiles: r.supportedProfile ?? [],
  interactions: r.interaction?.map((i: any) => i.code) ?? [],
  searchParams: r.searchParam?.map((p: any) => ({ name: p.name, type: p.type })) ?? [],
})) ?? [];

// Parse SMART config
const smartConfig = JSON.parse(readFileSync(join(base, "smart-configuration.json"), "utf-8"));

// Parse FHIR endpoints bundle
const endpointsBundle = JSON.parse(readFileSync(join(base, "fhir-endpoints-bundle.json"), "utf-8"));
const endpoints = endpointsBundle.entry
  ?.filter((e: any) => e.resource?.resourceType === "Endpoint")
  ?.map((e: any) => ({
    name: e.resource.name,
    status: e.resource.status,
    address: e.resource.address,
    tenantId: e.resource.header?.[0]?.replace("X-FHIR-TENANT-ID ", ""),
  })) ?? [];

const organizations = endpointsBundle.entry
  ?.filter((e: any) => e.resource?.resourceType === "Organization")
  ?.map((e: any) => ({
    name: e.resource.name,
    active: e.resource.active,
    npi: e.resource.identifier?.find((i: any) => i.system?.includes("us-npi"))?.value,
    city: e.resource.address?.[0]?.city,
    state: e.resource.address?.[0]?.state,
  })) ?? [];

const summary = {
  vendor: "AssureCare LLC",
  product: "iPatientCare",
  versions: ["18.0", "22.5", "23.0"],
  ehi_export: {
    documented_formats: [
      {
        format: "C-CDA XML",
        standard: "HL7 CDA R2 Consolidated CDA",
        uscdi_version: "v1",
        scope: "single_patient_and_population",
      },
      {
        format: "FHIR R4 Bulk Data",
        standard: "HL7 FHIR US Core STU 3.1.1",
        fhir_version: "4.0.1",
        scope: "single_patient_and_population",
      },
    ],
    documentation_pages: 3,
    has_data_dictionary: false,
    has_export_instructions: false,
    has_sample_data: false,
    has_schema: false,
    has_field_definitions: false,
  },
  fhir_server: {
    base_url: "https://fhir.ipatientcare.net:9443/fhirserver/fhir/",
    fhir_version: capStmt.fhirVersion,
    implementation_description: capStmt.implementation?.description,
    instantiates: capStmt.instantiates,
    resource_types: resources,
    resource_type_count: resources.length,
    smart_capabilities: smartConfig.capabilities,
    grant_types: smartConfig.grant_types_supported,
    auth_endpoint: smartConfig.authorization_endpoint,
    token_endpoint: smartConfig.token_endpoint,
  },
  tenant_summary: {
    total_endpoints: endpoints.length,
    total_organizations: organizations.length,
    active_endpoints: endpoints.filter((e: any) => e.status === "active").length,
    active_organizations: organizations.filter((o: any) => o.active).length,
    states_represented: [...new Set(organizations.map((o: any) => o.state).filter(Boolean))].sort(),
    organizations,
  },
  coverage_assessment: {
    covered_domains: [
      "demographics",
      "problems_conditions",
      "medications",
      "allergies",
      "lab_results",
      "vital_signs",
      "immunizations",
      "procedures",
      "care_plans",
      "clinical_notes",
      "implantable_devices",
      "goals",
      "smoking_status",
      "insurance_coverage",
      "encounters",
      "provenance",
    ],
    likely_missing_domains: [
      "billing_claims_charges",
      "payment_posting_remittances",
      "accounts_receivable",
      "denial_management",
      "e_prescribing_workflow",
      "scanned_documents_attachments",
      "secure_messages",
      "specialty_clinical_data",
      "referral_management",
      "quality_measures_mips",
      "telehealth_metadata",
      "revenue_cycle_data",
      "custom_templates_assessments",
    ],
    assessment: "Classic (b)(10) vs (g)(10) confusion. Export covers only USCDI clinical data via C-CDA and FHIR US Core, missing billing, specialty, and operational patient data.",
  },
};

writeFileSync(
  join(dirname(import.meta.path), "export-summary.json"),
  JSON.stringify(summary, null, 2)
);

console.log(`Wrote export-summary.json`);
console.log(`  FHIR resource types: ${resources.length}`);
console.log(`  Tenant endpoints: ${endpoints.length}`);
console.log(`  Organizations: ${organizations.length}`);
