# EHI Export Analysis: Health Information Management Systems, LLC

**Product**: Axiom (Version 7)
**Analysis date**: 2026-02-15
**CHPL ID**: 15.04.04.1590.Axio.02.01.1.201229 (CHPL #10512)

## 1. Product Context

Axiom is a **cloud-based, integrated EHR platform purpose-built for behavioral health and integrated healthcare providers**, developed by Health Information Management Systems, LLC (HiMS) of Tucson/Phoenix, Arizona. Founded in 2014, HiMS is a small, niche vendor targeting behavioral health clinics, addiction treatment centers, developmental disability (DD) and foster care facilities, and FQHCs.

Axiom is not a narrow clinical module — it is a full-stack platform encompassing:

- **Clinical documentation**: AI-powered note-taking, customizable dynamic forms, clinical decision support, e-signatures
- **Practice management & scheduling**: appointment scheduling, text/voice reminders
- **Billing & RCM**: full revenue cycle management — claims submission, eligibility verification, payment posting, HCPCS/CPT/ICD-10 coding, contract management
- **E-prescribing & labs**: full e-prescribing, lab orders and results
- **Telehealth**: built-in HIPAA-compliant video visits
- **Patient portal** (Axiom Connect): health record access, secure messaging, appointment scheduling
- **Mobile** (AxiomMobile): iOS/Android clinician app
- **Specialty modules**: Electronic Visit Verification (EVV) for Medicaid services, DD/foster care support, CRM/intake tracking

This breadth means a complete EHI export should cover clinical documentation (including behavioral health assessments), demographics, medications, labs, billing/claims, insurance, and specialty data (EVV, DD/foster care records).

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `Axiom-EHI-Export-Instructions.pdf` (188 KB, 4 pages) | The sole EHI export documentation. Contains step-by-step instructions with screenshots for single-patient and bulk export. Created 2026-01-30 by CEO Khalid Maskari. | **Primary artifact** — but extremely thin. No data dictionary, no schema, no format specification, no sample data. |
| `screenshot-ehi-export-page.png` (175 KB) | Full-page screenshot of https://axiomehr.com/ehiexport/. Shows a simple page with a heading and a "Download PDF" button — nothing else. | **Low value** — confirms no additional web-based documentation exists. |
| EHI export web page (live verification) | Fetched https://axiomehr.com/ehiexport/ on 2026-02-15. Returns HTTP 200 with heading "Axiom EHI Export Instructions" and the same PDF download link. No additional content. | **Confirms** no documentation beyond the PDF. |

**Total documentation surface area**: 4 PDF pages (1 cover page, ~1 page of text instructions, ~2 pages of screenshots). No data dictionary. No sample export files. No machine-readable schemas.

## 3. Export Mechanics

**Format**: Unknown. The exported file is a password-encrypted ZIP archive with a GUID filename (e.g., `1BA97693-8CC0-4C82-A96F-FF42748F15AA.zip`). The documentation does not describe what file format(s) are inside the ZIP — it could be PDFs, CSVs, JSON, FHIR, XML, or any other format. There is simply no information.

**Mechanism**: UI-driven. Users navigate to the Report page, enter a patient name and date range, select "Form Types" from a dropdown, click "BUILD REPORT," select individual forms/encounters via checkboxes, then choose "EHI Export" from an action dropdown. The export is generated asynchronously; the user is notified when it's ready.

**Single-patient**: Yes — documented with screenshots. The user selects a specific patient and specific forms/encounters to export.

**Bulk export**: Claimed in 2 sentences on page 4: "The request for patient population export will include all population data. The export file(s) will be compressed to reduce file size." No further detail — no screenshots, no steps, no scope definition, no mechanism described.

**Access constraints**: The exported ZIP is password-encrypted. The password is emailed to both the employee and the patient. Any file compression tool can be used to decompress.

**Fees**: Not mentioned.

## 4. Export Content: What's In It

### What the documentation tells us

The documentation provides **no data dictionary, no field definitions, no table names, no schema, and no format specification**. It is impossible to determine from the documentation alone what structured data the export contains.

What we can infer from the screenshots is that the export operates on a **per-form, per-encounter basis**. The "Form Types" dropdown lists clinical forms and encounters that can be selected for export. The visible form types (from the dropdown and export results across pages 2–4) include:

**Dynamic Forms** (clinical assessment forms):
- AccountLogin
- Active Meds Test
- ADAD Test Form (Adolescent Drug Abuse Diagnosis)
- Adult ADHD Self-Report Scale (ASRS-v1)
- Adult Brief Psychosocial Assessment (2 variants)
- Advance Directive Form
- Agency - Encounter Form Signature
- AKDA
- All Tools Form
- allow fax 1
- 13-17 EPSDT (Early and Periodic Screening, Diagnostic and Treatment — a Medicaid form)
- NPP Weekly Progress Report

**Encounters**:
- CPT Note
- CM 3.0 (Case Management)

The dropdown shows only ~12 items of what appears to be a longer alphabetical list (scrollbar visible). The complete list of available form types is not documented.

### What the documentation does NOT tell us

- **Export format**: What is inside the ZIP? Rendered PDFs of forms? Structured data files? Database tables?
- **Field-level content**: No field names, no data types, no value sets, no relationships
- **Data scope**: Does the export include demographics, medications, labs, allergies, immunizations, vitals, billing, insurance? Completely unknown.
- **Structured vs. rendered**: Are forms exported as structured data (field names + values) or as rendered documents (e.g., PDF printouts of filled forms)?

### Vendor's own content organization

The vendor does not organize export content into categories. The only organizing concept is "Form Types" — a flat list of dynamic forms and encounter types available in the system. No categories, no groupings, no domain taxonomy is provided.

| Evidence Source | Content Visible | Notes |
|---|---|---|
| Form Types dropdown (p2) | ~12 dynamic form names (behavioral health assessments, misc.) | Alphabetical list, truncated by scrollbar |
| Export results list (p3) | 4 items: 1 EPSDT form, 2 progress reports, 1 CPT encounter note | For a single test patient (KING, TERRY) |
| Export history (p4) | 1 item: Encounter - CM 3.0 | Single completed export |

**No entity/field table can be generated** because no data dictionary exists.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor's export documentation describes a **form-level document export system**, not a structured data export. Users select clinical forms and encounter types from a list and export them as encrypted ZIP files. The visible form types are overwhelmingly **behavioral health clinical assessments** (ADHD scales, psychosocial assessments, EPSDT screenings, progress reports) and **encounter notes** (CPT notes, case management notes).

There is **no evidence** in the documentation that the export covers:
- Structured patient demographics
- Medication lists or e-prescribing records
- Lab orders or results
- Allergies or immunizations
- Vitals
- Insurance/coverage information
- Claims, billing, or payment data
- Patient portal messages
- EVV records
- DD/foster care specialty data
- Care plans or referrals

The "Form Types" dropdown *may* contain forms that capture some of this data (e.g., "Active Meds Test" could relate to medications), but the documentation provides no way to verify what data these forms contain or how comprehensively they capture structured clinical data vs. free-text assessments.

The bulk export section's claim that it "will include all population data" is undefined — "all population data" could mean all forms for all patients, or all structured data in the system. The documentation does not clarify.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ❌ Not covered | No demographic entity in documentation. Export screenshots show patient name/ID only as metadata. | Product stores demographics (per product research); gap if not in export, but **cannot confirm** from documentation. |
| Encounters / visits | ⚠️ Partial | Encounter types visible (CPT Note, CM 3.0), but only as document-level exports — no structured encounter data | Product has encounters; export may capture encounter documents but not structured encounter data. |
| Problems / conditions / diagnoses | ❌ Not covered | No diagnosis-specific form visible in screenshots | Product stores diagnoses (certified for (a)(4) Problem List); not evidenced in export. |
| Medications / prescriptions | ❌ Not covered | "Active Meds Test" form visible but appears to be a test form, not a medication export | Product has full e-prescribing; no medication data entity in export. |
| Allergies | ❌ Not covered | No allergy-related form or entity visible | Product certified for (a)(3) Maintain Allergies; not evidenced in export. |
| Immunizations | ❌ Not covered | No immunization form visible | Product certified for (b)(1) Immunization Information; not evidenced in export. |
| Vitals | ❌ Not covered | No vitals form visible | Product likely stores vitals; not evidenced in export. |
| Lab results | ❌ Not covered | No lab-related form visible | Product has lab integration; not evidenced in export. |
| Imaging / diagnostic reports | N/A | Not applicable — behavioral health product | Not expected for this product type. |
| Procedures | ❌ Not covered | No procedure entity visible | Product stores procedure data (CPT codes for billing); not evidenced in export. |
| Clinical notes / documents | ⚠️ Partial | Progress reports, CPT notes, psychosocial assessments visible as form types | Form-based clinical documents appear to be the primary export content, but scope is unclear. |
| Care plans / goals | ❌ Not covered | No care plan form visible in screenshots | Product likely stores treatment/service plans; not evidenced. |
| Orders / referrals | ❌ Not covered | No order or referral form visible | Not evidenced in export. |
| Insurance / coverage | ❌ Not covered | No insurance entity visible | Product does eligibility verification; not evidenced in export. |
| Claims / billing | ❌ Not covered | No billing entity visible | Product has full RCM (claims, payments, coding); significant gap if absent. |
| Payments | ❌ Not covered | No payment entity visible | Product has payment posting; not evidenced in export. |
| Consents / directives | ⚠️ Partial | "Advance Directive Form" visible in form types dropdown | One form type visible; coverage unclear. |
| Patient communications / portal messages | ❌ Not covered | No portal message entity visible | Product has Axiom Connect patient portal with secure messaging; not evidenced. |
| Specialty-specific (behavioral health) | ⚠️ Partial | Behavioral health assessment forms visible (ADHD, ASAM, psychosocial, EPSDT) | These are the strongest visible content, but documented only as form names — no field-level detail. |

**Summary**: Of 18 applicable domains, **0 are confirmed covered**, **4 show partial evidence** (encounters, clinical notes, consents, behavioral health specialty), and **14 show no evidence** in the documentation. However, this assessment is limited by the complete absence of a data dictionary — it is possible the export contains more than what the screenshots reveal, but the documentation provides no way to verify this.

## 6. Documentation Quality

The documentation quality is **extremely poor** — among the thinnest possible for a certified (b)(10) export.

**What exists**:
- A 4-page PDF (1 cover page + ~3 pages of instructions/screenshots)
- Step-by-step instructions for initiating an export via the UI
- Screenshots of the export interface

**What is entirely absent**:
- **No data dictionary** — zero field names, types, or descriptions
- **No format specification** — the contents of the exported ZIP are completely undocumented
- **No schema** — no machine-readable or human-readable data model
- **No sample data** — no example export files
- **No entity/table inventory** — no list of what data categories are exported
- **No relationships** — no foreign keys, no entity relationships
- **No value sets** — no coded values, no terminology references

**Could a developer build an import?** No. A developer receiving an export from Axiom would have to reverse-engineer the file format, field names, data types, value sets, and relationships entirely on their own. The documentation provides zero guidance on what to expect inside the exported ZIP.

**Quality indicators**:
- Contains typos: "informaiton" (p2), "cllick" (p2), "compresses" (p4)
- Created in Microsoft Word, suggesting minimal technical investment
- Bulk export section is 2 sentences with no detail
- No version history or change log

## 7. Overall Assessment

### Classification

**Minimal/stub**

The entire (b)(10) EHI export documentation is a 4-page PDF with UI screenshots showing how to click an "EHI Export" button. There is no data dictionary, no schema, no format specification, no sample data, and no description of what data categories the export covers. The documentation demonstrates that an export *button* exists but provides no evidence that the export comprehensively covers the data Axiom stores, and no way for anyone to understand or use the exported data.

### Key Findings

1. **The entire EHI export documentation is 4 PDF pages with no data dictionary** (`Axiom-EHI-Export-Instructions.pdf`, 188 KB). It contains a cover page, ~1 page of instructions, and ~2 pages of screenshots. No field names, no data types, no entity lists, no format specs.

2. **The export format is completely undocumented.** The output is a password-encrypted ZIP file, but what's inside the ZIP (PDF? CSV? JSON? FHIR? Database dump?) is never stated. A recipient cannot know what to expect.

3. **The export appears to be a form/document-level export, not a structured data model export.** The UI shows users selecting individual "Form Types" (behavioral health assessment forms, encounter notes) for export — this is closer to a document download than a database export. No structured entities (demographics, medications, labs, billing) are visible.

4. **No evidence of billing, medication, lab, insurance, or most clinical data domains in the export.** Axiom is a full-stack EHR with built-in RCM, e-prescribing, lab integration, and patient portal — but the export documentation shows only behavioral health forms and encounter notes. The gap between what the product stores and what the export demonstrably covers is vast.

5. **Bulk export is asserted but not documented.** The claim that "patient population export will include all population data" appears in 2 sentences with no supporting detail — no steps, no screenshots, no scope definition, no mechanism.

### Summary Stats

```
Classification:  Minimal/stub
Export format:   Unknown (encrypted ZIP; contents undocumented)
Model type:      Unknown (appears to be form/document-level export)
Entities:        N/A (no data dictionary)
Fields:          N/A (no data dictionary)
Descriptions:    N/A (no data dictionary)
Sample data:     No
Bulk export:     Claimed but undocumented
Domains covered: 0 of 17 confirmed; 4 of 17 show partial evidence
```

### Bottom Line

Axiom's EHI export documentation is a minimal compliance stub — it proves an "EHI Export" button exists in the UI but provides no evidence that the export comprehensively covers the clinical, billing, and specialty data that this full-stack behavioral health EHR stores. The complete absence of a data dictionary, format specification, or sample data means a recipient of the export would have no way to understand or use the data. This is one of the thinnest (b)(10) documentation packages possible for a product of Axiom's breadth.
