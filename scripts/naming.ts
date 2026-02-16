// Shared naming utilities for EHI export analysis pipeline.
// Single source of truth for slugification and result directory naming.

/** Convert a name to a URL/filesystem-safe slug (no length limit). */
export function slugify(name: string): string {
  return name
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-|-$/g, "");
}

/** Build the result directory name for a family target. */
export function resultDirName(target: {
  developers: string[];
  family?: string;
  products?: string[];
}, idx?: number): string {
  let vendorSlug = slugify(target.developers[0]);
  if (target.developers.length > 1) vendorSlug = `${vendorSlug}-and-others-${idx ?? 0}`;
  const family = target.family ?? target.products?.[0] ?? "unknown";
  const familySlug = slugify(family);
  return `${vendorSlug}--${familySlug}`;
}
