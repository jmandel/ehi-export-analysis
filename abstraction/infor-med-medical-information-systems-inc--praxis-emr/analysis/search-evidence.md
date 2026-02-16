# Praxis EMR EHI Export Documentation Search Evidence

## Date: 2026-02-15

## Summary
After exhaustive searching, **no publicly accessible EHI export documentation was found** for Praxis EMR (Infor-Med Medical Information Systems Inc.).

## Search Methodology

### 1. Vendor Website (praxisemr.com)
- Reviewed full sitemap.xml (70+ URLs) — no EHI export page found
- Checked robots.txt — disallows /downloads/clients_downloads, /manuals
- Probed common EHI documentation URL patterns:
  - /ehi-export, /ehi, /ehi-export-documentation, /b10, /b10-documentation
  - /EHI, /export-documentation, /downloads/ehi, /downloads/EHI
  - All returned 404
- Probed common PDF paths:
  - /downloads/EHI_Export_Documentation.pdf
  - /downloads/ehi-export-documentation.pdf
  - /downloads/EHI-Export.pdf
  - /downloads/b10-documentation.pdf
  - All returned 404
- Checked for Real World Testing documentation:
  - /real-world-testing, /rwt, /downloads/real-world-testing-plan.pdf
  - All returned 404
- Reviewed certification and costs page (certifications-and-costs.html) — lists criteria including b(10) but no link to export documentation
- Reviewed costs-and-limitations.html — no mention of EHI export
- Reviewed all feature pages — no EHI export documentation referenced

### 2. CHPL (Certified Health IT Product List)
- CHPL API requires API key — unable to query directly
- CHPL website (#/listing/10853) failed to render (blank page with only "Skip to main content")
- Confirmed CHPL product number: 15.02.05.2766.INFO.01.02.1.220310

### 3. Web Searches
- "Praxis EMR" EHI export documentation — no results
- "Infor-Med" EHI export documentation — no results
- "praxisemr.com" EHI export data dictionary — no results
- "Praxis EMR" "real world testing" — no results
- site:praxisemr.com EHI export — no results
- Multiple search variations all returned generic ONC information, not Praxis-specific documentation

### 4. Downloaded Artifacts
- ONC Certification certificate PDF (Infor-Med-Praxis-EMR-v9-5-ONC-Certified-Health-IT.pdf):
  Confirms b(10) certification but contains no export documentation details
- CMS EHR Certification ID document (ONC-Certification-Document.pdf):
  Lists certified criteria but no export documentation URL

## Regulatory Requirement
Per 170.315(b)(10)(ii)(A), certified health IT must:
> "Enable a user to set the format of the export to be either in a computable format consistent with all export format specifications and documentation requirements of § 170.315(b)(10) or in a human-readable format."

And per 170.315(b)(10)(ii)(B):
> "The developer must provide or make available through a publicly accessible hyperlink documentation describing the format of the export."

**Praxis EMR appears to be non-compliant with this public documentation requirement.**
