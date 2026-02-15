# Patient First — Product Research

Researched: 2026-02-14
Developer website: https://www.PatientFirst.com

## Overview

Patient First Corporation is a privately held chain of urgent care and primary care walk-in medical centers operating ~79 locations across Virginia, Maryland, Pennsylvania, and New Jersey. Founded in 1981 by Richard P. "Pete" Sowers III, a former emergency physician, in Richmond, Virginia, the company remains privately held under the founder's leadership with no stated intention to sell. Patient First is among the top 10 largest urgent care chains in the United States (Washington Post, 2019), with estimated revenue in the hundreds of millions and roughly 1,000–5,000 employees. All locations operate 8am–8pm, 365 days a year, with no appointment necessary.

What makes Patient First distinctive in the EHR context is that they **developed their own proprietary EHR system in-house** rather than purchasing a commercial product. The PAS system is built and maintained by an internal MIS/software development team at their Glen Allen, VA headquarters. It is not sold or licensed to any external organization. This is an unusual case — a large healthcare provider organization that is also its own EHR developer.

## Product: PAS

CHPL IDs: 11065

### What It Is

PAS is Patient First's self-developed, ONC-certified electronic health record system. The acronym likely stands for "Patient Administration System" or "Practice Administration System," though this is not definitively confirmed in public sources. The CY 2025 Real World Testing Report explicitly states: "Patient First's PAS EHR was developed by Patient First for use exclusively in our own urgent care centers."

PAS is a **full EHR system** — not merely practice management or a clinical module. It covers clinical documentation, CPOE (medications, labs, diagnostic imaging), e-prescribing, clinical decision support, lab integration, imaging, transitions of care, patient portal, quality reporting, public health reporting, billing, and a FHIR API. The system is certified for 30 ONC criteria spanning clinical (a-criteria), interoperability (b-criteria), quality measures (c-criteria), security (d-criteria), patient access (e-criteria), public health (f-criteria), and API access (g-criteria).

The certified module *is* the product — there is no separate commercial platform or larger suite. PAS is a single, integrated system purpose-built for Patient First's urgent care + primary care workflow.

### Users & Market

**PAS has no external customers.** It is used exclusively in Patient First's own ~79 clinics. The intended users, per the CHPL listing, are "clinical and non-clinical health care staff." In practice this means:

- Physicians and mid-level providers (urgent care/primary care)
- Clinical staff (nurses, medical assistants)
- Registration/front desk staff
- Billing and administrative staff
- Patients (via the proprietary patient portal)

Patient First's volume is substantial. Per their CY 2025 Real World Testing Report (Q1 2025 data, annualized):
- ~1.9 million e-prescriptions per year
- ~716,000 transition-of-care C-CDAs per year
- ~240,000 patient portal logins per year
- ~3.3 million syndromic surveillance messages per year (VA and MD)
- ~65,000 immunization registry messages per year
- ~124 EHI export requests per year
- 0 third-party FHIR API applications connected (as of Q1 2025)

Because PAS is an internal-only system, there are **no third-party reviews** on G2, Capterra, KLAS, or Definitive Healthcare. Employee reviews on Glassdoor (3.4/5.0 stars, ~567 reviews) occasionally mention the technology: recurring themes include descriptions of the system as "old" or "outdated" and noting "unique abbreviations not used in other healthcare settings," suggesting a deeply custom system with its own conventions. Some employees describe it positively.

### Modules & Functionality

PAS covers the full scope of Patient First's clinical and administrative operations. Based on certification criteria, the mandatory disclosures page, the Real World Testing report, and information from the Patient First website:

**Clinical Documentation & CPOE:**
- CPOE for medications, laboratory orders, and diagnostic imaging orders (certified (a)(1)–(a)(3))
- Drug-drug and drug-allergy interaction checks (certified (a)(4), using Micromedex)
- Demographics recording (certified (a)(5))
- Family health history (certified (a)(12))
- Implantable device list (certified (a)(14), using FDA GUDID API)
- Clinical decision support (certified (a)(9) per disclosures page)
- Clinical quality measure recording, calculation, import, and reporting (certified (c)(1)–(c)(3))
- Certified CQMs include measures for blood pressure screening, BMI, diabetes management (HbA1c, foot exam, nephropathy), pneumococcal vaccination, tobacco screening, pharyngitis testing, URI treatment, and hypertension control

**E-Prescribing:**
- Electronic prescribing through Surescripts 10.6 (certified (b)(3))
- ~480,000 prescriptions per quarter across 4 states

**Lab & Imaging:**
- On-site CLIA-approved labs at every Patient First location (blood work, pregnancy tests, routine labs)
- Digital x-ray imaging on-site at every location
- Lab results available to patients immediately through portal when ready

**On-site Medication Dispensing:**
- Patient First dispenses select common medications directly to patients during visits (not a full pharmacy, but on-site dispensing of frequently needed medications)

**Transitions of Care & Interoperability:**
- C-CDA generation and exchange (certified (b)(1), (g)(6))
- Clinical information reconciliation and incorporation (certified (b)(2))
- Secure health information exchange via DataMotion Direct messaging
- ~180,000 C-CDAs sent per quarter

**Patient Portal:**
- Proprietary patient portal at portal.patientfirst.com (not MyChart or any third-party platform)
- View, download, transmit health information (certified (e)(1))
- Visit history across all Patient First locations
- Lab results access
- View and pay outstanding balances; view previous/itemized statements
- Secure messaging for questions about recent visits
- Requires in-person activation with photo ID; patients must be 18+

**Public Health Reporting:**
- Immunization registry transmission (certified (f)(1)) — ~16,000 messages per quarter
- Syndromic surveillance reporting (certified (f)(2)) — ~831,000 messages per quarter (VA and MD)

**API Access:**
- FHIR-based Standardized API (certified (g)(7), (g)(9), (g)(10))
- Production API server built; tested with Postman and ONC Inferno
- No third-party apps connected as of Q1 2025

**Occupational Health:**
- Workers' compensation treatment
- DOT physicals
- Drug testing and drug screen results
- Employer portal for invoices, drug screen results, medical records, and workers' comp summaries
- Return-to-work protocols

**Telehealth:**
- Available 8am–6pm daily in VA, MD, PA, NJ for patients 12+
- Integrated into the PAS system (implied by unified medical records across visit types)

### Data & Content

The mandatory disclosures page explicitly lists the following categories included in EHI exports, which reveals the data types PAS stores:

| Category | Description | Format |
|---|---|---|
| Medical Records | C-CDA clinical records (problems, medications, allergies, vitals, procedures, etc.) | XML (C-CDA) |
| X-Rays | Diagnostic x-ray images | DCM (DICOM) |
| Scanned Images | Insurance cards, photo ID, etc. | JPG, PNG |
| Consults | Documents from referrals | PDF |
| Messages | Secure messages to/from patient | EML |
| Forms | Drug screen results, etc. | PDF |
| Financials | Billing and claim information | JSON |

This is a useful starting point but the question for Phase 2 will be whether this covers everything PAS stores. Based on the functionality described above, PAS likely stores at minimum:

- **Clinical data:** encounter notes, problem lists, medication lists, allergy lists, vitals, family history, immunization records, implantable device records, clinical decision support alerts/interactions, lab orders and results, imaging orders, procedures
- **Administrative data:** demographics, insurance information, registration data, scheduling/appointment data
- **Financial data:** billing records, claims, payments, statements, balances (confirmed by "Financials" export category and portal payment features)
- **Communications:** secure patient-provider messages (confirmed by "Messages" category), referral/consult documents
- **Documents & images:** scanned insurance cards, photo IDs, x-ray images (DICOM), drug screen result forms, other clinical documents
- **Occupational health data:** workers' comp records, DOT physical results, drug testing results, employer-specific records
- **Portal data:** patient portal accounts, activation codes, login history
- **Quality measure data:** eCQM calculation data, quality reporting submissions
- **Public health data:** immunization registry submissions, syndromic surveillance data
- **Audit data:** access logs, amendment requests (required by (d) criteria)

The website doesn't clearly separate what's in the core clinical record vs. what's in separate administrative/occupational health modules. The degree to which occupational health, telehealth encounters, and employer portal data are part of the EHI export is a key question for Phase 2.

### Technology & Architecture

- **Internally developed and maintained** by Patient First's MIS department (VP MIS: Rhonda Beckner/Robert Pitt)
- **Developer contact:** SoftwareDevelopers@patientfirst.com
- Active hiring of Software Developers and Programmers at Glen Allen, VA headquarters
- Job postings reference on-premises and cloud infrastructure with a focus on automation
- External dependencies: Surescripts (e-prescribing), DataMotion (Direct messaging), Micromedex (drug interactions), FDA GUDID API (device identifiers)
- Uses Workday for HR (separate from PAS)
- Employee reviews suggest the system has proprietary conventions and unique abbreviations that differ from industry-standard EHR systems
