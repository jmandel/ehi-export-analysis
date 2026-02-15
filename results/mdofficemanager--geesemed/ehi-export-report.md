# MDOfficeManager — EHI Export Documentation

Collected: 2026-02-15

## Source
- Registered URL: https://geesemed.com/wp-content/uploads/2024/05/GeeseMed_b10_Health-Info.Export_11202023.pdf
- CHPL IDs: 11586
- Product: GeeseMed v7.1
- Certification date: 2025-01-01

## Navigation Journal

The registered URL is a direct PDF download hosted on the vendor's WordPress site.

```bash
curl -sI -L "https://geesemed.com/wp-content/uploads/2024/05/GeeseMed_b10_Health-Info.Export_11202023.pdf" \
  -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
# HTTP/2 200, content-type: application/pdf, content-length: 844065
```

No redirects, no authentication, no JavaScript required. Single `curl` command retrieves the PDF:

```bash
curl -sL "https://geesemed.com/wp-content/uploads/2024/05/GeeseMed_b10_Health-Info.Export_11202023.pdf" \
  -H 'User-Agent: Mozilla/5.0' \
  -o GeeseMed_b10_Health-Info.Export_11202023.pdf
```

Verified: `file` reports "PDF document, version 1.5, 8 page(s)". No embedded attachments. No URLs embedded in the PDF beyond the HL7 standard reference (external standard, not followed). Created 2023-11-20 using Microsoft Word 2016 by author "dimple" (consistent with developer contact Dimple Shah).

## What Was Found

The PDF is an 8-page document titled "§170.315(b)(10) Electronic Health Information export - Documentation" for GeeseMed EHR Version 7.1. It contains:

### Export Mechanism
GeeseMed implements EHI export as **C-CDA (Consolidated CDA) document generation** using the HL7 CDA R2 Consolidated CDA Templates for Clinical Notes (US Realm), DSTU Release 2.1, August 2015. Two modes are available:

1. **Single Patient Export** — select a date range, click "Create and View CCD," review the rendered CCD, then click "Export" to download a ZIP file containing a human-readable CCDA document and the XML source file.

2. **Bulk Patient Export** — select date range and provider, search for patients, select patients from a list, choose a destination (local path or direct mail), optionally schedule as recurring, and click "Generate CCD." A batch ZIP file is produced containing per-patient readable CCD files, XML files, and "other clinical data as PDF documents" (e.g., a "LungReport" PDF is shown in the example).

The export is delivered as a ZIP archive containing:
- Per-patient C-CDA XML files (named like `James Portability_11202023_013329.xml`)
- Per-patient human-readable CCD files (HTML/readable format)
- Additional clinical documents as PDF (e.g., `James_11202023_013329_LungReport`)

### Data Dictionary
Pages 6–8 provide a "Sections in CCD" table listing the C-CDA sections and data elements included in the export. The sections are organized by C-CDA template IDs:

| CCD Section | Template ID | Fields |
|---|---|---|
| Patient Demographics/Information | — | Name, Sex, DOB, Race, Ethnicity, Language, Phone, Address |
| Provider Info | — | Author, telecom, Organization name/address/phone |
| Participant (Next of Kin) | — | Name, relationship, address, telephone |
| Encounter Diagnosis | 2.16.840.1.113883.10.20.22.2.22.1 | Code, name, date, status |
| Immunizations | 2.16.840.1.113883.10.20.22.2.2.1 | Vaccine name, date, status, notes |
| Treatment Plan | 2.16.840.1.113883.10.20.22.2.10 | Appointments, lab/med/diagnostic orders, planned observations, dates |
| Social History | 2.16.840.1.113883.10.20.22.2.17 | Smoking status code/description/date |
| Problems | 2.16.840.1.113883.10.20.22.2.5.1 | Problem, status, date onset |
| Medications | 2.16.840.1.113883.10.20.22.2.1.1 | Medication, SIG/direction, start/end date |
| Medication Allergies | 2.16.840.1.113883.10.20.22.2.6.1 | Substance, reaction, severity, status, date |
| Vitals | 2.16.840.1.113883.10.20.22.2.4.1 | Observation, date |
| Laboratory Tests | — | Code, name, order date, ordering provider |
| Laboratory Information | — | Lab name, address, report date, test performed, specimen source |
| Laboratory Results | 2.16.840.1.113883.10.20.22.2.3.1 | Result date, ref range, observation, date/time |
| Goal | 2.16.840.1.113883.10.20.22.2.60 | Description, date |
| Procedures | 2.16.840.1.113883.10.20.22.2.7.1 | Procedure, date |
| Referral | 1.3.6.1.4.1.19376.1.5.3.1.3.1 | Referral, date |
| Medical Equipment | 2.16.840.1.113883.10.20.22.2.23 | Implanted device name/ID |
| Cognitive Status | 2.16.840.1.113883.10.20.22.2.56 | Assessment, date |
| Functional Status | 2.16.840.1.113883.10.20.22.2.14 | Assessment, date |
| Health Concern | 2.16.840.1.113883.10.20.22.2.58 | Concern, date |

## Export Coverage Assessment

### Data Domain Coverage

This export is fundamentally a **C-CDA clinical summary** — it covers the standard clinical domains that map to C-CDA sections but **omits significant portions of the data GeeseMed stores**. Comparing against the product research:

**Covered (via C-CDA sections):**
- Patient demographics and identifiers
- Diagnoses / problem lists
- Medications and prescription history
- Allergies
- Immunizations
- Lab orders, results, and laboratory information
- Vital signs
- Procedures
- Social history (smoking status only)
- Goals and treatment plans
- Referrals
- Implantable devices / medical equipment
- Cognitive and functional status assessments
- Health concerns

**Not covered or not mentioned:**
- **Billing and claims data** — GeeseMed has fully integrated billing with MDOfficeManager PMS. Claims, charges, payments, denial tracking, and revenue cycle data are entirely absent from this export. This is a significant EHI gap.
- **Clinical notes / encounter documentation** — The product's core charting workflow (template-based notes, dictation/transcription, macros, specialty cards) produces narrative clinical documents. The export mentions "other clinical data as PDF documents" in the batch export (a "LungReport" PDF is shown), suggesting some clinical notes may be included as PDFs. However, this is not systematically documented — there's no list of which clinical document types are exported.
- **E-prescribing history** — While medications are in the CCD, the detailed SureScripts e-Rx transaction history (including EPCS controlled substance prescriptions, formulary checks, eligibility results) is not described.
- **Family and surgical history** — Listed as product features but not appearing as CCD sections in the data dictionary.
- **Care plans** — The product is certified for (b)(11) care plans, but the CCD only includes "Treatment Plan" with future appointments and orders, not the full care plan structure.
- **Patient portal messages and activity** — Not mentioned.
- **Telehealth session data** — Not mentioned.
- **Remote patient monitoring data** — Not mentioned.
- **Secure messages** — Provider-to-provider and provider-to-staff messages are not mentioned.
- **Documents and attachments** — Beyond the ad-hoc PDF inclusion shown in the batch export, there's no systematic documentation of how uploaded documents, scanned records, faxes, or external records are included.
- **LTC-specific data** — The product markets to SNF/NF/ALF facilities, but no LTC-specific data elements (ADL tracking, MDS assessments, care facility documentation) are documented in the export.
- **Appointment/scheduling data** — Only "future appointments" appear under Treatment Plan; historical appointment data is not included.

### The (b)(10) vs (g)(10) Problem

This export is a textbook example of the (b)(10)/(g)(10) confusion. The vendor has implemented C-CDA export — which is essentially the (b)(1)/(b)(2) transitions-of-care mechanism — and labeled it as their (b)(10) EHI export. A C-CDA document, even a well-populated one, is a **clinical summary format** designed for care transitions. It covers the USCDI-equivalent clinical data domains but fundamentally cannot represent:

- Billing/financial data (no C-CDA section for claims)
- Free-text clinical notes in their original structure
- Specialty-specific clinical data beyond standard sections
- Operational data that's part of the designated record set

The inclusion of "other clinical data as PDF documents" in the batch export suggests the vendor recognizes the C-CDA alone is insufficient, but this PDF-attachment mechanism is undocumented — there's no way to know what triggers a PDF inclusion or what data it captures.

### Export Format & Standards

- **Format**: C-CDA (HL7 CDA R2, Consolidated CDA Templates DSTU 2.1, August 2015)
- **Delivery**: ZIP archive containing C-CDA XML + human-readable HTML + supplemental PDFs
- **Standard compliance**: Uses recognized C-CDA template IDs for each section
- **Adequacy for EHI**: C-CDA is appropriate for the clinical summary data it covers, but it's the wrong vehicle for a comprehensive EHI export. A database export, CSV dump, or FHIR Bulk Data export would better serve the (b)(10) requirement by covering all data domains.

### Documentation Quality

- **Readability**: The 8-page PDF is clearly laid out with screenshots and step-by-step instructions. A user could follow the export process.
- **Data dictionary**: Present but minimal — the "Sections in CCD" table lists field names and C-CDA element mappings but provides **no data types, cardinality, constraints, or value sets**. Most "Description" cells simply restate the field name (e.g., "Diagnosis code" maps to "Encounter Code"). Many description cells are blank.
- **Examples**: Screenshots show the export interface with sample patient data (Alice Newman, Von Portability, etc.), which is helpful. The batch export file listing shows the actual ZIP structure.
- **Developer usability**: A developer could not implement an import based on this documentation alone. They would need to rely on the C-CDA standard itself (which is well-documented externally) and would have no guidance on the supplemental PDF attachments.
- **Maintenance**: Created November 2023, references Version 7.1. The PDF on the server was last modified August 2025, though the creation date metadata is 2023. This may indicate the file was re-uploaded without content changes.

### Structure & Completeness

- **Field-level granularity**: Field names only. No data types, lengths, formats, or constraints.
- **Value sets**: Not documented. Coded fields (diagnosis codes, medication codes, smoking status codes) reference C-CDA template IDs but don't specify which code systems or value sets are used.
- **Relationships**: Not documented beyond the implicit C-CDA document structure.
- **Versioning**: No change history.

### Overall Assessment

This is a **minimal-effort compliance document** from a very small vendor. GeeseMed has essentially repackaged their C-CDA transitions-of-care export as their EHI export documentation. The coverage is limited to the standard USCDI clinical summary domains — appropriate for (g)(10) FHIR API or (b)(1)/(b)(2) transitions of care, but inadequate for (b)(10) which requires export of **all** electronic health information. Billing data, detailed clinical notes, specialty documentation, patient portal activity, telehealth data, and LTC-specific data (despite marketing to that segment) are all absent from the documented export. The data dictionary is superficial, listing field names without data types or value sets. The hint of supplemental PDFs in the batch export suggests awareness that C-CDA alone is insufficient, but this mechanism is not documented enough to assess.

## Access Summary
- Final URL: https://geesemed.com/wp-content/uploads/2024/05/GeeseMed_b10_Health-Info.Export_11202023.pdf
- Status: found
- Required browser: no
- Navigation complexity: direct_link
- Anti-bot issues: none

## Obstacles & Dead Ends
None. The URL returned the PDF directly with no authentication, redirects, or anti-bot measures.
