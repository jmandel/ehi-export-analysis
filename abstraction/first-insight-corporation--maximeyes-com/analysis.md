# EHI Export Analysis: First Insight Corporation

**Product**: MaximEyes.com v1.1
**Analysis date**: 2026-02-16
**CHPL IDs**: 10470

## 1. Product Context

MaximEyes.com is a cloud-based (Azure-hosted), specialty EHR and practice management platform built exclusively for ophthalmology and optometry. Developed by First Insight Corporation (Hillsboro, OR; ~50 employees; in business since 1994), it serves thousands of eye care practices including large chains like U.S. Vision (600+ locations).

The product is a **full-scope practice operations system** covering:
- **Clinical documentation**: Structured ophthalmic/optometric exams (visual acuity, IOP, slit lamp, fundus exam, refraction), SOAP notes, AI-assisted scribing (EVAA), problem lists, medication lists, allergy lists, family history, implantable device tracking (IOLs)
- **Practice management**: Scheduling, patient registration, insurance verification, recalls, waitlists
- **Revenue cycle / billing**: End-to-end claims management, ERA/EOB auto-posting, accounts receivable, VSP claims integration
- **Optical point-of-sale**: Frame catalog, contact lens orders, lab orders, barcode scanning, inventory tracking
- **Patient engagement**: Patient portal (EyeClinic.net), secure messaging, online intake forms, telehealth
- **Diagnostic imaging**: OCT, fundus cameras, visual fields — cloud-stored, linked to patient records
- **E-prescribing**: Via DrFirst Rcopia (pharmaceutical, eyeglass, contact lens prescriptions)
- **Quality reporting**: MIPS/PQRS, IRIS Registry, MORE Registry integrations

This breadth means a genuine (b)(10) export should cover significantly more than USCDI clinical data — it should include billing/claims, optical retail data, specialty eye exam structures, images, and patient communications.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/MaximEyes-EHI-Export-Documentation.pdf` | 4-page PDF (dated 03/17/25) describing how to perform the EHI export. Lists 15 "Scope of EHI" categories, export UI screenshots, API endpoint details. | **Primary EHI doc** — thin but informative about scope and mechanism |
| `downloads/MaximEyes-FHIR-API-Documentation.pdf` | 40-page PDF (dated 03/17/25) documenting the FHIR R4 API: SMART authorization, 20 FHIR resource types with search parameters, USCDI data class mappings. | **Core reference** — but this is the (g)(10) FHIR API doc, not a (b)(10) data dictionary |
| `downloads/swagger-v1.json` | 448 KB OpenAPI 3.0.1 spec from `fhir.maximeyes.com`. 59 paths covering all FHIR endpoints. Reveals 3 additional billing-related resources (Account, ChargeItem, Coverage) not in the PDF. | **Most revealing artifact** — shows undocumented billing resources, but has no response schemas |

The EHI Export Documentation PDF is the only artifact specifically written for (b)(10). The FHIR API Documentation PDF is the (g)(10) reference document repurposed by reference.

## 3. Export Mechanics

- **Format**: FHIR R4 NDJSON via Bulk Data 1.0.1 protocol
- **Mechanism**: Both UI-based and API-based:
  - **UI**: Reports → Incentive Programs → Electronic Health Information; select single patient or "All Patients" checkbox; download ZIP
  - **API**: `GET /api/{customerName}/R4/Patient/Export` with JWK token authentication
- **Single-patient**: Yes (via UI patient selector)
- **Bulk/all-patient**: Yes (via "All Patient" checkbox or system-level Export endpoint)
- **Output files**: ZIP containing NDJSON files named `PatientID_Date_ResourceType`
- **Query parameters**: `_since` (incremental export since date), `_type` (filter by resource type)
- **Access constraints**: Requires user permissions within MaximEyes.com; API requires JWK token (300s lifetime)
- **Fees**: Not mentioned; FHIR API access is stated as "free of charge" for app developers

## 4. Export Content: What's In It

### No data dictionary exists

There is **no field-level data dictionary** for the EHI export. The documentation provides:
1. A 15-item bulleted list of "Scope of EHI" categories (page 4 of EHI export PDF)
2. USCDI data class mappings for 20 FHIR resource types (FHIR API PDF)
3. Search parameters for each resource type (FHIR API PDF)
4. An OpenAPI/Swagger spec with endpoint definitions but **no response schemas** (all 200 responses return only "Success" with no body definition)

There are **no sample data files**, **no field-level documentation**, **no value set definitions**, and **no schema for what data elements appear in each FHIR resource**.

### Resource types in the export

The export covers 23 FHIR resource types: 20 documented in the FHIR API PDF and 3 additional (Account, ChargeItem, Coverage) found only in the Swagger spec.

### Vendor's own content organization

The EHI Export Documentation PDF (page 4) lists 15 "Scope of EHI" categories. Below is how these map to FHIR resources, plus the 3 undocumented Swagger resources:

| EHI Scope Category | FHIR Resource(s) | Documented in PDF | Notes |
|---|---|---|---|
| Patient Demographic | Patient | Yes | 12 USCDI elements listed (name, DOB, race, etc.) |
| Social History | Observation (social-history) | Yes | Only Smoking Status documented |
| Problems | Condition | Yes | Health Concerns + Problems + Encounter Diagnoses |
| Medications | MedicationRequest, Medication | Yes | Search params reference internal tables |
| Allergies and Reactions | AllergyIntolerance | Yes | Substance (Medication/Drug Class), Reaction |
| Diagnostic Results | DiagnosticReport, Observation (laboratory) | Yes | Lab reports, imaging narrative, pathology |
| Vital signs | Observation (vital-signs) | Yes | Standard vital sign profiles |
| Encounter Diagnoses | Condition (encounter-diagnosis category) | Yes | Shares Condition resource |
| Procedures | Procedure | Yes | References SNOMED codes |
| Care team members | CareTeam, Practitioner, PractitionerRole | Yes | Standard US Core profiles |
| Immunizations | Immunization | Yes | Date administered tracked |
| Assessment and plan of treatment | CarePlan | Yes | assess-plan category |
| Goals | Goal | Yes | Patient Goals |
| Insurance Providers | Organization, Coverage* | Partial | Organization in PDF; Coverage only in Swagger |
| Accounts | Account*, ChargeItem* | No | Only in Swagger; not documented in PDF |

*Resources marked with asterisk are present in the Swagger API but **not documented** in the FHIR API PDF — no search parameters, no USCDI mappings, no examples.

Additional resources not in the "Scope of EHI" list but in the API:
- **Device** (Implantable devices — IOLs)
- **DocumentReference** (Clinical notes: Consultation, Discharge Summary, H&P, Progress)
- **Encounter** (Visit information)
- **Location** (Facility information)
- **Provenance** (Author timestamps and organization)

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor's "Scope of EHI" (15 categories) maps directly to USCDI v3 data classes. The 20 documented FHIR resources are the standard US Core resource set required for the (g)(10) FHIR API certification. This is not a coincidence — the FHIR API PDF footer reads "MaximEyes FHIR API Documentation" and its content is explicitly a (g)(10) reference document.

The 3 undocumented Swagger resources (Account, ChargeItem, Coverage) represent a modest step beyond USCDI into billing territory, but:
- They have no documentation (no search parameters, no field descriptions, no examples)
- They cover only a fraction of the product's billing/financial data
- It's unclear whether they are included in the EHI export's `_type` parameter options or are API-only

The documented export is **exactly the USCDI/US Core clinical data surface** — no more, no less. The EHI scope list even uses USCDI terminology ("Assessment and plan of treatment," "Care team members").

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | Patient resource (12 USCDI elements) | Standard US Core demographics only; product likely stores more (e.g., employer, emergency contacts, patient preferences) |
| Encounters / visits | ✅ Covered | Encounter resource | Basic encounter data; no visit-level detail on exam type, room, duration |
| Problems / conditions / diagnoses | ✅ Covered | Condition resource (3 categories) | Standard problem list; no specialty-specific structured diagnoses |
| Medications / prescriptions | ✅ Covered | MedicationRequest, Medication | Pharmaceutical prescriptions; eyeglass/contact lens prescriptions (Rx/CLX) likely **not** covered |
| Allergies | ✅ Covered | AllergyIntolerance | Standard allergy recording |
| Immunizations | ✅ Covered | Immunization | Standard immunization recording |
| Vitals | ✅ Covered | Observation (vital-signs) | Standard vital signs |
| Lab results | ✅ Covered | Observation (laboratory), DiagnosticReport | Standard lab results |
| Imaging / diagnostic reports | ⚠️ Partial | DiagnosticReport (imaging narrative), DocumentReference | Report narratives likely covered; **actual diagnostic images** (OCT scans, fundus photos, visual fields) almost certainly **not** exported as binary attachments |
| Procedures | ✅ Covered | Procedure | Standard procedure recording |
| Clinical notes / documents | ✅ Covered | DocumentReference (4 note types) | Standard clinical note types; custom forms, intake forms, consent forms likely **not** included |
| Care plans / goals | ✅ Covered | CarePlan, Goal | Standard care plan and goals |
| Orders / referrals | ⚠️ Partial | MedicationRequest (intent=order) | Medication orders covered; no evidence of ServiceRequest for referrals or non-medication orders |
| Insurance / coverage | ⚠️ Partial | Coverage (Swagger only), Organization | Coverage resource exists but is undocumented; likely basic plan info only, not detailed eligibility/authorization data |
| Claims / billing | ⚠️ Partial | Account, ChargeItem (Swagger only) | Both undocumented; product has full claims management, ERA/EOB posting, AR tracking — almost certainly not fully covered |
| Payments | ❌ Not covered | No payment-related resources | Product tracks payments, AR; no evidence in export |
| Consents / directives | ❌ Not covered | No Consent resource | Product likely captures consent forms |
| Patient communications / portal messages | ❌ Not covered | No Communication resource | Product has patient portal (EyeClinic.net) with secure messaging |
| Specialty-specific (ophthalmology/optometry) | ❌ Not covered | No specialty resources or extensions | **Critical gap**: Product's core differentiator is structured ophthalmic data (visual acuity, IOP, slit lamp, fundus exam, refraction, etc.). FHIR US Core has no profiles for these. No vendor extensions documented. |
| Optical retail (frames, contacts, lab orders) | ❌ Not covered | No optical-related resources | Product has full optical POS; no export coverage |

**Key finding**: Of ~19 applicable domains, the export covers 10 fully (all USCDI-standard), 4 partially, and 5 not at all. The 5 missing domains include the product's most distinctive capabilities: specialty eye care data, optical retail, patient communications, payments, and consents.

## 6. Documentation Quality

**Overall**: Functional but thin; clearly repurposed (g)(10) documentation.

- **Strengths**: The EHI export PDF provides clear instructions with screenshots. The FHIR API PDF is a competent API reference (40 pages). The Swagger spec is machine-readable.
- **Weaknesses**:
  - No data dictionary — zero field-level documentation for any resource type
  - No sample export data or example NDJSON records
  - Swagger response schemas are empty (all 200 responses say "Success" with no body)
  - Three billing resources (Account, ChargeItem, Coverage) appear in the API but are completely undocumented
  - No documentation of vendor-specific FHIR extensions, custom value sets, or how MaximEyes-specific data maps to FHIR elements
  - No documentation of how data that doesn't fit standard FHIR resources is handled (or not)
- **Usability for a developer**: A developer could connect to the API and pull standard FHIR resources, but could not know what specific data elements to expect, what coding systems are used, or how to interpret MaximEyes-specific content. The documentation is sufficient for FHIR API consumption but insufficient for comprehensive data migration or analysis.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Partial**

The export covers standard USCDI clinical data well (demographics, problems, meds, allergies, vitals, labs, notes, procedures, immunizations, encounters, care plans, goals, care team). The presence of Account, ChargeItem, and Coverage in the Swagger API suggests some effort to include billing data beyond USCDI. However, the export is missing entire categories critical to an eye care practice: structured ophthalmic exam data (the product's core clinical value — visual acuity, IOP, slit lamp findings, refraction data, etc.), optical retail data (frames, contact lens orders, lab orders), diagnostic images (OCT, fundus photos, visual fields), patient portal communications, detailed billing workflow data (claims, ERA/EOBs, AR), and patient-reported forms. These omissions are significant because MaximEyes is not a generic EHR — it's a specialty system where the structured eye care data is the most clinically important content.

**Axis 2 — Export approach: Repackaged existing export**

This is a textbook case of (g)(10) FHIR API documentation being relabeled as (b)(10):
1. The FHIR API PDF was written for the FHIR API certification — its footer reads "MaximEyes FHIR API Documentation" on every page
2. The 20 documented resource types exactly match the US Core resource set required for (g)(10)
3. The "Scope of EHI" list on page 4 uses USCDI terminology verbatim
4. The export uses the same FHIR Bulk Data endpoint as the (g)(10) API
5. The EHI export PDF refers users to the FHIR API documentation "for details on the format of the exported files"
6. No product-specific data dictionary, no vendor extensions, no coverage of non-USCDI data domains

The 3 undocumented Swagger resources (Account, ChargeItem, Coverage) are the only evidence of anything beyond (g)(10), but they are completely undocumented and cover only a sliver of the product's billing capabilities.

### Key Findings

1. **The export is the (g)(10) FHIR API rebranded as (b)(10).** The 20 documented resource types, the USCDI-aligned scope list, and the shared Bulk Data endpoint all confirm this. The only EHI-specific document is a 4-page instruction sheet.

2. **The product's most distinctive data — structured ophthalmic exam findings — is absent from the export.** MaximEyes stores detailed visual acuity, IOP, slit lamp, fundus exam, and refraction data in structured form. FHIR US Core has no profiles for these, and no vendor extensions are documented. This is the single largest gap.

3. **Three billing resources (Account, ChargeItem, Coverage) appear in the Swagger API but are undocumented.** This suggests some effort to go beyond USCDI, but without documentation or field-level detail, their coverage of the product's full billing/RCM capabilities is unknowable.

4. **No data dictionary exists.** There is zero field-level documentation for any resource type. The FHIR API PDF documents search parameters only. The Swagger spec has endpoints but no response schemas. A developer cannot determine what data elements are included without calling the API.

5. **Optical retail data is entirely absent.** The product's optical POS module (frames, contact lenses, lab orders, inventory) represents patient-relevant data (eyeglass prescriptions, contact lens prescriptions) that has no representation in the export.

### Summary Stats

    Coverage:        Partial
    Approach:        Repackaged existing export
    Export format:   FHIR R4 NDJSON (Bulk Data 1.0.1)
    Entities:        23 FHIR resource types (20 documented + 3 Swagger-only)
    Fields:          N/A (no data dictionary)
    Descriptions:    N/A (no field-level documentation)
    Sample data:     No
    Bulk export:     Yes
    Domains covered: 10 of 19 applicable domains (fully); 4 partially; 5 not covered

### Bottom Line

MaximEyes.com's EHI export is its existing (g)(10) FHIR Bulk Data API relabeled as (b)(10), covering standard USCDI clinical data but missing the specialty ophthalmic exam data, optical retail records, diagnostic images, detailed billing/claims data, and patient communications that make up a significant portion of the designated record set for an eye care practice. A patient would get a generic clinical summary but not their structured eye exam findings, eyeglass/contact lens prescriptions, or billing history.
