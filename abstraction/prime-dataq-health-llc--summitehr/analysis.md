# EHI Export Analysis: Prime DataQ Health, LLC

**Product**: summitEHR  
**Analysis date**: 2026-02-15  
**CHPL IDs**: 11689 (15.04.04.3236.Davi.01.00.1.250827)

## 1. Product Context

summitEHR is a cloud-based ambulatory EHR developed jointly by DataQ Health (a population health / value-based care company) and Summus Health Care, a multi-specialty physician network in Dallas–Fort Worth. It targets internal medicine, endocrinology, and cardiology practices. The product was certified on August 27, 2025 (version 1.0), making it a very new entrant.

Based on ONC certification and the vendor website, summitEHR stores:

- **Clinical data**: demographics, problem lists, medication lists, medication allergy lists, clinical notes (with voice-enabled charting and smart templates), lab orders/results, vitals, immunizations, implantable devices, social/psychological/behavioral data (a)(15), family history, care plans
- **E-prescribing**: via NewCrop integration, including EPCS
- **Orders**: CPOE for medications, labs, and diagnostic imaging
- **Patient portal**: view/download/transmit certified (e)(1)
- **Telehealth**: built-in capabilities
- **Care coordination**: C-CDA generation (b)(1)–(b)(3), Direct messaging (h)(1) via EMR Direct
- **Analytics**: quality metrics dashboards, CQM reporting (c)(1)–(c)(3)
- **Scheduling**: integrated appointment scheduling with reminders

**Billing/PM status is unclear.** The website mentions "financial performance dashboards" and "auto-coding assistance," but does not explicitly describe claims management, charge capture, or revenue cycle management. It is unknown whether summitEHR includes integrated billing or relies on external PM systems.

This baseline means the export should cover at minimum: demographics, encounters, problems, medications, allergies, immunizations, vitals, labs, clinical notes, care plans, orders, prescriptions, implantable devices, social/behavioral data, and insurance information. Billing data coverage depends on whether the product stores it.

## 2. Artifacts Reviewed

| Artifact | Description | Informative? |
|---|---|---|
| `EHI-Export-Documentation-SummitEHR-v1.0.pdf` (377 KB, 4 pages) | The sole EHI export artifact. A PDF created 2025-12-03 by "Abdur Rehman" via Microsoft Print to PDF from a Word document. Contains: (1) cover page, (2) TSV format description with trivial example, (3–4) bulleted list of 47 resource names. **No data dictionary, no field definitions, no schemas, no sample data.** | Minimally informative — only provides resource names |

**No other artifacts exist.** The vendor's ONC certification page links only to this PDF for EHI export documentation. No additional data dictionaries, JSON schemas, sample export files, or supplemental documentation were found.

## 3. Export Mechanics

- **Format**: TSV (Tab-Separated Values) — one file per resource type
- **Mechanism**: Manual UI-based export ("lets you manually export")
- **Scope**: Single-patient or full practice population (bulk)
- **Bulk structure**: For population exports, a separate TSV file is generated per resource type; each row contains data for one patient
- **Access constraints/fees**: Not documented
- **Export instructions**: None provided — no screenshots, no step-by-step guide, no description of where to find the feature in the UI

The TSV format is a reasonable choice for a (b)(10) export — it's simple, portable, and suggests a native data model export rather than a FHIR/C-CDA repackaging.

## 4. Export Content: What's In It

### What we know

The PDF lists **47 resource type names** that the export covers. This is the complete extent of the documentation. There is:

- **No field/column documentation** — zero fields defined across all 47 resources
- **No data types** specified
- **No descriptions** of what any resource contains
- **No relationships** or foreign keys described
- **No value sets** or coded values documented
- **No sample data** (only a trivial 5-column example: PatientID, FirstName, LastName, DOB, Gender)
- **No schema** in any format

### Vendor's own content organization

The vendor presents the 47 resources as a flat alphabetical list with no categorization. For analytical purposes, I've grouped them by clinical domain (see `analysis/full-entity-inventory.json` for the full machine-readable inventory):

| Resource Name | Fields | Described | Types | Assigned Category |
|---|---|---|---|---|
| Allergies | 0 (unknown) | 0 | No | Allergies |
| Appointment reminders | 0 (unknown) | 0 | No | Encounters / Visits |
| Appointments | 0 (unknown) | 0 | No | Encounters / Visits |
| Assessments | 0 (unknown) | 0 | No | Other |
| Care plans | 0 (unknown) | 0 | No | Care Plans / Goals |
| Cognitive statuses | 0 (unknown) | 0 | No | Social / Behavioral |
| Diet | 0 (unknown) | 0 | No | Other |
| Document Details | 0 (unknown) | 0 | No | Clinical Notes / Documents |
| Encounter built procedures | 0 (unknown) | 0 | No | Encounters / Visits |
| Encounters | 0 (unknown) | 0 | No | Encounters / Visits |
| Exam | 0 (unknown) | 0 | No | Encounters / Visits |
| Family history | 0 (unknown) | 0 | No | Family History |
| Family history diseases | 0 (unknown) | 0 | No | Family History |
| Follow up appointments | 0 (unknown) | 0 | No | Encounters / Visits |
| Functional statuses | 0 (unknown) | 0 | No | Social / Behavioral |
| Goals | 0 (unknown) | 0 | No | Care Plans / Goals |
| Immunizations | 0 (unknown) | 0 | No | Immunizations |
| Implantable devices | 0 (unknown) | 0 | No | Implantable Devices |
| Interventions | 0 (unknown) | 0 | No | Care Plans / Goals |
| Lab order diagnosis | 0 (unknown) | 0 | No | Lab / Diagnostics |
| Lab Orders | 0 (unknown) | 0 | No | Lab / Diagnostics |
| Lab test result notes | 0 (unknown) | 0 | No | Lab / Diagnostics |
| Lab test results | 0 (unknown) | 0 | No | Lab / Diagnostics |
| Lab tests | 0 (unknown) | 0 | No | Lab / Diagnostics |
| Medications | 0 (unknown) | 0 | No | Medications |
| Past medical history | 0 (unknown) | 0 | No | Problems / Conditions |
| Past surgeries | 0 (unknown) | 0 | No | Procedures / Surgeries |
| Patient addresses | 0 (unknown) | 0 | No | Demographics |
| Patient care team members | 0 (unknown) | 0 | No | Care Team |
| Patient contacts | 0 (unknown) | 0 | No | Demographics |
| Patient information | 0 (unknown) | 0 | No | Demographics |
| Patient insurances | 0 (unknown) | 0 | No | Insurance / Payments |
| Patient payments | 0 (unknown) | 0 | No | Insurance / Payments |
| Patient races | 0 (unknown) | 0 | No | Demographics |
| Patient tasks | 0 (unknown) | 0 | No | Other |
| Patient vitals | 0 (unknown) | 0 | No | Vitals |
| PHQ 9 screening | 0 (unknown) | 0 | No | Social / Behavioral |
| Pregnancy status | 0 (unknown) | 0 | No | Other |
| Prior authentication | 0 (unknown) | 0 | No | Other |
| Problems | 0 (unknown) | 0 | No | Problems / Conditions |
| Progress notes | 0 (unknown) | 0 | No | Clinical Notes / Documents |
| Related person details | 0 (unknown) | 0 | No | Care Team |
| SDOH | 0 (unknown) | 0 | No | Social / Behavioral |
| Smoking status | 0 (unknown) | 0 | No | Social / Behavioral |
| Social history | 0 (unknown) | 0 | No | Social / Behavioral |
| Unsigned documents | 0 (unknown) | 0 | No | Clinical Notes / Documents |
| Vaping status | 0 (unknown) | 0 | No | Social / Behavioral |

**Summary by category:**

| Category | Resources | Fields Documented |
|---|---|---|
| Social / Behavioral | 7 | 0 |
| Encounters / Visits | 6 | 0 |
| Lab / Diagnostics | 5 | 0 |
| Other | 5 | 0 |
| Demographics | 4 | 0 |
| Care Plans / Goals | 3 | 0 |
| Clinical Notes / Documents | 3 | 0 |
| Care Team | 2 | 0 |
| Family History | 2 | 0 |
| Insurance / Payments | 2 | 0 |
| Problems / Conditions | 2 | 0 |
| Allergies | 1 | 0 |
| Immunizations | 1 | 0 |
| Implantable Devices | 1 | 0 |
| Medications | 1 | 0 |
| Procedures / Surgeries | 1 | 0 |
| Vitals | 1 | 0 |
| **Total** | **47** | **0** |

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor provides no categorization — just a flat list of 47 resource names. The resource names suggest breadth across clinical domains, including some that go beyond basic clinical summaries:

**Strongest signals of genuine EHI scope:**
- Insurance and payment resources (`Patient insurances`, `Patient payments`) — these go beyond C-CDA/FHIR clinical summaries
- Social determinants and behavioral screening (`SDOH`, `PHQ 9 screening`, `Cognitive statuses`, `Functional statuses`) — (a)(15) data
- Lab data broken into 5 separate resources (`Lab Orders`, `Lab tests`, `Lab test results`, `Lab test result notes`, `Lab order diagnosis`) — suggests granular native model, not a clinical summary projection
- `Encounter built procedures`, `Exam` as separate from `Encounters` — suggests internal table structure
- `Unsigned documents` — operational clinical data that wouldn't appear in a clinical summary

**Thinnest areas:**
- Medications: single resource called "Medications" with no indication of whether it covers prescriptions, medication administration, refills, pharmacy routing (product has NewCrop e-prescribing integration)
- Procedures: only "Past surgeries" and "Encounter built procedures" — no standalone procedure resource
- Orders: only lab orders are explicit; no separate medication order or imaging order resource despite CPOE certification for all three

**Without field-level documentation, it is impossible to determine the actual depth of any resource.** A resource named "Patient information" could have 5 fields or 50.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | `Patient information`, `Patient addresses`, `Patient contacts`, `Patient races` (4 resources, 0 documented fields) | Resource names suggest coverage, but no field detail to confirm completeness |
| Encounters / visits | ⚠️ Partial | `Encounters`, `Exam`, `Encounter built procedures`, `Appointments`, `Appointment reminders`, `Follow up appointments` (6 resources) | Multiple resources suggest structured encounter data; field content unknown |
| Problems / conditions | ⚠️ Partial | `Problems`, `Past medical history` (2 resources) | Present by name; field depth unknown |
| Medications / prescriptions | ⚠️ Partial | `Medications` (1 resource) | Single generic resource. Product has NewCrop e-prescribing with EPCS — unclear whether prescription details, pharmacy routing, controlled substance data are captured |
| Allergies | ⚠️ Partial | `Allergies` (1 resource) | Present by name; field depth unknown |
| Immunizations | ⚠️ Partial | `Immunizations` (1 resource) | Present by name |
| Vitals | ⚠️ Partial | `Patient vitals` (1 resource) | Present by name |
| Lab results | ⚠️ Partial | `Lab Orders`, `Lab tests`, `Lab test results`, `Lab test result notes`, `Lab order diagnosis` (5 resources) | Most granular domain — 5 separate resources suggest real internal model. Field content unknown |
| Imaging / diagnostic reports | ❌ Not covered | No imaging-specific resource | Product is certified for CPOE diagnostic imaging (a)(1)/(a)(12); imaging orders/results may be stored but are not explicitly represented in the export |
| Procedures | ⚠️ Partial | `Past surgeries`, `Encounter built procedures` | Surgical history present; in-encounter procedures present; no standalone procedures resource |
| Clinical notes / documents | ⚠️ Partial | `Progress notes`, `Unsigned documents`, `Document Details` (3 resources) | Notes and documents represented; product has voice-enabled charting and smart templates |
| Care plans / goals | ⚠️ Partial | `Care plans`, `Goals`, `Interventions` (3 resources) | Present by name |
| Orders / referrals | ⚠️ Partial | `Lab Orders` only | Lab orders covered; no explicit medication orders, imaging orders, or referrals resource despite CPOE certification |
| Insurance / coverage | ⚠️ Partial | `Patient insurances` (1 resource) | Present by name |
| Claims / billing | ❌ Not covered | No claims, charges, or billing code resources | Unclear whether product stores billing data (see Section 1). If it does, this is a gap |
| Payments | ⚠️ Partial | `Patient payments` (1 resource) | Present by name; may be limited to patient co-pays rather than full payment posting |
| Consents / directives | ❌ Not covered | No consent or advance directive resource | Product likely stores some consent data; gap depends on what the product manages |
| Patient communications / portal messages | ❌ Not covered | No secure messaging or portal message resource | Product has a patient portal with secure messaging — this data is not represented in the export |
| Specialty-specific (cardiology, endocrinology) | ❌ Not covered | No specialty-specific resources | Product targets cardiology and endocrinology; no disease-specific assessments, treatment protocols, or specialty forms visible |

**Coverage summary: 0 of 18 domains can be confirmed as fully covered** due to total absence of field-level documentation. 13 domains have at least a resource name that suggests coverage, but actual depth is unknowable. 5 domains have no representation at all.

## 6. Documentation Quality

The documentation quality is **critically deficient**:

- **No data dictionary exists.** The documentation provides only resource names — the equivalent of listing table names without any column definitions.
- **Zero fields documented** across all 47 resources.
- **No data types, no value sets, no relationships** — nothing beyond a name.
- **No sample export files** — only a trivial 5-column example that appears to be illustrative rather than real.
- **No machine-readable artifacts** — no JSON schema, no TSV header specification, no formal data model.
- **No export instructions** — the documentation says the feature "lets you manually export" but provides no UI walkthrough.
- **No information on how resources relate** — a recipient would not know how to join `Lab Orders` with `Lab test results` without examining actual export files.

A developer receiving this documentation alone could not build an import. They would know they're getting 47 TSV files but would have to reverse-engineer every column from the data itself. The documentation is one step above "we support EHI export" — it at least names the 47 resource types, but provides no information about their contents.

The PDF is 4 pages: 1 cover page, ~1 page of TSV format explanation, ~2 pages of bulleted resource names. The entire substantive content could fit in a single page.

## 7. Overall Assessment

### Classification

**Minimal/stub** — While the list of 47 resource names suggests an intent to export native data model content (not just C-CDA/FHIR), the total absence of field-level documentation makes the export effectively opaque. The documentation is too thin to confirm what is actually exported, how complete it is, or whether a recipient could use it. This is a compliance checkbox, not a genuine data portability effort.

### Key Findings

1. **Zero field-level documentation.** The entire EHI export documentation is a 4-page PDF listing 47 resource type names with no column definitions, data types, descriptions, relationships, value sets, or sample data. This is the thinnest documentation possible while still naming the data entities. (Source: `EHI-Export-Documentation-SummitEHR-v1.0.pdf`, pages 3–4)

2. **Resource list suggests native model, not standard repackaging.** The 47 resources use vendor-specific names (e.g., "Encounter built procedures," "Prior authentication," "Unsigned documents") that do not map to FHIR resources or C-CDA sections. This suggests the export is drawn from the product's internal data model, which is a positive signal. (Source: `EHI-Export-Documentation-SummitEHR-v1.0.pdf`, pages 3–4)

3. **Insurance and payment resources included — but billing depth is unknown.** The presence of `Patient insurances` and `Patient payments` is a positive signal that the export goes beyond clinical data. However, without field documentation, it's impossible to know whether these contain meaningful billing detail or just a coverage summary. (Source: `EHI-Export-Documentation-SummitEHR-v1.0.pdf`, page 3)

4. **Multiple domains entirely unrepresented.** Imaging/diagnostic reports, patient portal messages, consents, and specialty-specific clinical data (cardiology, endocrinology) have no corresponding resources despite being core to the product's intended use. (Source: comparison of resource list against certified criteria and vendor website)

5. **Very new product, very new documentation.** SummitEHR was certified 2025-08-27; the PDF was created 2025-12-03. The v1.0 designation and sparse documentation may reflect the product's early stage rather than a deliberate decision to withhold detail.

### Summary Stats

```
Classification:  Minimal/stub
Export format:   TSV (Tab-Separated Values)
Model type:      Likely native database (based on resource names), but unverifiable
Entities:        47
Fields:          N/A (zero fields documented)
Descriptions:    0% (no field documentation exists)
Sample data:     No (only a trivial illustrative example)
Bulk export:     Yes (single-patient and full population)
Domains covered: 0 confirmed; 13 of 18 plausible based on resource names alone
```

### Bottom Line

summitEHR's EHI export documentation is a minimal stub: 47 resource names in a 4-page PDF with zero field-level detail. While the resource list hints at a genuine native data model export covering clinical, insurance, and payment data, the complete absence of a data dictionary means a recipient cannot determine what data is actually exported, how fields are structured, or how resources relate to each other. The single biggest gap is the lack of any field documentation whatsoever — this makes the export effectively unusable without access to actual export files for reverse-engineering.
