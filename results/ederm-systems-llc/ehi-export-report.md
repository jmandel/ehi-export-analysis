# eDerm Systems LLC — EHI Export Documentation

Collected: 2026-02-15

## Source
- Registered URL: https://fhir.ederm.io:9443/fhir-server/api/v4/metadata
- CHPL IDs: 10149
- Mandatory disclosures URL: https://www.edermehr.com/ederm-onc-certified
- Developer: eDerm Systems LLC
- Product: eDerm Systems v2.8.0
- Certification date: 2019-10-25

## Navigation Journal

### Step 1: Probed the registered URL

```bash
curl -sv --connect-timeout 10 "https://fhir.ederm.io:9443/fhir-server/api/v4/metadata" \
  -H 'User-Agent: Mozilla/5.0' -H 'Accept: application/fhir+json' 2>&1
```

**Result:** TLS handshake completes but SSL certificate has expired (expired Feb 10, 2026, issued by Let's Encrypt E8). With `-k` (ignore cert errors), the server responds with **HTTP 404 — "The requested resource [/fhir-server/api/v4/metadata] is not available"**. The server is Apache Tomcat/11.0.14.

### Step 2: Probed alternative paths on the FHIR server

Tried all of these paths on `https://fhir.ederm.io:9443` with `-k`:

| Path | Result |
|------|--------|
| `/` | Tomcat default welcome page ("If you're seeing this, you've successfully installed Tomcat") |
| `/fhir-server/` | 404 |
| `/fhir-server/api/` | 404 |
| `/fhir-server/api/v4/` | 404 |
| `/api/v4/metadata` | 404 |
| `/api/metadata` | 404 |
| `/fhir/metadata` | 404 |

**Conclusion:** The Tomcat server is running but the FHIR application (fhir-server WAR) has been undeployed. The server at this address is no longer serving any FHIR content.

### Step 3: Checked fhir.ederm.io on port 80

```bash
curl -sL "http://fhir.ederm.io/" -H 'User-Agent: Mozilla/5.0'
```

**Result:** Default IIS Windows Server page. Different server on port 80 (IIS) vs port 9443 (Tomcat). Neither serves FHIR content.

### Step 4: Checked Wayback Machine

```bash
curl -s "https://web.archive.org/cdx/search/cdx?url=fhir.ederm.io:9443/*&output=text&fl=timestamp,original,statuscode&limit=50"
```

**Result:** No Wayback Machine captures exist for the :9443 port. The Wayback Machine only has captures of `http://fhir.ederm.io/` (port 80), which was always just the IIS default page. No historical captures of the FHIR CapabilityStatement are available.

### Step 5: Examined the mandatory disclosures / ONC certification page

```bash
curl -sL "https://edermehr.com/ederm-onc-certified/" -H 'User-Agent: Mozilla/5.0' -o ederm-onc-certified.html
```

**Result:** HTTP 200. The page contains:

1. A letter to Drummond Group (ONC-ACB) dated 01/25/2019 signed by Andrew Queen, Manager
2. A link labeled "eDerm-API Documentation G9-G10.pdf" which actually points to `eDerm-API Documentation G8-G9.pdf` (same file, mislabeled)
3. A link labeled "Valid URLs" pointing to `ValidURLs.json`
4. Links to Real World Testing Plans and Results (2022–2025)
5. Certification details: certified criteria, additional software (NLM API, Updox)

**No mention of EHI export, (b)(10), "electronic health information," data dictionary, or export documentation anywhere on the page.** The documentation sections on this page are exclusively about the (g)(9)/(g)(10) FHIR API.

### Step 6: Downloaded available documentation files

```bash
curl -sL "https://www.edermehr.com/sites/default/files/webform/eDerm-API%20Documentation%20G8-G9.pdf" \
  -H 'User-Agent: Mozilla/5.0' -o eDerm-API-Documentation-G8-G9.pdf
curl -sL "https://www.edermehr.com/sites/default/files/ValidURLs.json" \
  -H 'User-Agent: Mozilla/5.0' -o ValidURLs.json
```

Both downloaded successfully.

### Step 7: Examined the API Documentation PDF (26 pages)

The PDF titled "EHR OAuth Based API" documents eDerm Systems 2.8.0's proprietary REST API with three endpoints:

1. **POST /ederm/Authenticate** — OAuth-style token acquisition (username/password grant)
2. **POST /ederm/api/SearchPatient** — Patient search by demographics
3. **POST /ederm/api/GetPatientEncounters** — List encounters for a patient
4. **POST /ederm/api/GetPatientData** — Fetch patient data in XML (C-CDA), JSON, or HTML format

The GetPatientData API accepts boolean flags for these data sections:
- patientname, patientgender, patientdob, patientrace, patientethnicity, patientpreferredlanguage
- medications, medicationallergies
- labtest, labresults
- vitalsigns, procedures
- careteammembers, immunizations
- udiforpatientdevices (implantable devices)
- assessment (Assessment and Plan of Treatment)
- goals, healthconcerns
- smokingstatus
- problems

The PDF states: "All values are options, if you donot give any paratemer it will return complete record."

The sample response is a C-CDA document with sections: Chief Complaint, Allergies, Immunizations, Medications, Problems, Procedures, Results (Labs), Plan of Treatment, Social History, Vital Signs, Goals, Health Concerns, Assessment Section, and Mental Status.

### Step 8: Examined ValidURLs.json

This is a FHIR Bundle of type "collection" containing two Endpoint/Organization pairs. The endpoints point to `https://fhir.ederm.io:9443/fhir-server/api/v4/` with payload type C-CDA structured body. This appears to be the (g)(10) service base URL registration, not EHI export documentation.

### Step 9: Searched broadly for EHI export documentation

- Searched edermehr.com via WordPress search for "ehi export" — no relevant results
- Tried common paths: /ehi/, /ehi-export/, /interoperability/, /compliance/, /legal/, /onc/ — all 404
- Searched Wayback Machine CDX API for edermehr.com pages containing "ehi", "export", or "b10" — no results
- Web search for `"eDerm Systems" "EHI export" OR "b(10)"` — no vendor-specific results
- Checked the old domain (edermsystems.org) — it redirects to edermehr.com

## What Was Found

**No EHI export (b)(10) documentation exists.** The registered URL (the FHIR CapabilityStatement endpoint) is dead — the SSL certificate expired Feb 10, 2026, and the FHIR application has been undeployed from the Tomcat server, which now returns 404 for all FHIR paths.

The only documentation available on eDerm's certification page is for the (g)(9)/(g)(10) API:

1. **eDerm-API Documentation G8-G9.pdf** (26 pages, 584 KB) — documents a proprietary REST API that returns C-CDA documents. This covers standard USCDI clinical data sections (demographics, medications, allergies, labs, vitals, procedures, immunizations, problems, assessments, goals, health concerns, devices, care team). The API is not FHIR-based; it's a custom REST endpoint at `https://remotedev-5/ederm/api/`.

2. **ValidURLs.json** (4 KB) — A FHIR Endpoint Bundle registering the FHIR service base URL. Not documentation; just a registration artifact.

There is no data dictionary, no schema documentation, no export format specification, and no description of how to export all electronic health information from the system.

## Export Coverage Assessment

### Data Domain Coverage

The only documented API (the C-CDA-based GetPatientData endpoint) covers a narrow slice of what eDerm stores:

**Covered (standard USCDI clinical data only):**
- Demographics (name, gender, DOB, race, ethnicity, language)
- Medications
- Medication allergies
- Lab tests and results
- Vital signs
- Procedures
- Care team members
- Immunizations
- Implantable devices (UDI)
- Assessment and plan of treatment
- Goals
- Health concerns
- Smoking status
- Problems

**Not covered (based on product research):**
- **Clinical photography** — eDerm stores unlimited photos linked to encounters. This is a core dermatology feature. No export mechanism documented.
- **Pathology lifecycle data** — Biopsy orders, requisitions, pathology results, status tracking, biopsy logs. A distinctive dermatology-specific feature with no documented export.
- **Cancer tracking data** — Follow-up tracking for cancer patients. Not mentioned.
- **Billing/financial data** — CPT/ICD-10 codes, insurance claims (primary/secondary/tertiary), payment posting, collections, co-pay calculations. The product has a full RCM module. None of this is in the API.
- **Practice management data** — Patient registration details beyond basic demographics, insurance information and verification results, scheduling data.
- **Clinical encounter notes / charting** — eDerm's "One-Touch Charting" with 3D anatomical maps produces structured dermatology notes. The C-CDA only captures a generic "Chief Complaint" section, not the dermatology-specific charting data.
- **Scanned documents** — The product supports document scanning into patient records. No export documented.
- **Consent forms** — Automated consent form generation. No export documented.
- **Smart Coder output** — Automated billing code suggestions. No export documented.
- **Dermatology knowledge base references** — Disease-specific treatment plans linked to patients. No export documented.
- **Phone messages** — Provider-patient phone message records. No export documented.

**The documented API is clearly a (g)(9)/(g)(10) FHIR-adjacent clinical summary API, not a (b)(10) EHI export.** It covers roughly the USCDI data classes and nothing else.

### Export Format & Standards

The documented API returns C-CDA 2.1 (Consolidated Clinical Document Architecture) documents, which is an appropriate format for clinical summaries but wholly insufficient for full EHI export. C-CDA is designed for care transitions, not for complete data export.

Key format issues:
- C-CDA cannot represent dermatology-specific data (photography, biopsy workflows, anatomical charting)
- C-CDA has no billing/claims sections
- The API is patient-by-patient, with no bulk export capability documented
- There is no FHIR Bulk Data API, despite the registered URL being a FHIR server

### Documentation Quality

The API documentation PDF is rudimentary:
- No table of contents or structured navigation
- Sample URLs reference `remotedev-5` (an internal hostname), not the production server
- The sample C-CDA response is embedded inline as escaped XML in the PDF
- No field-level definitions for any data element
- No value sets or coded field documentation
- No error response examples beyond generic HTTP status codes
- "Terms of Use: TBD: Link will be added here" — suggesting the documentation was never finalized
- The link text on the certification page says "G9-G10.pdf" but the actual file is named "G8-G9.pdf"

### Structure & Completeness

**No data dictionary exists.** The only structural information is the list of boolean flags for GetPatientData (20 section toggles) and the embedded C-CDA sample. There are no field definitions, no data type specifications, no cardinality information, and no documentation of coded values.

The GetPatientData API note "if you donot give any paratemer it will return complete record" is notable — it suggests the API returns all available C-CDA sections by default, but this "complete record" is limited to what C-CDA can represent, which is the USCDI clinical summary.

### The (b)(10) vs (g)(10) Confusion

This is a textbook case of (b)(10)/(g)(10) conflation. The registered CHPL URL for the EHI export criterion points to a FHIR CapabilityStatement endpoint — this is the (g)(10) FHIR API endpoint, not an EHI export mechanism. The only documentation on the certification page covers the (g)(9)/(g)(10) API. There is no acknowledgment anywhere that (b)(10) requires export of all electronic health information, not just USCDI data.

eDerm appears to have registered its FHIR API endpoint as its EHI export documentation URL, and even that endpoint is now dead.

### Overall Assessment

eDerm Systems has not implemented or documented a (b)(10) EHI export capability. The registered URL is non-functional (expired SSL cert, undeployed application, 404 on all paths), and the only available documentation describes a C-CDA-based clinical summary API that covers approximately 30-40% of the patient data the system stores. The dermatology-specific data that makes this product valuable to its users — clinical photography, pathology lifecycle tracking, cancer follow-up, anatomical charting — has no documented export mechanism whatsoever. The billing/RCM data that constitutes a core module has no documented export either.

This is among the weakest EHI export implementations: no dedicated b(10) documentation, no data dictionary, a dead endpoint, and a misattribution of the (g)(10) API as the (b)(10) mechanism.

## Access Summary
- Final URL (after redirects): https://fhir.ederm.io:9443/fhir-server/api/v4/metadata (SSL cert expired, 404)
- Status: dead
- Required browser: no (curl sufficient for all working pages)
- Navigation complexity: direct_link (but the link is dead)
- Anti-bot issues: none

## Obstacles & Dead Ends

1. **FHIR server SSL certificate expired** — Let's Encrypt cert for fhir.ederm.io expired Feb 10, 2026 (5 days before collection). The server rejects valid TLS connections.
2. **FHIR application undeployed** — Even bypassing the cert error, the Tomcat server returns 404 for all FHIR paths. The server root shows the Tomcat default welcome page, meaning the fhir-server application WAR file has been removed.
3. **No Wayback Machine captures** — The Wayback Machine never captured the :9443 port, so no historical CapabilityStatement is available.
4. **No EHI-specific documentation anywhere** — The certification page only documents (g)(9)/(g)(10). No alternative pages on edermehr.com contain EHI export information. WordPress search yields no results. No common compliance paths (/ehi/, /compliance/, etc.) exist.
5. **Port 80 vs 9443 confusion** — fhir.ederm.io on port 80 is a separate IIS server showing the default Windows Server page, unrelated to the Tomcat-based FHIR server on port 9443.
