# EHI Export Analysis: MedConnect, Inc.

**Product**: MedConnectHealth 3.0  
**Analysis date**: 2026-02-16  
**CHPL IDs**: 15.04.04.1889.MedC.03.00.1.171212 (CHPL ID 9183)

## 1. Product Context

MedConnectHealth is a cloud-based integrated EHR and practice management platform developed by MedConnect, Inc. (Montgomery, Alabama). It targets ambulatory physician practices across 25+ specialties, offering a single platform combining clinical documentation, e-prescribing (via DrFirst/Surescripts), lab orders and results (LabCorp, Quest, 30+ labs/hospitals), scheduling, billing/claims management, patient portal, patient kiosk, and telehealth.

The product has meaningful **billing/practice management** capabilities: claims management with clearinghouse transmission (ClaimMD, Change Healthcare, Trizetto, Navicure, Waystar), direct BCBS Alabama connection, ERA/EOB auto-download, payment posting, eligibility checking, revenue reporting, and collection letters. The **patient portal** supports messaging, refill requests, appointment requests, electronic forms (registration, consent, wellness), online bill pay, and electronic statements. The **kiosk** captures scanned IDs and insurance cards.

For a complete (b)(10) export, the expected coverage baseline includes: clinical data (problems, meds, allergies, immunizations, vitals, labs, notes, procedures, orders, care plans), billing/claims data, patient portal communications and form submissions, scheduling, prescribing history, scanned documents, and demographic/insurance details.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/EHI_Export_Documentation.pdf` | 1-page PDF (334 KB, authored by Brett Chapman, created 2023-11-09). The sole export documentation. Restates (b)(10) regulatory requirements and describes the export format: ZIP containing C-CDA XML, demographics PDF, scanned documents, and clinical notes/lab results PDF. No data dictionary, no schema, no sample data. | **Primary source** — contains everything the vendor provides about the export format |
| `downloads/ehi-export-page.html` | HTML source of the registered EHI export page (50 KB). Contains a single link to the PDF and no other substantive content. WordPress site. | Low — just a link to the PDF |
| `downloads/ehi-export-page-screenshot.png` | Browser screenshot of the EHI export page (147 KB). Confirms the page has only a heading and a single PDF link. | Low — visual confirmation only |

**Total artifacts: 3.** The entire documentation corpus is effectively a single 1-page PDF.

## 3. Export Mechanics

- **Format**: ZIP file containing per-patient/clinic folders
- **Components per folder**:
  - C-CDA XML (USCDI v1) — the only computable component
  - Demographics PDF
  - Scanned Documents (PDF, JPG, PNG)
  - Clinical Notes / Lab Results PDF
- **Single-patient export**: User-initiated at any time, restricted to specific users or system administrators
- **Bulk export**: Available "upon request" — MedConnectHealth performs the export on the customer's behalf, not self-service
- **Access constraints**: Bulk export requires vendor involvement; single-patient export is self-service for authorized users
- **Fees**: Not mentioned in the documentation

## 4. Export Content: What's In It

### Data dictionary

**There is no data dictionary.** The documentation provides zero field-level detail. No entities, no tables, no field names, no types, no descriptions, no relationships, no value sets, no sample data. The only content-level information is the list of 4 export components.

### Export components

The export contains exactly 4 component types:

| Component | Format | Computable | Detail Level |
|---|---|---|---|
| C-CDA (USCDI v1) | XML | Yes | Defined by the C-CDA/USCDI v1 standard; no vendor-specific extensions documented |
| Demographics | PDF | No | No field list; just "Demographics" |
| Scanned Documents | PDF, JPG, PNG | No | Original uploaded files |
| Clinical Notes / Lab Results | PDF | No | No field list; just "Clinical Notes/Lab Results" |

**Computable format issues**: 3 of the 4 export components are PDF/image formats. The (b)(10) regulation requires the export to be "electronic and in a computable format." Demographics as PDF and lab results as PDF are notably non-computable — discrete lab values rendered in PDF lose their structured data.

### Vendor's own content organization

The vendor does not organize content into categories or entities. There is no data dictionary to tabulate. The complete "format documentation" is the 4-line list above.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor describes 4 export components with no field-level detail:

1. **C-CDA (USCDI v1)**: A standard clinical summary covering the USCDI v1 data elements — problems, medications, allergies, immunizations, vitals, lab results, procedures, and basic demographics. This is the same C-CDA that would be produced for transitions of care under (b)(1)–(b)(3). No vendor-specific extensions or additional data beyond the standard are documented.

2. **Demographics PDF**: A PDF rendering of patient demographics. Content and fields unknown.

3. **Scanned Documents**: Original scanned files from the patient record.

4. **Clinical Notes / Lab Results PDF**: A PDF rendering of clinical notes and lab results. This means lab results are exported as rendered text, not as discrete computable data.

There is no evidence of any content beyond what the vendor's existing C-CDA transitions-of-care capability already produces, plus PDF printouts and scanned documents.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | Demographics PDF (non-computable); some fields in C-CDA | PDF format loses structure; product stores detailed demographics |
| Encounters / visits | ⚠️ Partial | C-CDA may include encounter sections per USCDI v1 | Only what C-CDA standard includes; no scheduling or visit workflow data |
| Problems / conditions | ⚠️ Partial | C-CDA USCDI v1 problem list | Limited to C-CDA standard fields |
| Medications / prescriptions | ⚠️ Partial | C-CDA USCDI v1 medication list | E-prescribing history, EPCS data, formulary checks not mentioned |
| Allergies | ⚠️ Partial | C-CDA USCDI v1 allergy section | Limited to C-CDA standard fields |
| Immunizations | ⚠️ Partial | C-CDA USCDI v1 immunization section | Limited to C-CDA standard fields |
| Vitals | ⚠️ Partial | C-CDA USCDI v1 vitals section | Limited to C-CDA standard fields |
| Lab results | ⚠️ Partial | C-CDA has some lab data; also "Lab Results PDF" (non-computable) | PDF rendering of labs loses discrete values; significant data fidelity loss |
| Imaging / diagnostic reports | ❌ Not covered | Not mentioned | Product integrates with 30+ labs/hospitals; imaging reports not addressed |
| Procedures | ⚠️ Partial | C-CDA USCDI v1 procedures section | Limited to C-CDA standard fields |
| Clinical notes / documents | ✅ Covered | "Clinical Notes" PDF + scanned documents (PDF/JPG/PNG) | Notes are in PDF (non-computable) but present; scanned docs included |
| Care plans / goals | ⚠️ Partial | C-CDA may include care plan section | Product has care plan management; not specifically mentioned in export |
| Orders / referrals | ❌ Not covered | Not mentioned | Product has integrated lab/diagnostic orders; not in export |
| Insurance / coverage | ❌ Not covered | Not mentioned | Product stores insurance details, eligibility responses; not in export |
| Claims / billing | ❌ Not covered | Not mentioned | Product has full billing module (claims, ERA/EOB, clearinghouses); **major gap** |
| Payments | ❌ Not covered | Not mentioned | Product posts payments, tracks patient balances; not in export |
| Consents / directives | ❌ Not covered | Not mentioned | Patient portal collects electronic consent forms; not in export |
| Patient communications / portal messages | ❌ Not covered | Not mentioned | Portal supports messaging, refill requests, appointment requests; not in export |
| Specialty-specific data | ❌ Not covered | Not mentioned | Product claims 25+ specialty support with configurable templates; not in export |

**Summary**: 0 domains fully covered with computable data. Clinical notes/scanned documents are present but as PDFs. All clinical domains get only USCDI v1 C-CDA coverage. Billing, insurance, payments, portal communications, orders, consents, and specialty data are entirely absent.

## 6. Documentation Quality

The documentation is **extremely thin** — a single page that restates the regulation's requirements and lists 4 export components with no elaboration. Specific deficiencies:

- **No data dictionary**: Zero field-level documentation for any component
- **No schema**: No XML schema, JSON schema, or any machine-readable format specification beyond referencing the C-CDA standard
- **No sample data**: No example exports, no sample files
- **No relationships**: No entity-relationship documentation
- **No value sets**: No coded value specifications beyond the C-CDA standard
- **No API documentation**: No programmatic access method described
- **Non-computable components undocumented**: The PDF components (demographics, clinical notes, lab results) have no description of their layout or contents

A developer attempting to build an import from this documentation would have only the C-CDA standard specification to work from. The PDF components are completely opaque — there is no way to know what fields, layout, or content they contain without obtaining an actual export.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Minimal/stub/unclear**

The export documentation describes only a standard C-CDA (USCDI v1) plus PDF printouts and scanned documents. This covers a thin slice of what MedConnectHealth stores. The product has a full practice management/billing module (claims management across 5+ clearinghouses, ERA/EOB processing, payment posting, eligibility checking, revenue reporting), a patient portal (messaging, refill requests, forms, bill pay), a kiosk (scanned IDs/insurance cards), and specialty-configurable templates for 25+ specialties — none of which appear in the export. The documentation is too thin to definitively confirm or deny the presence of additional data, but nothing in the 1-page PDF suggests anything beyond C-CDA + PDFs.

**Axis 2 — Export approach: Repackaged existing export**

The export is clearly the vendor's existing C-CDA transitions-of-care capability (certified under (b)(1)–(b)(3)) supplemented with PDF printouts and scanned documents. The C-CDA is explicitly described as "in compliance with USCDI v1" with no mention of vendor extensions, additional data mappings, or coverage beyond the standard. The PDF components (demographics, clinical notes, lab results) appear to be print-to-PDF of existing screens. There is no evidence of a purpose-built EHI export: no product-specific data dictionary, no mapping beyond C-CDA standard templates, no billing or operational data, and no vendor-specific schema.

### Key Findings

1. **Entire documentation is 1 page with zero field-level detail.** The export format documentation (`EHI_Export_Documentation.pdf`) is a single page that restates (b)(10) regulatory text and lists 4 export components — no data dictionary, no schema, no sample data, no field descriptions.

2. **3 of 4 export components are non-computable (PDF/image).** Demographics, clinical notes, and lab results are exported as PDFs, which violates the spirit of (b)(10)'s "computable format" requirement. Lab results in PDF format specifically lose discrete data that the product stores.

3. **Billing and practice management data entirely absent.** MedConnectHealth has a full billing module (claims management, clearinghouse transmission, ERA/EOB, payment posting, eligibility) — none of this appears in the export. This is the single largest coverage gap.

4. **Export is a repackaged C-CDA plus PDF printouts.** The only computable component is a standard USCDI v1 C-CDA, which is the same output the vendor already produces for (b)(1)–(b)(3) transitions of care. No vendor-specific extensions or additional data domains documented.

5. **Bulk export requires vendor assistance.** Population-level export is not self-service — users must request it from MedConnectHealth, which limits patient/provider autonomy.

### Summary Stats

```
Coverage:        Minimal/stub/unclear
Approach:        Repackaged existing export
Export format:   C-CDA XML + PDF + images (in ZIP)
Entities:        N/A (no data dictionary)
Fields:          N/A (no field-level documentation)
Descriptions:    N/A
Sample data:     No
Bulk export:     Vendor-assisted only
Domains covered: 0 of 17 applicable domains fully covered (1 partially via non-computable PDF)
```

### Bottom Line

A patient or provider would receive a C-CDA clinical summary (the same data available through standard clinical exchange), PDF printouts of demographics and notes, and scanned documents — but no billing data, no portal communications, no orders, no insurance details, and no specialty-specific clinical data. The documentation is too thin to use as a technical specification, and the prevalence of PDF output undermines the "computable format" requirement. This is a minimal-effort compliance checkbox, not a genuine EHI export.
