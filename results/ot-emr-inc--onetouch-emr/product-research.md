# OT EMR, Inc. — Product Research

Researched: 2026-02-15
Developer website: https://onetouchemr.com (redirects to https://onetouchemr.net)

## Overview

OT EMR, Inc. is a small, privately held health IT company headquartered in Dallas, Texas, founded in 2010 by Dr. Robert Abbate, D.O., an internal medicine physician with a prior background in web-based software development (he previously founded a web-hosting company called "Performance Hosting"). After graduating from residency and becoming board-certified in Internal Medicine in 2010, Dr. Abbate found existing EMR systems to be "bulky, hard to navigate, utterly confusing and intimidating" and built OneTouch EMR as an alternative — an EMR "designed by a doctor for doctors." The company received investment backing from other physicians and launched circa 2011.

OneTouch EMR is a cloud-based ambulatory EHR and practice management system targeting small to mid-size physician practices, particularly in primary care specialties (internal medicine, family medicine, general practice). The vendor's tagline on its website is "Cloud-Based EMR Software, Medical Billing. Dallas, TX." The company appears to be a small operation — the contact person listed on the ONC certification is the founder himself (Dr. Robert Abbate), the App Store listing has only 24 ratings, and the product is listed on startup directories like Gust. There are no public indicators of large customer counts, venture rounds beyond early physician investors, or significant market share. Third-party review sites (Capterra, Software Advice, EMRFinder) list it among small-practice EMR options, and QATestLab lists OneTouch EMR as a customer for QA testing services.

## Product: OneTouch EMR

CHPL IDs: 11599

### What It Is

OneTouch EMR is a single, integrated cloud-based platform that combines electronic health records (EHR), practice management (PM), patient portal, medical billing, and e-prescribing into one product. The certified module (OneTouch EMR, Version 3, certified 2025-02-24) appears to be the entire product — there is no indication that the certified module is a component of a larger separate platform. The product is certified across a broad range of ONC criteria: clinical data management (a)(1)–(a)(5), (a)(12), (a)(14); transitions of care (b)(1)–(b)(3); patient portal (e)(1), (e)(3); clinical quality measures (c)(1)–(c)(3); public health reporting (f)(1), (f)(5); FHIR APIs (g)(7), (g)(10); and Direct messaging (h)(1). The intended users per the certification are "Clinical Assistants, Physician's Assistants, MD, RN, Admin."

The product is accessible via web browser, iPad, Android tablet, and has a native iOS app (available in the Apple App Store, requires iOS 16.0+, also runs on Mac with M1+ and Apple Vision Pro). The system was originally designed with a touch-screen-first approach, emphasizing tablet-based workflows.

### Users & Market

OneTouch EMR targets small and mid-size ambulatory practices, particularly:
- **Primary care**: Internal medicine, family medicine, general practice
- **Practice sizes**: Solo practitioners to small/medium multi-provider groups
- **User roles**: Physicians (MD/DO), physician assistants, nurses (RN), clinical assistants, and administrative staff

The vendor offers a free tier (with limited features) designed to attract medical students and small practices. Pricing ranges from free to $599/month per provider for the Platinum plan, with an "EHR + PM" bundle at $565/provider and a "Revenue Cycle" tier at custom pricing. The SaaS subscription model was specifically chosen to be more affordable than traditional on-premise EMR systems that required large upfront capital.

There are no publicly available customer counts, but the small number of reviews (24 App Store ratings, a handful of Capterra/Software Advice reviews) and the startup-scale company profile suggest a modest user base. Reviews indicate the product is used by small independent practices. One App Store reviewer noted it "can be configured to function for any size practice," but there is no evidence of hospital or large group deployments.

### Modules & Functionality

Based on vendor materials, third-party review sites, and the App Store listing, OneTouch EMR includes the following modules and features:

**Clinical Documentation / EHR:**
- Patient charting with customizable templates
- Touch, type, or voice dictation input (Dragon Medical integration)
- Clinical assessments and vital signs documentation
- Drawing tools for photo and image annotation (Free Draw tool for annotating clinical photos or standard images)
- iPad photo capture for clinical images
- Document management system
- E&M coding guidelines with built-in coding helper
- ICD-10 ready coding

**E-Prescribing:**
- Electronic prescribing (eRx) integrated into the workflow
- EPCS (Electronic Prescribing for Controlled Substances) support
- Drug interaction checks

**Lab Integration:**
- Electronic lab orders and results
- Integration with "most laboratories nationwide"
- Lab results auto-display in patient charts

**Practice Management / Scheduling:**
- Appointment scheduling with day/week/month/year views
- Appointment status tracking
- Appointment reminders via text and email
- Patient demographics management

**Patient Portal:**
- Secure patient-provider communication (HIPAA-compliant messaging)
- Telemedicine module
- Online billing / patient payment
- Online scheduling
- Medical summary viewing
- Patient check-in and online form completion

**Medical Billing & Revenue Cycle:**
- Integrated medical billing application
- Unlimited eClaims submission
- Claim scrubbing with rules-based engines
- Integrated clearinghouse (ERAs auto-queued for processing)
- Eligibility verification
- Denial management (auto-classification of denials by clinical, coding, and administrative reasons)
- POS / integrated payment processing (accept payments online and in-person)
- Full practice reporting
- Patient billing
- When ERAs are processed, denials are automatically sent to appropriate work lists for follow-up

**Interoperability / Integration:**
- HL7 interface for communicating with billing platforms and other PM systems
- Claims to integrate with "over 70 popular practice management and competitor systems" (AdvancedMD, Allscripts, NextGen, Meditech, eClinicalWorks mentioned by FindEMR — though this may be overstated)
- Integrated fax
- FHIR R4 API (per ONC certification)
- Direct messaging (certified for (h)(1))
- Transitions of care / C-CDA document exchange (certified for (b)(1)–(b)(3))

**Compliance / Reporting:**
- Meaningful Use Stage 1, 2, 3 certified
- MIPS/MACRA/ACI certified
- Clinical quality measure reporting (certified for (c)(1)–(c)(3))
- Public health reporting: immunization registry (f)(1), electronic case reporting (f)(5)
- HIPAA compliant

### Data & Content

Based on the features described above, OneTouch EMR stores and manages the following types of data:

- **Patient demographics** — names, contact information, insurance, background information (described in scheduling and demographics management features)
- **Clinical encounter notes** — charting documentation via templates, dictation, or touch input; including assessments, vital signs, and clinical narratives
- **Clinical images** — photos taken via iPad, annotated images using the drawing/Free Draw tool
- **Prescriptions and medication data** — e-prescribing records including controlled substances (EPCS), drug interaction data
- **Lab orders and results** — electronic lab orders sent to nationwide labs, results received and displayed in charts
- **Documents** — managed via the document management system, including faxes (integrated fax)
- **Appointments and scheduling data** — appointment records, statuses, reminders sent via text/email
- **Patient portal communications** — secure messages between patients and providers, telemedicine session data
- **Patient-submitted forms** — online check-in forms and patient-completed intake forms
- **Billing and claims data** — eClaims, claim scrubbing results, ERA/remittance data, eligibility verification records, denial management records, payment processing records
- **Clinical quality measures** — CQM reporting data (certified for (c)(1)–(c)(3))
- **Public health reports** — immunization registry submissions, electronic case reporting data
- **Care transition documents** — C-CDA documents for transitions of care
- **Audit logs** — required by (d) criteria certification
- **Medical summaries** — patient-facing medical summaries (viewable via patient portal)

**Gaps and uncertainties:**
- The vendor website was intermittently inaccessible during research (403 errors on several pages including /practice-management, /medical-billing, /software). Some feature details come from third-party review aggregators rather than the vendor directly.
- FindEMR's claim that OneTouch integrates with "over 70 popular practice management and competitor systems" seems unlikely for a small vendor and may be inaccurate or refer to clearinghouse-level connectivity rather than deep EMR-to-EMR integration.
- The distinction between the EHR-only plans and the "EHR + PM" and "Revenue Cycle" tiers is not fully clear — it's possible that billing/PM features are only available in higher tiers, meaning some OneTouch EMR installations may not have billing data if they use only the EHR tier.
- No mention was found of specialty-specific modules beyond primary care (e.g., no behavioral health, ophthalmology, or surgical modules described).
- The website does not describe specific reporting or analytics capabilities beyond what's required for MIPS/CQM compliance.
- No information was found about referral management, prior authorization workflows, or population health features.
