# The State of EHI Export: What 217 Certified EHRs Actually Export

*Working outline — follow-up to "Your C-CDA Is Exquisitely Unlikely" and "Five Ways"*

---

## Why this matters now

The hook: AI is changing what's possible with patient data. Clinical summaries
(C-CDA, FHIR US Core) are designed for a specific job — provider-to-provider
handoffs, population health queries, quality measures. They're lossy by design:
they capture the clinical highlights, not the full record.

But the use cases that are emerging now — and will accelerate — need more:

- An AI agent helping a patient navigate a complex cancer diagnosis needs the
  oncology staging data, the chemo regimen details, the radiation treatment
  plans — not just "Condition: malignant neoplasm of breast" in a problem list.
- A patient switching from one behavioral health provider to another needs
  their psychosocial assessments, PHQ-9 score trajectories, treatment plan
  history — not a C-CDA that can't even represent most of those concepts.
- An AI helping a patient understand and contest a medical bill needs the actual
  charge detail, the claim submission history, the EOBs — not a clinical summary
  that doesn't mention money.
- A personal health AI that monitors trends over time needs the granular
  medication administration records, the vitals flowsheets, the custom
  questionnaire responses — not a reconciled med list snapshot.

These all build on the same legal foundation: the patient's right under HIPAA
to access their Designated Record Set, which §170.315(b)(10) requires certified
EHRs to export in a computable format. The regulation was written before
the current AI moment, but it's exactly the pipe that needs to work.

So: does it?

## What we did

Brief methodology section. Keep it tight — point to the dashboard and repo
for details.

- Started from ONC's Certified Health IT Product List (CHPL). Every certified
  product that attests to (b)(10) registers a URL where their export format
  documentation lives.
- Focused on Phase 1: products certified for CPOE (computerized provider order
  entry) and the FHIR API [(g)(10)] — the products that function as real EHRs
  with order entry and standards-based API access. This filters out patient
  portals, lab-only systems, and minimal-certification modules.
- That gives us ~216 product families covering ~265 CHPL-certified products.
  (Products sharing an EHI documentation URL and developer were grouped into
  families — MEDITECH Expanse 2.1 and 2.2 are one family; MEDITECH Expanse
  and MEDITECH Client/Server are different families because they have different
  export configurations.)
- For each family: AI-assisted research on the vendor and product, then
  automated retrieval and examination of whatever documentation they published
  at their registered URL. Every PDF downloaded, every HTML page scraped,
  every data dictionary parsed.
- Then a deep analysis: what does the export actually contain? How does it
  compare to what the product stores? Is this a genuine EHI export or a
  relabeled clinical summary?

Link to dashboard, methodology page, and open source repo.

## 217 products, graded

217 product families analyzed so far. The grades:

| Grade | Count | What it means |
|-------|-------|---------------|
| A / A- | 28 (13%) | Purpose-built, comprehensive, documented |
| B+ / B / B- | 35 (16%) | Real effort, notable gaps |
| C+ / C / C- | 36 (17%) | Partial — some substance, significant holes |
| D+ / D / D- | 104 (48%) | Minimal or stub |
| F | 14 (6%) | Nothing meaningful |

**Over half** of the EHR products we analyzed — products certified by ONC,
attesting to a federal requirement, serving real patients — have (b)(10)
export documentation that is either too thin to evaluate or clearly describes
an export limited to what you'd get from a standard clinical summary.

[Consider a histogram visualization here — the bimodal distribution is
visually striking.]

## Billing as litmus test

Of all the signals in the data, one stands out: **does the export include
billing data?**

Almost every EHR in Phase 1 handles billing and revenue cycle management —
charge capture, claim submission, payment posting, insurance eligibility,
denials management. This is core operational data that is squarely part of
the Designated Record Set (it's used to make decisions about patient care
and coverage). And it has no representation in C-CDA or USCDI — there's no
C-CDA template for a superbill, no US Core profile for a claim denial.

So billing data is a natural litmus test: if a vendor included it, they had
to build something beyond their existing clinical exchange. If they didn't,
they probably just relabeled what they already had.

The numbers bear this out. Among products graded A or A-: 93% include billing.
Among products graded B or above: over 90%. Among products graded D or F:
**7%**.

[Not making a causal claim here — the grading rubric rewards comprehensiveness,
and billing is one signal of comprehensiveness. But it's the most *observable*
signal. You don't need to parse a data dictionary to check whether billing
tables exist in the export.]

### When vendors actually export billing

Vendors who take billing seriously export *a lot* of billing data. It's often
the single largest domain in the entire export:

- **Epic**: 1,286 billing/revenue cycle tables with 12,367 columns — this single
  billing category exceeds most vendors' *entire* exports.
- **Altera Sunrise**: 917 billing tables — 33% of all tables in the export.
- **Greenway Prime Suite**: 192 billing tables. Their `CFBClaimInfo` table has
  435 fields — the single largest entity in the entire export.
- **eClinicalWorks**: 161 billing tables, including state-specific Medicaid
  claim forms (NY Workers' Comp C-4.3: 218 fields) and the UB-04 institutional
  claim at 127 fields.
- **Juno Health**: The three largest tables in the entire export are all billing:
  `RCMUB04CLAIM` (260 fields mapping every box on the UB-04 form),
  `RCM1500CLAIM` (116 fields), `BILLINGITEM` (115 fields).

Smaller vendors get this right too. MDVita (24 entities total) is a
claims-adjudication company turned EHR vendor — their `Claims` entity has
85 fields with granular EOB data. Flatiron's oncology EHR has a 208-field
insurance entity. athenahealth invented 9 custom FHIR resource types
specifically for billing — 506 fields including charges, collections,
eligibility, and payment plans — proving you can do this in FHIR if you
actually do the mapping work.

A striking pattern: **the single largest entity in many vendor exports is a
billing entity, not a clinical one.** This makes sense — claim forms are
complex structured documents — but it also explains why vendors who don't
export billing are missing such a large fraction of their data footprint.

### And when they don't

- **MaxRemind (Maximus)**: A billing company's EHR whose export ironically
  omits all billing data. (Grade: D)
- **ClaimPower**: Core business is billing — company name says it. Export:
  C-CDA clinical summary, zero billing/claims/payment data, 502 words of
  screenshot walkthroughs. (Grade: D-)
- **Radysans EHR**: Full eBilling module with 2,500+ payer connections;
  export is a one-page doc listing C-CDA sections. (Grade: D)
- **Vohra Wound Physicians**: Company name literally includes "Coding" —
  billing data entirely absent from export. (Grade: D-)

## Specialty EHRs that don't export their specialty

Specialty EHRs are where this gets hard to look at. Products whose entire
value proposition is domain-specific clinical data.

**EndoVault** (endoscopy/GI EHR): Stores HD images, 4K video, bowel prep
scores, polyp characteristics, scope tracking via RFID. The export contains
zero endoscopy data. The 138-page “EHI” documentation is the (g)(10) FHIR
API spec relabeled — 18 standard FHIR resources identical to any generic EHR.

**OMS EHR** (cardiology): Claims “6,000+ data points per patient” across 16
cardiovascular modules (echo, EKG, cath lab, stress testing). The entire EHI
documentation: a 9-row, 2-column table on a single page. Zero fields defined.

**EyeMD** (ophthalmology): 2024 Best in KLAS winner. Integrates Zeiss,
Heidelberg, Topcon devices. Export: 25 standard FHIR resources, zero
ophthalmology data. Their mandatory disclosures describe (b)(10) as “Ability
to send CCDA information to other systems via secure transmission” — they
literally conflate EHI export with transitions of care.

**TheraOffice** (PT/OT/SLP, Netsmart): 900+ rehab practices. 16 of 19 export
tables are literally named `PAT_PROFILE_USCDI_*` — the clearest possible
confession that this is USCDI relabeled as EHI. Zero therapy notes, zero
evaluations, zero outcome measures (no LEFS, DASH, NDI, Oswestry).

**ARIA CORE** (radiation oncology, Varian/Siemens): The dominant US radiation
oncology system. Registered EHI documentation URL returns 404 — and has never
been captured by the Wayback Machine.

**InPracSys** (urology): “Built by urologists, for urologists.” Export:
15 standard FHIR resources, 328 fields. Zero urology data.

### Same specialty, opposite outcomes

Both ModMed’s gGastro and EndoSoft’s EndoVault are GI/endoscopy EHRs.
gGastro exports **441 tables with 4,453 fields** — including a `Finding` table
with **155 fields per endoscopic finding** (polyp size, morphology, location,
removal method), 115 billing tables, and 1,166 value sets. EndoVault
exports zero endoscopy data.

Both ModMed’s EMA and EyeMD are ophthalmology EHRs. EMA exports **25
ophthalmology pretesting tables with 1,209 fields** — visual acuity (93),
refraction (82), keratometry, IOP, pachymetry. EyeMD exports zero
ophthalmic data.

nAbleMD (fertility/IVF) exports 31 IVF-specific entities with 1,317 fields —
including `emrcycle` at 231 fields. Flatiron exports chemo dose calculations,
AJCC staging, treatment pathways, lifetime cumulative doses.

These vendors prove it’s possible. The specialty data exists in these systems.
The vendors who export it built something; the ones who don’t simply didn’t.

## Behavioral health

Behavioral health deserves special attention. These products handle some of
the most sensitive clinical data — psychosocial assessments, suicide risk
screenings, substance use treatment records, psychiatric treatment plans.
Most of this data has no C-CDA representation. And behavioral health
records have additional privacy protections under 42 CFR Part 2 that make
portability even more important (patients need to be able to verify what
their providers have on file).

Out of ~20 behavioral health EHRs in our Phase 1 analysis:

- A handful did it well (Qualifacts CareLogic: A-, Qualifacts Credible: A-,
  HCS EMR: A-)
- The rest ship generic C-CDA clinical summaries with zero behavioral health
  content (CarePaths: D, Core Solutions: D, Ehana: D, Streamline SmartCare: D,
  Procentive: F)

[Pull a specific example — maybe Procentive or Streamline — to illustrate
what "zero behavioral health content" actually means in practice.]

## Your portal messages aren't in your record

123 of 217 products (57%) have patient portal or messaging features but
exclude patient communications from their EHI export. Only 37 (17%)
include them.

This is data that patients generated — messages they sent to their doctors,
responses they received, portal interactions. It's unambiguously part of the
Designated Record Set. And for most products, it's simply missing.

[1-2 examples of products with robust portals that exclude portal data
from export.]

## What serious looks like

Brief section on the A-tier — not to be exhaustive but to establish
that this is achievable:

- **Oracle Health (Millennium)**: 6,604 tables, 129K+ columns, 99.9%
  description coverage, three export pathways. The gold standard.
- **Epic**: 7,672 tables, 63,121 columns, 100% descriptions. Native
  Clarity schema as TSV.
- **eClinicalWorks**: 1,466 tables, 21K+ fields. Billing gets 161 tables.
- **Greenway (Prime Suite)**: 1,026 tables, 11,868 fields.
- **athenahealth**: Purpose-built FHIR export with 9 custom financial
  resource types — proving you can do this in FHIR if you actually do
  the mapping work.

The point isn't that everyone needs 7,000 tables. The point is that
vendors who took this seriously built something real — whether it's a
native database dump or a deep standards-based mapping — and it shows.

## Back to the pipe

Return to the opening frame. The (b)(10) requirement is the regulatory
foundation for a patient's ability to get their full record in computable
form. As AI capabilities grow, the value of that full record grows with it.

But for over half of certified EHRs, the pipe is broken. The documentation
either describes a clinical summary relabeled as "all EHI" or is too thin
to assess. Patients at these systems can request an export and receive...
a C-CDA that covers the same data they could already get through their
patient portal's "download my record" button.

The gap between what the regulation requires and what the industry delivers
is stark. And it's measurable.

## So now what

[Keep this section measured — you're not a regulator, you're presenting data.]

- ONC could require actual testing of (b)(10) exports (currently attestation-only).
- ONC-ACBs could examine the published documentation as part of surveillance.
- Patients and patient advocates can use this data to ask informed questions.
- Downstream developers building on patient access rights should be aware
  that the theoretical right and the practical implementation diverge sharply.

## Closing

Link to dashboard, methodology, open source. Invite corrections.
Note that Phase 2 (CPOE without FHIR — 107 families) and Phase 3 are
in progress.

---

## Notes for drafting

- Direct, evidence-first, specific. No hedging where data is clear.
- Named vendors with CHPL links.
- Zagat summaries for color.
- AI framing as motivation, not hype.
- Don't overclaim billing correlation (rubric is partly tautological).
- Specialty gap is the hardest finding to explain away.
