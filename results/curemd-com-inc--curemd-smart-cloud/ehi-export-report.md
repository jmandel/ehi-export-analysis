# CureMD.com, Inc. — EHI Export Documentation

Collected: 2026-02-15

## Source
- Registered URL: https://www.curemd.com/ehi-export.asp
- CHPL IDs: 11246
- Product: CureMD SMART Cloud (version 10g, certified 2023-03-02)

## Navigation Journal

**Step 1: Initial probe**
```bash
curl -sI -L "https://www.curemd.com/ehi-export.asp" -H 'User-Agent: Mozilla/5.0'
```
Returned HTTP 200 with Content-Type: text/html, 125,287 bytes. No redirects.

**Step 2: Fetch and examine the page**
```bash
curl -sL "https://www.curemd.com/ehi-export.asp" -H 'User-Agent: Mozilla/5.0' -o /tmp/curemd-ehi.html
```
The page has a straightforward layout: a hero banner titled "Electronic Health Information Export", then a section titled "170.315(b)(10) EHI Export" with a brief explanation and a single download link to the DRS data dictionary.

**Step 3: Search for documentation links**
```bash
grep -oiE 'href="[^"]*\.(pdf|zip|xlsx|xls|csv|json|doc|docx|yaml|yml)[^"]*"' /tmp/curemd-ehi.html
```
Found two downloadable files:
- `href="/PDF/CureMD.pdf"` — linked from the site navigation (marketing brochure)
- `href="EHI_Export_DRS.xlsx"` — the EHI export data dictionary (linked from the b(10) section)

**Step 4: Download XLSX data dictionary**
```bash
curl -sL "https://www.curemd.com/EHI_Export_DRS.xlsx" -H 'User-Agent: Mozilla/5.0' -o downloads/EHI_Export_DRS.xlsx
```
Verified: `file` reports "Microsoft Excel 2007+", 101,490 bytes.

**Step 5: Download CureMD PDF**
```bash
curl -sL "https://www.curemd.com/PDF/CureMD.pdf" -H 'User-Agent: Mozilla/5.0' -o downloads/CureMD.pdf
```
Verified: `file` reports "PDF document, version 1.6, 20 page(s)", 1,280,945 bytes.
Content: General marketing brochure covering EHR, billing, scheduling, specialties, etc. No EHI export–specific content. Included for completeness since it was on the page, but not an EHI export artifact.

**Step 6: Screenshot**
Navigated to the page in Chrome and captured a viewport screenshot. The page is a simple static HTML page — no SPA, no accordion, no login wall.

**Step 7: Checked all links on the page**
Scanned all `href` attributes. No additional EHI-related links beyond the XLSX. Other links go to CureMD product pages, blog, login, privacy policy, etc. — none EHI-export related.

## What Was Found

CureMD's EHI export documentation consists of a single dedicated page and one XLSX file:

### The Web Page (ehi-export.asp)
The page explicitly addresses 170.315(b)(10) with a brief but clear description:
- EHI export is available for single-patient or population-level export
- Single patient export can be initiated by system administrators without developer assistance
- Population export requires a request, with updates delivered via email
- Export format is **CSV files** for structured data, with documents and images exported in their **native formats**
- All exports delivered as ZIP files

### The Data Dictionary (EHI_Export_DRS.xlsx)
The XLSX has two sheets:

**"EHI Export" sheet**: Repeats the overview from the web page, with an explicit reference to the public URL.

**"DRS" (Designated Record Set) sheet**: A detailed data dictionary with **38 data classes** and **893 fields** (excluding empty trailing rows). Each field includes:
- Data class name (e.g., "Allergies", "Charges", "Patient Demographics")
- Field name (e.g., "Allergy Name", "RxNorm", "Severity")
- Data type (varchar, int, datetime, numeric, float, bit, text, nvarchar, date)
- Description (plain English explanation of each field)

The 38 data classes are:
1. Allergies (15 fields)
2. Appointments (20 fields)
3. Cases (18 fields)
4. Charges (82 fields)
5. Chemo Admin (15 fields)
6. Chemo Admin IVSites (6 fields)
7. Chemo Plan (22 fields)
8. Chemo Plan Diagnosis (7 fields)
9. Chemo Plan Drugs (28 fields)
10. Claims (16 fields)
11. Complaints (6 fields)
12. Diagnosis (18 fields)
13. Disclosures (11 fields)
14. Diseases History (21 fields)
15. Documents & Images (exported in native formats, per the description)
16. Electronic Remittance Advice (19 fields)
17. Family History (12 fields)
18. Hospitalization History (6 fields)
19. Immunizations (20 fields)
20. Medications (19 fields)
21. Memos (8 fields)
22. OBGYN History (52 fields)
23. Orders (24 fields)
24. Patient Consents (5 fields)
25. Patient Contacts (20 fields)
26. Patient Demographics (71 fields)
27. Patient Education (6 fields)
28. Patient Insurances (76 fields)
29. Patient Note (16 fields)
30. Payments (77 fields)
31. Provider Notes (exported as HTML files)
32. Referrals (23 fields)
33. Results (29 fields)
34. Risk (8 fields)
35. Social History (65 fields)
36. Surgery History (18 fields)
37. Vitals A (23 fields)
38. Vitals B (9 fields)

Two special classes — "Documents & Images" and "Provider Notes" — don't have tabular field definitions. Instead, the data dictionary notes that documents/images are exported in their native formats, and provider notes are exported as HTML files with a naming convention.

The SQL-style data types (varchar, int, datetime, numeric, etc.) indicate the CSV columns map closely to the underlying database schema. This is a genuine (b)(10) approach: exporting the database's designated record set as flat files rather than mapping to FHIR or another clinical standard.

## Export Coverage Assessment

### Data Domain Coverage

CureMD's export documentation covers a genuinely broad range of data domains. This is one of the more thorough (b)(10) implementations — the data dictionary goes well beyond US Core/USCDI:

**Well covered (with detailed field definitions):**
- **Demographics** (71 fields) — comprehensive patient information
- **Clinical data** — allergies, diagnoses, complaints, vital signs (split into Vitals A and Vitals B), immunizations, medications, results (labs), orders, disease history, family history, social history (65 fields — very detailed), surgery history, hospitalization history, OBGYN history (52 fields)
- **Billing/financial** — charges (82 fields), claims (16 fields), payments (77 fields), electronic remittance advice (19 fields), patient insurances (76 fields). This is notable: many vendors omit billing data entirely from EHI exports.
- **Specialty clinical data** — chemotherapy plans, chemo plan drugs, chemo plan diagnosis, chemo administration, chemo admin IV sites. This oncology-specific data is exactly the kind of specialty content that a proper (b)(10) export should include.
- **Care coordination** — referrals (23 fields), patient education, patient consents
- **Documents** — documents and images in native formats, provider notes as HTML
- **Patient communications** — memos, patient notes
- **Risk assessments** — risk data (8 fields)
- **Cases** — case management data (18 fields)

**Notably present (and often missing from other vendors):**
- Billing records (charges, claims, payments, ERA) — often the biggest gap in EHI exports
- Oncology/chemotherapy data — specialty-specific clinical data
- OBGYN history — specialty-specific
- Disclosures — information release tracking
- Patient insurances — enrollment/coverage data
- Appointments — scheduling data

**Potentially missing or unclear:**
- **Telehealth session records** — CureMD offers integrated telehealth, but no data class for video visit records appears in the export
- **Chronic Care Management (CCM) data** — CureMD has a CCM module with care plans, time tracking, and engagement tracking, but no explicit CCM data class in the export. Care plan elements may be captured under other classes.
- **Remote Patient Monitoring (RPM) data** — CureMD integrates with wearables (Apple Watch, Fitbit), but device readings don't have their own data class
- **Secure messages** — the patient portal supports secure messaging between patients and providers; no explicit "Messages" data class (though "Memos" and "Patient Note" may cover some of this)
- **Care plans/goals** — no explicit care plan data class, though clinical notes and provider notes may embed this
- **Growth charts / pediatric-specific data** — CureMD supports pediatrics but no pediatric-specific data class appears
- **Behavioral health assessments** — CureMD supports behavioral health with screening tools (GAD-7, PHQ-9), but these may be captured under Results or Provider Notes rather than having dedicated fields

These gaps are relatively minor compared to many vendors. The missing domains are mostly specialty-module data that may be stored within the broader clinical note or results classes rather than as separate entities. The core clinical and financial data coverage is strong.

### Export Format & Standards

- **Format**: CSV files for structured data; native formats for documents and images; HTML for provider notes
- **Delivery**: ZIP archive
- **Standard**: Not FHIR, not C-CDA — this is a flat-file database export. The data types (varchar, int, datetime, numeric, float, bit, text, nvarchar) are SQL Server column types, indicating a direct mapping from the underlying relational database.
- **Appropriateness**: For a (b)(10) export, CSV is a reasonable format. It's computable, universally readable, and can represent the full breadth of the database without the limitations of mapping to FHIR resource types. A third party could reconstruct the patient record from these CSVs, though understanding relationships between tables (e.g., linking charges to claims to ERA) would require understanding the shared key fields (Patient ID, Account Number, etc.).
- **Relationship handling**: No explicit foreign key documentation or relationship diagram is provided. However, many tables share common fields (Practice, Patient ID, Account Number, Date/Time) that serve as implicit join keys. A developer would need to infer relationships from field names and descriptions.

### Documentation Quality

- **Readability**: Good. The web page is clear and concise. The XLSX data dictionary is well-structured with consistent formatting.
- **Data dictionary granularity**: Each field has a name, SQL data type, and plain English description. This is better than many vendors who only list table names or field names without descriptions.
- **Value sets**: Not documented. Coded fields (e.g., "Status", "Severity", "Type") have descriptions but no enumeration of valid values. A developer importing this data would need to discover valid values from the data itself.
- **Sample data**: None provided. No example CSV files or sample records.
- **Worked examples**: None. No step-by-step walkthrough of performing an export or interpreting the output.
- **Developer implementability**: A developer could understand the data model from this documentation, but importing the data would require some inference about relationships, coded values, and edge cases. The documentation is a solid data dictionary, but not a complete integration specification.
- **Maintenance**: The XLSX is dated "November 2023" (per the "Last Updated" cell in the EHI Export sheet). The product was certified in March 2023, so this was updated ~8 months post-certification.

### Structure & Completeness

- **Field-level granularity**: Excellent — 893 fields across 38 data classes, each with data type and description
- **Coded field value sets**: Not documented
- **Relationships between entities**: Implicit (shared key fields) but not explicitly documented
- **Versioning**: "Last Updated: November 2023" noted on the overview sheet
- **Schema files**: None (no XSD, JSON Schema, DDL, or OpenAPI)

### (b)(10) vs (g)(10) Assessment

This is a **genuine (b)(10) implementation**, not a repackaged (g)(10) FHIR API. Key evidence:
1. The export format is CSV, not FHIR
2. The data dictionary includes billing data (charges, claims, payments, ERA) which is not part of US Core
3. Specialty clinical data (oncology/chemo) is included
4. The data dictionary maps closely to the underlying relational database, not to FHIR resource types
5. There is no mention of FHIR, Bulk Data, or US Core in the EHI export documentation
6. Insurance/enrollment data is included with 76 fields — well beyond USCDI scope

CureMD has done the work of defining their designated record set and documenting the database fields that make up the export. This is exactly what a (b)(10) implementation should look like.

## Access Summary
- Final URL (after redirects): https://www.curemd.com/ehi-export.asp
- Status: found
- Required browser: no (all content accessible via curl)
- Navigation complexity: direct_link (XLSX linked directly from the page)
- Anti-bot issues: none

## Obstacles & Dead Ends
None. The page loaded cleanly, the XLSX downloaded without issues, and no authentication was required. The documentation was straightforward to locate and download. The CureMD.pdf found on the page is a marketing brochure unrelated to EHI export — included for completeness but not an EHI artifact.
