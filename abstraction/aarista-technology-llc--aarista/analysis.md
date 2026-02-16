# EHI Export Analysis: Aarista Technology LLC

**Product**: Aarista EHR System
**Analysis date**: 2026-02-16
**CHPL IDs**: 15.04.04.3168.Aari.01.00.1.230808

## 1. Product Context

Aarista is a certified EHR platform purpose-built for **post-acute and outpatient care**, serving 70,000+ patients across 14 states. Its primary users are nurse practitioners, physicians, and post-acute facility administrators working in skilled nursing facilities (SNFs), long-term care, and assisted living. The platform is closely linked to Altea Healthcare, a post-acute provider services company.

Key capabilities relevant to EHI export completeness:
- **Clinical documentation**: Progress notes with smart templates, voice dictation, specialty-specific workflows (wound care, psychiatry, cardiology, nephrology)
- **Practice management**: Scheduling, revenue cycle management, billing documentation, compliance tracking
- **Orders/prescribing**: E-prescribing (controlled and non-controlled), e-faxing
- **Care management**: Annual Wellness Visit (AWV), Chronic Care Management (CCM) workflows
- **Telehealth & remote monitoring**: Integrated virtual visits, vital sign monitoring
- **AI/analytics**: Risk prediction, real-time clinical alerts, population risk stratification ("Aari" neural network)
- **Integrations**: Bidirectional connections to PCC, MatrixCare, Epic, Cerner, Allscripts, Meditech, VA systems
- **Mobile app**: iOS/Android provider app

The product is certified for 32 ONC criteria including (b)(10) EHI export, (g)(10) FHIR API, (b)(1) transitions of care, and clinical criteria (a)(1)–(a)(5), (a)(12), (a)(14). This is a full clinical EHR with practice management capabilities — a genuine (b)(10) export should cover clinical data, billing/RCM data, insurance, care management workflows, and specialty assessments.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `Aarista_EHI_Export.pdf` (183 KB, 8 pages) | EHI Export Data Dictionary listing 7 data tables with field names and SQL Server data types. Created 2023-11-28 by Michael Mai. Retrieved from Wayback Machine (original URL returns 403). | **Primary artifact** — only source of export content detail |
| `b10-Real-World-Test-Plan-2025.pdf` (205 KB, 5 pages) | Real World Testing Plan 2025 for (b)(10). Scanned document describing test methodology, care settings, expected outcomes. Signed by Michael Mai on 10/15/2024. | **Secondary** — provides export mechanics info but no content detail |

Only two artifacts exist. No sample data files, no machine-readable schemas, no additional documentation. The data dictionary PDF is the sole source for understanding export content.

## 3. Export Mechanics

- **Format**: "Machine readable file formats" (per data dictionary, p.1). The RWT plan mentions "C-CDA files or FHIR APIs" as export format options. The data dictionary itself describes SQL Server column types (nvarchar, date, int, etc.), suggesting the native export is a database-level extraction, not a standards-based format.
- **Mechanism**: Export tool accessible to users with "appropriate permissions" (RWT plan, p.4). The RWT plan states users can "generate and download EHI exports" and can "execute this capability at any time... without developer assistance" (§170.315(b)(10)(i)(B)).
- **Single-patient vs bulk**: Both supported. The data dictionary defines two modes: "Single Patient" tables (4 entities for individual patient export) and "Practice Patients" tables (2 entities for bulk practice-level export). The RWT plan confirms testing of both "single-patient and population-level EHI exports."
- **Date filtering**: Exports can be generated "within a specified date and time range" (RWT plan, p.4).
- **Access constraints/fees**: Not documented; no mention of fees.

## 4. Export Content: What's In It

The data dictionary defines **7 entities with 154 total fields**. Zero fields have descriptions beyond their column names. All fields have SQL Server data types specified. No relationships, foreign keys, value sets, or code systems are documented.

### Vendor's own content organization

The vendor organizes the export into two modes: **Single Patient** (4 entities) and **Practice Patients** (2 entities for bulk export), plus a shared encounters table.

| Entity/Table | Fields | Described | Types | Mode |
|---|---|---|---|---|
| Single Patient - Patient Demographics | 28 | 0 | yes | Single Patient |
| Single Patient - Patient Addresses | 10 | 0 | yes | Single Patient |
| Single Patient - Patient Contacts | 20 | 0 | yes | Single Patient |
| Single Patient - Patient Insurances | 24 | 0 | yes | Single Patient |
| Single Patient - Patient Encounters – Clinical and Billing | 31 | 0 | yes | Single Patient |
| Practice Patients - Patient Demographics and Billing Encounters | 16 | 0 | yes | Practice (Bulk) |
| Practice Patients - Patient Demographics and Clinical Encounters | 25 | 0 | yes | Practice (Bulk) |

**Key observations:**

1. **The encounters table is a flattened clinical note**: The "Patient Encounters – Clinical and Billing" entity (31 fields) is essentially a denormalized progress note with fields like Chief Complaint, HPI, Review of Systems, Physical Exam, Vital Signs, Labs, Radiology, Assessment, Plan, and Billing — all as free-text `nvarchar(4000)` blobs. Clinical data elements (medications, problems, allergies, assessment, billing) are noted as "multiple records" but stored in narrow varchar fields, suggesting they're serialized text rather than structured data.

2. **Practice bulk export is even thinner**: The bulk "Billing Encounters" table (16 fields) contains only encounter-level billing line items (encounter code, diagnosis code, modifiers, place of service, insurers). The bulk "Clinical Encounters" table (25 fields) appears to be a generic clinical items table with a `Category` constant-string field that likely distinguishes problems, meds, labs, etc. — a single flat table for all clinical data types.

3. **Several fields marked "n/a"**: In the Practice Clinical Encounters table, fields like `Dispense Number`, `Sig Number`, `Ordering Provider NPI`, and `Refill Times` have data type "n/a", suggesting they are not yet implemented.

4. **Typos throughout**: "Ethnithity," "Mother Mainder Name," "Chief Comlaint," "Historhy of Present Illness," "L:abs" — suggesting minimal quality review of the documentation.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor's export covers two broad areas:

**Demographics & administrative data (82 fields across 4 entities)**: Patient demographics (28 fields), addresses (10 fields), contacts/emergency contacts (20 fields), and insurance information (24 fields). This is the richest area — insurance data includes payer details, policy holder information, and prior authorization reference.

**Clinical & billing encounter data (72 fields across 3 entities)**: A single-patient encounters table that flattens an entire clinical note into text blobs, plus two practice-level bulk tables for billing and clinical encounter data. The billing encounter table has basic claim-level fields (CPT code, ICD code, modifiers, place of service). The clinical encounter table is a generic structure with Code/Codesys/Category/Status fields that appears to handle problems, medications, labs, vitals, and other clinical items in a single flat table.

**What's notably absent**: No dedicated tables for medications (as structured data), lab results (structured), vital signs (structured), immunizations (structured), allergies (structured), care plans, procedures, orders, documents/attachments, care management workflows (AWV, CCM), telehealth encounters, remote monitoring data, or any specialty-specific assessments.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | `Patient Demographics` (28 fields), `Patient Addresses` (10 fields), `Patient Contacts` (20 fields) | Reasonably thorough for basic demographics |
| Encounters / visits | ⚠️ Partial | `Patient Encounters – Clinical and Billing` has DOS, Facility, Provider, Progress Notes Type | Encounter metadata present but minimal; no encounter status, type codes, or disposition |
| Problems / conditions | ⚠️ Partial | `Problems List` as nvarchar(270) text blob in encounters; `Practice Clinical Encounters` has Code/Description with Category | Serialized text, not structured. Bulk table may provide coded data but lacks onset dates, severity, verification status |
| Medications / prescriptions | ⚠️ Partial | `Medications` as nvarchar(500) text blob in encounters; bulk Clinical Encounters has Medication Strength, Sig fields | E-prescribing data not in dedicated table; medication fields in bulk table have "n/a" for Dispense Number, Ordering Provider NPI, Refill Times |
| Allergies | ⚠️ Partial | `Allergies` as nvarchar(500) text blob in encounters | Text only, no structured allergy data (reaction type, severity, substance coding) |
| Immunizations | ⚠️ Partial | `Immunizations` as nvarchar(4000) text blob in encounters | Text only, no structured immunization records (vaccine code, lot, site, route) |
| Vitals | ⚠️ Partial | `Vital Signs` as nvarchar(4000) text blob in encounters; may appear in bulk Clinical Encounters | Text blob in single-patient; possibly coded in bulk table but undifferentiated |
| Lab results | ⚠️ Partial | `L:abs` [sic] as nvarchar(4000) text blob; bulk Clinical Encounters has Numresult, Textresult, Units | Text blob in single-patient; bulk table may have structured results but unclear |
| Imaging / diagnostic reports | ⚠️ Partial | `Radiology` as nvarchar(4000) text blob in encounters | Text only |
| Procedures | ⚠️ Partial | `Past Surgical History` as nvarchar(4000) text blob | Historical text; no structured procedure records |
| Clinical notes / documents | ⚠️ Partial | Encounter table has Chief Complaint, HPI, ROS, Physical Exam, Assessment, Plan (all nvarchar(4000)) | Flattened note sections present but as text blobs; no document metadata, no scanned/uploaded documents |
| Care plans / goals | ❌ Not covered | No care plan entities in export | Product is certified for (b)(11) care plans; this is a gap |
| Orders / referrals | ❌ Not covered | `Order Date` field in bulk Clinical Encounters only | Product supports e-prescribing and ordering; no dedicated order tables |
| Insurance / coverage | ✅ Covered | `Patient Insurances` (24 fields) with payer details, policy info, prior auth | Reasonably detailed |
| Claims / billing | ⚠️ Partial | `Billing` text blob in single-patient encounters; bulk `Billing Encounters` (16 fields) with encounter/diagnosis codes | Bulk table has basic billing line items; no claims, payments, adjustments, charge detail |
| Payments | ❌ Not covered | No payment entities | Product has RCM capabilities; this is a gap |
| Consents / directives | ❌ Not covered | No consent entities | Not clear if product stores these |
| Patient communications | ❌ Not covered | No messaging or portal entities | Product has (e)(3) patient health info export certification; likely has some portal capability |
| Specialty-specific data | ❌ Not covered | No wound care, psychiatry, cardiology, or nephrology tables | Product advertises specialty-specific templates for wound care, psychiatry, cardiology, nephrology; this is a significant gap |

## 6. Documentation Quality

**Very poor.** The documentation has significant deficiencies:

- **No field descriptions**: All 154 fields have only a name and SQL Server data type. No descriptions, no explanations of what values to expect.
- **No value sets or code systems**: Fields like "Administrative Gender," "Race," "Category," and "Status" provide no information about valid values or coding systems used.
- **No relationships or foreign keys**: No indication of how entities relate to each other or how records link across tables.
- **No sample data**: No example exports or sample records to illustrate the format.
- **No machine-readable schema**: Only a PDF with tables.
- **Format ambiguity**: The dictionary says "machine readable file formats" but doesn't specify what format (CSV? JSON? XML?). The RWT plan adds confusion by mentioning "C-CDA files or FHIR APIs" — which contradicts the SQL Server data types in the dictionary.
- **Numerous typos**: "Ethnithity," "Mother Mainder Name," "Chief Comlaint," "Historhy of Present Illness," "L:abs" — undermining confidence in documentation quality.
- **Incomplete type specifications**: Several fields in the Practice Clinical Encounters table show "n/a" for data type, suggesting unfinished implementation.

A developer could not build a reliable import from this documentation alone. The lack of value sets, relationships, and format specification would require direct vendor engagement to interpret the export.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Partial**

The export covers demographics and insurance reasonably well (82 fields across 4 entities), but clinical data is largely exported as free-text blobs rather than structured data. The single-patient encounter table flattens an entire clinical note into ~20 nvarchar(4000) text fields — this is closer to a document export than a data export. The bulk practice-level tables provide some structure (coded clinical items, billing line items) but are thin and generic. Significant gaps exist relative to what the product stores: no care plans despite (b)(11) certification, no structured orders despite e-prescribing capability, no specialty-specific data despite advertising wound care/psychiatry/cardiology/nephrology templates, no payment or detailed billing data despite RCM capabilities, and no care management workflow data (AWV, CCM) despite these being core features.

**Axis 2 — Export approach: Purpose-built EHI export**

This is not a repackaged C-CDA or FHIR export. The data dictionary describes SQL Server column types and a native database-level extraction with tables mapped to the product's internal data model. The vendor built a specific export for (b)(10) that goes beyond standard clinical exchange formats. However, the "purpose-built" classification should not be confused with "well-built" — the export is purpose-built but thin and incomplete. The RWT plan's mention of "C-CDA files or FHIR APIs" as possible formats introduces confusion, but the data dictionary clearly describes a proprietary structure.

### Key Findings

1. **Clinical data exported as text blobs, not structured data.** The core encounter table stores clinical information (medications, problems, allergies, vitals, labs, radiology, assessment, billing) as nvarchar(4000) free-text fields. This means clinical data is technically present but not machine-parseable — defeating much of the purpose of a computable EHI export.

2. **Only 7 entities with 154 fields and zero descriptions.** For a product managing 70,000+ patients across multiple specialties, this is extremely thin. No field descriptions, no value sets, no relationships, and no sample data.

3. **Major domain gaps relative to product capabilities.** Care plans, structured orders, specialty-specific data (wound care, psychiatry, cardiology, nephrology templates), care management workflows (AWV, CCM), payments/detailed billing, and patient communications are all absent despite being advertised product capabilities.

4. **Documentation quality is poor.** Numerous typos ("Ethnithity," "L:abs," "Chief Comlaint"), unfinished fields marked "n/a," ambiguous format specification, and no machine-readable artifacts.

5. **Both single-patient and bulk export supported.** The export does support both individual and practice-level exports, which is a positive feature. The bulk export includes both billing and clinical encounter data, though in a very flat structure.

### Summary Stats

    Coverage:        Partial
    Approach:        Purpose-built EHI export
    Export format:   Proprietary (SQL Server-typed fields; format unspecified — possibly CSV/flat file)
    Entities:        7
    Fields:          154
    Descriptions:    0% (0 of 154 fields have descriptions)
    Sample data:     No
    Bulk export:     Yes
    Domains covered: 2 fully, 9 partially, 5 not covered of 16 applicable domains

### Bottom Line

Aarista's EHI export is a purpose-built but underdeveloped effort. While it covers demographics and insurance adequately and supports both single-patient and bulk export, the clinical data is largely exported as unstructured text blobs rather than computable data, and major domains (care plans, specialty assessments, structured orders, payments) are missing entirely. The biggest gap is the text-blob approach to clinical data: a patient could technically get their encounter notes, but the data would not be meaningfully structured or importable into another system.
