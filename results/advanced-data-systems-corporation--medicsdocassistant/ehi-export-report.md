# Advanced Data Systems Corporation — EHI Export Documentation

Collected: 2026-02-15

## Source
- Registered URL: https://apps.medicscloud.com/B10_MedicsDocAssistant.html
- CHPL ID: 10785
- CHPL Product Number: 15.02.05.1044.AVDD.01.01.1.220111
- Product: MedicsDocAssistant, Version 8.0
- Certification Date: 2022-01-11

## Navigation Journal

### 1. Initial probe of the registered URL

```bash
curl -sI -L "https://apps.medicscloud.com/B10_MedicsDocAssistant.html" -H 'User-Agent: Mozilla/5.0'
```

HTTP/2 200, Content-Type: text/html, Content-Length: 2375. A very small static HTML page.

### 2. Fetched and examined the page

```bash
curl -sL "https://apps.medicscloud.com/B10_MedicsDocAssistant.html" -H 'User-Agent: Mozilla/5.0' -o downloads/B10_MedicsDocAssistant.html
```

The entire page is a single paragraph stating:

> "MedicsDocAssistant authorized users can generate the Electronic Health Information Export (EHI) for a single patient and also the patient population in both HL7 CCDA xml format that comply with USCDI v1 requirements standards and HL7 FHIR v 4.0.1 US Core v 3.1.1."

Two links are provided, both to external HL7 standards:
1. HL7 CCDA XML Implementation Guide: https://www.hl7.org/implement/standards/product_brief.cfm?product_id=492
2. HL7 FHIR US Core IG STU3.1.1: https://hl7.org/fhir/us/core/STU3.1.1/

No vendor-specific documentation, data dictionary, schema, sample data, or export instructions are linked from this page.

### 3. Explored the vendor domain for additional docs

Checked adjacent paths on apps.medicscloud.com:
- `B10_MedicsCloud.html` → 200 (identical B10 page for MedicsCloud v11.0, the sibling product)
- `B10_MedicsCloudEHR.html`, `B10.html`, `EHI_Export.html`, `b10.html`, `ehi-export.html` → all 404
- `fhir/` → 301 → 403 (forbidden; not a public FHIR endpoint)
- `fhir/r4`, `api-docs`, `swagger`, `docs`, `data-dictionary` → all 404
- `robots.txt`, `sitemap.xml` → 404
- `.well-known/smart-configuration`, `fhir/metadata` → 404

Domain root (apps.medicscloud.com/) redirects to adsc.com.

### 4. Checked the mandatory disclosures page

```bash
# Navigated in browser (page requires JavaScript / HubSpot rendering)
https://www.adsc.com/onc-acb-health-it-certification-program-medicsdocassistant
```

The page lists certification criteria and CQMs for MedicsDocAssistant v8.0. 170.315(b)(10) is listed as a certified criterion. No additional EHI export documentation is linked — just the certification matrix, disclaimers, and additional software (Newcrop, Surescripts, Meinberg NTP).

### 5. Checked vendor marketing/compliance pages

- `https://www.adsc.com/interoperability` → marketing page mentioning HL7, FHIR, X12 standards generally; no EHI export documentation or links
- `https://www.adsc.com/cures-act` → 404
- `https://www.adsc.com/cures-act-compliance` → marketing page about Cures Act compliance, mentions OAuth 2, Medics Me app; no technical documentation or export specs
- `https://www.adsc.com/onc-certified` → links to MedicsDocAssistant and MedicsCloud certification pages plus Real World Testing plans; no EHI export documentation

### 6. Checked CHPL listing for additional URLs

Navigated to https://chpl.healthit.gov/#/listing/10785 in browser.

**b(10) section**: Confirmed Export Documentation URL is `https://apps.medicscloud.com/B10_MedicsDocAssistant.html`. Conformance method: Attestation.

**g(10) section** revealed two additional URLs:
- **API Documentation**: https://staging.medicscloud.com/MedicsDAExtAPI/FHIRMedicsDocAssistant.htm
- **Service Base URL List**: https://fhir-service.medicscloud.com/da/get-clients-end-points

### 7. Downloaded the FHIR API documentation

```bash
curl -sL "https://staging.medicscloud.com/MedicsDAExtAPI/FHIRMedicsDocAssistant.htm" -H 'User-Agent: Mozilla/5.0' -o downloads/FHIRMedicsDocAssistant.htm
```

566 KB HTML file. A Microsoft Word-generated document describing the MedicsDocAssistant FHIR API. This is the g(10) API documentation, not b(10)-specific documentation, but is relevant because the B10 page claims the EHI export uses FHIR US Core 3.1.1.

### 8. Downloaded the Service Base URL list

```bash
curl -sL "https://fhir-service.medicscloud.com/da/get-clients-end-points" -H 'Accept: application/json' -o downloads/service-base-urls.json
```

682 KB JSON — a FHIR Bundle of Endpoint and Organization resources listing client practice FHIR endpoints. This is operational g(10) infrastructure, not b(10) export documentation, but confirms the FHIR service is live.

### 9. Web search

Searched Google for `"Advanced Data Systems" "MedicsDocAssistant" EHI export data dictionary documentation` and `site:adsc.com "EHI" OR "data dictionary"`. No additional documentation found anywhere on the public internet.

## What Was Found

The EHI export documentation for MedicsDocAssistant consists of a single HTML page (2,375 bytes) containing one paragraph. It states that the product can export EHI for single patients and patient populations in two formats:

1. **HL7 CCDA XML** compliant with USCDI v1
2. **HL7 FHIR v4.0.1 US Core v3.1.1**

No vendor-specific documentation accompanies this claim. The page links only to the external HL7 standard specifications (CCDA IG and US Core IG), not to any vendor-specific data dictionary, export format specification, schema, mapping guide, or user instructions.

The separately-registered FHIR API documentation (g(10) API docs, `FHIRMedicsDocAssistant.htm`) provides more detail about the FHIR API. It documents 20 resource types:

1. Patient
2. AllergyIntolerance
3. CarePlan
4. CareTeam
5. Condition
6. Implantable Device (Device)
7. DiagnosticReport (Report and Note exchange)
8. Laboratory Results (Observation)
9. DocumentReference
10. Goal
11. Immunization
12. Medication
13. Smoking Status (Observation)
14. Vitals (Observation)
15. Procedure
16. Encounter
17. Organization
18. Practitioner
19. Provenance
20. Clinical Notes Guidance (DocumentReference)

These are exactly the US Core / USCDI v1 resource types — the standard set required for g(10) certification. The FHIR doc mentions "Bulk Data 1.0.1" in the introduction but provides no actual Bulk Data / $export API documentation. It only describes single-patient SMART on FHIR queries.

There is no data dictionary, no field-level documentation, no schema files, no sample export files, no export instructions, and no documentation of data beyond the USCDI v1 core set.

## Export Coverage Assessment

### Data Domain Coverage

The B10 page claims CCDA and FHIR US Core exports. Based on the product research, MedicsDocAssistant stores a broad range of clinical and operational data. Comparing what the product stores against what the documented export covers:

**Clearly covered (via USCDI v1 / US Core):**
- Demographics (Patient)
- Problem lists / diagnoses (Condition)
- Medications / prescriptions (MedicationRequest, Medication)
- Allergies (AllergyIntolerance)
- Lab results (Observation/Laboratory)
- Vital signs (Observation/Vitals)
- Immunization records (Immunization)
- Procedures (Procedure)
- Smoking status (Observation)
- Clinical notes (DocumentReference, DiagnosticReport)
- Care plans (CarePlan)
- Goals (Goal)
- Implantable devices (Device)
- Encounter records (Encounter)
- Care team (CareTeam)
- Provenance (Provenance)

**Missing or undocumented:**
- **Billing records, claims, charges, payments** — MedicsDocAssistant integrates tightly with MedicsPremier (practice management). The product research notes billing data lives primarily in MedicsPremier. Neither CCDA nor FHIR US Core naturally carries billing claims data. No documentation addresses whether billing data from the integrated suite is included or how it would be exported.
- **Specialty-specific clinical data** — The product serves 28+ specialties with dedicated templates and configurations (behavioral health ASAM assessments, radiology reports, group therapy records, dual diagnosis tracking, etc.). None of this specialty-specific data is addressed in the export documentation. USCDI v1 / US Core does not have resources for these data types.
- **Patient portal data** — Questionnaires, secure messages, appointment requests, online payments. Not addressed.
- **Family health history** — The product is certified for (a)(12) Family Health History, and FHIR R4 has FamilyMemberHistory, but this resource is not listed among the 20 supported.
- **Social/behavioral/psychological data** — Certified for (a)(15), but the FHIR API only covers smoking status, not broader SDOH data.
- **Referral documents and consult letters** — May be partially covered via DocumentReference but not explicitly addressed.
- **Images and attachments** — The product handles imaging orders, faxes, and document attachments. Not addressed.
- **E-prescribing history** — Prescription transmissions via Newcrop/Surescripts. Not addressed.
- **Public health reporting data** — Syndromic surveillance, cancer case reports, electronic case reports. Not addressed.

### Export Format & Standards

The export uses two standard formats:
- **HL7 CCDA XML** (USCDI v1) — a well-understood clinical document standard
- **HL7 FHIR v4.0.1** (US Core 3.1.1) — a well-understood API standard

Both are recognized standards appropriate for clinical summary data. However, both are inherently limited to the USCDI v1 data scope. Neither format was designed to carry billing claims, specialty-specific assessments, or the full breadth of an EHR's data.

The FHIR API doc mentions Bulk Data 1.0.1 in the introduction but provides no actual $export endpoint documentation. The population-level export mentioned on the B10 page is undocumented — there is no information about how to perform a population export, what format it produces, or how it differs from single-patient export.

A third party could reconstruct a clinical summary from the documented export, but could not reconstruct the full patient record including billing, specialty data, and operational data.

### Documentation Quality

**Extremely poor.** The B10 documentation is a single paragraph with no:
- Data dictionary or field definitions
- Export procedure instructions
- Schema or format specifications beyond naming external standards
- Sample data or worked examples
- Error handling or edge case documentation
- Information about what triggers or produces the export
- User guide or screenshots

The FHIR API documentation (g(10)) is more detailed — 10,568 lines with search parameters, example requests, and sample JSON responses for each resource type. But this is g(10) documentation, not b(10) documentation. It was not linked from the B10 page and is registered separately on CHPL.

A developer attempting to understand or import this vendor's EHI export would have essentially no vendor-specific guidance. They would need to know CCDA and FHIR US Core independently and hope the export conforms to those standards without deviations.

### Structure & Completeness

- **No data dictionary** — no table names, field names, data types, or cardinality
- **No value sets** — no coded field documentation
- **No relationship documentation** — no entity-relationship information
- **No versioning or change history**
- **No export format specification** — just "CCDA XML and FHIR US Core" with no details about how the product maps its internal data model to these standards
- **No sample exports** — no example files for either format

### The b(10) vs g(10) Confusion

This is a textbook case of the b(10)/g(10) conflation. The vendor's "EHI export" documentation is one paragraph pointing to their FHIR US Core API. The documentation:
- Only mentions USCDI v1 resource types
- Contains no mention of billing, specialty clinical data, or any data beyond US Core
- Points to the exact same FHIR standard (US Core 3.1.1) used for g(10)
- Provides no data dictionary or mapping for non-standard data

The B10 page's claim of "Electronic Health Information Export" is being fulfilled by the same clinical data API required for g(10). This covers perhaps 30-40% of the data a multi-specialty ambulatory EHR stores about patients — the standard clinical summary, not the full designated record set.

There is no evidence that the vendor has done any work specific to b(10) requirements. The B10 page appears to be a compliance checkbox pointing to the g(10) implementation.

## Access Summary
- Final URL (after redirects): https://apps.medicscloud.com/B10_MedicsDocAssistant.html (no redirect)
- Status: found
- Required browser: no (static HTML, curl works fine)
- Navigation complexity: direct_link
- Anti-bot issues: none

## Obstacles & Dead Ends
- The apps.medicscloud.com domain has no robots.txt, sitemap, or FHIR metadata endpoint
- The `/fhir/` path returns 403 Forbidden — the FHIR server is not publicly accessible
- No Wayback Machine data was retrievable (CDX API timed out)
- The ADSC website uses HubSpot CMS with JavaScript rendering; curl doesn't capture the mandatory disclosures page content, but the page loaded in-browser shows only a certification criteria table with no additional EHI export information
- The Cures Act page (adsc.com/cures-act) returned 404; the alternative path (adsc.com/cures-act-compliance) is a marketing page with no technical content
- Google search found no additional EHI export documentation for this vendor
- The FHIR API doc is hosted on a "staging" subdomain (staging.medicscloud.com), which is unusual for production documentation
