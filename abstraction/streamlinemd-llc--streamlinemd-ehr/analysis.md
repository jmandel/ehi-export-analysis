# EHI Export Analysis: StreamlineMD, LLC

**Product**: StreamlineMD EHR  
**Analysis date**: 2026-02-16  
**CHPL IDs**: 9974 (15.04.04.2383.Stre.15.00.1.190417)

## 1. Product Context

StreamlineMD EHR is a cloud-based ambulatory EHR and Practice Management (PM) platform purpose-built for interventional radiology and imaging specialists — interventional radiologists, vascular surgeons, vein specialists, and pain management providers. It is a product of StreamlineMD, LLC, a subsidiary of PRC Medical, LLC, a healthcare services company with 48+ years of history serving radiology practices across 42 states.

The product's core value proposition is tightly integrated clinical and billing workflows. Key capabilities include:

- **Clinical documentation**: Standardized templates for 500+ endovascular and interventional procedures, AI-powered documentation, nurse notes, procedure drawing tools
- **Practice management**: Enterprise scheduling, patient tracking, prior authorization management, referral management
- **Billing/Revenue cycle**: Charge capture that flows automatically from documentation, CPT/ICD-10 coding, claims submission, payment posting, denials management, patient payment estimator, online bill-pay
- **Patient engagement**: Patient portal with secure messaging, test result access, appointment scheduling, online payments
- **E-prescribing**: Medication management and electronic prescribing
- **Specialty features**: PACS integration, DICOM SR integration, inventory management for interventional supplies/devices, teleradiology workflow
- **Integrations**: Lab orders/results, FHIR API (g)(10), direct secure messaging

For EHI export assessment, the critical baseline is that this product stores: (1) clinical documentation including specialty interventional/radiology procedure data, (2) billing/claims/payment data as a core integrated module, (3) scheduling and referral data, (4) patient portal communications, (5) inventory/supply usage data, and (6) e-prescribing data. The vendor explicitly describes the tight integration of clinical documentation and billing as a core differentiator.

## 2. Artifacts Reviewed

| Artifact | Description | Informative? |
|---|---|---|
| `StreamlineMD-EHR-EHI-Export.pdf` (155 KB, 2 pages) | The **only** EHI export documentation. A title page (page 1) and three bullet points describing C-CDA/PDF export using USCDI v1 (page 2). Created 2023-10-30 by Smitesh Shah in Microsoft Word. | **Minimally informative** — confirms export format and standard but provides no data dictionary, schema, field definitions, sample data, or export instructions. |

Only one artifact exists. There are no additional data dictionaries, schemas, sample exports, or supplementary documentation in the downloads folder.

## 3. Export Mechanics

- **Format**: C-CDA documents and/or PDF files
- **Standard**: C-CDA with USCDI v1 data classes
- **Mechanism**: UI-based export ("clients export… without the intervention of software developers"); user selects a destination folder
- **Scope**: Single patient, multiple patients, or entire patient population
- **Bulk capability**: Yes — the documentation explicitly states export can be done for the "entire patient population"
- **Access constraints/fees**: Not documented

The PDF export likely renders the same clinical data as a human-readable document. The C-CDA export uses the standard C-CDA XML format constrained to USCDI v1 data classes.

## 4. Export Content: What's In It

### What the documentation states

The documentation explicitly references "C-CDA United States Core Data for Interoperability (USCDI v1) requirements" and provides a link to the ONC USCDI v1 specification. No additional data elements beyond USCDI v1 are mentioned.

USCDI v1 defines these data classes and elements:
- Allergies and Intolerances (substance, reaction, severity)
- Assessment and Plan of Treatment
- Care Team Members
- Clinical Notes (consultation note, discharge summary, history & physical, imaging narrative, laboratory report narrative, pathology report narrative, procedure note, progress note)
- Goals
- Health Concerns
- Immunizations
- Laboratory (tests, values/results)
- Medications
- Patient Demographics (name, DOB, address, phone, email, sex, race, ethnicity, preferred language)
- Problems (diagnoses)
- Procedures
- Provenance (author time stamp, author organization)
- Smoking Status
- Unique Device Identifier(s)
- Vital Signs (height, weight, BMI, blood pressure, heart rate, respiratory rate, temperature, pulse oximetry, inhaled O₂ concentration)

### What the documentation does NOT include

- **No data dictionary**: Zero entities, tables, or fields are documented
- **No field-level documentation**: No field names, types, descriptions, value sets, or relationships
- **No schema**: No machine-readable format specification
- **No sample data**: No example C-CDA documents or PDF exports
- **No mapping documentation**: No description of how StreamlineMD-specific data maps to C-CDA sections
- **No mention of non-USCDI data**: Billing, claims, payments, prior authorizations, inventory, specialty procedure templates, patient portal messages, referrals, and scheduling data are entirely absent from the documentation

### Vendor's own content organization

The vendor does not organize their export documentation into categories. The entire export description is three bullet points. There are no entities/tables to enumerate.

| Entity/Table | Fields | Described | Types | Category |
|---|---|---|---|---|
| *(none documented)* | — | — | — | — |

The `analysis/full-entity-inventory.json` file confirms: 0 entities, 0 fields documented.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor describes their (b)(10) export as a C-CDA/PDF export using USCDI v1 requirements. USCDI v1 is a defined subset of clinical data designed for interoperability — it was created for the (g)(10) Standardized API criterion, not for comprehensive EHI export.

The vendor provides no categories, modules, or sections of their own. The export is described in exactly 3 sentences across 3 bullet points. There is no depth to assess — the documentation says "we export C-CDA with USCDI v1" and nothing more.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | USCDI v1 includes basic demographics | USCDI v1 covers name, DOB, address, phone, sex, race, ethnicity, language. May miss specialty-specific registration fields. |
| Encounters / visits | ⚠️ Partial | C-CDA can include encounter sections | USCDI v1 does not have a dedicated encounters data class; encounters may appear as context in notes. Product tracks visits extensively — likely incomplete. |
| Problems / conditions / diagnoses | ⚠️ Partial | USCDI v1 "Problems" data class | Covers problem list but may miss diagnosis-level detail used in billing (ICD-10 coding for claims). |
| Medications / prescriptions | ⚠️ Partial | USCDI v1 "Medications" data class | Covers active medication list. Product has full e-prescribing — prescription history, pharmacy details, refill data likely not fully represented in C-CDA. |
| Allergies | ✅ Covered | USCDI v1 "Allergies and Intolerances" data class | Standard allergy data likely adequate. |
| Immunizations | ✅ Covered | USCDI v1 "Immunizations" data class | Likely adequate for this specialty. |
| Vitals | ✅ Covered | USCDI v1 "Vital Signs" data class | Standard vital signs covered. |
| Lab results | ⚠️ Partial | USCDI v1 "Laboratory" data class | Covers lab tests/results. Product integrates with lab interfaces — structured lab data may lose detail in C-CDA mapping. |
| Imaging / diagnostic reports | ⚠️ Partial | USCDI v1 includes "Imaging Narrative" in Clinical Notes | For a radiology/interventional product, imaging is core. USCDI v1 only supports imaging narratives, not structured imaging data, DICOM references, or PACS integration metadata. **Significant gap for this specialty.** |
| Procedures | ⚠️ Partial | USCDI v1 "Procedures" data class | Product has 500+ interventional procedure templates with drawing tools and specialty-specific documentation. Standard C-CDA procedure entries cannot capture this richness. **Significant gap.** |
| Clinical notes / documents | ⚠️ Partial | USCDI v1 "Clinical Notes" data class (8 note types) | Covers standard note types but specialty templates, nurse notes, procedure drawings, and AI-generated documentation may not map cleanly to C-CDA. |
| Care plans / goals | ⚠️ Partial | USCDI v1 "Goals" and "Assessment and Plan of Treatment" | Basic coverage. |
| Orders / referrals | ❌ Not covered | No mention in documentation; not in USCDI v1 | Product has referral management and lab/imaging ordering. Not addressed in USCDI v1 C-CDA export. **Gap.** |
| Insurance / coverage | ❌ Not covered | No mention in documentation; not in USCDI v1 | Product stores insurance/enrollment data. Not in C-CDA/USCDI v1. **Gap.** |
| Claims / billing | ❌ Not covered | No mention in documentation; not in USCDI v1 | Product has deeply integrated billing/RCM as a core differentiator — CPT/ICD-10 codes, charges, claims, payments, denials. Entirely absent. **Major gap.** |
| Payments | ❌ Not covered | No mention in documentation; not in USCDI v1 | Product includes payment posting, patient payments, online bill-pay. Not addressed. **Gap.** |
| Consents / directives | ❌ Not covered | No mention in documentation | Unknown if product stores consent data, but procedural consent is likely for interventional procedures. |
| Patient communications / portal messages | ❌ Not covered | No mention in documentation; not in USCDI v1 | Product has patient portal with secure messaging. Not addressed. **Gap.** |
| Specialty-specific (interventional radiology) | ❌ Not covered | No mention in documentation | Product's core specialty data — 500+ procedure templates, procedure drawings, interventional-specific clinical fields, inventory/supply usage per procedure, PACS/DICOM references — is not addressed. **Major gap for a specialty-focused product.** |

**Summary**: Of 18 assessed domains, 3 are adequately covered (allergies, immunizations, vitals), 8 are partially covered via generic USCDI v1 C-CDA mappings, and 7 are not covered at all. The uncovered domains include the product's most distinctive capabilities: integrated billing/RCM, specialty interventional procedure documentation, and patient portal communications.

## 6. Documentation Quality

The EHI export documentation is **extremely minimal**. Assessment:

- **Usability**: A developer cannot build an import from this documentation. The three bullet points confirm the format (C-CDA/PDF) and scope options (single/multiple/all patients) but provide zero technical detail.
- **Data dictionary**: None. No tables, entities, fields, types, descriptions, value sets, or relationships.
- **Schema/format specification**: None beyond "C-CDA USCDI v1" — which is an external standard reference, not vendor-specific documentation.
- **Sample data**: None. No example C-CDA documents or PDF exports.
- **Machine-readable artifacts**: None.
- **Export instructions**: None. No screenshots, no step-by-step guide, no UI description.
- **What requires guesswork**: Everything. A recipient would need to know the C-CDA standard independently and reverse-engineer any vendor-specific extensions or data mappings.

This documentation answers only two questions: "What format?" (C-CDA/PDF) and "How many patients?" (single/multiple/all). It does not answer: "What data is included?", "What data is excluded?", "How is the export triggered?", "What do the output files look like?", or "How does vendor-specific data map to C-CDA?"

## 7. Overall Assessment

### Classification

**Standard-based projection** — The export is explicitly described as a C-CDA export using USCDI v1, which is the standard clinical data interoperability format. This is a projection of the vendor's native data into a standard that was designed for clinical summaries, not comprehensive EHI export. The documentation makes no mention of any native database export, vendor-specific data beyond USCDI v1, or any mechanism to export billing, specialty, or administrative data.

This is a textbook case of a vendor repackaging their existing clinical summary/transitions-of-care export as their (b)(10) EHI export. The explicit reference to "USCDI v1 requirements" confirms the export scope is limited to the US Core Data for Interoperability subset — the same data set required for the (g)(10) Standardized API criterion.

### Key Findings

1. **The entire EHI export documentation is 3 bullet points on a single page** (`StreamlineMD-EHR-EHI-Export.pdf`, page 2). No data dictionary, no schema, no sample data, no export instructions. This is among the most minimal (b)(10) documentation possible.

2. **The export is explicitly a C-CDA/USCDI v1 projection, not a native data export.** The documentation references "C-CDA United States Core Data for Interoperability (USCDI v1) requirements" and links to the ONC USCDI v1 page. USCDI v1 covers a defined clinical summary subset — not all EHI.

3. **Billing/RCM data — the product's core differentiator — is entirely absent.** StreamlineMD's value proposition is tightly integrated clinical-to-billing workflow. The EHI export documentation makes no mention of billing, claims, charges, payments, CPT codes, or any financial data. C-CDA cannot represent this data.

4. **Specialty-specific data is not addressed.** The product stores rich interventional radiology data (500+ procedure templates, procedure drawings, PACS/DICOM references, inventory/supply usage). None of this is mentioned in the export documentation, and standard C-CDA sections cannot capture this specialty depth.

5. **No evidence of vendor engagement with (b)(10) requirements.** The documentation does not acknowledge that EHI encompasses more than USCDI v1 clinical data, does not discuss data domains beyond clinical summaries, and does not provide any path to obtaining billing, specialty, or administrative data.

### Summary Stats

    Classification:  Standard-based projection
    Export format:   C-CDA XML, PDF
    Model type:      Standard projection (C-CDA/USCDI v1)
    Entities:        N/A (no data dictionary)
    Fields:          N/A (no data dictionary)
    Descriptions:    N/A
    Sample data:     No
    Bulk export:     Yes (single, multiple, or all patients)
    Domains covered: 3 of 15 applicable domains adequately; 8 partial via USCDI v1

### Bottom Line

StreamlineMD's EHI export is a C-CDA clinical summary repackaged as a (b)(10) export. For a specialty product whose core value proposition is tightly integrated billing and interventional radiology workflows, the absence of billing data, specialty procedure documentation, and patient portal communications from the export represents a significant gap. A patient or provider requesting their complete health information would receive only the USCDI v1 clinical summary — missing the billing records, specialty-specific procedure details, and administrative data that constitute a substantial portion of their designated record set.
