# EHI Export Analysis: MedNet Medical Solutions

**Product**: emr4MD Version 9.10
**Analysis date**: 2026-02-15
**CHPL IDs**: 15.04.04.2796.emr4.09.00.1.191218 (CHPL ID 10214)

## 1. Product Context

emr4MD is a web-based ambulatory EHR by MedNet Medical Solutions (Webster, MA), part of the **4MD360** suite that bundles six components sharing a single database: emr4MD (clinical EHR), pm4MD (practice management/billing), eRx4MD (e-prescribing via DrFirst), patient4MD (patient portal), rcm4MD (revenue cycle management), and mu4MD (Meaningful Use consulting). The product targets small to medium-sized ambulatory practices, particularly solo and small internal medicine specialty practices. It was certified in December 2019 against 43 ONC 2015 Edition Cures Update criteria.

The product stores data across **clinical, administrative, financial, and patient-facing** domains: patient demographics, problem lists, medications, allergies, immunizations, vital signs, lab results (LabCorp/Quest integrations), clinical notes via customizable templates, family/social history, implantable devices, orders (medication/lab/imaging), care plans, e-prescribing history, appointment scheduling, charges, claims, payments (copays, ERA, EOB), patient statements, portal messages, and quality measure data. Key interoperability functions (FHIR APIs, C-CDA, Direct messaging, and the EHI export itself) are outsourced to EMR Direct via a required third-party subscription.

This product profile means a compliant b(10) export should cover clinical records, billing/financial data, e-prescribing, patient portal data, and specialty-specific clinical templates.

## 2. Artifacts Reviewed

| Artifact | Description | Informative? |
|---|---|---|
| `downloads/mednet-open-api-page.html` (18,238 bytes) | MedNet's registered Open API page. Contains product description and link to EMR Direct's FHIR STU3 API docs. **No b(10) EHI export content.** | ❌ Not relevant to b(10) |
| `downloads/interopengine-2017-open-api-documentation.html` (23,298 bytes) | EMR Direct Interoperability Engine 2017 — FHIR STU3 Ballot API covering 19 CCDS-mapped resource types. This is g(7)/g(9) documentation. | ❌ Not relevant to b(10) |
| `downloads/interopengine-2026-open-api-documentation.html` (41,219 bytes) | EMR Direct Interoperability Engine 2026 — FHIR R4 API with US Core IG 6.1, USCDI V3, 29 resource types, Bulk Data Access. This is g(10) documentation. | ❌ Not relevant to b(10) |
| `downloads/mednet-2015-cures-update.html` (48,159 bytes) | MedNet Cures Update page listing all 43 certified criteria, CQMs, and MIPS measures. Lists b(10) as a certified criterion with no link or documentation. | ⚠️ Confirms certification only |
| `downloads/Price_Transparency_emr4MD_v9.10.pdf` (956,711 bytes, 5 pages) | Price Transparency / Cost & Considerations document. Contains the **only** description of the b(10) export: one sentence. | ⚠️ Only b(10) artifact |
| `downloads/enrichment/api-documentation-extracted.json` (35,079 bytes) | Structured extraction of FHIR resource mappings from API docs + EHI export entry from PDF. | Useful for cross-referencing |
| `downloads/enrichment/coverage-accounting.json` (1,015 bytes) | Processing accounting for enrichment scripts. | Minimal |
| `downloads/enrichment/extract-api-docs.ts` (14,025 bytes) | Enrichment script source. | N/A |
| `downloads/enrichment/README.md` (1,854 bytes) | Documentation for enrichment scripts. | N/A |

**Most informative artifact**: `Price_Transparency_emr4MD_v9.10.pdf` — the sole source of any b(10) information.
**Least informative**: The four HTML pages, which exclusively document FHIR API (g-criteria), not EHI export.

## 3. Export Mechanics

Based on the sole available documentation (one sentence in the Price Transparency PDF):

- **Format**: Unknown. Not documented anywhere.
- **Mechanism**: Unknown. The PDF states the export allows "a practice to create individual and group exports of PHI without programming intervention," suggesting a UI-driven process. The EMR Direct subscription requirement suggests the export may route through EMR Direct's Interoperability Engine, but this is speculation.
- **Single-patient vs bulk**: Both implied — "individual and group exports."
- **Access constraints**: Requires an active EMR Direct subscription (separate from the base EHR subscription) with a one-time implementation fee and annual subscription. The export itself is "included in base service agreement."
- **No instructions exist** for how to initiate, receive, or interpret the export.

## 4. Export Content: What's In It

### What is documented

**Virtually nothing.** The entire b(10) EHI export documentation consists of this single sentence from the Price Transparency PDF (page 3):

> "This functionality allows a practice to create individual and group exports of PHI without programming intervention."

There is:
- **No data dictionary**
- **No field definitions**
- **No schema or format specification**
- **No entity/table listing**
- **No sample data**
- **No machine-readable artifacts**
- **No export instructions**
- **No description of what data domains are included**

### What the registered URL actually contains

The registered URL (`https://mednetmedical.com/Open_API.html`) — verified live on 2026-02-15 — contains exclusively g(7)/g(9) FHIR API documentation. It links to EMR Direct's Interoperability Engine 2017 documentation (FHIR STU3 Ballot), which covers 19 CCDS-mapped FHIR resource types. A newer 2026 version exists at interopengine.com (not linked from MedNet's page) covering 29 FHIR R4 resource types with US Core IG 6.1 and Bulk Data Access.

Neither MedNet's page nor EMR Direct's documentation contains any b(10) EHI export documentation. The vendor appears to have pointed their b(10) documentation URL at their g(7)/g(9) FHIR API page.

### Vendor's own content organization

No content organization can be presented because no data dictionary, schema, or content specification exists for the b(10) export.

### FHIR API resources (g-criteria only, NOT b(10))

For reference, the FHIR API documentation (which is **not** the b(10) export) covers:

**Interoperability Engine 2017 (FHIR STU3)**: AllergyIntolerance, CarePlan, CareTeam, Condition, Device, Goal, Immunization, MedicationStatement, Observation, Patient, Procedure — 11 unique clinical resource types covering CCDS data elements.

**Interoperability Engine 2026 (FHIR R4)**: AllergyIntolerance, Binary, CarePlan, CareTeam, Condition, Coverage, Device, DiagnosticReport, DocumentReference, Encounter, Endpoint, Goal, Group, Immunization, Location, Media, MedicationDispense, MedicationRequest, Observation, Organization, Patient, Person, Practitioner, PractitionerRole, Procedure, QuestionnaireResponse, RelatedPerson, ServiceRequest, Specimen — 29 resource types covering USCDI V3.

Even if the b(10) export were identical to the FHIR API output (which is not documented), it would cover only standard US Core clinical data and miss billing, financial, and specialty-specific data.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor provides **no documentation of b(10) export content**. There are no categories, no sections, no entities, no fields. The only statement is that "PHI" can be exported individually or in groups. It is impossible to assess coverage from the available documentation.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ❓ Unknown | No documentation | Product stores demographics (a)(5); gap cannot be assessed |
| Encounters / visits | ❓ Unknown | No documentation | Product stores encounters; gap cannot be assessed |
| Problems / conditions / diagnoses | ❓ Unknown | No documentation | Product stores problem lists; gap cannot be assessed |
| Medications / prescriptions | ❓ Unknown | No documentation | Product stores medications and e-prescribing data; gap cannot be assessed |
| Allergies | ❓ Unknown | No documentation | Product stores allergy lists; gap cannot be assessed |
| Immunizations | ❓ Unknown | No documentation | Product stores immunizations; gap cannot be assessed |
| Vitals | ❓ Unknown | No documentation | Product stores vital signs; gap cannot be assessed |
| Lab results | ❓ Unknown | No documentation | Product integrates with LabCorp/Quest; gap cannot be assessed |
| Imaging / diagnostic reports | ❓ Unknown | No documentation | Product supports diagnostic imaging orders; gap cannot be assessed |
| Procedures | ❓ Unknown | No documentation | Product stores procedures; gap cannot be assessed |
| Clinical notes / documents | ❓ Unknown | No documentation | Product stores clinical notes via customizable templates; gap cannot be assessed |
| Care plans / goals | ❓ Unknown | No documentation | Product has Disease Management Engine; gap cannot be assessed |
| Orders / referrals | ❓ Unknown | No documentation | Product supports CPOE for meds/labs/imaging; gap cannot be assessed |
| Insurance / coverage | ❓ Unknown | No documentation | Product stores insurance/eligibility data; gap cannot be assessed |
| Claims / billing | ❓ Unknown | No documentation | Product has full billing/claims via pm4MD; gap cannot be assessed |
| Payments | ❓ Unknown | No documentation | Product stores copays, ERA, EOB, payments; gap cannot be assessed |
| Patient communications / portal messages | ❓ Unknown | No documentation | Product has patient portal with secure messaging; gap cannot be assessed |
| Specialty-specific (internal medicine) | ❓ Unknown | No documentation | Product has customizable clinical templates; gap cannot be assessed |

**Note**: Every domain is marked "Unknown" because the vendor provides zero documentation of what the b(10) export contains. The product demonstrably stores data across all of these domains (per product-research.md and the vendor's own feature descriptions), but without any export documentation, it is impossible to determine which domains are covered.

## 6. Documentation Quality

The b(10) EHI export documentation is **effectively nonexistent**:

- **Data dictionary**: None
- **Field definitions**: None
- **Data types/value sets**: None
- **Relationships**: None
- **Sample data**: None
- **Schema files**: None
- **Export instructions**: None
- **Machine-readable artifacts**: None
- **Versioning**: None

A developer could not build an import from this documentation. A patient or provider could not understand what they would receive. The single sentence in the Price Transparency PDF — "This functionality allows a practice to create individual and group exports of PHI without programming intervention" — is the entirety of b(10) documentation.

The registered URL (`mednetmedical.com/Open_API.html`) points to g(7)/g(9) FHIR API documentation, which is a different certification criterion entirely. This appears to be a case of the vendor conflating their FHIR API docs with their EHI export documentation requirement.

The FHIR API documentation itself (provided by EMR Direct, not MedNet) is of reasonable quality for its purpose (g-criteria), but is irrelevant to the b(10) EHI export.

## 7. Overall Assessment

### Classification

**Minimal/stub**: Documentation is too thin to assess what the export contains. The entire b(10) documentation is a single sentence in a Price Transparency PDF. No data dictionary, no schema, no format specification, no sample data, no export instructions exist. The registered URL points to unrelated FHIR API documentation.

### Key Findings

1. **No b(10) export documentation exists.** The registered URL (`mednetmedical.com/Open_API.html`) contains exclusively g(7)/g(9) FHIR API documentation provided by third-party EMR Direct. The only mention of b(10) is a one-sentence description in the Price Transparency PDF (`Price_Transparency_emr4MD_v9.10.pdf`, page 3).

2. **The vendor conflates FHIR API docs with EHI export docs.** By registering their g(7)/g(9) FHIR API page as their b(10) documentation URL, the vendor appears to treat these as interchangeable. They are fundamentally different requirements — the FHIR API covers ~29 USCDI resource types, while b(10) requires export of all EHI.

3. **Export format is completely unknown.** The single sentence mentions "exports of PHI" but does not specify the format (FHIR, C-CDA, CSV, database dump, or otherwise). There is no way to determine what a recipient would actually receive.

4. **Critical third-party dependency.** The export requires an EMR Direct subscription with additional fees, suggesting the export mechanism runs through EMR Direct's infrastructure. Neither MedNet nor EMR Direct documents what the b(10) export produces.

5. **Product stores substantial data that should be in a b(10) export.** The 4MD360 suite includes clinical, billing, e-prescribing, patient portal, and revenue cycle management modules sharing a single database — a broad data footprint with zero documented export coverage.

### Summary Stats

```
Classification:  Minimal/stub
Export format:   Unknown (not documented)
Model type:      Unknown (not documented)
Entities:        N/A (no data dictionary)
Fields:          N/A (no data dictionary)
Descriptions:    N/A
Sample data:     No
Bulk export:     Unclear (mentions "group exports")
Domains covered: 0 of 17 assessable (coverage unknown due to absent documentation)
```

### Bottom Line

MedNet Medical Solutions provides no meaningful b(10) EHI export documentation. The registered URL points to unrelated FHIR API docs, and the only b(10) mention is a single sentence in a pricing PDF. A patient, provider, or developer receiving this export would have no way to know what format it comes in, what data it contains, or how to interpret it. This is a textbook compliance checkbox — the vendor obtained b(10) certification but published no documentation for the export.
