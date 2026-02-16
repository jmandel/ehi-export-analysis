# EHI Export Analysis: StreamlineMD, LLC

**Product**: StreamlineMD EHR (Version 15.0)
**Analysis date**: 2026-02-16
**CHPL IDs**: 15.04.04.2383.Stre.15.00.1.190417 (CHPL ID 9974)

## 1. Product Context

StreamlineMD EHR is a cloud-based, ONC-certified ambulatory EHR and Practice Management (PM) platform purpose-built for interventional radiology and imaging specialists. It is a wholly owned subsidiary of PRC Medical, LLC, serving practices in 42 states. The product's core value proposition is a **tightly integrated EHR and billing/RCM workflow** where "coding, charge capture, documentation, and inventory usage automatically flow into billing."

Key data domains the product stores:

- **Clinical documentation**: 500+ endovascular/interventional procedure templates, nurse notes, procedure drawing tool, AI-powered documentation
- **Billing/revenue cycle**: CPT/ICD-10 coding, charge capture, claims submission, payment posting, denials management, patient payment estimator, online bill-pay
- **Prior authorization**: Tracking, documentation, and status management
- **Scheduling**: Enterprise scheduling, patient tracking
- **Inventory management**: Device and supply tracking for interventional procedures (catheters, stents, etc.)
- **E-prescribing**: Medication/prescription management
- **Patient engagement**: Patient portal with secure messaging, test results, appointment scheduling
- **Referral management**: Referring/referred provider tracking
- **Imaging integration**: PACS/DICOM integration (references/metadata; actual images in separate PACS)
- **Quality reporting**: CQM/MIPS reporting data, performance benchmarking

This is a specialty EHR with deeply integrated billing — billing is not a separate module but a core differentiator. Any genuine (b)(10) export should cover clinical data, billing/claims, inventory, prior authorizations, and specialty procedure data.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/StreamlineMD-EHR-EHI-Export.pdf` | 2-page PDF (155 KB), created Oct 30, 2023 by Smitesh Shah in Microsoft Word. Page 1: title page. Page 2: company description + 3 bullet points describing C-CDA/PDF export using USCDI v1. | **Low** — contains no data dictionary, no schema, no field definitions, no sample data, no export instructions. The entirety of the technical content is 3 bullet points. |

**Only one artifact exists.** There are no additional data dictionaries, schemas, sample exports, or supplementary documentation in the downloads folder. The FHIR API documentation at `patientportal.streamlinemd.com` documents the (g)(10) API, not the (b)(10) export, and was not included in the collection (correctly).

## 3. Export Mechanics

- **Format**: C-CDA documents and/or PDF, per user selection
- **Mechanism**: UI-based export ("without the intervention of software developers"); user selects destination folder
- **Scope**: Single patient, multiple patients, or entire patient population
- **Access constraints**: Not documented; no mention of fees, special permissions, or turnaround time
- **Standard**: C-CDA conforming to USCDI v1 data classes (per explicit documentation statement with link to healthit.gov USCDI v1 page)

## 4. Export Content: What's In It

### What the documentation says

The documentation's only content specification is: "C-CDA United States Core Data for Interoperability (USCDI v1) requirements." There is no product-specific data dictionary, no field mapping, no schema, and no description of what StreamlineMD-specific data elements are included or excluded.

USCDI v1 defines these data classes:
- Patient Demographics/Information
- Problems
- Medications
- Medication Allergies
- Laboratory Tests/Values/Results
- Vital Signs
- Procedures
- Care Team Members
- Immunizations
- Unique Device Identifiers
- Assessment and Plan of Treatment
- Goals
- Health Concerns
- Smoking Status
- Clinical Notes (Consultation, Discharge Summary, H&P, Imaging Narrative, Lab Report, Pathology, Procedure, Progress)
- Provenance

### What the documentation does NOT say

There is zero information about:
- Which specific fields within each USCDI data class are populated
- How StreamlineMD-specific data (e.g., interventional procedure templates, procedure drawings) maps to C-CDA sections
- Whether any data beyond USCDI v1 is included
- Any billing, claims, inventory, prior authorization, or referral data

### Vendor's own content organization

No vendor-specific content organization exists. The only categorization is a blanket reference to "USCDI v1." No entities, tables, or fields are defined.

| Entity/Table | Fields | Described | Types | Category (vendor's) |
|---|---|---|---|---|
| *(none defined)* | — | — | — | — |

**Total entities: 0. Total fields: 0. Fields with descriptions: 0.**

The complete (empty) entity inventory is saved in `analysis/entity-inventory-full.json`.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor provides no product-specific content description. The only claim is conformance to "USCDI v1 requirements" via C-CDA export. This covers the 17 USCDI v1 data classes listed above — a clinical summary standard originally designed for transitions of care, not for comprehensive EHI export.

The C-CDA format itself is inherently limited to clinical summary data. It cannot represent:
- Billing/claims records
- Inventory/supply data
- Prior authorization workflows
- Specialty-specific structured data (procedure drawings, interventional templates)
- Patient portal messaging threads
- Referral tracking workflows

Even within clinical domains, C-CDA USCDI v1 captures only a standardized subset — the EHR likely stores far more detail per clinical encounter than what maps to C-CDA sections.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | Implied by USCDI v1 "Patient Demographics" class; no field-level detail | Product stores demographics; USCDI v1 covers basics but C-CDA demographics are limited vs. full registration data |
| Encounters / visits | ⚠️ Partial | Not a named USCDI v1 class; some encounter context in C-CDA sections | Product schedules/tracks encounters; C-CDA has limited encounter representation |
| Problems / conditions | ⚠️ Partial | Implied by USCDI v1 "Problems" class | Covered at USCDI level; depth unknown |
| Medications / prescriptions | ⚠️ Partial | Implied by USCDI v1 "Medications" class | Product has e-prescribing; USCDI v1 covers medication lists but not full Rx history detail |
| Allergies | ⚠️ Partial | Implied by USCDI v1 "Medication Allergies" class | Basic coverage likely |
| Immunizations | ⚠️ Partial | Implied by USCDI v1 "Immunizations" class | Basic coverage likely |
| Vitals | ⚠️ Partial | Implied by USCDI v1 "Vital Signs" class | Basic coverage likely |
| Lab results | ⚠️ Partial | Implied by USCDI v1 "Laboratory Tests/Values/Results" | Product integrates lab orders/results; USCDI level likely captures results but not full order workflow |
| Imaging / diagnostic reports | ⚠️ Partial | USCDI v1 "Imaging Narrative" clinical note type | Product has deep PACS/DICOM integration; C-CDA can carry narrative but not structured imaging data/references |
| Procedures | ⚠️ Partial | Implied by USCDI v1 "Procedures" class | Product has 500+ interventional procedure templates and a procedure drawing tool; C-CDA procedure sections capture a fraction of this specialty data |
| Clinical notes / documents | ⚠️ Partial | Implied by USCDI v1 "Clinical Notes" (8 types) | C-CDA carries note text; specialty-specific structured data likely lost |
| Care plans / goals | ⚠️ Partial | Implied by USCDI v1 "Goals" and "Assessment and Plan" | Basic coverage likely |
| Orders / referrals | ❌ Not covered | No mention in documentation; not a USCDI v1 class | Product has referral management; significant gap |
| Insurance / coverage | ❌ Not covered | No mention in documentation | Product stores insurance info for billing; gap |
| Claims / billing | ❌ Not covered | No mention in documentation | **Product's core differentiator is integrated billing/RCM** — charges, claims, payments, denials, CPT/ICD-10 coding. Major gap. |
| Payments | ❌ Not covered | No mention in documentation | Product has payment posting, patient bill-pay; gap |
| Prior authorizations | ❌ Not covered | No mention in documentation | Product has prior auth tracking; gap |
| Inventory / supply tracking | ❌ Not covered | No mention in documentation | Product tracks device/supply inventory per procedure; gap |
| Patient communications | ❌ Not covered | No mention in documentation | Product has patient portal with secure messaging; gap |
| Specialty-specific (interventional radiology) | ❌ Not covered | No mention of procedure drawings, interventional templates, or specialty data beyond C-CDA | Product has 500+ endovascular/interventional procedure templates and a procedure drawing tool; major gap |
| Consents / directives | ❌ Not covered | No mention in documentation | Unknown if product stores these |

**Summary**: Of ~19 applicable domains, USCDI v1 C-CDA covers approximately 12 at a partial/surface level (clinical summary data only). At least 7 significant domains are completely absent — most critically billing/RCM (the product's core differentiator), specialty interventional procedure data, prior authorizations, and inventory management.

## 6. Documentation Quality

The documentation is among the most minimal possible while technically existing:

- **Completeness**: 3 bullet points on a single page. No data dictionary, no field definitions, no schema, no sample data, no screenshots, no export instructions.
- **Developer usability**: A developer could not build an import from this documentation. The only actionable information is "it outputs C-CDA conforming to USCDI v1" — which tells you only what any generic C-CDA consumer already knows.
- **Machine-readable artifacts**: None. No schemas, no sample C-CDA documents, no JSON/XML specifications.
- **Specificity**: Zero product-specific detail. The documentation could apply to any C-CDA-capable EHR — nothing identifies what StreamlineMD-specific data elements are included or how they map.

This documentation does not meet even a minimal standard for transparency about what data is exported.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Minimal/stub/unclear**

The documentation explicitly states the export covers only "USCDI v1 requirements" via C-CDA — a clinical summary standard covering approximately 17 data classes of basic clinical information. For a product whose core value proposition is tightly integrated billing/RCM with 500+ specialty procedure templates, this represents a small fraction of the designated record set. Billing, claims, payments, prior authorizations, inventory, specialty procedure data (drawings, templates), patient portal communications, and referral workflows are all absent. The documentation is too thin to assess whether the actual C-CDA export even covers USCDI v1 completely, but even at best, USCDI v1 is a regulatory floor for clinical exchange, not a comprehensive EHI export.

**Axis 2 — Export approach: Repackaged existing export**

This is a textbook case of repackaging an existing clinical exchange export as (b)(10). The telltale signs are all present:
1. The documentation explicitly references "USCDI v1 requirements" with a link to healthit.gov — this is the standard for clinical summaries/transitions of care, not EHI export.
2. The export format is C-CDA, which is the same format used for (b)(1)/(b)(2) Transitions of Care requirements that StreamlineMD is also certified for.
3. There is no product-specific data dictionary, no mapping beyond the generic C-CDA standard, and no mention of any data domain beyond what USCDI v1 covers.
4. The product is certified for (b)(1), (b)(2), and (b)(3) — all transitions-of-care criteria that use C-CDA. The (b)(10) documentation describes the same C-CDA export capability.

The vendor appears to have pointed to their existing C-CDA transitions-of-care export and relabeled it as their (b)(10) EHI export.

### Key Findings

1. **The entire EHI export documentation is 3 bullet points on a single page** (`StreamlineMD-EHR-EHI-Export.pdf`, page 2). No data dictionary, no schema, no field definitions, no sample data exist. This is among the most minimal (b)(10) documentation possible.

2. **The export is explicitly limited to USCDI v1 via C-CDA** — the vendor's own documentation says "C-CDA United States Core Data for Interoperability (USCDI v1) requirements." This is the transitions-of-care clinical summary standard, not a comprehensive EHI export.

3. **Billing/RCM — the product's core differentiator — is completely absent.** StreamlineMD's value proposition is tightly integrated billing where "coding, charge capture, documentation, and inventory usage automatically flow into billing." None of this data (charges, claims, payments, denials, CPT codes) appears in the export.

4. **Specialty clinical data is absent.** The product stores 500+ endovascular/interventional procedure templates and has a procedure drawing tool for visual documentation. None of this specialty-specific structured data is mentioned in the export documentation or representable in standard C-CDA.

5. **The PDF export option adds no additional data coverage.** The PDF format likely renders the same C-CDA clinical summary content as a human-readable document — it does not expand the data domains covered.

### Summary Stats

```
Coverage:        Minimal/stub/unclear
Approach:        Repackaged existing export
Export format:   C-CDA, PDF
Entities:        0 (no data dictionary provided)
Fields:          0 (no field definitions provided)
Descriptions:    N/A
Sample data:     No
Bulk export:     Yes (single, multiple, or all patients)
Domains covered: ~12 of 19 applicable domains at partial/surface level via USCDI v1; 0 with verified depth
```

### Bottom Line

A patient or provider requesting their complete health record from StreamlineMD would receive a C-CDA clinical summary covering basic USCDI v1 data classes — a useful clinical snapshot but far from a complete copy of their designated record set. The most significant gap is the complete absence of billing and revenue cycle data from a product whose defining feature is integrated billing/RCM. The 3-bullet-point documentation provides no transparency about what is or isn't included, making it impossible to independently verify export completeness.
