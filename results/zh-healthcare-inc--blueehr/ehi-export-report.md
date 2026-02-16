# ZH Healthcare, Inc. — EHI Export Documentation

Collected: 2026-02-16

## Source
- Registered URL: https://blueehr.com/certifications-and-costs/
- CHPL IDs: 10797
- Product: BlueEHR Version 3
- Certification Date: 2022-01-19

## Navigation Journal

### Step 1: Probed the registered URL
```bash
curl -sI -L "https://blueehr.com/certifications-and-costs/" -H 'User-Agent: Mozilla/5.0'
```
Returned HTTP 200, `text/html`, 80,552 bytes. No redirects. Page is a static WordPress page served from Apache on CentOS.

### Step 2: Fetched and searched the page for documentation links
```bash
curl -sL "https://blueehr.com/certifications-and-costs/" -H 'User-Agent: Mozilla/5.0' -o /tmp/page.html
grep -oiE 'href="[^"]*\.(pdf|zip|xlsx|xls|csv|json|doc|docx|yaml|yml)[^"]*"' /tmp/page.html
```
Found 12 file links. The relevant EHI export link:
- `https://blueehr.com/wp-content/uploads/2023/09/EHI_Export.pdf`

Other links on the page (not EHI-specific):
- API Documentation PDF (general REST APIs, dated 2020)
- FHIR Documentation page (g)(10) standardized API docs
- FHIR URLs JSON (essentially empty FHIR Bundle, 99 bytes)
- API Reference developer portal (general BlueEHR APIs)
- Multi-factor authentication PDF
- Multiple Real World Testing plans and results (2022–2025)

### Step 3: Downloaded the EHI Export PDF
```bash
curl -sL "https://blueehr.com/wp-content/uploads/2023/09/EHI_Export.pdf" -H 'User-Agent: Mozilla/5.0' -o downloads/EHI_Export.pdf
```
Verified: `file` reports "PDF document, version 1.7, 2 page(s)", 194,524 bytes.

### Step 4: Examined the PDF
```bash
pdfinfo downloads/EHI_Export.pdf
pdftotext downloads/EHI_Export.pdf -
```
- Author: Munawar Peringadi Vayalil
- Created: 2023-09-15 (Microsoft Word)
- 2 pages: a title/cover page and one content page
- No embedded files, no embedded URLs

### Step 5: Checked related documentation pages

**FHIR Documentation** (`https://blueehr.com/fhir-documentation/`): This is the (g)(10) standardized FHIR R4 API documentation. It describes a read-only RESTful HL7 FHIR R4 API conforming to US Core STU3.1.1, with SMART on FHIR authorization and Bulk Data Access support. This is the standardized API for patient and population services — not the EHI export mechanism. Not relevant to (b)(10).

**API Reference** (`https://developer.blueehr.com/api-reference/`): General BlueEHR developer portal with REST APIs for various data categories (Data Pull, Billing, Lab, Encounter, Demographics, Immunization, etc.). These are the product's general APIs, not specifically the EHI export. The EHI Export PDF does not reference these APIs.

**FHIR URLs JSON** (`https://appstudio.interopengine.com/partner/fhirR4endpoints-zh.json`): A 99-byte FHIR Bundle with no entries — essentially empty.

**API Documentation PDF** (`https://developer.blueehr.com/wp-content/uploads/2020/04/blueEHR-APIs.pdf`): General API documentation from 2020, predates the EHI export certification. Not referenced by the EHI export documentation.

### Step 6: Searched the Knowledge Base
Navigated to `https://docs.blueehr.com/` (Document360-based KB). Searched for "export" — returned 0 articles, 2 category matches that only mention "Care Coordination Export and import patient details from one EHR application to another" in passing. No dedicated EHI export documentation in the knowledge base.

### Step 7: Screenshot
Took a screenshot of the certifications page showing the documentation links section, including the "Electronic Health Information Export" link.

## What Was Found

The entire EHI export documentation for BlueEHR consists of a **single 2-page PDF** (`EHI_Export.pdf`). The first page is a title/cover page with the blueEHR logo, product name, and heading "Electronic Health Information Export — blueEHR 3". The second page contains the actual documentation.

The document describes three export mechanisms:

### 1. Patient's Clinical Data via C-CDA Format
Users can export clinical data for one or multiple patients using the **Care Coordination** feature. A screenshot shows an interface with checkboxes for selecting data categories to include in the export. The visible checkbox options in the screenshot include:
- Check All – Components
- Medications, Problems, Procedures, Plan of Care, Social History, Functional Status, Deformities (left column)
- Medications, Results, Vitals, Documents, Encounter, Reason for Referral, Diagnostic Findings, Health Concerns (right column)

The export produces C-CDA (Consolidated Clinical Data Architecture) documents.

### 2. Demographics, Lab, and Payment Data
Users can export via the **Analytics** feature in BlueEHR:
- Single or multiple patients' demographic details
- Insurance details
- Payments
- Lab results
- Encounters
- Appointment details

This data is exported as **CSV or XLS** format. A screenshot shows the BlueEHR main menu with "Analytics" circled in red.

### 3. Documents
Any documents attached to patients' records can be exported via the **document module**. No additional details are provided about the format or process.

## Export Coverage Assessment

### Data Domain Coverage

Based on the product research, BlueEHR is a comprehensive multi-specialty EHR with 30–34 modules covering clinical care, billing, scheduling, telehealth, and more. The EHI export documentation describes coverage of only a narrow subset of the product's data:

**Clearly covered (via C-CDA):**
- Medications
- Problems/diagnoses
- Procedures
- Vital signs
- Lab results (also via CSV)
- Allergies (implied by "Plan of Care" and clinical components)
- Social history
- Functional status
- Encounters
- Documents
- Care plan/Plan of care
- Referrals (Reason for Referral)
- Health concerns

**Partially covered (via CSV/XLS Analytics export):**
- Demographics
- Insurance details
- Payment data
- Lab results
- Encounter data
- Appointment details

**Likely missing or undocumented:**
- **Billing/claims data** — The PDF mentions "Payments" but not the full billing/claims lifecycle (claims, charges, CPT/ICD codes, denial management, payment posting, claims adjudication). BlueEHR has a dedicated billing/RCM module.
- **E-prescribing history** — Prescription transmission records, pharmacy responses
- **Immunization records** — Not listed in either export mechanism (despite being a core module)
- **Clinical decision support alerts/records**
- **Family health history** — Certified under (a)(12) but not mentioned in export
- **Implantable device list** — Certified under (a)(14) but not mentioned in export
- **Custom forms/templates** — BlueEHR's form builder creates custom clinical forms; no mention of exporting this data
- **Telehealth records** — blueTeleMed session data
- **Secure messages** — Patient-provider messaging through patient portal
- **Patient-generated data** — Self-reported health history, family history from patient portal
- **Radiology/imaging data** — Despite having a radiology module and PACS integration
- **Pharmacy/inventory data**
- **ADT records** — Admission, discharge, transfer data for acute care
- **Clinical notes** — Progress notes, H&P, discharge summaries are not explicitly listed (though "Documents" may include these)
- **Orders** — CPOE data for medications, labs, imaging

The C-CDA export covers the standard USCDI clinical summary categories, while the CSV/Analytics export adds demographics, insurance, payments, and some operational data. However, this still looks like a **narrow clinical summary + some administrative data**, not a comprehensive "all electronic health information" export.

### Export Format & Standards

The export uses two formats:
1. **C-CDA** (Consolidated Clinical Data Architecture) — A recognized healthcare standard for clinical document exchange. Appropriate for clinical summaries but inherently limited in scope — C-CDA is designed for transitions of care, not comprehensive data export.
2. **CSV/XLS** — Tabular format via the Analytics feature. Simple and accessible but no documentation of field definitions, data types, or relationships.

No data dictionary is provided for either format. No schema files. No sample exports. No field-level documentation.

The use of C-CDA for clinical data is a significant design choice: C-CDA is the same format used for (b)(1) Transitions of Care. This strongly suggests the EHI export is reusing the existing C-CDA generation capability rather than building a dedicated comprehensive export. C-CDA has inherent limitations for capturing all EHR data — it's designed for clinical summaries, not full database exports.

### Documentation Quality

The documentation is **extremely minimal**:
- **2 pages total** (one is a cover page)
- **No data dictionary** — not even a list of exported fields
- **No schema or format specification** — for neither C-CDA profiles nor CSV column definitions
- **No sample exports or examples**
- **No step-by-step instructions** — just brief descriptions of three mechanisms
- **No API documentation** specific to the export
- **Two low-resolution screenshots** — one showing the Care Coordination export interface, one showing the main menu with Analytics circled

A developer could not implement an import of this data based on this documentation. A user would struggle to perform the export without additional training. The documentation reads as a compliance checkbox, not a genuine technical reference.

### Structure & Completeness

- **Granularity**: Category-level only (e.g., "Medications", "Payments"). No field-level documentation whatsoever.
- **Value sets**: Not documented
- **Relationships between entities**: Not documented
- **Data types**: Not documented
- **Versioning/change history**: None. PDF created September 2023.

### (b)(10) vs (g)(10) Assessment

This is **not** a case of conflating (b)(10) with (g)(10) — the vendor does not point to their FHIR API as the EHI export. The FHIR documentation and EHI Export PDF are separate documents linked separately on the certifications page. The EHI export uses C-CDA and CSV/XLS, not FHIR.

However, the export appears to suffer from a related problem: the C-CDA export is likely the same as the (b)(1) Transitions of Care export, which only covers standard clinical summary data (USCDI-equivalent). Combined with a CSV analytics export for demographics/payments/labs, this still falls well short of "all electronic health information." The product stores billing records, custom forms, telehealth data, orders, clinical notes, immunizations, and specialty-specific data that are not accounted for in this documentation.

## Access Summary
- Final URL (after redirects): https://blueehr.com/certifications-and-costs/
- Status: found
- Required browser: no (static HTML page, PDF is directly linked)
- Navigation complexity: one_click (single link on the certifications page)
- Anti-bot issues: none

## Obstacles & Dead Ends
- The FHIR URLs JSON file (`fhirR4endpoints-zh.json`) was essentially empty (99 bytes, a Bundle with no entries).
- The Knowledge Base (`docs.blueehr.com`) had no EHI export documentation.
- The developer portal (`developer.blueehr.com`) has general API docs but nothing specific to EHI export.
- No additional documentation, data dictionaries, or schema files were found anywhere on the vendor's properties.
