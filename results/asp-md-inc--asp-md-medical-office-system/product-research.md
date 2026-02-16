# ASP.MD Inc. — Product Research

Researched: 2026-02-15
Developer website: https://www.asp.md/

## Overview

ASP.MD Inc. is a very small, privately held healthcare IT company founded in 2001 by Christopher Kreis, MD — a physician and computer scientist — and headquartered in the Kendall Square technology center of Cambridge, Massachusetts. The company has approximately 14–19 employees and an estimated $1–5 million in annual revenue (per third-party business data aggregators). ASP.MD offers an integrated, web-based practice management and EHR platform alongside professional billing and compliance services. The company targets independent medical practices — primarily internal medicine and family medicine — that want to remain independent while managing regulatory complexity. There is no indication of any acquisitions, mergers, or rebranding history; the company appears to have operated under the same name since founding.

## Product: ASP.MD Medical Office System (AMOS)

CHPL ID: 10818

### What It Is

AMOS is a fully web-based, cloud-hosted, integrated Electronic Health Record (EHR) and Practice Management (PM) system. It is browser-based with no client-side software installation required. The product is subscription-based with no upfront licensing costs, and all updates, maintenance, and backups are handled by ASP.MD. The certified module appears to be the entire product — ASP.MD does not describe separate product lines or component-based licensing. This is a single, integrated platform covering clinical documentation, practice management, billing, and patient portal functions.

The CHPL certification is broad, covering 33 criteria across clinical data (a)(1)–(a)(14), transitions of care (b)(1)–(b)(3), clinical quality measures (c)(1), patient portal/VDT (e)(1)/(e)(3), public health reporting (f)(1)/(f)(2), FHIR APIs (g)(7)/(g)(10), and immunization registry (h)(1). The SED intended user description is "Internal Medicine."

### Users & Market

ASP.MD targets small, independent ambulatory medical practices. Specialties mentioned on the website include internal medicine, internal medicine subspecialties, family medicine, and "many other medical specialties." The company positions itself as a solution for practices that want to stay independent rather than joining large health systems — providing not just software but also billing services and compliance guidance (MACRA/MIPS).

The company is very small. No customer counts, site numbers, or user counts are published on the vendor's website. No third-party reviews were found on G2, Capterra, or SoftwareAdvice — the product does not appear to be listed on any of these platforms. Third-party business data suggests roughly 14–19 employees, which is consistent with a vendor serving a small number of practices. There are no notable customer case studies or press releases.

### Modules & Functionality

Based on the vendor's website (primarily the software features page and homepage):

**Scheduling & Registration**
- Appointment scheduling with automated phone/text/email reminders
- Patient registration
- Automatic electronic eligibility checking (real-time insurance verification)

**Electronic Health Record**
- Clinical documentation with templates and checklists
- Problem lists, medications, allergies tracking
- Clinical notes and encounter documentation
- Lab result management with built-in connectivity to external laboratories (LabCorp and Quest mentioned in search results, though not prominently on the current website)
- Image and document management
- Clinical decision support

**E-Prescribing**
- Electronic prescribing module (CHPL certification for (a)(1) CPOE medications confirms this)
- Drug interaction checking (certified under (a)(4))

**Billing & Claims**
- Electronic coding with payer-specific rules, eliminating paper encounter forms
- HCC (Hierarchical Condition Category) optimization alerts
- Automated claims generation and submission
- Claims scrubbing and adjudication tracking
- Electronic remittance/payment posting
- Reported first-pass claim acceptance rate of 98%+
- Real-time billing visibility

**Patient Portal**
- Patient access to core health information
- Lab results viewing
- Secure messaging with providers
- Clinical summary download
- Setup via email capture at check-in

**Quality Reporting / MIPS**
- MIPS analytics integrated into the platform
- ASP.MD is one of only 17 vendors certified as both a CMS data submission vendor and CMS-certified registry
- Supports 48 certified clinical quality measures (per mandatory disclosures page)

**Public Health Reporting**
- Immunization registry transmission (certified (h)(1))
- Syndromic surveillance reporting (certified (f)(2))
- Transmission to public health agencies (certified (f)(1))

**Transitions of Care**
- C-CDA generation for transitions of care (certified (b)(1)–(b)(3))
- Ability to receive and reconcile incoming transition documents

**API Access**
- FHIR-based API access (certified (g)(7)–(g)(10))

**Professional Services** (offered alongside the software)
- Medical billing services (ASP.MD appears to offer billing-as-a-service, not just billing software)
- Medical transcription services
- MACRA/MIPS compliance guidance and consulting

### Data & Content

Based on the features described above and the certification criteria, AMOS manages:

- **Patient demographics** — registration, insurance eligibility, contact information
- **Clinical records** — problem lists, medications, allergies, clinical notes, encounter documentation
- **Orders** — medication orders (e-prescribing), lab orders, imaging/radiology orders (certified (a)(2)/(a)(3))
- **Results** — lab results (with external lab connectivity), imaging results
- **Documents and images** — clinical documents, images, scanned records
- **Scheduling data** — appointments, reminder logs
- **Billing and claims data** — encounter coding, claims, remittances, payment posting, eligibility checks
- **Patient portal data** — secure messages between patients and providers, patient-accessed summaries
- **Quality measure data** — CQM tracking data for 48 measures, MIPS submissions
- **Public health submissions** — immunization data, syndromic surveillance data
- **Transition of care documents** — sent and received C-CDAs
- **Prescriptions** — e-prescribing history, drug interaction checks
- **Audit logs** — required by certification criteria (d)(1)–(d)(9)

The vendor's mandatory disclosures confirm there are no additional third-party software licenses required for operation, reinforcing that this is a single integrated system — all data listed above lives within AMOS.

**Gaps in information:** The website does not mention specific details about referral management, fax integration, patient consent tracking, or detailed document management beyond clinical images. It is unclear whether the system stores structured family history data (though (a)(12) family health history is a certified criterion, confirming it does). The website also does not describe any data analytics or population health features beyond MIPS reporting. No information was found about behavioral health, substance abuse, or specialty-specific clinical modules — the product appears to be a general ambulatory EHR/PM without deep specialty customization.
