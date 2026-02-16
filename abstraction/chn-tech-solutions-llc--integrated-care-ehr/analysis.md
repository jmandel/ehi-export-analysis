# EHI Export Analysis: CHN Tech Solutions LLC

**Product**: Integrated Care EHR (ICE)
**Analysis date**: 2026-02-16
**CHPL IDs**: 15.05.05.3133.CHTS.01.00.1.221213 (CHPL #11067)

## 1. Product Context

Integrated Care EHR (ICE) is a cloud-based EHR system built on the open-source OpenEMR platform, developed by CHN Tech Solutions LLC. The primary (and possibly sole) deployment is at MyCHN (Community Health Network), a Federally Qualified Health Center (FQHC) operating 19 locations across the Houston/Gulf Coast area providing primary care, pediatrics, women's health/OBGYN, behavioral health, dental, and pharmacy services.

**Key data domains the product stores:**
- **Clinical documentation**: SOAP notes across multiple specialties (primary care, pediatrics, women's health, psychiatry, therapy, MAT)
- **Screening/assessment data**: Extensive tools for SDOH, substance abuse, depression, fall risk, human trafficking, lead poisoning, vision, TB, smoking, dental, Zika
- **Billing/financial**: FQHC facility billing, fee-for-service billing, payment records, patient ledgers, payor aging
- **Medications/prescriptions**: E-prescribing via NewCrop/SureScripts
- **Lab results**: Interfaces with 20+ laboratories
- **Radiology/imaging**: Orders and results
- **Insurance data**: Coverage, enrollment, insurance companies
- **Patient portal**: Secure messaging, mobile apps
- **Dental data**: REST API includes `dental_issue` scopes (though extent unclear)
- **Surgical records**: REST API includes `surgery` scopes
- **Scheduling**: Appointments, no-show tracking

This is a small vendor with a feature-rich FQHC-oriented product. The OpenEMR REST API scopes reveal 23 distinct native data types, indicating the system stores significantly more data than what appears in the documented export.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `ehi-export-page.html` (47 KB) | Main (b)(10) page — 3 paragraphs stating C-CDA is the export format, with links to standard HL7 C-CDA IG specs | **Low** — no vendor-specific content |
| `fhir-api-page.html` (68 KB) | FHIR R4 API documentation — lists 21 CCD sections, Bulk FHIR export, $docref operation, SMART on FHIR support | **High** — most informative artifact for understanding export content |
| `rest-api-page.html` (78 KB) | OpenEMR native REST API documentation — 39 user scopes covering 23 data types including dental, insurance, surgery, SOAP notes | **High** — reveals data domains the product stores but doesn't export via (b)(10) |
| `standard-api-page.html` (82 KB) | Duplicate of REST API page — identical content | **Redundant** |
| `ccd-operation-in-fhir.html` (62 KB) | Step-by-step tutorial for generating CCD via $docref with Swagger screenshots | **Medium** — documents the export mechanism but not content |
| `ehi-export-page.png` (214 KB) | Screenshot of main EHI export page | **Low** — visual confirmation of page content |
| `ccd-operation-in-fhir-screenshot.png` (607 KB) | Screenshot of CCD tutorial page | **Low** — visual confirmation |
| `CCDA_Vol1_2022SEP_errata.pdf` (986 KB) | Standard HL7 C-CDA IG Volume 1 | **None** — generic HL7 standard, not vendor-specific |
| `CCDA_Vol2_2022SEP_errata.pdf` (7.2 MB) | Standard HL7 C-CDA IG Volume 2 (913 pages) | **None** — generic HL7 standard, not vendor-specific |

**Most informative**: `fhir-api-page.html` and `rest-api-page.html` — together they reveal the gap between what the product stores (23 native data types) and what the (b)(10) export covers (21 standard CCD sections).

**Least informative**: The two C-CDA IG PDFs are standard HL7 documents hosted on the vendor's site for convenience; they contain zero vendor-specific information.

## 3. Export Mechanics

- **Format**: C-CDA CCD (XML), conforming to C-CDA R2.1 standard
- **Mechanism**: FHIR `$docref` operation — an API call that generates a CCD on demand
- **Access**: Requires FHIR API client registration, OAuth2 authentication, and the `DocumentReference.$docref`, `DocumentReference.read`, and `Binary.read` scopes
- **Single-patient**: Yes — generates one CCD per patient per request
- **Bulk capability**: Not for (b)(10). A separate FHIR Bulk Data Export exists for (g)(10) but is not referenced as the (b)(10) mechanism
- **Date filtering**: Optional start/end date parameters filter encounter-related sections; 8 sections always include complete history
- **Retrieval**: CCD is generated, saved to patient's documents, and returned as a DocumentReference pointing to a Binary resource
- **Access constraints**: Requires developer-level API integration (client registration, OAuth2 flow, scope authorization). No simple UI button for non-technical users is documented
- **Fees**: Not mentioned

## 4. Export Content: What's In It

### No Data Dictionary

There is **no data dictionary** of any kind. Zero field-level documentation exists. The vendor provides:
- A list of 21 CCD section names (on the FHIR API page)
- Links to the generic HL7 C-CDA Implementation Guide (913 pages for Volume 2 alone)
- No vendor-specific mapping, no field definitions, no value sets, no sample data

A developer attempting to understand the export would need to:
1. Generate a CCD via the API (if they can access the system)
2. Parse the resulting XML against the generic C-CDA IG
3. Reverse-engineer what data elements are populated

### Vendor's own content organization

The vendor organizes the CCD into two groups based on date filtering behavior:

| Entity/Section | Fields | Described | Types | Category (vendor's) |
|---|---|---|---|---|
| History of Procedures | 0 | 0 | N/A | CCD (Date-Filterable) |
| Relevant DX Tests / LAB Data | 0 | 0 | N/A | CCD (Date-Filterable) |
| Functional Status | 0 | 0 | N/A | CCD (Date-Filterable) |
| Progress Notes | 0 | 0 | N/A | CCD (Date-Filterable) |
| Procedure Notes | 0 | 0 | N/A | CCD (Date-Filterable) |
| Laboratory Report Narrative | 0 | 0 | N/A | CCD (Date-Filterable) |
| Encounters | 0 | 0 | N/A | CCD (Date-Filterable) |
| Assessments | 0 | 0 | N/A | CCD (Date-Filterable) |
| Treatment Plan | 0 | 0 | N/A | CCD (Date-Filterable) |
| Goals | 0 | 0 | N/A | CCD (Date-Filterable) |
| Health Concerns | 0 | 0 | N/A | CCD (Date-Filterable) |
| Document Reason for Referral | 0 | 0 | N/A | CCD (Date-Filterable) |
| Mental Status | 0 | 0 | N/A | CCD (Date-Filterable) |
| Demographics | 0 | 0 | N/A | CCD (Full Record) |
| Allergies, Adverse Reactions, Alerts | 0 | 0 | N/A | CCD (Full Record) |
| History of Medication Use | 0 | 0 | N/A | CCD (Full Record) |
| Problem List | 0 | 0 | N/A | CCD (Full Record) |
| Immunizations | 0 | 0 | N/A | CCD (Full Record) |
| Social History | 0 | 0 | N/A | CCD (Full Record) |
| Medical Equipment | 0 | 0 | N/A | CCD (Full Record) |
| Vital Signs | 0 | 0 | N/A | CCD (Full Record) |

All 21 sections have **zero** vendor-documented fields. The "Fields" and "Described" columns are 0 because the vendor provides no field-level information whatsoever — only section names.

### What the REST API reveals about stored data

While not part of the (b)(10) export, the OpenEMR native REST API (documented on `rest-api-page.html`) exposes 23 data types via user scopes, revealing data domains the system stores:

| OpenEMR Data Type | Read | Write | In CCD? |
|---|---|---|---|
| allergy | ✅ | ✅ | ✅ (via Allergies section) |
| appointment | ✅ | ✅ | ❌ |
| dental_issue | ✅ | ✅ | ❌ |
| document | ✅ | ✅ | ❌ |
| drug | ✅ | — | ❌ |
| encounter | ✅ | ✅ | ✅ (via Encounters section) |
| facility | ✅ | ✅ | ❌ |
| immunization | ✅ | — | ✅ (via Immunizations section) |
| insurance | ✅ | ✅ | ❌ |
| insurance_company | ✅ | ✅ | ❌ |
| insurance_type | ✅ | — | ❌ |
| list | ✅ | — | ❌ |
| medical_problem | ✅ | ✅ | ✅ (via Problem List section) |
| medication | ✅ | ✅ | ✅ (via Medications section) |
| message | — | ✅ | ❌ |
| patient | ✅ | ✅ | ✅ (via Demographics section) |
| practitioner | ✅ | ✅ | ❌ |
| prescription | ✅ | — | ❌ (separate from med list) |
| procedure | ✅ | — | ✅ (via Procedures section) |
| soap_note | ✅ | ✅ | ❌ (CCD has Progress Notes but not full SOAP) |
| surgery | ✅ | ✅ | ❌ |
| transaction | ✅ | ✅ | ❌ |
| vital | ✅ | ✅ | ✅ (via Vital Signs section) |

Of the 23 native data types, only ~8 have clear CCD equivalents. 15 data types are accessible via the REST API but have no representation in the (b)(10) CCD export.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor's (b)(10) export is a standard C-CDA CCD document with 21 sections. The vendor provides zero customization, extension, or vendor-specific detail beyond the standard CCD template. The documentation consists of:

1. A brief paragraph saying "we use C-CDA" with links to HL7 standards
2. A list of 21 CCD section names categorized by date-filtering behavior
3. A tutorial for calling the FHIR $docref API to generate the CCD
4. Two standard HL7 C-CDA IG PDFs (not vendor-specific)

There is no depth — no field-level documentation, no data dictionary, no value sets, no sample data, no mapping between internal data and CCD elements. The CCD covers standard clinical summary domains (demographics, allergies, medications, problems, immunizations, vitals, encounters, procedures, labs, notes, goals, care plans) but cannot structurally carry billing, insurance, dental, scheduling, messaging, or surgical records.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | CCD "Demographics" section (no field detail) | CCD provides basic demographics; likely missing SDOH details, custom fields stored in OpenEMR |
| Encounters / visits | ⚠️ Partial | CCD "Encounters" section (date-filterable) | Basic encounter data; depth unknown without field documentation |
| Problems / conditions | ⚠️ Partial | CCD "Problem List" section | Standard problem list; REST API has separate `medical_problem` type suggesting richer internal model |
| Medications / prescriptions | ⚠️ Partial | CCD "History of Medication Use" section | Medication list present; but `prescription` is a separate REST API type not in CCD — e-prescribing details (NewCrop/SureScripts routing, dispense history) likely omitted |
| Allergies | ⚠️ Partial | CCD "Allergies, Adverse Reactions, Alerts" section | Section present but field depth unknown |
| Immunizations | ⚠️ Partial | CCD "Immunizations" section | Present but field depth unknown |
| Vitals | ⚠️ Partial | CCD "Vital Signs" section — latest only | **Only latest vitals** included per documentation; historical vitals excluded |
| Lab results | ⚠️ Partial | CCD "Relevant DX Tests / LAB Data" and "Laboratory Report Narrative" sections | Present but unknown whether results from all 20+ interfaced labs are represented |
| Imaging / diagnostic reports | ⚠️ Partial | CCD may include in DX Tests section | No explicit imaging section; unclear coverage |
| Procedures | ⚠️ Partial | CCD "History of Procedures" and "Procedure Notes" sections | Basic procedures present; but `surgery` is a separate REST API type not in CCD |
| Clinical notes / documents | ⚠️ Partial | CCD "Progress Notes" and "Procedure Notes" sections | Progress/procedure notes present; but `soap_note` is separate REST API type. `document` (uploaded docs/attachments) not in CCD |
| Care plans / goals | ⚠️ Partial | CCD "Treatment Plan", "Goals", "Health Concerns" sections | Present at section level; field depth unknown |
| Orders / referrals | ⚠️ Partial | CCD "Document Reason for Referral" section | Referral reasons included; full order/referral workflows not captured |
| Insurance / coverage | ❌ Not covered | No insurance sections in CCD | Product stores insurance data (3 REST API types: `insurance`, `insurance_company`, `insurance_type`); significant gap |
| Claims / billing | ❌ Not covered | No billing data in CCD | Product does FQHC facility billing and fee-for-service; major gap |
| Payments | ❌ Not covered | No payment data in CCD | `transaction` REST API type suggests financial records exist; not exported |
| Consents / directives | ❌ Not covered | No consent sections in CCD | N/A — no evidence product stores formal advance directives |
| Patient communications | ❌ Not covered | No messaging data in CCD | REST API has `message` scope; patient portal secure messaging not exported |
| Dental (specialty) | ❌ Not covered | No dental data in CCD | REST API has `dental_issue` scopes; MyCHN provides dental services; gap |
| Behavioral health (specialty) | ⚠️ Partial | CCD "Mental Status" section; potentially in Progress Notes | Product has psychiatry, therapy, MAT modules; CCD unlikely to capture specialty assessment forms |
| Screening assessments | ⚠️ Partial | CCD "Assessments" and "Functional Status" sections | Product has 10+ screening tools (SDOH, substance abuse, depression, etc.); unclear how much maps to standard CCD templates |
| Surgical records | ❌ Not covered | No surgery section in CCD | REST API has `surgery` scopes; not exported |

**Summary**: Of 21 applicable domains, 0 are fully covered (all marked partial due to zero field documentation), 12 have partial/possible coverage through CCD sections, and 7 are clearly not covered despite the product storing that data (insurance, billing, payments, messaging, dental, surgical records, uploaded documents).

## 6. Documentation Quality

**Overall**: Very poor for (b)(10) purposes.

- **Data dictionary**: None. Zero field-level documentation exists.
- **Schema/format documentation**: The vendor relies entirely on the generic HL7 C-CDA R2.1 standard (linking to 913-page HL7 PDFs). No vendor-specific mapping, constraints, or extensions are documented.
- **Sample data**: None. No example CCD exports are provided.
- **Machine-readable artifacts**: None. No schemas, no JSON definitions, no template examples.
- **Procedural documentation**: The $docref tutorial with Swagger screenshots is clear and followable — this is the strongest aspect of the documentation.
- **Developer usability**: A developer could generate a CCD by following the tutorial, but would have no way to understand the content structure without reverse-engineering the resulting XML against the 913-page C-CDA IG. There is no vendor-specific documentation to tell a developer which fields are populated, which value sets are used, or how internal data maps to CCD elements.

**Could a developer build an import from this documentation?** No. They would need to: (1) gain API access to the system, (2) generate sample CCDs, (3) reverse-engineer the XML structure, and (4) hope the generic C-CDA IG covers all vendor-specific choices. The documentation provides zero guidance for this.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Minimal/stub/unclear**

The (b)(10) export is a standard C-CDA CCD covering 21 clinical summary sections. With zero field-level documentation, there is no way to assess the actual depth of coverage within those sections. More critically, the CCD format structurally cannot carry multiple data domains the product stores: billing/financial data (FQHC facility billing, fee-for-service, payments, patient ledgers), insurance enrollment details, dental records, surgical records, uploaded documents, patient messages, and specialty screening tool results. The REST API scope list reveals 15 data types with no CCD equivalent, demonstrating a large gap between what the system stores and what the (b)(10) export covers.

The vendor's Vital Signs documentation states only "the latest vitals recorded" are included — explicitly excluding historical vital signs, which is a further indicator that even within covered domains, completeness is not a priority.

**Axis 2 — Export approach: Repackaged existing export**

The (b)(10) export is the FHIR `$docref` CCD generation operation — the same mechanism used for (g)(10) clinical exchange. The documentation on the EHI export page says simply "Integrated Care EHR exports patient data using the C-CDA" and links to the generic HL7 C-CDA IG. There is no purpose-built EHI export, no database dump, no additional data types beyond the standard CCD, and no vendor-specific data dictionary. The FHIR Bulk Data Export (also documented on the site) could theoretically export more FHIR resource types, but it too is a (g)(10) mechanism and not referenced as (b)(10). The EHI export page makes no attempt to address the designated record set beyond equating it with a clinical summary document.

### Key Findings

1. **Export is a standard C-CDA CCD with zero vendor-specific documentation.** The entire (b)(10) offering is a link to the FHIR $docref operation and two HL7 standard PDFs. No data dictionary, no field definitions, no sample data, no mapping exists. (Sources: `ehi-export-page.html`, `fhir-api-page.html`)

2. **REST API reveals 15 data types not covered by the CCD export.** The OpenEMR native REST API documentation (`rest-api-page.html`) exposes scopes for `dental_issue`, `insurance`, `insurance_company`, `insurance_type`, `surgery`, `soap_note`, `transaction`, `document`, `prescription`, `appointment`, `message`, `drug`, `facility`, `list`, and `medical_problem` (as distinct from the CCD Problem List) — none of which are exported via the (b)(10) mechanism.

3. **Billing data entirely absent despite FQHC billing being a core product feature.** The product supports FQHC facility billing, fee-for-service billing, payments, and patient ledgers. None of this is in the CCD export, and no alternative billing export is documented.

4. **Vital signs export is explicitly incomplete.** The documentation states the Vital Signs CCD section shows "the latest vitals recorded for the patient" — excluding historical vital sign readings, which are core clinical data.

5. **No sample data or machine-readable schemas exist.** A developer cannot assess export completeness without access to the live system to generate test CCDs.

### Summary Stats

    Coverage:        Minimal/stub/unclear
    Approach:        Repackaged existing export
    Export format:   C-CDA CCD (XML)
    Entities:        21 CCD sections (no field-level detail)
    Fields:          N/A (no data dictionary)
    Descriptions:    N/A
    Sample data:     No
    Bulk export:     No (single patient via $docref)
    Domains covered: ~12 of 21 applicable domains (partial, with 7 clear gaps)

### Bottom Line

A patient requesting their EHI from this system would receive a standard C-CDA clinical summary document — essentially the same document used for transitions of care. This covers basic clinical data (problems, meds, allergies, labs, notes) but omits billing records, insurance details, dental data, surgical records, patient messages, and detailed specialty assessments that the FQHC stores. The single biggest gap is the absence of any billing/financial data export from a product whose core value proposition includes FQHC facility billing. The single biggest documentation gap is the complete absence of any data dictionary — there is literally zero field-level information about what the export contains.
