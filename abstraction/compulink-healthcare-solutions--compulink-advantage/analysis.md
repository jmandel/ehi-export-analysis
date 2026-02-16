# EHI Export Analysis: Compulink Healthcare Solutions

**Product**: Compulink Advantage, Version 12
**Analysis date**: 2026-02-16
**CHPL IDs**: 15.04.04.2701.Comp.12.00.1.171106 (8873)

## 1. Product Context

Compulink Advantage is an all-in-one specialty EHR and practice management platform serving 13+ medical specialties (strongest in ophthalmology/optometry) across 20,000+ providers and 4,700+ locations. The product integrates:

- **EHR**: Clinical documentation, specialty templates (e.g., glaucoma flowsheets, cataract/LASIK), e-prescribing, lab interfacing, clinical decision support
- **Practice Management**: Scheduling, patient registration, insurance verification
- **Billing / RCM**: Integrated billing, claim generation/scrubbing, denial management, payments
- **Patient Engagement**: Portal, online scheduling, digital forms, automated messaging, referral tracking
- **Optical POS**: Frame/lens inventory, sales, job costing
- **ASC Management**: Case scheduling, anesthesia documentation, surgical supply tracking
- **Imaging**: DICOM integration, PACS

This is an extensive data footprint. A genuine (b)(10) export should cover clinical records, billing/claims, specialty-specific data (especially ophthalmic), optical POS transactions, documents/images, and patient engagement data.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/COMPULINK-PHIEXPORT-DOCUMENTATION.pdf` | 7-page PDF (267 KB). Only artifact available. 2 pages of technical content describe the export file structure (CSV naming, image naming, FLD files, table relationships). 2 pages of legal/usage terms. 3 pages of cover/TOC/blank. Created 2023-10-05 by Steven Polk via Microsoft Word. | **Low** — describes the export container format but provides no data dictionary, no table listing, no field definitions, no sample data. |

No other artifacts exist. No supplementary HTML pages, JSON schemas, sample exports, or data dictionaries were found at the vendor's website. The FLD files referenced in the PDF are only available as part of an actual export.

## 3. Export Mechanics

- **Format**: Flat CSV files (one per database table) + native image files (PDF, PNG, JPG), packaged in a **password-protected ZIP** file. Accompanied by `.FLD` text files containing field name/description pairs.
- **Mechanism**: In-application function ("PHI Export"). The PDF references "eLearning Help Manual and Compulink University" for instructions on running the export.
- **Single-patient vs bulk**: Supports both. Single-patient export uses `P###_` prefix; bulk export uses `P0_` prefix with all patients in one file per table.
- **Access constraints**: No additional fees for the export function itself. Cloud-hosted clients may incur fees if export size exceeds contracted storage. Password is provided when the function completes.

## 4. Export Content: What's In It

The PDF provides almost no detail about what the export contains. It describes the *structure* of the output (file types, naming conventions, linking keys) but not the *content* (which tables, which fields, what values).

### What is documented

**Tables mentioned by name**: Only 5 table names appear in the PDF:
1. `PATIENT` — key demographic information
2. `EXAM` — main exam/encounter record
3. `EXAMDIAG` — exam diagnosis sub-table
4. `DOCUMENT` — demographics document metadata
5. `EXAMIMAG` — exam image metadata

**Fields mentioned by name**: Only 7 unique field names across all tables (8 field entries total, as EXAMUNIQUE appears in both EXAM and EXAMDIAG):
- `PATUNIQUE` — patient identifier (join key for demographics/billing tables)
- `EXAMUNIQUE` — exam identifier (join key for exam sub-tables)
- `DOCUNIQUE` — document unique ID (links to D-type images)
- `IMAGUNIQUE` — image unique ID (links to E-type images)
- `ERXCONSENT` — E-Rx History Consent (from PATIENT.FLD snippet)
- `GENDERIDENTITYNOTE` — Gender Identity Note (from PATIENT.FLD snippet)
- `SEXUALORIENTATIONNOTE` — Sexual Orientation Note (from PATIENT.FLD snippet)

**Data types**: Not documented for any field.
**Value sets**: Not documented.
**Relationships**: Described in prose only: demographics/billing tables linked by PATUNIQUE, exam tables linked by EXAMUNIQUE, images linked via DOCUNIQUE/IMAGUNIQUE.

### Data dictionary mechanism

The PDF explicitly states: "Due to the comprehensive customization allowed within the software, there is no 'one size fits all' list of fields." Instead, `.FLD` files are generated alongside each CSV in the export. These contain `Name: FIELDNAME, Description: field description` pairs. Only 3 example entries are shown (the PATIENT fields listed above).

This means the actual data dictionary is **only available inside an export** — it is not published statically and cannot be reviewed without obtaining an export from a Compulink practice.

### Vendor's own content organization

The PDF categorizes export files into two groups:

| Category (vendor's) | Tables Named | Fields Named | Description |
|---|---|---|---|
| Demographics/Billing | PATIENT, DOCUMENT | PATUNIQUE, DOCUNIQUE, ERXCONSENT, GENDERIDENTITYNOTE, SEXUALORIENTATIONNOTE | "All CSV files where the table name does not start with EXAM" |
| Exam | EXAM, EXAMDIAG, EXAMIMAG | EXAMUNIQUE, IMAGUNIQUE | "All CSV files where the table name starts with EXAM" |

The vendor describes the export as containing "patient demographics, medical records, billing records, images, and more" but provides no enumeration of what "more" includes.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor organizes exported data into two broad categories — Demographics/Billing and Exam — plus image files. The PDF's language ("patient demographics, medical records, billing records, images, and more") suggests the export is intended to be a comprehensive database dump of all patient-related tables.

The CSV-per-table approach and the inclusion of native image files is architecturally sound for a full EHI export. If the export truly includes all tables in the database that contain patient data, it could be comprehensive. However, **no evidence is provided to verify what tables are actually exported**. The documentation names only 5 tables out of what is likely hundreds in a product this complex.

The FLD file mechanism for field descriptions is a reasonable approach to dynamic documentation, but its non-publication makes independent assessment impossible.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | PATIENT table mentioned; 3 demographic field names shown | Table exists but field inventory unknown. Product stores extensive demographics. |
| Encounters / visits | ⚠️ Partial | EXAM table mentioned as "prominent" | Table exists but no field details. Likely the core encounter record. |
| Problems / conditions / diagnoses | ⚠️ Partial | EXAMDIAG table mentioned | Table exists but no field details. |
| Medications / prescriptions | ❌ Not covered | No medication table mentioned; only ERXCONSENT field in PATIENT | Product has e-prescribing via Surescripts; no evidence medications are exported. |
| Allergies | ❌ Not covered | No allergy table mentioned | Product is certified for (a)(3) maintain active allergy list; no evidence in export docs. |
| Immunizations | ❌ Not covered | No immunization table mentioned | Product certified for clinical data; no evidence in export docs. |
| Vitals | ❌ Not covered | No vitals table mentioned | Product stores vitals per EHR functionality; no evidence in export docs. |
| Lab results | ❌ Not covered | No lab table mentioned | Product has lab interfacing; no evidence in export docs. |
| Imaging / diagnostic reports | ⚠️ Partial | EXAMIMAG table + native image files exported | Image metadata and files are included. DICOM/PACS data coverage unknown. |
| Procedures | ❌ Not covered | No procedure table mentioned | Product has ASC module with surgical data; no evidence in export docs. |
| Clinical notes / documents | ⚠️ Partial | DOCUMENT table mentioned + document image files | Document metadata table exists; note content format/completeness unknown. |
| Care plans / goals | ❌ Not covered | No care plan table mentioned | Product certified for (a)(12) family health history; no care plan evidence. |
| Orders / referrals | ❌ Not covered | No order or referral table mentioned | Product has SMART Orders and referral portal; no evidence in export docs. |
| Insurance / coverage | ❌ Not covered | No insurance table mentioned | Product has insurance verification; no evidence in export docs. |
| Claims / billing | ❌ Not covered | PDF mentions "billing records" in passing but no billing table named | Product has full billing/RCM; mentioned in category name but no specifics. |
| Payments | ❌ Not covered | No payment table mentioned | Product has text-to-pay, digital payments; no evidence in export docs. |
| Consents / directives | ❌ Not covered | No consent table mentioned (ERXCONSENT is a single field) | Product has digital forms with e-signatures; no evidence in export docs. |
| Patient communications | ❌ Not covered | No communications table mentioned | Product has automated messaging, portal; no evidence in export docs. |
| Specialty-specific (ophthalmology) | ❌ Not covered | No specialty table mentioned | Product's core identity is specialty eye care; no evidence in export docs. |

**Note**: The ❌ ratings above mean "no evidence in the documentation" — not necessarily "absent from the export." The export's CSV-per-table approach could include all of these domains if the underlying database tables are included. The documentation simply provides no way to verify this.

## 6. Documentation Quality

The documentation is **poor** by any standard for enabling third-party use of the export:

- **Can a developer understand and use the export?** No. A developer would know to expect CSV files, images, and FLD files in a ZIP, and how they link together. But they would not know what tables exist, what fields those tables contain, what data types to expect, or what coded values mean.
- **What's well-documented?** File naming conventions and top-level table relationships (PATUNIQUE/EXAMUNIQUE linking) are clearly described.
- **What requires guesswork?** Everything about actual data content. Which tables are in the export, what fields they have, what values are valid, what data types are used — all unknown without obtaining an actual export.
- **Machine-readable artifacts?** None published. The FLD files are machine-readable but only available inside exports. No JSON schema, no sample data, no static data dictionary.
- **Reconstructability**: A developer could not build an import system from this documentation. They would need an actual export to reverse-engineer the schema.

The 7-page PDF dedicates only 2 pages to technical content. The rest is title page, blank page, table of contents, and legal terms. For a product serving 13+ specialties with EHR, billing, optical POS, and ASC modules, this is extremely thin.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Minimal/stub/unclear**

The documentation is too thin to assess actual coverage. While the export mechanism described (CSV dump of database tables + images) is *architecturally* capable of being comprehensive, the PDF provides zero evidence of what tables are actually exported. Only 5 table names are mentioned out of what is likely hundreds in a product spanning EHR, practice management, billing, optical POS, ASC management, and patient engagement across 13+ specialties. The phrase "patient demographics, medical records, billing records, images, and more" is the sole claim of breadth, with no substantiation.

The vendor's approach of deferring the data dictionary to dynamically-generated FLD files means there is no publicly-reviewable evidence of export scope. This could be a genuinely comprehensive export — or it could be a narrow subset. The documentation makes it impossible to tell.

**Axis 2 — Export approach: Purpose-built EHI export**

Despite the documentation being thin, the export is clearly not a repackaged C-CDA or FHIR (g)(10) export. The CSV-per-database-table format with FLD field descriptions, native image files, and a two-category organization (Demographics/Billing vs Exam) is a purpose-built mechanism for database-level export. The naming conventions (P###_TABLENAME.csv), join key structure (PATUNIQUE, EXAMUNIQUE), and per-table FLD files indicate a custom export function built specifically for (b)(10), not a relabeling of existing clinical exchange capabilities.

### Key Findings

1. **Purpose-built but undocumented**: The export mechanism (CSV database dump + images + FLD files in ZIP) is architecturally appropriate for (b)(10) and is clearly purpose-built — not a repackaged C-CDA or FHIR export. However, the documentation provides essentially no visibility into what data is actually exported.

2. **Only 5 of unknown-total tables named**: The PDF mentions PATIENT, EXAM, EXAMDIAG, DOCUMENT, and EXAMIMAG as examples. For a product with EHR, billing, optical POS, ASC, and patient engagement modules, the actual database likely has dozens or hundreds of tables. None beyond these 5 are identified.

3. **Data dictionary exists only inside exports**: The FLD file mechanism is a reasonable approach to documenting a customizable schema, but publishing no static data dictionary means third parties cannot assess export completeness without first obtaining an export from a practice.

4. **No sample data provided**: No example CSV files, no example FLD files (beyond a 3-line snippet), no sample ZIP structure. A developer cannot prepare an import without an actual export in hand.

5. **Two pages of substance**: The entire technical documentation for a complex, multi-specialty platform fits on 2 pages. The remaining 5 pages are cover, blank, TOC, and legal terms — the legal section is longer than the technical content.

### Summary Stats

    Coverage:        Minimal/stub/unclear
    Approach:        Purpose-built EHI export
    Export format:   CSV + native images in password-protected ZIP
    Entities:        5 mentioned (total unknown)
    Fields:          8 entries across 7 unique names (total unknown)
    Descriptions:    3 of 7 mentioned fields have descriptions (43%); full descriptions in FLD files not publicly available
    Sample data:     No
    Bulk export:     Yes (P0_ prefix for all patients)
    Domains covered: Cannot determine — documentation names 5 tables covering ~3-4 domains but claims "demographics, medical records, billing records, images, and more"

### Bottom Line

Compulink built a purpose-specific EHI export function that dumps database tables as CSVs with dynamically generated field descriptions — an architecturally sound approach. However, the public documentation is a 2-page structural overview with no data dictionary, no table listing, no sample data, and no way to verify what the export actually covers. For a product spanning 13+ specialties with EHR, billing, optical, and surgical modules, the documentation gap makes it impossible to assess whether patients receive a complete copy of their data or just a fraction.
