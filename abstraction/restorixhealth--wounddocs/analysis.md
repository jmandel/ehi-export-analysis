# EHI Export Analysis: Net Health (RestorixHealth)

**Product**: WoundDocs (WoundExpert v7.0)
**Analysis date**: 2026-02-16
**CHPL ID**: 15.04.04.2272.Woun.07.01.1.191224 (CHPL #10234)

## 1. Product Context

WoundDocs is the RestorixHealth-branded deployment of Net Health's **WoundExpert**, a specialty cloud-based EHR designed exclusively for wound care management. It is not a general-purpose EHR — it operates as a specialty overlay alongside hospital-wide EHR systems (Epic, Cerner, MEDITECH, etc.) via bidirectional HL7 interfaces.

**Core data domains the product stores:**
- **Wound assessment data** (the product's primary purpose): wound measurements (L/W/D/area/volume), tissue type percentages, exudate characteristics, wound edges, periwound skin condition, wound bed descriptions, pain assessments, healing trajectories
- **Wound images**: clinical photographs with AI-based automated measurements (via Tissue Analytics acquisition), 3D imaging
- **Patient demographics**: name, DOB, address, insurance, contacts (received via ADT interfaces and patient registration)
- **Treatment plans**: dressing selections, debridement methods, wound care interventions
- **Progress notes/clinical documentation**: visit documentation, clinical impressions
- **Medications**: wound care-related medications; certified for CPOE and e-prescribing (via Surescripts/First Databank)
- **Diagnoses**: wound-related ICD-10 codes, comorbidities
- **Procedures**: debridement, skin grafts, NPWT, HBOT sessions
- **Lab/diagnostic results**: wound cultures, healing-related bloodwork (via ordered/unsolicited results interfaces)
- **Allergies**: medication allergies (certified for drug-allergy checking)
- **Coding and billing**: automatic ICD-10/CPT coding, claims management, billing/invoicing, payment tracking, revenue reporting, MIPS reporting
- **Referrals**: referral management (certified for transitions of care b(1)–b(3))
- **Scheduling**: clinical scheduling and appointment management

The product serves outpatient wound care centers and independent wound care providers across 260+ hospital wound centers (RestorixHealth alone).

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `drummond-certified-woundexpert.html` (399 KB) | ONC certification page with EHI Export section — primary source for b(10) export description. Contains the only public description of the export ZIP format, contents, and data dictionary. | **Most informative** for export format/structure |
| `Real-World-Testing-Plan-2026.pdf` (18 pages, 750 KB) | 2026 RWT Plan; Measure 8 describes b(10) export in most detail found anywhere. Reveals two export modes (Facility Admin CDA vs Net Health Admin full EHI). | **Most informative** for export mechanics/modes |
| `Real-World-Testing-Results-2025.pdf` (11 pages, 187 KB) | 2025 RWT Results; b(10) Measure 8 dropped after Q2 2025 per Executive Order 14192. Shows zero real production customer FHIR API usage; documents Darena Health migration. | Contextual — confirms low adoption |
| `registered-url-fullpage.png` (877 KB) | Full-page screenshot of registered URL | Corroborative only |
| `fhir-api-page.png` (349 KB) | Screenshot of FHIR API specs page (g(10), not b(10)) | Confirms separation of b(10)/g(10) |

**No data dictionary, sample data, schema, or field-level documentation is publicly available.** The `EHIDataExtract_DataDictionary.xlsx` file referenced in the export documentation exists only inside actual export ZIP files and is not downloadable from the website.

## 3. Export Mechanics

**Format**: ZIP archive containing per-patient folders with:
- CSV files of EHI data (machine-readable)
- All image files from the patient record (wound photos)
- All custom scans on file (scanned documents)
- `EHIDataExtract_DataDictionary.xlsx` (Excel data dictionary)
- `ExportSummary.txt` (plain text summary)

**Two export modes exist:**

1. **Facility Administrator** role: Can generate and download a **CDA file** containing relevant treatment information for one or more patients in a specific date and time range. This appears to be a clinical summary export (C-CDA), not the full EHI export.

2. **Net Health Administrator** role: Can execute **full facility EHI exports** that include patient medical records in PDF format and all EHI in CSV files. This is described as the comprehensive b(10) export.

**Mechanism**: Built-in export tool within the WoundExpert application (not API-based). The export is explicitly separate from the FHIR API (g(10)) operated through Darena Health.

**Single-patient**: Yes (stated on registered URL: "Single patient and patient population electronic health information can be exported")

**Bulk/population**: Yes (same statement; Net Health Administrator mode supports "full facility EHI exports")

**Access constraints**: The full EHI export (CSV + PDF + images) requires the "Net Health Administrator" role — a vendor-level role, not a customer-level role. The facility-level export (CDA) is available to Facility Administrators. This means the comprehensive export may require vendor involvement.

**Fees**: No explicit fees documented for the b(10) export itself. The registered URL documents fees for other services (e-prescribing, Direct messaging, FHIR API) but not for the EHI export.

## 4. Export Content: What's In It

### What can be determined

The registered URL states the export contains "csv files of EHI data" and the 2026 RWT plan states it includes "all EHI in CSV files." However, **no field-level documentation is publicly available**:

- **No public data dictionary**: `EHIDataExtract_DataDictionary.xlsx` exists only inside export ZIPs
- **No list of CSV file names or entity types** is published
- **No field names, types, or descriptions** are documented anywhere publicly
- **No sample data** is provided
- **No schema files** (JSON Schema, XSD, etc.) exist
- **No documentation of relationships** between CSV files

### What the documentation claims

The export is described as containing "all EHI" in CSV format, plus:
- All patient images (critical for wound care — clinical photographs are core data)
- All custom scans (scanned documents)
- A self-contained data dictionary (XLSX format, bundled with export)
- An export summary (TXT)

The vendor explicitly claims this is a comprehensive export ("all EHI in CSV files"), not just a clinical summary. The inclusion of images and scans alongside structured CSV data supports this claim, as does the separation from the FHIR/C-CDA based g(10) API.

### Vendor's own content organization

**Cannot be assessed.** Without access to the data dictionary or a sample export, the vendor's internal organization of entities, tables, and fields is unknown. The only public information is that the export contains "CSV files" — the specific CSV file names, the number of files, and their contents are undocumented publicly.

| Entity/Table | Fields | Described | Types | Category |
|---|---|---|---|---|
| *Unknown* | *Unknown* | *Unknown* | *Unknown* | *Unknown* |

**No entity inventory can be produced** because no data dictionary, schema, or sample data is publicly available. The `entity-inventory-full.json` in `analysis/` documents this absence.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

**Cannot be assessed from public documentation.** The vendor claims "all EHI in CSV files" but provides no public evidence of what data domains, entities, or fields the export actually contains. There is no data dictionary, no sample export, no field list, and no entity enumeration available for public review.

The only concrete content claims are:
1. CSV files of EHI data (unspecified scope)
2. All image files from the patient record
3. All custom scans on file

The inclusion of images and scans is a positive signal for a wound care system where clinical photographs are core data. But beyond "CSV files of EHI data," the actual data domains covered are opaque.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Likely but unverified | Vendor claims "all EHI"; product stores demographics via ADT | Product stores this; cannot confirm export includes it |
| Encounters / visits | ⚠️ Likely but unverified | Core wound care visit documentation is central to the product | Product stores this; cannot confirm export includes it |
| Problems / conditions / diagnoses | ⚠️ Likely but unverified | Product stores wound-related ICD-10 codes and comorbidities | Product stores this; cannot confirm export includes it |
| Medications / prescriptions | ⚠️ Likely but unverified | Certified for CPOE and e-prescribing | Product stores this; cannot confirm export includes it |
| Allergies | ⚠️ Likely but unverified | Certified for drug-allergy checking | Product stores this; cannot confirm export includes it |
| Immunizations | N/A | Not a primary function of a wound care specialty EHR | Not expected for this product |
| Vitals | ⚠️ Likely but unverified | Wound care visits likely capture basic vitals | May be stored; cannot confirm |
| Lab results | ⚠️ Likely but unverified | Product receives lab results via interfaces (wound cultures, etc.) | Product stores this; cannot confirm export includes it |
| Imaging / diagnostic reports | ✅ Likely covered | Export explicitly includes "all image files" and "custom scans" | Wound images are explicitly included; this is strong |
| Procedures | ⚠️ Likely but unverified | Product tracks debridement, NPWT, HBOT, skin grafts | Product stores this; cannot confirm export includes it |
| Clinical notes / documents | ⚠️ Likely but unverified | Progress notes, clinical impressions are core functionality | Product stores this; cannot confirm export includes it |
| Care plans / goals | ⚠️ Likely but unverified | Treatment plans are a core feature | Product stores this; cannot confirm export includes it |
| Orders / referrals | ⚠️ Likely but unverified | Certified for transitions of care; referral management | Product stores this; cannot confirm export includes it |
| Insurance / coverage | ⚠️ Likely but unverified | Product stores insurance data from ADT feeds and billing | Product stores this; cannot confirm export includes it |
| Claims / billing | ⚠️ Unknown | Product has billing/claims capability (ICD-10/CPT coding, claims management) | **Potential significant gap** — billing is a known product feature but no evidence it's in the export |
| Payments | ⚠️ Unknown | Product tracks payments and revenue | Same concern as billing |
| Consents / directives | ⚠️ Unknown | Unclear if product stores these independently | Cannot assess |
| Patient communications / portal messages | ⚠️ Unknown | Patient portal exists; Direct messaging certified | Cannot assess |
| Specialty-specific: Wound care assessments | ⚠️ Likely but unverified | This is the product's core data — wound measurements, tissue types, healing trajectories | Product's most critical data; cannot confirm granularity of export |
| Specialty-specific: Hyperbaric oxygen therapy | ⚠️ Likely but unverified | HBOT sessions are tracked in the product | Cannot confirm |

**Key observation**: Every domain except wound images/scans gets a "⚠️ Likely but unverified" rating because the export documentation provides no specifics about what CSV files contain. The vendor's claim of "all EHI" is plausible but unverifiable from public documentation.

## 6. Documentation Quality

**Poor.** The public documentation is insufficient for a developer to understand or use the export:

- **No field-level documentation**: Zero publicly available information about CSV column names, data types, value sets, or coded fields
- **No entity/table enumeration**: Not even a list of CSV file names is published
- **No sample data**: No example exports are available
- **No schema**: No machine-readable format specification
- **No relationship documentation**: No information about how CSV files relate to each other (foreign keys, patient identifiers)
- **No format specification**: No documentation of encoding, delimiters, date formats, null handling, quoting

**What IS documented** (minimally):
- The export exists and is a ZIP containing CSV files, images, and scans
- A data dictionary (XLSX) is included inside each export
- Two export modes exist with different roles and capabilities
- Both single-patient and population exports are supported

**Self-documenting claim**: The vendor states that `EHIDataExtract_DataDictionary.xlsx` is included in every export, making the export "self-describing." This is a reasonable approach if the data dictionary is thorough, but it means the documentation quality cannot be assessed without obtaining an actual export. A developer would need to request an export before they could even begin planning an import.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Minimal/stub/unclear**

The public documentation is too thin to assess the actual breadth of the export. The vendor *claims* "all EHI in CSV files," which if true would make this comprehensive, but there is zero public evidence to verify this claim. No data dictionary, no entity list, no field list, no sample data. The only concrete evidence is that wound images and scans are included. The distinction between "Facility Administrator" (CDA-only) and "Net Health Administrator" (full EHI) modes raises a question about whether typical users even have access to the comprehensive export, or whether it requires vendor involvement.

**Axis 2 — Export approach: Purpose-built EHI export**

Despite the documentation gaps, the export is clearly purpose-built for b(10). The evidence:
1. **Distinct from FHIR API**: The b(10) export (CSV/ZIP) is explicitly and correctly separated from the g(10) FHIR API (via Darena Health). The vendor does not repackage the FHIR API as their b(10) export.
2. **Native format**: The export uses CSV files from the product's own data model, not C-CDA or FHIR resources.
3. **Includes images and scans**: The export goes beyond structured clinical data to include all patient images and scanned documents — something a repackaged C-CDA or FHIR export would not do.
4. **Bundled data dictionary**: Including `EHIDataExtract_DataDictionary.xlsx` in every export indicates the vendor built a self-documenting export mechanism specific to this purpose.
5. **Two-tier export system**: The existence of both a CDA export (for facility admins) and a full CSV export (for Net Health admins) suggests the vendor built a comprehensive export beyond their existing clinical exchange capabilities.

The concern is that the full EHI export requires a "Net Health Administrator" role — meaning the vendor may need to be involved, rather than the facility being able to self-serve.

### Key Findings

1. **No public data dictionary or field-level documentation.** The `EHIDataExtract_DataDictionary.xlsx` is only available inside actual export ZIP files. This is the most significant gap — the export may be comprehensive, but it's impossible to verify from public documentation alone.

2. **Export is purpose-built and correctly separated from FHIR API.** The vendor built a dedicated CSV/ZIP export tool for b(10), distinct from their g(10) FHIR API (via Darena Health). This is the right architecture.

3. **Wound images explicitly included.** For a wound care EHR, clinical photographs are among the most critical data. The explicit inclusion of "all image files from the patient record" and "all custom scans" is a meaningful positive signal.

4. **Full EHI export requires vendor-level role.** The comprehensive CSV export is available only to "Net Health Administrator" — not to facility-level administrators, who can only generate CDA files. This may create a practical barrier to patient/provider access to the full export.

5. **Zero real-world testing results for b(10).** The 2025 RWT results dropped the data export metric (Measure 8) after Q2 2025 per Executive Order 14192, and the FHIR API had zero production customer usage in 2025 (only test data during the Darena Health migration). There is no evidence of the b(10) export being used in production.

### Summary Stats

    Coverage:        Minimal/stub/unclear
    Approach:        Purpose-built EHI export
    Export format:   CSV files + images + scans in ZIP archive
    Entities:        N/A (no public data dictionary)
    Fields:          N/A (no public data dictionary)
    Descriptions:    N/A
    Sample data:     No
    Bulk export:     Yes (Net Health Administrator role)
    Domains covered: Cannot be verified (vendor claims "all EHI")

### Bottom Line

Net Health built a dedicated b(10) export tool for WoundDocs/WoundExpert that is architecturally sound — CSV files with images and a bundled data dictionary, clearly separated from their FHIR API. However, the public documentation is so thin that the export's actual content scope is completely opaque: no data dictionary, no entity list, no field list, no sample data. A patient or provider cannot determine what data they would receive without first obtaining an export. The single biggest gap is the absence of any public documentation of what the CSV files actually contain.
