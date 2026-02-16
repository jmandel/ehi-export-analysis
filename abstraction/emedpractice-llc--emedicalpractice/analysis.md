# EHI Export Analysis: eMedPractice LLC

**Product**: eMedicalPractice v2.0
**Analysis date**: 2026-02-16
**CHPL IDs**: 15.02.05.2898.EMED.01.01.1.220112 (CHPL ID 10787)

## 1. Product Context

eMedicalPractice is a comprehensive, cloud-based ambulatory EHR and practice management platform by eMedPractice LLC (Delray Beach, FL). It integrates EHR, practice management, billing, clearinghouse, revenue cycle management, telemedicine, patient portal, MIPS quality reporting, and e-prescribing (including EPCS) into a single platform. The product targets outpatient clinics across multiple specialties including dermatology, cardiology, pediatrics, behavioral health, allergy/immunology, gastroenterology, chiropractic, ophthalmology, and neurology.

**Data domains the product stores** (baseline for export completeness):
- **Clinical**: Encounter notes, problem lists, medications, allergies, vitals, immunizations, lab orders/results, clinical documents, care plans, referrals, growth charts, AI-generated ambient documentation
- **Prescriptions**: E-prescribing with EPCS, drug interaction checking, pharmacy communications, refill management
- **Billing/RCM**: Claims creation/scrubbing/submission, clearinghouse integration, EOB auto-posting, patient statements, payment processing, copay tracking, financial dashboards
- **Scheduling/PM**: Appointment management, patient registration, insurance eligibility verification, prior authorizations
- **Patient Portal**: Appointment booking, health information viewing, prescription refill requests, document submission, messaging, online payments
- **Communications**: Secure Direct messaging, inbound/outbound faxing, email
- **Telehealth**: Virtual visit capabilities

This is a full-featured ambulatory EHR+PM+Billing platform. A genuine "all EHI" export should cover clinical, billing, insurance, prescribing, and scheduling data at a minimum.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/ehi-export-page.html` (361 KB) | Full HTML of the main EHI export documentation page. WordPress/Elementor page describing C-CDA + CSV export. Contains commented-out Section 4 about document exports. | **High** — primary source for export mechanics |
| `downloads/ehi-export-page-api.json` (14 KB) | WordPress JSON API response for the export page. Cleaner content, confirms page created 2023-09-19, modified 2025-12-05. | **High** — confirms page dates, easier to parse |
| `downloads/ehi-data-dictionary-tables.html` (398 KB) | Full HTML of data dictionary page with 3 table schemas (Patients, Insurance, Appointments). | **High** — primary source for CSV field definitions |
| `downloads/ehi-data-dictionary-tables-api.json` (56 KB) | WordPress JSON API for data dictionary. Created 2025-12-05, modified 2025-12-06. | **High** — cleaner for parsing |
| `downloads/screenshot-ehi-export-page.png` (1.1 MB) | Browser screenshot of export page | Low — confirms rendered layout |
| `downloads/screenshot-ehi-data-dictionary.png` (1.3 MB) | Browser screenshot of data dictionary | Low — confirms rendered layout |
| `downloads/enrichment/data-dictionary.json` (9 KB) | Pre-extracted data dictionary: 3 tables, 61 columns | Medium — verified against my own parse |
| `downloads/enrichment/ehi-export-content.json` (4 KB) | Pre-extracted export page sections | Medium — verified against my own parse |
| `downloads/enrichment/extraction-report.json` (1 KB) | Enrichment accounting | Low — summary only |

**Verification notes**: I independently fetched the live pages (2026-02-16) and confirmed their content matches the downloaded artifacts. The data dictionary still shows 3 tables with 61 columns. The commented-out Section 4 about documents remains in the HTML source.

## 3. Export Mechanics

**Format**: Dual-format export:
1. **C-CDA (XML)** — Per-encounter CDA documents plus a consolidated CDA file per patient, organized in directories by patient chart number
2. **CSV** — Comma-separated file containing demographics, insurance, and appointment data

**Mechanism**: Unclear. The documentation states CSV exports are available via the application's "Reports" section but does not provide step-by-step export instructions for either format. No API endpoint is documented. The export appears to be vendor-assisted or initiated through the application UI, but the process is not described.

**Single-patient vs bulk**: The C-CDA export appears to be per-patient (organized by chart number). It's unclear whether bulk export across all patients is supported or how it would be initiated.

**Access constraints/fees**: None documented.

## 4. Export Content: What's In It

### C-CDA Component

The vendor claims the C-CDA export "includes all data elements defined in USCDI v3, in addition to other EHI the system stores." No sample C-CDA documents are provided, no specific C-CDA templates or sections are listed, and no vendor-specific extensions are documented. The claim is unverifiable from the artifacts alone.

C-CDA is a clinical document standard. Even in the best case, it would cover: demographics, problems, medications, allergies, immunizations, vitals, lab results, procedures, clinical notes, care plans, and referrals. It does **not** naturally represent: billing/claims data, detailed scheduling, e-prescribing workflows, patient portal communications, or many specialty-specific structured assessments.

### CSV Component (Data Dictionary)

The CSV export covers **3 tables with 61 total fields**. None of the 61 fields have descriptions — only column names, data types, default values, and nullability are documented. No value sets, foreign key documentation, or sample data are provided.

### Vendor's own content organization

| Entity/Table | Fields | Described | Types | Vendor Category |
|---|---|---|---|---|
| Patients | 19 | 0 (0%) | 19/19 | Demographics |
| Insurance | 29 | 0 (0%) | 29/29 | Insurance |
| Appointments | 13 | 0 (0%) | 13/13 | Scheduling |
| **Total** | **61** | **0 (0%)** | **61/61** | — |

**Notable issues in the data dictionary:**

1. **Zero field descriptions**: All 61 fields have names and data types but no descriptions. A developer would have to guess what `status`, `PatientRel`, or `FacilityName` contain.

2. **12 coded fields with no value sets**: The following fields appear to be coded values (integers used as foreign keys or enumerations, or strings representing coded categories) but no reference tables or valid values are documented:
   - Patients: `ReferredPhysician` (int), `status` (varchar), `MaritalStatus` (varchar), `Race` (varchar), `Ethnicity` (varchar), `Gender` (varchar)
   - Insurance: `PatientRel` (varchar), `PatientRel1` (varchar)
   - Appointments: `FacilityName` (int), `SchedulerName` (int), `AppointmentType` (int), `AppointmentStatus` (int)

3. **Data type typo**: `InsuredDOB` in the Insurance table is typed as `datet` (apparent typo for `date`).

4. **Denormalized insurance table**: Primary and secondary insurance are flattened into a single row with duplicate column sets (e.g., `InsuranceName` / `InsuranceName2`, `Copay` / `Copay2`), limiting the export to at most 2 insurance records per patient.

5. **Duplicate rendering**: The data dictionary HTML page renders all 3 tables twice (6 HTML `<table>` elements total). Tables 4–6 are exact duplicates of tables 1–3 — likely a WordPress/Elementor layout artifact.

6. **No relationships documented**: `ChartNo` appears in all 3 tables and is clearly the patient identifier / join key, but this relationship is not formally documented.

### Commented-Out Section 4 (Documents)

The export page HTML contains a commented-out `<!-- -->` section describing a document export capability:

> **4. Documents (Scaned Documents like PDF, JPG, PNG File Formats)**
> Includes signed progress notes, lab results, radiology reports, and scanned/uploaded documents. Organized by patient chart number folders with category subfolders.

This section was part of the page at some point (section numbering jumps from 2 to Notes in the visible content, skipping 3 and 4). It's unclear whether the feature was removed or simply hidden from documentation. The misspelling "Scaned" (instead of "Scanned") persists in the HTML.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor describes two export components:

1. **C-CDA clinical data**: Claims to cover USCDI v3 and "other EHI," but provides no specifics beyond the C-CDA standard itself. No sample output, no template list, no vendor-specific extensions documented.

2. **CSV patient details**: Covers only 3 tables — basic demographics (19 fields), insurance enrollment (29 fields covering primary and secondary), and appointments (13 fields). This is an extremely thin data dictionary for a platform that integrates EHR, billing, prescribing, labs, and more.

The CSV component covers **patient-level administrative data only** — no clinical data, no encounter details, no charges, no claims, no prescriptions, no lab results. The vendor appears to rely entirely on C-CDA for clinical content, with the CSV as a supplement for demographic/insurance/scheduling data that C-CDA handles poorly.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | `Patients` table (19 fields) + C-CDA | Covered in CSV with basic fields; no preferred language, no emergency contacts, no guarantor |
| Encounters / visits | ⚠️ Partial | C-CDA claims per-encounter documents | C-CDA likely includes encounter summaries, but no native encounter data table. No visit-level metadata (provider, facility, duration, type) in CSV |
| Problems / conditions | ⚠️ Partial | C-CDA (claimed via USCDI v3) | Relies entirely on C-CDA; no native table. Unverifiable without sample data |
| Medications / prescriptions | ⚠️ Partial | C-CDA (claimed via USCDI v3) | C-CDA covers medication lists but not prescribing workflows, pharmacy responses, EPCS records, or refill management data. Product has full e-prescribing; significant gap |
| Allergies | ⚠️ Partial | C-CDA (claimed via USCDI v3) | Standard C-CDA section; likely adequate for allergy lists |
| Immunizations | ⚠️ Partial | C-CDA (claimed via USCDI v3) | Standard C-CDA section; likely adequate |
| Vitals | ⚠️ Partial | C-CDA (claimed via USCDI v3) | Standard C-CDA section; likely adequate |
| Lab results | ⚠️ Partial | C-CDA (claimed via USCDI v3) | C-CDA covers results but likely not lab orders, order metadata, or bidirectional integration data. Product has bidirectional lab integration |
| Imaging / diagnostic reports | ⚠️ Partial | C-CDA (claimed), commented-out Section 4 mentions radiology reports | Radiology reports may be in C-CDA or document export, but document export is hidden/removed |
| Procedures | ⚠️ Partial | C-CDA (claimed via USCDI v3) | Standard C-CDA section |
| Clinical notes / documents | ⚠️ Partial | C-CDA encounter documents, commented-out Section 4 | C-CDA covers structured notes; scanned documents were described in Section 4 but that section is now hidden |
| Care plans / goals | ⚠️ Partial | C-CDA (claimed via USCDI v3) | Standard C-CDA section if included |
| Orders / referrals | ⚠️ Partial | C-CDA may include referrals | No dedicated order/referral tables in CSV. Prior authorization data not covered |
| Insurance / coverage | ✅ Covered | `Insurance` table (29 fields) | Covers primary and secondary insurance with policyholder details, copay, addresses. No tertiary or historical coverage |
| Claims / billing | ❌ Not covered | No billing entities in either C-CDA or CSV | **Major gap**. Product has integrated billing, RCM, claims, clearinghouse, EOB posting, payment processing. None of this appears in the export |
| Payments | ❌ Not covered | No payment entities | Product processes patient payments, tracks copays and outstanding balances. Not exported |
| Consents / directives | ❌ Not covered | No consent entities | C-CDA may include advance directives if documented |
| Patient communications / portal messages | ❌ Not covered | No communication entities | Product has patient portal with messaging, refill requests, document submission. None exported |
| Specialty-specific data | ❌ Not covered | No specialty entities | Product markets to 9+ specialties with customizable templates. No specialty-specific data tables in the export |

**Summary**: 2 domains have dedicated coverage (Demographics, Insurance). 10 domains have partial coverage via C-CDA claims that cannot be verified. 5 domains have no coverage at all — including billing/claims, which is a core product capability and squarely within the EHI designated record set.

## 6. Documentation Quality

**Can a developer understand and use the export from these docs?**

No. The documentation is insufficient for a developer to build a reliable import:

- **C-CDA component**: No sample documents, no template list, no section inventory, no vendor-specific extensions. The developer would need to receive actual export files and reverse-engineer the content.
- **CSV component**: Column names and data types are provided, but zero field descriptions, zero value set definitions, and zero relationship documentation. A developer seeing `FacilityName` (int) or `AppointmentStatus` (int) has no way to decode the values.
- **No export instructions**: How to initiate an export is not described. The Reports section is mentioned for CSV but with no detail.
- **No sample data**: No example files of any kind.
- **No machine-readable schema**: The data dictionary is inline HTML only — no downloadable JSON, XML Schema, CSV, or other machine-readable format.

**What's well-documented**: Column names and data types are complete (61/61 fields have types). Nullability constraints are specified for every field.

**What requires guesswork**: Everything else — field semantics, valid values, relationships, export process, C-CDA content, document export status.

## 7. Overall Assessment

### Classification

**Minimal/stub**

The export documentation describes a C-CDA + CSV approach, but the CSV component covers only 3 tables with 61 fields (demographics, insurance, appointments) — a trivially small data dictionary for a comprehensive EHR+PM+Billing platform. The C-CDA component claims to include "all EHI" but provides no specifics, no samples, and no verification path. The entire billing/RCM domain — a core product capability — is absent from the export. The documentation is too thin to assess what's actually exported beyond the most basic administrative data.

### Key Findings

1. **Billing data is entirely absent**: Despite eMedicalPractice having integrated billing, RCM, claims, clearinghouse, and payment processing, the export documentation contains zero billing entities. This is a significant compliance gap — billing records are squarely within the HIPAA designated record set.

2. **Only 3 tables / 61 fields in the data dictionary**: For a product that integrates EHR, PM, billing, prescribing, labs, portal, and telehealth, a 3-table data dictionary is orders of magnitude smaller than what a genuine native data export would produce.

3. **Zero field descriptions**: All 61 fields have names and types but no descriptions, no value sets, and no relationship documentation. Twelve fields appear to be coded values (e.g., `AppointmentType` (int), `Race` (varchar)) with no valid values defined.

4. **C-CDA claim is unverifiable**: The vendor claims the C-CDA export includes "all data elements defined in USCDI v3, in addition to other EHI the system stores," but provides no sample output, no C-CDA template list, and no specifics beyond pointing to the HL7 standard.

5. **Commented-out document export**: Section 4 describing scanned document exports (PDFs, images) is present in the HTML source but hidden from the live page — raising questions about whether the capability was removed or simply undocumented.

### Summary Stats

```
Classification:  Minimal/stub
Export format:   C-CDA (XML) + CSV
Model type:      Standard projection (C-CDA) + minimal native tables (CSV)
Entities:        3 (CSV only; C-CDA content unspecified)
Fields:          61
Descriptions:    0% (0/61 fields have descriptions)
Sample data:     No
Bulk export:     Unclear
Domains covered: 2 of 14 applicable domains with dedicated entities; 10 more claimed via C-CDA but unverifiable
```

### Bottom Line

eMedPractice's EHI export documentation is a minimal compliance stub. The CSV component exports only basic demographics, insurance, and appointment data (61 fields across 3 tables), while the C-CDA component makes broad but unverifiable claims about covering "all EHI." The complete absence of billing, claims, payment, prescribing workflow, portal, and specialty data from the documented export — for a product that prominently features integrated billing/RCM — represents a major gap in EHI completeness. A patient or provider requesting their full record would receive a clinical summary and basic administrative data, but not their billing history, claims, payments, detailed prescribing records, portal communications, or specialty-specific clinical data.
