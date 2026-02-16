# EHI Export Analysis: Lunar Systems, Inc.

**Product**: Lunar Cloud Platform 2.6
**Analysis date**: 2026-02-16
**CHPL ID**: 15.04.04.3241.Luna.02.00.1.250917

## 1. Product Context

Lunar Systems, Inc. is a venture-backed startup building an "AI-native hospital information system" targeting smaller hospitals. The Lunar Cloud Platform is a cloud-hosted, comprehensive HIS covering inpatient, ED, and ambulatory settings. It was certified September 2025 with 37 ONC criteria — a broad certification profile consistent with a full-featured EHR.

**Key capabilities relevant to EHI scope:**
- **Clinical**: CPOE for medications, labs, and imaging; drug interaction checks; demographics; problem lists; allergy lists; vital signs; immunizations; family health history; implantable device list; clinical notes and documentation
- **Revenue cycle / billing**: Revenue cycle specialist role listed; "coders" and "billers" explicitly listed as platform users; the product overview page references "Lunar Revenue Suite"
- **Pharmacy**: Pharmacists listed as users; medication management
- **Laboratory**: Lab technicians listed as users; lab ordering and results
- **Supply chain**: Supply chain staff listed as users (unusual for an EHR — more typical of a full HIS)
- **Patient access**: Patient portal (e)(1) certified
- **Interoperability**: FHIR R4 API via EMR Direct HealthToGo; Direct messaging; C-CDA transitions of care
- **Named suites** (from the EHI Export PDF overview, p.2): Lunar Clinical Suite, Lunar Revenue Suite, Lunar Lab Suite, Lunar IT Suite, Lunar Operations Suite, Lunar Analytics Suite, Lunar Patient Suite

The product is early-stage with no public customer deployments, no third-party reviews, and limited feature documentation. However, the named suites and certification breadth indicate it stores clinical, billing/revenue, lab, operational, and patient-facing data.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/EHI_Export_Jan_2026.pdf` (1.1 MB, 54 pages) | Primary documentation. Contains C-CDA format guide, 18 C-CDA section specifications with XML examples and key element tables, plus supplemental CSV data dictionary for 3 categories (Documents, Orders, Charges). | **Most informative** — sole substantive artifact |
| `downloads/ehi-export-page.html` (6.7 KB) | Raw HTML of golunar.com/ehi-export. Webflow page containing a single iframe embedding the PDF. No additional content or links. | Low — just a PDF wrapper |
| `downloads/ehi-export-page-screenshot.png` (1.4 MB) | Screenshot of the web page showing the embedded PDF viewer. | Low — confirms page structure only |
| `downloads/enrichment/ehi-export-sections.json` (29.6 KB) | Machine-parsed extraction of all 18 C-CDA sections with 146 key elements. | Useful for verification |
| `downloads/enrichment/ehi-export-supplemental.json` (6.5 KB) | Parsed extraction of 3 supplemental CSV categories with 42 fields. | Useful for verification |
| `downloads/enrichment/extraction-stats.json` (185 B) | Parse accounting: 54 pages, 18/18 sections, 3 supplemental categories, 42 supplemental fields, 146 key elements, 0 parse failures. | Confirms completeness |

**No sample data files, no machine-readable schemas (JSON Schema, XSD), no FHIR resources, and no additional documentation beyond the single PDF.**

## 3. Export Mechanics

- **Format**: C-CDA XML for clinical data + supplemental CSV files for documents, orders, and charges. All packaged as a ZIP file.
- **Mechanism**: The PDF states "The platform supports single-patient and bulk-patient data extraction in the form of an 'export zip' file containing machine-readable files, enabling authorized users to access and manage the designated record set." No specific UI screenshots or API details are provided.
- **Single-patient vs bulk**: Both supported per the documentation.
- **Access constraints**: No fees or special access constraints mentioned. The documentation states "authorized users" can perform exports.
- **C-CDA version**: CDA Release 4.1

## 4. Export Content: What's In It

The export consists of two components:
1. **C-CDA XML document** containing 18 sections of clinical data
2. **Supplemental CSV files** containing 3 categories of non-C-CDA data (Documents, Orders, Charges)

### Data dictionary scope

- **Total entities**: 21 (18 C-CDA sections + 3 supplemental CSV categories)
- **Total fields**: 188 (146 C-CDA key elements + 42 supplemental CSV fields)
- **Fields with descriptions**: 188 (100%)
- **Fields with data types**: 42 of 42 supplemental CSV fields have explicit types; C-CDA elements are typed implicitly as XML elements
- **Relationships/foreign keys**: Not explicitly documented; some CSV fields reference visits by UUID
- **Value sets/code systems**: Referenced in XML examples (SNOMED CT, RxNorm, LOINC, CDC Race/Ethnicity, HL7 Administrative Gender, NUCC taxonomy) but not enumerated in the data dictionary
- **Sample data**: XML examples are provided inline for each C-CDA section (synthetic data); no standalone sample export files

### Vendor's own content organization

#### C-CDA Sections (18 sections, 146 elements)

| Entity | Fields | Described | Types | Category |
|---|---|---|---|---|
| Patient Summary | 15 | 15 | XML | C-CDA Section |
| Allergies and Intolerances | 7 | 7 | XML | C-CDA Section |
| Problem List | 9 | 9 | XML | C-CDA Section |
| History of Medication Use | 10 | 10 | XML | C-CDA Section |
| Laboratory/Diagnostic Results | 7 | 7 | XML | C-CDA Section |
| Procedures | 6 | 6 | XML | C-CDA Section |
| Social History | 5 | 5 | XML | C-CDA Section |
| Functional Status | 6 | 6 | XML | C-CDA Section |
| Mental/Cognitive Status | 6 | 6 | XML | C-CDA Section |
| Vital Signs | 8 | 8 | XML | C-CDA Section |
| History of Encounters | 10 | 10 | XML | C-CDA Section |
| History of Immunizations | 7 | 7 | XML | C-CDA Section |
| Care Team | 10 | 10 | XML | C-CDA Section |
| Assessments | 7 | 7 | XML | C-CDA Section |
| Treatment Plan | 9 | 9 | XML | C-CDA Section |
| Clinical Notes | 9 | 9 | XML | C-CDA Section |
| Payers | 10 | 10 | XML | C-CDA Section |
| Participant | 5 | 5 | XML | C-CDA Section |

#### Supplemental CSV Categories (3 categories, 42 fields)

| Entity | Fields | Described | Types | Category |
|---|---|---|---|---|
| Supplemental: Documents | 12 | 12 | Explicit (string, boolean, datetime, dict, uuid) | Supplemental CSV |
| Supplemental: Orders | 14 | 14 | Explicit (string, int, dict, datetime, uuid) | Supplemental CSV |
| Supplemental: Charges | 16 | 16 | Explicit (float, string, boolean, datetime, date, array) | Supplemental CSV |

The full entity inventory with all 188 fields is available in `analysis/entity-inventory-full.json`.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The export has two layers:

**C-CDA layer (16 clinical sections + 2 administrative sections):** This is a standard C-CDA document covering the USCDI-scope clinical domains. The 16 clinical sections (Patient Summary through Clinical Notes) map directly to standard C-CDA templates and cover the expected USCDI data classes. The two additional sections — Payers (insurance/coverage) and Participant (related persons) — are also standard C-CDA sections. Each section is documented with template IDs, LOINC codes, example XML, and key element tables. The depth within each section is moderate: the "key elements" tables list the primary XML elements but do not enumerate every possible sub-element or attribute — for example, the Encounters section lists 10 key elements but a real encounter record in C-CDA can have dozens of nested elements for diagnoses, providers, facilities, etc.

**Supplemental CSV layer (3 categories, 42 fields):** This is the vendor's attempt to go beyond C-CDA. The three categories are:
- **Documents** (12 fields): Captures document metadata (class, type, source, LOINC code) plus the actual content as text_data, json_data, and application_data fields. This could potentially be rich if the dict/JSON fields contain substantial structured data.
- **Orders** (14 fields): Captures order metadata (name, status, urgency, reason, times) plus a generic "data" dict field. Links to visits by UUID.
- **Charges** (16 fields): This is the most notable supplemental category — it includes rate, revenue_code, procedure_code, modifier, pos_code, dept, quantity, total, NDC, service dates, and diagnosis_ids. This represents genuine billing/charge data beyond what C-CDA covers.

The Charges CSV is the strongest signal that this is not purely a repackaged C-CDA export. It includes billing-specific fields (revenue_code, procedure_code, modifier, pos_code, NDC) that are not part of standard C-CDA or USCDI.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | Patient Summary (15 elements): name, DOB, gender, race, ethnicity, language, address, telecom, MRN, SSN, marital status, deceased status | Adequate for standard demographics |
| Encounters / visits | ✅ Covered | History of Encounters (10 elements): encounter type, performer, facility, discharge disposition, diagnosis | Standard C-CDA depth |
| Problems / conditions | ✅ Covered | Problem List (9 elements): diagnosis codes, status, dates | Standard C-CDA depth |
| Medications / prescriptions | ✅ Covered | History of Medication Use (10 elements): medication, dose, route, frequency, status, dates | Standard C-CDA depth |
| Allergies | ✅ Covered | Allergies and Intolerances (7 elements): allergen, reaction, severity, status | Standard C-CDA depth |
| Immunizations | ✅ Covered | History of Immunizations (7 elements): vaccine, date, route, dose, manufacturer | Standard C-CDA depth |
| Vitals | ✅ Covered | Vital Signs (8 elements): observation codes, values, units, dates | Standard C-CDA depth |
| Lab results | ✅ Covered | Laboratory/Diagnostic Results (7 elements): tests, values, ranges, dates | Standard C-CDA depth |
| Imaging / diagnostic reports | ⚠️ Partial | Laboratory/Diagnostic Results section may include imaging; no dedicated imaging section; Documents CSV may contain imaging documents | Product is certified for CPOE diagnostic imaging (a)(3); limited export evidence |
| Procedures | ✅ Covered | Procedures (6 elements): procedure codes, dates, performers | Standard C-CDA depth |
| Clinical notes / documents | ✅ Covered | Clinical Notes (9 elements) + Supplemental Documents CSV (12 fields): note types, content, authors, dates | Documents CSV adds depth with json_data and application_data |
| Care plans / goals | ✅ Covered | Treatment Plan (9 elements) + Assessments (7 elements): planned procedures, interventions | Standard C-CDA depth |
| Orders / referrals | ✅ Covered | Supplemental Orders CSV (14 fields): name, status, urgency, reason, times, visit linkage | Orders CSV goes beyond C-CDA |
| Insurance / coverage | ✅ Covered | Payers section (10 elements): payer, plan, member ID, coverage type, relationship | Standard C-CDA Payers section |
| Claims / billing | ⚠️ Partial | Supplemental Charges CSV (16 fields): rate, revenue_code, procedure_code, modifier, NDC, totals | Charges are present but no claims, superbills, payments, adjustments, or EOBs. Product has "Lunar Revenue Suite" — likely stores more than charges alone |
| Payments | ❌ Not covered | No payment entities in export | If Lunar Revenue Suite handles payments/collections, this is a gap |
| Consents / directives | ❌ Not covered | No consent or advance directive entities | May be in Documents CSV if stored as documents, but not explicitly covered |
| Patient communications / portal | ❌ Not covered | No messaging or portal communication entities | Product has patient portal (e)(1) certified; patient messages likely stored but not in export |
| Social history / SDOH | ✅ Covered | Social History (5 elements): social history observations with codes and values | Standard C-CDA depth |
| Functional / mental status | ✅ Covered | Functional Status (6 elements) + Mental/Cognitive Status (6 elements) | Standard C-CDA depth |
| Family health history | ❌ Not covered | No family health history section in C-CDA export | Product is certified for (a)(12) family health history; this data should be in the export |
| Related persons | ✅ Covered | Participant (5 elements): related persons with relationship codes | Standard C-CDA depth |

**Notable gap**: Family Health History is certified under (a)(12) and is a USCDI data class, but no corresponding section appears in the export's 18 C-CDA sections. This is a gap even by USCDI standards.

## 6. Documentation Quality

**Strengths:**
- All 188 fields have descriptions (100% coverage)
- Each C-CDA section includes example XML showing realistic synthetic data
- Template IDs and LOINC codes are documented for each section
- Supplemental CSV fields have explicit data types
- The document is clearly organized with a table of contents

**Weaknesses:**
- **No standalone sample export files** — a developer cannot see what a real export ZIP looks like
- **No machine-readable schema** — no JSON Schema, XSD, or CSV header spec; only the PDF
- **C-CDA "key elements" are high-level XML element names**, not a true field-level data dictionary. For example, `<observation>` and `<entry>` are structural containers, not data fields. The actual data granularity within each C-CDA section is defined by the C-CDA standard, not by this document.
- **No relationship/foreign key documentation** beyond visit UUIDs in supplemental CSVs
- **No value set enumerations** — code systems are referenced (SNOMED CT, RxNorm, LOINC) but no specific value sets are listed
- **Descriptions are sometimes truncated** in the key elements tables (appears to be a PDF formatting issue)
- **The "data" and "json_data" dict fields in supplemental CSVs are opaque** — no documentation of what structured data they contain

**Could a developer build an import?** Partially. For the C-CDA portion, a developer familiar with C-CDA could parse the XML using the template IDs. For the supplemental CSVs, the field definitions are clear enough but the dict/JSON fields are undocumented black boxes. There are no sample files to test against.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Partial**

The export covers clinical data adequately through standard C-CDA sections and makes a genuine effort to extend beyond C-CDA with supplemental CSV files for documents, orders, and charges. The Charges CSV with 16 fields (including revenue codes, procedure codes, modifiers, NDC, and totals) demonstrates awareness that billing data is part of the designated record set. However, relative to the product's stated scope — a full hospital information system with named Revenue, Lab, Operations, Analytics, and Patient suites — the export is thin:

- Only charges are exported from the Revenue Suite — no claims, payments, adjustments, or EOBs
- No patient portal communications despite (e)(1) certification  
- No family health history despite (a)(12) certification
- The Operations Suite, Analytics Suite, and IT Suite may store patient-relevant data that isn't exported
- The supplemental CSVs have opaque dict/JSON fields that could contain substantial additional data, but this is undocumented

The export goes meaningfully beyond USCDI (charges, orders, documents as supplemental CSVs) but doesn't demonstrably cover the full breadth of what a comprehensive HIS would store about patients.

**Axis 2 — Export approach: Purpose-built EHI export**

Despite being C-CDA-based, this is not simply a repackaged clinical exchange export. Key evidence:

1. The PDF is titled "Electronic Health Information Export" and explicitly references §170.315(b)(10) and the designated record set (45 CFR 164.502)
2. The supplemental CSV layer (Documents, Orders, Charges) is a proprietary Lunar format specifically created for this export — these are not part of standard C-CDA
3. The Charges CSV includes billing-specific fields (revenue_code, procedure_code, modifier, NDC) that would never appear in a (g)(10) FHIR API or standard C-CDA transition of care
4. The document explicitly states: "Supplemental Data is a proprietary Lunar data format that supplements a patient's C-CDA with any additional electronic health information... not captured by the standard C-CDA format"

The vendor clearly built a purpose-specific export that layers proprietary supplemental data on top of C-CDA. The question is whether the supplemental layer is complete enough — it covers only 3 categories (documents, orders, charges) with 42 fields total, which is thin for a full HIS.

### Key Findings

1. **The export is a genuine (b)(10) effort, not a repackaged clinical exchange.** The supplemental CSV layer with charges, orders, and documents goes beyond what any standard C-CDA or FHIR (g)(10) export would include. The Charges CSV (16 fields including revenue codes and NDC) is the strongest evidence.

2. **The supplemental layer is thin relative to product scope.** Only 3 supplemental categories with 42 total fields for a product that markets itself as a comprehensive hospital information system with 7 named suites. The charges data covers charge-level detail but not the full revenue cycle (no claims, payments, adjustments).

3. **Family Health History is missing despite certification.** The product is certified for (a)(12) family health history, which is a USCDI data class, but no corresponding section appears in the 18 C-CDA sections. This is a gap even at the USCDI level.

4. **Opaque dict/JSON fields may hide significant data.** The supplemental CSVs include `data`, `json_data`, and `application_data` fields typed as "dict" — these could contain substantial structured data but are completely undocumented. The actual data richness of the export may be greater than what the documentation reveals.

5. **No sample data or machine-readable schema.** Despite good descriptive documentation (100% of fields described), there are no sample export files, no XSD/JSON Schema, and no way to validate an implementation without access to a live system.

### Summary Stats

    Coverage:        Partial
    Approach:        Purpose-built EHI export
    Export format:   C-CDA XML + supplemental CSV (in ZIP)
    Entities:        21 (18 C-CDA sections + 3 supplemental CSV categories)
    Fields:          188 (146 C-CDA key elements + 42 CSV fields)
    Descriptions:    100%
    Sample data:     No (inline XML examples only)
    Bulk export:     Yes (per documentation)
    Domains covered: 14 of 18 applicable domains

### Bottom Line

Lunar has made a genuine effort to build a (b)(10) export that goes beyond standard C-CDA clinical exchange, notably including charge-level billing data and supplemental CSVs for documents and orders. However, for a product positioning itself as a comprehensive hospital information system with 7 named suites, exporting only 21 entities with 188 fields — and missing family health history, patient communications, payments, and consents — leaves significant gaps. The biggest strength is the honest attempt to include billing data; the biggest gap is the thinness of the supplemental layer relative to the product's stated scope.
