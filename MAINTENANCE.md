# Maintenance — pd-heat-guide

## What this does
Serves https://heatguide.planetdetroit.org/ — a static, one-page heat-safety guide for workers. No server, no database, no build. It should need about an hour of attention a year.

## How to tell it's working
- Open the URL on a phone: white header with Planet Detroit logo, red "Heat stroke = call 911" box first, blue resource buttons below, dark footer. Padlock icon (HTTPS) present.
- `curl -sI https://heatguide.planetdetroit.org/ | head -1` → `HTTP/2 200`.
- `python3 tests/test_page.py` → "All checks passed".
- GitHub → Actions → "Monthly link check" → last run green.

## Yearly review (put on the calendar for each June, before heat season)
1. Isabelle re-reads the copy against the current NIOSH/CDC guidance.
2. Run `python3 tests/check_links.py`; open any WARN'd (403) links in a browser by hand.
3. Update "Last reviewed: Month YYYY" in the footer of `index.html` (and `es/index.html`).
4. Commit + push.

## Common problems
| Symptom | Likely cause | Fix |
|---|---|---|
| GitHub issue "Broken link(s)" appeared | An agency moved a page | Find the new landing page (not a PDF), update `index.html` + `tests/test_page.py`, run tests, push, close issue |
| Link check WARNs 403 for cdc.gov | CDC blocks scripts, not a real outage | Open the link in a browser; if it loads, ignore |
| Page not updating after push | Browser cache / Pages build lag | Hard refresh; check Actions tab "pages build and deployment" |
| "Not secure" warning | Certificate lapsed (auto-renews; very unlikely) | Repo Settings → Pages → untick/retick Enforce HTTPS |
| Domain doesn't resolve | DNS record removed | MyKinsta → DNS → planetdetroit.org: CNAME `heatguide` → `planet-detroit.github.io` |
| Tests fail after a copy edit | An edit removed a required link, section id, or added a date to body copy | Read the FAIL line — it says exactly what's missing |

## Dependencies
- GitHub Pages (hosting, free) · planetdetroit.org DNS (MyKinsta)
- Google Analytics 4 (optional; page works without it)
- External resource sites: apps.apple.com, play.google.com, cdc.gov, michigan.gov (MIOSHA), osha.gov, deepdives.planetdetroit.org
- Python 3 (tests only)
