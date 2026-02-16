# Varian Medical Systems — Product Research

Researched: 2026-02-16
Developer website: https://www.varian.com/oncology/products/software (redirects to https://cancercare.siemens-healthineers.com)

## Overview

Varian Medical Systems is a major radiation oncology technology company, historically known for manufacturing linear accelerators (linacs) and radiation therapy treatment planning systems. Founded in 1948 and headquartered in Palo Alto, California, Varian was acquired by Siemens Healthineers in April 2021 for $16.4 billion. Varian continues to operate as a brand within Siemens Healthineers, and its oncology software products are now marketed under both the Varian and Siemens Healthineers Cancer Care brands (the varian.com domain redirects to cancercare.siemens-healthineers.com for software product pages).

Varian's primary software product is the ARIA Oncology Information System, an oncology-specific EMR/EHR that manages radiation, medical, and surgical oncology information. ARIA is the leading best-of-breed oncology information system (OIS) in the US market by revenue. According to Enlyft, approximately 369 organizations use ARIA, with 85% in the United States, 65% in the hospital & healthcare sector, and 59% being large organizations with over 1,000 employees. Varian's customers include major academic medical centers and health systems — a 2024 deal with Ballad Health for a 10-year oncology collaboration included ARIA CORE as a key component.

The intended users listed in the ONC certification are: "Registered nurses, nurse practitioners, therapist, medical doctors" — reflecting the clinical staff in radiation and medical oncology departments.

## Product: ARIA CORE

CHPL IDs: 11719

### What It Is

ARIA CORE (v18.3, certified 2025-11-26) is the current-generation oncology management system from Varian, replacing the legacy ARIA Oncology Information System. It is described as a modernized platform "built for and by oncology experts" that brings together capabilities from the legacy ARIA OIS with new features. ARIA CORE is designed as a comprehensive, oncology-specific electronic health record that combines radiation oncology, medical oncology, and surgical oncology information into a single workspace.

The certified module — ARIA CORE — is a full oncology information system, not a component of a larger general-purpose EHR. However, it is designed to integrate with hospital enterprise EHRs (like Epic or Cerner) in a hybrid approach. For example, Duke University Health System implemented ARIA alongside their enterprise EMR, using ARIA for radiation oncology-specific data and workflows while the enterprise system handled general clinical data. Providers accessed both systems simultaneously via Citrix, creating a "virtual radiation oncology chart."

ARIA CORE is part of a broader Varian/Siemens software ecosystem that includes:
- **Eclipse** — treatment planning system for radiation therapy
- **Noona** — patient engagement/patient-reported outcomes platform
- **ARIA CORE Insights** — cloud-native analytics platform
- **ARIA CORE Mobile** — iOS mobile app for clinicians
- **ARIA Systemic Therapy Management (STM)** — cloud-native module for chemotherapy/drug ordering
- **EQUICARE CS** — survivorship management solution for post-treatment care

### Users & Market

**Who uses it day-to-day:**
- Radiation oncologists (prescribing radiation therapy, reviewing treatment plans and images)
- Medical oncologists (prescribing chemotherapy/systemic therapy, managing medical oncology workflows)
- Medical physicists and dosimetrists (treatment planning QA, chart checks, patient setup verification)
- Radiation therapists (daily treatment delivery, image acquisition)
- Registered nurses and nurse practitioners (patient assessment, documentation, chemotherapy administration)
- Administrative/scheduling staff (patient scheduling, resource management)
- Billing staff (charge capture, RVU tracking)

**Clinical settings:**
- Hospital-based radiation oncology departments
- Freestanding cancer centers
- Academic medical centers (e.g., Duke)
- Community health systems (e.g., Ballad Health)
- Multi-site oncology networks

**Market position:**
ARIA holds the leading position among best-of-breed oncology information systems in the US. About 369 organizations use it (per Enlyft). The user base skews heavily toward large institutions — 55% of customers have annual revenues over $1 billion. Varian/Siemens competes in the oncology IT space with Elekta's MOSAIQ and general-purpose EHR vendors that have oncology modules.

### Modules & Functionality

Based on vendor materials, third-party reviews, and the published literature, ARIA CORE includes the following functional areas:

**Clinical Documentation & Patient Records:**
- Oncology-specific EMR with electronic documentation, e-signatures, and audit trails
- Customizable templates for clinical notes
- Problem lists, allergy tracking, medication management
- Review of systems (RoS) and physical examination (PE) documentation with automated transcription
- Consultation reports, weekly treatment check notes, treatment summaries

**Radiation Therapy Management:**
- Treatment planning orders and radiation therapy prescriptions
- Treatment plan review and approval workflows
- Daily treatment logs and therapy records
- On-treatment image review (MV, kV, CT, CBCT, MR, PET)
- Image comparison using automatic, manual, or fiducial marker matching
- Quality assurance reports and chart checks
- 2D/electron calculations
- Integration with Eclipse treatment planning system
- Support for proton therapy in addition to photon/electron

**Medical Oncology / Systemic Therapy:**
- Chemotherapy and drug ordering with access to 300+ disease-specific regimens
- Drug interaction checking
- Systemic Therapy Management (STM) module — a newer, cloud-native add-on for the full systemic therapy workflow from treatment management plans through medication administration
- Lab result review with trend graphing
- Vital signs tracking
- Toxicity and adverse event documentation using oncology-standard grading scales

**Cancer Staging & Decision Support:**
- Automated cancer staging based on AJCC guidelines
- Rule-based clinical decision support embedded in workflows
- Disease response documentation and tracking
- Partnership with OncoLog Cancer Registry for treatment analysis

**Scheduling & Resource Management:**
- Patient, staff, and resource scheduling
- Appointment management
- Task management and workflow routing

**Imaging & PACS:**
- Integrated image management for multi-modality oncology images
- DICOM-compliant image import/export
- Radiographic, fluoroscopic, and cone-beam CT image viewing
- Image archiving in DICOM or XML format

**Billing & Financial:**
- Charge posting with relative value unit (RVU) tracking
- Split technical and professional charges
- Charge export to HL7-compliant billing software
- Process tracking and productivity analysis
- The EMRSystems review notes ARIA partners with "Unlimited Systems' Centricity Physician Office" for practice management needs, suggesting billing may be partially handled by third-party integrations in some deployments

**Patient Portal & Engagement:**
- Certified for (e)(1) — patient view, download, transmit
- Integration with Noona patient engagement platform for patient-reported outcomes
- Mobile app (ARIA CORE Mobile) for clinician access to patient data, scheduling, document approvals, note dictation, lab results, vital signs

**Interoperability & Data Exchange:**
- HL7 interface support for real-time or scheduled data sharing
- DICOM compliance
- FHIR API access — certified for (g)(7) through (g)(10)
- Direct messaging — certified for (h)(1)
- Transitions of care — certified for (b)(1) through (b)(3)
- Clinical trial management capabilities

**Survivorship:**
- Integration with EQUICARE CS for post-treatment survivorship care management

### Data & Content

Based on vendor documentation, the implementation literature, user reviews, and certification criteria, ARIA CORE manages the following categories of data:

**Patient demographics and registration data** — standard patient identification information.

**Clinical notes and documentation** — consultation reports, weekly treatment check notes, treatment summaries, review of systems, physical exams, all with electronic signatures and timestamps.

**Treatment plans and prescriptions** — radiation therapy prescriptions, chemotherapy regimens, treatment planning data, dose distributions.

**Daily treatment records** — logs of each radiation therapy fraction delivered, including machine parameters.

**Medical images** — MV portal images, kV images, CBCT scans, CT simulation images, MR images, PET images. Stored in DICOM format.

**Lab results** — laboratory test results with trend tracking and graphing capabilities.

**Vital signs** — vital signs data with trending.

**Medications** — drug orders, chemotherapy regimens (300+ built-in), drug interaction data.

**Problem lists and diagnoses** — including automated AJCC cancer staging data.

**Allergies** — patient allergy information.

**Quality assurance data** — QA reports, chart check records, treatment plan verification data.

**Toxicity/adverse event records** — using oncology-standard grading scales.

**Disease response data** — tracking treatment outcomes and disease progression.

**Scheduling data** — appointments, resource utilization, task assignments.

**Billing/charge data** — RVU-based charges, technical/professional charge splits.

**Patient-reported outcomes** — via Noona integration.

**Survivorship care plans** — via EQUICARE CS integration.

**What's notably absent or unclear:**
- ARIA is not a general-purpose EHR — it does not appear to manage primary care, general surgery, or non-oncology specialty data. It is designed to coexist with a hospital's enterprise EHR.
- The system does not appear to include its own e-prescribing (Surescripts) integration — the certification criteria do not include (b)(3) for e-prescribing. Update: the criteria *do* include (b)(3) electronic prescribing, so some e-prescribing capability exists.
- Billing appears to be partially built-in (charge capture and RVU tracking) but full practice management/claims may rely on third-party integrations in some deployments.
- The website does not describe robust referral management, prior authorization, or revenue cycle management capabilities — these may be handled by the enterprise EHR or separate systems.

---
