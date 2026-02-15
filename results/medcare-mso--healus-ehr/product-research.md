# Medcare MSO — Product Research

Researched: 2026-02-15
Developer website: https://medcaremso.com

## Overview

Medcare MSO is a healthcare revenue cycle management (RCM) and medical billing company founded in 2012 and headquartered in Irvine, California. The company employs 501–1,000 people across offices in the US and Pakistan. Their primary business has historically been outsourced medical billing, revenue cycle management, and practice management services — they claim to serve "over 80,000 healthcare facilities" and "150,000 providers." The company reports a 98.5% first-pass clean claims rate and 96% collection ratios.

Medcare MSO's core go-to-market is providing billing and RCM services that work *with* third-party EHR systems. Their website features dedicated service pages for billing on top of NextGen, athenahealth, Cerner, Tebra/Kareo, Practice Fusion, AdvancedMD, and others — suggesting that many of their clients use other vendors' EHR products while Medcare MSO handles the billing/RCM layer.

More recently, Medcare MSO has been developing its own software products:
- **Maximus** — a web-based practice management and billing platform (announced June 2024)
- **HealUs EHR** — a cloud-based electronic health record system (ONC certified July 2024)
- **AI Scribe** — clinical documentation automation
- **AI Medical Coding** — automated coding solutions

HealUs EHR appears to be a relatively new, in-house-developed EHR product that Medcare MSO built to complement its existing billing/RCM services. The ONC certification was obtained in July 2024, making it quite new to market.

## Product: HealUs EHR

CHPL IDs: 11495

### What It Is

HealUs EHR is a cloud-based electronic health record system designed for ambulatory healthcare providers. The product website (healusehr.com) describes it as "designed by and for healthcare providers" with an emphasis on ease of use and quick setup — claiming users can be operational "in minutes, not days" with no downloads or installations required.

The product is broadly certified — it holds ONC certifications across 37 criteria spanning clinical (CPOE, drug interactions, demographics, implantable devices), care coordination (transitions of care, clinical information reconciliation, e-prescribing), patient engagement (patient portal with view/download/transmit), clinical quality measures, public health reporting (immunization registry, syndromic surveillance), and FHIR APIs.

The certified module appears to be the EHR itself, though it's clearly designed to work within a broader ecosystem that includes Medcare MSO's Maximus practice management software and their billing/RCM services. The ONC mandatory disclosures page lists three additional software dependencies:
- **DrFirst** — for e-prescribing (DrFirst is a major e-prescribing platform used by 100,000+ prescribers across 270+ EHR systems)
- **EMR Direct Interoperability Engine 2023** — for Direct messaging / secure health information exchange
- **AccessGUDID** — for the FDA's Global Unique Device Identification Database (required for implantable device list functionality)

### Users & Market

The intended user base per the ONC filing includes: "Healthcare Providers, Health IT Administrators, Patients, Pharmacists, Public Health Officials." The healusehr.com website lists target customers as ambulatory care providers, hospitals, health systems, billing companies, and management companies.

Given Medcare MSO's existing customer base of billing clients across "50+ specialties," HealUs EHR likely targets a similar market: small to mid-size ambulatory practices, particularly those already using Medcare MSO for billing services. The product's emphasis on rapid setup and cloud deployment suggests a focus on smaller practices rather than large health systems.

No third-party reviews of HealUs EHR were found on G2, Capterra, or other review platforms. Software Finder lists Medcare MSO's software (referring to Maximus) with a single 5-star review. The absence of reviews likely reflects the product's newness (certified July 2024).

No specific customer deployments or case studies for HealUs EHR were found during research.

### Modules & Functionality

The HealUs EHR website describes six core feature areas:
1. **Scheduling** — appointment and calendar management
2. **Charting** — patient data documentation
3. **Eligibility Verification** — insurance coverage verification
4. **Clinical Decision Support System (CDSS)** — integration of clinical knowledge with patient data
5. **Interoperability** — data exchange between systems
6. **Electronic Referrals** — referral management

The ONC certification criteria provide more specificity on clinical capabilities:
- **CPOE** for medications, laboratory orders, and diagnostic imaging orders — criteria (a)(1)-(a)(3)
- **Drug-drug and drug-allergy interaction checks** — criterion (a)(4)
- **Demographics recording** — criterion (a)(5)
- **Implantable device list** — criterion (a)(14), using AccessGUDID integration
- **E-prescribing** — criterion (b)(11), via DrFirst integration
- **Transitions of care** — criterion (b)(1), including C-CDA document creation
- **Clinical information reconciliation** — criterion (b)(2), for medications, allergies, and problems
- **Electronic prescribing** — criterion (b)(11)
- **Patient portal (view/download/transmit)** — criterion (e)(1), allowing patients to view, download, and transmit their health information
- **Patient health information capture** — criterion (e)(3)
- **Clinical quality measures** — criteria (c)(1)-(c)(3), supporting 7 CQMs including depression screening (CMS2), blood pressure screening (CMS22), medication documentation (CMS68), BMI screening (CMS69), fall risk screening (CMS139), hypertension control (CMS165), and HIV screening (CMS349)
- **Public health reporting** — immunization registry transmission (f)(1) and syndromic surveillance (f)(2)
- **FHIR API access** — criteria (g)(7)-(g)(10), including patient selection and bulk data access APIs
- **Direct messaging** — criterion (h)(1), via EMR Direct Interoperability Engine

The broader Medcare MSO ecosystem adds:
- **Maximus** practice management software with billing, claims management, payment posting, A/R tracking, Power BI analytics dashboards, and HL7 integration
- **AI Scribe** for clinical documentation
- **AI Medical Coding** for automated coding

The Medcare MSO website also mentions telehealth, SOAP notes, mobile charting, and reporting/dashboards as part of their EHR/EMR capabilities, though it's not always clear whether these features are in HealUs EHR specifically or in the broader Medcare MSO service offering.

### Data & Content

Based on the certified criteria and described features, HealUs EHR stores and manages:

**Clinical Data (from certification criteria):**
- Patient demographics (a)(5)
- Medication orders and prescriptions, including e-prescriptions via DrFirst (a)(1), (b)(11)
- Laboratory orders (a)(2)
- Diagnostic imaging orders (a)(3)
- Drug-drug and drug-allergy interaction data — implying allergy lists and medication lists (a)(4)
- Implantable device information via AccessGUDID (a)(14)
- Problems/conditions, medications, and allergies for reconciliation (b)(2)
- Clinical notes/charting (described on website)
- Clinical quality measure data for 7 CQMs (c)(1)-(c)(3) — including depression screening results, blood pressure readings, BMI data, fall risk assessments, HIV screening data, and medication documentation

**Care Coordination Data:**
- Transitions of care documents / C-CDAs (b)(1)
- Referral information (described on website)
- Direct messages for health information exchange (h)(1)

**Patient-Facing Data:**
- Patient portal content for view/download/transmit (e)(1)
- Patient-submitted health information (e)(3)

**Public Health Data:**
- Immunization records for registry reporting (f)(1)
- Syndromic surveillance data (f)(2)

**Administrative Data (from website and Maximus integration):**
- Scheduling/appointment data
- Insurance eligibility information
- Clinical decision support rules and alerts

**What's less clear:**
- Whether billing and claims data live in HealUs EHR or in the separate Maximus PMS. Medcare MSO is primarily a billing company, and Maximus is their dedicated practice management/billing tool. The HealUs EHR website does not prominently feature billing capabilities, suggesting billing may be handled by Maximus rather than within the EHR itself.
- Whether lab results (as opposed to lab orders) are stored in HealUs EHR. The system is certified for CPOE for lab orders, but it's unclear whether it also receives and stores results.
- The extent of document/image storage — the website mentions charting but doesn't detail document management or image storage capabilities.
- Whether the AI Scribe and AI Medical Coding products are integrated into HealUs EHR or are separate tools.
- The patient messaging/communication capabilities — it's unclear whether there is in-app messaging beyond the patient portal's view/download/transmit functionality.

---

## Relationship Between Products

Medcare MSO appears to be building an integrated suite:
- **HealUs EHR** = clinical EHR (the ONC-certified component)
- **Maximus** = practice management and billing
- **AI Scribe** = clinical documentation automation
- **AI Medical Coding** = automated coding

These appear to be marketed as complementary products rather than a single monolithic platform. The ONC certification is for "HealUs EHR" specifically, so the EHI export obligation under §170.315(b)(10) would cover all electronic health information storable by the product of which HealUs EHR is a part — which likely includes data from the integrated Maximus PMS if they're sold as a single product, but this boundary is somewhat ambiguous given that Medcare MSO markets these as distinct products.

## Research Gaps

- **Very limited independent information.** HealUs EHR is a new product (certified July 2024) with no third-party reviews, no case studies, and minimal online presence beyond the vendor's own websites.
- **Product boundaries are unclear.** The relationship between HealUs EHR and Maximus PMS — whether they share a database, are sold together, or are truly separate products — is not well documented.
- **Feature depth is unknown.** The healusehr.com website is sparse, listing feature categories without much detail. The ONC certification criteria tell us what the system was tested for, but not the full scope of functionality.
- **No user community or discussion** found online about HealUs EHR, consistent with it being very new to market.
