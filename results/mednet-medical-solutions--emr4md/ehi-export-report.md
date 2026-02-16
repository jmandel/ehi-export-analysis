# MedNet Medical Solutions — EHI Export Documentation

Collected: 2026-02-15

## Source
- Registered URL: https://mednetmedical.com/Open_API.html
- CHPL IDs: 10214 (15.04.04.2796.emr4.09.00.1.191218)
- Product: emr4MD Version 9.10
- Certification date: 2019-12-18

## Navigation Journal

### Step 1: Probe the registered URL
```bash
curl -sI -L "https://mednetmedical.com/Open_API.html" -H 'User-Agent: Mozilla/5.0'
```
HTTP 200, Content-Type: text/html, 18,238 bytes. Last-Modified: Mon, 19 Aug 2024.

### Step 2: Download and examine the page
```bash
curl -sL "https://mednetmedical.com/Open_API.html" -H 'User-Agent: Mozilla/5.0' -o mednet-open-api-page.html
```
The page is a simple static HTML page titled "OPEN API DOCUMENTATION FOR MedNet CLIENT APPLICATION DEVELOPERS." Last updated December 13, 2023. It contains:
- A brief description of the emr4MD product
- A statement that the API is "a read-only RESTful FHIR® STU 3 Ballot API"
- A link to EMR Direct's Interoperability Engine 2017 Open API documentation: https://www.interopengine.com/2017/open-api-documentation
- Developer contact info (Nagi Veam, nagi@mednetmedical.com, (508)970-5678)
- Links to the emr4MD login page and support portal

There is **no mention of EHI export, 170.315(b)(10), data dictionary, or export format** on this page. The page exclusively covers the FHIR API (g(7)/g(9) criteria), not the b(10) EHI export.

### Step 3: Follow the EMR Direct link
```bash
curl -sL "https://www.interopengine.com/2017/open-api-documentation" -H 'User-Agent: Mozilla/5.0' -o interopengine-2017-open-api-documentation.html
```
23,298 bytes. This is EMR Direct's Interoperability Engine 2017 documentation — a generic FHIR STU3 Ballot API guide for the Common Clinical Data Set (CCDS). It covers 20 CCDS data elements mapped to FHIR resources (Patient, Condition, MedicationStatement, AllergyIntolerance, Observation, Procedure, CareTeam, Immunization, Device, CarePlan, Goal). Authentication is OAuth 2.0 with patient portal credentials. Last updated February 12, 2020.

This is **not EHI export documentation.** It is g(7)/g(9) Application Access documentation.

### Step 4: Check for newer interopengine versions
The interopengine.com homepage links to three API doc versions: 2017, 2021, and 2026. Downloaded the 2026 version:
```bash
curl -sL "https://www.interopengine.com/2026/open-api-documentation" -H 'User-Agent: Mozilla/5.0' -o interopengine-2026-open-api-documentation.html
```
41,219 bytes. This is significantly more detailed: FHIR R4, US Core IG Release 6.1.0, USCDI V3 support, SMART App Launch, FHIR Bulk Data Access Group export, PKCE, UDAP Dynamic Client Registration. It covers ~29 resource types.

This is g(10) Standardized API documentation. It mentions Bulk Data Access but **only for the US Core resource types** — no mention of b(10) EHI export or non-USCDI data.

### Step 5: Check the ONC Certified HIT / Cures Update page
```bash
curl -sL "https://mednetmedical.com/2015-Cures-Update.html" -H 'User-Agent: Mozilla/5.0' -o mednet-2015-cures-update.html
```
48,159 bytes. Lists all 43 certified criteria. Under criterion (b)(10), it simply states:
> (b)(10): **Electronic Health Information (EHI) export**

No link to EHI export documentation, no description of the export format, no data dictionary. It's just a certification listing page.

### Step 6: Download the Price Transparency PDF
```bash
curl -sL "https://www.mednetmedical.com/price-transparency/Price_Transparency_emr4MD_v9.10.pdf" -H 'User-Agent: Mozilla/5.0' -o Price_Transparency_emr4MD_v9.10.pdf
```
956,711 bytes, 5 pages. Under 170.315(b)(10), it states:
> **Electronic Health Information (EHI) export**: "This functionality allows a practice to create individual and group exports of PHI without programming intervention."
> **Cost**: "Included in base service agreement, subscription fee plus Subscription fee from 3rd party - EMR Direct, one time implementation fee and annual subscription charged."

This is the only description of the b(10) EHI export found anywhere. It confirms:
1. The export exists as a feature
2. It requires EMR Direct (third-party dependency)
3. It supports individual and group exports
4. It does not require programming intervention

But there is **no documentation of the export format, no data dictionary, no field definitions, no schema**, and no instructions for how to use the export.

### Step 7: Search for additional EHI documentation
Searched the vendor's site for any pages containing "ehi", "export", "b(10)", "data dictionary", or "bulk":
- Checked common paths: /ehi, /ehi-export, /EHI_Export, /b10, /bulk-export, /data-dictionary — all returned 404
- Searched the interopengine.com site for EHI-specific pages — none found
- The homepage links to "AppStudio" at appstudio.interopengine.com but this is a developer portal, not EHI export documentation

No additional EHI export documentation was found anywhere on the vendor's site or the third-party partner's site.

## What Was Found

The registered URL points to a minimal Open API page that redirects to EMR Direct's generic FHIR API documentation. **No EHI export (b)(10) documentation exists at the registered URL or anywhere else on the vendor's site.**

What is documented:
- **FHIR API (g(7)/g(9)/g(10))**: EMR Direct's Interoperability Engine provides a FHIR API covering the Common Clinical Data Set (2017 version, STU3) and US Core/USCDI V3 (2026 version, R4). This is standard (g)(10) API documentation — not EHI export.
- **EHI Export feature existence**: The Price Transparency PDF confirms that a b(10) EHI export feature exists, allows individual and group exports of PHI without programming, and requires an EMR Direct subscription. But no format, schema, or field-level documentation is provided.

What is not documented:
- Export format (FHIR? C-CDA? CSV? Database dump? Unknown)
- Data dictionary or field definitions
- Which data domains are included in the export
- How to initiate or receive the export
- Sample data or examples
- Schema files of any kind
- Instructions for interpreting the exported data

## Export Coverage Assessment

### Data Domain Coverage

**Impossible to assess.** No data dictionary, schema, or format documentation exists for the b(10) export. The only statement is that the feature "allows a practice to create individual and group exports of PHI without programming intervention."

Based on the product research, emr4MD (as part of the 4MD360 suite) stores:
- **Clinical**: Problems, medications, allergies, immunizations, vital signs, lab results, procedures, clinical notes, family history, social history, implantable devices, care plans, clinical decision support alerts
- **Practice management/billing**: Scheduling, charges, claims, payments, copays, ERA, EOB, patient statements, ICD-10 billing
- **E-prescribing**: Prescription history, refill requests (via DrFirst)
- **Patient portal**: Secure messages, appointment requests, refill requests, patient-submitted health info
- **Quality measures**: eCQM data for ~20 clinical quality measures

The FHIR API documentation (which is for g(10), not b(10)) only covers USCDI/US Core clinical data — approximately 20 standard data categories. If the b(10) export is simply a repackaging of the g(10) FHIR API output, it would miss:
- All billing and financial data (charges, claims, payments, EOBs, patient statements)
- Scheduling and appointment data
- E-prescribing data beyond what's in MedicationRequest
- Patient portal messages and requests
- Custom clinical templates and disease management data
- Document scans and imports
- Quality measure submissions

However, since there is no documentation at all, we cannot determine whether the export actually covers these domains or not.

### Export Format & Standards

**Unknown.** The Price Transparency PDF mentions EMR Direct is required, suggesting the export may go through the Interoperability Engine — potentially using FHIR. But the registered URL points to the g(7)/g(9) FHIR STU3 API documentation, which is a patient-level API, not a bulk export mechanism.

The 2026 interopengine docs mention FHIR Bulk Data Access Group export, but this is for g(10) and only covers US Core resource types.

Without documentation, a third party could not reconstruct a patient record from this export because the format is not specified.

### Documentation Quality

**Virtually nonexistent for b(10).** The registered URL does not contain any b(10) EHI export documentation. It points to generic g(7)/g(9) FHIR API docs provided by a third-party partner (EMR Direct). The only mention of b(10) is a single sentence in the Price Transparency PDF.

The FHIR API documentation itself (for g(10)) is of reasonable quality — it specifies resource types, search parameters, authentication, data type choices, and US Core IG conformance. But this is irrelevant to the b(10) EHI export requirement.

A developer could not implement an import of EHI export data based on the available documentation because the export format is entirely undocumented.

### Structure & Completeness

- **Data dictionary**: None
- **Field-level definitions**: None
- **Data types/value sets**: None (except for the FHIR API which is a different system)
- **Relationships between entities**: None
- **Worked examples**: None
- **Schema files**: None
- **Export instructions**: None
- **Versioning/change history**: None

This is a textbook example of a vendor treating b(10) as a compliance checkbox rather than a substantive documentation requirement. The vendor is certified for b(10), but the registered documentation URL points to their g(7)/g(9) FHIR API documentation — a completely different certification criterion.

## Access Summary
- Final URL (after redirects): https://mednetmedical.com/Open_API.html (no redirect)
- Status: found (but content is g(7)/g(9) API docs, not b(10) EHI export docs)
- Required browser: no
- Navigation complexity: direct_link (single page with one external link)
- Anti-bot issues: none

## Obstacles & Dead Ends
- The registered URL contains no b(10) EHI export documentation whatsoever
- The URL links to EMR Direct's Interoperability Engine API docs, which cover g(7)/g(9)/g(10) FHIR API, not b(10) EHI export
- No alternative EHI documentation paths were found on the vendor's site
- The vendor appears to conflate their g(7)/g(9) FHIR API documentation with their b(10) EHI export documentation requirement
- The only evidence that a b(10) export feature exists is a one-sentence description in the Price Transparency PDF
- EMR Direct (the third-party partner) does not appear to publish b(10)-specific documentation either
- The MedNet page still references the 2017 interopengine docs (FHIR STU3), even though a 2026 version (FHIR R4, US Core 6.1) exists, suggesting the page is not actively maintained
