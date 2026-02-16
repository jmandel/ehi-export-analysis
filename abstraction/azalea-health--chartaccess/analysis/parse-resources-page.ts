import * as cheerio from "cheerio";
import { readFileSync } from "fs";
import { join } from "path";
const html = readFileSync(join(__dirname, "../../../results/azalea-health--chartaccess/downloads/hospital_resources.html"), "utf-8");
const $ = cheerio.load(html);
const main = $("main");
const rows = main.find("div.row.border-bottom.mx-0.p-2");
console.log(`Total rows in resources page: ${rows.length}`);
rows.each((i, row) => {
  const cols = $(row).find("div");
  const texts = cols.map((_, c) => $(c).text().trim()).get();
  if (texts[0] === "Resource") return; // header
  console.log(`  ${texts.join(" | ")}`);
});
