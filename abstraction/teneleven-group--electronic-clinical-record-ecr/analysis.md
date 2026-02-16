# EHI Export Analysis: TenEleven Group (Ensora Health)

**Product**: electronic Clinical Record (eCR™) v2.4  
**Analysis date**: 2026-02-16  
**CHPL ID**: 15.04.04.2861.Elec.24.01.1.221231

## 1. Product Context

electronic Clinical Record (eCR) is a comprehensive behavioral health EHR and practice management system developed by TenEleven Group (now part of Ensora Health, a KKR-backed portfolio company). It targets behavioral health and human services agencies — mental health clinics, substance use treatment centers, and residential/inpatient facilities — serving multi-disciplinary care teams at agencies with 10+ users.

The product covers a broad range of data domains relevant to EHI export assessment:

- **Clinical documentation**: Treatment plans, progress notes, clinical assessments, goals/objectives, DSM-5 diagnoses, customizable clinical templates (FormLab)
- **Medication-Assisted Treatment (MAT)**: Dosing schedules, dispensing records, tapering plans, patient verification — a major product differentiator
- **Medication Administration Records (MAR)**: For inpatient/residential settings
- **E-prescribing and e-labs**: Prescription and lab order workflows
- **Billing and revenue cycle management**: Claims submission (primary/secondary), ERA/EOB processing, payment tracking, credit card processing, patient statements, billing triggers linked to clinical documentation
- **Bed management**: Bed assignment, occupancy, resident status for residential/inpatient facilities
- **Scheduling**: Client appointments, calendar management
- **Patient portal**: Patient access to records
- **Intake and referral management**: Referral intake through admission
- **Compliance and reporting**: Outcomes dashboards, regulatory reporting, public health submissions

This is a full EHR + practice management system. A genuine (b)(10) export should cover clinical data, billing/financial data, MAT-specific data, bed management, custom forms, intake/referral, and scheduling data.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/PDF-for-Website-on-Formats-2.pdf` | 1-page PDF (116 KB) describing two export formats: JSON for single patient, .bak for population. Created 2023-11-30 by Catherine Baker in Microsoft Word. Contains 13 lines of text, no tables, no field definitions, no schema. | **Primary artifact** — but extremely thin |
| `downloads/screenshot-ehi-export-section.png` | Screenshot of the EHI Export section on ensorahealth.com/onc/teneleven/ showing two export types, variability disclaimer, and File Formats button | Confirms web page content |
| `downloads/screenshot-onc-page-top.png` | Screenshot of top of ONC certification disclosure page showing developer/product details | Confirms certification details |
| `downloads/screenshot-fhir-api-docs.png` | Screenshot of FHIR API documentation at fhir.10e11.com | Confirms (g)(10) API exists separately from (b)(10) |
| `ensorahealth.com/onc/teneleven/` (live page, verified 2026-02-16) | ONC disclosure page with EHI Export section — two paragraphs describing single patient and population export | Confirms page is still live and unchanged |

**No data dictionary, schema documentation, sample data, or machine-readable export specification exists among the artifacts.** The entire (b)(10) documentation consists of two paragraphs on a web page and a 1-page PDF with two bullet points.

## 3. Export Mechanics

**Two export modes are described:**

1. **Single Patient Export**
   - **Format**: JSON
   - **Mechanism**: User-initiated ("without developer assistance")
   - **Content**: "USCDI v1 data as well as other applicable data"
   - **No further detail** on what "other applicable data" includes, what the JSON schema looks like, or how to initiate the export

2. **Patient Population Export**
   - **Format**: .bak file (SQL Server database backup)
   - **Mechanism**: Vendor-assisted — requires submitting a support ticket via Salesforce
   - **Content**: "a full SQL Server database backup of all data for an agency that can be restored"
   - **Requires Microsoft SQL Server** to restore
   - **No schema documentation** for the database

The web page includes a variability disclaimer noting export content may vary based on software version, configuration, documentation practices, and other factors.

**Access constraints**: The population export requires a vendor support ticket (not self-service). No fees are mentioned for either export.

## 4. Export Content: What's In It

### What the documentation actually tells us

The documentation provides **zero** structured information about export content:

- **Entities/tables defined**: 0
- **Fields defined**: 0
- **Fields with descriptions**: 0
- **Fields with types**: 0
- **Sample data**: None
- **Schema documentation**: None
- **Value sets**: None
- **Relationships/foreign keys**: None

The single patient JSON export is described only as containing "USCDI v1 data as well as other applicable data." There is no JSON schema, no sample output, no field listing, and no documentation of what "other applicable data" means.

The population .bak export is described as "a full SQL Server database backup of all data for an agency." This implies completeness — a database backup would contain every table and every field in the system — but there is no schema documentation to verify what the database contains or help a recipient interpret it.

### Vendor's own content organization

The vendor provides no content organization. There are no categories, no entity listings, and no field definitions. The only content distinction is between the two export formats:

| Export Type | Format | Described Content | Schema Documented | Fields Listed |
|---|---|---|---|---|
| Single Patient | JSON | "USCDI v1 data as well as other applicable data" | No | 0 |
| Patient Population | .bak (SQL Server backup) | "Full SQL Server database backup of all data" | No | 0 |

### FHIR API (g)(10) — separate from (b)(10)

The FHIR API at fhir.10e11.com is clearly labeled as (g)(10) and explicitly states it is "limited by the data defined by the USCDI." Its CapabilityStatement shows 22 resource types (AllergyIntolerance, CarePlan, CareTeam, ClinicalImpression, Condition, Device, DiagnosticReport, DocumentReference, Encounter, Goal, Group, Immunization, Location, MedicationRequest, Observation, Organization, Patient, Practitioner, PractitionerRole, Procedure, Provenance, Binary), all profiled to US Core. This is the standard USCDI clinical exchange surface and is presented separately from the EHI export section on the disclosure page.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor's documentation is too thin to assess bottom-up coverage in any meaningful way.

**Single patient export**: Claims "USCDI v1 + other applicable data" but does not specify what "other applicable data" includes. At minimum, it covers USCDI v1 (demographics, problems, medications, allergies, immunizations, vitals, labs, procedures, encounters, clinical notes, care plans, goals, care teams, devices, provenance). Whether it goes beyond that is undocumented.

**Population export**: A SQL Server database backup would theoretically contain everything in the system — clinical, billing, scheduling, MAT, bed management, custom forms, and all other data. However, with zero schema documentation, this is an assertion that cannot be verified from the documentation alone.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | Single patient: implied via USCDI v1. Population: assumed in DB backup. No field-level detail. | Product stores extensive demographic data; export likely includes it but documentation provides no verification |
| Encounters / visits | ⚠️ Partial | Single patient: implied via USCDI v1. Population: assumed in DB backup. | Same — no detail |
| Problems / conditions / diagnoses | ⚠️ Partial | Single patient: implied via USCDI v1. Population: assumed in DB backup. | Product uses DSM-5 extensively; no documentation of how DSM-5 diagnoses map to export |
| Medications / prescriptions | ⚠️ Partial | Single patient: implied via USCDI v1. Population: assumed in DB backup. | Product has e-prescribing, MAR, and MAT dosing — USCDI covers only basic medication lists |
| Allergies | ⚠️ Partial | Single patient: implied via USCDI v1 | Likely covered at USCDI level |
| Immunizations | ⚠️ Partial | Single patient: implied via USCDI v1 | Likely covered at USCDI level |
| Vitals | ⚠️ Partial | Single patient: implied via USCDI v1 | Likely covered at USCDI level |
| Lab results | ⚠️ Partial | Single patient: implied via USCDI v1. Product has e-labs. | No detail on whether full lab orders/results or just USCDI subset |
| Procedures | ⚠️ Partial | Single patient: implied via USCDI v1 | Likely covered at USCDI level |
| Clinical notes / documents | ⚠️ Partial | Single patient: implied via USCDI v1 | Product has extensive FormLab custom templates; unclear if custom form data is in single-patient export |
| Care plans / goals | ⚠️ Partial | Single patient: implied via USCDI v1 | Product has treatment planning with Goal/Objective Library |
| Orders / referrals | ❌ Not covered | No documentation of orders/referrals in export | Product has intake/referral management; not documented in export |
| Insurance / coverage | ❌ Not covered | No documentation | Product manages insurance for billing; not mentioned in export docs |
| Claims / billing | ❌ Not covered | No documentation of billing data in single-patient export | Product has full RCM (claims, ERA/EOB, payments, statements) — **significant gap** in documentation |
| Payments | ❌ Not covered | No documentation | Product processes payments and credit cards |
| Specialty-specific: MAT | ❌ Not covered | No documentation of MAT-specific data (dosing, tapering, dispensing) in export | MAT is a major product differentiator — **significant gap** in documentation |
| Specialty-specific: Bed management | ❌ Not covered | No documentation | Product has bed management for residential settings |
| Consents / directives | ❌ Not covered | No documentation | Likely captured via FormLab forms |
| Patient communications | ❌ Not covered | No documentation | Product has a patient portal |

**Note on the .bak population export**: A SQL Server database backup would, by definition, contain all of the above domains. The coverage ratings above reflect what is *documented and verifiable* from the export documentation, not what the .bak file likely contains. The .bak approach is potentially comprehensive, but with zero schema documentation, a recipient cannot confirm what's in it or interpret the data without reverse-engineering the database.

## 6. Documentation Quality

**Documentation quality is extremely poor — among the worst possible for a certified product.**

- **Can a developer understand the export?** No. There is no schema, no field listing, no sample data, and no instructions for interpreting either export format.
- **Single patient JSON**: No JSON schema or sample output. A developer would have to request an export and reverse-engineer the JSON structure.
- **Population .bak**: A developer would need Microsoft SQL Server to restore the backup, then explore the database tables with no guidance on table names, relationships, or data types.
- **Machine-readable artifacts**: None. No schema files, no sample data, no API documentation specific to the (b)(10) export.
- **What's well-documented**: Nothing related to (b)(10). The FHIR (g)(10) API documentation at fhir.10e11.com is substantially more detailed, but that documents a different capability.

The documentation consists of exactly two artifacts:
1. Two paragraphs on a web page (verified live 2026-02-16)
2. A 1-page PDF with two bullet points (13 lines of text total, created 2023-11-30)

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Minimal/stub/unclear**

The documentation is too thin to assess coverage. The single patient JSON export claims "USCDI v1 + other applicable data" but provides no detail on what "other applicable data" means — it could be a handful of extra fields or a comprehensive export of all EHR data. The population .bak export is described as a "full database backup," which would be comprehensive by definition, but the complete absence of schema documentation makes it impossible to verify this claim or use the export effectively.

The phrase "other applicable data" is doing heavy lifting here. Without any specification of what it includes, the documented single-patient export reads as essentially USCDI v1 — the regulatory floor for clinical exchange — with a vague gesture toward additional content. For a product with deep behavioral health specialization (MAT, FormLab custom forms, bed management, billing), the documentation provides zero evidence that specialty-specific data is included in the single-patient export.

**Axis 2 — Export approach: Unclear/undetermined**

The vendor appears to understand the distinction between (g)(10) and (b)(10) — the FHIR API is presented separately from the EHI export section, and the .bak approach for population export is deliberately broader than the FHIR API. The .bak strategy (full database backup) suggests a purpose-built approach to population export that goes beyond clinical exchange. However, the single patient JSON export's description ("USCDI v1 data as well as other applicable data") sounds closer to a repackaged clinical export with unspecified additions. Without documentation of the JSON structure or the database schema, it's impossible to determine whether either export represents genuine purpose-built (b)(10) work or minimal compliance.

### Key Findings

1. **Documentation is near-empty**: The entire (b)(10) export documentation is 13 lines of text across a 1-page PDF and two web page paragraphs. Zero entities, zero fields, zero schema elements are documented. (`PDF-for-Website-on-Formats-2.pdf`, `ensorahealth.com/onc/teneleven/`)

2. **Population export (.bak) is potentially comprehensive but practically useless without documentation**: A SQL Server database backup is the most complete possible export format — it contains everything. But without a data dictionary, table documentation, or even a list of table names, a recipient would need to reverse-engineer the entire database. It also requires Microsoft SQL Server to restore.

3. **Single patient export scope is ambiguous**: The phrase "USCDI v1 data as well as other applicable data" is the only description. The "other applicable data" is completely unspecified — it could mean MAT dosing records and billing data, or it could mean nothing beyond USCDI. (`PDF-for-Website-on-Formats-2.pdf`)

4. **No behavioral health specialty data is documented**: For a product whose primary differentiator is MAT, FormLab custom forms, and residential bed management, none of this specialty-specific data is mentioned anywhere in the export documentation.

5. **Population export is not self-service**: Requires submitting a support ticket via Salesforce, adding a process barrier to what should be a patient/provider right under the Cures Act. (`ensorahealth.com/onc/teneleven/`)

### Summary Stats

```
Coverage:        Minimal/stub/unclear
Approach:        Unclear/undetermined
Export format:   JSON (single patient), .bak SQL Server backup (population)
Entities:        N/A (no data dictionary)
Fields:          N/A
Descriptions:    N/A
Sample data:     No
Bulk export:     Yes (population .bak via support ticket)
Domains covered: 0 of 19 verifiable (documentation too thin to confirm any domain)
```

### Bottom Line

TenEleven's EHI export documentation is a stub — 13 lines of text describing two file formats with no data dictionary, no schema, no sample data, and no field-level detail. The population export (.bak database backup) could be genuinely comprehensive, but without any schema documentation, it is practically unusable. A patient or provider receiving this export would have no way to interpret or use the data without reverse-engineering a SQL Server database or a proprietary JSON format.
