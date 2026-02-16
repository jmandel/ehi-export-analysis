# EHI Export Analysis: Office Ally, LLC

**Product**: EHR 24/7  
**Analysis date**: 2026-02-16  
**CHPL ID**: 15.04.04.2822.EHR2.05.03.1.241226 (internal ID 11572)

## 1. Product Context

EHR 24/7 is a cloud-based ambulatory EHR priced at $44.95/month per provider, targeting small to mid-size practices across all medical specialties. It is part of Office Ally's broader ecosystem that includes Practice Mate (free practice management), Service Center (claims clearinghouse processing $250B+ annually), Patient Ally (patient portal), and add-ons for e-prescribing, telehealth, and patient reminders.

The product stores:

- **Clinical data**: Patient demographics, SOAP notes with customizable templates, vitals, blood sugar logs, allergies, problem lists, medication lists, immunizations, lab orders/results (via LIS integration), radiology orders, referrals, family health history (certified (a)(12)), implantable devices (certified (a)(14)), clinical documents and images.
- **Administrative data**: Appointment scheduling (integrated with Practice Mate), patient intake forms (Intake Pro add-on).
- **Billing/financial data** (via Practice Mate integration): Superbills with custom code capture, patient billing (copays, balances, payments), patient ledger, insurance eligibility (270/271), claims submission to 5,000+ payers, claims status tracking, ERAs.
- **Communications**: Patient portal messages, provider-to-provider Direct messages, medication refill requests.
- **Prescribing**: E-prescribing via OA-Rx, EPCS for controlled substances.

The tight integration between EHR 24/7 and Practice Mate means the designated record set likely spans both systems. The export should cover clinical charting, billing/claims, appointments, communications, and specialty clinical data.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/EHI_Export_Documentation.pdf` | 1-page PDF (97 KB), version 1.0.1, dated 2024-02-08. Lists four export components (C-CDA, Appointments CSV, Claims CSV, Attachments) with no field-level detail. Author: Mark Vomocil. | **Primary artifact** — but extremely thin. Contains the entirety of the vendor's EHI export documentation. |
| `downloads/certification-page-full.png` | Full-page screenshot of the ONC ACB certification page at `cms.officeally.com/resources/onc-acb-certification`. Confirms the single PDF link under "Electronic Health Information Export." | Confirms no additional documentation artifacts exist on the certification page. |
| `files.json` | Manifest of downloaded files with source URLs and descriptions. | Confirms only two files were available. |
| `metadata.json` | CHPL certification details, developer contact info. | Confirms (b)(10) certification and product version (5.9.255 — newer than the 5.6.81 referenced in the PDF). |
| `product-research.md` | Detailed product research establishing what EHR 24/7 stores and does. | Essential for gap analysis — sets the baseline of expected export coverage. |

## 3. Export Mechanics

- **Format**: Mixed — C-CDA XML for clinical data, CSV for appointments and claims, original format for attachments.
- **Mechanism**: Not documented. The PDF does not describe how a user triggers the export, where in the UI it is located, or what parameters are available.
- **Single-patient vs bulk**: The PDF states the export supports "a single patient as well as for a patient population."
- **Access constraints/fees**: Not documented.

## 4. Export Content: What's In It

The export documentation describes four components with no field-level detail for any of them:

### 4.1 C-CDA (Clinical)

HL7 C-CDA XML files complying with USCDI Version 1. The documentation provides no vendor-specific mapping — it references the external HL7 C-CDA R2 specification. USCDI v1 is notably behind current standards (USCDI v3 is mandatory as of January 2026). C-CDA would cover: demographics, allergies, medications, problems, procedures, vital signs, immunizations, lab results, clinical notes, care plans — but only to the depth and breadth defined by the standard templates.

No information is provided about:
- Which C-CDA document types are generated (CCD, Discharge Summary, Referral, etc.)
- Whether vendor-specific extensions or custom sections are included
- How SOAP notes or clinical templates map to C-CDA sections
- Coverage of family health history, implantable devices, or other certified (a)-criteria data

### 4.2 Appointments (CSV)

Described only as "a comprehensive view of appointment details." No column headers, field names, data types, value sets, or sample rows are provided.

### 4.3 Claims (CSV)

Described only as "a comprehensive view of claim details." No column headers, field names, data types, value sets, or sample rows are provided.

### 4.4 Attachments

Scanned or uploaded documents exported in their original upload format. No metadata schema or index file is documented.

### Vendor's own content organization

| Entity/Table | Fields | Described | Types | Category (vendor's) |
|---|---|---|---|---|
| CCDA | 0 (defers to HL7 spec) | N/A | N/A | Clinical |
| Appointments | 0 (undocumented) | N/A | N/A | Administrative |
| Claims | 0 (undocumented) | N/A | N/A | Billing |
| Attachments | 0 (undocumented) | N/A | N/A | Documents |

**Total entities: 4. Total documented fields: 0.** There is no data dictionary of any kind. The full inventory is saved to `analysis/entity-inventory-full.json`.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor describes four export streams spanning three broad categories:

1. **Clinical (C-CDA)**: Delegates entirely to the HL7 C-CDA / USCDI v1 standard. This would include demographics, allergies, medications, problems, procedures, vitals, immunizations, labs, and clinical notes — but only those elements defined in standard C-CDA templates. No vendor-specific depth is documented. The USCDI v1 reference means the export may not include elements added in USCDI v2 and v3 (e.g., health insurance information, SDOH data, clinical tests beyond labs).

2. **Administrative (Appointments CSV)**: Appointment details in CSV. Could be thin (date, time, provider) or comprehensive (status, type, reason, insurance, notes) — impossible to assess without field documentation.

3. **Billing (Claims CSV)**: Claim details in CSV. Could range from minimal (claim ID, date, amount) to comprehensive (CPT/ICD codes, modifiers, line items, payer responses, adjustments) — impossible to assess without field documentation.

4. **Documents (Attachments)**: Scanned/uploaded documents. Potentially valuable for completeness but with no metadata index, difficult to use programmatically.

The Appointments and Claims CSV exports represent a genuine attempt to go beyond C-CDA/USCDI clinical data. However, the complete absence of field documentation makes it impossible to verify their actual coverage.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | C-CDA includes standard demographics | C-CDA covers basic demographics; unclear if all stored fields (custom demographics, detailed contact info) are included |
| Encounters / visits | ⚠️ Partial | C-CDA Encounters section; Appointments CSV | C-CDA has encounter data; Appointments CSV may add scheduling context. Depth unknown |
| Problems / conditions | ⚠️ Partial | C-CDA Problem List section | Standard C-CDA coverage; vendor-specific problem list fields (if any) unknown |
| Medications / prescriptions | ⚠️ Partial | C-CDA Medications section | C-CDA covers medication list. E-prescribing history (OA-Rx, EPCS records) likely not captured in C-CDA |
| Allergies | ⚠️ Partial | C-CDA Allergies section | Standard C-CDA coverage |
| Immunizations | ⚠️ Partial | C-CDA Immunizations section | Standard C-CDA coverage |
| Vitals | ⚠️ Partial | C-CDA Vital Signs section | Standard vitals covered; blood sugar logs (product feature) may not map to standard C-CDA |
| Lab results | ⚠️ Partial | C-CDA Results section | Standard lab results; may not include all LIS integration data |
| Imaging / diagnostic reports | ⚠️ Partial | C-CDA may include some; Attachments | Radiology orders/results coverage unclear |
| Procedures | ⚠️ Partial | C-CDA Procedures section | Standard C-CDA coverage |
| Clinical notes / documents | ⚠️ Partial | C-CDA clinical notes; Attachments | SOAP notes may be in C-CDA or Attachments. Customizable template content unclear |
| Care plans / goals | ⚠️ Partial | C-CDA may include Plan of Treatment | Standard C-CDA coverage |
| Orders / referrals | ❌ Not covered | Not mentioned | Product supports lab orders, radiology orders, and referrals; no dedicated export stream |
| Insurance / coverage | ❌ Not covered | Not mentioned | Product stores insurance eligibility (270/271) data; not in any documented export component |
| Claims / billing | ⚠️ Partial | Claims CSV | Claims CSV exists but has zero documented fields; impossible to assess depth |
| Payments | ❌ Not covered | Not mentioned | Product stores patient payments, copays, ledger entries via Practice Mate; not in documented export |
| Consents / directives | ❌ Not covered | Not mentioned | Not clearly a product feature; N/A or minor gap |
| Patient communications | ❌ Not covered | Not mentioned | Product has Patient Ally portal messages, Updox messaging, Direct messaging; none exported |
| Family health history | ❌ Not covered | Not mentioned | Product is certified for (a)(12) family health history; not mentioned in export |
| Implantable devices | ❌ Not covered | Not mentioned | Product is certified for (a)(14) implantable device list; not mentioned in export |
| Superbills / charge capture | ❌ Not covered | Not mentioned | Product has configurable superbills; not in documented export |
| Patient intake forms | ❌ Not covered | Not mentioned | Product has Intake Pro digital intake; not in documented export |

## 6. Documentation Quality

The documentation quality is **extremely poor** — among the most minimal possible for a certified product:

- **No data dictionary**: Zero field names, zero data types, zero descriptions for any export component.
- **No schema or machine-readable artifacts**: No JSON schema, no CSV headers, no C-CDA template constraints.
- **No sample data**: No example exports, no worked examples.
- **No export instructions**: A user reading this document would not know how to trigger the export or where to find it in the UI.
- **No relationship documentation**: No description of how the four export components relate to each other or link patient records.
- **Version mismatch**: PDF references product version 5.6.81; current certified version is 5.9.255, suggesting the documentation has not been updated in ~2 years.
- **Standard reference is outdated**: References USCDI v1, not the current USCDI v3 required as of January 2026.

A developer could not build an import from this documentation. The C-CDA component is interpretable only because C-CDA is a well-defined standard — but even there, the vendor provides no guidance on which templates or sections are populated. The CSV files are completely opaque without column documentation.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Partial**

The export attempts to go beyond pure clinical summaries by including Appointments CSV, Claims CSV, and Attachments alongside C-CDA — these represent data domains (scheduling, billing, documents) that are not part of USCDI/C-CDA clinical exchange. This is a meaningful signal that the vendor recognized (b)(10) requires more than clinical data. However, multiple data domains the product stores are entirely absent from the export documentation: insurance/coverage details, patient payments and ledger entries, superbills, patient portal communications, e-prescribing history, referral workflows, patient intake forms, family health history, and implantable devices. The complete absence of field-level documentation for the CSV components makes it impossible to confirm even the claimed coverage is substantive. The classification is "Partial" rather than "Minimal" because the four-component structure shows deliberate (b)(10) design, but the gaps and documentation void prevent a "Comprehensive" rating.

**Axis 2 — Export approach: Purpose-built EHI export**

Despite the thin documentation, this is clearly a purpose-built export rather than a repackaged (g)(10). The vendor built dedicated CSV exports for Appointments and Claims alongside C-CDA, and includes Attachments — none of these would exist in a standard (g)(10) FHIR API or C-CDA clinical exchange. The four-component architecture was designed specifically for (b)(10). The documentation explicitly names (b)(10) and describes an export mechanism distinct from their FHIR API or transitions-of-care C-CDA. However, the C-CDA component itself appears to be their standard clinical exchange output (USCDI v1), so that portion is effectively repackaged — only the CSV and Attachments components are purpose-built additions.

### Key Findings

1. **Entire EHI export documentation is a single 1-page PDF with four bullet points and zero field definitions.** This is one of the thinnest EHI export documentations observed — no data dictionary, no schema, no sample data, no export instructions. (`downloads/EHI_Export_Documentation.pdf`, 97 KB, 1 page)

2. **The export has a reasonable four-component structure** (C-CDA + Appointments CSV + Claims CSV + Attachments) that goes beyond clinical-only export, indicating the vendor engaged with the (b)(10) requirement rather than simply repackaging their (g)(10) API.

3. **Zero documented fields across all export components.** The CSV components ("Appointments" and "Claims") have no column headers, field names, types, or sample data documented. The C-CDA component defers entirely to the external HL7 specification with no vendor-specific mapping. This makes the export practically unusable without trial-and-error.

4. **Multiple data domains are missing from the export**: patient payments/ledger, insurance/eligibility details, superbills, patient communications, e-prescribing records, referral orders, intake forms, family health history, and implantable device records — all of which the product stores per its certification and feature set.

5. **Documentation is outdated**: References product version 5.6.81 (current is 5.9.255) and USCDI v1 (current requirement is USCDI v3 as of January 2026). Last updated February 2024.

### Summary Stats

```
Coverage:        Partial
Approach:        Purpose-built EHI export
Export format:   C-CDA XML + CSV + original format (attachments)
Entities:        4
Fields:          0 (no data dictionary)
Descriptions:    N/A
Sample data:     No
Bulk export:     Yes (documentation claims single-patient and population)
Domains covered: 2–3 of 15+ applicable domains confirmed; others possible but undocumented
```

### Bottom Line

EHR 24/7's EHI export has the right structural idea — combining C-CDA clinical data with CSV exports for appointments and claims, plus document attachments — but the documentation is so thin (one page, zero field definitions) that it's impossible to verify the actual completeness of any component. A patient or provider receiving this export would get clinical summaries via C-CDA and some billing/scheduling data in undocumented CSV files, but would likely be missing patient payments, portal communications, e-prescribing history, intake forms, and other data the product stores. The single biggest gap is the complete absence of field-level documentation, which renders the CSV exports opaque and makes the entire export difficult to use.
