# EHI Export Analysis: Zoobook Systems LLC

**Product**: Zoobook EHR 2.0
**Analysis date**: 2026-02-16
**CHPL IDs**: 9268 (15.04.04.3008.Zoob.02.00.1.171231)

## 1. Product Context

Zoobook EHR is a cloud-based electronic health record and practice management system built exclusively for **behavioral health, mental health, and addiction treatment** settings. It targets outpatient clinics, inpatient/residential treatment centers, detox facilities, and methadone/MAT clinics. The product is a single integrated platform — there are no separate tiers or modules sold independently.

Based on vendor website research and screenshots within the documentation, Zoobook stores data across these domains relevant to EHI completeness:

- **Clinical documentation**: Progress notes (psychiatric, CPST, counseling), assessments (comprehensive psychosocial, mental health, diagnostic), treatment plans, care plans, discharge plans
- **Medication management**: Medication lists, e-prescribing records, methadone dosing/take-home tracking (MAT)
- **Lab integration**: Lab orders/results (LabCorp, Quest), urine/toxicology screening
- **Billing & practice management**: Claims (EDI 837), payments, eligibility verification, co-pays, fee schedules, Medicaid batch billing, client invoicing
- **Scheduling & attendance**: Appointments, attendance tracking, no-show monitoring
- **Bed management**: Bed utilization for residential programs, associated billing
- **Referral management**: Referral tracking from sourcing through intake
- **HR/staffing**: Employment records, credentials, supervision hours, payroll
- **Communications**: Secure messaging, fax, SMS, email, telehealth (Zoom)
- **Patient portal**: Patient-facing records and interactions
- **Quality measures**: CQMs including depression screening, suicide risk assessment, tobacco screening
- **State reporting**: NJSAMS extracts for NJ regulatory reporting

The navigation bar visible in the PDF (page 1) confirms the breadth: Dashboard, Call Center, Clients, Employees, Appointments, Lab Results, Group Curriculum, Billing, Client Invoice/Payment, Payroll, Quality, Reports, Meetings/Group Supervision, Policies, Contracts, Marketing.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/EHIexportDocumentation.pdf` | 5-page PDF (389 KB, created 2023-11-28 in Microsoft Word 2016). UI walkthrough with annotated screenshots showing how to navigate to, configure, and generate EHI exports. Contains zero data dictionary, zero schema, zero format specification, zero sample data. | **Low** — documents the process of clicking buttons, not the content or format of what is exported |

This is the **sole artifact** available. There are no additional downloads, no supplementary data dictionaries, no sample export files, and no machine-readable schemas.

## 3. Export Mechanics

- **Format**: **Unknown.** The documentation does not specify the export file format anywhere — not CSV, JSON, PDF, XML, database dump, or any other format. The only clue is that each export produces a downloadable file accessible via a "Download Button" or "Public URL."
- **Mechanism**: UI-driven. Users navigate to Settings → EHI Export, set filters, and click "Generate."
- **Filters**: Date Range (creation/modification dates), Clients (individual selection), Modules (select from 172 available system modules)
- **Single-patient vs bulk**: The interface allows selecting specific clients, implying both single-patient and multi-patient exports are possible.
- **Access constraints**: Role-based. Administrators can control which of 20 user roles (from Administrative Staff to Super Administrator) can access the export function. Administrators can also configure Business Rules to exclude specific modules from the export.
- **Fees**: Not documented in the export PDF. The vendor's disclosures page (per product research) prices bulk data extraction at $25,000 or $200/month for ongoing storage access post-termination.

## 4. Export Content: What's In It

### The fundamental problem: no data dictionary

The documentation provides **zero field-level detail** about what the export contains. There is:

- **No data dictionary** — no tables, no fields, no types, no descriptions
- **No schema** — no JSON schema, no XSD, no database DDL
- **No format specification** — the file format of exports is not stated
- **No sample data** — no example exports are provided or described
- **No entity relationships** — no documentation of how data connects across modules
- **No value sets** — no coded values or terminology references

The only structured information about the export's content is:

1. **172 modules** are available for export (per the Business Rules screenshot, page 4)
2. **8 module names** are visible in screenshots:
   - Client Notes To File (excluded in the example configuration)
   - PHI Disclosure Log
   - CPST Note
   - Counseling Monthly Individual Progress Report
   - Comprehensive Psychosocial Evaluation
   - Pre-Admission Documents
   - Psychiatric Progress Note (from export records table)
   - Mental Health Assessment (from export records table)

3. **9 export listing columns** describe the UI table of completed exports (not the exported data itself): Client ID, Full Name, Module Name, URL, Start Date, End Date, Created By, Expiration Date, Download Button.

### Vendor's own content organization

The vendor does not organize content into categories. The only organizational structure is "modules" — and 164 of 172 module names are not disclosed. The visible modules are all clinical documentation types:

| Module Name | Fields | Described | Types | Category |
|---|---|---|---|---|
| PHI Disclosure Log | 0 | 0 | N/A | Unknown |
| CPST Note | 0 | 0 | N/A | Unknown |
| Counseling Monthly Individual Progress Report | 0 | 0 | N/A | Unknown |
| Comprehensive Psychosocial Evaluation | 0 | 0 | N/A | Unknown |
| Pre-Admission Documents | 0 | 0 | N/A | Unknown |
| Psychiatric Progress Note | 0 | 0 | N/A | Unknown |
| Mental Health Assessment | 0 | 0 | N/A | Unknown |
| Client Notes To File | 0 | 0 | N/A | Unknown (excluded by default) |
| *(164 additional modules)* | 0 | 0 | N/A | Unknown |

**Total entities documented**: 0 (172 claimed, 8 named, 0 with any field-level detail)
**Total fields documented**: 0
**Fields with descriptions**: 0

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

It is impossible to assess coverage from the documentation. The vendor claims 172 modules are available for export, which is a large number suggesting potential breadth, but provides no information about what those modules contain. The 8 visible module names are all behavioral health clinical documentation types (notes, assessments, evaluations), revealing nothing about whether billing, medications, labs, demographics, or other domains are represented in the remaining 164 modules.

The 172-module count is the only encouraging signal. A system with 172 exportable modules likely covers more than just clinical summaries — the navigation bar confirms the product has Billing, Payroll, Lab Results, Client Invoice/Payment, and other non-clinical modules. But whether these are among the 172 exportable modules is undocumented.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | No dedicated module visible; Client ID and Full Name appear in export listing | Product stores demographics (intake forms, patient records); no field-level detail available |
| Encounters / visits | ❌ Not covered | No encounter module visible | Product tracks appointments and attendance; no evidence in export |
| Problems / conditions / diagnoses | ❌ Not covered | No diagnostic module visible | Product stores diagnoses (certified for (a)(4) Problem List); no evidence in export |
| Medications / prescriptions | ❌ Not covered | No medication module visible | Product has e-prescribing and methadone dosing; no evidence in export |
| Allergies | ❌ Not covered | No allergy module visible | Certified for (a)(1) CPOE which implies allergy data; no evidence in export |
| Immunizations | ❌ Not covered | No immunization module visible | May store immunization data; no evidence in export |
| Vitals | ❌ Not covered | No vitals module visible | Likely stores vitals; no evidence in export |
| Lab results | ❌ Not covered | No lab module visible | Product integrates with LabCorp/Quest; nav bar shows "Lab Results"; no evidence in export |
| Imaging / diagnostic reports | ❌ Not covered | No imaging module visible | Likely limited in behavioral health context |
| Procedures | ❌ Not covered | No procedure module visible | Limited applicability for behavioral health |
| Clinical notes / documents | ⚠️ Partial | 7 clinical note/assessment modules visible by name | Product likely has many more note types among the 172 modules; visible modules are behavioral health-specific |
| Care plans / goals | ❌ Not covered | No care plan module visible | Product stores treatment plans; no evidence in export |
| Orders / referrals | ❌ Not covered | No orders/referral module visible | Product has referral management; nav bar shows no direct evidence |
| Insurance / coverage | ❌ Not covered | No insurance module visible | Product does eligibility verification; no evidence in export |
| Claims / billing | ❌ Not covered | No billing module visible | Product has full billing/claims (EDI 837, Medicaid batch); significant gap if absent |
| Payments | ❌ Not covered | No payment module visible | Product tracks payments, co-pays, credit cards; no evidence in export |
| Consents / directives | ❌ Not covered | No consent module visible; "Pre-Admission Documents" might include consents | Unknown |
| Patient communications | ❌ Not covered | No communication module visible | Product has secure messaging, SMS, fax, email; no evidence in export |
| Specialty-specific (behavioral health) | ⚠️ Partial | Visible modules include behavioral health-specific assessments (CPST Note, Comprehensive Psychosocial Evaluation, Mental Health Assessment) | Core specialty — more modules likely exist in the 172 but are not documented |

**Important caveat**: The "❌ Not covered" ratings above reflect the **documentation**, not necessarily the export itself. The 172 modules may well include billing, medications, labs, demographics, and other domains — but the documentation provides no evidence either way. The assessments are based solely on what is visible in screenshots.

## 6. Documentation Quality

The documentation quality is **very poor** from a technical standpoint:

- **Usability for developers**: A developer could not build an import from this documentation. The export format is not specified, no fields are documented, no schemas exist, and no sample data is provided.
- **Usability for end users**: The documentation adequately shows a user how to click through the UI to generate an export. It succeeds as a basic user guide.
- **Machine-readable artifacts**: None. No JSON schemas, no XSD, no CSV templates, no sample files.
- **What's well-documented**: The UI navigation path (Settings → EHI Export), the filter parameters (Date Range, Clients, Modules), and the role-based access control mechanism.
- **What requires guesswork**: Everything about the exported data itself — format, structure, fields, types, relationships, value sets, and which of the 172 modules cover which data domains.

The documentation describes **how to press the export button** but not **what comes out when you press it**.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Minimal/stub/unclear**

The documentation is too thin to assess coverage. While 172 modules are claimed, only 8 module names are visible (all clinical note types), and zero field-level documentation exists for any module. It is impossible to determine from the available artifacts whether the export covers billing, medications, labs, demographics, or any domain beyond a handful of behavioral health clinical note types. The 172-module count is suggestive of potential breadth, but without a module listing or data dictionary, this is speculation.

**Axis 2 — Export approach: Unclear/undetermined**

The architecture *suggests* a purpose-built EHI export — it has its own UI under Settings, module-based selection with 172 modules, date range filtering, and role-based access control. This is not obviously a repackaged C-CDA or FHIR export (the product has separate FHIR Settings and API documentation for (g)(10)). However, the documentation is so thin that it's impossible to confirm whether this is a genuine comprehensive export or a module-level document dump. The per-module structure (each export record shows one module for one client) suggests it may export individual clinical documents/forms rather than structured tabular data — but this too is speculation.

### Key Findings

1. **No data dictionary exists.** The documentation is a 5-page UI walkthrough (389 KB PDF, created 2023-11-28) with annotated screenshots. It contains zero field definitions, zero type specifications, zero format documentation, and zero sample data. This is the single most significant deficiency.

2. **Export format is completely undocumented.** Whether the export produces CSV, JSON, PDF, XML, or any other format is never stated. A recipient of an EHI export would have no documentation to help them parse or interpret the data.

3. **172 modules claimed, 8 named, 0 described.** The Business Rules screenshot shows 172 modules are selectable for export, but only 8 module names are visible in screenshots. All visible modules are behavioral health clinical documentation types (notes, assessments, evaluations). The remaining 164 modules are unknown.

4. **Architecture suggests purpose-built export.** The dedicated EHI Export UI with module selection, date filtering, Business Rules configuration, and role-based access is architecturally distinct from the product's FHIR API ((g)(10)). This is not a repackaged clinical exchange — but what it actually produces remains undocumented.

5. **Behavioral health product with known billing/PM capabilities.** The navigation bar confirms Billing, Payroll, Client Invoice/Payment, and other non-clinical modules exist in the product. Whether these are among the 172 exportable modules is the key unanswered question for (b)(10) compliance.

### Summary Stats

```
Coverage:        Minimal/stub/unclear
Approach:        Unclear/undetermined
Export format:   Unknown (not specified in documentation)
Entities:        172 claimed, 8 visible by name, 0 with field-level documentation
Fields:          N/A (no field documentation exists)
Descriptions:    N/A
Sample data:     No
Bulk export:     Unclear (client selection UI implies multi-patient possible)
Domains covered: Cannot assess — documentation too thin (at most 1 of 18 domains confirmed: clinical notes)
```

### Bottom Line

A patient or provider receiving this export would get a file of **unknown format** containing data of **unknown structure** from modules of **undisclosed content**. The vendor appears to have built a functional export mechanism with 172 selectable modules, but the complete absence of a data dictionary, format specification, or sample data means no recipient could independently parse, interpret, or use the exported information. The single biggest gap is the total lack of documentation about what the export actually contains.
