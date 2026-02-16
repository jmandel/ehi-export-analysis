# EHI Export Analysis: Glenwood Systems LLC

**Product**: GlaceEMR 6.0
**Analysis date**: 2026-02-16
**CHPL IDs**: 15.04.04.1535.Glac.06.00.1.180629 (CHPL ID 9559)

## 1. Product Context

GlaceEMR is a cloud-based, ONC-certified Complete EHR from Glenwood Systems LLC (Waterbury, CT), targeting ambulatory outpatient practices across multiple specialties including internal medicine, psychiatry/behavioral health, podiatry, cardiology, neurology, ophthalmology, and urgent care. It combines clinical documentation with integrated practice management and billing capabilities.

**Key data domains the product stores:**
- **Clinical**: Encounter documentation, problem lists, medications (with e-prescribing via SureScripts/EPCS), allergies, vitals, immunizations, lab orders/results, clinical notes (specialty templates), assessments, preventive screenings, care plans
- **History**: Extensive medical, surgical, family, social, substance abuse, pregnancy, obstetric, occupational, and exposure history
- **Billing/Financial**: Charges, claims, procedure codes (CPT), diagnosis codes (ICD-10), payments, adjustments, account balances, insurance (primary/secondary/tertiary), eligibility verification
- **Administrative**: Appointments, scheduling, provider and referring provider records, place of service
- **Documents**: Clinical templates, scanned documents, attachments, C-CDA documents, patient photos
- **Communications**: Patient portal messaging, phone messages, internal messages, reminders
- **Specialty**: Behavioral health (PHQ-9, BIMS, DSM-5 assessments, treatment plans), anticoagulation management (Coumadin tracking)
- **Add-on services**: GlaceRCM (revenue cycle management), GlaceOffice (practice admin), GlaceScribe (AI transcription) — these may store data outside the certified EHR boundary

This sets a high bar: the export should cover clinical, billing, administrative, document, and specialty clinical domains.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/GlaceEMR Export Data Dictionary.pdf` | 62-page PDF data dictionary, Version 1.0 (Nov 27, 2023), 783 KB. Documents all 42 CSV files across EMR (31) and PMS (11) folders with column-level schemas. | **Primary source** — most informative artifact |
| `downloads/transparencydisclosure.html` | Transparency disclosure page (27 KB, last modified Mar 24, 2025). Contains EHI export description, single-patient and population export capabilities, link to data dictionary PDF. | Useful for export mechanics |
| `downloads/enrichment/data-dictionary.json` | Structured JSON extraction of the PDF data dictionary (153 KB). All 42 file schemas with 820 columns. | Used as parsed representation, verified against PDF text |
| `downloads/enrichment/data-dictionary.txt` | Raw `pdftotext` extraction of the PDF (59 KB, 1,888 lines). | Used for verification |
| `downloads/enrichment/extract-data-dictionary.ts` | Bun TypeScript enrichment script (70 KB) encoding the data dictionary. | Reference for understanding extraction approach |
| `downloads/enrichment/README.md` | Enrichment documentation. | Minor |

The data dictionary PDF is the sole substantive artifact. No sample data, no machine-readable schema files (JSON Schema, XSD), and no additional documentation beyond the transparency page were provided.

## 3. Export Mechanics

- **Format**: ZIP file containing CSV files (structured data), HTML + PDF (clinical documents), PNG/JPEG (scanned documents), XML (C-CDA v2), JPG (patient photos)
- **Mechanism**: UI-driven — authorized user triggers export from within GlaceEMR
- **Single-patient**: Yes — exports all EHI for one patient as a ZIP
- **Bulk/population**: Yes — supports exporting a selected group of patients or the entire patient population
- **Access constraints**: Requires authorized user access to GlaceEMR. No fees mentioned in the transparency disclosure.
- **Folder structure**: ZIP contains 5 top-level folders: EMR/, PMS/, Documents/, Photos/, Reference/

## 4. Export Content: What's In It

The data dictionary documents **42 CSV files** with **820 total fields** across two main folders:
- **EMR/** (31 files, 576 fields): Clinical encounter and history data
- **PMS/** (11 files, 244 fields): Practice management, demographics, billing, and reference data

Additionally, the export includes non-CSV content:
- **Documents/**: Clinical templates (HTML+PDF), scanned documents (PNG/JPEG/original format), C-CDA v2 XML, organized per-patient
- **Photos/**: Patient photos in JPG format
- **Reference/**: Schema of exported file content (not further elaborated)

### Documentation quality per field

All 820 fields (100%) have data types documented. Only **164 fields (20.0%)** have descriptions beyond the column name. **113 fields (13.8%)** have comments (which include foreign key references, possible values, or other notes). Many fields are self-explanatory from their names (e.g., "Patient Last Name", "Patient DOB"), but the low description rate means specialized fields rely on naming conventions alone.

### Vendor's own content organization

The vendor organizes content into EMR and PMS folders. Below is the complete entity inventory:

| Entity/Table | Fields | Described | Types | Category |
|---|---|---|---|---|
| EMR/Encounters.csv | 18 | 4 | yes | Clinical Encounters |
| EMR/Vitals.csv | 24 | 4 | yes | Clinical Encounters |
| EMR/Past_Medical_History.csv | 14 | 4 | yes | Medical History |
| EMR/Surgical_History.csv | 15 | 4 | yes | Medical History |
| EMR/Family_History.csv | 16 | 4 | yes | Medical History |
| EMR/Family_Relations_History.csv | 14 | 4 | yes | Medical History |
| EMR/Social_History.csv | 14 | 4 | yes | Medical History |
| EMR/Substance_Abuse_History.csv | 14 | 4 | yes | Medical History |
| EMR/Contraception_Sexual_History.csv | 14 | 4 | yes | Medical History |
| EMR/Pregnancy_History.csv | 15 | 4 | yes | Medical History |
| EMR/Birthing_History.csv | 14 | 4 | yes | Medical History |
| EMR/Menstrual_History.csv | 14 | 4 | yes | Medical History |
| EMR/Occupational_History.csv | 14 | 4 | yes | Medical History |
| EMR/Obstetric_History.csv | 14 | 4 | yes | Medical History |
| EMR/Exposure_History.csv | 14 | 4 | yes | Medical History |
| EMR/Allergies.csv | 19 | 4 | yes | Clinical Data |
| EMR/Assesments.csv | 18 | 4 | yes | Clinical Data |
| EMR/Problem_List.csv | 22 | 4 | yes | Clinical Data |
| EMR/Medications.csv | 26 | 4 | yes | Clinical Data |
| EMR/InactiveMedications.csv | 28 | 4 | yes | Clinical Data |
| EMR/Investigation.csv | 46 | 7 | yes | Clinical Data |
| EMR/Preventive_Screenings.csv | 14 | 3 | yes | Clinical Data |
| EMR/Coumadin.csv | 35 | 5 | yes | Clinical Data |
| EMR/Vaccines.csv | 29 | 5 | yes | Clinical Data |
| EMR/Messages.csv | 22 | 5 | yes | Clinical Data |
| EMR/Reminders.csv | 13 | 3 | yes | Clinical Data |
| EMR/Patient_Photo_Index_File.csv | 12 | 4 | yes | Index Files |
| EMR/Clinical_Document_Index_File.csv | 19 | 7 | yes | Index Files |
| EMR/Phone_Messages_Index_File.csv | 15 | 5 | yes | Index Files |
| EMR/Scan_And_Attachments_Index_File.csv | 18 | 5 | yes | Index Files |
| EMR/CDA_Document_Index_File.csv | 12 | 4 | yes | Index Files |
| PMS/Patient_Demographics.csv | 55 | 3 | yes | Demographics & Insurance |
| PMS/Patient_Insurance.csv | 51 | 6 | yes | Demographics & Insurance |
| PMS/Patient_Account_Balance.csv | 9 | 3 | yes | Billing & Payments |
| PMS/Transactions.csv | 33 | 5 | yes | Billing & Payments |
| PMS/Payment_Receipts.csv | 22 | 5 | yes | Billing & Payments |
| PMS/Payment_Posting.csv | 12 | 3 | yes | Billing & Payments |
| PMS/Appointments.csv | 22 | 3 | yes | Administrative |
| PMS/Master_Insurance_List.csv | 6 | 1 | yes | Reference/Master Lists |
| PMS/Master_POS_List.csv | 4 | 0 | yes | Reference/Master Lists |
| PMS/Master_Provider_List.csv | 16 | 0 | yes | Reference/Master Lists |
| PMS/Master_Referring_Provider_List.csv | 14 | 0 | yes | Reference/Master Lists |

**Category breakdown:**

| Category | Entities | Fields | Fields with Description |
|---|---|---|---|
| EMR - Clinical Encounters | 2 | 42 | 8 |
| EMR - Medical History | 13 | 186 | 52 |
| EMR - Clinical Data | 11 | 272 | 50 |
| EMR - Index Files | 5 | 76 | 25 |
| PMS - Demographics & Insurance | 2 | 106 | 9 |
| PMS - Billing & Payments | 4 | 76 | 16 |
| PMS - Administrative | 1 | 22 | 3 |
| PMS - Reference/Master Lists | 4 | 40 | 1 |
| **Total** | **42** | **820** | **164** |

**Notable entities by size:**
- `PMS/Patient_Demographics.csv` (55 fields): Comprehensive demographics including guarantor, emergency contact, race/ethnicity, language, pharmacy, employer, deceased status
- `PMS/Patient_Insurance.csv` (51 fields): Primary, secondary, and tertiary insurance with full subscriber details and copays
- `EMR/Investigation.csv` (46 fields): Lab orders and results with diagnosis codes, CPT codes, result values, ranges, and status tracking — the deepest clinical entity
- `EMR/Coumadin.csv` (35 fields): Specialty anticoagulation management with INR/PT monitoring, daily dose schedules — a genuinely product-specific data element
- `PMS/Transactions.csv` (33 fields): Billing transactions with procedure codes, charges, diagnosis pointers (4 DX codes), payments, adjustments, balances, authorization numbers

**Standard coding systems referenced:** ICD-9, ICD-10, SNOMED, CPT4, NDC, LOINC, RXNORM, CVX.

**Foreign key relationships** are explicitly documented throughout, enabling relational reconstruction of patient records (Patient ID → Demographics, Encounter ID → Encounters, Insurance IDs → Master Insurance List, etc.).

The full entity inventory with all 820 field definitions is in `analysis/entity-inventory-full.json`.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor's export is organized into two logical domains:

**EMR (Clinical)**: 31 files covering the clinical record. Unusually granular in medical history — 13 separate history categories (past medical, surgical, family, family relations, social, substance abuse, contraception/sexual, pregnancy, birthing, menstrual, occupational, obstetric, exposure). This is more detailed than most EHR exports, which typically roll history into one or two tables. Clinical data coverage includes encounters, vitals, allergies, assessments (multi-coded with ICD-9/10, SNOMED, CPT4, NDC, LOINC, RXNORM), problem lists, active and inactive medications, lab orders/results, preventive screenings, vaccines, a specialty Coumadin tracking module, messages, and reminders. Five index files link to the Documents/Photos folders.

**PMS (Practice Management)**: 11 files covering demographics, insurance (3-tier), billing transactions, payments (receipts + posting), account balances, appointments, and four master/reference lists (insurance, place of service, providers, referring providers). This is genuine billing data — not a stub. `Transactions.csv` has 33 fields including procedure codes, charges, diagnosis pointers, payments, adjustments, balances, authorization numbers, and insurance references. `Payment_Receipts.csv` distinguishes cash/check/card/insurance payments with payment/adjustment/denial codes.

**Documents**: Clinical templates exported in both HTML and PDF (dual format ensures readability and preservation), scanned documents in original format, C-CDA v2 XML documents. All indexed by dedicated CSV files with metadata.

**Thinnest areas**: The master/reference lists (4 entities, 40 fields, only 1 field with a description) are minimal reference tables. Appointments (1 entity, 22 fields) is adequate but sparse.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | `PMS/Patient_Demographics.csv` (55 fields): name, DOB, address, phone, guarantor, emergency contact, race, ethnicity, language, pharmacy, employer, deceased status | Thorough |
| Encounters / visits | ✅ Covered | `EMR/Encounters.csv` (18 fields): encounter date, type, chief complaints, status, service/referring doctor, place of service | Adequate |
| Problems / conditions | ✅ Covered | `EMR/Problem_List.csv` (22 fields) with ICD-10, SNOMED coding, onset date, status, severity, comments | Good depth |
| Medications / prescriptions | ✅ Covered | `EMR/Medications.csv` (26 fields) + `EMR/InactiveMedications.csv` (28 fields) with NDC codes, SIG, dose, frequency, prescriber, start/stop dates | Good — both active and inactive meds |
| Allergies | ✅ Covered | `EMR/Allergies.csv` (19 fields) with allergy type, reaction, severity, NDC codes, status | Good |
| Immunizations | ✅ Covered | `EMR/Vaccines.csv` (29 fields) with CVX codes, manufacturer, lot number, administration site, funding source, VIS date | Thorough |
| Vitals | ✅ Covered | `EMR/Vitals.csv` (24 fields): weight, height, BP (systolic/diastolic), pulse, temp, resp, pulse ox, BMI | Complete |
| Lab results | ✅ Covered | `EMR/Investigation.csv` (46 fields): lab orders and results with CPT codes, diagnosis codes, result values, ranges, units, status, abnormal flags | Deepest clinical entity |
| Imaging / diagnostic reports | ⚠️ Partial | No dedicated imaging entity; may be captured in `Investigation.csv` or clinical documents (HTML/PDF) | Product likely stores imaging orders/results; no explicit imaging table |
| Procedures | ⚠️ Partial | Procedure codes appear in `PMS/Transactions.csv` (billing side) and `EMR/Surgical_History.csv` (history); no dedicated procedures table | Surgical procedures as history; billing-side CPT codes present |
| Clinical notes / documents | ✅ Covered | Clinical templates exported as HTML+PDF in Documents/ folder, indexed by `Clinical_Document_Index_File.csv` (19 fields). Scanned docs, C-CDA v2 XML also included. | Comprehensive — dual-format clinical docs plus scanned attachments |
| Care plans / goals | ⚠️ Partial | No dedicated care plan entity in CSV export. Treatment plans and goals likely captured within clinical document templates (HTML/PDF). | Product has treatment plan features (esp. behavioral health); absence of structured care plan CSV is a gap |
| Orders / referrals | ⚠️ Partial | Lab orders in `Investigation.csv`; medication orders in `Medications.csv`. No dedicated referral/order entity. Referring doctor tracked in `Encounters.csv` and `Transactions.csv`. | E-prescribing orders are implicit; referral workflows not explicitly exported |
| Insurance / coverage | ✅ Covered | `PMS/Patient_Insurance.csv` (51 fields): primary/secondary/tertiary insurance with subscriber details, copays, group/policy numbers. `Master_Insurance_List.csv` for reference. | Thorough — 3-tier coverage |
| Claims / billing | ✅ Covered | `PMS/Transactions.csv` (33 fields): charges, procedure codes, diagnosis pointers (4 DX), submit status, allowed amounts, payments, adjustments, balances, authorization numbers | Genuine billing depth |
| Payments | ✅ Covered | `PMS/Payment_Receipts.csv` (22 fields) + `PMS/Payment_Posting.csv` (12 fields): cash/check/card/insurance payments with adjustment/denial codes, linked to services | Good — receipt and posting detail |
| Consents / directives | ⚠️ Partial | Scanned documents may include consent forms and advance directives (per `Scan_And_Attachments_Index_File.csv`). No dedicated structured consent entity. | Likely present as scanned docs; no structured data |
| Patient communications | ⚠️ Partial | `EMR/Messages.csv` (22 fields) covers phone and internal messages with doctor responses. `Phone_Messages_Index_File.csv` indexes phone message documents. Patient portal messages not explicitly represented. | Phone/internal messages covered; patient portal messaging gap |
| Specialty — Behavioral Health | ⚠️ Partial | No dedicated BH entity. Assessments, PHQ-9, DSM-5 data likely within clinical document templates (HTML/PDF) and possibly `EMR/Assesments.csv`. | Product has significant BH module; structured BH data absent from CSV |
| Specialty — Anticoagulation | ✅ Covered | `EMR/Coumadin.csv` (35 fields): INR/PT values, daily dose schedules (Mon-Sun), target range, comments | Genuinely specialty-specific; excellent |
| Appointments | ✅ Covered | `PMS/Appointments.csv` (22 fields) | Adequate |

**Domains covered**: 12 of 19 applicable domains are fully covered; 7 have partial coverage. No applicable domains are entirely absent — even partially covered domains have some representation (often via clinical documents or implicit fields in other tables).

## 6. Documentation Quality

**Strengths:**
- **Clear structure**: 62-page PDF with consistent table formatting for all 42 files
- **Complete column enumeration**: Every column in every file is listed with a data type
- **Foreign key documentation**: Cross-references between files are explicitly documented (e.g., "Master information found in PMS/Patient_Demographics.csv"), enabling relational reconstruction
- **Value sets for coded fields**: Some fields have possible values documented (encounter status, allergy types, payment types, surgical history underwent values, subscriber relations)
- **Standard code systems identified**: ICD-9, ICD-10, SNOMED, CPT4, NDC, LOINC, RXNORM, CVX all referenced where used

**Weaknesses:**
- **Low description rate**: Only 164 of 820 fields (20.0%) have descriptions beyond the column name. Most fields rely on self-explanatory naming.
- **No sample data**: No example CSV rows, no sample export files
- **No machine-readable schema**: No JSON Schema, XSD, or DDL — only the PDF
- **Loose type specifications**: Many fields typed as "String" with no length, format, or pattern constraints. Date/time formats not specified.
- **No value set documentation for many coded fields**: Encounter Type, Appointment Type, document categories, and many other coded fields lack enumerated values
- **Single version**: v1.0 from November 2023 with no updates in 2+ years
- **Reference folder undocumented**: The export includes a "Reference" folder described as containing "the schema of the exported file content" but no details are provided about its contents

**Could a developer build an import?** Yes, for the CSV data — column names are clear enough and relationships are documented. The main challenge would be interpreting coded fields that lack value set documentation. Clinical documents (HTML/PDF) would require human reading for content not captured in structured CSV.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Comprehensive**

GlaceEMR's export demonstrably covers the breadth of data domains the product stores. It goes well beyond USCDI/clinical summary data to include genuine billing depth (charges, payments, adjustments, denial codes, account balances), comprehensive insurance data (3-tier), extensive medical history (13 separate categories — more granular than most EHRs), specialty clinical data (Coumadin anticoagulation management), and clinical documents in their original formats. The PMS folder with 11 files and 244 fields represents real practice management data, not a stub. The main gaps are structural rather than categorical — behavioral health assessments and care plans are likely exported within clinical document templates (HTML/PDF) rather than as structured CSV data, and patient portal messaging isn't explicitly mapped. For an ambulatory EHR of this scale, the export covers the expected breadth.

**Axis 2 — Export approach: Purpose-built EHI export**

This is clearly a purpose-built (b)(10) export, not a repackaged clinical exchange. The evidence is strong:
1. The export is CSV-based (not FHIR or C-CDA), representing the vendor's internal data model
2. It includes billing and practice management data (PMS folder) that would never appear in a (g)(10) or C-CDA export
3. The 62-page data dictionary is purpose-written for this export with column-level schemas, not repurposed API documentation
4. Specialty-specific content (Coumadin tracking with 35 fields) is exported as a dedicated entity
5. The export includes clinical documents in their original HTML/PDF format alongside the C-CDA XML — the C-CDA is supplementary, not the primary format
6. 13 separate history files reflect the EHR's internal data model, not a standards projection

### Key Findings

1. **Genuine purpose-built export with both clinical and billing depth**: 42 CSV files, 820 fields across EMR and PMS folders, with standard coding systems (ICD-10, SNOMED, CPT4, NDC, LOINC, RXNORM, CVX) and documented foreign key relationships. The PMS folder with transactions, payments, and insurance data is real billing export, not a stub.

2. **Unusually granular medical history**: 13 separate history categories (past medical, surgical, family, family relations, social, substance abuse, contraception/sexual, pregnancy, birthing, menstrual, occupational, obstetric, exposure) provide more historical depth than most EHR exports.

3. **Specialty clinical data exported**: The Coumadin tracking entity (35 fields with daily dose schedules and INR/PT monitoring) demonstrates product-specific clinical content beyond generic templates.

4. **Documentation is functional but thin on descriptions**: While all 820 fields have types and the relational structure is well-documented, only 20% of fields have descriptions. No sample data, no machine-readable schemas, and data dictionary hasn't been updated since November 2023.

5. **Behavioral health and care coordination gaps in structured data**: The product's significant behavioral health module (PHQ-9, BIMS, DSM-5) and care plan features don't have dedicated CSV files. This content is likely within clinical document templates (HTML/PDF), meaning it's exported but not in a computationally accessible form.

### Summary Stats

```
Coverage:        Comprehensive
Approach:        Purpose-built EHI export
Export format:   CSV (structured data) + HTML/PDF/PNG/JPEG/XML (documents)
Entities:        42 CSV files + 3 document types + photos + reference schema
Fields:          820
Descriptions:    20.0% of fields with descriptions
Sample data:     No
Bulk export:     Yes (single-patient and population)
Domains covered: 12 of 19 fully, 7 of 19 partially (0 N/A, 0 absent)
```

### Bottom Line

GlaceEMR provides a solid, purpose-built EHI export that covers both clinical and billing data in a practical CSV format with documented relationships. A patient or provider would receive a usable, reasonably complete copy of their data — structured clinical records, billing transactions, insurance details, and clinical documents in readable formats. The biggest gap is that specialty clinical content (behavioral health assessments, care plans) is exported only within HTML/PDF clinical documents rather than as structured CSV data, limiting computability for those domains.
