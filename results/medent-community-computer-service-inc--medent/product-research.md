# medent (Community Computer Service, Inc.) — Product Research

Researched: 2026-02-16
Developer website: https://www.medent.com

## Overview

MEDENT is the medical software brand of Community Computer Service, Inc., a privately held company founded in 1968 in Auburn, New York. The company was co-founded by Edward Cuthbert and Dick Fitzgerald. For over 50 years, MEDENT has focused on automating medical practices with an integrated EHR, practice management, and patient engagement platform. The company has approximately 260 employees (per historical reporting; LinkedIn lists ~114) headquartered at 15 Hulbert Street, Auburn, NY, with additional offices in New York and Pennsylvania. MEDENT serves over 11,000 healthcare providers across 37 states, primarily in the Eastern and Central United States, with over 1,700 client sites. The company completed a visual rebrand in November 2025 but has not changed ownership or been acquired. MEDENT has been ranked #1 by Medical Economics in their EHR report card. The current CEO is Gary S. Cuthbert.

MEDENT is squarely an ambulatory EHR vendor focused on independent medical practices, clinics, and FQHCs (Federally Qualified Health Centers). It supports over 30 medical specialties and serves practices ranging from solo providers to large multi-specialty groups. The product is available both as a cloud-hosted service and as a server-based on-premise installation.

## Product: medent

CHPL ID: 11347

### What It Is

MEDENT is an "All-In-One" integrated EMR/EHR, Practice Management, Patient Engagement, and Telehealth system. The certified module covers the full product — there is no separate certified module vs. larger product distinction. The single MEDENT platform encompasses clinical charting, billing, scheduling, e-prescribing, patient portal, telehealth, and interoperability features in one system. It can be deployed as a complete package or in individual modules.

The CHPL certification is extensive (40+ criteria) covering clinical data (a)(1)–(a)(5), (a)(12), (a)(14)–(a)(15); transitions of care (b)(1)–(b)(3); clinical quality measures (c)(1)–(c)(3); patient portal (e)(1), (e)(3); public health reporting (f)(1), (f)(2), (f)(4), (f)(5), (f)(7); FHIR API (g)(7), (g)(9), (g)(10); and Direct messaging (h)(1). This breadth confirms it is a comprehensive ambulatory EHR, not a narrowly scoped system.

### Users & Market

- **Target users**: Physicians, specialty doctors, clinical staff, billing staff, practice managers, and patients (via portal)
- **Clinical settings**: Independent ambulatory practices, multi-specialty groups, FQHCs, clinics across 30+ specialties
- **Customer base**: 11,000+ providers in 37 states, 1,700+ client sites, concentrated in the Eastern and Central US
- **Deployment**: Cloud (SaaS) or on-premise server-based
- **Market position**: Mid-size regional EHR vendor. Privately held, not part of a larger conglomerate. Competes in the independent ambulatory practice space against vendors like eClinicalWorks, athenahealth, and NextGen. Strong regional presence in the Northeast.
- **User reviews**: Generally positive (4.1/5.0 on Software Finder from 34 reviews). Users praise ease of use, customizability, and comprehensive functionality. Some concerns about occasional system slowness and customer support responsiveness.

### Modules & Functionality

Based on vendor materials, blog posts, review sites, and partner integrations, MEDENT includes the following modules and features:

**Clinical Documentation / EMR**
- **Chart Central**: Main clinical dashboard providing access to patient records, documents, messages, and lab results (EMRSystems, vendor website)
- Multiple documentation input methods: voice notes, Dragon Medical speech recognition, point-and-click, and touch inputs (EMRSystems)
- Health history timeline view in patient charts (EMRSystems)
- Disease management and health maintenance formulas for patient data mining (search results, vendor descriptions)
- Clinical decision support including IMO (Intelligent Medical Objects) for diagnosis searching and VisualDx integration for differential diagnosis (MEDENT blog post)
- HCC (Hierarchical Condition Category) code highlighting for risk assessment documentation (MEDENT blog post)
- Customizable templates: pre-built templates plus custom template creation based on workflow preferences (Software Finder)
- Bookmarks for frequently-used system options (EMRSystems)

**Practice Management & Billing**
- Patient scheduling with appointment templates, flexible time slots, and online scheduling for patients (vendor search results)
- **Patient Account module**: Patient lookup by multiple criteria (insurance policy, phone, appointment), family account grouping, centralized account information, organized account notes (search results)
- Billing and coding: CPT/HCPCS codes with fee schedules configurable by doctor, location, and specialty; error checking for missing codes before claim submission (vendor search results)
- Claims management and submission (Software Finder)
- ERA (Electronic Remittance Advice) processing — the system is described as "fully integrated with billing/ERA" (search results)
- Collections reporting: A/R summaries and trend analysis, year-to-date financial tracking (MEDENT blog post)
- Patient payments: online payments, Guest Pay, kiosk-based copay collection, text-to-pay via RevSpring partnership (MEDENT blog post, RevSpring page)
- E-Statements through patient portal (vendor materials)
- UDS reporting for FQHCs (multiple sources)
- MIPS reporting via Patient360 partnership (MEDENT blog post)
- Comprehensive suite of interactive and printed reports for practice management (vendor materials)

**E-Prescribing**
- Advanced drug and e-prescribing capabilities with patient-specific alerts at time of prescribing (vendor search results)
- Surescripts integration for NPI-based Direct Address lookup and electronic prescribing (interoperability search results)
- Auto-replace function for substituting brand-name drugs with generic equivalents (vendor search results)

**Lab Integration**
- Bidirectional lab interfaces with over 260 hospitals, lab companies, and LIS systems (vendor materials)
- Lab results posted to Chart Central and Patient Portal (vendor materials)

**Patient Portal & Patient Engagement**
- Secure messaging between patients and providers (vendor materials)
- Online appointment scheduling by patients (vendor materials)
- Test results and clinical documents viewable in portal, organized for easy review (MEDENT blog post on portal engagement)
- E-Statements with online payment options (vendor materials)
- E-Visits (virtual encounters via portal) (vendor materials, EMRSystems)
- Prescription refill requests (vendor materials)
- Proxy/family access for caregivers to view records (MEDENT blog post)
- Mobile-friendly portal access (MEDENT blog post)
- Medline Plus integration via infobutton for patient education (MEDENT blog post)

**Telehealth**
- Video visits integrated into the platform (MEDENT blog post, LinkedIn description)
- E-Visits (asynchronous virtual care via patient portal) (vendor materials)

**Messaging & Communication**
- **Message Central**: Internal messaging system for practice communication (webinar listings)
- Appointment reminders by phone/text (vendor materials)
- Patient reminders via phone and text (vendor materials)

**Interoperability & Data Exchange**
- **Community Chart**: Feature that automatically queries external sources for patient data when accessed; connects to hundreds of thousands of physicians nationwide (interoperability search results)
- Carequality and CommonWell Health Alliance membership for nationwide health information exchange (MEDENT blog post)
- **Direct Messaging**: Built-in at no additional cost; XDR Direct for sending/receiving electronic documents; automatic chart matching and triage creation for incoming messages (interoperability search results)
- FHIR API (g)(7), (g)(9), (g)(10) certified for standards-based API access
- C-CDA document exchange for transitions of care (implied by (b)(1)–(b)(3) certification)

**Public Health Reporting**
- Immunization registry submission (f)(1) certified; Data Export Module used for immunization interfaces (search results)
- Syndromic surveillance reporting (f)(2) certified
- Cancer case reporting (f)(4) certified
- Electronic case reporting (f)(5) certified
- Reportable conditions / electronic case reporting to public health agencies (search results)
- Clinical quality measures reporting per CMS QRDA Category III (search results)

**Document Management**
- Document management accessible from Chart Central dashboard (vendor materials)
- Faxing as an optional module, integrated into workflow (vendor materials)
- Scanning and imaging as optional modules (vendor materials)

**Mobile Access**
- MEDENT Mobile app for smartphones and tablets: access medical records, patient history, prescribe medications, review labs, reply to messages (vendor materials)
- Available on iPhone, iPad, and Android (EMRSystems)

**AI Features (Recent)**
- Ambient documentation (AI-powered clinical note generation) (LinkedIn, 2025)
- Intelligent document sorting (LinkedIn, 2025)
- Virtual receptionist capabilities (LinkedIn, 2025)
- Patient follow-up support (LinkedIn, 2025)

**Optional Modules**
- Dragon Speech Recognition integration
- Medical Equipment Interfaces
- Imaging module
- AccuVax and VaxCare vaccine management interfaces (MEDENT blog post)

**Workflow Automation**
- Customizable workflows with automatic task assignments triggered by specific conditions (Software Finder)
- Adjustable interface, color schemes, and information display (Software Finder)

### Data & Content

Based on the evidence gathered, MEDENT stores and manages the following categories of data:

- **Patient demographics**: Name, contact info, insurance policy numbers, family account groupings, phone numbers (Patient Account module description)
- **Clinical records**: Health history, clinical notes, problem lists, medication lists, allergies, vitals (implied by (a)(1)–(a)(5) certification and Chart Central description)
- **Lab results**: Bidirectional interfaces with 260+ labs; results stored in charts and posted to portal (vendor materials)
- **Prescriptions and medication data**: E-prescribing with drug alerts, Surescripts integration, brand/generic substitution (vendor materials)
- **Immunization records**: Tracked and reported to registries (f)(1) certification and blog post mention of flu vaccination tracking)
- **Documents**: Clinical documents, scanned images, faxes stored in document management accessible from Chart Central (vendor materials)
- **Billing and financial data**: CPT/HCPCS codes, fee schedules, claims, ERA data, patient accounts, A/R data, payment records, e-statements (billing descriptions and RevSpring integration)
- **Scheduling data**: Appointments, appointment templates, time slots, online scheduling records (vendor materials)
- **Messages**: Patient-provider portal messages, internal practice messages via Message Central, Direct Messages from external providers (multiple sources)
- **Care coordination records**: C-CDA documents received/sent, Community Chart external query results, referral-related data from Direct Messaging (interoperability descriptions)
- **Clinical quality data**: CQMs/MIPS measures; disease management reports (e.g., Diabetes HbA1c tracking) (search results)
- **Public health reporting data**: Immunization, syndromic surveillance, cancer cases, reportable conditions (certification criteria)
- **Telehealth encounter data**: Video visit records, e-Visit records (vendor materials)
- **Audit logs**: Implied by (d)(2)–(d)(3) certification for auditable events
- **Patient portal activity**: Portal access records, proxy access, document viewing, payment history (portal blog post)
- **Remote patient monitoring data**: Referenced in webinar listings though details are sparse (webinar search results)

**What was unclear or thin:**
- The vendor website was largely inaccessible via WebFetch (rendered as CSS/JS framework code rather than content), so much information came from third-party review sites, search result snippets, and blog posts rather than detailed vendor feature pages.
- Referral management is not explicitly described as a standalone module, though Direct Messaging and Community Chart clearly support referral-related data exchange.
- The imaging module is listed as "optional" but details about what imaging data is stored (e.g., DICOM, scanned documents, or both) are not clear.
- Detailed claims adjudication workflows and ERA processing are implied by "fully integrated with billing/ERA" but not described in depth.
- Remote patient monitoring is mentioned in webinar topics but no detailed feature description was found.
