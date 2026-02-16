# EHI Export Analysis: TenEleven Group

**Product**: electronic Clinical Record (eCR) v2.4
**Analysis date**: 2026-02-16
**CHPL ID**: 15.04.04.2861.Elec.24.01.1.221231

## 1. Product Context

TenEleven Group's electronic Clinical Record (eCR) is a comprehensive behavioral health EHR and practice management system serving mental health, substance use/addiction treatment, and human services agencies. Originally developed by TenEleven Group LLC (East Amherst, NY), the product is now part of the Ensora Health portfolio (formerly Therapy Brands, acquired by KKR in 2021). It targets larger behavioral health agencies (10+ users) rather than solo practitioners, with customers including Greenwich House (NYC, ~15,000 clients annually) and several New Jersey substance use treatment providers.

The product's feature set is broad for a behavioral health EHR:
- **Clinical documentation** with customizable FormLab templates, treatment planning, progress notes, and "Golden Thread" medical necessity documentation
- **Medication-Assisted Treatment (MAT)** — a key differentiator — with dosing schedules, dispensing with photo verification, tapering plans, and DEA/CMS compliance
- **E-prescribing and e-labs** (eRx module)
- **Medication Administration Record (MAR)** for inpatient/residential settings
- **Bed management** for residential/inpatient facilities
- **Billing and revenue cycle management** including electronic claims, ERA/EOB processing, credit card processing, and patient statements
- **Patient portal** (certified under (e)(1))
- **Scheduling** with alerts and integrated calendars
- **Intake/referral management** and **care transitions/discharge planning**
- **Compliance/reporting** including DSM-5, CCBHC support, and state system integrations (NJ PDMP, NJ SAMS)

This product stores a substantial amount of data across clinical, billing, specialty (MAT/behavioral health), and administrative domains. A complete (b)(10) export should cover all of these.

## 2. Artifacts Reviewed

| Artifact | Description | Informational Value |
|---|---|---|
| `PDF-for-Website-on-Formats-2.pdf` | 1-page PDF (116 KB, 111 words) describing two EHI export formats: JSON for single patient, .bak for population. Created 2023-11-30 by Catherine Baker in Microsoft Word. | **Primary (b)(10) documentation** — but contains no data dictionary, schema, or structural detail. The entire substantive content is two bullet points. |
| `screenshot-ehi-export-section.png` | Screenshot of the EHI Export section on the Ensora Health ONC disclosure page (https://ensorahealth.com/onc/teneleven/) | Confirms the vendor's two export modes (single patient, population) and that population export requires a Salesforce support ticket. |
| `screenshot-onc-page-top.png` | Screenshot of the ONC certification disclosure page header | Confirms product identity, version (2.4), certification number, and developer contact info. |
| `screenshot-fhir-api-docs.png` | Screenshot of FHIR API documentation at fhir.10e11.com | Shows the (g)(10) FHIR API documentation, branded "Dynamic FHIR" / "Therapy Brands." This is (g)(10), not (b)(10). |

**Verified via live fetch (2026-02-16):**
- The ONC disclosure page at https://ensorahealth.com/onc/teneleven/ is accessible and matches the screenshots. The "File Formats" button links to the same PDF.
- The FHIR API documentation at fhir.10e11.com is accessible and documents USCDI v1 resources via US Core profiles. It explicitly states "Available data via the API interface is limited by the data defined by the USCDI" and references (g)(7), (g)(9), (g)(10) — not (b)(10).

**Most informative**: The PDF and the live ONC page text are the only sources of (b)(10) information. **Least informative**: The FHIR API documentation, which documents a separate certification criterion.

## 3. Export Mechanics

**Two export mechanisms:**

1. **Single Patient Export**
   - **Format**: JSON
   - **Mechanism**: User-initiated via the eCR application UI ("without developer assistance")
   - **Scope**: Single patient
   - **Content**: Described as "USCDI v1 data as well as other applicable data" — the meaning of "other applicable data" is undefined and undocumented
   - **Access constraints**: Available to authorized users; no fee mentioned

2. **Patient Population Export**
   - **Format**: `.bak` (SQL Server database backup)
   - **Mechanism**: Vendor-assisted — requires submitting a support ticket via Salesforce
   - **Scope**: "All the data for a patient population" (described as full agency database)
   - **Content**: "A full SQL Server database backup of all data for an agency that can be restored"
   - **Access constraints**: Not self-service; requires vendor support; requires Microsoft SQL Server to restore; no fee mentioned but vendor involvement implies possible cost

The population export requires Microsoft SQL Server (a licensed proprietary product) to restore, creating a practical barrier to data portability.

## 4. Export Content: What's In It

### The documentation gap

There is **no data dictionary, no schema documentation, no field definitions, no entity descriptions, no sample data, and no machine-readable specification** for either export format. The vendor's entire (b)(10) documentation consists of 111 words across a single PDF page.

For the **single patient JSON export**, we know only that it includes "USCDI v1 data as well as other applicable data." The JSON structure, field names, nesting, data types, and relationship model are completely undocumented. It is unknown whether this JSON follows FHIR resource structures, mirrors the vendor's internal data model, or uses some other schema.

For the **population .bak export**, the vendor describes it as "a full SQL Server database backup of all data for an agency." If taken at face value, this would contain the vendor's complete database — every table, every row, every relationship — making it the most comprehensive possible export. However, without a schema or data dictionary, a recipient would need to restore the backup to SQL Server and reverse-engineer the entire database structure.

### FHIR API resources (for reference — this is (g)(10), not (b)(10))

The FHIR API at fhir.10e11.com supports 22 FHIR R4 resource types, all using US Core profiles:

| USCDI Category | FHIR Resource |
|---|---|
| Patient Demographics | Patient |
| Problem List | Condition |
| Procedures | Procedure |
| Smoking Status | Observation |
| Vital Signs | Observation |
| Laboratory Results | Observation, DiagnosticReport |
| Medications | MedicationRequest |
| Allergies | AllergyIntolerance |
| Immunizations | Immunization |
| Goals | Goal |
| Clinical Notes | DocumentReference, Binary |
| Care Plans | CarePlan |
| Care Teams | CareTeam |
| Implantable Devices | Device |
| Encounters | Encounter |
| Assessment/Plan | ClinicalImpression |
| Provenance | Provenance |
| Supporting | Patient, Practitioner, PractitionerRole, Organization, Location, Group |

The FHIR API explicitly states it is "limited by the data defined by the USCDI" — it does not cover billing, MAT-specific data, custom forms, bed management, or other behavioral health specialty data.

### Vendor's own content organization

There is no vendor-provided content organization, entity listing, or data dictionary. The vendor does not describe any tables, fields, or data categories for the (b)(10) export. The only structural information is the distinction between "USCDI v1 data" and "other applicable data" for the single patient export.

**No entity/field table can be generated** because no data dictionary exists.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor provides almost no information about what the export actually contains:

- **Single patient export**: Claims to include USCDI v1 data (demographics, problems, medications, allergies, immunizations, vitals, labs, procedures, clinical notes, care plans, goals, encounters) plus unspecified "other applicable data." No detail on what "other applicable data" means.
- **Population export**: Claims to be a "full SQL Server database backup of all data for an agency." If accurate, this would include everything in the database — clinical, billing, MAT, scheduling, bed management, custom forms — but there is zero documentation of the database schema.

The vendor does not organize content into categories, modules, or domains. There is no breakdown of what data areas are covered.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | Single patient: claimed via USCDI v1. Population: presumably in .bak. No schema documentation for either. | Product stores demographics; USCDI coverage likely but field-level content unknown. |
| Encounters / visits | ⚠️ Partial | Single patient: claimed via USCDI v1 (Encounter resource). Population: presumably in .bak. | Product stores encounter data; USCDI coverage likely but detail unknown. |
| Problems / conditions / diagnoses | ⚠️ Partial | Single patient: claimed via USCDI v1 (Condition). Population: presumably in .bak. | Product stores DSM-5 diagnoses and problem lists; USCDI may not capture behavioral health nuances. |
| Medications / prescriptions | ⚠️ Partial | Single patient: claimed via USCDI v1 (MedicationRequest). Population: presumably in .bak. | Product has e-prescribing and MAT; USCDI likely captures prescriptions but MAT dosing/dispensing data is unknown. |
| Allergies | ⚠️ Partial | Single patient: claimed via USCDI v1 (AllergyIntolerance). Population: presumably in .bak. | Likely covered at USCDI level. |
| Immunizations | ⚠️ Partial | Single patient: claimed via USCDI v1 (Immunization). Population: presumably in .bak. | Likely covered at USCDI level. |
| Vitals | ⚠️ Partial | Single patient: claimed via USCDI v1 (Observation). Population: presumably in .bak. | Likely covered at USCDI level. |
| Lab results | ⚠️ Partial | Single patient: claimed via USCDI v1 (Observation, DiagnosticReport). Population: presumably in .bak. | Product has e-labs; USCDI likely captures results but lab order details unknown. |
| Procedures | ⚠️ Partial | Single patient: claimed via USCDI v1 (Procedure). Population: presumably in .bak. | Likely covered at USCDI level. |
| Clinical notes / documents | ⚠️ Partial | Single patient: claimed via USCDI v1 (DocumentReference). Population: presumably in .bak. | Product has progress notes and FormLab templates; USCDI may not capture custom form data. |
| Care plans / goals | ⚠️ Partial | Single patient: claimed via USCDI v1 (CarePlan, Goal). Population: presumably in .bak. | Product has treatment planning with Goal/Objective Library; USCDI coverage likely partial. |
| Orders / referrals | ⚠️ Partial | Not explicitly documented. "Other applicable data" may include some. Population: presumably in .bak. | Product has intake/referral management; no evidence in single patient export. |
| Insurance / coverage | ❌ Not covered | No evidence in single patient export documentation. Population: presumably in .bak. | Product manages insurance information; gap in single patient export; undocumented in population export. |
| Claims / billing | ❌ Not covered | No evidence in single patient export documentation. Population: presumably in .bak. | Product has full RCM (claims, ERA/EOB, payments, statements); significant gap — no billing data documented in either export. |
| Payments | ❌ Not covered | No evidence in single patient export documentation. Population: presumably in .bak. | Product processes payments and credit cards; gap in documented export. |
| Patient communications / portal | ❌ Not covered | No evidence in either export's documentation. Population: presumably in .bak. | Product has patient portal; no evidence of portal data in export. |
| Specialty: MAT (dosing, dispensing, tapering) | ❌ Not covered | No evidence in single patient export documentation. "Other applicable data" is undefined. Population: presumably in .bak. | MAT is a core differentiator — dosing schedules, dispensing records, tapering plans, photo verification. None of this is documented as part of the export. Significant gap. |
| Specialty: Behavioral health assessments | ❌ Not covered | No evidence. Population: presumably in .bak. | Product has FormLab custom clinical forms, DSM-5 assessments, behavioral health-specific documentation. None documented in export. |
| Consents / directives | ❌ Not covered | No evidence in either export. | Unknown if product stores consent forms; cannot confirm gap. |
| Imaging / diagnostic reports | ⚠️ Partial | DiagnosticReport in USCDI. Population: presumably in .bak. | Likely limited to what USCDI covers. |

**Key assessment problem**: For the population export (.bak), the vendor claims it's "all data for an agency," which would theoretically cover every domain. But with zero schema documentation, there is no way to verify what is actually in the backup, and a recipient would have no guidance for interpreting the data. The "coverage" of the .bak format is theoretical, not practical.

For the single patient export, only USCDI v1 domains are explicitly claimed, leaving billing, MAT, custom forms, bed management, and other behavioral health specialty data either uncovered or undocumented.

## 6. Documentation Quality

**Documentation quality is extremely poor** — among the thinnest possible for a certified product.

- **Total documentation**: 1 PDF page, 111 words. No other (b)(10)-specific documentation exists.
- **Data dictionary**: None.
- **Field definitions**: None.
- **Entity/table descriptions**: None.
- **Schema documentation**: None.
- **Sample data**: None.
- **Machine-readable artifacts**: None.
- **Relationships/foreign keys**: None.
- **Value sets/code systems**: None.
- **Import/usage instructions**: None. No guidance on how to parse the JSON export or restore/interpret the .bak file.

**Could a developer build an import from this documentation?** No. A developer receiving the single patient JSON export would have no schema reference to parse it. A developer receiving the .bak file would need SQL Server, would need to restore the backup, and would then need to reverse-engineer the entire database schema — table names, column names, data types, relationships, coded values — with no documentation whatsoever.

The FHIR API documentation at fhir.10e11.com is substantially better — it includes USCDI-to-resource mappings, search parameters, sample responses, and API usage instructions. But this documents the (g)(10) API, not the (b)(10) EHI export. The vendor does not reference the FHIR API documentation as part of the EHI export documentation, and the two are presented as separate sections on the ONC disclosure page.

## 7. Overall Assessment

### Classification

**Minimal/stub**

The documentation is too thin to assess what the export actually contains. The single patient export is described in one sentence. The population export is described as a raw SQL Server backup with no schema documentation. No data dictionary, no field definitions, no sample data, no entity descriptions exist for either format.

While the population export (.bak) may in practice contain all data in the system, the complete absence of documentation renders it practically unusable for data portability without reverse engineering. The single patient export appears to be a USCDI v1 projection (possibly FHIR-based, given the FHIR infrastructure) with vague claims of "other applicable data."

### Key Findings

1. **The entire (b)(10) documentation is 111 words on a single PDF page.** There is no data dictionary, no schema, no sample data, no field definitions — nothing beyond two bullet points describing format names (JSON and .bak). This is among the thinnest documentation possible for a certified product.

2. **The population export (.bak) is a raw SQL Server database backup**, which would theoretically contain everything in the system but requires Microsoft SQL Server to restore and has zero documentation of its schema. This creates both a vendor lock-in barrier (proprietary format requiring licensed software) and a usability barrier (no guidance for interpreting the data).

3. **The single patient export claims "USCDI v1 + other applicable data"** but does not define what "other applicable data" means. For a behavioral health EHR with MAT dosing, custom FormLab assessments, billing/RCM, and bed management, USCDI v1 covers a small fraction of the data the product stores. The undefined "other applicable data" could bridge this gap — or could be nothing.

4. **The population export requires a vendor support ticket** (via Salesforce), making it non-self-service. This adds process friction and potential delays/costs to what should be a straightforward data export.

5. **Behavioral health specialty data is completely undocumented in the export.** MAT dosing/dispensing records, behavioral health assessments, FormLab custom forms, bed management, and DSM-5-specific clinical documentation are core product features with no documented representation in the export.

### Summary Stats

```
Classification:  Minimal/stub
Export format:   JSON (single patient), .bak SQL Server backup (population)
Model type:      Unknown (no schema documentation)
Entities:        N/A (no data dictionary)
Fields:          N/A
Descriptions:    N/A
Sample data:     No
Bulk export:     Yes (population via support ticket; .bak format)
Domains covered: 0 of 16 confirmed; ~10 claimed via USCDI v1 but undocumented
```

### Bottom Line

A patient or provider requesting their data from eCR would receive either an undocumented JSON file or a raw SQL Server database backup with no schema documentation. Neither format is practically usable for data portability without significant reverse engineering. For a product with deep behavioral health, MAT, billing, and custom form capabilities, the export documentation says essentially nothing about what data is included or how to interpret it. The single biggest gap is the complete absence of any data dictionary or schema — without it, the export's completeness cannot be verified and the data cannot be meaningfully used.
