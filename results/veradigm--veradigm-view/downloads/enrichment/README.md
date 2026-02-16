# Veradigm View EHI Export Documentation — Enrichment

## Run command

```bash
bun run extract-entities.ts
```

## Input boundary

- `../v6-index.html` — V6 index page (category assignments, entity descriptions)
- `../v6-entities/*.html` — 87 individual entity documentation pages

## Output files

- `entities-catalog.json` — Complete structured catalog of all 87 entities with their fields, data types, descriptions, and category assignments
- `coverage-accounting.json` — Parse statistics: files discovered, parsed, failures, field counts by entity and category

## Known parsing limitations

- Extracts only the first `<table class="table ...">` per page (each page has exactly one)
- Field descriptions that contain HTML tags are stripped to plain text
- Category assignments come from the index page's `<h3>` headings; if an entity slug is not found in the index, it gets category "Unknown"
