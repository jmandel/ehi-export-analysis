# NextGen Healthcare — Product Research

Researched: 2026-02-16
Developer website: https://nextgen.com

## Overview

NextGen Healthcare is a long-established health IT company founded in 1974 as Quality Systems, Inc. (QSI), originally a computer consulting and dental practice management firm. QSI entered the ambulatory EHR/PM market through acquisitions in the late 1990s (Clinitec for EMR, Micromed for PM) and combined them into "NextGen Healthcare Information Systems" in 2001. The company unified under the NextGen Healthcare brand in 2018. It was publicly traded on NYSE (QSII) until 2023, when it was acquired by private equity firm Thoma Bravo and taken private. In 2025, Madison Dearborn Partners joined as a significant co-owner.

NextGen Healthcare serves the ambulatory market — physician practices, multi-specialty groups, FQHCs, and specialty clinics — with two main product lines: **NextGen Enterprise** (for larger practices with 10+ providers) and **NextGen Office** (for small practices with fewer than 10 providers). The company reports serving more than 124,000 providers across the United States and approximately 2,900 employees. They have been ranked #1 in Practice Management by Black Book Research multiple years running. Key strategic acquisitions include HealthFusion/MediTouch (2016, cloud EHR for small practices), Mirth (2013, interoperability/integration engine), Topaz (2019, behavioral health), Medfusion (2019, patient experience), and OTTO Health (2019, telehealth).

## Product: NextGen Office

CHPL IDs: 9372

### What It Is

NextGen Office is a cloud-based, fully integrated EHR and practice management platform designed for small medical practices (1-10 providers). It originated as **MediTouch EHR**, created in 1998 by two family medicine physicians in California under the company HealthFusion. NextGen Healthcare (then QSI) acquired HealthFusion for $165M in 2016 specifically to gain a cloud-based EHR platform, and rebranded MediTouch as "NextGen Office" during the 2018 brand unification. The CHPL product number (15.04.04.2054.**Medi**.05.00.1.180220) still reflects the MediTouch origins.

NextGen Office is an all-in-one solution combining EHR, practice management, billing, patient portal, and revenue cycle management in a single cloud-based platform. It is ONC 2015 Edition Cures certified and NCQA PCMH 2017 prevalidated. The certified module targets "Clinicians holding the MD, DO, NP, or PA credential" per the SED intended user description. The certification is broad — covering clinical data ((a)(1)-(a)(5), (a)(12), (a)(14)), transitions of care ((b)(1)-(b)(3)), EHI export ((b)(10)-(b)(11)), patient portal ((e)(1)/(e)(3)), public health reporting ((f)(1)/(f)(5)), FHIR APIs ((g)(7)/(g)(9)/(g)(10)), clinical quality measures ((c)(1)-(c)(4)), and Direct messaging ((h)(1)).

### Users & Market

NextGen Office targets small ambulatory practices — solo practitioners and groups with fewer than 10 providers. It serves 40+ specialty markets with specialty-specific clinical content and templates, including primary care, family practice, behavioral health, cardiology, dermatology, orthopedics, pediatrics, ophthalmology, urology, neurology, gastroenterology, general surgery, geriatric medicine, pain management, pulmonology, rheumatology, physical therapy, urgent care, and dental health.

End users include physicians (MDs, DOs), nurse practitioners, physician assistants, front-desk/registration staff, billing staff, and practice managers. Patients interact with the system through the patient portal. NextGen Healthcare overall serves more than 124,000 providers; the breakdown between Office and Enterprise is not publicly disclosed, but Office specifically targets the small-practice segment.

### Modules & Functionality

Based on vendor materials and review sites, NextGen Office includes the following integrated modules and capabilities:

**Electronic Health Records (EHR)**
- Cloud-based clinical documentation accessible via laptop, iPad, or tablet
- Specialty-specific clinical "blueprints" (templates) for 40+ specialties
- Multiple input methods: "Talk, Type & Touch" for documentation
- AI-powered Ambient Assist: converts patient-provider conversations into structured SOAP notes automatically (reportedly saves 1.5-2 hours per day, notes generated within 30 seconds)
- E-prescribing with Surescripts integration (including controlled substances based on certification criteria (a)(14))
- Connections to major lab networks for ordering and results
- Immunization registry interfaces with forecasting capabilities — system sends administered immunization data to registries and supports updates
- Clinical decision support
- Problem lists, medication lists, allergy lists, vital signs documentation
- CPOE (computerized provider order entry) for medications, labs, and imaging

**Practice Management (PM)**
- Appointment scheduling with online booking, reminders (text/email), digital waitlists, and confirmation
- Patient registration and demographics management
- Real-time insurance eligibility verification
- Room status dashboard for workflow management
- Referral management

**Billing & Revenue Cycle Management**
- Integrated billing with electronic claims submission through clearinghouse (Office Ally)
- EDI (electronic data interchange) for claims processing
- Charge Review Rules Engine / AI Rules Engine for claim accuracy before submission
- Coding support (CPT, ICD-10)
- Collections and accounts receivable management
- Denial prevention and claims acceleration
- Electronic statements with online bill pay
- Revenue cycle management services (expert billing services available as add-on)

**Patient Engagement / Patient Portal (NextGen PxP Portal)**
- Patient self-scheduling and appointment management
- Digital intake forms with discrete data integration
- Secure messaging between patients and practice
- Access to medical records
- Medication refill requests
- Online bill payment
- Telehealth/virtual visit capabilities
- Automated messaging and patient surveys

**Reporting & Analytics**
- MACRA/MIPS quality measure reporting and consulting
- Practice-wide financial analytics
- Business intelligence dashboards
- Real-time operational reporting

**Public Health Reporting**
- Immunization registry submission (certified (f)(1))
- Electronic case reporting capabilities (certified (f)(5))

**Interoperability**
- Direct messaging for transitions of care (certified (h)(1))
- C-CDA document exchange (certified (b)(1)-(b)(3))
- FHIR R4 API access (certified (g)(10))
- Integration with Mirth (NextGen's interoperability engine)

**Care Management**
- Chronic care management support
- Care plan management tools
- Remote patient monitoring capabilities

### Data & Content

Based on the modules and features described above, NextGen Office manages the following categories of data:

**Clinical Data**: Patient demographics, clinical notes (including AI-generated SOAP notes), problem lists, medication lists, allergy/intolerance records, vital signs, immunization records (with registry submissions), lab orders and results, diagnostic imaging orders, clinical impressions, family history, care plans, goals, procedures, diagnoses (ICD-10), and clinical decision support alerts.

**Medications & Prescribing**: Prescription records (including controlled substances via EPCS), medication history, e-prescribing transactions via Surescripts, medication refill requests from patients.

**Documents & Communications**: Clinical documents (C-CDAs), patient portal messages, secure messaging, e-fax documents, uploaded documents from digital intake, telehealth/virtual visit records, patient surveys.

**Scheduling & Administrative**: Appointment schedules, booking history, waitlists, appointment reminders, room status, patient registration data, insurance eligibility verification records, referral records.

**Financial & Billing**: Insurance/coverage information, claims data (EDI 837), remittance data, charge records (CPT codes), payment records, accounts receivable, collections data, electronic statements, patient payment transactions, denial and rejection records.

**Quality & Reporting**: MIPS/MACRA quality measure data, clinical quality measure calculations, public health reporting submissions (immunization registries, electronic case reporting).

**Audit & Security**: Audit logs (implied by (d) criteria certification), MFA authentication records, user access logs.

The mandatory disclosures page notes that the patient portal and lab/immunization registry interfaces require separate licensing fees, suggesting these are optional add-on modules, though they are part of the certified product capability. Claims processing goes through Office Ally's clearinghouse for EDI.

---

*Note: NextGen Office is distinct from NextGen Enterprise, which targets larger practices (10+ providers) and has a different technology architecture. This research covers only NextGen Office (CHPL 9372). The two products share the NextGen Healthcare brand but are separate platforms with separate CHPL certifications.*
