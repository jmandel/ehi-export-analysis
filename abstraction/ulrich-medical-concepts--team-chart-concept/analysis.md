# EHI Export Analysis: Ulrich Medical Concepts

**Product**: Team Chart Concept (TCC) v7.1
**Analysis date**: 2026-02-15
**CHPL ID**: 15.05.05.3049.UL15.01.00.1.191226 (CHPL #10227)

## 1. Product Context

Team Chart Concept (TCC) is an integrated EHR and practice management system developed by Ulrich Medical Concepts (UMC), a small (~22 employee) company based in Paducah, Kentucky. The product targets ambulatory practices across multiple specialties including primary care, internal medicine, dermatology, OB/GYN, general surgery, urgent care, and therapy.

TCC is a comprehensive platform combining clinical and administrative functions:

- **Clinical EHR**: Encounter documentation, problem lists, medication lists, allergies, immunizations, vitals, health maintenance alerts, implantable device lists, clinical decision support, and quality measures
- **CPOE**: Medication, laboratory, and diagnostic imaging orders with bi-directional lab connectivity
- **E-prescribing**: Via NewCrop (DrFirst) integration
- **Practice management & billing**: Scheduling, integrated billing with "full HIPAA compliant billing routines," SmartCoder claims scrubbing, ICD-10, financial reporting
- **Document management**: Scanned documents, office forms, digitized historical records
- **Patient engagement**: Patient portal (via Medfusion), patient communications (via Bridge)
- **Interoperability**: C-CDA transitions of care, Direct messaging, FHIR API (via EMR Direct Interoperability Engine), HL7, HIE connectivity (KHIE)
- **Public health reporting**: Cancer registry, transmission to public health agencies

The vendor also provides medical billing services, making billing a core function. TCC is certified for 33 ONC criteria including (b)(10) EHI Export (certified 2019-12-26). Given this breadth, a compliant EHI export should cover clinical records, orders, prescriptions, billing/claims, documents, and patient communications.

## 2. Artifacts Reviewed

| Artifact | Type | Size | Description | Informative? |
|---|---|---|---|---|
| `cost-disclosure-and-transparency.html` | HTML | 104,270 bytes | Mandatory ONC disclosure page containing the **entire** (b)(10) documentation as a single footnote | **Primary source** — but contains almost nothing |
| `cost-disclosure-and-transparency-page.png` | PNG | 669,693 bytes | Full-page screenshot of the disclosure page | Visual confirmation only |
| `fhirR4endpoints-umc.json` | JSON | 99 bytes | FHIR R4 endpoint directory for UMC customers | Not EHI-relevant; empty Bundle with zero entries |
| `interopengine-open-api-documentation.html` | HTML | 34,678 bytes | EMR Direct Interoperability Engine API docs | Not EHI-relevant; generic (g)(10) FHIR API docs, no mention of EHI or (b)(10) |
| 2025 RWT Plan PDF (verified live) | PDF | 7 pages | Real World Testing plan with EHI Export measures | Marginal additional detail on export mechanism |
| 2025 RWT Results PDF (verified live) | PDF | 4 pages | Real World Testing results report | **Notable**: omits EHI Export outcomes entirely |

**Most informative**: The disclosure page HTML and the RWT Plan PDF, though together they provide less than 100 words about the EHI export.

**Least informative**: The FHIR endpoint JSON (empty) and the InteropEngine API docs (unrelated to (b)(10)).

## 3. Export Mechanics

**Format**: PDF and/or C-CDA files

**Mechanism**: A "chart export routine" within the TCC application. A user with export permissions selects a single patient or retrieves a list of patients and runs the export. Files are saved to a user-specified local folder.

**Single-patient**: Yes — explicitly described in RWT plan

**Bulk/multi-patient**: Yes — the RWT plan describes "retrieving a list of patients" and exporting each patient's chart. However, it's unclear if this is a true batch operation or requires manual iteration.

**Access constraints**: Requires user permission ("a user that has permission to complete a chart export"). No information about fees.

**Success criterion** (per RWT plan): "If a PDF is generated the result has been met successfully." The bar is file creation, not content completeness.

## 4. Export Content: What's In It

### What is documented

The entire (b)(10) EHI export documentation consists of this 36-word footnote on the disclosure page:

> *EHI can be exported in PDF or C-CDA format. Records for a patient are exported to one or more PDF/C-CDA files. The files created by the export are saved to a folder specified by the user.*

The RWT plan adds:

> "This test is completed by selecting a single patient in the Team Chart Concept product as user that has permission to complete a chart export and running the chart export routine to export the patient's chart to PDF and C-CDA file(s). If a PDF is generated the result has been met successfully."

**There is no data dictionary.** There are no entities, tables, fields, schemas, sample data, value sets, relationships, or any structured documentation of what the export contains. The vendor does not specify what data is included or excluded.

### What can be inferred

- **PDF export**: A PDF rendering of the patient chart. PDFs are non-computable — they flatten structured data into a visual layout that cannot be reliably parsed, queried, or imported into another system. The content likely mirrors whatever the EHR's chart view displays (demographics, notes, medications, problems, allergies, vitals, lab results), but this is speculation since no documentation exists.

- **C-CDA export**: Almost certainly the same C-CDA used for the Transitions of Care criterion (b)(1), which TCC is also certified for. A standard C-CDA covers USCDI-aligned clinical summary data: demographics, problems, medications, allergies, immunizations, vital signs, procedures, results, and care team. C-CDA has no representation for billing records, claims, scheduling, custom forms, scanned documents, or most practice management data.

### Vendor's own content organization

The vendor provides no content organization. There is no data dictionary, no entity listing, no categorization of export content. The table below is necessarily empty:

| Entity/Table | Fields | Described | Types | Category (vendor's) |
|---|---|---|---|---|
| *(none documented)* | — | — | — | — |

**Total entities documented: 0**
**Total fields documented: 0**
**Fields with descriptions: 0**

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor describes no specific data coverage. The export documentation says "records for a patient" without defining what constitutes a "record." There are no categories, no modules, no sections — just two format labels (PDF and C-CDA).

If we accept the C-CDA component at face value, it likely covers the standard USCDI clinical summary: demographics, problems, medications, allergies, immunizations, vitals, procedures, and results. This is the minimum clinical data set required by C-CDA.

The PDF component is a visual rendering that may display additional data visible in the EHR's chart view, but in a non-computable format that is effectively unusable for data portability.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | Inferred from C-CDA (standard section) | Likely present but not documented; coverage depth unknown |
| Encounters / visits | ⚠️ Partial | Inferred from C-CDA (may include encounter section) | TCC stores encounter notes — C-CDA may capture basic info but not full encounter detail |
| Problems / conditions | ⚠️ Partial | Inferred from C-CDA (standard section) | Likely present; depth unknown |
| Medications / prescriptions | ⚠️ Partial | Inferred from C-CDA (standard section) | C-CDA covers medication list; e-prescribing history via NewCrop likely missing |
| Allergies | ⚠️ Partial | Inferred from C-CDA (standard section) | Likely present |
| Immunizations | ⚠️ Partial | Inferred from C-CDA (standard section) | Likely present |
| Vitals | ⚠️ Partial | Inferred from C-CDA (standard section) | Likely present |
| Lab results | ⚠️ Partial | Inferred from C-CDA (results section) | C-CDA may include results; full lab order detail likely missing |
| Imaging / diagnostic reports | ❌ Not covered | No evidence | TCC has CPOE for imaging orders; no export evidence |
| Procedures | ⚠️ Partial | Inferred from C-CDA (standard section) | Basic procedure list may be present |
| Clinical notes / documents | ⚠️ Partial | PDF may render notes; C-CDA has limited note support | TCC's core function is encounter documentation; PDF captures visual but not structured data |
| Care plans / goals | ❌ Not covered | No evidence | Not documented |
| Orders / referrals | ❌ Not covered | No evidence | TCC has CPOE for meds, labs, imaging; no export evidence for order data |
| Insurance / coverage | ❌ Not covered | No evidence | TCC is an integrated PM system; insurance data not addressed |
| Claims / billing | ❌ Not covered | No evidence | **Significant gap**: TCC has "full HIPAA compliant billing routines" and SmartCoder claims scrubbing; billing is a core function |
| Payments | ❌ Not covered | No evidence | TCC provides billing services; payment data not addressed |
| Consents / directives | ❌ Not covered | No evidence | Not documented |
| Patient communications | ❌ Not covered | No evidence | TCC integrates with Medfusion portal and Bridge; communication data not addressed |
| Specialty-specific data | ❌ Not covered | No evidence | TCC serves dermatology, OB/GYN, surgery, therapy; no specialty data in export |

**Covered domains**: 0 confirmed (all assessments are inferred from C-CDA standard, not from vendor documentation)
**Partial (inferred)**: ~8 domains (if C-CDA is standard-conformant)
**Not covered**: ~10 domains
**Applicable domains**: ~18

The most significant gaps are:
1. **Billing/claims/payments**: TCC is an integrated practice management system where billing is a core function. The vendor also provides billing services. Zero billing data is documented in the export.
2. **Orders (lab, imaging, medication)**: TCC has CPOE for all three order types with bi-directional lab connectivity. No order data is documented.
3. **Clinical notes in structured form**: TCC's primary clinical function is encounter documentation. PDF captures visual rendering; C-CDA has limited note representation.
4. **Document management**: TCC has integrated document management with scanned documents and digitized historical records. No document/attachment export evidence.
5. **Specialty clinical data**: TCC serves multiple specialties (dermatology, OB/GYN, surgery, therapy) but no specialty-specific data appears in the export.

## 6. Documentation Quality

The documentation quality is **effectively nonexistent**:

- **Data dictionary**: None
- **Field-level documentation**: None — zero fields documented
- **Data types**: None
- **Value sets / code systems**: None
- **Relationships / foreign keys**: None (no entities to relate)
- **Sample data**: None
- **Machine-readable schemas**: None
- **User guide**: None — no instructions for performing the export
- **Content specification**: None — no description of what data is or isn't included

A developer cannot build an import from this documentation because there is nothing to build from. The documentation consists of 36 words explaining the export format (PDF/C-CDA) and file saving mechanism.

The RWT plan adds ~50 words of operational detail (user needs permission, can export single or multiple patients, success = PDF generated). This is testing procedure documentation, not export format documentation.

**The 2025 RWT Results report omits EHI Export outcomes entirely.** The plan included 12 measures; the results report covers only 3 (all API-related). The 9 omitted measures include both EHI Export Single and EHI Export Multiple, plus all Transitions of Care and CQM measures. All 3 reported measures note "No customers opted to implement."

## 7. Overall Assessment

### Classification

**Minimal/stub**

The export documentation is too thin to assess content coverage. What documentation exists (36 words) describes two export formats — PDF (non-computable) and C-CDA (clinical summary standard) — neither of which is appropriate for comprehensive EHI export of an integrated EHR/practice management system. There is no data dictionary, no schema, no sample data, and no description of what data is included or excluded.

### Key Findings

1. **The entire (b)(10) documentation is a 36-word footnote.** Six years after certification (2019-12-26), the vendor's public-facing EHI export documentation consists of a single sentence explaining that data can be exported as PDF or C-CDA files. No data dictionary, schema, sample data, or content specification exists. (Source: `cost-disclosure-and-transparency.html`)

2. **The export formats are structurally inadequate.** PDF is non-computable and cannot be reliably parsed or imported. C-CDA is a clinical summary standard covering ~20% of what an integrated EHR/PM system stores. Neither format can represent billing, claims, orders, scanned documents, or specialty clinical data. (Source: `cost-disclosure-and-transparency.html` footnote)

3. **Billing data — a core product function — has no export path.** TCC is marketed as an integrated EHR and practice management system with "full HIPAA compliant billing routines." The vendor also provides billing services. Neither PDF nor C-CDA has a standard representation for billing/claims data, and no supplementary export mechanism is documented. (Source: `product-research.md`, `cost-disclosure-and-transparency.html`)

4. **The RWT results report omits EHI Export outcomes.** The 2025 RWT plan defined 12 measures including "EHI Export Single" and "EHI Export Multiple." The results report covers only 3 measures (all API), silently dropping 9 measures including both EHI Export measures. (Source: 2025 RWT Plan PDF, 2025 RWT Results PDF, both verified live at `elearning.ulrichmedicalconcepts.com`)

5. **Zero active customer FHIR integrations.** The FHIR R4 endpoints JSON (`fhirR4endpoints-umc.json`) returns an empty Bundle with no entries, and all 3 reported RWT outcomes note "No customers opted to implement." This suggests minimal real-world interoperability usage. (Source: `fhirR4endpoints-umc.json`, 2025 RWT Results PDF)

### Summary Stats

    Classification:  Minimal/stub
    Export format:   PDF, C-CDA
    Model type:      Standard projection (C-CDA clinical summary) + non-computable PDF rendering
    Entities:        0 (no data dictionary)
    Fields:          0 (no field documentation)
    Descriptions:    N/A
    Sample data:     No
    Bulk export:     Yes (multi-patient described in RWT plan, mechanism unclear)
    Domains covered: 0 confirmed; ~8 inferred from C-CDA standard (of ~18 applicable)

### Bottom Line

A patient or provider requesting their data from Team Chart Concept would receive a PDF printout and/or a C-CDA clinical summary — the same documents available through existing clinical workflows, not a comprehensive export of all electronic health information. The most critical gap is the complete absence of billing and practice management data from an integrated EHR/PM system. With zero documentation of export contents and export formats that are structurally incapable of carrying the full designated record set, this is a compliance stub, not a genuine EHI export implementation.
