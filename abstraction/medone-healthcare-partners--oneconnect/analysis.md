# EHI Export Analysis: MedOne Healthcare Partners

**Product**: OneConnect Version 0
**Analysis date**: 2026-02-16
**CHPL IDs**: 11426 (15.04.04.3182.Onec.00.00.1.231227)

## 1. Product Context

OneConnect is a **custom clinical documentation tool** built by MedOne Healthcare Partners (a physician-owned hospital medicine practice in Columbus, Ohio) for **post-acute care settings**. It is not a commercial EHR product — it is internally developed and used by MedOne's ~100 physicians and 75+ advanced practice clinicians as they round across approximately 150 skilled nursing facilities, assisted living communities, rehab hospitals, and long-term acute care hospitals in Ohio.

OneConnect is a focused documentation overlay that integrates with facility EHRs (e.g., PointClickCare). Its primary function is streamlining clinical documentation. It is **not a full-featured EHR** — it does not certify for medication lists (a)(6), allergy lists (a)(8), clinical decision support (a)(9), e-prescribing (a)(10)–(a)(11), vital signs (a)(4), problem lists (a)(7), lab orders/results (a)(2)–(a)(3), imaging (a)(12)–(a)(13), or patient portal (e)(1). It uses third-party RXNT for e-prescribing and EMR Direct for health information exchange.

**What data the product stores** (baseline for export completeness):
- **Clinical notes/documentation** (core function)
- **Patient demographics** (certified (a)(5))
- **Medication orders** (certified CPOE (a)(1))
- **Implantable device information** (certified (a)(14))
- **Transitions of care documents** (C-CDAs, certified (b)(1))
- **Clinical quality measure data** (68 CQMs, certified (c)(1))

The related **BOLT** platform (same developer) may share code/data and includes billing/CPT code capture, but it is unclear whether these features are in OneConnect.

## 2. Artifacts Reviewed

| Artifact | Type | Size | What It Told Me |
|---|---|---|---|
| `EHI-Export.pdf` | PDF, 1 page | 282 KB | **Primary (b)(10) artifact.** Entire EHI export documentation: 6 sentences stating the export is a ZIP of C-CDA documents per encounter. No data dictionary, no schema, no sample data, no instructions. Created 2023-11-07 from Word. **Most important artifact — and extremely thin.** |
| `FHIR-API-Specifications.pdf` | PDF, 58 pages | 1.3 MB | (g)(10) FHIR API documentation. Smart on FHIR OAuth2 flow and US Core resource access covering 15 FHIR resource types. NOT the (b)(10) export, but shows what data the system makes available via FHIR API. Created 2023-11-28. |
| `FHIR_Valid_URLs.json` | JSON | 2 KB | FHIR Bundle with Endpoint (pointing to `qafhir.medonehp.com:9443`) and Organization resource. Infrastructure metadata only. |
| `certifications-page-screenshot.png` | PNG | 367 KB | Screenshot of `medonehp.com/certifications` showing certification details and footer links to all three documents above. Confirms the documentation is accessible via the certifications page. |

**Most informative**: `EHI-Export.pdf` (defines the export) and `FHIR-API-Specifications.pdf` (shows data capabilities).
**Least informative**: `FHIR_Valid_URLs.json` (endpoint metadata only).

## 3. Export Mechanics

- **Format**: ZIP file containing C-CDA documents (one per patient encounter). The documentation states "other files attached to the patient's chart will be added later (e.g. PDF and images)" — explicitly acknowledging the export is incomplete.
- **Mechanism**: Not documented. The PDF provides no instructions for how to initiate an export — no UI screenshots, no API endpoint, no request process.
- **Single-patient vs bulk**: Not documented. The language ("the patient EHI export") suggests single-patient.
- **Access constraints/fees**: Not documented. The CHPL metadata references third-party service fees (e.g., PCC integration at $250/month/interface, RXNT e-prescribing at $95/month/provider), but no fees specific to EHI export are mentioned.

## 4. Export Content: What's In It

### What we know

The entire EHI export documentation is 6 sentences (verbatim from `EHI-Export.pdf`):

> Product Name and Version : OneConnect Version 0
>
> The patient EHI export contains data from the patient's chart. Multiple file formats are used to store this information.
>
> ZIP is an archive file format.
>
> PDF or Portable Document Format is a file format that is used to present text or image based documents.
>
> C-CDA or Consolidated Clinical Document Architecture is a file format used for health information exchange.
>
> The export file itself is a zip file. It contains zip files of C-CDAs for now and other files attached to the patient's chart will be added later (e.g. PDF and images)
>
> Information for each patient encounter is available C-CDA format in zip archive.

**There is no data dictionary.** No entities, no tables, no fields, no types, no descriptions, no relationships, no value sets, no sample data, no schema.

### What can be inferred

Since the export is C-CDA format, its content is bounded by what C-CDA supports. Standard C-CDA sections include:
- Patient demographics (header)
- Medications
- Allergies
- Problems/conditions
- Procedures
- Results (labs)
- Vital signs
- Immunizations
- Encounters
- Plan of care

However, we have **no evidence** of which C-CDA sections OneConnect actually populates. The FHIR API documentation (`FHIR-API-Specifications.pdf`, 58 pages) shows the system can serve 15 FHIR resource types via its (g)(10) API:

| FHIR Resource | Section in API Doc |
|---|---|
| Patient | pp. 11–15 |
| AllergyIntolerance | pp. 16–17 |
| CarePlan | pp. 18–20 |
| CareTeam | pp. 21–22 |
| Condition (Problems/Health Concern) | pp. 23–25 |
| Implantable Device | pp. 26–27 |
| DiagnosticReport / DocumentReference | pp. 28–29 |
| Laboratory Result Observation | pp. 30–31 |
| Goal | pp. 32 |
| Immunization | pp. 33–34 |
| Medication (MedicationRequest) | p. 35 |
| Smoking Status (Observation) | pp. 35–38 |
| Procedure | pp. 39–40 |
| Provenance | pp. 41–44 |
| Vital Signs (Observation) | pp. 45–52 |

This represents the **USCDI v1 / US Core** data set — the standard clinical summary data that all certified EHRs must support via FHIR. The C-CDA export likely covers similar content, as it is the document-based equivalent of the same data.

### Vendor's own content organization

No vendor-defined organization exists. The vendor provides no data dictionary, no entity listing, and no categorization of export content. The only structured information comes from the FHIR API documentation, which is organized by FHIR resource type (not by clinical domain), and which documents the (g)(10) API rather than the (b)(10) export.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor's EHI export documentation describes exactly one thing: a ZIP of C-CDA documents, one per encounter. No categories, no modules, no sections are described. The documentation is the absolute minimum: it names the format and acknowledges it is incomplete.

The FHIR API (separate from the EHI export) covers standard USCDI v1 clinical data: demographics, allergies, care plans, care teams, conditions, devices, diagnostic reports, labs, goals, immunizations, medications, smoking status, procedures, provenance, and vital signs. If the C-CDA export covers similar content, it would provide a clinical summary per encounter — but this is inference, not evidence.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | C-CDA header would include patient demographics, but no field-level detail provided | Product stores demographics ((a)(5) certified); C-CDA header likely covers basics but custom fields unknown |
| Encounters / visits | ⚠️ Partial | Export is organized per-encounter (one C-CDA per encounter), so encounters are structurally present | Encounter metadata likely present but depth unknown |
| Problems / conditions / diagnoses | ⚠️ Partial | FHIR API documents Condition resources; C-CDA likely includes Problems section | Probable coverage via C-CDA but unverified |
| Medications / prescriptions | ⚠️ Partial | CPOE (a)(1) certified; FHIR API documents MedicationRequest; C-CDA likely includes Medications section | Probable coverage via C-CDA; unclear if RXNT e-prescribing data is included |
| Allergies | ⚠️ Partial | FHIR API documents AllergyIntolerance; C-CDA likely includes Allergies section | Product does NOT certify for allergy list (a)(8); may store allergy data but extent unclear |
| Immunizations | ⚠️ Partial | FHIR API documents Immunization resource | Probable coverage via C-CDA but unverified |
| Vitals | ⚠️ Partial | FHIR API documents Vital Signs; C-CDA likely includes Vitals section | Product does NOT certify for vital signs (a)(4); data availability unclear |
| Lab results | ⚠️ Partial | FHIR API documents Laboratory Result Observation | Product does NOT certify for lab results (a)(3); may receive results but doesn't generate them |
| Imaging / diagnostic reports | ⚠️ Partial | FHIR API documents DiagnosticReport/DocumentReference | Product does NOT certify for imaging (a)(12)–(a)(13); likely limited |
| Procedures | ⚠️ Partial | FHIR API documents Procedure resource | Probable coverage via C-CDA but unverified |
| Clinical notes / documents | ⚠️ Partial | Core product function is clinical documentation. EHI PDF says "other files attached to the patient's chart will be added later" — implying custom notes/PDFs are NOT yet exported | **Significant gap.** Clinical documentation is OneConnect's primary purpose. C-CDA sections may capture some note content, but the vendor's custom templates, voice-recognized notes, and shorthand documentation likely cannot be faithfully represented in C-CDA format |
| Care plans / goals | ⚠️ Partial | FHIR API documents CarePlan and Goal resources | Probable coverage via C-CDA but unverified |
| Orders / referrals | ⚠️ Partial | CPOE for meds certified; orders may appear in C-CDA | Limited to what C-CDA supports |
| Insurance / coverage | ❌ Not covered | No mention in export documentation or FHIR API | Unclear if product stores insurance data; no evidence of coverage |
| Claims / billing | ❌ Not covered | No billing entities in export. C-CDA has no billing section | Related BOLT platform captures CPT codes; unclear if OneConnect stores billing data. If it does, this is a gap |
| Payments | ❌ Not covered | No mention | N/A — product is a documentation tool, not a billing system |
| Consents / directives | ❌ Not covered | No mention | Not a primary product function; likely N/A |
| Patient communications / portal messages | ❌ Not covered | No patient portal ((e)(1) not certified) | N/A — product has no patient portal |
| Specialty-specific (post-acute care) | ❌ Not covered | OneConnect is designed for post-acute care with specialty workflows. No specialty-specific data in C-CDA | **Significant gap.** Post-acute documentation workflows, custom templates, facility-specific forms — the product's core differentiator — are not represented in a standard C-CDA export |

**Note**: Nearly all "Partial" ratings above are based on inference from the FHIR API documentation, not from evidence about the actual (b)(10) export. The EHI export documentation itself provides zero field-level detail. Every domain is rated ⚠️ rather than ✅ because we cannot verify what C-CDA sections the vendor actually populates.

## 6. Documentation Quality

**Extremely poor.** The EHI export documentation is 1 page with 6 sentences. It:

- ❌ Provides no data dictionary
- ❌ Provides no schema or machine-readable artifact
- ❌ Provides no sample data
- ❌ Provides no instructions for performing the export
- ❌ Provides no information about which C-CDA sections are populated
- ❌ Provides no field-level documentation
- ❌ Provides no value sets or coded vocabularies
- ❌ Provides no relationship documentation
- ❌ Explicitly states the export is incomplete ("will be added later")

A developer could not build an import from this documentation. They would not know which C-CDA template is used, what sections are populated, what coded values appear, how encounters are organized in the ZIP, or how to request an export.

The only useful information is that the export format is "ZIP of C-CDAs per encounter" — a developer familiar with C-CDA could parse the files, but they would be working blind regarding what content to expect.

The 58-page FHIR API Specifications document is well-structured by comparison, with endpoint URLs, request/response examples, and field descriptions — but it documents the (g)(10) API, not the (b)(10) EHI export.

## 7. Overall Assessment

### Classification

**Minimal/stub**

The EHI export documentation is 6 sentences with no data dictionary, no schema, and no sample data. The export itself is a C-CDA repackaging (one C-CDA per encounter in a ZIP) that the vendor explicitly acknowledges is incomplete. This is the minimum artifact needed to claim compliance, not a genuine effort to enable EHI portability.

### Key Findings

1. **The entire EHI export documentation is 6 sentences on 1 page** (`EHI-Export.pdf`, created 2023-11-07). It defines what ZIP, PDF, and C-CDA are, then states the export is a ZIP of C-CDAs. There is no data dictionary, no schema, no instructions, and no sample data.

2. **The export is explicitly acknowledged as incomplete.** The documentation states: "It contains zip files of C-CDAs for now and other files attached to the patient's chart will be added later (e.g. PDF and images)." This was written in November 2023 — over two years ago — with no evidence of updates.

3. **The export is a C-CDA repackaging, not a native data model export.** C-CDA is a clinical summary standard designed for transitions of care. It cannot represent the full breadth of data a clinical documentation tool stores — custom templates, voice-recognized notes, billing codes, quality measures, and post-acute specialty workflows are all outside C-CDA's scope.

4. **The product's core differentiator — streamlined clinical documentation for post-acute care — is likely the biggest gap.** OneConnect's value proposition is custom documentation workflows with templates, shorthand, and voice recognition. Standard C-CDA sections cannot faithfully represent this vendor-specific content.

5. **This is consistent with an internally-used product by a small physician practice**, not a commercial health IT vendor. MedOne built OneConnect for its own clinicians and obtained certification as a regulatory requirement. The documentation quality reflects minimal compliance effort rather than user-facing product documentation.

### Summary Stats

```
Classification:  Minimal/stub
Export format:   C-CDA (per encounter) in ZIP archive
Model type:      Standard projection (C-CDA)
Entities:        N/A (no data dictionary)
Fields:          N/A (no data dictionary)
Descriptions:    N/A
Sample data:     No
Bulk export:     Unclear
Domains covered: 0 of 12 applicable domains confirmed (up to 10 partially inferred from FHIR API)
```

### Bottom Line

A patient or provider would receive a set of C-CDA clinical encounter summaries — standard clinical data in a standard format — but the vendor provides no documentation of what's actually in those documents and explicitly acknowledges the export is incomplete. The single biggest gap is the product's core function: post-acute clinical documentation built on custom templates and workflows, which standard C-CDA cannot represent. This is a compliance checkbox, not a usable EHI export.
