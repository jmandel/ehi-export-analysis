# EHI Export Analysis: ZH Healthcare, Inc.

**Product**: BlueEHR 3
**Analysis date**: 2026-02-16
**CHPL IDs**: 15.02.05.3076.ZHHC.01.02.1.220119 (CHPL ID 10797)

## 1. Product Context

BlueEHR is a cloud-based, multi-specialty EHR and practice management system built on OpenEMR by ZH Healthcare, Inc. (now operating under the blueBriX brand). It is certified across 32 ONC criteria and marketed as having 30–34 modules covering a broad range of clinical and administrative functions.

**Key capabilities relevant to EHI export completeness:**

- **Clinical EHR core**: Demographics, problem lists, medications, allergies, lab orders/results, imaging orders, clinical notes, immunizations, vitals, care plans, clinical decision support, CPOE (certified (a)(1)–(a)(9))
- **Revenue cycle management / billing**: Claims management, insurance eligibility verification, payment posting, denial management, CPT/ICD-10 coding, patient ledger, ERA posting, batch charges, patient statements
- **E-prescribing**: Electronic prescribing capabilities
- **Patient portal**: Secure messaging, patient self-reported data, appointment requests, view/download/transmit
- **Telehealth**: blueTeleMed integrated video visits
- **Scheduling**: Appointment management and reminders
- **Pharmacy/inventory**: Pharmacy module, inventory tracking
- **Referral management**: Referral workflows
- **Public health reporting**: Immunization registries, syndromic surveillance
- **Custom forms**: Form builder for custom clinical templates
- **Transitions of care**: C-CDA generation/consumption, Direct messaging

The product's Billing Manager (visible in the PDF screenshot) includes at least 10 sub-modules: Payment, Payment Return, Claims Manager, Claims History, Payment Manager, Patient Ledger, Batch Charge, ERA Posting, ERA Download, and Patient Statement. This represents a significant body of patient-specific financial data that should be in a (b)(10) export.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/EHI_Export.pdf` (194 KB, 2 pages) | The sole EHI export documentation. Page 1 is a cover page with the blueEHR logo. Page 2 describes three export mechanisms with two embedded screenshots. Created 2023-09-15 in Microsoft Word. | **Primary artifact** — contains all vendor-provided EHI export documentation |
| `downloads/certifications-page-ehi-section.png` (154 KB) | Screenshot of blueehr.com/certifications-and-costs/ showing the "Electronic Health Information Export" link among other documentation links | Low — confirms the PDF is the only linked EHI documentation |
| `product-research.md` | Prior research on BlueEHR's capabilities and modules | Useful for establishing baseline of what the product stores |
| `ehi-export-report.md` | Prior agent's analysis of the export documentation | Useful for orientation; findings independently verified |
| `metadata.json` | CHPL certification details, developer contact info | Reference data |
| `chpl-metadata.json` | CHPL listing metadata | Reference data |

**Critical observation**: The entire EHI export documentation consists of a single 2-page PDF with 1 page of actual content. There are no additional artifacts — no data dictionary, no schema files, no sample exports, no API documentation specific to EHI export.

## 3. Export Mechanics

**Format(s)**:
1. **C-CDA (XML)** — Clinical data exported via the Care Coordination feature
2. **CSV or XLS** — Demographics, insurance, payments, labs, encounters, and appointments via the Analytics feature
3. **Original document formats** — Patient-attached documents via the document module

**Mechanism**: UI-based. The C-CDA export uses a checkbox-driven interface in the Care Coordination module. The CSV/XLS export uses the Analytics reporting feature. Documents are retrieved from the document module.

**Single-patient vs bulk**: Both the C-CDA and Analytics exports support "one or multiple patients" per the PDF text.

**Access constraints or fees**: Not documented. The certifications page links to an "Additional Types of Costs" document but this was not specific to EHI export.

## 4. Export Content: What's In It

### No data dictionary exists

The PDF provides **zero field-level documentation**. There are no entity definitions, no field names, no data types, no value sets, no relationships, no sample data, and no schemas. The documentation operates entirely at the category level — naming data domains (e.g., "Medications," "Payments") without specifying what fields or data elements are included in each.

### Vendor's own content organization

The vendor describes three export mechanisms covering 25 named categories total:

**Mechanism 1: C-CDA via Care Coordination (18 components)**

These are selectable via checkboxes in the Care Coordination UI (verified from the PDF screenshot):

| Component | Fields | Described | Types | Category |
|---|---|---|---|---|
| Allergies | 0 | N/A | N/A | C-CDA Clinical |
| Problems | 0 | N/A | N/A | C-CDA Clinical |
| Procedures | 0 | N/A | N/A | C-CDA Clinical |
| Plan Of Care | 0 | N/A | N/A | C-CDA Clinical |
| Social History | 0 | N/A | N/A | C-CDA Clinical |
| Functional Status | 0 | N/A | N/A | C-CDA Clinical |
| Instructions | 0 | N/A | N/A | C-CDA Clinical |
| Mental Status | 0 | N/A | N/A | C-CDA Clinical |
| Progress Notes | 0 | N/A | N/A | C-CDA Clinical |
| Medications | 0 | N/A | N/A | C-CDA Clinical |
| Immunizations | 0 | N/A | N/A | C-CDA Clinical |
| Results | 0 | N/A | N/A | C-CDA Clinical |
| Vitals | 0 | N/A | N/A | C-CDA Clinical |
| Encounters | 0 | N/A | N/A | C-CDA Clinical |
| Reason for Referral | 0 | N/A | N/A | C-CDA Clinical |
| Implanted Devices | 0 | N/A | N/A | C-CDA Clinical |
| Goals | 0 | N/A | N/A | C-CDA Clinical |
| Health Concerns | 0 | N/A | N/A | C-CDA Clinical |

These 18 components map directly to standard C-CDA sections. No vendor-specific extensions or additional data beyond the C-CDA standard are documented.

**Mechanism 2: CSV/XLS via Analytics (6 categories)**

| Category | Fields | Described | Types | Category |
|---|---|---|---|---|
| Demographic details | 0 | N/A | N/A | Administrative |
| Insurance details | 0 | N/A | N/A | Administrative |
| Payments | 0 | N/A | N/A | Financial |
| Lab results | 0 | N/A | N/A | Clinical |
| Encounters | 0 | N/A | N/A | Clinical |
| Appointment details | 0 | N/A | N/A | Administrative |

**Mechanism 3: Document Module (1 category)**

| Category | Fields | Described | Types | Category |
|---|---|---|---|---|
| Patient Documents | 0 | N/A | N/A | Documents |

**Summary statistics**:
- Total documented categories: **25**
- Total documented fields: **0**
- Fields with descriptions: **0**
- Fields with types: **0**
- Sample data provided: **No**
- Machine-readable schemas: **No**

The complete inventory is available in `analysis/entity-inventory-full.json`.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor organizes the export into three mechanisms:

1. **C-CDA clinical export** (18 components): This is the richest mechanism by category count, covering standard C-CDA sections for clinical data. However, these 18 components are exactly the standard C-CDA sections — there is no evidence of vendor-specific extensions or data beyond what the C-CDA standard defines. The Care Coordination feature used here is the same feature certified under (b)(1) Transitions of Care. The PDF's top navigation bar visible in the screenshot shows tabs labeled "Export," "Import," "CCPI," "Transition Of Care," "Cancer," "Immunization," "Syndromic Surveillance," and "Scheduled CCDA" — confirming this is the transitions of care module repurposed.

2. **Analytics CSV/XLS export** (6 categories): Adds demographics, insurance, payments, lab results, encounters, and appointments. This is the only mechanism that provides data outside the C-CDA clinical scope. However, "Payments" is notably thin compared to BlueEHR's full Billing Manager, which includes claims management, ERA posting, batch charges, patient ledgers, and patient statements — none of which are mentioned in the export.

3. **Document module** (1 category): A brief mention of document export with no details about what types of documents, what metadata accompanies them, or how the export is performed.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | "Demographic details" via CSV/XLS Analytics | Mentioned but no field-level detail; unclear what demographic fields are included |
| Encounters / visits | ⚠️ Partial | "Encounters" in both C-CDA and CSV/XLS | Present in two mechanisms but no documentation of what encounter data is included |
| Problems / conditions | ⚠️ Partial | "Problems" C-CDA component | Standard C-CDA section only; no vendor-specific depth documented |
| Medications / prescriptions | ⚠️ Partial | "Medications" C-CDA component | Standard C-CDA section; e-prescribing transaction history not mentioned |
| Allergies | ⚠️ Partial | "Allergies" C-CDA component | Standard C-CDA section only |
| Immunizations | ⚠️ Partial | "Immunizations" C-CDA component | Standard C-CDA section only |
| Vitals | ⚠️ Partial | "Vitals" C-CDA component | Standard C-CDA section only |
| Lab results | ⚠️ Partial | "Results" C-CDA + "Lab results" CSV/XLS | Available in two formats but no field details |
| Imaging / diagnostic reports | ❌ Not covered | No imaging-specific export mentioned | Product has DICOM Viewer and radiology module; gap |
| Procedures | ⚠️ Partial | "Procedures" C-CDA component | Standard C-CDA section only |
| Clinical notes / documents | ⚠️ Partial | "Progress Notes" C-CDA + "Patient Documents" via document module | Progress Notes in C-CDA; documents exportable but no detail on types or metadata |
| Care plans / goals | ⚠️ Partial | "Plan Of Care," "Goals," "Health Concerns" C-CDA components | Standard C-CDA sections |
| Orders / referrals | ⚠️ Partial | "Reason for Referral" C-CDA component | Only referral reason text; no CPOE order data, no order details |
| Insurance / coverage | ⚠️ Partial | "Insurance details" via CSV/XLS | Mentioned but no field definitions; unclear depth |
| Claims / billing | ❌ Not covered | "Payments" mentioned but not claims, charges, CPT codes, denials, ERA | Product has extensive Billing Manager with 10+ sub-modules (Claims Manager, Patient Ledger, Batch Charge, ERA Posting, etc.); **significant gap** |
| Payments | ⚠️ Partial | "Payments" via CSV/XLS Analytics | Mentioned but no detail; the product's full payment workflow (Payment Return, Payment Manager, Patient Statement) is much broader |
| Consents / directives | ❌ Not covered | Not mentioned | Product likely stores consent forms via form builder; gap |
| Patient communications | ❌ Not covered | Not mentioned | Product has patient portal with secure messaging; gap |
| Custom forms / questionnaires | ❌ Not covered | Not mentioned | Product has Forms Tracker and Forms Template Manager visible in screenshot; gap |
| Family health history | ❌ Not covered | Not mentioned | Certified under (a)(12); patient portal allows family history entry; gap |
| Referral workflows | ❌ Not covered | "Reason for Referral" in C-CDA only captures text | Product has dedicated Referral Management module visible in screenshot; gap |

**Coverage summary**: 0 domains fully covered, 13 domains partially covered (category-level mention only, no field documentation), 6 domains not covered at all. All "partial" ratings reflect that categories are named but zero field-level documentation exists — we cannot verify actual depth.

## 6. Documentation Quality

The documentation quality is **extremely poor** — among the thinnest possible for a certified product:

- **Volume**: 1 page of content (the other page is a cover page with a logo)
- **Detail level**: Category names only. Zero field definitions, zero data types, zero value sets, zero relationships
- **Machine-readable artifacts**: None (no JSON schemas, no CSV column definitions, no C-CDA profile documentation, no sample files)
- **Screenshots**: 2 embedded screenshots. The Care Coordination screenshot is moderately useful — it shows the 18 selectable C-CDA components. The Analytics screenshot only shows the main menu with "Analytics" circled, providing no insight into what the Analytics export produces
- **Usability**: A developer could not build an import from this documentation. The C-CDA portion could theoretically be parsed using generic C-CDA parsers, but the vendor provides no guidance on which C-CDA templates they use or what product-specific data maps to which C-CDA elements. The CSV/XLS export has no column definitions at all
- **Completeness**: The documentation does not describe what specific data elements are included, how to initiate the export programmatically, what format the output takes (beyond "C-CDA" and "CSV/XLS"), or how the three mechanisms relate to each other
- **Date**: Created September 15, 2023. No version history or updates since

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Minimal/stub/unclear**

The documentation is too thin to verify actual coverage. While the vendor names 25 data categories across three export mechanisms, zero field-level documentation exists to confirm what is actually exported. The C-CDA components map exactly to standard C-CDA sections (the same ones used for Transitions of Care), and the Analytics CSV/XLS categories are described only by name ("Payments," "Insurance details") without any specification of what data elements are included. Six entire data domains that the product demonstrably stores — billing/claims, imaging, patient communications, custom forms, family history, and referral workflows — are not mentioned at all. The Billing Manager's 10+ sub-modules (Claims Manager, Patient Ledger, Batch Charge, ERA Posting, ERA Download, Patient Statement, etc.) are completely absent from the export documentation despite being visible in the vendor's own screenshot.

**Axis 2 — Export approach: Repackaged existing export**

The clinical data export is clearly the existing (b)(1) Transitions of Care / Care Coordination C-CDA export relabeled as (b)(10). The PDF screenshot shows this is the same Care Coordination module with tabs for "Transition Of Care," "Syndromic Surveillance," and "Scheduled CCDA." The 18 selectable components are standard C-CDA sections with no vendor-specific extensions documented. The CSV/XLS Analytics export adds some administrative data categories but appears to be the product's existing reporting/analytics feature rather than a purpose-built EHI export. The document module export is a generic file retrieval capability. No purpose-built (b)(10) export mechanism was created.

### Key Findings

1. **The entire EHI export documentation is 1 page of content** — a cover page plus one content page with brief descriptions of three existing product features (Care Coordination, Analytics, Document Module) reframed as EHI export. No data dictionary, no field definitions, no schemas, no sample data exist (`downloads/EHI_Export.pdf`, page 2).

2. **The C-CDA export is the existing Transitions of Care feature**, not a purpose-built EHI export. The screenshot in the PDF shows the Care Coordination module with its standard navigation tabs. The 18 selectable components are standard C-CDA sections — identical to what would be produced for (b)(1) compliance.

3. **The product's extensive billing capabilities are almost entirely missing from the export**. The PDF's own screenshot reveals a Billing Manager with 10+ sub-modules (Claims Manager, Patient Ledger, Batch Charge, ERA Posting, ERA Download, Patient Statement, etc.), but the export documentation only mentions "Payments" as a CSV/XLS category with no detail.

4. **Zero field-level documentation exists for any export mechanism**. Not a single field name, data type, or value set is documented for any of the 25 named categories. A developer or patient receiving this export would have no documentation to interpret the data.

5. **Multiple product modules visible in the vendor's own screenshots are absent from the export**: Referral Management, Forms Tracker, Forms Template Manager, Pharmacy, Inventory, Messaging, and the full Billing Manager suite.

### Summary Stats

    Coverage:        Minimal/stub/unclear
    Approach:        Repackaged existing export
    Export format:   C-CDA (XML), CSV/XLS, document files
    Entities:        25 categories (no field-level detail)
    Fields:          0 documented
    Descriptions:    N/A (0 fields documented)
    Sample data:     No
    Bulk export:     Yes (multi-patient supported per PDF)
    Domains covered: 0 of 19 fully covered; 13 of 19 partially mentioned

### Bottom Line

BlueEHR's EHI export documentation is a 1-page PDF that repackages three existing product features — C-CDA clinical summaries, an analytics CSV export, and a document retrieval tool — as a (b)(10) export. With zero field-level documentation and significant gaps in billing, imaging, referrals, custom forms, and patient communications, a patient or provider would receive clinical summary data in standard formats but would miss large portions of what BlueEHR stores about them. The single biggest gap is the complete absence of the product's extensive billing and claims data from the export, despite the vendor's own screenshot showing a Billing Manager with 10+ sub-modules.
