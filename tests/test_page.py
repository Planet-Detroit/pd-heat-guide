#!/usr/bin/env python3
"""Checks the heatguide.planetdetroit.org holding page.

Plain-English purpose of each check is in the comment above it.
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


html_src = (ROOT / "index.html").read_text()
css_src = (ROOT / "styles.css").read_text()

# GitHub Pages serves the custom domain from this file — exact content matters.
check("CNAME is exactly heatguide.planetdetroit.org",
      (ROOT / "CNAME").read_text().strip() == "heatguide.planetdetroit.org")

# Mobile site: must have the viewport meta or phones render it zoomed-out.
check("Has mobile viewport meta",
      re.search(r'<meta name="viewport" content="width=device-width, initial-scale=1', html_src) is not None)

# Page must say what it is: a heat guide from Planet Detroit, coming soon.
check("Title mentions Heat Guide", re.search(r"<title>[^<]*Heat Guide[^<]*</title>", html_src) is not None)
check("Body says Planet Detroit", "Planet Detroit" in html_src)
check("Body says coming soon", re.search(r"coming soon", html_src, re.I) is not None)

# Holding page links to the newsletters page so readers can be told when it launches,
# and to the existing Heat and Harm deep dive so the page is useful today.
check("Links to planetdetroit.org/newsletters/",
      'href="https://planetdetroit.org/newsletters/"' in html_src)
check("Links to Heat and Harm deep dive",
      'href="https://deepdives.planetdetroit.org/heat-and-harm/"' in html_src)

# Search engines shouldn't index a placeholder.
check("noindex while it is a holding page",
      re.search(r'<meta name="robots" content="noindex', html_src) is not None)

# No external CSS/JS: the page must load fast on a phone with poor signal.
check("No external stylesheets or scripts",
      not re.search(r'<(link[^>]+rel="stylesheet"|script)[^>]+href?="https?://', html_src))
check("Uses local styles.css", 'href="styles.css"' in html_src)

# Every image needs alt text (accessibility).
imgs = re.findall(r"<img[^>]*>", html_src)
check("All images have alt text", all(re.search(r'\balt="', i) for i in imgs), f"{len(imgs)} imgs")

# All external links open safely.
ext = re.findall(r'<a[^>]+href="https?://[^"]+"[^>]*>', html_src)
check("External links have rel=noopener", all('rel="noopener"' in a for a in ext), f"{len(ext)} links")

# Brand colors are used (from design-system/colors/palette.html).
check("Uses brand accent blue #2982C4", "#2982C4" in css_src.upper())

# HTML is well-formed enough that a parser doesn't choke.
class P(HTMLParser):
    def __init__(self):
        super().__init__(); self.stack = []; self.bad = []
    VOID = {"meta", "link", "img", "br", "hr", "input"}
    def handle_starttag(self, tag, attrs):
        if tag not in self.VOID: self.stack.append(tag)
    def handle_endtag(self, tag):
        if self.stack and self.stack[-1] == tag: self.stack.pop()
        else: self.bad.append(tag)
p = P(); p.feed(html_src)
check("Tags are balanced", not p.stack and not p.bad, f"open={p.stack} stray={p.bad}")

print()
if failures:
    print(f"{len(failures)} check(s) failed"); sys.exit(1)
print("All checks passed")
