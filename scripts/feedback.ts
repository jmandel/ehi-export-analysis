/**
 * Load phase-specific feedback entries from feedback.json.
 *
 * feedback.json is a repo-root array of objects:
 *   { results_dir, abstraction_dir, phase, issue?, text }
 *
 * Entries match if the phase matches AND either results_dir or
 * abstraction_dir matches the provided dirSlug.
 */

import { readFileSync, existsSync } from "node:fs";
import { join, dirname } from "node:path";

const ROOT_DIR = join(dirname(import.meta.path), "..");

export interface FeedbackEntry {
  results_dir?: string;
  abstraction_dir?: string;
  phase: string;
  issue?: number;
  text: string;
}

export function loadFeedback(dirSlug: string, phase: string): FeedbackEntry[] {
  const feedbackPath = join(ROOT_DIR, "feedback.json");
  if (!existsSync(feedbackPath)) return [];

  try {
    const entries: FeedbackEntry[] = JSON.parse(readFileSync(feedbackPath, "utf8"));
    return entries.filter(
      (e) =>
        e.phase === phase &&
        (e.results_dir === dirSlug || e.abstraction_dir === dirSlug),
    );
  } catch {
    return [];
  }
}

export function renderFeedbackSection(dirSlug: string, phase: string): string {
  const entries = loadFeedback(dirSlug, phase);
  if (entries.length === 0) return "";

  const lines = [
    "",
    "## Feedback from prior reviews",
    "",
    "The following notes were recorded from previous pipeline runs or issue fixes.",
    "Take them into account when doing your work:",
    "",
  ];

  for (const entry of entries) {
    const issueRef = entry.issue ? ` (from issue #${entry.issue})` : "";
    lines.push(`- ${entry.text}${issueRef}`);
  }

  return lines.join("\n");
}
