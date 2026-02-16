# SolidPractice Technologies, LLC — EHI Export Documentation

Collected: 2026-02-14

## Source
- Registered URL: https://www.solidpractice.com/doc/SolidPractice-b10-exportable-data-content.pdf
- CHPL IDs: 10763
- Product: SolidPractice v2.0
- Certification date: 2021-12-27

## Navigation Journal

The registered URL is a direct PDF download. No navigation required.

```bash
# Probe the URL
curl -sI -L "https://www.solidpractice.com/doc/SolidPractice-b10-exportable-data-content.pdf" \
  -H 'User-Agent: Mozilla/5.0'
# Returns: HTTP/2 200, content-type: application/pdf, content-length: 29140

# Download the PDF
curl -sL "https://www.solidpractice.com/doc/SolidPractice-b10-exportable-data-content.pdf" \
  -H 'User-Agent: Mozilla/5.0' \
  -o downloads/SolidPractice-b10-exportable-data-content.pdf
# Verified: PDF document, version 1.3, 3 pages
```

The mandatory disclosures page (https://solidpractice.com/cost-limitation.php) lists three documentation links related to interoperability:
1. **Data Access API**: https://www.solidpractice.com/doc/SolidPractice-Data-Access-API.pdf
2. **Exportable Data Content (b10)**: https://www.solidpractice.com/doc/SolidPractice-b10-exportable-data-content.pdf (the registered URL)
3. **FHIR API document**: https://cdn.solidpractice.com/fhir/SolidPractice-FHIR-API-Documentation.pdf

The Data Access API PDF describes the export mechanism (an HTTP API that returns CCD XML), so I downloaded it as supplementary documentation relevant to understanding the b(10) export. The FHIR API document was not downloaded as it pertains to the (g)(10) FHIR API, not the b(10) export.

```bash
# Download Data Access API PDF
curl -sL "https://www.solidpractice.com/doc/SolidPractice-Data-Access-API.pdf" \
  -H 'User-Agent: Mozilla/5.0' \
  -o downloads/SolidPractice-Data-Access-API.pdf
# Verified: PDF document, version 1.4, 2 pages (6 logical pages)
```

## What Was Found

### Document 1: SolidPractice-b10-exportable-data-content.pdf (3 pages)

This is the core b(10) documentation. It is a single spreadsheet exported from Excel to PDF (landscape A4), created 2024-03-27. It contains a numbered list of 87 data elements organized in a table with these columns:

- **No** — sequential number (1–87)
- **Data Element** — field name
- **Data Description** — brief description of the field
- **Computable PDF Export** — marked with "X" for most fields
- **CCD XML Export** — marked with "X" for most fields
- **JSON** — marked with "X" only for item 30 (Prescriptions)

The 87 data elements cover these categories:

**Patient Demographics (1–29):** Patient ID, name components (first, last, middle, suffix), DOB, gender, race, ethnicity, marital status, language, contact method, full address, email, phone numbers (home/cell/work), and emergency contact information (name, relationship, address, phone).

**Clinical Data (30–47):** Prescriptions (current and past medications), preferred pharmacy details (name, address, city, state, zip), smoking status, social history, immunization history, problem list, procedures, vitals, allergies, primary provider, providers list (care team), lab results, lab/imaging orders, imaging reports.

**Uploaded Documents (48):** Files uploaded to the patient chart (insurance cards, consent forms, etc.).

**Insurance/Guarantor (49–65):** Primary and secondary carrier information (carrier name, subscriber ID, group number, plan name), and guarantor details (name, address, phone, relationship, city, state, zip).

**Appointments (66–71):** Appointment type, date/time, status, description, scheduled provider, duration.

**Billing/Receipts (72–87):** Receipt data including service date, copay, deductible, outstanding balance with claim number, credit account, amount, patient name and address on receipt, bill date, account number, amount paid, transaction number, payment method, billing facility name/address/contact info.

The export format columns indicate that most data elements are available in both "Computable PDF Export" and "CCD XML Export" formats. Notably, Prescriptions (#30) is the only element with a JSON export option. Lab Results (#45) and Lab/Imaging Orders (#46) appear to have marks in the CCD XML column but the marks are lowercase "x" suggesting they may be less consistently formatted. Imaging Reports (#47) has only a CCD XML export mark.

### Document 2: SolidPractice-Data-Access-API.pdf (2 pages / 6 logical pages)

This describes the Data Access API — an HTTP endpoint for exporting patient data as CCD XML. Key details:

- **Endpoint:** `https://<your-emr-baseUrl>/CCD/ExportPatientData?key={apiToken}&patientId={patientId}&<optional-parameters>`
- **Authentication:** Token-based (API key obtained from EMR Setup section)
- **Export scope:** Per-patient, with optional date range filter (`from`, `to` parameters)
- **Section selection:** An `all=true` parameter exports everything; otherwise individual sections can be toggled: allergiesAndIntolerances, medications, problem, procedures, immunizations, vitalSigns, socialHistory, results, medicalEquipment, assessment, planOfTreatment, reasonForReferral, goals, healthConcerns, functionalStatus, cognitiveStatus
- **Response format:** JSON wrapper with `success`, `data` (CCD XML string), and `message` fields
- **Date:** December 6, 2022

The API exports CCD XML data. Notably, the selectable sections are all clinical/USCDI-type data. The API does not mention exporting billing/receipt data, appointment data, insurance information, uploaded documents, or guarantor data — all of which appear in the b(10) data elements list. This suggests the CCD XML API handles the clinical subset, while the "Computable PDF Export" format may be the mechanism for exporting the full b(10) scope.

## Export Coverage Assessment

### Data Domain Coverage

Based on the product research, SolidPractice stores patient demographics, clinical notes/encounters, medications, allergies, vitals, problems, labs, imaging, referrals, prescriptions, immunizations, custom fields, appointments, billing/E&M codes, and patient portal data. Here's how the export documentation maps:

**Clearly covered:**
- Patient demographics (items 1–29) — comprehensive, including emergency contacts
- Medications/prescriptions (item 30) — current and past
- Allergies (item 42)
- Vitals (item 41)
- Problem list (item 39)
- Procedures (item 40)
- Immunizations (item 38)
- Lab results and orders (items 45–46)
- Imaging orders and reports (items 46–47)
- Social history and smoking status (items 36–37)
- Providers / care team (items 43–44)
- Insurance information (items 49–56) — primary and secondary
- Guarantor information (items 57–65)
- Appointments (items 66–71)
- Billing receipts (items 72–87) — service dates, payments, claims
- Uploaded documents (item 48) — insurance cards, consent forms, etc.
- Preferred pharmacy (items 31–35)

**Missing or unclear:**
- **Clinical notes / encounter documentation** — This is the product's core feature (voice-dictated notes are SolidPractice's signature capability). There is no explicit data element for encounter notes, progress notes, or dictated text. This is a significant gap — the product's most distinctive data type appears absent from the export.
- **Referral letters** — The product generates automated referral letters, but these are not listed as an exportable data element. "reasonForReferral" exists in the CCD XML API but not as a distinct field in the b(10) list.
- **Drug interaction data** — Not mentioned in the export.
- **Clinical quality measure data** — Not mentioned.
- **Patient portal data** — Not mentioned (messages, access logs, etc.).
- **Custom fields** — The product supports custom data field creation, but no mechanism for exporting these is documented.
- **E/M coding** — The billing/receipt section covers payment amounts but not CPT/ICD codes, E/M levels, or detailed claims data. Only "receipt" fields (copays, deductibles, balances, payment methods) are listed — not the underlying diagnosis or procedure codes that drive billing.
- **Direct messaging / C-CDA exchange history** — Not mentioned.
- **Syndromic surveillance data** — Not mentioned.
- **Telehealth session data** — Not mentioned.

The export is notably stronger on administrative/financial data (insurance, guarantor, appointments, receipts) than many vendors, but the absence of clinical encounter notes — the very heart of what this EHR stores — is a glaring omission.

### Export Format & Standards

SolidPractice offers three export formats:
1. **Computable PDF Export** — used for nearly all 87 data elements. The format is not further described; it's unclear whether this is a structured PDF (with form fields or tagged content) or simply a rendered document.
2. **CCD XML Export** — used for most clinical data elements. The Data Access API document describes an HTTP endpoint that returns CCD (Continuity of Care Document) XML wrapped in a JSON response. CCD is a well-established C-CDA standard.
3. **JSON** — listed only for Prescriptions (#30). No further specification is provided for the JSON format.

The CCD XML export covers only the clinical data subset (the 16 selectable sections in the API map to standard C-CDA sections). It does not cover billing, appointments, insurance, uploaded documents, or guarantor data. The "Computable PDF Export" appears to be the catch-all format for the full b(10) scope.

The use of CCD XML for clinical data is appropriate and standards-based. However, the reliance on "Computable PDF" for the broader export raises questions — PDF is generally not a computable format (despite the "computable" label). If the PDF is simply a rendered printout, a third party would have difficulty programmatically importing the data. No schema, sample files, or structural specification is provided for any of the formats.

### Documentation Quality

The documentation is minimal but functional:
- The b(10) data element list is clear and enumerated — 87 fields with brief descriptions
- The Data Access API has enough detail for a developer to make API calls (endpoint, parameters, authentication, response format, error examples)
- However, there are no data type specifications (what format is Date of Birth? What are the valid values for Gender? What coding systems are used?)
- No value sets or code systems are documented for coded fields
- No sample export files are provided
- No field-level cardinality (required vs. optional) is documented
- The "Computable PDF Export" format is completely undocumented beyond its name
- The documentation is sparse enough that it looks like a compliance checkbox exercise, but it does cover a broader scope than many vendors

A developer could use the CCD XML API based on the documentation, but would not be able to fully parse or validate the export without additional information about the PDF format and coded field values.

### Structure & Completeness

- **Granularity:** Field-level listing with brief descriptions, but no data types, constraints, or value sets
- **Coded fields:** Not documented with their value sets (e.g., Gender, Race, Ethnicity, Marital Status, Appointment Status, Payment Method — all presumably coded but no enumerations given)
- **Relationships:** Not documented (e.g., how receipts link to appointments, how orders link to results)
- **Versioning:** The b(10) PDF was created 2024-03-27; the Data Access API PDF is dated 2022-12-06. No version numbers or change history.
- **Machine-readable artifacts:** None. No JSON schema, XSD, OpenAPI spec, or sample files are provided.

## Access Summary
- Registered URL: https://www.solidpractice.com/doc/SolidPractice-b10-exportable-data-content.pdf
- Final URL (after redirects): same (no redirects)
- Status: found
- Required browser: no
- Navigation complexity: direct_link
- Anti-bot issues: none

## Obstacles & Dead Ends

None. The URL worked as a direct PDF download with no issues. The mandatory disclosures page was also accessible and provided additional context. The FHIR API documentation (https://cdn.solidpractice.com/fhir/SolidPractice-FHIR-API-Documentation.pdf) was not downloaded as it pertains to g(10) FHIR API, not the b(10) EHI export.
