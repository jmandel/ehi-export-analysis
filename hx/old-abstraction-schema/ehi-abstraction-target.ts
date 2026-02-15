/**
 * EHI Abstraction Target — v2 (simplified, evidence-first)
 *
 * Design principles:
 * 1. EVIDENCE FIRST: inventory what you actually found before making any judgments.
 *    Read the source artifacts in downloads/ deeply — PDFs, CSVs, schemas, data
 *    dictionaries. Use `pdftotext -layout`, write scripts to traverse structured data.
 *    Do not rely on the summary markdown files.
 *
 * 2. CONCRETE OVER GENERIC: cite specific tables, fields, sections, page numbers.
 *    "PatientEntity has 71 fields, 71 with descriptions" beats "field semantics are
 *    documented for a substantial subset."
 *
 * 3. THE CORE QUESTION: does this export plausibly contain all the EHI the product
 *    stores, or is it clearly an abbreviated/projected/filtered subset?
 *
 * 4. SIMPLE JUDGMENTS: a short rationale string beats a 7-field reasoning object
 *    that gets copy-pasted. Every rationale must cite specific artifacts.
 *
 * Workflow:
 * - Stage 1: Read all source artifacts. Build the evidence inventory.
 * - Stage 2: Describe the export model (entities, fields, formats).
 * - Stage 3: Assess domain coverage against what the product stores.
 * - Stage 4: Make overall judgments grounded in stages 1-3.
 *
 * Do NOT score while still reading. Finish the inventory first.
 */

/* ── Scalars ─────────────────────────────────────────────────────────────── */

export type IsoDate = `${number}-${number}-${number}`;

/**
 * 1-5 scale. Every use includes anchors in its JSDoc.
 * Use 0 only when evidence is entirely absent.
 */
export type Score0to5 = 0 | 1 | 2 | 3 | 4 | 5;

/* ── Evidence Inventory ──────────────────────────────────────────────────── */

/**
 * One artifact you actually reviewed.
 *
 * This is the foundation. Every later judgment must trace back to artifacts here.
 */
export interface ReviewedArtifact {
  /** Path relative to results/<slug>/, e.g. "downloads/data-dictionary.pdf" */
  path: string;

  /** What kind of artifact: data_dictionary, schema, sample_data, user_guide, screenshot, api_doc, export_spec, other */
  kind: string;

  /** What format: pdf, html, json, csv, xlsx, xml, xsd, openapi, zip, png, txt, other */
  format: string;

  /**
   * What you found in this artifact. Be specific and concrete.
   *
   * Good: "36 tables documented with column name, type, and max length.
   *        Most columns have no description text. Glossary defines 8 common
   *        fields (Id, PatientID, LastModifiedBy, etc.)."
   *
   * Bad: "Data dictionary with table definitions."
   */
  summary: string;

  /**
   * Size/scope of content: page count for PDFs, entity/table count for
   * dictionaries, field count, file count for ZIPs, etc.
   */
  size: string;
}

/* ── Export Model Description ────────────────────────────────────────────── */

/**
 * One entity/table/resource in the export.
 *
 * You don't need to list every entity — but list enough to characterize
 * the export model. For data dictionaries with many tables, list all of them.
 * For FHIR exports, list the resource types.
 */
export interface ExportEntity {
  /** Table/resource/entity name as it appears in the documentation. */
  name: string;

  /** Number of fields/columns/elements documented for this entity. */
  fieldCount: number;

  /**
   * How many of those fields have meaningful descriptions
   * (not just a name and type, but actual business/clinical meaning).
   */
  fieldsWithDescriptions: number;

  /** Brief note on what this entity represents and any notable observations. */
  note: string;
}

export type ExportFormat =
  | 'csv' | 'tsv' | 'json' | 'ndjson' | 'xml' | 'ccda'
  | 'fhir_r4_json' | 'fhir_r4_ndjson' | 'pdf' | 'cbor'
  | 'sql_dump' | 'parquet' | 'mixed' | 'other' | 'unknown';

/**
 * How the export is obtained.
 */
export type ExportMechanism =
  | 'ui_single_patient'
  | 'ui_bulk'
  | 'api_single_patient'
  | 'api_bulk'
  | 'vendor_assisted'
  | 'other'
  | 'unknown';

/**
 * Description of the export model — what the export actually looks like.
 *
 * Fill this AFTER reading all artifacts. This should be a factual description,
 * not a judgment.
 */
export interface ExportModel {
  /** Format(s) of the export output. */
  formats: ExportFormat[];

  /** How the export is triggered/obtained. */
  mechanism: ExportMechanism;

  /** Whether the customer can run it without vendor involvement. */
  selfService: 'yes' | 'no' | 'unknown';

  /**
   * Total number of distinct entities/tables/resources documented.
   * Null if not determinable.
   */
  totalEntities: number | null;

  /**
   * Total number of fields/columns across all entities.
   * Null if not determinable.
   */
  totalFields: number | null;

  /**
   * Entities in the export. List all if feasible (< 100).
   * For very large exports, list representative entities with notes.
   */
  entities: ExportEntity[];

  /**
   * Does the export look like a native database model (internal tables with
   * internal IDs and relationships) or a projection into an external standard
   * (FHIR resources, C-CDA sections, flattened summaries)?
   *
   * This is the most important structural question. Evidence patterns:
   *
   * Native model signals:
   * - Many domain-specific entities with internal GUID/integer keys
   * - Cross-entity foreign key references
   * - Workflow-level objects (orders, transactions, queue items)
   * - Entities that feel operational, not report-shaped
   *
   * Projection signals:
   * - Output maps to standard resource types (FHIR, C-CDA)
   * - Vendor docs describe "mapping" from internal model to output
   * - Fewer entities than expected for product complexity
   * - Generic payload fields (data, content, value) instead of specific columns
   */
  modelCharacter: 'native_database' | 'standard_projection' | 'hybrid' | 'unclear';

  /**
   * Free-text description of the export model.
   * Describe the structure, packaging, any notable patterns.
   * Cite specific artifacts and sections.
   */
  description: string;
}

/* ── Domain Coverage ─────────────────────────────────────────────────────── */

/**
 * Canonical EHI domains.
 *
 * These correspond to the HIPAA Designated Record Set (45 CFR 164.501):
 * data used to make decisions about individuals.
 *
 * NOT EHI (never flag as gaps):
 * - audit/access logs, system config, provider credentialing
 * - scheduling/appointment logs (administrative, generally not DRS)
 * - quality metrics, peer review, staff scheduling
 * - psychotherapy notes, litigation compilations (statutory carve-outs)
 *
 * Use 'other' with otherLabel for product-specific domains not in this list
 * (e.g. dental charts, optometry measurements, behavioral health screenings).
 */
export type EhiDomain =
  | 'demographics'
  | 'encounters'
  | 'problems_conditions'
  | 'medications'
  | 'allergies'
  | 'immunizations'
  | 'vitals'
  | 'laboratory'
  | 'diagnostic_reports'
  | 'procedures'
  | 'clinical_notes'
  | 'care_plans_goals'
  | 'orders_referrals'
  | 'documents_attachments'
  | 'insurance'
  | 'claims_billing'
  | 'payments'
  | 'consents_directives'
  | 'patient_communications'
  | 'other';

/**
 * Coverage assessment for one domain.
 *
 * The key rule: cite specific entities/tables/fields/sections from the
 * evidence inventory. If you can't cite domain-specific evidence, the
 * domain is not_clearly_present — regardless of global claims like
 * "exports all EHI."
 */
export interface DomainCoverage {
  domain: EhiDomain;

  /** Required when domain === 'other'. */
  otherLabel?: string;

  /**
   * - plausibly_comprehensive: evidence shows this domain broadly represented
   *   with multiple entities/fields covering major workflow slices
   * - present_but_limited: domain data is present but clearly thin or partial
   *   (e.g. only 2 fields for medications, or only a single generic table)
   * - not_clearly_present: no domain-specific evidence found
   *
   * IMPORTANT: a global claim like "all EHI" or "all patient data" does NOT
   * count as domain-specific evidence. You need actual tables/fields/sections.
   */
  coverage: 'plausibly_comprehensive' | 'present_but_limited' | 'not_clearly_present';

  /**
   * What specific entities/tables/fields/sections in the EXPORT DOCUMENTATION
   * support this coverage call?
   *
   * For 'plausibly_comprehensive': cite the entities and fields that cover this domain.
   *   "PatientInfo (71 fields), Patient_Medications (62 fields),
   *    Patient_MedicationAllergy (18 fields). Medication fields include
   *    drug name, dose, route, frequency, start/stop dates, prescriber."
   *
   * For 'present_but_limited': cite what IS present and explain why it's thin.
   *   "C-CDA export includes a Medications section per R2.1 standard, but no
   *    medication-specific table or field list in vendor docs. Only summary
   *    medication list, not prescribing history or e-Rx transactions."
   *
   * For 'not_clearly_present': state what you looked for and didn't find.
   *   "No billing tables, fields, or sections in data dictionary (36 tables
   *    reviewed). No claims or charge data in sample export. Export PDF makes
   *    no mention of billing or financial data."
   */
  exportEvidence: string;

  /**
   * The other side of the completeness question: what does the PRODUCT store
   * in this domain, and how does that compare to what the export covers?
   *
   * This is where you surface the inference. Connect product capabilities
   * (from product research, marketing, CHPL criteria) to export gaps.
   *
   * Good: "Product includes integrated billing with claims submission and
   *        payment posting (product-research.md). CHPL criteria include
   *        170.315(f)(1) transmission to public health. But export contains
   *        zero billing entities — this is a significant DRS gap for a product
   *        that stores patient-specific financial records."
   *
   * Good: "Product is ambulatory EHR only, no billing module.
   *        This domain is not applicable."
   *
   * For 'plausibly_comprehensive' domains, briefly confirm the product
   * stores this data and the export appears to cover it adequately.
   */
  gapAnalysis: string;
}

/* ── Documentation Quality ───────────────────────────────────────────────── */

/**
 * How well-documented is the export? Based on what you actually found
 * in the artifacts, not what you wish existed.
 */
export interface DocumentationQuality {
  /**
   * Are field names listed?
   * Cite: "All 36 tables list column names" or "Only 3 of 20 tables have field lists."
   */
  fieldNamesDocumented: { answer: 'yes' | 'partial' | 'no'; detail: string };

  /**
   * Are field data types documented?
   * Cite: "Every column has ColumnType and MaxLength" or "Types are not specified."
   */
  fieldTypesDocumented: { answer: 'yes' | 'partial' | 'no'; detail: string };

  /**
   * Are field meanings/semantics explained (beyond just the column name)?
   * Be precise about coverage. "164/715 fields (23%) have descriptions,
   * concentrated in 4 of 31 entities" is much more useful than "yes."
   */
  fieldSemanticsDocumented: { answer: 'yes' | 'partial' | 'no'; detail: string };

  /**
   * Are relationships between entities documented (FK references, ERDs,
   * explicit join instructions)?
   * "yes" requires explicit relationship documentation, not just similar
   * field names across tables.
   */
  relationshipsDocumented: { answer: 'yes' | 'partial' | 'no'; detail: string };

  /**
   * Are value sets / allowed values / code systems documented?
   * "yes" requires explicit enumerations, not just "status field."
   */
  valueSetsDocumented: { answer: 'yes' | 'partial' | 'no'; detail: string };

  /** Does sample export data exist (actual payloads, not just schema docs)? */
  sampleDataExists: { answer: 'yes' | 'no'; detail: string };

  /**
   * Could a developer build an import of this data using only the
   * provided documentation?
   *
   * 0: no useful documentation
   * 1: field names only, would require extensive reverse engineering
   * 2: names + types, but semantics and relationships unclear
   * 3: reasonable documentation, some guesswork needed
   * 4: good documentation, minor ambiguities
   * 5: thorough documentation, could confidently import
   */
  importReadiness: Score0to5;

  /** Rationale for importReadiness score, citing specific strengths/gaps. */
  importReadinessRationale: string;
}

/* ── Overall Assessment ──────────────────────────────────────────────────── */

/**
 * High-level posture of this export.
 *
 * - comprehensive_native: Export appears to be a broad native model dump covering
 *   most/all product data. Strong docs. Few gaps.
 *
 * - partial_native: Native model dump but with clear coverage gaps or thin
 *   documentation in important areas.
 *
 * - standard_projection: Export is primarily a projection into FHIR/C-CDA/etc.
 *   May cover clinical data well but likely misses vendor-specific data that
 *   doesn't map to the standard.
 *
 * - minimal_or_unclear: Very thin documentation, or export covers only a small
 *   slice of what the product stores, or evidence is too weak to assess.
 */
export type ExportPosture =
  | 'comprehensive_native'
  | 'partial_native'
  | 'standard_projection'
  | 'minimal_or_unclear';

export interface OverallAssessment {
  posture: ExportPosture;

  /**
   * Does this export plausibly cover everything the product stores?
   *
   * 0: cannot assess
   * 1: clearly covers only a small fraction
   * 2: significant gaps relative to product capabilities
   * 3: moderate coverage with notable gaps
   * 4: broad coverage with minor gaps
   * 5: appears to cover essentially everything
   */
  completeness: Score0to5;

  /**
   * Rationale for completeness score. Must reference:
   * - what the product is known to store (from product research)
   * - what the export covers (from your evidence inventory)
   * - specific gaps between the two
   */
  completenessRationale: string;

  /**
   * Rationale for posture choice. Explain why this posture fits better
   * than adjacent alternatives.
   */
  postureRationale: string;

  /** Single most important positive finding, with artifact citation. */
  strongestSignal: string;

  /** Single most important gap or risk, with artifact citation. */
  biggestConcern: string;

  /**
   * Narrative summary. Several paragraphs. Be specific and honest.
   * What would someone evaluating this vendor's EHI compliance need to know?
   * What would someone planning a data migration need to know?
   */
  narrative: string;
}

/* ── Access ───────────────────────────────────────────────────────────────── */

export interface AccessInfo {
  /** Is the export documentation publicly accessible without login? */
  docsPublic: boolean;

  /** Is vendor involvement required to run the export? */
  vendorInvolvementRequired: 'yes' | 'no' | 'unknown';

  /** Any fees mentioned for the standard export? */
  feesApply: 'yes' | 'no' | 'unknown';

  /** Notes on access barriers, login walls, broken links, etc. */
  notes: string;
}

/* ── Root ─────────────────────────────────────────────────────────────────── */

export interface EhiAbstractionRecord {
  meta: {
    schemaVersion: '2.0.0';
    assessedAt: IsoDate;
    assessor: string;
  };

  /** Vendor name. */
  vendorName: string;

  /** Product family name. */
  productName: string;

  /** CHPL IDs covered by this abstraction. */
  chplIds: number[];

  /**
   * What does this product do? What clinical and billing workflows does it
   * support? What patient populations and care settings does it serve?
   *
   * This is the BASELINE for assessing export completeness. You cannot judge
   * whether an export is complete without first understanding what the product
   * stores. Draw on product research, vendor marketing, CHPL certification
   * criteria, and any other context.
   *
   * Be specific about capabilities that imply stored data domains:
   *
   * Good: "Acme EHR is an integrated EHR + practice management system for
   *        ambulatory practices across 20+ specialties. Capabilities include
   *        e-prescribing, lab/imaging ordering, patient portal, claims submission,
   *        payment posting, and appointment scheduling. CHPL criteria include
   *        (b)(1) transitions of care, (e)(1) patient access, (f)(1) immunization
   *        registry reporting. This implies stored data in: clinical records,
   *        prescriptions, lab/imaging orders and results, portal messages,
   *        billing/claims, payments, and immunization records."
   *
   * Bad: "Acme EHR is an EHR system."
   */
  productContext: string;

  /**
   * Every artifact you reviewed. This is the evidence base.
   * Later sections must reference artifacts listed here.
   */
  artifacts: ReviewedArtifact[];

  /** Factual description of the export model. */
  exportModel: ExportModel;

  /**
   * Domain-by-domain coverage assessment.
   * Include one row for every domain where the product plausibly stores data.
   * Omit domains that don't apply to this product (e.g. no claims_billing
   * for a product that doesn't do billing).
   */
  domainCoverage: DomainCoverage[];

  /** Documentation quality assessment. */
  documentationQuality: DocumentationQuality;

  /** Access constraints. */
  access: AccessInfo;

  /** Overall assessment. */
  overall: OverallAssessment;

  /**
   * Short, concrete, evidence-backed facts that are high-signal.
   * Examples:
   * - "85 tables with 1,165 fields, all with descriptions"
   * - "Export is CBOR format (unusual); no sample data provided"
   * - "Data dictionary covers only 4 of 31 entities with semantic descriptions"
   */
  notableFacts: string[];
}
