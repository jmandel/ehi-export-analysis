#!/usr/bin/env node
'use strict';

const fs = require('node:fs');
const path = require('node:path');

const INPUT_PATH = path.join(__dirname, 'ehi-grading-results.json');
const OUTPUT_PATH = path.join(__dirname, 'ehi-dashboard-insights.json');

function countMap(items) {
  const map = {};
  for (const item of items) {
    map[item] = (map[item] || 0) + 1;
  }
  return map;
}

function topNFromMap(map, n = 10) {
  return Object.entries(map)
    .sort((a, b) => {
      if (b[1] !== a[1]) {
        return b[1] - a[1];
      }
      return a[0].localeCompare(b[0]);
    })
    .slice(0, n);
}

function normalizeFormatList(recordPath) {
  if (Array.isArray(recordPath)) {
    return recordPath
      .map((value) => String(value || '').trim().toLowerCase())
      .filter(Boolean);
  }

  return String(recordPath || '')
    .split('\n')
    .map((value) => String(value || '').trim().toLowerCase())
    .filter(Boolean);
}

function inferFormatFlags(records) {
  const signalFlags = {
    formats_csv: 0,
    mentions_fhir: 0,
    formats_ndjson: 0,
    formats_json_like: 0,
    formats_parquet: 0,
    native_ccda: 0,
    formats_xml: 0,
    formats_pdf: 0,
  };

  for (const record of records) {
    const hasCsv = (record.formats || []).some((value) => /csv/i.test(value));
    const hasFhir = (record.formats || []).some((value) => /fhir/i.test(value));
    const hasNdjson = (record.formats || []).some((value) => /ndjson|jsonl/i.test(value));
    const hasJson = (record.formats || []).some((value) => /json/i.test(value));
    const hasParquet = (record.formats || []).some((value) => /parquet/i.test(value));
    const hasCcda = (record.formats || []).some((value) => /c[- ]?cda|ccda/i.test(value));
    const hasXml = (record.formats || []).some((value) => /xml/i.test(value));
    const hasPdf = (record.formats || []).some((value) => /pdf/i.test(value));

    if (hasCsv) signalFlags.formats_csv += 1;
    if (hasFhir) signalFlags.mentions_fhir += 1;
    if (hasNdjson) signalFlags.formats_ndjson += 1;
    if (hasJson) signalFlags.formats_json_like += 1;
    if (hasParquet) signalFlags.formats_parquet += 1;
    if (hasCcda) signalFlags.native_ccda += 1;
    if (hasXml) signalFlags.formats_xml += 1;
    if (hasPdf) signalFlags.formats_pdf += 1;
  }

  return signalFlags;
}

function numericAverage(values) {
  if (!values.length) {
    return 0;
  }

  const total = values.reduce((sum, value) => sum + value, 0);
  return total / values.length;
}

function normalizeSamples(record) {
  const sampleData = record?.examples?.sampleData;
  const hasSampleData = record?.examples?.hasSampleData;

  if (typeof hasSampleData === 'boolean') {
    return hasSampleData;
  }

  if (sampleData && typeof sampleData.hasSamples === 'boolean') {
    return sampleData.hasSamples;
  }

  return false;
}

function run() {
  const raw = fs.readFileSync(INPUT_PATH, 'utf8');
  const { records = [] } = JSON.parse(raw);

  const categoryCounts = countMap(records.map((record) => record.category));
  const subcategoryCounts = countMap(records.map((record) => record.subcategory));
  const confidenceCounts = countMap(records.map((record) => String(record.confidence)));

  const coveredTop = topNFromMap(countMap(records.flatMap((record) => record?.domainCoverage?.covered || [])), 12);
  const missingTop = topNFromMap(countMap(records.flatMap((record) => record?.domainCoverage?.potentiallyMissing || [])), 12);

  const avgScores = {
    scope: numericAverage(records.map((record) => Number(record?.scores?.scope || 0))).toFixed(2),
    format: numericAverage(records.map((record) => Number(record?.scores?.format || 0))).toFixed(2),
    dictionary: numericAverage(records.map((record) => Number(record?.scores?.dictionary || 0))).toFixed(2),
    conflationRisk: numericAverage(records.map((record) => Number(record?.scores?.conflationRisk || 0))).toFixed(2),
    accessibility: numericAverage(records.map((record) => Number(record?.scores?.accessibility || 0))).toFixed(2),
  };

  const sampleData = {
    true: 0,
    false: 0,
    missing: 0,
  };

  for (const record of records) {
    const hasSamples = normalizeSamples(record);
    if (record?.examples?.hasSampleData == null && !record?.examples?.sampleData) {
      sampleData.missing += 1;
    } else if (hasSamples) {
      sampleData.true += 1;
    } else {
      sampleData.false += 1;
    }
  }

  const signalFlags = inferFormatFlags(records);

  const avgPotentiallyMissing = numericAverage(
    records.map((record) => Number((record?.domainCoverage?.potentiallyMissing || []).length)),
  );

  const out = {
    n: records.length,
    categoryCounts,
    subcategoryCounts,
    confidenceCounts,
    avgScores: {
      scope: parseFloat(avgScores.scope),
      format: parseFloat(avgScores.format),
      dictionary: parseFloat(avgScores.dictionary),
      conflationRisk: parseFloat(avgScores.conflationRisk),
      accessibility: parseFloat(avgScores.accessibility),
    },
    sampleData,
    coveredTop,
    missingTop,
    signalFlags,
    avgPotentiallyMissing: parseFloat(avgPotentiallyMissing.toFixed(2)),
  };

  fs.writeFileSync(OUTPUT_PATH, `${JSON.stringify(out, null, 2)}\n`, 'utf8');
  console.log(`Computed dashboard insights for ${records.length} records`);
}

run();
