# EHI Export Analysis: Nexus Clinical LLC

**Product**: Nexus EHR
**Analysis date**: 2026-02-16
**CHPL IDs**: 15.04.04.2989.Nexu.07.03.1.221227

## 1. Product Context

Nexus EHR is a cloud-based, unified ambulatory EHR platform from Nexus Clinical LLC (a small vendor with ~10-19 employees). It is a single product combining EHR, practice management, medical billing, patient portal, telehealth, and eFax. It targets small-to-midsize ambulatory practices (solo to 50+ physicians) across 25+ specialties. Pricing starts at ~$275-299/month per NPI.

Key capabilities relevant to EHI completeness:
- **Clinical EHR**: Charting, problem lists, medications, allergies, immunizations, vitals, lab results, imaging (DICOM/PACS), clinical notes, orders (CPOE for meds/labs/imaging), e-prescribing (EPCS via NewCrop)
- **Practice Management**: Scheduling, appointment reminders, patient intake forms, document scanning/importing, eFax, inventory management
- **Medical Billing**: Superbill/charge capture, claims submission, fee schedules, revenue cycle management, insurance eligibility verification, payment processing
- **Patient Portal**: Secure messaging, appointment requests, health questionnaires, demographic updates, online payments, visit summaries
- **Telehealth**: Video visits via Google Meet
- **Interoperability**: C-CDA exchange, FHIR APIs (g)(10), HL7 interfaces, Direct messaging, public health reporting

The product stores clinical records, billing/claims data, documents, patient communications, scheduling data, and administrative records. A complete EHI export should cover all of these domains.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/EHI-Export-Documentation.pdf` (774 KB, 2 pages) | Primary EHI export documentation. Describes export components, formats, and scope. Created 2023-11-30 in Microsoft Word 2010. | **Most informative** — the sole substantive artifact describing the export |
| `downloads/Nexus_EHR_Costs_And_Considerations.pdf` (178 KB) | ONC-required costs/considerations disclosure. Lists pricing for base product and add-ons. Confirms FHIR API is a separate paid subscription. | Moderately useful — confirms EHI export is part of base product and separate from FHIR API |
| `downloads/costs-and-limitations-page-full.png` (515 KB) | Screenshot of the costs and limitations webpage. | Low informativeness — visual record only |

No data dictionary, sample data, machine-readable schemas, or field-level documentation was provided.

## 3. Export Mechanics

- **Format**: Mixed — C-CDA R2.1 for clinical data, CSV for billing/demographics/appointments, native files (PDF, DOC, HTML, JPG, etc.) for documents
- **Mechanism**: UI-based export module accessible to admin users. Population exports may require coordination with Nexus support for monitoring.
- **Single-patient**: Yes — individual patient export supported
- **Bulk/population**: Yes — population-level export supported with some differences (documents exported as index CSV with offline utility for actual file retrieval)
- **Output**: ZIP file download
- **Access constraints**: Admin users only. No additional fees mentioned for EHI export (included in base product). Population export "may require time from few seconds to several hours."
- **Fees**: None apparent; EHI export is part of base certified product per costs disclosure

## 4. Export Content: What's In It

The export documentation is a 2-page PDF that describes 7 export components at a high level. **No data dictionary exists** — there are zero field-level definitions for any component. No column names, types, descriptions, relationships, value sets, or sample data are provided for any of the CSV files or C-CDA content.

### Vendor's own content organization

The vendor organizes the export into 5 numbered categories (some with sub-components):

| Entity/Component | Format | Fields Documented | Types Documented | Category (vendor's) |
|---|---|---|---|---|
| Clinical Data | C-CDA R2.1 | 0 | No | Clinical |
| Claims | CSV | 0 | No | Billing |
| Insurance Payment Details | CSV | 0 | No | Billing |
| Patient Payment Details | CSV | 0 | No | Billing |
| Patient Documents | Native files | 0 | No | Documents |
| Future Appointments | CSV | 0 | No | Administrative |
| Patient Demographics and Insurance | CSV | 0 | No | Demographics |

**Total entities**: 7 described export components
**Total documented fields**: 0 (no data dictionary)
**Fields with descriptions**: 0
**Fields with types**: 0
**Sample data**: None provided
**Machine-readable schema**: None provided

The clinical data component references C-CDA R2.1 with USCDI V1 compliance. The vendor links to generic external references (hl7.org/ccdasearch and healthit.gov USCDI page) rather than providing product-specific documentation of what C-CDA sections or data elements are populated.

The billing component names three CSV files (Claims, Insurance Payment Details, Patient Payment Details) but provides no column definitions.

The demographics/insurance component describes its content as "contact details, address, emergency contact, primary/secondary insurance, and responsible party information" but no field-level detail.

The documents component lists 6 document types exported in native format.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor describes 5 broad categories:

1. **Clinical Data (C-CDA)**: The broadest component but entirely reliant on the C-CDA R2.1 standard with USCDI V1 compliance. No vendor-specific extensions or customizations are described. This would cover standard clinical domains (problems, medications, allergies, immunizations, vitals, labs, procedures, clinical notes) but only to the depth defined by C-CDA R2.1 / USCDI V1 — which is the regulatory floor for clinical exchange, not a comprehensive clinical export.

2. **Billing (3 CSV files)**: This is the most notable aspect of the export. The vendor explicitly separates billing data (claims, insurance payments, patient payments) from clinical data and exports it in CSV format. This goes beyond what a repackaged C-CDA export would provide. However, without field-level documentation, we cannot assess the depth — we don't know if "Claims" includes diagnosis codes, procedure codes, modifiers, place of service, rendering provider, filing status, adjustment reasons, etc.

3. **Documents**: Documents exported in native format is reasonable and thorough in concept, covering chart notes, scanned documents, faxes, software-generated forms, PE images, and other imports. The population export limitation (index CSV + offline utility) is a practical accommodation.

4. **Demographics/Insurance**: Described as including contact details, address, emergency contact, and primary/secondary insurance with responsible party. This suggests some depth beyond basic demographics but no field detail.

5. **Future Appointments**: Only future-dated appointments are exported. Historical encounter/appointment data is presumably in the C-CDA but this is not explicit.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | "Patient Demographics and Insurance" CSV — described as contact details, address, emergency contact | Mentioned but no field detail; we can't verify completeness |
| Encounters / visits | ⚠️ Partial | C-CDA may include encounter history; chart note PDFs provide visit documentation | No dedicated encounter export; reliance on C-CDA encounter section (USCDI V1 scope) |
| Problems / conditions | ⚠️ Partial | C-CDA R2.1 includes Problems section | Standard C-CDA depth only; product likely stores more detail internally |
| Medications / prescriptions | ⚠️ Partial | C-CDA R2.1 includes Medications section; e-prescribing via NewCrop | Standard C-CDA depth only; prescription history detail unclear |
| Allergies | ⚠️ Partial | C-CDA R2.1 includes Allergies section | Standard C-CDA depth only |
| Immunizations | ⚠️ Partial | C-CDA R2.1 includes Immunizations section | Standard C-CDA depth only |
| Vitals | ⚠️ Partial | C-CDA R2.1 includes Vital Signs section | Standard C-CDA depth only |
| Lab results | ⚠️ Partial | C-CDA R2.1 includes Results section | Standard C-CDA depth only; eLab interface data may be richer than C-CDA captures |
| Imaging / diagnostic reports | ⚠️ Partial | C-CDA may include some results; PE Images in document export | Product has DICOM/PACS integration; unclear if imaging data beyond documents is exported |
| Procedures | ⚠️ Partial | C-CDA R2.1 includes Procedures section | Standard C-CDA depth only |
| Clinical notes / documents | ✅ Covered | Chart notes, scanned documents, faxes, forms, PE images exported as native files | Strong — documents exported in original format with multiple types listed |
| Care plans / goals | ⚠️ Partial | C-CDA R2.1 may include Goals/Care Plan sections per USCDI V1 | Dependent on C-CDA implementation; no explicit mention |
| Orders / referrals | ❌ Not covered | No dedicated order or referral export | Product has CPOE (meds/labs/imaging); order data not explicitly exported beyond C-CDA |
| Insurance / coverage | ⚠️ Partial | "Patient Demographics and Insurance" CSV includes primary/secondary insurance | Some coverage but depth unknown; eligibility check results not mentioned |
| Claims / billing | ⚠️ Partial | "Claims" CSV file mentioned | Present but zero field documentation; depth completely unknown |
| Payments | ⚠️ Partial | "Insurance Payment Details" and "Patient Payment Details" CSV files | Present but zero field documentation; depth completely unknown |
| Consents / directives | ❌ Not covered | No mention of consent or advance directive export | Product collects consent forms at intake; gap if stored digitally |
| Patient communications / portal messages | ❌ Not covered | No mention of secure messages, appointment requests, or portal communications | Product has patient portal with secure messaging; significant gap |
| Specialty-specific data | ❌ Not covered | No mention of specialty templates or custom form data export | Product supports 25+ specialties with custom templates; data from these not addressed |

## 6. Documentation Quality

The documentation quality is **very poor**:

- **Total documentation**: 2 pages describing export components at a high level
- **Data dictionary**: None. Zero field-level definitions for any export component
- **Field names**: Not documented for any CSV file
- **Types**: Not documented
- **Descriptions**: Not documented
- **Relationships**: Not documented
- **Value sets**: Not documented
- **Sample data**: None provided
- **Machine-readable schemas**: None provided

A developer receiving this documentation would know:
- The export comes as a ZIP file
- Clinical data is in C-CDA R2.1 format
- There are CSV files for billing, demographics, and appointments
- Documents come in native format

A developer would **not** know:
- What columns are in any CSV file
- What C-CDA sections are actually populated
- How to parse or import any component beyond generic C-CDA handling
- What billing fields are captured
- How entities relate to each other
- What codes or value sets are used

The documentation is essentially a marketing-level description of the export, not a technical specification. It would be insufficient to build an import or migration tool.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Partial**

The export goes beyond a pure C-CDA repackage by including separate CSV files for billing data (claims, insurance payments, patient payments) and native document files. This is meaningful — many vendors provide only C-CDA and call it (b)(10). However, significant gaps remain relative to what the product stores:
- Patient portal communications/secure messages are absent
- Specialty-specific template data is unaddressed
- Order history beyond C-CDA is not exported
- Consent forms (as structured data) are not mentioned
- Custom intake forms and health questionnaires are not mentioned
- Only future appointments are exported (not historical scheduling data)

The complete absence of field-level documentation makes it impossible to fully assess depth within covered domains. The billing CSV files *could* be comprehensive or could be minimal — we simply cannot tell.

**Axis 2 — Export approach: Purpose-built EHI export**

Despite the thin documentation, this is a purpose-built export rather than a repackaged existing exchange. Evidence:
1. The export combines multiple formats (C-CDA + CSV + native documents) into a single ZIP, which is not how any standard clinical exchange works
2. Billing data (claims, insurance payments, patient payments) is explicitly separated into dedicated CSV files — this data is not in C-CDA or FHIR (g)(10)
3. Demographics/insurance has its own CSV beyond what C-CDA provides
4. The document export includes non-clinical documents (faxes, scanned documents, forms)
5. The costs disclosure confirms FHIR API is a separate paid subscription, reinforcing that this export is distinct from (g)(10)
6. There is a dedicated admin-accessible export module with population export capability

The vendor clearly built something for (b)(10) rather than pointing to an existing export. The effort, however, was minimal in terms of documentation.

### Key Findings

1. **Purpose-built but poorly documented**: Nexus built a dedicated EHI export module that goes beyond C-CDA by adding billing CSVs and native documents, but provided only a 2-page high-level description with zero field-level documentation.

2. **Billing data is explicitly included**: The export includes 3 dedicated CSV files for claims, insurance payments, and patient payments — a meaningful signal that the vendor engaged with (b)(10) beyond clinical exchange. However, without field definitions, we cannot assess whether these CSVs are comprehensive or minimal.

3. **Clinical data limited to C-CDA R2.1 / USCDI V1**: The clinical component uses standard C-CDA without any documented vendor extensions. This means clinical data depth is limited to the USCDI V1 floor (the older standard, not even USCDI V3). Internal EHR data elements beyond what C-CDA captures are likely lost.

4. **Multiple domains absent**: Patient portal communications, specialty-specific template data, custom forms/questionnaires, order details, and consent data are not addressed in the export documentation.

5. **Documentation is insufficient for implementation**: A developer could not build an import tool from this documentation alone. The CSV file structures are completely undocumented, and the C-CDA scope is described only by reference to the generic standard.

### Summary Stats

    Coverage:        Partial
    Approach:        Purpose-built EHI export
    Export format:   Mixed (C-CDA R2.1, CSV, native document files)
    Entities:        7 described components
    Fields:          N/A (no data dictionary)
    Descriptions:    N/A (0% — no field-level documentation)
    Sample data:     No
    Bulk export:     Yes (population export supported)
    Domains covered: ~8 of 18 applicable domains (most only partially)

### Bottom Line

Nexus EHR's (b)(10) export is a genuine purpose-built effort that goes beyond repackaged C-CDA by including billing CSVs and native documents, but the near-total absence of documentation (2 pages, zero field definitions) makes it impossible to verify actual completeness. The biggest gap is documentation quality: even if the export contains comprehensive data, no one outside Nexus could assess or use it without reverse-engineering the CSV files and C-CDA output.
