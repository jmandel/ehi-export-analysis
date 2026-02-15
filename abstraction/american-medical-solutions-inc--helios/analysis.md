# EHI Export Analysis: American Medical Solutions, Inc.

**Product**: Helios (HeliosMD / HeliosND) v2.0
**Analysis date**: 2026-02-15
**CHPL ID**: 10834 (`15.02.05.1086.AMEM.01.01.1.220217`)

## 1. Product Context

American Medical Solutions, Inc. (AMS) is a small vendor based in Phoenix/Tempe, Arizona, offering Helios — a web-based, cloud-hosted **integrated EHR and practice management system** for ambulatory clinical settings. It comes in two variants: HeliosMD for conventional medical practices and HeliosND for naturopathic physicians.

Helios is described as an "all-in-one system inclusive of practice management, document management and medical records." Key data domains the product stores, based on vendor materials and CHPL certification:

- **Clinical documentation**: Customizable encounter notes, problem lists, medication lists, allergy lists, vitals, immunizations, lab orders/results, family health history, implantable devices
- **E-prescribing**: Including EPCS (controlled substances)
- **Billing / practice management**: Fee schedules, co-pays, claims submission, patient statements, billing analytics, account reconciliation
- **Scheduling**: Multi-physician scheduling with online patient appointment requests
- **Document management**: Document scanning, imaging, paper-to-electronic conversion (a core AMS service)
- **Patient portal**: Patient-facing scheduling, messaging, view/download/transmit
- **Inventory management**: Mentioned in product listings
- **Public health reporting**: Immunization registry, electronic case reporting
- **Interoperability**: Direct messaging, FHIR API, transitions of care (C-CDA)

The product is certified across 37 criteria, indicating broad functionality. This baseline sets a high bar for what the (b)(10) export should cover.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|----------|-------------|-----------------|
| `170.315b10-EHI-Export-Documentation.pdf` | 10-page PDF data dictionary for the EHI export. Created 2023-12-13, content approved 2022-06-29. Documents 15 CSV export sections with 71 total fields. | **Primary artifact** — the sole substantive documentation |
| `services-page-certified-ehr-section.png` | Screenshot of amsemr.com/services/ showing the "Certified EHR" section with link to the export PDF | Confirms the PDF is the vendor's official (b)(10) documentation |
| `services-page-top.png` | Screenshot of the top of the services page | Low value — confirms site layout only |

Only one substantive artifact exists: the 10-page PDF. There are no sample data files, no machine-readable schemas, no additional documentation, and no ZIP file examples.

## 3. Export Mechanics

- **Format**: CSV files, each section generating an independent `.csv` file, bundled into a single `.zip` archive for download
- **Mechanism**: User-initiated via a toolbar button on the "Encounter Summary" screen. System administrators must grant export permissions to specific users.
- **Scope**: Per-patient export. The user selects which categories of EHI to include. No bulk/batch export capability is documented.
- **Access constraints**: Requires administrator-granted permissions. No fees mentioned. No API-based export option.
- **Standard**: No recognized standard — ad-hoc vendor-defined CSV format.

## 4. Export Content: What's In It

The export documentation defines **15 sections** producing 15 CSV files with a combined **71 fields** (verified by manual count from the PDF; see `analysis/full-entity-inventory.json`).

**Note on prior report accuracy**: The prior report stated the Vitals section had 13 fields. The actual count is **14 fields** — `HeadOccipital-frontalCircumference` and `Percentile` are documented as separate columns in the PDF table (pages 5–6).

### Documentation depth

- **Fields with descriptions**: Only 2 of 71 fields (2.8%) have meaningful descriptive notes beyond the field name: `ChartNumber` ("Unique identifier for the patient") and `DateofBirth` ("yyyy/mm/dd"). Every `Id` field repeats the same generic note ("Unique identifier for each record in the table").
- **Data types**: Documented for all fields. Four types used: `long`, `varchar`, `numeric`/`decimal`, `DateTime`.
- **Value sets**: None documented. No indication of valid values for coded fields like `Race`, `Ethnicity`, `BirthSex`, `Severity`, or `Status`.
- **Relationships**: None documented. No foreign keys. No way to link records across sections (e.g., a lab result to its encounter).
- **Sample data**: None provided.

### Vendor's own content organization

The vendor organizes the export into 15 "sections," each corresponding to one CSV file:

| Section | Entity/Table | Fields | Described | Types | Category |
|---------|-------------|--------|-----------|-------|----------|
| 2.1 | Patient Demographics | 17 | 2 (ChartNumber, DateofBirth) | Yes | Clinical summary |
| 2.2 | Allergies | 6 | 0 | Yes | Clinical summary |
| 2.3 | Vitals | 14 | 0 | Yes | Clinical summary |
| 2.4 | Care Team | 3 | 0 | Yes | Clinical summary |
| 2.5 | Immunizations | 2 | 0 | Yes | Clinical summary |
| 2.6 | Procedures | 2 | 0 | Yes | Clinical summary |
| 2.7 | Assessment and Plan of Treatment | 2 | 0 | Yes | Clinical summary |
| 2.8 | Laboratory | 3 | 0 | Yes | Clinical summary |
| 2.9 | Provenance | 3 | 0 | Yes | Clinical summary |
| 2.10 | Medications | 2 | 0 | Yes | Clinical summary |
| 2.11 | Smoking Status | 2 | 0 | Yes | Clinical summary |
| 2.12 | Clinical Notes | 9 | 0 | Yes | Clinical summary |
| 2.13 | Goals | 2 | 0 | Yes | Clinical summary |
| 2.14 | Health Concerns | 2 | 0 | Yes | Clinical summary |
| 2.15 | Problems | 2 | 0 | Yes | Clinical summary |

**Key structural observation**: 8 of 15 sections (53%) consist of only 2 fields — `Id` (long) plus a single `varchar` column. These sections are: Immunizations, Procedures, Assessment and Plan of Treatment, Medications, Smoking Status, Goals, Health Concerns, and Problems. This extreme flattening suggests the export either dumps structured clinical data into a single text string per record or the documentation drastically under-describes the actual CSV output. Either way, the documentation is insufficient.

The 15 sections map directly to **USCDI v1 data classes** (the same data elements required for the g(10) FHIR API). This is not the vendor's native data model — it is a clinical summary projection.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor does not use its own categories — all 15 sections fall under the same umbrella of "EHI Export Sections" and directly mirror USCDI v1 clinical data classes. There is no organizational distinction between clinical, administrative, or billing data because **only clinical summary data is present**.

The richest sections are:
- **Patient Demographics** (17 fields): The only section with meaningful granularity — name, DOB, race, ethnicity, sex, language, addresses, phone, email.
- **Vitals** (14 fields): Individual vital sign measurements as separate numeric columns.
- **Clinical Notes** (9 fields): Eight distinct note types as separate varchar columns.

The thinnest sections (8 of 15) have just `Id` + one varchar. For example, `Medications` is a single varchar field — no drug name, dose, route, frequency, start/end dates, prescriber, or pharmacy. `Immunizations` is a single varchar — no vaccine code, date administered, lot number, or site.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|--------|----------|----------------|--------------|
| Demographics | ⚠️ Partial | Section 2.1 (17 fields) — name, DOB, race, ethnicity, sex, language, address, phone, email | Reasonable for basics but missing insurance/coverage info that demographics often includes |
| Encounters / visits | ❌ Not covered | No encounter entity; no visit dates, types, or providers | Product stores encounter data (Encounter Summary is the export trigger). Significant gap. |
| Problems / conditions / diagnoses | ⚠️ Partial | Section 2.15 — Id + single varchar "Problems" | Product stores structured problem lists (certified (a)(3)). A single varchar is inadequate: no codes, onset dates, or status. |
| Medications / prescriptions | ⚠️ Partial | Section 2.10 — Id + single varchar "Medications" | Product has full e-prescribing with EPCS. A single varchar captures almost none of the prescription detail (dose, route, frequency, prescriber, dates, pharmacy). Major gap. |
| Allergies | ⚠️ Partial | Section 2.2 (6 fields) — substance, reaction, severity, status, non-medication flag | Reasonable structure but no coded values documented. One of the better sections. |
| Immunizations | ⚠️ Partial | Section 2.5 — Id + single varchar "Immunizations" | Product reports to immunization registries (certified (f)(1)). A single varchar is inadequate. |
| Vitals | ✅ Covered | Section 2.3 (14 fields) — individual vital measurements as separate numeric columns | Best-structured section; individual measurements are granular. |
| Lab results | ⚠️ Partial | Section 2.8 (3 fields) — Id, Tests, Values/Results | Product has a lab ordering portal. Three varchar fields cannot capture structured lab data (codes, units, reference ranges, dates, ordering provider). |
| Imaging / diagnostic reports | ⚠️ Partial | Section 2.12 includes ImagingNarrative as one varchar column | Only narrative text; no structured imaging order data, results, or reports. |
| Procedures | ⚠️ Partial | Section 2.6 — Id + single varchar "Procedures" | No procedure codes, dates, providers, or details. |
| Clinical notes / documents | ⚠️ Partial | Section 2.12 (9 fields) — 8 note types as separate varchar columns | Covers multiple note types but all are unstructured varchar. No dates, authors, or encounter links. Product has document scanning/imaging capabilities — scanned documents are not exported. |
| Care plans / goals | ⚠️ Partial | Section 2.7 (Assessment and Plan) + Section 2.13 (Goals) — both Id + single varchar | Minimal structure. |
| Orders / referrals | ❌ Not covered | No order or referral entities | Product does lab ordering and transitions of care. Gap. |
| Insurance / coverage | ❌ Not covered | No insurance entities | Product handles insurance payment processing, co-pays. Gap. |
| Claims / billing | ❌ Not covered | No billing entities | Product has integrated billing with fee schedules, claims submission, patient statements, billing analytics. **Significant gap.** |
| Payments | ❌ Not covered | No payment entities | Product handles account reconciliation and payment processing. Gap. |
| Consents / directives | ❌ Not covered | No consent entities | Unknown if product stores these. Possible N/A. |
| Patient communications / portal messages | ❌ Not covered | No messaging entities | Product has a patient portal with messaging. Gap. |
| Family health history | ❌ Not covered | No family history entity | Product is certified for (a)(12) family health history. Gap. |

**Summary**: Of the 18 applicable domains, **1 is adequately covered** (vitals), **10 are partially covered** with severely thin structure, and **7 are entirely absent** — including billing, insurance, encounters, orders, family history, and portal messages, all of which the product stores.

## 6. Documentation Quality

The documentation quality is **poor**:

- **Usability**: A developer could not build a meaningful import from this documentation. Most sections have a single varchar field with no indication of format, delimiters, or content structure. Is the "Medications" varchar a drug name? A drug name plus dose? A serialized JSON object? The documentation does not say.
- **Field descriptions**: 2 of 71 fields (2.8%) have non-trivial descriptions. The remaining 69 fields have either no notes or only the generic Id description.
- **Value sets**: None documented for any field. Coded fields like `Race`, `Ethnicity`, `BirthSex`, `Severity`, and `Status` have no valid value documentation.
- **Relationships**: No foreign keys, no cross-references, no encounter linkage. Each CSV section is an isolated flat file.
- **Machine-readable artifacts**: None. No JSON schema, no sample CSV files, no XSD.
- **Maintenance**: Document version 1.0, approved June 2022, PDF created December 2023. No revision history beyond the initial creation. No updates in nearly 4 years.

The documentation reads as a minimal compliance artifact created once for certification and not maintained since.

## 7. Overall Assessment

### Classification

**Standard-based projection** — The export is a CSV rendering of USCDI v1 clinical data classes. The 15 sections map one-to-one to the data elements required for the g(10) FHIR API (demographics, allergies, vitals, immunizations, medications, problems, procedures, assessment/plan, labs, smoking status, clinical notes, goals, health concerns, care team, provenance). This is not the vendor's native data model — it is a clinical summary repackaged as CSVs. The export covers roughly the same scope as a C-CDA document or FHIR US Core patient summary, missing the billing, scheduling, document management, and administrative data that constitute the other half of the EHR's designated record set.

### Key Findings

1. **USCDI-only coverage masquerading as (b)(10)**: The 15 export sections are a direct mapping of USCDI v1 data classes. This is the textbook failure mode where a vendor repackages their g(10) clinical summary as the (b)(10) "all EHI" export. The product stores billing, scheduling, document imaging, and e-prescribing detail — none of which appears in the export.

2. **Extreme field flattening**: 53% of sections (8/15) have only `Id` plus a single varchar field. Structured clinical data (medications, immunizations, procedures, problems) is apparently serialized into a single text string, losing all discrete data elements. This makes the export far less useful than even a C-CDA, which at least preserves coded elements.

3. **No billing or practice management data**: The product is marketed as an "all-in-one" EHR and practice management system with integrated billing, yet the export contains zero billing, insurance, claims, or payment entities. This is the single largest gap.

4. **Documentation is a minimal compliance artifact**: Only 2 of 71 fields (2.8%) have meaningful descriptions. No value sets, no relationships, no sample data, no machine-readable schemas. Created once in June 2022, never updated.

5. **Per-patient only, no bulk export**: The export is triggered per-patient from the Encounter Summary toolbar. No bulk or batch export mechanism is documented, making large-scale data portability impractical.

### Summary Stats

    Classification:  Standard-based projection
    Export format:   CSV (ZIP archive)
    Model type:      Standard projection (USCDI v1 data classes as CSVs)
    Entities:        15
    Fields:          71
    Descriptions:    2.8% (2/71 with meaningful descriptions)
    Sample data:     No
    Bulk export:     No
    Domains covered: 1 of 18 adequately; 10 partial; 7 absent

### Bottom Line

This export is a USCDI v1 clinical summary rendered as CSVs — it covers roughly what a C-CDA or FHIR patient access API would provide, but in a less structured format. A patient or provider requesting their complete health record would not receive billing data, insurance information, e-prescribing details, scanned documents, scheduling history, portal messages, or family health history — all of which Helios stores. The single biggest gap is the complete absence of billing and practice management data from a product whose core value proposition is integrated EHR + PM.
