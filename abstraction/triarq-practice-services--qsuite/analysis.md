# EHI Export Analysis: TRIARQ Practice Services

**Product**: QSuite (version "Manistee")
**Analysis date**: 2026-02-16
**CHPL ID**: 15.02.05.2614.TRIQ.01.01.1.211105

## 1. Product Context

QSuite is a cloud-based integrated EHR and practice management platform developed by TRIARQ Practice Services (formerly gloStream), now a wholly owned subsidiary of Blue Cross Blue Shield of Michigan. The product targets independent ambulatory specialty practices, particularly in orthopedics, urology, oncology, cardiology, neurology, and gastroenterology. It is hosted on Google Cloud Platform.

QSuite is not just an EHR — it is a full MSO (managed services organization) technology stack spanning:

- **Clinical documentation** (charting, notes, QScribe AI-generated notes, voice recognition)
- **E-prescribing** (Surescripts-certified, EPCS via third-party integration)
- **Practice management** (scheduling, patient registration, insurance verification, prior authorization)
- **Billing / RCM** (claims, A/R, denial management, patient payments, collections)
- **Patient portal** (MyQOne — results, messages, scheduling, billing access)
- **Lab integration** (orders and results from external labs)
- **Referral management** (QPathways care coordination)
- **Reporting/Analytics** (QInsights dashboards, CQM/MIPS reporting)

For (b)(10) completeness, the export should cover clinical data across multiple specialties, billing/claims data, insurance, prescriptions, lab results, patient portal communications, referrals, and document management.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/enrichment/data-dictionary.json` (103 KB) | Complete structured data dictionary extracted from Angular JS bundle: 32 CSV entities, 777 fields, plus 4 non-CSV export categories with 19 document types | **Primary source** — most informative |
| `downloads/ehiexportdocs-raw.json` (110 KB) | Raw extraction of the `ehiexportdocs` array from JS bundle — 777 field definitions with module, field, type, and description | Cross-validation source |
| `downloads/resourceList-raw.json` (3.6 KB) | Raw extraction of `resourceList` array — 27 CSV resource types with IDs and descriptions | Cross-validation source |
| `downloads/main.js` (408 KB) | Compiled Angular bundle containing the complete EHI export data dictionary | Source of truth for all structured data |
| `downloads/ehi-page.html` (7.0 KB) | Angular SPA shell — no content (renders client-side) | Low — just confirms Angular architecture |
| `downloads/ehi-page-full.png` (176 KB) | Full-page screenshot of EHI export landing page showing CCDA, CSV, PDF, Word, Image sections | Visual confirmation of export organization |
| `downloads/demographic-detail-page.png` (173 KB) | Screenshot of Demographic CSV entity detail page showing field definitions table | Visual confirmation of data dictionary format |
| `downloads/TRIARQ-QSuite-Disclosure-Transparency-Statement.pdf` (299 KB, 7 pages) | Mandatory disclosures document dated December 2024. Lists 48 certification criteria including (b)(10) | Low — no EHI export technical details |
| `downloads/enrichment/extraction-report.json` (1.5 KB) | Extraction accounting: 0 parse failures | Confirms extraction completeness |

The EHI documentation site at `https://ehi.myqone.com/` is live and returns HTTP 200 as of analysis date.

## 3. Export Mechanics

- **Format**: Multi-format package:
  - C-CDA XML files (USCDI v3, C-CDA R2.1 Companion Guide Release 4.1)
  - 27 CSV files for structured tabular data
  - PDF documents (8 document types)
  - Word documents (6 document types)
  - Image files (4 image types)
- **Mechanism**: Described as a built-in feature of "QSuite Manistee v12.12 and later." No specific UI instructions or API endpoints are documented. The documentation states the capability exists but does not describe how to invoke it.
- **Single-patient vs bulk**: The documentation explicitly states: "The EHI Export feature also supports generating single-patient ePHI exports as well as bulk data exports for larger patient populations."
- **Access constraints**: The Transparency Disclosure Statement lists QSuite as available via one-time license fee or hosted monthly fee. No specific additional fees for EHI export are mentioned. However, the disclosure document does not explicitly address (b)(10) costs either way.

## 4. Export Content: What's In It

### Structured CSV data

The CSV portion of the export contains **30 entities with field definitions** (plus 2 parent groupings without their own fields) totaling **777 fields**. Every field has a name, description, and type.

**Description quality**: While 100% of fields have a description string, the descriptions are largely mechanical reformattings of the field name. Of 777 fields, **529 (68.1%) have trivial descriptions** that merely expand CamelCase into words (e.g., `PatientID` → "Patient Identifier", `VisitDate` → "Visit Date"). Only **248 fields (31.9%) have descriptions that add any information** beyond the field name (e.g., `DOEAllergy` → "Date of Estimated Allergy", `DOS` → "Date of Service", `Rx_bMaySubstitute` → "Rx May Substitute").

**Type system**: All fields are typed, but with only 4 coarse types: `text` (490 fields, 63.1%), `numeric` (174, 22.4%), `date` (81, 10.4%), `boolean` (32, 4.1%). No precision, length constraints, or format specifications. Minor casing inconsistencies exist (`Date` vs `date`, `Numeric` vs `numeric`) — 3 fields use capitalized types.

**No value sets, foreign keys, relationships, or sample data** are provided.

### Non-CSV exports

| Format | Document Types |
|---|---|
| **CCDA** | HL7 C-CDA XML files (USCDI v3 compliant) |
| **PDF** | Patient Messages, Lab Orders Documents, Exam Notes, Patient Letter, Patient Consent, Patient Order Template, Nurse Notes, Patient Education |
| **Word** | Exam Notes, Nurse Notes, Billing Statements, Collections, Triage Templates, Patient Forms |
| **Image** | Driver License, Insurance Card, DMS Documents, Other |

These non-CSV exports have no field-level specifications — they list document types included but provide no schema or structure documentation, which is appropriate for unstructured file exports.

### Vendor's own content organization

The vendor organizes CSV entities as a flat list. The table below shows all 30 entities with fields, ordered by field count:

| Entity/Table | Fields | Types | Description |
|---|---|---|---|
| Demographic | 105 | yes | Patient identification, contacts, parents, guardian, employer, registration |
| Medication | 52 | yes | Prescriptions, drugs, NDC/RxNorm codes, pharmacy, e-Rx details |
| Immunization | 51 | yes | Vaccine records, CVX codes, lot numbers, VIS, administration details |
| Vitals | 48 | yes | Standard vital signs and clinical measurements |
| OB Vitals | 43 | yes | Pregnancy-specific clinical data |
| Insurances | 39 | yes | Insurance plans, subscriber details, coverage, workers comp |
| Other Care Teams | 33 | yes | Care team members, contact information, specialties |
| Primary Care Physician | 33 | yes | PCP details, contact information, facility |
| Referrals | 33 | yes | Referral requests, providers, authorization, status |
| History | 27 | yes | Past medical/surgical/family/social history, SNOMED codes |
| Pharmacy | 26 | yes | Patient pharmacy information, NCPDP IDs, service levels |
| Allergy | 25 | yes | Allergies, reactions, SNOMED/NDC codes |
| Patient Cases - Master | 24 | yes | Case management: injury, workers comp, hospitalization |
| Guarantor | 22 | yes | Responsible party for billing |
| Medical devices or equipment | 22 | yes | Implantable devices, UDI, SNOMED codes |
| Charges, Payments and adjustment | 21 | yes | Claims, CPT codes, diagnoses, payments, adjustments |
| Problems | 21 | yes | Problem list, ICD-9 codes, SNOMED, resolution status |
| Patient Cases - Prior Auth Master | 20 | yes | Prior authorization details linked to cases |
| Prior Authorization Master | 20 | yes | Prior authorization records with tracking |
| Eligibility | 16 | yes | Insurance eligibility responses |
| Prior Authorization | 16 | yes | Prior authorization summary view |
| Appointments | 15 | yes | Appointment scheduling, provider, status, location |
| Denials | 14 | yes | Claim denials with payer remarks |
| Audit Trail | 11 | yes | Patient activity audit records |
| Refunds | 11 | yes | Payment refund records |
| Reserves | 8 | yes | Payment reserve records |
| Patient Cases - Diagnosis | 6 | yes | Diagnoses linked to patient cases |
| Patient Cases - Insurance Plan | 6 | yes | Insurance plans linked to cases |
| Patient-Provider Messages | 5 | yes | Portal messages between patients and providers |
| Patient Alert | 4 | yes | Patient alert messages |

Two entities (`DMS Document(Index)` and `Patient Cases`) serve as parent groupings with no fields of their own.

The full entity inventory with all 777 field definitions is in `analysis/full-entity-inventory.json`.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor does not explicitly categorize entities into domains, but the export spans multiple areas:

**Clinical data (strongest coverage)**: Demographics (105 fields — very thorough, including parents, guardian, employer, communication preferences), Medication (52 fields — includes NDC, RxNorm, prescriber details, e-Rx reference numbers), Immunization (51 fields — CVX codes, lot numbers, VIS tracking), Vitals (48 fields), OB Vitals (43 fields — specialty-specific pregnancy data), History (27 fields — medical/surgical/family/social with SNOMED), Allergy (25 fields — with SNOMED/NDC), Problems (21 fields — with ICD-9, SNOMED), Medical devices (22 fields — with UDI, SNOMED).

**Billing/financial data (solid coverage)**: Charges, Payments and adjustment (21 fields — CPT, diagnoses, amounts, adjustments), Denials (14 fields), Refunds (11 fields), Reserves (8 fields), Guarantor (22 fields). This is one of the stronger aspects — many vendors omit billing entirely.

**Insurance (strong coverage)**: Insurances (39 fields — detailed subscriber info, payer IDs, coverage types, workers comp flags), Eligibility (16 fields), Prior Authorization (16 + 20 fields across two entities), Patient Cases (56 fields across 4 sub-entities including case management, workers comp, injury dates).

**Care coordination**: Other Care Teams (33 fields), Primary Care Physician (33 fields), Referrals (33 fields), Pharmacy (26 fields).

**Administrative/communication**: Appointments (15 fields), Patient-Provider Messages (5 fields — thin), Patient Alert (4 fields — very thin), DMS Document Index (parent only, 0 CSV fields).

**Documents**: 8 PDF document types (clinical notes, lab orders, consent, education, messages), 6 Word document types (notes, billing statements, collections, triage, forms), 4 image types (driver license, insurance card, DMS documents).

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | `Demographic` (105 fields) — name, DOB, SSN, race, ethnicity, language, address, contacts, employer, parents, guardian, communication preferences | Thorough — unusually comprehensive |
| Encounters / visits | ⚠️ Partial | No dedicated encounter entity; `VisitID`/`VisitDate` appear as foreign-key fields in other entities (Allergy, History, Problems, etc.); `Appointments` (15 fields) captures scheduling | Missing dedicated encounter/visit entity with visit-level data (reason, type, disposition, duration) |
| Problems / conditions | ✅ Covered | `Problems` (21 fields) — ICD-9, SNOMED, status, resolution | Solid; ICD-9 field naming (not ICD-10) may reflect legacy naming but could export current codes |
| Medications / prescriptions | ✅ Covered | `Medication` (52 fields) — NDC, RxNorm, dosage, route, frequency, prescriber, e-Rx details, pharmacy, narcotic flag, refills | Strong — includes e-prescribing details |
| Allergies | ✅ Covered | `Allergy` (25 fields) — SNOMED, NDC, reactions, drug database IDs | Solid |
| Immunizations | ✅ Covered | `Immunization` (51 fields) — CVX codes, lot numbers, manufacturer, VIS tracking, administration site | Thorough |
| Vitals | ✅ Covered | `Vitals` (48 fields) | Thorough |
| Lab results | ⚠️ Partial | Lab Orders Documents exported as PDF only; no structured CSV entity for lab result values | Product integrates with external labs and stores results; PDF-only export loses queryability of discrete lab values |
| Imaging / diagnostic reports | ❌ Not covered | No imaging entity in CSV; no imaging category in non-CSV exports | Product supports CPOE for diagnostic images (certified for (a)(3)); structured imaging data is likely stored but not exported |
| Procedures | ⚠️ Partial | CPT codes appear in `Charges, Payments and adjustment`; no dedicated procedures entity | Procedures only captured as billing line items, not as clinical procedure records |
| Clinical notes / documents | ✅ Covered | Exam Notes and Nurse Notes exported as PDF and Word; Patient Letters as PDF | Exported as documents (appropriate for unstructured notes); no CSV metadata entity for note indexing |
| Care plans / goals | ⚠️ Partial | Product certified for (b)(9) Care Plan; no dedicated care plan entity in CSV export | Certified criterion suggests care plan data exists in system but it does not appear in the export |
| Orders / referrals | ✅ Covered | `Referrals` (33 fields); Lab Orders Documents as PDF; Patient Order Template as PDF | Good referral coverage; orders are document-based rather than structured |
| Insurance / coverage | ✅ Covered | `Insurances` (39 fields), `Eligibility` (16 fields), `Patient Cases - Insurance Plan` (6 fields) | Strong |
| Claims / billing | ✅ Covered | `Charges, Payments and adjustment` (21 fields), `Denials` (14 fields), `Refunds` (11 fields), `Reserves` (8 fields); Billing Statements and Collections as Word documents | Genuinely deep billing coverage — a notable strength |
| Payments | ✅ Covered | Payment data in `Charges, Payments and adjustment` (PatientPayment, InsurancePayment fields); `Refunds` (11 fields) | Included within billing entities |
| Consents / directives | ⚠️ Partial | Patient Consent exported as PDF only | No structured consent data; document-only |
| Patient communications | ⚠️ Partial | `Patient-Provider Messages` (5 fields — PatientID, ProviderID, Date, Message, Subject); Patient Messages as PDF | CSV entity is very thin (5 fields); minimal metadata |
| Specialty-specific (OB) | ✅ Covered | `OB Vitals` (43 fields) — pregnancy-specific clinical data | Strong specialty coverage for obstetrics |
| Specialty-specific (Ortho/Uro/Onc) | ❌ Not covered | No specialty-specific entities for orthopedics, urology, or oncology despite being the vendor's primary target specialties | Product is marketed as "specialty-built" for orthopedics, urology, and oncology; absence of specialty-specific templates/forms is a gap |
| Medical devices | ✅ Covered | `Medical devices or equipment` (22 fields) — UDI, SNOMED | Good implantable device coverage |

**Domains covered**: 12 of 19 applicable domains have dedicated coverage; 5 partial; 2 not covered.

## 6. Documentation Quality

**Strengths**:
- Purpose-built Angular web application at `ehi.myqone.com` — a genuine dedicated documentation effort, not a buried PDF
- Complete field-level data dictionary for all 27 CSV resource types (777 fields)
- Searchable interface with sidebar navigation and individual entity detail pages
- Every field has a name, description, and type
- Both single-patient and bulk export capabilities are documented
- Multi-format approach (CCDA + CSV + PDF + Word + Image) is well-organized

**Weaknesses**:
- **Descriptions are largely trivial**: 68.1% of field descriptions merely reformat the field name (`PatientID` → "Patient Identifier"). A developer gains almost nothing from these.
- **No value sets**: Coded fields like `HistoryStatus`, `Reaction`, `InsuranceType`, `Gender`, `Race`, `AppType` list no valid values. A developer cannot build a valid import without reverse-engineering from actual data.
- **No foreign key/relationship documentation**: Entities share identifiers (`PatientID`, `VisitID`, `nReferralID`, `nPriorAuthorizationID`) but no join relationships or cardinality are documented.
- **No sample data**: No example CSV files, no example export packages.
- **No export invocation instructions**: The documentation describes what the export contains but not how to perform it.
- **No directory structure or packaging documentation**: File naming conventions, directory layout, and packaging format are undocumented.
- **Coarse type system**: Only 4 types (text/numeric/date/boolean) with no precision, length, or format details.

**Could a developer build an import?** Partially. The field names and types would allow building a rough schema, but without value sets, relationships, or sample data, significant reverse-engineering would be required. A developer would need to request an actual export to understand relationships and validate assumptions.

## 7. Overall Assessment

### Classification

**Partial native export**: The export goes well beyond a standard-based projection — it includes native data model entities for billing, insurance, prior authorization, patient cases, pharmacy, and other domains that FHIR/C-CDA do not cover. However, it has meaningful coverage gaps (no dedicated encounters entity, no structured lab results, no specialty-specific clinical data for the vendor's primary specialties) and the documentation, while structurally present, is thin on substance.

### Key Findings

1. **Genuine multi-format (b)(10) implementation**: This is not a repackaged FHIR or C-CDA export. The combination of C-CDA for clinical summaries, CSV for structured billing/administrative data, and PDF/Word/Image for documents is a thoughtful architecture that covers data types a clinical standard alone would miss. The dedicated Angular documentation app at `ehi.myqone.com` shows genuine effort.

2. **Billing coverage is a standout strength**: Five billing-related CSV entities (`Charges, Payments and adjustment`, `Denials`, `Refunds`, `Reserves`, `Guarantor`) plus `Insurances` (39 fields), `Eligibility`, and `Prior Authorization` entities. Many vendors omit billing entirely; TRIARQ exports claim-level detail with CPT codes, diagnoses, payment splits, and denial remarks.

3. **No structured lab results export**: Lab Orders Documents are exported as PDF only. Given QSuite's lab integration features and (a)(2) certification for CPOE-Lab, structured lab result values almost certainly exist in the system but are not included in the structured CSV export. This is a significant gap for a clinical EHR.

4. **Specialty-specific data absent**: The vendor markets QSuite as "specialty-built" for orthopedics, urology, and oncology, yet no specialty-specific entities appear in the export. Only `OB Vitals` represents specialty content. If custom assessment forms, specialty workflows, or procedure-specific templates exist in the product, they are not represented in the export.

5. **Field descriptions add little value**: While 100% of 777 fields have descriptions, 68% are trivial reformattings of the field name. No value sets, no relationship documentation, no sample data. The data dictionary is structurally complete but informationally thin.

### Summary Stats

```
Classification:  Partial native export
Export format:   C-CDA XML + CSV + PDF + Word + Image (multi-format)
Model type:      Hybrid (native database CSV + standard C-CDA)
Entities:        32 (30 with field definitions)
Fields:          777
Descriptions:    100% have descriptions; 31.9% add information beyond the field name
Sample data:     No
Bulk export:     Yes (documented)
Domains covered: 12 of 19 applicable domains (5 partial, 2 not covered)
```

### Bottom Line

TRIARQ's QSuite EHI export is a genuine effort that goes meaningfully beyond a C-CDA repackaging — it includes native billing, insurance, and administrative data that most vendors omit. However, the absence of structured lab results, no specialty-specific clinical data (despite serving orthopedics/urology/oncology), and an encounter entity gap weaken it. A patient would get most of their clinical and billing data, but a developer trying to import it would struggle with the thin documentation (trivial descriptions, no value sets, no relationships, no sample data).
