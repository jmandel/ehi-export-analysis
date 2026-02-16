# Agastha, Inc. — EHI Export Documentation

Collected: 2026-02-16

## Source
- Registered URL: https://agastha.com/Agastha-B10-Documentation.pdf
- CHPL IDs: 11152 (v20.1, certified 2022-12-28), 11616 (v25.1, certified 2025-03-25)
- Developer: Agastha, Inc.
- Product: Agastha Enterprise Healthcare Software

## Navigation Journal

1. **Initial probe** — the registered URL returns a direct PDF download:
   ```bash
   curl -sI -L "https://agastha.com/Agastha-B10-Documentation.pdf" -H 'User-Agent: Mozilla/5.0'
   ```
   Result: HTTP 200, `Content-Type: application/pdf`, 586,413 bytes. No redirects.

2. **Downloaded the PDF**:
   ```bash
   curl -sL "https://agastha.com/Agastha-B10-Documentation.pdf" -H 'User-Agent: Mozilla/5.0' -o downloads/Agastha-B10-Documentation.pdf
   ```
   Verified with `file` and `pdfinfo`: 7-page PDF, title "§170.315(b)(10) Electronic Health Information export- Documentation", version 20.1, created 2023-10-10.

3. **Checked the mandatory disclosures / certifications page** at `http://www.agastha.com/certifications.html`. Found two relevant links:
   - `https://agastha.com/dataExport.html` — an EHI export guide/landing page
   - `https://agastha.com/apiR4.html` — FHIR R4 API documentation

4. **Fetched dataExport.html**: A minimal web page that serves as the EHI export landing page. Contains a version history table (v1.0, 2023-04-10, "Original Document") linking back to the same B10 PDF. Also links to `apiR4.html#resources-link` with the text "FHIR: Agastha also supports". No additional downloadable artifacts.

5. **Fetched apiR4.html**: A 215KB HTML page containing detailed FHIR R4 API documentation — this is the (g)(10) patient API documentation, not specifically (b)(10). It documents OAuth registration, authentication, SMART on FHIR, Bulk Data export, and per-resource API endpoints. Saved as supplementary context since the B10 PDF states exports use FHIR JSON format for listed resources.

6. **Checked PDF for embedded URLs and attachments**:
   - Only external URL in the PDF text: `http://hl7.org/fhir/` (standard spec, not followed)
   - No embedded file attachments (`pdfdetach -list` returned 0)
   - No additional documentation referenced

## What Was Found

The entire (b)(10) EHI export documentation is a **single 7-page PDF** (`Agastha-B10-Documentation.pdf`). Its contents:

### Cover page (p1)
Title, version (20.1), author (Eddy B. Dishueme), date (10/3/2023).

### Overview (p2)
States that Agastha meets §170.315(b)(10) by implementing "FHIR Export for Single Patient and Bulk Export." Users with assigned roles can generate exports for:
- A single patient
- A group of patients
- The entire patient population

Includes a brief "What Is EHI?" section quoting 45 CFR 164.501 definitions.

### Screenshot of export interface (p2-3)
Shows the "Data Portability/Export" interface with three variants:
- **Single Patient Export**: Date of Service filter (Date Range / Previous Month / None), a patient account search field, Comments field, Export button
- **Group of Patients EHI Export**: Same interface but with multiple patient accounts listed (comma-separated IDs)
- **Patient Population EHI Export**: Same interface with "All patients" radio button selected

### FHIR resource listing (p4-5)
Lists 21 FHIR resources that use FHIR JSON format:
1. AllergyIntolerance
2. CarePlan
3. CareTeam
4. Condition
5. Device
6. DiagnosticReport
7. DocumentReference
8. Encounter
9. Goal
10. Immunization
11. Location
12. Medication
13. MedicationRequest
14. Observation
15. Organization
16. Patient
17. Practitioner
18. Procedure
19. Provenance
20. RelatedPerson
21. ServiceRequest

States: "All the other resources are currently exported using the standard JSON format." This is a critical sentence — it implies there are additional data elements beyond the 21 FHIR resources, exported in non-FHIR JSON, but **does not specify what those additional resources are**.

Standards referenced: FHIR R4 (4.0.1), US Core IG STU V3.1.1, HL7 FHIR Bulk Data export.

### Resource Description table (p5-7)
A two-column table (Name, Description) for each of the 21 FHIR resources. The descriptions are **copied verbatim from the FHIR R4 specification** — they describe the generic FHIR resource definitions, not Agastha-specific mappings, extensions, or field details.

### Support section (p7)
Contact info: phone (704)544-6504, email support@agastha.com, physical address.

## Export Coverage Assessment

### Data Domain Coverage

The product research reveals Agastha is an integrated platform with EHR, practice management, pharmacy management, LIS, billing, patient portal, e-prescribing, and telehealth modules. The export documentation covers only clinical data that maps to standard FHIR US Core resources.

**Clearly covered** (via the 21 listed FHIR resources):
- Demographics (Patient)
- Allergies (AllergyIntolerance)
- Conditions/problem lists (Condition)
- Medications/prescriptions (Medication, MedicationRequest)
- Lab results/diagnostics (DiagnosticReport, Observation)
- Immunizations (Immunization)
- Procedures (Procedure)
- Encounters (Encounter)
- Care plans and goals (CarePlan, Goal)
- Care teams (CareTeam)
- Devices (Device)
- Documents (DocumentReference)
- Clinical notes (via DocumentReference)
- Referrals/orders (ServiceRequest)
- Provenance tracking (Provenance)
- Provider info (Practitioner, Organization, Location)
- Related persons (RelatedPerson)

**Apparently missing or undocumented:**
- **Billing and claims data** — The product has a full billing/claims/revenue cycle module. No billing-related FHIR resources (Claim, ClaimResponse, Coverage, ExplanationOfBenefit) appear in the FHIR resource list. The sentence "all the other resources are currently exported using the standard JSON format" *might* cover billing data, but this is not documented.
- **Pharmacy management data** — Inventory, procurement, stock levels, pharmacy sales. Not covered by any listed resource. Again, possibly covered by the "other resources" clause but unspecified.
- **E-prescribing details** — MedicationRequest covers prescriptions, but controlled substance prescribing details, EPCS records, and prescription transmission records are not specifically addressed.
- **Lab management (LIS) data** — Lab orders may be partially covered by ServiceRequest and DiagnosticReport, but LIS-specific data (specimen tracking, barcode data, device connectivity records) is not documented.
- **Patient portal data** — Secure messages between patients and providers, portal access logs.
- **Telehealth data** — Virtual visit records, remote monitoring data.
- **Insurance/enrollment information** — Coverage resources not listed.
- **Custom/specialty clinical data** — The product serves oncology, neurology, mental health, etc. No mention of specialty-specific assessments or data structures.

The critical ambiguity is the statement "All the other resources are currently exported using the standard JSON format." This suggests the export includes more than just the 21 FHIR resources, but there is **zero documentation** about what those other resources are, what format they take, or what data they contain. This is a significant documentation gap.

### Export Format & Standards

The export uses **FHIR R4 JSON** (4.0.1) conforming to US Core IG STU V3.1.1 for 21 listed resource types, plus "standard JSON format" for unspecified additional resources. The FHIR Bulk Data export standard is also referenced.

The 21 FHIR resources listed are essentially the **US Core resource set** — this is the exact pattern of a (g)(10) FHIR API being repackaged as (b)(10) EHI export. The resource list closely mirrors what a standard US Core / USCDI implementation would expose, with no additional resources for billing, pharmacy, or specialty data.

The mention of "standard JSON format" for "other resources" is potentially significant — it suggests Agastha may export non-FHIR data for areas like billing and pharmacy. However, without any documentation of what those resources are, this is not verifiable.

A third party receiving this export would be able to process the 21 FHIR resources using standard FHIR tooling. However, they would have no way to understand or import the "other resources" in "standard JSON format" without additional documentation.

### Documentation Quality

**Poor.** The documentation is minimal and largely derivative:
- **No data dictionary**: There are no field-level definitions, data types, cardinality, or value sets. The resource descriptions are copied verbatim from the FHIR R4 specification.
- **No export format specification for non-FHIR data**: The "standard JSON format" used for other resources is completely undocumented. No sample structure, no field names, nothing.
- **No sample data or examples**: No example export files, no sample JSON structures.
- **No schema files**: No JSON Schema, XSD, or OpenAPI spec. No FHIR StructureDefinitions or custom profiles.
- **No worked examples**: A developer receiving this export would know the FHIR resources are standard FHIR R4/US Core, but would have no guidance on the non-FHIR portions.
- **Screenshots are helpful**: The export interface screenshots show the "Data Portability/Export" screen with date range filters, patient selection options, and export buttons — this gives a user enough to find and use the feature.
- **Version mismatch**: The PDF says version 20.1 (created 2023), but the newer certification is version 25.1 (2025). The documentation has not been updated for the newer version.

### Structure & Completeness

The documentation provides only resource-level granularity — it names the 21 FHIR resources and gives their generic FHIR definitions. There is:
- No field-level documentation
- No Agastha-specific mapping (how does Agastha data map to each FHIR element?)
- No value sets or coded fields documentation
- No relationship documentation beyond what FHIR references provide
- No documentation of the non-FHIR "other resources"
- No versioning or change history beyond the single version entry on the dataExport page

The supplementary API R4 page (`apiR4.html`) provides more technical detail about the FHIR API (authentication, endpoints, resource-specific query parameters) but this is (g)(10) API documentation, not (b)(10) export documentation. The Bulk Data endpoint documented there would produce the same FHIR resources listed in the B10 PDF.

### Overall Assessment

This is a **minimal compliance checkbox** approach to (b)(10) documentation. The export mechanism appears to be their (g)(10) FHIR Bulk Data API repurposed as a (b)(10) export, with a user-facing "Data Portability/Export" interface layered on top. The 21 FHIR resources listed are the standard US Core set — there is no evidence of export capabilities for the substantial non-clinical data domains (billing, pharmacy, LIS) that the product stores.

The tantalizing reference to "all the other resources" being exported in "standard JSON format" hints that Agastha may actually export more than just US Core data, but the complete absence of documentation for these other resources makes this impossible to verify. If these other resources do include billing, pharmacy, and specialty data, the documentation fails by not describing them. If they don't exist, the statement is misleading.

For a product that integrates EHR, practice management, pharmacy, LIS, billing, e-prescribing, and telehealth, a 7-page document listing 21 standard FHIR resources with copy-pasted definitions is inadequate documentation of a comprehensive EHI export.

## Access Summary
- Final URL (after redirects): https://agastha.com/Agastha-B10-Documentation.pdf
- Status: found
- Required browser: no
- Navigation complexity: direct_link
- Anti-bot issues: none

## Obstacles & Dead Ends
- None. The PDF was directly accessible at the registered URL with no authentication or anti-bot measures.
- The dataExport.html page is a thin landing page that adds no substantive content beyond linking to the PDF and the API R4 docs.
- The apiR4.html page is (g)(10) documentation, not specifically (b)(10), but was saved as supplementary context since the export format references it.
