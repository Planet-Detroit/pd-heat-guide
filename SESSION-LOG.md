# Session Log — pd-heat-guide

Plain-English record of what was built, decided, and left open. Newest at the bottom.

---

## 2026-08-17 — Holding page, domain, spec

**Asked for:** a holding page at heatguide.planetdetroit.org (mobile heat-info site, content to come) plus a strategy.

**Done**
- Created `/projects/pd-heat-guide` (pd- prefix per house rule) and public GitHub repo `Planet-Detroit/pd-heat-guide`, following the same static-site/GitHub Pages pattern as sponsors.planetdetroit.org.
- Built a "HeatGuide — coming soon" card page with tests (`tests/test_page.py`), `README`, `MAINTENANCE`, `STRATEGY`.
- Enabled GitHub Pages with custom domain. Nina added the CNAME record in **MyKinsta** (`heatguide` → `planet-detroit.github.io`). Site served over HTTP within minutes; HTTPS certificate stalled until I removed/re-added the domain, then issued in ~30s. **Enforce HTTPS turned on**; http→https redirect confirmed.
- QR target agreed: `https://heatguide.planetdetroit.org/?utm_source=card&utm_medium=qr`
- Received Isabelle's "Resource card & mobile app copy" draft. Verified every external link (found 3 dead deep links; CDC/michigan.gov block scripts with 403). Wrote `spec.md`: single static page, emergency-first, resource hub, EN/ES, evergreen rules, monthly link check.
- Flagged: card front says `heatguide.planetdetroit.org`, card back says `planetdetroit.org/heatguide` — mismatch.

**Decisions (Nina)**
- Yes to a "Report unsafe conditions" section. Yes to GA4. WordPress redirect for the short URL: undecided.
- Build using `/projects/design-system`.

## 2026-08-17 — Real page built from spec

- Replaced holding page with the full "Guide to Working Safely in the Heat": logo header → 🔴 911 emergency block (tap-to-dial) → signs/actions (Isabelle's copy verbatim) → Tools (App Store/Google Play, CDC, MIOSHA, OSHA) → Report unsafe conditions (MIOSHA online + 800-866-4674, OSHA) → Heat and Harm → dark footer with "Last reviewed," not-medical-advice line.
- Design system applied: blue #2982C4, Georgia 18/20px body, system-sans headings, #333 footer w/ white logo. One deliberate exception: emergency block uses #DD3333 red (design system reserves red for donate; safety convention wins).
- GA4 `G-5QQJ9SVV07` (shared PD property) with `resource_click` outbound events.
- Added `.github/workflows/link-check.yml` (monthly; opens an issue on dead links; 403 treated as "check by hand") + `tests/check_links.py`. Test-ran: green.
- 41 automated checks passing; no horizontal overflow at 320/390px; page weight ~33 KB.
- CLAUDE.md project row added → Production.

## 2026-08-19 — Spanish page

- Isabelle delivered the Spanish card translation. Built `/es/` mirroring `/` section-for-section, with an English · Español switch (choice remembered via localStorage; works without JS).
- **Needs Isabelle's review:** web-only Spanish (tools blurbs, button labels, "Denuncia condiciones inseguras," reporting, footer) was translated by Claude and is marked with an HTML comment in `es/index.html`. Added "(En inglés.)" where a linked resource is English-only.
- Tests extended for ES (lang attr, same section count, cross-links, balanced HTML).

## 2026-08-19 — Live NWS heat-alert banner

- Nina asked whether a live heat warning is possible on GitHub Pages → yes, client-side from api.weather.gov (free, no key, CORS open). Approved.
- Built `alerts.js`: queries zones MIZ076 Wayne / MIZ069 Oakland / MIZ070 Macomb; shows amber (Advisory/Watch) or red (Warning) strip above the header; most serious alert wins; expired ignored; 6s timeout; **fails silently** (no alert / API down / no JS → nothing shown). EN + ES wording.
- 15 Node unit tests (`tests/test_alerts.js`) + page checks; total 57 + 15 passing. Verified visually with mocked alerts in both languages.
- `spec.md` amended to record this as an approved exception to "no live data."

---

## Open items
| Item | Owner | Notes |
|---|---|---|
| `planetdetroit.org/heatguide` short URL (card back) currently 404s | Nina | Either add a WP redirect → `https://heatguide.planetdetroit.org/` or change card back to the subdomain before Aug 21 print |
| Review Claude-translated Spanish sections | Isabelle | Marked by `<!-- NOTE: … -->` in `es/index.html` |
| Confirm CDC links by hand in a browser | Isabelle/Dustin | CDC blocks automated checks |
| Yearly copy review each June; bump "Last reviewed" | Isabelle | Checklist in `MAINTENANCE.md` |

## Key facts
- Live: https://heatguide.planetdetroit.org/ · https://heatguide.planetdetroit.org/es/
- Repo: https://github.com/Planet-Detroit/pd-heat-guide (push to `main` = deploy, ~1 min)
- DNS: MyKinsta · Hosting: GitHub Pages · Analytics: GA4 G-5QQJ9SVV07
- Run tests: `python3 tests/test_page.py` (runs the Node tests too) · links: `python3 tests/check_links.py`
