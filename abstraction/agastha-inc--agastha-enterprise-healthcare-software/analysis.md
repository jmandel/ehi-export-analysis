# EHI Export Analysis: Agastha, Inc.

**Product**: Agastha Enterprise Healthcare Software
**Analysis date**: 2026-02-16
**CHPL IDs**: 11152 (v20.1, certified 2022-12-28), 11616 (v25.1, certified 2025-03-25)

## 1. Product Context

Agastha Enterprise Healthcare Software is an integrated, cloud-based platform combining EHR, practice management, pharmacy management, laboratory information system (LIS), billing/claims, patient portal, e-prescribing (including EPCS), and telehealth into a single product. The company (~18 employees, Charlotte, NC) targets ambulatory practices, multi-specialty clinics, hospitals, pharmacies, and laboratories. Specialties served include primary care, internal medicine, oncology, neurology, dermatology, mental health, and pediatrics.

**What the export should cover**, given the product's capabilities:
- **Clinical data**: Encounter documentation, problem lists, medication lists, allergies, immunizations, vitals, lab results, clinical notes, care plans, imaging/diagnostics, procedures, clinical decision support alerts
- **Prescription data**: E-prescriptions, EPCS records, drug interaction history, refill requests
- **Lab/LIS data**: Lab orders, results, specimen tracking, device integration data
- **Pharmacy data**: Medication inventory, procurement, sales/billing, stock management
- **Billing/financial data**: Claims, invoices, insurance eligibility, payments, revenue cycle data
- **Patient demographics and insurance**: Registration, contacts, insurance/coverage information
- **Patient portal data**: Secure messages, portal access, appointment requests
- **Documents**: Clinical and administrative documents
- **Telehealth**: Virtual visit records, remote monitoring data

## 2. Artifacts Reviewed

| Artifact | Size | Description | Informativeness |
|---|---|---|---|
| `Agastha-B10-Documentation.pdf` | 586 KB, 7 pages | Primary (b)(10) documentation. Lists 21 FHIR R4 resources with generic FHIR spec descriptions, screenshots of the export UI, overview text. Created 2023-10-10. | **Primary** — sole source for (b)(10) export content |
| `dataExport.html` | 5 KB | EHI export landing page. Version history table (v1.0, 2023-04-10), link to B10 PDF, link to FHIR API docs. Product name/version: "Agastha Enterprise Healthcare Software / 20.1". | **Minimal** — adds only version history |
| `apiR4.html` | 215 KB, 50 tables | FHIR R4 API documentation for (g)(10). Documents 23 FHIR resources with API endpoints, search parameters, and example JSON responses. Includes OAuth/SMART authentication, Bulk Data endpoints. | **Supplementary** — not (b)(10) specific, but shows resource field examples |

The B10 PDF is the only artifact specifically documenting the (b)(10) EHI export. The apiR4.html is (g)(10) API documentation that provides supplementary context on FHIR resource structures.

## 3. Export Mechanics

- **Format**: FHIR R4 JSON (4.0.1) conforming to US Core IG STU V3.1.1 for 21 named resources, plus unspecified "standard JSON format" for unnamed "other resources"
- **Mechanism**: UI-based — a "Data Portability/Export" screen accessible to users with assigned roles (screenshot in PDF p2-3)
- **Single-patient**: Yes — search by patient account, optional date-of-service filter (date range, previous month, or none)
- **Group export**: Yes — comma-separated patient account IDs
- **Bulk/population export**: Yes — "All patients" radio button option
- **Access constraints**: Role-based — "clinical users with assigned rights" can generate exports
- **Fees**: Not documented
- **Standards referenced**: FHIR R4 4.0.1, US Core IG STU V3.1.1, HL7 FHIR Bulk Data export

## 4. Export Content: What's In It

### FHIR Resources Documented in B10 PDF

The B10 PDF lists exactly **21 FHIR R4 resources** exported in FHIR JSON format. The descriptions for all 21 are **copied verbatim from the FHIR R4 specification** — they describe generic FHIR resource definitions, not Agastha-specific mappings, extensions, or field details. There is **zero field-level documentation** — no element names, types, cardinality, value sets, or Agastha-specific mappings.

Additionally, the PDF states: *"All the other resources are currently exported using the standard JSON format."* This sentence implies additional data is exported beyond the 21 FHIR resources, but provides **no documentation whatsoever** about what those resources are, their structure, or their content.

### FHIR API Documentation (supplementary)

The apiR4.html (g)(10) documentation covers **23 FHIR resources** — the same 21 as the B10 PDF minus Location and Medication, plus 4 additional resources: **Appointment**, **ChargeItem**, **Coverage**, and **FamilyMemberHistory**. Each resource section includes API endpoints, search parameters, and example JSON responses.

The example JSON responses provide the closest thing to field-level documentation available. Across 20 resources with parseable examples, there are approximately **224 top-level fields** represented (counting each resource's example fields). These are standard FHIR elements with no vendor extensions visible.

### Vendor's own content organization

The vendor organizes resources only by the FHIR resource type names. There is no vendor-specific categorization (e.g., no "Billing" or "Clinical" groupings). The table below reflects the 21 resources explicitly listed in the B10 PDF:

| Resource | Example Fields (from API) | In B10 PDF | In API Docs | Category (FHIR) |
|---|---|---|---|---|
| AllergyIntolerance | 14 | ✅ | ✅ | Clinical |
| CarePlan | 10 | ✅ | ✅ | Clinical |
| CareTeam | 6 | ✅ | ✅ | Clinical |
| Condition | 12 | ✅ | ✅ | Clinical |
| Device | 10 | ✅ | ✅ | Clinical |
| DiagnosticReport | 14 | ✅ | ✅ | Clinical |
| DocumentReference | — | ✅ | ✅ | Clinical |
| Encounter | 12 | ✅ | ✅ | Clinical |
| Goal | 9 | ✅ | ✅ | Clinical |
| Immunization | 16 | ✅ | ✅ | Clinical |
| Location | — | ✅ | ❌ | Administrative |
| Medication | — | ✅ | ❌ | Clinical |
| MedicationRequest | 14 | ✅ | ✅ | Clinical |
| Observation | 9 | ✅ | ✅ | Clinical |
| Organization | 9 | ✅ | ✅ | Administrative |
| Patient | 15 | ✅ | ✅ | Administrative |
| Practitioner | 8 | ✅ | ✅ | Administrative |
| Procedure | 7 | ✅ | ✅ | Clinical |
| Provenance | 6 | ✅ | ✅ | Infrastructure |
| RelatedPerson | 9 | ✅ | ✅ | Administrative |
| ServiceRequest | — | ✅ | ✅ | Clinical |

**Additional resources in API docs but not in B10 PDF:**

| Resource | Example Fields | Category | Notes |
|---|---|---|---|
| Appointment | 12 | Administrative | Scheduling data |
| ChargeItem | 12 | Financial | Billing-related charge items |
| Coverage | 12 | Financial | Insurance coverage info |
| FamilyMemberHistory | 8 | Clinical | Family health history |

It is unclear whether these 4 additional resources are included in the (b)(10) export (possibly covered by the "other resources" clause) or are available only via the (g)(10) API.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The documented export covers the **standard US Core FHIR resource set** — the same resources that a (g)(10) FHIR API would expose. The 21 resources in the B10 PDF map directly to the US Core Implementation Guide profiles: Patient, Encounter, Condition, MedicationRequest, AllergyIntolerance, Immunization, Procedure, Observation, DiagnosticReport, DocumentReference, CarePlan, CareTeam, Goal, ServiceRequest, Device, Provenance, plus administrative resources (Organization, Practitioner, Location, RelatedPerson, Medication).

The supplementary API documentation adds ChargeItem and Coverage resources — the only financial resources visible anywhere in the documentation — but their inclusion in the (b)(10) export is not confirmed.

There is no documentation of any non-FHIR "standard JSON" resources despite the PDF's claim that "all the other resources" are exported in that format.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | `Patient` (15 fields in example) | Standard US Core Patient profile. Covers basics (name, DOB, gender, address, telecom, identifiers). May miss vendor-specific registration fields. |
| Encounters / visits | ⚠️ Partial | `Encounter` (12 fields in example) | Standard FHIR Encounter. Covers class, period, participants, diagnoses. Product stores richer encounter documentation. |
| Problems / conditions | ✅ Covered | `Condition` (12 fields in example) | Standard US Core Condition with clinical status, code, onset. |
| Medications / prescriptions | ⚠️ Partial | `MedicationRequest` (14 fields), `Medication` | Covers prescription orders. Does not document EPCS-specific data, pharmacy dispensing records, or prescription transmission details. |
| Allergies | ✅ Covered | `AllergyIntolerance` (14 fields in example) | Standard US Core AllergyIntolerance. |
| Immunizations | ✅ Covered | `Immunization` (16 fields in example) | Standard US Core Immunization with vaccine code, dose, lot, route, site. |
| Vitals | ⚠️ Partial | `Observation` (9 fields in example) | Observation covers vitals, labs, and social history together. No breakdown of which observation categories are exported. |
| Lab results | ⚠️ Partial | `DiagnosticReport` (14 fields), `Observation` | Standard FHIR diagnostic reports. Does not cover LIS-specific data (specimen tracking, barcodes, device connectivity). |
| Imaging / diagnostic reports | ⚠️ Partial | `DiagnosticReport` | DiagnosticReport includes media and presentedForm fields, but no detail on imaging-specific content. |
| Procedures | ✅ Covered | `Procedure` (7 fields in example) | Standard US Core Procedure — minimal fields (code, date, status). |
| Clinical notes / documents | ⚠️ Partial | `DocumentReference` | References to documents; actual content may be base64-encoded or linked. No detail on which note types are exported. |
| Care plans / goals | ✅ Covered | `CarePlan` (10 fields), `Goal` (9 fields) | Standard US Core CarePlan and Goal resources. |
| Orders / referrals | ✅ Covered | `ServiceRequest` | Standard FHIR ServiceRequest. |
| Insurance / coverage | ⚠️ Partial | `Coverage` in API docs only (12 fields) | Coverage resource exists in API docs but is NOT listed in B10 PDF. Uncertain if included in export. Product stores insurance/enrollment data. |
| Claims / billing | ❌ Not covered | No Claim, ClaimResponse, or ExplanationOfBenefit resources | Product has full billing/claims/RCM module. No billing resources in the documented export. ChargeItem in API only. **Significant gap.** |
| Payments | ❌ Not covered | No payment-related resources | Product processes payments via portal and billing module. Not represented. **Significant gap.** |
| Consents / directives | ❌ Not covered | No Consent resource | No evidence of consent/directive export. |
| Patient communications / portal messages | ❌ Not covered | No Communication resource | Product has patient portal with secure messaging. Not represented. **Gap.** |
| Pharmacy management | ❌ Not covered | No pharmacy-specific resources | Product has full pharmacy management (inventory, procurement, sales). None exported. **Significant gap.** |
| E-prescribing (EPCS details) | ❌ Not covered | MedicationRequest only covers orders | EPCS-specific records, transmission logs, controlled substance details not documented. |
| Telehealth | ❌ Not covered | No telehealth-specific resources | Product supports telehealth/remote monitoring. Not represented. |
| Specialty-specific data | ❌ Not covered | No specialty-specific resources | Product serves oncology, neurology, mental health, etc. No specialty assessments or custom forms documented. **Gap.** |
| Family history | ⚠️ Partial | `FamilyMemberHistory` in API only (8 fields) | In API docs but not in B10 PDF. Uncertain if in export. |

## 6. Documentation Quality

**Poor.** The documentation is inadequate for a developer to understand or use the export:

- **No data dictionary**: Zero field-level documentation. The B10 PDF provides only resource-level names with descriptions copied verbatim from the HL7 FHIR specification. No Agastha-specific field mappings, data types, cardinality, or constraints.
- **No sample data**: No example export files. The apiR4.html has JSON examples, but these are API response examples, not (b)(10) export samples.
- **No schema files**: No JSON Schema, FHIR StructureDefinitions, custom profiles, or OpenAPI specifications.
- **No documentation of non-FHIR content**: The claim that "all other resources are currently exported using the standard JSON format" is completely undocumented — no resource names, no field names, no structure, no examples.
- **No value sets or coded fields**: No documentation of which code systems or value sets are used for coded elements.
- **No relationship documentation**: Beyond implicit FHIR references, no documentation of how resources relate to each other.
- **Version mismatch**: The B10 PDF is version 20.1 (created 2023-10-10), but the newer certification is version 25.1 (certified 2025-03-25). The dataExport.html landing page also references version 20.1. Documentation has not been updated.
- **Helpful elements**: The export UI screenshots (PDF p2-3) clearly show how to access and use the export feature, including single-patient, group, and population export options with date filtering.

A developer receiving this export would be able to parse the FHIR JSON using standard FHIR libraries, but would have no guidance on Agastha-specific data mappings, the completeness of each resource, or the structure of any non-FHIR content.

## 7. Overall Assessment

### Classification

**Standard-based projection**: The (b)(10) export is the vendor's (g)(10) FHIR API repackaged with a user-facing "Data Portability/Export" interface. The 21 documented FHIR resources are the standard US Core set — the exact same resources exposed through the certified FHIR API. There is no evidence of native database export, and the undocumented "other resources" claim cannot be verified.

### Key Findings

1. **FHIR/(g)(10) repackaging**: The 21 FHIR resources listed in the B10 PDF are the standard US Core resource set. The apiR4.html confirms these are the same resources served by the (g)(10) FHIR API. This is a textbook case of a vendor relabeling their FHIR API as a (b)(10) EHI export.

2. **Major data domains missing**: The product integrates billing/claims, pharmacy management, LIS, patient portal messaging, e-prescribing (EPCS), and telehealth — none of which have documented export content. Only ChargeItem and Coverage appear in the supplementary API docs (not in the B10 PDF itself).

3. **Zero field-level documentation**: All 21 resource descriptions are copied verbatim from the FHIR R4 specification. There are no Agastha-specific mappings, no field-level detail, no value sets, and no sample data specific to the (b)(10) export.

4. **Ambiguous "other resources" claim**: The PDF's statement that "all the other resources are currently exported using the standard JSON format" is a potentially significant but completely undocumented claim. If these other resources cover billing, pharmacy, and specialty data, the export could be more comprehensive than it appears — but without any documentation, this is impossible to verify.

5. **Outdated documentation**: The B10 PDF (v20.1, 2023) has not been updated for the current certified version (v25.1, 2025), raising questions about whether the export has evolved without corresponding documentation updates.

### Summary Stats

```
Classification:  Standard-based projection
Export format:   FHIR R4 JSON (+ undocumented "standard JSON" for unnamed resources)
Model type:      Standard projection (US Core FHIR R4)
Entities:        21 (documented in B10 PDF) / 25 (including API-only resources)
Fields:          ~224 (from API example JSON; no field-level docs in B10)
Descriptions:    0% vendor-specific (all copied from FHIR spec)
Sample data:     No (API examples only, not export samples)
Bulk export:     Yes (single patient, group, and population)
Domains covered: 6-7 of 18+ applicable domains (clinical core only)
```

### Bottom Line

This is a minimal-effort (b)(10) implementation that repackages the standard FHIR/(g)(10) API as an EHI export. For a product that integrates EHR, billing/claims, pharmacy management, LIS, patient portal, e-prescribing, and telehealth, exporting only 21 standard US Core FHIR resources with zero field-level documentation leaves the majority of the product's data domains unaddressed. The biggest gap is the complete absence of documented billing, pharmacy, and specialty clinical data from the export — data domains that constitute a substantial portion of what this integrated platform stores about patients.
