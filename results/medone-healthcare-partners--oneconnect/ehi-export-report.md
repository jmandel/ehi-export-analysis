# MedOne Healthcare Partners — EHI Export Documentation

Collected: 2026-02-14

## Source
- Registered URL: https://www.medonehp.com/wp-content/uploads/2023/11/Export.pdf
- CHPL IDs: 11426
- Product: OneConnect Version 0
- Certification date: 2023-12-27

## Navigation Journal

The registered URL returns HTTP 500. The site has been rebuilt on Next.js/Vercel (previously WordPress), and the old `/wp-content/uploads/` path no longer works.

```bash
curl -sI -L "https://www.medonehp.com/wp-content/uploads/2023/11/Export.pdf" -H 'User-Agent: Mozilla/5.0'
# Returns: HTTP/2 500, Content-Type: text/html, x-matched-path: /500
```

The certifications/mandatory disclosures page at https://www.medonehp.com/certifications/ is live and contains the documentation. The page footer has a "DATA & POLICIES" section with three document links hosted on Vercel blob storage:

1. **EHI Exports** → `https://m8osrnd4strxadl3.public.blob.vercel-storage.com/EHI%20Export.pdf`
2. **FHIR URLs** → `https://m8osrnd4strxadl3.public.blob.vercel-storage.com/FHIR_Valid%20URLs.json`
3. **FHIR API Specifications** → `https://m8osrnd4strxadl3.public.blob.vercel-storage.com/FHIR%20API%20Specifications.pdf`

There is also a Wayback Machine link to the FHIR API Documentation in the "Interoperability" section of the page body, but it points to the same 1.3 MB PDF as the FHIR API Specifications link (identical file size: 1,296,059 bytes).

All three documents downloaded successfully via direct curl:

```bash
curl -sL "https://m8osrnd4strxadl3.public.blob.vercel-storage.com/EHI%20Export.pdf" -H 'User-Agent: Mozilla/5.0' -o EHI-Export.pdf
curl -sL "https://m8osrnd4strxadl3.public.blob.vercel-storage.com/FHIR%20API%20Specifications.pdf" -H 'User-Agent: Mozilla/5.0' -o FHIR-API-Specifications.pdf
curl -sL "https://m8osrnd4strxadl3.public.blob.vercel-storage.com/FHIR_Valid%20URLs.json" -H 'User-Agent: Mozilla/5.0' -o FHIR_Valid_URLs.json
```

All verified with `file` command — PDFs confirmed as PDF documents, JSON confirmed as JSON text data.

## What Was Found

### EHI Export PDF (1 page)

The entire EHI export documentation is a single-page PDF (created 2023-11-07 from a Word document). Its full text:

> **Product Name and Version: OneConnect Version 0**
>
> The patient EHI export contains data from the patient's chart. Multiple file formats are used to store this information.
>
> ZIP is an archive file format.
>
> PDF or Portable Document Format is a file format that is used to present text or image based documents.
>
> C-CDA or Consolidated Clinical Document Architecture is a file format used for health information exchange.
>
> The export file itself is a zip file. It contains zip files of C-CDAs for now and other files attached to the patient's chart will be added later (e.g. PDF and images)
>
> Information for each patient encounter is available C-CDA format in zip archive.

That is the entire document. It describes an export that produces a ZIP file containing:
- C-CDA documents (one per encounter)
- Promises that "other files attached to the patient's chart will be added later (e.g. PDF and images)"

There is **no data dictionary**, **no schema**, **no field-level documentation**, **no sample export**, and **no user instructions** for performing the export.

### FHIR API Specifications PDF (58 pages)

This is the (g)(10) Standardized API documentation — a Smart on FHIR implementation guide covering OAuth2 authentication, patient-level FHIR resource access (AllergyIntolerance, CarePlan, CareTeam, Conditions, ImplantableDevice, DiagnosticReport, DocumentReference, Labs, Goals, Immunizations, Medications, SmokingStatus, Procedures, Provenance, VitalSigns), patient search, encounter search, and CCDA retrieval. It ends with terms of use. This is **not** the (b)(10) EHI export documentation — it documents the standard FHIR API for individual patient access and population-level services.

### FHIR Valid URLs JSON

A FHIR Bundle containing a single Endpoint resource pointing to `https://qafhir.medonehp.com:9443/fhir-server/api/v4/` and an Organization resource. This is infrastructure metadata for the FHIR API, not related to the EHI export mechanism.

## Export Coverage Assessment

### Data Domain Coverage

The EHI export documentation says the export "contains data from the patient's chart" and delivers it as C-CDA documents per encounter. Based on the product research, OneConnect stores:

**Likely covered by C-CDA (standard C-CDA sections):**
- Patient demographics
- Medications/orders (CPOE certified)
- Implantable device information
- Clinical notes (the product's core function)
- Transitions of care data

**Almost certainly missing or inadequately covered:**
- **Billing/CPT codes** — The related BOLT platform captures CPT codes and exports to accounting systems. C-CDA does not have a standard billing section. No mention of billing data in the export documentation.
- **Custom clinical documentation** — OneConnect's primary value is streamlined clinical documentation with templates, voice recognition, and shorthand. C-CDA imposes a rigid structure that likely cannot faithfully represent the vendor's custom documentation workflows and formats.
- **Quality measure data** — 68 CQMs are certified; no mention of how this data is exported.
- **Provider order entry details** — Beyond what C-CDA captures in its standard medication sections.

**Ambiguous / cannot determine:**
- The scope claim is broad ("data from the patient's chart") but the format (C-CDA per encounter) inherently limits what can be represented. The document explicitly states additional content types "will be added later," implying the current export is incomplete.
- There is no mention of whether the export includes data from integrated systems (e.g., RXNT e-prescribing data, data received via Direct messaging, data from PCC/PointClickCare integration).

### Export Format & Standards

The export uses **C-CDA** documents packaged in a ZIP archive, one C-CDA per encounter. C-CDA is a recognized standard, but it is a **clinical summary standard**, not an EHI bulk export format. C-CDA is designed for transitions of care and patient summaries — it captures a defined set of clinical sections but is not designed to represent the full breadth of electronic health information a system stores.

This is a classic case of a vendor using their (g)(10)/(b)(1) clinical document infrastructure to satisfy (b)(10). The C-CDA will cover standard clinical data elements, but it is structurally incapable of representing:
- Billing records and charge data
- Custom form/template data that doesn't map to C-CDA sections
- System-specific workflow data used in patient care decisions
- Data relationships and metadata beyond what C-CDA supports

A third party receiving this export would get a set of clinical encounter summaries but would not be able to reconstruct the full patient record as it exists in OneConnect.

### Documentation Quality

**Extremely poor.** The entire EHI export documentation is 6 sentences on a single page. It:
- Defines what ZIP, PDF, and C-CDA are (which is unhelpful)
- States the export is a ZIP of C-CDAs
- Acknowledges the export is incomplete ("will be added later")
- Provides no instructions for performing the export
- Provides no data dictionary or field mapping
- Provides no sample data
- Provides no information about what C-CDA sections are populated
- Provides no information about how to request an export

A developer could not implement an import of this data based on this documentation alone. They would need to know which C-CDA template is used, what sections are populated, what coded values appear, and how encounters are organized in the ZIP structure — none of which is documented.

### Structure & Completeness

There is essentially no structured documentation. The document does not contain:
- Table or field definitions
- Data types or value sets
- Cardinality or constraints
- Entity relationships
- Schema files or machine-readable artifacts
- Versioning or change history
- Sample files

This appears to be the absolute minimum compliance artifact — a document that acknowledges the existence of an EHI export capability without meaningfully documenting it.

### Context

This is consistent with what the product research revealed: MedOne Healthcare Partners is a physician practice that built its own EHR, not a health IT vendor. OneConnect is used internally by ~100 physicians and 75+ APCs. The documentation quality reflects an organization that built software for internal use and obtained certification as a regulatory requirement, not as a commercial product feature. The phrase "will be added later" in a document dated November 2023 (over two years ago) suggests the export capability was still under development at certification time and the documentation was never updated.

## Access Summary
- Final URL (after redirects): https://m8osrnd4strxadl3.public.blob.vercel-storage.com/EHI%20Export.pdf (found via certifications page)
- Registered URL status: dead (HTTP 500 — site rebuilt on new platform)
- Required browser: no (curl works for all downloads)
- Navigation complexity: one_click (from certifications page footer)
- Anti-bot issues: none

## Obstacles & Dead Ends
- The registered CHPL URL (https://www.medonehp.com/wp-content/uploads/2023/11/Export.pdf) returns HTTP 500. The site was rebuilt from WordPress to Next.js/Vercel/Payload CMS, breaking the old wp-content paths.
- The certifications page at https://www.medonehp.com/certifications/ is the current location of the documentation links, hosted on Vercel blob storage.
- The FHIR API Documentation link in the Interoperability section points to a Wayback Machine URL (https://web.archive.org/web/20250805232450/https://www.medonehp.com/fhir/SmartOnFHIR-API.pdf), suggesting the original on-site link also broke during the platform migration and they patched it with an archive.org link rather than updating the file location.
