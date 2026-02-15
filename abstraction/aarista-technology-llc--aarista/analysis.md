# EHI Export Analysis: Aarista Technology LLC

**Product**: Aarista v1.0
**Analysis date**: 2026-02-15
**CHPL ID**: 15.04.04.3168.Aari.01.00.1.230808 (CHPL #11329)

## 1. Product Context

Aarista is a certified EHR platform purpose-built for **post-acute and outpatient care**, primarily serving skilled nursing facilities (SNFs), long-term care facilities, and assisted living facilities. It is developed by Aarista Technology LLC, closely linked to Altea Healthcare. As of 2024, the platform served over 70,000 patients across 14 states.

The product combines clinical EHR functionality with an AI/ML analytics layer ("Aari"). Key capabilities relevant to export completeness include:

- **Clinical documentation**: Progress notes with smart templates for multiple specialties (wound care, psychiatry, cardiology, nephrology), voice-enabled dictation, customizable workflows
- **Practice management/billing**: Revenue cycle management with billing documentation, encounter/diagnosis coding, RVU tracking, compliance metrics
- **Care management**: Annual Wellness Visit (AWV) and Chronic Care Management (CCM) workflows, care coordination
- **Ordering/prescribing**: E-prescribing for controlled and non-controlled medications
- **Scheduling**: Smart Scheduler with drag-and-drop appointments
- **Telehealth & RPM**: Integrated virtual consultations, remote patient monitoring
- **Integrations**: Bidirectional data exchange with PCC, MatrixCare, Epic, Cerner, and others
- **Insurance/coverage**: Patient insurance management

The product holds a broad ONC certification covering (a)(1)–(a)(5), (a)(12), (a)(14), (b)(1), (b)(10), (b)(11), (c)(1), (e)(3), (g)(7)–(g)(10), and (h)(1). This is a comprehensive clinical certification.

**Baseline expectation**: A complete EHI export should cover demographics, encounters/clinical notes, problems, medications, allergies, immunizations, vitals, labs, procedures, insurance, billing/claims, care plans, and any specialty-specific assessments.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|----------|-------------|-----------------|
| `Aarista_EHI_Export.pdf` (183 KB, 8 pages) | EHI Export Data Dictionary — lists 7 data tables with 154 fields, field names and SQL Server data types. Created 2023-11-28 by Michael Mai. Retrieved from Wayback Machine; confirmed byte-identical to live version at both `alteahc.com` and `aarista.com` as of 2026-02-15. | **Primary artifact** — the only documentation of what the export contains |
| `b10-Real-World-Test-Plan-2025.pdf` (205 KB, 5 pages) | Real World Testing Plan for b(10), scanned document signed 10/15/2024. Describes test methodology for ambulatory and post-acute care settings. | **Supplementary** — confirms export tool exists and mentions format as "C-CDA files or FHIR APIs" |
| Mandatory Disclosures (`.docx`, live on aarista.com) | Disclosures letter listing product capabilities and fees. Notes FHIR API access requires "additional annual subscription per production instance." | **Minor** — confirms product scope, reveals FHIR API cost |

**Note on site accessibility**: The prior report stated both `alteahc.com` and `aarista.com` returned HTTP 403. As of 2026-02-15, both sites are live and returning HTTP 200. The EHI Export PDF is directly accessible at its registered URL. The PDF content is byte-identical to the Wayback Machine version (MD5: `7899ad9b157c7d2176bb22e4b7cf383e`), confirming the data dictionary has not been updated since its original creation in November 2023.

## 3. Export Mechanics

- **Format**: Unspecified. The data dictionary says only "Export data files are machine readable file formats." Data types are SQL Server column types (nvarchar, int, date, datetime, float, bit), suggesting a flat file (likely CSV/TSV) derived from database views. The Real World Test Plan references "C-CDA files or FHIR APIs" as possible formats, but the data dictionary structure does not align with either standard.
- **Mechanism**: The Real World Test Plan states "Our export tool enables users with the appropriate permissions to generate and download EHI exports" — this suggests a **UI-based export tool** (not vendor-assisted). The b(10) certification requires executability "at any time without developer assistance."
- **Single-patient**: Yes — 5 of the 7 tables are prefixed "Single Patient."
- **Bulk/population**: Yes — 2 tables are prefixed "Practice Patients" for facility-wide export. The test plan confirms "a population of patients within a specified date and time range."
- **Access constraints**: The Mandatory Disclosures document notes that use of the FHIR API requires "an additional annual subscription per production instance." It is unclear whether the b(10) export tool itself has separate costs.

## 4. Export Content: What's In It

The data dictionary defines **7 tables with 154 total fields**. Zero fields have descriptions beyond the field name itself. All fields have SQL Server data types documented. No value sets, no relationships/foreign keys, no sample data, and no machine-readable schema are provided.

### Verified field counts (from `analysis/parsed_data_dictionary.json`)

| Table | Fields | Required | Category |
|-------|--------|----------|----------|
| Single Patient - Patient Demographics | 28 | 4 | Single Patient |
| Single Patient - Patient Addresses | 10 | 7 | Single Patient |
| Single Patient - Patient Contacts | 20 | 13 | Single Patient |
| Single Patient - Patient Insurances | 24 | 12 | Single Patient |
| Single Patient - Patient Encounters – Clinical and Billing | 31 | 5 | Single Patient |
| Practice Patients - Patient Demographics and Billing Encounters | 15 | 7 | Practice (Bulk) |
| Practice Patients - Patient Demographics and Clinical Encounters | 25 | 1 | Practice (Bulk) |
| **Total** | **154** | **49** | |

### Table-by-table content

**Single Patient - Patient Demographics** (28 fields): Names, DOB, SSN, administrative gender, MBI#, Medicaid#, preferred/previous names, mother's maiden name, gender at birth, gender identity, sexual orientation, race, ethnicity, marital/employment/military status, language preferences, date of death, PCP info (NPI, name, phone). Several typos present: "Ethnithity" (Ethnicity), "Mother Mainder Name" (Mother Maiden Name).

**Single Patient - Patient Addresses** (10 fields): Address type, street address, city/state/zip, plus communication type (phone/email) with preferred indicator. Appears to combine physical addresses and communication endpoints in one table.

**Single Patient - Patient Contacts** (20 fields): Emergency contacts and guarantors with relationship, contact info, and full address. Includes flags for is_emergency_contact and is_guarantor.

**Single Patient - Patient Insurances** (24 fields): Insurance type, payer type/name, insurance name, group, policy number, effective date, prior authorization, policy holder demographics and full contact info.

**Single Patient - Patient Encounters – Clinical and Billing** (31 fields): The core encounter table. Repeats patient demographics (name, DOB, address, phone) per encounter. Clinical content is stored as **free-text blobs** in nvarchar(4000) fields: chief complaint ("Chief Comlaint" [sic]), HPI ("Historhy of Present Illness" [sic]), past surgical/medical/family/social history, immunizations, ROS, vital signs, physical exam, labs ("L:abs" [sic]), radiology, plan, disclaimer. Five fields are marked "multiple records" within single nvarchar fields (medications, problems, allergies, assessment, billing) — the serialization format for these is not documented.

**Practice Patients - Patient Demographics and Billing Encounters** (15 fields): Bulk billing export with TIN, NPI, MRN, patient name/DOB/gender, visit date, Medicaid#, encounter code, diagnosis code, modifiers, place of service, and primary/secondary/tertiary insurer names. Note: TIN is described as "9 digits- hardcoded for now."

**Practice Patients - Patient Demographics and Clinical Encounters** (25 fields): A **generic/EAV-style table** mixing all clinical data types into a single flat structure with columns: Name, Description, Code, Codesys, Category (constant string), Status, Textresult, Numresult, Units, plus various dates and medication-specific fields (strength, sig, dispense, refills). Four fields have "n/a" as their data type (Dispense Number, Sig Number, Ordering Provider NPI, Refill Times), suggesting they are not yet implemented.

### Key structural observations

1. **Free-text blobs dominate clinical data**: The single-patient encounter table stores most clinical information as unstructured nvarchar(4000) text rather than discrete, coded data elements. This means vital signs, labs, physical exam findings, etc. are not individually queryable or parseable without knowing the internal text format.

2. **Multi-record fields with unknown serialization**: Medications, problems, allergies, assessment, and billing are described as "multiple records" within single nvarchar fields. How records are delimited (pipe-separated? newline? JSON array?) is not documented.

3. **Redundant patient demographics**: Patient name, DOB, and address are repeated in the encounter table rather than linked via a foreign key. No relationships between tables are documented.

4. **Generic clinical table**: The Practice-level clinical encounters table uses an EAV (entity-attribute-value) pattern, mixing labs, medications, vitals, and other clinical items into one flat structure. The "Category" column presumably discriminates between data types, but valid category values are not documented.

5. **Several "n/a" fields**: Four fields in the practice clinical encounters table have "n/a" as their data type, suggesting incomplete implementation.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor's data dictionary organizes content into 7 tables spanning two modes: single-patient export (5 tables) and practice-wide export (2 tables).

**Demographics/administrative data (4 tables, 82 fields)**: This is the richest area. Patient demographics (28 fields) are reasonably thorough, including USCDI v1 demographic elements (gender identity, sexual orientation, race, ethnicity, language) as well as Medicare/Medicaid identifiers. Addresses, contacts, and insurance tables add substantial detail. Insurance coverage (24 fields) captures payer, policy, and policy holder information.

**Clinical encounter data (1 single-patient table, 31 fields)**: This table attempts to capture an entire encounter as a flat record. While it covers the major clinical sections of a progress note (CC, HPI, ROS, PE, assessment, plan, medications, problems, allergies, immunizations, vitals, labs, radiology, surgical/medical/family/social history), nearly everything is stored as free-text blobs. Only a few fields (progress notes type, DOS, provider, facility) are discrete. Billing codes are included as a "multiple records" field.

**Practice-level billing (1 table, 15 fields)**: A summary billing table with encounter/diagnosis codes, modifiers, place of service, and insurer names. Relatively thin — no charges, payments, adjustments, or claim status.

**Practice-level clinical (1 table, 25 fields)**: A generic table that attempts to capture all structured clinical data types (labs, medications, etc.) in a single EAV-style structure. Includes coded data elements (Code, Codesys, Category) but category values are undocumented.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|--------|----------|-----------------|--------------|
| Demographics | ✅ Covered | `Patient Demographics` (28 fields), `Patient Addresses` (10 fields), `Patient Contacts` (20 fields) | Thorough; includes USCDI demographics |
| Encounters / visits | ⚠️ Partial | `Patient Encounters – Clinical and Billing` has DOS, provider, facility, progress notes type | Encounter metadata is minimal; encounter is just a container for free-text note sections |
| Problems / conditions / diagnoses | ⚠️ Partial | "Problems List" field (nvarchar 270, multiple records) in encounters; "Diagnosis Code" in billing table; generic clinical table has Code/Codesys | Problems are free-text blobs in encounter table; structured codes only in bulk tables |
| Medications / prescriptions | ⚠️ Partial | "Medications" field (nvarchar 500, multiple records) in encounters; generic clinical table has medication-specific fields (strength, sig, dispense, refills) | Single-patient medications are free-text; bulk table has structured medication fields but 4 medication columns show "n/a" type — apparently not implemented |
| Allergies | ⚠️ Partial | "Allergies" field (nvarchar 500, multiple records) in encounters | Free-text blob only; no coded allergy data in single-patient export |
| Immunizations | ⚠️ Partial | "Immunizations" field (nvarchar 4000) in encounters | Free-text blob only |
| Vitals | ⚠️ Partial | "Vital Signs" field (nvarchar 4000) in encounters; possible in generic clinical table | Free-text blob in single-patient; may be structured in bulk clinical table via Category discriminator |
| Lab results | ⚠️ Partial | "L:abs" [sic] field (nvarchar 4000) in encounters; generic clinical table has Numresult, Units, Textresult | Free-text blob in single-patient; bulk table has structured results but undocumented categories |
| Imaging / diagnostic reports | ⚠️ Partial | "Radiology" field (nvarchar 4000) in encounters | Free-text blob only |
| Procedures | ⚠️ Partial | "Past Surgical History" (nvarchar 4000) in encounters; encounter/diagnosis codes in billing table | Surgical history is free-text; billing codes provide some procedure data |
| Clinical notes / documents | ✅ Covered | Full encounter note structure: CC, HPI, ROS, PE, assessment, plan, plus progress notes type | This is the core export — clinical notes are well-represented, though as free-text |
| Care plans / goals | ❌ Not covered | No care plan table or fields in export | Product is certified under (b)(11) for care plans; this is a gap |
| Orders / referrals | ❌ Not covered | No order or referral tables or fields | Product has e-prescribing; ordering data is missing |
| Insurance / coverage | ✅ Covered | `Patient Insurances` (24 fields) | Thorough; includes payer, policy, and holder details |
| Claims / billing | ⚠️ Partial | `Patient Encounters – Clinical and Billing` has "Billing" field; `Practice Patients – Billing Encounters` (15 fields) has encounter/diagnosis codes, modifiers, POS | Billing data exists but is thin — no charges, payments, adjustments, or claim lifecycle data despite product having RCM features |
| Payments | ❌ Not covered | No payment fields in any table | Product has revenue cycle management; payment data is a gap |
| Consents / directives | ❌ Not covered | No consent or advance directive fields | Unclear whether product stores these |
| Patient communications / portal messages | ❌ Not covered | No communication or portal tables | Unclear whether product has patient portal |
| Specialty-specific (post-acute care) | ❌ Not covered | No post-acute-specific assessments, wound care documentation, or CCM/AWV-specific data structures | Product emphasizes specialty templates (wound care, psychiatry, etc.) and AWV/CCM workflows; these may be captured in free-text encounter notes but are not separately identifiable |

**Coverage summary**: 3 of 15 applicable domains are adequately covered (demographics, clinical notes, insurance). 8 domains are partially covered (data present but as free-text blobs or minimal structure). 4 domains appear not covered at all (care plans, orders/referrals, payments, specialty-specific data).

## 6. Documentation Quality

The documentation quality is **low**. While a data dictionary exists (many vendors provide nothing), it has significant shortcomings:

**What's provided**:
- Field names (154 total across 7 tables)
- SQL Server data types with lengths
- Required field indicators (asterisks)

**What's missing**:
- **Field descriptions**: 0 of 154 fields have any description beyond the field name itself (0%)
- **Value sets / code systems**: No enumerated values for any coded field (e.g., valid values for "Administrative Gender," "Category," "Progress Notes Type," "Communication Type")
- **Relationships**: No foreign keys, join fields, or entity-relationship documentation between the 7 tables
- **Multi-record serialization**: Five fields are noted as "multiple records" but the delimiter/format is not specified
- **Export file format**: The actual output format (CSV, JSON, XML, delimiter, encoding) is never specified
- **Sample data**: None
- **Machine-readable schema**: No XSD, JSON Schema, DDL, or CSV header specification
- **Instructions**: No procedure for how to perform the export

**Editorial quality**: Multiple typos are present in field names: "Ethnithity" (Ethnicity), "Mother Mainder Name" (Mother Maiden Name), "Chief Comlaint" (Chief Complaint), "Historhy of Present Illness" (History of Present Illness), "L:abs" (Labs). This suggests minimal editorial review.

**Staleness**: The document was created 2023-11-28 (at certification time) and has not been updated since — the 2025 version hosted on aarista.com is byte-identical. Created in Microsoft Word for Microsoft 365.

**Could a developer import this data?** Not without significant reverse-engineering. They would lack: the file format, the delimiter for multi-valued fields, valid values for coded fields, how to join tables, and what the Category values mean in the generic clinical encounters table. The free-text clinical blobs would require parsing an unknown text format to extract structured clinical data.

## 7. Overall Assessment

### Classification

**Partial native export**

The export represents a native database projection (SQL Server types, flat tables) rather than a standard (C-CDA, FHIR), which is directionally correct for a b(10) export. However, it has significant structural and coverage weaknesses: clinical data is predominantly free-text blobs rather than discrete coded elements, billing data is thin despite the product having RCM capabilities, and several data domains the product stores (care plans, orders, payments, specialty assessments) are absent from the export.

### Key Findings

1. **Clinical data is mostly free-text blobs, not structured data.** The encounter table stores nearly all clinical content (vitals, labs, physical exam, etc.) as nvarchar(4000) text fields. While the data is technically "exported," a receiving system cannot parse or interpret it without reverse-engineering the text format. This undermines the practical utility of the export.

2. **Zero field descriptions out of 154 fields (0%).** The data dictionary provides only field names and SQL types — no definitions, no value sets, no code systems, no relationships. A developer cannot reliably interpret or import this data from the documentation alone.

3. **Export file format is never specified.** Despite being the core deliverable, the actual output format (CSV? JSON? XML? What delimiter? What encoding?) is never stated. The Real World Test Plan mentions "C-CDA files or FHIR APIs" but the data dictionary's flat SQL-typed tables are inconsistent with either standard.

4. **Several data domains the product stores are absent.** Care plans (certified under (b)(11)), e-prescribing orders, payment/financial data (despite RCM features), and specialty-specific assessments (wound care, AWV, CCM workflows) have no representation in the export.

5. **Documentation has not been updated since certification.** The 2023-11-28 PDF is byte-identical to the current version. Multiple typos in field names ("Ethnithity," "Chief Comlaint," "L:abs") suggest it was created hastily for certification and never revisited.

### Summary Stats

```
Classification:  Partial native export
Export format:   Unspecified ("machine readable file formats")
Model type:      Native database projection (SQL Server types)
Entities:        7
Fields:          154
Descriptions:    0% (0 of 154 fields have descriptions)
Sample data:     No
Bulk export:     Yes (practice-level tables)
Domains covered: 3 of 15 applicable domains adequately; 8 partially
```

### Bottom Line

Aarista's EHI export provides a minimal skeleton of its data model — 7 tables with 154 fields — but the heavy reliance on free-text blobs for clinical data, the complete absence of field descriptions, and the failure to specify the export file format make this export of limited practical utility. A patient or provider receiving this export would get demographic and insurance data in structured form, but clinical data would arrive as opaque text blocks that cannot be reliably parsed or imported into another system. The biggest gap is structural: even data that is technically "exported" is not usable without significant reverse-engineering effort.
