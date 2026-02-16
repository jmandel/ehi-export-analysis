# EHI Export Analysis: MD Charts, LLC

**Product**: Physician's Solution
**Analysis date**: 2026-02-16
**CHPL IDs**: 11214 (15.99.09.2479.PH01.11.01.1.230117)

## 1. Product Context

Physician's Solution by MD Charts, LLC is an all-in-one cloud-based EHR, practice management, and revenue cycle management platform for ambulatory practices. Certified as a Complete EHR (January 2023), it serves multiple specialties under specialty-branded names: DermCharts (dermatology, the primary focus), KidsCharts (pediatrics), and OBGYNCharts (OB-GYN). The company is small (11–50 employees), based in Great Neck, NY, with approximately 150+ implementations.

The product stores extensive data across clinical, administrative, and financial domains:

- **Clinical**: Encounter documentation with 100+ customizable templates, problem lists, medication lists (e-prescribing to 50,000+ pharmacies), allergies, lab orders and results (bidirectional with 20+ labs including LabCorp, Quest, BioReference), immunizations, growth charts, clinical images, dermatology-specific biopsy tracking (BiopsyMapping™, InstaPath℠), telehealth records
- **Practice management**: Scheduling, patient intake forms, insurance eligibility verification, inventory control, 300+ built-in reports
- **Revenue cycle / billing**: Charge capture (Peak Charge Capture™), claims scrubbing (3M+ CCI edits), electronic claims submission, payment posting, denial management, A/R tracking, collections, patient account ledgers
- **Patient engagement**: Patient portal (view/download/transmit), secure messaging, educational materials, online payments (MDCPay™)
- **Reporting**: MIPS quality measures, SwiftDat™ dashboards, custom report builder

This breadth of functionality means a complete EHI export should cover clinical documentation, medications, labs, billing/claims, insurance, patient communications, and specialty-specific data (particularly dermatology biopsy tracking).

## 2. Artifacts Reviewed

| Artifact | Description | Size | Informative? |
|---|---|---|---|
| `screenshot-port-47102-unreachable.png` | Chrome error page (ERR_ADDRESS_UNREACHABLE) for the registered EHI export URL | 52 KB | Yes — confirms port 47102 is unreachable |
| `screenshot-mraemr-cert-invalid.png` | Chrome certificate error (ERR_CERT_DATE_INVALID) for mraemr.com standard port | 74 KB | Yes — documents expired SSL certificate on the EHR application domain |
| `screenshot-why-mdcharts-page.png` | Full-page screenshot of vendor's "Why MD Charts" compliance page | 1.6 MB | Yes — shows no EHI export content exists on the marketing site; mandatory disclosures link points to same dead port 47102 |

**No EHI export documentation artifacts exist in the downloads.** All three files are screenshots documenting the inaccessibility of the registered documentation URL. There are no data dictionaries, schemas, sample data files, PDFs, or any other export-related artifacts.

## 3. Export Mechanics

**Cannot be assessed.** The registered EHI export documentation URL (`https://mraemr.com:47102/api/DataExportGuidance.asp`) is completely unreachable. The URL path suggests a Classic ASP page that provided export guidance documentation, but no information about the export format, mechanism, access method, or capabilities can be determined.

**Independently verified on 2026-02-16:**
- **Port 47102**: TCP connection fails with "No route to host" (curl exit code 7). The service on this non-standard port is not running or is firewalled.
- **Port 443 (standard HTTPS)**: Also fails with "No route to host." The entire server at 75.99.93.174 appears to be offline. (Note: The prior collection report from 2026-02-14 found port 443 alive but with an expired certificate; the server has since gone fully offline.)
- **Marketing site** (mdchartsehr.com): Accessible. Contains no EHI export documentation. The "Why MD Charts" page links to mandatory disclosures at `https://mraemr.com:47102/api/mandatory_disclosure.asp` — the same dead port.
- **Wayback Machine**: No captures exist for any URL on `mraemr.com:47102`. Only 4 captures of the root domain exist (2016–2025), all showing the login page.
- **Google/web search**: No indexed or cached copies of the documentation page.

## 4. Export Content: What's In It

**Unknown.** No export documentation of any kind was retrievable. There is:

- No data dictionary
- No schema or field listing
- No sample data files
- No export format specification
- No API documentation
- No user-facing export instructions

The only evidence that an EHI export capability exists is:
1. The product is certified for 170.315(b)(10) (EHI export) as of January 2023
2. A URL was registered in CHPL for export documentation

### Vendor's own content organization

Not applicable — no vendor-provided export documentation is available to analyze.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

**Cannot be assessed.** No export documentation is available to determine what data domains are included in the export.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ❓ Unknown | No documentation accessible | Product stores demographics (certified (a)(5)); cannot assess export coverage |
| Encounters / visits | ❓ Unknown | No documentation accessible | Product stores encounter data; cannot assess |
| Problems / conditions / diagnoses | ❓ Unknown | No documentation accessible | Product stores problem lists (certified (a)(1)); cannot assess |
| Medications / prescriptions | ❓ Unknown | No documentation accessible | Product stores medications/e-prescribing (certified (a)(2)); cannot assess |
| Allergies | ❓ Unknown | No documentation accessible | Product stores allergies (certified (a)(3)); cannot assess |
| Immunizations | ❓ Unknown | No documentation accessible | Product stores immunization records (certified (f)(1)); cannot assess |
| Vitals | ❓ Unknown | No documentation accessible | Likely stored in clinical encounters; cannot assess |
| Lab results | ❓ Unknown | No documentation accessible | Product has bidirectional lab interfaces with 20+ labs; cannot assess |
| Imaging / diagnostic reports | ❓ Unknown | No documentation accessible | Product stores clinical images, especially dermatology; cannot assess |
| Procedures | ❓ Unknown | No documentation accessible | Product stores procedure data via billing/charge capture; cannot assess |
| Clinical notes / documents | ❓ Unknown | No documentation accessible | Product has 100+ customizable templates; cannot assess |
| Care plans / goals | ❓ Unknown | No documentation accessible | Cannot assess |
| Orders / referrals | ❓ Unknown | No documentation accessible | Product has AutoConsult Letters™; cannot assess |
| Insurance / coverage | ❓ Unknown | No documentation accessible | Product does real-time eligibility verification; cannot assess |
| Claims / billing | ❓ Unknown | No documentation accessible | Product has extensive RCM/billing (C-Track™, claims scrubbing, payment posting); cannot assess |
| Payments | ❓ Unknown | No documentation accessible | Product has payment posting and MDCPay™; cannot assess |
| Patient communications / portal messages | ❓ Unknown | No documentation accessible | Product has patient portal (certified (e)(1)); cannot assess |
| Specialty-specific (Dermatology) | ❓ Unknown | No documentation accessible | Product has BiopsyMapping™ and InstaPath℠; cannot assess |

**Every domain is unassessable** because no export documentation exists to review. The product clearly stores data across all these domains based on its feature set and ONC certifications, but whether the (b)(10) export covers any, some, or all of them cannot be determined.

## 6. Documentation Quality

**Documentation is entirely inaccessible.** The registered EHI export documentation URL has been unreachable since at least 2026-02-14 (the collection date). Key issues:

1. **Non-standard port**: Hosting public compliance documentation on port 47102 is inherently fragile. This suggests the documentation was served from the same infrastructure as the EHR application (an IIS server running Classic ASP), not a dedicated documentation platform.

2. **No redundancy**: There is no mirror, backup, or alternative location for the documentation. The vendor's WordPress marketing site (mdchartsehr.com) contains no EHI-related content.

3. **No archival**: The Wayback Machine never captured the page, and no search engine indexed it. The documentation may have existed at some point but left no public trace.

4. **Mandatory disclosures also unreachable**: The mandatory disclosures URL (`https://mraemr.com:47102/api/mandatory_disclosure.asp`) uses the same dead port, indicating a systemic infrastructure failure affecting all ONC compliance documentation.

5. **Server now fully offline**: As of 2026-02-16, even the standard HTTPS port (443) on mraemr.com is unreachable, whereas it was responding 2 days earlier with the EHR login page.

A developer or patient seeking to understand the EHI export would find **nothing** — no documentation, no guidance, no data dictionary, no sample data.

## 7. Overall Assessment

### Classification

**Minimal/stub**: Documentation is entirely inaccessible. The export cannot be assessed because no documentation, schema, sample data, or any other artifact is publicly available. The registered URL is dead, no alternative sources exist, and no web archive captured the content.

### Key Findings

1. **EHI export documentation URL is completely unreachable.** Port 47102 on mraemr.com does not accept TCP connections. The entire server (75.99.93.174) was offline as of 2026-02-16. No HTTP response of any kind can be obtained. (Verified via `curl -v` on 2026-02-16.)

2. **No alternative documentation exists anywhere.** The vendor's marketing website (mdchartsehr.com), the Wayback Machine, and search engines contain zero EHI export content. The documentation was never archived publicly.

3. **Mandatory disclosures are also unreachable.** The mandatory disclosures URL uses the same dead port 47102, indicating both required ONC public-facing documents are inaccessible.

4. **Infrastructure is fragile.** Hosting compliance documentation on a non-standard port (47102) from what appears to be a dynamic-DNS small-business server (noip.com mail, single IP) makes the documentation vulnerable to exactly this kind of outage.

5. **The product stores broad, deep data.** Based on product research, Physician's Solution is a full-featured EHR+PM+RCM platform covering clinical, billing, and specialty data across multiple specialties. A compliant (b)(10) export should cover dozens of data domains — but whether it does cannot be verified.

### Summary Stats

    Classification:  Minimal/stub (documentation inaccessible)
    Export format:   Unknown
    Model type:      Unknown
    Entities:        N/A
    Fields:          N/A
    Descriptions:    N/A
    Sample data:     No
    Bulk export:     Unknown
    Domains covered: 0 of 17 assessable (all unknown due to inaccessible documentation)

### Bottom Line

MD Charts' EHI export documentation is entirely inaccessible — the registered URL on port 47102 has been unreachable since at least 2026-02-14, and the server is now fully offline. No data dictionary, schema, sample data, or any documentation of the export exists in any publicly accessible location. For a product that stores extensive clinical, billing, and specialty data across multiple medical specialties, the complete absence of accessible (b)(10) documentation represents a fundamental compliance failure.
