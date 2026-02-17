# Fixup Log

**Date**: 2026-02-17
**Issue**: Field counts inflated by duplication across shared event definitions; patient messaging gap missed

## Diagnosis
- Root cause stage: 3 (Analysis)
- Problem: `parse-data-dictionary.ts` did not deduplicate fields when multiple event definitions share the same form. The XLSX crosswalk has one row per field per `event_definition_id`. For example, `BSAS_STAND_IE` is shared by 14 enrollment event types, so its 153 unique fields appeared as 2,142. This affected 107 of 1,314 event forms. Non-events had a similar issue from the SQL UNION including print-bundle duplicates, affecting all 118 non-event form codes with columns.

## Changes Made
- **Fixed `parse-data-dictionary.ts`** (events): Filter to one `event_definition_id` per `form_code` before collecting fields, plus a dedup-key guard (`form:prop`, `sub:code:prop`, `assess:code:qid`) for any remaining duplicates within a single event_definition.
- **Fixed `parse-data-dictionary.ts`** (non-events): Added same dedup-key mechanism to eliminate duplicates from the SQL UNION bringing in print-bundle versions.
- **Corrected counts**: Total fields 131,109 → 93,152 (29% was duplication). BSAS_STAND_IE: 2,142 → 153. CLIENT_LOGIN: 16 → 8.
- **Identified patient messaging gap**: `PERS_MESSAGES` (Person Messages) exists as a 0-field stub. Product has patient portal (myHealthPointe, certified (e)(1)/(e)(3)) and secure messaging (CareConnect Inbox), but message content is not exported.

## Cascade
- Reran analysis (stage 3) with `--focus` context explaining the dedup fix, data model, and messaging gap
- Reran summary (stage 4) — grade adjusted from A- to B+ reflecting billing and messaging gaps
- Updated dashboard copy

## Verification
- `BSAS_STAND_IE`: 153 fields (was 2,142) ✓
- `CLIENT_LOGIN`: 8 fields (was 16) ✓  
- Total fields: 93,152 (was 131,109) ✓
- `PERS_MESSAGES`: confirmed 0 fields in entity inventory ✓
- analysis.md: correctly explains data model hierarchy, dedup methodology, and messaging gap ✓
- summary.json: updated entity_count=1565, field_count=93152, coverage=partial, patient_communications=excluded ✓
