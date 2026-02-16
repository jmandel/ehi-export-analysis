# Nextech — EHI Export Documentation

Collected: 2026-02-16

## Source
- Registered URL: https://www.nextech.com/hubfs/Nextech%20Select_NexCloud%20EHI%20Export%20Documentation.pdf
- CHPL IDs: 11722 (Nextech Select and NexCloud), 11723 (Nextech Select and NexCloud with NewCropRx)
- Certification date: 2025-12-02

## Navigation Journal

**Step 1: Probe the registered URL**

```bash
curl -sI -L "https://www.nextech.com/hubfs/Nextech%20Select_NexCloud%20EHI%20Export%20Documentation.pdf" -H 'User-Agent: Mozilla/5.0'
```

Result: HTTP 200, `Content-Type: application/pdf`, 265,621 bytes. Direct PDF download from HubSpot (Cloudflare CDN). No redirects.

**Step 2: Download the original PDF**

```bash
curl -sL "https://www.nextech.com/hubfs/Nextech%20Select_NexCloud%20EHI%20Export%20Documentation.pdf" -H 'User-Agent: Mozilla/5.0' -o Nextech_Select_NexCloud_EHI_Export_Documentation.pdf
```

7-page PDF, authored by Hristina Arsovska in Microsoft Word, created 2023-11-16. This is the original version registered at CHPL.

**Step 3: Extract embedded URLs from the PDF**

The PDF contains a hyperlink on the text "Nextech Select/NexCloud EHI Data Dictionary" pointing to:
`https://www.nextech.com/compliance/ehi-export-documentation`

This is Nextech's compliance EHI export documentation hub page.

**Step 4: Fetch the compliance hub page**

```bash
curl -sL "https://www.nextech.com/compliance/ehi-export-documentation" -H 'User-Agent: Mozilla/5.0' -o compliance-ehi-export-documentation.html
```

Result: HTML page (92,339 bytes). This is a HubSpot-hosted page listing EHI export documentation for multiple Nextech products. The page includes download links for several products; the relevant Nextech Select/NexCloud files are:

- `Nextech Select_NexCloud EHI Export Documentation_2025.pdf` — updated (2025) version of the export documentation
- `Nextech Select_NexCloud EHI Export Data Dictionary_2025.xlsx` — Excel data dictionary

Also on the page (for other Nextech products, not downloaded):
- `Nextech EHR (powered by ICP) EHI Export Documentation.pdf`
- `Nextech EHR (powered by ICP) EHI Data Dictionary-1.xlsx`
- `EHI Single Export Data Dictionary_10.28.25.xlsx`
- `SRSPro EHI Export Documentation_10.30.25_.pdf`

**Step 5: Download the 2025 updated documentation**

```bash
curl -sL "https://www.nextech.com/hubfs/Nextech%20Select_NexCloud%20EHI%20Export%20Documentation_2025.pdf" -H 'User-Agent: Mozilla/5.0' -o Nextech_Select_NexCloud_EHI_Export_Documentation_2025.pdf
curl -sL "https://www.nextech.com/hubfs/Nextech%20Select_NexCloud%20EHI%20Export%20Data%20Dictionary_2025.xlsx" -H 'User-Agent: Mozilla/5.0' -o Nextech_Select_NexCloud_EHI_Export_Data_Dictionary_2025.xlsx
```

Both confirmed: PDF (729,375 bytes, 8 pages) and XLSX (56,430 bytes, 16 sheets).

**Step 6: Verify downloads**

- `file` command confirms PDF document and Microsoft Excel 2007+ format
- No login walls, no anti-bot issues, no JavaScript required

## What Was Found

Nextech provides a genuine (b)(10) EHI export — not a repackaged FHIR/g(10) API. The export produces a **per-patient ZIP file** containing:

### Export Format

The export is a ZIP file per patient, named `FirstNameInitial_LastName_PersonID_DateTimeStamp.ZIP`, containing:

1. **CSV folder** — 14 CSV files with structured clinical discrete data:
   - `Appointments.csv` (52 fields)
   - `PatientDemographics.csv` (212 fields — very comprehensive)
   - `Charges.csv` (140 fields)
   - `Payments.csv` (50 fields)
   - `CustomData.csv` (7 generic fields — practice-specific custom fields)
   - `Follow up.csv` (16 fields)
   - `Notes.csv` (23 fields)
   - `Insurances.csv` (85 fields)
   - `Recalls.csv` (27 fields)
   - `RecallsSteps.csv` (17 fields)
   - `PaymentPlans.csv` (13 fields)
   - `PracYakker.csv` (10 fields — internal messaging)
   - `iPad Tasks.csv` (15 fields)
   - `iPad Notes.csv` (9 fields)

2. **EMN folder** — One PDF per encounter (Electronic Medical Note), containing the full encounter documentation. Content is customizable per practice; the data dictionary describes ~43 common fields/sections.

3. **Documents folder** — All attached documents: photos, images, eCR reportability responses, direct message attachments, online visit attachments, clinical/summary of care documents.

4. **iPad Documents folder** — Documents from iPad Select application.

5. **CCDA file** — Standard C-CDA XML containing demographics, allergies, medications, problems (including SDOH), procedures (including SDOH interventions), labs, immunizations, vitals, goals (including SDOH), assessments, care team, implantable devices, and more.

6. **ReadMe file** — Public link to documentation.

### Data Dictionary

The XLSX data dictionary has **16 sheets** and **730 field definitions** across all export entities. Each field has a name, description, and optional note. Fields do not include explicit data types. Key observations:

- **Charges** (140 fields): Extremely detailed — includes CPT codes, ICD codes, modifiers, quantities, fees, adjustments, bill status, provider info, facility, referring provider, insurance info, authorization data, and more.
- **Patient Demographics** (212 fields): Very comprehensive — covers name, addresses, contact info, race/ethnicity, language, insurance identifiers, guarantor info, employer, emergency contacts, referral sources, custom fields, consent flags, marketing preferences, and portal access.
- **Payments** (50 fields): Payment method, amount, adjustments, check/CC info, insurance payments, copay tracking.
- **Insurances** (85 fields): Primary/secondary/tertiary coverage, subscriber details, group numbers, copays, deductibles, authorization info.
- **EMN** (43 fields): Encounter structure fields — title, sections, assessment/plan items, vitals, review of systems — noting that actual content is highly customizable per practice.

### 2023 vs 2025 Version Differences

The 2025 version (8 pages) is an updated and expanded version of the 2023 original (7 pages). Key additions in the 2025 version:
- Note about configurations with third-party PM systems (PM data not included in those cases)
- iPad billing data exclusion note
- Expanded CCDA data classes including SDOH Problems, SDOH Interventions, SDOH Assessments, SDOH Goals, Clinical Tests, Diagnostic Imaging, Disability Status, Pregnancy Status
- "DSI feedback" sheet added to the data dictionary (11 fields — Decision Support Intervention feedback tracking)
- Custom data export now explicitly notes field name exposure

## Export Coverage Assessment

### Data Domain Coverage

**Clearly covered:**
- **Patient demographics** — 212 fields, extremely comprehensive. Includes identifiers, contacts, insurance info, guarantor, employer, emergency contacts, race/ethnicity/language, consent preferences, portal access status.
- **Billing/charges** — 140 fields covering CPT, ICD-10, modifiers, fees, adjustments, billing status, authorization data. This is genuine billing data, not a summary.
- **Payments** — 50 fields including payment method, amounts, adjustments, insurance payments, copay tracking. Linked to charges via Bill ID.
- **Insurance data** — 85 fields covering multiple insurance tiers, subscriber info, copays, deductibles, authorization details.
- **Payment plans** — 13 fields for installment/payment plan tracking.
- **Clinical encounters (EMN)** — Full encounter notes exported as PDFs. While not structured data, this captures the complete clinical documentation including specialty-specific content (dermatology findings, ophthalmology exams, plastic surgery notes).
- **Appointments** — 52 fields including scheduling, provider, location, status, confirmation, and linked recall data.
- **Allergies, medications, problems, procedures, labs, immunizations, vitals** — via CCDA export, covering USCDI data classes.
- **Notes** — 23 fields capturing notes from across the system (clinical, billing, labs, appointments, reminders, history).
- **Documents/images** — All attached documents, clinical photos, eCR responses, direct message attachments, online visit attachments, clinical summaries.
- **Custom data** — Practice-specific custom fields and values exported.
- **Internal messaging (PracYakker)** — Including deleted messages.
- **Recalls/follow-ups** — Patient recall tracking with linked steps.
- **SDOH data** — Explicitly mentioned in 2025 version: SDOH Problems, Interventions, Assessments, Goals.

**Potentially missing or unclear:**
- **Prescription/e-prescribing data** — The NewCropRx variant (CHPL 11723) adds e-prescribing via DrFirst/NewCrop integration. Medications appear in the CCDA, but there is no dedicated CSV export for prescription details (Rx numbers, pharmacy routing, controlled substance tracking, prescription status). It's unclear whether the EMN PDFs fully capture this data or if it resides only in the DrFirst/NewCrop system (external to Nextech's database).
- **CRM/marketing data** — The product research identifies Nextech CRM (lead tracking, campaign data, communication logs) as part of the integrated platform. No CRM data appears in the export. This may be a separately licensed module, but if deployed as part of the same product, its patient-related data could be EHI.
- **Inventory/POS data** — Product and injectable inventory tracking is a documented feature. No inventory data appears in the export, though inventory transactions tied to specific patients (e.g., injectable tracking) could constitute EHI.
- **Referral details** — Referral management with automatic letter generation is a product feature. The CCDA includes "Reason for Referral" and the demographics CSV has referring provider fields, but there's no dedicated referral tracking export (referral status, recipient, letters sent).
- **Telehealth/online visit data** — The product supports integrated telehealth. Online visit attachments are exported in the Documents folder, but session metadata (dates, duration, provider) is not explicitly covered.
- **Patient portal interactions** — Portal messages, patient-completed forms, and self-scheduling data are product features. Portal message content doesn't appear to have a dedicated export (PracYakker covers internal messaging, not patient-facing).

### Export Format & Standards

The export uses a **multi-format approach** that is well-suited for comprehensive EHI export:

- **CSV files** for structured discrete data — easily parseable, clearly documented field-by-field
- **PDF files** for encounter notes (EMN) — preserves the customized clinical documentation layout
- **C-CDA XML** for standardized clinical data — covers USCDI data classes
- **Native documents/images** — preserves original format

This is a good approach. The CSV format is appropriate for the tabular data (billing, demographics, insurance). The CCDA provides standards-based clinical data. The EMN PDFs preserve the full clinical encounter including specialty-specific content that wouldn't map well to structured formats. The inclusion of attached documents/images ensures nothing is lost.

The one format concern is that **EMN encounter data is only available as PDF**, meaning the structured clinical data within encounters (diagnoses, vitals, procedures, findings) is not machine-readable beyond what's in the CCDA. A practice's ophthalmology exam data — IOP readings, visual acuity, slit lamp findings — would be in the EMN PDFs but not in a queryable format.

Relationships between CSV files are documented: Charges-Payments linked by Bill ID, Payments-PaymentPlans linked by Payment Plan ID/Payment ID, Recalls-Appointments linked by Appointment ID. This is sufficient for reconstruction.

### Documentation Quality

The documentation is **above average** for EHI export compliance:

- Clear, well-organized PDF describing the export structure, folder hierarchy, file naming, and data relationships
- Field-level data dictionary in XLSX with 730 fields across 16 sheets — one sheet per export entity
- Each field has a name and description; some have additional notes explaining values or behavior
- The documentation explains edge cases: empty CSVs for missing data, deleted records included with status flags, inactive patients included
- Billing data relationships (charges → payments → payment plans) are explicitly documented
- The 2025 update adds SDOH data classes and configuration-dependent notes

**Weaknesses:**
- No explicit data types (all fields described by name and text description only)
- No value set documentation for coded fields (e.g., what values does "Appointment Status" take?)
- No sample export files or worked examples
- No schema files (no CSV headers template, no XSD for CCDA customizations)
- The EMN documentation explicitly states the fields are "best practice" and may vary — the actual schema is unknowable without seeing a specific practice's configuration

### Structure & Completeness

**Granularity**: Field-level documentation with name + description + optional notes. This is adequate for understanding what's exported but insufficient for automated import — a developer would need sample data to understand data types, formats, and coded values.

**Relationships**: Key relationships between CSV files are documented (Bill ID, Payment Plan ID, Appointment ID, Recall Step ID). Patient ID links all files.

**Coded fields**: Not documented with value sets. Fields like "Appointment Status," "Charge Status," "Payment Method" are described but their possible values are not enumerated.

**Versioning**: Two versions available (2023 original, 2025 update). The 2025 version supersedes the original with expanded SDOH coverage and configuration notes. No formal changelog.

## Overall Assessment

Nextech has done genuine (b)(10) work. This is **not** a repackaged FHIR API — it's a purpose-built export covering structured billing data, insurance, demographics, appointments, and notes in CSV format, clinical encounters in PDF format, standardized clinical data in CCDA, and all attached documents. The 730-field data dictionary across 16 export entities demonstrates significant investment in the export mechanism.

The export covers the core data domains well: clinical documentation, billing, payments, insurance, demographics, appointments, notes, and documents. The multi-format approach (CSV + PDF + CCDA + documents) is pragmatic and covers more ground than a FHIR-only export would for a specialty EHR with highly customizable encounter templates.

The main gaps relate to peripheral product features (CRM, inventory, telehealth metadata) whose EHI status depends on whether they're part of the same product and whether the data is used for patient decisions. The lack of a structured export for encounter clinical data (beyond CCDA) is a limitation for specialty practices where the richest clinical data lives in custom EMN templates — but this is a common challenge for specialty EHRs with highly configurable documentation.

## Access Summary
- Final URL (after redirects): https://www.nextech.com/hubfs/Nextech%20Select_NexCloud%20EHI%20Export%20Documentation.pdf
- Compliance hub: https://www.nextech.com/compliance/ehi-export-documentation
- Status: found
- Required browser: no
- Navigation complexity: direct_link (original PDF), one_click (updated files from compliance hub)
- Anti-bot issues: none

## Obstacles & Dead Ends

None. The registered URL worked immediately. The compliance hub page was accessible and well-organized with clear download links for each product's documentation.
