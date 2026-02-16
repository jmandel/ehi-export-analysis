# EHI Export Analysis: CareCloud Health, Inc.

**Product**: CareCloud Charts v3.0
**Analysis date**: 2026-02-16
**CHPL ID**: 15.04.04.2981.Care.03.01.1.221229

## 1. Product Context

CareCloud Charts is a cloud-based ambulatory EHR serving 40,000+ providers across multiple specialties (internal medicine, cardiology, gastroenterology, orthopedics, etc.). It is part of CareCloud's integrated platform that includes:

- **CareCloud Charts** — EHR (clinical documentation, e-prescribing, lab/imaging orders, clinical decision support)
- **CareCloud Central** — Practice management (scheduling, billing, claims submission, denial management, revenue cycle)
- **CareCloud Breeze** — Patient engagement (portal, digital intake forms, secure messaging, online payments)
- **CareCloud Live** — Telehealth

The product stores clinical data (encounters, problems, medications, allergies, labs, vitals, immunizations, procedures, notes), administrative/financial data (claims, charges, CPT/ICD codes, insurance/eligibility, payments, denial records), and patient engagement data (portal messages, intake forms, appointment requests, online payments). This is relevant because a genuine (b)(10) export should cover data across all these integrated modules.

## 2. Artifacts Reviewed

| Artifact | Description | Informative? |
|---|---|---|
| `downloads/ehi-export-documentation.pdf` | 11-page PDF (457 KB). Core documentation: export overview, step-by-step instructions for single/bulk CCD export, CCD data dictionary mapping 82 data elements to CDA XPaths and code systems, brief descriptions of 6 PDF export types, and a single-sentence FHIR mention. Created 2023-11-14 by Rico Lopez. | **Primary source** — only substantive artifact |
| `downloads/screenshot-box-page.png` | Screenshot of Box.com shared link showing the PDF is accessible. | Minimal — confirms access only |

**Notable absence**: No sample export files, no FHIR resource documentation, no machine-readable schemas, no data dictionary beyond the CCD XPath mapping table.

## 3. Export Mechanics

CareCloud Charts describes three export mechanisms:

1. **Single Patient CCD Export**: Via Patient Application → Print Icon → "Clinical Summary CCD" → downloads XML file. This is the standard C-CDA clinical summary export.

2. **Bulk Patient CCD Export**: Via Analytics Application → Clinical → Patient List → filter → Options → Render Format: CDA → Run Report → downloads ZIP of XML files. This appears to be the existing clinical reporting/exchange feature repurposed.

3. **PDF Exports**: Via Analytics Application, clients can export demographics/insurance, appointments, messages, and claims in PDF format. Documents (signed notes, lab results, radiology reports, scanned documents) are also exported as PDFs organized by type.

4. **FHIR Bulk Data Export**: A single sentence states the FHIR Server "supports FHIR Bulk Data EHI Export for the patient population as described in §170.315(b)(10)(ii)." No detail on which FHIR resources, no documentation, no API endpoints.

**Access**: UI-driven (no API documented beyond the undocumented FHIR reference). Both single-patient and bulk export are available.

**Format**: C-CDA XML for clinical data; PDF for billing/demographics/messages/documents; FHIR (undocumented).

## 4. Export Content: What's In It

### CCD Data Dictionary (C-CDA Clinical Export)

The PDF documents 24 C-CDA sections containing 82 data elements mapped to CDA XPaths and code systems. This is a standard C-CDA 2.1 clinical summary — the same document type used for transitions of care under (b)(1)/(b)(2)/(b)(3). The sections and element counts:

| CCD Section | Elements | Code Systems |
|---|---|---|
| Patient Demographics/Information | 6 | AdministrativeGender, Race & Ethnicity - CDC |
| Provider Information | 3 | — |
| Date and Location of Visit | 2 | — |
| Chief Complaint and Reason for Visit | 1 | — |
| Encounters | 5 | CPT, SNOMED, ICD10 |
| Immunizations | 9 | CVX, CPT-4, NCI Thesaurus, SNOMED |
| Instructions | 1 | SNOMED |
| Treatment Plan | 2 | LOINC |
| Social History | 3 | LOINC, SNOMED |
| Problems | 3 | SNOMED, ICD10 |
| Medications | 5 | RxNorm, NDC |
| Medication Allergies | 4 | RxNorm, SNOMED |
| Laboratory Tests | 4 | LOINC |
| Laboratory Information | 5 | — |
| Laboratory Results | 5 | LOINC |
| Vitals | 2 | LOINC |
| Goals | 3 | — |
| Procedures | 2 | CPT-4, SNOMED, HCPCS |
| Care Team Members | 3 | — |
| Reason for Referral | 1 | SNOMED |
| Medical Equipment | 2 | SNOMED |
| Mental Status | 4 | SNOMED |
| Functional Status | 4 | SNOMED |
| Health Concern | 3 | SNOMED |

These are precisely the standard C-CDA sections required for USCDI clinical exchange — no vendor-specific extensions, no custom sections, no data beyond what a standard CCD contains.

### PDF Exports (Non-Clinical Data)

Six document types are exported as PDFs, each described in a single sentence with no field-level documentation:

1. **Patient Demographic/Insurance** — "comprehensive view of patient's demographics and insurance details"
2. **Advance Directive** — "comprehensive view of patient's Advance Directive"
3. **Appointments** — "comprehensive view of patient's Appointments"
4. **Provider-to-Patient Messages** — "comprehensive view of messages"
5. **Billing Data (Claim)** — "comprehensive view of billing data (CPT, ICD, Modifier)"
6. **Documents** — "signed progress notes, available lab results, radiology reports and any other scanned or uploaded document"

No data dictionary exists for any of these PDF exports. The documentation provides zero detail about what fields are included, how data is structured, or what "comprehensive" means in practice. PDF format means the data is not machine-readable.

### FHIR Bulk Data Export

One sentence on page 11: "CareCloud Charts' FHIR Server creates a single-patient FHIR resource Document Reference and supports FHIR Bulk Data EHI Export for the patient population as described in §170.315(b)(10)(ii)."

No documentation of which FHIR resource types are exported, no field mappings, no API details. The mention of "Document Reference" as a single-patient resource and generic reference to (b)(10)(ii) suggests this may be their existing (g)(10) FHIR API relabeled.

### Vendor's Own Content Organization

| Entity/Component | Fields Documented | Descriptions | Types | Category (vendor's) |
|---|---|---|---|---|
| CCD - Patient Demographics | 6 | 0 | No | Clinical Data (CCD) |
| CCD - Encounters | 5 | 0 | No | Clinical Data (CCD) |
| CCD - Immunizations | 9 | 0 | No | Clinical Data (CCD) |
| CCD - Problems | 3 | 0 | No | Clinical Data (CCD) |
| CCD - Medications | 5 | 0 | No | Clinical Data (CCD) |
| CCD - Medication Allergies | 4 | 0 | No | Clinical Data (CCD) |
| CCD - Laboratory (Tests+Info+Results) | 14 | 0 | No | Clinical Data (CCD) |
| CCD - Vitals | 2 | 0 | No | Clinical Data (CCD) |
| CCD - All other sections (14 sections) | 34 | 0 | No | Clinical Data (CCD) |
| Patient Demographic/Insurance (PDF) | 0 | N/A | N/A | PDF Export |
| Advance Directive (PDF) | 0 | N/A | N/A | PDF Export |
| Appointments (PDF) | 0 | N/A | N/A | PDF Export |
| Provider-to-Patient Messages (PDF) | 0 | N/A | N/A | PDF Export |
| Billing Data/Claim (PDF) | 0 | N/A | N/A | PDF Export |
| Documents (PDF) | 0 | N/A | N/A | PDF Export |
| FHIR Data Export | 0 | N/A | N/A | FHIR Bulk Data |

**Total documented fields**: 82 (CCD only; 0 descriptions beyond field names)

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

CareCloud's export has three tiers of documentation quality:

1. **CCD clinical data** (best documented): 24 standard C-CDA sections with 82 data elements mapped to XPaths and code systems. However, this is simply the standard CCD template — it contains exactly what any C-CDA 2.1 implementation would contain, with no product-specific depth. There are no vendor extensions, no additional fields from CareCloud's internal data model.

2. **PDF exports** (mentioned but undocumented): Six categories of data — demographics/insurance, advance directives, appointments, messages, billing/claims, and documents — are exported as PDFs. The documentation devotes one sentence to each with no field-level detail. These PDFs do cover domains beyond USCDI (billing, appointments, messages), which is a positive signal that the vendor is attempting some breadth. However, PDF format makes the data non-machine-readable, and the complete absence of documentation means we cannot assess depth.

3. **FHIR export** (essentially undocumented): One sentence mentions FHIR Bulk Data support. No resource types, fields, or API details are provided.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | CCD: 6 elements (name, sex, DOB, race, ethnicity, language); PDF: "demographics" mentioned | CCD covers USCDI minimum only; PDF may have more but undocumented |
| Encounters / visits | ⚠️ Partial | CCD: 5 elements (code, performer, diagnosis, location, date) | Standard CCD encounter section; likely missing internal encounter details |
| Problems / conditions | ⚠️ Partial | CCD: 3 elements (problem, status, active date) | USCDI minimum; product likely stores more (onset, severity, linked orders) |
| Medications / prescriptions | ⚠️ Partial | CCD: 5 elements (medication, directions, start/end date, status) | Standard CCD medications; no prescribing workflow data, no pharmacy details |
| Allergies | ⚠️ Partial | CCD: 4 elements (substance, reaction, severity, status) | USCDI minimum |
| Immunizations | ✅ Covered | CCD: 9 elements (vaccine, date, status, route, site, manufacturer, dose, lot, notes) | Relatively thorough for CCD |
| Vitals | ⚠️ Partial | CCD: 2 elements (observation, date/time) | Very thin — no individual vital types documented |
| Lab results | ⚠️ Partial | CCD: 14 elements across 3 sub-sections | Standard CCD lab results |
| Imaging / diagnostic reports | ⚠️ Partial | PDF: "radiology reports" mentioned in Documents export | Only as scanned/uploaded PDFs; no structured imaging data |
| Procedures | ⚠️ Partial | CCD: 2 elements (procedure, date) | USCDI minimum |
| Clinical notes / documents | ✅ Covered | PDF: "signed progress notes...and any other scanned or uploaded document" | Exported as PDFs; appears to include full document set |
| Care plans / goals | ⚠️ Partial | CCD: Goals (3 elements), Treatment Plan (2 elements), Care Team (3 elements) | Standard CCD sections |
| Orders / referrals | ⚠️ Partial | CCD: Reason for Referral (1 element) | Very thin; no order details, no order sets, no order tracking |
| Insurance / coverage | ⚠️ Partial | PDF: "insurance details" mentioned | No field-level documentation; PDF only |
| Claims / billing | ⚠️ Partial | PDF: "billing data (CPT, ICD, Modifier)" | Mentioned but only as PDF; no structured data dictionary; product has full RCM capabilities |
| Payments | ❌ Not covered | No mention in any export component | Product processes payments (Central PM, Breeze online payments); significant gap |
| Consents / directives | ⚠️ Partial | PDF: Advance Directive export | Mentioned as PDF export; no detail |
| Patient communications | ⚠️ Partial | PDF: "Provider-to-Patient Messages" | Mentioned as PDF export; no detail |
| Specialty-specific data | ❌ Not covered | No specialty-specific entities or sections | Product serves 12+ specialties with configurable templates; no specialty data in export |

## 6. Documentation Quality

The documentation is **poor**. Key deficiencies:

- **No data dictionary for PDF exports**: Six categories of data are exported as PDFs with zero field-level documentation. A developer could not build an import or even know what to expect.
- **CCD data dictionary is just the C-CDA standard**: The 82 data elements documented are standard CDA XPaths and code systems — this is the C-CDA 2.1 specification, not a product-specific data dictionary. Any C-CDA implementation would contain these same elements.
- **No FHIR documentation**: The FHIR export gets one sentence. No resource types, no field mappings, no API endpoints.
- **No descriptions**: Zero of 82 CCD fields have descriptions beyond their name. No types are documented. No relationships. No value sets (only code system OIDs).
- **No sample data**: No sample exports, no example files, no screenshots of PDF output.
- **No machine-readable artifacts**: No JSON schemas, no FHIR CapabilityStatements, no data dictionaries in any parseable format.
- **11 pages total**: 5 pages are step-by-step instructions with screenshots for the CCD export UI. The remaining 6 pages are the CCD data dictionary (standard C-CDA XPaths) and one-sentence descriptions of PDF exports.

A developer could not build a useful import from this documentation. The CCD portion would require consulting the C-CDA 2.1 specification directly. The PDF exports are completely opaque.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Partial**

The export *mentions* domains beyond USCDI clinical data — billing/claims, appointments, insurance, messages, and documents are listed as PDF exports. This is better than a pure C-CDA repackaging. However, the clinical data export (CCD) is exactly the standard C-CDA clinical summary with no additional depth, and the non-clinical exports are in non-machine-readable PDF format with zero documentation. The product has significant capabilities in practice management, revenue cycle, and patient engagement that are either missing (payments, specialty data, intake forms, denial management) or present only as opaque PDFs. The breadth attempt is real but incomplete and poorly documented.

**Axis 2 — Export approach: Repackaged existing export**

The core clinical export is unmistakably the existing C-CDA clinical summary — the same export used for transitions of care (b)(1)/(b)(2)/(b)(3). The documentation explicitly references the C-CDA 2.1 standard (§170.205(a)(4)) and the data dictionary maps exactly to standard CCD sections. The PDF exports appear to be existing reporting/print features repurposed for (b)(10). The FHIR mention appears to reference the existing (g)(10) API. There is no evidence of a purpose-built export that maps CareCloud's internal data model to a structured, documented format. The vendor has bolted PDF printouts of a few additional data categories onto their existing C-CDA export and called it (b)(10).

### Key Findings

1. **CCD export is the standard C-CDA clinical summary repackaged as (b)(10)**: The 82 documented data elements across 24 sections map exactly to the C-CDA 2.1 template with no vendor extensions or additional depth. This is the same export used for transitions of care.

2. **PDF exports add some breadth but are non-machine-readable and undocumented**: Billing, insurance, appointments, messages, and documents are exported as PDFs — a positive breadth signal, but with zero field-level documentation and no machine-readable format. This makes the data practically unusable for import.

3. **FHIR Bulk Data is mentioned in a single sentence with no documentation**: The one-sentence reference to FHIR Bulk Data EHI Export provides no detail on resource types or coverage. It appears to be the (g)(10) API referenced generically.

4. **Significant data domains are missing**: Payments, specialty-specific clinical data, digital intake forms (Breeze), denial management records, and detailed revenue cycle data are absent from the export despite being core product capabilities.

5. **Documentation is too thin to be independently useful**: 11 pages total, with the CCD dictionary being a restatement of the C-CDA standard and PDF exports getting one sentence each. No sample data, no schemas, no descriptions.

### Summary Stats

    Coverage:        Partial
    Approach:        Repackaged existing export
    Export format:   C-CDA XML (clinical) + PDF (billing/demographics/messages/documents) + FHIR (undocumented)
    Entities:        31 (24 CCD sections + 6 PDF export types + 1 FHIR reference)
    Fields:          82 (CCD only; PDF and FHIR exports have 0 documented fields)
    Descriptions:    0% (field names only; no descriptions)
    Sample data:     No
    Bulk export:     Yes (CCD bulk via Analytics; FHIR bulk mentioned)
    Domains covered: 0 fully, 14 of 17 partially, 2 not covered, 1 N/A

### Bottom Line

CareCloud Charts' (b)(10) export is primarily their existing C-CDA clinical summary with PDF printouts of billing, insurance, appointments, and messages bolted on. While the PDF exports demonstrate some awareness that (b)(10) requires more than USCDI clinical data, the non-machine-readable format and complete absence of field-level documentation make them practically unusable. The single biggest gap is the lack of structured, documented export of the product's substantial practice management and revenue cycle data — despite CareCloud Central being a core product module with full billing, claims, and payment capabilities.
