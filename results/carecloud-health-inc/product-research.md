# CareCloud Health, Inc. — Product Research

Researched: 2026-02-14
Developer website: http://www.carecloud.com

## Overview

CareCloud, Inc. (NASDAQ: CCLD) is a publicly traded healthcare IT company headquartered in Somerset, New Jersey, with approximately 4,000 employees worldwide and over 40,000 healthcare providers using its solutions across 50 states. The company was originally founded in 1999 as Medical Transcription Billing Corporation (MTBC), focused on transcription and manual medical billing for practices in New Jersey.

MTBC went public on NASDAQ in 2014 and made 16+ acquisitions of RCM and healthcare IT companies. In 2020, MTBC acquired two major companies: **CareCloud Corporation** (a Miami-based cloud EHR/PM company founded in 2009 by Albert Santalo, reportedly for ~$36M) and **Meridian Medical Management** (~$24.8M). In March 2021, MTBC rebranded itself as CareCloud, Inc., adopting the acquired company's name. This history is important context: the current CareCloud platform is an amalgamation of technologies from multiple acquisitions.

CareCloud serves ambulatory medical practices across a wide range of specialties, from solo practices to large medical groups, academic institutions, and health systems. Their go-to-market combines direct SaaS sales with managed services (outsourced billing/RCM). Reported first-quarter 2021 revenue was ~$29.8M (36% YoY growth driven by acquisitions). Specialties mentioned include internal medicine, family practice, cardiology, gastroenterology, neurology, orthopedics, nephrology, dermatology, urology, pain management, general surgery, and others. The CHPL SED certification was specifically tested with "Pediatric Nephrology" users, though the product itself is multi-specialty.

Notably, CareCloud operates **multiple EHR products** under its umbrella: **CareCloud Charts** (the certified product), **talkEHR** (another EHR platform), and **VertexDR** (designed for anesthesiology). This research focuses on CareCloud Charts as the certified product.

## Product: CareCloud Charts

CHPL ID: 11173

### What It Is

CareCloud Charts is a cloud-based Electronic Health Record (EHR) system, part of CareCloud's integrated healthcare platform. It is broadly certified across 30+ ONC criteria covering clinical documentation (a)(1)–(a)(5), (a)(12), (a)(14), care coordination (b)(1)–(b)(3), patient portal (e)(1), public health (f)(1), (f)(3), clinical quality (c)(1)–(c)(3), and FHIR API (g)(7), (g)(9), (g)(10) — indicating a full-featured clinical EHR with patient engagement, interoperability, and reporting capabilities.

Charts is one component of CareCloud's broader platform, which includes:
- **CareCloud Central** — Practice management (scheduling, billing, claims)
- **CareCloud Breeze** — Patient experience management (portal, intake, payments)
- **CareCloud Analytics** — Reporting and business intelligence
- **CareCloud Live** — Telehealth
- **cirrusAI** — AI-powered clinical documentation and decision support

The certified module is Charts (the EHR), but the *product* in practice is the integrated platform — Charts + Central + Breeze are sold and used together, and data flows between them.

### Users & Market

CareCloud Charts is used by ambulatory practices — physicians, clinical staff, billing staff, and practice administrators. The platform serves practices of varying sizes from solo providers to large multi-site groups. Per the vendor website, over 40,000 providers use CareCloud solutions. Specialty coverage is broad, with the vendor explicitly marketing to cardiology, family medicine, gastroenterology, internal medicine, nephrology, neurology, orthopedics, pulmonology, urology, dermatology, allergy/immunology, chiropractic, and others.

User reviews (from findemr.com, medesk.net) are mixed: praise for intuitive interface, workflow efficiency, and scheduling; criticism for slow performance, customer support responsiveness, high pricing ($628/provider/month for EMR+PM), and steep learning curves. Contracts are typically 3-year commitments.

### Modules & Functionality

Based on vendor website feature pages, product tours, and third-party reviews:

**Clinical Documentation (Charts)**
- Configurable, specialty-specific templates with charting-by-exception
- Integrated order sets and reusable care protocols
- Content Store: a marketplace to build and share templates across providers/practices
- cirrusAI Notes: ambient AI listening that auto-generates clinical documentation from patient-provider conversations
- cirrusAI Guide: automates clinical data input and provides real-time evidence-based recommendations
- Clinical decision support: drug-drug interactions, drug-allergy checking, evidence-based alerts

**E-Prescribing**
- 1-click ePrescribing with pharmacy lookup
- Integrated with Surescripts (inferred from e-prescribing capabilities, standard for certified EHRs)

**Lab & Imaging**
- 1-click lab ordering
- Lab results management in unified inbox
- X-ray/imaging ordering
- Results review and trending

**Patient Flow & Scheduling**
- Real-time patient flow board (check-in to check-out) with drag-and-drop
- Color-coded scheduling views (daily/weekly/monthly)
- Multi-provider, multi-location scheduling
- Room utilization tracking, patient wait time monitoring
- Automated text, email, and call appointment reminders

**Practice Management (Central)**
- Billing with auto-populated fields, diagnosis/CPT code lookups
- CollectiveIQ: billing rules engine that detects claims errors before submission
- Automated claims submission (nightly batch processing)
- Insurance eligibility verification
- Denial management
- E&M code translation from clinical encounters
- Claims tracking and revenue cycle analytics

**Patient Experience (Breeze)**
- Online patient portal with access to medical records, test results, treatment plans
- Digital check-in (at home or in-office via QR code)
- Customizable intake forms that flow into PM and EHR
- Online appointment scheduling and rescheduling
- Two-way secure patient messaging
- Online bill pay (credit card, e-check, saved cards, payment plans)
- Automated payment processing

**Telehealth (Live)**
- HIPAA-compliant video visits
- Integrated with EHR and scheduling
- Cross-platform (web, iOS, Android)

**Analytics & Reporting**
- Customizable dashboards with financial and clinical insights
- Quality initiative tracking (MIPS, CQMs)
- Population health management analytics
- KPI dashboard for practice performance
- Predictive analysis

**AI Capabilities (cirrusAI)**
- cirrusAI Notes: ambient clinical documentation
- cirrusAI Guide: clinical decision support and workflow automation
- cirrusAI Appeals: automated insurance appeal generation
- cirrusAI Chat: virtual assistant for EHR navigation
- stratusAI Desk Agent: AI-powered front desk assistant (calls, scheduling)

**Additional Services (managed/outsourced)**
- Revenue Cycle Management (outsourced billing)
- Medical coding and transcription
- Physician credentialing
- Chronic care management
- Remote patient monitoring
- Staff augmentation

### Data & Content

Based on the vendor's feature descriptions and product pages, CareCloud Charts and its integrated platform store and manage the following data:

**Clinical Data (Charts EHR)**
- Patient demographics and medical histories
- Clinical encounter notes and visit documentation
- Problem lists, diagnoses (ICD-10)
- Medication lists and prescription history (ePrescribing data)
- Allergy and adverse reaction records
- Vital signs
- Lab orders and results
- Imaging orders
- Immunization records
- Clinical care plans and treatment plans
- Clinical decision support alerts and interactions
- Order sets and clinical templates
- Quality measure data (CQMs, MIPS)

**Administrative & Financial Data (Central PM)**
- Appointment schedules across providers/locations
- Insurance/payer information and eligibility data
- Billing charges, CPT/E&M codes
- Claims (pre- and post-submission)
- Claim denial records
- Payment records and collections data
- Revenue cycle analytics

**Patient Engagement Data (Breeze)**
- Patient portal accounts and login history
- Digital intake form submissions
- Patient-provider secure messages
- Appointment requests and confirmations
- Online payment transactions
- Check-in records

**Telehealth Data (Live)**
- Virtual visit records (integrated with EHR encounters)

**Public Health Data**
- Immunization registry submissions (f)(1)
- Syndromic surveillance data (f)(3)

**Interoperability Data**
- C-CDA documents (transitions of care) — certified for (b)(1)–(b)(3)
- FHIR API resources — certified for (g)(7), (g)(9), (g)(10)

The product is cloud-hosted, which means all data resides in CareCloud's infrastructure. The vendor's marketing consistently emphasizes the integrated nature of clinical, administrative, and financial data flowing across Charts, Central, and Breeze. This is relevant for EHI export: the "product" is the integrated platform, and export should cover data across all these components.

**Gaps/Uncertainties:**
- The website doesn't mention document/image storage (scanned documents, uploaded files) explicitly, though this is common in EHRs
- Chronic care management and remote patient monitoring are mentioned as services; unclear how much of that data lives in Charts vs. separate systems
- The relationship between Charts and the other EHR products (talkEHR, VertexDR) is unclear — they may share backend infrastructure or be entirely separate
- Audit logs and system administration data are not described on marketing pages but would be expected for a certified product
