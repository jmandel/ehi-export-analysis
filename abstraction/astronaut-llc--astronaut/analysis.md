# EHI Export Analysis: Astronaut, LLC

**Product**: Astronaut (version 1709)
**Analysis date**: 2026-02-15
**CHPL ID**: 15.02.05.3099.ASTR.01.00.1.220201

## 1. Product Context

Astronaut EHR is a cloud-based adaptation of VistA (the VA's open-source EHR) built by Astronaut, LLC, a small Houston-based company founded by psychiatrist Dr. Ignacio Valdes. The product uses a customized version of VistA's CPRS client ("Astro-CPRS") and targets small ambulatory practices and community health centers.

Because it inherits VistA's architecture, Astronaut has a broad clinical footprint. Certified capabilities include:

- **Clinical**: CPOE for medications/labs/imaging (a)(1)–(a)(3), drug interaction checks (a)(4), demographics (a)(5), family health history (a)(12), implantable device list (a)(14)
- **Care coordination**: C-CDA transitions of care (b)(1), e-prescribing via Newcrop/Surescripts (b)(3)
- **Documentation**: Progress notes via VistA's TIU templating system, "Rocket Note" for efficient follow-up notes and billing capture
- **APIs**: FHIR R4 (g)(10), CCDA Web API (g)(7)/(g)(9)
- **Public health**: Immunization registry (h)(1)
- **Quality**: 16 CQMs (c)(1)

**Billing depth is ambiguous.** The vendor has "billers" on staff and "Rocket Note" integrates billing code capture with documentation, but whether the product includes full practice management/billing or just billing code capture during clinical documentation is unclear from available evidence.

**Data domains the export should cover**: demographics, problems/diagnoses, medications, allergies, lab results, imaging, vitals, immunizations, procedures, clinical notes, encounters, care plans/goals, orders (CPOE), e-prescribing records, family health history, implantable devices, and any billing data the product stores.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `Astronaut-EHR-Export-Format-Documentation.pdf` (222 KB, 10 pages) | The sole export documentation artifact. Describes a dual C-CDA + CSV export format with section-level C-CDA summaries and a brief CSV description. | **Primary source** — but very thin. No data dictionary, no schemas, no sample data. |
| `export-format-documentation-page.png` (178 KB) | Screenshot of the WordPress page hosting the PDF. Shows embedded PDF viewer and download button, no additional content. | Low — confirms no additional documentation on the page. |
| Live website: `astronautehr.com/index.php/disclosures/` | Disclosures page listing certifications, API docs, costs. Verified accessible 2026-02-15. | Low for EHI export specifically — no additional export documentation beyond the PDF link. |
| Live website: `astronautehr.com/index.php/disclosures/export-format-documentation/` | Export format documentation page. Verified accessible 2026-02-15. Contains only the embedded PDF. | Confirmed: no additional artifacts beyond the PDF. |

**Total artifacts**: 1 PDF document (the entire export documentation). No data dictionary, no schema files, no sample exports.

## 3. Export Mechanics

- **Format**: Dual format — C-CDA (XML) for clinical data, proprietary CSV (name-value pairs) for "advanced demographics and remaining EHI"
- **Mechanism**: Data is stored on a FHIR server. An authorized user must be granted permission by Astronaut EHR IT staff, who "walk an end-user through the process." This is **IT staff-assisted**, not self-service.
- **Single-patient**: Yes
- **Bulk export**: Yes (documentation states both single and bulk options are available "through the capabilities of our FHIR server")
- **Access constraints**: Requires IT staff involvement; user must be granted permission. No mention of fees specifically for export, though the disclosures page lists hourly charges for other assistance activities.

## 4. Export Content: What's In It

### Overview

The entire export specification is contained in a 10-page PDF (~1,779 words of substantive content). The documentation describes what amounts to a standard C-CDA clinical summary plus a vaguely defined CSV supplement, with no field-level detail for either component.

### C-CDA Component

The PDF documents 14 C-CDA sections plus a header section. For each section, the documentation provides a single paragraph paraphrased from HL7's official C-CDA documentation. No field names, data types, value sets, or vendor-specific mappings are provided.

| C-CDA Section | Documentation Depth |
|---|---|
| Allergies | 1 paragraph (paraphrased from HL7) |
| Immunizations | 1 paragraph |
| Medications | 1 paragraph |
| Plan of Treatment | 1 paragraph |
| Goals | 1 paragraph |
| Problem(s) | 1 paragraph |
| Results (Lab) | 2 paragraphs (most detailed section — mentions hematology, chemistry, serology, virology, toxicology, microbiology, imaging, pathology) |
| Vitals | 1 paragraph |
| Procedures | 1 paragraph |
| Social History | 1 paragraph |
| Encounters | 1 paragraph |
| Functional Status | 1 paragraph |
| Medical Equipment | 1 paragraph |
| Assessments | 1 paragraph |
| Header (demographics, author, timestamps) | XML snippet only |

The document explicitly defers to HL7's C-CDA specification: "If a user needs to know certain specifics about the syntactic language then we recommend going to the website above." No vendor-specific extensions, custom fields, or VistA-to-C-CDA mappings are described.

### CSV Supplement

The "Advanced Demographics and Remaining EHI" section describes a proprietary CSV format using name-value pairs. The entire specification consists of:

1. A statement that it exists
2. A single fictional example: `Place of Birth, USA, Mother's Maiden Name, Annabelle, Spouse's Employer Name, Astronaut LLC, Date of Retirement, 10/31/2023…(etc)`
3. A claim that "all available data will be present upon exportation"

**No field listing is provided.** The only concrete fields shown are 4 demographic items (Place of Birth, Mother's Maiden Name, Spouse's Employer Name, Date of Retirement). Whether the CSV includes billing data, clinical orders, consult records, or any non-demographic data is unstated.

### Vendor's own content organization

The vendor organizes content into two categories: C-CDA sections and "Advanced Demographics and Remaining EHI." Because no data dictionary exists, there are no entities, fields, or descriptions to enumerate:

| Category (vendor's) | Entities | Fields | Descriptions | Types |
|---|---|---|---|---|
| C-CDA Clinical Sections | 0 (section-level only) | 0 | 0 | No |
| Advanced Demographics / Remaining EHI (CSV) | 0 | 4 example fields shown | 0 | No |
| **Total** | **0** | **0** | **0** | **No** |

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor's documentation describes two components:

1. **C-CDA sections (14 sections)**: Standard clinical summary content — allergies, medications, problems, labs, vitals, immunizations, procedures, encounters, goals, plan of treatment, social history, functional status, medical equipment, and assessments. This is essentially what any C-CDA-compliant EHR would produce for transitions of care. The documentation provides no evidence of vendor-specific extensions or data beyond the C-CDA standard.

2. **CSV supplement ("remaining EHI")**: Claimed to cover everything not in the C-CDA, but the only example shows demographic fields. The scope is defined only by the vague promise that "all available data will be present upon exportation." Without a field listing or sample file, it is impossible to verify what this actually includes.

**The thinnest area** is the CSV supplement — it could theoretically contain hundreds of VistA FileMan fields, or it could contain only the 4 demographic fields shown in the example. The documentation provides zero evidence either way.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | C-CDA header + CSV example shows 4 demographic fields | C-CDA header covers basics; CSV claims "advanced demographics" but only shows 4 fields. Likely covered but unverifiable. |
| Encounters / visits | ⚠️ Partial | C-CDA "Encounters" section (1-paragraph description) | Product stores encounter data; C-CDA section exists but no field-level detail. |
| Problems / conditions / diagnoses | ⚠️ Partial | C-CDA "Problem(s)" section | C-CDA section described at paragraph level only. |
| Medications / prescriptions | ⚠️ Partial | C-CDA "Medications" section | Current medications via C-CDA. E-prescribing details (Newcrop/Surescripts transmission records, EPCS) not addressed. |
| Allergies | ⚠️ Partial | C-CDA "Allergies" section | C-CDA section described. |
| Immunizations | ⚠️ Partial | C-CDA "Immunizations" section | C-CDA section described. |
| Vitals | ⚠️ Partial | C-CDA "Vitals" section | C-CDA section described. |
| Lab results | ⚠️ Partial | C-CDA "Results (Lab)" section — most detailed, mentions multiple lab categories | Broad scope claimed (hematology, chemistry, imaging, pathology, etc.) but no field-level detail. |
| Imaging / diagnostic reports | ⚠️ Partial | Mentioned within "Results (Lab)" section | Imaging results mentioned as part of results; CPOE for imaging is certified (a)(3). |
| Procedures | ⚠️ Partial | C-CDA "Procedures" section | C-CDA section described. |
| Clinical notes / documents | ⚠️ Partial | C-CDA "Assessments" section; no mention of full TIU notes | Product uses VistA's TIU for extensive clinical documentation and "hundreds of templates." Only "Assessments" section is described in C-CDA — full progress notes, H&P, consult notes unclear. |
| Care plans / goals | ⚠️ Partial | C-CDA "Plan of Treatment" and "Goals" sections | C-CDA sections described. |
| Orders / referrals | ⚠️ Partial | C-CDA "Plan of Treatment" covers pending orders | Product has full CPOE (a)(1)–(a)(3); only prospective/pending orders mentioned. Historical completed orders unclear. |
| Insurance / coverage | ❌ Not covered | No insurance entities mentioned | Product likely stores insurance info for billing; not addressed in export documentation. |
| Claims / billing | ❌ Not covered | No billing entities mentioned | Product has "Rocket Note" for billing and employs billers; billing data not mentioned in export. |
| Payments | ❌ Not covered | No payment entities mentioned | If product handles billing, payment data likely exists; not mentioned. |
| Consents / directives | ❌ Not covered | No consent entities mentioned | No evidence in export. N/A if product doesn't store these. |
| Patient communications / portal messages | ❌ Not covered | No portal/messaging entities mentioned | Product is certified for (e)(3) patient access but no portal messaging described. Likely N/A. |
| Specialty-specific (Psychiatry) | ❌ Not covered | No psychiatry-specific entities mentioned | Developer is a psychiatrist running a psychiatry practice; product may store specialty assessments. Not addressed. |

**Summary**: All clinical domains get a "⚠️ Partial" rating because C-CDA sections are listed but with no field-level detail, no sample data, and no evidence of vendor-specific extensions. The C-CDA sections could be rich or could be bare-minimum — the documentation doesn't say. Billing, insurance, payments, and specialty data receive "❌ Not covered" because they are completely absent from the documentation.

## 6. Documentation Quality

**Can a developer build an import from this documentation?** No. The documentation provides:

- **For C-CDA**: Section names and 1-paragraph descriptions paraphrased from HL7's spec. A developer would need to independently study the HL7 C-CDA specification and then test against actual Astronaut export files (which are not provided) to determine what the vendor actually includes.
- **For CSV**: A single fictional example showing 4 demographic name-value pairs. A developer would have zero basis for parsing the CSV without an actual export file to reverse-engineer.

**What's missing**:
- No data dictionary (0 entities defined, 0 fields defined)
- No schema files (no XSD, JSON Schema, or any machine-readable artifact)
- No sample export files
- No value set or code system documentation
- No mapping between VistA's internal data model and the export output
- No field-level specifications of any kind

**Machine-readable artifacts**: None. The entire documentation is a 10-page PDF produced in Google Docs.

**Quality rating**: The documentation is a compliance stub. It establishes that an export exists and names the format (C-CDA + CSV) but provides no technical detail that would enable a recipient to understand, parse, or import the data.

## 7. Overall Assessment

### Classification

**Standard-based projection** — The export is primarily a C-CDA clinical summary with a vaguely defined CSV supplement. There is no evidence of a native database model export. The documentation describes standard C-CDA sections (the same content produced for transitions of care under (b)(1)) plus an undocumented CSV add-on. This is a C-CDA repackaging being called "(b)(10)" with a CSV safety valve whose actual contents are unverifiable.

### Key Findings

1. **The entire export documentation is a single 10-page PDF with no field-level detail.** Zero entities, zero fields, zero descriptions are defined. The document consists of section-level C-CDA descriptions paraphrased from HL7's website and a single fictional CSV example showing 4 demographic fields. (Source: `Astronaut-EHR-Export-Format-Documentation.pdf`)

2. **The C-CDA component is indistinguishable from a standard transitions-of-care document.** The 14 sections described are standard C-CDA sections that any (b)(1)-certified EHR would produce. No vendor-specific extensions, custom fields, or VistA-specific data elements are documented. (Source: PDF pages 5–9)

3. **The CSV "remaining EHI" supplement is effectively undocumented.** The only specification is a single example line with 4 demographic fields. Whether billing data, CPOE orders, clinical notes, or any non-demographic data is included cannot be determined. The vendor claims "all available data will be present" but provides no enumeration. (Source: PDF page 9)

4. **Billing and insurance data are completely absent from the documentation.** The product has billing capabilities ("Rocket Note," billers on staff) but the export documentation makes no mention of charges, claims, payments, or insurance records. (Source: product-research.md vs. PDF)

5. **Export requires IT staff involvement**, not self-service. An authorized user must be "granted permission by Astronaut EHR's IT staff" who "walk an end-user through the process." (Source: PDF page 3)

### Summary Stats

```
Classification:  Standard-based projection
Export format:   C-CDA (XML) + proprietary CSV
Model type:      Standard projection (C-CDA) with undocumented CSV supplement
Entities:        0 (no data dictionary)
Fields:          0 (no field-level documentation)
Descriptions:    N/A
Sample data:     No
Bulk export:     Yes (claimed)
Domains covered: 0 of 15 fully covered; 12 of 15 partially claimed via C-CDA section names
```

### Bottom Line

A patient or provider receiving this export would get a standard C-CDA clinical summary — the same document produced for any care transition — plus an undocumented CSV file of uncertain content. The documentation is too thin to verify what data is actually exported, and billing, insurance, and specialty clinical data are entirely unaddressed. The single biggest gap is the complete absence of a data dictionary or field-level documentation for either the C-CDA or CSV components, making it impossible to independently assess export completeness.
