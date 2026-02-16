# Elation Health, Inc. — EHI Export Documentation

Collected: 2026-02-16

## Source
- Registered URL: https://help.elationhealth.com/s/article/EHI-Export-Criteria
- CHPL IDs: 9876 (15.04.04.2717.Elat.03.00.1.181231)
- Product: Elation EMR, Version 3
- Certification date: 2018-12-31

## Navigation Journal

1. **Initial probe**: `curl -sI -L "https://help.elationhealth.com/s/article/EHI-Export-Criteria"` returned HTTP 200 with `content-type: text/html;charset=UTF-8` but `content-length: 1`. This is a Salesforce Lightning Community site that requires JavaScript to render.

2. **Fetched raw HTML**: `curl -sL "https://help.elationhealth.com/s/article/EHI-Export-Criteria" -o /tmp/page.html` returned 407KB of Salesforce Aura framework HTML with no visible article content in the raw source. The page is a fully client-side rendered SPA.

3. **Opened in browser**: Navigated to the URL in Chrome. The page loaded successfully after JavaScript execution, rendering a Salesforce Knowledge article titled "Electronic Health Information (EHI) Export Criteria" dated Sep 18, 2024. Took a full-page screenshot.

4. **Identified the key download link**: The article body contains a link labeled "Click here to download a copy of Elation's Data Resource Table and its export formats" pointing to `https://elation.my.salesforce.com/sfc/p/37000000L9cg/a/Ui000000gb9d/iZNUvfk2RrsubsEDBM18Eyr.QSjIklWlK.afMI1bG24`.

5. **Downloaded the Data Resource Table PDF**:
   - Direct GET returns an HTML form that auto-submits via POST (Salesforce content delivery mechanism).
   - Successful download via: `curl -sL "https://elation.my.salesforce.com/sfc/dist/version/download/?oid=00D37000000L9cg&ids=068Ui000002Etmf&d=%2Fa%2FUi000000gb9d%2FiZNUvfk2RrsubsEDBM18Eyr.QSjIklWlK.afMI1bG24&operationContext=DELIVERY"` — confirmed PDF, 7 pages, 87KB.
   - Verified: `file` reports "PDF document, version 1.4, 7 page(s)", title "Elation's Designated Record Set for EHI Export", created by Google Sheets.

6. **Rendered PDF pages as images**: Used `pdftoppm -r 200 -png` to render all 7 pages for visual inspection of the table layout.

7. **Checked for additional artifacts**: The PDF contains no embedded URLs or attachments (`pdftotext` URL extraction yielded nothing; `pdfdetach -list` would show 0 files). The article links to two "Related Articles" — "21st Century Cures Act Introduction" and "C-CDA format sharing guide" — neither is specific to the EHI export mechanism, so they were not downloaded.

8. **Saved article HTML**: Extracted the rendered article body from the Salesforce DOM (the `.slds-rich-text-editor__output` element), cleaned Aura framework attributes, and saved as a standalone HTML file.

9. **Built enrichment pipeline**: Created a Bun TypeScript script to parse the PDF table into structured JSON using `pdftotext -layout` for column-position-aware extraction.

## What Was Found

Elation's EHI export documentation consists of a single Salesforce Knowledge article with an attached PDF data dictionary. The documentation is genuinely focused on the (b)(10) EHI export requirement — it explicitly references § 170.315 (b)(10), discusses the designated record set, and describes a purpose-built export mechanism rather than repackaging a FHIR API.

### Export Mechanism

**Single patient export**: Available directly in the Elation EMR UI. Users navigate to a patient's chart → More → Data Exchange → "Export Entire Health Information (EHI)" → "Export Patient EHI". The export is delivered via two emails: one with a download link (valid 6 days) and one with the password to decrypt the file. Admin-level privileges are required.

**Bulk/population export**: Practices must contact Elation support to request a population-level export. The documentation notes that "expedited exports and customized exports may include a cost for customized reports." No self-service bulk export UI is described.

### Export Format

The export uses **multiple formats** depending on the data type:
- **Computable PDF**: Used for clinical data — demographics, medications, clinical records, problem lists, vitals, allergies, visit notes, lab results, referrals, letters, imaging reports
- **XML**: Used for some clinical data alongside PDF — problem lists, procedures, vitals, allergies, and some medications share XML export
- **JSON**: Used exclusively for billing and eligibility data — bills, CPT codes, patient liabilities, payment charges, payment requests, eligibility/insurance verification
- **CSV**: Used for appointments, demographics, guarantor information, insurance details, and some clinical data

This is a proprietary, multi-format export — not FHIR, not C-CDA, not a database dump. Different data domains are exported in whichever format Elation has implemented for that domain. The documentation explicitly states that some information "might not be available in an xml or pdf format, such as rich text documents or images" and that "actual files can be reviewed in a separate download in the export."

### Data Dictionary (PDF)

The "Designated Record Set for EHI Export" PDF (dated 2/6/2024) contains a 7-page table with 4 columns:
- **Data Element** (field name)
- **Data Description** (brief description)
- **Export format indicators**: Computable PDF Export, XML Export, JSON, CSV Export

The enrichment pipeline extracted 199 data elements across these sections:

| Section | Count | Primary Format |
|---------|-------|---------------|
| Patient Demographics | 57 | Computable PDF, CSV |
| Billing - Bills | 53 | JSON |
| Billing - Patient Liability | 26 | JSON |
| Eligibility/Insurance Verification | 14 | JSON |
| Clinical Records | 9 | Computable PDF, XML |
| Guarantor Information | 9 | CSV |
| Billing - Payment Requests | 9 | JSON |
| Appointments | 6 | CSV |
| Medications | 5 | Computable PDF |
| Care Team & Documents | 3 | Computable PDF (XML in the data) |
| Additional Demographics | 2 | CSV |
| Imaging | 1 | Computable PDF |
| Patient Status | 1 | CSV |
| Social History | 1 | Computable PDF |
| Clinical Orders | 1 | Computable PDF, JSON |

### Confidential Notes Exclusion

Elation has a "Confidential Notes" mechanism that excludes certain data by default:
- Files tagged as "Keep this Confidential" (orders, visit notes) or "Mark Confidential" (reports)
- Free text in the "Notes and Chart Management" section of the Demographic Dialog
- Free text in the "Notes" section of Elation Billing

For patient-requested exports, Confidential Notes are always withheld. For provider-requested bulk exports, users can choose to include or exclude them. This is appropriately scoped to the psychotherapy notes and litigation compilation carve-outs in EHI.

## Export Coverage Assessment

### Data Domain Coverage

**Clearly covered domains:**
- Patient demographics (extensive — 57+ fields including name, DOB, gender, race, ethnicity, address, contact info, insurance, emergency contacts, preferred pharmacy, language, marital status, sexual orientation)
- Billing (highly detailed — bills with CPT codes, modifiers, ICD-10/ICD-9 diagnosis codes, charges, payments; patient liabilities with payment processing details; eligibility verification with plan details, copay, coinsurance, deductible)
- Medications (current, OTC, temporary, discontinued, permanent Rx)
- Clinical records (problem list, procedures, vitals, allergies, visit notes, lab results, referrals, letters, medical history report)
- Immunization history
- Imaging reports
- Clinical orders (lab, imaging, pulmonary, cardiac, sleep orders)
- Social history and substance use
- Care team (providers list)
- Patient-uploaded files and documents
- Messages between patient and provider
- Appointment data (type, date/time, status, description, provider, duration)
- Guarantor information for billing

**Domains with potential gaps or ambiguity:**
- **ePrescribing details**: Medications are listed, but the data dictionary doesn't explicitly include prescription routing data, pharmacy responses, EPCS records, or Surescripts transaction details. The "Current Prescriptions" and "Permanent Rx" elements may contain this, but the descriptions are vague.
- **Telehealth records**: No explicit mention of telehealth session data, though it may be captured within visit notes.
- **Patient portal interactions**: "Messages" are included, but intake forms, appointment requests, prescription refill requests from the Patient Passport portal are not explicitly listed.
- **Care plans, goals, referral tracking**: "Referrals" are listed, but the close-the-loop referral tracking, care plans, and goals mentioned in the product research are not explicitly present.
- **Clinical decision support alerts**: Not mentioned (though these are operational data, not necessarily EHI).
- **Scheduling details beyond appointments**: The product has extensive scheduling features, but appointment data in the export is basic (6 fields).
- **DPC/membership data**: The product serves Direct Primary Care practices with membership management — no mention of membership or recurring payment data in the export.
- **Custom forms and templates**: The product supports customizable templates and macros — no mention of custom form data.
- **eFax documents**: The product has an eFax platform — "Files uploaded to the patient chart" may cover these, but it's not explicit.

**Domains appropriately absent** (not EHI):
- Audit logs (not part of designated record set)
- System configuration
- Provider credentialing
- Quality metrics/aggregates
- Staff scheduling

### Export Format & Standards

The export is a **proprietary multi-format bundle** — not a recognized interoperability standard. This is acceptable for (b)(10) since no specific format is mandated, but it creates significant challenges for data portability:

- **No unified schema**: The export mixes PDF, XML, JSON, and CSV with no documented schema for any of them. The PDF data dictionary lists field names but provides no XML/JSON schemas, XSDs, or sample files.
- **Format inconsistency**: The same type of clinical data is exported differently — vitals get PDF+XML, visit notes get only PDF, billing gets JSON. There's no obvious rationale for which format is used where.
- **No relational structure**: The data dictionary is a flat list of fields without table/entity groupings, foreign key relationships, or cardinality. A field like "Patient ID" appears multiple times across different conceptual entities but there's no explicit schema linking bills to patients to encounters.
- **Import difficulty**: A receiving system would have significant difficulty reconstructing the patient record from this export without extensive reverse-engineering of the file formats.

This is **not** a (g)(10) FHIR repackaging — it's a genuine custom export. However, the lack of machine-readable schemas (JSON Schema, XSD, OpenAPI) makes it much harder to use programmatically than a standard-based export would be.

### Documentation Quality

**Strengths:**
- The documentation explicitly addresses (b)(10) by name and correctly describes the designated record set concept
- The data dictionary covers 199 data elements across clinical, demographic, and billing domains
- The Confidential Notes exclusion mechanism is thoughtfully documented
- Export instructions are clear and step-by-step for single-patient exports
- The article is publicly accessible (no login required) as required

**Weaknesses:**
- **No sample export files**: There are no example exports showing what the actual output looks like — no sample CSV, JSON, XML, or PDF files
- **No format specifications**: The data dictionary says which *format* each element uses but provides zero detail about the format structure (JSON schema? XML element names? CSV column ordering? PDF layout?)
- **No field-level data types**: The data dictionary gives "Data Element" and "Data Description" but no data types, value sets, cardinality, or constraints
- **Vague descriptions**: Many field descriptions are essentially restating the field name ("Patient date of birth" for "Date of Birth", "Patient Vitals" for "Vitals")
- **No relationship documentation**: There's no entity-relationship model or documentation of how different data elements relate to each other
- **Bulk export is opaque**: Population-level export requires contacting support — there's no self-service mechanism and no documentation of what the bulk export contains that differs from the single-patient export
- **Version/change tracking**: The PDF is dated 2/6/2024, the article dated 9/18/2024, but there's no version history or changelog

### Structure & Completeness

The data dictionary provides field-level names and descriptions for 199 elements. This is a meaningful artifact — not just a checkbox — but it's at a shallow level of detail:

- **Entity/table structure**: Partially implied by section groupings but not formally documented. The billing JSON section has a clearer hierarchical structure (Bill → CPTs → DXs, PatientLiability → Payment_charges → Payment_requests) than the clinical data.
- **Data types**: Not specified for any field. We can infer some (e.g., timestamps are "UTC", amounts are "in USD") from descriptions, but dates, codes, and free-text fields are undifferentiated.
- **Value sets/codes**: Not documented. Fields like "Billing_status", "Appointment Status", "Gender" presumably have constrained value sets, but these are not listed.
- **Coded fields**: CPT codes and ICD-10/ICD-9 diagnosis codes are mentioned in billing, but no reference to specific code systems, versions, or validation rules.

Overall, the documentation is sufficient to understand what *categories* of data the export contains, but insufficient to programmatically parse the export without access to actual sample files and reverse-engineering.

## Access Summary
- Final URL (after redirects): https://help.elationhealth.com/s/article/EHI-Export-Criteria
- Status: found
- Required browser: yes (Salesforce Lightning SPA)
- Navigation complexity: direct_link (article renders immediately; PDF download requires one click)
- Anti-bot issues: Salesforce Content Delivery requires specific URL construction for direct file download (GET → auto-POST form → actual download); the version download endpoint works with curl

## Obstacles & Dead Ends
- The raw HTML from curl is 407KB of Salesforce Aura framework code with no article content — JavaScript rendering is mandatory
- The PDF download link uses Salesforce Content Delivery (`/sfc/p/...`) which returns an HTML form that auto-submits via POST; direct GET doesn't return the file. The underlying download URL was constructed by extracting the `versionId` and `contentId` from the Salesforce document viewer page and using the `/sfc/dist/version/download/` endpoint.
- No obstacles with the article content itself — fully public, no login required
