# Carbon Health Technologies, Inc. — EHI Export Documentation

Collected: 2026-02-16

## Source
- Registered URL: https://ehr-support.carbyos.com/certification-disclosures
- CHPL IDs: 11590 (version 2, certified 2025-01-29), 11700 (version 3, certified 2025-09-25)
- Product: CarbyOs EHR

## Navigation Journal

1. **Initial probe**: `curl -sI -L "https://ehr-support.carbyos.com/certification-disclosures"` returned HTTP 200 with `Content-Type: text/html; charset=utf-8`, 49,799 bytes. Hosted on Vercel (Next.js/Nextra static site).

2. **Page fetch and examination**: Downloaded full HTML. The page is a static Nextra documentation site with a sidebar navigation and a single-page layout containing sections for:
   - ONC Health IT Certification (vendor info, certification details)
   - Multi-Factor Authentication
   - **EHI Export Functionality** (the target section)
   - FHIR API Documentation (with download link)
   - Safety Enhanced Design Document (with download link)

3. **Downloadable file links found**:
   - `/carbonhealth-fhir-api-doc-v1_2.pdf` — FHIR API documentation (g)(10)
   - `/sed-testing.pdf` — Safety Enhanced Design usability report

4. **Downloaded both PDFs**:
   - `curl -sL "https://ehr-support.carbyos.com/carbonhealth-fhir-api-doc-v1_2.pdf" -o carbonhealth-fhir-api-doc-v1_2.pdf` — verified as PDF, 74 pages, 1.4MB
   - `curl -sL "https://ehr-support.carbyos.com/sed-testing.pdf" -o sed-testing.pdf` — verified as PDF, 36 pages, 522KB

5. **Explored site for additional EHI documentation**:
   - Checked all sidebar pages (clinic-patient-workflow, practice-management, billing-and-insurance, etc.) — none contain EHI export content.
   - Checked carbyos.com main site — marketing site, no documentation links.
   - Attempted to reach FHIR CapabilityStatement at `https://api-gateway.production.awscarbonhealth.com/hapi-fhir/metadata` — no response (likely requires authentication).
   - **No data dictionary, schema file, sample export, or additional EHI export documentation exists anywhere on the site.**

6. **Took screenshots** of the certification disclosures page (top, EHI section, full page) for archival.

## What Was Found

### EHI Export Section (on the certification-disclosures page)

The EHI Export documentation is a brief prose section embedded directly in the certification disclosures HTML page. It contains approximately 150 words total. Here is the complete substance:

**Export mechanism**: CarbyOs EHR supports both single-patient and patient-population (bulk) EHI exports.

**Export formats**:
- **C-CDA documents** for clinical records
- **PDFs** for billing and claims information
- **Original native formats** for uploaded documents

**Exclusions**: Psychotherapy notes (per 45 CFR 164.501) and information compiled for legal proceedings.

**Access control**: System administrators manage the ability to perform EHI exports.

**No other EHI export documentation exists.** There is no data dictionary, no field-level documentation, no schema, no sample exports, no instructions for how to perform the export, and no description of what specific data elements are included in the C-CDA or billing PDFs.

### FHIR API PDF (carbonhealth-fhir-api-doc-v1_2.pdf)

This is a 74-page document for the **170.315(g)(10) SMART-on-FHIR API** — not the (b)(10) EHI export. It documents:
- SMART on FHIR app launch flows (standalone, EHR-embedded, backend services)
- OAuth 2.0 authentication (symmetric, asymmetric, public client)
- FHIR R4 endpoints and USCDI v3 data class mappings to US Core 6.1.0 profiles
- Supported FHIR resources: Patient, AllergyIntolerance, CarePlan, CareTeam, Condition, Coverage, Device, DiagnosticReport, DocumentReference, Encounter, Goal, Immunization, Location, MedicationDispense, MedicationRequest, Observation, Procedure, ServiceRequest, Organization, Practitioner, Provenance, RelatedPerson, Specimen

This document is relevant for understanding what clinical data the product can expose via FHIR, but it explicitly covers only the USCDI v3 subset — not the full EHI designated record set.

### Safety Enhanced Design PDF (sed-testing.pdf)

A 36-page NISTIR 7742 usability test report from August 2025. This documents usability testing of the CarbyOs EHR interface. Not relevant to EHI export data content, but included for completeness as it was on the certification disclosures page.

## Export Coverage Assessment

### Data Domain Coverage

The product research identifies CarbyOs as storing extensive clinical, billing, operational, and patient engagement data. The EHI export description makes only the following claims:

| Data Domain | Covered? | Evidence |
|---|---|---|
| Clinical records (notes, problems, meds, labs, vitals, allergies) | Claimed via "C-CDA documents" | No specifics — which C-CDA sections? What templates? |
| Billing and claims | Claimed via "PDFs" | No detail on what billing data is included. PDFs are not computable. |
| Uploaded documents | Claimed via "original native formats" | Reasonable approach for uploaded artifacts |
| E-prescriptions | Unknown | Not mentioned separately; may be in C-CDA |
| Lab orders/results | Unknown | May be in C-CDA, not specified |
| Imaging orders/references | Unknown | May be in C-CDA, not specified |
| Referral packages | Unknown | Not mentioned |
| Care plans | Unknown | May be in C-CDA, not specified |
| Patient engagement data (messages, scheduling) | Unknown | Not mentioned |
| Insurance/eligibility information | Unknown | Possibly in billing PDFs, not specified |
| AI-generated charting data (SOAP notes from ambient AI) | Unknown | Not mentioned — significant gap given this is the product's flagship feature |
| Claim scrubbing/correction history | Unknown | Not mentioned |
| Payment records | Unknown | Possibly in billing PDFs, not specified |

**Critical observation**: The export description says "C-CDA documents for clinical records" but provides zero detail about which C-CDA document types, templates, or sections are included. A C-CDA could range from a minimal CCD (essentially a USCDI summary) to a comprehensive export with custom sections. Without a data dictionary or template documentation, it's impossible to assess actual coverage.

**Billing as PDF**: Exporting billing data as PDFs is problematic for (b)(10) compliance. PDFs are technically "electronic" but barely "computable." A third party receiving billing PDFs would need to OCR or manually extract data. The regulation requires export in an "electronic and computable" format. Structured billing data (claims, charges, payments) would be better served by CSV, 837, or JSON exports.

### Export Format & Standards

- **Clinical data**: C-CDA (a recognized standard, but scope unknown)
- **Billing data**: PDF (not computable — a significant weakness)
- **Uploaded documents**: Original native formats (reasonable)

The use of C-CDA for clinical data is appropriate if implemented comprehensively. However, without documentation of which C-CDA templates and sections are used, we cannot assess whether this covers only a USCDI summary (essentially the same as g(10) output in document form) or the full clinical record.

The FHIR API documentation covers the same USCDI v3 data classes that would be in a standard CCD/CCD-A. If the (b)(10) C-CDA export is just a CCD generated from the same data that feeds the (g)(10) API, then the (b)(10) export adds no additional coverage beyond what's already available via the standardized API — it would be a (g)(10) equivalent in C-CDA clothing, not a true "all EHI" export.

### Documentation Quality

**Extremely poor.** The EHI export documentation consists of approximately 150 words of marketing-quality prose on the certification disclosures page. There is:

- **No data dictionary** — no listing of tables, fields, data types, or relationships
- **No schema documentation** — no C-CDA templates specified, no XSD references
- **No sample exports** — no example files showing what the output looks like
- **No export instructions** — no screenshots, no step-by-step guide for performing an export
- **No format specification** — "C-CDA documents" and "PDFs" is the entire format description
- **No field-level documentation** — impossible to know what's included or excluded
- **No value set documentation** — no coded field definitions
- **No relationship documentation** — no description of how clinical and billing data link together

A developer tasked with importing this data would have essentially no information to work with beyond "expect some C-CDA files and some PDFs."

### Structure & Completeness

The documentation is effectively a compliance checkbox statement — it asserts that the export exists and lists three format categories, but provides no technical substance. This is among the least detailed EHI export documentation possible while still technically making a claim about (b)(10) compliance.

**Key gaps**:
1. **No data dictionary at all** — this is the most fundamental gap. Without knowing what data elements are exported, the documentation is effectively empty.
2. **Billing PDFs are not computable** — this likely fails the "electronic and computable" requirement of (b)(10).
3. **No mention of specialty-specific data** — CarbyOs is used in urgent care and primary care. While these are relatively standard clinical settings, the product's AI-generated charting data (a core differentiator) is not discussed in the export context.
4. **No distinction from (g)(10)** — there's no indication that the (b)(10) export covers anything beyond what's already available through the FHIR API, except for billing PDFs and uploaded documents.
5. **No bulk export format documentation** — the population-level export is mentioned but not described technically. Is it a ZIP of individual C-CDAs? A different format?

### Overall Assessment

Carbon Health's EHI export documentation is minimal and non-technical. The certification disclosures page makes the required (b)(10) compliance assertion but provides no supporting technical documentation. The only downloadable technical document (the FHIR API PDF) covers the (g)(10) standardized API, not the (b)(10) EHI export.

This is compounded by the company's February 2026 Chapter 11 bankruptcy filing. While operations reportedly continue, the sparse documentation may reflect limited investment in compliance documentation infrastructure. The version 2 product (CHPL 11590, certified January 2025) was certified only for (b)(10) and infrastructure criteria, suggesting minimal initial certification. Version 3 (CHPL 11700, certified September 2025) added comprehensive clinical and API certifications, but the EHI export documentation did not appear to be enhanced.

The export approach itself (C-CDA for clinical + PDF for billing + native for uploads) is reasonable in concept, but the total absence of technical documentation makes it impossible to verify actual coverage or quality. The billing-as-PDF approach is a specific concern for computability.

## Access Summary
- Final URL (after redirects): https://ehr-support.carbyos.com/certification-disclosures
- Status: found
- Required browser: no (static HTML, no JavaScript needed for content)
- Navigation complexity: direct_link (EHI section on the single page, linked via anchor #ehi-export-functionality)
- Anti-bot issues: none

## Obstacles & Dead Ends
- No obstacles accessing the page or downloading files.
- FHIR production endpoint (`api-gateway.production.awscarbonhealth.com`) returned empty responses (requires authentication) — no public CapabilityStatement available.
- No additional EHI documentation was found anywhere on the ehr-support.carbyos.com site, the carbyos.com main site, or linked from the certification disclosures page.
- The SED PDF and FHIR API PDF contained no links to additional EHI export documentation.
