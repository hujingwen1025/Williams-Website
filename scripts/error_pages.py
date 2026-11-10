"""Self-contained error pages: they also render at arbitrary missing URLs."""
from html import escape
from urllib.parse import urlsplit


ERRORS = {
    404: {
        "label": ("Page not found", "找不到页面"),
        "title": ("A small detour.", "走岔了一小段路。"),
        "description": ("This page may have moved, or the link may have a typo. Let’s get you back to somewhere familiar.", "这个页面可能已经移动，也可能是链接中有个小小的拼写错误。我们一起回到熟悉的地方吧。"),
        "symbol": '<path d="M8 24h9m14 0h9M17 24l5-6m4 12 5-6"/><circle cx="24" cy="24" r="18" stroke-dasharray="2 5"/>',
    },
    403: {
        "label": ("Access restricted", "访问受限"),
        "title": ("This door is closed.", "这扇门暂时关着。"),
        "description": ("This address isn’t available for public access. There’s still plenty to explore on my website.", "这个地址暂不对外开放。我的网站上还有许多其他内容，欢迎继续看看。"),
        "symbol": '<rect x="12" y="21" width="24" height="20" rx="5"/><path d="M17 21v-7a7 7 0 0 1 14 0v7m-7 8v4"/>',
    },
    500: {
        "label": ("Something went wrong", "出了点小问题"),
        "title": ("A little out of tune.", "节奏有点乱了。"),
        "description": ("Something went wrong while loading this page. Please try again in a moment, or head back to the homepage.", "加载页面时出了点问题。请稍后再试，或者先回到首页看看。"),
        "symbol": '<path d="M24 6v9m0 18v9M6 24h9m18 0h9M11 11l6 6m14 14 6 6m0-26-6 6M17 31l-6 6"/><circle cx="24" cy="24" r="6"/>',
    },
    503: {
        "label": ("Temporarily unavailable", "暂时无法访问"),
        "title": ("A brief intermission.", "短暂休息一下。"),
        "description": ("This page is taking a short break. Please try again later. In the meantime, you can find my public work on GitHub.", "这个页面暂时休息一下，请稍后再试。你也可以先到 GitHub 看看我的公开项目。"),
        "symbol": '<rect x="14" y="12" width="6" height="24" rx="3"/><rect x="28" y="12" width="6" height="24" rx="3"/>',
    },
}

STYLE = """
/* Hallmark · theme: Cobalt (by request) · redesign: full · scope: error pages · v2.0.0 */
:root { color-scheme: light; --paper: oklch(98.6% 0.005 250); --paper-2: oklch(96.2% 0.008 252); --ink: oklch(21% 0.028 262); --muted: oklch(47% 0.018 258); --blue: oklch(52% 0.19 258); --blue-edge: oklch(39% 0.16 260); --line: oklch(83% 0.012 252); --font-display: "Familjen Grotesk", "PingFang SC", "Microsoft YaHei", system-ui, sans-serif; --font-body: "IBM Plex Sans", "PingFang SC", "Microsoft YaHei", system-ui, sans-serif; font-family: var(--font-body); color: var(--ink); background: var(--paper); font-synthesis: none; }
@font-face { font-family: "Familjen Grotesk"; src: url("FONT_BASEfamiljen-grotesk-1.ttf") format("truetype"); font-weight: 600; font-display: swap; }
@font-face { font-family: "IBM Plex Sans"; src: url("FONT_BASEibm-plex-sans-0.ttf") format("truetype"); font-weight: 400; font-display: swap; }
* { box-sizing: border-box; }
html, body { overflow-x: clip; }
body { margin: 0; line-height: 1.6; -webkit-font-smoothing: antialiased; }
a { color: inherit; text-decoration: none; }
a:hover { text-decoration: underline; text-decoration-color: var(--blue); text-underline-offset: 0.25em; }
a:active { color: var(--blue); }
a:focus-visible { outline: 2px solid var(--blue); outline-offset: 5px; }
::selection { background: var(--paper-2); color: var(--blue); }
:root[lang=en] [data-error-language=zh], :root[lang=zh-Hans] [data-error-language=en] { display: none; }
.shell { width: min(1312px, calc(100% - 64px)); margin-inline: auto; }
.error-header { border-bottom: 1px solid var(--line); }
.error-nav { min-height: 80px; display: flex; align-items: center; justify-content: space-between; gap: 24px; }
.wordmark { display: flex; align-items: center; gap: 16px; font-family: var(--font-display); font-size: 16px; font-weight: 600; }
.wordmark b { font-size: 32px; letter-spacing: -0.08em; color: var(--blue); }
.language-link { font-size: 16px; padding: 12px 4px; }
.language-link span { color: var(--muted); }
.skip-link { position: fixed; top: 16px; left: 16px; z-index: 10; padding: 12px 24px; background: var(--ink); color: var(--paper); transform: translateY(-200%); }
.skip-link:focus-visible { transform: none; }
.error-main { min-height: calc(100svh - 180px); display: grid; align-content: center; justify-items: start; padding-block: 64px; }
.error-code { font-family: var(--font-display); font-size: clamp(112px, 17vw, 200px); font-weight: 600; line-height: 1; letter-spacing: -0.05em; font-variant-numeric: tabular-nums; color: var(--blue); margin-bottom: 32px; }
h1 { font-family: var(--font-display); font-size: clamp(32px, 4vw, 56px); font-weight: 600; line-height: 1.12; letter-spacing: -0.028em; margin: 0 0 24px; overflow-wrap: break-word; min-width: 0; text-wrap: balance; }
.error-description { font-size: 16px; color: var(--muted); max-width: 55ch; margin: 0 0 32px; text-wrap: pretty; }
.error-actions { display: flex; align-items: center; gap: 24px; flex-wrap: wrap; }
.button { display: inline-flex; align-items: center; justify-content: center; min-height: 48px; background: var(--blue); color: var(--paper); padding: 12px 24px; border: 1px solid var(--blue-edge); border-radius: 6px; font-family: var(--font-display); font-size: 16px; font-weight: 600; box-shadow: 0 3px 0 var(--blue-edge); transition: transform 120ms ease-out; }
.button:hover { transform: translateY(-1px); text-decoration: none; }
.button:active { transform: translateY(3px); box-shadow: none; color: var(--paper); }
.text-link { padding-block: 12px; font-size: 16px; }
.error-contact { font-size: 16px; color: var(--muted); margin: 32px 0 0; }
.error-contact a { text-decoration: underline; text-underline-offset: 4px; display: inline-block; padding-block: 4px; }
.error-footer { border-top: 1px solid var(--line); padding-block: 24px; display: flex; justify-content: space-between; gap: 24px; color: var(--muted); font-size: 14px; }
.error-footer p { margin: 0; }
@supports (corner-shape: bevel) { .button { border-radius: 16px 4px 16px 4px; corner-shape: bevel round bevel round; } }
@media(max-width:600px) { .shell { width: calc(100% - 32px); } .error-nav { min-height: 72px; } .error-main { padding-block: 40px; } .error-code { margin-bottom: 24px; } .error-footer p { max-width: 26ch; } }
@media(prefers-reduced-motion:reduce) { *, *::before, *::after { animation: none !important; transition: none !important; } .button:hover, .button:active { transform: none; } }
"""


def page(code, lang, site_url):
    info = ERRORS[code]
    zh = lang == "zh"
    home = urlsplit(site_url).path.rstrip("/") + "/"
    filename = f"{code}.html"
    en_error, zh_error = home + filename, home + "zh/" + filename

    def copy(en, cn):
        return (f'<span lang="en" data-error-language="en">{en}</span>'
                f'<span lang="zh-Hans" data-error-language="zh">{cn}</span>')

    title = f"{code} | {info['label'][int(zh)].title()} | William Hu"
    description = info["description"][int(zh)]
    # Error pages are inline and independent of site.js, including deep 404 URLs.
    script = """(() => {
      const root = document.documentElement;
      if (location.pathname.startsWith(root.dataset.home + 'zh/')) root.lang = 'zh-Hans';
      const chinese = root.lang === 'zh-Hans';
      document.title = root.dataset[chinese ? 'titleZh' : 'titleEn'];
      document.querySelector('meta[name="description"]').content = root.dataset[chinese ? 'descriptionZh' : 'descriptionEn'];
    })();"""
    return f'''<!doctype html>
<html lang="{'zh-Hans' if zh else 'en'}" data-home="{escape(home, quote=True)}"
 data-title-en="{code} | {escape(info['label'][0].title(), quote=True)} | William Hu"
 data-title-zh="{code} | {info['label'][1]} | William Hu"
 data-description-en="{escape(info['description'][0], quote=True)}" data-description-zh="{escape(info['description'][1], quote=True)}">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, follow"><meta name="color-scheme" content="light"><meta name="theme-color" content="#f8fafc">
<title>{title}</title><meta name="description" content="{escape(description, quote=True)}">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 40 40'%3E%3Crect width='40' height='40' rx='10' fill='%230050c8'/%3E%3Ctext x='5' y='29' fill='%23f8fafc' font-family='sans-serif' font-size='27' font-weight='700'%3EW%3C/text%3E%3C/svg%3E">
<link rel="alternate" hreflang="en" href="{escape(site_url.rstrip('/') + '/' + filename, quote=True)}">
<link rel="alternate" hreflang="zh-Hans" href="{escape(site_url.rstrip('/') + '/zh/' + filename, quote=True)}">
<style>{STYLE.replace("FONT_BASE", home + "assets/fonts/")}</style></head><body>
<a class="skip-link" href="#main">{copy('Skip to content', '跳到正文')}</a>
<header class="error-header"><nav class="error-nav shell" aria-label="William Hu">
<a class="wordmark" href="{home}" data-error-language="en"><b>W<span>.</span></b>William Hu</a>
<a class="wordmark" href="{home}zh/" data-error-language="zh"><b>W<span>.</span></b>William Hu</a>
<a class="language-link" href="{zh_error}" lang="zh-Hans" hreflang="zh-Hans" data-error-language="en" aria-label="Read this page in Chinese"><span>EN /</span> 中</a>
<a class="language-link" href="{en_error}" lang="en" hreflang="en" data-error-language="zh" aria-label="用英文阅读此页">EN <span>/ 中</span></a>
</nav></header>
<main id="main" class="error-main shell"><div class="error-code" aria-hidden="true">{code}</div><h1>{copy(*info['title'])}</h1><p class="error-description">{copy(*info['description'])}</p>
<div class="error-actions">
<a class="button" href="{home}" data-error-language="en">Back to home</a>
<a class="button" href="{home}zh/" data-error-language="zh">回到首页</a>
<a class="text-link" href="{home}#work" data-error-language="en">Explore my work</a>
<a class="text-link" href="{home}zh/#work" data-error-language="zh">看看我的项目</a></div>
<p class="error-contact">{copy('Need a hand?', '需要帮忙？')} <a href="mailto:jingwen.hu@exabyte.org.cn">{copy('Let me know', '给我写信')}</a></p></main>
<footer class="error-footer shell"><p>{copy('A little code. A little music. A lot of curiosity.', '一点代码，一点音乐，满满的好奇心。')}</p><a href="https://github.com/hujingwen1025">GitHub</a></footer>
<script>{script}</script></body></html>'''


def write_error_pages(public, site_url):
    for code in ERRORS:
        for lang, prefix in (("en", ""), ("zh", "zh/")):
            (public / f"{prefix}{code}.html").write_text(page(code, lang, site_url), encoding="utf-8")
