# QRS, Inc. — Product Research

Researched: 2026-02-16
Developer website: https://qrshs.com/

## Overview

QRS, Inc. (Quality Rep Services, Inc.) is a privately held healthcare IT company founded in 1983 by Rusty Dickerson, headquartered in Knoxville, Tennessee. The company has approximately 51–200 employees (per LinkedIn) and over 40 years of operational history. QRS specializes in practice management and electronic health record solutions for ambulatory physician practices, targeting small private practices and revenue cycle management (RCM) billing companies.

In May 2024, QRS joined Harris Computer (a Constellation Software subsidiary known for acquiring vertical market software businesses), according to LinkedIn. However, this acquisition is not prominently listed on Harris Computer's healthcare portfolio page, and QRS continues to operate under its own brand. The vendor also uses DGV Services as a reseller/channel partner for PARADIGM products.

QRS's customer base appears to be small ambulatory practices across a wide range of specialties. No specific customer counts or notable deployments were found in public sources. The company's web presence is modest — the main website (qrshs.com) had an expired SSL certificate at the time of research, which may indicate limited IT resources or a post-acquisition transition.

## Product: PARADIGM®

CHPL ID: 11142

### What It Is

PARADIGM is an integrated EHR and Practice Management (PM) suite designed for ambulatory physician practices. It is ONC-ATCB certified and consists of two main components that share a single database:

- **PARADIGM EHR** — the electronic health record / clinical module
- **PARADIGM PM (PARADIGM+)** — the practice management / billing module

The certified module covers the full product — both EHR and PM — since they share a single integrated database. The product is described as cloud-based (per SourceForge/Capterra listings). The certification covers 37 criteria spanning clinical documentation (a), care coordination (b), clinical quality measures (c), patient access (e), public health reporting (f), API/FHIR access (g), and direct messaging (h), indicating this is a comprehensive ambulatory EHR+PM platform.

### Users & Market

PARADIGM targets ambulatory practices, primarily small to mid-size physician offices. The product supports an extremely broad list of specialties (per vendor website and DGV Services): Family Medicine, Internal Medicine, Pediatrics, Cardiology, Dermatology, OB-Gyn, Orthopedics, Psychiatry, Ophthalmology, Urology, Pain Management, Chiropractic, Allergy, Behavioral Health, Oncology, Gastroenterology, Neurology, Podiatry, Rheumatology, Radiology, Urgent Care, SurgiCenter, and many more (~50+ specialties listed).

End users include physicians, clinical staff (for charting, prescriptions, patient flow), and administrative/billing staff (for scheduling, claims, billing). The product also has a patient-facing portal.

No reliable customer count or market share data was found. Third-party reviews are sparse — SourceForge shows 1 review (1/5 stars, a physician who found it "slow and cumbersome"), and Capterra shows 1 review with a 3/5 features rating. This suggests a small user base without significant market presence on review platforms. One user testimonial (from the vendor's own materials) mentioned using PARADIGM for 13+ years for filing claims and producing management reports.

### Modules & Functionality

**PARADIGM EHR (Clinical Module):**
- **Clinical documentation / note generation**: Customizable templates built to mirror practice workflow. Quick data entry options. Integrates scanning, electronic documents, note generation, and workflow into one system (vendor website via DGV Services).
- **Speech recognition**: Verbal input of data to reduce keyboard entry errors. Voice files stored as .wav files tied to specific encounters that can be filed in any tab section of the patient's chart and transcribed to text (vendor website).
- **E-prescribing**: Integrated e-prescribing sends prescriptions directly to pharmacies electronically. Access to the full FDA drug database with drug uses, side effects, precautions, interactions, and overdose information (vendor feature page via search results).
- **Patient flow / work lists**: Patient flow management, work lists, and patient search functionality (DGV Services listing).
- **Custom chart layout**: Configurable chart tabs and sections (DGV Services listing).
- **Scanning and document management**: Store virtually any type of file (documents, scanned images, audio, video) securely in a patient's record. Eliminates paper copies (vendor website).
- **Dictation**: Voice dictation capabilities in addition to speech recognition (DGV Services listing).
- **Fax integration**: Electronic fax capabilities (DGV Services listing).
- **Recalls/follow-up**: Patient recall and follow-up tracking (DGV Services listing).
- **Patient portal**: Secure portal where patients access health records, schedule appointments, and communicate with the practice (vendor website). A portal login exists at portal.qrshs.com.

**PARADIGM PM (Practice Management Module):**
- **Appointment scheduling**: Easy-to-use scheduling with built-in reminders to reduce no-shows (vendor website).
- **Billing / charge posting**: Single-screen concept for posting charges, payments, adjustments, messages, and notes to encounters (vendor website via search results).
- **Claims management**: Claims scrubbing, electronic claims submission, and direct access to the QRS Clearinghouse (vendor website).
- **Electronic remittance advice (ERA)**: Processing of insurance payments electronically. One testimonial noted "substantial increase in collections per procedure and overall revenue" from using this feature.
- **Insurance eligibility verification** (SourceForge feature listing).
- **Patient billing / guarantor billing** (vendor product suite description).
- **Multi-physician and multi-office support** (SourceForge feature listing).
- **E/M coding assistance** (SourceForge feature listing).
- **Inventory management** (SourceForge feature listing).

**Optional Modules / Add-ons (per DGV Services):**
- HL7 interfaces (lab, radiology, etc.)
- Insurance contract management
- Referral management
- Claims tracking
- Specialty-specific modules for radiology, allergy, chiropractic, and ambulance billing

**Certified Capabilities (from CHPL criteria):**
- CPOE for medications (a)(1) implied by other criteria — note: (a)(1) not listed, but (a)(2) drug-drug/drug-allergy checks, (a)(3) demographics, (a)(5) problem list are certified
- Drug-drug, drug-allergy interaction checking — (a)(2)
- Demographics — (a)(3)
- Problem list — (a)(5)
- Family health history — (a)(12)
- Implantable device list — (a)(14)
- Transitions of care — (b)(1), (b)(2)
- Clinical information reconciliation — (b)(7)
- Electronic notifications — (b)(8)
- EHI export — (b)(10)
- Bulk data export — (b)(11)
- Clinical quality measures — (c)(1), (c)(2), (c)(3)
- Patient portal / view-download-transmit — (e)(1)
- Patient health information export — (e)(3)
- Immunization registry reporting — (f)(1)
- Syndromic surveillance — (f)(2)
- Cancer case reporting — (f)(5)
- FHIR API access — (g)(7), (g)(9), (g)(10)
- Direct messaging — (h)(1)

### Data & Content

Based on the evidence gathered, PARADIGM stores and manages the following types of data:

**Clinical data** (evidenced by EHR features and certified criteria):
- Patient demographics (certified (a)(3))
- Problem lists (certified (a)(5))
- Family health history (certified (a)(12))
- Implantable device list (certified (a)(14))
- Clinical notes / encounter documentation (note generation feature, customizable templates)
- Prescriptions / medication data (e-prescribing feature, drug database, drug interaction checks)
- Drug-drug and drug-allergy interaction data (certified (a)(2))
- Voice recordings (.wav files stored per encounter)
- Scanned documents and images (scanning/document management)
- Electronic documents and faxes (fax integration feature)

**Administrative/billing data** (evidenced by PM features):
- Appointment/scheduling data
- Charges, payments, and adjustments
- Insurance claims and electronic remittance
- Insurance eligibility data
- Patient/guarantor billing records
- Encounter-level messages and notes
- Referral data (optional module)
- Insurance contract data (optional module)
- Inventory data

**Patient portal data** (evidenced by portal feature and (e)(1) certification):
- Patient-accessible health records
- Patient-provider messages
- Appointment requests

**Public health reporting data** (evidenced by (f) criteria):
- Immunization data (certified (f)(1))
- Syndromic surveillance data (certified (f)(2))
- Cancer case data (certified (f)(5))

**Integration/exchange data** (evidenced by (b), (g), (h) criteria):
- C-CDA documents for transitions of care
- FHIR resources via API
- Direct messages
- HL7 interface data (lab results, etc. — optional module)

**Gaps in evidence**: The vendor website does not explicitly mention lab orders/results management as a built-in feature (HL7 interfaces for labs are listed as an optional add-on module). It's unclear how deep the imaging/radiology integration goes beyond the optional radiology module. The vendor site was largely inaccessible due to an expired SSL certificate, limiting the depth of research possible from primary vendor sources.

---

## Research Notes

- The primary vendor website (qrshs.com) had an expired SSL certificate, preventing direct access to product pages, the mandatory disclosures page, feature detail pages, and a PDF product document. Research relied heavily on search result snippets, cached content, third-party sites (DGV Services reseller, SourceForge, Capterra), and LinkedIn.
- QRS reportedly joined Harris Computer in May 2024 (per LinkedIn), but this is not confirmed on Harris's website.
- The product appears to be a modest-scale ambulatory EHR+PM serving small practices. Very few third-party reviews exist, suggesting limited market penetration.
- The broad specialty list and optional modules suggest configurability for different practice types, but the depth of specialty-specific functionality is unclear.
