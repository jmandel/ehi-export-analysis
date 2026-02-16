# EHI Export Analysis: Healthie

**Product**: Healthie  
**Analysis date**: 2026-02-16  
**CHPL IDs**: 15.04.04.3130.Heal.01.00.1.221207 (CHPL ID 11055)

## 1. Product Context

Healthie is a cloud-based EHR and practice management platform focused on health and wellness professionals, particularly virtual-first care. It serves 25,000+ providers managing 10M+ patient records. Key specialties include behavioral health, nutrition/dietetics, health coaching, women's health, chronic care management, and substance use treatment.

The platform is an all-in-one system combining:
- **Clinical charting & documentation**: customizable note templates, AI Scribe, split-screen charting during telehealth
- **Scheduling & calendar**: appointment booking, recurring appointments, availability management
- **E-prescribing**: via DoseSpot integration (medications, EPCS, PDMP)
- **Lab ordering**: via Rupa Health, Evexia, Fullscript integrations
- **Insurance billing & revenue cycle**: superbills, CMS 1500 claims, clearinghouse integrations (ClaimMD, Office Ally), ERA processing, eligibility checks, patient invoicing
- **Telehealth**: HIPAA-compliant video sessions
- **Patient portal & engagement**: secure messaging, document sharing, health programs
- **Food & lifestyle journaling**: photo-based food logging, nutrient tracking (900K+ foods), mood/hunger tracking, activity logging, biometric metrics, wearable sync (Fitbit, Google Fit, Apple Health)
- **Intake forms**: customizable electronic forms
- **Document management**: uploads, e-fax

This product breadth means a genuine (b)(10) export should cover clinical data, billing/insurance, patient communications, custom forms, journaling/wellness data, and documents.

## 2. Artifacts Reviewed

| Artifact | Description | Informative? |
|---|---|---|
| `downloads/ehi-export-page.html` (53 KB) | Main (b)(10) documentation page with complete data dictionary for all 38 export files | **Primary source** — most informative |
| `downloads/enrichment/data-dictionary.json` (47 KB) | Structured JSON extraction of the data dictionary: 38 files, 451 columns | Used to verify HTML parse; confirmed accurate |
| `downloads/client-metrics-example.png` (159 KB) | Screenshot of client_metrics.csv pivot-table layout | Marginally useful |
| `downloads/screenshot-*.png` (4 files) | Browser screenshots of documentation page | Useful for visual verification |
| `downloads/enrichment/extract-data-dictionary.ts` (10 KB) | TypeScript enrichment script | Reviewed for methodology |
| `downloads/enrichment/extraction-log.json` (2 KB) | Extraction accounting: 38/38 files parsed, 0 errors | Confirmed completeness |

## 3. Export Mechanics

- **Format**: Per-patient ZIP archive containing 34 CSV files, 2 PDF files, 1 HTML file, and 1 documents folder
- **Mechanism**:
  - *Single patient*: UI button in patient profile → Charting section. Requires "Can generate organization report" permission or non-organization user.
  - *Population/bulk*: Administrator-only; must email Healthie Support at hello@gethealthie.com with subject "Patient Population b10 export request." Not self-service.
- **Structure**: Population export creates one directory per patient named `<FirstName><LastName><UniqueIdentifier>`
- **Access constraints**: Population export is vendor-assisted (not self-service for admins)
- **Fees**: Not mentioned in documentation
- **Data types**: All CSV values exported as strings; blank cells indicate no data

## 4. Export Content: What's In It

The export contains **38 files** with **451 total fields** across 34 CSV files. Only **60 fields (13.3%)** have any description beyond the field name. No fields have documented data types (all are noted as "exported as a string"). No foreign keys, relationships, or value sets are documented.

### Vendor's own content organization

The vendor does not organize the data dictionary into categories; each file is documented individually with a column listing. I have categorized them below based on content.

| Entity/File | Fields | Described | Category |
|---|---|---|---|
| **Demographics & Care Team** | | | |
| Client_Overview.csv | 14 | 2 | Demographics |
| Addresses.csv | 6 | 0 | Demographics |
| Family_and_Contacts.csv | 5 | 0 | Demographics |
| Client_User_Groups.csv | 2 | 0 | Demographics |
| Provider.csv | 12 | 0 | Care Team |
| Other_Care_Team_Members.csv | 12 | 0 | Care Team |
| Referring_Physicians.csv | 12 | 0 | Care Team |
| **Clinical** | | | |
| Allergies.csv | 11 | 0 | Clinical |
| Diagnoses.csv | 4 | 2 | Clinical |
| Medications.csv | 10 | 3 | Clinical |
| CarePlans.csv | 3 | 1 | Clinical |
| Goals.csv | 7 | 0 | Clinical |
| Recommendations.csv | 2 | 0 | Clinical |
| Charting.pdf | 0 (PDF) | — | Clinical Notes |
| **Billing & Insurance** | | | |
| cms1500s.csv | 25 | 5 | Claims |
| superbills.csv | 10 | 0 | Billing |
| Payments.csv | 15 | 3 | Payments |
| Insurance.csv | 2 | 0 | Insurance |
| Insurance_authorizations.csv | 23 | 0 | Insurance |
| Policies.csv | 19 | 5 | Insurance |
| Packages.csv | 19 | 2 | Billing/Packages |
| **Journaling & Wellness Tracking** | | | |
| FoodEntry.csv | 21 | 6 | Journaling |
| MetricEntry.csv | 21 | 6 | Journaling |
| MirrorEntry.csv | 21 | 6 | Journaling |
| NoteEntry.csv | 21 | 6 | Journaling |
| PoopEntry.csv | 21 | 0 | Journaling |
| SleepEntry.csv | 21 | 0 | Journaling |
| SymptomEntry.csv | 21 | 0 | Journaling |
| WaterIntakeEntry.csv | 21 | 0 | Journaling |
| WorkoutEntry.csv | 21 | 0 | Journaling |
| Food_Intolerances.csv | 11 | 0 | Food Allergies |
| Food_Preferences.csv | 11 | 0 | Food Allergies |
| Food_Sensitivities.csv | 11 | 0 | Food Allergies |
| client_metrics.csv | 8 | 6 | Metrics |
| journal_entries.pdf | 0 (PDF) | — | Journaling |
| **Patient Communications** | | | |
| Messages.csv | 8 | 6 | Messaging |
| **Documents & Export Metadata** | | | |
| Documents folder | — | — | Documents |
| format.html | — | — | Metadata |

**Notable patterns:**
- 9 journal entry files (FoodEntry, MetricEntry, MirrorEntry, NoteEntry, PoopEntry, SleepEntry, SymptomEntry, WaterIntakeEntry, WorkoutEntry) share an **identical 21-column schema**, suggesting a single polymorphic "Entry" table differentiated by category. This inflates the apparent entity count — functionally these are one entity type with 9 category filters.
- 3 food sensitivity files (Food_Intolerances, Food_Preferences, Food_Sensitivities) also share an identical 11-column schema mirroring Allergies.csv.
- The **Charting.pdf** and **journal_entries.pdf** are rendered PDFs, not structured data — their fields are organization-specific and undocumented.
- The **Documents folder** exports uploaded documents in original format with folder structure preserved.

**De-duplicated effective entity count**: Removing identical schemas, the export has approximately **18 unique entity structures** covering 451 nominal fields (~230 unique fields after deduplication of the 9 identical journal schemas and 3 identical food sensitivity schemas).

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The export spans five broad areas:

1. **Demographics & Care Team** (7 files, 63 fields): Basic patient info (name, DOB, gender, pronouns, contact), addresses, family contacts, provider and care team details, referring physicians. Moderate depth — covers essentials but lacks race, ethnicity, language, and sexual orientation fields that Healthie likely stores.

2. **Clinical** (7 files, 37 fields): Allergies (11 fields including coded reactions), diagnoses (4 fields: code, active, onset/end), medications (10 fields including dosage/frequency/route), care plans (3 fields: name, description, hidden), goals (7 fields), recommendations (2 fields), and charting notes (PDF). Clinical coverage is **thin** — no immunizations, no vitals, no procedures, no lab results, no encounters. The charting PDF captures note content but in an unstructured format.

3. **Billing & Insurance** (7 files, 113 fields): This is the **deepest category**. CMS 1500 claims (25 fields), superbills (10 fields), payments (15 fields with Stripe integration details), insurance policies (19 fields with holder demographics), insurance authorizations (23 fields), and packages (19 fields for service packages). This goes well beyond USCDI.

4. **Journaling & Wellness Tracking** (14 files, 230 nominal fields): This is Healthie's **distinctive contribution** — food logging, metrics, sleep, bowel, symptoms, workouts, selfies, water intake, and notes. These are wellness-specific data types not found in traditional EHRs. However, the 9 identical schemas suggest limited structural differentiation between entry types. Also includes food intolerances/preferences/sensitivities.

5. **Patient Communications** (1 file, 8 fields): Secure messages with conversation threading, timestamps, autoresponse flags, and deletion tracking.

6. **Documents** (folder): All uploaded documents in original format.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | `Client_Overview.csv` (14 fields), `Addresses.csv` (6 fields) | Missing race, ethnicity, language, sexual orientation — fields Healthie stores per USCDI certification |
| Encounters / visits | ❌ Not covered | No encounters or appointments file | Product has scheduling/appointments — significant gap |
| Problems / conditions | ⚠️ Partial | `Diagnoses.csv` (4 fields: code, active, onset, end) | Very thin — no description text, no coding system indicator |
| Medications / prescriptions | ⚠️ Partial | `Medications.csv` (10 fields) | Has basics but no prescriber, no pharmacy, no RxNorm code system indicator |
| Allergies | ✅ Covered | `Allergies.csv` (11 fields with coded reactions) | Adequate with reaction codes and system names |
| Immunizations | ❌ Not covered | No immunizations file | Product is certified for (a)(14) immunization recording — gap |
| Vitals | ❌ Not covered | No vitals file; `client_metrics.csv` covers weight/height/BMI/body fat only | Product stores vitals per clinical charting — gap. client_metrics is a pivot-table format, not individual readings |
| Lab results | ❌ Not covered | No lab results file | Product integrates with lab partners (Rupa Health, Evexia) — gap if results are stored |
| Imaging / diagnostic reports | N/A | No imaging file | Product does not appear to have imaging module |
| Procedures | ❌ Not covered | No procedures file | Product records procedure codes on superbills — gap |
| Clinical notes / documents | ⚠️ Partial | `Charting.pdf` (unstructured PDF), `Documents folder` | Notes exported but as PDF — not machine-readable; documents exported in original format |
| Care plans / goals | ✅ Covered | `CarePlans.csv` (3 fields), `Goals.csv` (7 fields) | Thin but present |
| Orders / referrals | ❌ Not covered | No orders or referrals file | Product supports referral workflows and lab ordering — gap |
| Insurance / coverage | ✅ Covered | `Policies.csv` (19 fields), `Insurance.csv` (2 fields), `Insurance_authorizations.csv` (23 fields) | Good depth with policy holder details and authorizations |
| Claims / billing | ✅ Covered | `cms1500s.csv` (25 fields), `superbills.csv` (10 fields) | Solid — includes claim status, amounts, procedure codes |
| Payments | ✅ Covered | `Payments.csv` (15 fields) | Includes Stripe integration, refunds, taxes |
| Consents / directives | ❌ Not covered | No consents file | Product has intake forms including consent collection — gap |
| Patient communications | ✅ Covered | `Messages.csv` (8 fields) | Secure messaging with threading |
| Specialty: Nutrition/wellness journaling | ✅ Covered | 9 Entry CSVs + `journal_entries.pdf` + `client_metrics.csv` + 3 food sensitivity files | Deep coverage of Healthie's distinctive wellness features |

**Summary**: 7 of 18 applicable domains are covered, 4 are partially covered, 7 are not covered.

## 6. Documentation Quality

The documentation is **functional but minimal**:

- **Data dictionary exists**: Yes — every export file is listed with its column names.
- **Field descriptions**: Only 60 of 451 fields (13.3%) have any description. Most descriptions are brief format notes (e.g., "Year-Mo-Day", "true or false") rather than semantic explanations.
- **Field types**: Not documented. All values exported as strings with no type indicators.
- **Relationships/foreign keys**: Not documented. No indication of how files relate to each other (e.g., how cms1500s.csv links to Policies.csv).
- **Value sets/code systems**: Not documented. Fields like "Category Type" and "Status" have no enumerated values.
- **Sample data**: No sample data files provided; one screenshot of client_metrics.csv format.
- **Machine-readable schema**: No formal schema (no JSON Schema, no XSD). The enrichment JSON is a third-party extraction.

A developer could understand the basics of each file but would need significant guesswork for data types, relationships, value constraints, and semantic meaning of most fields. The documentation is a bare minimum column listing, not a usable integration specification.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Partial**

The export covers some domains well — particularly billing/insurance (7 files, 113 fields) and wellness journaling (14 files, 230 fields) — while completely omitting others that the product demonstrably stores. The most significant gaps are:
- **No encounters/appointments**: despite scheduling being a core feature
- **No immunizations**: despite (a)(14) certification for immunization recording
- **No vitals**: despite clinical charting capabilities
- **No lab results**: despite lab ordering integrations
- **No procedures**: despite procedure code recording
- **No intake forms/custom forms**: despite this being a key feature
- **No consents**: despite electronic consent collection

The billing and journaling coverage is genuinely beyond USCDI, which is a positive signal. But the clinical data is surprisingly thin — only allergies, diagnoses, medications, care plans, goals, and recommendations are structured. All charting notes are exported as a single PDF, losing structure.

**Axis 2 — Export approach: Purpose-built EHI export**

This is a purpose-built export, not a repackaged C-CDA or FHIR export. The evidence:
- CSV-based format using Healthie's own data model (not FHIR resources or C-CDA sections)
- Includes non-USCDI data domains (billing, payments, wellness journaling, secure messages)
- Has its own dedicated help article specifically for (b)(10)
- Includes Healthie-specific entities (FoodEntry, PoopEntry, MirrorEntry, client_metrics) that would never appear in a clinical exchange standard
- Population export has a dedicated workflow (even if vendor-assisted)

However, it's a purpose-built export that is **incomplete** — the effort was real but didn't cover the full breadth of what Healthie stores.

### Key Findings

1. **Billing/insurance is the strongest area**: 7 files with 113 fields covering CMS 1500 claims, superbills, payments, insurance policies, and authorizations. This goes well beyond USCDI and represents genuine (b)(10) effort.

2. **Wellness journaling is distinctive but structurally repetitive**: 14 files covering Healthie's unique food/exercise/sleep/symptom tracking. However, 9 of these share an identical 21-column schema, suggesting a single polymorphic table rather than 9 distinct entities.

3. **Core clinical data has major gaps**: No immunizations, vitals, lab results, procedures, or encounters — all of which the product stores. Clinical charting is exported only as unstructured PDF.

4. **Documentation is bare-minimum**: Only 13.3% of fields have any description, and those descriptions are mostly format hints ("Year-Mo-Day"), not semantic definitions. No types, no relationships, no value sets.

5. **Population export is not self-service**: Bulk export requires emailing vendor support, creating a friction point and dependency for organizations needing to export all patient data.

### Summary Stats

    Coverage:        Partial
    Approach:        Purpose-built EHI export
    Export format:   CSV + PDF + Documents folder (ZIP)
    Entities:        38 files (18 unique structures after deduplication)
    Fields:          451 (nominal) / ~230 (unique after deduplication)
    Descriptions:    13.3% (60 of 451 fields)
    Sample data:     No
    Bulk export:     Yes (vendor-assisted, not self-service)
    Domains covered: 7 of 18 applicable domains fully; 4 partially

### Bottom Line

Healthie built a genuine (b)(10) export — not a repackaged clinical exchange — with real depth in billing/insurance and wellness journaling. However, the export has significant clinical gaps: no immunizations, vitals, lab results, procedures, encounters, or intake forms despite the product storing all of these. A patient would get their billing records, secure messages, and food journals, but would be missing meaningful portions of their clinical record.
