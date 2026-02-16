# Health Innovation Technologies, Inc. — Product Research

Researched: 2026-02-15
Developer website: https://www.revolutionehr.com

## Overview

Health Innovation Technologies, Inc. is the company behind RevolutionEHR, a cloud-based EHR and practice management platform built exclusively for optometry and eye care practices. The company was co-founded in 2006–2007 by optometrist Dr. Scott Jens and CTO Jim Schneider in Madison, Wisconsin. In October 2014, the company was acquired by RevOptix, a private investment group, which invested approximately $45 million into RevolutionEHR's parent entity, Rev360. Rev360 is the broader eye care software and business services company that delivers RevolutionEHR along with a suite of optional add-on business services. In 2016, RevolutionEHR/Rev360 also acquired Getwell, another cloud-based EHR/PMS provider for eye care practices. A former business unit, RevCycle Partners (billing/revenue cycle services), later spun out as an independent company.

RevolutionEHR reports serving over 13,000 eye care professionals with a 97% customer retention rate. The product has a 4.48-star rating across 838 reviews and won the 2025 Eyevote RC award. The company has converted 80+ competing EHR systems to its platform. Pricing starts at approximately $299/month, positioning it as a mid-range solution for optometry practices. It is cloud-hosted (recently migrated to AWS), accessible from any device with a web browser, and requires minimal internet bandwidth (4 Mb/s download, 512 Kb/s upload).

## Product: RevolutionEHR

CHPL IDs: 9923

### What It Is

RevolutionEHR is an integrated EHR and practice management platform designed exclusively for optometry. It is certified under ONC Health IT Certification with a broad set of criteria covering clinical documentation (a)(1)–(a)(14), transitions of care (b)(1)–(b)(2), patient portal (e)(1), clinical quality measures (c)(1)–(c)(3), FHIR APIs (g)(7)–(g)(10), and public health reporting (h)(1). The SED intended user description is "Eye care professionals and staff members — ambulatory setting."

The certified module (RevolutionEHR v7) appears to be the core product, but it is sold as part of a broader ecosystem of "Rev" add-on modules. The core platform includes clinical EHR, practice management, scheduling, optical dispensing, and basic billing. Additional integrated modules are available as paid add-ons.

### Users & Market

**Target users:** Optometrists, ophthalmologists (to a lesser extent), opticians, optical staff, billing staff, practice managers, and front-office staff. The platform also serves students at optometry colleges/schools.

**Clinical settings:** Single-location and multi-location optometry practices, corporate-affiliated practices, specialty eye care (low vision, vision therapy), mobile/home-based eye care (nursing home visits), and optometry schools. This is an ambulatory-only, eye-care-only product — it is not used in hospitals or non-eye-care settings.

**Customer base:** 13,000+ eye care professionals. This is a mid-market product for small-to-medium optometry practices, not a large enterprise health system EHR. The company competes with products like Crystal Practice Management, Eye Cloud Pro, Optosys, and MaximEyes.

**Notable:** The product was "designed by optometrists for optometrists" — the clinical workflows and exam templates are optometry-specific rather than generic. Users in reviews note that the system was "clearly designed by people with real world clinical experience."

### Modules & Functionality

Based on vendor website, integration pages, help documentation, and user reviews, RevolutionEHR includes the following modules and capabilities:

**Core EHR / Clinical Documentation:**
- Customizable exam templates for optometry encounters (routine exams, specialty exams)
- Patient summary dashboard showing exam history, account balance, and insurance info
- Optometry-specific clinical forms and coding tools
- Diagnostic equipment integration with 12+ instrument manufacturers (Canon, Essilor, Marco, Optos, Optovue, Reichert, TopCon, Zeiss, etc.) — diagnostic test data flows directly into patient records
- Specialty diagnostic tests for low vision, vision therapy, and other optometric specialties
- Clinical decision support and coding assistance
- Picture archiving system (PACS) for ophthalmic images
- Mobile/tablet-friendly clinical documentation

**Practice Management & Scheduling:**
- Appointment scheduling and calendar management
- Multi-location support
- Staff role customization and task list configuration
- Practice analytics and reporting

**Optical Dispensing & Ordering:**
- Optical point-of-sale (POS) functionality
- Frame and lens inventory management
- Contact lens ordering (via SmartFLOW integration with suppliers like Hoya, CooperVision, ABB Optical Group)
- Direct connections with optical suppliers (OOGP, VisionWeb, Arrellio)
- Integration with dispensing tools like OptikamPad for frame selection and measurements
- Real-time order status tracking

**Billing & Claims:**
- Built-in coding assistance and automated claims submission
- Integrated clearinghouse processing (via RevClear/TriZetto)
- Real-time insurance eligibility verification (via ABB Verify, Aloha, Ensora Health/APEX EDI)
- Ledger reconciliation and insurance remittance posting
- Patient billing and account balance tracking

**E-Prescribing:**
- Electronic prescribing via RXNT integration (additional subscription required)
- Surescripts connectivity implied by e-prescribing capability

**Patient Engagement & Portal:**
- Online patient portal with self-service scheduling
- Patient intake forms (via RevIntake or IntakeQ integration)
- Automated appointment reminders and patient communication (via integrations with Weave, SolutionReach, DemandForce, etc.)
- Patient surveys
- RevEngage module for reputation management and marketing campaigns
- Payment processing (via RevPayments / Global Payments)

**Clinical Quality Measures & Reporting:**
- RevAspire module for CMS quality reporting
- 9 certified clinical quality measures
- MIPS/quality reporting support

**Interoperability & Data Exchange:**
- RevDirect module for secure Direct messaging between providers (additional subscription)
- FHIR API server for data interoperability
- Single and population-level patient data export
- Bulk data exchange support
- Transitions of care (C-CDA) document exchange

**Add-on Modules (Rev Suite):**
- **RevAspire** — CMS quality reporting
- **RevBilling** — Claims management
- **RevClear** — Claim processing/clearinghouse
- **RevDirect** — Secure Direct messaging between providers
- **RevEngage** — Patient engagement, reputation management, marketing
- **RevIntake** — Online scheduling and patient registration
- **RevPayments** — Payment processing

### Data & Content

Based on the features, integrations, and user reviews described above, RevolutionEHR stores and manages the following categories of data:

**Clinical/Exam Data:** Optometric exam records with customizable templates, patient chief complaints, visual acuity measurements, refraction data, slit lamp findings, fundus exam results, intraocular pressure measurements, and other eye-specific clinical data. Specialty exam data for low vision and vision therapy. The system stores data from integrated diagnostic equipment (OCT scans, visual fields, retinal imaging, autorefraction, tonometry, etc.).

**Patient Demographics & Insurance:** Patient identity, demographics, contact information, insurance coverage details, and insurance eligibility data.

**Images & Diagnostic Data:** Ophthalmic images from integrated diagnostic devices (retinal photos, OCT images, visual field plots, corneal topography). The product includes a picture archiving system (PACS).

**Optical/Dispensing Data:** Eyeglass prescriptions, contact lens prescriptions, frame selections, lens orders, contact lens orders, optical inventory, and order fulfillment status from suppliers.

**Billing & Financial Data:** Insurance claims, claim status, remittance advice, patient account balances, payment transactions, ledger records, eligibility verification results.

**Scheduling Data:** Appointment schedules, appointment history, patient communication logs from automated reminders.

**Prescriptions:** Electronic prescription data (via RXNT integration), medication lists, prescription history.

**Patient Portal Data:** Patient-submitted intake forms, survey responses, portal messages, self-scheduled appointments.

**Provider Communication:** Direct secure messages between providers (via RevDirect).

**Quality Measure Data:** Clinical quality measure calculations and reporting data for CMS/MIPS programs.

**Audit/Administrative Data:** User access logs, staff roles and permissions, task lists, multi-location configuration.

**Evidence basis:** The vendor website explicitly describes integrated billing with claims processing, optical dispensing with order tracking, diagnostic equipment integration, patient portal functionality, e-prescribing via RXNT, quality reporting, and Direct messaging. User reviews confirm the system handles "exams, optical, scheduling, billing" as an integrated package. The Capterra and search-result reviews describe customizable clinical documentation, optical workflows, and billing/coding tools. The vendor's integration page lists specific connections to 30+ third-party systems spanning claims, equipment, patient communication, payments, analytics, practice management, and prescribing/ordering.

**Gaps/Uncertainty:** The website doesn't clearly describe lab ordering or lab result management beyond optical orders. It's unclear whether the system stores referral tracking data for specialist referrals. The vendor doesn't appear to support inpatient or surgical workflows. The relationship between the core product and the "Rev" add-on modules in terms of data storage is somewhat ambiguous — it's unclear whether RevBilling and RevClear data is stored within RevolutionEHR's database or in separate systems.

---
