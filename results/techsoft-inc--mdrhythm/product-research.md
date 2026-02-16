# TechSoft, Inc. — Product Research

Researched: 2026-02-16
Developer website: http://www.mdrhythm.com

## Overview

TechSoft, Inc. (also referred to as TechSoft Corporation) is a small, privately held company based in Marlton, New Jersey. The company has been in business since at least the late 1980s/early 1990s and describes itself as "well established in the professional Medical community with Practice Management and Billing solutions, along with Electronic Health Records." The principal contact, Parag Dadhania, is also linked to "Applied Healthcare Solutions, LLC" in Marlton, NJ — likely a related entity. The company also uses the domain medstech.com (titled "Welcome to Techsoft Inc. Medical Systems"), which appears to be an alternate or legacy corporate domain.

TechSoft is a micro-vendor in the EHR market. There are no reviews on G2, Capterra, KLAS, or Software Advice. The most recent press release found is from 2013. The company's website (mdrhythm.com) was unresponsive during research (server at 50.226.239.91 timing out), though cached search snippets and partner pages provided substantial product detail. The patient portal (web.mdronline.net) appears to still be operational.

## Product: MDRhythm

CHPL ID: 9797 (MDRhythm Version 8, certified 2018-12-08)

### What It Is

MDRhythm is a fully integrated EMR/EHR and Practice Management solution that has been in use since 1992. It is described as a "hybrid EHR" — the practice management/billing system came first, and the EMR component was added around 1999. It was designed by practicing healthcare providers, which TechSoft emphasizes as a differentiator. The product is positioned as an all-in-one system that "eliminates the need for disparate systems."

The certified product covers a broad set of ONC criteria including clinical data (a)(1)-(a)(15), transitions of care (b)(1)-(b)(3), patient portal (e)(1), public health reporting (f)(1)-(f)(7), FHIR APIs (g)(7)-(g)(10), and Direct messaging (h)(1). This breadth indicates a comprehensive ambulatory EHR, not a specialty or single-function module.

### Users & Market

**Target users:** Outpatient clinics (per CHPL SED intended users). The product is general-purpose ambulatory — no specialty-specific marketing was found.

**Notable market focus:** In 2013, TechSoft partnered with the National Association of Free & Charitable Clinics (NAFC, representing 1,200+ clinics nationwide) to provide MDRhythm as "a complete and affordable Electronic Health Record and Practice management solution designed specifically for Free and Charitable clinics." The outcome of this partnership (actual adoption numbers) is unknown.

**Market size:** Very small. No third-party reviews exist. No public data on customer count or installed base. The vendor website is currently unresponsive. HG Insights lists MDRhythm but detailed data is paywalled. All indicators point to a micro-vendor with a small number of installations, likely concentrated in the New Jersey/Philadelphia region.

**Clinical settings:** Small to mid-size ambulatory practices, free/charitable clinics. No evidence of hospital, inpatient, or large enterprise deployments.

### Modules & Functionality

Based on press releases, search result snippets of the vendor website, partner pages, and FHIR API documentation, MDRhythm includes:

**Practice Management & Billing:**
- Patient scheduling
- Medical billing and claims processing
- Demographic and insurance information management
- State and federal agency reporting
- Combined PAP (Prior Authorization Processing) with autofill
- (The PM system is the original core of the product, predating the EMR component)

**Electronic Medical Records (EMR/EHR):**
- Patient charting and documentation
- Past/present illness documentation
- Examination documentation
- Conditions/problem list management
- Allergies tracking
- Medication management
- Immunizations
- Lab results and diagnostic reports
- Vital signs
- Goals and care plans

**E-Prescribing:**
- Electronic prescriptions including controlled substances (EPCS)
- EPCS via IdenTrust partnership for identity proofing and two-factor authentication
- Supports USB token, mobile authentication, or identity proofing only configurations

**Pharmacy & Inventory:**
- Full pharmacy and inventory control (suggesting support for dispensing clinics or in-house pharmacies)

**Document Management:**
- Faxing (sending/receiving)
- Document scanning
- Transcription management — manage in-house, remote, and outsourced transcription; review partial dictation jobs forwarded by physicians from the EHR

**Patient Portal ("MDR Online" at web.mdronline.net):**
- View lab results, medication list, allergies, appointment schedule, immunizations, diagnosis list
- Patient education materials
- Request appointments
- Request prescription refills
- Maintain personal health profile
- Account delegation for authorized representatives
- HIPAA-compliant encrypted storage
- Activities tracked through computer audit; user entries may become part of medical record

**Interoperability:**
- Lab connectivity (external labs and diagnostic centers)
- State and regional facility connectivity
- Secure email / Direct messaging
- Transitions of care (C-CDA documents)
- Public health reporting (immunization registries, syndromic surveillance, cancer registries, case reporting)

**FHIR API (documented December 5, 2022):**
- SMART App Launch 2.0.0, OAuth2 authentication
- Supported FHIR R4 resources: Patient, AllergyIntolerance, CarePlan, CareTeam, Condition, Device, DiagnosticReport, DocumentReference, Encounter, Goal, Immunization, Location, Medication, MedicationRequest, Observation, Organization, Practitioner, PractitionerRole, Procedure, Provenance

**Third-Party Integrations:**
- IdenTrust for EPCS identity proofing and authentication
- 1-800 Notify for automated appointment reminders (call/text integration via PDF export of schedule)

### Data & Content

Based on the features, certifications, FHIR API, and patient portal capabilities, MDRhythm manages the following data:

**Clinical data:** Problems/conditions, allergies, medications (including controlled substances), immunizations, vital signs, lab results, diagnostic reports, procedures, goals, care plans, care teams, clinical impressions/notes.

**Patient demographics:** Name, DOB, address, contact info, insurance information, guarantor information.

**Encounter data:** Visit records, encounter types, provider assignments, care team.

**Prescriptions:** Medication orders including EPCS for controlled substances, prescription history.

**Pharmacy/inventory data:** Drug inventory, dispensing records (for in-house pharmacy use cases).

**Billing & financial data:** Claims, charges, insurance/coverage information, prior authorizations. The practice management/billing system is the original core of the product and predates the EMR component.

**Scheduling data:** Appointments, provider schedules (exported as PDF for 1-800 Notify integration).

**Documents & media:** Scanned documents, faxes, transcribed notes, clinical documents (C-CDAs), dictation/transcription jobs.

**Device data:** Implantable device information / UDI (certified for (a)(14)).

**Patient portal data:** Patient-initiated messages, appointment requests, prescription refill requests, patient health profile entries, portal access audit logs.

**Provenance/audit:** Data provenance tracking, audit events.

**Public health reporting data:** Immunization registry submissions, syndromic surveillance data, cancer case reports (certified for (f)(1), (f)(2), (f)(4), (f)(5), (f)(7)).

**Research gaps:**
- The vendor website was completely unresponsive during research, preventing access to detailed feature pages, the product brochure PDF, the FHIR API documentation PDF, and the mandatory disclosures page.
- No user reviews exist on any major platform, so there is no independent validation of which features are actually used vs. marketed.
- The depth of billing/RCM capabilities is unclear — it's described as having "Practice Management and Billing solutions" but the specific billing features (claim scrubbing, ERA/EOB processing, clearinghouse integrations, etc.) are not detailed in available sources.
- Whether the product is cloud-hosted, on-premise, or hybrid is not clearly stated, though the patient portal runs on a separate hosted domain (web.mdronline.net).
