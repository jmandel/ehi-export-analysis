# PCE Systems — Product Research

Researched: 2025-07-14
Developer website: https://www.pcesystems.com

## Overview

PCE Systems is a small, privately held IT services company based in Farmington Hills, Michigan, with an estimated 11–50 employees. The company specializes in building custom, fully-hosted electronic health record (EHR) and care management software for community-based behavioral health and social service organizations. PCE's primary market is Michigan's public behavioral health system — specifically the Community Mental Health Service Programs (CMHSPs) and Prepaid Inpatient Health Plans (PIHPs) that serve Medicaid beneficiaries with mental illness, substance use disorders, and developmental disabilities.

As of a 2013 press release, PCE described itself as "the largest behavioral health Electronic Medical Record (EMR) and provider management system vendor in the State of Michigan, with clients encompassing over 70% of the Michigan Medicaid mental health budget." The company has been in operation since at least 2001 (per Wayback Machine records). Jeff Chang, identified as Project Manager in 2013, is now CEO. The company's website is deliberately minimal — just a logo and navigation links (Home, About, Location), with the About and Location pages returning 404 errors as of 2025. The site has looked essentially the same since at least 2019. PCE does not appear to have a public marketing presence, product demos, or feature pages. This is consistent with a vendor whose customers are a known, finite set of government-funded behavioral health agencies in Michigan, acquired through direct relationships rather than inbound marketing.

## Product: PCE Care Management

CHPL ID: 11045
CHPL Product Number: 15.04.04.2125.PCEC.94.01.1.221205
Version: 9.4

### What It Is

PCE Care Management is a behavioral health EHR system designed to manage the full lifecycle of care for individuals receiving community mental health, substance use disorder treatment, and developmental disability services. The SED (Safety-Enhanced Design) intended user description in CHPL metadata is simply "Behavioral Health."

The product is broadly certified across 44 ONC criteria spanning clinical data (a)(1)–(a)(5), (a)(12), (a)(14)–(a)(15); transitions of care (b)(1)–(b)(3), (b)(9)–(b)(11); patient portal (e)(1), (e)(3); clinical quality measures (c)(1)–(c)(4); public health reporting (f)(1), (f)(7); and FHIR APIs (g)(7), (g)(9)–(g)(10). This is a comprehensive certification profile indicating a full-featured clinical EHR, not a limited-scope module.

The certified product appears to be the entire system — there is no evidence of PCE Care Management being a module within a larger product platform. The system is described as "fully-hosted" (cloud/hosted model, not on-premise), and the production FHIR API endpoint is at `w3.pcesecure.com`.

### Users & Market

**Primary users:** Clinicians, case managers, and administrative staff at Michigan community-based behavioral health organizations — including CMHSPs (Community Mental Health Service Programs), PIHPs (Prepaid Inpatient Health Plans), and their contracted service providers.

**Known customers:**
- **Detroit Wayne Integrated Health Network (DWIHN)** — the largest PIHP in Michigan, serving Wayne County (Detroit metro area). DWIHN's website hosts PCE API documentation and MichiCANS assessment training materials for PCE Systems.
- **Oakland Community Health Network (OCHN)** — a CMH authority serving ~30,000 Oakland County citizens at 400+ service sites. OCHN's website explicitly names PCE Systems as their EHR vendor and references the PCE API and patient portal (CEHR).
- **Community Mental Health Partnership of Southeast Michigan (CMHPSM)** — a PIHP serving Lenawee, Livingston, Monroe, and Washtenaw counties. CMHPSM's website describes their PCE-based EHR as "CRCT" (Confidential Record of Consumer Treatment), used by the PIHP, partner CMHSPs, and providers for claims submission, incident reporting, and service information.
- **Washtenaw County Community Mental Health** — featured in an ONC Brightspot case study as a PCE customer. Serves 5,000+ children and adults with serious mental illness, developmental disabilities, or emotional disturbances.

**Clinical settings:** These are not private medical practices. PCE's customers are publicly funded behavioral health authorities that manage networks of providers serving vulnerable populations — people with serious mental illness (schizophrenia, bipolar disorder, major depression), substance use disorders, developmental disabilities (autism, cerebral palsy, cognitive impairment), and co-occurring conditions. Settings include community mental health centers, substance abuse treatment programs, crisis services, residential treatment, clubhouse programs, and social service organizations.

**Geographic concentration:** Heavily Michigan-focused. All identified customers are Michigan public behavioral health entities. The 2013 claim of 70%+ of Michigan's Medicaid mental health budget suggests PCE is the dominant vendor across the state's CMH system.

**Scale:** PCE is small (11–50 employees) but punches above its weight in terms of the population served — Michigan's public behavioral health system serves hundreds of thousands of Medicaid beneficiaries across dozens of CMHSPs.

### Modules & Functionality

PCE's website provides essentially zero product information. However, the following functionality is documented across multiple third-party sources:

**Clinical Documentation & Care Management:**
- Intake and assessment (per MedicalRecords.com profile)
- Individualized treatment plan creation and tracking (MedicalRecords.com)
- Clinical assessments including MichiCANS (Michigan Child and Adolescent Needs and Strengths) — confirmed by DWIHN training materials
- Integrated health management / care coordination across providers (MedicalRecords.com)
- Discharge planning (MedicalRecords.com)
- Incident reporting (CMHPSM EHR page)

**Patient Portal (CEHR):**
- The patient portal is referenced as "CEHR" in the API documentation and the OCHN website
- Supports SMART on FHIR OAuth2 patient authentication
- Certified for patient view/download/transmit — (e)(1)

**Health Information Exchange (PIX):**
- PCE operates "PIX" (Provider Information Exchange), a behavioral health HIE built into the platform
- PIX uses common HIE standards and APIs to connect PCE EHR implementations across Michigan
- PIX enables providers to search for patient records from other PCE implementations, finding care team info, treatment plans, appointments, problem lists, medications, vitals, lab results, and clinical documentation (per ONC Brightspot case study)
- PIX is consent-managed — PCE built an eConsent Management System for 42 CFR Part 2 compliance (substance use disorder treatment privacy) and Michigan Mental Health Code requirements
- PCE is connected to MiHIN (Michigan Health Information Network) as a Virtually Qualified Data Sharing Organization, enabling data exchange between behavioral health and physical health networks

**MI Care Connect Portal:**
- A standalone portal providing PIX access to community partners who may not use PCE's EHR directly
- Used by community organizations like Packard Health, Shelter Association of Washtenaw County, and Avalon Housing (per ONC Brightspot)

**Billing:**
- Billing is described as integrated in the MedicalRecords.com profile ("from... all the way to billing")
- CMHPSM describes using the PCE EHR for "claims submission"
- TMG (The TM Group) sells a separate integration product ($5,000) connecting PCE Systems to Microsoft Dynamics 365 Business Central for accounting — handling cost centers, accounts payable transactions, and vendor information. This suggests PCE handles clinical billing/claims internally but some organizations use external accounting systems for financial management.
- The FHIR API includes Claims and Coverage resources, confirming claims data is stored

**Public Health Reporting:**
- Certified for (f)(1) transmission to immunization registries and (f)(7) health care surveys

**Clinical Quality Measures:**
- Certified for CQM recording (c)(1), import (c)(2), export (c)(3), and filtering (c)(4)

**FHIR API (g)(10)):**
- Full SMART on FHIR API supporting Patient and Population Services
- Exposed FHIR resources per API documentation: AllergyIntolerance, CarePlan, CareTeam, Claim, Condition, Coverage, Device, DiagnosticReport, DocumentReference, Encounter, Goal, HealthcareService, Immunization, Location, MedicationRequest, Observation, Organization, Patient, Practitioner, PractitionerRole, Procedure, Provenance
- Also includes a Message data element in API documentation, suggesting messaging capabilities
- Supports bulk export for population-level data access

### Data & Content

Based on the evidence gathered, PCE Care Management stores the following categories of data:

**Clinical Data** (confirmed via FHIR API resources and USCDI mapping in API documentation):
- Patient demographics
- Allergies and intolerances
- Conditions / problem lists
- Medications (medication requests)
- Immunizations
- Procedures
- Vital signs, laboratory results, smoking status (via Observations)
- Diagnostic reports
- Clinical notes / documents (DocumentReference, DiagnosticReport)
- Care plans / assessment and plan of treatment
- Care team members
- Goals
- Implantable devices (UDI)
- Encounters
- Provenance

**Behavioral Health-Specific Data** (confirmed via various sources):
- Treatment plans (individualized, per MedicalRecords.com and ONC Brightspot)
- Clinical assessments (MichiCANS and likely others — per DWIHN training materials)
- Intake and assessment records
- Discharge records
- Incident reports (per CMHPSM)
- Consent directives (eConsent Management System for 42 CFR Part 2 and Michigan Mental Health Code)

**Claims & Financial Data:**
- Claims data (FHIR Claims resource in API; CMHPSM uses system for "claims submission")
- Coverage / insurance information (FHIR Coverage resource)
- Service information reporting (per CMHPSM)

**Administrative & Care Coordination Data:**
- Provider/practitioner information (Practitioner, PractitionerRole resources)
- Organization and location data
- Healthcare service definitions
- Care team assignments
- Messages (Message data element in API documentation)
- Patient portal (CEHR) data — access logs, patient interactions

**Documents & Files:**
- Scanned documents, PDFs, and other non-computable files (confirmed by EHI export documentation which describes a "Files subdirectory" containing "exported, non-computable files... e.g., scanned documents, PDFs")

**Notable Data Considerations:**
- 42 CFR Part 2 data: The system explicitly manages substance use disorder treatment records with consent-based access controls. The API Terms of Use specifically references compliance with "42 C.F.R. Part 2" alongside HIPAA.
- Social service referral data: PCE signed MiHIN's Interoperable Referrals Pledge (2022) alongside social care companies like findhelp, Unite Us, and WellSky, suggesting the platform handles social service referral data.
- The EHI export documentation (b)(10) is only 3 pages and describes the export format (password-protected zip, NDJSON per resource, documentation.json for schema) but does **not** enumerate the specific data resources included in the export. The resource definitions are embedded in the `documentation.json` file within the export itself.

**Information gaps:**
- No product feature page, user manual, or detailed module documentation is publicly available from PCE Systems
- The vendor website is essentially non-functional for research purposes
- Scheduling capabilities are not mentioned in any source, though they likely exist given the ONC Brightspot mentions "appointments" as viewable through PIX
- e-Prescribing (EPCS, Surescripts integration) is not mentioned — behavioral health prescribing patterns may differ from general ambulatory care
- Patient messaging details beyond the API's Message data element are unclear
- Whether the system handles authorization/prior-auth workflows for Medicaid services is unclear, though this would be expected for a CMH/PIHP-focused product
