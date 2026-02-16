# Healthie EHI Export Data Dictionary Enrichment

## Run command

```bash
cd /home/jmandel/hobby/ehi-export-analysis/results/healthie--healthie/downloads/enrichment
bun run extract-data-dictionary.ts
```

## Input boundary

- Single file: `../ehi-export-page.html` — the raw HTML of the Healthie (b)(10) EHI export documentation page from `https://help.gethealthie.com/article/1200-b10-electronic-health-information-export-on-healthie`

## Output files

- `data-dictionary.json` — structured JSON with all 38 export file definitions, 451 total columns, export generation instructions, and overview metadata
- `extraction-log.json` — accounting output: files listed vs parsed, parse errors, type breakdown

## Known parsing limitations

- The source HTML contains a typo ("MirroEntry.csv" instead of "MirrorEntry.csv") which is corrected during parsing
- The "publicly accessible hyperlink" in the format.html description points to `#undefined` (broken link) in the source
- Many journal-type CSV files (FoodEntry, MetricEntry, MirrorEntry, NoteEntry, PoopEntry, SleepEntry, SymptomEntry, WaterIntakeEntry, WorkoutEntry) share an identical column schema — this appears to be a generic entry format, not a parsing artifact
- Documents folder, format.html, and journal_entries.pdf have no tabular column definitions and are added as manually-defined entries with text descriptions
- Data types are not specified in the source documentation beyond "All data in the CSV files will be exported as a string"
