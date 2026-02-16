# EHI Export Analysis: CHN Tech Solutions LLC

**Product**: Integrated Care EHR (ICE)  
**Analysis date**: 2026-02-16  
**CHPL IDs**: 11067 (15.05.05.3133.CHTS.01.00.1.221213)

## 1. Product Context

Integrated Care EHR (ICE) is a cloud-based EHR built on the open-source OpenEMR platform, developed by CHN Tech Solutions LLC. The product appears to serve primarily (possibly exclusively) MyCHN, a Federally Qualified Health Center (FQHC) operating 19 locations across the greater Houston/Gulf Coast area. CHN Tech Solutions is closely tied to MyCHN — the login portal is hosted at `ic-ehr.mychn.org`.

**Clinical workflows the product supports:**
- Primary care, pediatrics, women's health/OB-GYN (including high-risk pregnancy)
- Behavioral health (psychiatry, counseling, Medication Assisted Therapy)
- SOAP-note-based documentation across multiple specialties
- Extensive screening tools: SDOH, drug/alcohol abuse, depression, fall risk, human trafficking, lead poisoning, vision, TB, smoking, dental, Zika

**Billing/PM capabilities:**
- FQHC facility billing
- Traditional fee-for-service billing
- Financial reports (payments, patient ledger, payor aging, charges/collections)

**Other data domains:**
- E-prescribing (via NewCrop/SureScripts)
- Lab interfaces with 20+ laboratories
- Radiology connectivity
- Patient portal with secure messaging
- Immunization reporting
- UDS (Uniform Data System) reporting for FQHC compliance
- Chronic care management tracking and billing
- Scheduling and appointment tracking
- Dental services (MyCHN provides dental care; the REST API includes `dental_issue` scopes)

This is a feature-rich FQHC EHR. An adequate (b)(10) export should cover clinical documentation across multiple specialties, billing/claims data, insurance information, screening/assessment results, prescriptions, and dental records.

## 2. Artifacts Reviewed

| Artifact | Size | Description | Informativeness |
|---|---|---|---|
| `ehi-export-page.html` | 47 KB | Main (b)(10) EHI export page — 3 short paragraphs describing C-CDA as the export format, with links to IHE and HL7 standards | **Key** — defines the export mechanism |
| `ccd-operation-in-fhir.html` | 62 KB | 11-step Swagger tutorial for generating a CCD via FHIR `$docref` operation | **Key** — only procedural documentation for the export |
| `fhir-api-page.html` | 68 KB | FHIR R4/US Core 3.1 API documentation with Bulk FHIR, $docref CCD details, SMART on FHIR | **Key** — lists 21 CCD sections and 25 FHIR resource types |
| `rest-api-page.html` | 78 KB | OpenEMR-based REST API documentation with OIDC auth and scope listings | **Informative** — reveals 23 native OpenEMR data types beyond FHIR |
| `standard-api-page.html` | 82 KB | Duplicate of REST API page with minor formatting differences | **Redundant** |
| `ehi-export-page.png` | 214 KB | Screenshot of the EHI export page | Low (visual duplicate of HTML) |
| `ccd-operation-in-fhir-screenshot.png` | 607 KB | Screenshot of CCD tutorial with Swagger UI screenshots | Low (visual duplicate of HTML) |
| `CCDA_Vol1_2022SEP_errata.pdf` | 986 KB / 63 pages | HL7 C-CDA IG Volume 1 — standard HL7 document, NOT vendor-specific | **Not informative** for this analysis |
| `CCDA_Vol2_2022SEP_errata.pdf` | 7.2 MB / 913 pages | HL7 C-CDA IG Volume 2 — standard HL7 document, NOT vendor-specific | **Not informative** for this analysis |

**Most informative**: `ehi-export-page.html`, `fhir-api-page.html`, and `rest-api-page.html`. Together these define the export format, mechanism, CCD sections, and (via the REST API scopes) reveal what data domains the system stores but the CCD export doesn't cover.

**Least informative**: The two C-CDA IG PDFs are standard HL7 documents hosted on the vendor's site for convenience. They contain no vendor-specific information about what ICE actually exports.

## 3. Export Mechanics

- **Format**: C-CDA XML (Consolidated Clinical Document Architecture) — a single CCD document per patient
- **Mechanism**: FHIR `$docref` operation via Swagger UI. The tutorial walks through: (1) register an OAuth2 client, (2) set scopes, (3) authenticate, (4) select a patient, (5) call `$docref` endpoint, (6) download the resulting C-CDA binary
- **Single-patient**: Yes — the `$docref` operation generates a CCD for one patient at a time
- **Bulk capability**: The site documents FHIR Bulk Data Export (system, group, patient) for the (g)(10) criterion, but this is explicitly separate from the (b)(10) EHI export. The (b)(10) export is the CCD/$docref mechanism.
- **Date filtering**: Optional start/end date parameters filter encounter-related sections; 8 sections always include the full medical record
- **Access constraints**: Requires OAuth2 client registration. Only a testing endpoint is published (`chntech.from-tx.com`); no production endpoint is documented. The test endpoint's DNS did not resolve at collection time.
- **Fees**: Not mentioned

## 4. Export Content: What's In It

### What the export produces

The (b)(10) export is a single C-CDA CCD document per patient containing **21 documented sections**. There is **no data dictionary**, **no field-level documentation**, **no sample data**, and **no vendor-specific schema**. The vendor relies entirely on the generic HL7 C-CDA Implementation Guide (913-page Vol 2) as the format specification.

### CCD Sections

The FHIR API page (`fhir-api-page.html`) documents the following CCD sections:

**Date-filterable sections** (13 sections — filtered by date range when specified):

| Section | Source |
|---|---|
| History of Procedures | `fhir-api-page.html` |
| Relevant DX Tests / LAB Data | `fhir-api-page.html` |
| Functional Status | `fhir-api-page.html` |
| Progress Notes | `fhir-api-page.html` |
| Procedure Notes | `fhir-api-page.html` |
| Laboratory Report Narrative | `fhir-api-page.html` |
| Encounters | `fhir-api-page.html` |
| Assessments | `fhir-api-page.html` |
| Treatment Plan | `fhir-api-page.html` |
| Goals | `fhir-api-page.html` |
| Health Concerns | `fhir-api-page.html` |
| Document Reason for Referral | `fhir-api-page.html` |
| Mental Status | `fhir-api-page.html` |

**Full record sections** (8 sections — always include complete history):

| Section | Source |
|---|---|
| Demographics | `fhir-api-page.html` |
| Allergies, Adverse Reactions, Alerts | `fhir-api-page.html` |
| History of Medication Use | `fhir-api-page.html` |
| Problem List | `fhir-api-page.html` |
| Immunizations | `fhir-api-page.html` |
| Social History | `fhir-api-page.html` |
| Medical Equipment | `fhir-api-page.html` |
| Vital Signs (latest recorded) | `fhir-api-page.html` |

### What the REST API reveals the system stores (but CCD doesn't export)

The OpenEMR native REST API scopes (`rest-api-page.html`) reveal **23 data types** accessible via the native API. Many of these are NOT included in the C-CDA CCD export:

| OpenEMR API Resource | In CCD? | Notes |
|---|---|---|
| `allergy` | Yes | Mapped to CCD Allergies section |
| `appointment` | No | Scheduling data |
| `dental_issue` | No | Dental clinical records |
| `document` | No | Attached documents/files |
| `drug` | Partial | Drug reference data vs medication history |
| `encounter` | Yes | Mapped to CCD Encounters section |
| `facility` | N/A | Provider facility info |
| `immunization` | Yes | Mapped to CCD Immunizations section |
| `insurance` | No | Patient insurance/coverage data |
| `insurance_company` | No | Payor reference data |
| `insurance_type` | No | Insurance type reference data |
| `list` | Partial | Depends on list type |
| `medical_problem` | Yes | Mapped to CCD Problem List |
| `medication` | Yes | Mapped to CCD Medication Use |
| `message` | No | Patient-provider messages |
| `patient` | Yes | Mapped to CCD Demographics |
| `practitioner` | N/A | Provider info |
| `prescription` | No | Detailed prescription records beyond med list |
| `procedure` | Yes | Mapped to CCD Procedures |
| `soap_note` | Partial | CCD has Progress Notes but not full SOAP structure |
| `surgery` | Partial | May map to CCD Procedures |
| `transaction` | No | Billing/financial transactions |
| `vital` | Yes | Mapped to CCD Vital Signs |

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor's EHI export is a **C-CDA CCD document** — a clinical summary format designed for transitions of care. The vendor does not organize their export into custom categories; they simply point to the 21 standard CCD sections.

The CCD covers the standard clinical summary domains well: demographics, allergies, medications, problems, immunizations, vitals, procedures, labs, encounters, notes, care plans, goals, referrals, mental status, and medical equipment.

However, the CCD format structurally cannot carry several data types the system stores. The REST API scope list is the most revealing artifact because it exposes data domains (dental issues, insurance, transactions, SOAP notes, surgeries, prescriptions, messages, documents) that exist in the underlying OpenEMR database but are absent from the C-CDA export.

The vendor provides no documentation specific to their CCD implementation — no field mapping, no customizations, no extensions. A developer wanting to understand the actual content of the exported CCD would need to: (1) generate one from the API, and (2) parse the resulting XML against the generic 913-page C-CDA IG.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | CCD "Demographics" section (full record) | Standard CCD demographics |
| Encounters / visits | ✅ Covered | CCD "Encounters" section (date-filterable) | Present but detail level unknown |
| Problems / conditions / diagnoses | ✅ Covered | CCD "Problem List" section (full record) | Standard CCD problem list |
| Medications / prescriptions | ⚠️ Partial | CCD "History of Medication Use" (full record) | Medication list present; detailed prescription routing history (NewCrop/SureScripts) likely absent. REST API has separate `prescription` scope. |
| Allergies | ✅ Covered | CCD "Allergies, Adverse Reactions, Alerts" (full record) | Standard CCD allergies |
| Immunizations | ✅ Covered | CCD "Immunizations" section (full record) | Standard CCD immunizations |
| Vitals | ⚠️ Partial | CCD "Vital Signs" — "shows the latest vitals recorded" | Only latest vitals, not full history — significant limitation |
| Lab results | ✅ Covered | CCD "Relevant DX Tests / LAB Data" + "Laboratory Report Narrative" (date-filterable) | Present; coverage of results from 20+ interfaced labs unclear |
| Imaging / diagnostic reports | ⚠️ Partial | No dedicated imaging section in CCD; may appear under lab/DX tests | Product has radiology connectivity; representation in CCD unclear |
| Procedures | ✅ Covered | CCD "History of Procedures" + "Procedure Notes" (date-filterable) | Standard CCD procedures |
| Clinical notes / documents | ⚠️ Partial | CCD "Progress Notes" + "Assessments" (date-filterable) | CCD includes progress notes but likely not full SOAP notes, specialty module notes (psychiatry, therapy, MAT), or attached documents. REST API has `soap_note` and `document` scopes. |
| Care plans / goals | ✅ Covered | CCD "Treatment Plan" + "Goals" + "Health Concerns" (date-filterable) | Standard CCD care plan sections |
| Orders / referrals | ✅ Covered | CCD "Document Reason for Referral" (date-filterable) | Referral reasons present; order details unclear |
| Insurance / coverage | ❌ Not covered | No insurance data in CCD | Product stores insurance data (REST API has `insurance`, `insurance_company`, `insurance_type` scopes); significant gap |
| Claims / billing | ❌ Not covered | No billing entities in CCD | Product has FQHC facility billing and fee-for-service billing; significant gap |
| Payments | ❌ Not covered | No payment data in CCD | Product stores payment records, patient ledgers, payor aging; significant gap |
| Consents / directives | ❌ Not covered | No consent/directive section in CCD | Unknown if product stores this data |
| Patient communications / portal messages | ❌ Not covered | No messaging data in CCD | Product has patient portal with secure messaging; REST API has `message` scope; gap |
| Specialty-specific: Behavioral health | ⚠️ Partial | CCD "Mental Status" + "Assessments" sections | Product has psychiatry, therapy, and MAT modules; CCD likely captures only summary, not full specialty documentation |
| Specialty-specific: Dental | ❌ Not covered | No dental data in CCD | REST API has `dental_issue` scope; MyCHN provides dental services; gap |
| Specialty-specific: Screening tools | ⚠️ Partial | May appear under CCD "Assessments" or "Functional Status" | Product has extensive SDOH, substance abuse, depression, fall risk, and other screenings; representation in CCD unclear |

**Summary**: Of 20 applicable domains, 7 are covered, 6 are partial, 6 are not covered, and 1 is N/A (consents — unclear if stored). The most significant gaps are **billing/claims/payments**, **insurance**, **dental records**, **patient portal messages**, and **detailed prescription records**.

## 6. Documentation Quality

**Clarity**: The documentation is well-organized across WordPress pages. The 11-step Swagger tutorial for CCD generation is practical and clear.

**Completeness**: Extremely thin. The EHI export page itself is just 3 short paragraphs. There is:
- **No data dictionary** — zero field-level definitions
- **No schema documentation** — no mapping between EHR fields and CCD elements
- **No sample data** — no example CCD documents
- **No value set documentation** — vendor relies entirely on C-CDA standard value sets
- **No vendor-specific customizations documented** — unclear if any data beyond standard CCD templates is included

**Developer usability**: A developer could follow the Swagger tutorial to generate a CCD but would have no vendor-specific information about what the CCD contains. They would need to generate a sample CCD, inspect it, and cross-reference against the 913-page C-CDA IG Volume 2. The documentation answers "how to get a CCD" but not "what's in the CCD."

**Machine-readable artifacts**: None. No JSON schemas, no sample data files, no structured data dictionary.

**Honest assessment**: The documentation is insufficient for a developer to build an import or to understand what data is and isn't in the export. A patient or their representative cannot determine from this documentation what data they would receive.

## 7. Overall Assessment

### Classification

**Standard-based projection.** The (b)(10) EHI export is a C-CDA CCD document generated via the FHIR `$docref` operation. This is the vendor's existing FHIR API capability (documented alongside their (g)(10) Bulk FHIR implementation) repackaged as the EHI export. The export produces a standard clinical summary, not the vendor's native data model.

### Key Findings

1. **The (b)(10) export is the FHIR `$docref` CCD operation** — the vendor has equated their EHI export with C-CDA CCD generation. This is a textbook case of "C-CDA repackaging" (failure mode #1). The CCD is a clinical summary format that by design covers only a subset of patient data. (Source: `ehi-export-page.html`, `ccd-operation-in-fhir.html`)

2. **The REST API scope list reveals the gap**: The OpenEMR native REST API exposes 23 data types including `dental_issue`, `insurance`, `insurance_company`, `insurance_type`, `transaction`, `soap_note`, `surgery`, `prescription`, `message`, and `document` — none of which are represented in the C-CDA export. (Source: `rest-api-page.html`)

3. **Billing, insurance, and dental data are completely absent** from the export despite being core capabilities of this FQHC-focused EHR. MyCHN operates dental services and FQHC facility billing; these are significant data domains with no export mechanism. (Source: `rest-api-page.html` scopes, product research)

4. **Vital signs export is limited to the latest recorded values only** — not the full history. This is noted explicitly in the FHIR API documentation. (Source: `fhir-api-page.html`)

5. **No vendor-specific documentation exists** — the two PDFs are standard HL7 C-CDA IG documents. There is no data dictionary, no field mapping, no sample data, and no documentation of any vendor customizations or extensions. (Source: PDF metadata shows HL7 authorship; `ehi-export-page.html` contains only 3 paragraphs of vendor content)

### Summary Stats

```
Classification:  Standard-based projection (C-CDA CCD via FHIR $docref)
Export format:   C-CDA XML
Model type:      Standard projection (CCD clinical summary)
Entities:        21 CCD sections (no native tables/entities)
Fields:          N/A (no field-level documentation)
Descriptions:    N/A
Sample data:     No
Bulk export:     No (single patient CCD generation; FHIR Bulk Export exists but for (g)(10))
Domains covered: 7 of 20 applicable domains fully covered; 6 partial
```

### Bottom Line

This is a minimal compliance effort. The vendor has pointed their (b)(10) certification at their existing FHIR `$docref` CCD generation capability, producing a standard clinical summary that covers perhaps 40-50% of the patient data the system stores. Billing, insurance, dental, prescriptions, patient messages, and attached documents — all stored in the underlying OpenEMR database — are completely absent from the export. A patient requesting "all their electronic health information" from this system would receive a clinical summary document, not their complete record.
