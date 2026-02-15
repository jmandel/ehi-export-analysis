# EHI Export Analysis: Perk Medical Systems LLC (PCB Apps LLC)

**Product**: ezPractice V15.1
**Analysis date**: 2026-02-15
**CHPL IDs**: 15.07.04.2154.Ezpr.15.01.1.230208

## 1. Product Context

ezPractice is a certified ambulatory EHR developed by Perk Medical Systems LLC (also listed as PCB Apps LLC), a very small entity (approximately 3 employees, $230K revenue) based in Somerset, NJ. The product is hosted through the penn-clinical.com domain and appears to serve an extremely limited user base — possibly only the developer's own practice(s). The SED metadata indicates the product is designed for pediatric use.

According to the product's own executive summary (page 4 of `EHI Export.pdf`), ezPractice's product portfolio includes:
- **Products**: Certified EHR, Practice Management, Patient Portal, Health Information Exchange
- **Services**: Revenue Cycle Management, Professional Services

The product is described as including "components of care and billing for nursing programs, home health programs, wellness programs, specialty-based programs, physician driven care, employee health programs, public health programs and mental health programs in ambulatory facilities."

The certified criteria cover a broad range of ambulatory EHR capabilities including CPOE for medications, labs, and imaging (a)(1)–(a)(3), drug interaction checks (a)(4), demographics (a)(5), clinical decision support (a)(9), family health history (a)(12), implantable devices (a)(14), transitions of care (b)(1), EHI export (b)(10), clinical quality measures (c)(1), patient health information capture (e)(3), FHIR API (g)(10), and Direct messaging (h)(1). E-prescribing is handled via third-party DrFirst Rcopia.

**Baseline expectation**: Given the product includes Practice Management and Revenue Cycle Management, a complete EHI export should cover clinical data, billing/claims data, patient notes, scanned documents, orders, and any specialty clinical data the system stores.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/EHI Export.pdf` | 7-page PDF (289 KB). Primary EHI export documentation. Created 2023-12-20 in Microsoft Word. Pages 1–3 are cover, copyright, and TOC. Pages 4–7 contain substantive content (~3 pages of substance). | **Primary source** — only artifact with EHI export details |
| `downloads/fhir-base-urls.csv` | 263-byte CSV with 4 rows listing test and production FHIR endpoints. Production endpoints listed as "available upon request." | **Low relevance** — documents (g)(10) FHIR API, not (b)(10) EHI export |
| `downloads/ehi-export-page.png` | Screenshot of penn-clinical.com/ehi-export page | **Minimal** — confirms page layout only |
| `downloads/ehi-export-page-full.png` | Full-page screenshot of the EHI export page | **Minimal** — confirms page layout only |
| `chpl-metadata.json` | CHPL certification details including certified criteria list | **Useful** — confirms certification scope |
| `product-research.md` | Prior research on vendor and product | **Orientation** — established product context |

**No sample data files, no schemas, no data dictionaries, no machine-readable artifacts** were found in the downloads. The entire EHI export documentation consists of a single 7-page PDF.

## 3. Export Mechanics

- **Format**: Mixed — C-CDA R2.1 XML paired with HTML renderings (clinical data), CSV (patient notes), CDA XML with Base64 encoding (scanned records). "Claim Data" mentioned as a file TYPE but format is undocumented.
- **Mechanism**: The export produces ZIP file(s). The documentation states "the resulting export may contain one patient, or a full collection of patients" — implying both single-patient and bulk export capability. No UI screenshots or step-by-step instructions for initiating the export are provided.
- **Single-patient vs bulk**: Both supported per the documentation text.
- **Fees**: No fees for self-service export. Fees may apply if ezPractice performs the export on the user's behalf ("based on time and effort").
- **File naming**: Files follow `PID_INTERNALNUMBERING.EXT` or `PID_INTERNALNUMBERING_TYPE.EXT` where TYPE values include "Claim Data", "Echart", and "patNotes".

## 4. Export Content: What's In It

The export documentation describes **four categories** of exported data, but only one has field-level documentation.

### 4a. Patient Demographics and Clinical Data (C-CDA R2.1)

Format: HL7 C-CDA R2.1 XML files, each paired with an HTML rendering.
Documentation depth: **None** — the PDF defers entirely to the external C-CDA R2.1 specification with two URLs:
- https://www.ncbi.nlm.nih.gov/pmc/articles/PMC1380194/
- https://www.hl7.org/implement/standards/product_brief.cfm?product_id=447

No documentation is provided on:
- Which C-CDA sections are populated
- How ezPractice-specific data maps to C-CDA elements
- What vendor extensions or customizations exist (if any)
- Which data elements from the EHR are included vs excluded

A C-CDA document typically covers demographics, medications, allergies, problems, procedures, vital signs, immunizations, lab results, and clinical notes — but the actual coverage depends entirely on the vendor's implementation, which is not documented.

### 4b. Adhoc Patient Notes (CSV)

Format: CSV with `patNotes` TYPE indicator in filename.
Documentation depth: **7 columns documented** with names and descriptions (the only field-level documentation in the entire export).

| Column # | Column Name | Description |
|---|---|---|
| 1 | PID | Patient IDs (unique) |
| 2 | Patient Notes ID | Patient note IDs (unique) |
| 3* | Username | User who documented the note |
| 3* | Subject | Subject of the note (may be blank) |
| 4 | Patient Notes Category | Category from user-defined pick list |
| 5 | Patient Notes Date | Date the note was created |
| 6 | Patient Notes | Documented details of the patient note |

*Note: The PDF contains a numbering error — columns 3 and 4 (Username and Subject) are both labeled as column "3".*

This covers telephone calls, adhoc notes, and other unstructured patient documentation.

### 4c. Scanned Records (CDA XML / Base64)

Format: HL7 CDA XML with Base64-encoded scanned/uploaded documents. `Echart` TYPE indicator in filename.
Documentation depth: **None** — defers to external CDA specification. No documentation on what types of documents are encoded, how they're categorized, or their metadata structure.

### 4d. Claim Data (undocumented)

"Claim Data" appears as a TYPE value in the file naming convention (page 5 of the PDF), and the introductory text states "the zip file includes files containing the patient demographics, clinical records, billing records, scanned records, and more." However, **there is zero documentation** of the claim data format — no field descriptions, no format specification, no example. A recipient of claim data files would have no documentation to interpret them.

### Vendor's own content organization

| Entity/Category | Format | Fields Documented | Types Documented | Descriptions Provided |
|---|---|---|---|---|
| Patient Demographics & Clinical Data | C-CDA R2.1 XML + HTML | 0 (defers to C-CDA spec) | No | No |
| Adhoc Patient Notes | CSV | 7 | No | Yes (7/7) |
| Scanned Records | CDA XML / Base64 | 0 (defers to CDA spec) | No | No |
| Claim Data | Unknown | 0 | No | No |

**Total field-level documentation: 7 fields** (all in the patient notes CSV). All other data categories have zero vendor-specific documentation.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor describes four file categories but documents only one in detail:

1. **Patient Notes (CSV)**: The only category with field-level documentation. 7 columns described. Covers telephone calls and adhoc notes — a narrow slice of patient data.

2. **Clinical Data (C-CDA)**: The broadest category by implication but entirely undocumented at the vendor level. C-CDA R2.1 is a well-established standard that typically includes demographics, medications, allergies, problems, procedures, vitals, immunizations, and lab results — but the vendor provides no indication of which sections they populate or how completely.

3. **Scanned Records (CDA/Base64)**: Covers uploaded and scanned documents. Could contain important clinical documents but is undocumented.

4. **Claim Data**: Mentioned in the file naming convention and introductory text but completely undocumented. If present, this would partially address billing coverage, but without any documentation, it's impossible to assess depth.

The vendor's executive summary explicitly lists Practice Management and Revenue Cycle Management as part of the product portfolio, and the documentation text mentions "billing records" as part of the export. The mention of "Claim Data" as a file TYPE suggests billing data is exported, but the total absence of documentation for this category is a significant gap.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | Implied via C-CDA; no vendor-specific documentation | C-CDA typically includes demographics but vendor doesn't document which fields |
| Encounters / visits | ⚠️ Partial | Implied via C-CDA | C-CDA may include encounter data; undocumented |
| Problems / conditions / diagnoses | ⚠️ Partial | Implied via C-CDA | Standard C-CDA section; coverage unknown |
| Medications / prescriptions | ⚠️ Partial | Implied via C-CDA; e-prescribing via DrFirst Rcopia | Whether DrFirst prescription data is included is unclear |
| Allergies | ⚠️ Partial | Implied via C-CDA | Standard C-CDA section; coverage unknown |
| Immunizations | ⚠️ Partial | Implied via C-CDA | Likely present for pediatric product; undocumented |
| Vitals | ⚠️ Partial | Implied via C-CDA | Standard C-CDA section; coverage unknown |
| Lab results | ⚠️ Partial | Implied via C-CDA; product certified for CPOE-Lab (a)(2) | Coverage unknown |
| Imaging / diagnostic reports | ⚠️ Partial | Implied via C-CDA; product certified for CPOE-Imaging (a)(3) | Coverage unknown |
| Procedures | ⚠️ Partial | Implied via C-CDA | Standard C-CDA section; coverage unknown |
| Clinical notes / documents | ⚠️ Partial | Patient Notes CSV (7 fields); scanned records (CDA/Base64) | Adhoc notes documented; structured clinical notes (progress notes, H&P) coverage via C-CDA is unknown |
| Care plans / goals | ⚠️ Partial | May be in C-CDA | Not explicitly documented |
| Orders / referrals | ⚠️ Partial | Product certified for CPOE (a)(1)–(a)(3); may be in C-CDA | Whether order details export is unknown |
| Insurance / coverage | ❌ Not covered | No evidence in documentation | Product includes Practice Management; likely a gap |
| Claims / billing | ⚠️ Partial | "Claim Data" mentioned as TYPE; "billing records" mentioned in intro text; format completely undocumented | Product includes RCM; data may be exported but documentation is missing |
| Payments | ❌ Not covered | No evidence in documentation | If product handles payments via RCM, this is a gap |
| Consents / directives | ⚠️ Partial | May be in C-CDA advance directives section | Undocumented |
| Patient communications / portal messages | ⚠️ Partial | Product includes Patient Portal; not mentioned in export docs | Possible gap — portal messages may not be exported |
| Family health history | ⚠️ Partial | Certified for (a)(12); likely in C-CDA | Undocumented |
| Implantable devices | ⚠️ Partial | Certified for (a)(14); may be in C-CDA | Undocumented |
| Specialty-specific (pediatric) | ❌ Not covered | SED metadata says "Pediatric"; no pediatric-specific data elements documented | If product stores growth charts, well-child data, or pediatric assessments, these may be absent |

**Note on "Partial" ratings**: Nearly all clinical domains receive "Partial" rather than "Covered" because the vendor provides no documentation confirming which C-CDA sections are populated. The data *may* be present in the C-CDA files, but the documentation doesn't confirm it. Without sample data or a C-CDA section inventory, coverage cannot be verified.

## 6. Documentation Quality

The documentation quality is **very poor**:

- **Data dictionary**: Effectively nonexistent. Only 7 CSV fields are documented across the entire export. Clinical data, scanned records, and claim data have zero field-level documentation.
- **Schema/machine-readable artifacts**: None. No XSD, JSON Schema, sample data files, or any machine-readable format specification.
- **Sample data**: None provided.
- **Import guidance**: Absent. The document states "the user must understand the formatting of the resulting files" and "assumes the user has a technical understanding [of] HL7 specifications" — effectively shifting all documentation burden to the external C-CDA specification.
- **Data relationships**: Not documented. No indication of how files relate to each other beyond the PID (Patient ID) in filenames.
- **Value sets / code systems**: Not documented.
- **Completeness**: The document does not enumerate which data elements are included or excluded from the export. There is no way to determine from this documentation alone what data a recipient would actually receive.

**Could a developer build an import from this documentation?** Only for the patient notes CSV (7 fields, clearly described). For all other data categories, a developer would need to rely entirely on external C-CDA/CDA specifications and reverse-engineer the actual output by examining export files — the vendor documentation provides no implementation guidance.

The PDF also contains a formatting error: in the patient notes column table, columns for "Username" and "Subject" are both numbered as column "3".

## 7. Overall Assessment

### Classification

**Standard-based projection**

The export is primarily C-CDA R2.1 — a clinical document standard — supplemented with CSV for patient notes and CDA/Base64 for scanned records. This is not a native database export. C-CDA is inherently limited to clinical summary data and cannot represent the full breadth of data an EHR stores (billing, scheduling, custom forms, specialty data, practice management). The vendor appears to have wrapped their existing C-CDA transitions-of-care capability as their (b)(10) export, adding CSV for notes and mentioning "Claim Data" without documentation.

### Key Findings

1. **The export is a C-CDA repackaging with minimal additions.** Clinical data is exported as C-CDA R2.1 — the same standard used for transitions of care under (b)(1). This covers a clinical summary but not the full breadth of EHI the product stores. The only additions beyond C-CDA are a 7-column CSV for patient notes and Base64-encoded scanned records.

2. **Only 7 fields are documented across the entire export.** The patient notes CSV is the only data category with field-level documentation. All other categories (clinical data, scanned records, claim data) have zero vendor-specific field documentation, deferring entirely to external specifications.

3. **Claim data is mentioned but completely undocumented.** "Claim Data" appears as a file TYPE value in the naming convention, and "billing records" are mentioned in the introductory text, but there is zero documentation of the format, fields, or structure. This makes the billing data — if actually exported — unusable without reverse engineering.

4. **No sample data, no schemas, no machine-readable artifacts.** The entire export documentation is a single 7-page PDF with ~3 pages of substance. There are no sample export files, no schemas, and no data dictionaries that would allow a developer to process the export.

5. **The product explicitly includes Practice Management and RCM**, but the export documentation provides no evidence these data domains are meaningfully covered. The gap between the product's stated capabilities and the export's documented coverage is significant.

### Summary Stats

    Classification:  Standard-based projection
    Export format:   C-CDA R2.1 XML, CSV, CDA XML (mixed)
    Model type:      Standard projection (C-CDA + supplemental files)
    Entities:        4 file categories (not a native data model)
    Fields:          7 documented (patient notes CSV only)
    Descriptions:    100% of documented fields (7/7), but only 7 fields total
    Sample data:     No
    Bulk export:     Yes (single-patient and full collection)
    Domains covered: 0 of 18 fully confirmed; ~12 partially implied via C-CDA

### Bottom Line

ezPractice's EHI export is a C-CDA clinical summary repackaged as a (b)(10) export, supplemented with a basic CSV for patient notes and Base64-encoded scanned records. With only 7 documented fields, no sample data, no schemas, and critical data categories (billing, practice management) either undocumented or absent, a patient or provider would receive clinical summary data in a standard format but would have no assurance of completeness and no practical ability to interpret non-C-CDA portions of the export. The single biggest gap is the near-total absence of documentation — even if the export contains billing and specialty data, there is no way to know from the documentation what was exported or how to use it.
