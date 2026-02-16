# EHI Export Analysis: Magilen Enterprises Inc

**Product**: QSmartCare  
**Analysis date**: 2026-02-16  
**CHPL ID**: 15.05.05.3098.MAGE.01.00.1.220127

## 1. Product Context

QSmartCare is a specialty wound care EHR built by Magilen Enterprises Inc, the technology arm of Quality Surgical Management (QSM). QSM is a wound care services company providing bedside wound care in skilled nursing facilities (SNFs) across six states. QSmartCare is used exclusively by QSM — it is not sold to external customers.

**Core capabilities relevant to EHI completeness:**
- **Wound care charting** (primary function): wound assessments, measurements, photographs, healing progress, treatment documentation
- **Patient demographics**: imported from host facility EHRs (e.g., MatrixCare integration)
- **Clinical documentation**: encounters, diagnoses, HPI, care plans, vitals, medications, allergies, procedures, immunizations
- **Specialty wound data**: wound location, dimensions, stage/grade, wound bed characteristics, treatment protocols
- **Billing/coding**: the company employs billers and coders, but it is unclear whether billing is performed within QSmartCare or via a separate system
- **Patient portal**: certified for (e)(1) but low actual usage
- **FHIR API**: 21 FHIR R4 resources via (g)(10) certification

The product is a small, focused specialty EHR. The designated record set should primarily cover wound care clinical data, demographics, encounters, diagnoses, medications, labs, vitals, and possibly billing.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/ehi-template.html` (61 KB) | Main EHI documentation page — procedural walkthrough with screenshots showing how to export. No data dictionary. | Low — process docs only |
| `downloads/Single-Patient-PDF-Download.pdf` (40 KB, 7 pages) | Sample single-patient export in PDF format. Shows all 34 data sections with test data for patient "John Doe". | **High** — primary evidence of export content |
| `downloads/sample-ehi-export.json` (8 KB) | Sample single-patient export in proprietary JSON format. Contains ~20 sections with FHIR-like labels but non-FHIR structure. Less complete than PDF. | **High** — shows machine-readable format |
| `downloads/screenshots/` (22 images) | Screenshots of the export UI workflow — login, navigation, single/multi patient export, downloaded files. | Medium — confirms export mechanics |

**Most informative**: The sample PDF and JSON exports are the primary evidence of what the export contains. The EHI documentation page is procedural only — it describes *how* to export but not *what* is exported.

**Key gap**: There is **no data dictionary**. The vendor provides no documentation of field names, types, descriptions, value sets, or relationships. The only evidence of export content comes from the two sample files.

## 3. Export Mechanics

- **Format**: PDF (human-readable) and proprietary JSON (machine-readable). The JSON uses FHIR-like `resourceType` labels (e.g., `"resourceType": "Patient"`) but is **not FHIR-compliant** — field names, nesting, and structure differ from FHIR R4.
- **Mechanism**: UI-based. Navigate to Patient > CCDA > Export. Click "EHI data PDF" or "EHI data Json" icon.
- **Single-patient**: Downloads a PDF or JSON file directly.
- **Multi-patient**: Select multiple patients via checkboxes; downloads a ZIP file containing one PDF or JSON per patient.
- **Access**: Requires Author-level permissions within QSmartCare.
- **Fees**: No fees mentioned in documentation.
- **Bulk**: Multi-patient export is supported (ZIP of individual files), but there is no API-based bulk export.

## 4. Export Content: What's In It

### No data dictionary exists

The vendor provides **zero documentation** of the export's data model. No field definitions, no types, no descriptions, no value sets, no relationships. All content analysis below is derived from inspecting the two sample export files.

### JSON export analysis

The JSON export contains a single root object `object.organization` with 26 top-level keys. It is a flat, non-normalized proprietary structure. Notable limitations vs. the PDF:
- Missing: insurance, patient relationships, spouse info, past medical history, anticoagulant details, lab results, blood sugar, individual vital sign tables (BP, pulse, temp, etc.), past surgical histories, family history, functional/cognitive status
- Diagnosis keys are numbered (`codeSystemICD100`, `codeSystemICD101`, ...) rather than using arrays — fragile and non-standard
- Procedure keys are numbered (`content0`, `content1`) rather than using arrays
- Many fields contain `"null"` as a string rather than actual null values

### PDF export analysis (more complete)

The PDF export contains **34 distinct sections** across 7 pages. This is the most complete view of the export:

### Vendor's own content organization

| Section | Fields | Source | Category |
|---|---|---|---|
| Demographics | 24 | PDF | Patient |
| Organization | 5 | PDF | Administrative |
| Organization Address | 6 | PDF | Administrative |
| Location | 7 | PDF | Administrative |
| Care Team | 4 | PDF | Clinical |
| Encounters | 4 | PDF | Clinical |
| History of Present Illness | 1 | PDF | Clinical |
| Social History | 1 | PDF | Clinical |
| Family History | 1 | PDF | Clinical |
| Assessment and Plan of Treatment | 2 | PDF | Clinical |
| Patient Relationship | 2 | PDF | Patient |
| Insurance | 2 | PDF | Insurance |
| Spouse | 5 | PDF | Patient |
| Past Medical History | 5 | PDF | Clinical |
| Anticoagulant | 1 | PDF | Clinical |
| Patient Wound | 8 | PDF | **Wound Care** |
| Implantable Device | 12 | PDF | Clinical |
| Medications | 5 | PDF | Clinical |
| Diagnosis | 5 | PDF | Clinical |
| Lab | 4 | PDF | Clinical |
| Blood Pressure | 3 | PDF | Vitals |
| Blood Sugar | 4 | PDF | Vitals |
| BMI | 4 | PDF | Vitals |
| Pulse | 2 | PDF | Vitals |
| Pulse Oximetry | 2 | PDF | Vitals |
| Body Temperature | 2 | PDF | Vitals |
| Heart Rate | 2 | PDF | Vitals |
| Respiratory Rate | 2 | PDF | Vitals |
| Oxygen Concentration | 2 | PDF | Vitals |
| Past Surgical Histories | 6 | PDF | Clinical |
| Immunization | 6 | PDF | Clinical |
| Functional Status | 4 | PDF | Clinical |
| Cognitive Status | 4 | PDF | Clinical |
| Assessment Notes | 2 | JSON | Clinical |

**Total: 34 sections, 149 fields, 0 field descriptions (0%).**

Full inventory saved to `analysis/entity-inventory-full.json`.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The export covers a broad set of clinical categories organized as flat sections in the PDF. The content closely mirrors what you'd find in a C-CDA clinical summary, plus a few wound-care-specific additions:

**Strongest areas:**
- **Demographics** (24 fields) — most detailed section, includes race, ethnicity, language, granular race, SSN, multiple addresses
- **Wound data** (8 fields) — wound location, side, sub-location, vertical/horizontal plane, status, DOS. This is wound-care-specific data that goes beyond USCDI
- **Vitals** — broken out into 9 separate sections (BP, blood sugar, BMI, pulse, SpO2, temperature, HR, RR, O2 concentration) with date tracking
- **Implantable devices** (12 fields) — UDI, manufacturer, brand, model, MRI safety, NRL, GMDN, FDA codes

**Thinnest areas:**
- **Insurance** — only 2 fields (primary and secondary insurance names). No policy numbers, group numbers, coverage dates, subscriber info
- **Labs** — only 4 fields (Date, Path, Lab Name, Lab Location). No actual result values, reference ranges, or test codes
- **History of Present Illness**, **Social History**, **Family History** — each just 1 free-text field
- **Anticoagulant** — just the medication name; no dose, frequency, start date

**Missing entirely:**
- No billing/claims data
- No clinical notes beyond HPI and assessment
- No portal messages or patient communications
- No wound photographs (despite this being a wound care product with photo capability)
- No detailed wound measurements (dimensions, depth, stage/grade, wound bed description, exudate, periwound)

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | Demographics section (24 fields) | Thorough — includes race, ethnicity, language, granular race |
| Encounters / visits | ⚠️ Partial | Encounters section (4 fields: Consult For, Chief Complaints, DOS, Smoking Status) | Minimal — no encounter type, duration, disposition, facility |
| Problems / conditions / diagnoses | ✅ Covered | Diagnosis (5 fields) + Past Medical History (5 fields) with ICD-10 codes, dates, status | Adequate |
| Medications / prescriptions | ⚠️ Partial | Medications (5 fields: name, indication, dosage, frequency, status) + Anticoagulant (1 field) | Missing: prescriber, pharmacy, start/end dates, RxNorm codes |
| Allergies | ⚠️ Partial | In JSON only (allergy name + SNOMED code). Not a distinct PDF section (visible in medication area) | Thin — no reaction, severity, onset |
| Immunizations | ✅ Covered | Immunization section (6 fields: vaccine code, code system, name, date, status, notes) | Adequate |
| Vitals | ✅ Covered | 9 separate vital sign sections with date tracking | Thorough — BP, blood sugar, BMI, pulse, SpO2, temp, HR, RR, O2 |
| Lab results | ⚠️ Partial | Lab section (4 fields: Date, Path, Lab Name, Lab Location) | **Significant gap** — no actual result values, units, reference ranges |
| Imaging / diagnostic reports | ❌ Not covered | No imaging sections in export | Product may not do imaging beyond wound photos; wound photos themselves are missing |
| Procedures | ✅ Covered | Past Surgical Histories (6 fields with CPT/SNOMED codes) | Adequate |
| Clinical notes / documents | ⚠️ Partial | HPI (1 field), Assessment & Plan (2 fields) | Thin — no progress notes, consultation notes, or other note types |
| Care plans / goals | ⚠️ Partial | Assessment & Plan section (2 fields) + Goals in JSON | Minimal structure |
| Orders / referrals | ❌ Not covered | No order or referral sections | May not be a major product feature |
| Insurance / coverage | ⚠️ Partial | Insurance section — only primary and secondary insurer names | **Significant gap** — no policy details, dates, subscriber info |
| Claims / billing | ❌ Not covered | No billing, charges, or claims data in export | Unclear if billing is in QSmartCare or separate system |
| Payments | ❌ Not covered | No payment data | Likely handled outside QSmartCare |
| Consents / directives | ❌ Not covered | No consent or directive sections | May not be stored |
| Patient communications | ❌ Not covered | No portal messages or communication records | Product has patient portal but low usage |
| Specialty-specific (wound care) | ⚠️ Partial | Patient Wound (8 fields: wound #, DOS, location, side, sub-location, planes, status) | **Critical gap** — product is a wound care EHR but export only has basic wound location/status. Missing: wound dimensions, depth, stage/grade, wound bed description, exudate, periwound condition, treatment details, healing trajectory, wound photographs |

## 6. Documentation Quality

**Documentation is poor.** The EHI documentation page (`ehi-template.html`) is entirely procedural — it describes how to click buttons to export, with screenshots. It contains:
- No data dictionary
- No field definitions, types, or descriptions
- No schema documentation
- No value set documentation
- No relationship/FK documentation

The only way to understand what's in the export is to examine the sample files. The JSON sample is partially useful as a machine-readable format, but it is non-standard (not FHIR), inconsistently structured (numbered keys instead of arrays), and less complete than the PDF.

**Could a developer build an import from this documentation?** No. A developer would need to reverse-engineer the JSON structure from sample data and guess at field semantics. The PDF is human-readable but not machine-parseable. There is no schema, no API spec, and no documentation of the data model.

**0 out of 149 fields have descriptions.** Field names are the only semantic information available.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Partial**

The export covers the basic clinical categories you'd expect in a C-CDA summary (demographics, diagnoses, medications, allergies, vitals, procedures, immunizations) plus wound location/status data. However, for a wound care EHR, the wound data section is surprisingly thin — only 8 fields covering location and status, missing the detailed wound assessment data (dimensions, depth, stage, wound bed, exudate, periwound, treatment details) that is the product's core clinical value. Labs are structurally present but lack actual result values. Insurance has only insurer names. Clinical notes are minimal. There is no billing data, though it's unclear whether billing lives in QSmartCare.

**Axis 2 — Export approach: Purpose-built EHI export (minimal effort)**

This is not a repackaged C-CDA or FHIR export — the vendor built a custom PDF/JSON export with a proprietary structure that includes sections like "Anticoagulant," "Patient Wound," "Blood Sugar," and "Spouse" that wouldn't appear in a standard C-CDA or FHIR Bulk Data export. The export is accessed via a dedicated "EHI data" button (separate from the C-CDA export). However, the effort invested appears minimal: no data dictionary, a fragile JSON format with numbered keys, and shallow coverage of the product's core wound care data.

### Key Findings

1. **The wound care data — the product's raison d'être — is thinly exported.** The "Patient Wound" section has 8 fields (location, side, planes, status) but is missing wound dimensions, depth, stage/grade, wound bed characteristics, exudate, periwound condition, treatment protocols, and wound photographs. For a product described as purpose-built for wound care documentation over 30+ years, this is a significant gap.

2. **No data dictionary exists.** Zero fields out of 149 have descriptions, types, value sets, or relationship documentation. The only way to understand the export is to inspect the two sample files.

3. **The JSON format is non-standard and fragile.** Despite using FHIR-like `resourceType` labels, the JSON structure is proprietary. Diagnoses and procedures use numbered keys (`codeSystemICD100`, `content0`) instead of arrays, many fields contain the string `"null"` instead of actual null, and the JSON export is missing ~14 sections that appear in the PDF.

4. **Lab results section is empty in practice.** The Lab section has column headers (Date, Path, Lab Name, Lab Location) but no fields for actual result values, units, or reference ranges. The sample data shows all "None" values.

5. **The export does include some non-USCDI content** — spouse info, anticoagulant details, wound location data, blood sugar (fasting/random/HbA1c), past medical history, and patient relationships — indicating the vendor made some effort beyond just repackaging USCDI data.

### Summary Stats

    Coverage:        Partial
    Approach:        Purpose-built EHI export
    Export format:   PDF + proprietary JSON
    Entities:        34 sections
    Fields:          149
    Descriptions:    0%
    Sample data:     Yes (1 sample patient in both PDF and JSON)
    Bulk export:     Yes (multi-patient ZIP via UI)
    Domains covered: 9 of 17 applicable domains (5 partial, 4 not covered)

### Bottom Line

QSmartCare built a dedicated EHI export with a proprietary format that goes beyond standard C-CDA categories, but the export is shallow where it matters most. For a wound care EHR, the critical gap is the thin wound data section — the product almost certainly stores detailed wound assessments, measurements, photographs, and treatment protocols that don't appear in the export. The complete absence of documentation (no data dictionary, no field descriptions) makes the export difficult to use even for the data it does contain.
