# EHI Export Analysis: Aarista Technology LLC

**Product**: Aarista EHR System
**Analysis date**: 2026-02-15
**CHPL ID**: 15.04.04.3168.Aari.01.00.1.230808

## 1. Product Context

Aarista is a certified EHR platform purpose-built for **post-acute and outpatient care**, serving skilled nursing facilities (SNFs), long-term care facilities, and assisted living facilities. As of 2024, Aarista served 70,000+ patients across 14 states. The company is closely linked to Altea Healthcare, a post-acute care provider services organization.

The platform stores and manages:

- **Clinical documentation**: Patient profiles, clinical notes (with specialty-specific templates for wound care, psychiatry, cardiology, nephrology), voice-dictated notes, H&P, progress notes, discharge summaries
- **Medications**: Medication lists, e-prescribing for controlled and non-controlled substances
- **Problems, allergies, immunizations, vitals, labs**: Standard clinical data certified under (a)(1)–(a)(5)
- **Billing/RCM**: Revenue cycle management with billing documentation, coding, compliance tracking, RVU data
- **Insurance/coverage**: Patient insurance and payer information
- **Care plans**: Certified under (b)(11)
- **Encounters**: Visit records across in-person and telehealth modalities
- **Scheduling**: Smart Scheduler with drag-and-drop appointment management
- **Care management**: AWV workflows, Chronic Care Management workflows
- **Remote monitoring**: Vital signs and symptom data from RPM devices
- **AI/ML analytics**: Risk predictions, condition alerts, population risk stratification ("Aari" neural network)
- **Family health history**: Certified (a)(12)
- **Implantable device list**: Certified (a)(14)
- **Transitions of care**: C-CDA documents certified under (b)(1)

This establishes the baseline: an EHI export should cover clinical documentation, medications, problems, allergies, immunizations, vitals, labs, insurance/coverage, billing/claims, care plans, and specialty-specific clinical data.

## 2. Artifacts Reviewed

| # | Artifact | Description | Informativeness |
|---|----------|-------------|-----------------|
| 1 | `Aarista_EHI_Export.pdf` (183 KB, 8 pages) | EHI Export Data Dictionary — the primary and only EHI export documentation. Lists 7 data tables with 154 fields total. Field names and SQL Server data types only; no field descriptions, no value sets, no relationships, no sample data. Created 2023-11-28 by Michael Mai in Microsoft Word. Retrieved from Wayback Machine (original URL returns HTTP 403). | **Most informative** — the core artifact defining export content |
| 2 | `b10-Real-World-Test-Plan-2025.pdf` (205 KB, 5 pages) | Real World Testing Plan 2025 for §170.315(b)(10). Scanned document (no extractable text), signed 10/15/2024. Describes test methodology for single-patient and population-level exports in ambulatory and post-acute settings. Mentions export format as "C-CDA files or FHIR APIs." | **Moderately informative** — confirms export mechanism and care settings, but contradicts data dictionary format |

**Note**: Both vendor domains (alteahc.com, aarista.com) return HTTP 403 as of the collection date (2026-02-14). All artifacts were retrieved via Wayback Machine. The 2025 re-upload of the data dictionary on aarista.com was byte-identical to the November 2023 original, confirming the documentation has not been updated since initial certification.

## 3. Export Mechanics

- **Format**: Unspecified. The data dictionary states only "Export data files are machine readable file formats" without naming a specific format (CSV, JSON, XML, etc.). Data types are SQL Server column types (nvarchar, int, date, datetime, float, bit), suggesting flat-file exports derived from database tables or views. Confusingly, the Real World Test Plan (p.4) mentions "C-CDA files or FHIR APIs" as the export format — which contradicts the data dictionary's SQL-native table structure.
- **Mechanism**: The data dictionary states "Customers can request to export individual patients or all patients for the practice." The Real World Test Plan (p.4) states: "Our export tool enables users with the appropriate permissions to generate and download EHI exports for a single patient or a population of patients within a specified date and time range." This suggests a UI-based export tool accessible to authorized users.
- **Single-patient vs bulk**: Both supported. The data dictionary defines separate table structures for single-patient (5 tables) and practice-wide/population (2 tables) exports.
- **Access constraints**: The test plan references "appropriate permissions" but provides no further detail. No mention of fees.
- **Developer assistance**: The test plan certifies under §170.315(b)(10)(i)(B) — "Execute this capability at any time the user chooses without developer assistance."

## 4. Export Content: What's In It

The data dictionary defines **7 tables with 154 total fields**. Zero fields have descriptions beyond their column name. All 154 fields have SQL Server data types. No value sets, no relationships/foreign keys, no sample data are provided.

### Vendor's own content organization

The tables split into two scopes: **Single Patient** (5 tables, per-patient detail) and **Practice Patients** (2 tables, population-level summaries).

| Entity/Table | Fields | Described | Types | Category |
|---|---|---|---|---|
| Single Patient - Patient Demographics | 28 | 0 | Yes | Demographics |
| Single Patient - Patient Addresses | 10 | 0 | Yes | Demographics |
| Single Patient - Patient Contacts | 20 | 0 | Yes | Demographics |
| Single Patient - Patient Insurances | 24 | 0 | Yes | Insurance |
| Single Patient - Patient Encounters – Clinical and Billing | 31 | 0 | Yes | Clinical & Billing |
| Practice Patients - Patient Demographics and Billing Encounters | 16 | 0 | Yes | Billing |
| Practice Patients - Patient Demographics and Clinical Encounters | 25 | 0 | Yes | Clinical |

**Full inventory**: See `analysis/full-entity-inventory.json` for complete field-level detail.

### Key structural observations

1. **Clinical data is stored as free-text blobs**: The single-patient encounter table stores most clinical content as nvarchar(4000) text blobs — Chief Complaint, HPI, Review of Systems, Physical Exam, Vitals, Labs, Radiology, Surgical/Medical/Family/Social History, Plan, and Immunizations are all unstructured text fields. This means clinical data is narrative prose, not structured/coded data.

2. **Multi-valued fields packed into single columns**: Medications (nvarchar(500)), Problems List (nvarchar(270)), Allergies (nvarchar(500)), Assessment (nvarchar(270)), and Billing (nvarchar(270)) are annotated as "multiple records" — multiple items packed into a single database field. No documentation explains the delimiter or serialization format.

3. **Practice-level clinical table uses a generic EAV structure**: The "Practice Patients - Clinical Encounters" table uses a Name/Description/Code/Codesys/Category/Status pattern — an entity-attribute-value (EAV) design that mixes different clinical data types (labs, medications, problems, etc.) distinguished only by a "Category" column described as "constant string." The valid category values are not documented.

4. **Practice-level billing table is flat and minimal**: 16 fields covering encounter codes, diagnosis codes, modifiers, place of service, and insurer names — basic claims-level data but no charges, payments, adjustments, or financial detail.

5. **No relationships documented**: There are no foreign keys, join columns, or entity relationship documentation. It's unclear how single-patient tables link to each other (e.g., how encounters relate to demographics beyond repeating patient name/DOB in each table).

6. **Typos in field names**: 5 typos identified: "Ethnithity" (Ethnicity), "Mother Mainder Name" (Mother Maiden Name), "Chief Comlaint" (Chief Complaint), "Historhy of Present Illness" (History of Present Illness), "L:abs" (Labs). This suggests minimal editorial review.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The export organizes data into three functional areas:

**Demographics (3 tables, 58 fields)**: The richest area. Patient demographics includes comprehensive identity data (SSN, MBI#, Medicaid#, gender identity, sexual orientation, race, ethnicity, language), PCP information, and military/employment status. Addresses and contacts are separate tables with their own detail. This is genuinely thorough for patient identity.

**Insurance (1 table, 24 fields)**: Insurance coverage with payer details, policy information, and policy holder demographics/contact info. Reasonable depth for coverage data.

**Clinical & Billing Encounters (3 tables, 72 fields)**: This is where the export is weakest structurally despite having the most fields. The single-patient encounter table (31 fields) stores nearly all clinical content as unstructured text blobs — a complete encounter note flattened into one row with text fields for each note section. The practice-level tables provide a more structured (but generic) view of the same data.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | `Patient Demographics` (28 fields), `Patient Addresses` (10 fields), `Patient Contacts` (20 fields) — comprehensive identity, contact, and social data | Thorough; includes SSN, MBI, Medicaid#, gender identity, sexual orientation, race, ethnicity, language |
| Encounters / visits | ⚠️ Partial | Encounter data present in `Patient Encounters – Clinical and Billing` (31 fields) with DOS, Provider, Facility, Progress Notes Type | Encounter metadata is minimal (date, provider, facility, note type); no encounter ID, no encounter status, no visit type taxonomy |
| Problems / conditions / diagnoses | ⚠️ Partial | `Problems List` field (nvarchar(270), "multiple records") in encounters; Diagnosis Code in billing table; Category-based rows in practice clinical table | Problems exist but are packed into a single text field in encounter records; no standalone problem list entity with onset dates, status, etc. |
| Medications / prescriptions | ⚠️ Partial | `Medications` field (nvarchar(500), "multiple records") in encounters; practice clinical table has Medication Strength, Strength Units, Sig, Sig Freq, Refill Times fields | Medications in single-patient export are a text blob; practice-level table has more structure but the product has e-prescribing — no prescription/dispense records are apparent |
| Allergies | ⚠️ Partial | `Allergies` field (nvarchar(500), "multiple records") in encounters | Packed into a single text field; no structured allergy entity with reaction type, severity, onset |
| Immunizations | ⚠️ Partial | `Immunizations` field (nvarchar(4000)) in encounters | Free-text blob; no structured immunization records with vaccine codes, dates, lot numbers |
| Vitals | ⚠️ Partial | `Vital Signs` field (nvarchar(4000)) in encounters; practice clinical table has Numresult/Units fields that could hold vitals | Free-text blob in single-patient; may be structured in practice-level EAV table but category values undocumented |
| Lab results | ⚠️ Partial | `L:abs` [sic] field (nvarchar(4000)) in encounters; practice clinical table has Code/Codesys/Textresult/Numresult/Units | Free-text in single-patient; more structured in practice-level table with result fields |
| Imaging / diagnostic reports | ⚠️ Partial | `Radiology` field (nvarchar(4000)) in encounters | Free-text blob only; no structured imaging data |
| Procedures | ⚠️ Partial | `Past Surgical History` field (nvarchar(4000)) in encounters; Encounter Code/Diagnosis Code in billing table | Surgical history is narrative text; procedure codes appear only in the billing encounters table |
| Clinical notes / documents | ⚠️ Partial | Multiple nvarchar(4000) fields in encounter table: Chief Complaint, HPI, ROS, Physical Exam, Assessment, Plan, etc. | Note content is present but as raw text blobs — the single-patient encounter table is essentially a flattened progress note. No document metadata, no attachments |
| Care plans / goals | ❌ Not covered | No care plan entity in any export table | Product is certified under (b)(11) care plan; **significant gap** |
| Orders / referrals | ❌ Not covered | No order or referral entities | Product supports ordering/e-prescribing; gap for structured order data |
| Insurance / coverage | ✅ Covered | `Patient Insurances` (24 fields) with payer type, insurance name, policy details, policy holder info | Thorough coverage of insurance/enrollment data |
| Claims / billing | ⚠️ Partial | `Practice Patients - Billing Encounters` (16 fields) with encounter codes, diagnosis codes, modifiers, place of service, insurer names; `Billing` field in encounter table | Basic claims data present but no charges, payments, adjustments, or detailed financial records despite the product advertising revenue cycle management |
| Payments | ❌ Not covered | No payment entities | Product has RCM features; gap if payment data is stored |
| Consents / directives | ❌ Not covered | No consent or advance directive entities | Unclear if product stores these |
| Patient communications / portal messages | ❌ Not covered | No communication or messaging entities | Product has a patient-facing mobile app; potential gap |
| Specialty-specific (post-acute care) | ❌ Not covered | No specialty-specific entities for wound care, chronic care management, post-acute assessments | Product advertises specialty templates for wound care, psychiatry, cardiology, nephrology, plus AWV and CCM workflows — **significant gap** |
| Family health history | ⚠️ Partial | `Family History` field (nvarchar(4000)) in encounters | Free-text blob; certified under (a)(12) but no structured family history entity |
| Implantable device list | ❌ Not covered | No implantable device entity | Certified under (a)(14); gap |

## 6. Documentation Quality

**Overall: Low.** The documentation is a bare-minimum data dictionary that would not enable a developer to build an import system.

**What's provided**:
- Field names (154 total, somewhat self-descriptive despite typos)
- SQL Server data types for every field
- Required field indicators (asterisks)

**What's missing**:
- **Zero field descriptions**: Not a single field has a description beyond its column name. Fields like "Progress Notes Type," "Category," "Relation Reason," and "Place of Service" are unexplained.
- **No value sets**: Fields like Administrative Gender, Race, Ethnicity, Marital Status, Employment Status, Military Status, Insurance Type, Payer Type, Progress Notes Type, and Category have no documented allowed values.
- **No relationships**: No foreign keys, no join documentation, no entity-relationship diagram. It is impossible to determine how the 7 tables relate to each other.
- **No export format specification**: The actual file format (CSV, JSON, XML, delimiter, encoding) is never stated.
- **No sample data**: No example export files are provided.
- **No machine-readable schema**: No XSD, JSON Schema, DDL, or similar artifact.
- **No multi-record serialization format**: Five fields are annotated as "multiple records" but the delimiter/format for packing multiple records into a single nvarchar field is undocumented.
- **No export instructions**: No description of how to initiate, configure, or download an export.

**Staleness**: The document was created 2023-11-28 at certification time and has not been updated — the 2025 re-upload is byte-identical. The documentation predates the Real World Test Plan (dated 2024-10-15) and does not reflect any changes or improvements since certification.

**Could a developer use this?** No. A developer receiving this export would need to guess the file format, reverse-engineer the multi-record delimiter, discover the valid values for coded fields, and figure out table relationships — all without sample data.

## 7. Overall Assessment

### Classification

**Partial native export**: The data dictionary describes what appears to be a native SQL Server database projection (7 tables with SQL column types). It covers demographics, insurance, and encounters, but with significant coverage gaps (missing care plans, orders, specialty data, implantable devices) and critically thin documentation (no descriptions, no value sets, no relationships, no format specification). Clinical data is largely stored as unstructured text blobs rather than structured/coded data.

### Key Findings

1. **7 tables, 154 fields, zero descriptions**: The data dictionary provides field names and SQL types but nothing else. No field has a description, no value set is documented, no relationship is specified. This is the minimum viable documentation for certification compliance. (Source: `Aarista_EHI_Export.pdf`, all 8 pages)

2. **Clinical data is unstructured text**: The core encounter table stores clinical content (HPI, ROS, vitals, labs, radiology, exam, etc.) as nvarchar(4000) free-text blobs. Medications, problems, allergies, and billing are packed as "multiple records" into single nvarchar fields with no documented delimiter. This makes the export technically "machine-readable" but practically unusable for structured data exchange. (Source: `Aarista_EHI_Export.pdf`, pp. 5–6)

3. **Contradictory format claims**: The data dictionary describes SQL Server table exports, while the Real World Test Plan (p. 4) says exports will be "in the specified computable format (e.g., C-CDA files or FHIR APIs)." These are fundamentally different approaches and it's unclear which actually describes the implemented export. (Source: `b10-Real-World-Test-Plan-2025.pdf`, p. 4)

4. **Significant domain gaps**: Care plans (certified (b)(11)), implantable devices (certified (a)(14)), orders/referrals, specialty-specific clinical data (wound care, psychiatry, CCM, AWV), and payment/financial data are entirely absent from the export despite being core product features. (Source: comparison of `Aarista_EHI_Export.pdf` against product research)

5. **Documentation is stale and unmaintained**: Created November 2023 at certification time, byte-identical when re-uploaded in 2025, and hosted on domains that now return HTTP 403. Five typos in field names suggest minimal review. (Source: `files.json`, PDF metadata)

### Summary Stats

```
Classification:  Partial native export
Export format:   Unspecified ("machine readable file formats"); SQL Server types suggest flat files
Model type:      Native database projection (7 tables, SQL column types)
Entities:        7
Fields:          154
Descriptions:    0% (0 of 154 fields have descriptions)
Sample data:     No
Bulk export:     Yes (single-patient and practice-wide)
Domains covered: 3 of 15 fully; 10 of 15 partially; 2 N/A
```

### Bottom Line

A patient or provider would receive a structurally thin export — 7 tables with basic demographics, insurance, and encounter data, but with clinical content stored as unstructured text blobs that would be difficult to parse or import into another system. The biggest gap is the absence of entire data domains the product stores (care plans, orders, specialty assessments, structured medications, implantable devices) and the complete lack of documentation needed to actually use the export (no format specification, no value sets, no relationships, no sample data). This export appears to be a certification checkbox rather than a genuine effort to enable data portability.
