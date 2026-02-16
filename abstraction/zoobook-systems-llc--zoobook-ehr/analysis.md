# EHI Export Analysis: Zoobook Systems LLC

**Product**: Zoobook EHR 2.0
**Analysis date**: 2026-02-15
**CHPL IDs**: 15.04.04.3008.Zoob.02.00.1.171231 (CHPL product #9268)

## 1. Product Context

Zoobook EHR is a cloud-based electronic health record and practice management system built specifically for behavioral health, mental health, and addiction treatment facilities. It targets outpatient clinics, inpatient/residential treatment centers, detox units, and methadone/MAT (Medication-Assisted Treatment) clinics. The system is hosted on Amazon servers and used by small-to-medium behavioral health organizations.

Relevant data domains the product stores (based on product research and visible application navigation):

- **Clinical documentation**: Progress notes, assessments, treatment plans, care plans, psychosocial evaluations, CPST notes, psychiatric progress notes, mental health assessments, counseling reports, pre-admission documents
- **Medication management**: Medication lists, e-prescribing records, methadone dosing and take-home tracking (Methasoft integration)
- **Lab integration**: LabCorp/Quest connections, urine/toxicology test results
- **Billing and claims**: Automated billing, claims (EDI 837), insurance eligibility, payments, co-pay management, Medicaid batch billing, fee schedules — visible as "Billing" and "Client Invoicing/Payment" tabs in the application navigation
- **Scheduling**: Appointments, attendance tracking, no-show monitoring
- **Bed management**: Bed utilization tracking for residential providers
- **HR/staff data**: Employment records, credentials, payroll (visible as "Payroll" and "Employee" tabs)
- **Communication**: Secure messaging, faxes (Interfax), SMS, telehealth (Zoom)
- **Patient portal**: Patient-facing records and interactions (iOS/Android apps)
- **Quality measures**: 11 certified CQMs (depression screening, suicide risk, tobacco use, etc.)
- **Referral management**: Referral tracking and intake workflows
- **Specialty-specific**: Behavioral health assessments, substance abuse treatment records, group curriculum

The application navigation bar (visible in page 1 screenshot) confirms the product has dedicated tabs for: Dashboard, Call Center, Clients, Employee, Appointments, Lab Results, Group Curriculum, Billing, Client Invoicing/Payment, Payroll, Quality, Reports, Meetings/Group Supervision, Policies, Contracts, Marketing.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/EHIexportDocumentation.pdf` | 5-page PDF user guide (389 KB), created 2023-11-28 in Microsoft Word 2016. Contains annotated screenshots walking through the EHI export UI. Shows filter parameters (date range, clients, modules), sample export records, 172-module business rules picker (6 module names visible), and role-based access configuration (20 roles). **Does not contain** a data dictionary, export format specification, schema, field-level documentation, or sample data. | **Primary artifact but low informational value** — it shows *how to click buttons* but not *what the export contains* |
| Vendor disclosures page (`zoobooksystems.com/disclosures/`) | Live web page with certification details, real-world testing plan, data access policy, and third-party provider information. EHI export section describes 6 testing objectives (accuracy, usability, RBAC, date range, batch export, transmission). Confirms batch export capability. Data access policy reveals post-termination bulk extraction costs $25,000 (SQL format on encrypted media). | **Supplementary** — confirms batch export exists and post-termination pricing, but no export format or content details |

**No data dictionary, schema, sample data, or format specification exists in any artifact.**

## 3. Export Mechanics

- **Format**: **Unknown.** The documentation does not state the export file format anywhere. The disclosures page mentions "validation of format, structure, and completeness" in real-world testing objectives but never names the format. Post-termination bulk extraction is provided in "SQL format" on encrypted physical media, but this may be a different mechanism than the in-product EHI export.
- **Mechanism**: UI-based. Users navigate to Settings → EHI Export, set filter parameters (date range, clients, modules), and click "Generate." Exports are retrievable via a Download button or a public URL.
- **Single-patient vs bulk**: The interface supports selecting specific clients and specific modules. The real-world testing plan includes a "Batch Export Efficiency" objective (target: batch processing time ≤ 1.5× individual export time), confirming multi-patient/batch capability.
- **Access constraints**: Role-based access controls determine which user roles can generate exports (20 roles visible, all checked in the screenshot). Administrators can exclude specific modules from the export via Business Rules configuration.
- **Fees**: No fees mentioned for in-product EHI export during active contract. Post-termination: bulk data extraction costs $25,000 (SQL on encrypted media), or $200/month for ongoing storage access. Individual file access: $180/service request + $30/file over 10 files.

## 4. Export Content: What's In It

### What's known

The export is **module-based**: the system has 172 internal modules, and administrators can select which modules are included or excluded from the export. This is the only structural information available about the export content.

### What's visible

From the screenshots, only **8 module names** are identifiable (6 from the business rules picker on page 4, 2 from sample export records on page 2):

| Module ID | Module Name | Source |
|---|---|---|
| 253 | Psychiatric Progress Note | Page 2, sample export record |
| 246 | Mental Health Assessment | Page 2, sample export record |
| 836 | Client Notes To File | Page 4, business rules (excluded/unchecked) |
| 842 | PHI Disclosure Log | Page 4, business rules |
| 853 | CPST Note | Page 4, business rules |
| 1841 | Counseling Monthly Individual Progress Report | Page 4, business rules |
| 811 | Comprehensive Psychosocial Evaluation | Page 4, business rules |
| 883 | Pre-Admission Documents | Page 4, business rules |

All 8 visible modules are clinical documentation/form types. There are **zero visible modules** for medications, labs, billing, scheduling, bed management, referrals, or any non-clinical domain.

### What's unknown

- **164 of 172 module names** (96%) are not visible or documented
- **Export file format** (CSV? JSON? PDF? ZIP? Database dump?)
- **Data structure** within exported files (field names, types, relationships)
- **Whether the 172 modules cover all EHI domains** or only clinical forms/notes
- **Whether structured data (medications, labs, billing) is exported** or only document-type modules
- **Value sets, coded fields, foreign keys** — no information

### Vendor's own content organization

The vendor organizes export content by "modules" but does not provide a module listing or categorization. The 8 visible module names suggest modules correspond to individual clinical form types (progress notes, assessments, evaluations) rather than data tables (medications, lab_results, claims). It is unknown whether modules like "Billing" or "Lab Results" exist among the 172.

**No data dictionary exists.** There are no entities, fields, descriptions, types, or relationships documented. A table of export content cannot be constructed from the available artifacts.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor's documentation reveals almost nothing about export content. The only evidence is:

1. **172 modules are available** for export — this is architecturally promising if modules cover all data domains
2. **8 visible module names are all clinical forms**: psychiatric progress notes, mental health assessments, psychosocial evaluations, CPST notes, pre-admission documents, counseling reports, PHI disclosure logs
3. **The module ID space is non-sequential** (IDs range from 246 to 1841), suggesting modules are added over time as the product evolves
4. **Module selection is configurable** — administrators can exclude modules, meaning the "default" export may not include everything

There is no way to assess depth, breadth, or completeness from the available artifacts. The documentation provides zero field-level detail.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ❓ Unknown | No demographics module visible among the 8 shown | Product stores demographics (certified (a)(5)); unknown if included in the 164 unseen modules |
| Encounters / visits | ❓ Unknown | No encounter module visible | Product tracks appointments and attendance; unknown if in export |
| Problems / conditions / diagnoses | ❓ Unknown | Not visible in module list | Product stores diagnoses; unknown if in export |
| Medications / prescriptions | ❓ Unknown | Not visible in module list | Product has e-prescribing and methadone dosing; unknown if in export |
| Allergies | ❓ Unknown | Not visible in module list | Product stores allergies (CPOE drug-allergy checks certified); unknown if in export |
| Immunizations | N/A | Not visible | Behavioral health EHR — immunizations likely not a primary function |
| Vitals | ❓ Unknown | Not visible | Product may store vitals (BMI CQM certified); unknown if in export |
| Lab results | ❓ Unknown | Not visible in module list | Product integrates with LabCorp/Quest and has "Lab Results" nav tab; unknown if in export |
| Imaging / diagnostic reports | N/A | Not visible | Behavioral health EHR — imaging not a primary function |
| Procedures | ❓ Unknown | Not visible | Unknown if applicable or exported |
| Clinical notes / documents | ⚠️ Likely partial | 7 of 8 visible modules are clinical note types (Psychiatric Progress Note, Mental Health Assessment, CPST Note, etc.) | Only 7 note types visible; product likely has many more among the 172 modules |
| Care plans / goals | ❓ Unknown | Not visible | Product stores treatment plans; unknown if in export |
| Orders / referrals | ❓ Unknown | Not visible | Product has referral management; unknown if in export |
| Insurance / coverage | ❓ Unknown | Not visible | Product verifies insurance eligibility; unknown if in export |
| Claims / billing | ❓ Unknown | Not visible in module list | Product has extensive billing (EDI 837, Medicaid batch, fee schedules); "Billing" and "Client Invoicing/Payment" are major nav tabs; unknown if in export |
| Payments | ❓ Unknown | Not visible | Product tracks payments and co-pays; unknown if in export |
| Consents / directives | ❓ Unknown | Not visible | Unknown |
| Patient communications | ❓ Unknown | Not visible | Product has secure messaging, fax, SMS; unknown if in export |
| Specialty-specific (behavioral health) | ⚠️ Likely partial | Visible modules include behavioral health-specific forms (CPST Note, Comprehensive Psychosocial Evaluation, Mental Health Assessment, Counseling Progress Report) | Only a handful of specialty forms visible; product likely has many more assessment types |

**Summary**: Of 17 applicable domains, **0 can be confirmed as covered**, **2 are likely partially covered** (clinical notes and specialty-specific), and **15 are completely unknown**. The documentation is insufficient to make any definitive coverage claims.

The critical question — whether billing, medications, labs, demographics, and other structured data domains are among the 172 modules — cannot be answered from the artifacts.

## 6. Documentation Quality

**The documentation is severely deficient.** Specifically:

- **No data dictionary**: Zero tables, fields, types, descriptions, relationships, or value sets are documented
- **No format specification**: The export file format is never stated — a recipient would not know whether they're downloading a PDF, CSV, JSON, XML, SQL dump, or ZIP archive
- **No schema or sample data**: No machine-readable artifacts exist
- **No module listing**: Only 8 of 172 module names are visible (by accident, in screenshots); the remaining 164 are undocumented
- **UI-only documentation**: The entire 5-page PDF shows how to navigate the application interface, not what the export produces
- **No import guidance**: A developer receiving an export would have no information about how to parse, interpret, or import the data

**Could a developer build an import from this documentation?** No. A developer would not know the file format, let alone the data structure. The documentation is usable only for clicking through the Zoobook UI to generate an export — it says nothing about what comes out.

**Positive note**: The disclosures page's real-world testing plan demonstrates that the vendor has tested export functionality (accuracy, batch efficiency, RBAC, date range accuracy, transmission reliability). The export mechanism itself may work; the problem is that it's completely undocumented.

## 7. Overall Assessment

### Classification

**Minimal/stub**

The documentation is too thin to assess what the export actually contains. While the system appears to have a functional export mechanism with 172 modules and batch capability — which is architecturally promising — the complete absence of a data dictionary, format specification, module listing, or sample data means there is no way to verify what data is exported, in what format, or with what completeness. The documentation is a 5-page UI walkthrough, not a technical specification.

### Key Findings

1. **No data dictionary or format specification exists.** The sole artifact is a 5-page PDF showing how to click through the export UI. The export file format is never stated. Zero fields, types, relationships, or value sets are documented. (Source: `downloads/EHIexportDocumentation.pdf`, all 5 pages)

2. **172 modules are available for export, but only 8 names are visible.** The module picker screenshot shows "172 selected" but only 6 module names are readable; 2 more appear in sample export records. All 8 visible modules are clinical form types. Whether billing, medication, lab, or demographic modules exist among the remaining 164 is unknown. (Source: `EHIexportDocumentation.pdf`, pages 2 and 4)

3. **The product stores extensive data across many domains that may or may not be in the export.** The application navigation confirms tabs for Billing, Client Invoicing/Payment, Payroll, Lab Results, Appointments, and Employee — yet none of these domains appear in the visible export modules. (Source: `EHIexportDocumentation.pdf`, page 1 navigation bar)

4. **Batch export is confirmed but details are absent.** The vendor's real-world testing plan includes a "Batch Export Efficiency" objective, confirming multi-patient export exists. But no documentation describes how it works or what it produces. (Source: `zoobooksystems.com/disclosures/`, RWT Report ID 2, Objective 5)

5. **Post-termination data extraction costs $25,000 in SQL format.** The vendor's data access policy reveals that after contract termination, bulk clinical data extraction is provided on encrypted physical media for $25,000. This is separate from the in-product EHI export. (Source: `zoobooksystems.com/disclosures/`, Data Access and Retrieval Policy)

### Summary Stats

```
Classification:  Minimal/stub
Export format:   Unknown (not documented)
Model type:      Unknown (module-based, but structure undescribed)
Entities:        172 modules available (only 8 names visible)
Fields:          N/A (no field-level documentation)
Descriptions:    N/A
Sample data:     No
Bulk export:     Yes (confirmed in real-world testing plan)
Domains covered: 0 of 15 confirmed; 2 of 15 likely partial; 13 unknown
```

### Bottom Line

Zoobook's EHI export documentation is a 5-page screenshot walkthrough that tells users how to click buttons but says nothing about what the export actually contains or produces. Despite the product storing rich behavioral health, billing, and medication data across 172 internal modules, the absence of any data dictionary, format specification, module listing, or sample data makes it impossible to assess whether this export meets the (b)(10) requirement for exporting "all electronic health information." The single biggest gap is the complete lack of technical documentation — the export may be comprehensive under the hood, but there is zero evidence to evaluate that claim.
