# EHI Export Analysis: Perk Medical Systems LLC (PCB Apps LLC)

**Product**: ezPractice V15.1  
**Analysis date**: 2026-02-16  
**CHPL ID**: 15.07.04.2154.Ezpr.15.01.1.230208

## 1. Product Context

ezPractice is a small ambulatory EHR developed by Perk Medical Systems LLC (with technical support from PCB Apps LLC, an enterprise IT consulting firm). The product appears to serve a very small number of practices — possibly only the developer's own clinic. It is certified for pediatric use (per SED metadata).

Based on the EHI Export PDF's own executive summary (p. 4), ezPractice is described as including "components of care and billing for nursing programs, home health programs, wellness programs, specialty-based programs, physician driven care, employee health programs, public health programs and mental health programs in ambulatory facilities." The product portfolio explicitly lists:
- **Certified Health Information Technology – EHR**
- **Practice Management**
- **Patient Portal**
- **Health Information Exchange**
- **Revenue Cycle Management** (as a service)

ONC certification covers CPOE (medications, labs, imaging), drug interaction checks, demographics, clinical decision support, family health history, implantable devices, transitions of care (C-CDA), FHIR API (g)(10), Direct messaging, and patient health information capture. E-prescribing is via third-party DrFirst Rcopia.

The key point for export assessment: the vendor's own documentation claims the product handles **both clinical care and billing/practice management**, and the EHI Export PDF specifically mentions "billing records" as part of the export content. This sets the expectation for what the export should cover.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/EHI Export.pdf` (289 KB, 7 pages) | Primary EHI export documentation. Contains boilerplate (copyright, disclaimers), brief export description, file naming conventions, a 7-field CSV schema for patient notes, and references to external C-CDA specs. Created 2023-12-20. | **Primary source** — but thin on substance |
| `downloads/fhir-base-urls.csv` (263 bytes) | FHIR server endpoints for (g)(10) API, not (b)(10) export. Test and production URLs. | Not relevant to (b)(10) |
| `downloads/ehi-export-page.png` (127 KB) | Screenshot of penn-clinical.com/ehi-export showing PDF download link. | Confirms web page exists |
| `downloads/ehi-export-page-full.png` (153 KB) | Full-page screenshot of the EHI export page. | Confirms page layout |

The entire analysis rests on a single 7-page PDF, of which only ~2 pages contain substantive export documentation.

## 3. Export Mechanics

- **Format**: ZIP file(s) containing three types of files:
  1. C-CDA R2.1 XML + HTML pairs (demographics & clinical data)
  2. CSV files (adhoc patient notes)
  3. CDA XML with Base64-encoded scanned documents
- **Mechanism**: User-initiated within the ezPractice application
- **Scope**: Single patient or full collection of patients (bulk export supported)
- **Fees**: No fees for self-service export. Vendor-performed export may incur fees "based on time and effort."
- **Access**: Valid user subscription required

File naming convention: `PID_INTERNALNUMBERING[_TYPE].EXT` where PID is the patient ID, TYPE indicates content category (patNotes, Echart, or absent for clinical data).

## 4. Export Content: What's In It

The export documentation describes three categories of content, but provides a product-specific data dictionary for only one.

### 4a. Patient Demographics and Clinical Data (C-CDA R2.1)

The documentation states these files follow "the specification as set for HL7 C-CDA R2.1 specifications" and provides two external URLs to the C-CDA standard. **No product-specific data dictionary is provided.** There is no documentation of:
- Which C-CDA sections are populated
- What data elements beyond standard C-CDA are included
- Whether billing data (mentioned on p. 5 as included in the ZIP) is embedded in C-CDA or exported separately
- Whether any vendor extensions exist
- What clinical data elements the product actually stores vs. what maps to C-CDA

The documentation simply points to the generic HL7 C-CDA R2.1 spec and expects the reader to understand.

### 4b. Adhoc Patient Notes (CSV)

This is the **only component with product-specific documentation**. The CSV contains 7 fields (note: the PDF has a column numbering error, listing column 3 twice):

| Column | Name | Description | Type |
|---|---|---|---|
| 1 | PID | Patient IDs (unique) | identifier |
| 2 | Patient Notes ID | Patient note IDs (unique) | identifier |
| 3 | Username | User who documented the note | string |
| 4 | Subject | Subject of the note (may be blank) | string |
| 5 | Patient Notes Category | Category from user-defined pick list | string |
| 6 | Patient Notes Date | Date the note was created | date |
| 7 | Patient Notes | Documented details of the patient note | text |

### 4c. Scanned Records (CDA XML)

Base64-encoded scanned/uploaded documents within CDA XML files. No product-specific documentation; references the same external C-CDA/CDA specs. The documentation notes these files "could be large in size depending on the amount of scanned data."

### Vendor's own content organization

| Entity/Component | Fields Documented | Described | Types | Format |
|---|---|---|---|---|
| Patient Demographics and Clinical Data | 0 (defers to C-CDA spec) | N/A | N/A | C-CDA R2.1 XML + HTML |
| Adhoc Patient Notes | 7 | 7 (100%) | Informal | CSV |
| Scanned Records | 0 (defers to CDA spec) | N/A | N/A | CDA XML (Base64) |
| **Total** | **7** | **7** | — | — |

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor describes three export components:
1. **C-CDA clinical data**: Presumably covers demographics, problems, medications, allergies, vitals, labs, procedures, and other standard C-CDA sections — but this is inference from the C-CDA spec, not from vendor documentation. No product-specific mapping is provided.
2. **Patient notes CSV**: A narrow, well-documented component covering telephone calls and adhoc notes — 7 fields. This is the only purpose-built element.
3. **Scanned documents**: Binary documents wrapped in CDA XML. Valuable for completeness but no structured data.

The PDF's "Understanding resulting EHI Export Files" section (p. 5) states the ZIP includes "patient demographics, clinical records, billing records, scanned records, and more." However, the subsequent documentation describes **no billing-specific export component**. The word "billing" appears only in that introductory sentence and in the executive summary — there is no billing data dictionary, no billing file format description, and no indication of how billing data is actually exported.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | Presumably in C-CDA, but no product-specific mapping | Product stores demographics (a)(5); C-CDA covers basics but no vendor detail on what's included |
| Encounters / visits | ⚠️ Partial | Presumably in C-CDA encounters section | No product-specific documentation |
| Problems / conditions | ⚠️ Partial | Presumably in C-CDA problems section | No product-specific documentation |
| Medications / prescriptions | ⚠️ Partial | Presumably in C-CDA medications section; e-prescribing via DrFirst | No documentation on whether DrFirst prescription data is included |
| Allergies | ⚠️ Partial | Presumably in C-CDA allergies section | No product-specific documentation |
| Immunizations | ⚠️ Partial | Presumably in C-CDA immunizations section | Product likely tracks immunizations (pediatric focus); no specific documentation |
| Vitals | ⚠️ Partial | Presumably in C-CDA vitals section | No product-specific documentation |
| Lab results | ⚠️ Partial | Presumably in C-CDA results section; CPOE for labs certified (a)(2) | No product-specific documentation |
| Imaging / diagnostic reports | ⚠️ Partial | Presumably in C-CDA; CPOE for imaging certified (a)(3) | No product-specific documentation |
| Procedures | ⚠️ Partial | Presumably in C-CDA procedures section | No product-specific documentation |
| Clinical notes / documents | ✅ Covered | Patient Notes CSV (7 fields) + scanned records in CDA XML | The CSV captures adhoc notes; scanned records capture uploaded documents. Clinical encounter notes presumably in C-CDA. |
| Care plans / goals | ⚠️ Partial | May be in C-CDA care plan section | No product-specific documentation |
| Orders / referrals | ⚠️ Partial | CPOE certified for meds, labs, imaging; may be in C-CDA | No product-specific documentation on order export |
| Insurance / coverage | ❌ Not covered | No insurance-specific export documented | Product has Practice Management module; gap if PM stores insurance data |
| Claims / billing | ❌ Not covered | PDF mentions "billing records" in intro but provides no billing data dictionary or format | Product explicitly offers Revenue Cycle Management and Practice Management; significant gap |
| Payments | ❌ Not covered | No payment data documented | Product has RCM services; gap if payments stored in system |
| Consents / directives | ⚠️ Partial | May be in C-CDA advance directives section | No product-specific documentation |
| Patient communications | ✅ Covered | Patient Notes CSV captures telephone calls and adhoc notes | Well-documented with 7 fields |
| Family health history | ⚠️ Partial | Certified for (a)(12); presumably in C-CDA | No product-specific documentation |

**Key observation**: Nearly every domain is rated "Partial" because the export relies on standard C-CDA without any product-specific documentation. We cannot confirm or deny what C-CDA sections ezPractice actually populates. The only domains with clear evidence are patient communications (CSV) and scanned documents (CDA XML). Billing, insurance, and payments are completely absent from the export documentation despite the product explicitly offering practice management and revenue cycle management.

## 6. Documentation Quality

The documentation is **poor**:

- **7 pages total**, of which ~3.5 are boilerplate (copyright, disclaimers, liability, compliance statement)
- **Only 7 fields** have product-specific documentation (the patient notes CSV)
- **No product-specific data dictionary** for clinical data — the vendor simply points to the external C-CDA R2.1 specification
- **No sample data** provided
- **No machine-readable schemas** 
- **No relationship documentation** between export components
- **No value sets or code systems** documented beyond "user-defined pick list" for note categories
- **No billing data format** despite claiming billing records are included

A developer receiving this documentation would know:
1. The export is a ZIP file
2. There are XML, HTML, and CSV files inside
3. The CSV has 7 columns for patient notes
4. Everything else follows "C-CDA R2.1"

They would **not** know what C-CDA sections to expect, what vendor-specific data beyond standard C-CDA is included, how billing data appears, or how to reliably import the full record.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Minimal/stub/unclear**

The documentation is too thin to assess actual coverage. The PDF mentions "billing records" in a single introductory sentence but provides no billing export documentation, no billing data dictionary, and no billing file format. The clinical data component defers entirely to the external C-CDA R2.1 specification with no product-specific mapping. The only substantive, purpose-built element is the 7-field patient notes CSV. We cannot determine from the documentation alone whether the export actually includes billing data, specialty-specific data, or the full breadth of clinical data the product stores. The documentation describes aspirations ("patient demographics, clinical records, billing records, scanned records, and more") but documents only a tiny fraction of what's claimed.

**Axis 2 — Export approach: Repackaged existing export**

The export is built on C-CDA R2.1 — the same standard used for the vendor's (b)(1) Transitions of Care certification. The documentation provides no evidence of any data dictionary, mapping, or export capability beyond what the existing C-CDA exchange would produce. The only purpose-built component is the 7-field patient notes CSV, which is a minor addition. The scanned documents component (CDA XML with Base64 encoding) may represent some additional effort but uses the same CDA framework. There is no evidence the vendor built a purpose-specific export covering billing, practice management, or other non-clinical data domains.

### Key Findings

1. **Only 7 fields documented**: The entire product-specific data dictionary consists of a single 7-field CSV schema for patient notes. All other export content defers to external C-CDA R2.1 specifications with no vendor-specific mapping (EHI Export.pdf, p. 5-6).

2. **Billing gap despite claims**: The PDF explicitly states the export ZIP includes "billing records" (p. 5), and the executive summary describes the product as including "components of care and billing." However, no billing data format, schema, or dictionary is documented anywhere. This is a significant gap given the product's Practice Management and Revenue Cycle Management capabilities.

3. **C-CDA repackaging**: The clinical data component uses the same C-CDA R2.1 format as the vendor's (b)(1) Transitions of Care certification. No evidence of additional data elements, vendor extensions, or coverage beyond standard C-CDA sections.

4. **Documentation is mostly boilerplate**: Of 7 PDF pages, approximately 3.5 pages are copyright notices, disclaimers, and liability language. The substantive export documentation fits on roughly 2 pages.

5. **Scanned documents included**: The export does include scanned/uploaded documents (Base64 in CDA XML), which represents some effort beyond a basic C-CDA export, though no structured data is documented for this component.

### Summary Stats

```
Coverage:        Minimal/stub/unclear
Approach:        Repackaged existing export
Export format:   C-CDA R2.1 XML, CSV, CDA XML (Base64)
Entities:        3 export components
Fields:          7 (product-specific documentation)
Descriptions:    100% (of the 7 documented fields)
Sample data:     No
Bulk export:     Yes (single or full patient collection)
Domains covered: 2 of 16 applicable domains with clear evidence (patient communications, scanned documents); remainder uncertain due to C-CDA deferral
```

### Bottom Line

The ezPractice EHI export documentation is a 7-page PDF that provides a product-specific data dictionary for only 7 fields (a patient notes CSV) and defers all clinical data documentation to the external C-CDA R2.1 standard. Despite the vendor's own claim that billing records are included in the export, no billing data format or schema is documented. A patient or provider receiving this export would get C-CDA clinical summaries, telephone notes, and scanned documents — but would have no way to verify completeness, and billing/practice management data appears undocumented or absent.
