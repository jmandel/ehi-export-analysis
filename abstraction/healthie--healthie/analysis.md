# EHI Export Analysis: Healthie

**Product**: Healthie (version "Cures 1")
**Analysis date**: 2026-02-16
**CHPL IDs**: 15.04.04.3130.Heal.01.00.1.221207

## 1. Product Context

Healthie is a cloud-based EHR and practice management platform designed for health and wellness professionals, with a focus on virtual-first care. It serves 25,000+ active providers managing 10M+ patient records. Key specialties include behavioral health, nutrition/dietetics, women's health, chronic care management, health coaching, and substance use treatment.

The platform stores the following data relevant to EHI export completeness:

- **Clinical data**: charting notes (customizable templates), diagnoses (ICD codes), medications (via DoseSpot e-prescribing integration), allergies, care plans, goals
- **Billing & insurance**: CMS 1500 claims, superbills, insurance policies, prior authorizations, payments (via Stripe), eligibility tracking
- **Wellness/specialty data**: food journaling with nutrient tracking, biometric metrics (weight, BMI, body fat, waist circumference), sleep/symptom/workout/water intake logging, selfie/mirror progress photos — these are central to the product's clinical value
- **Lab ordering**: via integrations with Rupa Health, Evexia, and Fullscript (results appear as documents)
- **E-prescribing**: via DoseSpot integration (EPCS-capable)
- **Communications**: secure messaging, patient portal
- **Documents**: uploaded files, e-fax
- **Custom intake forms**: electronic forms and questionnaires that flow into the EHR
- **Telehealth**: integrated HIPAA-compliant video sessions

This is an ambulatory/virtual-first product with no inpatient or imaging workflows.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/ehi-export-page.html` (53,330 bytes) | Main (b)(10) documentation page from Healthie's HelpScout knowledge base. Contains complete data dictionary for all 38 export files with column-level definitions. | **Primary source** — the single most important artifact |
| `downloads/enrichment/data-dictionary.json` (46,848 bytes) | Pre-extracted JSON of the data dictionary (38 files, 451 columns). | Cross-validation reference; matched my independent parse |
| `downloads/enrichment/extraction-log.json` (2,409 bytes) | Extraction accounting: 38/38 files parsed, 0 errors. | Confirmed completeness of prior extraction |
| `downloads/enrichment/extract-data-dictionary.ts` (9,958 bytes) | TypeScript extraction script used to produce the JSON. | Reference for parsing methodology |
| `downloads/client-metrics-example.png` (159 KB) | Screenshot of client_metrics.csv pivot-table layout. | Useful — only visual sample of export data format |
| `downloads/screenshot-*.png` (4 files, 3.6 MB total) | Browser screenshots of the documentation page. | Low — redundant with HTML source |

**Verified**: The documentation URL (https://help.gethealthie.com/article/1200-b10-electronic-health-information-export-on-healthie) returns HTTP 200 with the same 53,330-byte HTML page. No downloadable supplementary files (PDFs, ZIPs, schemas, sample data) are linked from the page.

## 3. Export Mechanics

- **Format**: Compressed ZIP containing CSV files, PDF files, a Documents folder, and an HTML format page, per patient
- **Mechanism**:
  - **Single-patient**: Self-service via UI. Navigate to patient profile → Charting section. Requires "Can generate organization report" permission.
  - **Population/bulk**: **Not self-service**. Must email hello@gethealthie.com with subject "Patient Population b10 export request." Healthie Support handles the export "due to the size of data, time and efforts required to manage server resources." This appears to conflict with the (b)(10) requirement that export be self-service.
- **Single-patient vs bulk**: Both supported, but bulk requires vendor assistance.
- **Access constraints**: Single-patient requires specific permission. Population export requires administrator role and vendor involvement.
- **Fees**: Not mentioned.

## 4. Export Content: What's In It

The export consists of **38 files per patient**: 34 CSV files (451 total columns), 2 PDF files, 1 HTML metadata file, and 1 Documents folder.

### Data Dictionary Statistics

| Metric | Value |
|---|---|
| Total files | 38 |
| CSV files | 34 |
| Total columns (across all CSVs) | 451 |
| Unique columns (counting journal schema once) | 283 |
| Columns with data notes | 60 (13.3%) |
| Columns without any notes | 391 (86.7%) |
| Data types documented | No (all exported as strings) |
| Relationships/foreign keys documented | No |
| Value sets documented | Partially (a few boolean "true or false" and status "Active or Inactive" notes) |
| Sample data provided | 1 screenshot (client_metrics.csv only) |
| Machine-readable schema | No |

**Note on field descriptions**: Healthie's data dictionary provides column names and optional "Data Notes" — but these notes are sparse. Only 60 of 451 columns (13.3%) have any data notes, and most of those are just format hints ("Year-Mo-Day", "true or false") rather than semantic descriptions. No column has a data type, nullability, or foreign key specification.

### Vendor's own content organization

The vendor does not organize its data dictionary into categories — it's a flat list of files. I assigned categories based on file names and content. The 9 journal entry CSVs (FoodEntry, MetricEntry, MirroEntry, NoteEntry, PoopEntry, SleepEntry, SymptomEntry, WaterIntakeEntry, WorkoutEntry) all share an identical 21-column schema, suggesting a single underlying data model for all patient journal entries.

**Notable observation**: The HTML documentation contains "MirroEntry.csv" (missing the 'r') — likely a typo for "MirrorEntry.csv" (the selfie/progress photo journal).

| File | Columns | Notes | Type | Category |
|---|---|---|---|---|
| cms1500s.csv | 26 | 6 | csv | Billing & Insurance |
| Insurance_authorizations.csv | 23 | 0 | csv | Billing & Insurance |
| FoodEntry.csv | 21 | 3 | csv | Journal Entries (Wellness) |
| MetricEntry.csv | 21 | 3 | csv | Journal Entries (Wellness) |
| MirroEntry.csv | 21 | 3 | csv | Journal Entries (Wellness) |
| NoteEntry.csv | 21 | 3 | csv | Journal Entries (Wellness) |
| PoopEntry.csv | 21 | 3 | csv | Journal Entries (Wellness) |
| SleepEntry.csv | 21 | 3 | csv | Journal Entries (Wellness) |
| SymptomEntry.csv | 21 | 3 | csv | Journal Entries (Wellness) |
| WaterIntakeEntry.csv | 21 | 3 | csv | Journal Entries (Wellness) |
| WorkoutEntry.csv | 21 | 3 | csv | Journal Entries (Wellness) |
| Packages.csv | 19 | 6 | csv | Billing & Insurance |
| Policies.csv | 19 | 4 | csv | Billing & Insurance |
| Payments.csv | 15 | 1 | csv | Billing & Insurance |
| Client_Overview.csv | 13 | 2 | csv | Demographics & Contacts |
| Other_Care_Team_Members.csv | 12 | 0 | csv | Care Team |
| Provider.csv | 12 | 0 | csv | Care Team |
| Referring_Physicians.csv | 12 | 0 | csv | Care Team |
| Allergies.csv | 11 | 0 | csv | Allergies & Food Sensitivities |
| Food_Intolerances.csv | 11 | 0 | csv | Allergies & Food Sensitivities |
| Food_Preferences.csv | 11 | 0 | csv | Allergies & Food Sensitivities |
| Food_Sensitivities.csv | 11 | 0 | csv | Allergies & Food Sensitivities |
| Medications.csv | 10 | 3 | csv | Clinical - Medications |
| superbills.csv | 10 | 0 | csv | Billing & Insurance |
| client_metrics.csv | 8 | 3 | csv | Biometric Metrics |
| Messages.csv | 8 | 6 | csv | Communications |
| Goals.csv | 7 | 0 | csv | Care Plans & Goals |
| Addresses.csv | 6 | 0 | csv | Demographics & Contacts |
| Family_and_Contacts.csv | 5 | 0 | csv | Demographics & Contacts |
| Diagnoses.csv | 4 | 3 | csv | Clinical - Conditions |
| CarePlans.csv | 3 | 1 | csv | Care Plans & Goals |
| Client_User_Groups.csv | 2 | 0 | csv | Administrative |
| Insurance.csv | 2 | 0 | csv | Billing & Insurance |
| Recommendations.csv | 2 | 0 | csv | Care Plans & Goals |
| Charting.pdf | — | — | pdf | Clinical Notes |
| journal_entries.pdf | — | — | pdf | Journal Entries (Wellness) |
| Documents folder | — | — | folder | Documents |
| format.html | — | — | html | Export Metadata |

### Category Summary

| Category | Files | Total Columns | Columns with Notes |
|---|---|---|---|
| Billing & Insurance | 7 | 114 | 15 |
| Journal Entries (Wellness) | 10 | 189 (21 unique) | 27 (3 unique) |
| Demographics & Contacts | 3 | 24 | 2 |
| Care Team | 3 | 36 | 0 |
| Allergies & Food Sensitivities | 4 | 44 | 0 |
| Care Plans & Goals | 3 | 12 | 1 |
| Clinical - Medications | 1 | 10 | 3 |
| Clinical - Conditions | 1 | 4 | 3 |
| Biometric Metrics | 1 | 8 | 3 |
| Communications | 1 | 8 | 6 |
| Administrative | 1 | 2 | 0 |
| Clinical Notes | 1 (PDF) | — | — |
| Documents | 1 (folder) | — | — |
| Export Metadata | 1 (HTML) | — | — |

The full inventory is available in `analysis/full-entity-inventory.json`.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

**Billing & Insurance** is the deepest structured domain with 7 files and 114 columns. It includes CMS 1500 claims (26 columns covering procedure codes, reimbursement amounts, primary/secondary insurance policy details), prior authorizations (23 columns tracking visit counts and effective dates), superbills (10 columns), insurance policies (19 columns with holder demographics), payments (15 columns including Stripe IDs and refunds), and packages (19 columns for billing configurations).

**Journal Entries (Wellness)** is the most file-heavy domain (10 files) but uses a single repeated 21-column schema across 9 CSV types (food, metric, mirror/selfie, notes, bowel, sleep, symptoms, water intake, workouts). A 10th file (journal_entries.pdf) provides a formatted rendition. This is distinctive to Healthie's wellness focus and not found in typical EHRs.

**Demographics & Contacts** covers patient overview (13 columns including name, DOB, gender, pronouns, contact info, current weight/height), addresses (6 columns), and family contacts (5 columns).

**Clinical data** is spread across several files: Diagnoses (4 columns: code, active status, onset/end dates), Medications (10 columns: name, code, active status, dates, dosage, frequency, route, directions), Allergies (11 columns with coded allergens and reactions), CarePlans (3 columns: name, description, hidden status), and Goals (7 columns).

**Clinical Notes** are exported as Charting.pdf — a PDF containing all charting notes. The documentation states "Format and data elements are specific to an organization's and patient's charting notes," meaning the content is not structured or standardized.

**Documents** are exported in their original format with folder structure preserved from the patient's Documents page.

**Communications** includes Messages.csv (8 columns: conversation name, content, timestamps, deletion status, autoresponse flag, viewed status).

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | `Client_Overview.csv` (13 cols), `Addresses.csv` (6 cols), `Family_and_Contacts.csv` (5 cols) | Adequate; includes name, DOB, gender, pronouns, phone, email, address |
| Encounters / visits | ❌ Not covered | No encounters/appointments CSV. Encounter context only implicit in billing (cms1500s.csv Date of Service) and notes (Charting.pdf). | Product stores appointments and visit data; general help article confirms "Appointments cannot be exported." Modest gap — encounter dates reconstructable from claims/notes, but structured visit data is absent. |
| Problems / conditions / diagnoses | ✅ Covered | `Diagnoses.csv` (4 cols: Code, Active, Onset Date, End Date) | Adequate for problem list; no description/display text column, just codes |
| Medications / prescriptions | ⚠️ Partial | `Medications.csv` (10 cols: Name, Code, Active, Start/End Date, Directions, Dosage, Frequency, Route) | Medication list is present. However, product uses DoseSpot for e-prescribing (EPCS-capable); prescription-specific data (pharmacy, prescription status, PDMP queries, refill history) is not represented. |
| Allergies | ✅ Covered | `Allergies.csv` (11 cols with coded allergens, reactions, and code systems) | Thorough; includes allergen codes and typed reactions |
| Immunizations | ❌ Not covered | No immunizations file | Product is certified for (a)(14) implant list which may relate. Not a core workflow for Healthie's primary specialties (nutrition, behavioral health, coaching). Minor gap. |
| Vitals | ⚠️ Partial | `client_metrics.csv` (8 cols: weight, body fat %, waist circumference, height) and `MetricEntry.csv` (21 cols) | Captures biometrics central to wellness practice but limited to 4 metric categories. Standard vitals (BP, HR, temp, respiratory rate) are not separately structured. May appear in Charting.pdf. |
| Lab results | ❌ Not covered | No lab results CSV | Product integrates with Rupa Health, Evexia, and Fullscript for lab ordering. Lab reports likely stored as documents (in Documents folder), but no structured lab data (test names, values, reference ranges) is exported. Significant gap for practices using e-labs. |
| Imaging / diagnostic reports | N/A | No imaging module | Product does not include imaging workflows |
| Procedures | ⚠️ Partial | Procedure codes appear in `cms1500s.csv` (Procedure Codes column) and `superbills.csv` | Billing-side procedure documentation only; no clinical procedure records |
| Clinical notes / documents | ✅ Covered | `Charting.pdf` (all charting notes), `Documents folder` (all uploaded documents in original format) | Notes are comprehensive but exported as PDF — not machine-readable. Custom form data and intake responses are likely embedded in notes. |
| Care plans / goals | ✅ Covered | `CarePlans.csv` (3 cols), `Goals.csv` (7 cols), `Recommendations.csv` (2 cols) | Present but thin — CarePlans has only name/description/hidden; Goals is richer with due dates and metric targets |
| Orders / referrals | ⚠️ Partial | `Referring_Physicians.csv` (12 cols) captures referral source info | No order/referral records themselves; only referring physician contact details |
| Insurance / coverage | ✅ Covered | `Insurance.csv` (2 cols), `Policies.csv` (19 cols), `Insurance_authorizations.csv` (23 cols) | Deep coverage of policy holder details, authorization tracking, visit counts |
| Claims / billing | ✅ Covered | `cms1500s.csv` (26 cols), `superbills.csv` (10 cols) | CMS 1500 claims with procedure codes, reimbursement, insurance details. Genuine billing data. |
| Payments | ✅ Covered | `Payments.csv` (15 cols including amount, currency, refunds, Stripe charge IDs) | Thorough payment tracking |
| Consents / directives | ❌ Not covered | No consent file | Product has intake forms that could include consents, but no structured consent export. May be in Documents folder. |
| Patient communications / portal messages | ✅ Covered | `Messages.csv` (8 cols) | Includes conversation content and metadata. Note: general help article says "chat history cannot be exported, except by users of Healthie's API" — unclear if this limitation applies to b(10) export. |
| Specialty-specific (nutrition/wellness) | ✅ Covered | 9 journal entry CSVs (FoodEntry, MetricEntry, MirroEntry, NoteEntry, PoopEntry, SleepEntry, SymptomEntry, WaterIntakeEntry, WorkoutEntry), `client_metrics.csv`, `Food_Intolerances.csv`, `Food_Preferences.csv`, `Food_Sensitivities.csv` | Distinctive strength — captures Healthie's core wellness data including food journaling, biometrics, symptom tracking, sleep, exercise, and food sensitivity profiles |
| Specialty-specific (behavioral health) | ⚠️ Partial | Behavioral health assessments (PHQ-9, GAD-7) likely embedded in Charting.pdf | No structured export of standardized assessment scores. For behavioral health practices, this is a gap in machine-readability. |

## 6. Documentation Quality

**Strengths**:
- Complete column-name-level coverage: every CSV file has every column listed
- Single, well-organized documentation page with clear sections
- Export generation instructions are practical and clear (for single-patient)
- Some data notes provide useful context (date formats, boolean values, metric categories)

**Weaknesses**:
- **No data types**: All CSV data is exported as strings with no type documentation
- **No relationships**: No foreign keys or cross-file references documented. Files share a patient context implicitly (same ZIP) but inter-file relationships (e.g., which CMS 1500 relates to which superbill or charting note) are not specified
- **No value sets**: Only a handful of fields have enumerated values documented (e.g., "Active or Inactive"). Most coded fields (diagnosis codes, allergen codes, procedure codes) have no code system or value set reference
- **Sparse descriptions**: Only 60 of 451 columns (13.3%) have any data notes, and most are just format hints rather than semantic descriptions. A developer would need to guess the meaning of columns like "Ed Posthunger", "Metric Stat", or "Subentries Count"
- **No sample data**: Only one embedded screenshot (client_metrics.csv). No sample CSV files, no downloadable ZIP
- **No machine-readable schema**: No JSON Schema, XML Schema, DDL, or other parseable format definition
- **Broken link**: The format.html description contains a link to `#undefined` — should point to the format specification but doesn't
- **PDF for clinical notes**: Charting notes and journal entries are exported as PDF, making them non-machine-readable. Custom intake form responses are likely embedded in these PDFs with no structured alternative

**Developer usability**: A developer could build a basic import pipeline from this documentation, but would need to make significant assumptions about data types, coded values, and inter-file relationships. The journal entry schema is particularly opaque — column names like "Ed Posthunger" and "Perceived Hungriness" are domain-specific with no explanation.

## 7. Overall Assessment

### Classification

**Partial native export**: Healthie exports its native data model across 34 CSV files plus PDFs and documents, covering most clinical and billing domains the product stores. However, there are notable gaps (lab results, structured intake forms, encounter records, e-prescribing details) and the documentation, while complete at the column-name level, lacks the depth (types, relationships, value sets, descriptions) needed for robust data consumption.

### Key Findings

1. **Genuine (b)(10) effort with broad coverage**: This is not a repackaged FHIR/C-CDA export. Healthie built a purpose-specific CSV+PDF export covering 38 files and 451 columns across demographics, clinical, billing, wellness, and communications domains. The inclusion of wellness-specific data (food journaling, biometric tracking, symptom logging) is appropriate and distinctive.

2. **Billing data is genuinely deep**: The 7 billing/insurance files (114 columns) cover CMS 1500 claims, superbills, insurance policies, prior authorizations, and payments with Stripe integration. This is more billing depth than many certified EHRs provide in their (b)(10) exports.

3. **Lab results are a significant structured gap**: Despite integrating with Rupa Health, Evexia, and Fullscript for lab ordering and results, no structured lab data appears in the export. Lab reports may exist as documents in the Documents folder, but there is no CSV with test names, values, or reference ranges.

4. **Clinical notes are PDF-only, making rich data non-machine-readable**: Charting.pdf captures all clinical notes but in a non-structured format. Custom intake forms, behavioral health assessments (PHQ-9, GAD-7), and any organization-specific charting templates are locked in PDF, not exportable as structured data.

5. **Population export is not self-service**: Bulk export requires emailing Healthie Support, which may conflict with (b)(10) requirements for self-service access. Single-patient export is self-service.

### Summary Stats

```
Classification:  Partial native export
Export format:   CSV + PDF + documents in ZIP
Model type:      Native data model (vendor-specific CSV files)
Entities:        38 (34 CSVs + 2 PDFs + 1 folder + 1 HTML)
Fields:          451 (283 unique, counting journal schema once)
Descriptions:    13.3% of fields have data notes (60/451)
Sample data:     No (1 screenshot only)
Bulk export:     Requires vendor assistance (not self-service)
Domains covered: 15 of 19 applicable domains (10 ✅ + 5 ⚠️)
```

### Bottom Line

Healthie provides a genuine EHI export that covers most of what the platform stores, with particular strength in billing data and wellness-specific journaling. The biggest gap is the absence of structured lab results despite the product's lab integrations, and the reliance on PDF for clinical notes means custom intake forms and assessment data are not machine-readable. A patient would get a reasonably complete copy of their data, but a developer trying to import it would struggle with the thin documentation (13% of fields described, no types, no relationships).
