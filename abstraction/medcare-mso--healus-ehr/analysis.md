# EHI Export Analysis: Medcare MSO

**Product**: HealUs EHR v1.0
**Analysis date**: 2026-02-16
**CHPL IDs**: 15.05.05.3197.MDCR.01.00.1.240715

## 1. Product Context

HealUs EHR is a cloud-based ambulatory EHR developed by Medcare MSO, a medical billing and revenue cycle management company. The product was ONC-certified in July 2024 and is broadly certified across 37 criteria including CPOE (medications, labs, imaging), e-prescribing (via DrFirst), clinical information reconciliation, patient portal, clinical quality measures, immunization registry reporting, syndromic surveillance, and FHIR API access.

The product sits within a broader Medcare MSO ecosystem that includes **Maximus** (a separate practice management and billing platform), AI Scribe, and AI Medical Coding. HealUs EHR handles clinical workflows; billing and claims management appear to be handled by the separate Maximus PMS. The boundary between products is not clearly documented, which affects the scope assessment: billing data may live in Maximus rather than HealUs EHR itself.

Key data the product stores based on certification criteria and marketing: patient demographics, medication orders/e-prescriptions, lab/imaging/procedure orders, allergy lists, immunization records, problem lists, clinical notes/charting, encounters, referrals, advance directives, CQM data (7 measures), and patient portal content. Scheduling, eligibility verification, and clinical decision support are also described on the website.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/EHI.pdf` (681 KB, 6 pages) | The complete (b)(10) EHI export documentation. Lists 11 data categories and their export formats. Provides step-by-step export instructions. Contains zero field-level documentation. | **Primary source** — but thin |
| `downloads/fhir-capability-statement.json` (27 KB) | FHIR R4 CapabilityStatement from `fhirapi.medcaremso.com`. Shows 27 resource types, all standard US Core. Instantiates `us-core-server` and `bulk-data` capability statements. | **Useful** — confirms FHIR scope is standard (g)(10) |
| `downloads/screenshot-ehi-page.png` (171 KB) | Screenshot of the Angular SPA knowledge hub showing the PDF embedded in a viewer. | **Minimal value** — confirms the docs site layout |

No data dictionary, sample data, schema files, or field-level documentation of any kind were found. The EHI documentation consists entirely of the single 6-page PDF.

## 3. Export Mechanics

- **Format(s)**: Mixed — C-CDA XML, FHIR R4 JSON, CSV, and PDF. Most data categories (7 of 11) are exported only as PDF.
- **Mechanism**: UI-driven. Users navigate to "Data Export" in the EHR, select patient(s) and date range, choose sections, and download. Practice administrators can approve export requests.
- **Single-patient**: Yes — documented workflow (EHI.pdf p.4).
- **Bulk export**: Yes — same workflow with multi-patient selection (EHI.pdf p.4). FHIR Bulk Data also available.
- **Access constraints**: Requires practice administrator approval for export access. Optional password protection on export files.
- **Fees**: Not mentioned.
- **Timeliness**: Document states files are exported "in real time" without developer assistance.

## 4. Export Content: What's In It

### No data dictionary

The EHI documentation provides **zero field-level detail**. There are no field names, no data types, no column specifications for the CSV exports, no description of what data appears in the PDF exports, and no documentation of any vendor-specific C-CDA or FHIR extensions. The documentation operates at the category level only.

### Vendor's own content organization

The PDF describes 11 export categories. Since there is no data dictionary, the "Fields" and "Described" columns are N/A for all entries.

| Entity/Category | Format | Fields | Described | Types | Source |
|---|---|---|---|---|---|
| Patient Demographics | CSV | N/A | N/A | N/A | EHI.pdf p.4 |
| Appointments | PDF, CSV | N/A | N/A | N/A | EHI.pdf p.4 |
| Lab Results | PDF | N/A | N/A | N/A | EHI.pdf p.4 |
| Imaging Results | PDF | N/A | N/A | N/A | EHI.pdf p.4 |
| Procedure Results | PDF | N/A | N/A | N/A | EHI.pdf p.4 |
| Encounters | PDF | N/A | N/A | N/A | EHI.pdf p.5 |
| Referrals | PDF | N/A | N/A | N/A | EHI.pdf p.5 |
| Advance Directives | PDF | N/A | N/A | N/A | EHI.pdf p.5 |
| Documents | PDF | N/A | N/A | N/A | EHI.pdf p.5 |
| Clinical Data (C-CDA) | C-CDA XML | N/A | N/A | N/A | EHI.pdf p.3 |
| Clinical Data (FHIR) | FHIR R4 JSON | N/A | N/A | N/A | EHI.pdf p.3 |

### FHIR resource types (from CapabilityStatement)

The FHIR export supports 27 resource types, all standard US Core with no vendor-specific resources or extensions:

AllergyIntolerance, CarePlan, CareTeam, Condition, Coverage, Device, DiagnosticReport, DocumentReference, Encounter, Endpoint, Goal, Group, Immunization, Location, Medication, MedicationDispense, MedicationRequest, Observation, Organization, Patient, Practitioner, PractitionerRole, Procedure, Provenance, RelatedPerson, ServiceRequest, Specimen.

This is the standard US Core 6.1.0 resource set — identical to what a (g)(10) standardized API would expose. The CapabilityStatement explicitly instantiates the `us-core-server` and `bulk-data` capability statements.

### PDF export concerns

Seven of eleven export categories use PDF as the sole format. While the documentation describes these as "interpretable, machine-readable PDF," PDF is a presentation format — not a computable data format. Lab results, imaging results, procedure results, encounters, referrals, advance directives, and documents are all PDF-only. This means a recipient would need to visually read or OCR-parse these exports to extract structured data.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor organizes the export into 11 categories spanning demographics (CSV), appointments (PDF+CSV), clinical results (PDF), clinical encounters and referrals (PDF), documents (PDF), and clinical summary data (C-CDA and FHIR). The documentation is uniformly thin across all categories — every category gets a single sentence saying it provides "a comprehensive view of [X]" with no further detail.

The FHIR/C-CDA components cover the standard USCDI clinical data (problems, medications, allergies, immunizations, vitals, care plans, etc.). The additional PDF categories (encounters, referrals, advance directives, documents) represent a modest attempt to go beyond USCDI, though in a non-computable format.

No billing, insurance, claims, charges, or payment data is mentioned anywhere in the documentation.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | "Patient Demographics" CSV (no column spec) | CSV export exists but fields are completely undocumented |
| Encounters / visits | ⚠️ Partial | "Encounters" PDF; Encounter in FHIR | PDF is not computable; FHIR Encounter covers USCDI only |
| Problems / conditions | ⚠️ Partial | Condition in FHIR; C-CDA Problem List | Covered via standard C-CDA/FHIR — no vendor-specific depth |
| Medications / prescriptions | ⚠️ Partial | MedicationRequest/Medication in FHIR; C-CDA Medications | Standard USCDI scope only. E-prescribing details (DrFirst) not mentioned |
| Allergies | ⚠️ Partial | AllergyIntolerance in FHIR; C-CDA | Standard scope |
| Immunizations | ⚠️ Partial | Immunization in FHIR; C-CDA | Standard scope |
| Vitals | ⚠️ Partial | Observation in FHIR; C-CDA | Standard scope |
| Lab results | ⚠️ Partial | "Lab Results" PDF; DiagnosticReport/Observation in FHIR | PDF not computable; FHIR covers USCDI scope only |
| Imaging / diagnostic reports | ⚠️ Partial | "Imaging Results" PDF; DiagnosticReport in FHIR | PDF not computable |
| Procedures | ⚠️ Partial | "Procedure Results" PDF; Procedure in FHIR | PDF not computable |
| Clinical notes / documents | ⚠️ Partial | "Documents" PDF; DocumentReference in FHIR; C-CDA | Documents exported as PDF copies. Document metadata undocumented |
| Care plans / goals | ⚠️ Partial | CarePlan, Goal in FHIR; C-CDA | Standard scope only |
| Orders / referrals | ⚠️ Partial | "Referrals" PDF; ServiceRequest in FHIR | PDF not computable |
| Insurance / coverage | ⚠️ Partial | Coverage resource in FHIR CapabilityStatement | FHIR has Coverage resource, but EHI PDF doesn't mention insurance data |
| Claims / billing | ❌ Not covered | No billing entities in export | Product's parent company (Medcare MSO) is a billing company; billing may reside in separate Maximus PMS rather than HealUs EHR |
| Payments | ❌ Not covered | No payment data in export | Same as above — likely in Maximus PMS |
| Consents / directives | ⚠️ Partial | "Advance Directives" PDF | PDF only, no structured data |
| Patient communications | ❌ Not covered | No portal messages or communications in export | Product has patient portal (e)(1) but communications not exported |
| Specialty-specific | N/A | — | Product is general ambulatory EHR; no specialty-specific modules identified |

**Gap analysis summary**: The export's clinical coverage maps closely to USCDI via standard C-CDA and FHIR, supplemented by PDF exports of additional data categories. All domains rated "Partial" because while data is nominally present, it is either (a) in PDF-only format making it non-computable, or (b) limited to standard USCDI scope with no evidence of deeper vendor-specific field coverage. Billing and payment data are absent, but this may be appropriate if that data resides in the separate Maximus PMS rather than HealUs EHR. Patient communications are absent despite the product having a patient portal.

## 6. Documentation Quality

The documentation is **very poor**:

- **No data dictionary**: Zero field names, types, descriptions, or value sets documented for any export format.
- **No CSV specification**: The CSV exports for demographics and appointments have no column headers or field definitions.
- **No C-CDA/FHIR customization documentation**: No vendor-specific templates, extensions, or profiles beyond the base standards.
- **No sample data**: No example export files provided.
- **No schema files**: No XSD, JSON Schema, OpenAPI, or CSV header specifications.
- **No relationships**: No documentation of how exported entities relate to each other.

**Could a developer use this?** No. A developer receiving this documentation would know that an export capability exists and what formats it uses, but would have no idea what specific data fields will appear. They would need to request an actual export and reverse-engineer the structure. For PDF exports (7 of 11 categories), they would face the additional challenge of parsing presentation-formatted documents into structured data.

The documentation reads as a compliance checkbox — it demonstrates that an export mechanism exists for certification purposes, but provides insufficient detail for practical data portability.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Minimal/stub/unclear**

The documentation is too thin to assess actual field-level coverage. At the category level, the export lists 11 data categories that collectively touch most clinical domains the product stores. However, 7 of 11 categories export as PDF only (non-computable), and the computable components (C-CDA, FHIR) are standard USCDI scope with no evidence of vendor-specific depth. There is no billing data, no patient communications, and no data dictionary to verify what fields any category actually includes. The lack of field-level documentation makes it impossible to confirm whether the export covers the full designated record set or merely a surface-level clinical summary.

**Axis 2 — Export approach: Repackaged existing export**

The evidence strongly points to repackaging of existing capabilities:

1. The FHIR export is explicitly the (g)(10) standardized API — the CapabilityStatement instantiates `us-core-server` and `bulk-data` with 27 standard US Core resource types and zero vendor extensions.
2. The C-CDA export references the standard HL7 CDA R2 IHE Health Story Consolidation spec with no product-specific customizations.
3. The additional PDF/CSV categories (demographics, appointments, results, encounters, referrals, directives, documents) may represent some modest effort beyond (g)(10), but PDF exports are not a purpose-built computable data export.
4. No product-specific data dictionary exists — the vendor references the generic C-CDA and FHIR specifications rather than documenting their own data model.
5. The 6-page PDF documentation is perfunctory, with no indication of engineering effort specific to (b)(10).

### Key Findings

1. **No data dictionary exists.** The entire EHI documentation is a 6-page PDF with zero field-level definitions for any export format. This is the weakest possible documentation for a (b)(10) export. (Source: `downloads/EHI.pdf`)

2. **7 of 11 export categories are PDF-only.** Lab results, imaging results, procedure results, encounters, referrals, advance directives, and documents are exported exclusively as PDF — a presentation format, not a computable data format. (Source: `downloads/EHI.pdf` p.3-5)

3. **The FHIR export is the standard (g)(10) API.** The CapabilityStatement shows 27 US Core resource types with no vendor-specific resources or extensions. It instantiates `us-core-server` and `bulk-data` capability statements — this is the (g)(10) API relabeled as (b)(10). (Source: `downloads/fhir-capability-statement.json`)

4. **No billing or payment data is in the export.** This is notable given Medcare MSO's primary business is medical billing/RCM. However, billing likely resides in the separate Maximus PMS product rather than HealUs EHR, making this potentially appropriate scope. (Source: `downloads/EHI.pdf` — billing not mentioned; `product-research.md` — Maximus described as separate billing platform)

5. **CSV exports are undocumented.** Demographics and appointments have CSV export but with no column specification, making them theoretically computable but practically opaque. (Source: `downloads/EHI.pdf` p.4)

### Summary Stats

    Coverage:        Minimal/stub/unclear
    Approach:        Repackaged existing export
    Export format:   Mixed (C-CDA XML, FHIR R4 JSON, CSV, PDF)
    Entities:        11 categories (no field-level breakdown)
    Fields:          N/A (no data dictionary)
    Descriptions:    N/A
    Sample data:     No
    Bulk export:     Yes (multi-patient and FHIR Bulk Data)
    Domains covered: 0 fully covered; ~12 partially covered of 15 applicable domains

### Bottom Line

HealUs EHR's EHI export is a minimal compliance effort: a 6-page PDF with no data dictionary, heavy reliance on non-computable PDF format for most data categories, and a FHIR component that is the standard (g)(10) API relabeled. A patient or provider would receive PDF documents and standard C-CDA/FHIR clinical summaries, but no structured, comprehensive export of the full designated record set. The single biggest gap is the complete absence of field-level documentation — without performing an actual export and reverse-engineering the output, it's impossible to know what data is actually included.
