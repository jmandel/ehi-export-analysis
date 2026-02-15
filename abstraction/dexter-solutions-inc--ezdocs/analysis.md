# EHI Export Analysis: Dexter Solutions Inc

**Product**: eZDocs v5.5
**Analysis date**: 2026-02-15
**CHPL IDs**: 15.02.04.2708.eZDo.05.02.1.240102

## 1. Product Context

eZDocs is a cloud-based ambulatory EMR and practice management system developed by Dexter Solutions Inc, a small (~28-employee) HealthIT company based in Warrenville, Illinois. The product targets small to medium-sized medical practices across multiple specialties including internal medicine, neurology, cardiology, dermatology, and family medicine. It is delivered as a multi-tenant SaaS application (hosted at *.ezdocs.app subdomains).

**Clinical data stored**: Patient demographics, problems/conditions, medications, allergies, vital signs, lab results/orders, diagnostic imaging orders, clinical notes/encounters, implantable device list, smoking status/social history, family health history, immunizations, e-prescriptions, and clinical decision support data. The product is certified for 38 ONC criteria, confirming broad ambulatory EHR functionality.

**Additional capabilities**: Scheduling and appointment management, DME (Durable Medical Equipment) ordering, Remote Patient Monitoring (RPM), Chronic Care Management (CCM), a patient portal (eZHealthInfo), and public health reporting (immunization registries, syndromic surveillance).

**Billing**: The vendor offers a separate billing service (eZBill) and the EMR integrates with third-party billing systems. Login page code references "billing admin" roles, suggesting some billing functionality may exist within eZDocs itself, though the exact boundary is unclear.

**Interoperability**: Certified for C-CDA document exchange (b)(1)–(b)(3), FHIR APIs (g)(7)–(g)(10), and Direct messaging (h)(1).

**Baseline for export completeness**: A complete EHI export should cover clinical encounter data, medications, allergies, problems, labs, vitals, immunizations, clinical notes, e-prescriptions, DME orders, RPM/CCM data, patient portal data, and any billing data stored within eZDocs itself.

## 2. Artifacts Reviewed

| Artifact | Description | Informative? |
|---|---|---|
| `screenshot-certification-url-redirects-to-homepage.png` (1.55 MB) | Screenshot of `https://www.dexter-solutions.com/certification` showing the vendor's marketing homepage — "Transform your practice with Advanced IT Solutions." Navigation links: Home, Products, BPO Services, About, Contact. No certification or EHI content visible. | ❌ Confirms absence of documentation |
| `screenshot-certification-url-full-page.png` (1.76 MB) | Full-page screenshot of the same URL showing the complete homepage including footer. Footer links include HealthIT Products, BPO Services, About Us, Contact, Custom Software Development, Medical Billing, Revenue Cycle Management, Provider Credentialing. No certification page link anywhere. | ❌ Confirms absence of documentation |
| `files.json` | Manifest documenting the collection attempt: 2 files collected, access status "redirect_to_homepage" | ✅ Confirms collection scope |
| `chpl-metadata.json` | CHPL certification details: 38 certified criteria including (b)(10), certification date 2024-01-02, registered URL https://dexter-solutions.com/certification | ✅ Confirms certification status |
| `product-research.md` | Product research describing eZDocs features, modules, and data stored | ✅ Provides product context |
| `ehi-export-report.md` | Prior agent's report documenting the failed collection attempt | ✅ Provides collection narrative |

**No EHI export documentation, data dictionaries, schemas, sample data, or format descriptions were collected.** The registered certification URL redirects to the vendor's marketing homepage.

### Independent verification performed

1. **Current website (2026-02-15)**: Fetched `https://www.dexter-solutions.com/certification` — returns Wix SPA shell with `<title>Home | Dexter Solutions Inc.</title>`. The `/certification` path is not recognized by the Wix routing and falls through to the homepage. Confirmed: no certification content is accessible.

2. **Wayback Machine**: Retrieved all 9 captures of `dexter-solutions.com/certification` from 2022-07-06 through 2024-08-04. **Every capture shows the older eZDocs v5.0 certification page**, which references `170.315 (b)(6): Data Export` (the predecessor criterion), not `170.315 (b)(10)`. The v5.5 certification (dated 2024-01-02) with (b)(10) was apparently posted to the same URL after the v5.0 content but was never captured by the Wayback Machine before the site was rebuilt on Wix.

3. **Web search**: Search engine snippets consistently describe the v5.5 certification page as referencing "exporting EHI data in CDA (XML) and pdf format for a single patient and multiple patients" and linking to a downloadable PDF titled "170.315 (b)(10) Electronic Health Information Export." However, neither the page content nor the PDF is recoverable from any cached source.

## 3. Export Mechanics

**Cannot be fully assessed** — no export documentation is accessible.

Based solely on search engine snippet reconstruction (not verified from primary sources):
- **Format**: CDA (XML) and PDF
- **Scope**: Single-patient and multi-patient (bulk) export
- **Mechanism**: Unknown (UI button, admin function, or vendor-assisted — not determinable)
- **Access constraints**: Unknown; the prior certification page mentioned API access via email to info@dexter-solutions.com
- **Fees**: Unknown

## 4. Export Content: What's In It

**Cannot be assessed.** No data dictionary, schema, sample data, or format documentation is accessible for review.

### What search engine snippets suggest (unverified)

The only evidence about export content comes from search engine snippets, which are insufficient for a rigorous assessment:

- The export reportedly uses **CDA (XML) format**, which strongly suggests C-CDA (Consolidated Clinical Document Architecture). If so, the export would represent a **standard-based projection** covering a clinical summary subset (demographics, problems, medications, allergies, vitals, labs, immunizations, procedures, clinical notes) but likely omitting:
  - Billing/claims data (not representable in C-CDA)
  - DME ordering data
  - RPM/CCM data
  - Custom specialty templates
  - Insurance eligibility data
  - Patient portal interaction data

- The export also reportedly includes **PDF format**, which provides human-readable output but is not computable — raising questions about whether the "computable format" requirement of (b)(10) is met solely through the CDA portion.

- A **downloadable PDF** was reportedly linked from the certification page describing the export format, suggesting at least some documentation existed. Its depth and quality cannot be evaluated.

### Vendor's own content organization

Not available — no data dictionary or entity listing exists in the collected artifacts.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

**Cannot be assessed from available artifacts.** No export documentation is accessible to determine what data domains are covered, how many entities/tables/fields are exported, or what level of detail is provided.

The only signal is the search engine snippet reference to "CDA (XML) and PDF format," which, if taken at face value, suggests a C-CDA-based clinical summary rather than a native database export.

### 5b. Standardized domain coverage (top-down)

Without accessible documentation, coverage can only be inferred speculatively from the reported CDA/PDF format. The table below uses "❓ Unknown" for most domains because no primary evidence exists.

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ❓ Unknown | Likely in CDA if C-CDA is used, but unverified | Product stores this (a)(5) certified |
| Encounters / visits | ❓ Unknown | Likely in CDA if C-CDA is used | Product stores this; core clinical function |
| Problems / conditions | ❓ Unknown | Likely in CDA if C-CDA is used | Product stores this (a)(5) certified |
| Medications / prescriptions | ❓ Unknown | Likely in CDA if C-CDA is used | Product stores this (a)(1), (b)(3) certified |
| Allergies | ❓ Unknown | Likely in CDA if C-CDA is used | Product stores this (a)(1) certified |
| Immunizations | ❓ Unknown | Likely in CDA if C-CDA is used | Product stores this (f)(1) certified |
| Vitals | ❓ Unknown | Likely in CDA if C-CDA is used | Product stores this |
| Lab results | ❓ Unknown | Likely in CDA if C-CDA is used | Product stores this (a)(2), (a)(3) certified |
| Imaging / diagnostic reports | ❓ Unknown | May be partially in CDA | Product stores this (a)(3) certified |
| Procedures | ❓ Unknown | Likely in CDA if C-CDA is used | Product stores this |
| Clinical notes / documents | ❓ Unknown | Likely in CDA if C-CDA is used | Product stores this; core clinical function |
| Care plans / goals | ❓ Unknown | Unknown | RPM/CCM modules likely generate care plans |
| Orders / referrals | ❓ Unknown | May be partially in CDA | Product stores this (CPOE certified) |
| Insurance / coverage | ❓ Unknown | Unlikely if CDA-only | Product stores insurance eligibility data |
| Claims / billing | ❓ Unknown | Unlikely if CDA-only; C-CDA cannot represent billing | Unclear if billing data is in eZDocs vs. eZBill |
| Payments | ❓ Unknown | Unlikely if CDA-only | Same ambiguity as billing |
| Patient communications / portal | ❓ Unknown | Unlikely if CDA-only | Product has patient portal (eZHealthInfo) |
| RPM/CCM data | ❓ Unknown | Unlikely if CDA-only; no standard CDA representation | Product has RPM and CCM modules |
| DME orders | ❓ Unknown | Unlikely if CDA-only | Product has DME ordering capability |

## 6. Documentation Quality

**No documentation is accessible for evaluation.**

- The registered certification URL (`https://dexter-solutions.com/certification`) redirects to the vendor's marketing homepage.
- The Wayback Machine's 9 captures (2022–2024) all show the older v5.0 certification page with (b)(6) Data Export — the v5.5 (b)(10) page was never archived.
- Search engine snippets confirm a documentation PDF previously existed but it cannot be recovered.
- A developer cannot build an import from the available materials. There are no schemas, no field definitions, no sample data, and no format specifications accessible anywhere.

This represents a **compliance violation**: 170.315(b)(10) requires that "a description of the format used to create the export file(s) that is accessible via a publicly accessible hyperlink." The registered URL no longer serves this documentation.

## 7. Overall Assessment

### Classification

**Minimal/stub**: The EHI export documentation is entirely inaccessible. The registered certification URL redirects to the vendor's marketing homepage, and the previously published documentation (a PDF describing CDA/XML and PDF export) cannot be recovered from any public source. The fragmentary evidence from search engine snippets suggests the export may be a C-CDA-based clinical summary (standard-based projection) rather than a comprehensive native data model export, but this cannot be confirmed.

### Key Findings

1. **Documentation completely inaccessible**: The registered URL (`https://dexter-solutions.com/certification`) redirects to the vendor's Wix-hosted marketing homepage. The certification page and linked PDF were lost during a site rebuild. No EHI export documentation exists at any publicly accessible URL. (Verified: `screenshot-certification-url-redirects-to-homepage.png`, `screenshot-certification-url-full-page.png`, and independent fetch on 2026-02-15.)

2. **Wayback Machine shows only older certification**: All 9 Wayback Machine captures (2022-07-06 through 2024-08-04) show the v5.0 certification with (b)(6) Data Export, not the current v5.5 certification with (b)(10) EHI Export. The (b)(10) documentation was posted after the last capture and removed before being re-captured. (Verified: `analysis/wayback_verification.json`)

3. **Export likely CDA-based (unverified)**: Search engine snippets describe the export as "CDA (XML) and PDF format," suggesting a standard-based projection. If accurate, this would cover clinical summary data but likely miss billing, RPM/CCM, DME ordering, insurance, and patient portal data that eZDocs stores.

4. **Active compliance violation**: The (b)(10) certification requirement mandates publicly accessible format documentation. The vendor is currently not meeting this requirement, creating a gap for any practice or patient trying to understand what an EHI export from eZDocs contains.

5. **Small vendor with limited transparency**: Dexter Solutions is a ~28-employee company with limited web presence. The rebuilt Wix site contains only marketing content. No alternative documentation locations (product docs, knowledge base, support portal) were found.

### Summary Stats

```
Classification:  Minimal/stub
Export format:   CDA (XML) and PDF (per search engine snippets; unverified)
Model type:      Standard projection (likely C-CDA; unverified)
Entities:        N/A (no data dictionary accessible)
Fields:          N/A
Descriptions:    N/A
Sample data:     No
Bulk export:     Reportedly yes (single and multiple patients; unverified)
Domains covered: 0 of 15+ applicable domains verified (all unknown)
```

### Bottom Line

No EHI export documentation is publicly accessible for eZDocs. The registered certification URL redirects to the vendor's marketing homepage, and neither the certification page nor the linked export format PDF can be recovered from any cached or archived source. A patient or provider requesting their complete health data from eZDocs would have no publicly available documentation to understand what they would receive, and the fragmentary evidence suggests the export may be limited to a C-CDA clinical summary — far short of "all electronic health information" the product stores.
