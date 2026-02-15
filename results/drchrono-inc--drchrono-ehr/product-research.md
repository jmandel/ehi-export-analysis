# drchrono Inc. — Product Research

Researched: 2026-02-14
Developer website: https://www.drchrono.com

## Overview

drchrono is a cloud-based, all-in-one EHR and practice management platform targeting ambulatory care physicians, primarily at small to mid-sized independent practices. Founded in 2009 in New York City by Daniel Kivatinos and Michael Nusimow, the company went through Y Combinator and was an early mover in mobile-first EHR design — it released the first tablet-certified EHR system in 2011 and is the only official Apple Mobility Partner in healthcare. The company is headquartered in Sunnyvale, California.

In November 2021, drchrono was acquired by EverCommerce (Nasdaq: EVCM) for approximately $180 million. It now operates as "drchrono by EverHealth" within EverCommerce's EverHealth solutions division, which positions it as the center of an integrated ecosystem for independent healthcare practices.

drchrono serves tens of thousands of physicians and over 17 million patients. At the time of acquisition, the company reported 4,600+ independent practices and 13,000+ providers. The platform has facilitated over $11 billion in medical billings and 69 million+ appointments. It holds approximately 0.3% market share in the EHR space, placing it well behind major players like Cerner, McKesson, and athenahealth, but firmly in the tier of established cloud-based ambulatory EHR vendors.

## Product: drchrono EHR

CHPL ID: 10910 (15.99.04.2897.DRCH.11.03.1.220531)

### What It Is

drchrono EHR is a single, integrated cloud-based platform combining electronic health records, practice management, medical billing, revenue cycle management, a patient portal (OnPatient), and telehealth. The certified module — "drchrono EHR v11.0" — appears to be the entire product platform, not a sub-component. It is certified across 35+ ONC criteria spanning clinical data ((a)(1)-(a)(5), (a)(12), (a)(14)), care coordination ((b)(1)-(b)(3)), patient portal ((e)(1), (e)(3)), public health reporting ((f)(1), (f)(2), (f)(5)), and API/FHIR access ((g)(7), (g)(10)), indicating a full-featured EHR with broad clinical, administrative, and interoperability capabilities.

The product is cloud-hosted (SaaS) with native iOS apps for iPhone and iPad, plus a web interface. There is no on-premise option. The SED intended user description is "Ambulatory care physicians."

### Users & Market

**Who uses it:** Ambulatory care physicians, clinical staff, billing staff, practice managers, and patients (via the OnPatient portal). The product targets independent practices across all sizes — from solo practitioners to multi-site groups with 50+ physicians.

**What settings:** The product supports 20+ medical specialties including family medicine, internal medicine, psychiatry, OB/GYN, orthopedics, plastic surgery, chiropractic, and others. It is firmly an ambulatory/outpatient system — no hospital or inpatient capabilities were described.

**Customer profile:** 63% of customers are small organizations (<50 employees), 25% mid-size, and 9% large (1000+ employees). The largest industry segments are Hospital & Health Care (31%), Medical Practice (17%), and Health, Wellness & Fitness (10%). Users praise the mobile-first design and customization, though reviews note challenges with claims management and navigation.

**Pricing:** Four tiers — Prometheus, Hippocrates, Apollo, and Apollo Plus — on a per-provider-per-month model. Apollo Plus includes managed billing/RCM services.

### Modules & Functionality

The platform is organized into several integrated modules, based on vendor marketing materials, the features page, and the API documentation:

**Clinical EHR / EMR:**
- Customizable clinical note templates tailored for 20+ specialties (vendor feature page)
- HIPAA-compliant speech-to-text/dictation with medical vocabulary (vendor feature page)
- Medical drawing tools for image annotation on clinical notes (vendor feature page)
- Custom vitals tracking and baseline health data monitoring (features page)
- Problem lists, medication lists, allergy lists (API docs: /api/problems, /api/medications, /api/allergies)
- Procedure documentation (API: /api/procedures)
- Amendments/corrections to clinical notes (API: /api/amendments)
- Implantable device tracking (API: /api/implantable_devices)
- Care plans and patient interventions (API: /api/care_plans, /api/patient_interventions)
- Patient risk assessments and physical exams (API: /api/patient_risk_assessments, /api/patient_physical_exams)
- Clinical note field types and values for structured data capture (API: /api/clinical_note_field_types, /api/clinical_note_field_values)
- Yellow notepad (quick notes) (API: /api/yellow_notepad)

**Electronic Prescribing:**
- eRx and EPCS (Electronic Prescribing for Controlled Substances) (vendor site, certified criteria (b)(3))
- Electronic prior authorization (vendor feature page)
- Prescription messaging (API: /api/prescription_messages)
- Pharmacy note communications (API: /api/medications/:id/append_to_pharmacy_note)

**Lab & Imaging Integration:**
- Lab ordering and results viewing within the EHR (vendor feature page)
- Lab orders, lab documents, lab tests, lab results, sublabs/vendors (API: /api/lab_orders, /api/lab_documents, /api/lab_tests, /api/lab_results, /api/sublabs)
- Lab orders summary for aggregated data (API: /api/lab_orders_summary)

**Scheduling & Practice Management:**
- Appointment scheduling with customizable profiles and time blocks (vendor feature page)
- Appointment templates for doctor availability (API: /api/appointment_templates)
- Custom appointment fields (API: /api/custom_appointment_fields)
- Patient self-scheduling via embeddable website widget (vendor feature page)
- Automated appointment reminders via text, email, and phone (vendor feature page, API: /api/reminder_profiles)
- Patient check-in kiosk mode (vendor feature page)
- Office/location management with exam room configuration (API: /api/offices, /api/offices/:id/add_exam_room)
- Task management system with categories, notes, statuses, and templates (API: /api/tasks, /api/task_categories, /api/task_notes, /api/task_statuses, /api/task_templates)
- Practice group chat for staff communication (vendor feature page)
- Patient flags for identifying pertinent information (API: /api/patient_flag_types)

**Billing & Revenue Cycle Management:**
- Auto-generated HCFA 1500 claim forms (vendor feature page)
- Custom billing codes and profiles (API: /api/billing_profiles)
- Fee schedules (API: /api/fee_schedules)
- Electronic claims submission via eProvider Solutions (vendor feature page)
- Insurance eligibility verification (API: /api/eligibility_checks)
- Insurance carrier and plan management (API: /api/insurances, /api/custom_insurance_plan_names)
- Electronic Remittance Advice (ERA) access (vendor feature page)
- Claim status tracking dashboard (vendor feature page)
- Line items / billable service entries (API: /api/line_items)
- Financial transactions (API: /api/transactions)
- Patient payments and payment logs (API: /api/patient_payments, /api/patient_payment_log)
- Patient billing statements and payment plans (vendor feature page)
- Recurring payment setup (vendor feature page)
- Denial analysis and resolution (vendor feature page)
- Medical coding services (Apollo Plus tier, vendor feature page)

**Patient Portal (OnPatient):**
- Patient access to their health records (vendor site, support articles)
- Secure HIPAA-compliant messaging between patients and providers (vendor site)
- Online intake forms and consent forms (API: /api/consent_forms, vendor site)
- Appointment scheduling through the portal (vendor site)
- Payment processing from the portal (vendor site)
- Clinical summaries with medications, allergies, and lab results (support article)
- Automated patient education materials linked to problems, allergies, medications, and labs (support article)
- Video visits / telehealth from iOS devices (vendor site)

**Telehealth:**
- HIPAA-compliant video visits integrated within the EHR (vendor feature page)
- No additional software or downloads required for patients (vendor feature page)

**Document Management & Communications:**
- Integrated eFax with HIPAA-compliant inbox and audit trail (support articles)
- Faxing of uploaded documents, signed consent forms, outbound referrals, lab results, and amendments (support article)
- Patient referrals with attached clinical notes, documents, and imagery (vendor blog, support)
- Internal messaging system (API: /api/messages)
- Patient messaging/communications (API: /api/patient_messages, /api/patient_communications)
- Communication logs (API: /api/comm_logs)
- Custom demographics fields (API: /api/custom_demographics)

**Immunizations & Preventive Care:**
- Vaccine inventory tracking (API: /api/inventory_vaccines, /api/inventory_categories)
- Patient vaccine/immunization records (API: /api/patient_vaccine_records)
- Immunization registry integration (certified for (f)(1) immunization registry reporting)

**Public Health Reporting:**
- Certified for immunization registry reporting (f)(1)
- Certified for syndromic surveillance reporting (f)(2)
- Certified for cancer case reporting (f)(5)

**Interoperability & APIs:**
- C-CDA document generation and exchange (API: /api/patients/:id/ccda, certified (b)(1), (b)(2))
- FHIR R4 API (certified (g)(10))
- Open REST API (v4) with 27+ endpoint groups for third-party integration
- OAuth 2.0 authentication
- Bulk data export endpoints
- Direct messaging for care transitions (certified (h)(1))

**User & Access Management:**
- Doctor/provider accounts (API: /api/doctors)
- Staff user accounts (API: /api/users)
- User groups/permission management (API: /api/user_groups)
- Patient portal access control (API: /api/patients/:id/onpatient_access)

### Data & Content

Based on the API documentation (which is the most concrete evidence of what data the system stores), drchrono EHR manages:

- **Patient demographics** including custom demographic fields
- **Clinical notes** with structured field types and values, plus templates
- **Problems/diagnoses**, **medications**, **allergies** — the core clinical lists
- **Procedures** performed
- **Lab orders, results, documents**, and laboratory vendor information
- **Immunization/vaccine records** and vaccine inventory
- **Prescriptions** and pharmacy communications
- **Care plans**, **risk assessments**, **physical exams**, **interventions**
- **Implantable device** records
- **Amendments** to clinical records
- **Appointments** with profiles, templates, and custom fields
- **Billing data**: billing profiles, fee schedules, line items, transactions, patient payments, payment logs
- **Insurance information**: carriers, plan names, eligibility checks
- **Consent forms**
- **Messages**: internal (staff-to-staff), patient messages, prescription messages, communication logs
- **Documents**: faxed documents, uploaded documents, referral documents
- **Tasks** with categories, notes, statuses, and templates
- **Office/location** configurations including exam rooms
- **User/provider** accounts and permission groups
- **C-CDA documents** (clinical summaries for care transitions)
- **Patient portal access** records
- **Yellow notepad** (quick/sticky notes)
- **Patient flags** (alert categories)
- **Reminder profiles** (appointment reminder configurations)
- **Custom vitals** configurations

The vendor's feature page and reviews confirm the platform handles integrated billing with claims submission and denial management, which means it stores claims data, ERA/EOB data, and denial records. The API explicitly exposes line items, transactions, and payment logs.

The OnPatient patient portal stores patient-submitted intake forms, consent forms, secure messages, and payment information.

One area that is referenced but less clearly documented is **document management** — faxed documents and uploaded files are mentioned in support articles as faxable from the EHR, but the API doesn't have a clearly labeled "documents" endpoint for general uploaded files (though lab_documents, consent_forms, and amendments are present). The fax functionality appears built-in and would store fax records.
