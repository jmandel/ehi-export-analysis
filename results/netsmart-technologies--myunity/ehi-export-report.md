# Netsmart Technologies — myUnity EHI Export Documentation

Collected: 2026-02-16

## Source
- Registered URL: https://www.ntst.com/lp/certifications
- CHPL IDs: 11409
- Product: myUnity (version 2023)
- Certification date: 2023-12-18

## Navigation Journal

1. **Probed the registered URL** with `curl -sI -L https://www.ntst.com/lp/certifications` — returned HTTP 200, Content-Type text/html, 189KB page. This is Netsmart's main certifications hub for all products.

2. **Fetched and searched the page** for EHI-related links:
   ```bash
   curl -sL "https://www.ntst.com/lp/certifications" -H 'User-Agent: Mozilla/5.0' -o /tmp/ntst-certifications.html
   grep -oiE 'href="[^"]*"' /tmp/ntst-certifications.html | grep -iE 'ehi|export|myunity'
   ```
   Found product-specific EHI pages including `/lp/certifications/ehi-all-data-myunity`.

3. **Navigated to the myUnity EHI page**: `https://www.ntst.com/lp/certifications/ehi-all-data-myunity`
   - Page title: "EHI (Electronic Health Information) All Data Export"
   - Subheading: "EHI (Electronic Health Information) All Data Export for myUnity® and myUnity® Senior Living"
   - Page describes the export as a "manual one-time export of health data for one or more patients" in "computable, JSON file format native to myUnity"
   - Single "CLICK HERE" link to the PDF data dictionary

4. **Downloaded the PDF data dictionary**:
   ```bash
   curl -sL "https://www.ntst.com/-/media/pdfs/certifications/ehi_export_all_files_myunity_fall_2024.pdf" -H 'User-Agent: Mozilla/5.0' -o ehi_export_all_files_myunity_fall_2024.pdf
   ```
   Verified: `file` reports "PDF document, version 1.7, 64 page(s)", 467KB. Created by Microsoft Word, dated 2024-08-26.

5. **Examined the PDF** with `pdftotext` — clean text extraction. Full data dictionary with field-level documentation for 23 export files.

6. **Checked for additional links** on the EHI page. Found two non-EHI links:
   - Netsmart Developer Portal (https://careconnect-uat.netsmartcloud.com/) — for FHIR API integration, separate from EHI export
   - Information Sharing page (https://www.ntst.com/lp/information-sharing) — general integration contact info
   Neither contains additional EHI export documentation.

7. **Checked the mandatory disclosures PDF** (`myunity-certification-status-letter_mandatory-costs-disclosures_01-02-2025.pdf`) — lists (b)(10) EHI Export as an included capability at no additional cost, but contains no technical documentation.

8. **Ran enrichment** — parsed the PDF into structured JSON with `bun run extract-data-dictionary.ts`, producing `data-dictionary.json` with all 23 files and 404 fields.

## What Was Found

### Export Format

The myUnity EHI export produces **JSON files inside a ZIP archive**, one ZIP per patient. This is a proprietary, vendor-native format — not FHIR, C-CDA, or any external standard. The export is described as a "manual one-time export" that an organization initiates for one or more patients.

The page explicitly distinguishes this EHI export from the FHIR API (used for (g)(10) integrations) and directs developers interested in integration to the separate Developer Portal. This clear separation is a positive sign — Netsmart is not conflating (b)(10) with (g)(10).

### Export Files (23 total)

The export produces 23 distinct files per patient, each as a separate JSON file:

| # | File | Fields | Domain |
|---|------|--------|--------|
| 1 | **Demographics** | 29 | Patient demographics (name, DOB, SSN, race, ethnicity, language, gender identity, pronouns, etc.) |
| 2 | **CCD** | — | C-CDA XML document with 19 clinical sections (allergies, meds, problems, labs, vitals, immunizations, procedures, care team, etc.) |
| 3 | **FamilyHealthHistory** | 8 | Family member health conditions with SNOMED coding |
| 4 | **HealthInsurance** | 15 | Insurance plans, coverage, policy numbers, eligibility |
| 5 | **Referrals** | 36 | Admissions and referrals with source, status, care setting, discharge details, location history |
| 6 | **ResponsibleParties** | 21 | Related parties with addresses, phone numbers, and relationships |
| 7 | **CensusAdvanceDirectives** | 12 | Advance directives with type, dates, ordering physician |
| 8 | **AssessmentandPlanOfTreatment** | 14 | Goals and interventions with form/chart status |
| 9 | **Consents** | 9 | Consent forms with descriptions and captured values |
| 10 | **Attachments** | — | Raw files (PDF, DOC, XLS, JPG, PNG, GIF, TIF, BMP, TXT, RTF, XML) |
| 11 | **Documents** | 9 | Document metadata with base64-encoded document content |
| 12 | **PatientNotes** | 27 | Clinical/administrative notes with categories, lock status, follow-up, addenda |
| 13 | **Orders** | 37 | Physician orders (medications, advance directives) with dose, route, schedule, diagnoses |
| 14 | **OrderAdministrations** | 41 | Medication administration records with physical monitors (vitals at administration) |
| 15 | **Claims** | 29 | Claims/invoices with payer, charges, payments, adjustments, CBSA, certification periods |
| 16 | **ClaimCharges** | 18 | Charge details with CPT/HCPCS, revenue codes, modifiers, amounts |
| 17 | **ClaimChargeAdjustments** | 10 | Payment/adjustment transactions with type and batch |
| 18 | **RegulatoryAssessment** | 14 | MDS, OASIS, and Hospice Item Set assessments with ASCII/XML submission strings |
| 19 | **EventADTs** | 5 | ADT events (admit/discharge/transfer) with message type and timestamp |
| 20 | **Appointments** | 10 | Scheduled/completed appointments with service and status |
| 21 | **Eligibility** | 14 | Insurance eligibility verification requests and results |
| 22 | **Authorization** | 20 | Insurance authorization details with quantities and time periods |
| 23 | **NonRegulatoryAssessment** | 26 | Non-regulated assessments with question/answer pairs (e.g., custom clinical assessments) |

### Documentation Detail

Each export file is documented with:
- **File-level description** of what the file contains
- **Field-level definitions** with name, data type, and description
- Data types include: String, Integer, Date, Time, Timestamp, Boolean, Number, Money, Decimal, Array, Base64 encoded binary, Date/Time
- Descriptions are generally clear and actionable, explaining what each field represents and how it relates to the clinical workflow
- The CCD file references USCDI v1 and the ONC 2015 Cures Update standard
- Regulatory assessments include the raw ASCII/XML submission strings used for CMS reporting

### Key Design Decisions

- **Patient linkage**: `PatientID` is the primary cross-file join key, described as the MRN
- **Admission linkage**: `AdmissionID` links referrals and order administrations to specific admissions
- **Invoice linkage**: `InvoiceSys` joins Claims, ClaimCharges, and ClaimChargeAdjustments
- **Nested structures**: NonRegulatoryAssessment and RegulatoryAssessment use arrays with dot-notation field names (e.g., `AssessmentDocumentID.HumanReadableValue`)
- **Raw document export**: Both Attachments (raw files) and Documents (base64-encoded in JSON) are included

## Export Coverage Assessment

### Data Domain Coverage

**Well-covered domains:**

- **Demographics**: Comprehensive — 29 fields covering name, DOB, SSN, race, ethnicity, language, gender identity, pronouns, military status, employment, education, death date/time. Strong coverage of USCDI demographic requirements.
- **Clinical data via CCD**: The C-CDA document covers allergies, medications, problems, procedures, immunizations, labs, vitals, care team, encounters, goals, social history — the standard USCDI clinical summary. However, this is a structured summary, not raw clinical data.
- **Orders and medication administration**: Detailed — 37 order fields and 41 administration fields including scheduling, physical monitors (vitals), follow-ups, and notes. Good eMAR representation.
- **Billing/claims**: Strong — three linked files (Claims, ClaimCharges, ClaimChargeAdjustments) with 57 total fields covering invoices, CPT/HCPCS codes, revenue codes, modifiers, charges, payments, adjustments, authorizations, and payer details. This is genuinely comprehensive billing data, not just a summary.
- **Assessments**: Two separate files for regulatory (MDS/OASIS/Hospice Item Sets with raw CMS submission data) and non-regulatory assessments (question/answer pairs). The regulatory assessment includes the full ASCII/XML submission string — essentially the complete assessment content.
- **Insurance**: Covered across HealthInsurance (15 fields), Eligibility (14 fields), and Authorization (20 fields).
- **Notes**: 27-field PatientNotes file with categories, alerts, locking, addenda, and follow-ups.
- **Documents/attachments**: Both raw file attachments and document repository content with base64 encoding.
- **Referrals/admissions**: 36-field Referrals file covering the full admission lifecycle from referral through discharge.
- **Advance directives**: Dedicated file with 12 fields.
- **Consents**: 9-field file for consent forms.
- **Care plans**: AssessmentandPlanOfTreatment includes goals and interventions.

**Potentially missing or underrepresented domains:**

- **Vital signs as discrete data**: Vitals appear in the CCD (structured summary) and as physical monitors within OrderAdministrations, but there is no dedicated vitals file with time-series vital sign observations. For a post-acute care platform, discrete vital sign tracking is clinically important.
- **Allergies as discrete data**: Only present within the CCD; no separate structured allergy file.
- **Diagnoses/problem list as discrete data**: Only in the CCD. The Orders file has `Order_RelatedDiagnoses` but there's no standalone diagnosis file.
- **Immunizations as discrete data**: Only within the CCD.
- **Lab results as discrete data**: Only within the CCD.
- **Wound care documentation**: For a post-acute/home health platform, wound care is a major clinical workflow (measurements, staging, photos). Not explicitly present beyond what may be captured in non-regulatory assessments or notes.
- **ADL tracking**: Activities of daily living are core to SNF and senior living. May be captured in regulatory assessments (MDS includes ADL data in the XML string) but not as discrete data.
- **Dietary/nutrition records**: Not present as a dedicated export.
- **Therapy notes**: Physical, occupational, speech therapy documentation is not a distinct file (though may be in PatientNotes or NonRegulatoryAssessment).
- **Electronic Visit Verification (EVV)**: myUnity has EVV via Mobile Caregiver+; EVV records are not explicitly in the export.
- **Telehealth session records**: Not present.
- **Scheduling/visit details**: Appointments file covers scheduled appointments, but the detailed visit documentation workflow data (visit notes, time in/out for home health visits) is not explicit beyond what's in PatientNotes.

**Important nuance on CCD coverage**: Many "missing" clinical data domains (allergies, problems, meds, labs, vitals, immunizations, procedures) ARE exported — but within the CCD XML document, not as separate queryable JSON files. This means the data is present but in a standards-based summary format that may not capture every historical entry, custom field, or vendor-specific detail. The CCD is based on USCDI v1 / C-CDA R2.1, which has known limitations for data fidelity compared to the native EHR data model.

### Export Format & Standards

- **Primary format**: Vendor-native JSON files in a ZIP archive — a reasonable choice for (b)(10) since it captures the actual data model
- **Secondary format**: C-CDA XML for the CCD file (standardized clinical summary)
- **Attachments**: Raw files exported as-is (multiple file types supported)
- **Documents**: Base64-encoded within JSON
- **Regulatory assessments**: Include the actual CMS submission strings (ASCII/XML), which is excellent — these are the definitive regulatory records

The JSON format is proprietary but well-documented. Field names are descriptive. Data types are specified. Cross-file relationships are documented through shared IDs. A developer could implement an import of this data using only the PDF documentation.

### Documentation Quality

**Strengths:**
- Clear, consistent structure across all 23 files
- Every field has a name, type, and description
- File-level descriptions explain purpose
- Glossary defines common cross-file fields (PatientSys, PatientID, Patient_DisplayName)
- Explicit variability disclaimer acknowledging organization-specific differences
- Clear separation from FHIR API documentation (no (b)(10)/(g)(10) confusion)

**Weaknesses:**
- No sample data or example export files provided
- No value set documentation for coded fields (e.g., what are the possible values for `Order_Status`, `Patient_AdmissionStatus`, `Appointment_Status`?)
- No explicit schema files (JSON Schema, OpenAPI) — only the PDF
- No documentation of the ZIP structure (naming conventions, directory layout)
- No versioning or change history beyond "Last Updated: 08/15/2024"
- Relationship diagrams between files would help (e.g., how Claims → ClaimCharges → ClaimChargeAdjustments join)
- The PDF format is not ideal for a data dictionary — a CSV, JSON Schema, or HTML table would be more machine-readable

### Structure & Completeness

- **Granularity**: Field-level documentation with names, types, and descriptions — above average for EHI export documentation
- **Value sets**: Not documented. Coded fields like status, type, and category fields lack enumerated possible values
- **Relationships**: Implicitly documented through shared IDs (PatientID, InvoiceSys, Order_ID) but not formally diagrammed
- **Cardinality**: Not explicitly documented. Arrays are mentioned (NonRegulatoryAssessment) but 1:N relationships are mostly implied
- **Versioning**: Single version date (08/15/2024). No change log

## Overall Assessment

Netsmart's myUnity EHI export documentation is **above average** for the industry. Key positive findings:

1. **Genuine (b)(10) export**: This is clearly a purpose-built EHI export, not repackaged FHIR API documentation. The JSON-in-ZIP format exports native data structures.
2. **Broad data coverage**: 23 export files spanning demographics, clinical notes, orders, medication administration, billing (claims/charges/adjustments), assessments (both regulatory and non-regulatory), insurance, and documents/attachments.
3. **Billing data included**: Three linked billing files with CPT codes, revenue codes, and payment transactions. Many vendors omit billing entirely.
4. **Regulatory assessments preserved**: MDS, OASIS, and Hospice Item Sets are exported with their full CMS submission strings — the most complete representation possible.
5. **Good field-level documentation**: 404 fields across 23 files, each with type and description.

Key concerns:

1. **CCD dependency for core clinical data**: Allergies, problems, medications, labs, vitals, and immunizations appear to be exported only within the CCD (a clinical summary), not as discrete vendor-native JSON. This means the richest clinical data may be limited to what USCDI v1 covers, while the vendor's native data model likely contains more detail (custom fields, historical entries, vendor-specific extensions).
2. **No sample data**: Without example exports, it's hard to verify that the documentation matches reality.
3. **Missing value sets**: Coded fields lack enumerated values, making import implementation harder.
4. **Post-acute specialty gaps**: For a platform serving home health, hospice, SNF, and senior living, some domain-specific data may be underrepresented (wound care, ADLs, EVV, therapy-specific notes) — though these could be captured within the generic assessment and notes structures.

## Access Summary
- Final URL (after redirects): https://www.ntst.com/lp/certifications/ehi-all-data-myunity
- Status: found
- Required browser: no
- Navigation complexity: one_click (from certifications hub to product-specific EHI page)
- Anti-bot issues: none

## Obstacles & Dead Ends
- None. The documentation was straightforward to find and download. The certifications page clearly organizes EHI documentation by product with dedicated pages per product line.
