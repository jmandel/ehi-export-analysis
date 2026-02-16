# EHI Export Analysis: DigiDMS, Inc.

**Product**: DigiDMS v25.0
**Analysis date**: 2026-02-16
**CHPL IDs**: 15.04.04.2709.Digi.25.05.1.241212

## 1. Product Context

DigiDMS is an integrated EHR + Practice Management + Billing system for ambulatory/outpatient settings, targeting small to medium physician practices, dental offices, and physical therapy clinics. The company claims 300+ medical offices as customers. The product is ONC-certified as a Complete EHR (certified 2024-12-12 by Drummond).

Key data domains the product stores, relevant to export completeness:

- **Clinical data**: Demographics, problem lists, medications, allergies, vitals, immunizations, lab results, diagnostic tests, procedures, clinical notes/encounter documentation, orders, implantable device tracking, social/psychological/behavioral data, clinical decision support
- **Billing/PM data**: Insurance information, claims, CMS-1500/HCFA forms, ICD-10 coding, batch eligibility checks, invoices, payment records, revenue cycle management
- **Patient portal (myPersonalChart)**: Secure messaging, appointment scheduling, medication refill requests, referral requests, CCD export/import
- **Document management**: Scanned documents, OCR, digital signatures, uploaded files, metadata/annotations
- **Transitions of care**: CCD/CCDA generation, Direct messaging
- **Public health reporting**: Immunization registry, syndromic surveillance, cancer case reporting, electronic case reporting

The product's EHR UI (visible in PDF screenshots) includes menu tabs for Session, Masters, Patient, Appointment, Billing, Script, Clearing House, Tools, and Help — confirming robust billing and practice management capabilities. The patient chart sidebar includes Demographics, History, Active Problems, Allergies, Medications, Alerts, Vitals, Immunizations, Orders, Results, Documents, Notes, Messages, Encounters, and Appointments.

## 2. Artifacts Reviewed

| Artifact | Description | Informational Value |
|---|---|---|
| `B10_EHI_Export.pdf` (1.28 MB, 7 pages) | Primary EHI export documentation. Title page, overview, two pages of UI screenshots showing export workflow, and a 3-page section/element table listing C-CDA sections and their fields. Authored by Hemant J. Patel, dated 2025-11-18. References product version 22.0. | **Primary source** — contains the only export specification |
| `EHIexport-template.html` (1,977 bytes) | HTML fragment from the vendor's EHI export web page. Contains a brief overview paragraph and a link to the PDF. References product version 25.0. | **Low value** — just a landing page linking to the PDF |
| `ehi-export-page-screenshot.png` | Screenshot of the vendor's EHI export web page at `digidms.com/ehr/ehi-export`. Shows only a "Scroll" link on a blank white page — the JavaScript-rendered site failed to load. | **No value** — blank page |

The PDF is the only substantive artifact. The vendor's EHI export documentation consists of a single 7-page PDF document. There is no data dictionary, no JSON/XML schema, no sample data files, and no machine-readable specification.

**Verification**: The PDF remains accessible at `https://digidms.com/documents/B10_EHI_Export.pdf` (HTTP 200, content-length 1,283,932 bytes, last-modified 2025-11-18). The vendor's EHI export web page at `https://digidms.com/ehr/ehi-export` still renders blank (JavaScript-dependent SPA that returns only a "Scroll" link when fetched).

## 3. Export Mechanics

- **Format**: C-CDA (HL7 CDA® R2, Consolidated CDA Templates for Clinical Notes R2.1 Companion Guide), per § 170.205(a)(4)
- **Mechanism**: EHR UI — two modes:
  1. **Single patient**: Select patient → open "Clinical Document Section" dialog → check desired C-CDA sections → export. The dialog (visible in PDF page 3 screenshot) shows checkboxes for each C-CDA section with a date range filter.
  2. **Patient population (bulk)**: Access the "Patient Screening" module → run a query (e.g., "Diabetic patients") → use the "Export" dropdown → select "CCDA". The bulk export UI (visible in PDF page 4 screenshot) also offers Excel as an export format, but the documentation only describes CCDA as the (b)(10) export.
- **Access constraints**: Users must have appropriate access rights. The documentation states: "For rights to export specific feature DigiDMS user can raise request for grants to specific export functionality and given the access user can perform the operation."
- **Single-patient vs bulk**: Both supported
- **Fees**: Not mentioned in documentation
- **No developer/technical assistance required**: Stated explicitly in the overview

## 4. Export Content: What's In It

The export is a standard C-CDA clinical document. The PDF (pages 5–7) provides a simple two-column table listing "Section" and "Elements" — section names map to C-CDA sections, and elements are the data fields within each section.

### Key statistics (from parsed `full-entity-inventory.json`)

- **Total C-CDA sections**: 21 (including 4 header sections: Patient, Provider, Author, Practice)
- **Total fields/elements**: 61
- **Fields with data types documented**: 0 (0%)
- **Fields with descriptions**: 0 (0%)
- **Fields with value sets/code systems**: 0 (0%)
- **Fields with foreign keys/relationships**: 0 (0%)
- **Sample data provided**: No (screenshots show demo data but no export sample files)
- **Machine-readable schema**: No

### Vendor's own content organization

The vendor organizes content as C-CDA sections. The table below reproduces exactly what the PDF documents (parsed via `analysis/parse_pdf_sections.py`):

| Section (Vendor's) | Fields | Field Names |
|---|---|---|
| Patient | 8 | Name, Date Of Birth, Sex, Race, Ethnicity, Language, Contact Information, Patient Id |
| Provider | 1 | Contact Information |
| Author | 1 | Contact Information |
| Practice | 1 | Contact Information |
| Reason for Referral | 0 | *(section listed but no elements)* |
| Allergies | 4 | Substance, Reaction, Severity, Status |
| Encounters | 4 | Encounter, Location, Date, Diagnosis |
| Immunization | 3 | Vaccine, Date, Status |
| Medication | 4 | Medication, Direction, Quantity, Date |
| Health Concern | 3 | Concern, Status, Date |
| Interventions | 3 | Planned Intervention, Status, Date |
| Goals | 3 | Goal, Value, Date |
| Medical Equipments | 3 | Implant, Area, UDI |
| Problems | 3 | Condition, Effective Date, Status |
| Procedures | 2 | Procedure, Date |
| Care Plan | 2 | Observation, Date |
| Assessment | 3 | Problem, Date, Comments |
| Results | 5 | Result, Date, Interpretation, Reference Range, Remarks |
| Social History | 3 | Social History Element, Description, Effective Date |
| Vital Signs | 3 | Vital Sign, Date, Value |
| Functional Status | 2 | Criteria, Status |

No field has any type, description, value set, or relationship documentation. The table is purely a list of element names grouped by C-CDA section — it provides no information beyond what the C-CDA standard itself defines.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The export covers exactly the standard C-CDA clinical summary sections — and nothing more. There are 17 clinical sections plus 4 header/context sections (Patient, Provider, Author, Practice). This maps one-to-one to the C-CDA R2.1 template sections. There are no vendor extensions, no custom sections, and no data beyond what the C-CDA standard specifies.

The export is notably thin even within C-CDA's scope:
- Only 61 total elements across all sections — most sections have just 2–4 fields
- No section has more than 8 fields
- The Results section (lab results) has only 5 fields: Result, Date, Interpretation, Reference Range, Remarks
- There are no identifiers, codes, or structured references documented for any section

The single-patient export UI screenshot (PDF page 3) shows checkboxes matching these sections: Encounters, Problems, Allergies, Medications, Social History, Vital Signs, Results, Assessment and Plan, Immunizations, Procedures, Goals, Implanted Devices, Health Concerns, Functional Status, Reason for referral. This matches the table exactly.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | Patient section (8 fields: Name, DOB, Sex, Race, Ethnicity, Language, Contact Information, Patient Id) | Basic demographics only; missing address details, emergency contacts, preferred pharmacy, employer. The product stores richer demographics (visible in UI sidebar). |
| Encounters / visits | ⚠️ Partial | Encounters section (4 fields: Encounter, Location, Date, Diagnosis) | Minimal — no encounter type, duration, provider, status, or detailed visit documentation. Product's UI shows encounter history with more detail. |
| Problems / conditions / diagnoses | ⚠️ Partial | Problems section (3 fields: Condition, Effective Date, Status) | Basic problem list only. No ICD-10 codes explicitly documented, no onset/resolution dates, no severity. |
| Medications / prescriptions | ⚠️ Partial | Medication section (4 fields: Medication, Direction, Quantity, Date) | No dosage, no route, no frequency, no prescriber, no refill info. Product has e-prescribing (Script tab visible in UI) — prescription details absent. |
| Allergies | ✅ Covered | Allergies section (4 fields: Substance, Reaction, Severity, Status) | Reasonable for C-CDA scope. |
| Immunizations | ⚠️ Partial | Immunization section (3 fields: Vaccine, Date, Status) | Basic; missing lot number, manufacturer, administration site. |
| Vitals | ⚠️ Partial | Vital Signs section (3 fields: Vital Sign, Date, Value) | Minimal; the UI (PDF page 3) shows 13+ vital types (Height, Weight, BMI, Temperature, BP, Pulse, etc.) but the export only documents 3 generic fields. |
| Lab results | ⚠️ Partial | Results section (5 fields: Result, Date, Interpretation, Reference Range, Remarks) | Basic results only. No LOINC codes, units, specimen info, performing lab, or panel structure documented. |
| Imaging / diagnostic reports | ❌ Not covered | No imaging or radiology section in the export | Product stores diagnostic test results (per research); no dedicated imaging export section. |
| Procedures | ⚠️ Partial | Procedures section (2 fields: Procedure, Date) | Minimal — no CPT/procedure codes, no performer, no laterality, no outcome. |
| Clinical notes / documents | ❌ Not covered | No notes or documents section in the export | Product has "Notes" and "Documents" in the patient chart sidebar (visible in PDF page 3 screenshot). These are not in the export. Significant gap. |
| Care plans / goals | ⚠️ Partial | Care Plan (2 fields), Goals (3 fields), Health Concern (3 fields), Interventions (3 fields), Assessment (3 fields) | Skeleton fields with no structured detail. |
| Orders / referrals | ❌ Not covered | "Reason for Referral" section listed but has 0 fields. No orders section. | Product has "Orders" in the patient chart sidebar (visible in PDF page 3 screenshot showing orders with dates and ordering physicians). These are not in the export. |
| Insurance / coverage | ❌ Not covered | No insurance or coverage section in the export | Product stores insurance information (confirmed via patient portal help and billing features). Significant gap. |
| Claims / billing | ❌ Not covered | No billing, claims, or charge section in the export | Product has dedicated Billing tab, Clearing House tab, claim scrubbing, CMS-1500 generation, revenue cycle management. Major gap. |
| Payments | ❌ Not covered | No payment data in the export | Product tracks invoices and payment records. Significant gap. |
| Consents / directives | ❌ Not covered | No consent or advance directive section in the export | Unclear if product stores these, but C-CDA supports this section and it's absent. |
| Patient communications / portal messages | ❌ Not covered | No messaging or communication section in the export | Product has "Messages" in the patient chart sidebar and myPersonalChart portal supports secure messaging. Significant gap. |
| Specialty-specific data | N/A | No specialty-specific data sections | Product is general ambulatory, not specialty-specific. N/A. |

**Summary**: Of the 17 applicable EHI domains, 1 is adequately covered (Allergies), 8 are partially covered (with minimal fields), and 8 are completely absent. The most significant gaps are billing/claims/payments (the product has robust billing/PM capabilities), clinical notes/documents, orders, insurance, and patient communications — all confirmed as core data the product stores.

## 6. Documentation Quality

The documentation quality is very poor:

- **No data dictionary**: The only specification is a two-column table listing C-CDA section names and element names. There are no data types, no descriptions, no value sets, no code systems, no relationships.
- **No machine-readable artifacts**: No JSON schema, no XML schema, no sample C-CDA files, no WSDL, no API specification.
- **No sample data**: Screenshots in the PDF show demo patient data in the UI, but no actual C-CDA export sample is provided.
- **Minimal prose**: The overview is two short paragraphs. The export options description is approximately three sentences plus screenshots.
- **Version mismatch**: The PDF title page references "DigiDMS and 22.0" while the HTML template and CHPL certification reference version 25.0. The PDF was created 2025-11-18, after the certification date of 2024-12-12, but the version discrepancy is unexplained.
- **No import guidance**: A developer receiving this export would need to rely entirely on C-CDA standard documentation to parse the output. The vendor's documentation adds zero information beyond "it's C-CDA."

**Could a developer build an import from this documentation alone?** Only if they already understand C-CDA. The documentation provides no vendor-specific detail, no field mappings, no edge cases, and no sample output. It essentially says "we export C-CDA" and lists the section names — which are defined by the standard, not the vendor.

## 7. Overall Assessment

### Classification

**Standard-based projection**: The export is entirely a C-CDA document with no native data model components. It covers only the standard C-CDA clinical summary sections and explicitly omits billing, notes, documents, orders, messages, insurance, and other data domains that the product stores. This is a textbook case of C-CDA repackaging being called "(b)(10)."

### Key Findings

1. **C-CDA repackaging, not "all EHI"**: The export is exclusively C-CDA — a clinical summary standard designed for transitions of care, not comprehensive data export. It covers an estimated 20–30% of what the product stores about patients. The product's billing, document management, orders, notes, messages, and insurance data are entirely absent.

2. **Billing/PM data completely excluded**: Despite having a dedicated Billing tab, Clearing House tab, claim scrubbing technology, CMS-1500 generation, and revenue cycle management, zero billing or financial data appears in the export. This is the single largest gap given the product's integrated EHR+PM positioning.

3. **Clinical notes and documents excluded**: The patient chart UI (visible in PDF page 3) shows "Notes" and "Documents" navigation items, but the C-CDA export has no section for free-text clinical notes or uploaded documents. This omits a core part of the clinical record.

4. **Documentation is essentially empty**: 61 fields total, all with zero descriptions, zero types, zero value sets. The "data dictionary" is just a restatement of C-CDA section headers that any developer could find in the HL7 specification. No sample data, no schema, no import guidance.

5. **Version discrepancy**: The PDF documentation references version 22.0, but the certified product is version 25.0. Whether the export has changed between versions is unknown.

### Summary Stats

```
Classification:  Standard-based projection (C-CDA repackaging)
Export format:   C-CDA (HL7 CDA R2 Consolidated CDA R2.1)
Model type:      Standard projection (no native database export)
Entities:        21 C-CDA sections (17 clinical + 4 header)
Fields:          61
Descriptions:    0% (0 of 61 fields have descriptions)
Sample data:     No
Bulk export:     Yes (via Patient Screening module)
Domains covered: 1 of 17 adequately; 8 of 17 partially; 8 of 17 not covered
```

### Bottom Line

DigiDMS's (b)(10) export is a standard C-CDA clinical summary repackaged as "EHI export." A patient or provider would receive a basic clinical summary (allergies, problems, meds, vitals, labs, immunizations) but would not get their billing records, clinical notes, documents, orders, insurance information, or portal messages — all of which the product stores. The single biggest gap is the complete absence of billing and practice management data from an integrated EHR+PM system.
