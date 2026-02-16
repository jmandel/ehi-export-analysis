# EHI Export Analysis: Qualifacts Systems, LLC

**Product**: Insync EMR/PM (Version 10)  
**Analysis date**: 2026-02-16  
**CHPL ID**: 15.02.05.3124.INSY.01.03.1.220314

## 1. Product Context

InSync EMR/PM is a cloud-based, integrated electronic health record and practice management platform developed by Qualifacts Systems, LLC. It targets small to mid-size behavioral health, rehabilitative therapy, and medical practices. The "EMR/PM" name reflects its dual nature: clinical EHR functionality combined with practice management (scheduling, billing, revenue cycle) in one system.

**Key capabilities relevant to EHI completeness:**
- **Clinical documentation**: Progress notes, treatment plans, assessments (including ASAM criteria for addiction), dynamic custom forms, measurement-based care tracking
- **Behavioral health specialty**: Psychiatric history, substance abuse tracking, group therapy, behavioral data, case management
- **OB/GYN specialty**: Pregnancy tracking, newborn delivery, gynecological history, past pregnancy data
- **ePrescribing**: EPCS, eMAR, PDMP integration, drug interaction checks
- **Billing & revenue cycle**: Integrated billing engine, claims management, ICD coding, payment processing, financial summaries, prior authorizations
- **Patient portal**: Secure messaging, appointment requests, intake forms, payment, telehealth
- **Lab integration**: Lab orders and results (add-on)
- **Telehealth**: Integrated video (up to 50 participants)
- **Scheduling**: Multi-provider/room scheduling, reminders

The product stores clinical, financial, administrative, and specialty data. A genuine (b)(10) export should cover all of these domains.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/insync-ehi-export.html` (9.9 KB) | Sphinx-generated HTML page describing export workflows (single-patient and population), file format (NDJSON + attachments in ZIP), and linking to the data dictionary. | **High** — primary procedural documentation |
| `downloads/InSync_EHI_Export_Data_Dictionary.xls` (1.5 MB) | XLS workbook with 84 sheets: INDEX, Changelogs, Confidential Notice, and 81 data section sheets. Each sheet defines fields with column name, data type, nullability, and description. | **Very high** — the core artifact; complete data dictionary |
| `downloads/Qualifacts_EHI_Export_Terms_of_Use_SEP_2024.pdf` (149 KB) | 3-page PDF with legal terms governing EHI export usage, including HIPAA compliance requirements, disclaimers, and liability limitations. | **Low** — legal boilerplate, no technical content |
| `downloads/enrichment/data-dictionary.json` (241 KB) | Prior agent's JSON extraction of the XLS data dictionary (81 sections, 960 fields). Used for cross-validation of my independent parse. | **Reference** — validated against my own extraction |
| `downloads/enrichment/extraction-stats.json` (15 KB) | Prior agent's parse statistics (84 sheets, 81 parsed, 0 failures). | **Reference** — matches my results exactly |

## 3. Export Mechanics

- **Format**: NDJSON (Newline Delimited JSON) per patient, plus a "Supported File" folder for attachments (images, documents). Single-patient exports produce one ZIP with one NDJSON file + attachments; population exports produce one JSON per patient with a shared attachments folder.
- **Mechanism**:
  - **Single-patient**: Initiated by designated agency staff within the InSync UI upon patient/representative request. Completed export appears in the requester's To Do list with a download link.
  - **Population export**: Requested via Qualifacts Care Center support ticket. Qualifacts staff initiates the process. Up to 30 calendar days for completion. One population export at a time.
- **Access constraints**: Download links expire after 30 calendar days. Population exports require acceptance of Qualifacts Terms of Use. Qualifacts staff cannot provide single-patient exports on behalf of agencies.
- **Fees**: Not mentioned in documentation.
- **Bulk export**: Yes — the population export covers all patients.

## 4. Export Content: What's In It

The data dictionary defines **81 entities** with **960 total fields**. All 960 fields have data types documented. 909 fields (94.7%) have descriptions, though 426 of those are trivial reformulations of the column name (e.g., `AllergiesName` → "Allergies Name"). **534 fields (55.6%) have substantive descriptions** beyond restating the field name. No fields have remarks or value sets documented. No foreign key relationships are explicitly documented.

### Vendor's own content organization

The INDEX sheet classifies entities into categories and modules:

| Category | Entities | Fields | Modules |
|---|---|---|---|
| EMR | 55 | 657 | Charting, Patient Demographic, Interface |
| PM | 11 | 97 | Claims, Payments, Financial Summary, Census, Patient Insurance, Slidding Fee Scale, Patient Estimator Calculator, ERA |
| EMR / PM | 5 | 107 | Patient Insurance, Practice Management, Audit Logs, (none) |
| EHI Export | 1 | 3 | Patient Data Export |
| (uncategorized) | 9 | 96 | (not in INDEX or truncated sheet names) |

The 9 uncategorized entities are: Clinical tests Results, Functioning Functional Status, Health Concerns/Reason for Visit, Images/Documents, Additional Clinical Forms, List of prices/charges, Chief Complaints/HPI, Case Management, and Pregnancy Status. These appear to be clinical entities whose sheet names didn't match INDEX entries due to truncation.

### Top entities by field count

| Entity | Fields | Category | Module |
|---|---|---|---|
| Patient Demographics / Information | 64 | EMR | Patient Demographic |
| Health Insurance Information / Payer | 46 | EMR / PM | Patient Insurance |
| Vital signs | 43 | EMR | Charting |
| Case Management | 40 | (uncategorized) | — |
| Program | 29 | EMR | Patient Demographic |
| Newborn Delivery Information | 26 | EMR | Charting |
| Patient relationships | 22 | EMR | Patient Demographic |
| Encounter information | 21 | EMR | Charting |
| Patient Summary and Plan | 21 | EMR | Charting |
| Prior Authorizations or Authorizations | 21 | EMR / PM | Patient Insurance |
| Diagnostic Imaging | 20 | EMR | Charting |
| Organization | 20 | EMR / PM | Practice Management |
| Past Pregnancy Data | 19 | EMR | Charting |
| Claims | 18 | PM | Claims |
| Immunizations | 18 | EMR | Charting |

The full inventory is in `analysis/entity-inventory-full.json` (81 entities, 960 fields).

### Notable entities

- **Billing/Financial**: Claims (18 fields), Billing codes assigned (3), Billing statements and summaries (6), Charges/refunds/deductibles/interest (6), Collection information (3), Denials (4), EOBs (8), Financial Assistance applications (16), Price Estimates (17), List of prices/charges (2)
- **Behavioral Health**: Psychiatric History (7), Behavioral Data (4), Case Management (40), Substance Abuse (5), Program (29)
- **OB/GYN**: Pregnancy information (13), Past Pregnancy Data (19), Newborn Delivery Information (26), Gynecological History (18), Pregnancy Intent (2), Pregnancy Status (5)
- **History sections**: Medical History (7+13 across two sheets), Surgical History (9), Genetic History (12), Inpatient Hospice History (7), Ambulatory Hospice History (6), Palliative Care Summary History (6), Long Term Care History (5)

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The export is organized into EMR and PM categories covering a broad range of clinical and financial data:

**Richest areas:**
- **Patient Demographics** (64 fields) — the largest single entity, covering extensive demographic detail
- **Insurance/Payer** (46 fields) — deep insurance information including prior authorizations (21 fields) and eligibility (6 fields)
- **Vital Signs** (43 fields) — comprehensive vitals coverage
- **Case Management** (40 fields) — detailed behavioral health case management
- **OB/GYN** (83 fields across 6 entities) — deep pregnancy and gynecological tracking
- **Clinical Notes/Documentation** (~80 fields across 6 entities: Clinical notes, Chief Complaints/HPI, ROS, Physical Exam, Review of Results, Patient Summary/Plan)
- **Program** (29 fields) — program/enrollment tracking

**Thinnest areas:**
- **HL7 ADT notifications** (2 fields) — just message type and sent date
- **List of prices/charges** (2 fields) — minimal pricing data
- **Custom Field** (2 fields) — only field name and value
- **Social History Elements** (2 fields) — thin compared to the detailed Social History Consumption (13 fields)
- **Billing codes assigned** (3 fields) — sparse for a PM feature

**Notable observations:**
- The vendor has 11 dedicated PM (Practice Management) entities covering billing, claims, payments, denials, EOBs, financial assistance, and price estimates — this is a genuine billing/financial data export, not just clinical data.
- Behavioral health specialty data is well-represented with Psychiatric History, Behavioral Data, Case Management (40 fields), Substance Abuse, and Program entities.
- The export includes detailed history sections (medical, surgical, genetic, hospice, palliative care, long-term care) that go well beyond USCDI requirements.
- Documents/Images entity (5 fields) links to actual file attachments in the "Supported File" folder.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | `Patient Demographics / Information` (64 fields), `Patient relationships` (22), `Recorded Sex or Gender` (4) | Thorough — 90 fields across 3 entities |
| Encounters / visits | ✅ Covered | `Encounter information` (21 fields) | Solid coverage |
| Problems / conditions | ✅ Covered | `Problems` (8 fields), `Health Concerns Reason for Visit` (9), `Referring Diagnosis` (6) | Adequate |
| Medications | ✅ Covered | `Medications` (12 fields) | Moderate depth; no separate MAR entity despite product having eMAR |
| Allergies | ✅ Covered | `Allergies` (11 fields) with RXCUI, SNOMED codes, severity, reaction | Good — includes coded data |
| Immunizations | ✅ Covered | `Immunizations` (18 fields) | Thorough |
| Vitals | ✅ Covered | `Vital signs` (43 fields) | Very thorough |
| Lab results | ✅ Covered | `Clinical tests Results` (12 fields) | Adequate; lab integration is an add-on |
| Imaging / diagnostics | ✅ Covered | `Diagnostic Imaging` (20 fields) | Good |
| Procedures | ✅ Covered | `Procedures` (10 fields), `Surgical History` (9) | Adequate |
| Clinical notes / documents | ✅ Covered | `Clinical notes` (13), `Chief Complaints HPI` (11), `Patient Summary and Plan` (21), `Physical Exam` (7), `ROS` (8), `Review of Results` (7), `Additional Clinical Forms` (4) | Strong — 71 fields across 7 entities |
| Care plans / goals | ✅ Covered | `Assessments and Plan of Treatment/Plan of Care` (7), `Goals` (11), `Health Maintenance` (6) | Adequate |
| Orders / referrals | ✅ Covered | `Referrals` (6 fields), `Referring Diagnosis` (6) | Moderate; no dedicated orders entity |
| Insurance / coverage | ✅ Covered | `Health Insurance Information / Payer` (46), `Eligibility Information` (6), `Prior Authorizations` (21) | Very thorough — 73 fields |
| Claims / billing | ✅ Covered | `Claims` (18), `Billing codes assigned` (3), `Billing statements and summaries` (6) | Good — dedicated claims tracking |
| Payments | ✅ Covered | `Charges, refunds, deductibles, interest` (6), `Collection information` (3), `Denials` (4), `EOBs` (8), `Financial Assistance` (16), `Price Estimates` (17), `List of prices` (2) | Very thorough — 56 fields across 7 entities |
| Consents / directives | ✅ Covered | `Consents (TPO, negotiated, HIE, medication, etc.)` (6) | Present |
| Patient communications | ❌ Not covered | No secure messaging, portal messages, or communication log entities | Product has patient portal with secure messaging; this is a gap |
| Specialty – Behavioral Health | ✅ Covered | `Psychiatric History` (7), `Behavioral Data` (4), `Case Management` (40), `Substance Abuse` (5) | Good — 56 fields; case management is notably deep |
| Specialty – OB/GYN | ✅ Covered | `Pregnancy information` (13), `Past Pregnancy Data` (19), `Newborn Delivery` (26), `Gynecological History` (18), `Pregnancy Intent` (2), `Pregnancy Status` (5) | Very thorough — 83 fields across 6 entities |
| Documents / Images | ✅ Covered | `Images Documents` (5 fields) with actual file attachments in "Supported File" folder | Good — includes actual files |
| Social / family history | ✅ Covered | `Family Health History` (15), `Social History Consumption` (13), `Social History Elements` (2), `Smoking status` (8), `Substance Abuse` (5), `Work information` (17) | Very thorough — 60 fields |
| Medical devices | ✅ Covered | `Medical Device` (14 fields) | Good |
| Provenance | ✅ Covered | `Provenance` (3 fields) | Present |

**Coverage: 22 of 23 applicable domains covered. 1 gap (Patient Communications).**

The patient communications gap is notable because InSync has a full patient portal with secure messaging, broadcast messaging, and appointment request features. None of these communication records appear in the export.

Additionally, some covered domains have gaps in depth:
- **eMAR**: The product has electronic medication administration records, but no dedicated MAR entity appears in the export. Medication data is limited to the `Medications` entity (12 fields).
- **Scheduling/appointments**: Not flagged as a gap per EHI scope guidelines, but encounter data (21 fields) does capture visit information.
- **Telehealth**: No dedicated telehealth session metadata entity, though sessions may be captured via encounters.

## 6. Documentation Quality

**Strengths:**
- The data dictionary is a structured XLS workbook with a clear INDEX sheet categorizing all 81 entities by category and module
- Every field has a data type and nullability indicator
- The export format (NDJSON) is well-described with a concrete example of how document attachments link via `DownloadedFilePath`
- The documentation includes both single-patient and population export workflows
- A changelog sheet tracks data dictionary updates (last updated November 2025)

**Weaknesses:**
- **No value sets or coded values**: Fields like `AllergiesSeverityCode`, `ADTMessageType`, or status fields have no enumerated values
- **No foreign keys or relationships**: There is no documentation of how entities relate to each other (e.g., how Claims link to Encounters)
- **Trivial descriptions**: 426 of 960 fields (44.4%) have descriptions that merely restate the column name with spaces (e.g., `AllergiesName` → "Allergies Name")
- **No sample data**: No example NDJSON files or sample exports are provided
- **No machine-readable schema**: The XLS is the only structured artifact; no JSON Schema, OpenAPI spec, or similar
- **No remarks field content**: The "Remarks" column exists in every sheet but is empty for all 960 fields

A developer could build a basic import from this documentation but would need to reverse-engineer relationships between entities, guess at value sets, and handle ambiguous field semantics for nearly half the fields.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Comprehensive**

This export covers 22 of 23 applicable domains — an unusually high coverage rate. The vendor has clearly mapped their internal data model to the export: 81 entities span clinical charting, practice management/billing, behavioral health specialty data, OB/GYN specialty data, insurance, payments, and document attachments. The PM category alone has 11 dedicated entities covering claims, payments, denials, EOBs, financial assistance, and price estimates — this is not a clinical-only export. The behavioral health specialty coverage (Case Management at 40 fields, Psychiatric History, Behavioral Data, Substance Abuse) and OB/GYN coverage (83 fields across 6 entities) reflect the product's actual specialty capabilities. The only notable gap is patient communications/portal messages.

**Axis 2 — Export approach: Purpose-built EHI export**

This is clearly a purpose-built (b)(10) export, not a repackaged clinical exchange:
1. The export uses NDJSON with a custom, product-specific data model — not C-CDA or FHIR
2. The 81 entities map to InSync's internal data structures, not to any standard exchange format
3. The export includes billing/financial entities (Claims, Denials, EOBs, Price Estimates) that would never appear in a (g)(10) FHIR API or C-CDA export
4. A dedicated data dictionary was built specifically for this export (last updated November 2025, with changelogs)
5. The `Provenance` entity and `EHI Export` category in the INDEX confirm purpose-built tooling
6. Qualifacts built identical EHI export infrastructure across their three platforms (InSync, CareLogic, Credible), suggesting organizational investment

### Key Findings

1. **Genuinely broad coverage**: 81 entities across 22 of 23 applicable domains, with particularly strong billing/payments coverage (11 PM entities, 97 fields) and specialty data (behavioral health: 56 fields; OB/GYN: 83 fields). This goes well beyond USCDI.

2. **Purpose-built with product-specific data model**: The NDJSON format with InSync-specific field names and a dedicated XLS data dictionary confirms this is a bespoke (b)(10) export, not a relabeled clinical exchange.

3. **Description quality is mixed**: While 100% of fields have types and 94.7% have descriptions, 44.4% of descriptions are trivial reformulations of field names. Only 55.6% of fields have substantive descriptions. No value sets, relationships, or sample data.

4. **Patient communications gap**: The product has a full patient portal with secure messaging, but no communication records appear in the export's 81 entities — the only significant missing domain.

5. **Good population export support**: Both single-patient and bulk population exports are available, though the population export requires a support ticket and up to 30 days.

### Summary Stats

    Coverage:        Comprehensive
    Approach:        Purpose-built EHI export
    Export format:   NDJSON (per patient) + file attachments in ZIP
    Entities:        81
    Fields:          960
    Descriptions:    55.6% substantive (94.7% total, but 44.4% are trivial name reformulations)
    Sample data:     No
    Bulk export:     Yes (population export via support ticket)
    Domains covered: 22 of 23 applicable domains

### Bottom Line

InSync EMR/PM provides a genuinely comprehensive (b)(10) export that covers clinical, billing, specialty, and administrative data across 81 entities and 960 fields. The export is purpose-built with a product-specific NDJSON format and a structured data dictionary — it is clearly not a repackaged clinical exchange. The main limitation is documentation quality (trivial descriptions, no value sets or relationships) and the absence of patient portal communication records. A patient or provider would get a substantially complete copy of their data from this export.
