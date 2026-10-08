#!/usr/bin/env python3
"""Verify the publishable site. Optionally create isolated browser-check fixtures."""
import argparse
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
import re
import shutil
import struct
import xml.etree.ElementTree as ET
from error_pages import ERRORS, page as error_page

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"


class Document(HTMLParser):
    def __init__(self, source):
        super().__init__(convert_charrefs=True)
        self.nodes, self.text = [], []
        self.feed(source)

    def handle_starttag(self, tag, attrs):
        self.nodes.append((tag, dict(attrs)))

    def handle_data(self, text):
        self.text.append(text)

    def attrs(self, tag):
        return [attrs for t, attrs in self.nodes if t == tag]

    def classified(self, name):
        return [attrs for _, attrs in self.nodes if name in attrs.get("class", "").split()]


def check(condition, message):
    if not condition:
        raise AssertionError(message)


def verify():
    editions = []
    for relative, lang in [("index.html", "en"), ("zh/index.html", "zh-Hans")]:
        file = PUBLIC / relative
        source = file.read_text(encoding="utf-8")
        doc = Document(source)
        text = " ".join(doc.text)
        ids = [a["id"] for _, a in doc.nodes if "id" in a]
        check(len(ids) == len(set(ids)), f"Duplicate IDs: {relative}")
        check(doc.attrs("html")[0]["lang"] == lang, "Wrong page language")
        check(len(doc.attrs("h1")) == 1, "Expected one primary heading")
        check(len(doc.attrs("main")) == 1, "Expected one main landmark")
        check(len(doc.classified("feature-copy")) == 6, "Incomplete featured projects")
        check(len(doc.classified("repo-card")) == 18, "Incomplete project directory")
        check(len(doc.classified("interest-card")) == 4, "Incomplete interests")
        for required in ["about", "work", "exabyte", "beyond", "explore", "connect"]:
            check(required in ids, f"Missing section: {required}")
        # The substantive text is present in HTML, without executing any JavaScript.
        for name in ["Jingwen Hu", "胡竞文", "Resona", "WhaOS", "Rhythm Cook", "Sonora", "CAICP Academy", "Dorm Pass Manager", "Neuorise", "Python", "AppleScript", "UNO"]:
            check(name in text, f"Missing static content: {name}")
        for banned in [r"\bbirthday\b", r"\bage:\s*\d", r"\bBeijing\b", r"\bKeystone\b", r"Oct(?:ober)?\s*25", r"年龄", r"生日", r"北京", r"鼎石", r"KACO", r"Fisherman Fishes", r"Slay Apple"]:
            check(not re.search(banned, text, re.I), f"Excluded biography/archive content: {banned}")
        check("jingwen.hu@exabyte.org.cn" in text, "Missing approved business email")
        for _, a in doc.nodes:
            for key in ("href", "src"):
                value = a.get(key)
                if not value:
                    continue
                url = urlsplit(value)
                if url.scheme:
                    check(url.scheme in ("https", "mailto"), f"Unexpected URL: {value}")
                    if url.scheme == "mailto":
                        check(value == "mailto:jingwen.hu@exabyte.org.cn", "Unapproved email link")
                    continue
                if value.startswith("#"):
                    check(unquote(url.fragment) in ids, f"Broken section link: {value}")
                    continue
                path = (file.parent / unquote(url.path)).resolve()
                check(PUBLIC.resolve() in (path, *path.parents), f"Link escapes public/: {value}")
                check(path.exists(), f"Missing local resource: {value}")
                if path.is_dir():
                    check((path / "index.html").exists(), f"Missing directory index: {value}")
            if a.get("target") == "_blank":
                check("noopener" in a.get("rel", ""), "Unsafe external target")
            if "aria-labelledby" in a:
                check(all(label in ids for label in a["aria-labelledby"].split()), "Broken accessible label")
        for script in doc.attrs("script"):
            check(not urlsplit(script.get("src", "")).scheme, "Remote runtime script")
        for stylesheet in doc.attrs("link"):
            if stylesheet.get("rel") == "stylesheet":
                check(not urlsplit(stylesheet["href"]).scheme, "Remote stylesheet/font")
        metadata = {a.get("property", a.get("name")): a.get("content") for a in doc.attrs("meta")}
        for key in ["description", "og:title", "og:description", "og:image", "og:image:alt", "og:url", "twitter:card"]:
            check(bool(metadata.get(key)), f"Missing metadata: {key}")
        check(metadata["og:image"].startswith("https://"), "Sharing image needs a public absolute URL")
        check({a.get("hreflang") for a in doc.attrs("link") if a.get("rel") == "alternate"} == {"en", "zh-Hans", "x-default"}, "Missing language alternates")
        controls = doc.classified("directory-controls")[0]
        check("hidden" in controls, "Inactive no-JS search controls should not be shown")
        check("hidden" in doc.classified("menu-toggle")[0], "Inactive no-JS menu button should not be shown")
        repo_links = {a["href"] for a in doc.attrs("a") if a.get("href", "").startswith("https://github.com/") and len(urlsplit(a["href"]).path.strip("/").split("/")) == 2}
        check(len(repo_links) == 24, "Expected twenty-four distinct public projects")
        editions.append((set(ids), repo_links))
        print(f"PASS {relative}: static biography, 24 projects, labels, links, metadata, privacy")
    check(editions[0] == editions[1], "Languages differ in sections or repository destinations")
    ET.parse(PUBLIC / "sitemap.xml")
    ET.parse(PUBLIC / "assets/favicon.svg")
    for name in ("social.png", "social-zh.png"):
        data = (PUBLIC / "assets" / name).read_bytes()
        check(data[:8] == b"\x89PNG\r\n\x1a\n", "Invalid social PNG")
        check(struct.unpack(">II", data[16:24]) == (1200, 630), "Incorrect social image dimensions")
    allowed = {"index.html", "zh/index.html", "robots.txt", "sitemap.xml", "assets/style.css", "assets/site.js", "assets/favicon.svg", "assets/social.png", "assets/social-zh.png"}
    site_url = next(a['href'] for a in Document((PUBLIC / 'index.html').read_text()).attrs('link') if a.get('rel') == 'canonical').rstrip('/')
    base = urlsplit(site_url).path.rstrip('/') + '/'
    sitemap = (PUBLIC / 'sitemap.xml').read_text()
    for code in ERRORS:
        for lang, prefix in [('en', ''), ('zh', 'zh/')]:
            relative = f'{prefix}{code}.html'
            allowed.add(relative)
            source = (PUBLIC / relative).read_text()
            doc = Document(source)
            check(source == error_page(code, lang, site_url), f'Stale error page: {relative}')
            check(len(doc.attrs('h1')) == len(doc.attrs('main')) == 1, f'Error page landmarks: {relative}')
            check(doc.attrs('html')[0]['lang'] == ('zh-Hans' if lang == 'zh' else 'en'), f'Error language: {relative}')
            check(any(a.get('name') == 'robots' and 'noindex' in a.get('content', '') for a in doc.attrs('meta')), f'Error page must not be indexed: {relative}')
            check(not any(a.get('src') for a in doc.attrs('script')), f'Error page needs an external script: {relative}')
            check(not any(a.get('rel') == 'stylesheet' for a in doc.attrs('link')), f'Error page needs an external stylesheet: {relative}')
            for a in doc.attrs('a'):
                href = a['href']
                if href.startswith('#') or urlsplit(href).scheme:
                    continue
                check(href.startswith(base), f'Error link loses site base: {href}')
                local = PUBLIC / urlsplit(href).path[len(base):]
                check(local.exists(), f'Broken error recovery/language link: {href}')
            check(f'/{code}.html' not in sitemap, 'Error pages must not appear in sitemap')
    # Project Pages subpaths must survive arbitrary nested missing URLs.
    sample = Document(error_page(404, 'en', 'https://example.com/portfolio'))
    check(sample.attrs('html')[0]['data-home'] == '/portfolio/', 'Missing project-site base')
    check(all(a['href'].startswith(('/portfolio/', '#', 'https:', 'mailto:')) for a in sample.attrs('a')), 'Subpath recovery links break')
    print('PASS 8 bilingual, self-contained error pages, recovery links, noindex, project-site subpaths')
    # Finder may recreate its metadata while a folder is open; Git ignores it.
    actual = {p.relative_to(PUBLIC).as_posix() for p in PUBLIC.rglob("*") if p.is_file() and p.name != ".DS_Store"}
    check(actual == allowed, f"Unexpected/missing publishable files: {actual ^ allowed}")
    check(not any(p.is_symlink() for p in PUBLIC.rglob("*")), "Publishable directory must not link to private/source files")
    css = (PUBLIC / "assets/style.css").read_text()
    check("prefers-reduced-motion:reduce" in css and "focus-visible" in css, "Missing accessibility styles")
    js = (PUBLIC / "assets/site.js").read_text()
    check(not re.search(r"\b(fetch|XMLHttpRequest|WebSocket|localStorage|sessionStorage)\b", js), "Unexpected network or persistence API")
    print("PASS language parity, sitemap, sharing images, public-file allowlist, local runtime")


def fixtures(destination):
    """Prepare same-page fixtures; never alter the production site or browser settings."""
    destination.mkdir(parents=True, exist_ok=True)
    check(destination.resolve() != PUBLIC.resolve(), "Fixtures must be outside public/")
    shutil.copytree(PUBLIC / "assets", destination / "assets", dirs_exist_ok=True)
    source = (PUBLIC / "index.html").read_text()
    no_js = re.sub(r'<script\b[^>]*>.*?</script>', '', source, flags=re.S)
    (destination / "no-js.html").write_text(no_js)
    missing_observer = source.replace('<script src=', '<script>delete window.IntersectionObserver;</script><script src=', 1)
    (destination / "missing-observer.html").write_text(missing_observer)
    # Simulate the preference in both browser CSS and JS, without altering OS settings.
    css = (PUBLIC / "assets/style.css").read_text().replace('(prefers-reduced-motion:reduce)', '(min-width:0px)').replace('(prefers-reduced-motion:no-preference)', '(max-width:0px)')
    (destination / "assets/reduced.css").write_text(css)
    prelude = "<script>const nativeMatchMedia=window.matchMedia.bind(window);window.matchMedia=q=>q==='(prefers-reduced-motion: reduce)'?{matches:true,addEventListener(){}}:nativeMatchMedia(q);</script>"
    reduced = source.replace('assets/style.css', 'assets/reduced.css').replace('<script src=', prelude + '<script src=', 1)
    (destination / "reduced-motion.html").write_text(reduced)
    print(f"Browser fixtures created outside the site: {destination}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fixtures", type=Path, help="Optional temporary directory for browser-check fixtures")
    args = parser.parse_args()
    verify()
    if args.fixtures:
        fixtures(args.fixtures)
