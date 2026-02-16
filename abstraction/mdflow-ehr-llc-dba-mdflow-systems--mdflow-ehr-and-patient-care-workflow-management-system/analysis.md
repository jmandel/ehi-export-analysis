# EHI Export Analysis: MDFlow EHR, LLC DBA: MDFlow Systems

**Product**: MDFlow EHR and Patient Care Workflow Management System
**Analysis date**: 2026-02-16
**CHPL IDs**: 15.11.09.3190.MDEP.08.00.1.240402

## 1. Product Context

MDFlow is a web-based, cloud/SaaS EHR system developed by a small Miami-based company targeting **value-based care provider groups** — specifically staff-model medical groups under capitation contracts in South Florida. Their largest referenced customer, Community Medical Group, operates 18 medical centers with 70,000+ patients.

The certified EHR product stores and manages:
- **Core clinical data**: patient demographics, problem lists, medications (with e-prescribing), allergies, lab results, vital signs, immunizations, procedures, clinical notes/encounter documentation
- **Risk adjustment and quality data**: HCC/MRA scores, Star Ratings, HEDIS measures, PQRS/MIPS quality metrics — a central differentiator for this value-based care product
- **Document management**: scanned/uploaded documents
- **Patient engagement**: patient portal, secure messaging, telemedicine sessions (recorded and stored in the patient record)
- **Scheduling**: appointment scheduling with transportation management
- **Health information exchange**: HL7, CCD, CCR, CCDA documents

**Billing status is unclear**: the EHR product page does not explicitly describe billing/claims features, though it references "revenue enhancement." The separate Hospitalist Management System product explicitly includes billing and revenue cycle management. It is uncertain whether the EHR has built-in billing.

The product's value-based care focus (HCC scoring, risk adjustment, quality measures) means it stores significant data beyond standard clinical content that should be part of an EHI export.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/EHIExport.pdf` (442 KB, 1 page) | Registered EHI export documentation, v8.0. Five bullet points: C-CDA as primary format, CSV/PDF for custom requests, single/group export, ZIP compression. Created 2024-03-20. | **Very low** — no data dictionary, no field detail, no procedural guidance |
| `downloads/EHI-B10-Export.pdf` (40 KB, 1 page) | Supplemental EHI B10 export doc, v8.1. Clarifies the export is a ZIP containing per-encounter C-CDA ZIP archives. Created 2025-02-26. | **Very low** — marginally more structural detail than the primary PDF, still no data dictionary |
| `downloads/API-Documentation-g7910.pdf` (509 KB, 58 pages) | FHIR R4 API documentation for (g)(7)/(g)(9)/(g)(10) certification. Covers SMART on FHIR auth, ~15 US Core resource endpoints, search, error handling. Created 2025-02-26. | **Moderate** — useful for understanding the FHIR/(g)(10) surface, which is the same clinical scope as the C-CDA export |
| `downloads/ValidURLs.json` (3.7 KB) | FHIR Bundle listing FHIR server endpoints. Service Base URL artifact for (g)(10). | **None** for (b)(10) assessment |
| `downloads/mandatory-disclosures-page.png` (2.1 MB) | Screenshot of MDFlow's mandatory disclosures page showing EHI export links and certified criteria. | **Low** — confirms link structure, no additional export detail |

## 3. Export Mechanics

- **Format**: C-CDA (Consolidated Clinical Document Architecture) as the primary format. The vendor states CSV and PDF are available for "special and customized requests" but provides no documentation of what these alternative formats contain.
- **Structure**: A ZIP archive containing per-encounter ZIP files, each containing a C-CDA document (per `EHI-B10-Export.pdf`, v8.1).
- **Mechanism**: Not documented. No screenshots, procedural instructions, or UI description. Presumably a UI function within the EHR, but the documentation does not say.
- **Single-patient vs bulk**: Documentation states the system "can export single patient's EHI or a group of patients' EHI."
- **Access constraints or fees**: Not documented.

## 4. Export Content: What's In It

### No data dictionary exists

The vendor provides **zero** field-level, entity-level, or schema documentation. The entire (b)(10) export documentation consists of:

1. `EHIExport.pdf` — 1 page, 5 bullet points
2. `EHI-B10-Export.pdf` — 1 page, 6 bullet points

Neither document names a single data element, table, field, section, or clinical domain that is included in the export. The only content-related statement is that the export "contains data stored in the patient's chart in the SQL database" (v8.0) or "contains data from the patient's chart" (v8.1).

### What can be inferred

Since the export format is C-CDA, the content is bounded by what C-CDA supports. Standard C-CDA documents (CCD type) typically include sections for:

- Demographics (header)
- Problems / Conditions
- Medications
- Allergies
- Immunizations
- Vital Signs
- Lab Results
- Procedures
- Clinical Notes (narrative)
- Care Plan
- Social History (smoking status)

**However**, the vendor does not confirm which C-CDA sections or templates they actually populate. There is no documentation of vendor-specific extensions, custom sections, or additional content beyond the C-CDA standard. There are no sample files to inspect.

### Vendor's own content organization

There is no vendor-provided content organization. No entities, tables, fields, categories, or groupings are documented.

| Entity/Table | Fields | Described | Types | Category (vendor's) |
|---|---|---|---|---|
| *(none documented)* | — | — | — | — |

See `analysis/entity-inventory-full.json` and `analysis/entity-inventory-summary.json` for the machine-readable representation (both confirm zero documented entities/fields).

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor covers **nothing explicitly**. The documentation says the export "contains data from the patient's chart" in C-CDA format, but does not enumerate what that includes. There are no categories, no modules, no sections described.

The C-CDA format inherently limits the export to clinical summary data. C-CDA was designed for transitions of care — it covers core clinical domains (demographics, problems, medications, allergies, vitals, labs, immunizations, procedures, notes) but does not naturally accommodate billing data, risk adjustment scores, quality measures, scheduling, or the value-based care workflow data that is central to MDFlow's product differentiation.

The 58-page (g)(10) FHIR API documentation covers these US Core / USCDI v1 resource types: Patient, AllergyIntolerance, CarePlan, CareTeam, Condition, ImplantableDevice, DiagnosticReport, DocumentReference, Observation (labs, vitals, smoking status), Goal, Immunization, Medication, Procedure, Provenance, and Encounter (search only). These are the standard USCDI clinical domains — the same scope that C-CDA covers. There is no evidence the (b)(10) export goes beyond this.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | Inferred from C-CDA header; no field-level detail | C-CDA includes basic demographics but vendor doesn't confirm scope |
| Encounters / visits | ⚠️ Partial | Export is structured per-encounter (ZIP per encounter) | Encounter structure exists but encounter metadata detail unknown |
| Problems / conditions | ⚠️ Partial | Inferred from standard C-CDA section | No confirmation from vendor |
| Medications / prescriptions | ⚠️ Partial | Inferred from standard C-CDA section; product has e-prescribing | No confirmation; PBM history coverage unknown |
| Allergies | ⚠️ Partial | Inferred from standard C-CDA section | No confirmation from vendor |
| Immunizations | ⚠️ Partial | Inferred from standard C-CDA section | No confirmation from vendor |
| Vitals | ⚠️ Partial | Inferred from standard C-CDA section | No confirmation from vendor |
| Lab results | ⚠️ Partial | Inferred from standard C-CDA section | No confirmation from vendor |
| Imaging / diagnostic reports | ⚠️ Partial | Inferred from standard C-CDA section | Product capabilities in imaging unclear |
| Procedures | ⚠️ Partial | Inferred from standard C-CDA section | No confirmation from vendor |
| Clinical notes / documents | ⚠️ Partial | Inferred from standard C-CDA narrative sections | Depth unclear; telemedicine session records likely not included |
| Care plans / goals | ⚠️ Partial | Inferred from standard C-CDA section | No confirmation from vendor |
| Orders / referrals | ❌ Not covered | Not standard C-CDA content beyond medication orders | CPOE for medications is certified; referral workflow coverage unknown |
| Insurance / coverage | ❌ Not covered | Not standard C-CDA content | Product likely stores insurance info; not in C-CDA export |
| Claims / billing | ❌ Not covered | Not standard C-CDA content | Billing capabilities in EHR unclear (may be separate product); if present, not exported |
| Payments | ❌ Not covered | Not standard C-CDA content | N/A if billing is in separate product |
| Consents / directives | ❌ Not covered | C-CDA has an Advance Directives section but vendor doesn't confirm | Unknown |
| Patient communications / portal messages | ❌ Not covered | Not standard C-CDA content | Product has patient portal and secure messaging; these would not be in C-CDA |
| Risk adjustment / HCC scores | ❌ Not covered | Not standard C-CDA content | **Significant gap** — HCC/MRA scoring is a central product feature and part of the patient record |
| Quality measures (HEDIS, Star Ratings) | ❌ Not covered | Not standard C-CDA content | Quality measure data is used in patient care decisions in value-based care |
| Telemedicine session data | ❌ Not covered | Not standard C-CDA content | Vendor states sessions are "recorded and stored in the patient's medical record"; unlikely in C-CDA |

**Key finding**: Every "⚠️ Partial" domain above is rated partial — not covered — because the vendor provides no confirmation that any specific domain is included. We can only infer coverage from the fact that C-CDA is a standard with well-known sections. The vendor could be populating all standard sections, some, or none beyond the bare minimum.

## 6. Documentation Quality

The (b)(10) export documentation is among the poorest possible for a certified product:

- **No data dictionary**: Zero documentation of fields, tables, entities, or data elements
- **No schema**: No C-CDA template documentation, no custom extension documentation
- **No sample data**: No example export files to inspect
- **No procedural instructions**: No description of how to initiate an export
- **No screenshots**: No visual representation of the export interface
- **No value sets or code systems**: No documentation of coded values
- **No relationships**: No documentation of how data elements relate to each other

A developer receiving this documentation could not build an import without: (a) knowing C-CDA generically, and (b) obtaining and reverse-engineering actual export files from the system.

The contrast with the (g)(10) FHIR API documentation (58 pages with endpoint descriptions, request/response examples, OAuth2 flows) is stark. The vendor clearly invested effort in (g)(10) but treated (b)(10) as a minimal compliance checkbox.

**Total documentation for (b)(10)**: 2 pages, ~11 bullet points, zero technical substance.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Minimal/stub/unclear**

The documentation is too thin to assess actual coverage. The vendor provides zero detail about what data elements are exported. The choice of C-CDA as the primary format strongly suggests the export is limited to standard clinical summary content — the same USCDI-scope data available through the (g)(10) FHIR API. MDFlow's differentiating data domains — HCC/MRA risk adjustment scores, quality measures, value-based care workflow data, telemedicine session records, patient portal messages — are not naturally represented in C-CDA and there is no evidence they are included.

The mention of CSV and PDF as alternative formats for "customized requests" hints that broader data may be available on request, but this is completely undocumented.

**Axis 2 — Export approach: Repackaged existing export**

The (b)(10) export is C-CDA documents per encounter — the same clinical document format used for transitions of care under (b)(1). The FHIR API documentation confirms the (g)(10) API covers the same USCDI v1 clinical domains. There is no evidence of any purpose-built export mechanism that goes beyond the existing clinical exchange surface. The documentation does not describe any additional data elements, custom tables, or expanded scope compared to what C-CDA and FHIR already provide.

Key indicators:
- C-CDA is a clinical summary standard, not a database export format
- No data dictionary or product-specific field documentation exists
- The same clinical domains appear in both the (g)(10) FHIR API and the (b)(10) C-CDA export
- No mention of billing, risk adjustment, quality measures, or other non-USCDI data in the export documentation

### Key Findings

1. **Documentation is effectively empty**: Two 1-page PDFs with ~11 bullet points total. Zero field-level detail, zero data dictionary, zero sample data, zero schema documentation. This is among the thinnest (b)(10) documentation possible for a certified product.

2. **Export is C-CDA — a clinical summary repackaged as EHI**: The primary export format is C-CDA per encounter in ZIP archives. C-CDA covers USCDI-scope clinical data (demographics, problems, medications, allergies, labs, vitals, immunizations, procedures, notes) but does not accommodate the product's differentiating data: HCC/MRA scores, quality measures, telemedicine sessions, portal messages, or scheduling.

3. **Stark contrast with (g)(10) documentation**: The 58-page FHIR API documentation is detailed and well-structured, covering OAuth2 flows, endpoint descriptions, and request/response examples. The (b)(10) documentation got minimal effort — 2 pages vs 58 pages, zero technical detail vs comprehensive API docs.

4. **Risk adjustment / quality data gap is most significant**: MDFlow's primary market value is HCC/MRA scoring, Star Ratings, HEDIS measures, and value-based care workflows. This data is used to make care and payment decisions about patients and is squarely within the designated record set. Its absence from the export (or at least from the export documentation) is the most significant gap.

5. **CSV/PDF alternative undocumented**: The vendor mentions CSV and PDF exports for "customized requests" but provides zero documentation of what these contain, how to request them, or what data elements they include. These could theoretically address some gaps, but without documentation they are unusable.

### Summary Stats

    Coverage:        Minimal/stub/unclear
    Approach:        Repackaged existing export
    Export format:   C-CDA (per encounter, ZIP archive); CSV/PDF mentioned but undocumented
    Entities:        N/A (no data dictionary)
    Fields:          N/A (no data dictionary)
    Descriptions:    N/A
    Sample data:     No
    Bulk export:     Yes (group export mentioned)
    Domains covered: 0 confirmed; ~11 inferred from C-CDA format of ~19 applicable domains

### Bottom Line

MDFlow's (b)(10) EHI export is a repackaged C-CDA clinical summary with no data dictionary and no evidence of coverage beyond standard USCDI clinical domains. A patient or provider would receive per-encounter clinical summaries but would likely miss the product's most distinctive data — risk adjustment scores, quality measures, telemedicine records, and portal communications. The documentation is too thin for any developer to build a reliable import without reverse-engineering actual export files.
