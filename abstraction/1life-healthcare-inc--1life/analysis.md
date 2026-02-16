# EHI Export Analysis: 1Life Healthcare, Inc (One Medical)

**Product**: 1Life v1.0
**Analysis date**: 2026-02-16
**CHPL IDs**: 15.05.05.3121.ONEL.01.00.1.220823

## 1. Product Context

One Medical (operated by 1Life Healthcare, Inc, acquired by Amazon in 2023) is a membership-based primary care practice operating 125+ offices across 19+ U.S. cities. The company built its own proprietary EHR, **1Life**, from the ground up — it is not a third-party EHR sold to external practices but the internal technology platform powering all One Medical operations.

1Life stores and manages:
- **Clinical data**: Patient demographics, encounter notes, problem lists, medication lists, allergies, immunizations, vital signs, lab orders/results, family health history, implantable devices, clinical notes, care plans
- **Communication data**: Patient-provider secure messages, provider-to-provider messages, administrative messages
- **Prescriptions**: Electronic prescribing via SureScripts integration
- **Care coordination**: Referrals, chronic care management (Impact by One Medical), care team assignments
- **Administrative/billing**: Insurance verification, billing (accepts most major carriers and Medicare), membership management
- **Virtual care**: Video visit records, on-demand "Treat Me Now" visits, photo attachments
- **Patient-generated data**: Prescription renewal requests, referral requests, health screening questionnaire responses

Key for export assessment: One Medical bills insurance directly for clinical visits, so claims/billing data exists. They also have extensive messaging, virtual care, and chronic care management features that generate patient-specific data.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `ehi-export-overview.html` (37 KB) | Core EHI export page listing 16 unique FHIR resource types and 18 C-CDA sections | **High** — defines the export scope |
| `fhir/resources/*.html` (22 files, ~1.2 MB total) | Individual FHIR resource documentation pages with field-level tables | **High** — the detailed schema documentation |
| `enrichment/fhir-resources.json` (158 KB) | Pre-extracted structured JSON of all 22 FHIR resources, 629 fields | **High** — machine-readable parse of the field tables |
| `enrichment/ehi-export-summary.json` (12 KB) | Combined extraction: EHI format, C-CDA sections, 11 extensions, 3 terminology codes | **High** — structured summary |
| `fhir/extensions.html` (70 KB) | Documentation of 11 FHIR extensions including ML model extensions | **Medium** — shows vendor-specific customizations |
| `fhir/terminology.html` (39 KB) | 3 custom terminology codes (TOS consent, TMN messaging, AVS summaries) | **Medium** — shows custom data types |
| `ccda/patient-continuity-of-care-document.html` (37 KB) | C-CDA API endpoint documentation with sections and date filtering | **Medium** — documents alternative access path |
| `fhir/overview.html` (37 KB) | FHIR API overview with root URLs and media types | **Low** — infrastructure details |
| `fhir/authentication.html` (40 KB) | FHIR API authentication documentation | **Low** — access mechanics |
| `fhir/search-and-output.html`, `fhir/pagination.html`, `fhir/capability-statement.html` | FHIR API operational docs | **Low** — API usage, not export content |
| `homepage.html` (30 KB) | API documentation homepage | **Low** — navigation only |
| `screenshot-ehi-export-overview.png` (266 KB) | Full-page screenshot of EHI export page | **Low** — visual confirmation |
| `enrichment/extraction-report.json` (2 KB) | Extraction accounting (28 files parsed, 0 failures) | **Low** — process metadata |

No PDFs, ZIP files, sample data files, JSON schemas, or XLSX files were present. The entire documentation is HTML-only.

## 3. Export Mechanics

- **Format**: ZIP file containing two files per patient:
  1. `.json` — FHIR R4 Bundle with all resources for the patient
  2. `.xml` — C-CDA v2.1 Patient Continuity of Care Document
- **Mechanism**: The documentation does not describe how the export is triggered. No API endpoint, UI button, or process is documented for the (b)(10) EHI export itself. The C-CDA API endpoint (`GET https://production.app.1life.com/api/ccda`) is documented separately but is the C-CDA API, not the EHI export trigger.
- **Single-patient vs bulk**: The overview states the export covers "a single patient or multiple patients."
- **Access constraints**: Unknown — no documentation on who can trigger the export, what authentication is required, or whether there are fees.

## 4. Export Content: What's In It

### FHIR JSON Bundle

The EHI export overview page lists **16 unique FHIR resource types** (the page lists 17 rows but "Condition" appears twice — a documentation error). These are described as resource types that "may be included" in the FHIR bundle:

AllergyIntolerance, CareTeam, Communication, Condition, Consent, Device, DiagnosticReport, DocumentReference, Encounter, Goal, Immunization, MedicationRequest, Observation, Patient, Procedure, ServiceRequest.

The FHIR documentation site provides detailed field-level documentation for **22 resource types** with **629 total fields**. Of these 22, the 6 additional resources not listed on the EHI export page (CarePlan, Coverage, Location, Medication, Organization, Practitioner, Provenance, Questionnaire, QuestionnaireResponse) are likely included as referenced/supporting resources within the FHIR bundle.

Three resources listed on the EHI export page have **no individual documentation pages**: Communication, Consent, and Goal. Their field structure is not documented beyond being listed as included.

### Documentation quality per field

- **629 fields** documented across 22 resource types
- **628 fields (99.8%)** have descriptions
- **582 fields (92.5%)** have explicit types
- All fields have cardinality specified
- No value set documentation beyond 3 custom terminology codes
- No sample data or example FHIR bundles provided

### C-CDA XML Document

The C-CDA component contains **18 sections**: Allergies, Assessment and Plan, Care Team, Encounters, Family History, Goals, Health Concerns, Immunizations, Medical Equipment, Medications, Notes, Patient, Plan of Treatment, Problems, Procedures, Results, Social History, Vital Signs.

Some sections support date range filtering; others always return all data.

### Vendor's own content organization

The vendor organizes resources by FHIR resource type, not by clinical domain. The table below shows all 22 documented resources with field counts:

| Resource Type | Fields | Described | Types | In EHI Export List |
|---|---|---|---|---|
| Patient | 60 | 60 | 58 | ✓ |
| Observation | 48 | 47 | 43 | ✓ |
| DocumentReference | 42 | 42 | 40 | ✓ |
| Immunization | 36 | 36 | 34 | ✓ |
| DiagnosticReport | 35 | 35 | 33 | ✓ |
| Procedure | 34 | 34 | 32 | ✓ |
| Encounter | 33 | 33 | 31 | ✓ |
| Questionnaire | 31 | 31 | 29 | (supporting) |
| Coverage | 31 | 31 | 29 | (supporting) |
| ServiceRequest | 30 | 30 | 28 | ✓ |
| AllergyIntolerance | 27 | 27 | 25 | ✓ |
| CareTeam | 26 | 26 | 24 | ✓ |
| Location | 26 | 26 | 24 | (supporting) |
| CarePlan | 24 | 24 | 22 | (supporting) |
| QuestionnaireResponse | 23 | 23 | 21 | (supporting) |
| Condition | 23 | 23 | 21 | ✓ |
| MedicationRequest | 21 | 21 | 19 | ✓ |
| Practitioner | 19 | 19 | 17 | (supporting) |
| Organization | 18 | 18 | 16 | (supporting) |
| Provenance | 17 | 17 | 15 | (supporting) |
| Medication | 13 | 13 | 11 | (supporting) |
| Device | 12 | 12 | 10 | ✓ |

Three additional resources are listed in the EHI export but have no documentation pages: **Communication**, **Consent**, **Goal**.

### FHIR Extensions

11 FHIR extensions are documented:
- **US Core Race/Ethnicity** (2): Standard extensions on Patient
- **Machine Learning extensions** (8): Source type, model name, model repository, model type, model use case, model performance, prediction characteristics — used on Observation and Procedure. Resources with these extensions are flagged as ML-generated and "should generally NOT be considered authoritative."
- **First Party Data** (1): Marks resources as representing interactions at One Medical vs. external care

### Custom Terminology

3 custom codes under `http://onemedical.com/terminology`:
- `Consent.TOS`: Terms of Service consent forms
- `Communication.TMN`: Treat Me Now secure message threads
- `Communication.AVS`: After Visit Summary post-encounter instructions

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The export covers standard clinical data domains well through FHIR R4 resources. The strongest areas are:

- **Demographics/Patient**: 60 fields including US Core Race/Ethnicity extensions — the most detailed resource
- **Clinical observations**: Observation (48 fields) covers vitals, labs, social history; DiagnosticReport (35 fields) covers lab reports
- **Clinical notes**: DocumentReference (42 fields) with attachment support
- **Encounters**: 33 fields including status, class, type, participants, location
- **Procedures and immunizations**: Well-documented at 34 and 36 fields respectively
- **Questionnaires**: Questionnaire (31 fields) and QuestionnaireResponse (23 fields) capture custom forms and screening assessments — a strength beyond typical FHIR exports

The inclusion of Communication (for secure messaging), Consent (for consent records), and Questionnaire/QuestionnaireResponse goes beyond the standard US Core/USCDI clinical summary scope, showing some effort to capture vendor-specific data.

However, the export operates entirely within the FHIR data model, which constrains what can be represented. Any data that doesn't map naturally to FHIR resources is absent.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | Patient (60 fields), US Core Race/Ethnicity extensions | Thorough |
| Encounters / visits | ✅ Covered | Encounter (33 fields), Location (26 fields) | Thorough; unclear if virtual vs. in-person visit types are distinguished |
| Problems / conditions / diagnoses | ✅ Covered | Condition (23 fields) with clinical/verification status, SNOMED codes | Adequate |
| Medications / prescriptions | ✅ Covered | MedicationRequest (21 fields), Medication (13 fields) | Adequate; SureScripts integration data may not fully surface |
| Allergies | ✅ Covered | AllergyIntolerance (27 fields) with reaction details | Thorough |
| Immunizations | ✅ Covered | Immunization (36 fields) including lot number, site, route | Thorough |
| Vitals | ✅ Covered | Observation (48 fields) covers vitals, labs, social history | Thorough |
| Lab results | ✅ Covered | DiagnosticReport (35 fields), Observation (48 fields) | Thorough |
| Imaging / diagnostic reports | ⚠️ Partial | DiagnosticReport could contain imaging reports, but One Medical is primary care with limited imaging | Likely N/A for most data; no PACS integration mentioned |
| Procedures | ✅ Covered | Procedure (34 fields) with ML extension support | Adequate |
| Clinical notes / documents | ✅ Covered | DocumentReference (42 fields) with attachment URLs; C-CDA Notes section | Adequate |
| Care plans / goals | ✅ Covered | CarePlan (24 fields), CareTeam (26 fields), Goal (listed in EHI but undocumented) | Adequate; chronic care management (Impact) plans should map here |
| Orders / referrals | ✅ Covered | ServiceRequest (30 fields) | Adequate |
| Insurance / coverage | ⚠️ Partial | Coverage (31 fields) is documented but NOT explicitly listed in EHI export. May be included as supporting resource. | Product bills insurance directly; Coverage resource exists in FHIR docs but its inclusion in the EHI bundle is ambiguous |
| Claims / billing | ❌ Not covered | No billing resources (Claim, ExplanationOfBenefit, ChargeItem) documented or listed | **Significant gap** — One Medical bills insurance for every visit; billing transaction records are EHI |
| Payments | ❌ Not covered | No payment resources documented | Gap — membership fees and copays are processed |
| Consents / directives | ✅ Covered | Consent listed in EHI export; TOS custom terminology code defined | Adequate, though Consent has no field-level documentation page |
| Patient communications / portal messages | ⚠️ Partial | Communication listed in EHI export with TMN and AVS terminology codes, but no field-level documentation | Communication is listed but undocumented; unclear what message content/metadata is included |
| Questionnaires / assessments | ✅ Covered | Questionnaire (31 fields), QuestionnaireResponse (23 fields) | Good — captures screening forms and custom assessments |
| Family health history | ⚠️ Partial | C-CDA Family History section present, but no FHIR FamilyMemberHistory resource | Only in C-CDA; no structured FHIR representation |

**Key gaps**:
1. **Billing/claims**: One Medical bills insurance for every clinical visit. Billing transaction records (charges, claims, EOBs) are part of the designated record set and are completely absent from the export.
2. **Patient messaging content**: Communication is listed but has no documentation page. The depth of what's exported (full message threads vs. metadata) is unknown.
3. **Family health history**: Only in C-CDA, not in the FHIR bundle, despite being a certified criterion ((a)(12)).

## 6. Documentation Quality

**Strengths**:
- The documentation is hosted on a well-organized static site (`apidocs.onemedical.io`) with clear navigation
- 629 fields across 22 FHIR resources with 99.8% description coverage — nearly every field has an explanation
- Field tables consistently include name, type, cardinality, and description
- Custom extensions and terminology are explicitly documented with JSON examples
- The ML extension documentation is notably transparent about how machine learning is used and that ML-generated data is flagged as non-authoritative

**Weaknesses**:
- **No sample data**: No example FHIR bundles, no sample C-CDA documents, no test exports. A developer would have to construct expected outputs entirely from the field tables.
- **No export trigger documentation**: The EHI export page describes the output format but says nothing about how to request or trigger an export. Is it a UI button? An API call? A support request?
- **Three undocumented resources**: Communication, Consent, and Goal are listed in the EHI export but have no field-level documentation pages.
- **No value set documentation**: Beyond the 3 custom terminology codes, no value set bindings are documented for coded fields (e.g., what encounter types, condition categories, or observation codes does One Medical use?).
- **No relationship diagrams**: FHIR references between resources are described in individual field descriptions but there's no overview of how resources relate.
- **Ambiguous supporting resource inclusion**: It's unclear whether the 9 documented-but-not-listed resources (Coverage, CarePlan, Questionnaire, etc.) are actually included in the EHI export bundle.

**Could a developer build an import?** Partially. The FHIR field tables are detailed enough to parse the JSON bundle for the 22 documented resources. However, without sample data, without knowing which value sets are used, and without documentation for 3 of the listed resources, there would be significant guesswork required.

## 7. Overall Assessment

### Classification

**Standard-based projection**

The EHI export is a FHIR R4 JSON Bundle + C-CDA v2.1 XML document. It is not a native database export — it projects 1Life's internal data model into standard FHIR resources. While the inclusion of non-US Core resources (Communication, Consent, Questionnaire/QuestionnaireResponse) and ML extensions shows effort beyond a bare-minimum FHIR API repackaging, the export is fundamentally constrained by what FHIR can represent.

One Medical built a proprietary EHR from scratch with its own data model (Rails/PostgreSQL based on the tech stack descriptions). The native database almost certainly contains dozens or hundreds of internal tables covering billing, messaging threads, care navigation tasks, membership management, virtual visit logistics, and custom clinical workflows. None of this internal structure is exposed — everything is flattened into 16–22 FHIR resource types.

### Key Findings

1. **FHIR-based projection, not a native export**: The EHI export is a FHIR R4 bundle — a standard-format projection of the vendor's internal data model. This covers standard clinical data well but inherently cannot represent vendor-specific operational and billing data. (`ehi-export-overview.html`)

2. **Good field-level documentation**: 629 fields across 22 FHIR resources with 99.8% description coverage. The documentation quality for what IS documented is high. (`enrichment/fhir-resources.json`)

3. **Billing data entirely absent**: One Medical bills insurance for every visit, but no billing resources (Claim, ExplanationOfBenefit, ChargeItem) are included. This is a significant EHI gap — billing records are explicitly part of the HIPAA designated record set. (`ehi-export-overview.html` — no billing resources listed)

4. **Three EHI resources undocumented**: Communication, Consent, and Goal are listed in the export but have no field-level documentation, making it impossible to assess what's actually exported for messaging and consent data. (`fhir/resources/` directory — no files for these 3 types)

5. **No export trigger documentation**: How a patient or provider actually obtains the export is not described anywhere. (`ehi-export-overview.html` — only output format documented)

### Summary Stats

    Classification:  Standard-based projection
    Export format:   FHIR R4 JSON + C-CDA v2.1 XML (ZIP)
    Model type:      Standard projection (FHIR R4 + C-CDA)
    Entities:        16 FHIR resource types in EHI export (22 documented total)
    Fields:          629 (across 22 documented resources)
    Descriptions:    99.8% of fields have descriptions
    Sample data:     No
    Bulk export:     Yes (supports multiple patients)
    Domains covered: 12 of 16 applicable domains (✅ or better)

### Bottom Line

One Medical's EHI export is a well-documented FHIR R4 + C-CDA projection that covers standard clinical data domains thoroughly but entirely omits billing/claims data — a significant gap for a practice that bills insurance for every visit. The export reflects a thoughtful FHIR implementation (non-US Core resources, ML transparency, custom terminology) but falls short of a true "all EHI" export because the proprietary 1Life data model is flattened into standard FHIR resources, inevitably losing vendor-specific data that doesn't map to FHIR resource types.
