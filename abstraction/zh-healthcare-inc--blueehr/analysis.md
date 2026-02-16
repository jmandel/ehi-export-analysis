# EHI Export Analysis: ZH Healthcare, Inc.

**Product**: BlueEHR Version 3
**Analysis date**: 2026-02-16
**CHPL IDs**: 15.02.05.3076.ZHHC.01.02.1.220119 (CHPL ID 10797)

## 1. Product Context

BlueEHR is a cloud-based, multi-specialty electronic health record and practice management system built on top of OpenEMR. It is developed by ZH Healthcare, Inc. (Bethesda, MD) and is the ONC-certified EHR module within their broader blueBriX digital health platform. The product was certified on 2022-01-19 through SLI Compliance with 32 criteria, indicating a full-featured EHR.

**Clinical capabilities**: BlueEHR supports 30–34 modules spanning ambulatory and acute care. Core clinical functions include CPOE (medications, labs, imaging), drug interaction checking, clinical decision support, customizable form builder, problem/medication/allergy lists, immunization tracking, e-prescribing, lab and radiology management, care coordination, and clinical documentation.

**Billing/PM capabilities**: The product includes integrated revenue cycle management with claims management and submission, insurance eligibility verification, CPT/ICD-10 coding, denial management, payment posting, ERA posting, patient ledger, and patient statements. The main menu screenshot in the EHI Export PDF itself reveals 15 distinct billing-related modules (Claims Manager, Claims History, Payment Manager, Patient Ledger, Batch Charge, ERA Posting, ERA Download, Patient Statement, AR Posting, Eligibility Report, etc.).

**Patient engagement**: Patient portal with view/download/transmit, secure messaging, appointment requesting, and self-reported health history.

**Specialty features**: Supports cardiology, dentistry, ophthalmology, radiology, behavioral health, and general practice. Includes telehealth (blueTeleMed), ADT for inpatient workflows, pharmacy/inventory management, and PACS integration.

**Market**: Serves thousands of providers across 100+ countries, with notable deployments in Ghana, India, and the US. Customer base skews toward smaller practices and international deployments.

**Baseline for EHI export**: Given this scope, a complete EHI export should cover clinical data (problems, meds, allergies, labs, vitals, notes, imaging, procedures, immunizations, care plans), billing/financial data (claims, payments, charges, insurance), patient-generated data (portal messages, self-reported history), and specialty-specific clinical data (custom forms, assessments).

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `EHI_Export.pdf` (194 KB, 2 pages) | The **sole** EHI export documentation. Cover page + 1 content page with text describing 3 export mechanisms and 2 screenshots. Created 2023-09-15 by Munawar Peringadi Vayalil in Microsoft Word. | **Primary artifact** — contains all available export documentation |
| `certifications-page-ehi-section.png` (154 KB) | Screenshot of the blueehr.com/certifications-and-costs/ page showing documentation links including "Electronic Health Information Export" | **Context only** — confirms the PDF is the only EHI export document linked |

Both the certifications page (HTTP 200, 80,552 bytes) and the PDF (HTTP 200, 194,524 bytes) were verified as still accessible on 2026-02-16.

**No other artifacts exist.** There is no data dictionary, no schema, no sample data, no JSON/XML/CSV definitions, no field documentation of any kind. The entire (b)(10) documentation is a single content page of prose with two screenshots.

## 3. Export Mechanics

BlueEHR describes three export mechanisms:

1. **C-CDA Clinical Export** (via Care Coordination feature): Users select patients and choose data categories via checkboxes. Exports clinical data as C-CDA XML documents. Supports single or multiple patients. The screenshot shows 18 selectable C-CDA sections.

2. **Analytics CSV/XLS Export** (via Analytics feature): Users can export demographics, insurance details, payments, lab results, encounters, and appointment details as CSV or XLS files. The screenshot shows the Analytics module in the main menu.

3. **Document Export** (via Document Module): Patient-attached documents can be retrieved. No details on format, process, or scope.

**Access mechanism**: UI-based (in-application features). No API-based export is described for (b)(10).
**Bulk capability**: Both C-CDA and Analytics exports support "one or multiple patients."
**Fees**: Not mentioned in the export documentation. The certifications page links to an "Additional Types of Costs" document separately.

## 4. Export Content: What's In It

### No data dictionary exists

The export documentation provides **zero field-level detail**. There is no data dictionary, no schema, no field names, no data types, no descriptions, no relationships, no value sets, and no sample data. The documentation describes only category-level groupings.

### Vendor's own content organization

The vendor describes content at the category level only. The following is the complete inventory of what is documented:

**C-CDA Clinical Export (18 components):**

| Component | Format | Fields Documented | Types | Descriptions |
|---|---|---|---|---|
| Allergies | C-CDA XML | 0 | No | No |
| Problems | C-CDA XML | 0 | No | No |
| Procedures | C-CDA XML | 0 | No | No |
| Plan Of Care | C-CDA XML | 0 | No | No |
| Social History | C-CDA XML | 0 | No | No |
| Functional Status | C-CDA XML | 0 | No | No |
| Deformities | C-CDA XML | 0 | No | No |
| Mental Status | C-CDA XML | 0 | No | No |
| Progress Notes | C-CDA XML | 0 | No | No |
| Medications | C-CDA XML | 0 | No | No |
| Immunizations | C-CDA XML | 0 | No | No |
| Results | C-CDA XML | 0 | No | No |
| Vitals | C-CDA XML | 0 | No | No |
| Encounters | C-CDA XML | 0 | No | No |
| Reason for Referral | C-CDA XML | 0 | No | No |
| Implanted Devices | C-CDA XML | 0 | No | No |
| Goals | C-CDA XML | 0 | No | No |
| Health Concerns | C-CDA XML | 0 | No | No |

**Analytics CSV/XLS Export (6 categories):**

| Category | Format | Fields Documented | Types | Descriptions |
|---|---|---|---|---|
| Demographic details | CSV/XLS | 0 | No | No |
| Insurance details | CSV/XLS | 0 | No | No |
| Payments | CSV/XLS | 0 | No | No |
| Lab results | CSV/XLS | 0 | No | No |
| Encounters | CSV/XLS | 0 | No | No |
| Appointment details | CSV/XLS | 0 | No | No |

**Document Export (1 category):**

| Category | Format | Fields Documented | Types | Descriptions |
|---|---|---|---|---|
| Patient Documents | Unknown | 0 | No | No |

**Totals**: 25 category-level items documented. 0 individual fields documented. 0 field descriptions. 0 data types. 0 relationships. 0 value sets. 0 sample records.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor organizes the export into three mechanisms rather than data categories:

1. **C-CDA Clinical Export**: 18 standard C-CDA section types. This is a standard clinical summary — the same sections available in any C-CDA Transitions of Care document. The checkbox list closely mirrors the (b)(1) Transitions of Care requirements, strongly suggesting this is the same C-CDA generation capability repurposed as the (b)(10) export. There are no vendor-specific extensions or non-standard sections visible.

2. **Analytics CSV/XLS Export**: 6 categories of administrative/operational data (demographics, insurance, payments, labs, encounters, appointments). This adds some data beyond the C-CDA but is described only at the category level with no detail on what fields or depth is included.

3. **Document Export**: Catch-all for patient-attached documents. No detail on types, formats, or completeness.

The C-CDA export covers standard clinical summary data. The Analytics export adds a thin layer of administrative data. Neither mechanism appears to export the product's native database model — both are projections into standardized or simplified formats (C-CDA XML and flat CSV/XLS).

**Notably absent from the vendor's own documentation**: Any mention of the extensive billing/RCM functionality visible in the PDF's own screenshot. The main menu screenshot (included in the EHI Export PDF itself) shows 15 billing modules — Claims Manager, Claims History, Payment Manager, Patient Ledger, Batch Charge, ERA Posting, ERA Download, Patient Statement, AR Posting, Eligibility Report, and more — none of which are addressed in the export documentation beyond a vague reference to "Payments."

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | Analytics CSV: "Demographic details" (no field detail) | Listed but no documentation of what fields are included |
| Encounters / visits | ⚠️ Partial | C-CDA: "Encounters" + Analytics CSV: "Encounters" | Two export paths mention encounters but no field-level detail |
| Problems / conditions | ⚠️ Partial | C-CDA: "Problems" | Standard C-CDA section only; no native data model |
| Medications / prescriptions | ⚠️ Partial | C-CDA: "Medications" | Standard C-CDA section; product has e-prescribing and pharmacy modules not addressed |
| Allergies | ⚠️ Partial | C-CDA: "Allergies" | Standard C-CDA section only |
| Immunizations | ⚠️ Partial | C-CDA: "Immunizations" | Standard C-CDA section only |
| Vitals | ⚠️ Partial | C-CDA: "Vitals" | Standard C-CDA section only |
| Lab results | ⚠️ Partial | C-CDA: "Results" + Analytics CSV: "Lab results" | Two paths but no field detail; unclear what lab data model looks like |
| Imaging / diagnostic reports | ❌ Not covered | No imaging entities in export | Product has radiology module + PACS integration + DICOM Viewer; significant gap |
| Procedures | ⚠️ Partial | C-CDA: "Procedures" | Standard C-CDA section only |
| Clinical notes / documents | ⚠️ Partial | C-CDA: "Progress Notes" + Document export | Progress notes via C-CDA; documents via document module; no detail on H&P, discharge summaries, etc. |
| Care plans / goals | ⚠️ Partial | C-CDA: "Plan Of Care", "Goals", "Health Concerns" | Standard C-CDA sections only |
| Orders / referrals | ⚠️ Partial | C-CDA: "Reason for Referral" | Product has CPOE for meds/labs/imaging; only referral reason mentioned, not order details |
| Insurance / coverage | ⚠️ Partial | Analytics CSV: "Insurance details" | Listed but no detail on fields; product has insurance eligibility module |
| Claims / billing | ❌ Not covered | No claims/billing entities in export | **Major gap**: Product has 15 billing modules (Claims Manager, Claims History, Payment Manager, Patient Ledger, Batch Charge, ERA Posting, ERA Download, Patient Statement, AR Posting, etc.) — none addressed in export |
| Payments | ⚠️ Partial | Analytics CSV: "Payments" | Mentioned but no detail; product has Payment, Payment Return, Payment Manager modules |
| Consents / directives | ❌ Not covered | Not mentioned | Product likely stores consent data; not addressed |
| Patient communications / portal messages | ❌ Not covered | Not mentioned | Product has patient portal with secure messaging; not addressed |
| Specialty-specific data | ❌ Not covered | Not mentioned | Product supports cardiology, dentistry, ophthalmology, behavioral health with custom forms; none addressed |

**Coverage summary**: 0 domains fully covered (✅), 13 domains partially covered (⚠️), 5 domains not covered (❌), 0 domains N/A.

All "partial" ratings reflect that C-CDA sections or category names are mentioned but with zero field-level documentation — it is impossible to verify what data is actually exported. The C-CDA sections are standard clinical summary sections, not comprehensive data exports.

## 6. Documentation Quality

The documentation quality is **critically insufficient**:

- **Volume**: 1 page of content (the other page is a cover). This is among the thinnest EHI export documentation possible.
- **Field-level detail**: None. Not a single field name, data type, or description is provided for any export mechanism.
- **Machine-readable artifacts**: None. No schemas, no sample data, no JSON/XML definitions, no CSV column headers.
- **Process documentation**: Three brief paragraphs describing the mechanisms. No step-by-step instructions, no screenshots of the actual export output.
- **Usability**: A developer could not build an import from this documentation. They would know the export uses C-CDA and CSV but would have no idea what fields to expect, what format the CSVs take, or what documents might be included.
- **Screenshots**: Two screenshots — one showing the C-CDA export UI with component checkboxes, one showing the main menu with "Analytics" circled. The screenshots provide some useful information (the C-CDA component list, the existence of billing modules) but are low-resolution and informational only.

The documentation reads as a compliance checkbox — the minimum effort needed to have a document linked from the certifications page. It does not serve as a technical reference for understanding or consuming the export.

## 7. Overall Assessment

### Classification

**Minimal/stub**: The documentation is too thin to fully assess the export, but what is described is clearly a clinical summary (C-CDA) plus a thin analytics extract (CSV), not a comprehensive "all EHI" export. No data dictionary exists, no field-level documentation, and major data domains (billing, specialty data, portal messages) are absent.

### Key Findings

1. **The entire (b)(10) documentation is 1 page of prose with 2 screenshots.** No data dictionary, no schema, no sample data, no field definitions of any kind (`EHI_Export.pdf`, page 2).

2. **The C-CDA export is almost certainly the (b)(1) Transitions of Care capability repackaged.** The 18 selectable components are standard C-CDA sections that match transitions of care requirements, not a comprehensive EHI export. This is a textbook case of C-CDA repackaging.

3. **Billing/RCM data is conspicuously absent despite being a major product capability.** The vendor's own EHI Export PDF includes a screenshot of the BlueEHR main menu showing 15 billing modules (Claims Manager, Patient Ledger, ERA Posting, etc.), yet the export documentation mentions only "Payments" as a CSV category. This is the single largest coverage gap.

4. **Zero field-level documentation makes the export opaque.** Even for the domains listed (demographics, insurance, payments), there is no way to know what fields are actually exported, in what format, or with what completeness. A recipient of this export would be working blind.

5. **Multiple product domains are completely unaddressed**: imaging/radiology (despite having DICOM Viewer and PACS integration), patient portal messages, custom forms (despite having a form builder), specialty-specific data (despite claiming multi-specialty support), and e-prescribing history.

### Summary Stats

    Classification:  Minimal/stub
    Export format:   C-CDA XML, CSV/XLS, documents (mixed)
    Model type:      Standard projection (C-CDA) + simple analytics extract (CSV)
    Entities:        25 category-level items (no entity/table-level granularity)
    Fields:          N/A (zero field-level documentation)
    Descriptions:    N/A (0%)
    Sample data:     No
    Bulk export:     Yes (multi-patient supported per documentation)
    Domains covered: 0 of 18 fully; 13 of 18 partially (category-name only, no field detail)

### Bottom Line

BlueEHR's EHI export documentation is a 1-page stub that repackages the existing C-CDA transitions-of-care capability and an analytics CSV extract as a (b)(10) export. No data dictionary exists, no field-level detail is provided, and the product's extensive billing/RCM functionality (15 modules visible in the vendor's own screenshot) is almost entirely unaddressed. A patient or provider requesting their complete health information would receive a clinical summary and some demographic/payment CSVs — not the comprehensive record that (b)(10) requires.
