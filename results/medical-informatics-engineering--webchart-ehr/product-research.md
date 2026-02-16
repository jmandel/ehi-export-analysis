# Medical Informatics Engineering — Product Research

Researched: 2026-02-15
Developer website: https://www.webchartnow.com

## Overview

Medical Informatics Engineering (MIE) is a privately held health IT company founded in 1995, headquartered in Fort Wayne, Indiana. MIE was an early pioneer in cloud-based EHR systems and health information exchange — the company was "ahead of the cloud long before 'cloud computing' became a term of art," deploying web-based SaaS applications for healthcare since the late 1990s. MIE was among the first 18 EHRs certified by the Certification Commission for Health Information Technology.

Today, MIE operates three main product lines: **WebChart EHR** (ambulatory/clinical EHR), **Enterprise Health** (occupational and employee health platform, built on WebChart's technology), and **Ozwell AI** (an AI-powered health IT assistant). The company primarily serves ambulatory physician practices (from solo to multispecialty groups), occupational health providers, Fortune 500 employer health programs, hospitals and health systems, government agencies, and universities. Notable customer Concentra (a large occupational health provider) deployed MIE's platform across its worksite health centers starting around 2010.

In April 2024, MIE received a significant growth investment from Serent Capital, a healthcare-focused PE firm with $5B AUM. The press release noted MIE had grown by an average of 40% annually over the prior six years and maintained a near-100% client retention rate. The investment was intended to expand the Enterprise Health occupational health platform. MIE markets itself as serving "hospitals and health systems, physician practices, Fortune 500 employers, government agencies and consumers." Exact customer counts are not publicly disclosed.

## Product: WebChart EHR

CHPL IDs: 11022

### What It Is

WebChart EHR is a cloud-based, web-native electronic health record system for ambulatory medical practices. It is marketed as "The minimally invasive EHR" — emphasizing its flexibility, customizability, and ability to be adopted incrementally (module by module) rather than requiring an all-at-once implementation. The product is fully web-based — accessible from any browser without client software installation.

WebChart is the certified product under ONC certification (CHPL ID 15.04.04.1932.WebC.84.01.0.221117, version 8.4, certified 2022-11-17). It carries a broad set of certifications: 40+ criteria spanning clinical data management (a)(1)-(a)(5), (a)(12), (a)(14)-(a)(15); transitions of care (b)(1)-(b)(3); patient portal (e)(1); clinical quality measures (c)(1)-(c)(3); public health reporting (f)(1)-(f)(2),(f)(5); FHIR APIs (g)(7),(g)(10); and various security/infrastructure criteria. This is a fully-featured ambulatory EHR certification, not a narrow single-purpose module.

Enterprise Health, MIE's occupational health product, is built on WebChart's core platform and extends it with occupational health-specific modules. The WebChart EHR certification therefore underpins both the ambulatory EHR and the Enterprise Health product.

### Users & Market

**Target users**: Physicians, nurses, medical assistants, front desk staff, clinic administrators, transcriptionists, and billing staff in ambulatory settings. The CHPL SED description lists "Medical personnel, clinic administrators." Enterprise Health extends users to occupational health providers, employer health program managers, and supervisors.

**Settings**: Small to mid-sized ambulatory practices across many specialties — primary care, cardiology, orthopedic surgery, OB/GYN, dermatology, pediatrics, neurology, psychiatry, oncology, behavioral health, and particularly occupational/employee health. Also used in urgent care and worksite health centers.

**Notable deployments**: Concentra (major occupational health provider) deployed MIE's WebChart Enterprise Health platform at worksite locations. Multiple physician testimonials cite successful paperless transitions in ambulatory settings, with cardiologists, internists, and family medicine physicians highlighted (Dr. Stephen Beyer, Dr. Jay Alexander, Dr. John Dickins, Dr. Michael Mirro — per HealthITOutcomes article).

**Pricing**: Starts at $350/month per provider, with costs varying based on clinician count and selected modules (per FindEMR).

### Modules & Functionality

WebChart EHR is a comprehensive ambulatory EHR with extensive modular functionality. Based on the vendor's documentation site (docs.webchartnow.com) and marketing materials, the product covers:

**Clinical Documentation & Encounters**:
- Customizable encounter templates by specialty with point-and-click exams
- Chief complaint, HPI, past medical/surgical/family/social history
- Review of systems, physical examination, vitals
- Symptoms/diagnosis management with ICD-11 support
- E&M coding calculator
- Encounter protocols and workflows
- Visit and legacy encounter types
- Clinical education and depart instructions
- Carbon copy functionality for encounter sharing

**Medication Management & E-Prescribing**:
- Full e-prescribing including EPCS (Electronic Prescribing for Controlled Substances) with IdenTrust certificate support
- SureScripts integration for prescription routing, medication history reconciliation, formulary/dosing information
- Drug interaction/allergy warnings and clinical decision support
- E-refill management (pending, errors, all refills)
- Drug guide search and MedicalCodify integration
- Drug plan and formulary lookups
- Remembered prescriptions and medication libraries
- Travel kits

**Order & Result Management**:
- Computerized provider order entry (CPOE)
- Lab orders with real-time lab interfaces
- Order tracking with requisitions
- Observation flowsheets and vitals tracking
- Results review workflows

**Document Management**:
- Full document management system supporting scanned TIFFs, text, Word, PDF, pictures/photos, sketches, and forms
- Web-based and high-speed scanning with barcode indexing
- Bubble form support for standardized data capture
- Inbound fax queue management and outbound faxing
- Print definitions for documents, forms, and chart printing
- DICOM imaging: viewer, modality worklist (MWL), CD/DVD burning
- RadOmni and TechOmni interfaces for radiology workflow
- MammoTrack for mammography tracking

**Scheduling**:
- Appointment scheduling with multiple views
- Patient/appointment wizard
- Waiting lists
- Check-in functionality
- Guided template schedules
- Cancellation/no-show tracking
- Email appointment reminders

**Patient Portal & Engagement**:
- Patient portal with secure access to health information
- Self check-in capability
- Health questionnaires
- Portal activation codes
- Secure messaging from portal
- Virtual waiting room
- NoMoreClipboard integration
- Applicant portal (for employee health use cases)
- Employer/employee portal
- Supervisor portal with scheduling and questionnaire capabilities

**Injection & Immunization Management**:
- Injection tracking with vial management
- CHIRP (state immunization registry) interface
- Mass injection recording
- Vaccine compliance tracking

**Case Management & Injury Care** (particularly strong for occupational health):
- Case types: OSHA, hospital, absence management, MSEA
- Restriction tracking and editing (work restrictions/accommodations)
- Work status tracking
- Multiple exposure management
- Lost time tracking

**Health Surveillance & Compliance** (occupational health focus):
- Health surveillance panels with automated and manual membership
- Panel action evaluator and action rules
- Due list management
- Respirator information tracking
- Industrial hygiene integration
- Medical clearance workflows
- DOT fitness determination exams

**Occupational Health Programs**:
- Occupational medicine workflows
- Worksite injury & illness tracking
- Absence management
- Health risk assessment
- Employee assistance program
- Medical surveillance programs

**Dictation & Transcription**:
- MIEPlayer for voice recording
- SpeechMike dictation support
- Dictation routing and editing
- Transcription workflows
- Whisper AI dictation and summarization (via Ozwell AI)

**Quality & Reporting**:
- Quality reporting enrollment and provider status tracking
- Promoting Interoperability (PI) measures
- OSHA 300 Log, 300A, and 300/301 reporting
- 50+ specialized reports (activity logs, appointments, cases, demographics, encounters, medications, observations)
- DataVis grid data tools
- CSV export
- RAF Score (Risk Adjustment Factor)
- OpenPM export capabilities

**Financial/Billing**:
- Deal management and financial encounter sections
- Pending billing reports
- Insurance eligibility checking
- Insurance summary management
- Fee schedules
- EOB (Explanation of Benefits) scanning
- Integration with practice management and billing systems
- Revenue cycle management described on marketing site

**E-Signature**:
- Electronic signature workflows
- Request and un-request e-signature capabilities
- Pending review workflows

**Task Management**:
- Task lists with search
- Fast task templates
- Delegated and pending task tracking

**Integrations & Interoperability**:
- Over 300 vendor integrations claimed
- HL7 interfaces
- DICOM
- IHE profiles
- CCR/CDA document support
- FHIR APIs (g)(7) and (g)(10)
- Lab interfaces (real-time)
- Pharmacy interfaces (SureScripts)
- Immunization registry interfaces (CHIRP)
- Custom pharmacy setup
- Interface manager for managing connections
- Datasend queue for outbound data
- ODBC connectivity
- CSV import/export APIs for clinical encounters, injections, observations, PFT data, vital signs, lab results

**System Administration**:
- User/provider and department management
- Security roles with comparison tools
- SSO (SAML, ADFS)
- Multi-factor authentication
- Audit logging
- Chart merging
- Partition management
- Multilingual support
- Translation manager
- Asset management module (equipment tracking, warranties, maintenance, calibration)
- Scheduled jobs
- Auto-routing rules

**Data Migration**:
- ETL tools and standardized import formats
- Specialized importers for employees, health surveillance, audiometric data, PFT, vital signs, cases, panel membership
- CCR document import
- Chart file export

**Specialty Data Entry**:
- Audiogram data entry
- Vision testing
- Biometric data
- EKG data
- PFT (pulmonary function testing)
- X-ray results

### Data & Content

Based on the features documented above, WebChart EHR stores and manages a very broad range of clinical and administrative data:

**Clinical records**: Patient demographics, medical history (medical, surgical, family, social, gynecological, pregnancy), encounters/visit notes, chief complaints, review of systems, physical examination findings, vitals, diagnoses (ICD-11), clinical assessments, and depart instructions.

**Medication data**: Prescriptions (including controlled substances), medication lists, allergy/intolerance records, drug interaction data, refill requests, SureScripts medication history, formulary information.

**Orders & results**: Lab orders and results, observation data with flowsheets, vital sign tracking, imaging orders.

**Documents**: Scanned paper documents (TIFF), PDFs, Word documents, photos/pictures, sketches, forms, faxes (inbound and outbound), DICOM images, dictation audio files, transcriptions.

**Immunizations**: Injection records, vial tracking, vaccine compliance data, immunization registry submissions.

**Scheduling**: Appointments, waiting lists, check-in records, cancellations, no-shows.

**Portal data**: Patient portal messages, health questionnaires, portal activation/access records, self-check-in data.

**Occupational health data**: Case records (OSHA, injury/illness), work restrictions and accommodations, work status, exposure records, health surveillance panel memberships and results, respirator fit data, audiometric data, PFT results, vision test results, biometric data, EKG data, X-ray results, DOT fitness determinations, medical clearances, absence records, industrial hygiene data.

**Financial/billing data**: Insurance information and eligibility, deals, fee schedules, EOBs, pending billing records. The marketing site describes "Revenue Cycle Management" with billing and claims processing, though the detailed documentation also mentions OpenPM integration, suggesting billing may be partially handled by an external practice management system (OpenPM) in some deployments.

**Quality/compliance data**: Quality measure data, PI reporting data, OSHA 300/300A/301 case data, RAF scores.

**Administrative data**: User accounts, security roles, audit logs, task records, e-signature records, system configuration, interface/integration configuration, asset management records (equipment, calibration, maintenance).

**Key uncertainty**: While WebChart clearly has billing-adjacent features (insurance eligibility, fee schedules, deals, pending billing reports, EOB scanning, revenue cycle management), it's somewhat unclear whether full claims submission and billing is entirely built-in or whether some deployments rely on separate practice management/billing systems (e.g., OpenPM) for the complete billing workflow. The marketing site describes integrated RCM, but the documentation's references to "OpenPM export" suggest a hybrid approach may be common.
