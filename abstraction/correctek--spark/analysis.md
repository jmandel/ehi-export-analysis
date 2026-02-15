# EHI Export Analysis: CorrecTek

**Product**: Spark 7.1
**Analysis date**: 2026-02-15
**CHPL ID**: 15.05.05.1292.CORT.01.00.1.200114 (ID 10274)

## 1. Product Context

CorrecTek Spark is a full-featured EHR purpose-built for **correctional healthcare, juvenile detention, and behavioral health** settings. It serves over 120 organizations across 30+ U.S. states. The product integrates medical, dental, and behavioral health records into a unified patient chart and includes:

- **Clinical documentation**: encounters, notes, problem lists, medication lists, allergies, immunizations, vitals, clinical assessments, implantable device lists
- **Medication management**: eMAR, EPCS-certified e-prescribing (via NewCrop), SureScripts integration
- **CPOE**: medication, lab, and diagnostic imaging orders with bidirectional results interfaces
- **Integrated billing**: eligibility checks, claims submission (Medicare/Medicaid/private), ERA posting, Medicaid 1115 waiver support
- **Correctional-specific workflows**: intake screenings, sick call management (via kiosk/phone/tablet), inmate tracking data from jail management systems (JMS/OMS), NCCHC/ACA/AJA compliance documentation
- **Dental and behavioral health records**: integrated into the unified chart
- **Juvenile-specific features**: guardian portal access, release planning, immunization registry integration
- **Reporting**: hundreds of prebuilt reports, optional Power BI dashboards

This is a broad product storing data across clinical, billing, correctional-administrative, and specialty domains. An adequate (b)(10) export would need to cover far more than standard clinical summary data.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `cost-disclosure-page-text.txt` (2,140 bytes) | Extracted text of CorrecTek's mandatory disclosures page, containing the complete (b)(10) description | **Primary source** — contains the entirety of EHI export documentation |
| `screenshot-full-page.png` (1.0 MB) | Full-page screenshot of the Cost Disclosure & Transparency page | Confirms page layout and that (b)(10) section is a footnote at the bottom of the certification criteria table |
| `screenshot-ehi-text.png` (18 KB) | Close-up screenshot of the (b)(10) text | Confirms truncation on the live page — text cuts off at "the us" |
| `screenshot-ehi-section.png` (2.4 KB) | Screenshot of the §170.315(b)(10) certification label | Confirms the criterion is listed |
| `fhirR4endpoints-umc.json` (99 bytes) | FHIR R4 endpoints file linked from the disclosures page | Empty FHIR Bundle with no entries — relevant to (g)(10), not (b)(10) |

**Verification**: I independently fetched the live page at `https://correctek.com/cost-disclosure-and-transparency` on 2026-02-15. The page returns HTTP 200 and renders the same content as the screenshots. The (b)(10) text is still truncated at "the us" on the live page. No additional EHI documentation, data dictionaries, schemas, sample data, or downloadable files were found on the page or linked from it.

## 3. Export Mechanics

- **Format**: PDF and/or C-CDA
- **Mechanism**: Not specified beyond "exported to one or more PDF/C-CDA files" saved to a user-specified folder. Likely a UI-driven export within the Spark application.
- **Scope**: Single-patient ("Records for a patient are exported")
- **Bulk capability**: No mention of bulk/population-level export
- **Access constraints/fees**: No EHI-specific fees mentioned. The cost transparency section describes general software licensing, implementation, and maintenance fees.
- **Encryption/integrity**: Not mentioned

The complete (b)(10) documentation is one sentence (truncated on the live site):

> *EHI can be exported in PDF or C-CDA format. Records for a patient are exported to one or more PDF/C-CDA files. The files created by the export are saved to a folder specified by the user.*

## 4. Export Content: What's In It

### What the documentation tells us

**Nothing specific.** The single-sentence documentation provides no information about:
- What data fields or categories are exported
- Which C-CDA document type(s) are produced (CCD, Discharge Summary, Progress Notes, etc.)
- What content appears in the PDF(s)
- Whether different data goes to PDF vs. C-CDA
- How many files are produced per patient
- What time range of data is included

There is no data dictionary, no field listing, no schema, no sample data, and no user guide.

### What can be inferred from the format

The export uses **PDF and C-CDA** — both are document-oriented formats designed for clinical information exchange, not database-level exports:

- **C-CDA** (Consolidated Clinical Document Architecture) is a clinical document standard. Standard C-CDA sections cover demographics, problems, medications, allergies, immunizations, vital signs, lab results, procedures, encounters, and care plans. It does not have standard representations for billing data, correctional-specific forms, eMAR administration records, dental charting, or custom assessment instruments.

- **PDF** could theoretically contain anything rendered from the system, but without documentation of what is included, this is unknowable. PDFs are not machine-readable and cannot serve as a structured data export.

### Vendor's own content organization

No content organization is provided. The vendor does not describe, categorize, or enumerate what data is included in the export. There is no data dictionary to tabulate.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor provides **no specifics** about export content. The only information is the format: "PDF or C-CDA." Without a data dictionary, field listing, sample data, or even a narrative description of what's included, it is impossible to determine what data domains are covered.

The choice of C-CDA as a primary format strongly suggests the export covers standard clinical summary data (the USCDI/US Core data classes), since that is what C-CDA is designed to represent. The PDF component could potentially capture additional content (clinical notes, documents), but this is speculation.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial (inferred) | No documentation; C-CDA typically includes demographics | Likely present in C-CDA but not confirmed |
| Encounters / visits | ⚠️ Partial (inferred) | No documentation; C-CDA may include encounter headers | Spark stores detailed encounter documentation; coverage unknown |
| Problems / conditions / diagnoses | ⚠️ Partial (inferred) | No documentation; standard C-CDA section | Likely present but depth unknown |
| Medications / prescriptions | ⚠️ Partial (inferred) | No documentation; C-CDA medication section likely included | eMAR administration records, EPCS history, SureScripts data likely not captured in C-CDA |
| Allergies | ⚠️ Partial (inferred) | No documentation; standard C-CDA section | Likely present |
| Immunizations | ⚠️ Partial (inferred) | No documentation; standard C-CDA section | Likely present |
| Vitals | ⚠️ Partial (inferred) | No documentation; standard C-CDA section | Likely present |
| Lab results | ⚠️ Partial (inferred) | No documentation; C-CDA results section likely included | Spark receives bidirectional lab results; coverage unknown |
| Imaging / diagnostic reports | ⚠️ Partial (inferred) | No documentation; C-CDA may include some results | Spark receives radiology results/images; image inclusion unlikely |
| Procedures | ⚠️ Partial (inferred) | No documentation; standard C-CDA section | Likely present |
| Clinical notes / documents | ⚠️ Partial (inferred) | PDF may capture rendered notes | Spark has extensive clinical documentation; PDF capture scope unknown |
| Care plans / goals | ⚠️ Partial (inferred) | No documentation | Unknown |
| Orders / referrals | ⚠️ Partial (inferred) | No documentation | Spark supports CPOE for meds, labs, imaging; export coverage unknown |
| Insurance / coverage | ❌ Not covered (inferred) | No documentation; not a standard C-CDA element | Spark stores eligibility and insurance data; likely missing from C-CDA export |
| Claims / billing | ❌ Not covered (inferred) | No documentation; C-CDA does not represent billing data | Spark has full billing cycle (claims, ERA, eligibility); significant likely gap |
| Payments | ❌ Not covered (inferred) | No documentation; C-CDA does not represent payment data | Spark handles ERA posting and payment reconciliation; significant likely gap |
| Consents / directives | ⚠️ Partial (inferred) | No documentation | Unknown |
| Patient communications / portal messages | ❌ Not covered (inferred) | No documentation | Spark supports guardian portal in juvenile settings; likely missing |
| Specialty: Correctional intake/screening | ❌ Not covered (inferred) | No documentation; no C-CDA representation for correctional forms | Core product functionality — intake screenings, NCCHC/ACA forms; significant likely gap |
| Specialty: Dental | ❌ Not covered (inferred) | No documentation; no standard C-CDA representation | Spark integrates dental records; likely missing from C-CDA |
| Specialty: Behavioral health | ❌ Not covered (inferred) | No documentation; limited C-CDA representation | Spark integrates behavioral health records; likely missing or thin |
| Specialty: Sick call management | ❌ Not covered (inferred) | No documentation; no C-CDA representation | Core correctional workflow; likely missing |
| Specialty: eMAR | ❌ Not covered (inferred) | No documentation; C-CDA captures med lists, not administration records | Core nursing workflow; likely missing |

**Critical caveat**: Every coverage assessment above is **inferred**, not confirmed. The vendor provides zero documentation of export content. The "Partial (inferred)" ratings for clinical domains are based solely on the assumption that a C-CDA export would include standard C-CDA sections. The "Not covered (inferred)" ratings reflect that C-CDA has no standard representation for these data types and the vendor has not described any mechanism for exporting them.

## 6. Documentation Quality

The export documentation is **effectively nonexistent**. One truncated sentence (with a minor authoring error leaving the last two letters cut off on the live page) is the entirety of what CorrecTek provides for (b)(10).

- **No data dictionary**: zero information about what fields or data categories are exported
- **No schema**: no C-CDA profile, template, or section specification
- **No sample data**: no example export files
- **No user guide**: no instructions for initiating the export, no screenshots
- **No machine-readable artifacts**: the only JSON file is an empty FHIR Bundle for the (g)(10) API, unrelated to (b)(10)
- **Not developer-usable**: a developer receiving this export would have no documentation to work with — they would need to reverse-engineer the C-CDA and PDF files

This is among the least documented (b)(10) implementations possible while still having a certified criterion listed.

## 7. Overall Assessment

### Classification

**Minimal/stub**

The documentation is too thin to meaningfully assess coverage. One sentence describing the export format (PDF/C-CDA) with no content specification, no data dictionary, no schema, and no sample data constitutes a stub implementation of (b)(10) documentation obligations. The use of PDF/C-CDA as the export format — rather than a native data model export — further suggests this is a clinical summary repackaged as an "EHI export," not a genuine effort to provide access to all electronic health information the system stores.

### Key Findings

1. **The entire (b)(10) EHI export documentation is a single sentence** — "EHI can be exported in PDF or C-CDA format. Records for a patient are exported to one or more PDF/C-CDA files. The files created by the export are saved to a folder specified by the user." — which is truncated on the live page (`cost-disclosure-page-text.txt`; verified via live page fetch 2026-02-15).

2. **No data dictionary, schema, or sample data exists.** Zero artifacts describe what data is included in the export. There are no downloadable files related to (b)(10) — no PDFs, no schemas, no guides.

3. **Export format is PDF/C-CDA**, which is a standard-based clinical document format. C-CDA is designed for clinical summaries covering USCDI data classes, not for comprehensive database-level export. This format cannot naturally represent billing data, correctional-specific workflows, dental records, eMAR administration records, or custom assessment forms — all of which Spark stores.

4. **Significant probable coverage gaps**: Spark is a feature-rich correctional EHR with integrated billing, dental, behavioral health, eMAR, sick call management, and correctional compliance documentation. A PDF/C-CDA export almost certainly omits most of these specialty and administrative data domains.

5. **The FHIR endpoints file is empty**: `fhirR4endpoints-umc.json` contains an empty Bundle with no endpoint entries, suggesting minimal FHIR API deployment — but this is for the (g)(10) API, not (b)(10).

### Summary Stats

```
Classification:  Minimal/stub
Export format:   PDF, C-CDA
Model type:      Standard projection (C-CDA)
Entities:        N/A (no data dictionary)
Fields:          N/A (no data dictionary)
Descriptions:    N/A
Sample data:     No
Bulk export:     No (single-patient only per documentation)
Domains covered: 0 of 19 confirmed; ~10 of 19 inferred-partial from C-CDA format
```

### Bottom Line

CorrecTek provides the absolute minimum (b)(10) documentation: a single sentence stating the export format is PDF/C-CDA with no specification of content. A patient or provider requesting their data would receive files with no documentation explaining what's in them, and the C-CDA format almost certainly omits billing, dental, behavioral health, eMAR, and correctional-specific data that Spark stores. This is a compliance checkbox, not a genuine effort to enable access to all electronic health information.
