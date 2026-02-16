# Varian Medical Systems — EHI Export Documentation

Collected: 2026-02-16

## Source
- Registered URL: https://varian.com/aria/ehi
- CHPL IDs: 11719
- Product: ARIA CORE v18.3
- Certification Date: 2025-11-26
- ONC-ACB: Drummond Group

## Navigation Journal

### 1. Initial probe of registered URL

```bash
curl -sI -L "https://varian.com/aria/ehi" -H 'User-Agent: Mozilla/5.0'
```

**Result**: HTTP 301 redirect to `https://cancercare.siemens-healthineers.com/aria/ehi`, which returns **HTTP 404** (Page not found). Varian.com was acquired by Siemens Healthineers and the domain redirects to `cancercare.siemens-healthineers.com`, but the `/aria/ehi` path does not exist on the new domain.

### 2. Wayback Machine check

```bash
curl -s "https://web.archive.org/cdx/search/cdx?url=varian.com/aria/ehi&output=text&fl=timestamp,original,statuscode&limit=20"
curl -s "https://web.archive.org/cdx/search/cdx?url=cancercare.siemens-healthineers.com/aria/ehi&output=text&fl=timestamp,original,statuscode&limit=20"
```

**Result**: Zero captures in the Wayback Machine for either URL. The registered EHI documentation URL has apparently never had publicly accessible content indexed by the Internet Archive.

### 3. Alternative path probing on Siemens Healthineers

Tested the following paths on `cancercare.siemens-healthineers.com`:
- `/aria/ehi` — 404
- `/ehi` — 404
- `/ehi-export` — 404
- `/interoperability/ehi` — 404
- `/products/software/ehi` — 404
- `/products/software/digital-oncology/ehi` — 404
- `/products/software/digital-oncology/aria-ehi` — 404
- `/products/software/digital-oncology/legacy-solutions/aria-ehi` — 404

Also tested `www.siemens-healthineers.com`:
- `/products/radiotherapy/software-solutions/aria-ois/ehi` — 404
- `/products/radiotherapy/ehi` — 404

All returned 404.

### 4. Web search

Searched Google for:
- `Varian "ARIA CORE" "EHI export"` — no vendor-specific results
- `Varian ARIA "170.315(b)(10)" EHI export documentation` — no vendor-specific results
- `"varian.com/aria/ehi"` — no results

No publicly accessible EHI export documentation was found via web search.

### 5. CHPL listing examination

Navigated to https://chpl.healthit.gov/#/listing/11719 and expanded the 170.315 (b)(10) criteria details. Found:

| Attribute | Value |
|-----------|-------|
| Relied Upon Software | Winzip |
| Conformance Method | Attestation |
| Export Documentation | https://varian.com/aria/ehi |

The conformance method is **Attestation** (not tested), and the export documentation URL points to the dead link.

### 6. ARIA product page exploration

The ARIA legacy page at `cancercare.siemens-healthineers.com/products/software/digital-oncology/legacy-solutions/aria-oncology-information-system` links to:

- **DynamicFHIR portal**: https://varian.dynamicfhir.com/ — Varian's FHIR R4 API documentation
- **ONC Certification PDF**: via Widen asset management
- **Interoperability brochure**: marketing material about ARIA + Epic integration
- **Interoperability page**: product page about HL7/DICOM integration

None of these are specific to 170.315(b)(10) EHI export.

### 7. DynamicFHIR portal examination

```bash
curl -sL "https://varian.dynamicfhir.com/varian/basepractice/r4/Home/ApiDocumentation" -o fhir-api-documentation.html
curl -sL "https://varian.dynamicfhir.com/fhir/varian/basepractice/r4/metadata" -H 'Accept: application/fhir+json' -o fhir-capability-statement.json
curl -sL "https://varian.dynamicfhir.com/fhir/varian/basepractice/r4/.well-known/smart-configuration" -H 'Accept: application/json' -o fhir-smart-configuration.json
```

This is a SMART on FHIR R4 API portal built by Dynamic Health IT. It documents:
- FHIR API access (SMART on FHIR authorization flows)
- USCDI → FHIR resource mapping table
- Bulk Export (FHIR Bulk Data Access)
- Client registration and configuration

The documentation explicitly states: "Available data via the API interface is limited by the data defined by the USCDI" and maps to standard US Core FHIR resources.

## What Was Found

### No dedicated (b)(10) EHI export documentation exists

The registered EHI export documentation URL (`https://varian.com/aria/ehi`) returns a 404 error. It redirects to the Siemens Healthineers Cancer Care domain where the path does not exist. No alternative location for EHI-specific documentation was found through:
- Alternative URL paths on the vendor's domains
- Web search
- Wayback Machine
- The vendor's product/interoperability pages

### What does exist: FHIR API documentation (g)(10)

The only technical documentation found for data export from ARIA CORE is the **DynamicFHIR portal** at `https://varian.dynamicfhir.com/`, which documents the SMART on FHIR R4 API. This API is provided by Dynamic Health IT and is certified for 170.315(g)(7), (g)(9), and (g)(10).

The FHIR API documentation includes:
- **FHIR Mapping Table**: Maps USCDI data classes to FHIR R4 resources (Patient, Condition, AllergyIntolerance, Immunization, MedicationRequest, etc.)
- **Bulk Export**: Standard FHIR Bulk Data Access (`Patient/$export`, `Group/[id]/$export`) using NDJSON format
- **Client Configuration**: OAuth 2.0 with SMART on FHIR (authorization code, PKCE, client credentials for bulk)
- **CapabilityStatement**: Lists 27 resource types (AllergyIntolerance, Binary, CarePlan, CareTeam, ClinicalImpression, Composition, Condition, Coverage, Device, DiagnosticReport, DocumentReference, Encounter, Goal, Group, Immunization, Location, MedicationDispense, MedicationRequest, Observation, Organization, Patient, Practitioner, PractitionerRole, Procedure, Provenance, RelatedPerson, ServiceRequest, Specimen)

A critical detail from the documentation: "Varian FHIR API assumes the use of a cumulative C-CDA with patient data. For filtering C-CDA data by section, it will use the latest cumulative C-CDA document (by the document EffectiveDateTime) per patient." This means the FHIR API is a **C-CDA pass-through** — it consumes C-CDA documents and re-exposes them as FHIR resources. It is not querying the native ARIA database.

### CHPL b(10) metadata

The CHPL listing reveals that:
- The EHI export relies on **Winzip** as additional software, suggesting the export is a compressed file archive
- The conformance method is **Attestation** (the vendor attested to compliance rather than having it tested by a testing lab)
- The export documentation URL is non-functional

## Export Coverage Assessment

### Data Domain Coverage

**This is a significant finding: there is no publicly accessible documentation of the (b)(10) EHI export.** The only documentation available is the FHIR API portal, which is explicitly a (g)(10) USCDI-scoped API, not a (b)(10) export of all electronic health information.

Based on the product research, ARIA CORE stores extensive oncology-specific data that would be in a patient's designated record set:

| Data Domain | Covered by FHIR API? | Notes |
|-------------|----------------------|-------|
| Patient demographics | Yes | Patient resource |
| Problem lists / diagnoses | Yes | Condition resource |
| Allergies | Yes | AllergyIntolerance |
| Medications (chemotherapy regimens) | Partial | MedicationRequest/Dispense, but 300+ oncology-specific regimens unlikely fully mapped |
| Lab results | Yes | DiagnosticReport, Observation |
| Vital signs | Yes | Observation |
| Immunizations | Yes | Immunization |
| Clinical notes | Partial | DocumentReference (C-CDA), but oncology-specific note types unclear |
| **Radiation therapy prescriptions** | **Not documented** | Core ARIA data — RT prescriptions are not a standard FHIR US Core resource |
| **Treatment plans (dose distributions, beam parameters)** | **Not documented** | Physics-level treatment planning data has no FHIR mapping |
| **Daily treatment records (fraction logs)** | **Not documented** | Per-fraction radiation delivery logs are ARIA-specific |
| **On-treatment images (MV, kV, CBCT)** | **Not documented** | DICOM images stored in ARIA; not addressable via FHIR API |
| **Cancer staging (AJCC)** | **Not documented** | ARIA automates staging; no clear FHIR mapping documented |
| **Toxicity/adverse event records** | **Not documented** | Oncology-specific grading scales |
| **Disease response data** | **Not documented** | Treatment outcome tracking |
| **Billing/charge data (RVU tracking)** | **Not documented** | Coverage resource exists but charge capture is not mapped |
| **QA reports / chart checks** | **Not documented** | Physics QA data |
| **Patient-reported outcomes (Noona)** | **Not documented** | External integration |
| **Survivorship care plans** | **Not documented** | External integration (EQUICARE CS) |

The FHIR API covers roughly the standard USCDI clinical summary — the same data any general-purpose EHR would expose. It does **not** cover the oncology-specific data that is ARIA's primary reason for existence: radiation therapy plans, treatment delivery records, physics QA, imaging, cancer staging, and chemotherapy-specific regimen management.

### Export Format & Standards

No EHI export format is documented. The FHIR Bulk Data API produces NDJSON bundles of standard FHIR R4 US Core resources. The Winzip dependency listed in CHPL suggests a separate zip-based export mechanism exists but is undocumented.

The FHIR API documentation reveals that data flows through C-CDA as an intermediary: "Varian FHIR API assumes the use of a cumulative C-CDA with patient data." This means the API is re-projecting C-CDA content into FHIR resources. C-CDA clinical summaries are inherently USCDI-scoped and would not contain radiation therapy physics data, beam parameters, DICOM images, or other specialty oncology data.

### Documentation Quality

- **For the FHIR (g)(10) API**: The documentation is reasonably thorough for its scope — it includes authorization flows, resource mappings, search parameters, example responses, and bulk export instructions. A developer could implement a FHIR client against this API.
- **For the (b)(10) EHI export**: There is no documentation at all. The registered URL is dead (404), and no alternative documentation was found.

### Structure & Completeness

The FHIR API documentation provides:
- Resource-level mapping (USCDI category → FHIR resource type)
- Supported search parameters per resource
- Example JSON responses
- Authentication and authorization details

It does **not** provide:
- Field-level data dictionaries
- Value set definitions (relies on US Core defaults)
- Cardinality or constraint documentation
- Any mapping of oncology-specific data to export fields
- Any documentation of what a (b)(10) export contains

## Access Summary
- Final URL (after redirects): https://cancercare.siemens-healthineers.com/aria/ehi
- Status: dead (404)
- Required browser: N/A (URL is dead)
- Navigation complexity: N/A
- Anti-bot issues: none encountered

## Obstacles & Dead Ends

1. **Dead registered URL**: The primary registered EHI documentation URL (`https://varian.com/aria/ehi`) redirects to `cancercare.siemens-healthineers.com/aria/ehi` which returns 404. This appears to be a domain migration issue — Varian was acquired by Siemens Healthineers in 2021, and the varian.com domain now redirects to the Siemens Cancer Care domain, but the EHI path was never created on the new domain.

2. **No Wayback Machine captures**: Neither the original nor the redirected URL has any captures in the Internet Archive, suggesting the page may never have been publicly accessible.

3. **Widen PDF download**: The ONC Certification PDF hosted on Widen required extracting the signed preview URL from the JavaScript PDF viewer (`window.viewerPdfUrl`) since direct download endpoints returned HTML.

4. **Certification is very recent**: ARIA CORE v18.3 was certified on 2025-11-26 (less than 3 months before this assessment). The combination of a recent certification, attestation-only conformance for (b)(10), and dead documentation URL suggests the EHI export documentation may have been planned but never published.

5. **g(10) conflation**: The only export-related documentation available is the FHIR Bulk Data API documentation, which is explicitly scoped to USCDI/(g)(10). For a radiation oncology system like ARIA — where the majority of clinically significant data (treatment plans, fraction logs, physics data, DICOM images) lives outside the USCDI scope — using the FHIR API as a (b)(10) export would leave the vast majority of the designated record set unexported.
