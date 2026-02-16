# MD Charts, LLC — EHI Export Documentation

Collected: 2026-02-14

## Source
- Registered URL: https://mraemr.com:47102/api/DataExportGuidance.asp
- CHPL IDs: 11214
- Product: Physician's Solution (version 11)
- Certification date: 2023-01-17
- Developer: MD Charts, LLC

## Navigation Journal

### Step 1: Initial probe of registered URL (port 47102)

```bash
curl -sI -L "https://mraemr.com:47102/api/DataExportGuidance.asp" -H 'User-Agent: Mozilla/5.0' --connect-timeout 15 --max-time 30 -k 2>&1
```

**Result:** Connection refused (exit code 7). Port 47102 on mraemr.com is completely unreachable — no TCP connection can be established.

Verified with bash /dev/tcp probe:
```bash
timeout 10 bash -c 'echo >/dev/tcp/mraemr.com/47102' 2>&1
# Result: "No route to host"
```

Also attempted in Chrome browser — received `net::ERR_ADDRESS_UNREACHABLE`.

### Step 2: DNS verification

```bash
host mraemr.com
# mraemr.com has address 75.99.93.174
# mraemr.com mail is handled by 5 mx.noip.com.
```

The domain resolves to 75.99.93.174. Note the use of noip.com for mail, suggesting a dynamic DNS or small-business hosting setup.

### Step 3: Test mraemr.com on standard ports

```bash
curl -sI -L "https://mraemr.com" -H 'User-Agent: Mozilla/5.0' -k 2>&1
# HTTP/2 200, Content-Type: text/html; charset=windows-1251, Server: Microsoft-IIS/10.0
```

The standard HTTPS port (443) on mraemr.com is alive and serves the EHR application's login page. The page title is "Login" and shows "Licensed to: ABC Dermatology" and "Version 12.0 Oct 2024". This is the live EHR application, not public documentation.

The browser could not reach the standard port either due to an expired/invalid SSL certificate (`net::ERR_CERT_DATE_INVALID`), though curl with `-k` succeeds.

### Step 4: Test DataExportGuidance path on standard port

```bash
curl -sL "https://mraemr.com/api/DataExportGuidance.asp" -H 'User-Agent: Mozilla/5.0' -k
# {"Message":"No HTTP resource was found that matches the request URI 'https://mraemr.com/api/DataExportGuidance.asp'.",
#  "MessageDetail":"No type was found that matches the controller named 'DataExportGuidance.asp'."}
```

The `/api/` path on the standard port runs a different framework (ASP.NET Web API) that doesn't have this route. The DataExportGuidance.asp was a Classic ASP page served only on port 47102.

```bash
curl -sL "https://mraemr.com/DataExportGuidance" -H 'User-Agent: Mozilla/5.0' -k
# Returns the EHR login page (title: "Login")
```

Without the `/api/` prefix, it redirects to the login page — the application catches all unrecognized paths.

### Step 5: Probe common alternative paths

Tested 12 common paths (`/ehi`, `/ehi-export`, `/b10`, `/export`, `/data-export`, `/interoperability`, `/compliance`, `/disclosures`, `/onc`, `/documentation`, `/api/EhiExport`, `/api/data-export`). The non-API paths all return HTTP 200 with the login page. The `/api/` paths return proper 404s from the Web API framework. None contain EHI documentation.

### Step 6: Wayback Machine

```bash
curl -s "https://web.archive.org/cdx/search/cdx?url=mraemr.com:47102/*&output=json&limit=20"
# Result: [] (empty array — no captures)
```

No Wayback Machine snapshots exist for any page on mraemr.com:47102. Only 4 captures of the root domain (mraemr.com) exist, from 2016–2025, all showing the login/root page.

### Step 7: Google and web search

- `site:mraemr.com DataExportGuidance` — no results
- `"MD Charts" "EHI export"` — no results specific to MD Charts
- `mraemr.com "47102" DataExportGuidance` — no results
- Google cache of the target URL — not available

### Step 8: Vendor's marketing website (mdchartsehr.com / mdcharts.net)

The vendor's public website at mdchartsehr.com (mdcharts.net redirects there) is a WordPress marketing site. Examined all pages:

- **Homepage** (mdchartsehr.com) — product marketing, no compliance/EHI section
- **"Why MD Charts" page** (mdchartsehr.com/why-mdcharts/) — contains an "MD Charts is ONC Certified" section at the bottom, which:
  - Links to the CHPL listing (https://chpl.healthit.gov/#/listing/11214)
  - Links to mandatory disclosures at `https://mraemr.com:47102/api/mandatory_disclosure.asp` — same dead port 47102
  - Links to healthit.gov for ONC info
  - Contains no EHI export documentation, data dictionary, or export-related content

No page on mdchartsehr.com contains any reference to EHI export, data dictionaries, export formats, or (b)(10) documentation.

### Step 9: mraemr.com SSL certificate issue

The browser shows `ERR_CERT_DATE_INVALID` for mraemr.com, indicating an expired SSL certificate. This prevents normal browser access to any page on the domain without accepting the security warning.

## What Was Found

**Nothing.** The registered EHI export documentation URL is completely unreachable. Port 47102 on mraemr.com is not accepting connections — the service appears to be down or the port has been closed/firewalled. No alternative locations for the documentation could be found on the vendor's marketing website, in web archives, or via search engines.

The only evidence that this documentation ever existed is:
1. The URL registered in CHPL (https://mraemr.com:47102/api/DataExportGuidance.asp)
2. The fact that the product was certified for 170.315(b)(10) in January 2023

The mraemr.com domain is alive and serves the live EHR application on the standard HTTPS port, but it has an expired SSL certificate and requires login for all functionality. There is no publicly accessible documentation of any kind.

## Export Coverage Assessment

### Data Domain Coverage

**Cannot be assessed.** No export documentation is available. Based on the product research, Physician's Solution stores extensive data across many domains:

- Patient demographics and registration
- Clinical notes and encounter documentation (100+ specialty templates)
- Problem lists, medications, allergies
- Lab orders and results (bidirectional with 20+ labs)
- Clinical images and photographs (especially dermatology)
- Biopsy tracking (BiopsyMapping™, InstaPath℠)
- Immunization records
- Growth charts (pediatrics)
- Appointment scheduling
- Billing, claims, and revenue cycle data
- Insurance eligibility
- Patient account ledgers
- Patient portal messages
- Referral/consult letters
- MIPS quality measure data
- Audit logs
- Telehealth records
- Inventory data

Whether the (b)(10) export covers any, some, or all of these domains is unknown because the documentation is inaccessible.

### Export Format & Standards

**Unknown.** The URL path `DataExportGuidance.asp` suggests this was a Classic ASP page providing guidance documentation (not an API endpoint itself), but the actual format of the EHI export cannot be determined.

### Documentation Quality

**Inaccessible.** The documentation is hosted on a non-standard port (47102) that is currently unreachable. This represents a fundamental accessibility failure — the documentation registered with ONC for public access cannot be accessed by anyone.

### Structure & Completeness

**Cannot be assessed.** No documentation is available for review.

## Access Summary
- Registered URL: https://mraemr.com:47102/api/DataExportGuidance.asp
- Final URL (after redirects): N/A — connection refused
- Status: dead
- Required browser: N/A
- Navigation complexity: N/A (unreachable)
- Anti-bot issues: N/A

## Obstacles & Dead Ends

1. **Port 47102 completely unreachable** — The registered documentation URL uses a non-standard port (47102) that is not accepting TCP connections. This is the primary and insurmountable obstacle. The service on this port appears to have been taken offline or firewalled.

2. **Expired SSL certificate on mraemr.com** — Even the standard port has an expired certificate, preventing normal browser access. curl with `-k` bypasses this but browsers show security warnings.

3. **No Wayback Machine archive** — The page on port 47102 was never crawled by the Wayback Machine, so no historical version exists.

4. **No Google indexing** — No search engine has indexed or cached the page.

5. **Mandatory disclosures also unreachable** — The mandatory disclosures page (`https://mraemr.com:47102/api/mandatory_disclosure.asp`) uses the same dead port 47102, so both required public documents are inaccessible.

6. **Marketing site has no EHI content** — The vendor's WordPress marketing site (mdchartsehr.com) contains no EHI export documentation, no data dictionary, no API docs, and no interoperability documentation of any kind.

7. **Hosting on a non-standard port** — Using port 47102 for public documentation is inherently fragile and atypical. It suggests the documentation may have been served from the same server as the EHR application, possibly using a different IIS site binding, rather than being hosted on a dedicated documentation platform.
