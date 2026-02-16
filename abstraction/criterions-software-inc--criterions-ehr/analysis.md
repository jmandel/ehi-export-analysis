# EHI Export Analysis: Criterions Software Inc

**Product**: Criterions EHR (v4.0 Complete EHR Ambulatory)
**Analysis date**: 2026-02-16
**CHPL IDs**: 10171 (15.04.04.2705.Crit.04.00.1.191111)

## 1. Product Context

Criterions Software Inc is a small vendor (7–12 employees) based in Garden City, NY, offering an integrated cloud-based EHR and practice management suite called "The Criterions Medical Suite" (TCMS). The product targets independent ambulatory practices across nearly 50 specialties, from family medicine to surgical subspecialties, behavioral health, dentistry, ophthalmology, and more.

The product is a full-stack clinical + practice management platform. Key modules relevant to EHI export scope:

- **EHR/Clinical**: Customizable charting, encounter documentation, problem lists, medication lists, allergy lists, vital signs, immunizations, clinical decision support, implantable device tracking, social/psychological/behavioral data capture
- **E-Prescribing**: Integrated via Surescripts/NewCrop, including controlled substances (EPCS), drug interaction checking, refill tracking
- **Practice Management / Billing**: Insurance verification, superbill generation, claims submission, denial tracking, A/R management, payment posting, patient payment plans
- **Scheduling**: Appointment calendars, reminders, recurring appointments
- **Patient Portal**: Intake forms, secure messaging, prescription refill requests, online payments, document upload
- **Lab Interfaces**: Electronic lab ordering, LOINC-coded results
- **Document Management**: Folder organization, annotations, digital signatures
- **Reporting**: CQM/MIPS reporting, financial analytics, practice performance dashboards
- **Public Health Reporting**: Immunization registry and cancer case reporting

This baseline establishes that a complete EHI export should cover clinical data, billing/financial records, prescriptions, patient-submitted portal data, and specialty-specific clinical documentation — all of which are part of the designated record set.

## 2. Artifacts Reviewed

| Artifact | Type | Size | Description | Informativeness |
|---|---|---|---|---|
| `Patient-EHI-Data-Export-Overview.pdf` | PDF, 1 page | 82,693 bytes | Patient-facing overview listing 22 C-CDA sections included in the EHI export. Created 2024-11-27 by "cpicklesimer." | **Primary EHI doc** — lists section names only, no field-level detail |
| `2022-CURES-DISCLOSURES.pdf` | PDF, 1 page | 140,420 bytes | Cures Act disclosure covering MFA and EHI. Created 2024-05-10 by "cpicklesimer." States export uses C-CDA/XML via Email/Print Chart. | Confirms format and mechanism; no additional detail |
| `MandatoryDisclosure2022.pdf` | PDF, 9 pages (landscape) | 794,750 bytes | Mandatory disclosure table listing 48 certified capabilities with descriptions and costs. Created 2022-12-11 by "mgree." | Provides (b)(6) and (b)(10) descriptions; confirms C-CDA approach |
| `cures-disclosures-page-screenshot.png` | PNG | 463,647 bytes | Screenshot of the CHPL landing page at criterions.com/cures-disclosures-2022/ | Confirms page layout: three button-links to the PDFs |

**Most informative**: `Patient-EHI-Data-Export-Overview.pdf` — the only document that describes what's in the export.
**Least informative**: The screenshot, which merely confirms the landing page structure.

No data dictionary, schema, sample data, or field-level documentation was provided in any artifact.

## 3. Export Mechanics

- **Format**: C-CDA (Consolidated Clinical Document Architecture) — XML-based clinical document standard
- **Mechanism**: "Email/Print of your Chart" functionality within the Criterions EHR, plus a CCDA file download option
- **Single-patient**: Yes — individual patient export supported
- **Bulk export**: The 2022 Cures Disclosure states exports can be performed "for individual patients, groups of patients, or automated scheduled export"
- **Access constraints**: The Mandatory Disclosure states no charge for the export capability beyond the base EHR subscription. No programming intervention required.
- **Technical details**: None provided. No API documentation, no export format specification, no instructions beyond "Email/Print of your Chart"

The (b)(10) entry in the Mandatory Disclosure is notably terse: "Allow a practice to create individual and group exports of PHI without programming intervention." It does not describe what data is exported or in what format. The (b)(6) entry explicitly mentions C-CDA format and "Common Clinical Data Set."

## 4. Export Content: What's In It

The export is a C-CDA clinical document. The sole content documentation is a list of 22 C-CDA section names from the Patient EHI Data Export Overview PDF. There is:

- **No data dictionary** — zero entities/tables defined
- **No field-level documentation** — zero fields defined, zero types, zero descriptions
- **No relationships or foreign keys** documented
- **No value sets or code systems** specified (though the Mandatory Disclosure mentions ICD-9/10, SNOMED, RxNorm in passing)
- **No sample data** provided
- **No machine-readable schema** provided

### Vendor's own content organization

The vendor's only categorization is the flat list of 22 C-CDA sections. There is no grouping, no hierarchy, and no field-level breakdown. Presented as the vendor provides it:

| C-CDA Section Name | Fields Documented | Types | Descriptions |
|---|---|---|---|
| ALLERGIES | 0 | No | No |
| ASSESSMENT | 0 | No | No |
| CONSULT NOTE | 0 | No | No |
| DIAGNOSTIC IMAGING STUDY | 0 | No | No |
| ENCOUNTERS | 0 | No | No |
| FUNCTIONAL STATUS | 0 | No | No |
| GOALS | 0 | No | No |
| HEALTH CONCERN | 0 | No | No |
| HISTORY AND PHYSICAL | 0 | No | No |
| IMMUNIZATIONS | 0 | No | No |
| LABORATORY REPORT NARRATIVE | 0 | No | No |
| MEDICAL EQUIPMENT | 0 | No | No |
| MEDICATIONS | 0 | No | No |
| MENTAL STATUS | 0 | No | No |
| PLAN OF CARE | 0 | No | No |
| PROBLEM LIST | 0 | No | No |
| PROCEDURES | 0 | No | No |
| PROGRESS NOTE | 0 | No | No |
| REASON FOR REFERRAL | 0 | No | No |
| RESULTS | 0 | No | No |
| SOCIAL HISTORY | 0 | No | No |
| VITAL SIGNS | 0 | No | No |

**Total entities documented**: 0 (only section names listed, no entity/field definitions)
**Total fields documented**: 0

The full inventory is saved to `analysis/full-entity-inventory.json`.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor provides a single flat list of 22 C-CDA section names. These sections correspond to standard C-CDA clinical summary sections and cover clinical documentation only. There are no billing, scheduling, portal, or administrative sections.

The 22 sections map to these clinical domains:
- **Core clinical data**: Allergies, Medications, Problem List, Immunizations, Vital Signs, Results, Procedures — standard USCDI/CCDS data
- **Clinical documentation**: Assessment, Consult Note, History and Physical, Progress Note — narrative clinical notes
- **Care planning**: Goals, Health Concern, Plan of Care, Functional Status, Mental Status, Reason for Referral
- **Other clinical**: Diagnostic Imaging Study, Laboratory Report Narrative, Medical Equipment, Social History, Encounters

There is zero depth beyond section names. No fields, no types, no values — just the names of 22 C-CDA sections. This is essentially a table of contents for a C-CDA document, not a data export specification.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | No dedicated section; may be embedded in C-CDA header | Product captures demographics via PM integration (certified for (a)(5)). C-CDA header typically includes basic demographics but the vendor does not document this. |
| Encounters / visits | ⚠️ Partial | "ENCOUNTERS" section listed | Section name only — no field detail on what encounter data is included |
| Problems / conditions / diagnoses | ⚠️ Partial | "PROBLEM LIST" section listed | Section name only; product uses ICD-9/10, SNOMED per Mandatory Disclosure |
| Medications / prescriptions | ⚠️ Partial | "MEDICATIONS" section listed | Section name only. Product has full e-prescribing via Surescripts/NewCrop — controlled substance tracking, refill history, dispensing data — unlikely to be captured in a C-CDA Medications section |
| Allergies | ⚠️ Partial | "ALLERGIES" section listed | Section name only |
| Immunizations | ⚠️ Partial | "IMMUNIZATIONS" section listed | Section name only |
| Vitals | ⚠️ Partial | "VITAL SIGNS" section listed | Section name only |
| Lab results | ⚠️ Partial | "RESULTS" and "LABORATORY REPORT NARRATIVE" sections listed | Section names only; product has LOINC-coded lab interfaces |
| Imaging / diagnostic reports | ⚠️ Partial | "DIAGNOSTIC IMAGING STUDY" section listed | Section name only |
| Procedures | ⚠️ Partial | "PROCEDURES" section listed | Section name only |
| Clinical notes / documents | ⚠️ Partial | "PROGRESS NOTE", "HISTORY AND PHYSICAL", "CONSULT NOTE", "ASSESSMENT" sections listed | Section names suggest clinical notes are included, but no detail on completeness or specialty-specific templates |
| Care plans / goals | ⚠️ Partial | "PLAN OF CARE", "GOALS", "HEALTH CONCERN" sections listed | Section names only |
| Orders / referrals | ⚠️ Partial | "REASON FOR REFERRAL" section listed | Only referral reason — not referral management workflow data |
| Insurance / coverage | ❌ Not covered | No insurance/coverage entities in export | Product has insurance verification, eligibility checking — **significant gap** |
| Claims / billing | ❌ Not covered | No billing entities in export | Product has full billing module: superbills, claims, denial tracking, A/R — **significant gap** |
| Payments | ❌ Not covered | No payment entities in export | Product processes payments, payment plans, patient online payments — **significant gap** |
| Consents / directives | ❌ Not covered | No consent entities in export | Product collects consent forms via patient portal intake — gap |
| Patient communications / portal messages | ❌ Not covered | No portal/messaging entities in export | Product has secure messaging, refill requests, patient-submitted forms — **significant gap** |
| Specialty-specific data | ❌ Not covered | No specialty-specific entities in export | Product advertises support for ~50 specialties with customizable templates — gap for any specialty-specific clinical data beyond what C-CDA sections capture |

**Summary**: All clinical domains receive only "Partial" coverage because while C-CDA section names are listed, there is no documentation of what fields, depth, or completeness each section provides. All non-clinical domains (billing, insurance, payments, portal data) are completely absent from the export.

## 6. Documentation Quality

The documentation quality is **minimal**:

- **Completeness**: The entire EHI export documentation consists of one PDF page listing 22 section names and one paragraph in the Cures Disclosure. There is no data dictionary, no field definitions, no schema, no sample data.
- **Usability**: A developer could not build an import from this documentation alone. They would need to rely entirely on the C-CDA standard specification and assume Criterions follows it without extensions or deviations.
- **Machine-readability**: Zero machine-readable artifacts. No JSON schemas, no XML schemas, no sample C-CDA files, no CSV/TSV specifications.
- **Audience**: The documentation is patient-facing ("How to read your CCDA") rather than technical. It explains what a C-CDA file is to a layperson.
- **Versioning**: The EHI overview was created November 2024; the Cures Disclosure was created May 2024; the Mandatory Disclosure is from December 2022. No changelog or version history.

A developer receiving this export would have to: (1) parse an arbitrary C-CDA XML document with no vendor-specific documentation, (2) hope the 22 listed sections are populated according to standard, and (3) accept that billing, insurance, portal, and specialty data are simply absent.

## 7. Overall Assessment

### Classification

**Standard-based projection** — The export is a C-CDA clinical summary being presented as the (b)(10) EHI export. It is the same C-CDA format used for (b)(1) Transitions of Care and (b)(6) Data export, repackaged to satisfy the (b)(10) requirement. The Mandatory Disclosure's (b)(6) entry explicitly describes "export summaries for all patients in C-CDA format" covering the "Common Clinical Data Set" — the (b)(10) entry provides even less detail. This is a textbook case of C-CDA repackaging.

### Key Findings

1. **The EHI export is a C-CDA clinical summary, not a comprehensive data export.** The 22 C-CDA sections listed correspond to standard clinical summary sections — the same data available via (b)(1) Transitions of Care. The product's extensive billing, scheduling, patient portal, and specialty-specific data is entirely absent. (Source: `Patient-EHI-Data-Export-Overview.pdf`, `MandatoryDisclosure2022.pdf`)

2. **Zero field-level documentation exists.** The vendor provides no data dictionary, no field definitions, no types, no relationships, no value sets, and no sample data. The entire "data specification" is a bullet list of 22 section names on a single PDF page. (Source: all artifacts reviewed)

3. **Billing and practice management data is a major gap.** The product has a full billing module (superbills, claims, denial tracking, A/R, payments, insurance verification) — none of which can be represented in C-CDA format and none of which appears in the export documentation. (Source: `product-research.md`, `MandatoryDisclosure2022.pdf`)

4. **Patient portal data is absent.** The product captures patient intake forms, secure messages, refill requests, uploaded documents, and online payments through its portal — none of which is mentioned in the export. (Source: `product-research.md`)

5. **The (b)(10) entry in the Mandatory Disclosure is notably vague.** It says only "Allow a practice to create individual and group exports of PHI without programming intervention" — no mention of format, content, or scope. This contrasts with the (b)(6) entry which at least specifies C-CDA format and Common Clinical Data Set. (Source: `MandatoryDisclosure2022.pdf`)

### Summary Stats

```
Classification:  Standard-based projection (C-CDA repackaging)
Export format:   C-CDA (XML)
Model type:      Standard projection (not native database)
Entities:        0 (no data dictionary; 22 C-CDA section names listed)
Fields:          N/A (no field-level documentation)
Descriptions:    N/A
Sample data:     No
Bulk export:     Yes (individual, group, and scheduled per Cures Disclosure)
Domains covered: 0 of 17 fully covered; ~13 partially addressed via C-CDA section names; 5 not covered at all
```

### Bottom Line

Criterions' EHI export is a C-CDA clinical summary relabeled as a (b)(10) export, with no data dictionary, no field documentation, and no coverage of billing, insurance, patient portal, or specialty data. A patient or provider would receive a standard clinical summary XML file covering basic clinical data but missing the product's extensive practice management and billing records. The single biggest gap is the complete absence of the billing/PM data that constitutes roughly half of what this integrated EHR/PM suite stores about patients.
