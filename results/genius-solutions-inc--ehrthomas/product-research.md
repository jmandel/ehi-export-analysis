# Genius Solutions Inc. — Product Research

Researched: 2026-02-15
Developer website: http://www.geniussolutions.com/

## Overview

Genius Solutions Inc. is a small, privately held healthcare IT company headquartered in Warren, Michigan (7177 Miller Dr, Warren, MI 48092). Founded in 1986, the company has over 35 years of experience developing practice management and EHR software. ZoomInfo estimates 51–200 employees. The company develops, programs, and provides technical support and training entirely in-house from the US.

Genius Solutions serves ambulatory practices in several specialties — primarily **chiropractic**, **podiatry**, **physical therapy/occupational therapy (PT/OT)**, and **general medicine**. The company has a separate domain (geniuschiro.com) focused on chiropractic, suggesting that's a core market. The vendor website (geniussolutions.com, built on Wix) is fairly sparse on detailed product information, with most content oriented toward landing pages for each specialty vertical. Pricing starts at roughly $15–20/user/month per third-party review sites.

The company has no notable acquisition history, rebranding, or parent company — it appears to be the same small vendor it's been for decades. Its products include the **eTHOMAS** practice management system and the **ehrTHOMAS** certified EHR, plus ancillary modules (WritePad documentation tool, ADAMS appointment reminder system, Genius HL7 Interface).

## Product: ehrTHOMAS

CHPL ID: 9585

### What It Is

ehrTHOMAS is Genius Solutions' ONC-certified electronic health record system, described as a "4X-certified" EHR. It is designed as a **touch-screen clinical documentation system** that works alongside the eTHOMAS practice management and billing platform. The two products together form what the vendor calls the "THOMAS Complete Practice Management Software Solution" — THOMAS standing for **Total Health Office Management Automation System**.

The certified module (ehrTHOMAS) is the clinical EHR component, but it is tightly integrated with eTHOMAS (practice management/billing) and functions as part of a larger product suite. Diagnostic and billing codes flow automatically from ehrTHOMAS into eTHOMAS for billing. The certification covers a broad range of criteria: full clinical data ((a)(1)–(a)(14)), transitions of care ((b)(1)–(b)(5)), patient portal/VDT ((e)(1)–(e)(3)), public health reporting ((f)(1)–(f)(2)), FHIR APIs ((g)(7)–(g)(10)), and clinical quality measures ((c)(1),(c)(3)).

The SED intended users are "Providers, Medical Assistants" — consistent with ambulatory care workflows.

### Users & Market

ehrTHOMAS serves small to mid-size ambulatory practices across multiple specialties:
- **Chiropractic** — appears to be a primary market; the vendor has a dedicated chiropractic-focused website (geniuschiro.com) and product listing on Chiropractic Economics
- **Podiatry** — the vendor highlights "DRxContent™", described as "the most comprehensive EHR in the Podiatric industry," developed with a team of podiatric doctors and professional content developers
- **Physical therapy / Occupational therapy (PT/OT)**
- **General medicine** — marketed under the "Medical+" branding on the vendor site

The product is available as on-premise (own server), vendor-hosted, or cloud-based (eTHOMAS Cloud web app). Customer counts are not disclosed on the vendor site. Third-party review sites show a small number of reviews (8–10 total across platforms), suggesting a modest user base.

User reviews are mixed (roughly 3–3.6 out of 5 across review platforms). Positive feedback highlights ease of scheduling, user-friendly interface, and digital patient file creation. Negative feedback cites an antiquated appearance, system lags with multiple users, billing complexity, and slow updates.

### Modules & Functionality

The ehrTHOMAS/eTHOMAS suite includes the following modules and capabilities, based on vendor materials, third-party listings, and review sites:

**Core EHR (ehrTHOMAS):**
- Touch-screen clinical documentation with customizable templates
- Clinical decision support (CDS) — generates alerts during documentation
- Problem lists, medication lists, medication allergy lists
- Clinical data recording (vital signs, demographics, etc.)
- Certified for CPOE for medications and lab orders ((a)(1)–(a)(3))
- Drug formulary checking, allergy/drug-drug interaction checks

**E-Prescribing:**
- Electronic prescribing including controlled substances (EPCS) via DrFirst integration
- Formulary checks, allergy checking at point-of-care
- Prescriptions sent directly to pharmacies

**Lab Integration:**
- Lab order and result processing
- Integration with Quest Diagnostics noted by third-party sources
- Genius HL7 Interface (gsLink) for connecting with outside labs, third-party vendors, and other software applications

**Practice Management (eTHOMAS):**
- Appointment scheduling with customizable appointment book
- Automated appointment reminder calling (ADAMS module)
- Insurance verification
- Electronic claims submission
- Medical billing and insurance ledgers
- Patient statements and e-statements
- Remittance posting
- Online payments
- Inventory tracking
- Financial reports and productivity analysis
- Referral tracking
- Patient correspondence

**Patient Portal:**
- Patient access to clinical health records via integration with Microsoft HealthVault
- Certified for View, Download, Transmit (VDT) — (e)(1)–(e)(3)

**WritePad (ancillary documentation module):**
- Customizable point-and-click templates for visit documentation
- Medical necessity support with built-in Medicare P.A.R.T. guidelines
- E/M coding support
- Ability to attach electronic data (x-rays, lab reports, pictures) and embed images into reports
- Integrates bidirectionally with eTHOMAS — patient info, pictures, appointments flow in; diagnosis and procedure codes flow back for billing

**Specialty Content:**
- DRxContent™ — podiatry-specific clinical content library
- Specialty-specific templates, tests, and reports
- Resource library tailored by specialty

**Public Health Reporting:**
- Certified for immunization registry reporting ((f)(1)) and syndromic surveillance ((f)(2))

**Interoperability:**
- Transitions of care / C-CDA support ((b)(1)–(b)(5))
- FHIR API access ((g)(7)–(g)(10))
- HL7 interface (gsLink) for connecting with external systems

### Data & Content

Based on the certified criteria and described features, ehrTHOMAS/eTHOMAS manages the following categories of data:

**Clinical data (well-documented):**
- Patient demographics
- Problem lists / conditions
- Medication lists and prescriptions (including controlled substance prescriptions via DrFirst)
- Medication allergy lists
- Clinical notes / encounter documentation (via touch-screen templates and WritePad)
- Vital signs
- Lab orders and results (Quest integration documented)
- Diagnostic imaging attachments (x-rays, scans — described in WritePad documentation)
- Patient pictures
- Immunization records (certified for (a)(7) and (f)(1))
- Clinical decision support alerts

**Administrative / billing data (well-documented):**
- Appointment schedules and history
- Insurance information and verification records
- Claims data (electronic claims submission, claim tracking)
- Billing/insurance ledgers
- Patient statements
- Remittance/payment posting records
- Online payment records
- Inventory data
- Referral tracking data
- Financial/productivity reports

**Patient portal data:**
- Patient access logs
- The portal is described as HealthVault-based, so the extent of patient-generated data (e.g., patient messaging) is unclear — no mention of secure messaging was found in vendor materials

**Notable gaps in documentation:**
- The vendor website (Wix-based) renders poorly for automated content extraction, making it hard to get detailed feature descriptions
- No mention of secure messaging/patient messaging functionality was found
- No mention of care plan management was found (though (b)(9) care plan is in the certified criteria)
- The relationship between ehrTHOMAS and WritePad is somewhat unclear — WritePad appears to be an alternative or supplementary documentation module rather than a core part of ehrTHOMAS
- No information found about document management, scanned document storage, or fax integration
- The HealthVault-based patient portal is notably dated (Microsoft discontinued HealthVault in 2019), raising questions about current portal functionality
