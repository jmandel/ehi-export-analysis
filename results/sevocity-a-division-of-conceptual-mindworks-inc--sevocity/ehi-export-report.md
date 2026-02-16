# Sevocity, a division of Conceptual MindWorks, Inc. — EHI Export Documentation

Collected: 2026-02-16

## Source
- Registered URL: https://www.sevocity.com/ehi-export-technical-documentation/
- CHPL IDs: 11187
- Product: Sevocity v13.0
- Certification date: 2022-12-30

## Navigation Journal

### Step 1: Probe the registered URL

```bash
curl -sI -L "https://www.sevocity.com/ehi-export-technical-documentation/" \
  -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
```

Result: HTTP 200, `content-type: text/html; charset=UTF-8`. WordPress site hosted on WP Engine behind Cloudflare. No redirects.

### Step 2: Fetch and examine the page

```bash
curl -sL "https://www.sevocity.com/ehi-export-technical-documentation/" \
  -H 'User-Agent: Mozilla/5.0' \
  -o downloads/ehi-export-technical-documentation.html
```

The page is a single static HTML page with a table describing the EHI export format. The content is fully rendered in the HTML (no JavaScript-dependent content). The page contains one important outbound link to the FHIR API documentation: `https://fhirapi-docs.sevocity.com/`.

### Step 3: Follow the FHIR API Documentation link

```bash
curl -sL "https://fhirapi-docs.sevocity.com/" -o /tmp/fhirapi-docs.html
```

The FHIR API docs site is a Swagger UI (OpenAPI viewer) that loads `openAPIDocs.yml`. The initializer script (`swagger-initializer.js`) points to `./openAPIDocs.yml`.

### Step 4: Download the OpenAPI specification

```bash
curl -sL "https://fhirapi-docs.sevocity.com/openAPIDocs.yml" \
  -o downloads/openAPIDocs.yml
```

The main spec (9.3 KB) is an OpenAPI 3.0.1 document with `$ref` references to 130+ individual YAML files in `paths/`, `components/schemas/`, `components/parameters/`, and `examples/` directories.

### Step 5: Download all referenced YAML files

Extracted all `$ref` paths from the main spec and all path files, then downloaded each one:

```bash
# For each referenced file path:
curl -sL "https://fhirapi-docs.sevocity.com/${path}" \
  -o "downloads/fhir-api-docs/${path}"
```

Successfully downloaded 132 files total: 52 schema files, 52 path files, 26 example files, plus 2 parameter definitions. Zero failures.

### Step 6: Screenshots

Took full-page screenshots of both the main EHI export documentation page and the Swagger UI FHIR API docs page using browser automation.

## What Was Found

Sevocity's EHI export documentation consists of two components:

### 1. EHI Export Format Description (main page)

The main page at the registered URL describes the structure of the EHI export package. The export is delivered as an **encrypted RAR file** with the following folder structure:

| Path | Description |
|------|-------------|
| `/{Customer ID}/README.txt` | Contains the documentation URL (points back to this page) |
| `/{Customer ID}/DocumentData/{Patient ID}/` | All document and image data (PDFs, JPEGs, PNGs). Contains `summary.pdf` (chart summary) plus subfolders for document types: "admissions", "finalizedencounters", "referrals", etc. |
| `/{Customer ID}/Resources/` | FHIR resources in NDJSON format. DocumentReference resources with `type.coding.code` of "11503-0" have `content.attachment.url` pointing to files in the DocumentData folder. |
| `/{Customer ID}/PatientsDemographics.csv` | CSV file with all patient demographics |

The Patient ID is an internal value; the PatientsDemographics.csv file maps patients to their IDs.

### 2. Sevocity FHIR API Documentation (Swagger UI)

The FHIR API docs at `fhirapi-docs.sevocity.com` are a comprehensive OpenAPI 3.0.1 specification documenting 25 FHIR resource types with:

- **Read and Search operations** for each resource type
- **Detailed JSON schemas** for every resource (read variant and search/Bundle variant)
- **Example instances** for all 25 resource types, with realistic sample data
- **Group/$export endpoint** for FHIR Bulk Data export
- **CapabilityStatement** (metadata) example showing all supported resources

The API documentation explicitly distinguishes certified (g)(10) resources (marked with `*`) from non-certified resources. The API serves FHIR R4 resources conformant to US Core STU6.1.0.

**FHIR Resource Types in the Export:**

Certified (g)(10) — 19 resource types:
AllergyIntolerance, CarePlan, CareTeam, Condition, Coverage, Device, DiagnosticReport, DocumentReference, Encounter, Endpoint, Goal, Immunization, Location, Medication, MedicationDispense, MedicationRequest, Observation, Organization, Patient, Practitioner, Procedure, Provenance

Non-certified additions — 6 resource types:
Appointment, MedicationStatement, Questionnaire, QuestionnaireResponse, RelatedPerson, ServiceRequest

## Export Coverage Assessment

### Data Domain Coverage

The EHI export uses a hybrid approach: FHIR NDJSON resources plus a file-based document export with a CSV demographics file. This is genuinely more than just a (g)(10) FHIR API repackage — Sevocity has done real work to go beyond the standard API:

**Clearly covered:**
- **Demographics** — Patient resource (64 fields) with US Core extensions for race, ethnicity, birthsex, sex, gender identity, and tribal affiliation. Plus a CSV demographics file.
- **Problems/conditions** — Condition resource with ICD-10-CM coding
- **Medications** — MedicationRequest, MedicationStatement, MedicationDispense, and Medication resources (covering prescriptions, active meds, dispensing)
- **Allergies** — AllergyIntolerance resource
- **Lab results** — DiagnosticReport and Observation resources
- **Vital signs** — Observation resource (covers vitals via LOINC codes)
- **Immunizations** — Immunization resource
- **Procedures** — Procedure resource
- **Encounters/visits** — Encounter resource (45 fields including diagnoses, participants, locations)
- **Care plans and goals** — CarePlan and Goal resources
- **Care teams** — CareTeam resource
- **Referrals/orders** — ServiceRequest resource (non-certified addition covering lab and diagnostic orders with CPT/HCPCS/SNOMED coding and ICD-10-CM reason codes)
- **Insurance/coverage** — Coverage resource with member numbers, payer references, plan details
- **Documents/images** — DocumentReference resources plus raw files (PDFs, JPEGs, PNGs) in DocumentData folders, organized by patient with subfolders for document types
- **Clinical assessments** — QuestionnaireResponse resource — the example shows a Zung Self-Rating Depression Scale with 20 scored items, indicating Sevocity exports structured screening tool responses
- **Questionnaires** — Questionnaire resource providing the templates/definitions for assessments
- **Appointments** — Appointment resource (non-certified addition)
- **Related persons/contacts** — RelatedPerson resource for emergency contacts and guarantors
- **Provenance** — Provenance resource for data provenance tracking
- **Organizations** — Organization resource
- **Practitioners** — Practitioner resource
- **Locations** — Location resource

**Notable strengths beyond (g)(10):**
- The `DocumentData/` folder structure exports raw documents (PDFs, images) organized by patient, including chart summaries, finalized encounters, admissions documents, and referrals — this is data that FHIR alone cannot fully represent
- QuestionnaireResponse captures structured clinical assessments (depression scales, etc.) which are specialty-specific clinical data that most FHIR-only exports miss
- Appointment and ServiceRequest are non-certified resources that add scheduling and order data
- MedicationStatement adds historical medication use beyond just prescriptions

**Potentially missing or unclear:**
- **Billing data** — Coverage (insurance) is present, but there are no Claim, ExplanationOfBenefit, or ChargeItem resources. Sevocity Premier includes integrated billing, so for those customers, detailed billing records (claims, charges, payments, ERAs) may not be fully captured in the FHIR export. The documentation does not mention billing exports beyond insurance coverage.
- **Clinical notes/narrative text** — The DocumentData folder likely contains these as PDFs, but the FHIR resources don't include a specific note-text resource. Clinical notes may be embedded in DocumentReference resources or in the `summary.pdf` files.
- **E-prescribing details** — While MedicationRequest captures prescriptions, EPCS-specific data (controlled substance schedules, digital signatures) isn't explicitly documented.
- **PatientsDemographics.csv schema** — The CSV file is mentioned but its exact column structure is not documented. Only described as "all patient demographics."
- **Custom specialty template data** — Sevocity supports 40+ specialties with customizable templates. It's unclear whether specialty-specific charting fields (beyond what QuestionnaireResponse covers) are fully captured.

### Export Format & Standards

The export uses a thoughtful hybrid format:

1. **FHIR R4 NDJSON** — Machine-readable structured clinical data conformant to US Core STU6.1.0 profiles. Resources are in the `Resources/` folder.
2. **Raw document files** — PDFs, images (JPEG, PNG) in `DocumentData/` organized by patient ID and document type. This is critical because many clinical documents (scanned records, chart summaries, referral letters) cannot be adequately represented as pure FHIR resources.
3. **CSV demographics file** — Maps patients to internal IDs and provides demographic data in a simple tabular format.
4. **Encrypted RAR archive** — The entire export is delivered as an encrypted RAR file, providing transport-level security for PHI.

The FHIR resources use standard code systems (ICD-10-CM, SNOMED CT, LOINC, CPT, HCPCS, RxNorm via NDC) and reference each other via standard FHIR references. DocumentReference resources with LOINC code "11503-0" (Medical records) link to the physical files in DocumentData via relative URLs.

A third party could reconstruct a patient's clinical record from this export, given the FHIR resources for structured data and the document files for unstructured content. The PatientsDemographics.csv bridges the internal patient IDs used in folder names to patient identifiers.

### Documentation Quality

**Strengths:**
- The OpenAPI spec is comprehensive — 25 resource types with detailed JSON schemas, search parameters, and example instances for every resource
- Examples use realistic test data (San Antonio addresses, clinical codes, structured assessment responses)
- The Swagger UI presentation is interactive and navigable
- The main EHI export page clearly explains the RAR file structure and how FHIR resources relate to document files
- Clear distinction between (g)(10) certified and additional resources

**Weaknesses:**
- The PatientsDemographics.csv file format is not documented — no column headers, data types, or example provided
- No documentation of the NDJSON file naming conventions or how many NDJSON files are in the Resources folder
- No user guide for requesting or performing the export — no instructions on how to trigger the export, who can request it, or the expected turnaround time
- The main documentation page is minimal (one table) — the heavy lifting is delegated to the FHIR API docs
- No description of how the export handles large datasets, pagination, or incremental exports
- The "encrypted rar file" delivery mechanism lacks details — encryption algorithm, key distribution, file size limits

### Structure & Completeness

**Schema granularity:** Field-level documentation is strong. The OpenAPI schemas define every field with JSON types. The Patient resource alone has 64 nested fields including US Core extensions. However, the schemas are structural (type information) without semantic descriptions — fields like `status` are typed as `string` but don't enumerate valid values.

**Value sets:** Not explicitly documented. Coded fields (e.g., Condition.code, AllergyIntolerance.clinicalStatus) use `type: string` without binding to FHIR value sets. However, the examples demonstrate use of standard code systems (ICD-10-CM, SNOMED CT, LOINC), so practitioners familiar with FHIR US Core would understand the expected value sets.

**Relationships:** FHIR references between resources are documented in the schemas (e.g., Encounter.subject.reference → Patient, ServiceRequest.encounter.reference → Encounter). The DocumentReference→DocumentData linkage via LOINC code 11503-0 is explicitly called out on the main page.

**Versioning:** The OpenAPI spec lists version 1.0.0 with US Core STU6.1.0 as the external docs reference. The main page was last modified 2024-05-14 (per page metadata). No formal change history.

## Access Summary
- Final URL (after redirects): https://www.sevocity.com/ehi-export-technical-documentation/
- Status: found
- Required browser: no (all content accessible via curl; Swagger UI for interactive browsing but underlying YAML files are directly downloadable)
- Navigation complexity: one_click (main page → FHIR API docs link)
- Anti-bot issues: none (Cloudflare present but did not block automated access)

## Obstacles & Dead Ends

None. Both the main documentation page and the FHIR API documentation site were fully accessible without authentication, CAPTCHA, or JavaScript requirements. All 132 OpenAPI YAML files were successfully downloaded with simple curl requests.
