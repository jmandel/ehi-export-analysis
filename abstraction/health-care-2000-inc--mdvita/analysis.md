# EHI Export Analysis: Health Care 2000, Inc.

**Product**: MDVita  
**Analysis date**: 2026-02-15  
**CHPL IDs**: 11000 (CHPL Product Number: 15.04.04.2904.MDVi.27.02.1.221020)

## 1. Product Context

MDVita is an integrated EHR and practice management suite built by Health Care 2000, Inc., a small, family-owned healthcare IT company based in Palmetto Bay, Florida. Founded in 1997 as a claims adjudication company, the company launched its software division in 2000. MDVita serves "hundreds of medical centers" in South Florida, primarily value-based care providers in family/primary care operating under Medicare Advantage risk-based contracts.

The product combines:
- **EHR/Clinical**: Clinical notes (SOAP), problem lists, medications, allergies, vitals, lab results, immunizations, orders (medications, labs, imaging), clinical decision support, e-prescribing
- **Practice Management**: Scheduling, claims/encounters, revenue cycle management, billing management
- **Analytics**: MDVita Analytics add-on for financial reporting, claim counts, costs, utilization
- **Interoperability**: FHIR API, Direct messaging, C-CDA, patient portal (third-party component)
- **Public Health**: Immunization registry and syndromic surveillance reporting

The company's origin in claims adjudication makes billing/financial data a core strength. For (b)(10) assessment, the export should cover clinical records, billing/claims, insurance, referral authorization, and practice management data.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/MDVita_EHR_EHI_DataFormat.pdf` | 28-page EHI Export Data Format specification (Guide v1.2, Sep 2023; PDF created Jan 12, 2024). Documents 24 Parquet data files with field-level detail. **Primary and only artifact.** | ⭐⭐⭐ Highly informative |

This is a single-artifact analysis. The PDF is the only downloaded file and serves as the complete (b)(10) export documentation. It was downloaded directly from `https://www.hc2000inc.com/Pages/MDVita_EHR_EHI_DataFormat.pdf` with no access issues.

**Verification notes**: PDF confirmed at 28 pages (via `pdfinfo`), authored by Luis Martinez using Microsoft Word 2021. The prior agent's description was accurate on page count, access method, and general structure.

## 3. Export Mechanics

- **Format**: Apache Parquet for structured data, PDF for SOAP clinical notes, original format (PDF/XML/HTML/CSV/DOC/JPG/etc.) for uploaded documents. CSV reference files for document download URLs.
- **Mechanism**: Scheduled via MDVita application UI. Documentation states: "Please, use the MDVita User Guide for instructions how to schedule an EHI export." The user guide is available within the application but not publicly documented.
- **Single-patient vs bulk**: The document does not specify. The export structure (patient rosters, cross-file references by MemberID) implies bulk/multi-patient capability.
- **Document delivery**: SOAP Notes and Documents are delivered via time-limited Azure Blob Storage URLs (valid for 14 days). CSV reference files contain `FileName,FileDownloadURL` columns for automated download.
- **Access constraints**: No fees mentioned. The 14-day expiration on document download URLs is the only noted constraint.

## 4. Export Content: What's In It

The export produces **24 Apache Parquet data files** plus SOAP Note PDFs and uploaded documents in original format. Based on my parsing of the PDF data dictionary:

- **Total entities**: 24
- **Total fields**: 453
- **Fields with descriptions**: 453 (100%)
- **Fields with data types**: 453 (100%)
- **Value sets documented**: Yes, for all coded fields (gender, order types, claim types, referral urgency, result statuses, accident codes, bill frequency codes, EPSDT conditions, certification types, payment action codes, etc.)
- **Relationships documented**: Yes, cross-file references are consistently noted (e.g., "See Patients data file," "See ProviderPCPs data file") with join keys identified (MemberID/PatientID, CareEventID, PhysID, MemberPlanID, etc.)
- **Sample data**: No sample Parquet files provided. The PDF includes illustrative Azure Blob URLs.

**Note on field counts**: My automated parsing found higher counts than the prior agent's report for several entities (e.g., Patients: 31 vs claimed 27; ProviderNetwork: 21 vs claimed 18; PatientPlans: 24 vs claimed 21; Claims: 85 vs claimed 55+; Referrals: 50 vs claimed 35+). My counts were verified by manual inspection of the extracted text.

### Vendor's own content organization

The vendor organizes export files as "Raw Data" Parquet files, with SOAP Notes and Documents delivered by reference. The data dictionary (PDF sections 3–26) documents each file:

| Entity | Fields | Described | Types | Domain |
|---|---|---|---|---|
| Patients | 31 | 31 | yes | Demographics |
| ProviderNetwork | 21 | 21 | yes | Provider Reference |
| ProviderPCPs | 21 | 21 | yes | Provider Reference |
| Locations | 14 | 14 | yes | Provider Reference |
| PatientPlans | 24 | 24 | yes | Insurance / Coverage |
| Appointments | 20 | 20 | yes | Encounters / Visits |
| SOAPNotesIndex | 9 | 9 | yes | Clinical Notes |
| Orders | 10 | 10 | yes | Orders / Referrals |
| ProblemList | 10 | 10 | yes | Problems / Diagnoses |
| Allergies | 9 | 9 | yes | Allergies |
| MedicationList | 20 | 20 | yes | Medications |
| ProcedureList | 5 | 5 | yes | Procedures |
| DocumentsIndex | 12 | 12 | yes | Documents |
| LabResults | 21 | 21 | yes | Lab Results |
| Claims | 85 | 85 | yes | Claims / Billing |
| Referrals | 50 | 50 | yes | Orders / Referrals |
| Emails | 12 | 12 | yes | Communications |
| Immunizations | 17 | 17 | yes | Immunizations |
| Vitals | 7 | 7 | yes | Vitals |
| DocumentSignatures | 4 | 4 | yes | Documents |
| ClaimsInsurancePayments | 24 | 24 | yes | Claims / Billing |
| MemberCharges | 8 | 8 | yes | Claims / Billing |
| MemberPayments | 13 | 13 | yes | Payments |
| DocumentAnnotations | 6 | 6 | yes | Documents |

The full entity inventory with all field names, types, and descriptions is saved in `analysis/full-entity-inventory.json`.

### Domain breakdown

| Domain | Entities | Fields |
|---|---|---|
| Claims / Billing | 3 | 117 |
| Orders / Referrals | 2 | 60 |
| Provider Reference | 3 | 56 |
| Demographics | 1 | 31 |
| Insurance / Coverage | 1 | 24 |
| Documents | 3 | 22 |
| Lab Results | 1 | 21 |
| Encounters / Visits | 1 | 20 |
| Medications | 1 | 20 |
| Immunizations | 1 | 17 |
| Payments | 1 | 13 |
| Communications | 1 | 12 |
| Problems / Diagnoses | 1 | 10 |
| Allergies | 1 | 9 |
| Clinical Notes | 1 | 9 |
| Vitals | 1 | 7 |

The Claims/Billing domain is the deepest area (117 fields across 3 entities), consistent with the vendor's origin as a claims adjudication company. The Claims entity alone has 85 fields covering claim-level header data, procedure-level charges, EPSDT detail, and billing provider information in a denormalized structure.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The export covers the full clinical-to-financial lifecycle:

**Strongest areas:**
- **Claims/Billing** (117 fields): Extremely detailed. Claims entity captures encounter type, billing provider info, procedure-level charges with CPT codes, modifiers, place of service, drug NDC, EPSDT detail, and ICD diagnosis pointers. ClaimsInsurancePayments adds check-level and CPT-level payer payment detail including copay, deductible, coinsurance, and reason codes. MemberCharges and MemberPayments complete the financial picture with patient-side charges and payments including electronic payment details.
- **Referrals** (50 fields): Unusually deep referral/authorization tracking — certification types, payor action codes, service category codes, procedure-level authorization detail, and clinical notes receipt status. This reflects the product's Medicare Advantage/managed care focus.
- **Demographics** (31 fields): Comprehensive including employer info, transportation needs, language, race/ethnicity, and death information.

**Solid areas:**
- **Insurance/Coverage** (24 fields): Plan enrollment with line of business, copay breakdowns (ER, specialist, Rx brand/generic, X-ray), and effective/term dates.
- **Lab Results** (21 fields): Structured results with SNOMED codes, reference ranges, result statuses, and ordering provider.
- **Medications** (20 fields): Full prescription detail with NDC, SIG directions, route, frequency, dosage, and quantity.
- **Appointments** (20 fields): Scheduling data with transportation logistics and special needs — notable for a managed care product serving patients who may need transportation.
- **Immunizations** (17 fields): CVX codes, manufacturer, lot number, administered amount, and refusal reasons.

**Thinner areas:**
- **Clinical Notes**: Exported as SOAP Note PDFs (not structured data beyond the 9-field index), plus a text-based Comments field in SOAPNotesIndex. The actual note content is in the PDFs delivered by Azure Blob reference.
- **Vitals** (7 fields): Basic — vital name, unit of measure, and two value columns. No LOINC codes.
- **Procedures** (5 fields): Minimal — CPT code and dates only. Most procedure detail is captured in the Claims entity instead.
- **Documents**: Structure tracked via DocumentsIndex (12 fields), DocumentSignatures (4 fields), and DocumentAnnotations (6 fields). Actual documents delivered in original format by reference.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | `Patients` (31 fields): DOB, gender, SSN, name, address, employer, race, ethnicity, language, transportation, death info | Thorough |
| Encounters / visits | ✅ Covered | `Appointments` (20 fields) + `SOAPNotesIndex` (9 fields) + `Claims` (encounter-level data) | Well covered — appointments with status tracking, encounters linked to claims |
| Problems / conditions / diagnoses | ✅ Covered | `ProblemList` (10 fields): ICD-9/ICD-10/SNOMED codes, active/inactive/resolved status | Solid |
| Medications / prescriptions | ✅ Covered | `MedicationList` (20 fields): NDC, brand/generic names, SIG, route, frequency, dosage, quantity | Thorough |
| Allergies | ✅ Covered | `Allergies` (9 fields): NDC/SNOMED/UNII codes, drug/environmental/substance classes, active/inactive status | Solid |
| Immunizations | ✅ Covered | `Immunizations` (17 fields): CVX codes, manufacturer, lot number, administered amount, refusal reasons | Thorough |
| Vitals | ✅ Covered | `Vitals` (7 fields): vital name, unit, two value columns | Functional but thin — no LOINC codes |
| Lab results | ✅ Covered | `LabResults` (21 fields): SNOMED codes, reference ranges, result values, result statuses | Thorough |
| Imaging / diagnostic reports | ⚠️ Partial | Orders with `OrderTypeCode=1` (Order/Test) may include imaging orders. Documents in original format may include imaging reports. No dedicated imaging entity | Product supports imaging orders (a)(3) but no structured imaging results entity |
| Procedures | ✅ Covered | `ProcedureList` (5 fields) + procedure-level detail in `Claims` (CPT, charges, modifiers) | Adequately covered between ProcedureList and Claims |
| Clinical notes / documents | ✅ Covered | SOAP Notes as PDFs + `SOAPNotesIndex` (9 fields) + `DocumentsIndex` (12 fields) + documents in original format + `DocumentAnnotations` (6 fields) | Strong — both structured index and full document content |
| Care plans / goals | ❌ Not covered | No care plan entity in export | Unclear if product stores structured care plans; clinical notes may contain care plan information in SOAP format |
| Orders / referrals | ✅ Covered | `Orders` (10 fields) + `Referrals` (50 fields) | Exceptionally detailed referral tracking; orders cover referrals, tests, labs, text instructions |
| Insurance / coverage | ✅ Covered | `PatientPlans` (24 fields): plan enrollment, LOB, copay breakdowns, insurance company, effective/term dates | Thorough |
| Claims / billing | ✅ Covered | `Claims` (85 fields): encounter/HCFA 1500, procedure-level charges, modifiers, place of service, drug NDC, EPSDT, billing provider | Exceptionally detailed |
| Payments | ✅ Covered | `ClaimsInsurancePayments` (24 fields) + `MemberCharges` (8 fields) + `MemberPayments` (13 fields) | Full financial lifecycle — payer EOBs, patient charges, patient payments |
| Consents / directives | ⚠️ Partial | `Claims` has `ReleaseMedRec` and `PatSignSource` fields; no dedicated consent entity | Consent-adjacent fields exist in claims context but no standalone advance directive or consent tracking |
| Patient communications / portal messages | ⚠️ Partial | `Emails` (12 fields): internal MDVita user messages about patients. No patient portal message data | Internal staff communications exported; patient-facing portal messages not present. Product uses third-party portal, so portal data may reside outside MDVita |
| Specialty-specific (value-based care / managed care) | ✅ Covered | Referral authorization (50 fields), transportation logistics in Appointments, LOB in PatientPlans, EPSDT tracking in Claims | Strong — reflects Medicare Advantage managed care workflows |

**Summary**: 13 of 17 applicable domains are covered or well-covered. 3 are partially covered. 1 (care plans) is not covered, though the product may not store structured care plans.

## 6. Documentation Quality

**Strengths:**
- Every field in every entity has a name, data type, and natural-language description (453/453 = 100%)
- Coded fields include enumerated value sets with meanings (gender codes, order types, claim types, referral urgency, result statuses, accident codes, EPSDT conditions, certification types, payment action codes, etc.)
- Cross-file relationships are explicitly documented with join key references
- The Parquet format is self-describing (embedded schema), so the documentation supplements rather than replaces machine-readable structure
- Well-organized: each data file gets its own numbered section (3–26) with consistent table format

**Limitations:**
- No sample data files are provided
- No machine-readable schema file separate from the PDF (though Parquet files embed their own schema)
- No explicit cardinality documentation (required vs optional fields, one-to-many relationships)
- No changelog or version history beyond the version number (1.2)
- Export triggering instructions are only in the in-application user guide, not publicly documented
- No ERD or relationship diagram

**Developer usability**: A developer could build an import pipeline from this documentation. The Parquet format handles type fidelity natively, field descriptions clarify semantics, and coded value sets enable proper interpretation. The main gap is the lack of sample data to validate assumptions about record structure, especially for the denormalized Claims entity where procedure-level fields suggest one row per claim line.

## 7. Overall Assessment

### Classification

**Comprehensive native export**

This is a purpose-built (b)(10) export of MDVita's native data model. It exports 24 Parquet files covering the product's internal tables across clinical, billing, referral, and administrative domains. It is not a C-CDA or FHIR repackaging — the export uses the vendor's own entity/column names, internal identifier schemes, and denormalized structures. The breadth of coverage (demographics through claims through patient payments), the depth of documentation (453 fields, all described, all typed), and the choice of Apache Parquet as a format demonstrate genuine engineering effort.

### Key Findings

1. **Unusually strong billing/financial coverage**: 117 fields across Claims, ClaimsInsurancePayments, MemberCharges, and MemberPayments capture the full billing lifecycle — claims submission, payer EOB posting, and patient-side charges/payments. This is consistent with the vendor's origin as a claims adjudication company and is deeper than most (b)(10) exports.

2. **100% field documentation**: All 453 fields across 24 entities have names, data types, and descriptions. Coded fields include enumerated value sets. This is well above average for (b)(10) documentation.

3. **Apache Parquet is a technically strong format choice**: Parquet preserves data types natively, is self-describing, and is widely supported by data engineering tools (Python/pandas, R, Spark, DuckDB). This is an unusual and commendable choice that makes the export genuinely machine-consumable.

4. **Managed care workflow depth**: The 50-field Referrals entity with certification types, payor action codes, and authorization tracking reflects the product's Medicare Advantage/managed care focus. Transportation logistics in Appointments and EPSDT tracking in Claims further demonstrate specialty-appropriate coverage.

5. **Prior report field counts were consistently low**: The prior agent's report undercounted fields for multiple entities (Patients: 31 actual vs 27 claimed; ProviderNetwork: 21 vs 18; PatientPlans: 24 vs 21; Claims: 85 vs 55+; Referrals: 50 vs 35+). The actual export is more comprehensive than previously reported.

### Summary Stats

```
Classification:  Comprehensive native export
Export format:   Apache Parquet (structured data), PDF (clinical notes), original format (documents)
Model type:      Native database
Entities:        24
Fields:          453
Descriptions:    100%
Sample data:     No
Bulk export:     Unclear (likely yes based on structure)
Domains covered: 13 of 17 applicable domains (3 partial, 1 not covered)
```

### Bottom Line

MDVita's EHI export is one of the stronger (b)(10) implementations for a small vendor. A patient or provider would receive a comprehensive, well-documented copy of their clinical records, billing data, insurance information, referral authorizations, and financial transactions in a machine-readable format. The single biggest strength is the billing/financial depth (117 fields), which is often the weakest area for other vendors. The main gap is the absence of sample data files and the minor coverage gaps in imaging results and care plans.
