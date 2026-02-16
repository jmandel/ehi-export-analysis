# EHI Export Analysis: VisionWeb

**Product**: Uprise 3.1
**Analysis date**: 2026-02-16
**CHPL IDs**: 15.04.04.2514.Upri.31.01.1.221213

## 1. Product Context

Uprise is a **cloud-based, all-in-one practice management and EHR system built specifically for optometry/eye care practices**, developed by VisionWeb (now part of EssilorLuxottica's HELIX division). It targets independent optometry and ophthalmology practices, from solo ODs to multi-location groups.

Key data domains the product stores:

- **Clinical/EHR**: Eye exam documentation (SmartTouch EHR), diagnoses, medications, allergies, immunizations, vitals, lab results, clinical impressions, care plans, goals, patient education, clinical decision support
- **Optometry-specific**: Optical prescriptions (spectacle and contact lens), refractions (7 types: autorefraction, contact lens Rx, cycloplegic, manifest, retinoscopy, spectacle Rx, wavefront), procedures (dilation, IOPs, screening), keratometry, binocular vision
- **Optical dispensing & ordering**: Frame/lens orders with full lifecycle tracking, inventory management, integration with 400+ labs/suppliers via VisionWeb platform
- **Billing & claims**: Electronic claim submission (CMS-1500), invoices, payments, adjustments, CodeSAFE code verification
- **Insurance**: Policies, benefits, electronic eligibility verification, coverage determinations
- **Practice management**: Scheduling, patient intake, recall, patient portal (messaging, digital forms)
- **Documents & images**: Exam images, diagnostic equipment imports, attached documents

This establishes the baseline: a comprehensive (b)(10) export should cover clinical, optometry-specific, billing, insurance, ordering, and administrative data.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/Data_Export.pdf` (58 pages, 880 KB) | Complete data dictionary documenting 81 CSV files with field-level definitions for all 2,079 fields. Created 2024-02-20 by Philip Lu. | **Primary artifact** — most informative |
| `downloads/data-export-page.html` (36 KB) | ScreenSteps documentation page with introductory text about (b)(10) requirement and link to PDF | Confirms export mechanism and regulatory context |
| `downloads/screenshot-data-export-page.png` (155 KB) | Screenshot of the documentation page | Confirms page layout and navigation structure |

The PDF data dictionary is the sole substantive artifact and contains all export documentation.

## 3. Export Mechanics

- **Format**: CSV files in a ZIP archive, with supplementary images and XML data referenced by the CSVs
- **Mechanism**: UI-based — accessed via "Patient Export" section in Practice Management
- **Single-patient vs bulk**: Documentation states the system supports export of "single and patient population EHI" per the (b)(10) requirement
- **Access constraints**: No fees noted. The documentation page states "there are no technical or contractual considerations to use our certified product"
- **Documentation access**: Publicly accessible via ScreenSteps at the registered URL; no authentication required

## 4. Export Content: What's In It

The export consists of **81 CSV files** containing a total of **2,079 fields**. Every field (100%) has at least a brief text description. No data types, value sets, cardinality, or relationship documentation is provided — descriptions are name+brief note only (e.g., "Claim status," "Patient chart number").

No sample data, JSON schemas, or machine-readable artifacts accompany the data dictionary.

### Vendor's own content organization

The PDF organizes files alphabetically with no explicit categories. I categorized them based on content domain. Summary by category:

| Category | Entities | Fields |
|---|---|---|
| Clinical | 20 | 332 |
| Optometry-Specific | 17 | 696 |
| Demographics & Administration | 16 | 225 |
| Billing & Financial | 10 | 299 |
| Insurance & Benefits | 5 | 111 |
| Scheduling & Encounters | 4 | 85 |
| Orders & Products | 4 | 259 |
| Reference | 5 | 72 |
| **Total** | **81** | **2,079** |

### Top 20 entities by field count

| Entity | Fields | Category |
|---|---|---|
| RxOrder | 176 | Orders & Products |
| Prescription | 151 | Optometry-Specific |
| RefractionContactLensRx | 142 | Optometry-Specific |
| Claim | 136 | Billing & Financial |
| RefractionSpectacleRx | 58 | Optometry-Specific |
| Product | 43 | Orders & Products |
| RefractionManifest | 42 | Optometry-Specific |
| BenefitCoverageManual | 40 | Insurance & Benefits |
| InvoiceLine | 40 | Billing & Financial |
| RefractionAutorefraction | 40 | Optometry-Specific |
| RefractionCyclopegic | 40 | Optometry-Specific |
| RefractionRetinoscopy | 40 | Optometry-Specific |
| RefractionWavefront | 40 | Optometry-Specific |
| Patient | 39 | Demographics & Administration |
| ClaimLine | 31 | Billing & Financial |
| ConditionChiefComplaint | 31 | Clinical |
| Immunizations | 30 | Clinical |
| Procedure | 30 | Optometry-Specific |
| BenefitCoverageElectronic | 29 | Insurance & Benefits |
| ProcedureDilation | 29 | Optometry-Specific |

The complete entity inventory with all 2,079 fields is in `analysis/entity-inventory-full.json`.

### Notable content highlights

**Optometry-specific depth is exceptional.** The seven refraction CSVs alone total 402 fields, capturing autorefraction, contact lens Rx, cycloplegic, manifest, retinoscopy, spectacle Rx, and wavefront data for both eyes (OD/OS). `RefractionContactLensRx.csv` has 142 fields including product details, over-refractions, fitting observations, and wear schedule. `Prescription.csv` (151 fields) captures both spectacle and contact lens prescriptions with sphere, cylinder, axis, prism, base curve, diameter, addition, and keratometry readings per eye.

**Billing is deeply covered.** `Claim.csv` has 136 fields mapping to CMS-1500 form elements including billing/referring/rendering provider details, facility info, accident data, disability dates, prior authorization, and ERA (electronic remittance advice) references. Supporting files cover claim lines, diagnosis pointers, notes, status tracking, invoices, adjustments, and payments.

**RxOrder.csv is the largest entity** at 176 fields, covering the complete optical order lifecycle: frame specifications, lens measurements, trace data, personalization parameters, pricing, shipping, and lab instructions.

**Audit metadata is universal.** Every CSV includes CreatedDate, CreatedBy, ModifiedDate, ModifiedBy fields.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The export is organized around the product's core workflows:

- **Clinical (20 entities, 332 fields)**: Allergies, conditions (with chief complaints, concerns, and functional/cognitive status), medications, lab results, vitals, immunizations, clinical impressions, care plans, goals, patient education, physical exam, review of systems, past/family/social history, lifestyle observations, binocular vision, keratometry. This is thorough general clinical coverage.

- **Optometry-specific (17 entities, 696 fields)**: This is the richest category by far. Seven refraction types, prescriptions (spectacle + contact lens), procedures (dilation with up to 4 medications, IOPs with targets, screening, other), and associated add-ons. The depth of optometric exam data — 696 fields — reflects genuine specialty-specific export work that would never appear in a repackaged USCDI export.

- **Billing & Financial (10 entities, 299 fields)**: Claims (136 fields with CMS-1500 mapping), claim lines, diagnosis codes, status tracking, invoices, invoice line items, adjustments, payments, payment application details. This covers the full revenue cycle within the EHR.

- **Insurance & Benefits (5 entities, 111 fields)**: Policies, electronic eligibility responses, manual benefit coverage entries with detailed coverage parameters (copay, frequency, allowance, enhancements).

- **Demographics & Administration (16 entities, 225 fields)**: Patient demographics (39 fields including gender identity, sexual orientation, race, ethnicity, language, employment), addresses, phone numbers, emails, preferences, alerts, notes, documents, linked accounts, payment cards, questionnaire responses, contacts, devices (UDI).

- **Scheduling & Encounters (4 entities, 85 fields)**: Appointments, encounters (with recall info and service type), encounter-level procedures with diagnosis codes, patient recall records.

- **Orders & Products (4 entities, 259 fields)**: RxOrder (176 fields — the single largest entity), Product catalog, ServiceRequest (LOINC-coded), Task.

- **Reference (5 entities, 72 fields)**: Locations, providers, document references.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | `Patient` (39 fields), `PatientAddress`, `PatientPhoneNumber`, `PatientEmail`, `PatientPreference`, `Contact`, `ContactLinkedAccount` | Thorough — includes SOGI, race/ethnicity, language, employment |
| Encounters / visits | ✅ Covered | `Encounter` (28 fields), `EncounterProceduresDiagnosis` (26 fields) | Good — includes class, service type, participants, recall |
| Problems / conditions | ✅ Covered | `Condition` (26 fields), `ConditionChiefComplaint` (31 fields), `ConditionConcern`, `ConditionFunctionalCognitive` | Thorough — separate entities for chief complaints, concerns, functional/cognitive status |
| Medications / prescriptions | ✅ Covered | `MedicationRequest` (21 fields), `Prescription` (151 fields — optical Rx) | Comprehensive for both pharmaceutical and optical prescriptions |
| Allergies | ✅ Covered | `AllergyIntolerance` (24 fields) | Includes reactions, severity, substance codes, code systems |
| Immunizations | ✅ Covered | `Immunizations` (30 fields) | Detailed — codes, lots, routes, sites, VFC category, status reason |
| Vitals | ✅ Covered | `ObservationVitals` (10 fields) | Standard vital signs with codes, values, units |
| Lab results | ✅ Covered | `ObservationLabResults` (23 fields) | Includes codes, values, units, reference ranges, interpretations |
| Imaging / diagnostic reports | ✅ Covered | `Images` (28 fields) | Diagnostic images with OS/OD references, body sites, interpretations |
| Procedures | ✅ Covered | `Procedure` (30 fields), `ProcedureDilation`, `ProcedureIOPs`, `ProcedureOther`, `ProcedureScreening` | Deeply covered including optometry-specific procedures |
| Clinical notes / documents | ✅ Covered | `ClinicalImpression` (10 fields), `PatientDocumentReference`, `DocumentReference`, `PatientNote` | Assessment notes, general notes, medication notes, attached documents |
| Care plans / goals | ✅ Covered | `CarePlan` (11 fields), `Goal` (14 fields) | Standard care plan and goal tracking |
| Orders / referrals | ✅ Covered | `RxOrder` (176 fields), `ServiceRequest` (20 fields) | Optical orders deeply detailed; service requests with LOINC codes |
| Insurance / coverage | ✅ Covered | `Policy` (20 fields), `Benefit`, `BenefitCoverageElectronic`, `BenefitCoverageManual` | Thorough — both electronic eligibility and manual coverage |
| Claims / billing | ✅ Covered | `Claim` (136 fields), `ClaimLine`, `ClaimDiagnosis`, `ClaimLineCodes`, `ClaimNote`, `ClaimStatus` | Deep — CMS-1500 level detail |
| Payments | ✅ Covered | `Payment` (17 fields), `PaymentItem` (13 fields), `PatientAccount` (18 fields) | Payment method, payer, remittance, account balances |
| Invoices | ✅ Covered | `Invoice`, `InvoiceLine` (40 fields), `InvoiceLIneAdjustment`, `InvoiceLIneDiagnosis` | Line items, adjustments, discounts, write-offs |
| Patient communications | ⚠️ Partial | `PatientNote` (7 fields) | Product has patient portal with messaging; no dedicated messaging/portal communication entity. `PatientNote` may capture some communications but is thin (7 fields) |
| Specialty-specific (optometry) | ✅ Covered | 17 entities, 696 fields covering refractions, prescriptions, IOPs, dilation, keratometry, binocular vision | Exceptionally thorough specialty coverage |
| Questionnaires / forms | ✅ Covered | `Questionnaire` (11 fields) | Captures questionnaire responses |
| Consents / directives | ❌ Not covered | No consent or advance directive entity | Unclear if product stores consent data beyond portal/intake forms |
| Patient education | ✅ Covered | `CommunicationEducation` (13 fields) | Education records with content types |

## 6. Documentation Quality

**Strengths:**
- Every field across all 81 CSV files has a description (100% coverage)
- Clear export mechanism description (ZIP of CSVs, accessed via Practice Management)
- FHIR-influenced naming conventions make entities self-documenting (e.g., AllergyIntolerance, MedicationRequest, Condition)
- Consistent audit metadata pattern (CreatedDate/CreatedBy/ModifiedDate/ModifiedBy) across all entities
- Cross-reference identifiers (Patient chart number, EncounterID, ClaimID, etc.) enable record linking

**Weaknesses:**
- **No data types**: No indication of string vs. number vs. date vs. boolean for any field
- **No date formats**: No specification of datetime format (ISO 8601? MM/DD/YYYY?)
- **No value sets**: Coded fields (Status, Category, Classification, etc.) don't enumerate valid values
- **No cardinality**: No required vs. optional field indicators
- **No relationship documentation**: No ERD, no formal foreign key documentation — relationships must be inferred from field names
- **No sample data**: No example export files to test against
- **No machine-readable schema**: PDF-only; no JSON Schema, XSD, or CSV header spec
- **Descriptions are terse**: Most descriptions simply restate the field name (e.g., "Created date" for CreatedDate, "Claim status" for Status) — they help confirm purpose but don't explain semantics or formats

**Developer usability**: A developer could understand the structure and reconstruct patient records from the export, but would need actual export data to determine types, date formats, coded values, and edge cases. The documentation is a good map but not a complete integration specification.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Comprehensive**

This export demonstrably covers the breadth of data domains Uprise stores. Against the product's known capabilities:

- ✅ Clinical EHR data: thoroughly covered (20 entities)
- ✅ Optometry-specific exam data: exceptionally covered (17 entities, 696 fields — this alone proves purpose-built work)
- ✅ Billing and claims: deeply covered (10 entities including 136-field Claim table with CMS-1500 mapping)
- ✅ Insurance and benefits: well covered (5 entities including electronic eligibility responses)
- ✅ Optical ordering: deeply covered (RxOrder with 176 fields)
- ✅ Patient demographics and administration: thorough (16 entities)
- ⚠️ Patient portal communications: only partially covered (PatientNote is thin)
- ❌ Consents: not explicitly covered

The minor gaps (portal messages, consents) don't undermine the overall comprehensiveness. The export covers ~20 of ~22 applicable domains with genuine depth. Coverage goes far beyond USCDI — the 696 fields of optometry-specific data, 299 fields of billing data, and 259 fields of order data are all entirely outside USCDI scope.

**Axis 2 — Export approach: Purpose-built EHI export**

This is unambiguously a purpose-built (b)(10) export. Key signals:

1. **81 CSV files with 2,079 fields** — this is a native database export, not a clinical exchange format
2. **Optometry-specific depth** that would never appear in a (g)(10) FHIR API or C-CDA: 7 refraction types, IOP measurements/targets, dilation with medication tracking, optical order lifecycle
3. **Full billing/financial coverage**: CMS-1500 claim fields, invoice line adjustments, payment application details — none of which appear in USCDI or standard clinical exchange
4. **Insurance eligibility responses** with 29 fields of coverage determination data
5. **Vendor-specific product catalog** and optical order tracking with trace data, frame measurements, and personalization parameters
6. The CSV format itself signals a database-level export rather than a standards-based clinical summary

### Key Findings

1. **Genuinely comprehensive specialty EHR export.** 81 CSV files covering 2,079 fields across clinical, optometry-specific, billing, insurance, ordering, and administrative domains. The optometry-specific depth (696 fields across 17 entities) is particularly impressive and demonstrates real (b)(10) engagement.

2. **Billing coverage is substantive.** The Claim entity alone has 136 fields mapping to CMS-1500 form elements, supported by 9 additional billing entities. This is not a token billing mention — it's a full revenue cycle export.

3. **Prior report undercounted entities.** The earlier report stated "76 CSV files" — the actual count from the PDF is **81 CSV files**. The discrepancy appears to be a simple counting error in the prior analysis.

4. **Documentation quality is functional but limited.** 100% field description coverage is good, but descriptions are terse (often restating the field name), and the absence of data types, value sets, and relationship documentation means developers must reverse-engineer significant details from actual export data.

5. **Minor gap in patient communications.** The product has a patient portal with messaging, but the export lacks a dedicated messaging entity. `PatientNote` (7 fields) may partially cover this, but it's the most notable omission in an otherwise thorough export.

### Summary Stats

    Coverage:        Comprehensive
    Approach:        Purpose-built EHI export
    Export format:   CSV (ZIP archive with images/XML)
    Entities:        81
    Fields:          2,079
    Descriptions:    100% (all fields have descriptions, though terse)
    Sample data:     No
    Bulk export:     Yes (single-patient and population)
    Domains covered: ~20 of 22 applicable domains

### Bottom Line

Uprise delivers one of the stronger (b)(10) implementations for a specialty EHR. A patient or provider would get a genuinely complete copy of their data — clinical records, optometry-specific exam data, billing/claims, insurance, and optical orders — in a structured, parseable format. The biggest gap is the lack of explicit patient portal communication export, and the documentation would benefit from data types and value sets, but the core export content is comprehensive and clearly purpose-built.
