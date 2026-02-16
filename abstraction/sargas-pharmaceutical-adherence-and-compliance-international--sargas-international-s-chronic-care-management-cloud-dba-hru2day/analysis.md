# EHI Export Analysis: Sargas Pharmaceutical Adherence and Compliance International

**Product**: Sargas International's Chronic Care Management Cloud dba hru2day, VERSION 21.9  
**Analysis date**: 2026-02-16  
**CHPL ID**: 15.05.05.2306.SPAC.01.00.0.211014 (listing #10702)

## 1. Product Context

Sargas International (operating as "hru2day") is a niche vendor focused exclusively on **chronic care management (CCM), remote patient monitoring (RPM), and medication therapy monitoring (MTM)** — it is not a full EHR. The product is a cloud-based platform that serves physician practices, hospitals, ACOs, FQHCs, and home health agencies, primarily for Medicare patients with chronic conditions. The company operates a 24/7 clinical call center that performs care management services on behalf of contracting practices.

The product holds **modular** ONC certification (not complete EHR), covering CPOE (medications, labs, imaging), demographics, problem lists, EHI export, clinical information reconciliation, FHIR API, and security criteria. Notably absent: e-prescribing, transitions of care, patient portal VDT, and public health reporting.

**Data the product stores** (based on vendor materials and certification scope):
- Patient demographics
- Problem lists (chronic conditions)
- Medication lists and medication allergies
- Comprehensive care plans (physical, mental, cognitive, psychosocial, functional, environmental domains)
- RPM physiological data: glucose, blood pressure, heart rate, SpO2, weight (from FDA-approved devices)
- Medication adherence records and side effect reports (Drug Adherence® — the company's founding product)
- Care coordination logs (200,000+ interactions across 20,000+ patients)
- Secure messages between patients, care teams, and providers
- CCM/PCM/RPM time tracking for Medicare billing (CPT codes 99490, 99491, 99439, etc.)
- Patient consent records
- Clinical summaries

This data profile is deep on care management but narrow compared to a full EHR. The product is a supplement to a practice's primary EHR, not a replacement for it.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/SPAC-Export.pdf` | The **entire** EHI export documentation. A single 1-page PDF (379,759 bytes, A4) created from a Word document. Contains 8 lines of text (5 informational, 3 generic format definitions). Created 2023-12-19, modified 2025-11-25. | **Primary artifact** — minimal content |
| `downloads/screenshot-certification-page.png` | Screenshot of vendor's certification page at `spacinternational.com/certified-ehr-technology.php`. Standard certification boilerplate. | No additional export information |
| `ONC-HIT-CERTIFICATE-DISCLOSURE_ver_21_9_Revised-25.pdf` (checked live on vendor site) | Mandatory disclosure document listing certified criteria and pricing. | No EHI export technical detail |
| Vendor's open `/pdf/` directory (109 PDFs checked live) | CCM/RPM brochures, consent forms, white papers, billing guides, Real World Testing plans. | **None** contained additional EHI export documentation |

All URLs remained accessible at analysis time (HTTP 200). Seven alternative paths probed on the vendor site (`/ehi`, `/ehi-export`, `/api`, `/fhir`, `/interoperability`, `/data-export`, `/documentation`) all returned 404.

## 3. Export Mechanics

**Format**: ZIP archive containing:
- Nested ZIP archives of C-CDA XML documents (one per patient encounter)
- PDF files attached to the patient's chart

**Mechanism**: Not documented. The PDF provides no instructions on how to initiate an export — no mention of a UI button, admin function, API call, or vendor request process.

**Single-patient vs bulk**: Not specified. The documentation says "the patient EHI export" (singular), suggesting per-patient export.

**Access constraints or fees**: Not documented in the export PDF. The mandatory disclosures mention "one time implementation fee and yearly maintenance charge" and "contracting requirements to use Sargas Services," but do not specify EHI export fees.

## 4. Export Content: What's In It

The documentation provides **no field-level detail whatsoever**. The complete text of the export documentation is:

> **Product Name:** Sargas International's Chronic Care Management Cloud dba hru2day®
>
> **Product Version:** VERSION 21.9
>
> The patient EHI export contains data from the patient's chart. Multiple file formats are used to store this information.
>
> ZIP is an archive file format.
>
> PDF or Portable Document Format is a file format that is used to present text or image based documents.
>
> C-CDA or Consolidated Clinical Document Architecture is a file format used for health information exchange.
>
> The export file itself is a zip file. It contains zip files of C-CDAs and PDF files attached to the patient's chart (machine readable PDF)
>
> Information for each patient encounter is available C-CDA format in zip archive.

That is the entirety of the documentation. Key observations:

- **No data dictionary** — zero entities, zero fields documented
- **No schema** — no C-CDA profile, template IDs, or section specifications
- **No sample data** — no example C-CDA or export ZIP
- **No C-CDA section list** — the documentation does not specify which C-CDA sections are populated
- **No export instructions** — no description of how to initiate the export
- **3 of the 8 lines are filler** — generic definitions of ZIP, PDF, and C-CDA formats that provide no product-specific information

### Vendor's own content organization

There is nothing to tabulate. The vendor provides no entities, tables, fields, or categories. The only content classification is the implicit distinction between "C-CDAs" (clinical data) and "PDFs" (chart attachments).

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor describes exactly two types of content in the export:

1. **C-CDA documents**: Per-encounter clinical documents. No specification of which C-CDA sections are populated. Standard C-CDA documents typically include demographics, problems, medications, allergies, vital signs, procedures, and results — but without documentation or sample data, we cannot confirm what this vendor actually includes.

2. **PDF attachments**: Files attached to the patient's chart. No description of what these are — they could be scanned documents, reports from external systems, consent forms, or other artifacts.

The export provides no mechanism for exporting the product's **core differentiating data**: care plans, care coordination logs, RPM device readings, medication adherence tracking, CCM time logs, or secure messages. C-CDA is a clinical summary standard fundamentally mismatched with this product's primary data types.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | Likely in C-CDA but no sections specified | Product stores demographics (certified (a)(5)); C-CDA standard section exists but no confirmation of content |
| Encounters / visits | ⚠️ Partial | C-CDAs are "per encounter" — encounter metadata likely present | Product tracks encounters; C-CDA structure implies some encounter data |
| Problems / conditions | ⚠️ Partial | Likely in C-CDA but unconfirmed | Product stores problem lists (certified (a)(5)); likely covered by C-CDA but unverified |
| Medications / prescriptions | ⚠️ Partial | Likely in C-CDA but unconfirmed | Product stores medication lists (certified (a)(1)); likely covered by C-CDA but unverified |
| Allergies | ⚠️ Partial | Likely in C-CDA but unconfirmed | Product stores allergies; likely covered by C-CDA but unverified |
| Immunizations | N/A | — | No evidence the product stores immunization data |
| Vitals | ⚠️ Partial | Possibly in C-CDA if populated | RPM vitals (glucose, BP, HR, SpO2, weight) are core to the product; C-CDA vitals section cannot capture time-series RPM data adequately |
| Lab results | ❌ Not covered | No evidence in documentation | Product has CPOE for labs (certified (a)(2)) but no indication results are stored or exported |
| Imaging / diagnostic reports | ❌ Not covered | No evidence in documentation | Product has CPOE for imaging (certified (a)(3)) but no indication results are stored or exported |
| Procedures | ⚠️ Partial | Possibly in C-CDA | Unclear if product stores procedure data |
| Clinical notes / documents | ⚠️ Partial | PDF attachments may include notes | PDF attachments are described but no detail on their nature |
| Care plans / goals | ❌ Not covered | No dedicated care plan export format | **Significant gap**: Care plans are the product's central feature (addressing physical, mental, cognitive, psychosocial, functional, environmental domains). C-CDA has a care plan section but the vendor doesn't confirm it's populated, and C-CDA cannot capture the full richness of structured care plan data this product manages |
| Orders / referrals | ⚠️ Partial | Possibly in C-CDA | Product has CPOE certification; orders may be in C-CDA |
| Insurance / coverage | ❌ Not covered | No evidence in documentation | Unclear if product stores insurance data |
| Claims / billing | ❌ Not covered | No billing data in export | Product tracks CCM/PCM/RPM time for Medicare billing; this data appears absent from export |
| Payments | N/A | — | Product does not appear to process payments directly |
| Consents / directives | ❌ Not covered | No evidence in documentation | Product collects patient consent for CCM enrollment; not included in documented export |
| Patient communications | ❌ Not covered | No secure messaging export | Product supports secure messaging between patients and care teams; not included in documented export |
| Specialty: CCM coordination logs | ❌ Not covered | No coordination log export | **Significant gap**: 200,000+ care coordination interactions are the product's primary operational data |
| Specialty: RPM device data | ❌ Not covered | No RPM data export format | **Significant gap**: Time-series physiological monitoring data (glucose, BP, HR, SpO2, weight) from FDA-approved devices has no C-CDA analog |
| Specialty: Medication adherence | ❌ Not covered | No adherence tracking export | **Significant gap**: Drug Adherence® is the company's founding product; adherence records and side effect reports have no C-CDA representation |

**Summary**: Of 16 applicable domains, 0 are confirmed covered, 7 are partially/likely covered (based on C-CDA assumptions, not documentation), and 9 are not covered. The three most significant gaps — care coordination logs, RPM device data, and medication adherence records — represent the product's core differentiation and the data most unique to this system.

## 6. Documentation Quality

The documentation is **among the thinnest possible while still existing**. Assessment:

- **Completeness**: The documentation describes only the export format (ZIP/C-CDA/PDF) at the container level. It provides zero field-level detail — no entity names, no field names, no types, no descriptions, no value sets, no relationships.
- **Usability**: A developer given this document could not implement an import. They would know only that the export is "a ZIP with C-CDAs and PDFs inside" — nothing about the structure, content, or semantics of the data.
- **Machine-readable artifacts**: None. No schema, no JSON, no XLSX, no sample data.
- **Format descriptions are filler**: 3 of the 8 lines are generic definitions of ZIP, PDF, and C-CDA that any developer would already know.
- **No export procedure**: The documentation does not describe how to initiate the export, who can request it, or what parameters it accepts.
- **Stale indicators**: The PDF was created from a Word document in December 2023 and last modified November 2025. The minimal content suggests it was written as a certification requirement, not as genuine documentation.

The vendor's site has 109 PDFs in an open directory, none of which contain additional EHI export documentation. The mandatory disclosures PDF confirms the certification but adds no technical detail about the export.

## 7. Overall Assessment

### Classification

**Minimal/stub**: The documentation is too thin to meaningfully assess what the export contains. The single page describes only the container format (ZIP of C-CDAs and PDFs) with no data dictionary, no field-level documentation, no sample data, and no export instructions. Even assuming the C-CDAs are well-populated, the format is inherently incapable of representing the product's core data (care coordination logs, RPM device readings, medication adherence records).

### Key Findings

1. **Entire export documentation is 8 lines on a single page** — no data dictionary, no schema, no sample data, no export instructions. Three of the 8 lines are generic definitions of ZIP, PDF, and C-CDA formats. (`SPAC-Export.pdf`, verified via `pdftotext` and visual inspection)

2. **Export is C-CDA + PDF, fundamentally mismatched with the product's data** — The product is a chronic care management platform whose core data (care coordination logs, RPM device time-series, medication adherence records, structured care plans, CCM time tracking) has no standard C-CDA representation. Using C-CDA as the sole export format means the majority of the product's unique data likely cannot be exported.

3. **No C-CDA section specification** — The documentation does not even list which C-CDA sections are populated, making it impossible to confirm coverage of even standard clinical domains (demographics, problems, medications, allergies).

4. **No additional documentation found anywhere on the vendor's site** — 109 PDFs in the open `/pdf/` directory, 7 alternative URL paths probed, and the mandatory disclosures PDF all checked; none contain additional EHI export technical detail.

5. **Certification is modular, not complete EHR** — The product supplements a practice's primary EHR with CCM/RPM/MTM capabilities. Its data is specialized, which makes the lack of a native data export all the more concerning — this specialized data is exactly what C-CDA cannot capture.

### Summary Stats

```
Classification:  Minimal/stub
Export format:   ZIP containing C-CDA XML + PDF attachments
Model type:      Standard projection (C-CDA)
Entities:        N/A (no data dictionary)
Fields:          N/A (no data dictionary)
Descriptions:    N/A
Sample data:     No
Bulk export:     Unclear
Domains covered: 0 of 16 confirmed; 7 of 16 likely partial (based on C-CDA assumptions)
```

### Bottom Line

The EHI export documentation is a stub — a single page that describes the container format but nothing about the contents. The use of C-CDA as the sole clinical export format is especially problematic for this product, because the data that makes hru2day unique (care coordination logs, RPM device readings, medication adherence tracking, structured care plans, CCM billing time logs) has no representation in C-CDA. A patient requesting their data from this system would likely receive clinical summaries covering a fraction of what the product stores about them, with no access to the care management records that are the system's primary purpose.
