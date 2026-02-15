# Source Explorer PRD (Dashboard v2)

## Objective
Build a single-pane dashboard workflow where every graded aggregate point can be traced directly into the underlying source materials for each vendor, including markdown and JSON artifacts, without opening separate files.

## Scope in
- Keep `abstraction/ehi-dashboard.html` standalone (no external network deps).
- Parse complete folders from `abstraction/ehi-grading-results.json` records.
- Ignore incomplete folders.
- Embed source files at build time and render them in the dashboard.
- Add a dedicated Source Explorer panel with:
  - vendor selector and file search/filter,
  - file list with path context,
  - viewer supporting markdown rendering and JSON pretty printing,
  - fallback rendering for other text files.
- Add pivot interactions:
  - open source explorer from record table row,
  - prefer vendor report and evidence-cited files,
  - allow switching to full report artifacts from record/abstract JSON context.
- Add clear logic for unsupported file types (skip binaries), with metadata notes.

## Scope out
- No runtime remote fetching.
- No PDF/image rendering inside dashboard (show file metadata/no-preview placeholders).
- No heavy reclassification of prior rubric schema in this pass.

## Data and acceptance
- Complete vendors in current grading set: 20.
- All generated source data must include at least one full-text artifact per completed vendor.
- Interactive pivot points must move from table/insights into the same vendor file list.
- Markdown and JSON files must render in dedicated views with escaped raw fallback.

