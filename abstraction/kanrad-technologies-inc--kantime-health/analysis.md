# EHI Export Analysis: Kanrad Technologies Inc

**Product**: KanTime Health v1.0
**Analysis date**: 2026-02-15
**CHPL ID**: 15.04.04.3096.KanH.01.01.1.230118 (CHPL #11219)

## 1. Product Context

KanTime Health is a cloud-based enterprise EMR and agency management platform purpose-built for **post-acute care**: home health, hospice, palliative care, pediatric home care, private duty, and consumer-directed services. It is an all-in-one platform integrating clinical documentation, billing/revenue cycle management, HR/payroll, scheduling, e-prescribing (KRx), electronic visit verification (EVV), and business intelligence.

Key data domains the product stores about patients:
- **Clinical**: OASIS assessments (home health), HIS data (hospice), plans of care (auto-generated 485s), visit notes, vital signs, medications, e-prescriptions (via Surescripts), drug interactions, physician orders, care team records, bereavement records
- **Billing/Financial**: 837 claims, remittance/payment records, accounts receivable, denial tracking, payer information
- **Intake/Referral**: Referral tracking, eligibility verification, prior authorizations
- **Scheduling**: Visit schedules, caregiver assignments, EVV data (GPS/telephony)
- **HR/Payroll**: Employee records, credentials, timesheets, payroll data

The product serves 912,000+ patients and 210,000+ users, processing $12.9B in claims. The (b)(10) EHI export should cover all patient-facing clinical and billing data stored across these modules.

## 2. Artifacts Reviewed

| Artifact | Description | Size | Informativeness |
|---|---|---|---|
| `EHI_Tool_Documentation.pdf` | The registered (b)(10) export documentation. A 1-page PDF containing exactly 5 sentences. States clinical data exports as C-CDA 2.1 and billing data as CSV/XLSX/PDF. No data dictionary, no field definitions, no schema, no instructions. | 1 page, 42,570 bytes | **Low** — minimal content |
| `KanTime_Patient_API.pdf` | REST API documentation for retrieving patient clinical data as C-CDA XML. Includes authentication flow, patient search, CCDA retrieval endpoints, curl examples, and a sample C-CDA response. | 14 pages, 255,054 bytes | **Medium** — documents the API mechanism for clinical export but not the data content |
| `SmartOnFHIRAPIDoc.pdf` | SMART on FHIR API documentation for (g)(10) compliance. Lists ~23 FHIR resource types. **Not** the (b)(10) EHI export. | 66 pages, 685,961 bytes | **Contextual only** — separate certification criterion |
| `fhir-base-urls-1.json` | FHIR R4 endpoint Bundle with 2 organization endpoints. Part of (g)(10). | 3,719 bytes | **Contextual only** |

The two EHI-relevant artifacts (`EHI_Tool_Documentation.pdf` and `KanTime_Patient_API.pdf`) total 15 pages. There are no data dictionaries, no sample export files, no schemas, and no billing export documentation beyond the statement that it exists.

## 3. Export Mechanics

**Clinical data export:**
- **Format**: C-CDA 2.1 Release 2 (USCDI v1)
- **Mechanism**: REST API (`KanTime Patient API`)
  - Authenticate via Basic Auth → receive JWT token
  - Search patients by MRN, DOB, first/last name (returns up to 30 results)
  - Retrieve full C-CDA per patient, or request specific C-CDA sections
  - Optional date range filtering (`startDate`/`endDate` parameters)
- **Single-patient**: Yes — API is per-patient by MRN
- **Multi-patient / bulk**: The EHI PDF mentions "Single or Multi-Patient EHI Export" but provides no details on bulk mechanism. The documented API is per-patient only.

**Billing data export:**
- **Format**: CSV, XLSX, or PDF
- **Mechanism**: Undocumented. The EHI PDF states "the billing user role will facilitate the process for users to extract patient claims and payments in CSV format export." No API endpoint, no UI instructions, no screenshots.
- **Single-patient vs bulk**: Unclear
- **Access constraints**: Requires "EHI export authorization" user role (clinical) and "billing user role" (billing)
- **Fees**: Not mentioned

## 4. Export Content: What's In It

### Clinical export (C-CDA)

The Patient API documents 22 retrievable C-CDA sections (plus an "all" option). These are standard C-CDA sections, not vendor-specific extensions:

| C-CDA Section | API Parameter |
|---|---|
| Patient Demographics | `demographics` |
| Care Team | `careteam` |
| Allergies and Intolerances | `allergies` |
| Assessment | `assessments` |
| Encounters | `encounters` |
| Functional Status | `functionalstatus` |
| Goals | `goals` |
| Health Concerns | `healthconcerns` |
| Immunizations | `immunizations` |
| Medical Equipment | `medicalequipment` |
| Medications | `medications` |
| Mental Status | `mentalstatus` |
| Plan of Treatment | `planoftreatment` |
| Problem | `problem` |
| Procedures | `procedures` |
| Reason for Referral | `reasonforreferral` |
| Results | `results` |
| Social History | `socialhistory` |
| Vital Signs | `vitalsigns` |
| Consultation Note | `consultationnote` |
| Progress Note | `progressnote` |
| History and Physical Note | `historyandphysicalnote` |

The sample C-CDA response in the Patient API PDF is a standard "Summary of Care" document (`LOINC 34133-9`). The sample for the `careteam` section-specific query returns a C-CDA with an empty `<structuredBody />`, suggesting sections may return no data when unpopulated.

**There is no data dictionary for the C-CDA content.** The documentation lists section names but does not describe what fields/data elements appear within each section, what coded value sets are used, or whether KanTime includes any vendor-specific extensions beyond standard C-CDA.

The Patient API search response includes 18 demographic fields (MRN, name, DOB, gender, address, phone numbers, SSN, email, marital status). These are the only individually enumerated fields in any artifact.

### Billing export

**Zero documentation exists** for the billing export beyond the statement in `EHI_Tool_Documentation.pdf` that "the billing user role will facilitate the process for users to extract patient claims and payments in CSV format export" and that formats include CSV, XLSX, or PDF.

- No field names listed
- No column definitions
- No sample files
- No schema
- No instructions for how to access or perform the export
- No indication of what "claims and payments" includes (e.g., claim lines, denial reasons, payer details, remittance data)

### Vendor's own content organization

KanTime organizes the export into exactly two categories:

| Category (vendor's) | Export Format | Entities/Sections | Fields Documented | Descriptions |
|---|---|---|---|---|
| Clinical data | C-CDA 2.1 | 22 C-CDA sections | 0 (standard C-CDA) | N/A — no field-level documentation |
| Billing data | CSV/XLSX/PDF | Unknown | 0 | None |

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor describes exactly two export tracks:

1. **Clinical data via C-CDA**: Covers 22 standard C-CDA sections aligned with USCDI v1. This represents the standard clinical summary data classes — demographics, problems, medications, allergies, immunizations, vitals, procedures, results, clinical notes, care plans, goals, etc. These are generic C-CDA sections, not KanTime-specific data structures.

2. **Billing data via CSV/XLSX/PDF**: Described only as "patient claims and payments." Completely undocumented — no field definitions, no samples, no schema. It's impossible to assess depth or completeness.

**Critical observation**: KanTime is a post-acute care platform whose core differentiating data includes OASIS assessments, Hospice Item Sets (HIS), auto-generated 485 plans of care, EVV data, detailed visit documentation, referral/intake tracking, authorization records, and specialized hospice features (bereavement, volunteer tracking). **None of this specialty-specific clinical data is addressed in the export documentation.** The C-CDA sections are generic clinical summary sections that cannot represent these post-acute-specific data structures.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | C-CDA `demographics` section; Patient API search returns 18 fields | C-CDA demographics are standard; KanTime-specific fields (e.g., referral source, admission type, care type) are not documented |
| Encounters / visits | ⚠️ Partial | C-CDA `encounters` section | Standard C-CDA encounters; detailed visit documentation (POC notes, clock-in/out, EVV) not represented |
| Problems / conditions | ✅ Covered | C-CDA `problem`, `healthconcerns` sections | Standard coverage via C-CDA |
| Medications / prescriptions | ⚠️ Partial | C-CDA `medications` section | Standard medication list; e-prescribing workflow data (KRx module, Surescripts history) likely not included |
| Allergies | ✅ Covered | C-CDA `allergies` section | Standard coverage via C-CDA |
| Immunizations | ✅ Covered | C-CDA `immunizations` section | Standard coverage via C-CDA |
| Vitals | ✅ Covered | C-CDA `vitalsigns` section | Standard coverage via C-CDA |
| Lab results | ✅ Covered | C-CDA `results` section | Standard coverage; lab ordering may be limited for home health/hospice |
| Procedures | ✅ Covered | C-CDA `procedures` section | Standard coverage via C-CDA |
| Clinical notes / documents | ⚠️ Partial | C-CDA `consultationnote`, `progressnote`, `historyandphysicalnote` sections | Only 3 note types; specialty visit notes, OASIS documentation, HIS documentation not addressed |
| Care plans / goals | ⚠️ Partial | C-CDA `planoftreatment`, `goals` sections | Generic C-CDA plan of treatment ≠ KanTime's auto-generated 485 plans of care |
| Orders / referrals | ⚠️ Partial | C-CDA `reasonforreferral` section | Reason for referral only; physician order tracking, referral management data not addressed |
| Insurance / coverage | ❌ Not covered | Not in export documentation | Product manages payer/authorization data; not mentioned in export |
| Claims / billing | ⚠️ Partial | EHI PDF mentions "patient claims and payments" in CSV/XLSX/PDF | Exists in name only — completely undocumented; impossible to assess completeness |
| Payments | ⚠️ Partial | Mentioned alongside claims | Same as above — undocumented |
| Consents / directives | ❌ Not covered | No evidence in export | Product likely captures consent for care; not addressed |
| Specialty: OASIS assessments | ❌ Not covered | Not mentioned in any artifact | **Major gap** — OASIS is core to home health clinical documentation in KanTime |
| Specialty: HIS (Hospice Item Set) | ❌ Not covered | Not mentioned in any artifact | **Major gap** — HIS is core to hospice clinical documentation in KanTime |
| Specialty: 485 Plans of Care | ❌ Not covered | Not mentioned (C-CDA `planoftreatment` is generic) | **Major gap** — auto-generated 485s are a key product feature |
| Specialty: EVV data | ❌ Not covered | Not mentioned in any artifact | Product has integrated EVV (GPS/telephony); not in export |
| Specialty: Bereavement (hospice) | ❌ Not covered | Not mentioned | Product has bereavement management module; not in export |

**Coverage summary**: Of 20 applicable domains, 5 have standard C-CDA coverage, 7 are partial (either C-CDA sections that likely don't capture the full KanTime data or mentioned but undocumented), and 8 are not covered at all. The most significant gaps are the complete absence of KanTime's specialty post-acute care data (OASIS, HIS, 485s, EVV, bereavement) — the very data that differentiates this product from a generic EMR.

## 6. Documentation Quality

**Overall: Extremely poor.**

- The core EHI document (`EHI_Tool_Documentation.pdf`) is 1 page with 5 sentences. It is among the most minimal (b)(10) documentation possible.
- **No data dictionary exists** — not for clinical data, not for billing data, not for anything.
- **No sample files** are provided for any export format.
- **No schema** (XSD, JSON Schema, CSV headers) is provided.
- **No user instructions** explain how to perform the export within the KanTime application.
- The Patient API PDF (14 pages) is the most substantive artifact, but it documents the API mechanism (authentication, curl commands, endpoints), not the data content. It tells you how to call the API, not what you'll get back.
- The API documentation does include sample JSON responses for patient search (18 fields) and a partial sample C-CDA, providing minimal evidence of data structure.
- **A developer could not build a meaningful import** from these docs. For clinical data, they would need to parse standard C-CDA (which is documented elsewhere by HL7, not by KanTime). For billing data, they would have no idea what columns or format to expect.
- There are no machine-readable artifacts: no schemas, no OpenAPI/Swagger spec, no sample data files.

## 7. Overall Assessment

### Classification

**Minimal/stub**

The export documentation is too thin to meaningfully assess export completeness. What can be assessed — a C-CDA clinical summary plus an undocumented billing CSV — covers only a fraction of what KanTime Health stores. The C-CDA approach inherently cannot represent KanTime's specialty post-acute care data (OASIS, HIS, 485s, EVV), and the billing export is documented only by its existence, not its contents.

### Key Findings

1. **The entire EHI export documentation is 5 sentences.** `EHI_Tool_Documentation.pdf` is a 1-page, 42KB PDF that names formats (C-CDA, CSV/XLSX/PDF) but provides no data dictionary, no field definitions, no schema, and no instructions. This is a compliance checkbox, not a data portability effort.

2. **Clinical export is a standard C-CDA repackaging.** The 22 C-CDA sections map directly to USCDI v1 clinical data classes — the same clinical summary available through any (b)(1)/(b)(2) transitions-of-care export. This is not a native data model export; it's the existing C-CDA capability relabeled as "(b)(10)."

3. **KanTime's core differentiating data is entirely absent.** OASIS assessments, Hospice Item Sets, auto-generated 485 plans of care, EVV data, and bereavement management — the specialty post-acute care data that defines KanTime — are not mentioned in any export artifact. These are critical clinical data used to make care decisions and cannot be represented in standard C-CDA sections.

4. **Billing export is acknowledged but completely undocumented.** The EHI PDF states billing data can be exported as CSV/XLSX/PDF, but provides zero information about what fields, columns, or records are included. No sample files, no schema, no field list.

5. **No bulk export mechanism is documented.** The Patient API is per-patient (by MRN). While the EHI PDF mentions "Multi-Patient EHI Export," there are no details on how this works.

### Summary Stats

```
Classification:  Minimal/stub
Export format:   C-CDA 2.1 (clinical), CSV/XLSX/PDF (billing, undocumented)
Model type:      Standard projection (C-CDA) + undocumented billing
Entities:        0 native entities (22 C-CDA sections, no data dictionary)
Fields:          18 (patient search only; C-CDA fields not enumerated)
Descriptions:    N/A (no data dictionary)
Sample data:     No (partial C-CDA sample in API doc only)
Bulk export:     Unclear (mentioned but not documented)
Domains covered: 5 of 20 applicable domains (standard C-CDA only)
```

### Bottom Line

KanTime Health's EHI export is a minimal compliance stub. The clinical export is a standard C-CDA clinical summary — the same data already available through transitions-of-care exports — while the billing export is acknowledged in one sentence but completely undocumented. The product's core specialty data (OASIS, HIS, 485 plans of care, EVV) is entirely absent from the export, representing a significant gap for a post-acute care platform where these assessments and records are central to patient care decisions. A patient or provider requesting their full record from KanTime would receive a generic clinical summary and an unknown billing extract, missing the vast majority of the specialty clinical data the system actually stores.
