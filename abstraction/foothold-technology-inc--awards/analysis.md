# EHI Export Analysis: Foothold Technology, Inc.

**Product**: AWARDS 3.0
**Analysis date**: 2026-02-15
**CHPL ID**: 15.04.04.1500.AWAR.03.00.1.171220 (ID 9267)

## 1. Product Context

AWARDS is a web-based EHR and case management system purpose-built for **nonprofit human services and behavioral health organizations**. It is notably the only system federally certified as both a Behavioral Health EHR and a HUD-mandated Homeless Management Information System (HMIS). The product serves 1,000+ provider agencies across 28 states, with a strong presence in New York and New Jersey.

AWARDS stores data across these key domains relevant to EHI export completeness:

- **Clinical health records**: Demographics, diagnoses/problem lists, medications (including e-prescribing), allergies, vital signs, lab orders/results, immunizations, clinical progress notes, treatment plans, assessments, family health history, implantable devices, procedures
- **Case management/program data**: Service documentation, program enrollment/participation/discharge, multi-program coordination, scheduling
- **HMIS/housing data**: Housing status/history, homelessness episodes, income/benefits, health insurance status, disabilities, domestic violence indicators, HUD Universal Data Elements
- **Billing**: Billing records and claims integrated with service documentation (built into the core platform)
- **Custom data**: Agency-defined forms via FormBuilder (arbitrary data structures)
- **Specialty clinical data**: Behavioral health assessments, substance use disorder treatment records, developmental disability services data

The Mandatory Disclosures PDF (page 3, section on g(6)) confirms the following AWARDS modules store clinical data: Demographics, Medications, Allergies, Diagnoses, Functional/Cognitive Status, Encounters (or Progress Notes as Encounters), Procedures, Progress Notes, Family Health History, Implantable Devices, Immunizations, Lab Orders.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/exportbuilders-main.html` (193 KB) | Main ExportBuilders Zendesk help article — the registered (b)(10) URL. 32K chars of article text. Describes the ExportBuilder tool's UI workflow in detail. **Does NOT contain a data dictionary or field listing.** | ⭐⭐⭐ Most informative for understanding the export mechanism |
| `downloads/mandatory-disclosures-dec-2024.pdf` (281 KB, 7 pages) | Official ONC mandatory disclosures. Contains the (b)(10) statement describing ExportBuilder for single/multiple patient export in CSV, XLS, or XML. No cost/fees for EHI export. | ⭐⭐⭐ Key for official (b)(10) description |
| `downloads/hmis-data-export.html` (275 KB) | HMIS Data Export article — describes the separate HUD-compliant CSV export. Lists CSV file types, service types, and Full+ export with FormBuilder data. | ⭐⭐ Useful for understanding HMIS-specific export |
| `downloads/fhir-api-docs.html` (44 KB) | Static HTML capture of FHIR API docs (Postman-style, lazy-loaded). Minimal content in static capture. | ⭐ Low — static capture is mostly empty |
| Postman Collection JSON (fetched live from API) | Full Postman collection for FHIR R4 API documentation. Lists 24 FHIR resource types with sample responses. | ⭐⭐ Useful for (g)(10) comparison only — this is NOT the (b)(10) export |
| `downloads/costs-and-limitations.pdf` (161 KB, 4 pages) | 2020-era costs and limitations for 2015 Edition criteria. Predates Cures Act (b)(10). | ⭐ Minimal relevance |
| `downloads/exportbuilder-section.html` (24 KB) | Zendesk section index page; contains only the one ExportBuilders article. | ⭐ Minimal |
| `downloads/screenshot-exportbuilders-full.png` (3.9 MB) | Full-page screenshot of ExportBuilders article. | ⭐ Confirms article content |
| `downloads/images/` (4 icon files, 245–653 bytes each) | Tiny UI button icons (add, combine, split, delete). | ⭐ No analytical value |

## 3. Export Mechanics

**Format**: CSV, TXT (fixed-width or delimited), XLS, or XML — user-selectable per export.

**Mechanism**: The ExportBuilder is a UI-based tool within AWARDS. Each AWARDS module (Demographics, Medical, Employment, HMIS, Progress Notes, etc.) has its own ReportBuilder, and the ExportBuilder extends each ReportBuilder with export file generation. Users must:
1. Navigate to the desired module's ReportBuilder
2. Check "Provide ExportBuilder Options"
3. Select date range (max 2 years per export, except HMIS History)
4. Choose client scope (single patient, matching records, or all clients)
5. Select data fields to include
6. Configure field formatting, ordering, mapping
7. Generate the export file

**Single-patient vs bulk**: Both supported. "Select Client" for single-patient; "All Clients" or "Clients with Records" for bulk.

**Sub-exports**: The Demographics ExportBuilder can embed saved export formats from other modules (Hospital Episodes, Medical Allergies, Medical Medications, Employment Job Placements, Employment Job Interviews) as XML sub-exports.

**Delivery**: Files saved to computer or sent to AWARDS Messages inbox (retained 1 month). Exports can be scheduled.

**Access constraints**: Requires user permissions for each module's ReportBuilder. The ExportBuilder documentation explicitly warns it is "designed for use by individuals who are familiar with export files and formats." No cost or fees per mandatory disclosures.

**Key limitation**: There is no single "Export All EHI" button. A complete EHI export requires navigating to each module's ExportBuilder separately, configuring field selections for each, and generating multiple files. No documentation exists describing which ExportBuilders to use or in what combination to achieve a complete EHI export.

## 4. Export Content: What's In It

### The core problem: No data dictionary

The ExportBuilder documentation describes the **tool** (how to configure and run exports) but provides **zero information about the data** available for export. Specifically:

- **No field listings**: The documentation does not list any of the data fields available in any ExportBuilder module
- **No data types** beyond generic format categories (Text, Numeric, Date, Time, Date/Time, Yes/No, List, Phone)
- **No table/entity definitions**
- **No value sets or coded field documentation**
- **No relationship/foreign key documentation**
- **No sample export files**
- **No machine-readable schemas**

The documentation states that "the specific data variables you see are based on the ReportBuilder through which you have accessed this ExportBuilder" and directs users to the individual ReportBuilder instructions. **Those ReportBuilder articles are behind a login wall** (HTTP 403 verified on all three tested URLs: articles 366712240208, 366711613001, 331330615182).

### What we can identify from available evidence

**ExportBuilder modules confirmed by name** (from `exportbuilders-main.html`):

| Module | Evidence | Sub-export capable | Fields documented |
|---|---|---|---|
| Demographics ExportBuilder | Used as primary example throughout article | Yes (5 sub-export sources) | No |
| HMIS History ExportBuilder | Mentioned as exception to 2-year date limit | No | No |
| HMIS ExportBuilder | Referenced alongside Demographics ExportBuilder | No | No |
| Progress Notes ExportBuilder | Mentioned in FormBuilder integration context | No | No |

**Modules implied by sub-export sources** (these must have their own ExportBuilders for the sub-export mechanism to work):

| Module | Evidence |
|---|---|
| Hospital > Episodes | Listed as sub-export source for Demographics |
| Medical > Allergies | Listed as sub-export source for Demographics |
| Medical > Medications | Listed as sub-export source for Demographics |
| Employment > Jobs > Job Placements | Listed as sub-export source for Demographics |
| Employment > Jobs > Job Interviews | Listed as sub-export source for Demographics |

**Module implied by permissions reference**:

| Module | Evidence |
|---|---|
| Intake/Admission | "you will not have access to Intake reports if you do not have access to the Intake/Admission module" |

**Total known ExportBuilder modules: ~10** (4 confirmed + 5 implied from sub-exports + 1 implied from permissions). The actual number is unknown — the mandatory disclosures' C-CDA section lists 12 clinical data modules (Demographics, Medications, Allergies, Diagnoses, Functional/Cognitive Status, Encounters, Procedures, Progress Notes, Family Health History, Implantable Devices, Immunizations, Lab Orders), suggesting at least some of these have corresponding ExportBuilders, but this cannot be confirmed.

### HMIS Data Export (separate from ExportBuilder)

The HMIS Data Export is a separate feature producing HUD-compliant zipped CSV files. The "Full" export type generates ~14 CSV files per the HUD HMIS CSV specification. The "Full+" type adds FormBuilder custom form data as additional CSV files and a `ServicesOther.csv` with service contact details.

The HMIS CSV file set includes: Client.csv, Enrollment.csv, EnrollmentCoC.csv, Export.csv, Event.csv, Services.csv, Assessment.csv, AssessmentQuestions.csv, AssessmentResults.csv, Project.csv, ProgramCoC.csv, Inventory.csv, Site.csv, User.csv.

This export follows an external HUD standard (hudhdx.info/VendorResources.aspx), not a vendor-specific data dictionary.

### FHIR API (g)(10) — NOT the (b)(10) export

The FHIR R4 API (at fhir-docs.footholdtechnology.com) supports 24 resource types with US Core STU 6.1.0 profiles and USCDI v3. It includes Bulk Data Access. This is explicitly the (g)(10) standardized API and is **not** the (b)(10) EHI export mechanism. The 24 resources are: AllergyIntolerance, CarePlan, CareTeam, Condition, Coverage, Device, DiagnosticReport, DocumentReference, Encounter, Goal, Immunization, Location, Medication, MedicationDispense, MedicationRequest, Observation, Organization, Patient, Practitioner, Procedure, Provenance, RelatedPerson, ServiceRequest, Specimen.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor's (b)(10) export documentation describes ExportBuilder as a general-purpose, user-configurable export tool available "for data to which they have access throughout the system." The vendor does not organize the export documentation into data domains or categories. Instead, the tool is organized by AWARDS modules (Demographics, Medical, Hospital, Employment, HMIS, Progress Notes, etc.), each with its own ReportBuilder/ExportBuilder.

**What's confirmable**: The Demographics ExportBuilder exists and can pull in data from Hospital Episodes, Medical Allergies, Medical Medications, and Employment modules via sub-exports. The HMIS and Progress Notes ExportBuilders are confirmed to exist. FormBuilder custom fields can be included when configured.

**What's not confirmable**: Whether ExportBuilders exist for billing, treatment plans, diagnoses, lab results, vital signs, immunizations, procedures, service documentation, intake/assessments, care plans, or program enrollment data. The documentation does not mention billing at all. The login-walled ReportBuilder documentation would presumably list the available fields for each module, but this is inaccessible.

**Coverage depth**: Unknown. With zero fields documented in any module, it is impossible to assess whether any domain has thin or thorough coverage.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | Demographics ExportBuilder confirmed to exist; fields unknown | Module exists but no field listing; cannot verify completeness |
| Encounters / visits | ⚠️ Partial | Mandatory disclosures mention "Encounters (or Progress Notes as Encounters)" as C-CDA module; no ExportBuilder confirmed | Product stores encounters; coverage uncertain |
| Problems / conditions / diagnoses | ⚠️ Partial | Mandatory disclosures list "Diagnoses" as C-CDA module; no ExportBuilder confirmed | Product stores diagnoses; coverage uncertain |
| Medications / prescriptions | ⚠️ Partial | Medical > Medications sub-export source confirmed; e-prescribing is a core module | Sub-export exists; standalone ExportBuilder unconfirmed |
| Allergies | ⚠️ Partial | Medical > Allergies sub-export source confirmed | Sub-export exists; standalone ExportBuilder unconfirmed |
| Immunizations | ⚠️ Partial | Listed as C-CDA module; no ExportBuilder confirmed | Product stores immunizations; coverage uncertain |
| Vitals | ❌ Not confirmed | Not mentioned in ExportBuilder docs | Product stores vitals; no evidence of export coverage |
| Lab results | ⚠️ Partial | "Lab Orders" listed as C-CDA module; no ExportBuilder confirmed | Product has e-Labs module; coverage uncertain |
| Imaging / diagnostic reports | ❌ Not confirmed | Not mentioned in ExportBuilder docs | "Diagnostic Test Info" mentioned in mandatory disclosures for CPOE; export coverage uncertain |
| Procedures | ⚠️ Partial | Listed as C-CDA module; no ExportBuilder confirmed | Coverage uncertain |
| Clinical notes / documents | ⚠️ Partial | Progress Notes ExportBuilder confirmed | Exists but fields unknown |
| Care plans / goals | ❌ Not confirmed | Not mentioned in ExportBuilder docs | Product has treatment planning; no export evidence |
| Orders / referrals | ❌ Not confirmed | Not mentioned in ExportBuilder docs | Product supports CPOE; no export evidence |
| Insurance / coverage | ❌ Not confirmed | Not mentioned in ExportBuilder docs | HMIS tracks health insurance status; no general export evidence |
| Claims / billing | ❌ Not confirmed | "Billing" not mentioned once in ExportBuilder article | Product has integrated billing; significant potential gap |
| Payments | ❌ Not confirmed | Not mentioned | If billing exists, payments likely do too; no export evidence |
| Consents / directives | ❌ Not confirmed | Not mentioned | Unknown if product stores these |
| Patient communications | ❌ Not confirmed | Not mentioned | Patient portal exists but export of portal messages not evidenced |
| Specialty: Behavioral health assessments | ⚠️ Partial | FormBuilder fields can be included in ExportBuilders when configured | Custom BH assessments via FormBuilder may be exportable |
| Specialty: HMIS/housing data | ✅ Covered | Dedicated HMIS Data Export with Full/Full+ modes; ~14 CSV files per HUD spec | Covered by separate HMIS export feature, though this is a HUD-standard projection, not native export |
| Specialty: Substance use disorder | ❌ Not confirmed | Not explicitly mentioned in export docs | Product serves SUD providers; coverage uncertain |
| Specialty: Developmental disabilities | ❌ Not confirmed | Not mentioned in export docs | Product serves I/DD providers; coverage uncertain |

## 6. Documentation Quality

**Can a developer understand and use the export from these docs?** A developer could understand *how to operate the ExportBuilder tool* — the 32K-character article provides detailed step-by-step UI instructions. However, a developer could not:

- Know what fields are available for export in any module
- Build an import process for received export files (no schema, no field definitions)
- Verify that a complete EHI export has been performed (no checklist of modules/fields)
- Understand the data model or relationships between exported entities

**What's well-documented**: The ExportBuilder UI workflow, export format options (CSV/TXT/XLS/XML), field configuration features (value mapping, boolean formats, date formats), sub-export mechanism, FormBuilder integration concept, and client selection options.

**What requires guesswork**: Everything about the actual data content. The documentation is entirely about the *tool* and says nothing about the *data*.

**Machine-readable artifacts**: None. No schemas, no sample data, no data dictionaries, no JSON/XML specifications. The FHIR API has a Postman collection, but that's for (g)(10), not (b)(10).

**A critical gap**: The ReportBuilder articles that would list the available data fields for each module are behind a Zendesk login wall (HTTP 403 verified). This means the publicly accessible documentation registered for (b)(10) certification provides no information about what data can be exported.

## 7. Overall Assessment

### Classification

**Minimal/stub**

The vendor has pointed its (b)(10) EHI export certification at a general-purpose data export tool (ExportBuilder) that exists within the product. The ExportBuilder tool itself appears functional and flexible — it supports multiple formats, user-configurable field selection, and both single-patient and multi-patient export. However, the *documentation* provides zero information about what data is actually available for export. There is no data dictionary, no field listing, no sample data, no schema, and the key reference documentation (ReportBuilder field listings) is behind a login wall. It is impossible to assess from publicly available documentation whether this tool provides access to all EHI or only a fraction of it. The documentation essentially says "we have an export tool; trust us that it covers everything" without providing evidence.

### Key Findings

1. **No data dictionary or field listing exists in the public documentation.** The registered (b)(10) URL (ExportBuilders article) describes how to use the export tool but lists zero data fields available for export. This is the most fundamental gap — there is no way to assess export completeness without knowing what's in the export. (Source: `exportbuilders-main.html`, verified by parsing)

2. **Key documentation is behind a login wall.** The ReportBuilder articles that would list available data fields (articles 366712240208, 366711613001, 331330615182) all return HTTP 403. The publicly registered (b)(10) documentation directs users to these inaccessible articles for field-level detail. (Verified 2026-02-15)

3. **Billing is never mentioned in the export documentation.** Despite AWARDS having integrated billing as a core feature, the word "billing" does not appear in the ExportBuilder article. This suggests billing data may not be covered by the export, which would be a significant EHI gap. (Source: text search of `exportbuilders-main.html` — 0 matches for "billing")

4. **The export requires expert manual configuration across multiple modules.** There is no "Export All EHI" operation. Users must navigate to each module's ExportBuilder, select fields, and generate separate export files. The documentation warns the tool is "designed for use by individuals who are familiar with export files and formats." No guidance exists for performing a complete EHI export. (Source: `exportbuilders-main.html`)

5. **The FHIR API (g)(10) covers more identified clinical domains than the documented (b)(10) export.** The FHIR API documents 24 resource types including encounters, conditions, immunizations, procedures, and observations (vitals/labs) — none of which are confirmed as having ExportBuilder modules. This creates an ironic situation where the (g)(10) API appears more complete than the (b)(10) "all EHI" export, at least based on available documentation. (Source: Postman collection at fhir-docs.footholdtechnology.com)

### Summary Stats

```
Classification:  Minimal/stub
Export format:   CSV, TXT, XLS, XML (user-selectable)
Model type:      Native database (ad-hoc, user-configured field selection)
Entities:        ~10 ExportBuilder modules identified (actual total unknown)
Fields:          N/A (no field listing in public documentation)
Descriptions:    N/A
Sample data:     No
Bulk export:     Yes (multi-patient supported per module)
Domains covered: 1-2 of 17 applicable domains confirmed; ~8 partially evidenced
```

### Bottom Line

AWARDS' (b)(10) EHI export points to a general-purpose export tool (ExportBuilder) that may well be capable of exporting comprehensive data — but the public documentation provides no evidence of what data is actually available. With no data dictionary, no field listings, no sample data, and key reference documentation behind a login wall, it is impossible to verify that this export covers all electronic health information. The single biggest gap is the complete absence of data content documentation: a patient, provider, or developer receiving an AWARDS export would have no publicly available reference to understand what data they should expect or verify they received.
