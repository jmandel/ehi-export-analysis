# Infinx Solutions, LLC — EHI Export Documentation

Collected: 2026-02-16

## Source
- Registered URL: https://www.i3verticals.com/ehr-certification/
- CHPL IDs: 11759 (v5.4, certified 2026-01-28), 11554 (v5.3, certified 2024-12-19)
- Developer: Infinx Solutions, LLC
- Product: Infinx EHR (formerly iMedEMR / i3Med)

## Navigation Journal

1. **Probed the registered URL** (`https://www.i3verticals.com/ehr-certification/`):
   ```bash
   curl -sI -L "https://www.i3verticals.com/ehr-certification/" -H 'User-Agent: Mozilla/5.0'
   ```
   Result: **HTTP 404**. The page no longer exists on i3verticals.com.

2. **Checked the domain root** (`https://www.i3verticals.com/`): Returns 200, but the site is now a general fintech/payments company page. No EHR certification content found via link analysis.

3. **Investigated Infinx.com** (the acquiring company): The CHPL metadata lists Infinx Solutions, LLC as the developer (post-acquisition from i3 Verticals in May 2025). Searched the Infinx home page for EHR/certification links.

4. **Probed common paths on infinx.com**:
   ```bash
   for path in /ehr-certification/ /ehi-export/ /ehi/ /onc-certification/ /certification/ /disclosures/ /mandatory-disclosures/; do
     curl -sI "https://www.infinx.com${path}" -o /dev/null -w '%{http_code}'
   done
   ```
   Result: **`/ehr-certification/` returned HTTP 200**. All other paths returned 404.

5. **Fetched and examined** `https://www.infinx.com/ehr-certification/`:
   ```bash
   curl -sL "https://www.infinx.com/ehr-certification/" -H 'User-Agent: Mozilla/5.0' -o page.html
   ```
   This is a WordPress-based certification page titled "Infinx EHR Certification 5.4". It contains certification details and an "Other Information" section with document links.

6. **Identified the EHI export document** from the page's link analysis:
   ```bash
   grep -oiE 'href="[^"]*\.(pdf|zip|xlsx|csv|json|doc)[^"]*"' page.html
   ```
   Found: `IMED-Electronic-Health-Information-EHI-Export-Documentation-191223-221553-1.pdf`

7. **Downloaded the EHI Export Documentation PDF**:
   ```bash
   curl -sL "https://www.infinx.com/wp-content/uploads/2025/09/IMED-Electronic-Health-Information-EHI-Export-Documentation-191223-221553-1.pdf" -o IMED-EHI-Export-Documentation.pdf
   ```
   Verified: `file` confirms PDF document, 13 pages, 92 KB.

8. **Also captured**: full-page screenshot of the certification page, the certification page HTML, and rendered the PDF's first page to confirm readability.

## What Was Found

The certification page at `https://www.infinx.com/ehr-certification/` is a standard ONC certification disclosures page for Infinx EHR 5.4. Under "Other Information" it links to a single PDF document for b(10) EHI export:

**"Electronic Health Information Export Documentation (b10)"** — a 13-page PDF (filename retains the "IMED" branding from the product's iMedEMR origins).

### Export Format

The export is delivered as a **.zip file** containing a folder with three types of files:

1. **CSV files** — one per patient data table (15 tables documented). Each has a header row with field names followed by comma-separated data.

2. **XML files** — a main `ccda.xml` containing all C-CDA-compatible clinical data, plus additional `ccda_[id].xml` files for referrals (cross-referenced via the `patient_referrals` CSV's `ccda_id` field).

3. **PDF files** with specific prefixes:
   - `SoapDoc_` — visit/encounter SOAP notes
   - `document_` — scanned/uploaded chart documents
   - `Labs_` — lab results
   - `formletter_` — clinic-generated letters
   - `OB_` — pregnancy-related visit data

### Data Dictionary

The documentation defines **15 patient data tables** with **248 total fields**:

| Table | Description | Fields |
|-------|-------------|--------|
| patientinfo | Demographics, identifiers, social/medical history | 46 |
| charges | CPT charges, billing data | 21 |
| healthmaintenance | Scheduled recurrent diagnostic tests | 10 |
| ob | Pregnancy-related visits | 8 |
| patient_advforms | Online patient forms with responses | 11 |
| patient_codes | Codes from various code systems | 14 |
| patient_forms_data | Provider-side forms with responses | 6 |
| patient_guarantor | Guarantor demographics and billing info | 22 |
| patient_letters | Clinic-generated letters | 8 |
| patient_pmp | Prescription monitoring program results | 10 |
| patient_referrals | Provider referrals with C-CDA cross-references | 12 |
| ptinr | PT/INR anticoagulation tracking plans | 8 |
| ptinr_log | PT/INR test result logs | 15 |
| schedules | Appointment data with billing fields | 42 |
| surgerymemo | Surgical documentation (custom/optional) | 8 |

Most tables include a Schema column documenting data types (32-digit GUIDs, dates as Y-m-d, timestamps, integers, text, JSON arrays). Some simpler tables (patientinfo, ob, patient_letters, patient_referrals) only have Field Name and Description columns.

### Export Instructions

- **Single patient**: Available through the user guide (not provided publicly).
- **Bulk/multi-patient**: Requires contacting support via a support ticket.

## Export Coverage Assessment

### Data Domain Coverage

**Clearly covered in the export:**
- **Patient demographics** — Extensive coverage via `patientinfo` (46 fields including name, DOB, SSN, address, phone, email, gender identity, sexual orientation, birth sex, ethnicity, language, employer info, financial class, injury/accident details)
- **Billing/charges** — `charges` table covers CPT codes, fees, units, batch numbers, export status, billing descriptions. `patient_guarantor` covers guarantor demographics for billing.
- **Appointments/schedules** — `schedules` table with 42 fields including date, time, provider, location, copay, balance, payment types, visit numbers, virtual visit info
- **Health maintenance** — Preventive care tracking via `healthmaintenance`
- **Patient forms** — Two tables (`patient_advforms` for patient-facing online forms, `patient_forms_data` for provider-side forms), both storing responses as JSON arrays
- **Clinical codes** — `patient_codes` is a generic code storage table linking codes to patients and schedules, with type/value/description fields
- **Referrals** — `patient_referrals` with associated C-CDA documents
- **Letters/correspondence** — `patient_letters` with associated PDF files
- **Prescription monitoring** — `patient_pmp` with drug scoring categories
- **Surgical documentation** — `surgerymemo` (noted as custom/optional)
- **OB/pregnancy data** — `ob` table with associated PDFs
- **Anticoagulation tracking** — Specialized `ptinr` and `ptinr_log` tables
- **Clinical notes** — Exported as `SoapDoc_` PDFs (visit SOAP notes)
- **Lab results** — Exported as `Labs_` PDF files
- **Scanned documents** — Exported as `document_` PDFs
- **C-CDA clinical summary** — The main `ccda.xml` covers standard clinical data (problems, medications, allergies, immunizations, etc.)

**Domains that appear missing or underdocumented:**
- **Medication lists / prescriptions** — No dedicated CSV table for active medications, prescription history, or e-prescribing records. Medications may be captured in the C-CDA XML or within `patient_codes`, but there's no explicit medication table. Given the product's DrFirst e-prescribing integration, this is a notable gap.
- **Allergy lists** — Similarly no dedicated allergy table. Likely in C-CDA only.
- **Problem lists / diagnoses** — No dedicated diagnosis table. The generic `patient_codes` table may hold ICD codes, but this isn't explicitly documented. Diagnoses associated with visits likely appear in SOAP PDFs and C-CDA.
- **Vital signs** — No dedicated vitals table. Likely in C-CDA or SOAP note PDFs.
- **Immunizations** — No dedicated table; likely in C-CDA.
- **Insurance/enrollment information** — No insurance coverage table documenting payer details, policy numbers, coverage dates. `financial_class` in patientinfo is a single field. The `patient_guarantor` table covers the guarantor but not insurance plans themselves.
- **Implantable device list** — Certified for (a)(14) but no export table mentioned.
- **Family health history** — Certified for (a)(12) but no export table mentioned.
- **Care plans / goals** — No dedicated table.
- **Clinical decision support alerts** — Not exported.
- **Patient portal messages** — No dedicated table for secure messages.
- **Imaging orders** — Certified for CPOE diagnostic imaging but no dedicated table.

**Ambiguous coverage:**
- The `patient_codes` table is a generic code container — it could hold diagnoses, allergies, medications, or other coded data, but the documentation doesn't specify which code systems or types are stored. The `type` field presumably differentiates them, but no value set is documented.
- SOAP note PDFs (`SoapDoc_`) likely contain rich clinical data (vitals, assessments, plans) but in unstructured PDF form, not as queryable structured data.

### Export Format & Standards

The export uses a **hybrid approach**:
- **CSV files** for structured patient data tables — a vendor-proprietary schema, not a recognized standard
- **C-CDA XML** for clinical data that maps to the C-CDA standard
- **PDF files** for clinical notes, lab results, scanned documents, and other unstructured content

This is a reasonable and honest approach to b(10) — it doesn't pretend FHIR or C-CDA covers everything. The CSV tables export data that genuinely doesn't fit neatly into C-CDA (billing charges, guarantor info, PMP scores, custom forms). The C-CDA captures standardized clinical data.

**Strengths:**
- The export clearly goes beyond USCDI/US Core — billing data, guarantor demographics, PMP scores, custom forms with JSON responses, surgical memos, anticoagulation tracking
- Relationships between tables use consistent 32-digit GUIDs (patientid, scheduleid)
- C-CDA referral documents are cross-referenced to the `patient_referrals` CSV via `ccda_id`

**Weaknesses:**
- No formal schema file (no XSD, JSON Schema, or DDL). The PDF data dictionary is the only specification.
- CSV relationships are implicit via shared GUIDs — no foreign key documentation
- No sample export files provided

### Documentation Quality

**Readability:** The PDF is well-organized with a clear structure: overview → file types → table index → table-by-table field definitions. Each table has a summary description followed by field-level details.

**Field-level detail:** 11 of 15 tables include data types (Schema column). The `schedules` table notably lists ~35 fields without any descriptions — just bare field names. The `patientinfo` table has descriptions but no data types.

**Value sets:** A few coded fields document their values (e.g., `chrGender`: 1=male, 2=female; `status`: 0=active, 1=inactive; `caseType`: New/Pending/Processed). Most coded fields lack value set documentation.

**Missing:**
- No worked examples or sample export files
- No user guide for performing the export (referenced but not provided publicly)
- No versioning or change history
- No documentation of relationships between tables beyond the ccda_id cross-reference
- The `patient_codes` table's `type` field is the key to understanding what clinical data is exported as structured codes, but its possible values are not documented

A developer could import this data based on the documentation, but would need significant trial-and-error to understand the `patient_codes` and `patient_forms_data` tables fully.

### Structure & Completeness

The documentation provides table-level and field-level granularity, which is better than many vendors. The data dictionary covers 248 fields across 15 tables — not a trivial export. However:

- **Granularity is uneven**: `charges` has full field/description/schema documentation; `schedules` has 35 undocumented fields; `patientinfo` has no data types.
- **No relationship documentation**: Tables share GUIDs (patientid, scheduleid) but no ER diagram or foreign key mapping.
- **No value set catalog**: Coded fields like `patient_codes.type`, `patient_codes.code`, `patient_advforms.status` have minimal value documentation.
- **No versioning**: The filename suggests creation date of 2023-12-19. No indication of updates since then despite the product version advancing from 5.1 to 5.4.

### Overall Assessment

This is a **genuine b(10) effort** — the vendor has created a real EHI export that goes beyond just C-CDA/USCDI. The export includes billing data, custom forms, guarantor information, prescription monitoring scores, and other data that wouldn't appear in a FHIR or C-CDA-only export. The hybrid CSV + C-CDA + PDF approach is practical and honest.

However, the export has **meaningful gaps in clinical structured data**. Core clinical domains like medications, allergies, diagnoses, vitals, and immunizations appear to rely on C-CDA XML and/or SOAP note PDFs rather than being exported as structured CSV tables. The generic `patient_codes` table may contain some of this data, but it's underdocumented.

The documentation quality is **adequate but not exemplary**. The data dictionary covers most tables at field level, but the inconsistent depth (some tables fully documented, others with bare field names), missing value sets, and lack of relationship documentation or sample data mean a receiving system would need considerable work to correctly import this data.

The product's acquisition history (iMed → i3 Verticals → Infinx) is reflected in the documentation: the PDF still carries "IMED" branding, the CHPL-registered URL points to i3verticals.com (which 404s), and the actual documentation lives at infinx.com/ehr-certification/. The documentation appears to have been written during the iMed era and hasn't been updated for the Infinx rebrand.

## Access Summary
- Registered URL: https://www.i3verticals.com/ehr-certification/ (404 — dead)
- Final URL (after investigation): https://www.infinx.com/ehr-certification/
- EHI doc direct URL: https://www.infinx.com/wp-content/uploads/2025/09/IMED-Electronic-Health-Information-EHI-Export-Documentation-191223-221553-1.pdf
- Status: found (at different domain than registered)
- Required browser: no (curl works fine)
- Navigation complexity: one_click (from certification page to PDF download)
- Anti-bot issues: none

## Obstacles & Dead Ends
- The CHPL-registered URL (`https://www.i3verticals.com/ehr-certification/`) returns 404. This is because Infinx Solutions acquired i3 Verticals' healthcare business in May 2025 and the EHR certification page was moved to `infinx.com`.
- The `i3verticalshealthcare.com` domain returns 403 Forbidden.
- The Wayback Machine CDX API returned no results for the i3verticals.com/ehr-certification/ path.
- The infinx.com home page makes no mention of the EHR product; you have to know the `/ehr-certification/` path or find it via the `/security-compliance-trust-center/` page links.
- The CHPL listing should be updated to point to `https://www.infinx.com/ehr-certification/` instead of the dead i3verticals URL.
