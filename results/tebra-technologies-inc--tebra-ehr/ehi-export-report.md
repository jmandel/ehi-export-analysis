# Tebra Technologies, Inc. — EHI Export Documentation

Collected: 2026-02-15

## Source
- Registered URL: https://www.tebra.com/tebra-resources/macra-mips/
- CHPL IDs: 11557
- Product: Tebra EHR v5.1
- Certification Date: 2024-12-19

## Navigation Journal

### Step 1: Initial probe of registered URL
```bash
curl -sI -L "https://www.tebra.com/tebra-resources/macra-mips/" -H 'User-Agent: Mozilla/5.0'
```
Result: 301 redirect to `https://www.tebra.com/tebra-resources/macra-mips` (trailing slash removed), then 200 OK. WordPress site on WP Engine behind Cloudflare. Content-Type: text/html.

### Step 2: Page examination
The registered URL is a MACRA/MIPS marketing and compliance page titled "Quality programs & regulatory support." The page contains:
- MACRA/MIPS marketing content and product screenshots
- FAQ accordion about MACRA/MIPS (not EHI-related)
- ONC Health IT Certification section with vendor info, certification details, and certified modules listing
- Real World Test Plans table (2022-2025)
- APIs section linking to two PDFs: FHIR API Documentation and General Clinical API Documentation
- **EHI Export Functionality section** — a single paragraph (the entirety of the (b)(10) export documentation)

### Step 3: EHI Export section content (verbatim)
Found at the bottom of the certification section (HTML lines 2425-2431):
> **EHI Export Functionality**
> Tebra EHR enables providers to export out EHI for individual patients and their patient population at any time without developer assistance. Export formats include C-CDA documents for clinical records, PDFs for claims and billing information, and also documents in the original native format which they were uploaded.

No links to further documentation, data dictionary, schema, sample files, or format specifications.

### Step 4: Downloaded linked documents
From the page, I downloaded:
- FHIR API User Guide PDF (May 2025): `https://www.tebra.com/wp-content/uploads/2025/05/Tebra-FHIR-API-User-Guide.pdf`
- General Clinical API Documentation PDF (2023): `https://www.tebra.com/wp-content/uploads/2023/10/General_API_Documentation-Tebra.pdf`
- Costs and Guidance PDF (Dec 2022): `https://learn.tebra.com/rs/677-NCQ-300/images/TB-Costs-and-Guidance-Dec-2022.pdf`
- Real World Test Plans and Results (2022-2025)
- Full page HTML and screenshot

### Step 5: Searched help center
Searched `helpme.tebra.com` for EHI export documentation via web search and direct browsing. Key findings:
- **Export Patient Clinical Data** (`https://helpme.tebra.com/Platform/Practice_Settings/Data_Management/Export_Patient_Clinical_Data`): Describes how to do a bulk export of patient clinical data as individual XML Summary of Care (.ccda) files, filterable by date range and provider. One-time or recurring exports. Downloaded as a zip file.
- **21st Century Cures Act FAQs** (`https://helpme.tebra.com/CMS_Incentive_Programs/21st_Century_Cures_Act/21st_Century_Cures_Act_FAQs`): Describes EHI scope, notes that USCDI-defined EHI is available via patient portal, and for other EHI categories "Tebra can provide access through other means" including "a secure ShareFile service through which exports of EHI may be shared." Directs patients to submit a "Cures Act Request Form."

### Step 6: Found Cures Act Request Form
The FAQ links to `https://www.tebra.com/cures-act-request/` — a OneTrust-powered privacy portal form. The form allows patients (or authorized agents) to request specific categories of EHI:

1. Allergies and Intolerances
2. Assessment and Plan of Treatment
3. Care Team Members
4. Clinical Notes
5. Immunizations
6. Laboratory Tests & Results
7. Medications
8. Patient Demographics
9. Problems
10. Procedures
11. Patient's Implantable Device(s)
12. Vital Signs
13. Past Medical History
14. Past Surgical History
15. Family History
16. Social History (e.g., smoking status)
17. OB/Pregnancy History
18. Account/Insurance Information
19. Documents

### Step 7: Examined Real World Test Results
The 2024 Real World Test Results (315(b)(10)) document actual EHI export usage:
- 755 providers tested over 3 months (April-June 2024)
- 3,931 total EHI exports performed
- 790 practices performing exports
- ~4.98 exports per practice average
- Most exports contained fewer than 100 patients (short date ranges)
- Majority contained 10 or fewer patients (single-day or two-day range)
- All exports completed without issue
- Export includes C-CDAs and "other patient documents"

### Step 8: Searched for additional documentation
```
Web search: tebra EHR "EHI export" data dictionary format documentation 2024 2025
Web search: site:helpme.tebra.com "EHI export" OR "electronic health information export"
```
No additional EHI export-specific documentation found. No data dictionary, schema, or format specification exists beyond what is described above.

## What Was Found

### EHI Export Documentation Summary

Tebra's EHI export documentation is **extremely minimal**. The entire (b)(10) export documentation on the registered URL is a single paragraph that describes three export formats:

1. **C-CDA documents** for clinical records
2. **PDFs** for claims and billing information
3. **Native format documents** (documents in the format they were uploaded)

There is no data dictionary, no schema definition, no field-level documentation, no sample export files, and no format specification of any kind.

### Export Mechanism

Piecing together information from the help center and test results, the EHI export works as follows:

**For clinical data (C-CDA export):**
- Accessible via Practice Settings > Data Management > Export Patient Data
- Exports individual XML Summary of Care files (.ccda extension) per patient
- Filterable by date range and provider
- Can be one-time or recurring (monthly on 1st or weekly on Mondays)
- Downloads as a zip file
- Now also includes uploaded patient documents (added November 2023)

**For billing data:**
- Exported as PDFs (per the mandatory disclosures paragraph)
- The practice management module (formerly Kareo Billing) has separate report exports for demographics, charges, unpaid claims, A/R aging, and fee schedules in Excel/CSV format

**For other EHI categories:**
- Tebra provides a "Cures Act Request Form" (OneTrust privacy portal) where patients can request 19 categories of data
- Fulfillment is via "a secure ShareFile service"
- This is a manual, patient-initiated request process rather than a self-service export feature

### FHIR API (g(10), not b(10))

The FHIR API User Guide (May 2025) documents a SmileCDR-powered FHIR R4 API for USCDI v1 data. It covers:
- Standard US Core resource types: Patient, AllergyIntolerance, CarePlan, CareTeam, Condition, DiagnosticReport, DocumentReference, Encounter, Goal, Immunization, Implantable Device, Laboratory Result Observation, Location, Medication, MedicationRequest, Observation, Organization, Practitioner, PractitionerRole, Procedure, Provenance
- OAuth 2.0 authentication (3-legged for patient apps, 2-legged for backend services)
- Backend bulk data transfers for authorized applications

This is explicitly the (g)(10) standardized API, not the (b)(10) export. The guide itself states it covers "USCDI version 1 requirements" and uses "HL7 FHIR US Core Implementation Guide STU3 Release 3.1.1."

### General Clinical API

An older (2023) patient-facing API that provides JSON access to clinical data via API key authentication through the patient portal. Also covers only clinical data — not a (b)(10) mechanism.

## Export Coverage Assessment

### Data Domain Coverage

Based on the product research, Tebra stores data across clinical, billing, scheduling, telehealth, patient portal, and practice marketing domains. Here is the coverage assessment:

**Clearly covered (via C-CDA export):**
- Patient demographics
- Problems/conditions
- Medications
- Allergies
- Vital signs
- Lab results
- Immunizations
- Clinical notes (as Summary of Care content)
- Assessment and plan
- Procedures
- Implantable devices

**Partially covered (via PDF or request form):**
- Billing records — described as "PDFs for claims and billing information" but no details on what billing fields are included or excluded
- Account/Insurance Information — listed as a selectable category on the Cures Act Request Form
- Documents — uploaded documents now included in the export (since November 2023)

**Ambiguous or likely missing:**
- Prescription history detail (e-prescribing is handled by DrFirst Rcopia; unclear if Rx history beyond what's in C-CDA is exported)
- Lab order details (labs are handled by LabSoft; unclear if full order history is exported)
- Telehealth visit records (metadata, recordings if stored)
- Patient portal secure messages
- Patient intake form data
- Appointment/scheduling data (operational, but visit history linked to encounters may qualify)
- Referral records (beyond what's in C-CDA transitions of care)

**Clearly not covered (and expected to be):**
- Detailed billing data at the field level — charges, line items, CPT/ICD codes, ERA/EOB detail, denial information, claim status history, payment records. The "PDF for claims and billing" language suggests rendered summaries rather than computable billing data.
- Custom clinical forms/templates — Tebra supports SOAP note templates and macros; the data captured in these custom fields is unlikely to be fully represented in a standard C-CDA
- AI Note Assist generated content — the product touts AI-generated notes; unclear if the underlying data (audio transcripts, AI processing metadata) is included

### Export Format & Standards

The export uses three formats:

1. **C-CDA (XML)** — A recognized interoperability standard, appropriate for clinical data. However, C-CDA is a summary document standard, not a comprehensive database export. It captures the most recent/active clinical state well but is not designed to capture the full history of billing transactions, custom form data, or system-specific fields.

2. **PDF** — For claims and billing. PDF is not a computable format. A developer cannot programmatically parse PDF billing records to reconstruct billing history. This is a significant limitation for (b)(10) compliance, which requires data in a "computable" format.

3. **Native format** — Documents in their original upload format. Appropriate for documents but doesn't address structured data.

The mismatch between format and requirement is notable: the (b)(10) requirement specifies export in "computable" format. C-CDA satisfies this for clinical data, but PDF does not satisfy it for billing data. A CSV or JSON export of billing records would be more appropriate.

### Documentation Quality

**Very poor.** The documentation quality is among the weakest possible for a certified product:

- **No data dictionary whatsoever** — There is no listing of tables, fields, data types, or value sets anywhere in the publicly accessible documentation
- **No schema or format specification** — No XSD, JSON Schema, or even a prose description of what fields are in the C-CDA or billing PDF exports
- **No sample export files** — No examples of what an exported C-CDA looks like or what a billing PDF contains
- **No field-level definitions** — Nothing beyond "C-CDA documents for clinical records, PDFs for claims and billing"
- **No export instructions** — The mandatory disclosures page has no link to the help center article that actually describes how to perform the export
- **No version history or changelog** — No indication of how the export has evolved

The FHIR API guide is relatively well-documented (33 pages with resource descriptions, field tables, authentication flows), but it documents the (g)(10) API, not the (b)(10) export.

A developer attempting to import Tebra EHI export data would have essentially no documentation to work with beyond the C-CDA standard itself.

### Structure & Completeness

- **Granularity**: Table/field level documentation is completely absent for the (b)(10) export
- **Value sets**: Not documented for the export. The FHIR API guide references standard terminologies (SNOMED, ICD-10, LOINC, RxNorm) but these apply to the (g)(10) API, not the (b)(10) export
- **Relationships**: Not documented
- **Versioning**: No version history. The costs_and_guidance PDF still references "Kareo EHR" (the pre-rebrand name) and cites (b)(6) rather than (b)(10), suggesting it predates the December 2024 certification
- **Completeness**: The Cures Act Request Form lists 19 categories but there is no documentation of what data is included in each category or what format the response takes

### The (b)(10) vs (g)(10) Distinction

Tebra presents a nuanced but ultimately inadequate picture. The mandatory disclosures paragraph correctly distinguishes the EHI export (which includes billing PDFs and native documents) from the FHIR API (which covers USCDI clinical data). This shows awareness that (b)(10) is broader than (g)(10).

However, the clinical data portion of the EHI export is a C-CDA — which is essentially the same Summary of Care document used for transitions of care under (b)(1)/(b)(6). The 2024 test plan originally measured "Patient Batch Exports" under (b)(6) and then retroactively substituted it for the "broader 315(b)(10) EHI Export" — suggesting the same export mechanism was relabeled. The C-CDA Summary of Care covers roughly the same data as USCDI/US Core, so the clinical portion of the EHI export provides similar coverage to the (g)(10) API.

The key distinction Tebra makes is adding billing PDFs and uploaded documents to the export. This is a step beyond pure (g)(10), but the PDF format for billing data undermines the computable format requirement, and there is no evidence of comprehensive export of specialty-specific clinical data, custom forms, or structured billing records beyond what fits in a C-CDA and a rendered PDF.

## Access Summary
- Final URL (after redirects): https://www.tebra.com/tebra-resources/macra-mips
- Status: found
- Required browser: no (all content accessible via curl; browser used for screenshots and to examine Cures Act Request Form iframe)
- Navigation complexity: direct_link (EHI section is inline on the registered page)
- Anti-bot issues: none (Cloudflare present but no blocking)

## Obstacles & Dead Ends

- The Costs and Guidance PDF is outdated (December 2022) and references "Kareo EHR" with (b)(6) certification criteria rather than (b)(10). It does not mention EHI export.
- The FHIR API User Guide and General API Documentation are well-documented but cover (g)(10) patient API access, not (b)(10) EHI export.
- No downloadable data dictionary, schema, or format specification exists for the EHI export.
- Web searches for Tebra EHI export documentation returned no results beyond what was found on the registered URL and help center.
- The help center article "Export Patient Clinical Data" describes the mechanics of running a C-CDA batch export but provides no details about what data fields are included in the export.
- The Cures Act Request Form (OneTrust privacy portal) is a manual patient request process rather than technical documentation of export format.
