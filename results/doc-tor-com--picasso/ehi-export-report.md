# Doc-tor.com — EHI Export Documentation

Collected: 2026-02-15

## Source
- Registered URL: https://doc-tor.com/wp-content/uploads/2023/11/Picasso-EHI-Export-Documentation-V1_0-1-1.pdf
- CHPL IDs: 11652
- Product: Picasso v8.2
- Developer: Doc-tor.com (now owned by Harris Healthcare / Constellation Software)

## Navigation Journal

### Step 1: Probe the registered URL
```bash
curl -sI -L "https://doc-tor.com/wp-content/uploads/2023/11/Picasso-EHI-Export-Documentation-V1_0-1-1.pdf" \
  -H 'User-Agent: Mozilla/5.0'
```
Result: HTTP 200, Content-Type: application/pdf, 195,305 bytes. Direct download, no redirects.

### Step 2: Download the registered PDF
```bash
curl -sL "https://doc-tor.com/wp-content/uploads/2023/11/Picasso-EHI-Export-Documentation-V1_0-1-1.pdf" \
  -H 'User-Agent: Mozilla/5.0' -o Picasso-EHI-Export-Documentation-V1_0-1-1.pdf
```
Confirmed: PDF document, 8 pages, created 2023-10-16 by Kathiresan Palanisamy via Microsoft Word.

**Critical finding**: Despite the filename containing "Picasso," the document title is **"Amazing Charts EHI Export: Folder Organization and Data Format Specification – v1.0"**. This is the Amazing Charts sister product's data dictionary, not Picasso's own.

### Step 3: Check the mandatory disclosures page for additional documentation
```bash
curl -sL "https://doc-tor.com/certified-healthcare-technology-cehrt-price-transparency/" \
  -H 'User-Agent: Mozilla/5.0' -o /tmp/doc-tor-disclosures.html
grep -oiE 'href="[^"]*\.(pdf|zip|xlsx|xls|csv|json|doc|docx|yaml|yml)[^"]*"' /tmp/doc-tor-disclosures.html
```
Found two additional PDFs:
1. `http://doc-tor.com/wp-content/uploads/2024/01/Picasso-EHI-Export-Documentation-V1_0-1.pdf` — a **Picasso-specific** EHI export document (different from the registered URL)
2. `http://live.picassoemr.com/_PicassoAPI/PAA_API_documentation.pdf` — Picasso Application Access API documentation

### Step 4: Download the Picasso-specific EHI export document
```bash
curl -sL "https://doc-tor.com/wp-content/uploads/2024/01/Picasso-EHI-Export-Documentation-V1_0-1.pdf" \
  -H 'User-Agent: Mozilla/5.0' -o Picasso-EHI-Export-Documentation-V1_0-1.pdf
```
Confirmed: PDF document, 3 pages, created 2024-01-04 by Kathiresan Palanisamy. Title: **"Picasso EHI Export: Folder Organization and Data Format Specification – v1.0"**. This is the actual Picasso data dictionary with Picasso-specific column names and CSV-only format.

### Step 5: Download the API documentation
```bash
curl -sL "http://live.picassoemr.com/_PicassoAPI/PAA_API_documentation.pdf" \
  -H 'User-Agent: Mozilla/5.0' -o PAA_API_documentation.pdf
```
Confirmed: PDF document, 4 pages, created 2023-01-10. Documents a SOAP/REST API (`ApplicationAccess.asmx`) that returns USCDI-compliant CCDs in XML format. This is a (g)(10)-style API, not the (b)(10) export mechanism.

### Step 6: Verify no embedded URLs or attachments in PDFs
```bash
pdftotext Picasso-EHI-Export-Documentation-V1_0-1-1.pdf - | grep -oiE 'https?://[^[:space:]>)"]+' | sort -u
pdfdetach -list Picasso-EHI-Export-Documentation-V1_0-1-1.pdf
```
No embedded URLs or file attachments found in any of the three PDFs.

## What Was Found

Three PDF documents were collected, two of which are EHI export data dictionaries and one is a clinical API specification.

### Document 1: Amazing Charts EHI Export (Registered URL — V1_0-1-1)
- **8 pages**, 195 KB
- Titled "Amazing Charts EHI Export" despite being hosted under a Picasso filename
- Describes an export that creates per-patient folders with timestamped names
- Supports three export formats: CSV, JSON, and XML
- Contains a "Documents" subfolder for imported items, images, and related documents in original format
- **44 data classes** with column-level detail (column names only, no data types or descriptions)
- Supports single-patient and population-based export (by Provider, All Active, All Patients, or Encounter Range)
- Data classes include: Addendum, Advance Directives, Alerts, Allergies (active + pending), Assessments, **Billing History** (74 columns — very detailed with CPT, ICD, fees, charges, modifiers, NDC codes), Care Team Members, Clinical Notes (88 columns — full SOAP note structure with vitals, tobacco, pregnancy, vision, hearing), Demographic Immunization, Email, Family History, Functional Status, Goals, Health Concerns, Health Insurance, HM Rules Ignored, HM Rules/Immunizations, Immunizations, Implantable Device, Imported Items, Injections, Lab Tests (119 columns — extremely detailed with order, result, and note substructures), List Problem (active + pending), Medications (active + pending), Next Of Kin, Occupation and Industry History, Orders, Patient Demographics (62 columns), Patient Generated Data, Patient Health Information Capture, Patient Record Release, Plan of Treatment, Procedures, Referrals, Risk Factors, Scheduling, Smoking Statuses, Tracked Data, Travel History, User Defined Fields, Vital Signs
- Total columns across all data classes: ~1,094

### Document 2: Picasso EHI Export (V1_0-1 — found on disclosures page)
- **3 pages**, 154 KB
- Titled "Picasso EHI Export" — this is Picasso-specific
- CSV-only export format
- Creates per-patient folders identified by Picasso patient ID within a timestamped "ScheduledExport" folder
- Includes an "Attachments" subfolder for documents and other data
- **21 data classes** with column-level detail (column names only, no data types or descriptions)
- Data classes: Allergies, Assessment, Care Team, Clinical Notes, Demographics, Encounters, Family History, Health Concerns, Health Insurance, Immunizations, Implantable Devices, Labs, Medications, Orders, Plan Of Treatment, Problems, Procedures, Social History, Tasks, Tobacco, Vitals
- Total columns across all data classes: ~441
- Column names use ALL_CAPS convention (e.g., PROV_LAST, AMADIAGNOSISID) consistent with Picasso's database schema — different from the Amazing Charts document's PascalCase naming

### Document 3: Picasso Application Access API (PAA)
- **4 pages**, 175 KB
- Documents a SOAP-style web service at `https://live.picassoemr.com/NIST/EMRLDWebService/ApplicationAccess.asmx`
- Methods: GetAuthorizationToken, GetPatientId, GetPatientData (returns USCDI-compliant CCD XML), GetPatientCategoriesData (deprecated)
- Appendix A lists USCDI v1 Data Classes — this is clearly a (g)(10) API, not the (b)(10) bulk export
- Not relevant to EHI export assessment, but included for completeness

## Export Coverage Assessment

### Data Domain Coverage

**Comparing the Picasso-specific document (21 data classes) against product research:**

| Data Domain | Picasso Export | Notes |
|---|---|---|
| Demographics | Yes | 51 columns including race, ethnicity, language, sex orientation, gender identity |
| Allergies | Yes | 19 columns with RxNorm codes and severity |
| Problems/Diagnoses | Yes | Via "Problems" and "Assessment" classes with ICD/SNOMED codes |
| Medications | Yes | 27 columns including dosage, frequency, prescribing provider |
| Lab Results | Yes | 24 columns with LOINC codes, reference ranges, abnormal flags |
| Vital Signs | Yes | 17 columns including O2 saturation, head circumference |
| Immunizations | Yes | 27 columns with CVX codes, lot numbers, consent info |
| Clinical Notes | Yes | 15 columns — but notably simpler than Amazing Charts (just NOTETEXT + metadata vs. full SOAP structure) |
| Encounters | Yes | 28 columns with facility info, E/M codes, diagnoses |
| Care Team | Yes | 12 columns |
| Family History | Yes | 7 columns with SNOMED codes |
| Social History | Yes | 4 columns (sparse — just category/value pairs) |
| Health Concerns | Yes | 13 columns |
| Plan of Treatment | Yes | 26 columns with referral provider details |
| Procedures | Yes | 15 columns with CPT codes and modifiers |
| Implantable Devices | Yes | 22 columns with UDI details |
| Orders | Yes | 18 columns |
| Health Insurance | Yes | 51 columns — detailed payer, subscriber, and guarantor info |
| Tasks | Yes | 22 columns (clinical task/queue management) |
| Tobacco/Smoking | Yes | 4 columns |
| **Billing History** | **NO** | **Absent from Picasso-specific doc — present in Amazing Charts doc with 74 columns** |
| **Patient Portal Messages** | **NO** | Not in either document |
| **Documents/Attachments** | Partial | Referenced as "Attachments" subfolder preserving original format, but no data dictionary for metadata |
| **E-Prescribing Details** | **NO** | No Rx transaction data (SureScripts status, pharmacy transmit, etc.) — present in Amazing Charts doc |
| **Referrals** | **NO** | Present in Amazing Charts doc but absent from Picasso-specific doc |
| **Scheduling/Appointments** | **NO** | Present in Amazing Charts doc but absent from Picasso-specific doc |
| **Patient Generated Data** | **NO** | Present in Amazing Charts doc but absent from Picasso-specific doc |

**The most significant gap is billing data.** Picasso is an integrated EHR + Practice Management + RCM suite that processes claims, payments, charges, and denial management. The product research highlights billing as a core capability. Yet the Picasso-specific EHI export document contains no billing data class at all. The Amazing Charts document (incorrectly linked as the registered URL) does include a comprehensive "Billing History" class with 74 columns covering CPT codes, ICD codes, fees, charges, NDC codes, modifiers, facility info, and referring provider info. It's unclear whether Picasso's actual export includes billing data using the Amazing Charts schema, or whether billing data is truly absent.

### The Two-Document Problem

This vendor has a confusing documentation situation:

1. The **registered URL** points to an **Amazing Charts** data dictionary (44 data classes, ~1,094 columns, CSV/JSON/XML). This is a different product — Amazing Charts is a sister product under the Harris Healthcare umbrella. The data class names, column names, and column counts are all different from Picasso.

2. A **Picasso-specific** data dictionary exists (21 data classes, ~441 columns, CSV only) but was found only on the mandatory disclosures page, not at the registered URL. It has different column naming conventions (ALL_CAPS vs PascalCase) and a significantly narrower scope.

The relationship between these two documents is unclear. It could be:
- Picasso's export was built from Amazing Charts' codebase and the Amazing Charts document is the more complete/accurate one
- They are genuinely different exports for different products and the registered URL is simply wrong
- The Picasso-specific document is a newer, reduced version that replaced the broader Amazing Charts export

### Export Format & Standards
- The Picasso export uses **CSV files** — one per data class per patient, organized in a folder structure
- The Amazing Charts export additionally supports JSON and XML
- No FHIR, C-CDA, or other healthcare standard is used for the bulk export (the separate API returns CCDs, but that's a different mechanism)
- CSV is an appropriate format for a database-level export. Relationships between entities are implicit via shared IDs (PatientID, VisitID, ProviderID)
- No formal schema definition (no JSON Schema, XSD, or DDL) — just column names in a PDF

### Documentation Quality
- **Readability**: The documents are clear but minimal — a simple two-column table mapping data class names to column names
- **No field descriptions**: Only column names are provided. No data types, constraints, value sets, or cardinality information
- **No examples**: No sample export files, sample records, or worked examples
- **No export instructions**: Neither document explains how to trigger the export (which menu, which role has access, what parameters to set)
- **No relationship documentation**: No explanation of how entities relate (e.g., how VISITID in Clinical Notes links to VISITID in Encounters)
- **No value set documentation**: Coded fields like CODINGLANGUAGE, SEVERITYCODE, TYPE are listed but their allowed values are not defined
- **Developer implementability**: A developer receiving this export would have column names but would need to reverse-engineer data types, relationships, and coded values from the actual exported data. Import implementation would be possible but require significant trial and error.

### Structure & Completeness
- **Granularity**: Field-level (column names), but no data types or descriptions
- **Coded fields**: Not documented with value sets
- **Relationships**: Not documented — must be inferred from shared column names (PatientID, VisitID, etc.)
- **Versioning**: Both documents are v1.0 with no change history
- **The fundamental ambiguity**: The vendor has registered one product's data dictionary (Amazing Charts) as the documentation for a different product (Picasso), while also maintaining a separate Picasso-specific document that is narrower in scope. This makes it impossible to know with certainty what the actual Picasso EHI export contains.

### Assessment Summary

Doc-tor.com/Picasso has made a genuine attempt at (b)(10) compliance — the export is a database-level CSV dump organized by data class, not a FHIR/USCDI-only clinical summary. The Picasso-specific document covers 21 clinical and administrative data classes with field-level column listings. However, there are real concerns:

1. **Billing data is the biggest gap.** For an integrated EHR/PM/RCM suite, the absence of billing, claims, and payment data from the Picasso-specific export is a significant omission. The billing data exists in the Amazing Charts version of the document, but it's unclear whether that document actually applies to Picasso.

2. **The documentation is a column-name-only data dictionary.** No data types, no descriptions, no value sets, no examples, no export instructions. This is the bare minimum.

3. **The registered URL points to the wrong product's documentation.** The Amazing Charts document was given a Picasso filename and registered with CHPL, but it clearly describes a different system with different database schemas. A separate Picasso-specific document exists but is not registered.

4. **The author (Kathiresan Palanisamy) wrote both documents**, suggesting this is an internal Harris Healthcare effort to create parallel EHI documentation for sibling products, likely from a shared template or codebase.

## Access Summary
- Final URL (after redirects): https://doc-tor.com/wp-content/uploads/2023/11/Picasso-EHI-Export-Documentation-V1_0-1-1.pdf
- Status: found
- Required browser: no
- Navigation complexity: direct_link (registered URL) + one_click (additional docs on disclosures page)
- Anti-bot issues: none

## Obstacles & Dead Ends
- None — all three PDFs were directly downloadable without authentication or special headers.
- The main obstacle is interpretive: understanding the relationship between the two different EHI export documents (Amazing Charts vs. Picasso) required examining both documents' content, column naming conventions, and metadata.
