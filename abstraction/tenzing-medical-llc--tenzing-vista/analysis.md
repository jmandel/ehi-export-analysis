# EHI Export Analysis: Tenzing Medical LLC

**Product**: Tenzing VistA  
**Analysis date**: 2026-02-16  
**CHPL ID**: 15.02.05.2936.TENZ.01.01.1.220120 (CHPL #10799)

## 1. Product Context

Tenzing VistA is a certified adaptation of the VA's open-source VistA EHR, customized for community hospital use by Tenzing Medical LLC. The primary (and likely only) customer is Oroville Hospital, a 133-bed non-profit acute care facility in Northern California. Tenzing Medical is essentially a certification vehicle for Oroville Hospital's internal VistA implementation.

The product is a **full-scope inpatient and ambulatory EHR** running on a MUMPS/YottaDB stack with the CPRS clinical interface. Documented capabilities include:

- **Clinical**: CPRS (cover sheet, problems, meds, orders, notes, consults, surgery, discharge summaries, labs, reports), CPOE, vital signs, allergy tracking, immunizations, VistA Imaging
- **Pharmacy**: Inpatient and outpatient prescriptions, ePrescribing via Surescripts, controlled substance tracking
- **Laboratory**: Full clinical lab (chemistry, hematology, microbiology, pathology, blood bank, cytology) interfaced with Sunquest
- **Administrative**: ADT, scheduling, bed management, registration
- **Specialty**: Surgery module, dietary, radiology/nuclear medicine, consult tracking
- **Billing**: The product uses **McKesson Series** as a separate billing/practice management system (not VistA's built-in billing module). The EHI documentation explicitly references Series for billing data.
- **Patient Portal**: Bridge Patient Portal

This baseline means a comprehensive EHI export should cover clinical data from VistA **and** billing/account data from McKesson Series.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/TenzingEHIFormatInfo.pdf` | 3-page PDF (102 KB, created 2023-11-14). Lists 29 C-CDA sections exported by VistA and 4 McKesson Series billing data sections. Section-level documentation only — no field-level data dictionary. **Primary artifact.** | Most informative |
| `downloads/ElectronicHealthInformationExport.pdf` | 4-page PDF (114 KB, created 2023-07-10). User guide documenting two VistA menu options for performing exports (VGTM EHI EXPORT interactive, VGTM AUTO CCDA EXPORT scheduled batch). Includes VistA terminal screenshots. | Moderately informative (mechanics only) |
| `product-research.md` | Background research on the vendor and product capabilities | Context only |
| `files.json` | Manifest of 2 downloaded files | Index only |

No sample data files, no machine-readable schemas, no field-level data dictionary, no XLSX/CSV/JSON artifacts were provided.

## 3. Export Mechanics

- **Format**: Clinical data exported as **C-CDA XML (CDA R2.1, USCDI v2)**. Billing data from McKesson Series exported as **structured delimited format** (no further specification of delimiter or schema).
- **Mechanism**: Two VistA menu options:
  - `VGTM EHI EXPORT`: Interactive terminal option — user selects hospital location(s), encounter scope (latest, specific, or date range), and file/folder destination. Runs in real time.
  - `VGTM AUTO CCDA EXPORT`: Scheduled batch option via VistA TaskMan — can be configured for recurring exports (e.g., monthly). Parameters specify date range, location, and export path.
- **Granularity**: Per-patient (one XML document per patient). Multiple patients can be selected; batch selection available. Users select which C-CDA sections to include.
- **Single-patient vs bulk**: Both supported. Interactive mode is single-location; batch mode can be scheduled for recurring bulk export.
- **Access constraints**: Requires `VGTM DP-EHI EXPORT` security key for interactive export; requires `# Fileman Access` and `XUTM SCHEDULE` menu for scheduled export. No vendor assistance required — documentation states users can create exports "at any time without further developer assistance."
- **Fees**: Not mentioned.
- **Series billing data**: The documentation states Series provides export capability but gives no procedural detail on how billing data export is triggered or delivered.

## 4. Export Content: What's In It

### Overview

The export documentation identifies **33 total sections** across two systems:
- **29 C-CDA sections** from Tenzing VistA (clinical data)
- **4 sections** from McKesson Series (billing/administrative data)

**There is no field-level data dictionary.** The documentation provides only section names, C-CDA template IDs (for VistA sections), hierarchical paths (for Series sections), and one-sentence descriptions. No individual fields, data types, cardinality, value sets, foreign keys, or sample data are documented.

### Vendor's own content organization

#### Tenzing VistA — C-CDA Sections (29 sections)

| Section | Template ID / XPath | Description |
|---|---|---|
| Care Team | XPath: .../documentationOf/serviceEvent/performer | Ordering providers, clinical care team |
| Problems | 2.16.840.1.113883.10.20.22.2.5.1 | Clinical problem list |
| Vitals | 2.16.840.1.113883.10.20.22.2.4.1 | Vital signs |
| Medications | 2.16.840.1.113883.10.20.22.2.1.1 | Active and pertinent medication history |
| Admission Medications | 2.16.840.1.113883.10.20.22.2.44 | Medications during inpatient stay |
| Ambulatory Medications | 2.16.840.1.113883.10.20.22.2.38 | Medications during clinical visit |
| Discharge Medications | 2.16.840.1.113883.10.20.22.2.11.1 | Medications ordered upon discharge |
| Allergies and Intolerances | 2.16.840.1.113883.10.20.22.2.6.1 | Active and pertinent allergy list |
| Social History / Smoking Status | 2.16.840.1.113883.10.20.22.2.17 | Social history and smoking status |
| Assessments | 2.16.840.1.113883.10.20.22.2.8 | Impressions/diagnoses guiding treatment |
| Encounter Diagnosis | 2.16.840.1.113883.10.20.22.2.22.1 | Diagnoses at close of visit with location/timeframes |
| Procedures | 2.16.840.1.113883.10.20.22.2.7.1 | Surgical, diagnostic, therapeutic procedures |
| Diagnostic Results | 2.16.840.1.113883.10.20.22.2.3.1 | Lab, radiological, procedural results |
| Plan of Treatment | 2.16.840.1.113883.10.20.22.2.10 | Pending orders, interventions, encounters |
| Immunizations | 2.16.840.1.113883.10.20.22.2.2.1 | Immunization history |
| Reason For Referral | 1.3.6.1.4.1.19376.1.5.3.1.3.1 | Notes related to outside referrals |
| Chief Complaint | 2.16.840.1.113883.10.20.22.2.13 | Patient's description of complaint |
| Admit Diagnosis | 2.16.840.1.113883.10.20.22.2.43 | Diagnosis at inpatient admission |
| Discharge Diagnosis | (no template ID listed) | Diagnosis at inpatient discharge |
| Instructions | 2.16.840.1.113883.10.20.22.2.45 | Provider notes directed to patient |
| Functional Status | 2.16.840.1.113883.10.20.22.2.14 | Physical abilities assessments |
| Mental Status | 2.16.840.1.113883.10.20.22.2.56 | Psychological/mental competency evaluations |
| Notes | 2.16.840.1.113883.10.20.22.2.65 | Free text clinical documentation |
| Discharge Instructions | 2.16.840.1.113883.10.20.22.2.41 | Instructions at discharge |
| Medical Equipment | 2.16.840.1.113883.10.20.22.2.23 | Implanted/external devices and equipment |
| Health Concerns | 2.16.840.1.113883.10.20.22.2.58 | SDOH-related conditions |
| Goals | 2.16.840.1.113883.10.20.22.2.60 | Patient care goals |
| Payers/Insurance | 2.16.840.1.113883.10.20.22.2.18 | Insurance and payer information |
| Family History | 2.16.840.1.113883.10.20.22.2.15 | Genetic relatives' health risks/factors |

These are **standard C-CDA R2.1 sections** — every template ID maps to a well-known HL7 C-CDA section. The coverage is consistent with what a C-CDA document would contain for clinical exchange purposes (i.e., USCDI-aligned). There is no evidence of vendor-specific extensions, custom sections, or data beyond the C-CDA standard template set.

#### McKesson Series — Billing Sections (4 sections)

| Section | Path | Description |
|---|---|---|
| Patient | /Patient | Patient demographics |
| Payer/Insurance | /Patient/Payer | Insurance, payer information |
| Enrollment/Account Information | /Patient/Account | Enrollment, account information |
| Billing History | /Patient/Billing | Billing history, adjudication, etc. |

These four sections are documented at the highest possible level — just a name, a hierarchical path, and a one-sentence description. No fields, no schema, no data types, no sample data.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor organizes their export into two systems:

**Tenzing VistA (clinical)**: 29 C-CDA sections covering the standard clinical document scope — problems, medications, allergies, vitals, labs, procedures, immunizations, notes, diagnoses, care team, referrals, functional/mental status, goals, health concerns, family history, and insurance. This is a thorough C-CDA document with good section breadth. However, the sections are **standard C-CDA sections** with standard template IDs — this is the same content available through any C-CDA clinical exchange, not a deeper export of VistA's internal data model (which stores far more per-entity than C-CDA captures).

**McKesson Series (billing)**: 4 high-level sections covering patient demographics, payer/insurance, account/enrollment, and billing history. The inclusion of billing data from a separate system is notable and suggests genuine engagement with the (b)(10) requirement. However, the documentation is so thin (no fields, no schema) that it's impossible to assess whether this represents a comprehensive billing export or a minimal stub.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | C-CDA header (implicit); Series `/Patient` section | C-CDA header has basic demographics; Series may add more, but no field detail |
| Encounters / visits | ⚠️ Partial | Encounter Diagnosis section includes visit location/timeframes | Encounter data is embedded in diagnoses, not a standalone entity. VistA's ADT module stores much richer encounter data |
| Problems / conditions | ✅ Covered | Problems (2.16.840.1.113883.10.20.22.2.5.1) | Standard C-CDA coverage |
| Medications / prescriptions | ✅ Covered | 4 medication sections (active, admission, ambulatory, discharge) | Good medication coverage across care settings |
| Allergies | ✅ Covered | Allergies and Intolerances section | Standard C-CDA coverage |
| Immunizations | ✅ Covered | Immunizations section | Standard C-CDA coverage |
| Vitals | ✅ Covered | Vitals section | Standard C-CDA coverage |
| Lab results | ✅ Covered | Diagnostic Results section | Covers lab, radiology, and procedural results |
| Imaging / diagnostic reports | ✅ Covered | Diagnostic Results section | Combined with lab results |
| Procedures | ✅ Covered | Procedures section | Standard C-CDA coverage |
| Clinical notes / documents | ✅ Covered | Notes section + Chief Complaint + Instructions + Discharge Instructions | Multiple note types covered |
| Care plans / goals | ✅ Covered | Plan of Treatment + Goals sections | Standard C-CDA coverage |
| Orders / referrals | ⚠️ Partial | Plan of Treatment (pending orders); Reason For Referral | Orders are in plan-of-treatment context, not detailed order records. VistA's CPOE stores detailed order data not captured in C-CDA |
| Insurance / coverage | ⚠️ Partial | C-CDA Payers/Insurance section + Series Payer/Insurance | Covered in two places but no field-level detail to assess depth |
| Claims / billing | ⚠️ Partial | Series Billing History section | Listed but zero field documentation; impossible to assess depth |
| Payments | ⚠️ Partial | Series Billing History (description mentions "adjudication") | May be included in billing history but no detail provided |
| Consents / directives | ❌ Not covered | No consent or advance directive sections listed | VistA can store advance directives; gap |
| Patient communications / portal | ❌ Not covered | No messaging or portal data mentioned | Bridge Patient Portal data not mentioned in export |
| Specialty-specific (surgery, dietary) | ❌ Not covered | No surgical detail, dietary orders, or specialty data beyond standard C-CDA | VistA has surgery and dietary modules; these are not represented |

## 6. Documentation Quality

The documentation is **minimal and insufficient for implementation**:

- **No field-level data dictionary**: The most critical deficiency. For 29 C-CDA sections, only the section name, standard template ID, and a brief description are provided. For 4 Series sections, only names and paths. A developer would need to reverse-engineer the actual XML/delimited output to understand field structure.
- **No sample data**: No example XML documents or delimited files are provided.
- **No machine-readable schemas**: No XSD, JSON Schema, or other machine-readable artifact.
- **No value sets or code systems**: Beyond referencing standard C-CDA template IDs, no coded value documentation.
- **No relationship documentation**: No foreign keys, cross-references, or entity relationships.
- **Procedural documentation is adequate**: The user guide clearly explains how to trigger exports via VistA menu options, with screenshots and parameter explanations.

A developer receiving this documentation would know *which C-CDA sections to expect* and *that some billing data exists in delimited format*, but could not build an import system, validate completeness, or understand the depth of data in any section without examining actual export files.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Partial**

The export covers clinical data through C-CDA (which maps closely to USCDI scope) and makes a notable effort to include billing/administrative data from a separate McKesson Series system. The inclusion of billing data distinguishes this from a pure clinical-exchange repackaging. However:

- The C-CDA clinical content is standard template-based — it captures what C-CDA is designed for, but VistA's internal data model (MUMPS globals, FileMan files) stores considerably more detail per entity than C-CDA sections convey. VistA's problem file has dozens of fields; a C-CDA Problem section conveys a fraction of them.
- Several product capabilities are not represented: surgical records (beyond the Procedures C-CDA section), dietary orders, detailed pharmacy data (controlled substance tracking, dispensing records), VistA Imaging documents/images, patient portal data, scheduling/ADT detail, and consult tracking detail.
- The billing component is promising in concept but has zero field-level documentation, making it impossible to verify its depth.

**Axis 2 — Export approach: Repackaged existing export (with billing supplement)**

The clinical export is clearly the vendor's **existing C-CDA clinical exchange capability** relabeled as (b)(10). The evidence is unambiguous:

1. The export user guide explicitly states it produces "Consolidated-Clinical Document Architecture (C-CDA) CDA R2.1 format" and references "USCDI v2."
2. Every VistA section maps 1:1 to a standard C-CDA template ID — there are no vendor-specific sections or extensions.
3. The menu option is literally named "EHI EXPORT" but the output format is "CCDA" (the batch option is `VGTM AUTO CCDA EXPORT`).
4. The documentation references SVAP for maintaining "current standards" — this is clinical exchange language, not EHI export language.

The addition of McKesson Series billing data (4 sections) goes beyond a pure C-CDA repackaging and represents some effort toward (b)(10) compliance. However, the billing documentation is so thin that it could range from a comprehensive billing export to a minimal stub — there's no way to tell from the artifacts provided.

### Key Findings

1. **C-CDA is the clinical export format**: The clinical portion is standard C-CDA R2.1 with 29 sections — this is the vendor's existing clinical exchange capability, not a purpose-built EHI export of VistA's internal data. VistA's MUMPS/FileMan database contains far more data per entity than C-CDA can represent.

2. **Billing data from McKesson Series is a genuine addition**: The vendor acknowledges that billing data lives in a separate system (McKesson Series) and includes 4 billing sections in the export. This is a meaningful step beyond pure clinical exchange, but the documentation provides zero field-level detail.

3. **No field-level documentation exists**: Across all 33 sections, there are zero individually documented fields. The documentation consists of section names and one-sentence descriptions only. This makes the export effectively unverifiable without examining actual output files.

4. **VistA-specific data is lost in C-CDA translation**: VistA's FileMan data dictionary defines hundreds of fields across dozens of files. C-CDA captures a clinical summary view of this data. Detailed order entries, pharmacy dispensing records, surgical operative data, imaging metadata, dietary orders, and other VistA-specific data are not represented in the C-CDA output.

5. **Both interactive and batch export are supported**: The export mechanism is well-designed with both real-time and scheduled options, and can be run without vendor assistance.

### Summary Stats

```
Coverage:        Partial
Approach:        Repackaged existing export (with billing supplement)
Export format:   C-CDA XML (clinical) + structured delimited (billing)
Entities:        33 sections (29 C-CDA + 4 billing)
Fields:          N/A (no field-level documentation)
Descriptions:    100% of sections have one-sentence descriptions; 0% field-level
Sample data:     No
Bulk export:     Yes (scheduled batch via TaskMan)
Domains covered: 10 of 18 applicable domains (many partial)
```

### Bottom Line

Tenzing VistA's EHI export is a C-CDA clinical exchange repackaged as (b)(10), supplemented by a minimally-documented billing data export from McKesson Series. A patient would receive a standard clinical summary document covering core clinical domains, but would miss VistA's internal depth (detailed orders, pharmacy dispensing, surgical records, imaging documents) and have no way to assess what billing data they actually received. The single biggest gap is the complete absence of field-level documentation — even the billing addition, which represents genuine effort, is unverifiable without it.
