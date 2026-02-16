"""Parse the PracticeSuite EHI export page HTML and K3 report page HTML.
Extract all substantive text content, headings, lists, and any structured data."""

from html.parser import HTMLParser
import json, re, os

RESULTS = "/home/jmandel/hobby/ehi-export-analysis/results/practicesuite-inc--practicesuite/downloads"

class TextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.sections = []
        self.current_text = []
        self.in_content = False
        self.skip_tags = {'script', 'style', 'nav', 'header', 'footer', 'noscript'}
        self.skip_depth = 0
        self.tag_stack = []
        
    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        if tag in self.skip_tags:
            self.skip_depth += 1
            return
        if self.skip_depth > 0:
            return
        if tag in ('h1','h2','h3','h4','h5','h6'):
            self.current_text.append(f"\n{'#' * int(tag[1])} ")
        elif tag == 'p':
            self.current_text.append('\n\n')
        elif tag == 'li':
            self.current_text.append('\n- ')
        elif tag == 'br':
            self.current_text.append('\n')
        elif tag == 'img':
            src = attrs_dict.get('src', '')
            alt = attrs_dict.get('alt', '')
            if src:
                self.current_text.append(f'\n[IMG: {alt or src}]\n')
    
    def handle_endtag(self, tag):
        if tag in self.skip_tags:
            self.skip_depth -= 1
            return
        if tag in ('h1','h2','h3','h4','h5','h6'):
            self.current_text.append('\n')
    
    def handle_data(self, data):
        if self.skip_depth > 0:
            return
        text = data.strip()
        if text:
            self.current_text.append(text + ' ')
    
    def get_text(self):
        return ''.join(self.current_text)

def extract_article_content(html_text):
    """Try to extract just the article/main content area"""
    # Try to find WordPress entry-content
    match = re.search(r'<div[^>]*class="[^"]*entry-content[^"]*"[^>]*>(.*?)</div>\s*</article>', html_text, re.DOTALL)
    if not match:
        match = re.search(r'<article[^>]*>(.*?)</article>', html_text, re.DOTALL)
    if not match:
        match = re.search(r'<main[^>]*>(.*?)</main>', html_text, re.DOTALL)
    if match:
        return match.group(1)
    return html_text

for fname, label in [("ehi-export-page.html", "EHI Export Page"), ("k3-report-page.html", "K3 Report Page")]:
    fpath = os.path.join(RESULTS, fname)
    with open(fpath) as f:
        html = f.read()
    
    content = extract_article_content(html)
    extractor = TextExtractor()
    extractor.feed(content)
    text = extractor.get_text()
    
    # Clean up whitespace
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r' +', ' ', text)
    
    outname = fname.replace('.html', '-extracted.txt')
    with open(outname, 'w') as f:
        f.write(f"=== {label} ===\n\n")
        f.write(text.strip())
    
    print(f"\n{'='*60}")
    print(f"{label} ({fname}): {len(html)} bytes HTML -> {len(text.strip())} chars text")
    print(f"Output: {outname}")
    
    # Also find all image references
    imgs = re.findall(r'<img[^>]+src="([^"]+)"[^>]*(?:alt="([^"]*)")?', content)
    print(f"Images found: {len(imgs)}")
    for src, alt in imgs:
        print(f"  - {alt or '(no alt)'}: {src.split('/')[-1]}")

print("\nDone.")
