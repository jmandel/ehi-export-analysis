# EHI Export Analysis: Sai Systems Digital LLC

**Product**: PacEHR v20
**Analysis date**: 2026-02-16
**CHPL IDs**: 15.04.04.3137.Pace.20.00.1.221229

## 1. Product Context

PacEHR is a cloud-based EHR designed specifically for Post-Acute Long-Term Care (PALTC) practitioners — physicians, NPs, and clinicians who provide bedside care in skilled nursing facilities (SNFs), assisted living, rehabilitation centers, and home health settings. It is part of the "TheSNFist Suite" by Saisystems Health (a division of Saisystems International, Inc., Shelton, CT). PacEHR was launched in 2021 and targets mobile clinicians who visit multiple facilities, not the facilities themselves (which typically use PointClickCare).

**Core data the product stores** (relevant to export completeness):
- **Clinical encounter documentation**: Template-driven notes with voice-to-text, pre-populated past patient data — this is PacEHR's primary function
- **Billing/coding data**: Integrated billing, charge capture via companion app billEHR, coding recommendations, claims management
- **Medications/CPOE**: Certified for (a)(1) CPOE for medications, e-prescribing
- **Demographics**: Certified for (a)(5)
- **Implantable devices**: Certified for (a)(14)
- **Transitions of care**: C-CDA exchange via (b)(1), Direct messaging via (h)(1)
- **Quality measures**: Certified for (c)(1), MIPS/CCM reporting
- **Scheduling**: Appointment scheduling listed as a feature
- **Document management**: Listed as a feature
- **Patient portal**: Listed on review sites (messaging, appointment scheduling)

**Not expected** (or limited): Lab orders/results (not certified for (a)(2)/(a)(3); a user review noted inability to add lab values), imaging orders, vitals (facility EHR typically handles these). The product is not the facility's system of record — it's the visiting practitioner's documentation and billing tool.

## 2. Artifacts Reviewed

| Artifact | Description | Informative? |
|---|---|---|
| `pacehr-ehi-main-page.html` (139,585 bytes) | Main EHI export page at saisystems.com/health/pacehr-ehi/. Contains ~370 words of substantive content: EHI definition, two use cases (bulk and single-patient), export format claim ("machine readable XML formats"), and link to FHIR API docs. **No data dictionary, no schema, no sample data, no export instructions.** | Low — establishes vendor claims but provides no technical detail |
| `cures-update-fhir-api-docs.html` (189,075 bytes) | FHIR API documentation at thesnfist.com/cures-update/. Documents 16 standard US Core/USCDI FHIR resources with 29 API endpoints. Also contains Drummond certification disclosure and API Terms of Service. This is (g)(10) standardized API documentation. | Medium — provides the only technical substance, but documents (g)(10) not (b)(10) |
| `compliance-certificate-pacehr-v20.pdf` (265,896 bytes, 1 page) | Drummond Group ONC Health IT compliance certificate confirming certification of PacEHR v20 for criteria including (b)(10). Dated 12/29/2022. | Low — confirms certification but says nothing about export content |
| `screenshot-ehi-main-page.png` (651,704 bytes) | Screenshot of the EHI main page | Low — confirms page renders as expected |
| `screenshot-cures-update-fhir-api-docs.png` (3,488,686 bytes) | Screenshot of the FHIR API docs page | Low — confirms page renders as expected |

**Verification**: The live EHI page (checked 2026-02-16) is identical to the downloaded artifact (same file size: 139,585 bytes, same content). No changes since collection on 2026-02-14.

## 3. Export Mechanics

- **Format**: The EHI page claims "machine readable XML formats." The linked FHIR API documentation specifies `application/fhir+json`. These appear contradictory — the EHI page says XML, but the API docs say JSON.
- **Mechanism**: The only documented technical mechanism is the FHIR API ("FHIR Server 1.0.0 for Cures Act Update"). The EHI page also mentions "HL7, or native web service APIs" as integration options but provides no documentation for these alternatives.
- **Single-patient vs bulk**: The EHI page describes both: "Bulk EHI export enables export of all patient data belonging to a practice, provider, medical group, or department" and "Single/multi-patient export is useful when patients request their health information." However, no instructions or screenshots show how to perform either type.
- **Access**: The page states customers should "reach out to their dedicated Customer Success Manager" for integration details. No self-service export interface is documented.

## 4. Export Content: What's In It

### What the documentation provides

The only technical documentation of export content is the FHIR API page, which documents **16 standard FHIR resources** mapped to **68 USCDI data elements** across **29 API endpoints**. These are entirely standard US Core / USCDI v1/v2 resources with no vendor-specific extensions or custom resources.

There is **no data dictionary**, **no field-level documentation** beyond USCDI element names, **no schema files**, **no sample data**, and **no documentation of any data outside the USCDI clinical scope**.

### Vendor's own content organization

The vendor does not organize the export content into categories. The FHIR API documentation lists resources in alphabetical order. Below is the complete inventory of documented resources:

| FHIR Resource | USCDI Elements | USCDI Version | Search Parameters |
|---|---|---|---|
| AllergyIntolerance | 3 | v1 | patient, date |
| CarePlan | 1 | v1 | patient, date, status |
| CareTeam | 5 | v2 | patient, date, status |
| Condition | 2 | v1 | patient |
| Device | 1 | v1 | patient |
| DocumentReference | 8 | v1 | patient, period, status |
| Encounter | 5 | v2 | patient, id |
| Goal | 1 | v1 | patient, target |
| Immunization | 1 | v1 | patient, date |
| Location | 4 | v1 | — |
| Medication | 1 | v1 | — |
| MedicationRequest | 1 | v1 | Patient |
| Observation | 15 | v1 | patient, date |
| Patient | 14 | v1/v2 | 15 params (id, identifier, name, family, given, gender, birthdate, deceased, death-date, email, phone, address-city, -state, -postalcode, -country) |
| Practitioner | 5 | v1 | — |
| Procedure | 1 | v1 | patient, date |
| **Total** | **68** | | |

The full inventory is in `analysis/full-entity-inventory.json` with all 68 USCDI elements enumerated per resource.

### What's notably absent

There is **zero documentation** of any data outside the standard USCDI/US Core scope:
- No billing codes, charges, claims, or payment data
- No encounter templates, macros, or custom clinical forms
- No scheduling or appointment data
- No document management metadata
- No patient portal messages or communications
- No quality measure / MIPS data
- No facility census or practice management data
- No coding recommendations or AI-generated suggestions

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor's export documentation covers exactly one thing: the standard FHIR API per (g)(10). The documented resources map to standard USCDI clinical data classes — demographics, allergies, conditions, medications, immunizations, vitals, labs, procedures, clinical notes (as C-CDA documents), care plans, goals, encounters, care teams, devices, practitioners, and locations.

The documentation does not use any vendor-specific categories. The 16 resources documented are the exact set required by (g)(10) with no additions. The Observation resource is the richest (15 USCDI elements covering labs and vitals), followed by Patient (14 elements covering demographics). Most clinical resources have just 1-2 elements documented at the USCDI data class level, not at the field level.

The EHI page's own definition of EHI explicitly lists "billing records" and "enrollment, payment, claims adjudication" as EHI — but the technical documentation provides no mechanism to export any of this data.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | `Patient` resource (14 USCDI elements: name, DOB, sex, race, ethnicity, language, address, phone) | Standard USCDI demographics only; no insurance/coverage info, no facility affiliations |
| Encounters / visits | ⚠️ Partial | `Encounter` resource (5 USCDI v2 elements: type, diagnosis, time, location, disposition) | Basic encounter metadata; does not include the rich template-driven encounter documentation that is PacEHR's core function |
| Problems / conditions | ⚠️ Partial | `Condition` resource (2 elements: Health Concern, Problems) | Standard coded conditions only; no native problem list detail |
| Medications / prescriptions | ⚠️ Partial | `Medication` + `MedicationRequest` (1 element each) | Standard FHIR medication resources; no CPOE order detail, no e-prescribing metadata |
| Allergies | ⚠️ Partial | `AllergyIntolerance` (3 elements: substance drug class, substance medication, reaction) | Standard USCDI allergy data |
| Immunizations | ⚠️ Partial | `Immunization` (1 element) | Standard USCDI |
| Vitals | ⚠️ Partial | `Observation` (12 vital sign elements) | Standard USCDI vitals; PacEHR may have limited vitals data as facility EHR typically captures these |
| Lab results | ⚠️ Partial | `Observation` (2 lab elements: tests, values/results) | Standard USCDI; PacEHR not certified for lab CPOE, so lab data may be minimal |
| Imaging / diagnostic reports | ⚠️ Partial | `DocumentReference` includes "Imaging Narrative" as a note type | No dedicated imaging resource; product doesn't appear to handle imaging orders |
| Procedures | ⚠️ Partial | `Procedure` (1 element) | Minimal — just coded procedure reference |
| Clinical notes / documents | ⚠️ Partial | `DocumentReference` (8 C-CDA note types) + `CarePlan` (1 element) | C-CDA clinical documents are standardized summaries; **PacEHR's core value is its native template-driven encounter notes, which are not represented in the FHIR export** |
| Care plans / goals | ⚠️ Partial | `CarePlan` (1 element) + `Goal` (1 element) | Minimal USCDI representation |
| Orders / referrals | ❌ Not covered | No Order or ReferralRequest resources | Product handles CPOE for medications; no order data in export |
| Insurance / coverage | ❌ Not covered | No Coverage or InsurancePlan resources | Product stores patient insurance for billing; significant gap |
| Claims / billing | ❌ Not covered | No Claim, ChargeItem, or billing resources | **Product has integrated billing, charge capture (billEHR), and claims management — this is a core function; significant gap** |
| Payments | ❌ Not covered | No Payment resources | If product processes payments via RCM, this is a gap |
| Consents / directives | ❌ Not covered | No Consent resources | Unclear if product stores consent data |
| Patient communications | ❌ Not covered | No Communication resources | Product has patient portal and SNFConnect; gap if messages are stored |
| Specialty-specific (PALTC) | ❌ Not covered | No PALTC-specific data elements or resources | **PacEHR is purpose-built for PALTC with specialty-specific templates, census management, facility-level documentation — none of this appears in the export** |

## 6. Documentation Quality

The EHI export documentation is **extremely thin** — among the thinnest possible while having a page at the registered URL.

- **EHI page**: ~370 words of substantive content. Explains what EHI is (copying the regulatory definition), describes two use cases (bulk and single-patient), and states the format is "machine readable XML." Provides no technical guidance whatsoever.
- **FHIR API page**: More substantial (~814 text fragments) but is standard (g)(10) API documentation, not (b)(10)-specific. Lists FHIR resource endpoints, search parameters, and USCDI element mappings. Includes API Terms of Service dated December 23, 2022.
- **No data dictionary**: Not at the field level, not at the entity level. The only "documentation" of export content is the USCDI data element list per FHIR resource.
- **No machine-readable schemas**: No JSON Schema, no XSD, no OpenAPI spec.
- **No sample data**: No example exports, no sample FHIR bundles.
- **No export instructions**: No step-by-step guide, no screenshots of UI.
- **Format contradiction**: The EHI page says "XML formats" while the FHIR API says `application/fhir+json`.

A developer could not build a meaningful import from this documentation alone. They could call the FHIR API to get standard USCDI data, but that is (g)(10) functionality, not a comprehensive EHI export. The documentation provides no information about how to obtain billing data, native clinical notes, scheduling data, or any other vendor-specific content.

## 7. Overall Assessment

### Classification

**Standard-based projection**: The export is the vendor's (g)(10) FHIR API repackaged as a (b)(10) EHI export. It covers standard USCDI clinical data (approximately 16 FHIR resources, 68 USCDI data elements) but omits billing, native clinical documentation, scheduling, and specialty-specific PALTC data that PacEHR stores.

### Key Findings

1. **Textbook FHIR/(g)(10) repackaging as (b)(10)**: The EHI export page links directly to the (g)(10) FHIR API documentation as the export mechanism. The 16 documented resources are exactly the standard US Core/USCDI set with zero vendor-specific extensions. The FHIR API is titled "FHIR Server 1.0.0 for Cures Act Update" — it is the standardized API, not an EHI export tool.

2. **Billing data completely absent**: PacEHR has integrated billing, the billEHR charge capture app, and claims management as core product features. The vendor's own EHI page defines EHI as including "billing records" and "enrollment, payment, claims adjudication." Yet no billing data appears in the documented export — a direct contradiction between what the vendor says EHI is and what they actually export.

3. **Native clinical documentation missing**: PacEHR's primary value proposition is its template-driven encounter documentation with voice-to-text. The FHIR API only exposes clinical notes as C-CDA documents (via DocumentReference), which are standardized summaries — the native encounter structure, templates, and macros are not represented.

4. **Documentation is near-empty**: The EHI-specific documentation consists of ~370 words of prose with no data dictionary, no schema, no sample data, and no export instructions. This is a compliance stub, not functional documentation.

5. **PALTC specialty data absent**: Despite being purpose-built for post-acute/long-term care with features like facility census management and PALTC-specific templates, no specialty-specific data appears in the export.

### Summary Stats

    Classification:  Standard-based projection
    Export format:   FHIR JSON (claimed "XML" on EHI page, but API docs specify application/fhir+json)
    Model type:      Standard projection (US Core / USCDI v1/v2)
    Entities:        16 FHIR resources
    Fields:          68 USCDI data elements (not field-level)
    Descriptions:    0% (USCDI element names only, no field-level descriptions)
    Sample data:     No
    Bulk export:     Claimed but undocumented
    Domains covered: 0 of 13 fully covered; 11 partially via FHIR; 6 not covered at all

### Bottom Line

PacEHR's EHI export is its (g)(10) FHIR API relabeled as (b)(10). A patient or provider would get standard USCDI clinical data (demographics, conditions, medications, vitals, notes-as-C-CDA) but would miss billing/charge capture data, native encounter documentation, and PALTC-specific clinical data — all core functions of the product. The single biggest gap is the complete absence of billing data despite the vendor's own EHI definition explicitly including it.
