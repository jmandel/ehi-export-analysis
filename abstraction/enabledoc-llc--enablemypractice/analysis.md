# EHI Export Analysis: EnableDoc LLC

**Product**: Enablemypractice  
**Analysis date**: 2026-02-16  
**CHPL IDs**: 15.02.05.1439.ENAD.01.01.1.220118 (CHPL ID 10795)

## 1. Product Context

Enablemypractice is a cloud-based, all-in-one EHR, practice management, and billing platform developed by EnableDoc LLC, a small vendor (~11–50 employees) based in McLean, Virginia. It targets ambulatory medical practices across 20+ specialties including primary care, psychiatry/mental health, physical therapy, chiropractic, urology, pediatrics, ophthalmology, cardiology, and radiology/breast imaging.

The product integrates:
- **EHR**: AI-powered clinical documentation with customizable specialty templates, problem lists, vitals, allergies, immunizations, family history, care plans
- **E-prescribing**: EPCS-capable prescribing with PDMP/NARX integration, drug interaction checking, medication reconciliation
- **Lab orders/results**: Electronic ordering with LabCorp, Quest, and in-house lab management
- **Billing/RCM**: AI-powered coding (CPT, ICD-10), claims submission and tracking, ERA processing, payment reconciliation, superbill management, AR aging, electronic patient statements, EOB processing
- **Patient engagement**: Patient portal, secure messaging, telehealth, intake forms, surveys
- **Scheduling**: Drag-and-drop scheduling, online booking, telehealth appointment links
- **Radiology (RIS)**: PACS integration, DICOM management, MQSA tracking, radiology reporting
- **Population health**: Chronic care management, patient list generation, care coordination

This is relevant because a genuine (b)(10) export should cover not just clinical data but also billing/financial records, specialty data (radiology), patient communications, custom forms, and other designated-record-set content.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/Enabledoc-Exporting-Data-Guide-2023-updated-11202023.pdf` (476 KB, 19 pages) | The sole export documentation artifact. Contains export instructions with a UI screenshot, export format descriptions (C-CDA, Excel, Notes, Attachments), and a data dictionary covering 15 entities with 224 field definitions and 30 value sets. | **Primary artifact** — the only substantive documentation |
| `downloads/enablemypractice-data-export-guide.html` (78 KB) | HTML landing page at the registered EHI documentation URL. Contains a download link to the PDF and a broken WordPress `[embeddoc]` shortcode. | Low — confirms PDF link exists, broken shortcode visible |
| `downloads/enablemypractice-data-export-page-screenshot.png` (232 KB) | Screenshot of the landing page confirming broken embeddoc shortcode is visible to end users. | Low — confirms broken state |
| `downloads/enrichment/data-dictionary.json` (77 KB) | Structured JSON extraction of the PDF data dictionary: 15 entities, 224 fields, 30 value sets with 256 entries. | **High** — machine-readable parse of the PDF, verified against `pdftotext` output |
| `downloads/enrichment/excel-tabs.json` (337 bytes) | List of 15 Excel tab names documented in the export guide. | Low — supplementary |

## 3. Export Mechanics

- **Format**: Multi-format export consisting of four components:
  1. **C-CDA files** — clinical summaries per USCDI v1 / HL7 CDA R2 standard
  2. **Excel file** — structured tabular data organized by tabs (15 entities with FHIR-influenced schema)
  3. **Notes** — patient clinical notes exported as PDF files, grouped in ZIP archives by patient
  4. **Attachments** — attached files (images, Excel, Word, PDF) grouped in ZIP archives by patient
- **Mechanism**: UI-based. Users navigate to Registration → Data Export → Custom Export. The interface allows selecting specific patients or all patients, setting date ranges, and scheduling exports (one-time or recurring: daily, weekly, monthly, annually).
- **Single-patient vs bulk**: Supports both — users can select individual patients or check "all."
- **Access constraints**: Requires administrator-granted access to the Data Export screen. No fees mentioned (the ONC disclosure page confirms (b)(10) export is included at no additional charge).

## 4. Export Content: What's In It

The export documentation describes 15 Excel tabs with field-level definitions for 13 of them. Two tabs — **Condition** and **Coverage** — are listed but have no field-level definitions in the data dictionary.

**Data dictionary scope**: 15 entities, 224 total fields. Every field has a description (100% description coverage). 183 of 224 fields (81.7%) have explicit data types. All 224 fields have requirement levels (Required/Preferred/Optional). 30 value sets are defined with 256 coded values covering standard terminologies (HL7 administrative gender, OMB race/ethnicity, SNOMED CT findings, vaccine codes, encounter status, etc.).

The field naming and entity structure closely mirror FHIR R4 resource definitions — entities are named after FHIR resources (Patient, Encounter, Observation, MedicationRequest, etc.) and use FHIR-style field names and value sets. However, the export format is Excel, not FHIR NDJSON or Bundle.

### Vendor's own content organization

| Entity | Fields | Described | Types | Category |
|---|---|---|---|---|
| Organization | 16 | 16 | 13 | Administrative |
| Patient | 37 | 37 | 29 | Administrative |
| Location | 15 | 15 | 15 | Administrative |
| Practitioner | 14 | 14 | 13 | Administrative |
| Encounter Data | 9 | 9 | 9 | Clinical |
| Condition | (listed, no field definitions) | — | — | Clinical |
| Coverage | (listed, no field definitions) | — | — | Clinical |
| Procedure | 10 | 10 | 7 | Clinical |
| Service Request | 10 | 10 | 9 | Clinical |
| Family Member History | 17 | 17 | 15 | Clinical |
| Immunization | 13 | 13 | 5 | Clinical |
| AllergyIntolerance | 10 | 10 | 4 | Clinical |
| Care Plan | 10 | 10 | 8 | Clinical |
| Observation | 24 | 24 | 23 | Clinical |
| Medication Administration | 17 | 17 | 15 | Medication |
| MedicationRequest | 11 | 11 | 8 | Medication |
| Medication Statement | 11 | 11 | 10 | Medication |
| **TOTAL** | **224** | **224** | **183** | |

The complete entity and field inventory is available in `analysis/entity-inventory-full.json`.

**Notable observations**:
- **Patient** is the largest entity with 37 fields covering demographics, contact info, race/ethnicity, language, birth sex, gender identity, religious affiliation, marital status, and caregiver relationships — genuinely detailed.
- **Observation** (24 fields) is well-structured with support for coded values, quantities, date ranges, devices, and free-text — it handles vitals, labs, and clinical observations.
- **Medication Administration** (17 fields) includes dosage, route, timing, category, and links to the originating MedicationRequest — more detail than many vendors provide.
- **Condition** and **Coverage** are listed as Excel tabs but have zero field definitions. Condition (problems/diagnoses) and Coverage (insurance) are clinically important. Their absence from the data dictionary is a documentation gap — the tabs presumably exist in the export, but there's no way to know what fields they contain.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor organizes their export into four components:

1. **C-CDA files**: Standard USCDI v1 clinical summaries. These cover the usual C-CDA sections (problems, meds, allergies, vitals, procedures, etc.) but add nothing beyond the standard template.

2. **Excel file (15 tabs)**: This is where the vendor goes beyond C-CDA. The FHIR-influenced tabular export includes:
   - **Administrative context** (4 entities, 82 fields): Organization, Patient, Location, Practitioner — rich demographic and organizational data
   - **Clinical data** (8 entities, 103 fields): Encounters, procedures, service requests, family history, immunizations, allergies, care plans, observations (plus Condition and Coverage tabs without field definitions)
   - **Medication data** (3 entities, 39 fields): Administration, requests, and statements — covering prescriptions, MAR, and medication history

3. **Notes**: Clinical notes exported as PDFs — captures the narrative clinical record.

4. **Attachments**: All attached files — captures scanned documents, images, and other media.

The export's Excel component is the most substantive. It covers core clinical domains with reasonable depth. The FHIR-influenced structure means fields roughly align with FHIR R4 resource definitions — this is more than a raw database dump but also not a fully customized EHR-specific export. The entity and field selection closely mirrors what would be needed for USCDI compliance, with minor extensions.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | `Patient` (37 fields): name, DOB, gender, race, ethnicity, language, birth sex, gender identity, address, contact, marital status, religious affiliation, MRN | Thorough — one of the most detailed Patient entities seen |
| Encounters / visits | ✅ Covered | `Encounter Data` (9 fields): identifier, status, class, dates, participant, type | Adequate but thin — only 9 fields for what is typically a richer domain |
| Problems / conditions | ⚠️ Partial | `Condition` tab listed but has **zero field definitions** in the data dictionary | Tab presumably exists in export but content is undocumented |
| Medications / prescriptions | ✅ Covered | `MedicationRequest` (11 fields), `MedicationStatement` (11 fields), `Medication Administration` (17 fields) — three separate entities | Good depth across prescribing, administration, and patient-reported use |
| Allergies | ✅ Covered | `AllergyIntolerance` (10 fields): category, code, reaction, clinical status, criticality | Adequate |
| Immunizations | ✅ Covered | `Immunization` (13 fields): vaccine code, date, status, location, performer, reaction | Good |
| Vitals | ✅ Covered | Via `Observation` (24 fields) — handles all observation types including vitals | Good — rich Observation entity with coded values, quantities, date ranges |
| Lab results | ✅ Covered | Via `Observation` (24 fields) — lab results use the same Observation structure | Good — unified observation model handles labs |
| Imaging / diagnostic reports | ❌ Not covered | No DiagnosticReport or imaging-specific entity in the export | **Significant gap**: product has a full RIS module with PACS/DICOM/MQSA. No radiology-specific data appears in the export |
| Procedures | ✅ Covered | `Procedure` (10 fields): code, date, status, encounter, code system | Adequate |
| Clinical notes / documents | ✅ Covered | Notes exported as PDFs in ZIP archives by patient; also `Attachments` export for other document types | Good — captures narrative record and uploaded documents |
| Care plans / goals | ✅ Covered | `Care Plan` (10 fields): status, intent, dates, encounter link | Basic but present |
| Orders / referrals | ✅ Covered | `Service Request` (10 fields): code, intent, status, requester, patient | Adequate |
| Insurance / coverage | ⚠️ Partial | `Coverage` tab listed but has **zero field definitions** in the data dictionary | Tab presumably exists but content is undocumented |
| Claims / billing | ❌ Not covered | No claims, superbills, charge, payment, or ERA entities in the export | **Major gap**: product has full billing/RCM with claims, ERA, superbills, AR aging, patient statements, EOBs — none exported |
| Payments | ❌ Not covered | No payment or financial transaction entities | Part of the billing gap |
| Consents / directives | ❌ Not covered | No consent entity; may be captured as Attachments but not structured | Product collects consent forms via intake — not specifically exported |
| Patient communications | ❌ Not covered | No secure messaging, portal message, or communication entity | Product has portal messaging, secure chat, SMS — none in export |
| Specialty-specific (Radiology) | ❌ Not covered | No RIS, PACS, DICOM, MQSA, or radiology report entities | Product has a full RIS module — significant gap |
| Family history | ✅ Covered | `Family Member History` (17 fields): relationship, conditions, onset, outcome, birth sex, age | Good depth |

**Summary**: 11 of 19 applicable domains are covered, 2 are partial (documented as tabs but no field definitions), and 6 are not covered. The most significant gaps are billing/financial data (the product's billing module is a core feature) and radiology-specific data (the product has an integrated RIS).

## 6. Documentation Quality

**Strengths**:
- Every documented field (224/224) has a description — 100% description coverage
- Data types specified for 81.7% of fields
- Requirement levels (Required/Preferred/Optional) specified for all fields
- 30 value sets with 256 coded values referencing standard terminologies
- Clear export instructions with a UI screenshot
- Multiple export format options giving flexibility

**Weaknesses**:
- **Single 19-page PDF** is the entire documentation. No machine-readable schema, no sample data files, no API documentation.
- **Two entities (Condition, Coverage) lack field definitions** despite being listed as Excel tabs — these are clinically important domains
- **No relationship documentation**: entities reference each other (e.g., Observation → Encounter, Procedure → Patient) but the documentation doesn't explain how cross-tab references work in the Excel format (foreign key columns? identifier matching?)
- **No sample export files**: a developer would have to request an actual export to understand the output format
- **Stale documentation**: the PDF is dated November 2023 (over 2 years old) and the landing page has a broken WordPress `[embeddoc]` shortcode visible to end users — suggests limited maintenance
- **No versioning or change history** in the document

A developer could build a partial import from this documentation but would face challenges with: (1) understanding cross-entity relationships in the Excel format, (2) handling the two undocumented tabs, and (3) any billing or specialty data not covered.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Partial**

The export covers core clinical domains reasonably well through a combination of C-CDA files, a 15-entity Excel data dictionary, clinical notes as PDFs, and file attachments. This goes beyond a bare-minimum USCDI clinical summary. However, the product is marketed as an all-in-one EHR/PMS/billing platform with a full RCM module (claims, ERA, superbills, AR aging, patient statements, EOBs) and an integrated Radiology Information System (PACS, DICOM, MQSA) — neither billing data nor radiology-specific data appears in the export. Patient communications (portal messages, secure chat) are also absent. For a product where billing and radiology are core differentiators, these are significant omissions from the designated record set. Two documented tabs (Condition, Coverage) lack field definitions, further weakening coverage evidence.

**Axis 2 — Export approach: Purpose-built EHI export**

Despite coverage gaps, this is clearly a purpose-built export rather than a repackaged existing standard. The vendor created a multi-format export (C-CDA + Excel + Notes + Attachments) with a FHIR-influenced but product-specific Excel schema. The Excel component uses FHIR resource names and field conventions but is delivered as tabular data, not a FHIR API response. The UI provides scheduling (recurring exports), patient selection, and date range filtering — these are purpose-built export features. The vendor documented 15 entities with 224 fields and 30 value sets specific to their product. This is not simply pointing at an existing (g)(10) FHIR API or C-CDA transition-of-care document.

However, the entities and fields closely mirror FHIR R4/USCDI resource definitions rather than the product's native data model. The export appears to be a FHIR-to-Excel projection of standard clinical data rather than a dump of the product's internal tables. This means it inherits USCDI's scope limitations — it covers what FHIR R4 resources cover and little beyond that.

### Key Findings

1. **Multi-format purpose-built export with genuine effort**: The four-component export (C-CDA + Excel + Notes + Attachments) with a 224-field data dictionary across 15 entities demonstrates real engagement with (b)(10). This is meaningfully more than vendors who simply point to their FHIR API.

2. **Major billing data gap**: The product has a full billing/RCM module (claims, ERA, superbills, AR aging, patient statements, EOBs) that is a core selling point. Zero billing entities appear in the export. For a product where billing is a primary function, this is the single most significant gap.

3. **Radiology-specific data absent**: The product includes a dedicated RIS module (PACS integration, DICOM management, MQSA tracking, radiology reporting). No radiology-specific data appears in the export — only generic Observation and Procedure entities that don't capture imaging-specific detail.

4. **Two entities documented without field definitions**: Condition (problems/diagnoses) and Coverage (insurance) are listed as Excel tabs but have zero field-level documentation — a notable documentation gap for clinically important domains.

5. **Stale single-document approach**: The entire documentation is a single 19-page PDF from November 2023, hosted behind a broken WordPress page with a non-rendering `[embeddoc]` shortcode. No sample data, no machine-readable schema, no update since initial creation.

### Summary Stats

```
Coverage:        Partial
Approach:        Purpose-built EHI export
Export format:   Mixed (C-CDA + Excel + PDF notes + ZIP attachments)
Entities:        15 (13 with field definitions, 2 tabs without)
Fields:          224
Descriptions:    100%
Sample data:     No
Bulk export:     Yes (all patients + scheduling)
Domains covered: 11 of 19 applicable (+ 2 partial)
```

### Bottom Line

EnableDoc made a genuine effort to build a purpose-specific (b)(10) export with a multi-format approach and a 224-field data dictionary — this is more than many small vendors provide. However, the export is essentially a FHIR-influenced clinical data projection that covers USCDI-scope data well but omits entire product capabilities: billing/financial records, radiology-specific data, and patient communications are all absent despite being core features of the platform. A patient would get a solid clinical picture but would be missing their billing history and any specialty imaging data.
