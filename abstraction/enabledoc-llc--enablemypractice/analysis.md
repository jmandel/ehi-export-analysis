# EHI Export Analysis: EnableDoc LLC

**Product**: Enablemypractice  
**Analysis date**: 2026-02-16  
**CHPL IDs**: 15.02.05.1439.ENAD.01.01.1.220118 (CHPL ID 10795)

## 1. Product Context

Enablemypractice by EnableDoc LLC is a cloud-based, all-in-one EHR, practice management, and billing platform for ambulatory medical practices. It serves 20+ specialties (primary care, psychiatry, physical therapy, chiropractic, urology, pediatrics, ophthalmology, cardiology, radiology/breast imaging, and multispecialty groups). The company is small (11–50 employees, McLean, Virginia), targeting solo and small group practices.

The product stores data across these major functional areas relevant to EHI completeness:

- **Clinical**: Demographics, notes (AI-generated and manual), problem lists, medication lists, allergies, vital signs, immunizations, lab orders/results, procedures, clinical assessments, family history, care plans, observations
- **Medications/Prescribing**: E-prescribing (including EPCS), medication reconciliation, PDMP/NARX integration, drug interaction data, formulary/benefits
- **Billing/RCM**: Claims submission and tracking, superbills, ERA/remittance processing, payment reconciliation, patient statements, AR aging, EOB processing, CPT/ICD-10 coding
- **Radiology (RIS)**: Radiology orders, PACS integration, DICOM management, radiology reports, MQSA tracking
- **Patient engagement**: Patient portal, secure messaging, chat, telehealth sessions, intake forms, consent forms, surveys
- **Documents**: Scanned documents, uploaded files, insurance card images, encrypted PDF notes, faxes/Direct messages

This establishes a broad baseline: a complete (b)(10) export should cover clinical, billing, medication, radiology, and patient engagement data.

## 2. Artifacts Reviewed

| Artifact | Description | Size/Scope | Informativeness |
|---|---|---|---|
| `Enabledoc-Exporting-Data-Guide-2023-updated-11202023.pdf` | Primary EHI export documentation — 19-page PDF with export instructions, screenshots, data dictionary, and value sets | 476 KB, 19 pages, 15 entity definitions, 224 fields, 30 value sets | **Primary source** — most informative artifact |
| `enablemypractice-data-export-guide.html` | HTML landing page for the export documentation; contains download link to PDF | 78 KB | Low — just a download link and broken `[embeddoc]` shortcode |
| `enablemypractice-data-export-page-screenshot.png` | Screenshot of the landing page | 232 KB | Low — confirms broken shortcode on live page |
| `enrichment/data-dictionary.json` | Machine-readable extraction of the PDF data dictionary (15 entities, 224 fields, 30 value sets with 256 coded values) | 77 KB | **High** — structured version of the PDF data dictionary |
| `enrichment/excel-tabs.json` | List of 15 Excel tab names from the PDF | <1 KB | Reference |
| `enrichment/extract-data-dictionary.ts` | Parsing script (Bun TypeScript) | 12 KB | Reproducibility |
| `enrichment/README.md` | Enrichment documentation | 1.5 KB | Reference |

The entire EHI export documentation is a **single 19-page PDF**. There are no sample export files, no machine-readable schemas, no supplementary data dictionaries, and no additional documentation beyond what's in this PDF.

## 3. Export Mechanics

- **Format**: Four components — C-CDA files, Excel file (structured tabular data), Notes (PDF files in ZIP), Attachments (images/documents in ZIP)
- **Mechanism**: UI-based. Users navigate to Registration → Data Export → Custom Export. The interface includes patient selection (individual or all), date range filtering, and format selection checkboxes.
- **Bulk capability**: Yes — supports "select all" patients and "select all" dates for a full bulk export.
- **Scheduling**: Exports can be scheduled as one-time or recurring (daily, weekly, monthly, annually).
- **Access**: Requires administrator-granted access to the Data Export screen.
- **Fees**: Per the ONC disclosure page, (b)(10) export is included at no additional charge.

## 4. Export Content: What's In It

The export consists of four components:

### 4.1 C-CDA Files
Clinical summaries exported using USCDI v1 and HL7 CDA R2 C-CDA Templates R2.1 (October 2019). No field-level detail is provided for what C-CDA sections are included — the documentation only references the standard.

### 4.2 Excel File (Structured Data)
This is the core structured data export. The PDF documents 15 Excel tabs and provides field-level definitions for 15 entities with 224 total fields.

**Key finding**: The Excel tab listing and entity definitions don't perfectly align:
- **Tabs listed but lacking field definitions**: Condition (diagnoses/problems), Coverage (insurance)
- **Entities with field definitions but missing from the formal tab list**: AllergyIntolerance, Care Plan
- This suggests the actual export likely has **17 tabs** (15 listed + 2 implied), with 2 tabs (Condition, Coverage) undocumented at the field level.

**Data dictionary statistics** (from `analysis/full-entity-inventory.json`):
- Entities with field definitions: 15
- Total fields: 224
- Fields with descriptions: 224 (100%)
- Fields with explicit data types: 183 (81.7%)
- Fields with entity cross-references: 21
- Fields with value set references: 23
- Field requirement levels: 98 Required, 120 Preferred, 6 Optional
- Value sets: 30 (256 total coded values)

### 4.3 Notes
Patient clinical notes exported as PDF files, grouped in ZIP archives by patient name. No schema or field-level documentation.

### 4.4 Attachments
File attachments (images, Excel, Word, PDF) grouped in ZIP archives by patient name. No inventory or metadata schema.

### Vendor's own content organization

The entity naming follows FHIR R4 resource naming conventions closely. Entities are listed below by functional category (mine, based on content):

| Entity | Fields | Described | Types Specified | Category |
|---|---|---|---|---|
| Patient | 37 | 37 (100%) | 29 (78%) | Administrative |
| Organization | 16 | 16 (100%) | 13 (81%) | Administrative |
| Location | 15 | 15 (100%) | 15 (100%) | Administrative |
| Practitioner | 14 | 14 (100%) | 13 (93%) | Administrative |
| Encounter Data | 9 | 9 (100%) | 9 (100%) | Clinical |
| Observation | 24 | 24 (100%) | 23 (96%) | Clinical |
| Procedure | 10 | 10 (100%) | 7 (70%) | Clinical |
| Care Plan | 10 | 10 (100%) | 8 (80%) | Clinical |
| Family Member History | 17 | 17 (100%) | 15 (88%) | Clinical |
| AllergyIntolerance | 10 | 10 (100%) | 4 (40%) | Clinical |
| Immunization | 13 | 13 (100%) | 5 (38%) | Clinical |
| Service Request | 10 | 10 (100%) | 9 (90%) | Orders |
| Medication Administration | 17 | 17 (100%) | 15 (88%) | Medications |
| MedicationRequest | 11 | 11 (100%) | 8 (73%) | Medications |
| Medication Statement | 11 | 11 (100%) | 10 (91%) | Medications |
| *Condition* (tab listed) | *N/A* | *N/A* | *N/A* | *Clinical — no field defs* |
| *Coverage* (tab listed) | *N/A* | *N/A* | *N/A* | *Insurance — no field defs* |
| **TOTAL (defined)** | **224** | **224 (100%)** | **183 (82%)** | |

The entity/field model is a **FHIR-influenced projection** — names like "MedicationRequest," "AllergyIntolerance," "ServiceRequest," and field names like "subject," "encounter," "status" directly mirror FHIR R4 resource definitions. The data types (code, string, dateTime, reference) and value sets (HL7 administrative gender, SNOMED CT, V3 ActEncounterCode) are standard FHIR value sets. However, the export format is Excel, not FHIR JSON/XML.

**Entity cross-references**: 21 fields reference other entities (e.g., Encounter → Patient via "subject", Observation → Encounter via "encounter"). These references use "See section: [Entity]" notation in the documentation but the actual key format in the Excel output is not specified.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The export covers clinical and administrative data modeled after FHIR R4 resources:

**Richest areas** (most fields):
- Patient demographics (37 fields) — extensive, including race, ethnicity, language proficiency, gender identity, religious affiliation, birth sex, primary caregiver
- Observation (24 fields) — covers vitals, lab results, and clinical observations with interpretation, reference ranges, and category codes
- Medication Administration (17 fields) — detailed medication delivery records
- Family Member History (17 fields) — family health records with conditions and outcomes

**Thinnest areas**:
- Encounter Data (9 fields) — basic encounter status, dates, class, and participant only
- Condition and Coverage — tabs exist but have **zero** field-level documentation

**Absent from the export entirely**:
- All billing/financial data (claims, superbills, payments, ERA, AR aging, statements)
- Radiology-specific data (RIS, PACS references, MQSA, DICOM, radiology reports)
- Patient portal messages and secure communications
- Custom intake forms and clinical assessments
- Telehealth session records
- Documents/attachments metadata (attachments are exported as raw files with no schema)

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | Patient (37 fields), Organization (16), Location (15), Practitioner (14) | Thorough — includes race, ethnicity, language, gender identity, religious affiliation |
| Encounters / visits | ⚠️ Partial | Encounter Data (9 fields — status, dates, class, participant) | Minimal encounter record; no visit-level details, chief complaint, or disposition |
| Problems / conditions / diagnoses | ⚠️ Partial | Condition tab listed but **no field definitions**; conditions referenced in Family Member History | Tab exists but is undocumented — unclear what fields are exported |
| Medications / prescriptions | ✅ Covered | MedicationRequest (11), MedicationAdministration (17), Medication Statement (11) — 39 fields across 3 entities | Solid coverage of medication orders, administration, and statements |
| Allergies | ✅ Covered | AllergyIntolerance (10 fields — type, category, criticality, severity, clinical status) | Adequate |
| Immunizations | ✅ Covered | Immunization (13 fields) + Vaccine Administered Value Set (29 codes) | Adequate |
| Vitals | ✅ Covered | Observation entity (24 fields) handles vitals, labs, and clinical observations | Combined with labs in one entity — adequate for vitals |
| Lab results | ✅ Covered | Observation entity with interpretation, reference ranges, category codes | Covered within Observation entity |
| Imaging / diagnostic reports | ❌ Not covered | No radiology-specific entities in export | Product has full RIS module with PACS/DICOM; **significant gap** for radiology-using practices |
| Procedures | ✅ Covered | Procedure (10 fields — status, code, performed date, body site, outcome) | Adequate |
| Clinical notes / documents | ✅ Covered | Notes exported as PDF files in ZIP archives by patient | Covered via Notes export component (but no structured metadata) |
| Care plans / goals | ✅ Covered | Care Plan (10 fields — status, intent, dates, category, description) | Adequate |
| Orders / referrals | ✅ Covered | ServiceRequest (10 fields — status, intent, category, code, dates) | Adequate |
| Insurance / coverage | ⚠️ Partial | Coverage tab listed but **no field definitions** | Tab exists but is undocumented — unclear what fields are exported |
| Claims / billing | ❌ Not covered | No billing entities in export | Product has full billing/RCM module (claims, superbills, ERA, payments, AR); **major gap** |
| Payments | ❌ Not covered | No payment entities in export | Product handles payments, patient statements, credit card processing; **gap** |
| Consents / directives | ❌ Not covered | No consent entities in export | Product collects consent forms via intake; may be in Attachments but unstructured |
| Patient communications / portal messages | ❌ Not covered | No messaging or communication entities | Product has secure messaging, chat, portal; **gap for clinical communications** |
| Specialty-specific (Radiology/RIS) | ❌ Not covered | No RIS, PACS, DICOM, or MQSA entities | Product has dedicated RIS module; **significant gap** for imaging practices |

**Summary**: 9 of 17 applicable domains are covered, 3 are partially covered (2 with undocumented tabs), and 5 are not covered at all. The most significant gaps are billing/claims data and radiology-specific data, both of which are core product capabilities.

## 6. Documentation Quality

**Strengths:**
- Every defined field (224/224) has a description — 100% description coverage
- Data types specified for 82% of fields
- Requirement levels (Required/Preferred/Optional) specified for all fields
- 30 value sets with 256 coded values provide explicit allowed values for coded fields
- Clear export instructions with a UI screenshot
- Multiple export formats offer different views of the data

**Weaknesses:**
- **No sample export files.** A developer cannot verify the actual output format without running an export.
- **No machine-readable schema.** The only documentation is a PDF — no JSON Schema, XSD, or CSV header definitions.
- **Relationship/key format undocumented.** 21 fields cross-reference other entities ("See section: Patient") but the actual key format in the Excel file is not described. How does one join Encounter to Patient?
- **Two tabs completely undocumented.** Condition and Coverage tabs are listed but have zero field-level definitions — these are important clinical/insurance data categories.
- **FHIR-standard naming without FHIR specification.** The entities mirror FHIR R4 but the export is Excel, not FHIR. A developer must guess whether the Excel columns exactly match FHIR field paths or diverge.
- **Document is dated November 2023.** No version history, no changelog, no indication of updates in 2+ years.
- **Landing page has a broken WordPress shortcode** (`[embeddoc]`) visible to end users.

**Could a developer build an import from this documentation alone?** Partially. The field names and descriptions are clear enough for basic understanding, but without sample data, explicit key formats, or documentation for 2 tabs, a developer would need trial-and-error with actual export files.

## 7. Overall Assessment

### Classification

**Partial native export** — The export uses a FHIR-influenced data model exported as Excel, supplemented by C-CDA and raw notes/attachments. It covers clinical data reasonably but has significant coverage gaps in billing, radiology, and patient communications.

### Key Findings

1. **Billing data is entirely absent.** The product is marketed as an all-in-one EHR/PMS/billing platform with claims, superbills, ERA, payments, and AR management. None of this billing/financial data appears in the export — a major gap for the designated record set. (Source: product-research.md vs. data dictionary in PDF)

2. **224 fields across 15 entities, all with descriptions.** The documented portion of the export has decent field-level detail: 100% of fields have descriptions, 82% have explicit data types, and 30 value sets provide coded value definitions. (Source: `analysis/full-entity-inventory.json`)

3. **Two documented tabs (Condition, Coverage) lack any field definitions.** These are listed as Excel tabs but the PDF provides no field-level documentation for either. These represent diagnoses/problem lists and insurance — both important EHI categories. (Source: PDF pp. 1–2 vs. entity definitions pp. 2–12)

4. **The data model mirrors FHIR R4 but isn't FHIR.** Entity names, field names, data types, and value sets all follow FHIR R4 conventions, but the export format is Excel spreadsheet. This is a FHIR-influenced projection, not a native database export. It captures the clinical data FHIR covers but inherits FHIR's blind spots (billing, specialty data). (Source: entity names and value sets in `data-dictionary.json`)

5. **Radiology-specific data is completely absent.** The product includes a dedicated RIS module with PACS integration, DICOM management, and MQSA tracking. None of this appears in the export, leaving a significant gap for radiology/imaging practices. (Source: product-research.md vs. export entities)

### Summary Stats

```
Classification:  Partial native export
Export format:   Excel (FHIR-modeled tabs) + C-CDA + PDF notes + ZIP attachments
Model type:      Standard projection (FHIR-influenced flat file, not native database)
Entities:        15 documented (+ 2 tabs without field definitions = 17 total tabs)
Fields:          224 (across 15 documented entities)
Descriptions:    100% of defined fields
Sample data:     No
Bulk export:     Yes (select all patients, all dates)
Domains covered: 9 of 17 applicable domains (3 partial, 5 not covered)
```

### Bottom Line

Enablemypractice's EHI export goes beyond a simple C-CDA dump by providing structured Excel data with 224 documented fields, supplemented by clinical notes and file attachments. However, the export is modeled on FHIR R4 resources rather than the vendor's native database, which means it inherits FHIR's clinical focus while omitting the product's substantial billing/RCM, radiology (RIS), and patient engagement data. A patient or provider would get a reasonable clinical picture but would be missing all financial records, radiology-specific data, and communications — a significant gap for a product that bills itself as an all-in-one platform.
