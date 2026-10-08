# William Hu — personal website

A bilingual portfolio in English and Simplified Chinese, built with native HTML, CSS, and JavaScript. Six featured projects, eighteen additional public repositories, Exabyte Technologies, and interests beyond code.

## Preview

From this project folder:

```sh
python3 -m http.server 4825 --bind 127.0.0.1 --directory public
```

Open [English](http://127.0.0.1:4825/) or [简体中文](http://127.0.0.1:4825/zh/). If that port is busy, choose a different unused port. There are no packages to install or API keys to configure.

## Edit and rebuild

- `scripts/build.py` contains the bilingual copy, project catalog, and HTML templates. Run `python3 scripts/build.py` after changing it; this rebuilds both pages and the search-engine metadata.
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

`original/` is preserved as supplied. **Do not deploy the repository root:** the original site contains older personal details deliberately excluded from the new site. The source documents, checks, and original files remain outside `public/`.
