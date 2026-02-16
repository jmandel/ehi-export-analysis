# EHI Export Analysis: CorrecTek

**Product**: Spark 7.1
**Analysis date**: 2026-02-16
**CHPL IDs**: 15.05.05.1292.CORT.01.00.1.200114 (CHPL ID 10274)

## 1. Product Context

CorrecTek Spark is a full-featured EHR purpose-built for **correctional healthcare, juvenile detention, and behavioral health** settings. It serves 120+ organizations across 30+ U.S. states. Spark integrates medical, dental, and behavioral health records into a unified patient chart and includes:

- **Clinical**: Charting, clinical notes, problem lists, medications (eMAR, EPCS e-prescribing), lab and imaging orders/results, allergies, immunizations, vital signs, care plans
- **Correctional-specific**: Intake screenings, sick call management (via phones/kiosks/tablets), custody/tracking data from jail management systems, NCCHC/ACA/AJA compliance workflows, US Marshals documentation
- **Billing**: Full revenue cycle — eligibility checks, automatic code assignment, claim submission (Medicare/Medicaid/private), ERA posting, Medicaid 1115 waiver support
- **Specialty**: Behavioral health documentation, dental records, juvenile-specific features (release planning, guardian portal, immunization registry)
- **CPOE**: Medication, laboratory, and imaging orders
- **Reporting**: Hundreds of prebuilt reports; optional Power BI dashboard

This is a broad product with significant data domains beyond standard clinical summaries. A credible (b)(10) export would need to cover clinical, billing, correctional-specific, dental, and behavioral health data.

## 2. Artifacts Reviewed

| Artifact | Description | Informative? |
|---|---|---|
| `downloads/cost-disclosure-page-text.txt` (2.1 KB) | Full text of CorrecTek's Cost Disclosure & Transparency page, containing the complete b(10) EHI export documentation — a single sentence | **Most informative** — this is the entirety of the EHI export documentation |
| `downloads/screenshot-ehi-text.png` (18 KB) | Screenshot of the truncated EHI footnote text on the live page | Confirms the text truncation issue (cuts off at "the us") |
| `downloads/screenshot-full-page.png` (1.0 MB) | Full-page screenshot of the disclosure page | Confirms page layout and context |
| `downloads/screenshot-ehi-section.png` (2.4 KB) | Screenshot of the §170.315(b)(10) certification label | Confirms the criterion is listed |
| `downloads/fhirR4endpoints-umc.json` (99 bytes) | Empty FHIR R4 endpoints Bundle | Not relevant to b(10); this is the g(10) API endpoint list, and it's empty |

**Bottom line on artifacts**: There are no data dictionaries, schemas, sample export files, user guides, or any technical documentation beyond the single sentence. The entire collection confirms the absence of substantive documentation.

## 3. Export Mechanics

- **Format**: PDF and/or C-CDA (documentation says "PDF or C-CDA format" — unclear if user chooses or both are produced)
- **Mechanism**: Unclear — documentation says only that "records for a patient are exported to one or more PDF/C-CDA files" saved "to a folder specified by the user," implying a UI-driven export to a local directory
- **Scope**: Single-patient ("records for a patient")
- **Bulk capability**: No mention of bulk/population-level export
- **Access constraints/fees**: Not specified for EHI export specifically; Spark requires software license fees, implementation fees, and annual maintenance fees

The complete export documentation is this single sentence:

> *EHI can be exported in PDF or C-CDA format. Records for a patient are exported to one or more PDF/C-CDA files. The files created by the export are saved to a folder specified by the user.*

## 4. Export Content: What's In It

### What the documentation tells us

**Nothing specific.** There is no data dictionary, no list of exported entities or fields, no schema, no sample data, and no description of what clinical or non-clinical data is included in the export. The documentation states only the output formats (PDF, C-CDA) and the delivery mechanism (files to a folder).

### Vendor's own content organization

There is no vendor-provided content organization. No tables, entities, fields, categories, or data domains are documented.

| Entity/Table | Fields | Described | Types | Category (vendor's) |
|---|---|---|---|---|
| *(none documented)* | — | — | — | — |

### What can be inferred

Given the stated formats:

- **C-CDA** is a clinical document standard. A standard C-CDA (e.g., CCD or Continuity of Care Document) would typically include: demographics, problems, medications, allergies, immunizations, vital signs, lab results, procedures, and clinical notes. This maps closely to USCDI content.
- **PDF** could contain rendered versions of clinical documents, or potentially additional chart content (scanned documents, forms, notes).

However, C-CDA has no standard representation for:
- Billing records (claims, ERA postings, eligibility data)
- Correctional-specific data (intake screenings, sick call requests, custody/tracking)
- Dental charts
- eMAR administration detail
- Custom compliance forms (NCCHC/ACA/AJA assessments)

Without documentation specifying what data is included, it is impossible to determine whether CorrecTek has extended their C-CDA to cover non-standard domains or is exporting only the standard clinical summary subset.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor provides zero detail about export content. The only information is:
- Export format: PDF or C-CDA
- Export scope: per-patient
- Delivery: files to a user-specified folder

There are no categories, no modules, no sections described. It is impossible to assess depth or breadth from the documentation alone.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | Likely in C-CDA (standard section) but undocumented | Product stores demographics; C-CDA would include basic fields but depth unknown |
| Encounters / visits | ⚠️ Partial | Likely in C-CDA but undocumented | Product stores encounters; coverage uncertain |
| Problems / conditions | ⚠️ Partial | Likely in C-CDA (standard section) but undocumented | Product stores problem lists; likely basic coverage via C-CDA |
| Medications / prescriptions | ⚠️ Partial | Likely in C-CDA (standard section) but undocumented | Product has full eMAR and EPCS; C-CDA likely covers active medications but not detailed eMAR administration records |
| Allergies | ⚠️ Partial | Likely in C-CDA but undocumented | Probably covered |
| Immunizations | ⚠️ Partial | Likely in C-CDA but undocumented | Probably covered |
| Vitals | ⚠️ Partial | Likely in C-CDA but undocumented | Probably covered |
| Lab results | ⚠️ Partial | Likely in C-CDA but undocumented | Product has bidirectional lab interfaces; likely partially covered |
| Imaging / diagnostic reports | ⚠️ Partial | May be in C-CDA but undocumented | Product receives imaging results; uncertain |
| Procedures | ⚠️ Partial | Likely in C-CDA but undocumented | Probably covered |
| Clinical notes / documents | ⚠️ Partial | PDF may include notes; undocumented | Product stores extensive clinical documentation; PDF might capture rendered notes |
| Care plans / goals | ⚠️ Partial | May be in C-CDA but undocumented | Uncertain |
| Orders / referrals | ⚠️ Partial | May be in C-CDA but undocumented | Product has full CPOE; uncertain whether order detail is exported |
| Insurance / coverage | ❌ Not covered | No evidence; C-CDA does not naturally include insurance detail | Product stores insurance/eligibility data; **likely gap** |
| Claims / billing | ❌ Not covered | No evidence; C-CDA/PDF cannot represent billing data | Product has full billing cycle; **significant gap** |
| Payments | ❌ Not covered | No evidence | Product processes ERA/payments; **significant gap** |
| Consents / directives | ⚠️ Partial | May be in C-CDA (advance directives section) but undocumented | Uncertain |
| Patient communications | ❌ Not covered | No evidence | Product has patient/guardian portal; **likely gap** |
| Correctional-specific (intake screenings, sick call, custody data) | ❌ Not covered | No evidence; no C-CDA representation exists for these | Product's core domain; **critical gap** |
| Dental | ❌ Not covered | No evidence; no standard C-CDA dental sections | Product integrates dental records; **significant gap** |
| Behavioral health | ❌ Not covered | No evidence of specialized behavioral health data in export | Product integrates behavioral health; **significant gap** |

**Note**: Every "⚠️ Partial" rating above is generous — it assumes C-CDA includes the standard sections for that domain, but there is zero documentation confirming this. The actual export could be even thinner.

## 6. Documentation Quality

The documentation quality is the worst possible while still technically existing:

- **Data dictionary**: None
- **Field-level documentation**: None
- **Data types / value sets**: None
- **Entity relationships**: None
- **Sample data**: None
- **Machine-readable schemas**: None
- **User guide / export instructions**: None (only "saved to a folder specified by the user")
- **C-CDA profile/template specification**: None (no version, no document type, no section list)

A developer receiving this export would have **no way to**:
- Know what data to expect before requesting an export
- Parse the C-CDA reliably (no profile or template guidance)
- Verify export completeness against a reference
- Build an automated import pipeline

The documentation is a single truncated sentence on a general-purpose mandatory disclosures page. It provides no actionable technical information whatsoever.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Minimal/stub/unclear**

The documentation is far too thin to assess what the export actually contains. However, the choice of PDF and C-CDA as the only export formats strongly suggests the export covers only standard clinical summary data — the USCDI floor. CorrecTek Spark stores extensive correctional-specific, dental, behavioral health, and billing data that has no natural representation in C-CDA. There is no evidence of any effort to export these domains. The single-sentence documentation with no data dictionary, no schema, and no sample data indicates this is a compliance checkbox, not a genuine EHI export effort.

**Axis 2 — Export approach: Repackaged existing export**

The export uses the same formats available for clinical exchange (C-CDA) and document sharing (PDF). These are the formats CorrecTek already uses for transitions of care [(b)(1)] and clinical information exchange. There is no evidence of any purpose-built export mechanism, no database dump, no custom schema, no additional data domains beyond what C-CDA naturally carries. The lack of any documentation beyond a single sentence further indicates this is an existing capability (C-CDA generation + PDF rendering) relabeled as (b)(10) rather than a purpose-built EHI export.

### Key Findings

1. **The entire EHI export documentation is a single sentence** — "EHI can be exported in PDF or C-CDA format. Records for a patient are exported to one or more PDF/C-CDA files. The files created by the export are saved to a folder specified by the user." This is among the thinnest (b)(10) documentation possible. (Source: `downloads/cost-disclosure-page-text.txt`)

2. **No data dictionary, schema, or sample data exists.** There is zero technical documentation about what data is actually exported — no entities, no fields, no types, no descriptions. (Source: exhaustive search of the vendor's website, including sitemap, common URL paths, and Wayback Machine historical captures)

3. **Export formats (PDF/C-CDA) cannot represent the product's full data scope.** Spark stores correctional-specific data (intake screenings, sick call, custody tracking), dental records, behavioral health records, and full billing cycle data — none of which have standard C-CDA representations. No additional export format is offered for these domains. (Source: `product-research.md` vs. `downloads/cost-disclosure-page-text.txt`)

4. **The live documentation page has a text truncation bug.** The b(10) footnote is cut off at "the us" — the complete text "the user." was confirmed only via Wayback Machine. This suggests minimal attention to the (b)(10) requirement. (Source: `downloads/screenshot-ehi-text.png`, Wayback Machine 2024-04-18 capture per `ehi-export-report.md`)

5. **The FHIR endpoints file is empty.** The only linked technical artifact (`fhirR4endpoints-umc.json`) contains an empty FHIR Bundle with no entries, suggesting the g(10) API may not be actively deployed either. (Source: `downloads/fhirR4endpoints-umc.json`)

### Summary Stats

```
Coverage:        Minimal/stub/unclear
Approach:        Repackaged existing export
Export format:   PDF, C-CDA
Entities:        N/A (no data dictionary)
Fields:          N/A
Descriptions:    N/A
Sample data:     No
Bulk export:     No (single-patient only)
Domains covered: 0 of 19 confirmed; ~10 of 19 plausibly partial via C-CDA but undocumented
```

### Bottom Line

CorrecTek's (b)(10) EHI export documentation is a single sentence with no data dictionary, no schema, and no sample data. The PDF/C-CDA export format almost certainly delivers only standard clinical summary data (the USCDI floor), while the product stores extensive correctional-specific, dental, behavioral health, and billing data that C-CDA cannot represent. This is one of the weakest (b)(10) implementations possible — a compliance checkbox rather than a genuine effort to make patient data portable.
