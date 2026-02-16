# Enrichment: iPatientCare EHI Export Documentation

## Run Command

```bash
cd /home/jmandel/hobby/ehi-export-analysis/results/assurecare-llc--ipatientcare/downloads/enrichment
bun run extract-export-summary.ts
```

## Input Boundary

Parses 3 JSON files from the downloads directory:
- `../fhir-capability-statement.json` — FHIR CapabilityStatement from production server
- `../smart-configuration.json` — SMART on FHIR well-known configuration
- `../fhir-endpoints-bundle.json` — FHIR Bundle of Endpoint/Organization resources

Note: The two PDF documents (EHI export guide, SMART API guide) are not parsed programmatically
because the EHI export PDF has no structured data to extract (it's a single page of prose) and
the SMART API guide contains standard FHIR US Core examples that are already captured in the
CapabilityStatement.

## Output Files

- `export-summary.json` — Complete queryable summary including:
  - Export format documentation (C-CDA, FHIR Bulk Data)
  - FHIR server details (26 resource types with profiles, interactions, search params)
  - SMART on FHIR capabilities and OAuth2 endpoints
  - Tenant/organization directory (107 organizations with NPI, location)
  - Coverage assessment (covered vs. likely missing data domains)

## Known Limitations

- PDF text extraction is not included; only JSON artifacts are processed
- The enrichment cannot determine what data elements are actually included in
  C-CDA exports (no C-CDA template documentation was provided by the vendor)
- Organization active/inactive status from the endpoints bundle may not reflect
  current production state
