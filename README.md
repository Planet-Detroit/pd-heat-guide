# pd-heat-guide

**Live at:** https://heatguide.planetdetroit.org (once DNS + GitHub Pages are set up — see below)
**What it is:** A mobile-first website with extreme-heat information for Metro Detroit. Right now it is a **holding page** ("coming soon"). Real content to follow.
**Hosting:** GitHub Pages, same pattern as `sponsors.planetdetroit.org` and `civicactiontoolbox.org`.

## Files
| File | Purpose |
|---|---|
| `index.html` | The page. Plain HTML, no build step. |
| `styles.css` | Mobile-first styles using Planet Detroit brand colors. |
| `CNAME` | Tells GitHub Pages to serve at `heatguide.planetdetroit.org`. Do not rename. |
| `tests/test_page.py` | Automated checks. Run `python3 tests/test_page.py`. |
| `MAINTENANCE.md` | How to tell if it's working + how to fix common problems. |

## One-time launch steps (Nina)
1. **DNS — AWS Route 53** (planetdetroit.org's hosted zone; `sponsors.` and `deepdives.` are set up the same way):
   Route 53 → Hosted zones → planetdetroit.org → *Create record* → Record name `heatguide`, Type **CNAME**, Value `planet-detroit.github.io`, TTL 300. Save.
2. **GitHub Pages** — already enabled (branch `main`, custom domain `heatguide.planetdetroit.org`). After DNS propagates (5–60 min) go to https://github.com/Planet-Detroit/pd-heat-guide/settings/pages and tick **Enforce HTTPS** once the DNS check is green.
3. Open https://heatguide.planetdetroit.org on your phone.

## Deploying changes
Edit → `python3 tests/test_page.py` → commit → `git push`. GitHub Pages republishes in ~1 minute.

## Strategy for the real site
See `STRATEGY.md`.
