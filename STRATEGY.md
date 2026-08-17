# Heat Guide — build strategy (draft 2026-08-17)

## Phase 0 — Holding page (done)
Static HTML on GitHub Pages at heatguide.planetdetroit.org. Zero cost, zero maintenance, instantly swappable.

## Phase 1 — Static mobile guide (recommended first real version)
Keep it a static site in this repo. Heat info is mostly evergreen: symptoms, who's at risk, cooling-center basics, power-outage steps, who to call. Structure as short **cards/sections with anchor navigation** (one long scrolling page or a handful of pages), big tap targets, offline-tolerant (no JS required to read it). Add a "last updated" stamp and Spanish translation (mirror `deepdives/heat-and-harm` es pattern). Editors update via markdown or plain HTML in this repo; Claude Code handles edits + tests.

Why static first: reliability under load during a heat emergency, no server to fall over, works on cheap phones and weak signal.

## Phase 2 — Live data (only if editorially needed)
- Current heat index / NWS alerts for Detroit (NWS API is free, no key).
- Cooling-center list from City of Detroit open data (needs a scraper — fits `cat-civic-data/scrapers/` pattern, and could feed the Civic Action Toolbox too).
- Air quality via existing pollution-near-me / AQI work.
Fetch client-side with a graceful fallback (if the API fails, static content still shows).

## Phase 3 — Distribution
- WordPress: embed or link from heat stories via the civic-action-block.
- Newsletter promo block (see `deepdives/heat-and-harm/wordpress-promo-block.html` for a template).
- Add to `pd-tools-dashboard`? Probably not — this is reader-facing, not editorial.

## Decisions to make with Dustin
- Single long page vs. multi-page?
- Bilingual from day one?
- Which live data (if any) is worth the maintenance burden?
- Should it be a PWA (installable, works offline)? Cheap to add later.
