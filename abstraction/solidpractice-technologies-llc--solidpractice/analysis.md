# EHI Export Analysis: SolidPractice Technologies, LLC

**Product**: SolidPractice v2.0
**Analysis date**: 2026-02-15
**CHPL ID**: 15.05.05.3095.SOLP.01.00.1.211227 (CHPL #10763)

## 1. Product Context

SolidPractice is a desktop-based ambulatory EHR/EMR from a micro-vendor (SolidPractice Technologies, LLC / Innovative Medical Practice Solutions) in Sarasota, Florida. It targets small private medical practices and is certified as a Complete EHR (2015 Edition Cures Update) across 33 ONC criteria. The product's signature feature is real-time voice dictation for clinical documentation.

Based on vendor website and certification data, SolidPractice stores:

- **Patient demographics** including emergency contacts
- **Clinical notes/encounter documentation** — voice-dictated notes are the core feature
- **Medications/prescriptions** via NewCrop/SureScripts e-prescribing integration
- **Problem lists, allergies, vitals, immunizations, procedures**
- **Lab results and imaging orders/reports** via electronic lab integration
- **Referral letters** (automated generation)
- **Insurance/guarantor information**
- **Appointment/scheduling data**
- **Billing integration** — E/M coding support; unclear whether full billing is built in or handled externally
- **Custom data fields** — the product supports custom field creation
- **Patient portal data** — certified for (e)(1) view-download-transmit
- **C-CDA/transitions of care documents**

The billing scope is ambiguous: the vendor's feature page says "billing system integration" which could mean an external billing system rather than built-in claims management.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `SolidPractice-b10-exportable-data-content.pdf` (29 KB, 3 pages) | Core b(10) documentation: a spreadsheet listing 87 exportable data elements with names, descriptions, and export format assignments. Created 2024-03-27 from Excel. | **Primary artifact** — defines the complete scope of the export |
| `SolidPractice-Data-Access-API.pdf` (14.5 KB, 6 pages) | Data Access API documentation for the CCD XML export endpoint. Describes HTTP API with authentication, parameters, 16 selectable clinical sections, and JSON response format. Dated 2022-12-06. | **Supplementary** — explains the CCD XML export mechanism |

Only two artifacts were collected; both are PDFs. No sample data files, schemas, or machine-readable documentation exist.

## 3. Export Mechanics

- **Format(s)**: Three export formats are documented, each used for different data elements:
  - **CCD XML** (via HTTP API) — 43 elements (demographics, clinical data)
  - **JSON** — 42 elements (labs, insurance, guarantor, appointments, billing/receipts)
  - **Computable PDF** — 2 elements (imaging reports, uploaded documents)
  - Each element is assigned to exactly one format; no element is available in multiple formats.
- **Mechanism**: The CCD XML export uses an HTTP API endpoint (`/CCD/ExportPatientData`) with token-based authentication. The mechanism for JSON and Computable PDF exports is not documented.
- **Scope**: Single-patient export. The API requires a `patientId` parameter. No bulk/batch export capability is documented.
- **Access constraints**: API token required (obtained from EMR Setup section). No fees are mentioned.
- **Date filtering**: The CCD XML API supports optional `from`/`to` date range parameters and section-level toggles for 16 clinical data sections.

## 4. Export Content: What's In It

The export is documented as a flat list of 87 data elements (not a relational data model). All 87 elements have brief text descriptions. No data types, value sets, cardinality, relationships, or foreign keys are documented.

### Column assignment methodology

The column assignments in the b(10) PDF were verified using `pdftotext -bbox` coordinate analysis, which extracts exact x-positions for each "X" mark and compares them against the column headers' positions. The headers are positioned at: Computable PDF Export (x=455–556), CCD XML Export (x=565–635), JSON (x=667–691). X marks appear at three distinct x-positions: ~597 (CCD XML), ~676 (JSON), and ~503 (Computable PDF). Details in `analysis/parse_b10_elements.py`.

**Note**: The prior collection report incorrectly stated that "most data elements are available in both Computable PDF Export and CCD XML Export formats." In fact, each element is marked for exactly one format, and the distribution is CCD XML (43), JSON (42), Computable PDF (2).

### Vendor's own content organization

The 87 data elements span these categories:

| Category | Elements | Format | Element Range |
|---|---|---|---|
| Demographics | 29 | CCD XML | #1–29 (Patient ID, name, DOB, gender, race, ethnicity, marital status, language, contact method, address, phone, email, emergency contact) |
| Medications | 1 | CCD XML | #30 (Prescriptions — current and past) |
| Pharmacy | 5 | CCD XML | #31–35 (Preferred pharmacy name, address, city, state, zip) |
| Social History | 2 | CCD XML | #36–37 (Smoking status, social history) |
| Immunizations | 1 | CCD XML | #38 |
| Problems | 1 | CCD XML | #39 (Problem List) |
| Procedures | 1 | CCD XML | #40 |
| Vitals | 1 | CCD XML | #41 |
| Allergies | 1 | CCD XML | #42 |
| Providers/Care Team | 2 | CCD XML + JSON | #43 Primary Provider (CCD XML), #44 Providers List (JSON) |
| Labs & Imaging | 3 | JSON + PDF | #45 Lab Results (JSON), #46 Lab/Imaging Orders (JSON), #47 Imaging Reports (Computable PDF) |
| Uploaded Documents | 1 | Computable PDF | #48 (Files uploaded to patient chart — insurance cards, consent forms, etc.) |
| Insurance | 8 | JSON | #49–56 (Primary and secondary carrier name, subscriber ID, group no, plan name) |
| Guarantor | 9 | JSON | #57–65 (Guarantor name, address, phone, relationship, city, state, zip) |
| Appointments | 6 | JSON | #66–71 (Type, date/time, status, description, provider, duration) |
| Billing/Receipts | 16 | JSON | #72–87 (Service date, copay, deductible, outstanding balance with claim#, credit, amount, patient name/address, bill date, account no, amount paid, transaction no, payment method, billing facility info) |

**Key observations**:
- Clinical data items (30–43) are each represented as a single element (e.g., "Problem List" is one element, not broken into individual fields like diagnosis code, onset date, status). These are likely CCD sections exported as XML blocks rather than decomposed fields.
- The 16 billing/receipt elements are the most granular category, with individual fields for copay, deductible, balance, payment method, etc.
- Demographics (29 elements) are the most thoroughly decomposed, with individual fields for each address component and emergency contact field.
- Labs (#45–46) and Providers List (#44) use lowercase "x" marks in the JSON column, suggesting possible inconsistency or uncertainty in the documentation.

### Data Access API sections

The CCD XML API offers 16 toggleable clinical sections, several of which go beyond what's listed in the 87-element b(10) table:

| API Section | In b(10) list? |
|---|---|
| allergiesAndIntolerances | Yes (#42) |
| medications | Yes (#30) |
| problem | Yes (#39) |
| procedures | Yes (#40) |
| immunizations | Yes (#38) |
| vitalSigns | Yes (#41) |
| socialHistory | Yes (#37) |
| results | Yes (#45) |
| medicalEquipment | **No** — not listed as a b(10) element |
| assessment | **No** |
| planOfTreatment | **No** |
| reasonForReferral | **No** |
| goals | **No** |
| healthConcerns | **No** |
| functionalStatus | **No** |
| cognitiveStatus | **No** |

Eight API sections (medicalEquipment, assessment, planOfTreatment, reasonForReferral, goals, healthConcerns, functionalStatus, cognitiveStatus) are available via the CCD XML API but are **not** enumerated in the b(10) data element list. This suggests the actual export may include more data than the 87 elements documented — or these sections may be empty for most patients.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The export covers six broad areas:

1. **Demographics** (29 elements): The deepest category. Individual fields for name, DOB, gender, race, ethnicity, contact info, and emergency contacts. Thorough for basic patient identity.

2. **Clinical data** (13 elements, items 30–42): Each clinical domain is a single element (e.g., "Problem List," "Vitals," "Allergies"). These are almost certainly CCD XML sections rendered as complete blocks rather than individual fields. The CCD XML API additionally offers 8 sections not in the b(10) list (assessment, care plans, goals, referrals, etc.), adding undocumented clinical depth.

3. **Insurance** (8 elements): Primary and secondary carrier with subscriber ID, group number, and plan name. Basic but adequate for insurance identification.

4. **Guarantor** (9 elements): Name, address, phone, relationship. Standard guarantor fields.

5. **Appointments** (6 elements): Type, date/time, status, description, provider, duration. Covers appointment scheduling basics.

6. **Billing/Receipts** (16 elements): Service dates, copay, deductible, outstanding balance, payment method, billing facility info. Notably, this is receipt-level data (payments and balances) — not claims-level data (no CPT/ICD codes, no E/M levels, no charge amounts tied to procedures).

**Thinnest areas**: Clinical data is paradoxically the thinnest in terms of documentation granularity — each domain is one element with a terse description. The actual data depth depends entirely on what the CCD XML contains, which is undocumented.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | 29 elements (#1–29): name, DOB, gender, race, ethnicity, language, address, phone, email, emergency contacts | Thorough |
| Encounters / visits | ⚠️ Partial | Appointments (#66–71) provide scheduling data; CCD XML API has `assessment` section. No explicit encounter/visit records | Appointment data exists but encounter documentation is thin |
| Problems / conditions | ✅ Covered | #39 Problem List (CCD XML); API `problem` section | Single element; detail depends on CCD content |
| Medications / prescriptions | ✅ Covered | #30 Prescriptions — current and past (CCD XML); #31–35 Preferred Pharmacy | Adequate |
| Allergies | ✅ Covered | #42 Allergies (CCD XML); API `allergiesAndIntolerances` | Single element |
| Immunizations | ✅ Covered | #38 Immunization history (CCD XML); API `immunizations` | Single element |
| Vitals | ✅ Covered | #41 Vitals (CCD XML); API `vitalSigns` | Single element |
| Lab results | ✅ Covered | #45 Lab Results (JSON); API `results` section | Single element |
| Imaging / diagnostic reports | ✅ Covered | #46 Lab/Imaging Orders (JSON); #47 Imaging Reports (Computable PDF) | Imaging reports as "Computable PDF" |
| Procedures | ✅ Covered | #40 Procedures (CCD XML); API `procedures` | Single element |
| Clinical notes / documents | ❌ Not covered | No data element for encounter notes, progress notes, dictated text, or H&P notes | **Critical gap**: Voice-dictated clinical notes are SolidPractice's signature feature and core data type. Their absence is the most significant omission. |
| Care plans / goals | ⚠️ Partial | Not in b(10) list, but API has `planOfTreatment`, `goals`, `healthConcerns` sections | Available via API but undocumented in b(10) |
| Orders / referrals | ⚠️ Partial | #46 Lab/Imaging Orders (JSON); API has `reasonForReferral` section. No referral letters in export | Lab/imaging orders present; referral letters absent |
| Insurance / coverage | ✅ Covered | #49–56: Primary and secondary carrier, subscriber ID, group no, plan name (JSON) | Basic identification only; no coverage details, eligibility, or benefits |
| Claims / billing | ⚠️ Partial | #72–87: Receipt-level data (copay, deductible, balance, payment method). No CPT/ICD codes, no E/M levels, no charge line items | Receipt data only; no claims-level detail. Billing integration may be external, limiting what SolidPractice stores |
| Payments | ✅ Covered | #72–87 include amount paid, transaction number, payment method | Covered via receipt data |
| Consents / directives | ⚠️ Partial | #48 Uploaded Documents includes "consent forms." No structured consent records | Only as uploaded file attachments |
| Patient communications | ❌ Not covered | No patient portal messages or communication records | Product has a patient portal (certified for (e)(1)); messages are not exported |
| Uploaded documents | ✅ Covered | #48: Files uploaded to patient chart (Computable PDF) | Mechanism unclear — does "Computable PDF" mean the files themselves are exported? |
| Specialty-specific data | N/A | No specialty features identified | General ambulatory EHR |
| Custom fields | ❌ Not covered | Product supports custom data field creation; none appear in export | Gap if custom fields contain patient data |

## 6. Documentation Quality

**Strengths**:
- The b(10) data element list is enumerated and complete with 87 named elements, each with a brief description.
- The Data Access API document provides enough detail for a developer to make CCD XML API calls (endpoint, parameters, auth, response format, error examples).
- All 87 elements have descriptions (100%).

**Weaknesses**:
- **No data types**: No specification of formats (date formats, string lengths, coding systems) for any element.
- **No value sets**: Coded fields (Gender, Race, Ethnicity, Marital Status, Appointment Status, Payment Method) have no enumerated values or code system references.
- **No relationships**: No documentation of how records relate (e.g., how receipts link to appointments, how orders link to results).
- **No sample data**: No sample export files in any format.
- **No machine-readable artifacts**: No JSON schema, XSD, OpenAPI spec, or structured documentation.
- **Undocumented formats**: The JSON export format for 42 elements is completely undescribed — no structure, no schema, no examples. The "Computable PDF Export" for 2 elements is equally opaque.
- **Clinical items lack granularity**: Items like "Problem List" and "Vitals" are single elements, so it's impossible to know what fields (diagnosis codes, onset dates, blood pressure vs. heart rate) are included without sample data.
- **Inconsistency between b(10) list and API**: The CCD XML API exposes 16 clinical sections, but the b(10) list only covers 8 of them. The status of the other 8 sections (assessment, planOfTreatment, goals, etc.) in the export is unclear.

A developer could call the CCD XML API based on the documentation, but could not parse, validate, or import the JSON or PDF exports without additional information. Even for CCD XML, the lack of value sets and coding system references would require reverse-engineering from actual export data.

## 7. Overall Assessment

### Classification

**Partial native export**: The export uses a mix of CCD XML (for clinical data), JSON (for administrative/financial data), and Computable PDF (for documents) — suggesting some attempt to export native data beyond just clinical summaries. However, the most critical data domain (clinical notes/encounter documentation) is missing, the documentation is thin, and the actual structure of the JSON and PDF exports is entirely undocumented.

### Key Findings

1. **Clinical notes — the product's core feature — are absent from the export.** SolidPractice's signature capability is voice-dictated clinical documentation, yet no encounter notes, progress notes, or dictated text appear in the 87 exported data elements. This is the single most significant omission.

2. **The export uses three formats, each for different data elements — not three representations of the same data.** CCD XML covers demographics and clinical data (43 elements), JSON covers administrative/financial data (42 elements), and Computable PDF covers imaging reports and uploaded documents (2 elements). Each element appears in exactly one format. The prior collection report's claim that "most data elements are available in both formats" is incorrect (verified via `pdftotext -bbox` coordinate analysis).

3. **Receipt-level billing, not claims-level billing.** The 16 billing/receipt elements cover payment amounts (copay, deductible, balance, amount paid) but contain no CPT/ICD codes, E/M levels, or procedure-linked charges. This is receipt data, not claims data.

4. **The CCD XML API documents 8 clinical sections not listed in the b(10) export.** Assessment, plan of treatment, goals, reason for referral, health concerns, functional status, cognitive status, and medical equipment are available via the API but absent from the official data element list, creating ambiguity about what's actually exported.

5. **No sample data, no schemas, no machine-readable documentation.** The entire export is documented in two PDFs totaling 43.7 KB. A developer would need to reverse-engineer the JSON and PDF export formats from actual exports.

### Summary Stats

```
Classification:  Partial native export
Export format:   Mixed (CCD XML, JSON, Computable PDF)
Model type:      Hybrid — CCD standard for clinical, proprietary JSON for administrative
Entities:        87 data elements (flat list, not relational tables)
Fields:          87 (each element = one field)
Descriptions:    100% (all 87 elements have brief descriptions)
Sample data:     No
Bulk export:     No (single-patient API)
Domains covered: 10 of 15 applicable domains (with caveats — several are thin)
```

### Bottom Line

SolidPractice's b(10) export covers demographics, basic clinical data, insurance, appointments, and receipt-level billing across 87 data elements — broader than a pure C-CDA repackaging. However, the critical absence of clinical notes (the product's signature voice-dictated documentation) and the complete lack of documentation for the JSON and PDF export formats mean that a patient would likely not get a complete, usable copy of their clinical record. The biggest gap is the missing encounter documentation; the biggest structural weakness is that 42 of 87 elements are exported as undocumented JSON with no schema or sample data.
