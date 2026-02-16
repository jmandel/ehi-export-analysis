# TronsHealth LLC — EHI Export Documentation

Collected: 2026-02-15

## Source
- Registered URL: https://tronshealth.com/wp-content/uploads/2024/10/%C2%A7170.315b10-Electronic-Health-Information-Export-EHI.docx.pdf
- CHPL IDs: 11543
- Certification date: 2024-12-13
- Product version: 1.0

## Navigation Journal

Direct PDF download — no navigation required.

```bash
# Probe URL (confirms PDF, 739KB)
curl -sI -L "https://tronshealth.com/wp-content/uploads/2024/10/%C2%A7170.315b10-Electronic-Health-Information-Export-EHI.docx.pdf" \
  -H 'User-Agent: Mozilla/5.0'
# → HTTP/2 200, content-type: application/pdf, content-length: 739458

# Download
curl -sL "https://tronshealth.com/wp-content/uploads/2024/10/%C2%A7170.315b10-Electronic-Health-Information-Export-EHI.docx.pdf" \
  -H 'User-Agent: Mozilla/5.0' \
  -o 170.315b10-Electronic-Health-Information-Export-EHI.pdf

# Verify
file 170.315b10-Electronic-Health-Information-Export-EHI.pdf
# → PDF document, version 1.7, 27 page(s)
```

No embedded URLs, no embedded attachments, no links to additional documentation within the PDF.

## What Was Found

A 27-page PDF titled "§170.315(b)(10) Electronic Health Information Export (EHI)", prepared September 11, 2024 for ONC-ACB certification. The document has three main components:

### 1. Overview & Regulatory Context (pages 4-5)
A brief summary of what EHI means under HIPAA, correctly referencing the Designated Record Set definition and key requirements for individually identifiable health information.

### 2. Export Instructions with Screenshots (pages 5-9)
Step-by-step instructions for performing an EHI export through the TronsHealth web application:
1. Log in to TronsHealth
2. Navigate to the side menu → "Electronic Health Information Export"
3. Choose either a single patient or all patients
4. Select a patient from a popup list
5. Click "Export" to download a ZIP file

The export produces CSV files bundled in a ZIP archive. The documentation states: "Export data files are machine readable file formats in csv files for individual data of patients like allergies, problems, medications etc." Export is restricted to authorized/admin-level users. Practice-level permissions are required to export all patients.

### 3. Data Dictionary (pages 9-27)
Field-level documentation for 16 patient data entities, presented as tables with columns: Field, Data Type, Detail. The documented entities are:

| # | Entity | Fields | Notes |
|---|--------|--------|-------|
| 3.1 | Demographics | 52 | Comprehensive: names, DOB, SSN, address, race, ethnicity, language, gender identity, sexual orientation, alternate addresses |
| 3.2 | Medications | 28 | NDC, RxNorm, brand/generic names, sig, strength, form, route, prescriber |
| 3.3 | Allergies | 25 | Allergy name/type, RxNorm, NDC, reactions, severity, criticality, verification status |
| 3.4 | Appointments | 43 | Scheduling details, status, provider, insurance references, check-in/out, copay |
| 3.5 | Complaints | 18 | Chief complaints with SNOMED/IPC-2 codes, type, duration |
| 3.6 | Diagnosis | 15 | SNOMED/ICD-10/ICD-9 codes, verification status, linked to appointment |
| 3.7 | Documents & Images | 1 | Files exported in native format (PNG, JPEG, JPG) |
| 3.8 | Immunization | 13 | Vaccine code, amount administered, route, dates |
| 3.9 | Insurances | 32 | Member ID, payer ID, policy dates, eligibility, copay, insured party info |
| 3.10 | Contact | 22 | Emergency/related contacts with relationship, address, phone |
| 3.11 | Consent | 27 | Consent type, status, validity period, custodian party, attached documents |
| 3.12 | Education | 12 | Educational level, disability status |
| 3.13 | Patient Notes | 16 | Subject, priority, follow-up date, recall, note status |
| 3.14 | Payments | 33 | Credit card, check, and cash payments; wallet balance; transaction details |
| 3.16 | Social History | 16 | Tobacco use: status, type, frequency, duration, quit intent |
| 3.17 | Vitals | 48 | Height, weight, BP, pulse, respiration, temperature, O2 saturation, pain severity, blood type, and more |

**Critical finding: The document is truncated.** The Table of Contents lists two additional sections that are absent from the PDF:
- **3.15. Patient – Provider Note** (TOC says page 27, but page 27 is blank)
- **3.18. Patient – Encounter** (TOC says page 32, but the document only has 27 pages)

These are among the most important clinical data entities — provider notes and encounter records form the core of clinical documentation.

## Export Coverage Assessment

### Data Domain Coverage

**Covered domains (documented in the data dictionary):**
- Patient demographics (comprehensive, including USCDI-required fields)
- Medications (with NDC and RxNorm coding)
- Allergies (with RxNorm coding, severity, criticality)
- Diagnoses (with ICD-10/ICD-9/SNOMED coding)
- Immunizations
- Vital signs (extensive — 48 fields)
- Insurance/payer information
- Patient payments and billing (wallet, credit card, check transactions)
- Appointments and scheduling
- Chief complaints
- Documents and images (native file format export)
- Patient contacts/emergency contacts
- Consent records
- Social history (tobacco use)
- Patient education records
- Patient notes (administrative notes about patients)

**Missing or incomplete domains:**
- **Provider/clinical notes** — Section 3.15 is listed in the TOC but missing from the document. This is a major gap. Provider notes (progress notes, H&P, etc.) are core clinical documentation.
- **Encounters** — Section 3.18 is listed in the TOC but missing from the document. Encounter records tie together all clinical data for a visit.
- **Lab results / diagnostic reports** — Not mentioned anywhere in the data dictionary. The product research suggests lab results are at least viewable through the patient portal, so the product likely stores them. Their absence from the EHI export is a notable gap.
- **Referrals** — Not documented. If the product supports referral management, this would be missing.
- **Care plans / goals** — Not mentioned.
- **E-prescribing transmission records** — The Medications entity captures prescription data but not the electronic transmission history (e.g., pharmacy responses, refill requests).
- **CPOE orders** — The product is certified for (a)(1) CPOE for medications, but there's no separate "Orders" entity — medication orders may be captured within the Medications entity.
- **Implantable device list** — The product is certified for (a)(14) but there's no data entity for implantable devices in the export.
- **Clinical decision support alerts** — Not exported (though these may not be part of the designated record set).
- **Claims/billing beyond patient payments** — The Payments entity covers patient-side payments (copays, wallet deposits) but doesn't appear to cover insurance claim submissions, ERA/EOB data, or full billing records (CPT codes, charge amounts, claim status). For a product with practice management capabilities, this is a gap.
- **Secure messages** — The product offers secure messaging between providers and patients, but there's no entity for message content in the export.

**The (b)(10) vs (g)(10) question:** This is genuinely a (b)(10) export — it uses CSV files rather than FHIR, and it includes non-clinical data (payments, appointments, consents) that go beyond what a FHIR US Core API would cover. However, the export still has significant gaps relative to what the product appears to store.

### Export Format & Standards

- **Format:** CSV files bundled in a ZIP archive
- **Standard:** Proprietary/ad-hoc — no formal standard, which is acceptable for (b)(10)
- **Coding systems:** The data dictionary references standard coding systems (ICD-10, ICD-9, SNOMED, RxNorm, NDC) for clinical data
- **Relationships:** Entities reference each other via ID fields (e.g., PatientID, AppointmentID, ProviderNoteID in Vitals), but there's no formal schema document defining the relationships
- **Appropriateness:** CSV is a reasonable format for this ambulatory EHR. The flat file structure means some data relationships may be difficult to reconstruct, but the export is fundamentally usable

A third party could reconstruct most of a patient's record from these CSV files, though the missing Provider Note and Encounter sections are a critical gap that would leave the clinical narrative incomplete.

### Documentation Quality

**Strengths:**
- Field-level data dictionary with field name, data type, and description for every field
- Screenshots showing the actual export UI workflow
- Clear statement of the export format (CSV in ZIP)
- Covers both single-patient and all-patient export scenarios
- Each entity includes audit fields (CreatedBy, CreatedOn, ModifiedBy, ModifiedOn, IsDeleted, UUID)

**Weaknesses:**
- **Truncated document** — The most important clinical sections (Provider Note, Encounter) are missing. This strongly suggests the document was improperly converted or exported (the filename contains ".docx.pdf" — it may have been converted from Word and the conversion truncated the output).
- No sample export files or example CSV data
- No description of the ZIP file structure (folder hierarchy, file naming conventions)
- No documentation of how lookup IDs (e.g., SuffixLookupID, GenderLookupId, StatusLookupID) resolve to values — many fields are foreign key references to lookup tables, but the lookup values aren't documented
- No value set documentation for coded fields
- Data types are generic SQL-like types (varchar, long, boolean) without constraints (length limits, allowed values)
- No versioning or change history
- No documentation of character encoding, date formats, or CSV dialect (delimiter, quoting, escaping)

A developer attempting to import this data would need to reverse-engineer lookup tables, guess at CSV formatting, and would have no Provider Note or Encounter data to work with.

### Structure & Completeness

- **Granularity:** Field-level — each entity has individual field definitions
- **Data types:** Present but generic (varchar, long, boolean, datetime, decimal, int, list)
- **Descriptions:** Present for all fields, though brief and sometimes redundant with the field name
- **Coded fields:** Standard codes referenced (ICD-10, SNOMED, RxNorm, NDC) but lookup tables for internal codes are not documented
- **Relationships:** Implicit through ID fields (PatientID, AppointmentID, etc.) but not formally documented
- **Versioning:** None

## Overall Assessment

TronsHealth has made a genuine effort at (b)(10) compliance. The export is CSV-based (not a repackaged FHIR API), includes non-clinical data like payments and appointments, and has field-level documentation. This puts it ahead of vendors who simply point to their (g)(10) FHIR endpoint.

However, the documentation has significant problems:

1. **The PDF is truncated**, missing Provider Note and Encounter sections — arguably the two most important clinical entities. This appears to be a conversion error (the filename suggests it was converted from .docx to PDF).

2. **Several expected data domains are absent** from the export entirely — lab results, implantable devices, claims/billing detail, secure messages, and potentially others.

3. **The documentation lacks the detail needed for data portability** — no sample files, no lookup table definitions, no CSV format specification, no relationship documentation.

For a product certified in December 2024 (very new), this is a reasonable first effort, but the truncated document and missing data domains need to be addressed. The product appears to be a startup-stage EHR with limited market presence, and the documentation quality reflects that early stage.

## Access Summary
- Final URL (after redirects): https://tronshealth.com/wp-content/uploads/2024/10/%C2%A7170.315b10-Electronic-Health-Information-Export-EHI.docx.pdf
- Status: found
- Required browser: no
- Navigation complexity: direct_link
- Anti-bot issues: none

## Obstacles & Dead Ends
None. The URL resolved directly to a PDF download with no issues.
