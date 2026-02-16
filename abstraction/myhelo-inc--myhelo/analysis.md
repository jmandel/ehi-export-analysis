# EHI Export Analysis: myhELO, Inc.

**Product**: myhELO
**Analysis date**: 2026-02-16
**CHPL IDs**: 9930 (15.05.05.2637.MOXE.01.00.1.190305)

## 1. Product Context

myhELO is a cloud-based, all-in-one healthcare platform marketed as a "Healthcare Operating System" for outpatient specialty practices and ambulatory surgery centers (ASCs), with a particular focus on orthopedic practices. The platform integrates:

- **EMR / Clinical Documentation**: Charting, customizable surgical templates, medical image viewing/storage, automated note generation from intake forms, pre-op and post-op workflows
- **Scheduling & Practice Management**: Multi-device scheduling, OR resource management
- **E-Prescribing**: Electronic prescriptions, renewals, prior authorizations
- **Revenue Cycle Management (RCM)**: AI-powered coding, built-in clearinghouse, claims submission/tracking, payment collection, denial management, insurance verification
- **Patient Engagement / Portal**: Secure messaging, digital intake forms, patient-reported outcomes, online payments
- **Telehealth**: HIPAA-compliant video visits
- **Reporting & Analytics**: Financial dashboards, RCM analytics

The product is broadly certified across 35+ ONC criteria including (b)(10), (g)(10), and clinical data criteria (a)(1)–(a)(13). Certified users: "healthcare professionals and administrative staff operating in outpatient specialty practices and ambulatory surgery centers."

**Baseline for export completeness**: A credible (b)(10) export for myhELO should cover clinical documentation, billing/claims/charges, insurance/coverage, e-prescribing details, patient intake forms, patient communications, surgical templates, scheduling, and patient-reported outcomes — not just the USCDI clinical summary.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/main-page.html` (3.3 KB) | Rendered EHI export index page — title, intro text, table of 17 datasets | **High**: confirms scope and vendor framing |
| `downloads/dataset-pages/index.html` (9.4 KB) | Full rendered EHI export page with navigation and footer | **Medium**: same content as main-page.html, fuller rendering |
| `downloads/structure-definitions.json` (2.6 MB) | All 17 FHIR R4 StructureDefinitions extracted from the JS SPA bundle | **Highest**: machine-readable, complete element-level definitions |
| `downloads/dataset-summaries.json` (20.5 KB) | Overview metadata for all 17 resource types | **Medium**: brief descriptions and profile references |
| `downloads/fhir-metadata.json` (6.4 KB) | FHIR CapabilityStatement from provider.myhelo.com | **High**: confirms server capabilities, resource list, bulk export |
| `downloads/fhir-well-known.json` (98.9 KB) | API spec with example FHIR JSON responses for all resource types | **High**: shows realistic example data and field population |
| `downloads/api-docs.html` (69.9 KB) | Rendered FHIR API documentation page | **Medium**: API access instructions, endpoints, examples |
| `downloads/datasets/AllergyIntolerance.html` (106.9 KB) | Sample dataset specification page (one of 17) | **Medium**: detailed element definitions, representative of all dataset pages |
| `downloads/datasets/CarePlan.html` (106.9 KB) | CarePlan dataset specification page | **Low**: same size/structure as AllergyIntolerance, confirming template pattern |
| `downloads/datasets/CareTeam.html` (106.9 KB) | CareTeam dataset specification page | **Low**: same as above |
| Various screenshots (PNG) | Visual captures of web pages | **Low**: confirmatory only |
| `downloads/enrichment/` directory | Prior enrichment scripts and outputs | **Reference**: used for comparison, not as primary source |

## 3. Export Mechanics

- **Format**: FHIR R4 JSON, following US Core profiles
- **Mechanism**: FHIR API server at `https://provider.myhelo.com/fhir` with SMART-on-FHIR OAuth2 authentication. Supports individual resource read/search and Group/$export (Bulk Data Access) for multi-patient export.
- **Single-patient vs bulk**: Both supported. The vendor's introduction states: "Customers can choose to export all or selected myhELO EHI datasets for a single patient, multiple patients, or all patients in the practices."
- **Access constraints**: Requires SMART-on-FHIR OAuth2 authorization (authorize, token, revoke endpoints documented in CapabilityStatement). No fees mentioned in documentation.
- **Export initiation**: Not documented in the artifacts. There is no description of a UI workflow, admin panel, or specific API call sequence to initiate a (b)(10) export. The documentation describes the data format and API endpoints but not the operational process.

## 4. Export Content: What's In It

### Structure overview

The export documentation covers exactly **17 FHIR R4 resource types**, each conforming to a standard US Core profile. I parsed all 17 StructureDefinitions from `structure-definitions.json` and produced a complete element-level inventory.

**Aggregate statistics** (from `analysis/entity-inventory-full.json`):
- **17 resources** (FHIR resource types)
- **938 total elements** across all resources (including root elements)
- **179 USCDI elements** (mustSupport = true)
- **105 required elements** (min > 0)
- **203 elements with value set bindings**
- **938 elements with definitions** (100% — all elements have FHIR-standard definitions)
- **Example data**: 16 of 17 resources have example JSON responses in the API spec (Organization is the exception)

### Vendor's own content organization

The vendor organizes the export as "Clinical EHI Export Dataset List & Specifications" with 17 datasets. All datasets reference standard US Core profiles with no vendor-specific extensions, custom profiles, or proprietary elements.

| Resource Type | Elements | USCDI | Required | Bindings | US Core Profile(s) |
|---|---|---|---|---|---|
| AllergyIntolerance | 35 | 6 | 3 | 11 | US Core AllergyIntolerance |
| CarePlan | 65 | 8 | 8 | 12 | US Core CarePlan |
| CareTeam | 29 | 5 | 4 | 5 | US Core CareTeam |
| Condition | 37 | 5 | 3 | 10 | US Core Condition |
| Device | 66 | 10 | 8 | 6 | US Core ImplantableDevice |
| DiagnosticReport | 33 | 9 | 6 | 6 | US Core DiagnosticReport (Lab + Note) |
| DocumentReference | 56 | 16 | 8 | 14 | US Core DocumentReference |
| Encounter | 81 | 19 | 12 | 21 | US Core Encounter |
| Goal | 31 | 6 | 3 | 10 | US Core Goal |
| Immunization | 63 | 6 | 6 | 13 | US Core Immunization |
| MedicationRequest | 83 | 18 | 5 | 20 | US Core MedicationRequest |
| Observation | 51 | 9 | 6 | 14 | US Core Observation (Lab, Vitals, Smoking, Pediatric) |
| Organization | 56 | 15 | 2 | 10 | US Core Organization |
| Patient | 87 | 17 | 10 | 15 | US Core Patient |
| Practitioner | 63 | 15 | 6 | 12 | US Core Practitioner |
| Procedure | 48 | 4 | 5 | 13 | US Core Procedure |
| Provenance | 54 | 11 | 10 | 11 | US Core Provenance |
| **Totals** | **938** | **179** | **105** | **203** | |

### Key observations about the data

1. **No vendor-specific extensions or custom profiles**: Every resource uses standard US Core profiles. There are no custom FHIR extensions, no vendor-defined value sets, and no proprietary elements. This means the export contains exactly what the US Core IG specifies — nothing more.

2. **All descriptions are standard FHIR definitions**: The 100% description coverage is because these are the standard FHIR element definitions embedded in the StructureDefinitions — not vendor-written documentation explaining how myhELO's data maps to FHIR fields.

3. **Example data shows standard clinical content**: The example responses in `fhir-well-known.json` use standard coding systems (SNOMED CT, LOINC, CPT, CVX, ICD) and show typical US Core data — no billing codes, no specialty-specific data, no custom form responses.

4. **CapabilityStatement confirms API identity**: The CapabilityStatement lists 19 resources (the 17 EHI resources plus Group for bulk export and Location). The Group/$export endpoint is the standard Bulk Data Access mechanism used for (g)(10). The identical resource set confirms this is the (g)(10) API surface relabeled as (b)(10).

Full inventory: `analysis/entity-inventory-full.json` (938 element objects with path, definition, types, cardinality, bindings, and mustSupport flags).

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor's export covers a single domain: **USCDI clinical data** via US Core FHIR profiles. The 17 resource types map 1:1 to the US Core Implementation Guide resource set. There is no vendor-specific categorization — the vendor uses FHIR resource names as their dataset names.

The coverage within this USCDI domain is solid: all US Core profiles are represented, mustSupport elements are flagged, value set bindings are documented, and example data is provided. This is well-implemented (g)(10) API documentation.

However, there is no depth beyond USCDI. The export does not include vendor-specific elements within USCDI-scope resources (e.g., no extensions for orthopedic-specific procedure details, no custom fields on Encounter for surgical context). Every element is straight from the FHIR R4 base spec constrained by US Core.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | `Patient` (87 elements), US Core race/ethnicity/birthsex extensions | Standard US Core demographics — adequate |
| Encounters / visits | ✅ Covered | `Encounter` (81 elements) with type, period, participants, location | Standard encounter data — no surgical/OR-specific context |
| Problems / conditions | ✅ Covered | `Condition` (37 elements) with SNOMED coding, clinical status | Standard US Core |
| Medications / prescriptions | ⚠️ Partial | `MedicationRequest` (83 elements) — orders only | Product has e-prescribing with renewals, prior authorizations, pharmacy info — none exported beyond the order itself |
| Allergies | ✅ Covered | `AllergyIntolerance` (35 elements) | Standard US Core |
| Immunizations | ✅ Covered | `Immunization` (63 elements) | Standard US Core |
| Vitals | ✅ Covered | `Observation` (51 elements) with vital sign profiles | Standard US Core vitals |
| Lab results | ✅ Covered | `Observation` (lab profile), `DiagnosticReport` | Standard US Core |
| Imaging / diagnostic reports | ⚠️ Partial | `DiagnosticReport` (note exchange profile) can carry PDF attachments | Product has built-in medical image viewing/storage/sharing — no DICOM or native image export |
| Procedures | ✅ Covered | `Procedure` (48 elements) with CPT coding | Standard procedure data — no customizable surgical templates or orthopedic-specific fields |
| Clinical notes / documents | ✅ Covered | `DocumentReference` (56 elements) with PDF attachments | Notes as PDFs — no structured note content |
| Care plans / goals | ✅ Covered | `CarePlan` (65 elements), `Goal` (31 elements) | Standard US Core |
| Orders / referrals | ⚠️ Partial | `MedicationRequest` covers medication orders only | No `ServiceRequest` for lab/imaging/referral orders despite product having CPOE (a)(1)–(a)(3) |
| Insurance / coverage | ❌ Not covered | No `Coverage` resource in export | Product has insurance verification, advance benefit verification, insurance details — significant gap |
| Claims / billing | ❌ Not covered | No `Claim`, `ExplanationOfBenefit`, or billing resources | Product has full RCM with AI-powered coding, claims, charges, denial management — **major gap** |
| Payments | ❌ Not covered | No payment resources | Product has payment collection, payment arrangements, digital billing — significant gap |
| Consents / directives | ❌ Not covered | No `Consent` resource | Product likely has consent forms for surgical procedures |
| Patient communications | ❌ Not covered | No `Communication` resource | Product has secure messaging, patient portal messages — significant gap |
| Patient intake forms / PROs | ❌ Not covered | No `QuestionnaireResponse` resource | Product has digital intake forms and patient-reported outcomes tracking — significant gap |
| Specialty-specific (orthopedic) | ❌ Not covered | No custom resources or extensions | Product emphasizes customizable surgical templates, pre-op planning, post-op care, medical image sharing — all absent from export |
| Telehealth records | ❌ Not covered | No telehealth-specific data | Product has HIPAA-compliant video visits — session records absent |

**Summary**: 10 of 20 applicable domains are covered (all via standard US Core), 3 are partially covered, and 7 are not covered at all. The uncovered domains — billing/RCM, patient engagement, specialty clinical data — represent core functionality of the product per its own marketing.

## 6. Documentation Quality

**Strengths:**
- Clean, navigable web-based data dictionary with an index page linking to 17 dataset specifications
- Complete FHIR StructureDefinitions embedded in machine-readable form (extractable from JS bundle)
- Element-level definitions with cardinality, data types, value set bindings, and mustSupport flags
- Example FHIR JSON responses for 16 of 17 resources showing realistic test data
- CapabilityStatement and API spec available as machine-readable JSON
- USCDI elements explicitly tagged

**Weaknesses:**
- **No vendor-specific documentation**: Every definition, description, and constraint is standard FHIR/US Core boilerplate. There is zero vendor-written content explaining how myhELO's internal data model maps to FHIR resources, what data might be lost in translation, or what product-specific fields exist.
- **No export process documentation**: How does a user initiate an EHI export? What UI? What options? The introduction mentions selecting datasets and patients, but no workflow is described.
- **No sample export files**: No downloadable ZIP, NDJSON bundle, or complete patient export example.
- **SPA-only rendering**: All pages require JavaScript rendering (3.3 MB JS bundle). Content is invisible to curl, screen readers, or simple HTTP clients.
- **No downloadable artifacts**: No PDF, no schema files, no offline documentation.

**Developer usability**: A developer could use the FHIR API to retrieve US Core resources — the documentation adequately describes a standard FHIR API. However, a developer could not determine from this documentation what data myhELO actually stores beyond USCDI, because the documentation doesn't describe the product's data model — only the standard profiles it conforms to.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Minimal/stub/unclear**

The export covers only the 17 US Core FHIR resource types — the exact set required for (g)(10) API certification. For a product that markets itself as a "Healthcare Operating System" integrating EMR, RCM, e-prescribing, patient portal, scheduling, and telehealth, the absence of billing/claims data, patient communications, intake forms, patient-reported outcomes, specialty surgical data, and insurance/coverage information represents a fundamental coverage gap. The export addresses approximately the USCDI clinical summary — perhaps 20-30% of what myhELO stores about patients.

I classify this as "Minimal/stub/unclear" rather than "Partial" because the export doesn't appear to contain *any* data beyond the (g)(10) baseline. A "Partial" classification would require at least some non-USCDI domains to be present (e.g., some billing or some specialty data). Here, there is no evidence of any data domain beyond US Core.

**Axis 2 — Export approach: Repackaged existing export**

This is their (g)(10) FHIR API relabeled as (b)(10) EHI export documentation. The evidence is strong and convergent:

1. **Identical resource set**: The 17 EHI export resources exactly match the US Core resource set. The CapabilityStatement (from the same FHIR server at provider.myhelo.com) lists these same resources plus Group (for bulk export) and Location.
2. **No custom profiles or extensions**: Every resource uses unmodified US Core profiles. No vendor-specific FHIR extensions, no custom value sets, no proprietary elements.
3. **Same server**: The EHI export documentation and the API documentation both point to `provider.myhelo.com/fhir` — the same FHIR server endpoint.
4. **Group/$export**: The CapabilityStatement documents the standard Bulk Data Access Group/$export operation — the (g)(10) bulk export mechanism.
5. **Boilerplate descriptions**: All dataset descriptions follow the template: "This profile is used to define the content that will be returned by the API Server in response to requests to access [Resource] resources." This is API documentation language, not EHI export documentation.
6. **No vendor-specific content**: The "Data Dictionary" contains zero vendor-written field descriptions, zero product-specific data mappings, and zero documentation of how myhELO's internal data model translates to FHIR.

### Key Findings

1. **Repackaged (g)(10) as (b)(10)**: The EHI export is the vendor's standard FHIR API (g)(10) surface relabeled as (b)(10). The 17 resource types, US Core profiles, FHIR server endpoint, and Bulk Data Access mechanism are identical. No purpose-built EHI export capability exists.

2. **No billing/RCM data despite full RCM module**: myhELO's RCM module includes AI-powered coding, claims submission, payment collection, denial management, and insurance verification. None of this appears in the export — no Claim, Coverage, ExplanationOfBenefit, or Account resources.

3. **No specialty clinical data despite orthopedic focus**: The product emphasizes customizable surgical templates, pre-op planning, and post-op care workflows for orthopedic practices and ASCs. The export contains only generic US Core Procedure and Encounter resources with no orthopedic-specific extensions or custom data.

4. **No patient engagement data despite full portal**: Secure messaging, digital intake forms, patient-reported outcomes, and appointment data are all features of the product. None appear in the export.

5. **Documentation quality is strong for what it covers**: The FHIR API documentation is technically competent — machine-readable StructureDefinitions, CapabilityStatement, example data, and element-level definitions. The problem is not documentation quality but export scope.

### Summary Stats

    Coverage:        Minimal/stub/unclear
    Approach:        Repackaged existing export
    Export format:   FHIR R4 JSON (US Core profiles)
    Entities:        17 (FHIR resource types)
    Fields:          938 (FHIR elements across all resources)
    Descriptions:    100% (standard FHIR definitions, not vendor-written)
    Sample data:     Yes (example JSON responses for 16/17 resources)
    Bulk export:     Yes (Group/$export via Bulk Data Access)
    Domains covered: 10 of 20 applicable domains (all USCDI-scope only)

### Bottom Line

myhELO's (b)(10) EHI export is its (g)(10) FHIR API relabeled — 17 standard US Core resources covering USCDI clinical data, with zero billing, specialty, or patient engagement data exported despite the product having full RCM, orthopedic surgical workflows, patient portal, and telehealth capabilities. A patient or provider requesting their complete record would receive a clinical summary missing billing records, surgical template data, patient communications, intake forms, and insurance details — likely less than a third of their designated record set.
