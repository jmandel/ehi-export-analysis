# EHI Export Analysis: Benchmark Systems

**Product**: Benchmark EHR  
**Analysis date**: 2026-02-16  
**CHPL ID**: 15.04.04.1144.AntW.71.01.1.171219 (CHPL #9098)

## 1. Product Context

Benchmark EHR (now Benchmark Solutions, a division of Harris Healthcare) is a cloud-based, ONC-certified ambulatory EHR serving independent and small practices across 27+ medical specialties. The certified product is part of an integrated suite that includes:

- **Benchmark EHR**: Clinical documentation, e-prescribing, lab management, patient portal, immunization registry reporting, clinical quality measures, FHIR API access
- **Benchmark PM** (Practice Management): Scheduling, demographics, insurance verification, billing/claims, CPT/ICD-10 coding, payment processing, A/R management
- **Benchmark RCM** (Revenue Cycle Management): Charge entry, claims submission, denial management, payment posting, collections

For (b)(10) completeness, the export should cover clinical data (encounters, diagnoses, medications, labs, vitals, allergies, immunizations, procedures, notes, documents), patient demographics and insurance, billing/claims data, and specialty-specific clinical content across the 27+ specialties served.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `b-10-EHI-Export_Benchmark-Support_Self-Attestation-Document_final-1.pdf` | 28-page PDF (539 KB), created 2023-12-01 in Microsoft Word by Neha Parmar. Contains export workflow, data format specs, and field-level documentation for 47 data element types. | **Primary source** — all substantive analysis derives from this document. |
| `enrichment/benchmark-ehr-export-schema.json` | Pre-extracted JSON containing all 47 entities and 1,146 field names parsed from the PDF by a Bun TypeScript script. | **Very useful** — machine-readable extraction independently validated against my own parse (matched on 47 entities; 8-field discrepancy in 3 entities due to PDF line-break artifacts). |
| `enrichment/extract-export-schema.ts` | The extraction script source. | Useful for understanding parse methodology. |
| `enrichment/README.md` | Documents extraction process and known limitations. | Minor. |

**Note on URL accessibility**: The prior report states the live URL returns HTTP 403 and the PDF was recovered via Wayback Machine. My independent check on 2026-02-16 shows the live URL (`https://www.benchmarksystems.com/wp-content/uploads/2023/12/b-10-EHI-Export_Benchmark-Support_Self-Attestation-Document_final-1.pdf`) now returns HTTP 200 with the correct 539,084-byte PDF. The site is currently accessible.

## 3. Export Mechanics

- **Format**: ZIP file containing XLS (Excel) files for structured/tabular data, TXT files for text data, PDF files for documents and attachments, and HTML/XML files for CCD documents.
- **Mechanism**: 
  - **Single patient**: Self-service via EHR UI. Users with the `CuresEHIExport` role can select a patient, choose data element types via checkboxes, and trigger an asynchronous background export. The ZIP is downloadable under Settings → Configuration → Download Files → "Cures EHI Export" category. No password or developer assistance required.
  - **Patient population**: Not self-service. Requires contacting the "Bizmatics Data Migration Team" at `support@bizmaticsinc.com`. Described as resource-intensive and vendor-managed.
- **Single-patient vs bulk**: Single-patient is self-service; bulk requires vendor assistance.
- **Access constraints**: Single-patient export requires the `CuresEHIExport` user role. Population export depends on vendor scheduling and resources.
- **Fees**: Not mentioned in the documentation.

## 4. Export Content: What's In It

The export covers **47 data element types** documented in the PDF. Of these, **36 entities have explicit database column-level field lists** totaling **1,146 named fields**. The remaining 11 entities are document-type exports (PDFs, HTML/XML) or have only prose descriptions.

The field lists consist solely of database column names (e.g., `PT_FNAME`, `BLH_CLAIM_STATUS`, `LOD_TEST_LOINC`). **No per-field descriptions, data types, nullability, value sets, or foreign key relationships are documented.** The column naming convention follows a `PREFIX_FIELDNAME` pattern that is largely self-explanatory.

5 of the 47 entities are billing-only ("when Billing is turned on for the clinic"): Billing Ledger, Billing Claims, Billing Charges, Patient Advance, and Statements.

### Vendor's own content organization

The vendor lists all 47 data element types as a flat numbered list (1–47) without explicit categories. I've organized them below using logical groupings based on the entity names and descriptions. Field counts are from the enrichment JSON (validated against independent parse).

**Patient Demographics & Administration** (5 entities, 231 fields):

| Entity | Fields | Attachments | Notes |
|---|---|---|---|
| Patient Demographics | 131 | No | Active patients only; includes race, ethnicity, language, sexual orientation, gender identity, 5 PCP slots |
| Patient Insurance | 59 | No | Primary/secondary/tertiary insurance details |
| Patient Cases | 41 | No | Workers' comp, injury cases with dates, attorneys, adjusters |
| Patient Notes | 0 | No | Prose description only: "All Patient Notes saved for a Patient" |
| Patient Alert | 0 | No | Prose description only: "All Patient Alerts except deleted" |

**Clinical History** (7 entities, 71 fields):

| Entity | Fields | Notes |
|---|---|---|
| Vaccination | 18 | CVX codes, manufacturer, lot, route, site |
| Allergy | 13 | RxNorm, NDC, adverse event, SNOMED reaction codes |
| Social History | 11 | SNOMED and LOINC codes |
| Past Medical Hist | 9 | ICD-10 and SNOMED codes |
| Health Maintenance | 7 | — |
| Family History | 7 | SNOMED codes |
| Surgery | 6 | — |

**Encounter Clinical Data** (5 entities, 42 fields):

| Entity | Fields | Notes |
|---|---|---|
| Vitals | 11 | SNOMED and LOINC codes; per-encounter |
| Diagnosis Code | 11 | ICD-10 codes with assessment and plan notes |
| CPT Codes | 10 | SNOMED codes, IMO descriptions |
| HCPC Codes | 10 | — |
| All Vitals | 0 | "Vitals for all Encounters" — same fields as Vitals (#24) |

**Medications** (2 entities, 38 fields):

| Entity | Fields | Notes |
|---|---|---|
| Prescriptions | 20 | All drugs ever prescribed; includes Rx status, sent mode, sent date |
| Current Medication | 18 | Latest encounter status; NDC, RxNorm codes |

**Results** (3 entities, 82 fields):

| Entity | Fields | Notes |
|---|---|---|
| Lab Test Result Values | 38 | Discrete results with LOINC codes, panel info, ranges |
| Lab Results | 23 | Order-level lab results |
| Rad Results | 21 | Radiology results |

**Clinical Notes** (3 entities, 66 fields):

| Entity | Fields | Notes |
|---|---|---|
| Enc Progress Notes | 63 | Closed encounters only; includes attending/referring/rendering/supervisor provider details; PDF attachments |
| Procedure Notes | 3 | PDF attachments; requires print template assignment |
| CCD | 0 | HTML/XML files; Consolidated Clinical Document |

**Orders & Referrals** (2 entities, 63 fields):

| Entity | Fields | Notes |
|---|---|---|
| Procedure Orders | 33 | — |
| Consults | 30 | — |

**Documents & Correspondence** (6 entities, 20 fields):

| Entity | Fields | Notes |
|---|---|---|
| Letters | 15 | Inward/outward; PDF attachments |
| Messages | 5 | Patient messages |
| Legal Documents | 0 | PDF attachments |
| Other Documents | 0 | PDF attachments |
| Enc Attach Docs | 0 | PDF attachments |
| Old Progress Notes | 0 | PDF attachments (DocType: OPA) |

**Reference/Administrative** (7 entities, 176 fields):

| Entity | Fields | Notes |
|---|---|---|
| Adjusters | 33 | — |
| Medics | 31 | Active providers/staff; includes NPI, taxonomy, specialty |
| Referring Doctor | 28 | Provider reference data |
| Employers | 25 | — |
| Guarantor | 22 | — |
| Insurance Master | 21 | Insurance company reference data |
| Attorneys | 16 | — |

**Scheduling** (2 entities, 18 fields):

| Entity | Fields | Notes |
|---|---|---|
| Future Appointments | 18 | — |
| Past Appointments | 0 | Prose description: "Visit Status Scheduled, Tentative, Arrived, etc." |

**Billing** (5 entities, 339 fields — requires billing module):

| Entity | Fields | Notes |
|---|---|---|
| Billing Claims | 185 | CMS 1500 claim data; void claims excluded; UB04 excluded |
| Billing Charges | 124 | Line-level charge detail |
| Patient Advance | 30 | Advance payments |
| Billing Ledger | 0 | Prose: "Ledger for Run Date, billed claims only" |
| Statements | 0 | Latest statement only; PDF attachment |

The full machine-readable inventory is at `analysis/full-entity-inventory.json`.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The export is organized as 47 named data element types that collectively span clinical, administrative, billing, and document data. The strongest areas are:

- **Patient demographics** (131 fields) — extremely detailed, including race, ethnicity, language, sexual orientation, gender identity, 5 PCP slots, emergency contacts, employer, spouse, and multiple boolean flags
- **Billing claims** (185 fields) — deep CMS 1500-level claim data with insurance, provider, tracking, and EDI fields
- **Billing charges** (124 fields) — line-level charge detail
- **Encounter progress notes** (63 fields) — rich provider attribution (attending, referring, rendering, supervisor, reviewer — each with NPI, FTIN, taxonomy, specialty)
- **Patient insurance** (59 fields) — primary/secondary/tertiary coverage detail

The thinnest areas among entities with field lists are Surgery (6 fields), Health Maintenance (7 fields), Family History (7 fields), and Procedure Notes (3 fields). Additionally, 11 entities have no explicit field lists — mostly document-type exports delivered as PDFs.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | `Patient Demographics` (131 fields), `Guarantor` (22 fields) | Thorough — includes race, ethnicity, language, sexual orientation, gender identity |
| Encounters / visits | ✅ Covered | `Enc Progress Notes` (63 fields), `Past Appointments`, `Future Appointments` | Encounter data embedded in progress notes; closed encounters only for notes |
| Problems / conditions / diagnoses | ✅ Covered | `Diagnosis Code` (11 fields, ICD-10), `Past Medical Hist` (9 fields) | Adequate |
| Medications / prescriptions | ✅ Covered | `Current Medication` (18 fields), `Prescriptions` (20 fields) | Both current and historical; includes NDC, RxNorm |
| Allergies | ✅ Covered | `Allergy` (13 fields) | Includes RxNorm, NDC, SNOMED reaction codes |
| Immunizations | ✅ Covered | `Vaccination` (18 fields) | CVX codes, manufacturer, lot, route, site |
| Vitals | ✅ Covered | `Vitals` (11 fields), `All Vitals` | Per-encounter and all-encounters; SNOMED/LOINC |
| Lab results | ✅ Covered | `Lab Results` (23 fields), `Lab Test Result Values` (38 fields) | Both order-level and discrete values with LOINC |
| Imaging / diagnostic reports | ✅ Covered | `Rad Results` (21 fields) | Radiology results exported |
| Procedures | ✅ Covered | `Surgery` (6 fields), `CPT Codes` (10 fields), `HCPC Codes` (10 fields), `Procedure Orders` (33 fields), `Procedure Notes` (3 fields + PDF) | Covered across multiple entities |
| Clinical notes / documents | ✅ Covered | `Enc Progress Notes` (63 fields + PDF), `Procedure Notes` (3 fields + PDF), `Old Progress Notes` (PDF), `CCD` (HTML/XML) | Closed encounters only; rendered as PDFs; only default "My Note" per encounter |
| Care plans / goals | ⚠️ Partial | No dedicated entity; may be embedded in `Enc Progress Notes` or `CCD` | No explicit care plan entity; possible gap if product stores structured care plans |
| Orders / referrals | ✅ Covered | `Procedure Orders` (33 fields), `Consults` (30 fields) | Solid |
| Insurance / coverage | ✅ Covered | `Patient Insurance` (59 fields), `Insurance Master` (21 fields) | Detailed |
| Claims / billing | ✅ Covered | `Billing Claims` (185 fields), `Billing Charges` (124 fields), `Billing Ledger`, `Patient Advance` (30 fields), `Statements` (PDF) | Deep; requires billing module enabled; UB04 forms excluded |
| Payments | ✅ Covered | `Patient Advance` (30 fields), billing ledger | Advance payments explicitly covered |
| Consents / directives | ⚠️ Partial | `Legal Documents` (PDF exports) | Legal documents exported as PDFs but no structured consent data |
| Patient communications / portal messages | ✅ Covered | `Messages` (5 fields), `Letters` (15 fields + PDF) | Both messages and inward/outward letters |
| Specialty-specific data | ⚠️ Partial | Product supports 40+ specialty templates; export captures rendered notes as PDFs, not structured template field data | Template-based data exported only as rendered PDFs, not as structured fields |

**Domains not applicable to this product**: N/A — the product appears to cover all standard ambulatory domains.

**Key gaps**:
1. **Specialty-specific structured data**: The product supports 40+ specialty templates, but the export captures rendered progress notes as PDFs rather than the underlying structured template field data. A dermatology-specific assessment form, for example, would be exported as a PDF image rather than discrete fields.
2. **Care plans**: No dedicated entity for structured care plan data.
3. **UB04 billing**: Explicitly excluded from the billing export.
4. **Patient education materials**: The product distributes MedlinePlus materials; no evidence these are exported.
5. **Patient intake forms**: Portal feature; no explicit export of structured intake form data.

## 6. Documentation Quality

**Strengths**:
- 1,146 named database column fields across 36 entities — unusually detailed for (b)(10) documentation
- 47 data element types covering clinical, administrative, and billing domains
- Clear export workflow instructions with role-based access (CuresEHIExport role)
- Consistent entity documentation format (description + field list)
- Honest about exclusions (void claims, UB04, inactive patients, deleted encounters optional)

**Weaknesses**:
- **No per-field descriptions**: Fields are listed by name only. No explanation of what each field means beyond what the column name implies.
- **No data types**: No indication of whether fields are strings, dates, integers, booleans, or their lengths/constraints.
- **No value sets**: Fields like `PT_MARITAL_STATUS`, `BLH_CLAIM_STATUS`, `ENC_TYPE` use coded values that are never defined.
- **No relationship documentation**: No foreign keys, entity-relationship diagrams, or join instructions. Relationships must be inferred from shared ID patterns (e.g., `PT_ID`, `ENC_ID`).
- **No sample data**: No example export files or records.
- **Boolean fields unexplained**: Many `BOOL_*` fields (e.g., `PT_BOOL_SELFPAY`, `BLH_BOOL_WORK_COMP`) with no documentation of what true/false means.
- **Population export not self-service**: Bulk export requires contacting the Bizmatics Data Migration Team, creating a vendor dependency.
- **Internal comments visible**: The PDF contains a Word comment annotation on entity #44 noting "Same fields (BLH_TOS_CODE) with two different name... Need to discuss." — suggesting the documentation was not fully finalized.

**Developer usability**: A developer could identify *which* data elements are in an export and *what columns* they contain, but could not fully parse or import the data without significant reverse-engineering of data types, value sets, and inter-entity relationships. The column naming convention (`PT_DOB` = patient date of birth, `BLH_BILL_AMOUNT` = billing amount) makes many fields self-explanatory, but coded fields, boolean flags, and status codes would require experimentation or vendor support.

## 7. Overall Assessment

### Classification

**Comprehensive native export**

This is a genuine native data model export — not a C-CDA or FHIR repackaging. The 47 data element types with 1,146 database column-level fields represent a direct view of the underlying database schema. The export covers clinical, administrative, billing, and document data across the full scope of what the product stores. Documentation quality is moderate (field names but no types/descriptions/value sets), but the breadth and depth of coverage is above average.

### Key Findings

1. **Genuine (b)(10) effort**: 47 data element types with 1,146 named database fields across clinical, administrative, and billing domains. This is a proper designated record set export, not a repackaged FHIR/C-CDA. (Source: PDF pages 8–28)

2. **Deep billing coverage**: When the billing module is enabled, the export includes 339 fields across 5 billing entities — notably Billing Claims (185 fields) and Billing Charges (124 fields). This level of billing detail is uncommon. (Source: PDF pages 24–28)

3. **Documentation lacks per-field metadata**: Despite listing 1,146 field names, the documentation provides zero per-field descriptions, zero data type specifications, and zero value set definitions. A developer would need to reverse-engineer meaning from column names alone. (Source: entire PDF — field lists contain only comma-separated column names)

4. **Population export requires vendor contact**: Bulk/population export is not self-service and requires contacting the "Bizmatics Data Migration Team." This creates a vendor dependency for the (b)(10)(ii) requirement. (Source: PDF page 5)

5. **Specialty template data exported as PDFs only**: The product supports 40+ specialty clinical templates, but the export renders these as PDF documents rather than preserving the structured template field data. This means specialty-specific clinical data (structured assessments, specialty forms) loses its computable format in the export. (Source: PDF pages 20–21, entity #34 Enc Progress Notes)

### Summary Stats

```
Classification:  Comprehensive native export
Export format:   XLS, TXT, PDF, HTML/XML (in ZIP)
Model type:      Native database
Entities:        47
Fields:          1,146
Descriptions:    0% (field names only, no per-field descriptions)
Sample data:     No
Bulk export:     Vendor-assisted only (not self-service)
Domains covered: 15 of 17 applicable domains (care plans and specialty structured data are partial)
```

### Bottom Line

Benchmark EHR provides one of the more thorough (b)(10) exports: a genuine native database dump covering 47 data element types with 1,146 fields spanning clinical, administrative, and billing data. The biggest weakness is documentation quality — 1,146 field names with zero descriptions, types, or value sets means a receiving system would need significant reverse-engineering. The single biggest gap is that specialty-specific clinical template data (the product's key selling point across 27+ specialties) is exported only as rendered PDFs rather than as structured, computable data.
