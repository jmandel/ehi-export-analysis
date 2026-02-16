# EHI Export Analysis: Procentive (Ensora Health)

**Product**: Procentive
**Analysis date**: 2026-02-16
**CHPL IDs**: 15.04.04.2214.Proc.02.01.1.221228 (CHPL ID 11155)

## 1. Product Context

Procentive is a cloud-based EHR and practice management platform built specifically for behavioral health, mental health, and substance use recovery providers. It is now part of Ensora Health (formerly Therapy Brands, acquired by KKR for $1.2B in 2021). The product targets mid-size to larger behavioral health organizations, including residential/inpatient facilities, outpatient clinics, and substance abuse treatment centers.

Key data domains relevant to EHI completeness:

- **Clinical documentation**: Customizable notes, initial assessments, treatment plans (with Practice Planners for DSM-5-based treatment planning), progress notes, discharge summaries, group therapy notes
- **Medications/prescribing**: Full e-prescribing including EPCS for controlled substances (via DrFirst integration)
- **Billing/RCM**: Insurance claims, charge submission, payment tracking, denials/appeals management, clearinghouse services, Medicare/Medicaid billing
- **Bed management**: Dedicated module for residential facilities — bed assignments, stays, capacity, waitlists, attendance tracking
- **Patient portal**: Secure messaging, self-scheduling, bill pay, telehealth
- **Scheduling**: Appointments, reminders, telehealth/virtual waiting rooms
- **Reporting**: 120+ report templates covering clinical, financial, and utilization data

This is a comprehensive behavioral health platform that stores clinical, billing, scheduling, and specialty-specific data. A complete EHI export should cover all patient-facing data across these domains.

## 2. Artifacts Reviewed

| # | File | Type | Size | Description | Informativeness |
|---|------|------|------|-------------|-----------------|
| 1 | `PDF-for-Website-on-Formats-1.pdf` | PDF | 112 KB, 1 page | **The sole (b)(10) documentation artifact.** Describes XML, CSV, and PDF as export formats in generic terms. No data dictionary, no field definitions, no schema. Created 2023-11-30 by Catherine Baker in Microsoft Word. | Very low |
| 2 | `onc-procentive-page.html` | HTML | 83 KB | ONC certification landing page. Describes single-patient and population export capabilities. Links to the File Formats PDF and FHIR endpoints. | Low |
| 3 | `fhir-api-documentation.html` | HTML | 686 KB | Complete FHIR API documentation from Dynamic Health IT's ConnectEHR platform. USCDI-to-FHIR mapping, search parameters, example payloads, Bulk Export docs. **Explicitly limited to USCDI data.** | High (for g)(10) only) |
| 4 | `fhir-capability-statement.json` | JSON | 19 KB | FHIR R4 CapabilityStatement listing 22 resource types with supported interactions and operations. | Medium |
| 5 | `smart-configuration.json` | JSON | 3 KB | SMART on FHIR configuration with 87 scopes across 26 resource types. | Low |
| 6 | `fhir-endpoints.json` | JSON | 2 KB | FHIR Endpoint Bundle with one endpoint for Procentive base practice. | Low |
| 7 | `fhir-home-page.html` | HTML | 15 KB | FHIR server home page: "DYNAMIC FHIR SERVER - 4.0.1", ConnectEHR v4 + BulkFHIR4. | Low |
| 8–11 | Screenshots (4 PNG files) | PNG | 130–858 KB | Visual captures of ONC page, FHIR API docs, and PDF rendering. Used to verify content. | Verification only |

**Most informative**: The FHIR API documentation (`fhir-api-documentation.html`) is thorough but explicitly scoped to USCDI/(g)(10), not (b)(10). **Least informative**: The File Formats PDF — the only (b)(10)-specific artifact — contains zero information about what data is actually exported.

## 3. Export Mechanics

**Format(s)**: The ONC page states the export produces files in XML, CSV, and/or PDF. The linked PDF describes these three formats generically. No schema, structure, or example files are provided for any format.

**Mechanism**:
- **Single patient**: Self-service via the Procentive UI ("without developer assistance")
- **Patient population**: Requires submitting a support ticket via Salesforce — not self-service

**Bulk capability**: Population-level export exists but is vendor-assisted (support ticket required).

**Access constraints**: The ONC page notes export content "might vary" based on software version, configuration decisions, documentation practices, and other factors. No mention of fees.

**Separate from FHIR**: The EHI export (XML/CSV/PDF) and FHIR API (NDJSON) are presented as separate mechanisms on the ONC page. The FHIR API documentation explicitly states: *"Available data via the API interface is limited by the data defined by the USCDI."*

## 4. Export Content: What's In It

### (b)(10) EHI Export: Unknown

The (b)(10) export documentation provides **zero information** about what data is included in the export. The sole artifact — `PDF-for-Website-on-Formats-1.pdf` — is a single page containing textbook-style definitions of XML, CSV, and PDF file formats. It does not:

- List any tables, entities, or data elements
- Define any fields, types, or relationships
- Provide sample data or example files
- Describe which data domains are covered
- Offer any schema or data dictionary
- Explain how the exported files are structured

The ONC page adds only that the export covers "electronic health information (EHI) for a single patient" and "all the data for a patient population." No further specifics.

**There is no data dictionary. There are 0 entities documented. There are 0 fields documented.**

### (g)(10) FHIR API: Well-documented but USCDI-only

The FHIR API (provided via Dynamic Health IT's ConnectEHR platform) is well-documented and supports 22 resource types. The USCDI-to-FHIR mapping table lists 29 mappings:

| USCDI Category | FHIR Resource |
|---|---|
| Patient Demographics | Patient |
| Problem List | Condition |
| Procedures | Procedure |
| Smoking Status | Observation |
| Vital Signs | Observation |
| Laboratory Results | Observation |
| Laboratory Tests | DiagnosticReport |
| Goals | Goal |
| Immunizations Information | Immunization |
| Assessment and Plan of Treatment | CarePlan |
| Care Team Member(s) | CareTeam |
| Health Concerns | Condition |
| Medications | MedicationRequest |
| Allergies and Intolerances | AllergyIntolerance |
| Unique Device Identifier(s) | Device |
| Clinical Summary Document (C-CDA) | DocumentReference |
| Consultation Note | DocumentReference |
| Discharge Summary | DocumentReference |
| History and Physical Note | DocumentReference |
| Procedure Note | DocumentReference |
| Progress Note | DocumentReference |
| Cardiology Report | DocumentReference |
| Pathology Report | DocumentReference |
| Radiology Report | DocumentReference |
| Practitioner | Practitioner |
| PractitionerRole | PractitionerRole |
| Encounter | Encounter |
| Location | Location |
| Organization | Organization |

Additional resources in the CapabilityStatement not in the USCDI table: ClinicalImpression, Binary, Provenance, Composition, Group (for bulk export operations).

Bulk Export is supported via `Patient/$export` and `Group/[id]/$export` with JWT-based backend authentication, producing NDJSON output.

**This is explicitly (g)(10) documentation, not (b)(10).** The API docs state the data is "limited by the data defined by the USCDI" and the FHIR API "assumes the use of a cumulative C-CDA with patient data."

### Vendor's own content organization

There is no vendor-provided data dictionary or entity listing for the (b)(10) export. The only structured content comes from the FHIR API documentation, which organizes data by USCDI categories (see table above). No native database tables, field names, or vendor-specific data structures are documented anywhere.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor's (b)(10) documentation covers nothing specific — it only states that the export produces files in XML, CSV, and PDF formats. There is no breakdown by data domain, no entity listing, and no field-level detail.

The FHIR API documentation (which is explicitly (g)(10), not (b)(10)) covers USCDI clinical data categories: demographics, conditions, medications, allergies, vitals, lab results, immunizations, clinical notes, care plans, goals, encounters, and procedures. This is the standard USCDI clinical summary set.

**Entirely absent from all documentation** (both (b)(10) and (g)(10)):
- Billing/claims/payments data
- Insurance/coverage data
- Treatment plan detail (beyond generic CarePlan)
- Behavioral health assessments and specialty clinical instruments
- Bed management data
- Portal/secure messaging data
- Scheduling/appointment data
- E-prescribing detail beyond MedicationRequest
- Group therapy notes and session data
- Custom forms and templates

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | FHIR Patient resource (USCDI only); no (b)(10) docs | FHIR covers basic demographics; no evidence the (b)(10) XML/CSV export includes these or goes beyond USCDI |
| Encounters / visits | ⚠️ Partial | FHIR Encounter resource (USCDI only) | Same limitation — USCDI encounter data only |
| Problems / conditions / diagnoses | ⚠️ Partial | FHIR Condition resource (USCDI only) | DSM-5 diagnoses are central to behavioral health; unclear if specialty coding detail is preserved beyond standard FHIR |
| Medications / prescriptions | ⚠️ Partial | FHIR MedicationRequest (USCDI only) | Product has full EPCS capability; FHIR MedicationRequest is a clinical summary, not the full prescribing record |
| Allergies | ⚠️ Partial | FHIR AllergyIntolerance (USCDI only) | Standard USCDI coverage |
| Immunizations | ⚠️ Partial | FHIR Immunization (USCDI only) | Standard USCDI coverage |
| Vitals | ⚠️ Partial | FHIR Observation (USCDI only) | Standard USCDI coverage |
| Lab results | ⚠️ Partial | FHIR Observation, DiagnosticReport (USCDI only) | Less central to behavioral health but available via FHIR |
| Procedures | ⚠️ Partial | FHIR Procedure (USCDI only) | Standard USCDI coverage |
| Clinical notes / documents | ⚠️ Partial | FHIR DocumentReference (USCDI only) | Product has rich customizable clinical notes, group therapy notes, and Practice Planners; FHIR DocumentReference is a reference/container, not structured specialty content |
| Care plans / goals | ⚠️ Partial | FHIR CarePlan, Goal (USCDI only) | Product has detailed behavioral health treatment plans with Practice Planners; generic FHIR CarePlan unlikely to capture this depth |
| Insurance / coverage | ❌ Not covered | No evidence in any export documentation | Product manages insurance eligibility verification and authorization management; **significant gap** |
| Claims / billing | ❌ Not covered | No evidence in any export documentation | Product has comprehensive billing/RCM with claims, denials, appeals; **significant gap** |
| Payments | ❌ Not covered | No evidence in any export documentation | Product handles payment processing and tracking; **significant gap** |
| Specialty-specific: Behavioral health assessments | ❌ Not covered | No evidence in any export documentation | Product stores behavioral health assessments, DSM-5 treatment plans, intake/discharge workflows, group therapy data; **significant gap** |
| Specialty-specific: Bed management | ❌ Not covered | No evidence in any export documentation | Dedicated module for residential facilities; **significant gap** |
| Patient communications / portal messages | ❌ Not covered | No evidence in any export documentation | Product has patient portal with secure messaging; gap |
| Orders / referrals | ❌ Not covered | No evidence in any export documentation | N/A — unclear if product stores these distinctly |
| Consents / directives | ❌ Not covered | No evidence in any export documentation | N/A — unclear if product stores these distinctly |
| Imaging / diagnostic reports | ⚠️ Partial | FHIR DiagnosticReport (USCDI only) | Less relevant for behavioral health |

**Summary**: All "⚠️ Partial" ratings above reflect that the FHIR API provides USCDI-level clinical data, but (1) the FHIR API is (g)(10) documentation, not (b)(10), (2) USCDI captures only a clinical summary projection, not the full native data, and (3) there is zero documentation of what the actual (b)(10) XML/CSV/PDF export contains. The ❌ domains — billing, insurance, payments, behavioral health specialty data, bed management — represent the most significant gaps because these are core functions of the product with no evidence of coverage in any export path.

## 6. Documentation Quality

**For the (b)(10) export**: The documentation is effectively non-existent. A single-page PDF defining what XML, CSV, and PDF file formats are (in generic, non-product-specific terms) is the entirety of the (b)(10) technical documentation. A developer receiving an export from Procentive would have:

- No data dictionary
- No field definitions or types
- No entity/table descriptions
- No relationship documentation
- No value sets or coded field definitions
- No sample data or example files
- No schema (XSD, JSON Schema, or otherwise)
- No instructions on how to interpret the exported files

**It would be impossible to build an import from this documentation.** A recipient would need to reverse-engineer every file in the export.

**For the (g)(10) FHIR API**: The documentation is comprehensive and well-structured. The 686 KB HTML page includes:
- Complete USCDI-to-FHIR resource mapping table
- Search parameters and URL syntax for every resource
- Example request/response payloads with full JSON structures
- Authentication setup (SMART on FHIR + Backend Services)
- Bulk Export workflow documentation
- Postman collection setup instructions

However, this documentation explicitly covers only USCDI data via the FHIR API — it is not (b)(10) documentation and does not describe an "all EHI" export.

## 7. Overall Assessment

### Classification

**Minimal/stub**: The (b)(10) EHI export documentation is too thin to assess what is actually exported. The sole artifact is a generic description of file formats (XML, CSV, PDF) with no data dictionary, no schema, and no description of export content. The FHIR API documentation is well-done but is explicitly scoped to (g)(10)/USCDI, not (b)(10).

### Key Findings

1. **The (b)(10) export has effectively zero documentation.** The only (b)(10)-specific artifact (`PDF-for-Website-on-Formats-1.pdf`) is a 1-page document containing textbook definitions of XML, CSV, and PDF file formats. It provides no information whatsoever about what data is exported, how it is structured, or what fields/entities are included.

2. **The FHIR API is well-documented but explicitly not (b)(10).** The FHIR API documentation (686 KB, 22 resource types, 29 USCDI mappings) is thorough, but the docs themselves state data is "limited by the data defined by the USCDI" — this is a (g)(10) implementation, not an all-EHI export.

3. **Major data domains have no documented export path.** Billing/claims, insurance, payments, behavioral health assessments, bed management, and portal messages — all core functions of Procentive — have no evidence of inclusion in either the (b)(10) or (g)(10) export.

4. **Population export requires vendor assistance.** Bulk patient population export requires "submitting a support ticket via Salesforce," making it a vendor-mediated process rather than self-service.

5. **The export content is unknowable from the documentation.** The (b)(10) export may or may not include comprehensive data — but the documentation provides no way to determine this. The ONC page says the export covers "all the data for a patient population," but the sole technical document offers no evidence to support this claim.

### Summary Stats

```
Classification:  Minimal/stub
Export format:   XML, CSV, PDF (per documentation; no schema or examples provided)
Model type:      Unknown (no data dictionary or entity descriptions)
Entities:        0 documented for (b)(10); 22 FHIR resource types for (g)(10)
Fields:          0 documented for (b)(10); N/A for (g)(10) (standard FHIR)
Descriptions:    N/A (no data dictionary exists)
Sample data:     No
Bulk export:     Yes (vendor-assisted via support ticket)
Domains covered: 0 of 13 confirmed for (b)(10); ~10 of 13 at USCDI level via (g)(10)
```

### Bottom Line

Procentive's (b)(10) EHI export documentation is among the thinnest possible — a single page defining what XML, CSV, and PDF are, with no information about what data is actually exported. A patient or provider receiving this export would have no documentation to understand or use the data. The most significant gap is the complete absence of any documentation for billing, insurance, behavioral health specialty data, and bed management — all core product functions — in either the (b)(10) or (g)(10) export path.
