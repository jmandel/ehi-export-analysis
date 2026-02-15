# EHI Export Analysis: Criterions Software Inc

**Product**: Criterions EHR v4.0 (Complete EHR Ambulatory)
**Analysis date**: 2026-02-15
**CHPL IDs**: 10171 (15.04.04.2705.Crit.04.00.1.191111)

## 1. Product Context

Criterions Software Inc is a small vendor (~7–12 employees) based in Garden City, NY that develops an integrated cloud-based EHR and practice management suite called "The Criterions Medical Suite" (TCMS). The product targets independent ambulatory practices across nearly 50 specialties, from family medicine to surgical subspecialties, behavioral health, dentistry, ophthalmology, and more.

The product is an **integrated EHR + Practice Management system** with the following modules relevant to EHI scope:

- **EHR**: Customizable charting, specialty templates, vitals, problem lists, medication lists, allergy lists, clinical decision support, implantable device tracking, social/behavioral data
- **E-Prescribing**: Integrated EPCS via Surescripts/NewCrop, drug interaction monitoring, refill tracking
- **Practice Management / Billing**: Insurance verification, superbills, claims submission, denial tracking, A/R management, payment posting, patient payment plans, revenue cycle management
- **Patient Portal**: Intake forms, secure messaging, prescription refill requests, bill viewing/payment, document upload
- **Lab Interfaces**: Electronic lab ordering, automatic result filing, LOINC-coded results
- **Document Management**: Folder organization, annotations, digital signatures
- **Scheduling**: Appointment calendars, recurring appointments, automated reminders

This is a full-featured ambulatory EHR+PM suite. A complete (b)(10) export should cover clinical documentation, billing/financial records, prescription data, portal communications, and lab data — not just a clinical summary.

## 2. Artifacts Reviewed

| Artifact | Source | Description | Informativeness |
|---|---|---|---|
| `Patient-EHI-Data-Export-Overview.pdf` | [criterions.com](https://criterions.com/wp-content/uploads/2024/05/Patient-EHI-Data-Export-Overview.pdf) | 1-page patient-facing overview listing 22 C-CDA sections; created Nov 27, 2024; 82 KB | **Primary (b)(10) document** — most informative but very thin |
| `2022-CURES-DISCLOSURES.pdf` | [criterions.com](https://criterions.com/wp-content/uploads/2022/08/2022-CURES-DISCLOSURES.pdf) | 1-page cures disclosure covering MFA and EHI; created May 10, 2024; 140 KB | Low — one paragraph on EHI export |
| `MandatoryDisclosure2022.pdf` | [criterions.com](https://criterions.com/wp-content/uploads/2022/12/MandatoryDisclosure2022.pdf) | 9-page mandatory disclosure table (landscape); created Dec 11, 2022; 795 KB | Low for (b)(10) — one-line description, but useful for understanding product capabilities |
| `cures-disclosures-page-screenshot.png` | Screenshot of disclosure page | Shows the "Certifications & Documentation" page with three button-links | Confirms page structure; no additional content |

The disclosure page at `https://criterions.com/cures-disclosures-2022/` was verified as accessible on 2026-02-15. It contains exactly three button-links to the three PDFs above, plus Surescripts, Drummond ONC, and Claredi 5010 certification logos. No additional documentation, data dictionaries, schemas, or sample data exist beyond these three PDFs.

**No data dictionary, no schema, no sample data, no field-level documentation of any kind was provided.**

## 3. Export Mechanics

- **Format**: C-CDA (Consolidated Clinical Document Architecture) — XML-based clinical document standard
- **Mechanism**: "Email/Print of your Chart" functionality within the Criterions EHR, plus an option to download the CCDA file directly
- **Single-patient vs bulk**: The 2022 CURES Disclosures PDF states exports can be performed "for individual patients, groups of patients, or automated scheduled export"
- **Access constraints**: No charge for exports; no programming intervention required. The Mandatory Disclosure notes that the (b)(10) capability "requires separate service from EMRDirect" (a Direct messaging service), though it is unclear whether this is required only for electronic transmission vs. download
- **Cost**: Included with Criterions EHR subscription

## 4. Export Content: What's In It

The export is a **C-CDA clinical document** containing 22 sections. There is no data dictionary, no field-level documentation, no schema documentation, and no sample data. The only content specification is the list of 22 C-CDA section names from the Patient EHI Data Export Overview PDF.

### Vendor's own content organization

The vendor does not organize content into categories. They provide a flat list of 22 C-CDA section names. There are no entities, tables, or fields documented — only section headings:

| C-CDA Section | Fields | Described | Types | Category |
|---|---|---|---|---|
| Allergies | N/A | N/A | N/A | C-CDA section |
| Assessment | N/A | N/A | N/A | C-CDA section |
| Consult Note | N/A | N/A | N/A | C-CDA section |
| Diagnostic Imaging Study | N/A | N/A | N/A | C-CDA section |
| Encounters | N/A | N/A | N/A | C-CDA section |
| Functional Status | N/A | N/A | N/A | C-CDA section |
| Goals | N/A | N/A | N/A | C-CDA section |
| Health Concern | N/A | N/A | N/A | C-CDA section |
| History and Physical | N/A | N/A | N/A | C-CDA section |
| Immunizations | N/A | N/A | N/A | C-CDA section |
| Laboratory Report Narrative | N/A | N/A | N/A | C-CDA section |
| Medical Equipment | N/A | N/A | N/A | C-CDA section |
| Medications | N/A | N/A | N/A | C-CDA section |
| Mental Status | N/A | N/A | N/A | C-CDA section |
| Plan of Care | N/A | N/A | N/A | C-CDA section |
| Problem List | N/A | N/A | N/A | C-CDA section |
| Procedures | N/A | N/A | N/A | C-CDA section |
| Progress Note | N/A | N/A | N/A | C-CDA section |
| Reason for Referral | N/A | N/A | N/A | C-CDA section |
| Results | N/A | N/A | N/A | C-CDA section |
| Social History | N/A | N/A | N/A | C-CDA section |
| Vital Signs | N/A | N/A | N/A | C-CDA section |

No field counts, types, descriptions, relationships, or value sets are documented for any section. The vendor's documentation instructs patients: "If any of the fields are blank that is okay and not an error."

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor provides a single flat list of 22 C-CDA section names. These map to standard clinical summary categories — the same content that would appear in a transitions-of-care C-CDA document under §170.315(b)(1). The sections cover core clinical data: problems, medications, allergies, immunizations, vitals, labs, procedures, encounters, clinical notes, goals, and care plans.

There is no mention of any data beyond what C-CDA natively supports. The mandatory disclosure's (b)(6) Data Export description explicitly confirms this is the same C-CDA functionality: "create a set of export summaries for all patients in C-CDA format that represents the most current clinical information about each patient. It includes clinical data defined in the Common Clinical Data Set."

The (b)(10) entry in the mandatory disclosure is strikingly vague: "Allow a practice to create individual and group exports of PHI without programming intervention" — with no mention of format, content scope, or what "PHI" specifically includes. This one-sentence description is the totality of the (b)(10) specification.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | Not listed as a C-CDA section, but C-CDA documents include a patient header with basic demographics | C-CDA header contains limited demographics (name, DOB, sex, address); the product stores much richer demographic data per §170.315(a)(5) certification |
| Encounters / visits | ⚠️ Partial | "Encounters" C-CDA section | C-CDA Encounters section provides encounter summaries but likely omits scheduling details, visit metadata |
| Problems / conditions / diagnoses | ✅ Covered | "Problem List" C-CDA section | Standard C-CDA coverage |
| Medications / prescriptions | ⚠️ Partial | "Medications" C-CDA section | C-CDA Medications covers active/historical meds, but product has deep e-prescribing integration (Surescripts/NewCrop EPCS) with fulfillment tracking, refill requests, controlled substance audit trails — none of this is in C-CDA |
| Allergies | ✅ Covered | "Allergies" C-CDA section | Standard C-CDA coverage |
| Immunizations | ✅ Covered | "Immunizations" C-CDA section | Standard C-CDA coverage |
| Vitals | ✅ Covered | "Vital Signs" C-CDA section | Standard C-CDA coverage |
| Lab results | ✅ Covered | "Results" and "Laboratory Report Narrative" C-CDA sections | Standard C-CDA coverage |
| Imaging / diagnostic reports | ⚠️ Partial | "Diagnostic Imaging Study" C-CDA section | Section present but unclear what depth — C-CDA supports narrative reports but not images themselves |
| Procedures | ✅ Covered | "Procedures" C-CDA section | Standard C-CDA coverage |
| Clinical notes / documents | ⚠️ Partial | "Progress Note," "History and Physical," "Consult Note," "Assessment" C-CDA sections | C-CDA note sections are present but the product has a full document management module (folders, annotations, digital signatures) that is not represented |
| Care plans / goals | ✅ Covered | "Plan of Care," "Goals," "Health Concern" C-CDA sections | Standard C-CDA coverage |
| Orders / referrals | ⚠️ Partial | "Reason for Referral" C-CDA section | Section covers referral reason but not the full referral management workflow data |
| Insurance / coverage | ❌ Not covered | No insurance/coverage entities in export | Product has insurance verification, eligibility checking — **significant gap** |
| Claims / billing | ❌ Not covered | No billing entities in export | Product has full PM module: superbills, claims, denial tracking, A/R — **major gap** |
| Payments | ❌ Not covered | No payment entities in export | Product tracks payments, patient payment plans, online payments — **significant gap** |
| Consents / directives | ❌ Not covered | No consent entities in export | Product captures consent forms via patient portal intake — gap |
| Patient communications / portal messages | ❌ Not covered | No messaging entities in export | Product has secure messaging, intake forms, document upload — **significant gap** |
| Specialty-specific data | ❌ Not covered | No specialty-specific entities in export | Product supports ~50 specialties with customizable templates; C-CDA has no mechanism for specialty-specific structured data — **significant gap** |

**Summary**: 7 of 18 applicable domains have standard C-CDA coverage. 5 domains have partial coverage (C-CDA provides some data but misses product-specific depth). 6 domains with data stored by the product are entirely absent from the export.

## 6. Documentation Quality

The documentation quality is **minimal**:

- **No data dictionary**: There is no field-level documentation whatsoever. Not a single field name, data type, or description is provided beyond the 22 C-CDA section names.
- **No schema**: No XML schema, no mapping documentation, no constraints or extensions documented.
- **No sample data**: No example export files are provided.
- **No relationships**: No documentation of how data relates across sections.
- **No value sets**: No code systems, terminologies, or allowed values documented (the mandatory disclosure mentions ICD-9/10, SNOMED, RxNorm in other contexts but not in relation to the export).
- **Patient-facing, not technical**: The EHI Export Overview PDF is written for patients ("How to read your CCDA") rather than for developers or data recipients. It explains what a CCDA file is, not what specific data the export contains.
- **No technical mechanism documentation**: "Email/Print of your Chart" is the only description of how to obtain the export. The "automated scheduled export" mentioned in the CURES disclosure has no documentation.

A developer could not build an import from this documentation alone. They would need to rely entirely on the C-CDA specification and hope Criterions follows it without vendor-specific quirks. Even then, they would have no way to know what fields are populated, what code systems are used, or what data is actually included vs. left blank.

## 7. Overall Assessment

### Classification

**Standard-based projection** — The export is a C-CDA clinical summary being presented as the (b)(10) "all EHI" export. It covers the same clinical data as the vendor's transitions-of-care (b)(1) and patient access (e)(1) capabilities. The extensive billing, practice management, patient portal, document management, and specialty-specific data stored by the product is entirely absent.

### Key Findings

1. **The (b)(10) export is a repackaged C-CDA clinical summary.** The mandatory disclosure's (b)(6) Data Export and (b)(10) EHI Export entries describe functionally identical C-CDA exports. The 22 C-CDA sections listed match standard clinical summary content — this is the transitions-of-care document relabeled as "all EHI." (Sources: `Patient-EHI-Data-Export-Overview.pdf`, `MandatoryDisclosure2022.pdf`)

2. **The entire practice management/billing module is excluded.** The product has a comprehensive billing suite (superbills, claims, denial tracking, A/R, payment posting, patient payment plans) — none of which appears in the export. Billing data is core EHI under the designated record set definition. (Source: `product-research.md` vs. `Patient-EHI-Data-Export-Overview.pdf`)

3. **Documentation is essentially nonexistent.** The total (b)(10) documentation is a 1-page patient-facing PDF listing 22 section names, plus a single sentence in the mandatory disclosure. No data dictionary, no schema, no sample data, no field-level detail of any kind. (Sources: all three PDFs)

4. **Patient portal and secure messaging data is excluded.** The product captures patient intake forms, secure messages, uploaded documents, and online payment records — none appear in the C-CDA export. (Source: `product-research.md` vs. `Patient-EHI-Data-Export-Overview.pdf`)

5. **Specialty-specific data is excluded.** The product markets customizable templates for ~50 specialties — structured specialty data cannot be represented in standard C-CDA and is not documented as part of the export. (Source: `product-research.md` vs. `Patient-EHI-Data-Export-Overview.pdf`)

### Summary Stats

```
Classification:  Standard-based projection
Export format:   C-CDA (XML)
Model type:      Standard projection (C-CDA clinical summary)
Entities:        22 C-CDA sections (no native entities/tables)
Fields:          N/A (no field-level documentation)
Descriptions:    N/A (no field-level documentation)
Sample data:     No
Bulk export:     Yes (individual, group, and scheduled export per CURES disclosure)
Domains covered: 7 of 18 applicable domains (with 5 additional partial)
```

### Bottom Line

The Criterions EHR (b)(10) export is a C-CDA clinical summary repackaged as an "all EHI" export — a textbook example of the most common compliance shortcut. A patient or provider would receive a standard clinical summary covering core clinical data (problems, meds, allergies, labs, vitals, notes) but would be missing all billing records, insurance data, patient portal communications, specialty-specific assessments, and document management content. The single biggest gap is the complete absence of the practice management/billing data, which is a core module of this integrated EHR+PM product and constitutes designated record set data under HIPAA.
