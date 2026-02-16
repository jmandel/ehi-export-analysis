# EHI Export Analysis: Astronaut, LLC

**Product**: Astronaut (version 1709)
**Analysis date**: 2026-02-16
**CHPL IDs**: 10809

## 1. Product Context

Astronaut EHR is a cloud-based adaptation of VistA (Veterans Health Information Systems and Technology Architecture), the open-source EHR developed by the U.S. Department of Veterans Affairs. Built by a small Houston-based company led by psychiatrist Dr. Ignacio Valdes, it targets small ambulatory practices and community health centers. The product uses a customized VistA GUI client called Astro-CPRS.

**Data the product stores (relevant to export completeness):**
- **Core clinical**: Demographics, problems/diagnoses, medications, allergies, lab results, vitals, immunizations, procedures, clinical notes (via VistA's TIU templates — hundreds of "pre-built clinically proven templates"), encounters, goals, care plans, family health history, implantable devices, functional status
- **Orders/CPOE**: Medication orders, lab orders, radiology/imaging orders, consults
- **E-prescribing**: Integrated via Newcrop/Surescripts, including EPCS for controlled substances
- **Billing**: Ambiguous depth — the proprietary "Rocket Note" feature is described as enabling "very efficient follow-up notes and billing," and the company lists "billers" on staff. Whether this is full practice management or billing code capture during documentation is unclear.
- **Scheduling**: Enterprise scheduling for outpatient appointments; ADT (Admission/Discharge/Transfer) functions
- **Specialty**: The founder is a psychiatrist; the product has "Turbo Supervision" tools for mid-level provider oversight, suggesting some behavioral health workflow support

The product holds 30+ ONC certifications including (b)(10) for EHI export, (g)(10) for FHIR API, and criteria across CPOE, clinical data, care coordination, CQMs, and public health reporting. Being built on VistA, the underlying MUMPS/FileMan database potentially contains hundreds of files/tables.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `Astronaut-EHR-Export-Format-Documentation.pdf` (222,805 bytes, 10 pages) | The sole EHI export documentation artifact. A PDF describing a dual C-CDA XML + proprietary CSV export format. Contains section-level summaries of 14 C-CDA sections plus a CSV supplement description. Produced with Google Docs Renderer, copyright 2023. | **Primary artifact** — all export information comes from this single document |
| `export-format-documentation-page.png` (177,643 bytes) | Screenshot of the WordPress page hosting the PDF. Confirms the page layout: embedded PDF viewer with download button. | **Low value** — confirms page exists but adds no content |
| Live website verification (2026-02-16) | Verified `https://astronautehr.com/index.php/disclosures/export-format-documentation/` returns HTTP 200. Page last modified 2025-08-14 per metadata. PDF link is active. | Confirms artifact currency |

**No other artifacts exist.** There is no data dictionary, no schema file, no sample export, no field-level documentation of any kind. The entire EHI export documentation is a single 10-page PDF.

## 3. Export Mechanics

- **Format**: Dual format — C-CDA (XML) for clinical data; proprietary CSV (name-value pairs) for "advanced demographics and remaining EHI"
- **Mechanism**: Data is stored on a FHIR server. An authorized user must be granted permission by Astronaut EHR IT staff, who "walk the end-user through the process" of extraction. This is **vendor-assisted**, not self-service.
- **Single-patient**: Yes (documented)
- **Bulk export**: Yes (documented as available "through the capabilities of our FHIR server")
- **Access constraints**: Requires IT staff involvement to grant permissions and guide the user. No mention of fees for the export itself, though the product's disclosures page mentions hourly charges for other IT assistance.
- **Trigger**: Not described — no UI button, API endpoint, or command is specified

## 4. Export Content: What's In It

### Documentation depth

The PDF provides **zero field-level documentation**. There is:
- **No data dictionary** — not a single field name, data type, or field description
- **No schema files** — no XSD, JSON Schema, or other machine-readable artifact
- **No sample export files** — no example C-CDA document or CSV file
- **No value set documentation** — no coded fields enumerated
- **No relationship documentation** — no foreign keys, entity relationships, or data model information

The documentation consists entirely of section-level prose summaries, most paraphrased from HL7's C-CDA specification, plus a single fictional CSV example line.

### Vendor's own content organization

The vendor organizes the export into C-CDA sections plus a CSV supplement:

| Section | Type | Description Depth |
|---|---|---|
| Header (Demographics) | C-CDA header | XML snippet showing `<recordTarget>` and `<author>` tags; no field enumeration |
| Allergies | C-CDA section | ~40 words: medication allergies, adverse reactions, anaphylaxis, latex, iodine, tape |
| Immunizations | C-CDA section | ~54 words: current status and pertinent history |
| Medications | C-CDA section | ~43 words: current prescriptions and drug monitoring |
| Plan of Treatment | C-CDA section | ~191 words: pending orders, interventions, encounters, services, procedures, clinical reminders |
| Goals | C-CDA section | ~30 words: patient-defined goals and health concern goals |
| Problems | C-CDA section | ~30 words: current and historical problems, diagnoses |
| Results (Lab) | C-CDA section | ~189 words: hematology, chemistry, serology, virology, toxicology, microbiology, imaging, pathology |
| Vitals | C-CDA section | ~70 words: BP, HR, RR, height, weight, BMI, head circumference, pulse ox, temperature, BSA |
| Procedures | C-CDA section | ~105 words: interventional, surgical, diagnostic, therapeutic procedures |
| Social History | C-CDA section | ~35 words: smoking status, pregnancy; demographic data in header |
| Encounters | C-CDA section | ~80 words: healthcare encounters, visits, appointments, non-face-to-face interactions |
| Functional Status | C-CDA section | ~81 words: ADLs, mobility, self-care, IADLs |
| Medical Equipment | C-CDA section | ~31 words: implanted and external devices, DME |
| Assessments | C-CDA section | ~30 words: clinician conclusions, working assumptions, disease entities |
| Advanced Demographics & Remaining EHI | CSV supplement | ~100 words: name-value pairs. Single example: Place of Birth, Mother's Maiden Name, Spouse's Employer Name, Date of Retirement |

**Total documented sections**: 16 (14 C-CDA body sections + header + CSV supplement)
**Total documented fields**: 0 (no field-level documentation exists)
**Total description words across all sections**: ~1,000 words of paraphrased HL7 descriptions

The C-CDA section descriptions are largely paraphrased or quoted from HL7's official documentation, as the PDF itself acknowledges. The vendor directs users to HL7's C-CDA ↔ FHIR Index for "specifics of each section."

### CSV supplement detail

The CSV supplement is described in a single paragraph. The format uses alternating name-value pairs (not standard CSV with headers). The only concrete example shows 4 demographic fields: Place of Birth, Mother's Maiden Name, Spouse's Employer Name, Date of Retirement. The documentation claims "all available data will be present upon exportation" and that "categories that have no data assigned to them" are excluded, but does not enumerate what categories or fields exist.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor organizes the export into two components:

1. **C-CDA XML** (14 sections): Covers standard clinical data domains — allergies, immunizations, medications, problems, labs, vitals, procedures, encounters, goals, assessments, functional status, medical equipment, social history, and plan of treatment. This is a standard C-CDA clinical summary. The vendor provides no indication of whether vendor extensions, additional templates, or VistA-specific data beyond standard C-CDA elements are included.

2. **CSV supplement**: Described as covering "advanced demographics and remaining EHI." The only concrete example shows demographic fields not captured in C-CDA headers (place of birth, mother's maiden name, spouse's employer, retirement date). Whether this supplement includes billing, scheduling, orders, clinical notes, or other non-C-CDA data is **unknown** from the documentation. The vendor claims it covers "all available data" not in the C-CDA, but provides no enumeration.

The documentation's biggest weakness is the gap between its completeness claim and its specificity. It asserts coverage of the entire designated record set but documents only the C-CDA clinical summary in any detail, while hand-waving the rest into an undefined CSV format.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | C-CDA header (demographics, author). CSV supplement shows 4 additional demographic fields. No field enumeration. | Basic demographics likely present in C-CDA header; "advanced demographics" claimed via CSV but unverified |
| Encounters / visits | ⚠️ Partial | C-CDA "Encounters" section described | Standard C-CDA encounters section; likely limited to visit summaries, not full encounter data from VistA |
| Problems / conditions / diagnoses | ⚠️ Partial | C-CDA "Problems" section described | Standard C-CDA section; should cover problem list but level of detail from VistA unknown |
| Medications / prescriptions | ⚠️ Partial | C-CDA "Medications" section described | Standard prescriptions via C-CDA; e-prescribing data from Newcrop/Surescripts integration not addressed |
| Allergies | ⚠️ Partial | C-CDA "Allergies" section described | Standard C-CDA coverage |
| Immunizations | ⚠️ Partial | C-CDA "Immunizations" section described | Standard C-CDA coverage |
| Vitals | ⚠️ Partial | C-CDA "Vitals" section described | Standard C-CDA coverage; explicitly lists BP, HR, RR, height, weight, BMI, pulse ox, temp |
| Lab results | ⚠️ Partial | C-CDA "Results (Lab)" section — broadest description covering hematology, chemistry, serology, virology, toxicology, microbiology, imaging, pathology | Broad scope claimed; standard C-CDA section |
| Imaging / diagnostic reports | ⚠️ Partial | Mentioned within "Results (Lab)" section (imaging, pathology) | Covered as subset of results; product does radiology ordering |
| Procedures | ⚠️ Partial | C-CDA "Procedures" section described | Standard C-CDA coverage |
| Clinical notes / documents | ❌ Not covered | No dedicated section for clinical notes/progress notes. "Assessments" section covers clinician conclusions but not full note text. | **Significant gap.** VistA's TIU (Text Integration Utilities) stores extensive clinical documentation. Product markets "hundreds of pre-built clinically proven templates" and "Rocket Note." None of this appears in the export documentation. |
| Care plans / goals | ⚠️ Partial | C-CDA "Goals" and "Plan of Treatment" sections | Standard C-CDA coverage |
| Orders / referrals | ⚠️ Partial | "Plan of Treatment" covers pending orders. No historical order data described. | Product has full CPOE; completed/historical orders not addressed |
| Insurance / coverage | ❌ Not covered | No mention of insurance/coverage data in any section | Product stores insurance as part of demographics; not documented in export |
| Claims / billing | ❌ Not covered | No mention of charges, claims, payments, billing codes | Product has billing capabilities ("Rocket Note" billing, staff billers); gap significance depends on billing depth, which is ambiguous |
| Payments | ❌ Not covered | No mention | May be N/A if billing is limited to code capture |
| Consents / directives | ❌ Not covered | No mention of advance directives or consent documents | VistA stores advance directives; not documented |
| Patient communications / portal messages | ❌ Not covered | No mention | Product is (e)(3) certified for patient access; portal/messaging capability unclear |
| Specialty-specific (psychiatry) | ❌ Not covered | No mention of behavioral health assessments, psychiatric evaluations, or specialty clinical data | Founder is a psychiatrist; product has "Turbo Supervision" for mid-level providers. Any specialty clinical data stored would be a gap. |

**Summary**: All "⚠️ Partial" ratings reflect that C-CDA sections are *claimed* to be present but no field-level detail exists to verify actual content. The export may well contain standard C-CDA data for these domains, but the documentation does not allow verification. The "❌ Not covered" domains represent data the product likely stores but that has no representation in the export documentation at all — whether the CSV supplement captures any of this is unknown.

## 6. Documentation Quality

**Can a developer build an import from this documentation?** No. The documentation provides:
- Generic C-CDA XML structure (3 code snippets showing tag hierarchy)
- Section-level summaries paraphrased from HL7's official spec
- A link to HL7's C-CDA ↔ FHIR Index website
- A single line of fictional CSV data

A developer would need to: (1) use HL7's C-CDA specification to parse the XML portion, treating it as a standard C-CDA document, and (2) reverse-engineer the CSV format from actual export files, since the name-value pair format has no schema, no field enumeration, and only 4 example fields.

**Machine-readable artifacts**: None. No XSD, JSON Schema, sample files, or structured documentation of any kind.

**What's well-documented**: The fact that the export exists, uses C-CDA + CSV, and is accessible via a FHIR server with IT assistance.

**What requires guesswork**: Everything else — which fields are in each C-CDA section, what "remaining EHI" the CSV contains, how the CSV is structured beyond the brief example, what VistA FileMan files are covered, and whether billing/scheduling/notes/specialty data are included.

## 7. Overall Assessment

### Classification

**Standard-based projection**

The export is primarily a C-CDA clinical summary with a vaguely described CSV supplement. The C-CDA portion covers the standard clinical domains that any C-CDA document would — this is not a native database export of VistA's FileMan model. The CSV supplement *could* contain additional data, but the documentation provides no evidence of what it includes beyond 4 demographic fields. There is no data dictionary, no schema, and no indication that the vendor's native data model (VistA's hundreds of FileMan files) is exported.

### Key Findings

1. **The entire EHI export documentation is a single 10-page PDF with zero field-level detail.** No data dictionary, no schema, no sample files. The 14 C-CDA section descriptions are paraphrased from HL7's own documentation, totaling ~1,000 words of section summaries.

2. **The export is structurally a C-CDA clinical summary**, not a native VistA/FileMan data export. Despite VistA's rich, well-documented data model with hundreds of files, the vendor chose to project data into standard C-CDA sections rather than expose the native model.

3. **Clinical notes are not addressed.** VistA's TIU (Text Integration Utilities) system is a core strength of the platform, storing extensive clinical documentation. The product markets "hundreds of pre-built clinically proven templates." None of this appears in the export documentation — there is no "Notes" or "Documents" section.

4. **The CSV "remaining EHI" supplement is a black box.** It is described in ~100 words with a single 4-field demographic example. It could theoretically contain billing, scheduling, and other non-clinical data, but the documentation provides no evidence of this. The claim that "all available data will be present" is unverifiable.

5. **Export requires vendor IT staff involvement**, making it neither self-service nor truly patient-accessible. Users must be "granted permission by Astronaut EHR's IT staff" who "walk the end-user through the process."

### Summary Stats

```
Classification:  Standard-based projection
Export format:   C-CDA (XML) + proprietary CSV
Model type:      Standard projection (C-CDA) + undefined supplement
Entities:        0 (no data dictionary; 16 C-CDA sections described)
Fields:          0 (no field-level documentation)
Descriptions:    N/A (no fields to describe)
Sample data:     No
Bulk export:     Yes (claimed)
Domains covered: 0 of 14 fully verified; 10 of 14 partially claimed via C-CDA sections
```

### Bottom Line

This is a minimal compliance effort. The documentation describes a standard C-CDA clinical summary — the same type of document produced by any certified EHR for transitions of care — and labels it as the (b)(10) EHI export. The vaguely described CSV supplement may contain additional data, but without any field enumeration, schema, or sample, its content is unknowable from the documentation. For a product built on VistA — which has one of the most thoroughly documented and comprehensive data models in healthcare IT — the absence of any native data model export or field-level documentation is a significant missed opportunity. A patient or provider receiving this export would get a standard clinical summary, not a complete copy of their data.
