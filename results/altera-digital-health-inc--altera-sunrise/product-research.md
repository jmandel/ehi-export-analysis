# Altera Digital Health Inc. — Product Research

Researched: 2026-02-16
Developer website: https://www.alterahealth.com

## Overview

Altera Digital Health is a global healthcare IT company headquartered in Niagara Falls, NY. It was formed in May 2022 when N. Harris Computer Corporation (a subsidiary of Constellation Software Inc.) acquired Allscripts' Hospitals and Large Physician Practices business segment for approximately $700 million. The acquired operation was rebranded as "Altera Digital Health" and became a business unit of Harris Healthcare. Under Constellation Software's "buy and hold forever" philosophy, Altera is positioned as a long-term investment with continued development of legacy Allscripts products.

Altera's product portfolio includes multiple EHR platforms for different market segments: **Sunrise** (for hospitals and large health systems), **Paragon** (for community and critical access hospitals), **TouchWorks** (for large ambulatory physician practices), plus interoperability (dbMotion), care coordination (Care Director), revenue cycle (Ventus), clinical workflow (CareFX/Altera Context), and a new data analytics platform (CareInTelligence). The three CHPL-certified products under review — Sunrise Acute Care, Sunrise Acute Care for Hospital-based Providers, and Sunrise Ambulatory Care — are all modules of the unified Sunrise platform.

**Note on CHPL metadata:** The CHPL metadata file lists the developer as "Providers Management, Inc." (integratedproviders.com, Burton, MI), which is actually a separate healthcare management organization that operates its own patient portal product (Integrated Providers Patient Portal) running on Altera TouchWorks. The Sunrise products are developed by Altera Digital Health Inc. This appears to be a data quality issue in the CHPL metadata file.

---

## Product: Sunrise (Sunrise Acute Care / Sunrise Acute Care for Hospital-based Providers / Sunrise Ambulatory Care)

CHPL IDs: 11707 (Sunrise Acute Care), 11708 (Sunrise Acute Care for Hospital-based Providers), 11709 (Sunrise Ambulatory Care)

### What It Is

Sunrise is Altera Digital Health's flagship comprehensive EHR platform designed for hospitals and health systems. It provides a **single, unified patient record** across acute (inpatient), ambulatory (outpatient), and financial/revenue cycle settings. The platform is cloud-capable, built on Microsoft Azure, and can be deployed on-premise, hosted, or in the cloud. It has both Windows-based desktop clients and native iOS mobile applications (Sunrise Air).

The three CHPL-certified products represent different modules or configurations of the same Sunrise platform:
- **Sunrise Acute Care** (CHPL 11707): The inpatient/hospital EHR module — the core acute care system.
- **Sunrise Acute Care for Hospital-based Providers** (CHPL 11708): A variant specifically for hospital-based clinicians (e.g., hospitalists, ED physicians). It shares nearly identical certified criteria with the base Acute Care product.
- **Sunrise Ambulatory Care** (CHPL 11709): The outpatient/ambulatory care module. It has slightly fewer public health reporting criteria (missing (f)(3) and (f)(6) vs. the acute products).

All three share a common underlying database and patient record. They are not separate platforms but rather different views/modules within the same Sunrise ecosystem. All three were certified at version 25.1 on September 5, 2025, with extensive certifications spanning clinical data (a)(1)–(a)(5), (a)(12), (a)(14)–(a)(15); transitions of care (b)(1)–(b)(3); patient portal/VDT (e)(1); FHIR APIs (g)(7)–(g)(10); public health reporting (f)(1)–(f)(7); and direct messaging (h)(1).

### Users & Market

Sunrise targets **midsize to large hospitals and health systems**, including community hospitals (particularly 101+ beds), academic medical centers, and specialty hospitals such as acute rehabilitation facilities. It has been recognized by Black Book Research as the #1 inpatient EHR for community hospitals (101–250 beds) and the top EHR for acute rehabilitation hospitals.

The end users include:
- **Physicians** (hospitalists, ED physicians, attending physicians, specialists)
- **Nurses** (inpatient and ambulatory)
- **Pharmacists** (integrated pharmacy module)
- **Radiologists** (radiology module)
- **HIM/coding staff** (health record/HIM module)
- **Financial/billing staff** (Sunrise Financial Manager)
- **Schedulers and front-desk staff** (scheduling module)
- **Patients** (via Sunrise CarePath patient engagement app)

Altera has a global presence, with Sunrise installations in North America, APAC, and other regions (referenced via alteradigital.com, the international variant). Specific customer counts are not publicly disclosed, but the product has a well-established installed base from its legacy as the Allscripts Sunrise Clinical Manager platform, which has been in the market for decades.

On G2, Sunrise has a 3.2/5 rating from 19 reviews (as of 2026). KLAS Research tracks it as an acute care EHR with a moderate market presence — recognized in its niche but trailing Epic and Cerner/Oracle Health in new large-system sales and overall market momentum.

### Modules & Functionality

Based on vendor materials, press releases, product pages, and third-party reviews, Sunrise includes the following modules and capabilities:

**Clinical Documentation & Workflow**
- Electronic clinical documentation with multidisciplinary progress notes
- Real-time patient data entry at point of care
- Clinical decision support (CDS) engine that aggregates patient data and provides diagnostic/treatment guidance
- Computerized physician order entry (CPOE) with patient-level order management
- Patient tracking boards with configurable views for ED and inpatient throughput
- Threaded clinical messaging system for team communication
- Support for preferred names and pronouns in patient records (added in 25.1)
- Sunrise Thread AI: ambient scribe and note generation assistant that captures patient-provider conversations in real time and generates structured visit summaries directly in the EHR (launched November 2025)

**Medication Management & Pharmacy**
- Integrated pharmacy module with real-time sharing of medication information between physicians and pharmacists
- e-Prescribing (via Surescripts integration implied by certification criteria)
- Medication reconciliation
- Barcode medication administration (BCMA)
- RxWriter for prescription writing with safety features

**Orders & Results**
- Order entry, viewing, and maintenance at patient level
- Lab integration for ordering and receiving results
- Advanced order search functionality

**Radiology**
- Dedicated radiology module enabling paperless cooperation between radiologists and physicians
- Order entry, image review, result distribution, and reporting integration

**Surgery & Perioperative**
- Anesthesia and perioperative modules
- Integrated pre-op, intra-op, and post-op records within the single patient record

**Scheduling & Patient Tracking**
- Unified scheduling interface for appointments and walk-in patients across clinics, radiology, and surgical suites
- Real-time schedule updates with at-a-glance view
- Resource management for staff, rooms, and equipment
- Patient tracking with data-driven throughput optimization

**Financial Management / Revenue Cycle**
- **Sunrise Financial Manager**: Consolidated billing hub handling claims, self-pay, and billing requests
- Episode management and automated adjustments
- Advanced appeals and denials management
- SuperBill with automated field population for coding
- Front-to-back revenue cycle workflow from scheduling through discharge and payment
- Registration and admission/discharge/transfer (ADT)

**Health Information Management (HIM)**
- Sunrise Health Record module for managing medical records
- Document management and scanning
- Audit support and compliance

**Patient Engagement**
- **Sunrise CarePath**: Mobile app for patient engagement with automated scheduling, appointment reminders, direct communication with providers, online bill pay, and access to results
- Patient portal with view/download/transmit capabilities (certified under (e)(1))

**Mobile**
- **Sunrise Mobile / Sunrise Air**: Native iOS application for clinicians to access patient summaries, review results, manage tasks, and (with Thread AI) initiate ambient documentation capture on the go

**Analytics & Reporting**
- Business intelligence and analytics solution combining clinical and financial data
- Quality measures tracking (antibiotic stewardship, opioid crisis, infection control)
- Reporting tools for operational and clinical performance

**Interoperability**
- FHIR API support (certified under (g)(7)–(g)(10))
- USCDI v3 compliance
- HL7 CDA support
- SMART App Launch
- Direct messaging (h)(1)
- Transitions of care (b)(1)–(b)(3): C-CDA generation and consumption
- Public health reporting: immunization registries, syndromic surveillance, electronic case reporting, cancer registries, antimicrobial use/resistance reporting

### Data & Content

Based on the certified criteria, vendor documentation, and product features, Sunrise stores and manages the following categories of data:

**Clinical Data (directly evidenced)**
- Patient demographics (including preferred name/pronouns per 25.1 release notes)
- Problem lists, diagnoses, conditions
- Medication lists and prescribing history
- Allergy and intolerance data
- Vital signs and clinical measurements
- Lab orders and results (lab integration module)
- Radiology orders, images (references), and reports (radiology module)
- Clinical notes and progress notes (documentation module + Thread AI-generated summaries)
- Surgical/perioperative records (surgery module)
- Immunization records (certified for immunization registry reporting)
- Clinical decision support alerts and interactions

**Orders & Workflow Data**
- CPOE orders (medications, labs, imaging, procedures)
- Order sets and templates
- Task lists and work queues

**Financial & Administrative Data (directly evidenced via Sunrise Financial Manager)**
- Billing claims and billing requests
- Self-pay transactions
- Episode/encounter financial records
- Registration/ADT data
- SuperBill/charge capture data
- Appeals and denials records
- Scheduling data (appointments, resources, rooms)

**Patient-Generated & Communication Data**
- Patient portal messages and data (CarePath app)
- Clinical team messaging threads
- Patient-provider conversation transcripts (Sunrise Thread AI captures and stores these)

**Regulatory & Reporting Data**
- Public health reports: immunization submissions, syndromic surveillance data, electronic case reports, cancer reports, antimicrobial use/resistance reports
- Clinical quality measure data (certified for CQM collection under (c)(1)–(c)(3))
- Audit logs (certified under (d) criteria)

**What's less clear:**
- Whether Sunrise includes a built-in **laboratory information system (LIS)** or only interfaces with external LIS systems. The vendor describes "lab integration" but details are sparse — it may be order/result integration rather than full specimen tracking and processing.
- Whether **blood bank** management is included or is a separate system.
- The extent of **Enterprise Master Patient Index (EMPI)** capabilities — Altera's separate Ventus product includes EMPI, suggesting Sunrise may rely on Ventus or another component for enterprise-level patient matching.
- Whether **dictation/transcription** data (beyond Thread AI) is stored within Sunrise or comes from external systems.
- The depth of **supply chain or inventory management** data — the pharmacy module likely tracks some inventory, but the extent is unclear.

---

## Product Ecosystem Context

Sunrise does not exist in isolation. Altera's broader product portfolio includes several complementary products that may integrate with or supplement Sunrise at customer sites:

- **Ventus**: Revenue cycle management, Enterprise Master Patient Index (EMPI), surgery scheduling, intelligent coding, and medical necessity compliance. This suggests some financial/scheduling functionality may be handled by Ventus rather than (or in addition to) Sunrise Financial Manager.
- **dbMotion**: Interoperability platform providing a longitudinal patient record with semantically normalized data from multiple sources. May aggregate data from Sunrise and other systems.
- **Care Director**: Outpatient care coordination across the continuum — value-based care, population health, care plans.
- **CareFX / Altera Context**: Clinical workflow integration and single sign-on across disparate applications using HL7 CCOW standard.
- **Paragon**: Separate EHR platform for community/critical access hospitals (different product from Sunrise, though same vendor). Paragon Denali is a newer cloud-native variant.
- **TouchWorks**: Separate ambulatory EHR platform for large physician practices (different from Sunrise Ambulatory Care).
- **CareInTelligence**: New data analytics platform announced 2026.

At a given hospital, the "product of which the Health IT Module is a part" likely includes Sunrise Acute Care + Sunrise Ambulatory Care + Sunrise Financial Manager at minimum, potentially with Ventus, dbMotion, and other modules depending on the deployment.
