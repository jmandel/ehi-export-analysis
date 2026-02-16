# EHI Export Analysis: TRIARQ Practice Services

**Product**: QSuite (version "Manistee")
**Analysis date**: 2026-02-16
**CHPL IDs**: 15.02.05.2614.TRIQ.01.01.1.211105

## 1. Product Context

QSuite is a cloud-based integrated EHR and practice management platform developed by TRIARQ Practice Services (now a BCBSM subsidiary). It targets independent ambulatory specialty practices — particularly orthopedics, urology, oncology, cardiology, neurology, and gastroenterology. The product is hosted on Google Cloud Platform.

QSuite is not just an EHR — it is a full-stack practice platform spanning:

- **Clinical documentation**: Charting, customizable templates, AI-generated notes (QScribe), clinical decision support
- **E-prescribing**: Surescripts-certified, EPCS integration
- **Practice management**: Scheduling, patient registration, insurance/eligibility verification, prior authorization
- **Billing / RCM**: Claims management, A/R, denial management, patient payments, collections (QComplete)
- **Patient engagement**: Patient portal (MyQOne), messaging, intake (QIntake)
- **Lab integration**: Orders and results from external labs
- **Referrals & care coordination**: QPathways referral network
- **Reporting**: QInsights dashboards, CQM/MIPS reporting
- **Document management**: Scanned documents, images

This means a complete EHI export should cover clinical data, billing/financial data, insurance, prior authorizations, prescriptions, lab results, referrals, patient communications, documents/images, and specialty-specific clinical data (e.g., OB vitals).

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/ehi-page-full.png` | Full-page screenshot of the EHI export documentation landing page at ehi.myqone.com. Shows CCDA, CSV (27 categories), PDF (8 types), Word (6 types), Image (4 types) sections. | **High** — confirms multi-format export structure |
| `downloads/demographic-detail-page.png` | Screenshot of CSV field-level data dictionary for Demographics entity (105 fields). Shows Name/Description/Type columns. | **High** — confirms field-level documentation quality |
| `downloads/ehiexportdocs-raw.json` (110 KB) | Raw extraction of 777 field definitions from the Angular JS bundle. Each field has id, module, field name, type, and description. | **Primary source** — the complete data dictionary |
| `downloads/resourceList-raw.json` (3.6 KB) | Raw extraction of 27 CSV resource types with IDs and descriptions. | **High** — the entity catalog |
| `downloads/main.js` (408 KB) | Compiled Angular bundle containing the embedded data dictionary. | **Source** — verified the raw extractions are accurate |
| `downloads/ehi-page.html` (7 KB) | Angular SPA shell HTML — no content (rendered client-side). | **Low** — confirms SPA architecture only |
| `downloads/TRIARQ-QSuite-Disclosure-Transparency-Statement.pdf` (299 KB, 7 pages) | Mandatory disclosures document dated December 2024. Lists (b)(10) in certification criteria; no additional export technical details. | **Low** — confirms certification, no export detail |
| `downloads/enrichment/data-dictionary.json` (103 KB) | Prior agent's structured extraction of the data dictionary. Used to cross-check my own extraction. | **Cross-reference** |

## 3. Export Mechanics

- **Format**: Multi-format package:
  - C-CDA XML files (USCDI v3 compliant, C-CDA R2.1 Companion Guide Release 4.1)
  - 27 CSV files for structured tabular data beyond C-CDA scope
  - PDF files (8 document types)
  - Word files (6 document types)
  - Image files (4 image types)
- **Mechanism**: Built-in feature in QSuite Manistee v12.12+. The landing page states it supports "generating single-patient ePHI exports as well as bulk data exports for larger patient populations."
- **Single-patient vs bulk**: Both supported per the documentation.
- **Access constraints / fees**: The Transparency Disclosure Statement lists (b)(10) among certified criteria but does not mention any fees specific to EHI export. No paywall or access restrictions were encountered accessing the documentation site.

## 4. Export Content: What's In It

### CSV Data Dictionary

The data dictionary is embedded in the Angular JS bundle at `ehi.myqone.com` and contains **30 CSV entities with 777 total fields**. The 27 top-level resource types include sub-entities: Patient Cases breaks into 4 sub-entities (Master, Diagnosis, Insurance Plan, Prior Authorization Master), and Prior Authorization has a related Prior Authorization Master entity.

**Field documentation quality:**
- All 777 fields have a description (100%)
- However, 474 fields (61.0%) have **trivial descriptions** that merely restate the field name (e.g., field `SSN` → description "SSN", field `Gender` → description "Gender")
- Only 303 fields (39.0%) have **meaningful descriptions** that add information beyond the field name (e.g., field `PatientID` → "Patient Identifier", field `NDCCode` → "NDC Code")
- Types are documented for every field but limited to 5 values: `text` (490), `numeric` (173), `date` (79), `boolean` (32), plus 3 fields with inconsistent capitalization (`Date` ×2, `Numeric` ×1)
- **No value sets**, foreign keys, relationships, max lengths, or nullability documented
- **No sample data** provided

### Vendor's own content organization

The CSV entities span clinical, billing/financial, and administrative domains:

| Entity | Fields | Category | Description |
|---|---|---|---|
| Demographic | 105 | Administrative | Data used to categorize individuals for identification, records matching |
| Medication | 52 | Clinical | Pharmacologic agents used in diagnosis, cure, treatment, or prevention |
| Immunization | 51 | Clinical | Record of vaccine administration |
| Vitals | 48 | Clinical | Physiologic measurements indicating life-sustaining functions |
| OB Vitals | 43 | Clinical | Pregnancy details of patient |
| Insurances | 39 | Billing & Financial | Data related to insurance coverage for health care |
| Other Care Teams | 33 | Administrative | Person who participates in patient care |
| Primary Care Physician | 33 | Administrative | Provider as first contact and principal point of continuing care |
| Referrals | 33 | Administrative | Request from one health professional to another |
| History | 27 | Clinical | Current and past conditions and observations |
| Pharmacy | 26 | Administrative | Patient pharmacy details |
| Allergy | 25 | Clinical | Harmful physiological responses to substance exposure |
| Patient Cases - Master | 24 | Billing & Financial | Prior authorization master for patient |
| Guarantor | 22 | Billing & Financial | Responsible party for patient bills |
| Medical devices or equipment | 22 | Clinical | Instrument, machine, implant used for medical purpose |
| Charges, Payments and adjustment | 21 | Billing & Financial | Billing charges of patient |
| Problems | 21 | Clinical | Condition, diagnosis, or reason for seeking attention |
| Patient Cases - Prior Auth Master | 20 | Billing & Financial | Prior authorization master details |
| Prior Authorization Master | 20 | Billing & Financial | Prior authorization details |
| Eligibility | 16 | Billing & Financial | Patient eligibility data |
| Prior Authorization | 16 | Billing & Financial | Prior authorization details |
| Appointments | 15 | Administrative | Appointment information |
| Denials | 14 | Billing & Financial | Claim denials |
| Audit Trail | 11 | Administrative | Audit trails of patient |
| Refunds | 11 | Billing & Financial | Patient refunds |
| Reserves | 8 | Billing & Financial | Patient reserves |
| Patient Cases - Diagnosis | 6 | Billing & Financial | Case diagnosis details |
| Patient Cases - Insurance Plan | 6 | Billing & Financial | Case insurance plan details |
| Patient-Provider Messages | 5 | Administrative | Provider messages |
| Patient Alert | 4 | Administrative | Alert messages for patient |

**Category breakdown:**

| Category | Entities | Fields |
|---|---|---|
| Billing & Financial | 13 | 223 |
| Clinical | 8 | 289 |
| Administrative | 9 | 265 |
| **Total** | **30** | **777** |

### Non-CSV Export Components

| Format | Document Types | Details |
|---|---|---|
| CCDA | 1 | HL7 CCDA XML files compliant with USCDI v3, C-CDA R2.1 Companion Guide Release 4.1 |
| PDF | 8 | Patient Messages, Lab Orders Documents, Exam Notes, Patient Letter, Patient Consent, Patient Order Template, Nurse Notes, Patient Education |
| Word | 6 | Exam Notes, Nurse Notes, Billing Statements, Collections, Triage Templates, Patient Forms |
| Image | 4 | Driver License, Insurance Card, DMS Documents, Other |

The non-CSV components have **no field-level documentation** — they list document types only, which is appropriate since these are unstructured file exports (documents, images).

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

TRIARQ organizes their export across five format categories:

**CSV (structured data) — the richest component:**
- **Clinical depth is solid**: Demographics (105 fields), Medication (52 fields with NDC codes, drug database IDs, dosage details), Immunization (51 fields with CVX codes, lot numbers), Vitals (48 fields), OB Vitals (43 fields for pregnancy-specific data), Allergy (25 fields with SNOMED codes), Problems (21 fields), History (27 fields), Medical devices (22 fields). This goes meaningfully beyond USCDI minimum fields.
- **Billing/financial coverage is genuine**: 13 entities with 223 fields covering charges/payments/adjustments, denials, refunds, reserves, insurance details (39 fields), eligibility (16 fields), guarantor (22 fields), prior authorizations (36 fields across 2 entities), and patient cases (56 fields across 4 sub-entities). This is real billing data, not just insurance membership info.
- **Administrative coverage is present**: Appointments (15 fields), referrals (33 fields), care teams (33 fields), pharmacy info (26 fields), patient-provider messages (5 fields), patient alerts (4 fields), and a DMS document index.

**CCDA — standard clinical summary**: References HL7 C-CDA R2.1 and USCDI v3. No vendor-specific customizations documented. This is the standard clinical exchange layer.

**PDF/Word/Image — unstructured documents**: Covers clinical notes (exam notes, nurse notes), patient communications (messages, letters), consent forms, billing statements, collections documents, patient education, lab order documents, triage templates, patient forms, and scanned images (driver license, insurance cards, DMS documents).

The **combination of C-CDA + CSV + documents/images** is well-designed: C-CDA handles the USCDI clinical summary, CSV handles the structured data beyond C-CDA scope (billing, admin, detailed clinical fields), and PDF/Word/Image handles unstructured content.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | `Demographic` CSV (105 fields) — name, DOB, SSN, race, ethnicity, language, address, employer, contacts | Thorough — one of the most detailed entities |
| Encounters / visits | ⚠️ Partial | No dedicated encounter/visit entity. `VisitID` and `VisitDate` appear across clinical entities (Allergy, History, Vitals, etc.) | No standalone visit/encounter table; visit context is embedded in other entities |
| Problems / conditions | ✅ Covered | `Problems` CSV (21 fields) | Adequate |
| Medications / prescriptions | ✅ Covered | `Medication` CSV (52 fields) including NDC codes, drug database IDs, dosage, SIG | Detailed — though no separate e-prescribing transaction entity |
| Allergies | ✅ Covered | `Allergy` CSV (25 fields) with SNOMED codes, NDC codes, reactions | Thorough |
| Immunizations | ✅ Covered | `Immunization` CSV (51 fields) with CVX codes, lot numbers, manufacturer | Very detailed |
| Vitals | ✅ Covered | `Vitals` CSV (48 fields) + `OB Vitals` CSV (43 fields) | Thorough, includes specialty OB vitals |
| Lab results | ⚠️ Partial | Lab Orders Documents exported as PDF only. No structured CSV entity for lab result values | Product has lab integration; exporting only PDFs loses structured queryability |
| Imaging / diagnostic reports | ⚠️ Partial | No dedicated imaging entity. Exam Notes exported as PDF/Word | Product supports diagnostic imaging CPOE (a)(3); no structured imaging results in CSV |
| Procedures | ❌ Not covered | No procedures entity in CSV. Exam Notes (PDF/Word) may contain procedure documentation | Product likely stores procedure records; no dedicated export entity |
| Clinical notes / documents | ✅ Covered | Exam Notes (PDF + Word), Nurse Notes (PDF + Word), Patient Letters (PDF), Patient Education (PDF), DMS Documents (Image), DMS Document Index (CSV) | Multi-format coverage of notes and documents |
| Care plans / goals | ⚠️ Partial | Product is certified for (b)(9) Care Plan. No dedicated care plan CSV entity; may be in C-CDA | Certified for care plans but no dedicated structured export beyond C-CDA |
| Orders / referrals | ✅ Covered | `Referrals` CSV (33 fields), Patient Order Template (PDF), Lab Orders Documents (PDF) | Referrals well-covered; orders partially via PDF |
| Insurance / coverage | ✅ Covered | `Insurances` CSV (39 fields), `Eligibility` CSV (16 fields), Insurance Card (Image) | Thorough |
| Claims / billing | ✅ Covered | `Charges, Payments and adjustment` CSV (21 fields), `Denials` (14 fields), `Refunds` (11 fields), `Reserves` (8 fields), Billing Statements (Word), Collections (Word) | Genuine billing coverage across multiple entities |
| Payments | ✅ Covered | Included in `Charges, Payments and adjustment` (21 fields), `Refunds` (11 fields) | Combined with charges entity |
| Consents / directives | ✅ Covered | Patient Consent (PDF) | Document export only, no structured data |
| Patient communications | ✅ Covered | `Patient-Provider Messages` CSV (5 fields), Patient Messages (PDF), Patient Letters (PDF) | Messages exported in both CSV and PDF |
| Prior authorizations | ✅ Covered | `Prior Authorization` (16 fields), `Prior Authorization Master` (20 fields), `Patient Cases - Prior Authorization Master` (20 fields) | Very detailed — 56 fields across 3 related entities |
| Specialty-specific (OB/GYN) | ✅ Covered | `OB Vitals` CSV (43 fields) — pregnancy-specific clinical data | Notable specialty coverage |

**Summary**: 13 of 19 applicable domains are covered (✅), 4 are partially covered (⚠️), and 1 is not covered (❌). The most significant gaps are structured lab results (exported as PDF only, losing queryability) and procedures (no dedicated entity).

## 6. Documentation Quality

**Strengths:**
- **Purpose-built documentation site**: TRIARQ built a dedicated Angular web application at `ehi.myqone.com` with a searchable sidebar, entity detail pages, and clean layout. This is substantially more effort than most vendors.
- **Complete field-level dictionary**: Every one of the 777 CSV fields has a name, description, and type. Zero fields lack descriptions.
- **Multi-format awareness**: Documentation clearly distinguishes between structured (CSV) and unstructured (PDF/Word/Image) export components and documents both.
- **Both single-patient and bulk export**: Explicitly states support for both modes.

**Weaknesses:**
- **Description quality is shallow**: 61% of field descriptions (474 of 777) are trivial restatements of the field name (e.g., `Gender` → "Gender", `SSN` → "SSN"). Only 39% add meaningful information.
- **Coarse data types**: Only 5 types used (`text`, `numeric`, `date`, `boolean`, and 3 inconsistently capitalized variants). No integer vs. decimal distinction, no string lengths, no datetime formats.
- **No value sets or coded values**: Fields like `HistoryStatus`, `HistoryCategory`, `Reaction`, `Gender`, `Race`, `MaritalStatus` don't document valid values.
- **No relationships/foreign keys**: Entity relationships must be inferred from repeated field names like `PatientID` and `VisitID`.
- **No sample data or example exports**: No sample CSV files, no example C-CDA documents.
- **No export instructions**: No user guide for initiating an export in QSuite.
- **C-CDA documented by reference only**: Links to HL7 spec but no vendor-specific customizations or constraints documented.

**Usability assessment**: A developer could build a basic import schema from the field definitions but would need actual export data to reverse-engineer relationships, value sets, and format details. The documentation is sufficient to understand *what* is exported but not to build a reliable import without sample data.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Comprehensive**

This export demonstrably covers data domains well beyond USCDI and C-CDA. The 13 billing/financial entities (223 fields) covering charges, payments, denials, refunds, reserves, insurance, eligibility, guarantor, and prior authorizations represent genuine billing data — not just insurance membership info. The inclusion of OB Vitals (43 fields) shows specialty-specific clinical coverage. Appointments, referrals, care teams, patient messages, document management, and consent forms round out the administrative and communication domains. The only significant structural gap is the absence of structured lab results (exported as PDF only) and a dedicated procedures entity. Relative to what QSuite stores (as an integrated EHR/PM platform for specialty ambulatory practices), this export covers the substantial majority of patient-facing data domains.

**Axis 2 — Export approach: Purpose-built EHI export**

This is clearly a purpose-built (b)(10) export, not a repackaged clinical exchange. The evidence:
1. **Dedicated documentation site** (`ehi.myqone.com`) built as an Angular web application — not a link to a FHIR spec or C-CDA standard.
2. **777 fields across 30 CSV entities** covering billing, insurance, prior auth, denials, refunds — data domains absent from any C-CDA or FHIR (g)(10) export.
3. **Multi-format design** that uses C-CDA for clinical summaries AND CSV for structured data beyond C-CDA scope AND PDF/Word/Image for unstructured documents — this is a deliberate architectural choice.
4. **The export goes well beyond USCDI**: USCDI covers ~22 data classes; this export adds charges, payments, denials, refunds, reserves, eligibility, guarantor, prior authorization, patient cases, appointments, pharmacy, patient alerts, DMS document index, and audit trail.

### Key Findings

1. **Genuine purpose-built EHI export with real billing coverage**: 13 billing/financial entities with 223 fields (charges, payments, denials, refunds, reserves, insurance, eligibility, guarantor, prior auth) demonstrate this is not a repackaged clinical summary. This is one of the better small-vendor (b)(10) implementations.

2. **Multi-format export is well-designed**: The C-CDA + CSV + PDF/Word/Image approach is architecturally sound — each format handles the data type it's best suited for. 19 non-CSV document types cover clinical notes, billing statements, consent forms, and scanned images.

3. **Lab results gap**: Despite QSuite having lab integration features, lab results are exported only as PDF documents (Lab Orders Documents), not as structured CSV data. This means lab values lose queryability in the export.

4. **Field descriptions are shallow**: While 100% of fields have a description, 61% are trivial restatements of the field name. No value sets, no foreign keys, no sample data are provided. The documentation tells you what data exists but requires actual export files to understand the details.

5. **Specialty data included**: The OB Vitals entity (43 fields) for pregnancy-specific data shows the vendor considered specialty-specific clinical data in their export, not just generic ambulatory data.

### Summary Stats

```
Coverage:        Comprehensive
Approach:        Purpose-built EHI export
Export format:   C-CDA + CSV + PDF + Word + Image (multi-format)
Entities:        30 (CSV) + 19 non-CSV document types
Fields:          777 (CSV fields with data dictionary)
Descriptions:    100% have descriptions; 39% meaningful (61% trivially restate field name)
Sample data:     No
Bulk export:     Yes
Domains covered: 13 of 19 applicable domains fully covered; 4 partial; 1 not covered
```

### Bottom Line

TRIARQ built a genuine, purpose-built EHI export that covers clinical, billing, insurance, administrative, and specialty data across 30 CSV entities and 19 document types — well beyond a repackaged C-CDA or FHIR summary. A patient or provider would receive a substantially complete copy of their record, though structured lab results and procedure data are the most notable gaps. The documentation is better than most small vendors but would benefit from value sets, sample data, and non-trivial field descriptions.
