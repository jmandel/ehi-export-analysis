# Claimpower, Inc. — Product Research

Researched: 2026-02-14
Developer website: https://www.claimpower.com

## Overview

Claimpower, Inc. is a small, family-run healthcare IT and billing services company based in Glen Rock, New Jersey. Founded in 1992, the company is now led by CEO Rohan Thadani (whose parents founded the business). Claimpower's core business is **managed medical billing services** for small physician practices. They also offer a proprietary cloud-based EHR/EMR, practice management tools, credentialing services, and MIPS reporting support.

The company positions itself as serving "hundreds of doctors in small practices across the United States" (per ZoomInfo), emphasizing personalized service and a "small company touch." Their business model bundles EHR software free of charge to practices that use their billing services — the EMR is **not offered as a stand-alone product** (per their mandatory disclosures page). This means Claimpower is primarily a billing services company that includes an EHR as part of its service offering, rather than a pure software vendor.

## Product: Claimpower Mobile EMR

CHPL ID: 11209
Version: 6.1
Certification Date: 2023-01-09

### What It Is

Claimpower Mobile EMR is a cloud-based, mobile-friendly electronic medical records system designed for small ambulatory physician practices. It is certified under ONC's 2015 Edition Cures Update and carries a broad set of certifications including clinical documentation (a)(1)–(a)(5), (a)(12), (a)(14), transitions of care (b)(1)–(b)(3), patient access (e)(1), clinical quality measures (c)(1)–(c)(4), immunization registry reporting (f)(1), FHIR APIs (g)(7), (g)(10), and direct messaging (h)(1).

The certified module is part of a broader integrated offering that includes practice management and managed billing services. The EHR is tightly coupled with Claimpower's billing operation — it is only available to billing clients.

### Users & Market

**Target users**: Doctors and their staff (per the CHPL SED description), specifically small and solo physician practices across multiple specialties.

**Market position**: Very small vendor. Claimpower serves "hundreds of doctors" in small practices. There are no listings on major review platforms (G2, Capterra, Software Advice), suggesting limited market visibility. The company appears to have a small team and serves a niche market of practices that want an integrated billing-service-plus-EHR bundle rather than a standalone EHR.

**Pricing** (from mandatory disclosures):
- EMR included free with billing services (no additional cost for core EMR)
- ePrescribing: $25/prescriber/month
- Direct Messaging: $15/Direct Address/month
- Text Messaging: $0.10/text
- Document Indexing: $0.10/page for bulk uploads

**Clinical settings**: Ambulatory/outpatient physician practices. The vendor claims experience "across all specialties" for their billing services. No indication of hospital, inpatient, or institutional use.

### Modules & Functionality

Based on the vendor website, mandatory disclosures, and certification criteria, the Claimpower Mobile EMR and its associated practice management platform include:

**Clinical Documentation (EHR)**
- Cloud-based EMR accessible on any platform and device ("Mobile EMR")
- Customizable templates that can be adapted to practice workflows
- Dragon voice dictation integration for clinical note documentation
- Patient queue interface for streamlined EMR access
- CPOE (Computerized Provider Order Entry) — certified under (a)(1)
- Demographics recording — certified under (a)(5)
- Problem list, medication list, medication allergy list — certified under (a)(2)–(a)(4)
- Drug-drug and drug-allergy interaction checking — certified under (a)(4)
- Clinical decision support — certified under (a)(14) (non-standard; typically (a)(9), but this product is certified for (a)(14) which is implantable device list)
- Family health history — certified under (a)(12)

**Lab Integration**
- Lab order submission and results viewing within the EMR (described on EHR feature page)

**ePrescribing**
- Electronic prescribing available as an add-on ($25/prescriber/month)
- Likely integrated with Surescripts given the (b)(3) electronic prescribing certification

**Patient Communication & Portal**
- Secure messaging to other doctors and patients (described on EHR page)
- Patient portal / view-download-transmit — certified under (e)(1)
- Text messaging for recall reminders and patient communications ($0.10/text)

**Transitions of Care**
- Transitions of care send/receive — certified under (b)(1), (b)(2)
- Direct messaging for secure health information exchange — certified under (h)(1), priced at $15/address/month

**Practice Management**
- Patient scheduling
- Real-time eligibility checking
- Patient balance viewing
- Payment collection and credit card processing
- Customizable super bills (paper and electronic)
- Dozens of prebuilt reports plus custom reporting
- 24/7 web-based access to all practice data
- eFaxing integration
- Paper chart digitization / document scanning and indexing

**Billing (Managed Service, not self-service)**
- Daily electronic claims submission (primary and secondary)
- Proprietary claim scrubbing software
- CPT and ICD-10 coding services
- Pre-loaded intuitive e-superbills
- ERA/EOB posting and patient balance billing
- Denial management and appeals
- Soft collections (calls and texts)
- Work processed overnight by Claimpower's billing team

**Quality Reporting**
- MIPS submission support — Claimpower offers dedicated experts who personally assist doctors
- Clinical quality measures — certified under (c)(1)–(c)(4)

**Public Health Reporting**
- Immunization registry transmission — certified under (f)(1)

**Chronic Care & Transitional Care**
- The EHR page mentions support for Chronic Care Management (CCM) and Transitional Care Management (TCM) services

**Interoperability / APIs**
- FHIR API access — certified under (g)(7), (g)(9), (g)(10)
- API documentation mentioned on the vendor website

### Data & Content

Based on the evidence gathered, the Claimpower Mobile EMR and its integrated practice management/billing platform store or manage the following data:

**Clinical data** (confirmed by certification criteria and feature descriptions):
- Patient demographics
- Problem lists, medication lists, medication allergy lists
- Clinical notes/encounter documentation (with voice dictation)
- Lab orders and lab results
- Prescriptions / medication orders
- Family health history
- Implantable device list (per (a)(14) certification)
- Clinical quality measure data
- Immunization records (per (f)(1) certification)
- C-CDA documents for transitions of care

**Practice management data** (confirmed by feature descriptions):
- Patient scheduling / appointments
- Insurance eligibility data
- Patient balances and payment records
- Super bills and encounter forms
- Scanned/indexed paper documents

**Billing and claims data** (confirmed by billing service descriptions):
- Electronic claims (primary and secondary)
- ERA/EOB records
- CPT and ICD-10 codes
- Denial and appeal records
- Payment posting records
- Collections activity

**Communication data** (confirmed by feature and pricing descriptions):
- Secure messages (provider-to-provider and provider-to-patient)
- Direct messages (health information exchange)
- Text messages (patient reminders/recalls)
- eFax records

**Important caveat**: Because Claimpower's billing is a **managed service** (Claimpower staff process claims, not the practice), the billing/claims data may reside partly in Claimpower's billing operations systems rather than entirely within the EMR module. The boundary between "data stored in the EMR" and "data managed by Claimpower's billing service" is unclear from public sources. However, the practice management module does provide 24/7 access to billing/claims data, suggesting it is accessible through the same platform even if operationally managed by Claimpower staff.

**Gaps in research**: The vendor website is relatively sparse. No third-party reviews were found on G2, Capterra, or Software Advice. The ZoomInfo profile mentioned "remote patient monitoring" and "AI-driven charting" as services, but these are not prominently described on the vendor's own website — it's unclear whether these are current product features or aspirational/emerging offerings. The product's actual UI and feature depth are difficult to assess from public sources alone.
