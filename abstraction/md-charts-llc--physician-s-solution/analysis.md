# EHI Export Analysis: MD Charts, LLC

**Product**: Physician's Solution  
**Analysis date**: 2026-02-16  
**CHPL IDs**: 15.99.09.2479.PH01.11.01.1.230117 (CHPL ID 11214)

## 1. Product Context

Physician's Solution by MD Charts, LLC is an all-in-one cloud-based EHR, practice management, and revenue cycle management platform for ambulatory practices. It holds Complete EHR certification (37 criteria including (b)(10)). The product is marketed under specialty-branded names — DermCharts (dermatology), KidsCharts (pediatrics), OBGYNCharts (OB-GYN) — but these are the same platform with specialty-specific templates. The SED intended user description is "Dermatology." The company has approximately 150+ implementations.

The product stores data across these domains relevant to EHI export completeness:

- **Clinical EHR**: Patient demographics, encounters, problem lists, medications, allergies, immunizations, vitals, lab orders/results (bidirectional with 20+ labs), clinical notes (100+ specialty templates), clinical images, e-prescribing, implantable device tracking, growth charts (pediatrics), biopsy tracking with BiopsyMapping™ and InstaPath℠ (dermatology)
- **Practice Management**: Scheduling, insurance eligibility verification, patient intake forms, inventory control, 300+ reports
- **Revenue Cycle Management / Billing**: Charge capture (Peak Charge Capture™), superbills (Smart Super Bill℠), claims submission and scrubbing, payment posting, denial management, A/R tracking, collections, text-to-pay (MDCPay™)
- **Patient Engagement**: Patient portal, secure messaging, educational materials, remote check-in, telehealth
- **Data Exchange**: C-CDA transitions of care, FHIR API (g)(10), public health reporting, referral/consult letters (AutoConsult Letters™)

This is a feature-rich product with deep billing, specialty clinical (dermatology), and practice management capabilities. A genuine (b)(10) export should cover all of these domains.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/screenshot-port-47102-unreachable.png` | Browser screenshot showing `ERR_ADDRESS_UNREACHABLE` for the registered EHI documentation URL on port 47102. 52 KB. | Confirms documentation inaccessibility |
| `downloads/screenshot-mraemr-cert-invalid.png` | Browser screenshot showing `ERR_CERT_DATE_INVALID` for mraemr.com standard port. 74 KB. | Shows expired SSL certificate on main domain |
| `downloads/screenshot-why-mdcharts-page.png` | Full-page screenshot of vendor's "Why MD Charts" page with ONC certification section. 1.5 MB. | Shows mandatory disclosures link also points to dead port 47102 |
| `files.json` | Manifest of collected artifacts | Documents collection attempt and results |
| `metadata.json` | Developer contact info, CHPL details, certified criteria list | Provides product and certification context |
| `chpl-metadata.json` | CHPL listing details including EHI documentation URL | Confirms registered URL |
| `product-research.md` | Detailed product research from vendor website | Establishes baseline of what the product stores |
| `ehi-export-report.md` | Prior agent's narrative about documentation collection attempt | Documents systematic search for documentation |
| `sources.json` | URLs visited during research | Documents search scope |

**No EHI export documentation artifacts exist.** All three downloaded files are screenshots documenting the inaccessibility of the registered documentation URL. There is no data dictionary, no schema, no sample data, no export guidance documentation of any kind in the collection.

## 3. Export Mechanics

**Unknown.** The registered EHI export documentation URL (`https://mraemr.com:47102/api/DataExportGuidance.asp`) is completely unreachable. The URL path suggests a Classic ASP page that would have provided export guidance documentation, but no information about the export format, mechanism, or access method is available.

- **Format**: Unknown
- **Mechanism**: Unknown
- **Single-patient vs bulk**: Unknown
- **Access constraints or fees**: Unknown

The product is certified for (b)(10) (certification date 2023-01-17), so an export capability presumably exists within the product, but its documentation is not publicly accessible as required.

## 4. Export Content: What's In It

**Cannot be assessed.** No export documentation, data dictionary, schema, or sample data is available for review. The registered documentation URL has been unreachable since at least the collection date (2026-02-14), confirmed by independent verification on 2026-02-16 (curl exit code 7 — connection refused on port 47102).

Verification steps performed:
1. Direct curl to `https://mraemr.com:47102/api/DataExportGuidance.asp` — connection refused (exit code 7)
2. Direct curl to `https://mraemr.com` standard port — also connection refused (exit code 7)
3. Wayback Machine search for `mraemr.com:47102/*` — empty results (no archived snapshots)
4. Wayback Machine search for `mraemr.com/api/DataExportGuidance*` — empty results
5. Vendor marketing site (`mdchartsehr.com/why-mdcharts/`) — still links to the dead port 47102 URL for mandatory disclosures; contains zero EHI export documentation

### Vendor's own content organization

N/A — No data dictionary or export documentation available.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

**Cannot be assessed.** No export documentation is available to determine what the vendor's (b)(10) export covers.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ❓ Unknown | No documentation accessible | Product stores demographics (certified (a)(5)); cannot assess export |
| Encounters / visits | ❓ Unknown | No documentation accessible | Product stores encounters; cannot assess export |
| Problems / conditions / diagnoses | ❓ Unknown | No documentation accessible | Product stores problem lists (certified (a)(1)); cannot assess export |
| Medications / prescriptions | ❓ Unknown | No documentation accessible | Product stores medications and e-prescribes (certified (a)(1)); cannot assess export |
| Allergies | ❓ Unknown | No documentation accessible | Product stores allergies (certified (a)(3)); cannot assess export |
| Immunizations | ❓ Unknown | No documentation accessible | Product stores immunizations (certified (f)(1)); cannot assess export |
| Vitals | ❓ Unknown | No documentation accessible | Product stores vitals; cannot assess export |
| Lab results | ❓ Unknown | No documentation accessible | Product has bidirectional lab integration with 20+ labs; cannot assess export |
| Imaging / diagnostic reports | ❓ Unknown | No documentation accessible | Product stores clinical images especially for dermatology; cannot assess export |
| Procedures | ❓ Unknown | No documentation accessible | Product stores procedures; cannot assess export |
| Clinical notes / documents | ❓ Unknown | No documentation accessible | Product has 100+ specialty templates; cannot assess export |
| Care plans / goals | ❓ Unknown | No documentation accessible | Cannot assess |
| Orders / referrals | ❓ Unknown | No documentation accessible | Product has AutoConsult Letters™ and CPOE; cannot assess export |
| Insurance / coverage | ❓ Unknown | No documentation accessible | Product does real-time eligibility verification; cannot assess export |
| Claims / billing | ❓ Unknown | No documentation accessible | Product has full RCM with claims, payments, denials, A/R; cannot assess export |
| Payments | ❓ Unknown | No documentation accessible | Product has payment posting and MDCPay™; cannot assess export |
| Consents / directives | ❓ Unknown | No documentation accessible | Product has electronic intake forms; cannot assess export |
| Patient communications / portal messages | ❓ Unknown | No documentation accessible | Product has patient portal; cannot assess export |
| Specialty-specific (Dermatology) | ❓ Unknown | No documentation accessible | Product has BiopsyMapping™, InstaPath℠, lesion tracking; cannot assess export |

**Every domain is unassessable** due to the complete absence of accessible documentation.

## 6. Documentation Quality

**The documentation is entirely inaccessible.** This represents the most fundamental failure mode possible:

- The registered CHPL URL (`https://mraemr.com:47102/api/DataExportGuidance.asp`) uses a non-standard port (47102) that is not accepting TCP connections
- The mandatory disclosures URL (`https://mraemr.com:47102/api/mandatory_disclosure.asp`) uses the same dead port
- The main domain (`mraemr.com`) also appears to have connectivity issues and has an expired SSL certificate
- No alternative documentation locations exist on the vendor's marketing website (`mdchartsehr.com`)
- No Wayback Machine archives capture the documentation
- No search engine results reference the documentation content

A developer cannot understand, use, or even discover the export from these docs because the docs do not exist in any publicly accessible form.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth**: **Minimal/stub/unclear**

The export documentation is completely inaccessible. There is zero public evidence of what the (b)(10) export contains. The product is certified for (b)(10), implying some export capability exists in the software, but without any accessible documentation, the coverage cannot be assessed. The hosting of documentation on a non-standard port (47102) that is now unreachable, with no backup on the marketing site or web archives, suggests this was not a robust, well-maintained compliance effort.

**Axis 2 — Export approach**: **Unclear/undetermined**

With no accessible documentation, it is impossible to determine whether MD Charts built a purpose-built EHI export or repackaged an existing clinical exchange export. The URL path (`DataExportGuidance.asp`) suggests there was at least a guidance page, but its contents are unknown. The product is certified for both (b)(10) and (g)(10) FHIR API, so either approach is possible, but no evidence exists to distinguish between them.

### Key Findings

1. **Documentation is completely unreachable.** The registered EHI export documentation URL on port 47102 returns connection refused. This was verified independently on 2026-02-16, confirming the prior agent's finding from 2026-02-14. No TCP connection can be established to the port.

2. **No alternative documentation exists anywhere.** The vendor's marketing site (mdchartsehr.com) contains an ONC certification section but zero EHI export content. No Wayback Machine archives, no Google-indexed pages, and no alternative URLs contain export documentation.

3. **Both required public URLs are dead.** The mandatory disclosures page (`mandatory_disclosure.asp`) uses the same dead port 47102 as the EHI documentation, meaning the vendor is non-compliant with two separate public documentation requirements.

4. **The product itself is feature-rich, making the documentation gap especially notable.** Physician's Solution is a comprehensive EHR with deep billing/RCM, specialty dermatology features (BiopsyMapping™, InstaPath℠), practice management, and patient engagement — a genuinely complex product. The absence of any public export documentation for such a product is a significant compliance gap.

5. **Fragile hosting architecture.** Hosting compliance documentation on a non-standard port (47102) on what appears to be the same server as the live EHR application (with dynamic DNS via noip.com) represents an inherently fragile approach to public documentation availability.

### Summary Stats

```
Coverage:        Minimal/stub/unclear
Approach:        Unclear/undetermined
Export format:   Unknown (documentation inaccessible)
Entities:        N/A
Fields:          N/A
Descriptions:    N/A
Sample data:     No
Bulk export:     Unknown
Domains covered: 0 of 19 assessable (all unknown due to inaccessible documentation)
```

### Bottom Line

Physician's Solution's EHI export documentation is completely inaccessible — the registered URL on a non-standard port returns connection refused, with no alternative locations, no web archives, and no fallback. Despite being a feature-rich ambulatory EHR with deep billing, dermatology specialty features, and practice management capabilities, there is zero publicly available evidence of what the (b)(10) export contains, how it works, or how to obtain it. This is a total documentation failure that makes the export entirely unassessable.
