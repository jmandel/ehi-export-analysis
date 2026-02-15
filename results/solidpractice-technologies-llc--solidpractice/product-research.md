# SolidPractice Technologies, LLC — Product Research

Researched: 2026-02-14
Developer website: http://www.solidpractice.com

## Overview

SolidPractice Technologies, LLC is a small, privately held company based in Sarasota, Florida. The product is built by Innovative Medical Practice Solutions (IMPS), which has over 30 years of experience in medical document management. The company traces its origins to Voice Activated Systems / Medical Voice Products, which developed voice-enabled medical record software technology. The company was founded in 1994, and the CEO/Chief Medical Officer is Dr. Andras Fenyves, a practicing physician.

SolidPractice is a small-vendor ambulatory EMR/EHR targeted at private medical practices. The company appears to be very small — no employee count is published, but the website emphasizes "friendly, local staff" and direct phone support without ticketing systems. There are no published customer counts, no notable case studies, and no reviews on major platforms (G2, Capterra). The product has zero user reviews on Slashdot's SourceForge comparison platform. This suggests a very small install base, likely serving a handful of small ambulatory practices.

## Product: SolidPractice

CHPL ID: 10763

### What It Is

SolidPractice is a desktop-based ambulatory EHR/EMR system designed for small medical practices. It is certified as a Complete EHR (originally Stage 2 Meaningful Use, now ONC 2015 Edition Cures Update). The certified module appears to be the entire product — there is no evidence of a larger product suite or separate components. The product emphasizes ease of use ("as simple and easy to use as a paper chart") and voice dictation as its key differentiators.

The product is broadly certified across 33 ONC criteria spanning clinical documentation (a)(1)-(a)(5), (a)(12), (a)(14), transitions of care (b)(1)-(b)(3), patient portal (e)(1), clinical quality measures (c)(1)-(c)(3), public health reporting (f)(1), (f)(5), FHIR APIs (g)(7)-(g)(10), and direct messaging (h)(1). This is a full-scope ambulatory EHR certification.

### Users & Market

Target users are described as "providers and support staff" in ambulatory settings. The product is marketed to small private practices seeking a simple, affordable EHR that qualifies for government EHR incentive payments (Meaningful Use / Promoting Interoperability). No specialty focus is identified — it appears to be a general ambulatory EHR.

No customer count, number of sites, or market share data is available. The vendor website mentions no notable customers or case studies. The company's very small web footprint and absence of third-party reviews suggest a micro-vendor with a very limited install base.

The vendor offers monthly subscription pricing with no upfront software costs, US-based phone support, and on-site implementation assistance. They emphasize quick implementation ("days, not weeks or months").

### Modules & Functionality

Based on vendor website pages and third-party feature listings, SolidPractice includes:

**Clinical Documentation & Charting**
- Comprehensive charting functionality (per vendor feature page)
- Real-time voice dictation/transcription — this is the product's signature feature, originating from the company's roots in voice-enabled medical software
- Handwriting recognition (listed on Slashdot comparison)
- Custom data field creation
- Vital signs recording
- Medication and allergy tracking

**E-Prescribing**
- E-prescribing via integration with NewCrop and SureScripts Network for Clinical Interoperability (per mandatory disclosures page and press release)

**Labs & Imaging**
- Electronic lab integration (per support page and feature list)
- Lab and imaging management (per feature page)

**Clinical Decision Support**
- Drug interaction checking (per feature page)
- Clinical decision support through "risk management approach" (per mandatory disclosures)

**Referrals**
- Automated referral letter generation (per feature page)

**Patient Portal**
- Patient portal / self-service portal (listed on Slashdot comparison; certified for (e)(1) view-download-transmit)

**Billing Integration**
- Billing system integration is mentioned on the feature page, along with E/M coding support
- PQRS registry reporting for Medicare/Medicaid (per feature page)
- It is unclear whether billing is built into SolidPractice or handled through an external integration. The feature page says "billing system integration" which could imply an external billing system rather than built-in billing.

**Telehealth**
- Integrated telehealth (listed on Slashdot comparison feature list)

**Reporting & Compliance**
- Report generation tools
- MIPS certified (per Slashdot comparison)
- Clinical Quality Measures — 11 CQMs per mandatory disclosures
- Meaningful Use / Promoting Interoperability attestation support

**Interoperability**
- FHIR API and Data Access API (per mandatory disclosures)
- Import/export functionality
- Direct messaging (certified for (h)(1))
- Transitions of care / C-CDA exchange (certified for (b)(1)-(b)(3))

**Scheduling**
- Appointment management (listed on Slashdot comparison feature list)
- Activity center for workflow tracking (per feature page)

### Data & Content

Based on the features and certifications identified, SolidPractice stores or manages:

- **Patient demographics** — implied by (a)(5) certification and core EHR function
- **Clinical notes / encounter documentation** — central function; voice-dictated notes are a core feature
- **Medication lists** — medication tracking, e-prescribing via NewCrop/SureScripts
- **Allergy lists** — allergy tracking per feature page
- **Vital signs** — explicitly mentioned on feature page
- **Problem lists / conditions** — implied by (a)(1)-(a)(4) certifications
- **Lab orders and results** — electronic lab integration per feature page
- **Imaging orders** — lab and imaging management per feature page
- **Referral letters** — automated referral letter generation per feature page
- **Prescriptions / prescription history** — e-prescribing integration
- **Drug interaction data** — drug interaction checking per feature page
- **Clinical quality measure data** — 11 CQMs per mandatory disclosures
- **Patient portal data** — patient portal certified for (e)(1)
- **C-CDA / transitions of care documents** — certified for (b)(1)-(b)(3)
- **Immunization data** — implied by (f)(1) immunization registry reporting
- **Syndromic surveillance data** — implied by (f)(5) certification
- **Custom fields** — custom data field creation per feature page
- **Appointment/scheduling data** — appointment management per feature comparison
- **Billing/E&M codes** — E/M coding and billing integration per feature listings, though the depth of billing data stored is unclear

**Gaps in research**: The vendor website is sparse and marketing-oriented. There are no user reviews, case studies, or detailed documentation publicly available to confirm the full scope of data stored. The billing integration is ambiguous — it's unclear whether full billing/claims data is stored within SolidPractice or in an external system. The telehealth feature is listed in a third-party comparison but not described on the vendor's own site, so its data scope is unclear.
