# Verification — 2026-10-08

The local website was checked in the Codex in-app browser. This file is outside the publishable directory.

- **Responsive layout:** both English and Chinese checked at 320, 390, 768, 1024, and 1440 CSS pixels. Document width matched the viewport in all ten checks. Mobile uses stacked project illustrations; larger screens use the sticky sequence.
- **Interactions:** English/Chinese search, Chinese keywords, Unicode-width normalization, category filters combined with search, singular/plural result text, empty results, and reset to all eighteen directory projects passed.
- **Navigation:** mobile open/close, Escape with focus restoration, section navigation, a visible keyboard skip link with a 3px outline, and section-preserving language switching passed.
- **Motion:** desktop scrolling selected the matching WhaOS illustration and story while the illustration stage stayed at its sticky position. Hero entrance, project scenes, and interests were visually reviewed.
- **First-view illustration animations:** piano keys, the basketball and shadow, video, chess, and the active project waveform were checked in the browser. Sequences ended automatically and did not restart on a return visit to the section within the same page. Chinese mobile testing confirmed the basketball waited until scrolling brought it into view, with no horizontal overflow at 390px. Inactive sticky scenes and hidden mobile artwork did not start alongside the visible desktop scene. A reduced-motion fixture kept the new illustrations static. These animations use the same shared assets in both languages.
- **Fallbacks:** separate temporary pages verified the same content without JavaScript, with IntersectionObserver unavailable, and with reduced motion simulated in CSS and JavaScript. The reduced-motion edition disabled hero animation and smooth scrolling and replaced the sticky sequence with static artwork. Phone fallback layouts also passed. No operating-system preferences were changed.
- **Console:** no warning/error messages observed during the checked website sessions.
- **Static checks:** `python3 scripts/verify.py`, `node --check public/assets/site.js`, and `git diff --check` passed. Static checks include twenty-four project links in each language, matching sections and destinations, local resources, labels, approved contact information, excluded biography/archive content, sharing-image dimensions, sitemap, and public-file boundaries.
- **Public sources:** all twenty-four repository destinations were confirmed in the live public GitHub catalogs. This does not assert that every linked application has a functioning live deployment.
- **Original preservation:** all thirteen supplied original files matched the SHA-256 hashes recorded before implementation, including the original images and stylesheet.
- **Preview boundary:** English, Chinese, and the sharing image returned HTTP 200. Requests for the original biography, the source notes, and the build script returned HTTP 404 from the public-directory preview server.

The site has not been publicly deployed. Browser checks used one browser engine and simulated phone/tablet sizes, not physical devices. Social-sharing metadata defaults to the public-profile domain `https://williamhu.tech`; live sharing-platform previews depend on future hosting at that address or a rebuilt metadata base URL.

For local preview, rebuild, test, and hosting instructions, see [README.md](README.md).

Saved previews: [desktop English](artifacts/desktop-preview.jpg), [mobile Chinese](artifacts/mobile-zh-preview.jpg), and [animated illustration section](artifacts/animation-preview.jpg) (a still frame).

## Error pages — 2026-10-08

- Added English and Chinese 403, 404, 500, and 503 pages. Static checks verify all eight generated files, landmarks, noindex metadata, self-contained resources, recovery links, language links, and project-site subpaths. Rebuilding retains the error pages.
- The custom local preview returned HTTP 404 for deeply nested English and Chinese missing URLs, including a request under `original/`. HEAD requests retained HTTP 404 with an empty body. Existing homepages and directly requested error files returned HTTP 200 as expected for static files.
- Browser checks used installed Chrome in headless mode. Both error-page languages fit 320, 390, 768, and 1440px viewports without horizontal overflow. All eight pages loaded with the expected headings and titles. Home, projects, and language links worked; the keyboard skip link had a visible 3px focus outline. Reduced motion disabled the illustration animation. English and Chinese recovery remained usable without JavaScript. No JavaScript exceptions or external resource requests occurred.
- Desktop English and mobile Chinese screenshots were visually reviewed: [404 desktop](artifacts/error-404-desktop.png), [404 mobile Chinese](artifacts/error-404-mobile-zh.png).
- GitHub Pages’ automatic custom 404 convention was checked against [GitHub’s documentation](https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-custom-404-page-for-your-github-pages-site). The 403/500/503 pages require a host configured to use them; the presence of static HTML files does not configure GitHub’s own infrastructure errors.
