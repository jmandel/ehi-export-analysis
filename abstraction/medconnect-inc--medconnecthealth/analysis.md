# EHI Export Analysis: MedConnect, Inc.

**Product**: MedConnectHealth 3.0
**Analysis date**: 2026-02-16
**CHPL IDs**: 9183 (15.04.04.1889.MedC.03.00.1.171212)

## 1. Product Context

MedConnectHealth 3.0 is a cloud-based, integrated EHR and practice management platform developed by MedConnect, Inc. (Montgomery, Alabama). It targets ambulatory physician practices across 25+ specialties, priced at $349/month per provider. The product is a single integrated platform combining:

- **EHR / Clinical Documentation**: Structured charts with problems, medications, allergies, immunizations, vitals, lab results, flowsheets, clinical notes (multiple documentation methods: voice recognition, point-and-click, scanning, image annotation), configurable specialty templates, care plans
- **E-Prescribing**: Surescripts-certified EPCS via DrFirst partnership, contraindication/formulary checking
- **Orders & Lab Integration**: Interfaces with LabCorp, Quest, 30+ hospitals/labs; discrete lab results populate into notes
- **Practice Management / Billing**: Full claims lifecycle (pending → submission → rework), ERA/EOB processing, eligibility checking, clearinghouse integrations (ClaimMD, Change Healthcare, Trizetto, Navicure, Waystar), direct BCBS Alabama connection, financial statements, collection letters, revenue reporting
- **Scheduling**: Multi-provider views, templates, appointment reminders
- **Patient Portal**: View/update meds, allergies, problems, demographics; view labs; request refills; messaging; online bill pay; electronic forms (registration, consent, wellness)
- **Patient Kiosk**: ID/insurance card scanning, check-in, copay collection
- **Telehealth**: Integrated video visits
- **Quality/Reporting**: 35 CQMs, population health, PI reporting
- **Interoperability**: C-CDA, DIRECT messaging, Alabama HIE, immunization registry, FHIR APIs (g)(7)–(g)(10)

This is a full-stack ambulatory platform. A complete EHI export should cover clinical documentation, billing/claims, prescriptions, orders/results, patient portal interactions, insurance/enrollment, and specialty-specific clinical data — not just a clinical summary.

## 2. Artifacts Reviewed

| Artifact | Type | Size | Description | Informativeness |
|---|---|---|---|---|
| `EHI_Export_Documentation.pdf` | PDF | 334,660 bytes, 1 page | Single-page document describing EHI export compliance and format. Created 2023-11-09 by Brett Chapman using Acrobat PDFMaker 23 for Word. | **Primary source** but extremely minimal — restates regulatory text and lists 4 export components with no field-level detail |
| `ehi-export-page.html` | HTML | 49,778 bytes | WordPress page at the registered CHPL URL. Contains heading "Electronic Health Information Export" and a single link to the PDF. Published 2023-11-09. | Minimal — just a container for the PDF link |
| `ehi-export-page-screenshot.png` | PNG | 146,612 bytes | Browser screenshot confirming the page layout. | Corroborative only |

**Verified**: The EHI export page (https://medconnecthealth.com/electronic-health-information-export/) returns HTTP 200 as of analysis date. The PDF downloads cleanly from `staging.medconnecthealth.com`. No additional EHI documentation was found on the vendor's website (confirmed by checking the HTML source and the mandatory disclosures page at /pricing/).

**Most informative artifact**: `EHI_Export_Documentation.pdf` — it is the only artifact with substantive content, but that content is a single page with two sections.

## 3. Export Mechanics

- **Format**: ZIP file containing a folder per patient/clinic with 4 components: C-CDA XML, Demographics PDF, Scanned Documents (PDF/JPG/PNG), Clinical Notes/Lab Results PDF
- **Mechanism**: 
  - **Single patient**: User-initiated, available at any time without developer assistance, restricted to specific users or system administrators
  - **Bulk/population**: Two options — (1) repeat single-patient export for each patient individually, or (2) "MedConnectHealth can perform a complete export of all patients upon request" (vendor-assisted)
- **Single-patient**: Yes
- **Bulk capability**: Yes, but vendor-assisted for the full population export
- **Access constraints**: Export restricted to identified users or system administrators
- **Fees**: Not documented in the EHI export PDF; the mandatory disclosures page was not found to specify fees for export

## 4. Export Content: What's In It

The entire export format documentation is a 4-bullet list in the PDF. There is:

- **No data dictionary** — zero field-level documentation
- **No schema files** — no XSD, no C-CDA profile constraints, no custom extensions documented
- **No sample data** — no example export files
- **No value set documentation** — no coded terminology descriptions
- **No relationship documentation** — no entity-relationship information
- **No export workflow instructions** — no screenshots or step-by-step guide

### Vendor's own content organization

The vendor describes exactly 4 export components within a per-patient folder structure:

| Component | Format | Computable | Category (vendor's) | Field Documentation |
|---|---|---|---|---|
| C-CDA (USCDI v1) | XML | Yes | Clinical Data | None (refers to USCDI v1 standard) |
| Demographics | PDF | No | Demographics | None |
| Scanned Documents | PDF, JPG, PNG | No | Documents | None |
| Clinical Notes/Lab Results | PDF | No | Clinical Data | None |

**Total entities/tables documented**: 4 export components (no further decomposition)
**Total fields documented**: 0 (no field-level documentation exists for any component)
**Fields with descriptions**: 0
**Types documented**: No
**Relationships documented**: No
**Value sets/code systems**: No

The C-CDA component is the only computable element. It follows USCDI v1, which includes: patient demographics, problems, medications, allergies, immunizations, vital signs, lab results, procedures, health concerns, goals, assessments, care team members, and clinical notes. However, the vendor provides no documentation of any customizations, extensions, or vendor-specific content beyond the USCDI v1 standard.

The remaining 3 components (Demographics PDF, Scanned Documents, Clinical Notes/Lab Results PDF) are non-computable formats. Their content, structure, and layout are entirely undocumented.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor organizes the export into two implicit categories:

1. **Clinical Data** (C-CDA XML + Clinical Notes/Lab Results PDF): The C-CDA covers the USCDI v1 clinical data slice — standard clinical summary elements. The PDF adds clinical notes and lab results in a non-computable format, but it's unclear whether this duplicates or supplements the C-CDA content.

2. **Demographics & Documents** (Demographics PDF + Scanned Documents): Basic demographics in PDF form, plus any scanned documents (images of paper records, insurance cards, etc.) in their original formats.

This is a clinical summary export with document attachments — not a native data model export. The vendor's own categories are minimal and do not distinguish between clinical, billing, administrative, or specialty data.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | Demographics PDF (non-computable); C-CDA header demographics | Demographics in PDF only; not machine-readable beyond C-CDA header fields |
| Encounters / visits | ⚠️ Partial | C-CDA may include encounter sections per USCDI v1 | Limited to what C-CDA captures; no native encounter/visit data |
| Problems / conditions | ⚠️ Partial | C-CDA problem list (USCDI v1) | Standard C-CDA only; no vendor-specific problem metadata |
| Medications / prescriptions | ⚠️ Partial | C-CDA medication list (USCDI v1) | Medication list only; no EPCS data, no prescription history, no formulary checks, no DrFirst integration data |
| Allergies | ⚠️ Partial | C-CDA allergy section (USCDI v1) | Standard C-CDA only |
| Immunizations | ⚠️ Partial | C-CDA immunization section (USCDI v1) | Standard C-CDA only |
| Vitals | ⚠️ Partial | C-CDA vital signs section (USCDI v1) | Standard C-CDA only |
| Lab results | ⚠️ Partial | C-CDA results section + Clinical Notes/Lab Results PDF | C-CDA has structured results; PDF adds non-computable view. Discrete lab data from LabCorp/Quest interfaces may not be fully represented |
| Imaging / diagnostic reports | ❌ Not covered | No evidence in export documentation | Product connects to 30+ hospitals/diagnostics; imaging data not mentioned in export |
| Procedures | ⚠️ Partial | C-CDA procedures section (USCDI v1) | Standard C-CDA only |
| Clinical notes / documents | ⚠️ Partial | Clinical Notes/Lab Results PDF + Scanned Documents | Notes exported as non-computable PDF; scanned documents preserved. Structured note data (templates, specialty-specific fields) likely lost |
| Care plans / goals | ⚠️ Partial | C-CDA care plan/goals sections (USCDI v1) | Standard C-CDA only; vendor's care plan module data not addressed |
| Orders / referrals | ❌ Not covered | No evidence in export | Product has integrated orders with lab interfaces; order data not mentioned |
| Insurance / coverage | ❌ Not covered | No evidence in export | Product stores insurance/eligibility data; none included in export |
| Claims / billing | ❌ Not covered | No evidence in export | **Major gap**: Product has full PM/billing module with claims, ERA/EOB, clearinghouse integrations |
| Payments | ❌ Not covered | No evidence in export | Product handles payment posting, copay collection, patient balances, online bill pay |
| Consents / directives | ❌ Not covered | No evidence in export | Product collects consent forms via portal/kiosk |
| Patient communications / portal messages | ❌ Not covered | No evidence in export | Product has patient portal with messaging, refill requests, appointment requests |
| E-prescribing (detailed) | ❌ Not covered | No evidence beyond C-CDA medication list | Product is Surescripts/EPCS certified; prescription transaction data not in export |

**Summary**: Of 19 applicable domains, 0 are fully covered, 9 have partial coverage via C-CDA standard sections, and 10 are not covered at all. The partial coverage for clinical domains is limited to what USCDI v1 C-CDA naturally captures — no vendor-specific extensions or native data model export.

**Largest gaps**: Billing/claims (full PM module not represented), insurance/coverage, payments, patient portal data, orders, e-prescribing detail, and consent forms. These represent entire product modules that generate patient-specific data used for care and billing decisions.

## 6. Documentation Quality

The documentation quality is extremely poor:

- **Completeness**: A single page with two sections — a restatement of the regulatory requirements and a 4-line export format description. No data dictionary, schema, sample data, value sets, field definitions, or export instructions.
- **Usability**: A developer could not build an import from this documentation alone. They would need independent C-CDA knowledge for the XML component and would have no guidance whatsoever on the PDF content structure.
- **Machine-readable artifacts**: None. No schemas, no sample exports, no API documentation.
- **Versioning**: No version number or change history (though the PDF creation date is 2023-11-09).
- **Format specification**: The format description is the 4-bullet folder structure reproduced in Section 4 — nothing more.

The document reads as a compliance checkbox: it copies the regulatory language of 170.315(b)(10), asserts compliance, and provides the minimum possible description of the export format. It does not attempt to help a recipient understand or use the exported data.

## 7. Overall Assessment

### Classification

**Minimal/stub**: The export documentation is a single page describing a C-CDA clinical summary plus PDF attachments. There is no data dictionary, no native data model export, and no coverage of billing, insurance, orders, portal data, or other non-clinical domains. The documentation is too thin to fully assess the export's actual content, but the described format (C-CDA + PDFs) is structurally incapable of covering the full breadth of data MedConnectHealth stores.

### Key Findings

1. **The export is a C-CDA/USCDI v1 clinical summary repackaged as "(b)(10)"**: The only computable element is a standard C-CDA XML document covering the USCDI v1 data set — the same clinical summary scope as (g)(10). This covers a small fraction of the product's total data (`EHI_Export_Documentation.pdf`).

2. **The entire practice management module is absent from the export**: MedConnectHealth has a full billing/PM system with claims management, ERA/EOB processing, eligibility checking, and integrations with 5+ clearinghouses. None of this data appears in the export (`EHI_Export_Documentation.pdf`, 4-component format list).

3. **Heavy reliance on non-computable PDF format**: Three of four export components (Demographics, Clinical Notes/Lab Results, Scanned Documents) are PDFs — not machine-readable. This means most exported data requires manual review or OCR to use (`EHI_Export_Documentation.pdf`).

4. **Zero field-level documentation**: No data dictionary, no schema, no sample data, no value sets. The entire format specification is 4 bullet points (`EHI_Export_Documentation.pdf`, 1 page total).

5. **Bulk export requires vendor assistance**: While single-patient export is self-service, the full population export requires MedConnectHealth to perform the export "upon request" — it is not a self-service capability for the organization (`EHI_Export_Documentation.pdf`).

### Summary Stats

```
Classification:  Minimal/stub
Export format:   C-CDA XML + PDF (in ZIP)
Model type:      Standard projection (USCDI v1 C-CDA)
Entities:        4 export components (no data dictionary)
Fields:          N/A (no field-level documentation)
Descriptions:    N/A
Sample data:     No
Bulk export:     Vendor-assisted only
Domains covered: 0 of 19 fully; 9 of 19 partially (via C-CDA)
```

### Bottom Line

MedConnectHealth's EHI export is a USCDI v1 C-CDA clinical summary with PDF attachments — functionally the same as their (g)(10) output relabeled as "(b)(10)." A patient or provider would receive a clinical snapshot (problems, meds, allergies, vitals, labs) but would not get billing records, insurance data, prescription transaction history, patient portal communications, orders, or any of the practice management data the product stores. The single biggest gap is the complete absence of the billing/PM module's data from the export, despite MedConnectHealth being an integrated EHR+PM platform.
