# EHI Export Analysis: MedOne Healthcare Partners

**Product**: OneConnect Version 0
**Analysis date**: 2026-02-15
**CHPL ID**: 11426 (15.04.04.3182.Onec.00.00.1.231227)

## 1. Product Context

OneConnect is a **custom clinical documentation tool** built by MedOne Healthcare Partners (formerly Central Ohio Hospitalists), a physician-owned hospital medicine practice in Columbus, Ohio. It is **not a commercial EHR** — it is an internally developed and internally used tool for MedOne's ~100 physicians and 75+ advanced practice clinicians who provide care across approximately 150 post-acute facilities (skilled nursing, assisted living, rehab, and long-term acute care) in Ohio.

The product is designed as a **documentation overlay** that integrates with a post-acute facility's existing EMR. Its core function is streamlining clinical documentation for providers rounding in post-acute settings. It was built by MedOne's founder, Dr. Joseph Mack, who is both a physician and programmer.

**What OneConnect stores (relevant to export completeness):**
- **Clinical notes/documentation** — the primary data type; the product's core purpose
- **Patient demographics** — certified for (a)(5)
- **Medication orders** — certified for CPOE (a)(1); e-prescribing via third-party RXNT
- **Implantable device information** — certified for (a)(14)
- **Transitions of care documents** — certified for (b)(1)
- **Clinical quality measure data** — 68 CQMs certified (c)(1)

**What OneConnect does NOT certify for** (and likely does not store natively):
- Medication lists (a)(6), allergy lists (a)(8), problem lists (a)(7), vital signs (a)(4), lab orders/results (a)(2)/(a)(3), clinical decision support (a)(9), e-prescribing (a)(10)–(a)(11), patient portal (e)(1), imaging (a)(12)–(a)(13)

This is a narrowly focused documentation tool, not a comprehensive EHR. The expected EHI scope is correspondingly narrow: primarily clinical encounter documentation, demographics, medication orders, implantable devices, and transitions of care data.

## 2. Artifacts Reviewed

| Artifact | Description | Size/Scope | Informativeness |
|---|---|---|---|
| `EHI-Export.pdf` | The sole (b)(10) export documentation | 1 page, 111 words, created 2023-11-07 | **Primary artifact** — extremely minimal |
| `FHIR-API-Specifications.pdf` | SMART on FHIR API documentation for (g)(7)/(g)(9)/(g)(10) | 58 pages, 7,749 words, created 2023-11-28 | Not (b)(10) documentation; useful for understanding what FHIR resources the system supports |
| `FHIR_Valid_URLs.json` | FHIR Bundle with Endpoint and Organization resources | 2,235 bytes, 2 entries | Infrastructure metadata only |
| `certifications-page-screenshot.png` | Screenshot of medonehp.com/certifications page | 367 KB | Confirms page layout and links to documentation |

**Most informative**: `EHI-Export.pdf` (the only (b)(10) artifact, though extremely thin).
**Least informative**: `FHIR_Valid_URLs.json` (infrastructure metadata, not relevant to EHI export).

## 3. Export Mechanics

- **Format**: ZIP archive containing C-CDA documents, one per patient encounter. The documentation states "other files attached to the patient's chart will be added later (e.g. PDF and images)" — indicating the export was incomplete as of the documentation date (November 2023).
- **Mechanism**: Not documented. There are no instructions for how to initiate, request, or receive an export. No UI screenshots, no API endpoint, no process description.
- **Single-patient vs bulk**: Not documented. The text refers to "the patient EHI export," suggesting single-patient scope, but this is ambiguous.
- **Access constraints or fees**: Not documented.

## 4. Export Content: What's In It

### What the documentation says

The entire EHI export documentation is **6 substantive sentences** on a single page (verified via `pdftotext`). The full text is:

> Product Name and Version: OneConnect Version 0
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

Three of these sentences merely define what ZIP, PDF, and C-CDA are. The substantive content is:
1. The export contains "data from the patient's chart"
2. The format is a ZIP of C-CDA documents, one per encounter
3. PDFs and images "will be added later" (i.e., are not currently included)

### What we can infer

There is **no data dictionary**, **no schema**, **no field-level documentation**, **no sample export file**, and **no list of C-CDA sections or templates used**. It is impossible to determine from this documentation exactly what data elements are included in the C-CDA documents.

The FHIR API Specifications PDF (not a (b)(10) artifact) documents 16 FHIR resource types the system can serve, which gives an indirect signal about what data the system stores:

- Patient, AllergyIntolerance, CarePlan, CareTeam, Conditions/Problems, Implantable Device, Diagnostic Report, DocumentReference, Clinical Notes, Laboratory Result Observation, Goal, Immunization, Medication, Smoking Status, Procedure, Provenance, Vital Signs

However, it is unclear whether the C-CDA export includes data for all these resource types or only a subset. The FHIR API documentation is for the (g)(10) standardized API, not the (b)(10) export.

### Vendor's own content organization

The vendor provides no content organization. There is no data dictionary, no entity list, no table structure, and no field inventory. The export cannot be broken down into entities or fields because no such documentation exists.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor describes exactly one thing: a ZIP archive of C-CDA documents organized by encounter. No categories, no modules, no sections are described. The documentation is so thin that coverage assessment must be based entirely on inference from the export format (C-CDA) rather than from any vendor-provided detail.

Standard C-CDA documents (CCD, Discharge Summary, etc.) typically include sections for:
- Demographics, problems, medications, allergies, immunizations, vital signs, procedures, results, plan of care, encounters, social history

But without knowing which C-CDA template OneConnect uses or which sections it populates, we cannot confirm any specific coverage.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | C-CDA header typically includes demographics, but no field-level detail provided | Product stores demographics (a)(5) certified; C-CDA likely includes basic demographics but completeness unknown |
| Encounters / visits | ⚠️ Partial | Documentation says "one C-CDA per encounter" | Structure implies encounters are represented, but detail level unknown |
| Problems / conditions | ⚠️ Partial | C-CDA standard section; FHIR API supports Conditions | Likely in C-CDA if populated, but product not certified for problem lists (a)(7) |
| Medications / prescriptions | ⚠️ Partial | C-CDA standard section; CPOE (a)(1) certified | CPOE certified so medication orders exist; C-CDA medication section likely present but e-prescribing data from RXNT may not be included |
| Allergies | ⚠️ Partial | C-CDA standard section; FHIR API supports AllergyIntolerance | Not certified for allergy lists (a)(8); may or may not be populated |
| Immunizations | ⚠️ Partial | C-CDA standard section | Not a core function of a post-acute documentation tool; likely thin |
| Vitals | ⚠️ Partial | C-CDA standard section | Not certified for vitals (a)(4); may or may not be populated |
| Lab results | ⚠️ Partial | C-CDA standard section | Not certified for lab results; product likely receives but may not store lab data natively |
| Imaging / diagnostic reports | ❌ Not covered | No evidence | Not certified for imaging; N/A for this product |
| Procedures | ⚠️ Partial | C-CDA standard section | May include basic procedure data if documented |
| Clinical notes / documents | ⚠️ Partial | C-CDA may include notes; documentation promises PDFs "later" | **This is the product's core function** — clinical documentation. C-CDA's rigid structure likely cannot represent OneConnect's custom templates, voice-recognition-generated notes, and shorthand documentation. The documentation explicitly says PDFs/images "will be added later," suggesting clinical document attachments are NOT currently exported. **Significant potential gap.** |
| Care plans / goals | ⚠️ Partial | C-CDA standard section | May be present if populated |
| Orders / referrals | ⚠️ Partial | C-CDA may include | CPOE certified; orders may appear in C-CDA medication section |
| Insurance / coverage | ❌ Not covered | No evidence in C-CDA export | C-CDA does not have a standard insurance/coverage section. Unknown if product stores this data. |
| Claims / billing | ❌ Not covered | No evidence in C-CDA export | The related BOLT platform captures CPT codes; unclear if OneConnect does. C-CDA has no billing section. If OneConnect stores billing data, this is a gap. |
| Payments | N/A | — | No evidence OneConnect handles payments |
| Consents / directives | ⚠️ Partial | C-CDA may include advance directives section | Unknown if populated |
| Patient communications | N/A | — | No patient portal; not applicable |
| Implantable devices | ⚠️ Partial | C-CDA may include; (a)(14) certified | Certified for implantable device list; likely in C-CDA but no field detail |

**Critical note**: Every "⚠️ Partial" rating above is generous — it assumes the C-CDA contains standard sections. Without sample data or a list of populated sections, the actual coverage could be significantly less. The ratings reflect what C-CDA *can* contain, not what this vendor's C-CDA *does* contain.

## 6. Documentation Quality

The EHI export documentation quality is **extremely poor** — among the thinnest possible for a certified product.

**What's missing:**
- No instructions for performing or requesting an export
- No data dictionary or field inventory
- No C-CDA template identification (CCD? Discharge Summary? Custom?)
- No list of populated C-CDA sections
- No field-level mapping or descriptions
- No data types, value sets, or coded terminology references
- No entity relationships
- No sample export file
- No machine-readable schema
- No versioning or change history

**What's present:**
- The export format (ZIP of C-CDAs) — 1 sentence
- Definitions of ZIP, PDF, and C-CDA — 3 sentences
- An admission that the export is incomplete — 1 sentence

**Could a developer build an import from this documentation?** No. A developer would know only that they're receiving a ZIP file containing C-CDA XML documents. They would need to determine the C-CDA template, parse the XML, discover which sections are populated, and map the data — all without any guidance from the vendor. While C-CDA is a standard, implementations vary widely in which sections are included and how data is coded.

## 7. Overall Assessment

### Classification

**Minimal/stub**: The documentation is too thin to meaningfully assess the export content. The export is described as C-CDA documents per encounter — a standard-based projection that inherently cannot represent the full breadth of OneConnect's native data model (particularly custom clinical documentation, the product's core value proposition). The documentation explicitly acknowledges incompleteness ("will be added later"). There is no data dictionary, no schema, no sample data, and no process documentation.

### Key Findings

1. **The entire (b)(10) documentation is 111 words on 1 page** (`EHI-Export.pdf`, created 2023-11-07). Three of six substantive sentences merely define file format acronyms. This is among the most minimal export documentation possible for a certified product.

2. **The export is C-CDA per encounter — a standard-based projection, not a native data export.** C-CDA is a clinical summary standard that cannot represent billing data, custom documentation templates, or vendor-specific workflow data. For a product whose core value is streamlined clinical documentation with custom templates and voice recognition, C-CDA is structurally inadequate to capture the full record.

3. **The vendor explicitly acknowledges the export is incomplete**: "It contains zip files of C-CDAs for now and other files attached to the patient's chart will be added later (e.g. PDF and images)." This statement, dated November 2023 (over 2 years ago), suggests the export was a work-in-progress at certification time and was never updated.

4. **No sample data, no data dictionary, no process documentation.** It is impossible to verify from the available artifacts what data elements the C-CDA documents actually contain, how to request an export, or what format the ZIP structure takes.

5. **Context mitigates the severity somewhat**: OneConnect is a narrowly focused documentation overlay used internally by one physician practice, not a comprehensive commercial EHR. The scope of EHI it stores is correspondingly narrow. However, even for its narrow scope, the documentation fails to describe how the product's core data (clinical encounter documentation) is faithfully represented in C-CDA format.

### Summary Stats

```
Classification:  Minimal/stub
Export format:   C-CDA (XML) in ZIP archive
Model type:      Standard projection (C-CDA)
Entities:        N/A (no data dictionary)
Fields:          N/A (no data dictionary)
Descriptions:    N/A
Sample data:     No
Bulk export:     Unclear
Domains covered: 0 of 13 confirmed; up to 11 of 13 inferred from C-CDA format (but unverifiable)
```

### Bottom Line

A patient or provider requesting an EHI export from OneConnect would receive a ZIP file of C-CDA documents with no guidance on what's inside, no way to verify completeness, and an explicit vendor admission that the export is incomplete. The single biggest gap is the complete absence of documentation — not just thin documentation, but effectively *no* documentation beyond stating the file format. For a product whose primary value is custom clinical documentation, exporting only C-CDA summaries (without even confirming which sections are populated) raises serious questions about whether the full designated record set is captured.
