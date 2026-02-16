# EHI Export Analysis: Office Ally, LLC

**Product**: EHR 24/7
**Analysis date**: 2026-02-15
**CHPL ID**: 15.04.04.2822.EHR2.05.03.1.241226 (internal ID 11572)

## 1. Product Context

EHR 24/7 is a cloud-based ambulatory EHR serving 20,000+ users at small to mid-size practices across all specialties. At $44.95/month per provider, it is one of the lowest-cost certified EHRs on the market. It is part of a tightly integrated Office Ally ecosystem that includes Practice Mate (free practice management/billing), Service Center (claims clearinghouse processing $250B+ annually), Patient Ally (patient portal), and OA-Rx (e-prescribing).

**Data the product stores** (relevant to export completeness):
- **Clinical**: demographics, medical/family/social history, SOAP notes, vitals, allergies, medications, immunizations, lab orders/results, radiology orders, referrals, diagnoses/problem lists, procedures, clinical documents/images, implantable device list, family health history
- **Billing/Administrative** (via Practice Mate integration): appointment schedules, insurance eligibility, claims (submissions/statuses/remittances), superbills, patient billing records (invoices, copays, balances, payments, ledger)
- **Communication**: patient-provider portal messages, secure Direct messages, patient intake forms, appointment requests, medication refill requests
- **Prescribing**: e-prescribing history, EPCS records

The boundary between EHR 24/7 and Practice Mate is blurred — they share patient records and workflows. For (b)(10) purposes, the export scope should include data from both systems since they constitute "the product of which the Health IT Module is a part."

## 2. Artifacts Reviewed

| # | Artifact | Type | Size | Informativeness | What It Tells Us |
|---|----------|------|------|-----------------|------------------|
| 1 | `EHI_Export_Documentation.pdf` | PDF | 97 KB, 1 page | **Low** | The sole EHI export documentation. Describes 4 export components (C-CDA, Appointments CSV, Claims CSV, Attachments) in four bullet points. No field definitions, no schema, no sample data. |
| 2 | `certification-page-full.png` | Screenshot | 753 KB | **Minimal** | Full-page screenshot of the ONC ACB Certification page confirming the PDF is the only EHI export artifact linked. No additional data dictionaries, schemas, or sample files exist on the page. |

**Most informative**: The PDF, though its information content is extremely limited — four sentences describing four export components.

**Least informative**: The screenshot, which serves only to confirm no additional artifacts exist.

**Total artifact count**: 2 files. This is among the smallest artifact sets possible for an EHI export documentation review.

## 3. Export Mechanics

- **Format(s)**: HL7 C-CDA XML (USCDI v1), CSV (appointments and claims), and original upload format (attachments)
- **Mechanism**: Not documented. The PDF does not describe how a user triggers the export, where the function is located in the UI, or how files are delivered. A user would need to contact Office Ally or consult separate support documentation to learn how to perform an export.
- **Single-patient**: Yes (stated in PDF)
- **Bulk/population**: Yes (stated in PDF: "for a single patient as well as for a patient population")
- **Access constraints or fees**: Not documented in the EHI export documentation. A separate "Cost and Considerations" document exists on the certification page but is a general pricing disclosure, not specific to EHI export.
- **Version note**: The PDF references product version 5.6.81, while the current certified version is 5.9.255 (certified 2024-12-26). The documentation has not been updated since February 2024.

## 4. Export Content: What's In It

The export documentation describes four components. There is **no data dictionary** — no table names, no field names, no data types, no value sets, no foreign keys, no relationships, no schemas, and no sample data for any component.

### Vendor's own content organization

The vendor organizes the export into four named components. This is the complete extent of what the vendor documents:

| Component | Format | Description (vendor's words) | Fields Documented | Types Documented | Schema Provided | Sample Data |
|-----------|--------|------------------------------|-------------------|------------------|-----------------|-------------|
| CCDA | HL7 C-CDA XML | "bulk export of HL7 CCDA xml files which comply to USCDI, Version 1" | No | No | No (references external HL7 spec) | No |
| Appointments | CSV | "a comprehensive view of appointment details" | No | No | No | No |
| Claims | CSV | "a comprehensive view of claim details" | No | No | No | No |
| Attachments | Original format | "scanned or uploaded documents in the patient's record" | N/A | N/A | No | No |

**Total vendor-documented fields**: 0. Not a single field name, column header, or data element is specified anywhere in the documentation.

**C-CDA coverage (inferred)**: Since the vendor references USCDI v1 and the HL7 C-CDA standard, we can infer the C-CDA component would contain standard sections: Patient Demographics, Allergies, Medications, Problems, Procedures, Results, Vital Signs, Immunizations, Goals, Health Concerns, Assessment and Plan, Care Team, Clinical Notes, Smoking Status, and Unique Device Identifiers. However, the vendor does not confirm which C-CDA templates are actually populated, whether any vendor extensions exist, or how their internal data maps to C-CDA elements.

**CSV coverage (unknown)**: The Appointments and Claims CSV files have zero documentation beyond their names. We cannot determine what columns they contain, what data types are used, how dates are formatted, whether identifiers are included, or what constitutes a "comprehensive view." A recipient of these files would need to reverse-engineer their structure from column headers in the actual export.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor describes four export streams:

1. **C-CDA (clinical)**: Covers standard clinical summary data per USCDI v1. This is inherently limited to what C-CDA can represent — structured clinical data that fits standard templates. It excludes custom clinical templates, free-text SOAP note details beyond what maps to C-CDA sections, blood sugar logs, and other vendor-specific clinical data structures.

2. **Appointments (CSV)**: Potentially covers scheduling data, but with zero field documentation it's impossible to assess depth. Could range from basic date/time/provider to comprehensive scheduling with visit types, durations, cancellation reasons, and notes.

3. **Claims (CSV)**: Potentially covers payer claims data, but again with zero field documentation. Could range from basic claim IDs and amounts to detailed line-item billing with diagnosis codes, procedure codes, modifiers, and adjudication results. Critically, this likely covers *payer claims* but may not cover *patient-facing billing* (invoices, copays, balances, payments, ledger entries).

4. **Attachments**: Covers scanned/uploaded documents in their original format. This is a reasonable approach for binary content but includes no metadata schema.

The C-CDA component is essentially the same clinical data available through the vendor's (g)(10) FHIR API, repackaged in C-CDA format. The Appointments and Claims CSVs represent the only attempt to go beyond standard clinical summary data — but without documentation, their value is significantly diminished.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | C-CDA Patient Demographics section (USCDI v1) | C-CDA covers standard demographics; product likely stores additional fields (contacts, preferences, custom intake data) not representable in C-CDA |
| Encounters / visits | ⚠️ Partial | C-CDA may include encounter data; Appointments CSV may contain visit records | Appointments CSV is undocumented; C-CDA encounter representation is limited; progress note context may be lost |
| Problems / conditions / diagnoses | ⚠️ Partial | C-CDA Problems section | Standard C-CDA coverage; vendor-specific problem list features or custom fields unknown |
| Medications / prescriptions | ⚠️ Partial | C-CDA Medications section | C-CDA covers medication lists but e-prescribing history, EPCS records, refill requests, pharmacy communications may not be captured |
| Allergies | ⚠️ Partial | C-CDA Allergies section | Standard C-CDA coverage; likely adequate for this domain |
| Immunizations | ⚠️ Partial | C-CDA Immunizations section | Standard C-CDA coverage; likely adequate for this domain |
| Vitals | ⚠️ Partial | C-CDA Vital Signs section | Standard vitals likely covered; blood sugar logs and other non-standard measurements may not map to C-CDA |
| Lab results | ⚠️ Partial | C-CDA Results section | Standard lab results in C-CDA; may lose vendor-specific formatting, ordering context, or LIS integration metadata |
| Imaging / diagnostic reports | ⚠️ Partial | C-CDA may include some; Attachments may include imaging documents | Radiology orders and reports may be partially covered; structured order data likely lost |
| Procedures | ⚠️ Partial | C-CDA Procedures section | Standard C-CDA coverage |
| Clinical notes / documents | ⚠️ Partial | C-CDA Clinical Notes section; Attachments for scanned documents | SOAP notes are a core product feature; C-CDA represents notes but custom templates, nurse notes, and structured note data may not fully serialize to C-CDA |
| Care plans / goals | ⚠️ Partial | C-CDA Goals and Care Plan sections | Standard C-CDA coverage |
| Orders / referrals | ❌ Not covered | No dedicated export component | Product supports lab orders, radiology orders, and referrals; no export path documented beyond what may appear in C-CDA |
| Insurance / coverage | ❌ Not covered | No dedicated export component | Product stores insurance eligibility, benefits, and coverage data via Practice Mate integration; not documented in export |
| Claims / billing | ⚠️ Partial | Claims CSV (undocumented) | Claims CSV exists but is completely undocumented; may cover payer claims but patient-facing billing (invoices, copays, balances, payments, ledger) likely not included |
| Payments | ❌ Not covered | No dedicated export component | Product processes patient payments; no export path documented |
| Consents / directives | ❌ Not covered | No dedicated export component | Product likely stores consent forms; no export path |
| Patient communications / portal messages | ❌ Not covered | No dedicated export component | Patient Ally portal supports messaging, appointment requests, refill requests; none documented in export |

**Summary**: Of 18 standard EHI domains applicable to this product, **0 are fully covered**, **11 have partial coverage** (mostly via C-CDA with its inherent limitations), and **5 have no coverage at all**. The partial ratings for C-CDA domains reflect the fundamental limitation that C-CDA clinical summaries capture a subset of what the product actually stores — they're projections into a standard, not exports of the native data model.

## 6. Documentation Quality

**Can a developer understand and use the export?** No. The documentation consists of four sentences. A developer receiving this export would be able to parse the C-CDA files using standard tooling, but the CSV files would require reverse-engineering from actual column headers. There is no basis for building an import system from this documentation alone.

**What's well-documented?** Almost nothing. The document confirms four export streams exist and names their formats. That is the extent of the documentation.

**What requires guesswork?** Everything beyond the existence of the four components:
- How to trigger the export (not documented)
- What fields are in the CSV files (not documented)
- What C-CDA templates/sections are populated (references external spec only)
- How attachments are organized or identified (not documented)
- How the four components relate to each other (no cross-references or shared identifiers documented)
- What data is excluded from the export (not documented)

**Machine-readable artifacts**: None. No schemas, no sample data, no JSON, no data dictionaries.

**Version alignment**: The documentation (v1.0.1, dated 2024-02-08) references product version 5.6.81, while the currently certified version is 5.9.255 (certified 2024-12-26). The documentation has not been updated in nearly two years.

## 7. Overall Assessment

### Classification

**Minimal/stub**

The export documentation is a single page with four bullet points. While the actual export mechanism may produce useful data (C-CDA files, CSV files, attachments), the documentation provides virtually no technical detail about what is exported, how to interpret it, or how to use it. The C-CDA component is a standard-based projection that covers only clinical summary data. The CSV components (Appointments, Claims) go beyond clinical summaries but are completely undocumented. Significant data domains stored by the product — patient billing, insurance, portal messages, e-prescribing history, custom clinical data — have no documented export path.

### Key Findings

1. **The entire EHI export documentation is a single 1-page PDF with four bullet points and zero field-level detail** (`EHI_Export_Documentation.pdf`, 97 KB, authored 2024-02-08). No data dictionary, schema, sample data, or export instructions exist.

2. **The C-CDA component is a standard clinical summary, not a native data export.** It references USCDI v1 (not v3 or v4) and provides the same data available through the vendor's (g)(10) FHIR API — a clinical summary projection, not the vendor's internal data model.

3. **The Appointments and Claims CSV files are the only non-standard components, but they are completely undocumented** — no column headers, no field definitions, no data types, no sample data. Their actual content cannot be assessed from the documentation.

4. **Major data domains have no export path**: patient billing/payments (beyond payer claims), insurance/coverage, portal messages, e-prescribing history, referral orders, and patient intake forms are not mentioned in the export documentation despite being core features of the product.

5. **The documentation is stale**: it references product version 5.6.81 while the currently certified version is 5.9.255. No updates have been made since January 2024 despite a December 2024 recertification.

### Summary Stats

```
Classification:  Minimal/stub
Export format:   C-CDA XML, CSV, original document format (mixed)
Model type:      Standard projection (C-CDA) + undocumented CSV
Entities:        4 export components (0 with field-level documentation)
Fields:          0 documented
Descriptions:    N/A (no fields documented)
Sample data:     No
Bulk export:     Yes (stated in documentation)
Domains covered: 0 of 18 fully; 11 of 18 partially (via C-CDA); 5 of 18 not covered
```

### Bottom Line

Office Ally's EHI export documentation is a compliance stub — the minimum possible acknowledgment that an export mechanism exists. A patient or provider receiving this export would get C-CDA clinical summaries (standard clinical data only), two undocumented CSV files for appointments and claims, and their uploaded attachments, but would have no way to verify completeness or interpret the CSV data without reverse-engineering it. The single biggest gap is the complete absence of any field-level documentation or data dictionary for any export component, making it impossible to assess whether the export actually captures "all electronic health information" the product stores.
