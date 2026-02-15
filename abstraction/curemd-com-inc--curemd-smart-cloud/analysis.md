# EHI Export Analysis: CureMD.com, Inc.

**Product**: CureMD SMART Cloud (version 10g)
**Analysis date**: 2026-02-15
**CHPL ID**: 15.07.04.2706.CURE.10.01.1.230302 (CHPL #11246)

## 1. Product Context

CureMD SMART Cloud is a comprehensive, cloud-based ambulatory healthcare platform integrating EHR, practice management, patient portal (LEAP), and revenue cycle management. Founded in 1997, the company claims 30,000+ practices, 109,000+ users across 44 states and 32+ specialties including oncology, OB/GYN, behavioral health, dermatology, and more. It is certified across 35+ ONC criteria including (b)(10) for EHI export.

Key data domains the product stores that are relevant for export completeness:
- **Clinical**: Charting, encounter notes, problem lists, medications, allergies, vitals, lab results, imaging, immunizations, referrals, care plans, clinical decision support
- **E-Prescribing**: Prescriptions including EPCS, medication reconciliation, formulary data
- **Practice Management**: Demographics, scheduling, insurance eligibility, document management, referral management
- **Billing/RCM**: Charge capture, claims submission/scrubbing, payment posting, denial management, ERA processing, patient balances
- **Patient Portal**: Secure messaging, lab results access, appointment scheduling, online payments, wearable device data
- **Specialty**: Oncology/chemotherapy protocols, OB/GYN history, behavioral health screenings (GAD-7, PHQ-9)
- **Telehealth**: Integrated video visits
- **CCM/RPM**: Care plans, time tracking, remote monitoring data

This breadth of functionality sets a high bar for what "all EHI" should include.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `EHI_Export_DRS.xlsx` (101 KB) | Primary artifact: 2-sheet Excel file with export overview and data dictionary (38 data classes, 891 fields). SQL data types and descriptions for every field. | **Most informative** |
| `ehi-export-page.html` (125 KB) | Saved HTML of https://www.curemd.com/ehi-export.asp describing (b)(10) export mechanics | Moderately informative |
| `CureMD.pdf` (1.3 MB, 20 pages) | Marketing brochure covering EHR/PM features, specialties, and deployment options | Not EHI-specific; useful for product context only |
| `screenshot-ehi-export-page.png` (802 KB) | Viewport screenshot of the EHI export page | Confirmatory only |
| `enrichment/drs-data-dictionary.json` (166 KB) | Prior agent's JSON extraction of the XLSX data dictionary | Cross-reference (verified against my own parsing) |
| `enrichment/drs-summary.json` (30 KB) | Prior agent's summary of data classes and field names | Cross-reference |

The XLSX data dictionary is the sole substantive EHI export artifact. The web page provides export mechanics. No sample data, no schema files, and no relationship documentation were provided.

**Verification note**: The prior agent's report claims 893 fields. My independent parsing of the XLSX yields **891 actual data fields** across 36 data classes with tabular definitions. The discrepancy is because the prior agent counted placeholder entries ("-") for the two special classes (Documents & Images and Provider Notes) as fields. These two classes have no tabular field definitions — they describe files exported in native formats.

I also verified the EHI export page is live and accessible at https://www.curemd.com/ehi-export.asp as of the analysis date.

## 3. Export Mechanics

- **Format**: CSV files for structured data; native format for documents and images; HTML for provider notes. All delivered as ZIP archives.
- **Mechanism**: In-application "EHI Export module" accessible to system administrators.
  - **Single patient**: Initiated directly in the application without developer assistance. Download link provided once extraction is complete.
  - **Population/bulk**: Requested from within the application; updates delivered via email.
- **Access constraints**: Requires system administrator role. No mention of fees. No developer assistance needed for single-patient export.
- **Documentation source**: XLSX data dictionary linked from https://www.curemd.com/ehi-export.asp. Last updated November 2023 (8 months post-certification in March 2023).

## 4. Export Content: What's In It

The export is documented via a single XLSX file with a "DRS" (Designated Record Set) sheet containing **38 data classes** and **891 fields** (excluding 2 special classes exported as native-format files).

**Documentation quality per field**:
- 891 of 891 fields (100%) have descriptions — plain English explanations
- 891 of 891 fields (100%) have SQL data types (varchar, int, datetime, numeric, float, bit, text, nvarchar, date)
- No value sets or coded value enumerations are provided
- No foreign key or relationship documentation
- No sample data

### Vendor's own content organization

The vendor organizes export data into 38 "data classes." All tabular data classes have complete field-level documentation.

| Data Class | Fields | Described | Types | Domain |
|---|---|---|---|---|
| Allergies | 15 | 15 | Yes | Clinical |
| Appointments | 20 | 20 | Yes | Administrative |
| Cases | 18 | 18 | Yes | Care Coordination |
| Charges | 82 | 82 | Yes | Billing & Financial |
| Chemo Admin | 15 | 15 | Yes | Specialty (Oncology) |
| Chemo Admin IVSites | 6 | 6 | Yes | Specialty (Oncology) |
| Chemo Plan | 22 | 22 | Yes | Specialty (Oncology) |
| Chemo Plan Diagnosis | 7 | 7 | Yes | Specialty (Oncology) |
| Chemo Plan Drugs | 28 | 28 | Yes | Specialty (Oncology) |
| Claims | 16 | 16 | Yes | Billing & Financial |
| Complaints | 6 | 6 | Yes | Clinical |
| Diagnosis | 18 | 18 | Yes | Clinical |
| Disclosures | 11 | 11 | Yes | Consent |
| Diseases History | 21 | 21 | Yes | Clinical History |
| Documents & Images | N/A (native format) | N/A | N/A | Documents |
| Electronic Remittance Advice | 19 | 19 | Yes | Billing & Financial |
| Family History | 12 | 12 | Yes | Clinical History |
| Hospitalization History | 6 | 6 | Yes | Clinical History |
| Immunizations | 20 | 20 | Yes | Clinical |
| Medications | 19 | 19 | Yes | Clinical |
| Memos | 8 | 8 | Yes | Communications |
| OBGYN History | 52 | 52 | Yes | Specialty (OB/GYN) |
| Orders | 24 | 24 | Yes | Clinical |
| Patient Consents | 5 | 5 | Yes | Consent |
| Patient Contacts | 20 | 20 | Yes | Demographics |
| Patient Demographics | 71 | 71 | Yes | Demographics |
| Patient Education | 6 | 6 | Yes | Patient Education |
| Patient Insurances | 76 | 76 | Yes | Insurance |
| Patient Note | 16 | 16 | Yes | Communications |
| Payments | 77 | 77 | Yes | Billing & Financial |
| Provider Notes | N/A (exported as HTML) | N/A | N/A | Documents |
| Referrals | 23 | 23 | Yes | Care Coordination |
| Results | 29 | 29 | Yes | Clinical |
| Risk | 8 | 8 | Yes | Clinical |
| Social History | 65 | 65 | Yes | Clinical History |
| Surgery History | 18 | 18 | Yes | Clinical History |
| Vitals A | 23 | 23 | Yes | Clinical |
| Vitals B | 9 | 9 | Yes | Clinical |

**Full inventory**: See `analysis/full-entity-inventory.json` for all 891 fields with names, types, and descriptions.

### Notable data classes

- **Charges** (82 fields): The largest tabular class. Includes CPT codes, modifiers, diagnoses, plan/patient balances, claim status, billing/rendering provider details, place of service, and financial breakdowns. Genuine billing-level detail.
- **Payments** (77 fields): Includes payment method, denial reasons, plan payments, patient payments, transfers, write-offs, check/CC numbers, deposit dates, and payment plans. Very granular financial data.
- **Patient Insurances** (76 fields): Covers primary, secondary, and tertiary insurance plans each with subscriber info, policy/group numbers, effective/termination dates, insured party demographics, and copay amounts.
- **Patient Demographics** (71 fields): Comprehensive — includes race, ethnicity, language, gender identity, sexual orientation, religion, income, household size, responsible party info, alternate addresses, portal account status, and date of death.
- **Social History** (65 fields): Unusually detailed — covers tobacco, alcohol, drug use, sexual history (including STD risk factors, protection methods), occupation, education, sleep, diet/exercise, and dermatology-specific UV exposure/tanning history.
- **OBGYN History** (52 fields): Full reproductive history including pregnancy details, menstrual data, contraception, GYN screening dates, and obstetric summary (gravida/para).
- **Chemotherapy classes** (5 classes, 78 fields total): Oncology-specific data covering treatment plans, drug regimens (with dose calculations, routes, infusion rates), administration records, IV sites, and diagnoses.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The export spans 8 functional domains in the vendor's organization:

| Domain | Classes | Total Fields |
|---|---|---|
| Demographics & Contacts | 2 | 91 |
| Clinical - Core (allergies, dx, meds, vitals, labs, orders, complaints, risk) | 10 | 171 |
| Clinical - History (disease, family, hospitalization, surgery, social) | 5 | 122 |
| Specialty - OB/GYN | 1 | 52 |
| Specialty - Oncology | 5 | 78 |
| Billing & Financial (charges, claims, payments, ERA) | 4 | 194 |
| Insurance | 1 | 76 |
| Documents & Notes (provider notes, documents/images, memos, patient notes, education) | 5 | 30 |
| Care Coordination (referrals, cases, appointments, consents, disclosures) | 5 | 77 |

The billing/financial domain is the richest (194 fields across 4 classes), followed by clinical history (174 fields across 6 classes). This is a strong signal of a genuine (b)(10) effort — billing data is the most commonly omitted domain in EHI exports.

The oncology and OB/GYN specialty data are also notable inclusions that go well beyond USCDI/US Core.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | `Patient Demographics` (71 fields), `Patient Contacts` (20 fields) | Thorough — includes race, ethnicity, language, gender identity, sexual orientation, religion |
| Encounters / visits | ⚠️ Partial | `Appointments` (20 fields) has date, provider, location, status, check-in/out times; `Cases` (18 fields) has case management data | Appointment scheduling is documented; however, there's no dedicated encounter entity tying clinical activities to a visit. Visit context is implicit via appointment IDs in other tables. |
| Problems / conditions / diagnoses | ✅ Covered | `Diagnosis` (18 fields) with ICD-10/ICD-9, status, onset, severity, chronic flag; `Diseases History` (21 fields) | Comprehensive problem list with coded diagnoses |
| Medications / prescriptions | ✅ Covered | `Medications` (19 fields) with NDC codes, prescriber NPI, status, chronic flag, start/end dates | Covers current and historical medications. E-prescribing detail (SIG, pharmacy, quantity) not explicitly present as separate fields — may be embedded in medication records or provider notes. |
| Allergies | ✅ Covered | `Allergies` (15 fields) with RxNorm coding, severity, reactions, onset | Well-documented |
| Immunizations | ✅ Covered | `Immunizations` (20 fields) with CVX codes, NDC codes, lot numbers, dosage, ordering provider | Thorough |
| Vitals | ✅ Covered | `Vitals A` (23 fields: height, weight, BMI, BSA, O2 sat, pain, blood type, etc.) + `Vitals B` (9 fields: pulse, respiration, temp, BP) | Split across two tables but comprehensive |
| Lab results | ✅ Covered | `Results` (29 fields) with LOINC codes, values, units, ranges, flags; `Orders` (24 fields) with CPT, status, specimen | Good coverage with standard coding |
| Imaging / diagnostic reports | ⚠️ Partial | `Orders` includes radiology orders with `Radiology Result` field; `Results` has `Radiology Result` field | Radiology results appear within the general orders/results tables. No dedicated imaging entity. Actual images would be in Documents & Images. |
| Procedures | ⚠️ Partial | `Charges` contains CPT codes/descriptions for procedures billed; `Surgery History` (18 fields) covers past surgeries | Procedures are documented through billing charges and surgery history, but there's no dedicated procedure entity for in-visit procedures not yet billed. |
| Clinical notes / documents | ✅ Covered | `Provider Notes` exported as HTML files; `Documents & Images` exported in native formats; `Patient Note` (16 fields); `Memos` (8 fields) | Provider notes exported as rendered HTML; documents/images in native format. No structured note metadata in tabular form. |
| Care plans / goals | ❌ Not covered | No dedicated care plan or goal entity | CureMD offers CCM care plans (see Section 1). Their absence from the export is a gap for practices using that module. |
| Orders / referrals | ✅ Covered | `Orders` (24 fields) for lab/imaging; `Referrals` (23 fields) with diagnosis, procedure, urgency | Well-documented |
| Insurance / coverage | ✅ Covered | `Patient Insurances` (76 fields) covering primary, secondary, and tertiary plans with full subscriber/insured party detail | Exceptionally thorough |
| Claims / billing | ✅ Covered | `Charges` (82 fields), `Claims` (16 fields) | Detailed charge-level and claim-level data with financial breakdowns |
| Payments | ✅ Covered | `Payments` (77 fields), `Electronic Remittance Advice` (19 fields) | Very granular — includes ERA data, denial reasons, payment plans |
| Consents / directives | ✅ Covered | `Patient Consents` (5 fields), `Disclosures` (11 fields) | Basic consent tracking — type, status, date range. Disclosures track PHI releases. |
| Patient communications / portal messages | ⚠️ Partial | `Memos` (8 fields), `Patient Note` (16 fields with task-related fields) | Memos and patient notes may cover some provider-patient communications, but no dedicated secure messaging entity for portal messages. |
| Specialty-specific: Oncology | ✅ Covered | 5 chemo classes (78 fields): plans, drugs (with dosing, routes, infusion rates), administration, IV sites, diagnoses | Genuinely deep specialty data |
| Specialty-specific: OB/GYN | ✅ Covered | `OBGYN History` (52 fields): reproductive history, pregnancy details, screening dates, contraception | Comprehensive |
| Specialty-specific: Behavioral health | ❌ Not covered | No dedicated behavioral health screening or assessment entity (e.g., GAD-7, PHQ-9 scores) | CureMD supports behavioral health with screening tools. These may be embedded in provider notes or results, but no dedicated structured data class exists. |
| Specialty-specific: Dermatology | ⚠️ Partial | `Social History` includes 17 dermatology-specific fields (UV exposure, tanning, skin cancer, etc.) | Some specialty content is embedded in Social History, but no dedicated dermatology-specific clinical entities. |

**Summary**: 14 of 20 applicable domains are covered or well-covered, 4 are partially covered, and 2 are not covered. The most significant gap is the absence of care plans/goals despite the product having a CCM module.

## 6. Documentation Quality

**Strengths**:
- Every tabular field (891/891) has a name, SQL data type, and plain English description
- The data dictionary is structured, consistent, and machine-parseable (XLSX format)
- Export mechanics are clearly described (single-patient vs. population, CSV format, ZIP delivery)
- SQL data types (varchar, int, datetime, numeric, float, bit) indicate direct database-to-CSV mapping

**Weaknesses**:
- **No value sets**: Coded fields like `Status`, `Severity`, `Type`, `Category` have descriptions but no enumeration of valid values. A developer would need to discover valid values from actual data.
- **No relationship documentation**: Tables share implicit keys (Patient ID, Account Number, Appointment ID, Chemo Plan ID) but there are no foreign key definitions, ERD, or explicit join documentation. A developer would need to infer relationships.
- **No sample data**: No example CSV files, no sample records, no worked examples of an actual export.
- **No schema files**: No JSON Schema, XSD, DDL, or OpenAPI specification — only the XLSX dictionary.
- **Provider Notes and Documents & Images lack field definitions**: These are described as "exported in native format" and "exported as HTML" but have no metadata schema.

**Developer usability**: A developer could understand the data model and build a basic import from this documentation. However, understanding relationships between tables (e.g., linking Charges → Claims → ERA → Payments) would require significant inference. The absence of value sets means coded fields need empirical discovery.

## 7. Overall Assessment

### Classification

**Comprehensive native export**

This is a genuine (b)(10) implementation that exports the vendor's native database model, not a repackaging of FHIR or C-CDA. Key evidence:
1. CSV format maps directly to SQL Server column types — this is a flat-file projection of the relational database
2. 38 data classes covering clinical, billing, insurance, specialty, and administrative domains
3. Billing data (Charges, Claims, Payments, ERA) is present with deep granularity — 194 fields across 4 classes
4. Oncology and OB/GYN specialty data are included with dedicated structured entities
5. No mention of FHIR, C-CDA, or USCDI in the export documentation

### Key Findings

1. **Genuinely broad coverage with real billing depth**: 891 fields across 38 data classes. The billing/financial domain (194 fields) is among the most detailed seen in (b)(10) exports. Charges, claims, payments, and ERA data are all present with field-level documentation.

2. **100% field documentation rate**: Every one of the 891 tabular fields has both a SQL data type and a plain English description. This is above average for (b)(10) data dictionaries.

3. **Meaningful specialty data**: Oncology (5 data classes, 78 fields covering chemo plans, drugs, administration) and OB/GYN (52-field reproductive history) demonstrate export of specialty clinical content beyond USCDI. Social History includes dermatology-specific UV exposure fields (17 fields).

4. **Missing care plans and secure messaging**: Despite offering CCM care plan and patient portal messaging features, neither has a dedicated data class in the export. This is the most notable coverage gap.

5. **No relationship or value set documentation**: While field-level documentation is complete, the absence of foreign key definitions, ERD diagrams, and coded value enumerations reduces developer usability. Relationships must be inferred from shared key field names (Patient ID, Account Number, Appointment ID).

### Summary Stats

```
Classification:  Comprehensive native export
Export format:   CSV (structured data); native formats (documents/images); HTML (provider notes)
Model type:      Native database
Entities:        38 data classes (36 tabular + 2 native-format)
Fields:          891 (tabular fields with definitions)
Descriptions:    100%
Sample data:     No
Bulk export:     Yes (population-level export available via request)
Domains covered: 14 of 20 applicable domains fully covered; 4 partial; 2 not covered
```

### Bottom Line

CureMD's EHI export is one of the stronger (b)(10) implementations. It exports a genuine native database model with 891 documented fields spanning clinical, billing, insurance, and specialty domains — notably including detailed oncology and OB/GYN data that most vendors omit. The biggest gaps are the absence of care plan/goal data (despite a CCM module) and secure portal messaging, plus the lack of relationship documentation that would be needed for full data reconstruction.
