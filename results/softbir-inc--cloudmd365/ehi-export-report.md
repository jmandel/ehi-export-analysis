# Softbir, Inc. — EHI Export Documentation

Collected: 2026-02-16

## Source
- Registered URL: https://docindy.com/assets/CloudMD365%20EHI%20Export%20Documentation-Befwxq4M.pdf
- CHPL ID: 10282
- Product: CloudMD365, Version 1
- Certification date: 2020-01-22

## Navigation Journal

The registered URL is a direct PDF download. No navigation required.

```bash
# Probe headers
curl -sI -L "https://docindy.com/assets/CloudMD365%20EHI%20Export%20Documentation-Befwxq4M.pdf" \
  -H 'User-Agent: Mozilla/5.0'
# Returns HTTP 200, Content-Type: application/pdf, Content-Length: 157444

# Download
curl -sL "https://docindy.com/assets/CloudMD365%20EHI%20Export%20Documentation-Befwxq4M.pdf" \
  -H 'User-Agent: Mozilla/5.0' \
  -o downloads/CloudMD365-EHI-Export-Documentation.pdf
```

The PDF is 7 pages, produced by Google Docs Renderer (Skia/PDF m132). No embedded files or attachments. No URLs embedded in the PDF linking to additional documentation.

## What Was Found

The document is a single 7-page PDF titled "CloudMD365 EHI Export Documentation." It covers three topics: file format/structure, extraction process, and data interpretation.

### Export Format

The export is a **JSON file** containing patient data. The document mentions JSON or XML as possibilities but the sample and field definitions are all JSON-oriented. A sample JSON snippet is provided showing a simple patient object with nested name and demographics.

### Export Process

The extraction process is straightforward:
1. Log into CloudMD365
2. Navigate to Admin > Export Patient Health Data
3. Select patients to export
4. Set parameters (date range for encounters)
5. Click Export, then download the generated file

The export is per-patient (select specific patients) with a date range filter for encounters.

### Data Dictionary

The document defines six data sections with field-level definitions (field name, data type, short description):

**1. Patient Demographics** (10 fields)
- patient_id (GUID), first_name, last_name, date_of_birth, gender, address (Object), email
- Address sub-object: street, city, state, zip_code, home_phone, work_phone

**2. Health Summary** (3 fields)
- chronic_conditions (Array of Problem), diagnosis (Array of Problem), family_history (Array of String)
- Problem sub-object: problem (String), icd_10 (String)

**3. Medications** (5 fields)
- medication (Array of Object), dosage, frequency, start_date, end_date

**4. Allergies** (3 fields)
- allergy, type, reaction

**5. Encounters** (10 fields)
- encounter_date, chief_complaint, diagnosis (Array of Problem), treatment, care_plan_goals (Array of String), care_plan_actions (Array of String), care_plan_followup, provider_id (GUID), provider_name, notes

**6. RPM Data** (5 fields)
- recorded_time, data_type, attribute_type, value (Float), unit

Total: ~36 fields across 6 entities (plus 2 sub-objects).

### Data Standards

The document states the EHI file "adheres to standards like HL7 FHIR to ensure interoperability" — but there is no actual use of FHIR resource types, FHIR profiles, or FHIR-specific structure in the documented format. The JSON format shown is a custom/proprietary structure, not FHIR. The mention of FHIR appears to be aspirational or boilerplate rather than descriptive of the actual export.

## Export Coverage Assessment

### Data Domain Coverage

The product research reveals CloudMD365/iVisitDoc is a behavioral health-oriented EHR with telehealth, eMAR, care coordination, and billing capabilities. Comparing the documented export against what the product stores:

**Covered domains:**
- Patient demographics (basic — name, DOB, gender, address, contact)
- Problem list / diagnoses (with ICD-10 codes)
- Medications (with dosage, frequency, dates)
- Allergies (type and reaction)
- Encounters (date, complaint, diagnosis, treatment, care plan, provider, notes)
- RPM data (remote monitoring vitals)
- Care plans (goals, actions, follow-up — embedded in encounters)
- Family history (as array of strings in health summary)

**Missing or absent domains — significant gaps:**
- **Billing data**: The product has integrated billing and CCM/TCM billing (Medicare codes 99490, 99487, 99489). None of this appears in the export. No charges, claims, payments, or billing codes.
- **Behavioral health-specific data**: The product's core strength is behavioral health — therapy session notes (SOAP/DAP format), DSM-5 coding, treatment plans linked to patient journeys, assessment forms, outcome measures, homework planners, utilization review, pre-admission workflows, rounds/security checks. None of these specialty-specific data types appear in the export.
- **Medication Administration Records (eMAR)**: The eMARneek module tracks medication administration with barcode verification, quantities, and reorder notifications. The export only includes prescribed medications, not administration records.
- **Documents and attachments**: No mention of clinical documents, uploaded files, images (e.g., dermatology consultation images), or scanned records.
- **Electronic signatures**: The product captures patient and guardian signatures. Not in the export.
- **Patient-provided data**: Medical history disclosures, patient-uploaded images. Not in the export.
- **Communication records**: HIPAA-compliant messages, telehealth visit records. Not in the export (encounters may capture visit metadata but not the communications themselves).
- **Lab results**: Despite having a lab interface with 90+ testing partners and certified CPOE for labs (a)(1), there is no lab results section in the export. The encounters section might include some lab information in notes, but there is no structured lab data.
- **Diagnostic imaging orders/results**: Certified for CPOE diagnostic imaging (a)(1) but no imaging data in the export.
- **Insurance/enrollment information**: Not in the export despite verification of benefits being a product feature.
- **Discharge planning and aftercare records**: Product features but absent from export.

**The export covers roughly 6 clinical data categories out of ~15+ data domains the product manages.** The missing domains include both EHI-qualifying data (billing records, clinical documents, lab results, specialty assessments) and data that is clearly part of the designated record set (medication administration records, behavioral health assessments, treatment plans as standalone entities).

### Export Format & Standards

The export uses a **custom JSON format** — not FHIR, not C-CDA, not any recognized healthcare standard. Despite the document claiming adherence to "HL7 FHIR," the actual structure is a flat proprietary JSON with no FHIR resource types, no references, no coded terminologies beyond ICD-10, and no standard identifiers.

The format is simple and readable but lacks:
- Standard terminology bindings (SNOMED, LOINC, RxNorm — only ICD-10 is mentioned)
- Explicit value set definitions for coded fields (e.g., what are valid values for `gender`? `type` of allergy?)
- Relationship/reference mechanisms between entities
- Metadata (export date, system version, provenance)

A third party could parse this JSON but would have limited ability to semantically interpret many fields without additional context.

### Documentation Quality

The documentation is **minimal but clear**. It reads like a compliance artifact rather than a developer-oriented technical specification:

- **Strengths**: Clean layout, field-level definitions with data types, a sample JSON snippet, step-by-step extraction instructions.
- **Weaknesses**:
  - No sample export file showing a complete patient record (the sample only shows a demographics fragment)
  - No value set definitions for coded fields
  - No specification of array element structure for some fields (e.g., medications says `medication` is "Array of Object" but the sub-fields are listed flat, not as object properties)
  - No error handling or edge case documentation
  - No versioning or change history
  - The FHIR claim is misleading — the format is not FHIR
  - No machine-readable schema (JSON Schema, OpenAPI, etc.)

A developer could implement a basic import from this documentation but would encounter ambiguities around nested structures, coded values, and missing data handling.

### Structure & Completeness

The field-level documentation covers **6 entities with ~36 fields total**. This is very sparse for an EHR that manages behavioral health patients. For comparison:
- Demographics: 10 fields (reasonable for basics, but missing race, ethnicity, language, marital status, emergency contacts)
- Health summary: 3 fields (very high-level — just lists of conditions and family history strings)
- Medications: 5 fields (missing prescriber, pharmacy, NDC/RxNorm codes, route, status)
- Allergies: 3 fields (missing severity, onset date, status)
- Encounters: 10 fields (the most detailed section — includes care plan elements)
- RPM: 5 fields (reasonable for vitals data)

There are no relationships between entities (e.g., which encounter prescribed which medication), no value sets documented, and no cardinality constraints.

### (b)(10) vs (g)(10) Assessment

This is **not** a case of (g)(10) FHIR API documentation being repackaged as (b)(10). The export is genuinely a separate, proprietary JSON export mechanism accessed through the admin interface. However, it appears to cover approximately the same narrow scope of data that a basic USCDI/US Core export would cover (demographics, conditions, medications, allergies, encounters) — plus RPM data, which is a product-specific addition.

The fundamental problem is **breadth**: the export captures a patient clinical summary, not a comprehensive dump of all electronic health information the system stores about a patient. The behavioral health specialty data, billing records, medication administration records, lab results, documents, and communications are all absent. This is a significant gap for a (b)(10) requirement that mandates export of the entire designated record set.

### Overall Assessment

This is a **minimal compliance effort** — a short PDF documenting a basic patient summary export. The documentation is honest (it doesn't overclaim) but severely incomplete relative to the data the product manages. The export appears to produce a JSON file containing a clinical summary of roughly the same scope as a C-CDA CCD, but in a proprietary format without standard terminologies.

For a ~20-employee company with a small customer base, this is not unusual — the documentation fulfills the letter of having *something* for (b)(10) while leaving significant data domains unaddressed. The 7-page PDF with ~36 field definitions is among the thinnest EHI export documentation in the CHPL ecosystem.

## Access Summary
- Final URL (after redirects): https://docindy.com/assets/CloudMD365%20EHI%20Export%20Documentation-Befwxq4M.pdf
- Status: found
- Required browser: no
- Navigation complexity: direct_link
- Anti-bot issues: none

## Obstacles & Dead Ends

None. The URL returned a clean PDF download on the first attempt with no redirects, authentication, or anti-bot measures.
