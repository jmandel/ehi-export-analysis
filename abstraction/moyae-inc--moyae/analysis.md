# EHI Export Analysis: Moyae, Inc.

**Product**: Moyae (Version 1)
**Analysis date**: 2026-02-16
**CHPL ID**: 11331 (15.05.05.3141.MOYA.01.01.1.230816)

## 1. Product Context

Moyae is a cloud-based, AI-powered EHR built exclusively for ophthalmology and optometry practices. It was founded by Sami Mirimiri (formerly at Capital One and EnterMedicare) and emerged from Techstars Seattle 2023. The company is small and early-stage, with no visible market traction on third-party review sites.

**What it stores (relevant to EHI completeness)**:
- **Ophthalmology-specific clinical data**: IOP measurements, visual acuity, refraction data, anterior/posterior segment findings, retina drawings, intravitreal injection series
- **Clinical documentation**: Encounter notes, care plans, customizable charting templates with AI-suggested diagnostic coding
- **Prescriptions**: Embedded e-prescribing via DrFirst/Rcopia
- **Implantable devices**: IOLs and other ophthalmic implants (certified (a)(14))
- **Diagnostic imaging orders**: CPOE for imaging (certified (a)(3))
- **Quality/registry data**: IRIS Registry integration, MIPS reporting

**What it delegates externally**:
- **Billing, scheduling, and practice management** are handled by AdvancedMD via a bi-directional integration. Moyae explicitly chose not to build its own PM/billing system. Therefore, missing billing data in Moyae's export is expected — that data lives in AdvancedMD.

**Notable certification gaps**: No certification for CPOE for medications (a)(1), lab ordering (a)(2), clinical decision support (a)(9), problem list (a)(8), medication list (a)(7), or patient portal (e)(1). This is a narrow certification footprint consistent with a specialty-focused startup.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `disclosures-and-costs.html` (24 KB) | ONC mandatory disclosures page. Contains a single line about EHI export format: "New-line delimited JSON export of FHIR data." Links to NDJSON spec. Lists certification criteria and costs. | Low — one sentence of EHI-specific content |
| `moyae-fhir-api-postman-collection.json` (2.5 MB) | Full Postman collection: 125 folders, 485 endpoints across ~120 FHIR resource types plus Authentication, Export, CCDA, MFA folders. No response examples, no field descriptions. | Medium — shows API structure but zero content documentation |
| `fhir-capability-statement.json` (1.2 MB) | FHIR R4 CapabilityStatement listing 146 resource types with full CRUD interactions and 2,416 search parameters. One system-level `$export` operation. Software: "FHIR Server" v1.0.0. | Medium — confirms server scope but reveals generic nature |
| `smart-configuration.json` (556 B) | SMART on FHIR config with Auth0-based OAuth2 endpoints. Standard capabilities. | Low |
| Screenshots (5 PNGs) | Visual evidence of disclosures page and Postman API docs (Export section). | Low — confirms text content |
| Enrichment scripts and outputs | Prior agent's parsing of Postman and CapabilityStatement. | Reference only — I re-parsed from raw sources |

**Most informative**: The CapabilityStatement and Postman collection together reveal the full scope of the FHIR server. **Least informative**: The disclosures page, which contributes a single sentence about EHI export format.

## 3. Export Mechanics

- **Format**: FHIR R4 NDJSON (Newline Delimited JSON)
- **Mechanism**: FHIR Bulk Data `$export` operation at the system level (`{{API_URL}}/$export`)
- **Parameters**: `_outputFormat=ndjson`, `_since` (date filter), `_type` (resource type filter)
- **Authentication**: Bearer token (Cognito/Auth0) + API key header
- **Job management**: Async — initiate export, poll status at `$export/:jobId`, cancel via DELETE
- **Single vs bulk**: System-level `$export` exports all patients; `_type` parameter can filter by resource type
- **Access constraints**: Requires API key and authenticated bearer token; no documentation on who can initiate exports or whether patients can self-serve
- **Fees**: None mentioned specifically for EHI export; general pricing is per-user subscription

## 4. Export Content: What's In It

### No data dictionary exists

Moyae provides **no data dictionary, no schema documentation, no field-level documentation, and no sample data**. The only documentation of what the export contains is:

1. A single sentence: "New-line delimited JSON export of FHIR data"
2. A Postman collection showing API endpoints (URLs and HTTP methods only)
3. A FHIR CapabilityStatement listing supported resource types

### What the CapabilityStatement reveals

The FHIR server declares support for **146 resource types** — essentially the entire FHIR R4 specification catalog. Key characteristics:

- **All 146 resource types** support identical interactions: create, read, update, delete, vread, and search-type (except Binary, which lacks search)
- **2,416 search parameters** total, all standard FHIR definitions — zero custom parameters
- **Zero custom profiles** — no StructureDefinitions referenced
- **Zero custom extensions** documented
- **Software name**: "FHIR Server" v1.0.0 (generic, not product-specific)
- **One operation**: `$export` referencing the standard Bulk Data IG

This is a textbook generic FHIR server. It mechanically supports every FHIR R4 resource type with identical CRUD operations, with no evidence of product-specific customization.

### What the Postman collection reveals

The Postman collection has **125 folders** with **485 endpoints**. Each resource type folder has a uniform structure (typically 4 endpoints: GET by ID, POST, PUT, DELETE/search). Notable:

- **Zero endpoint descriptions** (except the Authentication folder, which has a brief note about OAuth flow)
- **Zero response examples** for any endpoint
- **Zero field-level documentation** for any resource type
- The Export folder documents 3 endpoints: initiate export, check status, cancel job
- Includes some STU3-era resource names (e.g., "Body Site," "Procedure Request," "Eligibility Request") alongside R4 names, suggesting the collection may be auto-generated or not carefully maintained

### Vendor's own content organization

Since there is no data dictionary, I can only present the resource types from the CapabilityStatement organized by FHIR domain:

| Category | Resource Types | Search Params | Notes |
|---|---|---|---|
| Clinical | 41 | 801 | Standard FHIR clinical resources (Patient, Condition, Observation, etc.) |
| Financial | 16 | 265 | Claim, Coverage, ExplanationOfBenefit, ChargeItem, Invoice, etc. |
| Administrative | 14 | 253 | Practitioner, Organization, Location, Appointment, Schedule, etc. |
| Infrastructure/Definitional | 75 | 1,097 | CapabilityStatement, StructureDefinition, CodeSystem, ValueSet, etc. |
| **Total** | **146** | **2,416** | |

The full inventory is at `analysis/entity-inventory-full.json`.

**Critical observation**: The 75 Infrastructure/Definitional resource types (StructureDefinition, CodeSystem, ValueSet, OperationDefinition, SearchParameter, TestScript, ImplementationGuide, etc.) are FHIR conformance and vocabulary resources that no EHR stores patient data in. Their inclusion is evidence that this is a generic FHIR server, not a purpose-built export. Similarly, resources like `SubstanceNucleicAcid`, `MedicinalProductPharmaceutical`, `ResearchElementDefinition`, `MolecularSequence`, and `SubstancePolymer` have no relevance to an ophthalmology practice.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

Moyae's export documentation provides essentially **zero product-specific content information**. The vendor does not describe, categorize, or document what data is exported. The only evidence of scope is:

- The FHIR server supports 146 resource types (the entire FHIR R4 catalog)
- The `$export` operation can theoretically export from any of these resource types

The server supports financial resource types (Claim, Coverage, ExplanationOfBenefit, etc.), but since Moyae delegates billing to AdvancedMD, it is highly unlikely these contain data. The server also supports clinical resource types that could theoretically represent ophthalmology data (Observation for IOP/visual acuity, Procedure for injections, Device for implants), but there is no documentation of how — or whether — specialty-specific data is mapped to these resources.

**The fundamental problem**: Supporting a resource type in a FHIR server is not the same as populating it with data. A generic FHIR server that accepts any valid FHIR resource proves nothing about what patient data is actually stored and exportable. Without a data dictionary, sample data, or documentation of data mappings, it is impossible to assess what the export actually contains.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | `Patient` resource type supported in server; no documentation of which demographic fields are populated | Product stores demographics (certified (a)(5)); likely present but undocumented |
| Encounters / visits | ⚠️ Partial | `Encounter` resource type supported; no documentation | Product stores encounters; likely present but undocumented |
| Problems / conditions | ⚠️ Partial | `Condition` resource type supported; no documentation | Product likely stores diagnoses (ICD coding); undocumented |
| Medications / prescriptions | ⚠️ Partial | `MedicationRequest`, `Medication` supported; no documentation | Product has e-prescribing; likely present but undocumented |
| Allergies | ⚠️ Partial | `AllergyIntolerance` supported; no documentation | Uncertain if product stores structured allergies |
| Immunizations | ⚠️ Partial | `Immunization` supported; no documentation | Unlikely to be a major ophthalmology data domain |
| Vitals | ⚠️ Partial | `Observation` supported; no documentation | Product stores IOP, visual acuity — but how these map to Observation is undocumented |
| Lab results | ⚠️ Partial | `Observation`, `DiagnosticReport` supported; no documentation | Product not certified for lab ordering; may not store lab data natively |
| Imaging / diagnostic reports | ⚠️ Partial | `ImagingStudy`, `DiagnosticReport` supported; no documentation | Product does CPOE for imaging (certified (a)(3)); orders likely present, images likely external |
| Procedures | ⚠️ Partial | `Procedure` supported; no documentation | Product stores intravitreal injections, procedures; mapping undocumented |
| Clinical notes / documents | ⚠️ Partial | `DocumentReference`, `Composition` supported; no documentation | Product stores encounter notes; format/mapping undocumented |
| Care plans / goals | ⚠️ Partial | `CarePlan`, `Goal` supported; no documentation | Product stores care plans; undocumented |
| Orders / referrals | ⚠️ Partial | `ServiceRequest` supported; no documentation | Product has CPOE for imaging; undocumented |
| Insurance / coverage | ⚠️ Partial | `Coverage`, `InsurancePlan` supported; no documentation | May store basic coverage info; billing/PM is in AdvancedMD |
| Claims / billing | N/A | `Claim`, `ExplanationOfBenefit` supported but billing delegated to AdvancedMD | Not a gap — billing data lives in AdvancedMD, not Moyae |
| Payments | N/A | `PaymentNotice`, `PaymentReconciliation` supported but payments handled by AdvancedMD | Not a gap — payment data lives in AdvancedMD |
| Consents / directives | ⚠️ Partial | `Consent` supported; no documentation | Unknown if product stores consent data |
| Patient communications | ❌ Not covered | No patient portal (not certified for (e)(1)); `Communication` resource supported but no portal | N/A — product doesn't have a patient portal |
| Specialty: Ophthalmology | ❌ Not covered | No custom FHIR profiles, no custom extensions, no documentation of how IOP, visual acuity, refraction, retina drawings, or injection series are represented | **Major gap**: Product's core differentiator (ophthalmic data) has zero documented export representation |
| Implantable devices | ⚠️ Partial | `Device`, `DeviceUseStatement` supported; certified (a)(14) | Likely present but undocumented |

**Every domain rated "⚠️ Partial" is rated so because the FHIR resource type exists in the server but there is zero documentation confirming data is actually populated.** The rating could be "Covered" or "Not covered" — we simply cannot tell.

**The ophthalmology gap is the most significant finding.** Moyae's entire value proposition is specialty-specific ophthalmic data (IOP tracking, visual acuity, refraction, retina drawings, intravitreal injection series). Standard FHIR R4 has no native representation for most of these — they would require custom Observation profiles, extensions, or at minimum documentation of LOINC/SNOMED codes used. None of this exists.

## 6. Documentation Quality

**Documentation quality is extremely poor.** The EHI export documentation consists of:

1. **One sentence** on the disclosures page ("New-line delimited JSON export of FHIR data")
2. **A Postman collection** showing API URLs and HTTP methods — no descriptions, no examples, no field documentation
3. **A CapabilityStatement** that is the output of a generic FHIR server, not product-specific documentation

**What's missing**:
- No data dictionary mapping product data to FHIR resources
- No documentation of custom profiles or extensions for ophthalmology data
- No sample data or worked examples
- No user guide for initiating an export
- No description of which resource types actually contain data
- No value set or code system documentation
- No documentation of relationships between resources

**Could a developer build an import?** A developer could parse generic FHIR R4 NDJSON, but would have no guidance on:
- Which resource types contain data vs. which are empty
- How ophthalmology-specific data is encoded
- What coded values or extensions to expect
- Whether the export is complete

**Machine-readable artifacts**: The CapabilityStatement and SMART configuration are machine-readable but contain only generic FHIR server metadata, not product-specific content documentation.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Minimal/stub/unclear**

The documentation is too thin to assess actual coverage. While the FHIR server technically supports 146 resource types, there is zero evidence about which ones are populated with patient data. More critically, the product's core ophthalmology-specific data (IOP, visual acuity, refraction, retina drawings, injection series) — which is the main clinical data Moyae stores — has no documented FHIR mapping. The generic FHIR server supports `Observation` and `Procedure`, but without custom profiles or extensions documented, there is no way to know if specialty data is exported, let alone interpret it. Since billing is delegated to AdvancedMD, missing financial data is not a gap, but missing ophthalmology-specific clinical data representation is a critical one.

**Axis 2 — Export approach: Repackaged existing export**

Multiple signals indicate this is the same FHIR API used for (g)(10) being relabeled as (b)(10):

1. **Generic FHIR server**: Software self-identifies as "FHIR Server" v1.0.0 — a generic name, not a product-specific export
2. **Full R4 catalog**: Supporting all 146 FHIR R4 resource types with identical CRUD operations is characteristic of a generic FHIR server (likely an off-the-shelf FHIR server deployment), not a purpose-built export
3. **Zero customization**: No custom profiles, no custom extensions, no custom search parameters — nothing that would indicate product-specific data mapping
4. **Irrelevant resource types**: Includes SubstanceNucleicAcid, MedicinalProductPharmaceutical, ResearchElementDefinition, MolecularSequence — resources that no ophthalmology EHR would use
5. **Same infrastructure**: The `$export` endpoint, authentication, and API base URL are the same as the (g)(10) FHIR API
6. **One-sentence description**: The disclosures page describes the EHI export as "New-line delimited JSON export of FHIR data" — identical to how one would describe Bulk FHIR (b)(11)/(g)(10) exports
7. **STU3/R4 naming inconsistencies in Postman**: The Postman collection includes some STU3-era resource names (e.g., "Body Site," "Procedure Request," "Eligibility Request") alongside R4 names, suggesting the collection may have been auto-generated

The `$export` endpoint used for (b)(10) is the same standard Bulk Data export operation used for (b)(11)/(g)(10). There is no purpose-built EHI export layer — Moyae pointed to their generic FHIR server and called it (b)(10).

### Key Findings

1. **No data dictionary exists.** The entire EHI export documentation is one sentence ("New-line delimited JSON export of FHIR data") plus a Postman collection of API URLs with no descriptions or examples. There is no way to assess what data is actually exported. (Sources: `disclosures-and-costs.html`, `moyae-fhir-api-postman-collection.json`)

2. **Generic FHIR server, not purpose-built export.** The CapabilityStatement reveals a generic FHIR R4 server supporting all 146 resource types with identical interactions, zero custom profiles, and zero custom extensions. Software self-identifies as "FHIR Server" v1.0.0. This is the same infrastructure used for (g)(10). (Source: `fhir-capability-statement.json`)

3. **Ophthalmology-specific data has no documented export path.** Moyae's core clinical data — IOP tracking, visual acuity, refraction, retina drawings, intravitreal injection series — requires custom FHIR profiles or extensions to represent. None are documented. This is the product's primary clinical data, and its export representation is completely opaque. (Sources: `product-research.md`, `fhir-capability-statement.json`)

4. **Billing gap is expected, not a deficiency.** Moyae delegates billing, scheduling, and practice management to AdvancedMD. Financial resource types exist in the server but are unlikely to contain data. This is by design, not a gap in the (b)(10) export. (Source: `product-research.md`)

5. **Postman collection has zero useful content documentation.** Of 125 folders and 485 endpoints, only the Authentication folder has any description text. No resource type folder has field descriptions, response examples, or data documentation. (Source: `moyae-fhir-api-postman-collection.json`, parsed in `analysis/parse-artifacts.py`)

### Summary Stats

    Coverage:        Minimal/stub/unclear
    Approach:        Repackaged existing export
    Export format:   FHIR R4 NDJSON (Bulk Data $export)
    Entities:        146 FHIR resource types (entire R4 catalog; actual population unknown)
    Fields:          2,416 search parameters (all standard FHIR; zero product-specific)
    Descriptions:    0% (zero field-level descriptions anywhere)
    Sample data:     No
    Bulk export:     Yes (system-level $export)
    Domains covered: 0 of 15 confirmed; up to 13 possible but unverifiable

### Bottom Line

Moyae's (b)(10) export is a generic FHIR R4 server's Bulk Data `$export` operation rebranded as EHI export — the same infrastructure used for (g)(10). With no data dictionary, no custom profiles, no sample data, and no documentation beyond a single sentence, it is impossible to verify what patient data is actually exported. The most significant concern is that the product's core ophthalmology-specific clinical data (IOP, visual acuity, refraction, retina drawings, injection series) has no documented FHIR mapping, meaning the export's representation of the product's primary clinical data is completely opaque.
