# Qualifacts Systems, LLC — Product Research

Researched: 2026-02-16
Developer website: https://www.qualifacts.com

## Overview

Qualifacts Systems, LLC is one of the largest behavioral health and human services EHR providers in the United States, serving over 2,500 customer agencies representing approximately 75,000 providers and more than 6 million patients across all 50 states. The company is headquartered in Nashville, Tennessee, with additional offices in Tampa and global employees. It was founded in 2000 and describes itself as having over 25 years of experience in the behavioral health technology space.

The company has gone through several ownership and consolidation phases. In 2014, Great Hill Partners made a majority investment. In September 2019, Warburg Pincus acquired Qualifacts. In August 2020, Warburg Pincus and Martis Capital merged their respective portfolio companies — Qualifacts and Credible Behavioral Health — combining CareLogic with Credible's platform. In December 2021, the combined entity acquired InSync Healthcare Solutions, doubling the customer count and enabling service to over 10 million patients. The combined company rebranded under the Qualifacts name, operating three distinct EHR platforms: **CareLogic**, **Credible**, and **InSync**. Each platform targets different segments of the behavioral health market. Qualifacts was ranked #1 in Best in KLAS for Behavioral Health EHR in 2022 and 2023. It was also recognized as a top-25 healthcare software company of 2025 by Capterra.

## Product: CareLogic

CHPL ID: 9807

### What It Is

CareLogic Enterprise is a cloud-based (SaaS) electronic health record platform designed specifically for behavioral health and human services organizations. It is positioned as an enterprise-grade solution for multi-location, multi-state organizations providing value-based care. The certified module is "CareLogic Enterprise S3," and it represents the full CareLogic platform — not a subset of a larger product. CareLogic has been in the market for over 20 years.

CareLogic is broadly certified across clinical (a)(1)–(a)(5), (a)(12), (a)(14), transitions of care (b)(1)–(b)(3), patient portal (e)(1), public health reporting (f)(1), (f)(7), FHIR APIs (g)(7), (g)(9), (g)(10), and other criteria — indicating a full clinical EHR with integrated data exchange capabilities.

The SED intended user description is "Outpatient Clinic," confirming its primary use in outpatient behavioral health settings.

### Users & Market

CareLogic serves enterprise-level behavioral health organizations, including:
- **Certified Community Behavioral Health Clinics (CCBHCs)** — Qualifacts claims to partner with one-third of all CCBHCs nationwide
- **Community mental health centers**
- **Substance abuse and addiction treatment facilities**
- **Intellectual and Developmental Disability (I/DD) providers**
- **Autism services providers**
- **Health and human services organizations**
- **Multi-site and multi-state behavioral health agencies**

The typical deployment is practices with 11+ physicians/providers. Day-to-day users include clinicians (therapists, psychiatrists, counselors), prescribers, billing staff, practice managers, and administrative staff. Patients/clients interact via the patient portal.

Within Qualifacts' three-platform portfolio, CareLogic targets enterprise organizations, while Credible targets large CCBHCs and multi-location entities, and InSync targets small-to-mid-size practices. There appears to be some overlap between CareLogic and Credible in the CCBHC and enterprise segments.

### Modules & Functionality

Based on vendor materials, review sites, and third-party profiles, CareLogic includes the following integrated modules and capabilities:

**Clinical Documentation & Treatment Planning**
- Configurable clinical documentation with custom service documents and form builder
- Treatment planning with automated workflows, goal/objective tracking, and alignment with assessments and outcomes
- Library of evidence-based clinical assessments and outcome instruments
- Progress notes and SOAP notes
- Clinical decision support with alerts, reminders, and guidelines integrated into workflows
- AI-powered clinical documentation via "Qualifacts iQ" (released July 2025), which transcribes appointments and generates notes automatically

**Intake & Patient Management**
- Patient demographics, medical history, and diagnosis tracking
- Intake workflows with configurable forms
- Single-screen views of client information for care team collaboration
- Document scanning, importing, and organization by patient history

**Scheduling**
- Provider scheduling by specialty and availability
- In-person and virtual appointment management
- Automated appointment reminders to reduce no-shows
- Room scheduling integration

**ePrescribing & Medication Management**
- Electronic prescribing integrated into the clinical workflow
- Medication management and adherence tracking
- Particularly emphasized for IDD and autism care populations

**Billing & Revenue Cycle Management**
- Claim validation and service alerts before submission
- Clean claims generation with bulk update capabilities
- Eligibility inquiries and claims scrubbing
- Direct-to-carrier claims processing
- Invoice generation, payment tracking, accounts receivable management
- State-specific billing rules and matrices (supporting 88+ state reports)
- CCBHC billing support
- Value-based reimbursement (VBR) program support
- Customers report "an adjusted collections rate 4% higher than the industry average"

**Patient/Client Portal**
- Mobile-friendly portal (web, iOS, Android) with organizational branding
- Digital form assignments with automated reminders and eSignature
- Self-serve access to treatment plans, appointments, and documents
- In-portal payment module (view balances, make payments, access receipts)
- Broadcast messaging for mass client communications
- Telehealth/video appointments for up to 50 individuals
- Demographic data mapping from portal to medical records

**Telehealth / Virtual Care**
- Integrated telehealth with video appointments
- Branded client engagement portal (OnCall Virtual Care)
- Instant messaging capabilities

**Electronic Visit Verification (EVV)**
- Integrated EVV module for IDD and home-based services
- Multiple verification methods: GPS, phone, QR code
- Data transport to state data aggregators
- Available as an add-on module (not included in base pricing)

**Reporting & Analytics**
- Advanced reports and analytics dashboards
- Business intelligence capabilities
- Support for 16 Clinical Quality Measures (CQMs)
- MIPS and APM reporting
- Outcome tracking and data visualizations
- State compliance reporting (88+ state-specific reports)

**Integrations & Interoperability**
- Laboratory integration
- Health Information Exchange (HIE) connectivity
- Hospital and third-party software integrations
- FHIR API access (certified for g(7), g(9), g(10))
- Direct messaging for care coordination

**Compliance & Regulatory**
- HIPAA compliance
- 42 CFR Part 2 compliance (substance abuse confidentiality)
- CCBHC program requirements
- State-specific regulatory compliance across all 50 states

**Inpatient/Residential Support**
- Admission and discharge management
- Bed tracking (mentioned on findemr.com)

### Data & Content

Based on the features and modules described above, CareLogic stores and manages the following types of data:

**Clinical data**: Patient demographics, medical history, diagnoses (ICD codes), treatment plans with goals and objectives, clinical assessments and outcome instruments, progress notes, SOAP notes, clinical encounter documentation, and custom service documents. The (a)(1)–(a)(5) certification confirms it stores CPOE data, demographics, problem lists, medication lists, medication allergy lists, and clinical decision support data.

**Medication data**: Prescription records, medication lists, medication allergy lists, and medication management records. The ePrescribing module implies Surescripts or similar connectivity, meaning prescription data flows through the system.

**Billing & financial data**: Claims data, eligibility records, invoices, payment records, accounts receivable, billing matrices, and state-specific billing configurations. The integrated billing module means financial data is stored within the same system as clinical data.

**Scheduling data**: Appointment records, provider availability, room bookings, and appointment reminder logs.

**Patient portal data**: Patient-submitted forms with eSignatures, portal messages, broadcast communications, telehealth session records, and payment transactions.

**EVV data**: Visit verification records including GPS coordinates, phone check-ins, QR code scans, timestamps, and provider/client identifiers (when EVV module is active).

**Compliance & reporting data**: Clinical quality measures, state reporting data, MIPS/APM data, and audit trails.

**Document management**: Scanned documents, imported files, and attachments organized by patient.

**Administrative data**: User accounts, provider credentials, organizational configurations, and custom form definitions.

**Notable gaps in research**: The vendor's website does not clearly describe whether CareLogic stores lab results directly (it mentions lab integration but not result storage), and the extent of inpatient/residential data is only briefly mentioned on third-party sites. The (c)(1)–(c)(3) certification for clinical quality measures and the (f)(1) immunization reporting certification suggest the system stores immunization data and structured clinical quality data, though these aren't prominently featured in marketing materials (likely because the primary market is behavioral health, where immunizations are less central). The (h)(1) direct messaging certification confirms the system can send and receive clinical messages.
