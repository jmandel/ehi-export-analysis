# EHI Export Analysis: Procentive (Ensora Health)

**Product**: Procentive  
**Analysis date**: 2026-02-16  
**CHPL ID**: 15.04.04.2214.Proc.02.01.1.221228

## 1. Product Context

Procentive is a cloud-based EHR and practice management platform purpose-built for behavioral health, mental health, and substance use recovery providers. It is now part of the Ensora Health portfolio (formerly Therapy Brands, acquired by KKR for $1.2B in 2021). The product targets mid-size to larger behavioral health organizations including outpatient clinics, residential/inpatient facilities, and substance abuse treatment centers.

Procentive is a **full-spectrum** behavioral health platform, not just clinical charting. It stores and manages:

- **Clinical data**: Assessments, treatment plans, progress notes, discharge summaries, group therapy notes, DSM-5 diagnoses
- **E-prescribing**: Prescriptions including EPCS (controlled substances) via DrFirst integration
- **Billing & RCM**: Insurance claims, charges, payments, denials, appeals, clearinghouse services
- **Bed management**: Client stays, bed status, capacity, waitlists (residential facilities)
- **Client portal**: Secure messaging, appointment requests, bill payments
- **Scheduling**: Appointments, telehealth sessions, automated reminders
- **Insurance**: Eligibility verification, authorization management
- **Reporting**: 120+ report templates, census tracking, clinical/financial analytics

This breadth of functionality means a genuine (b)(10) export should cover clinical documentation, medications, billing/claims, bed management, portal communications, insurance details, and scheduling — not just USCDI clinical summaries.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `PDF-for-Website-on-Formats-1.pdf` (112 KB, 1 page) | The sole (b)(10) documentation artifact. Lists XML, CSV, and PDF as export formats with generic dictionary definitions of each format. No data dictionary, no field definitions, no schema. | **Least informative** — contains zero product-specific content |
| `onc-procentive-page.html` (83 KB) | ONC certification landing page. Contains a brief EHI export section (~12 lines) mentioning single-patient and population export, links to the PDF above, and FHIR endpoints. | Low — confirms export exists but gives no detail on content |
| `fhir-api-documentation.html` (686 KB) | Complete FHIR API documentation from Dynamic Health IT's ConnectEHR platform. Documents USCDI-to-FHIR resource mapping. Explicitly states: "Available data via the API interface is limited by the data defined by the USCDI." | Informative for understanding the (g)(10) scope, which confirms it's USCDI-only |
| `fhir-capability-statement.json` (19 KB) | FHIR R4 CapabilityStatement listing 22 resource types with read and search-type interactions, plus bulk export operations. | Confirms FHIR scope is standard USCDI |
| `smart-configuration.json` (3 KB) | SMART on FHIR config with scopes for 26 resource types. | Minor — confirms standard FHIR setup |
| `fhir-endpoints.json` (2 KB) | Single FHIR endpoint. | Minimal |
| `fhir-home-page.html` (15 KB) | Dynamic FHIR Server home page. | Minimal |
| Screenshots (4 files, ~1.4 MB total) | Visual captures of the ONC page, FHIR docs, and PDF. | Corroborative only |

## 3. Export Mechanics

**Format(s)**: The vendor states the export uses XML, CSV, and/or PDF formats, "depending on set-up and use of the system by the agency." No further detail on which data goes in which format.

**Mechanism**:
- **Single-patient**: User can export "without developer assistance" — implies a UI-accessible function, but no screenshots or workflow documentation is provided.
- **Population/bulk**: "can be requested by submitting a support ticket via Salesforce" — vendor-assisted, not self-service.

**Access constraints**: Population export requires a support ticket. The ONC page notes that content "might vary based on a variety of factors" including software version, configuration, and documentation practices — a significant disclaimer that effectively says the export content is undefined.

**Fees**: The attestation disclosure mentions "one-time costs to establish interfaces" and "on-going annual fees" for certain services. It's unclear if this applies to (b)(10) exports.

## 4. Export Content: What's In It

### The core problem: No data dictionary exists

Procentive provides **zero field-level documentation** for its EHI export. The entire (b)(10) documentation consists of:

1. **A 12-line section on the ONC page** saying exports exist in XML/CSV/PDF
2. **A 1-page PDF** providing Wikipedia-level definitions of XML, CSV, and PDF as file formats

There is no:
- Data dictionary
- Schema definition
- Entity/table listing
- Field names, types, or descriptions
- Sample data files
- Mapping documentation
- Relationship/foreign key documentation
- Value set or code system specifications

### What the FHIR API covers (for reference)

The FHIR API documentation (which is (g)(10), not (b)(10)) explicitly limits itself to USCDI data. The CapabilityStatement exposes 22 resource types — all standard US Core:

| FHIR Resource | Category | Notes |
|---|---|---|
| Patient | Demographics | Standard US Core |
| AllergyIntolerance | Allergies | Standard US Core |
| CarePlan | Care Plans | Standard US Core |
| CareTeam | Care Team | Standard US Core |
| Condition | Problems | Standard US Core |
| Device | Devices | Standard US Core |
| DiagnosticReport | Diagnostics | Standard US Core |
| DocumentReference | Documents | Standard US Core |
| Encounter | Encounters | Standard US Core |
| Goal | Goals | Standard US Core |
| Immunization | Immunizations | Standard US Core |
| MedicationRequest | Medications | Standard US Core |
| Observation | Clinical Observations | Standard US Core |
| Procedure | Procedures | Standard US Core |
| Provenance | Provenance | Standard US Core |
| Location | Facility | Standard US Core |
| Organization | Organization | Standard US Core |
| Practitioner | Provider | Standard US Core |
| PractitionerRole | Provider | Standard US Core |
| ClinicalImpression | Clinical | Non-standard addition |
| Binary | Documents | Binary access |
| Group | Administrative | Bulk export operation |

The FHIR API covers USCDI only and explicitly says so. It does not cover billing, bed management, scheduling, portal messages, insurance authorization, or any behavioral health–specific data structures.

### Vendor's own content organization

The vendor provides no content organization because there is no data dictionary. The only structured information is the list of export formats (XML, CSV, PDF) with no indication of what entities or fields appear in each.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

**It is impossible to assess coverage from the provided documentation.** The vendor's (b)(10) documentation consists entirely of:
- A statement that exports exist
- A list of three generic file formats (XML, CSV, PDF) with textbook definitions
- A disclaimer that content "might vary" based on configuration

There is no entity listing, no field listing, no category breakdown, and no sample data. The vendor has not documented *what* is exported, only *that* something can be exported in one of three formats.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ❓ Unknown | No data dictionary. FHIR API has Patient resource (USCDI only). | Product stores demographics; cannot confirm export coverage |
| Encounters / visits | ❓ Unknown | No data dictionary. FHIR API has Encounter (USCDI only). | Product tracks appointments/encounters; cannot confirm |
| Problems / conditions | ❓ Unknown | No data dictionary. FHIR API has Condition. | Product stores DSM-5 diagnoses; cannot confirm depth |
| Medications / prescriptions | ❓ Unknown | No data dictionary. FHIR API has MedicationRequest. | Product has EPCS; cannot confirm prescription detail level |
| Allergies | ❓ Unknown | No data dictionary. FHIR API has AllergyIntolerance. | Cannot confirm |
| Immunizations | ❓ Unknown | No data dictionary. FHIR API has Immunization. | Cannot confirm |
| Vitals | ❓ Unknown | No data dictionary. FHIR API has Observation. | Behavioral health product; vitals less central but still relevant |
| Lab results | ❓ Unknown | No data dictionary. | Labs less central for behavioral health; likely N/A or minimal |
| Procedures | ❓ Unknown | No data dictionary. FHIR API has Procedure. | Cannot confirm |
| Clinical notes / documents | ❓ Unknown | No data dictionary. FHIR API has DocumentReference. | Product stores assessments, treatment plans, progress notes, group notes; cannot confirm export completeness |
| Care plans / goals | ❓ Unknown | No data dictionary. FHIR API has CarePlan, Goal. | Product has "Practice Planners" for treatment plans; cannot confirm |
| Insurance / coverage | ❓ Unknown | No evidence in any documentation. | Product stores insurance details, eligibility, authorizations; **likely gap** |
| Claims / billing | ❓ Unknown | No evidence in any documentation. | Product has full RCM (claims, charges, payments, denials); **likely gap** |
| Payments | ❓ Unknown | No evidence in any documentation. | Product processes payments; **likely gap** |
| Orders / referrals | ❓ Unknown | No data dictionary. | Cannot assess |
| Patient communications | ❓ Unknown | No evidence in any documentation. | Product has client portal with secure messaging; **likely gap** |
| Bed management | ❓ Unknown | No evidence in any documentation. | Product has dedicated bed management module; **likely gap** |
| Specialty-specific (behavioral health) | ❓ Unknown | No evidence in any documentation. | Product stores BH-specific data (DSM-5, treatment plans, group therapy, substance use workflows); **likely gap** |
| Consents / directives | ❓ Unknown | No evidence. | Cannot assess |

**Summary**: Every domain is marked "Unknown" because the vendor provides no documentation of what the export actually contains. Domains with no FHIR API representation (billing, insurance, payments, bed management, portal communications, behavioral health–specific data) are the most likely gaps — these are exactly the domains where a purpose-built (b)(10) export would need to go beyond the USCDI FHIR API.

## 6. Documentation Quality

The EHI export documentation quality is **critically deficient**:

- **No data dictionary**: Zero entities, tables, or fields are documented.
- **No schema**: No machine-readable schema of any kind.
- **No sample data**: No example exports or sample files.
- **No field definitions**: Not a single field name, type, or description is provided.
- **No mapping**: No documentation of how internal data maps to export formats.
- **No relationships**: No foreign key or entity relationship documentation.
- **No value sets**: No code systems or enumerated values documented.
- **Generic format descriptions only**: The PDF defines what XML, CSV, and PDF *are as file formats* — not what Procentive data they contain.
- **Undetermined content**: The ONC page explicitly disclaims that export content "might vary" based on configuration, version, and practices.

A developer could not build an import, understand the data model, or even determine what data domains are included without actually obtaining an export and reverse-engineering it. This documentation is among the thinnest possible while still technically claiming to describe an export.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Minimal/stub/unclear**

The documentation is too thin to assess coverage. There is literally no listing of what data the export contains — no entities, no fields, no categories. The only structured information available is the FHIR API CapabilityStatement, which explicitly limits itself to USCDI. The vendor's (b)(10) documentation (one ONC page section + one PDF page) provides zero product-specific content about what is exported. The PDF's content could apply to any software product — it contains generic definitions of XML, CSV, and PDF copied from standard references.

For a product with substantial billing/RCM, bed management, client portal, e-prescribing, and behavioral health–specific capabilities, the complete absence of documentation about whether any of these domains are exported is a critical gap.

**Axis 2 — Export approach: Unclear/undetermined**

The vendor mentions XML, CSV, and PDF as export formats, which suggests *something* beyond the FHIR API may exist — but without any documentation of content, it's impossible to determine whether this is a purpose-built export or a minimal data dump. The FHIR API is clearly (g)(10) and USCDI-only (the documentation explicitly says so). Whether the XML/CSV/PDF exports contain additional data beyond USCDI is completely undocumented.

The population export requiring a Salesforce support ticket further suggests this may not be a fully productized, self-service export.

### Key Findings

1. **No data dictionary whatsoever**: Procentive's entire (b)(10) documentation is a 1-page PDF containing generic definitions of XML, CSV, and PDF as file formats, plus a ~12-line section on the ONC page. There is zero product-specific content about what data is exported. (`PDF-for-Website-on-Formats-1.pdf`, `onc-procentive-page.html`)

2. **FHIR API is explicitly USCDI-only**: The FHIR API documentation states "Available data via the API interface is limited by the data defined by the USCDI," covering 22 standard resource types with no vendor extensions. (`fhir-api-documentation.html`)

3. **Significant product capabilities undocumented in export**: Procentive stores billing/RCM data, bed management records, client portal messages, insurance authorizations, and behavioral health–specific clinical data. None of these domains appear in any export documentation. (`product-research.md`)

4. **Population export is vendor-assisted**: Bulk export for patient populations requires submitting a support ticket via Salesforce, not a self-service UI function. (`onc-procentive-page.html`)

5. **Content explicitly disclaimed as variable**: The ONC page states export content "might vary" based on configuration, software version, and documentation practices — effectively saying the export content is undefined. (`onc-procentive-page.html`)

### Summary Stats

```
Coverage:        Minimal/stub/unclear
Approach:        Unclear/undetermined
Export format:   XML, CSV, PDF (per documentation; no detail on content)
Entities:        N/A (no data dictionary)
Fields:          N/A
Descriptions:    N/A
Sample data:     No
Bulk export:     Vendor-assisted (support ticket required)
Domains covered: 0 of 15+ applicable domains confirmed (documentation insufficient)
```

### Bottom Line

Procentive provides effectively no (b)(10) export documentation. A patient or provider requesting their data would have no way to know what they'd receive — the vendor hasn't documented what the export contains, and the only structured documentation (FHIR API) is explicitly limited to USCDI clinical data. For a product with full billing/RCM, bed management, client portal, and behavioral health–specific capabilities, the absence of any data dictionary or content specification represents one of the weakest (b)(10) implementations reviewed.
