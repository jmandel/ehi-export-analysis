# EHI Export Analysis: CareCloud, Inc.

**Product**: talkEHR
**Analysis date**: 2026-02-16
**CHPL IDs**: 9799 (15.04.04.2790.Talk.01.01.1.181217)

## 1. Product Context

talkEHR is a cloud-based ambulatory EHR and practice management platform developed by CareCloud, Inc. (formerly MTBC). Launched in 2017 as a voice-enabled EHR, it serves small to mid-sized independent medical practices across 70+ specialties. It is an integrated platform combining:

- **Clinical EHR**: Patient charting with specialty-specific templates, clinical documentation with voice dictation, CPOE, clinical decision support, e-prescribing (Surescripts including controlled substances)
- **Practice Management**: Appointment scheduling, patient check-in, staff scheduling, reporting
- **Medical Billing / RCM**: Insurance claim submission, payment posting, denial management, end-to-end revenue cycle management
- **Patient Engagement**: Patient portal (talkPHR) with secure messaging, self-service scheduling, lab results viewing, telehealth/video visits
- **Interoperability**: FHIR APIs (g)(10), Direct messaging, public health reporting (immunization registries, syndromic surveillance, cancer/electronic case reporting)
- **Analytics**: PrecisionBI Lite dashboards, financial analytics, customizable reports

The product is certified for 45+ ONC criteria including (a)(1)–(a)(5), (a)(12) family health history, (a)(14)–(a)(15), (b)(1)–(b)(3), (b)(7)–(b)(11), (c)(1)–(c)(4), (d)(1)–(d)(13), (e)(1)/(e)(3), (f)(1)/(f)(2)/(f)(4)/(f)(6)/(f)(7), (g)(2)–(g)(7)/(g)(9)/(g)(10), and (h)(1).

**Baseline expectation**: A complete EHI export should cover clinical data across all charting workflows, medications/e-prescribing data, lab results, billing/claims data, insurance information, patient portal communications, appointment history, and clinical documents.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `talkEHR-b10-EHI-Export-Documentation.pdf` (1.1 MB, 12 pages) | The sole EHI export documentation. Contains overview (pp. 1–3), export UI screenshots (pp. 4–5), C-CDA field mapping with XPATHs and code systems (pp. 6–10), one-sentence descriptions of 6 PDF export categories (p. 11), one-sentence FHIR mention (p. 12). Created 2023-11-14 by Jahanzaib Nisar in Microsoft Word 2013. | **Primary source** — most informative artifact |
| `cost-and-fees-information.html` (61 KB) | talkEHR's ONC mandatory disclosures page on Webflow. Lists all 45+ certified criteria, CQMs, and has footer link to the b(10) PDF. Last published Fri Jan 30 2026. | Low — only confirms the PDF link exists |
| `screenshot-footer-with-b10-link.png` (229 KB) | Screenshot of page footer showing the b(10) documentation link under "Legal & Compliance". | Minimal — visual confirmation only |
| `screenshot-b10-link-footer.png` (3 KB) | Focused screenshot of the b(10) link element. | Minimal |

**No sample data files, no machine-readable schemas, no API documentation, no data dictionary beyond the C-CDA field mapping table.** The entire EHI export documentation is a single 12-page PDF.

## 3. Export Mechanics

- **Format**: Dual-format — C-CDA R2.1 XML for clinical data + PDF for non-clinical data. FHIR mentioned but undocumented.
- **Single Patient Export**: Navigate to CCDA Report → CCDA Export tab → select patient → Generate → Download XML file.
- **Bulk Patient Export**: Navigate to CCDA Report → Data Portability tab → select date range → Export → downloads ZIP file of C-CDA XML files.
- **PDF Exports**: Via the application's "Reports" section — export appointments, demographics/insurance, messages, billing data, and documents as individual PDFs.
- **FHIR Export**: Page 12 states "talkEHR FHIR server creates a single-patient FHIR resource Document Reference and supports FHIR Bulk Data EHI Export for patient population as described in § 170.315(b)(10)(ii)." No endpoint URLs, API documentation, resource types, or profiles are provided.
- **Access**: User-initiated via UI; "A user of the Product can perform an electronic health information (EHI) export at any time the user chooses without developer assistance."
- **Fees**: Mandatory disclosures page states "No" for additional fees.
- **Output organization**: "The files created by the export are saved to a folder specified by the user. Documents can be sorted and categorized as per their Type."

## 4. Export Content: What's In It

### C-CDA XML Component (Pages 6–10)

The PDF documents 24 C-CDA sections containing 82 data elements (fields). The mapping table provides, for each field: the data element name, an XPATH or entry template reference, a code system OID (where applicable), and the code system name. This follows the HL7 C-CDA R2.1 standard (§ 170.205(a)(4)).

Of the 82 C-CDA fields:
- **28 fields** (34%) have a code system specified (OID + name)
- **30 fields** (37%) have an XPATH or template reference
- **0 fields** have descriptions beyond the field name
- **0 fields** have data types, nullability, or value set bindings documented
- **13 distinct code systems** are referenced: AdministrativeGender, CDC Race & Ethnicity, CPT, CPT-4, SNOMED, ICD-10, CVX, NCI Thesaurus, LOINC, RxNorm, NDC, HCPCS, GMDN

### PDF Export Component (Page 11)

Six categories of data are exported as PDF, each described in a single sentence with no field-level documentation:

| Category | Documentation Provided |
|---|---|
| Patient Demographic/Insurance | "a comprehensive view of demographics and insurance details" |
| Advance Directive | "a comprehensive view of Advance Directive" |
| Appointments | "a comprehensive view of appointments" |
| Provider-to-Patient Messages | "a comprehensive view of messages" |
| Billing Data (Claim) | "a comprehensive view of billing data (CPT, ICD, Modifier)" |
| Documents | "signed progress notes, available lab results, radiology reports, and any other scanned or uploaded document" |

No field names, no data types, no sample PDFs, no structure specification. The billing export mentions "CPT, ICD, Modifier" but does not specify what other billing fields (dates of service, amounts, payer info, adjustments) are included.

### FHIR Component (Page 12)

One sentence mentions FHIR Bulk Data support and a DocumentReference resource. No resource types listed, no endpoint URLs, no profiles, no API documentation. This is essentially an assertion without evidence.

### Vendor's own content organization

| Section | Fields | With Code Systems | With XPATHs | Format | Category |
|---|---|---|---|---|---|
| Patient Demographics/Information | 6 | 2 | 6 | C-CDA XML | Clinical |
| Provider's name and office contact information | 3 | 0 | 3 | C-CDA XML | Clinical |
| Date and Location of visit | 2 | 0 | 2 | C-CDA XML | Clinical |
| Chief Complaint and Reason for Visit | 1 | 0 | 0 | C-CDA XML | Clinical |
| Encounters | 5 | 2 | 1 | C-CDA XML | Clinical |
| Immunizations | 9 | 3 | 1 | C-CDA XML | Clinical |
| Instructions | 1 | 1 | 1 | C-CDA XML | Clinical |
| Treatment Plan | 2 | 1 | 1 | C-CDA XML | Clinical |
| Social History | 3 | 2 | 1 | C-CDA XML | Clinical |
| Problems | 3 | 1 | 1 | C-CDA XML | Clinical |
| Medications | 5 | 1 | 1 | C-CDA XML | Clinical |
| Medication Allergies | 4 | 4 | 1 | C-CDA XML | Clinical |
| Laboratory Tests | 4 | 1 | 0 | C-CDA XML | Clinical |
| Laboratory Information | 5 | 0 | 0 | C-CDA XML | Clinical |
| Laboratory value(s)/result(s) | 5 | 1 | 1 | C-CDA XML | Clinical |
| Vitals | 2 | 1 | 1 | C-CDA XML | Clinical |
| Goal | 3 | 0 | 1 | C-CDA XML | Clinical |
| Procedures | 2 | 1 | 1 | C-CDA XML | Clinical |
| Care team member(s) | 3 | 0 | 1 | C-CDA XML | Clinical |
| Reason for Referral | 1 | 1 | 1 | C-CDA XML | Clinical |
| Medical Equipment | 2 | 2 | 1 | C-CDA XML | Clinical |
| Mental Status | 4 | 1 | 1 | C-CDA XML | Clinical |
| Functional Status | 4 | 1 | 1 | C-CDA XML | Clinical |
| Health Concern | 3 | 1 | 1 | C-CDA XML | Clinical |
| Patient Demographic/Insurance | 0 | — | — | PDF | Non-clinical |
| Advance Directive | 0 | — | — | PDF | Non-clinical |
| Appointments | 0 | — | — | PDF | Non-clinical |
| Provider-to-Patient Messages | 0 | — | — | PDF | Non-clinical |
| Billing Data (Claim) | 0 | — | — | PDF | Non-clinical |
| Documents | 0 | — | — | PDF | Non-clinical |
| FHIR Data Export | 0 | — | — | FHIR | Undocumented |

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The export has two clearly documented tiers:

**Tier 1 — C-CDA clinical data (well-documented)**: 24 sections covering standard ambulatory clinical data: demographics, encounters, problems, medications, allergies, immunizations, labs, vitals, procedures, goals, care plans, referrals, social history, mental/functional status, health concerns, and implantable devices. This maps closely to the USCDI/US Core Data for Interoperability set — it's the standard C-CDA clinical summary, not a native data model export. The field mapping (82 fields, XPATHs, code systems) is the strongest part of the documentation.

**Tier 2 — PDF non-clinical data (barely documented)**: 6 categories covering demographics/insurance, advance directives, appointments, messages, billing, and clinical documents. Each category gets a single boilerplate sentence. No field-level specification whatsoever. Exporting structured data (billing claims, appointment schedules) as non-machine-readable PDF is a significant limitation — a recipient could read it visually but could not programmatically import it.

**FHIR (unverifiable)**: A one-sentence mention of FHIR Bulk Data support with zero technical detail. Cannot be assessed.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | C-CDA: 6 fields (name, sex, DOB, race, ethnicity, language). PDF: "comprehensive demographics" (undocumented) | C-CDA has basic USCDI demographics. PDF may cover more (address, phone, emergency contacts) but no way to verify from documentation |
| Encounters / visits | ✅ Covered | C-CDA: Encounters section (5 fields), Date/Location section (2 fields), Chief Complaint (1 field) | Standard C-CDA encounter data |
| Problems / conditions / diagnoses | ✅ Covered | C-CDA: Problems section (3 fields) with SNOMED + ICD-10, Health Concern section (3 fields) | Standard C-CDA problem list |
| Medications / prescriptions | ⚠️ Partial | C-CDA: Medications section (5 fields) with RxNorm + NDC | Covers medication list but likely misses e-prescribing workflow data (refill requests, pharmacy routing, controlled substance details, drug interaction alert history) that talkEHR stores |
| Allergies | ✅ Covered | C-CDA: Medication Allergies section (4 fields) with RxNorm + SNOMED | Standard allergy data with substance, reaction, severity |
| Immunizations | ✅ Covered | C-CDA: Immunizations section (9 fields) with CVX, CPT-4, NCI, SNOMED | Most detailed C-CDA section; includes vaccine, date, status, route, site, manufacturer, dose, lot, notes |
| Vitals | ✅ Covered | C-CDA: Vitals section (2 fields) with LOINC | Minimal but standard |
| Lab results | ✅ Covered | C-CDA: 3 lab sections (14 fields total) — tests, lab info, results with LOINC | Reasonably detailed for C-CDA |
| Imaging / diagnostic reports | ⚠️ Partial | PDF Documents export includes "radiology reports" | Only as PDF documents — no structured radiology data |
| Procedures | ✅ Covered | C-CDA: Procedures section (2 fields) with CPT-4/SNOMED/HCPCS | Standard procedure data |
| Clinical notes / documents | ✅ Covered | PDF Documents export: "signed progress notes, available lab results, radiology reports, and any other scanned or uploaded document" | Exported as PDF files — preserves content but not as structured data |
| Care plans / goals | ✅ Covered | C-CDA: Treatment Plan section (2 fields), Goal section (3 fields) | Standard C-CDA care plan data |
| Orders / referrals | ⚠️ Partial | C-CDA: Reason for Referral section (1 field with SNOMED); Treatment Plan mentions "Referrals to other providers" | Referral reason documented but order management details (order status, ordering provider, fulfillment) not addressed |
| Insurance / coverage | ⚠️ Partial | PDF: "comprehensive view of demographics and insurance details" (no field-level detail) | Mentioned but completely undocumented. As PDF, not machine-readable. Product stores detailed insurance/payer data for billing |
| Claims / billing | ⚠️ Partial | PDF: "comprehensive view of billing data (CPT, ICD, Modifier)" (no field-level detail) | Product has full RCM with claim submission, payment posting, denial management. Export mentions CPT/ICD/Modifier only. Amounts, dates of service, payer adjudication, payment details — unknown if included. PDF format makes any billing data non-computable |
| Payments | ❌ Not covered | No mention of payment data in export | Product supports payment posting and revenue cycle management. Payment data is EHI (billing records about individuals). Significant gap |
| Consents / directives | ⚠️ Partial | PDF: "comprehensive view of Advance Directive" (no field-level detail) | Advance directives mentioned but undocumented. Broader consent data (data segmentation per (b)(7) certification) not addressed |
| Patient communications / portal messages | ⚠️ Partial | PDF: "comprehensive view of messages" (no field-level detail) | Provider-to-patient messages exported but as undocumented PDF. Patient-initiated portal activity (appointment requests, demographic updates, patient-entered data) not mentioned |
| Family health history | ❌ Not covered | Not mentioned in any export section | Product is certified for (a)(12) Family Health History but this data domain does not appear anywhere in the export documentation. Genuine gap |

### Notable gaps

1. **Family health history**: Certified for (a)(12) but entirely absent from export documentation.
2. **Payments**: Product handles payment posting and RCM but export documentation does not mention payment records.
3. **E-prescribing details**: Product has extensive e-prescribing (Surescripts, controlled substances, refill management) but export only captures the medication list via C-CDA, not prescription workflow data.
4. **Specialty-specific data**: Product advertises 70+ specialty templates. Custom specialty data (assessments, specialty-specific clinical fields) would not fit in standard C-CDA sections and is not mentioned in the export.

## 6. Documentation Quality

**Strengths:**
- The C-CDA field mapping (pages 6–10) provides genuine technical detail: field names, XPATH references, template IDs, code system OIDs, and code system names for 82 data elements across 24 sections.
- The document is organized with a table of contents and includes UI screenshots showing the export workflow.
- Export mechanisms for both single-patient and bulk export are clearly described.

**Weaknesses:**
- **No field-level documentation for PDF exports.** Six categories of data get one generic sentence each. A developer cannot determine what fields appear in a billing PDF or a demographics/insurance PDF.
- **No sample data or examples.** No sample C-CDA XML, no sample PDF export, no worked examples of export output.
- **No machine-readable schema.** No JSON schema, no XSD beyond the standard C-CDA reference, no CSV column specifications.
- **FHIR documentation is a single sentence.** No API endpoints, no resource types, no SMART/OAuth details, no bulk data operation documentation.
- **No data types, relationships, or value set bindings** beyond code system names. No indication of which fields are required vs. optional, max lengths, or cardinality.
- **No descriptions.** The 82 C-CDA fields have names and XPATHs but zero descriptive text explaining what they contain.

**Could a developer build an import from this documentation?** For C-CDA clinical data: yes, by following the C-CDA R2.1 standard (the documentation adds XPATHs that help locate data). For PDF exports: no — field structures are completely unspecified. For FHIR: no — nothing actionable is documented.

## 7. Overall Assessment

### Classification

**Standard-based projection**

The export is fundamentally a C-CDA clinical summary augmented with undocumented PDF exports for non-clinical data and an unverifiable FHIR mention. The C-CDA portion maps standard clinical data elements to the HL7 CDA R2.1 structure — this is a projection of EHR data into a standard format, not a native database model export. The PDF exports attempt to cover data beyond C-CDA's scope (billing, appointments, messages) but use a non-machine-readable format with no field-level specification.

This is not a native data model export. The vendor does not expose internal table structures, database schemas, or vendor-specific data entities. The 82 documented fields represent standard C-CDA content, not the full breadth of data talkEHR stores (which includes RCM workflows, e-prescribing details, specialty templates, patient portal activity, and more).

### Key Findings

1. **C-CDA is the primary export format** — 24 sections, 82 fields, with XPATH and code system references. This is a standard clinical summary, not a comprehensive EHI export. It covers USCDI-level clinical data but not billing workflows, specialty data, or practice management data.

2. **Billing/non-clinical data is exported as PDF** — a non-machine-readable format with no field-level documentation. The vendor acknowledges billing, appointments, insurance, and messages need to be exported but provides them as visual-only PDFs. This effectively traps structured data in a non-computable format.

3. **Family health history is missing despite certification** — the product is certified for (a)(12) Family Health History, but this data domain does not appear in any section of the export documentation.

4. **FHIR Bulk Data is claimed but undocumented** — page 12 asserts FHIR Bulk Data EHI export support in a single sentence with no technical detail. This is unverifiable from the documentation alone and may or may not address coverage gaps.

5. **No sample data, no machine-readable schemas** — the documentation is a 12-page Word-to-PDF conversion. No artifacts exist that would allow independent validation of export content or automated import development.

### Summary Stats

```
Classification:  Standard-based projection
Export format:   C-CDA R2.1 XML + PDF + FHIR (undocumented)
Model type:      Standard projection (C-CDA) with PDF supplements
Entities:        24 C-CDA sections + 6 PDF categories + 1 FHIR mention = 31 total
Fields:          82 (C-CDA only; PDF and FHIR sections have 0 documented fields)
Descriptions:    0% (no field has a description beyond its name)
Sample data:     No
Bulk export:     Yes (Data Portability tab for C-CDA ZIP; FHIR Bulk Data claimed)
Domains covered: 8 of 17 applicable domains fully; 7 partial; 2 not covered
```

### Bottom Line

talkEHR's EHI export is a standard C-CDA clinical summary supplemented by undocumented PDF exports for billing, insurance, appointments, and messages. A patient would get their clinical data in a portable standard format but their billing records, insurance details, and other non-clinical data only as non-machine-readable PDFs with no field specifications. The single biggest gap is the use of PDF for structured data — exporting billing claims and insurance records as PDFs rather than computable formats undermines data portability for a product whose core selling points include RCM and billing management.
