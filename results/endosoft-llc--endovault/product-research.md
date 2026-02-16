# EndoSoft, LLC — Product Research

Researched: 2026-02-15
Developer website: https://www.endosoft.com/

## Overview

EndoSoft, LLC is a healthcare IT company founded in 1995 by Rakesh Madan and Manish Madan, headquartered in Schenectady, NY. The company specializes in EHR/EMR software designed specifically for **procedure-based specialties**, with its roots in endoscopy documentation and image capture. EndoSoft is a subsidiary of Utech Products Inc. and employs approximately 50–100 people.

EndoSoft claims over 100,000 clinical users worldwide across 100+ hospitals, with operations in 40+ countries including the US, UK, Germany, Australia, India, China, UAE, and Canada. The company maintains international offices in the Netherlands, the UK, Australia, India, China, Germany, and the UAE. Their primary market is endoscopy suites, ambulatory surgery centers, and procedure-focused specialty practices, though they have expanded into oncology and other specialties.

The company's product lineup includes EndoVault (the flagship certified EHR), Qlinical (a cloud-based EHR alternative), Argus AI (AI-powered documentation), and Approvon (a clinical vetting/workflow management application for the UK market). EndoVault is the ONC-certified product and the focus of this research.

## Product: EndoVault

CHPL IDs: 10854

### What It Is

EndoVault is an ONC-certified, multi-specialty EHR designed for procedure-focused medical specialties. While the product supports many specialties, its core strength and origin is in **gastroenterology/endoscopy** — it was originally built to capture and document endoscopic procedures with integrated imaging. The product has since expanded to support oncology, pulmonology, pain management, general surgery, orthopedics, OB/GYN, otolaryngology (ENT), urology, pathology, ophthalmology, dermatology, and cardiology.

The certified module appears to be the full EndoVault EHR platform, not a subset. The CHPL certification covers 41+ criteria spanning clinical documentation (a), transitions of care (b), clinical quality measures (c), security (d), patient portal (e), public health reporting (f), and API/FHIR access (g). Intended users per the certification are "Physicians, Nurses, Medical Technicians, Clerical Staff and Non-Clinical staff."

EndoVault runs on Microsoft SQL Server and Interbase database platforms. It is described as scope-manufacturer-neutral, working with Olympus, Pentax, Fujinon, Stryker, and other scope brands.

### Users & Market

EndoVault serves procedure-focused practices and facilities including:
- **Gastroenterology/endoscopy suites** (the primary market)
- **Ambulatory surgery centers (ASCs)**
- **Hospital-based endoscopy and procedure units**
- **Oncology clinics** (chemotherapy management, cancer registry)
- **Multi-specialty procedure practices**

Day-to-day users include gastroenterologists, endoscopists, oncologists, proceduralists, endoscopy nurses, medical technicians, scheduling/admitting staff, and practice managers. The ENR (Electronic Nursing Record) module is specifically designed for procedural nursing workflows.

Notable customers include McGill University's Segal Cancer Centre and Queen Elisabeth Hospital (UK). In Australia, EndoVault integrates with the National Bowel Cancer Screening Program (NBCSP) and the National Cancer Screening Register (NCSR).

On Capterra, EndoVault has a 4.0/5 rating based on 1,284 reviews. Users praise its flexibility for endoscopy documentation; one reviewer called it "the best system I have used in the 7 Endoscopy units I have worked in over the last 6 years." SoftwareFinder shows a lower 3/5 based on only 2 reviews.

### Modules & Functionality

EndoVault is a modular system with the following components described across vendor materials:

**Scheduling & Admitting (EndoVault Scheduler)**
- Multi-provider, multi-facility appointment scheduling
- Procedure-type-based slot allocation with training/fellow time accommodations
- Recall management with automated reminders (text, email, phone)
- Role-based access for scheduling staff
- Integration with ADT feeds from hospital information systems

**Consultation & Office Visits**
- Consult reports and progress notes
- Patient history, diagnoses, medications documentation
- Specialty-specific clinical templates with rich vocabulary
- Physician dashboard with real-time workflow visibility

**Procedure Documentation & Report Writing**
- Real-time procedure documentation with customizable templates
- HD image capture (up to 4K) in BMP, JPEG, TIF, DICOM formats
- Simultaneous capture of up to 4 video signals (AVI format, up to 4K)
- Supports HDMI, HD/SDI, DVI, S-video, RGB, AV, composite connections
- Natural language processing dictation via Argus AI during procedures
- Specialty-specific findings documentation (e.g., polyp detection, cecal intubation, bowel prep scores)

**Image Management & PACS**
- Integrated PACS with DICOM-compliant storage
- Vendor-neutral — works with all major scope manufacturers
- Accelerated image retrieval across multiple sites
- Image compression and server backup
- HL7 and DICOM visible light worklists and storage
- Encapsulated PDF support

**Electronic Nursing Record (ENR)**
- Automatic vital sign recording interfaced with vital sign monitors
- Medication administration documentation during procedures
- Medication reconciliation integrated with EHR
- Patient tracking across waiting areas, exam rooms, procedure rooms, recovery beds
- Intra-procedure data: intubation, IV assessment, sedation scores
- Post-procedure data: pain scales, adverse events, consciousness levels, discharge status
- SGNA and AORN nursing dataset compliance
- RFID/barcode scanning for inventory and scope tracking

**E-Prescribing (EndoVault Rx)**
- Surescripts-certified electronic prescribing

**Computerized Provider Order Entry (CPOE)**
- Order entry for medications, labs, imaging
- Drug interaction checking

**Patient Portal & Mobile App**
- Patient access to medical questionnaires and forms
- Laboratory test results access
- Electronic messaging with providers
- (Detailed portal feature set not extensively documented on the website)

**Pathology Module**
- Pathology requisition — automatic patient info and tissue sample submission to lab
- Pathology results handling

**Oncology-Specific Modules**
- Cancer staging with TNM classification and ICD-O-3 coding
- Chemotherapy management: automated dose calculations (BSA, AUC, BMI, creatinine, GFR)
- Prebuilt chemotherapy order sets by specialty
- Radiation therapy ordering (fractions, dosage, treatment sites)
- Medication administration records (MAR) for chemo
- Pre/post-chemotherapy medication management
- Adverse reaction tracking and lifetime medication restrictions
- Tumor board coordination
- Cancer registry interfacing and data submission
- Patient consent management for clinical trials
- Palliative care and recall management

**Inventory & Scope Management**
- RFID/barcode-based inventory tracking
- Scope tracking for infection prevention
- Time and material billing (tracks items used, procedure/recovery room utilization)

**Reporting & Analytics**
- 150+ prebuilt reports
- Customizable reporting and data query tools
- Discrete data stored for operational and clinical reporting
- ES Reporting Tool for extracting quality/safety outcomes to Excel/CSV
- Registry submissions: GIQuIC, AGA, MIPS/MACRA, CDC, NBCSP/NCSR (Australia)

**Quality Measures**
- Polyp detection rates, adenoma detection rates
- Cecal intubation rates, bowel prep scores (Boston scale)
- Specimen collection and biopsy documentation
- CMS, TJC, AGA, ASGE, ACG compliance

**Public Health Reporting**
- Immunization registries (f)(1)
- Syndromic surveillance (f)(2)
- Electronic case reporting (f)(3)
- Cancer registry (f)(4)–(f)(7) transmission

**Interoperability**
- HL7 and FHIR interfaces
- Integration with major EHR/HIS systems (Epic, Cerner, McKesson, Meditech)
- Epic Lumens integration (standalone image capture)
- ADT, scheduling, orders, query from HIS
- Results, pathology, billing, room/inventory utilization messages outbound
- Electronic signatures (signature pad for consent and procedure sign-offs)
- Multi-language support with translated reports

### Data & Content

Based on vendor materials and the feature descriptions above, EndoVault stores and manages the following categories of data:

**Clinical Data**: Patient demographics, medical history, allergies, medications, problem lists, diagnoses (ICD-O-3, TNM staging for oncology), vital signs (automatically captured from monitors), procedure findings, clinical assessments, progress notes, consult reports, discharge summaries.

**Procedure Documentation**: Detailed procedure reports with findings (e.g., polyp characteristics, cecal intubation, bowel prep quality), intra-procedure nursing documentation (sedation scores, IV access), post-procedure observations (pain, consciousness, adverse events).

**Images & Video**: Still images (BMP, JPEG, TIF, DICOM) and video recordings (AVI, up to 4K) from endoscopic and other procedures, stored in integrated PACS with DICOM compliance. This is a core data type for this product — it was originally built around endoscopy image capture.

**Orders**: CPOE data for medications, labs, and imaging. Chemotherapy orders with dosing calculations, cycle tracking, and medication administration records.

**Prescriptions**: Electronic prescriptions via Surescripts integration.

**Pathology**: Pathology requisitions and results, tissue sample tracking.

**Scheduling**: Appointment data, recalls, multi-provider/multi-facility schedules, patient admitting information.

**Patient Portal Data**: Patient-submitted questionnaires and forms, electronic messages between patients and providers, lab results shared with patients.

**Inventory & Equipment**: Scope tracking data (infection prevention), RFID/barcode inventory records, time and material billing data (items used per procedure, room utilization).

**Quality Metrics**: Registry data for GIQuIC, AGA, MIPS/MACRA, CDC, NBCSP. Adenoma detection rates, polyp detection rates, bowel prep scores, and other quality indicators.

**Billing Data**: Time and material billing is integrated in the ENR module, tracking items used and room utilization. However, full practice management/billing appears to be handled via interfaces with external billing systems — the vendor website states EndoSoft "has interfaced with all billing and scheduling software vendors for all major Hospital Information systems." This suggests billing claims processing is **not** built into EndoVault itself, but billing data (charges, items, time) is generated within the system and transmitted outbound.

**Audit/Compliance**: Audit trails documenting all chart modifications, electronic signatures for consent and procedure sign-offs, multi-factor authentication logs.

**Oncology-Specific Data**: Cancer staging, chemotherapy regimens and cycles, radiation therapy orders, adverse reaction histories, lifetime medication restrictions, tumor board records, clinical trial consent, cancer registry submissions.

**Notable Gaps/Uncertainty**: The vendor website does not describe a built-in full practice management or revenue cycle management system. Billing appears limited to time-and-materials tracking within procedures, with claims/revenue cycle handled externally. The patient portal feature set is only lightly documented — it exists but its full scope is unclear.

---
