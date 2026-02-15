# Astronaut, LLC — Product Research

Researched: 2026-02-14
Developer website: https://astronautehr.com

## Overview

Astronaut, LLC is a small, privately held EHR company founded in 2009 by Dr. Ignacio Valdes, a Houston-based psychiatrist board-certified in both Psychiatry and Clinical Informatics. The company builds **Astronaut EHR**, a cloud-hosted adaptation of **VistA** — the open-source electronic health record system originally developed by the U.S. Department of Veterans Affairs. Astronaut was the first VistA-based EHR to be deployed in the cloud. The company appears to be a very small operation: the leadership page lists a CEO (Dr. Valdes), a President (Janet Blazek Valdes), two senior software engineers, and a Director of Training. The developer contact email is a Gmail address.

Dr. Valdes also operates Blue Bonnet Clinic, a psychiatry practice in Houston, which uses Astronaut EHR — making this both a product company and a practitioner-driven venture. The company markets itself as a low-cost alternative to proprietary EHR systems, emphasizing that implementation costs are "a small fraction" of commercial systems. Astronaut has a national footprint but appears to serve a small number of practices, primarily small ambulatory clinics and community health centers.

## Product: Astronaut

CHPL IDs: 10809

### What It Is

Astronaut EHR is a cloud-based, modernized version of **VistA** (Veterans Health Information Systems and Technology Architecture) with a customized version of **CPRS** (Computerized Patient Record System) — the standard VistA GUI client — rebranded as **Astro-CPRS**. The product builds on VistA's comprehensive clinical platform while adding proprietary features and modern web technologies to the user interface.

The certified product (version 1709, certified 2022-02-01) carries a substantial set of ONC certifications — 30+ criteria spanning clinical data (a)(1)–(a)(14), care coordination (b)(1)/(b)(3), FHIR APIs (g)(10), Clinical Quality Measures (c)(1), public health (h)(1), and the EHI export requirement (b)(10). This broad certification footprint is consistent with VistA's heritage as a full-featured EHR.

The product is browser-based ("100% of browsers, no software installation required") and cloud-delivered with automatic upgrades. It provides a CCDA Web API (version 2021.12.19) using HTTP Basic authentication for patient data exchange.

### Users & Market

**Target users:** Physicians, nurse practitioners, mid-level providers, and clinical staff in small-to-mid-size ambulatory practices. Dr. Valdes's own psychiatry practice (Blue Bonnet Clinic in Houston) is a reference deployment.

**Settings:** The product has been deployed in individual physician offices, outpatient clinics, community health centers, and Partial Hospitalization Programs (PHPs). One announced customer is MSP-Healthcare, an Arizona-based provider who joined the Astronaut network in 2016.

**Market position:** This is a very small, niche vendor. No customer counts, revenue figures, or market share data were found. The company does not appear on major EHR review sites (G2, Capterra, KLAS). No third-party reviews were found. The product is positioned as a low-cost option for practices that want VistA's clinical depth without a large IT footprint.

**Go-to-market:** Direct sales. The company describes itself as a "full-service EHR vendor" offering billers, developers, and programmers — suggesting they provide implementation and support services directly rather than through channel partners.

### Modules & Functionality

Because Astronaut is built on VistA, it inherits VistA's extensive module architecture. The following capabilities are documented through a combination of Astronaut's own website, the Open Health News profile, the mandatory disclosures page, and VistA's well-known architecture:

**Core VistA/CPRS capabilities (inherited):**
- **Computerized Physician Order Entry (CPOE):** Ordering of medications, laboratory tests, radiology/imaging, diets, and procedures — confirmed by (a)(1)–(a)(3) certification
- **Problem List:** Patient diagnoses and problem tracking — (a)(6)
- **Medication List / Pharmacy:** Active and historical medications, drug-drug and drug-allergy interaction checking — (a)(1), (a)(4)
- **Allergy/Adverse Reaction Tracking:** Recording and alerting on medication allergies
- **Laboratory:** Lab test ordering and results management — national lab ordering capability noted
- **Radiology/Imaging:** Imaging order entry and results
- **Progress Notes / Clinical Documentation:** Via VistA's Text Integration Utilities (TIU) — hundreds of "pre-built clinically proven templates" per Astronaut's marketing
- **Vital Signs:** Recording and tracking
- **Consults:** Requesting, tracking, and completing specialty consultations
- **Scheduling:** Enterprise scheduling for outpatient appointments; Admission/Discharge/Transfer (ADT) functions also noted
- **Demographics:** Patient demographic data management — (a)(5) certification
- **Family Health History:** Confirmed by (a)(12) certification
- **Implantable Device List:** Confirmed by (a)(14) certification
- **Clinical Decision Support (CDS):** Drug interaction checks and alerts — (a)(2), (a)(4)

**E-Prescribing:**
- Integrated e-prescribing through **Newcrop** and the **Surescripts** network
- **EPCS** (Electronic Prescribing of Controlled Substances) — Surescripts-certified
- This is a third-party integration with associated monthly costs ("Monthly Newcrop and the Surescripts network charge")

**Astronaut proprietary additions:**
- **Rocket Note:** Described as "very efficient follow-up notes and billing" — suggesting integrated clinical documentation and billing code capture
- **Turbo Supervision:** Mid-level provider supervision tools with "patient navigation capabilities" — designed for attending physicians supervising NPs/PAs
- **Astro-CPRS:** Enhanced CPRS interface with modern web technologies, improved typography, embedded graphics, and single sign-on

**Interoperability:**
- CCDA generation and exchange — (b)(1), (b)(3)
- FHIR R4 API — (g)(10) certified
- Patient access API — (e)(3) certified for patient electronic access to health information
- Direct messaging for transitions of care implied by (b)(1)/(b)(3)

**Quality Reporting:**
- Supports 16 Clinical Quality Measures (CQMs) per the disclosures page — (c)(1) certified
- QRDA reporting capability (the disclosures mention potential "hourly charge to assist training, preparing, and submitting QRQA to the government")

**Public Health:**
- Immunization registry transmission — (h)(1) certified

### Data & Content

Based on the certified criteria, vendor materials, and VistA's known architecture, Astronaut EHR stores/manages:

**Clinical data (well-documented):**
- Patient demographics (name, DOB, contact, insurance, identifiers)
- Problem/diagnosis lists
- Medication lists (active, historical, prescribed)
- Allergy and adverse reaction records
- Lab orders and results
- Radiology/imaging orders and results
- Vital signs
- Progress notes and clinical documentation (via TIU templates)
- Consult requests and notes
- Family health history
- Implantable device records
- Immunization records
- Encounter/visit data
- Clinical orders (CPOE)
- Drug interaction alerts and CDS data

**Scheduling/administrative data:**
- Appointment scheduling data
- ADT (Admission/Discharge/Transfer) records
- Patient-provider assignments

**E-prescribing data:**
- Prescriptions sent via Newcrop/Surescripts
- EPCS records for controlled substances

**Unclear/not well-documented:**
- **Billing:** The disclosures page and "Rocket Note" feature reference billing, but it's unclear how deep billing capabilities go. VistA's original architecture included billing modules (particularly for VA fee-basis and third-party billing), but whether Astronaut implements full practice management/billing or just captures billing codes during documentation is unclear. The vendor describes itself as having "billers" on staff, suggesting some billing support.
- **Patient portal:** The product is certified for (e)(3) — patient electronic access — but no standalone patient portal product is described on the website. It may be API-based access rather than a traditional portal.
- **Secure messaging:** No patient messaging capability is described on the vendor website.
- **Document imaging/scanning:** Not mentioned.
- **Referral management:** Consults are supported via VistA, but external referral tracking is not specifically described.
- **Audit logs and access records:** Required by (d)(1)–(d)(9) certification, so these exist but aren't marketed as a feature.

**Key observation:** Because Astronaut is built on VistA, the underlying database (MUMPS/FileMan) has a very large data dictionary — potentially hundreds of files/tables inherited from the VA's decades of development. The EHI export scope could be very broad if they expose the full VistA data model, or quite narrow if they only export the subset they've actively configured for ambulatory use.

---

## Research Gaps

- No third-party reviews found (G2, Capterra, KLAS, etc.) — the product's market presence appears too small for coverage on these platforms
- No detailed feature documentation or user manual found publicly
- Customer count and deployment scale are unknown beyond a handful of mentions
- The boundary between VistA's full module set and what Astronaut actually deploys/configures for customers is unclear
- Billing depth is ambiguous — somewhere between "billing code capture in notes" and "full practice management"
