# EHI Export Analysis: Greenway Health, LLC

**Product**: Greenway Prime Suite
**Analysis date**: 2026-02-16
**CHPL IDs**: 15.04.04.2913.Prim.21.03.1.231003 (v21), 15.04.04.2913.Prim.22.04.1.250814 (v22)

## 1. Product Context

Greenway Prime Suite is an integrated ambulatory EHR and practice management system serving ~55,000+ providers across 40+ specialties. It combines clinical documentation, practice management, billing/revenue cycle, patient engagement, and e-prescribing in a single platform.

**Key capabilities relevant to export completeness:**
- **Clinical**: 4,000+ customizable clinical templates, problem lists, medications, allergies, immunizations, lab ordering/results, vital signs, clinical notes, care plans, clinical decision support
- **Billing/RCM**: Integrated medical billing, claims management (submission, scrubbing, denial management), payment processing, clearinghouse integration, superbills
- **Practice Management**: Scheduling, patient registration, insurance eligibility verification, multi-location management
- **E-Prescribing**: CPOE, drug interaction checking, formulary checks, medication history
- **Patient Engagement**: Patient portal with secure messaging, intake forms, appointment requests
- **Specialty**: OB/GYN, pediatrics, and 40+ specialty-specific templates/workflows
- **CHC/FQHC**: NCQA PCMH pre-validation, community health center–specific data

The product is being phased out in favor of Greenway Intergy, but remains actively certified and widely deployed.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/PrimeSuiteEHIExport.html` (8 KB) | Main EHI export landing page; describes two export modes and links to dictionary/schema | Medium — establishes export structure |
| `downloads/PrimeSuiteEHIExport_Data_Dictionary.html` (1.75 MB) | **Data dictionary: 1,026 tables, 11,868 columns** with names, types, nullable flags, and descriptions including FK references | **Most informative** — the core artifact |
| `downloads/PrimeSuiteEHIExport_Document_Reference.html` (2.47 MB) | XML reference for 19 proprietary clinical document types (progress notes, custom notes, lab flowsheets, allergy docs, medical drawings) | High — documents proprietary format |
| `downloads/SinglePatientExport_Structure_Schema.html` (21 KB) | Structure/schema for single-patient export: directory layout, XML file format, document folder conventions | Medium — explains export mechanics |
| `downloads/PatientPopulationExport_Structure_Schema.html` (167 KB) | Structure/schema for population export: batch process, XML schema, 1M-document batching | Medium — explains bulk mechanics |
| `downloads/default.htm` (3.5 KB) | Landing page for both Prime Suite and Intergy EHI exports | Low — navigation only |
| `downloads/enrichment/data-dictionary.json` (2.4 MB) | Pre-extracted JSON of all 1,026 tables (verified against raw HTML — counts match) | Reference validation |

## 3. Export Mechanics

- **Format**: XML files for tabular data (one XML file per database table), plus original-format documents (PDF, C-CDA XML, TIF, JPG, GIF, BMP, TXT). Each table's XML uses `<TableName><row><Column>value</Column></row></TableName>` schema.
- **Mechanism**:
  - **Single Patient**: UI-driven export within Prime Suite (minimum version 21.23.00.00). Output is a directory structure with `DataExport` (XML table files) and `DocumentExport` (clinical documents in subfolders: `AdamImage`, `ClinicalBin`, `ImgLibGroupItem`), plus logs.
  - **Patient Population**: Vendor-assisted via My Greenway portal request, fulfilled by Greenway Professional Services. XML files batched at 1M documents per file.
- **Encryption**: Some exported files require a conversion tool (available on My Greenway portal) to decrypt before reading.
- **Single-patient**: Yes, self-service via UI
- **Bulk**: Yes, but vendor-assisted (requires support request to Greenway Professional Services)
- **Access constraints**: Population export requires contacting Greenway; conversion tool needed for decryption

## 4. Export Content: What's In It

### Data Dictionary Overview

The export covers **1,026 database tables** with **11,868 columns** — this is a direct dump of the product's internal relational database schema.

- **All 1,026 tables** have descriptions (100%)
- **11,864 of 11,868 fields** (>99.9%) have descriptions beyond just a name
- **All fields** have data types documented (varchar, numeric, int, datetime, etc.)
- **All fields** have nullable flags documented
- **578 fields** include explicit foreign key references (e.g., "References: dbo.ClinicalDocuments")
- No value sets or coded value enumerations are provided
- No sample data is provided

### Document Export

In addition to the tabular XML data, the export includes clinical documents in their original formats:
- PDFs, C-CDA (XML), TIF, JPG, GIF, BMP, TXT files
- Each document is accompanied by two XML metadata files (Data file and Document file) linking it to the patient
- The XML Reference documents 19 proprietary document type formats including progress notes (type 1005), custom notes (1016), lab flowsheets, allergy test records, allergy education documents, and medical drawings (with SVG reconstruction instructions)

### Vendor's Own Content Organization

The vendor does not organize tables into explicit categories; the data dictionary is a flat alphabetical list of all 1,026 tables. The table names reflect the internal database schema. Below is an analyst-assigned categorization based on table names and descriptions:

| Category (analyst-assigned) | Tables | Fields | Notes |
|---|---|---|---|
| Billing & Financial | 192 | 4,340 | Claims (CFBClaimInfo: 435 fields), payment history, service details, superbills, EDI/835 transactions, statements, charge schedules |
| Patient Demographics | 97 | 1,129 | Patient records, contacts, addresses, phone numbers, next of kin, race/ethnicity, employers |
| Insurance & Coverage | 30 | 667 | Patient insurance (110 fields), insurance plans (106 fields), eligibility transactions, authorizations |
| Immunizations | 61 | 564 | Vaccines, injections, vials, serums, dose tracking, VFC data, vaccine history |
| Clinical Forms & Alerts | 56 | 536 | Clinical alerts, health risk assessments (HRA), clinical forms, recall alerts |
| Lab & Results | 73 | 520 | OBR/OBX segments, lab results, manual results, flowsheets, result concepts |
| Clinical Documents & Notes | 59 | 441 | Clinical documents, CDA imports, image library items, sticky notes, document metadata |
| CHC / FQHC Data | 34 | 384 | Community health center–specific: FPL schedules, benefit sets, agricultural work status, contract settings |
| Encounters & Scheduling | 44 | 385 | Encounters, appointments, visit data |
| Medications & Prescriptions | 21 | 367 | Patient medications (77 fields), drug interactions, PBM info, prescriptions |
| Orders | 52 | 346 | Order tracking, requisitions, order admin, order sets |
| Specialty: OB/GYN & Pediatrics | 20 | 174 | Menstrual history, pregnancy details, EDC (prenatal), WHO pediatric growth charts |
| Provider / Staff | 12 | 164 | Care provider details, locations, user accounts |
| Allergies | 19 | 117 | Allergy records, allergens, adverse reactions |
| Vitals | 10 | 115 | Vital signs, vital history |
| Procedures | 10 | 83 | Procedure master info, procedure codes |
| Problems & Diagnoses | 12 | 81 | Problem lists, diagnosis records |
| Vocabulary / Terminology | 14 | 75 | Concept vocabularies, terminology mappings |
| Care Plans & Goals | 11 | 65 | Care plans, goals, interventions |
| Imaging | 3 | 59 | Image work lists, imaging history |
| Social History | 6 | 54 | Social history, travel records |
| Patient Reminders | 6 | 52 | Patient reminders, reminder history |
| Family History | 4 | 42 | Family history records |
| Interoperability | 6 | 39 | IHE document exchange, interface events, data sources |
| Genetic Testing | 4 | 38 | Genetic scan orders |
| Referrals | 8 | 36 | Referral records |
| Patient Communications | 8 | 35 | Messages, inbox, communications |
| Devices | 2 | 34 | Implanted device tracking |
| Case Management | 3 | 32 | Case headers, case status, case types |
| Research | 4 | 17 | Research requests |
| Other / Uncategorized | 145 | 877 | Miscellaneous tables not fitting above categories |

**Representative largest entities:**

| Entity | Fields | Description |
|---|---|---|
| CFBClaimInfo | 435 | Claim form billing information |
| ClaimHeaderHistory | 272 | Claims header history data |
| ClaimHeaderHistoryOLD | 226 | Legacy claims header history |
| CHCClaim | 177 | Community health center claims |
| CFBUBInfo | 135 | UB (uniform billing) form info |
| fctPatientInsurance | 110 | Patient insurance details |
| fctAccount | 107 | Patient account information |
| InsurancePlan | 106 | Insurance plan configuration |
| ServiceDetailHistory | 96 | Service/charge detail history |
| CHCClaim_Lines | 95 | CHC claim line items |
| br_ServiceDetail | 92 | Service charge details |
| ASCX12_835D_Claim | 90 | EDI 835 (remittance) claim data |
| Claim | 85 | Claim request records |
| ClinicalPatMeds | 77 | Patient medication tracking |

The full inventory of all 1,026 entities with their 11,868 fields is available in `analysis/entity-inventory-full.json`.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The export is a native database dump of Prime Suite's internal relational schema. It is remarkably deep:

**Billing & Financial** is the single largest domain at 192 tables and 4,340 fields — 36.6% of all fields. This includes claims (with the largest single table CFBClaimInfo at 435 fields), payment history, service details, superbills, EDI 835/837 transactions, statements, charge schedules, denial data, and batch claims. This level of billing detail is far beyond what any USCDI/FHIR-based export would cover.

**Patient Demographics** is the second-largest domain (97 tables, 1,129 fields), covering far more than USCDI demographic fields — includes address history, phone numbers, next of kin relationships, race/ethnicity detail, employer information.

**Insurance & Coverage** (30 tables, 667 fields) includes detailed patient insurance records (110 fields per patient-insurance link), insurance plan configuration (106 fields), eligibility request/response transactions, authorization tracking.

**Clinical domains** are well-represented: Medications (21 tables, 367 fields), Immunizations (61 tables, 564 fields), Lab & Results (73 tables, 520 fields), Orders (52 tables, 346 fields), Problems/Diagnoses (12 tables, 81 fields), Allergies (19 tables, 117 fields), Vitals (10 tables, 115 fields), and Clinical Documents (59 tables, 441 fields).

**Specialty data** is present: OB/GYN and pediatric tables (20 tables, 174 fields) covering menstrual history, pregnancy details, prenatal flowsheets, and WHO pediatric growth standards. CHC/FQHC-specific data (34 tables, 384 fields) is also exported.

**Thinner areas**: Patient Communications (8 tables, 35 fields), Referrals (8 tables, 36 fields), Care Plans & Goals (11 tables, 65 fields), and Devices (2 tables, 34 fields) are present but relatively thin.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | 97 tables, 1,129 fields: patient records, contacts, addresses, next of kin, race/ethnicity, employers | Thorough — far exceeds USCDI |
| Encounters / visits | ✅ Covered | 44 tables, 385 fields: encounters, appointments, scheduling | Well-covered |
| Problems / conditions / diagnoses | ✅ Covered | 12 tables, 81 fields: problem lists, diagnoses | Adequate |
| Medications / prescriptions | ✅ Covered | 21 tables, 367 fields: patient meds (77-field table), drug interactions, PBM, prescriptions | Deep |
| Allergies | ✅ Covered | 19 tables, 117 fields: allergy records, allergens, reactions | Good |
| Immunizations | ✅ Covered | 61 tables, 564 fields: vaccines, injections, vials, dose tracking, VFC, history | Very deep |
| Vitals | ✅ Covered | 10 tables, 115 fields: vital signs, vital history | Good |
| Lab results | ✅ Covered | 73 tables, 520 fields: OBR/OBX results, manual results, flowsheets | Deep |
| Imaging / diagnostic reports | ⚠️ Partial | 3 tables, 59 fields: image work lists, imaging history | Product likely stores more imaging metadata; but imaging ordering/results may be covered via orders and OBR/OBX tables |
| Procedures | ✅ Covered | 10 tables, 83 fields: procedure master info, procedure codes | Adequate |
| Clinical notes / documents | ✅ Covered | 59 tables, 441 fields + document export (PDFs, C-CDAs, images) + XML reference for 19 document types | Very thorough — includes proprietary format documentation |
| Care plans / goals | ✅ Covered | 11 tables, 65 fields: care plans, goals, interventions | Present |
| Orders / referrals | ✅ Covered | 52 order tables (346 fields) + 8 referral tables (36 fields) | Good |
| Insurance / coverage | ✅ Covered | 30 tables, 667 fields: patient insurance (110 fields), plans (106 fields), eligibility | Deep |
| Claims / billing | ✅ Covered | 192 tables, 4,340 fields: claims, payment history, service details, EDI 835/837, superbills, charge schedules | **Exceptionally deep** — largest domain |
| Payments | ✅ Covered | Included in billing tables: payment history, allocation types, remittance data | Included within billing |
| Consents / directives | ⚠️ Partial | No dedicated consent tables identified in the data dictionary | Product likely captures consent; not clearly present |
| Patient communications / portal messages | ⚠️ Partial | 8 tables, 35 fields: messages, inbox, communications | Present but thin relative to product's patient portal capabilities |
| Specialty-specific (OB/GYN, Pediatrics, CHC/FQHC) | ✅ Covered | 20 OB/GYN tables (174 fields) + 34 CHC/FQHC tables (384 fields) + specialty-specific immunization/injection tables | Good specialty coverage |

## 6. Documentation Quality

**Strengths:**
- The data dictionary is comprehensive: all 1,026 tables and all 11,868 fields have descriptions
- Data types and nullable flags are documented for every field
- 578 fields have explicit foreign key references to related tables (e.g., "References: dbo.ClinicalDocuments")
- The XML reference provides detailed format documentation for proprietary clinical document types, including SVG reconstruction instructions for medical drawings
- The export structure documentation clearly explains directory layouts, file naming conventions, and XML schemas for both single-patient and population exports

**Weaknesses:**
- Table descriptions are often boilerplate (e.g., "This table stores CFBClaimInfo information") — the table name is more informative than the description for many entities
- No value sets or code enumerations are provided (e.g., what StatusID values mean)
- No entity-relationship diagrams or formal schema documentation
- No sample data files
- Foreign key references are mentioned in field descriptions (free text) rather than in structured metadata
- The population export requires vendor assistance and a proprietary conversion tool for decryption

**Developer usability**: A developer could understand the broad structure and build an import, but would need significant reverse-engineering for value sets, business rules, and relationships not captured in FK references. The database table names are reasonably self-documenting (e.g., `ClinicalPatMeds`, `CFBClaimInfo`, `fctPatientInsurance`).

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Comprehensive**

This is a genuine database-level export of the product's internal schema. With 1,026 tables and 11,868 fields spanning clinical, billing, insurance, specialty, and administrative domains, it far exceeds USCDI scope. The billing domain alone (192 tables, 4,340 fields) constitutes 36.6% of all fields — this is not data that would appear in any clinical exchange export. CHC/FQHC tables, OB/GYN data, genetic testing, and implanted device tracking represent specialty depth beyond standard clinical summaries. The only notable thin areas are patient communications (portal messages) and consent/directive tracking, which are minor gaps relative to the breadth covered.

**Axis 2 — Export approach: Purpose-built EHI export**

This is clearly a purpose-built (b)(10) export, not a repackaged clinical exchange. The telltale signs:
- **Native database schema**: The export uses the vendor's internal relational model (1,026 SQL Server tables exported as XML), not FHIR resources or C-CDA sections
- **Billing data dominance**: 36.6% of all fields are billing/financial — data that would never appear in a (g)(10) FHIR API or C-CDA transition of care document
- **EDI transaction tables**: ASCX12_835 (remittance), eligibility request/response tables are operational billing data, not clinical exchange data
- **Custom document format documentation**: The 19-section XML Reference for proprietary document types (with SVG reconstruction instructions) shows purpose-built format documentation
- **Dedicated EHI documentation site**: ehi.greenwayhealth.com has product-specific documentation with data dictionary, XML reference, and schema documentation — not a generic FHIR/C-CDA spec link

### Key Findings

1. **Exceptionally deep billing/financial coverage**: 192 tables and 4,340 fields for billing data — the single largest entity (CFBClaimInfo) has 435 fields alone. This includes claims, payments, EDI 835/837 transactions, superbills, and charge schedules. This is the strongest signal that the export is genuine (b)(10).

2. **Complete field-level documentation**: >99.9% of 11,868 fields have descriptions, all have data types and nullable flags, and 578 have explicit FK references. This level of documentation for 1,026 tables is unusual and demonstrates serious effort.

3. **Native database dump with proprietary document format support**: The export provides both structured data (XML table dumps) and clinical documents (PDF, C-CDA, images) with detailed format documentation for proprietary document types.

4. **Specialty and CHC/FQHC data included**: OB/GYN tables (menstrual history, pregnancy, prenatal flowsheets), pediatric growth charts, and 34 CHC/FQHC-specific tables go well beyond standard clinical exchange.

5. **Population export requires vendor assistance**: The bulk export is not self-service — it requires a request through My Greenway portal and is fulfilled by Greenway Professional Services. Files also require a proprietary conversion tool for decryption.

### Summary Stats

```
Coverage:        Comprehensive
Approach:        Purpose-built EHI export
Export format:   XML (native database tables) + original-format documents (PDF, C-CDA, TIF, JPG, etc.)
Entities:        1,026
Fields:          11,868
Descriptions:    >99.9% of fields have descriptions
Sample data:     No
Bulk export:     Yes (vendor-assisted)
Domains covered: 17 of 19 applicable domains (partial: consents, patient communications)
```

### Bottom Line

Greenway Prime Suite's EHI export is one of the stronger (b)(10) implementations: a purpose-built native database dump of 1,026 tables with 11,868 fully-documented fields, covering clinical, billing, insurance, specialty, and administrative data far beyond USCDI. The biggest limitation is operational — the population export requires vendor assistance and a proprietary decryption tool — but the data content itself is comprehensive.
