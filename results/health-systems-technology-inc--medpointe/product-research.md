# Health Systems Technology, Inc. — Product Research

Researched: 2026-02-14
Developer website: http://www.hstcentral.com (redirects to https://medpointemr.com)

## Overview

Health Systems Technology, Inc. (HST) is a small, privately held company headquartered in Rochester, NY (3255 Brighton-Henrietta TL Rd, Rochester, NY 14623). The company has been in the medical software business since 1989, when it began developing practice management software. In 1998, HST released **Practice Made Perfect**, a Windows-based practice management system (upgrading from their earlier DOS-based product). In 2000, working closely with physician clients, HST developed version 1 of **MedPointe**, an EMR workflow suite tightly integrated with Practice Made Perfect. The product is described as having been "developed by physicians working closely with a developer who was an expert workflow analyst."

HST appears to be a very small vendor — the contact person listed on CHPL (Tim Schmidt) appears to be the primary developer/owner. The company targets small to mid-sized ambulatory practices, particularly in family medicine, internal medicine, pediatrics, urgent care, and sleep medicine. There is no information suggesting significant market share; third-party review sites show only a handful of user reviews (3–8 depending on the site), suggesting a limited customer base. Pricing ranges from $299–$499/provider/month (with the first 12 months free for new implementations), though one source lists a base price of $110/month.

## Product: MedPointe

CHPL ID: 11238

### What It Is

MedPointe is a cloud-based, complete EHR and practice management suite marketed as "Med Pointe Workflow Solutions." It is an integrated platform combining electronic health records, practice management, medical billing, and a patient portal into a single product. The current certified version is MedPointe v13 (2015 Edition, ONC-ACB certified as of February 2023), though the customer help site references v12 as well. The product is web-based and also supports thick/thin client and wireless pen-based configurations.

MedPointe has a broad certification footprint with 37 certified criteria spanning clinical documentation (a)(1)–(a)(5), (a)(12), (a)(14)–(a)(15); transitions of care (b)(1)–(b)(3); EHI export (b)(10)–(b)(11); clinical quality measures (c)(1)–(c)(3); patient portal / view-download-transmit (e)(1), (e)(3); public health reporting for immunization registries (f)(1) and cancer case reporting (f)(5); FHIR API access (g)(7)–(g)(10); and direct messaging (h)(1). This is the profile of a full-featured ambulatory EHR — not a narrow module or specialty tool.

The certified module *is* essentially the whole product. MedPointe is an all-in-one system, not a component of a larger suite. Practice Made Perfect (the older PM system) appears to have been subsumed into or tightly integrated with MedPointe rather than sold as a separate product today.

### Users & Market

MedPointe is designed for **small to mid-sized ambulatory practices**. Target specialties explicitly mentioned include:
- Family Medicine
- Internal Medicine
- Pediatrics
- Urgent Care
- Sleep Medicine / Sleep Centers
- Private practices generally

The CHPL metadata lists the intended user as "Ambulatory." Third-party sites describe the customer base as SMBs (small and medium-sized businesses). One source (FindEMR) claims MedPointe serves "a broad spectrum of healthcare providers across small clinics to large hospitals, including government, non-profit, and private institutions," but this seems like marketing language — all other evidence points to a small-practice focus.

There are no specific customer case studies, named deployments, or customer count figures available. The very small number of user reviews across major review platforms (3 on EMRSystems, 8 on SoftwareFinder, scattered others) suggests a modest installed base, likely dozens to low hundreds of practices rather than thousands.

### Modules & Functionality

Based on vendor materials, feature pages, and third-party review sites, MedPointe includes the following integrated modules and features:

**Clinical / EHR:**
- Electronic health records with full clinical documentation
- **Intelligent Text Generation** — a distinctive feature where MedPointe's "Clinical Intelligence" engine learns a provider's documentation style and pre-fills notes based on past encounters with similar characteristics (creating a "multi-dimensional digital fingerprint" of the encounter). This is not a simple template system; it adapts to individual provider patterns over time.
- Problem lists, medication lists, allergy lists with drug interaction checking
- E-prescribing (eRx)
- Order sets
- Preventive care alerts and disease management tracking
- Referral management
- Bidirectional lab integration (electronic lab ordering and results)
- Imaging ordering
- Document management (scanning, organizing, routing documents)
- Picture archiving (medical imaging/photos)
- Correspondence tools (customizable)

**Practice Management / Administrative:**
- Patient scheduling with automated reminders (text, email, voice call)
- Patient demographics management
- Insurance eligibility verification (real-time, directly from MedPointe)
- Custom practice workflows (configurable)
- Analytics and custom reporting / data-driven insights
- Accounting features

**Billing / Revenue Cycle Management (RCM):**
- Integrated medical billing (fully integrated with EHR, not a separate product)
- Revenue Cycle Management — described as handling the full cycle from eligibility verification to payment posting
- Integrated clearinghouse — claims submission and tracking in real time; automatic posting of Electronic Explanation of Benefits (EOBs) and Electronic Remittance Advices (ERAs)
- Claims generation, submission, and denial management
- Payment collection and posting
- Option for outsourced coding and billing services

**Patient Engagement:**
- Patient portal — scheduling, messaging, and records access
- Online intake forms
- Appointment reminders (text, email, voice call)
- Prescription alerts
- Lab result notifications via portal, text, email, and voice call
- Alerts for pending lab/diagnostic tests or procedures

**Telemedicine:**
- Built-in virtual visit capabilities (via ZoomVisit integration, available as $100/provider/month add-on per one source)

**Health Information Exchange:**
- Secure referrals and patient data sharing
- Direct messaging (h)(1) certified
- Transitions of care (C-CDA exchange)

**Public Health Reporting:**
- Immunization registry reporting (f)(1)
- Cancer case reporting (f)(5)

**Compliance / Regulatory:**
- Meaningful Use certified with real-time dashboards and monitoring tools
- Clinical quality measure reporting (c)(1)–(c)(3)
- HIPAA compliant
- ICD-10 compatible
- FHIR API (g)(10) certified

**User Reviews Note:**
User reviews on third-party sites highlight ease of use and fast onboarding ("staff completely unfamiliar with any EMR programming able to use it flawlessly within a day"), customizable correspondence and preventive care features, and responsive customer support willing to add features. Negative feedback mentions occasional system slowness/freezing and longer-than-expected initial setup.

### Data & Content

Based on the features and modules described above, MedPointe stores and manages the following categories of data:

**Clinical Records:**
- Patient demographics
- Problem lists / diagnoses
- Medication lists and prescription history (e-prescribing data)
- Allergy lists and drug interaction data
- Lab orders and results (bidirectional)
- Imaging orders
- Clinical notes / encounter documentation (including the Intelligent Text Generation history)
- Referral records
- Immunization records (required for f(1) registry reporting)
- Cancer case data (required for f(5) reporting)
- Preventive care tracking / disease management records
- Vital signs, clinical observations (implied by (a)(1)–(a)(5) criteria)
- Care plans (implied by (a)(12) certification)
- Clinical decision support interventions (implied by (a)(14)–(a)(15) criteria)

**Administrative / Financial:**
- Appointment schedules and scheduling history
- Insurance/eligibility verification records
- Claims data (submitted claims, ERA/EOB records, denial data)
- Payment records and posting history
- Accounting data
- Patient billing statements

**Documents & Media:**
- Scanned documents
- Medical images / picture archives
- Correspondence
- Referral documents
- C-CDA / transition of care documents

**Patient Portal / Communication:**
- Portal messages between patients and providers
- Online intake form submissions
- Appointment reminders sent (text, email, voice)
- Lab result notifications sent to patients
- Patient-facing health records

**Audit / Compliance:**
- Meaningful Use dashboard data and compliance metrics
- Clinical quality measure data
- Audit logs (required by (d) criteria)

**Note:** The vendor website is heavily styled with the Divi WordPress theme, and most pages failed to return substantive text content when fetched (returning primarily CSS/JS). Feature descriptions were pieced together from the features overview page (which did render), search result snippets, and multiple third-party review sites. The vendor does not publish detailed technical documentation or data dictionaries publicly. The mandatory disclosures page at medpointemr.com/meaningful-use was not parseable — it rendered only styling code.

---
