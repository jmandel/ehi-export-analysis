# Infor-Med Medical Information Systems Inc. — Product Research

Researched: 2026-02-15
Developer website: http://www.praxisemr.com/

## Overview

Infor-Med Medical Information Systems Inc. (commonly known as "Praxis EMR") is a small, privately held EHR vendor based in Commerce, CA. The company was founded by Dr. Richard Low, a Yale Medical School graduate who practiced Emergency Medicine and Internal Medicine for 20 years. Dr. Low began developing the product in the late 1980s after observing the repetitive nature of medical documentation during locum tenens work in California. He assembled a software development team in Argentina and partnered with attorney Allan Bloom to form Infor-Med Corporation. An early distribution deal with SmithKline Beecham helped bring the product to market.

Praxis EMR targets independent and small ambulatory practices, particularly solo practitioners and small groups across a wide range of specialties (90+ supported). The product claims "more than 5,000 physician-users" in the US, Canada, and worldwide, though third-party data (Enlyft) suggests a very small market share (~0.03%). The product is highly rated on review sites — 4.9/5 on Capterra with 200+ reviews — and has won the Capterra "Best EHR Value" report multiple times. It also received a HIMSS Davies Award. The company's go-to-market is direct sales, targeting independent practices, concierge/DPC practices, and physicians who value clinical documentation autonomy over standardized templates.

## Product: Praxis EMR

CHPL IDs: 10853

### What It Is

Praxis EMR is a full ambulatory EHR system — not a specialty module or middleware. It is the sole product of Infor-Med. The certified product (Version 9) covers the full scope of clinical documentation, e-prescribing, lab integration, patient portal, quality reporting, and FHIR API access. The certification covers 30+ ONC criteria spanning clinical data (a)(1)-(a)(15), transitions of care (b)(1)-(b)(2), patient portal (e)(1), public health reporting (f)(1), and FHIR APIs (g)(7)-(g)(10).

The product's key differentiator is its "template-free" charting approach powered by an AI "Concept Processor." Rather than using pre-built templates, the system learns from each physician's natural language documentation patterns and progressively becomes faster by recognizing recurring concepts. This is the core of Praxis's identity and marketing.

The product runs on an Oracle database (network version) or Microsoft Access (single-user version). Deployment is available both on-premise and cloud-hosted (via RDP/RemoteApp). The mandatory disclosures note a one-time Oracle Database license purchase per user.

### Users & Market

- **Primary users**: Solo and small independent practice physicians across many specialties
- **Specialties**: 90+ supported, including Family Medicine, Internal Medicine, Cardiology, Dermatology, Endocrinology, Pediatrics, Surgery, Gastroenterology, Pulmonology, Podiatry, Urgent Care, OB-GYN, Psychiatry, Orthopedics, Allergy & Immunology, and others
- **SED intended users**: "General Practitioners"
- **Customer base**: ~5,000+ physician-users claimed; very small market share nationally
- **Ideal customer profile**: Independent/solo practitioners, concierge/DPC practices, physicians who dislike template-driven EHRs, practices wanting to own software outright (lease-to-own model)
- **Pricing model**: Lease-to-own — $219/month for 60 months or $259/month for 48 months per first provider, then own outright. Additional providers at ~50% discount. Support $70-$500/month. Implementation $3,000-$15,000+. Data migration $2,000-$10,000.
- **Notable**: HIMSS Davies Award recipient. Dr. Jeremy Bradley reported 45% revenue increase and 250% first-year ROI in a case study.

### Modules & Functionality

Based on vendor website feature pages, third-party reviews, and product documentation:

**AI-Based Clinical Documentation (Concept Processor)**
- Template-free natural language charting — the system learns from physician documentation patterns
- "Reflective Ambient Intelligence" — newer AI feature merging ambient understanding with the Concept Processor
- The system builds a personal knowledge base for each physician that grows over time
- Users report creating charts in as little as 40 seconds for routine visits

**Datum+ Clinical Data Engine**
- Embeds discrete clinical data parameters within free-text narrative documentation
- Enables automated quality measure reporting (MIPS, ACO, MACRA, eCQM) directly from natural text — "Write it once and Praxis reports forever"
- Supports 40+ CMS clinical quality measures

**E-Prescribing (eRx)**
- Direct Surescripts integration for all medications including EPCS (controlled substances)
- Automated refill request handling
- Prescription Drug Monitoring Program (PDMP) integration
- Prescriptions routed directly to pharmacy

**Laboratory Integration**
- Real-time lab result streaming directly into patient charts
- Lab order transmission from system to laboratory
- Integrations with LabCorp, Quest Diagnostics, Dynacare, Sunquest, and 20+ other lab systems
- HL7-based interfaces

**Patient Portal**
- AI-driven patient-provider portal
- Encounter-based content — automatically determines what information each patient should see based on their visit and medical profile
- Patient self-scheduling
- Patient intake forms (AI-driven, condition-specific)
- Secure messaging
- Automated reminders
- Check-in kiosk functionality

**PraxDocs Document Manager**
- Scanning, imaging, and document archiving
- Multi-format support (PDF, DOC, JPG)
- Paperless office capabilities

**Clinical Decision Support**
- Practice Guidelines and customizable clinical queries
- Real-time Clinical Practice Advisories with provider-modifiable protocols
- Outcome-based recommendations from previous patient cases

**DataMiner Research & Query Tool**
- Population health queries across patient data
- Custom practice performance reports
- Research capabilities

**Knowledge Exchanger**
- Peer-to-peer sharing of clinical knowledge bases between physicians
- Specialty-specific knowledge bases available
- Import and adapt colleagues' documentation patterns, drug protocols, patient instructions, questionnaires, diagnostic discussions

**Scheduling**
- Patient scheduling and appointment management
- AI-driven patient self-scheduling
- Smart Agent automated reminders

**Intelligent Messaging / Smart Agents**
- AI-driven clinical communication and task automation
- Automated workflow agents for reminders and follow-ups
- Secure Direct messaging (provider-to-provider, HIPAA-compliant)

**Telemedicine**
- Remote patient consultation capabilities

**Billing Integration**
- Praxis integrates with external billing/practice management systems rather than providing a fully built-in billing module
- PraxCoder — intelligent coding optimization tool for maximizing reimbursement (E&M coding suggestions)
- Interfaces with 34+ billing/practice management systems (Allscripts, athenaOne, Tebra/Kareo, Medisoft, MicroMD, CollaborateMD, and others)
- Supports both insurance-based and direct-pay/concierge practice models
- Bidirectional synchronization with practice management systems for demographics

**Health Information Exchange**
- C-CDA document support for transitions of care
- HIE participation
- Direct secure messaging
- EMR Direct integration (noted in compound certification)

### Data & Content

Based on the features and integrations described above, Praxis EMR manages the following categories of data:

**Clinical Records**: Patient encounter notes/charts (free-text narrative with embedded discrete data via Datum+), medical histories, problem lists, diagnoses, assessments, treatment plans. The Concept Processor builds a growing knowledge base per physician, so the system stores both the individual patient records and the physician's learned documentation patterns.

**Medications & Prescriptions**: Medication lists, prescription history, controlled substance prescriptions (EPCS), refill requests, pharmacy routing records. Flows through Surescripts.

**Lab Data**: Lab orders (outbound), lab results (inbound real-time streaming), integrated with 20+ lab systems via HL7.

**Documents & Images**: Scanned documents, imported files (PDF, DOC, JPG), archived paper records via PraxDocs.

**Patient Demographics**: Patient demographic data, synchronized bidirectionally with practice management systems.

**Patient Portal Data**: Portal messages, intake forms, consent forms, self-scheduled appointments, patient-facing encounter summaries.

**Quality Reporting Data**: CQM/eCQM measure data, MIPS scores, ACO reporting data — derived from Datum+ discrete parameters embedded in narrative notes.

**Scheduling Data**: Appointments, scheduling history, automated reminders.

**Knowledge Bases**: Per-physician learned concept libraries, shared knowledge bases from Knowledge Exchanger (drug protocols, patient instructions, questionnaires, diagnostic discussions, case presentations).

**Clinical Decision Support Data**: Practice guidelines, clinical advisories, protocol configurations.

**Messaging & Communications**: Secure Direct messages (provider-to-provider), patient portal messages, Smart Agent automated communications.

**Billing/Coding Data**: While billing itself is handled externally, Praxis stores E&M coding suggestions (PraxCoder), superbills/charge data for transmission to billing systems, and demographic data synchronized with practice management systems.

**Unclear/External**: Full billing claims, payment records, and accounts receivable appear to be managed by external billing systems, not within Praxis itself. The vendor explicitly positions billing as an integration rather than a built-in module, though PraxCoder does handle coding optimization within Praxis.

---
