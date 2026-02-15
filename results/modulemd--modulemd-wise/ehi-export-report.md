# ModuleMD — EHI Export Documentation

Collected: 2026-02-14

## Source
- Registered URL: https://modulemd.com/wp-content/uploads/2023/11/B10-Data-Export-Process-Flow-Document_compressed.pdf
- CHPL IDs: 11092
- Product: ModuleMD WISE™ 10.0
- Certification date: 2022-12-19

## Navigation Journal

The registered URL is a direct link to a PDF hosted on ModuleMD's WordPress site.

```bash
# Probe URL — direct PDF download, no redirects
curl -sI -L "https://modulemd.com/wp-content/uploads/2023/11/B10-Data-Export-Process-Flow-Document_compressed.pdf" -H 'User-Agent: Mozilla/5.0'
# Returns: HTTP 200, Content-Type: application/pdf, Content-Length: 448021

# Download
curl -sL "https://modulemd.com/wp-content/uploads/2023/11/B10-Data-Export-Process-Flow-Document_compressed.pdf" -H 'User-Agent: Mozilla/5.0' -o downloads/B10-Data-Export-Process-Flow-Document_compressed.pdf

# Verify
file downloads/B10-Data-Export-Process-Flow-Document_compressed.pdf
# PDF document, version 1.5, 9 page(s)
```

Also checked the ONC mandatory disclosures page at https://modulemd.com/onc-certified/ for additional EHI export documentation or links. Found no additional downloadable files, data dictionaries, or EHI-specific content beyond general certification information. The ONC page confirms the (b)(10) certification but does not link to any supplementary export documentation.

## What Was Found

The entire EHI export documentation consists of a single 9-page PDF titled **"B10 DATA EXPORT PROCESS FLOW"**, authored by Rajesh Dandu, created 2023-11-20 using Microsoft Word 2016, and compressed via iLovePDF.

### Document Content

The PDF is a step-by-step process guide with annotated screenshots showing how to use the Data Export feature in ModuleMD WISE. The content covers:

1. **Navigation path**: Administration → Practice Setup → Data Export

2. **Export creation workflow**:
   - Click "+New Export" to initiate a request
   - Select patients: single patient (by name or account number), multiple patients, or "Select All Patients"
   - Configure options: Archive Name, File Type (dropdown, not enumerated), Encryption Key (password protection), Comments

3. **Processing pipeline** (3 steps):
   - Step 1: Request submitted, status = "New"
   - Step 2: Data generated into folders, status = "InProgress"
   - Step 3: Data copied to cloud, URL generated, status = "Completed" with an expiry date
   - A backend program runs daily to process export requests

4. **Download mechanism**:
   - Only the requestor who submitted the request can see the download link
   - Downloaded as a folder structure organized by patient
   - Each patient folder contains **C-CDA XML files** (e.g., `QAT-1-11142023_ClinicalSummary`)

5. **Patient Portal access**:
   - Individual patients can download their own C-CDA files via Patient Portal → Documents
   - File naming pattern: `DevAsthma7-6-11172023_ClinicalSummary.xml`

### What Is NOT in the Document

- No data dictionary or field definitions
- No description of which data elements are included in the C-CDA export
- No schema documentation or C-CDA template specifications
- No description of what "File Type" options are available in the dropdown
- No sample export files or example data
- No documentation of export format beyond "C-CDA in XML files"
- No mention of data that falls outside C-CDA (billing, specialty-specific clinical data, etc.)
- No API documentation
- No mention of how non-clinical data is exported

## Export Coverage Assessment

### Data Domain Coverage

This is a specialty allergy/immunology, pulmonology, and ENT EHR that stores a rich set of clinical and operational data. Based on the product research, ModuleMD WISE manages:

**Likely covered by C-CDA export (standard clinical data):**
- Demographics, contacts
- Problem lists, conditions
- Medication lists, prescriptions
- Allergies and adverse reactions
- Lab results (Quest/LabCorp integration)
- Vital signs
- Immunization records
- Clinical notes (to some extent)
- Care plans

**Almost certainly missing from a C-CDA export (specialty-specific and non-clinical):**
- **Allergy skin test results** — wheal/flare measurements per allergen, intradermal and prick testing panels. This is the product's core differentiator and there is no standard C-CDA section for detailed skin test data grids.
- **Immunotherapy treatment records** — extract/vial compounding records with lot numbers, allergen compositions, Beyond Use Dates, dosage schedules, injection administration records with questionnaires, MQT algorithm data. This is highly specialized data with no C-CDA equivalent.
- **USP 797 compliance data** — lot-specific allergens, BUDs, vial expiration tracking, operator logs
- **Spirometry/PFT results** — while some spirometry data might fit in C-CDA diagnostic results, the trending and detailed PFT data likely does not
- **SkinSight AI image analysis results** — image-based skin test analysis data
- **Billing and financial data** — claims, charges, payments, account balances, insurance coverage. C-CDA does not carry billing data.
- **Practice management data** — scheduling, referrals, insurance eligibility, custom forms, digital signatures
- **Revenue cycle data** — claim scrubbing results, auto-generated charge records
- **Infusion records** — infusion session details, pre-authorization data, biologic administration records
- **Inventory data** (InDrA) — medication/supply inventory, dispensing records
- **Patient portal interactions** — messages, appointment requests, refill requests
- **AI-generated content** — JOSH dictation transcripts, AI-suggested ICD/CPT codes

The gap between what this product stores and what a C-CDA clinical summary can represent is enormous. This is a specialty product where the most valuable data — detailed allergy testing, immunotherapy management, skin test imaging — is precisely the data that has no standard C-CDA representation. The export appears to be a clinical summary repackaged as the EHI export, which would cover perhaps 20-30% of the patient's designated record set.

### Export Format & Standards

The export uses **C-CDA (Consolidated Clinical Document Architecture) XML files**. Based on the screenshots showing filenames like `QAT-1-11142023_ClinicalSummary`, these appear to be CCD/ClinicalSummary documents — the same document type typically generated for transitions of care under (b)(1).

This is a textbook case of the **(b)(10) vs (g)(10) confusion**, though here it's more like (b)(10) vs (b)(1). The vendor appears to be reusing their transitions-of-care C-CDA generation as their EHI export mechanism. C-CDA Clinical Summaries are designed for clinical summaries during care transitions, not for comprehensive data export. They cover a defined set of clinical domains (problems, medications, allergies, results, etc.) but cannot represent:
- Specialty-specific structured data (allergy testing, immunotherapy)
- Billing and financial data
- Practice management data
- Custom forms and assessments
- Inventory and dispensing data

A C-CDA is fundamentally the wrong format for a comprehensive EHI export from a specialty allergy/immunology platform. The appropriate approach would be a database export (CSV, SQL dump, or similar) that captures all patient-facing data tables, supplemented by C-CDAs for the clinical summary portion.

### Documentation Quality

The documentation is minimal — a 9-page process guide with screenshots showing how to click through the export UI. It reads as a quick user guide, not technical export documentation:

- **No data dictionary**: There are no field definitions, no table listings, no description of what data elements appear in the export
- **No schema documentation**: No C-CDA templates are specified, no profile constraints documented
- **No sample files**: No example export output is provided
- **No format specification**: The "File Type" dropdown is visible in screenshots but never described — we don't know what options exist
- **No worked examples**: A developer could not implement an import based on this documentation
- **Marked "Confidential"**: The last page is marked "|| Confidential ||", suggesting the vendor may not have intended this as fully public documentation, despite it being publicly accessible via direct URL

A developer receiving this export would get C-CDA XML files and would need to reverse-engineer the content and structure entirely from the files themselves.

### Structure & Completeness

The documentation provides:
- ✓ Navigation instructions to reach the export feature
- ✓ Screenshots of the export creation UI
- ✓ Description of the 3-step processing pipeline
- ✓ Information about access control (only requestor can download)
- ✓ Encryption key option for security
- ✗ No field-level documentation at all
- ✗ No data dictionary
- ✗ No value set documentation
- ✗ No relationship documentation
- ✗ No versioning or change history
- ✗ No description of export content/scope

This is among the most minimal EHI export documentation possible — it documents the *process* of requesting and downloading an export but says nothing about the *content* of the export. The documentation is a compliance checkbox, not a technical specification.

## Access Summary
- Final URL (after redirects): https://modulemd.com/wp-content/uploads/2023/11/B10-Data-Export-Process-Flow-Document_compressed.pdf
- Status: found
- Required browser: no
- Navigation complexity: direct_link
- Anti-bot issues: none

## Obstacles & Dead Ends

None — the URL worked perfectly as a direct PDF download. The obstacle is not access but substance: the documentation itself is extremely thin, providing no technical detail about the export's data content, format specifications, or scope.
