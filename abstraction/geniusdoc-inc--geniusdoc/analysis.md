# EHI Export Analysis: GeniusDoc, Inc.

**Product**: GeniusDoc 12.0
**Analysis date**: 2026-02-16
**CHPL IDs**: 15.02.05.1529.GDOC.01.01.1.211209 (CHPL ID 10745)

## 1. Product Context

GeniusDoc is a fully integrated ambulatory EHR, practice management, and revenue cycle management system developed by GeniusDoc, Inc. (Santa Monica, CA) in partnership with B2B Software Technologies Ltd (Hyderabad, India). The product's flagship specialty is **hematology/oncology**, with deep chemotherapy management capabilities including regimen libraries, BSA/AUC/ANC dose calculations, cumulative dose tracking, TNM cancer staging, tumor marker tracking, and oncology nurse documentation.

Beyond oncology, GeniusDoc provides comprehensive clinical documentation (SOAP notes, encounter management), CPOE/order entry, lab integration, e-prescribing (Surescripts), immunization tracking, vital signs, and document management (scanned documents, faxes, images, audio/video). The product has a full **billing and revenue cycle management** module including charge posting, claims generation/submission, CPT/ICD coding, EOB processing, remittance advice, payment posting, and secondary claims. It also includes scheduling, a patient portal, care coordination (CCM), and quality reporting (MIPS, QOPI).

The product is certified across 42 ONC criteria including (b)(10) EHI export, (g)(10) FHIR API, and multiple clinical, care coordination, and public health reporting criteria. It runs on Windows Server/SQL Server architecture. The vendor appears to be a small niche player with a limited install base.

**Baseline expectation**: A comprehensive (b)(10) export from this product should cover clinical documentation, oncology-specific data, prescribing, billing/RCM, labs, orders, vitals, immunizations, documents, and insurance — at minimum.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/GeniusDoc_Data_Export.pdf` (159 KB, 2 pages — page 2 blank) | The sole EHI export documentation artifact. A 1-page PDF listing 6 export categories with one-sentence descriptions each. Created Nov 17, 2023 in Microsoft Word. No data dictionary, no field definitions, no schema, no sample data. | **Primary and only artifact.** Extremely thin. |

No other artifacts exist. There is no data dictionary, no schema file, no sample export data, no supplemental documentation. The single PDF is the entirety of the vendor's publicly available (b)(10) documentation.

## 3. Export Mechanics

- **Format**: Excel (XLSX) for structured data (demographics, insurance, meds, allergies, problems, labs); PDF and CDA (HL7 CDA) for visit summaries; original file formats for scanned/imported documents; Excel for reference/index files
- **Mechanism**: Not documented. The PDF does not describe how to initiate an export — no mention of a UI button, API endpoint, admin console, or vendor-mediated process
- **Single-patient vs bulk**: Not documented
- **Access constraints or fees**: Not documented. The PDF mentions encryption and "safe transmission techniques" but provides no operational detail
- **Timeliness**: Not documented

## 4. Export Content: What's In It

The PDF describes 6 categories of export data. There is **zero field-level documentation** — no column names, no data types, no value sets, no relationships, no schema. The documentation is purely categorical.

### Vendor's own content organization

| Entity/Category | Fields | Described | Types | Category (vendor's) | Format |
|---|---|---|---|---|---|
| Demographics and Insurance | 0 (undocumented) | N/A | N/A | Demographics / Insurance | Excel |
| Medications and Allergies | 0 (undocumented) | N/A | N/A | Clinical | Excel |
| Problems | 0 (undocumented) | N/A | N/A | Clinical | Excel |
| Lab Results | 0 (undocumented) | N/A | N/A | Clinical | Excel |
| Visit Summaries | 0 (undocumented) | N/A | N/A | Clinical | PDF, CDA, Excel (index) |
| Documents | 0 (undocumented) | N/A | N/A | Documents | Original formats, Excel (index) |

**Total documented entities: 6 categories**
**Total documented fields: 0** — not a single field name, column heading, or data type is specified anywhere.

The only substantive detail beyond category names:
- **Problems** is explicitly limited to "the active patient diagnosis" — resolved and historical diagnoses appear to be excluded
- **Visit Summaries** use CDA format described as "per HL7 CDA standards" — no CDA template, profile, or section list is specified
- **Documents** include "all scanned or imported documents" with an index file containing "document index, file information, folder names and patient details"

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor describes 6 export categories that map to basic clinical summary data:

1. **Demographics and Insurance** — the broadest-sounding category, but with zero detail on what "comprehensive" means
2. **Medications and Allergies** — combined into one file, no distinction between active/historical medications or medication administration records
3. **Problems** — explicitly limited to active diagnoses only, excluding historical/resolved
4. **Lab Results** — "structured" results, no detail on whether this includes order information, specimen data, or just final results
5. **Visit Summaries** — the only multi-format category (PDF + CDA + Excel index); claims to contain "all the details of each encounter" but no enumeration of what those details are
6. **Documents** — scanned/imported documents with an index; this is the one area where the export may be reasonably complete since it's file-based

These 6 categories correspond closely to a standard **C-CDA patient summary** (demographics, medications, allergies, problems, labs, encounters, documents). This is essentially the USCDI data surface repackaged in Excel/CDA format.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | "Demographics and Insurance" category — no field detail | Product stores demographics; mentioned but undocumented |
| Encounters / visits | ⚠️ Partial | "Visit Summaries" in PDF/CDA format | Encounters mentioned but no detail on what's included beyond "all details" |
| Problems / conditions | ⚠️ Partial | "Problems" — explicitly active only | Product stores full problem history; active-only is a gap |
| Medications / prescriptions | ⚠️ Partial | "Medications and Allergies" category | Product has full e-prescribing; export detail unknown |
| Allergies | ⚠️ Partial | "Medications and Allergies" category | Mentioned but no field detail |
| Immunizations | ❌ Not covered | Not mentioned | Product tracks immunizations and submits to registries; gap |
| Vitals | ❌ Not covered | Not mentioned as discrete data | Product records vitals; may be in visit summaries but undocumented |
| Lab results | ⚠️ Partial | "Lab Results" category | Mentioned but no field detail |
| Imaging / diagnostic reports | ❌ Not covered | Not mentioned | Product has imaging orders/results; gap |
| Procedures | ❌ Not covered | Not mentioned | Product documents procedures; gap |
| Clinical notes / documents | ⚠️ Partial | "Visit Summaries" + "Documents" | Visit summaries in CDA/PDF; scanned documents included; but no detail on note types covered |
| Care plans / goals | ❌ Not covered | Not mentioned | Product has CCM module and care coordination; gap |
| Orders / referrals | ❌ Not covered | Not mentioned | Product has CPOE and referral workflows; gap |
| Insurance / coverage | ⚠️ Partial | "Demographics and Insurance" category | Mentioned but no field detail on depth of insurance data |
| Claims / billing | ❌ Not covered | Not mentioned | Product has full RCM — charges, claims, CPT/ICD, EOBs, payments; **major gap** |
| Payments | ❌ Not covered | Not mentioned | Product processes payments, remittance advice; gap |
| Consents / directives | ❌ Not covered | Not mentioned | Unknown if product stores these |
| Patient communications | ❌ Not covered | Not mentioned | Updox integration handles messaging; may not be in GeniusDoc's data |
| Specialty — Oncology | ❌ Not covered | Not mentioned | **Product's flagship feature.** Chemo regimens, dose tracking, cancer staging, tumor markers, administration records — none mentioned. **Most significant gap.** |

**Summary**: Of approximately 15 applicable domains for this product, 8 are not covered at all, 6 are partially mentioned (category-level only, no field detail), and 1 (oncology) is the product's defining specialty yet entirely absent from the export documentation.

## 6. Documentation Quality

The documentation is **among the thinnest possible** while technically existing:

- **No data dictionary**: Not a single field name, column heading, or data type is documented anywhere
- **No schema or structure definition**: No description of what the Excel columns are or what CDA sections are included
- **No sample data**: No example files, records, or screenshots
- **No export instructions**: No description of how to request or initiate an export
- **No relationships**: No description of how the 6 exported files relate to each other
- **No value sets or coding systems**: No mention of what code systems are used (ICD-10, SNOMED, RxNorm, etc.)
- **No versioning**: No version number, no changelog (PDF created Nov 2023 with no revision history)
- **No machine-readable artifacts**: Everything is in a single PDF

A developer receiving an export based on this documentation would need to reverse-engineer every Excel file to understand its structure. Import into another system would be impossible without examining actual export data. The documentation does not meet a reasonable standard for interoperability.

The PDF is 1 page of actual content (page 2 is blank). It reads as a minimal compliance artifact — the least possible effort to have a publicly accessible URL that references 170.315(b)(10).

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Minimal/stub/unclear**

The documentation describes only 6 high-level categories corresponding to standard clinical summary domains (demographics, meds, allergies, problems, labs, encounters, documents). With zero field-level documentation, it is impossible to assess actual export depth. However, the category-level description alone reveals critical gaps: the product's flagship oncology capabilities (chemotherapy management, cancer staging, tumor markers, dose tracking) are entirely absent; the full billing/RCM module (charges, claims, payments, EOBs) is absent; immunizations, vitals, orders, procedures, imaging, and care plans are absent. The Problems category explicitly exports only "active" diagnoses, excluding historical/resolved conditions. Even taking the categories at face value, this covers roughly the USCDI clinical summary surface — far less than the designated record set for a product with this breadth of functionality.

**Axis 2 — Export approach: Repackaged existing export**

The 6 export categories map almost exactly to a standard C-CDA patient summary: demographics, medications, allergies, problems, labs, encounters, and documents. The visit summaries are exported in CDA format "per HL7 CDA standards." This is consistent with the vendor repackaging their existing clinical exchange / (g)(10) export as their (b)(10) compliance. There is no evidence of a purpose-built EHI export — no native database tables, no product-specific data model, no coverage of billing or specialty data, no data dictionary reflecting the product's internal schema. The export surface matches what would be available through standard clinical exchange, not a designated record set export.

### Key Findings

1. **Oncology data entirely absent**: GeniusDoc's core differentiator — chemotherapy management, cancer staging, tumor markers, dose tracking, oncology nurse documentation — is not mentioned anywhere in the export documentation. For an oncology-focused EHR, this is the most significant gap. (`GeniusDoc_Data_Export.pdf` — no mention of chemotherapy, oncology, staging, tumor, or regimen)

2. **Billing/RCM data entirely absent**: Despite having a full revenue cycle management module (charges, claims, CPT/ICD coding, EOBs, remittance advice, payment posting), no billing data is included in the export. (`GeniusDoc_Data_Export.pdf` — no billing, claims, charges, or payment categories)

3. **Zero field-level documentation**: Across all 6 export categories, not a single field name, column heading, data type, or value set is documented. The entire documentation is 6 one-sentence category descriptions. (`GeniusDoc_Data_Export.pdf` — 1 page, 6 categories, 0 fields)

4. **Active problems only**: The Problems category explicitly states it exports "the active patient diagnosis," excluding resolved and historical diagnoses that are part of the designated record set. (`GeniusDoc_Data_Export.pdf`, category 3)

5. **No export process documentation**: There are no instructions on how to initiate, request, or receive an export — no UI description, no API endpoint, no timeline, no delivery mechanism. (`GeniusDoc_Data_Export.pdf` — no operational detail)

### Summary Stats

```
Coverage:        Minimal/stub/unclear
Approach:        Repackaged existing export
Export format:   Excel (XLSX), PDF, CDA (HL7), original document formats
Entities:        6 categories (no entity/table-level breakdown)
Fields:          0 documented
Descriptions:    N/A (0 fields documented)
Sample data:     No
Bulk export:     Unclear
Domains covered: ~6 of 15 applicable domains (all partial — category-level only)
```

### Bottom Line

GeniusDoc's (b)(10) documentation is a single 1-page PDF listing 6 export categories with no field-level detail, no data dictionary, no schema, and no sample data. A patient or provider would receive an export covering basic clinical summary data but with no documentation to interpret it, no oncology-specific data despite this being an oncology-focused EHR, and no billing/RCM data despite the product having full revenue cycle management. This is one of the thinnest (b)(10) implementations reviewed — a compliance stub rather than a genuine EHI export effort.
