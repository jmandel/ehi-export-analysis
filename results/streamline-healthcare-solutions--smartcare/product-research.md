# Streamline Healthcare Solutions — Product Research

Researched: 2026-02-14
Developer website: https://streamlinehealthcare.com/

## Overview

Streamline Healthcare Solutions is a mid-size EHR vendor founded in 2003 and headquartered in Oak Brook, Illinois, focused exclusively on **behavioral health and human services**. The company employs approximately 400–450 people and reports annual revenue in the range of $56–67 million (per third-party estimates from RocketReach and Latka). They are privately held and appear to have grown organically within the behavioral health niche rather than through acquisitions.

Streamline's sole product is **SmartCare**, a cloud-based (Microsoft Azure) EHR platform purpose-built for behavioral health, substance use disorder, foster care/adoption, intellectual and developmental disabilities (IDD), and managed behavioral health organizations. The company positions SmartCare as an enterprise, single-platform solution — meaning all modules (clinical, billing, reporting, etc.) run on one unified architecture rather than being bolted-on integrations. They are a member of the National Council for Mental Wellbeing's vendor ecosystem and compete with vendors like Qualifacts (CareLogic/Credible), Netsmart (myAvatar), and Core Solutions.

## Product: SmartCare

CHPL IDs: 10987

### What It Is

SmartCare is a comprehensive, web-based EHR designed specifically for behavioral health and human services organizations. It is certified as an ONC Health IT Module (version R6, certified September 2022) with 40+ certification criteria spanning clinical data (a)(1)–(a)(15), care coordination (b)(1)–(b)(3), clinical quality measures (c)(1)–(c)(3), patient portal (e)(1)/(e)(3), public health reporting (f)(1)–(f)(5), FHIR API access (g)(7)–(g)(10), and Direct messaging (h)(1). The SED intended users are described as "Ambulatory and Inpatient."

The certified module and the product are essentially the same thing — SmartCare is the entire platform, not a component of a larger suite. The MCO (Managed Care Organization) module appears to be an add-on or variant of the same SmartCare platform rather than a separate product.

SmartCare runs entirely in a web browser (Chrome or Edge) with no plugins required. Each customer gets a single-tenant instance on Azure. It follows a subscription/SaaS pricing model, though the vendor describes it as having "more local control than a standard SaaS offering."

### Users & Market

**Target organizations:**
- Community mental health centers (CMHCs)
- Certified Community Behavioral Health Clinics (CCBHCs)
- Substance use disorder (SUD) treatment providers
- Foster care and adoption agencies
- Intellectual/developmental disabilities (IDD) service providers
- Managed behavioral health organizations (MCOs)
- Organizations providing inpatient/residential behavioral health services

**End users:** Clinicians (psychiatrists, psychologists, therapists, counselors, social workers), nurses, case managers, administrative/billing staff, and supervisors. The patient portal extends access to patients/clients.

**Customer scale:** The vendor website features testimonials from Valley Oaks Health, George Junior Republic, and The Nord Center. Exact customer counts are not publicly disclosed, but the company's ~$60M revenue and ~400 employees suggest a moderate-sized customer base of behavioral health agencies. Third-party sources describe Streamline as a "Leader" among behavioral health EHR vendors alongside Qualifacts, Netsmart, and others.

**Geography:** Primarily U.S.-based behavioral health and human services organizations.

### Modules & Functionality

SmartCare is marketed as a single integrated platform with the following distinct modules and capabilities, based on vendor website descriptions:

**Clinical Care Management:**
- Clinical documentation with progress notes and assessments
- Treatment planning with auto-population features
- Clinical decision support tools
- Care plans and outcome tracking
- "Golden thread" documentation (linking presenting problems → diagnoses → treatment goals → interventions → progress notes — a behavioral health compliance requirement)
- Client tracking module that monitors due dates for documents and events, with automated flags and alerts when items are due or overdue
- Support for tracking by assigned staff, workgroup, or professional role

**Inpatient & Residential:**
- Medication administration records
- Bed management
- Inpatient documentation within the same platform as outpatient

**Intensive Outpatient Program (IOP) & Day Services:**
- Service delivery for IOP and day services settings

**Primary Care Integration:**
- Scheduling
- Referral tracking
- Flow sheets
- Order entry and management
- Progress notes
- Problem tracking
- Health maintenance templates
- Physician dashboard (orders, appointments, lab orders, batch signatures, alerts, messages)
- Uses standardized coding: SNOMED CT, LOINC, RxNorm, ICD-10-CM
- Permissions-based sharing of data between physical and behavioral health records

**ePrescribing (SmartCare Rx):**
- Electronic prescribing integrated with Surescripts pharmacy network
- Access to order history and allergy information
- Prescription transmission to pharmacies

**Revenue Cycle Management:**
- Claims processing and billing
- Claim scrubbing and denial management
- Reimbursement acceleration
- Described as "intelligent, data-driven revenue management functionality"

**MCO Module (SmartCare MCO):**
- Provider contract and rate management
- Credentialing and site reviews
- Provider search for member referrals
- Electronic claims reception (837 format) and adjudication
- Payment processing and check distribution
- Remittance advice (835) generation
- Authorization tracking
- Hospitalization pre-screens, concurrent reviews, discharge management
- Utilization management reviews (URAC standards)
- Capitated arrangement management with contract cap threshold alerts
- Population-level management with recommended service packages based on acuity

**Patient Portal:**
- Patient/client engagement and service access
- Secure communication

**Telehealth:**
- Remote service delivery capabilities

**SmartCare Anywhere (Mobile):**
- Mobile access to EHR
- Online and offline functionality

**Business Intelligence:**
- Data warehouse
- Native reporting tools
- Integration with leading BI software
- Performance monitoring dashboards for supervisors
- User-specific dashboards for daily tasks

**Additional capabilities mentioned:**
- Electronic signature capture (signature pad, including client signing)
- 20 Clinical Quality Measures (CQMs) for reporting
- State-specific reporting customization (at additional cost per mandatory disclosures)
- AI-powered documentation integration via Eleos Health for automated progress note creation (recent addition per SoftwareFinder)

### Data & Content

Based on the features and modules described above, SmartCare stores and manages:

**Clinical data:** Progress notes, treatment plans, assessments, care plans, clinical documentation, diagnoses (ICD-10-CM), problem lists, medication lists, allergies, immunization records, vital signs/flow sheets, lab orders and results, and outcome measurements. The "golden thread" emphasis means these clinical records are linked from presenting problems through to treatment outcomes.

**Medication data:** Prescription records via Surescripts integration (ePrescribing), medication administration records (for inpatient), allergy information, and order history.

**Administrative/demographic data:** Client registration, program enrollment, discharge records, scheduling data, referral tracking, staff assignments, and provider credentialing.

**Billing/financial data:** Claims (837 format), remittance advice (835), billing status, reimbursement records, denial tracking, capitation data, and contract/rate information (especially for the MCO module).

**Compliance/tracking data:** Document due dates, event tracking flags, recurring compliance deadlines, protocol-based tracking tied to client status transitions (registration, waitlist, enrollment, discharge).

**Care coordination data:** Transitions of care documentation (certified for (b)(1)–(b)(3)), Direct messaging (certified for (h)(1)), and referral data.

**Public health data:** Syndromic surveillance, immunization registry, and other public health reporting data (certified for (f)(1)–(f)(3), (f)(5)).

**Patient portal data:** Patient-generated messages and portal access records.

**Reporting/analytics data:** Clinical quality measures, business intelligence data warehouse contents, performance dashboards.

**What's unclear:** The vendor website is relatively high-level in describing features and doesn't provide detailed data dictionaries or schema documentation. The extent of custom forms and assessments (which are very common in behavioral health EHRs, where agencies often have dozens of custom intake forms, screening tools like PHQ-9, AUDIT, etc.) is not well-documented on the marketing site, though the references to "customizable" templates and auto-population of assessments suggest significant form/assessment capabilities. The specifics of what data the mobile module (SmartCare Anywhere) can access offline is also unclear.

---
