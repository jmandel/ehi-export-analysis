# EHI Export Analysis: WRS Health

**Product**: WRS Health Web EHR and Practice Management System v7.0
**Analysis date**: 2026-02-15
**CHPL ID**: 15.02.05.2527.WRSH.01.01.1.211214

## 1. Product Context

WRS Health is a cloud-based, physician-founded EHR and practice management platform serving ambulatory practices across 32+ medical specialties. The platform is an all-in-one system combining:

- **Clinical charting**: Specialty-specific templates (six-tier content system) for HPI, physical exam, ROS, assessment/plan across specialties including internal medicine, cardiology, dermatology, OB/GYN, orthopedics, psychiatry, pain management, and more
- **E-prescribing**: Surescripts Gold-certified with EPCS, drug interaction checking, PBM/formulary integration, medication history
- **Lab integration**: Bidirectional connectivity with LabCorp, Quest; order tracking system with alerts and patient communication logging
- **Billing/RCM**: Integrated claim scrubbing, electronic superbills with specialty ICD/CPT codes, charge capture, denial management, online payments
- **Patient portal**: Secure messaging, lab results viewing, appointment scheduling, prescription refills, demographics self-entry, bill payment
- **Telehealth**: Integrated video visits with virtual waiting room, charting during visits
- **Document management**: eFax, scanning/import, image upload
- **Scheduling**: Multi-provider/location, automated reminders (phone/email/SMS), insurance eligibility verification
- **Referral management**: Tracking and provider communications
- **Reporting**: MIPS/quality measures (39 CQMs), practice analytics

This baseline establishes what the EHI export *should* cover: a rich set of clinical, billing, scheduling, communication, and specialty-specific data.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `170.315-b10-EHI-Export.pdf` (1.1 MB, 8 pages) | The sole EHI export documentation. Describes export workflow with screenshots (pages 3–4), and file structure of the exported ZIP (pages 5–7). Created with Google Docs, version 1.0, dated October 14, 2023. | **Primary source** — only substantive documentation |
| `screenshot-certification-page-full.png` (1.4 MB) | Full-page screenshot of the ONC certification page at wrshealth.com/onc-certification-and-costs | Confirms single PDF link for EHI export |
| `screenshot-ehi-section-viewport.png` (686 KB) | Viewport screenshot of the "Electronic Health Information Export" section | Confirms only one link: the PDF above |

**Verification**: The webpage at `https://www.wrshealth.com/onc-certification-and-costs` was independently accessed on 2026-02-15. It returns HTTP 200 and contains exactly one EHI export link pointing to the same PDF (`170.315-b10-EHI-Export.pdf`). No additional data dictionary, schema, sample data, or API documentation exists. The prior report's description of artifacts is accurate.

## 3. Export Mechanics

- **Format**: ZIP file (`ehi_documents.zip`) containing CSV files, a C-CDA XML, HTML encounter notes, and raw document attachments
- **Single-patient export**: Self-service via EHR Admin UI. Users with Clinical Admin/Admin permissions search for a patient, right-click, select "EHI Export," click "Request Electronic Health Information," wait for processing, then download the ZIP. The PDF includes screenshots of this workflow (pages 3–4).
- **Multi-patient/bulk export**: Available but **not self-service**. Requires emailing `accountmanagement@wrshealth.com`. Same ZIP format as single-patient.
- **Access constraints**: Requires Clinical Admin or Admin permissions in EHR Admin
- **Fees**: Not mentioned in the export documentation. The certification page states the system is charged as a monthly per-provider subscription with no cost differential for ONC-certified features.

## 4. Export Content: What's In It

The export contains 9 components packaged in a ZIP file. There is **no field-level data dictionary** for any file — the PDF describes each file/folder at a high level (1–2 sentences each) but provides no column names, data types, value sets, or schema definitions.

### Export file structure (from PDF pages 5–7)

| Component | Format | Description (from PDF) |
|---|---|---|
| `Documents/` | Various (PDF, DOCX, XLS, XML, HTML, DAT, JPG, GIF, PNG) | Patient's supporting documents, attachments, lab results uploaded by practice. Filename references patient name and ID. |
| `Notes/` | HTML + CSS/JS/images | Encounter notes from patient visits. One HTML file per encounter note. Includes CSS, images, and JavaScript for readable rendering. Filename references patient name, ID, date, and note type. |
| `Notes/PatientNoteFiles.csv` | CSV | Mapping file listing all exported notes |
| `Notes/NOTES.LOG` | Text | Log of successfully exported notes and any errors |
| `BillingReport.csv` | CSV | Financial transactions: patient information, transaction dates, charges, claims, descriptions of transactions, and status |
| `CCDA.xml` | XML (C-CDA) | Clinical data export compliant with HL7 C-CDA and USCDI v1 |
| `demographics.csv` | CSV | Patient key information, identification details, contact information, insurance information |
| `PatientDocumentFiles.csv` | CSV | Mapping file listing all documents in the Documents/ folder |
| `schedule.csv` | CSV | Encounter records: appointment date, provider, location, appointment type, workflow, notes, and date on which notes are recorded |

### Data dictionary assessment

- **Entities/tables**: 9 components (3 data CSVs, 1 C-CDA XML, 2 index/mapping CSVs, 1 log file, 2 folders of files)
- **Total fields**: **Unknown** — no column definitions are provided for any CSV file
- **Fields with descriptions**: **0** — no field-level documentation exists
- **Types documented**: **No**
- **Relationships/foreign keys**: **Minimal** — PatientDocumentFiles.csv and PatientNoteFiles.csv serve as indexes for the Documents/ and Notes/ folders, but no column definitions explain these relationships
- **Value sets/code systems**: **None documented** — the C-CDA references USCDI v1 compliance but no custom value sets
- **Sample data**: **None provided**
- **Machine-readable schemas**: **None**

### Vendor's own content organization

The PDF does not organize content into clinical domains or categories. It presents a flat file listing. The vendor's structure is simply the ZIP file contents described above.

| Component | Fields | Described | Types | Category |
|---|---|---|---|---|
| demographics.csv | Unknown | 0 | No | Demographics / Insurance |
| BillingReport.csv | Unknown | 0 | No | Billing / Financial |
| schedule.csv | Unknown | 0 | No | Encounters / Scheduling |
| CCDA.xml | USCDI v1 standard | By reference to HL7 spec | By reference | Clinical (standard) |
| Notes/ (HTML) | N/A (narrative) | N/A | N/A | Clinical Notes |
| Documents/ | N/A (files) | N/A | N/A | Documents / Attachments |
| PatientNoteFiles.csv | Unknown | 0 | No | Index / Mapping |
| PatientDocumentFiles.csv | Unknown | 0 | No | Index / Mapping |
| NOTES.LOG | N/A | N/A | N/A | Operational Log |

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The export takes a **hybrid approach** with three layers:

1. **C-CDA XML** for standard clinical data (USCDI v1): This covers the standard clinical summary data classes — problems, medications, allergies, immunizations, vitals, lab results, procedures, and patient demographics. The PDF provides no detail beyond stating USCDI v1 compliance and referring users to the HL7 website for specifications.

2. **CSV files** for billing, demographics, and scheduling: Three data CSVs add billing transactions, patient demographics/insurance, and encounter schedules beyond what C-CDA covers. However, without column definitions, the actual depth and breadth of these files is unknowable from the documentation alone.

3. **HTML files and raw documents** for notes and attachments: Encounter notes are exported as rendered HTML (human-readable but not machine-parseable). Uploaded documents are exported in their original formats.

The strongest coverage evidence is for **billing** (dedicated CSV with transactions, charges, claims) and **demographics** (dedicated CSV). The clinical domain relies entirely on the C-CDA standard, meaning only USCDI v1 data classes are guaranteed to be represented in structured form.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | `demographics.csv` (fields unknown — no column list) | Likely adequate but impossible to verify depth without column definitions |
| Encounters / visits | ✅ Covered | `schedule.csv` (appointment date, provider, location, type, workflow, notes, note dates) | Described at high level; no field list |
| Problems / conditions | ⚠️ Partial | Only via `CCDA.xml` (USCDI v1) | Product stores specialty-specific diagnoses; C-CDA covers standard problem list only |
| Medications / prescriptions | ⚠️ Partial | Only via `CCDA.xml` (USCDI v1) | Product has rich e-prescribing (EPCS, PBM, formulary, Surescripts history); no dedicated medication export beyond C-CDA |
| Allergies | ⚠️ Partial | Only via `CCDA.xml` (USCDI v1) | Standard USCDI coverage; adequate if C-CDA is complete |
| Immunizations | ⚠️ Partial | Only via `CCDA.xml` (USCDI v1) | Standard USCDI coverage |
| Vitals | ⚠️ Partial | Only via `CCDA.xml` (USCDI v1) | Standard USCDI coverage |
| Lab results | ⚠️ Partial | `CCDA.xml` + uploaded files in `Documents/` | Structured results via C-CDA; uploaded results as documents. Product's order tracking system (order status, alerts, patient communications) not exported in structured form. |
| Imaging / diagnostic reports | ⚠️ Partial | May appear in `Documents/` folder | Only as uploaded files, not structured data |
| Procedures | ⚠️ Partial | Only via `CCDA.xml` (USCDI v1) | Standard USCDI coverage |
| Clinical notes / documents | ✅ Covered | `Notes/` folder (HTML per encounter) + `Documents/` folder | Notes exported as HTML narrative; human-readable but not computable. Documents in original format. This is reasonable coverage. |
| Care plans / goals | ❌ Not covered | Not mentioned in export documentation | Product has health maintenance and recall features; these appear absent from export |
| Orders / referrals | ❌ Not covered | Not mentioned in export documentation | Product has referral management and lab order tracking; not in export |
| Insurance / coverage | ⚠️ Partial | `demographics.csv` mentions "insurance information" | Some coverage likely via demographics CSV; depth unknown |
| Claims / billing | ✅ Covered | `BillingReport.csv` (transactions, charges, claims, status) | Dedicated file; likely the strongest non-clinical coverage. Field-level depth unknown. |
| Payments | ⚠️ Partial | May be in `BillingReport.csv` | Transaction records mentioned but unclear if patient payments vs. insurance payments are included |
| Consents / directives | ❌ Not covered | Not mentioned | May not be a core feature of this product; unclear gap |
| Patient communications | ❌ Not covered | Not mentioned | Product has secure portal messaging, eFax, and order-tracking communications; none exported |
| Specialty-specific data | ⚠️ Partial | `Notes/` folder (HTML) | Product has 32+ specialty template systems with structured data fields. These are exported only as rendered HTML narrative — the structured specialty-specific data elements are lost. This is a significant gap. |

**Summary**: Of 18 applicable domains, 4 are covered (✅), 10 are partially covered (⚠️), and 4 are not covered (❌). The partial coverage is largely due to reliance on the C-CDA standard, which provides breadth across clinical domains but only at the USCDI v1 depth.

## 6. Documentation Quality

The documentation is an **8-page PDF** that functions as a user guide rather than a technical specification:

- **Pages 1–2**: Title page, revision history, introduction, intended users
- **Pages 3–4**: Step-by-step single-patient export workflow with screenshots (6 screenshots showing the UI flow)
- **Page 5**: Multi-patient export (one paragraph; requires email to vendor)
- **Pages 5–7**: File structure description table (file-level descriptions only)

**What's present**:
- Clear procedural steps for performing a single-patient export
- File-level description of each component in the ZIP
- Screenshots of the export UI workflow

**What's missing**:
- No column/field names for any CSV file
- No data types, formats, or constraints
- No value sets, code systems, or enumerated values
- No sample data files or example exports
- No machine-readable schema (XSD, JSON Schema, DDL, OpenAPI)
- No description of C-CDA profile beyond "USCDI v1 compliant"
- No documentation of relationships between files
- No versioning beyond v1.0 (October 2023)

**Developer usability**: A developer receiving this documentation could not build an import tool. They would need to examine actual export files to discover column names, data types, and relationships. The C-CDA component is understandable by reference to the HL7 standard, but the vendor-specific CSV files are entirely undocumented at the field level.

## 7. Overall Assessment

### Classification

**Partial native export**

The export is a genuine (b)(10) effort — it goes beyond C-CDA/FHIR repackaging by including billing data, encounter notes, and documents in vendor-specific formats. However, it has significant coverage gaps (no portal messages, referrals, care plans, or structured specialty data) and critically thin documentation (no field-level data dictionary for any CSV file). The clinical data component relies on C-CDA/USCDI v1, which covers only a standard subset of what the product stores.

### Key Findings

1. **Hybrid export with genuine billing coverage**: The export combines C-CDA (clinical summary), CSV files (billing, demographics, scheduling), HTML (notes), and raw documents. The inclusion of `BillingReport.csv` with financial transactions, charges, and claims is a meaningful addition beyond standard clinical summaries. This is not a C-CDA/FHIR repackaging — it's a real (b)(10) effort.

2. **Zero field-level documentation**: None of the 3 data CSV files (`demographics.csv`, `BillingReport.csv`, `schedule.csv`) have documented column names, data types, or value sets. The entire data dictionary is effectively absent. A developer cannot determine what fields are exported without examining actual export files. (Source: `170.315-b10-EHI-Export.pdf`, pages 5–7)

3. **Clinical data limited to C-CDA/USCDI v1**: All structured clinical data (problems, medications, allergies, immunizations, vitals, labs, procedures) is delivered only through the C-CDA XML, constrained to USCDI v1 data classes. The product's rich specialty-specific templates (32+ specialties with structured data elements), detailed e-prescribing records (EPCS, formulary, medication history), and lab order tracking are not exported in structured form.

4. **Specialty clinical data reduced to HTML narrative**: The product's six-tier specialty template system stores structured clinical data, but the export renders encounter notes as HTML files. This preserves the human-readable narrative but loses all structured, computable specialty-specific data elements.

5. **Bulk export requires vendor involvement**: Population-level export is not self-service — it requires an email to `accountmanagement@wrshealth.com`. Only single-patient export is available through the UI.

### Summary Stats

```
Classification:  Partial native export
Export format:   Mixed (CSV, C-CDA XML, HTML, raw documents) in ZIP
Model type:      Hybrid — vendor CSV files + standard C-CDA projection + document dump
Entities:        9 components (3 data CSVs + 1 C-CDA + 2 index CSVs + 1 log + 2 file folders)
Fields:          N/A (no field-level documentation)
Descriptions:    N/A (0% — no fields documented)
Sample data:     No
Bulk export:     Yes, but vendor-assisted (email required)
Domains covered: 4 of 18 fully, 10 partially (via C-CDA or undocumented CSVs)
```

### Bottom Line

WRS Health has built a legitimate (b)(10) export that goes beyond clinical summary repackaging — it includes billing data, encounter notes, and documents alongside the C-CDA. However, the complete absence of any field-level data dictionary makes the export a black box: without examining actual export files, it is impossible to determine what data is actually exported in the CSV files. The single biggest gap is the lack of structured specialty clinical data — a product built around 32+ specialty templates with structured data fields exports those only as rendered HTML narrative, losing all structured clinical information beyond the standard USCDI v1 C-CDA subset.
