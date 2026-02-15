# EHI Export Analysis: Aarista Technology LLC

**Product**: Aarista v1.0
**Analysis date**: 2026-02-15
**CHPL IDs**: 15.04.04.3168.Aari.01.00.1.230808 (CHPL ID 11329)

## 1. Product Context

Aarista is a certified EHR platform purpose-built for **post-acute and outpatient care**, serving skilled nursing facilities (SNFs), long-term care facilities, and assisted living facilities. As of 2024, it served ~70,000 patients across 14 states. The company is closely linked to Altea Healthcare, a post-acute care provider services organization.

The platform combines clinical EHR functionality with an AI/ML analytics layer ("Aari"). Key data domains the product stores include:

- **Clinical documentation**: patient demographics, clinical notes (with specialty templates for wound care, psychiatry, cardiology, nephrology), problem lists, medications, allergies, immunizations, vitals, labs, radiology results, care plans
- **Practice management / billing**: revenue cycle management, billing documentation, coding trends, RVU tracking, encounter/diagnosis codes
- **Insurance/coverage**: payer information, policy details
- **Scheduling**: Smart Scheduler with drag-and-drop appointments
- **Care management**: Annual Wellness Visit (AWV) workflows, Chronic Care Management (CCM) workflows, care coordination
- **E-prescribing**: controlled and non-controlled medications
- **Telehealth/RPM**: integrated telemedicine, remote patient monitoring
- **AI analytics**: risk scores, condition alerts, population stratification

The product holds a broad ONC certification covering (a)(1)–(a)(5), (a)(12), (a)(14), (b)(1), (b)(10), (b)(11), (c)(1), (e)(3), (g)(7)–(g)(10), and (h)(1). This is a comprehensive clinical certification, not a narrow single-criterion module.

## 2. Artifacts Reviewed

| Artifact | Description | Informative? |
|---|---|---|
| `Aarista_EHI_Export.pdf` (183 KB, 8 pages) | EHI Export Data Dictionary — the only substantive export documentation. Defines 7 data tables with 154 fields. Created 2023-11-28 by Michael Mai in Microsoft Word. Retrieved from Wayback Machine (2024-08-09 snapshot) since both vendor domains (alteahc.com, aarista.com) return HTTP 403. | **Primary source** — this is the entire export documentation |
| `b10-Real-World-Test-Plan-2025.pdf` (205 KB, 5 pages) | Real World Testing Plan for b(10), signed 10/15/2024. Scanned document (from Xerox scanner). Describes testing approach for single-patient and population-level exports. Mentions "C-CDA files or FHIR APIs" as export format. | **Secondary** — useful for understanding export mechanics but provides no data-level detail |
| `product-research.md` | Prior research on vendor/product capabilities | Orientation only |
| `ehi-export-report.md` | Prior agent's analysis narrative | Orientation only; confirmed against primary artifacts |
| `chpl-metadata.json` | CHPL certification details | Verified CHPL ID, certification date, criteria list |

**Both vendor websites (alteahc.com and aarista.com) are currently inaccessible** (HTTP 403 on all paths as of 2026-02-14). The 2025 re-upload of the EHI Export PDF on aarista.com is byte-identical to the 2023 original, confirming no updates have been made.

## 3. Export Mechanics

- **Format**: Unspecified. The data dictionary says only "Export data files are machine readable file formats" with no further detail. Data types are SQL Server types (nvarchar, int, date, datetime, float, bit), suggesting flat file export (likely CSV) derived from database tables/views. The Real World Test Plan separately mentions "C-CDA files or FHIR APIs" as possible formats, which contradicts the data dictionary's flat-table structure.
- **Mechanism**: The data dictionary states "Customers can request to export individual patients or all patients for the practice." The RWT Plan states the export tool "enables users with the appropriate permissions to generate and download EHI exports." This suggests a UI-based export tool, but no screenshots, URLs, or step-by-step instructions are provided.
- **Single-patient**: Yes — 5 of the 7 tables are prefixed "Single Patient."
- **Bulk/practice-level**: Yes — 2 tables are prefixed "Practice Patients" for population-level exports.
- **Access constraints**: Unknown. No documentation on fees, permissions, or request process beyond the generic statements above.

## 4. Export Content: What's In It

The data dictionary defines **7 tables with 154 total fields**. No fields have descriptions beyond the field name itself. No value sets, no foreign keys, no relationships between tables, no sample data, and no export format specification are provided.

### Vendor's own content organization

The vendor organizes the export into two tiers: single-patient tables (5 tables) and practice-level tables (2 tables).

| Entity/Table | Fields | Described | Types | Required | Category (vendor's) |
|---|---|---|---|---|---|
| Single Patient - Patient Demographics | 28 | 0 | Yes (SQL Server) | 4 | Demographics |
| Single Patient - Patient Addresses | 10 | 0 | Yes | 7 | Demographics |
| Single Patient - Patient Contacts | 20 | 0 | Yes | 13 | Demographics |
| Single Patient - Patient Insurances | 24 | 0 | Yes | 12 | Insurance |
| Single Patient - Patient Encounters – Clinical and Billing | 31 | 0 | Yes | 5 | Clinical & Billing |
| Practice Patients - Patient Demographics and Billing Encounters | 16 | 0 | Yes | 8 | Practice Billing |
| Practice Patients - Patient Demographics and Clinical Encounters | 25 | 0 | Yes | 1 | Practice Clinical |
| **Totals** | **154** | **0** | — | **50** | — |

Source: `analysis/full-entity-inventory.json`, `analysis/parse_data_dictionary.py`

### Key structural observations

**Clinical encounter data is stored as free-text blobs.** The "Single Patient - Patient Encounters – Clinical and Billing" table stores most clinical content as `nvarchar(4000)` text fields — Chief Complaint, HPI, Review of Systems, Physical Exam, Vital Signs, Labs, Radiology, Plan are all free-text blobs up to 4,000 characters. This is essentially a note dump, not structured clinical data.

**Multi-valued fields are packed into single columns.** Medications (`nvarchar(500)`), Problems List (`nvarchar(270)`), Allergies (`nvarchar(500)`), Assessment (`nvarchar(270)`), and Billing (`nvarchar(270)`) are each marked "multiple records" but stored in single nvarchar fields. The delimiter/serialization format is undocumented.

**The practice clinical encounters table is a generic EAV-like structure.** It uses a single flat table with Name/Description/Code/Codesys/Category/Status columns to mix different clinical data types (labs, medications, etc.). The valid values for "Category" (the discriminator) are not documented.

**Several fields have "n/a" as the data type** in the Practice Clinical table: Dispense Number, Sig Number, Ordering Provider NPI, and Refill Times are listed with type "n/a", suggesting they are defined but not populated.

**Multiple typos** in field names suggest limited editorial review: "Mother Mainder Name" (Maiden), "Ethnithity" (Ethnicity), "Chief Comlaint" (Complaint), "Historhy of Present Illness" (History), "L:abs" (Labs).

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor organizes the export into three functional areas:

1. **Demographics** (3 tables, 58 fields): Patient demographics (28 fields), addresses/communication (10 fields), and emergency contacts/guarantors (20 fields). This is the richest area relative to typical EHR demographics — includes SSN, MBI, Medicaid#, gender identity, sexual orientation, race, ethnicity, multiple languages, military status, employment status, PCP info.

2. **Insurance** (1 table, 24 fields): Insurance/payer details including policy holder demographics. Reasonably thorough for payer data.

3. **Clinical & Billing Encounters** (3 tables, 72 fields total):
   - Single-patient encounters (31 fields) — a single denormalized table mixing clinical note content (as free-text blobs) with billing codes. Covers chief complaint, HPI, ROS, physical exam, assessment, plan, medications, problems, allergies, surgical/medical/family/social history, immunizations, vitals, labs, radiology, and a "Billing" field.
   - Practice billing encounters (16 fields) — encounter-level billing with TIN, NPI, MRN, encounter codes, diagnosis codes, modifiers, place of service, and insurer names.
   - Practice clinical encounters (25 fields) — generic EAV structure for coded clinical data (labs, medications, etc.) with dates, codes, and text results.

**The clinical encounter table is essentially a progress note dump** — it captures the narrative content of an encounter note but does not provide structured, coded clinical data at the single-patient level. The practice-level clinical encounters table does provide coded data (with Name, Code, Codesys fields) but only for bulk exports, and its structure conflates all clinical data types into one table.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | `Patient Demographics` (28 fields), `Patient Addresses` (10 fields), `Patient Contacts` (20 fields) | Thorough — includes USCDI v1 demographic elements plus SSN, MBI, military/employment status |
| Encounters / visits | ⚠️ Partial | `Patient Encounters – Clinical and Billing` has DOS, Facility, Provider, Progress Notes Type; Practice Billing has Visit Date, Encounter Code | Encounter metadata is minimal — no encounter IDs, no encounter status, no visit type taxonomy, no duration |
| Problems / conditions / diagnoses | ⚠️ Partial | `Problems List` field (nvarchar(270), multi-record blob); Practice Clinical has Category-based coded data; Practice Billing has Diagnosis Code | At single-patient level, problems are a text blob with no structure. Practice-level exports have coded data but undocumented Category values |
| Medications / prescriptions | ⚠️ Partial | `Medications` field (nvarchar(500) blob); Practice Clinical has Medication Strength, Sig, Refill Times | Single-patient level is a text blob. Practice-level has more structure but several medication fields are "n/a". Product does e-prescribing (certified criteria); structured Rx data appears absent |
| Allergies | ⚠️ Partial | `Allergies` field (nvarchar(500) blob); likely in Practice Clinical by Category | Same text blob issue. No reaction type, severity, or onset date at single-patient level |
| Immunizations | ⚠️ Partial | `Immunizations` field (nvarchar(4000) blob); likely in Practice Clinical | Text blob at single-patient level; may be coded at practice level |
| Vitals | ⚠️ Partial | `Vital Signs` field (nvarchar(4000) blob); Practice Clinical has Numresult/Units/Textresult | Text blob at single-patient level; structured at practice level via EAV table |
| Lab results | ⚠️ Partial | `L:abs` field (nvarchar(4000) blob); Practice Clinical has Code/Numresult/Units/Textresult | Same pattern — blob vs. EAV |
| Imaging / diagnostic reports | ⚠️ Partial | `Radiology` field (nvarchar(4000) blob) | Text blob only; no structured imaging data |
| Procedures | ⚠️ Partial | `Past Surgical History` field (nvarchar(4000) blob) | Only historical surgical procedures; no coded procedure records |
| Clinical notes / documents | ✅ Covered | Encounter table contains Chief Complaint, HPI, ROS, Physical Exam, Assessment, Plan (all free-text) | The encounter table is essentially a clinical note export. This is the core of the single-patient export. |
| Care plans / goals | ❌ Not covered | No care plan entity in data dictionary | Product is certified for (b)(11) care plan; this is a gap |
| Orders / referrals | ❌ Not covered | No order or referral entities | Product mentions care coordination and ordering; gap |
| Insurance / coverage | ✅ Covered | `Patient Insurances` (24 fields); Practice Billing has insurer names | Solid payer coverage including policy holder details |
| Claims / billing | ⚠️ Partial | Practice Billing has Encounter Code, Diagnosis Code, Modifiers, Place of Service; Encounter table has `Billing` text blob | Basic billing encounter data present. No claim status, amounts, payments, or adjudication data. Product has "revenue cycle management" features |
| Payments | ❌ Not covered | No payment entities | Product mentions RCM with billing documentation; if it tracks payments, this is a gap |
| Consents / directives | ❌ Not covered | No consent or advance directive entities | Unclear if product stores these |
| Patient communications / portal messages | ❌ Not covered | No portal or messaging entities | Unclear if product has patient portal |
| Specialty-specific (post-acute care) | ❌ Not covered | No specialty assessment entities (wound care, psychiatry, cardiology, nephrology) | Product advertises specialty templates for wound care, psychiatry, cardiology, nephrology. If these generate structured data beyond the generic encounter note, the export misses it |
| Family history | ⚠️ Partial | `Family History` field (nvarchar(4000) blob); certified (a)(12) | Text blob — no structured family health history despite (a)(12) certification |
| Social history | ⚠️ Partial | `Social History` field (nvarchar(4000) blob) | Text blob only |
| Implantable devices | ❌ Not covered | No implantable device entity | Product is certified (a)(14); this is a gap |

## 6. Documentation Quality

**Rating: Poor.**

The documentation consists of a single 8-page PDF with field names and SQL Server data types in tabular format. It provides:

- ✅ Field names (mostly self-descriptive, with typos)
- ✅ SQL Server data types with lengths
- ✅ Required field indicators (asterisks)

It lacks:

- ❌ **Field descriptions or definitions** — 0 of 154 fields have any description
- ❌ **Value sets** — no valid values documented for any coded field (e.g., Administrative Gender, Progress Notes Type, Category, Status)
- ❌ **Relationships** — no foreign keys, join fields, or entity-relationship documentation between the 7 tables
- ❌ **Export format specification** — no information on file format (CSV? JSON? XML?), delimiters, encodings, or how multi-record fields are serialized
- ❌ **Sample data** — no example exports provided
- ❌ **Machine-readable schemas** — no XSD, JSON Schema, DDL, or CSV header specifications
- ❌ **Instructions** — no step-by-step guide for performing the export
- ❌ **Versioning** — document created 2023-11-28, byte-identical 2025 re-upload confirms zero updates

A developer receiving this documentation alone could not build an import. The export format is unknown, multi-record field serialization is undocumented, the Category discriminator values in the practice clinical table are unstated, and the relationship between single-patient tables and practice-level tables is undefined.

The 5 typos in field names (`Mother Mainder Name`, `Ethnithity`, `Chief Comlaint`, `Historhy of Present Illness`, `L:abs`) and the TIN field type described as "9 digits- hardcoded for now" suggest this was a quickly-produced certification artifact that received minimal review.

## 7. Overall Assessment

### Classification

**Partial native export.** The data dictionary describes what appears to be a projection of the vendor's SQL Server database tables — not C-CDA, not FHIR resources, but flat tables with SQL Server data types. However, it covers only 7 tables (far fewer than what a product of this complexity would store internally), and the clinical content is largely free-text blobs rather than structured, coded data. The documentation is thin enough that it borders on "minimal/stub" territory.

The Real World Test Plan's mention of "C-CDA files or FHIR APIs" as the export format introduces confusion — the data dictionary clearly describes a native flat-table export, not a standards-based one. This may indicate the vendor has not yet settled on an approach, or the RWT plan was written independently from the actual implementation.

### Key Findings

1. **Only 7 tables with 154 fields, and zero field descriptions.** For a product with clinical documentation, billing/RCM, e-prescribing, scheduling, telehealth, RPM, and specialty templates, 7 tables is strikingly thin. None of the 154 fields have any description beyond the field name.

2. **Clinical data is largely free-text blobs.** The single-patient encounter table stores clinical content (HPI, ROS, Physical Exam, Vitals, Labs, etc.) as `nvarchar(4000)` text fields — these are essentially note sections dumped into columns, not structured clinical data. This means the export captures narratives but not discrete, coded clinical observations.

3. **Multiple certified capabilities have no export representation.** Care plans (b)(11), implantable devices (a)(14), family health history (a)(12) as structured data, and transitions of care (b)(1) are all certified but absent from the export data dictionary.

4. **Specialty-specific data is absent.** The product advertises specialty templates for wound care, psychiatry, cardiology, and nephrology, but no specialty assessment entities appear in the export — these are presumably captured only as generic encounter note text.

5. **Documentation is a certification artifact, not a living document.** Created November 2023 at certification time, never updated (byte-identical 2025 re-upload), with typos, a "hardcoded for now" TIN field, and no format specification. Both vendor websites are currently returning HTTP 403.

### Summary Stats

```
Classification:  Partial native export
Export format:   Unspecified ("machine readable file formats"); SQL Server types suggest flat files
Model type:      Native database (flat tables with SQL Server data types)
Entities:        7
Fields:          154
Descriptions:    0% (0 of 154 fields have descriptions)
Sample data:     No
Bulk export:     Yes (practice-level tables)
Domains covered: 4 of 16 applicable domains fully; 9 partial; 3 not covered
```

### Bottom Line

This is a minimal export effort that captures basic demographics, insurance, and clinical encounter notes — but the clinical content is mostly free-text blobs rather than structured data, and entire product capabilities (care plans, specialty assessments, e-prescribing records, implantable devices) have no export representation. A patient or provider receiving this export would get narrative encounter notes and billing codes, but would lose structured clinical data, specialty assessments, and care management information. The single biggest gap is the lack of structured clinical data: the product almost certainly stores coded medications, problems, and labs internally, but the single-patient export flattens these into text blobs.
