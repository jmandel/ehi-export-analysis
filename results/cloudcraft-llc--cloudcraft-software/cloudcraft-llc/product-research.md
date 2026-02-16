# CloudCraft, LLC — Product Research

Researched: 2026-02-15
Developer website: http://www.naiacorp.com (listed in CHPL; resolves to naiacorp.net)
Product website: https://cloudcraftsoftware.com

## Overview

CloudCraft, LLC is the certified developer name, but the company behind it is **NAIA Corporation**, a Birmingham, Alabama-based IT services company founded in 1997 by Terry Lee. NAIA was originally (and still partly) a general IT consulting firm serving manufacturing and distribution companies. The company expanded internationally with offices in Hyderabad, India and Birmingham, England. Tanveer Patel (formerly CEO of CircleSource) was hired as CEO in 2010. NAIA has approximately 11–50 employees per ZoomInfo.

CloudCraft Software is NAIA's healthcare product — a cloud-hosted EHR and practice management system. The company is small and niche; CloudCraft does not appear on major EHR review/comparison sites (G2, Capterra, Software Advice listings for this product do not exist — the "Cloudcraft" on those sites is an unrelated AWS architecture diagramming tool by Datadog). The product has very limited public-facing documentation, marketing materials, or third-party reviews. NAIA Corporation itself is not listed among Alabama's top healthcare software companies in industry directories.

The strongest evidence of CloudCraft's customer base comes from subdomains on `naiacorp.net`: **Goshen Medical Center**, a Federally Qualified Health Center (FQHC) with 38 service locations across eastern North Carolina, appears to be a customer based on the existence of `goshenmedical.naiacorp.net` (a CloudCraft-powered staff portal with login, career center, and other administrative tools hosted on NAIA's infrastructure). This suggests CloudCraft targets community health centers / FQHCs as a primary market segment, which aligns with the product's feature set including a dedicated sliding fee scale module (visible at `cloudcraft-slidingfee.naiacorp.net`).

## Product: CloudCraft Software

CHPL ID: 11150
CHPL Product Number: 15.04.04.3071.Clou.09.01.1.221227
Version: 9.0
Certification Date: 2022-12-27

### What It Is

CloudCraft Software is described by the vendor as a "cloud-hosted EHR system" and "all-in-one solution for electronic health records, practice management, billing, and human resources." It is a web-based application (Angular SPA) hosted on AWS infrastructure, accessed through modern browsers (Chrome, Firefox — IE is explicitly not supported). The system supports Office 365 authentication integration.

The product architecture appears modular, with distinct application components hosted on separate subdomains:
- **cloudcraft-clinical.naiacorp.net** — EMR / clinical module (branded "EMR - CloudCraft")
- **cloudcraft-billing[preprod].naiacorp.net** — Billing module
- **cloudcraft-slidingfee.naiacorp.net** — Sliding fee scale management (FQHC-specific)
- **ehrpatientportal.naiacorp.net** — Patient portal
- **ehrweb[qa/preprod].naiacorp.net** — Main EHR web application (version 8.1.2 observed on QA)
- **fhirapitest.naiacorp.net** — FHIR R4 API endpoint

The certified module encompasses the entire product — there's no indication that CloudCraft Software is a component of a larger platform. It appears to be the full product offering from NAIA for healthcare.

### Users & Market

**Target users**: "Users at a healthcare office or facility" (per CHPL SED description). Based on the Goshen Medical Center evidence, primary users appear to be clinical and administrative staff at FQHCs and community health centers, including:
- Physicians, NPs, PAs (Goshen Medical employs these roles across 38 sites)
- Nurses (RNs, LPNs)
- Medical assistants
- Front desk/reception staff
- Billing/finance staff
- Practice administrators

**Market segment**: Small to mid-size ambulatory practices and community health centers, particularly FQHCs. The sliding fee scale module is a strong indicator of FQHC focus (sliding fee schedules are a HRSA requirement for FQHCs).

**Customer count**: Unknown. Only one customer (Goshen Medical Center) is identifiable through public evidence. The company's small size (11–50 employees) suggests a limited customer base.

**Geography**: The vendor is based in Birmingham, AL. The identifiable customer is in eastern North Carolina. No geographic constraints are apparent — the product is cloud-hosted.

### Modules & Functionality

The vendor website is marketing-heavy and feature-light — it describes CloudCraft in broad strokes without detailed feature breakdowns. What follows is synthesized from the vendor website, subdomain structure, CHPL certification criteria, and the B10 export documentation page.

**Core modules identified:**

1. **Electronic Health Records (EHR/EMR)** — The clinical module (`cloudcraft-clinical.naiacorp.net`). Based on CHPL certification criteria, this must support:
   - Computerized Provider Order Entry (CPOE) for medications, lab orders, and diagnostic imaging — certified under (a)(1), (a)(2), (a)(3)
   - Drug-drug and drug-allergy interaction checking — certified under (a)(4)
   - Demographics recording — certified under (a)(5)
   - Problem list — certified under (a)(9) (clinical decision support implies structured problem data)
   - Family health history — certified under (a)(12)
   - Patient-specific education resources — certified under (a)(14)
   - Clinical decision support — certified under (a)(9)

2. **Practice Management** — Mentioned on the vendor website. Likely includes scheduling, registration, and administrative workflows. The team-based login flow ("Choose Team" page post-authentication) suggests multi-location/multi-provider support.

3. **Billing** — A distinct billing module exists (`cloudcraft-billing.naiacorp.net`). Described as part of the "all-in-one solution." No details on specific billing features (e.g., claim submission, ERA/EOB processing, charge capture) are publicly available.

4. **Sliding Fee Scale** — A dedicated module (`cloudcraft-slidingfee.naiacorp.net`) for managing income-based sliding fee discount programs, a core FQHC/community health center requirement under HRSA.

5. **Human Resources** — Mentioned on the vendor website as part of the all-in-one solution. The Goshen Medical career center (`goshenmedical.naiacorp.net/CareerCenter`) showing job postings may be a feature of this module.

6. **Patient Portal** — A patient-facing portal exists (`ehrpatientportal.naiacorp.net`). Certified under (e)(3) for patient electronic access/request for amendment.

7. **FHIR API** — FHIR R4 endpoint documented at `fhirapitest.naiacorp.net`, certified under (g)(7)–(g)(10). The B10 page mentions FHIR R4 DocumentReference resources enabling connections to third-party apps (MyLinks, Apple Health, etc.).

**Transitions of care / interoperability:**
- Certified for (b)(1) Transitions of Care — C-CDA creation/consumption
- Certified for (b)(2) Clinical Information Reconciliation — medication, allergy, and problem list reconciliation
- Certified for (h)(1) Direct Project — secure messaging/transport

**Public health reporting:**
- (f)(1) Immunization registry reporting — transmission to immunization registries
- (f)(5) Electronic case reporting
- (f)(7) Health care surveys — implies data collection/reporting capability

**Clinical quality measures:**
- Certified for (c)(1)–(c)(4) — CQM recording, import, reporting, and filtering. The vendor site references a "Clinical Quality Measures" section, though details aren't publicly accessible.

### Data & Content

Based on certification criteria, the B10 export documentation, and product evidence, CloudCraft stores and manages:

**Clinical data** (inferred from certified criteria):
- Patient demographics (a)(5)
- Medication orders and records (a)(1) — CPOE for medications
- Lab orders (a)(2) — CPOE for lab
- Diagnostic imaging orders (a)(3) — CPOE for diagnostic imaging
- Allergy and drug interaction data (a)(4)
- Problem lists (a)(9)
- Family health history (a)(12)
- Clinical decision support rules/alerts (a)(9)
- Patient education resources provided (a)(14)
- Immunization records (f)(1)
- Clinical quality measure data (c)(1)–(c)(4)

**Documents and files** (from B10 export page):
- C-CDA USCDI v3 documents
- PDFs (including scanned and faxed records)
- Image files (JPEG, GIF, TIF)
- Word documents
- Internal correspondence: tasks and notes
- Any document format with a recognized MIME type

**Transitions of care data:**
- Incoming and outgoing C-CDA documents (b)(1)
- Reconciled medications, allergies, and problem lists (b)(2)

**Practice management / billing data:**
- Billing records (billing module exists but details are sparse)
- Sliding fee scale/discount calculations and patient financial data (sliding fee module)
- HR/staffing data (HR module mentioned but unverified)
- Scheduling/appointment data (implied by practice management description)

**Patient portal data:**
- Patient-accessible health records (e)(3)
- Amendment requests (e)(3)

**Notable gaps in available information:**
- The vendor website provides almost no feature-level detail — no screenshots, no detailed module descriptions, no feature comparison pages
- No information on whether the product supports e-prescribing (no (b)(3) or EPCS certification)
- No information on lab interfaces or results management beyond CPOE for ordering
- No details on specific billing capabilities (claim types, payer integrations, ERA processing, etc.)
- No details on reporting capabilities beyond CQM
- No information about fax/scanning workflows despite B10 mentioning "scanned and faxed records"
- Whether the HR module stores meaningful employee/staffing data or is lightweight is unknown
- UDS reporting capability (critical for FQHCs) is not mentioned anywhere, despite FQHC customer base

---

## Research Limitations

CloudCraft Software has an unusually thin public web presence for a certified EHR product. The vendor website (`cloudcraftsoftware.com`) is essentially a single-page marketing site with no deep feature documentation, screenshots, or detailed product descriptions. All internal application pages are JavaScript SPAs that cannot be inspected without authentication. No third-party reviews, case studies, or industry analyst coverage was found. The most informative evidence came from the subdomain structure on `naiacorp.net` and the CHPL certification criteria themselves, rather than from vendor-provided documentation.
