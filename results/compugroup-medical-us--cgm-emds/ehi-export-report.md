# CompuGroup Medical US — CGM eMDs — EHI Export Documentation

Collected: 2026-02-15

## Source
- Registered URL: https://www.cgm.com/usa_en/products/electronic-health-records/other-ehrs/cgm-emds.html
- CHPL IDs: 11133
- CHPL Product Number: 15.04.04.2700.eMDs.10.02.1.221227
- Certification Date: 2022-12-27

## Navigation Journal

1. **Initial probe** — `curl -sI -L` to the registered URL returned HTTP 200 with `Content-Type: text/html`. The page is served via Cloudflare CDN. No redirects.

2. **Fetched and examined the page** (145 KB HTML):
   ```bash
   curl -sL "https://www.cgm.com/usa_en/products/electronic-health-records/other-ehrs/cgm-emds.html" \
     -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36' -o /tmp/cgm-emds-page.html
   ```
   The page is a product marketing page for CGM eMDs with sections: Key Benefits, Case Study, Featured Options, Learn More (contact form), and Certifications.

3. **Found the Certifications section** — an accordion labeled "CGM eMDs" at `#certifications`. When expanded (clicking the accordion header), it reveals:
   - Drummond Certified / ONC Health IT badge
   - Certification details (v10, certified 2022-12-27)
   - Criteria tested: 170.315 (a)(1-5, 12, 14-15); (b)(1-3, 9-11); (d)(1-9, 12-13); (e)(3); (f)(1, 5); (g)(2-7, 9-10)
   - Document links: API Terms of Use, CHPL Listing, Costs, **EHI Export Documentation**, FHIR API Documentation, and Real World Testing plans/results (2022-2025)

4. **Downloaded the EHI Export Documentation PDF**:
   ```bash
   curl -sL "https://www.cgm.com/_Resources/Persistent/30934b4f69192e0e12b3183761cb55c21c159630/cgm-emds-electronic-health-information-export-user-guide.pdf" \
     -H 'User-Agent: Mozilla/5.0' \
     -o downloads/cgm-emds-electronic-health-information-export-user-guide.pdf
   ```
   Verified: PDF document, 14 pages, 196 KB, dated December 2023.

5. **Downloaded the FHIR API Documentation Guide** (for comparison with EHI export):
   ```bash
   curl -sL "https://www.cgm.com/_Resources/Persistent/aaa2e921f29934f6e308b73daadaf3e94a3b21d5/fhir-api-documentation-guide.pdf" \
     -H 'User-Agent: Mozilla/5.0' \
     -o downloads/fhir-api-documentation-guide.pdf
   ```
   Verified: PDF document, 76 pages, 498 KB, dated April 2024. This is the (g)(10) FHIR API documentation — separate from the EHI export.

6. **Checked for additional EHI documentation** — no additional data dictionary files, schema files, or export-specific documentation found on the page beyond the single EHI Export User Guide PDF. The PDF contains no embedded attachments and references only external standards (hl7.org, healthit.gov).

## What Was Found

### EHI Export User Guide (Primary Document)

The **"Electronic Health Information Export User Guide for CGM eMDs"** (December 2023, 14 pages) is the sole EHI export documentation. It describes a **per-patient export** delivered as a password-protected ZIP file.

**Export format**: The export produces a ZIP file named with the pattern `Patient(lastname, firstname[AccountNumber]) YYYY-MM-DD HH-MM-SS.zip`. Inside the ZIP are:

- **~README.txt** — explanatory file
- **Chart Cover Report.xlsx** — demographics, insurance, guarantor info, current clinical summaries
- **Entire Patient Chart Report.xlsx** — all clinical visit notes, allergies, medications, problems, messages, immunizations, SDOH, education, medical/social/family/substance/mental health history
- **Health Summary Report.xlsx** — current problems, medications, allergies, past medical history, orders, health maintenance items
- **Referral Authorization Report.xlsx** — inbound/outbound referrals and authorizations
- **Trial Balance Report.rtf** — billing data: ICD/CPT codes, charges, insurance/patient payments, adjustments, balances
- **DocMan Files folder** — images, C-CDA documents, care plans, consent forms, letters, lab images, radiology images, procedure images, pregnancy history, and miscellaneous patient documents

The guide documents **27 distinct document categories** that may appear in the export, and provides **field-level detail** for each of the 5 structured files (Chart Cover Report, Entire Patient Chart Report, Health Summary Report, Referral Authorization Report, Trial Balance Report). Fields include names, data types (String, Date, Number, Image, String List), and section groupings.

### FHIR API Documentation Guide (Separate — g(10))

A 76-page guide for the FHIR R4 API, covering standard US Core resources (AllergyIntolerance, CarePlan, CareTeam, Condition, Device, DiagnosticReport, DocumentReference, Encounter, Goal, Immunization, Location, Medication, MedicationRequest, Observation, Organization, Patient, Practitioner, Procedure, Provenance, ServiceRequest). This is clearly the **(g)(10) standardized API** documentation, not the (b)(10) EHI export. The EHI export is a distinct mechanism — a ZIP file of XLSX/RTF/document files generated within the application, not a FHIR API call.

**This is a correctly-scoped (b)(10) implementation.** CGM eMDs has two separate mechanisms:
- **(g)(10)**: FHIR R4 API for standardized data access (US Core resources)
- **(b)(10)**: In-application per-patient ZIP export with comprehensive clinical, billing, and document data

## Export Coverage Assessment

### Data Domain Coverage

Comparing the export documentation against the product research:

| Data Domain | Export Coverage | Notes |
|---|---|---|
| **Patient demographics** | Covered | Chart Cover Report.xlsx: name, address, DOB, SSN, gender, marital status, phone numbers, email, employer |
| **Insurance/guarantor** | Covered | Chart Cover Report.xlsx: insurance company, policy, copay, deductible, insurance card images; guarantor demographics |
| **Clinical visit notes** | Covered | Entire Patient Chart Report.xlsx: all clinical visit notes |
| **Problem lists** | Covered | Health Summary Report.xlsx: active and inactive problems |
| **Medications** | Covered | Health Summary Report.xlsx: current and past medications with dosage, form, instructions |
| **Allergies** | Covered | Health Summary Report.xlsx: allergies and adverse reactions |
| **Immunizations** | Covered | Entire Patient Chart Report.xlsx |
| **Lab orders/results** | Partially covered | Health Summary Report.xlsx has "Orders" and "Tests and Procedures"; Lab Images in DocMan Files (HL7 format). No explicit field-level detail for discrete lab result values |
| **Vital signs** | Unclear | Not explicitly listed as a separate category. May be embedded in visit notes within Entire Patient Chart Report.xlsx |
| **Social history / SDOH** | Covered | Both Health Summary Report.xlsx (social history) and Entire Patient Chart Report.xlsx (SDOH responses) |
| **Care plans** | Covered | DocMan Files as CDA documents |
| **Referrals** | Covered | Referral Authorization Report.xlsx |
| **Authorizations** | Covered | Referral Authorization Report.xlsx |
| **Billing: charges** | Covered | Trial Balance Report.rtf: ICD codes, CPT codes, fees, units |
| **Billing: payments** | Covered | Trial Balance Report.rtf: insurance and patient payments, adjustments, balances |
| **Documents/images** | Covered | DocMan Files: images, PDFs, TIFs, scanned documents, procedure images, radiology images, lab images |
| **C-CDA documents** | Covered | DocMan Files: XML/ZIP format |
| **Patient letters** | Covered | DocMan Files |
| **Consent forms** | Covered | DocMan Files |
| **Patient messages** | Covered | Entire Patient Chart Report.xlsx |
| **Patient education** | Covered | Entire Patient Chart Report.xlsx |
| **Pregnancy history** | Covered | DocMan Files |
| **Prescribing data** | Partially covered | Medications are listed, but electronic prescription transmission records, prior authorization details, EPCS records, and PDMP query results are not explicitly mentioned |
| **Family medical history** | Covered | Health Summary Report.xlsx and Entire Patient Chart Report.xlsx |
| **Scheduling/appointments** | Not mentioned | Not part of the designated record set; not a gap |

**Notable gaps:**
- **Discrete lab results**: While lab orders appear in Health Summary Report and lab images in DocMan Files, there is no clear documentation of discrete lab result values (numeric results, reference ranges, units) being exported in a structured format. These may be in the Entire Patient Chart Report's visit notes or HL7 lab files, but this isn't explicitly documented.
- **Vital signs**: Not explicitly listed as a document category. Likely embedded in visit note data within Entire Patient Chart Report.xlsx, but not broken out with field-level detail.
- **Prescribing details**: Medication lists are covered, but detailed prescription records (Surescripts transactions, prior auth records, EPCS audit trails, PDMP query results) from the CGM PRESCRIBE module are not mentioned.
- **Procedures**: Listed as a document category for images but procedure codes/details appear only in the billing file (Trial Balance Report). Clinical procedure documentation may be embedded in visit notes.

### Export Format & Standards

The export uses a **proprietary but practical format**: password-protected ZIP containing Excel spreadsheets (XLSX), RTF text, and document files (images, C-CDA XML, HL7). This is:

- **Not FHIR** — the export is entirely separate from the FHIR API
- **Not C-CDA for structured data** — C-CDA appears only for existing care plan/CCD documents in DocMan
- **Spreadsheet-based** — the primary structured data is in XLSX files, which are widely readable
- **Document-inclusive** — the DocMan Files folder captures the full range of images, scanned documents, and electronic documents associated with the patient

The format is appropriate for an ambulatory EHR export. XLSX is universally readable and preserves tabular structure. The inclusion of DocMan Files ensures images and external documents are captured. The Trial Balance Report provides genuine billing data with charge/payment granularity.

**Relationships between files**: The files are loosely coupled. Patient Account Number appears in multiple files and could be used to join them. However, there is no explicit foreign key documentation or entity-relationship diagram.

**Could a third party reconstruct the record?** Largely yes. The export captures clinical notes, structured clinical summaries, billing data, and all document images. The main challenge would be reconstructing the temporal sequence of care from the spreadsheet format, and linking specific lab results to their orders. The export is designed for human readability rather than machine import.

### Documentation Quality

**Strengths:**
- Clear, well-organized 14-page guide with table of contents
- Field-level documentation for each export file, including data types
- Comprehensive table of 27 document categories with descriptions, locations, and file types
- Practical instructions for extracting the ZIP file (Windows and Mac)
- File naming convention documented with examples

**Weaknesses:**
- No sample data or example export files provided
- No schema files (XSD, JSON Schema, etc.) — the XLSX column structure is documented only in the PDF
- Data types are generic ("String", "Date", "Number") — no format specifications (date format, string length limits, encoding)
- No value set documentation for coded fields (e.g., what values can Patient Gender take?)
- The "Entire Patient Chart Report.xlsx" is described at a high level rather than with individual column headers, making it the least well-documented file
- No versioning or change history

### Structure & Completeness

- **Granularity**: Field-level for 4 of 5 files; high-level content description for 1 file (Entire Patient Chart Report)
- **Data types**: Specified but generic (String, Date, Number, Image, String List, Time)
- **Value sets**: Not documented
- **Relationships**: Not documented (no ERD, no foreign key documentation)
- **Coded fields**: ICD and CPT codes are referenced in the Trial Balance Report but their coding system context is implicit, not explicit
- **Versioning**: The document is dated December 2023 for v10; no change history

## Access Summary
- Final URL (after redirects): https://www.cgm.com/usa_en/products/electronic-health-records/other-ehrs/cgm-emds.html
- Status: found
- Required browser: no (PDF directly downloadable via curl; accordion content visible in HTML source)
- Navigation complexity: accordion (one click to expand Certifications section, then direct PDF link)
- Anti-bot issues: none (standard User-Agent header sufficient)

## Obstacles & Dead Ends

None. The documentation was easily accessible:
- The registered URL loads correctly and contains the certification section
- The EHI Export Documentation PDF is directly linked from the certifications accordion
- No login wall, CAPTCHA, or anti-bot protection beyond standard Cloudflare
- All downloads returned valid PDF files
