# EHI Export Analysis: Medi-EHR, LLC

**Product**: Medi-EHR v2.1
**Analysis date**: 2026-02-16
**CHPL IDs**: 10831 (15.02.05.2979.MEDI.01.01.1.220215)

## 1. Product Context

Medi-EHR is a cloud-based (SaaS) EHR platform built on Oracle 11g, serving small to medium-sized healthcare practices. It is a broadly certified ambulatory EHR (37 ONC criteria) with integrated billing/practice management, e-prescribing (including EPCS), scheduling, patient portal, telemedicine, and FHIR API support.

The product serves multiple clinical settings with dedicated modules:
- **Primary care / ambulatory clinics** ($495/provider/month)
- **Ambulatory Surgery Centers** ($750/OR or procedure room/month)
- **Behavioral health** ($65/user/month)
- **Residential treatment facilities** ($150/bed)
- **Workers' compensation / no-fault** (specialized claims processing)

Key data domains the product stores (relevant to EHI export completeness):
- **Clinical**: demographics, problem lists, medications, allergies, vitals, immunizations, lab results, radiology reports, procedures, clinical notes/templates, consent forms
- **Billing/PM**: superbills, claims, payments, revenue cycle management, insurance verification, workers' comp/no-fault claims
- **Administrative**: scheduling, patient portal messages, refill requests, intake forms
- **Specialty**: behavioral health assessments/treatment plans, ASC surgical workflows, residential treatment records
- **E-prescribing**: Surescripts integration, EPCS with MFA
- **Care coordination**: C-CDA transitions of care, direct messaging, FHIR API

This is a full-featured EHR with substantial billing and specialty clinical capabilities beyond basic clinical charting.

## 2. Artifacts Reviewed

| Artifact | Type | Size | Description | Informativeness |
|---|---|---|---|---|
| `compliance-page.html` | HTML page | 196 KB | Main EHI compliance page. ~3 paragraphs on EHI export plus generic CSV/HTML format definitions. No data dictionary, no field lists, no schema. | **Low** — minimal content |
| `compliance-page.png` | Screenshot | 1.2 MB | Full-page screenshot confirming rendered content matches HTML parse. Shows the entire compliance page fits in ~1 screen. | Low (confirmatory) |
| `API_Document.html` | Swagger UI HTML | 359 KB | Pre-rendered Swagger UI documenting 4 proprietary REST API endpoints. Most informative artifact — documents the C-CDA 2.1 export endpoint with 19 toggleable sections. | **Medium** — most informative |
| `developer-portal-api-docs.png` | Screenshot | 177 KB | Oracle APEX developer portal showing embedded Swagger UI. Confirms authentication scheme (access/refresh tokens) and server URL. | Low (confirmatory) |
| `enrichment/api-docs.json` | Extracted JSON | 14 KB | Structured extraction of API_Document.html: 4 endpoints, all parameters, 19 C-CDA section toggles, 8 error codes. | Medium (structured parse) |
| `fhir-service-base-bundle.json` | FHIR Bundle | 1.2 KB | FHIR R4 service base URL bundle pointing to InteropEngine sandbox server. This is the (g)(10) FHIR API — **not** the (b)(10) EHI export. | Low (not EHI export) |
| `public-fhir-api-page.html` | HTML page | 197 KB | Public FHIR API page linking to InteropEngine. Production endpoints listed as "Coming Soon." Not EHI export documentation. | Low (not EHI export) |

**Most informative**: `API_Document.html` and its structured extraction `enrichment/api-docs.json` — these are the only artifacts with any technical detail about the export content.

**Least informative**: The compliance page itself provides almost no technical detail — the CSV and HTML descriptions are dictionary definitions of those file formats, not descriptions of the export data.

## 3. Export Mechanics

**Documented export mechanism**: Proprietary REST API returning C-CDA 2.1 XML documents.

- **Format**: C-CDA 2.1 XML (HL7 Clinical Document Architecture)
- **Mechanism**: API call to `POST /mediehrgetpatientdata.php` at `https://proda.mediemr.net/patient/v1`
- **Single-patient**: Yes — the API accepts a single `PATIENT_MRN` parameter with date range filters (`START_DATE_MMDDYYYY`, `END_DATE_MMDDYYYY`)
- **Bulk/multi-patient**: The compliance page claims "Medi-EHR can export all the data for a patient population in our standardized format" but the API documentation provides no bulk export endpoint. The only patient data endpoint takes a single MRN. How multi-patient export works is undocumented.
- **Authentication**: Proprietary access/refresh token scheme (not OAuth 2.0 or SMART on FHIR). Tokens obtained by registering on the developer portal (`https://proda.mediemr.net:8443/pls/htmldb/f?p=300`) and getting office/facility approval. Access tokens expire after 60 minutes; refresh tokens valid for 1 year.
- **Additional formats claimed**: The compliance page mentions CSV and HTML export formats, but provides zero documentation on what these contain, how to obtain them, or what fields they include. It is unclear whether these are UI-based exports within the application or API-based.
- **Access constraints**: Requires developer portal registration and office approval. No mention of fees for the API, but Medi-EHR offers a separate paid "Custom Export" service (marketing page at `/custom-export/`).

**Notable issues**:
- The `mediehrgetpatientdata.php` endpoint has a duplicated `USERNAME` parameter (appears twice in the documentation) — likely a copy-paste error.
- No OpenAPI/Swagger JSON spec is available; only a pre-rendered static HTML page.
- The API title says "Medi-EMR" (not "Medi-EHR") suggesting possible copy-paste from a related product.

## 4. Export Content: What's In It

### What the documentation tells us

The export is a **C-CDA 2.1 clinical document** with 19 toggleable sections. Each section can be included (`S`) or excluded with NullFlavour (`H`). An `ALL_DATA_CATEGORIES` master toggle can include all sections at once.

There is **no data dictionary** at any level of granularity. The documentation provides:
- 19 section names (e.g., "Allergies," "Medications," "Problems")
- Toggle parameters (S/H) for each section
- No field-level detail within any section
- No coded values, terminologies, or template IDs
- No sample C-CDA output (the API docs show a placeholder `...CCDA Document...`)
- No description of what specific data elements appear in each C-CDA section

### Vendor's own content organization

The vendor does not organize the export into categories — all 19 sections are presented as a flat list of C-CDA components within a single API endpoint. The only categorization is implicit: these are all clinical data sections of a C-CDA document.

| C-CDA Section | Parameter | Fields | Described | Types | Category |
|---|---|---|---|---|---|
| Allergies and Adverse Reactions | PAT_ALLERGY | N/A | No | No | Clinical |
| Medications | PAT_MEDS | N/A | No | No | Clinical |
| Problems / Diagnoses | PAT_PROBLEM | N/A | No | No | Clinical |
| Encounters | PAT_ENCOUNTER | N/A | No | No | Clinical |
| Immunizations | PAT_IMMUNIZATION | N/A | No | No | Clinical |
| Vital Signs | PAT_VITALS | N/A | No | No | Clinical |
| Social History | PAT_SOCHX | N/A | No | No | Clinical |
| Procedures | PAT_PROCEDURES | N/A | No | No | Clinical |
| Laboratory Results | PAT_LABS | N/A | No | No | Clinical |
| Implantable Devices | PAT_IMPLANTABLEDEVICES | N/A | No | No | Clinical |
| Goals | PAT_GOALS | N/A | No | No | Clinical |
| Functional Status | PAT_FUNCTIONALSTATUS | N/A | No | No | Clinical |
| Cognitive Status | PAT_COGNITIVESTATUS | N/A | No | No | Clinical |
| Referrals | PAT_REFERRAL | N/A | No | No | Clinical |
| Assessment | PAT_ASSESSMENT | N/A | No | No | Clinical |
| Care Team Members | PAT_CARETEAM | N/A | No | No | Clinical |
| Health Concerns | PAT_HEALTH_CONCERNS | N/A | No | No | Clinical |
| Plan of Treatment | PAT_PLANOFTREAT | N/A | No | No | Clinical |
| Diagnostic and Imaging Reports | PAT_DI_REPORT | N/A | No | No | Clinical |

**Field counts**: Not applicable. Zero fields are individually documented. The 19 C-CDA sections are the finest level of granularity provided.

**Sample data**: None provided. No example C-CDA documents, no test patient records, no sample CSV or HTML files.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor provides a single category of export content: **C-CDA 2.1 clinical sections**. All 19 sections are clinical in nature, mapping to standard C-CDA template sections defined by HL7. This is essentially a USCDI-level clinical summary — the same data that would be exchanged for care transitions.

The 19 sections cover the core clinical domains (allergies, medications, problems, encounters, immunizations, vitals, procedures, labs, imaging) plus extended clinical data (functional status, cognitive status, goals, health concerns, care plans, care team, assessments, referrals, social history).

**No non-clinical data is documented in the export.** The C-CDA standard does not natively support billing data, insurance claims, patient portal messages, consent forms, or specialty-specific assessment instruments. The vendor has not documented any supplementary export mechanism (CSV, HTML, or otherwise) that would cover these domains.

The compliance page's mention of CSV and HTML formats _could_ theoretically cover non-clinical data, but with zero documentation, this is unverifiable. The CSV and HTML descriptions on the compliance page are literal dictionary definitions of those file formats — they tell a developer nothing about what data would be in those files.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | C-CDA header contains patient demographics by standard, but no specific documentation of what demographic fields are included | Product stores full demographics; C-CDA header likely includes basics (name, DOB, address, MRN) but detail is unknown |
| Encounters / visits | ⚠️ Partial | `PAT_ENCOUNTER` C-CDA section | Section exists but no field-level detail. Encounter documentation depth unknown. |
| Problems / conditions | ✅ Covered | `PAT_PROBLEM` C-CDA section | Standard C-CDA problem list section |
| Medications / prescriptions | ⚠️ Partial | `PAT_MEDS` C-CDA section | C-CDA medication section likely covers active meds. Full e-prescribing history (Surescripts transmissions, EPCS records, refill history) unlikely to be in C-CDA. |
| Allergies | ✅ Covered | `PAT_ALLERGY` C-CDA section | Standard C-CDA allergy section |
| Immunizations | ✅ Covered | `PAT_IMMUNIZATION` C-CDA section | Standard C-CDA immunization section |
| Vitals | ✅ Covered | `PAT_VITALS` C-CDA section | Standard C-CDA vital signs section |
| Lab results | ✅ Covered | `PAT_LABS` C-CDA section | Standard C-CDA results section |
| Imaging / diagnostic reports | ✅ Covered | `PAT_DI_REPORT` C-CDA section | Standard C-CDA section |
| Procedures | ✅ Covered | `PAT_PROCEDURES` C-CDA section | Standard C-CDA procedures section |
| Clinical notes / documents | ❌ Not covered | No clinical notes/documents section in the 19 C-CDA sections | Product stores progress notes, clinical documentation with customizable templates. No mechanism to export these. Significant gap. |
| Care plans / goals | ✅ Covered | `PAT_GOALS`, `PAT_PLANOFTREAT`, `PAT_HEALTH_CONCERNS` C-CDA sections | Multiple related sections present |
| Orders / referrals | ⚠️ Partial | `PAT_REFERRAL` C-CDA section | Referrals covered; lab/imaging orders (CPOE) not explicitly a separate export section |
| Insurance / coverage | ❌ Not covered | No insurance/coverage entity in export | Product stores insurance/benefits data. Not in C-CDA export. Gap. |
| Claims / billing | ❌ Not covered | No billing entity in export | Product has integrated billing/PM with superbills, claims, payments, revenue cycle management. Significant gap. |
| Payments | ❌ Not covered | No payment entity in export | Product processes payments. Not in export. Gap. |
| Consents / directives | ❌ Not covered | No consent entity in export | Product has dedicated Consent Module. Not in export. Gap. |
| Patient communications / portal messages | ❌ Not covered | No messaging entity in export | Product has patient portal with secure messaging. Not in export. Gap. |
| Specialty: Behavioral health | ❌ Not covered | No behavioral health-specific sections | Product has dedicated behavioral health module. C-CDA sections are generic, not specialty-specific. Gap. |
| Specialty: ASC surgical data | ❌ Not covered | No surgical-specific sections | Product has dedicated ASC module. C-CDA procedures section is generic. Gap. |
| Specialty: Residential treatment | ❌ Not covered | No residential treatment sections | Product has dedicated residential treatment module. Not in export. Gap. |
| Specialty: Workers' comp / no-fault | ❌ Not covered | No workers' comp entity in export | Product has specialized workers' comp/no-fault claims module. Not in export. Gap. |

**Summary**: 7 of 15 applicable EHI domains have documented coverage via C-CDA sections (problems, allergies, immunizations, vitals, labs, imaging, procedures). 4 domains have partial coverage (demographics, encounters, medications, orders/referrals — present as C-CDA sections but depth is unknown). 10+ domains with clear gaps, including billing, insurance, clinical notes, patient communications, consent forms, and all specialty modules.

## 6. Documentation Quality

The EHI export documentation is **extremely thin** — among the sparsest possible while still technically existing.

**What a developer gets:**
- The compliance page: 3 short paragraphs and two generic file format definitions (~150 words of actual EHI content)
- The API documentation: 4 REST endpoints with parameter names/types and a list of 19 C-CDA section toggles
- Authentication flow: proprietary token scheme described in the API docs

**What a developer does NOT get:**
- No data dictionary at any level of granularity
- No field-level documentation within any C-CDA section
- No sample export data (no example C-CDA documents, no sample CSV/HTML files)
- No machine-readable schema (no OpenAPI JSON, no XSD, no C-CDA template OIDs)
- No documentation of the CSV or HTML export formats beyond dictionary definitions
- No documentation of how to perform the export from the UI
- No value sets, code systems, or terminology references
- No relationship documentation
- No instructions for multi-patient/bulk export (despite claiming this capability)

**Could a developer build an import from this documentation?** No. A developer would know the API URL and authentication flow, and that the output is C-CDA 2.1 XML, but they would not know the specific C-CDA templates used, what coded values to expect, what optional elements are populated, or what the CSV/HTML exports contain. They would need to make API calls to a real system and reverse-engineer the output format.

## 7. Overall Assessment

### Classification

**Standard-based projection** — The documented export is a C-CDA 2.1 clinical document delivered via a proprietary REST API. This covers approximately USCDI-level clinical summary data but misses the vendor's substantial billing, specialty, and administrative data. The vendor is essentially repackaging their existing clinical document exchange capability (appropriate for transitions of care and the (g)(10) API) as their (b)(10) EHI export.

### Key Findings

1. **The export is a C-CDA clinical summary, not a full EHI export.** The 19 documented C-CDA sections cover standard clinical data (allergies, medications, problems, labs, etc.) but exclude billing, insurance, clinical notes, consent forms, patient portal data, and all specialty module data. This is a textbook case of (b)(10)/(g)(10) conflation — the vendor appears to be using the same clinical document output for both requirements.

2. **Billing and specialty data are entirely absent despite the product storing substantial amounts.** Medi-EHR has integrated billing/PM, workers' comp, behavioral health, ASC, and residential treatment modules. None of these data domains appear in the documented export. These are core EHI — part of the designated record set.

3. **The CSV and HTML export formats mentioned on the compliance page are completely undocumented.** The compliance page says these formats exist and are "updated quarterly," but provides only dictionary definitions of CSV and HTML as file formats. No field lists, no sample data, no instructions. These _could_ cover the missing domains, but there is no evidence either way.

4. **Documentation quality is among the poorest possible.** There is no data dictionary, no sample data, no machine-readable schema, and no field-level documentation. The 19 C-CDA section names are the only substantive technical content. A developer cannot implement an import from this documentation alone.

5. **The API has quality issues suggesting low investment.** The API title says "Medi-EMR" (not "Medi-EHR"), the `USERNAME` parameter is duplicated in the patient data endpoint, and the response example shows `...CCDA Document...` instead of actual sample output. The API uses proprietary authentication rather than standard OAuth 2.0/SMART on FHIR.

### Summary Stats

```
Classification:  Standard-based projection
Export format:   C-CDA 2.1 XML (CSV and HTML mentioned but undocumented)
Model type:      Standard projection (C-CDA clinical document)
Entities:        19 C-CDA sections (no native database entities)
Fields:          N/A (no field-level documentation)
Descriptions:    N/A (0% — no field-level documentation exists)
Sample data:     No
Bulk export:     Claimed but undocumented
Domains covered: 7 of 15 applicable domains (clinical only)
```

### Bottom Line

A patient or provider requesting their complete health information from Medi-EHR would receive a C-CDA clinical summary — essentially the same document used for care transitions. This covers core clinical data but omits billing records, insurance information, clinical notes, consent forms, patient portal messages, and all specialty-specific data (behavioral health, surgical, residential treatment, workers' comp). Given that Medi-EHR is a full-featured EHR with integrated billing and multiple specialty modules, the documented export covers perhaps 30-40% of the patient data the system stores. The single biggest gap is the complete absence of billing and specialty clinical data from the export.
