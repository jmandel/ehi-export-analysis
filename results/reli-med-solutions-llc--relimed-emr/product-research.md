# ReLi Med Solutions, LLC — Product Research

Researched: 2026-02-15
Developer website: http://www.relimedsolutions.com

## Overview

ReLi Med Solutions, LLC is a small, privately held health IT company headquartered in Cary, North Carolina. Founded around 2008 by Renu Kasula (CEO) and Lisa Davies (COO), who previously co-founded CareAnyware, a web-based home health and hospice solutions provider. Their CTO, Clint Hopper, also came from CareAnyware and has 20+ years of healthcare IT development experience (including time at Misys and GlaxoSmithKline). The company has approximately 48–50 employees across operations in North America, Asia, and Europe.

ReLi Med Solutions makes a single product — ReLiMed EMR — a cloud-based, integrated EMR and practice management platform targeting small to mid-size ambulatory care practices. The company serves family medicine, internal medicine, pediatrics, urgent care, psychiatry/behavioral health, and FQHCs/CHCs. They also offer a full-service Revenue Cycle Management (RCM) service alongside the software. Growth appears to be driven primarily by client referrals rather than large-scale marketing. The company positions itself as offering responsive, personalized support — a differentiator for small practices that have been burned by larger EHR vendors.

## Product: ReLiMed EMR

CHPL IDs: 11024 (Version 7.3, certified 2022-11-18)

### What It Is

ReLiMed EMR is an integrated, cloud-based electronic medical records and practice management system. The certified module encompasses the full product — there is no separate "certified module" distinct from the broader platform. The system bundles EHR, practice management (scheduling, billing, claims), patient portal, telemedicine, and reporting into a single platform. It can also be deployed on-premise ("cloud-based or in-house deployment options" per the vendor website), though cloud appears to be the primary model.

The certification is broad: 35+ ONC criteria covering clinical documentation (a)(1)–(a)(5), (a)(12), (a)(14); transitions of care (b)(1)–(b)(3); patient portal (e)(1); clinical quality measures (c)(1)–(c)(3); public health reporting (f)(1)–(f)(2); FHIR APIs (g)(7), (g)(9)–(g)(10); and immunization exchange (h)(1). This is a full-featured ambulatory EHR certification.

### Users & Market

**Target users**: Physicians, nurses, clinical staff, billing staff, and practice managers at small to mid-size ambulatory practices. The system supports solo providers up to multi-specialty groups of around 50 physicians.

**Clinical settings**: Family practice, internal medicine, pediatrics, urgent care, psychiatry/behavioral health, and FQHCs/CHCs. The vendor specifically markets to FQHCs with specialized features (UDS reporting, sliding fee schedules).

**Customer scale**: Not publicly disclosed. The company is small (~50 employees) and appears to serve a modest customer base of small-to-mid-size practices. No specific customer counts or notable large deployments were found in public materials.

**Geography**: Primarily US-based practices. The vendor is headquartered in North Carolina.

### Modules & Functionality

Based on vendor website, feature pages, and third-party review sites:

**Clinical Documentation / Charting**
- Fully customizable charting templates by provider, described as createable "in seconds"
- Multi-specialty charting including Women's Health, Pediatric Health, and Behavioral Health templates (per FQHC page)
- Clinical data stored in "a granular, quantifiable way allowing for easier, more concise reporting" (vendor website)
- Clinical workflow tools with real-time patient care alerts and triggers based on patient health history
- Health guidelines and clinical decision support

**E-Prescribing**
- Electronic prescription management (certified under (a)(1) CPOE for medications)

**Lab Integration**
- Electronic lab interface (e-Lab) for ordering and receiving lab results
- Integration with Quest Diagnostics specifically mentioned

**Scheduling & Front Desk**
- Appointment scheduling by provider and/or customizable resource
- Front desk display with alerts and patient balance visibility
- Insurance verification accessible from multiple screens
- Patient self-scheduling through the portal
- Self check-in via kiosk with insurance card upload
- Automated appointment reminders

**Billing & Claims (Practice Management)**
- Integrated billing — as clinical activities are documented, superbills are auto-populated
- Automated charge entry as tests, procedures, screenings, and immunizations are charted
- Multi-level claim scrubbing with real-time alerts
- Claim reminders for communication between billing and clinical staff
- Automated posting with customizable biller automation
- In-depth billing reports for AR management and revenue tracking
- Split billing using "clone claim" feature (per FQHC page)

**Revenue Cycle Management (Service)**
- Full-service RCM offered alongside the software (not just a software module)
- Includes insurance verification, denial management, patient statements, reporting
- "Multi-tier approach to billing" combining specialized teams and technology edits

**Patient Portal / Patient Engagement**
- Patients can view health history, lab results, request appointments
- HIPAA-compliant secure messaging between patients and providers
- Patient self-registration (online forms completed before appointments)
- Online payment processing (QR code on statements to access payment portal)
- Access from multiple device types

**Telemedicine**
- Secure video visits from any mobile device or computer
- Pre-scheduled and on-demand visit requests through patient portal
- Patient demographics and medical history entered online flow into EMR in real-time
- Providers document notes during telehealth appointments
- Post-visit chart notes accessible to patients

**Reporting & Analytics**
- Reporting module for tracking referrals, patient census, population health, personnel productivity, and revenue cycle
- UDS reporting built into the system (critical for FQHCs)
- Quality of care reporting / clinical quality measures
- Customizable reporting

**FQHC/CHC-Specific Features**
- UDS (Uniform Data System) reporting built-in, updated annually
- Sliding fee schedule with automated charges based on poverty level
- Sliding fee calculator per patient based on income level
- Specialized FQHC coding rules
- Population health management tools
- Multi-specialty charting (Women's Health, Pediatrics, Behavioral Health)

**Interoperability & Data Exchange**
- Interfaces with HIE (Health Information Exchanges)
- Immunization registry reporting
- ACO data exchange
- Secure Direct email for provider-to-provider communication
- Referral tracking
- FHIR API access (certified (g)(7), (g)(9), (g)(10))
- HL7 standards compliance

**Security & Compliance**
- HIPAA compliant with bank-level encryption
- Automated access controls and activity logging
- ICD-10 compliant

**Document Management**
- Document management capabilities (per ehrinpractice.com feature list)

**Inventory Management**
- Basic inventory capabilities (per findemr.com feature list)

**Notable absence**: Automated faxing was noted as lacking by at least one review source (findemr.com).

### Data & Content

Based on the features described above, the system manages and stores:

- **Clinical encounter data**: Chart notes, customizable templates, visit documentation for multiple specialties
- **Medication data**: E-prescriptions, medication orders (CPOE certified)
- **Lab data**: Lab orders, lab results (electronic lab interface with Quest and others)
- **Patient demographics**: Registration data, insurance information, income/poverty level (for FQHC sliding fee)
- **Scheduling data**: Appointments, provider schedules, resource allocation
- **Billing/financial data**: Superbills, charges, claims, payments, posting records, denial data, patient statements, AR data, sliding fee schedules
- **Patient portal data**: Secure messages, appointment requests, self-registration forms, online payments
- **Telemedicine data**: Video visit records, encounter notes from telehealth visits
- **Immunization data**: Immunization records (registry reporting certified)
- **Allergy data**: Allergy tracking (per findemr.com)
- **Health history**: Patient health history viewable through portal
- **Referral data**: Referral tracking and oversight
- **Clinical alerts/triggers**: Care alerts based on patient history
- **Documents**: Uploaded/managed documents
- **Reporting data**: UDS reports, quality measures, population health metrics, productivity reports
- **Audit/access logs**: Activity logging for compliance

The vendor's certification disclosure page notes additional costs for patient portal hosting, immunization registry interfaces, FHIR connectivity, and Direct email for care transition summaries — confirming these are real, active data exchange channels in the product.

The website doesn't specifically mention imaging/radiology integration, inventory details beyond "basic," or dental modules (even for FQHCs). Behavioral health charting is mentioned in the FQHC context but details are sparse.

---
