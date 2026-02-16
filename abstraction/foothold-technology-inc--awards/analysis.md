# EHI Export Analysis: Foothold Technology, Inc.

**Product**: AWARDS v3.0
**Analysis date**: 2026-02-16
**CHPL IDs**: 15.04.04.1500.AWAR.03.00.1.171220 (CHPL ID 9267)

## 1. Product Context

AWARDS is a web-based EHR and case management system purpose-built for nonprofit human services and behavioral health organizations. It is the only record-keeping system federally certified as both a Behavioral Health EHR and a Homeless Management Information System (HMIS). It serves 1,000+ provider agencies across 28+ states, primarily in community-based behavioral health, homeless services, supportive housing, developmental disabilities, and substance use treatment.

**Data domains the product stores** (relevant for assessing export completeness):

- **Core clinical**: Demographics, problem lists/diagnoses, medications, allergies, vital signs, progress notes, treatment plans, assessments, immunizations, family health history, implantable devices, lab orders/results (via e-labs add-on), e-prescribing (via add-on)
- **Case management**: Service documentation, program enrollment/participation/discharge, multi-program coordination, scheduling
- **HMIS/housing data**: HUD Universal Data Elements (~30+ fields), housing status/history, homelessness episodes, income/benefits, health insurance, disabilities, domestic violence indicators
- **Administrative**: Billing records/claims (integrated with service documentation), HR, facilities maintenance
- **Custom data**: FormBuilder custom forms (agency-defined data structures), custom assessments
- **Interoperability**: C-CDA documents, FHIR resources (US Core/USCDI v3)

This product has significant breadth beyond typical ambulatory EHRs — particularly in HMIS data, case management, custom forms, and behavioral health workflows. A complete (b)(10) export would need to cover all of these domains.

## 2. Artifacts Reviewed

| Artifact | Description | Informative Value |
|---|---|---|
| `exportbuilders-main.html` (193 KB) | Main ExportBuilder Zendesk help article — the registered (b)(10) EHI export documentation. Detailed step-by-step instructions for using ExportBuilder. | **Most informative** for understanding the export mechanism; provides zero information about exportable data fields |
| `hmis-data-export.html` (275 KB) | HMIS Data Export article — describes HUD-compliant CSV export feature including Full, HIC, RHY, Full+ export types | Moderately informative — documents a separate specialized export feature with some field-level detail (ServicesOther.csv) |
| `mandatory-disclosures-dec-2024.pdf` (281 KB, 7 pages) | Official mandatory disclosures (updated Jan 2025). Contains the (b)(10) description and lists all certified criteria with costs | **Key artifact** — confirms ExportBuilder is the (b)(10) mechanism, lists C-CDA modules, confirms "No cost or fees" |
| `costs-and-limitations.pdf` (161 KB, 4 pages) | Original 2015 Edition costs/limitations. Predates (b)(10) | Low — does not cover (b)(10) |
| `fhir-api-docs.html` (44 KB) | FHIR API documentation (partial static capture). Lists US Core STU 6.1.0 / USCDI v3 resources for (g)(10) | Low — this is (g)(10), not (b)(10) |
| `exportbuilder-section.html` (24 KB) | Zendesk section index for ExportBuilder — contains only one article | Minimal |
| `screenshot-exportbuilders-full.png` (3.9 MB) | Full-page screenshot of ExportBuilder article | Confirms rendered content matches HTML text |
| `screenshot-exportbuilders-top.png` (270 KB) | Top portion screenshot | Minimal |
| `images/attachment-*.png` (4 files, <1 KB each) | Tiny UI button icons (add/combine/split/delete field) | None |

**No data dictionary, field listing, schema, or sample export data was found in any artifact.** The most critical documentation — the ReportBuilder articles that would list available data fields per module — is behind a Zendesk login wall (HTTP 403).

## 3. Export Mechanics

- **Format(s)**: CSV, TXT (fixed-width or delimited), XLS, XML
- **Mechanism**: UI-based tool ("ExportBuilder") accessed through each module's ReportBuilder within AWARDS
- **Single-patient**: Yes — "Select Client" option available
- **Bulk/multi-patient**: Yes — "Clients with Records" or "All Clients" options
- **Date range**: Limited to 2-year periods per export (except HMIS History ExportBuilder); multiple exports must be concatenated for longer periods
- **Delivery**: Direct download or sent to AWARDS Messages inbox (retained for 1 month)
- **Scheduling**: Can be scheduled and delivered to user's inbox
- **Access constraints**: Requires "Program Chart Access" permission; each ReportBuilder/ExportBuilder requires the corresponding module permission
- **Fees**: No cost or fees per mandatory disclosures
- **Separate HMIS export**: A distinct "HMIS Data Export" feature produces HUD-compliant zipped CSV files, separate from ExportBuilder

**Key limitation**: There is no single "export all EHI" button. Users must navigate to each module's ExportBuilder individually, select fields, configure formats, and generate separate export files. The documentation provides no guidance on which ExportBuilders to use, or in what combination, to produce a complete EHI export.

## 4. Export Content: What's In It

### The fundamental documentation gap

The ExportBuilder documentation describes the **export tool** in exhaustive detail (field selection, formatting, filtering, value mapping, sub-exports, saved formats) but provides **zero information** about what data fields are available for export. The article repeatedly states:

> "The specific data variables you see are based on the ReportBuilder through which you have accessed this ExportBuilder; both utilize the same options on this page."

The ReportBuilder documentation — which would list the actual data variables per module — requires Zendesk authentication and is not publicly accessible. The prior report confirmed that searching the help center for "ReportBuilder Report Contents," "ReportBuilders," "ReportBuilder Configuration Options," and "FormBuilder ReportBuilder" all returned HTTP 403.

### What we can determine from available artifacts

**Confirmed ExportBuilder modules** (explicitly mentioned in exportbuilders-main.html):

| Module | Evidence | Source |
|---|---|---|
| Demographics | Primary ExportBuilder; used as example throughout documentation | exportbuilders-main.html |
| Progress Notes | Mentioned in FormBuilder context ("if a form is available for inclusion when writing progress notes, the form's fields... will be available when using the Progress Notes ExportBuilder") | exportbuilders-main.html |
| HMIS History | Referenced as exception to 2-year date range limit | exportbuilders-main.html |

**Confirmed sub-export modules** (can be embedded in Demographics XML export):

| Module Path | Data Domain |
|---|---|
| Hospital > Episodes | Hospital/inpatient episodes |
| Medical > Allergies | Allergy records |
| Medical > Medications | Medication records |
| Employment > Job Placements | Employment placements |
| Employment > Job Interviews | Job interview records |

**HMIS Data Export** (separate from ExportBuilder):
- Produces HUD HMIS CSV files per the HUD specification
- Full+ export type adds FormBuilder custom form CSVs (as `FB_[id]_[name].csv`)
- Full+ includes `ServicesOther.csv` with 7 included fields: Date of Contact, Service Type, Unit, Cost, End Date, Service Details (max 50 chars), Funding Sources
- 64 service type categories and 26 funding source categories documented
- 5 fields explicitly noted as "Not transferred": Time, Duration, Location, Primary Problem Area, Attached Progress Notes

**C-CDA sections** (from mandatory disclosures PDF, for (g)(6)/(b)(1) not (b)(10)):
Demographics, Medications, Allergies, Diagnoses, Functional/Cognitive Status, Encounters (Progress Notes), Procedures, Progress Notes, Family Health History, Implantable Devices, Immunizations, Lab Orders (12 sections)

**FHIR resources** (from fhir-api-docs.html, for (g)(10) not (b)(10)):
19 US Core resource types: AllergyIntolerance, CarePlan, Condition, Coverage, Device, DiagnosticReport, DocumentReference, Goal, Location, Medication, MedicationDispense, MedicationRequest, Observation, Organization, Patient, Practitioner, Provenance, ServiceRequest, Specimen

### Vendor's own content organization

Because no data dictionary exists, we cannot present a table of entities with field counts. The vendor's documentation provides only the following organizational structure:

| Category | Known Modules/Entities | Fields | Described | Types | Source |
|---|---|---|---|---|---|
| Demographics | Demographics ExportBuilder | Unknown | No | No | exportbuilders-main.html |
| Medical | Allergies, Medications (sub-exports) | Unknown | No | No | exportbuilders-main.html |
| Hospital | Episodes (sub-export) | Unknown | No | No | exportbuilders-main.html |
| Employment | Job Placements, Job Interviews (sub-exports) | Unknown | No | No | exportbuilders-main.html |
| Progress Notes | Progress Notes ExportBuilder | Unknown | No | No | exportbuilders-main.html |
| HMIS | HMIS History ExportBuilder + HMIS Data Export | 7 (ServicesOther.csv only) | Partial | Partial | hmis-data-export.html |
| Custom Forms | FormBuilder fields (included if configured) | Variable per agency | No | No | exportbuilders-main.html |

**Total known field-level detail**: 12 fields documented (7 included + 5 excluded in ServicesOther.csv). All other field counts are unknown.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor's approach is to provide a **generic ad-hoc export tool** (ExportBuilder) rather than a purpose-built EHI export. The tool is described as available for "data to which [users] have access throughout the system," implying broad coverage — but without a data dictionary or field listing, this claim cannot be verified.

**Richest documentation**: The HMIS Data Export has the most field-level detail, with specific service types, funding sources, and ServicesOther.csv field definitions. However, this is a specialized HUD compliance export, not the general EHI export.

**Thinnest documentation**: Everything about the ExportBuilder's actual data content. The documentation is entirely procedural (how to use the tool) with zero substantive content about what data is exportable.

**Critical unknown**: The documentation mentions that ExportBuilders are located within "corresponding ReportBuilders" and that access depends on module permissions. This implies there may be ExportBuilders for other modules (Intake, Billing, Lab, Vitals, etc.), but without the ReportBuilder documentation, we cannot confirm or deny their existence.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | Demographics ExportBuilder confirmed; no field listing | Product stores demographics (certified (a)(5)); ExportBuilder exists but field coverage unknown |
| Encounters / visits | ⚠️ Partial | Hospital Episodes sub-export; Progress Notes ExportBuilder | Product stores encounters; some coverage confirmed but depth unknown |
| Problems / conditions / diagnoses | ❌ Not confirmed | Not explicitly mentioned as ExportBuilder module | Product stores diagnoses (certified (a)(3), C-CDA includes Diagnoses); no confirmed ExportBuilder |
| Medications / prescriptions | ⚠️ Partial | Medical > Medications sub-export confirmed | Product has e-prescribing and medication management; sub-export exists but field depth unknown |
| Allergies | ⚠️ Partial | Medical > Allergies sub-export confirmed | Sub-export exists; field depth unknown |
| Immunizations | ❌ Not confirmed | Not mentioned in ExportBuilder context | Product stores immunizations (certified (h)(1), in C-CDA); no confirmed ExportBuilder |
| Vitals | ❌ Not confirmed | Not mentioned in ExportBuilder context | Product tracks vital signs; no confirmed ExportBuilder |
| Lab results | ❌ Not confirmed | Not mentioned in ExportBuilder context | Product has e-labs module; no confirmed ExportBuilder |
| Imaging / diagnostic reports | ❌ Not confirmed | Not mentioned in ExportBuilder context | Product has diagnostic test info; no confirmed ExportBuilder |
| Procedures | ❌ Not confirmed | Not mentioned in ExportBuilder context | In C-CDA but not confirmed in ExportBuilder |
| Clinical notes / documents | ⚠️ Partial | Progress Notes ExportBuilder confirmed | Product stores progress notes and clinical documentation; ExportBuilder exists but depth unknown |
| Care plans / goals | ❌ Not confirmed | Not mentioned in ExportBuilder context | Product stores treatment plans; no confirmed ExportBuilder |
| Orders / referrals | ❌ Not confirmed | Not mentioned in ExportBuilder context | Product has CPOE; no confirmed ExportBuilder |
| Insurance / coverage | ❌ Not confirmed | HMIS export includes health insurance status | Product stores insurance data (HMIS and clinical); limited to HMIS export context |
| Claims / billing | ❌ Not confirmed | Not mentioned in ExportBuilder or HMIS export | Product has integrated billing; **significant potential gap** if no Billing ExportBuilder exists |
| Payments | ❌ Not confirmed | Not mentioned | Product processes billing; no export evidence |
| Consents / directives | ❌ Not confirmed | HMIS consent mentioned but only as a filter | Unknown |
| Patient communications / portal messages | N/A | Not mentioned | No evidence product stores portal messages beyond basic portal access |
| HMIS / housing data | ✅ Covered | Dedicated HMIS Data Export with Full/Full+ types; HUD-compliant CSV | Product's distinguishing feature; well-covered via HMIS Data Export |
| Case management / program data | ⚠️ Partial | Employment sub-exports (Job Placements, Job Interviews); HMIS export | Product's core function; some coverage but program enrollment/service documentation uncertain |
| Custom forms (FormBuilder) | ⚠️ Partial | FormBuilder fields available in ExportBuilder "when configured for inclusion in ReportBuilders"; FormBuilder CSVs in Full+ HMIS export | Product stores agency-defined custom forms; exportable only if pre-configured |
| Family health history | ❌ Not confirmed | In C-CDA but not mentioned in ExportBuilder | Product stores family health history (certified (a)(12)); no confirmed ExportBuilder |
| Behavioral health assessments | ❌ Not confirmed | Not mentioned in ExportBuilder context | Core product function; no confirmed ExportBuilder |

**Summary**: Of 22 applicable domains, only 1 (HMIS/housing data) has confirmed comprehensive coverage. 6 domains have partial/uncertain coverage. 15 domains have no confirmed coverage in the (b)(10) export documentation.

## 6. Documentation Quality

**Can a developer understand and use the export from these docs?**

A developer could learn to **operate the ExportBuilder tool** — the step-by-step instructions are thorough. However, a developer could not:
- Know what data fields are available for export in any module
- Build an import system without access to a sample export
- Determine whether a complete EHI export is achievable via ExportBuilder
- Understand the data model, relationships, or value sets

**What's well-documented**: The ExportBuilder's UI workflow, format options (CSV/TXT/XLS/XML), sub-export mechanism, saved format management, field mapping, and filtering capabilities.

**What requires guesswork**: Everything about the actual data — which modules have ExportBuilders, what fields each provides, data types beyond the generic format-level types, value sets, relationships between entities, and how to construct a complete patient record export.

**Machine-readable artifacts**: None. No schemas, no sample data, no data dictionary in any format. The HUD HMIS CSV specification is referenced externally but not provided.

**Assessment**: The documentation describes a flexible export tool but fails entirely as (b)(10) EHI export documentation. A patient or third party receiving an ExportBuilder export would have no schema, no field definitions, and no way to understand the data without direct access to the AWARDS system.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Minimal/stub/unclear**

The documentation is too thin to assess actual coverage. While the ExportBuilder is described as available for "data to which [users] have access throughout the system" — suggesting potentially broad coverage — the publicly available documentation provides no data dictionary, no field listing, and no evidence of which modules have ExportBuilders beyond 3 confirmed modules and 5 sub-export modules. The claim of system-wide availability cannot be verified. The most critical reference documentation (ReportBuilder articles listing available fields) is behind a login wall. Without that documentation, it's impossible to determine whether billing, lab results, vitals, treatment plans, immunizations, or other core domains are exportable.

**Axis 2 — Export approach: Unclear/undetermined**

The ExportBuilder appears to be a pre-existing general-purpose reporting/export tool that has been pointed to as the (b)(10) mechanism, rather than a purpose-built EHI export. Key evidence:
- The ExportBuilder documentation reads as generic product help, not EHI-specific documentation
- There is no guidance on performing a complete EHI export (which ExportBuilders to run, in what combination)
- The tool requires expert configuration — the documentation warns it "was designed for use by individuals who are familiar with export files and formats"
- The mandatory disclosures describe it as a flexible tool, not an EHI export process
- The 2-year date range limit per export would require multiple runs for longer patient histories

However, this is not a C-CDA or FHIR repackaging. The ExportBuilder exports native AWARDS data in configurable formats, which could potentially cover more data than USCDI if the underlying ReportBuilders provide access to all AWARDS modules. The distinction between "repurposed existing tool" and "purpose-built export" is ambiguous here — it's a pre-existing tool that may or may not cover the full designated record set.

### Key Findings

1. **No data dictionary exists in any publicly available artifact.** The registered (b)(10) URL documents how to use the ExportBuilder tool but provides zero information about what data can be exported. This is the most significant finding — the documentation describes the mechanism, not the content.

2. **Critical documentation is behind a login wall.** The ReportBuilder articles (which would list available data fields per module) require Zendesk authentication. Without these, neither patients, providers, nor third parties can determine what data the (b)(10) export covers.

3. **Only 3 ExportBuilder modules are explicitly confirmed** (Demographics, Progress Notes, HMIS History), plus 5 sub-export modules (Hospital Episodes, Allergies, Medications, Job Placements, Job Interviews). Major product domains — billing, treatment plans, labs, vitals, immunizations, behavioral health assessments — have no confirmed ExportBuilder coverage.

4. **The HMIS Data Export is the strongest component**, with dedicated export types (Full, HIC, RHY, Full+), FormBuilder custom form inclusion, and reference to the HUD HMIS CSV specification. This covers the HMIS domain well but is a specialized HUD compliance tool, not a general EHI export.

5. **No sample data, no schema, no machine-readable artifacts** of any kind. A recipient of an ExportBuilder export would receive a CSV/XLS/XML file with user-chosen fields, no documentation of what those fields mean, and no standard schema to reference.

### Summary Stats

    Coverage:        Minimal/stub/unclear
    Approach:        Unclear/undetermined (pre-existing tool repurposed; not C-CDA/FHIR repackaging)
    Export format:   CSV, TXT, XLS, XML (user-configurable)
    Entities:        8 confirmed modules (3 ExportBuilders + 5 sub-export modules); actual total unknown
    Fields:          N/A (no data dictionary; only 12 fields documented in HMIS ServicesOther.csv)
    Descriptions:    N/A
    Sample data:     No
    Bulk export:     Yes (multi-patient supported; 2-year date range limit per run)
    Domains covered: 1 of 22 confirmed (HMIS); 6 partial; 15 unconfirmed

### Bottom Line

The AWARDS (b)(10) EHI export documentation points to a general-purpose export tool (ExportBuilder) without providing any information about what data can actually be exported. A patient requesting their complete health record would receive no guidance on which ExportBuilders to use, what fields are available, or whether the export covers billing, labs, assessments, or other key domains. The single biggest gap is the complete absence of a data dictionary — the publicly registered documentation tells you *how* to export but never tells you *what* you can export.
