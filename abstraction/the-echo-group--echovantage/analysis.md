# EHI Export Analysis: The Echo Group (Ensora Health)

**Product**: EchoVantage
**Analysis date**: 2026-02-16
**CHPL IDs**: 11129 (15.04.04.2425.Echo.13.02.1.221227)

## 1. Product Context

EchoVantage is a **web-based, integrated EHR, billing, and practice management platform** purpose-built for **community behavioral health agencies**. Developed by The Echo Group (founded ~1980, acquired by Therapy Brands in 2022, rebranded to Ensora Health in 2025), it serves mental health clinics, substance use recovery centers, I/DD service providers, crisis intervention departments, foster/residential care programs, correctional health facilities, and county behavioral health programs.

Key functional areas relevant to EHI export completeness:

- **Clinical/EHR**: Visual Health Record (VHR) timeline, progress notes, treatment plans, assessments (standardized and custom via Forms Designer), client intake, diagnoses, clinical intelligence engine
- **e-Prescribing**: Via DrFirst integration — medication histories, interaction checking, pharmacy transmission
- **Billing & RCM**: Claims submission (via Apex Clearinghouse), eligibility verification, payment posting, remittance processing, charge creation, credit balances
- **Scheduling**: Appointments, reminders
- **Telehealth**: HIPAA-compliant video sessions
- **State Reporting**: State-specific mandatory behavioral health reporting
- **Document Management**: Storage integrated with clinical record
- **Medication Assisted Treatment (MAT)**: Methadone dosing/dispensing (announced for H1 2025)

This is a **full-spectrum behavioral health platform** — clinical, billing, and administrative. A complete EHI export should cover clinical documentation, behavioral health-specific assessments and treatment plans, medications, billing/claims, and specialty data (substance use, I/DD, crisis).

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `Electronic-Health-Information-Export_EchoVantage.pdf` | 1-page PDF (148,587 bytes, created 2025-08-15). Lists export file formats for single patient (CCD/C-CDA, JSON, PDF) and population (.bak MSSQL backup). ~100 words of substantive content. No data dictionary, schema, or field definitions. | **Low** — format names only, no content detail |
| `onc-echo-page.html` | Full HTML of ONC certification page (81,717 bytes). Contains ~130 words of EHI export text describing single patient and population export modes. Links to the PDF above. | **Low** — prose description of export modes only |
| `onc-echo-page-screenshot.png` | Full-page screenshot (915,427 bytes) confirming page layout. Shows EHI Export section, FHIR API section, Real World Testing section. | **Confirmatory** — verified HTML text extraction accuracy |

**Total substantive documentation**: ~230 words across all artifacts. No data dictionary, no schema, no field definitions, no sample data, no machine-readable artifacts of any kind.

The live URL (https://ensorahealth.com/onc/echo/) was verified accessible on 2026-02-16 and contains identical content to the captured HTML. The only EHI-related link on the page points to the same PDF. No additional documentation has been added since collection.

## 3. Export Mechanics

**Single Patient Export**:
- **Mechanism**: Self-service — "allows a user to export electronic health information (EHI) for a single patient without developer assistance"
- **Formats**: CCD/C-CDA, JSON, PDF
- **Scope**: Explicitly limited to "data required by the USCDI v1 standards" (per PDF)
- **Access constraints**: None stated for single patient

**Patient Population Export**:
- **Mechanism**: Vendor-assisted — "can be requested by submitting a support ticket via Salesforce"
- **Format**: `.bak` file (full MSSQL Server database backup)
- **Scope**: "All data for an agency" (per PDF)
- **Access constraints**: Requires support ticket; no timeline, fees, or process documented

**Variability caveat** (from the ONC page): "The content included in the export might vary based on a variety of factors" including software applications in use, version, documentation practices, configuration decisions, and "materials not sourced from the application."

## 4. Export Content: What's In It

### What can be determined

The documentation provides **no data dictionary, no schema, no field-level definitions, and no sample data**. The entire technical specification of export content is:

1. **Single patient CCD/C-CDA**: Will contain "data required by the USCDI v1 standards." USCDI v1 defines a specific set of data classes: Allergies and Intolerances, Assessment and Plan of Treatment, Care Team Members, Clinical Notes, Goals, Health Concerns, Immunizations, Laboratory, Medications, Patient Demographics, Problems, Procedures, Provenance, Smoking Status, Unique Device Identifiers, and Vital Signs.

2. **Single patient JSON**: No documentation whatsoever of structure, schema, or content. The PDF describes JSON generically ("a lightweight format for storing and transporting data") but says nothing about what data elements are included or how they are structured.

3. **Single patient PDF**: Human-readable document. No specification of content.

4. **Population .bak**: "A full MSSQL Server database backup of all data for an agency that can be restored." No schema documentation — table names, column names, data types, relationships, value sets, and coded values are all undocumented.

### Vendor's own content organization

The vendor does not organize or categorize export content. There is no entity list, no table list, no field inventory. The only categorization is by **export mode** (single patient vs. population) and **file format** (CCD/C-CDA, JSON, PDF, .bak).

| Entity/Table | Fields | Described | Types | Category |
|---|---|---|---|---|
| *(none documented)* | — | — | — | — |

**Entity count**: 0 documented
**Field count**: 0 documented
**Fields with descriptions**: 0

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor describes two export tiers with no content detail:

1. **Single patient**: USCDI v1 scoped. This standard covers core clinical data classes but excludes behavioral health-specific content (custom assessments, treatment plan structures, substance use data, I/DD data), billing/claims, and any vendor-specific data structures. For a behavioral health EHR, USCDI v1 represents a small fraction of the patient record.

2. **Population**: Full database backup. This *theoretically* contains everything in the system, but with zero documentation, it is practically opaque. A recipient would need MSSQL Server to restore the backup and would then need to reverse-engineer every table, column, relationship, and coded value.

Neither tier has any documentation of what specific data elements are included.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | USCDI v1 includes Patient Demographics; population .bak presumably includes full demographics | Single patient: limited to USCDI v1 fields. Population: undocumented schema. |
| Encounters / visits | ⚠️ Partial | USCDI v1 includes Encounters minimally; .bak presumably includes encounter data | Product stores encounters; single patient export likely thin. |
| Problems / conditions / diagnoses | ⚠️ Partial | USCDI v1 includes Problems | Only USCDI-defined problems for single patient. |
| Medications / prescriptions | ⚠️ Partial | USCDI v1 includes Medications | Product has deep e-prescribing via DrFirst; USCDI covers basic medication list only. |
| Allergies | ⚠️ Partial | USCDI v1 includes Allergies and Intolerances | Basic coverage via USCDI. |
| Immunizations | ⚠️ Partial | USCDI v1 includes Immunizations | Basic coverage via USCDI. |
| Vitals | ⚠️ Partial | USCDI v1 includes Vital Signs | Basic coverage via USCDI. |
| Lab results | ⚠️ Partial | USCDI v1 includes Laboratory | Product has lab integration; USCDI covers basic results. |
| Imaging / diagnostic reports | N/A | — | Behavioral health system; no imaging capability described. |
| Procedures | ⚠️ Partial | USCDI v1 includes Procedures | Basic coverage via USCDI. |
| Clinical notes / documents | ⚠️ Partial | USCDI v1 includes Clinical Notes | Product has progress notes, session notes, clinical narratives — USCDI captures some but not behavioral health-specific note structures. |
| Care plans / goals | ⚠️ Partial | USCDI v1 includes Goals, Assessment and Plan of Treatment | Product has structured treatment plans with outcome linkage — a core feature. USCDI captures goals but not EchoVantage's treatment plan structures. |
| Orders / referrals | ❌ Not covered | No evidence in single patient export; no schema for .bak | Product supports e-prescribing orders; not documented in export. |
| Insurance / coverage | ❌ Not covered | Not in USCDI v1; no schema for .bak | Product manages insurance/eligibility; significant gap in single patient export. |
| Claims / billing | ❌ Not covered | Not in USCDI v1; no schema for .bak | Product has full billing/RCM; significant gap in single patient export. |
| Payments | ❌ Not covered | Not in USCDI v1; no schema for .bak | Product manages payments/remittances; significant gap. |
| Consents / directives | ❌ Not covered | Not in USCDI v1; no schema for .bak | Likely present in behavioral health system; not documented. |
| Patient communications | ❌ Not covered | Not in USCDI v1; no schema for .bak | Product has appointment reminders; not documented in export. |
| Specialty: Behavioral health assessments | ❌ Not covered | Not in USCDI v1; no schema for .bak | **Core product feature** — standardized and custom assessments with scored results tracked over time. Major gap. |
| Specialty: Substance use recovery | ❌ Not covered | Not in USCDI v1; no schema for .bak | Product serves SUR centers; specialty data not documented. |
| Specialty: I/DD services | ❌ Not covered | Not in USCDI v1; no schema for .bak | Product serves I/DD providers; specialty data not documented. |
| Specialty: Crisis intervention | ❌ Not covered | Not in USCDI v1; no schema for .bak | Product has crisis intervention capabilities; not documented. |
| Specialty: MAT (methadone) | ❌ Not covered | Not in USCDI v1; no schema for .bak | Product has MAT module; not documented. |

**Summary**: The single-patient export covers only USCDI v1 clinical domains — approximately 10-12 of the ~22 applicable domains, and even those only at the USCDI depth (not the full EchoVantage data model). The population .bak export *may* contain everything, but with zero schema documentation, no coverage claim can be verified.

**Domains covered**: At most 10-12 of 22 applicable domains (single patient, USCDI-scoped only). Population export: unknown (undocumented).

## 6. Documentation Quality

The EHI export documentation is **among the most minimal possible**:

- **Total documentation**: ~230 words across a 1-page PDF and an HTML section
- **Data dictionary**: None
- **Schema**: None
- **Field definitions**: None
- **Sample data**: None
- **Machine-readable artifacts**: None
- **Value sets/code systems**: None
- **Relationships/foreign keys**: None
- **User guide for performing export**: None
- **Screenshots of export interface**: None

**Could a developer build an import from this documentation?** No. For the CCD/C-CDA export, a developer could parse the C-CDA standard, but would have no idea which optional sections/entries EchoVantage populates. For the JSON export, a developer would have nothing to work with — no schema, no structure, no example. For the .bak file, a developer would need MSSQL Server and would face a complete reverse-engineering exercise with no documentation assistance.

The JSON export description is particularly notable: the PDF describes what JSON *is* ("a lightweight format for storing and transporting data") rather than what the vendor's JSON export *contains*. This suggests the documentation was written for a non-technical audience with no consideration for data portability.

## 7. Overall Assessment

### Classification

**Minimal/stub**

The documentation is too thin to meaningfully assess what the export contains. The single-patient export is explicitly a USCDI v1 clinical summary (a standard-based projection), while the population export is an undocumented raw database backup. Neither has any schema, field-level, or content documentation. The total substantive documentation is ~230 words — insufficient to determine what data is actually exported.

### Key Findings

1. **Single-patient export is explicitly USCDI v1 scoped** — the PDF states the CCD/C-CDA "will contain data required by the USCDI v1 standards." This is a clinical summary standard, not an all-EHI export. For a behavioral health EHR with treatment plans, custom assessments, billing, substance use data, and I/DD data, USCDI v1 covers a small fraction of stored EHI. (Source: `Electronic-Health-Information-Export_EchoVantage.pdf`)

2. **Zero data dictionary or schema documentation exists** — across all artifacts (PDF, HTML page, live site), there are no table names, field names, data types, relationships, value sets, or structural information of any kind. Entity count: 0. Field count: 0. (Source: all artifacts reviewed)

3. **Population export requires vendor assistance and provides no schema** — the .bak MSSQL backup must be requested via Salesforce support ticket and comes with no documentation of the database structure. A recipient would need to restore it in MSSQL Server and reverse-engineer the entire schema. (Source: `onc-echo-page.html`, `Electronic-Health-Information-Export_EchoVantage.pdf`)

4. **JSON export format is completely undefined** — the documentation describes what JSON is as a generic format but says nothing about the structure, content, or schema of EchoVantage's JSON export. (Source: `Electronic-Health-Information-Export_EchoVantage.pdf`)

5. **Behavioral health specialty data is the biggest gap** — EchoVantage's core value is in behavioral health-specific features (treatment plans with outcome linkage, custom assessments, substance use recovery, I/DD services, crisis intervention, MAT). None of this appears in the USCDI-scoped single-patient export, and the population export is undocumented.

### Summary Stats

```
Classification:  Minimal/stub
Export format:   CCD/C-CDA, JSON, PDF (single patient); MSSQL .bak (population)
Model type:      Standard projection (single patient); native database dump (population)
Entities:        0 (no data dictionary)
Fields:          0 (no field definitions)
Descriptions:    N/A
Sample data:     No
Bulk export:     Yes (population .bak via support ticket)
Domains covered: ~10-12 of 22 applicable (single patient, USCDI v1 only); unknown (population)
```

### Bottom Line

EchoVantage's EHI export documentation is a compliance stub — ~230 words total, no data dictionary, no schema, no sample data. The single-patient export is explicitly limited to USCDI v1 clinical summary data, missing the behavioral health-specific assessments, treatment plans, billing, and specialty data that constitute the product's core value. The population-level database backup may be complete but is practically unusable without schema documentation, and the single biggest gap is the complete absence of any structural documentation for any export format.
