# EHI Export Analysis: Net Health

**Product**: Net Health® WoundExpert (also sold as WoundDocs by RestorixHealth)
**Analysis date**: 2026-02-16
**CHPL IDs**: 9836 (WoundExpert v7.0, certified 2018-12-31), 10234 (WoundDocs v7.0, certified 2019-12-24)

## 1. Product Context

Net Health® WoundExpert is a **specialty wound care EHR** designed for hospital outpatient wound care centers, wound care management companies, and post-acute care settings. It is not a general-purpose EHR — it supplements a facility's primary hospital EHR (Epic, Cerner, etc.) with deep wound care functionality. Net Health claims WoundExpert is the dominant wound care EHR in the US, serving ~23,000 organizations with approximately 90% market penetration in wound care.

Based on product documentation, vendor materials, and certified criteria, WoundExpert stores data across these domains relevant to EHI completeness:

- **Wound-specific clinical data**: Wound assessments (size, depth, tissue type, location, etiology, healing stage), wound photographs with automated measurement (via Tissue Analytics), treatment plans, wound dressings, progress tracking over time
- **General clinical data**: Demographics, problem lists, medication lists, allergy lists, family health history, implantable device lists, lab/imaging orders and results, progress notes with customizable templates
- **Medications**: CPOE, drug interaction checking, e-prescribing (including controlled substances via DrFirst)
- **Billing/financial**: Invoice generation, payment processing, insurance claims management, revenue/expense tracking, ICD-10-CM coding, E&M level documentation
- **Transitions of care**: C-CDA documents (send/receive), clinical information reconciliation
- **Patient engagement**: Patient portal (patientportal.nethealth.com), FHIR R4 API (via Darena Health)
- **Specialty data**: Hyperbaric oxygen therapy records (via RestorixHealth/CutisCare)

The breadth of certified criteria (37 criteria across (a), (b), (c), (d), (e), (g), (h) groups) and the presence of 8 interface types (ADT, Billing, C-CDA, Clinical Documentation, Ordered Results, Scheduling, Transcription, Unsolicited Results) indicate a system that stores significantly more data than a clinical summary would capture.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/certification-page.html` (399 KB) | Full HTML of the ONC certification page containing the EHI export description | **Primary source** — only public EHI documentation |
| `downloads/certification-page-text.txt` (6 KB) | Clean text extraction of the certification page via WordPress REST API | Useful for verifying content |
| `downloads/certification-page-full.png` (874 KB) | Full-page screenshot of the certification page | Visual confirmation of page layout |
| Live fetch of certification page (2026-02-16) | Verified page content is unchanged from downloaded version | Confirmed current accuracy |
| Live fetch of linked pages: regulatory compliance, FHIR API, real-world testing, data/AI governance | None contain EHI export details | Confirmed no additional EHI docs |
| Real-World Testing Results 2025 PDF (from live URL) | RWT results; Data Export metric (#8) ceased collection after Q2 2025 per Executive Order 14192 | Minor context |
| Real-World Testing Results 2022 PDF (from live URL) | Earlier RWT results; Data Export section references (b)(6), not (b)(10), describing CDA file exports | Reveals older export mechanism |

**Key finding**: Only 3 files were collected in `downloads/`. The certification page is the sole source of EHI export information. No data dictionaries, schemas, sample exports, user guides, or other documentation artifacts exist publicly.

## 3. Export Mechanics

- **Format**: ZIP file containing one folder per patient, with CSV data files, image files, custom scans, an XLSX data dictionary, and a text summary
- **Mechanism**: Not documented publicly. The certification page does not describe how to initiate the export (no UI screenshots, no API endpoint, no instructions). The 2022 RWT results reference a "data export tool" accessible to users with a "Facility Administrator" user role, suggesting a UI-based mechanism
- **Single-patient vs bulk**: Explicitly supports both — "single patient and patient population electronic health information can be exported"
- **Access constraints**: Not documented. No mention of fees for EHI export. The RWT results indicate exports are generated within the production SaaS environment
- **Variability note**: The vendor states "the content and format of the data contained within the export zip file depending on number of patients selected and software functionality in use," suggesting the CSV contents may vary by which modules a facility has licensed

## 4. Export Content: What's In It

### What's publicly documented

The public documentation describes only the **container structure** of the export:

1. **CSV files of EHI data** — no CSV file names, column names, data types, or relationship documentation are provided publicly
2. **All image files from the patient record** — presumably wound photographs and associated imaging
3. **All custom scans on file** — presumably scanned paper documents
4. **EHIDataExtract_DataDictionary.xlsx** — an Excel data dictionary bundled in each export (not publicly downloadable)
5. **ExportSummary.txt** — a text summary of the export

### What's NOT publicly documented

- **Zero** CSV file/table names
- **Zero** field/column names
- **Zero** data types
- **Zero** value sets or coded value definitions
- **Zero** relationship/foreign key documentation
- **Zero** sample data records
- **No** machine-readable schema (the XLSX dictionary exists but is locked inside the export)

### Vendor's own content organization

The vendor provides no content organization. There are no categories, no table listings, no domain groupings — the entire EHI documentation is 87 words describing the container format. The only named files are `EHIDataExtract_DataDictionary.xlsx` and `ExportSummary.txt`.

**No entity/field table can be generated** because no entity or field information is publicly available. The `analysis/full-entity-inventory.json` file documents this absence with 0 entities and 0 fields.

### Positive architectural signals

Despite the documentation gap, there are structural indicators that the underlying export may be reasonable:

1. **CSV-based native export** (not C-CDA/FHIR repackaging) — suggests export of internal data model
2. **Includes images and custom scans** — awareness of unstructured data in the patient record
3. **Bundled XLSX data dictionary** — each export is self-documenting (for the recipient)
4. **Single-patient AND population export** — both modes required by (b)(10)
5. **Separate from FHIR API** — vendor correctly distinguishes (b)(10) from (g)(10), not conflating them

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor provides **no information** about which data domains are in the export. The description "csv files of EHI data" is completely opaque. The variability caveat ("depending on ... software functionality in use") further complicates assessment — it implies coverage may differ per facility based on licensed modules.

The only concrete content commitments are:
- Image files from the patient record (likely wound photos)
- Custom scans on file (likely scanned documents)

Everything else — whether demographics, wound assessments, medications, billing, or any other domain is exported — is unknown from the public documentation.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ❓ Unknown | No CSV names documented | Product stores demographics (certified (a)(5)); cannot assess |
| Encounters / visits | ❓ Unknown | No CSV names documented | Product stores encounter data; cannot assess |
| Problems / conditions / diagnoses | ❓ Unknown | No CSV names documented | Product stores problem lists (certified (a)(5)); cannot assess |
| Medications / prescriptions | ❓ Unknown | No CSV names documented | Product has CPOE and e-prescribing; cannot assess |
| Allergies | ❓ Unknown | No CSV names documented | Product stores allergies (certified (a)(5)); cannot assess |
| Immunizations | N/A | — | Wound care EHR; immunizations unlikely to be a primary data store |
| Vitals | ❓ Unknown | No CSV names documented | Cannot assess |
| Lab results | ❓ Unknown | No CSV names documented | Product has CPOE for lab (certified (a)(2)); cannot assess |
| Imaging / diagnostic reports | ⚠️ Partial | "all image files from the patient record" confirmed; wound photos via Tissue Analytics | Images confirmed; structured imaging reports unknown |
| Procedures | ❓ Unknown | No CSV names documented | Wound care procedures likely stored; cannot assess |
| Clinical notes / documents | ❓ Unknown | No CSV names documented | Product has progress notes with customizable templates; cannot assess |
| Care plans / goals | ❓ Unknown | No CSV names documented | Treatment plans are core wound care data; cannot assess |
| Orders / referrals | ❓ Unknown | No CSV names documented | Product has CPOE; cannot assess |
| Insurance / coverage | ❓ Unknown | No CSV names documented | Product has billing interfaces; cannot assess |
| Claims / billing | ❓ Unknown | No CSV names documented | Product has invoice, claims, payment features; cannot assess |
| Payments | ❓ Unknown | No CSV names documented | Product tracks revenue/expenses; cannot assess |
| Consents / directives | ❓ Unknown | No CSV names documented | Cannot assess |
| Patient communications / portal messages | ❓ Unknown | No CSV names documented | Product has patient portal; cannot assess |
| Specialty – Wound care assessments | ❓ Unknown | No CSV names documented | **Core product data** (wound size, depth, tissue type, location, etiology, healing stage); cannot assess |
| Specialty – Hyperbaric oxygen therapy | ❓ Unknown | No CSV names documented | RestorixHealth/CutisCare integration; cannot assess |

**Summary**: Of 20 applicable domains, **0** can be confirmed as covered, **1** is partially confirmed (images), and **19** are completely unknown. This is not because the export necessarily lacks coverage — it's because the public documentation is too thin to make any determination.

## 6. Documentation Quality

**Rating: Very poor / effectively absent**

The public EHI export documentation consists of **87 words** — two short paragraphs plus a 5-item bulleted list on the certification page. This is among the most minimal (b)(10) documentation encountered.

**What exists**:
- Container format description (ZIP with folders per patient)
- List of file types in the export (CSVs, images, scans, XLSX dictionary, TXT summary)
- Statement of support for single-patient and population export
- Explicit reference to §170.315(b)(10)

**What's missing**:
- Any data dictionary or schema (the XLSX dictionary exists but is not publicly accessible)
- Any field names, data types, or descriptions
- Any value sets or coded value documentation
- Any relationship/foreign key documentation
- Any export instructions, screenshots, or user guide
- Any sample data
- Any statement about which data domains are covered
- Any API specification

**Could a developer build an import from this documentation?** No. A developer would know only that they'll receive a ZIP with CSVs, images, and an XLSX dictionary. They would need to obtain an actual export and reverse-engineer the structure from the bundled dictionary. The XLSX data dictionary may be thorough — but since it's locked inside the export, it cannot be evaluated.

## 7. Overall Assessment

### Classification

**Minimal/stub**

The public-facing documentation is too thin to assess what the export actually covers. While the architectural approach (CSV-based native export with bundled data dictionary, images, and scans) is sound, the 87-word public description provides no visibility into content, coverage, or structure. The export *may* be comprehensive for those who have access to it, but the public documentation functions as a stub — it confirms the capability exists without documenting what it does.

### Key Findings

1. **No public data dictionary**: The data dictionary (`EHIDataExtract_DataDictionary.xlsx`) exists only inside export ZIPs. Zero entities, zero fields, zero data types, and zero value sets are documented publicly. This makes independent assessment of export completeness impossible.

2. **Sound architectural approach**: The export uses CSV files (native data model), includes images and custom scans, bundles a per-export data dictionary, supports both single-patient and population export, and is correctly distinguished from the FHIR API. These are positive signals about the underlying implementation.

3. **87 words of public documentation**: The entire EHI export documentation is two paragraphs on the certification page — no downloadable artifacts, no linked pages, no user guides, no sample data. No additional EHI content was found on linked pages (regulatory compliance, FHIR API, real-world testing, data/AI governance) or via WordPress REST API search.

4. **Coverage is entirely opaque**: The vendor states "csv files of EHI data" without any specificity. The caveat that content "depend[s] on ... software functionality in use" suggests variable coverage by facility. For a wound care EHR with deep specialty data (wound measurements, tissue types, healing trajectories), this opacity is a significant problem.

5. **2022 RWT reveals older export mechanism**: The 2022 Real-World Testing results describe the Data Export metric using CDA files under §170.315(b)(6), not the CSV-based (b)(10) mechanism described on the certification page. This suggests the CSV/ZIP approach may have been implemented later, during the Cures Update.

### Summary Stats

```
Classification:  Minimal/stub
Export format:   CSV (within ZIP), plus images and scans
Model type:      Appears to be native database (CSV), but unverifiable
Entities:        N/A (no public data dictionary)
Fields:          N/A (no public data dictionary)
Descriptions:    N/A
Sample data:     No
Bulk export:     Yes (single-patient and population)
Domains covered: 0 confirmed of ~20 applicable (1 partial: images)
```

### Bottom Line

Net Health has built a structurally reasonable (b)(10) export — CSV-based, with images, scans, and a bundled data dictionary — but has published effectively zero public documentation about its content. A patient or provider requesting an export would receive a self-documenting ZIP, but no one outside the system can evaluate what data it contains, whether it covers wound-specific clinical data, billing, or any other domain. The single biggest gap is the absence of a publicly accessible data dictionary: publishing the already-existing `EHIDataExtract_DataDictionary.xlsx` would instantly transform this from a stub into a potentially assessable export.
