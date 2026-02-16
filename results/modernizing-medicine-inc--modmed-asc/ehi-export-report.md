# EHI Export Documentation Report: ModMed ASC

**Collection Date:** 2026-02-15
**Product:** ModMed ASC version 6
**Vendor:** Modernizing Medicine, Inc.
**CHPL ID:** 11701
**Certification Date:** 2025-09-02
**Registered URL:** https://www.modmed.com/asc-onc-certification/

---

## Navigation Journal

### Step 1: Probe the Registered URL

Attempted to curl the registered URL `https://www.modmed.com/asc-onc-certification/`. Received a 403 Forbidden response from Cloudflare's anti-bot protection. The site requires browser-like headers to access content.

### Step 2: Navigate via Browser

Opened the registered URL in Chrome. The page loaded successfully and is titled "ModMed ASC ONC Certification." The page has several sections:

- **EHI Export Documentation** — Contains one link: "Data Dictionary for ModMed gGastro EHI Export" pointing to a PDF.
- **Intervention Risk Management** — PDSI Risk Management Summary PDF.
- **Real World Testing Plans and Results** — Multiple year plans/results (not EHI-specific).
- **Multi-Factor Authentication Use Case** — MFA documentation PDF.
- **Mandatory Disclosures** — PDF describing capabilities, costs, and requirements.
- **ModMed ASC Certification** — Compliance certificate PDF from Drummond Group.

A "SELECT A SESSION 7" element appeared on the page but was investigated and found to be a decorative Divi page builder element, not a functional dropdown or navigation control. The "7" corresponds to the number of sections on the page.

A link to "Technical API Documentation" at `https://portal.api.modmed.com/` was also present.

### Step 3: Download EHI Export Documentation

Downloaded the primary EHI export document:

- **gGastro-Patient-Export-Specifications.pdf** (2,319,825 bytes, 168 pages)
  - Title: "gGastro Patient Export Specifications"
  - Version: 6.4.4.20250707
  - Source: `https://www.modmed.com/wp-content/uploads/2025/08/gmd-13030-gGastro-Patient-Export-Specifications.pdf`

Initial curl attempts returned HTML (Cloudflare challenge pages) instead of PDF content. Adding an `Accept: application/pdf,*/*` header along with User-Agent, Referer, and Accept-Language headers resolved the issue.

### Step 4: Download Supporting Documents

Also downloaded from the ASC certification page:

- **ASC-Mandatory-Disclosures.pdf** (148,559 bytes, 5 pages) — describes ModMed ASC capabilities (EHR, patient portal, lab interface), associated costs, contractual requirements, and technical requirements for each certified capability.
- **ModMed-ASC-Certification.pdf** (331,011 bytes, 1 page) — Drummond Group compliance certificate confirming ModMed ASC 6 certification on 09/02/2025.

### Step 5: Examine the EHI Export Data Dictionary

The 168-page PDF is organized into five sections:

1. **CSV Files Dictionary** (pp 1–87): Defines ~416 CSV entities/tables with field-level detail including column position, field name, data type, maximum length, format/translation references, and comments.

2. **Data Schema** (pp 88–95): A hierarchical tree view showing parent-child relationships between all CSV tables, rooted at "Patient." Each node shows the related table name and the foreign key field linking them.

3. **Translations** (pp ~96–162): Value set lookup tables for coded fields. Categories include Billing, Configuration, Patient, Report, Scheduler, Security, and Service Components. Each translation maps numeric codes to human-readable values.

4. **Patient Documents** (pp ~163–166): Instructions for reconstructing file pointers for five document types:
   - Service Documents (clinical docs attached to procedures)
   - Imaging Documents
   - Patient Portal Documents
   - Statements
   - Letters

5. **Glossary** (p 168): Definitions of data types (Alphanumeric, Boolean, Date, Date & Time, Decimal, GUID, Numeric, Time, XML).

### Step 6: Check Other ModMed Certification Pages

Checked sibling certification pages linked from the ASC page footer:

**EMA ONC Certification** (`https://www.modmed.com/onc-certification/`):
- Has a separate EHI export document: "Data Dictionary for ModMed EMA EHI Export" (different product, not directly relevant to ASC).

**gGastro ONC Certification** (`https://www.modmed.com/onc-certification-gi/`):
- Has TWO EHI export documents:
  1. "Data Dictionary for ModMed gGastro EHI Export" — Version 6.5.3.20251230 (167 pages, 14.4 MB). This is a newer version of the same document found on the ASC page (which was version 6.4.4.20250707).
  2. "Data Dictionary for ModMed gGastro EHI Export Additional" (551 pages, 16.9 MB). A supplementary document containing extended translation/value set tables, starting with a massive "Occupation" table mapping thousands of SOC occupation codes to job titles.

Both additional documents were downloaded. The Dec 2025 version has the same ~416 entities as the Aug 2025 version with minor updates. The "Additional" document provides the full reference data for translation columns that were summarized or truncated in the main document.

### Step 7: Check Technical API Documentation Portal

Navigated to `https://portal.api.modmed.com/`. This is the **FHIR API portal** for §170.315(g)(10) — the standardized API certification, not the full EHI export. It describes:
- **EMA Proprietary FHIR API** — A non-certified API for extending EMA capabilities.
- **EMA and gGastro Certified FHIR API** — HL7 FHIR R4 compliant, supports USCDI data exchange, bulk data export in NDJSON format, SMART on FHIR.

This is a separate, narrower data access channel than the CSV-based full EHI export. The FHIR API provides USCDI-scoped data in standardized FHIR format, while the EHI export provides ALL electronic health information in CSV format.

### Step 8: Screenshots

Captured full-page and viewport screenshots of the ASC ONC Certification page.

---

## What Was Found

ModMed ASC's EHI export is documented through a comprehensive **CSV-based data dictionary** (the "gGastro Patient Export Specifications"). The ASC product is built on the gGastro platform, so both share the same underlying data model and export mechanism.

**Export Format:** The export produces a package of CSV files, one per entity/table. The data dictionary provides complete field-level documentation for every CSV file.

**Export Scope:** The export covers approximately **416 distinct CSV entities** spanning:

- **Clinical Data:** Patient demographics, allergies, diagnoses (ICD-10), problems, vital signs, clinical notes, addenda, questionnaire responses
- **Procedures & Services:** Service records, procedure documentation, findings, impressions, pathology, anesthesia records (Aldrete scores, anesthesia complications), ASC quality measures
- **Medications:** Prescriptions, administered medications, drug interactions, medication allergies, pharmacy details
- **Scheduling:** Appointments, appointment sets, holds, reminders, wait lists, kiosk snapshots
- **Billing:** Charges, claims, payments, collections, adjustments, insurance, EDI transactions, billing batches, patient prepay, authorization, fee schedules (30+ billing-related entities)
- **Orders & Results:** Lab orders, lab results, imaging orders, interface specimens, radiology reports
- **Documents:** Service documents, imaging documents, patient portal documents, statements, letters, faxes
- **GI-Specific:** AGA export/service (registry data), GIQUIC exports, findings, impressions, endoscopy follow-ups, colonoscopy data
- **Ophthalmology:** Service procedure ophthalmology, lens data
- **Cardiology:** Cardiology procedures, carotid ultrasound, echocardiography (TTE), nuclear perfusion, stress tests, HeartCentrix
- **Patient Portal:** Portal messages, kiosk data, appointment reminders, patient consent
- **Administrative:** Staff, locations, users, task management, audit logs, configurations
- **Telehealth:** Telehealth session data
- **Quality Reporting:** ASC quality measures, AGA registry data, GIQUIC registry data

**Data Schema:** A complete relationship model showing how all 416 tables connect hierarchically through foreign key relationships, rooted at the Patient entity.

**Translations/Value Sets:** Coded fields reference translation tables providing human-readable values for dozens of domains (billing codes, appointment statuses, procedure types, clinical scores, etc.). An additional 551-page supplementary document provides extended value sets including occupation codes.

**Document Reconstruction:** Instructions explain how to reconstruct file paths for binary documents (PDFs, images) associated with services, imaging, portal uploads, statements, and letters.

---

## Export Coverage Assessment

### Data Domain Coverage: STRONG

The ~416 CSV entities cover an exceptionally broad range of clinical, administrative, and financial data domains. The export goes well beyond USCDI minimum requirements to include:

- Complete billing/claims data (30+ entities)
- Specialty-specific clinical data (GI, ophthalmology, cardiology)
- ASC-specific operational data (quality measures, anesthesia records)
- Patient portal and engagement data
- Scheduling and administrative data
- Full document/attachment reconstruction support

This appears to export the **complete database schema** rather than a curated subset, which is the ideal approach for §170.315(b)(10) compliance.

### Format & Standards: PROPRIETARY BUT WELL-DOCUMENTED

- **CSV format** — widely readable by any spreadsheet or data tool, but not a healthcare-specific standard (not FHIR, C-CDA, etc.)
- **Proprietary schema** — the entity names and field structures are ModMed/gGastro-specific, requiring the data dictionary to interpret
- **GUID-based identifiers** — all records use GUIDs as primary/foreign keys
- **Coded values require translation tables** — many fields contain numeric codes that must be cross-referenced with the translation section

### Documentation Quality: STRONG

- **Field-level documentation** for every entity: column position, name, type, length, format/translation references
- **Complete relationship schema** showing how tables connect
- **Value set translations** for all coded fields (with supplementary 551-page document for extended sets)
- **Document reconstruction instructions** for binary content
- **Glossary** of data types used
- **Versioned documents** (version 6.4.4 on ASC page, 6.5.3 on gGastro page) indicate active maintenance

### Structure & Completeness: STRONG

- All entities have consistent documentation format
- Foreign key relationships are explicitly documented in the Data Schema section
- Translation tables map codes to human-readable values
- The export covers clinical, financial, operational, and engagement data

### Overall Assessment

ModMed ASC provides **strong EHI export documentation**. The 416-entity CSV export with complete data dictionary, relationship schema, translation tables, and document reconstruction instructions represents one of the more thorough EHI export specifications encountered. The documentation is well-organized across five clear sections and appears to cover the full database schema.

The main limitation is the **proprietary CSV format** — while universally readable, it requires the data dictionary to interpret and does not use healthcare-standard formats like FHIR. However, for §170.315(b)(10) purposes, this is acceptable as the requirement is to export ALL electronic health information, not to use a specific standard format.

---

## Obstacles & Dead Ends

1. **Cloudflare Anti-Bot Protection:** The modmed.com site uses Cloudflare protection that blocks standard curl requests with 403 errors. Required browser automation for navigation and specific HTTP headers (Accept, User-Agent, Referer, Accept-Language) for direct PDF downloads.

2. **"SELECT A SESSION" Element:** A UI element on the certification page appeared to be an interactive dropdown but was actually a decorative Divi page builder element showing the number "7" (count of page sections). Investigated thoroughly before confirming it was non-functional.

3. **Version Discrepancy:** The ASC certification page links to an August 2025 version (6.4.4) of the data dictionary, while the gGastro certification page has a newer December 2025 version (6.5.3) plus a supplementary "Additional" document. The ASC page may not have been updated to reference the latest version. Both versions contain essentially the same ~416 entities.

---

## Access Summary

| Item | Value |
|------|-------|
| Registered URL | https://www.modmed.com/asc-onc-certification/ |
| Access Status | Found |
| EHI Export Docs Present | Yes |
| Primary Document | gGastro Patient Export Specifications (PDF, 168 pages) |
| Export Format | CSV files with data dictionary |
| Entity Count | ~416 CSV tables |
| Documentation Sections | CSV Files Dictionary, Data Schema, Translations, Patient Documents, Glossary |
| Supplementary Docs | Updated Dec 2025 version (167 pages) + Additional translations (551 pages) from gGastro certification page |
| Related: FHIR API Portal | https://portal.api.modmed.com/ (separate §170.315(g)(10) channel) |
