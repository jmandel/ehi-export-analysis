# 1Life Healthcare, Inc — Product Research

Researched: 2026-02-16
Developer website: https://www.onemedical.com/

## Overview

1Life Healthcare, Inc is the legal entity behind **One Medical**, a membership-based, technology-enabled primary care practice acquired by Amazon in February 2023 for $3.9 billion. Founded by physician Tom Lee in San Francisco in 2007, One Medical operates as a direct-to-consumer and B2B primary care service across 19+ major U.S. cities with over 125 offices. The company also acquired Iora Health in September 2021, adding 47 offices serving Medicare patients.

One Medical's business model combines an annual membership fee ($99/year for Amazon Prime members; higher for non-Prime) with standard insurance billing for clinical visits. They partner with over 8,500 companies to offer One Medical as an employee health benefit. The practice employs board-certified physicians, nurse practitioners, and physician assistants specializing in family medicine and internal medicine. One Medical reports a 90+ Net Promoter Score, with 45% of members using digital services monthly.

Crucially, One Medical built its own proprietary EHR platform called **1Life** from the ground up — they do not use a third-party EHR like Epic or athenahealth. This makes the certified "1Life" product both the EHR and essentially the entire technology backbone of the One Medical clinical operation.

## Product: 1Life

CHPL IDs: 10964

### What It Is

1Life is One Medical's proprietary, purpose-built health IT platform. It is not a standalone EHR sold to third parties — it is the internal technology system that powers all of One Medical's clinical, administrative, and patient-facing operations. The certified module "1Life" is the EHR component, but the broader 1Life ecosystem encompasses the entire technology stack for running One Medical's primary care practice.

The platform was built on AWS from the company's founding in 2007, using a modern tech stack including Rails, React, GraphQL, and OpenSearch/ElasticSearch. It supports FHIR for interoperability and incorporates machine learning for workflow optimization. SureScripts is listed as relied-upon software in the ONC certification, indicating electronic prescribing integration.

Certified criteria include clinical documentation (a)(1), demographics (a)(5), family health history (a)(12), implantable device list (a)(14), transitions of care (b)(1), patient health information request (e)(3), and FHIR-based API access (g)(10). Notably absent from certification: CPOE criteria (a)(2)/(a)(3), clinical decision support (a)(9), and public health reporting (f) criteria. The intended users are described as "ambulatory physicians and nurses."

### Users & Market

One Medical is a direct provider of primary care — the end users of 1Life are:
- **Clinicians**: Physicians, nurse practitioners, and physician assistants who chart, order labs, prescribe medications, and document visits
- **Care team members**: Nurses, care navigators, and health coaches who manage chronic care programs, handle tasks, and coordinate referrals
- **Administrative staff**: Handle scheduling, insurance, billing, and referral logistics
- **Patients/Members**: Access the patient-facing portal and mobile apps (iOS/Android) for scheduling, messaging, prescription renewals, lab results, and virtual visits

The clinical setting is exclusively ambulatory primary care — no hospitals, no specialty practices, no surgical centers. One Medical operates its own clinics with employed providers rather than licensing the software to external practices. The company has over 125 offices across cities including San Francisco, New York, Seattle, Los Angeles, Chicago, Boston, Atlanta, and others.

Notable partnerships include collaborations with Cleveland Clinic (October 2024) and Montefiore Health System to coordinate primary and specialty care. Amazon has also been integrating AI features, including a Health AI assistant launched in early 2025 that can connect members to providers, review lab results, and manage medications.

### Modules & Functionality

Based on vendor materials, the AWS case study, and the One Medical technology blog, the 1Life ecosystem includes the following integrated components:

**EHR & Clinical Charting**
- Clinical documentation system designed collaboratively with clinicians
- Patient records accessible across all One Medical offices and virtual visits
- Unified patient profiles with "all relevant information about each patient"
- Support for note-writing, medication prescribing, test ordering, and outside record review
- Family health history tracking (certified (a)(12))
- Implantable device list management (certified (a)(14))

**Scheduling Platform**
- Online appointment booking, rescheduling, and cancellation
- Same-day and next-day appointment availability
- Support for both in-person office visits and virtual video visits
- Walk-in lab appointment management

**Messaging & Communication**
- Secure patient-to-provider messaging through the app/portal
- Provider-to-provider internal communication
- Internal tasking system for care team coordination
- Administrative messaging for billing, insurance, and referral questions
- Response times typically 24-72 hours for patient messages

**Virtual Care / Telehealth**
- 24/7 video chat for urgent concerns ("Treat-Me-Now" on-demand visits)
- Scheduled video visits with providers
- Photo sharing capability for clinical assessment (e.g., rashes)

**Patient Portal & Mobile Apps**
- Web portal (app.onemedical.com) and native iOS/Android apps
- View lab results, request prescription renewals, manage appointments
- Health reminders and screening follow-ups
- Digital health records access

**Prescriptions & E-Prescribing**
- Electronic prescribing via SureScripts integration (listed as relied-upon software)
- Prescription renewal requests through app/portal
- Pharmacy selection and management

**Lab Services**
- On-site walk-in laboratory testing at One Medical offices
- Lab order management and results delivery (typically 7-10 business days)
- Provider interpretation of results

**Referral & Care Coordination**
- Specialist referral requests through the portal
- Coordination with hospitals and specialty practices
- Care coordination across One Medical's office network

**Chronic Care Management (Impact by One Medical)**
- Team-based chronic condition management program
- Personalized care plans with 1:1 coaching and group classes
- Care navigators and health coaches
- Integration with specialist coordination at health system partners

**Administrative & Billing**
- Insurance verification and billing (accepts most major carriers and Medicare)
- Membership management
- Administrative support through messaging

**Transitions of Care**
- C-CDA document generation and consumption (certified (b)(1))
- Health information exchange capabilities

**API & Interoperability**
- FHIR R4 API for patient and population access (certified (g)(10))
- FHIR-based data exchange supporting standard resource types

### Data & Content

Based on the features described above and the certification criteria, 1Life stores and manages:

**Clinical Data** (evidenced by certified criteria and feature descriptions):
- Patient demographics (a)(5)
- Clinical encounter/visit notes (charting system described in blog and AWS case study)
- Problem lists / conditions (a)(1) — CPOE for medications
- Medication lists and prescription history (SureScripts integration, prescription renewal features)
- Allergy lists (certified (a)(1))
- Family health history (certified (a)(12))
- Implantable device lists (certified (a)(14))
- Lab orders and results (on-site lab services, results in patient portal)
- Vital signs and observations (clinical documentation)
- Immunization records (described in FAQ — vaccinations including travel medicine)
- Assessment and plan documentation

**Communication Data** (evidenced by messaging features):
- Patient-provider secure messages (described in technology page and FAQ)
- Provider-to-provider internal messages and tasks (described in technology blog)
- Administrative messages about billing, insurance, referrals

**Care Coordination Data** (evidenced by referral and chronic care features):
- Specialist referral records
- Care plans for chronic condition management
- Care team assignments and navigator notes
- Transitions of care documents (C-CDA, certified (b)(1))

**Administrative & Scheduling Data** (evidenced by platform features):
- Appointment history (scheduling, cancellations, virtual vs. in-person)
- Insurance and billing information
- Membership data
- Patient consent and preferences

**Virtual Care Data** (evidenced by telehealth features):
- Video visit records
- On-demand "Treat-Me-Now" visit records
- Photo attachments shared during virtual visits

**Patient-Generated Data** (evidenced by portal features):
- Prescription renewal requests
- Referral requests submitted through portal
- Health screening questionnaire responses

**What's unclear or not described:**
- The vendor website does not detail separate billing/claims data architecture — billing is mentioned in the FAQ but the depth of claims processing (e.g., claim scrubbing, ERA/EOB management) is unclear. One Medical bills insurance directly, so claims data exists, but whether it's stored within 1Life or a separate billing system is not specified.
- Imaging/radiology: The website does not mention diagnostic imaging services or PACS integration. As a primary care practice, they may not store imaging data beyond external records received.
- Detailed audit logs and system administration data are implied by security certifications (d)(1)-(d)(9) but not described in user-facing materials.
- The Iora Health acquisition (Medicare-focused practices) may use different technology — it's unclear whether Iora practices have been migrated to 1Life or operate on a separate system.

---
