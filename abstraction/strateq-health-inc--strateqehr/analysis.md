# EHI Export Analysis: Strateq Health, Inc.

**Product**: StrateqEHR Version 5
**Analysis date**: 2026-02-16
**CHPL ID**: 15.05.05.3097.STRQ.01.00.1.220105 (ID 10778)

## 1. Product Context

StrateqEHR is a comprehensive, cloud-based Hospital Information System (HIS) developed by Strateq Health, Inc., a subsidiary of Malaysia-based Strateq Group. It targets critical access hospitals, rural hospitals, small community hospitals, and freestanding emergency rooms. The system is delivered as SaaS on AWS.

The product is not a lightweight ambulatory EHR — it is a full-scope inpatient HIS covering:

- **Patient Administration / ADT**: Registration, admission/discharge/transfer, bed management, insurance verification, scheduling
- **Clinical Documentation**: H&P, assessments, care plans, nursing notes, dictation, via a proprietary "Dynamic Form Engine"
- **CPOE**: Close-loop orders for medications, labs, radiology, nursing, and procedures; complaint-specific order sets for ED
- **Pharmacy / Medication Management**: Integrated pharmacy, e-prescribing (SureScripts/NewCrop), FDB drug database, eMAR, medication reconciliation
- **Emergency Department**: ED tracking board (ESI, location, LOS, disposition), triage documentation, ED-specific templates
- **Nursing**: Care plans, assessments, eMAR, worklists, Kardex
- **Perioperative**: Scheduling, operative checklists, documentation, order entry
- **HIM / Medical Records**: Patient master record, document scanning, deficiency tracking, release of information
- **Revenue Cycle Management**: Charges, claims processing (Waystar), eligibility checking, 3M CRS coding integration, remittance processing, denial management, patient statements, credit card payments, GL journal entries
- **Patient Portal**: Via Bridge Patient Portal (third-party)
- **Interoperability**: C-CDA, FHIR API (g)(7)–(g)(10), e-prescribing, immunization registry, syndromic surveillance, CQMs

This is a system that stores extensive clinical, financial, and operational data about patients. A compliant (b)(10) EHI export should cover demographics, clinical documentation, orders, medications/eMAR, lab results, vitals, billing/claims, insurance, ED data, perioperative data, scanned documents, and more.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `Strateq-Export.pdf` (282 KB, 1 page) | The entire EHI export documentation. A single A4 page with 7 paragraphs / 9 sentences describing the export as a ZIP of per-encounter C-CDAs plus attached files. Created 2023-12-06 from "Microsoft Word - Export.docx" via "Microsoft: Print To PDF." | **Primary artifact** — but extremely thin. Contains no data dictionary, no field definitions, no schema, no sample data, no export instructions. |

No other artifacts were found. The vendor's certification page links to the same PDF as their sole (b)(10) documentation. Other PDFs on the certification page (Real-World Testing plans, SMART on FHIR API documentation) relate to other certification criteria, not (b)(10).

## 3. Export Mechanics

- **Format**: ZIP archive containing per-encounter C-CDA documents (themselves in ZIP sub-archives) and "other files attached to the patient's chart (e.g. PDF and images)"
- **Mechanism**: Not documented. The PDF contains no information about how a user initiates the export — no UI screenshots, no API endpoints, no workflow description.
- **Single-patient vs bulk**: Not documented. The language ("the patient EHI export") suggests single-patient scope.
- **Access constraints or fees**: Not documented.

## 4. Export Content: What's In It

### What the documentation says

The documentation is 7 paragraphs on a single page. Here is the substantive content (excluding the title line and 3 paragraphs that are generic definitions of ZIP, PDF, and C-CDA file formats):

1. "The patient EHI export contains data from the patient's chart. Multiple file formats are used to store this information."
2. "The export file itself is a zip file. It contains zip files of C-CDAs and other files attached to the patient's chart (e.g. PDF and images)"
3. "Information for each patient encounter is available C-CDA format in zip archive."

That is the totality of the export content description.

### What is not documented

- **No data dictionary**: Zero entities, zero fields, zero descriptions
- **No C-CDA template specification**: No indication of which C-CDA document types are generated (CCD, Discharge Summary, Progress Note, Operative Note, etc.)
- **No C-CDA section enumeration**: No listing of which sections are populated within the C-CDA documents
- **No field-level documentation**: No information about what specific data elements appear in the C-CDA or what coding systems are used
- **No sample data**: No example C-CDA files, no example export ZIP structure
- **No schema**: No machine-readable specification of any kind
- **No mention of non-clinical data**: Billing, claims, revenue cycle, insurance, orders, eMAR, ED tracking, perioperative, HIM — none of these are mentioned

### Vendor's own content organization

The vendor provides no content organization. There is no data dictionary, no entity listing, and no categorization of exported data.

| Entity/Table | Fields | Described | Types | Category |
|---|---|---|---|---|
| *(none documented)* | 0 | 0 | N/A | N/A |

**Total entities: 0. Total fields: 0. Fields with descriptions: 0.**

The full inventory is saved at `analysis/full-entity-inventory.json`.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor's documentation describes exactly one export mechanism: per-encounter C-CDA documents bundled in a ZIP archive, alongside attached files (PDFs, images). There is no categorization, no data domain enumeration, and no indication of scope beyond "data from the patient's chart."

C-CDA is a clinical summary standard. At best, it can carry:
- Demographics
- Problems/diagnoses
- Medications
- Allergies
- Immunizations
- Vitals
- Lab results
- Procedures
- Clinical notes (as narrative sections)
- Care plans (if explicitly implemented)

However, without documentation of which C-CDA templates and sections are used, we cannot confirm that even these clinical domains are populated in the export.

C-CDA structurally cannot represent:
- Billing/claims/charges/remittance/GL data
- Order lifecycle data (CPOE with statuses, timestamps, results linkage)
- eMAR administration records (detailed medication administration with nurse, time, held/refused)
- ED tracking operational data (ESI, arrival time, disposition, LOS, turnaround times)
- Dynamic Form Engine structured data (custom clinical forms)
- HIM records (deficiency tracking, ROI)
- Insurance/eligibility verification data
- Perioperative checklists and scheduling

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | C-CDA likely includes demographics header, but no confirmation of specific fields | Product stores extensive registration data; C-CDA header is a subset |
| Encounters / visits | ⚠️ Partial | Documentation says "per encounter" C-CDA; encounter metadata likely in C-CDA headers | ADT detail, ED tracking data, LOS data unlikely to be fully represented |
| Problems / conditions | ⚠️ Partial | Standard C-CDA section; likely present but unconfirmed | Probably adequate if section is populated |
| Medications / prescriptions | ⚠️ Partial | Standard C-CDA section; likely present but unconfirmed | eMAR administration records (timestamps, nurse, held/refused) unlikely in C-CDA |
| Allergies | ⚠️ Partial | Standard C-CDA section; likely present but unconfirmed | Probably adequate if section is populated |
| Immunizations | ⚠️ Partial | Standard C-CDA section; likely present but unconfirmed | Product does immunization registry reporting; C-CDA section may suffice |
| Vitals | ⚠️ Partial | Standard C-CDA section; likely present but unconfirmed | Probably adequate if section is populated |
| Lab results | ⚠️ Partial | Standard C-CDA section; likely present but unconfirmed | Lab integration via Aspyra CyberLAB; unclear how much detail C-CDA captures |
| Imaging / diagnostic reports | ⚠️ Partial | Possibly in C-CDA results section; unconfirmed | Radiology orders via CPOE; report detail in C-CDA unclear |
| Procedures | ⚠️ Partial | Standard C-CDA section; likely present but unconfirmed | Perioperative detail (checklists, scheduling) unlikely in C-CDA |
| Clinical notes / documents | ⚠️ Partial | C-CDA can carry notes; attached PDFs may include scanned documents | Dynamic Form Engine structured data likely lost in C-CDA serialization |
| Care plans / goals | ⚠️ Partial | C-CDA can include care plan section; unconfirmed | Nursing care plans are a product feature; unclear if exported |
| Orders / referrals | ⚠️ Partial | Some orders may appear in C-CDA medication/procedure sections | Close-loop CPOE order lifecycle detail (statuses, timestamps) unlikely |
| Insurance / coverage | ❌ Not covered | No mention in documentation; C-CDA does not carry insurance data | Product stores insurance verification and pre-authorization data — **gap** |
| Claims / billing | ❌ Not covered | No mention in documentation; C-CDA cannot represent billing data | Product has extensive RCM module (charges, claims, remittance, denials, GL) — **major gap** |
| Payments | ❌ Not covered | No mention in documentation | Product handles credit card payments, remittance processing — **gap** |
| Consents / directives | ⚠️ Partial | C-CDA can include advance directives section; unconfirmed | Unclear if product stores consent data |
| Patient communications | ❌ Not covered | No mention in documentation | Patient portal via Bridge (third-party); data boundary unclear |
| Specialty: ED operations | ❌ Not covered | No mention of ED-specific data in export | ED tracking board data (ESI, disposition, turnaround times) — **gap** |
| Specialty: Perioperative | ❌ Not covered | No mention of perioperative data | Operative checklists, perioperative documentation — **gap** |

**Summary**: 0 domains are confirmed as fully covered. 12 domains are rated ⚠️ Partial based solely on the assumption that standard C-CDA sections may be populated — no documentation confirms this. 5 domains are rated ❌ Not covered because C-CDA structurally cannot represent the data (billing, insurance, payments, ED operations, perioperative detail).

## 6. Documentation Quality

The export documentation is among the weakest possible while still technically existing:

- **No data dictionary**: Zero entities, zero fields documented
- **No export instructions**: No information on how to initiate an export
- **No sample data**: No example C-CDA files or export ZIP structure
- **No schema**: No machine-readable specification
- **No C-CDA profile specification**: No indication of which templates or sections are used
- **Definitional padding**: 3 of 7 paragraphs are generic definitions of common file formats (ZIP, PDF, C-CDA) that add zero value
- **Provenance**: Created from "Microsoft Word - Export.docx" via "Print to PDF" — the minimal effort path

A developer cannot implement an import from this documentation. They would know to expect a ZIP with C-CDAs inside, but nothing about the content, structure, completeness, or specific elements of those C-CDAs. The only way to understand the export would be to obtain a sample export and reverse-engineer it.

**Could a developer build an import?** No. The documentation provides no actionable technical detail.

## 7. Overall Assessment

### Classification

**Minimal/stub**

The documentation is a single page with 9 sentences, 3 of which are definitions of common file formats. There is no data dictionary, no field-level documentation, no schema, no sample data, and no export instructions. The export itself appears to be a C-CDA-based clinical summary projection — a standard-based approach that structurally cannot represent the billing, revenue cycle, insurance, ED operational, and perioperative data that this comprehensive HIS stores. However, the documentation is so thin that even the C-CDA content cannot be confirmed.

### Key Findings

1. **The entire (b)(10) documentation is 9 sentences on a single page**, 3 of which are generic definitions of ZIP, PDF, and C-CDA file formats. This is among the thinnest documentation encountered. (`Strateq-Export.pdf`, 1 page, 282 KB)

2. **The export is C-CDA-based, not a native data model export.** StrateqEHR is a comprehensive HIS with extensive revenue cycle management, ED operations, perioperative, pharmacy/eMAR, and CPOE modules. C-CDA is a clinical summary standard that cannot represent billing, claims, insurance, payment, or operational data — all of which this product stores.

3. **Zero entities and zero fields are documented.** There is no data dictionary, no schema, no field definitions, and no C-CDA template/section specification. It is impossible to determine what specific data elements are included in the export.

4. **Revenue cycle data is entirely absent.** The product has a significant RCM module (Waystar integration, 3M CRS coding, claims, remittance, denials, GL journal entries, patient statements) — none of this can be represented in C-CDA and none is mentioned in the export documentation.

5. **No sample data or export instructions exist.** A recipient of this export would need to reverse-engineer the C-CDA documents to understand what data is present.

### Summary Stats

```
Classification:  Minimal/stub
Export format:   C-CDA (in ZIP archives) + attached files (PDF, images)
Model type:      Standard projection (C-CDA)
Entities:        0 (no data dictionary)
Fields:          0 (no field-level documentation)
Descriptions:    N/A
Sample data:     No
Bulk export:     Unclear
Domains covered: 0 of 17 confirmed; 12 partial (assumed from C-CDA standard); 5 not covered
```

### Bottom Line

StrateqEHR's EHI export documentation is a single page of near-empty prose that describes a C-CDA-based export with no data dictionary, no field definitions, and no technical detail. For a comprehensive hospital information system with extensive billing, ED, perioperative, and pharmacy modules, a C-CDA-only export structurally misses entire categories of patient data — particularly revenue cycle and operational data. This is a compliance checkbox, not a genuine effort to support patient data portability.
