# Sargas Pharmaceutical Adherence and Compliance International — EHI Export Documentation

Collected: 2026-02-15

## Source
- Registered URL: https://www.spacinternational.com/SPAC-Export.pdf
- CHPL ID: 10702
- Product: Sargas International's Chronic Care Management Cloud dba hru2day, VERSION 21.9
- Certification date: 2021-10-14

## Navigation Journal

1. Probed the registered URL with curl:
   ```
   curl -sI -L "https://www.spacinternational.com/SPAC-Export.pdf" -H 'User-Agent: Mozilla/5.0'
   ```
   Result: HTTP 200, Content-Type: application/pdf, Content-Length: 379759 bytes. Direct PDF download — no redirects.

2. Downloaded the PDF:
   ```
   curl -sL "https://www.spacinternational.com/SPAC-Export.pdf" -H 'User-Agent: Mozilla/5.0' -o downloads/SPAC-Export.pdf
   ```
   Verified with `file` and `pdfinfo`: 1-page PDF, created from "Microsoft Word - SPAC-Export.docx", produced with "Microsoft: Print To PDF", dated 2023-12-19 (modified 2025-11-25).

3. Extracted full text with `pdftotext`. The PDF contains only 6 sentences describing the export at a very high level.

4. Checked for embedded URLs and attachments — none found.

5. Checked the mandatory disclosures page at https://www.spacinternational.com/certified-ehr-technology.php — it contains only a certification statement paragraph and a link to the mandatory disclosures PDF (ONC-HIT-CERTIFICATE-DISCLOSURE_ver_21_9_Revised-25.pdf). The disclosures PDF lists certified criteria and pricing but no additional EHI export technical detail.

6. Browsed the open `/pdf/` directory at https://www.spacinternational.com/pdf/ — found ~100 PDFs. All are CCM/RPM brochures, consent forms, white papers, billing guides, Real World Testing plans, and enrollment forms. None contain additional EHI export documentation.

7. Probed common alternative paths (/ehi, /ehi-export, /api, /fhir, /interoperability, /data-export) — all returned 404.

## What Was Found

The entire EHI export documentation consists of a **single 1-page PDF** with 6 sentences. Here is the complete text:

> **Product Name:** Sargas International's Chronic Care Management Cloud dba hru2day®
>
> **Product Version:** VERSION 21.9
>
> The patient EHI export contains data from the patient's chart. Multiple file formats are used to store this information.
>
> ZIP is an archive file format.
>
> PDF or Portable Document Format is a file format that is used to present text or image based documents.
>
> C-CDA or Consolidated Clinical Document Architecture is a file format used for health information exchange.
>
> The export file itself is a zip file. It contains zip files of C-CDAs and PDF files attached to the patient's chart (machine readable PDF)
>
> Information for each patient encounter is available C-CDA format in zip archive.

That is the entirety of the documentation. It tells us:
- The export is a ZIP file
- Inside the ZIP are C-CDA documents (one per encounter) and PDF files from the patient's chart
- The C-CDAs are in nested ZIP archives

There is no data dictionary, no field-level documentation, no schema, no sample data, no API specification, no user guide for performing the export, and no description of what data fields or sections are included in the C-CDAs.

## Export Coverage Assessment

### Data Domain Coverage

The documentation says the export "contains data from the patient's chart" — but does not specify which data elements are included or excluded. Based on the product research, the hru2day platform stores:

**Likely covered (if C-CDA sections are reasonably populated):**
- Patient demographics (C-CDA standard section)
- Problem lists / chronic conditions (C-CDA standard section)
- Medication lists and allergies (C-CDA standard sections)
- Clinical summaries (C-CDA standard section)

**Uncertain — no documentation to confirm or deny:**
- Care plans (the core of what this product does — comprehensive care plans addressing physical, mental, cognitive, psychosocial, functional, and environmental domains). C-CDA has a Care Plan section, but it's unclear if the vendor populates it with the full richness of their care plan data.
- Physiological monitoring data from RPM devices (glucose, BP, heart rate, SpO2, weight). C-CDA is not well-suited for time-series device data. These may be entirely absent from the export.
- Medication adherence records and side effect reports. This is the company's founding specialty (Drug Adherence® for oncology patients). C-CDA has no standard section for medication adherence tracking.
- Care coordination logs (documenting 20+ minutes/month of CCM services) — 200,000+ logged interactions. These are critical billing-supporting records.
- Call center interaction records
- Secure messages between patients, care teams, and providers
- Time tracking for CCM/PCM/RPM services (linked to CPT codes)
- Patient consent records

**Likely missing:**
- Billing-relevant time tracking and service documentation. C-CDA is a clinical document standard; it does not accommodate billing/administrative data well.
- RPM device time-series data. C-CDA cannot reasonably represent continuous glucose readings, daily blood pressure logs, etc.
- Care coordination activity logs. These are workflow records that are core to the product's purpose but have no C-CDA analog.

The fundamental concern is that this is a **chronic care management platform** — its primary value is in care plans, care coordination logs, RPM device data, and medication adherence tracking — none of which map cleanly to C-CDA. Using C-CDA as the sole export format for this product likely means the export captures only the clinical summary data (demographics, problems, meds, allergies) while missing the majority of the product's actual data.

### The (b)(10) vs (g)(10) Question

This is not the typical FHIR-as-b(10) confusion, but it's an analogous problem: the vendor appears to be using their **C-CDA clinical summary export** (which would support (e)(2) Clinical Information Reconciliation and general clinical data exchange) as their (b)(10) EHI export. A C-CDA clinical summary is a standardized subset of clinical data — it is not "all electronic health information" the product stores. The product's differentiating data (RPM telemetry, care coordination logs, medication adherence tracking, CCM time logs) would require a custom export format, not C-CDA.

### Export Format & Standards

- **Format**: ZIP containing C-CDA XML documents (per encounter) and PDF attachments
- **Standard**: C-CDA (Consolidated Clinical Document Architecture) — a recognized health information exchange standard
- **Appropriateness**: C-CDA is a reasonable format for clinical summaries but is fundamentally mismatched with the product's core data. A chronic care management platform's most important data — care coordination logs, RPM device readings, medication adherence tracking, time-based billing records — cannot be expressed in C-CDA. A CSV or database dump of care plan tables, RPM readings, and interaction logs would provide far more complete EHI coverage.
- **Reconstructability**: A third party could reconstruct a basic clinical summary from the C-CDAs, but could not reconstruct the patient's full care management history, device monitoring data, or coordination activity.

### Documentation Quality

The documentation is **extremely minimal** — arguably the minimum viable compliance artifact. Six sentences on one page:
- No data dictionary whatsoever
- No field-level definitions
- No description of which C-CDA sections are populated
- No sample data or example files
- No schema or profile documentation
- No instructions for how to perform the export (who initiates it, from what screen, what parameters)
- No description of how PDFs are organized within the ZIP
- A developer given only this document could not implement an import — they would know only "it's a ZIP with C-CDAs and PDFs inside."

The documentation reads as a certification checkbox, not a genuine guide to the export.

### Structure & Completeness

- **Granularity**: Product and format level only. No table, field, or section-level detail.
- **Value sets**: Not documented
- **Relationships**: Not documented
- **Versioning**: The PDF was last modified 2025-11-25, originally created 2023-12-19. No change history.

## Access Summary
- Final URL (after redirects): https://www.spacinternational.com/SPAC-Export.pdf
- Status: found
- Required browser: no
- Navigation complexity: direct_link
- Anti-bot issues: none

## Obstacles & Dead Ends
- No obstacles accessing the PDF — it's a direct, unauthenticated download.
- No additional EHI export documentation found anywhere on the vendor's website despite checking the certification page, mandatory disclosures, the open /pdf/ directory listing (~100 files), and probing common alternative URL paths.
- The entire vendor website is focused on CCM/RPM service marketing and Medicare billing compliance. Technical product documentation appears to be essentially absent from the public-facing site.
