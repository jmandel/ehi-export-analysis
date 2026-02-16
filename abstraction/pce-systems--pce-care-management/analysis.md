# EHI Export Analysis: PCE Systems

**Product**: PCE Care Management v9.4
**Analysis date**: 2026-02-16
**CHPL IDs**: 15.04.04.2125.PCEC.94.01.1.221205 (CHPL ID 11045)

## 1. Product Context

PCE Care Management is a behavioral health EHR built for Michigan's community mental health system. PCE Systems (Farmington Hills, MI; ~11–50 employees) is the dominant EHR vendor across Michigan's Community Mental Health Service Programs (CMHSPs) and Prepaid Inpatient Health Plans (PIHPs), serving populations with serious mental illness, substance use disorders, and developmental disabilities. As of 2013, PCE claimed coverage of over 70% of Michigan's Medicaid mental health budget.

**Clinical workflows the product supports:**
- Intake and assessment (including MichiCANS structured assessments)
- Individualized treatment plan creation and tracking
- Clinical documentation and progress notes
- Care coordination across providers
- Discharge planning
- Incident reporting

**Billing / PM capabilities:**
- Integrated billing with claims submission (confirmed by CMHPSM website, FHIR Claim/Coverage resources)
- Insurance/coverage management
- Service information reporting for Medicaid

**Specialty features:**
- PIX (Provider Information Exchange) — a behavioral health HIE connecting PCE implementations across Michigan
- eConsent Management System for 42 CFR Part 2 (substance use disorder privacy) and Michigan Mental Health Code
- MI Care Connect Portal for community partners
- Patient portal (CEHR) with SMART on FHIR OAuth2

**Baseline for export completeness:** A complete EHI export should cover demographics, clinical assessments (including behavioral health–specific instruments like MichiCANS), treatment plans, encounter notes, medications, diagnoses, billing/claims, insurance/coverage, consent records, documents/scanned files, and care coordination data.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `b10_documentation.pdf` (3 pages, 889 KB, dated Nov 20, 2023) | EHI Export (b)(10) format specification. Describes the export container: password-protected ZIP with `meta.json`, `documentation.json` (embedded schema), and per-patient NDJSON files plus non-computable files. Does NOT enumerate resources or fields. | **Medium** — tells us the format but not the content |
| `PIX_9_4_API_Documentation.pdf` (87 pages, 1.9 MB, dated Jan 6, 2025) | FHIR (g)(10) API documentation. Covers SMART on FHIR OAuth2, all API operations, USCDI v1 mapping, and Data Elements section (pp. 65–78) with field-level definitions for 22 FHIR resource types plus 3 helper types. Includes appendices on costs and terms of use. | **High** — only public enumeration of PCE's data model, though this is the FHIR API model, not the native (b)(10) export model |
| `capability-statement.json` (42 KB) | FHIR R4 CapabilityStatement from production endpoint (`w3.pcesecure.com`). Machine-readable declaration of 22 supported FHIR resources. Declares conformance to US Core Server and FHIR Bulk Data. | **Medium** — confirms resource list and bulk data support |
| `g10APIInfo.html` (2.3 KB) | Landing page with links to both documentation PDFs and FHIR API base URLs (test and production). | **Low** — just a link page |
| `landing-page-screenshot.png` (56 KB) | Screenshot of the landing page. | **Low** — visual confirmation only |

## 3. Export Mechanics

- **Format**: Password-protected ZIP files containing NDJSON (Newline-Delimited JSON) files per resource type, plus non-computable files (scanned documents, PDFs) in a `Files/` subdirectory. A `meta.json` file records export metadata (who ran it, when) and a `documentation.json` file contains the complete self-describing data dictionary (resource definitions, property names, types, descriptions).
- **Mechanism**: Initiated by "authorized EHR users" through the EHR system (UI-based). This is a purpose-built (b)(10) export function, distinct from the FHIR API.
- **Single-patient vs bulk**: Supports both per-patient and all-patient export ("Data may be exported per patient or for all patients within the EHR" — b10_documentation.pdf, p. 1).
- **Access constraints**: Export is available to authorized EHR users. The password for the ZIP is "provided with the zip file(s)." No public pricing or fees specific to (b)(10) export are documented. The API documentation (Appendix C) mentions a one-time setup fee for API access, but this appears to apply to the (g)(10) FHIR API, not the (b)(10) export.
- **Data types supported**: CLOB, DATE, DECIMAL, INTEGER, RESOURCE (cross-references), STRING, TIMESTAMP.

## 4. Export Content: What's In It

### The fundamental limitation

The (b)(10) export documentation explicitly states that the data dictionary — the list of resources and their fields — is embedded in the `documentation.json` file within the export ZIP itself. The public documentation describes only the container format. This means **the specific resources, field names, and data types exported are not publicly knowable** without performing an actual export.

The documentation states `documentation.json` contains "a list of all possible resource definitions" (emphasis on "all"), which suggests the export may cover the full native data model.

### What the FHIR API reveals (proxy for the native model)

Since the (b)(10) export content is not publicly documented, the FHIR (g)(10) API documentation serves as the only public window into PCE's data model. The API documentation (pp. 65–78) defines 25 data elements: 22 FHIR resources plus 3 helper types. Parsed from the PDF, these contain **318 total fields, 314 with descriptions (98.7%), all 318 with data types.**

However, the FHIR API is a USCDI-conformant projection — it necessarily represents a subset of PCE's native data model. The (b)(10) export, which uses a proprietary NDJSON format with its own schema, likely includes additional resources (e.g., behavioral health assessments, consent records, treatment plans beyond CarePlan) that cannot be expressed in standard FHIR profiles.

### FHIR API entity inventory

The full parsed inventory is saved in `analysis/full-entity-inventory.json`. Summary:

| Entity | Fields | Described | Types | Profile/Category |
|---|---|---|---|---|
| Address | 9 | 9 | 9 | Helper type |
| AllergyIntolerance | 12 | 12 | 12 | US Core 4.0.0 |
| CarePlan | 15 | 15 | 15 | US Core 4.0.0 |
| CareTeam | 9 | 9 | 9 | US Core 4.0.0 |
| Claim | 22 | 22 | 22 | Base FHIR |
| Coded Element | 4 | 4 | 4 | Helper type |
| Condition | 10 | 10 | 10 | US Core 4.0.0 |
| Coverage | 8 | 8 | 8 | Base FHIR |
| Device | 21 | 21 | 21 | US Core 4.0.0 |
| Diagnostic Report | 15 | 15 | 15 | US Core 4.0.0 |
| Document Reference | 17 | 17 | 17 | US Core 4.0.0 |
| Encounter | 16 | 15 | 16 | US Core 4.0.0 |
| Goal | 9 | 9 | 9 | US Core 4.0.0 |
| Healthcare Service | 11 | 11 | 11 | Base FHIR |
| Immunization | 19 | 19 | 19 | US Core 4.0.0 |
| Location | 14 | 14 | 14 | Base FHIR |
| Medication Request | 16 | 16 | 16 | US Core 4.0.0 |
| Message | 4 | 4 | 4 | Helper type |
| Observation | 16 | 15 | 16 | US Core 4.0.0 |
| Organization | 12 | 12 | 12 | US Core 4.0.0 |
| Patient | 16 | 16 | 16 | US Core 4.0.0 |
| Practitioner | 13 | 13 | 13 | US Core 4.0.0 |
| Practitioner Role | 11 | 10 | 11 | US Core 4.0.0 |
| Procedure | 8 | 7 | 8 | US Core 4.0.0 |
| Provenance | 11 | 11 | 11 | US Core 4.0.0 |

**Totals**: 25 entities, 318 fields, 314 described (98.7%), 318 typed (100%).

Notable: The API includes **Claim** (22 fields) and **Coverage** (8 fields) resources, going beyond standard USCDI v1 requirements. This confirms PCE stores and exposes billing/insurance data through their FHIR API.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor does not publish an explicit content inventory for the (b)(10) export. Based on the FHIR API data elements (the only public enumeration):

**Well-represented domains** (via FHIR API):
- **Patient demographics** (Patient: 16 fields) — comprehensive demographics including race, ethnicity, language, addresses, contacts
- **Clinical documentation** (DocumentReference: 17 fields, DiagnosticReport: 15 fields) — supports both structured reports and unstructured documents, plus the `Files/` directory for scanned documents
- **Claims/billing** (Claim: 22 fields, Coverage: 8 fields) — one of the richest entities in the API, includes billable periods, service codes, modifiers, paid/total amounts, insurance references
- **Medications** (MedicationRequest: 16 fields) — prescriptions with dosage, dispense instructions, refills
- **Immunizations** (Immunization: 19 fields) — detailed with lot numbers, sites, funding sources
- **Encounters** (Encounter: 16 fields) — visit types, periods, participants, diagnoses, discharge dispositions

**Present but limited** (via FHIR API):
- **Care plans** (CarePlan: 15 fields) — generic FHIR CarePlan conforming to US Core; unlikely to capture PCE's full behavioral health treatment plan model
- **Goals** (Goal: 9 fields) — basic goal tracking
- **Procedures** (Procedure: 8 fields) — relatively thin

**Unknown / not visible through FHIR API:**
- Behavioral health assessments (MichiCANS, intake assessments, etc.)
- Consent directives (42 CFR Part 2 consent records)
- Incident reports
- Treatment plan details beyond FHIR CarePlan
- PIX/HIE exchange metadata
- Social service referrals
- Patient portal (CEHR) messages

The (b)(10) export may well include these domains in its native NDJSON format, but this cannot be verified from public documentation.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | Patient (16 fields) in FHIR API; likely more in native export | FHIR projection covers USCDI demographics; native export may include additional behavioral health–specific demographic fields |
| Encounters / visits | ⚠️ Partial | Encounter (16 fields) in FHIR API | Standard encounter data present; unknown if native export captures behavioral health–specific encounter details |
| Problems / conditions / diagnoses | ⚠️ Partial | Condition (10 fields) in FHIR API | Standard conditions present; behavioral health diagnostic details may be richer in native model |
| Medications / prescriptions | ⚠️ Partial | MedicationRequest (16 fields) in FHIR API | Present in FHIR; unknown if native export includes medication administration details |
| Allergies | ⚠️ Partial | AllergyIntolerance (12 fields) in FHIR API | Present |
| Immunizations | ⚠️ Partial | Immunization (19 fields) in FHIR API | Present with good detail |
| Vitals | ⚠️ Partial | Observation (16 fields) in FHIR API | Present (vital signs are a subcategory of Observation) |
| Lab results | ⚠️ Partial | Observation + DiagnosticReport in FHIR API | Present |
| Imaging / diagnostic reports | ⚠️ Partial | DiagnosticReport (15 fields), DocumentReference (17 fields) in FHIR API | Present for reports; images may be in Files/ directory |
| Procedures | ⚠️ Partial | Procedure (8 fields) in FHIR API | Present but thin |
| Clinical notes / documents | ⚠️ Partial | DocumentReference (17 fields) + Files/ directory for non-computable files | Strong — the export explicitly includes scanned documents and PDFs in a Files/ subdirectory |
| Care plans / goals | ⚠️ Partial | CarePlan (15 fields), Goal (9 fields) in FHIR API | FHIR CarePlan unlikely to capture full behavioral health treatment plans; significant uncertainty |
| Orders / referrals | ❌ Not covered | No evidence in any artifact | Product likely handles referrals (PIX, MiHIN Interoperable Referrals Pledge); not visible in FHIR API or export documentation |
| Insurance / coverage | ⚠️ Partial | Coverage (8 fields) in FHIR API | Present; Medicaid coverage management is core to this product |
| Claims / billing | ⚠️ Partial | Claim (22 fields) in FHIR API | Present with good detail (service codes, modifiers, amounts); unknown if native export includes additional billing tables |
| Payments | ❌ Not covered | No evidence in any artifact | Product handles claims but payment details are not visible |
| Consents / directives | ❌ Not covered | No evidence in any artifact | Significant gap — PCE has a dedicated eConsent Management System for 42 CFR Part 2 and Michigan Mental Health Code; consent data is EHI and should be exported |
| Patient communications / portal messages | ❌ Not covered | No evidence in any artifact | CEHR patient portal exists; message data is not visible in export documentation |
| Specialty-specific (behavioral health) | ❌ Not covered | No evidence in any artifact | **Critical gap in documentation** — MichiCANS assessments, structured intake forms, behavioral health treatment plan details, incident reports, and substance use disorder treatment records are core to this product but not visible in any public export documentation |

**Important caveat**: All "⚠️ Partial" ratings reflect that the FHIR API data is a confirmed proxy for the native (b)(10) export model, which may be more comprehensive. The "❌ Not covered" ratings mean there is no evidence in any public artifact — but the native export's `documentation.json` may well include these domains. The vendor's deliberate design of a separate, native-format (b)(10) export (rather than repackaging FHIR) suggests an intent to export more than the FHIR API surface.

## 6. Documentation Quality

**For the (b)(10) export itself**: Poor. The documentation is 3 pages describing the container format only. There is no public data dictionary, no resource enumeration, no field definitions, no sample data, no sample `documentation.json`, and no user guide for initiating the export. The self-describing nature of `documentation.json` within the export is technically sound but means the export's content is completely opaque to external review.

**For the (g)(10) FHIR API**: Good. The 87-page API documentation includes:
- USCDI v1 data class mapping (p. 8)
- Complete API operations with URL patterns, parameters, and return values
- Data Elements section (pp. 65–78) with field-level definitions: attribute name, data type, and description for each resource
- 98.7% of fields have descriptions; 100% have data types
- Appendices with access request form, terms of use, and cost information
- Revision history

**Could a developer build an import?** From the (b)(10) documentation alone, no — they would need an actual export file containing `documentation.json` to understand the schema. From the FHIR API documentation, yes, for the FHIR-standard resources. The gap is that the (b)(10) export likely contains vendor-native resources not documented publicly.

**Machine-readable artifacts**: The FHIR CapabilityStatement at `w3.pcesecure.com` is a machine-readable declaration of supported resources. No machine-readable (b)(10) schema is publicly available.

## 7. Overall Assessment

### Classification

**Minimal/stub** — with important nuance.

The (b)(10) export mechanism itself appears thoughtfully designed: a purpose-built, native-format export with NDJSON, cross-references, self-describing schema, and non-computable file support. This is architecturally superior to many vendors' approaches. However, the **public documentation is a 3-page format specification with zero content enumeration**. Without access to an actual export's `documentation.json`, it is impossible to assess what the export contains, how many entities/tables it covers, or whether it includes behavioral health–specific data. The export may be comprehensive or minimal — there is no public evidence either way.

The FHIR API documentation (87 pages, 318 fields across 25 entities) is decent but represents a standard USCDI projection, not the native export model. It notably includes Claim and Coverage resources beyond USCDI requirements.

### Key Findings

1. **The (b)(10) export is a purpose-built, native-format system** — not a repackaged FHIR or C-CDA export. PCE explicitly designed a separate export mechanism with NDJSON, a self-describing JSON schema (`documentation.json`), cross-references between resources, and a `Files/` directory for non-computable content. This is architecturally sound. (Source: `b10_documentation.pdf`, all 3 pages)

2. **The data dictionary is entirely hidden from public view.** The `documentation.json` containing "all possible resource definitions" is embedded in the export ZIP itself. No sample `documentation.json`, no list of resources, no field counts are publicly available. This makes external compliance assessment impossible. (Source: `b10_documentation.pdf`, p. 2)

3. **The FHIR API goes beyond USCDI** by including Claim (22 fields) and Coverage (8 fields) resources. This confirms PCE stores billing/insurance data and exposes it through APIs. (Source: `PIX_9_4_API_Documentation.pdf`, pp. 67–68; `capability-statement.json`)

4. **Behavioral health–specific data (the product's core value) is not visible in any public documentation.** MichiCANS assessments, 42 CFR Part 2 consent records, structured treatment plans, intake/discharge records, and incident reports are all core to this EHR but have no representation in either the FHIR API or the (b)(10) documentation. (Source: absent from all downloaded artifacts; product capabilities per `product-research.md`)

5. **Both single-patient and bulk export are supported**, and the export is initiated by authorized EHR users through the system UI. (Source: `b10_documentation.pdf`, p. 1)

### Summary Stats

```
Classification:  Minimal/stub (well-designed format, but zero public content documentation)
Export format:   NDJSON in password-protected ZIP (native format)
Model type:      Native database (separate from FHIR API)
Entities:        N/A (not publicly documented; embedded in documentation.json)
Fields:          N/A (not publicly documented)
Descriptions:    N/A (not publicly documented; documentation.json contains descriptions per spec)
Sample data:     No
Bulk export:     Yes (per-patient and all-patient)
Domains covered: Unverifiable from public documentation
```

FHIR API (for reference, not the (b)(10) export):
```
Entities:        25 (22 FHIR resources + 3 helper types)
Fields:          318
Descriptions:    98.7% (314/318)
```

### Bottom Line

PCE Systems built a technically sound (b)(10) export mechanism with a native NDJSON format, self-describing schema, and non-computable file support — better architecture than many vendors. However, the public documentation is essentially a 3-page format specification that tells you nothing about what data is actually exported. A patient, provider, or regulator cannot determine whether behavioral health assessments, consent records, treatment plans, or billing data are included without performing an actual export and examining `documentation.json`. The single biggest gap is the complete absence of a public data dictionary — the export could be comprehensive, but there is no way to verify this from the available artifacts.
