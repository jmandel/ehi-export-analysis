# EndoSoft, LLC — EHI Export Documentation

Collected: 2026-02-15

## Source
- Registered URL: https://www.endosoft.com/ephi/
- CHPL IDs: 10854
- Product: EndoVault 3.2
- Certification date: 2022-03-10

## Navigation Journal

### Step 1: Probe the registered URL
```bash
curl -sI -L "https://www.endosoft.com/ephi/" -H 'User-Agent: Mozilla/5.0'
```
Returned HTTP 200, Content-Type: text/html. WordPress site. Page loaded successfully.

### Step 2: Fetch and examine the EHI export page
```bash
curl -sL "https://www.endosoft.com/ephi/" -H 'User-Agent: Mozilla/5.0' -o ephi-page.html
```
Page title: "EndoSoft® ePHI - Secure Protected Health Information". The page describes two EHI export methods:

1. **Single/multi patient export** using HL7 C-CDA 2.1 guidelines (XML files + CDA.xsl stylesheet)
2. **Bulk EHI Export** using FHIR APIs, with a link labeled "here" pointing to `https://old.endosoft.com/fhir/#_Toc120735483`

The page lists 22 data sections available for export: Allergies, Encounter, Immunizations, Medications, Plan of treatment, Referral reason, Active problems, Reason for visit, Implants, Health concerns, Procedures, Functional status, Results, Social history, Vitals, Goals, Discharge instructions, Assessments, Cognitive status, Media, Diagnostic Report, Documents, Service Request.

### Step 3: Follow the "here" link for Bulk EHI Export
The link on the EHI page points to `https://old.endosoft.com/fhir/#_Toc120735483`. This URL is **broken**:
- HTTPS returns `ERR_CERT_COMMON_NAME_INVALID` (invalid SSL certificate)
- With `-k` (skip cert verification): returns HTTP 502 Bad Gateway
- No Wayback Machine snapshots exist for `old.endosoft.com/fhir/`

### Step 4: Find the working FHIR documentation
Discovered that `https://www.endosoft.com/fhir/` exists and returns HTTP 200. This page describes the EndoVault SMART on FHIR service and contains a "Click Here to View FHIR API" link pointing to a PDF:
```bash
curl -sL "https://www.endosoft.com/wp-content/uploads/2024/09/170.315-g10-Standardized-API-FHIR-2.pdf" -o 170.315-g10-Standardized-API-FHIR-2.pdf
```
The PDF downloaded successfully — 138 pages, 1.3 MB, titled "API Definition" dated 11/25/2022 by EndoSoft LLC.

### Step 5: Check the mandatory disclosures page
```bash
curl -sL "https://www.endosoft.com/mu_stage3/" -H 'User-Agent: Mozilla/5.0'
```
The page confirms certification for 170.315 (b)(10) Electronic Health Information Export along with all other criteria. Contains a cost disclosure link:
```bash
curl -sL "https://www.endosoft.com/wp-content/uploads/2025/10/endovault_ehr_disclosure_onc_2015-10_15_25.xlsx" -o endovault_ehr_disclosure_onc_2015-10_15_25.xlsx
```
Downloaded successfully (23 KB XLSX file).

### Step 6: Examine the FHIR API PDF
The 138-page PDF covers the full EndoVault SMART on FHIR API, including:
- Authorization (OAuth 2.0, SMART on FHIR)
- Individual patient API endpoints (pages 5-119)
- **Bulk Data Access section** (pages 120-132)
- EndoVault API resources table (page 134)
- API Rate and Quota (page 135)
- Examples (page 135)
- Terms of Service (pages 136-138)

## What Was Found

EndoSoft documents two EHI export mechanisms:

### 1. Single/Multi-Patient C-CDA Export
The EHI page states that EndoVault exports patient data in CCD/C-CDA format using HL7 C-CDA 2.1 guidelines. The export produces:
- `*.xml` files containing discrete data elements
- `CDA.xsl` stylesheet for rendering

Users can select from 22 named data sections to include in the export. The documentation for this method is limited to the brief description on the `/ephi/` page itself — there is no separate data dictionary, schema, or detailed specification for the C-CDA export format.

### 2. Bulk EHI Export via FHIR API
The Bulk EHI Export uses the same FHIR API documented in the 138-page PDF (`170.315-g10-Standardized-API-FHIR-2.pdf`). The Bulk Data section (pages 120-132) describes static NDJSON file endpoints for 18 FHIR resource types:

| Resource | Bulk Endpoint |
|----------|--------------|
| AllergyIntolerance | `/bulk/allergyintolerance-bulkfile.ndjson` |
| CarePlan | `/bulk/careplan-bulkfile.ndjson` |
| CareTeam | `/bulk/careteam-bulkfile.ndjson` |
| Condition | `/bulk/condition-bulkfile.ndjson` |
| Device | `/bulk/device-bulkfile.ndjson` |
| DiagnosticReport | `/bulk/diagnosticreport-bulkfile.ndjson` |
| DocumentReference | `/bulk/documentreference-bulkfile.ndjson` |
| Encounter | `/bulk/encounter-bulkfile.ndjson` |
| Goal | `/bulk/goal-bulkfile.ndjson` |
| Immunization | `/bulk/immunization-bulkfile.ndjson` |
| MedicationRequest | `/bulk/medicationrequest-bulkfile.ndjson` |
| Observation | `/bulk/observation-bulkfile.ndjson` |
| Organization | `/bulk/organization-bulkfile.ndjson` |
| Practitioner | `/bulk/practitioner-bulkfile.ndjson` |
| Procedure | `/bulk/procedure-bulkfile.ndjson` |
| Provenance | `/bulk/provenance-bulkfile.ndjson` |
| RelatedPerson | `/bulk/relatedperson-bulkfile.ndjson` |
| ServiceRequest | `/bulk/servicerequest-bulkfile.ndjson` |

Each resource endpoint is documented with a sample JSON response. The samples are generally well-formed FHIR R4 resources using standard US Core profiles.

The individual patient API section covers the same 18 resource types with more detailed query parameters and search capabilities per resource.

## Export Coverage Assessment

### Data Domain Coverage

EndoVault is a specialty EHR focused on procedure-based specialties (primarily gastroenterology/endoscopy, with extensions into oncology, pulmonology, and others). Comparing the product research to the documented export:

**Clearly covered (via FHIR resources and C-CDA sections):**
- Demographics (Patient)
- Allergies (AllergyIntolerance)
- Medications (MedicationRequest)
- Diagnoses / Problem lists (Condition)
- Immunizations (Immunization)
- Procedures (Procedure)
- Lab results, vitals, clinical observations (Observation — the PDF has extensive documentation spanning pages 45-103 covering vital signs, lab results, smoking status, pulse ox, and social determinants)
- Care plans (CarePlan)
- Care teams (CareTeam)
- Goals (Goal)
- Encounters (Encounter)
- Diagnostic reports (DiagnosticReport)
- Documents / clinical notes (DocumentReference)
- Implantable devices (Device)
- Service requests / orders (ServiceRequest)
- Related persons (RelatedPerson)
- Provenance tracking (Provenance)

**Missing or not mentioned — significant gaps given the product's specialty focus:**
- **Endoscopy images and video** — This is arguably the most critical data type for EndoVault. The product was built around HD endoscopic image capture (BMP, JPEG, TIF, DICOM) and video recording (AVI, 4K). The FHIR export includes "Media" as a C-CDA section name but the Bulk Data API does not include a Media resource endpoint. There is a DocumentReference resource that could theoretically reference images, but the sample data shows only clinical notes, not images. The export documentation does not address how the product's core imaging data is exported.
- **Procedure-specific endoscopy findings** — EndoVault stores rich specialty data: polyp characteristics, cecal intubation records, bowel prep quality scores (Boston scale), adenoma detection data, scope tracking. None of this specialty data is addressed in the FHIR export documentation. It is unclear whether this data is captured in Observation or Procedure resources, or omitted entirely.
- **Oncology-specific data** — Cancer staging (TNM, ICD-O-3), chemotherapy regimens, radiation therapy orders, adverse reaction histories, lifetime medication restrictions, tumor board records, clinical trial consent. None of these are mentioned in the export.
- **Electronic Nursing Record (ENR) data** — Vital sign recordings from monitors during procedures, medication administration during procedures, sedation scores, IV assessments, pain scales, adverse events, consciousness levels, discharge status. The Observation resource may capture some vitals, but the procedural nursing workflow data is not addressed.
- **Pathology data** — Pathology requisitions and results are a named module in EndoVault but have no specific export representation beyond what may be in DiagnosticReport.
- **Billing/charge data** — Time and material billing data (items used per procedure, room utilization) is generated in EndoVault. There is no billing-related FHIR resource in the export.
- **Scheduling/recall data** — While scheduling is operational data (not necessarily EHI), recall management for follow-up procedures (e.g., colonoscopy surveillance) could be clinically relevant if it documents care recommendations.
- **Patient portal data** — Patient-submitted questionnaires and electronic messages. Not addressed.
- **E-prescriptions** — Surescripts prescriptions are mentioned in the product but MedicationRequest only captures medication orders, not the full e-prescribing transaction.
- **Quality metrics** — Registry data (GIQuIC, AGA) and quality indicators. These are aggregated metrics and may not qualify as EHI, but individual patient quality data (e.g., a specific patient's adenoma detection) would be.
- **PACS/DICOM images** — The integrated PACS with DICOM-compliant storage is a core feature. Export of DICOM images is not documented.

### Export Format & Standards

The export uses two recognized standards:
1. **C-CDA 2.1** (HL7) for single/multi-patient export — a well-established clinical document format
2. **FHIR R4 NDJSON** for bulk export — using what appear to be standard US Core profiles

Both are appropriate standards for clinical data exchange. However, the FHIR bulk export appears to be a repackaging of the (g)(10) standardized API as the (b)(10) export. The evidence:

- The PDF is titled "170.315-g10-Standardized-API-FHIR-2.pdf" — it is explicitly the g(10) documentation
- The resource types (18 total) map precisely to the US Core resource types required by g(10)
- There are no EndoVault-custom FHIR profiles or extensions for specialty data
- No resource types exist for the product's core differentiators (endoscopy images, procedure findings, oncology data)
- The Bulk Data endpoints are simple static NDJSON file downloads, not a true Bulk Data Export API with kick-off/status/download workflow

The C-CDA export's 22 named sections align with standard C-CDA sections and include some additions (Media, Diagnostic Report, Documents, Service Request) but there is no documentation of how specialty data maps to these sections.

**A third party could reconstruct a basic clinical summary** (demographics, problems, meds, allergies, labs, vitals, encounters) from the export, but could **not** reconstruct the complete patient record as stored in EndoVault. The endoscopy procedure documentation, imaging, oncology data, and procedural nursing records — the product's primary clinical value — are not covered.

### Documentation Quality

- **Readability**: The EHI export page itself is clear and well-organized, though very brief. The 138-page FHIR API PDF is reasonably structured with a table of contents and resource-by-resource documentation.
- **Data dictionary**: There is no field-level data dictionary. The FHIR API PDF provides sample JSON responses for each resource type, which implicitly show the data model. However, these are standard FHIR resource structures — there is no EndoVault-specific mapping documentation showing which EndoVault database fields map to which FHIR elements.
- **Data types and value sets**: Relies entirely on standard FHIR data types and US Core value set bindings. No EndoVault-specific coded value documentation.
- **Worked examples**: The PDF includes sample JSON responses for each resource type and bulk endpoint, plus three example API calls with base64-encoded parameters.
- **Developer implementability**: A developer familiar with FHIR could implement an import of the exported data. However, they would only receive the US Core clinical summary subset, not the full EndoVault dataset.
- **Maintenance**: The PDF was authored 2022-12-12 and last modified the same day. The EHI page was last modified 2025-03-25. The cost disclosure XLSX is dated October 2025. The documentation appears to be maintained but the FHIR API PDF has not been updated since initial certification.

### Structure & Completeness

- **Field-level granularity**: The bulk data section documents each resource type with a sample JSON response. The individual API section (pages 15-119) provides more detail on query parameters and response structures per resource. However, there are no field-by-field descriptions, cardinality constraints, or required vs. optional designations beyond what FHIR US Core defines.
- **Coded fields**: Standard FHIR code systems are used (SNOMED, LOINC, ICD-10). No EndoVault-specific code sets are documented.
- **Relationships**: FHIR references between resources are shown in sample data (e.g., Encounter references in Conditions, Patient references everywhere). No entity-relationship diagram.
- **Versioning**: No versioning or change history beyond the PDF creation date.

### Overall Assessment

EndoSoft's EHI export documentation reveals a classic (b)(10)/(g)(10) conflation. The "Bulk EHI Export" is the same FHIR API used for g(10) certification, repackaged as the b(10) mechanism. This covers the US Core / USCDI clinical data subset but misses the product's core value proposition and specialty data:

1. **Endoscopy imaging and video** — the product's original raison d'être — has no documented export path
2. **Specialty procedure documentation** (polyp findings, bowel prep scores, cecal intubation) — not addressed
3. **Oncology data** (staging, chemo, radiation) — not addressed
4. **Procedural nursing records** (ENR) — not addressed
5. **Billing/charge data** — not addressed
6. **Pathology data** — not specifically addressed

The C-CDA single-patient export may capture slightly more than the FHIR bulk export (it lists 22 sections including "Media"), but there is no detailed documentation of what "Media" includes or how specialty data maps to C-CDA sections.

The documentation is functional for its g(10) purpose but inadequate as b(10) EHI export documentation. A patient or third party requesting their complete health information from an EndoVault system would receive a clinical summary but would be missing their endoscopy images, procedure reports with detailed findings, and any oncology treatment records — data that is clearly part of the designated record set and used for clinical decision-making.

An additional operational concern: the "here" link on the primary EHI export page (`/ephi/`) points to `old.endosoft.com/fhir/` which is completely broken (SSL cert error + 502 gateway). A user following the documented path would hit a dead end. The working FHIR page exists at `www.endosoft.com/fhir/` but the EHI page hasn't been updated to point there.

## Access Summary
- Final URL (after redirects): https://www.endosoft.com/ephi/
- Status: found
- Required browser: no (curl works fine)
- Navigation complexity: one_click (main page + one link to FHIR page/PDF)
- Anti-bot issues: none

## Obstacles & Dead Ends

1. **Broken FHIR documentation link**: The EHI page links to `https://old.endosoft.com/fhir/#_Toc120735483` which returns SSL certificate error and 502 Bad Gateway. No Wayback Machine snapshots exist. The equivalent content is available at `https://www.endosoft.com/fhir/` (same domain, without "old" subdomain).

2. **No dedicated b(10) documentation**: There is no document specifically addressing the b(10) EHI export requirement. The PDF is explicitly a g(10) FHIR API document. The EHI page provides only a brief overview without technical depth.
