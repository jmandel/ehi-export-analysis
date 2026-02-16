# Compulink Healthcare Solutions — Product Research

Researched: 2026-02-16
Developer website: https://www.compulinkadvantage.com

## Overview

Compulink Healthcare Solutions (formerly just "Compulink" — rebranded in June 2018) is a privately held health IT company founded in 1985, headquartered in Newbury Park, California. The company started with practice management software and added one of the industry's first EHR products in 1994, well before the Meaningful Use mandate. As of the 2018 name-change announcement, Compulink had approximately 160 US-based employees and served over 20,000 providers across 4,700+ locations. More recent data (2025) suggests ~201 employees. The company is privately held; CEO is Link Wilson.

Compulink's core identity is as a **specialty-focused EHR and practice management** vendor. Their strongest presence is in **eye care** (ophthalmology and optometry), but they have expanded to serve 13+ medical specialties including addiction medicine, audiology, behavioral/mental health, dermatology, gastroenterology, orthopedics, otolaryngology (ENT), pain management, physical therapy, podiatry, and urology. They are notably deployed in 16 ophthalmic colleges and universities. The product is marketed as an "all-in-one" solution that combines EHR, practice management, billing, patient engagement, optical POS, ASC management, and analytics in a unified platform. Available cloud-hosted or on-premise (server-based).

## Product: Compulink Advantage (branded as "Advantage Intelligence")

CHPL ID: 8873

### What It Is

Compulink Advantage is an all-in-one EHR and practice management platform designed for specialty medical practices. The certified module is Version 12, certified November 2017. It carries a broad certification profile: (a)(1)–(a)(5), (a)(12), (a)(14) for clinical capabilities; (b)(1)–(b)(3), (b)(10)–(b)(11) for care transitions and EHI export; (c)(1)–(c)(3) for clinical quality measures; (e)(1), (e)(3) for patient access; (g)(7), (g)(9)–(g)(10) for FHIR/API access; and (h)(1) for direct messaging. This broad certification footprint indicates the product handles clinical documentation, e-prescribing, care coordination, patient portal, quality reporting, and API-based data exchange.

The certified module appears to be the full product — not a component of something larger. All modules (EHR, practice management, billing, patient engagement, optical, ASC) are part of the same integrated Advantage platform. The product is sold under specialty-specific branding (e.g., "Ophthalmology Advantage," "Optometry Advantage," "Orthopaedic Advantage") but these are configurations of the same underlying platform, not separate products.

### Users & Market

**Target users**: Physicians, clinical staff, billing staff, practice managers, and patients (via the patient portal). The SED intended user description is "Outpatient Clinic."

**Clinical settings**: Primarily ambulatory specialty practices — solo practitioners through multi-site groups. Strong presence in ophthalmology and optometry. Also serves orthopedics, dermatology, behavioral health, pain management, ENT, gastroenterology, podiatry, urology, audiology, addiction medicine, and physical therapy. Supports ambulatory surgical centers (ASCs) connected to these practices. In 2018, Compulink debuted a multi-specialty group solution at HIMSS.

**Market size**: 20,000+ providers, 4,700+ locations. Pricing starts around $133/month per the marketing materials. Compulink competes in the mid-market specialty EHR space — not a large enterprise vendor, but well-established with a 40-year history.

**Reviews**: 4/5 stars on EMRSystems (37 reviews). Users praise customization options, the all-in-one integrated approach, and specialty-specific workflows. Common complaints include a steep learning curve, excessive clicking for some tasks, occasional post-update glitches, and system crashes. Customer support receives mixed feedback — some say it's responsive, others say it isn't.

### Modules & Functionality

Based on vendor website, press releases, and third-party review sources, Compulink Advantage includes these major modules:

**Electronic Health Records (EHR)**
- OneTab single-page charting layout customizable per provider
- Specialty-specific templates and workflows (e.g., glaucoma flowsheets, cataract/LASIK documentation for ophthalmology)
- AI-powered features: Ambient Virtual Scribe, SMART Orders (auto-generates treatment plans from diagnosis codes and historical ordering patterns), branded as "Advantage AI Practice"
- Customizable healthcare graphs and charts
- E-prescribing via Surescripts integration
- Lab interfacing and lab orders
- PQRS/quality measure coding assistance
- Clinical decision support
- Problem lists, medication lists, allergies, demographics (per certified criteria)
- CCDA generation and import for transitions of care

**Practice Management**
- Appointment scheduling with flexible views
- Patient registration and demographic management
- Insurance verification (automated, including vision insurance plans)
- Patient tracking and management workflows
- Staff productivity tools

**Medical Billing / Revenue Cycle Management**
- Integrated billing with "SMART billing tools" (claim generation, scrubbing)
- Denial management
- Revenue cycle management services (optional outsourced billing with dedicated billing managers)
- Price transparency / cost estimation for patients
- Text-to-pay and digital payment processing (credit card, debit, digital wallets)

**Patient Engagement (branded "Promptly" / "DREAM Suite" / "Advantage Patient Experience")**
- Patient portal for viewing records (per e(1) certification)
- Online appointment scheduling (self-schedule or request)
- Online pre-registration and demographic updates
- Mobile check-in (phone, tablet, kiosk) — auto-marks patient as arrived
- Digital forms with e-signatures, supporting 100+ languages
- Driver's license and insurance card scanning
- Automated messaging (text, email, voice) for reminders and balance alerts
- Referral portal (inbound/outbound referral tracking with file sharing)
- Reputation management (automated review solicitation)
- Integrated marketing tools

**Optical Point-of-Sale (POS)**
- Optical inventory management
- Lens and frame catalog (auto-updating optical plans and lens catalog)
- Job costing and cost-of-goods reporting
- Sales checkout workflows

**Ambulatory Surgical Center (ASC)**
- Data transfer from office EHR to surgical center (eliminates paper/double entry)
- Case scheduling and coordination
- Surgeon preference cards
- Pre-op and post-op assessment documentation
- Anesthesia documentation
- Medical supply/equipment inventory management
- Lab and pathology integration
- Administrative, statistical, and outcomes reporting

**eCommerce**
- Personalized online patient stores (contact lens ordering, etc.)
- Launched at AAO 2019 specifically for ophthalmology

**Imaging / DICOM**
- DICOM interface for diagnostic device integration
- PACS system for image storage, retrieval, and sharing
- Automatic image capture and push from diagnostic devices into PACS
- Mandatory disclosures page references DICOM conformance statement

**Analytics and Reporting**
- Clinical, financial, and operational analytics
- Advanced reporting tools

**Interoperability**
- Direct messaging (per h(1) certification)
- FHIR API (per g(10) certification)
- Surescripts e-prescribing
- CCDA import/export for transitions of care
- IHE participation (per mandatory disclosures page)

### Data & Content

Based on the certified criteria and documented features, Compulink Advantage stores and manages the following categories of data:

**Clinical data** (established by certified criteria and EHR features):
- Patient demographics, problems, medications, allergies, vitals, lab results, clinical notes, encounter history, immunizations, care plans, assessment/plan documentation
- Specialty-specific clinical data: ophthalmic exam data (glaucoma flowsheets, cataract/LASIK documentation, visual acuity, ocular structures), orthopedic assessments, dermatology notes, etc.
- E-prescribing records (via Surescripts)
- Lab orders and results (via lab interfacing)
- Clinical quality measure data (per c(1)–c(3) certification)
- CCDAs (generated and received)

**Imaging data**:
- DICOM images from diagnostic devices
- PACS-stored images linked to patient records

**Administrative/billing data** (established by practice management and billing features):
- Appointment/scheduling data
- Insurance information (medical and vision plans)
- Claims data (generated, scrubbed, submitted)
- Payment records, patient balances
- Denial management records

**Patient engagement data** (established by Promptly/DREAM Suite features):
- Patient portal accounts and access logs
- Digital forms and signed consents
- Appointment requests and self-scheduling history
- Automated message logs (reminders, balance alerts)
- Referral records
- Patient reviews/feedback
- Scanned driver's licenses and insurance cards

**Optical/retail data** (established by Optical POS module):
- Frame and lens inventory
- Sales transactions
- Job costing data, cost-of-goods data
- Patient orders (including eCommerce contact lens orders)

**Surgical center data** (established by ASC module):
- Case schedules, preference cards
- Pre-op/post-op assessments
- Anesthesia records
- Surgical supply inventory
- Lab/pathology results
- Outcomes data

**Notable**: The mandatory disclosures page mentions integration with Updox (a patient communication/fax platform), which implies additional communication data may flow through the system. The breadth of the product — from clinical EHR to optical POS to ASC management to eCommerce — means the total data footprint is quite large for a specialty EHR.
