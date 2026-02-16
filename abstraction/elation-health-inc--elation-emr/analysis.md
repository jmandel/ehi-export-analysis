# EHI Export Analysis: Elation Health, Inc.

**Product**: Elation EMR (Version 3)
**Analysis date**: 2026-02-16
**CHPL IDs**: 9876 (15.04.04.2717.Elat.03.00.1.181231)

## 1. Product Context

Elation EMR is a cloud-based, all-in-one EHR, billing, and practice management platform purpose-built for ambulatory primary care. It serves 46,000+ clinical users across independent practices, small-to-medium groups (1–10 physicians), and Direct Primary Care (DPC) practices. The product won Best in KLAS 2025–2026 for Small Practice Ambulatory EHR/PM.

Key data domains the product stores that are relevant for EHI completeness assessment:

- **Clinical charting**: Structured templates, visit notes (including AI-generated "Note Assist" notes), problem lists, medication lists, allergy lists, vital signs, growth charts (pediatrics)
- **ePrescribing**: Full prescriptions via Surescripts including EPCS for controlled substances
- **Labs & imaging**: Orders and results from national/regional labs and imaging centers
- **Referrals**: Provider directory, electronic chart sharing, close-the-loop tracking
- **Billing (Elation Billing)**: Real-time eligibility verification, charge capture, claim submission, ERA posting, copay collection, denial management, 100+ billing reports
- **Patient portal (Patient Passport)**: Secure messaging, appointment scheduling, prescription refills, online bill pay, intake forms
- **Telehealth**: Integrated via Zoom, launched from visit notes
- **DPC/membership management**: Recurring membership fees, payment tracking
- **Care management**: Patient registries, outreach campaigns, chronic disease management
- **Communications**: Internal staff messaging, secure patient messaging, Direct messaging, eFax

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `elation-designated-record-set-ehi-export.pdf` | 7-page PDF data dictionary listing 200 data elements with descriptions and export format indicators. Created from Google Sheets, dated 2/6/2024. 87 KB. | **Primary artifact** — the only structured documentation of export contents |
| `ehi-export-criteria-page.html` | Cleaned HTML extraction of the Salesforce Knowledge article describing export mechanics, Confidential Notes policy, and FAQs. 6 KB. | **High** — provides export procedure, access requirements, and regulatory context |
| `ehi-export-criteria-snapshot.txt` | Accessibility tree text snapshot of the rendered help page. 17 KB. | Medium — confirms HTML content, captures text not in simplified HTML (e.g., additional support contact info) |
| `ehi-export-criteria-page.png` | Full-page screenshot of the help article. 840 KB. | Low — visual confirmation only |
| `pdf-pages/page-1.png` through `page-7.png` | Rendered PNG images of each PDF page at 200 DPI. | **High** — used to verify and correct parsing errors in the enrichment JSON |
| `enrichment/data-dictionary.json` | Machine-parsed JSON of the PDF's 199 data elements (prior agent's extraction). 53 KB. | High — but contains 2 errors: missing "Personal Relationship" and "Clinical Orders" entries; includes 1 artifact ("Field"→"Description" header parsed as data) |
| `enrichment/coverage-summary.json` | Aggregate statistics from the prior parsing. 1 KB. | Medium — useful for orientation, numbers verified and corrected |
| `enrichment/extract-data-dictionary.ts` | Bun TypeScript script used for the initial PDF parse. 8 KB. | Low — documents prior methodology |

## 3. Export Mechanics

- **Format**: Multi-format bundle — Computable PDF, XML, JSON, and CSV depending on data domain. This is **not** FHIR, C-CDA, or a database dump. It is a proprietary, purpose-built EHI export.
- **Single-patient export**: Available via Elation EMR UI. Navigate to patient chart → More → Data Exchange → "Export Entire Health Information (EHI)" → "Export Patient EHI". Export delivered via two emails: one with download link (valid 6 days), one with decryption password. **Requires admin-level privileges.**
- **Bulk/population export**: Must contact Elation support. No self-service UI. "Expedited exports and customized exports may include a cost for customized reports."
- **Confidential Notes**: By default excluded from exports. For patient-requested exports, always withheld. For provider-requested bulk exports, users can choose to include or exclude. Covers: files tagged "Keep this Confidential"/"Mark Confidential", free text in "Notes and Chart Management" (Demographic Dialog), and free text in Billing "Notes" section. This appropriately maps to the psychotherapy notes and litigation compilation carve-outs.
- **Access constraints**: Admin privileges required for single-patient export. Bulk export requires vendor involvement and may incur fees.

## 4. Export Content: What's In It

### Data dictionary structure

The PDF data dictionary (dated 2/6/2024) is a flat table with 4 columns per data element:
- **Data Element**: Field/entity name
- **Data Description**: Brief prose description
- **Export format indicators**: Checkmarks across Computable PDF Export, XML Export, JSON, CSV Export

After correcting 3 parsing errors in the enrichment extraction (see `analysis/parse_and_analyze.py` for details), the dictionary contains **200 data elements** across **15 sections**.

**Critical structural observation**: The data dictionary has **two levels of granularity**:
1. **Field-level detail** for billing/demographics: Individual JSON fields with specific descriptions (e.g., `Billing_status` → "Human readable billing status", `Unit_charge` → "Charge per unit for a CPT")
2. **Domain-level entries only** for clinical data: Entire clinical domains appear as single rows (e.g., "Problem List" → "Patient problem complaints", "Visit Note" → "Visit notes", "Lab Results" → "Lab Results"). No field breakdown is provided for what's inside these exported PDFs/XMLs.

This means we know exactly what billing JSON fields are exported, but have no visibility into the internal structure of clinical data exports.

### Documentation depth

- **Descriptions**: 199 of 200 elements (99.5%) have descriptions. However, 51 (25.5%) are trivial restatements of the field name (e.g., "Patient allergies" for "Allergies", "Guarantor for Patient Payment" for all 9 guarantor fields). Only **148 (74.0%)** have meaningful descriptions.
- **Data types**: **0** elements have data types documented. Some types can be inferred from descriptions (e.g., timestamps noted as "UTC", amounts noted as "in USD"), but no systematic type documentation exists.
- **Value sets**: **0** elements have value sets documented. Fields like `Billing_status`, `Appointment Status`, and `Gender` presumably use constrained value sets, but none are specified.
- **Relationships**: No foreign keys or entity relationships are formally documented, though the billing JSON section implies hierarchical nesting (Bill → CPTs → DXs, PatientLiability → Payment_charges → Payment_requests).
- **Sample data**: None provided.
- **Machine-readable schemas**: None (no JSON Schema, XSD, or OpenAPI spec).

### Vendor's own content organization

| Section (Vendor Category) | Fields | With Description | Meaningful Descriptions | Primary Format(s) |
|---|---|---|---|---|
| Patient Demographics | 57 | 57 | 27 | PDF, CSV, XML |
| Billing - Bills | 52 | 52 | 52 | JSON |
| Billing - Patient Liability | 29 | 29 | 29 | JSON |
| Eligibility/Insurance Verification | 14 | 14 | 14 | JSON |
| Clinical Records | 10 | 9 | 3 | PDF, XML |
| Guarantor Information | 9 | 9 | 0 | CSV |
| Billing - Payment Requests | 9 | 9 | 9 | JSON |
| Appointments | 6 | 6 | 6 | CSV |
| Medications | 5 | 5 | 2 | PDF |
| Care Team & Documents | 3 | 3 | 2 | PDF |
| Additional Demographics | 2 | 2 | 0 | CSV |
| Imaging | 1 | 1 | 1 | PDF |
| Patient Status | 1 | 1 | 1 | CSV |
| Social History | 1 | 1 | 1 | PDF |
| Clinical Orders | 1 | 1 | 1 | PDF, JSON |

**Key pattern**: The billing sections (Bills + Patient Liability + Payment Requests + Eligibility = 104 fields) are documented at full field-level detail with meaningful descriptions for every field. The clinical sections (Clinical Records + Medications + Care Team & Documents + Imaging + Social History + Clinical Orders = 21 entries) are documented only as domain-level categories with mostly trivial descriptions.

The full inventory of all 200 elements with their sections, descriptions, formats, and domain mappings is in `analysis/full-entity-inventory.json`.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The export documentation spans six functional areas, with dramatically varying depth:

**Billing & Financial (104 fields — 52% of all elements)**: This is the deepest area. The "Billing - Bills" section (52 fields) documents a hierarchical JSON object with bills, CPT codes, modifiers, ICD-10/ICD-9 diagnosis codes, charges, provider NPIs, service locations, and timestamps. "Billing - Patient Liability" (29 fields) covers payment charges with processing details, refund tracking, and billing addresses. "Billing - Payment Requests" (9 fields) covers payment request lifecycle. "Eligibility/Insurance Verification" (14 fields) covers RTE checks with plan details, copay, coinsurance, deductible, and out-of-pocket maximums.

**Demographics (61 fields — 30.5%)**: Patient Demographics (57 fields) covers name, DOB, gender, race/ethnicity, address, phone numbers, email, insurance carrier/subscriber/plan details (primary and secondary), preferred pharmacies (primary and secondary), emergency contacts, smoking status, and current prescriptions. Additional Demographics (2) adds sexual orientation and deceased date. Guarantor Information (9 fields) covers guarantor contact details. Patient Status (1) covers living/deceased status.

**Clinical Records (10 domain-level entries)**: Each entry represents an entire clinical data domain exported as Computable PDF (some also XML): Problem List, Procedures, Vitals, Allergies, Visit Note, Lab Results, Referrals, Letters, Medical History Report, Personal Relationship. No field-level detail is provided.

**Medications (5 entries)**: Domain-level entries for OTC medications, Temporary medications, Discontinued Medications, Patient Immunization history, and Permanent Rx. All exported as Computable PDF only.

**Care Team & Documents (3 entries)**: Providers List, Files uploaded to patient chart, Messages (between patient and provider). All Computable PDF.

**Appointments (6 fields)**: Type, Date/Time, Status, Description, Scheduled Provider, Duration. Exported as CSV.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | Patient Demographics (57 fields), Additional Demographics (2), Patient Status (1), Social History (1) — 61 fields total | Thorough field-level documentation |
| Encounters / Visits | ⚠️ Partial | Appointments (6 CSV fields: type, date/time, status, description, provider, duration) | Basic appointment metadata only; no encounter-level clinical data grouping. Visit notes exist separately. |
| Problems / Conditions / Diagnoses | ⚠️ Partial | "Problem List" (1 domain-level entry, PDF+XML) | Listed but no field-level detail. Product stores structured problem lists per (a)(5) certification. |
| Medications / Prescriptions | ⚠️ Partial | 5 medication categories (OTC, Temporary, Discontinued, Permanent Rx) + Current Prescriptions in demographics + 12 pharmacy fields. All PDF. | Listed but no field detail on prescription structure. Product has full ePrescribing/EPCS; no prescription routing data, pharmacy responses, or Surescripts details documented. |
| Allergies | ⚠️ Partial | "Allergies" (1 domain-level entry, PDF+XML) | Listed but no field-level detail. |
| Immunizations | ⚠️ Partial | "Patient Immunization history" (1 entry, PDF) | Listed but no field-level detail. |
| Vitals | ⚠️ Partial | "Vitals" (1 domain-level entry, PDF+XML) | Listed but no field-level detail. |
| Lab Results | ⚠️ Partial | "Lab Results" (1 entry, PDF) | Listed but no field-level detail. |
| Imaging / Diagnostic Reports | ⚠️ Partial | "Imaging Reports" (1 entry, PDF) | Listed but no field-level detail. |
| Procedures | ⚠️ Partial | "Procedures" (1 domain-level entry, PDF+XML) | Listed but no field-level detail. |
| Clinical Notes / Documents | ⚠️ Partial | "Visit Note" (PDF), "Letters" (PDF), "Medical History Report" (PDF), "Files uploaded to the patient chart" (PDF), "Messages" (PDF) | Multiple document types listed, but no structure documented. Unclear if AI-generated notes (Note Assist) are included. |
| Care Plans / Goals | ❌ Not covered | No care plan or goal entities in export | Product has chronic disease management, patient registries, and outreach campaigns. No evidence these are exported. |
| Orders / Referrals | ✅ Covered | "Lab Order, Imaging Order, Pulmonary Order, Cardiac Order, Sleep Order" (PDF+JSON), "Referrals" (PDF) | Orders and referrals listed. Close-the-loop referral tracking status not explicitly documented. |
| Insurance / Coverage | ✅ Covered | 8 insurance fields in demographics (carrier names, subscriber IDs, group numbers, plan names for primary + secondary) + Eligibility/Insurance Verification (14 JSON fields) | Thorough — both demographic insurance info and detailed eligibility checks. |
| Claims / Billing | ✅ Covered | Billing - Bills (52 JSON fields) + Guarantor Information (9 CSV fields) | **Best-documented section.** Detailed JSON structure with CPTs, modifiers, DX codes, charges, provider NPIs, service locations. |
| Payments | ✅ Covered | Billing - Patient Liability (29 JSON fields) + Billing - Payment Requests (9 JSON fields) | Detailed payment processing, refunds, charge lifecycle. |
| Consents / Directives | ❌ Not covered | No consent or directive entities in export | Product likely stores consent documentation; not addressed. |
| Patient Communications / Portal Messages | ⚠️ Partial | "Messages" (1 entry, PDF) | Messages listed but no detail. Patient portal (Patient Passport) features like intake forms, appointment requests, prescription refill requests not explicitly covered. |
| Specialty-specific (Primary Care) | N/A | Primary care platform without specialty-specific modules | Pediatric growth charts and well-child templates are product features; unclear if growth chart data is in the export. |

**Summary**: 6 of 18 domains are well-covered (Demographics, Insurance, Billing, Payments, Orders/Referrals, plus Claims). 10 domains are listed but only at domain level with no field documentation — they appear in the export but we cannot assess depth. 2 domains (Care Plans/Goals, Consents) appear absent despite being product features.

## 6. Documentation Quality

**Strengths**:
- Documentation explicitly addresses § 170.315 (b)(10) by name and correctly describes the designated record set concept
- The export is a genuine purpose-built EHI export — not FHIR or C-CDA repackaging
- Billing data is documented at a genuinely useful field level with a clear hierarchical JSON structure
- The Confidential Notes exclusion mechanism is thoughtfully implemented and well-documented
- Export instructions are clear and step-by-step
- All documentation is publicly accessible without login

**Weaknesses**:
- **Asymmetric documentation depth**: Billing has 104 fields with meaningful descriptions; the entire clinical domain has 21 domain-level entries with mostly trivial descriptions. A developer could reconstruct billing data from this documentation but would have no idea what fields are in a "Visit Note" or "Lab Results" PDF.
- **No sample data**: No example export files are provided. Without seeing the actual output, the clinical data structure is completely opaque.
- **No machine-readable schemas**: No JSON Schema for billing data, no XSD for XML exports, no CSV header documentation. Even the well-documented billing JSON lacks a formal schema.
- **No data types**: Zero elements have documented data types (string, integer, date, etc.)
- **No value sets**: Fields like `Billing_status`, `Appointment Status`, and `Gender` have no enumerated values.
- **No relationships**: No entity-relationship model. The billing JSON implies nesting (Bill contains CPTs, CPTs contain DXs), but no formal documentation of foreign keys or cardinality.
- **"Computable PDF" is an oxymoron**: The clinical data is exported as "Computable PDF" — PDF is inherently not computable. This format makes the clinical data essentially non-machine-readable, undermining the "computable format" requirement of (b)(10).
- **Bulk export is opaque**: Population-level export requires contacting support with potential fees. No documentation of what bulk exports contain or how they differ from single-patient exports.

**Could a developer build an import from this documentation?** For billing data — partially, with significant reverse-engineering. For clinical data — no. The PDF/XML exports have zero documented structure. A developer would need access to actual export files to begin.

## 7. Overall Assessment

### Classification

**Partial native export**

This is a genuine custom EHI export (not C-CDA/FHIR repackaging) that covers clinical, billing, and demographic domains. However, it has two significant limitations: (1) the clinical data documentation is domain-level only — no field-level detail for what's inside visit notes, lab results, vitals, allergies, etc., and (2) the clinical data is exported as "Computable PDF" which is not truly computable. The billing side is well-documented at field level with a clear JSON structure. The overall export appears to cover most data domains but the documentation is too thin on the clinical side to confirm depth, and several product features (care plans, patient portal data, DPC membership) are not visibly covered.

### Key Findings

1. **Billing documentation is genuinely strong**: 104 fields across Bills, Patient Liability, Payment Requests, and Eligibility — all in JSON with meaningful descriptions, hierarchical structure, and specific field-level detail including CPT codes, ICD-10/ICD-9 diagnosis codes, modifier codes, provider NPIs, and service locations. This is better than many vendors' entire export documentation.

2. **Clinical documentation is domain-level only**: All clinical data (problems, medications, allergies, vitals, notes, labs, imaging, referrals) appears as single-row entries in the data dictionary. There are no fields, no structure, and most descriptions are trivial restatements. We know the export *lists* these domains but cannot verify what fields or depth they contain.

3. **"Computable PDF" undermines computability**: The clinical export format — "Computable PDF" — is inherently non-machine-readable. This creates a paradox: the (b)(10) requirement mandates export in a "computable" format, but PDF requires visual inspection or OCR to extract data. Only billing data (JSON) and some demographics/appointments (CSV) are truly computable.

4. **200 data elements across 15 sections**: After correcting 3 parsing errors in the enrichment extraction (1 artifact removed, 2 missing multi-line entries added), the data dictionary documents 200 elements. 148 (74%) have meaningful descriptions. Zero have data types or value sets documented.

5. **Missing product features in export**: Care plans/goals, patient portal intake forms, DPC membership data, telehealth records, and close-the-loop referral tracking — all documented product features — are not explicitly represented in the export.

### Summary Stats

```
Classification:  Partial native export
Export format:   Mixed (PDF, XML, JSON, CSV)
Model type:      Hybrid — native JSON for billing, opaque PDF/XML for clinical
Entities:        15 sections (not normalized tables)
Fields:          200 data elements
Descriptions:    74.0% meaningful (99.5% present, but 25.5% trivially restate field name)
Sample data:     No
Bulk export:     Yes (vendor-assisted, may incur fees)
Domains covered: 6 of 17 well-covered; 10 partial (listed but undocumented structure); 2 absent
```

### Bottom Line

Elation's EHI export is a legitimate, purpose-built export that covers clinical, billing, and demographic data — not a C-CDA/FHIR repackaging. The billing side is impressively documented (104 JSON fields with real descriptions), but the clinical side is essentially a black box: domain names are listed, but the actual data is exported as "Computable PDF" with zero structural documentation. A patient would receive their data, but a developer trying to import it would find the clinical portion non-machine-readable and undocumented. The single biggest gap is the lack of any field-level documentation or machine-readable format for clinical data.
