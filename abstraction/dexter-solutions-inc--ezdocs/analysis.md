# EHI Export Analysis: Dexter Solutions Inc

**Product**: eZDocs v5.5
**Analysis date**: 2026-02-16
**CHPL IDs**: 15.02.04.2708.eZDo.05.02.1.240102 (CHPL ID 11432)

## 1. Product Context

eZDocs is a cloud-based ambulatory EMR/PM system developed by Dexter Solutions Inc, a small (~28 employees) healthcare IT company in Warrenville, Illinois. The product targets small to medium-sized medical practices and is delivered as a multi-tenant SaaS application (hosted at *.ezdocs.app subdomains). The current certified version is 5.5, certified by Drummond Group on 2024-01-02.

**Clinical workflows**: Patient demographics, problem lists, medication lists, allergies, clinical notes/encounters, vital signs, lab results/orders, diagnostic imaging orders/results, e-prescribing, implantable device lists, clinical decision support, smoking status, social history, family health history, immunizations, and specialty templates. The product was certified with internal medicine and neurology workflows but supports multiple specialties.

**Additional capabilities**: Scheduling and appointment management, insurance eligibility checking, DME ordering, Remote Patient Monitoring (RPM), Chronic Care Management (CCM), patient portal (eZHealthInfo), and clinical quality measures reporting.

**Billing/PM**: The product integrates with external billing systems, and the vendor also offers eZBill as a separate billing/RCM service. Login page code references "billing admin" roles, suggesting some billing functionality within eZDocs, but the extent of in-product billing data storage is unclear.

**Certification breadth**: 38 certified criteria including clinical data management (a)(1)–(a)(15), transitions of care (b)(1)–(b)(3), EHI export (b)(10), patient portal (e)(1), public health reporting (f)(1)–(f)(2), FHIR APIs (g)(7)–(g)(10), and direct messaging (h)(1). This is a comprehensive ambulatory EHR, not a narrow module.

## 2. Artifacts Reviewed

| Artifact | Description | Informative? |
|----------|-------------|-------------|
| `downloads/screenshot-certification-url-redirects-to-homepage.png` (1.5 MB) | Screenshot of dexter-solutions.com/certification showing it renders as the vendor homepage. Confirms navigation links (Home, Products, BPO Services, About, Contact) with no certification or compliance link. | **Low** — confirms documentation is absent |
| `downloads/screenshot-certification-url-full-page.png` (1.7 MB) | Full-page screenshot of the same homepage at /certification path. | **Low** — redundant with above |
| `product-research.md` | Prior research on eZDocs features, users, and data types. | **Medium** — establishes product context |
| `ehi-export-report.md` | Prior agent's narrative about the failed attempt to find documentation. | **Medium** — documents the search process |
| `files.json` | Manifest of downloaded artifacts (2 screenshots only). | **Low** — confirms minimal artifacts |
| `sources.json` | URLs visited during research (12 sources). | **Low** — documents research scope |
| `chpl-metadata.json` | CHPL certification details for eZDocs v5.5. | **Medium** — confirms (b)(10) certification and documentation URL |
| Wayback Machine captures (9 captures, 2022–2024) | Archived versions of the certification page. All show v5.0 (2019) content with (b)(6), never updated to v5.5 (b)(10). | **High** — most informative artifact; proves the page was never updated |

**No data dictionaries, schemas, sample data, export format specifications, or PDF documentation were available for review.**

## 3. Export Mechanics

**Format**: Unknown. The prior report references search engine snippets mentioning "CDA (XML) and PDF format," but this claim cannot be verified from any accessible artifact or Wayback Machine capture.

**Mechanism**: Unknown. No documentation describes how the export is initiated (UI button, API call, or vendor-assisted process).

**Single-patient vs bulk**: Unknown. The prior report references snippets mentioning "single patient and multiple patients," but this cannot be independently verified.

**Access constraints or fees**: Unknown. The archived certification page (which only covers v5.0/2019) does not mention EHI export. The v5.5 certification page content was never captured.

## 4. Export Content: What's In It

**No export content documentation is available.** The registered documentation URL (dexter-solutions.com/certification) redirects to the vendor's homepage after a Wix website rebuild. No data dictionary, schema, sample data, or export format specification exists in the available artifacts.

### What the Wayback Machine reveals

All 9 Wayback Machine captures of the certification page (spanning 2022-07-06 through 2024-08-04) show identical content: the **v5.0 certification page from December 2019**, listing (b)(6) Data Export — not (b)(10) EHI Export. Key observations:

- The March 2024 capture (3 months after the v5.5 certification date of 2024-01-02) still shows v5.0 content
- No (b)(10) documentation was ever visible on the archived page
- No downloadable PDF was linked or captured
- The page was rebuilt on Wix at some point between August 2024 and February 2026, and the certification path was dropped entirely

### What search engine caches suggested (unverifiable)

The prior report found search engine snippets describing: (1) "The attached document lists the details of exporting EHI data in CDA (XML) and pdf format for a single patient and multiple patients," and (2) a downloadable PDF titled "170.315 (b)(10) Electronic Health Information Export." However, this content was never captured by the Wayback Machine, and the prior report was also unable to retrieve the cached page or PDF. **These claims cannot be independently verified and are noted here only as unconfirmed leads.**

### Vendor's own content organization

Not applicable — no data dictionary or export content documentation exists.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

**Cannot be assessed.** No export documentation is available to determine what data domains the export covers. The only hint — unverifiable search engine snippets suggesting CDA/XML and PDF format — would, if true, indicate a C-CDA-based clinical summary rather than a comprehensive native data model export.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|--------|----------|----------------|--------------|
| Demographics | ❓ Unknown | No documentation available | Product stores this (certified (a)(5)); cannot assess export |
| Encounters / visits | ❓ Unknown | No documentation available | Product stores this; cannot assess export |
| Problems / conditions / diagnoses | ❓ Unknown | No documentation available | Product stores this (certified (a)(5)); cannot assess export |
| Medications / prescriptions | ❓ Unknown | No documentation available | Product stores this (certified (a)(1), (b)(3)); cannot assess export |
| Allergies | ❓ Unknown | No documentation available | Product stores this (certified (a)(1)); cannot assess export |
| Immunizations | ❓ Unknown | No documentation available | Product stores this (certified (f)(1)); cannot assess export |
| Vitals | ❓ Unknown | No documentation available | Product stores this; cannot assess export |
| Lab results | ❓ Unknown | No documentation available | Product stores this (certified (a)(2), (a)(3)); cannot assess export |
| Imaging / diagnostic reports | ❓ Unknown | No documentation available | Product stores this (certified (a)(3)); cannot assess export |
| Procedures | ❓ Unknown | No documentation available | Product likely stores this; cannot assess export |
| Clinical notes / documents | ❓ Unknown | No documentation available | Product stores this; cannot assess export |
| Care plans / goals | ❓ Unknown | No documentation available | Product may store this (CCM services); cannot assess export |
| Orders / referrals | ❓ Unknown | No documentation available | Product stores this (CPOE certified); cannot assess export |
| Insurance / coverage | ❓ Unknown | No documentation available | Product checks eligibility; may store limited data; cannot assess |
| Claims / billing | ❓ Unknown | No documentation available | Unclear if stored in eZDocs vs separate eZBill service; cannot assess |
| Payments | ❓ Unknown | No documentation available | Likely in separate eZBill service; may be N/A |
| Patient communications / portal messages | ❓ Unknown | No documentation available | Patient portal (eZHealthInfo) exists; cannot assess export |
| Specialty-specific (neurology, etc.) | ❓ Unknown | No documentation available | Product supports specialty templates; cannot assess export |

**Every domain is unknown** because no export documentation is available.

## 6. Documentation Quality

**There is no accessible documentation to assess.** The registered EHI documentation URL (dexter-solutions.com/certification) redirects to the vendor's marketing homepage. The Wayback Machine shows the page was never updated from the 2019 v5.0 certification to include v5.5 (b)(10) content.

- No data dictionary exists in any reviewed artifact
- No machine-readable schema or sample data is available
- No prose description of export format, content, or process is accessible
- A developer could not build an import tool from the available documentation because there is no documentation

This represents a **compliance violation**: 170.315(b)(10) requires that "the export format(s) used must be accessible via a publicly accessible hyperlink" (45 CFR 170.315(b)(10)(ii)(B)). The registered URL no longer serves this content.

## 7. Overall Assessment

### Classification

**Minimal/stub**: Documentation is completely inaccessible. The registered URL redirects to the vendor's homepage, and no export documentation, data dictionary, schema, or sample data was available at the time of analysis. The Wayback Machine confirms the certification page was never updated from v5.0/(b)(6) to v5.5/(b)(10).

### Key Findings

1. **Documentation URL is broken**: The registered CHPL documentation URL (dexter-solutions.com/certification) redirects to the Dexter Solutions marketing homepage after a Wix site rebuild. No certification, compliance, or EHI export content is accessible. (Verified via HTTP request returning `<title>Home | Dexter Solutions Inc.</title>` and screenshot in `downloads/screenshot-certification-url-redirects-to-homepage.png`.)

2. **Certification page was never updated for v5.5**: All 9 Wayback Machine captures (2022-07-06 through 2024-08-04) show the v5.0 (2019) certification page listing (b)(6) Data Export. The v5.5 certification (b)(10) content was never visible on the archived page, even 3+ months after the 2024-01-02 certification date.

3. **No data dictionary or export format specification exists in artifacts**: The `downloads/` folder contains only 2 screenshots. No PDF, HTML, JSON, XML, CSV, or any other format of export documentation was collected because none was available.

4. **Unverifiable hints suggest C-CDA repackaging**: The prior report found search engine snippets referencing "CDA (XML) and PDF format" for the export. If accurate, this would suggest the export is a C-CDA clinical summary rather than a native database export — covering only a fraction of the product's stored data. However, this cannot be independently confirmed.

5. **Active compliance gap**: The (b)(10) certification requirement mandates publicly accessible export format documentation. Dexter Solutions is currently not meeting this requirement, creating a regulatory compliance issue.

### Summary Stats

```
Classification:  Minimal/stub
Export format:   Unknown (unverified hints suggest CDA/XML + PDF)
Model type:      Unknown (likely standard projection if CDA/XML)
Entities:        N/A (no data dictionary)
Fields:          N/A
Descriptions:    N/A
Sample data:     No
Bulk export:     Unknown
Domains covered: 0 of 15+ applicable domains verifiable
```

### Bottom Line

No usable EHI export documentation is publicly available for eZDocs. The registered documentation URL redirects to the vendor's homepage, the Wayback Machine shows the certification page was never updated for the (b)(10) criterion, and no data dictionary, schema, or sample data exists in any accessible artifact. A patient or provider requesting their complete health data would have no way to understand what the export contains, in what format, or how to request it — assuming the export functionality even exists as documented.
