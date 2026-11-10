# Verification: 2026-11-10

Balanced Hallmark Cobalt redesign. The English and Simplified Chinese sites introduce William personally before the work, retain all four interest areas, and feature Resona Lite, Cubers, CAICP Academy, and Dorm Pass Manager. The full catalog contains 28 distinct public projects.

## Checks completed

- `python3 scripts/verify.py`: passed. Covers the personal-first section order, flagship lineup, 28 distinct repository destinations, four interests, original project anchors, bilingual parity, approved contacts, editorial exclusions, local HTML/CSS/font/image dependencies, sharing image dimensions, metadata, sitemap, self-contained error pages, subpath recovery, and the explicit public-file allowlist.
- `node --check public/assets/site.js`, `node --check scripts/check_browser.mjs`, and `git diff --check`: passed.
- `scripts/check_browser.mjs`, with installed puppeteer-core and headless Chrome: passed. Both languages were checked at 320, 375, 768, 1280, 1440, and 1920 CSS pixels without horizontal overflow. Project images and local fonts loaded; desktop hero actions fit the first screen.
- Final targeted check: Chinese hero actions fit 1280 × 800 and 1440 × 900 after the typography adjustment; keyboard Tab exposed the skip link with a visible outline.
- Search: combined categories and text, Unicode-width normalization, two calendar entries, empty results, reset to 28 entries, and focus restoration passed.
- Navigation: mobile open/close, Escape restoring menu-button focus, section links, old project anchors opening the correct catalog disclosure, and language switching retaining the selected personal-interest anchor passed. External navigation links no longer enter the section-selector logic.
- Fallbacks: complete content and working native disclosures without JavaScript; content with IntersectionObserver unavailable; a static ASCII field under reduced motion. No browser runtime exceptions were recorded.
- Errors: nested English and Chinese missing URLs returned HTTP 404 with the correct language and noindex metadata. The six directly requested 403/500/503 files loaded, as expected for ordinary static URLs. Recovery and language links retain a configured hosting subpath.
- Visual review: desktop/full-page English and Chinese, mobile introduction, compact project grid, sharing cards, desktop English error page, and mobile Chinese error page. The original decorative artwork was replaced by the ASCII monogram, real project captures, typography, and ruled interest rows.

## Hallmark review

Used Hallmark 2.0.0 at upstream commit `407fa689f4a276f2fd389208d271d0fef08f5058`, with the requested Cobalt theme. The approved personal-first composition overrides the randomized Long Document / Index draw. Tokens and base styles came from the Cobalt scaffold. Tooling remained in a temporary directory.

Final rendered sweep: **0 FAIL, 0 unresolved REFLEX**. The original site recorded 248 Floor findings and 176 Reflex findings under Hallmark's rules; these are design-tool findings, not a claim that all were functional defects.

Preservation check: **37/37 links, 1/1 fields, 23/23 script hooks**. Five of the 38 original headings remain headings verbatim; the rest were reworded under the approved plan, retained as catalog names/toolkit text, or replaced by direct project titles. Project descriptions, supported capabilities, shared-work attribution, and substantive interest coverage are preserved. `.hallmark/copy-changes.json` records the heading treatments.

Five warning rows were reviewed:

- The short footer caption intentionally uses a 28-character measure; it is not running prose.
- Two button warnings identify the same Cobalt control recipes: one cobalt primary, neutral keycap secondary actions, and sunken category selections. This follows the theme's controls.
- Direct `file://` capture reports a failed font preload. HTTP captures and browser checks verified both local typefaces; delivered comparison images use the HTTP captures.
- The heading-preservation warning reflects the approved copy and semantic changes described above.

The catalog word-budget notes are expected for a retained 28-project personal archive. Native disclosures keep technical details optional. The user explicitly requested full project and interest coverage; no content was removed to satisfy a landing-page word budget.

Hero and finish reviews ran in-thread using Hallmark's review criteria. The greeting wrapping, hero spacing, and language-anchor findings were resolved. A section capture was retaken after correcting the temporary helper's smooth-scroll/lazy-image handling and excluding fixed navigation/skip-link overlays from that capture only.

## Evidence and practical limits

- [Before/after comparison](artifacts/cobalt/comparison.html)
- [Desktop introduction](artifacts/cobalt/after/index-1440x900.png)
- [Chinese mobile introduction](artifacts/cobalt/chinese-home-phone.png)
- [Selected project grid](artifacts/cobalt/sections/projects-home-desktop-part.png)
- [Desktop error page](artifacts/cobalt/errors/error-404-html-desktop.png)
- [Chinese mobile error page](artifacts/cobalt/errors/error-zh-404-html-phone.png)

Project-image provenance and public claims are documented in [CONTENT-SOURCES.md](CONTENT-SOURCES.md). Cubers is explicitly in development and its images contain synthetic test progress. Dorm Pass Manager's image is explicitly a public sign-in template preview, not an authenticated live application. A verified, non-sensitive application screen would be the most useful future replacement image.

Checks used headless Chrome with simulated viewport sizes, not physical devices or other engines. No production deployment, application-store approval, or live operation of external projects was asserted. The GitHub Pages workflow and hosting configuration remain unchanged; this work has not been published. Generated Hallmark capture caches were moved outside `public/` before the final allowlist check.
