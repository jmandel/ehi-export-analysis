# EHI Export Analysis: DOX EMR

**Product**: DOX EMR v5.2
**Analysis date**: 2026-02-15
**CHPL IDs**: 15.02.05.1317.DOXE.01.01.1.220131 (CHPL ID 10806)

## 1. Product Context

DOX EMR is a cloud-based, specialty-specific EHR and practice management system designed exclusively for podiatry practices. Founded in 2002 by Dr. Bart Ripperger, DPM, the product is built around a pre-built podiatry-specific medical database covering "all location, diagnosis, treatment, and plan options for conditions below the knee." It is a very small company based in Scottsdale, Arizona, with a handful of staff and a small installed base.

The product is an integrated EMR/PM system with modules for:
- **Front Office**: scheduling, demographics, insurance management
- **EMR/Clinical**: podiatry-specific charting, assessments, diagnoses, treatment plans, medication management, allergies, vitals
- **E-Prescribing/Orders**: auto-generated orders and prescriptions from clinical documentation
- **Patient Portal**: patient-completed medical histories, lab results, appointment viewing
- **Billing/RCM**: integrated billing with automatic CPT/ICD code extraction, claims, invoices, payments
- **Clinical Quality Measures**: MIPS/Meaningful Use reporting
- **Interoperability**: FHIR API (g)(10), Direct messaging, C-CDA transitions of care

This baseline establishes that a complete EHI export should cover clinical data (podiatry-specific structured assessments, notes, medications, labs, etc.), billing data (claims, invoices, payments, insurance), and patient-entered portal data — not just a standard clinical summary.

## 2. Artifacts Reviewed

| Artifact | Description | Informative? |
|---|---|---|
| `downloads/b10doc-page.html` | Raw HTML of the (b)(10) documentation page (417 KB, mostly Wix JavaScript framework). Contains 3 sentences of actual EHI export content. | **Primary source** — but contains almost no information |
| `downloads/b10doc-page-screenshot.png` | Full-page screenshot of the rendered b(10) page (210 KB). Confirms the page shows only a title, 3 sentences, and one external link. | Confirms minimal content |
| `product-research.md` | Prior research on DOX EMR's product capabilities and data domains | Useful for establishing baseline of what the product stores |
| `ehi-export-report.md` | Prior agent's narrative analysis of the export documentation | Useful for orientation; findings confirmed by direct artifact inspection |
| `chpl-metadata.json` | CHPL certification details including all certified criteria | Confirms (b)(10) certification and broad criteria coverage |
| `files.json` | Manifest of downloaded artifacts | Confirms only 2 files were available to download |
| `sources.json` | URLs visited during research | Documents that the full site was searched for additional content |

**No data dictionary, schema, sample data, user guide, or downloadable documentation of any kind was found.** The entire vendor-provided documentation is 3 sentences on a single web page.

## 3. Export Mechanics

- **Format**: C-CDA XML (Consolidated Clinical Document Architecture)
- **Standard**: USCDI v1
- **Scope**: Single patient and patient population ("DOX EMR authorized users can generate the Electronic Health Information Export (EHI) for a single patient and also the patient population")
- **Mechanism**: Not documented. No user instructions, screenshots, or workflow description for how to trigger the export.
- **Access constraints**: Not documented. No mention of fees, role requirements, or turnaround time.
- **Documentation reference**: The only reference is to the external HL7 C-CDA Implementation Guide at `https://www.hl7.org/implement/standards/product_brief.cfm?product_id=492` — a generic standard, not vendor-specific documentation.

## 4. Export Content: What's In It

### What the documentation says

The entire (b)(10) documentation consists of this single statement:

> "DOX EMR authorized users can generate the Electronic Health Information Export (EHI) for a single patient and also the patient population using CCDA xml format that comply with USCDI v1 requirements standards."

This tells us only that the export format is C-CDA XML conforming to USCDI v1. There is:

- **No data dictionary**: zero entities, zero fields documented
- **No schema**: no vendor-specific C-CDA templates or constraints
- **No sample data**: no example export files
- **No field-level documentation**: not even a list of which C-CDA sections are populated
- **No export instructions**: no description of how to initiate the export
- **No downloadable artifacts**: the page contains zero downloadable files (confirmed by parsing all 31 links on the page; 0 point to PDF, ZIP, CSV, JSON, XML, or any other documentation file — see `analysis/b10-content-analysis.json`)

### What C-CDA USCDI v1 can contain (maximum theoretical coverage)

At best, a C-CDA USCDI v1 document would contain these sections:
- Patient demographics (recordTarget)
- Allergies and intolerances
- Medications
- Problems / conditions
- Procedures
- Lab results
- Vital signs
- Immunizations
- Clinical notes (various note types)
- Care team members
- Goals
- Health concerns
- Assessment and plan
- Smoking status

This represents the standard clinical summary data — the same data available through their (g)(10) FHIR API.

### What cannot be in C-CDA USCDI v1

C-CDA is a clinical document exchange standard. It has no sections or structures for:
- Billing records (CPT codes, claims, invoices)
- Payment data
- Insurance / payer details (beyond minimal header)
- Specialty-specific structured data (podiatry database)
- Patient portal activity (patient-entered histories)
- Clinical quality measure calculations
- Full order lifecycle data

## 5. Coverage Assessment

Based on the coverage gap analysis (`analysis/coverage-gap-analysis.json`), mapping DOX EMR's known data domains against what C-CDA USCDI v1 can represent:

| Domain | Product Stores? | Export Coverage | Notes |
|---|---|---|---|
| Demographics & contacts | Yes | **Covered** | C-CDA recordTarget |
| Problems / diagnoses | Yes | **Covered** | C-CDA Problems section |
| Medications / prescriptions | Yes | **Covered** | C-CDA Medications section |
| Allergies | Yes | **Covered** | C-CDA Allergies section |
| Immunizations | Yes | **Covered** | C-CDA Immunizations section |
| Vitals | Yes | **Covered** | C-CDA Vital Signs section |
| Lab results | Yes | **Covered** | C-CDA Results section |
| Procedures | Yes | **Covered** | C-CDA Procedures section |
| Care plans / goals | Yes | **Covered** | C-CDA Goals / Plan of Treatment |
| Encounters / visits | Yes | **Partially covered** | C-CDA Encounters section exists but limited |
| Clinical notes | Yes | **Partially covered** | Notes representable but podiatry-specific structured data may not transfer |
| Orders / referrals | Yes | **Partially covered** | Some orders in C-CDA but not full lifecycle |
| Insurance / coverage | Yes | **Not covered** | C-CDA has no payer/insurance detail sections |
| Billing (CPT/ICD, claims, invoices) | Yes | **Not covered** | No billing sections in C-CDA |
| Payments | Yes | **Not covered** | No payment data in C-CDA |
| Podiatry-specific structured data | Yes | **Not covered** | Proprietary pre-built podiatry database cannot map to standard C-CDA |
| Patient portal data | Yes | **Not covered** | Patient-entered histories not representable |
| Clinical quality measures | Yes | **Not covered** | CQM data not in C-CDA |

**Summary**: Of 18 data domains DOX EMR stores, 9 (50%) are covered by C-CDA USCDI v1, 3 (17%) are partially covered, and 6 (33%) are not covered at all.

The most significant gaps are:
1. **Billing/financial data** — DOX EMR's integrated billing module auto-extracts CPT and ICD codes, manages claims, invoices, and payments. None of this is exportable via C-CDA.
2. **Podiatry-specific structured clinical data** — The product's core differentiator is its pre-built podiatry database. This proprietary structured data for conditions below the knee almost certainly cannot be fully represented in standard C-CDA sections.
3. **Insurance/payer information** — Managed in the front office module but not representable in C-CDA.

## 6. Documentation Quality

The documentation quality is essentially zero:

- **Comprehensiveness**: 3 sentences. No data dictionary, no schema, no sample data, no user guide.
- **Developer usability**: A developer receiving a DOX EMR export would have only the generic C-CDA specification to work with. They would have no guidance on which sections are populated, what value sets are used, how DOX EMR's internal data model maps to C-CDA, or what data is missing from the export.
- **Machine-readable artifacts**: None. Zero downloadable files of any kind.
- **Vendor-specific information**: The only vendor-specific content is the statement that they use "V1 standard for connection." Everything else defers to the external HL7 C-CDA standard.
- **Import feasibility**: A developer could not build a reliable import from this documentation. They would need to reverse-engineer the actual C-CDA output to understand what's included.

The page has been in this minimal state since at least November 2025 (per Wayback Machine), despite certification in January 2022 — over 4 years without improvement.

## 7. Overall Assessment

### Classification

**Minimal/stub**: The documentation is too thin to fully assess export content, and the stated export format (C-CDA USCDI v1) structurally limits coverage to roughly half of the data domains the product stores. This is a textbook case of C-CDA/FHIR repackaging — the vendor's (b)(10) "EHI export" appears to be their existing clinical document capability relabeled for compliance purposes.

### Key Findings

1. **The entire (b)(10) documentation is 3 sentences on a single web page with zero downloadable artifacts** — no data dictionary, no schema, no sample data, no user guide, no field-level documentation of any kind (source: `downloads/b10doc-page.html`, confirmed by screenshot and HTML parsing in `analysis/b10-content-analysis.json`).

2. **The export is C-CDA XML limited to USCDI v1**, which is a clinical summary standard — not a database export format. This covers the same data as their (g)(10) FHIR API and structurally cannot include billing, insurance, payments, or specialty-specific structured data (source: vendor's own statement on the b10doc page).

3. **6 of 18 data domains (33%) are structurally excluded** by the choice of C-CDA as the export format, including billing/claims, payments, insurance details, podiatry-specific structured data, patient portal data, and clinical quality measures (source: `analysis/coverage-gap-analysis.json`).

4. **The product's core differentiator — its pre-built podiatry database — is likely not exportable.** DOX EMR's unique value is structured clinical data for conditions below the knee. This proprietary data model almost certainly exceeds what standard C-CDA sections can represent, yet no vendor extensions or custom mappings are documented.

5. **No export instructions exist.** A user cannot determine from the documentation how to initiate an export, what roles are required, or what the output looks like.

### Bottom Line

A patient or provider requesting their complete data from DOX EMR would receive, at best, a standard clinical summary (demographics, meds, allergies, labs, vitals, notes) — equivalent to what's already available through the FHIR API. Billing records, insurance information, payment history, and the podiatry-specific structured clinical data that is the product's core value would all be missing. The documentation provides no evidence of a genuine effort to comply with the (b)(10) requirement for export of all electronic health information.
