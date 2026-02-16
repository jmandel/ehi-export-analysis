# EHI Export Analysis: EHNOTE, INC

**Product**: EHNOTE v1.0
**Analysis date**: 2026-02-16
**CHPL IDs**: 11356 (15.04.04.3171.EHNO.01.00.1.231025)

## 1. Product Context

EHNOTE is a cloud-based EHR and practice management platform built primarily for ophthalmology and eye care practices, developed by EHNOTE, Inc. (Plano, TX). The vendor claims 200+ specialty practices in the USA and India. Certified 2023-10-25.

The product spans a broad set of functional domains relevant to EHI completeness assessment:

- **Clinical EHR/Charting**: Subspecialty ophthalmology templates, multi-layered anatomical drawing pad, DICOM imaging integration, visual acuity/IOP/refraction tracking, drug interaction checking, ICD-11 coded diagnoses
- **E-Prescribing**: Via DrFirst Rcopia integration
- **Ambulatory Surgery Center (ASC)**: Pre-op, intra-op, post-op, anesthesia documentation, operative notes
- **Practice Management**: Multi-view scheduling, insurance eligibility verification, multi-location management
- **Revenue Cycle Management / Billing**: Integrated billing, claims processing, accounts receivable, payment gateway
- **Optical Point-of-Sale**: Eyeglasses/contact lens retail, inventory management
- **Patient Portal**: Health records access, secure messaging, care plans, self-vision testing
- **Telemedicine**: Video consultations with real-time charting
- **Analytics**: Clinical analytics, population health, MIPS dashboard, revenue analytics
- **Additional specialty modules**: Dental, gynecology, pediatrics, general physician

The product also uses third-party components: Carefluence Open API R4 (FHIR), DrFirst Rcopia (e-prescribing), EMR Direct (Direct messaging), and Concurred (fax).

This is a feature-rich product storing clinical, billing, optical retail, surgical, and patient engagement data across multiple specialties — setting a high bar for what a complete EHI export should cover.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/ehi-export-page.html` (31,265 bytes) | The complete EHI export documentation — a single static HTML page. Contains 6 sections: Introduction, Understanding the Files, Linking the Files, Understanding the Fields and Descriptions, Usage Terms, Contact Information. ~592 words of technical content, ~659 words of legal boilerplate. | **Primary artifact** — this is the entirety of the vendor's EHI export documentation |
| `downloads/ehi-export-page-screenshot.png` (835 KB) | Full-page screenshot of the EHI export documentation page | Confirms HTML content renders as expected; no hidden/dynamic content |
| `downloads/ehi-export-page-top.png` (203 KB) | Viewport screenshot of top portion | Confirms color-coded naming convention examples visible in browser |
| `product-research.md` | Prior research on EHNOTE's product capabilities | Useful for establishing baseline of what data the product stores |
| `ehi-export-report.md` | Prior agent's narrative analysis | Orientation; claims independently verified against HTML source |
| `files.json` | Manifest of downloaded artifacts | Confirmed: only 3 files in downloads/, all from the single EHI export page |

**Key finding**: There are zero downloadable files (no PDFs, ZIPs, CSVs, JSON schemas, XLSX data dictionaries, or sample exports). The entire EHI export documentation is inline HTML text on a single web page. This was verified both by parsing the HTML (0 download links to data files found) and by visual inspection of the screenshots.

The live page was verified accessible at `https://ehnote.com/certification/ehi-export` (HTTP 200, `Last-Modified: 2025-06-03`).

## 3. Export Mechanics

- **Format**: PDF files (clinical case sheets) and PNG/JPEG image files (investigations, surgery consents, referrals, billing/authorization documents)
- **Mechanism**: UI-based — user clicks an "export and download" button in the EHR. Files are "downloaded individually" per the documentation.
- **Scope**: Single-patient export. The documentation states: "An export will include a single patient, depending on the specifications."
- **Bulk capability**: No evidence of bulk/multi-patient export capability.
- **Fees**: "No extra costs" for basic export. Potential fees "if the export size exceeds the contracted available size of your instance" for cloud-hosted clients.
- **No API**: No programmatic export endpoint. The FHIR API (Carefluence Open API R4 at `openapi.ehnote.com`) is for the (g)(10) standardized API criterion, not the (b)(10) EHI export.

## 4. Export Content: What's In It

### No data dictionary

EHNOTE provides **no data dictionary, no schema, no field-level documentation, and no sample data**. The vendor explicitly acknowledges this:

> *"There is no 'one size fits all' set of fields in the software because of the extensive customization that is possible."*

The only description of export content is a single sentence:

> *"DATA: Name of the clinic, patient demographics, Chief complaints, Review of systems, Assessments, Medications and other clinical data part of the appointment"*

This describes the contents of the PDF case sheet files at a category level — no individual fields, types, value sets, or structures are documented.

### Vendor's own content organization

The documentation describes 5 categories of exported files. None have field-level documentation:

| Category | Format | Fields Documented | Types | Description |
|---|---|---|---|---|
| Case sheets (case history) | PDF | 0 | No | Per-appointment clinical history. Content described only as: "demographics, Chief complaints, Review of systems, Assessments, Medications and other clinical data" |
| Investigations | PNG/JPEG | 0 | No | Image files of investigation results |
| Surgery consents | PNG/JPEG | 0 | No | Image files of surgery consent forms |
| Referrals | PNG/JPEG | 0 | No | Image files of referral documents |
| Billings and Authorization files | PNG/JPEG | 0 | No | Image files of billing and authorization documents |

**Total entities documented**: 0 (no structured entities/tables)
**Total fields documented**: 0
**Fields with descriptions**: 0
**Machine-readable artifacts**: None

### What the export actually is

The export is essentially a **"print to PDF" of the visit record** plus associated scanned/attached image documents. Key characteristics:

1. **Appointment-centric**: Each PDF covers one appointment for one patient. There is no patient-level summary or longitudinal record — the export is fragmented across individual visit PDFs.
2. **Non-computable**: All structured data in the EHR (ICD-coded diagnoses, medication lists, vitals, lab values) is flattened into rendered PDF text. A recipient cannot programmatically extract individual data elements without OCR/PDF parsing.
3. **Images are opaque**: The image files (investigations, consents, referrals, authorization documents) are raw image files with no metadata or structured content — they are whatever was scanned or uploaded into the EHR.
4. **File linking by naming convention only**: Files for the same patient share a `P####` patient identifier in the filename. Files for the same appointment share the patient ID and date. There is no manifest file, index, or structured linkage.

### Naming conventions

- **PDFs**: `CaseSheet_{BranchId}P{PatientId}_A{AppointmentDate}.pdf`
  - Example: `CaseSheet_731P518612_A2023-12-08.pdf`
- **Images**: `{PatientName}_P{PatientId}_{Date}.{ext}`
  - Example: `Alice_P2546_2023-01-08.PNG`

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor's documentation describes 5 categories of exported content, all in non-computable formats (PDF and image files):

1. **Case sheets** (PDF): The richest category — contains the clinical visit record as a rendered PDF. Content is described only at the category level (demographics, complaints, review of systems, assessments, medications). No field-level detail.
2. **Investigations** (images): Diagnostic images or scanned investigation results. No description of what types of investigations or what data they contain.
3. **Surgery consents** (images): Scanned consent forms.
4. **Referrals** (images): Scanned or generated referral documents.
5. **Billings and Authorization files** (images): The documentation mentions "Billings and Authorization files" as a category but provides no detail on whether this includes actual billing data (charges, CPT codes, claim submissions, payment records) or merely scanned authorization/pre-authorization documents. Given the image format (PNG/JPEG), these are almost certainly scanned documents, not structured billing data.

The documentation is too thin to determine whether the case sheet PDFs contain the full structured clinical record or a subset. The phrase "other clinical data part of the appointment" is vague and could encompass vitals, lab results, procedures, and ophthalmic measurements — or it could mean only what appears on a standard visit summary printout.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | Mentioned in case sheet PDF content description | May appear in PDFs but no field-level detail; not structured/extractable |
| Encounters / visits | ⚠️ Partial | Each PDF represents one appointment | Appointments are represented but only as rendered PDFs; no structured encounter data |
| Problems / conditions / diagnoses | ⚠️ Partial | "Assessments" mentioned in case sheet content | Likely present in PDFs but as rendered text, not coded ICD data |
| Medications / prescriptions | ⚠️ Partial | "Medications" mentioned in case sheet content | Product uses DrFirst Rcopia for e-prescribing; unclear if prescription transmission records are in the export |
| Allergies | ❌ Not covered | Not mentioned in documentation | Product stores allergy data (certified for (a)(1)); not mentioned in export |
| Immunizations | ❌ Not covered | Not mentioned in documentation | Product is certified for immunizations; not mentioned in export |
| Vitals | ❌ Not covered | Not specifically mentioned | May fall under "other clinical data" in PDFs but not documented |
| Lab results | ❌ Not covered | Not specifically mentioned | "Investigations" category exists but is image files only; no structured lab data |
| Imaging / diagnostic reports | ⚠️ Partial | "Investigations" category exports images | DICOM integration is a key product feature; export only produces PNG/JPEG images, not DICOM files or structured reports |
| Procedures | ❌ Not covered | Not specifically mentioned | Product has ASC charting with operative notes; not mentioned in export |
| Clinical notes / documents | ⚠️ Partial | Case sheet PDFs contain visit documentation | Visit notes are exported as PDFs; but no mention of operative notes, discharge summaries, or other note types |
| Care plans / goals | ❌ Not covered | Not mentioned | Product has care plans viewable via patient portal; not in export |
| Orders / referrals | ⚠️ Partial | "Referrals" category exists as image files | Referrals exported as images only; no structured order data |
| Insurance / coverage | ❌ Not covered | Not mentioned | Product does insurance eligibility verification; insurance data not in export |
| Claims / billing | ❌ Not covered | "Billings and Authorization files" mentioned but as image files only | Product has integrated billing, claims, and RCM. Export appears to include only scanned authorization images, not structured billing/claims data. **Significant gap.** |
| Payments | ❌ Not covered | Not mentioned | Product has integrated payment gateway; payment data not in export |
| Consents / directives | ⚠️ Partial | "Surgery consents" category exports image files | Only surgery consents as images; no structured consent records |
| Patient communications / portal messages | ❌ Not covered | Not mentioned | Product has secure messaging portal; not in export |
| Specialty-specific (Ophthalmology) | ❌ Not covered | Not specifically addressed | Visual acuity, IOP, refraction, anatomical drawings, DICOM images — the core specialty data for this ophthalmology EHR — are not documented in the export. May appear in case sheet PDFs but as rendered text, not structured measurements. **Critical gap for an ophthalmology-focused product.** |

**Summary**: Of 18 applicable domains, 0 are fully covered, 7 have partial evidence (mostly meaning "might appear in a PDF but not as structured data"), and 11 show no evidence of coverage. The partial ratings are generous — they reflect that some data *might* appear in the rendered case sheet PDFs, but there is no documentation confirming this and the data would not be in a computable format.

## 6. Documentation Quality

The EHI export documentation is **extremely thin and practically unusable** for its stated purpose:

- **Total technical content**: ~592 words (excluding ~659 words of legal boilerplate)
- **No data dictionary**: Zero fields documented. The vendor explicitly states there is no standard set of fields.
- **No schema or format specification**: Beyond file naming conventions, there is no specification of what the PDFs contain or how they are structured.
- **No sample data**: No example PDFs, no example image files, no screenshots of what an exported case sheet looks like.
- **No machine-readable artifacts**: No JSON schema, no CSV template, no XML schema, no FHIR profiles, no database schema.
- **No export instructions**: No step-by-step guide, no screenshots of the export UI, no user workflow documentation. Only a passing reference to an "export and download button."
- **No relationship documentation**: File linkage is described only through naming convention (shared patient ID in filename).

**Could a developer build an import from this documentation?** No. A developer receiving these exported PDFs and images would have no specification for what fields to expect, what format they are in within the PDF, or how to parse them. They would need to reverse-engineer the PDF structure from sample files — which are not provided.

The documentation reads as a minimal compliance artifact rather than a practical technical guide. The substantive content (excluding boilerplate) is approximately one page of text describing file naming conventions.

## 7. Overall Assessment

### Classification

**Minimal/stub**: The documentation is too thin to fully assess the export, but what is described — per-appointment PDF case sheets and image files — clearly covers only a small fraction of what the product stores. There is no data dictionary, no schema, no sample data, and no structured export format. The export appears to be a "print to PDF" of the visit record plus scanned document images.

### Key Findings

1. **Export is non-computable PDFs and images**: All structured EHR data (coded diagnoses, medications, vitals, ophthalmic measurements) is flattened into rendered PDF text and raw image files. This is the least computable export format possible — a recipient cannot programmatically extract individual data elements. (Source: `ehi-export-page.html`, sections 2 and 4)

2. **No data dictionary exists**: The vendor provides zero field-level documentation and explicitly acknowledges this: *"There is no 'one size fits all' set of fields."* The only content description is a single sentence naming 6 broad categories. (Source: `ehi-export-page.html`, section 4)

3. **Critical specialty data gaps**: EHNOTE is primarily an ophthalmology EHR, yet the export documentation makes no mention of visual acuity measurements, IOP readings, refraction data, DICOM images, or anatomical drawings — the core structured clinical data for the product's primary specialty. (Source: comparison of `product-research.md` specialty features vs. `ehi-export-page.html`)

4. **Billing and financial data not meaningfully exported**: The product includes integrated billing, claims processing, RCM, and payment gateway. The export mentions "Billings and Authorization files" but only as image files (PNG/JPEG) — almost certainly scanned documents rather than structured billing data. (Source: `ehi-export-page.html`, section 2)

5. **Single-patient, appointment-fragmented export**: The export is single-patient only with no bulk capability. Each appointment generates a separate PDF — there is no longitudinal patient record, no manifest, and no structured linkage between files beyond filename conventions. (Source: `ehi-export-page.html`, sections 2-3)

### Summary Stats

```
Classification:  Minimal/stub
Export format:   PDF + PNG/JPEG images
Model type:      Rendered documents (print-to-PDF), not native database or standard projection
Entities:        0 (no data dictionary)
Fields:          0 (no field-level documentation)
Descriptions:    N/A
Sample data:     No
Bulk export:     No
Domains covered: 0 of 18 fully; 7 of 18 partially (data may exist in PDFs but undocumented and non-computable)
```

### Bottom Line

EHNOTE's EHI export is a per-appointment PDF printout of the clinical visit record plus scanned image attachments — the minimum conceivable interpretation of "export." For a product that stores structured ophthalmology data, billing records, surgical documentation, patient portal communications, and optical retail data across multiple specialties, exporting only rendered PDFs and images fails to make the vast majority of EHI available in any usable form. The documentation is among the thinnest reviewed: ~592 words of technical content, no data dictionary, no schema, no sample data.
