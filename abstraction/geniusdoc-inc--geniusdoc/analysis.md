# EHI Export Analysis: GeniusDoc, Inc.

**Product**: GeniusDoc 12.0
**Analysis date**: 2026-02-15
**CHPL IDs**: 15.02.05.1529.GDOC.01.01.1.211209

## 1. Product Context

GeniusDoc is a fully integrated ambulatory EHR, practice management, and revenue cycle management system developed by GeniusDoc, Inc. (Santa Monica, CA) in partnership with B2B Software Technologies Ltd (Hyderabad, India). Its flagship specialty is **hematology/oncology**, with deep chemotherapy management capabilities including regimen libraries, BSA/AUC/ANC dose calculations, cumulative dose tracking, TNM cancer staging, and tumor marker tracking. The product targets small-to-midsize physician practices.

Beyond oncology, GeniusDoc stores and manages:
- **Clinical data**: SOAP-formatted encounters, problem lists, medication lists, allergy lists, vital signs, immunizations, lab results, imaging orders, clinical notes, care plans
- **Prescribing**: E-prescribing via Surescripts with drug interaction screening, formulary checks
- **Billing/RCM**: Charges, claims, CPT/ICD codes, E&M coding, EOBs, remittance advice, payment posting, accounts receivable
- **Documents**: Scanned documents, faxes, diagnostic images, procedure photos, audio/video files
- **Scheduling**: Appointments, treatment calendars, wave scheduling for chemo
- **Patient portal**: Patient access to health information (certified for (e)(1)-(e)(3))
- **Quality/reporting**: MIPS, PQRS, QOPI measures; immunization registry; cancer registry reporting

The product is certified for 42 ONC criteria including (b)(10) EHI export. This certification breadth sets a high bar for what a complete EHI export should cover.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/GeniusDoc_Data_Export.pdf` | 2-page PDF (page 2 blank); 1 page of content listing 6 export categories with one-sentence descriptions each. Created 2023-11-17 in Microsoft Word. 159 KB. No data dictionary, no field definitions, no schema, no sample data. | **Primary artifact** — extremely thin |
| `product-research.md` | Detailed product research identifying GeniusDoc's modules and data domains | Useful for baseline |
| `chpl-metadata.json` | CHPL certification details — 42 certified criteria | Confirms certification scope |
| `ehi-export-report.md` | Prior agent's analysis of export documentation | Orientation only |
| `https://www.geniusdoc.com/API.php` (live) | FHIR API page — states "There are currently no GeniusDoc customers integrated with the API" | Confirmed live; confirms FHIR API is separate and unused |
| `https://www.geniusdoc.com/ONC_Certification_Costs.php` (live) | Mandatory disclosures — no EHI export details; confirms product last modified 12/13/2024 | No export info |

Only one artifact contains EHI export documentation: a single PDF with 1 page of content and zero field-level detail.

## 3. Export Mechanics

- **Format**: Excel (.xls/.xlsx) for structured data; PDF and CDA (HL7) for visit summaries; original file formats for scanned/imported documents
- **Mechanism**: Not documented. No description of how to initiate an export, whether it's self-service or vendor-assisted, or what parameters are available
- **Single-patient vs bulk**: Not documented
- **Access constraints or fees**: Not documented. The mandatory disclosures page (`ONC_Certification_Costs.php`) does not mention EHI export costs
- **Delivery**: The PDF mentions "reliable encryption standards and safe transmission techniques" but provides no specifics

The export process is effectively opaque — no user-facing instructions exist in the documentation.

## 4. Export Content: What's In It

The entire export documentation consists of 6 category descriptions on a single page. There is **no data dictionary** — not a single field name, column heading, or data type is documented anywhere. There are no schemas, no sample data files, no relationships between exported files, and no documentation of what columns the Excel files contain.

### Vendor's own content organization

The vendor describes exactly 6 export categories:

| Category (vendor's) | Format | Description (verbatim from PDF) | Fields Documented | Types | Relationships |
|---|---|---|---|---|---|
| Demographics and Insurance | Excel | "comprehensive patient demographics and insurance details" | 0 | No | No |
| Medications and Allergies | Excel | "patient medications and allergies details" | 0 | No | No |
| Problems | Excel | "the active patient diagnosis" | 0 | No | No |
| Lab Results | Excel | "structured patient lab results" | 0 | No | No |
| Visit Summaries | PDF, CDA, Excel (index) | "all the details of each encounter" | 0 | No | No |
| Documents | Original formats, Excel (index) | "all the scanned or imported documents in the patient chart" | 0 | No | No |

**Total entities/tables documented: 6 categories (not tables — no table-level detail exists)**
**Total fields documented: 0**
**Fields with descriptions: 0**
**Fields with types: 0**

Notable observations:
- The "Problems" category explicitly says it contains only "the active patient diagnosis" — resolved and historical diagnoses appear to be excluded
- The "Visit Summaries" category mentions CDA format but specifies no CDA template, profile, or version (just "as per HL7 CDA standards")
- No category addresses chemotherapy/oncology data, billing, prescriptions, vitals, immunizations, orders, care plans, or scheduling

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor's 6 export categories correspond roughly to the core data classes in a USCDI/C-CDA clinical summary: demographics, medications, allergies, problems, labs, encounter notes, and documents. This is the data you would expect from a patient summary exchange — not from a comprehensive EHI export.

The categories are described at a high level with no field detail. There is no way to assess depth within any category because no fields, columns, or schemas are documented. For example, "comprehensive patient demographics and insurance details" could mean 10 fields or 100 fields — the documentation provides no way to tell.

The most striking absence is **oncology/chemotherapy data** — GeniusDoc's signature specialty. None of the 6 export categories mention chemo regimens, dose tracking, cancer staging, tumor markers, or any oncology-specific data. For an EHR whose primary differentiator is hematology/oncology workflows, this is the most significant gap.

Billing data is also entirely absent. GeniusDoc has a full revenue cycle management module with charges, claims, EOBs, remittance advice, and payment posting — none of which appears in the export.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | Category 1: "comprehensive patient demographics" — but no field detail to verify | Mentioned but impossible to assess depth; no fields documented |
| Encounters / visits | ⚠️ Partial | Category 5: visit summaries in PDF/CDA format | Likely clinical summaries only; no structured encounter data fields |
| Problems / conditions / diagnoses | ⚠️ Partial | Category 3: "active patient diagnosis" only | Only active diagnoses; resolved/historical explicitly excluded by wording. Product stores full problem history. **Gap.** |
| Medications / prescriptions | ⚠️ Partial | Category 2: "patient medications" | Medication list mentioned but e-prescribing history, drug interaction logs, formulary data not mentioned. Likely current med list only. |
| Allergies | ⚠️ Partial | Category 2: "allergies details" | Mentioned but no field detail |
| Immunizations | ❌ Not covered | No mention in any export category | Product is certified for immunization management (h)(1) and stores immunization records. **Gap.** |
| Vitals | ❌ Not covered | No mention in any export category | Product stores vital signs. May be embedded in visit summaries but not documented. **Likely gap.** |
| Lab results | ⚠️ Partial | Category 4: "structured patient lab results" in Excel | Mentioned but no field detail; unknown whether discrete results or just report text |
| Imaging / diagnostic reports | ❌ Not covered | No mention in any export category | Product stores imaging orders and results. **Gap.** |
| Procedures | ❌ Not covered | No mention in any export category | Product stores procedure data. **Gap.** |
| Clinical notes / documents | ⚠️ Partial | Category 5 (visit summaries) + Category 6 (scanned/imported documents) | Visit summaries as PDF/CDA; scanned docs included. But no structured note data. |
| Care plans / goals | ❌ Not covered | No mention in any export category | Product has CCM module and care coordination. **Gap.** |
| Orders / referrals | ❌ Not covered | No mention in any export category | Product has CPOE for orders. **Gap.** |
| Insurance / coverage | ⚠️ Partial | Category 1 includes "insurance details" | Mentioned alongside demographics but no detail |
| Claims / billing | ❌ Not covered | No mention in any export category | Product has full RCM: charges, claims, EOBs, remittance, payments. **Significant gap.** |
| Payments | ❌ Not covered | No mention in any export category | Product tracks payments, adjustments, A/R. **Gap.** |
| Consents / directives | ❌ Not covered | No mention in any export category | N/A — unclear if product stores these |
| Patient communications / portal messages | ❌ Not covered | No mention in any export category | Patient portal is certified; messaging via Updox integration. **Likely gap** if messages stored in GeniusDoc. |
| Specialty-specific (hematology/oncology) | ❌ Not covered | No mention in any export category | Product's flagship feature: chemo regimens, dose tracking, BSA/AUC/ANC calculations, cancer staging (TNM), tumor markers, chemo administration records, oncology nursing assessments. **Most significant gap.** |

**Summary**: Of ~17 applicable domains, 0 are fully covered, 6 have partial/unverifiable mentions, and 11 are entirely absent from the export documentation. The partial coverage cannot be verified because no field-level detail exists.

## 6. Documentation Quality

The documentation quality is **near-zero**. The entire EHI export documentation is a single page of text with 6 one-sentence category descriptions.

**What's absent:**
- No data dictionary (zero fields documented)
- No field names, types, or descriptions
- No schema or structure definition for any export file
- No sample data or example files
- No export process instructions (how to request, who can initiate, what parameters)
- No relationship documentation between exported files
- No value sets, coding systems, or terminology references
- No versioning or change history
- No CDA template or profile specification

**Could a developer build an import from this documentation?** No. A developer would have no idea what columns the Excel files contain, what the CDA documents look like, how files relate to each other, or what coding systems are used. They would need to receive an actual export and reverse-engineer the structure.

**Machine-readable artifacts**: None. The documentation is a single PDF with prose text only.

The PDF was created 2023-11-17 (author field: "exotic") using Microsoft Word. It reads as a minimal compliance artifact — the absolute minimum to have a URL that references (b)(10).

## 7. Overall Assessment

### Classification

**Minimal/stub**: The documentation is too thin to assess what's actually exported. Only 6 broad categories are named with no field-level detail. Major data domains the product stores (oncology, billing, immunizations, vitals, orders, care plans) are entirely absent. The described export covers roughly the same scope as a C-CDA clinical summary — core USCDI data classes — which is far less than "all electronic health information."

### Key Findings

1. **Zero field-level documentation**: Across all 6 export categories, not a single field name, column heading, or data type is documented. The entire export specification fits in ~200 words of prose. (`GeniusDoc_Data_Export.pdf`, page 1)

2. **Oncology data entirely missing**: GeniusDoc's flagship hematology/oncology module — chemotherapy regimens, dose calculations, cancer staging, tumor markers, chemo administration records — is not mentioned anywhere in the export. This is the product's primary differentiator and represents a critical coverage gap.

3. **Billing/RCM data entirely missing**: Despite having a full revenue cycle management module (charges, claims, EOBs, remittance, payments, A/R), no billing data appears in the export documentation.

4. **Export resembles a clinical summary, not an EHI export**: The 6 categories (demographics, insurance, medications, allergies, problems, labs, visit summaries, documents) closely mirror the data classes in a C-CDA patient summary. This suggests the (b)(10) export may be a repackaging of existing clinical summary capabilities rather than a genuine "all EHI" export.

5. **Problems limited to active diagnoses**: The documentation explicitly states problems contain only "the active patient diagnosis," excluding resolved and historical diagnoses that are part of the patient's electronic health information.

### Summary Stats

```
Classification:  Minimal/stub
Export format:   Excel, PDF, CDA (HL7)
Model type:      Unknown — no schema or structure documented
Entities:        6 categories described (no table/entity-level detail)
Fields:          0 documented
Descriptions:    N/A (no fields to describe)
Sample data:     No
Bulk export:     Unclear
Domains covered: 0 of ~17 fully covered; 6 partially mentioned without field detail
```

### Bottom Line

GeniusDoc's EHI export documentation is a single page naming 6 broad data categories with zero field-level detail, no schema, and no sample data. The export omits the product's most important data domains — hematology/oncology treatment data and billing/RCM data — and provides only category-level mentions of core clinical data. A patient or provider receiving this export would get an undocumented collection of Excel files and PDFs covering roughly what a C-CDA summary provides, with no way to understand the structure and no access to specialty clinical data or financial records.
