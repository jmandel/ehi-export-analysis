# EHI Export Analysis: Medi-EHR, LLC

**Product**: Medi-EHR v2.1  
**Analysis date**: 2026-02-16  
**CHPL IDs**: 15.02.05.2979.MEDI.01.01.1.220215 (CHPL ID 10831)

## 1. Product Context

Medi-EHR is a cloud-based (SaaS) EHR platform built on Oracle 11g, serving small to medium ambulatory practices across multiple specialties. It is a full-featured system with 37 certified ONC criteria including (b)(10).

**Key capabilities relevant to EHI scope:**
- **Clinical EHR**: Charting, problem lists, medications, vitals, immunizations, lab results, radiology, clinical notes, custom templates, document management
- **Billing/Practice Management**: Integrated billing module ($250/provider/month standalone), superbill creation, revenue cycle management, clearinghouse integrations (Optum, Waystar, Change Healthcare), insurance benefits verification
- **E-Prescribing**: Surescripts integration including EPCS
- **Patient Portal**: Secure messaging, prescription refills, bill payment, digital check-in
- **Scheduling**: Appointments, self-scheduling, reminders
- **Specialty modules**: Ambulatory Surgery Centers ($750/OR/month), Behavioral Health ($65/user/month), Residential Treatment Facilities ($150/bed)
- **Workers' Compensation / No-Fault**: Specialized claims processing module
- **Telemedicine**: Built-in video conferencing
- **Communications**: SMS, fax, email, secure messaging

This is a broadly capable ambulatory EHR with integrated billing and multiple specialty modules. A genuine (b)(10) export should cover clinical data, billing/claims, specialty-specific records, and patient communications.

## 2. Artifacts Reviewed

| Artifact | Size | Description | Informational Value |
|---|---|---|---|
| `downloads/compliance-page.html` | 196 KB | Main compliance page; Section I covers EHI export | **Low** — 3 paragraphs with generic format descriptions, no data dictionary |
| `downloads/compliance-page.png` | 1.2 MB | Full-page screenshot of compliance page | **Low** — confirms HTML rendering matches text extraction |
| `downloads/API_Document.html` | 359 KB | Swagger UI page for MediEHR Patient Access API v2.1 | **Medium** — documents 4 API endpoints including C-CDA export with 19 sections |
| `downloads/developer-portal-api-docs.png` | 177 KB | Screenshot of Oracle APEX developer portal | **Low** — shows iframe embedding of API docs |
| `downloads/fhir-service-base-bundle.json` | 1.2 KB | FHIR Bundle with sandbox endpoint and Organization | **Low** — confirms (g)(10) FHIR is via InteropEngine, separate from (b)(10) |
| `downloads/public-fhir-api-page.html` | 197 KB | Public FHIR API page | **Low** — (g)(10) documentation, not (b)(10) |
| `downloads/enrichment/api-docs.json` | 14 KB | Structured extraction of API endpoints/parameters | **Medium** — machine-readable inventory of API; verified against source HTML |

The most informative artifact is `API_Document.html` (and its parsed form `api-docs.json`), which documents the C-CDA export API. The compliance page itself contributes almost no technical detail.

## 3. Export Mechanics

**Format(s):**
- **C-CDA 2.1 XML**: Documented via a proprietary REST API (`mediehrgetpatientdata.php`). 19 toggleable clinical sections.
- **CSV**: Mentioned on the compliance page but entirely undocumented — no field lists, no schema, no instructions.
- **HTML**: Mentioned on the compliance page but entirely undocumented — no structure, no field details.

**Mechanism:**
- **API-based**: The documented export uses a proprietary REST API (base URL: `https://proda.mediemr.net/patient/v1`) with custom token-based authentication (not OAuth 2.0 or SMART on FHIR). Requires registration on an Oracle APEX developer portal and facility approval.
- **UI-based (claimed)**: The compliance page states "Medi-EHR allows a user to export electronic health information (EHI) for a single patient at any time without developer assistance." This implies a UI export, but no documentation of how to perform it is provided.

**Single-patient vs bulk:**
- API supports single-patient export only (requires `PATIENT_MRN` parameter).
- Compliance page claims multi-patient export capability ("export all the data for a patient population") but no mechanism is documented.

**Access constraints:**
- API requires registration, facility approval, and token management.
- No documentation of fees for export; a separate "Custom Export" page advertises paid data extraction services, which is distinct from (b)(10).

## 4. Export Content: What's In It

### No data dictionary exists

There is **no data dictionary** at any level of granularity. The vendor provides:
- **Section names**: 19 C-CDA sections that can be toggled on/off
- **Zero field-level detail**: No field names, types, descriptions, cardinalities, value sets, code systems, or template identifiers
- **Zero sample data**: No example C-CDA documents, CSV files, or HTML exports
- **Zero schemas**: No XSD, JSON Schema, or C-CDA template OIDs

### Vendor's own content organization

The vendor does not organize content into categories — they simply list 19 C-CDA section toggles. The compliance page adds CSV and HTML as formats but with no content detail.

| Entity/Section | Fields | Described | Types | Category |
|---|---|---|---|---|
| Allergies | 0 (unknown) | N/A | N/A | C-CDA Section |
| Medications | 0 (unknown) | N/A | N/A | C-CDA Section |
| Problems | 0 (unknown) | N/A | N/A | C-CDA Section |
| Encounters | 0 (unknown) | N/A | N/A | C-CDA Section |
| Immunizations | 0 (unknown) | N/A | N/A | C-CDA Section |
| Vitals | 0 (unknown) | N/A | N/A | C-CDA Section |
| Social History | 0 (unknown) | N/A | N/A | C-CDA Section |
| Procedures | 0 (unknown) | N/A | N/A | C-CDA Section |
| Labs | 0 (unknown) | N/A | N/A | C-CDA Section |
| Implantable Devices | 0 (unknown) | N/A | N/A | C-CDA Section |
| Goals | 0 (unknown) | N/A | N/A | C-CDA Section |
| Functional Status | 0 (unknown) | N/A | N/A | C-CDA Section |
| Cognitive Status | 0 (unknown) | N/A | N/A | C-CDA Section |
| Referrals | 0 (unknown) | N/A | N/A | C-CDA Section |
| Assessment | 0 (unknown) | N/A | N/A | C-CDA Section |
| Care Team | 0 (unknown) | N/A | N/A | C-CDA Section |
| Health Concerns | 0 (unknown) | N/A | N/A | C-CDA Section |
| Plan of Treatment | 0 (unknown) | N/A | N/A | C-CDA Section |
| Diagnostic and Imaging Reports | 0 (unknown) | N/A | N/A | C-CDA Section |

**Field count: 0 documented fields.** Only 19 section-level labels exist with no sub-field detail. The API documents 11 input parameters for patient search (name, SSN, DOB, email, mobile, mother's maiden name) but these describe how to query patients, not what the export contains.

The complete parsed inventory is in `analysis/entity-inventory-full.json`.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor documents exactly one export mechanism with substance: a C-CDA 2.1 API endpoint producing standard clinical document sections. The 19 sections are the standard C-CDA sections that map directly to USCDI data classes — allergies, medications, problems, encounters, immunizations, vitals, social history, procedures, labs, implantable devices, goals, functional/cognitive status, referrals, assessments, care team, health concerns, plan of treatment, and diagnostic/imaging reports.

This is a **textbook clinical summary export**. The section list maps 1:1 to what a C-CDA Continuity of Care Document (CCD) or Summary of Episode Note would contain. There is no evidence of any content beyond standard C-CDA templates.

The compliance page mentions CSV and HTML formats, which *could* theoretically contain billing, specialty, or administrative data. However, with zero documentation about their content, structure, or how to generate them, they cannot be assessed. The vendor has not demonstrated that these formats export anything beyond what the C-CDA API provides.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | Included in C-CDA header (standard); patient search API accepts name/DOB/SSN/email/phone | C-CDA demographic header is limited; no dedicated demographics export documented |
| Encounters / visits | ⚠️ Partial | `PAT_ENCOUNTER` C-CDA section | Section-level only; no field detail; unclear if encounter notes included |
| Problems / conditions | ⚠️ Partial | `PAT_PROBLEM` C-CDA section | Section-level only; standard C-CDA problem list |
| Medications / prescriptions | ⚠️ Partial | `PAT_MEDS` C-CDA section | Section-level only; e-prescribing history (EPCS, Surescripts) unclear |
| Allergies | ⚠️ Partial | `PAT_ALLERGY` C-CDA section | Section-level only |
| Immunizations | ⚠️ Partial | `PAT_IMMUNIZATION` C-CDA section | Section-level only |
| Vitals | ⚠️ Partial | `PAT_VITALS` C-CDA section | Section-level only |
| Lab results | ⚠️ Partial | `PAT_LABS` C-CDA section | Section-level only; Quest Diagnostics integration data unclear |
| Imaging / diagnostic reports | ⚠️ Partial | `PAT_DI_REPORT` C-CDA section | Section-level only |
| Procedures | ⚠️ Partial | `PAT_PROCEDURES` C-CDA section | Section-level only |
| Clinical notes / documents | ❌ Not covered | No explicit clinical notes/documents section | Product has clinical charting, progress notes, custom templates; no export documented |
| Care plans / goals | ⚠️ Partial | `PAT_GOALS`, `PAT_PLANOFTREAT` C-CDA sections | Section-level only |
| Orders / referrals | ⚠️ Partial | `PAT_REFERRAL` C-CDA section | Referrals only; no general order export |
| Insurance / coverage | ❌ Not covered | No insurance/coverage entities in export | Product has insurance benefits verification; significant gap |
| Claims / billing | ❌ Not covered | No billing entities in export | Product has integrated billing module with superbills, claims, RCM; **major gap** |
| Payments | ❌ Not covered | No payment entities in export | Product processes payments via patient portal and clearinghouses; gap |
| Consents / directives | ❌ Not covered | No consent entities in export | Product has a dedicated Consent Module; gap |
| Patient communications | ❌ Not covered | No communications/messaging entities | Product has patient portal messaging, SMS, secure messaging; gap |
| Behavioral health | ❌ Not covered | No behavioral health-specific entities | Product has dedicated BH module ($65/user/month); **significant gap** |
| ASC / surgical data | ❌ Not covered | No surgical-specific entities | Product has ASC module ($750/OR/month); gap |
| Residential treatment | ❌ Not covered | No residential treatment entities | Product has residential treatment module ($150/bed); gap |
| Workers' comp / no-fault | ❌ Not covered | No workers' comp entities | Product has specialized WC/no-fault module; gap |

**Summary**: 12 domains receive some coverage (all ⚠️ Partial because only section-level documentation exists without field detail); 10 domains that the product stores are completely absent from the documented export. The covered domains are exclusively standard C-CDA clinical sections — the USCDI data set.

## 6. Documentation Quality

The documentation is **very poor**:

- **No data dictionary**: Zero field-level documentation for any format.
- **No sample data**: No example exports in any format.
- **No schema/template documentation**: No C-CDA template OIDs, XSD references, or structural specifications.
- **Generic format descriptions**: The compliance page's CSV and HTML "documentation" consists of dictionary definitions of these file formats (e.g., "A comma-separated values file is a delimited text file..."), not descriptions of export content.
- **Copy-paste errors**: The API documentation has a duplicated `USERNAME` parameter in the patient data endpoint. The `mediehrgetpatientdata.php` block reuses an HTML `id` from another endpoint.
- **No export instructions**: No user-facing documentation exists for how to perform a UI-based export. The API docs describe programmatic access but require registration and facility approval.
- **No versioning**: The compliance page claims quarterly updates but provides no version history.

A developer could not build an import system from this documentation. They would know the API endpoint structure and authentication flow, but not the detailed structure of C-CDA output, what coded values to expect, or what (if anything) the CSV/HTML exports contain.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Minimal/stub/unclear**

The documented export covers only standard C-CDA clinical sections — the USCDI data set that every certified EHR must support for clinical exchange. Despite the product storing substantial billing data (integrated billing module, superbills, claims, clearinghouse integrations), specialty clinical data (behavioral health, ASC, residential treatment, workers' comp), patient communications (portal messaging, SMS), and consent records, none of these domains appear in the documented export. The CSV and HTML formats mentioned on the compliance page are entirely undocumented, making it impossible to assess whether they cover any additional domains. With zero field-level documentation and no sample data, the actual breadth of even the C-CDA export cannot be independently verified.

**Axis 2 — Export approach: Repackaged existing export**

The export is a C-CDA 2.1 document with exactly the standard clinical sections used for care coordination and clinical exchange. The 19 sections map 1:1 to standard C-CDA/USCDI categories. There is no product-specific data dictionary, no mapping beyond standard C-CDA templates, no billing or operational data, and no vendor extensions. This is the vendor's existing clinical document export (used for transitions of care and patient access under other certification criteria) relabeled as (b)(10). The proprietary REST API (`mediehrgetpatientdata.php`) appears to be the same patient data export endpoint used for (g)(10) clinical exchange, presented as the (b)(10) solution. The mention of CSV and HTML on the compliance page could indicate additional export capability, but with zero documentation, this is unverifiable.

### Key Findings

1. **No data dictionary at all.** Zero field-level documentation exists for any export format. The only structured information is 19 C-CDA section names that can be toggled on/off. This is among the thinnest export documentation possible. (Source: `compliance-page.html`, `API_Document.html`)

2. **C-CDA export is standard clinical exchange, not (b)(10).** The 19 documented sections are the standard C-CDA CCD sections mapping directly to USCDI data classes. No evidence of vendor-specific extensions, billing data, or specialty content. (Source: `api-docs.json`, 19 sections listed)

3. **Significant product capabilities are absent from export.** Medi-EHR has integrated billing/PM, behavioral health, ASC, residential treatment, and workers' comp modules — all generating patient-specific EHI. None appear in the documented export. (Source: `product-research.md` vs. `api-docs.json`)

4. **CSV and HTML formats are ghosts.** The compliance page mentions these formats but provides literally zero information about their content. The CSV description reads: "A comma-separated values (CSV) file is a delimited text file that uses a comma to separate values." This is a dictionary definition, not export documentation. (Source: `compliance-page.html`)

5. **API has quality issues.** Duplicated `USERNAME` parameter, copy-paste HTML `id` errors, proprietary auth (not OAuth 2.0), and no bulk export mechanism despite claiming multi-patient capability. (Source: `api-docs.json`, `API_Document.html`)

### Summary Stats

    Coverage:        Minimal/stub/unclear
    Approach:        Repackaged existing export
    Export format:   C-CDA 2.1 XML (documented); CSV and HTML (mentioned, undocumented)
    Entities:        19 C-CDA sections (section-level only)
    Fields:          0 (no field-level documentation)
    Descriptions:    N/A (no fields documented)
    Sample data:     No
    Bulk export:     Unclear (claimed but no mechanism documented)
    Domains covered: 0 of 19 fully covered; 12 of 19 partially (section-level only); 10 entirely absent

### Bottom Line

Medi-EHR's (b)(10) export documentation is a compliance stub. The documented export is a standard C-CDA clinical document — the same output used for clinical exchange and patient access — with no field-level detail, no sample data, and no coverage of the billing, specialty, or administrative data the product stores. A patient or provider would receive a clinical summary, not a complete copy of their data.
