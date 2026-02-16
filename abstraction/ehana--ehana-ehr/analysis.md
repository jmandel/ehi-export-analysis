# EHI Export Analysis: eHana

**Product**: eHana EHR  
**Analysis date**: 2025-07-18  
**CHPL IDs**: 15.04.04.2594.eHan.19.00.1.191206

## 1. Product Context

eHana EHR is a cloud-based behavioral health EHR purpose-built for behavioral health and human service organizations, with deep penetration in the Massachusetts market (10,000+ monthly active users, 900+ sites, 150,000+ clients). The product serves outpatient mental health, SUD/addiction, ESP/MCI (Emergency Services Program/Mobile Crisis Intervention), CBHI programs, I/DD, residential services, and justice-involved populations.

**Data domains the product stores** (per vendor website and product research):
- **Clinical documentation**: Service notes, clinical assessments, treatment plans, progress notes, CANS assessments, incident reports — 600,000+ documents/month
- **Demographics**: Multi-program client demographics, enrollment across programs
- **Medications**: E-prescribing with EPCS and PDMP integration
- **Billing/claims**: Automated claims (837/835), eligibility management, complex behavioral health billing rules, zero-paid and bundled claims for MassHealth
- **Scheduling**: Client and employee scheduling, front-desk check-in
- **Care coordination**: Cross-program notifications, secure messaging, DIRECT messaging, patient portal
- **Scanned documents**: OCR-processed documents filed into client charts
- **Specialty behavioral health**: CANS assessments, ESP/MCI workflows, CBHI/CSA/IHT/TM/ICC programs, I/DD-specific data

This breadth of data domains is the baseline against which export completeness must be measured.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/EHI_Export.pdf` (1.5 MB, 15 pages) | **Primary artifact.** Image-based PDF documenting the C-CDA XML export format. Contains 18 sections, each with an overview, UI screenshot, and XML element example. Created 2023-05-10 by "maralee.mies" via Microsoft Print to PDF from a Google Doc. | **Most informative** — sole source for export content |
| `downloads/SmartOnFHIR-API-Doc.pdf` (703 KB, 68 pages) | SMART on FHIR API documentation for §170.315(g)(10). Separate from (b)(10) EHI export. Documents OAuth2/SMART App Launch and FHIR R4 resource access. | Context only — not (b)(10) |
| `downloads/fhir-base-urls.csv` (282 bytes, 4 rows) | Lists FHIR server and auth server endpoints (test/prod). Production URLs listed as "available upon request." | Minimal — (g)(10) infrastructure only |
| `downloads/screenshot-certification-page.png` (517 KB) | Screenshot of ehana.com/certification-documentation page showing EHI Export link. | Minimal — confirms page layout |

**Key observation:** The entire (b)(10) EHI export documentation consists of a single 15-page PDF. There is no data dictionary, no machine-readable schema, no sample export file, and no supplemental documentation.

## 3. Export Mechanics

- **Format**: CDA R2 / C-CDA (Consolidated Clinical Document Architecture) XML
- **Mechanism**: Not explicitly described in the documentation. The PDF describes what data elements are included but does not document the user interface, API endpoint, or workflow for initiating an export. The certification documentation page refers to "export" in general terms.
- **Single-patient vs bulk**: Not documented. C-CDA is inherently a single-patient document format. No evidence of bulk/population-level export capability.
- **Access constraints**: Not documented. Production FHIR endpoints are "available upon request" (per `fhir-base-urls.csv`), but this pertains to (g)(10), not (b)(10).
- **Fees**: Not documented in the artifacts.

## 4. Export Content: What's In It

The export is a standard C-CDA clinical summary document containing 18 sections. The documentation (EHI_Export.pdf) presents each section with:
1. A brief **overview** sentence describing what the section stores
2. An **HTML Element** — a UI screenshot showing how the data appears in eHana's interface
3. An **XML Element** — a C-CDA XML code snippet showing the element structure with sample data

There is **no formal data dictionary**. The documentation does not provide field-level definitions, data types, cardinality, optionality, or value set bindings beyond what is visible in the XML snippets. The XML examples use standard C-CDA template OIDs and code systems (SNOMED-CT, LOINC, RxNorm, CDC Race/Ethnicity, CVX, NDC) but these are properties of the C-CDA standard, not vendor-specific documentation.

### Vendor's own content organization

The PDF organizes content as 18 C-CDA sections listed in a table of contents on page 1. The sections and their visible fields (extracted from visual inspection of all 15 rendered pages):

| Section | Fields Visible | Code Systems | Pages |
|---|---|---|---|
| Electronic Chart / Patient Data | 8 | AdministrativeGender, CDC Race/Ethnicity | 2–3 |
| Vital Signs | 4 | LOINC | 4 |
| Immunization | 4 | CVX | 5 |
| Allergies, Adverse Reactions, Alerts | 5 | RxNorm, SNOMED-CT | 5–6 |
| History of Medication Use | 5 | RxNorm, NDC | 6–7 |
| Instructions | 3 | — | 7–8 |
| Functional and Cognitive Status | 4 | SNOMED-CT | 8 |
| Chief Complaint / Reason For Visit | 2 | — | 9 |
| Problem List | 4 | SNOMED-CT, ICD-10-CM | 9–10 |
| Social History | 2 | SNOMED-CT, AdministrativeSex | 10 |
| Encounters | 4 | CPT | 11 |
| Results | 5 | LOINC | 12 |
| Procedures | 4 | SNOMED-CT | 13 |
| Reason for Referral | 2 | — | 13–14 |
| Implantable Devices | 4 | — | 14 |
| Health Concerns | 3 | — | 14–15 |
| Assessment and Plan | 1 | — | 15 |
| Goals | 3 | — | 15 |

**Totals**: 18 sections, 67 fields visible across all sections. All 67 fields have brief descriptions and data type indicators (as CDA data types like CE, TS, PQ). 18 fields reference specific code systems. Only 11 fields show explicit sample values in the screenshots.

The complete field-level inventory is in `analysis/full-entity-inventory.json`.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The export covers exactly what a standard C-CDA clinical summary covers — the 18 sections are standard C-CDA sections found in any certified EHR's clinical summary document. There is no evidence of vendor-specific extensions, custom sections, or additional data beyond what the C-CDA standard defines. The sections cover:

- **Demographics** (1 section, 8 fields): Name, DOB, sex, race, ethnicity, language, address, phone
- **Clinical observations** (4 sections, 17 fields): Vital signs, immunizations, allergies, problem list
- **Medications** (1 section, 5 fields): Prescribed/concurrent medications
- **Encounters** (2 sections, 6 fields): Visit records, chief complaint
- **Lab/diagnostics** (1 section, 5 fields): Lab results
- **Care planning** (3 sections, 7 fields): Health concerns, assessment & plan, goals
- **Procedures** (1 section, 4 fields)
- **Devices** (1 section, 4 fields): Implantable devices with UDI
- **Social/behavioral** (1 section, 2 fields): Smoking status, birth sex only
- **Care coordination** (1 section, 2 fields): Reason for referral
- **Other** (2 sections, 7 fields): Instructions, functional/cognitive status

This is a **clinical summary**, not a comprehensive data export. The thinnest sections are Assessment and Plan (1 free-text field) and Chief Complaint (2 fields). Social History is limited to smoking status and birth sex — extremely thin for a behavioral health EHR.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | "Electronic Chart / Patient Data" (8 fields): name, DOB, sex, race, ethnicity, language, address, phone | Basic demographics present. Missing: insurance/enrollment info, emergency contacts, multi-program enrollment data that eHana stores |
| Encounters / visits | ⚠️ Partial | "Encounters" section (4 fields) with CPT codes | Basic encounter records. Missing: service documentation with date/time, service type, location, program code, modifiers — the core of behavioral health service notes |
| Problems / conditions / diagnoses | ✅ Covered | "Problem List" (4 fields) with SNOMED-CT and ICD-10-CM | Standard problem list coverage |
| Medications / prescriptions | ⚠️ Partial | "History of Medication Use" (5 fields) with RxNorm/NDC | Medication list present, but eHana has full e-prescribing with EPCS/PDMP — prescribing workflow data, refill history, PDMP queries likely not captured in C-CDA |
| Allergies | ✅ Covered | "Allergies, Adverse Reactions, Alerts" (5 fields) with RxNorm, SNOMED-CT | Standard allergy documentation |
| Immunizations | ✅ Covered | "Immunization" (4 fields) with CVX codes | Standard immunization records |
| Vitals | ✅ Covered | "Vital Signs" (4 fields) with LOINC | Standard vital signs |
| Lab results | ✅ Covered | "Results" (5 fields) with LOINC | Standard lab results |
| Procedures | ✅ Covered | "Procedures" (4 fields) with SNOMED-CT | Standard procedure records |
| Clinical notes / documents | ❌ Not covered | "Assessment and Plan" has 1 free-text field; "Instructions" has 3 fields | **Major gap.** eHana generates 600,000+ clinical documents/month — service notes, progress notes, clinical assessments, treatment plans, CANS assessments, incident reports. None of these appear as structured or unstructured data in the C-CDA export. |
| Care plans / goals | ⚠️ Partial | "Goals" (3 fields), "Health Concerns" (3 fields), "Assessment and Plan" (1 field) | Free-text only. No structured treatment plan data. |
| Orders / referrals | ⚠️ Partial | "Reason for Referral" (2 fields) | Referral reason text only. No order data. |
| Insurance / coverage | ❌ Not covered | No insurance/enrollment entities in export | **Significant gap.** eHana manages eligibility verification and insurance information. Not in export. |
| Claims / billing | ❌ Not covered | No billing entities in export | **Critical gap.** eHana has comprehensive billing (837/835 processing, claims generation, billing dashboards). None exported. |
| Payments | ❌ Not covered | No payment entities in export | Product processes 835 remittance — payment data not exported. |
| Consents / directives | ❌ Not covered | No consent entities in export | Not in C-CDA export. |
| Patient communications / portal messages | ❌ Not covered | No messaging entities in export | eHana has a patient portal with secure messaging. Not exported. |
| Specialty-specific (behavioral health) | ❌ Not covered | Social History limited to smoking/birth sex | **Critical gap.** eHana's core value is behavioral health: CANS assessments, ESP/MCI workflows, CBHI programs, I/DD data, service notes, program enrollment, incident reports. None of this is in the C-CDA export. |
| Imaging / diagnostic reports | N/A | Not in export | eHana is behavioral health-focused; imaging is not a core capability. |
| Scanned documents | ❌ Not covered | No document attachment entities | eHana stores OCR-scanned documents in client charts. Not exported. |

**Summary**: 6 of 18 applicable domains are adequately covered (all standard clinical data). 5 domains are partially covered. 7 domains with data the product stores are not covered at all — including the three most critical for a behavioral health EHR: clinical notes/service documentation, billing/claims, and specialty behavioral health data.

## 6. Documentation Quality

The documentation is **minimal and not independently usable**:

- **No data dictionary**: No formal field definitions, cardinality, optionality, or value set bindings. The XML snippets implicitly reference standard C-CDA template OIDs and code systems, but these are properties of the standard, not vendor documentation.
- **No machine-readable schema**: No JSON schema, XSD, or other parseable artifact. The documentation is an image-based PDF that cannot even be text-searched.
- **No sample export file**: Only XML fragments shown in screenshots. No complete C-CDA document is provided. A developer cannot validate their parser against actual output.
- **No export workflow documentation**: The PDF does not explain how to initiate an export, whether it's per-patient or bulk, or how the output is delivered.
- **Image-based PDF**: The entire document is scanned/printed images — `pdftotext` returns empty output. The PDF was created by printing a Google Doc to "Microsoft: Print To PDF" (per PDF metadata: Creator "maralee.mies", Producer "Microsoft: Print To PDF", CreationDate 2023-05-10). This makes the documentation non-searchable, non-accessible, and difficult to process.

A developer could not build an import system from this documentation alone. They would need to refer to the C-CDA Implementation Guide independently and hope eHana's output conforms to it without extensions.

## 7. Overall Assessment

### Classification

**Standard-based projection.** The (b)(10) EHI export is a C-CDA clinical summary document containing 18 standard sections. It is not an export of eHana's native data model. It covers standard clinical summary data but omits the majority of what the product stores — billing, service documentation, behavioral health assessments, program enrollment, scanned documents, and messaging.

### Key Findings

1. **C-CDA repackaging as (b)(10)**: The export is a standard C-CDA clinical summary with 18 sections and 67 visible fields. This is the same format used for transitions of care and patient access — it is not a purpose-built EHI export. No vendor extensions or custom sections are present.

2. **Critical behavioral health data missing**: eHana's core value — behavioral health service documentation (600,000+ docs/month), CANS assessments, ESP/MCI workflows, program enrollment, and specialty clinical data — is entirely absent from the export. The Social History section contains only smoking status and birth sex, which is essentially meaningless for a behavioral health EHR.

3. **Billing/claims data missing**: Despite comprehensive billing capabilities (837/835 processing, claims generation, eligibility management), no billing or financial data appears in the export.

4. **Documentation is an image-based PDF**: The sole documentation artifact is a 15-page scanned PDF that cannot be text-searched. It provides no data dictionary, no sample export file, no machine-readable schema, and no export workflow instructions.

5. **Single artifact**: The entire (b)(10) export documentation consists of one PDF. There are no supplementary schemas, sample files, or detailed specifications.

### Summary Stats

```
Classification:  Standard-based projection
Export format:   C-CDA (CDA R2) XML
Model type:      Standard projection (C-CDA clinical summary)
Entities:        18 (C-CDA sections)
Fields:          67 (visible in documentation)
Descriptions:    100% (brief descriptions per field, but no formal data dictionary)
Sample data:     No (XML fragments in screenshots only, no complete sample file)
Bulk export:     Unclear (not documented)
Domains covered: 6 of 17 applicable domains fully covered
```

### Bottom Line

eHana's (b)(10) export is a standard C-CDA clinical summary being labeled as an EHI export. It covers basic clinical data (demographics, meds, allergies, vitals, labs, problems) but omits the behavioral health service documentation, assessments, billing/claims, and specialty program data that constitute the core of what eHana stores about patients. For a behavioral health EHR that generates 600,000+ clinical documents per month and manages complex MassHealth billing, exporting only an 18-section C-CDA clinical summary represents a small fraction of the designated record set. The single biggest gap is the complete absence of behavioral health clinical documentation — the very data that makes eHana a behavioral health EHR.
