# EnableDoc LLC — Product Research

Researched: 2026-02-15
Developer website: https://www.enabledoc.com/

## Overview

EnableDoc LLC is a small health IT company headquartered in McLean, Virginia, founded in 2009. The company has approximately 11–50 employees (per LinkedIn/ZoomInfo data). EnableDoc develops and sells "Enablemypractice," a cloud-based, all-in-one EHR, practice management, and billing platform targeting ambulatory medical practices across a wide range of specialties. The company is privately held, with Steve Rothschild listed as Founder & CEO and primary contact.

EnableDoc markets to diverse practice types including primary care, psychiatry/mental health, physical therapy, chiropractic, urology, pediatrics, ophthalmology, cardiology, occupational therapy, breast imaging/radiology, and multispecialty groups. The vendor emphasizes AI-powered automation (using Deepgram for speech-to-text and ChatGPT for note generation), customizable clinical templates, and integrated billing. The product appears to serve small-to-mid-size ambulatory practices rather than hospitals or large health systems. No notable enterprise customers or large deployments were identified in publicly available materials.

The vendor has very limited third-party review presence — Capterra, Software Advice, and other review sites show only a handful of reviews (approximately 3 total across platforms). Users who have reviewed the product praise its customization capabilities and developer responsiveness but note limitations in reporting and template flexibility. The company does not appear to have significant market share or brand recognition compared to larger EHR vendors.

## Product: Enablemypractice

CHPL ID: 10795
CHPL Product Number: 15.02.05.1439.ENAD.01.01.1.220118
Version: EHR 5.0
Certification Date: 2022-01-18

### What It Is

Enablemypractice is a unified, cloud-based platform that combines EHR, practice management (PMS), billing/revenue cycle management (RCM), patient engagement, telehealth, and a radiology information system (RIS) into a single product. The certified module appears to encompass the full product — there is no indication of separate product lines or distinct platforms. The product is modular, allowing practices to pay for only the functionality they need, but it is marketed and sold as one integrated platform.

The product is certified across a broad set of ONC criteria: clinical data (a)(1)–(a)(5), (a)(12), (a)(14); transitions of care (b)(1)–(b)(2); EHI export (b)(10)–(b)(11); CQMs (c)(1)–(c)(3); patient portal (e)(1), (e)(3); public health reporting (f)(1); FHIR APIs (g)(7), (g)(9)–(g)(10); and health information exchange (h)(1). The SED intended users are described as "Family Medicine, Neurology, Urology."

### Users & Market

The product targets ambulatory practices across 20+ specialties. Key segments mentioned on the vendor website include:
- **Clinical practices**: solo and small group practices
- **Multispecialty groups**: groups with multiple provider types
- **Outpatient centers**: outpatient/ambulatory surgical settings
- **Breast imaging / radiology**: dedicated RIS module for imaging centers

Day-to-day users include physicians, clinical staff, billing staff, practice managers, and patients (via the patient portal). The vendor website does not disclose specific customer counts or case studies. Third-party sources (ZoomInfo, LinkedIn) suggest this is a very small company with limited market penetration.

Pricing is disclosed as approximately $100/month/provider for practice management and $200/month/provider for EHR, with custom pricing for behavioral health and therapy practices ($1/visit/month). Revenue management services are available for 2.5% of collections.

### Modules & Functionality

Based on the vendor's website feature pages, the product includes the following integrated modules:

**AI-Powered Clinical Documentation**
- Speech-to-text dictation using Deepgram, with AI (ChatGPT-based) transformation into structured clinical notes
- Customizable specialty-specific templates with configurable fields (checkboxes, text, tables, date fields)
- AI auto-populates ICD-10 codes, CPT codes, current medications, prescriptions, lab orders/results, allergies, vitals, devices, and immunizations into notes
- Pull-from-prior functionality to retrieve prior visit notes (whole note or by section/field)
- Professional word processor with formatting, spell-check, electronic signatures
- Encrypted PDF note storage with addendum and supervisor co-signature support
- Macro insertion capabilities
(Source: enabledoc.com/ai-powered-clinical-documentation-with-custom-templates/)

**Smart Scheduling & Appointments**
- Drag-and-drop graphical schedule with custom colors and visit types
- Booking by provider, resource, service, facility, and room
- Online patient self-booking
- Telehealth appointment links auto-generated
- Google Calendar synchronization
- Voice, text, email, and app appointment notifications
- Insurance eligibility checking and account balance display at scheduling
- Group/class appointments, waiting list management
- Patient location tracking and on-demand chat
- Electronic referrals and Direct Messaging integration
(Source: enabledoc.com/smart-scheduling-appointments/)

**E-Prescribing & Medication Management**
- Electronic prescribing to any pharmacy, including EPCS (electronic prescribing for controlled substances)
- Built-in drug database with AI prescription writing assistance
- Medication reconciliation (request/reconcile past medications with current)
- PDMP (Prescription Drug Monitoring Program) integration with NARX score checking
- Medication and immunization inventory management
- Medication administration documentation with superbill/billing integration
- Drug interaction warnings and formulary/benefits checking
(Source: enabledoc.com/eprescribe-pdbm/)

**In-House & Electronic Lab Orders**
- Electronic ordering and results with major labs (LabCorp, Quest, regional labs)
- In-house lab/test ordering and results management
- Results review interface for clinicians
- Results available for patient portal transmission
(Source: enabledoc.com/inhouse-and-electronic-labs-orders/)

**AI Medical Billing & Revenue Cycle**
- AI-powered code generation (CPT, ICD-10, modifiers) from clinical notes
- Code verification with payer- and specialty-specific suggestions
- Electronic claims submission and tracking
- ERA (Electronic Remittance Advice) processing and payment reconciliation
- Electronic patient statements with integrated credit/debit card processing
- AI reads paper EOBs and creates insurance payment records
- Superbill management
- AR aging dashboard and collections management
- Real-time claim tracking
(Source: enabledoc.com/ai-medical-billing/)

**Patient Engagement & Telehealth**
- Patient portal: access clinical summaries, notes, reports, vitals, test results
- Patients can track health/vitals, complete intake forms, access televisits, send messages, chat securely, pay bills, update insurance
- Telehealth via web browsers and iOS/Android mobile apps
- Secure messaging (text, email, voice, app notifications) with speech recognition
- Messages saved to patient records
- Automated notifications for appointments, preventive care, birthdays, and custom events
- Automated patient satisfaction surveys
- Task management for patient engagement in preventive/regular care
(Source: enabledoc.com/patient-engagement-and-telehealth/)

**Custom Intake & Smart Data Capture**
- Intake forms sent via text, email, or portal
- In-office and televisit check-in with provider notification
- Customizable forms by visit type
- AI card reader: scans insurance and ID cards to auto-populate records
- Collects demographics, consent forms, guarantor information, insurance, medications, allergies, clinical assessments
- Credit card on file (PCI-compliant vault)
- Driver's license scanning for identity/address verification
- All intake data flows directly into patient chart
(Source: enabledoc.com/custom-intake-smart-data-capture/)

**Chronic Care & Population Management**
- Patient list generation using custom logic
- Program and status tracking
- Vitals and nutrition tracking
- Population-level reporting and management
- Care coordination and proactive outreach tools
(Source: enabledoc.com/chronic-care-population-management/)

**Radiology Information System (RIS)**
- Radiology test ordering with HL7 transmission to PACS
- PACS study prefetching based on patient appointments
- AI-powered radiology reporting with automated diagnosis selection
- Custom radiology templates
- Result tracking through custom fields
- MQSA (Mammography Quality Standards Act) tracking and reporting
- MIPS reporting
- DICOM management and PACS integration
(Source: enabledoc.com/radiology-information-system/)

**Predictive Decision Support (PDSI)**
- AI-driven clinical decision support generating notes from provided clinical information
- Risk management aligned to ONC HTI-1 and NIST AI Risk Management Framework
- Continuous monitoring, periodic audits, incident tracking
- Reinforcement learning from provider feedback
(Source: enabledoc.com/enabledocs-predictive-decision-support-intervention-pdsi-intervention-risk-management-practices-2/)

**Additional Capabilities** (from vendor homepage and disclosure page):
- MIPS quality measure tracking (15 specific CQMs listed in ONC disclosure)
- Direct messaging via Kno2/Surescripts ($50/month per account, per disclosure page)
- FHIR API access (g)(7), (g)(9), (g)(10) — included at no additional charge
- Patient health information capture and implantable device tracking — included at no additional charge
- Document management: scan, upload, route documents
- Electronic signatures
- Security: AES 256-bit encryption, HIPAA compliance

### Data & Content

Based on the vendor's feature descriptions, the product stores and manages the following categories of data:

**Clinical Data**: Patient demographics, clinical notes (AI-generated and manual), problem lists, medication lists, allergy lists, vital signs, immunization records, medical history, clinical assessments, diagnoses (ICD-10), procedures (CPT), clinical templates, note addenda, electronic signatures, supervisor co-signatures.

**Orders & Results**: Prescription records (including controlled substances), lab orders, lab results (electronic from major labs and in-house), radiology orders, radiology reports, PACS/DICOM references, medication administration records.

**Billing & Financial**: Claims data, superbills, ERA/remittance records, payment records, AR aging data, insurance information, eligibility verification records, patient statements, credit card on file (PCI vault), collection records, EOB data.

**Scheduling**: Appointment records, provider schedules/availability, visit types, facility/room assignments, waiting lists, referral records, Google Calendar sync data.

**Patient Engagement**: Patient portal access records, secure messages, chat transcripts, intake form submissions, consent forms, patient surveys, appointment reminders/notifications, telehealth session records.

**Documents**: Scanned documents, uploaded files, insurance card images, driver's license images, encrypted PDF clinical notes, faxes/Direct messages.

**Population Health**: Patient lists, program enrollment/status tracking, vitals/nutrition tracking data, population-level reports, care coordination records.

**Regulatory & Quality**: MIPS/quality measure data, CQM calculations, PDMP/NARX scores, MQSA tracking data, public health reporting data (immunization registries per (f)(1) certification), audit logs.

**Medication-Specific**: Current medications, medication history, prescription routing/pharmacy data, controlled substance tracking, drug interaction data, formulary/benefits data, medication reconciliation records, immunization inventory.

The ONC disclosure page confirms that data export (b)(10), API access, patient health capture, and implantable device tracking are included at no additional cost. Direct messaging is the only certified feature with an additional fee ($50/month per account).

---
