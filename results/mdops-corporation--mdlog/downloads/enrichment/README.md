# Schema Enrichment

## Run Command

```bash
cd /home/jmandel/hobby/ehi-export-analysis/results/mdops-corporation--mdlog/downloads/enrichment
bun run extract-schema.ts
```

## Input Boundary

Parses all `*-schema.xml` files in the `../` (downloads) directory:

- `ccd-schema.xml` — CCD Clinical Document Architecture schema (POCD_MT000040)
- `datatype-schema.xml` — HL7 v3 data types
- `voc-schema.xml` — HL7 v3 vocabulary/value set enumerations
- `narrative-block-schema.xml` — CDA narrative block structures

## Output Files

- `schema-extract.json` — Complete structured extraction of all complex types, simple types,
  elements, attributes, and enumeration values from all 4 schema files.

## Known Limitations

- Regex-based XML parsing; does not use a full XSD parser
- Nested complex types within elements (anonymous types) are not extracted
- Documentation annotations within types are captured only at the top level
- Schema inheritance (extension/restriction) relationships are not resolved
