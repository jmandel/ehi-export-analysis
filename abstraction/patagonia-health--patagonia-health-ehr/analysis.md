# EHI Export Analysis: Patagonia Health

**Product**: Patagonia Health EHR (Version 6)
**Analysis date**: 2026-02-16
**CHPL IDs**: 15.04.04.2139.Pata.06.01.1.221227

## 1. Product Context

Patagonia Health EHR is a cloud-based integrated EHR, practice management, and billing platform specifically designed for **public health departments** and **behavioral health agencies**. Founded in 2009, the company serves 510+ counties across 38+ states, processing $622M+ in claims. Key capabilities relevant to export completeness:

- **Clinical documentation**: Customizable clinical templates, encounter notes, problem lists, medication lists, allergy lists, immunization records, lab orders/results, vital signs, care plans, referrals, document uploads
- **Behavioral health**: Psychiatric assessments, treatment plans, progress notes, group notes, case management notes, DSM-5 coding
- **Public health programs**: Immunization tracking and registry sync, communicable disease surveillance, contact tracing, vaccine inventory, community outreach
- **Billing & revenue cycle**: Insurance claim submission/processing, clearinghouse connectivity, automated insurance verification, financial reporting, claims scrubbing
- **Practice management**: Scheduling, patient registration, intake/consent forms, referral tracking, case management
- **Patient portal (MyHealth)**: Secure messaging, questionnaires, demographic/insurance updates, lab results viewing
- **E-prescribing**: Surescripts connectivity, drug interaction/allergy checking
- **Telehealth**: Embedded audio/video virtual visits

This is a comprehensive platform — not just a charting tool — with integrated billing, scheduling, and specialty workflows for public/behavioral health.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/ehi-export-section.html` (3.1 KB) | Extracted EHI Export documentation section from the ONC certification page. This is the **only** (b)(10)-specific documentation. | **Most informative** for understanding the EHI export itself |
| `downloads/onc-certified-hit-page.html` (50.8 KB) | Full HTML of the ONC certification page containing the EHI Export section, Meaningful Use info, and API links | Context for the EHI section |
| `downloads/PatientHealth-Data-API-Documentation-v1.1.pdf` (7 pages, 364 KB) | Proprietary REST API documentation (April 2018). Returns C-CDA XML in JSON wrappers. Lists 19 clinical sections available. | Useful — documents C-CDA sections available |
| `downloads/SmartOnFHIR-API-Documentation.pdf` (67 pages, 840 KB) | SmartOnFHIR (g)(10) FHIR R4 API documentation. 20 FHIR resource types documented. | Not directly relevant — this is (g)(10), NOT (b)(10) |
| `downloads/FHIRBaseURL.json` (4.8 KB) | FHIR Service Base URLs for (g)(10) API discovery | Not relevant to EHI export |
| `downloads/PatagoniaHealth-MeaningfulUse-Stage3-CostsandLimitations-May2018.pdf` (3 pages, 117 KB) | Supplemental costs/limitations document from 2018 | Not relevant to EHI export |
| `downloads/screenshot-ehi-export-section-1.png` through `-3.png` | Screenshots of EHI export section on certification page | Confirms HTML content; no additional information |
| `downloads/screenshot-main-page-top.png` | Screenshot of the top of the certification page | Minimal relevance |

**Key observation**: There is **no data dictionary, no schema documentation, no field-level documentation, and no sample data** for the (b)(10) EHI export. The entire EHI export documentation consists of approximately 300 words of prose on the certification page.

## 3. Export Mechanics

- **Format**: Clinical data exported as **C-CDA 2.1 Release 2 (USCDI v1)** XML. Billing data exported as **CSV, XLSX, or PDF**.
- **Mechanism**: UI-based export via two separate workflows:
  - **Clinical**: Reports > Medical Practice Reports > Electronic Health Information (EHI) Export
  - **Billing**: Dashboard > Billing > Reports > Claim > Detail (separate navigation path)
- **Single-patient**: Yes — search for specific patient, click "EHI Export" to download. Billing data: Dashboard > Billing > Search > Claims.
- **Multi-patient (bulk)**: Yes — "Multi Patients" button with scheduled task execution (Queued → Completed status). Billing bulk: set all date filters to "All" and run report.
- **Access constraints**: Role-based access — Practice Administrator must enable "EHI Export" and "Schedule Data Export" permissions per user via Practice Administration > Staff Management > Edit Selected User.
- **Fees**: Not mentioned.

**Critical note**: The clinical and billing exports are separate processes accessed through different parts of the application. There is no single unified EHI export.

## 4. Export Content: What's In It

### No Data Dictionary

Patagonia Health provides **zero field-level documentation** for the (b)(10) EHI export. There is:
- No data dictionary
- No schema documentation
- No field-name listing
- No type documentation
- No relationship documentation
- No value set documentation
- No sample data files

The only description of what's exported is the statement: *"The format of the clinical data is CCDA 2.1 Release 2 USCDI v1."* This tells us the export follows the standard C-CDA specification — it is not a product-specific mapping.

### Clinical Export (C-CDA 2.1)

The clinical export produces standard C-CDA 2.1 XML. Based on the Patient Health Data API documentation (which uses the same underlying C-CDA engine), the following 19 clinical sections are available:

| Section | C-CDA Standard Section |
|---|---|
| Patient Demographics | Standard C-CDA header |
| Allergies and Intolerances | Standard C-CDA section |
| Assessment | Standard C-CDA section |
| Care Team | Standard C-CDA section |
| Encounters | Standard C-CDA section |
| Functional Status | Standard C-CDA section |
| Goals | Standard C-CDA section |
| Health Concerns | Standard C-CDA section |
| Immunizations | Standard C-CDA section |
| Medical Equipment | Standard C-CDA section |
| Medications | Standard C-CDA section |
| Mental Status | Standard C-CDA section |
| Plan of Treatment | Standard C-CDA section |
| Problem | Standard C-CDA section |
| Procedures | Standard C-CDA section |
| Reason for Referral | Standard C-CDA section |
| Results | Standard C-CDA section |
| Social History | Standard C-CDA section |
| Vital Signs | Standard C-CDA section |

These are **standard C-CDA sections** — there is no evidence of any vendor-specific extensions, additional data elements, or mapping beyond what the C-CDA 2.1 / USCDI v1 standard defines. The documentation explicitly states the format is "CCDA 2.1 Release 2 USCDI v1."

### Billing Export

Billing data is exported via a completely separate workflow:
- Single patient: Dashboard > Billing > Search > Claims → download as CSV or XLSX
- Multi-patient: Dashboard > Billing > Reports > Claim > Detail → set all dates to "All" → export as CSV, XLSX, or PDF

**No documentation exists for what fields are included in the billing export.** The vendor provides no field names, no schema, no sample data — just the instruction to navigate to the billing module and export.

### Vendor's own content organization

Since no data dictionary exists, the only content organization comes from the vendor's EHI export documentation:

| Entity/Category | Fields | Described | Types | Format | Source |
|---|---|---|---|---|---|
| Clinical Data (19 C-CDA sections) | Unknown | N/A | N/A | C-CDA 2.1 XML | EHI Export UI |
| Claims Data | Unknown | N/A | N/A | CSV/XLSX/PDF | Billing Reports UI |
| Patient Financial Data | Unknown | N/A | N/A | CSV/XLSX | Billing Search UI |

**Total documented fields: 0.** No field-level documentation exists for any part of the export.

Full machine-readable inventory: `analysis/entity-inventory-full.json` (21 entities cataloged from available documentation, 0 fields documented).

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor describes two export categories:

1. **Clinical data** — exported as C-CDA 2.1 (USCDI v1). This covers standard clinical summary sections: demographics, allergies, medications, problems, procedures, results, immunizations, vital signs, encounters, care team, goals, health concerns, assessments, social history, functional/mental status, plan of treatment, reason for referral, and medical equipment. This is a **standard clinical summary document** — the same content that would be exchanged via transitions of care or patient access. There is no evidence the export includes any product-specific data beyond what C-CDA 2.1 defines.

2. **Billing data** — exported as CSV/XLSX via the billing reports module. While billing inclusion is a positive signal, there is zero documentation of what fields or scope this covers. It could range from a full claims history to a simple claim status list.

The **thinnest** aspect is documentation quality — with zero field-level documentation, it's impossible to assess depth. The **strongest** signal is that billing data is at least mentioned as part of the export, unlike many vendors who only provide clinical summaries.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | C-CDA header demographics section | C-CDA provides limited demographic fields (name, DOB, address, phone, gender, race, ethnicity, language). Product likely stores more (insurance info, emergency contacts, portal data). |
| Encounters / visits | ⚠️ Partial | C-CDA Encounters section | Standard C-CDA encounter summaries; likely missing detailed encounter metadata, custom forms, behavioral health session details |
| Problems / conditions | ⚠️ Partial | C-CDA Problem section | Standard C-CDA problem list; may miss behavioral health-specific diagnostic details, DSM-5 coding depth |
| Medications / prescriptions | ⚠️ Partial | C-CDA Medications section | Standard C-CDA medication list; likely missing detailed e-prescribing history, pharmacy interactions |
| Allergies | ✅ Covered | C-CDA Allergies and Intolerances section | Standard C-CDA coverage likely sufficient for allergy data |
| Immunizations | ⚠️ Partial | C-CDA Immunizations section | Standard C-CDA immunization records; may miss vaccine inventory linkage, VFC eligibility, registry sync details — important for a public health product |
| Vitals | ✅ Covered | C-CDA Vital Signs section | Standard C-CDA vital signs likely sufficient |
| Lab results | ⚠️ Partial | C-CDA Results section | Standard C-CDA results; may miss detailed lab order workflows, specimen details |
| Imaging / diagnostic reports | ⚠️ Partial | No dedicated section; may be in Results | Limited evidence of imaging support |
| Procedures | ⚠️ Partial | C-CDA Procedures section | Standard C-CDA procedures |
| Clinical notes / documents | ⚠️ Partial | No dedicated clinical notes section in C-CDA export | C-CDA is a structured summary, not a notes repository. Behavioral health notes, progress notes, group notes are a core product feature but may not be fully captured in C-CDA |
| Care plans / goals | ⚠️ Partial | C-CDA Goals, Plan of Treatment, Health Concerns sections | Standard C-CDA coverage; behavioral health treatment plans may have more depth than C-CDA captures |
| Orders / referrals | ⚠️ Partial | C-CDA Reason for Referral section | Referral reason only; no detailed referral tracking, order sets, or order status |
| Insurance / coverage | ❌ Not covered | Not in C-CDA; unknown if in billing export | Product stores insurance info (automated verification feature); not documented in export |
| Claims / billing | ⚠️ Partial | Billing export exists (CSV/XLSX) but undocumented | Billing export mentioned but zero field documentation; impossible to assess completeness. Product processes $622M+ in claims. |
| Payments | ❌ Not covered | No evidence | Product has revenue cycle capabilities; no payment data in documented export |
| Consents / directives | ❌ Not covered | No evidence | Product supports electronic consent forms; not in export |
| Patient communications / portal messages | ❌ Not covered | No evidence | Product has MyHealth patient portal with secure messaging; not in export |
| Specialty: Behavioral health | ❌ Not covered | No evidence beyond standard C-CDA | Product is specifically designed for behavioral health — psychiatric assessments, treatment plans, group notes, DSM-5 coding — none of this specialty data appears in a standard C-CDA export |
| Specialty: Public health | ❌ Not covered | No evidence | Product's core market — communicable disease surveillance, contact tracing, immunization registries, community outreach — none documented in export |

## 6. Documentation Quality

The EHI export documentation is **extremely thin** — approximately 300 words of prose on the certification web page with no supporting technical artifacts:

- **No data dictionary**: Zero field-level documentation for either the clinical or billing export
- **No schema**: No machine-readable definition of export content
- **No sample data**: No example export files provided
- **No field names, types, or descriptions**: A developer receiving this export would have to reverse-engineer the C-CDA XML structure from the generic C-CDA standard specification and guess at the billing CSV column meanings
- **No relationships or foreign keys**: No documentation of how clinical and billing data relate
- **No value sets**: No coded value documentation
- **Split workflow**: The clinical and billing exports are accessed through different parts of the application with separate instructions, suggesting they were not designed as a unified EHI export

**Could a developer build an import from this documentation alone?** For the clinical C-CDA: partially — they could rely on the generic C-CDA 2.1 standard, but wouldn't know which optional fields Patagonia populates or any vendor extensions. For the billing CSV/XLSX: no — there is literally no documentation of what columns or data are included.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Partial**

The export covers standard clinical summary data via C-CDA 2.1 and mentions billing data via CSV/XLSX. However, significant gaps exist relative to what the product stores:
- **Behavioral health** data (the product's primary specialty) has no dedicated export path — psychiatric assessments, treatment plans, group notes, DSM-5 coding details are unlikely to be fully captured in standard C-CDA sections
- **Public health** program data (the product's core market — disease surveillance, contact tracing, immunization registries, community outreach) has no representation in the export
- **Patient portal** data (secure messages, questionnaires) is absent
- **Practice management** data (scheduling, referral tracking, case management) is absent
- **Consents and intake forms** are absent
- Billing is mentioned but completely undocumented, making it impossible to verify actual coverage

The clinical portion is standard USCDI v1 scope — the regulatory floor for clinical exchange, not a comprehensive EHI export. The billing mention elevates this above pure C-CDA repackaging, but the lack of any documentation makes it impossible to confirm actual billing coverage.

**Axis 2 — Export approach: Repackaged existing export**

The clinical export is explicitly documented as "CCDA 2.1 Release 2 USCDI v1" — this is the vendor's existing C-CDA clinical exchange capability relabeled as (b)(10). The telltale signs:
1. The format is standard C-CDA with no vendor-specific extensions or product-specific data dictionary
2. The documentation references USCDI v1, which is the clinical exchange standard, not a comprehensive EHI specification
3. The same C-CDA engine powers both the Patient Health Data API (from 2018, predating (b)(10)) and the EHI export
4. The billing data is accessed through the existing billing reports module, not a purpose-built export
5. There are two separate export paths (clinical + billing) rather than a unified EHI export, suggesting the vendor assembled existing capabilities rather than building something new

The billing CSV/XLSX component is a step beyond pure C-CDA repackaging — many vendors don't even mention billing — but it appears to be the existing billing report download functionality relabeled, not a purpose-built comprehensive export.

### Key Findings

1. **No data dictionary or field documentation exists.** The entire (b)(10) documentation is ~300 words of prose with zero field-level detail. This is among the thinnest EHI export documentation possible. (`downloads/ehi-export-section.html`)

2. **Clinical export is standard C-CDA 2.1 / USCDI v1** — the same clinical summary format used for transitions of care and patient access, not a purpose-built comprehensive export. The 19 C-CDA sections map exactly to standard C-CDA content. (`downloads/ehi-export-section.html`, `downloads/PatientHealth-Data-API-Documentation-v1.1.pdf`)

3. **Behavioral health and public health specialty data — the product's core differentiators — have no dedicated export path.** Standard C-CDA sections cannot capture psychiatric assessments, DSM-5 coding details, group therapy notes, communicable disease surveillance, contact tracing, or immunization registry data in meaningful depth.

4. **Billing data is mentioned but completely undocumented.** The vendor says billing data can be exported as CSV/XLSX but provides no field names, no schema, no sample data. This makes it impossible to assess actual billing coverage despite the product processing $622M+ in claims.

5. **The export is split across two separate UI workflows** (clinical via Reports, billing via Dashboard > Billing), suggesting this is an assembly of existing capabilities rather than a purpose-built (b)(10) export.

### Summary Stats

```
Coverage:        Partial
Approach:        Repackaged existing export
Export format:   C-CDA 2.1 XML (clinical) + CSV/XLSX/PDF (billing)
Entities:        21 (19 C-CDA sections + 2 billing categories)
Fields:          0 documented
Descriptions:    N/A (no field documentation exists)
Sample data:     No
Bulk export:     Yes (multi-patient with scheduled task)
Domains covered: 3-4 of 19 applicable domains (allergies, vitals confirmed; others partial or undocumented)
```

### Bottom Line

Patagonia Health's (b)(10) export is a standard C-CDA clinical summary paired with an undocumented billing CSV/XLSX download — neither component has field-level documentation, and the clinical portion explicitly uses USCDI v1 scope. For a product whose core value proposition is behavioral health and public health workflows, the absence of any specialty-specific export content is the most significant gap. A patient or provider would get a basic clinical summary and some billing data, but would miss the behavioral health assessments, public health program data, portal communications, and custom forms that represent much of what makes this product's records meaningful.
