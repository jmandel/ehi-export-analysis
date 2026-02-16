# Sai Systems Digital LLC — EHI Export Documentation

Collected: 2026-02-14

## Source
- Registered URL: https://saisystems.com/health/pacehr-ehi/
- CHPL IDs: 11177
- Product: PacEHR v20
- Certified: 12/29/2022

## Navigation Journal

### Step 1: Probe the registered URL
```bash
curl -sI -L "https://saisystems.com/health/pacehr-ehi/" -H 'User-Agent: Mozilla/5.0'
```
Returned HTTP 200, Content-Type: text/html. A WordPress-based page on the saisystems.com domain.

### Step 2: Fetch and examine the main EHI page
```bash
curl -sL "https://saisystems.com/health/pacehr-ehi/" -H 'User-Agent: Mozilla/5.0' -o /tmp/pacehr-ehi.html
```
The page is titled "PacEHR Electronic Health Information (EHI) All Data Export." It's a single static page (139KB of HTML, mostly WordPress theme boilerplate) with approximately 4 paragraphs of substantive content. No downloadable files (PDFs, ZIPs, CSVs, schemas) are linked from this page.

The page contains:
- A general description of what EHI is (citing the HIPAA Designated Record Set definition)
- Two use cases: bulk EHI export (all patient data for a practice/provider/department) and single/multi-patient export
- A brief description of the export format: "machine readable XML formats"
- A link to "FHIR API documentation for PacEHR" pointing to https://thesnfist.com/cures-update/

No data dictionary, no field-level documentation, no schema files, no sample exports, no screenshots of the export interface.

### Step 3: Follow the FHIR API documentation link
```bash
curl -sL "https://thesnfist.com/cures-update/" -H 'User-Agent: Mozilla/5.0' -o /tmp/cures-update.html
```
This page (189KB) is the "21st Century Cures Act" page on the TheSNFist.com domain (the companion product site). It contains:

1. **Drummond ONC Certification disclosure** — restating the certification details
2. **A link to the Compliance Certificate PDF** hosted on HubSpot: `Compliance Certificate PacEHR v20 010325.pdf`
3. **FHIR API documentation** — "FHIR Server 1.0.0 for Cures Act Update" — covering 16 standard FHIR resources:
   - AllergyIntolerance
   - CarePlan
   - CareTeam
   - Condition
   - Device
   - DocumentReference (CCDA)
   - Encounter
   - Goal
   - Immunization
   - Location
   - Medication / MedicationRequest
   - Observation (labs, vitals, smoking status)
   - Patient (demographics including USCDI v1/v2 elements)
   - Practitioner
   - Procedure
4. **API Terms of Service** — standard boilerplate terms

The FHIR resources documented are standard US Core / USCDI resources. The page references HL7 FHIR STU3 documentation links. Each resource has endpoint documentation with GET-by-id and search parameter details.

### Step 4: Download the Compliance Certificate
```bash
curl -sL "https://43775473.fs1.hubspotusercontent-na1.net/hubfs/43775473/PacEHR%20Certifications/Compliance%20Certificate%20PacEHR%20v20%20010325.pdf" -o compliance-certificate-pacehr-v20.pdf
```
A 1-page PDF from Drummond Group confirming ONC certification of PacEHR v20 with all listed criteria including (b)(10).

### Step 5: Check the Certifications page
```bash
curl -sL "https://saisystems.com/health/certifications/" -H 'User-Agent: Mozilla/5.0' -o /tmp/certifications.html
```
The certifications page at saisystems.com/health/certifications/ contains the same Drummond certification disclosure text, links to "Real World Testing Plan 2024" (results listed as "Coming Soon"), and the same compliance certificate link. No additional EHI export documentation.

### Step 6: Browser verification
Navigated to both pages in Chrome. The main EHI page renders as a simple WordPress page with the text content described above. The cures-update page renders with the FHIR API documentation in a long-form layout with tables for each resource endpoint. Screenshots captured.

## What Was Found

The EHI export documentation for PacEHR consists of a single web page (https://saisystems.com/health/pacehr-ehi/) that provides a high-level description of the EHI export capability. The page describes three things:

1. **What EHI is**: The page explains EHI by referencing the HIPAA Designated Record Set, noting it includes medical records, billing records, enrollment/payment/claims data, and data used for decision-making.

2. **Export use cases**: Two modes are described — bulk export (all patient data for a practice/provider/department) and single/multi-patient export (for patient requests or referrals).

3. **Export format**: The export is described as being in "machine readable XML formats" and using "PacEHR's APIs that foster interoperability."

The page then links to the FHIR API documentation at thesnfist.com/cures-update/, which documents a standard FHIR R3 (STU3) API covering 16 US Core resources.

**Critically absent** from the documentation:
- No data dictionary or field-level documentation
- No list of what data tables, entities, or domains are included in the export
- No schema files (XSD, JSON Schema, or otherwise)
- No sample export files or examples
- No screenshots of the export interface
- No instructions for how to perform the export
- No mapping between PacEHR's internal data model and the export format
- No documentation of non-USCDI data (billing, scheduling, administrative, etc.)

## Export Coverage Assessment

### Data Domain Coverage

The EHI export page claims to export "all patient data" and references billing records, claims, and decision-making data in its definition of EHI. However, there is **no documentation whatsoever** of what specific data domains are actually included in the export. The only concrete technical documentation provided is the FHIR API, which covers standard USCDI clinical data:

**Covered by the documented FHIR API (g)(10) scope):**
- Allergies (AllergyIntolerance)
- Problems/conditions (Condition)
- Medications (Medication, MedicationRequest)
- Immunizations (Immunization)
- Lab results and vitals (Observation)
- Procedures (Procedure)
- Clinical notes/documents (DocumentReference with CCDA)
- Care plans and goals (CarePlan, Goal)
- Care teams (CareTeam)
- Encounters (Encounter)
- Patient demographics (Patient)
- Implantable devices (Device)
- Practitioners (Practitioner)
- Locations (Location)

**Not documented and likely missing from the export:**
- **Billing and coding data** — PacEHR has integrated billing, charge capture (billEHR), and claims management. The product research identifies this as a core capability. No billing data appears in the FHIR API documentation.
- **Scheduling/appointment data** — Listed as a PacEHR feature on review sites. Not documented.
- **Clinical encounter notes in native format** — PacEHR's core value is template-driven encounter documentation with voice-to-text. The FHIR API only exposes DocumentReference/CCDA, which is a standardized summary, not the native encounter note structure.
- **Document management data** — Listed as a feature. Not documented.
- **Communication records** — SNFConnect messages, patient portal messages. Not documented.
- **Practice/facility census data** — Patient census by facility is a core workflow feature. Not documented.
- **Quality measure/MIPS reporting data** — Certified for (c)(1). Not documented in the export.
- **Audit logs** — Required for (d) criteria. Not documented in the export.
- **User/provider configuration** — Templates, macros, custom settings. Not documented.

### The (b)(10) vs (g)(10) Problem

This is a textbook case of conflating (b)(10) with (g)(10). The EHI export page describes "machine readable XML formats" and points to the FHIR API documentation. The FHIR API documents only standard US Core resources — this is the (g)(10) standardized API, not a comprehensive EHI export.

The EHI page's own definition of EHI includes "billing records," "enrollment, payment, claims adjudication," and "case or medical management record systems" — none of which appear in the FHIR API documentation. The vendor's documentation contradicts itself: the EHI page promises comprehensive health information, but the only technical documentation provided covers a narrow clinical data subset.

Key evidence that this is (g)(10) repackaged as (b)(10):
- The documented resources are exactly the standard US Core / USCDI resource set
- All HL7 documentation links point to FHIR STU3 standard resources
- There is no mention of billing, scheduling, or administrative data in the technical documentation
- The FHIR server is described as "FHIR Server 1.0.0 for Cures Act Update" — not as an EHI export tool
- No documentation of data that doesn't map to standard FHIR resources

### Export Format & Standards

The export is described as "machine readable XML formats" on the EHI page. The linked FHIR API documentation specifies `application/fhir+json` as the accepted format. This creates some confusion — the EHI page says XML, but the FHIR API says JSON. It's unclear if these refer to the same mechanism or different ones.

If the export is via the FHIR API, it uses FHIR R3 (STU3) with US Core profiles. The documented resources cover standard USCDI v1/v2 data classes. This is a recognized standard but only covers clinical data — it cannot represent PacEHR's billing, scheduling, or administrative data.

The format is appropriate for the clinical data it covers, but inappropriate as a comprehensive EHI export format for a product that also stores billing/coding data, scheduling, document management, and practice administration data.

### Documentation Quality

The documentation is **extremely thin**. The main EHI export page is approximately 150 words of substantive content. It provides no:
- Data dictionary
- Field-level definitions
- Data types or value sets
- Worked examples or sample exports
- Instructions for performing the export
- Screenshots of the export interface

The FHIR API documentation on the cures-update page is more substantial but is standard (g)(10) API documentation, not (b)(10) export documentation. It lists endpoints, parameters, and USCDI data element mappings for each resource.

A developer reading this documentation would know how to call the FHIR API to retrieve standard clinical data. They would have no idea how to obtain a complete export of all data PacEHR stores for a patient — billing codes, encounter templates, scheduling records, practice configuration, etc.

The documentation does not appear to be actively maintained. The API Terms of Service are dated December 23, 2022 (the certification date). The Real World Testing results are listed as "Coming Soon" on the certifications page.

### Structure & Completeness

- **Granularity**: The EHI-specific page has zero field-level documentation. The FHIR API page lists USCDI data elements mapped to FHIR resources and documents API endpoint parameters, but does not provide PacEHR-specific field mappings.
- **Coded fields**: No value sets are documented beyond what's standard in US Core.
- **Relationships**: No entity relationship documentation.
- **Versioning**: No version history or change log for the export documentation.

This is among the thinnest EHI export documentation possible while still having a page at the registered URL. The vendor created an EHI landing page that describes the concept of EHI, pointed to their existing FHIR API as the export mechanism, and did not create any (b)(10)-specific documentation.

## Access Summary
- Final URL (after redirects): https://saisystems.com/health/pacehr-ehi/ (no redirect)
- Status: found
- Required browser: no (all content accessible via curl)
- Navigation complexity: direct_link (main page) + one_click (FHIR API docs on separate domain)
- Anti-bot issues: none

## Obstacles & Dead Ends

No technical obstacles. The page loaded cleanly via curl and browser. No authentication required, no anti-bot protection, no JavaScript-dependent rendering.

The obstacle is substantive rather than technical: the registered EHI export URL contains almost no technical documentation. The export mechanism, data dictionary, and format specifications are simply not documented. The only linked technical resource is the FHIR API documentation, which is the (g)(10) standardized API, not a comprehensive (b)(10) export.
