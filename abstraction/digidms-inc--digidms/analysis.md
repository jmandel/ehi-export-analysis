# EHI Export Analysis: DigiDMS, Inc.

**Product**: DigiDMS v25.0
**Analysis date**: 2026-02-16
**CHPL IDs**: 11549 (15.04.04.2709.Digi.25.05.1.241212)

## 1. Product Context

DigiDMS is an integrated ambulatory EHR + Practice Management + Billing system from a small New Jersey-based vendor (DigiDMS, Inc.). It serves small to medium outpatient practices — physician offices, dental offices, and PT clinics — with ~300+ medical offices reported as customers.

Key capabilities relevant to EHI scope:

- **Clinical EHR**: Charting, problem lists, medications, allergies, vitals, immunizations, lab results, procedures, clinical notes, encounters, e-prescribing, implantable device tracking, social/psychological/behavioral data, clinical decision support. Certified for CPOE ((a)(1)–(a)(3)).
- **Practice Management / Billing**: Appointment scheduling, insurance management, claim scrubbing, HCFA/CMS-1500 form generation, ICD-10 coding, batch eligibility checks, revenue cycle management, invoices, and payment records.
- **Patient Portal (myPersonalChart)**: Secure messaging, view clinical data, appointment management, medication refill requests, referral requests, CCD export/import.
- **Document Management**: Centralized repository, OCR, version control, digital signatures, metadata tagging, annotations.
- **Transitions of Care**: C-CDA generation, direct messaging ((b)(1)–(b)(3), (h)(1)).
- **Public Health Reporting**: Immunization registry, syndromic surveillance, cancer case reporting, electronic case reporting.

The product stores clinical, billing/financial, scheduling, communication, and document data. A complete EHI export should cover all of these domains.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|----------|-------------|-----------------|
| `downloads/B10_EHI_Export.pdf` | 7-page PDF (1.28 MB); sole EHI export documentation. Contains overview, two UI screenshots, and a data dictionary listing 21 C-CDA sections with 61 total element names. Created 2025-11-18 by Hemant J. Patel. Title page says v22.0 but web page references v25.0. | **Primary** — the only substantive artifact |
| `downloads/EHIexport-template.html` | AngularJS template (1,977 bytes) for the EHI export page. Describes C-CDA export for single/bulk patients, links to the PDF. References "DigiDMS 25.0". | Minor — confirms format and scope |
| `downloads/ehi-export-page-screenshot.png` | Browser screenshot showing blank page (AngularJS SPA failed to render). | Uninformative |

**Most informative**: The PDF is the only artifact with substantive content. No sample data, no machine-readable schema, no additional documentation was found.

## 3. Export Mechanics

- **Format**: C-CDA (HL7 CDA R2 IG: C-CDA Templates for Clinical Notes R2.1 Companion Guide), per § 170.205(a)(4)
- **Mechanism**: User-initiated via EHR UI. No developer/technical assistance required.
- **Single patient**: From the patient chart, a "Clinical Document Section" dialog allows selecting which C-CDA sections to include, with a date range filter. Sections include Encounters, Problems, Allergies, Medications, Social History, Results, Assessment and Plan, Immunizations, Procedures, Goals, Implanted Devices, Health Concerns, Functional Status, and Reason for Referral.
- **Bulk export**: From the "Patient Screening" module, users run a population query (e.g., "Diabetic patients"), view results, and export via a dropdown with CCDA option. Screenshot shows 11 records for a sample query.
- **Access constraints**: Users must request permission grants for export functionality ("DigiDMS user can raise request for grants to specific export functionality").
- **Fees**: Not mentioned in the documentation. No cost/limitation information found on the mandatory disclosures page.

## 4. Export Content: What's In It

The export produces standard C-CDA documents. The "data dictionary" in the PDF is a two-column table listing 21 C-CDA sections and their element names — a total of 61 elements across all sections.

**Documentation depth is extremely shallow:**
- Only element names are listed (e.g., "Substance", "Reaction", "Severity", "Status" under Allergies)
- No data types specified for any element
- No value sets or code systems documented (e.g., what coding system for diagnoses? What severity scale for allergies?)
- No cardinality or nullability information
- No descriptions beyond the element name itself
- No relationships or foreign keys
- No sample data or examples
- No machine-readable schema (the C-CDA standard is cited by reference only)

### Vendor's own content organization

All content is organized as C-CDA sections. The vendor provides no categories beyond the section names themselves.

| Entity/Section | Fields | Described | Types | Category |
|---|---|---|---|---|
| Patient | 8 | 0 | no | C-CDA Section |
| Provider | 1 | 0 | no | C-CDA Section |
| Author | 1 | 0 | no | C-CDA Section |
| Practice | 1 | 0 | no | C-CDA Section |
| Reason for Referral | 0 | 0 | no | C-CDA Section |
| Allergies | 4 | 0 | no | C-CDA Section |
| Encounters | 4 | 0 | no | C-CDA Section |
| Immunization | 3 | 0 | no | C-CDA Section |
| Medication | 4 | 0 | no | C-CDA Section |
| Health Concern | 3 | 0 | no | C-CDA Section |
| Interventions | 3 | 0 | no | C-CDA Section |
| Goals | 3 | 0 | no | C-CDA Section |
| Medical Equipments | 3 | 0 | no | C-CDA Section |
| Problems | 3 | 0 | no | C-CDA Section |
| Procedures | 2 | 0 | no | C-CDA Section |
| Care Plan | 2 | 0 | no | C-CDA Section |
| Assessment | 3 | 0 | no | C-CDA Section |
| Results | 5 | 0 | no | C-CDA Section |
| Social History | 3 | 0 | no | C-CDA Section |
| Vital Signs | 3 | 0 | no | C-CDA Section |
| Functional Status | 2 | 0 | no | C-CDA Section |

**Totals**: 21 sections, 61 elements, 0 descriptions, 0 types.

Full inventory available at `analysis/entity-inventory-full.json`; summary at `analysis/entity-inventory-summary.json`.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The export covers exactly the standard C-CDA clinical summary sections — the same sections used for transitions of care ((b)(1)) and patient portal CCD export. There is no evidence of any content beyond what a standard C-CDA document carries:

- **Demographics**: Patient name, DOB, sex, race, ethnicity, language, contact info, ID (8 elements)
- **Clinical core**: Problems, medications, allergies, vitals, immunizations, procedures, results, encounters, social history, care plan, goals, functional status, health concerns, assessments, medical equipments (implantable devices), reason for referral, interventions
- **Provider/author/practice metadata**: Contact information only

No section has more than 8 elements. The richest section is "Patient" (8 elements); most have 2–4 elements. "Results" has 5 elements (Result, Date, Interpretation, Reference Range, Remarks). "Reason for Referral" has 0 elements listed — just the section name.

This is the standard C-CDA clinical summary. There is nothing in the export that goes beyond what would be produced for a (b)(1) transitions of care document.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | Patient section: 8 elements (Name, DOB, Sex, Race, Ethnicity, Language, Contact Info, Patient Id) | Basic demographics present but thin — no address breakdown, no emergency contacts, no preferred pharmacy |
| Encounters / visits | ⚠️ Partial | Encounters section: 4 elements (Encounter, Location, Date, Diagnosis) | Minimal — no visit type, no provider, no duration, no disposition |
| Problems / conditions | ⚠️ Partial | Problems section: 3 elements (Condition, Effective Date, Status) | Basic problem list only — no onset context, no severity, no linked orders |
| Medications / prescriptions | ⚠️ Partial | Medication section: 4 elements (Medication, Direction, Quantity, Date) | No pharmacy, no fill status, no prescriber, no prior authorization details |
| Allergies | ⚠️ Partial | Allergies section: 4 elements (Substance, Reaction, Severity, Status) | Adequate for allergy list; limited depth |
| Immunizations | ⚠️ Partial | Immunization section: 3 elements (Vaccine, Date, Status) | No lot number, no site, no administering provider |
| Vitals | ⚠️ Partial | Vital Signs section: 3 elements (Vital Sign, Date, Value) | Minimal — no units, no method, no source |
| Lab results | ⚠️ Partial | Results section: 5 elements (Result, Date, Interpretation, Reference Range, Remarks) | Best-documented section but still no units, no specimen type, no ordering provider |
| Imaging / diagnostic reports | ❌ Not covered | No imaging-specific section in the data dictionary | DigiDMS is certified for clinical data and likely stores diagnostic imaging results; gap |
| Procedures | ⚠️ Partial | Procedures section: 2 elements (Procedure, Date) | Very thin — no provider, no site, no outcome |
| Clinical notes / documents | ❌ Not covered | No clinical notes section; Assessment has "Comments" field only | DigiDMS stores clinical notes/encounter documentation; significant gap |
| Care plans / goals | ⚠️ Partial | Care Plan (2 elements), Goals (3 elements), Interventions (3 elements) | Present but thin |
| Orders / referrals | ⚠️ Partial | Reason for Referral section (0 elements listed) | DigiDMS is CPOE-certified ((a)(1)–(a)(3)); order data not represented; significant gap |
| Insurance / coverage | ❌ Not covered | No insurance section in export | DigiDMS stores insurance/enrollment data (patient portal shows it); significant gap |
| Claims / billing | ❌ Not covered | No billing entities in export | DigiDMS has integrated billing (claim scrubbing, HCFA forms, ICD-10, eligibility, invoices, payments); **major gap** |
| Payments | ❌ Not covered | No payment data in export | Product tracks payment records; gap |
| Consents / directives | ❌ Not covered | No consent section | Unknown if product stores these; possible gap |
| Patient communications | ❌ Not covered | No messaging/communication section | DigiDMS patient portal has secure messaging; gap |
| Specialty-specific data | N/A | Product is general ambulatory, not specialty-specific | N/A |

**Summary**: Of 17 applicable domains, 7 are not covered at all (including billing, insurance, clinical notes, and patient communications), and all 10 "covered" domains are partial — each has only 2–8 elements with no types, no value sets, and no descriptions.

## 6. Documentation Quality

The documentation is **very poor** from a developer perspective:

- **Completeness**: A 7-page PDF with a cover page, 2 pages of screenshots, and 3 pages of a section/element listing. No machine-readable artifacts.
- **Usability**: A developer could not build an import from this documentation alone. The C-CDA standard is cited by reference only — all structural detail (XML schema, code systems, value sets, cardinality) must be found independently in the HL7 C-CDA R2.1 specification.
- **Element descriptions**: Zero of 61 elements have descriptions. Element names are self-evident (e.g., "Date", "Status") but ambiguous without context.
- **Types**: No data types specified for any element.
- **Value sets**: No coded values or value sets documented. What codes are used for allergy severity? What coding system for diagnoses? Not specified.
- **Sample data**: None provided.
- **Machine-readable schema**: None provided.
- **Version discrepancy**: The PDF title page says "DigiDMS and 22.0" but the current product is v25.0 and the web template references 25.0. The PDF was created 2025-11-18, suggesting the version number on the title page was not updated.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Minimal/stub**

The export covers only the standard C-CDA clinical summary sections — approximately the USCDI floor. DigiDMS is an integrated EHR + Practice Management + Billing system, meaning it stores substantial data in domains that are entirely absent from this export: billing records (claims, HCFA forms, payments, eligibility), insurance information, clinical notes, patient portal communications, document management content, and CPOE order data. The C-CDA export addresses perhaps 20-30% of the data domains the product stores, and even within covered domains, the element depth is very shallow (2-8 elements per section, no types or descriptions).

**Axis 2 — Export approach: Repackaged existing export**

This is a textbook case of repackaging an existing transitions-of-care C-CDA export as (b)(10). The telltale signs are:
1. The format is C-CDA — the same standard used for (b)(1) transitions of care, which DigiDMS is also certified for
2. The sections listed in the data dictionary are exactly the standard C-CDA sections — no vendor-specific extensions or additions
3. The patient portal (myPersonalChart) already offers CCD export — the (b)(10) export appears identical in scope
4. No product-specific data dictionary exists — just a listing of standard C-CDA section/element names
5. No billing, financial, administrative, or operational data is included — only clinical summary data
6. The PDF overview describes generating a "Clinical Care Document" — this is literally what C-CDA was designed for, and it's the (b)(1) function

### Key Findings

1. **Repackaged C-CDA transitions-of-care export**: The (b)(10) export is indistinguishable from a standard C-CDA clinical summary. The 21 sections and 61 elements listed map directly to standard C-CDA sections with no vendor-specific extensions. (`B10_EHI_Export.pdf`, pages 5–7)

2. **Major billing/financial data gap**: DigiDMS has integrated billing capabilities (claim scrubbing, HCFA/CMS-1500 forms, ICD-10 coding, eligibility checks, invoices, payment records), but zero billing data appears in the export. Billing records are squarely within the HIPAA designated record set. (`product-research.md`, lines 59–68 vs. `B10_EHI_Export.pdf` data dictionary)

3. **Clinical notes not exported**: Despite DigiDMS storing clinical notes and encounter documentation, no clinical notes section appears in the C-CDA export. The Assessment section has a "Comments" field, but this is not equivalent to full clinical notes. (`product-research.md`, line 41 vs. data dictionary)

4. **Documentation is a stub**: 61 elements with zero descriptions, zero types, zero value sets. A developer would need to consult the full C-CDA R2.1 specification independently; the vendor's documentation adds no product-specific information beyond the section/element names. (`analysis/entity-inventory-summary.json`)

5. **Version inconsistency**: PDF title page says v22.0; web template says v25.0. Created 2025-11-18 for a 2024-12-12 certification. This suggests the documentation was created after certification and the version number was not updated. (`B10_EHI_Export.pdf` page 1, `EHIexport-template.html` line 24)

### Summary Stats

```
Coverage:        Minimal/stub
Approach:        Repackaged existing export
Export format:   C-CDA (HL7 CDA R2 IG: C-CDA Templates for Clinical Notes R2.1)
Entities:        21 C-CDA sections
Fields:          61 elements
Descriptions:    0% (0 of 61 elements have descriptions)
Sample data:     No
Bulk export:     Yes (population-level via Patient Screening module)
Domains covered: 10 of 17 applicable (all partial; 7 not covered at all)
```

### Bottom Line

DigiDMS's (b)(10) EHI export is a standard C-CDA clinical summary repackaged as an EHI export — the same output produced for transitions of care. For an integrated EHR + billing system, the complete absence of billing/financial data, clinical notes, insurance information, patient communications, and document management content represents a fundamental failure to export the designated record set. A patient receiving this export would get a clinical summary but not their billing records, insurance details, portal messages, or scanned documents.
