# ModuleMD — Product Research

Researched: 2026-02-14
Developer website: http://www.modulemd.com

## Overview

ModuleMD is a specialty-focused EHR and practice management vendor based in Grand Blanc, Michigan, founded in 1999 by two practicing physicians with combined 50+ years of clinical experience. The company's flagship niche is **allergy & immunology**, and they are one of the few EHR vendors specifically designed for allergists. They also serve pulmonology, ENT allergy/otolaryngology, internal medicine, and infusion center practices. ModuleMD was the first EMR to upload data to the AAAAI (American Academy of Allergy, Asthma & Immunology) Registry (2014) and the first with OpenAPI certification (2016).

In 2021, ModuleMD was acquired by Silverstone Capital Holdings, a private equity firm focused on healthcare technology. The company serves 300+ practice locations and manages 10 million+ medical records. They hold four consecutive G2 High Performer awards in the EHR category (94%+ of reviews at 4-5 stars). Target customers are ambulatory specialty practices — small to medium in size, independent practices, with a strong concentration in allergy/immunology. The product is cloud-based (SaaS).

## Product: ModuleMD WISE™

CHPL IDs: 11092

### What It Is

ModuleMD WISE is an integrated, cloud-based EHR + Practice Management + Revenue Cycle Management platform designed specifically for specialty ambulatory practices. The certified module (WISE 10.0, certified 2022-12-19) covers a broad range of ONC criteria: clinical documentation (a)(1)-(a)(5), (a)(12), (a)(14); transitions of care (b)(1)-(b)(3); patient portal (e)(1); public health reporting (f)(1)-(f)(3); FHIR API (g)(7)-(g)(10); and direct messaging (h)(1). This is not a narrow module — it's a comprehensive ambulatory EHR platform with 38 certified criteria.

The product is the whole platform — EHR, practice management, and patient engagement are all part of one integrated suite called WISE. Additional add-on tools (SPOCK, InDrA, Hubble Health, JOSH AI, SkinSight AI) extend it but operate within the same platform.

### Users & Market

**Primary users**: Allergists/immunologists, pulmonologists, ENT physicians, internists, and infusion center staff. The vendor states the majority of their clients are allergy practices. Day-to-day users include physicians, nurses/clinical staff (administering immunotherapy injections, documenting skin tests), billing/RCM staff, and front-office staff (scheduling, check-in).

**Settings**: Ambulatory specialty practices, ranging from solo practitioners to multi-provider groups. The Richmond Allergy & Asthma Specialists case study describes a practice that doubled revenue within 8 months of implementing ModuleMD, suggesting mid-size multi-provider practices are a common customer profile.

**Scale**: 300+ practice locations, 10M+ medical records. This is a small-to-mid-size vendor with a focused specialty niche, not a broad-market EHR.

**Partners**: CommonWell Health Alliance member. Certified partners include phiMail (Direct messaging), Updox, DrFirst Rcopia4 (e-prescribing), and Carefluence (interoperability).

### Modules & Functionality

The WISE platform includes the following modules and capabilities, per vendor materials:

**Core EHR / Clinical Documentation**
- Flexible clinical documentation with specialty-specific templates (allergy, pulmonology, ENT, internal medicine)
- Patient dashboard with customizable medical summary views
- Practice dashboard for management oversight
- JOSH AI: real-time dictation assistant supporting 75+ languages, with ability to pause/resume across multiple patients
- AI-powered ICD/CPT coding automation

**Allergy & Immunology (flagship specialty)**
- Skin test orders and results (intradermal and skin prick testing)
- Custom allergens and skin test panels
- SkinSight AI: image-based skin test analysis that auto-detects positive reactions and measures wheal/flare
- Extract orders and vial mixing (compounding)
- Vial and shipping labels
- Injection administration with questionnaires
- Contactless injection check-in
- Immunotherapy management: automated dosage calculations, treatment schedules, progress tracking
- Modified Quantitative Testing (MQT) algorithm support for immunotherapy formulation
- USP 797 compliance: lot numbers, lot-specific allergens, Beyond Use Dates (BUDs), vial expiration tracking, operator logs, audit trails
- AAAAI QCDR integration for quality reporting
- Patient allergy educational materials

**Pulmonology / Respiratory**
- Spirometry integration and trending
- Asthma Control Test (ACT) scoring and trending
- Vital signs trending
- Sleep study questionnaires
- DICOM/PACS integration for chest imaging
- Biologic/medication administration charting
- Remote patient monitoring integration

**ENT Allergy / Otolaryngology**
- Templates and workflows for multi-specialty ENT + allergy + audiology
- Allergy testing within ENT context
- ENT-specific procedure documentation

**Infusion Center Management**
- Automated scheduling and real-time updates
- Seamless check-in
- Infusion records accessible through patient portal
- Integrated billing and insurance verification for infusion services
- Regulatory/compliance tracking for infusion therapy guidelines

**e-Prescribing**
- Electronic prescribing via DrFirst Rcopia4 integration
- Drug interaction checks and formulary information
- Monthly per-provider subscription (disclosed on ONC page)

**Lab Integration**
- Bidirectional interfaces with Quest Diagnostics and LabCorp
- Electronic order sending and result receipt within the EMR

**Practice Management**
- Patient scheduling with waitlist management
- Batch eligibility verification
- Automated appointment reminders (call/text/email)
- Electronic check-in (including contactless parking lot check-in)
- Demographics and referral data management
- Insurance coverage tracking
- Account balance tracking
- Custom forms and digital signatures
- Real-time dashboards and administrative reports
- Timesheet management for payroll
- Secure internal messaging between staff

**Revenue Cycle Management (RCM)**
- Claims management and submission
- Advanced auto-charging from clinical data
- Real-time financial reports
- Patient payment processing
- Claim scrubbing (case study reports 98% clean claim rate)
- Comprehensive billing service option available

**Patient Portal (Hale Hub)**
- Appointment scheduling
- Prescription refill requests
- Statement and payment review
- Lab results access
- Secure messaging with providers
- Demographic information updates
- Mobile app (iOS/Android) for payments, demographics, medication history
- Contactless check-in via mobile

**Additional Tools**
- **SPOCK**: "Smart Patient Outreach & Communication Kit" — front-office automation for scheduling, reminders, communications, task management
- **InDrA**: Inventory management with real-time stock levels, expiration alerts, immunotherapy/medication dispensing tracking, vendor/order management, smart forecasting
- **Hubble Health**: Clinician mobile app
- **Telemedicine**: Integrated with single sign-on and seamless visit documentation

**Interoperability & Data Exchange**
- Direct messaging for transitions of care (via phiMail/Updox)
- FHIR API access (g)(7)-(g)(10) certified
- CommonWell Health Alliance membership
- Patient chart sharing with external organizations
- Clinical Quality Measures (CQM) reporting — 15 CMS measures listed on ONC page

### Data & Content

Based on documented features and workflows, ModuleMD WISE stores and manages:

- **Clinical records**: Patient demographics, medical history, problem lists, medication lists, allergy lists, vital signs, clinical notes/documentation
- **Allergy-specific data**: Skin test results (wheal/flare measurements per allergen), allergen panels, extract/vial compounding records (lot numbers, allergen compositions, BUDs, expiration dates), immunotherapy treatment plans and dosage schedules, injection administration records with questionnaires, USP 797 compliance audit trails and operator logs, SkinSight AI image analysis results
- **Pulmonary data**: Spirometry results and trends, ACT scores over time, sleep study questionnaire data, PFT results, DICOM imaging references
- **Prescriptions**: e-Prescribing records, drug interaction check results, formulary data, prescription refill requests
- **Lab data**: Lab orders, lab results (bidirectional with Quest/LabCorp)
- **Scheduling & administrative**: Appointments, waitlists, check-in records, referral data, insurance eligibility and coverage information, custom forms, digital signatures, timesheets
- **Billing & financial**: Claims data, charge records (including auto-generated charges), payment records, account balances, patient statements, financial reports
- **Infusion data**: Infusion scheduling, infusion session records, insurance pre-authorization data (implied by insurance verification for infusion), biologic/medication administration records
- **Inventory data** (via InDrA): Stock levels, medication/supply inventory, vendor information, purchase orders, expiration tracking, dispensing records
- **Patient portal data**: Patient messages, appointment requests, prescription refill requests, demographic updates, patient-facing health records
- **Communication data**: Secure internal messages, patient-provider messages, transition-of-care documents (CCDAs via Direct messaging)
- **Quality/compliance**: Clinical quality measure data for 15+ CMS measures, AAAAI QCDR data
- **AI-generated content**: JOSH dictation transcripts, AI-suggested ICD/CPT codes, SkinSight skin test analysis results
- **Audit/operational**: User activity logs, compliance audit trails, operational reports

**Gaps/uncertainties**: The vendor website does not describe problem-specific behavioral health, dental, or inpatient workflows — this is an ambulatory specialty system. It is unclear how much structured data vs. free-text narrative makes up the clinical documentation (the JOSH AI dictation feature suggests significant narrative content). The boundary between what's stored in WISE vs. in partner systems (DrFirst for e-prescribing, phiMail/Updox for Direct messaging) is not entirely clear from public materials — the prescription data likely flows through DrFirst but is also visible in the WISE chart.
