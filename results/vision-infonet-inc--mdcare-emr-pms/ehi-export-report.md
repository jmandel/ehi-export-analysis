# Vision Infonet Inc — EHI Export Documentation

Collected: 2026-02-15

## Source
- Registered URL: https://www.mdcare.com/EHIexport
- CHPL ID: 11650
- Product: MDCare EMR/PMS v6.0 (certified 2025-06-04; documentation references v5.1)

## Navigation Journal

1. **Initial probe**: The registered URL `https://www.mdcare.com/EHIexport` returns HTTP 404. The server (LiteSpeed) returns a generic "404 Not Found" page with no redirects.

2. **Alternative path probing**: Tested common alternative paths on mdcare.com:
   - `/EHIexport`, `/ehi-export`, `/ehi`, `/EHI`, `/EHIExport`, `/ehi_export`, `/interoperability`, `/compliance`, `/b10`, `/onc`, `/legal` — all return 404.
   - `/pdf` returns 301 → `/pdf/` → 403 (directory listing forbidden).

3. **Homepage inspection**: Fetched `https://www.mdcare.com/` (56 KB HTML). Found a "Downloads" section with links to ONC compliance artifacts including:
   ```
   href="pdf/EHIexport.pdf" — labeled "EHI Export (b10)"
   href="pdf/APIDocument.pdf" — FHIR API documentation
   href="pdf/API.json" — FHIR endpoint JSON bundle
   ```

4. **Downloads**:
   ```bash
   curl -sL "https://www.mdcare.com/pdf/EHIexport.pdf" -H 'User-Agent: Mozilla/5.0' -o EHIexport.pdf
   # PDF document, version 1.7, 19 pages, 5,118,785 bytes

   curl -sL "https://www.mdcare.com/pdf/APIDocument.pdf" -H 'User-Agent: Mozilla/5.0' -o APIDocument.pdf
   # PDF document, version 1.5, 20 pages, 1,427,389 bytes

   curl -sL "https://www.mdcare.com/pdf/API.json" -H 'User-Agent: Mozilla/5.0' -o API.json
   # JSON text data, 3,981 bytes
   ```

5. **Wayback Machine**: Checked `web.archive.org` for captures of the registered URL in 2024 and 2025 — no archived captures found. The registered URL appears to have always been a 404; the actual documentation has always been at `/pdf/EHIexport.pdf`.

## What Was Found

### EHIexport.pdf (primary document, 19 pages)

This is the sole EHI export documentation. It is titled "§170.315(b)(10) Electronic Health Information – Export (Documentation)" and references MDCare EMR/PMS Version V5.1. Created November 29, 2023.

**Export mechanism**: The system provides a dedicated "EHI-Export" feature accessible from `Home page → Records Tab → 'EHI-Export'`. Two modes:

1. **Single Patient Export**: Search by patient name, select specific encounter(s), generates a ZIP file containing C-CDA (XML), PDF, and "all scanned clinical and administrative documents." Users can export a single encounter or all encounters for one patient.

2. **Bulk Patients Export**: Select "Multiple Patients," specify a date range, resource, and physicians. Select "Patient Demographics" and "All POS Documents" checkboxes. Generates one ZIP per patient, each containing C-CDA, PDF, XML, and scanned documents.

**Export format**: C-CDA (Consolidated CDA) per §170.205(a)(4), HL7 Implementation Guide for CDA Release 2: Consolidated CDA Templates for Clinical Notes (US Realm), DSTU R2.1 (August 2015). The export file names follow the pattern `{MRNo}-{Date}` (e.g., `1004-20231128`) in three formats: HTML, PDF, and XML. References USCDI Version 1.

**Data dictionary** (pages 12–19): Lists C-CDA sections with XPATHs, code systems, and data elements:

| C-CDA Section | Data Elements |
|---|---|
| Patient Demographics | Name, Sex, DOB, Race, Ethnicity, Preferred Language |
| Provider Info | Name, phone, address |
| Encounters | Date/location, encounter code (CPT) |
| Chief Complaint/Reason for Visit | Patient visit details/complaints |
| Diagnosis | Problem code (SNOMED/ICD-10), location, date |
| Immunizations | Vaccine (CVX/CPT-4), date, status, route, site, manufacturer, dose, lot, notes |
| Instructions | Patient instructions/follow-up reasons |
| Treatment Plan | Planned observations, dates |
| Social History | Observations, descriptions, dates |
| Problems | Problem code (SNOMED/ICD-10), status, active date |
| Medications | Medication (RxNorm/NDC), directions, start/end date, status |
| Medication Allergies | Substance, reaction, severity, status |
| Lab Tests/Results | Test code, lab info, specimen source, result type (LOINC), value, reference range, interpretation |
| Vitals | Observation (LOINC), date/time |
| Goals | Goal, value, date |
| Procedures | Procedure (CPT-4/SNOMED/HCPCS), date |
| Care Team | Name, specialty, date |
| Reason for Referral | Reason (SNOMED) |
| Medical Equipment | Implanted device (SNOMED), GMDN description |
| Mental Status | Assessment (SNOMED), date, results, comments |
| Functional Status | Assessment (SNOMED), date, results, comments |
| Health Concern | Concern/observation (SNOMED), status, date |

**UI screenshots**: The PDF includes annotated screenshots of the EHI-Export-Request window showing:
- Checkboxes for "Medical Records," "Patient Demographics," "All POS Documents"
- Message type selector: "CCD" or "Referral"
- A "C-CDA/Referral Summary" panel with ~40+ selectable data categories (Patient Name, Sex, DOB, Race, Ethnicity, Preferred Language, Medications, Medication Allergies, Social History/Smoking Status, Problems, Lab Tests, Lab Values/Results, Vital Signs, Care Plan, Procedures, Care Team Members, Provider's Info, Date and Location of Visit, Chief Complaint, Immunizations, Clinical Instructions, Future Appointments, Medication Administered, Diagnostic Pending Test, Future Scheduled Tests, Recommended Patient Decision Aids, Encounter/Final Diagnosis, Referrals, Functional and Status, MentalStatus, Assessment, Interventions, General Status, Physical Exam, Goals, Medical Device Equipment, HealthConcerns, HPI, ROS, Past Medical History, Clinical Notes)

### APIDocument.pdf (20 pages) — FHIR g(10) API documentation

This is the SMART on FHIR / FHIR R4 API documentation for the g(10) certified API. It covers:
- FHIR endpoints (production: `https://fhir.mdcare.com:9443/fhir-server/api/v4/`)
- SMART on FHIR authentication (OAuth 2.0, symmetric/asymmetric auth, public clients)
- API request examples for: Patient, AllergyIntolerance, CarePlan, CareTeam, Problems/HealthConcern, ImplantableDevice, DiagnosticReport/ClinicalNotes/DocumentReference, LabResultObservation, Goal, Immunization, Medication, SmokingStatus, Procedure, Provenance, VitalSigns
- Terms of Use

**This is the (g)(10) API, not the (b)(10) export.** It covers standard USCDI/US Core FHIR resources only. It is included here for completeness since it was linked alongside the EHI export on the homepage, but it documents a different certification criterion.

### API.json (4 KB) — FHIR Endpoint bundle

A FHIR R4 Bundle (type: collection) containing two Endpoint/Organization pairs pointing to the FHIR server at `https://fhir.mdcare.com:9443/fhir-server/api/v4/`. This is the service base URL JSON file for the g(10) API, not related to the b(10) export.

## Export Coverage Assessment

### Data Domain Coverage

The EHI export documentation describes a C-CDA-based export that covers **standard clinical data domains** but **does not address billing, practice management, or administrative data that MDCare EMR/PMS stores**.

**Clearly covered** (via C-CDA sections):
- Patient demographics (name, sex, DOB, race, ethnicity, language)
- Clinical encounters (date, location, CPT codes, diagnoses)
- Problems/conditions (SNOMED/ICD-10)
- Medications and prescriptions (RxNorm/NDC)
- Allergies (medication allergies with substance, reaction, severity)
- Lab orders and results (LOINC-coded)
- Vital signs
- Immunizations
- Procedures (CPT-4/SNOMED/HCPCS)
- Care plans, goals, health concerns
- Social history (smoking status)
- Mental and functional status assessments
- Referrals
- Implantable devices
- Clinical notes (the UI shows a "Clinical Notes" checkbox)
- Care team members
- Scanned/uploaded clinical and administrative documents (included as files in the ZIP)

**Missing or not documented**:
- **Billing data**: No mention of claims, CMS-1500 forms, superbills, accounts receivable, payment posting, denial management data. MDCare is explicitly an EMR/PMS with integrated billing. The billing module handles insurance claims, payment posting, AR, and revenue cycle management — none of this appears in the export documentation.
- **Insurance/enrollment information**: Patient insurance IDs, payer data, coverage details. The C-CDA demographics section covers basic demographic data but not insurance.
- **Scheduling/appointment data**: Not in the export (though this is borderline — see scope reference; appointment data is generally not part of the designated record set).
- **E-prescribing history**: While current medications are included via C-CDA, the Surescripts e-prescribing transaction history (prescription fills, pharmacy communications) is not mentioned.
- **Document management metadata**: The export claims to include scanned documents but doesn't describe how document metadata (document types, dates, sources, categories) is preserved.
- **Patient portal data**: Messages, portal activity, patient-submitted data — not mentioned.
- **Clinical messaging**: Inter-provider messages, staff communications about patients — not mentioned.
- **Fax records**: Integrated fax (Faxtone) records about patients — not mentioned.
- **Specialty-specific data**: MDCare markets specialty versions for cardiology, dermatology, endocrinology, psychiatry, etc. No specialty-specific clinical data structures are documented beyond what fits in standard C-CDA sections.

### Export Format & Standards

The export uses **C-CDA (Consolidated CDA)** per the 2015 edition standard (§170.205(a)(4)), referencing USCDI v1. The output is delivered as a ZIP file containing three representations of each encounter: C-CDA XML, PDF, and HTML.

This is a well-understood standard format for clinical data exchange. However, C-CDA is designed for **clinical summaries**, not for comprehensive data export. It has well-defined sections for demographics, problems, medications, allergies, labs, vitals, procedures, immunizations, and notes — but it has no native structure for:
- Billing records (claims, charges, payments)
- Insurance enrollment
- Custom assessment forms
- Specialty-specific structured data beyond what maps to standard C-CDA sections

The documentation also mentions "all scanned clinical and administrative documents" are included in the ZIP, suggesting that non-structured content (scanned images, uploaded PDFs) is exported alongside the C-CDA. This is a positive signal — it means the export captures document-level content that doesn't fit in C-CDA. However, there is no description of how these documents are organized, named, or indexed within the ZIP.

A third party could reconstruct the **clinical summary** from this export. They could not reconstruct the full patient record including billing history, insurance data, or any specialty-specific structured data that MDCare stores in its proprietary database.

### Documentation Quality

The documentation is **moderate quality**:

**Strengths**:
- Clear step-by-step instructions with annotated screenshots for both single-patient and bulk export
- A data dictionary listing C-CDA sections, XPATHs, and code systems
- The UI screenshots show a rich selection interface with ~40+ selectable data categories

**Weaknesses**:
- The document references version V5.1, but the current certified version is V6.0 (certified June 2025). The PDF was created November 2023 and may not reflect the current product.
- The data dictionary only covers C-CDA sections and data elements. There is no documentation of what "All POS Documents" includes, what document types are exported, or how the ZIP file structure is organized.
- No sample export files are provided.
- No description of how non-C-CDA data (scanned documents, administrative documents) is structured in the export.
- Field-level descriptions are minimal — the data dictionary lists element names and code systems but rarely provides descriptions, cardinality, or constraints.
- No export file format specification beyond "C-CDA, PDF, and XML formats."

### Structure & Completeness

- **Granularity**: The data dictionary provides section-level and element-level coverage with XPATHs and code systems. However, it lacks data type specifications, cardinality, optionality, and descriptions.
- **Value sets**: Code systems are identified (SNOMED, ICD-10, LOINC, RxNorm, NDC, CVX, CPT-4, HCPCS) but specific value set bindings are not documented.
- **Relationships**: Not documented — the C-CDA standard itself defines relationships between sections and entries, but this documentation doesn't describe any custom relationship handling.
- **Versioning**: None. The document appears to be a static snapshot from November 2023.

### Overall Assessment

This is a **classic (b)(10)/(g)(10) conflation case**, though with a twist. The vendor has created a dedicated EHI-Export feature (not just reusing their FHIR API), which shows genuine effort. The export uses C-CDA rather than FHIR, and includes both structured clinical data and scanned documents. However, the scope of the export is essentially a **clinical care document** — it covers the same data domains as USCDI/US Core, not the full designated record set.

The critical gap is **billing and practice management data**. MDCare EMR/PMS is explicitly an EMR **and** PMS — the "PMS" stands for Practice Management System. The product handles claims, billing, AR, payment posting, denial management, and revenue cycle operations. None of this billing data appears in the export documentation. For a product where billing is a core function (and Vision Infonet's primary business is medical billing services), this is a significant omission from the (b)(10) perspective.

The inclusion of "All POS Documents" and scanned documents in the ZIP is a positive indicator that the vendor is trying to capture non-C-CDA content, but without documentation of what this includes, it's impossible to assess its completeness.

## Access Summary
- Registered URL: https://www.mdcare.com/EHIexport → **404 Not Found**
- Actual documentation URL: https://www.mdcare.com/pdf/EHIexport.pdf (linked from homepage)
- Status: found (via homepage, not at registered URL)
- Required browser: no (direct PDF download)
- Navigation complexity: one_click (from homepage downloads section)
- Anti-bot issues: none

## Obstacles & Dead Ends
- The registered CHPL URL (`/EHIexport`) returns 404. The vendor appears to have intended this as the documentation URL but the path doesn't resolve — the actual file is at `/pdf/EHIexport.pdf`.
- Tested 12 alternative URL paths — all 404 except `/pdf` which is a forbidden directory listing.
- Wayback Machine has no captures of the registered URL.
- The EHI export PDF references MDCare V5.1 while the current certification is for V6.0 (certified June 2025), suggesting the documentation has not been updated since November 2023.
