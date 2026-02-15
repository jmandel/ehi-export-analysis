# Medplum — EHI Export Documentation

Collected: 2026-02-15

## Source
- Registered URL: https://www.medplum.com/docs/api/fhir/operations/patient-everything
- CHPL ID: 11745
- CHPL Product Number: 15.04.04.3147.Medp.05.03.1.251231
- Certification Date: 2025-12-31
- Product: Medplum, Version 5

## Navigation Journal

### Step 1: Probe the registered URL

```bash
curl -sI -L "https://www.medplum.com/docs/api/fhir/operations/patient-everything" \
  -H 'User-Agent: Mozilla/5.0'
```

Result: HTTP 200, Content-Type `text/html; charset=utf-8`, 59,472 bytes. The URL resolves directly to a Docusaurus-powered documentation page titled "Patient $everything | Medplum". No redirects.

### Step 2: Examine the page content

The page documents the FHIR `$patient-everything` operation. Key content:
- Endpoint: `[base]/R4/Patient/<id>/$everything`
- Parameters: `start`, `end`, `_since`, `_count`, `_offset`, `_type`
- Output: a FHIR Bundle containing all resources in the Patient Compartment
- Explicit statement: *"The FHIR Bundle created from this operation is the supported machine readable Electronic Health Information Export (EHI) format for Medplum."*

### Step 3: Check the ONC compliance page

```bash
curl -sL "https://www.medplum.com/docs/compliance/onc" -H 'User-Agent: Mozilla/5.0'
```

The ONC compliance page lists certified criteria. The b(10) row reads "Electronic Health Information Export (Cures Update)" and links directly to the `$patient-everything` documentation page. This confirms the registered URL is the authoritative EHI export documentation.

### Step 4: Download machine-readable API artifacts

```bash
# CapabilityStatement (313 KB)
curl -sL "https://api.medplum.com/fhir/R4/metadata" \
  -H 'Accept: application/fhir+json' \
  -o capability-statement.json

# OpenAPI 3.1 spec (2.6 MB)
curl -sL "https://api.medplum.com/openapi.json" \
  -o openapi.json
```

Both endpoints are unauthenticated and publicly accessible. The CapabilityStatement reports FHIR version 4.0.1, server version 5.0.14, and lists 146 supported resource types. The OpenAPI spec contains 737 schemas with complete field definitions.

### Step 5: Download FHIR resource documentation

The Medplum documentation site (Docusaurus) contains 146 individual resource type pages, 41 data type pages, and 35 operations pages. URLs were extracted from the sitemap at `https://www.medplum.com/sitemap.xml` and downloaded in bulk:

```bash
# Example: download all 146 resource documentation pages
while IFS= read -r url; do
    filename=$(basename "$url")
    curl -sL "$url" -H 'User-Agent: Mozilla/5.0' \
      -o "fhir-resources/${filename}.html"
done < resource-urls.txt
```

### Step 6: Download source code for `$patient-everything` implementation

Since Medplum is open source (Apache 2.0), the implementation source was retrieved from GitHub:

```bash
curl -sL "https://raw.githubusercontent.com/medplum/medplum/main/packages/server/src/fhir/operations/patienteverything.ts" \
  -o patienteverything.ts
```

This provides authoritative detail on exactly what the export includes and how reference resolution works.

### Step 7: Download documentation markdown sources

```bash
curl -sL "https://raw.githubusercontent.com/medplum/medplum/main/packages/docs/docs/api/fhir/operations/patient-everything.md" \
  -o patient-everything.md
curl -sL "https://raw.githubusercontent.com/medplum/medplum/main/packages/docs/docs/compliance/onc.md" \
  -o onc-compliance.md
curl -sL "https://raw.githubusercontent.com/medplum/medplum/main/packages/docs/docs/api/fhir/operations/bulk-fhir.mdx" \
  -o bulk-fhir-api.md
```

### Step 8: Screenshots

Full-page screenshots were captured of the Patient $everything page and the ONC Certification page using a browser.

### Step 9: Enrichment

Two Bun TypeScript scripts were created to extract structured JSON from the downloaded artifacts:
- `extract-schemas.ts`: Parses the CapabilityStatement and OpenAPI spec into a unified `resources.json` with 165 resource types, 4006 fields, and Patient Compartment mapping.
- `extract-html-docs.ts`: Parses HTML pages for metadata. (Note: field-level tables are rendered client-side by Docusaurus React components, so the OpenAPI-derived data is the authoritative source.)

## What Was Found

### EHI Export Mechanism

Medplum's EHI export is the FHIR `$patient-everything` operation. This is a standard FHIR operation that returns a Bundle containing all resources in the Patient Compartment for a given patient, plus referenced resources (Organizations, Practitioners, PractitionerRoles, Locations, Medications, Devices).

The export is invoked via:
```
GET [base]/R4/Patient/<id>/$everything
```

The output is a **FHIR R4 JSON Bundle** — the documentation explicitly states this is "the supported machine readable Electronic Health Information Export (EHI) format for Medplum."

### What the Export Includes

The export returns all resources in the FHIR R4 Patient Compartment. Based on analysis of the source code (`patienteverything.ts`) and the CapabilityStatement, this includes **68 resource types** that can be linked to a patient:

**Clinical data resources:**
- Patient demographics
- AllergyIntolerance, Condition (diagnoses/problems)
- Observation (vitals, labs, clinical observations)
- DiagnosticReport (lab reports, imaging reports)
- Procedure, ServiceRequest
- MedicationRequest, MedicationAdministration, MedicationDispense, MedicationStatement
- Immunization, ImmunizationEvaluation, ImmunizationRecommendation
- CarePlan, CareTeam, Goal
- Encounter, EpisodeOfCare
- FamilyMemberHistory
- ClinicalImpression
- NutritionOrder
- Composition (clinical documents)
- DocumentReference, DocumentManifest
- Media (images, attachments)
- ImagingStudy
- Specimen
- BodyStructure
- MolecularSequence
- QuestionnaireResponse

**Administrative/financial resources:**
- Account, ChargeItem
- Claim, ClaimResponse, ExplanationOfBenefit
- Coverage, CoverageEligibilityRequest, CoverageEligibilityResponse
- EnrollmentRequest
- Invoice
- Consent, Contract
- Appointment, AppointmentResponse, Schedule
- Communication, CommunicationRequest
- Flag, DetectedIssue
- Task, RequestGroup

**Additionally resolved references (not in compartment but included for completeness):**
- Organization
- Practitioner, PractitionerRole
- Location
- Medication
- Device

The implementation recursively walks all references in compartment resources and resolves references to these six additional resource types, ensuring complete context.

### Bulk Export (Alternative Mechanism)

Medplum also supports the FHIR Bulk Data API 2.0.0 (`/fhir/R4/$export` and `/fhir/R4/Group/<id>/$export`), which exports data in NDJSON format. While not explicitly designated as the b(10) mechanism (that's `$patient-everything`), the system-level `$export` can export all FHIR resources in a Project, which is effectively a superset. The Bulk FHIR API page includes complete Python code examples for performing the export.

### Data Dictionary

Medplum's data dictionary is the FHIR R4 specification itself. Because Medplum is "FHIR-native" (it stores data in FHIR format), the schema for every resource type is the standard FHIR R4 schema plus any Medplum-specific extensions. The documentation site provides per-resource pages with:
- Element definitions (name, type, required, description) for all fields
- Search parameters with FHIRPath expressions
- Inherited elements from base Resource/DomainResource
- Links to US Core profiles where applicable

The OpenAPI spec at `https://api.medplum.com/openapi.json` (2.6 MB) provides machine-readable schema definitions for all 737 types (resources + data types + backbone elements).

## Export Coverage Assessment

### Data Domain Coverage

Medplum is a FHIR-native platform — its data model IS FHIR R4. Unlike traditional EHRs where the export might only cover a subset of the internal data model, Medplum's export mechanism returns everything in the Patient Compartment because the Patient Compartment IS the internal storage model. This is a fundamental architectural advantage for EHI completeness.

**Clearly covered domains:**
- Demographics (Patient resource)
- Diagnoses/problems (Condition)
- Medications (MedicationRequest, MedicationAdministration, MedicationDispense, MedicationStatement)
- Lab results/observations (Observation, DiagnosticReport)
- Vital signs (Observation)
- Allergies (AllergyIntolerance)
- Immunizations (Immunization)
- Procedures (Procedure)
- Clinical notes (Composition, DocumentReference)
- Care plans (CarePlan, Goal, CareTeam)
- Encounters/visits (Encounter, EpisodeOfCare)
- Family history (FamilyMemberHistory)
- Imaging (ImagingStudy, Media)
- Questionnaire/assessment responses (QuestionnaireResponse)
- Insurance/coverage (Coverage, CoverageEligibilityRequest/Response)
- Billing/claims (Claim, ClaimResponse, ExplanationOfBenefit, ChargeItem, Account, Invoice)
- Appointments/scheduling (Appointment, AppointmentResponse, Schedule)
- Communications (Communication, CommunicationRequest)
- Consent records (Consent)
- Documents and attachments (DocumentReference, Binary — though Binary is excluded from compartment search by default per the source code)
- Implantable devices (DeviceUseStatement, Device — resolved via references)

**Key nuance — platform vs. product:**
Because Medplum is a platform (headless EHR), the actual data stored varies entirely by deployment. A pediatric telehealth deployment will have different resource types populated than a radiology deployment. The export mechanism is complete in the sense that it exports *everything the deployment has stored* for a patient, but what's stored depends on how the customer built their application.

**Potential gap — Binary resources:**
The source code explicitly excludes `Binary` from compartment search (`r.code === 'Binary' ? undefined : r.code`). Binary resources hold raw file data (PDFs, images, DICOM). If clinical documents are stored as Binary + DocumentReference, the DocumentReference would be exported but the actual binary content might not be, depending on how references are resolved. This is a minor concern — the reference resolution code would include them if they're referenced by a resource in the compartment through one of the six allowed reference types, but it depends on the reference chain.

**Not applicable (not a gap):**
- Specialty-specific clinical data: Medplum handles this through FHIR extensions and Questionnaire/QuestionnaireResponse, which are included in the export
- Custom assessments: Captured as QuestionnaireResponse, included
- E-prescribing data: Flows through DoseSpot integration but medication data stored in Medplum as MedicationRequest resources, included

### Export Format & Standards

- **Format**: FHIR R4 JSON Bundle (for `$patient-everything`); NDJSON (for Bulk FHIR API)
- **Standard**: HL7 FHIR R4 (4.0.1) — the recognized international standard for healthcare interoperability
- **Profiles**: The documentation references US Core STU 5.0.1 profiles (adopted via SVAP for g(10)), but the export is not limited to US Core resource types — it includes the full Patient Compartment
- **Schema**: Fully defined in the OpenAPI 3.1 spec (737 schemas) and CapabilityStatement (146 resource types)

This is an appropriate format. Since Medplum's internal data model IS FHIR, the export is lossless — there is no transformation or lossy conversion from an internal format to the export format. A third party with FHIR knowledge could reconstruct the complete patient record from the exported Bundle.

### Documentation Quality

**Strengths:**
- Clear, developer-oriented documentation written for a technical audience
- The `$patient-everything` page is concise and actionable — it tells you the endpoint, parameters, and output format
- Complete machine-readable artifacts: CapabilityStatement (313 KB) and OpenAPI spec (2.6 MB) are publicly accessible without authentication
- Open source: the actual implementation is readable on GitHub, providing the ultimate source of truth
- Per-resource documentation pages with field definitions, data types, descriptions, search parameters, and links to US Core profiles
- Explicit statement connecting the operation to EHI/Cures Act compliance
- The ONC compliance page cleanly maps b(10) to the `$patient-everything` operation

**Weaknesses:**
- No sample export output (a sample Bundle showing what a real `$patient-everything` response looks like would be helpful)
- No explicit enumeration of which resource types are in the Patient Compartment (the docs say "FHIR R4 Patient Compartment" and link to the FHIR spec, but don't list them on the page itself)
- No export instructions for non-developer users (the documentation assumes API literacy)
- The documentation doesn't discuss the Binary resource exclusion or its implications
- The Bulk FHIR API is documented separately but its relationship to b(10) vs g(10) could be clearer

### Structure & Completeness

- **Field-level granularity**: Excellent. The OpenAPI spec provides complete field definitions for every resource type including name, type, description, required/optional, and cardinality. The documentation pages add search parameters with FHIRPath expressions.
- **Value sets**: Referenced via the FHIR specification standard bindings. The server supports `ValueSet/$expand` and `CodeSystem/$lookup` for code lookup.
- **Relationships**: Expressed through FHIR Reference types — each reference field specifies which resource types it can point to. The Patient Compartment definition specifies which search parameters link each resource to a Patient.
- **Versioning**: The CapabilityStatement includes server version (5.0.14). Documentation was last updated Feb 10, 2026. Product was certified Dec 31, 2025.

### Overall Assessment

Medplum represents one of the best cases for EHI export documentation among certified EHRs. The fundamental architectural decision — storing data natively in FHIR — means the export is not a translation layer but a direct extraction of the actual data model. The `$patient-everything` operation is a standard FHIR operation, not a vendor-specific API, and the documentation leverages the FHIR specification as its data dictionary.

The documentation is compact but sufficient for a developer audience. The machine-readable artifacts (CapabilityStatement, OpenAPI spec) are the real deliverable — they provide complete, queryable schema definitions that would allow a third party to build an import system for Medplum's EHI export.

There is no b(10)/g(10) confusion here. While Medplum also supports the g(10) FHIR API (via the same FHIR server), the `$patient-everything` operation explicitly covers the full Patient Compartment — not just US Core/USCDI resource types. The export includes billing resources (Claim, ExplanationOfBenefit, ChargeItem, Account, Invoice), financial resources (Coverage), and administrative resources (Appointment, Communication) that go well beyond the USCDI clinical summary.

## Access Summary
- Registered URL: https://www.medplum.com/docs/api/fhir/operations/patient-everything
- Final URL (after redirects): same (no redirects)
- Status: found
- Required browser: no (static HTML served by Vercel, though tables render client-side)
- Navigation complexity: direct_link
- Anti-bot issues: none (standard User-Agent works fine)

## Obstacles & Dead Ends

- **Docusaurus client-side rendering**: The FHIR resource documentation pages use React/Docusaurus to render field definition tables client-side. The raw HTML downloaded via curl contains empty `<table>` elements. This was mitigated by using the OpenAPI spec (which contains the same schema information in machine-readable JSON) as the primary structured data source.
- **C-CDA export page 404**: The URL `/docs/api/fhir/operations/patient-ccda-export` returned a 404. The sidebar lists it as `/docs/api/fhir/operations/ccda-export`. This is a minor documentation link issue, not relevant to the b(10) export.
- **No issues with access**: All documentation and API endpoints were publicly accessible without authentication.
