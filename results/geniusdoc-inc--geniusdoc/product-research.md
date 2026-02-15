# GeniusDoc, Inc. — Product Research

Researched: 2026-02-14
Developer website: https://geniusdoc.com/

## Overview

GeniusDoc, Inc. is a small, privately held health IT company based in Santa Monica (Los Angeles), California. The company markets a fully integrated EHR and practice management system "designed by physicians for physicians," with a primary focus on **hematology/oncology** practices, though it also serves other specialties. The company was founded by CEO Sunil Nemani and lists a contact named Bosco Fernando. GeniusDoc appears to be a very small operation — one source (ZoomInfo, not directly verified) lists approximately $6.1M in revenue and a very small employee count, though exact figures are uncertain.

The product is developed in partnership with (or by) **B2B Software Technologies Ltd**, a publicly traded company on the Mumbai Stock Exchange since 1998, headquartered in Hyderabad, India. B2B Software Technologies is a Microsoft Gold certified partner. The exact nature of the relationship is unclear — B2B Software Technologies' own website lists GeniusDoc as part of their healthcare suite, and the EMR Industry listing identifies B2B Software Technologies as the developer. GeniusDoc, Inc. appears to be the US-based entity that markets and certifies the product.

GeniusDoc targets small-to-midsize ambulatory physician practices, particularly oncology and hematology groups. The CHPL metadata's SED description confirms the intended users are "healthcare providers in private practices." The product is certified as ambulatory practice management software.

## Product: GeniusDoc

CHPL ID: 10745

### What It Is

GeniusDoc is a fully integrated EHR + Practice Management + Revenue Cycle Management system with a patient portal. It is an ambulatory-focused system targeting physician practices, especially hematology/oncology. The certified module (GeniusDoc 12.0, certified December 2021) appears to be the whole product — a single integrated platform covering clinical documentation, billing, scheduling, e-prescribing, patient portal, and specialty-specific oncology workflows.

The product has a broad certification footprint: 42 criteria spanning clinical data (a)(1)-(a)(15), transitions of care (b)(1)-(b)(3), clinical quality measures (c)(1)-(c)(4), patient portal/VDT (e)(1)-(e)(3), public health reporting (f)(1)-(f)(5), FHIR APIs (g)(7)-(g)(10), and immunization registry (h)(1). This is a comprehensive ambulatory EHR certification.

The system runs on a Windows Server/SQL Server architecture (on-premise), with specifications scaling from 1–10 users up to 151–200 users. It also has a web-based/browser access mode. Required dependencies include Surescripts (for e-prescribing) and "Best Sync."

### Users & Market

- **Primary users**: Physicians, nurses, physician assistants, billing staff, and practice administrators at ambulatory private practices
- **Specialty focus**: Hematology/oncology is the flagship specialty, with deep oncology-specific features (chemotherapy management, cancer staging, tumor markers). The vendor also references gastroenterology-specific features on the billing page, suggesting multi-specialty customizations
- **Practice size**: "Ideal for smaller and middle size practices" per the EMR Industry listing
- **Deployment**: On-premise Windows Server deployment with remote access capabilities; also mentions browser-based access
- **Customer count**: Not publicly disclosed. The vendor appears to be a small niche player — no mention of large customer counts, and the company does not appear on major market share lists like KLAS or Definitive Healthcare rankings
- **Integration partners**: Updox (communications/fax management, partnered 2016), Gateway EDI (claims clearinghouse), Surescripts (e-prescribing), Dragon NaturallySpeaking (voice recognition)
- **Mobile**: GDMobile app mentioned on the website

### Modules & Functionality

Based on vendor website pages and third-party sources, GeniusDoc includes the following modules and capabilities:

**Clinical Documentation (Point of Care)**
- SOAP-formatted patient charts with vertically organized hierarchy
- Point-and-click encounter documentation for office visits, telephone encounters, workers' comp cases, hospital visits
- Documentation by physicians, nurses, and physician assistants
- Physical exam designer with dynamic customizable templates (head-to-extremities)
- Past medical history, problem lists, allergy lists, medication lists
- Vital signs recording and tracking
- Smoking status documentation
- Clinical decision support
- Health maintenance/preventive care alerts based on age, sex, clinical factors
- Immunization tracking and management
- Patient-specific education resources
- Image capture — imports diagnostic and procedure-generated images into patient charts
- Audio/video file storage in patient charts
- Telephone triage with standardized care paths converted to progress notes
- Correspondence templates (referral letters, vaccination notes, workers' comp reports)

**Chemotherapy/Oncology Module** (described in detail on Chemo.html)
- Chemotherapy regimen library organized by disease and stage
- Regimen builder for practice-specific customization
- Automatic BSA, AUC, ANC calculations
- Dose limits and cumulative dose tracking
- Dose adjustment before order processing with historical dose tracking
- Chemotherapy administration documentation (IV, VAD, blood products, vesicants)
- Oncology nurse documentation for chemo administration and symptom management
- Vital signs, IV flow rate monitoring
- TNM cancer staging (Sixth Edition, AJCC)
- Tumor marker tracking with graphical display
- Lab test results in graphical format for trend analysis
- Treatment calendar integrated with scheduling
- Wave scheduling for multi-appointment treatment regimens
- Conflict checking and resolution for treatment scheduling

**Prescribing / Medication Management**
- Comprehensive drug database with dosage, interactions, adverse reactions, contraindications
- Drug-drug interaction screening
- Drug-allergy interaction screening
- Drug recall alerts
- Simple and complex prescriptions (IV, sequenced)
- Dose calculators (BSA, BMI, creatinine clearance)
- Batch prescription generation
- Electronic prescribing via Surescripts (ERX Gold certified)
- Drug formulary checks

**Lab / Orders**
- Computerized provider order entry (CPOE)
- One-touch order entry for tests and procedures
- Orders categorized by test type (CTs, MRIs, ultrasounds, blood panels) and specialty
- Preferred laboratory facility designation
- Electronic lab result integration into patient records
- Lab result trend analysis and annotation
- Lab order and specimen tracking (COLA compliance)

**Billing & Revenue Cycle Management**
- Integrated billing at point of care
- Automated charge posting
- Claims generation and electronic submission (HIPAA compliant)
- CPT and ICD code resources with automated E&M code suggestions
- Specialty-specific code filtering (gastroenterology mentioned specifically)
- Automatic modifier assignment
- Electronic remittance advice processing
- EOB reason and remark code tracking
- Rules-based adjustment posting, balance transfers, charge dispute management
- Batch posting of billable procedures
- "99% first pass through" rate claimed
- Automated appeals features
- Secondary claims processing via Gateway EDI
- Revenue cycle management described as fully integrated

**Healthcare EDI / Claims Processing**
- Partnership with Gateway EDI
- Electronic claims submission to 3,000+ payers
- 24/7 transaction processing
- Remittance notifications
- All-electronic secondary claim processing
- HIPAA compliant, EHNAC accredited

**Document Management**
- Scanned document storage and retrieval with predefined folders
- Referral letters, discharge summaries, radiology images, procedure photos
- Incoming/outgoing fax transmission (integration with E-Fax, SilentFax, Microsoft Fax)
- Document commenting and user assignment with multi-level security
- Paperless office workflow

**Scheduling**
- Appointment scheduling (mentioned across multiple pages)
- Real-time patient tracking
- Treatment calendar for chemo regimens
- Wave scheduling for oncology
- Conflict checking

**Patient Portal** (certified for (e)(1)-(e)(3))
- Patient access to health information (view, download, transmit)
- Patient engagement features (implied by certification criteria)

**Care Coordination**
- Chronic Care Management (CCM) module mentioned on website
- Oncology Care Model (OCM) support mentioned on website
- Clinical information exchange
- Continuity of Care Records (CCR)
- Medication reconciliation
- Patient summary records

**Quality Reporting**
- MIPS/Promoting Interoperability quality measures
- PQRS data extraction and registry reporting
- QOPI (Quality Oncology Practice Initiative) reporting
- 43 ambulatory clinical quality measures certified
- Automated measure calculation and submission

**Public Health Reporting** (certified for (f)(1)-(f)(5))
- Immunization registry submission
- Public health surveillance
- Syndromic surveillance
- Cancer registry reporting (implied by (f)(5) certification)

**Interoperability / APIs**
- FHIR API access (certified for (g)(7)-(g)(10))
- HL-7 transcription interface
- Interfaces with hospitals, commercial labs, inventory systems
- Continuity of Care Document exchange

**Security & Administration**
- Role-based access control
- Emergency access provisions
- Automatic log-off
- Audit logging
- Multiple levels of encryption
- Off-site data backup and disaster recovery
- Module-based security

### Data & Content

Based on the features documented across vendor pages, GeniusDoc stores and manages the following types of data:

**Clinical data**: Patient demographics, encounter notes (SOAP format), problem lists, medication lists, allergy lists, vital signs, smoking status, immunization records, lab results, imaging orders/results, clinical summaries, care plans, referral letters, discharge summaries, progress notes

**Oncology-specific data**: Chemotherapy regimen details, treatment calendars, dose calculations (BSA, AUC, ANC), cumulative dose tracking, cancer staging (TNM), tumor markers, chemo administration records (IV flow rates, blood products, vesicants), oncology nurse assessments, treatment outcomes

**Prescribing data**: Prescriptions (simple and complex), drug interaction screening results, formulary data, e-prescribing transactions via Surescripts

**Billing/financial data**: Charges, claims, CPT/ICD codes, E&M codes, modifiers, EOB data, remittance advice, payment posting, adjustment records, accounts receivable, secondary claims

**Documents**: Scanned documents, faxes (incoming/outgoing), referral letters, correspondence, diagnostic images, procedure photos, audio/video files

**Scheduling data**: Appointments, treatment calendars, patient flow/tracking

**Quality/reporting data**: MIPS measures, PQRS data, QOPI measures, clinical quality measures, public health reports, immunization registry submissions, cancer registry data

**Patient portal data**: Patient-facing health information (view/download/transmit), patient engagement records

**Administrative/audit data**: Access logs, audit trails, user security roles, backup records

The vendor's website does not explicitly mention patient messaging/secure messaging as a built-in feature — communication capabilities were added via the Updox integration (2016), which handles messages, documents, and faxes. It's unclear whether messaging data resides within GeniusDoc or within Updox's platform.

The billing page's mention of gastroenterology-specific code filtering suggests the product has specialty-specific customizations beyond oncology, but the depth of non-oncology specialty features is not well-documented on the website.

---

## Research Notes

- GeniusDoc is a small, niche vendor — web presence is limited and some pages return 404 errors
- The relationship between GeniusDoc, Inc. (US entity) and B2B Software Technologies Ltd (India-based developer) is not fully transparent from public sources
- No third-party reviews were found on major platforms like G2 or Capterra; SoftwareSuggest had only 2 reviews
- The vendor does not appear in major market share databases (KLAS, Definitive Healthcare) suggesting a very small install base
- Some website content appears dated (references to Windows Server 2008, SQL Server 2008, Office 2010)
- The SoftwareSuggest listing had potentially inaccurate company metadata (listing headquarters as Hyderabad, which is the B2B Software Technologies office, not the GeniusDoc, Inc. office)
