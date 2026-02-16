# EHI Export Analysis: Moyae, Inc.

**Product**: Moyae  
**Analysis date**: 2026-02-16  
**CHPL IDs**: 11331 (CHPL# 15.05.05.3141.MOYA.01.01.1.230816)

## 1. Product Context

Moyae is an early-stage, cloud-based EHR designed exclusively for ophthalmology and optometry practices. Founded by Sami Mirimiri, it emerged from the Techstars Seattle 2023 accelerator and is based in Austin, TX. The product is advised by ophthalmologists from Bascom Palmer, Baylor, Harvard/Mass Eye and Ear, Stanford, and UT Southwestern. It has minimal market traction — no third-party reviews or customer counts are publicly available.

**Clinical data the product stores** (relevant to export completeness):
- Patient demographics
- Ophthalmic examination data: IOP measurements, visual acuity, refraction, anterior/posterior segment findings
- Retina drawings (visual documentation)
- Intravitreal injection records with injection series history
- Implantable device records (certified (a)(14))
- Diagnostic imaging orders (certified (a)(3))
- Care plans and encounter notes with customizable templates
- Diagnostic codes (ICD) with AI-suggested coding
- E-prescribing data (via DrFirst/Rcopia integration)
- IRIS Registry / MIPS quality reporting data

**What Moyae does NOT store natively** (important for gap assessment):
- Billing, scheduling, and practice management data reside primarily in **AdvancedMD**, an external partner platform. Moyae explicitly chose not to build its own PM/billing system.
- No patient portal (not certified for (e)(1) VDT)
- No lab ordering (not certified for (a)(2))
- No PACS/image storage (orders imaging but doesn't store images)

This partnership with AdvancedMD is critical: it means billing and scheduling data are likely outside Moyae's data model entirely, so their absence from the EHI export may be a scoping issue rather than a coverage gap.

## 2. Artifacts Reviewed

| Artifact | Size | What It Is | Informativeness |
|---|---|---|---|
| `disclosures-and-costs.html` | 24 KB | Webflow-hosted ONC disclosures page with certification info, EHI export format statement, costs | Low — single line about EHI export format |
| `moyae-fhir-api-postman-collection.json` | 2.5 MB | Full Postman collection documenting the Moyae FHIR API | Moderate — shows API structure but no descriptions, no examples |
| `fhir-capability-statement.json` | 1.2 MB | Live FHIR R4 CapabilityStatement from Moyae's FHIR server | High — lists 146 resource types, search params, US Core profiles |
| `smart-configuration.json` | 556 B | SMART on FHIR OAuth2 configuration | Low — confirms Auth0-based authentication |
| `enrichment/postman-api-summary.json` | 470 KB | Prior agent's parsed summary of Postman collection | Moderate — structured but redundant with raw collection |
| `enrichment/capability-statement-summary.json` | 823 KB | Prior agent's parsed summary of CapabilityStatement | Moderate — structured but redundant with raw data |
| Screenshots (5 files) | ~989 KB total | Visual evidence of disclosures page and Postman API docs | Low — confirms page layout |

**Most informative**: The FHIR CapabilityStatement reveals the server structure, US Core profile declarations, and the $export operation. The Postman collection confirms the same and includes a single C-CDA sample response.

**Least informative**: The disclosures page contributes exactly one sentence about EHI export: *"New-line delimited JSON export of FHIR data."*

## 3. Export Mechanics

- **Format**: NDJSON (Newline Delimited JSON) containing FHIR R4 resources
- **Mechanism**: FHIR Bulk Data `$export` operation at the system level
  - Endpoint: `{{API_URL}}/$export`
  - Parameters: `_outputFormat=ndjson`, `_since` (date filter), `_type` (resource type filter)
  - Asynchronous: returns a job ID; status polled at `$export/:jobId`; cancellable via DELETE
- **Authentication**: OAuth2/SMART on FHIR via Auth0 (bearer token + API key header)
- **Single-patient vs bulk**: The `$export` endpoint is system-level, implying bulk export. A `_type` filter can restrict to specific resource types. No patient-level `$export` is documented, though FHIR Bulk Data supports `Patient/:id/$export`.
- **Access constraints**: Requires developer credentials obtained by emailing support@moyae.com. Terms of use are extensive (see Postman collection description).
- **Fees**: Not explicitly stated for export. General pricing is per-user with add-on fees for eRx and direct messaging.

## 4. Export Content: What's In It

### What the documentation tells us

The export is described as a FHIR Bulk Data `$export` that operates over a FHIR R4 server supporting **146 resource types** — essentially the entire FHIR R4 resource catalog. This is atypical; most EHRs expose only the 20-25 US Core resource types.

**However, supporting 146 resource types in the API does not mean data lives in all 146.** There is no documentation of which resource types Moyae actually populates with patient data. The FHIR R4 specification defines ~150 resource types, and this server mechanically supports nearly all of them (including irrelevant types like `SubstanceNucleicAcid`, `MedicinalProductPharmaceutical`, `ResearchElementDefinition`, `BiologicallyDerivedProduct`).

### Evidence of actual data: US Core profiles

The CapabilityStatement declares **US Core supported profiles** on 20 resource types, which is the strongest signal of which resources Moyae actually populates:

| Resource Type | US Core Profile(s) |
|---|---|
| AllergyIntolerance | us-core-allergyintolerance |
| CarePlan | us-core-careplan |
| CareTeam | us-core-careteam |
| Condition | us-core-condition |
| Device | us-core-implantable-device |
| DiagnosticReport | us-core-diagnosticreport-lab, us-core-diagnosticreport-note |
| DocumentReference | us-core-documentreference |
| Encounter | us-core-encounter |
| Goal | us-core-goal |
| Immunization | us-core-immunization |
| Location | us-core-location |
| Medication | us-core-medication |
| MedicationRequest | us-core-medicationrequest |
| Observation | 6 profiles (lab, vitals, smoking status, pulse oximetry, pediatric BMI, pediatric weight-for-height, head circumference) |
| Organization | us-core-organization |
| Patient | us-core-patient |
| Practitioner | us-core-practitioner |
| PractitionerRole | us-core-practitionerrole |
| Procedure | us-core-procedure |
| Provenance | us-core-provenance |

These 20 resources align closely with the USCDI/US Core data set — the standard clinical summary data required for (g)(10) FHIR API access. This strongly suggests the export is essentially the **(g)(10) FHIR API export repackaged as (b)(10)**.

### C-CDA sample evidence

The Postman collection includes one C-CDA sample response ("Generate Alice Newman's CCDA," 151 KB). It contains 23 sections with 33 entries covering standard clinical summary content:

| C-CDA Section | Entries |
|---|---|
| Allergies, adverse reactions, alerts | 2 |
| History of medication use | 3 |
| Problem List | 5 |
| History of Procedures | 2 |
| Relevant Dx tests/lab data | 1 |
| Progress Notes | 1 |
| Evaluation Notes | 1 |
| Goal Notes | 2 |
| Plan Notes | 4 |
| Procedure Notes | 1 |
| Laboratory Report Narrative | 1 |
| Immunizations | 2 |
| Health Concerns Document | 4 |
| Social History | 2 |
| Vital Signs | 1 |
| Medical Equipment | 1 |

No ophthalmology-specific content (IOP, visual acuity, refraction, retina drawings, injection records) appears in the C-CDA sample.

### What's NOT documented

- **No data dictionary**: No mapping of Moyae's internal data model to FHIR resources
- **No custom extensions/profiles**: No documentation of how ophthalmology-specific data (IOP measurements, visual acuity, refraction, retina drawings, intravitreal injection series) is represented in FHIR. Standard FHIR has no built-in structures for most of these.
- **No sample export data**: Zero response body examples across 953 of 954 API endpoints
- **No field-level documentation**: No descriptions on any FHIR resource endpoint
- **No value sets**: No coded value documentation
- **No export user guide**: No instructions for initiating an export

### Vendor's own content organization

Moyae does not provide a data dictionary or organize export content into categories. The only structure comes from the FHIR resource type names. Below are the 20 US Core-profiled resources (the best evidence of populated resources), plus the financial resource types that are supported but have no US Core profiles:

| Resource Type | Category | US Core Profile | Search Params | Description Available |
|---|---|---|---|---|
| Patient | Clinical | ✅ | 23 | No |
| Encounter | Clinical | ✅ | 22 | No |
| Condition | Clinical | ✅ | 22 | No |
| Observation | Clinical | ✅ (6 profiles) | 37 | No |
| Procedure | Clinical | ✅ | 14 | No |
| MedicationRequest | Clinical | ✅ | 20 | No |
| AllergyIntolerance | Clinical | ✅ | 13 | No |
| Immunization | Clinical | ✅ | 14 | No |
| DiagnosticReport | Clinical | ✅ (2 profiles) | 16 | No |
| DocumentReference | Clinical | ✅ | 15 | No |
| CarePlan | Clinical | ✅ | 15 | No |
| CareTeam | Clinical | ✅ | 11 | No |
| Goal | Clinical | ✅ | 10 | No |
| Device | Clinical | ✅ | 11 | No |
| Medication | Clinical | ✅ | 7 | No |
| Provenance | Clinical | ✅ | 7 | No |
| Location | Administrative | ✅ | 14 | No |
| Organization | Administrative | ✅ | 13 | No |
| Practitioner | Administrative | ✅ | 13 | No |
| PractitionerRole | Administrative | ✅ | 11 | No |
| VisionPrescription | Clinical | ❌ | 11 | No |
| Media | Clinical | ❌ | 14 | No |
| Claim | Financial | ❌ | 15 | No |
| Coverage | Financial | ❌ | 14 | No |
| ExplanationOfBenefit | Financial | ❌ | 14 | No |

**No field counts are possible** because the FHIR resource definitions are standard (defined by the FHIR spec, not by the vendor). No custom profiles, extensions, or data dictionaries exist.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

Moyae provides no vendor-specific categorization or documentation of export content. The export is defined entirely by reference to the FHIR R4 specification.

**What's definitely there** (based on US Core profile declarations): Standard clinical summary data — demographics, conditions, medications, allergies, immunizations, vitals, lab results, procedures, encounters, care plans, goals, implantable devices, clinical notes/documents. This is the USCDI data set, which represents a clinical summary.

**What's unclear**: Whether the remaining 126 resource types without US Core profiles contain any data. The server supports them mechanically, but there's no evidence any are populated. Key uncertain resources include:
- Financial types (Claim, Coverage, ExplanationOfBenefit, ChargeItem, etc.) — billing data may live in AdvancedMD, not Moyae
- VisionPrescription — relevant to an ophthalmology EHR but has no US Core profile
- Media — could contain retina drawings but undocumented
- Observation extensions — IOP, visual acuity, and refraction could be Observations, but no custom profiles document how

**What's almost certainly missing**: Ophthalmology-specific clinical data. IOP measurement series, intravitreal injection histories, anterior/posterior segment findings, refraction data, and retina drawings are core to what Moyae stores, but:
- No FHIR profiles or extensions document how they're represented
- Standard FHIR Observation could theoretically carry IOP and visual acuity, but without coded value documentation, a recipient can't interpret the data
- Retina drawings would need Media or Binary resources, but these aren't profiled
- There is no evidence anywhere in the documentation that ophthalmology-specific data is included in the export

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | Patient (US Core profile, 23 search params) | Adequate per USCDI |
| Encounters / visits | ✅ Covered | Encounter (US Core profile, 22 search params) | Adequate per USCDI |
| Problems / conditions / diagnoses | ✅ Covered | Condition (US Core profile, 22 search params) | Adequate per USCDI |
| Medications / prescriptions | ✅ Covered | MedicationRequest, Medication (US Core profiles) | Adequate per USCDI |
| Allergies | ✅ Covered | AllergyIntolerance (US Core profile) | Adequate per USCDI |
| Immunizations | ✅ Covered | Immunization (US Core profile) | Adequate per USCDI |
| Vitals | ✅ Covered | Observation (6 US Core profiles including pulse oximetry) | Adequate per USCDI |
| Lab results | ⚠️ Partial | DiagnosticReport, Observation (US Core lab profiles) | Product not certified for lab ordering (a)(2); limited lab data expected |
| Imaging / diagnostic reports | ⚠️ Partial | DiagnosticReport (US Core note profile), ImagingStudy (no profile) | Product orders imaging (a)(3) but doesn't store images; unclear if imaging orders appear in export |
| Procedures | ✅ Covered | Procedure (US Core profile) | Adequate per USCDI |
| Clinical notes / documents | ✅ Covered | DocumentReference (US Core profile); C-CDA sample has notes sections | Adequate per USCDI |
| Care plans / goals | ✅ Covered | CarePlan, Goal (US Core profiles) | Adequate per USCDI |
| Orders / referrals | ⚠️ Partial | ServiceRequest exists but no profile; no referral-specific documentation | Product handles imaging orders; representation unclear |
| Insurance / coverage | ⚠️ Partial | Coverage resource supported, no profile | Likely stored in AdvancedMD; may not be populated in Moyae |
| Claims / billing | ⚠️ Partial | Claim, ExplanationOfBenefit resources supported, no profiles | Moyae partners with AdvancedMD for billing; billing data likely NOT in Moyae's FHIR server |
| Payments | ⚠️ Partial | PaymentNotice, PaymentReconciliation supported, no profiles | Same as billing — likely in AdvancedMD |
| Consents / directives | ⚠️ Partial | Consent resource supported, no profile | Unknown if populated |
| Patient communications / portal messages | N/A | No patient portal; not certified for (e)(1) | Product doesn't have patient portal |
| Specialty: Ophthalmology (IOP, visual acuity, refraction, retina drawings, injections) | ❌ Not covered | No custom profiles, extensions, or documentation for any ophthalmology-specific data | **Critical gap**: This is the core clinical data the product stores. No evidence it is included in the FHIR export. |

## 6. Documentation Quality

The documentation is **extremely sparse**. Quantitatively:

- **Endpoints documented**: 954 API endpoints exist; **2** have any description text (0.2%)
- **Response examples**: **1** of 954 endpoints has a response example (the C-CDA endpoint)
- **Data dictionary**: None
- **Custom profiles/extensions**: None
- **Value sets**: None
- **Export user guide**: None
- **Sample export data**: None
- **Relationship documentation**: None

A developer receiving a Moyae EHI export would have:
1. Standard FHIR R4 resources in NDJSON format — parseable using any FHIR library
2. US Core profiles on 20 resource types — interpretable using standard US Core documentation
3. **Zero** vendor-specific guidance on how ophthalmology data is encoded, which resources are populated, what extensions exist, or how to interpret specialty-specific observations

For standard clinical summary data (demographics, conditions, medications, etc.), a developer could reconstruct a basic patient record using FHIR knowledge alone. For ophthalmology-specific data — the product's primary differentiator and the most valuable clinical data it stores — the documentation provides no help whatsoever.

The disclosures page's single-line description ("New-line delimited JSON export of FHIR data") and the bare Postman collection (URLs and HTTP methods only) are the minimum possible compliance artifacts.

## 7. Overall Assessment

### Classification

**Standard-based projection**

Moyae's EHI export is its FHIR Bulk Data `$export` endpoint — the same mechanism used for (g)(10) API access — relabeled as the (b)(10) EHI export. The FHIR server mechanically supports 146 resource types (essentially the entire FHIR R4 spec), but the only resources with evidence of actual data population are the 20 with US Core profiles, which correspond exactly to the USCDI clinical summary data set.

This is a textbook example of failure mode #1 described in the assessment framework: **FHIR API repackaging**. The vendor points to their existing FHIR $export endpoint and calls it "(b)(10)." The clinical summary data (demographics, conditions, medications, etc.) is likely present, but the product's core ophthalmology-specific data — IOP measurements, visual acuity, refraction, retina drawings, intravitreal injection histories — has no documented representation in the FHIR export and no custom profiles or extensions to support it.

### Key Findings

1. **The export is the (g)(10) FHIR API relabeled as (b)(10).** The 20 US Core-profiled resources match the USCDI data set exactly. The remaining 126 resource types appear to be a generic FHIR server supporting the full spec mechanically, with no evidence of data population.

2. **Ophthalmology-specific clinical data is undocumented in the export.** Moyae's core value proposition — IOP tracking, intravitreal injection series, retina drawings, refraction data, anterior/posterior segment findings — has no FHIR profiles, extensions, or documentation. Standard FHIR R4 has no native structures for most of these, so custom extensions would be required. None exist.

3. **Documentation is among the thinnest possible.** One sentence on the disclosures page plus a Postman collection with URLs but no descriptions, no examples, and no field documentation. 2 of 954 endpoints have any description text.

4. **Billing/scheduling data is likely out of scope.** Moyae partners with AdvancedMD for billing, scheduling, and practice management. Financial FHIR resources exist in the server but are likely empty. This is a legitimate architectural choice rather than a coverage gap, but it means a complete patient record requires data from both systems.

5. **The C-CDA sample confirms standard clinical content only.** The one available data sample (Alice Newman's C-CDA) contains 23 sections of standard clinical summary data — allergies, medications, problems, vitals, etc. — with no ophthalmology-specific content.

### Summary Stats

```
Classification:  Standard-based projection
Export format:   FHIR R4 NDJSON (via Bulk Data $export)
Model type:      Standard projection (FHIR R4 / US Core)
Entities:        146 resource types declared; 20 with US Core profiles (evidence of population)
Fields:          N/A (standard FHIR resources; no custom profiles or extensions)
Descriptions:    0% (no field-level documentation; 2 of 954 endpoints have any description)
Sample data:     No (1 C-CDA sample only; no FHIR NDJSON sample)
Bulk export:     Yes (system-level $export)
Domains covered: 10 of 15 applicable domains (standard clinical only; ophthalmology specialty data not covered)
```

### Bottom Line

Moyae's EHI export provides standard USCDI clinical summary data via FHIR Bulk Data — adequate for basic demographics, conditions, medications, and vitals, but fundamentally missing the ophthalmology-specific data that is the product's entire reason for existence. A patient exported from Moyae would get a generic clinical summary but lose their IOP measurement history, intravitreal injection records, retina drawings, refraction data, and specialty examination findings. The documentation is minimal to the point of being effectively absent.
