# EHI Export Analysis: Genius Solutions Inc.

**Product**: ehrTHOMAS (Version 3)
**Analysis date**: 2026-02-15
**CHPL ID**: 15.05.05.2737.GENI.01.00.1.180802 (CHPL #9585)

## 1. Product Context

ehrTHOMAS is a certified EHR for small to mid-size ambulatory practices, developed by Genius Solutions Inc. (Warren, Michigan, est. 1986). It serves primarily **chiropractic**, **podiatry**, **physical therapy/occupational therapy**, and **general medicine** practices. The product is part of a larger suite:

- **ehrTHOMAS** — the clinical EHR component (touch-screen clinical documentation, CPOE, e-prescribing via DrFirst, lab integration with Quest Diagnostics, immunization management)
- **eTHOMAS** — the practice management/billing component (scheduling, insurance verification, claims submission, billing ledgers, remittance posting, patient statements, inventory tracking)
- **WritePad** — ancillary documentation module for customizable point-and-click clinical templates
- **ADAMS** — automated appointment reminder system

The product is certified for a broad range of criteria including CPOE for medications and labs ((a)(1)–(a)(3)), e-prescribing ((b)(3)), care plan ((b)(9)), patient portal/VDT ((e)(1)–(e)(3)), public health reporting ((f)(1)–(f)(2)), and FHIR APIs ((g)(7)–(g)(10)). Specialty content includes DRxContent™ for podiatry.

**What the export should cover**: Given the tightly integrated EHR + practice management suite, a complete EHI export should include: demographics, encounters, problems/conditions, medications/prescriptions, allergies, immunizations, vitals, lab orders/results, procedures, clinical notes, billing/claims, insurance information, care plans, and specialty-specific clinical data (chiropractic/podiatry templates).

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/ehi-export-page.html` (25,139 bytes) | Single HTML page containing all EHI export documentation: introduction, how-to instructions, and XML sample snippets for 8 data domains. Last-Modified: 2024-04-18. **Primary artifact.** | ★★★ Most informative |
| `downloads/EHI_Export1.jpg` (160 KB) | Screenshot of ehrTHOMAS Reports Menu showing the "Electronic Health Information (Export)" button. Also reveals the full application toolbar: Patients, Code Files, Appointments, Physicians, Signing Dashboard, Messages, Labs/Dx Orders, Dx Order, Immunization, Send Charges, Reports, Import, Logout. | ★★ Reveals product modules |
| `downloads/EHI_Export2.jpg` (218 KB) | Screenshot of single-patient export dialog. Shows Export Folder Path, "Single Patient" export type, patient search by last name/account number, and Export button. | ★ Confirms UI mechanics |
| `downloads/EHI_Export3.jpg` (177 KB) | Screenshot of bulk export dialog. Shows "All Patients (Entire Database)" export type. | ★ Confirms bulk capability |
| `downloads/screenshot-ehi-export-full-page.png` (1.2 MB) | Full-page browser screenshot of the documentation page as rendered. | ★ Redundant with HTML file |

**No additional artifacts exist.** No XSD schema, no downloadable sample export files, no data dictionary document, no PDF. The entire EHI export documentation is this single HTML page. The source URL remains live and returns HTTP 200 (verified 2026-02-15).

## 3. Export Mechanics

- **Format**: Proprietary XML (vendor-defined element names; not FHIR, C-CDA, or any recognized standard)
- **Mechanism**: Built-in UI function accessed via Reports Menu → "Electronic Health Information (Export)" button
- **Single-patient**: Yes — user selects "Single Patient" from dropdown, searches by last name or account number, selects patient, clicks Export
- **Bulk export**: Yes — user selects "All Patients (Entire Database)" from dropdown. Documentation notes this "may require support from the health IT developer"
- **Output location**: Files exported to a configurable local folder path (sample shows `C:\Users\RashidM\Documents\EHRElectronicHealthInformation\02`)
- **Access constraints**: User must have "full rights or system administrator" access, or the system administrator can run the export on their behalf
- **Fees**: Not mentioned in documentation
- **File structure**: Not documented. It is unclear whether the export produces one XML file per dataset, one file per patient, or a single combined file

## 4. Export Content: What's In It

The export documentation describes **8 XML datasets** containing a total of **96 leaf-level data fields** (corrected count; see `analysis/vital_fields_detail.py`). There is **no data dictionary** — the XML format is documented solely through sample XML snippets embedded in the HTML page. Zero fields have descriptions, type definitions, value set enumerations, or cardinality documentation. The only type annotations are `type="date"` and `type="time"` attributes on 18 elements.

### Vendor's own content organization

The vendor organizes the export into 8 "datasets" (their term). Counts below are corrected for the Vital Dataset's nested structure.

| Dataset | Leaf Fields | Coded Fields | Category |
|---|---|---|---|
| Patient Dataset | 22 | Race, Language, Ethnicity, Gender (no code systems specified) | Demographics |
| Encounter Dataset | 10 | None | Encounters |
| Device Dataset | 11 | Snomed (SNOMED CT) | Devices (UDI) |
| Immunization Dataset | 7 | CVXCode (CVX) | Immunizations |
| Allergy Dataset | 7 | SNOMED (SNOMED CT) | Allergies |
| Procedure Dataset | 9 | CPTCode (CPT) | Procedures |
| Vital Dataset | 21 | None | Vitals |
| Condition Dataset | 9 | ICD10Code (ICD-10, **but see note below**) | Conditions/Diagnoses |
| **Total** | **96** | | |

### Data quality issues in sample data

1. **Condition ICD10Code contains GUIDs, not ICD-10 codes**: The `ICD10Code` field in the Condition Dataset sample contains values like `f1f0bd65-a248-4930-b981-2531ed4fcd93` — internal database GUIDs rather than actual ICD-10 codes. The `ICD10Description` field has the diagnosis text ("ABRASION, LEFT LOWER LEG, INITIAL ENCOUNTER") but the code field appears broken or mapped to an internal key. This is a significant data quality concern.

2. **Encounter doctor fields populated with NPI**: All PerformingDoctor sub-fields (LastName, FirstName, MidInitial, TaxonomyCode) contain the NPI value `1234567897`. This appears to be a data masking artifact in the sample rather than a code bug, but it makes it impossible to verify from the documentation whether these fields actually work correctly.

3. **Sentinel null dates**: The value `1800-01-01T00:00:00` is used as a sentinel for null dates (seen in Encounter DischargeDate, Procedure ProcedureEndTime, and Condition OnSetDate). This is undocumented.

4. **Vital Dataset XML structural error**: In the second Vital sample record, a `<Unit>%</Unit>` element appears outside of any parent vital sign element (between SpO2 and FiO2), suggesting a structural bug in the XML output or documentation.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor's 8 datasets cover a narrow clinical summary:

- **Demographics** (Patient Dataset, 22 fields): Reasonably thorough for a single-entity demographic record. Includes SSN, multiple phone numbers, email, and demographic coding (race, language, ethnicity). Does **not** include insurance, emergency contacts, or preferred pharmacy.

- **Encounters** (10 fields): Minimal encounter shell — just dates, status, and performing doctor. No encounter type, reason for visit, location, or associated diagnoses/procedures linkage.

- **Devices** (11 fields): Good UDI coverage with standard identifiers (DeviceIdentifier, CarrierHRF, SNOMED).

- **Immunizations** (7 fields): Basic — CVX code, lot number, date. Missing manufacturer, route, site, administering provider.

- **Allergies** (7 fields): Basic — SNOMED coded, includes clinical status and reaction.

- **Procedures** (9 fields): Includes CPT codes and timing. Adequate for procedure records.

- **Vitals** (21 fields): The most detailed dataset. Covers temperature, blood pressure, pulse, respiration, SpO2, FiO2, height, weight, BMI with units.

- **Conditions** (9 fields): ICD-10 coded (though the code field contains GUIDs in the sample — see data quality issues). Includes clinical status and verification status.

**Notable pattern**: These 8 datasets correspond closely to USCDI v1 data classes and the data available through the vendor's FHIR (g)(10) API. The ehrTHOMAS help site navigation (from `_masterLayout.html`, per the prior report) lists FHIR resources including AllergyIntolerance, Condition, Encounter, Immunization, Patient, Procedure, and Observation — nearly the same set as the b(10) export. This strongly suggests the b(10) export was built from the same data layer as the FHIR API rather than from the native database model.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | Patient Dataset (22 fields): name, DOB, gender, SSN, address, phone, email, race/ethnicity/language | Covers core demographics but missing emergency contacts, insurance info, preferred pharmacy |
| Encounters / visits | ⚠️ Partial | Encounter Dataset (10 fields): dates, status, performing doctor | Very thin — no encounter type, reason, location, or facility |
| Problems / conditions / diagnoses | ⚠️ Partial | Condition Dataset (9 fields): ICD-10 (but GUID issue), status | Reasonable structure but ICD10Code data quality issue undermines it |
| Medications / prescriptions | ❌ Not covered | No Medication dataset in export | **Major gap.** ehrTHOMAS is certified for CPOE-Medications (a)(1), e-prescribing (b)(3), and integrates with DrFirst for EPCS. Medications are core clinical data. |
| Allergies | ✅ Covered | Allergy Dataset (7 fields): SNOMED coded | Basic but adequate |
| Immunizations | ✅ Covered | Immunization Dataset (7 fields): CVX coded | Basic but adequate |
| Vitals | ✅ Covered | Vital Dataset (21 fields): comprehensive vital signs | Good coverage including SpO2/FiO2 |
| Lab results | ❌ Not covered | No Lab dataset in export | **Major gap.** ehrTHOMAS is certified for CPOE-Lab (a)(2), integrates with Quest Diagnostics, and has a "Labs/Dx Orders" module visible in the UI toolbar. |
| Imaging / diagnostic reports | ❌ Not covered | No imaging dataset in export | WritePad can attach x-rays and images; these are not exported |
| Procedures | ✅ Covered | Procedure Dataset (9 fields): CPT coded | Adequate |
| Clinical notes / documents | ❌ Not covered | No notes/documents in export | **Major gap.** ehrTHOMAS has touch-screen templates, WritePad documentation module, and a "Signing Dashboard" visible in UI. Clinical notes are core EHI. |
| Care plans / goals | ❌ Not covered | No care plan dataset in export | ehrTHOMAS is certified for (b)(9) Care Plan. Gap. |
| Orders / referrals | ❌ Not covered | No orders dataset in export | "Dx Order" module visible in UI toolbar. eTHOMAS has referral tracking. Gap. |
| Insurance / coverage | ❌ Not covered | No insurance dataset in export | eTHOMAS handles insurance verification and claims. Gap. |
| Claims / billing | ❌ Not covered | No billing dataset in export | **Major gap.** eTHOMAS is a full practice management system with claims submission, billing ledgers, and "Send Charges" module visible in UI. Billing records are part of the designated record set. |
| Payments | ❌ Not covered | No payment dataset in export | eTHOMAS handles remittance posting and online payments. Gap. |
| Consents / directives | ❌ Not covered | No consent dataset in export | N/A — unclear if product stores advance directives |
| Patient communications | ❌ Not covered | No communications dataset in export | "Messages" module visible in UI toolbar. Gap. |
| Devices (UDI) | ✅ Covered | Device Dataset (11 fields): standard UDI identifiers | Good |
| Specialty-specific data | ❌ Not covered | No specialty content in export | ehrTHOMAS has DRxContent™ for podiatry, chiropractic-specific templates, and specialty clinical content. None of this appears in the export. Gap. |

**Summary**: 5 of 18 applicable domains are covered (✅), 3 are partially covered (⚠️), and 10 are not covered at all (❌). The 10 missing domains include **medications, lab results, clinical notes, and billing** — all core EHI that the product demonstrably stores.

## 6. Documentation Quality

The documentation consists of a single HTML page with:

- **Strengths**: Clean layout, annotated screenshots showing the export UI, sample XML for each dataset, and clear step-by-step instructions for running the export.
- **No data dictionary**: Zero fields have descriptions. A developer must infer field semantics from element names and sample values alone.
- **No schema**: No XSD, DTD, JSON Schema, or any formal format specification. The XML sample snippets embedded in the HTML are the only format documentation.
- **No value sets**: Fields like `Gender`, `ClinicalStatus`, `VerificationStatus`, `Race`, `MaritalStatus` show sample values but no enumeration of valid values.
- **No relationship documentation**: Entities are linked via `KeyId`/`PatientId`/`EncounterId` integer references, but these relationships are not formally documented.
- **No file structure documentation**: The page does not describe whether the export produces one XML file, multiple files, how files are named, or the overall structure of the export output.
- **No cardinality or optionality**: No documentation of which fields are required vs. optional, or whether elements can repeat.

**Could a developer build an import?** With significant effort and guesswork, a developer could parse the 8 documented datasets from the XML. However, they would have no way to know: (a) what values are valid for coded fields, (b) which fields may be empty, (c) how null values are represented beyond the 1800-01-01 sentinel, (d) whether there are additional XML elements not shown in the samples, or (e) the file/directory structure of the export output. The ICD10Code GUID issue would be a blocking problem for conditions data.

## 7. Overall Assessment

### Classification

**Partial native export** — ehrTHOMAS has built a dedicated b(10) export function that produces proprietary XML (not a repackaged FHIR or C-CDA export). However, it covers only 8 clinical data categories out of the ~18 EHI domains the product stores. The export appears to be scoped to the same clinical summary data available through the product's FHIR (g)(10) API, minus medications and labs — making it even narrower than their FHIR API. The complete absence of medications, lab results, clinical notes, and billing data means this falls well short of "all electronic health information."

### Key Findings

1. **Medications are entirely absent from the export.** ehrTHOMAS is certified for medication CPOE and e-prescribing (including controlled substances via DrFirst), yet the EHI export has no Medication dataset. This is the single most critical gap — a patient record without medications is not a meaningful health record. (Source: `ehi-export-page.html`, verified against certified criteria (a)(1), (b)(3))

2. **The export covers only 8 of ~18 applicable EHI domains.** Missing domains include lab results, clinical notes, billing/claims, insurance, care plans, orders/referrals, patient messages, and specialty-specific clinical data. The UI toolbar visible in `EHI_Export1.jpg` confirms the product has modules for Labs/Dx Orders, Messages, Dx Order, and Send Charges — none of which are represented in the export.

3. **There is no data dictionary, schema, or field documentation.** The XML format is documented solely through sample snippets. Zero of 96 fields have descriptions. No value sets, cardinality, or relationship documentation exists. (Source: `ehi-export-page.html`, exhaustive review)

4. **The Condition dataset has a data quality issue**: ICD10Code fields contain GUIDs (`f1f0bd65-a248-4930-b981-2531ed4fcd93`) instead of actual ICD-10 codes, rendering the coded diagnoses potentially unusable. (Source: `ehi-export-page.html`, Condition Dataset XML sample)

5. **The export appears scoped to FHIR API coverage minus medications and labs**, suggesting it was built from the same clinical data layer as the (g)(10) API rather than from the full native database model. This is even narrower than a typical USCDI clinical summary.

### Summary Stats

```
Classification:  Partial native export
Export format:   Proprietary XML
Model type:      Native (vendor-defined XML), but scoped like a standard projection
Entities:        8
Fields:          96
Descriptions:    0% (0 of 96 fields have descriptions)
Sample data:     Yes (XML snippets in HTML, not downloadable files)
Bulk export:     Yes (with possible developer assistance)
Domains covered: 5 of 18 applicable domains fully; 3 partial
```

### Bottom Line

The ehrTHOMAS EHI export is a genuine but severely incomplete effort. A patient would receive demographics, encounters, allergies, immunizations, vitals, procedures, devices, and conditions — but **no medications, no lab results, no clinical notes, and no billing records**. For a product that includes e-prescribing, lab integration, clinical documentation, and full practice management, exporting only 8 clinical summary datasets falls far short of the "all electronic health information" requirement of §170.315(b)(10). The single biggest gap is the complete absence of medication data from a product with robust e-prescribing capabilities.
