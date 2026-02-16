# EHI Export Analysis: Health Systems Technology, Inc.

**Product**: MedPointe v13
**Analysis date**: 2026-02-16
**CHPL IDs**: 15.04.04.1597.MedP.13.01.1.230216 (CHPL ID 11238)

## 1. Product Context

MedPointe is a cloud-based, all-in-one ambulatory EHR and practice management suite developed by Health Systems Technology, Inc. (HST), a small vendor based in Rochester, NY. The product targets small to mid-sized ambulatory practices in family medicine, internal medicine, pediatrics, urgent care, and sleep medicine. HST appears to be a very small company — the CHPL contact (Tim Schmidt) appears to be the primary developer/owner.

MedPointe is a full-featured integrated system combining:

- **Clinical/EHR**: Full charting, problem lists, medication lists, allergy management with drug interaction checking, e-prescribing, order sets, lab integration (bidirectional), imaging ordering, referral management, clinical notes with "Intelligent Text Generation," preventive care tracking, document management, care plans
- **Practice Management**: Scheduling with automated reminders, demographics, insurance eligibility verification, custom workflows, reporting, accounting
- **Billing/RCM**: Integrated medical billing, revenue cycle management, clearinghouse integration, claims submission/tracking, ERA/EOB auto-posting, payment collection/posting, denial management
- **Patient Engagement**: Patient portal (scheduling, messaging, records access), online intake forms, appointment reminders, lab result notifications
- **Public Health**: Immunization registry reporting, cancer case reporting

With 37 certified ONC criteria (including (b)(10) EHI export), this is a comprehensive ambulatory EHR storing clinical records, billing/financial data, administrative data, patient communications, scanned documents, and more. A complete EHI export should cover all of these domains.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/Providers - Exporting Computer Readable Documents.pdf` | 2-page PDF (474,907 bytes). Author: Tim Schmidt, created 2023-11-16. Describes how to export clinical documents using the proprietary "C62" file format via the MedPointe UI. Contains two screenshots: a right-click context menu and an "Export Chart" dialog. | **Primary artifact** — the only export documentation that exists. Extremely thin: UI instructions only, no data dictionary, no schema, no format spec. |
| `downloads/help-documents-page.png` | Full-page screenshot (563,801 bytes) of the registered EHI documentation URL (hstspot.com/help-documents.php). Shows three categories: Exporting Documents (1 PDF), Tutorials (12 MP4 videos), e-Prescribing (7 PDFs). | **Contextual** — confirms only one export-related document exists on the help site. |

**Total documentation**: 1 PDF, 2 pages. No data dictionary, no schema, no sample data, no additional technical documentation.

## 3. Export Mechanics

- **Format**: Proprietary "C62" file format. No public documentation, specification, or schema exists for this format. Web searches for "C62 file format" in healthcare contexts return no results. It is unknown whether C62 files are human-readable text, binary, structured data, or rendered documents.
- **Mechanism**: UI-driven export from within the MedPointe clinical window:
  - **Single document**: Right-click a document in the patient's TOC → "Export via C62"
  - **Chart export**: Right-click from Overview Page → "Export Chart" → select date range, document types, output option (C62)
  - **Batch export**: Main Menu → Tools → Clinical → Export → select patient criteria (name range, DOB, classification, provider), document types, date range
- **Single-patient vs bulk**: Both supported. Single-patient chart export and multi-patient batch export are available.
- **Access constraints**: The documentation describes an end-user workflow within the MedPointe application. No API access is documented. A recipient of a C62 file would presumably need MedPointe (or vendor assistance) to interpret the data.

**Notable**: The right-click menu screenshot (PDF page 1) reveals additional export functions beyond C62: "Export Continuity of Care," "Export Continuity of Care - Referral," "Export Continuity of Care - Batch," "Export Immunization Data," "Export Syndromic Data," and "Export Medical Records." These appear to be separate from the C62 export and are not documented in the (b)(10) materials.

## 4. Export Content: What's In It

### What the documentation tells us

The documentation provides **zero field-level detail**. There is no data dictionary, no schema, no format specification, and no sample data. The only indication of content comes from the Export Chart dialog's checkboxes:

- Cover Sheet
- Notes
- Text Documents
- Scanned/Faxed Documents
- Include Restricted Documents

These are document categories, not data entities or tables. The documentation describes exporting *documents* from a patient's chart — not structured data fields. There is no mention of what data fields, tables, or structures exist within the C62 format.

### Vendor's own content organization

Since there is no data dictionary, the only "content organization" visible is the document type checkboxes in the export dialog:

| Entity/Table | Fields | Described | Types | Category (vendor's) |
|---|---|---|---|---|
| Cover Sheet | 0 | 0 | N/A | Document type |
| Notes | 0 | 0 | N/A | Document type |
| Text Documents | 0 | 0 | N/A | Document type |
| Scanned/Faxed Documents | 0 | 0 | N/A | Document type |
| Restricted Documents | 0 | 0 | N/A | Document type modifier |

**Total documented entities**: 5 document categories
**Total documented fields**: 0
**Fields with descriptions**: 0
**Fields with types**: 0

This is not a data dictionary — these are UI checkbox labels. No field-level, table-level, or schema-level documentation exists.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor's documentation describes a **document-level export** — it exports clinical documents (notes, cover sheets, text documents, scanned/faxed documents) from a patient's chart as files in a proprietary C62 format. The documentation does not describe exporting any structured data (discrete vital signs, coded diagnoses, medication records, lab values, allergy lists, etc.), nor does it mention any non-clinical data (billing, claims, insurance, scheduling, portal messages).

The export dialog suggests the system treats the patient chart as a collection of documents, and the C62 export packages selected document types for output. This is conceptually closer to "export a folder of documents" than "export the patient's electronic health information."

The right-click menu also reveals separate export functions (Continuity of Care/C-CDA, Immunization Data, Syndromic Data, Medical Records) that are not part of the C62 export and are not documented as part of the (b)(10) process.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ❌ Not covered | No mention in export documentation | Product stores demographics; significant gap |
| Encounters / visits | ❌ Not covered | No encounter-level export documented | Product stores encounters; significant gap |
| Problems / conditions / diagnoses | ❌ Not covered | No structured problem list export | Product stores problem lists (certified (a)(1)); significant gap |
| Medications / prescriptions | ❌ Not covered | No medication data export | Product has e-prescribing and med lists (certified (a)(1)); significant gap |
| Allergies | ❌ Not covered | No allergy data export | Product stores allergies with drug interaction checking; significant gap |
| Immunizations | ❌ Not covered | Not part of C62 export (separate "Export Immunization Data" function exists but is not documented as (b)(10)) | Product stores immunization records (certified (f)(1)); significant gap |
| Vitals | ❌ Not covered | No vitals export documented | Product stores vitals; significant gap |
| Lab results | ❌ Not covered | No lab results export | Product has bidirectional lab integration; significant gap |
| Imaging / diagnostic reports | ❌ Not covered | No imaging data export | Product has imaging ordering and picture archiving; significant gap |
| Procedures | ❌ Not covered | No procedure data export | Product stores procedures; significant gap |
| Clinical notes / documents | ⚠️ Partial | C62 export includes "Notes," "Text Documents," "Cover Sheet," "Scanned/Faxed Documents" — but format is undocumented, so actual content/fidelity is unknown | Documents appear to be included, but without format documentation it's impossible to verify completeness or usability |
| Care plans / goals | ❌ Not covered | No care plan export | Product stores care plans (certified (a)(12)); gap |
| Orders / referrals | ❌ Not covered | No order or referral export | Product has referral management and order sets; significant gap |
| Insurance / coverage | ❌ Not covered | No insurance data export | Product stores insurance/eligibility data; significant gap |
| Claims / billing | ❌ Not covered | No billing data export | Product has full RCM/billing with clearinghouse integration; significant gap |
| Payments | ❌ Not covered | No payment data export | Product stores payment records; significant gap |
| Consents / directives | ❌ Not covered | No consent data export | Unknown if product stores structured consents; possibly N/A |
| Patient communications / portal messages | ❌ Not covered | No portal/messaging export | Product has patient portal with messaging; gap |
| Specialty-specific | N/A | — | No specialty-specific data documented beyond general ambulatory |

**Summary**: 0 of 14 applicable domains are fully covered. 1 domain (clinical notes/documents) is partially covered. 13 domains with known product capability are not covered by the documented export.

## 6. Documentation Quality

The documentation is among the most minimal possible for a (b)(10)-certified product:

- **Completeness**: A 2-page PDF with step-by-step UI instructions and two screenshots. No technical content whatsoever.
- **Data dictionary**: None. Not even a list of field names.
- **Schema/format spec**: None. The C62 format is named but never defined.
- **Sample data**: None.
- **Machine-readable artifacts**: None.
- **Developer usability**: A developer could not build an import from this documentation. A recipient of a C62 file would have no way to interpret it without MedPointe software or vendor assistance.
- **Patient usability**: A patient receiving this export could not meaningfully access their data without proprietary tools.

The documentation reads as a compliance checkbox: it documents *how to click the export button* but not *what comes out*. The title of the source Word document ("Exporting Documents via C62") confirms this was written as a how-to guide, not as technical export documentation.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Minimal/stub/unclear**

The documentation describes exporting only clinical documents (notes, text documents, scanned/faxed documents) in a proprietary format. MedPointe is a full-featured ambulatory EHR with integrated billing/RCM, practice management, patient portal, e-prescribing, lab integration, and more — the documented export covers at most one narrow slice (clinical documents) of the product's extensive data footprint. Even within that slice, there is zero documentation of what data fields, structures, or content the C62 format actually contains. There is no evidence of structured clinical data (medications, labs, vitals, allergies, problems) being exported, let alone billing, insurance, or administrative data. The documentation is too thin to definitively assess even the document export's completeness.

**Axis 2 — Export approach: Unclear/undetermined**

The C62 format appears to be a pre-existing proprietary document export mechanism that was pointed to for (b)(10) compliance. The PDF was created November 2023, nine months after the February 2023 certification date, suggesting the documentation was created after the fact. The right-click menu screenshot reveals that C62 export sits alongside other export functions (C-CDA, immunization data, syndromic data, medical records), suggesting it is one of several existing export mechanisms rather than a purpose-built EHI export. However, the complete lack of format documentation makes it impossible to determine whether C62 actually contains comprehensive structured data or is truly just a document container. The most charitable interpretation is that C62 might encode some structured data, but the documentation provides zero evidence for this.

### Key Findings

1. **The entire (b)(10) documentation is a 2-page PDF with zero technical content.** No data dictionary, no schema, no format specification, no sample data. The document is a UI guide ("how to right-click and select Export") with no description of what the export contains. (Source: `downloads/Providers - Exporting Computer Readable Documents.pdf`)

2. **The export uses a proprietary, undocumented format ("C62").** No public specification exists. A recipient of a C62 file cannot interpret it without MedPointe software. This is the opposite of the interoperability that (b)(10) is meant to enable. (Source: PDF title, export dialog screenshots)

3. **The export appears limited to clinical documents only.** The Export Chart dialog offers only document-type checkboxes (Cover Sheet, Notes, Text Documents, Scanned/Faxed Documents). There is no indication that structured clinical data (medications, labs, vitals, problems, allergies), billing data, insurance data, or administrative data is included. (Source: Export Chart dialog screenshot, PDF page 2)

4. **MedPointe stores far more data than the export covers.** The product is a full ambulatory EHR with integrated billing/RCM, e-prescribing, lab integration, patient portal, scheduling, and more — at least 14 data domains. The documented export addresses at most 1 domain (clinical documents), and even that is only partially documented. (Source: `product-research.md`, certified criteria list)

5. **The right-click menu reveals separate, undocumented export functions** (Export Continuity of Care, Export Immunization Data, Export Syndromic Data, Export Medical Records) that are not part of the (b)(10) documentation. These suggest the vendor has other export capabilities that were not included in the EHI export. (Source: right-click menu screenshot, PDF page 1)

### Summary Stats

    Coverage:        Minimal/stub/unclear
    Approach:        Unclear/undetermined
    Export format:   C62 (proprietary, undocumented)
    Entities:        5 document categories (no structured entities)
    Fields:          0 (no field-level documentation)
    Descriptions:    N/A (no fields documented)
    Sample data:     No
    Bulk export:     Yes (batch export for multiple patients)
    Domains covered: 1 of 14 applicable domains (partial)

### Bottom Line

A patient or provider would receive clinical documents in a proprietary, undocumented format that cannot be interpreted without MedPointe software — and even then, the export would not include their medications, lab results, vitals, allergies, diagnoses, billing records, insurance information, or any other structured data the system stores. This is one of the thinnest EHI export implementations possible: a pre-existing document export function relabeled for (b)(10) compliance, with documentation that describes how to click buttons but not what data comes out.
