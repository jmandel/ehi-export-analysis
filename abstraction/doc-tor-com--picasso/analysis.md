# EHI Export Analysis: Doc-tor.com

**Product**: Picasso
**Analysis date**: 2026-02-16
**CHPL IDs**: 15.04.04.2985.Pica.08.06.1.250604

## 1. Product Context

Picasso is a cloud-based, fully integrated ambulatory EHR and practice management suite developed by Doc-tor.com (now part of Harris Healthcare / Constellation Software). It is marketed as an "All In One Medical Suite" encompassing four integrated components:

1. **Picasso EHR**: Clinical documentation with 1,000+ specialty templates, CPOE (meds, labs, imaging), drug interaction checking, lab results management, e-prescribing (NewCrop), document management, immunization reporting, and clinical quality measures.
2. **Picasso Practice Management**: Scheduling, patient registration, insurance eligibility verification, charge posting (CPT/HCPCS), claims management, payment posting, denial management, and KPI dashboards.
3. **Picasso Community (Patient Portal)**: Secure messaging, medication/records viewing, appointment scheduling, online bill payment.
4. **Revenue Cycle Management (RCM)**: Claims creation/submission, payment posting, denial remediation, financial analytics — offered as both software and managed service.

At the time of Harris acquisition (2020), the product served 550+ practices and 2,200+ clinicians, primarily in the NY/NJ/PA region. The product is general ambulatory (no specific specialty focus) and has had $1.7B+ in billings processed through its RCM arm. This means the EHI export should cover clinical data (encounters, notes, meds, labs, vitals, etc.), administrative data (demographics, insurance), and billing/financial data (charges, claims, payments) — all of which are part of the designated record set.

## 2. Artifacts Reviewed

| Artifact | Description | Size/Scope | Informativeness |
|---|---|---|---|
| `Picasso-EHI-Export-Documentation-V1_0-1.pdf` | **Picasso-specific EHI export data dictionary** — 21 data classes with column headings listed, CSV format. Created Jan 2024. | 3 pages, 154 KB | **Primary artifact** — the actual Picasso (b)(10) documentation |
| `Picasso-EHI-Export-Documentation-V1_0-1-1.pdf` | **Amazing Charts EHI export data dictionary** — 44 data classes, CSV/JSON/XML format. Despite Picasso filename, document title says "Amazing Charts EHI Export." Created Oct 2023. | 8 pages, 195 KB | Informative as a comparison — this is the sibling product's doc, not Picasso's. The CHPL-registered URL points to this file. |
| `PAA_API_documentation.pdf` | Picasso Application Access API — SOAP-style web service returning USCDI-compliant CCD XML. 4 methods: auth, patient lookup, single-patient CCD, multi-patient CCD. Lists USCDI v1 data classes. | 4 pages, 175 KB | Low — this is the (g)(10) clinical exchange API, not the (b)(10) EHI export |
| `enrichment/picasso-data-classes.json` | Structured JSON extraction of Picasso PDF: 21 data classes with column names | 12 KB | High — machine-readable parse of primary artifact |
| `enrichment/amazing-charts-data-classes.json` | Structured JSON extraction of Amazing Charts PDF: 44 data classes | 33 KB | Reference only |

**Key observation**: The CHPL-registered EHI documentation URL (`Picasso-EHI-Export-Documentation-V1_0-1-1.pdf`) actually points to the **Amazing Charts** EHI export document, not Picasso's. The actual Picasso-specific document (`V1_0-1.pdf`) was found on the mandatory disclosures page. This is a documentation error — the registered URL serves a sibling product's specification.

## 3. Export Mechanics

- **Format**: CSV (`.csv` files), one file per data class per patient. Attachments preserved in original format in an "Attachments" subfolder.
- **Mechanism**: Built-in export feature within the Picasso application. Export creates a folder named `ScheduledExport_MM-dd-yyyy hhmmss`.
- **Single-patient and bulk**: Supports both individual patient export and patient population export. Each patient gets a subfolder identified by their Picasso patient ID.
- **Access constraints**: No fees or access constraints mentioned in the documentation.
- **File naming**: Standardized pattern `[Data Class Name].csv`.

## 4. Export Content: What's In It

The Picasso EHI export documentation provides **only column headings** for each data class. There are:
- **0 field descriptions** (no field has any description beyond its column name)
- **0 field types** documented
- **0 value sets** or coded value enumerations
- **0 relationships/foreign keys** documented (though some column names like `VISITID`, `PROVIDERSID` imply foreign keys)
- **0 sample data** provided
- **No machine-readable schema** (only a PDF listing column names)

### Vendor's own content organization

The vendor organizes the export into 21 "Data Classes," each corresponding to a CSV file. All column names use ALL_CAPS naming convention. Provider information (name, DEA, license, email, UPIN) is denormalized into 15 of 21 entities, accounting for 119 of 441 total field occurrences.

| Entity/Table | Fields | Described | Types | Category |
|---|---|---|---|---|
| Demographics | 51 | 0 | no | Patient Information |
| Health Insurance | 51 | 0 | no | Insurance |
| Encounters | 28 | 0 | no | Clinical |
| Immunizations | 27 | 0 | no | Clinical |
| Medications | 27 | 0 | no | Clinical |
| Plan Of Treatment | 26 | 0 | no | Clinical |
| Labs | 24 | 0 | no | Clinical |
| Assessment | 23 | 0 | no | Clinical |
| Implantable Devices | 22 | 0 | no | Clinical |
| Tasks | 22 | 0 | no | Clinical |
| Allergies | 19 | 0 | no | Clinical |
| Orders | 18 | 0 | no | Clinical |
| Vitals | 17 | 0 | no | Clinical |
| Problems | 16 | 0 | no | Clinical |
| Clinical Notes | 15 | 0 | no | Clinical |
| Procedures | 15 | 0 | no | Clinical |
| Health Concerns | 13 | 0 | no | Clinical |
| Care Team | 12 | 0 | no | Clinical |
| Family History | 7 | 0 | no | Clinical |
| Social History | 4 | 0 | no | Clinical |
| Tobacco | 4 | 0 | no | Clinical |
| **TOTAL** | **441** | **0** | **no** | |

**Notable patterns:**
- Demographics is comprehensive (51 fields including pharmacy info, referral info, gender identity, sexual orientation, birth order).
- Health Insurance is detailed (51 fields with payer, policyholder, insured, and responsible party information plus case/plan details).
- Provider columns (`PROV_LAST`, `PROV_FIRST`, `PROV_PHONE`, `PROV_TITLE`, `PROV_DEA`, `PROV_LIC`, `PROV_EMAIL`, `PROV_UPIN`) appear in 15/21 entities — roughly 119 of 441 fields (27%) are just denormalized provider identifiers.
- Excluding provider column repetitions, unique clinical content fields number approximately 322.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The Picasso export covers primarily **USCDI-scope clinical data** plus health insurance. The 21 data classes map closely to USCDI v1 data classes:

**USCDI-aligned classes** (18 of 21): Allergies, Assessment, Care Team, Clinical Notes, Demographics, Encounters, Family History, Health Concerns, Health Insurance, Immunizations, Implantable Devices, Labs, Medications, Orders, Plan Of Treatment, Problems, Procedures, Vitals.

**Beyond USCDI** (3 of 21): Social History (4 fields), Tasks (22 fields — clinical task tracking), Tobacco (4 fields — though tobacco/smoking is part of USCDI).

The export is essentially a USCDI-plus-insurance export. There is **no billing data** (charges, claims, CPT codes beyond encounter E/M codes, payments, denials), **no patient portal communications**, **no scheduling data**, **no attachments/documents listing** (though an Attachments subfolder is mentioned for preservation), and **no custom forms or specialty-specific data**.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | `Demographics` (51 fields) — name, DOB, address, phone, email, SSN, race, ethnicity, language, gender identity, sexual orientation, pharmacy info | Thorough — comprehensive demographic data |
| Encounters / visits | ✅ Covered | `Encounters` (28 fields) — visit ID, name, type, E/M code, diagnosis, provider, facility, dates | Adequate — encounter-level data present |
| Problems / conditions | ✅ Covered | `Problems` (16 fields), `Assessment` (23 fields) — ICD codes, dates, status, coding language | Adequate |
| Medications / prescriptions | ✅ Covered | `Medications` (27 fields) — drug ID, name, dosage, duration, frequency, route, strength, active status | Adequate |
| Allergies | ✅ Covered | `Allergies` (19 fields) — allergen ID, name, type, severity, RxNorm code | Adequate |
| Immunizations | ✅ Covered | `Immunizations` (27 fields) — vaccine name, CVX code, lot, site, manufacturer, route, consent info | Thorough |
| Vitals | ✅ Covered | `Vitals` (17 fields) — height, weight, BP, pulse, respiration, temp, O2 sat, head circ, O2 flow rate | Adequate |
| Lab results | ✅ Covered | `Labs` (24 fields) — test description, value, LOINC, units, reference range, abnormal flags | Adequate |
| Imaging / diagnostic reports | ❌ Not covered | No imaging data class | Product supports imaging orders (a)(3) but no imaging results export |
| Procedures | ✅ Covered | `Procedures` (15 fields) — procedure code, date, modifiers | Adequate |
| Clinical notes / documents | ✅ Covered | `Clinical Notes` (15 fields) — note text, encounter date, visit type | Adequate but minimal — no note type categorization |
| Care plans / goals | ⚠️ Partial | `Plan Of Treatment` (26 fields) — category, description, referral info. No explicit goals entity. | Plan of treatment present but goals are missing as a separate entity |
| Orders / referrals | ⚠️ Partial | `Orders` (18 fields) — appears to be lab orders only (LABID, LABTESTCODE). No referral tracking. | Only lab orders exported; product does imaging orders and referrals but these aren't represented |
| Insurance / coverage | ✅ Covered | `Health Insurance` (51 fields) — payer, plan, policy, group, subscriber, insured, responsible party | Thorough |
| Claims / billing | ❌ Not covered | No billing, charges, claims, or CPT entities | **Significant gap** — product has full PM and RCM with charge posting, claims management, and payment processing |
| Payments | ❌ Not covered | No payment entities | **Significant gap** — product manages payment posting, patient balances, and payment plans |
| Consents / directives | ❌ Not covered | No advance directives or consent entity | Minor gap |
| Patient communications / portal messages | ❌ Not covered | No secure messaging or portal data entity | Product has "Community" patient portal with secure messaging |
| Specialty-specific | N/A | No specialty-specific data classes | Product is general ambulatory with 1,000+ specialty templates, but no specialty data in export |

## 6. Documentation Quality

The documentation quality is **very poor**:

- **No field descriptions**: Every field has only a column name (e.g., `ALLERGENSID`, `SEVERITYCODE`, `STABILITYTYPE`). Many names are ambiguous — `LONG_`, `TYPE`, `DEPRECATED`, `PHRASE`, `VALUE` give no indication of content.
- **No data types**: No indication of whether fields are strings, dates, integers, or booleans.
- **No value sets**: Fields like `ALLERGYTYPE`, `SEVERITY`, `CODINGLANGUAGE`, `TYPE`, `STATUS` have no enumerated values.
- **No relationships**: Foreign keys like `VISITID`, `PROVIDERSID`, `MEDID` are not documented as relationships.
- **No sample data**: No example records are provided.
- **No machine-readable schema**: The only artifact is a 3-page PDF listing column names.
- **Wrong URL registered**: The CHPL-registered documentation URL points to the Amazing Charts document, not the Picasso document.

A developer could not build a reliable import from this documentation alone. The column names provide some guidance (e.g., `BLOODPRESSURESYSTOLIC` is self-explanatory), but many fields would require reverse-engineering from actual export data. The lack of types, value sets, and relationships makes automated processing error-prone.

**Comparison with sibling product (Amazing Charts)**: The Amazing Charts export doc at the same URL has 44 data classes and 1,102 fields (vs. Picasso's 21 and 441). Amazing Charts includes billing history (74 fields), scheduling, referrals, advance directives, patient-generated data, emails, imported items, and several other classes absent from Picasso's export. This suggests Picasso's export is significantly less comprehensive than even its sibling product's.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Partial**

The export covers the core USCDI clinical domains (demographics, encounters, meds, labs, vitals, allergies, immunizations, problems, procedures, notes) plus health insurance — essentially a USCDI-plus-insurance scope. However, Picasso is explicitly a **combined EHR and Practice Management suite** with robust billing, claims, payments, and RCM capabilities. None of this financial/billing data appears in the export. The product also has a patient portal with secure messaging, scheduling, and appointment management — none of which appear in the export. The clinical coverage is reasonable but the complete absence of billing/PM data from a product whose identity is "All In One Medical Suite" (including PM and RCM) represents a significant gap in designated record set coverage. The 21 data classes align closely to USCDI v1's 16 data classes, suggesting this was built to match the USCDI checklist rather than comprehensively export the product's data.

**Axis 2 — Export approach: Purpose-built EHI export (minimal effort)**

This is not a repackaged C-CDA or FHIR export — it is a purpose-built CSV export with Picasso-specific column names (`ALLERGENSID`, `AMADIAGNOSISID`, `PROVIDERSID`, etc.) that map to the product's internal data model. The separate PAA API documentation confirms the (g)(10) API is a different mechanism (SOAP-based CCD XML). So the (b)(10) export was built as a distinct feature. However, the effort was minimal: only 21 data classes, no descriptions, no types, no sample data, and critical product domains (billing, PM) are entirely omitted. It's purpose-built in the sense that it's not a repackaged standard, but the scope is narrow.

### Key Findings

1. **Billing/PM data completely absent**: Picasso's core value proposition includes practice management and RCM (charge posting, claims, payments, denial management, patient balances), yet zero billing entities appear in the EHI export. This is the single largest gap — the product has processed $1.7B+ in billings.

2. **Documentation is column-names-only**: All 441 fields across 21 data classes have zero descriptions, zero type definitions, zero value set documentation, and zero relationship documentation. The entire data dictionary fits on 3 PDF pages.

3. **CHPL URL points to wrong product**: The registered EHI documentation URL serves the Amazing Charts export spec (44 data classes, 8 pages) rather than the Picasso export spec (21 data classes, 3 pages). The actual Picasso document was found separately.

4. **27% of fields are denormalized provider info**: Provider identifiers (name, DEA, license, email, UPIN, phone) are repeated in 15 of 21 entities, inflating the field count. Excluding these, unique clinical content fields number approximately 322.

5. **Sibling product has 2x the coverage**: The Amazing Charts export (same corporate parent, same URL) covers 44 data classes including billing history, scheduling, referrals, advance directives, emails, and user-defined fields — all absent from Picasso's export. This suggests Picasso received less development attention for (b)(10) compliance.

### Summary Stats

    Coverage:        Partial
    Approach:        Purpose-built EHI export
    Export format:   CSV
    Entities:        21
    Fields:          441
    Descriptions:    0% (0 of 441 fields have descriptions)
    Sample data:     No
    Bulk export:     Yes (single-patient and population)
    Domains covered: 12 of 18 applicable domains

### Bottom Line

Picasso's EHI export is a purpose-built CSV export that covers core USCDI clinical domains and insurance, but completely omits billing, claims, payments, patient portal communications, and scheduling data — all of which the product stores and which are part of the designated record set. The documentation is bare-minimum (column names only, no descriptions, no types, no sample data), and the CHPL-registered URL actually points to a sibling product's document. A patient would get their clinical summary and insurance info but not their billing history, claims, or portal messages.
