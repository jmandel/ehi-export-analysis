# Core Solutions Inc — Product Research

Researched: 2026-02-15
Developer website: https://www.coresolutionsinc.com/about/

## Overview

Core Solutions Inc is a behavioral health and intellectual/developmental disabilities (IDD) software company founded in 1999 and headquartered in the Philadelphia, PA area (Devon, PA). The company specializes in EHR and practice management technology purpose-built for mental health, substance use disorder (SUD), and IDD providers. They claim over 25 years in the market, supporting "400K+ lives" and "35K users." The company is privately held and not publicly traded.

Core Solutions evolved from a billing software company (founded 1999) to a clinical EHR platform over time: they added clinical systems in 2003–2013, experienced significant growth in 2014–2018, expanded during COVID-19, launched the current Cx360 Enterprise platform in 2022, and introduced AI-powered tools (Cx360 Intelligence, Cx360 GO) starting in 2024. Their go-to-market is direct sales to behavioral health organizations, community mental health centers, IDD agencies, and child/family services organizations. They have a notable focus on Certified Community Behavioral Health Clinics (CCBHCs), a federally-defined model for comprehensive behavioral health care.

## Product: Cx360

CHPL IDs: 9168

### What It Is

Cx360 is an integrated EHR and practice management platform specifically designed for behavioral health, substance use disorder (SUD), and intellectual/developmental disabilities (IDD) providers. It is not a general-purpose ambulatory EHR — it is purpose-built for the behavioral health and IDD sector. The certified module (Cx360 version 7) appears to be the core of the entire Cx360 product suite, with several additional components:

- **Cx360 Enterprise**: The main scalable EHR platform for multi-service behavioral health organizations
- **Cx360 Intelligence**: An AI-powered analytics and reporting layer (includes CCBHC compliance reporting, operational dashboards, symptom tracking)
- **Cx360 GO**: A mobile app for ambient documentation, symptom tracking, electronic visit verification (EVV), and mileage tracking
- **DSP Assist**: A companion mobile tool for direct support professionals (IDD field staff), providing EVV, time tracking, medication management, and goal documentation

The product is cloud/SaaS-based, with pricing through a one-time deployment fee plus monthly per-user license fees. Additional modules (e-prescribing, labs, health information exchange, client portal) carry additional activation and usage fees.

### Users & Market

**Target users**: Clinicians (therapists, psychiatrists, counselors), case managers, direct support professionals, billing staff, practice administrators, and clients/patients (via portal). The CHPL metadata lists intended users as "Ambulatory Providers."

**Target settings**:
- Community mental health centers and CCBHCs
- Substance use disorder treatment programs
- IDD service agencies
- Child and family services organizations
- Multi-site behavioral health groups and health systems with behavioral health programs

**Market size**: Core Solutions claims 35,000+ users and 400,000+ lives served. They appear to be a mid-size niche vendor, not competing with Epic or Cerner but well-established in the behavioral health EHR space.

**Notable focus areas**: CCBHCs are a significant market focus — Core Solutions has built CCBHC-specific compliance reporting, quality measure tracking, and care coordination features into the platform. They also emphasize IDD services, which have distinct documentation requirements (person-centered planning, valued outcomes, EVV).

**Reviews**: Mixed reviews on Capterra and KLAS. Users praise ease of use, billing capabilities, and search functionality. Criticisms include limited training from the vendor, slow product updates at times, and suitability concerns for some substance abuse facility charting. KLAS users noted the vendor had improved support responsiveness over time. Some users said they would buy the product again, particularly for billing.

### Modules & Functionality

Based on vendor website, press releases, and mandatory disclosures, Cx360 includes the following modules and capabilities:

**Clinical / Care Management:**
- Comprehensive assessments covering medical, addiction, social, and psychiatric history
- Evidence-based screening tools (depression, PTSD, anxiety, and others)
- Treatment planning with trackable goals and person-centered life plans (IDD)
- Progress notes linked to treatment goals
- Medication management and medication administration records
- Risk assessment and client risk stratification/scoring
- Measurement-based care (tracking client change over time via scheduled self-surveys and assessments)
- Clinical dashboards and decision support
- Preconfigured templates and configurable workflows/forms

**Scheduling & Workflow:**
- Appointment scheduling
- Workflow engine with automated task triggering (tasks auto-generate upon completion of prior tasks)
- Call tracking for referral management
- Configurable alerts and notifications for deadlines and authorizations

**E-Prescribing:**
- Integrated via third-party Dr. First integration (per mandatory disclosures)
- Drug interaction checking (CPOE criteria certified)

**Laboratory:**
- Electronic labs/CPOE for order transmission and result retrieval (per mandatory disclosures)

**Telehealth:**
- Built-in HIPAA-compliant telehealth directly in the platform
- Clinician availability scheduling with personalized client invitations

**Client Portal / Engagement:**
- Patient/client portal for reviewing and completing documentation
- Secure messaging between clients and care team
- Bill payment and eCommerce functionality (credit card pre-payment)
- Client self-surveys and assessments (ad hoc or scheduled)

**Revenue Cycle Management / Billing:**
- Automated ledger and bill generation with rule-based customization
- Claims submission and claim scrubbing
- Authorization management (tracking provider credentialing with payors)
- Accounts receivable management (payment tracking, follow-up on unpaid claims)
- Tracking reports and embedded billing files

**Reporting & Analytics:**
- Customizable dashboards and reporting
- CCBHC-specific compliance reporting (federal, state, operational)
- Operational reports: access/availability, client demographics, staffing/credentialing, supervision/license tracking, service delivery, state-mandated roster files
- Quality measures / CQMs (certified for c(1)–c(4))
- AI-powered analytics via Cx360 Intelligence

**Health Information Exchange:**
- HL7 connections (monthly per-connection fees based on user count/volume)
- Direct Secure Messaging via HISP providers (per-transaction charges)
- FHIR API access (certified for g(7), g(9), g(10))
- Transitions of care / CCDA (certified for b(1))

**Mobile / Field:**
- Cx360 GO: ambient documentation via AI conversation capture, automatic session note generation, symptom tracking, EVV, GPS/time stamping, mileage tracking, offline capability
- DSP Assist: EVV, time tracking, medication management, goal documentation for IDD direct support professionals
- Mobile documentation for field-based staff in residences and community settings

**IDD-Specific:**
- Person-centered life plans/service plans
- Valued outcomes tracking (needs identified automatically flow to plans)
- Task assignment to staff for achieving quality outcomes
- Audit-ready records for IDD compliance
- Foster care management module with secure multi-record visibility

**Child & Family Services:**
- Family portals and trauma-informed communication
- Foster care management
- Compliance with Title IV-E, CAPTA, and COA requirements
- State child welfare standards support

**Compliance & Security:**
- HIPAA compliance
- Audit trail / authentication (certified for d-criteria)
- Configurable compliance tracking
- Automated documentation and regulatory reporting

### Data & Content

Based on the features and modules described above, Cx360 stores and manages the following categories of data:

**Clinical data**: Patient/client demographics, medical/addiction/social/psychiatric history, clinical assessments, screening results (depression, PTSD, anxiety, etc.), diagnoses (ICD-10), treatment plans and goals, progress notes, session summaries, medication lists and administration records, lab orders and results, risk scores and stratification data, measurement-based care outcomes/surveys.

**Scheduling data**: Appointments, clinician availability, telehealth session records.

**Billing/financial data**: Claims, billing codes, ledger entries, payment records, accounts receivable, authorization/credentialing status with payors, client credit card information (for portal payments), reimbursement tracking.

**Communication data**: Secure messages between clients and providers, care team communications, direct secure messages (via HISP), referral tracking/call logs.

**Documents and forms**: Configurable clinical forms and templates, completed assessments, treatment plans, progress notes, compliance documentation.

**Mobile/field data**: EVV records (GPS location, timestamps), mileage logs, ambient documentation transcripts, session audio-to-note conversions (via Cx360 GO).

**IDD-specific data**: Person-centered life plans, valued outcomes, DSP task assignments and completions, behavioral tracking data, goal documentation.

**Child & family services data**: Foster care records, family engagement records, case management documentation, compliance records (Title IV-E, CAPTA, COA).

**Operational/administrative data**: Staff credentialing, supervision/license tracking, audit trails, compliance reports, CCBHC quality measures, organizational dashboards, user activity logs.

**Exchange data**: CCDAs/transitions of care documents, HL7 messages, FHIR resources.

**Notable absences or uncertainties**: The vendor website does not prominently describe imaging/radiology, complex surgical workflows, or inpatient/hospital-specific features — consistent with an ambulatory behavioral health focus. Physical health documentation appears limited to what's relevant for integrated behavioral health care (e.g., basic medical history, vital signs for medication management) rather than comprehensive primary care charting. The product does not appear to be certified for public health reporting criteria (f-criteria), suggesting limited immunization registry, syndromic surveillance, or cancer registry functionality.
