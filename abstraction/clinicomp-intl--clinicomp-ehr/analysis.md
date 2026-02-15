# EHI Export Analysis: CliniComp, Intl.

**Product**: CliniComp|EHR v213.03
**Analysis date**: 2026-02-15
**CHPL ID**: 15.05.05.2695.CLIN.02.01.1.221013 (CHPL #10998)

## 1. Product Context

CliniComp|EHR is a **comprehensive, enterprise-wide inpatient EHR** developed by CliniComp, Intl. (San Diego, CA, founded 1983). It is a full hospital information system — not a specialty or ambulatory-only product — delivered as "System as a Service" (SYaaS). Primary customers are U.S. military (DoD) and Veterans Administration medical centers, with some private/community hospitals.

The product includes extensive modules relevant to EHI scope:

- **Clinical documentation**: flowsheets, progress notes, H&P, discharge summaries, multidisciplinary charting across ICU, ED, med-surg, ambulatory, behavioral health, perioperative/PACU, neonatal/perinatal
- **CPOE**: full computerized provider order entry with integrated pharmacy, radiology, and lab order workflows
- **Medication management**: BCMA, dispensing, compounding records, drug interaction checking
- **Laboratory Information System**: clinical chemistry, microbiology, molecular, pathology, blood bank/transfusion
- **Radiology (RIS) & Imaging (PACS)**: integrated radiology and imaging
- **Medical device integration**: waveform capture from bedside monitors, ventilators, pumps, anesthesia equipment
- **Perinatal/Neonatal**: fetal monitoring, growth curves, specialized neonatal dosing
- **Revenue Cycle Management**: eligibility verification, charge capture, medical coding, claims, payment processing, KPI reporting
- **Clinical decision support**: real-time alerts, early warning dashboards, AI analytics

This is a product that stores an enormous breadth and depth of patient data across clinical, ancillary, and billing domains. The export should reflect this breadth.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `ehi-data-export-details.html` (43 KB) | The registered (b)(10) EHI export documentation page. Single WordPress page with ~150 words of substance: lists 24 C-CDA sections, describes 4 export formats. No schema, no data dictionary, no sample files. | **Primary but very thin** — the sole EHI-specific artifact |
| `250-70079_CliniComp_EHR_ONC-API_USCDI.pdf` (846 KB, 42 pages) | CliniComp proprietary REST API documentation (P/N 250-70079 Rev D, Jan 2024). Defines 20 USCDI data objects with field-level data dictionaries. Not EHI-export-specific; documents the USCDI query API. Pages 28–42 are Terms of Use. | **Most technically detailed** — only artifact with field-level data definitions |
| `FHIR_Api_2_Merged_20231110_01.pdf` (13.1 MB, 2,155 pages) | Auto-generated HAPI FHIR R4 server API reference. Documents all 148 standard FHIR R4 resource types with generic CRUD operations and `$export` bulk data endpoints. | **Low value for EHI analysis** — generic FHIR R4 reference, not EHI-specific |
| `screenshot-ehi-export-page-full.png` (2.2 MB) | Full-page screenshot of the EHI export page showing the C-CDA sections table and brief export format text. Confirms "Reason for Referral" is duplicated in the table (25 cells, 24 unique sections). | **Confirmatory** |
| `screenshot-certified-ehr-disclosures.png` (2.3 MB) | Full-page screenshot of the Certified EHR Technology – Costs & Disclosures page. Shows CHPL ID, certification date, criteria list, and CQMs. | **Confirmatory** |

## 3. Export Mechanics

- **Format**: C-CDA (Consolidated Clinical Document Architecture) XML, using the CCD (Continuity of Care Document) template. The page specifies "CCDA version 1.0" for direct export and "C-CDA 2.1 XML" for FHIR Bulk Data downloads.
- **Additional formats**: HTML/web page format; FHIR DocumentReference (single patient); FHIR Bulk Data EHI Export (population-level, downloading C-CDA 2.1 XML files).
- **Scope**: "Customers can choose to export EHI datasets for a single patient, or all patients within the selected time range." Both single-patient and bulk export are stated.
- **Mechanism**: The page describes FHIR server-based export (FHIR DocumentReference for single patient, FHIR Bulk Data `$export` for populations). No workflow instructions, screenshots, or step-by-step process documented. The FHIR API PDF documents `$export` endpoints at system (`GET /$export`), Patient (`GET /Patient/$export`, `GET /Patient/{id}/$export`), and Group (`GET /Group/$export`, `GET /Group/{id}/$export`) levels.
- **Access constraints**: The proprietary API documentation notes IP-based restrictions and per-minute query limits. No mention of fees for export.

## 4. Export Content: What's In It

### 4.1 C-CDA Export (primary EHI export)

The EHI export page lists **24 unique C-CDA sections** (25 table cells with "Reason for Referral" duplicated):

| # | C-CDA Section |
|---|---|
| 1 | Admission Diagnosis |
| 2 | Encounter Data |
| 3 | Implantable Devices |
| 4 | Problems |
| 5 | Social History |
| 6 | Allergies |
| 7 | Discharge Medications |
| 8 | Immunization |
| 9 | Procedures |
| 10 | Smoking Status |
| 11 | Assessment |
| 12 | Hospital Discharge Instructions |
| 13 | Functional Status |
| 14 | Plan of Care |
| 15 | Reason for Referral |
| 16 | Care Team |
| 17 | Health Concerns |
| 18 | Medications |
| 19 | Vital Signs |
| 20 | Cognitive Status |
| 21 | Goals |
| 22 | Results |
| 23 | Laboratory Tests |
| 24 | Payers |

These are standard CCD sections. There is **no documentation** of:
- Which C-CDA templates are used for each section
- What coded value sets are applied (SNOMED CT, LOINC, RxNorm, CVX, etc.)
- What optional C-CDA elements are included or excluded
- Whether any vendor extensions or custom sections exist
- Sample C-CDA output files

### 4.2 USCDI API (supplementary, not EHI-export-specific)

The proprietary API documentation (250-70079) defines **20 USCDI data objects** with field-level data dictionaries. These map precisely to USCDI v1 data classes. Each object has a table with columns: NAME, TYPE, NULLABLE, DESCRIPTION, and EHR MAJOR IT (internal field identifier).

**Summary statistics** (verified via `full_entity_inventory.py` → `full-entity-inventory.json`):
- **20 objects** total
- **129 total fields** across all objects
- **81 unique data fields** (excluding infrastructure fields: MRN, nit/Nit, tkey/Tkey/Key that repeat in every object)
- **100% of fields have descriptions** (though many are tautological — e.g., "Race" described as "Race")
- **All fields are typed as String** — no numeric, date, or boolean types
- **No value set bindings** documented (code systems like SNOMED CT, LOINC, CVX are referenced in field names but no formal value set URIs or binding strengths)
- **No foreign keys or relationships** documented

### Vendor's own content organization

The USCDI API organizes data into 20 objects. The C-CDA export lists 24 sections. Both cover essentially the same USCDI v1 data classes:

| USCDI API Object | Fields (total/data) | C-CDA Section Equivalent | Category |
|---|---|---|---|
| Patient_Name | 3 / 1 | (part of header) | Demographics |
| Sex | 3 / 1 | (part of header) | Demographics |
| Date_of_Birth | 3 / 1 | (part of header) | Demographics |
| Race | 4 / 2 | (part of header) | Demographics |
| Ethnicity | 3 / 1 | (part of header) | Demographics |
| Preferred_Language | 3 / 1 | (part of header) | Demographics |
| Smoking_Status | 8 / 5 | Smoking Status, Social History | Social History |
| Problems | 11 / 8 | Problems | Clinical |
| Medications | 8 / 7 | Medications, Discharge Medications | Clinical |
| Medication_Allergies | 10 / 9 | Allergies | Clinical |
| Laboratory_Tests | 7 / 5 | Laboratory Tests | Clinical |
| Laboratory_Values | 9 / 6 | Results | Clinical |
| Vital_Signs | 6 / 4 | Vital Signs | Clinical |
| Implantable_Device | 8 / 5 | Implantable Devices | Clinical |
| Procedures | 10 / 7 | Procedures | Clinical |
| Care_Team_Members | 7 / 4 | Care Team | Clinical |
| Immunizations | 10 / 7 | Immunization | Clinical |
| Health_Concerns | 4 / 1 | Health Concerns | Clinical |
| Assessment_Treatment | 5 / 2 | Assessment | Clinical |
| Goals | 7 / 4 | Goals | Clinical |

C-CDA sections without a corresponding USCDI API object: Admission Diagnosis, Encounter Data, Hospital Discharge Instructions, Functional Status, Plan of Care, Reason for Referral, Cognitive Status, Payers. These are standard CCD sections with no field-level documentation provided.

### 4.3 FHIR Server (generic API reference)

The FHIR API PDF documents a HAPI FHIR R4 server with endpoints for all 148 standard FHIR R4 resource types. It includes `$export` and `$export-poll-status` endpoints. However, this is a generic auto-generated API reference — it does not specify which FHIR resources are actually populated with data, what profiles are used, or what the export output looks like. The document provides **zero EHI-specific information**.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The export covers exactly one thing: **USCDI v1 clinical summary data**, delivered via C-CDA documents. The 24 C-CDA sections and 20 USCDI API objects map precisely to the USCDI v1 data classes required for (g)(10) Standardized API certification. This is the same data set that any ONC-certified EHR must provide through its FHIR API.

The vendor provides no indication that the (b)(10) export goes beyond this clinical summary. There are no vendor-specific tables, no native database entities, no billing/RCM data, no specialty clinical data, no orders, no pharmacy records, no medical device data, no clinical notes beyond the Assessment section.

The deepest objects are Problems (8 data fields including SNOMED-CT and ICD9 codes, onset/resolved/diagnosed dates, and status), Medication Allergies (9 data fields including type, symptoms, severity, RxNorm), and Medications (7 data fields including RxNorm, route, frequency, dose). The thinnest objects are single-field entries like Health Concerns (1 data field), Ethnicity (1 data field), and Assessment Treatment (2 data fields: Assessment and Treatment as free text).

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | 6 USCDI objects (Patient_Name, Sex, DOB, Race, Ethnicity, Preferred_Language) — 7 data fields total | Basic identifiers only. No address, phone, contacts, marital status, employer. The product stores full registration data via patient access services. |
| Encounters / visits | ⚠️ Partial | "Encounter Data" C-CDA section listed, but no field-level documentation | Section name only; no detail on what encounter data is included |
| Problems / conditions | ✅ Covered | Problems object: 8 data fields (name, onset/resolved/diagnosed dates, SNOMED-CT, ICD9, status, acute/chronic) | Reasonably detailed for a summary |
| Medications / prescriptions | ✅ Covered | Medications object: 7 data fields (RxNorm, name, start/end dates, route, frequency, dose) | Medication list only. No dispensing records, no BCMA logs, no compounding records — all of which the product stores |
| Allergies | ✅ Covered | Medication_Allergies object: 9 data fields (type, name, onset, symptoms, severity, RxNorm) | Medication allergies only — no food or environmental allergies documented |
| Immunizations | ✅ Covered | Immunizations object: 7 data fields (CVX, vaccine name, admin date, status, lot, manufacturer, notes) | Adequate for immunization records |
| Vitals | ✅ Covered | Vital_Signs object: 4 data fields (name, timing, value, unit) | Basic vital signs |
| Lab results | ✅ Covered | Laboratory_Values (6 data fields) + Laboratory_Tests (5 data fields) | LOINC-coded results with values, units, ranges. Reasonable coverage |
| Imaging / diagnostic reports | ❌ Not covered | No radiology sections, no imaging references | Product has integrated RIS/PACS. **Significant gap.** |
| Procedures | ✅ Covered | Procedures object: 7 data fields (name, date, status, target site, CCI/ICD9/SNOMED codes) | Coded procedure list |
| Clinical notes / documents | ⚠️ Partial | "Assessment" and "Hospital Discharge Instructions" C-CDA sections | Only assessment/discharge instructions. No progress notes, H&P, consult notes, flowsheet data, operative notes — all core to this ICU/hospital EHR. **Major gap.** |
| Care plans / goals | ✅ Covered | Goals object (4 data fields), Health Concerns (1 data field), Assessment_Treatment (2 data fields), Plan of Care C-CDA section | Present but thin |
| Orders / referrals | ❌ Not covered | "Reason for Referral" C-CDA section only (no field detail). No order data. | Product has full CPOE. **Significant gap.** |
| Insurance / coverage | ⚠️ Partial | "Payers" C-CDA section listed, no field-level documentation | Section name only; no detail on what payer data is included |
| Claims / billing | ❌ Not covered | No billing entities in export | Product has full RCM suite (charges, claims, payments, eligibility, coding). **Major gap.** |
| Payments | ❌ Not covered | No payment data in export | Product processes payments. **Significant gap.** |
| Consents / directives | ❌ Not covered | No consent data in export | N/A — not a documented product feature |
| Patient communications / portal messages | ❌ Not covered | No patient communication data | Product is certified for (e)(1) patient view/download/transmit. Gap uncertain — portal feature details are thin. |
| Specialty: Perinatal/Neonatal | ❌ Not covered | No perinatal data in export | Product has specialized neonatal/perinatal module with fetal monitoring, growth curves, specialized dosing. **Significant gap.** |
| Specialty: ED | ❌ Not covered | No ED-specific data in export | Product has ED-specific documentation module. **Gap.** |
| Specialty: Perioperative/PACU | ❌ Not covered | No perioperative data in export | Product has perioperative/PACU module. **Gap.** |
| Specialty: Behavioral Health | ❌ Not covered | No behavioral health data in export | Product supports behavioral health settings. **Gap.** |
| Medical device data | ❌ Not covered | No device data (beyond implantable device list) | Product captures waveforms, parameters, settings from hundreds of bedside devices. **Significant gap.** |
| Pharmacy (dispensing, compounding) | ❌ Not covered | No pharmacy data in export | Product has full pharmacy IS with compounding, dispensing, BCMA. **Significant gap.** |

**Summary**: Of approximately 20 applicable EHI domains for this comprehensive hospital EHR, the export covers 7 fully, 4 partially, and 9+ are entirely absent. The covered domains represent the USCDI v1 clinical summary — the exact data already available through the mandatory (g)(10) FHIR API.

## 6. Documentation Quality

**Overall**: Poor. The documentation is insufficient for a developer to build an import or understand what data the export actually contains.

**EHI Export Page** (`ehi-data-export-details.html`):
- ~150 words of substantive content on a single web page
- Lists 24 C-CDA section names in a 5×5 table (with one duplicate)
- No field-level documentation for any C-CDA section
- No C-CDA template references, no coded value set specifications
- No sample export files (C-CDA XML, HTML, or FHIR)
- No workflow instructions for initiating an export
- No description of the FHIR Bulk Data export process beyond one sentence
- Published 2023-11-07, last modified 2023-11-09

**USCDI API PDF** (250-70079, 42 pages):
- Well-structured with field-level data dictionaries for 20 objects
- Includes field names, types (all String), nullability, descriptions, and internal EHR field identifiers ("Major IT" numbers)
- Sample API requests and JSON response examples included
- However, this documents the USCDI query API, not the (b)(10) export itself
- Descriptions are mostly tautological (e.g., "Race" described as "Race", "LOINC Code" described as "LOINC Code")
- No value set URIs or binding documentation
- 14 of 42 pages are Terms of Use

**FHIR API PDF** (2,155 pages):
- Auto-generated HAPI FHIR R4 reference covering all 148 resource types
- Zero EHI-specific content
- Documents `$export` endpoints exist but nothing about what data they return
- Size (2,155 pages) is grossly disproportionate to informational value for EHI analysis

**Machine-readable artifacts**: None. No JSON schemas, no XSD schemas, no sample data files, no data dictionaries in machine-readable format.

**Could a developer build an import?** No. A developer would know the export produces C-CDA XML with up to 24 standard sections, but would have no specification of which C-CDA templates, which optional elements, what coded values, or what the actual output looks like. The USCDI API documentation provides field-level detail, but only for 20 objects that map to standard USCDI data classes and only for the proprietary JSON API — not for the C-CDA export.

## 7. Overall Assessment

### Classification

**Standard-based projection.** The (b)(10) EHI export is a C-CDA clinical summary repackaged as the EHI export. The 24 C-CDA sections and 20 USCDI API objects map precisely to USCDI v1 data classes — the identical data set already required for (g)(10) FHIR API certification. There is no evidence of any native database model export, no vendor-specific data entities, and no coverage of the many data domains this comprehensive hospital EHR stores beyond clinical summaries.

### Key Findings

1. **The (b)(10) export is functionally identical to the (g)(10) clinical summary.** The 24 C-CDA sections listed exactly match standard CCD sections, and the 20 USCDI API objects are the USCDI v1 data classes. There is no additional data beyond what the FHIR API already provides. This is a textbook case of C-CDA/FHIR repackaging as "(b)(10)."

2. **Entire major data domains are absent.** The product stores deep revenue cycle data (charges, claims, payments, eligibility, coding), pharmacy data (dispensing, compounding, BCMA), clinical orders (CPOE), medical device waveforms, radiology/imaging, and specialty clinical data (neonatal, perioperative, ED, behavioral health). None of this appears in the export.

3. **Documentation is extremely thin.** The registered EHI export page contains approximately 150 words of substance — a 5×5 table of C-CDA section names and four bullet points about export formats. No field-level documentation, no sample data, no schemas, no workflow instructions.

4. **The USCDI API documentation is well-structured but off-target.** The 42-page API PDF (250-70079) is the only artifact with field-level data definitions, but it documents a proprietary USCDI query API, not the (b)(10) export. Its 20 objects with 129 fields (81 unique data fields) cover only the USCDI v1 data set.

5. **Internal field identifiers hint at a much deeper data model.** The "EHR MAJOR IT" column in the USCDI API documentation references internal field numbers (e.g., "14074 labresult_ID", "2225 meds_flow_definition", "27836 ImplantableDeviceUDI") that reveal the native data model has thousands of fields. Only ~80 are surfaced through the export.

### Summary Stats

```
Classification:  Standard-based projection
Export format:   C-CDA XML (v1.0 and v2.1), HTML, FHIR DocumentReference
Model type:      Standard projection (C-CDA CCD)
Entities:        20 USCDI API objects / 24 C-CDA sections
Fields:          129 total (81 unique data fields) via USCDI API; C-CDA fields undocumented
Descriptions:    100% (via USCDI API; mostly tautological)
Sample data:     No
Bulk export:     Yes (FHIR Bulk Data with C-CDA 2.1 output)
Domains covered: 7 of 20+ applicable domains
```

### Bottom Line

CliniComp|EHR is a comprehensive hospital information system storing data across clinical, pharmacy, billing, imaging, medical devices, and multiple specialty domains. The (b)(10) export provides only a C-CDA clinical summary — the same USCDI v1 data set available through any certified EHR's FHIR API. A patient or provider would get a basic clinical summary (demographics, problems, meds, labs, vitals, allergies, immunizations, procedures) but would miss the vast majority of their health information: billing records, clinical notes, orders, pharmacy dispensing, device data, imaging reports, and all specialty-specific documentation. The single biggest gap is the complete absence of any mechanism to export the product's native data model.
