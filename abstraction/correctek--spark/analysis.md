# EHI Export Analysis: CorrecTek

**Product**: Spark 7.1
**Analysis date**: 2026-02-16
**CHPL ID**: 10274 (15.05.05.1292.CORT.01.00.1.200114)

## 1. Product Context

CorrecTek Spark is a purpose-built EHR for **correctional healthcare, juvenile detention, and behavioral health** settings. Founded in 2006 and based in Paducah, Kentucky, CorrecTek serves over 120 organizations across 30+ U.S. states. Spark is their single product — the certified module IS the entire EHR.

Spark is a full-featured system that stores and manages:

- **Clinical data**: Demographics, encounters, clinical notes, problem lists, allergies, immunizations, vital signs, clinical assessments, care plans, referrals
- **Unified health record**: Integrates medical, dental, and behavioral health records in a single patient chart
- **Medication management**: eMAR, EPCS-certified e-prescribing (via NewCrop), SureScripts integration, pharmacy interfaces
- **Orders and results**: Lab orders/results (bidirectional), radiology orders/results (bidirectional with optional images)
- **Integrated billing**: Full billing cycle — eligibility checks, auto code assignment, claim submission (Medicare/Medicaid/private), ERA posting, Medicaid 1115 waiver support
- **Correctional-specific**: Intake screenings, sick call management (phone/kiosk/tablet), inmate tracking/custody data (from JMS/OMS), NCCHC/ACA/AJA compliance forms
- **Juvenile-specific**: Release planning, medication compliance tracking, guardian portal, immunization registry verification

This is a data-rich application. A genuine EHI export would need to cover clinical data across medical/dental/behavioral health, billing records, correctional intake and compliance forms, medication administration records, and specialty-specific assessments.

## 2. Artifacts Reviewed

| Artifact | Description | Informative? |
|---|---|---|
| `cost-disclosure-page-text.txt` (2,140 bytes) | Full text of CorrecTek's Cost Disclosure & Transparency page. Contains the **entire** EHI export documentation: a single 3-sentence footnote. | **Primary artifact** — confirms the totality of export documentation |
| `screenshot-full-page.png` (1,069,538 bytes) | Full-page screenshot of the cost disclosure page. Confirms page layout and that b(10) is a footnote at the bottom of the certification criteria table. | Corroborates text extract |
| `screenshot-ehi-text.png` (18,319 bytes) | Close-up of the truncated EHI footnote text on the live page (cuts off at "the us"). | Confirms truncation bug on live site |
| `screenshot-ehi-section.png` (2,433 bytes) | Screenshot of the §170.315(b)(10) label in the criteria table. | Minor |
| `fhirR4endpoints-umc.json` (99 bytes) | FHIR R4 endpoints JSON linked from the page. An empty Bundle: `{"resourceType":"Bundle","type":"collection","timestamp":"..."}` with no entries. | Confirms this is for g(10) API, not b(10); no customer endpoints listed |

**No data dictionary, schema, sample data, user guide, or export format specification was found among the artifacts.** The live website was independently verified on 2026-02-16 and confirmed to still contain only the same single-sentence footnote with the same truncation.

## 3. Export Mechanics

Based on the sole documentation available (the footnote on the cost disclosure page):

- **Format**: PDF or C-CDA
- **Mechanism**: Unclear. "Records for a patient are exported to one or more PDF/C-CDA files. The files created by the export are saved to a folder specified by the user." — implies a UI-driven single-patient export to a local filesystem folder.
- **Single-patient vs bulk**: Documentation describes single-patient export ("Records for a patient"). No mention of bulk/population-level export capability.
- **Access constraints or fees**: Not documented. The cost transparency section mentions software license fees, implementation fees, and annual maintenance fees, but does not specifically address EHI export costs.
- **Encryption/integrity**: Not mentioned.

There are no instructions for initiating the export, no screenshots of the export interface, and no details on any configuration options.

## 4. Export Content: What's In It

### What the documentation tells us

The complete EHI export documentation is:

> *EHI can be exported in PDF or C-CDA format. Records for a patient are exported to one or more PDF/C-CDA files. The files created by the export are saved to a folder specified by the user.*

This is **189 characters** of documentation. There is:

- **No data dictionary** — zero entities, zero fields documented
- **No C-CDA template/profile specification** — no indication of which C-CDA document type (CCD, Discharge Summary, Continuity of Care, etc.), which sections are included, or which template versions are used
- **No PDF structure specification** — no indication of whether the PDF is a rendered clinical document, a form printout, or a database dump
- **No schema files** — no XSD, JSON Schema, or other machine-readable format definition
- **No sample data** — no example export files demonstrating actual output
- **No field-level documentation** of any kind

### Vendor's own content organization

There is no vendor-provided content organization. The vendor does not describe any entities, tables, sections, fields, or categories of exported data. The entire documentation is a format statement ("PDF or C-CDA") with no content specification.

| Entity/Table | Fields | Described | Types | Category |
|---|---|---|---|---|
| *(none documented)* | — | — | — | — |

### What can be inferred

The only thing that can be reasonably inferred from "PDF or C-CDA format":

- **C-CDA** is a clinical document standard. A standard C-CDA (e.g., CCD) would typically include: demographics, problems, medications, allergies, immunizations, vital signs, lab results, procedures, and possibly encounters and clinical notes. This represents the USCDI/US Core clinical summary subset.
- **PDF** could contain anything from a simple chart printout to rendered clinical documents. Without specification, its content is unknown.

Neither PDF nor C-CDA is designed to represent billing records, correctional intake forms, eMAR administration records, dental charts, behavioral health assessments, sick call workflows, or custody/tracking data — all of which Spark stores.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor provides **no content specification whatsoever**. The documentation mentions only two export formats (PDF, C-CDA) without describing what data is included in either. There are no categories, no modules, no sections, no entities, no fields.

It is impossible to assess coverage from the documentation alone. The only statement that can be made with confidence is that C-CDA, as a standard, has a defined scope — and that scope does not include billing, correctional-specific, dental-specific, or behavioral-health-specific data structures.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | Likely in C-CDA (standard section), but no confirmation | Spark stores demographics + facility/custody info; C-CDA would cover basic demographics only |
| Encounters / visits | ⚠️ Partial | Likely in C-CDA encounters section, but unconfirmed | Spark documents encounters across medical, dental, behavioral health |
| Problems / conditions | ⚠️ Partial | Likely in C-CDA problem list, but unconfirmed | Standard C-CDA section |
| Medications / prescriptions | ⚠️ Partial | Likely in C-CDA medications section, but unconfirmed | Spark has full eMAR, EPCS, pharmacy interfaces — C-CDA captures medication lists but not administration records |
| Allergies | ⚠️ Partial | Likely in C-CDA allergies section, but unconfirmed | Standard C-CDA section |
| Immunizations | ⚠️ Partial | Likely in C-CDA immunizations section, but unconfirmed | Standard C-CDA section |
| Vitals | ⚠️ Partial | Likely in C-CDA vital signs section, but unconfirmed | Standard C-CDA section |
| Lab results | ⚠️ Partial | Likely in C-CDA results section, but unconfirmed | Spark receives bidirectional lab results |
| Imaging / diagnostic reports | ⚠️ Partial | May be in C-CDA, but unconfirmed | Spark receives radiology results and optional images |
| Procedures | ⚠️ Partial | Likely in C-CDA procedures section, but unconfirmed | Standard C-CDA section |
| Clinical notes / documents | ⚠️ Partial | May be in PDF export; possibly in C-CDA notes section | Spark stores extensive clinical documentation |
| Care plans / goals | ⚠️ Partial | May be in C-CDA, but unconfirmed | Spark supports care plans |
| Orders / referrals | ⚠️ Partial | May be in C-CDA, but unconfirmed | Spark has full CPOE |
| Insurance / coverage | ❌ Not covered | No evidence; C-CDA does not natively represent insurance data | Spark stores eligibility/coverage data — **gap** |
| Claims / billing | ❌ Not covered | No evidence; C-CDA does not represent billing data | Spark has integrated billing (claims, ERA, Medicaid waivers) — **significant gap** |
| Payments | ❌ Not covered | No evidence | Spark processes ERA/payment posting — **gap** |
| Consents / directives | ❌ Not covered | No evidence | Spark likely stores consent data (juvenile guardian consent mentioned) — **gap** |
| Patient communications | ❌ Not covered | No evidence | Spark has patient portal, sick call requests — **gap** |
| Specialty: Correctional intake/screening | ❌ Not covered | No evidence; C-CDA has no representation for correctional forms | Spark stores intake screenings, NCCHC/ACA compliance forms — **significant gap** |
| Specialty: Dental | ❌ Not covered | No evidence; C-CDA has no dental chart representation | Spark integrates dental records in unified chart — **significant gap** |
| Specialty: Behavioral health | ❌ Not covered | No evidence; C-CDA has limited behavioral health support | Spark integrates behavioral health records — **significant gap** |

**Note**: Every clinical domain is marked "⚠️ Partial" rather than "✅ Covered" because there is zero documentation confirming that any specific data is included. The inference that C-CDA includes standard clinical sections is based on the C-CDA standard itself, not on anything CorrecTek has documented. It is possible their C-CDA implementation includes more or fewer sections than a standard CCD.

## 6. Documentation Quality

**Rating: Essentially absent.**

- **Completeness**: The entire EHI export documentation is 3 sentences (189 characters). No data dictionary, no schema, no sample data, no user guide.
- **Actionability**: A developer receiving this export would have no way to know what data to expect, how to parse the C-CDA (which template? which sections? which extensions?), or how to verify completeness.
- **Machine-readable artifacts**: None. The only machine-readable file is the FHIR endpoints JSON, which is an empty Bundle related to the g(10) API, not the b(10) export.
- **Presentation issue**: The EHI documentation text is truncated on the live website (cuts off at "the us"), meaning even the single sentence isn't fully readable without consulting the Wayback Machine.

A developer attempting to build an import from this documentation would have nothing to work with. They would need to receive an actual export file and reverse-engineer its structure.

## 7. Overall Assessment

### Classification

**Minimal/stub**: Documentation is too thin to assess what the export contains. The entire b(10) documentation is a single truncated footnote stating the export format is "PDF or C-CDA" with no content specification, no data dictionary, no schema, and no sample data. The choice of PDF/C-CDA as export formats — rather than a native database export — strongly suggests this covers only a clinical summary subset of the data Spark stores.

### Key Findings

1. **The entire EHI export documentation is 3 sentences (189 characters).** There is no data dictionary, no schema, no sample data, no export guide — just a footnote on the cost disclosure page stating "EHI can be exported in PDF or C-CDA format." This is among the thinnest EHI documentation possible. (Source: `cost-disclosure-page-text.txt`)

2. **The export uses PDF and C-CDA — standard clinical document formats that cannot represent the breadth of data Spark stores.** Spark is a correctional healthcare EHR with integrated billing, dental, behavioral health, eMAR, sick call management, and correctional compliance workflows. C-CDA has no native representation for billing records, correctional intake forms, dental charts, eMAR administration records, or custody data. (Source: `product-research.md`, `cost-disclosure-page-text.txt`)

3. **No content specification exists.** Without any documentation of what data domains, entities, or fields the export includes, it is impossible to assess coverage. There is no way to determine whether billing, dental, behavioral health, or correctional-specific data is exported. (Source: all artifacts reviewed — none contain content specifications)

4. **The live documentation page has a truncation bug.** The EHI footnote text is cut off at "the us" on the live website, meaning the documentation isn't even fully readable. The complete text ("the user.") was confirmed via Wayback Machine. (Source: `screenshot-ehi-text.png`, live site verification 2026-02-16)

5. **The FHIR endpoints JSON is empty.** The only downloadable file linked from the disclosure page is an empty FHIR Bundle with no customer endpoints — this relates to the g(10) API, not the b(10) EHI export. (Source: `fhirR4endpoints-umc.json`)

### Summary Stats

```
Classification:  Minimal/stub
Export format:   PDF, C-CDA
Model type:      Standard projection (C-CDA clinical document)
Entities:        N/A (no data dictionary)
Fields:          N/A (no data dictionary)
Descriptions:    N/A
Sample data:     No
Bulk export:     No (single-patient only per documentation)
Domains covered: 0 of 19 confirmed (up to ~10 inferred from C-CDA standard, but unconfirmed)
```

### Bottom Line

CorrecTek's EHI export documentation is a single truncated sentence offering PDF/C-CDA export with no specification of content. For a correctional healthcare EHR that stores medical, dental, behavioral health, billing, eMAR, and correctional-specific data, a C-CDA-based export almost certainly captures only a clinical summary subset. The complete absence of a data dictionary or any content specification makes it impossible to confirm what is actually exported, but the choice of format and lack of documentation are strong indicators that this is a compliance checkbox rather than a genuine effort to enable complete EHI portability.
