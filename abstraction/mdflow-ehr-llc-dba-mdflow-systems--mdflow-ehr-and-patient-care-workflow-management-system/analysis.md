# EHI Export Analysis: MDFlow EHR, LLC DBA: MDFlow Systems

**Product**: MDFlow EHR and Patient Care Workflow Management System  
**Analysis date**: 2026-02-15  
**CHPL ID**: 15.11.09.3190.MDEP.08.00.1.240402 (CHPL #11459)

## 1. Product Context

MDFlow EHR is a web-based, cloud/SaaS electronic health records and patient care workflow management system built for **value-based care provider groups** — particularly staff-model medical groups operating under capitation contracts in South Florida. The product is certified for version 8.0 (April 2, 2024). MDFlow is a very small vendor with no presence on G2, Capterra, or KLAS, serving a niche market of managed care provider groups. Its largest referenced customer, Community Medical Group, operates 18 medical centers with over 70,000 patients.

Per the mandatory disclosures page (verified live at `https://www.mdflow.com/www/mdflow-electronics-health-records.html`), the EHR stores and manages data across these areas relevant to EHI completeness:

- **Patient demographics and medical records** (core EHR)
- **Problem lists** ("Maintain up-to-date Problem List")
- **Medication and allergy lists** ("Maintain active Medication and Allergy List")
- **E-prescribing and medication reconciliation** with PBM history
- **CPOE** for medications with clinical decision support
- **Lab results** (automatic retrieval and incorporation into charts)
- **Immunization records** (registry submission certified under (h)(1))
- **Encounter data** ("Encounter data submission")
- **Document scanning and management**
- **HCC/MRA scores, Star Ratings, HEDIS, PQRS & MIPS** quality measures
- **Referrals and utilization management**
- **Telemedicine consultations** (integrated into the EHR)
- **Patient portal**
- **Patient-specific education resources**

It is **unclear** whether MDFlow's EHR includes billing/claims functionality — the disclosures page does not list billing as a feature, though the vendor's separate Hospitalist Management System product explicitly does. The product emphasizes "revenue enhancement" and "cost reduction" but this may refer to operational efficiency rather than integrated billing.

## 2. Artifacts Reviewed

| # | Artifact | Size | Description | Informativeness |
|---|----------|------|-------------|-----------------|
| 1 | `EHIExport.pdf` | 1 page, 131 words | Registered (b)(10) documentation. Five bullet points stating C-CDA is the primary export format. | **Very low** — no data dictionary, no field definitions, no procedural detail |
| 2 | `EHI-B10-Export.pdf` | 1 page, 74 words | Supplemental (b)(10) documentation for v8.1. Clarifies export structure as ZIP of per-encounter C-CDA ZIPs. | **Very low** — even less content than the registered PDF |
| 3 | `API-Documentation-g7910.pdf` | 58 pages | FHIR R4 API documentation for (g)(7)/(g)(9)/(g)(10). Covers SMART on FHIR auth and 15 FHIR resource types. | **Not (b)(10)** — but provides context on what clinical data MDFlow exposes via FHIR |
| 4 | `ValidURLs.json` | 3.6 KB | FHIR Bundle with 2 Endpoint and 2 Organization resources (service base URLs). | **Not relevant** to EHI export |
| 5 | `mandatory-disclosures-page.png` | 2.1 MB | Screenshot of product page with feature list, certification details, and EHI links. | **Moderate** — confirms product features and link structure |

**Total (b)(10) EHI export documentation: 2 pages, 205 words, zero data dictionary content.** The API Documentation PDF (58 pages) is solely (g)(10) FHIR API documentation and does not describe the (b)(10) export.

## 3. Export Mechanics

- **Format**: C-CDA (Consolidated Clinical Document Architecture) is described as the "primary" export format. CSV and PDF are mentioned as alternatives for "special and customized requests."
- **Structure**: The v8.1 supplemental document (`EHI-B10-Export.pdf`) clarifies the export is a ZIP file containing per-encounter C-CDA documents, each in their own ZIP archive within the main ZIP.
- **Mechanism**: Not described. There are no screenshots, no procedural instructions, and no indication whether this is a UI button, an admin function, or requires vendor assistance.
- **Single-patient vs bulk**: `EHIExport.pdf` states "Our system can export single patient's EHI or a group of patients' EHI."
- **Access constraints/fees**: Not documented. The mandatory disclosures page states clients "may be required to cover additional costs related to customization of software, training, setup, data analysis and/or consulting services" but does not specifically mention EHI export fees.

## 4. Export Content: What's In It

### No data dictionary exists

There is **no data dictionary** in any of the artifacts. Neither the registered `EHIExport.pdf` nor the supplemental `EHI-B10-Export.pdf` provides:
- Any list of entities, tables, or data elements
- Any field names, types, or descriptions
- Any value sets or coded field documentation
- Any relationship or schema documentation
- Any sample data or worked examples

The entire (b)(10) documentation consists of the following factual claims:

1. The export "contains data stored in the patient's chart in the SQL database" (`EHIExport.pdf`)
2. The primary format is C-CDA (`EHIExport.pdf`)
3. CSV and PDF are available for custom requests (`EHIExport.pdf`)
4. Single or group patient export is supported (`EHIExport.pdf`)
5. ZIP compression is used (`EHIExport.pdf`)
6. The export ZIP contains per-encounter C-CDA ZIP archives (`EHI-B10-Export.pdf`)

### What C-CDA typically includes

Since the export is C-CDA based, the content is bounded by what the C-CDA standard supports. A standard CCD (Continuity of Care Document) or C-CDA document includes sections for:

- Patient demographics (header)
- Problems / conditions
- Medications
- Allergies
- Immunizations
- Vital signs
- Procedures
- Lab results
- Clinical notes (narrative sections)
- Care plan information
- Encounter information

However, without sample data or any vendor-specific documentation, it is impossible to verify which C-CDA sections MDFlow actually populates, whether they include vendor extensions, or how completely any section is filled.

### What C-CDA does NOT naturally accommodate

C-CDA was designed for clinical summary exchange (transitions of care), not comprehensive EHI export. The following data domains that MDFlow stores are **not representable in standard C-CDA**:

- HCC/MRA risk adjustment scores and disease group management
- Star Ratings and HEDIS quality measures
- PQRS/MIPS quality measurement data
- Referral and utilization management workflows
- Telemedicine session recordings and metadata
- Patient portal messages and communications
- Patient-specific education resource tracking
- Document management (scanned documents beyond what C-CDA embeds)
- PBM (pharmacy benefits management) history beyond medication lists

### FHIR API comparison (for context)

The (g)(10) FHIR API documentation (`API-Documentation-g7910.pdf`, 58 pages) covers 15 FHIR resource types: Patient, AllergyIntolerance, CarePlan, CareTeam, Condition, ImplantableDevice, DiagnosticReport/ClinicalNotes/DocumentReference, Laboratory Result Observation, Goal, Immunization, Medication, SmokingStatus, Procedure, Provenance, and VitalSigns. These are the standard USCDI v1 / US Core resource set. The (b)(10) C-CDA export covers the same clinical domain as the FHIR API — both represent the standard clinical summary, not the full designated record set.

### Vendor's own content organization

No vendor-provided content organization exists. There are no tables, entities, categories, or field inventories to present. The vendor's documentation consists solely of prose describing the format (C-CDA) and packaging (ZIP) without any specification of content.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor provides **no content specification whatsoever**. The only claim is that the export "contains data stored in the patient's chart in the SQL database" and uses C-CDA format. There is no breakdown by category, module, or domain. There are no entity lists, field counts, or data element inventories.

The export is entirely dependent on what MDFlow's C-CDA implementation includes, which is undocumented. Based on C-CDA standards, it likely covers core clinical summary data (demographics, problems, medications, allergies, immunizations, vitals, procedures, labs, notes) but this cannot be verified from the artifacts.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | Implied by C-CDA header; no field-level documentation | C-CDA includes basic demographics; depth unknown |
| Encounters / visits | ⚠️ Partial | Per-encounter C-CDA structure described in `EHI-B10-Export.pdf` | Structure suggests one C-CDA per encounter, but encounter details undocumented |
| Problems / conditions / diagnoses | ⚠️ Partial | Standard C-CDA section; product explicitly maintains problem lists | Likely present in C-CDA but completeness unverifiable |
| Medications / prescriptions | ⚠️ Partial | Standard C-CDA section; product has e-prescribing and medication reconciliation | C-CDA medications section likely present; prescription detail depth unknown |
| Allergies | ⚠️ Partial | Standard C-CDA section; product maintains allergy lists | Likely present in C-CDA |
| Immunizations | ⚠️ Partial | Standard C-CDA section; product submits to immunization registries | Likely present in C-CDA |
| Vitals | ⚠️ Partial | Standard C-CDA section | Likely present in C-CDA |
| Lab results | ⚠️ Partial | Standard C-CDA section; product auto-retrieves lab results | Likely present in C-CDA |
| Imaging / diagnostic reports | ⚠️ Partial | C-CDA can include diagnostic report sections | No evidence imaging is a significant MDFlow feature |
| Procedures | ⚠️ Partial | Standard C-CDA section | Likely present in C-CDA |
| Clinical notes / documents | ⚠️ Partial | C-CDA narrative sections; product has document management | Notes likely present; scanned documents may not be embedded in C-CDA |
| Care plans / goals | ⚠️ Partial | C-CDA can include care plan sections | Presence unverifiable |
| Orders / referrals | ❌ Not covered | Referrals and utilization management are product features but not standard C-CDA export content | Product stores this data; likely missing from C-CDA export |
| Insurance / coverage | ❌ Not covered | Not a standard C-CDA section | Product targets capitated/managed care groups; insurance data likely stored but not in C-CDA |
| Claims / billing | N/A | No billing entities in export; unclear if product has integrated billing | Product's billing capabilities are unclear; separate HMS product handles billing |
| Payments | N/A | Not documented | Same as above — unclear if EHR has billing |
| Consents / directives | ❌ Not covered | Not documented in export artifacts | HIPAA compliance features suggest consent data exists |
| Patient communications / portal messages | ❌ Not covered | Product has patient portal and secure messaging; not in C-CDA | Real gap — product stores portal messages but C-CDA cannot represent them |
| Specialty-specific (value-based care / risk adjustment) | ❌ Not covered | Product's core differentiator — HCC/MRA scores, Star Ratings, HEDIS, quality measures — has no C-CDA representation | **Significant gap** — the product's defining feature (value-based care analytics) is not exportable via C-CDA |

All clinical domains are rated "⚠️ Partial" rather than "✅ Covered" because there is zero documentation confirming which C-CDA sections MDFlow actually populates. The coverage assessment is based entirely on what C-CDA *can* include, not what MDFlow's implementation *does* include.

## 6. Documentation Quality

The (b)(10) export documentation quality is **among the worst possible for a certified product**:

- **Total documentation**: 2 pages, 205 words across two PDFs. No other (b)(10) documentation exists.
- **Data dictionary**: None. Zero field-level documentation.
- **Schema / structure documentation**: Only the statement that the export uses C-CDA format in ZIP archives.
- **Sample data**: None.
- **Machine-readable artifacts**: None (the `ValidURLs.json` is for (g)(10), not (b)(10)).
- **Procedural instructions**: None. No screenshots, no step-by-step guide, no indication of where to find the export function in the UI.
- **Contrast with (g)(10)**: The FHIR API documentation is 58 pages with endpoint specifications, request/response examples, and OAuth2 flow documentation. The 290:1 word count ratio between (g)(10) and (b)(10) documentation suggests the vendor invested in the FHIR API and treated (b)(10) as a compliance checkbox.

**Could a developer build an import from this documentation?** No. A developer would need to: (1) know C-CDA generically, (2) obtain actual export files, (3) reverse-engineer MDFlow's specific C-CDA implementation. The documentation provides no vendor-specific information whatsoever.

## 7. Overall Assessment

### Classification

**Standard-based projection.** MDFlow's (b)(10) EHI export is C-CDA — a clinical summary standard — being used as the complete EHI export mechanism. C-CDA covers the same clinical summary domains as FHIR US Core / USCDI v1 (which MDFlow's (g)(10) API also serves). The export does not represent MDFlow's native database model and cannot cover the vendor-specific data domains (risk adjustment, quality measures, referral management, patient portal communications) that are central to the product's value proposition.

### Key Findings

1. **The export is C-CDA repackaged as (b)(10).** Both EHI export documents describe per-encounter C-CDA documents in ZIP archives. This is functionally the same clinical summary data available through C-CDA exchange or the FHIR (g)(10) API, not a comprehensive EHI export.

2. **Zero data dictionary or field-level documentation.** The entire (b)(10) documentation is 205 words across 2 single-page PDFs. There are no field names, types, descriptions, value sets, relationships, schemas, or sample data.

3. **The product's core differentiator is not exportable.** MDFlow's defining feature — value-based care workflow management with HCC/MRA scoring, Star Ratings, HEDIS, and quality measures — has no representation in C-CDA. This is the most significant coverage gap.

4. **Stark asymmetry between (g)(10) and (b)(10) investment.** The FHIR API documentation is 58 pages with detailed endpoint specifications. The EHI export documentation is 2 pages with 5 bullet points plus a structural clarification. This strongly suggests (b)(10) was treated as a compliance checkbox.

5. **CSV/PDF alternatives are undocumented.** The registered PDF mentions CSV and PDF formats for "special and customized requests," which *could* theoretically cover broader data domains, but there is zero documentation of what these contain or how to request them.

### Summary Stats

```
Classification:  Standard-based projection
Export format:   C-CDA (in ZIP archives); CSV/PDF mentioned for custom requests
Model type:      Standard projection (C-CDA clinical summary)
Entities:        N/A (no data dictionary)
Fields:          N/A (no data dictionary)
Descriptions:    N/A
Sample data:     No
Bulk export:     Yes (group patient export mentioned)
Domains covered: 0 of 14 confirmed; ~10 of 14 likely via C-CDA but unverifiable
```

### Bottom Line

MDFlow's (b)(10) export is a C-CDA clinical summary repackaged as an EHI export, documented with only 205 words and no data dictionary. A patient or provider receiving this export would get standard clinical summary data (demographics, problems, medications, allergies, labs, vitals) per encounter but would almost certainly miss the product's core value-based care data — HCC/MRA risk adjustment scores, quality measures, referral management, and patient portal communications. The single biggest gap is the complete absence of documentation: without a data dictionary, sample data, or any field-level detail, it is impossible to verify what the export actually contains or to assess its completeness beyond what the C-CDA standard generically allows.
