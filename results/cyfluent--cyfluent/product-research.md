# Cyfluent — Product Research

Researched: 2026-02-16
Developer website: https://www.cyfluent.com/

## Overview

Cyfluent is a cloud-based Electronic Health Record (EHR) platform developed, operated, and owned by Planned Systems International (PSI), a leading provider of mission-focused national security, health IT, clinical, training, and environmental services to the U.S. Federal Government. Cyfluent is headquartered in Arlington, VA (3717 Columbia Pike) with additional offices in San Antonio, TX and Columbia, MD, and international presence in Ho Chi Minh City (Vietnam) and Shanghai/Hangzhou (China). The company was founded in 2009. CEO is Terry Lin; Elaine Law serves as VP of Operations.

Cyfluent is a small, niche vendor primarily focused on the federal government and small ambulatory practices. The product is used by 150+ clinical practices across the U.S. and is notably the system of record for HRSA's National Hansen's Disease (Leprosy) Program — one of the few commercial EHR systems with a Federal Authority to Operate (ATO). They hold a GSA IT Schedule 70 contract (with Health SIN), enabling federal procurement. The company has approximately 11 employees. Their clearinghouse has processed over $7B in claims and more than 125 million prescriptions have been transmitted through the platform. Cyfluent is EHNAC accredited (both HNAP and Cloud-Enabled Accreditation Program/CEAP) and deployed on Azure FedRAMP cloud with NIST SP-800-37 Risk Management Framework compliance.

Cyfluent describes itself as a Microsoft-based software development firm aiming to become "a global provider of Electronic Health Record (EHR) software as a service (SaaS) for medical communities and patients worldwide."

## Product: Cyfluent

CHPL IDs: 10072 (Version 3.2, certified 2019-08-13), 11546 (Version 3.3, certified 2024-12-11)

### What It Is

Cyfluent is a comprehensive, cloud-native outpatient EHR platform delivered as SaaS. It is not just an EHR module — it's a complete health services platform encompassing EHR, practice management, patient portal (PHR), telehealth, occupational health, health services management, and pharmacy fulfillment. The certified module appears to represent the whole product rather than a component of something larger.

The platform is built on a modular web services architecture, meaning components can be configured independently. Cyfluent describes this architecture as allowing "rapid component configurations and modifications to meet specific mission requirements/user needs" — with custom health workflows configurable within one to four weeks.

The product is broadly certified with 40+ ONC criteria spanning clinical data (a)(1)–(a)(15), transitions of care (b)(1)–(b)(9), EHI export (b)(10), patient access (e)(2)–(e)(3), public health (f)(1), (f)(4), (f)(5), and FHIR API access (g)(7)–(g)(10). SED intended users are described as "Outpatient Clinic."

### Users & Market

**Primary users**: Physicians, clinicians, nurses, billing staff, and practice managers in outpatient/ambulatory settings. Patients access the system through the PHR portal (CyPHR). The product also targets federal government health programs with specialized occupational health and health services management modules.

**Clinical settings**: Solo and small ambulatory practices (fewer than 3 physicians is the typical target), as well as federal health programs. Supports 8 medical specialties along with general family practice, urgent, and emergency ambulatory care. Explicitly mentioned specialties include cardiology, ophthalmology, podiatry, and pulmonology.

**Notable deployments**: The flagship deployment is HRSA's National Hansen's Disease (Leprosy) Program — the system serves as their EHR of record on Azure FedRAMP. The platform supports 150+ clinical practices across 13 states (EHR) and 21 states (practice management).

**Go-to-market**: Dual channel — direct sales to commercial practices (available online with "Buy Now" option) and federal government procurement via GSA IT Schedule 70 contract. Pricing starts at $49/month for entry-level, $199/month for certified EHR, $199/month for practice management, $395/month for professional suite.

### Modules & Functionality

The vendor's website describes five major service areas, each with detailed sub-capabilities:

**1. Electronic Health Record (EHR) System — CyCHART**
The EHR module, branded CyCHART, is described on the vendor's EHR detail page (cyfluent.com/services-7) with six functional areas:

- **Patient Management**: Patient summary page with configurable longitudinal data including Allergies, Prescriptions, Problems, Patient Health History, Family History, Personal Habits, Contacts, Patient Alerts, Body Measurements, previous Vitals, previous Encounters, Vision, and Quality Indicators. Supports complex medical community organization.
- **Clinic Processes**: Encounter documentation mimicking paper notes, all sections visible from one screen. Supports treatment pathways, chronic disease management, prescription management, CPOE, interoperable encounter documentation, clinical flowcharts, structured and unstructured medical notes, nutritional notes. Customizable templates that compose sentences/paragraphs from user selections. Multiple encounters can be opened simultaneously.
- **Lab Functions and Prescriptions**: Electronic orders and results management for prescriptions, labs, and procedures — all accessible from inside the encounter. eRX (branded CySCRIPT) with automated checks for drug contraindications, dosing alerts, and generics. Includes Electronic Prescribing for Controlled Substances (EPCS), DEA certified with two-factor authentication.
- **Telehealth**: Synchronous and asynchronous telehealth via PHR Portal. Can connect with remote home telehealth devices from vendors including Cardiocom, AMC, Authentidate, American Telecare, Bosch Healthcare, Visual Telecommunication Network, Viterion TeleHealthcare, and Qualcomm Life's 2net Platform.
- **Patient Records and Mobile App Interoperability**: Mobile app and PHR allow patients to manage medical information. Data integration technology supporting XML, HL7 FHIR, X.12, CCR, TXT, HTML, SQL, PDF, DICOM and other image formats. Supports clinical assessments, medication reconciliation, care plans, order management, Clinical Data Exchange (CDE), encounter documentation, physician web access, patient web access, and notes access. Can pull from devices including smart watches, portable sonograms, EKGs via Bluetooth, Wi-Fi, USB.
- **Custom Forms Builder**: Allows creating custom forms with discrete, reportable data for workflows not matching pre-existing templates.

**2. Practice Management — CyMED / CyfluentPM**
Described on the Practice Management detail page (cyfluent.com/copy-of-electronic-health-record-system):

- **Medical Billing**: Automated proof of filing, desktop payer status integration, real-time billing from integrated EHR, claims manager for A/R, single-button electronic claims submission through EHNAC-accredited clearinghouse (operated by Cyfluent themselves). Consolidated billing across multiple payers. Charge ledger displaying all patient billing information. Exit billing from scheduling window.
- **Appointment Scheduling**: Multi-provider, multi-location scheduling. Treatment program scheduling with benchmarks and decision points. Patient automated messaging (text/email) integration. Business rules for practice alerts.
- **Medical Resource Management**: Clinic supply chain and inventory management covering pharmaceuticals, medical supplies, medical equipment, medical gases, and biohazardous materials. RFID/barcode reader integration for large inventories. Inventory usage patterns associated with treatment patterns. Inventory alerts as business rules. Billing module handles purchasing.

**3. Occupational Health Management and Compliance System**
Described on the Occupational Health detail page (cyfluent.com/copy-of-practice-management):

- Record of work-related injuries and illnesses (OSHA compliance), integrating with the employee's complete longitudinal medical history
- Adaptive forms for standard and custom metrics on specific injuries/illnesses
- Hearing and other exams required by OSHA standards
- Annual posting of injury and illness summary data (continuous integration of examination results)
- 24-hour OSHA workplace fatality notification with compliance forms and deadline alerts
- Workplace medical records for employees (OSHA-compliant, HIPAA/Privacy Act compliant)
- OSHA recordkeeping and reporting requirements with multi-vector indexing and graphing

**4. Health Services Management System**
Described on the Health Services Management detail page (cyfluent.com/copy-of-occupational-health-management):

- **Medical Evacuation**: Supports personnel deployed at remote locations needing return for medical conditions, with configurable assessment procedures and evacuation protocols
- **Medical Clearance for Travel**: Examination and approval for deployment to higher-risk environments, automatic completion of approval checklists by travel location
- **Travel Immunization**: Integration of immunization records with travel requirements by global region
- **Mental Health and Substance Abuse**: Configurable evaluation templates for job-related mental health and substance abuse metrics, with data separated from EHR data per behavioral health regulations

**5. Pharmacy Fulfillment**
Described on the Pharmacy Fulfillment detail page (cyfluent.com/copy-of-health-services-management-sy):

- **Shipping**: Pharmacy shipping services with tracking, labeling, temperature-controlled packaging for sensitive medications
- **Inventory**: Pharmacy inventory management with stock control and supply chain optimization
- **Barcodes**: Barcode technology for medication tracking, dispensing accuracy, and verification

**Named sub-products**:
- **CyCHART**: EHR/charting module
- **CySCRIPT**: E-prescribing module
- **CyMED**: Practice management software
- **CyPORTAL**: Patient portal
- **CyCLAIMS**: Claims management
- **CyPHR**: Personal Health Record (patient-facing portal at cyfluentphr.com)

### Data & Content

Based on vendor materials, the product stores and manages the following types of data:

**Clinical data** (per EHR detail page and product pages):
- Patient demographics and contact information
- Allergies
- Prescriptions / medication lists (including controlled substances)
- Problem lists
- Patient health history
- Family history
- Personal habits (social history)
- Patient alerts
- Body measurements
- Vitals (current and historical)
- Encounters / visit documentation (structured and unstructured notes)
- Vision data
- Quality indicators
- Clinical flowcharts
- Nutritional notes
- Lab orders and results
- Procedure orders
- CPOE orders
- Drug interaction/contraindication data
- Chronic disease management data
- Clinical assessments
- Care plans
- Medication reconciliation records
- Immunization records (explicitly for travel immunizations)
- Custom form data (discrete, reportable)

**Practice management / financial data** (per PM detail page):
- Appointment scheduling data (multi-provider, multi-location)
- Billing/charge data (charge ledger)
- Insurance claims (electronic claims via their own clearinghouse)
- Electronic remittance
- Insurance verification records
- A/R management data
- Payer status information
- Proof of filing records

**Patient-generated / portal data** (per PHR and telehealth pages):
- Patient-managed health records via CyPHR
- Patient messages (automated text/email from scheduling)
- Telehealth encounter data (synchronous and asynchronous)
- Remote device data (vital signs from home telehealth devices, smart watches, EKGs, portable sonograms)

**Occupational health data** (per Occupational Health page):
- Work-related injury and illness records (OSHA-compliant)
- OSHA examination results
- Workplace fatality notification records
- Employee workplace medical records
- Hearing exam data and other OSHA-mandated exams

**Health services management data** (per Health Services page):
- Medical evacuation assessment and protocol records
- Medical travel clearance records
- Travel immunization records linked to global requirements
- Mental health and substance abuse evaluation data (separated per behavioral health regulations)

**Pharmacy data** (per Pharmacy Fulfillment page):
- Pharmacy inventory data
- Medication shipping/tracking records
- Barcode/medication verification data

**Interoperability/exchange data** (per Patient Records page):
- DICOM images
- CCD/CCR documents
- HL7 FHIR resources
- X.12 transactions
- Clinical Data Exchange (CDE) records

**What's unclear**: The website doesn't explicitly mention document scanning/storage, fax integration, or internal messaging between providers, though an earlier search result mentioned "instant messaging" as a component. The depth of imaging support (beyond DICOM format mention) is not detailed. The relationship between the commercial product sold to small practices and the federal deployment capabilities (occupational health, medical evacuation, pharmacy fulfillment) is not entirely clear — it's possible these specialized modules are primarily used in federal contracts rather than by typical small-practice customers.

---
