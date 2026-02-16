# EHI Export Analysis: Compulink Healthcare Solutions

**Product**: Compulink Advantage, Version 12
**Analysis date**: 2026-02-16
**CHPL IDs**: 15.04.04.2701.Comp.12.00.1.171106 (8873)

## 1. Product Context

Compulink Advantage is a specialty-focused, all-in-one EHR and practice management platform from Compulink Healthcare Solutions (founded 1985, ~200 employees, 20,000+ providers). It serves 13+ medical specialties with strongest presence in ophthalmology/optometry, and also covers orthopedics, dermatology, behavioral health, pain management, ENT, gastroenterology, podiatry, urology, audiology, addiction medicine, and physical therapy.

The product is a broad integrated platform encompassing:
- **EHR**: Specialty-specific clinical documentation, e-prescribing (Surescripts), lab interfacing, clinical decision support, problem lists, medications, allergies, vitals, immunizations, care plans
- **Practice Management**: Scheduling, patient registration, insurance verification
- **Billing/RCM**: Claim generation, denial management, payment processing
- **Patient Engagement**: Patient portal, online scheduling, digital forms, messaging
- **Optical POS**: Frame/lens inventory, sales, job costing (ophthalmology/optometry)
- **ASC Management**: Surgical scheduling, anesthesia documentation, pre/post-op assessments
- **Imaging**: DICOM integration, PACS for image storage
- **Analytics**: Clinical, financial, and operational reporting

This breadth means a complete EHI export should cover clinical documentation, billing/claims, specialty-specific assessments (especially ophthalmic data), imaging metadata, and patient engagement data across all these modules.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `COMPULINK-PHIEXPORT-DOCUMENTATION.pdf` | 7-page PDF (267 KB). Created Oct 5, 2023 by Steven Polk via Microsoft Word. Contains 2 pages of technical content describing the export file format, 2+ pages of legal terms, and cover/TOC/blank pages. **No data dictionary, no table listing, no field definitions, no sample data.** | Low — describes export structure but not content |

**Only one artifact exists.** No additional EHI export documentation was found on the vendor's certification page, which lists only this PDF for (b)(10). The vendor's mandatory disclosures page references other documents (FHIR API docs, DICOM conformance, etc.) but none relate to EHI export content.

## 3. Export Mechanics

- **Format**: Flat CSV files (one per database table) + native image files (PDF, PNG, JPG), packaged as a **password-protected ZIP file**. Field description files (.FLD) accompany each CSV.
- **Mechanism**: Built-in product function ("PHI Export"). The PDF references "eLearning Help Manual and Compulink University content" for how to run the function, suggesting a UI-driven process.
- **Single-patient vs bulk**: Supports both. Single-patient export uses `P###_` prefix; bulk export of all patients uses `P0_` prefix.
- **Access constraints**: No additional fees for the export function itself. Cloud-hosted clients may incur fees if export size exceeds contracted storage. Password for the ZIP is provided when the function completes.
- **Naming conventions**: Tables: `P###_TABLENAME.csv`. Images: `P###_E/D###_####.ext` (E=exam image, D=demographics image).

## 4. Export Content: What's In It

### What the documentation tells us

The PDF describes the export as containing "patient demographics, medical records, billing records, images, and more" but **provides no enumeration of what tables or fields are included**. The document explicitly states that field-level documentation is provided via dynamically generated .FLD files included in each export, because "comprehensive customization" means fields vary per installation.

### Explicitly mentioned entities

Only 5 table names are referenced in the documentation, all as illustrative examples rather than a comprehensive listing:

| Entity/Table | Fields Shown | Category (vendor's) | Role |
|---|---|---|---|
| PATIENT | 4 (3 example + PATUNIQUE) | Demographics/Billing | Primary demographics table |
| EXAM | 1 (EXAMUNIQUE) | Exam | Primary exam/encounter table |
| EXAMDIAG | 1 (EXAMUNIQUE FK) | Exam | Exam diagnoses |
| DOCUMENT | 1 (DOCUNIQUE) | Demographics/Billing | Demographics document metadata |
| EXAMIMAG | 1 (IMAGUNIQUE) | Exam | Exam image metadata |

**Total explicitly documented: 5 tables, 3 described fields** (ERXCONSENT, GENDERIDENTITYNOTE, SEXUALORIENTATIONNOTE — all from the PATIENT table's FLD file snippet).

### Key relationship structure

The PDF describes a two-category organization:
1. **Demographics/Billing files**: All CSVs where the table name does NOT start with "EXAM." Linked by `PATUNIQUE` (patient identifier).
2. **Exam files**: All CSVs where the table name starts with "EXAM." Linked by `EXAMUNIQUE` (exam identifier). Sub-tables (e.g., EXAMDIAG) link back to the main EXAM table.

Images link via:
- Demographics images (D prefix) → `DOCUNIQUE` in the DOCUMENT table
- Exam images (E prefix) → `IMAGUNIQUE` in the EXAMIMAG table

### What we cannot verify

The export *approach* (CSV dump of all database tables) is structurally capable of exporting all EHI. However, without a table listing, sample export, or published FLD files, it is impossible to verify from this documentation:
- How many tables are actually exported
- What fields each table contains
- Whether specialty-specific data (ophthalmic exams, etc.) is included
- Whether billing/claims data is included at the detail level
- Whether optical POS, ASC, or patient engagement data is included
- What data types fields use
- What coded value sets apply

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor organizes the export into two broad categories:
1. **Demographics/Billing** — tables not prefixed with EXAM, linked by PATUNIQUE
2. **Exam** — tables prefixed with EXAM, linked by EXAMUNIQUE

Beyond this two-category split, there is no detail about what specific data domains are included. The vendor explicitly mentions "patient demographics, medical records, billing records, images" as the content scope, but provides no table inventory to verify these claims.

The three example field descriptions (ERXCONSENT, GENDERIDENTITYNOTE, SEXUALORIENTATIONNOTE) suggest the PATIENT table includes e-prescribing consent and demographic identity fields, but this is a fragment — the full PATIENT table and its FLD file are not published.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | PATIENT table mentioned; 3 field snippets shown | Table exists but content unknown — only 3 of presumably many fields are documented |
| Encounters / visits | ⚠️ Partial | EXAM table mentioned as primary encounter table | Table exists but no field details. Sub-tables implied but not listed |
| Problems / conditions / diagnoses | ⚠️ Partial | EXAMDIAG table explicitly mentioned | Table exists; no field details |
| Medications / prescriptions | ❌ Not verified | ERXCONSENT field in PATIENT suggests e-prescribing data exists, but no medication table is listed | Product has Surescripts e-prescribing; cannot verify medication data is exported |
| Allergies | ❌ Not verified | No allergy-related table or field mentioned | Product stores allergies (certified (a)(8) equivalent); cannot verify inclusion |
| Immunizations | ❌ Not verified | No immunization table mentioned | Product stores immunizations (certified criteria); cannot verify inclusion |
| Vitals | ❌ Not verified | No vitals table mentioned | Product stores vitals (certified criteria); cannot verify inclusion |
| Lab results | ❌ Not verified | No lab table mentioned | Product has lab interfacing; cannot verify inclusion |
| Imaging / diagnostic reports | ⚠️ Partial | EXAMIMAG table and image files included. DOCUMENT table for demographics images | Image files exported in native format. Metadata tables exist but fields unknown |
| Procedures | ❌ Not verified | No procedure table mentioned | Product stores procedures; cannot verify inclusion |
| Clinical notes / documents | ⚠️ Partial | DOCUMENT table mentioned; image files may include scanned notes | Documents exported as image files; structure unknown |
| Care plans / goals | ❌ Not verified | No care plan table mentioned | Product supports care plans; cannot verify inclusion |
| Orders / referrals | ❌ Not verified | No orders/referral table mentioned | Product supports orders; cannot verify inclusion |
| Insurance / coverage | ❌ Not verified | Described as part of "Demographics/Billing" category but no insurance table listed | Product manages insurance verification; cannot verify inclusion |
| Claims / billing | ❌ Not verified | "Billing records" mentioned in general description but no billing table listed | Product has full billing/RCM module; cannot verify inclusion |
| Payments | ❌ Not verified | No payment table mentioned | Product processes payments; cannot verify inclusion |
| Consents / directives | ⚠️ Partial | ERXCONSENT field exists in PATIENT table | One consent field shown; broader consent data unknown |
| Patient communications | ❌ Not verified | No communications table mentioned | Product has patient engagement suite; cannot verify inclusion |
| Specialty-specific (ophthalmology) | ❌ Not verified | No specialty-specific tables mentioned despite being primary market | Product is specialty-focused with ophthalmic flowsheets, cataract/LASIK docs; major gap if not included |
| Optical POS | ❌ Not verified | No optical/retail table mentioned | Product has optical POS for frame/lens sales; cannot verify inclusion |
| ASC data | ❌ Not verified | No surgical center table mentioned | Product has ASC management module; cannot verify inclusion |

**Summary**: Of ~20 applicable data domains, **0 are confirmed covered** with field-level evidence, **5 are partially evidenced** (table name exists but no content details), and **15+ cannot be verified** from the documentation.

## 6. Documentation Quality

**Very poor.** The documentation fails to serve its purpose as an EHI export specification:

- **No data dictionary**: The single most important element — a listing of exported tables and fields — is entirely absent. The vendor explicitly defers this to .FLD files generated with each export, which are not published.
- **No table inventory**: Only 5 tables are mentioned as examples out of what is presumably dozens or hundreds. There is no way to know what the export contains.
- **No data types**: Field types are never mentioned.
- **No value sets or coded values**: No documentation of what values are valid for any field.
- **No sample data**: No example CSV content, no example FLD file content beyond a 3-line snippet.
- **No entity-relationship diagram**: Relationships described only in prose for 4 key identifiers.
- **No machine-readable artifacts**: No JSON schema, no SQL DDL, no CSV templates.

The 7-page PDF contains approximately 2 pages of substantive technical content (pages 4-5), with the remainder being cover page, blank page, table of contents, legal terms, and contact information. The total word count of the entire document is ~1,709 words.

**Could a developer build an import from this documentation?** No. A developer would need to obtain an actual export from a Compulink practice, examine the CSV files and FLD files contained within, and reverse-engineer the table structures, relationships, data types, and value sets. The published documentation provides only the file naming conventions and high-level linking strategy.

The vendor's rationale — that "comprehensive customization" makes a static data dictionary impossible — has some validity but is not a complete excuse. Even with customizable fields, the base table structure and standard field set could be documented. Many EHR vendors with customizable schemas still publish baseline data dictionaries.

## 7. Overall Assessment

### Classification

**Minimal/stub**: The documentation is too thin to assess actual export content. Only 5 table names and 3 field descriptions are provided across the entire document. The export *mechanism* (CSV dump of database tables with FLD field descriptions) is structurally sound and potentially comprehensive, but the published documentation provides no way to verify what is actually exported.

### Key Findings

1. **The export approach is architecturally sound but undocumented**: A per-table CSV dump with accompanying field description files (.FLD) is exactly the right approach for a comprehensive EHI export. The naming conventions and relationship structure described in the PDF are well-designed. However, none of the actual content is documented.

2. **Only 5 of presumably many tables are named**: The PDF mentions PATIENT, EXAM, EXAMDIAG, DOCUMENT, and EXAMIMAG as examples. For a product spanning EHR, practice management, billing, optical POS, ASC management, patient engagement, and 13+ medical specialties, the actual database likely contains hundreds of tables. Zero tables beyond these 5 examples are identified.

3. **Only 3 field descriptions are published**: The entire public documentation of what data is exported consists of three field snippets from the PATIENT table's FLD file (ERXCONSENT, GENDERIDENTITYNOTE, SEXUALORIENTATIONNOTE). All other field documentation exists only inside actual exports.

4. **The documentation is primarily legal and procedural**: Pages 6-7 (40%+ of substantive content) are usage terms, liability limitations, and indemnification clauses. The technical specification occupies ~2 pages.

5. **Specialty-specific data — the vendor's core differentiator — is completely undocumented**: Compulink's primary market is ophthalmology/optometry with specialty-specific templates, glaucoma flowsheets, and LASIK documentation. Whether any of this specialty clinical data is included in the export cannot be determined from the published documentation.

### Summary Stats

```
Classification:  Minimal/stub
Export format:   CSV + native images in password-protected ZIP
Model type:      Native database (CSV per table)
Entities:        5 mentioned (actual count unknown — no table listing provided)
Fields:          3 described (actual count unknown)
Descriptions:    N/A (3 field descriptions published; FLD files in exports not publicly available)
Sample data:     No
Bulk export:     Yes (P0_ prefix for all patients)
Domains covered: 0 of ~20 confirmed; 5 partially evidenced (table name only)
```

### Bottom Line

Compulink Advantage's EHI export is architecturally promising — a native database CSV dump with auto-generated field descriptions is the right approach — but the public documentation is essentially a 2-page format guide with no content specification. A patient or provider cannot determine what data will be in their export without actually running it. The single biggest gap is the complete absence of a data dictionary: no table listing, no field definitions, no sample data, making it impossible to assess whether this is a comprehensive export or a thin subset of the product's extensive data model.
