# EHI Export Analysis: MDOps Corporation

**Product**: MDLog v5.0
**Analysis date**: 2026-02-16
**CHPL ID**: 15.99.05.1836.MDOP.01.01.1.220117 (CHPL ID 10792)

## 1. Product Context

MDLog is a cloud-based, voice-controlled clinical documentation EHR designed for long-term care (LTC) and post-acute care physicians. It targets physicians and nurse practitioners who round at skilled nursing facilities (SNFs), assisted living, and similar settings. MDLog is positioned as the **physician's charting layer** that integrates with facility-level EHRs like PointClickCare and MatrixCare — the facility EHR holds the comprehensive patient record while MDLog handles physician documentation.

Key data-storing capabilities relevant to EHI export completeness:

- **Clinical notes**: Core function — voice-dictated encounter notes, progress notes, consult notes, wound care notes, CCM notes, admission/discharge documentation
- **Patient demographics**: Name, contact info, facility assignment
- **Medications**: CPOE for medications (a)(1), e-prescribing via NewCrop
- **Lab orders/results**: CPOE for labs (a)(2), results imported from facility EHRs
- **Care plans**: Certified for (b)(9)
- **Implantable device list**: Certified for (a)(14)
- **Billing/charges**: Charge capture at point of care via billing portal (not full claims/AR)
- **Patient portal**: Messages via MDPortal, health info in C-CDA format
- **Clinical quality measures**: CQM recording and export
- **Chronic care management**: CCM encounter documentation with time tracking

MDLog is a small niche product ($249-$299/month per provider) serving small geriatrics and elder care practices. Its scope is narrower than a full hospital EHR — it does not appear to store imaging, radiology, detailed nursing assessments, or MDS data (those reside in the facility EHR).

## 2. Artifacts Reviewed

| Artifact | Size | Description | Informativeness |
|---|---|---|---|
| `downloads/ccd-schema.xml` | 85,354 bytes (1,351 lines) | HL7 CDA R2 XML Schema (POCD_MT000040) — the standard clinical document architecture schema. Contains a vendor comment: "Supported EHI export format(s) : XML". 88 complex types. | **Low** — This is the unmodified standard schema, not a vendor-specific data dictionary. |
| `downloads/datatype-schema.xml` | 65,977 bytes (1,377 lines) | HL7 v3 data type schema. 37 complex types defining coded values, identifiers, timestamps, etc. | **Low** — Standard HL7 data types, no vendor customization. |
| `downloads/voc-schema.xml` | 84,535 bytes (2,123 lines) | HL7 v3 vocabulary schema. 183 simple types with 657 enumeration values for coded fields. | **Low** — Standard HL7 vocabulary, no vendor customization. |
| `downloads/narrative-block-schema.xml` | 24,950 bytes (543 lines) | CDA narrative block schema for structured text. 25 complex types. | **Low** — Standard narrative schema. |
| `downloads/enrichment/schema-extract.json` | 329,764 bytes | Prior agent's JSON extraction of schema content. | **Reference** — Used to cross-check parsing. |
| `product-research.md` | — | Product research from vendor website | **High** — Established what MDLog stores. |
| `ehi-export-report.md` | — | Prior agent's analysis | **Medium** — Orientation; findings verified. |

**Most informative**: `product-research.md` (for understanding what the product stores) and the vendor comment in `ccd-schema.xml` (the only MDLog-specific content in any artifact).

**Least informative**: The four XSD files themselves — they are the **standard, unmodified HL7 CDA R2 schema** published by Health Level Seven, not a product-specific data dictionary. They tell us nothing about what MDLog actually exports.

## 3. Export Mechanics

- **Format**: XML, conforming to HL7 CDA R2 / C-CDA (per the vendor comment "Supported EHI export format(s) : XML" in `ccd-schema.xml`)
- **Mechanism**: Unknown. No export instructions, UI documentation, or API documentation was found. The registered (b)(10) URL (`https://pcc-demo.mdops.com/api/viewCCDSchema`) serves the schema definition, not an export interface.
- **Single-patient vs bulk**: Unknown. No documentation addresses this.
- **Access constraints**: Unknown. The demo site (`pcc-demo.mdops.com`) requires authentication. No documentation describes how a patient or provider initiates an export.
- **Fees**: Unknown. No pricing information for EHI export was found.

## 4. Export Content: What's In It

### What the documentation actually provides

The entire EHI export documentation consists of the **standard HL7 CDA R2 XML schema** (POCD_MT000040) — the same schema that underlies all C-CDA documents. The only vendor-specific content is a single XML comment at the top of `ccd-schema.xml`:

```
Supported EHI export format(s) : XML
```

There is **no vendor-specific data dictionary**, no mapping of MDLog data fields to CDA elements, no documentation of which CDA sections are populated, no sample export files, and no export instructions.

### Schema statistics (from `analysis/entity-inventory-full.json`)

Since the only artifacts are standard CDA schemas, the "entities" are CDA complex types:

- **Total entities (complex types)**: 150 (across 4 schema files)
- **Total fields (elements + attributes)**: 1,270
- **Fields with descriptions**: 0 (0.0%) — the standard CDA schema contains no field-level descriptions
- **Fields with data types**: 1,248 (98.3%)
- **Value sets**: 168 simple types with 657 enumeration values

### Standard CDA types by domain (not MDLog-specific)

These are the standard CDA R2 schema types, categorized by clinical domain. This reflects the **theoretical capacity** of CDA, not what MDLog actually exports:

| Domain | Entities | Fields | Notes |
|---|---|---|---|
| Clinical Data | 11 | 191 | Observation, Procedure, Encounter, Act, Organizer, etc. |
| Document Structure | 21 | 220 | ClinicalDocument, Section, Entry, Components, etc. |
| Participants | 19 | 169 | Authors, performers, various role types |
| Medications | 7 | 94 | SubstanceAdministration, Supply, ManufacturedProduct, etc. |
| Demographics | 5 | 52 | Patient, PatientRole, Guardian, etc. |
| Provenance | 7 | 56 | Author, Authenticator, DataEnterer, Custodian |
| Organization | 5 | 45 | Organization, HealthCareFacility, Location, Place |
| References | 4 | 38 | ExternalAct/Document/Observation/Procedure |
| Devices | 2 | 19 | Device, AuthoringDevice |
| Consent | 2 | 15 | Authorization, Consent |
| Laboratory | 2 | 13 | Specimen, SpecimenRole |
| Orders | 1 | 9 | Order |
| Infrastructure | 1 | 2 | typeId |
| Other (data types, narrative) | 63 | 347 | HL7 data types and narrative block types |

**Critical caveat**: These numbers describe the **standard CDA specification**, not MDLog's actual export content. Without vendor documentation of which sections/templates are used, or a sample export file, we cannot determine what data MDLog actually places into this format.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor provides **no product-specific documentation** of export content. The entire (b)(10) documentation is a pointer to the standard HL7 CDA R2 schema. There are no vendor-defined categories, sections, or data mappings.

The only information available is:
1. The export format is XML (per the schema comment)
2. The schema is CDA R2 / C-CDA (the same format used for transitions of care under (b)(1))

This strongly suggests the (b)(10) export is the same C-CDA document used for transitions of care, repackaged as the EHI export. The URL itself is `viewCCDSchema` — CCD being the Continuity of Care Document, a clinical summary format.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | CDA Patient/PatientRole types exist in schema, but no MDLog-specific field mapping | Product stores demographics (a)(5); likely present in C-CDA but depth unknown |
| Encounters / visits | ⚠️ Partial | CDA Encounter type exists; no specifics on MDLog encounter notes | Core product function (dictated encounter notes); likely in C-CDA but completeness unknown |
| Problems / conditions | ⚠️ Partial | CDA Observation/Act types could carry this; no mapping documented | Likely in C-CDA if used |
| Medications / prescriptions | ⚠️ Partial | CDA SubstanceAdministration type exists | Product does CPOE (a)(1) and e-prescribing; likely in C-CDA but unknown depth |
| Allergies | ⚠️ Partial | Could be carried in CDA Observation; no documentation | Product likely tracks allergies via medication workflow; unknown |
| Immunizations | ⚠️ Partial | Could be carried in CDA SubstanceAdministration; no documentation | Not a core MDLog feature; may not be present |
| Vitals | ⚠️ Partial | CDA Observation type exists | Vitals likely in facility EHR, not MDLog; possibly N/A |
| Lab results | ⚠️ Partial | CDA Observation/Organizer types exist | Product imports labs from facility EHRs; may or may not be in export |
| Imaging / diagnostic reports | N/A | — | MDLog does not appear to store imaging data |
| Procedures | ⚠️ Partial | CDA Procedure type exists | May be documented in notes but not as structured data |
| Clinical notes / documents | ⚠️ Partial | CDA Section/NonXMLBody could carry notes | **Core product function** — dictated notes are the primary data. C-CDA can carry these, but completeness of all note types is unknown |
| Care plans / goals | ⚠️ Partial | CDA Act type could carry this | Product certified for (b)(9) care plan |
| Orders / referrals | ⚠️ Partial | CDA Order type exists (1 entity, 9 fields) | Product does CPOE; unknown if orders are in export |
| Insurance / coverage | ❌ Not covered | No specific insurance/coverage mechanism in standard CDA | MDLog may store basic insurance info; C-CDA has limited support for this |
| Claims / billing | ❌ Not covered | CDA has no mechanism for billing/charge data | **Product has billing portal** for charge capture; significant gap |
| Payments | ❌ Not covered | CDA has no payment mechanism | Product captures charges; gap if payment data exists |
| Consents / directives | ⚠️ Partial | CDA Consent/Authorization types exist | Unknown if used |
| Patient communications | ❌ Not covered | CDA has no mechanism for portal messages | **Product has MDPortal** with secure messaging; gap |
| CCM encounter data | ❌ Not covered | CDA has no mechanism for time-tracking CCM data | Product has CCM module with timer-based billing; gap |
| Wound care assessments | ❌ Not covered | Standard CDA has no specialty wound care templates | Product has wound care documentation; gap |
| Clinical quality measures | ❌ Not covered | CDA has no CQM reporting mechanism | Product captures CQM data; gap |

**Note**: Nearly all clinical domains are marked "Partial" rather than "Covered" because we have **no evidence** of what MDLog actually puts into the C-CDA. The schema says what *could* be there; without a sample export or data dictionary, we cannot confirm what *is* there.

## 6. Documentation Quality

**Extremely poor.** The documentation fails on every dimension:

- **No export instructions**: A user cannot determine how to perform an EHI export from these documents.
- **No data dictionary**: No mapping between MDLog's internal data model and the CDA schema elements.
- **No section documentation**: No list of which CDA sections (Problems, Medications, Results, Vitals, etc.) are populated.
- **No field-level documentation**: 0 of 1,270 fields in the schema have descriptions (though this is inherent to the standard CDA schema, not a vendor-specific shortcoming — the vendor simply didn't provide any product-specific documentation at all).
- **No sample data**: No example export files.
- **No machine-readable mapping**: No vendor-specific profiles, templates, or implementation guides.
- **No relationship documentation**: No foreign keys, no entity relationships beyond what CDA defines.

A developer receiving this documentation would know the export is "XML" and could look up the CDA R2 specification independently, but would have **no idea** what MDLog data to expect, which CDA sections are present, what template IDs are used, or how to interpret vendor-specific content.

**Could a developer build an import?** No. They would need to reverse-engineer the actual export files to understand the content.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Minimal/stub/unclear**

The documentation is too thin to assess actual coverage. The only evidence is a standard CDA R2 schema with a one-line comment saying the export format is XML. No product-specific data dictionary, no field mappings, no sample data, and no documentation of which CDA sections are populated. Even if the underlying C-CDA export covers standard clinical domains (demographics, medications, problems, notes), the documentation provides zero evidence of this. And even if it does cover those domains, C-CDA fundamentally cannot carry MDLog's billing/charge data, CCM time-tracking data, wound care assessments, patient portal messages, or clinical quality measure data — all of which MDLog stores.

**Axis 2 — Export approach: Repackaged existing export**

The evidence strongly indicates this is MDLog's existing C-CDA/transitions-of-care capability relabeled as (b)(10):

1. The registered URL is literally `viewCCDSchema` — CCD is the Continuity of Care Document, a clinical summary format.
2. The schema is the **unmodified standard HL7 CDA R2 schema** (POCD_MT000040), identical to what any C-CDA implementation uses.
3. MDLog is certified for transitions of care (b)(1), which requires C-CDA generation — the same capability.
4. There is no evidence of any vendor-specific extensions, profiles, or data beyond what a standard C-CDA would contain.
5. The C-CDA format has no mechanism for billing, portal messages, CCM data, or specialty assessments — domains MDLog stores.

### Key Findings

1. **The entire (b)(10) documentation is a single standard schema file.** MDOps provides the unmodified HL7 CDA R2 XML schema as their EHI export documentation, with no vendor-specific content beyond a one-line comment ("Supported EHI export format(s) : XML"). This is the most minimal possible documentation — it tells a recipient the format but nothing about the content.

2. **This is almost certainly a repackaged C-CDA export.** The `viewCCDSchema` URL, the standard CDA schema, and the lack of any vendor extensions all indicate MDOps is pointing to their existing transitions-of-care (b)(1) C-CDA capability and calling it (b)(10). No purpose-built EHI export work is evident.

3. **C-CDA cannot carry several data domains MDLog stores.** Even if the C-CDA export is well-populated with clinical data, it has no mechanism for billing/charge data (billing portal), patient portal messages (MDPortal), CCM time-tracking data, wound care assessments, or CQM data — all of which are part of MDLog's designated record set.

4. **Zero product-specific documentation exists.** No data dictionary, no field mappings, no sample exports, no export instructions. A developer or patient receiving this documentation cannot determine what data the export contains or how to use it.

5. **MDLog's scope is narrow, which limits the severity.** As a physician charting layer for LTC (not a full hospital EHR), MDLog stores less data than larger systems. The designated record set is primarily clinical notes, demographics, medications, and charges. But even against this limited scope, the documentation fails to demonstrate coverage.

### Summary Stats

```
Coverage:        Minimal/stub/unclear
Approach:        Repackaged existing export
Export format:   XML (C-CDA / CDA R2)
Entities:        150 (standard CDA complex types, not vendor-specific)
Fields:          1,270 (standard CDA elements/attributes, not vendor-specific)
Descriptions:    0% (standard schema has none; no vendor docs provided)
Sample data:     No
Bulk export:     Unclear
Domains covered: 0 confirmed (all ⚠️ Partial at best due to lack of documentation)
```

### Bottom Line

MDOps provides the bare minimum compliance artifact — a standard CDA R2 schema file with a comment saying the export format is XML. This is a textbook example of a repackaged C-CDA export with no evidence of purpose-built (b)(10) work. A patient or provider cannot determine what data is in the export, how to obtain it, or how to interpret it. The biggest gap is not any single missing domain but the complete absence of product-specific documentation — there is literally nothing connecting MDLog's data model to the export format.
