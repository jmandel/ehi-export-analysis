# EHI Export Analysis: CliniComp, Intl.

**Product**: CliniComp|EHR v213.03
**Analysis date**: 2026-02-16
**CHPL ID**: 15.05.05.2695.CLIN.02.01.1.221013 (CHPL #10998)

## 1. Product Context

CliniComp|EHR is a **comprehensive, enterprise-wide inpatient EHR** built for high-acuity hospital environments, primarily deployed in U.S. Department of Defense and Veterans Administration medical centers. It is a full hospital information system — not a specialty or ambulatory-only tool.

The product includes:
- **Clinical documentation & charting**: flowsheets, multidisciplinary charting across ICU, ED, med-surg, ambulatory, perioperative
- **CPOE**: integrated order entry for meds, labs, radiology
- **Medication management**: BCMA, pharmacy dispensing, compounding records, drug interaction checking
- **Pharmacy Information System**: dispensing, compounding, after-hours operations, cost tracking
- **Laboratory Information System**: chemistry, microbiology, molecular, pathology, specimen tracking, blood bank
- **Radiology (RIS) & Imaging (PACS)**: integrated radiology and image management
- **Medical device integration**: automated data capture from bedside monitors, ventilators, pumps, anesthesia equipment; waveform capture
- **Perinatal/neonatal**: fetal surveillance, growth curves, specialized neonatal dosing
- **Emergency Department**: ED-specific documentation
- **Perioperative/PACU**: pre-op through post-op documentation
- **Behavioral health**: listed as supported (details sparse)
- **Revenue Cycle Management**: eligibility verification, automated charge capture, medical coding, billing/claims generation, payment applications, KPI reporting
- **Patient portal**: certified for (e)(1) view/download/transmit

This breadth means a genuine (b)(10) export should cover clinical documentation (including flowsheets, notes, specialty data), orders, pharmacy records, lab results beyond summary values, radiology reports, device data, billing/claims, and more.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/ehi-data-export-details.html` (43 KB) | The registered (b)(10) EHI export documentation page. Single WordPress page listing 24 C-CDA sections and describing 4 export formats. ~150 words of substance. | **Low** — lists section names but no field-level detail, no schema, no sample data |
| `downloads/250-70079_CliniComp_EHR_ONC-API_USCDI.pdf` (42 pages, 846 KB) | CliniComp proprietary REST API documentation for USCDI data. Defines 20 CCDS/USCDI objects with field-level data dictionaries. Rev D, Jan 2024. | **Medium** — provides field-level detail but only for USCDI-scope data |
| `downloads/FHIR_Api_2_Merged_20231110_01.pdf` (2,155 pages, 13.1 MB) | Auto-generated HAPI FHIR R4 server API reference. Generic FHIR endpoint documentation for all R4 resource types. | **Minimal** — generic FHIR API dump, not EHI-specific |
| `downloads/screenshot-ehi-export-page-full.png` (2.2 MB) | Full-page screenshot of the EHI export documentation page | Confirms HTML content |
| `downloads/screenshot-certified-ehr-disclosures.png` (2.3 MB) | Screenshot of the Certified EHR Technology disclosures page | Shows link structure |

## 3. Export Mechanics

- **Format**: C-CDA XML (versions 1.0 and 2.1), HTML, FHIR DocumentReference (single patient), FHIR Bulk Data (population). Also a proprietary JSON API for USCDI data.
- **Mechanism**: FHIR Bulk Data `$export` for population-level; FHIR DocumentReference for single-patient; proprietary REST API (`/Api/getData`). Bulk data downloads produce C-CDA 2.1 XML files (not FHIR NDJSON).
- **Single-patient vs bulk**: Both supported. "Customers can choose to export EHI datasets for a single patient, or all patients within the selected time range."
- **Access constraints**: The proprietary API requires IP whitelisting, per-minute query limits, and page size restrictions. API access requires a user account with API permissions. Terms of Use span 15 pages.
- **Fees**: Not explicitly stated as free or paid; Terms of Use (section 6.2.3) reserve the right to charge fees.

## 4. Export Content: What's In It

### Data Dictionary (Proprietary API)

The USCDI API documentation (250-70079) defines **20 CCDS objects** with **129 total fields** (81 substantive, 48 metadata fields for MRN/nit/tkey). Every field has: name, type (all String), nullable flag, description, and EHR Major IT identifier.

All fields are typed as `String`. No value sets, code system bindings, or enumerated values are documented beyond noting which standard code applies (SNOMED-CT, LOINC, CVX, RxNorm, ICD-9). No foreign key relationships are documented. No sample export files are provided.

### C-CDA Sections

The HTML page lists 24 C-CDA sections (after deduplication of "Reason for Referral" which appeared twice):

Admission Diagnosis, Encounter Data, Implantable Devices, Problems, Social History, Allergies, Discharge Medications, Immunization, Procedures, Smoking Status, Assessment, Hospital Discharge Instructions, Functional Status, Plan of Care, Reason for Referral, Care Team, Health Concerns, Medications, Vital Signs, Cognitive Status, Goals, Results, Laboratory Tests, Payers

No field-level documentation is provided for the C-CDA export — only section names. No C-CDA templates specified, no value set bindings, no optional element documentation.

### Vendor's own content organization

The vendor organizes USCDI data into objects named with a "CCDS." prefix. All are clinical or demographic; none address billing, orders, notes, or specialty data.

| Entity/Object | Total Fields | Substantive Fields | Category |
|---|---|---|---|
| Patient Name | 3 | 1 | Demographics |
| Sex | 3 | 1 | Demographics |
| Date of Birth | 3 | 1 | Demographics |
| Race | 4 | 2 | Demographics |
| Ethnicity | 3 | 1 | Demographics |
| Preferred Language | 3 | 1 | Demographics |
| Smoking Status | 8 | 5 | Clinical |
| Problems | 11 | 8 | Clinical |
| Medication | 8 | 7 | Clinical |
| Medication Allergies | 10 | 9 | Clinical |
| Laboratory Tests | 7 | 5 | Clinical |
| Laboratory Values | 9 | 6 | Clinical |
| Vital Signs | 6 | 4 | Clinical |
| Implantable Device | 8 | 5 | Clinical |
| Procedures | 10 | 7 | Clinical |
| Care Team Members | 7 | 4 | Clinical |
| Immunizations | 10 | 7 | Clinical |
| Health Concerns | 4 | 1 | Clinical |
| Assessment Treatment | 5 | 2 | Clinical |
| Goals | 7 | 4 | Clinical |
| **Totals** | **129** | **81** | |

Full entity-level JSON at `analysis/entity-inventory-full.json`; summary at `analysis/entity-inventory-summary.json`.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor's export covers exactly two categories:

**Demographics** (6 objects, 7 substantive fields): Patient name, sex, DOB, race (with secondary race), ethnicity, preferred language. This is the bare minimum for patient identification. No address, phone, email, emergency contact, marital status, or next of kin.

**Clinical summary data** (14 objects, 74 substantive fields): Problems (with SNOMED-CT, ICD-9, onset/resolved/diagnosed dates, status, severity), medications (RxNorm, name, route, frequency, dose, dates), medication allergies (type, name, symptom, severity, RxNorm, onset), lab tests and values (LOINC, name, value, unit, range), vital signs (name, value, unit), procedures (SNOMED-CT, ICD-9, CCI code, name, date, status, target site), immunizations (CVX, lot, manufacturer, status, date), implantable devices (UDI, SNOMED-CT, device ID), care team members (team, facility, address, phone), smoking status (SNOMED-CT, dates), health concerns, assessment/treatment, goals.

**Not covered at all (0 objects)**: Billing/revenue cycle, clinical notes/documentation, orders/CPOE data, pharmacy dispensing records, medical device integration data (waveforms, parameters), radiology/imaging reports, encounter details beyond an ID, insurance/payer details (listed as a C-CDA section but no API object or field documentation), documents/attachments, patient communications, perinatal/neonatal specialty data, ED-specific records, perioperative records, behavioral health records.

The 20 CCDS objects map precisely to **USCDI v1** data classes. This is a clinical exchange data set — the exact same scope as (g)(10) FHIR API certification — relabeled as (b)(10).

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | 6 CCDS objects (7 substantive fields): name, sex, DOB, race, ethnicity, language | Minimal demographics — no address, phone, email, emergency contacts, marital status. Product stores full registration data. |
| Encounters / visits | ⚠️ Partial | "Encounter Data" listed as C-CDA section; no API object or field-level detail | Product has full encounter management; export provides no encounter field documentation |
| Problems / conditions | ✅ Covered | `CCDS.Problems`: 8 substantive fields including SNOMED-CT, ICD-9, onset/resolved dates, status, severity | Reasonable for a summary; likely missing internal problem list detail |
| Medications / prescriptions | ⚠️ Partial | `CCDS.Medications`: 7 fields (RxNorm, name, route, frequency, dose, dates) | Summary-level only — no prescriber, no pharmacy dispense, no MAR data. Product has full pharmacy system. |
| Allergies | ✅ Covered | `CCDS.Medication_Allergies`: 9 substantive fields | Labeled "medication allergies" — unclear if food/environmental allergies are included |
| Immunizations | ✅ Covered | `CCDS.Immunizations`: 7 substantive fields (CVX, name, date, status, lot, manufacturer, notes) | Adequate for USCDI scope |
| Vitals | ✅ Covered | `CCDS.Vital_Signs`: 4 substantive fields (name, timing, value, unit) | Summary-level; product captures continuous bedside monitoring data |
| Lab results | ✅ Covered | `CCDS.Laboratory_Values` + `CCDS.Laboratory_Tests`: 11 substantive fields | Product has full LIS; export provides summary values only |
| Imaging / diagnostic reports | ❌ Not covered | Not present in export | Product has integrated RIS/PACS — significant gap |
| Procedures | ✅ Covered | `CCDS.Procedures`: 7 substantive fields | Summary-level |
| Clinical notes / documents | ❌ Not covered | No notes entities in API; some C-CDA sections (Assessment, Discharge Instructions) may contain narrative text | Product has extensive clinical documentation — flowsheets, progress notes, H&P, consult notes, discharge summaries. Major gap. |
| Care plans / goals | ✅ Covered | `CCDS.Goals` + `CCDS.Assessment_Treatment` + `CCDS.Health_Concerns`: 7 substantive fields | Thin — goals have 4 substantive fields; health concerns has 1 |
| Orders / referrals | ❌ Not covered | Not present in export | Product has full CPOE — significant gap |
| Insurance / coverage | ⚠️ Partial | "Payers" listed as C-CDA section; no API object or field documentation | Product has full eligibility verification and coverage management |
| Claims / billing | ❌ Not covered | Not present in export | Product has full RCM suite (charges, claims, payments, coding) — **major gap** |
| Payments | ❌ Not covered | Not present in export | Product handles payment applications — gap |
| Consents / directives | ❌ Not covered | Not present in export | N/A — unclear if product stores these discretely |
| Patient communications | ❌ Not covered | Not present in export | Product has patient portal (e)(1) — likely gap |
| Specialty: Perinatal/Neonatal | ❌ Not covered | Not present in export | Product has specialized perinatal/neonatal module — gap |
| Specialty: ED | ❌ Not covered | Not present in export | Product has ED module — gap |
| Specialty: Perioperative | ❌ Not covered | Not present in export | Product has perioperative/PACU — gap |
| Specialty: Behavioral Health | ❌ Not covered | Not present in export | Product supports behavioral health — gap |
| Medical devices (data) | ❌ Not covered | `CCDS.Implantable_Device` covers device registry only, not captured device data | Product captures waveforms, parameters, settings from bedside devices — gap |

**Domains covered**: 7 of 19 applicable domains (✅ or ⚠️)
**Domains missing**: 12 of 19 applicable domains

## 6. Documentation Quality

**Strengths:**
- The USCDI API PDF (250-70079) is well-structured with field-level data dictionaries for each object
- Every field has name, type, nullable flag, description, and internal EHR Major IT identifier
- Sample API requests, JSON responses, and error handling are documented
- The EHR Major IT identifiers provide a partial window into the internal database schema

**Weaknesses:**
- The EHI export page itself has ~150 words of substance — no schema, no examples, no field descriptions
- C-CDA export has zero field-level documentation — only 24 section names
- The 2,155-page FHIR PDF is a generic HAPI FHIR API dump with no EHI-specific content
- All 129 fields are typed as `String` — no numeric, date, boolean, or coded types
- No value sets or code system bindings are specified for coded fields
- No sample export data files (no sample C-CDA, no sample bulk export output)
- No documentation of the FHIR Bulk Data Export workflow (initiation, polling, retrieval)
- No foreign key relationships or entity associations documented
- "CCDA version 1.0" is ambiguous (C-CDA 1.1 was the first published version)

**Could a developer build an import?** Partially — the proprietary API JSON format is documented enough to query USCDI data, but the C-CDA and FHIR Bulk Data exports have no product-specific documentation. A developer would need to rely on generic C-CDA/FHIR specs and reverse-engineer CliniComp's implementation.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Minimal/stub**

The export covers exactly the USCDI v1 data classes — the same scope as (g)(10) clinical exchange certification. For a product that stores ICU waveform data, full pharmacy records, radiology images, perioperative documentation, ED records, neonatal data, and a complete revenue cycle management suite, exporting only 20 USCDI summary objects with 81 substantive fields represents a tiny fraction of the designated record set. The 24 C-CDA sections are standard clinical summary sections; none address billing, specialty clinical data, orders, or detailed documentation.

The EHR Major IT identifiers in the USCDI PDF reveal numbered internal fields (e.g., 27836, 27841, 19074-19895) suggesting a database with thousands of data points, yet only ~80 are surfaced in the export. This is a clinical exchange surface, not the designated record set.

**Axis 2 — Export approach: Repackaged existing export**

The export is clearly the vendor's existing clinical exchange capability (USCDI/C-CDA) relabeled as (b)(10). Key evidence:
1. The 20 CCDS objects map 1:1 to USCDI v1 data classes
2. The API document is titled "Web API & USCDI Dataset" — it was built for USCDI compliance, not (b)(10)
3. The C-CDA sections are standard CCD template sections
4. The FHIR Bulk Data endpoint produces C-CDA 2.1 documents (not a custom export format)
5. No billing, specialty, orders, or detailed clinical documentation is included — exactly the gap between (g)(10) and (b)(10)
6. The proprietary API predates the (b)(10) requirement and was designed for USCDI clinical exchange

### Key Findings

1. **Export is a relabeled USCDI/C-CDA clinical exchange.** The 20 CCDS objects and 24 C-CDA sections match USCDI v1 exactly. No data beyond the clinical exchange floor is exported. (Sources: `ehi-data-export-details.html`, `250-70079_CliniComp_EHR_ONC-API_USCDI.pdf` §3.1)

2. **Revenue cycle management — the product's major non-clinical capability — is entirely absent.** CliniComp|EHR has a full RCM suite (charges, claims, payments, eligibility, coding), but zero billing entities appear in the export. (Source: `product-research.md` lines 111-118 vs export content)

3. **Clinical notes and documents are not exported.** The product stores flowsheets, progress notes, H&P, discharge summaries, consult notes, and multidisciplinary charting — none of which have dedicated export objects. The C-CDA may contain some narrative text in sections like "Assessment" but there is no documentation of this.

4. **Only 81 substantive fields across the entire export.** For a full hospital EHR with ICU device integration, pharmacy, LIS, RIS/PACS, and specialty modules, this represents a fraction of the data stored about patients. The EHR Major IT numbers suggest the internal database has thousands of data points.

5. **No sample data or machine-readable schemas.** The documentation provides no sample C-CDA files, no sample FHIR Bulk Data output, no JSON schemas, and no XSD schemas. A developer cannot validate an implementation against reference output.

### Summary Stats

    Coverage:        Minimal/stub
    Approach:        Repackaged existing export
    Export format:   C-CDA XML (1.0/2.1), HTML, FHIR DocumentReference, proprietary JSON API
    Entities:        20 (USCDI objects)
    Fields:          129 total (81 substantive, 48 metadata)
    Descriptions:    100% of fields have descriptions
    Sample data:     No
    Bulk export:     Yes (FHIR Bulk Data producing C-CDA 2.1 files)
    Domains covered: 7 of 19 applicable domains

### Bottom Line

CliniComp's (b)(10) export is their existing USCDI/C-CDA clinical exchange relabeled — 20 summary objects with 81 substantive fields for a product that stores ICU waveforms, full pharmacy records, a complete revenue cycle, and specialty clinical data across perinatal, ED, perioperative, and behavioral health settings. The single biggest gap is that the entire revenue cycle management suite — one of the product's core capabilities — produces zero export data.
