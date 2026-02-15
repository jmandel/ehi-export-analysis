# BroadStreet Health LLC — Product Research

Researched: 2026-02-14
Developer website: https://www.broadstreetcare.com

## Overview

BroadStreet Health LLC is a very small health IT startup (1–10 employees) that develops an ONC-certified EHR for post-acute and community-based health providers. The company is closely related to — and likely a subsidiary or DBA of — WashSense Inc. and Arsana Health. The contact listed on CHPL (Laura Ivanoski) uses a `washsense.com` email address and serves as VP of Finance & Operations at WashSense. The BroadStreet product portal is hosted at `broadstreet.arsanahealth.com`.

**Corporate structure:** The overall entity appears to be **Arsana Health**, founded by Connor Dahlberg, headquartered at the Black River Innovation Campus in Springfield, Vermont. Arsana Health operates a "Multi-Provider Integrated Platform" with two main components:
1. **Arsana Health Portal / BroadStreet** — an EHR software platform
2. **WashSense** — smart handwashing/infection surveillance hardware devices

The CORI Innovation Fund led a funding round for Arsana Health (announced ~June 2020), providing capital to expand in the post-acute care market. Thomas Dahlberg (a rural health physician) is listed as co-founder of WashSense. The company appears very early-stage with minimal market presence — no third-party reviews (G2, KLAS, Capterra) were found, the main website at broadstreetcare.com shows a "Coming Soon" placeholder for most content, and web searches return almost no customer references or independent coverage.

## Product: BroadStreet

CHPL ID: 11410 (15.05.05.3161.BRDS.01.00.1.231222)

### What It Is

BroadStreet Version 1 is an ONC-certified Electronic Health Record system specifically designed for post-acute care and community-based healthcare settings, including skilled nursing facilities and assisted living homes. It was certified on December 22, 2023.

Per the mandatory disclosures page, BroadStreet was "developed with the goal of creating a new way to experience, interact, and deliver care." The product's usability testing report (from SLI Compliance, December 2024) describes it as featuring "a unique task architecture that enhances the way users capture, modify, and interact with patient health information."

BroadStreet is part of the broader Arsana Health platform, which positions itself as combining medical records from multiple sources (post-acute care facilities, doctors' offices, labs, and pharmacies) into a unified interface. The Arsana platform also includes AI-powered analytics for health risk detection (fever, respiratory symptoms, antibiotic usage) and care coordination capabilities.

### Users & Market

**Target users:** Post-acute and community-based health providers (per the CHPL `sed_intended_user_description`). This means staff at skilled nursing facilities (SNFs), assisted living communities, and potentially other long-term care settings.

**Market presence:** Essentially unknown. No customer count, no case studies, no third-party reviews were found. The vendor website is largely a placeholder. The company has fewer than 10 employees. This appears to be an early-stage product with very limited deployment.

**Geography:** Based in Springfield, Vermont (at the Black River Innovation Campus, designated as a federal Opportunity Zone). Vermont rural health focus is suggested by the founder's background and CORI Innovation Fund investment.

**No reviews found** on G2, KLAS, Capterra, or any other third-party review platform. No press coverage of customer deployments.

### Modules & Functionality

Based on the mandatory disclosures page and certified criteria, BroadStreet includes the following capabilities:

**Clinical Documentation & Orders (from certified criteria):**
- CPOE for medications — 170.315(a)(1)
- CPOE for laboratory orders — 170.315(a)(2)
- CPOE for diagnostic imaging orders — 170.315(a)(3)
- Demographics capture — 170.315(a)(5)
- Family health history — 170.315(a)(12)
- Implantable device list — 170.315(a)(14)
- Social, psychological, and behavioral data capture — 170.315(a)(15)

**Care Coordination & Interoperability:**
- Transitions of care (C-CDA) — 170.315(b)(1)
- Clinical information reconciliation (medications, problems, allergies) — 170.315(b)(2)
- EHI export — 170.315(b)(10)
- Care plan — 170.315(b)(11)
- Direct secure messaging via EMR Direct Interoperability Engine (requires annual subscription) — 170.315(h)(1)

**Patient Access:**
- View, download, and transmit health information — 170.315(e)(1)
- Patient-generated health data — 170.315(e)(3)

**Clinical Quality Measures (CQMs):**
- CMS2 v13: Screening for depression and follow-up plan
- CMS69 v12: Preventive care and screening: BMI screening and follow-up
- CMS138 v12: Preventive care and screening: tobacco use screening and cessation intervention
- CMS139 v12: Falls: screening for future fall risk
- CMS149 v12: Dementia: cognitive assessment
- CMS951 v2: Kidney health evaluation

The CQM selections are strongly indicative of the post-acute/geriatric care focus — fall risk, dementia cognitive assessment, depression screening, and kidney health are core measures for skilled nursing and long-term care populations.

**FHIR API Access:**
- Standardized API for patient and population services — 170.315(g)(7), (g)(9), (g)(10)

**Security & Infrastructure:**
- Full suite of security criteria: (d)(1) through (d)(13), covering authentication, access control, audit logging, encryption, emergency access, and multi-factor authentication.

**Usability testing (from SLI Compliance report):** Tasks tested included collecting, modifying, and reconciling outside records; working with demographics, implantable devices, labs, diagnostics, and medications.

**Broader Arsana Platform capabilities** (from washsense.com/post-acute and press coverage, not specifically from BroadStreet certification docs):
- Infection surveillance with cross-contamination mapping
- Chronic care management
- Remote clinical evaluation of complex cases
- Advanced care planning
- Hospital diversion initiatives
- AI-powered health risk analytics (fever, respiratory symptoms, antibiotic usage patterns)
- Integration with WashSense smart handwashing devices for real-time hygiene compliance monitoring

It is unclear how much of the broader Arsana platform is part of the certified BroadStreet product vs. separate products in the same ecosystem.

### Data & Content

**Data types confirmed by certification criteria:**
- Patient demographics
- Medication orders and medication lists
- Laboratory orders and results
- Diagnostic imaging orders
- Problem lists
- Allergy lists
- Family health history
- Implantable device records
- Social, psychological, and behavioral data (SDOH-adjacent)
- Care plans
- Clinical quality measure data (depression screening, BMI, tobacco use, fall risk, cognitive assessment, kidney health)
- C-CDA documents (for transitions of care)
- Patient-generated health data
- Audit logs and access records

**Data types implied by Arsana platform marketing (but not confirmed as part of BroadStreet specifically):**
- Infection surveillance data
- Hand hygiene compliance data
- Cross-contamination mapping
- Records aggregated from external sources (doctors' offices, labs, pharmacies)

**What's unclear / not mentioned:**
- **Billing and claims data:** Not mentioned anywhere. The certification criteria don't include billing-related items, and neither the vendor website nor any marketing materials mention billing functionality. The Arsana/CORI press release mentions the platform "creates new billing opportunities" but doesn't describe integrated billing/claims modules. Billing is likely handled by a separate system.
- **Scheduling:** Not mentioned.
- **Progress notes / clinical narrative documentation:** Not explicitly described, though likely present given the clinical charting implied by CPOE and CQM capabilities.
- **Nursing assessments (MDS, OASIS, etc.):** Not mentioned, despite the post-acute focus where MDS assessments are a core workflow for SNFs. This is a notable gap in available information.
- **eMAR (electronic medication administration record):** Not mentioned, though this would be expected for a post-acute EHR.
- **Pharmacy integration:** Not explicitly described.
- **Messaging/communication between staff:** Not mentioned.

The overall picture is of an early-stage post-acute EHR with a solid set of ONC-certified clinical capabilities, but with very limited publicly available information about the full breadth of the product's functionality. The vendor website and marketing materials are sparse, making it difficult to assess what the product does beyond what's required for certification.
