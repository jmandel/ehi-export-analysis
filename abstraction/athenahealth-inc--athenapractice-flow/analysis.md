# EHI Export Analysis: athenahealth, Inc.

**Product**: athenaPractice v25 / athenaFlow v25
**Analysis date**: 2026-02-16
**CHPL IDs**: 11629 (athenaPractice), 11663 (athenaFlow)

## 1. Product Context

athenaPractice (formerly GE Centricity Practice Solution) is a fully integrated EHR and Practice Management system serving ambulatory practices. It is a Windows-based client-server application — architecturally distinct from athenahealth's cloud-native flagship, athenaOne. athenaFlow (formerly GE Centricity EMR) is the companion EMR product from the same GE Centricity lineage, focused more on clinical charting and lacking some practice management features.

**Data the products store** (relevant to EHI scope):

- **Clinical**: SOAP notes, encounter charting, problem lists, medication lists, allergy lists, CPOE (medications, labs, imaging), e-prescribing, lab results, immunizations, family history, care plans, care teams, clinical impressions, consent, devices, diagnostic reports, documents/images, clinical notes, specimens
- **Practice Management**: Patient registration/demographics, appointment scheduling, insurance/coverage management
- **Billing/Financial**: Patient accounting (charges, payments, adjustments), claims submission, collections, eligibility verification, deductible tracking, electronic remittance, billing statements
- **Patient Engagement**: Patient portal, secure messaging, appointment reminders
- **Interoperability**: FHIR R4 API, C-CDA, Direct messaging, public health reporting

The product is certified across 35+ ONC criteria including (b)(10) for EHI export. The FHIR API documentation reveals 47 resource types in the CapabilityStatement, including 9 custom (non-standard FHIR) financial resource types.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/site/ehiexport.html` (25 KB) | EHI Export page — lists all 43 (athenaPractice) / 31 (athenaFlow) resource types in the export, describes format as FHIR R4 NDJSON via Bulk Data Access | **High** — primary source for what's in the export |
| `downloads/site/index.html` (23 KB) | IG home page — overview of resource availability by product, footnotes on product differences | **High** — clarifies product-specific resource availability |
| `downloads/site/operations.html` (11 KB) | Operations page — confirms `Group/$export` endpoint for bulk data | **Medium** — confirms export mechanism |
| `downloads/definitions/*.json` (121 files, ~13 MB total) | FHIR StructureDefinition profiles (54) and extension definitions (56), CapabilityStatements (2), ConceptMap, ValueSets | **Highest** — machine-readable field-level schemas for all resource types |
| `downloads/examples/*.json` (220 files, ~18 MB total) | Example resource instances: 98 clinical/PM examples + 110 StructureDefinitions + 12 system/metadata | **High** — demonstrates real data shapes for standard resources; no examples for custom financial resources |
| `downloads/profiles/*.html` (43 files) | HTML profile pages for each resource type — human-readable field documentation | **Medium** — same content as JSON StructureDefinitions in more readable form |
| `downloads/enrichment/profiles-catalog.json` | Pre-extracted catalog of all 54 profiles with element counts and categories | **High** — structured summary |
| `downloads/enrichment/coverage-accounting.json` | Category assignments for all profiles | **Medium** — categorization reference |
| `downloads/site/full-ig.zip` (52.7 MB) | Complete FHIR Implementation Guide package | Not extracted — constituent parts already available |
| `downloads/site/definitions.json.zip` (1.3 MB) | Source for the extracted definitions | N/A — already extracted |
| `downloads/site/examples.json.zip` (2.0 MB) | Source for the extracted examples | N/A — already extracted |
| `downloads/site/security.html` (28 KB) | OAuth 2.0 / SMART on FHIR authentication docs | **Low** — relevant to API access, not export content |
| `downloads/site/restapi.html` (21 KB) | RESTful API search parameters | **Low** — operational details |

## 3. Export Mechanics

- **Format**: FHIR R4 Newline Delimited JSON (NDJSON) — both standard FHIR resources and custom (non-FHIR) logical resources
- **Mechanism**: FHIR Bulk Data Access via `Group/$export` API endpoint
- **Capability**: Bulk export (group-level), per the Bulk Data Access specification
- **Single-patient**: Not explicitly documented for EHI export; the API supports `Patient/$everything` for individual patients
- **Access constraints**: OAuth 2.0 / SMART on FHIR authentication required (documented in `security.html`). No fees mentioned. No explicit step-by-step instructions for initiating an EHI export are provided — the documentation covers the data model exhaustively but not the operational process.

The EHI export page states: *"athenaPractice and athenaFlow support the export of electronic health information (EHI) based on FHIR Bulk Data Access."* Custom resources *"conform to the basic requirements for any FHIR Base Resource with id and meta elements"* — they use FHIR-like JSON structures but define their own element schemas for data types (billing, collections, etc.) that have no standard FHIR equivalent.

## 4. Export Content: What's In It

### Source data

The export documentation is a FHIR R4 Implementation Guide (IG) v25.0.0, generated 2025-04-10, published using standard HL7 FHIR IG Publisher tooling. It contains:

- **54 StructureDefinition profiles** defining field-level schemas
- **56 custom extension definitions** adding vendor-specific fields to standard FHIR resources
- **4,270 total fields** across all profiles, with **100% having descriptions** (every field has at least a `short` or `definition` text)
- **698 fields with value set bindings** (16.3%) for coded elements
- **220 example JSON files**, including 98 clinical/PM example instances
- **2 CapabilityStatements** (one per product) documenting full API capabilities

Of the 54 profiles, **43 are included in the EHI export** for athenaPractice (3,654 fields) and **31 for athenaFlow** (approximately 2,640 fields). The remaining 11 profiles (AuditEvent, ConceptMap, Endpoint, List, NamingSystem, Subscription, ValueSet — system/infrastructure resources — plus MedicationDispense, Media, Specimen, and Basic/Posting — clinical resources) have profiles but are not listed on the EHI export page.

### Vendor's own content organization

The vendor organizes resources into four categories. The following table shows all 43 EHI export entities for athenaPractice:

**Practice Management (7 entities, 697 fields)**

| Entity | Base Type | Fields | Descriptions | Bindings | Product |
|---|---|---|---|---|---|
| Patient | Patient | 279 | 279 | 32 | Both |
| RelatedPerson | RelatedPerson | 102 | 102 | 20 | Both |
| Appointment | Appointment | 101 | 101 | 28 | Both |
| Account | Account | 83 | 83 | 5 | athenaPractice only |
| Coverage | Coverage | 74 | 74 | 11 | Both |
| Slot | Slot | 33 | 33 | 8 | athenaPractice only |
| Schedule | Schedule | 25 | 25 | 6 | athenaPractice only |

**Clinical (20 entities, 1,839 fields)**

| Entity | Base Type | Fields | Descriptions | Bindings | Product |
|---|---|---|---|---|---|
| AllergyIntolerance | AllergyIntolerance | 198 | 198 | 39 | Both |
| Observation | Observation | 193 | 193 | 29 | Both |
| MedicationRequest | MedicationRequest | 134 | 134 | 23 | Both |
| Encounter | Encounter | 126 | 126 | 23 | Both |
| Immunization | Immunization | 110 | 110 | 17 | Both |
| DocumentReference | DocumentReference | 99 | 99 | 20 | Both |
| Condition | Condition | 88 | 88 | 16 | Both |
| Consent | Consent | 87 | 87 | 17 | Both |
| Device | Device | 84 | 84 | 10 | Both |
| Procedure | Procedure | 82 | 82 | 19 | Both |
| CarePlan | CarePlan | 81 | 81 | 13 | Both |
| MedicationStatement | MedicationStatement | 80 | 80 | 15 | Both |
| ServiceRequest | ServiceRequest | 77 | 77 | 19 | Both |
| ClinicalImpression | ClinicalImpression | 73 | 73 | 13 | Both |
| CareTeam | CareTeam | 70 | 70 | 11 | Both |
| MedicationAdministration | MedicationAdministration | 69 | 69 | 13 | Both |
| FamilyMemberHistory | FamilyMemberHistory | 63 | 63 | 12 | Both |
| DiagnosticReport | DiagnosticReport | 59 | 59 | 9 | Both |
| Goal | Goal | 50 | 50 | 14 | Both |
| Binary | Binary | 16 | 16 | 4 | Both |

**Custom / Financial (10 entities, 519 fields) — athenaPractice only**

| Entity | Kind | Fields | Descriptions | Bindings |
|---|---|---|---|---|
| Charge | logical | 106 | 106 | 12 |
| Eligibility | logical | 86 | 86 | 9 |
| Collection | logical | 78 | 78 | 13 |
| Payment | logical | 49 | 49 | 5 |
| PatientInsurance | logical | 46 | 46 | 5 |
| Adjustment | logical | 40 | 40 | 4 |
| Claim | logical | 40 | 40 | 3 |
| Deductible | logical | 40 | 40 | 4 |
| BillingStatement | logical | 21 | 21 | 2 |
| OperationOutcome | logical | 13 | 13 | 0 |

**System (6 entities, 599 fields)**

| Entity | Base Type | Fields | Descriptions | Bindings | Product |
|---|---|---|---|---|---|
| Organization | Organization | 121 | 121 | 21 | Both |
| PractitionerRole | PractitionerRole | 104 | 104 | 12 | Both |
| Provenance | Provenance | 98 | 98 | 14 | Both |
| Medication | Medication | 95 | 95 | 6 | Both |
| Location | Location | 94 | 94 | 19 | Both |
| Practitioner | Practitioner | 87 | 87 | 15 | Both |

The complete entity inventory with all 4,270 fields is in `analysis/full-entity-inventory.json`.

### Custom financial resource detail

The 9 custom financial resources (excluding OperationOutcome) are the most distinctive feature of this export. They use FHIR's "logical" model type — JSON structures following FHIR conventions but defining entirely vendor-specific schemas. For example, the **Charge** resource (106 fields) includes: CPT codes, modifiers (up to 4), service date ranges, fee/allowed amounts, RVU values, revenue codes, place/type of service, authorization numbers, referring/rendering/supervising/ordering providers, co-pay amounts, and facility information. Field descriptions reference internal structures: *"This column should be linked to the MedLists table MedListsId column with a TableName of ProcedureCodeQualifier."*

### Notable omissions from EHI export

Three clinical resources with profiles in the IG are **not included** in the EHI export:
- **MedicationDispense** (84 fields) — pharmacy dispensing records
- **Media** (49 fields) — clinical images/photos
- **Specimen** (66 fields) — laboratory specimen tracking

These are available through the regular FHIR API but are not listed on the EHI export page.

### Example data coverage

98 example instances cover all standard resource types in the EHI export. However, **no example instances exist for any of the 9 custom financial resources** (Adjustment, BillingStatement, Charge, Claim, Collection, Deductible, Eligibility, PatientInsurance, Payment). The only "custom" example is a Basic/Posting resource. This means developers cannot see what a financial resource actually looks like in practice — they have only the StructureDefinition schema.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor organizes the export into four categories:

1. **Clinical Resources** (20 entities, 1,839 fields): The deepest category. Covers the full clinical workflow from encounter documentation through diagnoses, medications (request, administration, statement), allergies (198 fields — the most detailed allergy model seen), lab results (Observation with 193 fields), procedures, care plans, goals, immunizations, family history, devices, consents, and documents/binary attachments. ServiceRequest (77 fields) covers lab orders, imaging orders, referrals, and consultations via category/code differentiation. Custom extensions add vendor-specific data like encounter authenticator/description/summary, medication NDC/RxNorm/DDID codes, and allergy encounter links.

2. **Custom / Financial Resources** (10 entities, 519 fields, athenaPractice only): This is where the export stands out. Nine purpose-built resource types cover the full billing lifecycle: Charge (106 fields — CPT codes, modifiers, fees, RVUs, providers), Claim (40 fields — claim numbers, status, payer info), Payment (49 fields — payment types, check/EFT details), Adjustment (40 fields — adjustment codes, amounts), Collection (78 fields — agency details, amounts, statuses), Deductible (40 fields — patient responsibility tracking), Eligibility (86 fields — coverage details, copays, plan info), PatientInsurance (46 fields), and BillingStatement (21 fields).

3. **Practice Management Resources** (7 entities, 697 fields): Patient demographics (279 fields — extremely detailed with 12 custom extensions for gender identity, sexual orientation, tribal affiliation, pronouns, occupation, guarantor details), insurance coverage, appointments, scheduling, related persons, and accounts.

4. **System Resources** (6 entities, 599 fields): Reference data for organizations, practitioners, practitioner roles, locations, medications, and provenance.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | Patient (279 fields, 12 custom extensions), RelatedPerson (102 fields) | Exceptionally thorough — includes gender identity, pronouns, sexual orientation, tribal affiliation, occupation, guarantor details |
| Encounters / visits | ✅ Covered | Encounter (126 fields, 3 extensions for authenticator/description/summary) | Thorough — includes encounter classification, hospitalization details, status tracking |
| Problems / conditions | ✅ Covered | Condition (88 fields) with 3 example instances | Thorough — includes onset, abatement, severity, verification status, category |
| Medications / prescriptions | ✅ Covered | MedicationRequest (134 fields, 6 extensions for NDC/RxNorm/DDID/dispenser), MedicationStatement (80 fields), MedicationAdministration (69 fields), Medication (95 fields) | Comprehensive — covers prescribing, administration, and medication catalog. **MedicationDispense (84 fields) is profiled but NOT in EHI export** — a gap for pharmacy dispensing records |
| Allergies | ✅ Covered | AllergyIntolerance (198 fields, 2 extensions) | Exceptionally detailed — one of the most thorough allergy models observed |
| Immunizations | ✅ Covered | Immunization (110 fields, 2 extensions for VFC eligibility and wasNotGiven) | Thorough |
| Vitals | ✅ Covered | Observation (193 fields) — vitals are a category within Observation | Covered via Observation with category-based filtering |
| Lab results | ✅ Covered | Observation (193 fields), DiagnosticReport (59 fields) | Thorough — 19 Observation examples demonstrate various types |
| Imaging / diagnostic reports | ⚠️ Partial | DiagnosticReport (59 fields), ServiceRequest for imaging orders. **Media (49 fields) is profiled but NOT in EHI export** | DiagnosticReport covers reports; imaging orders via ServiceRequest. However, Media resource (clinical images/photos) is excluded from EHI export despite having a profile |
| Procedures | ✅ Covered | Procedure (82 fields) | Thorough |
| Clinical notes / documents | ✅ Covered | DocumentReference (99 fields), Binary (16 fields, 8 examples showing text/RTF/JPEG/gzip content), ClinicalImpression (73 fields), Encounter extensions (description, summary, authenticator) | Good coverage — documents stored as Binary attachments referenced by DocumentReference. Examples show office visit notes, clinical photos, and compressed attachments |
| Care plans / goals | ✅ Covered | CarePlan (81 fields), Goal (50 fields), CareTeam (70 fields) | Thorough — includes care plan activities, goal targets, team member roles |
| Orders / referrals | ✅ Covered | ServiceRequest (77 fields) — categorized as service, referral, or test; subcategorized as lab orders, imaging orders, consultations | Good — single resource handles multiple order types via category/code |
| Insurance / coverage | ✅ Covered | Coverage (74 fields), PatientInsurance (46 fields, custom), Eligibility (86 fields, custom) | Thorough — standard Coverage plus custom resources for insurance details and eligibility verification |
| Claims / billing | ✅ Covered | Charge (106 fields), Claim (40 fields) — athenaPractice only | Thorough for athenaPractice — CPT codes, modifiers, fees, RVUs, providers. **Not available for athenaFlow** |
| Payments | ✅ Covered | Payment (49 fields), Adjustment (40 fields) — athenaPractice only | Good for athenaPractice. **Not available for athenaFlow** |
| Consents / directives | ✅ Covered | Consent (87 fields, 2 extensions for encounter and period) | Thorough |
| Patient communications / portal messages | ❌ Not covered | No resource type for patient portal messages or secure messaging | Product has patient portal with secure messaging (see Section 1); no evidence in export. This is a gap for patient communication records that may be part of the designated record set |
| Specialty-specific data | ⚠️ Partial | No specialty-specific resources beyond general clinical types. ClinicalImpression (73 fields) may capture some assessment data. Custom forms/templates not explicitly represented | Product supports specialty-specific templates; unclear if custom form data is captured in standard resources or lost in export |

**Critical athenaFlow gap**: athenaFlow's EHI export excludes **all 12 resources** that are athenaPractice-only: Account, Schedule, Slot, Adjustment, BillingStatement, Charge, Claim, Collection, Deductible, Eligibility, PatientInsurance, Payment. The EHI export page notes these are *"only available through the athenaPractice or Practice Management products."* If athenaFlow installations store or integrate billing data (and the FHIR API index suggests some PM capabilities exist), this represents a significant EHI gap.

## 6. Documentation Quality

**Strengths:**
- **Machine-readable schemas**: All 54 profiles are published as FHIR StructureDefinition JSON with full element-level detail — paths, types, cardinality, descriptions, and value set bindings. This is the gold standard for API documentation.
- **100% description coverage**: Every one of the 4,270 fields has a short description or definition text. No undocumented fields.
- **698 value set bindings**: Coded fields reference standard terminologies (LOINC, SNOMED CT, ICD-10, CPT, RxNorm, NDC, CVX) with binding strength (required/extensible/preferred/example).
- **56 custom extension definitions**: All vendor-specific extensions are formally defined with URLs, types, and descriptions.
- **220 example instances**: Real data shapes for standard resource types, including 8 Binary examples showing various content types (JPEG images, plain text, RTF, gzip-compressed attachments).
- **Downloadable package**: Full IG available as ZIP in JSON/XML/TTL formats for programmatic consumption.
- **Standard tooling**: Published using HL7 FHIR IG Publisher, making it navigable with standard FHIR tools.

**Weaknesses:**
- **No export process documentation**: No step-by-step instructions for initiating an EHI export. The `Group/$export` operation is listed but not described with parameters, authentication flows, or workflow guidance.
- **No custom financial resource examples**: Zero example instances for the 9 custom billing resources (Charge, Claim, Payment, etc.). A developer implementing an import for these resources would have only the StructureDefinition schema — no sample data to validate against.
- **No sample NDJSON export files**: Individual resource examples exist but no representative bulk export output.
- **Cross-resource relationships underspecified**: While Reference-type fields link resources (e.g., Charge.patient → Patient), the full referential graph is not documented. The Charge profile references "MedLists table MedListsId" — a native database reference that suggests the FHIR model is a projection of a relational database, but the mapping is not fully exposed.

**Could a developer build an import from this documentation alone?** Largely yes, for standard FHIR resources — the StructureDefinitions and examples are sufficient. For custom financial resources, it would be significantly harder due to the lack of examples and the references to internal database structures (MedLists, ProcedureCodeQualifier codes) that aren't fully externalized.

## 7. Overall Assessment

### Classification

**Comprehensive native export** (for athenaPractice) / **Partial native export** (for athenaFlow)

For athenaPractice, this is one of the strongest EHI export implementations observed. It uses FHIR R4 as the export framework but extends it with 9 custom "logical" resource types to cover billing and financial data that standard FHIR doesn't address. This hybrid approach — standard FHIR for clinical data plus vendor-defined resources for financial data — delivers genuine breadth across clinical, administrative, and financial domains. The 43 resource types with 3,654 fully-documented fields cover the vast majority of what the product stores.

For athenaFlow, the export is significantly weaker: 31 resource types with no billing/financial data. If athenaFlow installations have billing capabilities (as the API documentation suggests), this is a real (b)(10) gap.

### Key Findings

1. **Exceptionally well-documented FHIR-based export**: 43 resource types (athenaPractice), 3,654 fields, 100% with descriptions, 698 value set bindings, 56 custom extensions, 220 example instances. This is among the most thoroughly documented EHI exports in the market. (Source: `definitions/*.json`, `examples/*.json`)

2. **Custom financial resources are the standout feature**: 9 vendor-defined "logical" resource types (Charge, Claim, Payment, Adjustment, Collection, Deductible, Eligibility, PatientInsurance, BillingStatement) with 506 fields covering the full billing lifecycle. Most vendors omit billing data entirely from EHI exports. (Source: `StructureDefinition-athena-charge-profile.json` and 8 peers)

3. **Three clinical resources profiled but excluded from EHI export**: MedicationDispense (84 fields), Media (49 fields), and Specimen (66 fields) have StructureDefinition profiles and are available through the regular FHIR API, but are **not listed on the EHI export page**. This is a minor but real gap — 199 fields of clinical data that the system stores but doesn't include in EHI export. (Source: comparison of `ehiexport.html` resource list vs. `definitions/` directory)

4. **No example data for custom financial resources**: Despite thorough StructureDefinition profiles, zero example instances exist for any of the 9 custom billing resource types. This makes the financial portion of the export harder to implement and validate. (Source: `examples/` directory — no Charge, Claim, Payment, etc. example files)

5. **athenaFlow billing gap**: athenaFlow's EHI export has 12 fewer resource types than athenaPractice, excluding all billing/financial data and some practice management data. This is explicitly documented but represents a meaningful gap for athenaFlow users. (Source: `ehiexport.html` comparison table)

### Summary Stats

```
Classification:  Comprehensive native export (athenaPractice); Partial native export (athenaFlow)
Export format:   FHIR R4 NDJSON (standard + custom logical resources)
Model type:      Hybrid — standard FHIR R4 resources + 9 vendor-defined logical resources for financial data
Entities:        43 (athenaPractice) / 31 (athenaFlow)
Fields:          3,654 (athenaPractice) / ~2,640 (athenaFlow)
Descriptions:    100% (4,270 of 4,270 fields across all profiles)
Sample data:     Yes (98 example instances for standard resources; none for custom financial resources)
Bulk export:     Yes (Group/$export via FHIR Bulk Data Access)
Domains covered: 15 of 17 applicable (athenaPractice) / 13 of 17 (athenaFlow)
```

### Bottom Line

For athenaPractice, this is a strong EHI export implementation — one of the better ones in the market. The combination of standard FHIR R4 resources for clinical data with 9 custom financial resource types for billing gives genuine breadth across clinical and financial domains, and the documentation quality (100% field descriptions, machine-readable StructureDefinitions, 220 examples) is excellent. The biggest gaps are the exclusion of MedicationDispense/Media/Specimen from the export, the absence of patient portal messaging data, and the lack of example instances for the custom financial resources. For athenaFlow, the omission of all billing/financial data is a significant limitation that reduces the export to a clinical-only projection.
