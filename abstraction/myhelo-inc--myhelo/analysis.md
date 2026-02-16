# EHI Export Analysis: myhELO, Inc.

**Product**: myhELO
**Analysis date**: 2026-02-15
**CHPL IDs**: 9930 (CHPL Product Number: 15.05.05.2637.MOXE.01.00.1.190305)

## 1. Product Context

myhELO is a cloud-based, all-in-one healthcare platform developed by myhELO, Inc. (Fishers, Indiana, ~11–16 employees). The company brands its product a "Healthcare Operating System" targeting **outpatient specialty practices and ambulatory surgery centers (ASCs)**, with a particular focus on **orthopedic practices**.

The product integrates the following modules into a single platform:

- **EMR / Clinical Documentation**: Charting with manual, dictation, and automated note generation; customizable surgical templates for orthopedic procedures; medical image viewing/storage/sharing; pre-op/post-op workflows
- **E-Prescribing**: Nationwide pharmacy access, automated renewals, prior authorizations
- **Revenue Cycle Management (RCM)**: AI-powered coding, built-in clearinghouse, claims submission, advance benefit verification, point-of-service payment collection, digital patient billing, denial prevention, financial dashboards
- **Scheduling / Practice Management**: Multi-device scheduling, OR resource management, automated appointment confirmations/reminders
- **Patient Portal / Engagement**: Secure messaging, digital intake forms, patient-reported outcomes, family record management, online payment
- **Telehealth**: HIPAA-compliant video visits, screen sharing, messaging threads
- **Reporting & Analytics**: Dynamic reporting, RCM analytics

The product is broadly certified across 35+ ONC criteria including (b)(10) EHI export, (g)(7)/(g)(9)/(g)(10) FHIR APIs, clinical criteria (a)(1)–(a)(13), transitions of care (b)(1)–(b)(3), and public health reporting.

**Baseline for export completeness**: A genuine EHI export from myhELO should cover clinical documentation, medications, labs, procedures, **plus** billing/claims, insurance coverage, scheduling, patient portal communications, e-prescribing details, patient-reported outcomes, and orthopedic-specific surgical templates/data.

## 2. Artifacts Reviewed

| Artifact | Location | Description | Informative? |
|---|---|---|---|
| **Main page HTML** | `downloads/main-page.html` (3.3 KB) | Rendered HTML of the EHI export data dictionary landing page at `myhelo.com/api_export_format/`. Lists 17 datasets with links. | ✅ High — confirms dataset listing |
| **Main page screenshot** | `downloads/main-page-screenshot.png` (2.9 MB) | Browser screenshot of the EHI export page. Confirms 17 datasets, title "Data Dictionary for myhELO EHI Export", subtitle "Ambulatory Clinical EHI Export" | ✅ High — visual confirmation |
| **AllergyIntolerance dataset page** | `downloads/datasets/AllergyIntolerance.html` (107 KB, SPA shell) + `AllergyIntolerance-screenshot.png` (2.9 MB) | HTML is an unrendered SPA shell. Screenshot shows detailed FHIR R4 structure definition with field-level definitions, cardinality, types, value set bindings. Content is standard FHIR spec, not vendor-specific. | ⚠️ Medium — screenshot shows standard FHIR definitions |
| **CarePlan, CareTeam dataset pages** | `downloads/datasets/CarePlan.html`, `CareTeam.html` (107 KB each) | SPA shells identical to AllergyIntolerance.html — no rendered content captured | ❌ Low — no usable content |
| **FHIR CapabilityStatement** | `downloads/fhir-metadata.json` (6.4 KB) | Machine-readable FHIR CapabilityStatement from `provider.myhelo.com/fhir/metadata`. Lists 18 resource types, SMART-on-FHIR security, Group/$export bulk operation. Software version 3.14, released 2022-12-15. | ✅ High — definitive resource listing |
| **FHIR well-known spec** | `downloads/fhir-well-known.json` (99 KB) | Machine-readable API spec from `provider.myhelo.com/fhir/.well-known/fhir.json`. Contains example FHIR JSON responses for 17 of 18 resources, search parameters, and endpoint definitions. | ✅ High — example data for all resources |
| **API docs page** | `downloads/api-docs.html` (70 KB) | Rendered API documentation page from `myhelo.com/api/`. Contains introduction, API access instructions, terms, and full API reference with example responses for each resource type. Same content as the well-known JSON. | ⚠️ Medium — duplicates well-known |
| **Enrichment data dictionary** | `downloads/enrichment/ehi-export-data-dictionary.json` (2.4K lines) | Extracted data dictionary combining CapabilityStatement, well-known, and dataset pages. 19 resources, 119 fields — but 0 fields have descriptions populated. | ⚠️ Medium — field names/types only |
| **CHPL metadata** | `chpl-metadata.json` | Certification details: 35+ criteria certified, including (b)(10) and (g)(10) | ✅ High — certification context |

**Most informative artifacts**: `fhir-metadata.json` (CapabilityStatement), `fhir-well-known.json` (example data), `main-page.html` (dataset listing). These three machine-readable files contain essentially all available information about the export.

**Least informative**: The dataset HTML pages (`downloads/datasets/*.html`) are SPA shells with no rendered content. The screenshot of AllergyIntolerance shows it contains standard FHIR R4 structure definitions — the same content available in the FHIR specification itself, not vendor-specific documentation.

## 3. Export Mechanics

- **Format**: FHIR R4 JSON
- **Mechanism**: FHIR REST API at `https://provider.myhelo.com/fhir` with SMART-on-FHIR OAuth2 authentication. The introduction states customers can "easily export clinical or healthcare data from patient records." No UI export button or download mechanism is documented — the export appears to be API-only.
- **Single-patient vs. bulk**: Both. Individual resource read/search endpoints support per-patient queries. The Group/$export operation (Bulk Data Access) enables multi-patient/all-patient export. The main page states: "Customers can choose to export all or selected myhELO EHI datasets for a single patient, multiple patients, or all patients in the practices."
- **Access constraints**: API access requires registration ("Access to the myhELO API can be requested by submitting a request on our contact page"). SMART-on-FHIR OAuth2 with authorize/token/revoke endpoints.
- **Fees**: Not mentioned in available documentation.

## 4. Export Content: What's In It

### Data Dictionary Assessment

The EHI export data dictionary is structured as follows:

- **Main page**: Lists 17 FHIR R4 resource types (datasets) with links to individual specification pages
- **Dataset pages**: Each page shows a FHIR R4 structure definition with field-level elements, cardinality, types, value set bindings, and detailed per-field descriptions. Based on the AllergyIntolerance screenshot, these are **standard FHIR R4 resource definitions** — the descriptions, constraints, and bindings come from the FHIR specification, not from vendor-specific documentation.
- **Example data**: The well-known JSON provides example FHIR responses for 17 resources with realistic test data (patient "Bob Fhir", practitioner "Joe Provider", organization in Indianapolis, IN).
- **Machine-readable schema**: The CapabilityStatement documents supported resources, interactions, and search parameters.

**Field-level analysis from example data** (119 fields total across 19 resources):
- Fields with descriptions: **0 of 119** (0%) — descriptions exist in the browser-rendered dataset pages but are standard FHIR spec text, not in any downloadable/parseable format
- Fields with types: **119 of 119** (100%) — inferred from example data
- Fields with example values: **79 of 119** (66%)
- Fields marked USCDI: **57** (from the enrichment extraction, based on dataset page tagging)

### Vendor's own content organization

The vendor organizes the export as 17 "datasets," each corresponding to a FHIR R4 resource type. There are no vendor-specific categories, no grouping beyond the flat resource list.

| Resource Type | Example Fields | Has Example | Search Params | Category |
|---|---|---|---|---|
| AllergyIntolerance | 6 | ✅ | 3 | Clinical |
| CarePlan | 6 | ✅ | 5 | Clinical |
| CareTeam | 4 | ✅ | 5 | Clinical |
| Condition | 6 | ✅ | 3 | Clinical |
| Device | 9 | ✅ | 3 | Clinical |
| DiagnosticReport | 10 | ✅ | 6 | Clinical |
| DocumentReference | 11 | ✅ | 7 | Clinical |
| Encounter | 13 | ✅ | 4 | Clinical |
| Goal | 5 | ✅ | 3 | Clinical |
| Immunization | 7 | ✅ | 3 | Clinical |
| MedicationRequest | 9 | ✅ | 5 | Clinical |
| Observation | 7 | ✅ | 6 | Clinical |
| Organization | 0 | ❌ | 2 | Infrastructure |
| Patient | 9 | ✅ | 6 | Demographics |
| Practitioner | 5 | ✅ | 4 | Infrastructure |
| Procedure | 5 | ✅ | 4 | Clinical |
| Provenance | 4 | ✅ | 1 | Infrastructure |

Additionally, the CapabilityStatement includes **Group** (for bulk export operations) and the well-known JSON includes **Location** (with 3 example fields) — neither is listed in the EHI export data dictionary.

**Notable observations**:
- Organization has no example data and 0 fields in the well-known JSON
- The field counts are from example responses only and represent minimum populated fields; the actual FHIR resource definitions have many more possible fields
- No vendor-specific extensions, custom profiles, or additional elements beyond standard FHIR R4 are documented anywhere

The complete entity inventory is saved to `analysis/full-entity-inventory.json`.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor covers standard USCDI clinical data across 17 FHIR R4 resource types. There is no vendor-specific categorization — the export is simply the US Core resource set:

- **Clinical observations & results**: Observation (vitals, labs, social history), DiagnosticReport (lab/radiology reports with PDF attachments), DocumentReference (clinical notes as PDFs)
- **Problems & history**: Condition, AllergyIntolerance, Immunization
- **Treatments & orders**: MedicationRequest, Procedure, CarePlan, Goal, Device (implantable)
- **Visit records**: Encounter (with type, period, participants, location, reason codes)
- **Care coordination**: CareTeam, Provenance
- **Demographics**: Patient (with US Core extensions for race, ethnicity, birth sex)
- **Directory**: Organization, Practitioner

The example data shows appropriate use of standard code systems (SNOMED CT, LOINC, CPT, CVX, ICD) and inter-resource references (e.g., Encounter→Patient, MedicationRequest→Practitioner). Clinical notes and diagnostic reports include base64-encoded PDF attachments.

**What's absent from the vendor's export**: There are no vendor-specific resources, extensions, or custom data structures. The export contains zero data elements that go beyond what the standard FHIR US Core profiles define. For a product with integrated RCM, scheduling, patient portal, telehealth, and orthopedic-specific features, this is notable.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | Patient resource (9 example fields incl. name, DOB, gender, address, telecom, race, ethnicity, birth sex) | Adequate for clinical demographics |
| Encounters / visits | ✅ Covered | Encounter resource (13 example fields incl. class, type, period, participants, location, reason) | Adequate |
| Problems / conditions | ✅ Covered | Condition resource (6 example fields with SNOMED coding, clinical/verification status) | Adequate |
| Medications / prescriptions | ⚠️ Partial | MedicationRequest (9 example fields with dosage, requester, status). No MedicationAdministration, no pharmacy fill status, no prior authorization records, no renewal histories | Product has e-prescribing with renewals and prior auth; export covers orders only |
| Allergies | ✅ Covered | AllergyIntolerance (6 example fields with reactions, severity, SNOMED coding) | Adequate |
| Immunizations | ✅ Covered | Immunization (7 example fields with CVX vaccine codes, dates, status) | Adequate |
| Vitals | ✅ Covered | Observation resource (covers vitals, labs, social history via category filtering) | Adequate |
| Lab results | ✅ Covered | Observation + DiagnosticReport (with PDF attachments) | Adequate |
| Imaging / diagnostic reports | ⚠️ Partial | DiagnosticReport includes radiology reports with PDF attachments. No DICOM/image data despite product's built-in medical image viewing/storage/sharing | Product stores and shares medical images; PDF-only export loses image data |
| Procedures | ✅ Covered | Procedure (5 example fields with CPT coding) | Basic coverage; no surgical template details |
| Clinical notes / documents | ✅ Covered | DocumentReference (clinical notes as base64 PDF) | Notes exported as PDFs, not structured data |
| Care plans / goals | ✅ Covered | CarePlan + Goal resources | Adequate |
| Orders / referrals | ⚠️ Partial | MedicationRequest covers medication orders. No ServiceRequest for lab/imaging orders or referrals despite CPOE certification (a)(1)–(a)(3) | Product supports CPOE for drugs, labs, imaging, referrals; only medication orders exported |
| Insurance / coverage | ❌ Not covered | No Coverage or InsurancePlan resource | Product has advance benefit verification and insurance details; **significant gap** |
| Claims / billing | ❌ Not covered | No Claim, ClaimResponse, or ExplanationOfBenefit resource | Product has full RCM with AI coding, clearinghouse, claims, denial management; **major gap** |
| Payments | ❌ Not covered | No payment-related resources | Product has point-of-service collection, digital billing, payment arrangements; **significant gap** |
| Consents / directives | ❌ Not covered | No Consent resource | N/A — unclear if product stores structured consent data |
| Patient communications / portal messages | ❌ Not covered | No Communication resource | Product has secure messaging, intake forms, patient-reported outcomes; **significant gap** |
| Specialty-specific (orthopedic) | ❌ Not covered | No custom profiles, extensions, or specialty-specific resources | Product emphasizes customizable surgical templates, pre-op/post-op workflows, OR scheduling; **major gap** for a product targeting orthopedic ASCs |

**Summary**: 8 of 18 applicable domains have adequate coverage, 3 have partial coverage, and 7 are not covered at all. The uncovered domains include the product's most distinctive features: RCM, scheduling, patient engagement, and orthopedic specialty data.

## 6. Documentation Quality

**Strengths**:
- Clean, organized landing page with a clear list of 17 datasets
- Machine-readable CapabilityStatement and API specification (well-known JSON) are available and current (verified live on 2026-02-15)
- Example FHIR JSON responses are provided for 17 of 18 resources with realistic test data
- SMART-on-FHIR OAuth2 authentication endpoints are documented
- Dataset pages (browser-rendered) include standard FHIR R4 element definitions with cardinality, types, and value set bindings

**Weaknesses**:
- **No vendor-specific documentation**: The dataset pages contain standard FHIR R4 structure definitions — the same content available at hl7.org/fhir. There is no vendor-specific mapping explaining how myhELO's internal data maps to these FHIR resources.
- **SPA-only rendering**: All pages require JavaScript to render; HTML source is an empty `<body>` tag. This means the data dictionary is not accessible to screen readers, crawlers, or simple HTTP clients. The downloaded HTML files contain no content.
- **No downloadable artifacts**: No PDF, ZIP, CSV, schema files, or sample export files are available for download
- **No export process documentation**: How does a user initiate an EHI export? What UI is involved? What does the output look like? None of this is documented.
- **0% vendor-specific field descriptions**: While the browser-rendered pages show field descriptions, these are standard FHIR definitions, not vendor-specific explanations of how myhELO populates each field
- **No relationship documentation beyond FHIR references**: No vendor-specific data model or entity-relationship documentation
- **No documentation of what's excluded**: The export documentation doesn't explain why billing, scheduling, patient portal, or specialty data are absent

**Could a developer build an import?** A developer familiar with FHIR R4 and US Core could consume this export, but they would learn nothing vendor-specific from the documentation — the examples and CapabilityStatement provide the only practical guidance. The 70KB of API documentation adds no information beyond what any FHIR R4 US Core server provides.

## 7. Overall Assessment

### Classification

**Standard-based projection**

The myhELO EHI export is the vendor's g(10) FHIR API repackaged as b(10) EHI export documentation. The evidence for this conclusion is strong and multi-faceted:

1. The 17 EHI export datasets are **exactly** the 17 US Core R4 resource types — a verified exact match (`analysis/verification-report.json`)
2. The CapabilityStatement shows the same FHIR server with Group/$export (Bulk Data Access — the g(10) mechanism)
3. SMART-on-FHIR OAuth2 authentication (the g(10) authentication mechanism)
4. No custom profiles, extensions, or vendor-specific resources anywhere in the documentation
5. The API Docs page (`/api/`) documents the same endpoints as the EHI export page (`/api_export_format/`)
6. Zero billing, financial, scheduling, patient portal, or specialty resources despite the product having full modules for each
7. No native database model or vendor-specific data structures — only standard FHIR resources

### Key Findings

1. **g(10) FHIR API repackaged as b(10)**: The 17 EHI export resource types are a verified exact match to the US Core R4 resource set. The same FHIR server, endpoints, and authentication mechanism serve both g(10) API access and what the vendor calls the EHI export. This is the textbook example of FHIR repackaging. (Evidence: `fhir-metadata.json`, `main-page.html`, `verification-report.json`)

2. **Major billing/RCM gap**: myhELO has a full Revenue Cycle Management module with AI-powered coding, built-in clearinghouse, claims submission, denial management, digital patient billing, and financial dashboards — none of which appears in the export. Zero billing-related FHIR resources (no Claim, Coverage, ExplanationOfBenefit, Account). (Evidence: `product-research.md` RCM section; `fhir-metadata.json` resource list)

3. **Major specialty data gap**: The product specifically targets orthopedic practices and ASCs, emphasizing customizable surgical templates, OR scheduling, and pre-op/post-op workflows. None of this specialty-specific clinical data appears in the export. Procedures are exported with basic CPT codes only. (Evidence: `product-research.md` orthopedic focus; Procedure example in `fhir-well-known.json` shows only 5 fields)

4. **Patient engagement data absent**: Despite having a patient portal with secure messaging, digital intake forms, patient-reported outcomes, and family record management, none of this data appears in the export. (Evidence: `product-research.md` patient engagement section; no Communication or QuestionnaireResponse resources)

5. **Documentation quality is thin**: While the API is well-structured and machine-readable artifacts exist, the EHI export "data dictionary" is simply standard FHIR spec content, not vendor-specific documentation. 0 of 119 fields have vendor-specific descriptions. No sample export files, no data model documentation, no mapping guide. (Evidence: `enrichment/ehi-export-data-dictionary.json` — 0 descriptions; dataset screenshots show standard FHIR definitions)

### Summary Stats

```
Classification:  Standard-based projection
Export format:   FHIR R4 JSON
Model type:      Standard projection (US Core R4)
Entities:        17 (EHI export) / 19 (total with Group + Location)
Fields:          119 (from example data; standard FHIR definitions have more)
Descriptions:    0% vendor-specific (dataset pages show standard FHIR descriptions)
Sample data:     Yes (example FHIR JSON responses in well-known spec)
Bulk export:     Yes (Group/$export via Bulk Data Access)
Domains covered: 8 of 18 applicable domains (3 partial, 7 not covered)
```

### Bottom Line

myhELO's EHI export is its g(10) FHIR API relabeled as b(10) — it covers the USCDI clinical data subset (~17 US Core resources) but omits the product's most distinctive capabilities: revenue cycle management, orthopedic surgical templates, patient portal communications, scheduling, and insurance data. For a product that bills itself as a "Healthcare Operating System" replacing six separate tools, exporting only the standardized clinical fraction represents a significant gap. A patient or provider requesting their complete record would receive clinical summaries but miss billing records, specialty surgical data, patient-reported outcomes, and portal communications.
