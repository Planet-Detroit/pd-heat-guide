# pd-heat-guide

**Live at:** https://heatguide.planetdetroit.org/
**What it is:** "Guide to Working Safely in the Heat" — a one-page, phone-first hub for Metro Detroit workers, reached from the QR code on Planet Detroit's printed resource card. Emergency steps first, then early signs, then links to the best existing tools (OSHA-NIOSH app, CDC, MIOSHA, OSHA), how to report unsafe conditions, and Planet Detroit's Heat and Harm reporting.
**Spec:** `spec.md` (approved by Nina 2026-08-17). **Copy owner:** Isabelle. **Hosting:** GitHub Pages (custom domain + HTTPS already configured).

## Files
| File | Purpose |
|---|---|
| `index.html` | The English page. Copy is inside `<!-- SECTION: … -->` blocks so it's easy to find. |
| `es/index.html` | Spanish page — **not created yet**; add when Isabelle's translation is ready (see below). |
| `styles.css` | Styles following `/projects/design-system` (blue #2982C4, Georgia body, dark footer). |
| `assets/` | Planet Detroit logos (dark for white bg, white for footer). |
| `CNAME` | Custom-domain file for GitHub Pages. Do not rename. |
| `tests/test_page.py` | Automated checks from the spec's acceptance criteria. `python3 tests/test_page.py` |
| `tests/check_links.py` | Fetches every external link; run by hand or by the monthly Action. |
| `.github/workflows/link-check.yml` | Monthly link check; opens a GitHub issue if a link dies. |
| `MAINTENANCE.md` | How to tell it's working, common fixes, yearly review. |
| `STRATEGY.md` | Earlier thinking on phases (mostly superseded by spec.md). |

## Editing copy
1. Ask Claude Code: "In pd-heat-guide, change X to Y in the [section name] section."
2. Claude runs `python3 tests/test_page.py`, commits, pushes. GitHub Pages updates in ~1 minute.
3. If you change a URL, it also needs changing in `tests/test_page.py` (the test lists the required links on purpose, so a link can't quietly disappear).

## Adding the Spanish page
Create `es/index.html` with the same sections in the same order (`<html lang="es">`), add a language switch (`class="lang-switch"`) at the top of both pages linking `/` ↔ `/es/`. The tests already know how to check it — they're skipped until the file exists.

## Deploy
Push to `main` → live. Nothing else. There is no build step, server, or database.

## Analytics
GA4 property `G-5QQJ9SVV07` (same as civicactiontoolbox.org). Fires an event `resource_click` for every outbound/phone tap. QR code should point to `https://heatguide.planetdetroit.org/?utm_source=card&utm_medium=qr`.

## Still to do (outside this repo)
- WordPress redirect `planetdetroit.org/heatguide` → `https://heatguide.planetdetroit.org/` (card back uses the short form). Nina undecided on the Redirection plugin — decide before Aug 21 print date, or change the card back to the subdomain.
