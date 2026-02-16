# EHI Export Analysis: QRS, Inc.

**Product**: PARADIGM® Version 22
**Analysis date**: 2026-02-16
**CHPL IDs**: 15.04.04.2838.PARA.22.01.1.221227

## 1. Product Context

PARADIGM® is an integrated EHR and Practice Management (PM) suite for ambulatory physician practices, developed by QRS, Inc. (Knoxville, TN; founded 1983, ~51–200 employees). The EHR and PM modules share a single database. The product targets small to mid-size practices across 50+ specialties (family medicine, internal medicine, pediatrics, cardiology, dermatology, OB-Gyn, orthopedics, psychiatry, and many more).

**Clinical capabilities** include clinical documentation with customizable templates, e-prescribing with full FDA drug database, speech recognition/dictation, scanning and document management (PDF, images, audio, video), patient flow management, recalls/follow-up, and a patient portal.

**Practice management capabilities** include appointment scheduling, billing/charge posting, claims management with electronic submission, ERA processing, insurance eligibility verification, patient/guarantor billing, inventory management, and optional modules for HL7 interfaces, insurance contract management, referral management, and specialty-specific billing (radiology, allergy, chiropractic, ambulance).

**Certified criteria** include (b)(10) EHI Export, (b)(11) Bulk Data Export, (g)(10) FHIR API, and numerous clinical, quality, patient engagement, and public health criteria (37 total).

For a complete EHI export, the product should cover: demographics, problems/conditions, medications, allergies, immunizations, vitals, lab results, procedures, clinical notes/documents, encounters, care plans, goals, family history, implantable devices, billing/claims data, insurance/coverage, payments, and specialty-specific clinical data. The presence of a full PM module means billing/financial data is a key domain.

## 2. Artifacts Reviewed

| Artifact | Size/Scope | Description | Informativeness |
|---|---|---|---|
| `PARADIGM_EHI_Export_Documentation.pdf` | 6 pages (163 KB); 4 pages legal boilerplate, 2 pages technical | Core (b)(10) EHI export documentation. Version 1.0, dated 2023-09-26. Describes ZIP export format, EHI checkbox, and two REST API endpoints. | **Primary source** — but extremely thin. The only document describing what the EHI export actually produces. |
| `PARADIGM_FHIR_API_Documentation.pdf` | 27 pages (279 KB); 4 pages legal boilerplate, 23 pages technical | (g)(10) FHIR R4 API documentation. Documents 15 US Core resource types with request/response parameters and example JSON. | **Supplementary** — documents the FHIR API, not the EHI export, but indicates which clinical data domains the product exposes via FHIR. |
| `PARADIGM_Patient_API_Documentation.pdf` | 6 pages (160 KB); 4 pages legal boilerplate, 2 pages technical | Non-FHIR REST API for patient search and C-CDA retrieval. Same endpoints as EHI export doc. | **Low** — nearly identical to pages 5–6 of the EHI export doc. |
| `qrshs-info-main-page.html` | 29 KB | QRS Disclosures landing page listing all compliance PDFs. | **Navigation only** — confirms no additional EHI documentation exists beyond the three PDFs. |

No sample data, no data dictionary, no JSON schema, no machine-readable artifacts of any kind were found. The `enrichment/` directory is empty.

## 3. Export Mechanics

- **Format**: ZIP archive containing:
  - C-CDA XML document per patient (e.g., `10000.xml`)
  - Supplemental JSON files (e.g., `10000_invoice history.json`)
  - Imported files in original format (e.g., `10000_addt_files/` containing PDFs, PNGs, etc.)
- **Mechanism**: UI-based. The "Data Portability module" is accessed through "EHR System Reports" by authorized users. An EHI checkbox ("include all Electronic Healthcare Information (EHI) for each patient in the set") enables the full export.
- **API access**: Two REST endpoints using Basic auth at `api.qrshs.com/v1/`:
  - `GET /patient/search` — lookup by name, DOB, or SSN
  - `GET /patient/ccda` — retrieve C-CDA for a patient (with optional date filtering)
- **Single-patient vs bulk**: The EHI export doc references "a patient or set of patients," suggesting both single and batch export are supported.
- **Access constraints**: API access requires developer account registration "through direct consultation and permission of a QRS Client" per the Terms and Conditions (pages 1–4 of the EHI doc).

## 4. Export Content: What's In It

### No data dictionary

The EHI export documentation contains **zero field-level documentation**. There is no data dictionary, no schema, no list of tables or fields, no value sets, and no sample data. The entire technical content is 2 pages (pages 5–6 of the 6-page PDF), and it describes the export at a structural level only (ZIP → C-CDA + JSON + files).

### What is documented

The documentation describes three export components but provides no detail about their internal structure:

| Component | Format | Naming Convention | Documentation Level |
|---|---|---|---|
| Patient clinical data | C-CDA XML | `{patient_code}.xml` | Name only — no specification of which C-CDA sections are populated or how |
| Supplemental data | JSON | `{patient_code}_{info_type}.json` | Single example filename only (`10000_invoice history.json`); no schema, no field list |
| Imported files | Original format (PDF/PNG/etc) | `{patient_code}_addt_files/` directory | Described generically; no metadata schema |

### Vendor's own content organization

The vendor does not organize the export into categories or domains. The only structure described is the three-component ZIP (C-CDA + JSON + files). There is no table/entity breakdown to present.

### FHIR API as proxy for clinical content

While the FHIR API documentation (27 pages) is not the EHI export itself, it provides the best available evidence of what clinical data PARADIGM stores and can export. The FHIR API documents 15 US Core resource types with 117 total response parameters (`analysis/fhir_resources.json`):

| FHIR Resource | Response Parameters | Clinical Domain |
|---|---|---|
| Patient | 10 | Demographics |
| AllergyIntolerance | 7 | Allergies |
| CarePlan | 5 | Care plans |
| CareTeam | 3 | Care teams |
| Condition | 6 | Problems/diagnoses |
| Device | 12 | Implantable devices |
| DiagnosticReport | 13 | Lab/diagnostic reports |
| DocumentReference | 10 | Clinical notes/documents |
| Goal | 5 | Goals |
| Immunization | 7 | Immunizations |
| MedicationRequest | 11 | Medications/prescriptions |
| Observation | 7 | Vitals, labs, smoking status |
| Procedure | 5 | Procedures |
| Encounter | 13 | Encounters/visits |
| Provenance | 3 | Data provenance |

These are standard US Core / USCDI resources. The C-CDA in the EHI export likely maps to the same clinical domains, but this is inference — the EHI export doc does not confirm which sections are included.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor describes three export components but provides almost no detail:

1. **C-CDA XML**: Standard clinical summary document. Based on the FHIR API documentation (which covers the same product), the clinical domains likely include demographics, allergies, conditions, medications, immunizations, procedures, vitals, labs/diagnostics, clinical notes, encounters, care plans, goals, care teams, and implantable devices. However, this is C-CDA — it captures clinical summaries, not the vendor's native data model.

2. **Supplemental JSON**: The only example given is "invoice history," suggesting billing/invoice data. The format is completely undocumented. It is unknown whether other JSON supplements beyond invoice history are produced, what fields they contain, or how they relate to the C-CDA data.

3. **Imported files**: Scanned documents, images, audio recordings, faxes, and other files stored in the patient chart. These are exported in their original format. No metadata about these files is documented.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | C-CDA likely includes demographics (FHIR API shows Patient resource with 10 params) | C-CDA covers standard demographics; unknown if vendor-specific fields are captured |
| Encounters / visits | ⚠️ Partial | C-CDA likely includes encounters (FHIR API shows Encounter resource with 13 params) | Standard C-CDA encounter data only |
| Problems / conditions | ⚠️ Partial | C-CDA likely includes problem list (FHIR API shows Condition resource; certified (a)(5)) | Standard C-CDA section |
| Medications / prescriptions | ⚠️ Partial | C-CDA likely includes medications (FHIR API shows MedicationRequest; e-prescribing feature) | C-CDA covers basic medication data; vendor's full e-prescribing data model likely has more detail |
| Allergies | ⚠️ Partial | C-CDA likely includes allergies (FHIR API shows AllergyIntolerance; certified (a)(2) drug-allergy) | Standard C-CDA section |
| Immunizations | ⚠️ Partial | C-CDA likely includes immunizations (FHIR API shows Immunization; certified (f)(1)) | Standard C-CDA section |
| Vitals | ⚠️ Partial | C-CDA likely includes vitals (FHIR API shows Observation) | Standard C-CDA section |
| Lab results | ⚠️ Partial | C-CDA likely includes labs (FHIR API shows DiagnosticReport, Observation) | Standard C-CDA section; HL7 lab interface data may not fully map |
| Imaging / diagnostic reports | ⚠️ Partial | Via DiagnosticReport in C-CDA; imported images via `_addt_files` | Images in original format; no structured radiology data documented |
| Procedures | ⚠️ Partial | C-CDA likely includes procedures (FHIR API shows Procedure resource) | Standard C-CDA section |
| Clinical notes / documents | ⚠️ Partial | C-CDA narrative sections; imported documents via `_addt_files`; voice recordings (.wav) likely in `_addt_files` | Notes available as C-CDA sections and/or raw files; not as structured vendor data |
| Care plans / goals | ⚠️ Partial | C-CDA may include these (FHIR API shows CarePlan, Goal) | Available in FHIR API but not confirmed in EHI export |
| Orders / referrals | ❌ Not covered | No evidence in export documentation | Product has referral management module; not documented in export |
| Insurance / coverage | ❌ Not covered | No insurance/eligibility entities in export documentation | Product does insurance eligibility verification; significant gap |
| Claims / billing | ⚠️ Partial | "Invoice history" JSON mentioned as example filename | Product has full claims/billing module; the undocumented "invoice history" JSON is the only evidence of billing data in the export. Without schema or sample data, impossible to assess completeness |
| Payments | ❌ Not covered | No payment entities documented | Product processes ERA and payments; not documented in export |
| Family health history | ❌ Not covered | Not mentioned in EHI export doc | Certified (a)(12); gap |
| Implantable devices | ⚠️ Partial | Available in FHIR API (Device resource with 12 params) but not confirmed in EHI export | Certified (a)(14); may be in C-CDA but not confirmed |
| Patient communications / portal | ❌ Not covered | No portal messages or communication entities documented | Product has patient portal; gap |
| Specialty-specific data | ❌ Not covered | No specialty-specific entities or templates documented | Product supports 50+ specialties with customizable templates; no evidence of specialty data in export |
| Consents / directives | ❌ Not covered | No consent entities documented | N/A — no evidence product stores structured consent data |

## 6. Documentation Quality

The EHI export documentation quality is **very poor**:

- **67% legal boilerplate**: 4 of 6 pages are Terms and Conditions (identical across all three PDFs). Only 2 pages describe the export.
- **No data dictionary**: Zero field-level documentation for any export component.
- **No JSON schema**: The supplemental JSON format (which carries non-C-CDA data like billing) is completely undefined. A developer cannot interpret these files without reverse-engineering.
- **No sample data**: No example export files, no sample C-CDA, no sample JSON structures.
- **No machine-readable artifacts**: No XSD, JSON Schema, OpenAPI spec, or any programmatic specification.
- **No screenshots or user guide**: The usage instructions are a single sentence: access through EHR System Reports and click the EHI checkbox.
- **Stale**: Version 1.0, dated September 26, 2023 (over 2 years old), never updated.

A developer attempting to build an import for PARADIGM EHI exports could process the C-CDA (a recognized standard) but would be unable to interpret the JSON supplements or understand the metadata of attached files. The FHIR API documentation (27 pages, with request/response parameters and example JSON for each resource) is substantially more detailed but serves the (g)(10) requirement, not (b)(10).

## 7. Overall Assessment

### Classification

**Standard-based projection**: The EHI export is primarily a C-CDA document with an undocumented JSON sidecar and raw file attachments. The C-CDA provides a standard clinical summary covering the USCDI data elements but does not represent the vendor's native data model. The supplemental "invoice history" JSON suggests awareness that billing data must be included beyond C-CDA, but its lack of documentation makes it unusable in practice.

### Key Findings

1. **Only 2 pages of technical content**: The core EHI export documentation is 6 pages, but 4 are legal boilerplate. The entire export is described in ~500 words with no field-level detail. (`PARADIGM_EHI_Export_Documentation.pdf`, pages 5–6)

2. **Undocumented JSON supplement is the critical gap**: The "invoice history" JSON is the only evidence that non-clinical data is included in the export, but its structure is completely unspecified — no schema, no field names, no sample data. This makes the billing portion of the export effectively opaque to any recipient. (`PARADIGM_EHI_Export_Documentation.pdf`, page 5)

3. **C-CDA + JSON + files is architecturally reasonable**: QRS shows awareness that EHI extends beyond clinical summaries by including JSON supplements and imported files alongside the C-CDA. The approach of C-CDA for clinical data + JSON for billing + raw files for documents is a defensible design — but without documentation of the JSON format, it fails in practice.

4. **Multiple data domains are unaddressed**: Insurance/coverage, payments, referrals, family history, patient portal messages, and specialty-specific clinical data (for 50+ supported specialties) have no evidence of inclusion in the export. The product's PM module handles claims, ERA, eligibility, and billing — this is a significant data domain with no documented export coverage beyond the undefined "invoice history."

5. **FHIR API is substantially better documented than the EHI export**: The FHIR API doc (27 pages, 15 resources, 117 response parameters with examples) demonstrates the vendor can produce detailed technical documentation — they simply didn't do it for the (b)(10) export. (`PARADIGM_FHIR_API_Documentation.pdf`)

### Summary Stats

```
Classification:  Standard-based projection
Export format:   C-CDA XML + undocumented JSON + raw files (ZIP)
Model type:      Standard projection (C-CDA) with proprietary supplement
Entities:        3 components described (C-CDA, JSON supplement, attached files); no entity/table breakdown
Fields:          N/A (no data dictionary)
Descriptions:    N/A
Sample data:     No
Bulk export:     Yes (set of patients supported)
Domains covered: 0 fully covered; ~10 of 17 partially via C-CDA inference; 5–7 not covered
```

### Bottom Line

PARADIGM's EHI export is a C-CDA clinical summary with an undocumented JSON sidecar and file attachments — not a comprehensive native data export. A recipient would get standard clinical data via C-CDA but could not interpret the billing JSON or know what other data domains are missing. The single biggest gap is the complete absence of documentation for the non-C-CDA portions of the export, which are precisely the data (billing, specialty-specific, administrative) that make a (b)(10) export different from a (g)(10) FHIR API.
