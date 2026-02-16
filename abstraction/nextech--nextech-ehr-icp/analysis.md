# EHI Export Analysis: Nextech

**Product**: SRS EHR (SRSPro) and Nextech EHR (ICP)
**Analysis date**: 2026-02-16
**CHPL IDs**: 15.04.04.2051.SRSE.12.03.1.221202 (SRS EHR v12), 15.04.04.2051.Inte.09.02.0.251202 (Nextech EHR ICP v9)

## 1. Product Context

Nextech is a specialty-focused healthcare IT company serving 16,000+ practices and 11,000+ physicians across dermatology, ophthalmology, orthopedics, plastic surgery, and med spa. It operates **three distinct EHR/PM platforms** under the Nextech umbrella, two of which are CHPL-certified:

- **SRS EHR (SRSPro)** — Originating from SRS Health (acquired 2019), historically dominant in orthopedic surgery. Certified 2022-12-02. EHR with integrated PM, CPOE, e-prescribing, CDS, CQM reporting, and PACS integration. Notable: lacks (g)(10) FHIR API and (e)(1) patient portal certifications.
- **Nextech EHR (ICP / IntelleChartPRO)** — Cloud-based EHR for specialty practices. Certified 2025-12-02. Full feature set including patient portal (e)(1), FHIR API (g)(10), AI documentation (Cora Scribe), imaging/TouchMD, specialty templates, integrated billing, inventory management, CRM/lead tracking, and cosmetic workflow tools (quotes, packages, gift cards).
- **Nextech Select/NexCloud** — A third platform (not independently CHPL-certified in this metadata) with its own EHI export documentation.

**Data the products should export**: Patient demographics, encounters/clinical notes, problems/diagnoses, medications, allergies, immunizations, vitals, lab results, orders/results, imaging/PACS, procedures, referrals, family history, social history, implantable devices, insurance/guarantor information, billing/charges/payments, specialty-specific data (ophthalmology refractions, glaucoma flowsheets, retinal injection logs; orthopedic surgical data), custom forms/UDFs, patient communications/messages, documents/images, and care plans.

Both SRS EHR and ICP have integrated practice management and billing capabilities, so billing data is part of the designated record set for both.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `srspro-ehi-export-documentation.pdf` (8 pages) | EHI export documentation for SRSPro — folder structure, file formats (CSV/XML), C-CDA data classes, relationship notes between entities. | **High** — detailed structural documentation |
| `srspro-ehi-data-dictionary.xlsx` (19 sheets) | Data dictionary for SRSPro with 860 fields across 19 entities. Covers CSV and XML export formats. | **High** — primary field-level reference |
| `nextech-ehr-icp-ehi-export-documentation.pdf` (6 pages) | EHI export documentation for ICP — folder structure, file formats (JSON/XML/PDF), C-CDA data classes, single/bulk export, auditing. | **High** — good structural documentation |
| `nextech-ehr-icp-ehi-data-dictionary.xlsx` (19 sheets) | Data dictionary for ICP with 340 fields across 19 entities. Covers JSON, PDF, TXT formats. | **High** — primary field-level reference |
| `nextech-select-nexcloud-ehi-export-documentation.pdf` (8 pages) | EHI export documentation for Select/NexCloud — folder structure, CSV formats, billing data, custom data, iPad exports. | **High** — most complete billing coverage |
| `nextech-select-nexcloud-ehi-data-dictionary.xlsx` (16 sheets) | Data dictionary for NexCloud with 730 fields across 16 entities. Richest billing data. | **High** — deepest field-level detail |
| `ehi-export-page-screenshot.png` | Screenshot of the EHI documentation landing page. | Low — confirms page structure only |
| `enrichment/data-dictionaries.json` | Prior agent's parsed JSON of all three dictionaries. | Reference only — independently re-parsed |

## 3. Export Mechanics

All three platforms share a similar export approach:

- **Format**: ZIP file containing a mix of CSV/XML/JSON files (platform-dependent) plus C-CDA XML and documents/images as original files (PDF, JPG, etc.)
  - SRSPro: CSV + XML + C-CDA + Documents folder
  - ICP: JSON + PDF (chart notes) + C-CDA + Documents/Images folders
  - NexCloud/Select: CSV + EMN PDFs + C-CDA + Documents folder
- **Mechanism**: UI-initiated single-patient export. Bulk export available for ICP (via support ticket). SRSPro and NexCloud don't explicitly mention bulk capability.
- **Single-patient**: Yes, ZIP per patient.
- **Bulk capability**: ICP mentions bulk export via support ticket with auditing. SRSPro and NexCloud unclear.
- **Access constraints**: No fees mentioned. Export initiated by authorized users. Audit logging of who requested/downloaded.
- **File naming**: Patient name + ID + timestamp (e.g., `FirstNameInitial_LastName_PersonID_DateTimeStamp.ZIP`).

## 4. Export Content: What's In It

### Data Dictionary Statistics

| Platform | Entities | Total Fields | Described | Description % | Has Types |
|---|---|---|---|---|---|
| SRSPro | 19 | 860 | 826 | 96.0% | No |
| Nextech EHR (ICP) | 19 | 340 | 319 | 93.8% | No |
| Nextech Select/NexCloud | 16 | 730 | 730 | 100.0% | No |
| **Total** | **54** | **1,930** | **1,875** | **97.2%** | **No** |

None of the three data dictionaries include explicit data types, max lengths, nullability, foreign key definitions, or value sets. Descriptions are generally present but brief (e.g., "First name of the patient"). Some fields are marked "Non Clinical Data" without further explanation. Relationships between entities are documented narratively in the PDF documentation but not formally in the data dictionary.

### SRS EHR (SRSPro) — 19 entities, 860 fields

The SRSPro export combines CSV files for discrete clinical data, XML files for encounter-specific and results data, a C-CDA, and a Documents folder.

| Entity | Fields | Described | Format | Category |
|---|---|---|---|---|
| Encounter Data Capture (XMLs) | 404 | 404 | XML | Encounters (per-encounter files) |
| Results (XML) | 95 | 93 | XML | Lab/Results |
| Smoking Status (CSV) | 58 | 58 | CSV | Social History |
| Diagnoses (CSV) | 35 | 35 | CSV | Problems/Diagnoses |
| Implantable Devices (CSV) | 35 | 35 | CSV | Implantable Devices |
| Insurance Information (CSV) | 33 | 33 | CSV | Insurance |
| Orders (CSV) | 31 | 0 | CSV | Orders |
| GuarantorInformation (CSV) | 30 | 30 | CSV | Insurance |
| Messages (CSV) | 28 | 28 | CSV | Communications |
| Injections (CSV) | 26 | 26 | CSV | Medications/Injections |
| Vitals (XML) | 24 | 24 | XML | Vitals |
| Family History (CSV) | 18 | 18 | CSV | Family History |
| Medication (CCDA) | 13 | 13 | C-CDA | Medications |
| Family History Codes (CSV) | 12 | 12 | CSV | Family History |
| Family History Statuses (CSV) | 4 | 4 | CSV | Family History |
| Custom Alerts (CSV) | 4 | 3 | CSV | Alerts |
| CodeSystemNames (CSV) | 4 | 4 | CSV | Reference |
| UDFs (CSV) | 3 | 3 | CSV | Custom/UDFs |
| Appointment List (CSV) | 3 | 3 | CSV | Appointments |

**Notable**: The Encounter Data Capture entity is the largest at 404 fields, representing the full XML schema for per-encounter data including procedures (27 fields), diagnoses (31 fields), notes/narrative (34 fields), vitals (11 fields), social history (12 fields), lab/results (24 fields), care plans (11 fields), encounter metadata (15 fields), and 235 other fields covering various clinical domains. The Orders entity has 31 fields but **zero descriptions** — the only entity with this gap. Medications are documented only via C-CDA reference (13 fields), not as a separate discrete export.

**Missing from SRSPro**: No billing/charges/payments entities. No dedicated procedures CSV (procedures are embedded in encounter XML). No dedicated vitals CSV beyond the XML format. Demographics are covered by C-CDA only — no separate discrete demographic export.

### Nextech EHR (ICP) — 19 entities, 340 fields

The ICP export uses JSON files for most entities, PDFs for chart notes, and includes specialty-specific ophthalmology entities.

| Entity | Fields | Described | Format | Category |
|---|---|---|---|---|
| Patient Demographics (JSON) | 71 | 70 | JSON | Demographics |
| ChartNote (PDF) | 49 | 49 | PDF | Clinical Notes |
| Tasking_Microservice (JSON_CSV) | 47 | 46 | JSON/CSV | Communications |
| Refractions (JSON) | 31 | 31 | JSON | Ophthalmology |
| Insurance & Auth (JSON) | 22 | 22 | JSON | Insurance |
| Glaucoma Flowsheet (JSON) | 20 | 20 | JSON | Ophthalmology |
| Communications (PDF) | 14 | 13 | PDF | Communications |
| Referrals (JSON) | 13 | 13 | JSON | Referrals |
| Laboratory (JSON) | 12 | 0 | JSON | Lab/Results |
| Procedures (JSON) | 11 | 11 | JSON | Procedures |
| Specialty Medications | 10 | 10 | JSON | Medications |
| Patient Tasks | 10 | 10 | JSON | Communications |
| Appointments (JSON) | 7 | 7 | JSON | Appointments |
| Internal Communication (JSON) | 6 | 6 | JSON | Communications |
| Secure Messages (JSON) | 5 | 5 | JSON | Communications |
| Retina Injection Log (JSON) | 4 | 4 | JSON | Ophthalmology |
| Documents (TXT) | 3 | 0 | TXT | Documents |
| Images (TXT) | 3 | 0 | TXT | Images |
| Shared Care Comments (JSON) | 2 | 2 | JSON | Care Coordination |

**Notable**: ICP includes **ophthalmology-specific entities** (Glaucoma Flowsheet, Refractions, Retina Injection Log) with 55 fields — genuine specialty clinical data not available via C-CDA. Patient Demographics is the richest entity at 71 fields. The Laboratory entity has 12 fields but zero descriptions. The Tasking_Microservice entity at 47 fields appears to capture a wide range of task/workflow data.

**Missing from ICP**: No billing/charges/payments entities. No diagnoses/problems as a separate entity (covered by C-CDA only). No vitals entity. No family history entity. No smoking/social history entity. No orders entity.

### Nextech Select/NexCloud — 16 entities, 730 fields

NexCloud has the deepest data dictionary of the three, with comprehensive billing data.

| Entity | Fields | Described | Format | Category |
|---|---|---|---|---|
| Patient Demographics (CSV) | 212 | 212 | CSV | Demographics |
| Charges (CSV) | 140 | 140 | CSV | Billing |
| Insurances (CSV) | 85 | 85 | CSV | Insurance |
| Appointments (CSV) | 52 | 52 | CSV | Appointments |
| Payments (CSV) | 50 | 50 | CSV | Billing |
| EMN (PDF) | 43 | 43 | PDF | Clinical Notes |
| Recalls (CSV) | 27 | 27 | CSV | Recalls |
| Notes (CSV) | 23 | 23 | CSV | Notes |
| Recalls Steps (CSV) | 17 | 17 | CSV | Recalls |
| Follow up (CSV) | 16 | 16 | CSV | Follow-up |
| iPad Tasks (CSV) | 15 | 15 | CSV | Communications |
| Payment Plans (CSV) | 13 | 13 | CSV | Billing |
| DSI feedback | 11 | 11 | CSV | Other |
| PracYakker (CSV) | 10 | 10 | CSV | Internal Messaging |
| iPad Notes (CSV) | 9 | 9 | CSV | Notes |
| Custom (CSV) | 7 | 7 | CSV | Custom |

**Notable**: NexCloud is the **only platform with explicit billing data** — Charges (140 fields), Payments (50 fields), and Payment Plans (13 fields) totaling 203 billing fields. Patient Demographics at 212 fields is exceptionally detailed. All 730 fields have descriptions.

**Missing from NexCloud**: No dedicated diagnoses/problems entity. No medications entity. No vitals entity (clinical data in EMN PDFs). No lab/results entity. No allergies entity. No immunizations entity. No procedures entity. No family history entity. Clinical discrete data is largely relegated to C-CDA and EMN PDFs.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

Each platform has different strengths. Nextech's approach splits the EHI export across three strategies:

1. **C-CDA**: All three platforms export a standard C-CDA covering USCDI-scope clinical data (demographics, allergies, medications, problems, procedures, vitals, labs, immunizations, care teams, goals, health concerns, etc.).

2. **Discrete data files** (CSV/XML/JSON): Each platform supplements the C-CDA with product-specific discrete data exports. These go beyond C-CDA in important ways:
   - **SRSPro**: Deep encounter-level XML (404 fields per encounter), orders/results in XML, injections, family history (3 related CSVs), smoking status (58 fields), implantable devices, insurance/guarantor info, messages, and custom alerts/UDFs
   - **ICP**: Ophthalmology-specific data (glaucoma flowsheets, refractions, retinal injection logs), specialty medications, multiple communication channels (secure messages, internal comms, patient tasks, tasking microservice), referrals, shared care, and 71-field demographics
   - **NexCloud**: Billing (charges, payments, payment plans — 203 fields), 212-field demographics, 85-field insurance, custom data, internal messaging (PracYakker), recalls, iPad-specific exports

3. **Documents and images**: All platforms export attached documents and images as original files.

**Key gap**: SRSPro and ICP — the two CHPL-certified products — have **no billing data** in their EHI exports, despite both having integrated practice management with billing capabilities. Only NexCloud/Select (which is not a separate CHPL-certified product) includes billing.

### 5b. Standardized domain coverage (top-down)

Since this analysis covers two certified products, I assess both. NexCloud is included for reference but is not independently CHPL-certified.

| Domain | SRSPro | ICP | Evidence | Gap Analysis |
|---|---|---|---|---|
| Demographics | ⚠️ Partial | ✅ Covered | SRSPro: via C-CDA only (no separate discrete export). ICP: 71-field JSON entity | SRSPro relies entirely on C-CDA for demographics |
| Encounters / visits | ✅ Covered | ✅ Covered | SRSPro: 404-field Encounter Data Capture XML per encounter + 3-field Appointments. ICP: Encounter folders with ChartNote PDFs + C-CDA + 7-field Appointments JSON | SRSPro's encounter XML is deeply detailed |
| Problems / diagnoses | ✅ Covered | ⚠️ Partial | SRSPro: 35-field Diagnoses CSV + encounter XML. ICP: C-CDA only, no discrete entity | ICP has no dedicated problems export |
| Medications / prescriptions | ⚠️ Partial | ⚠️ Partial | SRSPro: 13-field Medication via C-CDA ref + 26-field Injections CSV. ICP: 10-field Specialty Medications JSON + 4-field Retina Injection Log | Neither has a comprehensive medication list export |
| Allergies | ⚠️ Partial | ⚠️ Partial | Both: C-CDA only. SRSPro encounter XML has 2 allergy fields | No dedicated allergy entities in either |
| Immunizations | ⚠️ Partial | ⚠️ Partial | Both: C-CDA only | No discrete immunization export |
| Vitals | ✅ Covered | ⚠️ Partial | SRSPro: 24-field Vitals XML. ICP: C-CDA only | ICP has no dedicated vitals entity |
| Lab results | ✅ Covered | ⚠️ Partial | SRSPro: 95-field Results XML + Orders CSV. ICP: 12-field Laboratory JSON (no descriptions) | SRSPro has deep results; ICP is thin |
| Imaging / diagnostic reports | ⚠️ Partial | ⚠️ Partial | Both: Documents/Images folders with original files. Results in encounter data | No structured imaging report entities |
| Procedures | ⚠️ Partial | ✅ Covered | SRSPro: embedded in encounter XML (27 fields). ICP: 11-field Procedures JSON | SRSPro lacks dedicated procedures export |
| Clinical notes / documents | ✅ Covered | ✅ Covered | SRSPro: Encounter XML + Documents folder. ICP: ChartNote PDF (49 fields) + Documents/Images folders | Both well-covered |
| Care plans / goals | ⚠️ Partial | ⚠️ Partial | Both: C-CDA includes Plan of Treatment and Goals | No dedicated care plan entities |
| Orders / referrals | ✅ Covered | ✅ Covered | SRSPro: 31-field Orders CSV (no descriptions) + Results XML. ICP: 13-field Referrals JSON | SRSPro orders lack descriptions |
| Insurance / coverage | ✅ Covered | ✅ Covered | SRSPro: 33-field Insurance Info + 30-field Guarantor CSVs. ICP: 22-field Insurance & Auth JSON | Both have dedicated entities |
| Claims / billing | ❌ Not covered | ❌ Not covered | Neither certified product exports billing data | **Significant gap** — both products have integrated PM/billing |
| Payments | ❌ Not covered | ❌ Not covered | No payment entities in either | **Significant gap** |
| Patient communications | ✅ Covered | ✅ Covered | SRSPro: 28-field Messages CSV. ICP: Secure Messages, Internal Comms, Communications, Patient Tasks, Tasking Microservice (72 fields across 4 entities) | ICP especially thorough |
| Specialty-specific | ⚠️ Partial | ✅ Covered | SRSPro: encounter XML captures specialty data generically. ICP: Glaucoma Flowsheet (20 fields), Refractions (31 fields), Retina Injection Log (4 fields) | ICP has genuine ophthalmology-specific entities |
| Family history | ✅ Covered | ❌ Not covered | SRSPro: 3 CSV files (34 fields total). ICP: C-CDA only | ICP has no dedicated family history |
| Social history | ✅ Covered | ⚠️ Partial | SRSPro: 58-field Smoking Status CSV. ICP: C-CDA only | SRSPro is deeply detailed |
| Custom forms / UDFs | ✅ Covered | ⚠️ Partial | SRSPro: 3-field UDFs CSV + 4-field Custom Alerts. ICP: no dedicated custom entity (some data in Tasking) | Modest coverage in both |
| Consents / directives | ❌ Not covered | ✅ Covered | SRSPro: no consent entity. ICP: Consents folder with signed PDFs | ICP exports signed consent forms |
| Implantable devices | ✅ Covered | ⚠️ Partial | SRSPro: 35-field ImplantableDevices CSV. ICP: C-CDA only | SRSPro has dedicated entity |

**Summary**: SRSPro covers 10 of 21 domains at ✅ level, 7 at ⚠️, 4 at ❌. ICP covers 8 of 21 at ✅, 9 at ⚠️, 4 at ❌. The most critical shared gap is the complete absence of billing/payment data from both certified products' exports.

## 6. Documentation Quality

**Strengths:**
- All three platforms have dedicated EHI export documentation PDFs with folder structure descriptions, file format details, and guidance on relationships between entities (e.g., Orders-Results linked by RequisitionId).
- Data dictionaries in XLSX format with individual sheets per entity — well-organized and machine-parseable.
- High description rates: 96-100% of fields have descriptions across platforms.
- The PDFs include helpful notes about edge cases (e.g., how deleted records are handled, what happens when no data exists, how insurance IDs map).

**Weaknesses:**
- **No data types** documented in any dictionary. Fields like "PatientProblemId" could be integer, GUID, or string — undocumented.
- **No value sets or enumerations**. Status fields, type fields, and coded values have no documented allowed values.
- **No formal relationships/foreign keys**. Relationships are described narratively in the PDF (e.g., "RequisitionId is the OrderID") but not structured in the dictionary.
- **Some entities lack descriptions entirely**: SRSPro's Orders (31 fields, 0 described), ICP's Laboratory (12 fields, 0 described), ICP's Documents and Images (3 fields each, 0 described).
- **No sample data** provided for any platform.
- **No machine-readable schema** (JSON Schema, XSD, etc.) beyond the XLSX dictionary.

**Overall**: A developer could understand the *structure* of the export but would need to reverse-engineer data types, value sets, and some relationships. The documentation is workmanlike but not self-sufficient for building an import pipeline without access to actual exported data.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Partial**

Both certified products (SRS EHR and Nextech EHR ICP) go meaningfully beyond C-CDA/USCDI by exporting product-specific discrete data in CSV/XML/JSON alongside the C-CDA. SRSPro's 404-field encounter XML, 95-field results XML, 58-field smoking status, and 35-field implantable devices are genuine depth beyond what C-CDA provides. ICP's ophthalmology-specific entities (glaucoma, refractions, retinal injections) represent real specialty clinical data. However, the **complete absence of billing/payment data** from both certified products is a significant gap. Both products have integrated PM and billing — SRS Health was described as providing "EHR/EMR, PM, and PACS software solutions" and ICP's feature list includes extensive billing, claims, POS, and payment plan capabilities. The fact that NexCloud/Select (which shares the same EHI documentation page) includes 203 fields of billing data (Charges, Payments, Payment Plans) shows that Nextech *knows* billing is part of EHI but only implemented it for one platform. Additionally, several clinical domains (allergies, immunizations, care plans, vitals in ICP) rely solely on C-CDA with no discrete export.

**Axis 2 — Export approach: Purpose-built EHI export**

Despite the billing gap, these are clearly purpose-built (b)(10) exports, not repackaged C-CDA or FHIR. Each platform has a unique export architecture with product-specific data entities, custom folder structures, and discrete data formats that go well beyond what C-CDA or FHIR bulk data would provide. The documentation explicitly references 170.315(b)(10), describes custom ZIP structures, and includes entities (UDFs, custom alerts, internal messaging, specialty clinical data, encounter-level XML with hundreds of fields) that have no equivalent in standard clinical exchange formats. The vendor built three separate export systems for three separate platforms.

### Key Findings

1. **No billing data in either certified product**: Both SRS EHR and Nextech EHR (ICP) omit billing, charges, payments, and payment plans entirely — despite having integrated billing/PM capabilities. Only the non-CHPL-certified NexCloud/Select platform includes billing (203 fields). This is the single largest gap.

2. **SRSPro's encounter XML is genuinely deep**: The 404-field Encounter Data Capture XML is the richest single entity across all three platforms, capturing procedures, diagnoses, medications, notes, vitals, social history, and care plans at an encounter-specific level.

3. **ICP exports specialty ophthalmology data**: Glaucoma Flowsheet (20 fields), Refractions (31 fields), and Retina Injection Log (4 fields) are genuine specialty clinical data that goes beyond USCDI and standard clinical exchange — a positive signal of purpose-built (b)(10) engagement.

4. **Documentation quality is inconsistent**: While 97.2% of fields have descriptions overall, no data types are documented anywhere, and key entities (SRSPro Orders, ICP Laboratory) have zero field descriptions. No sample data or machine-readable schemas are provided.

5. **Three platforms, three exports, uneven coverage**: Each platform covers different domains — SRSPro is strongest on encounter-level clinical data, ICP on communications and specialty data, NexCloud on billing and demographics. No single platform provides complete coverage across all domains.

### Summary Stats

```
Coverage:        Partial
Approach:        Purpose-built EHI export
Export format:   Mixed (CSV + XML + JSON + PDF + C-CDA, varies by platform)
Entities:        54 total (SRSPro: 19, ICP: 19, NexCloud: 16)
Fields:          1,930 total (SRSPro: 860, ICP: 340, NexCloud: 730)
Descriptions:    97.2% of fields have descriptions
Sample data:     No
Bulk export:     ICP only (via support ticket)
Domains covered: ~14 of 21 applicable domains (across both certified products)
```

### Bottom Line

Nextech built genuine purpose-built EHI exports for all three platforms with product-specific data dictionaries and discrete clinical data beyond C-CDA — this is real (b)(10) work, not a repackaged standard export. However, **both CHPL-certified products (SRS EHR and Nextech EHR ICP) completely omit billing and payment data** despite having integrated PM/billing capabilities, making the export incomplete for the designated record set. The billing gap is especially notable because Nextech's third platform (NexCloud/Select) does export billing data, demonstrating awareness of the requirement but inconsistent implementation.
