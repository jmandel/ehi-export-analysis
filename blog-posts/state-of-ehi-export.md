# What 217 Certified EHRs Actually Export

*A caveat up front: evaluating EHI export documentation is hard. Vendors' published specs are often cryptic, limited, or use product-specific terminology that's unfamiliar even to domain experts. AI-assisted analysis of these documents is a best-effort understanding, not a definitive audit. If any product assessment below is in error, I'd welcome the correction — [file an issue](https://github.com/jmandel-bot/ehi-export-analysis/issues/new) or [message me on LinkedIn](https://www.linkedin.com/in/joshuamandel/).*

Under the [21st Century Cures Act](https://www.congress.gov/bill/114th-congress/house-bill/34/text/pl) and [its implementing regulations from HHS](https://www.healthit.gov/topic/laws-regulation-and-policy/health-it-legislation-and-regulations), every certified EHR must be able to export **all** of a patient's electronic health information (["(b)(10)"](https://www.healthit.gov/test-method/electronic-health-information-export) is the shorthand). Everything the system stores, in a computable format, with public documentation describing what the export contains. I examined the published (b)(10) documentation for 217 certified EHR product families. Over half describe nothing more than a relabeled clinical summary.

## Why this matters more than it used to

Clinical summaries have always been lossy by design. A C-CDA or FHIR US Core document captures the highlights: the problem list, the med list, the recent labs. That's genuinely useful for provider-to-provider handoffs and population health queries. But the use cases emerging now need more than highlights.

Consider:

- **Surprise billing.** A patient trying to understand a surprise medical bill needs the actual charge detail, claim submissions, and denial history — data that has no representation in any standard clinical exchange format.
- **Cancer navigation.** An AI agent helping a patient navigate a complex cancer diagnosis needs the oncology staging data, the chemo regimen details, the radiation treatment plans, not just "Condition: malignant neoplasm of breast" on a problem list.
- **Behavioral health research.** A researcher studying treatment-resistant depression needs structured data from behavioral health EHRs: which therapeutic modalities were attempted (CBT, DBT, EMDR) and for how many sessions, ECT or TMS treatment parameters if tried — none of which has a comprehensive USCDI representation.
- **Longitudinal AI assistance.** An AI health assistant reviewing a patient's history needs the portal message threads where the patient reported worsening side effects and the doctor adjusted the treatment plan; those conversations are part of the clinical narrative but vanish from a standard summary.

These use cases all build on the same legal foundation: the patient's right under HIPAA to access their [Designated Record Set](https://www.ecfr.gov/current/title-45/subtitle-A/subchapter-C/part-164/subpart-E/section-164.501), which (b)(10) requires certified EHRs to export in computable form. The regulation was written before the current AI moment, but it defines what goes in the box that AI agents, personal health applications, and other downstream consumers need: a patient's *whole* record, not just the summary. This post examines what vendors are putting in the box. A separate question — how patients actually get it delivered — matters too, and I'll return to it.

So: does it?

## What I did

Over 600 certified health IT products attest to (b)(10). ONC maintains a public registry of these products (the [Certified Health IT Product List](https://chpl.healthit.gov/), or CHPL) where each one posts a URL to its export format documentation. Many of those 600+ are narrow-scope modules: a standalone patient portal, a quality measure calculation engine, an API adapter. To focus on products that function as fairly complete EHRs, I filtered for those also certified for CPOE [(a)(1)–(a)(3)](https://www.healthit.gov/test-method/computerized-provider-order-entry-cpoe-medications) and the standardized FHIR API [(g)(10)](https://www.healthit.gov/test-method/standardized-api-patient-and-population-services), a rough proxy for a typical clinical capability set.

That leaves 265 CHPL-certified products, which I grouped into 217 product families. (Products sharing an EHI documentation URL and developer are one family; MEDITECH Expanse 2.1 and 2.2 are a single family; MEDITECH Expanse and MEDITECH Client/Server are different families because they have different export architectures.)

![EHI Export Analysis Pipeline](pipeline-diagram.svg)
*The full pipeline: CHPL registry → filter and deduplicate → phased collection → deep analysis → structured summary → public dashboard.*

For each family, an AI agent researched the vendor and product, then navigated to the registered documentation URL and downloaded everything it found: PDFs, HTML pages, data dictionaries, schema files. A separate agent then performed a deep analysis: what does the export actually contain? How does it compare to what the product stores? Is this a genuine EHI export or a relabeled clinical summary?

Everything is open source. The [dashboard](https://jmandel-bot.github.io/ehi-export-analysis/) has the full results; the [repository](https://github.com/jmandel-bot/ehi-export-analysis) has the methodology, prompts, and raw data.

*A note on method: I evaluated documentation, not actual export files. Actually requesting and receiving a (b)(10) export remains difficult in practice — most require a manual request to the health system, often with weeks of turnaround — which is one reason this analysis is limited to what vendors publish. When this post says an export "includes" or "omits" something, it means the vendor's published documentation does or doesn't describe it. Some vendors may export more than they document, but the point of the (b)(10) documentation requirement is that patients and developers can assess an export's contents without running it. If it's not documented, it doesn't exist for accountability purposes.*

## 217 products, graded

| Grade | Count | What it means |
|-------|-------|---------------|
| A / A- | 28 (13%) | Purpose-built, comprehensive, documented |
| B+ / B / B- | 35 (16%) | Real effort, notable gaps |
| C+ / C / C- | 36 (17%) | Partial; some substance, significant holes |
| D+ / D / D- | 104 (48%) | Minimal or stub |
| F | 14 (6%) | Nothing meaningful |

Over half of the EHR products analyzed (products certified by ONC, attesting to a federal requirement, serving real patients) have (b)(10) export documentation that either describes what amounts to a clinical summary relabeled as "all EHI" or is too thin to evaluate at all.

The most common single grade is a plain D, at 58 products (27%). These are the textbook cases: a C-CDA clinical summary or (g)(10) FHIR API relabeled as the (b)(10) export, with no data dictionary, no specialty data, and usually no billing.

## Billing as litmus test

Almost every EHR in this cohort handles billing: charge capture, claim submission, payment posting, denial management. Billing data is squarely part of the Designated Record Set. And it has no representation in C-CDA or USCDI: there's no C-CDA template for a superbill, no US Core profile for a claim denial.

So billing is a natural litmus test. If a vendor's documentation describes billing data in the export, they built something beyond their existing clinical exchange infrastructure. If it doesn't, they probably relabeled what they already had.

Of the 190 products in this cohort that handle billing, **100 (53%) do not document its inclusion in their export**. This is data the product stores, data that's part of the patient's legal record, data that patients increasingly need for dispute resolution and financial planning, and data that simply cannot be delivered through existing clinical exchange formats. Its absence from the documentation is the clearest signal that an export was not purpose-built.

### When vendors export billing, they export *a lot*

Billing often turns out to be the single largest domain in the entire export:

- **Epic** exports 1,286 billing and revenue cycle tables with 12,367 columns. This single domain exceeds most vendors' *entire* exports.
- **Altera Sunrise** dedicates 917 tables to billing, 33% of everything in the export.
- **Greenway Prime Suite** includes 192 billing tables. Their `CFBClaimInfo` table has 435 fields, the single largest entity in the export.
- **eClinicalWorks** exports 161 billing tables, including state-specific Medicaid claim forms: a NY Workers' Comp C-4.3 at 218 fields, a UB-04 institutional claim at 127 fields.
- **Juno Health**: the three largest tables in the entire export are all billing. `RCMUB04CLAIM` (260 fields mapping every box on the UB-04 form), `RCM1500CLAIM` (116 fields), `BILLINGITEM` (115 fields).

Smaller vendors get this right too. MDVita (24 entities total) is a claims-adjudication company turned EHR vendor; their `Claims` entity has 85 fields with granular EOB data. athenahealth defined 9 custom FHIR resource types specifically for billing (506 fields including charges, collections, eligibility, and payment plans), proving you can do this in FHIR if you actually do the mapping work.

### And when they don't

Sometimes the irony is hard to miss:

- **MaxRemind (Maximus EHR)**: a billing company's EHR. Export: repackaged (g)(10) FHIR plus two undocumented Excel files. Zero billing data.
- **ClaimPower**: the company name says it. Export: C-CDA clinical summary, 502 words of screenshot walkthroughs. Zero claims or payment data.
- **Radysans**: full eBilling module with 2,500+ payer connections. Export: one-page doc listing C-CDA sections.
- **Vohra Wound Physicians**: the company name includes "Coding." Billing data entirely absent from the documentation.

## Specialty EHRs and their specialty data

Specialty EHRs are where the stakes are clearest. These products exist to capture domain-specific clinical data, and some vendors export it beautifully.

**ModMed's gGastro** (GI/endoscopy) has a `Finding` table with 155 fields per endoscopic finding: polyp size, morphology, location, removal method, EUS staging, Barrett's esophagus measurements. The export also covers GI-specific quality registries (GIQuIC colonoscopy quality, AGA registry) and IBD disease tracking with Montreal Classification and HBI scoring.

**ModMed's EMA** (ophthalmology) exports 25 pretesting tables with fields like `near_point_conv_blur`, `near_point_conv_break`, `near_point_conv_recover` (the full binocular vision workup), plus per-eye diagnostic drop tracking (`tropicamide_1_phenylephrine_2_5_od`), color vision plate-by-plate results, and cover test data across 9 gaze positions.

**nAbleMD** (fertility/IVF) exports 30 IVF-specific entities. A single `emrcycle` table tracks a treatment cycle in 231 fields from egg source through stimulation, retrieval, ICSI, culture, and transfer, down to catheter depth and whether there was mucus in the sheath. The embryology tables grade each oocyte on inner cell mass, zona pellucida, fragmentation, and multinucleation. There are fields for TMRW robotic cryostorage barcodes, SCSA sperm DNA fragmentation scores, and donor phenotyping (`RomanNose`, `dimples`, `CleftChin`).

**Flatiron OncoEMR** has a `DoseCalculationHistory` table that models the full pharmacology pipeline: BSA calculation, AUC/carboplatin dosing from creatinine clearance, then the dose cascade from regimen value through adjustment percentage to final rounded dose. It tracks AJCC staging with clinical vs. pathologic differentiation, treatment pathway concordance against NCCN guidelines, and lifetime cumulative drug exposure for agents with toxicity limits.

These vendors looked at what their products actually capture and built exports that cover it.

Not every specialty vendor did the work.

**EndoVault** (also endoscopy/GI): stores HD images, 4K video, bowel prep scores, polyp characteristics, scope tracking via RFID. The export: zero endoscopy data. The 138-page "EHI" documentation is the (g)(10) FHIR API spec relabeled; 18 standard FHIR resources, identical to any generic EHR.

**EyeMD** (also ophthalmology): 2024 Best in KLAS winner. Integrates Zeiss, Heidelberg, and Topcon imaging devices. Export: 25 standard FHIR resources, zero ophthalmology data. Their mandatory disclosures describe (b)(10) as "Ability to send CCDA information to other systems via secure transmission," literally conflating EHI export with transitions of care.

**TheraOffice** (PT/OT/SLP, Netsmart): serves 900+ rehab practices. 16 of 19 export tables are named `PAT_PROFILE_USCDI_*`, the clearest possible confession that this is USCDI relabeled as EHI. Zero therapy evaluations, zero outcome measures, no LEFS, no DASH, no NDI, no Oswestry.

**ARIA CORE** (radiation oncology, Varian/Siemens): the dominant US radiation oncology system. Registered EHI documentation URL returns 404. It has never been captured by the Wayback Machine.

The specialty data exists in all of these systems; it's what they're built to capture. The difference is whether the vendor did the work.

## Behavioral health

Behavioral health deserves specific attention. These products handle some of the most sensitive clinical data: psychosocial assessments, suicide risk screenings, substance use treatment records, psychiatric treatment plans. Most of this data has no C-CDA representation. And behavioral health records carry additional privacy protections under [42 CFR Part 2](https://www.ecfr.gov/current/title-42/chapter-I/subchapter-A/part-2) that make portability *more* important, not less; patients need to be able to verify what their providers have on file.

The pattern is consistent: a handful of behavioral health EHRs did it well, and the rest ship generic C-CDA with zero behavioral health content.

Qualifacts' **CareLogic** (A-) shows what a serious BH export looks like. It has dedicated tables for clinical instruments: `MOD_CIWA_AR` with field-by-field alcohol withdrawal scoring (`NAUSEA`, `TREMOR`, `PAROXYSMAL_SWEATS`, `TACTILE_DISTURBANCES`), `MOD_CAGE_AID` for substance screening, `MOD_CAFAS` for child functional assessment with fields like `SELF_HARM_BEHAVIOR` and `FIRE_SETTING_BEHAVIOR_YN`. A 42-field risk-of-harm table tracks suicidal ideation (`SELF_PLAN`, `SELF_MEANS`, `SELF_CONTRACT` for safety contracting). There's multi-layered substance use tracking with per-substance detail down to route of administration, age of first use, and whether the patient used in the previous 48 hours. Twelve tables cover court-ordered treatment (`DOCKET_NUMBER`, `DEFENDANT_COOPERATE`, `BLOOD_ALCOHOL_LEVEL`). And roughly 50 tables handle state-specific BH program reporting (Ohio MACSIS, Colorado CCAR, Indiana HAP), the actual data feeds community mental health centers submit to state authorities. Qualifacts' **Credible** (also A-) exports similar depth. These products prove comprehensive BH exports are feasible.

Then there's the rest. **Streamline SmartCare** (Netsmart) is an EHR built specifically for community behavioral health and human services. Its export contains nothing behavioral-health-specific: no treatment plans with the "golden thread" linking diagnosis to interventions, no BH progress notes, no screening tools (PHQ-9, AUDIT, DAST), no substance use disorder treatment records, no case management. The export covers standard clinical domains only, roughly 10–15% of what the product stores.

The same pattern repeats across **CarePaths** (D), **Core Solutions** (D), **Ehana** (D), **Foothold** (D). Each is a purpose-built behavioral health platform. Each exports a generic clinical summary.

## Portal messages aren't in your record

Of the 193 products that appear to include messaging functionality, 123 (64%) have no clear documentation of how patient communications are included in the export. Only 70 (36%) document their inclusion.

This is data that patients generated: messages sent to their doctors, responses received, portal interactions. It's unambiguously part of the Designated Record Set. Even among otherwise strong exports, it's a common gap: **PointClickCare** (A-, 48 entities) lacks clear documentation of patient communications despite an otherwise substantial export.

## What serious looks like

Twenty-eight product families earned an A or A-. They span from the largest EHR vendors to solo developers. A few examples:

- **Oracle Health (Millennium)**: 6,853 tables, 130,853 columns, 99.9% description coverage, three complementary export pathways. The gold standard for documentation depth.
- **Epic**: 7,672 tables, 63,121 columns, 100% descriptions. The Clarity data model exported as TSV with full field documentation.
- **eClinicalWorks**: 1,466 tables, 21,143 fields. Billing at 161 tables, clinical at 350+.
- **Greenway Prime Suite**: 1,026 tables, 11,868 fields.
- **athenahealth**: a purpose-built FHIR export with 9 custom financial resource types, proving you can do this in FHIR if you invest in the mapping.
- **Crystal Practice Management** (ABEO, 80 entities): a small ENT vendor with a 921-page data dictionary. 58 tables covering clinical, billing, VSP insurance, and ophthalmology supply chain. Size doesn't determine effort.
- **OpenEMR**: 322 entities, 4,941 fields. Community-maintained, open-source, and more thoroughly documented than most commercial vendors.

The point isn't that every product needs thousands of tables. The point is that if a product has fields driving its UI, its clinical decision support, and its specialty workflows, and the documented export offers only a fraction of them, that's not a comprehensive export. The vendors above looked at what their products actually store and built exports that cover it. That's what the regulation requires.

## What's in the box

The (b)(10) requirement is the regulatory infrastructure for a patient's right to get their full record in computable form. As AI capabilities expand (cancer navigation, behavioral health transitions, billing dispute resolution, longitudinal health monitoring), the value of that full record grows with them. Clinical summaries are a fine starting point, but they are not the ceiling.

For the 29% of products graded A or B, the box is packed well. These vendors looked at what their products store, included it, and documented what's inside — exports that could meaningfully support downstream AI applications, patient data portability, and independent analysis.

For the 54% graded D or F, the box is mostly empty. The export describes a clinical summary, sometimes literally the same C-CDA used for transitions of care, relabeled as "all EHI." A patient at one of these systems can request an export and receive roughly the same data they'd get from the Blue Button download on their patient portal. The billing data, the specialty clinical data, the messages, the administrative records -- everything that makes the EHR *the EHR* -- isn't in the box.

The gap between what the regulation requires and what the industry delivers is large, and it's measurable.

## So now what

Based on these findings, a few recommendations:

**ONC could require a patient-facing EHI export API.** Even when vendors pack the box properly, there's no reliable delivery. Most (b)(10) exports require a manual request to the health system, often with weeks of turnaround — the equivalent of asking patients to drive to the warehouse and pick it up themselves. The (g)(10) standardized API already delivers USCDI data through SMART on FHIR. Extending that infrastructure with a full-EHI scope (same authorization, same app ecosystem, broader data) would create a delivery channel. That matters because automated delivery creates accountability: when any patient-authorized app can request a shipment and inspect what arrives, half-empty boxes can't hide.

**ONC could require actual testing.** Today, (b)(10) conformance is attestation-based: vendors attest, ONC-ACBs review the attestation, but nobody runs a test export and checks what comes out. The extreme variability in what vendors publish at their documentation URLs suggests attestation alone isn't producing consistent outcomes.

**ONC already has oversight tools that could drive immediate change.** ONC-ACBs can conduct in-the-field surveillance of certified products and request documentation from developers as part of ongoing certification maintenance. ONC itself can directly review any certified product when there's reason to believe it isn't meeting certification requirements. None of these powers require new rulemaking. Today, the only real feedback loop is a patient requesting their records, waiting weeks, receiving an export, and having the technical sophistication to realize it's a relabeled clinical summary, then figuring out where to complain. That loop is too long, too rare, and too quiet to drive change. If ONC-ACBs started examining what vendors actually publish at their (b)(10) documentation URLs, and comparing it to what the product stores, problems would surface before patients have to discover them firsthand. Vendors whose entire (b)(10) spec is a link to the HL7 C-CDA spec would have to explain themselves. That alone could shift posture across the industry.

**ONC should preserve Real World Testing requirements for (b)(10).** The proposed rollback in HTI-5 would eliminate one of the few mechanisms that provides any visibility into whether EHI exports are functioning in practice.

**Patients and advocates can ask informed questions.** The [dashboard](https://jmandel-bot.github.io/ehi-export-analysis/) is public. If your EHR is graded D and you're requesting your records, you now have specific language for what's missing.

**Developers building on patient access rights should calibrate expectations.** The theoretical right to a complete computable export and the practical implementation diverge sharply. Plan accordingly.

---

The [full results and per-vendor analyses](https://jmandel-bot.github.io/ehi-export-analysis/) are public and will continue to be updated as I complete Phase 2 (107 additional product families with CPOE but no FHIR API) and Phase 3 (remaining certified products). The [methodology, prompts, and source data](https://github.com/jmandel-bot/ehi-export-analysis) are open source.

*Analysis by [Josh Mandel, MD](https://www.linkedin.com/in/joshuamandel/). Assessments are AI-assisted and may contain errors; [please report corrections](https://github.com/jmandel-bot/ehi-export-analysis/issues/new).*
