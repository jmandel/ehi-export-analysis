# athenahealth, Inc. — EHI Export Documentation

Collected: 2026-02-16

## Source
- Registered URL: https://docs.mydata.athenahealth.com/fhir-r4/ehiexport.html#electronic-health-information-ehi-export
- CHPL IDs: 11629 (athenaPractice v25), 11663 (athenaFlow v25)
- Certification dates: 2025-04-28 (athenaPractice), 2025-07-11 (athenaFlow)

## Navigation Journal

### Step 1: Probe the URL
```bash
curl -sI -L "https://docs.mydata.athenahealth.com/fhir-r4/ehiexport.html" -H 'User-Agent: Mozilla/5.0'
```
Returned HTTP 200, Content-Type: text/html, 25,036 bytes. Static HTML hosted on Azure Blob Storage. No redirects, no authentication required, no anti-bot measures.

### Step 2: Fetch and examine the page
```bash
curl -sL "https://docs.mydata.athenahealth.com/fhir-r4/ehiexport.html" -H 'User-Agent: Mozilla/5.0' -o ehiexport.html
```
The page is part of a FHIR R4 Implementation Guide (IG) v25.0.0, generated 2025-04-10 using standard HL7 FHIR IG Publisher tooling. The site has a nav bar with links to: Home, Table of Contents, API Artifacts (EHI Export, Operations, Security), Artifact Index, RESTful API, Support (FHIR Spec, Downloads).

### Step 3: Download key site pages
Downloaded all 8 key pages from the IG:
```bash
for page in ehiexport.html index.html toc.html artifacts.html operations.html downloads.html restapi.html security.html; do
  curl -sL "https://docs.mydata.athenahealth.com/fhir-r4/$page" -H 'User-Agent: Mozilla/5.0' -o "$page"
done
```

### Step 4: Check downloads page for machine-readable artifacts
The downloads page links to:
- `full-ig.zip` (52.7 MB) — complete IG package
- `definitions.json.zip` (1.3 MB) — JSON StructureDefinitions, CapabilityStatements, IG metadata
- `examples.json.zip` (2.0 MB) — JSON example resources
- Also: definitions.xml.zip, definitions.ttl.zip, examples.xml.zip, examples.ttl.zip

Downloaded the JSON variants:
```bash
BASE="https://docs.mydata.athenahealth.com/fhir-r4"
curl -sL "$BASE/full-ig.zip" -o full-ig.zip
curl -sL "$BASE/definitions.json.zip" -o definitions.json.zip
curl -sL "$BASE/examples.json.zip" -o examples.json.zip
```

All verified as valid ZIP archives via `file` command.

### Step 5: Extract and catalog definitions
Extracted `definitions.json.zip`: 120 JSON files including:
- 54 StructureDefinition profiles (resource + logical models)
- 56 StructureDefinition extensions
- 2 CapabilityStatements (athenaPractice, athenaFlow)
- 1 ImplementationGuide
- 4 ValueSets, 1 ConceptMap, 1 NamingSystem, 1 OperationDefinition

Extracted `examples.json.zip`: 220 JSON files including example instances of all resource types.

### Step 6: Download profile HTML pages
Downloaded 43 StructureDefinition profile HTML pages for all resources listed on the EHI Export page. Some URL case variations existed (e.g., `carePlan` vs `careplan`) — both were tried and the working variant retained.

### Step 7: Build enrichment
Created Bun TypeScript scripts to extract structured JSON from the 54 profile definitions and 220 examples. All files parsed successfully with 0 failures.

## What Was Found

athenahealth documents their EHI export as a **FHIR R4 Bulk Data Export** using the `Group/$export` operation. The export produces **Newline Delimited JSON (NDJSON)** files containing both standard FHIR R4 resources and custom (non-standard) FHIR-like resources.

### Export Mechanism
The EHI Export page states: "athenaPractice and athenaFlow support the export of electronic health information (EHI) based on FHIR Bulk Data Access." The Operations page confirms a `Group/$export` endpoint is available. The export uses NDJSON format per the FHIR Bulk Data specification.

### Export Format
Data is output as:
- **Standard FHIR R4 resources** for clinical and system data (conforming to athenahealth's own profiles, not US Core)
- **Custom non-FHIR "logical" resources** for financial/billing data that don't map to standard FHIR resource types

Custom resources "conform to the basic requirements for any FHIR Base Resource with id and meta elements" but define their own element structures. This is a practical approach — billing data like charges, claims, and collections don't have good standard FHIR equivalents, so athenahealth defined their own.

### Resource Types in EHI Export

**System Resources (6):** Location, Medication, Organization, Practitioner, PractitionerRole, OperationOutcome

**Clinical Resources (21 in athenaPractice, same for athenaFlow):** AllergyIntolerance, Binary, CarePlan, CareTeam, ClinicalImpression, Condition, Consent, Device, DiagnosticReport, DocumentReference, Encounter, FamilyMemberHistory, Goal, Immunization, MedicationAdministration, MedicationRequest, MedicationStatement, Observation, Procedure, Provenance, ServiceRequest

**Practice Management Resources (7, athenaPractice only for Account/Schedule/Slot):** Account, Appointment, Coverage, Patient, RelatedPerson, Schedule, Slot

**Custom Financial Resources (9, athenaPractice only):** Adjustment, BillingStatement, Charge, Claim, Collection, Deductible, Eligibility, PatientInsurance, Payment

**Total: 43 resource types for athenaPractice, 30 for athenaFlow**

The athenaFlow product lacks: Account, Schedule, Slot (practice management), and all 9 custom financial resources (Adjustment, BillingStatement, Charge, Claim, Collection, Deductible, Eligibility, PatientInsurance, Payment). This is a significant difference — athenaFlow's EHI export excludes all billing/financial data.

### Documentation Depth
The IG contains **54 StructureDefinition profiles** with a combined **4,324 snapshot elements**. Each profile includes:
- Element-level definitions with paths, data types, cardinality (min/max)
- Short descriptions and full definitions for most elements
- Value set bindings for coded elements (53 of 54 profiles have bindings)
- Extension definitions (16 profiles use custom extensions, with 56 extension definitions total)
- Cross-resource references (e.g., Charge.patient → Patient)

The IG also includes **220 example instances** demonstrating real data shapes for all resource types, including examples for custom financial resources.

### Custom Resource Detail
The custom financial resources are particularly well-documented. For example:
- **Charge** (107 elements): ticketNumber, batchName, CPT codes, modifiers, diagnosis codes, amounts, service dates, rendering provider, facility, place of service, and more
- **Collection** (79 elements): collection agency details, amounts, statuses, dates
- **Eligibility** (87 elements): coverage details, plan information, copays, deductibles
- **Claim** (41 elements): claim number, status, amounts, dates, payer information
- **Payment** (50 elements): payment type, amounts, check/EFT details, adjustment codes

## Export Coverage Assessment

### Data Domain Coverage

**Clearly covered:**
- **Demographics & patient data**: Patient resource with 280 elements — extremely detailed including extensions for gender identity, sexual orientation, tribal affiliation, pronouns, occupation, guarantor details, preferred contact
- **Clinical documentation**: Encounter (127 elements), ClinicalImpression, DiagnosticReport, DocumentReference — covers encounters, assessments, reports, and documents
- **Problems/conditions**: Condition resource with 89 elements
- **Medications**: MedicationRequest (135 elements), MedicationStatement (81 elements), MedicationAdministration (70 elements), MedicationDispense (85 elements), Medication (96 elements) — very comprehensive medication coverage
- **Allergies**: AllergyIntolerance with 199 elements
- **Lab results**: Observation (194 elements), DiagnosticReport, Specimen
- **Vital signs**: Observation resource with category-based filtering
- **Immunizations**: Immunization (111 elements) with VFC eligibility extension
- **Procedures**: Procedure (83 elements)
- **Care plans/goals**: CarePlan (82 elements), Goal (51 elements), CareTeam (71 elements)
- **Family history**: FamilyMemberHistory (64 elements)
- **Devices**: Device (85 elements)
- **Consent**: Consent (88 elements)
- **Documents & images**: Binary, DocumentReference, Media
- **Insurance/coverage**: Coverage (75 elements), PatientInsurance (47 elements)
- **Scheduling**: Appointment, Schedule, Slot (athenaPractice only)
- **Billing — charges**: Charge resource (107 elements) with CPT codes, modifiers, diagnosis codes, amounts
- **Billing — claims**: Claim resource (41 elements)
- **Billing — payments**: Payment (50 elements), Adjustment (41 elements)
- **Billing — collections**: Collection (79 elements)
- **Billing — deductibles**: Deductible (41 elements)
- **Billing — eligibility**: Eligibility (87 elements)
- **Billing — statements**: BillingStatement (22 elements)
- **Service requests/orders**: ServiceRequest (78 elements) covering lab orders, imaging orders, referrals, consultations
- **Provenance**: Provenance (99 elements) tracking data origin

**Key gap — athenaFlow billing data**: athenaFlow's export excludes all 9 custom financial resource types and 3 practice management resources (Account, Schedule, Slot). The index page explicitly states: "These resources are only available through the athenaPractice or Practice Management products. They are not available in athenaFlow." If athenaFlow installations store billing data (and the product research suggests they may through integration), this data would not be in the EHI export.

**Possible gap — clinical notes as free text**: While DocumentReference and Binary resources can carry clinical documents, and ClinicalImpression handles assessments, it's unclear whether all free-text clinical notes (progress notes, H&P, discharge summaries) are captured. They may be in DocumentReference with Binary attachments, or in Encounter narrative fields, but this isn't explicitly documented.

**Not missing (correctly excluded)**: Audit logs are present in the CapabilityStatement (AuditEvent resource) but are not listed on the EHI export page — this is correct as audit logs are not part of the designated record set.

### Export Format & Standards

The export format is **FHIR R4 NDJSON via Bulk Data Access**, which is an excellent choice:
- Uses an established, standardized export protocol
- Machine-readable JSON format
- Newline-delimited for easy streaming/parsing
- Includes both standard FHIR R4 resources AND custom resources for data that doesn't fit standard types

The custom resources maintain FHIR conventions (id, meta, JSON structure) while adding vendor-specific elements for billing data. This is a pragmatic approach — rather than leaving billing data out entirely (as many vendors do), athenahealth defined custom resource types that extend the FHIR pattern.

**Reconstruction assessment**: A third party could reconstruct a comprehensive patient record from this export. The combination of standard clinical resources plus custom financial resources covers both the clinical and billing sides. Cross-resource references (patient, encounter, practitioner links) maintain the relational structure. Standard terminologies (LOINC, SNOMED, ICD-10, CPT, RxNorm, NDC, CVX) plus ConceptMap resources for local code mappings would allow meaningful interpretation.

### Documentation Quality

**Strengths:**
- Very well-structured as a FHIR Implementation Guide using standard IG Publisher tooling
- Machine-readable StructureDefinitions with element-level constraints, types, cardinality, and bindings
- 220 example instances demonstrating real data shapes
- Two CapabilityStatements (one per product) documenting API capabilities
- ConceptMap for local-to-standard code mappings
- Downloadable IG package in multiple formats (JSON, XML, TTL)
- Custom extension definitions fully documented
- Separate documentation for athenaPractice vs athenaFlow resource availability

**Weaknesses:**
- No explicit "how to perform an EHI export" user guide — no step-by-step instructions for an administrator to initiate the export
- No sample NDJSON export files (only individual resource examples, not a complete bulk export sample)
- The EHI Export page itself is sparse (just a resource list) — no narrative description of the export process, access controls, timing, or limitations
- No documentation of the `Group/$export` operation parameters specific to EHI export
- No Bulk Data-specific OperationDefinition for `$export` (only `$unique` is defined)
- Missing examples for custom financial resources (Charge, Claim, Collection, etc.) — the examples directory has standard resource examples but none of the custom types

### Structure & Completeness

**Granularity**: Element-level documentation across 4,324 elements is excellent. Each element has:
- Path, data type(s), cardinality (min/max)
- Short description and definition text
- Value set bindings where applicable (strength: required, extensible, preferred, example)
- Extension definitions with URLs and value types

**Coded fields**: 53 of 54 profiles include value set bindings for coded elements. Standard value sets reference HL7 FHIR value sets; local value sets are available via the ValueSet resource. ConceptMaps provide local-to-standard code translations.

**Relationships**: Cross-resource references are documented via Reference type elements with target profiles. The CapabilityStatement documents search parameters for navigating relationships.

**Versioning**: The IG is versioned (v25.0.0) and dated (2025-04-10). The IG tracks FHIR R4 (4.0.1).

## Access Summary
- Final URL (after redirects): https://docs.mydata.athenahealth.com/fhir-r4/ehiexport.html
- Status: found
- Required browser: no
- Navigation complexity: direct_link (EHI Export page is directly linked; downloadable packages are one click from Downloads page)
- Anti-bot issues: none

## Obstacles & Dead Ends

1. **Profile URL case sensitivity**: The EHI Export page links to profiles using two different URL casings (e.g., `StructureDefinition-athena-carePlan-profile.html` vs `StructureDefinition-athena-careplan-profile.html`). The server appears case-sensitive — some URLs return a 321-byte error page. The correct URLs were identified by trying both variants.

2. **Typo in URL**: One profile is linked as `StructureDefinition-athena-rocedure-profile.html` (missing the "p" in "Procedure"). The correct URL is `StructureDefinition-athena-procedure-profile.html`.

3. **athenaFlow billing gap**: The documentation clearly states that all custom financial resources and some practice management resources are only available for athenaPractice, not athenaFlow. This is properly documented but represents a real EHI export gap for athenaFlow.

4. **No export process documentation**: The IG thoroughly documents the data model but provides no user-facing instructions on how to actually initiate or receive an EHI export. The `Group/$export` operation is listed on the Operations page but without specific parameters, authentication requirements, or workflow instructions for EHI export specifically.
