# Tenzing Medical LLC — EHI Export Documentation

Collected: 2026-02-15

## Source
- Registered URL: http://tenzingmedical.com/TenzingEHIFormatInfo.pdf
- CHPL IDs: 10799
- Certification date: 2022-01-20
- Mandatory disclosures page: http://www.tenzingmedical.com/onc-cert

## Navigation Journal

1. **Initial probe** — The registered URL returns HTTP 200 with `Content-Type: application/pdf` (102,594 bytes). Direct download, no redirects.
   ```
   curl -sI -L "http://tenzingmedical.com/TenzingEHIFormatInfo.pdf" -H 'User-Agent: Mozilla/5.0'
   ```

2. **Downloaded the registered PDF** (`TenzingEHIFormatInfo.pdf`) — 3 pages, created 2023-11-14, authored in Microsoft Word for Microsoft 365. This is the EHI export format specification.
   ```
   curl -sL "http://tenzingmedical.com/TenzingEHIFormatInfo.pdf" -H 'User-Agent: Mozilla/5.0' -o downloads/TenzingEHIFormatInfo.pdf
   ```

3. **Checked the mandatory disclosures / ONC cert page** at `http://www.tenzingmedical.com/onc-cert` (HTTP 200, HTML, 13,618 bytes). Found two EHI-related links:
   - "EHI Export" → `http://tenzingmedical.com/ElectronicHealthInformationExport.pdf`
   - "Tenzing Electronic Health Information (EHI) Export Format" → `http://tenzingmedical.com/TenzingEHIFormatInfo.pdf` (the registered URL)

4. **Downloaded the second PDF** (`ElectronicHealthInformationExport.pdf`) — 4 pages, created 2023-07-10, titled "170.315(b)(10) Electronic Health Information export". This is the user guide / operational instructions for performing the export.
   ```
   curl -sL "http://tenzingmedical.com/ElectronicHealthInformationExport.pdf" -H 'User-Agent: Mozilla/5.0' -o downloads/ElectronicHealthInformationExport.pdf
   ```

5. **Checked both PDFs for embedded URLs and attachments** — none found. No links to additional documentation, schemas, sample files, or external resources.

6. **Other links on the ONC cert page** — `realworldtestingplan.pdf` and `SVAP.docx` are not EHI export documentation (regulatory filings). The CHPL developer page link goes to healthit.gov. None of these are in scope.

## What Was Found

The EHI export documentation consists of two short PDFs (7 pages total) describing a **dual-system export approach**:

### System 1: Tenzing VistA (Clinical Data)

**Format:** Structured XML using Consolidated-Clinical Document Architecture (C-CDA) CDA R2.1, with USCDI v2. Exports one XML document per patient.

**Export mechanism:** Two VistA menu options:
- `VGTM EHI EXPORT` — interactive, user-facing option. Allows selecting hospital locations, latest encounter / specific encounter / date range, and export destination path. Runs in real-time at the console.
- `VGTM AUTO CCDA EXPORT` — scheduled batch option using VistA's Taskman scheduling system. Configurable for one-time or recurring exports (e.g., monthly) with date range parameters.

**Data sections documented (28 sections):**

| Section | C-CDA Template ID |
|---------|-------------------|
| Care Team | XPath-based (performer) |
| Problems | 2.16.840.1.113883.10.20.22.2.5.1 |
| Vitals | 2.16.840.1.113883.10.20.22.2.4.1 |
| Medications | 2.16.840.1.113883.10.20.22.2.1.1 |
| Admission Medications | 2.16.840.1.113883.10.20.22.2.44 |
| Ambulatory Medications | 2.16.840.1.113883.10.20.22.2.38 |
| Discharge Medications | 2.16.840.1.113883.10.20.22.2.11.1 |
| Allergies and Intolerances | 2.16.840.1.113883.10.20.22.2.6.1 |
| Social History / Smoking Status | 2.16.840.1.113883.10.20.22.2.17 |
| Assessments | 2.16.840.1.113883.10.20.22.2.8 |
| Encounter Diagnosis | 2.16.840.1.113883.10.20.22.2.22.1 |
| Procedures | 2.16.840.1.113883.10.20.22.2.7.1 |
| Diagnostic Results | 2.16.840.1.113883.10.20.22.2.3.1 |
| Plan of Treatment | 2.16.840.1.113883.10.20.22.2.10 |
| Immunizations | 2.16.840.1.113883.10.20.22.2.2.1 |
| Reason For Referral | 1.3.6.1.4.1.19376.1.5.3.1.3.1 |
| Chief Complaint | 2.16.840.1.113883.10.20.22.2.13 |
| Admit Diagnosis | 2.16.840.1.113883.10.20.22.2.43 |
| Discharge Diagnosis | (template ID not listed) |
| Instructions | 2.16.840.1.113883.10.20.22.2.45 |
| Functional Status | 2.16.840.1.113883.10.20.22.2.14 |
| Mental Status | 2.16.840.1.113883.10.20.22.2.56 |
| Notes | 2.16.840.1.113883.10.20.22.2.65 |
| Discharge Instructions | 2.16.840.1.113883.10.20.22.2.41 |
| Medical Equipment | 2.16.840.1.113883.10.20.22.2.23 |
| Health Concerns | 2.16.840.1.113883.10.20.22.2.58 |
| Goals | 2.16.840.1.113883.10.20.22.2.60 |
| Payers/Insurance | 2.16.840.1.113883.10.20.22.2.18 |
| Family History | 2.16.840.1.113883.10.20.22.2.15 |

The user selects which data sections to include in each export.

### System 2: McKesson Series (Billing/Financial Data)

**Format:** "Structured delimited format" (no further specification of delimiter, encoding, or schema).

**Data sections documented (4 sections):**

| Section | Path | Description |
|---------|------|-------------|
| Patient | /Patient | Patient demographics |
| Payer/Insurance | /Patient/Payer | Insurance, payer information |
| Enrollment/Account Information | /Patient/Account | Enrollment, account information |
| Billing History | /Patient/Billing | Billing history, adjudication, etc. |

Supports individual patient and batch selection with date range filtering.

## Export Coverage Assessment

### Data Domain Coverage

**Genuinely strong areas:**

Tenzing's approach of using two systems — VistA for clinical data and McKesson Series for billing — is architecturally sound for (b)(10) compliance. The C-CDA export from VistA covers a broad set of clinical data sections that goes well beyond a minimal USCDI/US Core set. Notable inclusions:

- **Mental Status and Functional Status** — specialty assessments not always included in basic exports
- **Health Concerns (SDOH)** — social determinants of health
- **Medical Equipment** — implanted and external devices
- **Multiple medication contexts** — admission, ambulatory, and discharge medications separately
- **Payers/Insurance** — from VistA side, complementing the Series billing data
- **Notes** — free text clinical documentation (section 2.16.840.1.113883.10.20.22.2.65)
- **Family History, Goals, Chief Complaint** — additional clinical context

The McKesson Series export addresses billing, account enrollment, and payer data explicitly — domains that most vendors using only FHIR/C-CDA exports completely miss.

**Apparent gaps relative to product research:**

- **Laboratory results detail** — "Diagnostic Results" is listed but VistA at Oroville interfaces with Sunquest for a full-service lab (chemistry, microbiology, pathology, blood bank, cytology). It's unclear whether the C-CDA export captures granular lab results from the Sunquest interface or just high-level summaries.
- **Radiology/Imaging** — The "Diagnostic Results" section may cover radiology results, but VistA Imaging (clinical images, scanned documents) is not explicitly mentioned as an exportable data type. Clinical images and scanned documents are part of the designated record set.
- **Pharmacy-specific data** — While multiple medication sections exist, specific pharmacy data like controlled substance tracking, drug interaction history, formulary decisions, and ePrescribing transmission records (which are stored in VistA) are not clearly covered in C-CDA sections.
- **Surgical records** — Despite VistA having a Surgery module and CPRS having a Surgery tab, there is no specific "Surgery" export section. Surgical data may be captured under "Procedures" but operative notes, anesthesia records, and surgical details may not be fully represented.
- **ADT (Admission/Discharge/Transfer) records** — No explicit section for encounter/visit-level ADT data beyond diagnoses. The encounter context (dates, locations, providers, disposition) is EHI.
- **Custom Oroville/Tenzing applications** — The product research identifies custom apps (patient dashboard, pediatric growth charts, flow sheets for anesthesia/obstetrics/infusion, bed control). Data generated by these custom modules is likely not captured in standard C-CDA sections.
- **Dietary/Nutrition orders** — VistA has a Dietetics module, but no export section for dietary orders is listed.
- **Patient portal communications** — Messages or data shared through the Bridge Patient Portal are not mentioned.

**Billing export ambiguity:**

The McKesson Series billing export is described at an extremely high level — 4 sections (Patient, Payer, Account, Billing) with no field-level documentation whatsoever. We don't know:
- What fields are in each section
- What the delimiter is
- What the encoding is
- What "billing history, adjudication, etc." actually includes
- Whether claims detail, line items, charge codes, or payment records are included

### Export Format & Standards

**VistA clinical export (C-CDA):**
- Uses C-CDA R2.1, a well-established HL7 standard for clinical document exchange
- USCDI v2 data classes
- Sections identified by standard HL7 template IDs — a third party with C-CDA parsing capability could process these
- The choice of C-CDA is reasonable for a system like VistA, though it constrains what can be expressed (VistA's internal FileMan data model is far richer than C-CDA's section structure)
- SVAP is mentioned for keeping up with format standards

**Series billing export:**
- "Structured delimited format" — no standard identified, completely proprietary
- The path notation (/Patient, /Patient/Payer, etc.) suggests a hierarchical structure but provides no actual schema
- Without field documentation, a recipient could not parse or use this data

**Key concern:** C-CDA is a document standard designed for care coordination summaries, not a database export format. While it can carry substantial clinical data, it inherently flattens and lossy-compresses the rich relational data in VistA's FileMan database. VistA stores data in hundreds of FileMan files with complex cross-references — a C-CDA export maps this to ~28 standardized sections, necessarily losing specificity, internal relationships, and non-standard data fields. A more complete (b)(10) approach would export the underlying FileMan data dictionaries, but this is the approach they've chosen.

### Documentation Quality

**Moderate but thin.** The two PDFs total just 7 pages for a complex dual-system export.

Positives:
- Clear identification of each C-CDA section with standard template IDs
- Practical screenshots/examples of the VistA menu interface for running exports
- Clear explanation of both interactive and scheduled export options
- Task parameter syntax is well-documented for the scheduled export

Weaknesses:
- **No field-level documentation** — the format spec lists 28 section names and their template IDs but not the individual data elements within each section. A developer would need to refer to the C-CDA R2.1 specification to know what fields are in each section.
- **No sample export files** — no example C-CDA XML or Series delimited files are provided
- **No schema artifacts** — no XSD, schematron, or other machine-readable format specification
- **Series export is barely documented** — 4 section names with one-line descriptions and no field definitions
- **No data dictionary** in any meaningful sense — the table of sections is essentially a table of contents, not a data dictionary
- **No value set or coded field documentation**
- **No relationship documentation** between VistA and Series data

A developer could implement a C-CDA import for the VistA portions by referencing the standard C-CDA specification (since template IDs are provided), but could not implement a Series data import without additional information.

### Structure & Completeness

- **Granularity:** Section-level only. No field-level detail for either system.
- **Coded fields:** Not documented. C-CDA template IDs are provided, but the actual coded values (SNOMED, LOINC, RxNorm, etc.) used within each section are not specified.
- **Relationships:** Not documented. How VistA clinical data relates to Series billing data for the same patient is not explained.
- **Versioning:** Document shows "rev: 11/14/2023" — a single version, no change history.

### Overall Assessment

Tenzing Medical's approach is **architecturally sensible but under-documented**. The dual-system strategy (VistA for clinical, Series for billing) is a legitimate (b)(10) design that goes beyond the common vendor pattern of simply repackaging their (g)(10) FHIR API. The 28 C-CDA clinical sections represent broader coverage than most vendors provide, and the inclusion of a separate billing system export shows awareness that EHI includes financial data.

However, the documentation is a **compliance checkbox** rather than a practical technical reference. Seven pages for a dual-system export that spans clinical, financial, and administrative data is inadequate. The absence of field-level documentation, sample files, or machine-readable schemas means the documentation alone does not enable a third party to fully understand, validate, or import the exported data.

The use of C-CDA for a full VistA EHI export also raises questions about completeness — VistA's FileMan database contains hundreds of files with data that doesn't map cleanly to C-CDA sections (custom flow sheets, scheduling data, specialty-specific clinical entries). The documentation does not address what VistA data is *not* included in the C-CDA export or how to access it.

This is consistent with the vendor profile: a very small company (essentially an in-house team at Oroville Hospital) that built a functional export but invested minimally in external-facing documentation. The documentation was last updated in November 2023 and the ONC cert page was updated as recently as June 2025, suggesting the site is still maintained.

## Access Summary
- Final URL (after redirects): http://tenzingmedical.com/TenzingEHIFormatInfo.pdf
- Status: found
- Required browser: no
- Navigation complexity: direct_link (registered URL is a direct PDF download; second PDF found one click away on the ONC cert page)
- Anti-bot issues: none (note: site uses HTTP, not HTTPS — SSL certificate issues noted in product research)

## Obstacles & Dead Ends
- None. Both PDFs were directly accessible via simple HTTP GET requests with no authentication, CAPTCHA, or anti-bot measures.
- The website uses HTTP (not HTTPS) — the SSL certificate was expired at time of prior research. This is a minor access concern but did not impede downloads.
