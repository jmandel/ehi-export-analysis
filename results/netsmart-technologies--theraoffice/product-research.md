# Netsmart Technologies — Product Research

Researched: 2026-02-16
Developer website: https://www.ntst.com/

## Overview

Netsmart Technologies is a large, privately held health IT company headquartered in Overland Park, Kansas, with approximately 2,500 employees and estimated annual revenue of ~$500–550M. The company has over 50 years of history in community-based healthcare technology. Netsmart is currently owned by private equity firms GI Partners and TA Associates (since 2018). Prior ownership history includes Genstar Capital (2010–2016) and a joint venture with Allscripts (2016–2018).

Netsmart's primary markets are behavioral health, human services, post-acute care (home health, hospice, skilled nursing), and senior living. Their main EHR platform is called CareFabric, which encompasses several distinct products: myAvatar (behavioral health), myEvolv (human services/addiction treatment), myUnity (post-acute care), GEHRIMED (geriatric medicine), and TheraOffice (physical therapy/rehabilitation). They also offer myHealthPointe (patient engagement), myInsight (public health), and CarePathways (quality measures).

Netsmart acquired TheraOffice in April 2022, adding outpatient physical therapy and rehabilitation to their portfolio. TheraOffice was originally founded in 2001 by Dan Morrill (a practicing physical therapist) and Ryan Havlick (a software developer) and operated independently under the company name Hands On Technology, Inc. before the acquisition.

## Product: TheraOffice

CHPL ID: 11493

### What It Is

TheraOffice is a specialty EMR and practice management platform designed specifically for outpatient physical therapy, occupational therapy, and speech-language pathology (SLP) practices. It is an all-in-one system combining clinical documentation, scheduling, billing/revenue cycle management, and reporting in a single integrated platform. The certified module (TheraOffice v14.1) appears to be the full product — not a component of something larger, though it now integrates with Netsmart's broader CareFabric ecosystem.

The product is cloud-hosted (available as both on-site and web-based historically, but now primarily cloud-based) and HIPAA-compliant. It was ONC-certified (Cures Update) on June 28, 2024, by Drummond Group, with a broad set of criteria including clinical data (a)(1),(a)(5),(a)(12),(a)(14), transitions of care (b)(1)–(b)(3), patient portal (e)(1),(e)(3), clinical quality measures (c)(1)–(c)(3), public health reporting (f)(1),(f)(5), FHIR API (g)(10), and direct messaging (h)(1).

### Users & Market

TheraOffice serves outpatient rehabilitation practices — primarily small to mid-size physical therapy clinics, but also occupational therapy and speech-language pathology practices. The product was named #1 EMR and Practice Management solution for physical therapy and outpatient rehabilitation in the 2025 Black Book Research Survey, with 902 rehabilitation/PT practices evaluating 58 competing products.

Netsmart reports TheraOffice is used by over 900 practices. The typical users are physical therapists, occupational therapists, speech-language pathologists, billing staff, and practice managers. It supports both pediatric and adult outpatient rehabilitation, as well as home health rehabilitation (Medicare Part B) and specialty rehabilitation services including pelvic health, vestibular, low vision, and lymphedema.

The product targets private therapy practices and multi-site rehab groups. It serves both solo practitioners and multi-location operations, with centralized administrative monitoring across sites.

### Modules & Functionality

Based on vendor materials, press releases, and third-party reviews, TheraOffice has the following core modules and features:

**Clinical Documentation**
- Over 40 customizable templates covering PT, OT, SLP, McKenzie, lymphedema, pelvic health, pediatric, and vestibular specialties
- Claims to reduce documentation time by up to 80% — daily notes in 1–2 minutes, initial evaluations in 5–7 minutes
- Goal creation tools and treatment planning
- Condition/pain history tracking
- AI documentation assistant with speech-to-text and noise filtering for hands-free charting
- MIPS (Merit-Based Incentive Payment System) documentation and quality measure support — TheraOffice operates as a Qualified Registry for Medicare compliance

**Scheduling**
- Appointment scheduling with recurring appointment support
- Mobile check-in and intake validation
- Co-pay collection at check-in
- Schedule Optimizer tool to automatically fill cancellations from waitlists
- Online patient scheduling (patient-facing appointment booking)

**Billing & Revenue Cycle Management**
- Fully integrated billing connected to scheduling and documentation
- Claims processing (submission, tracking, denial management)
- ERA (Electronic Remittance Advice) downloads
- Denial tracking and aging reports
- Payment posting automation
- Collections management
- Telemedicine billing
- TheraOffice Pay: integrated card processing, tap-to-pay, mobile payments (Apple/Google Pay), chip reader support
- Ability to save patient card profiles for recurring payments

**Patient Portal**
- Digital patient intake (eliminates paper forms)
- Prescription requests and refill checking
- Appointment booking
- Online payments
- Patient-provider communication/messaging
- Access to health records (HIPAA-compliant)

**E-Prescribing**
- Electronic prescription and refill capabilities
- Analysis of patient reports, treatment history, and insurance coverage for prescription generation
- Authorized refills for controlled substances (EPCS)

**Telehealth**
- Built-in virtual visit functionality integrated with scheduling, documentation, and billing

**Reporting & Analytics**
- 175+ built-in reports
- KPIs and productivity tracking
- HSA receipts
- Sign-in logs
- Visit history reports
- Custom report capabilities

**Communication & Document Management**
- Inbound/outbound e-faxing within the platform
- Automated appointment reminders
- Electronic referral management

**Integrations**
- Integration with Netsmart CareFabric ecosystem
- Third-party integrations including QuickBooks and Google Calendar mentioned by a review site (FindEMR)
- The ONC certification press release references "near seamless and secure exchange of patient health data and electronic referrals among different healthcare providers"
- Direct messaging (h)(1) certification implies support for Direct protocol for health information exchange
- FHIR API (g)(10) certification for standardized data access

**Compliance & Security**
- Automatic backups and redundant data storage
- Real-time traffic re-routing during outages
- Password misuse monitoring
- Multi-factor authentication
- Multi-level daily risk assessments
- 99.9% uptime claimed

### Data & Content

Based on the features and certifications described above, TheraOffice stores and manages the following categories of data:

- **Patient demographics**: Names, contact details, insurance information, patient registration data
- **Clinical documentation**: Evaluations, progress notes, daily notes, treatment plans, goals, condition/pain history — all via customizable templates across therapy specialties
- **Scheduling data**: Appointments, recurring schedules, cancellations, waitlists, check-in records
- **Billing and financial data**: Claims, ERA/remittance data, denial records, aging reports, payment transactions, patient card profiles, co-pay records, collections data, HSA receipt data
- **Prescriptions**: E-prescribing data including controlled substance prescriptions (EPCS), refill history
- **Patient portal data**: Patient messages, intake form submissions, appointment requests, online payment records
- **Telehealth records**: Virtual visit records (integrated with documentation and billing)
- **Fax/document management**: Inbound and outbound fax documents, referral documents
- **Quality measures**: MIPS/quality reporting data, clinical quality measure calculations
- **Outcome tracking**: Treatment effectiveness measures, care plan adjustments
- **Audit data**: Sign-in logs, user access records, audit events (certified for (d) criteria)
- **Public health reporting data**: Immunization data ((f)(1) certified), electronic case reporting ((f)(5) certified)

**Notable**: The certified criteria include (a)(5) Demographics, (a)(1) CPOE, (a)(12) Family health history, and (a)(14) Implantable device list — somewhat surprising for a PT-focused product, but these are required for ONC certification breadth. The (a)(1) CPOE certification implies the product supports some form of computerized provider order entry (likely for diagnostic tests, imaging referrals, or medication orders within the therapy context). The (a)(12) family health history criterion suggests the product stores family health history data. The (a)(14) implantable device list means the product can track patient implantable devices.

**Gaps in research**: The vendor website does not provide detailed technical documentation about the data model or database schema. The specific structure of how clinical notes, billing data, and patient records are stored internally is not publicly documented. Integration capabilities beyond what's listed are unclear — the vendor mentions "multiple other Netsmart solutions" but doesn't enumerate specific data exchange pathways. Whether TheraOffice stores lab results or imaging data directly (vs. receiving them via interfaces) is unclear from the marketing materials, though the (b)(1)–(b)(3) transitions of care certifications suggest it can receive and display C-CDA clinical summaries from other systems.
