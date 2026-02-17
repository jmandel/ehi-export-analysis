/**
 * Core logic for creating SingleFile snapshots of HTML files in a results dir.
 *
 * Used by both scripts/run-singlefile.ts (standalone) and scripts/run-download.ts
 * (optional post-download step).
 *
 * Default policy: for each directory containing HTML files, snapshot up to
 * `perDir` files (default 3), prioritizing files whose names contain
 * index/overview/export/main/etc. Use `--all` to snapshot everything.
 *
 * By default, each single-file invocation launches its own headless Chrome
 * (located via CHROME_PATH env var). Pass `--browser-server <url>` to reuse
 * an externally-managed Chrome instance instead.
 */

import { existsSync, mkdirSync, unlinkSync } from "node:fs";
import { join, dirname, basename, extname } from "node:path";

const CHROME = process.env.CHROME_PATH ?? "/usr/bin/google-chrome-stable";
const DEFAULT_PER_DIR = 3;

const PRIORITY_KEYWORDS = /\b(index|overview|export|main|certification|ehi|home|landing|about|default)\b/i;

export interface FileEntry {
  path: string;
  source_url: string | null;
  size_bytes: number;
  description: string;
  curl_command: string | null;
}

export interface FilesManifest {
  collection_date: string;
  url: string;
  final_url: string;
  access_status: string;
  files: FileEntry[];
}

export interface SnapshotResult {
  created: number;
  skipped: number;
  failed: number;
}

// ── File selection ───────────────────────────────────────────────────────────

/** Select HTML files to snapshot, capping per directory with priority sorting. */
function selectFiles(allHtml: FileEntry[], perDir: number): FileEntry[] {
  const byDir = new Map<string, FileEntry[]>();
  for (const f of allHtml) {
    const d = dirname(f.path);
    if (!byDir.has(d)) byDir.set(d, []);
    byDir.get(d)!.push(f);
  }

  const selected: FileEntry[] = [];
  for (const [, files] of [...byDir.entries()].sort((a, b) => a[0].localeCompare(b[0]))) {
    files.sort((a, b) => {
      const aPrio = PRIORITY_KEYWORDS.test(basename(a.path)) ? 0 : 1;
      const bPrio = PRIORITY_KEYWORDS.test(basename(b.path)) ? 0 : 1;
      if (aPrio !== bPrio) return aPrio - bPrio;
      return a.path.localeCompare(b.path);
    });
    selected.push(...files.slice(0, perDir));
  }
  return selected;
}

// ── Main entry point ─────────────────────────────────────────────────────────

export async function snapshotHtmlFiles(
  resultsDir: string,
  opts: { force?: boolean; perDir?: number; browserServer?: string } = {},
): Promise<SnapshotResult> {
  const perDir = opts.perDir ?? DEFAULT_PER_DIR;

  const filesJsonPath = join(resultsDir, "files.json");
  if (!existsSync(filesJsonPath)) {
    throw new Error(`files.json not found: ${filesJsonPath}`);
  }

  const manifest: FilesManifest = await Bun.file(filesJsonPath).json();

  if (opts.force) {
    manifest.files = manifest.files.filter(f => !f.path.includes(".singlefile."));
  }

  const allHtml = manifest.files.filter(f => {
    const ext = extname(f.path).toLowerCase();
    return (ext === ".html" || ext === ".htm")
      && !f.path.includes(".singlefile.")
      && f.source_url
      && f.source_url !== "n/a";
  });

  const htmlFiles = selectFiles(allHtml, perDir);

  if (htmlFiles.length === 0) {
    console.log("  No HTML files with source URLs — nothing to snapshot.");
    return { created: 0, skipped: 0, failed: 0 };
  }

  // Filter out already-existing snapshots (unless forcing)
  const toProcess = opts.force
    ? htmlFiles
    : htmlFiles.filter(e => {
        const sp = e.path.replace(/\.(html?)$/i, ".singlefile.$1");
        return !existsSync(join(resultsDir, sp));
      });

  const skippedExisting = htmlFiles.length - toProcess.length;

  const skippedByPolicy = allHtml.length - htmlFiles.length;
  if (skippedByPolicy > 0) {
    console.log(`  HTML files: ${allHtml.length} total, ${htmlFiles.length} selected (${perDir}/dir cap, ${skippedByPolicy} skipped)`);
  } else {
    console.log(`  HTML files to snapshot: ${htmlFiles.length}`);
  }
  if (skippedExisting > 0) {
    console.log(`  Already snapshotted: ${skippedExisting} (use --force to redo)`);
  }

  if (toProcess.length === 0) {
    return { created: 0, skipped: skippedExisting, failed: 0 };
  }

  // Build single-file browser args: use external server if provided,
  // otherwise let single-file launch Chrome itself.
  const browserArgs: string[] = opts.browserServer
    ? ["--browser-server", opts.browserServer]
    : ["--browser-executable-path", CHROME];

  if (opts.browserServer) {
    console.log(`  Using external Chrome at ${opts.browserServer}`);
  }

  let created = 0, failed = 0;
  const newEntries: FileEntry[] = [];

  for (const entry of toProcess) {
    const snapshotPath = entry.path.replace(/\.(html?)$/i, ".singlefile.$1");
    const fullSnapshotPath = join(resultsDir, snapshotPath);

    mkdirSync(dirname(fullSnapshotPath), { recursive: true });

    console.log(`  SNAP ${entry.source_url}`);
    console.log(`    → ${snapshotPath}`);

    const proc = Bun.spawn(
      [
        "single-file",
        ...browserArgs,
        "--browser-wait-until", "networkIdle",
        "--browser-load-max-time", "30000",
        entry.source_url!,
        fullSnapshotPath,
      ],
      { stdout: "pipe", stderr: "pipe", timeout: 60_000 },
    );

    const exitCode = await proc.exited;
    if (exitCode !== 0) {
      const stderr = await new Response(proc.stderr).text();
      console.log(`    ✗ FAILED (exit ${exitCode}): ${stderr.trim().slice(0, 200)}`);
      failed++;
      continue;
    }

    const size = Bun.file(fullSnapshotPath).size;
    if (size < 100) {
      console.log(`    ✗ FAILED (output too small: ${size} bytes)`);
      try { unlinkSync(fullSnapshotPath); } catch {}
      failed++;
      continue;
    }

    if (!manifest.files.some(f => f.path === snapshotPath)) {
      newEntries.push({
        path: snapshotPath,
        source_url: entry.source_url,
        size_bytes: size,
        description: `SingleFile snapshot of ${basename(entry.path)} — self-contained HTML with inlined CSS/images/fonts.`,
        curl_command: null,
      });
    }

    created++;
    console.log(`    ✓ ${size} bytes`);
  }

  if (newEntries.length > 0) {
    manifest.files.push(...newEntries);
  }

  if (newEntries.length > 0 || opts.force) {
    await Bun.write(filesJsonPath, JSON.stringify(manifest, null, 2) + "\n");
    if (newEntries.length > 0) {
      console.log(`  Updated files.json with ${newEntries.length} snapshot entries.`);
    }
  }

  return { created, skipped: skippedExisting, failed };
}
