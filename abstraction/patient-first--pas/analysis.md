# EHI Export Analysis: Patient First

**Product**: PAS
**Analysis date**: 2026-02-16
**CHPL IDs**: 15.04.04.2140.PAS1.15.02.1.221212

## 1. Product Context

Patient First is a privately held urgent care / primary care chain operating ~79 walk-in clinics across Virginia, Maryland, Pennsylvania, and New Jersey. Uniquely, Patient First developed its own EHR system ("PAS") in-house — it is not commercially sold. PAS is a full-scope integrated EHR covering clinical documentation, CPOE (medications, labs, imaging), e-prescribing (via Surescripts; ~1.9M Rx/year), on-site lab and x-ray, medication dispensing, patient portal, quality measure reporting, public health reporting (immunizations, syndromic surveillance), transitions of care (C-CDA via DataMotion), and billing/claims. It also supports occupational health workflows (DOT physicals, drug screens, workers' comp). The system serves ~240K portal logins/year and processes ~716K C-CDAs/year for transitions of care.

For a (b)(10) assessment, the export should cover: clinical encounters and notes, problems, medications, allergies, vitals, labs, imaging (x-rays), immunizations, prescriptions/dispensing records, scanned documents, patient messages, referral/consult documents, billing/claims, insurance data, occupational health records, and any specialty forms.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/mandatory-disclosure-page-api.json` (26 KB) | WordPress REST API JSON of the mandatory disclosure page. Contains the EHI export section: 1 paragraph + 1 table (7 rows × 4 columns). **Primary source of export documentation.** | High — this *is* the entire EHI export documentation |
| `downloads/mandatory-disclosure-page.html` (530 KB) | Full HTML page of mandatory disclosures. Same content as API JSON but in full page context. | Redundant with API JSON |
| `downloads/PatientFirst_Real_World_Test_Results_CY2025.pdf` (23 pages, 227 KB) | CY 2025 Real World Testing Results. RWT Measure #3 covers b(10) with operational data. | Moderate — reveals the b(10) metric is labeled "Number of C-CDA Batch Exports Sent" (31 exports in Q1 2025) |
| `downloads/screenshot-ehi-export-section.png` (213 KB) | Screenshot of the EHI export section on the disclosure page. | Low — visual confirmation only |
| `downloads/screenshot-page-top.png` (252 KB) | Screenshot of page header and certification list. | Low — visual confirmation only |

No data dictionary, schema, sample data, or additional documentation artifacts exist beyond the single HTML table.

## 3. Export Mechanics

- **Format**: Multi-format ZIP archive with 7 folders, each containing files in a category-specific format (C-CDA XML, DICOM, JPG/PNG, PDF, EML, JSON)
- **Mechanism**: Manual "one-time export" per the documentation. The exact UI workflow is not described; no API endpoint is documented.
- **Single-patient vs bulk**: The documentation says "manual one-time export" for a patient's record. The RWT report mentions "bulk patient exports" in passing but the metric is per-patient export count. 31 exports in Q1 2025 across ~79 clinics (~0.4 per clinic per quarter).
- **Access constraints**: Not documented. No mention of fees.
- **Turnaround**: Not documented.

## 4. Export Content: What's In It

### Documentation scope

The entire EHI export documentation consists of **1 paragraph and 1 table (7 rows × 4 columns)** on the mandatory disclosure page. There is:

- **No data dictionary** — zero field-level documentation for any export category
- **No JSON schema** for the Financials/BillingClaim JSON format
- **No C-CDA template specification** or profile documentation
- **No DICOM metadata description**
- **No sample export files**
- **No user guide or instructions**

### Vendor's own content organization

| Entity/Category | Fields | Described | Types | Format | Folder |
|---|---|---|---|---|---|
| Medical Records | N/A | Category-level only | N/A | XML (C-CDA) | CCDA |
| X-Rays | N/A | Category-level only | N/A | DCM (DICOM) | Xray |
| Scanned Images | N/A | Category-level only | N/A | JPG, PNG, etc. | Scan/{type} |
| Consults | N/A | Category-level only | N/A | PDF | ConsultNotes |
| Messages | N/A | Category-level only | N/A | EML | DirectSecureMessages |
| Forms | N/A | Category-level only | N/A | PDF | Forms |
| Financials | N/A | Category-level only | N/A | JSON | BillingClaim |

**Total entities/categories**: 7
**Total documented fields**: 0 (no field-level documentation exists)

The vendor provides no breakdown of what is inside each category. For "Medical Records," the only description is "Medical records in industry-standard C-CDA format" — no mention of which C-CDA sections, templates, or data elements are included. For "Financials," the only description is "Billing and Claim information" in JSON format — no schema, no field names, no structure.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor describes 7 export categories spanning clinical records, imaging, documents, messages, and financials. This is a broader set of categories than most vendors provide — notably including:

- **DICOM x-ray images**: Unusual and positive; most vendors don't export actual imaging data
- **Scanned documents** (insurance cards, photo IDs): Administrative artifacts often omitted
- **Secure messages** in EML format: Patient communications preserved in a standard format
- **Billing/claims in JSON**: Financial data included in a computable format
- **Consult/referral documents**: PDF documents from referrals
- **Forms** (e.g., drug screen results): Specialty/occupational health documents

However, the depth within each category is completely unknown. The C-CDA "Medical Records" category could contain a rich set of sections or a minimal clinical summary — the documentation doesn't say. The JSON "Financials" could include detailed claim line items or just a billing summary — no schema is provided.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | Presumably in C-CDA Medical Records (standard C-CDA includes demographics) | C-CDA includes basic demographics; unclear if full registration detail (emergency contacts, employer info, etc.) is captured |
| Encounters / visits | ⚠️ Partial | Presumably in C-CDA Medical Records | C-CDA typically includes encounter data but level of detail unknown |
| Problems / conditions | ⚠️ Partial | Presumably in C-CDA Medical Records | Standard C-CDA section; depth unknown |
| Medications / prescriptions | ⚠️ Partial | Presumably in C-CDA Medical Records | C-CDA includes medication lists; unclear if individual prescription records (~1.9M/year) or on-site dispensing records are included |
| Allergies | ⚠️ Partial | Presumably in C-CDA Medical Records | Standard C-CDA section |
| Immunizations | ⚠️ Partial | Presumably in C-CDA Medical Records | Standard C-CDA section |
| Vitals | ⚠️ Partial | Presumably in C-CDA Medical Records | Standard C-CDA section |
| Lab results | ⚠️ Partial | Presumably in C-CDA Medical Records | C-CDA typically includes lab results; unclear if discrete structured results from on-site CLIA labs are fully captured or summarized |
| Imaging / diagnostic reports | ✅ Covered | X-Rays category exports DICOM files | Strong — actual images exported in native DICOM format |
| Procedures | ⚠️ Partial | Presumably in C-CDA Medical Records | Standard C-CDA section |
| Clinical notes / documents | ⚠️ Partial | C-CDA Medical Records + Consults (PDF) + Forms (PDF) | Multiple categories address documents; unclear if all note types are covered |
| Care plans / goals | ⚠️ Partial | Presumably in C-CDA if documented | Product likely captures care plans for primary care; coverage unknown |
| Orders / referrals | ⚠️ Partial | Consults category exports referral documents as PDF | Referral documents are exported; unclear if order detail (lab orders, imaging orders) is captured beyond C-CDA |
| Insurance / coverage | ⚠️ Partial | Scanned Images includes insurance cards | Scanned card images are present; structured insurance/eligibility data unclear |
| Claims / billing | ⚠️ Partial | Financials category exports "Billing and Claim information" as JSON | Category exists but zero field documentation; impossible to assess depth without a schema or sample |
| Payments | ❌ Not covered | No evidence of payment data in export | Patient First portal allows payment; payment history likely exists in PAS but not mentioned in export |
| Consents / directives | ❌ Not covered | No evidence | Likely exists (HIPAA consents, telehealth consent); not mentioned |
| Patient communications | ✅ Covered | Messages category exports secure messages as EML | Patient-provider messages explicitly included |
| Occupational health | ⚠️ Partial | Forms category mentions "Drug Screen results" as PDF | Drug screen forms included; DOT physical structured data, workers' comp records unclear |

**Key uncertainty**: Because the clinical data is exported as "industry-standard C-CDA format" with no further specification, it's impossible to determine whether the C-CDA includes only USCDI-minimum sections or a richer set of data. C-CDA is capable of encoding extensive clinical data, but many implementations only populate the basic sections (problems, medications, allergies, vitals, immunizations, procedures, results). Without a template specification or sample file, the actual clinical depth is unknown.

## 6. Documentation Quality

The documentation is **minimal — among the thinnest we've seen**. The entire EHI export specification is 1 paragraph + 7 table rows on a WordPress page. There are:

- **Zero** field-level definitions across all 7 categories
- **No schema** for the JSON billing format (the only proprietary structured format)
- **No C-CDA implementation guide** or template list
- **No sample exports** to inspect
- **No user/developer guide** for requesting or interpreting exports
- **No versioning** information

A developer receiving this export would know the folder structure and file formats but would have **no documentation to interpret the content**. The C-CDA and DICOM formats are self-describing standards, which partially mitigates this for 2 of the 7 categories. But the JSON financial data is completely opaque without documentation — a developer would need to reverse-engineer the structure.

The RWT report's b(10) metric being labeled "Number of C-CDA Batch Exports Sent" raises a question: does the actual export include all 7 categories, or is the operational reality just C-CDA batch exports? The disclosure page describes the full 7-category ZIP, but the RWT metric language suggests the export may be C-CDA-centric in practice.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Partial**

The 7 export categories span clinical, imaging, documents, communications, and financial data — broader than a pure C-CDA or FHIR repackaging. The inclusion of DICOM x-rays, secure messages (EML), scanned documents, and billing JSON demonstrates genuine effort to export beyond USCDI clinical summaries. However, without field-level documentation, a schema for the JSON financial data, or sample exports, it's impossible to verify the actual depth within each category. The clinical data relies on C-CDA, which may or may not go beyond USCDI. Payments, consents, and detailed occupational health data appear absent. The export is more complete than a simple C-CDA repackaging but the documentation is too thin to confirm comprehensive coverage.

**Axis 2 — Export approach: Purpose-built EHI export**

This is clearly not a repackaged (g)(10) FHIR API or a simple C-CDA export relabeled as (b)(10). The multi-format ZIP structure with 7 distinct categories (C-CDA, DICOM, EML, JSON, PDF, images) is purpose-built for EHI export. The inclusion of non-clinical data (billing JSON, scanned documents, messages) confirms this was designed specifically for (b)(10) rather than repurposing an existing clinical exchange mechanism. The RWT metric's "C-CDA Batch Exports" label is concerning but the documented export structure clearly goes beyond C-CDA. Patient First, as both the developer and sole user of PAS, had the advantage of designing the export around their own data model.

### Key Findings

1. **Purpose-built multi-format export with genuine breadth**: The 7-category ZIP structure (C-CDA, DICOM, EML, JSON, PDF, images) covers clinical records, imaging, documents, communications, and billing — broader than most vendors' (b)(10) implementations. The inclusion of DICOM x-rays and EML messages is notably thorough.

2. **Zero field-level documentation**: Despite covering 7 categories, there is no data dictionary, no schema, no field definitions, and no sample data for any category. The entire documentation is 1 paragraph and a 7-row table. The JSON billing format is completely undocumented.

3. **C-CDA clinical depth is unknowable**: The "Medical Records" category is described only as "industry-standard C-CDA format." Without a template specification, section list, or sample file, it's impossible to determine whether this contains rich clinical detail or a minimal USCDI summary.

4. **RWT metric suggests C-CDA centricity**: The b(10) Real World Testing metric is labeled "Number of C-CDA Batch Exports Sent" despite the documented export being a multi-format ZIP. This ambiguity raises questions about whether the full 7-category export is what's actually produced in practice.

5. **Very low export volume**: 31 exports in Q1 2025 across ~79 clinics (annualized ~124/year). This is operationally marginal, suggesting EHI export is rarely requested or used.

### Summary Stats

```
Coverage:        Partial
Approach:        Purpose-built EHI export
Export format:   Multi-format ZIP (C-CDA XML, DICOM, EML, JSON, PDF, JPG/PNG)
Entities:        7 categories (no field-level breakdown)
Fields:          N/A (no field-level documentation)
Descriptions:    N/A (category-level descriptions only)
Sample data:     No
Bulk export:     Unclear (RWT mentions "bulk patient exports" but details absent)
Domains covered: 11 of 17 applicable domains (most only partially, due to documentation gaps)
```

### Bottom Line

Patient First built a genuinely purpose-built EHI export that spans 7 data categories including clinical records, imaging, billing, and communications — more breadth than many vendors. However, the documentation is critically thin: zero field-level definitions, no JSON schema for billing data, no sample exports, and no C-CDA template specification. A patient would receive a ZIP file with data in standard formats, but a developer or downstream system would have no documentation to interpret most of it — particularly the proprietary billing JSON. The biggest gap is documentation depth, not export scope.
