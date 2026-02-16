# EHI Export Analysis: Objective Medical Systems, LLC

**Product**: OMS EHR  
**Analysis date**: 2026-02-15  
**CHPL ID**: 15.04.04.2086.OMSE.06.07.1.260108

## 1. Product Context

OMS EHR is a cardiology-specific electronic health record system built by Objective Medical Systems, LLC (Houma, LA). The product is designed "by cardiologists, for cardiologists" and serves outpatient cardiovascular practices. Key capabilities include:

- **EHR**: Cardiology-specific clinical documentation with highly customizable templates. The vendor claims 1,000+ discrete data elements captured per patient chart (source: [EHR product page](https://objectivemedicalsystems.com/solution/care-delivery/ehr/)).
- **Diagnostic Reporting (OMS Diagnostics®)**: Structured reporting across 17 cardiovascular diagnostic modalities including echocardiograms, myocardial perfusion imaging, PET scans, and more. The vendor claims 4,500+ discrete data elements captured per patient (source: [Diagnostics product page](https://objectivemedicalsystems.com/solution/care-delivery/diagnostic-reporting/)).
- **Chronic Care Coordinator (C3)**: Remote patient monitoring (RPM), chronic care management (CCM), and principal care management (PCM) with built-in audio/video calls, texting, and automatic time tracking.
- **Clinical Decision Support**: Real-time alerts for clinical trial enrollment, diagnosis detection, and remote patient monitoring.
- **e-Prescribing**: Electronic prescriptions via Surescripts® integration.
- **Charge Capture / Billing Integration**: Partnership with White Plume Technologies for charge capture (per press releases). The disclosures page references ICD-9/ICD-10 and CPT codes for "identifying diagnosis and procedure codes."
- **CPOE**: Computerized provider order entry for medications.
- **Lab Integration**: Ordering and receiving lab results.
- **Smart Forms**: Custom clinical forms within the EHR.
- **Patient Messaging**: Internal messaging system.

The product is certified for 38 ONC criteria including 170.315(b)(10) (EHI Export). The intended user description is "Medical/Cardiology." Given the depth of cardiovascular data capture (the vendor's own claim of 4,500+ discrete data elements per patient for diagnostics alone), a complete EHI export should cover demographics, encounters, problems, medications, allergies, labs, cardiovascular diagnostic reports (echo, stress, cath, etc.), clinical notes, care plans, prescriptions, orders, messages, and any billing/charge data the system stores.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `EHI-Export-Data-Format.pdf` (2 pages, 133 KB) | The sole export documentation artifact. Page 1 is a title page; page 2 contains a 9-row table listing export "functions" and their document type formats. No field-level detail. | **Primary artifact** but extremely thin |
| `chpl-metadata.json` (2 KB) | CHPL certification details including certified criteria, developer contact, and the source URL for the EHI export documentation PDF. | Useful for context |
| OMS website — [disclosures page](https://objectivemedicalsystems.com/disclosures/) | Mandatory disclosures listing certified capabilities, fees, and technical prerequisites. No additional EHI export documentation found. | Confirms product capabilities |
| OMS website — [EHR product page](https://objectivemedicalsystems.com/solution/care-delivery/ehr/) | Marketing page describing 1,000+ discrete data elements per patient. | Establishes baseline for what should be exported |
| OMS website — [Diagnostics product page](https://objectivemedicalsystems.com/solution/care-delivery/diagnostic-reporting/) | Marketing page describing 4,500+ discrete data elements, 17 cardiovascular modalities. | Establishes baseline for diagnostics scope |
| OMS website — [C3 product page](https://objectivemedicalsystems.com/solution/care-delivery/chronic-care-coordinator-c3/) | Describes RPM/CCM/PCM programs with time tracking and billing. | Establishes additional data domains |

No data dictionary, schema, sample export data, or additional documentation artifacts were found. The `downloads/` folder was empty at the start of analysis; the PDF was downloaded directly from the URL in `chpl-metadata.json`.

## 3. Export Mechanics

- **Format(s)**: Mixed document-oriented formats — XML, HTML, PDF, and "discrete fields" (format unspecified). The CCDA and Labs are exported as XML and HTML. Notes and Smart Forms are exported as HTML. Scanned items are exported as PDF. Diagnostics and Messages are exported as "discrete fields" with no further specification of what format those discrete fields take.
- **Mechanism**: Not documented. The PDF does not describe how a user initiates the export (UI button, API call, request to vendor, etc.).
- **Single-patient vs bulk**: Not documented. No indication of whether the export supports single-patient or bulk/population-level export.
- **Access constraints or fees**: Not documented in the EHI export PDF. The disclosures page does not mention EHI export fees.

## 4. Export Content: What's In It

The entire export documentation is a single table with 9 rows. There is **no data dictionary**, no field-level documentation, no schema, no sample data, and no description of what data elements are included within each category.

### Vendor's own content organization

The vendor organizes the export into 9 "functions" with only a document type format specified:

| Function | Doc Type | Fields Documented | Types Documented | Descriptions |
|---|---|---|---|---|
| CCDA | XML, HTML | 0 | No | No |
| Notes | HTML | 0 | No | No |
| C3 Notes | HTML | 0 | No | No |
| Labs | XML, HTML | 0 | No | No |
| Labs Scanned | PDF | 0 | No | No |
| Diagnostics | Discrete fields, PDF | 0 | No | No |
| Scanned documents | PDF | 0 | No | No |
| Smart Forms | HTML | 0 | No | No |
| Messages | Discrete fields | 0 | No | No |

**Total entities**: 9 high-level categories  
**Total fields documented**: 0  
**Fields with descriptions**: 0  
**Field types documented**: No  
**Relationships/foreign keys**: No  
**Value sets/code systems**: No  
**Sample data**: No  

The term "discrete fields" appears for Diagnostics and Messages but is never defined — it is unclear whether this means structured CSV, JSON, database records, or something else. No specification of what fields are included in any category.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor identifies 9 functional categories for export. These can be loosely grouped:

- **Clinical documents**: CCDA (XML/HTML), Notes (HTML), C3 Notes (HTML), Smart Forms (HTML) — 4 categories covering clinical summaries and documentation
- **Lab data**: Labs (XML/HTML), Labs Scanned (PDF) — 2 categories for lab results
- **Diagnostics**: Diagnostics (discrete fields, PDF) — 1 category, likely cardiovascular diagnostic reports
- **Documents**: Scanned documents (PDF) — 1 category for externally-sourced or scanned materials
- **Communications**: Messages (discrete fields) — 1 category

No category addresses demographics, medications, allergies, immunizations, vitals, problems/diagnoses, procedures, orders, referrals, insurance, billing, charges, payments, or care plans as standalone data. The vendor may assume the CCDA covers some of these (demographics, medications, allergies, problems, etc.), but there is no documentation confirming this, and C-CDA typically provides only a clinical summary subset of the full record.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | Likely embedded in CCDA only | Product stores demographics; no dedicated export entity. CCDA provides limited demographic fields. |
| Encounters / visits | ⚠️ Partial | Likely embedded in CCDA only | Product tracks encounters; no dedicated export entity. |
| Problems / conditions / diagnoses | ⚠️ Partial | Likely embedded in CCDA only | Product uses ICD-9/ICD-10 codes extensively (per disclosures); no dedicated export entity. |
| Medications / prescriptions | ⚠️ Partial | Likely embedded in CCDA only | Product has e-Prescribing (Surescripts); no dedicated export entity. Prescription history, pharmacy details likely missing. |
| Allergies | ⚠️ Partial | Likely embedded in CCDA only | Product tracks allergies (per certified criteria); no dedicated export entity. |
| Immunizations | ⚠️ Partial | Likely embedded in CCDA only | Product is cardiology-focused; immunizations may be minimal but are tracked per certification criteria. |
| Vitals | ⚠️ Partial | Likely embedded in CCDA only | Product captures vitals; no dedicated export entity. |
| Lab results | ✅ Covered | "Labs" (XML, HTML) and "Labs Scanned" (PDF) — 2 dedicated categories | Covered, though no field-level detail on what lab data elements are included. |
| Imaging / diagnostic reports | ✅ Covered | "Diagnostics" (discrete fields, PDF) — dedicated category | This is a core strength of the product (17 CV modalities, 4,500+ data elements). However, no documentation of which discrete fields are exported. |
| Procedures | ❌ Not covered | No export category for procedures | Product tracks cardiovascular procedures; significant gap. |
| Clinical notes / documents | ✅ Covered | "Notes" (HTML), "C3 Notes" (HTML), "Smart Forms" (HTML), "Scanned documents" (PDF) — 4 categories | Multiple note types covered. No field-level detail. |
| Care plans / goals | ❌ Not covered | No export category | C3 module manages chronic care programs; care plan data likely stored but not exported. |
| Orders / referrals | ❌ Not covered | No export category | Product has CPOE; order data not addressed in export. |
| Insurance / coverage | ❌ Not covered | No export category | Product likely stores insurance info for billing; not in export. |
| Claims / billing | ❌ Not covered | No export category | Product integrates charge capture (White Plume partnership); billing data not in export. |
| Payments | ❌ Not covered | No export category | If the product tracks payments, they are not exported. |
| Consents / directives | ❌ Not covered | No export category | No evidence. |
| Patient communications / portal messages | ⚠️ Partial | "Messages" (discrete fields) — 1 category | Covered as a category but no detail on what's included (sender, recipient, timestamp, content?). |
| Specialty-specific (Cardiology) | ⚠️ Partial | "Diagnostics" covers CV diagnostic reports | The product captures 4,500+ discrete data elements per patient across 17 CV modalities. The export lists "Diagnostics" as a single line item with no detail on which of these data elements are included. RPM/CCM data from C3 is not addressed except via "C3 Notes." |

**Summary**: Of 19 assessed domains, 3 are marked as covered (labs, diagnostics, clinical notes), 7 as partial (mostly via assumed CCDA inclusion), and 9 as not covered. The partial ratings are generous — without documentation confirming what the CCDA contains, even these may be overstated.

## 6. Documentation Quality

The documentation quality is **extremely poor**:

- **No data dictionary**: The entire export specification is a 9-row table mapping function names to file formats. There is zero field-level documentation.
- **No schema**: No machine-readable schema (JSON Schema, XSD, database schema, etc.) is provided.
- **No sample data**: No example export files are provided.
- **No process documentation**: No description of how to initiate an export, what parameters are available, or what the output file/folder structure looks like.
- **No relationships**: No documentation of how data elements relate to each other (e.g., which notes belong to which encounter).
- **Ambiguous terminology**: The term "discrete fields" is used for Diagnostics and Messages without any definition of what format, structure, or content this entails.
- **Document age**: The PDF was created on 2023-11-16 (per PDF metadata), over 2 years before the January 2026 certification date. It may not reflect current export capabilities.

**Could a developer build an import from this documentation?** No. A developer would know that the export produces some combination of XML, HTML, and PDF files organized by 9 functional categories, but would have no information about data structure, field names, field types, relationships, encoding, or file organization. They would need to request sample data and reverse-engineer the format.

## 7. Overall Assessment

### Classification

**Minimal/stub**: The documentation is a 2-page PDF with a 9-row table listing export categories and file formats. There is no data dictionary, no field-level detail, no schema, no sample data, and no process documentation. It is impossible to assess from this documentation alone whether the export covers a meaningful fraction of the product's data.

### Key Findings

1. **Documentation is a single table on a single page.** The entire EHI export specification (`EHI-Export-Data-Format.pdf`, 2 pages) consists of a title page and a 9-row table mapping function names (CCDA, Notes, Labs, etc.) to document formats (XML, HTML, PDF, "discrete fields"). Zero fields are documented.

2. **The CCDA component suggests standard-based projection for clinical data.** The first row of the export table is "CCDA" (XML, HTML), which is a clinical summary standard — not a native data model export. This likely covers demographics, medications, allergies, problems, and vitals but only at the C-CDA summary level, missing the depth of the product's 1,000+ discrete data elements per patient.

3. **Cardiovascular diagnostic data depth is unknown.** The product's core differentiator is structured cardiovascular diagnostic reporting (4,500+ discrete data elements, 17 modalities). The export lists "Diagnostics" as "discrete fields, PDF" but provides no specification of which fields are included or in what format.

4. **Major data domains are absent from the export.** No export categories exist for procedures, orders, referrals, insurance, billing/charges, payments, care plans, or consents. The product integrates charge capture and uses ICD/CPT codes, suggesting billing data is stored but not exported.

5. **No mechanism documentation.** It is completely unclear how a user or administrator would initiate the export, whether it supports single-patient or bulk export, or what the output file structure looks like.

### Summary Stats

```
Classification:  Minimal/stub
Export format:   Mixed (XML, HTML, PDF, unspecified "discrete fields")
Model type:      Hybrid — C-CDA standard projection + document-oriented export
Entities:        9 high-level categories (no entity/table detail)
Fields:          0 documented
Descriptions:    0% (no fields documented at all)
Sample data:     No
Bulk export:     Unclear
Domains covered: 3 of 15 applicable domains (with 7 partial via assumed CCDA)
```

### Bottom Line

The OMS EHR EHI export documentation is among the thinnest possible — a single table listing 9 document categories and their file formats, with zero field-level detail. Given that the product captures over 5,500 discrete data elements per patient (1,000+ EHR + 4,500+ diagnostics) across cardiology-specific workflows, billing integration, and chronic care management, the documented export covers only a fraction of what the product stores. A patient or provider receiving this export would get a collection of C-CDA documents, HTML notes, and PDFs, but would have no way to know whether the export is complete, and no structured access to the product's rich cardiovascular data model.
