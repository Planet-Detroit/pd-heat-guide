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
1. **DNS** (wherever planetdetroit.org DNS lives — likely Cloudflare/GoDaddy):
   add a `CNAME` record → name `heatguide`, value `planet-detroit.github.io`, TTL auto. If Cloudflare, set proxy to **DNS only** (grey cloud) until the certificate is issued.
2. **GitHub:** repo `Planet-Detroit/pd-heat-guide` → Settings → Pages → Source: *Deploy from branch* `main` / root. Custom domain: `heatguide.planetdetroit.org`. Tick *Enforce HTTPS* once the check turns green (can take up to an hour).
3. Open https://heatguide.planetdetroit.org on your phone.

## Deploying changes
Edit → `python3 tests/test_page.py` → commit → `git push`. GitHub Pages republishes in ~1 minute.

## Strategy for the real site
See `STRATEGY.md`.
