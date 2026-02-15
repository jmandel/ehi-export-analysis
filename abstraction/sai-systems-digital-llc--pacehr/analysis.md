# EHI Export Analysis: Sai Systems Digital LLC

**Product**: PacEHR v20
**Analysis date**: 2026-02-15
**CHPL ID**: 15.04.04.3137.Pace.20.00.1.221229

## 1. Product Context

PacEHR is a cloud-based EHR designed specifically for Post-Acute Long-Term Care (PALTC) practitioners — physicians, nurse practitioners, and APRNs who provide bedside care in skilled nursing facilities (SNFs), assisted living, rehabilitation centers, and home health settings. It is developed by Saisystems International (branded as Saisystems Health), headquartered in Shelton, Connecticut. The product was launched in 2021 and targets mobile clinicians who visit multiple facilities.

PacEHR is part of the "TheSNFist® Suite" which bundles the EHR with billEHR® (charge capture), SNFConnect (communications), navigatEHR (business intelligence), and managed services for RCM, coding/billing, and payor enrollment.

**Key data domains PacEHR stores** (relevant to export completeness):
- **Clinical encounter documentation** — the product's core function: template-driven encounter notes with voice-to-text, macros, and pre-populated data from prior visits
- **Medications / e-prescribing** — CPOE for medications, certified for (a)(1)
- **Demographics** — patient demographics, certified for (a)(5)
- **Implantable devices** — certified for (a)(14)
- **Billing and coding** — integrated encounter billing, charge capture (billEHR), claims management, coding suggestions
- **Transitions of care** — C-CDA document exchange, certified for (b)(1)
- **Clinical quality measures** — MIPS/CCM reporting, certified for (c)(1)
- **Patient portal** — listed as a feature (scheduling, messaging, records access)
- **Document management** — listed as a feature on review sites

**Architectural note**: PacEHR serves the visiting practitioner, not the SNF facility itself (which typically runs PointClickCare). PacEHR stores the practitioner's encounter documentation and billing — not the facility's nursing notes, vitals, or medication administration records. This narrows the expected EHI scope but still includes all data the practitioner generates about patients.

**Not certified for**: (a)(2) CPOE for lab orders, (a)(3) CPOE for imaging, (a)(4) vital signs, (a)(6) problem list, (a)(7) medication list, (a)(8) allergy list, (e)(1) view-download-transmit. This suggests limited lab, imaging, and vitals data originating in PacEHR (though these may be pulled from the facility EHR via integration).

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `pacehr-ehi-main-page.html` (136 KB) | Main EHI export page at saisystems.com/health/pacehr-ehi/. ~362 words of substantive content describing EHI export capability. No data dictionary, schema, sample data, or field-level documentation. | Low — describes concept of EHI but provides no technical detail about what is actually exported |
| `cures-update-fhir-api-docs.html` (185 KB) | FHIR API documentation at thesnfist.com/cures-update/. Documents 16 FHIR STU3 resource endpoints with search parameters. This is (g)(10) standardized API documentation, not (b)(10)-specific. | Moderate — shows what clinical data is available via FHIR API, but this is standard USCDI data, not comprehensive EHI |
| `compliance-certificate-pacehr-v20.pdf` (1 page, 260 KB) | Drummond Group ONC certification compliance certificate. Confirms (b)(10) certification. | Low — confirms certification but provides no export detail |
| `screenshot-ehi-main-page.png` (637 KB) | Screenshot of the EHI export page | Minimal — visual confirmation of page content |
| `screenshot-cures-update-fhir-api-docs.png` (3.4 MB) | Screenshot of the FHIR API documentation page | Minimal — visual confirmation of page content |

**Most informative artifact**: `cures-update-fhir-api-docs.html` — it is the only artifact with any technical specificity (FHIR resource types, search parameters, USCDI data element mappings).

**Verification**: The live EHI page at https://saisystems.com/health/pacehr-ehi/ was checked on 2026-02-15 and returns HTTP 200 with content identical to the collected artifact. No additional documentation, data dictionary, or schema files have been added since collection.

## 3. Export Mechanics

- **Format**: Described as "machine readable XML formats" on the EHI page. The linked FHIR API documentation specifies `application/fhir+json` as the accepted format. These may refer to different mechanisms (C-CDA XML vs. FHIR JSON) or may be inconsistent documentation.
- **Mechanism**: The only documented technical mechanism is the FHIR API (endpoint documentation at thesnfist.com/cures-update/). The EHI page also mentions "HL7, or native web service APIs" but provides no documentation for these.
- **Single-patient vs bulk**: The EHI page describes both "bulk EHI export" (all patients for a practice/provider/department) and "single/multi-patient export." However, no technical instructions are provided for either.
- **Access**: The page directs customers to "reach out to their dedicated Customer Success Manager" for integration details. No self-service export button, API keys, or automated process is documented.
- **Fees**: Not mentioned.

## 4. Export Content: What's In It

### What the documentation actually provides

The EHI export documentation consists of a single narrative webpage (~362 words) that:
1. Defines EHI by citing the HIPAA Designated Record Set
2. Describes two use cases (bulk and single/multi-patient)
3. States the export is in "machine readable XML formats"
4. Links to the FHIR API documentation

**There is no data dictionary.** No tables, no fields, no types, no descriptions, no relationships, no value sets, no sample data.

### FHIR API documentation (the only technical content)

The linked FHIR API documentation covers 16 standard FHIR STU3 US Core resource types:

| FHIR Resource | USCDI Data Elements | Search Parameters |
|---|---|---|
| AllergyIntolerance | Substance (Drug Class, Medication), Reaction | patient, date |
| CarePlan | Assessment and Plan of Treatment | patient, date, status |
| CareTeam | Care Team (v1); Member Name, Identifier, Role, Location, Telecom (v2) | patient, date, status |
| Condition | Health Concern, Problems | patient |
| Device | Unique Device Identifier(s) for Implantable Devices | patient |
| DocumentReference | C-CDA documents | patient, period, status |
| Encounter | (not specified) | patient, id |
| Goal | (not specified) | patient, id |
| Immunization | (not specified) | patient, date |
| Location | (not specified) | id |
| Medication | (not specified) | id |
| MedicationRequest | (not specified) | patient |
| Observation | (labs, vitals, smoking status — implied by USCDI) | patient, date |
| Patient | Suffix, Sex, Date of Birth, Race, Ethnicity, Preferred Language, Address, Phone Number, Sexual Orientation (v2), Gender Identity (v2) | id, identifier, name, family, given, gender, birthdate, and 8 others |
| Practitioner | (not specified) | id |
| Procedure | (not specified) | patient, date |

This is the standard US Core / USCDI v1/v2 resource set — identical to what any (g)(10)-certified product would expose. There are no vendor-specific extensions, no custom resources, and no documentation of data beyond what USCDI requires.

### Vendor's own content organization

The vendor does not organize its export by data categories. There is no data dictionary to present. The only structure comes from the FHIR resource types listed above, which are standard FHIR categories, not vendor-specific.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor provides exactly one layer of documentation: a standard FHIR API covering 16 US Core resource types. This represents the (g)(10) standardized API for patient access and population-level data — not a comprehensive (b)(10) EHI export.

The EHI page *claims* the export includes "medical records and billing records" and "enrollment, payment, claims adjudication" data (quoting the HIPAA Designated Record Set definition), but no billing, claims, or payment data appears anywhere in the FHIR API documentation. The only technical specificity provided contradicts the marketing text.

There are zero vendor-specific data elements documented. Nothing about PacEHR's template-driven encounter notes, coding suggestions, charge capture data, practice configuration, or any other product-specific data.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | `Patient` FHIR resource with USCDI v1/v2 elements (name, DOB, sex, race, ethnicity, language, address, phone) | Standard USCDI demographics only; no vendor-specific demographic fields documented |
| Encounters / visits | ⚠️ Partial | `Encounter` FHIR resource (search by patient/id only) | No documentation of encounter content/structure; PacEHR's core workflow is encounter documentation — this is critically thin |
| Problems / conditions | ⚠️ Partial | `Condition` FHIR resource with Health Concern and Problems | Standard USCDI; may be adequate if PacEHR pulls problem lists from facility EHR |
| Medications / prescriptions | ⚠️ Partial | `Medication` + `MedicationRequest` FHIR resources | Standard USCDI; PacEHR is certified for CPOE (a)(1) so stores medication orders |
| Allergies | ⚠️ Partial | `AllergyIntolerance` FHIR resource (substance, reaction) | Standard USCDI only |
| Immunizations | ⚠️ Partial | `Immunization` FHIR resource | Standard USCDI only |
| Vitals | ⚠️ Partial | `Observation` FHIR resource (implied by USCDI) | PacEHR not certified for (a)(4) vitals; may pull from facility EHR |
| Lab results | ⚠️ Partial | `Observation` FHIR resource (implied by USCDI) | PacEHR not certified for lab CPOE; limited originating lab data expected |
| Imaging / diagnostic reports | ❌ Not covered | No imaging FHIR resources documented | PacEHR not certified for imaging CPOE; likely N/A |
| Procedures | ⚠️ Partial | `Procedure` FHIR resource | Standard USCDI only |
| Clinical notes / documents | ⚠️ Partial | `DocumentReference` FHIR resource (C-CDA documents) | C-CDA summaries only — does **not** capture PacEHR's native template-driven encounter notes, macros, or voice-to-text documentation. This is PacEHR's core product function and a significant gap. |
| Care plans / goals | ⚠️ Partial | `CarePlan` + `Goal` FHIR resources | Standard USCDI only |
| Orders / referrals | ❌ Not covered | No referral resources documented | Unknown if PacEHR stores referral data |
| Insurance / coverage | ❌ Not covered | No insurance/coverage data in FHIR API | PacEHR integrates with billing; insurance data likely stored |
| Claims / billing | ❌ Not covered | No billing, claims, or charge data documented | PacEHR has integrated billing, charge capture (billEHR), and claims management. The EHI page itself cites "billing records" and "claims adjudication" as part of EHI. **Significant gap.** |
| Payments | ❌ Not covered | No payment data documented | RCM services are part of the suite; payment data likely exists |
| Consents / directives | ❌ Not covered | No consent resources documented | Unknown if stored |
| Patient communications | ❌ Not covered | No messaging/portal data documented | Patient portal and SNFConnect are product features |
| Specialty-specific (PALTC) | ❌ Not covered | No PALTC-specific data documented | PacEHR is purpose-built for PALTC with specialty-specific templates, census management, and multi-facility workflows. None of this is in the export. **Major gap.** |

## 6. Documentation Quality

The EHI export documentation is **extremely thin** — among the most minimal possible while still having a page at the registered URL.

- **No data dictionary**: Zero field-level documentation. No tables, entities, or schemas.
- **No sample data**: No example exports, no screenshots of export output.
- **No export instructions**: No step-by-step process for performing an export. Users are directed to contact their Customer Success Manager.
- **No machine-readable artifacts**: No XSD, JSON Schema, CSV templates, or any other parseable format.
- **Contradictory format claims**: The EHI page says "XML formats" while the FHIR API accepts `application/fhir+json`.
- **The only technical documentation is the (g)(10) FHIR API**: This is standard API documentation for the Cures Act update, not (b)(10)-specific documentation. It covers 16 US Core resources — a standard clinical data projection, not a comprehensive EHI export.

A developer reading this documentation would be able to call a standard FHIR API for USCDI clinical data. They would have **no way** to obtain a complete export of all data PacEHR stores — encounter notes in their native format, billing codes, charge capture data, claims, insurance information, practice census, patient communications, or any PALTC-specific data.

## 7. Overall Assessment

### Classification

**Standard-based projection**: The EHI export documentation points exclusively to a standard FHIR STU3 API covering 16 US Core resources. This is the (g)(10) standardized API being repackaged as the (b)(10) EHI export. It covers a standard clinical summary — approximately the USCDI v1/v2 data set — but omits billing, specialty clinical data, native encounter documentation, and all vendor-specific data domains.

### Key Findings

1. **Classic (g)(10) → (b)(10) repackaging**: The EHI export page links directly to the FHIR API documentation as its sole technical reference. The 16 documented FHIR resources are the standard US Core / USCDI set — identical to what any (g)(10)-certified product exposes. No additional (b)(10)-specific data is documented. (`pacehr-ehi-main-page.html`, `cures-update-fhir-api-docs.html`)

2. **No data dictionary or schema of any kind**: Across all 5 collected artifacts, there is zero field-level documentation of what data the export contains. No tables, no entities, no field names, no types, no relationships. (`files.json`, all artifacts reviewed)

3. **Core product data missing from export**: PacEHR's primary value is template-driven PALTC encounter documentation with voice-to-text and customizable macros. None of this native encounter data structure appears in the FHIR API — only standardized C-CDA document references. (`cures-update-fhir-api-docs.html` — DocumentReference endpoint)

4. **Billing and claims data absent despite being cited in EHI definition**: The vendor's own EHI page defines EHI as including "billing records" and "claims adjudication" data, yet no billing, claims, charge capture, or payment data appears in the FHIR API documentation. PacEHR includes integrated billing and the billEHR charge capture app. (`pacehr-ehi-main-page.html`)

5. **~362 words of substantive EHI documentation total**: The entire EHI-specific content is a brief marketing-style description of EHI concepts with no technical substance. (Verified by text extraction from `pacehr-ehi-main-page.html`)

### Summary Stats

```
Classification:  Standard-based projection
Export format:   FHIR STU3 JSON (documented) / XML (claimed on EHI page)
Model type:      Standard projection (US Core / USCDI)
Entities:        16 FHIR resource types
Fields:          N/A (no field-level documentation)
Descriptions:    N/A (no data dictionary)
Sample data:     No
Bulk export:     Claimed (text says "bulk EHI export") but no technical documentation
Domains covered: 0 of 13 fully covered; 10 of 13 partially via standard FHIR; 3 not covered at all
```

### Bottom Line

PacEHR's EHI export is a standard FHIR API relabeled as a (b)(10) export, with no data dictionary, no schema, and no documentation of the product's native data model. A patient or provider would receive a USCDI clinical summary — standard demographics, conditions, medications, and C-CDA documents — but would miss PacEHR's native encounter documentation, billing/charge capture data, claims, insurance information, and all PALTC-specific clinical data that the product is purpose-built to manage. The single biggest gap is the absence of native encounter documentation, which is the product's core function.
