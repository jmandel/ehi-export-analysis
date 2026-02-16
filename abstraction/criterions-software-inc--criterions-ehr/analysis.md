# EHI Export Analysis: Criterions Software Inc

**Product**: Criterions EHR v4.0
**Analysis date**: 2026-02-16
**CHPL IDs**: 15.04.04.2705.Crit.04.00.1.191111 (CHPL ID 10171)

## 1. Product Context

Criterions EHR is a cloud-based, ONC-certified electronic health records system from Criterions Software Inc, a small company (~7–12 employees) headquartered in the New York area. The certified product, "Criterions EHR 4.0 Complete EHR Ambulatory," is part of a broader integrated suite called "The Criterions Medical Suite" (TCMS) that combines EHR, practice management/billing, patient portal, e-prescribing, scheduling, lab interfaces, and document management into a unified platform.

The product targets independent ambulatory practices across nearly 50 specialties, from family medicine and internal medicine to surgical subspecialties, behavioral health, ophthalmology, oncology, and more. Despite the small team, the product is broadly certified (a)(1)–(a)(5), (b)(1)–(b)(3), (b)(10), (e)(1), (c)(1)–(c)(3), (f)(1), (f)(5), (g)(10).

**Data domains the product stores** (relevant for assessing export completeness):
- **Clinical**: Encounter notes, problem lists, medication lists, allergy lists, immunizations, vital signs, lab results, procedures, clinical decision support alerts, implantable devices, social/family/past medical history
- **E-Prescribing**: Prescriptions (including EPCS), refill requests, drug interaction alerts, pharmacy info (Surescripts/NewCrop integration)
- **Billing/Financial**: Insurance info, eligibility verification, superbills, claims, denials, A/R, payment history, patient payment plans, revenue cycle data
- **Scheduling**: Appointments, recurring appointments, reminders
- **Patient Portal**: Intake forms, secure messages, document/ID uploads, online payments
- **Document Management**: Folders, annotations, digital signatures
- **Clinical Notes**: Progress notes, H&P, consult notes (specialty-customizable templates)
- **Public Health**: Immunization registry submissions, cancer case reports
- **Reporting**: CQM/MIPS data, practice analytics

## 2. Artifacts Reviewed

| Artifact | Description | Informative? |
|---|---|---|
| `Patient-EHI-Data-Export-Overview.pdf` (83 KB, 1 page) | Patient-facing single-page overview listing 22 C-CDA sections included in the EHI export. Primary (b)(10) documentation. | **Most informative** — defines the export content |
| `2022-CURES-DISCLOSURES.pdf` (140 KB, 1 page) | Single-page disclosure covering MFA and EHI. States exports use C-CDA/XML via Email/Print Chart; individual, group, or scheduled export; no charge. | Moderately informative — describes export mechanism |
| `MandatoryDisclosure2022.pdf` (795 KB, 9 pages) | Full mandatory disclosure table listing all certified capabilities, descriptions, and costs. | Moderately informative — confirms (b)(10) and (b)(6) entries |
| `cures-disclosures-page-screenshot.png` (464 KB) | Screenshot of the registered CHPL documentation URL showing three PDF links. | Least informative — confirms page layout only |

**No data dictionary, schema, sample data, or machine-readable artifact exists in the documentation.** The entire technical documentation for the EHI export is a single-page patient-facing PDF listing 22 C-CDA section names.

## 3. Export Mechanics

- **Format**: C-CDA (Consolidated Clinical Document Architecture) — XML-based clinical document standard
- **Mechanism**: "Email/Print of your Chart" plus C-CDA file download via the Criterions EHR UI
- **Single-patient vs bulk**: The 2022 CURES Disclosures document states exports can be performed "for individual patients, groups of patients, or automated scheduled export"
- **Access constraints**: No charge per the CURES Disclosures. No programming intervention required. The Mandatory Disclosure notes the capability "requires separate service from EMRDirect" (for Direct messaging transport)
- **Technical detail**: None provided. No API documentation, no export format specification beyond "C-CDA XML"

## 4. Export Content: What's In It

The export is described as a C-CDA document containing 22 clinical sections. **No data dictionary exists** — the documentation provides only section names with zero field-level detail: no field names, no data types, no descriptions, no value sets, no relationships, no sample data.

The 22 sections listed are standard C-CDA clinical sections. There are no vendor-specific extensions, custom sections, or non-clinical data categories mentioned.

### Vendor's own content organization

The vendor does not organize the export into categories. The documentation is a flat bullet list of 22 C-CDA section names. Categorization below is derived from standard C-CDA section types:

| Entity/Section | Fields | Described | Types | Category |
|---|---|---|---|---|
| ALLERGIES | 0 (undocumented) | N/A | N/A | Clinical |
| ASSESSMENT | 0 | N/A | N/A | Clinical |
| CONSULT NOTE | 0 | N/A | N/A | Clinical Notes |
| DIAGNOSTIC IMAGING STUDY | 0 | N/A | N/A | Diagnostics |
| ENCOUNTERS | 0 | N/A | N/A | Clinical |
| FUNCTIONAL STATUS | 0 | N/A | N/A | Clinical |
| GOALS | 0 | N/A | N/A | Clinical |
| HEALTH CONCERN | 0 | N/A | N/A | Clinical |
| HISTORY AND PHYSICAL | 0 | N/A | N/A | Clinical Notes |
| IMMUNIZATIONS | 0 | N/A | N/A | Clinical |
| LABORATORY REPORT NARRATIVE | 0 | N/A | N/A | Diagnostics |
| MEDICAL EQUIPMENT | 0 | N/A | N/A | Clinical |
| MEDICATIONS | 0 | N/A | N/A | Clinical |
| MENTAL STATUS | 0 | N/A | N/A | Clinical |
| PLAN OF CARE | 0 | N/A | N/A | Clinical |
| PROBLEM LIST | 0 | N/A | N/A | Clinical |
| PROCEDURES | 0 | N/A | N/A | Clinical |
| PROGRESS NOTE | 0 | N/A | N/A | Clinical Notes |
| REASON FOR REFERRAL | 0 | N/A | N/A | Clinical |
| RESULTS | 0 | N/A | N/A | Diagnostics |
| SOCIAL HISTORY | 0 | N/A | N/A | Clinical |
| VITAL SIGNS | 0 | N/A | N/A | Clinical |

**Total sections**: 22
**Total fields documented**: 0
**Data dictionary**: None

The full inventory is available at `analysis/entity-inventory-full.json`.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor's export covers exactly one category: **clinical data in C-CDA format**. All 22 listed sections are standard C-CDA clinical sections — allergies, medications, problems, encounters, vitals, labs, notes, procedures, immunizations, referrals, goals, assessments, social history, functional/mental status, medical equipment, and diagnostic imaging.

This is precisely the data covered by C-CDA transitions of care documents. There is no evidence of any data beyond the standard C-CDA clinical summary. The vendor's own language confirms this: the export uses "industry-standard patient information in XML format using CCDA architecture" (2022-CURES-DISCLOSURES.pdf).

The Mandatory Disclosure's (b)(6) Data export entry explicitly states the export creates "a set of export summaries for all patients in C-CDA format that represents the most current clinical information about each patient. It includes clinical data defined in the Common Clinical Data Set." The (b)(10) entry description is sparser: "Allow a practice to create individual and group exports of PHI without programming intervention." There is no indication (b)(10) differs from (b)(6) in content — both appear to use the same C-CDA export.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | C-CDA patient header (standard, not documented by vendor) | C-CDA includes basic demographics but depth is unknown; no field-level docs |
| Encounters / visits | ⚠️ Partial | "ENCOUNTERS" section listed | Section name only; no detail on encounter depth |
| Problems / conditions | ⚠️ Partial | "PROBLEM LIST" section listed | Section name only |
| Medications / prescriptions | ⚠️ Partial | "MEDICATIONS" section listed | Section name only; EPCS/Surescripts transaction data likely absent |
| Allergies | ⚠️ Partial | "ALLERGIES" section listed | Section name only |
| Immunizations | ⚠️ Partial | "IMMUNIZATIONS" section listed | Section name only |
| Vitals | ⚠️ Partial | "VITAL SIGNS" section listed | Section name only |
| Lab results | ⚠️ Partial | "RESULTS", "LABORATORY REPORT NARRATIVE" sections listed | Section names only |
| Imaging / diagnostic reports | ⚠️ Partial | "DIAGNOSTIC IMAGING STUDY" section listed | Section name only |
| Procedures | ⚠️ Partial | "PROCEDURES" section listed | Section name only |
| Clinical notes / documents | ⚠️ Partial | "PROGRESS NOTE", "HISTORY AND PHYSICAL", "CONSULT NOTE" listed | Only 3 note types; product likely stores more document types |
| Care plans / goals | ⚠️ Partial | "PLAN OF CARE", "GOALS", "ASSESSMENT" listed | Section names only |
| Orders / referrals | ⚠️ Partial | "REASON FOR REFERRAL" listed | Referral reason only; order detail/tracking likely absent |
| Insurance / coverage | ❌ Not covered | No insurance entities in export | Product has insurance verification, eligibility checking — **significant gap** |
| Claims / billing | ❌ Not covered | No billing entities in export | Product has full billing module (superbills, claims, denial tracking, A/R) — **significant gap** |
| Payments | ❌ Not covered | No payment entities in export | Product tracks payments, patient payment plans — **significant gap** |
| Consents / directives | ❌ Not covered | No consent entities | Product portal collects consent forms — gap |
| Patient communications / portal messages | ❌ Not covered | No messaging entities | Product has secure messaging via portal — gap |
| Specialty-specific data | ❌ Not covered | No specialty entities | Product supports ~50 specialties with custom templates — gap |

**Summary**: All clinical domains are marked "Partial" rather than "Covered" because the documentation only provides section names — there is no field-level detail to confirm depth within any domain. All non-clinical domains the product stores (billing, insurance, payments, portal data, specialty forms) are entirely absent from the export.

## 6. Documentation Quality

The documentation quality is **extremely poor**:

- **No data dictionary** at any level — no field names, types, descriptions, value sets, or relationships
- **No machine-readable artifacts** — no JSON schema, no XML schema, no sample C-CDA files
- **No sample data** provided
- **No technical specification** — no mapping documentation, no C-CDA template OIDs, no extension documentation
- **Patient-facing only** — the one-page overview is written for patients ("How to read your CCDA"), not for technical consumers
- **No import guidance** — a developer receiving this export would need to rely entirely on the generic C-CDA specification and hope Criterions follows it faithfully

A developer could not build an import from this documentation. They would receive a C-CDA XML file with no vendor-specific documentation about what data is populated, what coding systems are used, or how Criterions maps its internal data to C-CDA sections.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Minimal/stub/unclear**

The export covers only standard C-CDA clinical sections — the same data available through (b)(1) transitions of care and (g)(10) FHIR API. The product has substantial non-clinical data storage (billing module with claims/superbills/A/R/payment tracking, patient portal with messaging/forms, scheduling, document management) that is entirely absent from the export. Even within clinical domains, the lack of any field-level documentation makes it impossible to confirm depth. The 22 C-CDA sections are the standard USCDI-scope clinical summary, not a comprehensive EHI export.

**Axis 2 — Export approach: Repackaged existing export**

This is a textbook case of repackaging the existing C-CDA transitions-of-care export as (b)(10). The evidence is clear:

1. The export format is C-CDA — the same format used for (b)(1) and (b)(6) certified capabilities
2. The Mandatory Disclosure's (b)(6) entry explicitly states it creates "export summaries for all patients in C-CDA format" with "clinical data defined in the Common Clinical Data Set" — the (b)(10) entry appears to be the same export
3. The 2022 CURES Disclosures document describes the export as "industry-standard patient information in XML format using CCDA architecture"
4. The 22 sections listed are standard C-CDA sections, mapping directly to USCDI data classes
5. There is no vendor-specific data dictionary, no custom sections, no non-clinical data — nothing that would indicate a purpose-built (b)(10) effort
6. There is no coverage of billing, scheduling, portal, or any other non-clinical data the product stores

### Key Findings

1. **The (b)(10) export is identical to the (b)(1)/(b)(6) C-CDA clinical summary export.** The Mandatory Disclosure confirms both use C-CDA format for "clinical data defined in the Common Clinical Data Set." No additional data or format was built for (b)(10).

2. **The product's full billing/PM module is entirely excluded from the export.** Criterions has an integrated practice management suite with insurance verification, superbills, claims, denial tracking, A/R management, and payment processing — none of which appears in the C-CDA export.

3. **Zero field-level documentation exists.** The entire (b)(10) technical documentation is a single-page PDF listing 22 section names. No data dictionary, no schema, no sample data, no mapping specification.

4. **Patient portal data is excluded.** The product supports secure messaging, intake forms, consent forms, document uploads, and online payments through its portal — none included in the export.

5. **The documentation is patient-facing, not technical.** The overview PDF explains "How to read your CCDA" rather than providing the technical documentation needed to interpret or import the export data.

### Summary Stats

```
Coverage:        Minimal/stub/unclear
Approach:        Repackaged existing export
Export format:   C-CDA (XML)
Entities:        22 C-CDA sections (section names only, no field detail)
Fields:          N/A (no data dictionary)
Descriptions:    N/A
Sample data:     No
Bulk export:     Yes (group and scheduled export mentioned)
Domains covered: ~10 of 19 applicable domains (all partial, clinical only)
```

### Bottom Line

Criterions has repackaged their existing C-CDA clinical summary as their (b)(10) EHI export, providing no data dictionary and no coverage of the billing, portal, scheduling, or specialty data their integrated suite stores. A patient receiving this export would get a standard clinical summary — the same data available through any transitions-of-care exchange — but would be missing their billing records, portal messages, intake forms, and any specialty-specific clinical data beyond what C-CDA supports. The single biggest gap is the complete absence of the practice management/billing data that the product is built to manage.
