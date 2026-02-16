# EHI Export Analysis: Braintree Health

**Product**: BRAINTREE (BMW Platform) v10.5.1.1
**Analysis date**: 2026-02-16
**CHPL ID**: 15.02.05.1167.BRNT.01.01.1.211119 (listing #10727)

## 1. Product Context

Braintree Health develops the BMW (Braintree Medical Workflow) Platform, an integrated EHR designed primarily for **outpatient procedure centers, ambulatory surgery centers, vascular access centers, and interventional radiology facilities**. The company is based in Corpus Christi, Texas and appears to be a small niche vendor.

The BMW Platform is distinguished from typical ambulatory EHRs by its deep integration of:

- **Medical imaging (BT PACS/BT RIS)**: DICOM image acquisition, archival, display, and routing; radiology procedure tracking and reporting
- **Procedure-oriented workflow**: Pre-operative, intra-operative, and post-operative clinical documentation
- **Integrated billing with auto-CPT encoding**: Billing codes generated automatically as nurses record procedural steps
- **Inventory management (BT Inventory)**: Per-procedure supply consumption tracking
- **Scheduling (BT Scheduler)**: Multi-doctor, multi-facility appointment management

The product stores clinical data (demographics, encounters, vitals, medications, allergies, problems, labs, clinical notes, procedure documentation), imaging data (DICOM images, radiology reports), financial/billing data (CPT codes, charges, insurance, receivables), and patient engagement data (portal access, consent forms). It is certified for 49 ONC criteria including (b)(10) EHI Export.

**Baseline expectation**: A complete EHI export should cover clinical documentation (especially procedure-oriented pre-op/intra-op/post-op records), medications, allergies, labs, vitals, problems, immunizations, billing/charges, imaging, and consent forms.

## 2. Artifacts Reviewed

| Artifact | Size | Description | Informativeness |
|---|---|---|---|
| `certification-page.html` | 71,326 bytes | Full HTML of the ONC certification page; contains the entire b(10) EHI export documentation as 6 inline bullet points | **Primary source** — this is the only b(10) documentation |
| `ehi-export-section-screenshot.png` | 244,687 bytes | Screenshot of the b(10) section on the page | Confirms the HTML extraction; visually verified 6 bullet points |
| `certification-page-full.png` | 938,405 bytes | Full-page screenshot of ONC certification page | Context only |
| `Braintree-FHIR-API-Documentation-1.pdf` | 803,598 bytes (76 pages) | FHIR g(10) API documentation — SMART on FHIR launch, OAuth2 auth, 16 supported FHIR resource types with sample JSON | **Not b(10)** — useful only as context for what clinical data the system can expose via FHIR |
| `Braintree-fhir-doc.pdf` | 166,453 bytes (1 page) | FHIR server endpoint URLs (test and production) | Not relevant to b(10) |
| `transparency.htm` | 9,971 bytes | Excel-exported HTML frameset for ONC cost disclosures | Not relevant to b(10) |

**Key finding**: There are **no b(10)-specific downloadable artifacts** — no data dictionary, no schema, no sample export files, no user guide. The entire b(10) documentation is 6 bullet points of inline text on the certification page.

## 3. Export Mechanics

- **Format(s)**: Mixed — C-CDA XML (demographics), HTML (consent forms, reports), PDF described as "computable format" (clinical/billing/encounter documentation), DICOM (medical images), original upload format (attachments)
- **Mechanism**: Not documented. No description of how the export is triggered, whether it's a UI button, API call, or vendor-assisted process.
- **Single-patient vs bulk**: Not documented. No indication of whether single-patient or bulk export is supported.
- **Access constraints or fees**: Not documented.
- **Who can request**: Not documented.

The certification page provides zero procedural information about how to actually perform an export.

## 4. Export Content: What's In It

### What the b(10) documentation says

The entire b(10) documentation consists of an introductory sentence and 6 bullet points (verified against both the downloaded HTML and the screenshot):

> Braintree understands the importance of ensuring patients have timely, secure and easy access to electronic health information ("EHI") to empower them in managing their own health and well-being.
>
> Key Information About the Exported Data:
> 1. While certain EHI, such as images, documents, reports are exported in human-readable html/pdf format where applicable.
> 2. The patient demographics are exported in CCDA xml format.
> 3. The consents form of the patient are exported in HTML format.
> 4. The clinical and billing report and encounter documentation of the patient is exported in PDF format. The PDF provided are in computable format.
> 5. The patient attachments are exported in the original format as uploaded into EMR.
> 6. The patient images are exported into DICOM format.

**There is no data dictionary.** Zero fields, zero tables, zero entities are documented. No field names, no types, no descriptions, no value sets, no relationships, no sample data exist in any artifact.

### Vendor's own content organization

The vendor organizes the export by output format, not by data domain. There are no entity/table definitions. The entirety of what is documented:

| Entity (vendor's term) | Fields | Described | Types | Format | Category |
|---|---|---|---|---|---|
| General EHI (images, documents, reports) | 0 | 0 | N/A | HTML/PDF | General |
| Patient Demographics | 0 | 0 | N/A | C-CDA XML | Demographics |
| Consent Forms | 0 | 0 | N/A | HTML | Consents |
| Clinical & Billing Report / Encounter Documentation | 0 | 0 | N/A | PDF ("computable format") | Clinical/Billing |
| Patient Attachments | 0 | 0 | N/A | Original upload format | Attachments |
| Patient Images | 0 | 0 | N/A | DICOM | Imaging |

**Total entities described**: 6 categories (format-level, not field-level)
**Total fields documented**: 0
**Fields with descriptions**: 0
**Fields with types**: 0

### g(10) FHIR API (for context only)

The 76-page FHIR API documentation (g(10), **not** b(10)) covers 16 FHIR resource types per USCDI v1:

1. Allergies and Intolerances
2. Assessment and Plan of Treatment
3. Care Team Members
4. Clinical Notes / DocumentReference / DiagnosticReport
5. Goals
6. Health Concerns (Condition)
7. Immunizations
8. Laboratory Results (Observation, DiagnosticReport)
9. Medications (Medication, MedicationRequest)
10. Patient Demographics
11. Problems (Condition)
12. Procedures
13. Provenance
14. Smoking Status (Observation)
15. Unique Device Identifiers (ImplantableDevice)
16. Vital Signs (Observation)

This confirms the product stores standard clinical data domains (allergies, meds, labs, vitals, immunizations, problems, procedures, care plans). However, none of this is referenced by the b(10) documentation — the b(10) export is described as using C-CDA/PDF/HTML/DICOM, not FHIR.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor describes 6 export format categories with no field-level detail:

- **Demographics** (C-CDA XML): Presumably covers patient demographic fields but no specifics given. C-CDA provides a known structure, so a developer could infer basic demographics.
- **Clinical & Billing Reports / Encounter Documentation** (PDF): The broadest and most ambiguous category. "Clinical and billing report and encounter documentation" could mean anything from a comprehensive patient chart to a clinical summary. The claim of "computable format" PDFs is unexplained — it could mean tagged/structured PDFs, PDF/A, or embedded machine-readable data.
- **Consent Forms** (HTML): Narrow scope — just consent documents.
- **Patient Attachments** (original format): Documents uploaded to the EMR, preserved in original format.
- **Patient Images** (DICOM): Medical imaging data. Appropriate for this imaging-heavy product.
- **General EHI** (HTML/PDF): A catch-all for "images, documents, reports" — overlaps with other categories.

The thinnest aspect is the complete lack of any field-level documentation for any category.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | "Patient demographics are exported in CCDA xml format" — no field enumeration | C-CDA implies standard demographics but scope unclear |
| Encounters / visits | ⚠️ Partial | "Encounter documentation" mentioned in bullet 4 (PDF) | May be in PDFs but no detail on structure or content |
| Problems / conditions / diagnoses | ❌ Not covered | Not mentioned in b(10); available via g(10) FHIR | Product stores this (per FHIR docs). Significant gap in b(10) documentation |
| Medications / prescriptions | ❌ Not covered | Not mentioned in b(10); available via g(10) FHIR | Product has e-prescribing. Significant gap |
| Allergies | ❌ Not covered | Not mentioned in b(10); available via g(10) FHIR | Product stores this. Significant gap |
| Immunizations | ❌ Not covered | Not mentioned in b(10); certified for (f)(1) immunization registries | Product stores this. Significant gap |
| Vitals | ❌ Not covered | Not mentioned in b(10); available via g(10) FHIR | Product captures vitals from monitors. Significant gap |
| Lab results | ❌ Not covered | Not mentioned in b(10); available via g(10) FHIR | Product certified for CPOE lab orders. Significant gap |
| Imaging / diagnostic reports | ✅ Covered | "Patient images are exported into DICOM format" | DICOM is the correct standard; a strength for this imaging-focused product |
| Procedures | ⚠️ Partial | May be included in "encounter documentation" PDFs | Product is procedure-center-focused; this is a core data domain. No explicit mention |
| Clinical notes / documents | ⚠️ Partial | "Clinical...report and encounter documentation" in PDF; attachments in original format | Likely included but no detail on scope or completeness |
| Care plans / goals | ❌ Not covered | Not mentioned in b(10); available via g(10) FHIR | Product stores this (per FHIR docs). Gap |
| Orders / referrals | ❌ Not covered | Not mentioned in b(10) | Product has CPOE certification. Gap |
| Insurance / coverage | ❌ Not covered | Not mentioned in b(10) | Product stores insurance data (per product research). Gap |
| Claims / billing | ⚠️ Partial | "Billing report" mentioned in bullet 4 (PDF) | Product has integrated billing with auto-CPT. "Billing report" could be comprehensive or summary-level — impossible to assess without a data dictionary |
| Payments | ❌ Not covered | Not mentioned in b(10) | Product tracks receivables/payment cycles. Gap |
| Consents / directives | ✅ Covered | "Consents form of the patient are exported in HTML format" | Explicitly mentioned |
| Patient communications / portal messages | ❌ Not covered | Not mentioned in b(10) | Product has patient portal (e)(1). Uncertain if portal messages are stored |
| Specialty-specific (vascular access, interventional radiology) | ❌ Not covered | Not mentioned in b(10) | Product's core market. Specialty assessments, access flow history, procedure-specific data not mentioned. Significant gap |

**Summary**: Of 18 applicable domains, 2 are clearly covered (imaging, consents), 4 are partially/ambiguously covered (demographics, encounters, clinical notes, billing), and 12 are not mentioned at all. The documentation is too sparse to determine whether these missing domains are actually included in the PDF/HTML exports or genuinely absent.

## 6. Documentation Quality

**Overall quality: Very poor.**

- **No data dictionary**: Zero fields, zero tables, zero entities are documented at the field level.
- **No sample data**: No example export files are provided.
- **No machine-readable schema**: No JSON schema, no XML schema, no CSV headers, nothing a developer could parse.
- **No export instructions**: No description of how to trigger, configure, or receive an export.
- **No format specification**: The claim that PDFs are in "computable format" is unexplained and undefined.
- **No relationship documentation**: No description of how exported files relate to each other.
- **No versioning**: No indication of what data elements have been added or changed.

A developer tasked with building an import system from this export would have **nothing actionable to work with**. They would need to obtain an actual export file and reverse-engineer the structure entirely. The documentation reads as a compliance checkbox — acknowledging that the b(10) requirement exists — rather than genuine technical documentation enabling data portability.

The only semi-positive note is that the vendor uses recognized standards where they do specify formats: C-CDA for demographics (a known schema) and DICOM for images (the industry standard). But even with C-CDA, no guidance is given on which C-CDA template or sections are populated.

## 7. Overall Assessment

### Classification

**Minimal/stub**: The documentation is too thin to meaningfully assess what the export covers. Six bullet points describing output formats — with zero field-level detail, no data dictionary, no sample data, and no export instructions — constitutes a stub rather than documentation.

### Key Findings

1. **The entire b(10) documentation is 6 bullet points on a web page** (`certification-page.html`). No linked data dictionary, schema, sample data, or user guide exists. This is among the thinnest EHI export documentation possible.

2. **Zero fields are documented.** There is no field-level documentation for any data domain. It is impossible to determine from the documentation alone what specific data elements are included in the export.

3. **The b(10) export is distinct from the g(10) FHIR API**, which is appropriate. The vendor uses C-CDA/PDF/HTML/DICOM rather than repackaging FHIR. However, the b(10) documentation fails to explicitly mention numerous data domains (medications, allergies, labs, vitals, immunizations, problems, care plans) that the product demonstrably stores (as evidenced by the g(10) FHIR documentation covering these domains).

4. **DICOM export for medical images is a genuine strength** for this imaging-focused product. Using the correct standard for imaging data is appropriate and commendable for a procedure center/vascular access EHR.

5. **The "computable format" PDF claim is unsubstantiated.** The vendor claims clinical and billing PDFs are in "computable format" but provides no explanation of what this means (tagged PDF, PDF/A, embedded structured data, etc.). PDF as the primary export format for structured clinical and billing data is inherently limited for data portability regardless of how "computable" it is.

### Summary Stats

```
Classification:  Minimal/stub
Export format:   Mixed (C-CDA XML, HTML, PDF, DICOM, original upload format)
Model type:      Not determinable — no data dictionary exists
Entities:        6 format-categories described (not entities in any meaningful sense)
Fields:          0 (no field-level documentation)
Descriptions:    N/A (0 fields documented)
Sample data:     No
Bulk export:     Unclear
Domains covered: 2 of 18 clearly, 4 partially, 12 not mentioned
```

### Bottom Line

Braintree Health's b(10) EHI export documentation is a minimal stub — 6 bullet points describing output formats with zero field-level detail. For a product that integrates clinical documentation, medical imaging, billing, inventory, and specialty procedure workflows across multiple modules, this documentation makes it impossible to assess whether patients or providers would receive a complete copy of their data. The DICOM image export is appropriate, but the absence of any data dictionary or specification for the clinical and billing content means this export cannot be independently verified, imported, or evaluated for completeness.
