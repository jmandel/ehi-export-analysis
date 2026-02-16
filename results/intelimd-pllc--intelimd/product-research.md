# inteliMD PLLC — Product Research

Researched: 2026-02-15
Developer website: https://www.intelimd.com/

## Overview

inteliMD PLLC is a small healthcare technology company headquartered in Phoenix, Arizona (Two North Central Ave, 18th and 19th Floor, Phoenix, AZ 85004). The company describes itself as a "pioneer in integrated telemedicine platforms" that provides "innovative healthcare related software and applications to healthcare providers and patients." The trademark for "INTELIMD" was filed in March 2018 under Class 044 (Medical services), registered to inteliMD PLLC at 5129 W. Pedro Ln, Laveen, AZ 85339.

inteliMD appears to be a very small vendor with minimal market footprint. There are no reviews on G2, Capterra, or other major software review sites. There is essentially no third-party coverage or press mentions. The company does not appear to have a LinkedIn company page. ZoomInfo lists the company but with minimal detail. The web presence suggests a startup/micro-vendor targeting individual providers and small practices with a low-cost, cloud-based platform.

Notably, inteliMD has a related entity called **InteliPsych**, described as "the telepsychiatry arm of InteliMD, a telemedicine company that delivers services across the spectrum." InteliPsych is a national telepsychiatry service provider specializing in crisis telepsychiatry, providing on-demand psychiatric evaluations. This suggests inteliMD operates both as a software platform and as a clinical services organization (PLLC = Professional Limited Liability Company, consistent with a clinical practice entity).

The product was ONC-certified on November 27, 2024 (version 1), making it a very recent certification. The ONC certification page reveals that inteliMD is "specifically designed for the post-acute and primary segment of care" and is optimized for "skilled nursing facilities, home health settings or by their primary care physician." This is a significant detail that doesn't appear prominently on the main marketing website, which emphasizes telemedicine more broadly.

## Product: inteliMD

CHPL ID: 11555

### What It Is

inteliMD is an integrated, cloud-based healthcare platform combining electronic medical records, telemedicine/telehealth, e-prescribing, scheduling, billing, and patient portal capabilities into a single platform. The tagline is "more than telehealth — where patients & providers connect."

Per the ONC certification page, the product is "an ONC certified electronic health record (EHR) specifically designed for the post-acute and primary segment of care." It is described as "a secure, HIPAA compliant, cloud-based platform supported for web application" and is "designed to maximize provider efficiency and to ensure continuity of care and health equity for patients being cared for in skilled nursing facilities, home health settings or by their primary care physician."

The ONC certification page also notes: "inteliMD's technology team has self-developed and certified this software, optimized directly for its provider group, with maximized interoperability and integrations between facility partner EHRs and laboratory partner LIMS platforms." The phrase "optimized directly for its provider group" reinforces that this was built partly for the company's own clinical operations (InteliPsych and related services).

Additional software used for certification: **EMR Direct Interoperability Engine** (for transitions of care / C-CDA exchange).

The certified product is the whole platform — there is no separation between a "certified module" and a larger product. inteliMD is a single integrated system.

The certification is broad, covering 30 criteria including:
- Clinical data: (a)(1) CPOE medications, (a)(2) CPOE labs, (a)(3) CPOE imaging, (a)(4) drug-drug/drug-allergy interaction checks, (a)(5) demographics, (a)(12) family health history, (a)(14) implantable device list
- Transitions of care: (b)(1) and (b)(2)
- Patient access: (e)(1) view/download/transmit, (e)(3) patient health information capture
- Public health: (f)(1) immunization registry reporting
- APIs: (g)(7)-(g)(10) including FHIR
- EHI export: (b)(10)

### Users & Market

The product targets healthcare providers across various practice types and sizes, with the ONC page specifically highlighting post-acute care (skilled nursing facilities, home health) and primary care. The homepage mentions "corporate, institutional or private practice" as target customers.

The pricing tiers (listed on the website) suggest a small-practice/individual-provider market:
- **Basic**: Free (limited features — listing, scheduling, waiting room, telemedicine invitation, online appointments)
- **Intermediate**: $49/physician/month
- **Advance**: $199/physician/month
- **Enterprise**: $299/physician/month ("all access")

All tiers list the same set of features in the pricing table (which appears to be a UI issue — the differentiation between tiers is not clearly displayed). Listed features across tiers include: physician scheduling, patient scheduling, waiting room, telemedicine invitation, online appointments, outpatient telemedicine, credit card processing, patient electronic billing, inpatient telemedicine, electronic eligibility check, electronic medical record, ePrescribe, and electronic claim.

The product has both a web application and mobile app (Apple and Android). The login URL is `accounts.intelimd.com/signin?clientId=ehr-intelimd-app`.

No information about customer count, number of users, or notable deployments was found. The lack of reviews on any third-party platform and the minimal web presence suggest very limited market penetration. InteliPsych (the telepsychiatry arm) may be one of the primary users of the platform.

### Modules & Functionality

Based on the vendor website, ONC certification page, and terms of service, the product includes the following modules/capabilities:

**Electronic Medical Records (EMR)**
- Cloud-based EMR accessible via web and mobile
- Patient health records that can be shared between providers and patients
- Records retained for minimum 6 years per legal requirements, then archived for 4+ years (per T&C)

**Telehealth/Telemedicine**
- Outpatient telemedicine (video and phone consultations)
- Inpatient telemedicine
- Electronic Intensive Care Unit (eICU) capabilities mentioned on homepage
- Virtual waiting room
- Telemedicine invitation system
- Secure video chat and phone conferencing between providers and patients

**E-Prescribing**
- Automated prescription system with E-Prescribe
- Drug-drug and drug-allergy interaction checks (certified under (a)(4))
- CPOE for medications (certified under (a)(1))

**Scheduling & Appointments**
- Online appointment booking (via provider's website or inteliMD website)
- Physician scheduling
- Patient scheduling
- Provider directory ("unlimited provider's directory to accommodate a variety of practice types")

**Billing & Financial**
- Credit card processing (additional fee applies)
- Patient electronic billing / patient statement service
- Electronic claim submission
- Automatic insurance/eligibility verification

**Clinical Decision Support**
- CPOE for lab orders (certified under (a)(2))
- CPOE for imaging orders (certified under (a)(3))
- Drug interaction checks

**Patient Demographics & History**
- Demographics recording (certified under (a)(5))
- Family health history (certified under (a)(12))
- Implantable device list (certified under (a)(14))

**Communication**
- Direct communication with staff, physicians, specialists, and referring physicians
- Secure messaging between providers and patients
- Provider-to-provider communication

**Interoperability**
- Transitions of care via C-CDA (using EMR Direct Interoperability Engine)
- FHIR API access (certified under (g)(10))
- Patient view/download/transmit (certified under (e)(1))
- Immunization registry reporting (certified under (f)(1))
- Integration with facility partner EHRs and laboratory LIMS platforms (per ONC page)

**Voice Recognition**
- Integrated voice recognition dictation for documenting consultations

**Patient Portal**
- Patient registration and account creation (free for patients)
- Access to electronic medical records
- Ability to view health information on demand

**Administrative**
- Customizable, configurable and scalable dashboard
- Configurable administrative functions
- Multi-site support ("unlimited number of sites and employee use")

### Data & Content

Based on the certified criteria, feature descriptions, and legal documents, the product stores and manages:

**Clinical Data** (inferred from certified criteria and features):
- Patient demographics (name, DOB, gender, contact info, address — per (a)(5) and registration form)
- Medication orders and prescriptions (per CPOE (a)(1) and e-prescribing)
- Lab orders (per CPOE (a)(2))
- Imaging/radiology orders (per CPOE (a)(3))
- Drug allergy information (per (a)(4) drug-allergy interaction checks)
- Family health history (per (a)(12))
- Implantable device list (per (a)(14))
- Clinical notes / consultation documentation (per integrated dictation feature)
- Immunization records (per (f)(1) immunization registry reporting)
- Vital signs, problems, medications — implied by transitions of care C-CDA support

**Telemedicine/Communication Data**:
- Video consultation records/logs
- Secure messages between providers and patients
- Communication records between providers

**Financial/Billing Data**:
- Credit card information (per privacy policy: "credit card information or other details for billing")
- Insurance information and eligibility verification results
- Electronic claims
- Patient billing statements
- Payment processing records

**Administrative Data**:
- Provider credentials, DEA license information, state licenses
- Provider scheduling data
- Business information (business name, federal tax ID, incorporation date, business type — per privacy policy)
- SSN (collected per privacy policy for provider identity verification)
- User account information (username, password, email)

**Patient-Generated Data**:
- Patient registration information
- Patient health information captured via portal (per (e)(3))

**System/Technical Data** (per privacy policy):
- IP addresses, browser information, usage logs
- Cookie data
- Device information

The T&C mentions that if a provider's account is canceled, they can still access records, and if access is fully terminated, records can be obtained via fax through support. Records are retained for at least 6 years, then archived for at least 4 years.

The T&C also notes: "InteliMD may also use de-identified data for statistics or marketing purposes," confirming they maintain the ability to de-identify and aggregate clinical data.

**Gaps in information**: The website does not provide detailed information about the specific clinical documentation workflows (e.g., specific note templates, assessment tools, care plans for post-acute settings). Given the ONC page's emphasis on skilled nursing and home health, the product likely stores care plans, functional assessments, and post-acute-specific documentation, but this is not explicitly described on the website. The laboratory LIMS integration mentioned on the ONC page suggests lab results flow into the system, but details are sparse.
