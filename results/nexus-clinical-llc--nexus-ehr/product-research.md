# Nexus Clinical LLC — Product Research

Researched: 2026-02-15
Developer website: https://www.nexusclinical.com/

## Overview

Nexus Clinical LLC is a small, privately held health IT company founded in 2009, headquartered in Delray Beach, FL. The company has approximately 10-19 employees across North America and Asia. Leadership includes CEO Pooja Tripathi (25+ years experience), VP of IT Kiran Agate (who led EHR design and development), a billing consultant (Jennifer Somers, dual AAPC-certified CPC/CPPM), and a director of customer acquisition (Sunil Gupta). The company's mission is delivering affordable Healthcare IT solutions to ambulatory medical practices.

Nexus Clinical makes one product — Nexus EHR — a cloud-based, unified platform combining EHR, practice management, medical billing, patient portal, telehealth, and eFax. The product targets small to midsize ambulatory practices (solo practitioners up to 50+ physician organizations) across 25+ specialties. Pricing starts around $275-299/month per NPI with no long-term contracts. The company competes against much larger players (athenahealth, eClinicalWorks, NextGen) primarily on price, customer service responsiveness, and willingness to customize. Third-party reviews consistently praise the customer support (response times ~2 hours, phone access) — this appears to be their primary competitive differentiator. The exact customer count is not publicly disclosed; the low number of third-party reviews (~19 on Software Finder) suggests a small install base.

## Product: Nexus EHR

CHPL ID: 11130 (version 7.3, certified 2022-12-27, 34 criteria)

### What It Is

Nexus EHR is a comprehensive, cloud-based ambulatory EHR platform. It is a single product — the certified module *is* the whole product. There are no separate product lines or distinct platform editions. The product includes clinical EHR, practice management, medical billing, patient portal, telehealth, and eFax as integrated modules within one system. It is accessible via any web browser or tablet.

The certification is broad: clinical criteria (a)(1)-(a)(5), (a)(12), (a)(14) cover CPOE for medications/labs/imaging, drug interaction checks, demographics, family health history, and implantable devices. Care coordination criteria (b)(1)-(b)(3) cover transitions of care, clinical information reconciliation, and e-prescribing. Patient engagement (e)(1) and (e)(3) cover the patient portal and patient health information capture. Public health criteria (f)(1), (f)(2), (f)(5) cover immunization registry reporting, syndromic surveillance, and electronic case reporting. FHIR APIs are certified under (g)(7), (g)(9), (g)(10). CQM criteria (c)(1)-(c)(3) support 20 clinical quality measures.

Included third-party components: MedlinePlus Connect (patient education) and NewCropRx (pharmacy integration/e-prescribing). Optional add-ons: EMR Direct (interoperability engine) and DynaMed Plus by EBSCO Host (clinical decision support).

### Users & Market

**Target users:** Physicians, nurses, lab managers, pharmacists, clinical staff, billing staff, front desk staff, practice managers, and patients (via portal). The product is ambulatory-focused — no hospital/inpatient capabilities were described.

**Practice sizes:** Solo practitioners up to organizations of 50+ physicians.

**Specialties supported (from vendor materials):** Cardiology, Family Medicine, General Surgery, Neurology, Neurosurgery, Orthopedics, Podiatry, Psychiatry, Pain Management, Behavioral Health, Dermatology, Pediatrics, Urgent Care, Pulmonary, Oncology, Primary Care, and more. Testimonials also reference Minimally Invasive Spine Surgery and Sleep Medicine practices.

**Notable deployments (from testimonials):**
- Bay City Psychiatry (Dr. Mathew Sipple) — Psychiatry
- Costrini Sleep Services, Savannah, GA (Don Causey, VP/COO) — Sleep Medicine
- Dr. Edward Rhomberg, Western Arkansas — Orthopedics
- North Atlanta Surgical Associates (Joan Troy, Practice Administrator) — Surgery
- Fortanasce & Associates Neurology, Arcadia, CA (George McNeill, IT Manager) — Neurology
- Dr. Georgiy Brusovanik — Minimally Invasive Spine Surgery

**Market position:** Very small vendor. No customer count disclosed. Competes on price, service quality, and customization rather than market share or brand recognition.

### Modules & Functionality

The vendor website describes six core modules. Information comes primarily from dedicated pages at nexusclinical.com/features/, nexusclinical.com/nexus-ehr/, and individual module pages.

**1. Electronic Health Records (Core Clinical)**
Source: nexusclinical.com/nexus-ehr/
- Single-screen visit documentation — no window switching needed
- Multi-modal input: preconfigured templates, free text, built-in voice-to-text, Dragon compatibility, transcription services
- Support for up to 10 simultaneous open patient records without losing unsaved work
- Rapid charting using conventional formats (superbill, medical history, review of systems)
- Customizable workflows per visit type
- Real-time MIPS/MACRA quality measure alerts before chart sign-off
- Integrated DICOM/PACS for medical imaging
- eLab and diagnostics center interfaces
- Plug-and-play camera device compatibility
- Direct messaging for secure clinical communication
- Custom specialty templates (25+ specialties, though the specialty pages themselves are thin — mostly restate general features and invite demos)

**2. Practice Management**
Source: nexusclinical.com/practice-management/
- Scheduling with configurable appointment types
- Automated appointment reminders (email/text)
- Patient recalls and follow-up scheduling
- Task management
- Real-time insurance eligibility checks and payment collection at check-in
- Digital patient intake (contact info, medical history, allergies, visit reasons, consent)
- Document scanning, importing, and organizing with custom classification
- Inventory management — track in-house medications and supplies; prescribe and bill directly from inventory
- Integrated eFax for sending and importing documents
- Operations dashboard

**3. Medical Billing**
Source: nexusclinical.com/medical-billing/
- Integrated with EHR clinical documentation (seamless charge capture)
- Configurable superbill, fee schedules, and claim workflows
- Real-time eligibility verification
- Claims submission and management
- Revenue cycle management
- Error minimization in billing processes
- Timely filing adherence to prevent claim denials
- Coordinated workflow between front desk, clinicians, and billing staff
- The billing consultant on the leadership team (Jennifer Somers, dual AAPC-certified) suggests billing is a core competency

**4. Patient Engagement / Patient Portal**
Source: nexusclinical.com/patient-engagement/
- 24/7 patient access to health information
- Review visit summaries and medical documentation
- View and download medical records
- View account statements
- Update demographics, medical history, and allergies
- Complete intake forms and custom health questionnaires
- Request appointments online
- Join telemedicine/eVisit sessions
- Pay balances through secure online payments (Stripe, Clover integration)
- Receive automated appointment reminders
- Complete post-visit experience surveys
- Secure messaging with providers
- Online patient registration for new patients
- Practice-controlled screening of patient-submitted data before acceptance
- Note: Third-party reviews cite the patient portal as difficult for patients to understand/use

**5. Telehealth**
Source: nexusclinical.com/telehealth/
- Powered by Google Meet
- Cross-platform: iOS, Android, desktop
- Patients join via link in text or email
- Providers can chart simultaneously during video visit
- Integrated with scheduling workflow
- Automated email/text reminders before visits
- HIPAA-compliant

**6. E-Prescribing**
Via NewCrop integration:
- Electronic prescribing
- EPCS (Electronic Prescribing for Controlled Substances) with MFA
- PDMP (Prescription Drug Monitoring Program) integration
- SureScripts drug history
- Formulary checking
- Drug-drug and drug-allergy interaction checks

**Interoperability:**
Source: nexusclinical.com blog on interoperability, mandatory disclosures
- FHIR APIs (certified g(10))
- HL7 integration with third-party practice management systems
- C-CDA document exchange for transitions of care
- Custom APIs offered for real-time data exchange
- Public health reporting: immunization registries, syndromic surveillance, electronic case reporting
- Payment processor integration (Stripe, Clover)

### Data & Content

Based on vendor feature descriptions, certified criteria, and user reviews, Nexus EHR stores the following categories of data:

**Patient demographics:** Name, DOB, sex, race, ethnicity, preferred language, address, phone, email, insurance information (source: a(5) certification, patient intake features)

**Clinical records:**
- Chief complaint and history of present illness
- Medical history (past medical, surgical, family, social) — family health history certified under (a)(12)
- Review of systems
- Physical examination findings
- Assessment and plan / clinical notes
- Problem lists
- Medication lists (active and historical)
- Allergy lists
- Immunization records
- Vital signs
- Lab results (via eLab interfaces)
- Diagnostic imaging (DICOM/PACS integrated — source: nexusclinical.com/nexus-ehr/)
- Implantable device list (certified under (a)(14))

**Orders:**
- Medication orders (CPOE certified under (a)(1))
- Laboratory orders (CPOE certified under (a)(2))
- Diagnostic imaging orders (CPOE certified under (a)(3))
- Prescriptions including controlled substances (eRx/EPCS via NewCrop)

**Documents:**
- Clinical notes and visit summaries
- Scanned/uploaded documents (source: practice management page)
- eFax sent and received (source: practice management page)
- Consent forms
- Patient intake forms
- Letters and custom form templates with auto-fill
- Patient education materials (via MedlinePlus Connect)

**Financial/Administrative:**
- Superbill/encounter charges
- Claims data
- Fee schedules
- Insurance eligibility verification records
- Payment records
- Account statements
- Appointment schedules and history
- Inventory records (in-house medications and supplies)

**Quality and Compliance:**
- Clinical quality measure data (20 CQMs)
- MIPS/MACRA quality reporting data
- Audit logs (certified under (d)(2)-(d)(3))
- Public health reporting data (immunizations, syndromic surveillance, case reports)

**Patient-Generated Data:**
- Portal-submitted demographics updates
- Health questionnaire responses
- Appointment requests
- Secure messages between patients and providers
- Post-visit experience surveys
- Online payment transactions

**Communication:**
- Direct messages (clinical)
- Secure portal messages (patient-provider)
- eFax records
- Appointment reminders (email/text logs)

**What's unclear or absent from vendor materials:**
- Whether the product stores referral tracking data (not explicitly mentioned)
- Depth of inventory management data (medications and supplies tracking is mentioned but details are sparse)
- Whether there is a standalone reporting/analytics module beyond CQM dashboards
- No mention of care plan management as a distinct feature
- No mention of patient consent management beyond intake forms
