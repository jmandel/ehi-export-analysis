# AssureCare LLC — EHI Export Documentation

Collected: 2026-02-16

## Source
- Registered URL: https://ipatientcare.com/onc-certified-health-it/
- CHPL IDs: 8970 (v18.0, 2017-12-01), 11103 (v22.5, 2022-12-21), 11286 (v23.0, 2023-05-22)
- Product: iPatientCare (ambulatory EHR with integrated practice management and billing)

## Navigation Journal

1. **Initial probe** — HTTP 200 from `https://ipatientcare.com/onc-certified-health-it/`, Content-Type `text/html; charset=UTF-8`, served by Apache. No redirects.

```bash
curl -sI -L "https://ipatientcare.com/onc-certified-health-it/" -H 'User-Agent: Mozilla/5.0'
```

2. **Page examination** — The page is a single WordPress/Elementor page titled "Meaningful Use Transparency and Disclosure Statement." It lists three certified product versions (18.0, 22.5, 23.0) with certification dates and IDs. Below the product info, there are direct download links to PDF documents organized in sections.

3. **Found EHI Export link** — A clearly labeled link "Electronic Health Information Export" pointing to:
```
https://ipatientcare.com/wp-content/uploads/2025/04/170.315b10-Electronic-Health-Information-Export-v1.0.0.2.pdf
```

Downloaded with:
```bash
curl -sL "https://ipatientcare.com/wp-content/uploads/2025/04/170.315b10-Electronic-Health-Information-Export-v1.0.0.2.pdf" \
  -H 'User-Agent: Mozilla/5.0' \
  -o 170.315b10-Electronic-Health-Information-Export-v1.0.0.2.pdf
```
Verified: PDF document, 3 pages, 126,823 bytes.

4. **Found SmartOnFHIR API Documentation** — Referenced by the EHI export PDF (which says "Please refer 170.315(g)(10) SmartOnFHIR API Documentation.PDF for the API Specifications") and also directly linked on the certification page:
```
https://ipatientcare.com/wp-content/uploads/2025/12/SMART-on-FHIR-API-Authentication-and-Access-Guide-–-1.0.0.3.pdf
```

Downloaded with:
```bash
curl -sL "https://ipatientcare.com/wp-content/uploads/2025/12/SMART-on-FHIR-API-Authentication-and-Access-Guide-%E2%80%93-1.0.0.3.pdf" \
  -H 'User-Agent: Mozilla/5.0' \
  -o SMART-on-FHIR-API-Authentication-and-Access-Guide-1.0.0.3.pdf
```
Verified: PDF document, 118 pages, 570,126 bytes.

5. **FHIR server artifacts** — The certification page links to the FHIR endpoint list at `https://oauth.ipatientcare.net/api/FHIREndpoint`. From the FHIR server base URL (`https://fhir.ipatientcare.net:9443/fhirserver/fhir/`), I retrieved the CapabilityStatement and SMART configuration:

```bash
curl -s "https://fhir.ipatientcare.net:9443/fhirserver/fhir/metadata" -H 'Accept: application/fhir+json' -o fhir-capability-statement.json
curl -s "https://fhir.ipatientcare.net:9443/fhirserver/fhir/.well-known/smart-configuration" -H 'Accept: application/json' -o smart-configuration.json
curl -s "https://oauth.ipatientcare.net/api/FHIREndpoint" -H 'Accept: application/json' -o fhir-endpoints-bundle.json
```

6. **Full-page screenshot** captured showing the complete certification page layout.

## What Was Found

### EHI Export Document (3 pages)

The primary EHI export document (`170.315b10-Electronic-Health-Information-Export-v1.0.0.2.pdf`) is remarkably brief — just 3 pages, of which 2 are front matter (title, revision history, conventions, support contact). The substantive content is a single page that states:

> "The applications provide export of electronic health information (EHI) for a single patient as well as for patient population in the following formats:
> 1. **CCDA**: iPatientCare supports bulk export of HL7 CCDA xml files which comply to United States Core Data for Interoperability (USCDI), Version 1 requirements.
> 2. **FHIR**: iPatientCare also supports HL7® Version 4.0.1 FHIR® Release 4, October 30, 2019, FHIR® US Core Implementation Guide STU V3.1.1, HL7 FHIR Bulk Data export."

That is the entirety of the EHI export documentation. No data dictionary, no field definitions, no schema, no export instructions, no screenshots, no sample data.

### SmartOnFHIR API Documentation (118 pages)

This is the (g)(10) FHIR API guide referenced by the EHI export document. It covers:
- SMART on FHIR OAuth2 authentication flow (standalone, EHR-embedded, backend services)
- Production and test FHIR endpoint URLs
- API request/response examples for each supported FHIR resource type

**Supported FHIR resources** (per the API guide and CapabilityStatement):
- Patient, AllergyIntolerance, CarePlan, CareTeam, Condition, Coverage, Device (implantable), DiagnosticReport, DocumentReference, Encounter, Goal, Immunization, Medication, MedicationDispense, MedicationRequest, Observation (labs, vitals, smoking status), Organization, Practitioner, PractitionerRole, Procedure, Provenance, ServiceRequest, Specimen, RelatedPerson, Location, Group

These are standard US Core FHIR resources — the (g)(10) standardized API profile.

### FHIR CapabilityStatement

The CapabilityStatement confirms:
- FHIR R4 (4.0.1) server based on HAPI FHIR
- Instantiates US Core Server and Bulk Data capability statements
- The implementation description literally says "Inferno Reference Server for US Core, Bulk Data, and SMART App Launch"
- 26 resource types, all with US Core supported profiles

## Export Coverage Assessment

### Data Domain Coverage

This is a textbook case of the **(b)(10) vs (g)(10) confusion**. The vendor's EHI export documentation explicitly equates EHI export with their FHIR US Core API and C-CDA documents. Both of these formats are limited to USCDI data classes.

**Domains clearly covered** (via FHIR US Core / C-CDA USCDI v1):
- Demographics (Patient)
- Problems/Conditions
- Medications (MedicationRequest, Medication, MedicationDispense)
- Allergies
- Lab results (Observation, DiagnosticReport)
- Vital signs (Observation)
- Immunizations
- Procedures
- Care plans and care teams
- Clinical notes (DocumentReference)
- Implantable devices
- Goals
- Smoking status
- Coverage (insurance)
- Encounters
- Provenance

**Domains likely stored by iPatientCare but NOT addressed in the export:**
- **Billing records** — Claims, charges, payments, accounts receivable, denials, appeals. iPatientCare has a full integrated billing/RCM system. None of this appears in the export documentation. The FHIR Coverage resource covers insurance info, but not claims/billing transactions.
- **Scheduling data** — Appointments, wait lists, recall lists. (Note: scheduling is generally not part of the designated record set, so this is not a critical gap.)
- **E-prescribing details** — While MedicationRequest is covered, the full e-prescribing workflow data (EPCS details, pharmacy transactions, Surescripts interactions) likely has richer detail than what FHIR captures.
- **Scanned documents and attachments** — DocumentReference is supported, but it's unclear whether the bulk export includes the actual document content (binary attachments) or just metadata references.
- **Secure messages** — Patient-provider messages from the patient portal.
- **Custom/specialty clinical data** — The product serves behavioral health, cardiology, pain management, orthopedics, pediatrics, and other specialties. Specialty-specific templates, assessments, and clinical data likely have fields that don't map to standard US Core resources.
- **Referral management data** — Referral letters, tracking, status.
- **Quality measure/MIPS data** — Patient-specific quality measure calculations.
- **Telehealth encounter metadata** — Virtual visit details beyond what's in a standard Encounter resource.
- **Revenue cycle data** — Eligibility verification results, fee schedules, patient balance information.

### Export Format & Standards

The export uses two recognized standards:
1. **C-CDA XML** (HL7 CDA R2, Consolidated CDA templates) — USCDI v1 compliant
2. **FHIR R4 via Bulk Data** — US Core STU 3.1.1 profiles

Both are well-established interoperability standards, but they are designed for clinical data exchange, not for complete EHI export. A C-CDA document is a clinical summary — it contains a curated subset of the patient record. FHIR Bulk Data using US Core profiles exports standardized clinical data but explicitly does not cover billing, custom forms, or specialty-specific data that doesn't fit US Core resource types.

The CapabilityStatement reveals the FHIR server is based on the "Inferno Reference Server" — this is ONC's testing tool infrastructure, suggesting the FHIR endpoint may be primarily designed to pass (g)(10) certification testing rather than serve as a production-grade data access layer.

Neither format is appropriate for a complete EHI export of all data stored by an integrated ambulatory EHR with billing and practice management. A database dump, CSV export, or comprehensive proprietary format would better serve the (b)(10) requirement.

### Documentation Quality

**Extremely poor.** The EHI export documentation is one substantive page. It:
- Provides zero data dictionary or field definitions
- Gives no instructions for how a user or administrator would perform the export
- Contains no screenshots of the export interface
- Includes no sample data or example export files
- Does not specify which data elements are included in the C-CDA documents
- Does not explain what happens with data that doesn't fit C-CDA or FHIR formats
- Does not address the completeness question at all — it simply asserts CCDA and FHIR as the export formats without acknowledging that these formats cover only a subset of the data the product stores

The SmartOnFHIR API documentation (118 pages) is more substantial but is a (g)(10) API guide, not a (b)(10) export guide. It documents how to authenticate and query the FHIR API, with example requests/responses for each resource type. While useful for API developers, it does not serve as EHI export documentation.

A developer trying to reconstruct a complete patient record from these exports would have no way to know what data is missing, what format the billing data is in, or how to access non-USCDI data.

### Structure & Completeness

- **Data dictionary**: None. No table definitions, no field listings, no schema documentation.
- **Field-level detail**: None beyond what is inherent in the FHIR US Core profiles (which are externally defined standards, not vendor-specific documentation).
- **Value sets**: Not documented (relies entirely on standard FHIR/US Core value sets).
- **Relationships**: Not documented.
- **Versioning**: The document has a version history (3 versions), but all changes were cosmetic (adding product version numbers).
- **Sample data**: None provided.

### Overall Assessment

This documentation represents a **minimal compliance checkbox approach** to the (b)(10) requirement. The vendor has essentially pointed to their (g)(10) FHIR API and C-CDA implementation and declared it their EHI export, without any analysis of whether these formats actually cover all electronic health information stored by their product.

iPatientCare is an integrated EHR/practice management/billing system that stores extensive data across clinical, financial, and administrative domains. The FHIR US Core API and C-CDA documents cover perhaps 30-40% of the total data the product stores — primarily the USCDI clinical data classes. The remaining 60-70% (billing records, custom clinical data, specialty assessments, document attachments, portal messages, referral data, etc.) is not addressed in the export documentation at all.

The 3-page PDF does not even acknowledge that data exists beyond what C-CDA and FHIR cover, let alone explain how it would be exported. This is a significant gap in (b)(10) compliance.

## Access Summary
- Final URL (after redirects): https://ipatientcare.com/onc-certified-health-it/
- Status: found
- Required browser: no (all content accessible via curl; browser used only for screenshots)
- Navigation complexity: direct_link (single click from certification page to PDF)
- Anti-bot issues: none

## Obstacles & Dead Ends
- None. The page loaded cleanly, all links worked, and files downloaded without issues.
- The FHIR CapabilityStatement server description ("Inferno Reference Server") suggests the FHIR endpoint may be a repurposed testing environment rather than a purpose-built production endpoint, but this is an observation rather than an obstacle.
