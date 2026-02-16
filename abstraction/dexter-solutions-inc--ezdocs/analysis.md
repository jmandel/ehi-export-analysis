# EHI Export Analysis: Dexter Solutions Inc

**Product**: eZDocs v5.5
**Analysis date**: 2026-02-16
**CHPL IDs**: 15.02.04.2708.eZDo.05.02.1.240102 (CHPL ID 11432)

## 1. Product Context

eZDocs is a cloud-based ambulatory EMR/EHR and practice management system built by Dexter Solutions Inc, a small (~28 employee) healthcare IT company based in Warrenville, Illinois. It targets small to medium-sized medical practices, with particular focus on internal medicine and neurology, though the vendor claims multi-specialty support.

**Clinical capabilities** (per certified criteria and product research): Patient demographics, problem lists, medication lists, allergy lists, clinical notes/encounter documentation, vital signs, lab orders/results, diagnostic imaging orders/results, drug-drug/drug-allergy interaction checks, implantable device lists, clinical decision support, smoking status/social history, family health history, immunization records, e-prescribing, DME ordering, and clinical quality measures.

**Interoperability**: C-CDA document exchange (transitions of care), FHIR API access (g)(7)–(g)(10), Direct messaging, immunization registry submission, syndromic surveillance reporting.

**Practice management/billing**: The vendor also offers eZBill, a separate billing/revenue cycle management service. The login page references "billing admin" roles, suggesting some billing functionality may exist within eZDocs, but billing is primarily described as an integration or separate service.

**Patient portal**: eZHealthInfo (ezhealthinfo.com) for patient access to records, medication refill requests, and appointments.

**Remote monitoring**: RPM (Remote Patient Monitoring) and CCM (Chronic Care Management) modules.

For (b)(10) assessment, the export should cover at minimum the clinical data domains (demographics, problems, medications, allergies, vitals, labs, imaging, notes, immunizations, procedures, devices, prescriptions) and ideally any billing, RPM/CCM, and patient communication data stored within eZDocs itself.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/screenshot-certification-url-redirects-to-homepage.png` (1.5 MB) | Screenshot showing the registered certification URL (https://www.dexter-solutions.com/certification) renders as the vendor's homepage. 1920×1053 PNG. | **Key evidence** — documents that EHI export documentation is inaccessible |
| `downloads/screenshot-certification-url-full-page.png` (1.7 MB) | Full-page screenshot of the homepage at the /certification path. 1905×3678 PNG. Shows Dexter Solutions marketing site with navigation: Home, Products, BPO Services, About, Contact. No certification or EHI content. | **Confirmatory** — no certification content anywhere on the visible page |
| Wayback Machine capture (2024-08-04) | Archived version of the certification page at https://web.archive.org/web/20240804232517/https://dexter-solutions.com/certification. Contains the **old v5.0** certification from 2019 with (b)(6) Data Export — NOT the current v5.5 (b)(10) certification. No EHI export documentation, no data dictionary, no PDF link. | **Limited** — only documents the old certification, not the (b)(10) content |
| Live URL verification (2026-02-16) | Fetched https://www.dexter-solutions.com/certification; confirmed it returns Wix SPA shell with `<title>Home | Dexter Solutions Inc.</title>` — still the homepage. | **Confirmatory** — documentation is still inaccessible as of analysis date |

**No substantive EHI export documentation artifacts are available.** The downloads folder contains only two screenshots documenting the broken URL. No PDF, data dictionary, schema, sample data, or any other export documentation was collected or could be recovered.

## 3. Export Mechanics

**Cannot be determined from available evidence.**

Based on unverifiable search engine snippet evidence (from the prior agent's report), the export was described as:
- **Format**: CDA (XML) and PDF
- **Scope**: Single patient and multiple patients (bulk)
- **Documentation**: A downloadable PDF titled "170.315 (b)(10) Electronic Health Information Export" was reportedly linked from the certification page

However, I was unable to retrieve or verify any of this. The actual PDF document, its content, and the full text of the v5.5 certification page are not available from any source I checked (current website, Wayback Machine, web search, Google cache).

**Access mechanism**: Unknown. No documentation describes how a user initiates an export (UI button, API call, vendor-assisted request, etc.).

**Fees**: Unknown for (b)(10) specifically. The old v5.0 certification page mentions no additional cost for training/implementation for 1–10 provider practices.

## 4. Export Content: What's In It

**Cannot be assessed.** No data dictionary, schema, sample data, or export format documentation is available for review.

### Vendor's own content organization

No vendor-provided content organization is available to present.

The only indirect evidence comes from unverifiable search engine snippets suggesting the export uses "CDA (XML) and pdf format." If accurate, this would suggest the export is based on C-CDA (Consolidated Clinical Document Architecture), which is the same standard used for the vendor's existing (g)(6) Consolidated CDA Creation and (b)(1) Transitions of Care capabilities. This would be consistent with a repackaged clinical exchange export rather than a purpose-built EHI export.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

**Cannot be assessed.** No export documentation is available.

If the export is indeed C-CDA-based (per the unverifiable search engine snippets), it would likely be limited to the standard C-CDA clinical summary sections: demographics, problems, medications, allergies, vital signs, results, procedures, encounters, immunizations, and clinical notes. C-CDA does not natively represent billing data, RPM/CCM data, DME orders, patient portal communications, or many specialty-specific clinical data elements.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ❓ Unknown | No documentation available | Product stores demographics (certified (a)(5)); coverage cannot be verified |
| Encounters / visits | ❓ Unknown | No documentation available | Product stores encounter data; coverage cannot be verified |
| Problems / conditions | ❓ Unknown | No documentation available | Product stores problem lists (certified (a)(5)); coverage cannot be verified |
| Medications / prescriptions | ❓ Unknown | No documentation available | Product stores medications and e-prescribing data; coverage cannot be verified |
| Allergies | ❓ Unknown | No documentation available | Product stores allergy lists (certified (a)(5)); coverage cannot be verified |
| Immunizations | ❓ Unknown | No documentation available | Product stores immunization data (certified (f)(1)); coverage cannot be verified |
| Vitals | ❓ Unknown | No documentation available | Product stores vital signs; coverage cannot be verified |
| Lab results | ❓ Unknown | No documentation available | Product stores lab results (certified (a)(2)); coverage cannot be verified |
| Imaging / diagnostic reports | ❓ Unknown | No documentation available | Product stores imaging orders (certified (a)(3)); coverage cannot be verified |
| Procedures | ❓ Unknown | No documentation available | Coverage cannot be verified |
| Clinical notes / documents | ❓ Unknown | No documentation available | Product stores clinical notes; coverage cannot be verified |
| Care plans / goals | ❓ Unknown | No documentation available | Coverage cannot be verified |
| Orders / referrals | ❓ Unknown | No documentation available | Product stores orders (certified (a)(1)–(a)(3)); coverage cannot be verified |
| Insurance / coverage | ❓ Unknown | No documentation available | Product checks insurance eligibility; unclear how much coverage data is stored vs. passed through |
| Claims / billing | ❓ Unknown | No documentation available | Billing is primarily handled by separate eZBill service; some billing functionality may exist in eZDocs (login page references "billing admin" role) but scope is unclear |
| Payments | ❓ Unknown | No documentation available | Likely handled by eZBill, not eZDocs directly |
| Consents / directives | ❓ Unknown | No documentation available | Coverage cannot be verified |
| Patient communications | ❓ Unknown | No documentation available | Patient portal (eZHealthInfo) exists; unclear if portal messages are stored in eZDocs |
| RPM/CCM data | ❓ Unknown | No documentation available | Product has RPM/CCM modules; coverage cannot be verified |

**Gap analysis is impossible** without accessible documentation. Every domain is marked unknown because there is no evidence to evaluate.

## 6. Documentation Quality

**The documentation does not exist at its registered URL.** This is the most fundamental quality failure possible.

- The registered CHPL documentation URL (https://dexter-solutions.com/certification) redirects to the vendor's marketing homepage
- No certification page, EHI export documentation, data dictionary, or linked PDF is accessible
- The vendor rebuilt their website on Wix and did not migrate the certification content
- The Wayback Machine only captured the old v5.0 certification page (2019), which predates the v5.5 (b)(10) certification (2024-01-02) and does not contain EHI export documentation
- No alternative URL or location for the documentation could be found through web search

A developer, patient, or provider seeking to understand the EHI export format would find **nothing** at the published URL. They would need to contact the vendor directly (Rakesh Vedavyas, rakeshv@dexter-solutions.com, 630-219-1919) to obtain any information about the export.

This represents a **regulatory compliance violation**: 45 CFR 170.315(b)(10) requires that "the developer of certified health IT must publish documentation describing the format(s) used by the export and any additional data elements or structured data that are included in the export that are not expressed in a standard adopted by the Secretary" — and this documentation must be available at a publicly accessible hyperlink registered with the ONC.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth**: **Minimal/stub/unclear**

The documentation is entirely inaccessible. There is no way to assess what the export covers. The only indirect evidence (unverifiable search engine snippets) suggests the export uses C-CDA and PDF format, which would be consistent with a clinical summary export covering USCDI-scope data at most. Even taking those snippets at face value, there is no evidence of coverage beyond standard clinical domains — no billing, no RPM/CCM, no specialty data, no patient communications.

**Axis 2 — Export approach**: **Unclear/undetermined**

Without access to the actual documentation or the referenced PDF, it is impossible to determine whether this is a purpose-built EHI export or a repackaged existing export. However, the circumstantial evidence tilts toward repackaged: the snippet description of "CDA (XML) and pdf format" aligns exactly with what would be produced by the vendor's existing (g)(6) Consolidated CDA Creation capability — the same C-CDA documents used for transitions of care, repackaged as a (b)(10) export. The vendor is also certified for (g)(6) Consolidated CDA Creation and (b)(1) Transitions of Care, both of which produce C-CDA documents. A vendor who built a purpose-built EHI export covering data beyond C-CDA scope would likely describe it differently than "CDA (XML) and pdf format."

### Key Findings

1. **Documentation is completely inaccessible.** The registered certification URL (https://dexter-solutions.com/certification) redirects to the vendor's Wix marketing homepage. This is a regulatory compliance failure — the (b)(10) requirement mandates publicly accessible documentation.

2. **No documentation artifacts were recoverable.** The Wayback Machine only captured the old v5.0 certification page (with (b)(6), not (b)(10)). The v5.5 (b)(10) documentation PDF was never archived and could not be found through web search.

3. **Circumstantial evidence suggests a C-CDA-based export.** Search engine snippets (unverifiable) describe the export as "CDA (XML) and pdf format," which would be consistent with repackaging the vendor's existing C-CDA clinical summary capabilities rather than building a comprehensive EHI export.

4. **Small vendor with limited transparency.** Dexter Solutions is a ~28-employee company with a regional presence. Their website rebuild on Wix lost their certification content, and there is no evidence they have noticed or remedied this gap. No third-party reviews or coverage exist for eZDocs to provide alternative evidence about the product's export capabilities.

5. **Product scope includes domains unlikely to be in a C-CDA export.** eZDocs stores RPM/CCM data, DME orders, patient portal data, and potentially some billing data — none of which would be covered by a standard C-CDA export.

### Summary Stats

    Coverage:        Minimal/stub/unclear
    Approach:        Unclear/undetermined
    Export format:   Reportedly CDA (XML) and PDF (unverifiable)
    Entities:        N/A (no data dictionary available)
    Fields:          N/A
    Descriptions:    N/A
    Sample data:     No
    Bulk export:     Reportedly yes (single patient and multiple patients, per unverifiable snippets)
    Domains covered: 0 of 16+ applicable domains verifiable

### Bottom Line

No EHI export documentation is publicly accessible for eZDocs. The registered certification URL redirects to the vendor's homepage, and no documentation artifacts could be recovered from any source. This is both a regulatory compliance failure and a practical barrier: no patient, provider, or developer can understand what the eZDocs EHI export contains or how to use it. The single biggest issue is that the documentation simply does not exist at its published location.
