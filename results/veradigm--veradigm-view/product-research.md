# Veradigm — Product Research (Veradigm View)

Researched: 2026-02-16
Developer website: https://www.veradigm.com/

## Overview

Veradigm Inc. (formerly Allscripts Healthcare Solutions, Inc.) is a health IT company headquartered in Chicago, Illinois, with approximately 2,450 employees and ~$585M in annual revenue. The company rebranded from Allscripts to Veradigm in January 2023. In May 2022, Allscripts sold its hospital/large-practice segment (Sunrise, Paragon, TouchWorks, Opal, dbMotion) to Harris Computer/Constellation Software for ~$700M; that business became Altera Digital Health. What remained — ambulatory EHR, e-prescribing, data analytics, life sciences — became Veradigm.

Veradigm's current business has two segments: Provider (~77% of revenue, including EHR, practice management, patient engagement, and revenue cycle) and Payer & Life Sciences (~23%, data analytics and real-world evidence). The company has been through significant turbulence — a $20M revenue overstatement disclosed in March 2023 triggered SEC investigation, executive departures, and eventual Nasdaq delisting in February 2024 (now trades OTC as MDRX). The company claims over 180,000 physician users and holds roughly 3.1–3.6% of the U.S. ambulatory EHR market (7th place per Definitive Healthcare, with ~2,580 installations).

Veradigm acquired Practice Fusion in 2018 for $100M. Practice Fusion was a pioneering cloud-based EHR that had offered a free, ad-supported model before switching to a subscription model. (Allscripts/Veradigm later paid a $145M DOJ settlement related to Practice Fusion's pre-acquisition kickback/opioid marketing issues.)

## Product: Veradigm View

CHPL ID: 11697 (15.04.04.2891.View.01.02.1.250909)

### What It Is

**Veradigm View is the ONC-certified product name for Practice Fusion EHR.** On the Veradigm marketing site and in customer-facing contexts, the product is still called "Practice Fusion EHR." The name "Veradigm View" appears specifically in ONC certification and EHI export documentation. Evidence for this identity:

- The EHI export documentation for Veradigm View internally references "Practice Fusion EHR" in entity descriptions
- The login URL is `app.veradigmview.com` with a dedicated customer community at `help.veradigmview.com`
- The Veradigm EHR Solutions page lists two products: "Veradigm EHR" (formerly Allscripts Professional) and "Practice Fusion EHR" — there is no third product called "Veradigm View"
- The Veradigm login page lists a "Practice Fusion" login, not "Veradigm View"

Practice Fusion / Veradigm View is a 100% cloud-based ambulatory EHR designed for small, independent physician practices. It is positioned as "a simple, intuitive EHR" offering "quick integration and immediate operational efficiency" that "operates effortlessly and requires no dedicated IT support." It is a completely separate product from Veradigm EHR (CHPL 11763, formerly Allscripts Professional), which targets larger multi-specialty organizations with advanced customization needs. The two products have different codebases, different login portals, different data models, and different EHI export formats (View exports TSV files; EHR exports JSON).

The product is certified for 32 ONC criteria covering clinical documentation (a)(1)-(a)(5), (a)(12), (a)(14)-(a)(15), care coordination (b)(1)-(b)(3), (b)(10)-(b)(11), clinical quality measures (c)(1)-(c)(3), patient access (e)(1), (e)(3), public health reporting (f)(1), (f)(5), and FHIR APIs (g)(7), (g)(9), (g)(10). Compared to Veradigm EHR, it lacks certifications for data segmentation (b)(7)-(b)(9), syndromic surveillance (f)(2), electronic case reporting (f)(4), antimicrobial reporting (f)(7), and Direct messaging (h)(1) — consistent with Practice Fusion being a simpler product.

### Users & Market

Practice Fusion / Veradigm View targets solo practitioners and small clinics seeking an affordable, easy-to-use, cloud-based EHR with minimal IT overhead. Veradigm reports over 31,000 clinicians use it, serving approximately 5 million patient visits per month.

On Capterra, Practice Fusion has a 3.7/5 rating based on 429 reviews. Users appreciate the user-friendly interface and affordability. Criticisms include limited customization options, rigid workflows, and inconsistent customer support. The product is popular with small to medium-sized practices that prioritize simplicity over advanced configurability.

### Modules & Functionality

Based on the Veradigm website, EHI export documentation (87 TSV entity types in v6), third-party reviews, and ONC certification criteria:

**Clinical Documentation & Charting**
- Customizable templates for various medical forms and documentation (per vendor marketing and Capterra reviews)
- Encounter documentation with assessments, assessment plans, diagnoses, procedures, observations, events, medications, and addendums (per EHI export entity list)
- Clinical worksheet summaries and details
- Problem lists / conditions and diagnoses
- Patient education records
- Advance directives
- Health concerns and goals
- Care plans
- Pinned notes (clinical sticky notes)
- Smoking status tracking
- Family history
- Healthcare device/implant tracking
- Risk scores (e.g., HCC/RAF)

**Medications & E-Prescribing**
- Electronic prescribing including controlled substances (EPCS) — certified for (a)(1) CPOE
- Medication lists and medication history
- Prescription management and transmission with transaction tracking
- Drug alert override tracking (clinical decision support)
- Pharmacy directory and preferred pharmacy management
- Medication history consent tracking
- Immunization management with VIS (Vaccine Information Statement) edition tracking
- Immunization transmission history (registry reporting)

**Laboratory**
- Lab orders with items, specimens, diagnoses, answers, and order documents
- Lab results with test observations, notes, observation diagnoses, specimen data, and result documents
- Electronic lab results integration (per vendor marketing: integration with laboratory systems)

**Billing & Insurance**
- Integrated billing and claims management described by vendor as "comprehensive" with automation to reduce denied claims (per Veradigm website and EMRSystems review)
- Superbills with associated diagnoses, procedures, modifiers, events, and insurance links (per EHI export entities)
- Patient insurance information and eligibility verification
- Guarantor information
- Financial resource tracking
- Service restrictions

**Patient Engagement**
- Patient portal providing access to health records, lab results, and appointment schedules — certified for (e)(1) VDT
- Patient messaging with attachments and recipients
- Patient questionnaires
- Patient documents
- Free personal health record for patients (per Veradigm marketing)
- Automated appointment reminders (per EMRSystems review)

**Scheduling**
- Appointment scheduling (per vendor marketing: "integrated scheduling")

**Referrals**
- Referral management with recipients

**Telemedicine**
- Telemedicine integration for virtual visits (per Veradigm marketing and third-party reviews; appears to be a more recent addition)

**Analytics & Reporting**
- Analytics and reporting tools for monitoring practice performance and patient outcomes (per vendor marketing)
- Clinical quality measure capture, export, and reporting — certified for (c)(1)-(c)(3)

**Interoperability**
- FHIR R4 API access — certified for (g)(7), (g)(9), (g)(10)
- Transitions of care / C-CDA — certified for (b)(1)-(b)(3)
- Immunization registry reporting — certified for (f)(1)
- Cancer registry reporting — certified for (f)(5)
- EHI bulk data export in TSV format — certified for (b)(10)

**Administrative**
- Provider profiles and user management
- Facility information
- Care team assignment and profiles
- Contact profiles
- Communication settings

### Data & Content

Based on the v6 EHI export documentation (87 TSV files with 1,194 total fields), Veradigm View stores data across these major categories:

| Category | Entity Count | Key Data |
|---|---|---|
| Demographics | 10 | Communication settings, occupation, appointments, contacts, demographics, ethnicity, financial resources, gender identity/sexual orientation, race, tribal affiliation |
| Patient Records | 2 | Documents, questionnaire responses |
| Clinical Data | 31 | Care team, facilities, advance directives, allergies/reactions, clinical worksheets, conditions, diagnoses, education, encounters (with assessments, procedures, observations, events, addendums, medications, documents), family history, goals, healthcare devices, health concerns, immunizations, risk scores, smoking status, pinned notes, providers/users |
| Billing & Insurance | 13 | Contact profiles, encounter documents, guarantor, insurance eligibilities, insurances, restrictions, superbills (with diagnoses, procedures, modifiers, events, insurances) |
| Medications | 12 | Immunization VIS editions, drug alert overrides, encounter medications, immunization transmission history, medication history, medication history consent, medications, prescriptions, pharmacies, preferred pharmacy, prescription transactions |
| Labs | 16 | Lab orders (with items, diagnoses, answers, specimens, documents), lab results (with items, notes, test observations, observation diagnoses, specimen data, documents) |
| Referrals | 2 | Referral recipients, referrals |
| Messaging | 3 | Message attachments, message recipients, messages |

The EHI export documentation is the strongest evidence for what data the product stores, since it maps directly to database entities. The 87 entity types cover a comprehensive ambulatory EHR data model appropriate for small practices: clinical encounters, medications/prescriptions, lab orders/results, billing/superbills, insurance, patient messaging, referrals, immunizations, and demographic data.

**Notable observations about data scope:**
- Billing data is present (superbills, insurance, eligibility) but appears practice-management-oriented rather than full RCM — consistent with a small-practice product where billing may be handled by a clearinghouse or external service
- Messaging is built into the product (3 entities), not just through FollowMyHealth patient portal
- Lab integration appears robust (16 entities covering orders and results with detailed observation-level data)
- Scheduling data is relatively light in the export — appointments appear under demographics rather than as a rich scheduling module, suggesting basic scheduling capability

---

## Product Ecosystem Context

Veradigm maintains five separately ONC-certified products:

| Product | CHPL ID | Former Name | Target Market |
|---|---|---|---|
| Veradigm EHR | 11763 | Allscripts Professional | Multi-location, multi-specialty |
| **Veradigm View** | **11697** | **Practice Fusion** | **Small, independent practices** |
| Veradigm FollowMyHealth | 11609 | FollowMyHealth | Patient engagement portal (EHR-agnostic) |
| Veradigm ePrescribe | 11632 | Allscripts ePrescribe | Standalone e-prescribing |

FollowMyHealth is the shared patient engagement platform that can integrate with either EHR product. ePrescribe is available both embedded and standalone. Veradigm View/Practice Fusion and Veradigm EHR are completely separate products with different codebases, data models, and target markets despite sharing a parent company.
