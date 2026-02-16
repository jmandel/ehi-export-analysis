# EnSoftek, Inc — Product Research

Researched: 2026-02-15
Developer website: https://www.drcloudehr.com

## Overview

EnSoftek, Inc is a Beaverton, Oregon–based health IT company with over 22 years of technology experience and approximately 70+ employees, with additional offices in Hinsdale, IL; Washington, DC; and Hyderabad, India. The company's flagship product is DrCloudEHR, a cloud-based electronic health record platform focused specifically on **behavioral health and human services organizations**. EnSoftek reports having assisted over 170 public and private sector enterprises and completed over $175M in technology projects. The product is described as being in use in 26 states. EnSoftek holds government contracting vehicles (CIO-SP3 Small Business GWAC, GSA MAS), reflecting a significant government/public-sector customer base — several of their press-release customers are county health departments.

EnSoftek is a small, privately-held company. Their go-to-market is direct sales, with a particular focus on CCBHCs (Certified Community Behavioral Health Clinics), county health and human services agencies, substance use disorder treatment programs, and IDD (intellectual/developmental disability) service providers. They are not a general-purpose ambulatory EHR — the product is deeply specialized for behavioral health and human services workflows.

## Product: DrCloudEHR

CHPL IDs: 10835

### What It Is

DrCloudEHR is a cloud-based, MU Stage 3 certified EHR purpose-built for behavioral health and human services. The certified module appears to be the whole product — there is no evidence of a separate "certified module" vs. a larger platform. DrCloudEHR encompasses clinical documentation, practice management, billing, patient engagement, telehealth, and reporting in a single integrated platform.

The CHPL certification is broad: clinical data capabilities (a)(1)–(a)(5), (a)(12), (a)(14)–(a)(15); transitions of care (b)(1)–(b)(3); patient portal (e)(1); public health reporting (f)(1)–(f)(2); FHIR APIs (g)(7), (g)(9)–(g)(10); clinical quality measures (c)(1)–(c)(3); and security/infrastructure criteria (d)(1)–(d)(13). This indicates a full-featured EHR with clinical documentation, medication management, lab/imaging ordering, care coordination, patient portal, e-prescribing, and public health reporting.

### Users & Market

**Target users:** Clinicians (psychiatrists, psychologists, therapists, counselors, social workers), nurses, prescribers, front desk/scheduling staff, billing staff, program managers/administrators, and patients (via portal).

**Clinical settings served:**
- Mental health clinics
- Substance use disorder (SUD) treatment programs
- Certified Community Behavioral Health Clinics (CCBHCs)
- Intellectual and developmental disability (IDD) service providers
- Applied Behavior Analysis (ABA) providers
- Children and family services agencies
- County health and human services departments
- Public health organizations

**Notable customers:**
- Yamhill County Health and Human Services (Oregon) — selected after competitive procurement for integrated behavioral health, developmental disabilities, and public health services
- Marion County Health and Human Services — unanimous board of commissioners vote approving contract
- Vitality Unlimited — Nevada CCBHC provider with four locations
- K.A.M Alliance
- Community Hope and Recovery Center
- Public Health Supportive Services (PH-SS) — strategic partnership supporting CCBHCs nationwide

The customer base is heavily weighted toward public-sector/safety-net organizations: county agencies, CCBHCs, and community behavioral health providers.

### Modules & Functionality

Based on vendor website, press releases, and third-party reviews, DrCloudEHR includes the following modules and capabilities:

**Clinical Documentation & Care:**
- Referral and intake management
- Clinical assessments and documentation
- Person and family-centered treatment planning
- Service delivery documentation
- Progress notes
- Form Builder — customizable clinical forms for documentation
- "Golden Thread" — quality management system with automated alerts after predetermined clinical events
- Support for the nine required CCBHC service areas (crisis services, outpatient MH/SUD treatment, etc.)

**Medication Management:**
- ePrescribing (via DrFirst integration, per mandatory disclosures page)
- Electronic Medication Administration Record (eMAR) — noted as relevant for long-term care/residential settings
- Drug-drug and drug-allergy interaction checking
- Computerized Provider Order Entry (CPOE) for medications, labs, and diagnostic imaging

**Practice Management:**
- Calendar and scheduling module
- Front desk management
- Document management with scanning and file storage
- Role-based access controls
- Electronic signatures

**Billing / Revenue Cycle Management:**
- Integrated billing module with "full spectrum" RCM functions
- Clearinghouse integration (Office Ally mentioned in third-party review)
- Claims management — vendor claims 35% improvement in first-pass claim acceptance rates
- Compliance with state quality reporting measures and Medicaid billing rules

**Patient Engagement:**
- Patient portal for self-service registration, appointments, forms, lab reviews, consent signing
- Telehealth (integrated)
- Vendor claims 50% reduction in intake time via portal

**Reporting & Analytics:**
- Standard built-in reports
- Custom report generator
- Business intelligence dashboards
- KPI tracking and outcomes measurement
- Real-time compliance dashboards (vendor claims 50% reduction in audit prep time)
- CCBHC-required clinical measures for state-level reporting

**Interoperability & Data Exchange:**
- "Connections Suite" for interoperability
- DIRECT Project messaging (via EMRDirect DIRECT Trust Messaging, per disclosures page)
- FHIR APIs (standardized API for patient and population services)
- Immunization registry reporting
- Syndromic surveillance reporting to public health agencies
- Transitions of care / clinical information reconciliation

**AI Features (newer additions):**
- AI Group Scribing — AI-powered group therapy documentation with speaker diarization (up to 15 participants), sentiment analysis, per-speaker summaries, interaction timelines, clinical keyword detection, and audit-ready group transcripts
- DrCloudDictate — clinical dictation
- DrCloudIQ — details not fully described on the website

**IDD/ABA-Specific:**
- ABA tools for comprehensive assessments and data analysis
- Configurable workflows for developmental disability services

**Infrastructure:**
- Cloud-hosted
- Mobile support with offline functionality ("Unplugged")
- HIPAA compliance, multi-factor authentication, encryption, audit logging

### Data & Content

Based on the modules and features described above, DrCloudEHR stores and manages:

- **Patient demographics and registration data** — per (a)(5) certification and patient portal intake
- **Clinical notes and assessments** — treatment plans, progress notes, intake assessments, service delivery records
- **Medication data** — prescriptions (via ePrescribing/DrFirst), medication administration records (eMAR), drug interaction data
- **Lab and imaging orders** — CPOE for labs and diagnostic imaging per (a)(2)–(a)(3) certification
- **Billing and claims data** — integrated RCM, insurance information, claim submissions, clearinghouse transactions
- **Scheduling and appointment data** — calendar module
- **Patient portal data** — messages, consents, completed forms, self-registration data
- **Telehealth session data** — integrated telehealth module
- **Documents and scanned files** — document management with scanning
- **Immunization records** — per (f)(1) public health reporting certification
- **Syndromic surveillance data** — per (f)(2) certification
- **Clinical quality measures** — per (c)(1)–(c)(3) certification
- **Audit logs** — per (d)(2) certification requirements
- **Care coordination / transitions of care records** — CCDAs, clinical information reconciliation
- **AI-generated content** — group therapy transcripts, dictation output, sentiment analysis, per-speaker summaries
- **CCBHC-specific program data** — required service area documentation, compliance measures, state reporting data
- **IDD/ABA assessment data** — behavioral assessments, ABA data collection
- **Electronic signatures**

The mandatory disclosures page notes that some functionality requires third-party integrations (DrFirst for ePrescribing, EMRDirect for DIRECT messaging), implying that some data may flow through or be stored in external systems, though the EHR is the primary repository.

One area that's **unclear**: The website doesn't specifically describe lab results storage (as opposed to lab ordering), though the patient portal mentions "lab reviews." The (a)(14) certification for implantable device lists suggests the system stores device data, but this isn't prominently featured in marketing (likely because it's less relevant for the behavioral health market). Similarly, the (a)(12) family health history and (a)(15) social/psychological/behavioral data criteria suggest storage of these data types, though the latter is deeply relevant to behavioral health and likely a core part of clinical documentation.

---
