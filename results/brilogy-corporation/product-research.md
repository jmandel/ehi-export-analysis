# Brilogy Corporation — Product Research

Researched: 2026-02-14
Developer website: https://www.axeium.com

## Overview

Brilogy Corporation is a very small, regional IT services company based in Santa Ana, CA (Orange County), founded in 1996. The company is WBE-certified (Women Business Enterprise) through LA City since 2007, owned by Julie Allione (CEO), with Milton Allione serving as President. The company operates with roughly 11–50 employees and estimated revenue of $5M–$20M. Brilogy is a Microsoft Gold Certified Partner whose core business categories include computer systems design, custom programming, and staffing services — but its primary public-facing product is AXEIUM, a multi-specialty EHR and practice management system purpose-built for Federally Qualified Health Centers (FQHCs) and community health centers.

AXEIUM originated from a decade-long grant-funded consortium effort supported by United Healthcare, Kaiser Permanente, Tides Foundation, Orange County Healthcare Agency, Orange County Community Foundation, and the Coalition of Orange County Community Health Centers. This public-good origin — rather than a typical commercial startup path — is distinctive and explains the product's deep specialization for safety-net healthcare organizations. The vendor has essentially no presence on major review platforms (G2, Capterra, KLAS), no press coverage, and no Crunchbase activity. The brilogy.com parent website was unreachable during research; the company appears to operate almost entirely under the AXEIUM brand for its EHR business. In the FQHC EHR market, AXEIUM competes against much larger players like eClinicalWorks, NextGen, athenahealth, and Netsmart, differentiating on its purpose-built multi-service-line integration.

## Product: AXEIUM

CHPL ID: 11086

### What It Is

AXEIUM is a full-featured, multi-specialty EHR and practice management system designed specifically for community health centers that deliver medical, dental, vision, and behavioral health services under one organizational umbrella. The vendor positions it as "the one and only practice management and electronic health records system that supports all Community Health Service Lines." ONC classifies it as a Modular EHR for the Ambulatory setting, but in practice it functions as a comprehensive integrated platform covering clinical, administrative, and financial operations.

The certified module (CHPL 15.05.05.1171.BRIL.02.01.1.221219, certified 2022-12-19, version MU3) covers 26+ criteria spanning clinical data management, transitions of care, clinical quality measures, patient portal, FHIR APIs, and direct messaging. This is the product — the certified module and the full AXEIUM system appear to be one and the same, not a component of something larger.

The system uses a hybrid, client-hosted deployment model — data is stored on the client's own servers ("It is your data that is stored on your servers"), with a Windows desktop client as the primary interface and mobile/web extensions available. Pricing disclosed on the certifications page includes a monthly subscription plus visit-based SaaS fee.

### Users & Market

**Primary users:** FQHCs, free clinics, and community health centers, predominantly in Southern California / Orange County. The product's grant-funded consortium origins tied it closely to the Orange County community health ecosystem.

**Known client organizations** (from testimonials and development history):
- La Amistad Family Health Center (Orange, CA)
- The Gary Center
- Share Our Selves (Costa Mesa, CA — a nationally recognized FQHC)
- Camino Health Center
- Lestonnac Free Clinic
- St. Joseph Hospital of Orange / St. Joseph Community Health
- Puente Mobile Vision
- CHOC Children's
- St. Jude Neighborhood Health Centers

EMR review site reviewers suggest some geographic reach beyond Southern California (South Boston Community Health Center, North Florida Medical Associates), though the total number of deployed sites is unknown. Third-party reviews on small EMR directory sites (EMRSystems.net: 2 reviews, 4/5 stars; EMRFinder.com: 4 reviews, 4/5 stars) are positive but very sparse.

**Day-to-day users:** Physicians, medical assistants, dentists, dental hygienists, optometrists, behavioral health counselors, front desk/check-in staff, billing staff, and practice managers. The system is designed for high-volume clinics with features like patient photo capture at check-in, group class scheduling, and program tracking.

**Settings:** Multi-service-line community health centers offering primary care, dental, vision, and behavioral health. Designed for small to mid-size organizations, typically multi-site.

### Modules & Functionality

AXEIUM's module structure is organized around four clinical service lines plus administrative/practice management capabilities. The following is drawn from the vendor's own module pages.

**Medical Module** (source: axeium.com/Medical):
- Vitals collection with automated MA queue routing, dual BP readings, BMI auto-calculation, color-coded displays, trend charting
- Customizable exam templates with configurable defaults, required fields, tab organization
- Clinical Decision Support (CDS) rules triggering alerts based on conditions, demographics, and lab data
- Problem list with 6000+ SNOMED conditions, ICD-9/10 cross-referencing, severity adjustment
- Medication management with Lexicomp drug database, Surescripts ePrescribe (including eRefill), drug-drug and drug-allergy interaction checking, on/off-formulary notifications
- Allergy tracking (drug, food, environmental) with RxNorm codes and CDS alerts
- Lab integration with Quest Diagnostics, LabCorp, and Meditech — fully integrated order entry, auto-send, auto-match results, abnormal flagging, on-the-fly graphing, LOINC-coded structured data
- Immunization management with VIS in patient's preferred language, HL7 transmission to registries
- Surveys and assessment builder converting paper forms to electronic
- Health maintenance schedule with rules-based policy engine for condition-specific reminders
- SOAP and progress notes with AutoText phrases and hot-key shortcuts
- Electronic document repository with scanning, classification, task routing, batch scanning, multi-monitor support
- Drawings and annotation on clinical images

**Dental Module** (source: axeium.com/Dental):
- Tooth charting with configurable QuickChart buttons, color-coded existing vs. planned work, graphic tooth surface picker
- Periodontal charting with electronic probe depth tracking, mobility, periodontitis, gingivitis, prognosis
- Treatment plans importing from charted work, multiple plans per patient, automatic status updates
- Automatic CDT coding from completed work
- Progress notes with AutoText templates
- Imaging integration with DEXIS and Planmeca Romexis (bidirectional, automatic demographic sync)

**Vision Module** (source: axeium.com/Vision):
- Symptoms recording with customizable templates
- Refraction and prescription with myopia/hyperopia/astigmatism tracking, historical Rx viewing, glasses prescription printing
- Anterior and posterior segment documentation
- Glaucoma assessment with tonometry history and gonioscopy
- Clinical drawings and annotations

**Behavioral Health Module** (source: axeium.com/Behavior):
- Assessment management with scheduled reminders, patient alerts, automatic scoring
- Customizable intake forms with Microsoft Office integration, auto-population of known patient data
- SIRP workflow (Situation-Intervention-Response-Plan) with configurable templates and automatic clinical note generation
- Treatment planning with long-term goals, action tracking, printable plans for client signatures

**Administrative / Practice Management:**
- Patient management for high-volume clinics
- Appointment scheduling (next available, calendar, search by service/provider/location)
- Provider schedule management
- Group classes scheduling and check-in
- Task assignment to users or roles
- Patient contact logs (calls, correspondence, recalls)
- Patient check-in/check-out with photo capture and fee collection
- News management with read receipts

**Billing:**
- HCFA 1500 (standard commercial billing)
- PM-160 (FQHC-specific billing)
- Electronic billing
- CPT and ICD code libraries, superbills

**Reporting:**
- 8 certified eCQMs: CMS2 (depression screening), CMS74 (fluoride varnish), CMS75 (childhood dental decay), CMS117 (childhood immunization), CMS122 (diabetes HbA1c), CMS124 (cervical cancer screening), CMS125 (breast cancer screening), CMS165 (blood pressure control)
- OSHPD reporting (California state health facility reporting)
- UDS reporting (HRSA Uniform Data System — mandatory for FQHCs)
- Enterprise report writer with custom queries, filtering, Excel export, shareable views

**Interoperability:**
- RESTful FHIR API (patient search and patient data endpoints)
- C-CDA document creation and exchange
- Direct messaging via MDToolbox (Surescripts HISP) — required third-party component
- Secure email via Paubox — required third-party component
- Lab interfaces (Quest, LabCorp, Meditech)
- Imaging interfaces (DEXIS, Planmeca Romexis)
- eReferral network connecting health centers, hospitals, and surgery centers
- CCD import/export with medication reconciliation
- Patient portal with View/Download/Transmit capability
- Mobile app (iOS and Android)

### Data & Content

Based on the vendor's module descriptions, certification criteria, and EHI export documentation, AXEIUM stores the following categories of data:

**Patient demographics:** Name, DOB, contact information (multiple addresses, phone numbers), insurance, employment, language, race/ethnicity, smoking status, poverty scale, patient photo, chart number, DIRECT address, program assignments (for grant/specialty programs like food distribution).

**Medical clinical data:** Problem/diagnosis lists (SNOMED, ICD-9/ICD-10), medication lists (active and historical, via Lexicomp), allergy records (drug/food/environmental, RxNorm coded with severity), vital signs with historical trends, lab orders and results (structured, LOINC-coded), immunization records (with VIS documentation and HL7 registry submissions), family health history, implantable device records, clinical exam data from configurable templates, progress notes and SOAP notes, CDS alerts, health maintenance schedules, prescription history via Surescripts.

**Dental clinical data:** Tooth charts and odontograms, periodontal charts (probe depths, mobility, gingivitis/periodontitis, prognosis), treatment plans (planned and completed per-tooth with provider and date), CDT procedure codes, dental imaging references.

**Vision clinical data:** Refraction measurements, habitual and manifest refraction data, final Rx history, anterior and posterior segment findings, tonometry history, gonioscopy documentation, clinical drawings and annotations.

**Behavioral health clinical data:** Intake assessments with auto-scoring, SIRP documentation, treatment plans with goals and actions, assessment score histories, group therapy/class attendance records.

**Administrative/financial data:** Appointment scheduling data, provider schedules, check-in/check-out records, fee collection records, billing data (HCFA 1500, PM-160), superbill data, patient contact logs, task assignments.

**Documents and images:** Scanned documents (classified in three-level taxonomy), clinical images and annotations, referral documents, lab result PDFs, rich text documents.

**Interoperability/exchange data:** C-CDA documents (sent and received), transition of care records, reconciliation data (medications, allergies, problems reconciled from external sources), Direct messages.

**Audit and compliance data:** Access control records, audit logs (tamper-resistant per (d)(2)), amendment records, accounting of disclosures, emergency access records.

**Reporting data:** CQM/eCQM data for 8 measures, UDS reporting data, OSHPD reporting data.

The EHI export (per axeium.com/EHI) uses tab-separated files in AXEIUM's native record layout with a published schema (Schema.pdf), with separate handling for rich text documents and images. The actual export scope varies by deployed applications, software version, external data sources, and site configuration.

---

## Research Gaps

- The brilogy.com website was unreachable; the parent company's full service portfolio and history could not be assessed directly.
- No customer count or total deployment numbers are available.
- AXEIUM does not appear on G2, Capterra, or KLAS — third-party validation is very limited.
- No press releases, news articles, or media coverage were found about Brilogy Corporation.
- The patient portal's specific features beyond ONC-required VDT are unclear.
- The exact number of database tables/fields in the EHI export requires the Schema.pdf document from the EHI page (to be reviewed in Phase 2).
