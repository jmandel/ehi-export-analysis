# Prime DataQ Health, LLC — Product Research

Researched: 2026-02-15
Developer website: https://www.summitehr.com/

## Overview

Prime DataQ Health, LLC is the formal entity behind **DataQ Health**, a healthcare technology and clinical services company headquartered in Dallas, Texas. Founded in 2020 by Dr. R. Haris Naseem (a cardiac electrophysiologist who has founded 10+ healthcare ventures), DataQ Health initially focused on population health management, value-based care services, and MIPS reporting. In 2023, DataQ acquired Wiseman Innovations, LLC, a healthcare data analytics and population health management company, to strengthen its analytics and predictive modeling capabilities.

DataQ Health developed its **360 Platform** suite — including 360 DeepLearn™ (risk stratification), 360 CareManager™ (care coordination), 360 Ribbon™ (EMR integration), and related tools — aimed at ACOs and value-based care organizations. The company reports serving 15,000 providers across 3,000 practices with $295M in total shared savings, though these figures likely relate to its population health/MIPS business, not the EHR product.

**summitEHR** is a newer product, a joint venture between DataQ Health and **Summus Health Care** — a North Texas healthcare management and services organization also founded by Dr. Naseem. Summus Healthcare operates 35+ primary care and specialty providers across the Dallas-Fort Worth area through entities including Premier Independent Physicians (primary care/internal medicine network), North Texas Diabetes & Endocrinology, Premier Care Behavioral Health, and Starwood Pharmacy. The summitEHR product was certified on August 27, 2025, making it a very recent entrant to the certified EHR market.

DataQ Health appears to be a small company. No public funding rounds, revenue figures, or significant employee counts were found. The company is privately held and does not appear in major EHR market rankings or third-party review platforms (G2, Capterra, KLAS, etc.). No independent user reviews of summitEHR were found on any review platform.

## Product: summitEHR

CHPL ID: 11689
CHPL Product Number: 15.04.04.3236.Davi.01.00.1.250827
Version: 1.0
Certified: 2025-08-27

### What It Is

summitEHR is an ambulatory electronic health record system designed for internal medicine, endocrinology, and cardiology specialties (per the SED intended user description). The vendor markets it more broadly as suitable for primary care practices, multispecialty groups, and behavioral health providers.

The product was certified against a broad set of 34 ONC criteria spanning clinical data management (a)(1)–(a)(5), (a)(12), (a)(14)–(a)(15); transitions of care (b)(1)–(b)(3); clinical quality measures (c)(1)–(c)(3); patient portal/view-download-transmit (e)(1); FHIR APIs (g)(7), (g)(9)–(g)(10); direct messaging (h)(1); and the full suite of security/infrastructure criteria (d)(1)–(d)(9), (d)(12)–(d)(13). This is a comprehensive ambulatory EHR certification profile.

The product tagline is "Designed by clinicians, deployed in weeks," emphasizing quick onboarding and clinical workflow alignment. The vendor describes it as a "modern platform built for connected, value-based care" with embedded AI and predictive modeling capabilities — reflecting DataQ Health's existing analytics background.

### Users & Market

**Target users**: Physicians, clinical staff, and practice administrators in ambulatory settings — specifically internal medicine, endocrinology, and cardiology, though the marketing also mentions behavioral health and primary care.

**Customer base**: Unknown. No customer counts, case studies, or testimonials specific to summitEHR were found. Given the very recent certification date (August 2025) and the version number (1.0), it's likely that the product is in early deployment stages. Summus Healthcare's own network (35+ providers in DFW) is the most probable initial/anchor customer, as the product was explicitly co-developed between DataQ Health and Summus Health Care.

**Market position**: Very small, very new. summitEHR does not appear on any third-party EHR comparison sites, review platforms, or market analyses. No press coverage beyond the vendor's own website was found. This is essentially a startup EHR.

**Deployment model**: Appears to be cloud-hosted based on the web-based interface and "deployed in weeks" messaging, though this is not explicitly stated.

### Modules & Functionality

Based on the vendor website (summitehr.com) and the ONC certification page, summitEHR includes the following capabilities:

**Clinical Documentation**
- Smart templates and voice-enabled charting
- Quick actions and streamlined note completion
- Auto-coding assistance (AI-powered suggestions for coding)
- The (a)(1)–(a)(5) certifications confirm: CPOE for medications, labs, and diagnostic imaging; demographics; problem list; medication list; medication allergy list

**Electronic Prescribing**
- Real-time pharmacy connectivity (electronic prescription routing)
- Medication history access (view past prescriptions and fill history)
- Drug interaction alerts (allergies, interactions, dosage issues)
- EPCS (Electronic Prescribing of Controlled Substances) compliance
- Integrates with **NewCrop** for e-prescribing (noted on the ONC certification page)

**Patient Management**
- Integrated scheduling with appointment reminders
- Secure messaging between providers and patients
- Telehealth capabilities built into the platform

**Patient Portal**
- Certified for (e)(1) — view, download, and transmit health information
- Patient access to their records

**Care Coordination**
- Team-based workflows with task delegation
- Transparent communication tools across practices
- Certified for transitions of care (b)(1)–(b)(3) — create, receive, and reconcile C-CDAs
- Direct messaging via **EMR Direct** integration (noted on ONC certification page)

**Analytics & Reporting**
- Dashboards tracking quality metrics and financial performance
- Population health trend analysis
- Predictive analytics for risk identification
- Clinical quality measure reporting — certified for (c)(1)–(c)(3) — CQM capture, export, and reporting
- 13 clinical quality measures tested per the ONC certification page

**Interoperability**
- FHIR API access — certified for (g)(7), (g)(9), (g)(10)
- Connections with labs, pharmacies, HIEs, and payers
- Direct messaging for clinical information exchange (h)(1)
- OAuth 2.0 authentication

**Security**
- Optional multi-factor authentication (MFA)
- End-user device encryption
- Trusted connection protocols
- Full suite of (d) criteria: authentication, auditing, authorization, encryption, etc.

**Implantable Device List**
- Certified for (a)(14) — maintaining a list of a patient's implantable devices

**Social/Psychological/Behavioral Data**
- Certified for (a)(15) — capturing social, psychological, and behavioral data

### Data & Content

Based on the certified criteria and described features, summitEHR stores and manages:

- **Patient demographics** — (a)(5) certification
- **Problem lists** — (a)(3) certification
- **Medication lists** — (a)(4) certification, plus e-prescribing data via NewCrop integration
- **Medication allergy lists** — (a)(2) certification
- **Clinical notes** — voice-enabled charting, smart templates
- **Orders** — CPOE for medications (a)(1), labs (a)(12), and diagnostic imaging (a)(12 context suggests lab/radiology ordering)
- **Prescription data** — e-prescribing with EPCS, medication history, pharmacy connectivity
- **Lab results** — interoperability with labs, (b)(11) certification for electronic health information export
- **Clinical quality measure data** — (c)(1)–(c)(3) certified
- **Implantable device data** — (a)(14) certified
- **Social/psychological/behavioral data** — (a)(15) certified
- **Care plans and transition of care documents** — (b)(1)–(b)(3) certified, C-CDA generation
- **Patient portal messages** — secure messaging described
- **Scheduling/appointment data** — integrated scheduling with reminders
- **Telehealth session data** — telehealth built into the platform
- **Audit logs** — (d)(2) certified
- **Direct messages** — (h)(1) certified, EMR Direct integration

**What's unclear or absent:**
- **Billing/claims**: The website does not explicitly describe billing, claims management, or revenue cycle management as a feature. The mention of "financial performance dashboards" and "auto-coding assistance" hints at some billing-adjacent functionality, but it's unclear whether summitEHR includes integrated billing or if billing is handled externally. This is a notable gap in the available information.
- **Document management/scanning**: No mention of document imaging or scanning capabilities.
- **Patient-reported outcomes**: Not mentioned.
- **Faxing**: Not mentioned, though this is common in ambulatory EHRs.
- **Referral management**: Not explicitly described, though care coordination is mentioned.
- **Practice management**: The product emphasizes clinical workflows; it's unclear whether practice management (insurance verification, eligibility checking, claims submission) is built in or separate.
