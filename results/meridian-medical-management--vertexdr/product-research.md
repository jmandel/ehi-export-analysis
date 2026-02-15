# Meridian Medical Management — Product Research

Researched: 2026-02-15
Developer website: https://vertexdr.com/

## Overview

Meridian Medical Management is a healthcare IT and revenue cycle management (RCM) company originally formed in 2002 and based in Windsor, Connecticut. The company was a former GE Healthcare IT entity, later acquired by The Gores Group as a portfolio company. In December 2014, Meridian acquired Origin Healthcare Solutions (bringing analytics capabilities and expanding to over 40,000 healthcare providers). In January 2016, Meridian rebranded its two core technology products — SSIMED (practice management) and EMRge (electronic medical records) — under the unified VertexDr brand.

In June 2020, MTBC, Inc. acquired Meridian Medical Management for approximately $24.8M. MTBC subsequently rebranded itself as CareCloud, Inc. in 2021. CareCloud (NASDAQ: CCLD) is now a publicly traded healthcare IT company. Meridian continues to operate as a division ("Meridian Medical Management, a CareCloud Company"), and VertexDr remains its certified EHR/PM product.

Meridian's typical customers are large, multi-specialty physician groups and academic faculty practice plans, often with 200–600 providers. Notable customers include Hutchinson Clinic (a 118-provider multi-specialty group in Kansas) and The Polyclinic (a multi-specialty group in Seattle). The company also serves smaller physician practices, ACOs, specialty groups, and integrated delivery networks. The contact email in the CHPL metadata uses the @carecloud.com domain, confirming the CareCloud ownership.

## Product: VertexDr

CHPL IDs: 11002

### What It Is

VertexDr is a fully integrated electronic medical records (EMR) and practice management (PM) system. The vendor describes it as "one of the only fully-integrated EMR and PM systems built from the ground up; no acquisitions, no interfacing" — meaning the clinical EHR and the practice management/billing sides were designed as a single integrated platform rather than assembled from separate acquisitions.

The product originated as two separate but tightly coupled products: SSIMED (practice management) and EMRge (electronic medical records), both rebranded to VertexDr in January 2016. The current certified version is 9.1 (certified October 2022). The predecessor version 9.0 received ONC 2015 Edition certification in November 2018.

The certified module (the Health IT Module) is the VertexDr EMR/PM system itself. It appears to constitute the core of the product rather than being a small component of a larger platform. However, Meridian also offers surrounding services (outsourced RCM, medical coding, analytics via PrecisionBI/Origin Analytics) that complement the software.

### Users & Market

**Intended users**: Clinical staff (per CHPL metadata's SED description), physicians, practice administrators, billing staff.

**Clinical settings**: Ambulatory physician practices — private practices, group practices, multi-specialty groups, and academic practice plans. The product serves various specialties (a Pediatrics Plus customer was cited in one press release).

**Market position**: VertexDr is a niche product. It has no presence on major review platforms like G2 or Capterra, and web presence is limited. The vendor website (vertexdr.com) is functional but minimal. Meridian's broader business serves "thousands of healthcare providers nationwide" (per the MTBC acquisition announcement), though it's unclear how many of those specifically use VertexDr vs. other PM/EHR systems (Meridian describes itself as "EHR and PM system agnostic" for its RCM services, meaning they also service clients using other EHR platforms).

**Ownership**: Now part of CareCloud, Inc., a publicly traded company (NASDAQ: CCLD). CareCloud also separately acquired the original CareCloud platform (a Miami-based EHR/PM product) in 2020. These are distinct product lines within the same parent company.

### Modules & Functionality

Based on vendor website, press releases, and product descriptions, VertexDr encompasses:

**Practice Management / Billing**:
- Appointment scheduling with customizable workflows
- Practice management (registration, demographics, insurance)
- Claims management and billing — designed to "accelerate physician reimbursements"
- Proactive claims editing tool (mentioned in 2019 press release)
- Billing reminders via SMS text messages (added as a feature enhancement)
- Revenue cycle management integration

**Electronic Health Records (Clinical)**:
- Customizable electronic health records with templates for clinical documentation
- E-Prescribing including Electronic Prescribing of Controlled Substances (EPCS)
- Clinical decision support (implied by (a)(2), (a)(3) certification criteria)
- CPOE — Computerized Provider Order Entry (certified for (a)(1)–(a)(4))
- Problem list, medication list, medication allergy list management (per (a)(5) and related criteria)
- Clinical quality measures / quality reporting (certified for (c)(1)–(c)(3))

**Interoperability & Data Exchange**:
- HL-7 compatibility
- ANSI, NCPDP, HIPAA-specified EDI format support
- Integration with clinical, reporting, accounting, and hospital systems
- Transitions of care / C-CDA support (certified for (b)(1)–(b)(3))
- FHIR API access (certified for (g)(7), (g)(10))
- Immunization registry reporting (certified for (f)(1))
- Syndromic surveillance reporting (certified for (f)(3))

**Patient Engagement**:
- Patient portal / View-Download-Transmit (certified for (e)(1))
- Secure messaging to patients (certified for (e)(3) — "patient health information capture")
- SMS text message reminders for appointments and billing

**Analytics & Reporting**:
- Embedded PrecisionBI analytics solution (described as providing "operational insights" and enabling "greater transparency and efficiency")
- "Most advanced reporting engine on the market" (vendor claim)
- Customizable dashboards

**Other**:
- Mobile functionality
- Workflow automation
- Inscribe5 medical transcription/scribe tool (mentioned in 2019 press release as an enhancement)
- Data center hosting (Meridian offers AWS-based hosting)

### Data & Content

Based on the certified criteria and described features, VertexDr stores and manages:

**Clinical data** (confirmed by certification criteria (a)(1)–(a)(5), (a)(12), (a)(14)):
- Patient demographics
- Problem lists / diagnoses
- Medication lists and medication allergy lists
- Clinical notes / encounter documentation (customizable templates)
- Lab orders and results (implied by CPOE and clinical data criteria)
- Vital signs
- Immunization records (confirmed by (f)(1) immunization registry reporting)
- Family health history ((a)(12) certification)
- Clinical decision support rules/alerts

**Prescription data** (confirmed by EPCS capability):
- E-prescriptions including controlled substances
- Prescription history

**Billing/Financial data** (confirmed by PM module description):
- Insurance information
- Claims data with claim scrubbing/editing
- Billing records and payment information
- Scheduling/appointment data

**Care coordination data** (confirmed by (b)(1)–(b)(3) certification):
- C-CDA documents (transitions of care summaries)
- Referral information

**Patient engagement data** (confirmed by (e)(1), (e)(3) certification):
- Patient portal access records
- Patient-generated health data (implied by (e)(3))
- SMS reminders and communication records

**Quality/Reporting data** (confirmed by (c)(1)–(c)(3) certification):
- Clinical quality measures
- Promoting Interoperability / Meaningful Use metrics

**Analytics data** (confirmed by PrecisionBI integration):
- Operational and financial performance metrics
- Practice analytics and dashboards

**Gaps/Uncertainties**:
- The vendor website doesn't specifically mention lab interfaces or lab result management beyond what's implied by the certification criteria.
- It's unclear whether VertexDr handles imaging orders/results or has any radiology integration.
- Document management / scanned document storage is not explicitly mentioned.
- The relationship between VertexDr's built-in analytics and the separate PrecisionBI / Origin Analytics platform is ambiguous — some analytics may live in VertexDr's database while others may be in a separate analytics data warehouse.
- The Inscribe5 transcription/scribe tool's data storage model is unclear — whether transcribed notes are stored within VertexDr's database or managed separately.
