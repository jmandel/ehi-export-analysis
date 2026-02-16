# EHI Export Analysis: Zoobook Systems LLC

**Product**: Zoobook EHR 2.0  
**Analysis date**: 2026-02-16  
**CHPL IDs**: 15.04.04.3008.Zoob.02.00.1.171231 (CHPL ID 9268)

## 1. Product Context

Zoobook EHR is a cloud-based EHR and practice management platform built exclusively for behavioral health, mental health, and addiction treatment facilities. Target settings include outpatient behavioral health clinics, inpatient/residential treatment centers, detox facilities, and methadone/MAT clinics. The product is a single, integrated platform covering:

- **Clinical documentation**: Progress notes, assessments, treatment plans, care plans, AI-powered note-writing, customizable templates. Behavioral-health-specific forms (psychosocial evaluations, CPST notes, psychiatric progress notes, mental health assessments).
- **Medication management & e-prescribing**: Medication lists, e-prescribing, drug interaction checks, and native methadone dosing/take-home tracking (Methasoft integration).
- **Lab integration**: LabCorp, Quest, urine/toxicology testing.
- **Scheduling & attendance**: Appointments, staff scheduling, attendance tracking, no-show monitoring.
- **Bed management**: Residential bed utilization tracking and billing (a differentiating feature).
- **Billing & practice management**: Claims creation/submission (EDI 837), eligibility verification, payment tracking, Medicaid batch billing, fee schedules, co-pay management, credit card processing.
- **Referral management**: Tracking from sourcing through intake and follow-up.
- **HR & payroll**: Employment records, credentials, supervision hours, leave, productivity, payroll.
- **Communication**: Secure messaging, encrypted SMS, HIPAA-compliant fax, email, telehealth (Zoom), patient portal (web + iOS/Android).
- **Reporting & quality**: Pre-built and custom reports, analytics dashboards, 11 certified CQMs (depression, suicide risk, substance use screening), NJSAMS state reporting.
- **Interoperability**: C-CDA transitions of care, Direct messaging, FHIR API, EHI export.

The navigation bar visible in the PDF screenshot (page 1) confirms major functional areas: Dashboard, Call Center, Clients, Employees, Appointments, Lab Results, Group Curriculum, Billing, Client Invoicing/Payment, Payroll, Quality, Reports, Meetings/Group Supervision, Policies, Contacts, Marketing.

This product stores a broad range of EHI across clinical, billing, specialty behavioral health, and administrative domains. A complete (b)(10) export should cover all of these.

## 2. Artifacts Reviewed

| Artifact | Description | Informative? |
|---|---|---|
| `downloads/EHIexportDocumentation.pdf` | 5-page PDF (389 KB), created 2023-11-28 in Microsoft Word 2016. UI walkthrough showing how to navigate to and use the EHI Export feature. Contains annotated screenshots of the export interface, module picker, and role-based access settings. **No data dictionary, no schema, no format specification, no sample data.** | Low — tells us how to click buttons but nothing about what data is exported or in what format |
| Vendor disclosures page (`zoobooksystems.com/disclosures/`) | Real-world testing plan for (b)(10) with 6 testing objectives. Confirms batch export capability, role-based access, date range filtering. Mentions "validation of format, structure, and completeness" but does not name the format. | Low — confirms export exists and has basic features; no content detail |

**No additional artifacts were found.** The `downloads/` directory contains only the single PDF. The vendor's registered EHI documentation URL (`https://app.zoobooksystems.com/EHIexportDocumentation`) still returns the same 389,047-byte PDF as of 2026-02-16. No linked data dictionaries, schemas, sample files, or supplementary documentation exist at the vendor's disclosures page or API documentation page.

## 3. Export Mechanics

- **Format**: Unknown. The documentation does not specify whether the export produces CSV, JSON, PDF, XML, a ZIP archive, a database dump, or any other format. The disclosures page mentions "validation of format, structure, and completeness" but never names the format.
- **Mechanism**: UI-based. Users navigate to Settings → EHI Export, apply filters, and click "Generate." Results are retrieved via a Download Button or a Public URL.
- **Filters**: Date range (created/modified date), client selection, module selection. The export is per-client and per-module — each export record in the results table shows one client + one module combination.
- **Single-patient vs bulk**: Both implied. The UI allows selecting multiple clients and modules. The disclosures page's Real World Testing plan includes "Batch Export Efficiency" as Objective 5 (target: ≤1.5× individual export time).
- **Access constraints**: Role-based access control. Administrators configure which of 20 user roles can access the EHI Export function. The 20 roles visible are: Administrative Staff, Administrator, Assistant Clinical Director, Billers, Clerical, Client, Counselor, Director, Driver, Hr Staff, Intake, Intern/Trainee, Manager, Medical Staff, Provisional User, Receptionist, Sample Collector, Super Administrator, Supervisor, Support.
- **Module selection**: Administrators can configure "EHI Export Business Rules" to include/exclude specific modules. The screenshot shows 172 modules selected, with the ability to uncheck individual modules. This means the export's content scope is configurable and may vary by deployment.
- **Fees**: Not mentioned in the export documentation itself. However, the vendor's disclosures page describes post-termination data extraction pricing: $25,000 for bulk extraction or $200/month for ongoing storage access, $180 per service request + $30/file over 10 files.

## 4. Export Content: What's In It

### What the documentation reveals

The documentation provides **zero** field-level, table-level, or format-level detail about the export's content. There is:

- No data dictionary
- No schema definition
- No field names, types, or descriptions
- No value sets or coded values
- No relationship/foreign key documentation
- No sample data files
- No description of the export file format or structure

The only content information comes from:

1. **Module count**: The module picker shows "172 selected" — this is the total number of modules available for export.
2. **6 module names visible in the module picker** (PDF page 4):
   - 836: Client Notes To File (unchecked — excluded by default)
   - 842: PHI Disclosure Log
   - 853: CPST Note
   - 1841: Counseling Monthly Individual Progress Report
   - 811: Comprehensive Psychosocial Evaluation
   - 883: Pre-Admission Documents
3. **2 module names visible in sample export records** (PDF page 2):
   - 253: Psychiatric Progress Note
   - 246: Mental Health Assessment

That gives us **8 uniquely named modules out of 172** (4.7%). The remaining 164 modules are completely unidentified.

### Vendor's own content organization

The vendor organizes exports by "modules" — internal system modules that correspond to clinical forms, document types, or data categories. Each module has a numeric ID and a name. The export appears to produce one downloadable file per client-module combination.

| Module ID | Module Name | Fields Documented | Description | Category |
|---|---|---|---|---|
| 253 | Psychiatric Progress Note | 0 | None | Unknown |
| 246 | Mental Health Assessment | 0 | None | Unknown |
| 836 | Client Notes To File | 0 | None (excluded by default) | Unknown |
| 842 | PHI Disclosure Log | 0 | None | Unknown |
| 853 | CPST Note | 0 | None | Unknown |
| 1841 | Counseling Monthly Individual Progress Report | 0 | None | Unknown |
| 811 | Comprehensive Psychosocial Evaluation | 0 | None | Unknown |
| 883 | Pre-Admission Documents | 0 | None | Unknown |
| (164 more) | (not visible) | 0 | None | Unknown |

**Total modules**: 172 claimed, 8 named, 0 with any field-level documentation.  
**Total fields documented**: 0.  
**Fields with descriptions**: 0.  
**Fields with types**: 0.

The full inventory is saved to `analysis/full-entity-inventory.json`.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor does not organize their export documentation by domain or category — there are no categories at all. The 8 visible module names suggest the export covers at least some behavioral health clinical documentation types (psychiatric progress notes, mental health assessments, psychosocial evaluations, CPST notes, counseling reports, pre-admission documents). The module named "PHI Disclosure Log" suggests at least one administrative/compliance module is included.

The 172-module count is architecturally promising. Given that the product's navigation bar shows 16+ major functional areas (including Billing, Payroll, Lab Results, Appointments, etc.), it is plausible that many of these domains are represented among the 172 modules. However, **this cannot be verified from the documentation.** The vendor provides no module listing, no domain mapping, and no way to determine what the 164 unnamed modules contain.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ❓ Unknown | "Pre-Admission Documents" (module 883) may contain intake demographics, but no field-level detail | Product stores demographics (certified for (a)(5)); cannot verify coverage |
| Encounters / visits | ❓ Unknown | No module with "encounter" or "visit" in name visible | Product tracks visits/appointments; cannot verify coverage |
| Problems / conditions / diagnoses | ❓ Unknown | May be embedded in clinical note modules; no detail | Product stores diagnoses; cannot verify |
| Medications / prescriptions | ❓ Unknown | No medication-related module name visible in the 8 identified | Product has e-prescribing and methadone dosing; cannot verify |
| Allergies | ❓ Unknown | No allergy module visible | Product likely stores allergies; cannot verify |
| Immunizations | ❓ Unknown | No immunization module visible | Behavioral health EHR — may or may not store; cannot verify |
| Vitals | ❓ Unknown | No vitals module visible | Product likely captures some vitals; cannot verify |
| Lab results | ❓ Unknown | No lab module visible; "Urine Screen Code Management" in settings suggests lab data exists | Product integrates with LabCorp/Quest; cannot verify |
| Imaging / diagnostic reports | N/A | No evidence product stores imaging | Not a core behavioral health function |
| Procedures | ❓ Unknown | No procedure module visible | May be relevant for some settings; cannot verify |
| Clinical notes / documents | ⚠️ Partial evidence | 5 of 8 visible modules are clinical note types (Psychiatric Progress Note, Mental Health Assessment, CPST Note, Counseling Monthly Individual Progress Report, Comprehensive Psychosocial Evaluation) | Product's core function; at least some clinical notes are in the export, but 164 modules are unidentified |
| Care plans / goals | ❓ Unknown | No care plan module visible | Product stores treatment plans; cannot verify |
| Orders / referrals | ❓ Unknown | "Referrals/Payers" appears in settings menu but not in visible export modules | Product has referral management; cannot verify |
| Insurance / coverage | ❓ Unknown | No insurance module visible | Product does eligibility verification; cannot verify |
| Claims / billing | ❓ Unknown | No billing module visible; "Billing" tab exists in navigation | Product does billing/claims/EDI 837; cannot verify |
| Payments | ❓ Unknown | No payment module visible; "Client Invoicing/Payment" tab in navigation | Product processes payments; cannot verify |
| Consents / directives | ❓ Unknown | No consent module visible | Behavioral health likely requires extensive consents; cannot verify |
| Patient communications / portal messages | ❓ Unknown | No communication module visible | Product has secure messaging, SMS, portal; cannot verify |
| Specialty: Behavioral health assessments | ⚠️ Partial evidence | Mental Health Assessment, Comprehensive Psychosocial Evaluation, CPST Note visible | Core specialty data; some evidence of coverage but scope unknown |
| Specialty: Addiction/MAT treatment | ❓ Unknown | No methadone/MAT module visible | Product has native methadone dosing; cannot verify |
| Specialty: Bed management | ❓ Unknown | "Bed Management Settings" visible in settings menu but no export module | Product has bed management module; cannot verify |

**Coverage summary**: Of 21 applicable domains, **0 can be confirmed as covered**, 2 have partial evidence (clinical notes and behavioral health assessments from the 8 visible module names), and 19 are completely unknown. This is not because the export necessarily lacks them — the 172-module architecture could cover all domains — but because the documentation provides no way to verify.

## 6. Documentation Quality

The documentation is fundamentally inadequate for its stated purpose:

- **Can a developer understand and use the export?** No. A developer receiving this documentation would know how to click buttons to generate an export but would have no idea what file format to expect, how to parse it, what fields it contains, or how to map the data to any standard.
- **What's well-documented?** The UI navigation steps (how to access the export, how to filter by date/client/module, how to download) are adequately illustrated with screenshots. Role-based access configuration is shown.
- **What requires guesswork?** Everything about the export's content: file format, data structure, field names and types, value sets, relationships between modules, what each module contains, and what the 164 unnamed modules are.
- **Machine-readable artifacts?** None. No schemas, no sample data files, no structured documentation of any kind. The only artifact is a PDF with screenshots.
- **Could someone build an import?** No. Without knowing the file format, schema, or field definitions, it is impossible to programmatically process the exported data.

## 7. Overall Assessment

### Classification

**Minimal/stub**: The documentation is too thin to assess what is actually exported. While the product appears to have built a module-based export mechanism with 172 modules (which is architecturally promising), the documentation provides zero detail about the export format, content, or structure. The PDF is a 5-page UI walkthrough with screenshots — not a technical specification. No data dictionary, no schema, no sample data, no format specification.

### Key Findings

1. **172 modules exist but are undocumented.** The export's module picker shows 172 selectable modules, but only 8 module names are visible across the entire documentation. No module listing, no category mapping, no field definitions for any module. (Source: `EHIexportDocumentation.pdf`, page 4 screenshot)

2. **Export format is completely unknown.** The documentation never states whether the export produces CSV, JSON, PDF, XML, or any other format. A recipient would receive a file of unknown format containing data of unknown structure. (Source: full text extraction of `EHIexportDocumentation.pdf` — no format mention anywhere)

3. **Zero fields are documented.** There is no data dictionary, no schema, no field names, no types, no descriptions, no value sets. The total field-level documentation is 0. (Source: `analysis/full-entity-inventory.json`)

4. **The architecture is promising but unverifiable.** A module-based export with 172 modules across a behavioral health EHR with 16+ functional areas could genuinely cover "all EHI." But without a module listing or any content documentation, this cannot be assessed. The 8 visible module names suggest at least clinical notes are covered, but billing, medications, labs, scheduling, bed management, and all other domains are unverifiable.

5. **Configurable exclusions create compliance risk.** The "EHI Export Business Rules" allow administrators to exclude modules from the export. The screenshot shows module 836 ("Client Notes To File") unchecked. If administrators exclude modules containing EHI, the export may not meet (b)(10) requirements. No guidance is provided about which modules must remain included for compliance.

### Summary Stats

```
Classification:  Minimal/stub
Export format:   Unknown (not documented)
Model type:      Module-based (internal system modules), but structure undocumented
Entities:        172 modules claimed, 8 named, 164 unknown
Fields:          0 documented
Descriptions:    N/A (0 fields documented)
Sample data:     No
Bulk export:     Yes (per disclosures page RWT objectives)
Domains covered: 0 of 19 confirmed; 2 of 19 with partial evidence
```

### Bottom Line

Zoobook EHR's EHI export documentation is a 5-page screenshot walkthrough that tells users how to click buttons but provides zero information about what data is exported or in what format. The underlying export mechanism — 172 selectable modules — is architecturally promising for a behavioral health EHR, but the documentation makes it impossible for a recipient to understand, parse, or use the exported data. The single biggest gap is the complete absence of a data dictionary, schema, or format specification.
