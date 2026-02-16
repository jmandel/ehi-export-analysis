# Altera Digital Health — EHI Export Documentation

Collected: 2026-02-16

## Source
- Registered URL: https://www.alterahealth.com/legal/onc-reg-compliance/
- CHPL IDs: 11589 (Paragon® Denali v1), 11761 (Paragon® EHR v25)
- Developer: Altera Digital Health Inc. (listed via Providers Management, Inc.)

## Navigation Journal

1. **Initial probe:** `curl -sI -L "https://www.alterahealth.com/legal/onc-reg-compliance/" -H 'User-Agent: Mozilla/5.0'` returned HTTP 200, Content-Type text/html, 203KB WordPress page hosted on WP Engine.

2. **Page examination:** Downloaded the full HTML page (~204KB). The page is a comprehensive ONC regulatory compliance hub covering all Altera products: Altera Lab, dbMotion, Paragon, Sunrise, and TouchWorks.

3. **Located EHI section:** The page has a clearly labeled "EHI Export Documentation" section with the description: "Documentation on the 170.315 (b)(10) EHI Export output format for each Altera ONC certified solution is provided below."

4. **Paragon-specific links found:** Under the "Paragon" heading within the EHI Export Documentation section, the page provides:
   - A current version: "Paragon EHR® 25.1 & Paragon® Denali 1" — a ZIP file containing CapabilityStatement.json + Extension-Details.xlsx
   - An archived section with: "Paragon 23.2 Capability Statement" (JSON) and "Paragon 23.2 Extension Details" (XLSX), plus "Paragon EHR® 24.1 & Paragon® Denali 1" (ZIP)

5. **Downloads performed:**
   ```bash
   curl -sL -o paragon-ehr-25-1-denali-1.zip "https://www.alterahealth.com/download/204/ehi-documentation/16995/paragon-ehr-25-1-paragon-denali-1" -H 'User-Agent: Mozilla/5.0'
   curl -sL -o paragon-ehr-24-1-denali-1.zip "https://www.alterahealth.com/download/204/ehi-documentation/15915/paragon-ehr-24-1-paragon-denali-1" -H 'User-Agent: Mozilla/5.0'
   curl -sL -o capabilitystatement.json "https://www.alterahealth.com/download/204/ehi-documentation/11851/capabilitystatement.json" -H 'User-Agent: Mozilla/5.0'
   curl -sL -o extension-details.xlsx "https://www.alterahealth.com/download/204/ehi-documentation/11954/extension-details.xlsx" -H 'User-Agent: Mozilla/5.0'
   ```

6. **Verification:** All files verified — ZIPs extract correctly, JSON is valid FHIR, XLSX is valid Excel. The 25-1 ZIP contains a CapabilityStatement.json (460KB) and Extension-Details.xlsx (64KB). The 24-1 ZIP contains the same file types with identical structure.

7. **No additional Paragon EHI docs found.** No PDFs, user guides, sample export files, or schema documents beyond the CapabilityStatement + Extension Details were available for Paragon. The page provides no export instructions specific to Paragon.

## What Was Found

Altera's EHI export documentation for Paragon consists of exactly two artifacts per version:

### 1. CapabilityStatement.json (FHIR R4)
A FHIR CapabilityStatement resource titled "Paragon EHI Export FHIR R4 Implementation" that documents the export format. It declares the EHI export produces **48 FHIR R4 resource types**:

**Clinical:** AllergyIntolerance, BodyStructure, CarePlan, CareTeam, Communication, CommunicationRequest, Condition, Consent, DetectedIssue, DiagnosticReport, DocumentReference, FamilyMemberHistory, Goal, GuidanceResponse, Immunization, ImagingStudy, Media, Medication, MedicationAdministration, MedicationDispense, MedicationRequest, MedicationStatement, NutritionOrder, Observation, Procedure, ServiceRequest, Specimen

**Billing/Financial:** Account, Claim, ChargeItem, ChargeItemDefinition, Coverage, CoverageEligibilityRequest, CoverageEligibilityResponse, PaymentNotice, PaymentReconciliation

**Patient/Demographics:** Patient, Person, RelatedPerson

**Encounter/Scheduling:** Encounter, Appointment, AppointmentResponse

**Infrastructure:** Device, Endpoint, Location, Organization, Practitioner, PractitionerRole

For each resource type, the CapabilityStatement lists:
- Standard FHIR elements supported (as extension entries linking to hl7.org element definitions)
- Custom Paragon-specific extensions (linking to the Extension-Details.xlsx)
- Search parameters (patient, _lastUpdated)

### 2. Extension-Details.xlsx
An Excel spreadsheet with 826 rows documenting custom extensions across 33 resource types. Each row contains:
- **Resource** — the FHIR resource type
- **Key** — a URL identifier for the extension
- **Extension** — human-readable name (e.g., "Organ Donor", "Veteran", "VIP")
- **Definition** — natural-language description of what the extension captures

The most extension-heavy resources reflect Paragon's specialty coverage:
- Claim: 172 extensions (detailed billing/claim data)
- Coverage: 130 extensions (insurance/coverage detail)
- Patient: 64 extensions (demographics beyond FHIR base)
- PaymentReconciliation: 58 extensions
- Encounter: 51 extensions
- MedicationRequest: 48 extensions

## Export Coverage Assessment

### Data Domain Coverage

**This is a genuinely comprehensive (b)(10) export, not just a (g)(10) repackaging.** The 48 FHIR resource types with 826 custom extensions demonstrate that Altera has done substantial work to map Paragon's full data model into FHIR R4, going well beyond US Core / USCDI requirements.

**Clearly covered domains:**
- **Demographics/Patient:** 64 custom extensions including Organ Donor, Veteran status, VIP flag, race, ethnicity — comprehensive patient data
- **Clinical notes/documents:** DocumentReference with 40 custom extensions, Media
- **Billing/Claims:** Claim (172 extensions!), ChargeItem, Account, PaymentNotice, PaymentReconciliation — this is the strongest evidence of genuine (b)(10) work. US Core doesn't touch billing.
- **Insurance/Coverage:** Coverage with 130 custom extensions, CoverageEligibilityRequest/Response
- **Medications:** MedicationRequest (48 extensions), MedicationAdministration (36), MedicationDispense, MedicationStatement, Medication
- **Lab:** Observation (37 extensions), DiagnosticReport, Specimen
- **Encounters:** Encounter with 51 custom extensions
- **Orders:** ServiceRequest (19 extensions), NutritionOrder (8 extensions)
- **Immunizations:** Immunization with 13 custom extensions
- **Allergies:** AllergyIntolerance with custom sensitivity and Rx-verification fields
- **Problems/Conditions:** Condition
- **Procedures:** Procedure
- **Imaging:** ImagingStudy
- **Care Plans:** CarePlan, CareTeam, Goal
- **Consent:** Consent with 21 custom extensions
- **Appointments/Scheduling:** Appointment, AppointmentResponse
- **Family History:** FamilyMemberHistory
- **Devices:** Device with 17 custom extensions

**Domains with potential gaps:**
- **Pharmacy Management:** While medication resources are present, there's no clear mapping of the full pharmacy management workflow (medication verification, drug interaction alerts history, dispensing cabinet data) that Paragon's pharmacy module handles
- **OR/Surgical data:** Procedure is present but with only 2 custom extensions — given Paragon's OR management module with perioperative charting, supply tracking, and charge capture, this seems light
- **ED-specific data:** No ED-specific resources or extensions visible, despite Paragon having an ED module
- **Radiology workflow:** ImagingStudy is present but has 0 custom extensions — Paragon's radiology module tracks film tracking, department workflow, which isn't captured
- **Clinical Decision Support alerts:** GuidanceResponse has 5 custom extensions (appears to capture CDS history)
- **Patient portal/messaging:** No clear representation of CarePath portal messages
- **ERP data:** Fiscal management, supply chain, HR data from Altera's ERP modules are absent — though these may be separate products

### Export Format & Standards

The export is **FHIR R4 (4.0.1) NDJSON** format, delivered through what appears to be a FHIR Bulk Data-style API endpoint. The CapabilityStatement references a development server URL (`pqsambmainc9.cloud.mdrxdev.com`), suggesting the export runs through a FHIR server that supports patient-level queries.

This is a well-chosen format: FHIR R4 is a recognized standard, and by mapping proprietary data elements as custom extensions (826 of them), Altera preserves both interoperability with standard FHIR tooling and completeness of the original data. The approach is technically sound — a third party with these two documentation files could parse the FHIR resources and understand both the standard elements and Paragon-specific additions.

However, **no US Core or other profiles are referenced** — all resources use base FHIR R4 with extensions. This means the export is a custom mapping rather than a standards-compliant US Core export with additional data.

### Documentation Quality

**Moderate quality with significant gaps:**

**Strengths:**
- The CapabilityStatement is machine-readable and follows FHIR conventions
- Extension definitions include natural-language descriptions that explain the clinical purpose
- The documentation covers 48 resource types — comprehensive breadth
- Versioned releases (23.2, 24.1, 25.1) show active maintenance

**Weaknesses:**
- **No export instructions:** There are no user guides, screenshots, or step-by-step instructions for performing the export. The page says "Open the Capability Statement file to look at all the fields" but doesn't explain how to trigger an export.
- **No sample data:** No example FHIR resources or sample export files are provided
- **No data type specifications:** Extensions list names and descriptions but don't specify data types, cardinality, or value set bindings
- **No formal StructureDefinitions:** The custom extensions are documented only in the Excel spreadsheet, not as proper FHIR StructureDefinition resources that would be machine-processable
- **No relationship documentation:** How resources reference each other (e.g., Encounter → Patient → Coverage → Claim) is not documented
- **No schema files:** No JSON Schema, XSD, or OpenAPI specifications

### Structure & Completeness

**Field-level documentation is present but thin.** The CapabilityStatement lists which elements are supported per resource, and the Extension Details spreadsheet provides names and descriptions for 826 custom extensions. However:

- Standard elements are listed by name only (no data types, cardinality, or constraints)
- Custom extensions have descriptions but no formal type definitions
- Value sets for coded fields are not documented
- Relationships between resources are implicit (via FHIR references) but not explicitly mapped
- No change history or versioning notes between releases

A developer could understand the shape of the export (which resources, which fields) but would need to inspect actual export data to understand data types, coding systems, and reference patterns. The documentation serves as a field inventory rather than a complete implementation guide.

## Access Summary
- Final URL: https://www.alterahealth.com/legal/onc-reg-compliance/
- Status: found
- Required browser: no (all content accessible via curl)
- Navigation complexity: one_click (EHI section clearly labeled, download links direct)
- Anti-bot issues: none (User-Agent header sufficient)

## Obstacles & Dead Ends
- None significant. The page loaded cleanly, all download links worked, files verified as expected types.
- The root-level capabilitystatement.json and extension-details.xlsx (the "Paragon 23.2" versions) are an older format — the CS is wrapped in a FHIR Bundle rather than being a standalone resource. The 25-1 versions are the current/primary artifacts.
- pip/pip3 were broken in the environment, so xlsx parsing was done via bun + xlsx npm package instead of Python openpyxl.
