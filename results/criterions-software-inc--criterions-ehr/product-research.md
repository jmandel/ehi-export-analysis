# Criterions Software Inc — Product Research

Researched: 2026-02-14
Developer website: https://criterions.com/

## Overview

Criterions Software Inc is a small, privately held healthcare IT company headquartered in Garden City, NY (some sources cite Great Neck, NY). The company has been in business for over 30 years and has approximately 7–12 employees depending on the source. They develop an integrated cloud-based EHR and practice management suite marketed to independent medical practices, multi-provider clinics, and medical billing services of all sizes. Their target market is ambulatory practices across a very wide range of specialties — their website lists nearly 50 supported specialties, from family medicine and internal medicine to surgical subspecialties, behavioral health, dentistry, ophthalmology, and more.

Criterions is a small niche vendor without a large public market presence. They do not appear to have significant venture funding or private equity backing. The company appears to be a modest, long-standing player in the ambulatory EHR/PM space, focused on direct relationships with independent practices and billing companies.

## Product: Criterions EHR (part of Criterions Medical Suite / TCMS)

CHPL ID: 10171

### What It Is

Criterions EHR is a cloud-based, ONC-certified electronic health records system that is part of a broader integrated suite called "The Criterions Medical Suite" (TCMS). The certified product is listed as "Criterions EHR 4.0 Complete EHR Ambulatory." It is broadly certified across clinical documentation (a)(1)–(a)(5), (a)(12), (a)(14)–(a)(15), transitions of care (b)(1)–(b)(3), patient portal (e)(1), clinical quality measures (c)(1)–(c)(3), public health reporting (f)(1), (f)(5), and FHIR API access (g)(10). The certification is for "All Ambulatory Practices."

The certified EHR module is part of a larger integrated product suite that includes practice management/billing, patient portal, e-prescribing, scheduling, lab interfaces, and document management. These are marketed as an integrated platform rather than standalone products.

### Users & Market

The product is designed for independent and growing medical practices, from single-provider offices to multi-location clinics, as well as medical billing services. Criterions supports an unusually wide range of specialties — nearly 50 are listed on their website including allergy, anesthesiology, bariatric surgery, behavioral health, cardiology, chiropractic, dentistry, dermatology, emergency medicine, endocrinology, ENT, family medicine, gastroenterology, general surgery, geriatrics, hematology/oncology, hospitalist, infectious disease, internal medicine, long-term care, mental health, multi-specialty, nephrology, neurology, neurosurgery, OB-GYN, occupational medicine, oncology, ophthalmology, optometry, orthopedics, pain management, pathology, pediatrics, physical therapy, plastic surgery, podiatry, psychiatry, psychology, pulmonology, radiology, rheumatology, sleep medicine, surgery, SurgiCenter, urgent care, urology, and vascular surgery.

Given the company's small size (7–12 employees), the customer base is likely modest. No specific customer counts or notable deployments were found in public materials. The login portal at portal.nymed.com suggests at least some New York-area medical practices as customers. Third-party reviews on Capterra indicate a small number of reviews with generally positive sentiment, noting the vendor's responsiveness and willingness to customize.

### Modules & Functionality

Based on the vendor's website and feature pages, the Criterions Medical Suite includes the following integrated modules:

**Electronic Health Records (EHR)**
- Customizable charting tools with specialty-specific templates
- Patient vitals tracking
- Clinical documentation for encounters
- Problem lists, medication lists, allergy lists (implied by (a)(1)–(a)(5) certification)
- Clinical decision support (certified for (a)(2), (a)(4))
- Implantable device tracking (certified for (a)(14))
- Social, psychological, and behavioral data (certified for (a)(15))

**E-Prescribing**
- Integrated e-prescribing including controlled substances (EPCS)
- Prescription history access
- Drug interaction monitoring
- Controlled substance tracking
- Prescription fulfillment and refill request tracking
- Integrated with Surescripts network (SureScripts certificate displayed on disclosures page)
- NewCrop integration mentioned in the mandatory disclosures page

**Practice Management / Billing**
- Insurance verification and eligibility checking
- Electronic superbill generation and transmission
- Claims submission and clean claim processing
- Denial tracking
- Accounts receivable (A/R) management
- Payment posting (automated and manual)
- Patient payment plans and online payment processing
- Daily transaction reports, multi-practice reports, PQRS reports
- Revenue cycle management
- Claredi 5010 certified (for electronic claims)

**Scheduling**
- Drag-and-drop appointment calendars
- Recurring appointment tools
- Task queues
- Automated appointment reminders (email and text)
- Real-time analytics on scheduling

**Patient Portal**
- 24/7 patient access to health information
- Online appointment scheduling and check-in
- Electronic patient intake forms (demographics, insurance, medical history, social history, family history, medications, allergies, pharmacy preferences, consent forms, medical questionnaires)
- Prescription refill requests
- Secure HIPAA-compliant messaging between patients and practice
- Message routing to appropriate staff based on message type
- Online bill viewing and payment (credit card)
- Document and ID upload

**Lab Interfaces**
- Electronic lab ordering
- Automatic receipt and filing of lab results
- Results filed to ordering provider's queue
- LOINC-coded results with automatic MIPS measure calculation
- Connections to labs, imaging groups, and public health organizations (specific partners not listed publicly)

**Document Management**
- Folder creation and organization
- Document annotations
- Digital signature locking
- Patient documentation storage

**Reporting & Analytics**
- Financial reports and analytics
- Practice performance dashboards
- Patient outcome reporting
- Clinical quality measures (CQM) support (certified for (c)(1)–(c)(3))
- MIPS/quality reporting

**Transitions of Care**
- C-CDA generation and transmission (certified for (b)(1)–(b)(3))
- Integration with EMRDirect (mentioned on mandatory disclosures page) for Direct messaging

**Public Health Reporting**
- Immunization registry reporting (certified for (f)(1))
- Cancer case reporting (certified for (f)(5))

**Administrative Features**
- Role-based access controls
- Audit logging of record access and modifications
- Recall procedures for follow-up visit reminders
- User access controls limiting record visibility
- Referral management

### Data & Content

Based on the features described above, the Criterions Medical Suite stores and manages the following categories of data:

**Clinical Data**: Patient demographics, encounter notes/clinical documentation, vital signs, problem lists, medication lists, allergy lists, immunization records, lab orders and results (LOINC-coded), social history, family history, past medical history, implantable device records, clinical decision support alerts/interactions, referral information, and C-CDA documents.

**Prescription Data**: Active and historical prescriptions, controlled substance prescriptions, drug interaction alerts, prescription fulfillment tracking, refill requests, and pharmacy information — all flowing through the Surescripts/NewCrop integration.

**Billing/Financial Data**: Insurance information (plans, eligibility verification results), superbills, claims, denial records, accounts receivable, payment history, patient payment plans, patient ledger entries, transaction records, and financial reports.

**Scheduling Data**: Appointment calendars, appointment history, recurring appointment patterns, reminder records, and no-show tracking.

**Patient Portal Data**: Patient-submitted intake forms (demographics, insurance, medical questionnaires, consent forms), secure messages between patients and practice staff, online payment records, uploaded documents and IDs.

**Administrative Data**: User accounts and roles, audit logs (who accessed/modified what records), document management records (with annotations and digital signatures), recall/follow-up reminders.

**Reporting Data**: Clinical quality measure calculations, MIPS measure data, practice performance analytics, financial analytics.

**Public Health Data**: Immunization registry submissions, cancer case reports.

The vendor website does not specifically mention imaging/PACS storage, fax management, or integrated telehealth — though these may exist as features not prominently marketed. The website also doesn't detail how historical data is retained or archived.
