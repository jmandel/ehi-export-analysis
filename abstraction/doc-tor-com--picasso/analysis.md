# EHI Export Analysis: Doc-tor.com

**Product**: Picasso v8.2
**Analysis date**: 2026-02-15
**CHPL ID**: 15.04.04.2985.Pica.08.06.1.250604 (listing ID 11652)

## 1. Product Context

Picasso is an integrated cloud-based ambulatory EHR, practice management, and revenue cycle management (RCM) suite developed by Doc-tor.com (acquired by Harris Healthcare / Constellation Software in 2020). It targets independent physician practices, clinically integrated networks, and billing companies, serving 550+ practices and 2,200+ clinicians primarily in the NY/NJ/PA region.

The product has four integrated components:
- **Picasso EHR**: Clinical documentation with 1,000+ specialty templates, CPOE for meds/labs/imaging, drug interaction checking, e-prescribing (via NewCrop), lab results, document management, immunization registry reporting
- **Picasso Practice Management**: Scheduling, patient registration, eligibility verification, charge posting, claims management, payment posting, KPI dashboards
- **Picasso Community (Patient Portal)**: Secure messaging, medication history, appointment scheduling, online bill pay
- **Revenue Cycle Management**: Claims creation/submission, payment posting, denial management, financial analytics

For (b)(10) completeness, the export should cover clinical data (encounters, notes, meds, labs, vitals, allergies, problems, immunizations, procedures, orders, care plans), billing/claims/payment data, insurance/coverage information, patient portal communications, and documents/attachments. The product is certified across 37 ONC criteria including (b)(10) EHI Export.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `Picasso-EHI-Export-Documentation-V1_0-1.pdf` (3 pages, 154 KB) | **Picasso-specific** EHI export data dictionary. 21 data classes, 441 columns, CSV format. Created 2024-01-04 by Kathiresan Palanisamy. Found on mandatory disclosures page. | **Primary source** — the actual Picasso export specification |
| `Picasso-EHI-Export-Documentation-V1_0-1-1.pdf` (8 pages, 195 KB) | **Amazing Charts** EHI export data dictionary, mislabeled with a Picasso filename. 44 data classes, 1,094 columns, CSV/JSON/XML format. Created 2023-10-16 by Kathiresan Palanisamy. This is the CHPL-registered URL. | **Contextually useful** — shows what a sister product exports, highlights gaps in Picasso's export |
| `PAA_API_documentation.pdf` (4 pages, 175 KB) | Picasso Application Access API documentation. SOAP web service returning USCDI-compliant CCD XML. Created 2023-01-06 by Nathan Marmelo. | **Not relevant to (b)(10)** — this is a (g)(10) clinical API, not the EHI bulk export |
| `enrichment/picasso-data-classes.json` (12 KB) | Machine-parsed extraction of the Picasso PDF: 21 data classes with column names | Useful pre-existing parse, verified against raw PDF |
| `enrichment/amazing-charts-data-classes.json` (33 KB) | Machine-parsed extraction of the Amazing Charts PDF: 44 data classes with column names | Useful pre-existing parse, verified against raw PDF |

**Note on the registered URL**: The CHPL-registered URL (`Picasso-EHI-Export-Documentation-V1_0-1-1.pdf`) points to an Amazing Charts document, not a Picasso document. The document's title is "Amazing Charts EHI Export: Folder Organization and Data Format Specification" and its column naming convention (PascalCase, e.g., `PatientID`, `EncounterDate`) differs entirely from Picasso's ALL_CAPS convention (e.g., `VISITID`, `ENCOUNTERDATE`). A separate Picasso-specific document exists at a different URL found on the mandatory disclosures page. Both were authored by the same person (Kathiresan Palanisamy at Harris Healthcare).

## 3. Export Mechanics

- **Format**: CSV files — one `.csv` file per data class per patient
- **Folder structure**: `ScheduledExport_MM-dd-yyyy hhmmss/` → `{PatientID}/` → `{DataClassName}.csv` + `Attachments/` subfolder
- **Scope**: Supports single-patient and patient-population export
- **Additional files**: An `Attachments` subfolder preserves documents and other data in their original format
- **Mechanism**: The documentation references a "ScheduledExport" folder naming convention but does not describe how to trigger the export (which menu, which role, what parameters). No UI screenshots or step-by-step instructions are provided.
- **Access constraints**: No fees or access constraints mentioned in the documentation
- **Bulk capability**: Yes — the document states it supports "exporting data for a patient population"

## 4. Export Content: What's In It

### Data dictionary characteristics

The Picasso-specific EHI export documentation provides:
- **21 data classes** with a total of **441 columns**
- **Column names only** — no data types, no field descriptions, no value sets, no constraints
- **No relationship documentation** — foreign keys (e.g., `VISITID`, `PROVIDERSID`) must be inferred from shared column names
- **No sample data** — no example CSV files or records
- **No machine-readable schema** — the data dictionary is embedded in a PDF as a two-column table

### Vendor's own content organization

The Picasso export organizes data into 21 "Data Classes." The vendor does not use explicit categories — the listing is flat. I've grouped them by clinical domain based on content:

| Data Class | Columns | Category (inferred) | Notable fields |
|---|---|---|---|
| Demographics | 51 | Administrative | Name, DOB, SSN, address, race/ethnicity, language, sex orientation, gender identity, preferred pharmacy, referring provider |
| Health Insurance | 51 | Insurance / Coverage | Payer info, policy/group numbers, subscriber details, insured party, responsible party (guarantor), case codes |
| Encounters | 28 | Administrative | VISITID, visit type, E/M code, encounter diagnoses, responsible provider, facility info, open/close dates |
| Medications | 27 | Clinical | Drug ID, name, dosage, duration, frequency, route, form, strength, prescribing provider, active status |
| Immunizations | 27 | Clinical | Vaccine name, CVX code, CPT code, lot, manufacturer, route, site, consent info, provider |
| Plan Of Treatment | 26 | Clinical | Category, description, E/M code, referred provider details (name, address, specialty) |
| Labs | 24 | Clinical | Test description, value, LOINC codes, reference range, abnormal flags, result status, units |
| Assessment | 23 | Clinical | Diagnosis ID, coding language (ICD/SNOMED), type, stability, start/inactive dates, provider |
| Tasks | 22 | Clinical | Queue ID, summary, notes, category, status, assigned/started/completed dates |
| Implantable Devices | 22 | Clinical | UDI, device name, brand, company, model number, MRI safety, implant date |
| Allergies | 19 | Clinical | Allergen name, type, RxNorm code, severity, provider |
| Orders | 18 | Clinical | Lab ID, test code/description, LOINC code, CPT code, visit ID, provider |
| Vitals | 17 | Clinical | Height, weight, BP, pulse, respiration, temp, O2 sat, head circumference, O2 flow rate |
| Problems | 16 | Clinical | Diagnosis ID, short description, coding language, type, start/inactive dates |
| Clinical Notes | 15 | Clinical | Note ID, full note text, visit ID, visit type, encounter date, provider |
| Procedures | 15 | Clinical | CPT procedure ID, date, description, coding, up to 3 modifiers |
| Health Concerns | 13 | Clinical | Concern name, note, code, date added, provider |
| Care Team | 12 | Administrative | Provider ID, specialty, contact info, active/disabled status |
| Family History | 7 | Clinical | Family member, disease name, SNOMED code, onset age, age of death |
| Social History | 4 | Clinical | Category name, value, date added, date of occurrence |
| Tobacco | 4 | Clinical | Unique ID, value, diagnosis ID, date added |

**Total: 21 data classes, 441 columns, 0 field descriptions, 0 data types documented.**

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The Picasso export covers the core clinical EHR workflow reasonably well: encounters, clinical notes, medications, labs, vitals, allergies, problems, immunizations, procedures, orders, care plans, and implantable devices are all present. Insurance/coverage information is detailed (51 columns covering payer, subscriber, insured, and guarantor data).

**Strengths**:
- Demographics is thorough (51 columns including USCDI v3 elements like sex orientation, gender identity, previous name)
- Health Insurance is deep (51 columns with payer, subscriber, insured, and responsible party detail)
- Labs include LOINC codes, reference ranges, and abnormal flags
- Immunizations include CVX codes, lot numbers, manufacturer, route, and consent info
- Implantable Devices include full UDI detail

**Weaknesses**:
- **No billing/claims/payment data** — the most significant gap for an integrated EHR/PM/RCM suite
- **No patient portal messages** — no secure messaging or patient communications
- **No referral management data** — Plan of Treatment includes referred provider fields, but there's no dedicated referral tracking class
- **No advance directives** or patient-generated data classes
- **Clinical Notes are thin** — only 15 columns (note ID, text blob, visit linkage, provider) vs. Amazing Charts' 88-column structured SOAP note with embedded vitals, tobacco, pregnancy, vision, hearing data
- **Social History is minimal** — 4 columns (category/value pairs) with no structured data
- **No documents/attachments metadata** — the Attachments subfolder is mentioned but has no data dictionary entry describing what's included

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | `Demographics` (51 fields) including race, ethnicity, language, sex orientation, gender identity, preferred pharmacy | Thorough |
| Encounters / visits | ✅ Covered | `Encounters` (28 fields) with visit type, E/M code, diagnoses, facility, provider | Adequate |
| Problems / conditions | ✅ Covered | `Problems` (16 fields) + `Assessment` (23 fields) with ICD/SNOMED codes | Adequate |
| Medications / prescriptions | ✅ Covered | `Medications` (27 fields) with drug ID, dosage, frequency, route, strength | No e-prescribing transaction data (SureScripts status, pharmacy transmit) |
| Allergies | ✅ Covered | `Allergies` (19 fields) with RxNorm codes, severity | Adequate |
| Immunizations | ✅ Covered | `Immunizations` (27 fields) with CVX codes, lot, manufacturer, consent | Thorough |
| Vitals | ✅ Covered | `Vitals` (17 fields) including O2 sat, head circumference, O2 flow rate | Adequate |
| Lab results | ✅ Covered | `Labs` (24 fields) with LOINC codes, reference ranges, abnormal flags | Adequate |
| Imaging / diagnostic reports | ❌ Not covered | No imaging-specific data class | Product supports CPOE for imaging orders (a)(3) but export has no imaging results. Orders class covers lab orders only (fields reference LABID, LABTESTCODE). |
| Procedures | ✅ Covered | `Procedures` (15 fields) with CPT codes and modifiers | Adequate |
| Clinical notes / documents | ⚠️ Partial | `Clinical Notes` (15 fields) — note text blob + metadata. Attachments subfolder mentioned but undocumented. | Notes are present but unstructured (single NOTETEXT field vs. structured SOAP sections). No metadata schema for attachments. |
| Care plans / goals | ⚠️ Partial | `Plan Of Treatment` (26 fields) with referral provider details | No separate Goals data class (present in Amazing Charts). Health Concerns (13 fields) partially fills this role. |
| Orders / referrals | ⚠️ Partial | `Orders` (18 fields) focused on lab orders. No dedicated referral entity. | Product likely manages referrals; Plan Of Treatment has referral provider fields but no referral tracking (dates, status, number of visits). |
| Insurance / coverage | ✅ Covered | `Health Insurance` (51 fields) with payer, subscriber, insured, guarantor | Thorough |
| Claims / billing | ❌ Not covered | No billing, claims, charges, or superbill data class | **Major gap.** Product has full PM and RCM with claims management, charge posting, payment posting, denial management. The Amazing Charts sister document includes "Billing History" (74 fields). |
| Payments | ❌ Not covered | No payment data class | **Major gap.** Product handles payment posting and reconciliation. |
| Consents / directives | ❌ Not covered | No advance directives or consent data class | Product likely stores consents. Amazing Charts includes "Advance Directives" (14 fields). |
| Patient communications / portal messages | ❌ Not covered | No messaging or communication data class | Product has Picasso Community patient portal with secure messaging. Amazing Charts includes "Email" (11 fields). |
| Specialty-specific data | N/A | No specialty-specific clinical modules identified | Product claims 1,000+ specialty templates, but these appear to be note templates, not specialty data models |

**Summary: 10 of 18 applicable domains covered, 3 partial, 5 not covered.**

## 6. Documentation Quality

The Picasso EHI export documentation is **minimal**:

- **What's provided**: Column names for 21 data classes in a 3-page PDF, plus a brief prose description of the folder structure and file naming convention
- **What's missing**: Data types, field descriptions, value sets, constraints, cardinality, relationships/foreign keys, sample data, export trigger instructions, error handling, versioning beyond "v1.0"
- **Machine-readability**: None. The data dictionary is a PDF table with no machine-readable alternative (no JSON schema, no XSD, no DDL, no CSV/TSV data dictionary)
- **Developer usability**: A developer receiving this export would have CSV headers but would need to reverse-engineer data types, relationships, coded values, and business rules from actual exported data. Building a reliable import would require significant trial and error.
- **No export instructions**: Neither document explains how to trigger the export — which menu item, which user role, what parameters are available, what the output looks like in practice

The documentation is the bare minimum to demonstrate that an export exists and what data classes it contains. It falls well short of enabling independent implementation.

## 7. Overall Assessment

### Classification

**Partial native export**

The Picasso EHI export is a genuine native data model export (CSV dump of internal database tables, not a FHIR/C-CDA projection), which is the right approach for (b)(10). However, it has significant coverage gaps — most notably the complete absence of billing, claims, and payment data from a product whose core value proposition includes integrated practice management and revenue cycle management. The documentation is column-names-only with no types, descriptions, or sample data.

### Key Findings

1. **The CHPL-registered URL points to the wrong product's documentation.** The registered URL (`Picasso-EHI-Export-Documentation-V1_0-1-1.pdf`) contains an "Amazing Charts EHI Export" data dictionary (44 data classes, 1,094 columns) — a different Harris Healthcare product with a completely different database schema. The actual Picasso data dictionary (21 data classes, 441 columns) exists at a separate URL found only on the mandatory disclosures page.

2. **Billing/claims/payment data is entirely absent.** For an integrated EHR + PM + RCM suite that processes claims, payments, denials, and manages accounts receivable, the export contains zero billing entities. The Amazing Charts sister document includes a comprehensive "Billing History" class with 74 columns; Picasso's export has nothing comparable. This is the single largest gap.

3. **The export is roughly half the scope of the sister product's export.** Picasso: 21 data classes, 441 columns. Amazing Charts: 44 data classes, 1,094 columns. The 23 data classes present in Amazing Charts but absent from Picasso include billing (74 cols), email/communications (11 cols), referrals (12 cols), advance directives (14 cols), patient-generated data (31 cols combined), next of kin (17 cols), and several clinical classes.

4. **Documentation provides no field descriptions, types, or value sets.** All 441 columns are documented only by name — no data types, no descriptions, no coded value definitions, no relationship documentation. This is a column-name-only data dictionary.

5. **Core clinical domains are adequately covered.** Despite the gaps, the export does cover demographics, encounters, medications, labs, vitals, allergies, problems, immunizations, procedures, orders, care plans, and insurance at a native database level with reasonable field depth (441 columns across 21 clinical/administrative classes).

### Summary Stats

```
Classification:  Partial native export
Export format:   CSV
Model type:      Native database
Entities:        21 data classes
Fields:          441 columns
Descriptions:    0% (column names only)
Sample data:     No
Bulk export:     Yes (single-patient and population)
Domains covered: 10 of 18 applicable domains (3 partial, 5 missing)
```

### Bottom Line

Picasso's EHI export takes the right structural approach — a native CSV dump of clinical database tables rather than a FHIR/C-CDA repackaging — but it covers only about half of what the product stores. The complete absence of billing, claims, payment, and patient portal data from an integrated EHR/PM/RCM suite is a significant compliance gap under (b)(10). The registered URL pointing to a different product's documentation compounds the problem, making it unclear to patients and regulators exactly what data the Picasso export actually provides.
