# EHI Export Analysis: Indian Health Service

**Product**: Resource and Patient Management System Electronic Health Record (BCERv9.0)
**Analysis date**: 2026-02-16
**CHPL IDs**: 11717 (15.02.05.1673.RPMS.02.05.1.251124)

## 1. Product Context

The Resource and Patient Management System (RPMS) is a comprehensive health information system built and maintained by the Indian Health Service (IHS), a federal agency within HHS. It serves approximately 2.6 million American Indian and Alaska Native patients across 574 federally recognized tribes, running at hundreds of IHS-operated, tribal, and urban Indian health facilities.

RPMS is built on the same MUMPS/FileMan/Kernel technology stack as the VA's VistA system. It has been in continuous development since 1984. The certified module (BCERv9.0, certified 2025-11-24) covers the full suite of RPMS functionality:

- **Clinical**: Patient Care Component (PCC) with its V-file architecture linking all clinical data to visits; clinical notes (TIU); pharmacy (outpatient, controlled substances, e-prescribing, Surescripts); laboratory; radiology; allergies; immunizations; problem lists; orders/consults; care plans
- **Specialty clinical**: Behavioral health (MHSS), dental, women's health, diabetes management, HIV management, community health, prenatal care, well-child, optometry, podiatry, elder care, emergency department
- **Administrative/financial**: Patient registration, ADT, scheduling, third-party billing (Medicare/Medicaid/private/railroad), accounts receivable, pharmacy point-of-sale claims, contract health services (Purchased/Referred Care)
- **Population health**: GPRA clinical reporting, iCare, eCQM, data warehouse exports
- **Interoperability**: C-CDA, HL7, FHIR (g)(10), immunization registry exchange, Direct messaging

This breadth means a complete EHI export should cover clinical encounters, pharmacy, lab, imaging metadata, behavioral health, dental, specialty assessments, billing/claims, insurance eligibility, and patient demographics across all these domains.

## 2. Artifacts Reviewed

| Artifact | Description | Size | Informativeness |
|---|---|---|---|
| `IHS_EHI_Schema_Definition.pdf` | BREH package user manual; describes export mechanics, EHI scope, and customization options | 241 KB, 7 pages (4 pages of content) | Moderate — essential for understanding mechanics but no technical detail on export format |
| `BREH_OIT_20250714.txt` | 2025 national EHI export schema in JSON; defines 301 patient files with 8,415 field definitions and 548 pointer files | 5.75 MB | **Primary artifact** — machine-readable, complete schema for all exported data |
| `BREH_OIT_20240703.txt` | 2024 national schema; 298 files, ~8,274 fields, 542 pointer files | 5.66 MB | Useful for version comparison |
| `BREH_OIT_20230607.txt` | 2023 national schema (initial version); 296 files, ~8,221 fields, 538 pointer files | 5.61 MB | Useful for version comparison |
| `enrichment/files-catalog.json` | Prior agent's parse of the 2025 schema into a queryable catalog | 3.48 MB | Cross-validation reference |
| `enrichment/schema-summary.json` | Summary of all 3 schema versions | 2.6 KB | Quick reference |
| `enrichment/coverage-stats.json` | Domain categorization of all 301 files | 10 KB | Cross-validation reference |
| `enrichment/schema-diff.json` | Version-to-version diffs (2023→2024, 2024→2025) | 3.3 KB | Shows schema evolution |
| `enrichment/field-types.json` | Field type distribution for 2025 schema | 2.6 KB | Cross-validation reference |
| `enrichment/pointer-files.json` | All 548 reference/lookup tables | 199 KB | Reference file catalog |

The schema JSON files (`BREH_OIT_*.txt`) are by far the most informative artifacts — they are the complete, machine-readable data dictionary for the export. The PDF provides context on how the export works but contains minimal technical detail.

## 3. Export Mechanics

- **Format**: JSON, structured according to the RPMS FileMan database model
- **Mechanism**: The BREH (RPMS Electronic Health Information Export) package allows authorized users to manually generate an EHI export through the EHR GUI
- **Patient scope**: Supports single-patient and patient-population exports
- **Schema**: Uses a predefined national schema published on the IHS website; sites can also create custom schemas based on the national schema
- **Versioning**: Three annual schema versions have been published (2023, 2024, 2025), each additive (no files or fields removed)
- **Exclusions**: The PDF explicitly states images are excluded ("Imaging links/data are presented but not the images themselves"). Psychotherapy notes and litigation compilations are excluded per 45 CFR 164.501
- **Access**: Schema files are publicly downloadable from the IHS FTP site without authentication. The export itself requires authorized access to an RPMS system
- **Fees**: None mentioned
- **Viewer guidance**: "EHI exports are best viewed using a JSON viewer or html compliant text editor/viewer"

The export is **not** FHIR, C-CDA, or any standard format — it is a native database model export in JSON using the RPMS FileMan data dictionary structure. Fields reference FileMan file numbers, globals, nodes, and pieces.

## 4. Export Content: What's In It

### Data dictionary overview

The 2025 national schema (`BREH_OIT_20250714.txt`) defines:

- **301 patient files/tables** (all EHI-enabled)
- **8,415 total field definitions** across those files
- **548 pointer/reference files** (lookup tables for coded fields)
- **1,411 fields with enumerated value sets** (SET OF CODES type)
- **1,378 fields with length/range constraints** (min/max length for FREE TEXT, bounds for NUMERIC)
- **2,291 pointer fields** linking to reference files (POINTER TO A FILE type)
- **7,689 fields with validation check expressions** (MUMPS code for input validation)
- **0 fields with narrative descriptions** — field names serve as the only human-readable identifier

Each field definition includes: field name, field number, field type, FileMan metadata (file/subfile number, global, node, piece), field sequence, and type-specific attributes (value sets, length constraints, numeric bounds, pointer targets, word processing sub-fields).

### Schema evolution

| Version | Date | Patient Files | Fields | Pointer Files | Changes |
|---|---|---|---|---|---|
| BREH_OIT_20230607 | 2023-06-07 | 296 | ~8,221 | 538 | Initial version |
| BREH_OIT_20240703 | 2024-07-03 | 298 | ~8,274 | 542 | +2 files (BJVN HL7 EXCEPTIONS, CHS CHEF REGISTRY); field changes in 13 files |
| BREH_OIT_20250714 | 2025-07-14 | 301 | 8,415 | 548 | +3 files (BLRAU ANTIMICROBIAL USE LOG, BPHR MED REFILL REQUEST, V DELIVERY); field changes in 12 files |

All changes are additive — no files or fields have been removed across versions.

### Field type distribution

| Field Type | Count | Percentage |
|---|---|---|
| POINTER TO A FILE | 2,291 | 27.2% |
| FREE TEXT | 1,445 | 17.2% |
| SET OF CODES | 1,411 | 16.8% |
| DATE/TIME | 1,251 | 14.9% |
| NUMERIC | 698 | 8.3% |
| COMPUTED | 573 | 6.8% |
| WORD PROCESSING | 554 | 6.6% |
| WORD-PROCESSING | 170 | 2.0% |
| VARIABLE-POINTER | 21 | 0.2% |
| MULTIPLE COMPUTED | 1 | <0.1% |

### Vendor's own content organization

The schema does not organize files into named categories — all 301 files are flat within the PATIENT structure. For analysis purposes, files are categorized by their FileMan file names, global references, and functional domains. The full inventory of all 301 entities is in `analysis/full-entity-inventory.json`.

#### Category summary

| Category | Entities | Fields | % of Total Fields |
|---|---|---|---|
| Clinical - PCC V-files | 43 | 1,416 | 16.8% |
| Clinical - Pharmacy | 15 | 507 | 6.0% |
| Clinical - Laboratory | 7 | 201 | 2.4% |
| Clinical - Behavioral Health | 28 | 560 | 6.7% |
| Clinical - Dental | 4 | 41 | 0.5% |
| Clinical - Immunizations | 7 | 98 | 1.2% |
| Clinical - Other | 103 | 2,462 | 29.3% |
| Administrative - Billing | 35 | 1,552 | 18.4% |
| Administrative - Registration | 41 | 1,219 | 14.5% |
| Administrative - Scheduling | 12 | 182 | 2.2% |
| Imaging | 6 | 177 | 2.1% |
| **Total** | **301** | **8,415** | **100%** |

#### Top 20 entities by field count

| Entity (FileMan Name) | File Number | Fields | Category |
|---|---|---|---|
| VA PATIENT | 2 | 436 | Registration |
| BW PROCEDURE | 9002086.1 | 277 | Women's Health |
| ABSP LOG OF TRANSACTIONS | 9002313.57 | 239 | Billing (Pharmacy POS) |
| 3P BILL | 9002274.4 | 201 | Billing |
| 3P CLAIM DATA | 9002274.3 | 198 | Billing |
| PATIENT | 9000001 | 194 | Registration |
| A/R BILL/IHS | 90050.01 | 181 | Billing (Accounts Receivable) |
| PRESCRIPTION | 52 | 155 | Pharmacy |
| MHSS RECORD | 9002011 | 143 | Behavioral Health |
| RCIS REFERRAL | 90001 | 138 | Referrals |
| BILL/CLAIMS | 399 | 131 | Billing |
| NON-VERIFIED ORDERS | 53.1 | 101 | Orders |
| ER VISIT | 9009080 | 100 | Emergency |
| DRUG ACCOUNTABILITY TRANSACTION | 58.81 | 96 | Pharmacy |
| LAB DATA | 63 | 93 | Laboratory |
| VISIT | 9000010 | 89 | PCC Core |
| CHR RECORD | 90002 | 81 | Community Health |
| PAF | 45.9 | 78 | Clinical |
| REPRODUCTIVE FACTORS | 9000017 | 76 | Women's Health |
| TIU DOCUMENT | 8925 | 75 | Clinical Notes |

#### Key clinical entity groups

**PCC V-files (43 files, 1,416 fields)**: The core clinical data repository. Every clinical observation links to a VISIT record. Includes:
- V MEASUREMENT (vitals), V MEDICATION, V LAB, V MICROBIOLOGY, V PATHOLOGY
- V POV (diagnoses/purpose of visit), V CPT (procedures), V PROVIDER
- V IMMUNIZATION, V EXAM, V SKIN TEST, V DENTAL, V RADIOLOGY
- V HOSPITALIZATION, V EMERGENCY VISIT RECORD, V DELIVERY
- Specialty: V ELDER CARE, V WELL CHILD, V NUTRITION SCREENING, V TELEHEALTH
- Chronic disease: V AMI, V ANTICOAGULATION, V ASTHMA, V STROKE

**Behavioral health (28 files, 560 fields)**: Complete MHSS system — intake, records, case dates, groups, treatment plans, treatment notes, problems, goals, methods, suicide forms, personal history, health factors, Navajo referral forms, CD staging tool, prevention activities, and treated medical problems.

**Billing (35 files, 1,552 fields)**: Third-party billing (3P BILL with 201 fields, 3P CLAIM DATA with 198 fields), accounts receivable (A/R BILL/IHS with 181 fields), pharmacy point-of-sale (ABSP LOG OF TRANSACTIONS with 239 fields), insurance eligibility across payer types (Medicaid, Medicare, private, railroad), claims tracking, billing exemptions, and CDMIS billing.

**Registration/Demographics (41 files, 1,219 fields)**: Two massive patient files — VA PATIENT (436 fields) and PATIENT (194 fields) — covering demographics, insurance, enrollment, eligibility, name changes, legal documents, implanted devices, allergies, movement records, and outpatient encounter data.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The RPMS EHI export schema covers an exceptional breadth of patient data. Key observations:

**Deepest areas:**
- **Billing/claims**: 35 entities with 1,552 fields — the most field-rich domain. Covers third-party billing (3P BILL at 201 fields), claim data, accounts receivable, pharmacy point-of-sale transactions, insurance eligibility across all payer types (Medicaid, Medicare, private, railroad), and claims tracking. This is genuinely deep billing coverage.
- **Patient registration**: 41 entities with 1,219 fields. The two PATIENT files alone have 630 combined fields, covering demographics, insurance, eligibility, enrollment, and extensive administrative data.
- **PCC clinical visit data**: 43 V-files with 1,416 fields covering the full range of visit-linked clinical observations (vitals, meds, labs, procedures, diagnoses, immunizations, dental, radiology, and specialty data).

**Notable specialty coverage:**
- **Behavioral health**: 28 entities (560 fields) — unusually deep for an EHI export, covering intake, treatment plans with goals/methods/problems, suicide assessment forms, and Navajo-specific referral forms.
- **Women's health**: BW PROCEDURE (277 fields) plus BW PATIENT, BW NOTIFICATION, REPRODUCTIVE FACTORS (76 fields), BIRTH MEASUREMENT, prenatal problems — comprehensive maternal/reproductive health data.
- **Emergency department**: ER VISIT (100 fields) and ER ADMISSION (34 fields).
- **Community health**: CHR RECORD (81 fields), CHR POV, CHR EDUCATION PROVIDED — community health representative activity data.
- **Dental**: 4 entities (41 fields) covering dental patient data, procedures, deferred services, and followup.

**Thinnest areas:**
- **Scheduling**: 12 entities but only 182 fields — mostly appointment references and wait lists, which is appropriate since scheduling is administrative/operational data.
- **Dental**: Only 41 fields across 4 entities — light relative to a full dental data system, though the V DENTAL visit file adds additional coverage.
- **Immunizations**: 98 fields across 7 entities — adequate given that immunization data is also in V IMMUNIZATION.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | PATIENT (194 fields), VA PATIENT (436 fields), PATIENT NAME CHANGES, PATIENT APPLICATIONS, PATIENT ENROLLMENT | Thorough — 630+ combined fields across two patient files |
| Encounters / visits | ✅ Covered | VISIT (89 fields), OUTPATIENT ENCOUNTER, INPATIENT DIAGNOSIS/PROCEDURE/PROVIDERS, PATIENT MOVEMENT, ENCOUNTER FORM TRACKING, ER VISIT (100 fields), ER ADMISSION (34 fields) | Comprehensive — PCC visit architecture captures all encounter types |
| Problems / conditions | ✅ Covered | PROBLEM (59 fields), V POV (68 fields — purpose of visit/diagnoses), OUTPATIENT DIAGNOSIS, INPATIENT DIAGNOSIS | Thorough |
| Medications / prescriptions | ✅ Covered | PRESCRIPTION (155 fields), PHARMACY PATIENT, PHARMACY ARCHIVE, V MEDICATION, BCMA MEDICATION LOG/VARIANCE LOG, NON FORMULARY REQUESTS, BPHR MED REFILL REQUEST, RX SUSPENSE, RX VERIFY | Deep — covers outpatient Rx, inpatient medication admin, archives, and patient portal refill requests |
| Allergies | ✅ Covered | PATIENT ALLERGIES, ADVERSE REACTION ASSESSMENT (5 fields), ADVERSE REACTION REPORTING (62 fields) | Adequate |
| Immunizations | ✅ Covered | BI PATIENT + 6 related files (98 fields total), V IMMUNIZATION, BI V IMMUNIZATIONS DELETED, IZ EXPORTS | Thorough — RPMS immunization tracking is famously detailed |
| Vitals | ✅ Covered | V MEASUREMENT (via PCC V-files) | Adequate |
| Lab results | ✅ Covered | LAB DATA (93 fields), LAB ORDER ENTRY, V LAB, V MICROBIOLOGY, V PATHOLOGY, BLS LOINC EXPORT, PT LAB RELATED DATA, BLRAU ANTIMICROBIAL USE LOG, BLOOD INVENTORY | Comprehensive |
| Imaging / diagnostic reports | ⚠️ Partial | IMAGE (metadata), IMAGE AUDIT, IMAGING ANNOTATION, PACS MESSAGE, TELEREADER; RAD/NUC MED ORDERS (44 fields), RAD/NUC MED REPORTS (48 fields), NUC MED EXAM DATA, RADIATION ABSORBED DOSE | Metadata and reports included; **actual image files excluded by design** (per PDF documentation). This is documented and acknowledged. |
| Procedures | ✅ Covered | V CPT, V PROCEDURE, INPATIENT PROCEDURE, DAY SURGERY, DENTAL PROCEDURE, BW PROCEDURE (277 fields) | Thorough |
| Clinical notes / documents | ✅ Covered | TIU DOCUMENT (75 fields), TIU EXTERNAL DATA LINK, TIU MULTIPLE SIGNATURE, TIU PROBLEM LINK, GMR TEXT, V NARRATIVE TEXT | TIU is RPMS's clinical note system (Text Integration Utility) — covers all note types |
| Care plans / goals | ✅ Covered | CARE PLAN (11 fields), TREATMENT PLAN (23 fields), PATIENT GOALS, MHSS PATIENT TREATMENT PLANS/GOALS/METHODS | Present in both general and behavioral health contexts |
| Orders / referrals | ✅ Covered | ORDER (64 fields), NON-VERIFIED ORDERS (101 fields), REQUEST/CONSULTATION (41 fields), RCIS REFERRAL (138 fields), RCIS SECONDARY REFERRAL, REFERRAL PATIENT, PENDING OUTPATIENT ORDERS | Comprehensive — includes consult tracking (RCIS) system |
| Insurance / coverage | ✅ Covered | MEDICAID ELIGIBLE, MEDICARE ELIGIBLE, PRIVATE INSURANCE ELIGIBLE, RAILROAD ELIGIBLE, ABSP COMBINED INSURANCE, ABSP ELIGIBILITY, AGEV INSURANCE ELIGIBILITY HOLDING, PERSONAL POLICY, POLICY HOLDER | Thorough — covers all payer types with separate eligibility files |
| Claims / billing | ✅ Covered | 3P BILL (201 fields), 3P CLAIM DATA (198 fields), A/R BILL/IHS (181 fields), ABSP LOG OF TRANSACTIONS (239 fields), BILL/CLAIMS (131 fields), plus 30 additional billing entities | Exceptionally deep — 35 entities, 1,552 fields total |
| Payments | ✅ Covered | A/R TRANSACTIONS/IHS, A/R PREPAYMENT, A/R FLAT RATE POSTING, BENEFICIARY TRAVEL CLAIM | Covered through A/R system |
| Consents / directives | ✅ Covered | ADVANCE DIRECTIVE (2 fields), NOTICE OF PRIVACY PRACTICES (7 fields), RESTRICTED HEALTH INFORMATION (20 fields), ACCESS RESTRICTIONS, PATIENT REFUSALS FOR SERVICE/NMI (20 fields) | Present though some entities have very few fields |
| Patient communications / portal | ✅ Covered | BPHR MED REFILL REQUEST (29 fields), PATIENT NOTIFICATION (Rx READY), ALERT TRACKING, ICARE REMINDER NOTIFICATIONS | Portal medication refill requests and patient notifications included |
| Specialty: Behavioral Health | ✅ Covered | 28 MHSS entities (560 fields), MST HISTORY, BH CD STAGING TOOL | Exceptionally thorough — treatment plans, goals, methods, suicide forms, personal history |
| Specialty: Dental | ✅ Covered | DENTAL PATIENT, DENTAL PROCEDURE, DENTAL DEFERRED SVCS REGISTER, DENTAL FOLLOWUP, V DENTAL | Adequate |
| Specialty: Women's Health | ✅ Covered | BW PROCEDURE (277 fields), BW PATIENT, BW NOTIFICATION, REPRODUCTIVE FACTORS (76 fields), BIRTH MEASUREMENT, BJPN PRENATAL PROBLEMS | Deep — maternal/reproductive health well-represented |
| Specialty: Diabetes Management | ✅ Covered | BCDM PATIENT, CIC VISIT | Present but light — BCDM and CIC entities |
| Specialty: HIV Management | ✅ Covered | HMS REGISTRY (4 fields) | Present but minimal (4 fields) |
| Specialty: Community Health | ✅ Covered | CHR RECORD (81 fields), CHR POV, CHR EDUCATION PROVIDED | Community health representative data included |
| Specialty: Emergency | ✅ Covered | ER VISIT (100 fields), ER ADMISSION (34 fields) | Thorough |
| Specialty: Podiatry | ✅ Covered | PODIATRY HISTORY (16 fields) | Present |
| Specialty: Elder Care | ✅ Covered | ELDER CARE (16 fields), V ELDER CARE | Present |

## 6. Documentation Quality

**Strengths:**
- The schema files are **machine-readable JSON** — a developer can programmatically enumerate every file, field, type, constraint, and value set
- **Field types** are thoroughly documented: 10 distinct types (POINTER TO A FILE, FREE TEXT, SET OF CODES, DATE/TIME, NUMERIC, COMPUTED, WORD PROCESSING, WORD-PROCESSING, VARIABLE-POINTER, MULTIPLE COMPUTED)
- **1,411 SET OF CODES fields** include their full enumerated value lists (e.g., STATUS: M=MET, N=NOT MET, C=CONTINUED)
- **2,291 pointer fields** include references to the 548 pointer/reference files, documenting the relational structure
- **1,378 fields** have length or range constraints
- **7,689 fields** have MUMPS validation check expressions
- **Three annual versions** (2023, 2024, 2025) demonstrate active maintenance
- The schema is **self-contained** — pointer files provide the lookup tables needed to interpret coded data
- The PDF correctly scopes EHI per 45 CFR 171.102 and explicitly excludes psychotherapy notes and litigation compilations

**Weaknesses:**
- **No field descriptions**: Zero of 8,415 fields have narrative descriptions. Field names (e.g., "BLOOD TYPE", "BIRTH CERTIFICATE NO.") are the only human-readable identifiers. While most are self-explanatory, some are cryptic (e.g., "PAF", "OPC", "VAMB ELIGIBLE")
- **No sample export data**: No example JSON output is provided. A developer cannot see what the actual export looks like — key names, nesting structure, array handling, null representation
- **No documentation of JSON output format**: The schema defines what data is included and its types, but not how it maps to the output JSON structure
- **No entity/table descriptions**: File names are the only identifiers; there's no documentation of what each file represents or how it relates to clinical workflows
- **No ER diagram or relationship documentation**: While pointer fields document individual foreign key relationships, there's no overview of the relational model
- **PDF is minimal**: 4 pages of content in a 7-page document. No walkthrough, no examples, no diagrams
- **No user guide for the export process**: The PDF states the BREH package "allows authorized users to manually generate an EHI export" but provides no step-by-step instructions

**Could a developer build an import?** Partially. The schema provides enough structure to parse the field definitions and understand data types, constraints, and relationships. However, the lack of sample output means a developer would need to reverse-engineer the actual JSON format. The absence of narrative descriptions means some fields would require RPMS/FileMan domain knowledge to interpret. The MUMPS validation check expressions (present on 91.4% of fields) would be largely opaque to non-MUMPS developers.

## 7. Overall Assessment

### Classification

**Comprehensive native export**

This is a genuine, purpose-built native data model export that covers virtually all patient-facing clinical and administrative data stored in RPMS. The BREH package exports 301 files with 8,415 fields directly from the FileMan database, not repackaged through FHIR or C-CDA. The coverage spans demographics, encounters, medications, labs, imaging metadata, clinical notes, billing/claims, insurance, behavioral health, dental, women's health, community health, emergency, and numerous specialty domains. The schema is machine-readable, versioned, and actively maintained.

### Key Findings

1. **Exceptionally broad coverage**: 301 patient files across 8,415 fields covering clinical, billing, specialty, and administrative domains. Very few EHR products export this breadth of data for (b)(10). The PCC V-file architecture (43 files) captures virtually all visit-linked clinical data, and billing coverage (35 entities, 1,552 fields) is genuinely deep — not a token inclusion.

2. **Purpose-built (b)(10) implementation**: The BREH package is a dedicated EHI export tool, not a repackaging of existing FHIR or C-CDA functionality. It exports the native FileMan database model in JSON with a published, versioned schema. This is exactly what the regulation intends.

3. **Machine-readable schema with rich metadata**: The JSON schema files serve as a complete data dictionary with field types, validation rules, enumerated value sets (1,411 fields), length/range constraints (1,378 fields), and pointer relationships (2,291 fields linking to 548 reference tables). This level of technical detail exceeds most commercial EHR vendors' EHI documentation.

4. **No narrative field descriptions**: Despite the technical richness, zero of 8,415 fields have human-readable descriptions explaining what the field contains. Field names are the only documentation. This makes the export schema less accessible to non-RPMS developers.

5. **No sample data or output format documentation**: The absence of example export output means developers must guess at the JSON structure. Combined with the lack of field descriptions, this creates a significant barrier to building an import tool despite the otherwise thorough schema.

### Summary Stats

    Classification:  Comprehensive native export
    Export format:   JSON (native FileMan database model)
    Model type:      Native database
    Entities:        301
    Fields:          8,415
    Descriptions:    0% (no narrative field descriptions; field names only)
    Sample data:     No
    Bulk export:     Yes (single-patient and patient-population)
    Domains covered: 19 of 19 applicable domains

### Bottom Line

IHS's RPMS EHI export is one of the most complete (b)(10) implementations encountered — 301 native database entities covering 8,415 fields across clinical, billing, specialty, and administrative domains, with a machine-readable JSON schema that includes field types, value sets, constraints, and relational pointers. The single biggest gap is usability: zero field descriptions and no sample output mean a developer would need RPMS/FileMan expertise to interpret the export, despite the comprehensive coverage. A patient or provider would receive a genuinely complete copy of their data, but making sense of it would require significant effort.
