# EHI Export Analysis: Health Information Management Systems, LLC

**Product**: Axiom Version 7
**Analysis date**: 2026-02-16
**CHPL IDs**: 10512 (15.04.04.1590.Axio.02.01.1.201229)

## 1. Product Context

Axiom is a **cloud-based, integrated EHR platform purpose-built for behavioral health and integrated healthcare providers**, developed by Health Information Management Systems, LLC (HiMS), headquartered in Arizona. It is not a narrow clinical module — it encompasses:

- **Clinical documentation**: AI-powered note-taking, customizable clinical templates, drag-and-drop form builder, e-signatures, clinical decision support
- **Behavioral health-specific**: ASAM assessments, psychosocial assessments, EPSDT forms, developmental disability (DD) and foster care support, Electronic Visit Verification (EVV)
- **Practice management & scheduling**: Appointment scheduling, text/voice reminders
- **Billing & RCM**: Full revenue cycle management — claims submission, eligibility verification, payment posting, HCPCS/CPT/ICD-10 coding, AI-driven coding recommendations
- **E-prescribing & labs**: Full e-prescribing, lab integration and results management
- **Patient portal (Axiom Connect)**: Health record access, scheduling, secure messaging
- **Telehealth**: Built-in HIPAA-compliant virtual sessions
- **Reporting & analytics**: AI report builder, predictive analytics, practice KPIs

Target users include behavioral health clinics, addiction treatment centers, integrated health providers, FQHCs, and developmental disability/foster care facilities. Notable customers include COPE Community Services (15,000+ clients in Pima County, AZ).

**Baseline for export completeness**: A genuine "all EHI" export from Axiom should cover clinical encounter notes, behavioral health assessments/forms, diagnoses, medications, prescriptions, lab results, allergies, treatment/care plans, billing/claims data, insurance information, patient demographics, patient portal communications, and specialty behavioral health data (EVV, DD records).

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `Axiom-EHI-Export-Instructions.pdf` (187,728 bytes, 4 pages) | The sole EHI export documentation. Contains a cover page, ~1 page of step-by-step instructions for single-patient export, ~2 pages of screenshots, and a 2-sentence description of bulk export. Created 2026-01-30 by Khalid Maskari using Microsoft Word. | **Low** — procedural instructions only; no data dictionary, no schema, no format specification, no sample data |
| `screenshot-ehi-export-page.png` (174,638 bytes) | Full-page screenshot of https://axiomehr.com/ehiexport/. Shows a simple page with a purple hero banner, "Axiom EHI Export Instructions" heading, and a single "Download PDF" button. Footer shows "AxiomEHR is a part of Radicle Health." | **Minimal** — confirms the web page is a single download link with no additional documentation |
| https://axiomehr.com/ehiexport/ (verified live 2026-02-16) | The vendor's EHI export page. Confirmed accessible; contains only the heading "Axiom EHI Export Instructions" and the PDF download link. No additional content, data dictionary, or schema on the page. | **Minimal** — verified still live and unchanged |

**Total artifacts with substantive export documentation: 1** (the 4-page PDF). There is no data dictionary, no schema, no sample data, and no format specification in any artifact.

## 3. Export Mechanics

- **Format**: Password-encrypted compressed ZIP file. The format of files inside the ZIP is **not documented** — no indication whether contents are PDFs, CSVs, JSON, FHIR resources, or any other format.
- **Mechanism**: UI-based. Users access the Report page in Axiom EHR, enter patient name and parameters (date range, form types), click "BUILD REPORT," select documents to export, then choose "EHI Export" from an action dropdown.
- **Single-patient**: Supported. User selects a patient and specific form types/documents to export.
- **Bulk export**: Claimed. The PDF states: "The request for patient population export will include all population data. The export file(s) will be compressed to reduce file size." No further details on mechanism, timing, or scope.
- **Delivery**: The ZIP file's password is emailed to both the employee and the patient.
- **File naming**: GUID-based (e.g., `1BA97653-8CC0-4C82-A96F-FF42748F15AA.zip`).
- **Access constraints / fees**: Not mentioned in the documentation.

## 4. Export Content: What's In It

### What can be determined

The documentation provides **zero field-level detail** about export contents. There is no data dictionary, no schema, no entity list, no field definitions, no format specification, and no sample data. The only evidence of what the export contains comes from:

1. **Form Types visible in the screenshot dropdown** (page 2): A scrollable list showing ~12 form type names, primarily behavioral health dynamic forms
2. **Export record list** (page 3): Shows 4 selected items for export
3. **Export History table** (page 4): Shows column headers and one completed export record
4. **Bulk export claim**: "all population data" (undefined)

### Observable form types from screenshots

The following form type names are visible in the PDF screenshots (the dropdown is scrollable — this is only a partial view):

**From page 2 (Form Types dropdown):**
- Dynamic Form: AccountLogin
- Dynamic Form: Active Meds Test
- Dynamic Form: ADAD Test Form
- Dynamic Form: Adult ADHD Self-Report Scale (ASRS-v1...)
- Dynamic Form: Adult Brief Pscyhosocial Assessment - Dra...
- Dynamic Form: Advance Directive Form
- Dynamic Form: Agency - Encounter Form Signature
- Dynamic Form: AKDA
- Dynamic Form: All Tools Form
- Dynamic Form: allow fax 1

**From page 3 (export record list for patient KING, TERRY):**
- Dynamic Form: 13-17 EPSDT
- Dynamic Form: NPP Weekly Progress Report
- Encounter: CPT Note

**From page 4 (export history):**
- Encounter - CM 3.0

These 13 unique form type names suggest the export is **document/form-based** — it exports completed clinical forms and encounter notes, not structured data tables. The form types are predominantly behavioral health assessment instruments (ASAM, ADHD Self-Report Scale, Psychosocial Assessment, EPSDT) and encounter types (CPT Note, Case Management).

### Vendor's own content organization

No content organization is provided by the vendor. There is no table of entities, fields, or data categories. The only organizational concept visible is the distinction between "Dynamic Form" types and "Encounter" types in the Form Types dropdown.

| Category (inferred from screenshots) | Observable Items | Fields Documented | Types Documented | Descriptions |
|---|---|---|---|---|
| Dynamic Forms (behavioral health assessments) | ~10 visible (scrollable list, total unknown) | 0 | No | No |
| Encounters (CPT notes, case management) | ~2 visible | 0 | No | No |

**Total entities formally documented: 0**
**Total fields formally documented: 0**
**Fields with descriptions: 0**

### Export History table columns

The only "field-level" information in the entire documentation is the column headers of the EHI Export History table (page 4):

| Column | Example Value |
|---|---|
| Rec | 461053 |
| Patient Name | KING, TERRY |
| Patient # | TK10140210 |
| Patient Id | 81662 |
| Form Type | Encounter - CM 3.0 |
| Form Date | 11/26/2023 |
| File Name | 1BA97653-8CC0-4C82-A96F-FF42748F15AA.zip |
| Status | Completed |

These describe the export tracking metadata, not the exported data itself.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor's documentation provides **no information about data coverage**. The export appears to be a document-level export system where users select clinical forms and encounter notes by type and date range. Based solely on the form type names visible in screenshots:

- **Behavioral health assessments** are represented: ASAM, ADHD Self-Report Scale, Psychosocial Assessment, ADAD Test Form, EPSDT, and several others
- **Encounter notes** are represented: CPT Notes, Case Management encounters
- **Advance Directives** appear in the form types list
- **Medication-related**: "Active Meds Test" appears as a form type (unclear if this is a medication list or a test form)

The bulk export section claims to include "all population data" but provides no definition of what that encompasses. It is impossible to determine from the documentation whether the export includes demographics, medications, lab results, billing data, or any other domain beyond clinical forms/encounters.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ❓ Unknown | Not documented. Patient name/ID visible in export UI but unclear if demographic data is in the exported ZIP. | Product stores demographics; cannot assess from documentation. |
| Encounters / visits | ⚠️ Partial evidence | "Encounter: CPT Note" and "Encounter - CM 3.0" visible as exportable form types. | Some encounter types visible, but scope of encounter data within exports is undocumented. |
| Problems / conditions / diagnoses | ❓ Unknown | Not documented. | Product stores diagnoses; cannot assess. |
| Medications / prescriptions | ❓ Unknown | "Dynamic Form: Active Meds Test" visible but unclear if this exports medication data or is an assessment form. E-prescribing is a core feature. | Product has full e-prescribing; no evidence of medication/Rx data in export. |
| Allergies | ❓ Unknown | Not documented. | Product likely stores allergies; cannot assess. |
| Immunizations | ❓ Unknown | Not documented. | Behavioral health product; may not be primary data. N/A or minimal gap. |
| Vitals | ❓ Unknown | Not documented. | Product may store vitals for integrated care; cannot assess. |
| Lab results | ❓ Unknown | Not documented. | Product has lab integration; cannot assess. |
| Imaging / diagnostic reports | N/A | Not mentioned. | Behavioral health product — imaging not a core function. |
| Procedures | ❓ Unknown | Not documented. | Cannot assess. |
| Clinical notes / documents | ⚠️ Partial evidence | Multiple "Dynamic Form" types visible (behavioral health assessments, progress notes). This appears to be the primary export content. | Clinical forms/notes appear to be the focus, but scope and depth are undocumented. |
| Care plans / goals | ❓ Unknown | Not documented. | Product stores treatment plans; cannot assess. |
| Orders / referrals | ❓ Unknown | Not documented. | Cannot assess. |
| Insurance / coverage | ❓ Unknown | Not documented. | Product stores insurance data; cannot assess. |
| Claims / billing | ❓ Unknown | Not documented. Product has full RCM. | Product has comprehensive billing/RCM; no evidence of billing data in export. Potentially significant gap. |
| Payments | ❓ Unknown | Not documented. | Product handles payment posting; cannot assess. |
| Consents / directives | ⚠️ Partial evidence | "Dynamic Form: Advance Directive Form" visible in dropdown. | At least one consent-related form type exists. |
| Patient communications / portal messages | ❓ Unknown | Not documented. Product has patient portal (Axiom Connect). | Cannot assess. |
| Specialty-specific (behavioral health) | ⚠️ Partial evidence | ASAM, ADHD Self-Report Scale, Psychosocial Assessment, ADAD, EPSDT, NPP Weekly Progress Report visible as form types. | Behavioral health forms are represented but total scope is unknown. EVV and DD/foster care records not mentioned. |

**Key finding**: The documentation is so thin that coverage assessment is largely impossible. Most domains are "Unknown" — not because they're confirmed absent, but because the documentation provides no information about what data the export contains. The only domains with any evidence are clinical forms/encounters (visible in screenshots) and advance directives.

## 6. Documentation Quality

The documentation quality is **extremely poor** — among the worst possible for a certified (b)(10) export:

- **No data dictionary**: Zero entities, zero fields documented
- **No schema**: No structural description of the export whatsoever
- **No format specification**: The format of files inside the exported ZIP is not stated (could be PDF, CSV, JSON, XML, or anything else)
- **No sample data**: No examples of exported content
- **No value sets or code systems**: Not applicable (no fields documented)
- **No relationships**: Not applicable (no entities documented)
- **Machine-readable artifacts**: None

**What exists**: A 4-page PDF with a cover page, basic procedural instructions ("login, go to Report page, click BUILD REPORT"), 5 screenshots of the export UI, and a 2-sentence paragraph about bulk export. The PDF contains typos ("informaiton," "cllick").

**Could a developer build an import?** No. A developer receiving this export would have to reverse-engineer the ZIP file contents with no guidance. They would not know the format, the fields, the data types, the encoding, or the relationships between records. The documentation tells you how to click the export button but nothing about what comes out.

## 7. Overall Assessment

### Classification

**Minimal/stub**: The documentation is too thin to assess what the export actually covers. The 4-page PDF is purely procedural (how to click buttons in the UI) with zero technical content about the exported data. There is no data dictionary, no schema, no format specification, no sample data, and no description of what data domains are included. The bulk export claim of "all population data" is unsubstantiated by any detail.

### Key Findings

1. **The entire EHI export documentation is a 4-page PDF containing only UI click instructions and screenshots** — no data dictionary, no schema, no format specification, no sample data. This is the thinnest possible documentation for a certified (b)(10) export. (Source: `Axiom-EHI-Export-Instructions.pdf`)

2. **The export format is completely undocumented.** The output is a password-encrypted ZIP file, but what's inside the ZIP — the actual data format (CSV, JSON, PDF, FHIR, etc.) — is never stated. A recipient would have no way to know what to expect or how to parse the contents. (Source: PDF page 4)

3. **The export appears to be document/form-based rather than structured data.** The UI shows users selecting "Dynamic Form" types and "Encounter" types for export, suggesting the system exports rendered clinical documents rather than structured database tables. This is consistent with a behavioral health EHR where clinical forms are the primary data artifact, but it raises questions about whether structured data (demographics, medications, lab results, billing) is captured. (Source: PDF pages 2-3 screenshots)

4. **Billing/RCM data — a major product capability — has no evidence of inclusion.** Axiom has full built-in revenue cycle management (claims, eligibility, payments, coding), but the export documentation shows only clinical forms and encounter types. There is no mention of billing entities, claims, payments, or financial data. (Source: absence in PDF; product capabilities from product-research.md)

5. **The bulk export feature is described in exactly two sentences** with no detail on what "all population data" means, how it's triggered, or what the output contains. (Source: PDF page 4)

### Summary Stats

```
Classification:  Minimal/stub
Export format:   Password-encrypted ZIP (internal format undocumented)
Model type:      Unknown (possibly document/form-based export)
Entities:        0 (no data dictionary)
Fields:          0 (no field-level documentation)
Descriptions:    N/A
Sample data:     No
Bulk export:     Claimed (two sentences, no detail)
Domains covered: Cannot assess — documentation too thin (partial evidence for 3-4 of ~15 applicable domains)
```

### Bottom Line

The Axiom EHI export documentation is a minimal compliance stub — a 4-page PDF that shows users how to click an export button but provides zero information about what data is actually exported, in what format, or how to interpret it. A patient or developer receiving this export would have to reverse-engineer the ZIP file contents with no guidance. The single biggest gap is the complete absence of any data dictionary, schema, or format specification — making it impossible to assess whether the export actually covers "all electronic health information" as required by 170.315(b)(10).
