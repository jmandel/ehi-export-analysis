# EHI Export Analysis: Genensys LLC

**Product**: Simplify EMR v4.0
**Analysis date**: 2026-02-16
**CHPL IDs**: 10317 (15.05.05.1523.GENS.01.00.1.200225)

## 1. Product Context

Simplify EMR is a cloud-based, ONC-certified EHR and integrated practice management system developed by Genensys LLC, a small (~12-employee) healthcare IT company in Florida. The product targets small to mid-sized independent practices, with a notable specialty focus on pediatric therapy clinics (OT, PT, speech therapy, ABA). The certified product (35+ criteria) encompasses a unified platform combining:

- **Clinical EHR**: Patient charting, problem lists, medication lists, allergies, immunizations, vitals, lab results, procedures, clinical notes with customizable templates, CPOE, drug interaction checking, implantable device tracking, family health history, clinical decision support
- **E-Prescribing**: Via MDToolBox integration, including controlled substances (EPCS)
- **Lab Integration**: Electronic ordering, result receipt, trending, abnormal alerts
- **Practice Management**: Scheduling, billing, claims management, eligibility checks, authorization management, rules-based claims editing, revenue cycle management
- **Patient Portal**: Secure messaging, bill pay, appointment requests, prescription renewals, lab results viewing
- **Interoperability**: FHIR APIs (g)(10), Direct messaging, C-CDA exchange, public health reporting (immunization registries, syndromic surveillance)
- **Therapy-specific features**: Pediatric therapy dashboards, specialty-specific templates and workflows

This is a full-featured ambulatory EHR+PM system. A genuine (b)(10) export should cover clinical records, billing/claims, patient portal data, e-prescribing transactions, and therapy-specific structured assessments — not just clinical summaries.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/ehi-export-doc.txt` (808 bytes) | Plain text export of the Google Doc — the entire (b)(10) documentation. 22 lines describing export folder structure and file naming. | **Primary source** — but extremely minimal |
| `downloads/ehi-export-doc.pdf` (39 KB, 2 pages) | PDF version of the same Google Doc, titled "Simplify EMR b(10) Export Format" | Same content as .txt, confirmed via `pdftotext` extraction |
| `downloads/ehi-export-doc.docx` (7.8 KB) | DOCX version preserving formatting and embedded hyperlink to USCDI v1 errata PDF | Same content; confirms the USCDI v1 reference link |
| `downloads/google-doc-screenshot.png` (71 KB) | Screenshot of title page | Shows document header "Simplify EMR / Export Format" |
| `downloads/google-doc-screenshot-page2.png` (131 KB) | Screenshot of content page | Full specification visible — confirms text extraction is complete |

All five artifacts are representations of the same single document. No data dictionary, schema, sample data, or supplementary documentation exists. The entire (b)(10) documentation is 808 bytes of plain text.

## 3. Export Mechanics

- **Format**: C-CDA XML (one per patient) + PDF/HTML files for encounter notes and patient documents
- **Mechanism**: Not documented. The documentation describes output structure but provides no instructions for initiating an export (no screenshots, no UI guidance, no API endpoint).
- **Single-patient**: Produces a folder `Lastname_FirstName_patientId_Date` containing C-CDA file and two subfolders
- **Bulk/all-patient**: Produces a ZIP file `Patient_export_{date}.zip` containing one patient folder each
- **Access constraints/fees**: Not mentioned. Mandatory disclosures state "no additional costs for the certified functionality"

## 4. Export Content: What's In It

### Documentation completeness

The documentation provides **zero field-level detail**. The entire specification is:

1. A C-CDA XML file "Conformant to USCDI v1" — references the standard USCDI v1 errata document for specifications
2. An "Encounters" subfolder with visit notes as PDF or HTML (0 to many per patient)
3. A "Patient Documents" subfolder with other documents as PDF or HTML (0 to many per patient)

There is no data dictionary, no entity/table definitions, no field names, no data types, no value sets, no relationships, no sample data, and no machine-readable schema.

### Vendor's own content organization

| Entity/Component | Fields Documented | Described | Types | Category |
|---|---|---|---|---|
| C-CDA XML File | 0 | 0 | No | Clinical Summary |
| Encounter Notes (PDF/HTML) | 0 | 0 | No | Visit Documentation |
| Patient Documents (PDF/HTML) | 0 | 0 | No | Other Documents |

**Totals**: 3 export components, 0 documented fields, 0 descriptions, 0 type definitions.

The vendor provides only file naming conventions (`Lastname_FirstName_ccda.xml`, `{encounterId}_{date}.pdf`, `{documentId}_{date}.pdf`) and references the generic USCDI v1 C-CDA standard for content specifications.

### What the C-CDA likely contains (inferred, not documented)

Based on the USCDI v1 claim, the C-CDA would typically include sections for: demographics, problems, medications, allergies, immunizations, vital signs, lab results, procedures, care team, goals, health concerns, assessment/plan, and some clinical notes. However, the vendor does not specify which C-CDA sections are actually populated or what data elements are included within each section.

### What the encounter notes and documents contain

Completely unspecified. The documentation says "All Visit Notes" and "Other Documents" but does not describe what types of notes, what content, or how clinical information is represented in these unstructured files. Rendering clinical data as PDF/HTML means any structured data (coded diagnoses, measurements, therapy assessments) becomes non-computable.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor describes three export components — all in the vendor's own terms:

1. **C-CDA XML**: A single structured file per patient, claimed to conform to USCDI v1. This is the only structured data component. USCDI v1 covers core clinical data classes (demographics, problems, medications, allergies, immunizations, vitals, labs, procedures) but excludes billing, scheduling, portal data, and specialty-specific content. The vendor provides no evidence that their C-CDA goes beyond the standard USCDI v1 template.

2. **Encounters**: Visit notes as flat PDF/HTML files. These may capture clinical narrative beyond the C-CDA summary, but as unstructured documents, their content is opaque and non-computable. No details on what types of encounters are included.

3. **Patient Documents**: Other documents as PDF/HTML. No indication of what document types are included. Could include scanned forms, consent documents, or other attachments — but this is entirely speculative.

The documentation is so thin that substantive bottom-up analysis is impossible. There are no entity lists, no field counts, no category breakdowns beyond these three components.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | Assumed via C-CDA (USCDI v1 claim); no field-level confirmation | Product stores demographics; C-CDA covers basics but depth unknown |
| Encounters / visits | ⚠️ Partial | Encounter notes as PDF/HTML; C-CDA may have encounter data | Visit notes exported as documents, but structured encounter data (dates, types, providers) only via C-CDA — detail unknown |
| Problems / conditions | ⚠️ Partial | Assumed via C-CDA | Likely present in C-CDA but depth of problem list data unknown |
| Medications / prescriptions | ⚠️ Partial | Assumed via C-CDA | C-CDA covers medication lists; e-prescribing transaction history (MDToolBox), formulary data, prescription benefits likely missing |
| Allergies | ⚠️ Partial | Assumed via C-CDA | Likely present but detail unknown |
| Immunizations | ⚠️ Partial | Assumed via C-CDA | Likely present but detail unknown |
| Vitals | ⚠️ Partial | Assumed via C-CDA | Likely present but detail unknown |
| Lab results | ⚠️ Partial | Assumed via C-CDA | Results likely in C-CDA; ordering workflow, task assignments, trending data likely not |
| Imaging / diagnostic reports | ⚠️ Partial | May appear in C-CDA or as patient documents | No specific evidence |
| Procedures | ⚠️ Partial | Assumed via C-CDA | Likely present but detail unknown |
| Clinical notes / documents | ⚠️ Partial | Encounter notes subfolder (PDF/HTML) | Notes exported as unstructured documents — clinical narrative preserved but structured data lost |
| Care plans / goals | ⚠️ Partial | Assumed via C-CDA (USCDI v1 includes goals) | Depth unknown |
| Orders / referrals | ⚠️ Partial | Medication orders may be in C-CDA; lab orders unclear | Product supports CPOE and lab orders; export coverage uncertain |
| Insurance / coverage | ❌ Not covered | No evidence in any artifact | Product stores insurance/eligibility data; significant gap |
| Claims / billing | ❌ Not covered | No evidence in any artifact | Product has full billing/claims/RCM; **major gap** |
| Payments | ❌ Not covered | No evidence in any artifact | Product processes payments (including patient portal bill pay); gap |
| Consents / directives | ❌ Not covered | No specific evidence; may appear in patient documents | Unknown if consent forms are in document subfolder |
| Patient communications / portal messages | ❌ Not covered | No evidence in any artifact | Product has patient portal with messaging; gap |
| Specialty-specific (pediatric therapy) | ❌ Not covered | No evidence of structured therapy data | Product has therapy-specific templates, dashboards, and assessments; **significant gap** — therapy progress data may appear in encounter PDFs but as unstructured content |

**Summary**: Every "covered" domain is marked ⚠️ Partial because coverage is inferred from the generic USCDI v1 C-CDA conformance claim — no vendor-specific evidence confirms actual content or depth. All non-USCDI domains (billing, insurance, payments, portal messages, therapy-specific data) are absent from the export with no evidence of coverage.

## 6. Documentation Quality

The documentation quality is **among the worst possible** for a certified (b)(10) export:

- **Total documentation**: 808 bytes of plain text (22 lines), equivalent to roughly one paragraph
- **Data dictionary**: None
- **Field definitions**: None
- **Value sets / code systems**: None
- **Sample data**: None
- **Machine-readable schema**: None
- **Export instructions**: None — no UI screenshots, no step-by-step guide, no API documentation
- **Content specification**: The only content detail is "CCDA File Conformant to USCDI v1" with a link to the standard USCDI v1 errata document. This tells a developer what the *standard* supports, not what Simplify EMR *actually exports*.
- **Error handling / edge cases**: None

A developer attempting to consume this export would have no vendor-specific guidance. They would need to treat the C-CDA as a generic USCDI v1 document and the PDF/HTML files as opaque blobs. There is no way to programmatically map Simplify EMR's data model from this documentation. The documentation describes a container format (folder structure and file names) but says nothing about the data content.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Minimal/stub/unclear**

The export is a thin wrapper around standard C-CDA (USCDI v1) plus unstructured document dumps. Even assuming the C-CDA is fully populated with all USCDI v1 data classes, this covers only the clinical summary floor — roughly the same data available through the vendor's existing (g)(6) or (g)(10) clinical exchange capabilities. The product's integrated practice management (billing, claims, payments, eligibility, authorization, RCM), patient portal (messaging, appointment requests, prescription renewals, bill pay), e-prescribing transaction history, and therapy-specific structured assessments are all absent from the documented export. The documentation is too thin to even confirm what the C-CDA actually contains, let alone assess completeness.

**Axis 2 — Export approach: Repackaged existing export**

This is clearly a C-CDA clinical summary export relabeled as (b)(10). The telltale signs are unambiguous:
- The export format is standard C-CDA conformant to USCDI v1 — the same standard used for transitions of care (b)(1)/(b)(2) and clinical information exchange
- The only external reference is to the generic USCDI v1 specification, not any product-specific data dictionary
- No product-specific mapping, no custom data elements, no vendor extensions
- No coverage of data domains beyond what C-CDA supports (no billing, no portal data, no specialty data)
- The encounter notes and patient documents as PDF/HTML are essentially a document dump appended to the clinical summary — this is not a purpose-built data export

The vendor added encounter note and document subfolders to their existing C-CDA export and called it (b)(10). This is a minimal compliance gesture, not a genuine effort to export all electronic health information.

### Key Findings

1. **Entire (b)(10) documentation is 808 bytes** — the shortest and most minimal export documentation reviewed. A single Google Doc describing only folder structure and file naming with zero content specification (`downloads/ehi-export-doc.txt`).

2. **Export is a standard C-CDA + document dump** — one USCDI v1 C-CDA XML per patient plus encounter notes and patient documents as PDF/HTML files. No structured data beyond what standard C-CDA provides. No vendor-specific data dictionary or schema exists.

3. **All billing/PM data is missing** — despite the product having integrated practice management with full billing, claims, eligibility, authorization, and revenue cycle management, none of this data appears in the export. This is the largest gap relative to what the product stores.

4. **Patient portal and specialty therapy data absent** — portal messaging, appointment requests, prescription renewals, bill pay records, and therapy-specific structured assessments (pediatric OT/PT/speech/ABA) are all unaccounted for in the export.

5. **Zero field-level documentation** — no data dictionary, no field names, no types, no descriptions, no sample data. A developer cannot determine what data the export contains from the documentation alone.

### Summary Stats

```
Coverage:        Minimal/stub/unclear
Approach:        Repackaged existing export
Export format:   C-CDA XML + PDF/HTML documents
Entities:        3 components (1 C-CDA file, 2 document folders)
Fields:          0 documented
Descriptions:    N/A (no fields documented)
Sample data:     No
Bulk export:     Yes (all-patient ZIP mode documented)
Domains covered: 0 of 19 confirmed; ~12 of 19 assumed via C-CDA (unverified)
```

### Bottom Line

Simplify EMR's (b)(10) export is a standard C-CDA clinical summary with encounter notes dumped as PDF/HTML files — the same data available through existing clinical exchange mechanisms, repackaged with folder structure. A patient would receive a clinical summary and their visit notes but would **not** receive their billing records, claims history, patient portal messages, insurance details, or therapy-specific assessment data. The documentation is 808 bytes with zero field-level detail, making it among the most minimal (b)(10) implementations possible.
