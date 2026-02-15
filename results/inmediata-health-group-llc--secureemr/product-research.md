# Inmediata Health Group LLC — Product Research

Researched: 2026-02-15
Developer website: https://www.inmediata.com (redirects to https://portal.inmediata.com/)

## Overview

Inmediata Health Group LLC is a San Juan, Puerto Rico-based healthcare IT company founded in 2002 by Severiano Lopez-Marrero. The company started as a healthcare clearinghouse and claims processing intermediary, and has grown into a full-suite health IT vendor serving physicians, dentists, hospitals, labs, medical schools, and payers — predominantly in Puerto Rico. Inmediata processes approximately 85% of all medical claims in Puerto Rico and manages over 1.3 million lives on the island. They serve over 13,000–15,000 healthcare providers (sources vary) across more than 300 specialties.

The company's product suite includes: **SecureClaim** (practice management and billing), **SecureTrack** (clearinghouse), **SecureEMR+** (electronic medical records), and **SecureInsight** (analytics/business intelligence). All solutions are 100% cloud-based. Inmediata also dominates over 80% of Puerto Rico's dental claims processing market. The company has an office in Charlotte, NC, with expansion plans toward Florida, Texas, Arizona, New Mexico, and Spanish-speaking markets in Central and South America.

Notably, Inmediata was the subject of a HIPAA settlement with HHS OCR following a 2019 data breach, resulting in a $1.13M settlement and corrective action plan.

## Product: SecureEMR+

CHPL ID: 11753

### What It Is

SecureEMR+ is a cloud-based electronic medical records system with integrated billing, described by Inmediata as "the most comprehensive EMR, Integrated Billing (PMS), and Services System Puerto Rico has ever seen." It is the only ONC-certified EHR product in Puerto Rico with KLAS recognition.

**Critical context: SecureEMR+ is built on PrognoCIS**, an established EHR platform developed by Bizmatics, Inc. (a Silicon Valley-based company). In May 2021, Inmediata and PrognoCIS/Bizmatics announced a partnership, and SecureEMR+ is "derived from this union" — combining PrognoCIS's clinical EMR platform with Inmediata's billing tools (SecureClaim) and clearinghouse connectivity (SecureTrack). The EHI export documentation URL references "PrognoCIS Support" in its filename, confirming the underlying platform.

This means SecureEMR+ is essentially a localized/integrated version of PrognoCIS tailored for the Puerto Rico market, bundled with Inmediata's existing billing and clearinghouse infrastructure. PrognoCIS itself has a 20+ year track record (since ~2001) and is used by ambulatory clinics across the US mainland.

The certified product has a broad set of ONC criteria: clinical data management (a)(1)–(a)(5), (a)(12), (a)(14)–(a)(15); transitions of care (b)(1)–(b)(3); patient portal (e)(1), (e)(3); public health reporting (f)(1), (f)(2), (f)(5), (f)(7); FHIR APIs (g)(7), (g)(9), (g)(10); and clinical quality measures (c)(1)–(c)(4). The intended user description is "Outpatient Clinic."

### Users & Market

SecureEMR+ is used primarily by outpatient/ambulatory medical practices in Puerto Rico. Inmediata's overall customer base includes 13,000–15,000 providers across 300+ specialties (medical, dental, allied health, ambulance). The EMR product specifically targets physicians and clinical staff in ambulatory settings.

The underlying PrognoCIS platform (per SoftwareFinder reviews, 118 reviews, 4/5 stars) is used across cardiology, dermatology, family medicine, internal medicine, psychiatry, and other specialties. Users praise its ease of use and integrated billing-clinical workflow, though some complain about support responsiveness and document upload size limits (5 MB cap).

No specific customer case studies or deployment numbers were found for SecureEMR+ specifically (as distinct from Inmediata's broader product suite).

### Modules & Functionality

Based on vendor materials from the mandatory disclosures page and the Inmediata/PrognoCIS partnership announcement, SecureEMR+ includes:

**Clinical EMR (from PrognoCIS):**
- Clinical charting with customizable templates, smart phrases, and specialty-specific progress notes
- Clinical Decision Support — automated analysis of data and symptoms to assist diagnoses
- Problem lists, medication lists, allergy lists (certified criteria (a)(1)–(a)(5))
- Drug-drug and drug-allergy interaction checking ((a)(4))
- Demographics recording ((a)(5))
- Implantable device list ((a)(14))
- Social, psychological, and behavioral data ((a)(15))
- Lab ordering and results integration (seamless integrations with labs, radiology companies, vaccine registries)

**Practice Management & Billing (from Inmediata SecureClaim + PrognoCIS PMS):**
- Integrated billing — HL7 format data generation converting to claims
- Patient eligibility verification
- Appointment scheduling with reminders
- Claims management, electronic submission, payment posting, denial tracking
- Revenue cycle management with financial reporting
- Payment reconciliation and electronic payment settlements
- Automated inventory control for medical billing tasks
- Case management and authorization requests

**e-Prescribing:**
- Electronic prescribing including controlled substances (EPCS)
- Direct pharmacy transmission (Surescripts integration implied by certification)
- Complete medication histories
- Prescription refill management

**Patient Portal:**
- Lab results viewing
- Appointment reminders and scheduling
- Prescription refill requests
- Secure messaging with providers
- Document access
- Patient app for mobile access
- Two-factor authentication

**Telemedicine:**
- HIPAA-compliant video conferencing for remote consultations

**Referral Management:**
- Tools to streamline and manage referred patients

**Population Health:**
- Specialty-tailored metrics and population health analytics

**Interoperability & Data Exchange:**
- Transitions of care / C-CDA document exchange ((b)(1)–(b)(3))
- FHIR API access ((g)(7), (g)(9), (g)(10))
- Integration with Inmediata's SecureTrack clearinghouse (handles ~85% of PR medical claims)

**Productivity Tools:**
- E-faxing
- Text messaging
- Voice/speech recognition
- Electronic signatures
- Document scanning and management

**Public Health Reporting:**
- Immunization registry reporting ((f)(1))
- Syndromic surveillance ((f)(2))
- Cancer registry ((f)(5))
- Electronic case reporting ((f)(7))

**Clinical Quality Measures:**
- CQM capture, calculation, import, and filtering ((c)(1)–(c)(4))

### Data & Content

Based on the features and certified criteria described above, SecureEMR+ stores and manages:

- **Patient demographics** — names, addresses, insurance info, identifiers (certified (a)(5))
- **Clinical records** — problem lists, medication lists, allergy lists, immunizations, vital signs, clinical notes/progress notes with specialty-specific templates
- **Orders and results** — lab orders, lab results, radiology orders/results, imaging data references
- **Medications and prescriptions** — current/historical medications, e-prescribing records, controlled substance prescriptions, pharmacy transmission records, refill history
- **Clinical decision support data** — alerts, rules, intervention records
- **Implantable device data** — UDI tracking (certified (a)(14))
- **Social/behavioral data** — social determinants, psychological and behavioral health data (certified (a)(15))
- **Billing and claims data** — claims, superbills, payment records, ERA/EOB data, eligibility responses, denial tracking, financial reports. This is deeply integrated given Inmediata's clearinghouse role processing 85% of PR claims.
- **Scheduling data** — appointments, reminders, provider schedules
- **Patient portal interactions** — messages, portal access logs, patient-submitted documents
- **Telemedicine records** — virtual visit records/sessions
- **Referral data** — referral orders, tracking, authorization requests
- **Documents** — scanned documents, faxes, uploaded files (note: 5 MB upload limit per PrognoCIS user reviews)
- **Transitions of care documents** — C-CDA documents sent and received
- **Public health reports** — immunization submissions, syndromic surveillance data, cancer registry reports, electronic case reports
- **Quality measure data** — CQM numerator/denominator data, measure calculations
- **Audit logs** — access and activity tracking (certified (d) criteria)

**Key observation:** The billing/claims data aspect is unusually deep for this product because Inmediata's core business is clearinghouse and claims processing. SecureClaim (the billing/PMS component integrated into SecureEMR+) handles the full lifecycle from patient intake through claim processing and reimbursement. Given that Inmediata processes ~85% of all medical claims in Puerto Rico, the claims and billing data stored in the system is likely extensive.

**Gaps in research:** No detailed product documentation or user manual was available publicly. The vendor website is relatively sparse compared to mainland US EHR vendors. The PDF brochure at portal.inmediata.com was not machine-readable. No third-party reviews specific to SecureEMR+ (as distinct from PrognoCIS) were found on G2, Capterra, or similar sites. The KLAS recognition mentioned on the site likely refers to PrognoCIS's KLAS ranking rather than a separate SecureEMR+ evaluation.
