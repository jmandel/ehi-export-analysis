# iKnowMed Generation 2 (Ontada / McKesson) — Product Research

Researched: 2026-02-15
Developer website: https://www.ontada.com/developer/

## Overview

iKnowMed Generation 2 is a cloud-based, web-accessible electronic health record (EHR) system designed exclusively for oncology and hematology practices. It is a specialty EHR — not a general-purpose system — built specifically for the clinical workflows of community oncologists, including chemotherapy treatment planning, cancer staging, regimen management, and precision medicine. The product is developed and maintained by McKesson Specialty Health Technology Products LLC, operating under the Ontada brand.

iKnowMed was originally developed in 1996 and acquired by US Oncology in 2004. McKesson Corporation acquired US Oncology Inc. in December 2010 for approximately $2.16 billion (including $1.6 billion in assumed debt), bringing iKnowMed into the McKesson portfolio. In May 2013, McKesson Specialty Health announced iKnowMed Generation 2, a next-generation rebuild developed in collaboration with over 200 practicing oncologists. In December 2020, McKesson launched Ontada as a dedicated oncology technology and insights business, and iKnowMed became a core component of the Ontada product suite. The name "Ontada" combines "oncology" and "data," reflecting the business's dual focus on clinical care delivery and real-world data/research.

Ontada is headquartered in Boston, MA (33 Arch Street, 20th Floor) and operates as a business unit within McKesson Corporation. The developer contact (Arun Meelyan, Arun.Meelyan@McKesson.com) reflects the McKesson organizational structure.

## Product: iKnowMed Generation 2

CHPL ID: 9580 (15.04.04.2920.iKno.30.01.1.180508)

### What It Is

iKnowMed Generation 2 Version 3 is a web-based, mobile-optimized oncology EHR certified under the ONC 2015 Edition criteria (certification date May 8, 2018, certified by Drummond Group Inc.). It is the only next-generation EHR designed exclusively for oncology and hematology available on the market. The system provides cloud-based access to patient charts, treatment decision support, and oncology-specific clinical workflows from any web browser, with an iOS mobile app for on-the-go access.

The product is offered as a monthly subscription fee per user, covering access, maintenance, support, and upgrades. Additional costs include one-time professional services for implementation, setup, and user training, plus one-time setup fees and annual maintenance for interface configurations.

The system depends on NewCropRx for e-prescribing functionality and Surescripts Clinical Messaging for secure direct messaging. Providers must register with Surescripts (DirectTrust network participant) to maintain these capabilities. Direct exchange messaging is not available outside the Surescripts/DirectTrust network.

### Users & Market

iKnowMed serves the community oncology market exclusively. Key metrics reported across sources (numbers vary by date and source):

- **2,700+ oncology providers** actively use the platform (Ontada's most recent figures)
- **2,400 providers** within The US Oncology Network specifically (December 2024 data)
- **620+ sites of care** nationwide (at time of ONC certification)
- **1.5 million+ active patient portal users** nationally
- **1 million+ clinical decisions** supported through the platform
- **~2.5 million patient records** in the system
- **~1.4 million patients** seen annually across the connected network

The US Oncology Network, one of the nation's largest integrated community oncology networks, is the primary user base. The network's affiliated practices use iKnowMed as their standard EHR. Ontada also connects to Onmark practices beyond the core network. US Oncology Network practices care for approximately one in five cancer patients in the United States.

Intended users per ONC certification: Prescribers (oncologists/hematologists), Nurses, and Configuration Users (practice administrators). Day-to-day users include oncologists (treatment planning, charting, ordering), nurses (medication administration documentation, treatment monitoring), clinical staff (patient intake, documentation), and practice administrators (configuration, analytics).

iKnowMed has been recognized as the top-ranked EHR platform for oncologists and hematologists for five consecutive years by Black Book Rankings. In KLAS Research's July 2025 oncology EHR ranking, iKnowMed scored 80.1 out of 100, placing second behind Epic Beacon (86.3) and ahead of Flatiron Health OncoEMR (79.8) and Elekta ONE (76.7).

### Modules & Functionality

Based on vendor website, McKesson product pages, mandatory disclosures, FHIR API documentation, and third-party reviews:

**Oncology-Specific Clinical Documentation**
- Cancer diagnosis and staging using AJCC (American Joint Committee on Cancer) and FIGO (International Federation of Gynecology and Obstetrics) staging criteria
- Comprehensive patient charting with oncology-focused templates and customizable dashboards
- Flexible documentation options with auto-sharing of clinical notes
- Encounter-based documentation with customizable charts and order sets
- Elimination of handwritten notes and drug orders to minimize inaccuracies

**Chemotherapy Treatment Planning & Regimen Management**
- Extensive, up-to-date cancer regimen library organized by disease categories and treatment types
- Value Pathways powered by NCCN and NCCN Clinical Practice Guidelines in Oncology (NCCN Guidelines) integrated directly into clinical workflow
- Personalized protocol creation for disease complications, patient-specific needs, and drug replacements
- Pre-populated order forms with ability to save drafts and access completed forms in patient chart
- Safety alerts for medication conflicts and high toxicity levels

**Clinical Decision Support (Clear Value Plus)**
- Clear Value Plus is a companion clinical decision support tool highlighting evidence-based treatment options
- Integrated financial information alongside clinical pathways at point of care
- Real-time reporting and benchmarking against evidence-based standards
- Constantly refreshed clinical information including guidelines and pathways

**Precision Medicine & Biomarker Support**
- Biomarker ordering within the EHR displaying latest targeted therapy options at point-of-need
- Biomarker test guidelines suggesting molecular tests by disease type
- Rapid integration of new guidelines and biomarkers as they emerge
- Real-time data capture enhancing precision medicine decision-making
- Ontada's Precision Care Companion (announced 2024) for community oncology precision medicine workflows

**Clinical Decision Support Alerts**
- Drug-drug and drug-allergy interaction alerts
- Clinical decision support monitoring changes in BSA, lab results, hepatic/renal dysfunction
- Actionable alerts allowing single-click implementation of recommended changes
- Safety alerts for toxicity levels and medication conflicts

**Electronic Prescribing**
- Surescripts-certified e-prescribing
- Electronic prescription exchange with pharmacies on the Surescripts network
- Real-time patient eligibility and formulary information
- Prescription history access
- Integration via NewCropRx

**Practice Analytics (Practice Insights)**
- Multi-source data aggregation for clinical, operational, and financial insights
- Drug utilization metrics and clinical pathway compliance based on NCCN Guidelines
- Peer and industry benchmarking
- Quality initiative tracking for value-based care programs (MIPS, Oncology Care Model)
- Performance metrics and productivity measures
- Proactive, actionable insights for oncology practice management

**Patient Engagement (Ontada Health)**
- Secure patient portal providing online access to clinical information
- Provider-patient communication tools and secure messaging
- Expanded library of patient education resources
- Interoperable technology for sharing information across care systems
- 1.5 million+ active patient portal users nationally

**Appointment & Scheduling Management**
- Appointment management integrated into the EHR
- Mobile access to patient appointments via iOS app

**Billing & Charge Capture**
- Automated charge capture functionality
- EM coding support
- Integration with revenue cycle management workflows

**Quality Reporting**
- CMS-approved Qualified Clinical Data Registry (QCDR) for MIPS quality measure reporting
- iKnowMed users can submit quality data directly to CMS (2023 QCDR designation)
- Clinical quality measure CMS68v6 certified

**Public Health Reporting**
- Immunization registry reporting (certified under 170.315(f)(1))
- Electronic case reporting (certified under 170.315(f)(2))
- Cancer case reporting (certified under 170.315(f)(5))

**Interoperability & APIs**
- FHIR R4 API (Ontada FHIR Server) with 30+ clinical resources
- SMART on FHIR support for EHR-embedded application launches
- Client Credentials authentication for backend integration
- OAuth 2.0 and OpenID Connect for authorization
- Transitions of care via C-CDA (certified (b)(1)-(b)(3))
- EHI bulk export via FHIR Group resource (certified (b)(10))
- Certified API Developer Program (self-serve) and Value Add Developer Program (by-invitation with sandbox, marketplace listing, workflow integration)
- Ontada Marketplace for third-party application distribution

**Mobile Access**
- iOS app providing secure cloud-based access to patient charts and appointments
- Web-based mobile-optimized interface accessible from any device

**Document Management**
- Document storage and management within patient records
- Clinical note auto-sharing across care team

### Data & Content

The FHIR API documentation reveals 30+ clinical data resource types accessible through the Ontada FHIR Server, providing a comprehensive view of the data model:

**Patient Identity & Demographics**
- Patient demographics, contact information, identifiers
- Related persons (family members, caregivers)
- Coverage (insurance information)

**Clinical Encounters & Care Coordination**
- Encounter records
- Appointment scheduling data
- CarePlan (treatment plans)
- CareTeam assignments
- Goal tracking
- ServiceRequest (orders and referrals)

**Diagnoses & Conditions**
- Condition records (cancer diagnoses, staging, comorbidities)
- Cancer staging data (AJCC, FIGO criteria)

**Medications & Prescriptions**
- MedicationRequest (prescriptions and orders)
- MedicationStatement (reported medications)
- MedicationAdministration (infusion/treatment administration records)
- MedicationDispense (dispensing records)
- Medication reference data

**Laboratory & Observations**
- Observation (lab results, vital signs, clinical measurements including BSA)
- DiagnosticReport (lab reports, pathology reports)
- Specimen data

**Treatment & Procedures**
- Procedure records (chemotherapy administration, surgeries, biopsies)
- Chemotherapy regimen data (based on NCCN pathways)
- Treatment protocol documentation

**Safety Data**
- AllergyIntolerance records
- Immunization records

**Documents & Provenance**
- DocumentReference (clinical documents, notes)
- Binary (document content)
- Provenance (data source tracking)
- QuestionnaireResponse (patient-reported data)

**Administrative & Reference**
- Organization, Practitioner, Location, Device reference data
- Provider profiles and facility information

The EHI export functionality delivers data as compressed zip files containing pipe-delimited (|) flat files. Ontada provides a data dictionary (b10_data_dictionary.xlsx) describing the contents of each exported table. The exact content varies by organization based on which iKnowMed features are active, configuration choices, clinical usage patterns, and available documentation.

Beyond the standard clinical EHR data, iKnowMed's deep oncology focus means the system stores specialty-specific data not found in general EHRs:
- Cancer-specific diagnosis and staging information (tumor type, stage, grade)
- Chemotherapy regimen selections and treatment cycles
- Biomarker and molecular test orders and results
- NCCN pathway compliance tracking
- Drug toxicity monitoring data
- BSA (body surface area) calculations for dosing
- Treatment response assessments

### Deployment & Architecture

iKnowMed Generation 2 is a **cloud-based** system. It is accessed via web browser and does not require local software installation. The iOS mobile app provides additional access to patient charts and appointments. The system login URL (https://ikm.ontada.com/) confirms the cloud-hosted deployment model under the Ontada domain.

The system is ISO 9001:2015 Stage 2 certified, HIPAA compliant, and ICD-10 certified.

### Integrations

- **Surescripts/DirectTrust** — e-prescribing and direct messaging (required dependency)
- **NewCropRx** — e-prescribing engine (required dependency)
- **NCCN** — Value Pathways and Clinical Practice Guidelines integration
- **Ontada Marketplace** — third-party developer ecosystem via Certified API and Value Add Developer Programs
- **FHIR R4 API** — standards-based integration for external applications
- **Immunization registries** — public health reporting
- **Cancer registries** — case reporting

**Known integration challenges**: KLAS user reviews note persistent interoperability concerns, with nearly half of respondents reporting poor integration with external EHRs, labs, and scheduling tools. One user described interfacing with iKnowMed as "a nightmare." This likely reflects iKnowMed's position as a specialty system that must coexist alongside hospital/health system general-purpose EHRs.

### Ecosystem & Beyond-EHR Capabilities

iKnowMed is not just a clinical EHR — it serves as the data collection backbone for Ontada's broader oncology intelligence platform:

**Real-World Data & Research**
- iKnowMed data feeds Ontada's real-world evidence (RWE) generation engine
- Over 400 real-world research publications supported by Ontada
- Data from ~2.5 million patient records used for research insights
- FDA selected Ontada to investigate rare cancer natural history
- Partnerships with pharmaceutical companies (Merck, BeiGene, Amgen) for evidence-based research

**AI & Advanced Analytics**
- ON.Genuity platform leveraging AI for oncology data analysis
- 2024 collaboration with Microsoft to transform unstructured oncology data using Azure OpenAI technology
- Genospace for next-generation sequencing (genomic) data analysis

**Data Products (for life sciences companies)**
- ON.ClinicalDataView — clinical data access
- ON.Insights — oncology market insights
- ON.OutcomesView — health economics and outcomes research
- ON.JourneyView — patient journey analytics
- Alerts — real-time notification system

**Provider Education**
- Ontada Learn — digital education platform for oncology practitioners
- Practice-based education and strategy effectiveness training

## Competitive Landscape

iKnowMed competes primarily with:
1. **Epic Beacon** — Epic's oncology module, which leads KLAS rankings (86.3 vs iKnowMed's 80.1) and dominates in health system/academic oncology settings
2. **Flatiron Health OncoEMR** — another oncology-specific EHR focused on community oncology and real-world data, scoring 79.8 in KLAS
3. **Elekta ONE (Mosaiq)** — primarily radiation oncology information system, scoring 76.7 in KLAS

iKnowMed's primary differentiation is its deep integration with The US Oncology Network (the largest community oncology network) and its dual role as both a clinical EHR and a data collection platform for real-world oncology research. While Epic Beacon leads in overall satisfaction, iKnowMed's oncology-specific design (built by oncologists for oncologists) gives it advantages in community oncology workflows that general-purpose EHRs with oncology modules cannot easily replicate.

## Research Notes

- iKnowMed is tightly coupled with the US Oncology Network; its market penetration outside that network appears limited, though the Ontada Marketplace and developer programs suggest efforts to broaden the ecosystem.
- The dual role of iKnowMed as both clinical EHR and real-world data collection instrument for pharmaceutical research is distinctive. Clinician data entry directly feeds Ontada's commercial data products.
- The EHI export uses pipe-delimited flat files rather than standard formats like FHIR bundles — the data dictionary (b10_data_dictionary.xlsx) would need to be reviewed in Phase 2 to understand the full export schema.
- The 2018 certification date is notably old; many competing products have more recent certifications. However, the FHIR API and EHI export capabilities appear to be actively maintained.
- Interoperability with non-Ontada systems is a documented pain point per KLAS reviews, which is significant for practices that need iKnowMed to coexist with hospital EHRs.
- Full source list available in sources.json.
