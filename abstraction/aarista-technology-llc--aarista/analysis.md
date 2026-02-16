# EHI Export Analysis: Aarista Technology LLC

**Product**: Aarista EHR System v1.0
**Analysis date**: 2026-02-16
**CHPL IDs**: 15.04.04.3168.Aari.01.00.1.230808 (CHPL ID 11329)

## 1. Product Context

Aarista is a certified EHR platform purpose-built for **post-acute and outpatient care**, targeting skilled nursing facilities (SNFs), long-term care facilities, and assisted living facilities. It serves 70,000+ patients across 14 states (as of August 2024). The developer, Aarista Technology LLC, is closely linked to Altea Healthcare, a post-acute care provider services organization.

**Key capabilities relevant to EHI export completeness:**

- **Clinical documentation**: Patient profiles, clinical notes with customizable smart templates (wound care, psychiatry, cardiology, nephrology), voice-enabled dictation ("Smart Scribe"), AI-enhanced documentation
- **Practice management / billing**: Revenue cycle management, billing documentation, compliance tracking, RVU tracking, coding trends
- **Care management**: Annual Wellness Visit (AWV) workflows, Chronic Care Management (CCM) workflows, care coordination tracking
- **Ordering & prescribing**: E-prescribing for controlled and non-controlled medications
- **Telehealth & RPM**: Integrated telemedicine, remote patient monitoring for vital signs
- **Scheduling**: Smart Scheduler with drag-and-drop appointments
- **AI/analytics**: "Aari" neural network for risk prediction, patient population risk stratification, real-time condition alerts
- **Integrations**: Bidirectional EHR integration with PCC, MatrixCare, Epic, Cerner, and others

The product holds a broad ONC certification covering (a)(1)–(a)(5), (a)(12), (a)(14), (b)(1), (b)(10), (b)(11), (c)(1), (e)(3), (g)(7)–(g)(10), and (h)(1). Certified 2023-08-08.

## 2. Artifacts Reviewed

| Artifact | Description | Size | Informativeness |
|---|---|---|---|
| `Aarista_EHI_Export.pdf` | Data Dictionary for Aarista EHI Export — 8-page PDF listing 7 data tables with field names and SQL Server data types. Created 2023-11-28 by Michael Mai. Retrieved from Wayback Machine (original URL returns 403). | 183 KB, 8 pages | **Primary artifact** — the only EHI export documentation. Contains all table/field definitions. |
| `b10-Real-World-Test-Plan-2025.pdf` | Real World Testing Plan 2025 for (b)(10) — 5-page scanned PDF describing test methodology, care settings, expected outcomes. Signed by Michael Mai on 10/15/2024. | 205 KB, 5 pages | **Secondary** — confirms export exists for single-patient and population-level, mentions "C-CDA files or FHIR APIs" as format but contradicts the data dictionary structure. |

Both artifacts were retrieved from the Wayback Machine since both vendor domains (alteahc.com, aarista.com) return HTTP 403 on all paths as of the collection date.

No sample data files, JSON schemas, machine-readable specifications, or additional documentation were available.

## 3. Export Mechanics

- **Format**: Unspecified. The data dictionary states only "Export data files are machine readable file formats" without naming the actual format. The data types are SQL Server column types (nvarchar, int, date, datetime, float, bit), suggesting flat files (likely CSV/TSV) derived from database tables or views. The RWT plan separately mentions "C-CDA files or FHIR APIs" but the data dictionary's structure is neither C-CDA nor FHIR — it describes flat, denormalized tables.
- **Mechanism**: The data dictionary overview states "Customers can request to export individual patients or all patients for the practice." The RWT plan states the export tool "enables users with the appropriate permissions to generate and download EHI exports for a single patient or a population of patients within a specified date and time range." This implies a UI-based export initiated by the customer.
- **Single-patient**: Yes — Tables 1–5 are explicitly prefixed "Single Patient."
- **Bulk export**: Yes — Tables 6–7 are prefixed "Practice Patients" and cover population-level export.
- **Access constraints**: The RWT plan mentions "appropriate permissions" are required. No fees mentioned.
- **Developer assistance**: The RWT plan explicitly states the capability can be "execute[d] at any time without developer assistance" per §170.315(b)(10)(i)(B).

## 4. Export Content: What's In It

### Data Dictionary Overview

The data dictionary defines **7 tables** with a total of **154 fields**. Zero fields have descriptions — only field names and SQL Server data types are provided. No value sets, foreign keys, relationships, or sample data are documented.

Source: `Aarista_EHI_Export.pdf` (8 pages), parsed via `analysis/parse_data_dictionary.py` → `analysis/full-entity-inventory.json`

### Vendor's own content organization

The vendor organizes the export into two scopes: **Single Patient** (5 tables, 113 fields) and **Practice Patients** (2 tables, 41 fields).

| Table Name | Fields | Required | Multi-valued | Scope | Category |
|---|---|---|---|---|---|
| Single Patient - Patient Demographics | 28 | 4 | 0 | Single patient | Demographics |
| Single Patient - Patient Addresses | 10 | 7 | 0 | Single patient | Demographics |
| Single Patient - Patient Contacts | 20 | 13 | 0 | Single patient | Demographics |
| Single Patient - Patient Insurances | 24 | 12 | 0 | Single patient | Insurance |
| Single Patient - Patient Encounters – Clinical and Billing | 31 | 5 | 5 | Single patient | Clinical / Billing |
| Practice Patients - Patient Demographics and Billing Encounters | 16 | 8 | 0 | Practice-wide | Billing |
| Practice Patients - Patient Demographics and Clinical Encounters | 25 | 1 | 0 | Practice-wide | Clinical |
| **Totals** | **154** | **50** | **5** | | |

### Key structural observations

**Encounters table (31 fields)**: This is the core clinical content table, but it stores most clinical data as **free-text blobs** in nvarchar(4000) fields. Chief Complaint, HPI, Physical Exam, Review of Systems, Vital Signs, Labs, Radiology, and Plan are all single text fields. Five fields (Medications, Problems List, Allergies, Assessment, Billing) are annotated as "multiple records" within nvarchar fields, but no serialization format is documented.

**Practice Clinical table (25 fields)**: Uses a **generic EAV-like structure** with Name, Description, Code, Codesys, Category, Status columns. The "Category" field is listed as "constant string" type, implying it discriminates between different clinical data types (labs, medications, problems, etc.) that are all stored in the same flat table. This is more structured than the encounters table but mixes heterogeneous data types without documenting the Category values.

**Notable field-level issues** (typos preserved from source):
- "Mother Mainder Name" (should be Mother Maiden Name)
- "Ethnithity" (should be Ethnicity)
- "Chief Comlaint" (should be Chief Complaint)
- "Historhy of Present Illness" (should be History of Present Illness)
- "L:abs" (should be Labs)

**Fields marked "n/a"**: In the Practice Clinical table, 4 fields (Dispense Number, Sig Number, Ordering Provider NPI, Refill Times) have data type "n/a" — suggesting they are defined in the schema but not yet implemented.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor's export covers two main areas:

**Demographics and administrative data** (4 tables, 82 fields): Comprehensive patient demographics including USCDI-relevant fields (race, ethnicity, gender identity, sexual orientation, preferred language). Addresses, contacts (emergency and guarantor), and insurance details with policy holder information. This is the strongest area of the export.

**Clinical encounter data** (2 tables, 56 fields for single-patient encounters + practice clinical): The single-patient encounters table captures the full clinical note structure (CC, HPI, ROS, PE, assessment, plan) but as free-text blobs. The practice-level clinical table provides a more structured representation with code, code system, and category fields, plus medication-specific columns (strength, sig, dispense, refills).

**Billing data** (encounter-level and practice-level): The encounters table includes a "Billing" multi-record field. The practice billing table adds TIN, NPI, encounter codes, diagnosis codes, modifiers, place of service, and insurer names. This is a thin but present billing representation.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | `Patient Demographics` (28 fields), `Patient Addresses` (10 fields), `Patient Contacts` (20 fields) — name, DOB, SSN, MBI, Medicaid#, race, ethnicity, gender identity, sexual orientation, language, PCP | Thorough; includes USCDI v1 elements |
| Encounters / visits | ✅ Covered | `Patient Encounters – Clinical and Billing` (31 fields) — DOS, facility, provider, progress notes type | Present but thin on structured encounter metadata |
| Problems / conditions / diagnoses | ⚠️ Partial | "Problems List" field (nvarchar(270), multi-record) in encounters; "Category" discriminator in practice clinical table; Diagnosis Code in practice billing | Present but as free-text blobs in encounters; somewhat structured in practice clinical table. No standalone problems table. |
| Medications / prescriptions | ⚠️ Partial | "Medications" field (nvarchar(500), multi-record) in encounters; medication-specific columns in practice clinical table (Strength, Sig, Dispense, Refills) | Product has e-prescribing capability. The practice clinical table has medication-specific fields, but 4 of them are "n/a" (not implemented). No standalone prescription/dispensing table. |
| Allergies | ⚠️ Partial | "Allergies" field (nvarchar(500), multi-record) in encounters | Free-text blob only; no structured allergy data |
| Immunizations | ⚠️ Partial | "Immunizations" field (nvarchar(4000)) in encounters | Free-text blob only |
| Vitals | ⚠️ Partial | "Vital Signs" field (nvarchar(4000)) in encounters; Numresult/Units in practice clinical | Free-text in encounters; may be more structured in practice clinical table via Category discriminator |
| Lab results | ⚠️ Partial | "L:abs" field (nvarchar(4000)) in encounters; Textresult/Numresult/Units in practice clinical | Free-text blob in encounters; structured result fields exist in practice clinical table |
| Imaging / diagnostic reports | ⚠️ Partial | "Radiology" field (nvarchar(4000)) in encounters | Free-text blob only |
| Procedures | ⚠️ Partial | "Past Surgical History" field (nvarchar(4000)) in encounters | Free-text surgical history; no structured procedure table |
| Clinical notes / documents | ✅ Covered | Full note structure in encounters: CC, HPI, ROS, PE, Assessment, Plan, Family/Social/Medical/Surgical History | Present but entirely as free-text blobs (nvarchar(4000)); represents the traditional SOAP note structure |
| Care plans / goals | ❌ Not covered | No care plan table or fields | Product is certified for (b)(11) Care Plan; this is a gap |
| Orders / referrals | ❌ Not covered | Order Date exists in practice clinical table; no standalone orders entity | Product supports e-prescribing and ordering; gap |
| Insurance / coverage | ✅ Covered | `Patient Insurances` (24 fields) — type, payer, policy details, policy holder info | Solid coverage |
| Claims / billing | ⚠️ Partial | "Billing" multi-record field in encounters; `Practice Billing Encounters` (16 fields) — TIN, NPI, encounter/diagnosis codes, modifiers, place of service, insurers | Product has RCM features; billing data present but thin (single encounter code, single diagnosis code per row — unclear how multiple diagnoses per encounter are handled) |
| Payments | ❌ Not covered | No payment data in any table | If the product tracks payments as part of RCM, this is a gap |
| Consents / directives | ❌ Not covered | No consent or advance directive fields | Unknown whether product stores these |
| Patient communications / portal | ❌ Not covered | No patient messaging or portal data | Unknown whether product has patient portal |
| Specialty-specific (post-acute care) | ❌ Not covered | No specialty-specific tables for wound care, CCM, AWV, or other post-acute workflows | Product has specialized templates for wound care, psychiatry, cardiology, nephrology, plus AWV and CCM workflows. None of these appear as distinct export entities. Significant gap given the product's post-acute focus. |

## 6. Documentation Quality

**Overall: Low.** The documentation is a basic data dictionary consisting only of field names and SQL Server data types. It lacks nearly everything a developer would need to work with the export:

- **No field descriptions**: Zero of 154 fields have descriptions. Field names are the only guide (e.g., "Codesys" — what code systems? "Category" — what are the valid values?).
- **No value sets**: Fields like "Administrative Gender," "Race," "Ethnithity," "Progress Notes Type," and "Category" have no enumerated values.
- **No relationships**: No foreign keys, join conditions, or entity-relationship documentation. How does a single-patient encounter link to demographics? Presumably by patient identity, but this isn't documented.
- **No format specification**: The actual export file format (CSV, JSON, XML, etc.) is never specified. "Machine readable file formats" is the only statement.
- **No serialization documentation**: Five fields are noted as "multiple records" in a single nvarchar field, but the delimiter/structure is not documented.
- **No sample data**: No example exports provided.
- **No machine-readable artifacts**: No JSON schema, XSD, DDL, or CSV header specification.
- **Several typos**: "Ethnithity," "Mother Mainder Name," "Chief Comlaint," "Historhy of Present Illness," "L:abs" — suggesting limited editorial review.
- **Stale**: Created November 2023 at certification time; byte-identical copy posted in 2025 confirms no updates.
- **Contradictory format claims**: The data dictionary describes flat SQL Server-derived tables, while the RWT plan mentions "C-CDA files or FHIR APIs." These are fundamentally different structures.

A developer receiving this export would be unable to reliably parse multi-valued fields, distinguish between clinical data categories in the generic practice clinical table, or understand what code systems are used — without direct vendor assistance.

## 7. Overall Assessment

### Classification

**Partial native export.** The data dictionary describes a native database projection (SQL Server column types, denormalized tables) rather than a standard-based representation. However, it has significant coverage gaps — particularly in specialty clinical data, care plans, orders, and structured clinical content — and the documentation is too thin to be usable without vendor assistance.

### Key Findings

1. **Export is a thin native database projection with 7 tables and 154 fields** — sourced from `Aarista_EHI_Export.pdf`, this represents a modest schema with basic coverage of demographics, insurance, encounters, and billing. Compare to vendors with hundreds of tables covering the same domains.

2. **Clinical content is largely free-text blobs** — the encounters table stores most clinical data (ROS, PE, vitals, labs, radiology, assessment, plan) as nvarchar(4000) text fields, making structured data extraction very difficult. Only the practice-level clinical table offers some structured representation (code, code system, category, results).

3. **Zero field descriptions across all 154 fields** — the data dictionary provides only names and SQL types. No value sets, no code system documentation, no relationships, no sample data. The format of the export files themselves is never specified.

4. **Specialty/post-acute clinical workflows are absent** — despite the product's focus on post-acute care with specialized templates (wound care, CCM, AWV, psychiatry), none of these appear in the export. Care plans (certified under (b)(11)) are also missing.

5. **Documentation is stale and contradictory** — created at certification time (Nov 2023) and never updated. The RWT plan (Oct 2024) mentions "C-CDA files or FHIR APIs" as the export format, which contradicts the flat-table structure in the data dictionary.

### Summary Stats

```
Classification:  Partial native export
Export format:   Unspecified ("machine readable file formats"); SQL Server types suggest CSV/TSV
Model type:      Native database projection
Entities:        7 tables
Fields:          154
Descriptions:    0% (0 of 154 fields have descriptions)
Sample data:     No
Bulk export:     Yes (practice-level tables for population export)
Domains covered: 7 of 15 applicable domains (✅ or ⚠️ partial)
```

### Bottom Line

The Aarista EHI export provides a minimal data dictionary with 7 flat tables covering demographics, insurance, encounters, and basic billing — but clinical data is mostly stored as unstructured text blobs, the export format is never specified, and zero fields have descriptions. The most significant gap is the absence of the product's specialty post-acute care data (wound care, CCM, AWV templates, care plans) — the very workflows that define this product's value proposition. A patient or provider would get a rough outline of their clinical record but not the structured, specialty-specific data that drives care decisions in post-acute settings.
