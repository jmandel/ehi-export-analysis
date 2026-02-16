# EHI Export Analysis: Perk Medical Systems LLC (PCB Apps LLC)

**Product**: ezPractice V15.1
**Analysis date**: 2026-02-16
**CHPL IDs**: 15.07.04.2154.Ezpr.15.01.1.230208

## 1. Product Context

ezPractice is a certified ambulatory EHR developed by Perk Medical Systems LLC (operating through PCB Apps LLC) and hosted via the PennClinical platform (penn-clinical.com). The product is designed for pediatric practices (per CHPL SED metadata) and appears to serve an extremely small market — possibly only the developer's own practice(s). There are no third-party reviews, no visible customer base, and the developer entity (Perk Medical Systems) is a 3-employee primary care clinic in Somerset, NJ.

The EHI export documentation itself states the product portfolio includes: **Certified EHR**, **Practice Management**, **Patient Portal**, and **Health Information Exchange**, with services including **Revenue Cycle Management** and **Professional Services** (source: `EHI Export.pdf`, page 4, Executive Summary). This is significant because it establishes that the product handles both clinical and billing/PM data — all of which should be exportable.

Certified capabilities include CPOE for medications, labs, and imaging orders; drug-drug/drug-allergy interaction checks; demographics; clinical decision support; family health history; implantable device list; transitions of care (C-CDA); FHIR API; clinical quality measures; patient health information capture; and Direct messaging. E-prescribing is handled via third-party DrFirst Rcopia.

The baseline expectation: the export should cover clinical data across all certified criteria, plus billing/practice management data from the integrated PM module, plus any patient portal content.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `EHI Export.pdf` (289 KB, 7 pages) | Primary EHI export documentation. Created 2023-12-20 in Microsoft Word. ~3 pages of substantive content after cover page, copyright boilerplate, and legal disclaimers. Describes export mechanism, file naming, and format details. | **Primary source** — this is the only substantive artifact |
| `fhir-base-urls.csv` (263 bytes) | CSV with 4 rows listing test and production FHIR server endpoints. Production URLs listed as "available upon request." Documents the (g)(10) FHIR API, not the (b)(10) EHI export. | **Not relevant** to EHI export assessment |
| `ehi-export-page.png` / `ehi-export-page-full.png` | Screenshots of the penn-clinical.com/ehi-export page showing "Download PDF" link and embedded PDF viewer (page 1/7). PennClinical header with nav: Home, Products, Services, About Us, Contact Us, ONC dropdown. | **Contextual** — confirms delivery mechanism |

The EHI export page (https://penn-clinical.com/ehi-export) was verified live as of 2026-02-16 (HTTP 200). The PDF remains downloadable.

**Bottom line**: The entire EHI export documentation consists of a single 7-page PDF, of which roughly 3 pages contain substantive export information. There are no sample data files, no schemas, no data dictionaries, and no supplementary artifacts.

## 3. Export Mechanics

- **Format**: ZIP file(s) containing a mix of C-CDA R2.1 XML (with paired HTML rendering), CSV, and CDA XML with Base64-encoded documents
- **Mechanism**: Self-service export available through the EHR UI. Vendor-assisted export also available.
- **Scope**: Single patient or full collection of patients (bulk capability confirmed in documentation)
- **Fees**: No fees for self-service export. Vendor-assisted export "may" incur fees based on time and effort.
- **Access constraints**: Valid user subscription required

File naming follows: `PID_INTERNALNUMBERING.EXT` or `PID_INTERNALNUMBERING_TYPE.EXT`, where TYPE can be `Claim Data`, `Echart`, or `patNotes`.

## 4. Export Content: What's In It

The export documentation describes **four** categories of exported content, but only **one** has field-level documentation:

### Vendor's own content organization

The PDF organizes the export into three explicitly documented categories plus one implicitly mentioned category:

| Category | Format | Fields Documented | Fields with Descriptions | Documentation Level |
|---|---|---|---|---|
| Patient Demographics and Clinical Data | C-CDA R2.1 XML + HTML | 0 (defers to C-CDA spec) | 0 | Spec reference only |
| Adhoc Patient Notes | CSV | 7 | 7 (100%) | Field-level with descriptions |
| Scanned Records | CDA XML (Base64) | 0 (defers to CDA spec) | 0 | Spec reference only |
| Claim Data | Unknown | 0 | 0 | **Completely undocumented** |

**Total documented fields across all categories: 7** (all from the patient notes CSV).

#### Patient Demographics and Clinical Data (C-CDA R2.1)
The documentation states these files "follow the specification as set for HL7 C-CDA R2.1 specifications" and provides two external references. No ezPractice-specific documentation explains which C-CDA sections are populated, how the product's data maps to C-CDA elements, or what vendor-specific extensions (if any) are used. The C-CDA standard covers demographics, medications, allergies, problems, procedures, lab results, vital signs, immunizations, and clinical notes — but the actual content of these files depends entirely on what ezPractice chooses to populate, which is undocumented.

#### Adhoc Patient Notes (CSV)
The only category with field-level documentation. Seven columns are described:

1. **PID** — Patient ID (unique)
2. **Patient Notes ID** — Note ID (unique)
3. **Username** — User who documented the note
4. **Subject** — Subject of the note (may be blank)
5. **Patient Notes Category** — User-defined category from pick list
6. **Patient Notes Date** — Date note was created
7. **Patient Notes** — Note content

Note: The PDF has a numbering error — column numbers are printed as 1, 2, 3, 3, 4, 5, 6 (the "Subject" column is misnumbered as 3, duplicating "Username"). The actual column count is 7.

#### Scanned Records (CDA XML with Base64)
Files with TYPE value "Echart" contain Base64-encoded scanned and uploaded documents in CDA format. No documentation beyond the external CDA spec reference. The documentation warns these files "could be large in size depending on the amount of scanned data."

#### Claim Data (Undocumented)
The file naming convention section lists "Claim Data" as a valid TYPE value (page 5 of the PDF), confirming that billing/claims data is part of the export output. However, there is **zero documentation** of claim data: no format description, no field definitions, no schema reference, no sample. A recipient of claim data files would have no way to interpret them from this documentation alone.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor describes three documented content types plus one undocumented one:

1. **C-CDA clinical/demographic data** — The broadest category but entirely undocumented beyond citing the C-CDA spec. This likely covers standard clinical summary content (demographics, medications, allergies, problems, procedures, vitals, immunizations, lab results) but the documentation provides no confirmation of which sections are actually populated.

2. **Adhoc patient notes (CSV)** — A genuinely supplementary export beyond C-CDA. This captures telephone calls, miscellaneous patient notes, and other ad-hoc documentation that wouldn't appear in a C-CDA clinical summary. The 7-field schema is simple but adequately documented.

3. **Scanned records** — Base64-encoded documents in CDA format. This captures uploaded/scanned documents, extending the export beyond structured clinical data. However, the documentation provides no guidance on decoding or interpreting these files beyond the CDA spec reference.

4. **Claim data** — Mentioned as a file TYPE but completely undocumented. This is the most significant documentation gap: the product's own executive summary states it includes Practice Management and Revenue Cycle Management, and the export explicitly includes claim data files, yet there is no documentation of their format or content.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | Presumed in C-CDA files; no product-specific field documentation | C-CDA typically includes basic demographics; depth unknown without sample data |
| Encounters / visits | ⚠️ Partial | Presumed in C-CDA Encounters section | No confirmation of which encounter data is included |
| Problems / conditions / diagnoses | ⚠️ Partial | Presumed in C-CDA Problems section | Product certified for (a)(9) CDS which implies problem lists; coverage unverified |
| Medications / prescriptions | ⚠️ Partial | Presumed in C-CDA Medications section | Product certified for CPOE meds (a)(1); e-prescribing via DrFirst Rcopia — unclear if Rcopia data is captured in export |
| Allergies | ⚠️ Partial | Presumed in C-CDA Allergies section | Product certified for drug-allergy checks (a)(4); coverage unverified |
| Immunizations | ⚠️ Partial | Presumed in C-CDA Immunizations section | Pediatric product; immunizations should be heavily used; coverage unverified |
| Vitals | ⚠️ Partial | Presumed in C-CDA Vital Signs section | Coverage unverified |
| Lab results | ⚠️ Partial | Presumed in C-CDA Results section | Product certified for CPOE labs (a)(2); coverage unverified |
| Imaging / diagnostic reports | ⚠️ Partial | Presumed in C-CDA if included; possibly in scanned records | Product certified for CPOE imaging (a)(3); coverage unverified |
| Procedures | ⚠️ Partial | Presumed in C-CDA Procedures section | Coverage unverified |
| Clinical notes / documents | ⚠️ Partial | Adhoc notes exported via CSV (7 fields); scanned records via CDA/Base64 | CSV covers ad-hoc notes; structured clinical notes (progress notes, H&P) presumably in C-CDA but unconfirmed |
| Care plans / goals | ❌ Not covered | No evidence in export documentation | Product may store care plans; no export evidence |
| Orders / referrals | ❌ Not covered | No evidence in export documentation | Product certified for CPOE (a)(1-3); orders likely stored but not explicitly exported |
| Insurance / coverage | ❌ Not covered | No evidence in export documentation | Product includes Practice Management (per executive summary); insurance data likely stored but not documented in export |
| Claims / billing | ⚠️ Partial | "Claim Data" listed as file TYPE in naming convention (p.5); no format/field documentation | Product explicitly offers Practice Management and Revenue Cycle Management; claim data files are generated but completely undocumented |
| Payments | ❌ Not covered | No evidence in export documentation | Product offers Revenue Cycle Management; payment data likely stored but not mentioned |
| Family health history | ⚠️ Partial | Presumed in C-CDA if included | Certified for (a)(12); coverage unverified |
| Implantable devices | ⚠️ Partial | Presumed in C-CDA if included | Certified for (a)(14); coverage unverified |
| Patient communications / portal | ❌ Not covered | No evidence in export documentation | Product includes Patient Portal (per executive summary); portal messages not mentioned |
| Consents / directives | ❌ Not covered | No evidence in export documentation | Likely not a significant gap for small pediatric practice |
| Specialty-specific (Pediatric) | ❌ Not covered | No evidence of pediatric-specific data in export | Product designed for pediatric use (per SED metadata); growth charts, well-child visits, developmental screenings are standard pediatric data — none documented in export |

**Summary**: 0 domains have confirmed full coverage. 11 domains have partial/presumed coverage (relying entirely on the assumption that C-CDA files contain standard sections, unverified). 8 domains have no coverage evidence. The fundamental problem is that the C-CDA approach means we must _assume_ coverage rather than _confirm_ it.

## 6. Documentation Quality

The documentation quality is **poor**:

- **Data dictionary**: Effectively none. Only the 7-field patient notes CSV is documented. The primary clinical data export (C-CDA) provides zero product-specific documentation, deferring entirely to external C-CDA specifications. Claim data is completely undocumented.
- **Field descriptions**: 7 out of 7 for the CSV format (100%); 0 for everything else.
- **Types**: Described only for CSV columns (implicitly — all appear to be text/string).
- **Relationships/foreign keys**: PID is identified as a linking field across file types. No other relationships documented.
- **Value sets**: Only "Patient Notes Category" is noted as coming from a "pick list" — no actual values provided.
- **Sample data**: None provided.
- **Machine-readable schemas**: None (no XSD, JSON Schema, or any formal schema).
- **Developer usability**: A developer could process the C-CDA files (since C-CDA is a well-known standard) and the patient notes CSV (since fields are described). However, claim data files would be completely uninterpretable without additional information from the vendor. The documentation assumes the reader has "a technical understanding [of] HL7 specifications such as C-CDA standards and formatting around CSV type files" (p.4).

A developer could not build a complete import from this documentation alone. The C-CDA component is processable because C-CDA is a standard, not because the documentation is good. The claim data component is not processable at all.

## 7. Overall Assessment

### Classification

**Standard-based projection**: The export is primarily C-CDA R2.1 (a clinical document standard), supplemented with CSV for ad-hoc notes and CDA for scanned records. It is not a native database export — it projects the product's data into C-CDA, which inherently limits the export to what C-CDA sections can represent. The mention of "Claim Data" files suggests some native data is also exported, but this is completely undocumented.

### Key Findings

1. **The export is fundamentally a C-CDA repackaging with thin supplements.** The core clinical/demographic data is exported as C-CDA R2.1, which is a clinical summary standard — not a comprehensive data export format. C-CDA was designed for transitions of care, not for full EHI export. This approach inherently limits what can be exported to what C-CDA sections support. (Source: `EHI Export.pdf`, p.5)

2. **Claim data is exported but completely undocumented.** The file naming convention on p.5 explicitly lists "Claim Data" as a TYPE value, confirming billing data is part of the export. Yet the documentation provides zero information about the format, fields, or structure of these files. A recipient would have no way to interpret them. (Source: `EHI Export.pdf`, p.5 naming convention vs. pp.5-6 format descriptions)

3. **Only 7 fields are documented across the entire export.** The patient notes CSV is the only component with field-level documentation. Everything else either defers to external specifications (C-CDA, CDA) or is undocumented (claim data). For a product that includes EHR, Practice Management, Patient Portal, and Health Information Exchange, 7 documented fields is strikingly thin. (Source: `EHI Export.pdf`, p.6)

4. **The product's own executive summary reveals coverage gaps.** The PDF states the product portfolio includes Practice Management, Patient Portal, and Health Information Exchange (p.4). The export documentation addresses none of these beyond the oblique "Claim Data" TYPE mention. Patient portal data, insurance/coverage information, and HIE content are absent from the export.

5. **No sample data or schemas provided.** There are no sample export files, no machine-readable schemas, and no worked examples. A developer receiving this documentation would rely entirely on their pre-existing knowledge of C-CDA and would have to reverse-engineer claim data files. (Source: all artifacts in `downloads/`)

### Summary Stats

```
Classification:  Standard-based projection
Export format:   Mixed: C-CDA R2.1 XML + CSV + CDA XML (Base64)
Model type:      Standard projection (C-CDA), not native database
Entities:        4 file categories (demographics/clinical, notes, scanned records, claims)
Fields:          7 (only patient notes CSV documented)
Descriptions:    100% of documented fields (7/7), but only 7 fields total
Sample data:     No
Bulk export:     Yes (single patient or full collection)
Domains covered: 0 of 15 confirmed; 11 presumed via C-CDA; 4 not covered
```

### Bottom Line

This is a minimal compliance effort. The export wraps clinical data in C-CDA (a standard designed for care summaries, not comprehensive export), adds a 7-field CSV for ad-hoc notes, and mentions claim data files without documenting them at all. A patient or provider would get C-CDA clinical summaries and some supplementary files, but the lack of documentation for claim data — combined with the absence of practice management, patient portal, and pediatric-specific data — means this falls well short of a complete EHI export for a product that advertises EHR, Practice Management, and Revenue Cycle Management capabilities.
