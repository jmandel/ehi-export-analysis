# Altera Digital Health Inc. — Product Research

Researched: 2026-02-16
Developer website: https://www.alterahealth.com

## Overview

Altera Digital Health is a healthcare IT company formerly known as the Hospitals and Large Physician Practices business segment of Allscripts Healthcare Solutions. In May 2022, N. Harris Computer Corporation (a subsidiary of Constellation Software Inc.) acquired this segment for approximately $700 million and rebranded it as Altera Digital Health. The company's product portfolio includes Sunrise (acute/hospital EHR), Paragon (community hospital EHR), TouchWorks EHR (ambulatory EHR), dbMotion (interoperability platform), Care Director (care coordination), Ventus (revenue cycle management), CareFX (clinical workflow), and Altera Context (context management/SSO). Altera serves hospitals, health systems, and large physician practices globally, with a presence in the U.S., APAC, and Israel.

**Important CHPL certification note:** The CHPL listing (ID 11675) for this TouchWorks EHR certification names the developer as **Providers Management, Inc.** (website: integratedproviders.com), not Altera Digital Health directly. Providers Management, Inc. is a small company based in Burton, Michigan, associated with Genesys PHO (a Physician Hospital Organization affiliated with Ascension Genesys Hospital). Providers Management operates the "Integrated Providers Patient Portal" (IGP Patient Portal), which is itself separately ONC-certified and lists "Altera Digital Health Touchworks EHR" as required additional software. This suggests Providers Management is either a reseller/deployment partner for TouchWorks EHR or has obtained a separate certification for the TouchWorks instance they deploy within their Genesys PHO network. The contact email (Nate.Buchholz@genesyspho.com) confirms the Genesys PHO affiliation.

## Product: TouchWorks EHR

CHPL IDs: 11675 (CHPL Product Number: 15.04.04.3123.Touc.25.12.1.250723)

### What It Is

TouchWorks EHR is an ambulatory electronic health record platform designed for medium to large, single or multi-specialty physician practices, Management Services Organizations (MSOs), and Integrated Delivery Networks (IDNs). It is Altera's flagship ambulatory product, distinct from their hospital-focused Sunrise and Paragon platforms. The product covers clinical documentation, order management, e-prescribing, scheduling, billing/revenue cycle tools, patient portal, analytics, and mobile access.

The certified module here represents the full TouchWorks EHR product (version 2025), with a very broad set of 38 certified criteria spanning clinical data (a)(1)-(a)(5), (a)(12), (a)(14)-(a)(15); transitions of care (b)(1)-(b)(3), (b)(10)-(b)(11); CQMs (c)(1)-(c)(3); privacy/security (d)(1)-(d)(9), (d)(12)-(d)(13); patient portal (e)(1), (e)(3); public health reporting (f)(1)-(f)(2), (f)(4)-(f)(5), (f)(7); APIs/FHIR (g)(2)-(g)(7), (g)(9)-(g)(10); and direct messaging (h)(1). This is a comprehensive certification covering essentially all clinical, interoperability, and reporting categories.

### Users & Market

TouchWorks EHR targets large ambulatory practices and multi-specialty clinics. Altera Digital Health (formerly Allscripts/Veradigm) holds approximately 3–3.6% of the U.S. ambulatory EHR market, placing it roughly 7th-8th among vendors, well behind Epic (~19-44%), eClinicalWorks (~12%), and athenahealth (~7%). The product is designed for organizations with 1,000+ employees.

On G2, TouchWorks has a 4.0/5.0 star rating. KLAS rates it at 6.8/9 for ambulatory EHR functionality, trailing Epic (7.5) and athenahealth (7.1). User reviews note solid customization and scalability but flag a steep learning curve, occasional usability issues, and mixed customer support responsiveness. Some KLAS commenters noted the vendor is "behind and playing catch-up" since the Allscripts separation.

The specific CHPL certification here is under Providers Management, Inc. / Genesys PHO, a Michigan-based physician network with ~100 primary care physicians and several hundred specialists associated with Ascension Genesys Hospital. This represents a deployment of TouchWorks EHR within a specific PHO network rather than the broader Altera customer base.

### Modules & Functionality

Based on vendor materials (alterahealth.com/solution/touchworks/), product pages, release notes, and third-party reviews:

**Clinical Documentation & Charting:**
- Comprehensive patient records centralizing orders, lab results, radiology reports, and multidisciplinary notes in a single database
- Flexible charting with customizable templates
- Note+ module: ambient listening and AI-driven note generation (introduced 2024-2025) to reduce documentation burden
- AI-powered dictation and proofreading (2025 release)

**Order Management:**
- Computerized order entry for labs, radiology, referrals
- Direct connections to labs, radiology centers, pharmacies, and preferred providers
- Smart pharmacy and lab choices (2025 enhancement)
- Group filtering of orders, streamlined chart review (2025 enhancement)
- Direct faxing from orders (2025 enhancement)

**E-Prescribing:**
- Electronic prescribing and refills
- Remote prescribing via mobile devices
- EPCS (Electronic Prescribing of Controlled Substances) support (implied by (a)(4) certification)

**Scheduling:**
- Advanced appointment management and patient scheduling
- Automated reminder options

**Billing & Revenue Cycle:**
- Integrated billing and coding assistance
- Revenue cycle management tools
- Risk adjustment and compliance reports
- (Altera also offers Ventus as a separate, more comprehensive revenue cycle product — unclear how much billing is built into TouchWorks vs. handled by Ventus)

**Clinical Decision Support:**
- Structured recommendations and clinical guidelines
- Actionable alerts at point of care
- Drug-drug, drug-allergy interaction checking (implied by (a)(4) certification)

**Patient Portal:**
- Patient access to records and test results
- Secure messaging between patients and providers
- (The Providers Management/Genesys PHO deployment uses the separately certified "Integrated Providers Patient Portal" for (e)(1) patient access functionality, listing TouchWorks as required additional software)

**Analytics & Reporting:**
- Quality measures and compliance reporting
- Practice analytics for care gap identification
- Data trending and patient outcome monitoring across multiple locations
- CQM reporting (certified for (c)(1)-(c)(3))

**Public Health Reporting:**
- Immunization registry reporting (f)(1)
- Syndromic surveillance (f)(2)
- Cancer case reporting (f)(4)-(f)(5)
- Electronic case reporting (f)(7)

**Interoperability:**
- FHIR API support (g)(10)
- C-CDA document generation and consumption
- Support for USCDI v3 and C-CDA R4.1 (2025 release)
- Direct messaging (h)(1)
- Transitions of care / care summaries (b)(1)-(b)(3)
- Integration with dbMotion interoperability platform (separate Altera product)

**Mobile Access:**
- TouchWorks EHR Mobile for accessing patient records, prescribing, and task management from mobile devices

**Task Management:**
- Streamlined task queues for review, order management, and follow-ups

**Attachment Management:**
- Enhanced attachment management (2025 release)
- Document scanning and management

### Data & Content

Based on the features described above and the certified criteria, TouchWorks EHR stores and manages:

- **Patient demographics** — standard registration data
- **Clinical notes and documentation** — progress notes, encounter notes, AI-generated notes, dictation
- **Orders** — lab orders, radiology orders, referral orders, prescription orders
- **Lab results** — structured laboratory data
- **Radiology reports** — imaging results
- **Medications** — active medication lists, prescription history, refill records
- **Allergies** — allergy and adverse reaction records
- **Problem lists** — diagnoses and conditions
- **Vital signs** — clinical measurements
- **Immunizations** — vaccination records (evidenced by (f)(1) immunization registry reporting)
- **Clinical decision support data** — alerts, rules, guidelines
- **Patient messages** — secure messaging through patient portal
- **Scheduling data** — appointments, reminders
- **Billing/claims data** — charge capture, coding, claims (though the extent of built-in vs. Ventus is unclear)
- **Quality measure data** — CQM calculations and submissions
- **Public health reports** — immunization submissions, syndromic surveillance, cancer case reports, electronic case reports
- **Care summaries / C-CDA documents** — transitions of care documents
- **Attachments/scanned documents** — uploaded clinical documents
- **Audit logs** — access and activity tracking (required by (d) criteria)
- **User/provider data** — provider profiles, credentials, preferences

The Providers Management/Genesys PHO deployment also integrates with their IGP Patient Portal, which adds ACO reporting data, online bill pay, and community resource directories. The patient portal stores its own data about patient portal accounts, message threads, and patient-entered information.

**Areas of uncertainty:**
- The website doesn't clearly delineate what billing data lives in TouchWorks vs. the separate Ventus revenue cycle product. TouchWorks has "billing and coding assistance" but Ventus is described as the comprehensive revenue cycle solution.
- Population health analytics capabilities are mentioned but it's unclear how much data is stored in TouchWorks vs. dbMotion or other analytics platforms.
- The relationship between the Providers Management certification and the broader Altera/TouchWorks product is unusual — this specific certification may represent a customized deployment within the Genesys PHO network.

---

## Altera Product Ecosystem Context

TouchWorks EHR exists within Altera's broader product portfolio. Key related products that may share or exchange data:

- **Sunrise** — acute/hospital EHR for hospitals and health systems (separate product, different architecture)
- **Paragon** — community/critical access hospital EHR (separate product)
- **dbMotion** — interoperability platform that aggregates data across disparate EHRs into a longitudinal patient record
- **Ventus** — revenue cycle management including billing, coding, EMPI, surgery scheduling, and medical necessity compliance
- **Care Director** — outpatient care coordination across the continuum
- **CareFX** — clinical workflow streamlining across disparate systems
- **Altera Context** — context management / single sign-on using HL7 CCOW standard

For this (b)(10) EHI export assessment, the relevant scope is what TouchWorks EHR itself stores — but awareness of these adjacent products is important because some data (especially financial/billing and cross-system interoperability data) may reside in companion products rather than in TouchWorks directly.
