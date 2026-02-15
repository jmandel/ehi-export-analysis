# EHI Export Analysis: GeniusDoc, Inc.

**Product**: GeniusDoc 12.0
**Analysis date**: 2026-02-15
**CHPL ID**: 15.02.05.1529.GDOC.01.01.1.211209 (CHPL Product ID 10745)

## 1. Product Context

GeniusDoc is a fully integrated ambulatory EHR, practice management, and revenue cycle management system developed by GeniusDoc, Inc. (Santa Monica, CA) in partnership with B2B Software Technologies Ltd (Hyderabad, India). The product's flagship specialty is **hematology/oncology**, with deep chemotherapy management features including regimen libraries, BSA/AUC/ANC dose calculations, cumulative dose tracking, TNM cancer staging, tumor marker tracking, and chemotherapy administration documentation. It also serves other ambulatory specialties.

Key data domains the product stores, based on vendor website documentation:

- **Clinical**: SOAP encounter notes, problem lists, medication lists, allergy lists, vital signs, immunizations, lab results, imaging orders, clinical decision support alerts, health maintenance
- **Oncology-specific**: Chemotherapy regimens, dose calculations, cancer staging, tumor markers, chemo administration records, oncology nurse assessments, treatment calendars
- **Prescribing**: E-prescribing via Surescripts, drug interaction screening, formulary data, complex prescription management (IV, sequenced)
- **Billing/RCM**: Charges, claims, CPT/ICD codes, E&M coding, modifiers, EOB data, remittance advice, payment posting, AR management, secondary claims
- **Documents**: Scanned documents, faxes, referral letters, diagnostic images, procedure photos, audio/video files
- **Care coordination**: CCM module, referrals, medication reconciliation, care plans
- **Patient portal**: Patient-facing health information access (certified for (e)(1)–(e)(3))
- **Quality reporting**: MIPS, PQRS, QOPI measures, clinical quality measures
- **Public health reporting**: Immunization registry, syndromic surveillance, cancer registry

This is a comprehensive ambulatory EHR with 42 certified criteria. The (b)(10) export should cover all patient-facing clinical, billing, oncology, prescribing, and document data the system stores.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/GeniusDoc_Data_Export.pdf` (159 KB, 2 pages — page 2 blank) | The complete EHI export documentation. A 1-page PDF listing 6 export categories with 1–2 sentence descriptions each. Created 2023-11-17 in Microsoft Word. Contains zero field names, zero data types, no schema, no sample data, and no export process instructions. | **Primary artifact** — the only documentation available |
| `product-research.md` | Prior research on GeniusDoc's capabilities, modules, and data domains. Used to establish what the export *should* cover. | Context — sets the baseline |
| `chpl-metadata.json` | CHPL certification details including 42 certified criteria and (b)(10) certification. | Context |
| `files.json` | Manifest confirming the PDF is the sole downloaded artifact. | Context |

**Verification performed**: Downloaded the PDF independently and confirmed its content via `pdftotext` and `pdfinfo`. Verified the vendor's API page (`API.php`) still states "There are currently no GeniusDoc customers integrated with the API." Verified the mandatory disclosures page shows product last modified 12/13/2024. All claims in this analysis are independently verified.

## 3. Export Mechanics

- **Format**: Excel (`.xlsx` or `.xls` — unspecified) for structured data; PDF and HL7 CDA for visit summaries; original file formats for scanned/imported documents
- **Mechanism**: Not documented. The PDF provides no instructions on how to request or perform an export. It is unclear whether this is a UI-driven self-service function, a vendor-assisted process, or something else entirely.
- **Single-patient vs bulk**: Not documented.
- **Access constraints or fees**: Not documented. The mandatory disclosures page (`ONC_Certification_Costs.php`) does not mention EHI export-specific costs.

The export documentation provides no operational detail — a user reading only this PDF would not know how to initiate an export.

## 4. Export Content: What's In It

The PDF describes 6 categories of data. There is **no data dictionary, no field definitions, no schema, no sample data, and no machine-readable artifacts** of any kind. The entirety of what is known comes from category-level prose descriptions:

### Vendor's own content organization

| Category (vendor's) | Export Format | Vendor Description (complete text) | Fields Documented |
|---|---|---|---|
| Demographics and Insurance | Excel | "comprehensive patient demographics and insurance details" | 0 |
| Medications and Allergies | Excel | "patient medications and allergies details" | 0 |
| Problems | Excel | "the active patient diagnosis" | 0 |
| Lab Results | Excel | "structured patient lab results" | 0 |
| Visit Summaries | PDF + CDA + Excel reference | "all the details of each encounter" | 0 |
| Documents | Original formats + Excel reference | "all the scanned or imported documents in the patient chart" | 0 |

**Total categories**: 6
**Total fields documented**: 0
**Total entities/tables documented**: 0
**Data dictionary**: None
**Sample data**: None
**Schema**: None

Notable: The "Problems" category explicitly states it contains "the active patient diagnosis" — this excludes resolved or historical diagnoses, which is a scope limitation even within the narrow set of data described.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor's documentation describes 6 broad categories that correspond roughly to a clinical summary: demographics, insurance, current medications, allergies, active problems, lab results, visit summaries, and scanned documents. This is essentially the USCDI v1 data class set — the same content available through a C-CDA or FHIR US Core export — plus document attachments.

The 6 categories are described at the highest possible level of abstraction. There is no way to assess depth because no field-level information exists. The vendor provides no evidence of what "comprehensive patient demographics" actually includes — it could be 5 fields or 50 fields.

The export makes no mention of the product's two most significant data domains: **oncology/chemotherapy data** (the product's differentiating feature) and **billing/RCM data** (a major integrated module).

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | "Demographics and Insurance" category mentioned; no fields documented | Claimed but unverifiable — zero field detail |
| Encounters / visits | ⚠️ Partial | "Visit Summaries" in PDF + CDA format | Format described but content unknown; CDA profile unspecified |
| Problems / conditions | ⚠️ Partial | "Problems" category — explicitly "active patient diagnosis" only | Excludes resolved/historical diagnoses; significant scope limitation |
| Medications / prescriptions | ⚠️ Partial | "Medications and Allergies" category mentioned | Current medication list only; no prescribing history, e-prescribing transactions, or drug interaction records |
| Allergies | ⚠️ Partial | "Medications and Allergies" category mentioned | Claimed but no field detail |
| Immunizations | ❌ Not covered | Not mentioned in export documentation | Product is certified for immunization registry reporting (f)(1) and stores immunization records; gap |
| Vitals | ❌ Not covered | Not mentioned (may be embedded in visit summaries but not documented) | Product stores vital signs; gap unless included in CDA visit summaries |
| Lab results | ⚠️ Partial | "Lab Results" category in Excel | Claimed but no field detail; unclear if includes all lab data or just results |
| Imaging / diagnostic reports | ❌ Not covered | Not mentioned | Product has imaging orders/results; gap |
| Procedures | ❌ Not covered | Not mentioned | Product documents procedures; gap |
| Clinical notes / documents | ⚠️ Partial | "Visit Summaries" (PDF/CDA) + "Documents" (scanned/imported) | Visit summaries may contain notes; scanned documents exported; but no detail on what's included |
| Care plans / goals | ❌ Not covered | Not mentioned | Product has CCM module and care plans; gap |
| Orders / referrals | ❌ Not covered | Not mentioned | Product has CPOE and referral capabilities; gap |
| Insurance / coverage | ⚠️ Partial | "Demographics and Insurance" category | Claimed but no field detail |
| Claims / billing | ❌ Not covered | Not mentioned | Product has full integrated billing/RCM; **major gap** |
| Payments | ❌ Not covered | Not mentioned | Product processes payments, EOBs, remittances; **major gap** |
| Consents / directives | ❌ Not covered | Not mentioned | Unknown if product stores these |
| Patient communications | ❌ Not covered | Not mentioned | Communications via Updox integration; may be external |
| Specialty — oncology/hematology | ❌ Not covered | Not mentioned | Product's flagship specialty: chemo regimens, dose tracking, cancer staging, tumor markers, chemo administration — **none mentioned**. This is the single largest gap. |

**Summary**: Of 19 assessed domains, 0 are fully covered, 7 are partially covered (claimed at category level but with zero field detail), and 10 are not covered at all. Among the uncovered domains, at least 7 represent data that GeniusDoc demonstrably stores (oncology, billing, payments, immunizations, vitals, orders, care plans).

## 6. Documentation Quality

The export documentation is **extraordinarily thin** — among the thinnest possible while technically existing as a published artifact:

- **No data dictionary**: Zero field names, column headings, or data types are documented anywhere
- **No schema**: No description of what the Excel files contain, what columns exist, or how data is structured
- **No sample data**: No example files, records, or screenshots
- **No export instructions**: No description of how to request, initiate, or configure an export
- **No relationships**: No description of how exported files relate to each other
- **No value sets**: No coding systems, terminologies, or enumerated values documented
- **No machine-readable artifacts**: No JSON schema, XSD, CSV header documentation, or any parseable format specification

A developer receiving an export produced by this system would have **zero documentation** to work from. They would need to reverse-engineer every Excel file's column meanings, infer data types, guess at coded values, and hope the data is self-documenting.

The CDA format for visit summaries references "HL7 CDA standards" but does not specify a profile (e.g., C-CDA R2.1, CCD, CDA R2). This could mean anything from a minimal CDA header to a full Continuity of Care Document.

The entire substantive content of the documentation is approximately 200 words — less than a typical email.

## 7. Overall Assessment

### Classification

**Minimal/stub**: The documentation is a 1-page PDF with 6 category names and no field-level detail. There is no data dictionary, no schema, no sample data, and no evidence that the export covers more than a basic clinical summary. The export documentation appears to be a compliance checkbox — the minimum conceivable effort to have a publicly accessible URL that references 170.315(b)(10).

### Key Findings

1. **Zero field-level documentation**: The entire EHI export is described in ~200 words across 6 categories. Not a single field name, data type, or column heading is documented. This is among the thinnest EHI export documentation of any certified product. (Source: `GeniusDoc_Data_Export.pdf`, verified via `pdftotext`)

2. **Flagship oncology data completely absent**: GeniusDoc's primary differentiator is deep hematology/oncology capabilities — chemotherapy regimen management, dose tracking, cancer staging, tumor markers, chemo administration records. None of this data is mentioned in the export documentation. (Source: `GeniusDoc_Data_Export.pdf` lists no oncology categories; `product-research.md` documents extensive oncology features)

3. **Billing/RCM data completely absent**: The product includes fully integrated billing, claims processing, payment posting, and revenue cycle management. None of this data is mentioned in the export. (Source: `GeniusDoc_Data_Export.pdf`; `product-research.md` documents comprehensive billing capabilities)

4. **Export resembles a clinical summary, not an EHI export**: The 6 documented categories (demographics, insurance, medications, allergies, problems, labs, visit summaries, documents) correspond closely to USCDI v1 / C-CDA content — the same data available through a patient portal or standard clinical summary. This suggests the vendor may be repackaging existing clinical summary functionality as their (b)(10) export.

5. **"Active diagnosis" limitation**: The Problems category explicitly exports only "the active patient diagnosis," excluding resolved or historical diagnoses that are part of the electronic health record. (Source: `GeniusDoc_Data_Export.pdf`, category 3)

### Summary Stats

```
Classification:  Minimal/stub
Export format:   Excel + PDF + CDA (unspecified profile)
Model type:      Unknown — no field-level detail to assess
Entities:        6 categories (no entity/table documentation)
Fields:          0 documented
Descriptions:    N/A (0 fields to describe)
Sample data:     No
Bulk export:     Unclear
Domains covered: 0 of 14 applicable domains fully covered; 7 partially claimed at category level
```

### Bottom Line

GeniusDoc's EHI export documentation is a 1-page PDF with 6 category names and zero technical detail. A patient or provider requesting their data would receive files with no documentation explaining their contents, and the export appears to omit the product's most important data domains — oncology/chemotherapy data and billing records. This is a compliance stub, not a genuine effort to support electronic health information export.
