# Phase 2: Download EHI Export Documentation

You are downloading the EHI (Electronic Health Information) export documentation
for a certified EHR product. Your job is to find, navigate, and download
everything at the vendor's registered documentation URL — producing a complete,
reproducible archive of their export documentation.

## Your Target

**URL**: {{URL}}
**Developer(s)**: {{DEVELOPERS}}
**Product(s)**: {{PRODUCTS}}
**CHPL IDs**: {{CHPL_IDS}}

**Output directory**: {{OUTPUT_DIR}}
**Downloads directory**: {{OUTPUT_DIR}}/downloads/

**CHPL metadata**: `{{OUTPUT_DIR}}/chpl-metadata.json`
**Product research**: `{{OUTPUT_DIR}}/product-research.md` — read this first if it exists.
A prior research agent investigated this vendor and product. Their findings will
give you useful context about what data this product stores, who uses it, and
what to expect from the export documentation.

## What To Download

Everything at the registered URL that documents the EHI export. This includes:

- **Data dictionaries** — table/field definitions, schemas, column listings
- **Export format specifications** — file formats, encoding, structure
- **API documentation** that is specific to this vendor's EHI export mechanism —
  if the b(10) export itself works via an API, get those docs
- **Sample data / examples** — example export files, sample records, test data
- **Schema files** — XSD, JSON Schema, OpenAPI specs, DDL, anything machine-readable
- **Instructions / user guides** for performing the export
- **Screenshots** of export interfaces (take them yourself if the page shows one)

### What NOT to download

- **External standards documentation** — don't follow links to hl7.org, fhir.org,
  build.fhir.org, uscdi.healthit.gov, etc. We already understand those standards.
- **Marketing materials** — unless they contain substantive EHI export information
- **Compliance certificates** — unless they contain technical export details
- **Unrelated regulatory documents** — real-world testing plans, SVAP notices, etc.
  unless they describe the export mechanism

### The (b)(10) vs (g)(10) confusion

A very common pattern: a vendor's "EHI export documentation" is actually just
their FHIR Bulk Data API documentation repackaged. This conflates two different
ONC requirements:

- **170.315(g)(10)** requires a standardized FHIR API exposing US Core data.
  This covers a defined subset of clinical data — USCDI data classes like
  problems, medications, allergies, labs, vitals, etc.
- **170.315(b)(10)** requires export of **all electronic health information**
  the product stores — not just US Core, not just USCDI, but *everything*
  in the designated record set: billing, images, custom forms,
  specialty-specific clinical data, and more. (See the EHI scope
  reference below for what "designated record set" includes and excludes.)

The (b)(10) export doesn't need to be FHIR. It doesn't need to be standardized
at all. A SQL dump or CSV export of every table would satisfy the requirement
better than a polished FHIR API that only covers 20% of the data.

When you find a vendor pointing to their FHIR Bulk Data endpoint as their EHI
export, ask: does this actually cover everything? Or is it just the US Core
slice? Look for signs:
- The documentation only mentions US Core / USCDI resource types
- There's no mention of billing or specialty-specific clinical data
- The export endpoint is the same as their (g)(10) certified API
- The data dictionary (if any) maps only to standard FHIR resources

This is not necessarily bad faith — many vendors genuinely don't understand
the distinction. But it's a critical finding for the coverage assessment.
A vendor that has done real (b)(10) work will have documented how they export
data that *doesn't* fit neatly into FHIR US Core.

{{EHI_SCOPE_REFERENCE}}

### Staying focused: let the export docs guide you

EHI export documentation often lives on a larger certification or compliance
page alongside other vendor documentation — FHIR API portals, regulatory
filings, product feature pages. Your job is the EHI export, not everything else.

The way to stay focused is to **let the export documentation itself tell you
what's relevant.** Once you find the core EHI export docs (a PDF, a data
dictionary page, a download link), read them enough to understand the export
format. That understanding tells you what else you need:

- If the export is CSV files with a data dictionary, you probably have
  everything you need in that dictionary. You don't need to go explore the
  vendor's FHIR API docs — that's a different system.
- If the export documentation says "exports are in FHIR NDJSON format using
  our custom profiles," then yes, you need the profile/IG documentation to
  understand the export. Follow those links.
- If the data dictionary references a separate schema document or format
  spec hosted elsewhere on the vendor's site, follow that link.

The principle: follow what you need to understand the export. Don't follow
everything that happens to be nearby on the same page. A certification page
might link to both "EHI Export Data Dictionary" and "FHIR API Developer
Portal" — those are different things, and only the first is your job unless
the export docs tell you otherwise.

### Prefer computable formats

When a document is available in multiple formats, prefer the most computable:
- JSON/YAML/XML schema over PDF description of the same schema  
- CSV/TSV data dictionary over PDF table
- HTML with structured tables over a scanned PDF
- If only PDF exists, that's fine — download it

If a ZIP contains structured files (HTML data dictionary, CSV exports, etc.),
download and extract it.

### Always look for the underlying data

When navigating a vendor's documentation site — especially custom-built doc
portals, wikis, or SPA-based sites — don't just scrape the rendered text from
web pages. Look for ways to download the underlying structured data:

- **Downloadable files**: CSV, JSON, XML, XLSX, ZIP, YAML, XSD, OpenAPI specs
- **FHIR endpoints**: if the vendor exposes a FHIR server, grab machine-readable
  artifacts like CapabilityStatement, StructureDefinitions (custom profiles),
  ImplementationGuide packages — not prose descriptions of standard resources
- **API endpoints**: if the doc site has an API or data endpoint behind it,
  prefer that over scraping rendered HTML
- **Export/download buttons**: many doc sites have "Download as PDF", "Export
  data dictionary", or "Download ZIP" options — use those

The goal is computable artifacts, not screenshots and text extractions of
web pages. A JSON schema is worth more than a text scrape of the page that
describes the same schema.

### Required enrichment for large documentation corpora

If you collect a substantial set of HTML/docs (for example many extracted
model pages like `.../mysql-model/html/*.html`), do not stop at raw files.
You must produce a reproducible enrichment pass that extracts the underlying
content into queryable JSON.

Create:
- `{{OUTPUT_DIR}}/downloads/enrichment/`

Inside that folder, include:
- One or more Bun TypeScript scripts that perform the extraction
  (for example `extract-*.ts`).
- A short `README.md` with:
  - exact run command(s)
  - input boundary (which files were parsed)
  - output files produced
  - known parsing limitations
- Extracted JSON artifacts that are complete and queryable (not just ad-hoc
  snippets).

Minimum enrichment expectations:
- Parse all in-scope files in the corpus, not just a sample.
- Emit machine-queryable structures for core documentation content
  (entities/models, fields/columns, relationships/references, value sets/codes,
  and source-page linkage where available).
- Emit coverage/accounting output:
  - total files discovered
  - total files parsed
  - parse failures with file paths and error reasons
- Keep transformations deterministic and rerunnable from local artifacts only.

This enrichment output is part of the deliverable, not optional analysis scratch.

## How To Navigate

### Step-by-step process:

**1. Initial probe — what does the URL return?**
```bash
curl -sI -L "$URL" -H 'User-Agent: Mozilla/5.0' 2>&1
```
Record: HTTP status chain, final URL, Content-Type, content-disposition headers.
If it's a direct file download, grab it and you're nearly done.

**2. Fetch and examine the page:**
```bash
curl -sL "$URL" -H 'User-Agent: Mozilla/5.0' -o /tmp/page.html
wc -c /tmp/page.html
cat /tmp/page.html | sed 's/<[^>]*>/ /g' | tr -s ' \n' | head -50
```

**3. Search for documentation links:**
```bash
grep -oiE 'href="[^"]*\.(pdf|zip|xlsx|xls|csv|json|doc|docx|yaml|yml)[^"]*"' /tmp/page.html
grep -oiE 'href="[^"]*[^"]*"' /tmp/page.html | grep -iE 'ehi|export|data.dictionary|b.10|bulk'
```

**4. If the page is a SPA or needs JavaScript:**
- Navigate in the browser, wait for load, take a screenshot
- Note what you see and what you had to click

**5. If the page is a compliance hub with accordions/tabs:**
- Look for sections labeled "170.315(b)(10)", "EHI Export", "Electronic Health Information"
- Check page source for hidden content in collapsed sections
- Click to expand, record what heading you expanded

**6. Follow links one or two levels deep:**
Record each hop: "From the main page, I clicked X which led to Y"

**7. Check certification dates in chpl-metadata.json.**
If the product was certified very recently (last few months), missing or
incomplete documentation is common — note this in your log but still
investigate thoroughly.

**8. If the URL is dead (404, domain expired, redirects to homepage):**
Try:
- Domain root, search for EHI docs
- Common paths: /legal/, /compliance/, /onc/, /ehi/, /interoperability/
- Wayback Machine: `curl -s "https://web.archive.org/web/2024*/{{URL}}"`
- Google: `curl -s "https://www.google.com/search?q=site:DOMAIN+EHI+export"`
Record everything you tried.

### Patterns you'll encounter:

| Pattern | What to do |
|---------|------------|
| Direct file download (PDF/ZIP) | Download it, done |
| Static HTML + download links | Download all linked files |
| Compliance hub with accordion | Find and expand EHI section, download linked files |
| JavaScript SPA | Use browser, screenshot, download what you can |
| Multi-page HTML doc site | Download index + representative pages (prefer ZIP if available) |
| Dead/moved URL | Investigate alternatives, document what you tried |
| Login wall | Document it as a finding — this violates the public accessibility requirement |

### Anti-bot notes:
- Some sites need a User-Agent header
- WordPress sites may use lazy-loading JS
- Accordion content is often in HTML source but hidden via CSS
- If curl gets HTML instead of expected file, try different Accept headers

### Verify every download
- After downloading a file, confirm it's what you expected: `file filename.pdf`
  should say "PDF document", not "HTML document" or "ASCII text"
- For JSON files, check the first few hundred bytes: `head -c 500 file.json` —
  make sure it's actual data, not an error response or auth redirect
- Some servers return HTTP 200 with an error message in the body (e.g., a
  login page, a JSON error object, or a "401 Unauthorized" HTML page). Don't
  trust the status code alone — inspect the content.
- If a download requires authentication, note it in the collection log and
  don't include it in the downloads. The documentation is supposed to be
  publicly accessible.

### Examining PDFs
PDFs are common for EHI export documentation. To understand what's in them:

```bash
# Basic info: page count, title, author
pdfinfo filename.pdf

# Extract text (works well for text-based PDFs)
pdftotext filename.pdf - | head -100

# Render a page as image (useful for complex layouts, tables, diagrams)
pdftoppm -f 1 -l 1 -r 150 -png filename.pdf /tmp/page-preview
# Then view the image with your image tools
```

Use `pdftotext` first. If the extracted text is garbled or missing structure
(common with scanned documents or complex table layouts), render a few sample
pages as images to understand the content visually.

Also check whether the PDF points to additional material (links, attachments),
so you don't miss follow-on artifacts:

```bash
# Find clickable URLs embedded in PDF objects (not just visible text)
pdfinfo -url filename.pdf

# Check for embedded files/attachments inside the PDF
pdfdetach -list filename.pdf

# Extract plain-text URLs from the PDF text layer
pdftotext filename.pdf - | rg -No 'https?://[^[:space:]>)"]+' | sort -u
pdftotext filename.pdf - | rg -No 'www\\.[^[:space:]>)"]+' | sort -u
```

Interpretation examples:
- If `pdfinfo -url` is empty and `pdfdetach -list` says `0 embedded files`,
  there are no embedded follow-on artifacts in that PDF.
- Build a concrete URL checklist in your notes:
  `url -> destination title/type -> relevant to EHI export? yes/no + why`
- If the PDF says things like "See detailed guide" but gives no URL and no
  attachment, record that as a documentation gap in your report.

Note in the collection log what the PDF contains — a data dictionary with N
tables? Export instructions? A schema diagram? This context helps Phase 3.

## Output

Two files: a narrative report and a file manifest.

### `{{OUTPUT_DIR}}/ehi-export-report.md`

This is the primary deliverable. It combines the collection journal, analysis
of what was found, and a coverage assessment informed by the product research.

**Start by reading `{{OUTPUT_DIR}}/product-research.md`** if it exists. The
product research tells you what data this product stores. As you examine the
export documentation, think about what's covered and what's missing.

```markdown
# {{Vendor Name}} — EHI Export Documentation

Collected: {{date}}

## Source
- Registered URL: {{url}}
- CHPL IDs: ...

## Navigation Journal
(How you found and accessed the documentation. Be reproducible — include
curl commands, clicks, expanded accordions. Someone should be able to
follow your steps and get the same files.)

## What Was Found
(Describe what the export documentation says. What format is the export?
What data does it include? Is there a data dictionary, schema, API spec?
How detailed is it? Summarize the substance — don't just list filenames,
explain what the documentation tells you about the export.)

## Export Coverage Assessment

This is the most important section. It's why we did the product research
first. Assess the export along several dimensions:

### Data Domain Coverage
- What data domains from the product research are clearly covered?
- What domains appear to be missing or not mentioned?
- Does the export describe a bulk export of *everything*, or a narrow
  subset like a patient summary or clinical data only?
- Are there ambiguities — domains where you can't tell?
- Be specific. Name the domains. "Billing data is absent" not "some data
  is missing."

### Export Format & Standards
- What format does the export use? (FHIR, C-CDA, CSV, SQL dump, proprietary
  XML, PDF, etc.)
- Is it a recognized standard or an ad-hoc vendor format?
- If FHIR: which resources, what profile constraints, what version?
- If CSV/database dump: how are relationships between tables expressed?
- Is the format appropriate for the data? (e.g., a FHIR IPS for a product
  that stores radiation therapy physics data is a mismatch)
- Could a third party actually reconstruct the patient record from this
  export, or is critical context missing?

### Documentation Quality
- How readable and navigable is the documentation?
- Is there a clear data dictionary with field-level definitions?
- Are data types, value sets, and constraints specified?
- Are there worked examples or sample export files?
- Could a developer implement an import of this data based solely on
  the documentation?
- Is the documentation clearly maintained, or does it look like a
  compliance checkbox?

### Structure & Completeness
- How granular is the field-level documentation? (just table names?
  field names? data types? descriptions? cardinality?)
- Are coded fields documented with their value sets?
- Are relationships between entities documented?
- Is there versioning or change history?

Don't just answer these as a checklist — write a narrative assessment
that paints a picture of how well this vendor has approached EHI export.

## Access Summary
- Final URL (after redirects): ...
- Status: found | dead | redirect_to_homepage | login_required
- Required browser: yes/no
- Navigation complexity: direct_link | one_click | accordion | multi_page
- Anti-bot issues: none | user-agent required | cloudflare | etc.

## Obstacles & Dead Ends
(anything that didn't work, special headers needed, etc.)
```

### `{{OUTPUT_DIR}}/files.json`

A manifest of everything you downloaded:

```typescript
interface FilesManifest {
  collection_date: string;                   // ISO date
  url: string;                               // registered URL from CHPL
  final_url: string;                         // after redirects
  access_status: "found" | "dead" | "redirect_to_homepage" | "login_required";
  files: Array<{
    path: string;                            // local path relative to output dir
    source_url: string;                      // where it came from
    size_bytes: number;
    description: string;                     // what this file is and why it matters
    curl_command: string | null;             // reproducible download command
  }>;
}
```

Include everything you saved: docs, screenshots, evidence of dead pages.
Include enrichment scripts and enrichment JSON outputs under
`downloads/enrichment/`.

## Mindset

- **Reproducibility is the goal.** Someone should be able to follow your log and
  get the same files. Every curl command, every click, every expanded accordion.
- **Be persistent.** If a URL 404s, investigate. If a page looks empty, view source.
  If an accordion is collapsed, check if content is in the DOM.
- **Download generously, but stay on-topic.** Get everything that documents the
  EHI export. Skip unrelated regulatory filings.
- **Prefer computable formats.** If there's a JSON schema AND a PDF describing
  the same thing, get both but note the JSON is the primary artifact.
- **When docs are large, normalize them.** Build a rerunnable Bun+TypeScript
  enrichment step and deliver the script + JSON outputs in
  `downloads/enrichment/` so downstream analysis can query the full corpus.
- **Capture obstacles.** Did you need special headers? Did Cloudflare block you?
  This information is as valuable as the docs themselves.
- **Be proportionate.** Single PDF with clean link? 2 minutes. Complex multi-page
  site with buried docs? Take the time. Dead URL? Check Wayback Machine,
  try a few obvious alternative paths, do a web search, and move on — don't
  exhaustively probe every subdomain and sitemap. The difficulty is itself a finding.
