#!/usr/bin/env python3
"""Checks heatguide.planetdetroit.org against spec.md (acceptance criteria §5).

Each check has a plain-English comment saying what it protects.
Run with:  python3 tests/test_page.py
"""
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
failures = []


def check(name, condition, detail=""):
    if condition:
        print(f"  PASS  {name}")
    else:
        print(f"  FAIL  {name}  {detail}")
        failures.append(name)


def strip_tags(s):
    s = re.sub(r"<(script|style)[^>]*>.*?</\1>", "", s, flags=re.S)
    return re.sub(r"<[^>]+>", " ", s)


html_src = (ROOT / "index.html").read_text()
css_src = (ROOT / "styles.css").read_text()
es_path = ROOT / "es" / "index.html"
es_src = es_path.read_text() if es_path.exists() else None

# ---- Hosting -------------------------------------------------------------
# GitHub Pages serves the custom domain from this file — exact content matters.
check("CNAME is exactly heatguide.planetdetroit.org",
      (ROOT / "CNAME").read_text().strip() == "heatguide.planetdetroit.org")

# ---- Emergency-first structure ------------------------------------------
# One h1 only, and the 911 block comes before the early-signs block, so a
# panicking reader sees the most urgent info first.
check("Exactly one h1", len(re.findall(r"<h1[\s>]", html_src)) == 1)
check("Has tel:911 link", 'href="tel:911"' in html_src)
emerg = html_src.find('id="emergency"')
signs = html_src.find('id="signs"')
check("Emergency section appears before early-signs section",
      0 < emerg < signs, f"emergency@{emerg} signs@{signs}")
for sec in ["emergency", "signs", "tools", "report", "reporting"]:
    check(f"Section #{sec} exists", f'id="{sec}"' in html_src)

# ---- Required resource links (spec §4.8, research table) ----------------
REQUIRED = {
    "App Store": "https://apps.apple.com/us/app/osha-niosh-heat-safety-tool/id1239425102",
    "Google Play": "https://play.google.com/store/apps/details?id=erg.com.nioshheatindex",
    "CDC illnesses": "https://www.cdc.gov/niosh/heat-stress/about/illnesses.html",
    "CDC app page": "https://www.cdc.gov/niosh/heat-stress/communication-resources/app.html",
    "MIOSHA heat": "https://www.michigan.gov/leo/bureaus-agencies/miosha/topics/heat",
    "MIOSHA complaint": "https://www.michigan.gov/leo/bureaus-agencies/miosha/enforcement-and-appeals/how-to-file-a-complaint-with-miosha",
    "OSHA heat": "https://www.osha.gov/heat-exposure",
    "OSHA complaint": "https://www.osha.gov/workers/file-complaint",
    "Heat and Harm": "https://deepdives.planetdetroit.org/heat-and-harm/",
}
for name, url in REQUIRED.items():
    check(f"Links to {name}", f'href="{url}"' in html_src)
check("MIOSHA phone is tap-to-call", 'href="tel:18008664674"' in html_src)

# ---- Link hygiene (spec §4.7) -------------------------------------------
ext = re.findall(r'<a\s[^>]*href="https?://[^"]+"[^>]*>', html_src)
check("External links open in new tab with rel=noopener",
      ext and all('target="_blank"' in a and 'rel="noopener"' in a for a in ext), f"{len(ext)} links")
hrefs = re.findall(r'href="([^"]+)"', html_src)
check("No deep PDF or ?rev= links (they break when agencies re-upload)",
      not any(".pdf" in h.lower() or "?rev=" in h for h in hrefs))

# ---- Self-contained & fast (spec §4.3) ----------------------------------
# The only allowed third-party request is the GA4 tag Nina approved.
externals = re.findall(r'(?:src|href)="(https?://[^"]+)"', html_src)
loaded = [u for u in externals if re.search(r'<(script|link|img)[^>]+' + re.escape(u), html_src)]
check("Only external asset loaded is GA4",
      all("googletagmanager.com" in u for u in loaded), str(loaded))
check("Uses local styles.css", 'href="styles.css"' in html_src)
check("No web-font imports", "@import" not in css_src and "fonts.googleapis" not in html_src)
total = sum(p.stat().st_size for p in [ROOT / "index.html", ROOT / "styles.css", *(ROOT / "assets").glob("*")])
check("Page weight under 150 KB", total < 150_000, f"{total} bytes")

# ---- GA4 (spec §4.15) ---------------------------------------------------
check("GA4 tag present (G-5QQJ9SVV07, same property as other PD sites)",
      "G-5QQJ9SVV07" in html_src)

# ---- Search-friendly (spec §4.11) ---------------------------------------
check("No noindex (holding-page tag removed)", 'name="robots"' not in html_src or "noindex" not in html_src)
check("Has <title>", re.search(r"<title>[^<]{10,}</title>", html_src) is not None)
check("Has meta description", 'name="description"' in html_src)
check("Has viewport meta", 'name="viewport"' in html_src)
check("html lang=en", '<html lang="en">' in html_src)

# ---- Readable on phones in sunlight (spec §4.2) -------------------------
m = re.search(r"body\s*{[^}]*font-size:\s*(\d+)px", css_src)
check("Body font size >= 17px", m and int(m.group(1)) >= 17, m.group(0) if m else "none")
m = re.search(r"\.btn\s*{[^}]*min-height:\s*(\d+)px", css_src)
check("Buttons at least 48px tall", m and int(m.group(1)) >= 48)
check("Has print stylesheet", "@media print" in css_src)
check("Brand accent blue #2982C4 used", "#2982C4" in css_src.upper())

# ---- Evergreen (spec §4.6): no dates in body copy -----------------------
body = strip_tags(html_src)
foot_i = html_src.find("<footer")
body_only = strip_tags(html_src[:foot_i]) if foot_i > 0 else body
check("No years in body copy (dates only in footer)",
      not re.search(r"\b(19|20)\d{2}\b", body_only), (re.search(r"\b(19|20)\d{2}\b.{0,30}", body_only) or [""])[0] if re.search(r"\b(19|20)\d{2}\b", body_only) else "")
check("Footer has 'Last reviewed'", "Last reviewed" in html_src)
check("Footer has not-medical-advice line", re.search(r"not (a substitute for )?medical advice", html_src, re.I) is not None)

# ---- Accessibility -------------------------------------------------------
imgs = re.findall(r"<img[^>]*>", html_src)
check("All images have alt text", imgs and all(re.search(r'\balt="', i) for i in imgs), f"{len(imgs)} imgs")

# ---- Well-formed ---------------------------------------------------------
class P(HTMLParser):
    VOID = {"meta", "link", "img", "br", "hr", "input", "source"}
    def __init__(self):
        super().__init__(); self.stack = []; self.bad = []
    def handle_starttag(self, tag, attrs):
        if tag not in self.VOID: self.stack.append(tag)
    def handle_endtag(self, tag):
        if self.stack and self.stack[-1] == tag: self.stack.pop()
        else: self.bad.append(tag)
p = P(); p.feed(html_src)
check("Tags are balanced (EN)", not p.stack and not p.bad, f"open={p.stack} stray={p.bad}")

# ---- Spanish page (only once Isabelle's translation ships) --------------
if es_src is None:
    print("  SKIP  es/index.html not present yet — language toggle must be absent")
    check("No language toggle before Spanish exists", 'class="lang-switch"' not in html_src)
else:
    check("ES html lang=es", '<html lang="es">' in es_src)
    check("ES has same number of h2 sections as EN",
          len(re.findall(r"<h2[\s>]", es_src)) == len(re.findall(r"<h2[\s>]", html_src)))
    check("EN links to /es/", 'href="/es/"' in html_src)
    check("ES links to /", 'href="/"' in es_src)
    p2 = P(); p2.feed(es_src)
    check("Tags are balanced (ES)", not p2.stack and not p2.bad)

print()
if failures:
    print(f"{len(failures)} check(s) failed"); sys.exit(1)
print("All checks passed")
