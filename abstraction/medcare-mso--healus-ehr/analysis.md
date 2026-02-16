# EHI Export Analysis: Medcare MSO

**Product**: HealUs EHR v1.0
**Analysis date**: 2026-02-15
**CHPL ID**: 11495 (15.05.05.3197.MDCR.01.00.1.240715)

## 1. Product Context

HealUs EHR is a cloud-based ambulatory EHR developed by Medcare MSO, a healthcare revenue cycle management (RCM) and medical billing company headquartered in Irvine, California. The product was ONC-certified in July 2024, making it relatively new to market. HealUs EHR is part of a broader Medcare MSO ecosystem that includes Maximus (practice management/billing), AI Scribe (clinical documentation), and AI Medical Coding.

The product is broadly certified across 37 ONC criteria including CPOE (medications, labs, imaging), drug interaction checks, demographics, e-prescribing (via DrFirst), transitions of care (C-CDA), clinical information reconciliation, patient portal (view/download/transmit), clinical quality measures (7 CQMs), public health reporting (immunization registry, syndromic surveillance), FHIR APIs (g)(7)-(g)(10), and Direct messaging (via EMR Direct).

**Data the product stores (baseline for completeness assessment):**
- Patient demographics
- Medication orders and e-prescriptions
- Laboratory and imaging orders
- Allergies and drug interaction data
- Implantable device records
- Problem lists, conditions, diagnoses
- Clinical notes/charting
- Encounters and visit data
- Lab results, imaging results, procedure results
- Immunization records
- Referrals
- Advance directives
- Documents (scanned, uploaded)
- Patient portal content and patient-submitted health information
- Insurance eligibility information
- Appointment/scheduling data

**Ambiguous boundary**: Whether billing/claims data lives in HealUs EHR or exclusively in the separate Maximus PMS is unclear. Medcare MSO markets these as distinct products, so billing data may be out of scope for the HealUs EHR (b)(10) certification. However, the HealUs website does mention eligibility verification as a core feature.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `EHI.pdf` (681 KB, 6 pages) | The complete EHI export documentation. A Word-to-PDF document created 2024-04-22 by Ramsha Rasheed. 5 content pages + 1 blank. Describes export formats, workflow steps, and data categories at a high level. **No data dictionary, no field definitions, no sample data.** | **Primary source** — but very thin |
| `fhir-capability-statement.json` (27 KB) | FHIR R4 CapabilityStatement from `fhirapi.medcaremso.com`. Identifies 27 resource types (standard US Core set), `export` operation, and Bulk Data Access support. | **Informative** — confirms FHIR export is standard US Core with no vendor extensions |
| `screenshot-ehi-page.png` (171 KB) | Screenshot of the HealUs Knowledge Hub Angular SPA showing the EHI documentation page with sidebar navigation (All APIs, Security, Data Export, Predictive DSIs). | **Minimal value** — confirms the PDF is the only EHI documentation |

The screenshot confirms the documentation site structure: the "Data Export" section contains only "Electronic Health Information" which renders the same PDF. No additional data dictionaries, schemas, or sample data are available elsewhere on the site.

## 3. Export Mechanics

- **Format**: Mixed — C-CDA XML, FHIR R4 JSON, CSV, and PDF
- **Mechanism**: UI-based. Users navigate to "Data Export" in quick links, select patient(s) and date range, choose sections, and download.
- **Single-patient**: Yes. Documented step-by-step in the PDF (page 4).
- **Bulk/population**: Yes. Same workflow but selecting multiple or all patients (page 4).
- **Access control**: Practice administrator can approve export requests. Users can export "at any time without the developer assistance."
- **Timeliness**: Files exported "in real time" per the documentation.
- **Password protection**: Optional — users can check a "Confidential" checkbox for password-protected exports.
- **Fees/constraints**: None mentioned in the documentation.

## 4. Export Content: What's In It

### No data dictionary exists

The EHI documentation provides **zero field-level detail**. There are no field names, no data types, no value sets, no relationships, no column specifications for the CSV exports, no content descriptions for the PDF exports. The entire documentation is at the data-category level only.

### Vendor's own content organization

The PDF (pages 3–5) describes 11 export categories. Since no field-level documentation exists, field counts cannot be determined:

| Entity/Category | Export Format | Fields Documented | Types | Description Quality |
|---|---|---|---|---|
| Patient Demographics | CSV | 0 | No | One sentence: "comprehensive view of patient demographics" |
| Appointments | PDF + CSV | 0 | No | One sentence: "comprehensive view of appointments in both formats" |
| Lab Results | PDF | 0 | No | One sentence: "comprehensive view of laboratory results" |
| Imaging Results | PDF | 0 | No | One sentence: "comprehensive view of imaging results" |
| Procedure Results | PDF | 0 | No | One sentence: "comprehensive view of procedure results" |
| Encounters | PDF | 0 | No | One sentence: "comprehensive view of all data associated with encounters" |
| Referrals | PDF | 0 | No | One sentence: "comprehensive view of referrals" |
| Advance Directives | PDF | 0 | No | One sentence: "comprehensive view of advance directives" |
| Documents | PDF | 0 | No | Two sentences describing organizational structure with category subfolders |
| Clinical Data (C-CDA) | XML (C-CDA) | Standard | Standard | References HL7 CDA R2 IHE Health Story Consolidation DSTU 1.1 |
| Clinical Data (FHIR) | JSON (FHIR R4) | Standard | Standard | References US Core IG STU 4.0.0 + Bulk Data Access v1.0.1 |

**Total categories**: 11
**Categories with field-level documentation**: 0
**Categories exported as non-computable PDF**: 7 of 11 (64%)
**Categories in computable format**: 4 (CSV: 2, C-CDA: 1, FHIR: 1)

### FHIR capability detail

The CapabilityStatement at `fhirapi.medcaremso.com/api/R4/metadata` identifies 27 resource types. This is a standard US Core resource set with no custom resources or vendor-specific extensions:

AllergyIntolerance, CarePlan, CareTeam, Condition, Coverage, Device, DiagnosticReport, DocumentReference, Encounter, Endpoint, Goal, Group, Immunization, Location, Medication, MedicationDispense, MedicationRequest, Observation, Organization, Patient, Practitioner, PractitionerRole, Procedure, Provenance, RelatedPerson, ServiceRequest, Specimen

The server instantiates the `us-core-server` and `bulk-data` capability statements and supports the `export` operation. No vendor-specific extensions or custom resources are present.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor organizes export content into 11 categories spanning clinical data, results, demographics, appointments, referrals, advance directives, and documents. The clinical data categories (C-CDA and FHIR) cover the standard USCDI clinical domains. The remaining 9 categories attempt to go beyond USCDI by including appointments, referrals, advance directives, encounters, documents, and various results — but 7 of these 9 are exported only as PDF, which severely limits their utility as computable data.

**Richest areas**: Clinical data via C-CDA and FHIR covers the standard clinical domains (problems, medications, allergies, immunizations, vitals, procedures, care plans, goals) in computable formats. Patient demographics and appointments are in CSV — computable but undocumented.

**Thinnest areas**: Every non-clinical category gets a single boilerplate sentence of documentation (e.g., "comprehensive view of [X], structured for clarity and ease of access"). No category has any field-level detail. The PDF format for 7 categories makes them essentially non-computable.

**Absent entirely**: No billing, claims, charges, payments, or insurance data. No medication administration records beyond C-CDA standard content. No patient portal or patient-submitted data. No clinical decision support data. No messaging or communication data.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | "Patient Demographics" category in CSV. No column specification provided. | Format is computable (CSV) but completely undocumented — unknown what fields are included |
| Encounters / visits | ⚠️ Partial | "Encounters" category in PDF; also Encounter resource in FHIR | PDF is non-computable; FHIR covers standard US Core Encounter only |
| Problems / conditions / diagnoses | ⚠️ Partial | C-CDA and FHIR (Condition resource) | Standard projection only — no vendor-specific fields or custom data |
| Medications / prescriptions | ⚠️ Partial | C-CDA and FHIR (MedicationRequest, MedicationDispense) | Standard projection. Product has e-prescribing via DrFirst; prescription transmission details likely not exported |
| Allergies | ⚠️ Partial | C-CDA and FHIR (AllergyIntolerance) | Standard projection only |
| Immunizations | ⚠️ Partial | C-CDA and FHIR (Immunization) | Standard projection only |
| Vitals | ⚠️ Partial | C-CDA and FHIR (Observation) | Standard projection only |
| Lab results | ⚠️ Partial | "Lab Results" in PDF; DiagnosticReport + Observation in FHIR | PDF is non-computable; FHIR covers standard profiles only |
| Imaging / diagnostic reports | ⚠️ Partial | "Imaging Results" in PDF; DiagnosticReport in FHIR | PDF is non-computable |
| Procedures | ⚠️ Partial | "Procedure Results" in PDF; Procedure resource in FHIR | PDF is non-computable; FHIR standard only |
| Clinical notes / documents | ⚠️ Partial | "Documents" in PDF with category subfolders; DocumentReference in FHIR | Scanned/uploaded documents exported as PDF copies, which is reasonable. But no structured note export beyond what C-CDA provides |
| Care plans / goals | ⚠️ Partial | CarePlan, Goal resources in FHIR | Standard US Core profiles only |
| Orders / referrals | ⚠️ Partial | "Referrals" in PDF; ServiceRequest in FHIR | PDF is non-computable; FHIR standard only |
| Insurance / coverage | ⚠️ Partial | Coverage resource in FHIR CapabilityStatement | FHIR supports Coverage resource, but EHI PDF doesn't mention insurance data. Product has eligibility verification; uncertain what's actually exported |
| Claims / billing | ❌ Not covered | No billing entities in any export format | Billing may live in separate Maximus PMS. If any billing data is in HealUs EHR, this is a gap. |
| Payments | ❌ Not covered | No payment data in any export format | Same ambiguity as billing — likely in Maximus |
| Consents / directives | ⚠️ Partial | "Advance Directives" in PDF | PDF-only export; no structured data |
| Patient communications / portal messages | ❌ Not covered | Not mentioned in export documentation | Product has patient portal (e)(1) and patient-submitted data (e)(3); no evidence these are exported |

**Summary**: 0 of 17 applicable domains are fully covered with computable, documented export. 13 domains have partial coverage (standard projections via C-CDA/FHIR and/or non-computable PDF). 3 domains (billing, payments, portal communications) have no coverage, though billing/payments may be out of scope if they reside in Maximus PMS. No domain has vendor-specific field-level documentation.

## 6. Documentation Quality

The documentation quality is **very poor**.

**What exists**: A 5-page (content) PDF that describes 11 data categories at a category level, provides step-by-step UI instructions for triggering an export, and references the C-CDA and FHIR standards used. The document also notes organizational structure for exported documents (category subfolders).

**What's missing**:
- **No data dictionary** — zero field definitions for any export format
- **No CSV column specifications** — a developer receiving demographics CSV would have to reverse-engineer every column
- **No PDF content descriptions** — no indication of what fields appear in the PDF exports for encounters, lab results, etc.
- **No sample data** — no example exports of any format
- **No schemas** — no XSD, JSON Schema, CSV header specification, or any machine-readable format definition
- **No relationship documentation** — no description of how entities link (e.g., encounters to results, patients to documents)
- **No value sets or coded fields** — no documentation of any coded values or enumerations
- **No C-CDA or FHIR customization documentation** — no indication of whether the vendor uses any extensions or custom templates beyond the base standards

**Could a developer build an import from this documentation?** No. A developer would need to: (1) request an actual export and reverse-engineer the CSV columns, (2) write PDF parsing/OCR code to extract data from 7 categories of PDF output, (3) assume standard C-CDA/FHIR profiles with no vendor-specific guidance. The documentation is insufficient for any practical data portability purpose.

## 7. Overall Assessment

### Classification

**Minimal/stub** — The documentation is too thin to fully assess export completeness, and the export design relies heavily on non-computable PDF format (7 of 11 categories). The clinical data components (C-CDA and FHIR) are standard projections covering only USCDI data. There is no native data model export and no field-level documentation for any category.

### Key Findings

1. **No data dictionary exists.** The entire EHI export documentation is a 5-page PDF (EHI.pdf, created 2024-04-22) with zero field-level definitions. Every data category gets a single boilerplate sentence of description. No fields, types, relationships, value sets, or schemas are documented anywhere. (Source: `EHI.pdf`, pages 3–5)

2. **64% of export categories are PDF-only.** Seven of 11 data categories (lab results, imaging results, procedure results, encounters, referrals, advance directives, documents) are exported only as PDF. While the vendor calls these "interpretable, machine-readable PDF," PDF is a presentation format, not a computable data format. This fundamentally undermines the purpose of electronic data export. (Source: `EHI.pdf`, pages 4–5)

3. **The FHIR and C-CDA components are standard (g)(10) repackaging.** The FHIR CapabilityStatement (`fhir-capability-statement.json`) confirms 27 standard US Core resource types with no custom resources or vendor extensions. The C-CDA export references standard HL7 CDA R2 IHE Health Story Consolidation. These cover the same USCDI clinical data available via the (g)(10) standardized API — they are not a native data model export. (Source: `fhir-capability-statement.json`)

4. **Billing data is entirely absent.** Despite Medcare MSO being primarily a billing/RCM company, the EHI export documentation makes no mention of billing records, charges, claims, payments, or insurance information. If any billing data resides in HealUs EHR rather than the separate Maximus PMS, this is a significant gap. (Source: absence from `EHI.pdf`)

5. **The export does attempt to go beyond USCDI.** In fairness, the vendor includes categories not typically in a C-CDA or FHIR clinical summary: appointments, referrals, advance directives, encounters, and scanned documents. The CSV format for demographics and appointments is computable. The document-category subfolder organization shows some thought. But the lack of documentation and PDF format choice severely limits the practical value. (Source: `EHI.pdf`, pages 4–5)

### Summary Stats

```
Classification:  Minimal/stub
Export format:   Mixed (C-CDA XML, FHIR R4 JSON, CSV, PDF)
Model type:      Standard projection (C-CDA + FHIR) with PDF supplements
Entities:        11 data categories (no entity/table-level detail)
Fields:          N/A (no field-level documentation)
Descriptions:    N/A (0% — no fields documented)
Sample data:     No
Bulk export:     Yes
Domains covered: 0 fully, 13 partially, of 17 applicable domains
```

### Bottom Line

HealUs EHR's EHI export is a minimal compliance effort. The clinical core is standard C-CDA and FHIR repackaging covering only USCDI data, while most additional data categories are exported as non-computable PDFs with no field-level documentation. A patient or provider receiving this export would get standard clinical summaries plus a collection of PDFs that would require manual review or OCR to use — not a usable, complete copy of their data. The single biggest gap is the complete absence of any data dictionary or field-level documentation, which makes it impossible to programmatically consume or validate the export.
