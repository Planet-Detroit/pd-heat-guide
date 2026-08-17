# Maintenance — pd-heat-guide

## What this does
Serves https://heatguide.planetdetroit.org. Currently a single "coming soon" page pointing readers to the Planet Detroit newsletters page and the "Heat and Harm" deep dive.

## How to tell it's working
- Open the URL on a phone. You should see the white "HeatGuide" card on a dark/warm background, two blue buttons, no browser security warning.
- `curl -sI https://heatguide.planetdetroit.org | head -1` → `HTTP/2 200`.

## Common problems
| Symptom | Likely cause | Fix |
|---|---|---|
| "404 There isn't a GitHub Pages site here" | Pages not enabled or `CNAME` file missing | Repo Settings → Pages; confirm `CNAME` file contains exactly `heatguide.planetdetroit.org` |
| Domain doesn't resolve | DNS record missing/wrong | CNAME `heatguide` → `planet-detroit.github.io` |
| Certificate / "not secure" warning | HTTPS not yet issued, or Cloudflare proxy on | Wait up to 1 hr; in Cloudflare set record to DNS-only, then re-tick *Enforce HTTPS* |
| Change pushed but page unchanged | Browser cache / Pages build lag | Hard refresh; check repo Actions tab for the "pages build and deployment" run |
| Search engines showing the placeholder | `noindex` meta was left in / removed too early | Remove `<meta name="robots" content="noindex…">` at launch; tests will need updating then |

## Dependencies
- GitHub Pages (free) — hosting
- planetdetroit.org DNS
- Links out to planetdetroit.org/newsletters/ and deepdives.planetdetroit.org/heat-and-harm/ — if either URL moves, update `index.html` **and** `tests/test_page.py`.
