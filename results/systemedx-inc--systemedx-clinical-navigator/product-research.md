# Systemedx Inc — Product Research

Researched: 2026-02-15
Developer website: https://www.systemedx.com/

## Overview

Systemedx Inc is a small, privately held healthcare technology company headquartered in Cullman, Alabama, founded in 1997. The company was originally chartered to provide document management systems to businesses and healthcare organizations, and later pivoted to focus on healthcare IT. The CEO is Kevin Bonner. The company has an estimated 11–50 employees and revenue in the $1–6 million range (sources vary). They also have an office in Alexandria, Louisiana.

Systemedx is a small-scale EHR vendor serving ambulatory practices. They are not widely reviewed on third-party platforms — Slashdot/SourceForge lists the product but has zero user reviews. The company does not appear on major review sites like G2 or Capterra with any meaningful review volume. Their customer base appears to be regional, concentrated in the Southeast U.S., with a notable presence in orthopedic and sports medicine practices. A Birmingham Medical News article describes a deployment at "a practice of 43 sports medicine and orthopedic physicians" that was an early adopter of their Surgical Pathways module.

## Product: Systemedx Clinical Navigator

CHPL ID: 11536
Version: 2024.12
Certification Date: 2024-11-26

### What It Is

Systemedx Clinical Navigator is an all-in-one ambulatory EHR and practice management system. It is a single integrated platform that combines electronic health records, practice management (scheduling, billing, claims), a patient portal, and a surgical pathways module. The certified module encompasses the full product — there is no indication of separate products or a larger platform beyond what is certified.

The product is certified for 37 ONC criteria spanning clinical documentation (a)(1)–(a)(14), transitions of care (b)(1)–(b)(3), clinical quality measures (c)(1)–(c)(3), privacy/security (d), patient portal/VDT (e)(1), public health reporting (f)(1),(f)(2),(f)(5),(f)(7), FHIR API (g)(10), and Direct messaging (h)(1). This is a broad certification footprint for a small vendor.

### Users & Market

Clinical Navigator targets ambulatory practices — primarily physician offices and multi-physician group practices. The SED intended user description is simply "Clinical Users." Based on the surgical pathways module and the Birmingham Medical News case study, orthopedic and sports medicine practices are a key customer segment.

No specific customer count is published on the website or easily found in third-party sources. The company is small enough (11–50 employees, $1–6M revenue) that the customer base is likely modest — probably dozens to low hundreds of practice sites rather than thousands.

End users include physicians/providers, clinical staff, front desk/scheduling staff, billing/coding staff, and patients (via the portal).

### Modules & Functionality

Based on the vendor website's dedicated pages for each area:

**EHR / Clinical Documentation (ehrsolutions.html)**
- "AI Office Visit" — uses AI to identify patterns in documentation and optimize frequently used items; claims to enable users to "write entire visit" with minimal clicks
- "Touch Orders" — single-click actions to send orders to imaging, write medications, and document in the chart simultaneously
- Medication management with one-click prescribing of physician favorites and refills
- Prescription Drug Monitoring Program (PDMP) integration
- Controlled substance prescribing (EPCS)
- Automatic drug interaction checking
- Patient tracking to monitor exam room status
- Doctor-specific dashboards with customizable graphs and drill-down to individual patient records
- Customizable workflows, forms, and document templates

**Practice Management (pmsolutions.html)**
- Scheduling with patient check-in/check-out tracking and wait time monitoring
- Patient registration/demographics — patients can enter demographic information from home (pre-visit)
- AI-assisted coding — analyzes coding patterns and insurance reimbursement data to suggest optimal CPT/ICD codes
- Claims worksheet — consolidates worklist management, account inquiry, and claim refiling
- Automated clean claim submission and auto-posting of remittance information
- Batched statement generation for approval
- Automated eligibility verification (mentioned on homepage)
- Claim scrubbing (mentioned on homepage)
- Financial dashboards with clinic comparisons using red/yellow/green status indicators

**Patient Portal (portal.html)**
- Patient self-registration with demographic, insurance, and clinical data entry
- Appointment requests
- Medication refill requests
- Secure messaging with clinical staff (re: lab results, plans of care)
- Online statement viewing and bill pay
- Access to clinical summaries (both overall healthcare information and service-specific summaries)

**Surgical Pathways (surgicalpathways.html + Birmingham Medical News article)**
- Surgical case tracking from start to finish
- AI-driven billing that analyzes surgeries to detect missed billing opportunities
- "Rogue surgery detection" — identifies procedures performed but not billed (article claims up to $100K/year/surgeon in recovered revenue)
- Automated CPT code suggestion (~80% accuracy, learns from adjustments)
- ICD coding optimization and automatic insurance appeal filing
- Procedure-specific task list generation (cardiac clearance, equipment ordering, OR scheduling, etc.)
- Patient text reminders for appointments, pre-surgery instructions, location maps, and post-op follow-up surveys
- Real-time dashboards for surgical pathway performance, revenue recovery, and compliance monitoring
- Mobile integration — surgeons can photograph hospital forms and send encrypted patient data to office

**MIPS/Quality Reporting (mipssolutions.html)**
- Measure calculation dashboard with color-coded performance metrics
- Quality measures export compatible with QPP submission
- Registry reporting: immunization, survey, syndromic surveillance
- 20+ clinical quality measures tested for certification

**Interfaces & Integrations (interfaces.html)**
- HL7 2.x interfaces for clinical data exchange
- Lab interfaces: LabCorp, Quest Diagnostics, Huntsville Hospital Lab, Decatur Morgan Hospital Lab, Marshall Medical Centers Lab, Indiana HIE, Intermountain Laboratory, APEX, Compass Lab
- Physical therapy: WebPT, ATI Indiana
- DME: MotionMD, Motion Medical
- Transcription/Dictation: Command Health, Nuance
- Imaging: Aspyra, RadInfo, Medstrat, WW XRay
- Other: Clearwave Kiosk, Expeditor, Oberd, Open Edge Payments, Relatient, Surgimate, WhitePlume

**FHIR API (API/AppRegistration.html)**
- OAuth 2.0-based API through "Systemedx XNet" portal
- Supports standalone patient/user apps, EHR launch apps, and bulk data apps
- Developer and user portals for app registration
- Certified for (g)(7)–(g)(10) FHIR API criteria

### Data & Content

Based on the features described above, Clinical Navigator stores and manages:

- **Patient demographics and registration data** — explicitly described as entered by patients or front desk staff, including insurance information
- **Clinical encounter documentation** — visit notes, AI-assisted office visit documentation, customizable templates
- **Medications** — prescribing, refills, medication lists, drug interactions, PDMP data, controlled substance records
- **Orders** — imaging orders, medication orders, lab orders (implied by "Touch Orders" and lab interfaces)
- **Lab results** — received via HL7 interfaces from LabCorp, Quest, and hospital labs; communicated to patients via portal messaging
- **Problems/diagnoses** — mentioned in EHI export page ("medications, problems, etc.") and implied by clinical documentation
- **Billing and claims data** — CPT codes, ICD codes, insurance claims, remittances, statements, eligibility verification results, claim scrubbing results
- **Scheduling data** — appointments, check-in/check-out, wait times
- **Surgical case data** — surgical pathways with task lists, procedure tracking, billing recovery, pre/post-op communication
- **Patient portal messages** — secure messaging between patients and clinical staff
- **Clinical summaries** — CDA documents (mentioned in EHI export page), clinical summaries accessible through portal
- **Quality measures data** — MIPS/QPP measure calculations and submissions
- **Public health reporting data** — immunization records, syndromic surveillance, cancer registry reporting (certified for f(1), f(2), f(5), f(7))
- **Documents** — clinical documents stored as PDFs (mentioned in EHI export page), transcription/dictation integration
- **Dashboard/analytics data** — physician-specific dashboards, billing dashboards, surgical pathway analytics

**Information gaps:** The website does not explicitly describe allergy management, vital signs, or growth charts as features, though these are implied by clinical (a) criteria certification (a)(1) for CPOE, (a)(3) for demographics, (a)(5) for demographics). The vendor website is relatively marketing-oriented and thin on detailed feature documentation. e-Prescribing is not explicitly labeled on the interfaces page but is implied by medication management features and PDMP/EPCS certification. Referral management is not explicitly described. The system's approach to imaging results (as distinct from imaging orders) is unclear — they integrate with imaging systems via HL7 but don't describe a results viewing workflow.
