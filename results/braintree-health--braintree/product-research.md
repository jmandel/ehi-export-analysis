# Braintree Health — Product Research

Researched: 2026-02-14
Developer website: https://www.braintreehealth.com

## Overview

Braintree Health (also known as Braintree LLC) is a small healthcare technology company founded in 2004, headquartered in Corpus Christi, Texas. The company develops the Braintree Medical Workflow (BMW) Platform, an integrated software suite designed primarily for outpatient procedure centers, ambulatory surgery centers, vascular access centers, and specialty clinics. The company also operates under the name "NephroPACS" (nephropacs.com redirects to braintreehealth.com), suggesting origins in or strong ties to nephrology/vascular access imaging.

Braintree has two business divisions: **Braintree Products** (direct software sales to healthcare facilities in the US and Canada) and **Braintree Operations** (IT and billing management services for outpatient procedure centers). This dual model means the company both sells software and operates as a managed services provider for billing and IT. The contact listed on the CHPL certification is Sunil Reddy, and the support email uses the domain braintreemd.com. The company appears to be a small/niche vendor — no employee count or customer numbers are published, and no third-party reviews were found on G2, Capterra, or Software Advice (search results for "Braintree" on these sites return only PayPal Braintree, an unrelated payment processor).

## Product: BRAINTREE (BMW Platform)

CHPL ID: 10727
Version: 10.5.1.1
Certification Date: 2021-11-19

### What It Is

The BRAINTREE product is the BMW (Braintree Medical Workflow) Platform — described as "an intranet, web-based medical workflow software application that combines all the functions of every department in a medical facility into one complete package." It is a broadly certified ambulatory EHR with 49 certified criteria spanning clinical data management (a)(1)-(a)(15), transitions of care (b)(1)-(b)(3), patient portal (e)(1)-(e)(3), public health reporting (f)(1)-(f)(7), FHIR API (g)(10), and clinical quality measures (c)(1)-(c)(4). The SED description states it "supports a variety of healthcare professional roles (e.g., Nurses, Medical Assistants, Physicians, etc.) across a variety of healthcare practices (e.g., Family Practice, Vascular, Interventional Radiology, etc.)."

Unlike many ambulatory EHRs that focus purely on clinical documentation, the BMW Platform is distinguished by its deep integration of imaging (PACS/RIS), inventory management, and procedure-oriented workflow — reflecting its core market in outpatient procedure and surgery centers rather than primary care offices.

### Users & Market

**Target settings:**
- Vascular access centers (appears to be the primary/origin market)
- Ambulatory surgery centers
- Outpatient procedure centers
- Interventional radiology centers
- Pain management centers
- Imaging/cath labs
- Orthopedic centers
- Behavioral health clinics
- Hospitals (marketed but unclear how many hospital deployments exist)

**End users:** Physicians, nurses, medical assistants, billing staff, supply clerks, receptionists, and practice managers. The system is designed to serve every department in a medical facility.

**Market size:** Unknown. No customer counts, user numbers, or notable customer references are published on the website. No third-party reviews were found. The company is likely a small niche vendor serving a limited number of procedure-oriented facilities. The dual "Products" and "Operations" business model suggests a hands-on, managed-services relationship with customers rather than large-scale software distribution.

**Geography:** US and Canada (per vendor website).

### Modules & Functionality

The BMW Platform consists of five integrated modules plus supporting capabilities:

**BT Scheduler** — Appointment scheduling with electronic calendar, multi-doctor and multi-hospital scheduling support, daily/weekly/monthly views, patient admission workflow integration. Links to EMR and imaging worklists.

**BT RIS (Radiology Information System)** — Web-based database for radiology procedure information. Manages patient scheduling, procedure tracking, results reporting, and film tracking. Integrates with BT PACS for image management.

**BT PACS (Picture Archive Communication System)** — Medical imaging management with FDA-approved viewer. Handles image acquisition, archiving, compression/backup, display, and routing. DICOM-compliant. Images attach to patient EMR records. Eliminates need for physical film storage.

**BT Inventory** — Real-time supply and inventory management. Tracks per-procedure supply consumption, stock levels, low-stock alerts, purchase order generation, and spending analytics. Nursing staff log supplies used during procedures, which are automatically deducted from master inventory.

**BT Monitor** — System and infrastructure monitoring tool. Tracks EMR/practice management server health, network infrastructure, disk/memory/CPU usage, facility environmental conditions (temperature). Sends alerts via email, text, and instant message. Archives system logs.

**EMR/Clinical Documentation** — Pre-operative, intra-operative, and post-operative clinical documentation. Point-and-click workflows. Vital signs capture from monitors. Medication management with e-prescribing (additional per-provider fee for e-prescription license). Nursing documentation. Clinical notes and dictation. Drug interaction checking. Problem lists, medication lists, allergy lists. Clinical decision support.

**Practice Analysis/Reporting** — Business analytics covering procedure volumes vs. charges, referral physician trends, staff productivity, wait times, receivables/payment cycles, and quality outcomes. Chart audits and recertification tracking.

**Billing** — Integrated billing with CPT code auto-encoding during procedures. When nurses record procedural steps, billing codes are simultaneously generated. Billing can be completed same-day because encoding is done during the procedure. (Note: Braintree Operations also offers billing management as a service.)

**Patient Portal** — Certified for (e)(1) patient access. Patient portal mentioned on the website along with referral portal for physicians.

**Referral Portal** — Enables referring physicians to access patient DICOM images, clinical cines, and reports in real-time.

**Interoperability** — HL7 interfaces, DICOM worklist support, health information exchange. Interfaces mentioned with Transonic and Vasc-Alert (vascular access monitoring devices). FHIR API (g)(10) certified.

**Public Health Reporting** — Certified for immunization registries (f)(1)), syndromic surveillance (f)(2), electronic lab reporting (f)(3), cancer case reporting (f)(5), transmission to public health agencies (f)(6)-(f)(7).

**Compliance/Quality** — Meaningful Use checklists, MACRA/MIPS reporting, clinical quality measures (CQMs).

**Population Health** — Website mentions MSO/ACO and chronic care management workflows, though details are sparse.

### Data & Content

Based on the vendor's product descriptions and the typical workflow scenario documented on their website, the BMW Platform stores and manages:

**Clinical data:**
- Patient demographics and insurance information
- Medical history and prior admittances
- Pre-operative, intra-operative, and post-operative documentation
- Vital signs (captured from monitoring equipment)
- Medications and prescriptions (e-prescribing certified)
- Drug interaction data
- Problems/diagnoses
- Allergies
- Clinical notes and dictation
- Nursing assessments and documentation
- Procedure documentation and steps
- Lab orders and results (CPOE certified for lab and diagnostic imaging)
- Safety incidents and complication events
- Access flow history (vascular-specific)

**Imaging data:**
- DICOM medical images (acquisition, archiving, display, routing)
- Radiology procedure information and reports
- Clinical cine loops
- Study routing and worklist data

**Administrative/operational data:**
- Appointment schedules and availability
- Patient admission records
- Staff schedules and productivity metrics
- Wait time tracking (check-in through procedure completion)

**Financial/billing data:**
- CPT codes (auto-generated during procedures)
- Billing codes and charge data
- Insurance coverage information
- Receivables and payment cycle data
- Procedure costs and financial performance metrics
- Practice analysis data (volumes, referral trends, market segment capture)

**Supply chain/inventory data:**
- Medical supply inventory levels
- Per-procedure supply consumption records
- Purchase orders
- Vendor information
- Supply spending and budget data

**Infrastructure/system data:**
- System monitoring logs (BT Monitor)
- Network and server health data
- Environmental monitoring data

**Patient engagement data:**
- Patient portal access and interactions
- Referral portal data for external physicians
- SMS alerts

**Public health data:**
- Immunization records
- Syndromic surveillance data
- Lab reporting data
- Cancer case reports

The product's distinctive data profile compared to a typical ambulatory EHR is the deep integration of medical imaging (PACS/RIS), inventory/supply chain management, and procedure-oriented workflow data. This reflects its core market in outpatient procedure centers rather than primary care offices.

**Gaps/uncertainty:** The website does not clearly describe whether the system stores patient messaging or secure communication data beyond the patient portal. The "behavioral health" specialization mentioned on the website has no detailed feature description — it's unclear whether there are behavioral health-specific documentation templates or assessments. The "population health" and "chronic care management" capabilities are mentioned but not elaborated. No information about document scanning/storage, consent forms, or patient-generated health data was found.
