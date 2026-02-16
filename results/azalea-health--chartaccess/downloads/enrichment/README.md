# Enrichment: Azalea Health ChartAccess EHI Export

## Run Command

```bash
cd /home/jmandel/hobby/ehi-export-analysis/results/azalea-health--chartaccess/downloads/enrichment
bun run extract-export-mappings.ts
```

## Input Boundary

- `../hospital_export.html` — Hospital EHI Export Guide page from dev.azaleahealth.com
- `../capability-statement-hospital.json` — FHIR R4 CapabilityStatement from hospital.azaleahealth.com

## Output Files

- `export-mappings.json` — Complete extraction including:
  - 45 EHR concept → FHIR resource mappings from the export guide
  - CapabilityStatement resource inventory (36 resource types)
  - Coverage analysis (resources in mappings vs. CapabilityStatement)
  - Export format specification
  - File inventory of all downloaded artifacts

## Known Limitations

- HTML table parsing uses regex; may break if Azalea changes their HTML structure
- Only parses the Hospital platform export guide (not Ambulatory, which is a different product)
- Does not parse the rendered JavaScript content; works on server-rendered HTML
