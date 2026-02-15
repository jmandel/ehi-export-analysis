# Patagonia Health — Product Research

Researched: 2026-02-14
Developer website: https://patagoniahealth.com

## Overview

Patagonia Health is a privately held healthcare IT company founded in 2009 by Ashok Mathur, headquartered in Cary, North Carolina. The company builds an integrated cloud-based EHR, practice management, and billing platform specifically designed for **public health departments** and **behavioral health agencies**. This is a niche-focused vendor — rather than serving general ambulatory or hospital settings, Patagonia Health targets local/county health departments, statewide public health systems, school-based health clinics, and community behavioral health organizations.

The company claims to cover 60M+ lives across 38+ states and 510+ counties, with $622M+ in claims processed. They report a 98% client retention rate and have won consecutive Stevie Awards for customer service since 2015. Patagonia Health is a Certified NC Minority-Owned business. Notable customers include Fairfax County Health Department (Virginia), Cleveland County Health Department, Beaufort County Health Department, and Richmond and Stokes County Health Departments (North Carolina). The vendor appears to be mid-size, serving the public/behavioral health niche rather than competing with large general-purpose EHR vendors.

## Product: Patagonia Health EHR

CHPL ID: 11147

### What It Is

Patagonia Health EHR is a cloud-based, web-delivered SaaS application that combines electronic health records, practice management, billing, telehealth, and a patient portal into a single integrated platform. The product is specifically designed for public health and behavioral health workflows — not a general ambulatory EHR repurposed for these settings. It requires only a modern web browser and internet connection (no VPN or local installation needed). The certified module (Patagonia Health EHR Version 6) appears to be the full product — there is no indication that this is a subset of a larger platform. The certification covers 35+ criteria spanning clinical data (a)(1)-(a)(14), transitions of care (b)(1)-(b)(3), patient portal (e)(1), public health reporting (f)(1)-(f)(5), and FHIR APIs (g)(7)-(g)(10), indicating a comprehensive clinical system.

### Users & Market

**Primary customer segments:**
- **Local/county health departments** — the core market. These organizations handle immunizations, communicable disease surveillance, contact tracing, community outreach, and general public health services.
- **Statewide and federal health systems** — multi-location deployments with centralized reporting and a statewide master patient index.
- **Behavioral health agencies** — therapists, counselors, psychiatrists, clinical directors, and supervisors in community mental health and substance use treatment settings.
- **School-based health programs** — clinics operating in school settings.

**Day-to-day users** include clinicians (physicians, nurses, therapists, counselors, psychiatrists), clinical directors/supervisors, billing staff, front desk/registration staff, practice managers, and public health administrators. Patients interact through the MyHealth patient portal.

The product is positioned for small-to-medium organizations — county health departments, community behavioral health agencies — though it also scales to statewide deployments. Pricing starts at ~$500/user/month with modular scaling.

### Modules & Functionality

Based on vendor website, feature pages, third-party reviews, and case studies:

**Electronic Health Record (Clinical Documentation)**
- Customizable clinical templates (described as configurable to match paper forms the organization was previously using)
- Write-in sections for custom clinical information
- Document upload functionality
- Electronic charting with multiple input methods
- Clinical quality measures (CQM) tracking and reporting
- Support for behavioral health-specific documentation: psychiatric assessments, treatment plans, progress notes, group notes, case management notes
- DSM-5 coding support (DSM V database referenced on technology page)

**E-Prescribing**
- Medication selection from extensive database
- Automatic drug interaction and allergy checking
- Secure electronic transmission to pharmacies
- Surescripts connectivity implied by e-prescribing certification criteria

**Lab Integration**
- Lab order management
- Lab results viewing for clinicians and patients
- Interfaces with LabCorp, Solstas, and Quest Diagnostics (per technology page)

**Immunization & Public Health Programs**
- Vaccine inventory tracking
- Immunization registry synchronization with state registries
- Communicable disease surveillance and tracking
- Contact tracing support
- Community outreach program management
- Support for mobile off-site clinics
- State-specific program eligibility and reporting (e.g., HRSA UDS reporting)

**Practice Management**
- Appointment scheduling with robust calendar features
- Automated appointment reminders and recalls
- Patient registration and intake
- Electronic consent forms
- Patient ID scanning
- Self-check-in kiosk support
- Case management with referral tracking (inbound and outbound)
- eFax automation
- Time-tracking for program compliance

**Billing & Revenue Cycle**
- Integrated billing with clearinghouse connectivity
- Insurance claim submission and processing
- Automated insurance verification that populates into records
- Financial reporting
- Claims scrubbing (implied by "reduce errors, claim denials, and re-submissions")
- CSV, XLSX, and PDF export formats for billing data

**Telehealth**
- Embedded audio/video virtual visit capabilities
- Integrated into the clinical workflow

**Patient Portal (MyHealth)**
- View medical records, lab results, medications, and care instructions
- HIPAA-compliant secure messaging with providers
- Demographic and insurance information updates
- Questionnaire and consent form completion
- Pre-check-in / eCheck-in
- Self-scheduling (configurable by agency)
- Automated notifications for messages, alerts, and test results
- Browser-based, mobile-optimized (no app download required)

**Reporting & Analytics**
- State, federal, and county report generation
- PQRI/NCQA/NQF reporting
- HRSA Uniform Data System (UDS) reporting
- Customizable analytic dashboards
- Management dashboard app (developed with customer input)
- Patient list generation with configurable filters

**Interoperability**
- Direct Messaging for health information exchange
- CCDA exchange (via portal and transitions of care)
- HIE connectivity (state HIEs, Carequality network)
- HL7 2.5.1 compliance
- FHIR API (SmartOnFHIR)
- Immunization registry connections
- Lab system interfaces
- Clinical terminology databases: ICD-10, CPT, SNOMED, RxNorm, DSM-5

**Enterprise/Statewide Features**
- Statewide master patient index (single ID per person across jurisdictions)
- Multi-location management
- Centralized reporting across departments
- Role-based dashboards

### Data & Content

Based on the features and modules documented above, the product stores and manages the following categories of data:

**Clinical data:** Patient demographics, clinical notes/encounter documentation, problem lists, medication lists, allergy lists, immunization records, lab orders and results, vital signs, clinical assessments (including behavioral health assessments, psychiatric evaluations, treatment plans, progress notes, group therapy notes), care plans, referral records, clinical quality measures data, clinical documents (uploaded and generated), CCDA documents.

**Public health program data:** Communicable disease surveillance records, immunization tracking and registry data, vaccine inventory, community outreach records, contact tracing data, school health records, program eligibility determinations, state-specific program reporting data.

**Administrative/scheduling data:** Appointment schedules, appointment reminders/recalls, patient registration records, consent forms, insurance information, patient check-in data, referral tracking, case management records.

**Billing/financial data:** Insurance claims ($622M+ processed), insurance verification records, billing codes (ICD-10, CPT), financial reports, clearinghouse transactions.

**Patient portal data:** Secure messages between patients and providers, patient-completed questionnaires, self-reported demographic updates, portal notification history.

**Communication data:** eFax records, Direct messages, HIE transactions, lab interface messages.

**Reporting/analytics data:** Clinical quality measure calculations, UDS reports, state/federal/county compliance reports, custom report definitions, dashboard configurations.

The product uses standard clinical terminologies (ICD-10, CPT, SNOMED, RxNorm, DSM-5) and supports CCDA 2.1 and FHIR data formats for interoperability.
