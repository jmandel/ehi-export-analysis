# EHI Export Analysis: PCE Systems

**Product**: PCE Care Management v9.4
**Analysis date**: 2026-02-15
**CHPL ID**: 15.04.04.2125.PCEC.94.01.1.221205

## 1. Product Context

PCE Care Management is a behavioral health EHR developed by PCE Systems (Farmington Hills, MI, ~11–50 employees) serving Michigan's public community mental health system. Its customer base consists of Community Mental Health Service Programs (CMHSPs) and Prepaid Inpatient Health Plans (PIHPs) serving Medicaid beneficiaries with mental illness, substance use disorders, and developmental disabilities. PCE claims its clients encompass over 70% of Michigan's Medicaid mental health budget (as of 2013).

**Data domains the product is known to store** (based on product research and API evidence):
- **Clinical**: demographics, allergies, conditions/diagnoses, medications, immunizations, procedures, vitals, lab results, clinical notes/documents, care plans, care teams, goals, diagnostic reports, implantable devices
- **Behavioral health-specific**: individualized treatment plans, clinical assessments (e.g., MichiCANS), intake/discharge records, incident reports, consent directives (42 CFR Part 2 / Michigan Mental Health Code)
- **Billing/financial**: claims, insurance/coverage, service information reporting for Medicaid
- **Care coordination**: provider information exchange (PIX), cross-agency record sharing, social service referrals
- **Patient-facing**: patient portal (CEHR)
- **Documents**: scanned documents, PDFs, non-computable files

This is a comprehensive behavioral health EHR, not a limited-scope module. It is certified across 44 ONC criteria, including (b)(10) EHI export.

## 2. Artifacts Reviewed

| Artifact | Size | Description | Informativeness |
|---|---|---|---|
| `b10_documentation.pdf` | 889 KB, 3 pages | EHI Export (b)(10) format specification. Describes the ZIP container structure, NDJSON format, data types, and self-describing `documentation.json` schema — but does **not** enumerate which resources or fields are actually exported. | **Core artifact** for understanding export mechanics; uninformative for content coverage |
| `PIX_9_4_API_Documentation.pdf` | 1.9 MB, 87 pages | FHIR (g)(10) API documentation covering SMART on FHIR OAuth2, 22 FHIR resource types, and field-level data element definitions (pages 65–78). Dated April 23, 2025. | **Most informative** — only public enumeration of PCE's data model, but describes the FHIR API, not the (b)(10) export |
| `capability-statement.json` | 42.6 KB | FHIR CapabilityStatement from production endpoint. Declares 22 resource types (21 clinical + Group) with FHIR v4.0.1, US Core Server conformance, and Bulk Data support. | Confirms API resource set; machine-readable |
| `g10APIInfo.html` | 2.3 KB | Landing page with links to API and EHI Export documentation, plus FHIR API base URLs (production and test at `w3.pcesecure.com`). | Navigation only |
| `landing-page-screenshot.png` | 56 KB | Screenshot of the landing page. | Minimal |

**No sample export data, no `documentation.json`, and no data dictionary for the (b)(10) export were available.** The only field-level documentation is for the FHIR (g)(10) API, not the (b)(10) EHI export.

## 3. Export Mechanics

- **Format**: Password-protected ZIP files containing:
  - `meta.json` — export process metadata (who ran it, when)
  - `documentation.json` — self-describing JSON schema with all resource definitions, property names, data types, and descriptions
  - `Patient_[EHRPatientId]/` subdirectories — one per patient, containing NDJSON files per resource type and a `Files/` subdirectory for non-computable attachments (scanned documents, PDFs)
- **Serialization**: NDJSON (Newline-Delimited JSON), with 7 supported data types: CLOB, DATE, DECIMAL, INTEGER, RESOURCE (cross-reference), STRING, TIMESTAMP
- **Mechanism**: Initiated by "authorized EHR users" through the EHR system — a purpose-built export function, not a repurposed FHIR Bulk Data endpoint
- **Single-patient vs bulk**: Supports both per-patient and all-patient export
- **Access constraints**: Export is performed by authorized EHR users; password protection on ZIP files. No mention of fees for the export itself (API has setup fees per Appendix C, but that's separate)
- **Key design feature**: The actual data dictionary is embedded in `documentation.json` within the export ZIP itself — it is not published separately

## 4. Export Content: What's In It

### The fundamental evidence gap

The (b)(10) documentation (3 pages) describes only the **container format** — how data is packaged — but does not enumerate **what data** is exported. The documentation states that `documentation.json` contains "a list of all possible resource definitions" (emphasis on "all"), but this file is only available inside an actual export ZIP, which was not provided as a public artifact.

**We cannot determine from the available documentation how many resources, tables, or fields the (b)(10) export contains.** The prior agent's report correctly identified this gap.

### What the FHIR API documentation tells us (indirect evidence only)

The API documentation (87 pages) is the only public source of field-level data definitions from PCE. It documents 22 FHIR resource types with a total of approximately 288 fields (277 across 22 clinical/business resources, plus ~11 for PractitionerRole which the parser couldn't fully extract due to PDF formatting). All fields include attribute names, data types, and descriptions. The resources conform to US Core 4.0.0 profiles.

**However, this documents the (g)(10) FHIR API, not the (b)(10) export.** The (b)(10) export uses a different format (NDJSON in ZIP) with its own schema (`documentation.json`), and could contain either more or fewer resources than the API. The b(10) documentation's use of "all possible resource definitions" suggests it may export more than the FHIR subset, but this cannot be verified.

### FHIR API resource inventory (for reference, not b(10) export)

| Resource | Fields | Descriptions | Notes |
|---|---|---|---|
| AllergyIntolerance | 11 | 11 | US Core profile |
| CarePlan | 15 | 15 | US Core profile |
| CareTeam | 8 | 8 | US Core profile |
| Claim | 21 | 21 | Not standard USCDI; includes line items, modifiers, paid/total amounts |
| Condition | 10 | 10 | US Core profile |
| Coverage | 8 | 8 | Insurance coverage |
| Device | 21 | 21 | US Core Implantable Device profile |
| DiagnosticReport | 15 | 15 | US Core Lab + Report/Note profiles |
| DocumentReference | 17 | 17 | US Core profile; includes base64 content |
| Encounter | 15 | 15 | US Core profile; includes discharge disposition |
| Goal | 9 | 9 | US Core profile |
| HealthcareService | 6 | 6 | Service availability info |
| Immunization | 19 | 19 | US Core profile |
| Location | 14 | 14 | US Core profile |
| MedicationRequest | 16 | 16 | US Core profile; includes dosage, refills |
| Observation | 15 | 15 | Vitals, smoking status per US Core |
| Organization | 12 | 12 | US Core; includes NPI, CLIA |
| Patient | 16 | 16 | US Core; includes race, ethnicity, birth sex |
| Practitioner | 13 | 13 | US Core; includes qualifications |
| PractitionerRole | ~11 | ~11 | US Core; PDF formatting prevented exact parse |
| Procedure | 7 | 7 | US Core profile |
| Provenance | 9 | 9 | US Core; author + transmitter agents |

**Total**: 22 clinical/business resources, ~288 fields, 100% with descriptions.

The Claim resource (21 fields including `billablePeriod`, `item:productOrService`, `item:modifier`, `paid:value`, `total:value`) and Coverage resource (8 fields) are notable — they go beyond standard USCDI v1 requirements and indicate PCE stores and exposes billing/insurance data.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The (b)(10) documentation provides no content enumeration. Based solely on the (b)(10) format spec:

- **Structured data**: NDJSON files organized per-patient, per-resource type. Resource types and fields are defined in `documentation.json`, which is embedded in the export itself.
- **Unstructured data**: A `Files/` subdirectory per patient for non-computable files (scanned documents, PDFs). Resources reference these files via `fileName` or `imageName` properties.
- **Cross-references**: The RESOURCE data type supports inter-resource linking via `resource` name and `id`.

The vendor's documentation explicitly claims the export contains "all possible resource definitions" — but without the `documentation.json` or sample data, this cannot be verified.

The FHIR API provides indirect evidence of data the product stores, organized around US Core FHIR resources plus Claim and Coverage. If the (b)(10) export mirrors or exceeds this, it would cover standard clinical data plus some billing. If it only mirrors the FHIR set, it would miss behavioral health-specific data (assessments, treatment plans, incident reports, consent directives).

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial (inferred) | No (b)(10) content spec; FHIR API has Patient (16 fields) | Product stores demographics; likely in export but unverifiable |
| Encounters / visits | ⚠️ Partial (inferred) | No (b)(10) content spec; FHIR API has Encounter (15 fields) | Product stores encounters; likely in export but unverifiable |
| Problems / conditions | ⚠️ Partial (inferred) | No (b)(10) content spec; FHIR API has Condition (10 fields) | Likely covered |
| Medications / prescriptions | ⚠️ Partial (inferred) | No (b)(10) content spec; FHIR API has MedicationRequest (16 fields) | Likely covered |
| Allergies | ⚠️ Partial (inferred) | No (b)(10) content spec; FHIR API has AllergyIntolerance (11 fields) | Likely covered |
| Immunizations | ⚠️ Partial (inferred) | No (b)(10) content spec; FHIR API has Immunization (19 fields) | Likely covered |
| Vitals | ⚠️ Partial (inferred) | No (b)(10) content spec; FHIR API has Observation (15 fields) | Likely covered |
| Lab results | ⚠️ Partial (inferred) | No (b)(10) content spec; FHIR API has DiagnosticReport + Observation | Likely covered |
| Imaging / diagnostic reports | ⚠️ Partial (inferred) | No (b)(10) content spec; FHIR API has DiagnosticReport (15 fields) | Likely covered |
| Procedures | ⚠️ Partial (inferred) | No (b)(10) content spec; FHIR API has Procedure (7 fields) | Likely covered |
| Clinical notes / documents | ⚠️ Partial (inferred) | No (b)(10) content spec; FHIR API has DocumentReference (17 fields); b(10) has Files/ folder | Likely covered including non-computable attachments |
| Care plans / goals | ⚠️ Partial (inferred) | No (b)(10) content spec; FHIR API has CarePlan (15) + Goal (9) | Likely covered |
| Orders / referrals | ❌ Not evidenced | No dedicated resource in API or export docs | Product may handle referrals (signed MiHIN referrals pledge); gap uncertain |
| Insurance / coverage | ⚠️ Partial (inferred) | No (b)(10) content spec; FHIR API has Coverage (8 fields) | Likely covered |
| Claims / billing | ⚠️ Partial (inferred) | No (b)(10) content spec; FHIR API has Claim (21 fields) | Product does billing/claims submission; Claim resource is present in API but unclear if in (b)(10) export |
| Payments | ❌ Not evidenced | No payment resource in API or export docs; Claim has `paid:value` field | Product processes payments; partial data exists in Claim |
| Consents / directives | ❌ Not evidenced | No Consent resource in API or export docs | **Significant gap**: PCE has an explicit eConsent Management System for 42 CFR Part 2 and Michigan Mental Health Code. No evidence this critical behavioral health data is in the export |
| Patient communications | ❌ Not evidenced | API docs mention a "Message" data element but it's for error messages, not patient communications | Unknown if patient portal messages are exported |
| Specialty: Behavioral health assessments | ❌ Not evidenced | No assessment-specific resources in API or export docs | **Significant gap**: MichiCANS and other clinical assessments are core to the product. No evidence they're in either the FHIR API or (b)(10) export |
| Specialty: Treatment plans | ⚠️ Partial (inferred) | FHIR CarePlan may partially represent these | Individualized behavioral health treatment plans are more detailed than a standard FHIR CarePlan; likely incomplete representation |
| Specialty: Incident reports | ❌ Not evidenced | No resource for incidents in API or export docs | Product stores incident reports (per CMHPSM); no evidence in export |

**Key finding**: Every domain assessment is qualified with "inferred" because there is no direct evidence of what the (b)(10) export contains. The most concerning gaps are in behavioral health-specific data — assessments, consent directives, and incident reports — which are core to the product's purpose but have no representation in any available documentation.

## 6. Documentation Quality

**The (b)(10) export documentation is a format specification, not a content specification.** It tells you:
- ✅ How the export is packaged (ZIP, NDJSON, per-patient directories)
- ✅ What data types are supported (7 types)
- ✅ How cross-references work (RESOURCE type)
- ✅ How non-computable files are included (Files/ subdirectory)
- ❌ What resources/entities are exported
- ❌ What fields each resource contains
- ❌ What value sets or code systems are used
- ❌ What relationships exist between resources
- ❌ Any sample data or example `documentation.json`

**Could a developer build an import from this documentation alone?** No. A developer would know the container format but would have no idea what data to expect until they received an actual export and examined the `documentation.json` file inside it.

**Self-describing format mitigation**: The embedded `documentation.json` means the schema always travels with the data, which is a sound engineering choice. But it fails the transparency test — no one can evaluate the export's completeness without performing one.

**API documentation quality**: The 87-page FHIR API documentation is much better — it has field-level definitions with attribute names, data types, and descriptions for all 22 resources, plus OAuth2 flows, search parameters, and USCDI mapping. But this documents a different system ((g)(10) API, not (b)(10) export).

## 7. Overall Assessment

### Classification

**Minimal/stub** — The (b)(10) export documentation is too thin to assess actual content coverage. While the export *mechanism* is well-designed (purpose-built NDJSON export with self-describing schema, not a repurposed FHIR endpoint), the public documentation provides zero visibility into what data is actually exported. There is no data dictionary, no sample data, no resource enumeration, and no way to evaluate completeness without performing an actual export.

The export *could* be comprehensive — the format supports it, and the language "all possible resource definitions" is promising. But based on available evidence, this cannot be confirmed.

### Key Findings

1. **The (b)(10) export is architecturally distinct from the FHIR API** — PCE built a separate, purpose-built export function using NDJSON in ZIP files with a self-describing JSON schema. This is a positive signal that they didn't just rebrand their FHIR Bulk Data endpoint as (b)(10). However, the actual content is entirely opaque from the public documentation.

2. **The only public data dictionary describes the (g)(10) API, not the (b)(10) export** — The 87-page API documentation enumerates 22 FHIR resources with ~288 fields, all with descriptions. But this is a FHIR R4 / US Core projection, not the native data model, and it's for a different certification criterion.

3. **Behavioral health-specific data — the product's core domain — has no representation in any available documentation** — MichiCANS assessments, individualized treatment plans (beyond generic CarePlan), incident reports, and 42 CFR Part 2 consent directives are central to this product but absent from both the API and the (b)(10) export docs.

4. **The FHIR API includes Claim and Coverage resources** — This is notable because it goes beyond standard USCDI v1 requirements, with the Claim resource including line items, modifiers, and payment amounts (21 fields). This suggests billing data is at least partially available via API, though its presence in the (b)(10) export is unconfirmed.

5. **The self-describing `documentation.json` approach is sound engineering but poor transparency** — Having the schema embedded in the export means it's always in sync with the data. But it means no external party can assess export completeness without actually running the export.

### Summary Stats

```
Classification:  Minimal/stub
Export format:   NDJSON in password-protected ZIP
Model type:      Unknown — could be native database or standard projection; documentation.json is not publicly available
Entities:        N/A (no data dictionary for b(10) export)
Fields:          N/A
Descriptions:    N/A
Sample data:     No
Bulk export:     Yes (per-patient and all-patient)
Domains covered: Cannot be determined from available documentation
```

### Bottom Line

PCE Systems built a thoughtfully designed (b)(10) export mechanism with a self-describing schema, per-patient NDJSON files, non-computable file support, and cross-reference capabilities. However, the public documentation is a 3-page format specification that says nothing about what data is actually exported. The product's core behavioral health data (assessments, consent directives, incident reports) has no representation in any public artifact. Until PCE publishes the `documentation.json` schema or a sample export, it is impossible for a patient, provider, or third party to evaluate whether this export meets the "all electronic health information" requirement of (b)(10).
