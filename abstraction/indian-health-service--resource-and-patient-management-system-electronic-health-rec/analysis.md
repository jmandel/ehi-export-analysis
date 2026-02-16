# EHI Export Analysis: Indian Health Service

**Product**: Resource and Patient Management System Electronic Health Record (BCERv9.0)
**Analysis date**: 2026-02-15
**CHPL ID**: 15.02.05.1673.RPMS.02.05.1.251124

## 1. Product Context

The Indian Health Service (IHS) is a federal agency within HHS providing healthcare to ~2.6 million members of 574 federally recognized American Indian and Alaska Native tribes. RPMS is IHS's internally developed, comprehensive health information system built on MUMPS/FileMan (the same foundation as VA VistA). It has been in continuous operation since ~1984 and is deployed across hundreds of IHS, tribal, and urban Indian health facilities.

RPMS is not a single application but a suite of ~50–100 interconnected packages covering:

- **Clinical**: Patient Care Component (PCC) with its V-file visit-linked architecture, clinical notes (TIU), pharmacy (outpatient, controlled substances, e-prescribing), laboratory, radiology, allergies, immunizations, problem lists, orders, consults/referrals, care plans
- **Specialty clinical**: Behavioral health (MHSS), dental (ADE), women's health (BW), diabetes management (BCDM), HIV management, prenatal care, optometry, emergency department, podiatry, elder care, community health
- **Administrative/Financial**: Patient registration, ADT, scheduling, third-party billing (Medicare/Medicaid/private — CMS-1500, UB-04, X12 837), accounts receivable, pharmacy point-of-sale claims, contract health services (purchased/referred care)
- **Interoperability**: C-CDA generation, FHIR API (g)(10), HL7 interfaces, immunization registry exchange, Direct messaging

This is an exceptionally broad system. An adequate (b)(10) export must cover clinical data across all these specialties, plus billing, insurance, and administrative data tied to patient records.

## 2. Artifacts Reviewed

| Artifact | Description | Informational Value |
|---|---|---|
| `IHS_EHI_Schema_Definition.pdf` | 7-page PDF (241 KB). User manual for the BREH export package. Describes scope, format, EHI definition, and customization. | **Moderate** — establishes export mechanics and scope but no technical detail on output format |
| `BREH_OIT_20250714.txt` | 5.75 MB JSON file. Latest (July 2025) national EHI export schema defining 301 patient files with 8,415 top-level field definitions and 548 pointer/reference files. | **Primary source** — the actual machine-readable data dictionary |
| `BREH_OIT_20240703.txt` | 5.66 MB JSON. 2024 schema (298 files, ~8,274 fields). | **Supplementary** — used for version diff |
| `BREH_OIT_20230607.txt` | 5.61 MB JSON. 2023 schema (296 files, ~8,221 fields). | **Supplementary** — used for version diff |
| `enrichment/files-catalog.json` | 3.48 MB JSON. Pre-parsed catalog of all 301 files and 8,415 fields from the 2025 schema. | **Corroborative** — verified against my own independent parse |
| `enrichment/schema-summary.json` | Summary metadata for all three schema versions. | **Corroborative** |
| `enrichment/coverage-stats.json` | Domain categorization of all 301 files across 11 categories. | **Corroborative** — cross-checked against my categorization |
| `enrichment/schema-diff.json` | Version-to-version diffs (added files, field count changes). | **Useful** — confirms schema evolution |
| `enrichment/pointer-files.json` | All 548 reference/lookup tables with field references. | **Useful** — documents relational structure |
| `enrichment/field-types.json` | Field type distribution with samples. | **Corroborative** |
| `enrichment/extract-schema.ts` | Bun TypeScript script that produced the enrichment files. | **Reference** |

## 3. Export Mechanics

- **Format**: JSON, reflecting the native RPMS FileMan database structure
- **Mechanism**: The BREH package provides a UI within the RPMS EHR that "allows authorized users to manually generate an EHI export" (PDF, p. 1). No API endpoint is described.
- **Scope**: Single patient or patient population export capability
- **Schema**: Uses a predefined "national schema" published on the IHS website. Sites can also create custom schemas based on the national schema.
- **Exclusions**: Images are explicitly excluded ("Imaging links/data are presented but not the images themselves" — PDF, p. 1). Psychotherapy notes and litigation compilations are excluded per 45 CFR 164.501.
- **Viewing**: "IHS EHI exports are best viewed using a JSON viewer or html compliant text editor/viewer" (PDF, p. 1)
- **Factors affecting content**: The PDF notes that export content varies based on EHR version, installed software packages, schema version, and site configuration decisions.
- **Access constraints/fees**: No fees mentioned. Export requires "authorized users" — standard EHR access control.
- **Bulk export**: Yes — the PDF states both "a single patient or a patient population."

## 4. Export Content: What's In It

### Overview

The 2025 national schema (`BREH_OIT_20250714.txt`) defines **301 patient files/tables** with **8,415 top-level field definitions** (13,090 including subfields within nested multi-valued fields). These files are supported by **548 pointer/reference files** (lookup tables for coded references). All 301 files have `EHI_ENABLED = "ENABLED"`.

**Field-level detail**: Every field definition includes:
- Field type (one of 10 types — see distribution below)
- FileMan data dictionary info (file-subfile number, global reference, node, piece)
- Validation constraints (check routines, min/max lengths)
- For SET OF CODES fields: complete value lists with internal codes and display values
- For POINTER TO A FILE fields: target file reference

**Field type distribution** (8,415 top-level / 13,090 total including subfields):

| Field Type | Top-Level | Including Subfields |
|---|---|---|
| POINTER TO A FILE | 2,291 | 3,433 |
| FREE TEXT | 1,445 | 2,625 |
| SET OF CODES | 1,411 | 1,997 |
| DATE/TIME | 1,251 | 1,971 |
| NUMERIC | 698 | 1,214 |
| COMPUTED | 573 | 665 |
| WORD PROCESSING / WORD-PROCESSING | 724 | 294 (consolidated) |
| VARIABLE-POINTER | 21 | 33 |
| MULTIPLE COMPUTED | 1 | 1 |

**Value sets**: 1,411 SET OF CODES fields include their complete coded value lists, totaling 4,383 distinct code values across all files. 210 of 301 files contain at least one coded field with a value set.

**Relationships**: 2,291 POINTER TO A FILE fields establish relational links to the 548 reference/lookup tables. This creates a richly interconnected data model where, for example, a V POV (diagnosis) record links to the VISIT file, ICD DIAGNOSIS file, PROVIDER file, etc.

**No human-readable field descriptions**: Field names serve as the description (e.g., "BLOOD TYPE," "BIRTH CERTIFICATE NO.," "DATE OF LAST VISIT"). There are no separate narrative descriptions explaining what each field contains. This is inherent to the FileMan data model — field names are the documentation.

### Vendor's own content organization

The schema organizes data into patient-level files reflecting RPMS's native FileMan database structure. I categorized the 301 files into domains based on their names and known RPMS module affiliations. The full inventory is in `analysis/full-entity-inventory.json`.

**Category summary:**

| Category | Files | Top-Level Fields | Total Fields (incl. subfields) |
|---|---|---|---|
| Clinical - PCC V-files | 43 | 1,416 | 1,603 |
| Clinical - Pharmacy | 13 | 470 | 1,003 |
| Clinical - Laboratory | 7 | 201 | 1,262 |
| Clinical - Behavioral Health | 27 | 554 | 622 |
| Clinical - Dental | 4 | 41 | 56 |
| Clinical - Immunizations | 7 | 98 | 104 |
| Imaging (metadata) | 6 | 177 | 245 |
| Administrative - Billing | 35 | 1,552 | 2,432 |
| Administrative - Scheduling | 10 | 145 | 211 |
| Clinical - Other / Administrative | 149 | 3,761 | 5,552 |
| **Total** | **301** | **8,415** | **13,090** |

**20 largest files by total field count:**

| File | Number | Top-Level Fields | Total Fields | Category |
|---|---|---|---|---|
| LAB DATA | 63 | 93 | 918 | Laboratory |
| VA PATIENT | 2 | 436 | 643 | Registration |
| 3P BILL | 9002274.4 | 201 | 551 | Billing |
| 3P CLAIM DATA | 9002274.3 | 198 | 509 | Billing |
| PHARMACY PATIENT | 55 | 52 | 358 | Pharmacy |
| PRESCRIPTION | 52 | 155 | 338 | Pharmacy |
| BW PROCEDURE | 9002086.1 | 277 | 282 | Women's Health |
| PATIENT | 9000001 | 194 | 280 | Registration |
| ABSP LOG OF TRANSACTIONS | 9002313.57 | 239 | 239 | Billing (Pharmacy POS) |
| A/R BILL/IHS | 90050.01 | 181 | 228 | Billing (A/R) |
| CHS FACILITY | 9002080 | 61 | 212 | Contract Health |
| BILL/CLAIMS | 399 | 131 | 168 | Billing |
| RCIS REFERRAL | 90001 | 138 | 167 | Referrals |
| BLOOD INVENTORY | 65 | 71 | 158 | Laboratory |
| MHSS RECORD | 9002011 | 143 | 150 | Behavioral Health |
| RAD/NUC MED PATIENT | 70 | 13 | 132 | Radiology |
| NON-VERIFIED ORDERS | 53.1 | 101 | 121 | Orders |
| ORDER | 100 | 64 | 121 | Orders |
| ER VISIT | 9009080 | 100 | 110 | Emergency |
| CHS DENIAL DATA | 9002071 | 2 | 106 | Contract Health |

### Schema evolution

The schema has grown steadily across three annual versions, with only additions and no removals:

| Version | Date | Patient Files | New Files Added |
|---|---|---|---|
| BREH_OIT_20230607 | June 2023 | 296 | (initial) |
| BREH_OIT_20240703 | July 2024 | 298 | BJVN HL7 EXCEPTIONS, CHS CHEF REGISTRY |
| BREH_OIT_20250714 | July 2025 | 301 | BLRAU ANTIMICROBIAL USE LOG, BPHR MED REFILL REQUEST, V DELIVERY |

Notable field count changes in 2024→2025: PATIENT grew from 171→194 fields, MHSS RECORD from 125→143 fields, ER VISIT from 97→100 fields.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The BREH schema exports RPMS's native FileMan database model — not a FHIR projection, not a C-CDA summary, but the actual internal tables. This is reflected in the depth and breadth:

**PCC V-files (43 files, 1,603 total fields)**: The complete Patient Care Component visit-linked clinical data. Every encounter type has its own V-file: V MEASUREMENT (vitals), V MEDICATION, V POV (diagnoses), V CPT (procedures), V LAB, V IMMUNIZATION, V RADIOLOGY, V DENTAL, V HOSPITALIZATION, V EMERGENCY VISIT RECORD, plus specialty-specific files like V AMI, V ANTICOAGULATION, V ASTHMA, V ELDER CARE, V STROKE, V TELEHEALTH, V WELL CHILD, V NUTRITION SCREENING, V PATIENT ED, V DELIVERY. The central VISIT file ties everything together.

**Billing (35 files, 2,432 total fields)**: Genuinely deep. The 3P BILL file alone has 551 fields including subfiles. Coverage includes third-party billing (3P BILL, 3P CLAIM DATA, 3P CANCELLED CLAIM DATA), accounts receivable (A/R ACCOUNTS/IHS, A/R BILL/IHS, A/R TRANSACTIONS/IHS, A/R EDI CLAIM STATUS), insurance eligibility by type (MEDICAID ELIGIBLE/CLAIMS, MEDICARE ELIGIBLE/CLAIMS, PRIVATE INSURANCE ELIGIBLE/CLAIMS, RAILROAD ELIGIBLE/CLAIMS), pharmacy point-of-sale (ABSP LOG OF TRANSACTIONS, ABSP COMBINED INSURANCE, ABSP ELIGIBILITY), and integrated billing (BILL/CLAIMS, CLAIMS TRACKING, BILLING PATIENT).

**Pharmacy (13 files, 1,003 total fields)**: PRESCRIPTION (338 fields), PHARMACY PATIENT (358 fields), PHARMACY ARCHIVE, controlled substance audit logs (APSP CS AUDIT LOG, APSP DEA ARCHIVE INFO), Surescripts e-prescribing requests, drug accountability transactions, medication verification (RX VERIFY), and prescription notifications.

**Laboratory (7 files, 1,262 total fields)**: LAB DATA is the single largest file (918 fields including extensive subfiles for all pathology areas). Also includes LAB ORDER ENTRY, BLOOD INVENTORY, BLRA LAB AUDIT, antimicrobial use logging, LOINC exports, and patient lab data.

**Behavioral Health (27 files, 622 total fields)**: Complete Mental Health Summary System (MHSS): intake, records (143 fields), case dates, group sessions, treatment plans and goals, treatment notes, problem lists, patient personal history, prevention activities, Navajo referral forms, suicide assessment forms, and the CD staging tool. This is one of the deepest specialty modules.

**Registration/Demographics**: The VA PATIENT file (643 total fields) and IHS PATIENT file (280 total fields) together provide exhaustive demographic, enrollment, eligibility, and administrative data. Also includes PATIENT NAME CHANGES, PATIENT'S LEGAL DOCS, PATIENT ENROLLMENT, PATIENT APPLICATIONS.

**Specialty Clinical**: Women's health (BW PROCEDURE at 282 fields, BW PATIENT, BW NOTIFICATION), emergency department (ER VISIT at 110 fields, ER ADMISSION at 34 fields), dental (4 files), immunizations (7 files), elder care, prenatal (BJPN PRENATAL PROBLEMS, REPRODUCTIVE FACTORS at 76 fields, BIRTH MEASUREMENT), diabetes management (BCDM PATIENT), HIV management (HMS REGISTRY), community health (CHR RECORD, CHR POV, CHR EDUCATION PROVIDED), podiatry (PODIATRY HISTORY), chronic disease (CIC VISIT), workman's compensation, military sexual trauma (MST HISTORY).

**Other patient-level data**: Advance directives, allergies (PATIENT ALLERGIES, ADVERSE REACTION ASSESSMENT/REPORTING), care plans, treatment plans, clinical notes (TIU DOCUMENT plus 3 related files), problem lists (PROBLEM), orders (ORDER, NON-VERIFIED ORDERS, PENDING OUTPATIENT ORDERS), consults/referrals (REQUEST/CONSULTATION, RCIS system with 6 files, REFERRAL PATIENT), family history, personal history, implanted devices, guarantor information, prior authorizations, restricted health information, notice of privacy practices, and release-of-information records (ROI LISTING RECORD).

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | VA PATIENT (643 fields), PATIENT (280 fields), PATIENT NAME CHANGES, PATIENT ENROLLMENT | Exceptionally thorough — two major files totaling 923 fields |
| Encounters / visits | ✅ Covered | VISIT (central file), OUTPATIENT ENCOUNTER, INPATIENT files, ER VISIT/ADMISSION, DELETED OUTPATIENT ENCOUNTER | Full encounter lifecycle including inpatient, outpatient, ER |
| Problems / conditions / diagnoses | ✅ Covered | PROBLEM (59 fields), V POV (68 fields), OUTPATIENT DIAGNOSIS, INPATIENT DIAGNOSIS, BGO PROBLEM PRIORITY | Problem list plus visit-linked diagnoses |
| Medications / prescriptions | ✅ Covered | PRESCRIPTION (338 fields), PHARMACY PATIENT (358 fields), PHARMACY ARCHIVE, V MEDICATION, BCMA MEDICATION LOG/VARIANCE LOG, BPHR MED REFILL REQUEST | Deep — covers outpatient Rx, medication administration, archive, refill requests |
| Allergies | ✅ Covered | PATIENT ALLERGIES, ADVERSE REACTION ASSESSMENT, ADVERSE REACTION REPORTING | Comprehensive allergy/adverse reaction tracking |
| Immunizations | ✅ Covered | BI PATIENT system (7 files, 104 fields), V IMMUNIZATION, BI V IMMUNIZATIONS DELETED, IZ EXPORTS | Full immunization tracking including deleted records and registry exports |
| Vitals | ✅ Covered | V MEASUREMENT | Standard vital signs via PCC V-file |
| Lab results | ✅ Covered | LAB DATA (918 fields), LAB ORDER ENTRY, V LAB (58 fields), V MICROBIOLOGY (57 fields), V PATHOLOGY, BLS LOINC EXPORT, BLOOD INVENTORY, BLRAU ANTIMICROBIAL USE LOG | Very deep — LAB DATA is the largest file in the schema |
| Imaging / diagnostic reports | ✅ Covered | IMAGE, IMAGE AUDIT, IMAGING ANNOTATION, RAD/NUC MED ORDERS/REPORTS/PATIENT, NUC MED EXAM DATA, PACS MESSAGE, V RADIOLOGY, RADIATION ABSORBED DOSE | Metadata/reports covered; actual image files excluded by design |
| Procedures | ✅ Covered | V CPT, V PROCEDURE, INPATIENT PROCEDURE, DAY SURGERY, BW PROCEDURE (282 fields), DENTAL PROCEDURE, RCIS PROCEDURE | Covers outpatient, inpatient, surgical, and specialty procedures |
| Clinical notes / documents | ✅ Covered | TIU DOCUMENT, TIU EXTERNAL DATA LINK, TIU MULTIPLE SIGNATURE, TIU PROBLEM LINK, V NARRATIVE TEXT, GMR TEXT | TIU is the text integration utility for all note types |
| Care plans / goals | ✅ Covered | CARE PLAN, TREATMENT PLAN, PATIENT GOALS, MHSS treatment plan system (goals, methods, problems) | Both general and behavioral-health-specific care plans |
| Orders / referrals | ✅ Covered | ORDER (121 fields), NON-VERIFIED ORDERS (121 fields), PENDING OUTPATIENT ORDERS, REQUEST/CONSULTATION, RCIS REFERRAL (167 fields), REFERRAL PATIENT, V REFERRAL | Deep order and referral system |
| Insurance / coverage | ✅ Covered | MEDICAID/MEDICARE/PRIVATE INSURANCE/RAILROAD ELIGIBLE files, ABSP COMBINED INSURANCE, ABSP ELIGIBILITY, AGEV INSURANCE ELIGIBILITY HOLDING, PERSONAL POLICY, POLICY HOLDER, THIRD PARTY LIABILITY | Coverage tracked by payer type — granular |
| Claims / billing | ✅ Covered | 3P BILL (551 fields), 3P CLAIM DATA (509 fields), A/R system (7 files), BILL/CLAIMS, CLAIMS TRACKING, ABSP LOG OF TRANSACTIONS (239 fields) | 35 billing files with 2,432 total fields — one of the deepest billing exports analyzed |
| Payments | ✅ Covered | A/R TRANSACTIONS/IHS, A/R PREPAYMENT, A/R FLAT RATE POSTING, SPENDDOWN INFORMATION | Part of the A/R system |
| Consents / directives | ✅ Covered | ADVANCE DIRECTIVE, NOTICE OF PRIVACY PRACTICES, RESTRICTED HEALTH INFORMATION, PATIENT REFUSALS FOR SERVICE/NMI | Both directives and privacy/consent tracking |
| Patient communications / portal messages | ⚠️ Partial | BPHR MED REFILL REQUEST (added 2025), ALERT TRACKING, AG MESSAGE TRANSACTIONS | Med refill requests from personal health record present; general patient portal messaging not explicitly represented |
| Specialty: Behavioral health | ✅ Covered | 27 MHSS files (622 fields) including intake, treatment plans, goals, methods, suicide forms, Navajo referral forms, personal history, prevention activities | Exceptionally deep specialty coverage |
| Specialty: Dental | ✅ Covered | DENTAL PATIENT, DENTAL PROCEDURE, DENTAL DEFERRED SVCS REGISTER, DENTAL FOLLOWUP, V DENTAL | Dedicated dental module |
| Specialty: Women's health | ✅ Covered | BW PROCEDURE (282 fields), BW PATIENT, BW NOTIFICATION, REPRODUCTIVE FACTORS (76 fields), BIRTH MEASUREMENT, BJPN PRENATAL PROBLEMS, V DELIVERY | Very deep women's health and prenatal coverage |
| Specialty: Emergency medicine | ✅ Covered | ER VISIT (110 fields), ER ADMISSION (34 fields), V EMERGENCY VISIT RECORD | Full ER documentation |
| Specialty: Contract/purchased care | ✅ Covered | CHS FACILITY (212 fields), CHS DEFERRED SERVICE DATA, CHS DENIAL DATA (106 fields), CHS CHEF REGISTRY, QA CHS ADMISSION | IHS-specific: outside provider referral management |

## 6. Documentation Quality

**Strengths:**
- The schema files are **fully machine-readable JSON** — parseable and queryable. My script extracted all 301 files, 8,415 top-level fields, and 13,090 total fields (including subfields) in a single pass.
- **Field-level metadata is thorough**: every field has a type, FileMan data dictionary info (file-subfile number, global, node, piece), and validation constraints.
- **Value sets are complete**: 1,411 SET OF CODES fields include their full coded value lists (4,383 total code values), with both internal codes and display values.
- **Relationships are machine-readable**: 2,291 POINTER TO A FILE fields identify their target reference files, and all 548 reference files are included in the schema.
- **Three versioned schemas** (2023, 2024, 2025) show active maintenance and additive evolution.
- The schema is **self-contained**: no external documentation is required to understand the relational structure.

**Weaknesses:**
- **No sample export data**: There are no sample JSON output files showing what an actual export looks like. A developer would need to infer the output structure from the schema definition.
- **No narrative field descriptions**: Field names are the only documentation (e.g., "BLOOD TYPE," "DATE OF LAST VISIT"). While most are self-explanatory, some are cryptic (e.g., "PAF," "OPC," "EWL CLEAN-UP").
- **No output format specification**: The PDF says exports are JSON, but doesn't show the JSON structure — how are multi-valued fields represented? How are pointer references serialized?
- **The PDF is very brief**: Only 4 pages of content in a 7-page document. It describes what the BREH package does but provides no examples, walkthroughs, or implementation guidance.
- **No ERD or relationship diagram**: The pointer references establish relationships but there's no visual or narrative description of the data model.

**Could a developer build an import?** Partially. The schema provides enough structural information to understand field types, coded values, and relationships. However, without sample output data, the actual JSON serialization format would require either access to an RPMS instance or reverse engineering. The FileMan conventions (global references, node/piece positions) are well-documented in VA/FileMan literature but unfamiliar to most developers.

## 7. Overall Assessment

### Classification

**Comprehensive native export**

This is a genuine native database model export — 301 patient files directly reflecting RPMS's FileMan database structure, with 8,415 top-level field definitions, 548 reference/lookup tables, and deep coverage across clinical, billing, specialty, and administrative domains.

### Key Findings

1. **One of the most comprehensive EHI exports analyzed.** 301 patient files with 8,415 top-level fields (13,090 including subfields) covering virtually every data domain the product stores. The billing system alone has 35 files and 2,432 total fields — more billing depth than most vendors' entire exports.

2. **Genuine native data model, not a standards projection.** The export uses RPMS's own FileMan database structure — not FHIR, not C-CDA. Field definitions reference FileMan file numbers, globals, nodes, and pieces. This means nothing is lost in translation, but portability requires FileMan/RPMS knowledge.

3. **Machine-readable schema with complete value sets and relationships.** The schema files are well-structured JSON with typed fields, coded value lists (1,411 fields with 4,383 code values), and 2,291 pointer references to 548 lookup tables. This level of structural metadata exceeds what most commercial vendors provide.

4. **Actively maintained with annual updates.** Three schema versions (2023→2025) show steady growth from 296→301 files, with only additions and no removals. Changes include new files (V DELIVERY, BPHR MED REFILL REQUEST, BLRAU ANTIMICROBIAL USE LOG) and expanded fields in existing files.

5. **Documentation gaps**: No sample export data, no output format specification, and no narrative field descriptions. The schema defines *what* data is included but not *how* it's serialized in the actual JSON output. The PDF user manual is only 4 pages of content.

### Summary Stats

```
Classification:  Comprehensive native export
Export format:   JSON (native FileMan database structure)
Model type:      Native database
Entities:        301 patient files + 548 pointer/reference files
Fields:          8,415 top-level (13,090 including subfields)
Descriptions:    Field names only (no separate narrative descriptions)
Sample data:     No
Bulk export:     Yes (single patient or patient population)
Domains covered: 21 of 22 assessed domains (all fully or partially covered)
```

### Bottom Line

IHS's RPMS EHI export is among the most thorough (b)(10) implementations in the industry. With 301 native database files spanning clinical care, billing, pharmacy, laboratory, behavioral health, dental, women's health, emergency medicine, and administrative functions — plus 548 supporting reference tables — this export genuinely represents "all electronic health information" as the Cures Act intends. The single notable gap is the absence of sample export data and output format documentation, which would help developers actually consume the export. The data model itself is exemplary.
