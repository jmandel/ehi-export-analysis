# EHI Export Analysis: Ulrich Medical Concepts

**Product**: Team Chart Concept (TCC) v7.1
**Analysis date**: 2026-02-16
**CHPL IDs**: 15.05.05.3049.UL15.01.00.1.191226 (CHPL #10227)

## 1. Product Context

Team Chart Concept (TCC) is an integrated EHR and practice management system developed by Ulrich Medical Concepts (UMC), a small vendor (~22 employees, ~$1.4M revenue) based in Paducah, Kentucky. The product serves ambulatory practices across primary care, internal medicine, dermatology, OB/GYN, general surgery, urgent care, and therapy. It was certified on 2019-12-26 for 29 ONC criteria including (b)(10).

TCC is described as a "full-featured suite" combining:
- **Clinical EHR**: encounter notes, problem lists, medications, allergies, immunizations, vitals, implantable device lists, health maintenance alerts, clinical decision support, quality measures
- **Practice management & billing**: appointment scheduling, integrated billing with "full HIPAA compliant billing routines," SmartCoder claims scrubbing, ICD-10, PQRS, financial reporting
- **Orders**: CPOE for medications, labs, and diagnostic imaging; bi-directional lab connectivity
- **E-prescribing**: via NewCrop (DrFirst) integration (add-on)
- **Document management**: scanned documents, office forms, digitized historical records
- **Patient engagement**: patient portal via Medfusion (add-on), Bridge partnership for communications
- **Interoperability**: C-CDA, Direct messaging, HL7, FHIR API via EMR Direct Interoperability Engine (add-on)

UMC also provides medical billing services, making billing a core competency. The product's integrated PM/billing capabilities make missing billing data in the export a significant gap.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/cost-disclosure-and-transparency.html` (104 KB) | Vendor's mandatory ONC disclosure page. Contains the **entire** (b)(10) documentation: a single sentence footnote. Lists 29 certified criteria, cost information, and links to API docs. | **Primary source** — confirmed the EHI export documentation is a single sentence |
| `downloads/cost-disclosure-and-transparency-page.png` (670 KB) | Full-page screenshot of the disclosure page | Corroborates HTML content |
| `downloads/fhirR4endpoints-umc.json` (99 bytes) | FHIR R4 endpoint directory for UMC customers | Confirms zero active FHIR integrations — an empty Bundle with no entries |
| `downloads/interopengine-open-api-documentation.html` (35 KB) | EMR Direct's generic FHIR R4 API documentation for (g)(10) | Not UMC-specific; covers OAuth 2.0, SMART App Launch, US Core. Unrelated to (b)(10) |

No data dictionary, schema, sample data, user guide, or any technical documentation about the EHI export exists among the artifacts. The prior report's claim about a 2025 RWT plan PDF with additional detail was not available in downloads but its content was summarized in `ehi-export-report.md`.

## 3. Export Mechanics

- **Format**: PDF and/or C-CDA files
- **Mechanism**: UI-based "chart export routine" within the TCC application, initiated by an authorized user
- **Single-patient**: Yes — select a patient and run the export
- **Bulk capability**: Yes — retrieve a list of patients and export each patient's chart
- **Output**: Files saved to a user-specified folder on the local filesystem
- **Access constraints**: Requires user permission ("permission to complete a chart export")
- **Fees**: Not mentioned on the disclosure page; the export appears to be a built-in feature

The complete documentation of how the export works is:

> *EHI can be exported in PDF or C-CDA format. Records for a patient are exported to one or more PDF/C-CDA files. The files created by the export are saved to a folder specified by the user.*

## 4. Export Content: What's In It

### No data dictionary exists

There is **zero** structured documentation of what the export contains. No entities, tables, fields, types, descriptions, relationships, value sets, or sample data are documented anywhere in the vendor's public-facing materials.

The vendor provides no:
- Data dictionary or field listing
- Schema definition (JSON, XML, or otherwise)
- Sample export files
- C-CDA template conformance documentation
- Description of what data is included or excluded

### What can be inferred

Based solely on the stated formats:

1. **PDF export**: Likely a rendered view of the patient chart — whatever the EHR displays. PDFs are not computable and cannot preserve structured data. Field-level content is unknowable without a sample.

2. **C-CDA export**: If this uses the same C-CDA generated for Transitions of Care (b)(1), it would follow standard CCD/CCD-A templates covering USCDI-scope data: demographics, problems, medications, allergies, immunizations, vitals, procedures, results, care team. C-CDA has no standard representation for billing, scheduling, custom forms, or many specialty data types.

### Vendor's own content organization

No vendor-organized content categories exist. The vendor does not describe, categorize, or enumerate any exported data.

| Entity/Table | Fields | Described | Types | Category (vendor's) |
|---|---|---|---|---|
| *(none documented)* | — | — | — | — |

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor provides no content documentation whatsoever. The export is described only by its output format (PDF or C-CDA). There are no categories, modules, sections, or entities described. Assessment of coverage is impossible based on available documentation.

The C-CDA component, if it follows standard CCD templates, would implicitly cover USCDI-scope clinical data. The PDF component is a black box — it could contain anything visible in the chart view, but nothing is documented.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | Likely in C-CDA (standard section) and PDF; no documentation confirms | Product stores demographics (certified (a)(5)); probably exported but undocumented |
| Encounters / visits | ⚠️ Partial | Likely in C-CDA encounters section; undocumented | Product does encounters; probably partially covered via C-CDA |
| Problems / conditions | ⚠️ Partial | Likely in C-CDA problem list section; undocumented | Product stores problem lists; probably covered via C-CDA |
| Medications / prescriptions | ⚠️ Partial | Likely in C-CDA medications section; undocumented | Product does e-prescribing via NewCrop; C-CDA may not capture full Rx history |
| Allergies | ⚠️ Partial | Likely in C-CDA allergies section; undocumented | Product stores allergies; probably covered via C-CDA |
| Immunizations | ⚠️ Partial | Likely in C-CDA immunizations section; undocumented | Product stores immunizations; probably covered via C-CDA |
| Vitals | ⚠️ Partial | Likely in C-CDA vital signs section; undocumented | Product stores vitals; probably covered via C-CDA |
| Lab results | ⚠️ Partial | Likely in C-CDA results section; undocumented | Product has bi-directional lab connectivity; probably partially covered |
| Imaging / diagnostic reports | ⚠️ Partial | May appear in C-CDA or PDF; undocumented | Product has imaging CPOE; results coverage unknown |
| Procedures | ⚠️ Partial | Likely in C-CDA procedures section; undocumented | Product stores procedures; probably covered via C-CDA |
| Clinical notes / documents | ⚠️ Partial | PDF may render notes; C-CDA notes section possible; undocumented | Product stores encounter notes; coverage depth unknown |
| Care plans / goals | ❌ Not covered | No evidence | Product may store care plans; no documentation of export |
| Orders / referrals | ❌ Not covered | No evidence beyond what C-CDA may include | Product has CPOE for meds, labs, imaging; order detail likely lost in C-CDA |
| Insurance / coverage | ❌ Not covered | Not a standard C-CDA section; no evidence | Product stores insurance data (integrated PM); significant gap |
| Claims / billing | ❌ Not covered | Not a standard C-CDA section; no evidence | Product has integrated billing with claims scrubbing; **major gap** given billing is a core function |
| Payments | ❌ Not covered | No evidence | Product handles billing/financial; significant gap |
| Consents / directives | ❌ Not covered | May be in C-CDA advance directives section; undocumented | Unknown |
| Patient communications | ❌ Not covered | No evidence | Product has patient portal (Medfusion) and Bridge communications; gap if data stored |
| Specialty-specific data | ❌ Not covered | No evidence | Product serves dermatology, OB/GYN, surgery, therapy — specialty templates likely exist but are undocumented |

**Note**: All "⚠️ Partial" ratings above are **inferred** from the fact that C-CDA is a stated export format, not from any vendor documentation. The vendor does not confirm that any specific data domain is included. Without sample exports or a data dictionary, these are assumptions based on C-CDA standard capabilities.

## 6. Documentation Quality

The documentation quality is **effectively nonexistent**:

- **Data dictionary**: None
- **Field-level documentation**: None (0 fields documented)
- **Types/constraints**: None
- **Relationships**: None
- **Value sets**: None
- **Sample data**: None
- **Schema**: None
- **User guide**: None (no instructions for performing the export)
- **Machine-readable artifacts**: None

A developer could not build an import from this documentation. A patient could not understand what data they would receive. The entire (b)(10) documentation is 34 words in a footnote on a compliance disclosure page.

The (g)(10) API documentation (EMR Direct Interoperability Engine) is a separate, generic third-party document unrelated to the EHI export. The FHIR endpoints JSON shows zero active customer integrations.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Minimal/stub/unclear**

The documentation is far too thin to assess actual coverage. There is no data dictionary, no field listing, no sample data, and no description of what data domains are included or excluded. The stated export formats (PDF and C-CDA) are inherently limited: PDF is non-computable and C-CDA covers only USCDI-scope clinical summaries. For a product with integrated practice management and billing — which the vendor highlights as a core capability — the absence of any billing, claims, scheduling, or financial data in the export (or at least in its documentation) is a significant red flag. The entire documentation is a single footnote.

**Axis 2 — Export approach: Repackaged existing export**

The export uses PDF (a chart printout) and C-CDA (the same format used for Transitions of Care (b)(1) compliance). There is no evidence of any purpose-built EHI export mechanism. The C-CDA component was almost certainly built for (b)(1) and reused for (b)(10). No additional data domains beyond what C-CDA standard sections provide are documented. The RWT plan's success criterion — "if a PDF is generated" — confirms this is a compliance checkbox, not a genuine EHI export effort.

### Key Findings

1. **Single-sentence documentation**: The entire (b)(10) EHI export documentation is 34 words in a footnote: "*EHI can be exported in PDF or C-CDA format. Records for a patient are exported to one or more PDF/C-CDA files. The files created by the export are saved to a folder specified by the user.*" (`cost-disclosure-and-transparency.html`)

2. **No data dictionary at all**: Zero entities, zero fields, zero descriptions. There is no structured documentation of what the export contains. This is among the most minimal (b)(10) documentation possible.

3. **Billing data almost certainly missing**: TCC is an integrated EHR+PM system with billing as a core function. Neither PDF nor C-CDA can represent billing, claims, payments, or financial data. No vendor documentation suggests these domains are exported.

4. **C-CDA likely repackaged from (b)(1)**: The vendor is certified for both (b)(1) Transitions of Care (which requires C-CDA) and (b)(10). The C-CDA export is almost certainly the same artifact serving both criteria, covering only USCDI-scope clinical summary data.

5. **Zero active FHIR integrations**: The FHIR endpoints JSON (`fhirR4endpoints-umc.json`) contains an empty Bundle with no entries, indicating no UMC customers have active API integrations. Combined with the RWT results noting "No customers opted to implement" for API measures, this suggests very low adoption of interoperability features.

### Summary Stats

```
Coverage:        Minimal/stub/unclear
Approach:        Repackaged existing export
Export format:   PDF, C-CDA
Entities:        0 (no data dictionary)
Fields:          0 (no data dictionary)
Descriptions:    N/A
Sample data:     No
Bulk export:     Yes (multi-patient via patient list)
Domains covered: 0 confirmed (up to ~10 inferred from C-CDA standard sections, but unverified)
```

### Bottom Line

Team Chart Concept's (b)(10) EHI export is a compliance stub: a PDF chart printout and a C-CDA clinical summary (likely reused from Transitions of Care) with zero documentation of what data is actually exported. A patient requesting their complete health information from a TCC-based practice would receive a non-computable PDF and/or a clinical summary missing billing, scheduling, specialty, and operational data — despite the product storing all of these as an integrated EHR+PM system. This represents one of the weakest (b)(10) implementations possible while still technically having a certified export function.
