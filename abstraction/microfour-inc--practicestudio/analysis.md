# EHI Export Analysis: MicroFour, Inc.

**Product**: PracticeStudio X20
**Analysis date**: 2026-02-16
**CHPL IDs**: 15.04.04.1985.Prac.20.00.1.180810

## 1. Product Context

PracticeStudio is a fully integrated EHR and Practice Management (PM) system developed by MicroFour, Inc., a small (~21–31 employees) company in Amarillo, Texas. It targets small-to-midsize ambulatory medical practices across multiple specialties (family medicine, cardiology, dermatology, orthopedics, chiropractic, urgent care, etc.).

The product is a single platform covering both clinical and financial workflows:

- **Clinical/EHR**: Touch-based charting with specialty templates ("Blueprints"), SOAP notes, problem lists, e-prescribing (RxWriter, Surescripts-certified), lab orders/results (bidirectional HL7), documents & media management, immunization records, clinical quality measures
- **Practice Management**: Appointment scheduling, claims management and scrubbing, electronic claims submission, remittance processing, patient ledger/billing, insurance eligibility verification, inventory control, practice statistics
- **Patient Engagement**: Patient portal (patientwebportal.com), secure messaging, CCD sharing
- **Interoperability**: HL7 v2.5.1, FHIR R4 API (g)(10), DIRECT messaging, NCPDP e-prescribing

This is critical context: PracticeStudio stores **billing/claims data, insurance information, scheduling, inventory, and patient communications** in addition to clinical data. A genuine (b)(10) export should cover all of these domains.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/ExportProcess.html` (85 KB) | The registered (b)(10) EHI export documentation page. Contains a **single paragraph** describing the export process. | **Most informative for (b)(10) assessment** — it's the entirety of the export documentation |
| `downloads/Interoperability.html` (91 KB) | Education page listing 16 CCD sections that PracticeStudio generates, plus HL7/FHIR/NCPDP overview | Useful context — confirms CCD is the export format |
| `downloads/fhir-api-docs/` (16 HTML files, ~800 KB total) | FHIR R4 API documentation for 16 resources (AllergyIntolerance, CarePlan, CareTeam, Condition, DiagnosticReport, DocumentReference, Encounter, Goals, Immunization, Medication, Observation, Organization, Patient, Practitioner, Procedure, Provenance) | Context only — this is the (g)(10) API, **not** the (b)(10) export |
| `downloads/fhir-r4-endpoints-bundle.json` (1.8 KB) | FHIR Endpoints Bundle listing service base URLs | Minimal — just endpoint URLs |
| `downloads/export-process-page.png` / `export-process-fullpage.png` | Screenshots of the export process page | Confirms the page content visually |
| `downloads/enrichment/fhir-docs-extracted.json` (630 KB) | Structured extraction of all documentation pages | Useful reference (verified against source HTML) |

## 3. Export Mechanics

- **Format**: CCD (Continuity of Care Document) — a C-CDA clinical summary
- **Mechanism**: Vendor-assisted. Users must **contact MicroFour technical support** to initiate the export. The exact quote from the documentation page:

  > "In the case where a user needs to export all medical records for their entire user base, they only need to contact MicroFour technical support who will help them to do a mass export. The export will produce CCD documents for each patient."

- **Scope**: Bulk (entire user base), producing one CCD per patient
- **Self-service**: No — requires contacting vendor support
- **Access constraints**: Unknown — no mention of fees, turnaround time, or format options
- **Single-patient export**: Not described for (b)(10); individual CCDs can be generated through the portal/DIRECT messaging for transitions of care, but that's a different workflow

## 4. Export Content: What's In It

### What the (b)(10) export documentation says

The (b)(10) documentation is a **single paragraph** on the Export Process page. It provides:

- **No data dictionary**
- **No field-level documentation**
- **No schema or format specification**
- **No sample data**
- **No description of what data is included beyond "CCD documents"**

The only information about CCD content comes from the separate Interoperability education page, which lists the 16 standard CCD sections:

### Vendor's own content organization

The vendor's CCD contains the standard 16 sections. No product-specific field documentation exists.

| Entity/Table | Fields | Described | Types | Category (vendor's) |
|---|---|---|---|---|
| Advance Directives | N/A | No | No | CCD Section |
| Alerts | N/A | No | No | CCD Section |
| Encounters | N/A | No | No | CCD Section |
| Family History | N/A | No | No | CCD Section |
| Functional Status | N/A | No | No | CCD Section |
| Immunizations | N/A | No | No | CCD Section |
| Medical Equipment | N/A | No | No | CCD Section |
| Medications | N/A | No | No | CCD Section |
| Payers | N/A | No | No | CCD Section |
| Plan of Care | N/A | No | No | CCD Section |
| Problems | N/A | No | No | CCD Section |
| Procedures | N/A | No | No | CCD Section |
| Purpose | N/A | No | No | CCD Section |
| Results | N/A | No | No | CCD Section |
| Social History | N/A | No | No | CCD Section |
| Vital Signs | N/A | No | No | CCD Section |

There are **0 fields documented** at any level. The vendor provides no product-specific data dictionary — the only specification for what these sections contain is the generic CCD/C-CDA standard itself.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor's (b)(10) export is a standard CCD document containing 16 sections. This is the same CCD format used for transitions of care (criteria (b)(1)–(b)(3)) — it is not a purpose-built EHI export.

The 16 CCD sections cover standard clinical summary content:
- **Clinical data**: Problems, Medications, Alerts (allergies), Immunizations, Vital Signs, Results, Procedures, Encounters, Family History, Social History, Functional Status, Plan of Care, Advance Directives, Medical Equipment
- **Limited financial**: Payers section (insurance information only — no claims, charges, or payment data)
- **Metadata**: Purpose section

This is the standard C-CDA clinical summary — it is **exactly** what the vendor already produces for transitions of care. There is no evidence of any additional data domains, vendor-specific extensions, or product-specific customization for (b)(10).

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | CCD header contains basic demographics; no field-level detail documented | CCD includes basic demographics but PracticeStudio stores richer registration data |
| Encounters / visits | ⚠️ Partial | CCD "Encounters" section | Standard CCD encounter data; product likely stores more visit detail |
| Problems / conditions | ⚠️ Partial | CCD "Problems" section | Standard problem list; product may store richer diagnosis context |
| Medications / prescriptions | ⚠️ Partial | CCD "Medications" section | Standard medication list; product's RxWriter stores prescription routing, refill history, formulary data not in CCD |
| Allergies | ⚠️ Partial | CCD "Alerts" section | Standard allergy list |
| Immunizations | ⚠️ Partial | CCD "Immunizations" section | Standard immunization records |
| Vitals | ⚠️ Partial | CCD "Vital Signs" section | Standard vital signs |
| Lab results | ⚠️ Partial | CCD "Results" section | Standard results; product's bidirectional lab integration stores order details, analyte-level discrete data not fully captured in CCD |
| Procedures | ⚠️ Partial | CCD "Procedures" section | Standard procedure list |
| Clinical notes / documents | ❌ Not covered | No CCD section for full clinical notes | Product stores SOAP notes, narrative reports, documents & media — none exported in CCD format beyond what fits in structured sections |
| Care plans / goals | ⚠️ Partial | CCD "Plan of Care" section | Standard care plan |
| Orders / referrals | ❌ Not covered | No CCD section for orders | Product handles lab orders; not in CCD export |
| Insurance / coverage | ⚠️ Partial | CCD "Payers" section | Basic payer info only; product stores eligibility verification data, detailed insurance info |
| Claims / billing | ❌ Not covered | No billing data in CCD | **Major gap** — Product has full claims management, electronic claims submission, remittance processing, patient ledger |
| Payments | ❌ Not covered | No payment data in CCD | **Major gap** — Product tracks patient ledger, remittances, payments |
| Consents / directives | ⚠️ Partial | CCD "Advance Directives" section | Standard advance directives |
| Patient communications | ❌ Not covered | No messaging data in CCD | Product has patient portal with secure messaging |
| Specialty-specific data | ❌ Not covered | No specialty templates/forms in CCD | Product has specialty-specific "Blueprints" for cardiology, dermatology, orthopedics, etc. — none exported |

**Summary**: Of 18 applicable domains, 0 are fully covered, 11 have partial coverage via standard CCD sections, and 7 are not covered at all. The missing domains are significant: billing/claims, payments, clinical notes/documents, orders, patient communications, and specialty-specific clinical data are all core product features with no representation in the CCD export.

## 6. Documentation Quality

The (b)(10) export documentation is **essentially nonexistent**:

- **Total documentation**: 1 paragraph (2 sentences)
- **Data dictionary**: None
- **Field-level documentation**: None
- **Schema/format specification**: None (relies on generic CCD standard)
- **Sample data**: None
- **Machine-readable artifacts**: None
- **Relationship documentation**: None
- **Value sets**: None

A developer could not build an import from this documentation. They would need to rely entirely on the generic CCD/C-CDA specification and reverse-engineer what PracticeStudio populates in each section. There is no indication of which CCD fields PracticeStudio actually populates, what coding systems are used, or how product-specific data maps to CCD elements.

The FHIR API documentation (for (g)(10), not (b)(10)) is modestly better — it includes example responses for 16 resources with field-level JSON examples. However, this is the clinical exchange API, not the EHI export.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Minimal/stub/unclear**

The (b)(10) export is a standard CCD — the same clinical summary format used for transitions of care. A CCD covers a subset of USCDI clinical data domains (problems, medications, allergies, vitals, results, immunizations, etc.) but explicitly does **not** cover billing, claims, payments, detailed clinical notes, specialty forms, patient communications, or any of the practice management data that PracticeStudio stores. Since PracticeStudio is explicitly an integrated EHR+PM system with full billing/claims capabilities, the CCD export omits entire categories of designated record set data. The documentation is too thin (one paragraph) to even assess whether any product-specific content is included beyond standard CCD elements. This is a minimal/stub effort.

**Axis 2 — Export approach: Repackaged existing export**

This is a textbook case of repackaging. The (b)(10) export produces CCD documents — the exact same format PracticeStudio already generates for transitions of care under criteria (b)(1)–(b)(3). The vendor's interoperability page describes CCDs as the standard exchange format, and the export process page simply says "The export will produce CCD documents for each patient." There is no product-specific data dictionary, no additional data domains, no vendor extensions, and no indication that anything was built specifically for (b)(10). The only difference from the standard CCD workflow is that it's a "mass" export triggered by calling support.

### Key Findings

1. **The (b)(10) "export" is simply a mass CCD generation** — users contact MicroFour support to produce CCD documents for all patients. This is the existing transitions-of-care CCD repackaged as (b)(10). (Source: `ExportProcess.html`, line 129)

2. **Documentation is a single paragraph** — the entire (b)(10) documentation is two sentences with no data dictionary, no schema, no field documentation, and no sample data. (Source: `ExportProcess.html`)

3. **Entire practice management domain is missing** — PracticeStudio is an integrated EHR+PM system with claims management, remittance processing, patient ledger, and insurance verification. None of this data is in the CCD export. (Source: `product-research.md` capabilities vs. CCD section list from `Interoperability.html`)

4. **Clinical notes and documents are not exported** — the product stores SOAP notes, narrative reports, and uploaded documents/media, but CCD structured sections don't capture full clinical note content. (Source: product features vs. CCD format limitations)

5. **Export requires vendor intervention** — there is no self-service mechanism; users must contact MicroFour technical support. No turnaround time or process details are documented. (Source: `ExportProcess.html`)

### Summary Stats

```
Coverage:        Minimal/stub/unclear
Approach:        Repackaged existing export
Export format:   CCD (C-CDA)
Entities:        16 (standard CCD sections, no product-specific entities)
Fields:          N/A (no field-level documentation)
Descriptions:    N/A
Sample data:     No
Bulk export:     Yes (vendor-assisted mass export)
Domains covered: 0 of 18 fully; 11 of 18 partially via standard CCD
```

### Bottom Line

PracticeStudio's (b)(10) export is its existing CCD clinical summary relabeled as an EHI export — a single paragraph of documentation pointing to vendor-assisted mass CCD generation with no data dictionary and no coverage of billing, practice management, specialty forms, or clinical notes beyond standard CCD sections. For a product that is explicitly an integrated EHR and practice management system, exporting only a clinical summary leaves the majority of the designated record set — billing, claims, payments, patient communications, specialty templates, and detailed clinical documentation — completely unaddressed.
