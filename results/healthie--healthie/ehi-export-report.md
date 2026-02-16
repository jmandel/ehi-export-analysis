# Healthie — EHI Export Documentation

Collected: 2026-02-16

## Source
- Registered URL: https://help.gethealthie.com/article/1200-b10-electronic-health-information-export-on-healthie
- CHPL IDs: 11055
- Product: Healthie, version "Cures 1", certified 2022-12-07
- Developer: Healthie (contact: compliance@gethealthie.com)

## Navigation Journal

1. **Initial probe**: `curl -sI -L "https://help.gethealthie.com/article/1200-b10-electronic-health-information-export-on-healthie" -H 'User-Agent: Mozilla/5.0'` returned HTTP 200 with `Content-Type: text/html; charset=utf-8`, 53,330 bytes. No redirects. The URL is served by a HelpScout Docs knowledge base hosted on Caddy/Istio.

2. **Page download**: `curl -sL "https://help.gethealthie.com/article/1200-b10-electronic-health-information-export-on-healthie" -H 'User-Agent: Mozilla/5.0' -o ehi-export-page.html`. The page loaded fully without JavaScript; the article body is in the HTML source, not loaded via SPA.

3. **Link inventory**: Extracted all links from the `#fullArticle` element. The page contains only:
   - Internal anchor links (#What-is-Electronic-Health-Information-EHI-KViuE, #Generating-an-Export-WBpPg, #Export-Format-zRlWB)
   - A mailto link (hello@gethealthie.com)
   - A broken link (`href="#undefined"`) labeled "this publicly accessible hyperlink" that should point to format.html (included within each export ZIP)
   - No downloadable files (PDF, ZIP, JSON, etc.) linked from the page

4. **File search**: `grep -oiE 'href="[^"]*\.(pdf|zip|xlsx|csv|json)..."'` found no downloadable artifacts.

5. **Image download**: One embedded image — a screenshot example of client_metrics.csv format: `curl -sL "https://d33v4339jhl8k0.cloudfront.net/docs/assets/5bbe96a22c7d3a04dd5b8761/images/6567bb962edfc966c355e31c/file-owoQwAwIzc.png"`.

6. **Browser verification**: Navigated in Chrome, took screenshots of the page top, "Generating an Export" section, "Export Format" section, and full page. All content rendered correctly; no hidden content behind accordions or JavaScript interactions.

7. **Related articles search**: Searched Healthie help site for "EHI export" and browsed the "EHR & Billing" category. Found:
   - [ONC Certification overview](https://help.gethealthie.com/article/1091-onc-certification) — hub page that links to the b(10) article; no additional export details
   - [Export or Transfer Healthie Account Data](https://help.gethealthie.com/article/819-export-your-data) — describes general data export/reporting features, not the b(10) EHI export; notably mentions that "chat history cannot be exported, except by users of Healthie's API"
   - [CCDA Import and Export](https://help.gethealthie.com/article/1214-consolidated-clinical-document-architecture-ccda-import-and-export-on-healthie) — separate ONC certification feature for transitions of care, not the b(10) export

   No additional EHI export documentation was found beyond the single registered page.

## What Was Found

Healthie provides a single, comprehensive documentation page for their (b)(10) EHI export. This is genuine (b)(10) documentation — not a repackaged FHIR API or (g)(10) reference.

### Export Mechanism

The export produces a **compressed ZIP file** containing CSV files, PDF files, a Documents folder, and an HTML format page, organized per patient. Two export modes are supported:

1. **Single-patient export**: Self-service. User navigates to patient profile > Charting section. Requires the "Can generate organization report" permission or non-organization user status.
2. **Patient population export**: Administrator-only, but **not self-service** — must email hello@gethealthie.com with subject "Patient Population b10 export request". Healthie Support handles the export due to "size of data, time and efforts required to manage server resources."

For population exports, the ZIP contains one directory per patient named `<FirstName><LastName><uniqueidentifier>`, each containing the same files as a single-patient export.

### Export Format

The export consists of **38 files per patient**:
- **34 CSV files** with column-level documentation (451 total columns across all files)
- **2 PDF files**: Charting.pdf (all charting notes) and journal_entries.pdf (all journal entries)
- **1 HTML file**: format.html (self-referencing export format documentation)
- **1 folder**: Documents folder (all uploaded documents in original format, preserving folder structure)

### Data Dictionary

The page contains a complete data dictionary with HTML tables defining every column for each CSV file. For some files, "Data Notes" indicate value formats (e.g., "Year-Mo-Day", "true or false", "Active or Inactive") or provide semantic context (e.g., "Metric categories: Weight, Body Fat %, Waist Circumference, Height (in)").

Notable structural observations:
- **Nine journal-type CSV files** (FoodEntry, MetricEntry, MirrorEntry, NoteEntry, PoopEntry, SleepEntry, SymptomEntry, WaterIntakeEntry, WorkoutEntry) all share an identical 21-column schema — a generic entry format with columns like Category, Code, Code System Name, Description, Ed Posthunger, Ed Prehunger, Emotions, etc. The column names suggest this is a single underlying data model for all patient journal entries.
- **Three food-related allergy CSV files** (Food_Intolerances, Food_Preferences, Food_Sensitivities) share the same 11-column schema as Allergies.csv but with different column naming (Allergen Code System Name vs. System Name).
- **cms1500s.csv** has 26 columns covering billing claims with insurance policy details, procedure codes, and reimbursement tracking.
- **Insurance_authorizations.csv** has 23 columns for prior authorization tracking.
- **All CSV data is exported as strings** — no typed columns.

### Broken Link

The format.html entry states: "Within this html page you can find this publicly accessible hyperlink that describes the export format." However, the hyperlink points to `#undefined` — a broken anchor. This appears to be a bug in the documentation page; the link was probably intended to point back to the documentation page itself.

## Export Coverage Assessment

### Data Domain Coverage

Comparing the export files against the product research findings:

**Clearly covered domains:**
- Demographics and contacts: Client_Overview.csv (13 cols including name, DOB, gender, pronouns, contact info), Addresses.csv, Family_and_Contacts.csv
- Clinical conditions: Diagnoses.csv (code, active status, onset/end dates)
- Medications: Medications.csv (name, code, active status, start/end dates, directions, dosage, frequency, route)
- Allergies: Allergies.csv (allergen code, category, reactions)
- Care plans: CarePlans.csv (description, name, hidden status)
- Goals: Goals.csv (description, due date, metric target, repeat, subgoals)
- Insurance billing: cms1500s.csv (26 cols), superbills.csv (10 cols), Insurance.csv, Insurance_authorizations.csv (23 cols), Policies.csv (19 cols)
- Payments: Payments.csv (15 cols including amount, currency, refunds, Stripe IDs)
- Provider information: Provider.csv, Other_Care_Team_Members.csv, Referring_Physicians.csv
- Messages: Messages.csv (conversation content, timestamps, deletion status)
- Documents: Documents folder (all uploaded files in original format with folder structure)
- Charting notes: Charting.pdf (all notes in PDF format)
- Journal entries: journal_entries.pdf, FoodEntry.csv, NoteEntry.csv, MetricEntry.csv, MirrorEntry.csv, PoopEntry.csv, SleepEntry.csv, SymptomEntry.csv, WaterIntakeEntry.csv, WorkoutEntry.csv
- Food/nutrition data: Food_Intolerances.csv, Food_Preferences.csv, Food_Sensitivities.csv, FoodEntry.csv
- Client metrics/biometrics: client_metrics.csv (weight, body fat, waist circumference, height with daily tracking)
- Client groups: Client_User_Groups.csv
- Packages: Packages.csv (billing packages with pricing, frequency, visibility)
- Recommendations: Recommendations.csv

**Domains with potential gaps or ambiguities:**

1. **Lab results**: No dedicated lab results CSV. The product integrates with Rupa Health, Evexia, and Fullscript for lab ordering and results. Lab reports may be captured as documents in the Documents folder, but structured lab data (test names, values, reference ranges) does not appear in the export schema.

2. **E-prescribing data**: Medications.csv captures medication records, but the product's DoseSpot e-prescribing integration likely stores additional prescription-specific data (pharmacy information, prescription status, PDMP queries, refill history) that isn't reflected in the 10-column Medications.csv schema.

3. **Intake forms/questionnaires**: The product has extensive custom intake form capabilities. Intake form data may be embedded in Charting.pdf, but there's no structured CSV export of form responses. For organizations using complex custom forms (e.g., behavioral health assessments, PHQ-9, GAD-7), the PDF format means this data is not machine-readable in the export.

4. **Telehealth session data**: The product supports HIPAA-compliant video sessions. There's no explicit telehealth session file in the export. Session metadata (date, duration, participants) may be captured in charting notes but isn't separately structured.

5. **Immunization records**: The product is certified for (a)(14) implant list which may include immunizations. No dedicated immunizations CSV exists in the export.

6. **Procedures/surgical records**: Procedure codes appear in cms1500s.csv and superbills.csv as billing data, but there's no dedicated clinical procedure record (e.g., procedure notes, outcomes, complications).

7. **Wearable device data**: The product syncs with Google Fit, Apple Health, and Fitbit. The MetricEntry.csv and other journal CSVs have a "Third Party Source" column, suggesting wearable data may flow through these files. However, the general "Export or Transfer" help article states "We do not currently support the bulk download of... metrics collected from wearables (outside of what is available in Reports)."

8. **Supplement recommendations**: The product integrates with Fullscript. Recommendations.csv exists but only has 2 columns (Body, Type) — unclear if this captures supplement-specific data.

9. **AI Scribe transcriptions**: The product offers an AI Scribe feature. Transcription data would likely be embedded in Charting.pdf but is not separately structured.

10. **Appointment/scheduling data**: No appointments CSV in the export. The general export article confirms "Appointments cannot be exported, however, the Appointments Report can be run to obtain this information." While appointment schedules are generally operational data (not EHI), encounter/visit history that documents when care was delivered may be relevant.

### Export Format & Standards

- **Format**: CSV + PDF + raw documents in a ZIP archive. This is a pragmatic, vendor-specific format — not FHIR, not C-CDA, not a standardized schema.
- **Appropriate for the data?**: Mostly yes. CSV is a reasonable export format for structured tabular data. PDF for charting notes preserves formatting of potentially complex clinical documentation. Raw document export preserves original files.
- **Key limitation**: No schema file (XSD, JSON Schema, DDL) is provided — only the HTML-based data dictionary on this page. A third party would need to parse the documentation page to understand the CSV column definitions.
- **Data types**: All CSV values are exported as strings. No type information, no coded value sets, no enumerated values beyond what's in the "Data Notes" column.
- **Relationships**: No foreign keys or explicit relationships between files are documented. For example, cms1500s.csv has a "Unique ID" column that presumably links to client records, but this isn't specified.
- **Reconstructability**: A third party could reconstruct a reasonable picture of the patient record from this export. The CSV structure is flat and readable. However, charting notes are in PDF (not structured) and the lack of explicit relationships between files means some context must be inferred.

### Documentation Quality

- **Readability**: Good. The page is well-organized with clear sections (EHI definition, export generation, format overview, per-file data dictionary).
- **Data dictionary**: Complete at the column-name level for all 34 CSV files. Every column is listed. Data notes are provided for some but not all columns (e.g., date formats, boolean indicators, enumerated values).
- **Missing from documentation**: Data types (all strings), value sets for coded fields, relationships between files, cardinality/nullability constraints, examples for most files (only client_metrics.csv has a screenshot example).
- **Worked examples**: One embedded screenshot showing client_metrics.csv layout. No sample export files or sample CSV content.
- **Developer-usable?**: A developer could implement a basic import, but would need to make assumptions about date parsing, coded values, and inter-file relationships. The documentation is sufficient for understanding what data is exported but insufficient for building a robust automated import pipeline.
- **Maintenance**: The documentation was likely created around December 2023 (based on the nearby release notes mentioning EHI export). The broken `#undefined` link suggests incomplete maintenance.

### Structure & Completeness

- **Granularity**: Column-name level with optional data notes. No data type specifications, no cardinality, no constraints.
- **Value sets**: Not documented. Fields like "Current Status" are noted as "Active or Inactive" in data notes, but most coded fields lack value documentation.
- **Relationships**: Not documented. Files share patient context implicitly (they're in the same patient folder) but inter-file references (e.g., which CMS1500 relates to which charting note) are not specified.
- **Versioning**: No version number or change history on the documentation.

### Notable Concern: Population Export Not Self-Service

The b(10) requirement states that the export must be "self-service and able to be executed at any time the user chooses and without subsequent developer assistance to operate." Healthie's population export requires emailing their support team, which appears to conflict with this requirement. Single-patient export is self-service.

### Overall Assessment

Healthie has made a genuine effort at (b)(10) compliance. This is clearly not a repackaged FHIR API — it's a purpose-built CSV/PDF export that covers the breadth of the platform's data. The data dictionary is thorough at the column level for all 38 export files.

The export covers the core clinical record well: demographics, diagnoses, medications, allergies, care plans, billing records, messages, and clinical documents. Healthie's distinctive wellness data (food journaling, biometric tracking, sleep/symptom/workout logging) is also included, which is appropriate given these are central to the product's clinical use.

The main gaps are in structured data for lab results, e-prescribing details, immunizations, and custom intake form responses. The reliance on PDF for charting notes and journal entries means rich clinical data is captured but not machine-readable. The lack of a schema file, explicit relationships, or typed columns limits the export's utility for automated data processing.

## Access Summary
- Final URL (after redirects): https://help.gethealthie.com/article/1200-b10-electronic-health-information-export-on-healthie
- Status: found
- Required browser: no (content is in HTML source, not SPA-loaded)
- Navigation complexity: direct_link
- Anti-bot issues: none

## Obstacles & Dead Ends
- The "publicly accessible hyperlink" in the format.html description has a broken `href="#undefined"` — should point to a format specification but doesn't
- No downloadable artifacts (no PDF, ZIP, JSON schema, or sample files linked from the page)
- The documentation is entirely contained on a single web page with no supplementary files
- The general "Export or Transfer" article (separate from b(10)) notes several export limitations: chat history only via API, no bulk wearable metric download, no appointment export — some of these may apply to the b(10) export as well
