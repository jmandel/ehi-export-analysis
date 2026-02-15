# VisionWeb — Product Research

Researched: 2026-02-14
Developer website: http://www.startyouruprise.com/ (redirects to helixsolution.com)

## Overview

VisionWeb is an Austin, Texas-based technology company focused exclusively on the eye care / optometry market. It is owned by **EssilorLuxottica**, the global eyewear and lens conglomerate. In October 2023, EssilorLuxottica launched **HELIX**, a new division consolidating its U.S. digital solutions for independent eye care practitioners (ECPs). HELIX brought together VisionWeb (online ordering platform), CLX (contact lens ordering), 4PatientCare (patient engagement), and Revenue Cycle Management into one portfolio. VisionWeb's EHR/PM product, Uprise, is now part of this HELIX ecosystem, and a next-generation replacement product called **Vision(X) PMS & EHR** was announced for Q2 2024 availability, though Uprise continues to operate with full support.

VisionWeb's ordering platform claims to serve over 20,000 eye care practices, connecting to 475+ optical labs and 25+ practice management system integrations. The company's core competency historically was online ordering for spectacle lenses, contact lenses, and frames — Uprise extended them into the EHR/PM space. The target market is independent optometry practices, from single-location to multi-location and enterprise optical businesses.

## Product: Uprise

CHPL IDs: 11069

### What It Is

Uprise is a **cloud-based, all-in-one practice management and electronic health records system** built specifically for optometry/eye care practices. The CHPL metadata describes it as "Ambulatory (Optometry)." It was introduced by VisionWeb at an optometry industry conference and is described as being "built by ODs" (optometrists). The product is the full certified system — the certified module (Uprise 3.1) encompasses both the EHR and practice management capabilities.

Uprise is certified for a broad range of ONC criteria including clinical data (a)(1)-(a)(5), (a)(12), (a)(14), transitions of care (b)(1)-(b)(3), patient portal/VDT (e)(1), clinical quality measures (c)(1)-(c)(3), FHIR API (g)(7), (g)(9), (g)(10), and direct messaging (h)(1). The mandatory disclosures page also notes 11 CMS clinical quality measures are certified. E-prescribing is integrated via NewCrop/Surescripts.

The product comes in two tiers:
- **Uprise Essentials**: PM + EHR + ePrescribing + secure messaging
- **Uprise Pro**: All of Essentials plus frame catalogs, patient recall (via 4PatientCare), patient education, and CodeSAFE code verification tools

Pricing starts around $104/month per the emrsystems.net listing, with no long-term contracts and no hidden fees.

### Users & Market

Uprise targets **independent optometry and ophthalmology practices** — from solo ODs to multi-location groups and enterprise optical businesses. Day-to-day users include:
- **Optometrists (ODs)** — clinical charting, exam documentation, e-prescribing, diagnosis
- **Opticians** — optical dispensing, frame ordering, lens ordering, inventory management
- **Front office staff** — scheduling, patient intake, insurance verification, check-in/checkout
- **Billing staff** — claims management, insurance processing (or this is outsourced to VisionWeb's RCM service)
- **Patients** — via the patient portal for intake forms, appointment scheduling, and communication

The product is cloud-based and accessible from desktop or tablet. Reviews mention a mobile app exists but is limited compared to the desktop experience.

### Modules & Functionality

Based on vendor materials, blog posts, and third-party reviews, Uprise includes the following modules and capabilities:

**Clinical / EHR:**
- **SmartTouch EHR**: Touch-optimized clinical charting for ODs — exam documentation with customizable image templates and annotation tools
- **Clinical Decision Support**: Annotations on image templates auto-populate treatment code mappings, ICD-10 codes, diagnoses, treatment plans, special testing options, and patient education materials based on severity
- **Prescription history**: Full list of past and present prescription history (both Rx and optical)
- **Pre-testing integration**: Results from ophthalmic diagnostic equipment feed directly into patient records
- **Contact lens fitting**: When an OD performs a contact refraction, diameter and base curve pre-populate based on the specific product
- **ePrescribing**: Via NewCrop/Surescripts to 60,000+ pharmacies, with drug interaction checking and real-time flags for dangerous interactions
- **CPOE**: Treatment code mapping auto-populates ICD-10 codes and treatment plans
- **Patient education materials**: Counseling materials and recommendation topics linked to clinical findings

**Practice Management:**
- **Scheduling**: Web-based scheduler with appointment management, walk-in patient tracking, and resource utilization
- **Patient demographics**: Full patient profile management
- **Patient intake**: Patient portal replaces paper intake forms with digital questionnaires including lifestyle questions
- **Patient checkout**: Integrated checkout workflow
- **Patient recall**: Automated recall based on customizable settings tied to last visit dates (via embedded 4PatientCare integration in Pro tier), using Intelligent Escalation technology across text and email
- **Appointment reminders**: Automated email and text reminders to reduce no-shows
- **Referral management**: Referral doctor communications

**Optical Dispensing & Ordering:**
- **Optical Dashboard**: Real-time view of jobs in process, jobs waiting for pickup, order status
- **Frame catalog integration**: Via Frames Data database with daily automatic updates; custom catalogs also supported
- **Inventory management**: Real-time quantity on hand, updated as products are received and sold
- **Lab ordering**: Direct electronic order submission to labs — "sending an order to the lab is a matter of pressing a button"
- **VisionWeb ordering integration**: Connection to 400+ spectacle lens, contact lens, stock lens, and frame suppliers via VisionWeb's ordering platform
- **Drop shipping**: Frames can be ordered and sent directly to finishing labs for "frame to come" jobs
- **Order tracking**: Full order lifecycle tracking from submission through lab processing to patient pickup
- **Prior Rx import**: Import and duplicate prior prescriptions or frame/lens combinations

**Billing & Claims:**
- **Claims management**: Electronic claim submission, tracking, and generation for review
- **CodeSAFE alerts**: Flags incompatible CPT code combinations to prevent claim denials (Pro tier)
- **Billing code verification**: Built-in code verification tools
- **Insurance processing**: Vision and medical insurance claims
- **Revenue Cycle Management (RCM)**: Available as a separate managed service where VisionWeb's billing specialists handle claims filing, rejection correction, denial appeals, and performance reporting — described as "an extension of your billing team." Claims are "scrubbed" for accuracy and medical necessity before submission. This appears to be an add-on service rather than built into Uprise itself.

**Patient Portal:**
- Secure, HIPAA-compliant portal
- Digital intake forms (replace paper)
- Lifestyle questionnaires
- Exam history access
- Patient-practice messaging
- Online scheduling

**Telehealth:**
- Telehealth capabilities are mentioned (Uprise Telehealth Essentials), enabling remote eye care workflows

**Integrations:**
- 400+ labs and suppliers via VisionWeb ordering platform
- Pharmacies via Surescripts/NewCrop for e-prescribing
- Diagnostic ophthalmic equipment (direct data import)
- 4PatientCare for patient engagement (embedded)
- Frames Data database
- Direct messaging for care coordination (certified for (h)(1))

**Reporting:**
- Operational reports
- Financial reports
- Auditing reports
- Analytical reports
- Clinical quality measure reporting (CQMs)
- Claims performance reporting (via RCM service)

### Data & Content

Based on the features described above, Uprise stores and manages the following categories of data:

- **Patient demographics**: Names, contact info, insurance details, patient profiles
- **Clinical exam data**: Eye exam findings, annotations on image templates, diagnoses, visual acuity measurements, refractions, contact lens fits, pre-test results from diagnostic equipment
- **Prescriptions**: Optical Rx history (spectacle and contact lens prescriptions), medication prescriptions (via e-prescribing)
- **Medications**: Current and past medication lists with drug interaction data
- **Treatment plans**: ICD-10 codes, treatment code mappings, special testing orders
- **Patient education**: Counseling materials and recommendations linked to clinical findings
- **Orders**: Spectacle lens orders, contact lens orders, frame orders, lab orders — with full lifecycle tracking
- **Optical inventory**: Frame and lens stock levels, product catalogs
- **Scheduling data**: Appointments, recalls, reminders, walk-in tracking
- **Billing/claims**: CPT codes, insurance claims, claim status, denials, resubmissions, payments
- **Patient portal data**: Intake forms, lifestyle questionnaires, patient messages, online scheduling requests
- **Documents & images**: Exam images, annotations, referral communications
- **Audit trails**: Change tracking showing who modified records and when
- **Clinical quality measures**: CQM reporting data for 11 certified CMS measures
- **Secure messages**: Internal messaging and patient-practice communications

**Gaps and uncertainties:**
- The boundary between what billing data lives in Uprise itself vs. the separate RCM managed service is unclear. Uprise has built-in claims management, but more complex billing operations may be handled by the external RCM team accessing the system remotely.
- The website doesn't clearly describe document management or image storage capabilities beyond exam annotations and pre-test device imports.
- Whether Uprise stores comprehensive allergy data beyond drug interaction flags is not explicitly described, though (a)(1) certification (CPOE) typically requires allergy/adverse reaction recording.
- The telehealth module's data storage (video visit records, telehealth-specific notes) is not well documented.
- Lab results beyond in-office pre-testing (e.g., external lab results) are not explicitly described.

---

## Business & Ecosystem Context

VisionWeb's core business was historically the **online ordering platform** connecting eye care practices with optical labs and suppliers. Uprise extended this into EHR/PM, creating a vertically integrated solution where clinical documentation flows directly into optical ordering. This tight integration between clinical records and optical supply chain is a distinctive feature — most EHR vendors don't have a built-in connection to 400+ optical suppliers.

The HELIX reorganization under EssilorLuxottica signals that Uprise is transitioning to a new platform (Vision(X)), but as of the certification (2022) and available documentation, Uprise 3.1 remains the active certified product. The mandatory disclosures page states "there are no technical or contractual considerations to use our certified product (Uprise 3.1)" and "no additional one-time or ongoing costs."

VisionWeb/Uprise competes in the optometry-specific EHR market against products like LiquidEHR, MedFlow EHR, RevolutionEHR, Crystal PM, and others. Reviews (overall ~4/5 stars from limited review counts) praise the integrated workflow and optical dispensing features, but note system stability issues, a steep learning curve, and underwhelming mobile experience.
