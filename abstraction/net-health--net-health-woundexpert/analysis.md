# EHI Export Analysis: Net Health

**Product**: Net Health® WoundExpert (also white-labeled as WoundDocs by RestorixHealth)
**Analysis date**: 2026-02-16
**CHPL IDs**: 15.04.04.2815.Woun.07.00.1.181231 (WoundExpert), 15.04.04.2272.Woun.07.01.1.191224 (WoundDocs)

## 1. Product Context

Net Health WoundExpert is a **specialty wound care EHR** — not a general-purpose EHR. It is a cloud/web-based system purpose-built for wound care providers (hospital outpatient wound care centers, wound care management companies, long-term care facilities). It supplements rather than replaces a facility's primary hospital EHR (Epic, Cerner, etc.).

Based on product research and certified criteria, WoundExpert stores:

- **Core wound care data**: Wound assessments (size, depth, tissue type, location, etiology, healing stage), wound photographs and automated measurements (via Tissue Analytics), treatment plans, wound dressing recommendations, healing progression tracking
- **Clinical data**: Demographics, problem lists, medication lists, allergy lists, family health history, implantable device lists, vital signs, lab/imaging orders and results, progress notes with customizable templates
- **Billing/financial**: Invoice generation, payment processing, insurance claims management, revenue/expense tracking, billing compliance (per FindEMR listing and vendor materials)
- **Scheduling**: Appointments, reminders, rescheduling
- **Medications**: E-prescribing (via SureScripts), CPOE, drug interaction checking (via First Databank)
- **Transitions of care**: C-CDA documents for referrals, clinical reconciliation
- **Patient portal**: View/download/transmit via Net Health Patient Portal
- **Interoperability**: FHIR R4 API (via Darena Health partnership), HL7 interfaces, ADT feeds

The key question for (b)(10) assessment: does the export cover the specialty wound care data (wound assessments, images, treatment plans, healing trajectories) as well as the supporting clinical and billing data?

## 2. Artifacts Reviewed

| Artifact | Description | Informative? |
|---|---|---|
| `downloads/certification-page.html` (399 KB) | Full HTML of ONC certification page at nethealth.com — contains the only public EHI export documentation | **Primary source** — contains the EHI export section (~97 words) |
| `downloads/certification-page-text.txt` (6.3 KB) | Clean text extraction via WordPress REST API | Useful for parsing; confirms HTML content |
| `downloads/certification-page-full.png` (874 KB) | Full-page screenshot of certification page | Visual confirmation of page layout |
| `downloads/rwt-results-2025.pdf` (187 KB, 11 pages) | Real World Testing Results 2025 | **Low value for (b)(10)** — metric 8 (Data Export) was dropped after Q2 2025 per Executive Order 14192; no (b)(10) results reported |
| `downloads/rwt-plan-2025.pdf` (3.3 MB, 18 pages, image-based PDF) | Real World Testing Plan 2025 — OCR'd via tesseract | **Moderately informative** — Measure 8 describes two export tiers: CDA files (Facility Admin) and full EHI CSV exports (Net Health Admin) |

**No data dictionary, sample export, schema, user guide, or API spec for (b)(10) was available.** The data dictionary (`EHIDataExtract_DataDictionary.xlsx`) exists but is bundled inside each export ZIP and is not publicly downloadable. Multiple paths were probed (`/ehi/`, `/ehi-export/`, `/data-dictionary/`, `/b10/`, WordPress REST API search) — all returned 404 or no results.

## 3. Export Mechanics

- **Format**: ZIP file containing: CSV files of EHI data, image files, custom scans, an XLSX data dictionary, and a TXT export summary. One folder per patient within the ZIP.
- **Mechanism**: Built-in data export tool within WoundExpert. Two tiers of access:
  - *Facility Administrator*: Can generate and download CDA files containing "relevant treatment information" for one or more patients in a date/time range (per RWT Plan 2025)
  - *Net Health Administrator*: Can execute "full facility EHI exports" that include patient medical records in PDF format and all EHI in CSV files (per RWT Plan 2025)
- **Single-patient vs bulk**: Both supported — "Single patient and patient population electronic health information can be exported" (certification page)
- **Access constraints**: The full EHI export requires a "Net Health Administrator" role, not just a Facility Administrator. This suggests the comprehensive export may require vendor involvement or elevated permissions, which could be a practical barrier for facilities.
- **Fees**: No specific fees mentioned for (b)(10) export. Other criteria have associated costs (e.g., EPCS, Direct messaging, FHIR API).

## 4. Export Content: What's In It

### What is publicly documented

The certification page states the export ZIP contains:
1. CSV files of EHI data
2. All image files from the patient record
3. All custom scans on file
4. `EHIDataExtract_DataDictionary.xlsx`
5. `ExportSummary.txt`

**That is the entirety of the public documentation.** No CSV file names, no field names, no data types, no relationships, no value sets, no sample data are provided publicly.

### What can be inferred

- The existence of `EHIDataExtract_DataDictionary.xlsx` indicates Net Health has actually built a structured data dictionary — it's just not publicly available. This is a meaningful positive signal: the export is likely well-organized internally.
- "All image files" likely includes wound photographs (the core imaging data for a wound care EHR).
- "All custom scans" suggests scanned documents (intake forms, consent forms, etc.) are included.
- The phrase "content and format of the data contained within the export zip file depending on number of patients selected and software functionality in use" suggests the CSV contents may vary by which WoundExpert modules a facility uses.
- The RWT Plan confirms two distinct export paths: a CDA-based summary export and a full CSV-based EHI export.

### Vendor's own content organization

No vendor-defined categories or entity/table names are publicly available. Without access to the data dictionary XLSX, no entity inventory can be constructed.

| Entity/Table | Fields | Described | Types | Category |
|---|---|---|---|---|
| *Unknown — no public data dictionary* | N/A | N/A | N/A | N/A |

**Full inventory**: See `analysis/entity-inventory-full.json` — documents the absence of public data and what is known about export components.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor's public documentation is too thin to assess export coverage in any meaningful detail. We know:

1. **CSV files of "EHI data"** — this is a black box. The word "EHI" is promising (it implies intent to export all electronic health information, not just a clinical summary), but without knowing which CSV files exist or what fields they contain, we cannot verify this claim.
2. **Image files** — wound photographs are the core clinical imaging artifact for wound care, so including "all image files" is appropriate and important.
3. **Custom scans** — documents beyond structured data are included.
4. **Data dictionary included** — self-documenting exports are a positive design choice.

The RWT Plan 2025 adds one important detail: the full EHI export includes "patient medical records in PDF format and all EHI in CSV files." This confirms the export produces both a human-readable (PDF) and machine-readable (CSV) representation of patient records.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ❓ Unknown | No public documentation of CSV contents | Product stores demographics (certified (a)(5)); cannot verify inclusion |
| Encounters / visits | ❓ Unknown | No public documentation | Product stores wound care visit data; cannot verify |
| Problems / conditions / diagnoses | ❓ Unknown | No public documentation | Certified (a)(5); cannot verify |
| Medications / prescriptions | ❓ Unknown | No public documentation | Certified (a)(1), (b)(3); cannot verify |
| Allergies | ❓ Unknown | No public documentation | Certified (a)(5); cannot verify |
| Immunizations | N/A | Not a typical wound care EHR function | Product likely doesn't store immunization data natively |
| Vitals | ❓ Unknown | No public documentation | Likely stored for wound care encounters; cannot verify |
| Lab results | ❓ Unknown | No public documentation | Certified (a)(2) CPOE labs; cannot verify export inclusion |
| Imaging / diagnostic reports | ⚠️ Partial | "All image files from the patient record" — wound photos likely included | Wound images explicitly included; lab/diagnostic report data unknown |
| Procedures | ❓ Unknown | No public documentation | Wound care procedures (debridement, etc.) are core data; cannot verify |
| Clinical notes / documents | ⚠️ Partial | "Custom scans" included; RWT mentions "medical records in PDF format" | PDF renditions and scanned docs included; structured note data in CSV unknown |
| Care plans / goals | ❓ Unknown | No public documentation | Treatment plans are core to wound care; cannot verify |
| Orders / referrals | ❓ Unknown | No public documentation | Certified (a)(1-3), (b)(1-2); cannot verify |
| Insurance / coverage | ❓ Unknown | No public documentation | Product has billing/insurance; cannot verify |
| Claims / billing | ❓ Unknown | No public documentation | Product has billing/claims (per vendor materials); cannot verify export inclusion — **potentially significant gap if missing** |
| Payments | ❓ Unknown | No public documentation | Product tracks payments; cannot verify |
| Consents / directives | ⚠️ Partial | "Custom scans" may include consent forms | Scanned consents likely included; structured consent data unknown |
| Patient communications | ❓ Unknown | No public documentation | Patient portal exists; portal messages unknown |
| Specialty-specific (wound care) | ⚠️ Partial | Images included; wound assessment data in CSV unknown | Wound assessments, measurements, tissue types, healing trajectories are the **core** data — critical to verify but impossible from public docs |

**Key gap**: The inability to assess any domain with confidence (except partial credit for images and scans) is itself the most significant finding. For a wound care specialty EHR, the wound assessment data — sizes, depths, tissue types, healing stages, treatment plans — is the most important clinical data. We simply cannot tell whether it's in the export from the public documentation.

## 6. Documentation Quality

**Very poor public documentation.** The EHI export is described in approximately 97 words on the certification page — two short paragraphs and a bullet list. This is among the most minimal (b)(10) documentation possible while still acknowledging the requirement.

Specific deficiencies:
- **No data dictionary** publicly available (exists inside exports but not downloadable)
- **No CSV file/table names** documented
- **No field definitions**, data types, or cardinality
- **No value set** documentation
- **No relationship/foreign key** documentation
- **No sample export** files
- **No export instructions** or user guide
- **No screenshots** of the export interface
- **No worked examples**

A developer could not build an import from this documentation. They would need to obtain an actual export and reverse-engineer the CSV structure from the bundled `EHIDataExtract_DataDictionary.xlsx`.

**Positive signals**: The existence of a bundled XLSX data dictionary and the two-tier export architecture (CDA for facility admins, full CSV for Net Health admins) suggest the actual implementation may be more robust than the public documentation implies. But since the data dictionary is locked inside the export, external assessment is impossible.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Minimal/stub/unclear**

The public documentation is too thin to assess coverage. The vendor claims to export "EHI data" in CSV files but provides zero detail about which data domains are included, which CSV files exist, or what fields they contain. The inclusion of images and custom scans is a positive signal for unstructured data completeness, but the structured data coverage is a complete black box. The phrase "all EHI in CSV files" from the RWT Plan is promising but unverifiable.

Notably, the RWT Plan reveals that the "full" EHI export requires a "Net Health Administrator" role (not a facility-level admin), suggesting the comprehensive export may be vendor-mediated rather than self-service — which could limit practical patient access.

**Axis 2 — Export approach: Purpose-built EHI export**

Despite the minimal documentation, there are clear signals that Net Health built a dedicated (b)(10) export rather than repackaging an existing clinical exchange:

1. The export produces CSV files in a vendor-native format (not C-CDA or FHIR)
2. It includes a custom data dictionary (EHIDataExtract_DataDictionary.xlsx)
3. It's explicitly distinct from the FHIR API (g)(10) — the certification page treats them as separate capabilities
4. The RWT Plan describes it as "Net Health has built a data export tool to meet this certification criterion"
5. It includes non-clinical artifacts (images, scans) beyond what C-CDA or FHIR would provide

The export architecture is appropriate and purpose-built. The problem is entirely in the documentation: we can't verify what's actually in it.

### Key Findings

1. **Documentation is a near-total black box.** The public EHI export documentation is ~97 words. No CSV file names, no fields, no types, no value sets, no sample data. The data dictionary exists but is locked inside the export ZIP — a "you have to buy it to see it" situation that defeats the purpose of public documentation.

2. **The export architecture is sound.** ZIP → per-patient folders → CSV files + images + scans + data dictionary + summary is a well-designed (b)(10) export structure. This is clearly purpose-built, not a clinical exchange repackaging.

3. **Two-tier access model raises concerns.** The RWT Plan reveals that Facility Administrators can only generate CDA files (clinical summaries), while "full facility EHI exports" with CSV data require a "Net Health Administrator" role. This may mean facilities cannot self-serve the complete (b)(10) export — they may need vendor involvement.

4. **RWT metric 8 (Data Export) was dropped.** The 2025 RWT Results report ceased collecting data for the Data Export metric after Q2 2025 (per Executive Order 14192), so no real-world testing results for (b)(10) are available.

5. **Wound-specific data coverage is unverifiable.** For a wound care specialty EHR, the most critical question is whether wound assessments, measurements, tissue types, healing trajectories, and treatment protocols are in the CSV export. The public documentation provides no answer.

### Summary Stats

    Coverage:        Minimal/stub/unclear
    Approach:        Purpose-built EHI export
    Export format:   CSV (in ZIP with images, scans, XLSX dictionary, TXT summary)
    Entities:        N/A (no public data dictionary)
    Fields:          N/A
    Descriptions:    N/A
    Sample data:     No
    Bulk export:     Yes (single patient and population)
    Domains covered: Cannot assess — 0 of ~16 applicable domains verifiable from public docs

### Bottom Line

Net Health built what appears to be a genuine (b)(10) export — CSV-based, purpose-built, with a bundled data dictionary — but published virtually no public documentation about its contents. A patient or developer cannot tell what's in the export without first obtaining one. The single biggest gap is the absence of a publicly available data dictionary: publishing the existing `EHIDataExtract_DataDictionary.xlsx` would immediately transform this from an opaque black box into an assessable export.
