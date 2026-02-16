# EHI Export Analysis: CursaHealth LLC

**Product**: CursaHealth EHR v2.0
**Analysis date**: 2026-02-16
**CHPL IDs**: 15.05.05.3249.CRSA.01.00.1.251229

## 1. Product Context

CursaHealth EHR is a cloud-based, all-in-one platform combining electronic health records, practice management, medical billing, patient portal, and transcription services. It targets small-to-medium ambulatory practices across internal medicine, family medicine, OB/GYN, pediatrics, and mental health/psychiatry. The company is small (11–50 employees, based in Greenfield, Wisconsin) and was certified in December 2025 across 37 ONC criteria.

Key data domains the product stores:
- **Clinical**: Patient demographics, encounters, medications (CPOE), allergies, problem lists, vitals, immunizations, lab orders/results, imaging orders, family health history, social/behavioral data, implantable devices, clinical notes, care plans
- **Practice management**: Appointment scheduling, patient check-in
- **Billing**: Medical billing (claims processing, A/R management, coding review, insurance claims), offered as both software and managed service. Pricing at 6% of collections for the all-inclusive tier suggests billing data resides in the platform.
- **Patient portal**: Secure messaging, document access, appointment scheduling
- **Lab integrations**: Apollo Laboratories, Quest Diagnostics, ConnectDX, LabTrack

The product is certified for (b)(10) EHI export, (g)(10) FHIR API, C-CDA transitions of care, and public health reporting. Notably, e-prescribing (EPCS) is absent from certification.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/B10-Electronic-Health-information-Export.pdf` | 4-page PDF (467 KB, created 2025-08-14) describing the (b)(10) export. Lists three export components: C-CDA, FHIR Bulk Data, and supplemental exports (Excel + documents). No data dictionary or field-level documentation. | **Primary source** — defines the export but provides minimal detail |
| `downloads/FHIR-Documentation.html` | 121 KB HTML page documenting the (g)(10) FHIR API. Lists 18 US Core resource types with OAuth2 auth details. Standard USCDI-scope API documentation. | **Secondary** — this is the (g)(10) API doc, referenced by the (b)(10) PDF as part of the export |

Only two artifacts were collected. No data dictionary, no sample data, no schema files, no additional documentation exists.

## 3. Export Mechanics

**Formats**:
1. **C-CDA XML** — Bulk export of HL7 C-CDA documents complying with USCDI v1. References HL7 CDA R2 and C-CDA R2.1 specifications.
2. **FHIR Bulk Data** — HL7 FHIR R4 via US Core STU v4.0.0. Documentation references the (g)(10) FHIR API (same API endpoint at `fhirapi.cursahealth.com`).
3. **Supplemental exports**:
   - Patient Demographics & Insurance (Excel format)
   - Appointments (Excel format)
   - Documents (scanned/imported files: PDF, JPG, PNG organized by patient chart number)

**Mechanism**: Single-patient export available via UI "at any time without developer assistance." Multi-patient/bulk export described as available in "standardized format." No details on bulk export UI or whether it requires vendor assistance.

**Access constraints/fees**: Not documented.

## 4. Export Content: What's In It

### No data dictionary exists

The (b)(10) documentation contains **zero field-level documentation**. There is no data dictionary, no schema, no field names, no types, no descriptions, no value sets, no relationships, and no sample data. The documentation is entirely prose-level, describing export components in 1–2 sentences each.

### Component 1: C-CDA XML

The PDF states C-CDA documents comply with USCDI v1. No product-specific mapping or extension documentation is provided. The vendor references the HL7 C-CDA R2.1 specification directly without any indication of vendor-specific customization beyond the standard.

### Component 2: FHIR Bulk Data

The FHIR documentation (which is the (g)(10) API doc, not (b)(10)-specific) lists 18 US Core resource types:

| Resource | Profile Reference |
|---|---|
| AllergyIntolerance | US Core Allergy Intolerance |
| CarePlan | US Core CarePlan |
| CareTeam | US Core CareTeam |
| Condition | US Core Condition |
| Device | US Core Device |
| DiagnosticReport | US Core DiagnosticReport |
| DocumentReference | US Core DocumentReference |
| Encounter | US Core Encounter |
| Goal | US Core Goal |
| Immunization | US Core Immunization |
| Location | US Core Location |
| MedicationRequest | US Core MedicationRequest |
| Observation | US Core Observation (multiple profiles: Lab, Vitals, BMI, Pulse, etc.) |
| Organization | US Core Organization |
| Patient | US Core Patient |
| Practitioner | US Core Practitioner |
| Procedure | US Core Procedure |
| Provenance | US Core Provenance |

Each resource is described only as "conforms to USCDI profile for [X]" with a reference to the US Core IG. No vendor extensions, no product-specific fields, no mapping documentation beyond the standard profiles.

### Component 3: Supplemental Exports

Three supplemental exports add minimal content beyond C-CDA/FHIR:

1. **Patient Demographics & Insurance (Excel)**: "comprehensive view of demographics and insurance details structured for clarity and ease of access." No fields listed.
2. **Appointments (Excel)**: "comprehensive view of all appointment details." No fields listed.
3. **Documents**: Signed progress notes, lab results, radiology reports, and scanned/uploaded documents organized in patient chart number folders with category subfolders.

### Vendor's own content organization

| Entity/Component | Fields | Described | Types | Category (vendor's) |
|---|---|---|---|---|
| C-CDA XML documents | N/A | No | No | Standards-based export |
| 18 FHIR US Core resources | N/A | No | No | Standards-based export |
| Patient Demographics & Insurance | N/A | No | No | Supplemental (Excel) |
| Appointments | N/A | No | No | Supplemental (Excel) |
| Documents (scanned/imported) | N/A | No | No | Supplemental (files) |

No entity has any field-level documentation whatsoever.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor describes three layers of export:

1. **C-CDA + FHIR (standard clinical exchange)**: This is the standard (g)(10) clinical exchange surface — 18 US Core FHIR resources plus C-CDA documents. Both are explicitly documented as conforming to USCDI profiles. This covers the standard clinical summary: demographics, conditions, medications, allergies, immunizations, vitals, labs, procedures, encounters, care plans, goals, clinical notes, and devices. There is no evidence of any vendor-specific extensions or customizations beyond the standard.

2. **Supplemental Excel exports**: Demographics/Insurance and Appointments in Excel format. These could potentially add depth beyond what's in C-CDA/FHIR (e.g., more insurance detail, appointment scheduling data), but without field-level documentation, their actual content is unknown. The insurance Excel export is the only evidence of any data beyond standard USCDI scope.

3. **Document export**: Scanned/uploaded files organized by patient. This captures documents that might not be in C-CDA or FHIR (e.g., scanned receipts, external records).

The export is thin — it's fundamentally the (g)(10) FHIR API and C-CDA exchange relabeled as (b)(10), with two undocumented Excel files and a document folder added.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | FHIR Patient resource (US Core); Demographics & Insurance Excel (undocumented fields) | US Core Patient covers basics; Excel may add depth but no field documentation to confirm |
| Encounters / visits | ⚠️ Partial | FHIR Encounter resource (US Core) | Standard US Core Encounter; product stores rich encounter data for multiple specialties — unclear if full encounter detail is captured |
| Problems / conditions | ⚠️ Partial | FHIR Condition resource (US Core) | Standard profile only; EHR likely stores more fields (onset context, severity history, etc.) |
| Medications / prescriptions | ⚠️ Partial | FHIR MedicationRequest (US Core) | Standard profile; no EPCS but CPOE is certified — medication detail likely exceeds US Core |
| Allergies | ⚠️ Partial | FHIR AllergyIntolerance (US Core) | Standard profile |
| Immunizations | ⚠️ Partial | FHIR Immunization (US Core) | Standard profile |
| Vitals | ⚠️ Partial | FHIR Observation (US Core vitals profiles) | Standard profiles |
| Lab results | ⚠️ Partial | FHIR Observation, DiagnosticReport (US Core) | Standard profiles; product integrates with Quest, Apollo, etc. — detailed lab data may exceed US Core |
| Imaging / diagnostic reports | ⚠️ Partial | FHIR DiagnosticReport (US Core) | Standard profile; product has CPOE for imaging |
| Procedures | ⚠️ Partial | FHIR Procedure (US Core) | Standard profile |
| Clinical notes / documents | ✅ Covered | FHIR DocumentReference (US Core) + document file export (PDFs, images) | Best-covered domain — document file export adds real content beyond FHIR |
| Care plans / goals | ⚠️ Partial | FHIR CarePlan, Goal (US Core) | Standard profiles |
| Orders / referrals | ❌ Not covered | No ServiceRequest or order-specific export | Product has CPOE for meds, labs, imaging — order data is not exported as a distinct entity |
| Insurance / coverage | ⚠️ Partial | Demographics & Insurance Excel (undocumented) | Excel export exists but fields are unknown; no FHIR Coverage resource |
| Claims / billing | ❌ Not covered | No billing entities in export | Product offers billing/claims/A/R management — **significant gap** |
| Payments | ❌ Not covered | No payment data in export | Product records payments — gap |
| Consents / directives | ❌ Not covered | No consent entities | Unknown if product stores consents |
| Patient communications / portal messages | ❌ Not covered | No messaging export | Product has secure messaging — gap |
| Scheduling / appointments | ⚠️ Partial | Appointments Excel (undocumented fields) | Excel export exists but fields unknown |
| Specialty-specific (mental health, OB/GYN, pediatrics) | ❌ Not covered | No specialty-specific entities | Product has specialty modules — gap |
| Family health history | ⚠️ Partial | May be in C-CDA; no FHIR FamilyMemberHistory resource listed | Certified for family health history but no dedicated export entity |
| Social/behavioral data | ⚠️ Partial | May be captured in Observation; certified for (a)(15) | No explicit export entity |

## 6. Documentation Quality

The documentation quality is **very poor**:

- **No data dictionary**: Zero field-level documentation for any export component.
- **No schema**: No machine-readable format definitions for the Excel exports.
- **No sample data**: No examples of what the exported files contain.
- **No relationships/mappings**: No documentation of how internal data maps to C-CDA sections or FHIR resources.
- **Generic references only**: The C-CDA section points to the HL7 specification. The FHIR section points to the (g)(10) API doc which references US Core profiles. No product-specific documentation.
- **Supplemental exports undocumented**: The Excel files (Demographics & Insurance, Appointments) are described in one sentence each with no field listing.

A developer could not build an import from this documentation. The C-CDA and FHIR components could be consumed using standard parsers, but only the USCDI-scope data would be captured. The Excel exports have no documented structure whatsoever.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Minimal/stub/unclear**

The export documentation is a 4-page PDF that essentially points to existing C-CDA and FHIR (g)(10) exports and adds two undocumented Excel files and a document folder. The C-CDA and FHIR components are explicitly described as conforming to USCDI — this is the regulatory floor for clinical exchange, not a comprehensive EHI export. The supplemental Excel exports (demographics/insurance, appointments) could potentially add some depth, but with zero field documentation, their actual scope is unknowable. Major data domains the product stores — billing/claims, payments, secure messages, specialty-specific clinical data, order details — are entirely absent from the export documentation.

**Axis 2 — Export approach: Repackaged existing export**

The (b)(10) export is transparently built from pre-existing components:
- The C-CDA export is the standard (b)(1) transitions-of-care output, explicitly citing USCDI v1 and HL7 C-CDA R2.1 specs
- The FHIR Bulk Data export is the (g)(10) API, with the documentation literally titled "FHIR Documentation" and describing the same `fhirapi.cursahealth.com` API endpoint
- Two Excel files and a document folder were added as supplements, but without any documentation, they constitute a minimal effort to differentiate from pure (g)(10)

The telltale signs are unmistakable: documentation references USCDI, US Core, and HL7 specifications throughout with no product-specific data dictionary or schema. The FHIR documentation page is the same (g)(10) API documentation, not a purpose-built (b)(10) artifact.

### Key Findings

1. **Repackaged (g)(10) as (b)(10)**: The FHIR Bulk Data component of the export is explicitly the (g)(10) API, using the same documentation and endpoints. The C-CDA component is the standard (b)(1) transitions-of-care document. Neither has any vendor-specific extensions or customizations documented.

2. **Zero field-level documentation**: Across all export components, there is not a single documented field name, type, or description. The two Excel exports are described in one sentence each. No data dictionary, schema, or sample data exists.

3. **Billing/claims data missing despite being a product capability**: CursaHealth offers integrated billing, claims processing, and A/R management (priced at 6% of collections), but the (b)(10) export contains no billing entities whatsoever. This is a significant gap.

4. **Specialty clinical data absent**: The product supports specialty-specific modules for mental health, OB/GYN, and pediatrics, but the export makes no mention of specialty-specific data beyond what standard C-CDA/FHIR captures.

5. **Supplemental exports are a small step beyond pure repackaging**: The Demographics & Insurance Excel, Appointments Excel, and document folder show some awareness that (b)(10) should go beyond C-CDA/FHIR, but without documentation they contribute minimal verifiable value.

### Summary Stats

```
Coverage:        Minimal/stub/unclear
Approach:        Repackaged existing export
Export format:   C-CDA XML, FHIR R4, Excel, document files (PDF/JPG/PNG)
Entities:        21 (18 FHIR resources + 2 Excel exports + 1 document export)
Fields:          N/A (zero field-level documentation)
Descriptions:    N/A
Sample data:     No
Bulk export:     Yes (described but not detailed)
Domains covered: ~3 of 15 applicable domains (clinical notes/docs, partial demographics, partial appointments)
```

### Bottom Line

CursaHealth's (b)(10) export is essentially their existing C-CDA and FHIR (g)(10) clinical exchange rebranded, with two undocumented Excel files and a document folder added. A patient or provider would get a standard clinical summary — not a complete copy of their data. The single biggest gap is the complete absence of billing/claims data despite the product's integrated billing capabilities, compounded by the total lack of field-level documentation for any export component.
