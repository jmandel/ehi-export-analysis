# OpenEMR Foundation — Product Research

Researched: 2026-02-16
Developer website: https://www.open-emr.org/

## Overview

OpenEMR is the most popular open-source electronic health records (EHR) and medical practice management platform in the world. Originally released in 2001 as "MedicalPractice Professional (MP Pro)" by Synitech, it was reworked for HIPAA compliance and released as OpenEMR under the GNU GPL in August 2002. The project was maintained by various community developers over the years; the nonprofit OEMR organization was formed in 2010, followed by the OpenEMR Foundation in April 2019 to serve as the current steward of the project.

OpenEMR is used globally at an estimated 20,000+ healthcare facilities across 184 countries, serving over 90 million patients. In the US alone, there are an estimated 5,000+ installations serving 30+ million patients. Notable adopters include the U.S. Peace Corps (deployed across 77 countries via a five-year contract with EnSoftek) and the International Planned Parenthood Federation (IPPF). The software is primarily used by small to mid-size ambulatory practices, community health centers, and clinics, though it also serves hospitals in developing countries. It supports 34+ languages and runs on Windows, Linux, and macOS.

The product is free and open-source, with no licensing fees. Revenue in the ecosystem comes from professional support vendors, hosted cloud services, and optional paid add-on modules (telehealth, fax/SMS, claims clearinghouse). The OpenEMR Foundation is a nonprofit and the project is community-driven, with contributions from volunteers and commercial supporters. The software is built on PHP, Apache, and MySQL/MariaDB.

## Product: OpenEMR

CHPL IDs: 10938 (version 7.0, certified 2022-07-08), 11757 (version 8, certified 2026-01-30)

### What It Is

OpenEMR is a full-featured ambulatory EHR and practice management system. It is ONC-certified as a Complete Ambulatory EHR. The certified module *is* the whole product — there is no separate commercial product wrapping it. Both CHPL listings represent successive versions of the same platform (7.0 and 8), with identical certified criteria covering clinical documentation (a)(1-5, 12, 14), transitions of care (b)(1), CQMs (c)(1-3), security/privacy (d)(1-13), patient access (e)(3), FHIR APIs (g)(2-10), and direct messaging (h)(1).

The SED intended user description is "Ambulatory clinic providers and staff." One required paid third-party service exists for ONC compliance: the EMR Direct phimail service (~$300 setup, ~$150/year per provider) for Direct secure messaging.

### Users & Market

**Primary users**: Physicians, clinical staff, billing staff, and practice managers at ambulatory clinics. Patients access the system via the built-in patient portal.

**Clinical settings**: Predominantly small practices (1-10 staff), solo practitioners, community health centers, FQHCs, and small clinics. Also used in hospitals internationally, especially in developing countries. Some specialty use including ophthalmology/optometry (has dedicated eye care module), behavioral health (group therapy support), orthopedic, and dental practices (per user reviews).

**Market position**: OpenEMR occupies a unique niche as the leading open-source ambulatory EHR. It competes not on features parity with enterprise EHRs (Epic, Cerner) but on cost (free), flexibility (fully customizable source code), and data ownership (self-hosted option). On Capterra, it holds a 3.9/5 rating (21 reviews) with 4.4/5 for value for money. On SoftwareFinder, 4.2/5 (31 reviews) with 58% giving 5 stars.

**User feedback themes** (from Capterra and SoftwareFinder reviews):
- Pros: Free/low cost, full control over data, extensive customization, fast performance, reliable uptime, integrated billing makes it a complete practice management package
- Cons: Requires IT expertise to install and configure, steep learning curve, billing module needs enhancement for specialized practices, community support can be slow for urgent issues, complex codebase

### Modules & Functionality

Based on the vendor's feature pages, wiki documentation, and third-party descriptions, OpenEMR includes the following integrated modules:

**Clinical / EHR:**
- Patient demographics and registration
- Encounter management with SOAP notes
- Medical issues/problems list
- Medications tracking
- Allergies
- Immunizations records
- Vitals with growth charts
- Review of systems
- Lab orders, results, and integration (automated lab interface)
- Procedures tracking
- Referrals management
- Clinical decision rules / alerts
- DICOM medical image viewer
- Eye/Ophthalmology/Optometry specialty module (dedicated form tables: `form_eye_*`)
- Group therapy support
- Graphical charting
- Electronic syndrome surveillance

**Scheduling:**
- Appointment calendar with categories, colors, and type restrictions
- Repeating appointments
- Patient flow board, tracking, and reporting
- Find open appointment slots
- Patient appointment notifications (email/SMS)
- Recall/reminders board
- Multi-facility support

**Prescriptions & e-Prescribing:**
- Prescription creation and tracking
- Online drug search (RXNORM integration)
- e-Prescribing to pharmacies
- Print, fax, and email distribution
- Customizable prescription layouts (DEA, NPI, state license numbers)
- In-house pharmacy dispensary support

**Billing & Practice Management:**
- Flexible coding: CPT, HCPCS, ICD-9, ICD-10, SNOMED
- 5010 standards support
- Professional (CMS-1500) and institutional (UB-04) billing
- Electronic claim submission via clearinghouse integration
- Paper claims support
- Insurance eligibility queries
- Insurance tracking (multiple plans per patient)
- Accounts receivable interface
- EOB entry interface
- Automated 835/ERA (electronic remittance) posting
- Sales, collections, and insurance distribution reports

**Patient Portal (built-in):**
- Patient self-registration
- View demographics, conditions, medications, allergies, lab results
- Appointment scheduling and cancellation (with staff confirmation)
- Secure email-style messaging with clinic staff
- Secure real-time chat with clinic staff
- Online payments and account ledger viewing
- Document center: fill out forms (privacy agreements, consents, medical history)
- Submit documents for staff review
- Download CCR/CCD continuity of care records
- Download lab documents
- Electronic signature capability
- CCDA support

**Interoperability & Data Exchange:**
- CCDA import/export
- FHIR R4 API (US Core IG)
- SMART on FHIR support
- Direct secure messaging (via EMR Direct phimail)
- USCDI v5 support (as of late 2025 SVAP update)

**Forms & Documentation:**
- Layout-based forms (LBF) system for custom form creation
- CAMOS (Computer Aided Medical Ordering System)
- Nation Notes (WYSIWYG editor)
- Template-driven forms
- Electronic digital document management
- Voice recognition ready (Windows)

**Reporting:**
- Appointment, encounter, patient list reports
- Prescription and drug dispensing reports
- Referral and immunization reports
- Clinical Quality Measure (CQM) calculations (CMS22, CMS69, CMS122, CMS124, CMS125, CMS127, CMS130, CMS138, CMS147, CMS165)
- Automated Measure Calculations (AMC) and tracking
- Syndromic surveillance reports
- Procedure order statistics
- Insurance eligibility reports

**Internal Messaging:**
- Clinic messaging between staff
- Patient notes (pnotes) passed between users
- Dated reminders

**Optional Paid Add-on Modules:**
- Telehealth (Comlink video conferencing, ~$16/month)
- Fax and SMS (via etherFAX/RingCentral for fax, Twilio for SMS)
- Claims clearinghouse (ClaimRev)
- Payment processing
- Prior authorization

**Security & Administration:**
- Role-based access controls (phpGACL)
- Fine-grained per-user access permissions
- Active Directory / LDAP integration
- Patient document encryption
- Database connection encryption
- Audit logging
- Multi-facility support
- Custom menus

### Data & Content

Based on the database structure documentation and feature descriptions, OpenEMR stores the following categories of data:

**Patient demographics**: Full demographic records (`patient_data` table), including contact info, insurance information, employer data, and patient history (`history_data`).

**Clinical records**: Encounters (`form_encounter`), with associated clinical forms stored across numerous specialized tables — vitals (`form_vitals`), SOAP notes (`form_soap`), ophthalmology exams (`form_eye_*`), and custom layout-based forms (`lbf_data`). A `forms` table serves as an index linking form instances to encounters.

**Problem lists, medications, allergies**: Stored in the `lists` table with issue-encounter cross-references (`issue_encounter`).

**Prescriptions**: Prescription records including drug information and dispensation history.

**Lab/procedure data**: Procedure orders, reports, and results with dedicated tracking tables.

**Billing and financial data**: Billing codes per encounter (`billing` table), claims (`claims`), payments, AR activity (`ar_activity`), AR sessions (`ar_session`), and insurance data (`insurance_data`, `insurance_companies`, `insurance_numbers`).

**Scheduling**: Calendar events and appointment data.

**Documents**: Electronic document management system storing uploaded and generated documents.

**Messaging**: Patient notes between staff (`pnotes`), patient portal messages and chat history (stored in patient records for audit trail).

**Portal data**: Patient portal credentials (`patient_access_onsite/offsite`), portal-submitted forms and documents.

**Reference/coding data**: Extensive code tables for ICD-9, ICD-10, RXNORM, SNOMED, CPT, HCPCS.

**User and access data**: User accounts (`users` — dual-purpose as users and address book), access control lists (`gacl_*` tables), facility information.

**System configuration**: Global settings (`globals` table), list options (`list_options`), layout definitions.

**Disclosures**: Patient information disclosure tracking.

The database is MySQL/MariaDB with InnoDB engine (since v5.0.2). Being open-source, the full database schema is publicly visible in the GitHub repository at `sql/database.sql`.

---

*Note: Both CHPL listings (10938 and 11757) represent the same product platform — OpenEMR versions 7.0 and 8 respectively. Version 7.0 certification is being retired on February 27, 2026, with users directed to upgrade to version 8. The certified criteria are identical between the two versions.*
