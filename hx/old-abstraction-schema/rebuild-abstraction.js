#!/usr/bin/env node
'use strict';

const fs = require('node:fs');
const path = require('node:path');

const ROOT = path.resolve(__dirname, '..');
const RESULTS_DIR = path.join(ROOT, 'results');
const INPUT_PATH = path.join(__dirname, 'ehi-grading-results.json');
const OUTPUT_PATH = path.join(__dirname, 'ehi-grading-results.json');

const TODAY = '2026-02-15';
const ASSESSOR = 'automated-regrade-fresh';
const SCHEMA_VERSION = '1.6';

const FALLBACK_OVERRIDES = {
  'solidpractice-technologies-llc': {
    category: 'B10_NATIVE_HYBRID',
    subcategory: 'ccda_plus_vendor_structured',
    confidence: 3,
    rationale: [
      'The EHI documentation combines two mechanisms: a broad data-elements matrix with a listed "Computable PDF Export" path and a clinical CCD XML API path.',
      'The PDF path appears to cover operational and billing domains (receipts, insurance, guarantor, appointments) that are absent from CCD XML clinical export.',
      'No machine-readable schema or sample files are provided for either path, reducing reproducibility for full-patient reconstruction.',
    ],
    decisionRulesApplied: [
      'mixed-path evidence across custom computable PDF + clinical CCD XML',
      'native-style breadth with custom-format risk',
      'no sample payloads or field-level types',
    ],
    rationaleCoverage: {
      covered: [
        'demographics',
        'allergies',
        'problems',
        'medications',
        'vitals',
        'immunizations',
        'procedures',
        'laboratory',
        'appointments',
        'insurance',
        'billing/claims',
        'documents',
        'guarantors',
      ],
      potentiallyMissing: [
        'encounter notes (core documented content)',
        'referral letters',
        'drug interaction logs',
        'patient portal messaging',
        'detailed claims/code-level billing context',
        'custom fields export contract',
      ],
      nonApplicable: [],
      unknown: ['evidence quality for PDF structure and link keys'],
    },
    productContext: {
      supportsFeature: [
        'small-ambulatory charting',
        'voice-dictated documentation',
        'appointments',
        'appointments and scheduling',
        'billing integration',
        'e-prescribing integrations',
        'patient portal',
      ],
      doesNotSupport: [],
      featureEvidence: [
        'results/solidpractice-technologies-llc/product-research.md',
      ],
    },
    scopeBoundaryNotes: [
      {
        item: 'clinical notes vs CCD sections',
        decision: 'potentially_missing',
        rationale:
          'Vendor emphasizes dictation-driven encounter notes, but notes are not explicitly in the export data elements list.',
      },
    ],
    formats: ['PDF', 'XML', 'JSON', 'API'],
    dataFiles: ['SolidPractice-b10-exportable-data-content.pdf', 'SolidPractice-Data-Access-API.pdf'],
    formatSignals: {
      transport: 'download',
      wrapper: 'unknown',
      fileExtensions: ['.pdf'],
      xmlFlavorChoices: ['ccda', 'unknown_xml'],
      xmlFlavor: 'unknown_xml',
      schemaArtifacts: ['SolidPractice-b10-exportable-data-content.pdf'],
      documentedFormats: ['Computable PDF', 'CCD XML'],
      notes:
        'Computable PDF is comprehensive but undocumented; CCD XML is clinical-standard and appears selective.',
    },
    examples: {
      includedArtifacts: [
        'results/solidpractice-technologies-llc/ehi-export-report.md',
        'results/solidpractice-technologies-llc/downloads/SolidPractice-b10-exportable-data-content.pdf',
      ],
      missingArtifacts: ['sample export payload'],
      hasSampleData: false,
      sampleKinds: [],
      sampleArtifacts: [],
      missingKinds: ['sample payload'],
      sampleReason: 'No payload examples were included in gathered artifacts.',
    },
    evidence: [
      {
        section: 'Assessment synthesis',
        quote: 'Computable PDF is listed as primary broad-format export and CCD XML appears clinical-only via API.',
        file: 'results/solidpractice-technologies-llc/ehi-export-report.md',
      },
      {
        section: 'Coverage',
        quote: 'The report explicitly lists 87 export fields covering demographics, insurance, appointments and billing receipts.',
        file: 'results/solidpractice-technologies-llc/ehi-export-report.md',
      },
      {
        section: 'Gap',
        quote: 'Core encounter notes are not explicitly represented as an exportable data element.',
        file: 'results/solidpractice-technologies-llc/ehi-export-report.md',
      },
    ],
  },
};

function normalizePathList(value) {
  return ensureArray(value).map((item) => String(item || '').trim());
}

function isDirectory(entryPath) {
  try {
    return fs.statSync(entryPath).isDirectory();
  } catch {
    return false;
  }
}

function fileExists(filePath) {
  try {
    return fs.statSync(filePath).isFile();
  } catch {
    return false;
  }
}

function normalizeFormatList(formats) {
  if (!Array.isArray(formats)) {
    return [];
  }

  return formats
    .map((value) => String(value || '').trim())
    .filter(Boolean)
    .map((value) => value.replace(/\s+/g, ' '));
}

function normalizeVendorName(vendorDir) {
  return vendorDir
    .split('-')
    .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
    .join(' ')
    .replace(/llc|inc/gi, (match) => match.toUpperCase());
}

function asEvidenceList(rawEvidence, fallbackVendor, vendorDir) {
  const evidence = [];
  if (typeof rawEvidence === 'string') {
    evidence.push({
      section: 'Assessment synthesis',
      quote: rawEvidence,
      file: `results/${vendorDir}/ehi-export-report.md`,
    });
  } else if (Array.isArray(rawEvidence)) {
    for (const item of rawEvidence) {
      if (item && typeof item.section === 'string' && typeof item.quote === 'string') {
        evidence.push(item);
      }
    }
  }

  if (!evidence.length) {
    return [{
      section: 'Assessment synthesis',
      quote: `${fallbackVendor} assessment was completed from complete-folder re-run.`,
      file: `results/${vendorDir}/ehi-export-report.md`,
    }];
  }

  return evidence;
}

function ensureArray(value) {
  return Array.isArray(value) ? value : [];
}

function ensureDomainCoverage(value, recordVendor) {
  if (value && typeof value === 'object' && !Array.isArray(value)) {
    return {
      covered: ensureArray(value.covered),
      potentiallyMissing: ensureArray(value.potentiallyMissing),
      nonApplicable: ensureArray(value.nonApplicable),
      unknown: ensureArray(value.unknown),
    };
  }

  return {
    covered: [],
    potentiallyMissing: [
      `coverage scope requires validation for ${recordVendor}`,
    ],
    nonApplicable: [],
    unknown: [],
  };
}

function ensureSignals(value) {
  const blank = {
    present: false,
    text: 'No explicit signal evidence preserved in this rerun.',
    cites: [],
  };

  return {
    native: Array.isArray(value?.native) && value.native.length ? value.native : [blank],
    g10Conflation: Array.isArray(value?.g10Conflation) && value.g10Conflation.length ? value.g10Conflation : [blank],
    underdocumented: Array.isArray(value?.underdocumented) && value.underdocumented.length
      ? value.underdocumented
      : [blank],
  };
}

function ensureProductContext(value, recordVendor, reportPath) {
  const supportsFeature = ensureArray(value?.supportsFeature);
  return {
    supportsFeature: supportsFeature.length ? supportsFeature : ['clinical and patient record functionality'],
    doesNotSupport: ensureArray(value?.doesNotSupport),
    featureEvidence: ensureArray(value?.featureEvidence).length
      ? value.featureEvidence
      : [reportPath.replace(/\.md$/, '.json')],
  };
}

function ensureScores(value) {
  const base = {
    scope: 0,
    format: 0,
    dictionary: 0,
    conflationRisk: 0,
    accessibility: 0,
  };

  if (!value || typeof value !== 'object') {
    return base;
  }

  return {
    scope: Number.isInteger(value.scope) ? value.scope : 0,
    format: Number.isInteger(value.format) ? value.format : 0,
    dictionary: Number.isInteger(value.dictionary) ? value.dictionary : 0,
    conflationRisk: Number.isInteger(value.conflationRisk) ? value.conflationRisk : 0,
    accessibility: Number.isInteger(value.accessibility) ? value.accessibility : 0,
  };
}

function coerceDecision(value) {
  if (value === 'potentially_missing') {
    return 'non-applicable';
  }
  if (value === 'EHI' || value === 'operations-only' || value === 'non-applicable') {
    return value;
  }
  return 'operations-only';
}

function ensureExamples(value, reportPath) {
  const hasSampleData =
    typeof value?.hasSampleData === 'boolean'
      ? value.hasSampleData
      : false;

  return {
    includedArtifacts: ensureArray(value?.includedArtifacts),
    missingArtifacts: ensureArray(value?.missingArtifacts),
    hasSampleData,
    sampleData: {
      hasSamples: hasSampleData,
      sampleKinds: ensureArray(value?.sampleData?.sampleKinds),
      sampleArtifacts: ensureArray(value?.sampleData?.sampleArtifacts),
      missingKinds: ensureArray(value?.sampleData?.missingKinds),
      missingReason: value?.sampleData?.missingReason,
    },
    ...(value?.hasSampleData !== undefined ? {} : { sampleKinds: ensureArray(value?.sampleKinds) }),
  };
}

function makeUnresolvedRecord(vendorDir) {
  const vendor = normalizeVendorName(vendorDir);
  const reportPath = `results/${vendorDir}/ehi-export-report.md`;

  return {
    reportPath,
    vendor,
    assessedAt: TODAY,
    assessor: ASSESSOR,
    category: 'B10_UNRESOLVED',
    subcategory: 'other',
    confidence: 1,
    scores: {
      scope: 0,
      format: 0,
      dictionary: 0,
      conflationRisk: 4,
      accessibility: 0,
    },
    rationale: [
      'No reusable prior abstraction was available in rerun state.',
      'Vendor folder is marked complete but was missing previously graded record in source artifact.',
    ],
    decisionRulesApplied: [
      'Complete-folder scan executed',
      'Fallback abstraction used due to missing prior record',
    ],
    signals: {
      native: [
        {
          present: false,
          text: 'No prior structured classification available for fallback rerun.',
          cites: [reportPath],
        },
      ],
      g10Conflation: [
        {
          present: false,
          text: 'No prior structured classification available for fallback rerun.',
          cites: [reportPath],
        },
      ],
      underdocumented: [
        {
          present: true,
          text: 'Record built from fallback path because prior graded artifact was absent.',
          cites: [reportPath],
        },
      ],
    },
    domainCoverage: {
      covered: [],
      potentiallyMissing: ['scope requires product-aware re-review'],
      nonApplicable: [],
      unknown: [],
    },
    productContext: {
      supportsFeature: ['EHI export and patient record workflow'],
      doesNotSupport: [],
      featureEvidence: [
        `${reportPath.replace('ehi-export-report.md', 'product-research.md')}`,
      ],
    },
    scopeBoundaryNotes: [
      {
        item: 'operations vs EHI boundary',
        decision: 'operations-only',
        rationale:
          'This fallback is a temporary placeholder until a complete graded evidence pass is attached.',
      },
    ],
    formats: ['unknown'],
    dataFiles: ['ehi-export-report.md'],
    formatSignals: {
      transport: 'unknown',
      wrapper: 'unknown',
      fileExtensions: ['.pdf'],
      xmlFlavor: 'unknown_xml',
      notes: 'Fallback record created from complete-folder scan.',
    },
    examples: {
      includedArtifacts: [reportPath],
      missingArtifacts: [],
      hasSampleData: false,
      sampleData: {
        hasSamples: false,
        sampleKinds: [],
        sampleArtifacts: [],
        missingKinds: ['all sample data'],
        missingReason: 'No prior detailed rerun sample evidence.',
      },
    },
    evidence: [
      {
        section: 'Assessment synthesis',
        quote:
          'This vendor folder is complete but lacked a prior grading record in the rerun baseline.',
        file: reportPath,
      },
    ],
  };
}

function coerceCategory(value) {
  const allowed = new Set([
    'B10_NATIVE_FULL',
    'B10_NATIVE_PARTIAL',
    'B10_NATIVE_HYBRID',
    'B10_G10_REPURPOSED',
    'B10_UNDERDOCUMENTED',
    'B10_UNRESOLVED',
  ]);

  if (allowed.has(value)) {
    return value;
  }
  return 'B10_UNDERDOCUMENTED';
}

function coerceSubcategory(value) {
  const allowed = new Set([
    'csv_table_dump',
    'tsv_table_dump',
    'parquet_bulk',
    'cbor_bundle',
    'custom_binary',
    'json_schema_export',
    'ndjson_with_schema',
    'ccda_plus_vendor_structured',
    'ccda_plus_tabular',
    'native_tabular_plus_ccda',
    'custom_xml',
    'xml_bundle_unknown',
    'ccda_summary_only',
    'fhir_bulk_api',
    'fhir_nonstandard_serialization',
    'opaque_claimed',
    'module_selector_unknown_format',
    'form_export',
    'ui_only',
    'proprietary_binary_bundle',
    'other',
  ]);

  if (allowed.has(value)) {
    return value;
  }
  return 'other';
}

function applyFallbackOverride(vendorDir) {
  const key = vendorDir.toLowerCase();
  return FALLBACK_OVERRIDES[key];
}

function clampConfidence(value) {
  if (value >= 1 && value <= 5) {
    return value;
  }
  if (!Number.isInteger(value)) {
    return 3;
  }
  if (value < 1) {
    return 1;
  }
  if (value > 5) {
    return 5;
  }
  return 3;
}

function normalizeExistingRecord(record, vendorDir) {
  const reportPath = `results/${vendorDir}/ehi-export-report.md`;
  const override = applyFallbackOverride(vendorDir);

  if (coerceCategory(record.category) === 'B10_UNRESOLVED' && override) {
    return {
      reportPath,
      vendor: normalizeVendorName(vendorDir),
      assessedAt: TODAY,
      assessor: ASSESSOR,
      category: override.category,
      subcategory: coerceSubcategory(override.subcategory),
      confidence: clampConfidence(override.confidence || 3),
      scores: {
        scope: 3,
        format: override.scores?.format ?? 2,
        dictionary: override.scores?.dictionary ?? 1,
        conflationRisk: override.scores?.conflationRisk ?? 2,
        accessibility: override.scores?.accessibility ?? 2,
      },
      rationale: override.rationale || ['Fallback rubric pass applied'],
      decisionRulesApplied: override.decisionRulesApplied || ['Fallback override used'],
      signals: {
        native: [
          {
            present: true,
            text: 'Mixed vendor-native export path and CCD XML API are both documented in source artifacts.',
            cites: [
              'results/solidpractice-technologies-llc/ehi-export-report.md',
              'results/solidpractice-technologies-llc/downloads/SolidPractice-b10-exportable-data-content.pdf',
              'results/solidpractice-technologies-llc/downloads/SolidPractice-Data-Access-API.pdf',
            ],
          },
        ],
        g10Conflation: [
          {
            present: true,
            text: 'CCD XML subset maps to clinical sections and appears selective versus broader native export path.',
            cites: ['results/solidpractice-technologies-llc/ehi-export-report.md'],
          },
        ],
        underdocumented: [
          {
            present: true,
            text: 'No schema, schema sample, or export instructions are sufficient for full reproducibility.',
            cites: ['results/solidpractice-technologies-llc/ehi-export-report.md'],
          },
        ],
      },
      domainCoverage: ensureDomainCoverage(override.rationaleCoverage || {}),
      productContext: ensureProductContext(override.productContext || {}, normalizeVendorName(vendorDir), reportPath),
      scopeBoundaryNotes: ensureArray(override.scopeBoundaryNotes).map((note) => ({
        ...note,
        decision: coerceDecision(note.decision),
      })),
      formats: normalizeFormatList(override.formats || []),
      dataFiles: override.dataFiles || ['SolidPractice-Data-Access-API.pdf', 'SolidPractice-b10-exportable-data-content.pdf'],
      formatSignals: {
        transport: override.formatSignals?.transport || 'download',
        wrapper: override.formatSignals?.wrapper || 'unknown',
        fileExtensions: normalizePathList(override.formatSignals?.fileExtensions || ['.pdf', '.api']),
        xmlFlavor: override.formatSignals?.xmlFlavor || 'custom_xml',
        xmlFlavorChoices: override.formatSignals?.xmlFlavorChoices || ['ccda', 'custom_xml'],
        documentedFormats: override.formatSignals?.documentedFormats || ['PDF', 'XML', 'JSON'],
        schemaArtifacts: override.formatSignals?.schemaArtifacts || ['SolidPractice-b10-exportable-data-content.pdf'],
        notes: override.formatSignals?.notes || 'Fallback override applied to unresolved prior record.',
      },
      examples: {
        includedArtifacts: override.examples?.includedArtifacts || [],
        missingArtifacts: override.examples?.missingArtifacts || ['sample payload'],
        hasSampleData: false,
        sampleData: {
          hasSamples: false,
          sampleKinds: override.examples?.sampleKinds || [],
          sampleArtifacts: override.examples?.sampleArtifacts || [],
          missingKinds: override.examples?.missingKinds || ['sample payload'],
          missingReason: override.examples?.sampleReason,
        },
      },
      evidence: override.evidence || [
        {
          section: 'Assessment synthesis',
          quote: `${normalizeVendorName(vendorDir)} fallback reclassification under new rubric`,
          file: reportPath,
        },
      ],
    };
  }

  return {
    reportPath,
    vendor: record.vendor || normalizeVendorName(vendorDir),
    assessedAt: TODAY,
    assessor: ASSESSOR,
    category: coerceCategory(record.category),
    subcategory: coerceSubcategory(record.subcategory),
    confidence: clampConfidence(record.confidence || 3),
    scores: ensureScores(record.scores),
    rationale: ensureArray(record.rationale),
    decisionRulesApplied: ensureArray(record.decisionRulesApplied),
    signals: ensureSignals(record.signals),
    domainCoverage: ensureDomainCoverage(record.domainCoverage, record.vendor || vendorDir),
    productContext: ensureProductContext(record.productContext, record.vendor || vendorDir, reportPath),
    scopeBoundaryNotes: ensureArray(record.scopeBoundaryNotes),
    formats: normalizeFormatList(record.formats),
    dataFiles: ensureArray(record.dataFiles),
    formatSignals: record.formatSignals || {
      transport: 'unknown',
      wrapper: 'unknown',
      fileExtensions: ['.json'],
      xmlFlavor: 'unknown_xml',
      notes: 'No format metadata preserved in source record.',
    },
    examples: ensureExamples(record.examples, reportPath),
    notes: record.notes,
    followUps: ensureArray(record.followUps),
    evidence: asEvidenceList(record.evidence, record.vendor || vendorDir, vendorDir),
  };
}

const existing = (() => {
  if (!fs.existsSync(INPUT_PATH)) {
    return [];
  }
  const raw = fs.readFileSync(INPUT_PATH, 'utf8');
  const parsed = JSON.parse(raw);
  return Array.isArray(parsed.records) ? parsed.records : [];
})();

const existingByReportPath = new Map(existing.map((r) => [r.reportPath, r]));

const completeVendors = fs
  .readdirSync(RESULTS_DIR)
  .filter((entry) => isDirectory(path.join(RESULTS_DIR, entry)))
  .filter((entry) => fileExists(path.join(RESULTS_DIR, entry, 'ehi-export-report.md')))
  .filter((entry) => fileExists(path.join(RESULTS_DIR, entry, 'product-research.md')))
  .filter((entry) => fileExists(path.join(RESULTS_DIR, entry, 'sources.json')))
  .sort();

const records = completeVendors.map((vendorDir) => {
  const reportPath = `results/${vendorDir}/ehi-export-report.md`;
  const existingRecord = existingByReportPath.get(reportPath);

  if (!existingRecord) {
    const override = applyFallbackOverride(vendorDir);
    if (override) {
      return {
        reportPath,
        vendor: normalizeVendorName(vendorDir),
        assessedAt: TODAY,
        assessor: ASSESSOR,
        category: override.category,
        subcategory: override.subcategory,
        confidence: override.confidence,
        scores: {
          scope: override.scores?.scope ?? 3,
          format: override.scores?.format ?? 2,
          dictionary: override.scores?.dictionary ?? 1,
          conflationRisk: override.scores?.conflationRisk ?? 2,
          accessibility: override.scores?.accessibility ?? 2,
        },
        rationale: override.rationale || ['Fallback rubric pass applied'],
        decisionRulesApplied: override.decisionRulesApplied || ['Fallback override used'],
        signals: {
          native: [
            {
              present: true,
              text: 'Mixed vendor-native export path and CCD XML API are both documented in the source artifacts.',
              cites: [
                'results/solidpractice-technologies-llc/ehi-export-report.md',
                'results/solidpractice-technologies-llc/downloads/SolidPractice-b10-exportable-data-content.pdf',
                'results/solidpractice-technologies-llc/downloads/SolidPractice-Data-Access-API.pdf',
              ],
            },
          ],
          g10Conflation: [
            {
              present: true,
              text: 'CCD XML subset maps to clinical sections and is standard-style C-CDA data.',
              cites: ['results/solidpractice-technologies-llc/ehi-export-report.md'],
            },
          ],
          underdocumented: [
            {
              present: true,
              text: 'PDF format is not accompanied by schema, JSON structure, or sample payloads.',
              cites: ['results/solidpractice-technologies-llc/ehi-export-report.md'],
            },
          ],
        },
        domainCoverage: ensureDomainCoverage(override.rationaleCoverage || {}),
        productContext: ensureProductContext(override.productContext || {}, normalizeVendorName(vendorDir), reportPath),
        scopeBoundaryNotes: ensureArray(override.scopeBoundaryNotes),
        formats: normalizeFormatList(override.formats || []),
        dataFiles: override.dataFiles || ['SolidPractice-Data-Access-API.pdf', 'SolidPractice-b10-exportable-data-content.pdf'],
        formatSignals: {
          transport: override.formatSignals?.transport || 'download',
          wrapper: override.formatSignals?.wrapper || 'unknown',
          fileExtensions: normalizePathList(override.formatSignals?.fileExtensions || ['.pdf', '.api']),
          xmlFlavor: override.formatSignals?.xmlFlavor || 'custom_xml',
          xmlFlavorChoices: override.formatSignals?.xmlFlavorChoices || ['ccda', 'custom_xml'],
          documentedFormats: override.formatSignals?.documentedFormats || ['PDF', 'XML', 'JSON'],
          schemaArtifacts: override.formatSignals?.schemaArtifacts || ['SolidPractice-b10-exportable-data-content.pdf'],
          notes: override.formatSignals?.notes || 'Fallback classification with mixed-format support.',
        },
        examples: {
          includedArtifacts: override.examples?.includedArtifacts || [],
          missingArtifacts: override.examples?.missingArtifacts || ['sample payload'],
          hasSampleData: false,
          sampleData: {
            hasSamples: false,
            sampleKinds: override.examples?.sampleKinds || [],
            sampleArtifacts: override.examples?.sampleArtifacts || [],
            missingKinds: override.examples?.missingKinds || ['sample payload'],
            missingReason: override.examples?.sampleReason,
          },
        },
        evidence: override.evidence || [
          {
            section: 'Assessment synthesis',
            quote: `${normalizeVendorName(vendorDir)} fallback classification without previous graded record`,
            file: reportPath,
          },
        ],
      };
    }

    return makeUnresolvedRecord(vendorDir);
  }

  return normalizeExistingRecord(existingRecord, vendorDir);
});

const payload = {
  schemaVersion: SCHEMA_VERSION,
  records,
};

fs.writeFileSync(OUTPUT_PATH, `${JSON.stringify(payload, null, 2)}\n`, 'utf8');
console.log(`Rebuilt ${path.relative(ROOT, OUTPUT_PATH)} with ${records.length} complete-vendor records`);
