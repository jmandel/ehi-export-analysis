# EHI Export Analysis: Radysans, Inc

**Product**: Radysans EHR v5.0
**Analysis date**: 2026-02-16
**CHPL IDs**: 15.04.04.2912.Rady.05.00.1.191231

## 1. Product Context

Radysans EHR is an integrated ambulatory EHR and practice management platform targeting small outpatient clinics, developed by Radysans, Inc (Apex, NC). The product is cloud-hosted (ehr.cutecharts.com) and offered as SaaS. It is certified across 40+ ONC criteria.

The product is a **full-spectrum ambulatory platform** with the following data-generating modules:
- **EMR**: Demographics, problems, medications, allergies, vitals, lab results, clinical notes, implantable devices, social history, care plans, immunizations
- **Practice Management (PMS)**: Scheduling, patient registration, insurance eligibility, referral management, message routing
- **eBilling**: Charge capture, claim scrubbing, electronic claim submission (2,500+ payers), payment posting, denial tracking, EOB/ERA processing, patient statements
- **Patient Portal**: Patient access to health information, patient representative login
- **Order Entry**: CPOE for medications, labs, diagnostic imaging
- **Transcription Services**: Medical transcription with long-term document storage

The vendor explicitly markets integrated billing/RCM as a core capability. This means a (b)(10) export should cover both clinical and billing/financial data domains.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `B-10-Documentation.pdf` (1 page, 61 KB) | The sole (b)(10) export documentation. Lists 22 C-CDA section names and references the (g)(10) FHIR API. No data dictionary, no field-level detail. | **Primary but extremely thin** |
| `G10ApplicationAccessTermsandCondition.pdf` (41 pages, 311 KB) | (g)(10) FHIR API documentation with OAuth2 flow, 18 FHIR resource endpoints, sample JSON responses, and API Terms of Use. | **Informative for understanding the FHIR scope** |
| `RadysansEHRCostsandLimitations.pdf` (2 pages, 582 KB) | Mandatory disclosure of costs. Notes a "one-time fee per provider" for data portability/extraction. | **Confirms data extraction has associated fees** |
| `fhir-endpoint-bundle.json` (1.2 KB) | FHIR Bundle with Endpoint and Organization resources confirming API base URL. | **Minimal — confirms infrastructure only** |
| `screenshot-onc-certification-page.png` (275 KB) | Screenshot of the ONC certification page with links. | **Orientation only** |

## 3. Export Mechanics

- **Formats**: C-CDA (HL7 CDA XML) and FHIR R4 (JSON via REST API)
- **Mechanism**: The C-CDA export is described as "bulk export of HL7 CCDA xml files." The FHIR export is via the standard (g)(10) API (OAuth2-authorized REST endpoints). No UI screenshots or step-by-step export instructions are provided.
- **Scope**: Single patient and "patient population" per the (b)(10) document
- **Access constraints**: The Costs and Limitations document lists a "one-time fee per provider upon request of data extraction" for "Data Portability"
- **No sample export files** are provided

## 4. Export Content: What's In It

### No data dictionary exists

The (b)(10) documentation provides **zero field-level documentation**. It consists of:
1. A list of 22 C-CDA section names with a link to the HL7 C-CDA specification website
2. A reference to the (g)(10) FHIR API documentation for FHIR-based export

The (g)(10) document lists 18 FHIR resource types with their API endpoints, query parameters, and sample JSON responses. All 18 are standard US Core STU 3.1.1 resources with no vendor-specific extensions observed in any sample output.

### Vendor's own content organization

The vendor does not organize content into their own categories. The only structure is the two export formats:

**C-CDA Sections (22):**

| Section Name | Fields Documented | Source |
|---|---|---|
| Allergies, Adverse Reactions, Alerts | 0 | B-10-Documentation.pdf |
| Assessment Plan | 0 | B-10-Documentation.pdf |
| Chief Complaint | 0 | B-10-Documentation.pdf |
| Cognitive Status | 0 | B-10-Documentation.pdf |
| Demographics | 0 | B-10-Documentation.pdf |
| Reason for Visit / Encounters | 0 | B-10-Documentation.pdf |
| Family History | 0 | B-10-Documentation.pdf |
| Functional Status | 0 | B-10-Documentation.pdf |
| Goals | 0 | B-10-Documentation.pdf |
| Health Concerns | 0 | B-10-Documentation.pdf |
| Immunizations | 0 | B-10-Documentation.pdf |
| Instructions | 0 | B-10-Documentation.pdf |
| Lab Results | 0 | B-10-Documentation.pdf |
| Medical Equipment UDI | 0 | B-10-Documentation.pdf |
| Medications | 0 | B-10-Documentation.pdf |
| Plan of Care | 0 | B-10-Documentation.pdf |
| Problem List | 0 | B-10-Documentation.pdf |
| Procedures | 0 | B-10-Documentation.pdf |
| Reason for Referral | 0 | B-10-Documentation.pdf |
| Social History | 0 | B-10-Documentation.pdf |
| Plan of Treatment | 0 | B-10-Documentation.pdf |
| Vitals | 0 | B-10-Documentation.pdf |

**FHIR Resources (18):**

| Resource Type | US Core | Sample Output | Vendor Extensions | Source |
|---|---|---|---|---|
| AllergyIntolerance | ✅ | Yes | None | G10 PDF §1.1 |
| CarePlan | ✅ | Yes | None | G10 PDF §1.2 |
| CareTeam | ✅ | Yes | None | G10 PDF §1.3 |
| Condition | ✅ | Yes | None | G10 PDF §1.4 |
| Device | ✅ | Yes | None | G10 PDF §1.5 |
| DiagnosticReport | ✅ | Yes | None | G10 PDF §1.6 |
| DocumentReference | ✅ | Yes | None | G10 PDF §1.7 |
| Encounter | ✅ | Yes | None | G10 PDF §1.8 |
| Goal | ✅ | Yes | None | G10 PDF §1.9 |
| Immunization | ✅ | Yes | None | G10 PDF §1.10 |
| MedicationRequest | ✅ | Yes | None | G10 PDF §1.11 |
| Observation | ✅ | Yes | None | G10 PDF §1.12 |
| Organization | ✅ | Yes | None | G10 PDF §1.13 |
| Patient | ✅ | Yes | None | G10 PDF §1.14 |
| Practitioner | ✅ | Yes | None | G10 PDF §1.15 |
| PractitionerRole | ✅ | Yes | None | G10 PDF §1.16 |
| Procedure | ✅ | Yes | None | G10 PDF §1.17 |
| Provenance | ✅ | Yes | None | G10 PDF §1.18 |

All 18 FHIR resources are standard US Core STU 3.1.1 — the exact set required for (g)(10) certification. No additional resources, no vendor extensions, no custom mappings.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor's (b)(10) export covers exactly two things:
1. **Standard C-CDA sections** — 22 sections matching USCDI v1, with no product-specific field documentation. The vendor simply lists section names and links to the HL7 C-CDA spec.
2. **Standard (g)(10) FHIR API** — 18 US Core resource types, which are exactly the resources required for ONC (g)(10) certification. The sample outputs show standard US Core conformant resources with no vendor-specific extensions.

There is no evidence of any content beyond what the existing (g)(10) and C-CDA clinical exchange capabilities already provide. The (b)(10) document is literally 1 page and explicitly says to "refer 170.315(g)(10)" for the FHIR export specification.

The export covers USCDI clinical domains only. There is **no coverage whatsoever** of:
- Billing, claims, charges, or financial data
- Insurance/coverage details beyond what's in the Patient resource
- Practice management data (scheduling, referrals)
- Patient communications or portal messages
- Custom forms or intake documents
- Scanned documents or transcription records
- Denial tracking or payment data

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | C-CDA Demographics section; FHIR Patient resource | Standard USCDI fields only |
| Encounters / visits | ✅ Covered | C-CDA Encounters section; FHIR Encounter resource | Standard USCDI fields only |
| Problems / conditions | ✅ Covered | C-CDA Problem List; FHIR Condition resource | Standard USCDI fields only |
| Medications / prescriptions | ✅ Covered | C-CDA Medications; FHIR MedicationRequest resource | Standard USCDI fields only |
| Allergies | ✅ Covered | C-CDA Allergies section; FHIR AllergyIntolerance | Standard USCDI fields only |
| Immunizations | ✅ Covered | C-CDA Immunizations; FHIR Immunization | Standard USCDI fields only |
| Vitals | ✅ Covered | C-CDA Vitals; FHIR Observation | Standard USCDI fields only |
| Lab results | ✅ Covered | C-CDA Lab Results; FHIR DiagnosticReport, Observation | Standard USCDI fields only |
| Imaging / diagnostic reports | ⚠️ Partial | FHIR DiagnosticReport covers some imaging; no dedicated imaging section | No imaging narratives in C-CDA sections |
| Procedures | ✅ Covered | C-CDA Procedures; FHIR Procedure | Standard USCDI fields only |
| Clinical notes / documents | ⚠️ Partial | FHIR DocumentReference available; no sample showing clinical note content | Unclear what note types are exported |
| Care plans / goals | ✅ Covered | C-CDA Plan of Care/Treatment, Goals; FHIR CarePlan, Goal | Standard USCDI fields only |
| Orders / referrals | ⚠️ Partial | C-CDA "Reason for Referral" section; MedicationRequest for med orders | No ServiceRequest resource; referral workflows not covered |
| Insurance / coverage | ❌ Not covered | No Coverage resource; no insurance entity | Product stores insurance data (Registration module); **significant gap** |
| Claims / billing | ❌ Not covered | No billing entities whatsoever | Product has full eBilling module with claims, charges, denials, EOBs; **major gap** |
| Payments | ❌ Not covered | No payment data | Product handles payment posting and reconciliation; **significant gap** |
| Consents / directives | ❌ Not covered | No consent entities | Product scans regulatory documents per Registration module |
| Patient communications | ❌ Not covered | No messaging or portal communication data | Product has patient portal and Message Manager; **gap** |
| Specialty-specific data | N/A | No specialty modules documented | Product is general ambulatory; no specialty-specific modules identified |

## 6. Documentation Quality

The (b)(10) documentation is **extremely poor**:

- **No data dictionary at all**: Zero field-level documentation. Not a single field name, type, or description is provided for either the C-CDA or FHIR export beyond what's in the referenced standards.
- **No product-specific mapping**: The vendor does not explain how their internal data maps to C-CDA sections or FHIR resources. A developer would have no idea what Radysans-specific data ends up in each section/resource.
- **No sample export files**: While the (g)(10) PDF includes sample JSON for each FHIR resource type, no actual C-CDA sample documents or complete export packages are provided.
- **No machine-readable schema**: No JSON Schema, no XML Schema, no structural documentation of any kind.
- **No value sets or code systems**: Beyond the standard terminologies visible in FHIR samples (SNOMED, RxNorm, LOINC), no product-specific value sets are documented.
- **No relationship documentation**: No entity relationships, no foreign key documentation.

A developer could not build an import from this documentation. They would need to rely entirely on the generic HL7 C-CDA and FHIR specifications, with no knowledge of what Radysans-specific data would actually appear in the export.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Minimal/stub**

The (b)(10) documentation is a single page that lists C-CDA section names and points to the existing (g)(10) FHIR API. It covers only USCDI clinical domains. The product has significant billing/RCM capabilities (charge capture, claim submission to 2,500+ payers, payment posting, denial tracking, EOB/ERA processing) — none of which appear in the export. Practice management data (scheduling, referrals, insurance eligibility), patient portal communications, and scanned documents are also absent. The documentation is too thin to even confirm what fields within the clinical domains are actually exported.

**Axis 2 — Export approach: Repackaged existing export**

This is a textbook case of repackaging. The (b)(10) document explicitly references the (g)(10) API as the FHIR export mechanism — it is literally the same API. The C-CDA export appears to be the standard transitions-of-care C-CDA also used for (b)(1) certification. Both exports are limited to USCDI scope. There are no vendor extensions, no additional resource types, no product-specific data dictionary, and no coverage of data domains (billing, insurance, scheduling) that go beyond clinical exchange. The entire (b)(10) "documentation" is 1 page pointing to existing clinical exchange specs.

### Key Findings

1. **The (b)(10) export is explicitly the (g)(10) API plus C-CDA, relabeled.** The 1-page B-10-Documentation.pdf says to "refer 170.315(g)(10)" for FHIR specifications. All 18 FHIR resources are standard US Core with zero vendor extensions. This is not a purpose-built EHI export.

2. **Major billing gap despite significant billing capabilities.** Radysans advertises electronic claim submission to 2,500+ payers, payment posting, denial tracking, and EOB/ERA processing — an entire eBilling module. None of this data appears in the (b)(10) export.

3. **Zero field-level documentation.** The vendor provides no data dictionary, no field mappings, no value sets. The entirety of the (b)(10) content documentation is a bullet list of 22 C-CDA section names and a pointer to the generic HL7 spec.

4. **Data extraction carries a fee.** The Costs and Limitations document specifies a "one-time fee per provider" for data portability/extraction, which may create a barrier to patients exercising their (b)(10) rights.

5. **No sample export data provided.** While the (g)(10) PDF includes sample FHIR JSON responses for individual resources, no complete export package or C-CDA sample is available for evaluation.

### Summary Stats

    Coverage:        Minimal/stub
    Approach:        Repackaged existing export
    Export format:   C-CDA XML, FHIR R4 JSON
    Entities:        40 (22 C-CDA sections + 18 FHIR resources, all standard)
    Fields:          N/A (no field-level documentation)
    Descriptions:    N/A
    Sample data:     No (only sample FHIR JSON in API docs)
    Bulk export:     Claimed for C-CDA; FHIR via (g)(10) API
    Domains covered: ~12 of 18 applicable (clinical only; no billing, insurance, payments, communications, consents)

### Bottom Line

Radysans EHR's (b)(10) export is a 1-page document that rebrands the existing C-CDA and (g)(10) FHIR API as the EHI export. It covers only USCDI clinical domains while the product stores significant billing, insurance, and practice management data that is entirely absent. A patient or provider would receive a clinical summary, not a complete copy of their designated record set — and they would pay a per-provider fee for it.
