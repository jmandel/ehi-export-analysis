# EHI Export Analysis: Genensys LLC

**Product**: Simplify EMR v4.0
**Analysis date**: 2026-02-16
**CHPL IDs**: 10317 (15.05.05.1523.GENS.01.00.1.200225)

## 1. Product Context

Simplify EMR is a cloud-based, ONC-certified EHR and integrated practice management system developed by Genensys LLC (Oviedo, FL). The company targets small to mid-sized ambulatory practices (roughly 6 physicians or fewer), with a notable specialty focus on pediatric therapy clinics (speech, OT, PT, ABA). The product is marketed as a "fully unified" system — EHR, scheduling, billing, patient portal, and e-prescribing are integrated, not modular bolt-ons.

**Data the product stores (relevant to export completeness):**

- **Clinical documentation**: Patient charting with customizable templates, problem lists, medication lists, allergy lists, family health history, implantable device lists, clinical notes, clinical decision support data
- **Orders & prescribing**: CPOE for medications and labs, e-prescribing including controlled substances (via MDToolBox integration), medication history, formulary data
- **Lab integration**: Electronic lab ordering and results with trending, abnormal result alerts
- **Practice management / billing**: Enterprise scheduling, billing/claims management, rules-based claims editing, eligibility checks, authorization management, revenue cycle management (AR, denial management, credentialing)
- **Patient portal**: Secure messaging, online bill pay, appointment requests, prescription renewal requests, lab results viewing
- **Interoperability**: C-CDA exchange, Direct messaging, FHIR APIs, public health reporting (immunization registries, syndromic surveillance)
- **Specialty features**: Pediatric therapy-specific templates, dashboards, and workflows (Simplify Therapy variant)

This is a product that stores substantial data across clinical, billing, and patient engagement domains. A complete EHI export should cover all of these.

## 2. Artifacts Reviewed

| Artifact | Size | Description | Informativeness |
|---|---|---|---|
| `ehi-export-doc.txt` | 831 bytes | Plain text export of the Google Doc — the entirety of the vendor's EHI export documentation | **Primary source** — but extremely minimal |
| `ehi-export-doc.pdf` | 39,194 bytes (2 pages) | PDF version of the same Google Doc, titled "Simplify EMR b(10) Export Format" | Same content as .txt, confirms 2-page document |
| `ehi-export-doc.docx` | 7,838 bytes | DOCX version preserving original formatting and a hyperlink to USCDI v1 errata PDF | Same content; confirms the USCDI v1 reference |
| `google-doc-screenshot.png` | 70,721 bytes | Screenshot of Google Doc title page showing "Simplify EMR / Export Format" heading | Confirms document structure: title page only |
| `google-doc-screenshot-page2.png` | 131,491 bytes | Screenshot of content page showing All Patient Mode and Single Patient Mode descriptions | **Most informative** — confirms exact content and hyperlink to USCDI v1 errata |

**Verification notes:**
- Confirmed the Google Doc is still accessible at the registered URL (title "Simplify EMR b(10) Export Format" visible in fetch response).
- Confirmed the mandatory disclosures page at `genensys.com/mu-disclosure/` lists (b)(10) certification but provides no additional export documentation.
- The plain text export is 831 bytes (808 bytes of actual content excluding trailing whitespace). This is the entire vendor-provided EHI export specification.

## 3. Export Mechanics

- **Format**: USCDI v1 C-CDA XML (one file per patient) + PDF/HTML files for encounter notes and patient documents
- **Mechanism**: Not documented. The Google Doc describes the output format but provides no instructions on how to initiate the export (no UI screenshots, no API endpoints, no step-by-step guide).
- **Single-patient capability**: Yes — "Single Patient Mode" produces a folder named `Lastname_FirstName_patientId_Date`
- **Bulk capability**: Yes — "All Patient Mode" produces a ZIP file `Patient_export_{date}.zip` containing one folder per patient
- **Access constraints or fees**: The mandatory disclosures page states "no additional costs for the certified functionality." No fees specifically mentioned for the export.

## 4. Export Content: What's In It

The entire export documentation is 831 bytes of text describing **only the folder/file structure**. There is no data dictionary, no field definitions, no schema, no sample data.

The export consists of three components per patient:

### Vendor's own content organization

| Component | Format | Documentation Detail | Description |
|---|---|---|---|
| C-CDA XML file | XML (USCDI v1 C-CDA) | Name convention only: `Lastname_FirstName_ccda.xml` | "CCDA File Conformant to USCDI v1" — no field-level documentation; vendor references USCDI-Version-1-July-2020-Errata-Final_0.pdf |
| Encounters subfolder | PDF or HTML files | Name convention only: `{encounterId}_{date}.pdf` or `.html` | "All Visit Notes in PDF or HTML Format (0 to many)" — no specification of what note types, what content |
| Patient Documents subfolder | PDF or HTML files | Name convention only: `{documentId}_{date}.pdf` or `.html` | "Other Documents in PDF Format or HTML Format (0 to many)" — no specification of document types |

**There is no data dictionary.** Zero fields are documented. Zero types are specified. Zero relationships are described. Zero value sets are defined. The vendor provides no information about what data elements actually appear in the C-CDA beyond claiming "Conformant to USCDI v1."

Based on the USCDI v1 standard (which the vendor references), the C-CDA would be expected to contain data classes including: Patient Demographics, Allergies and Intolerances, Assessment and Plan of Treatment, Care Team Members, Clinical Notes, Goals, Health Concerns, Immunizations, Lab Results, Medications, Problems, Procedures, Provenance, Smoking Status, Implantable Device Identifiers, and Vital Signs. However, without sample data or field-level documentation, it is impossible to verify what Simplify EMR actually includes in its C-CDA exports or how complete the mapping is.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor describes exactly three output components, with no categorization or data domain organization:

1. **C-CDA XML**: A standard clinical summary conformant to USCDI v1. This would cover the ~16 USCDI v1 data classes if fully implemented, but the vendor provides no specifics about their implementation.

2. **Encounter notes (PDF/HTML)**: Unstructured document dumps of visit notes. These may capture clinical narrative beyond what's in the C-CDA, but the data is not structured or machine-readable.

3. **Patient documents (PDF/HTML)**: Other documents in the patient record. No specification of what types of documents this includes.

The vendor provides no structured export of their native database tables. There is no mention of billing data, scheduling data, portal messages, e-prescribing transaction data, or specialty-specific structured data. The entire export is a C-CDA clinical summary plus document images.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | C-CDA USCDI v1 includes demographics, but no field-level documentation from vendor | USCDI v1 demographics are limited; product stores more than C-CDA carries |
| Encounters / visits | ⚠️ Partial | Encounter notes as PDF/HTML files; C-CDA may include encounter data | Encounter metadata is in C-CDA; clinical notes exported as unstructured PDFs lose structured data |
| Problems / conditions | ⚠️ Partial | Expected in C-CDA USCDI v1 | Standard C-CDA coverage only; no verification possible |
| Medications / prescriptions | ⚠️ Partial | Expected in C-CDA USCDI v1 | C-CDA carries medication list but not full e-prescribing transaction history, formulary data, or MDToolBox integration data. Product has extensive e-prescribing; significant gap likely. |
| Allergies | ⚠️ Partial | Expected in C-CDA USCDI v1 | Standard C-CDA coverage only |
| Immunizations | ⚠️ Partial | Expected in C-CDA USCDI v1 | Standard C-CDA coverage only |
| Vitals | ⚠️ Partial | Expected in C-CDA USCDI v1 | Standard C-CDA coverage only |
| Lab results | ⚠️ Partial | Expected in C-CDA USCDI v1 | C-CDA carries results but not ordering workflow, trending data, task assignments, or historical comparisons the product stores |
| Procedures | ⚠️ Partial | Expected in C-CDA USCDI v1 | Standard C-CDA coverage only |
| Clinical notes / documents | ⚠️ Partial | Encounter notes + patient documents as PDF/HTML; some notes in C-CDA | Notes are exported but as unstructured documents, losing all structured/coded data from templates |
| Care plans / goals | ⚠️ Partial | Expected in C-CDA USCDI v1 | Standard C-CDA coverage only |
| Orders / referrals | ⚠️ Partial | Medication and lab orders may appear in C-CDA | CPOE order details, referral workflows likely not fully captured in C-CDA |
| Insurance / coverage | ❌ Not covered | No mention in export documentation | Product stores eligibility, authorization, and insurance data; significant gap |
| Claims / billing | ❌ Not covered | No mention in export documentation | Product has full billing/claims/RCM; this is a major gap |
| Payments | ❌ Not covered | No mention in export documentation | Product supports online bill pay and payment processing; gap |
| Patient communications / portal messages | ❌ Not covered | No mention in export documentation | Product has patient portal with messaging; gap |
| Specialty-specific (pediatric therapy) | ❌ Not covered | No structured export of therapy-specific data | Product has therapy-specific templates, dashboards, and assessments (OT/PT/speech/ABA); significant gap |
| Imaging / diagnostic reports | ⚠️ Partial | May appear in C-CDA or patient documents subfolder | No documentation to confirm |
| Consents / directives | ⚠️ Partial | May appear in patient documents subfolder | No documentation to confirm |

**Summary**: Clinical domains marked ⚠️ Partial because C-CDA USCDI v1 provides some coverage, but (a) the vendor provides zero verification of what they actually include, and (b) C-CDA is inherently a summary — it cannot carry the full depth of data the product stores. All non-clinical domains (billing, insurance, payments, portal messages) and specialty data are completely absent.

## 6. Documentation Quality

The documentation quality is **extremely poor** — among the worst possible for a certified product.

- **Total documentation**: 831 bytes of plain text (2 PDF pages, of which page 1 is just a title)
- **Data dictionary**: None
- **Field definitions**: None (zero fields documented)
- **Types**: None
- **Relationships**: None
- **Value sets**: None
- **Sample data**: None
- **Machine-readable schema**: None
- **Export instructions**: None (no UI guide, no API documentation for the export)
- **Error handling**: None

The documentation describes only the file/folder naming conventions for the export output. A developer receiving this export would know that they'll get a C-CDA XML file and some PDFs, but would have no vendor-specific guidance on what data is in the C-CDA, what types of encounter notes exist, what document categories appear, or how to map any of it.

The sole external reference is to the USCDI v1 errata PDF, which describes the C-CDA standard in general — not what Simplify EMR's specific implementation includes.

**Could a developer build an import from this documentation?** Only to the extent that they can parse generic USCDI v1 C-CDA XML — which is standard-based work, not vendor-specific documentation. For the PDF/HTML documents, they would have no structured metadata beyond filenames.

## 7. Overall Assessment

### Classification

**Standard-based projection**

The export is a USCDI v1 C-CDA clinical summary plus unstructured document dumps. There is no native data model export. The C-CDA covers a subset of clinical data; billing, scheduling, patient portal, e-prescribing workflow, and specialty therapy data are entirely absent. This is essentially the vendor's existing C-CDA creation capability (certified under (g)(6)) repackaged with a folder of PDF documents and labeled as a (b)(10) export.

### Key Findings

1. **The entire EHI export documentation is 831 bytes.** Two PDF pages (one is a title page) describing only folder structure and file naming conventions. No data dictionary, no field definitions, no sample data, no export instructions. This is among the most minimal documentation possible for a certified product.

2. **The export is C-CDA repackaging, not a native data export.** The (b)(10) export consists of a USCDI v1 C-CDA XML file per patient plus PDF/HTML encounter notes and documents. This is functionally the same as the vendor's (g)(6) Consolidated CDA Creation capability with document attachments — not a genuine "all EHI" export.

3. **Billing, insurance, and practice management data are completely absent.** The product is a fully integrated EHR + practice management system with billing, claims, eligibility, authorization, and revenue cycle management. None of this data is mentioned in the export. C-CDA cannot carry this data.

4. **Specialty therapy data has no structured export.** The vendor's core market is pediatric therapy clinics with specialty-specific templates, assessments, and dashboards. None of this structured clinical data is specifically addressed. Therapy assessments may appear as flat PDF documents, losing all structured/coded data.

5. **No verification is possible.** Without sample data, field-level documentation, or a schema, it is impossible to verify what the C-CDA actually contains or how complete the export is. The vendor asks users to trust "Conformant to USCDI v1" with no supporting evidence.

### Summary Stats

```
Classification:  Standard-based projection
Export format:   C-CDA XML + PDF/HTML documents
Model type:      Standard projection (USCDI v1 C-CDA) + document dump
Entities:        3 (C-CDA file, encounters folder, documents folder)
Fields:          N/A (no data dictionary)
Descriptions:    N/A (0 fields documented)
Sample data:     No
Bulk export:     Yes (All Patient Mode produces ZIP)
Domains covered: 0 of 17 fully covered; ~12 partially via C-CDA; 5 not covered at all
```

### Bottom Line

This export is a C-CDA clinical summary repackaged as a (b)(10) export, supplemented by unstructured PDF/HTML document dumps. A patient or provider would get a basic clinical summary and copies of visit notes, but would **not** get billing records, insurance data, e-prescribing transaction history, patient portal messages, or structured specialty therapy assessments. The documentation is so minimal (831 bytes, zero field definitions) that it provides no basis for verifying completeness or building an import. The single biggest gap is the complete absence of billing and practice management data from a product that is marketed as a unified EHR + PM system.
