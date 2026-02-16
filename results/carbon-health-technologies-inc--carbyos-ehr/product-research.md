# Carbon Health Technologies, Inc. — Product Research

Researched: 2026-02-16
Developer website: https://carbonhealth.com

## Overview

Carbon Health Technologies, Inc. is a venture-backed healthcare technology company and clinical care provider founded in 2015 in San Francisco by Udemy co-founder Eren Bali, engineer Tom Berry, and physician Greg Burell. In 2018, Carbon Health merged with Direct Urgent Care (founded by emergency medicine physician Caesar Djavaherian), combining its technology platform with a physical clinic network. The company raised over $600 million across multiple funding rounds, including a $350M Series C led by Blackstone in 2021, reaching a peak valuation of approximately $3.3 billion. CVS Health led a $100M investment in 2023 to pilot clinics within CVS retail stores.

Carbon Health operates as both a healthcare provider (urgent care and primary care clinics) and a technology company. It built a proprietary EHR platform called CarbyOS, initially for use in its own clinics. In late 2022, the company announced plans to license CarbyOS to external healthcare providers. As of its most recent disclosures, CarbyOS claims to serve over 1 million patients, 1,200 providers, and 200 locations — suggesting meaningful external adoption beyond Carbon Health's own ~93 clinics.

In August 2024, CEO Eren Bali stepped down to return to Udemy, and COO Kerem Ozkay became CEO. In February 2026, Carbon Health filed for Chapter 11 bankruptcy with liabilities exceeding $100 million, citing $100M–$500M in debt. The company secured $19.5M in debtor-in-possession financing and is pursuing a dual-track restructuring (debt-for-equity exchange or asset sale). The company states operations will continue without interruption during restructuring, including patient access to medical records.

## Product: CarbyOs EHR

CHPL IDs: 11590 (version 2), 11700 (version 3)

### What It Is

CarbyOS is described as an "AI-powered operating system for care delivery." It is a cloud-based, proprietary EHR platform originally built by Carbon Health for its own urgent care and primary care clinics, now also licensed to external healthcare organizations. The platform integrates clinical documentation, billing/RCM, operations management, and patient engagement into a unified system.

The CHPL certification covers two versions:
- **Version 2** (CHPL 11590, certified January 2025): Minimal certification — only (b)(10) EHI export plus infrastructure/security criteria (d)(1), (d)(5), (d)(6), (d)(8), (d)(9), (d)(12), (d)(13), (g)(4), (g)(5). This appears to be the initial certification for export compliance.
- **Version 3** (CHPL 11700, certified September 2025): Broad certification covering 30+ criteria including clinical data capture (a)(1)–(a)(5), (a)(12), (a)(14), transitions of care (b)(1), clinical quality measures (c)(1)–(c)(3), patient access (e)(3), FHIR APIs (g)(7), (g)(9), (g)(10), public health (h)(1), and additional security/infrastructure criteria. This represents the full-featured certified product.

Both versions represent the same platform (CarbyOS EHR), with version 3 being a more broadly certified iteration.

### Users & Market

**Primary users**: Physicians, nurse practitioners, and clinical staff in urgent care and primary care settings. Also billing/coding staff and practice operations managers.

**Clinical settings**: Primarily ambulatory — urgent care clinics, primary care offices, virtual care. Carbon Health's own network includes ~93 clinics across eight states (California, Colorado, Kansas, Massachusetts, New Jersey, Texas, Washington, and others). The company also piloted clinics inside CVS retail stores.

**Customer scale**: CarbyOS reports serving 1,200+ providers and 200+ locations. At its peak, Carbon Health itself operated more clinics, but recent reporting in the bankruptcy filing lists approximately 93 clinics and 1,400 employees with ~480 providers. The gap between these numbers suggests meaningful external CarbyOS licensing has occurred.

**End users**: Clinicians (documentation, orders, prescribing), billing staff (RCM, claims), operations managers (analytics, reporting), and patients (via mobile app for scheduling, records access, messaging).

### Modules & Functionality

CarbyOS is marketed with four core modules (per carbyos.com):

1. **Care (EHR)**: The core clinical module. Described as "provider-tested and approved" with features including:
   - **AI-powered hands-free charting**: GPT-4-based ambient documentation that records doctor-patient conversations and generates SOAP notes. Carbon Health claims this was "the first [EHR] to deploy native AI-assisted charting at scale" (BusinessWire, June 2023). Reports indicate ~800,000+ AI-powered charts created, with 90%+ provider adoption.
   - **Template-based charting** with customizable templates and macros
   - **Clinical decision support** including AI-driven clinical suggestions
   - **E-prescribing** (consistent with (a)(14) certification for implantable device list, though e-prescribing itself is referenced in vendor materials and third-party reviews)
   - **Lab ordering and results viewing** (referenced in vendor blog and third-party sources)
   - **Medical imaging** (referenced in GetApp/third-party review listings)
   - **Referral management** with secure medical record sharing during referrals
   - **Care plans** with patient summaries and takeaways
   - **One-touch check-in and triage workflows**
   - **Automated ICD-10 and CPT coding suggestions** driven by AI during documentation

2. **Health (Patient App)**: Mobile patient engagement application (iOS and Android) providing:
   - Same-day appointment scheduling
   - Video/virtual visits
   - Live doctor chat messaging
   - Treatment plan and medical record viewing
   - Lab results viewing
   - Prescription order tracking
   - Online billing and payment
   - "Health Pass" digital vaccine card (introduced during COVID-19 era)

3. **Operate (Operations Platform)**: Analytics and operational insights for practice management, described as providing "insights for business efficiency." Specific details are thin in public materials.

4. **Billing (Intelligent RCM)**: A fully integrated revenue cycle management module (per the Carby Billing blog post). Features include:
   - Real-time eligibility (RTE) verification at check-in
   - Automated calculation of patient responsibility (co-pays, co-insurance, deductibles, out-of-pocket limits)
   - Credit card payment processing (claims 98%+ same-day patient payment capture)
   - Ambient AI analysis suggesting coding during visits
   - Automated extraction of diagnostic/procedural data for coding
   - Claims scrubbing via customizable rules engine
   - Automated identification/correction of missing or invalid codes
   - Batch claim correction
   - Full claims lifecycle visibility
   - Built-in safeguards requiring complete coding and care plans before chart sign-off

**Additional capabilities** referenced in certification and vendor materials:
- **Transitions of Care / C-CDA exchange** (certified for (b)(1))
- **Clinical Quality Measures** (certified for (c)(1)–(c)(3), with CQM 122v13 listed)
- **FHIR API access** (certified for (g)(7), (g)(9), (g)(10) — FHIR v1.2 documentation available per disclosures page)
- **Public health reporting — immunization registry** (certified for (h)(1))
- **EHI Export** as C-CDA documents for clinical records, PDFs for billing/claims information (per mandatory disclosures page)
- **DataMotion** listed as dependent software (likely for Direct messaging / secure health information exchange)
- **SAML 2.0 SSO** integration with identity providers (Okta, Microsoft Entra)

### Data & Content

Based on the vendor materials, certifications, and feature descriptions, CarbyOS stores and manages the following categories of data:

**Clinical Data** (supported by (a)(1)–(a)(5), (a)(12), (a)(14) certifications and vendor descriptions):
- Patient demographics and history
- SOAP notes / clinical documentation (including AI-generated visit summaries)
- Problem lists, medication lists, medication allergy lists
- Vital signs, lab results, diagnostic imaging references
- Care plans and patient instructions
- Clinical decision support alerts
- Implantable device list
- Family health history

**Orders and Prescribing**:
- E-prescriptions (referenced in multiple sources)
- Lab orders and results
- Imaging orders
- Referral packages with associated clinical records

**Billing and Financial Data** (from the Carby Billing module):
- Insurance eligibility and benefit information
- Claims data (ICD-10, CPT codes)
- Patient financial responsibility calculations
- Payment records (credit card processing)
- Billing workflow status and audit trails
- Claim scrubbing rules and correction history

**Patient Engagement Data** (from the patient app and portal):
- Appointment scheduling records
- Patient-provider messages (chat and video visit records)
- Patient-accessible health records and treatment plans
- Prescription tracking information
- Vaccination records (Health Pass)

**Transitions of Care / Interoperability**:
- C-CDA documents for clinical information exchange
- FHIR resources (per (g)(10) API certification)
- Immunization registry submissions (per (h)(1) certification)
- Direct messaging via DataMotion

**Operational/Analytics Data** (from the Operate module):
- Operational performance metrics (details thin in public materials)
- Provider productivity data (e.g., keystrokes saved, charts created)

**Notable**: The mandatory disclosures page explicitly states that EHI export includes "C-CDA documents for clinical records, PDFs for billing and claims information" and excludes psychotherapy notes per privacy regulations. This confirms both clinical and billing data are within the export scope.

**Gaps in research**: The Operate (analytics/operations) module has minimal public documentation about what data it specifically stores. Virtual visit recordings/transcripts are not explicitly discussed in terms of storage/retention, though the AI charting feature clearly processes audio recordings of visits. It's unclear whether the raw audio/transcripts are retained or only the generated notes.

---

## Business Context

- **Cloud-hosted**: CarbyOS is a cloud-based platform, consistent with Carbon Health's technology-forward positioning.
- **Bankruptcy impact**: The February 2026 Chapter 11 filing introduces uncertainty about the product's long-term viability. The dual-track process (restructuring or asset sale) could result in CarbyOS being acquired by another entity. However, the company states operations continue during restructuring.
- **Product evolution**: CarbyOS evolved from an internal tool to a commercially licensed product. The 2022 announcement of licensing plans and the subsequent ONC certifications (2025) represent a deliberate productization effort.
- **AI differentiation**: The heavy emphasis on AI-powered charting (GPT-4 based ambient documentation) is the product's primary market differentiator. Carbon Health claims this reduces charting time by 75% and saves ~1,200 keystrokes per visit.
- **No third-party reviews found**: CarbyOS does not appear to have a meaningful presence on G2, Capterra, or similar review platforms, likely reflecting its relatively recent entry as an externally-sold product and its origin as an internal tool.
