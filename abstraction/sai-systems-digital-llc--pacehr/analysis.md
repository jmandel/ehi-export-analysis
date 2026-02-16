# EHI Export Analysis: Sai Systems Digital LLC

**Product**: PacEHR v20
**Analysis date**: 2026-02-16
**CHPL IDs**: 15.04.04.3137.Pace.20.00.1.221229

## 1. Product Context

PacEHR is a cloud-based EHR designed specifically for post-acute long-term care (PALTC) practitioners — physicians, nurse practitioners, and APRNs who provide bedside services in skilled nursing facilities (SNFs), assisted living, rehabilitation centers, and home health settings. It is built by Saisystems Health, a division of Saisystems International (Shelton, CT).

PacEHR is part of the "TheSNFist® Suite" which bundles the EHR with:
- **billEHR®** — mobile point-of-care charge capture
- **SNFConnect** — practice communication system
- **navigatEHR** — business intelligence dashboards
- Revenue cycle management, medical coding/billing, and credentialing services

**Key architectural point**: PacEHR targets *visiting practitioners*, not the SNF facilities themselves. The facility typically runs its own EHR (often PointClickCare). PacEHR stores the practitioner's encounter documentation and billing data for visits, integrating with PointClickCare for patient context.

**Data the product stores** (relevant for export completeness assessment):
- Clinical encounter notes with template-driven documentation, voice-to-text, and customizable macros
- Medication orders / CPOE / e-prescribing
- Diagnoses/problems, allergies, immunizations
- Implantable device list
- Billing codes and charge capture (integrated billing via billEHR)
- Claims management
- Patient demographics
- Scheduling/appointments
- Document management
- Quality measure / MIPS reporting data
- Patient portal messaging
- Practice communications (SNFConnect)

This is a niche product with a small user base (only 4 third-party reviews found). It was launched in 2021 and certified 12/29/2022.

## 2. Artifacts Reviewed

| Artifact | Size | Description | Informativeness |
|---|---|---|---|
| `pacehr-ehi-main-page.html` | 140 KB | Main EHI export page at saisystems.com/health/pacehr-ehi/. ~150 words of substantive content describing EHI export capability at a high level. No data dictionary, no schema, no field-level documentation. | **Low** — marketing-level description only |
| `cures-update-fhir-api-docs.html` | 189 KB | FHIR API documentation at thesnfist.com/cures-update/. Documents 16 standard US Core FHIR resources with API endpoints and USCDI data element mappings. This is (g)(10) documentation, not (b)(10)-specific. | **Most informative** — the only technical documentation |
| `compliance-certificate-pacehr-v20.pdf` | 266 KB | 1-page Drummond Group ONC certification certificate. Confirms (b)(10) certification along with other criteria. | **Low** — confirms certification only |
| `screenshot-ehi-main-page.png` | 652 KB | Full-page screenshot of the EHI page | Confirms page rendering |
| `screenshot-cures-update-fhir-api-docs.png` | 3.5 MB | Full-page screenshot of the FHIR API docs | Confirms page rendering |

**Total artifacts**: 5 files. No data dictionary, no schema, no sample data, no export-specific documentation.

## 3. Export Mechanics

- **Format**: Described as "machine readable XML formats" on the EHI page. The linked FHIR API documents JSON (`application/fhir+json`). This is contradictory — the EHI page says XML, the FHIR API says JSON. Likely the export uses FHIR JSON via the documented API.
- **Mechanism**: The EHI page states the export "utilizes PacEHR's APIs that foster interoperability" and links to the FHIR API documentation. This is an API-based export, not a UI download or database dump.
- **Single-patient vs bulk**: The EHI page describes both: "Bulk EHI export enables export of all patient data belonging to a practice, provider, medical group, or department" and "Single/multi-patient export is useful when patients request their health information." The product is certified for (b)(11) bulk FHIR export.
- **Access**: Customers are directed to "reach out to their dedicated Customer Success Manager" for integration details. No self-service export mechanism is documented.

## 4. Export Content: What's In It

There is **no data dictionary** for the EHI export. The only technical documentation is the FHIR API specification, which documents 16 standard FHIR resource types with 74 USCDI data elements across 28 API endpoints. No field-level descriptions, no types beyond what FHIR defines by default, no value sets, no relationships, and no sample data are provided.

### Vendor's own content organization

The FHIR API documentation organizes content by FHIR resource type, mapping each to USCDI data elements. There are no vendor-specific categories — this is standard US Core mapping.

| Resource Type | USCDI Data Elements | USCDI Version | Category |
|---|---|---|---|
| AllergyIntolerance | 3 (Substance Drug Class, Substance Medication, Reaction) | v1 | Allergies |
| CarePlan | 1 (Assessment and Plan of Treatment) | v1 | Care Plans |
| CareTeam | 6 (Team, Member Name/Identifier/Role/Location/Telecom) | v1/v2 | Care Team |
| Condition | 2 (Health Concern, Problems) | v1 | Problems |
| Device | 1 (Unique Device Identifier) | v1 | Devices |
| DocumentReference | 8 (Consultation, Discharge Summary, H&P, Procedure, Progress, Imaging, Lab Report, Pathology Report notes) | v1 | Clinical Notes |
| Encounter | 5 (Type, Diagnosis, Time, Location, Disposition) | v2 | Encounters |
| Goal | 1 (Goals) | v1 | Goals |
| Immunization | 1 (Immunization) | v1 | Immunizations |
| Location | 5 (Facility, NPI, Status, Address, Telecom) | v1 | Facility Info |
| Medication | 1 (Medications) | v1 | Medications |
| MedicationRequest | 1 (Medications) | v1 | Medications |
| Observation | 15 (Labs, Vitals × 11, Smoking Status, pediatric percentiles) | v1 | Labs/Vitals |
| Patient | 14 (Name fields, Sex, Sexual Orientation, Gender Identity, DOB, Race, Ethnicity, Language, Address, Phone) | v1/v2 | Demographics |
| Practitioner | 9 (Role, Name, DOB, NPI, Status, Address, Telecom) | v1 | Providers |
| Procedure | 1 (Procedures) | v1 | Procedures |

**Total**: 16 resource types, 74 USCDI data elements, 28 endpoints. Zero vendor-specific fields or extensions. Zero fields with product-specific descriptions. This is an exact reproduction of the standard US Core/USCDI resource set.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor's documentation covers exactly the USCDI v1/v2 data element set mapped to standard FHIR resources. There are no vendor-specific additions, no extensions beyond US Core, and no mapping of PacEHR-specific data concepts.

The documentation is organized as a FHIR API reference — each resource type has endpoint documentation (GET by id, search parameters) and a list of the USCDI data elements it maps to. This is functionally identical to what would be expected for a (g)(10) standardized API implementation.

The EHI page itself is extremely thin (~150 words of substantive content), describes two export modes (bulk and single/multi-patient), and links to the FHIR API documentation as the export mechanism. It offers no additional coverage beyond the FHIR API.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | Patient resource with 14 USCDI elements (name, DOB, race, ethnicity, sex, address, phone, language) | Standard USCDI demographics only; no insurance/enrollment data elements |
| Encounters / visits | ⚠️ Partial | Encounter resource with 5 elements (type, diagnosis, time, location, disposition) | Basic encounter metadata; no encounter-specific billing, facility census, or template-driven note structure |
| Problems / conditions | ✅ Covered | Condition resource (Health Concern, Problems) | Standard USCDI coverage |
| Medications / prescriptions | ✅ Covered | Medication + MedicationRequest resources | Standard USCDI coverage; PacEHR has CPOE and e-prescribing |
| Allergies | ✅ Covered | AllergyIntolerance resource (3 elements) | Standard USCDI coverage |
| Immunizations | ✅ Covered | Immunization resource | Standard USCDI coverage |
| Vitals | ✅ Covered | Observation resource (11 vital sign types + pediatric percentiles) | Standard USCDI coverage |
| Lab results | ⚠️ Partial | Observation resource (Laboratory Tests, Values/Results) | Standard USCDI; product may have limited lab capability per user reviews |
| Procedures | ✅ Covered | Procedure resource | Standard USCDI coverage |
| Clinical notes / documents | ⚠️ Partial | DocumentReference with C-CDA encoding for 8 note types | Notes exported as C-CDA summaries, not native template-driven encounter documentation — PacEHR's core value prop is rich template/macro-based notes |
| Care plans / goals | ✅ Covered | CarePlan + Goal resources | Standard USCDI coverage |
| Care teams | ✅ Covered | CareTeam resource (6 elements) | Standard USCDI v2 coverage |
| Devices | ✅ Covered | Device resource (implantable devices) | Standard USCDI coverage |
| Insurance / coverage | ❌ Not covered | No Coverage or related resources | Product handles billing/claims; insurance data likely stored but not exported |
| Claims / billing | ❌ Not covered | No Claim, ChargeItem, or billing resources | **Significant gap** — PacEHR integrates billing, charge capture (billEHR), and claims management. This is core product functionality completely absent from the export. |
| Payments | ❌ Not covered | No payment-related resources | Product offers RCM services; payment data likely exists |
| Orders / referrals | ❌ Not covered | No ServiceRequest or referral resources | Product is used for referrals in PALTC settings |
| Patient communications | ❌ Not covered | No Communication resources | Product has patient portal and SNFConnect communication system |
| Specialty-specific (PALTC) | ❌ Not covered | No PALTC-specific data elements | PacEHR is designed for PALTC — facility census, multi-facility tracking, place-of-service coding are core features with no export representation |
| Imaging / diagnostic reports | ⚠️ Partial | DiagnosticReport mentioned alongside DocumentReference | Product is not certified for imaging CPOE; limited applicability |
| Consents / directives | ❌ Not covered | No Consent resources | N/A — no evidence product manages consents |

## 6. Documentation Quality

The EHI export documentation is **extremely thin** — among the thinnest possible while still having a page at the registered URL.

- **No data dictionary**: No field-level documentation of any kind exists for the export.
- **No schema**: No XSD, JSON Schema, or other machine-readable format specification.
- **No sample data**: No example exports, sample files, or test data.
- **No export instructions**: No screenshots, user guide, or step-by-step instructions for performing an export.
- **No value sets or code systems**: Beyond what FHIR/US Core defines by default.
- **No relationships or entity model**: No documentation of how data entities relate to each other.

The only technical artifact is the FHIR API documentation, which is standard (g)(10) API reference material. It documents API endpoints and USCDI data element mappings but provides no PacEHR-specific information about what data the product actually stores or exports.

A developer reading this documentation would know how to call a standard FHIR API to retrieve USCDI data elements. They would have **no information** about:
- What billing, scheduling, or administrative data PacEHR stores
- How encounter notes are structured internally
- What data the "EHI export" includes beyond the FHIR API
- How to perform a bulk export
- What "machine readable XML formats" means (the only format documented is FHIR JSON)

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Minimal/stub/unclear**

The export documentation covers only the standard USCDI data element set via 16 FHIR resource types. PacEHR is a product centered on encounter documentation and billing for PALTC practitioners. Its core value propositions — template-driven encounter notes, charge capture, claims management, facility census tracking, and practice communications — are completely absent from the export documentation. The FHIR API documents the exact set of US Core resources one would expect from any (g)(10) implementation, with no additional coverage. The EHI page claims "comprehensive and structured data" but provides zero evidence of coverage beyond USCDI.

**Axis 2 — Export approach: Repackaged existing export**

This is a textbook case of repackaging (g)(10) as (b)(10). The evidence is clear:

1. The EHI page links directly to the FHIR API documentation at thesnfist.com/cures-update/, which is the (g)(10) API documentation.
2. The documented resources are exactly the 16 standard US Core resource types — no more, no fewer.
3. Every data element maps to USCDI v1/v2 with no vendor-specific extensions.
4. There is no data dictionary, no product-specific schema, and no documentation of non-USCDI data.
5. The FHIR API page itself is titled "FHIR Server 1.0.0 for Cures Act Update" — it is the Cures Act (g)(10) implementation, not an EHI export tool.
6. Billing, scheduling, communications, and PALTC-specific data — all core product features — are completely undocumented.

The vendor's own EHI page definition of EHI includes "billing records" and "enrollment, payment, claims adjudication" — none of which appear in the linked technical documentation. The documentation contradicts itself.

### Key Findings

1. **The (b)(10) export is the (g)(10) FHIR API relabeled.** The EHI page links to the same FHIR API documentation used for standardized API access. The 16 resource types and 74 data elements are exactly the USCDI/US Core set with zero vendor additions (`cures-update-fhir-api-docs.html`).

2. **Billing and charge capture data — a core product feature — is completely absent.** PacEHR integrates billing via billEHR® and offers claims management, but no billing, claims, or financial resources appear in the export documentation.

3. **Native encounter note structure is lost.** PacEHR's primary value is template-driven, macro-enabled encounter documentation with voice-to-text. The export delivers notes only as C-CDA documents via DocumentReference, discarding the native structured data.

4. **PALTC-specific data has no export representation.** The product is designed for multi-facility visiting practitioners with facility census tracking, place-of-service coding, and SNF-specific workflows. None of this appears in the export.

5. **Documentation is near-empty.** The EHI-specific page has ~150 words of content with no data dictionary, no schema, no sample data, and no export instructions. A developer cannot determine what the export contains from the available documentation.

### Summary Stats

```
Coverage:        Minimal/stub/unclear
Approach:        Repackaged existing export
Export format:   FHIR JSON (via API); EHI page says "XML" (contradictory)
Entities:        16 FHIR resource types (standard US Core set)
Fields:          74 USCDI data elements (no vendor-specific fields)
Descriptions:    0% (no product-specific field descriptions)
Sample data:     No
Bulk export:     Claimed (certified for b(11)) but no documentation of mechanism
Domains covered: 8 of 15 applicable domains (all at USCDI level only)
```

### Bottom Line

PacEHR's EHI export is its (g)(10) FHIR API relabeled as (b)(10), covering only standard USCDI clinical data. A patient or provider would not receive billing records, charge capture data, native encounter notes, or any PALTC-specific information — all of which are core to what PacEHR stores. The single biggest gap is the complete absence of billing and revenue cycle data from a product whose value proposition centers on integrated billing and charge capture for PALTC practitioners.
