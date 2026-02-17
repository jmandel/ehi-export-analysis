/**
 * Shared prompt template renderer.
 * Replaces {{VAR}} placeholders and includes {{FILE_NAME}} from prompts dir.
 */

import * as fs from "fs";
import * as path from "path";

export function renderTemplate(
  templatePath: string,
  vars: Record<string, string>,
  promptsDir?: string,
): string {
  let tmpl = fs.readFileSync(templatePath, "utf8");

  for (const [key, value] of Object.entries(vars)) {
    tmpl = tmpl.replaceAll("{{" + key + "}}", value);
  }

  // File includes for remaining {{PLACEHOLDERS}}
  if (promptsDir) {
    tmpl = tmpl.replace(/\{\{([A-Z_]+)\}\}/g, (match, key) => {
      const filename = key.toLowerCase().replace(/_/g, "-") + ".md";
      const filepath = path.join(promptsDir, filename);
      try {
        return fs.readFileSync(filepath, "utf8");
      } catch {
        return match;
      }
    });
  }

  return tmpl;
}
