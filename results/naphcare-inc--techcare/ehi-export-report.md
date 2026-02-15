# NaphCare, Inc. — EHI Export Documentation

Collected: 2026-02-14

## Source
- Registered URL: https://devportal.techcareehr.com/EHIExport
- CHPL IDs: 10207
- Product: TechCare® Version 5.0
- Certification date: 2019-12-08

## Navigation Journal

1. Probed the registered URL with `curl -sI -L "https://devportal.techcareehr.com/EHIExport"` — returned HTTP 200, Content-Type text/html, 24,038 bytes. No redirects.

2. Fetched the full page with `curl -sL "https://devportal.techcareehr.com/EHIExport" -o ehi-export-page.html`. The page is an ASP.NET MVC application (Microsoft-IIS/10.0) serving a Word-to-HTML document embedded in a Bootstrap navbar layout.

3. The dev portal has five navigation links: Home, Docs (FHIR API documentation), Terms, RWTP, and EHI Export. The EHI Export page is a dedicated page containing the full (b)(10) documentation.

4. The page embeds 13 images from `/Content/` — one screenshot of the TechCare UI showing the export notification, and 12 data dictionary table screenshots. Downloaded all 13 images:
   ```
   curl -sL "https://devportal.techcareehr.com/Content/image001.png" -o image001.png
   curl -sL "https://devportal.techcareehr.com/Content/image003.jpg" -o image003.jpg
   # ... (repeated for all 13 images)
   ```

5. Checked the Home page (`/`) and Docs page (`/Help`) — the Home page is a bare landing page. The Docs page covers the general TechCare REST/FHIR API (g)(10) with JWT authentication and endpoint documentation. No additional EHI export content found on either page.

6. Checked references in the HTML source to `/Content/filelist.xml` and `/Content/editdata.mso` (artifacts from the Microsoft Word export) — both return 404.

7. Took a full-page screenshot of the rendered EHI Export page in browser.

## What Was Found

The EHI Export page is a single, self-contained Word document exported to HTML. It was last updated 11/28/2023. It describes a genuine (b)(10) EHI export mechanism — not just a repackaged FHIR API.

### Export Format

The export produces three file types per patient:

1. **CSV files** — One CSV per data category, with header rows. Each CSV contains structured, discrete data from TechCare's database tables. All categories in the data dictionary are output as CSV.

2. **C-CDA documents** — One per patient, containing clinical data types that are best represented in C-CDA format: Medication Administrations, Vital Signs, Diagnostic Results, Treatment Plans (Plan of Care), Social History, Assessments, Functional Status, and Mental Status.

3. **PDF files** — All images (e.g., wound photos) and scanned paper records (e.g., faxed progress notes from outside clinics) are automatically converted to PDF. Named with conventions ensuring positive patient identification.

### Export Scope

- **Single patient**: Can be exported at any time by administrative users without developer assistance. Completes in minutes/seconds, with a notification in the TechCare UI.
- **All patients**: Uses a "side-loaded export engine" that scalably produces files continuously for all patients. Same data file types as single-patient export.

### Data Dictionary

The data dictionary is presented as 12 screenshot images of database table schemas. Each table shows columns for: Unique Key, Name, Data type, Description/Attributes, and NULLABLE. The primary key linking patients across tables is `INMATES.ID` (the demographic table's unique key — reflecting the correctional healthcare context).

The documented CSV export tables are:

| Table | Fields | Key Details |
|-------|--------|-------------|
| **Demographics** | ID, Booking Number, BookingDate, CustodyStatus, First Name, Last Name, Date of Birth, Gender, HousingLocation, SSN | Primary patient table. ID from OMS/JMS interface. CustodyStatus: ACTIVE/NOT ACTIVE. |
| **Medications** | ~22 fields including drug description, instructions (SIG), start/stop dates, GPI, route, order type (PRN/DOT/KOP), quantity, refills, authorizing provider NPI | References MEDISPAN for drug names. Internal medication order IDs. |
| **Allergies** | ~14 fields including allergy name/type, onset/stop dates, NDC, allergy class (Drug/Class/Environmental), GPI, reaction description (SNOMED) | References dbo.ALLERGIES_ENVIRONMENTAL. |
| **Problem List** | ~10 fields including ICD-10 code, problem name (from FLAGS), date identified/resolved, resolve text | References dbo.FLAGS table. |
| **Flags** (alerts) | ~8 fields including subject, message, alert date, location ID | Patient alerts/flags system. |
| **Appointments** | ~13 fields including scheduled/completed dates, appointment type, status, housing location, reason, created by | References dbo.APPOINTMENT_TYPE, dbo.STATUS. |
| **Diet Orders** | ~12 fields including diet type code/description, status, order/end dates, clinical comments, cancel reason | References dbo.DIET_TYPES. |
| **Lab Orders** | ~14 fields including order code (lab type), order description (test name), status, order/end dates, service provider ID, priority, cancel reason | References dbo.LAB_TYPES. |
| **Treatment Orders** | ~12 fields including treatment code, description (free text), status, order/end dates, clinical comments, cancel reason | References dbo.TREATMENT_TYPES. |
| **Specialty Consult Orders** | ~13 fields including order code (offsite/onsite/hospitalization/ER), specialty type, status, order/end dates, priority, clinical comments, cancel reason | References dbo.OFF_SITE_SPECIALTY_TYPES, dbo.OFF_SITE_PRIORITY_TYPES. |
| **Admission Orders** | ~12 fields including admission management type, order description, status (ACTIVE/NOT ACTIVE), order/end dates, clinical comments (quick notes), cancel reason | References dbo.ADMISSION_MANAGEMENT_TYPE. |
| **Immunizations** | ~22 fields including immunization group, date given, vaccine name, CVX code, administered by, route, site, manufacturer (MVX), lot number, expiration date, VIS info, refusal reasons | Most detailed table in the dictionary. |

### Additional Data via C-CDA

The following data categories are exported exclusively in C-CDA format (not as separate CSVs):
- Medication Administrations
- Vital Signs
- Diagnostic Results (lab results presumably, vs. lab orders in CSV)
- Treatment Plans (Plan of Care)
- Social History
- Assessments
- Functional Status
- Mental Status

## Export Coverage Assessment

### Data Domain Coverage

**Clearly covered (via CSV + C-CDA + PDF):**
- Patient demographics (including correctional-specific fields: booking number, custody status, housing location)
- Medications (orders, with detailed pharmacological data — GPI, route, SIG, refills, NPI)
- Medication Administrations (via C-CDA)
- Allergies (with SNOMED-coded reactions, NDC codes, GPI)
- Problem list (with ICD-10 coding)
- Immunizations (very detailed — CVX, MVX, lot numbers, VIS tracking, refusal reasons)
- Vital Signs (via C-CDA)
- Diagnostic/Lab Results (via C-CDA)
- Lab Orders (via CSV)
- Treatment Orders (via CSV)
- Appointments/scheduling
- Diet Orders (correctional-specific)
- Specialty Consult/Offsite Orders (hospitalization, ER, onsite, offsite referrals)
- Admission Orders (admissions management, discharge/group notes)
- Patient flags/alerts
- Social History (via C-CDA)
- Assessments (via C-CDA)
- Functional Status (via C-CDA)
- Mental Status (via C-CDA)
- Care Plans/Treatment Plans (via C-CDA)
- Scanned documents and images (via PDF)

**Notably missing or not mentioned:**
- **Clinical encounter notes / progress notes** — The single largest category of clinical documentation. Encounter notes are not in the CSV data dictionary, and the C-CDA section doesn't explicitly mention "encounters" or "clinical notes" as a category. Some encounter data may be captured indirectly through C-CDA Assessments or Treatment Plans, but free-text encounter documentation appears absent.
- **Mental health and behavioral health records** — While "Mental Status" and "Assessments" appear in the C-CDA section, there is no mention of substance abuse assessments, level of care designations, detox/withdrawal management data, suicide prevention documentation, or MAT records — all of which are core to correctional healthcare.
- **Pharmacy dispensing/administration records** — Medication orders are in CSV, and "Medication Administrations" are in C-CDA, but the detailed MAR (Medication Administration Record) tracking with accountability documentation that TechCare GO provides is not separately documented.
- **Claims and billing data** — No mention anywhere in the export documentation.
- **Compliance and audit records** — Chart audits, NCCHC compliance monitoring data not mentioned.
- **Staff training/credentialing records** — Not mentioned (though arguably not patient EHI).
- **Telehealth encounter records** — STATCare sessions not mentioned.
- **Health Services Requests (sick calls)** — A core correctional healthcare workflow with dedicated dashboards, but absent from the export.
- **Patient portal (MyCare) activity** — Not mentioned.
- **Intake screening data** — Receiving screenings upon facility admission are a core correctional workflow. Not explicitly present as a separate export category (may be partially captured in Assessments via C-CDA).
- **Discharge planning records** — Not mentioned as a distinct data category.
- **Audit logs** — System access and data modification logs not mentioned.
- **Family health history** — Certified for (a)(12) but not in the data dictionary or C-CDA list.
- **Implantable device information** — Certified for (a)(14) but not mentioned in the export.
- **Care plan data** — Certified for (b)(11); "Treatment Plans" in C-CDA may partially cover this.

The export covers the core clinical data categories reasonably well through the combination of CSV + C-CDA + PDF, but significant gaps exist in correctional-specific operational data, behavioral health records, billing, and administrative data. For a product built specifically for correctional healthcare, the absence of intake screening data, health services requests, mental health assessments, and behavioral health specialty data is surprising — these are the workflows that differentiate TechCare from a general-purpose EHR.

### Export Format & Standards

The three-format approach (CSV + C-CDA + PDF) is pragmatic and appropriate:

- **CSV** is highly computable and broadly accessible. The data dictionary provides enough structure (table names, field names, data types, descriptions, nullability, foreign key references) to reconstruct the data model. The use of database table references (dbo.DIET_TYPES, dbo.FLAGS, etc.) reveals the underlying SQL Server schema, which aids comprehension.
- **C-CDA** is well-suited for the clinical data types assigned to it (vitals, med administrations, assessments). However, this means some data is only accessible in C-CDA's XML structure, which is less computable than CSV for bulk analysis.
- **PDF** is appropriate for images and scanned documents, which have no discrete data to extract.

The format choices are reasonable. The main concern is that the C-CDA section is a "catch-all" for data types that don't have their own CSV table, and it's unclear how complete or structured the C-CDA content actually is for categories like "Assessments" and "Mental Status."

A third party could reconstruct much of the patient record from this export, but the lack of encounter notes and behavioral health documentation would leave significant gaps in the clinical narrative.

### Documentation Quality

**Strengths:**
- The data dictionary provides field-level detail: column names, SQL data types, descriptions, nullability, and foreign key references to lookup tables.
- The descriptions are written by someone who understands the data (e.g., "value is pre-populated when an alert is created from an item in a queue or list").
- The export process is clearly described — single patient vs. all patients, the file types used, and the rationale for each format.
- The documentation explicitly acknowledges the (b)(10) requirement and frames the export accordingly.

**Weaknesses:**
- The data dictionary is presented as **screenshot images of table schemas** rather than actual structured data (no CSV, JSON, or machine-readable format of the dictionary itself). This means the documentation cannot be programmatically consumed.
- There are no sample export files or worked examples.
- The C-CDA section is vague — it lists data types by name but provides no details about the C-CDA template structure, what sections are used, or what level of detail is included.
- No schema files (XSD, JSON Schema, OpenAPI) are provided.
- The documentation appears to be a one-time Word document export from November 2023 that has not been significantly updated.
- The page has Word/Office markup artifacts (VML, MSO namespaces), suggesting minimal effort in presentation.

### Structure & Completeness

The CSV data dictionary is moderately granular:
- **Table names**: Yes (12 categories)
- **Field names**: Yes
- **Data types**: Yes (SQL Server types with lengths — nvarchar(50), datetime, int, float, etc.)
- **Descriptions**: Yes, generally helpful
- **Nullability**: Yes
- **Foreign key references**: Partially — some fields reference lookup tables (dbo.DIET_TYPES, dbo.FLAGS, dbo.CVX, dbo.MVX, dbo.MEDISPAN) but the contents of these lookup tables are not provided
- **Value sets**: Minimal — some fields note possible values (e.g., CustodyStatus: "ACTIVE or NOT ACTIVE", Gender: "M or F or Male or Female") but most coded fields just reference a lookup table without listing the values
- **Cardinality**: Not explicitly documented, though it's implied (INMATES.ID is the primary key, one-to-one and one-to-many relationships mentioned)
- **Versioning/change history**: Only "Current as of 11/28/2023"

The documentation is functional but minimal. A developer could build an import for the CSV files based on this data dictionary, though they would need to reverse-engineer the lookup table contents and handle the C-CDA and PDF portions without detailed guidance.

## Access Summary
- Final URL (after redirects): https://devportal.techcareehr.com/EHIExport
- Status: found
- Required browser: no (static HTML with images, no JavaScript required)
- Navigation complexity: direct_link
- Anti-bot issues: none

## Obstacles & Dead Ends

- The data dictionary is presented as images (screenshots of what appears to be a database design tool or Excel), not as structured text or downloadable files. There is no CSV, JSON, or other machine-readable version of the data dictionary itself.
- The Word-to-HTML export includes references to supporting files (filelist.xml, editdata.mso) that return 404, but these are just Microsoft Office artifacts and not meaningful content.
- The Docs page on the dev portal covers the FHIR API (g)(10) — this is separate from and not relevant to the (b)(10) EHI export.
