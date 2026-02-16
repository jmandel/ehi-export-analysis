# EHI Export Analysis: The Echo Group (Ensora Health)

**Product**: EchoVantage  
**Analysis date**: 2026-02-16  
**CHPL IDs**: 11129 (15.04.04.2425.Echo.13.02.1.221227)

## 1. Product Context

EchoVantage is a **web-based, integrated EHR, billing, and practice management platform** purpose-built for **community behavioral health organizations** — mental health clinics, substance use recovery centers, I/DD services, crisis intervention, foster/residential care, and correctional health facilities. Originally developed by The Echo Group (founded ~1980), the product is now part of Ensora Health (formerly Therapy Brands, acquired 2022).

Key capabilities relevant to EHI export completeness:

- **Clinical documentation**: Visual Health Record (VHR) timeline, progress notes, treatment plans, assessments (standardized and custom), client intake, forms designer for custom clinical forms
- **e-Prescribing**: Via DrFirst integration — medication histories, prescriptions, interaction checking
- **Billing & RCM**: Claims submission (Apex Clearinghouse), eligibility verification, payment posting, remittance processing, charge creation
- **Scheduling**: Appointment management with reminders
- **Telehealth**: HIPAA-compliant video sessions
- **Reporting**: 30+ dashboard presets, productivity metrics, financial reporting
- **State reporting**: State-specific mandatory behavioral health reporting
- **AI integration**: Eleos Health voice-to-note technology

The product is certified for (b)(10) EHI export, (b)(1) transitions of care, (g)(7)/(g)(10) FHIR APIs, and multiple clinical criteria including (a)(3) CPOE demographics, (a)(5) demographics, (a)(12) family health history, (a)(14) implantable device list, and (a)(15) social/psychological/behavioral data. It does **not** hold CPOE drug/lab certifications, patient portal (e)(1), or public health reporting (f) criteria.

A genuine (b)(10) export for this product should cover: demographics, clinical notes, treatment plans, behavioral health assessments, diagnoses, medications, billing/claims, insurance, scheduling data, custom forms, documents, and state reporting data.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `Electronic-Health-Information-Export_EchoVantage.pdf` (1 page, 149 KB) | Single-page PDF listing export file formats. Created 2025-08-15 by Catherine Baker. Contains format names and generic descriptions — no data dictionary, no schema, no field-level detail. | **Low** — describes only format names, not content |
| `onc-echo-page.html` (82 KB) | Full HTML of the ONC certification page at ensorahealth.com/onc/echo/. Contains EHI Export section describing single-patient and population export modes. | **Low** — repeats PDF content with minor additional context about export mechanisms |
| `onc-echo-page-screenshot.png` (915 KB) | Full-page screenshot of the ONC page. | **Minimal** — visual confirmation only |

**Total artifacts: 3.** No data dictionary, no schema documentation, no sample data, no field-level documentation of any kind.

## 3. Export Mechanics

EchoVantage offers two export modes:

### Single Patient Export
- **Format**: CCD/C-CDA, JSON, or PDF
- **Mechanism**: User-initiated within the EHR, "without developer assistance"
- **Scope**: Explicitly described as containing "data required by the USCDI v1 standards" (per the PDF)
- **Access**: Self-service

### Patient Population Export
- **Format**: MSSQL Server `.bak` file (full database backup)
- **Mechanism**: Must submit a support ticket via Salesforce
- **Scope**: Described as "a full MSSQL Server database backup of all data for an agency that can be restored"
- **Access**: Vendor-assisted (support ticket required)
- **Caveats**: The web page notes content may vary based on software applications in use, software version, documentation practices, configuration decisions, and "materials not sourced from the application"

**Fees**: Not documented.  
**Turnaround time**: Not documented.

## 4. Export Content: What's In It

### The core problem: no documentation of content

There is **zero field-level, entity-level, or schema-level documentation** for either export mode. The entirety of the technical documentation is:

1. A 1-page PDF that names four file formats (CCD/C-CDA, JSON, PDF, .bak) with generic descriptions of what those formats are (not what data they contain)
2. A web page section that describes the two export modes and their access mechanisms

For the **single patient export**, the PDF explicitly scopes it to "USCDI v1 standards" — this is a C-CDA clinical summary, not a comprehensive EHI export. USCDI v1 covers demographics, problems, medications, allergies, labs, vitals, immunizations, procedures, clinical notes, goals, assessments, and health concerns. It does **not** cover billing, claims, custom assessments, treatment plan details, behavioral health-specific data, or most of what makes EchoVantage a behavioral health EHR.

For the **patient population export**, the `.bak` file is described as a "full MSSQL Server database backup." This could potentially contain everything in the database, making it theoretically comprehensive. However:
- There is no schema documentation — a recipient would receive a raw database backup with no understanding of the table structure, field meanings, relationships, or value sets
- There is no data dictionary explaining what tables exist, what they contain, or how they relate
- There is no sample data showing what the export looks like
- The export requires a support ticket, suggesting it is not a routine self-service operation

### Vendor's own content organization

The vendor provides no content organization because there is no content documentation. The only categorization is by format:

| Export Mode | Format | Documented Scope | Entities | Fields | Descriptions |
|---|---|---|---|---|---|
| Single Patient | CCD/C-CDA | USCDI v1 | 0 documented | 0 documented | None |
| Single Patient | JSON | Not specified | 0 documented | 0 documented | None |
| Single Patient | PDF | Not specified | 0 documented | 0 documented | None |
| Population | MSSQL .bak | "All data for an agency" | 0 documented | 0 documented | None |

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor's documentation provides almost no basis for assessing coverage:

- **Single patient export**: Explicitly scoped to USCDI v1, which is the minimum clinical exchange standard. This is the vendor's existing C-CDA/clinical summary capability relabeled as EHI export.
- **Population export**: A raw database backup that could contain everything but is completely undocumented. Without a schema or data dictionary, it is impossible to verify what is actually included.

The vendor does not organize their export documentation into clinical, billing, administrative, or any other categories. There are no categories because there is no content documentation.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | Single-patient C-CDA covers USCDI v1 demographics; .bak likely contains full demographics but undocumented | Product stores rich demographics (intake data, contacts); C-CDA covers only USCDI subset |
| Encounters / visits | ⚠️ Partial | C-CDA may include encounter data per USCDI v1; .bak undocumented | Product stores detailed encounter/visit data; no documentation of coverage |
| Problems / conditions / diagnoses | ⚠️ Partial | C-CDA covers problems per USCDI v1; .bak undocumented | Product stores diagnoses for clinical and billing purposes |
| Medications / prescriptions | ⚠️ Partial | C-CDA covers medications per USCDI v1; .bak undocumented | Product has DrFirst e-prescribing integration with full medication histories |
| Allergies | ⚠️ Partial | C-CDA covers allergies per USCDI v1; .bak undocumented | Likely adequate for USCDI but unknown beyond that |
| Immunizations | ⚠️ Partial | C-CDA covers immunizations per USCDI v1; .bak undocumented | May be limited for behavioral health focus |
| Vitals | ⚠️ Partial | C-CDA covers vitals per USCDI v1; .bak undocumented | Standard USCDI coverage |
| Lab results | ⚠️ Partial | C-CDA covers labs per USCDI v1; .bak undocumented | Product has lab integration but depth unclear |
| Imaging / diagnostic reports | N/A | Not applicable | Behavioral health EHR — no imaging capability |
| Procedures | ⚠️ Partial | C-CDA covers procedures per USCDI v1; .bak undocumented | Standard coverage |
| Clinical notes / documents | ⚠️ Partial | C-CDA covers clinical notes per USCDI v1; .bak undocumented | Product stores progress notes, treatment plans, custom forms — C-CDA likely misses behavioral health-specific documentation |
| Care plans / goals | ⚠️ Partial | C-CDA may include goals per USCDI v1; .bak undocumented | Product has structured treatment plans with outcome linkage — a core feature likely not fully captured in C-CDA |
| Orders / referrals | ❌ Not covered | No evidence in single-patient export; .bak undocumented | Product likely handles referrals given behavioral health workflow |
| Insurance / coverage | ❌ Not covered | Not in USCDI v1 C-CDA; .bak undocumented | Product stores insurance for eligibility and billing — significant gap in single-patient export |
| Claims / billing | ❌ Not covered | Not in USCDI v1 C-CDA; .bak undocumented | Product has full billing/RCM capabilities — major gap in single-patient export |
| Payments | ❌ Not covered | Not in USCDI v1 C-CDA; .bak undocumented | Product processes payments and remittances — gap in single-patient export |
| Consents / directives | ❌ Not covered | Not in USCDI v1 C-CDA; .bak undocumented | Behavioral health requires extensive consent management |
| Patient communications | ❌ Not covered | Not in USCDI v1 C-CDA; .bak undocumented | Unknown if product has messaging/portal |
| Specialty-specific (behavioral health) | ❌ Not covered | Not in USCDI v1 C-CDA; .bak undocumented | **Core gap**: Custom assessments, treatment plans with outcome linkage, behavioral health-specific documentation, substance use data, I/DD data — the product's differentiating features are not documented as part of the single-patient export |

**Summary**: The single-patient export is explicitly limited to USCDI v1, covering perhaps 20-30% of what the product stores. The population export (.bak) could theoretically cover everything, but with zero documentation, it's impossible to verify coverage or use the exported data meaningfully.

## 6. Documentation Quality

The documentation quality is **extremely poor**:

- **No data dictionary** — zero entities, zero fields, zero descriptions
- **No schema** — no table definitions, no relationships, no data types
- **No sample data** — no examples of what the export looks like
- **No machine-readable artifacts** — no JSON schema, no OpenAPI spec, no FHIR CapabilityStatement for the export
- **No field-level documentation** of any kind
- **No value sets or code systems** documented
- **No documentation of the JSON format** — the PDF describes JSON generically ("a lightweight format for storing and transporting data") but provides no information about the JSON structure, what data it contains, or how it differs from the C-CDA

A developer receiving this documentation could not build an import system. They would know only that single-patient exports come as C-CDA (USCDI v1 scoped), JSON (structure unknown), or PDF, and that population exports come as raw MSSQL backups (schema unknown). They would need to reverse-engineer the database schema from the .bak file or parse the C-CDA/JSON outputs to discover the data structure.

The 1-page PDF is essentially a format label sheet, not technical documentation.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Minimal/stub/unclear**

The single-patient export is explicitly scoped to USCDI v1 — the minimum clinical exchange standard — which covers a small fraction of what a behavioral health EHR stores. The vendor says so directly: the C-CDA "will contain data required by the USCDI v1 standards." For a product whose core value proposition is behavioral health treatment plans, custom assessments, and integrated billing, an export limited to USCDI v1 misses the majority of the designated record set.

The population export (.bak file) could potentially be comprehensive since it's described as "a full MSSQL Server database backup of all data for an agency." However, the complete absence of schema documentation makes it impossible to verify what's included or to use the exported data in any practical way. A raw database backup without documentation is not a usable EHI export — it requires MSSQL Server to restore and deep technical expertise to interpret. The vendor provides no help bridging that gap.

**Axis 2 — Export approach: Repackaged existing export** (single-patient); **Unclear** (population)

The single-patient export is clearly a repackaged existing capability. The C-CDA export scoped to USCDI v1 is the same clinical summary the vendor already produces for (b)(1) transitions of care and (g)(10) FHIR API compliance. There is no evidence of any purpose-built EHI export effort for single patients.

The population export (.bak database backup) is technically different — it's not a C-CDA or FHIR repackaging. But it's also not a purpose-built EHI export: it's a standard database administration operation (MSSQL backup) reframed as an export mechanism. There's no evidence the vendor built anything specific for (b)(10) — they appear to have pointed at their existing database backup capability and their existing C-CDA generation, labeled them as EHI export, and published a 1-page PDF.

### Key Findings

1. **No data dictionary exists.** The entire EHI export documentation is a 1-page PDF listing format names (CCD/C-CDA, JSON, PDF, .bak) with generic descriptions of what those formats are — not what data they contain. Zero entities, zero fields, zero descriptions documented.

2. **Single-patient export is explicitly USCDI v1 only.** The vendor's own documentation states the C-CDA export "will contain data required by the USCDI v1 standards." This is a clinical summary, not a comprehensive EHI export. It misses billing, behavioral health assessments, treatment plans, custom forms, insurance, and other core data the product stores.

3. **Population export requires vendor assistance and provides no schema.** The .bak database backup requires submitting a Salesforce support ticket, and the vendor provides no documentation of the database schema. A recipient would receive a raw MSSQL backup with no way to understand its contents without reverse-engineering.

4. **The JSON export format is completely undocumented.** The PDF describes JSON generically but provides no information about structure, content, or scope. It's impossible to assess what this format contains.

5. **Behavioral health-specific data — the product's core — is undocumented in the export.** EchoVantage's differentiating features (treatment plans with outcome linkage, custom assessments, behavioral health forms, substance use data, I/DD records) have no documented presence in the export. The USCDI v1 scoping of the single-patient export suggests these are excluded.

### Summary Stats

```
Coverage:        Minimal/stub/unclear
Approach:        Repackaged existing export (single-patient) / Unclear (population)
Export format:   CCD/C-CDA, JSON (undocumented), PDF, MSSQL .bak
Entities:        0 documented
Fields:          0 documented
Descriptions:    N/A (no fields documented)
Sample data:     No
Bulk export:     Yes (via support ticket, .bak file)
Domains covered: 0 of 15 applicable domains confirmed (all rated Partial or Not Covered due to no documentation)
```

### Bottom Line

EchoVantage's EHI export documentation is among the thinnest possible — a single-page PDF naming file formats with no data dictionary, schema, or field-level detail. The single-patient export is explicitly limited to USCDI v1 (a clinical summary, not comprehensive EHI), while the population export is an undocumented database backup requiring vendor assistance and MSSQL Server expertise to interpret. A patient or provider would receive either a clinical summary missing most of what the behavioral health EHR stores, or a raw database file they cannot meaningfully use without significant technical resources and reverse-engineering.
