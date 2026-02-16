# EHI Export Analysis: CompuGroup Medical US

**Product**: CGM APRIMA v19  
**Analysis date**: 2026-02-16  
**CHPL ID**: 15.04.04.2700.Apri.19.01.1.221228

## 1. Product Context

CGM APRIMA is a comprehensive ambulatory EHR and practice management system serving 70+ medical specialties, from solo practitioners to multi-physician groups. The product lineage traces from iMedica (1998) → Aprima (2009) → eMDs (2019) → CompuGroup Medical (2020). It is purely ambulatory — no inpatient/hospital capabilities.

Key capabilities relevant to EHI completeness:
- **Clinical documentation**: Adaptive learning templates for 70+ specialties, structured data capture, clinical decision support, vitals, labs, immunizations, problem lists, medications, allergies, family/social history
- **E-prescribing**: EPCS, ePA, PDMP integration (via CGM PRESCRIBE / Surescripts)
- **Practice management / billing**: Integrated PM module with claims management, revenue cycle, eMEDIX clearinghouse integration for real-time eligibility, ERA posting, claim scrubbing
- **Patient portal**: Bilingual portal with secure messaging, appointment requests, refill requests, lab results
- **Scheduling**: Integrated appointment scheduling
- **Telehealth/RPM**: Virtual visits and remote patient monitoring
- **Lab ordering**: Electronic lab orders
- **Quality reporting**: MIPS, 60+ CQMs, UDS/UDS+ for FQHCs (CGM MEASURES)
- **Document workflow**: AI-enabled document management (CGM INDEX.AI)
- **Public health reporting**: Immunization registries, syndromic surveillance, cancer reporting, eCR

The product stores clinical, billing/financial, scheduling, insurance, prescribing, portal messaging, telehealth, and document management data. A complete EHI export should cover all of these patient-facing domains.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|----------|-------------|-----------------|
| `cgm-aprima-electronic-health-information-export-user-guide.pdf` (328 KB, 28 pages) | Primary (b)(10) EHI export documentation. Contains export instructions, ZIP structure description, and complete data dictionary for 22 CSV files with 389 fields. Dated Nov 2, 2023. | **Most informative** — the core artifact |
| `fhir-api-documentation-guide.pdf` (498 KB, 76 pages) | (g)(10) FHIR R4 API documentation covering standard US Core resources. Useful for comparison only. | Moderate — establishes the FHIR API scope for contrast |
| `certifications-expanded-screenshot.png` | Screenshot of CGM APRIMA product page certifications section showing EHI export documentation link | Low — confirms navigation path |
| `ehi-export-link-screenshot.png` | Closeup of EHI export documentation link | Low |
| `enrichment/ehi-data-dictionary.json` (64 KB) | Prior automated extraction of data dictionary into JSON. Contains minor parsing errors (identified and corrected in this analysis). | Moderate — used as base for corrected inventory |

## 3. Export Mechanics

- **Format**: ZIP file per patient containing:
  - 22 CSV files with structured tabular data
  - Image folders organized by encounter (e.g., `Radiology/`)
  - USCDI XML file (C-CDA) with bundled `EEHR_ChartViewer.exe` viewer
  - Complete Patient Chart PDF (full printout of all visit charts)
- **Mechanism**: In-application batch process. From Patient Demographics or Scheduler: Tools menu → Batch Process Management → EHI Export link. Three-step process documented on page 28 of the PDF.
- **Single-patient vs bulk**: Supports both individual patient export and "total population of patient records" export.
- **Access constraints**: Requires application access (provider/staff UI). No documented fees. No API-based export mechanism.

## 4. Export Content: What's In It

### Data dictionary scope

The EHI Export User Guide provides a field-level data dictionary for all 22 CSV files. Each field is documented with:
- Column heading name
- SQL data type with length (e.g., `char(255)`, `datetime`, `money`, `bit`, `uniqueidentifier`)
- Human-readable description (387 of 389 fields; 2 fields have no description)

**No value sets** are documented — coded fields (Gender Code, Race Code, Appointment Type Code, etc.) show the data type but not allowed values. **No explicit foreign key documentation** — relationships must be inferred from shared identifiers (PatientID, SuperbillID, AccountID, etc.). **No sample export files** are provided beyond a single 2-row CSV example on page 5.

### Verification notes

The prior enrichment extraction reported 383 fields. My independent PDF verification found 389 fields across 22 CSV files after correcting the following parsing errors:
- Audit Trail: was missing "Description" field (5 → 6 fields)
- Appointment Information: was missing "Appointment Type Code" field (16 → 17 fields)
- Eligibility: "Authorize Assignment" and "Payer Name" were merged; "OutNetwork Deductible" was missing (25 → 27 fields)
- Patient Ledger: "glDate" and "whoPaid" were merged; "lastInsurancePaymentAmount" was missing (58 → 60 fields)

### Vendor's own content organization

The vendor does not explicitly categorize the CSV files. I assigned categories based on content:

| Category | Files | Fields | Notes |
|----------|-------|--------|-------|
| Clinical | 11 | 163 | Medications, allergies, problems, results, vitals, immunizations, family/social/medical history, visit comments, referrals |
| Demographics | 4 | 80 | Patient demographics (39 fields), contacts, responsible party, employment |
| Billing / Financial | 1 | 60 | Patient Ledger — superbills, payments, adjustments, balances |
| Insurance | 2 | 49 | Patient insurance (22 fields) + eligibility inquiries (27 fields) |
| Administrative | 2 | 23 | Audit trail + appointment information |
| Care Team | 1 | 7 | Patient's providers with roles and specialties |
| Clinical Decision Support | 1 | 7 | HM rule responses and provider decisions |

### Entity detail

| CSV File | Fields | Described | Types | Category |
|----------|--------|-----------|-------|----------|
| Patient Ledger | 60 | 59 | yes | Billing / Financial |
| Patient Demographics | 39 | 39 | yes | Demographics |
| Eligibility | 27 | 26 | yes | Insurance |
| Active Medication | 23 | 23 | yes | Clinical |
| Patient Insurance | 22 | 22 | yes | Insurance |
| Responsible Party | 20 | 20 | yes | Demographics |
| Results | 19 | 19 | yes | Clinical |
| Appointment Information | 17 | 17 | yes | Administrative |
| Medical History | 17 | 17 | yes | Clinical |
| Immunization | 15 | 15 | yes | Clinical |
| Problem List | 15 | 15 | yes | Clinical |
| Vitals | 15 | 15 | yes | Clinical |
| Allergies | 14 | 14 | yes | Clinical |
| Contacts | 14 | 14 | yes | Demographics |
| Patient Referrals | 14 | 14 | yes | Clinical |
| Family History | 13 | 13 | yes | Clinical |
| Social History | 13 | 13 | yes | Clinical |
| Employment | 7 | 7 | yes | Demographics |
| Providers | 7 | 7 | yes | Care Team |
| Response Report | 7 | 7 | yes | Clinical Decision Support |
| Audit Trail | 6 | 6 | yes | Administrative |
| Visit Comments | 5 | 5 | yes | Clinical |

Full inventory: `analysis/entity-inventory-full.json` (389 field objects)  
Summary statistics: `analysis/entity-inventory-summary.json`

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The export is organized around 22 CSV files that map to the product's core data domains, plus supplementary image folders, a C-CDA XML file, and a complete chart PDF.

**Richest areas:**
- **Billing/Financial** (Patient Ledger, 60 fields): Exceptionally detailed. Includes superbill data (SuperbillID, status, procedure codes, 4 diagnosis codes, service dates), amounts (billed, due, paid, adjusted — split by insurance vs. patient), liability balances, payment dates, payer information, financial center, and service site. This is genuine billing data, not a summary.
- **Demographics** (80 fields across 4 files): Comprehensive patient demographics (39 fields including 4 phone numbers, 2 emails, language/race/ethnicity codes, AKA names, death date), plus contacts (14 fields with medical decisions/POA/HIPAA permissions), responsible party (20 fields), and employment history (7 fields).
- **Insurance** (49 fields across 2 files): Patient Insurance captures primary and secondary coverage. Eligibility goes deeper with deductibles, copays, coinsurance, network status, and eligibility request timestamps — this is operational insurance data beyond what a clinical summary provides.

**Adequate areas:**
- **Clinical** (163 fields across 11 files): Covers the expected ambulatory clinical domains — medications (23 fields with NDC, strength, formulation, route, frequency, duration, refills), allergies (14 fields with SNOMED codes), problems (15 fields with ICD-9/10), results (19 fields with codes, values, ranges, flags), vitals (15 fields), immunizations (15 fields with CPT, lot, manufacturer), medical/surgical history (17 fields with ICD codes), family history (13 fields), social history (13 fields as question/answer pairs), and referrals (14 fields).
- **Visit documentation**: Visit Comments (5 fields: PatientID, VisitDate, VisitId, Comment, Section) provides structured note content organized by section. The Complete Patient Chart PDF provides a human-readable full chart as fallback.

**Thinnest areas:**
- **Care Team** (Providers, 7 fields): Minimal — just provider name, role, specialty, and active dates.
- **Clinical Decision Support** (Response Report, 7 fields): Captures HM rule text and provider responses, but limited detail.
- **Audit Trail** (6 fields): Basic change tracking — who changed what, when, from where.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|--------|----------|-----------------|--------------|
| Demographics | ✅ Covered | `Patient Demographics` (39 fields), `Contacts` (14 fields), `Responsible Party` (20 fields), `Employment` (7 fields) | Thorough — includes 4 phone numbers, 2 emails, language, race, ethnicity, AKA names, death date, SSN |
| Encounters / visits | ⚠️ Partial | No dedicated encounters CSV. Visit data embedded in `Visit Comments` (VisitDate, VisitId), `Patient Ledger` (serviceDate), `Appointment Information` (StartDateTime). Complete Patient Chart PDF captures encounter narrative. | Product stores encounters; no dedicated encounter table with visit types, diagnoses, and providers per encounter. Data is distributed across other files. |
| Problems / conditions | ✅ Covered | `Problem List` (15 fields) with ICD-9/10 codes, onset/resolved dates | Solid |
| Medications / prescriptions | ✅ Covered | `Active Medication` (23 fields) with NDC, strength, formulation, route, frequency, duration, refills | Covers order data well. Does not export prescription transmission details (e-prescribing confirmations, prior auth records, PDMP results) — these are operational prescribing workflow data. |
| Allergies | ✅ Covered | `Allergies` (14 fields) with SNOMED codes | Solid |
| Immunizations | ✅ Covered | `Immunization` (15 fields) with CPT, lot, manufacturer, dosage, administration site | Solid |
| Vitals | ✅ Covered | `Vitals` (15 fields) with name, value, unit, position | Solid |
| Lab results | ✅ Covered | `Results` (19 fields) with lab codes, attribute names, values, reference ranges, abnormal flags, units, sample collected dates | Solid. No separate lab orders file — pending orders without results may not appear. |
| Imaging / diagnostic reports | ⚠️ Partial | Clinical images exported in encounter-organized folders (e.g., `Radiology/`). No structured imaging report data (no DICOM metadata, no radiology reports as structured data). May appear in Visit Comments or Complete Patient Chart PDF. | Product stores imaging orders and results; structured imaging data absent from CSV export |
| Procedures | ✅ Covered | `Medical History` (17 fields) covers medical/surgical procedures with ICD-9/10 and procedure codes. `Patient Ledger` includes procedure codes from superbills. | Adequate |
| Clinical notes / documents | ✅ Covered | `Visit Comments` (5 fields) provides structured note sections per visit. Complete Patient Chart PDF captures full clinical narrative. Clinical images exported in folders. | Notes are structured by section but thin (5 fields). The PDF provides comprehensive fallback. |
| Care plans / goals | ❌ Not covered | No dedicated care plan or goals CSV. May appear in Visit Comments or Complete Patient Chart PDF. | Product likely stores care plans (FHIR API supports CarePlan and Goal resources). Absence of structured export is a gap. |
| Orders / referrals | ⚠️ Partial | `Patient Referrals` (14 fields) covers referrals with procedure codes and dates. No dedicated orders CSV for lab/imaging orders. | Referrals are covered. Lab/imaging orders without results may not be captured. |
| Insurance / coverage | ✅ Covered | `Patient Insurance` (22 fields) with primary/secondary coverage, member/group IDs. `Eligibility` (27 fields) with deductible, copay, coinsurance details. | Thorough — includes operational eligibility data beyond basic coverage |
| Claims / billing | ✅ Covered | `Patient Ledger` (60 fields) with superbills, procedure codes, diagnosis codes, amounts billed/due/paid/adjusted, insurance vs. patient splits, liability balances, financial center, service site | Exceptionally detailed. This is genuine billing data. |
| Payments | ✅ Covered | `Patient Ledger` includes PaymentAmount, lastPatientPaymentDate, lastInsurancePaymentDate, lastPatientPaymentAmount, lastInsurancePaymentAmount, TotalPayment, InsurancePayment, PatientPayment, PayerCredits | Well covered within the ledger |
| Consents / directives | ⚠️ Partial | `Contacts` includes HIPAA Release and Power of Attorney flags. No dedicated advance directives or consent forms CSV. | Basic consent flags present but no structured consent document export |
| Patient communications / portal messages | ❌ Not covered | No portal messages, secure messaging, or patient communication data in export | Product has patient portal with secure messaging (CGM CONNECTION). This is a gap. |
| Specialty-specific data | ⚠️ Partial | Product supports 70+ specialties with adaptive templates. Visit Comments and Complete Patient Chart PDF likely contain specialty-specific structured data. No dedicated specialty-specific CSV files. | Specialty template data may be captured in visit notes but not as structured CSV |

## 6. Documentation Quality

**Strengths:**
- Field-level documentation for all 389 fields with SQL data types and human-readable descriptions
- 99.5% of fields have descriptions (387/389)
- Clear ZIP file structure documentation with naming conventions
- Consistent formatting across all 22 CSV definitions
- Well-organized 28-page PDF with table of contents

**Weaknesses:**
- **No value sets**: Coded fields (Gender Code, Race Code, Ethnicity Code, Appointment Type Code, Appointment Status Code, Marital Code, etc.) show only the data type, not allowed values. A developer cannot determine valid codes without sample data.
- **No relationship/foreign key documentation**: Fields like SuperbillID, AccountID, DepositUid, ResponsiblePartyUid have `uniqueidentifier` types suggesting relational linkage, but relationships are not documented.
- **No sample export**: One 2-row CSV snippet on page 5 is insufficient. No sample ZIP file, no realistic test data.
- **Minimal export instructions**: Three steps on the last page with no screenshots.
- **No versioning**: Single document dated Nov 2, 2023 with no revision history or changelog.

**Developer usability**: A developer could build a basic import from these docs. The field names are generally self-explanatory, types are precise (SQL types with lengths), and descriptions are clear. However, the lack of value sets, relationships, and sample data would require reverse-engineering from actual export files.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Comprehensive**

CGM APRIMA's export covers the breadth of an ambulatory EHR's designated record set. The Patient Ledger (60 fields) with detailed superbill, payment, and adjustment data demonstrates genuine billing coverage. Insurance eligibility data (27 fields with deductibles, copays, and coinsurance) goes beyond basic coverage information. Demographics (80 fields across 4 files), clinical data (163 fields across 11 files), and the Complete Patient Chart PDF provide thorough clinical and administrative coverage. The export addresses data domains that would never appear in a clinical exchange format: employment history, eligibility inquiry details, financial center data, liability balances, and payer credits.

Notable gaps exist for care plans/goals (no structured CSV), patient portal communications, and encounter-level data (no dedicated encounters file). These are real but relatively narrow gaps for an ambulatory product. The Complete Patient Chart PDF likely captures much of the care plan and encounter narrative data, though not in structured form.

**Axis 2 — Export approach: Purpose-built EHI export**

This is clearly a purpose-built (b)(10) export, distinct from the vendor's (g)(10) FHIR API:
1. **Separate mechanism**: Dedicated batch process in the application UI (Tools → Batch Process Management → EHI Export), not the FHIR API.
2. **Native format**: CSV files mapping to the product's internal database model, not FHIR resources or C-CDA sections.
3. **Beyond-USCDI content**: The Patient Ledger, Eligibility, Employment, Audit Trail, and Response Report CSVs contain data that has no representation in USCDI or US Core FHIR profiles.
4. **FHIR API is separate**: The FHIR API Documentation Guide (76 pages) documents standard US Core resources (AllergyIntolerance, CarePlan, CareTeam, Condition, etc.) — the EHI export covers substantially more data domains.
5. **The export includes a USCDI file alongside the CSVs**, explicitly distinguishing the clinical exchange portion from the full EHI dataset.

### Key Findings

1. **Genuine billing data export**: The 60-field Patient Ledger with superbill detail, procedure/diagnosis codes, payment splits (insurance vs. patient), adjustment tracking, and liability balances is among the more detailed billing exports seen. This alone demonstrates the vendor took (b)(10) seriously.

2. **389 fields across 22 CSV files, 99.5% documented**: The data dictionary covers all fields with SQL types and descriptions. The main documentation gaps are missing value sets and relationship documentation, not missing field definitions.

3. **Multi-format export is well-designed**: The combination of structured CSVs (machine-readable), USCDI XML (standards-based portability), Complete Patient Chart PDF (human-readable narrative), and clinical images provides both usability and completeness.

4. **Care plans, portal messages, and dedicated encounter data are absent**: These are the most significant gaps. The product stores care plans (the FHIR API supports CarePlan/Goal resources) and patient portal messages, but these don't appear as structured CSV exports. Encounter-level data must be reconstructed from visit comments, appointments, and ledger entries.

5. **No sample data or value sets**: A developer attempting to build an import would need to work from actual export files to determine coded field values and inter-table relationships. This limits practical usability despite the thorough field-level documentation.

### Summary Stats

```
Coverage:        Comprehensive
Approach:        Purpose-built EHI export
Export format:   CSV + images + USCDI XML + PDF (in ZIP)
Entities:        22 CSV files (+ images, XML, PDF)
Fields:          389
Descriptions:    99.5% (387/389 fields with descriptions)
Sample data:     No (one 2-row snippet only)
Bulk export:     Yes (total population export supported)
Domains covered: 14 of 18 applicable domains (4 partial, 2 not covered)
```

### Bottom Line

CGM APRIMA delivers a genuine, purpose-built EHI export with solid coverage of clinical, billing, insurance, and demographic data. The 60-field Patient Ledger and 27-field Eligibility file demonstrate real engagement with (b)(10) beyond clinical summaries. The primary gaps — missing structured care plans, patient portal messages, and a dedicated encounters file — are meaningful but don't undermine the overall comprehensiveness for an ambulatory product. A patient would get a substantially complete copy of their designated record set, with the Complete Patient Chart PDF serving as a human-readable safety net for any data not captured in the CSVs.
