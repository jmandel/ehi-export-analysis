# EHI Export Analysis: Astronaut, LLC

**Product**: Astronaut EHR
**Analysis date**: 2026-02-16
**CHPL IDs**: 15.02.05.3099.ASTR.01.00.1.220201

## 1. Product Context

Astronaut EHR is a cloud-based adaptation of **VistA** (the VA's open-source EHR), built by a small Houston-based company founded by Dr. Ignacio Valdes, a psychiatrist. The product uses a customized CPRS client ("Astro-CPRS") and targets small ambulatory practices and community health centers. It is certified across 30+ ONC criteria including (b)(10).

Because it inherits VistA's architecture, the product has broad clinical capabilities:
- **CPOE**: medication, lab, radiology, diet, and procedure ordering
- **Clinical documentation**: progress notes via TIU templates ("hundreds of pre-built clinically proven templates"), problem lists, medication lists, allergy tracking
- **Lab and imaging**: ordering and results management
- **Vitals, immunizations, family health history, implantable devices**
- **E-prescribing**: via Newcrop/Surescripts integration (including EPCS)
- **Scheduling**: enterprise appointment scheduling, ADT functions
- **Consults**: specialty consultation requesting and tracking
- **Quality reporting**: 16 CQMs, QRDA capability
- **Proprietary features**: "Rocket Note" (follow-up notes + billing), "Turbo Supervision" (NP/PA supervision tools)

**Billing**: The depth is unclear. The product references billing (via "Rocket Note," biller staff, and billing-related disclosures charges), but whether it performs full practice management/claims processing or just captures billing codes during documentation is ambiguous. VistA's original architecture included billing modules.

**Patient portal/messaging**: Certified for patient electronic access (e)(3) but no standalone portal described.

For (b)(10) assessment, the key question is whether the export covers VistA's extensive internal data model or just the standard C-CDA clinical summary surface.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/Astronaut-EHR-Export-Format-Documentation.pdf` | 10-page PDF (222 KB), copyright 2023. Describes C-CDA + CSV export format. Contains section-level summaries of 14 C-CDA sections and a brief description of a proprietary CSV for "remaining EHI." No data dictionary, no field lists, no schema, no sample data. | **Primary artifact; low information density** |
| `downloads/export-format-documentation-page.png` | Screenshot of the vendor's export documentation web page showing the embedded PDF viewer. | Minimal value (confirms page layout only) |

**Total artifacts: 2.** One substantive document (the PDF) and one screenshot. No sample export files, no data dictionary, no machine-readable schema.

## 3. Export Mechanics

- **Format**: Dual format — C-CDA XML for clinical data + proprietary CSV (name-value pairs) for "advanced demographics and remaining EHI"
- **Mechanism**: Vendor-assisted. Data is stored on a FHIR server; authorized users must be granted permissions by "Astronaut EHR's IT staff" who "will walk an end-user through the process." This is not a self-service export.
- **Single-patient vs bulk**: Documentation states both "Single Patient Export and/or a Bulk Patient Export" are available through the FHIR server.
- **Access constraints**: Requires authorization from vendor IT staff. No mention of fees for the export itself, though the vendor's disclosures page mentions hourly charges for other services.

## 4. Export Content: What's In It

### No data dictionary exists

The 10-page PDF provides **zero field-level documentation**. There is no data dictionary, no schema, no field list, no type definitions, no value sets, and no sample export files. The documentation consists of:

1. **Generic C-CDA format explanation** (pages 3-5): XML structure overview with placeholder examples (`<!-- Allergy Details -->`)
2. **Section summaries** (pages 5-9): 14 C-CDA section descriptions paraphrased/quoted from HL7's official C-CDA documentation (the PDF itself states these are "paraphrased/quoted from HL7's website")
3. **CSV description** (page 9): A single paragraph with one fictional 4-field example

### Vendor's own content organization

The vendor organizes the export into two components:

**Component 1: C-CDA XML** — 14 sections

| Section | Fields Documented | Types | Description Source |
|---|---|---|---|
| Allergies | 0 | No | HL7 C-CDA spec (paraphrased) |
| Immunizations | 0 | No | HL7 C-CDA spec (paraphrased) |
| Medications | 0 | No | HL7 C-CDA spec (paraphrased) |
| Plan of Treatment | 0 | No | HL7 C-CDA spec (paraphrased) |
| Goals | 0 | No | HL7 C-CDA spec (paraphrased) |
| Problems | 0 | No | HL7 C-CDA spec (paraphrased) |
| Results (Lab) | 0 | No | HL7 C-CDA spec (paraphrased) |
| Vitals | 0 | No | HL7 C-CDA spec (paraphrased) |
| Procedures | 0 | No | HL7 C-CDA spec (paraphrased) |
| Social History | 0 | No | HL7 C-CDA spec (paraphrased) |
| Encounters | 0 | No | HL7 C-CDA spec (paraphrased) |
| Functional Status | 0 | No | HL7 C-CDA spec (paraphrased) |
| Medical Equipment | 0 | No | HL7 C-CDA spec (paraphrased) |
| Assessments | 0 | No | HL7 C-CDA spec (paraphrased) |

**Component 2: Proprietary CSV** — "Advanced Demographics and Remaining EHI"

| Content | Fields Documented | Description |
|---|---|---|
| Demographics + "remaining EHI" | 4 (examples only) | Name-value pair CSV. Example fields: Place of Birth, Mother's Maiden Name, Spouse's Employer Name, Date of Retirement |

**Total documented fields across all components: 4** (all from a single fictional example; none are formally documented with types, constraints, or completeness guarantees).

The complete entity inventory is saved in `analysis/entity-inventory-full.json` (16 entities, 4 documented fields).

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor describes two export components:

1. **C-CDA XML**: Covers the standard C-CDA clinical document sections. The vendor provides no product-specific mapping — the documentation explicitly directs users to "HL7's official C-CDA documentation" for field details. There is no indication of vendor extensions, custom sections, or mappings beyond the standard C-CDA template. This is a **standard C-CDA export** with no product-specific enrichment documented.

2. **Proprietary CSV**: Described as covering "advanced demographics and remaining EHI." This is the only component that goes beyond standard C-CDA, but the documentation provides essentially no detail about what it contains. The four example fields (Place of Birth, Mother's Maiden Name, Spouse's Employer Name, Date of Retirement) are extended demographics — not clinical, billing, or operational data. The documentation says "all available data will be present" but provides no enumeration of what "all available data" includes. Without a field list or sample data, this claim cannot be verified.

The C-CDA component is the thinnest possible documentation — literally just a paraphrase of the standard. The CSV component has a promising name ("remaining EHI") but lacks any substantiation.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | C-CDA header (demographics, marital status, race, ethnicity, religion). CSV has extended demographics (Place of Birth, Mother's Maiden Name, etc.) | Basic demographics via C-CDA standard; extended demographics via CSV but undocumented |
| Encounters / visits | ⚠️ Partial | C-CDA Encounters section | Standard C-CDA encounter data only; no VistA-specific visit detail |
| Problems / conditions | ⚠️ Partial | C-CDA Problems section | Standard C-CDA; VistA problem list has many more fields |
| Medications / prescriptions | ⚠️ Partial | C-CDA Medications section | Standard C-CDA; no e-prescribing detail (Newcrop/Surescripts data) |
| Allergies | ⚠️ Partial | C-CDA Allergies section | Standard C-CDA representation |
| Immunizations | ⚠️ Partial | C-CDA Immunizations section | Standard C-CDA representation |
| Vitals | ⚠️ Partial | C-CDA Vitals section | Standard C-CDA representation |
| Lab results | ⚠️ Partial | C-CDA Results section | Standard C-CDA; VistA lab module is far more detailed |
| Imaging / diagnostic reports | ⚠️ Partial | C-CDA Results section mentions imaging | Imaging results may appear in Results section, but no dedicated imaging export |
| Procedures | ⚠️ Partial | C-CDA Procedures section | Standard C-CDA representation |
| Clinical notes / documents | ❌ Not covered | No dedicated notes export | VistA/TIU has extensive note content; C-CDA may embed some notes but no documentation of this. "Hundreds of pre-built templates" suggests rich note data not covered |
| Care plans / goals | ⚠️ Partial | C-CDA Plan of Treatment + Goals sections | Standard C-CDA representation |
| Orders / referrals | ⚠️ Partial | C-CDA Plan of Treatment (pending orders only) | CPOE ordering data (medications, labs, radiology) is a core product feature; only pending orders appear in Plan of Treatment |
| Insurance / coverage | ❌ Not covered | No insurance entities documented | Product stores insurance info in demographics; not documented in export |
| Claims / billing | ❌ Not covered | No billing entities in export | "Rocket Note" feature references billing; billing depth unclear but any billing data is absent from documented export |
| Payments | ❌ Not covered | No payment entities | May not be applicable if product doesn't do full billing |
| Consents / directives | ❌ Not covered | Not mentioned | Product handles advance directives in clinical context; not exported |
| Patient communications | ❌ Not covered | Not mentioned | Limited patient portal capability; may be N/A |
| Scheduling data | N/A | Not EHI | Scheduling is generally not part of the designated record set |
| Specialty-specific (psychiatry) | ❌ Not covered | Not mentioned | Dr. Valdes's psychiatry background and Blue Bonnet Clinic use suggest psychiatric-specific data (assessments, treatment plans); none documented in export |

## 6. Documentation Quality

The documentation quality is **extremely poor**:

- **No data dictionary**: Zero fields are formally documented with names, types, constraints, or value sets.
- **No product-specific mapping**: The C-CDA section descriptions are paraphrased from HL7's website, not mapped to Astronaut/VistA's internal data model.
- **No sample data**: No example export files are provided.
- **No machine-readable artifacts**: No JSON schema, XML schema, CSV template, or any other machine-readable format definition.
- **No relationship documentation**: No foreign keys, no cross-references between entities.
- **Fictional example only**: The only concrete data example is a 4-field fictional CSV snippet.
- **Vendor-assisted access**: A developer cannot independently access or interpret the export from this documentation alone. The documentation says Astronaut's "IT staff will walk an end-user through the process."

A developer attempting to build an import from this documentation would have essentially nothing to work with beyond the generic C-CDA specification (which applies to any C-CDA-producing system, not Astronaut specifically) and a vague description of a CSV format with no field enumeration.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Minimal/stub/unclear**

The documentation is too thin to assess actual coverage. The C-CDA component covers the standard USCDI-scope clinical summary — this is the minimum regulatory floor for clinical exchange, not a comprehensive EHI export. The CSV component claims to cover "remaining EHI" but provides no evidence of what that includes. VistA's data model has potentially hundreds of FileMan files/tables; the documented export covers 14 standard C-CDA sections with zero product-specific field detail. Key domains like clinical notes (TIU), detailed orders (CPOE), billing, insurance, and specialty-specific psychiatric data are entirely absent from the documentation. The gap between what VistA/Astronaut stores and what this export documents is enormous.

**Axis 2 — Export approach: Repackaged existing export**

The C-CDA component is clearly the vendor's existing clinical document exchange capability (certified under (b)(1)/(b)(3)) relabeled for (b)(10). The telltale signs are unmistakable:
- Section descriptions are explicitly "paraphrased/quoted from HL7's website"
- Documentation directs users to HL7's C-CDA spec for field details rather than providing product-specific mapping
- No vendor extensions, custom sections, or mappings beyond the standard C-CDA template are documented
- The 14 C-CDA sections map directly to standard C-CDA sections, with no billing, administrative, or specialty data

The CSV add-on for "remaining EHI" shows some awareness that C-CDA alone is insufficient, but with only 4 example fields (all extended demographics), no field enumeration, and no sample data, it appears to be a nominal gesture rather than a substantive export expansion.

### Key Findings

1. **Documentation is essentially empty**: 10 pages that contain no product-specific data dictionary, no field list, no schema, and no sample data. The C-CDA section descriptions are copied from HL7's website. This is among the thinnest (b)(10) documentation possible while still having a document to point to.

2. **Standard C-CDA relabeled as (b)(10)**: The export's clinical component is a standard C-CDA — the same format used for transitions of care under (b)(1)/(b)(3). No evidence of coverage beyond USCDI-scope clinical summary data.

3. **"Remaining EHI" CSV is unsubstantiated**: The CSV component is described in a single paragraph with a 4-field example. It could contain significant data or virtually nothing — without a field list or sample data, the claim that it covers "remaining EHI" cannot be verified.

4. **Massive gap relative to product capabilities**: VistA's FileMan database has hundreds of file definitions. Astronaut inherits this architecture and adds proprietary features (Rocket Note, Turbo Supervision). The documented export covers only the standard C-CDA clinical summary surface — a tiny fraction of what the system stores.

5. **Vendor-assisted access model**: Users cannot self-serve; Astronaut's IT staff must grant permissions and walk users through the process. This creates a practical barrier to exercising the (b)(10) export right.

### Summary Stats

```
Coverage:        Minimal/stub/unclear
Approach:        Repackaged existing export
Export format:   C-CDA XML + proprietary CSV (name-value pairs)
Entities:        16 (14 C-CDA sections + 1 CSV component + 1 C-CDA header)
Fields:          4 (example fields only; no formal field documentation)
Descriptions:    0% (no fields formally documented)
Sample data:     No
Bulk export:     Yes (claimed)
Domains covered: ~7-8 of 15+ applicable domains (all via standard C-CDA only, no depth)
```

### Bottom Line

This is a standard C-CDA clinical summary with a vaguely described CSV attachment, presented as a (b)(10) EHI export. The documentation provides zero product-specific field-level detail — a developer would have no more information about Astronaut's data model after reading it than before. Given that the product is built on VistA (with hundreds of underlying data files), the gap between what the system stores and what the export documents is vast. The single biggest issue is the complete absence of any data dictionary or substantive documentation of what the export actually contains.
