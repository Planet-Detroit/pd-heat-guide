# Feature Spec: Heat Guide mobile site (heatguide.planetdetroit.org)

**Date**: 2026-08-17
**Status**: Draft — for Nina/Dustin/Isabelle review
**Source copy**: Isabelle's "Pulitzer resource card & mobile app copy" (Aug 14 draft)
**Hard deadline**: cards go to print Aug 21; site must be live and final by **Aug 26** (photo show Aug 28)

---

## 1. Purpose
A one-screen, phone-first "Guide to Working Safely in the Heat" that a worker reaches by scanning the QR code on the printed resource card. It repeats the card's life-saving basics (signs of heat illness, what to do, when to call 911) and then acts as a **hub of links** to the best existing tools — it does not try to be a full explainer. It must stay accurate for years with almost no upkeep, so it contains **no live data and no content that dates** (no dates, no seasonal language, no "this summer").

## 2. Users
- **Primary user**: Outdoor/indoor workers in Metro Detroit (many Spanish-speaking), often on a cheap phone, in bright sun, possibly with poor signal or while a coworker is sick. Some will be employers/supervisors.
- **How they'll access it**: QR code or typed short URL from the printed card; links from Planet Detroit heat stories and newsletter.
- **How often**: Usually once, in a hurry. Design for "find the answer in 10 seconds," not for browsing.
- **Secondary**: Isabelle/Dustin editing copy or adding a link (roughly once a year).

## 3. User Workflow
1. Worker scans QR → lands on `https://heatguide.planetdetroit.org/` in under 2 seconds on 4G.
2. Top of screen: Planet Detroit mark, title, and an **English / Español** switch (one tap).
3. First thing visible without scrolling: a red **"Heat stroke is an emergency — call 911"** block with the four call-911 signs and the "while you wait" steps.
4. Scrolling down: **Early warning signs** and **Take action right away** (the card copy, verbatim from Isabelle/NIOSH).
5. Next: **Tools** — big tappable buttons: OSHA-NIOSH Heat Safety Tool (App Store / Google Play), CDC heat illness explainer, MIOSHA heat page (sample prevention plan lives there), OSHA heat page.
6. Next: **Know your rights / report unsafe conditions** — MIOSHA complaint page + phone 800-866-4674, OSHA complaint page. (Recommended addition; Isabelle to approve wording.)
7. Next: **Planet Detroit's reporting** — one button to the Heat and Harm landing page (deepdives.planetdetroit.org/heat-and-harm/). Policy brief gets added there later, not here.
8. Footer: source credit (NIOSH), "Last reviewed: Month YYYY", link to planetdetroit.org, tiny "This guide is general information, not medical advice."
9. Tapping the language switch shows the same page in the other language, and the choice is remembered on that phone.

## 4. Requirements
1. **Static site, no build step, no JavaScript required to read it.** Plain HTML + CSS in this repo, served by GitHub Pages (already set up). One file per language: `index.html` (EN) and `es/index.html` (ES). A few lines of optional JS only for remembering the language choice.
2. **Phone-first**: readable at 320px wide, body text ≥ 17px, buttons ≥ 48px tall, high contrast (works in sunlight), no horizontal scrolling. Also fine on desktop (centered column, max ~600px).
3. **Loads fast on weak signal**: total page weight under 150 KB, no web fonts, no external CSS/JS/images (logo inlined as SVG or a small PNG in the repo).
4. **Emergency block first**: 911 content is visible before any scrolling on a typical phone; `tel:911` link so a tap dials.
5. **Content is Isabelle's copy, verbatim** (EN), plus her Spanish translation once delivered. Claude does not rewrite medical guidance. Copy lives in the HTML with clear `<!-- SECTION: … -->` comments so a non-developer (with Claude) can edit it.
6. **Evergreen content rules**: no dates in body copy (only "Last reviewed" in footer), no weather, no live data, no event references, no phone numbers except 911 and the MIOSHA/OSHA hotlines.
7. **Link hygiene**: link to stable **landing pages**, not deep PDFs or files with `?rev=` query strings (those break when agencies re-upload). Every external link opens in a new tab with `rel="noopener"`. Each link shows the site name in plain words ("michigan.gov") so people know where they're going.
8. **App links**: OSHA-NIOSH Heat Safety Tool linked directly to App Store and Google Play (one tap to install), with the CDC page as a fallback link.
9. **Bilingual parity**: EN and ES pages have the same sections in the same order; each links to the other at the top. `<html lang>` set correctly.
10. **Accessibility**: proper headings (`h1` → `h2`), one `h1`, alt text on the logo, color is never the only signal (the emergency block also has an icon/label).
11. **Search-friendly**: remove the `noindex` used on the holding page; add title/description; the site *should* be found by Googling "heat guide Detroit workers."
12. **Print-friendly**: a small print stylesheet so the page prints cleanly on one or two sheets (employers may pin it up).
13. **Short URL redirect** (outside this repo): `planetdetroit.org/heatguide` → `https://heatguide.planetdetroit.org/` set up in WordPress (Redirection plugin or Newspack redirect), because the card back currently says `planetdetroit.org/heatguide`. Both must work.
14. **Low-maintenance safety net**: a GitHub Action runs **monthly** and checks that every external link still returns 200 (with a browser-like User-Agent, since CDC/michigan.gov block bots); if any fails it opens a GitHub issue. Plus a **once-a-year "review the copy" reminder** (calendar/issue), which is when "Last reviewed" gets bumped.
15. **Analytics**: lightweight and optional — either none, or a single GA4 tag matching planetdetroit.org (decision for Nina). QR should carry `?utm_source=card&utm_medium=qr`.

## 5. Acceptance Criteria (these become the automated tests)
- [ ] When `index.html` is loaded, then it contains exactly one `h1`, the phrase "911", a `tel:911` link, and the emergency section appears in the HTML **before** the early-signs section.
- [ ] When `es/index.html` is loaded, then `<html lang="es">`, it has the same number of `h2` sections as the English page, and it links to `/`; the English page links to `/es/`.
- [ ] When the page is scanned for links, then all external `<a>` have `target="_blank" rel="noopener"`, and none point to a URL containing `.pdf` or `?rev=`.
- [ ] When the required resource links are checked, then the page contains each of: App Store URL, Google Play URL, CDC illnesses page, MIOSHA heat page, MIOSHA complaint page, OSHA heat-exposure page, Heat and Harm deep dive.
- [ ] When the page is scanned, then there are no `<script src="http`, `<link href="http`, web-font `@import`s, or `<img src="http` — everything is local.
- [ ] When total bytes of `index.html` + `styles.css` + local images are summed, then the total is under 150 KB.
- [ ] When the page is scanned, then no `<meta name="robots" content="noindex">` remains, and `<title>` + `<meta name="description">` exist in both languages.
- [ ] When the CSS is checked, then base font size ≥ 17px and `.btn` min-height ≥ 48px, and a `@media print` block exists.
- [ ] When the body text is scanned, then it contains no four-digit year and no month names except inside the footer "Last reviewed" line (evergreen check).
- [ ] When the monthly link-check workflow runs against a deliberately broken URL, then it fails and opens an issue (tested once by hand at setup).
- [ ] When `https://planetdetroit.org/heatguide` is requested, then it redirects (301) to `https://heatguide.planetdetroit.org/` (checked with curl after WP redirect is added).
- [ ] When the page renders at 320px and 390px wide in headless Chrome, then no element overflows horizontally (screenshot check).

## 6. Out of Scope (v1)
- No live heat index, weather, or alerts — the OSHA-NIOSH app does that; we link to it.
- No cooling-center map or list (dates quickly; belongs in cat-civic-data if ever).
- No sign-up form, comments, or accounts.
- No native app / app-store listing. ("Mobile app" = mobile website. Adding "Add to Home Screen" support later is cheap if wanted.)
- No CMS — copy edits are made in the HTML via Claude Code.
- Not the policy brief — that goes on the Heat and Harm landing page.
- Not a general public heat guide (kids/elders/outages) — worker-focused, per Isabelle's copy. Holding-page bullets get replaced.

## 7. Connects To
- GitHub Pages repo `Planet-Detroit/pd-heat-guide` (this repo, custom domain already configured).
- planetdetroit.org WordPress — for the `/heatguide` redirect and links from stories.
- deepdives.planetdetroit.org/heat-and-harm/ — PD's reporting hub.
- External: apps.apple.com, play.google.com, cdc.gov/niosh, michigan.gov/leo (MIOSHA), osha.gov.
- Printed resource card (Ro's design) — QR code target and short URL must match.

## 8. Known Risks
- **Card/URL mismatch (act now):** the card front says `http://heatguide.planetdetroit.org`, the back says `planetdetroit.org/heatguide`. Fix before print: use `heatguide.planetdetroit.org` on both, **and** add the WordPress redirect so the short form works anyway. QR should encode `https://heatguide.planetdetroit.org/?utm_source=card&utm_medium=qr`.
- **HTTPS timing:** GitHub is still issuing the certificate; until then `https://` fails on phones. Must be green before Aug 21 (expected within the hour; being monitored).
- **Government links move** (osha.gov/heat already redirects; MIOSHA deep pages 404). Mitigated by linking landing pages only + monthly automated link check.
- **If content is wrong**: it's medical guidance — copy is NIOSH-sourced and owned by Isabelle; Claude must not edit wording without her sign-off. Footer disclaimer.
- **If site goes down**: card still has the essentials printed on it; GitHub Pages uptime is excellent and there's nothing to break (no server, no database).
- **Spanish translation arrives late**: ship EN with the ES toggle hidden; add ES page when ready (no other change needed).
- **Security**: static HTML, no forms, no user data — minimal surface. Only third-party code would be the optional GA4 tag.

## 9. Success Metrics
- QR scans / page views with `utm_source=card` (if analytics enabled).
- Taps on app-store links and MIOSHA complaint link (outbound clicks).
- Zero broken links reported by the monthly check over the first year.
- Copy still accurate at the annual review with ≤ 1 hour of work.

---

## Research notes (link verification, 2026-08-17)
| Resource | URL to use | Status |
|---|---|---|
| Heat Safety Tool — iOS | https://apps.apple.com/us/app/osha-niosh-heat-safety-tool/id1239425102 | 200 ✅ |
| Heat Safety Tool — Android | https://play.google.com/store/apps/details?id=erg.com.nioshheatindex | 200 ✅ |
| Heat Safety Tool — CDC page (fallback) | https://www.cdc.gov/niosh/heat-stress/communication-resources/app.html | CDC blocks automated checks (403); page confirmed live via search — verify by hand in a browser |
| CDC heat illness types | https://www.cdc.gov/niosh/heat-stress/about/illnesses.html | same — verify by hand |
| MIOSHA heat page (has Sample Heat Illness Prevention Plan, fact sheets) | https://www.michigan.gov/leo/bureaus-agencies/miosha/topics/heat | 200 ✅ — link the page, not the plan PDF (`?rev=` URL) |
| MIOSHA file a complaint | https://www.michigan.gov/leo/bureaus-agencies/miosha/enforcement-and-appeals/how-to-file-a-complaint-with-miosha | 200 ✅ · phone 800-866-4674 · note: MIOSHA has no heat standard, but expects a Heat Illness Prevention Program |
| OSHA heat page | https://www.osha.gov/heat-exposure | 200 ✅ (`osha.gov/heat` redirects here) |
| OSHA heat illness first aid | https://www.osha.gov/heat-exposure/illness-first-aid | 200 ✅ |
| OSHA file a complaint | https://www.osha.gov/workers/file-complaint | 200 ✅ |
| PD Heat and Harm | https://deepdives.planetdetroit.org/heat-and-harm/ | 200 ✅ |

Dead/avoid: `michigan.gov/leo/bureaus-agencies/miosha/complaints` (404), `osha.gov/heat-exposure/heat-app` (404), any michigan.gov `/-/media/...?rev=` file link.

_After approval, hand this to Claude Code: "Read spec.md. Write automated tests for each acceptance criterion first, then implement."_
