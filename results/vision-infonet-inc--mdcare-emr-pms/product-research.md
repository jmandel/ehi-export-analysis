# Vision Infonet Inc — Product Research

Researched: 2026-02-15
Developer website: http://www.vinfonet.com

## Overview

Vision Infonet Inc is an Illinois-based healthcare technology and services company founded in 1999 by a medical doctor (Dr. Murali). Headquartered in Naperville, IL, the company has grown to serve over 2,000 clients across the United States with 750–1,000+ employees across multiple locations (including international offices in Asia and Europe). The company positions itself primarily as a healthcare back-office services provider, offering medical billing/RCM, medical coding, medical transcription, denial management, and back-office services — with MDCare EMR/PMS as their proprietary EHR/practice management software product.

Vision Infonet reports handling $200M+ in revenue, 500,000+ claims, and 600,000+ calls annually across its client base, and claims to support 50,000+ physicians. The company serves practices ranging from solo providers to groups with 400+ physicians. This is a mid-size vendor whose business model combines software (MDCare EMR/PMS) with managed services (billing, coding, transcription). The EMR appears to be tightly coupled with their billing services offering — many clients likely use both. The company is privately held and does not appear on major third-party review platforms (G2, Capterra, Software Advice) with a dedicated profile, suggesting a relatively low market profile compared to larger EHR vendors.

## Product: MDCare EMR/PMS

CHPL ID: 11650

### What It Is

MDCare EMR/PMS is a web-based, ONC-certified combined Electronic Medical Records (EMR) and Practice Management System (PMS) designed for ambulatory/outpatient practices. It is currently at version 6.0, certified as of June 2025. The product name "EMR/PMS" reflects its dual nature — it is both the clinical charting system and the practice management/billing system in a single platform. The certified module appears to be the whole product, not a component of something larger.

The product carries a broad set of ONC certifications including clinical data criteria (a)(1)–(a)(5), (a)(12), (a)(14), transitions of care (b)(1), clinical quality measures (c)(1),(c)(3),(c)(4), FHIR API access (g)(10), and public health reporting (f)(3) — indicating it is a full-featured clinical EHR, not a niche or limited system.

### Users & Market

**Target users**: Physicians, nurses, and admin/billing staff (per the CHPL SED description: "Physician / Nurses / Admin Users").

**Clinical settings**: Ambulatory/outpatient practices of varying sizes, from solo practices to multi-provider groups (1–100+ physicians). The product serves multiple medical specialties — the vendor specifically markets specialty-specific versions for cardiology, dermatology, endocrinology, family practice, pulmonary medicine, psychiatry, critical care, geriatric/palliative care, radiology, podiatry, and internal medicine.

**Customer base**: Vision Infonet claims 2,000+ clients across the U.S. It is unclear what fraction of these are MDCare EMR users vs. billing-services-only clients. Testimonials on the vendor website reference physicians in pulmonary medicine, psychiatry, critical care, dermatology, radiology, podiatry, geriatric/palliative care, and internal medicine.

**Deployment**: Cloud/web-based — "access from any device, anywhere" with no special infrastructure required beyond an internet connection.

No notable large health system deployments or case studies were found. The product appears to serve smaller independent practices, consistent with Vision Infonet's positioning as a back-office services company for practices that want to outsource billing and related functions.

### Modules & Functionality

Based on vendor materials (mdcare.com and vinfonet.com), MDCare EMR/PMS includes the following modules and features:

**Clinical Documentation / EMR**:
- Customizable specialty-specific templates (point-and-click)
- Multiple documentation modes: structured templates, free text, speech recognition, tablet handwriting recognition
- AI-powered features (v6.0): speech-to-text for clinical notes, automated SOAP note generation from voice, AI-based ICD/CPT code generation
- Clinical decision support tools (evidence-based diagnosis support)
- Health maintenance recording and disease management
- Over 1,000 customizable patient education handouts
- Integrated digital signature

**E-Prescribing (eRx)**:
- Surescripts integration for electronic prescribing
- (Certified for (a)(1) CPOE and (a)(4) drug-drug/drug-allergy interaction checks, implying medication lists, allergy lists, drug interaction checking)

**Scheduling**:
- Drag-and-drop appointment scheduling and rescheduling
- Multi-provider and resource scheduling (nurses, rooms, equipment)
- Appointment management: cancel, no-show, hold time slots for specific types/procedures
- Authorized visit management

**Billing / Practice Management (PMS)**:
- Integrated billing module with CMS-1500 claims filing
- Accounts receivable (AR) module
- Denial management module
- Automated CPT coding / E&M coding
- Point-of-service (POS) collections
- Electronic superbill
- (The tight coupling with Vision Infonet's billing services suggests the billing module handles insurance claims, payment posting, and related revenue cycle data)

**Document Management**:
- Document editing and management module
- Consolidation of consult letters, patient files, insurance IDs, consent forms with built-in imaging/scanning functionality
- Fax integration ("Faxtone" — integrated fax)

**Interfaces & Interoperability**:
- HL7 interface
- DICOM interface (for imaging)
- Lab interfacing (lab orders/results)
- Fax interfacing
- FHIR API (certified for g(10))
- Patient portal (confirmed by the existence of app.mdcare.com/mdcareportal — a dedicated patient portal application)
- HIPAA-compliant email
- Clinical messaging between physicians and staff

**Compliance & Reporting**:
- HIPAA compliant
- ICD-10 compliant
- MU3 / 2025 MIPS compliant
- Clinical quality measure reporting (certified for (c)(1), (c)(3), (c)(4))
- Immunization registry reporting (certified for (f)(3))
- Customizable end-of-day and practice performance reports

**AI Capabilities (newer in v6.0)**:
- AI-based authorization generation
- AI-based payment posting and denial management
- Practice performance analysis

### Data & Content

Based on the features described above and the certification criteria, MDCare EMR/PMS stores and manages the following categories of data:

**Clinical data** (strongly evidenced by vendor materials + certification):
- Patient demographics and registration data
- Clinical encounter/visit notes (SOAP notes, specialty-specific documentation)
- Problem lists, medication lists, allergy lists (certified (a)(1)–(a)(5))
- Vital signs and clinical assessments
- Lab orders and results (lab interfacing described)
- Imaging/DICOM data (DICOM interface mentioned)
- Prescriptions and medication history (Surescripts eRx integration)
- Clinical decision support data
- Patient education materials delivered
- Health maintenance and disease management tracking
- Immunization data (certified for (f)(3) immunization registry reporting)
- Clinical quality measure data
- Care plan data (certified for (a)(12) family health history, (a)(14) implantable device list)
- Digital signatures on clinical documents

**Administrative/practice management data** (evidenced by vendor materials):
- Appointment scheduling data (appointments, cancellations, no-shows, provider schedules, resource schedules)
- Insurance and billing data (claims, CMS-1500 forms, superbills, CPT/ICD codes)
- Accounts receivable data (payments, denials, collections)
- Patient registration and insurance ID documents
- Consent forms and scanned documents

**Communication data** (evidenced by vendor materials):
- Clinical messages between physicians and staff
- HIPAA-compliant emails
- Fax records (integrated fax system)
- Patient portal data (patient-facing portal exists at app.mdcare.com/mdcareportal)

**Gaps/uncertainties**:
- The vendor website doesn't specifically mention referral management, though it likely exists given the multi-specialty ambulatory focus.
- The extent of patient portal functionality (messaging, appointment requests, bill pay, etc.) is unclear — the portal exists but its capabilities aren't well documented on the marketing site.
- Whether the product stores discrete radiology reports vs. just DICOM image links is unclear.
- The product is not found on major third-party review platforms (G2, Capterra, Software Advice), which limits independent validation of features. Most information comes from the vendor's own marketing materials.
- The mandatory disclosures PDF (mdcare.com/pdf/MDCAREEMRPMSDisclosurestatement.pdf) could not be read/parsed, so any additional product details or limitations documented there are not reflected in this report.
