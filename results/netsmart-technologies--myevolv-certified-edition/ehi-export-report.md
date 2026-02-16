# Netsmart Technologies — myEvolv Certified Edition — EHI Export Documentation

Collected: 2026-02-16

## Source
- Registered URL: https://www.ntst.com/lp/certifications
- CHPL IDs: 11131
- CHPL Product Number: 15.04.04.2816.myEv.11.02.1.221227
- Certification Date: 2022-12-27

## Navigation Journal

1. **Probed the registered URL** with curl — returned HTTP 200, Content-Type text/html, ~190KB. The page is server-rendered but content is in the DOM.

2. **Loaded the page in a browser** at `https://www.ntst.com/lp/certifications`. The page is Netsmart's main ONC certifications hub covering all their certified products (myAvatar, myEvolv, myUnity, GEHRIMED, TheraOffice, etc.).

3. **Found the EHI section**: Under the heading "EHI (Electronic Health Information) All Data Export", there are separate links for each product. Clicked the **"myEvolv®"** link, which navigated to:
   ```
   https://www.ntst.com/lp/certifications/ehi-all-data-myevolv
   ```

4. **The EHI page** describes the export functionality and contains a prominent "CLICK HERE" link to download documentation:
   ```
   curl -sL "https://www.ntst.com/-/media/pdfs/certifications/myevolv-all-ehi-export-documentation_v2.zip" \
     -H 'User-Agent: Mozilla/5.0' \
     -o myevolv-all-ehi-export-documentation_v2.zip
   ```
   This returned a 11.1 MB ZIP file.

5. **Also downloaded the certification status letter** linked from the main certifications page:
   ```
   curl -sL "https://www.ntst.com/-/media/pdfs/certifications/myevolv_certification_status_letter_040425.pdf" \
     -H 'User-Agent: Mozilla/5.0' \
     -o myevolv_certification_status_letter_040425.pdf
   ```

6. **Extracted the ZIP** containing three files:
   - `(1) myEvolv All EHI Export Companion Guide.docx` (939 KB) — comprehensive user guide
   - `(2) myEvolv All EHI Export Data Dictionary Crosswalk.xlsx` (11.2 MB) — massive data dictionary with 5 sheets
   - `(3) myEvolv ALL EHI Export Queries.sql` (6 KB) — SQL queries for agencies to discover their own forms/events

7. **Took a full-page screenshot** of the EHI export page.

## What Was Found

Netsmart provides a dedicated, purpose-built EHI export tool for myEvolv that is clearly designed for (b)(10) compliance. This is **not** a repurposed FHIR API or USCDI export — it is a native data extraction system that exports the full breadth of clinical, administrative, and specialty data stored in myEvolv's SQL Server database.

### Export Mechanism

The export uses myEvolv's "Print Bundle" infrastructure. An administrator configures a "Full EHI Export" template that lists all event types and forms eligible for export. The process:

1. Navigate to Reports > All EHI Exports > EHI Export
2. Select "Full EHI Export" template
3. Choose parameters (all clients or specific clients)
4. Run the export (asynchronous, can take significant time)
5. Output is deposited as ZIP files to a configured directory (local path for self-hosted, SFTP for Netsmart-hosted)

### Export Format

The export produces **JSON files** packaged in ZIP archives. Key characteristics:

- **File naming**: `EHI_Export_MMDDYYYYHHMM.zip` containing `Bulk_Bundle_ID_N.json` files
- **Structure**: Each JSON file contains arrays of records. Individual records correspond to form entries or events in myEvolv.
- **Record identification**: Each record has `x_form_code` (form identifier), `people_id` (patient), `key_value` (unique record ID), and for events, `event_definition_id`.
- **Size-limited**: Individual JSON files are capped at a size limit; a patient's data may span multiple files.
- **Sorted by event type**: Records are grouped by event type across files.

**Data types in JSON**:
- Strings, dates (ISO 8601), booleans, numeric values
- Foreign key fields include both the GUID (`field_id`) and human-readable description (`field_id_desc`) and prompt (`field_id_prompt`)
- **Attachments/images**: Base64-encoded with MIME type (`field_base64`, `field_mimeType`)
- **Signatures**: Base64-encoded images
- **Progress notes**: Nested arrays with note ID, content, author, duration, dates
- **Subforms**: Nested arrays within parent records (e.g., allergy reactions within an allergy record)
- **Assessments/tests**: Nested structures with questions, answers, scores, and field type codes

### Data Dictionary

The XLSX data dictionary crosswalk is remarkably comprehensive:

| Sheet | Rows | Description |
|-------|------|-------------|
| Info | 4 | Metadata about the crosswalk |
| Events | 1,679 | All event definitions (date-based clinical records) |
| Events + Columns | 115,663 | Field-level detail for all events including subforms and assessments |
| Non-Events | 250 | Non-event forms (demographics, static records) |
| Non-Events + Columns | 21,006 | Field-level detail for non-event forms |

**Total: ~138,600 field-level entries** across events and non-events.

The crosswalk represents a "freshly installed myEvolv instance" and does not include user-defined events, which agencies can discover using the provided SQL queries.

### SQL Queries

Four T-SQL queries are provided that can be run against the myEvolv database:
1. **Events**: Lists all people-based events eligible for EHI export
2. **Events + Columns**: Field-level detail for each event
3. **Non-Events**: Lists non-event forms
4. **Non-Events + Columns**: Field-level detail for non-event forms

These allow agencies to generate their own crosswalk including custom forms/events.

### Type Code Legend

The companion guide includes a comprehensive type code legend mapping 50+ data type codes to their SQL types (e.g., FK = Foreign Key/uniqueidentifier, SF = Sub Form, M = Memo/varchar(max), DT = DateTime, etc.).

### Glossary

A detailed glossary defines 35+ common field names found in event-based records (e.g., `event_log_id`, `belongs_to_event`, `service_track_event_id`, `program_providing_service`, etc.) with explanations of their meaning in the myEvolv data model.

## Export Coverage Assessment

### Data Domain Coverage

The export documentation reveals an **exceptionally broad** coverage of data domains. With 119 event categories and 87 unique database tables, the export encompasses virtually everything myEvolv stores about patients.

**Clearly Covered Domains** (with specific event categories/tables):

| Domain | Evidence |
|--------|----------|
| **Demographics** | 250 non-event forms including Personal Information, address, race, ethnicity, language, contact info, identifiers |
| **Diagnoses** | "Diagnosis" event category, `diagnosis_data` table |
| **Medications** | "Medication History", "Medication Administration", "Standing Orders" categories; `medication_history`, `medication_administered_history`, `standing_orders` tables |
| **Allergies** | "Allergies" category, `people_allergies` table |
| **Immunizations** | "Immunizations" category, `immunization_history` table |
| **Lab Tests** | "Lab Tests" category, `lab_tests` table |
| **Vital Signs/Physical Characteristics** | "Physical Characteristics" category, `physical_characteristics` table; detailed example in companion guide shows height, weight, BMI, BP, pulse, respiration, temperature, SpO2, etc. |
| **Problems/Needs** | "Problems/Needs" category, `problems` table |
| **Progress Notes** | "NYSCRI Progress Notes", "Care Manager Notes" categories; nested progress note arrays in export |
| **Treatment/Service Plans** | "Treatment/Service Plans for People", "Treatment/Service Plans for Profiles", "Service Plan Development", "Service Plan Addendum" categories; `service_plan_header`, `service_plan_development`, `service_plan_addendum` tables |
| **Assessments/Tests** | "Test/Assessments for People", "MSDP Tests and Assessments", "NYSCRI Test and Assessments", "HCBS Test/Assessments", "Family Case Test/Assessment" — extensive assessment infrastructure |
| **Consents** | "Consents", "System Consents" categories, `consents` table |
| **Incidents** | "Incidents Header", "Incident Medical Exam", "Incident Medications", "Incident Physical Findings", "Incident Restraints" — 5 separate categories; `incident_header`, `incident_medical_exam`, etc. |
| **ABA/Autism Services** | "ABA Data Collection", "ABA Service", "ABA Session" categories; `aba_data_collection`, `aba_session` tables |
| **Substance Use** | "Substance Use" category, `substance_use_history` table |
| **Behavioral Monitoring** | "Behavioral Monitoring Activities", "Behavioral Monitoring Activities - Other" categories |
| **Foster Care** | "Adoption Activities", "Placement Disruptions", "Placement and Treatment History", "Permanency Plan Goals" categories |
| **Referrals** | "Referrals Made", "Referrals Made Status", "Referrals to Agency" categories; `referrals_made`, `referrals_made_status`, `referrals_to_agency` tables |
| **Enrollment/Placement** | "Program Enrollment", "Benefit Assignment", "Service Track - Agency Placement", "Memberships/Placement in Profiles" categories |
| **Billing-Adjacent Data** | "Authorization Requests", "Income Information", "Monthly Income", "Resources and Liabilities" categories; `authorization_requests`, `income_history`, `monthly_income`, `resource_liability_data` tables; benefit assignments and program enrollment tracked |
| **Legal History** | "Legal History for People", "Legal History for Profiles" categories |
| **Smoking Status** | "Smoking Status" category, `smoking_status` table |
| **Pregnancy** | "Pregnancy", "Primary Birth Control" categories |
| **Employment** | "Employment History" category, `employment_history` table |
| **Marital History** | "Marital History" category, `marital_history` table |
| **Disclosures** | "Disclosures" category, `disclosure` table |
| **Letters/Documents** | "Letters", "Received Documents" categories |
| **Evidence-Based Practice** | "Evidence Based Practice" category |
| **Restrictions/Alerts** | "Restrictions/Alerts" category, `restrictions` table |
| **Outreach** | "Outreach Header" category |
| **Worker Assignments** | 4 separate categories for Case, Client, Profiles, Referral assignments |
| **Public Health** | "Public Health Activities", "Public Health Encounters", "Public Health Tests/Assessments" |
| **State Reporting** | "State Reporting Forms", "State Reporting Requirements", "State Reporting Agency Specific Records" |
| **Images/Attachments** | Base64-encoded in export; explicit handling for documents, images, signatures |
| **E-Signatures** | "eSignature" category; base64-encoded signature images in export |

**Notably Present — Specialty/BH-Specific Data**:
- ABA data collection (interval recording, session data)
- MST (Multisystemic Therapy) events
- NYSCRI and MSDP state-specific documentation
- CCBHC-related assessments
- Methadone/MAT demographics forms
- Foster care/adoption activities
- Incident management with restraints, medications, physical findings
- HIV status history
- Behavioral monitoring

**Potential Gaps**:
- **Billing claims/charges**: While authorization requests, income, benefit assignments, and program enrollment are covered, I do not see explicit "claims", "charges", "payments", or "billing" event categories in the export. The certification status letter mentions billing capabilities, and the product has extensive billing/revenue cycle features. The financial data present (authorization requests, income, benefit assignments) is patient-adjacent billing data, but the actual claims/charges/payments/AR data may not be exported. This could be a significant gap given that billing records are part of the designated record set.
- **Scheduling/appointments**: There is no explicit scheduling/appointment category. While this is borderline EHI (scheduling data is generally operational), service events inherently capture date/time/duration information that documents encounters.
- **Telehealth session records**: No explicit telehealth category, though telehealth encounters may be captured as regular activities/events.
- **Group therapy session notes**: "Group Activities" and "Group Activities - Other" categories exist, which likely cover this.

### Export Format & Standards

The export uses a **proprietary JSON format native to myEvolv** — this is not FHIR, C-CDA, or any recognized standard. This is entirely appropriate for a (b)(10) export:

- The JSON structure directly reflects myEvolv's internal data model (events, forms, subforms, assessments)
- Foreign key fields include both GUIDs and human-readable descriptions, making the data interpretable without access to the source system
- Binary data (images, documents, signatures) is base64-encoded inline
- The format is computable and parseable by any JSON-capable tool
- The data dictionary crosswalk provides the key to interpreting the export structure

**Could a third party reconstruct the patient record?** Yes, largely. The combination of:
1. The JSON export with `_desc` fields for all foreign keys
2. The 138,600-row data dictionary crosswalk
3. The companion guide with worked examples and type code legend
4. The glossary of common field names

...provides sufficient context to understand what each record represents and how records relate to each other. The `people_id` links records to patients, `belongs_to_event` shows event nesting, and `x_form_code` maps to the crosswalk.

### Documentation Quality

**Strengths**:
- The companion guide is well-written and thorough, with step-by-step configuration instructions, annotated JSON examples, a complete type code legend, and a glossary of terms
- The data dictionary crosswalk is massive (138K+ rows) and covers the full breadth of the system's forms and events at the field level
- The SQL queries allow agencies to generate their own crosswalk including custom content
- The documentation clearly distinguishes event-based vs. form-based records and explains the export structure
- Worked examples with color-coded annotations show how to interpret the JSON output
- Last updated November 2024 — recently maintained

**Weaknesses**:
- The DOCX format for the companion guide is less accessible than HTML or PDF (though the content is high quality)
- No sample export JSON file is provided as a standalone artifact (examples are embedded in the DOCX)
- The data dictionary notes that it represents a "freshly installed" system and may not match a specific agency's configuration — agencies must run the SQL queries to get their actual data dictionary
- Relationship documentation between tables is implicit (via foreign keys with `_desc` suffix) rather than explicit (no ERD or relationship diagram)
- Value sets/code lists are not documented — FK fields show "Foreign Key ID" as the type but don't enumerate the possible values

**Overall**: This is significantly above-average EHI export documentation. The level of detail — 138K+ field-level entries, worked examples, SQL queries for customization — demonstrates genuine effort to make the export interpretable.

### Structure & Completeness

- **Granularity**: Field-level documentation with column names, captions, type codes, and form/subform/assessment hierarchy
- **Data types**: Comprehensive type code legend with 50+ types mapped to SQL data types
- **Coded fields**: Foreign key fields are identified by type code "FK" but value sets are not enumerated
- **Relationships**: Implicit through foreign key naming conventions and the `belongs_to_event` pattern; no explicit relationship diagram
- **Versioning**: Document dated 11/04/2024; ZIP filename includes "_v2" suggesting at least one prior version

### (b)(10) vs (g)(10) Assessment

This is a **genuine (b)(10) implementation**. Key evidence:

1. **The export is not FHIR** — it's a native JSON dump of the myEvolv database structure
2. **Coverage far exceeds USCDI** — includes ABA data, incident management, foster care, legal history, substance use, behavioral monitoring, and dozens of other specialty domains
3. **The page explicitly distinguishes** EHI export from FHIR APIs: "If you are working with a Netsmart customer and want to understand different options on integrating with our solutions, please visit our Netsmart Developer Portal for documentation regarding our FHIR API's"
4. **119 event categories** vs. the ~20 USCDI data classes — this is clearly a full data export, not a USCDI subset
5. **Binary data included** — base64-encoded images, documents, and signatures

## Access Summary
- Registered URL: https://www.ntst.com/lp/certifications
- Final URL (EHI page): https://www.ntst.com/lp/certifications/ehi-all-data-myevolv
- Status: found
- Required browser: no (curl works for downloads, but browser helps navigate the hub page)
- Navigation complexity: one_click (from certifications hub to EHI page, then one download link)
- Anti-bot issues: none

## Obstacles & Dead Ends
None. The documentation was straightforward to find and download. The certifications page rendered content in the DOM (not a true SPA), and the ZIP download worked without authentication or special headers.
