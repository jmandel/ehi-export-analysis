# EHI Export Analysis: Medi-EHR, LLC

**Product**: Medi-EHR v2.1
**Analysis date**: 2026-02-15
**CHPL IDs**: 15.02.05.2979.MEDI.01.01.1.220215 (CHPL ID 10831)

## 1. Product Context

Medi-EHR is a cloud-based, full-featured ambulatory EHR with integrated billing/practice management, built on Oracle 11g and delivered via web browser. It is developed by a small, privately-held company in Bedminster, NJ, and targets small to medium-sized practices across multiple clinical settings.

**Clinical modules**: Clinical EHR with customizable templates, e-prescribing (including EPCS), CPOE for medications/labs/imaging, lab and radiology integration (Quest Diagnostics), document management, and consent management.

**Specialty modules**: Ambulatory Surgery Center ($750/OR/month), Behavioral Health ($65/user/month), Residential Treatment Facility ($150/bed), and Workers' Compensation/No-Fault.

**Administrative modules**: Integrated billing/practice management with superbills, claims, RCM, clearinghouse integrations (Optum, Waystar, Change Healthcare), insurance benefits verification, scheduling, and appointment reminders.

**Patient-facing**: Patient portal (messaging, prescription refills, bill payment, records access), kiosk (intake, consent forms, multilingual), telemedicine (video conferencing).

**Certification breadth**: Certified across 37 ONC criteria including (b)(10) EHI export, (g)(7)–(g)(10) FHIR APIs, and public health reporting. This is a broadly certified product — not a niche module.

**Baseline expectation**: Given the integrated billing/PM, multiple specialty modules, patient portal, and consent module, a complete EHI export should cover clinical data, billing/claims, insurance, patient portal data, consent forms, and specialty-specific clinical data (behavioral health assessments, surgical records, residential treatment records).

## 2. Artifacts Reviewed

| Artifact | Size | Description | Informative? |
|---|---|---|---|
| `compliance-page.html` | 196 KB | Main compliance page; Section I describes EHI export in CSV/HTML, Section II links to API docs | **Low** — 3 paragraphs of generic text, no data dictionary |
| `compliance-page.png` | 1.2 MB | Full-page screenshot of compliance page | **Low** — confirms the page is sparse |
| `API_Document.html` | 359 KB | Swagger UI page for MediEHR Patient Access API v2.1; 4 endpoints | **Medium** — documents 19 C-CDA sections, proprietary auth |
| `developer-portal-api-docs.png` | 177 KB | Screenshot of Oracle APEX developer portal with Swagger UI iframe | **Low** — confirms portal structure |
| `fhir-service-base-bundle.json` | 1.2 KB | FHIR Bundle pointing to InteropEngine sandbox | **Low** — confirms (g)(10) is separate from (b)(10) |
| `public-fhir-api-page.html` | 197 KB | Public FHIR API page; production endpoints "Coming Soon" | **Low** — not relevant to (b)(10) |
| `enrichment/api-docs.json` | 14 KB | Structured JSON extraction: 4 endpoints, 44 parameters, 19 C-CDA sections, 8 error codes | **Most informative** — machine-readable API inventory |
| `enrichment/extract-api-docs.ts` | 7.5 KB | Bun script that parsed API_Document.html | N/A (tooling) |
| `enrichment/README.md` | 1 KB | Enrichment script documentation | N/A (tooling) |

**Most informative**: The `enrichment/api-docs.json` extraction provides the clearest picture of the API. The compliance page and API Document HTML are the primary sources but contain minimal substance.

**No data dictionary, schema, sample data, or field-level documentation was found in any artifact.**

## 3. Export Mechanics

**Documented formats**: The compliance page mentions three formats:
1. **CSV** — described generically as "a delimited text file that uses a comma to separate values." No field list, no schema, no sample file, no instructions for how to produce the export.
2. **HTML** — described generically as "the standard markup language for documents designed to be displayed in a web browser." Same lack of specifics.
3. **C-CDA 2.1 XML** — available via the proprietary REST API (`/mediehrgetpatientdata.php`), with 19 selectable clinical sections.

**Mechanism**:
- **UI export**: The compliance page states users can "export electronic health information (EHI) for a single patient at any time without developer assistance" — implying an in-app UI button. However, no screenshots, instructions, or documentation for this UI workflow are provided.
- **API export**: The documented API endpoint (`POST /mediehrgetpatientdata.php`) accepts a single patient MRN and date range, returning C-CDA 2.1 XML. Authentication uses proprietary access/refresh tokens (not OAuth 2.0 or SMART on FHIR). The server URL is `https://proda.mediemr.net/patient/v1`.

**Single vs. bulk**: The compliance page claims multi-patient export capability ("Medi-EHR can export all the data for a patient population"), but the API only documents a single-patient endpoint requiring `PATIENT_MRN`. No bulk export endpoint is documented.

**Access constraints**: API access requires registration on the developer portal (`https://proda.mediemr.net:8443/pls/htmldb/f?p=300`), facility approval, and proprietary token management (access token valid 60 minutes, refresh token valid 1 year). No fees are mentioned for the export itself, though the product has a separate paid "Custom Export" service.

## 4. Export Content: What's In It

### What the documentation tells us

The **only concrete, enumerated content** in the export documentation is the 19 C-CDA sections available through the API. No field-level, data-type, or value-set documentation exists for any format.

**C-CDA 2.1 API — 19 sections:**

| # | API Parameter | C-CDA Section | Toggle |
|---|---|---|---|
| 1 | PAT_ALLERGY | Allergies | S/H |
| 2 | PAT_MEDS | Medications | S/H |
| 3 | PAT_PROBLEM | Problems | S/H |
| 4 | PAT_ENCOUNTER | Encounters | S/H |
| 5 | PAT_IMMUNIZATION | Immunizations | S/H |
| 6 | PAT_VITALS | Vitals | S/H |
| 7 | PAT_SOCHX | Social History | S/H |
| 8 | PAT_PROCEDURES | Procedures | S/H |
| 9 | PAT_LABS | Labs | S/H |
| 10 | PAT_IMPLANTABLEDEVICES | Implantable Devices | S/H |
| 11 | PAT_GOALS | Goals | S/H |
| 12 | PAT_FUNCTIONALSTATUS | Functional Status | S/H |
| 13 | PAT_COGNITIVESTATUS | Cognitive Status | S/H |
| 14 | PAT_REFERRAL | Referrals | S/H |
| 15 | PAT_ASSESSMENT | Assessment | S/H |
| 16 | PAT_CARETEAM | Care Team | S/H |
| 17 | PAT_HEALTH_CONCERNS | Health Concerns | S/H |
| 18 | PAT_PLANOFTREAT | Plan of Treatment | S/H |
| 19 | PAT_DI_REPORT | Diagnostic and Imaging Reports | S/H |

Each section can be individually toggled on (`S`) or off (`H`), or all can be included with `ALL_DATA_CATEGORIES=S`. The response is a complete `<ClinicalDocument>` in HL7 CDA format.

**CSV and HTML exports**: Zero documentation beyond generic file format definitions. No field lists, no table names, no sample data, no instructions for generating these exports. It is impossible to assess what these formats contain from the available documentation.

### What's missing from the documentation

The API documentation has notable quality issues:
- **Duplicated parameter**: The `mediehrgetpatientdata.php` endpoint lists `USERNAME` twice (confirmed in `api-docs.json`, lines 160–168).
- **Copy-paste errors**: Parameter descriptions for `PATIENT_MOBILE` and `PATIENT_MOTHERSMAIDENNAME` both say "The username in the office number" — clearly wrong.
- **No response schema**: The C-CDA response is described only as `...CCDA Document...` — no template IDs, no example document, no field definitions.
- **No OpenAPI spec**: The Swagger UI is a static pre-rendered HTML page (last modified 2021-12-01 per server headers); there is no downloadable OpenAPI/Swagger JSON specification.

### Vendor's own content organization

The vendor does not organize export content into categories. The only structure is the 19 C-CDA section parameters. There is no data dictionary, no entity list, and no category system.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor's documented export consists of a single C-CDA 2.1 document with 19 toggleable clinical sections. This is essentially a **standard clinical summary** — the same content typically used for care transitions and the (g)(10) FHIR API. The 19 sections map closely to standard US Core / USCDI data classes.

The vendor also mentions CSV and HTML exports on their compliance page, but these are completely undocumented. Without any field lists, schemas, or samples, it is impossible to determine whether these formats include data beyond the C-CDA sections (e.g., billing, specialty data) or are simply alternative renderings of the same clinical summary.

The vendor's FHIR API (powered by InteropEngine) is explicitly separate from the (b)(10) export and was not yet in production ("Coming Soon") at the time of review.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | Patient search endpoint has name, DOB, SSN, email, mobile; Social History C-CDA section | No explicit demographics export with address, race, ethnicity, language, marital status, or emergency contacts |
| Encounters / visits | ⚠️ Partial | PAT_ENCOUNTER C-CDA section | Section present but no field-level detail; unknown depth |
| Problems / conditions / diagnoses | ⚠️ Partial | PAT_PROBLEM, PAT_HEALTH_CONCERNS C-CDA sections | Standard C-CDA sections; unknown whether vendor-specific problem list data is fully captured |
| Medications / prescriptions | ⚠️ Partial | PAT_MEDS C-CDA section | C-CDA medication section present; e-prescribing transmission history and EPCS records not specifically addressed |
| Allergies | ⚠️ Partial | PAT_ALLERGY C-CDA section | Standard section present; no field-level detail |
| Immunizations | ⚠️ Partial | PAT_IMMUNIZATION C-CDA section | Standard section present; no field-level detail |
| Vitals | ⚠️ Partial | PAT_VITALS C-CDA section | Standard section present; no field-level detail |
| Lab results | ⚠️ Partial | PAT_LABS C-CDA section | Section present; unknown whether full discrete results or summaries |
| Imaging / diagnostic reports | ⚠️ Partial | PAT_DI_REPORT C-CDA section | Report text likely included; actual images not exported |
| Procedures | ⚠️ Partial | PAT_PROCEDURES, PAT_IMPLANTABLEDEVICES C-CDA sections | Standard sections present; ASC surgical detail not specifically addressed |
| Clinical notes / documents | ⚠️ Partial | PAT_ASSESSMENT, PAT_FUNCTIONALSTATUS, PAT_COGNITIVESTATUS C-CDA sections | No dedicated clinical notes section for progress notes, H&P, discharge summaries, or specialty templates |
| Care plans / goals | ⚠️ Partial | PAT_GOALS, PAT_PLANOFTREAT, PAT_CARETEAM C-CDA sections | Standard sections present |
| Orders / referrals | ⚠️ Partial | PAT_REFERRAL C-CDA section | Referrals present; CPOE orders (medications, labs, imaging) not explicitly addressed as separate export content |
| Insurance / coverage | ❌ Not covered | No insurance entities in documented export | Product has insurance benefits verification module; **significant gap** |
| Claims / billing | ❌ Not covered | No billing entities in documented export | Product has integrated billing/PM with superbills, claims, and RCM; **significant gap** |
| Payments | ❌ Not covered | No payment entities in documented export | Product processes payments via patient portal and billing module; **gap** |
| Consents / directives | ❌ Not covered | No consent entities in documented export | Product has dedicated Consent Module; **gap** |
| Patient communications / portal messages | ❌ Not covered | No portal/messaging entities in documented export | Product has patient portal with secure messaging, refill requests; **gap** |
| Specialty-specific (Behavioral Health) | ❌ Not covered | No BH-specific entities in documented export | Product has dedicated Behavioral Health module at $65/user/month; assessments and treatment plans not in export; **significant gap** |
| Specialty-specific (ASC/Surgical) | ❌ Not covered | No ASC-specific entities in documented export | Product has ASC module at $750/OR/month; pre-op/post-op data not addressed; **significant gap** |
| Specialty-specific (Residential Treatment) | ❌ Not covered | No residential treatment entities in documented export | Product has Residential Treatment module at $150/bed; addiction treatment records not addressed; **significant gap** |

**Summary**: 0 of 21 domains fully covered, 13 partially covered (via C-CDA sections with no field-level detail), 8 not covered at all. All 8 uncovered domains represent data the product demonstrably stores.

## 6. Documentation Quality

**Overall quality: Very poor.**

- **No data dictionary**: There are zero field-level definitions in any artifact. The only enumerated content is 19 C-CDA section names.
- **No sample data**: No example C-CDA documents, no sample CSV files, no sample HTML files.
- **No machine-readable schema**: No OpenAPI/Swagger JSON, no XSD for the C-CDA output, no C-CDA template IDs.
- **Generic format descriptions**: The CSV and HTML descriptions on the compliance page are textbook definitions of the formats themselves, not descriptions of the export data content.
- **API docs have errors**: Duplicated USERNAME parameter, copy-paste errors in descriptions ("The username in the office number" for PATIENT_MOBILE and PATIENT_MOTHERSMAIDENNAME).
- **Stale documentation**: The API Document HTML file was last modified 2021-12-01 (per HTTP `Last-Modified` header), despite the compliance page stating formats are updated quarterly.
- **No export instructions**: No user-facing documentation for how to perform the CSV or HTML exports from within the application.

**Could a developer build an import from this documentation?** No. A developer would know the 4 API endpoints and authentication flow, but would have no idea what data elements to expect in the C-CDA output, what coded values are used, or what the CSV/HTML exports contain. Without sample data or field definitions, implementing a reliable data import would require reverse-engineering actual export files.

## 7. Overall Assessment

### Classification

**Minimal/stub**

The documented export is a C-CDA 2.1 clinical summary via a proprietary API — a standard-based projection covering approximately USCDI-level clinical data. However, the documentation is so thin (19 section names with no field-level detail, no data dictionary, no sample data) that it barely rises above a stub. The CSV and HTML formats mentioned on the compliance page are completely undocumented. The export clearly omits major data domains the product stores (billing, insurance, consent, patient portal, behavioral health, ASC, residential treatment).

### Key Findings

1. **Classic C-CDA repackaging**: The documented (b)(10) export is a C-CDA 2.1 document with 19 clinical sections — essentially the same clinical summary content used for care transitions. This covers approximately USCDI-level data but misses the full designated record set. (`API_Document.html`, `enrichment/api-docs.json`)

2. **8 of 21 applicable data domains have zero coverage**: Billing/claims, insurance, payments, consents, patient portal messages, behavioral health, ASC surgical data, and residential treatment data are all absent from the documented export — despite the product having dedicated modules for each. (`compliance-page.html` — no mention of these domains)

3. **No data dictionary at any level**: Not a single field name, data type, or value set is documented for any export format. The most granular documentation is 19 C-CDA section names. (`compliance-page.html`, `API_Document.html`)

4. **CSV and HTML exports are phantom documentation**: The compliance page mentions these formats but provides only generic Wikipedia-style definitions of CSV and HTML. No field lists, no schemas, no instructions for generating them, no sample files. It is impossible to assess whether these formats contain additional data beyond what the C-CDA API exports.

5. **API documentation has quality issues**: Duplicated parameters, copy-paste errors in field descriptions, stale content (last modified December 2021), and no machine-readable specification. (`enrichment/api-docs.json` — USERNAME duplicated; PATIENT_MOBILE description wrong)

### Summary Stats

```
Classification:  Minimal/stub
Export format:   C-CDA 2.1 XML (via API); CSV and HTML mentioned but undocumented
Model type:      Standard projection (C-CDA)
Entities:        N/A (no data dictionary; 19 C-CDA sections documented)
Fields:          N/A (no field-level documentation)
Descriptions:    N/A
Sample data:     No
Bulk export:     Claimed on compliance page but no API mechanism documented
Domains covered: 13 of 21 partial; 0 fully covered; 8 not covered
```

### Bottom Line

Medi-EHR's EHI export documentation is a compliance checkbox, not a substantive data export capability. A patient or provider requesting their complete record would receive a C-CDA clinical summary — missing billing records, insurance data, consent forms, patient portal messages, and all specialty-specific data (behavioral health, surgical, residential treatment). The single biggest gap is the total absence of billing/claims data from a product with an integrated billing/practice management module, combined with no documentation whatsoever for the CSV/HTML exports that might theoretically contain it.
