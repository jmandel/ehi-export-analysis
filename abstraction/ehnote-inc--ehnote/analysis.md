# EHI Export Analysis: EHNOTE, INC

**Product**: EHNOTE v1.0  
**Analysis date**: 2026-02-16  
**CHPL IDs**: 15.04.04.3171.EHNO.01.00.1.231025 (CHPL ID 11356)

## 1. Product Context

EHNOTE is a cloud-based, all-in-one EHR and practice management platform built primarily for ophthalmology and eye care practices, serving 200+ specialty practices in the USA and India. Founded in 2018 and headquartered in Plano, Texas, the company also offers specialty modules for dental, gynecology, pediatrics, and general physician practices.

The platform spans a broad range of functional areas relevant to assessing export completeness:

- **Clinical EHR**: Subspecialty charting templates, examination findings, diagnoses (ICD-11), clinical notes, problem lists, medication lists, allergy lists, immunization records, care plans
- **Ophthalmology-specific data**: Visual acuity measurements, intraocular pressure (IOP) readings, refraction data, DICOM imaging, anatomical drawings, before/after surgical comparisons
- **ASC (Ambulatory Surgery Center) charting**: Pre-op, intra-op, post-op, anesthesia documentation, operative notes
- **E-prescribing**: Via DrFirst Rcopia integration
- **Practice management**: Scheduling, multi-location management, digital check-in/out, insurance eligibility verification
- **Revenue cycle management / Billing**: Claims processing, accounts receivable, financial transactions, reimbursement tracking, integrated payment gateway
- **Optical point-of-sale**: Retail management for eyeglasses/contacts, inventory tracking
- **Patient portal**: Health record access, secure messaging, telemedicine, self-vision testing, medicine reminders
- **Analytics/reporting**: MIPS dashboard, population analytics, clinical analytics, 200+ pre-built reports

This is a feature-rich platform storing clinical, financial, specialty, and administrative data across multiple domains. A genuine (b)(10) export should reflect this breadth.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/ehi-export-page.html` (31,265 bytes) | The entire EHI export documentation — a single static HTML page describing file naming conventions, export format (PDFs and images), and legal terms. **~1,268 words of content** (including boilerplate). | **Primary source** — this is the totality of the vendor's EHI export documentation |
| `downloads/ehi-export-page-screenshot.png` (835 KB) | Full-page screenshot of the EHI export documentation page | Confirms HTML content renders as expected; no hidden dynamic content |
| `downloads/ehi-export-page-top.png` (203 KB) | Viewport screenshot of the top portion of the page | Confirms page header and introduction |
| `files.json` | Manifest of collected artifacts | Confirms no additional downloadable files exist (no PDFs, ZIPs, CSVs, schemas) |
| `product-research.md` | Prior research on EHNOTE's capabilities and data domains | **Essential context** for assessing export completeness |
| `sources.json` | URLs visited during research (14 sources) | Confirms vendor website pages and third-party listings reviewed |
| `chpl-metadata.json` | CHPL certification details | Confirms (b)(10) certification, certification date 2023-10-25 |

**No downloadable artifacts exist.** The EHI export page contains zero links to PDFs, ZIPs, CSV templates, JSON schemas, sample data files, or any other downloadable documentation. The entire documentation is inline HTML text.

## 3. Export Mechanics

- **Format**: PDF files (case sheets) and image files (PNG/JPEG)
- **Mechanism**: UI-driven — user clicks an "export and download" button in the EHR
- **Scope**: Single-patient export, per-appointment granularity. Each appointment generates one PDF case sheet plus associated image files.
- **Bulk capability**: No evidence of bulk or multi-patient export capability
- **Access constraints**: No extra fees for the export function itself, though fees may apply "if the export size exceeds the contracted available size of your instance" for cloud-hosted clients
- **Output structure**: Files are linked by a shared `P####` patient identifier in filenames. Appointment-specific files also share the appointment date.

The export is essentially a "print to PDF" of visit records plus attached images — the least computable format possible for structured EHR data.

## 4. Export Content: What's In It

### No data dictionary

EHNOTE provides **no data dictionary, no schema, and no field-level documentation**. The documentation explicitly states: *"There is no 'one size fits all' set of fields in the software because of the extensive customization that is possible."*

The only description of export content is a single sentence listing broad categories of data found in the case sheet PDFs: *"Name of the clinic, patient demographics, Chief complaints, Review of systems, Assessments, Medications and other clinical data part of the appointment."*

### Vendor's own content organization

The documentation describes five categories of exported files:

| Entity/Category | Fields | Described | Types | Format | Category (vendor's) |
|---|---|---|---|---|---|
| Case Sheets (PDF) | 7 broad categories | Category-level only | N/A (rendered PDF) | PDF | Clinical |
| Investigations | 1 (image) | Minimal | Image | PNG/JPEG | Clinical |
| Surgery Consents | 1 (image) | Minimal | Image | PNG/JPEG | Clinical |
| Referrals | 1 (image) | Minimal | Image | PNG/JPEG | Clinical |
| Billings and Authorization | 1 (image) | Minimal | Image | PNG/JPEG | Billing |

**Total "entities": 5 file categories**  
**Total "fields": 11 broad content descriptors** (not actual database fields)  
**Fields with meaningful descriptions: 0** (descriptions are just the category name restated)

These are not database entities or structured data tables. They are categories of rendered output files. The 7 "fields" for case sheet PDFs (clinic name, demographics, chief complaints, review of systems, assessments, medications, other clinical data) are broad content labels — not individual data fields with types, constraints, or value sets.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor describes exactly two types of exported output:

1. **PDF Case Sheets**: One per appointment, containing a rendered view of the clinical encounter record. Content described at a high level: demographics, complaints, review of systems, assessments, medications, and "other clinical data." No field-level detail, no indication of what specific data elements are captured or omitted.

2. **Image Files**: PNG/JPEG images categorized as investigations, surgery consents, referrals, or billings/authorization files. These are raw image files with no structured metadata — essentially attached documents exported in their native format.

The documentation is so thin that it's impossible to determine what data is actually in the export. The case sheet PDFs could contain anything from a bare-bones visit summary to a detailed multi-page clinical record — there's no way to tell from the documentation alone. The "Billings and Authorization" image category is especially vague: it's unclear whether this includes actual billing records (charges, claims, payment data) or just scanned authorization documents.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | Mentioned in PDF case sheet content ("patient demographics") | No field-level detail; unknown what demographic fields are included |
| Encounters / visits | ⚠️ Partial | Each PDF represents one appointment — but as rendered output, not structured data | Encounter structure is implicit in PDF naming (appointment date), not as structured records |
| Problems / conditions / diagnoses | ⚠️ Partial | "Assessments" mentioned in PDF content | Unknown whether coded diagnoses (ICD-11) are preserved or just rendered text |
| Medications / prescriptions | ⚠️ Partial | "Medications" mentioned in PDF content | E-prescribing is a core feature (via DrFirst); unclear if full prescription data is in export |
| Allergies | ❌ Not covered | Not mentioned in documentation | Product stores allergy lists; not specifically referenced in export |
| Immunizations | ❌ Not covered | Not mentioned in documentation | Product stores immunization records; not referenced in export |
| Vitals | ❌ Not covered | Not mentioned in documentation | May be under "other clinical data" but not specified |
| Lab results | ❌ Not covered | Not specifically mentioned | "Investigations" image category may include lab-related images, but no structured lab data |
| Imaging / diagnostic reports | ⚠️ Partial | "Investigations" exported as image files | DICOM imaging is a core feature; only raw images exported, no structured reports or DICOM metadata |
| Procedures | ⚠️ Partial | "Surgery consents" exported as images | ASC charting is a major feature; surgical records not specifically addressed beyond consent images |
| Clinical notes / documents | ⚠️ Partial | Case sheet PDFs are essentially clinical notes for each visit | No indication of note types, templates, or completeness |
| Care plans / goals | ❌ Not covered | Not mentioned | Product offers customized care plans; not referenced in export |
| Orders / referrals | ⚠️ Partial | "Referrals" exported as images | Only as image files, not structured order data |
| Insurance / coverage | ❌ Not covered | Not specifically mentioned | Product does insurance eligibility verification; not in export documentation |
| Claims / billing | ⚠️ Partial | "Billings and Authorization files" exported as images | Product has full RCM/billing; export appears to be scanned documents, not structured billing data |
| Payments | ❌ Not covered | Not mentioned | Product has integrated payment gateway; not in export |
| Consents / directives | ⚠️ Partial | "Surgery consents" exported as images | Only surgical consents as images |
| Patient communications / portal messages | ❌ Not covered | Not mentioned | Product has secure messaging, SMS broadcasting, chatbot; none in export |
| Specialty-specific (Ophthalmology) | ❌ Not covered | Not specifically mentioned | Visual acuity, IOP, refraction, DICOM images, anatomical drawings — the core specialty data for this ophthalmology EHR — are not addressed |
| Optical retail / POS | ❌ Not covered | Not mentioned | Product has optical retail management; not in export |

**Summary**: Of 20 applicable domains, **0 are fully covered**, **8 have partial/uncertain coverage** (mostly through vague PDF content), and **12 have no evidence of coverage**. The "partial" ratings are generous — they reflect mentions in the documentation that *might* indicate presence in the PDF output, not confirmed structured data export.

## 6. Documentation Quality

The documentation quality is **extremely poor**:

- **No data dictionary**: Explicitly acknowledged by the vendor ("no 'one size fits all' set of fields")
- **No schema**: No machine-readable format specification of any kind
- **No sample data**: No example PDFs, no sample export files
- **No export instructions**: No screenshots, no step-by-step workflow, no user guide
- **No field-level documentation**: Content described only at broad category level (7 vague labels for PDFs)
- **No value sets or coded fields**: No mention of coding systems, terminologies, or enumerated values
- **No relationship documentation**: Files linked only by filename convention (patient ID)

The substantive technical content of the documentation is approximately **200-300 words** — the remainder is legal boilerplate (terms of use, limitation of liability, indemnification). A developer receiving exported files would have essentially no guidance on what to expect or how to process the data. Reconstruction of a patient record from the export would require manual PDF reading — programmatic processing is not feasible without OCR and considerable guesswork about PDF structure.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Minimal/stub/unclear**

The documentation is too thin to determine what the export actually covers. The described output — appointment-level PDF case sheets plus image attachments — represents at best a rendered snapshot of visit-level clinical data. Even taking the most generous interpretation, there is no evidence that the export covers:
- Structured clinical data (coded diagnoses, discrete vitals, lab values)
- Ophthalmology-specific data (visual acuity, IOP, refraction — the product's core specialty)
- Billing/claims/financial data (despite the product having full RCM capabilities)
- Patient portal content (messages, self-tests, forms)
- Prescriptions (despite e-prescribing being a core feature)
- Optical retail data
- ASC surgical records (beyond consent images)
- Care plans, immunizations, allergy lists

The export appears to be a PDF printout of appointment records — essentially "print to PDF" rather than a data export.

**Axis 2 — Export approach: Unclear/undetermined**

The export is neither a repackaged standard (not C-CDA, not FHIR) nor a recognizable purpose-built data export. It's a PDF/image file dump with no structured data format. This doesn't fit neatly into either "purpose-built" or "repackaged" — it's closer to "print the chart and hand it over." The lack of any structured format, schema, or data dictionary suggests minimal engineering effort was invested in the (b)(10) export. This is not a repackaging of a (g)(10) FHIR API (EHNOTE does have FHIR via Carefluence); it's something even less sophisticated — a rendered document export.

### Key Findings

1. **No structured data in export**: The export produces only PDFs and images — the structured data in the EHR (coded diagnoses, discrete measurements, medication records) is flattened into rendered documents, making the export essentially non-computable.

2. **No data dictionary exists**: The vendor explicitly acknowledges the absence of standardized field definitions. The entire export documentation is ~1,268 words of content, most of which is legal boilerplate. The technical documentation for file naming is about 200-300 words.

3. **Core specialty data is unaddressed**: For an ophthalmology-focused EHR, visual acuity measurements, IOP readings, refraction data, and DICOM imaging metadata are the most critical clinical data. None of these are specifically mentioned in the export documentation.

4. **Billing data is almost certainly not included in structured form**: The product has full revenue cycle management, but the export only mentions "Billings and Authorization files" as image files — likely scanned documents rather than structured claims/charge data.

5. **Export is appointment-level, not patient-level comprehensive**: Each export produces files for individual appointments. There's no indication of a comprehensive patient-level export that includes longitudinal records, cumulative medication lists, problem lists, or cross-visit data.

### Summary Stats

```
Coverage:        Minimal/stub/unclear
Approach:        Unclear/undetermined (PDF/image dump, not repackaged standard and not purpose-built)
Export format:   PDF + PNG/JPEG images
Entities:        5 file categories (not structured entities)
Fields:          11 broad content labels (not discrete fields)
Descriptions:    0% meaningful field-level descriptions
Sample data:     No
Bulk export:     No
Domains covered: 0 of 20 fully; 8 of 20 partially (uncertain)
```

### Bottom Line

A patient or provider would receive appointment-level PDF printouts and associated images — essentially a paper chart in digital form. The export loses all structured data (coded diagnoses, discrete measurements, medication records) and appears to omit major data domains the product stores (billing, specialty ophthalmology data, prescriptions, portal communications, optical retail). This is one of the most minimal (b)(10) implementations possible — a compliance checkbox rather than a genuine effort at health information portability.
