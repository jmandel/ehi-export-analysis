# CareTracker, Inc. — EHI Export Documentation

Collected: 2025-07-18

## Source
- Registered URL: https://amazingcharts.com/hubfs/Amazing-Charts-EHI-Export-Documentation-V1_0-1-1.pdf?hsLang=en
- CHPL IDs: 11608, 11646, 11720, 11492

## Navigation Journal

### Step 1: Probe the URL

```bash
curl -sI -L "https://amazingcharts.com/hubfs/Amazing-Charts-EHI-Export-Documentation-V1_0-1-1.pdf?hsLang=en" -H 'User-Agent: Mozilla/5.0'
```

Result: HTTP 200 directly. Content-Type: `application/pdf`, Content-Length: 195305 bytes. No redirects. The URL is a direct PDF download hosted on HubSpot's file CDN (`amazingcharts.com/hubfs/...`).

### Step 2: Download the PDF

```bash
curl -sL "https://amazingcharts.com/hubfs/Amazing-Charts-EHI-Export-Documentation-V1_0-1-1.pdf?hsLang=en" \
  -H 'User-Agent: Mozilla/5.0' \
  -o downloads/Amazing-Charts-EHI-Export-Documentation-V1_0-1-1.pdf
```

Verified with `file`: confirmed "PDF document, version 1.7, 8 pages". No authentication required. No anti-bot measures encountered.

### Step 3: Examine PDF contents

```bash
pdfinfo downloads/Amazing-Charts-EHI-Export-Documentation-V1_0-1-1.pdf
pdftotext downloads/Amazing-Charts-EHI-Export-Documentation-V1_0-1-1.pdf - | head -100
```

- 8 pages, created October 2023, authored by Kathiresan Palanisamy
- Created with Microsoft Word for Microsoft 365
- No embedded URLs, no embedded files/attachments (`pdfdetach -list` returns 0)
- No hyperlinks in the document pointing to additional resources

### Step 4: Check for additional documentation

Extracted all URLs from the PDF text: none found. The PDF is self-contained — no references to external schema files, API documentation, sample data, or supplementary guides. This is the entire EHI export documentation.

## What Was Found

### Document: "Amazing Charts EHI Export: Folder Organization and Data Format Specification – v1.0"

A single 8-page PDF that describes the EHI export mechanism for Amazing Charts EHR. The document covers:

**Export Mechanism:**
- Supports single-patient and population-level export
- Population filters: by Provider, All Active Patients, All Patients, or Encounter Range
- Creates a per-patient folder with a timestamp for identification
- Each data class is exported as a separate file named `[Data Class Name].[Export Format]`
- Supported formats: CSV, JSON, and XML (user-selectable)
- A "Documents" subfolder preserves imported items, images, and documents in original format

**Data Dictionary:**
The bulk of the document (pages 1–8) is a two-column table listing 44 data classes and their column headings. This is the complete data dictionary. Each row gives:
- **Data Class Name** — the export category (e.g., "Billing History", "Clinical Notes", "Medications")
- **Column Headings** — the field names that appear in the exported file

There are 44 data classes with a combined total of ~1,100 columns. The data classes span:

| Category | Data Classes |
|----------|-------------|
| **Demographics** | Patient Demographics, Next Of Kin, Demographic Immunization |
| **Clinical Notes** | Clinical Notes, Addendum, Assesments, Plan of Treatment |
| **Problems/Diagnoses** | List Problem, List Problem Pending |
| **Medications** | Medications, Medications Pending, Injections |
| **Allergies** | Allergies and Intolerances, Allergies and Intolerances Pending |
| **Immunizations** | Immunizations, HM Rules, HM Rules Ignored |
| **Labs/Results** | Lab Tests |
| **Vitals** | Vital Signs, Smoking Statuses |
| **Procedures** | Procedures |
| **Billing** | Billing History |
| **Insurance** | Health Insurance |
| **Orders/Referrals** | Orders, Referrals |
| **History** | FamilyHistory, Risk Factors, Travel History, Occupation and Industry History |
| **Care Planning** | Goals, Health Concerns, Care Team Members, Advance Directives, FunctionalStatus |
| **Documents** | Imported Items, Patient Generated Data, Patient Health Information Capture, Patient Record Release |
| **Communication** | Email, Alerts |
| **Administrative** | Scheduling, User Defined Fields, Tracked Data |
| **Devices** | Implantable device |

**What the documentation does NOT include:**
- No data types for any column (everything is just a column name)
- No value sets, enumerations, or coded value documentation
- No descriptions or definitions of what columns mean
- No relationships between data classes (e.g., foreign keys)
- No sample export files or example data
- No schema files (XSD, JSON Schema, etc.)
- No versioning or change history beyond "v1.0"
- No export instructions or screenshots of the export interface

## Export Coverage Assessment

### Data Domain Coverage

Comparing the export's 44 data classes against the product research (which describes Amazing Charts as an ambulatory EHR for small-to-mid practices with modules for charting, e-prescribing, billing, patient portal, and population health):

**Well-Covered Domains:**
- **Demographics and contacts** — Patient Demographics (62 columns) includes name, address, contact info, race, ethnicity, language, sexual orientation, gender identity, and more. Next Of Kin is separate.
- **Clinical documentation** — Clinical Notes has 89 columns covering chief complaint, HPI, ROS, physical exam, assessment, plan, vitals, tobacco use, pregnancy data, vision/hearing, and location info. Addendum captures note amendments.
- **Medications** — Both active (Medications, 50 columns) and pending (Medications Pending, 38 columns) are included, with prescribing provider, pharmacy info, e-prescribing status, dispensing details, and controlled substance tracking.
- **Problems** — List Problem and List Problem Pending cover ICD codes, SNOMED codes, chronicity, date tracking, and provider attribution.
- **Allergies** — Both confirmed and pending allergies are exported with severity, reaction, SNOMED-mapped adverse reaction IDs, and date ranges.
- **Lab results** — Lab Tests is the largest data class (126 columns) with extensive detail: ordering info, specimen data, result values, reference ranges, abnormal flags, LOINC codes, lab facility info, and notes.
- **Billing** — Billing History (74 columns) covers place of service, CPT/ICD codes (up to 12 ICD pointers), modifiers, NDC codes, fees/charges, billing/referring provider details including NPI, and facility information.
- **Insurance** — Health Insurance (39 columns) covers payer info, plan details, subscriber/guarantor demographics, and coverage dates.
- **Immunizations** — Comprehensive (122 columns combined with HM Rules) including vaccine, lot, manufacturer, VIS info, VFC status, registry submission, and health maintenance rule tracking.
- **Family history** — FamilyHistory (20 columns) with relational data, SNOMED/ICD coding, and diagnosis details.
- **Vital signs** — Vital Signs (28 columns) covering temperature, BP, pulse, respiratory rate, O2 sat, weight, height, BMI, head circumference, pain, peak flow, vision, hearing, and pregnancy-related vitals.
- **Procedures** — Procedures (15 columns) with CPT codes, descriptions, fees, NDC codes.
- **Orders and Referrals** — Orders (24 columns) with order type, status, tracking, and assignment. Referrals (12 columns) with provider, date range, and visit count.
- **Scheduling** — Scheduling (14 columns) with appointment date, visit type, provider, duration, and telehealth flag.
- **Advance Directives** — Covered with status tracking, dates, and document paths.

**Potentially Missing or Incomplete Domains:**
- **Patient portal messages** — The product research notes Amazing Charts uses Updox for patient portal/messaging. There is an "Email" data class (11 columns) that may capture some of this, but it's unclear whether portal messages are fully captured or just internal email.
- **E-prescribing details** — The product uses NewCrop/DrFirst for e-prescribing. Medications includes `ERXstatus`, `SentBySureScripts`, and pharmacy transaction details, but formulary checking results, prior authorization interactions, and EPCS audit trails may live in the third-party system.
- **Digital intake forms / consent forms** — The "Patient Health Information Capture" and "Patient Generated Data" data classes (17 and 14 columns respectively) may partially cover these, but the column names suggest they may be more about directive-type documents than structured intake data.
- **Telemedicine records** — Scheduling has an `IsTelehealth` flag, but there's no separate data class for telemedicine session details, recordings, or virtual visit documentation.
- **Document content** — The "Documents" subfolder preserves imported items and images, which is good. But the documentation doesn't describe what document types are captured or their metadata schema.

**Notable Inclusions (Good (b)(10) Signals):**
- **Billing History** is present with 74 columns — this is a strong signal of genuine (b)(10) compliance. Many vendors omit billing data.
- **Health Insurance** is a separate data class — uncommon and thorough.
- **User Defined Fields** — captures custom/practice-specific data, which is important for completeness.
- **Tracked Data** — appears to capture user-defined tracked clinical values.
- **Risk Factors, Travel History, Occupation and Industry History** — specialty data that many vendors miss.
- **Scheduling** — appointment data is included (not always considered EHI but relevant).
- **Patient Record Release** — documents when records were released, to whom, and why.
- **Pending states** — separate data classes for pending allergies, pending problems, and pending medications shows attention to data completeness.

### Export Format & Standards

- **Format:** CSV, JSON, or XML — user-selectable per export. Not FHIR, not C-CDA.
- **Structure:** Flat files per data class, one file per category per patient. No schema files provided.
- **Standard:** Ad-hoc vendor format. Column names are vendor-defined, not mapped to any standard terminology (though some columns reference SNOMED, ICD, LOINC, and CPT codes as values).
- **Relationships:** Not documented. There are no foreign key definitions or entity-relationship documentation. PatientID appears in most data classes and is the implicit join key, but relationships between data classes (e.g., which medications relate to which encounters) are not explicitly mapped.
- **Reconstruction feasibility:** A developer could import the flat files into a database, but without relationship documentation, reconstructing the clinical narrative (which note led to which order, which problem is linked to which medication) would require inference from dates and IDs.

This is **not a repackaged (g)(10) FHIR API** — it's clearly a genuine (b)(10) bulk export of the underlying database tables. The column names are raw database field names (with typos like "FristName", "Signetur", "BillingProvideerState"), not standardized FHIR resource paths.

### Documentation Quality

- **Readability:** Simple two-column table format. Easy to scan.
- **Completeness:** Column names only — no data types, no descriptions, no value sets, no constraints. You know that "Billing History" has a column called "Complexity" but not what values it can take or what it means.
- **Examples:** None. No sample export files, no example records, no test data.
- **Developer usability:** A developer could parse the export files using these column names as headers, but would need significant domain knowledge (or access to a sample export) to understand the semantics. Many column names are self-explanatory ("PatientID", "BirthDate") but others are opaque ("COSTAR", "Migrated", "HowMigrated", "PendingFlag").
- **Maintenance:** Version "v1.0" from October 2023. No change history. No indication of update cadence.

Overall, this documentation is a **compliance minimum** — it tells you the column names for each data class, which is enough to parse the files, but not enough to fully understand the data without additional context.

### Structure & Completeness

- **Granularity:** Field names only. No data types, cardinality, nullability, or constraints.
- **Value sets:** Not documented anywhere. Coded fields (e.g., `RxChangeGuidForApproved`, `ERXstatus`, `MaritalStatus`, `InsuranceType`) have no value set definitions.
- **Relationships:** Not documented. The only implicit relationship is PatientID as a shared key.
- **Entity model:** Each data class is effectively a flat table. No hierarchical structure or nesting documented.
- **Versioning:** "v1.0" — first and only version.

## Access Summary
- Final URL (after redirects): https://amazingcharts.com/hubfs/Amazing-Charts-EHI-Export-Documentation-V1_0-1-1.pdf?hsLang=en
- Status: found
- Required browser: no
- Navigation complexity: direct_link
- Anti-bot issues: none

## Obstacles & Dead Ends

None. The URL worked directly with a simple curl request. No authentication, no redirects, no anti-bot measures. The PDF downloaded cleanly on the first attempt.

The only limitation is the PDF format itself — the two-column table layout required a custom parser to extract structured data, and the `pdftotext` output merges the "HM Rules" data class columns into the "Immunizations" entry due to how the table rows are laid out in the PDF.
