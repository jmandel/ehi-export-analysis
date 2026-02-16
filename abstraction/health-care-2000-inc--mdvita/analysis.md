# EHI Export Analysis: Health Care 2000, Inc.

**Product**: MDVita
**Analysis date**: 2026-02-16
**CHPL IDs**: 15.04.04.2904.MDVi.27.02.1.221020

## 1. Product Context

MDVita is an ONC-certified EHR and practice management suite developed by Health Care 2000, Inc., a small family-owned company based in Miami, FL. The product serves ambulatory primary care practices, particularly those in South Florida operating under Medicare Advantage risk-based contracts and value-based payment arrangements. The SED-tested user type is "Family Practice."

MDVita is a combined clinical EHR and practice management system. Key capabilities include:

- **Clinical EHR**: Patient demographics, problem lists, medication management, allergies, vital signs, clinical notes (SOAP), CPOE for medications/labs/imaging, immunizations, clinical decision support, family health history, care plans
- **Practice Management / Billing**: Revenue cycle management, billing/claims management (the company originated as a claim adjudication company), scheduling, insurance plan management
- **ePrescribing**: Electronic prescribing
- **Analytics** (MDVita Analytics add-on): Financial reporting, utilization analysis, claims data reporting
- **Interoperability**: FHIR API, C-CDA exchange, Direct messaging, patient portal
- **Public Health**: Immunization registry, syndromic surveillance reporting

The product holds 38+ ONC certification criteria including (b)(10). Given its combined EHR + practice management nature, a comprehensive (b)(10) export should cover clinical data, billing/claims, insurance, payments, referrals, documents, and communications.

## 2. Artifacts Reviewed

| Artifact | Description | Informative? |
|---|---|---|
| `downloads/MDVita_EHR_EHI_DataFormat.pdf` | 28-page EHI Export Data Format specification (Guide v1.2, Sep 2023, PDF created Jan 2024). Documents all 24 Parquet data files plus SOAP notes and documents delivery mechanism. Contains column-level data dictionary with names, types, descriptions, and coded value enumerations for every field. | **Primary artifact — highly informative** |
| `product-research.md` | Prior research on MDVita's capabilities, market position, and data stored. | Useful for context |
| `ehi-export-report.md` | Prior agent's narrative about the export documentation. | Used for orientation only |

The single PDF is the sole artifact and it is substantive — 28 pages of detailed, field-level data dictionary documentation for a purpose-built EHI export.

## 3. Export Mechanics

- **Format**: Apache Parquet files for structured data; PDF files for SOAP clinical notes; original format (PDF, XML, HTML, CSV, DOC, JPG, etc.) for uploaded documents
- **Mechanism**: Scheduled from within the MDVita application UI (per the document: "use the MDVita User Guide for instructions how to schedule an EHI export")
- **Single-patient vs bulk**: Not explicitly stated in the export format document; the export appears to be a bulk export (file names like `Patient.parquet` suggest all patients, not per-patient files)
- **Document delivery**: SOAP notes and documents are provided by reference via time-limited Azure Blob Storage URLs (valid for 14 days). CSV reference files map filenames to download URLs
- **Access constraints**: The 14-day download window for documents/SOAP notes is a constraint. No fees are mentioned in the export documentation

## 4. Export Content: What's In It

The export produces 24 Apache Parquet data files plus SOAP note PDFs and uploaded documents. The PDF data dictionary documents every file with column names, data types, descriptions, and coded value enumerations.

**Parsed statistics** (from `analysis/entity-inventory-full.json`):
- **24 entities** (Parquet files)
- **453 total fields** across all entities
- **453 fields with descriptions** (100% coverage)
- **453 fields with data types** (100% coverage)
- **21 fields with coded value enumerations** (e.g., gender codes, order types, claim types, status indicators)

### Vendor's own content organization

The vendor organizes files by functional area. Below is a complete table:

| Entity/Table | Fields | Described | Types | Category |
|---|---|---|---|---|
| Patients | 31 | 31 | yes | Demographics |
| ProviderNetwork | 21 | 21 | yes | Providers (external) |
| ProviderPCPs | 21 | 21 | yes | Providers (in-house) |
| Locations | 14 | 14 | yes | Facility |
| PatientPlans | 24 | 24 | yes | Insurance / Coverage |
| Appointments | 20 | 20 | yes | Scheduling |
| SOAPNotesIndex | 9 | 9 | yes | Clinical Notes (index) |
| Orders | 10 | 10 | yes | Orders |
| ProblemList | 10 | 10 | yes | Clinical - Problems |
| Allergies | 9 | 9 | yes | Clinical - Allergies |
| MedicationList | 20 | 20 | yes | Clinical - Medications |
| ProcedureList | 5 | 5 | yes | Clinical - Procedures |
| DocumentsIndex | 12 | 12 | yes | Documents (index) |
| LabResults | 21 | 21 | yes | Clinical - Labs |
| Claims | 85 | 85 | yes | Billing / Claims |
| Referrals | 50 | 50 | yes | Referrals / Prior Auth |
| Emails | 12 | 12 | yes | Communications |
| Immunizations | 17 | 17 | yes | Clinical - Immunizations |
| Vitals | 7 | 7 | yes | Clinical - Vitals |
| DocumentSignatures | 4 | 4 | yes | Documents |
| ClaimsInsurancePayments | 24 | 24 | yes | Billing / Payments |
| MemberCharges | 8 | 8 | yes | Billing / Charges |
| MemberPayments | 13 | 13 | yes | Billing / Payments |
| DocumentAnnotations | 6 | 6 | yes | Documents |

**Notable entities:**
- **Claims** (85 fields): The largest entity — a denormalized table combining claim header data (encounter type, billing pay-to info, accident details, EPSDT flags) with procedure line details (CPT codes, charges, modifiers, diagnosis pointers). Includes both encounters and HCFA 1500 FFS claims. Richly coded with 10 fields having enumerated values.
- **Referrals** (50 fields): Combines referral tracking with prior authorization/certification data, including payor certification actions, diagnosis codes, procedure codes, and clinical notes status. 5 fields with coded values.
- **PatientPlans** (24 fields): Detailed insurance plan data including line of business, copay breakdowns (X-ray, ER, specialist, Rx brand/generic), and location linkage.
- **ClaimsInsurancePayments** (24 fields): Detailed EOB posting data with check info, procedure-level paid amounts, allowed amounts, coinsurance, copay, deductibles, interest, adjustments, and reason codes.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor's export covers three distinct areas:

**Clinical data (7 entities, ~92 fields):** Problem lists, allergies, medications, procedures, lab results, immunizations, and vitals. Each is a dedicated Parquet file with field-level detail. The medication list is particularly thorough (20 fields including NDC, route, frequency, dosage, SIG directions). Lab results include SNOMED mappings and multiple test identifiers. The problem list supports ICD-10, ICD-9, and SNOMED standards.

**Billing / Revenue Cycle (4 entities, ~130 fields):** Claims (85 fields) is the richest entity in the entire export, covering both encounters and HCFA 1500 fee-for-service claims with procedure-level detail, modifiers, diagnosis pointers, charges, and payments. ClaimsInsurancePayments (24 fields) provides granular EOB data. MemberCharges (8 fields) and MemberPayments (13 fields) track patient-facing financial transactions. This is genuinely deep billing coverage — the company's roots in claim adjudication are evident.

**Administrative / Coordination (13 entities, ~231 fields):** Demographics (31 fields including employer data, language, transportation needs), insurance plans (24 fields), appointments (20 fields), providers (42 fields across two files for in-house vs. network), locations (14 fields), referrals/prior auth (50 fields), clinical notes index (9 fields), documents index (12 fields), document signatures (4 fields), document annotations (6 fields), and internal emails (12 fields).

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | `Patients` (31 fields): name, DOB, SSN, address, phones, race, ethnicity, language, employer, PCP, cause of death | Thorough — includes employer data, transportation needs, language codes |
| Encounters / visits | ✅ Covered | `Appointments` (20 fields), `SOAPNotesIndex` (9 fields), `Claims` encounter records | Appointments + encounters in claims + SOAP note index |
| Problems / conditions | ✅ Covered | `ProblemList` (10 fields): ICD codes with standard qualifier (ICD-10/ICD-9/SNOMED), status, date ranges | Solid — supports multiple coding standards |
| Medications / prescriptions | ✅ Covered | `MedicationList` (20 fields): drug name, generic name, strength, NDC, route, frequency, dosage, SIG, date ranges | Thorough — covers drug details, dispensing info |
| Allergies | ✅ Covered | `Allergies` (9 fields): name, class (Drug/Environmental/Substance), NDC, SNOMED, UNII codes, status | Good — multiple standard identifiers |
| Immunizations | ✅ Covered | `Immunizations` (17 fields): CVX code, vaccine name, manufacturer, lot, administered amount/unit, refusal reason | Thorough |
| Vitals | ✅ Covered | `Vitals` (7 fields): meter name, unit, two value fields per vital per visit | Functional but minimal structure — uses name/value pattern |
| Lab results | ✅ Covered | `LabResults` (21 fields): SNOMED descriptions, reference ranges, result values, units, status, ordering provider | Good — includes multiple test identifiers |
| Imaging / diagnostic reports | ⚠️ Partial | Orders with `OrderTypeCode=1` (Order/Test) may include imaging; no dedicated imaging entity | No separate imaging results entity; imaging orders exist but results would be in documents |
| Procedures | ✅ Covered | `ProcedureList` (5 fields): CPT code, date, last reported date | Thin — only 5 fields, no descriptions or outcome data |
| Clinical notes / documents | ✅ Covered | `SOAPNotesIndex` + PDF exports; `DocumentsIndex` (12 fields) + original format documents; `DocumentAnnotations` (6 fields); `DocumentSignatures` (4 fields) | Strong — notes exported as readable PDFs, documents in original format, with annotations and signatures |
| Care plans / goals | ❌ Not covered | No care plan entity | MDVita is certified for (a)(12) family health history but care plan export is absent; may be embedded in SOAP notes |
| Orders / referrals | ✅ Covered | `Orders` (10 fields): referral, order/test, lab, text instruction types; `Referrals` (50 fields): detailed referral + prior auth tracking | Very strong — referrals include authorization tracking, payor certification, procedure/diagnosis details |
| Insurance / coverage | ✅ Covered | `PatientPlans` (24 fields): plan info, line of business, copay breakdowns, effective/termination dates | Thorough — includes multiple copay types, LOB detail |
| Claims / billing | ✅ Covered | `Claims` (85 fields): encounter and HCFA 1500 claims with procedure-level detail | Exceptionally thorough — 85 fields covering header and line-level claim data |
| Payments | ✅ Covered | `ClaimsInsurancePayments` (24 fields), `MemberCharges` (8 fields), `MemberPayments` (13 fields) | Strong — both insurer EOB payments and patient payments/charges |
| Consents / directives | ❌ Not covered | No consent or advance directive entity | Not clear if MDVita stores these as structured data; may be in documents |
| Patient communications / portal messages | ⚠️ Partial | `Emails` (12 fields): internal MDVita user emails linked to patients | Internal staff emails exported; no patient portal messages visible |
| Specialty-specific data | N/A | MDVita targets general/family practice | No specialty modules to export |

**Summary**: 14 of 17 applicable domains are covered (✅), 2 are partially covered (⚠️), and 1 is not covered (❌ care plans). The missing care plan entity is a minor gap — care plan content likely exists in SOAP notes (exported as PDFs). The export covers the product's core strength (billing/claims) in exceptional depth.

## 6. Documentation Quality

The documentation is **good to excellent** for a small vendor:

- **Completeness**: Every one of the 24 Parquet files is documented with a complete column-level data dictionary — 453 fields total, all with names, data types, and descriptions
- **Descriptions**: 100% of fields have human-readable descriptions, not just column names. Descriptions explain what each field means and reference related entities (e.g., "See Patients data file")
- **Data types**: Every field has a documented data type (Numeric, String, Boolean, DateTime, Date)
- **Coded values**: 21 fields include enumerated value definitions (e.g., `F=Female, M=Male, U=Unknown` for GenderCode)
- **Relationships**: Foreign key relationships are documented in descriptions (e.g., "Patient ID. See Patients data file"), though not in a formal schema notation
- **Missing elements**: No formal schema file (JSON Schema, XSD, etc.). No sample data files. No ERD or relationship diagram. Value sets for fields like `RaceDesc`, `Ethnicity`, and `LanguageDesc` are not enumerated (just typed as String)
- **Developer usability**: A developer could build an import from this documentation. The Parquet format is self-describing (includes schema in file metadata), which supplements the PDF documentation. The document structure is clear and consistent

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Comprehensive**

This export demonstrably covers the breadth of data domains MDVita stores. As a combined EHR + practice management system from a company that originated in claim adjudication, the billing/claims domain is the most important test — and it passes decisively. The Claims entity alone has 85 fields covering HCFA 1500 claims and encounters with procedure-level detail. Insurance payments, patient charges, and patient payments each have dedicated entities. Beyond billing, the export covers all major clinical domains (problems, medications, allergies, labs, immunizations, vitals, procedures), referrals with prior authorization tracking (50 fields), clinical notes as PDFs, uploaded documents in original format, insurance plans, appointments, provider networks, locations, internal communications, and document signatures/annotations. The only notable gap is care plans as a structured entity, but this is a minor omission given SOAP notes are fully exported. For a primary care practice management EHR, this is comprehensive.

**Axis 2 — Export approach: Purpose-built EHI export**

This is clearly a purpose-built export for (b)(10), not a repackaged clinical exchange. The telltale signs:
- **Apache Parquet format**: This is the vendor's native data model exported in a modern columnar format, not C-CDA or FHIR. No existing clinical exchange standard uses Parquet.
- **Billing/financial data**: Claims, insurance payments, member charges, and member payments are extensively documented — these would never appear in a (g)(10) FHIR API or C-CDA exchange.
- **Internal emails**: Patient-linked internal communications are exported — not part of any clinical exchange standard.
- **Document annotations and signatures**: Operational metadata about document review workflows is included.
- **24 distinct entity types**: Far beyond the scope of C-CDA sections or USCDI FHIR resources.
- **Dedicated documentation**: The 28-page PDF is specifically about the EHI export format, not repurposed API documentation.

### Key Findings

1. **Genuinely comprehensive billing coverage**: The export's strongest signal is its billing depth — 130+ fields across 4 billing entities (Claims, ClaimsInsurancePayments, MemberCharges, MemberPayments). The Claims entity at 85 fields is the largest in the export and covers both encounters and HCFA 1500 FFS claims at the procedure level. This reflects the vendor's claim adjudication heritage and goes far beyond USCDI scope.

2. **100% documentation coverage**: All 453 fields across 24 entities have names, types, and descriptions. This is unusually thorough for a small vendor. 21 fields include coded value enumerations.

3. **Purpose-built Parquet export**: The choice of Apache Parquet is distinctive — a modern, efficient columnar format that preserves the vendor's native data model. The export includes its own data model, not a mapping to FHIR or C-CDA.

4. **Referral/prior authorization depth**: The Referrals entity (50 fields) is notably thorough, covering not just referral tracking but prior authorization workflows, payor certification actions, and clinical notes receipt status — operational data relevant to value-based care practices.

5. **Document handling is well-designed**: SOAP notes are exported as machine-readable PDFs, documents in original format, with Azure Blob Storage URLs for download. The 14-day download window is a practical constraint but the mechanism is sound.

### Summary Stats

    Coverage:        Comprehensive
    Approach:        Purpose-built EHI export
    Export format:   Apache Parquet (structured data), PDF (SOAP notes), original format (documents)
    Entities:        24
    Fields:          453
    Descriptions:    100%
    Sample data:     No
    Bulk export:     Yes (appears to be all-patient bulk export)
    Domains covered: 14 of 17 applicable domains (✅), 2 partial (⚠️), 1 not covered (❌)

### Bottom Line

MDVita's EHI export is a well-executed, purpose-built export that covers the full breadth of what this combined EHR/practice management system stores. The export's strongest feature is its billing depth (130+ fields across 4 entities), reflecting the vendor's claim adjudication origins. With 24 Parquet files, 453 fully-documented fields, and coverage spanning clinical, billing, administrative, and communication domains, a patient or provider would get a substantively complete copy of their data. The only notable gap is care plans as a structured entity, and the 14-day document download window is a practical limitation.
