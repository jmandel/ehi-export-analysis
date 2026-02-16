# EHI Export Analysis: Aarista Technology LLC

**Product**: Aarista v1.0
**Analysis date**: 2026-02-16
**CHPL IDs**: 11329 (15.04.04.3168.Aari.01.00.1.230808)

## 1. Product Context

Aarista is a certified EHR platform purpose-built for **post-acute and outpatient care**, primarily serving skilled nursing facilities (SNFs), long-term care, assisted living, and ambulatory settings. It is developed by Aarista Technology LLC, closely linked to Altea Healthcare. As of 2024, the platform served 70,000+ patients across 14 states.

The product combines traditional EHR functionality with an AI/ML analytics layer ("Aari"). Key capabilities relevant to EHI scope:

- **Clinical documentation**: Patient profiles, clinical notes, smart templates for specialties (wound care, psychiatry, cardiology, nephrology), voice-enabled dictation
- **Ordering/prescribing**: E-prescribing for controlled and non-controlled medications
- **Practice management/billing**: Revenue cycle management with billing documentation, compliance tracking, RVU tracking, coding trends
- **Care management**: Automated AWV and CCM workflows, care coordination
- **Scheduling**: Smart Scheduler with drag-and-drop appointments
- **Telehealth**: Integrated virtual consultations, remote patient monitoring
- **Integrations**: Bidirectional EHR integration with PCC, MatrixCare, Epic, Cerner, etc.

The product holds a broad set of ONC certifications: (a)(1)–(a)(5), (a)(12), (a)(14), (b)(1), (b)(10), (b)(11), (c)(1), (e)(3), (g)(7)–(g)(10), (h)(1). This indicates comprehensive clinical capability, not a single-criterion module.

**Baseline for export completeness**: A genuine (b)(10) export should cover demographics, encounters, clinical notes, medications, problems, allergies, immunizations, vitals, labs, procedures, insurance/coverage, billing/claims data, care plans, and specialty-specific assessments.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `Aarista_EHI_Export.pdf` (183,079 bytes, 8 pages) | EHI Export Data Dictionary — 7 tables with field names and SQL Server data types. Created 2023-11-28 by Michael Mai in Microsoft Word. | **Primary artifact** — the only structured documentation of the export. |
| `b10-Real-World-Test-Plan-2025.pdf` (204,611 bytes, 5 pages) | Real World Testing Plan for (b)(10), scanned document signed 10/15/2024. Describes test methodology, care settings, expected outcomes. | **Secondary** — confirms export scope and format claims but provides no additional data dictionary detail. |

**Verification note**: The prior report stated both `alteahc.com` and `aarista.com` were returning HTTP 403 as of 2026-02-14. As of this analysis (2026-02-16), both sites are live and returning HTTP 200. The PDF at the registered URL (`https://alteahc.com/wp-content/uploads/2023/11/Aarista_EHI_Export-.pdf`) is accessible and byte-identical to the Wayback Machine copy (MD5: `7899ad9b157c7d2176bb22e4b7cf383e`). The document has not been updated since its original creation on 2023-11-28.

## 3. Export Mechanics

- **Format**: Unspecified. The documentation states only "Export data files are machine readable file formats." The data types are SQL Server column types (nvarchar, int, date, datetime, float, bit), suggesting flat file output (likely CSV/TSV) derived from database tables/views. The Real World Test Plan (page 4) mentions "C-CDA files or FHIR APIs" as possible formats, but the data dictionary does not align with either standard — it describes denormalized flat tables, not C-CDA sections or FHIR resources.
- **Mechanism**: The data dictionary states "Customers can request to export individual patients or all patients for the practice." The RWT plan (page 4) states "Our export tool enables users with the appropriate permissions to generate and download EHI exports for a single patient or a population of patients within a specified date and time range." This indicates a UI-based export tool.
- **Single-patient vs bulk**: Both supported — 5 of the 7 tables are single-patient; 2 are practice-wide (all patients).
- **Access constraints**: Export requires "appropriate permissions." No mention of fees. Can be executed "at any time without developer assistance" per the RWT plan (page 4, citing §170.315(b)(10)(i)(B)).

## 4. Export Content: What's In It

The data dictionary defines **7 tables with 154 total fields**. Zero fields have descriptions beyond the field name. All fields specify SQL Server data types. No value sets, relationships, foreign keys, or sample data are documented.

### Vendor's own content organization

The vendor organizes the export into single-patient tables and practice-wide tables:

| Entity/Table | Fields | Descriptions | Types | Required | Category |
|---|---|---|---|---|---|
| Single Patient - Patient Demographics | 28 | 0/28 | Yes (SQL) | 6 | Demographics |
| Single Patient - Patient Addresses | 10 | 0/10 | Yes (SQL) | 7 | Demographics |
| Single Patient - Patient Contacts | 20 | 0/20 | Yes (SQL) | 12 | Demographics |
| Single Patient - Patient Insurances | 24 | 0/24 | Yes (SQL) | 8 | Insurance |
| Single Patient - Patient Encounters – Clinical and Billing | 31 | 0/31 | Yes (SQL) | 5 | Clinical & Billing |
| Practice Patients - Demographics and Billing Encounters | 16 | 0/16 | Yes (SQL) | 8 | Billing |
| Practice Patients - Demographics and Clinical Encounters | 25 | 0/25 | Yes (SQL) | 4 | Clinical |
| **Totals** | **154** | **0/154 (0%)** | — | **50** | — |

**Notable structural issues:**

1. **Free-text clinical blobs**: The single-patient encounter table stores clinical documentation as large nvarchar(4000) text fields — HPI, ROS, Physical Exam, Vital Signs, Labs, Radiology, Plan are all free-text blobs, not structured/coded data. This means clinical content is exported but not in a computable format.

2. **Multi-valued fields within single columns**: Medications (nvarchar(500)), Problems List (nvarchar(270)), Allergies (nvarchar(500)), Assessment (nvarchar(270)), and Billing (nvarchar(270)) are annotated as "multiple records" within single nvarchar fields. How these are delimited or structured is not documented.

3. **Generic clinical encounter table**: The practice-wide clinical encounters table uses a generic Name/Description/Code/Codesys/Category/Status structure to represent heterogeneous clinical data (labs, medications, problems, etc.) in a single flat table with a "Category" discriminator column (type: "constant string"). The valid Category values are not documented.

4. **Several fields marked n/a**: In the clinical encounters table, Dispense Number, Sig Number, Ordering Provider NPI, and Refill Times are listed as "n/a" — suggesting they are defined in the schema but not actually populated.

5. **Typos in field names**: "Mother Mainder Name" (Maiden), "Ethnithity" (Ethnicity), "Chief Comlaint" (Complaint), "Historhy of Present Illness" (History), "L:abs" (Labs) — indicating limited editorial review.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The export organizes data into three functional areas:

**Demographics and contacts** (3 tables, 58 fields): Comprehensive patient demographics including SSN, MBI, Medicaid#, gender identity, sexual orientation, race/ethnicity, language, PCP info, addresses, phone/email, emergency contacts, and guarantors. This is the richest area proportionally.

**Insurance** (1 table, 24 fields): Insurance type, payer, policy details, policy holder demographics. Reasonably thorough for coverage data.

**Clinical encounters and billing** (3 tables, 72 fields): Encounter-level clinical documentation (single-patient) plus practice-wide billing and clinical encounter tables. The single-patient encounter table is essentially a progress note export — chief complaint, HPI, ROS, exam, assessment, plan — stored as free-text blobs. The practice billing table captures encounter codes, diagnosis codes, modifiers, and place of service. The practice clinical table uses a generic entity-attribute-value structure for coded clinical data (medications, labs, problems, etc.).

**What's thinnest**: The clinical content is largely free-text. The billing data is limited to encounter-level codes (CPT/diagnosis) with no charge amounts, payment data, or claims lifecycle information. The generic clinical encounters table attempts to cover many data types in one flat structure but lacks documentation of the Category discriminator values.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | `Patient Demographics` (28 fields), `Patient Addresses` (10 fields), `Patient Contacts` (20 fields) | Thorough — SSN, MBI, Medicaid#, gender identity, sexual orientation, race, ethnicity, language, PCP |
| Encounters / visits | ✅ Covered | `Patient Encounters – Clinical and Billing` (31 fields) with DOS, facility, provider, progress note type | Encounter records present; no distinction between in-person and telehealth |
| Problems / conditions | ⚠️ Partial | "Problems List" in encounter table (nvarchar(270), multiple records); "Category" in practice clinical table | Included but as free-text blob in encounter notes; practice table may have structured data but Category values undocumented |
| Medications / prescriptions | ⚠️ Partial | "Medications" in encounter table (nvarchar(500), multiple records); medication-specific fields in practice clinical table (Strength, Sig, Dispense, Refills) | Encounter-level as free-text blob; practice clinical table has structured medication fields but 4 are marked "n/a" (unused) |
| Allergies | ⚠️ Partial | "Allergies" in encounter table (nvarchar(500), multiple records) | Free-text blob only; no structured allergy data (allergen, reaction, severity) |
| Immunizations | ⚠️ Partial | "Immunizations" in encounter table (nvarchar(4000)) | Free-text blob; no structured immunization records (vaccine, date, lot, site) |
| Vitals | ⚠️ Partial | "Vital Signs" in encounter table (nvarchar(4000)); Numresult/Units in practice clinical table | Free-text in encounter; practice table may have structured vitals via Category discriminator |
| Lab results | ⚠️ Partial | "L:abs" in encounter table (nvarchar(4000)); Code/Textresult/Numresult/Units in practice clinical table | Free-text in encounter; practice table likely has structured labs but undocumented |
| Imaging / diagnostic reports | ⚠️ Partial | "Radiology" in encounter table (nvarchar(4000)) | Free-text only |
| Procedures | ⚠️ Partial | Overview mentions "procedures" in the export; encounter codes in billing table | Encounter/diagnosis codes present; no dedicated procedure table |
| Clinical notes / documents | ✅ Covered | Encounter table: Chief Complaint, HPI, ROS, Physical Exam, Assessment, Plan, etc. | Full progress note structure, albeit as free-text blobs |
| Care plans / goals | ❌ Not covered | No care plan entity in export | Product is certified for (b)(11) care plans; this is a gap |
| Orders / referrals | ❌ Not covered | No orders or referrals table | Product has e-prescribing; no prescription order records in export |
| Insurance / coverage | ✅ Covered | `Patient Insurances` (24 fields) with type, payer, policy details | Solid coverage of insurance/enrollment data |
| Claims / billing | ⚠️ Partial | `Practice Billing Encounters` (16 fields): encounter codes, diagnosis codes, modifiers, place of service, insurer names | Coding data present but no charge amounts, payments, claims status, or RCM lifecycle data. Product has revenue cycle management features. |
| Payments | ❌ Not covered | No payment data in export | Product has RCM features; no payment amounts, adjustments, or financial transactions |
| Consents / directives | ❌ Not covered | No consent entities | Unknown whether product stores advance directives |
| Patient communications | ❌ Not covered | No messaging or portal data | Product has (e)(3) patient health info export certification but no patient-facing data in EHI export |
| Specialty-specific data | ❌ Not covered | No specialty-specific tables (wound care assessments, psychiatry notes, etc.) | Product advertises smart templates for wound care, psychiatry, cardiology, nephrology — none represented as distinct data in export |

**Summary**: 4 of 18 domains covered, 8 partially covered, 6 not covered.

## 6. Documentation Quality

**Rating: Low**

The data dictionary provides field names and SQL Server data types — nothing more. A developer receiving this export would face major challenges:

- **No field descriptions**: 0 of 154 fields have descriptions. Field names are the only guide (e.g., "Codesys" — code system? "Sig" — prescription directions? A developer would need to guess).
- **No value sets**: Fields like "Administrative Gender," "Category," "Progress Notes Type," "Status" have no documented allowed values.
- **No relationships**: No documentation of how the 7 tables relate to each other. No foreign keys, join columns, or entity-relationship diagram.
- **No export format specification**: The actual file format is never stated — CSV? TSV? JSON? What delimiter, encoding, or header conventions?
- **No multi-value serialization spec**: Five fields are marked "multiple records" within a single nvarchar column, but how they are delimited is never explained.
- **No sample data**: No example export files or sample records.
- **No machine-readable schema**: No XSD, JSON Schema, DDL, or CSV header spec.
- **Typos in field names**: Five typos in field names suggest minimal editorial review.
- **Stale documentation**: Created 2023-11-28 at certification time and never updated (byte-identical to 2025 re-upload).

A developer could not build a reliable import from this documentation alone. The format is unknown, the multi-valued field encoding is unknown, the Category discriminator values are unknown, and relationships between tables are undocumented.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Partial**

The export covers demographics and insurance well, and includes encounter-level clinical and billing data, but has significant gaps relative to what the product stores. Care plans (certified (b)(11)) are absent. Specialty-specific clinical data (wound care, psychiatry, cardiology, nephrology templates) is absent despite being a key product feature. Revenue cycle management data beyond encounter codes is absent — no charge amounts, payments, or claims lifecycle. E-prescribing order records are absent. The clinical content that is included is largely free-text blobs rather than structured/coded data, limiting its computability.

The export covers the core structure of a patient record (demographics, insurance, encounter notes, basic billing codes) but misses the depth and breadth expected from a product with this feature set. It's more than a bare C-CDA summary — it includes insurance and billing code data — but less than a comprehensive EHI export.

**Axis 2 — Export approach: Purpose-built EHI export**

This is not a repackaged C-CDA or FHIR export. The data dictionary describes a native database projection with SQL Server types, 7 custom tables, and a structure that doesn't correspond to any clinical exchange standard. The export includes insurance and billing data that would not be in a standard (g)(10) or C-CDA exchange. Despite the RWT plan's mention of "C-CDA files or FHIR APIs," the data dictionary clearly describes a purpose-built flat-file export from the product's internal data model.

However, the export appears to have been built quickly with minimal documentation effort — the typos, the free-text blobs, the "n/a" fields, and the lack of any descriptive metadata all suggest this was a certification-time artifact created with limited investment.

### Key Findings

1. **The export is purpose-built but thin**: 7 tables with 154 fields covering demographics, insurance, encounters, and basic billing — a real (b)(10) effort, not a relabeled C-CDA, but significantly below the breadth of what the product stores.

2. **Zero field descriptions**: Not a single field out of 154 has a description. Combined with no value sets, no relationships, and no format specification, the documentation would be extremely difficult for a third party to use.

3. **Clinical content is largely free-text**: The encounter table stores clinical documentation (HPI, ROS, Physical Exam, Vitals, Labs, etc.) as nvarchar(4000) text blobs — this is exported but not computable. The practice-wide clinical table has a more structured EAV format but its Category discriminator is undocumented.

4. **Care plans, specialty data, and RCM data missing**: Despite the product being certified for care plans (b)(11), having specialty templates (wound care, psychiatry), and offering revenue cycle management features, none of these appear in the export.

5. **Vendor websites now accessible**: Both `alteahc.com` and `aarista.com` are currently live (HTTP 200), contradicting the prior report's finding of HTTP 403. The PDF at the registered URL is accessible and unchanged since 2023-11-28.

### Summary Stats

```
Coverage:        Partial
Approach:        Purpose-built EHI export
Export format:   Unspecified ("machine readable file formats"); SQL Server types suggest flat file (CSV/TSV)
Entities:        7
Fields:          154
Descriptions:    0% (0/154 fields with descriptions)
Sample data:     No
Bulk export:     Yes (practice-wide tables support all-patient export)
Domains covered: 4 of 18 fully, 8 partially, 6 not covered
```

### Bottom Line

Aarista built a purpose-specific (b)(10) export rather than relabeling an existing clinical exchange, which puts it ahead of many vendors — but the result is thin. A patient would get their demographics, insurance info, and encounter notes (as free-text), plus some billing codes, but would miss care plans, specialty assessments, detailed prescriptions, and financial data. The documentation is too sparse (0% field descriptions, no format spec, no value sets) for any third party to reliably interpret or import the exported data.
