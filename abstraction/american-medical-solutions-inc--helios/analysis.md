# EHI Export Analysis: American Medical Solutions, Inc.

**Product**: Helios v2.0
**Analysis date**: 2026-02-16
**CHPL ID**: 15.02.05.1086.AMEM.01.01.1.220217

## 1. Product Context

Helios is a web-based, cloud-hosted EHR and practice management system from American Medical Solutions, Inc. (AMS), a small Phoenix, AZ-based vendor. It targets small ambulatory medical practices across a range of specialties, with a naturopathic variant (HeliosND). The product is an integrated system covering:

- **Clinical documentation**: customizable encounter notes, problem lists, medication lists, allergy lists, vitals, immunizations, lab ordering/results, family health history, implantable device tracking
- **Practice management/billing**: integrated billing with fee schedules, co-pay management, claims submission, patient statements, billing analytics, account reconciliation
- **Scheduling**: multi-physician scheduling with online patient appointment requests
- **Document management**: document scanning/imaging, paper-to-electronic conversion (a core AMS service)
- **Patient portal**: patient-facing portal for scheduling and communication
- **E-prescribing**: including EPCS (controlled substances)
- **Interoperability**: Direct messaging, HL7 integration, FHIR API (g)(10), transitions of care (C-CDA)

The product holds 37 ONC certification criteria. For (b)(10) assessment, the key question is whether the export covers billing, scheduling, documents, e-prescribing details, and patient portal data — not just the clinical summary data covered by USCDI.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/170.315b10-EHI-Export-Documentation.pdf` | 10-page PDF: the sole EHI export documentation. Contains overview (1 page) and data dictionary for 15 CSV export sections (9 pages). Created June 2022, approved by Anthony Puglisi. 172 KB. | **Primary source** — this is the entire (b)(10) documentation |
| `downloads/services-page-certified-ehr-section.png` | Screenshot of amsemr.com/services/ showing the "Certified EHR" section with the Export Documentation link | Context only — confirms link location |
| `downloads/services-page-top.png` | Screenshot of the services page header showing AMS branding | Context only |

No sample data files, no machine-readable schemas, no additional documentation beyond the single PDF.

## 3. Export Mechanics

- **Format**: CSV files bundled in a ZIP archive. Each export section generates an independent CSV file named after the section.
- **Mechanism**: User-initiated from the Encounter Summary toolbar. System administrators must grant export permissions. User selects which categories to export.
- **Scope**: Single-patient export only. No evidence of bulk/batch export capability.
- **Access constraints**: Requires system administrator to enable export permissions for individual users.
- **Fees**: Not mentioned in documentation.

## 4. Export Content: What's In It

The PDF documents 15 CSV export sections with a total of **70 fields** across all sections. Only **17 fields (24.3%)** have any description beyond the field name — and 15 of those 17 are just the generic "Unique identifier for each record in the table" note on Id fields. Only 2 fields have substantive notes: `ChartNumber` ("Unique identifier for the patient") and `DateofBirth` ("yyyy/mm/dd").

No types are documented beyond basic datatypes (long, varchar, numeric, decimal, DateTime). No value sets, no relationships/foreign keys, no sample data.

### Vendor's own content organization

The vendor organizes the export into 15 sections, all clinical in nature:

| Entity/Table | Section | Fields | Fields w/ Description | Types Documented |
|---|---|---|---|---|
| Patient Demographics | 2.1 | 17 | 3 | Yes |
| Allergies | 2.2 | 6 | 1 | Yes |
| Vitals | 2.3 | 13 | 1 | Yes |
| Care Team | 2.4 | 3 | 1 | Yes |
| Immunizations | 2.5 | 2 | 1 | Yes |
| Procedures | 2.6 | 2 | 1 | Yes |
| Assessment and Plan of Treatment | 2.7 | 2 | 1 | Yes |
| Laboratory | 2.8 | 3 | 1 | Yes |
| Medications | 2.10 | 2 | 1 | Yes |
| Smoking Status | 2.11 | 2 | 1 | Yes |
| Clinical Notes | 2.12 | 9 | 1 | Yes |
| Goals | 2.13 | 2 | 1 | Yes |
| Health Concerns | 2.14 | 2 | 1 | Yes |
| Problems | 2.15 | 2 | 1 | Yes |
| Provenance | 2.9 | 3 | 1 | Yes |
| **TOTAL** | | **70** | **17** | |

**Critical structural issue**: 10 of the 15 sections have only 2 fields — an Id and a single varchar column. For example, `Medications` has only `Id` (long) and `Medications` (varchar). This means complex clinical data (medication name, dose, route, frequency, start date, prescriber, status) is presumably serialized into a single text string, making the export nearly unusable for programmatic consumption. Only Patient Demographics (17 fields), Vitals (13 fields), Clinical Notes (9 fields), and Allergies (6 fields) have meaningful field-level granularity.

Full entity and field inventory is in `analysis/entity-inventory-full.json`.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor's 15 export sections map directly to the **USCDI v1 data classes**. They are exclusively clinical summary data:

- **Demographics** (17 fields) — the most complete section, covering name, DOB, race, ethnicity, birth sex, language, addresses, phone, email
- **Vitals** (13 fields) — individual numeric fields for each vital sign measurement, the second-most granular section
- **Clinical Notes** (9 fields) — 8 note types as separate columns (Consultation, Discharge Summary, H&P, Procedure, Progress, Imaging, Lab Report, Pathology Report)
- **Allergies** (6 fields) — substance, reaction, severity, status, non-medication flag
- **Remaining 11 sections** (2-3 fields each) — minimal single-varchar representations of immunizations, procedures, assessment/plan, labs, medications, smoking status, goals, health concerns, problems, care team, provenance

There are **zero sections** for any non-USCDI data domain. No billing, no scheduling, no documents, no insurance, no prescribing details, no patient portal data.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | `Patient Demographics` (17 fields) — name, DOB, race, ethnicity, sex, language, address, phone, email | Covers basics but no insurance info, no emergency contacts, no employer |
| Encounters / visits | ❌ Not covered | No encounter entity | Product stores encounters (Encounter Summary toolbar is where export lives). Significant gap |
| Problems / conditions | ⚠️ Partial | `Problems` — Id + single varchar | Single text field; no codes, dates, status, or severity |
| Medications / prescriptions | ⚠️ Partial | `Medications` — Id + single varchar | Product has EPCS e-prescribing. Single text field loses dose, route, frequency, prescriber, dates. Major gap |
| Allergies | ⚠️ Partial | `Allergies` (6 fields) — substance, reaction, severity, status | Reasonable but no codes, no onset dates |
| Immunizations | ⚠️ Partial | `Immunizations` — Id + single varchar | Single text field; no dates, lot numbers, sites, manufacturers |
| Vitals | ✅ Covered | `Vitals` (13 fields) — individual numeric columns for each vital sign | Most granular section; no date/time of measurement though |
| Lab results | ⚠️ Partial | `Laboratory` — Id, Tests, Values/Results | Only 3 fields; no units, reference ranges, dates, ordering provider |
| Imaging / diagnostic reports | ⚠️ Partial | `Clinical Notes` has ImagingNarrative column | Narrative text only; no structured imaging data |
| Procedures | ⚠️ Partial | `Procedures` — Id + single varchar | Single text field; no codes, dates, performers |
| Clinical notes / documents | ⚠️ Partial | `Clinical Notes` (9 fields) — 8 note type columns | Covers USCDI note types but all as varchar; unclear if full note text or just titles |
| Care plans / goals | ⚠️ Partial | `Assessment and Plan of Treatment` + `Goals` — each Id + single varchar | Minimal; no structured data |
| Orders / referrals | ❌ Not covered | No orders entity | Product has lab ordering portal. Gap |
| Insurance / coverage | ❌ Not covered | No insurance entity | Product has integrated billing with insurance. Significant gap |
| Claims / billing | ❌ Not covered | No billing entity | Product has integrated billing, fee schedules, claims submission, billing analytics. **Major gap** |
| Payments | ❌ Not covered | No payment entity | Product tracks co-pays and account reconciliation. Gap |
| Consents / directives | ❌ Not covered | No consents entity | N/A — unclear if product stores these |
| Patient communications / portal | ❌ Not covered | No communications entity | Product has patient portal. Gap |
| Family health history | ❌ Not covered | No family history entity | Certified for (a)(12). Gap |
| Implantable devices | ❌ Not covered | No device entity | Certified for (a)(14). Gap |
| Scanned documents | ❌ Not covered | No documents entity | AMS core service includes document scanning/imaging. **Significant gap** |

## 6. Documentation Quality

The documentation quality is **poor**:

- **No field-level descriptions**: Beyond generic Id notes and 2 fields (ChartNumber, DateofBirth), no field has a semantic description. A developer would have to guess what "Non-Medication" means in the Allergies table, or what format the single "Medications" varchar uses.
- **No value sets**: Fields like Race, Ethnicity, BirthSex, Severity, Status have no documented valid values or code systems.
- **No relationships**: No foreign keys, no encounter references. There is no way to associate a lab result with its ordering encounter, or a medication with its prescriber.
- **No sample data**: No example CSV files are provided.
- **No machine-readable schemas**: Only a PDF.
- **No date/time on most entities**: Vitals have no measurement date. Medications have no start/end dates. Labs have no result dates. Without temporal context, these records are nearly meaningless.
- **Ambiguous single-field entities**: For 10 of 15 sections, the entire clinical concept is reduced to a single varchar. The documentation does not explain how structured data (e.g., medication details, immunization records) is represented in that single field.

A developer could not build a meaningful import from this documentation. The schema is too sparse to understand the data format, and the single-varchar approach for most entities means the actual data structure is hidden within unspecified text formatting.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Minimal/stub**

The export covers only USCDI-scope clinical summary data, and even within that scope, most entities are reduced to a single text field (Id + varchar). The product is an integrated EHR and practice management system with billing, scheduling, document management, e-prescribing, and patient portal capabilities — none of which appear in the export. Even within the clinical domains that are nominally covered, the single-varchar approach for 10 of 15 sections means the export provides far less structured data than the product actually stores. This is not a genuine attempt to export "all EHI."

**Axis 2 — Export approach: Repackaged existing export**

The 15 export sections map exactly to the USCDI v1 / US Core data classes. The section names (Patient Demographics, Allergies, Vitals, Care Team, Immunizations, Procedures, Assessment and Plan of Treatment, Laboratory, Provenance, Medications, Smoking Status, Clinical Notes, Goals, Health Concerns, Problems) are a near-perfect match to the C-CDA / FHIR US Core patient summary scope. There is no evidence of any data domain beyond what would be in a standard clinical exchange — no billing tables, no scheduling data, no document management exports, no e-prescribing detail. This is a CSV rendering of the USCDI clinical summary relabeled as (b)(10).

### Key Findings

1. **The export is a CSV rendering of USCDI v1 clinical summary data, not an EHI export.** All 15 sections map directly to USCDI data classes. No billing, scheduling, documents, insurance, or other practice management data is included despite Helios being an integrated EHR/PM system. (Source: `170.315b10-EHI-Export-Documentation.pdf`, sections 2.1–2.15)

2. **10 of 15 sections reduce complex clinical data to a single varchar field.** Medications, Immunizations, Procedures, Problems, Goals, Health Concerns, Smoking Status, and Assessment/Plan each have only an Id and one text column. This means structured clinical data is serialized into unspecified text, making the export largely unusable for data portability. (Source: `entity-inventory-full.json`)

3. **No temporal context for most data.** Vitals have no measurement date. Medications have no start/end dates. Labs have no result dates. Immunizations have no administration dates. Clinical data without dates has minimal utility. (Source: PDF sections 2.3, 2.5, 2.6, 2.8, 2.10)

4. **Major product capabilities are entirely absent from the export.** The product has integrated billing (fee schedules, claims, co-pays, patient statements), scheduling, document scanning/imaging, e-prescribing (EPCS), and a patient portal. None of these appear in any export section. (Source: `product-research.md` capabilities vs. PDF export sections)

5. **Documentation is a single 10-page PDF from June 2022 with no updates in nearly 4 years.** No sample data, no value sets, no relationship documentation, no machine-readable schema. Only 2 of 70 fields have substantive descriptions. (Source: PDF document properties and content analysis)

### Summary Stats

    Coverage:        Minimal/stub
    Approach:        Repackaged existing export
    Export format:   CSV files in ZIP archive
    Entities:        15
    Fields:          70
    Descriptions:    24.3% (17/70, but 15 are generic Id descriptions; effectively 2.9% substantive)
    Sample data:     No
    Bulk export:     No (single-patient only)
    Domains covered: 1 of 15+ applicable domains (partial clinical only; 0 complete)

### Bottom Line

This is a textbook example of a vendor repackaging USCDI clinical summary data as a (b)(10) EHI export. A patient receiving this export would get a minimal, largely unstructured dump of their clinical summary (most fields are single text strings) with no dates, no billing records, no prescription details, no scanned documents, and no portal communications — despite Helios storing all of this data. The single biggest gap is the complete absence of billing and practice management data from a product that is explicitly an integrated EHR/PM system.
