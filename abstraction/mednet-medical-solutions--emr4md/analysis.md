# EHI Export Analysis: MedNet Medical Solutions

**Product**: emr4MD Version 9.10  
**Analysis date**: 2026-02-16  
**CHPL ID**: 15.04.04.2796.emr4.09.00.1.191218

## 1. Product Context

emr4MD is a web-based ambulatory EHR for small to medium-sized practices, developed by MedNet Medical Solutions (Webster, MA). It is part of the **4MD360 suite**, which bundles six components sharing a single database: emr4MD (EHR), pm4MD (practice management/billing/scheduling), eRx4MD (e-prescribing via DrFirst), patient4MD (patient portal), rcm4MD (revenue cycle management), and mu4MD (meaningful use consulting).

The product stores clinical data (problems, medications, allergies, immunizations, vitals, labs, procedures, clinical notes, family/social history, implantable devices, care plans), billing/financial data (charges, claims, payments, copays, ERA, EOBs, patient statements), e-prescribing data, patient portal messages and requests, quality measure data, and scanned documents. The practice management module shares the same database as the EHR, meaning billing data is co-located with clinical data.

Key third-party dependencies: **EMR Direct** provides interoperability (FHIR APIs, Direct messaging, C-CDA, and reportedly the EHI export) and **DrFirst** provides e-prescribing. Both require separate subscriptions.

The product has an extremely small market presence — zero reviews on Capterra, G2, or SourceForge — suggesting a very limited user base.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/Price_Transparency_emr4MD_v9.10.pdf` (957 KB, 5 pages) | Price Transparency / Cost & Considerations document. Contains the **only** mention of (b)(10) EHI export anywhere: a single sentence. Revised 2024-Jul-12. | **Most informative** for (b)(10) — but contains only 1 sentence |
| `downloads/mednet-open-api-page.html` (18 KB) | Registered EHI documentation URL. Contains Open API info for g(7)/g(9) FHIR STU3 API. **No mention of (b)(10) EHI export at all.** Last updated Dec 13, 2023. | Low — wrong criterion |
| `downloads/interopengine-2026-open-api-documentation.html` (41 KB) | EMR Direct InteropEngine 2026 API docs. FHIR R4, US Core 6.1.0, USCDI V3, 29 resource types. This is g(10) documentation. | Moderate — shows g(10) scope but irrelevant to b(10) |
| `downloads/interopengine-2017-open-api-documentation.html` (23 KB) | EMR Direct InteropEngine 2017 API docs. FHIR STU3, 20 CCDS elements. Linked from the registered URL. | Low — older API docs, not b(10) |
| `downloads/mednet-2015-cures-update.html` (48 KB) | ONC Certified HIT / Cures Update listing 43 certified criteria. Lists (b)(10) as certified but provides zero documentation or links. | Low — confirms certification only |
| `downloads/enrichment/api-documentation-extracted.json` (35 KB) | Structured extraction of API docs and price transparency info. | Useful for confirming resource counts |

## 3. Export Mechanics

- **Format**: Unknown. No documentation specifies the export format.
- **Mechanism**: Unknown. The Price Transparency PDF says the export "allows a practice to create individual and group exports of PHI without programming intervention," suggesting a UI-based mechanism.
- **Single-patient vs bulk**: Both individual and group exports are mentioned.
- **Third-party dependency**: Requires EMR Direct subscription (separate implementation fee + annual subscription).
- **Access constraints**: Costs include "base service agreement subscription fee" plus EMR Direct third-party fees.

The Price Transparency PDF is the sole source for all of the above. No instructions, screenshots, or technical details exist anywhere.

## 4. Export Content: What's In It

### What documentation exists

**None.** There is no data dictionary, no schema, no field definitions, no sample data, no format specification, and no export instructions for the (b)(10) EHI export.

The entirety of the (b)(10) documentation is this single sentence from the Price Transparency PDF (page 3):

> "This functionality allows a practice to create individual and group exports of PHI without programming intervention."

### What the g(10) API covers (separate system, not b(10))

For reference only, the EMR Direct InteropEngine 2026 g(10) API supports 29 FHIR R4 resource types conforming to US Core 6.1.0 / USCDI V3:

AllergyIntolerance, Binary, CarePlan, CareTeam, Condition, Coverage, Device, DiagnosticReport, DocumentReference, Encounter, Endpoint, Goal, Group, Immunization, Location, Media, MedicationDispense, MedicationRequest, Observation, Organization, Patient, Person, Practitioner, PractitionerRole, Procedure, QuestionnaireResponse, RelatedPerson, ServiceRequest, Specimen.

These are standard USCDI-scope clinical resources. They do not include billing, claims, payments, scheduling, portal messages, or any product-specific data.

### Vendor's own content organization

No vendor-provided content organization exists. There is no data dictionary to parse.

| Entity/Table | Fields | Described | Types | Category |
|---|---|---|---|---|
| *(none documented)* | — | — | — | — |

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor covers **nothing documentable** for (b)(10). The single sentence in the Price Transparency PDF confirms a feature exists but provides zero detail about what data is exported. There is no way to assess coverage from the available documentation.

The g(10) API (a separate system via EMR Direct) covers standard USCDI V3 clinical resources — 29 FHIR resource types. This is clinical exchange functionality, not EHI export.

### 5b. Standardized domain coverage (top-down)

Since no (b)(10) documentation exists, all domains are assessed as "Undetermined" — not "Not covered," because the export feature reportedly exists but is entirely undocumented.

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ❓ Undetermined | No b(10) docs; g(10) has Patient resource | Product stores demographics; cannot verify b(10) coverage |
| Encounters / visits | ❓ Undetermined | No b(10) docs; g(10) has Encounter | Product stores encounters; cannot verify |
| Problems / conditions | ❓ Undetermined | No b(10) docs; g(10) has Condition | Product stores problem lists; cannot verify |
| Medications / prescriptions | ❓ Undetermined | No b(10) docs; g(10) has MedicationRequest | Product stores medications; cannot verify |
| Allergies | ❓ Undetermined | No b(10) docs; g(10) has AllergyIntolerance | Product stores allergies; cannot verify |
| Immunizations | ❓ Undetermined | No b(10) docs; g(10) has Immunization | Product stores immunizations; cannot verify |
| Vitals | ❓ Undetermined | No b(10) docs; g(10) has Observation | Product stores vitals; cannot verify |
| Lab results | ❓ Undetermined | No b(10) docs; g(10) has Observation, DiagnosticReport | Product integrates with LabCorp/Quest; cannot verify |
| Imaging / diagnostic reports | ❓ Undetermined | No b(10) docs; g(10) has DiagnosticReport | Product supports imaging orders; cannot verify |
| Procedures | ❓ Undetermined | No b(10) docs; g(10) has Procedure | Product stores procedures; cannot verify |
| Clinical notes / documents | ❓ Undetermined | No b(10) docs; g(10) has DocumentReference | Product has clinical templates; cannot verify |
| Care plans / goals | ❓ Undetermined | No b(10) docs; g(10) has CarePlan, Goal | Product stores care plans; cannot verify |
| Orders / referrals | ❓ Undetermined | No b(10) docs; g(10) has ServiceRequest | Product supports CPOE; cannot verify |
| Insurance / coverage | ❓ Undetermined | No b(10) docs; g(10) has Coverage | Product stores insurance info; cannot verify |
| Claims / billing | ❓ Undetermined | **No evidence in g(10) API** | Product has full billing (pm4MD, rcm4MD); likely gap if export is g(10)-based |
| Payments | ❓ Undetermined | **No evidence in g(10) API** | Product stores copays, ERA, EOBs; likely gap if export is g(10)-based |
| Patient communications / portal messages | ❓ Undetermined | **No evidence in g(10) API** | Product has patient portal (patient4MD); likely gap if export is g(10)-based |
| Specialty-specific data | ❓ Undetermined | No b(10) docs | Product has disease management engine, custom templates; cannot verify |
| Consents / directives | ❓ Undetermined | No b(10) docs | Cannot verify |

**Key observation**: If the (b)(10) export is simply the g(10) FHIR API repackaged (which the EMR Direct dependency and lack of separate documentation strongly suggest), then billing, payments, portal messages, and specialty data would all be absent — these are domains the product actively stores via pm4MD, rcm4MD, and patient4MD.

## 6. Documentation Quality

The (b)(10) EHI export documentation quality is **effectively zero**:

- **No data dictionary** — not even a list of what data types are exported
- **No schema or format specification** — the export format is completely unknown
- **No field definitions** — zero fields documented
- **No sample data** — no examples of what exported data looks like
- **No export instructions** — no guidance on how to initiate or receive the export
- **No machine-readable artifacts** — no schema files, no OpenAPI specs for b(10)
- **No value sets or terminology documentation**

A developer could not build an import from this documentation. A patient could not understand what data they would receive. The registered EHI documentation URL (mednetmedical.com/Open_API.html) does not even mention (b)(10) — it exclusively covers the g(7)/g(9) FHIR API.

The g(10) API documentation (via EMR Direct) is reasonable quality for its purpose — FHIR R4 resource types, search parameters, authentication — but this is irrelevant to the (b)(10) requirement.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Minimal/stub/unclear**

Documentation is far too thin to assess coverage. The entire (b)(10) documentation is a single sentence: "This functionality allows a practice to create individual and group exports of PHI without programming intervention." There is no data dictionary, no schema, no format, no field list — nothing that would allow anyone to determine what data is actually exported. The product has significant data breadth (clinical + billing + portal + e-prescribing) via its 4MD360 suite sharing a single database, but zero evidence exists that the export covers any of it in any documented way.

**Axis 2 — Export approach: Unclear/undetermined**

The export requires an EMR Direct subscription, and the registered URL points to EMR Direct's g(7)/g(9) API documentation rather than any (b)(10)-specific documentation. This strongly suggests the (b)(10) export may be a repackaging of the g(10) FHIR API or C-CDA exchange, but without documentation, this cannot be confirmed. The mention of "individual and group exports of PHI without programming intervention" is compatible with either a purpose-built export or a relabeled g(10) bulk export. The most telling signal is the complete absence of any b(10)-specific documentation separate from the g(10) API docs — vendors who build purpose-built exports typically document them.

### Key Findings

1. **Zero (b)(10) documentation exists.** The registered EHI documentation URL contains no mention of (b)(10) EHI export — it points exclusively to g(7)/g(9) FHIR API documentation from a third-party partner (EMR Direct). The only evidence of a (b)(10) feature is a single sentence in the Price Transparency PDF (`Price_Transparency_emr4MD_v9.10.pdf`, page 3).

2. **Export format is completely unknown.** No documentation specifies whether the export produces FHIR, C-CDA, CSV, database dump, or any other format. No schema, sample data, or structural description exists.

3. **The EMR Direct dependency is a red flag.** The (b)(10) export requires the same third-party subscription (EMR Direct) as the g(7)/g(9)/g(10) FHIR API, suggesting the export likely leverages the same interoperability infrastructure — which covers only USCDI-scope clinical data, not billing, payments, or portal data.

4. **Significant product data would be missing if export is g(10)-based.** emr4MD's 4MD360 suite includes practice management (pm4MD), revenue cycle management (rcm4MD), and a patient portal (patient4MD) — all sharing a single database. The g(10) API's 29 FHIR resources cover none of these domains.

5. **This is a textbook compliance checkbox.** The vendor obtained (b)(10) certification but appears to have invested zero effort in documenting the export. The registered URL is mismatched (points to g(7)/g(9) docs), no data dictionary exists, and the only description is boilerplate in a price transparency document.

### Summary Stats

    Coverage:        Minimal/stub/unclear
    Approach:        Unclear/undetermined
    Export format:   Unknown
    Entities:        N/A (no data dictionary)
    Fields:          N/A
    Descriptions:    N/A
    Sample data:     No
    Bulk export:     Unclear (mentions "group exports")
    Domains covered: 0 of 17 applicable domains confirmed (all undetermined)

### Bottom Line

emr4MD's (b)(10) EHI export is a certification with no substantive documentation behind it. A patient requesting their data would have no way to know what they'll receive, in what format, or whether it includes their billing records, portal messages, or specialty data. The single biggest issue is the complete absence of any documentation — not thin documentation, not bad documentation, but literally none.
