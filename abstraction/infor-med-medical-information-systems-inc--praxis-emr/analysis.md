# EHI Export Analysis: Infor-Med Medical Information Systems Inc.

**Product**: Praxis EMR Version 9
**Analysis date**: 2026-02-15
**CHPL ID**: 15.02.05.2766.INFO.01.02.1.220310

## 1. Product Context

Praxis EMR is a template-free, AI-driven Electronic Health Record system developed by Infor-Med Medical Information Systems Inc., based in Commerce, CA. The product is marketed primarily to general practitioners and ambulatory care providers across multiple specialties (internal medicine, OB-GYN, gastroenterology, otolaryngology, and others are highlighted in case studies).

The product's core technology is the "Concept Processor," a neural network engine that learns from the physician's own charting patterns rather than using pre-built templates. Key data domains the product manages include:

- **Clinical charting**: Progress notes, H&P, all clinical documentation (the product's primary value proposition)
- **Prescriptions/e-Prescribing**: Direct SureScripts integration including EPCS (controlled substances)
- **Lab results**: Real-time integrated lab results streamed into charts
- **Billing/coding**: Integrated billing through partners (OpenPM, CollaborateMD); PraxCoder for optimal coding and superbill generation
- **Patient portal**: AI-driven portal with intake forms, health maintenance, patient communications
- **Document management**: PraxDocs for scanning, imaging, and archiving documents, faxes, and electronic files
- **Quality reporting**: Datum+ for automated MIPS, ACO, eCQM reporting; clinical quality measures
- **Practice management**: Scheduling, demographics, appointment management
- **Clinical decision support**: Practice advisories, clinical guidelines
- **Immunizations**: Reporting to state registries
- **Secure messaging**: Direct messaging for care coordination
- **Telehealth**: Telemedicine capabilities
- **PDMP integration**: Prescription drug monitoring program data

The product uses Oracle Database as its backend (per the costs/limitations page, an Oracle Database license is required for on-premise installations). The CHPL listing shows certification for 170.315(b)(10) — EHI Export.

## 2. Artifacts Reviewed

| Artifact | Source | Description | Informativeness |
|---|---|---|---|
| `chpl-metadata.json` | CHPL | Certification details: product name, version, developer, certified criteria list | Moderate — confirms (b)(10) certification |
| `praxis-cert.pdf` | praxisemr.com | ONC certification certificate (2 pages) — confirms Praxis EMR v9 certified for (b)(10) among other criteria. Certified 2022-03-10, updated 2025-06-05 | Low — certificate only, no export details |
| `onc-cert-doc.pdf` | praxisemr.com | CMS EHR Certification ID document listing Praxis EMR v8 alongside EMR Direct. Shows CMS EHR ID: 0015EQK5P3WW0UD | Low — no export details |
| Vendor website pages | praxisemr.com | Reviewed ~15 pages including features, billing, portal, certifications, costs/limitations, system requirements, sitemap | Moderate for product context; **zero** for EHI export details |
| Vendor sitemap.xml | praxisemr.com | Complete list of ~70 public URLs — no EHI export documentation page exists | High negative signal — confirms absence |

**Most informative**: The vendor website pages collectively establish what data Praxis EMR stores (setting the baseline for coverage assessment).

**Least informative / Missing**: The downloads directory collected by the prior agent is completely empty. No EHI export documentation, data dictionary, sample data, schema, or export format specification was found anywhere — not on the vendor's website, not via web search, and not on the CHPL listing (which failed to render).

## 3. Export Mechanics

**Format**: Unknown — no documentation found describing the export format.

**Mechanism**: Unknown — no user-facing documentation, screenshots, or process descriptions for the EHI export were found on the vendor's website or through web searches.

**Single-patient vs bulk**: Unknown — while (b)(10) requires both single-patient and patient-population export capabilities, no documentation was found describing how either is invoked in Praxis EMR.

**Access constraints or fees**: The vendor's costs-and-limitations page does not mention any fees specifically for EHI export. The page does note that "There are no known technical restrictions that a user may encounter regarding the exchange or portability of data generated when using the capability."

## 4. Export Content: What's In It

**No export content documentation exists.** After exhaustive searching (detailed in `analysis/search-evidence.md`), no artifacts describing the EHI export content were found:

- No data dictionary
- No schema documentation
- No sample export files
- No format specification
- No field-level documentation
- No entity/table listing
- No export description of any kind

The vendor's website comprehensively describes product features (charting, billing integration, e-prescribing, labs, portal, quality reporting, document management, coding, scheduling) but provides **zero information** about what data is included in the (b)(10) EHI export, in what format, or how to interpret it.

### Vendor's own content organization

No vendor-provided export content organization exists to present. The `analysis/full-entity-inventory.json` file reflects this: it contains zero entities and zero fields.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

**Cannot be assessed.** No export documentation exists from which to determine coverage. The vendor does not describe what data categories, tables, fields, or formats are included in their EHI export.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ❓ Unknown | No export documentation | Product stores demographics (per features page); cannot assess if exported |
| Encounters / visits | ❓ Unknown | No export documentation | Product stores encounter data (core charting function); cannot assess if exported |
| Problems / conditions / diagnoses | ❓ Unknown | No export documentation | Product stores diagnoses (certified for (a)(9) CDS); cannot assess if exported |
| Medications / prescriptions | ❓ Unknown | No export documentation | Product has e-Prescribing with SureScripts/EPCS; cannot assess if exported |
| Allergies | ❓ Unknown | No export documentation | Product stores allergies (certified for (a)(1)-(a)(5)); cannot assess if exported |
| Immunizations | ❓ Unknown | No export documentation | Product reports to state registries; cannot assess if exported |
| Vitals | ❓ Unknown | No export documentation | Product stores vitals (referenced in flowcharts feature); cannot assess if exported |
| Lab results | ❓ Unknown | No export documentation | Product has real-time integrated labs; cannot assess if exported |
| Imaging / diagnostic reports | ❓ Unknown | No export documentation | PraxDocs stores scanned/imported imaging docs; cannot assess if exported |
| Procedures | ❓ Unknown | No export documentation | Product stores procedure reports; cannot assess if exported |
| Clinical notes / documents | ❓ Unknown | No export documentation | Core product function (Concept Processor charting); cannot assess if exported |
| Care plans / goals | ❓ Unknown | No export documentation | Product references flowcharts and care plans; cannot assess if exported |
| Orders / referrals | ❓ Unknown | No export documentation | Product stores referral letters, lab orders; cannot assess if exported |
| Insurance / coverage | ❓ Unknown | No export documentation | Billing integration partners handle insurance; cannot assess if exported |
| Claims / billing | ❓ Unknown | No export documentation | Superbills/PraxCoder; billing via OpenPM/CollaborateMD integration; cannot assess if exported |
| Payments | ❓ Unknown | No export documentation | Billing partners handle payments; cannot assess if exported |
| Consents / directives | ❓ Unknown | No export documentation | Portal references consent forms; cannot assess if exported |
| Patient communications / portal messages | ❓ Unknown | No export documentation | Patient portal with AI-driven communications; cannot assess if exported |

**Every domain is "Unknown"** because no export documentation of any kind was found. This is not a case where documentation exists but is thin — it is a case where documentation appears to be entirely absent from the public internet.

## 6. Documentation Quality

**Documentation quality: Non-existent.**

There is no EHI export documentation to assess. Per 170.315(b)(10), certified health IT must provide publicly accessible documentation describing the format of the export. Despite:

- Reviewing the complete vendor website sitemap (70+ pages)
- Probing 20+ common EHI documentation URL paths
- Conducting multiple web searches across different search engines
- Downloading and examining ONC certification documents
- Attempting to access the CHPL listing (site failed to render)

...no EHI export documentation was found. A developer receiving an EHI export from Praxis EMR would have zero documentation to work from — no data dictionary, no schema, no format specification, no sample data, and no export process description.

The vendor's website is well-developed for marketing and feature descriptions, which makes the complete absence of compliance documentation particularly notable. The mandatory disclosures page (certifications-and-costs.html) lists the certified criteria including (b)(10) but provides no link to export documentation.

## 7. Overall Assessment

### Classification

**Minimal/stub**: Documentation is entirely absent. It is impossible to determine what the export contains, what format it uses, or how to access it. While the product is certified for (b)(10), no publicly accessible evidence exists to evaluate the export's quality, completeness, or usability.

### Key Findings

1. **No publicly accessible EHI export documentation exists.** After exhaustive searching of the vendor website, web searches, and CHPL, zero documentation about the EHI export format, content, or process was found. This appears to violate the (b)(10) requirement for publicly accessible export format documentation.

2. **The product stores substantial clinical and administrative data.** Based on product feature descriptions, Praxis EMR manages demographics, clinical notes, prescriptions, labs, vitals, immunizations, documents, billing/coding data, portal communications, and more — all of which should be covered by an EHI export.

3. **The prior collection agent found nothing.** The downloads directory is completely empty, and no product-research.md or ehi-export-report.md files were generated, suggesting the prior agent also could not find any export documentation.

4. **Billing is handled through integration partners** (OpenPM, CollaborateMD), which raises questions about whether billing data generated through these integrations would be included in any Praxis EHI export, or whether it resides in the partner systems.

5. **The product uses Oracle Database** as its backend, suggesting a structured relational data model exists. However, no database schema, table listing, or data dictionary has been made public.

### Summary Stats

```
Classification:  Minimal/stub
Export format:   Unknown (no documentation found)
Model type:      Unknown
Entities:        N/A (no data dictionary)
Fields:          N/A
Descriptions:    N/A
Sample data:     No
Bulk export:     Unknown
Domains covered: 0 of 18 assessable (all Unknown due to absent documentation)
```

### Bottom Line

It is impossible to assess whether a patient or provider would get a usable, complete copy of their data from Praxis EMR's EHI export because **no publicly accessible documentation about the export exists**. The single biggest issue is the apparent absence of any export documentation — a basic regulatory requirement under 170.315(b)(10). While the product is ONC-certified and stores broad clinical data, the complete lack of public export documentation makes it impossible to evaluate export quality, format, content, or completeness. This represents one of the most opaque (b)(10) implementations encountered.
