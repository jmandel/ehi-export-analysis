# EHI Export Analysis: Nexus Clinical LLC

**Product**: Nexus EHR V 7.3
**Analysis date**: 2026-02-15
**CHPL ID**: 15.04.04.2989.Nexu.07.03.1.221227

## 1. Product Context

Nexus EHR is a cloud-based, unified ambulatory EHR platform made by Nexus Clinical LLC (Delray Beach, FL, ~10-19 employees). It is a single product combining EHR, practice management, medical billing, patient portal, telehealth, and eFax. It targets small to midsize ambulatory practices (solo to 50+ physicians) across 25+ specialties including cardiology, psychiatry, orthopedics, neurology, pain management, and behavioral health.

Key data domains the product stores (relevant for export completeness assessment):
- **Clinical**: Chief complaint, HPI, medical/surgical/family/social history, ROS, physical exam, assessment/plan, problem lists, medication lists, allergy lists, immunizations, vital signs, lab results (via eLab interfaces), diagnostic imaging (DICOM/PACS), implantable devices, clinical notes.
- **Orders**: Medication orders (CPOE), laboratory orders (CPOE), imaging orders (CPOE), e-prescriptions including controlled substances (EPCS via NewCrop).
- **Documents**: Chart notes, scanned documents, eFax, consent forms, intake forms, letters, custom form templates, patient education materials.
- **Financial/Administrative**: Superbill/encounter charges, claims, fee schedules, insurance eligibility records, payment records, account statements.
- **Patient-generated**: Portal-submitted demographics updates, health questionnaire responses, secure messages, appointment requests, post-visit surveys, online payments.
- **Specialty-specific**: Custom templates for 25+ specialties, though vendor materials don't detail what specialty-specific data fields exist.

The product is certified for 34 ONC criteria including (b)(10) EHI export, (g)(10) FHIR APIs, CPOE for meds/labs/imaging, e-prescribing, transitions of care, patient portal, and public health reporting. The FHIR API is a separate paid add-on module, confirming the (b)(10) export is a distinct mechanism.

## 2. Artifacts Reviewed

| # | Artifact | Type | Size | Description | Informativeness |
|---|----------|------|------|-------------|-----------------|
| 1 | `EHI-Export-Documentation.pdf` | PDF | 774 KB, 2 pages | Primary EHI export documentation for 170.315(b)(10). Describes export format and categories. Created 2023-11-30 by "Francis Carlo Hofilena" in Microsoft Word 2010. | **Primary** — only artifact describing the export. Contains category-level description of 5 export components but no field-level detail. |
| 2 | `Nexus_EHR_Costs_And_Considerations.pdf` | PDF | 178 KB, 2 pages | ONC-required costs and considerations disclosure. Lists pricing for certified functionality and add-on modules. | **Secondary** — confirms FHIR API is separate paid module; EHI export cost not separately listed (appears included in base product). |
| 3 | `costs-and-limitations-page-full.png` | PNG | 515 KB | Screenshot of the vendor's costs-and-limitations web page. | **Low** — visual record only; no content beyond what's in the PDFs. |

**No data dictionary, schema, sample data, or machine-readable artifacts were found.** The entire EHI export documentation consists of one 2-page PDF.

## 3. Export Mechanics

- **Format**: ZIP file containing a mix of C-CDA R2.1 XML (clinical data), CSV files (billing, demographics, appointments), and raw document files (PDF, DOC, HTML, JPG, etc.)
- **Mechanism**: UI-driven. Admin users access an "export module" within Nexus EHR. No API-based export mechanism documented.
- **Single-patient**: Yes — "Individual Patient Export" described.
- **Bulk/population**: Yes — "Population Data Export" described. For population export, Nexus recommends contacting support (support@nexusclinical.com) to monitor the process for large datasets. Document content is replaced by a document index CSV; a separate "document export utility program" provided by Nexus exports actual documents offline based on the index.
- **Timing**: "May require time from few seconds to several hours based on size of data."
- **Access constraints**: Admin users only. No fees explicitly listed for the export; appears included in base subscription.
- **FHIR API**: Separately sold module (one-time setup + annual subscription); not part of the (b)(10) export.

## 4. Export Content: What's In It

The export documentation describes **5 categories** of data, with no field-level detail for any of them. There is no data dictionary, no column headers listed, no data types, no sample data.

### Vendor's own content organization

The vendor organizes the export into these 5 components (identical language for both individual and population export, except for document handling):

| # | Export Component | Format | Fields Documented | Column Headers Listed | Description |
|---|-----------------|--------|-------------------|-----------------------|-------------|
| 1 | Clinical Data | C-CDA R2.1 | 0 (defers to standard) | N/A | "Clinical Data is exported in C-CDA R2.1 format. Exported C-CDA complies with USCDI V1." No Nexus-specific extensions or constraints documented. |
| 2 | Patient Billing Information | CSV (3 files) | 0 | No | Three separate CSV files: Claims, Insurance payment details, Patient payment details. No column names, types, or values specified. |
| 3 | Patient Documents | Original format | 0 | N/A | Documents exported as-is (PDF, DOC, HTML, JPG). Types: Chart Notes, Scanned Documents, Imported Faxes, Software-generated Documents/Forms, PE Images, Other. |
| 4 | Future Appointments | CSV | 0 | No | "Appointments scheduled for future dates." No fields specified. |
| 5 | Patient Demographics and Insurance | CSV | 0 | No | "Contact details, address, and emergency contact" and "Primary, Secondary Insurance and Responsible Party." No column headers specified. |

**Total documented fields: 0.** The documentation provides category labels only — not a single field name, data type, column header, value set, or relationship is specified for any CSV file.

For the C-CDA component, the vendor defers entirely to the standard ("complies with USCDI V1") without specifying which C-CDA templates or sections are populated, what vendor-specific extensions exist, or what clinical data elements are actually included vs. excluded.

### Population export differences

The only documented difference for population export is that Component 3 (Patient Documents) becomes a "Patient Documents Index" CSV containing: document ID, patient identification details, document classification, name, and created date. Actual document files are exported offline via a separate Nexus-provided utility program.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor describes five export categories, but provides no field-level detail for any of them:

1. **Clinical Data (C-CDA R2.1 / USCDI V1)**: This is the richest component by scope, but only because it defers to the C-CDA R2.1 standard. USCDI V1 includes demographics, problems, medications, allergies, immunizations, lab results (values/tests), vital signs, clinical notes, health concerns, goals, assessment/plan, referral note, and care team members. However, the vendor provides no confirmation of which C-CDA sections are actually populated, and USCDI V1 is a subset of what a 25+ specialty EHR stores.

2. **Patient Billing (3 CSV files)**: Positive that billing data is included (claims, insurance payments, patient payments). This goes beyond a typical C-CDA/FHIR-only export. However, zero field-level documentation makes it impossible to assess depth or completeness. We cannot verify whether these include line items, diagnosis codes, procedure codes, modifiers, payer IDs, ERA details, or just summary amounts.

3. **Patient Documents**: Exporting raw document files (chart notes, scanned docs, faxes, generated forms, images) in original format is a good practice. However, there's no metadata or indexing specified for individual export — just loose files.

4. **Future Appointments**: Only future appointments; no historical appointment or encounter data explicitly mentioned beyond what appears in C-CDA.

5. **Demographics and Insurance**: Basic contact/address/emergency contact and insurance info. No detail on how many fields or what specific data points are included.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | CSV file described as "Contact details, address, and emergency contact" — no field list | Product stores detailed demographics (per (a)(5) certification). CSV likely covers basics, but 0 fields documented so completeness unverifiable. |
| Encounters / visits | ⚠️ Partial | C-CDA may include encounter sections; chart notes exported as PDFs | No dedicated encounter data export. C-CDA encounter headers likely minimal. |
| Problems / conditions | ⚠️ Partial | Likely in C-CDA (USCDI V1 scope) | No explicit confirmation. Product is certified for problem lists; probably in C-CDA but undocumented. |
| Medications / prescriptions | ⚠️ Partial | Likely in C-CDA (USCDI V1 scope) | Medication lists probably in C-CDA, but prescribing details (CPOE orders, EPCS data, NewCrop records, PDMP queries) not mentioned. |
| Allergies | ⚠️ Partial | Likely in C-CDA (USCDI V1 scope) | Probably present but undocumented. |
| Immunizations | ⚠️ Partial | Likely in C-CDA (USCDI V1 scope) | Probably present (certified for immunization registry reporting) but undocumented. |
| Vitals | ⚠️ Partial | Likely in C-CDA (USCDI V1 scope) | Probably present but undocumented. |
| Lab results | ⚠️ Partial | Likely in C-CDA (USCDI V1 scope) | Product has eLab interfaces; results probably in C-CDA but no detail on discrete values vs. narrative. |
| Imaging / diagnostic reports | ⚠️ Partial | PE Images exported as files; DICOM/PACS integration exists | Product integrates DICOM/PACS; image files exported, but imaging orders and structured radiology reports not mentioned. |
| Procedures | ⚠️ Partial | Likely in C-CDA (USCDI V1 scope) | Probably present in C-CDA procedures section but undocumented. |
| Clinical notes / documents | ✅ Covered | Chart notes exported as PDFs; C-CDA may include note text; scanned docs and faxes exported | Good coverage via raw document export. Both structured (C-CDA) and unstructured (PDF) notes appear covered. |
| Care plans / goals | ⚠️ Partial | USCDI V1 includes goals and health concerns | Possibly in C-CDA; vendor does not explicitly mention care plans as a product feature. |
| Orders / referrals | ❌ Not covered | No mention in export documentation | Product has CPOE for meds/labs/imaging (certified (a)(1)-(a)(3)); order data not exported. |
| Insurance / coverage | ⚠️ Partial | Demographics CSV includes "Primary, Secondary Insurance and Responsible Party" | Insurance info exported but field-level detail unknown. |
| Claims / billing | ⚠️ Partial | 3 CSV files: Claims, Insurance payments, Patient payments | Positive that billing data is explicitly included. However, 0 fields documented — impossible to assess depth (line items? codes? modifiers? payer details?). |
| Payments | ⚠️ Partial | CSV files for insurance and patient payments | Included but undocumented at field level. |
| Consents / directives | ❌ Not covered | No mention; some consent forms may be in document export | Product has digital intake including consent; no dedicated consent data export. Consent PDFs may be in document export. |
| Patient communications / portal messages | ❌ Not covered | No mention in export documentation | Product has secure messaging, portal messages, appointment requests — none mentioned in export. |
| Specialty-specific data | ❌ Not covered | No mention; C-CDA USCDI V1 does not cover specialty data | Product supports 25+ specialties with custom templates. Specialty-specific clinical data (behavioral health assessments, cardiology data, orthopedic records, etc.) unlikely to be captured in standard C-CDA. Significant gap. |

**Summary**: Of 18 applicable domains, 1 is clearly covered, 12 are partially covered (mostly by assumption that C-CDA includes them — unverifiable from documentation), 4 are not covered, and 1 is borderline (care plans). The "partial" ratings are generous; without any field-level documentation, even the "covered" domains cannot be verified for completeness.

## 6. Documentation Quality

**Rating: Very poor.**

- **Data dictionary**: None. Not a single field name, column header, or data type is documented for any of the 5+ CSV files in the export.
- **C-CDA specification**: Defers entirely to "C-CDA R2.1 compliant with USCDI V1" with no vendor-specific detail. No template OIDs, no extension documentation, no section inventory.
- **Machine-readable artifacts**: None. No JSON schema, no XSD, no CSV templates, no sample data files.
- **Sample data**: None provided.
- **Import feasibility**: A developer receiving this export could process the C-CDA using standard C-CDA parsing libraries, and could open the raw document files. However, the CSV files would require reverse-engineering — no column headers, data types, encoding, delimiters, date formats, or relationship keys are documented. The CSVs cannot be programmatically consumed from this documentation alone.
- **Relationships**: No documentation of how data links across files (e.g., how a claim CSV row relates to a patient or encounter).
- **Completeness of documentation**: The entire documentation is 2 pages of prose with no tables, no code, no examples. It reads as a compliance checkbox rather than technical documentation.

The document was created 2023-11-30 (11 months after certification 2022-12-27) and has not been updated since. The page hosting it was last modified 2025-04-01 per website metadata, but the PDF itself remains the original version.

## 7. Overall Assessment

### Classification

**Partial native export** — The export goes beyond a pure C-CDA/FHIR projection by including billing CSVs, raw documents, demographics/insurance CSVs, and appointment data alongside C-CDA clinical data. This hybrid approach (C-CDA + native CSVs + raw files) attempts to cover more than the standard clinical summary. However, documentation is so thin (zero fields documented) that completeness cannot be verified, and several data domains the product stores (orders, patient portal data, specialty clinical data, secure messages) are not mentioned in the export at all.

### Key Findings

1. **No data dictionary exists**: Zero field names, column headers, data types, or value sets are documented for any export component. This is the single most critical deficiency — the export format is unknowable from the documentation alone. (`EHI-Export-Documentation.pdf`, both pages)

2. **Billing data inclusion is a positive signal**: The export explicitly includes claims, insurance payments, and patient payments as separate CSV files, going beyond vendors who only export C-CDA or FHIR clinical summaries. However, without field-level documentation, the depth of this billing data is unverifiable. (`EHI-Export-Documentation.pdf`, "Patient Billing Information" section)

3. **Clinical data relies entirely on C-CDA R2.1/USCDI V1**: The clinical portion is a standard projection, not a native data model export. USCDI V1 is a narrow subset that likely misses specialty-specific clinical data for the 25+ specialties this product supports (e.g., behavioral health assessments, cardiology-specific data, orthopedic protocols). (`EHI-Export-Documentation.pdf`, "Clinical Data" section)

4. **Patient-generated data and portal content are absent**: The product has a patient portal with secure messaging, questionnaire responses, appointment requests, demographics updates, and post-visit surveys. None of these appear in the export documentation. This is a genuine gap for data that is used to make decisions about patients.

5. **Orders/prescriptions are not explicitly exported**: Despite CPOE certification for medications, labs, and imaging ((a)(1)-(a)(3)), and EPCS capability, the export does not mention order-level data. Medication lists may appear in C-CDA, but prescribing workflow data and order details are likely missing.

### Summary Stats

    Classification:  Partial native export
    Export format:   Mixed (C-CDA R2.1 XML + CSV + raw document files, in ZIP)
    Model type:      Hybrid (standard projection for clinical data + native CSV for billing/admin)
    Entities:        5 export categories (not database entities; no data dictionary)
    Fields:          N/A (0 fields documented)
    Descriptions:    N/A
    Sample data:     No
    Bulk export:     Yes (population export supported)
    Domains covered: 1 of 18 clearly; 12 partially (unverifiable); 4 not covered

### Bottom Line

Nexus EHR's EHI export attempts to go beyond a pure C-CDA clinical summary by including billing CSVs and raw documents, which is architecturally sound. However, the complete absence of any data dictionary or field-level documentation — zero fields documented across the entire export — makes it impossible to verify what is actually exported or to programmatically consume the data. The biggest gap is the combination of zero documentation plus missing data domains (orders, patient portal data, specialty clinical content), leaving patients and providers unable to confirm they have received a complete copy of their health information.
