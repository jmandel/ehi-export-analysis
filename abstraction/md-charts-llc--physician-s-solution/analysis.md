# EHI Export Analysis: MD Charts, LLC

**Product**: Physician's Solution (also branded as DermCharts, KidsCharts, OBGYNCharts)
**Analysis date**: 2026-02-15
**CHPL ID**: 15.99.09.2479.PH01.11.01.1.230117 (listing 11214)

## 1. Product Context

Physician's Solution by MD Charts, LLC is an all-in-one cloud-based EHR, practice management, and revenue cycle management platform for ambulatory practices. Certified as a "Complete EHR" in January 2023, it holds 37 ONC certification criteria including 170.315(b)(10) for EHI export. The product is headquartered in Great Neck, New York and has approximately 150+ implementations.

The product's primary specialty focus is **dermatology** (the SED intended user description is "Dermatology"), and it is marketed under specialty-branded names (DermCharts, KidsCharts, OBGYNCharts). It serves multiple ambulatory specialties including OB-GYN, pediatrics, cardiology, urology, hematology/oncology, internal medicine, gastroenterology, and pulmonology.

**Key data domains the product stores** (based on vendor marketing at mdchartsehr.com and product research):

- **Clinical EHR**: Patient demographics, clinical notes (100+ specialty templates), problem lists, medication lists, allergies, lab orders/results (bidirectional with 20+ labs), vitals, immunizations, growth charts (pediatrics), clinical images (especially dermatology), biopsy tracking (BiopsyMapping™, InstaPath℠), e-prescribing, clinical decision support, implantable device tracking
- **Practice Management**: Scheduling, patient reminders, electronic intake forms, insurance eligibility verification, 300+ built-in reports, inventory control
- **Revenue Cycle Management / Billing**: Charge capture (Peak Charge Capture™), Smart Super Bill℠, claims scrubbing, electronic claims submission, payment posting, denial management, A/R tracking, text-to-pay (MDCPay™), collections management
- **Patient Engagement**: Patient portal (view/download/transmit), portal messages, educational materials, remote check-in
- **Interoperability**: C-CDA transitions of care, FHIR API (g)(10), public health reporting (immunization registries, syndromic surveillance, electronic case reporting, cancer registries)

This is a feature-rich product with deep clinical, billing, and specialty functionality — the EHI export should correspondingly be substantial.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/screenshot-port-47102-unreachable.png` (51 KB) | Browser screenshot showing `ERR_ADDRESS_UNREACHABLE` for the registered EHI export documentation URL | Confirms URL is dead |
| `downloads/screenshot-mraemr-cert-invalid.png` (72 KB) | Browser screenshot showing `ERR_CERT_DATE_INVALID` for mraemr.com on standard HTTPS port | Confirms SSL certificate issues |
| `downloads/screenshot-why-mdcharts-page.png` (1.5 MB) | Full-page screenshot of vendor's "Why MD Charts" marketing page with ONC certification section | Shows no EHI export documentation exists on marketing site |
| `files.json` | Manifest of downloaded artifacts — 3 screenshots, all showing error states | Confirms no substantive artifacts were obtainable |
| `ehi-export-report.md` | Prior agent's narrative documenting extensive attempts to reach documentation | Useful orientation; findings independently verified |
| `product-research.md` | Research on product capabilities and data domains | Establishes baseline for coverage assessment |
| `chpl-metadata.json` | CHPL certification details including registered URL | Confirms registered URL and certification criteria |

**No substantive EHI export documentation artifacts exist.** The entire downloads folder contains only screenshots of error pages. There is no data dictionary, no schema, no sample data, no export guide, no PDF, no HTML documentation — nothing.

## 3. Export Mechanics

**Unknown.** The registered EHI export documentation URL (`https://mraemr.com:47102/api/DataExportGuidance.asp`) is completely unreachable:

- **Port 47102** on mraemr.com does not accept TCP connections (curl exit code 7: connection refused)
- **Port 443** (standard HTTPS) on mraemr.com is also unreachable as of 2026-02-15 ("No route to host")
- **Port 80** responds but only serves a default IIS 8.5 landing page — not the EHR application or any documentation
- The URL path (`DataExportGuidance.asp`) suggests a Classic ASP guidance page, but its actual content is unknown
- The mandatory disclosures page (`https://mraemr.com:47102/api/mandatory_disclosure.asp`) uses the same dead port and is equally inaccessible
- **No Wayback Machine snapshots** exist for any page on port 47102, so no historical version can be examined
- **No Google indexing** of the page exists
- The vendor's marketing website (mdchartsehr.com) contains no EHI export documentation of any kind

The following cannot be determined:
- Export format (CSV, JSON, FHIR, C-CDA, native database dump, etc.)
- Export mechanism (UI button, API call, vendor-assisted, etc.)
- Single-patient vs. bulk capability
- Access constraints or fees
- What data is included in the export

## 4. Export Content: What's In It

**Cannot be assessed.** No documentation, data dictionary, schema, or sample data is available for review. The only evidence that an EHI export capability exists is:

1. The product is certified for 170.315(b)(10), which requires EHI export support
2. A URL was registered in CHPL for export documentation

Without accessible documentation, it is impossible to determine:
- How many entities/tables the export contains
- What fields are included
- Whether field descriptions, types, relationships, or value sets are documented
- Whether sample data exists
- What data domains are covered

### Vendor's own content organization

No vendor-provided content organization can be presented because no documentation is accessible.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

**Cannot be assessed.** No export documentation is available to analyze.

### 5b. Standardized domain coverage (top-down)

Because no export documentation is accessible, coverage for every domain is marked as **Unknown**. The "Product stores this?" column is based on vendor marketing and product research.

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ❓ Unknown | No documentation accessible | Product stores demographics (certified for (a)(5)); cannot assess export coverage |
| Encounters / visits | ❓ Unknown | No documentation accessible | Product stores encounter data; cannot assess |
| Problems / conditions / diagnoses | ❓ Unknown | No documentation accessible | Product stores problem lists (certified for (a)(1)); cannot assess |
| Medications / prescriptions | ❓ Unknown | No documentation accessible | Product stores medications and e-prescribes (certified for (a)(1)); cannot assess |
| Allergies | ❓ Unknown | No documentation accessible | Product stores allergies (certified for (a)(3)); cannot assess |
| Immunizations | ❓ Unknown | No documentation accessible | Product stores immunizations (certified for (f)(1)); cannot assess |
| Vitals | ❓ Unknown | No documentation accessible | Product likely stores vitals; cannot assess |
| Lab results | ❓ Unknown | No documentation accessible | Product stores labs with bidirectional interfaces to 20+ labs; cannot assess |
| Imaging / diagnostic reports | ❓ Unknown | No documentation accessible | Product stores clinical images (especially dermatology); cannot assess |
| Procedures | ❓ Unknown | No documentation accessible | Product stores procedures; cannot assess |
| Clinical notes / documents | ❓ Unknown | No documentation accessible | Product stores notes via 100+ specialty templates; cannot assess |
| Care plans / goals | ❓ Unknown | No documentation accessible | Unclear if product stores structured care plans; cannot assess |
| Orders / referrals | ❓ Unknown | No documentation accessible | Product supports CPOE and AutoConsult Letters™; cannot assess |
| Insurance / coverage | ❓ Unknown | No documentation accessible | Product stores insurance and does real-time eligibility verification; cannot assess |
| Claims / billing | ❓ Unknown | No documentation accessible | Product has deep RCM (claims, payments, denials, A/R); cannot assess |
| Payments | ❓ Unknown | No documentation accessible | Product supports payment posting and MDCPay™; cannot assess |
| Consents / directives | ❓ Unknown | No documentation accessible | Unclear if product stores these; cannot assess |
| Patient communications / portal messages | ❓ Unknown | No documentation accessible | Product has patient portal; cannot assess |
| Specialty-specific (Dermatology) | ❓ Unknown | No documentation accessible | Product stores biopsy tracking, lesion mapping, derm-specific data; cannot assess |

## 6. Documentation Quality

**Documentation is inaccessible.** This represents the most fundamental failure mode possible for EHI export compliance:

- The registered documentation URL has been unreachable since at least 2026-02-14 (and possibly longer, as no Wayback Machine snapshots exist to indicate it was ever publicly crawlable)
- The URL uses a non-standard port (47102), which is inherently fragile — it suggests the documentation was served from the same server as the EHR application rather than a dedicated documentation platform
- The vendor's marketing website contains no alternative EHI export documentation
- The mandatory disclosures page uses the same dead port and is equally inaccessible
- The mraemr.com domain uses dynamic DNS (noip.com for mail), suggesting small-scale self-hosted infrastructure
- Even the standard HTTPS port (443) on mraemr.com is now unreachable, with only port 80 serving a default IIS page

A developer, patient, or regulator has no way to understand what the EHI export contains, how to request it, or what format to expect. The documentation is not merely thin or incomplete — it is nonexistent from a public accessibility standpoint.

## 7. Overall Assessment

### Classification

**Minimal/stub**: Documentation is completely inaccessible, making it impossible to assess what the export covers. While the product is certified for (b)(10) and a documentation URL was registered, the URL has been unreachable with no archived version available. The hosting infrastructure appears degraded (non-standard port, expired SSL certificate, and now the standard HTTPS port is also down). This represents a compliance failure in making export documentation publicly accessible as required.

### Key Findings

1. **Registered EHI export documentation URL is completely dead.** The URL `https://mraemr.com:47102/api/DataExportGuidance.asp` uses a non-standard port (47102) that does not accept TCP connections. No alternative documentation source exists. (Verified 2026-02-15; see `analysis/verification-log.md`)

2. **No Wayback Machine or Google cache exists.** The documentation page was never indexed or archived by any public service, meaning no historical version can be examined. It is unknown whether the page ever contained substantive content.

3. **Infrastructure appears degraded.** As of 2026-02-15, even the standard HTTPS port (443) on mraemr.com is unreachable ("No route to host"), whereas it was reportedly accessible one day earlier. Only port 80 responds, serving a default IIS page. The domain uses dynamic DNS (noip.com), suggesting fragile self-hosted infrastructure.

4. **Mandatory disclosures are also inaccessible.** The mandatory disclosures URL (`https://mraemr.com:47102/api/mandatory_disclosure.asp`) uses the same dead port, meaning both required public-facing compliance documents are unreachable. The marketing site links to this dead URL.

5. **The product stores extensive data that should be exportable.** Physician's Solution is a full-featured EHR+PM+RCM platform with deep clinical, billing, and specialty-specific (especially dermatology) functionality across 37 ONC certification criteria. The gap between what the product stores and what can be verified as exportable is total — nothing can be verified.

### Summary Stats

```
Classification:  Minimal/stub
Export format:   Unknown (documentation inaccessible)
Model type:      Unknown
Entities:        N/A
Fields:          N/A
Descriptions:    N/A
Sample data:     No
Bulk export:     Unknown
Domains covered: 0 of 19 verifiable (all unknown due to inaccessible documentation)
```

### Bottom Line

MD Charts' EHI export documentation is completely inaccessible — the registered URL on a non-standard port is dead, no archived version exists, and no alternative documentation is available anywhere. For a product that stores extensive clinical, billing, and specialty data across dermatology, OB-GYN, pediatrics, and other specialties, this is a significant compliance failure. A patient, provider, or developer has absolutely no way to determine what the EHI export contains, how to obtain it, or what format to expect.
