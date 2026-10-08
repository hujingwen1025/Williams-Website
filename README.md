# William Hu — personal website

A bilingual portfolio in English and Simplified Chinese, built with native HTML, CSS, and JavaScript. Six featured projects, eighteen additional public repositories, Exabyte Technologies, and interests beyond code.

## Preview

From this project folder:

```sh
python3 scripts/preview.py
```

Open [English](http://127.0.0.1:4825/) or [简体中文](http://127.0.0.1:4825/zh/). If that port is busy, choose a different unused port. There are no packages to install or API keys to configure.

The preview serves only `public/` and returns the custom 404 page with an HTTP 404 status for missing URLs. Try `/missing/page` or `/zh/missing/page` to check each language. Use `python3 scripts/preview.py --port 4827` to choose another port. Python’s basic `http.server` also previews the site, but uses its own generic page for missing URLs.

## Edit and rebuild

- `scripts/build.py` contains the bilingual copy, project catalog, and HTML templates. Run `python3 scripts/build.py` after changing it; this rebuilds both pages, error pages, and the search-engine metadata.
- `scripts/error_pages.py` contains the bilingual 403, 404, 500, and 503 templates and their self-contained styles. Rebuild after editing it.
- `public/assets/style.css` contains the responsive design, original CSS illustrations, and reduced-motion layouts.
- `public/assets/site.js` enhances the static pages with project search, filters, mobile navigation, section-preserving language switching, scroll reveals, the desktop project sequence, and brief first-view illustration animations.
- `public/assets/` also contains a favicon and two original 1200 × 630 sharing images, one per language. The sharing images are ready-to-use assets and do not need a build step.
- [CONTENT-SOURCES.md](CONTENT-SOURCES.md) records sources and editorial boundaries. Update it when adding facts or projects.

All biography and project text is in the generated HTML. Without JavaScript, readers still get both complete editions, navigation, repository links, and the contact email. Search and menu controls appear only after their handlers are installed. Native scrolling is preserved; reduced motion replaces the desktop sticky sequence with ordinary layouts.

Illustrations perform once per page visit when at least a quarter of the artwork enters view: piano keys play, the basketball bounces, the record spins, and project artwork responds to its theme. Each performance settles within four seconds. Hidden desktop/mobile variants and inactive sticky scenes wait until visible. Reduced-motion readers get static illustrations.

## Verify

```sh
python3 scripts/verify.py
node --check public/assets/site.js
```

The automated checks cover static content and language parity, links/assets, privacy boundaries, metadata, the publishable file allowlist, and JavaScript syntax. Real-browser checks cover search/filter behavior, navigation, focus, scroll scenes, and responsive layouts.

For reproducible browser fallback checks, run `python3 scripts/verify.py --fixtures /tmp/william-browser-checks` and serve that temporary directory on another local port. It creates a JavaScript-free edition, an edition without IntersectionObserver, and an edition simulating the reduced-motion preference in both CSS and JavaScript. These fixtures stay outside `public/` and do not alter browser or system settings.

## Static hosting

Publish **only the contents of `public/`**, which is the complete website. Serve `index.html` for directory URLs, including `/zh/`. All runtime assets are local; neither GitHub API calls nor a server application is required.

Canonical URLs, language alternates, sharing images, and the sitemap currently use **https://williamhu.tech**, the website listed on William’s public GitHub profile. If publishing at another address (including a repository subpath), rebuild first:

```sh
python3 scripts/build.py --site-url https://example.com/portfolio
```

The argument sets metadata only. It does not publish files, register a domain, or change DNS. Sharing cards become fetchable by social platforms after the images are available at that public address.

## Error pages

`public/404.html` is GitHub Pages’ custom missing-page entry point. It detects missing paths under `/zh/` and displays Chinese copy; `/zh/404.html` is also available directly. Each error page has native language links, home and project links, and the approved email contact. Styles and the small language enhancement are inline, so arbitrary nested missing URLs cannot break the design. Both editions remain readable without JavaScript; the explicit Chinese edition works without JavaScript too. Motion is brief and respects reduced-motion preferences. Error pages use `noindex` and are excluded from the sitemap.

Matching `403.html`, `500.html`, and `503.html` files, with Chinese editions under `zh/`, are ready for hosts that support custom forbidden, server-error, and unavailable responses. GitHub Pages automatically routes missing URLs to `404.html`; adding the other files does not configure GitHub’s own infrastructure errors. On another host, map each HTTP status to its corresponding file and preserve that response status. Directly visiting a numbered HTML file returns an ordinary successful static-file response.

For a repository site hosted under a subpath, rebuild with the full URL (for example `python3 scripts/build.py --site-url https://hujingwen1025.github.io/William-s-Website`). This also sets the error pages’ home and language links to the correct subpath. For a custom domain, use that domain instead.

`original/` is preserved as supplied. **Do not deploy the repository root:** the original site contains older personal details deliberately excluded from the new site. The source documents, checks, and original files remain outside `public/`.
