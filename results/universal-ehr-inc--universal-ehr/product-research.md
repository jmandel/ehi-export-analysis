# Universal EHR, Inc. — Product Research

Researched: 2026-02-15
Developer website: https://www.universalehr.com

## Overview

Universal EHR, Inc. (also operating as Universal EHR Solutions / UniEHR) is a very small, privately held healthcare IT company founded in May 2005, with roots going back to 2002. The company is based in the Garden Grove / Great Neck area and appears to have only a handful of employees (LinkedIn lists 3 visible employees, with a stated range of 11-50). The company was co-founded by Aaron Wachspress (CTO) and led by Mitchell C. Shapiro (President/Chairman). The lead developer listed on CHPL, Binh Pham, is based in Garden Grove, CA.

The company's flagship product is **Physician's Solution** (also branded as Universal EHR), a browser-based EHR and practice management system targeting ambulatory/outpatient practices of all sizes. The product is marketed as "Designed FOR Doctors BY Doctors" and emphasizes ease of use, low cost, and rapid deployment (claims of going live within one week). The company has a very small market footprint — it does not appear on major review sites like Capterra or G2, and its customer base appears to be concentrated in Southern California, particularly among Vietnamese-American medical practices in the Garden Grove/Westminster area (DAO Medical Group, a 30+ physician group, appears to be a primary customer and may have a business relationship with the product's developers).

The company was recognized as the preferred EMR vendor of the Florida Chapter of the American College of Cardiology and was used by Telemedik in Puerto Rico, per a 2011 press release. There is no evidence of significant market growth since then.

## Product: Universal EHR (Physician's Solution)

CHPL IDs: 9333

### What It Is

Universal EHR (formerly/also known as Physician's Solution) is a browser-based, fully integrated EHR and practice management system for ambulatory/outpatient medical practices. It is certified as a Complete EHR under ONC standards. The system is designed for use across multiple specialties and practice sizes, from solo practitioners to multi-specialty groups.

The CHPL certification is for version 2.0.0 (certified 2018-03-12) and is broadly certified across 35+ criteria including clinical data (a)(1)-(a)(14), transitions of care (b)(1)-(b)(3), patient portal/VDT (e)(1), clinical quality measures (c)(1)-(c)(3), public health reporting (f)(1)-(f)(2), and FHIR APIs (g)(7)-(g)(10)). The SED intended user description is "OUTPATIENT CLINIC."

### Users & Market

The product targets outpatient/ambulatory practices. Based on the patient portal login page and web research, known customers include:

- **DAO Medical Group, Inc.** (Garden Grove, CA) — a 30+ physician, 100+ employee internal medicine and multi-specialty group. This appears to be the largest and most prominent customer. Michael M. Dao, MD, the group's principal, appears on LinkedIn as associated with both DAO Medical Group and universalehr.com, suggesting a deeper business relationship.
- **BAN DUC DOAN, M.D., F.A.C.O.G.** — an OB/GYN practitioner
- **Reform24 Medical Group** — appears in the patient portal login
- **Southern California Vein and Wound Care Center** — a specialty practice

The customer base appears very small and geographically concentrated in Southern California. A 2011 press release mentioned customers in Puerto Rico (Telemedik) and endorsement from the Florida ACC chapter, but there is no evidence of broader adoption. The product does not appear on any major third-party EHR review sites (Capterra, G2, KLAS, Software Advice), which is consistent with a very small user base.

### Modules & Functionality

Based on vendor press releases, the website, and product descriptions, Universal EHR / Physician's Solution includes the following modules and capabilities:

**Clinical / EHR:**
- Patient information management — entering and storing patient health information electronically
- Clinical documentation and charting
- Customizable templates designed by specialists for specific fields (OB/GYN, cardiology, pediatrics, internal medicine, and "more than a dozen" other specialty types)
- Prescription ordering (e-prescribing)
- Lab orders and results review
- Diagnostic device interfacing (e.g., EKG machines — printed graphs automatically filed in patient chart)
- Image management (labs and images accessible remotely)
- Message review

**Practice Management:**
- Appointment scheduling
- Claims and billing processing — described as a "turnkey solution" that either includes billing or interfaces with existing practice management/billing systems bidirectionally via XML or HL7 formats
- Charge capture
- Collections
- Reporting and performance analysis
- Superbill generation (evidenced by a "superbill2000comp.pdf" document on their site linked to DAO Medical Group)

**Patient Engagement:**
- **Patient Direct** — patient-facing portal (the patient portal at universalehr.com/Login/ is visible and functional)
- **Doctor Direct** — physician-patient communication system; allows doctors to send test results and comments directly to a secure patient vault; described as reducing non-essential phone calls
- **Physician's Portal** — message and data sharing between providers

**Interoperability & Integration:**
- HL7 and XML bidirectional interfaces with practice management/billing systems
- Hospital, laboratory, and radiology interfaces
- Referring physician communication
- Interoperability Engine / API access (references to EMR Direct API terms of use on the website)
- FHIR API support (certified for g(7)-(g)(10))

**Enterprise:**
- **Hospital's Solution** — described as a "three-in-one package" for enterprise control (mentioned in press releases, likely a separate product line for larger facilities)

**Deployment:**
- Cloud/browser-based — accessible from any internet-connected device (laptop, tablet, PDA, smartphone)
- No third-party applications required
- Described as supporting rapid deployment

### Data & Content

Based on the features described above and the certification criteria, the system stores and manages:

- **Patient demographics** — names, dates of birth, SSN (last 4 digits used for patient lookup), phone numbers, zip codes, email addresses, patient photos (evidenced by photo display on login)
- **Clinical records** — patient charts, clinical notes, treatment procedures
- **Prescriptions and refills** — medication orders and history
- **Lab results** — laboratory data, test results
- **Diagnostic images** — EKG graphs, imaging results automatically filed in charts
- **Messages** — provider-to-patient communications via Doctor Direct, provider-to-provider messages via Physician's Portal
- **Scheduling data** — appointment records
- **Billing/claims data** — charge capture, claims, superbills, collections (whether built-in or via bidirectional interface with external PM system is somewhat ambiguous — the product is described both as a "turnkey solution" and as something that "interfaces with" existing PM systems)
- **Reports** — performance analysis, clinical quality measures (certified for CQMs)
- **Public health reports** — immunization and syndromic surveillance data (certified for f(1) and f(2))
- **Security questions and authentication data** — patient portal security questions, usernames/passwords

**Gaps and uncertainties:**
- The vendor website is sparse and provides limited detail. Most specific feature information comes from press releases from 2011, which may not fully reflect the current state of version 2.0.0 (certified 2018).
- Whether billing is fully integrated or primarily relies on bidirectional interfaces with external PM systems is unclear — both descriptions exist in vendor materials.
- The "Hospital's Solution" product is mentioned in press releases but there is no current web presence for it; it's unclear if it's still offered.
- No third-party reviews were found on any major review platform, making it impossible to corroborate vendor claims with user experiences (other than one unverifiable Capterra reference that may have been for a different product).
- The product appears to have very limited documentation publicly available. The mandatory disclosures URL points to the main website homepage, which provides minimal information.

---
