# Genensys LLC — Product Research

Researched: 2026-02-15
Developer website: http://www.genensys.com/

## Overview

Genensys LLC is a small, privately held healthcare IT company based in Oviedo, Florida (Orlando metro area). The company has approximately 11–12 employees and an estimated annual revenue of ~$7 million. Genensys develops EMR/EHR and practice management software primarily targeting small to mid-sized independent and specialty practices, with a notable focus on pediatric therapy clinics (speech therapy, occupational therapy, physical therapy, applied behavior therapy). The company also offers revenue cycle management services, digital marketing for medical practices, and HIPAA compliance consulting. The company appears to be founder-led (Farhan Shamsi is listed as the primary contact).

Genensys operates a product ecosystem under the "Simplify" brand, including Simplify EMR (the general-purpose certified EHR), Simplify Therapy (a therapy-focused variant/configuration), and Simplify SMP (a School Medicaid Program billing tool for school districts). The company positions itself on affordability, ease of use, and customizability relative to larger EHR vendors.

## Product: Simplify EMR

CHPL IDs: 10317 (15.05.05.1523.GENS.01.00.1.200225)

### What It Is

Simplify EMR v4.0 is a cloud-based, ONC-certified EHR and integrated practice management system designed for ambulatory clinics of all sizes. The certification is broad — 35+ criteria spanning clinical documentation (a)(1)–(a)(14), transitions of care (b)(1)–(b)(2), patient portal (e)(1)–(e)(2), public health reporting (f)(1)–(f)(2), FHIR APIs (g)(7)–(g)(10), and direct messaging (h)(1). The system was certified in February 2020 and remains active.

The certified product appears to encompass the full Simplify EMR platform, which includes the EHR, practice management, and patient portal as a unified system. The vendor describes it as "fully unified" — the EHR, scheduling, billing, and patient portal are integrated rather than separate bolt-on modules.

The mandatory disclosures page notes that MDToolBox is required as additional software (likely for e-prescribing/EPCS functionality), and the system is web-based, requiring only a current web browser.

### Users & Market

**Target users:** Clinicians (physicians, therapists), nurses, billing staff, and practice managers at small to mid-sized independent practices. The FindEMR listing describes the target as "practices with approximately six physicians or fewer."

**Specialty focus:** The vendor has a strong emphasis on pediatric therapy practices (OT, PT, speech therapy, ABA), but also markets to general ambulatory clinics. The "Simplify Therapy" branding on their website targets pediatric therapy clinics specifically, while "Simplify EMR" is the general-purpose offering. Both appear to share the same underlying platform with specialty-specific configurations/templates.

**Customer base:** No specific customer count is disclosed on the website. The company's small size (11–12 employees, ~$7M revenue) suggests a relatively small installed base, likely in the hundreds of practices or fewer. Testimonials on the site come from small practice owners who emphasize affordability.

**Geography:** Primarily US-based; the company is in Florida and markets nationally.

**Additional product — Simplify SMP:** Genensys also offers a School Medicaid Program billing tool that helps school districts manage Medicaid reimbursement for IDEA-related therapeutic services (speech, PT, OT, behavioral services, nursing, transportation). This integrates with the broader Simplify EMR ecosystem and manages billing/claims data for school-based therapy services.

### Modules & Functionality

Based on vendor website pages, mandatory disclosures, and third-party descriptions:

**Electronic Health Records / Clinical Documentation:**
- Patient charting and clinical documentation with customizable templates
- Comprehensive patient records accessible in a consolidated view ("one click on a patient's name will give you the entire record")
- Designed to be "fully customizable" to individual practice workflows
- Supports CPOE for medications and laboratory orders (certified (a)(1))
- Drug-drug, drug-allergy, and drug-diagnosis interaction checking
- Demographics recording, problem list, medication list/reconciliation, medication allergy list (certified (a)(5)–(a)(8))
- Clinical decision support (certified (a)(6))
- Implantable device list (certified (a)(14))
- Family health history (certified (a)(12))
- Patient-specific education resources (certified (a)(13))
- Clinical quality measures reporting — tested with CQMs including depression screening, specialist referral follow-up, medication documentation, BMI screening, high-risk medication use in elderly, blood pressure control

**E-Prescribing (EPCS):**
- Electronic prescribing including controlled substances
- Integrated with MDToolBox (required additional software per disclosures)
- Connections to "over 40,000 pharmacies across the country"
- Medication history, prescription benefits, formulary data
- Age and weight-based dosing adjustments
- Treatment recommendations and dosage guidance

**Laboratory Integration:**
- Electronic lab ordering and result receipt
- Lab result trending and comparison (current vs. past results)
- Alerts for abnormal results
- Task assignment for lab follow-up
- Advanced lab reporting

**Practice Management / Scheduling:**
- Enterprise scheduling integrated with patient records
- Automated messaging services and appointment reminders
- Billing and claims management
- Rules-based claims editing (vendor claims 40% error reduction)
- Eligibility checks
- Responsibility estimator for point-of-service collections
- Authorization management
- Revenue cycle management (billing, credentialing, denial management, AR management)

**Patient Portal:**
- Secure online access to medical records and clinical summaries
- Online bill pay (credit card)
- Patient-provider messaging
- Appointment request submission
- Prescription renewal requests
- Lab results viewing
- Educational materials access
- Email reminders for upcoming appointments

**Interoperability / Data Exchange:**
- FHIR APIs for third-party access (certified (g)(7), (g)(9), (g)(10))
- Direct messaging (certified (h)(1))
- Transitions of care / C-CDA exchange (certified (b)(1), (b)(2))
- Connections to health information exchanges, pharmacies, payers, imaging services, hospital networks, referring providers, immunization registries, and specialty registries
- Public health reporting: immunization registry (f)(1) and syndromic surveillance (f)(2)

**Telehealth:**
- Tele-therapy / telemedicine services mentioned on the website, though details are sparse

**Reporting & Analytics:**
- Data mining reports
- Intelligent billing reports
- Pediatric-specific dashboard monitoring (for therapy variant)

### Data & Content

Based on the features described above, Simplify EMR stores and manages:

- **Patient demographics** — standard demographic data
- **Clinical records** — problem lists, medication lists, allergy lists, medication history, family health history, implantable device lists, clinical notes/charting
- **Orders** — medication orders (CPOE), lab orders
- **Prescriptions** — e-prescribing data including controlled substances, medication history, formulary data, prescription benefits
- **Lab results** — electronic lab results with trending data and historical comparisons
- **Clinical quality measures** — CQM data for reporting (depression screening, BMI, blood pressure, etc.)
- **Scheduling data** — appointments, reminders, automated messages
- **Billing/claims data** — claims, eligibility records, authorization data, payment data, AR data
- **Patient portal data** — messages, prescription renewal requests, appointment requests, bill payments
- **Care coordination** — C-CDA documents, transition of care records, direct messages
- **Public health data** — immunization registry submissions, syndromic surveillance data
- **Audit logs** — required by (d) criteria certifications
- **User/provider data** — multi-factor authentication, access controls, user profiles

The mandatory disclosures state there are "no additional costs for the certified functionality" — all features are included in the base subscription, with recurring fees for support and licensing.

**Information gaps:** The vendor website provides limited detail on specific data fields or database structure. There is no public documentation of the data model. The therapy-specific features (pediatric dashboards, therapy-specific templates) suggest additional specialty data structures, but these are not detailed on the website.
