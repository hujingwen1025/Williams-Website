"""Self-contained error pages: they also render at arbitrary missing URLs."""
from html import escape
from urllib.parse import urlsplit


ERRORS = {
    404: {
        "label": ("PAGE NOT FOUND", "找不到页面"),
        "title": ("A small detour.", "走岔了一小段路。"),
        "description": ("This page may have moved, or the link may have a typo. Let’s get you back to somewhere familiar.", "这个页面可能已经移动，也可能是链接中有个小小的拼写错误。我们一起回到熟悉的地方吧。"),
        "symbol": '<path d="M8 24h9m14 0h9M17 24l5-6m4 12 5-6"/><circle cx="24" cy="24" r="18" stroke-dasharray="2 5"/>',
    },
    403: {
        "label": ("ACCESS RESTRICTED", "访问受限"),
        "title": ("This door is closed.", "这扇门暂时关着。"),
        "description": ("This address isn’t available for public access. There’s still plenty to explore on my website.", "这个地址暂不对外开放。我的网站上还有许多其他内容，欢迎继续看看。"),
        "symbol": '<rect x="12" y="21" width="24" height="20" rx="5"/><path d="M17 21v-7a7 7 0 0 1 14 0v7m-7 8v4"/>',
    },
    500: {
        "label": ("SOMETHING WENT WRONG", "出了点小问题"),
        "title": ("A little out of tune.", "节奏有点乱了。"),
        "description": ("Something went wrong while loading this page. Please try again in a moment, or head back to the homepage.", "加载页面时出了点问题。请稍后再试，或者先回到首页看看。"),
        "symbol": '<path d="M24 6v9m0 18v9M6 24h9m18 0h9M11 11l6 6m14 14 6 6m0-26-6 6M17 31l-6 6"/><circle cx="24" cy="24" r="6"/>',
    },
    503: {
        "label": ("TEMPORARILY UNAVAILABLE", "暂时无法访问"),
        "title": ("A brief intermission.", "短暂休息一下。"),
        "description": ("This page is taking a short break. Please try again later. In the meantime, you can find my public work on GitHub.", "这个页面暂时休息一下，请稍后再试。你也可以先到 GitHub 看看我的公开项目。"),
        "symbol": '<rect x="14" y="12" width="6" height="24" rx="3"/><rect x="28" y="12" width="6" height="24" rx="3"/>',
    },
}

STYLE = """
:root{color-scheme:light;--paper:#f8f7f4;--ink:#222522;--muted:#626661;--blue:#2459e0;--line:#deded7;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC","Microsoft YaHei",sans-serif;color:var(--ink);background:var(--paper);font-synthesis:none}
*{box-sizing:border-box}body{margin:0;-webkit-font-smoothing:antialiased}a{color:inherit;text-decoration:none}a:focus-visible{outline:3px solid var(--blue);outline-offset:6px;border-radius:5px}::selection{background:#cbd9fc;color:#153571}
:root[lang=en] [data-error-language=zh],:root[lang=zh-Hans] [data-error-language=en]{display:none}
.shell{width:min(1184px,calc(100% - 64px));margin-inline:auto}.error-header{border-bottom:1px solid var(--line)}.error-nav{min-height:80px;display:flex;align-items:center;justify-content:space-between;gap:24px}.wordmark{display:flex;align-items:center;gap:15px;font-size:14px;font-weight:600}.wordmark b{font-size:32px;letter-spacing:-3px}.wordmark b span{color:var(--blue)}.language-link{font-size:12px;padding:14px 4px}.language-link span{color:var(--muted)}
.skip-link{position:fixed;top:12px;left:20px;z-index:10;padding:14px 20px;background:var(--ink);color:white;transform:translateY(-180%)}.skip-link:focus{transform:none}
.error-main{min-height:calc(100svh - 166px);display:grid;place-content:center;text-align:center;padding-block:60px 70px}.error-visual{position:relative;width:min(440px,100%);height:220px;margin:0 auto 28px;display:flex;align-items:center;justify-content:center;gap:9px;isolation:isolate}.error-visual::before{content:"";position:absolute;inset:8px -20px;background-image:radial-gradient(#c8cbc0 .8px,transparent .8px);background-size:19px 19px;mask-image:radial-gradient(ellipse,black,transparent 70%);-webkit-mask-image:radial-gradient(ellipse,black,transparent 70%);z-index:-1}.error-digit{font-size:154px;font-weight:550;letter-spacing:-13px;line-height:1;color:#263728}.error-orb{width:130px;height:155px;border-radius:50%;background:linear-gradient(135deg,#edf0e2,#ccd9b8);border:1px solid #bbcba5;box-shadow:inset 0 1px 3px #fff,0 15px 30px #54634518;display:grid;place-items:center;transform:rotate(12deg);margin-left:10px}.error-orb svg{width:59px;height:59px;stroke:#536c40;stroke-width:1.4;fill:none;stroke-linecap:round;stroke-linejoin:round;transform:rotate(-12deg)}.error-orbit{position:absolute;inset:38px 0;border:1px solid #b6c4a780;border-radius:50%;transform:rotate(-18deg);z-index:-1}.error-dot{position:absolute;right:9%;top:10%;width:10px;height:10px;border-radius:50%;background:var(--blue)}
.eyebrow{font:10px/1.8 ui-monospace,"SFMono-Regular",Consolas,monospace;letter-spacing:1.5px;color:var(--muted);margin:0 0 18px}h1{font-size:clamp(34px,5vw,58px);font-weight:550;line-height:1.16;letter-spacing:-2px;margin:0 0 22px}html[lang=zh-Hans] h1{letter-spacing:-1px;line-height:1.3}.error-description{font-size:16px;line-height:1.85;color:var(--muted);max-width:510px;margin:0 auto 30px}.error-actions{display:flex;justify-content:center;align-items:center;gap:20px;flex-wrap:wrap}.button{display:inline-flex;align-items:center;justify-content:center;gap:18px;background:var(--blue);color:white;padding:16px 24px;border-radius:99px;font-size:13px;font-weight:550;transition:background .2s}.button:hover{background:#1748c5}.text-link{padding:12px 0;border-bottom:1px solid transparent;font-size:13px;font-weight:550}.text-link:hover{border-color:currentColor}.error-contact{font-size:12px;color:var(--muted);margin:30px 0 0;line-height:1.8}.error-contact a{text-decoration:underline;text-underline-offset:4px;display:inline-block;padding-block:5px}.error-footer{border-top:1px solid var(--line);padding-block:24px;display:flex;justify-content:space-between;align-items:center;gap:20px;color:var(--muted);font-size:11px;line-height:1.8}.error-footer a{padding-block:6px}.error-footer p{margin:0}
@media(prefers-reduced-motion:no-preference){.error-orb{animation:error-orb-settle 2.8s ease-in-out .2s}.error-dot{animation:error-dot-drift 2.8s ease-in-out .2s}@keyframes error-orb-settle{0%,100%{transform:rotate(12deg) translateY(0)}30%{transform:rotate(4deg) translateY(-10px)}65%{transform:rotate(16deg) translateY(-4px)}}@keyframes error-dot-drift{50%{transform:translate(-12px,9px)}}}
@media(max-width:600px){.shell{width:calc(100% - 40px)}.error-nav{min-height:66px}.error-main{min-height:calc(100svh - 176px);padding-block:42px 52px}.error-visual{height:175px;max-width:320px;margin-bottom:22px;gap:5px}.error-digit{font-size:120px;letter-spacing:-10px}.error-orb{width:101px;height:123px;margin-left:8px}.error-orb svg{width:47px;height:47px}.error-orbit{inset:32px 0}.error-description{font-size:14px;max-width:350px}.error-footer{align-items:flex-start;font-size:10px}.error-footer p{max-width:210px}.error-actions{gap:18px}h1{letter-spacing:-1.4px}}
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

    title = f"{code} — {info['label'][int(zh)].title()} | William Hu"
    description = info["description"][int(zh)]
    visual = (f'<span class="error-digit">{code // 100}</span><span class="error-orb">'
              f'<svg viewBox="0 0 48 48">{info["symbol"]}</svg></span>'
              f'<span class="error-digit">{code % 10}</span>')
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
 data-title-en="{code} — {escape(info['label'][0].title(), quote=True)} | William Hu"
 data-title-zh="{code} — {info['label'][1]} | William Hu"
 data-description-en="{escape(info['description'][0], quote=True)}" data-description-zh="{escape(info['description'][1], quote=True)}">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, follow"><meta name="color-scheme" content="light"><meta name="theme-color" content="#f8f7f4">
<title>{title}</title><meta name="description" content="{escape(description, quote=True)}">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 40 40'%3E%3Crect width='40' height='40' rx='10' fill='%23263728'/%3E%3Ctext x='5' y='29' fill='%23f8f7f4' font-family='sans-serif' font-size='27' font-weight='700'%3EW%3C/text%3E%3C/svg%3E">
<link rel="alternate" hreflang="en" href="{escape(site_url.rstrip('/') + '/' + filename, quote=True)}">
<link rel="alternate" hreflang="zh-Hans" href="{escape(site_url.rstrip('/') + '/zh/' + filename, quote=True)}">
<style>{STYLE}</style></head><body>
<a class="skip-link" href="#main">{copy('Skip to content', '跳到正文')}</a>
<header class="error-header"><nav class="error-nav shell" aria-label="William Hu">
<a class="wordmark" href="{home}" data-error-language="en"><b>W<span>.</span></b>William Hu</a>
<a class="wordmark" href="{home}zh/" data-error-language="zh"><b>W<span>.</span></b>William Hu</a>
<a class="language-link" href="{zh_error}" lang="zh-Hans" hreflang="zh-Hans" data-error-language="en" aria-label="Read this page in Chinese"><span>EN /</span> 中</a>
<a class="language-link" href="{en_error}" lang="en" hreflang="en" data-error-language="zh" aria-label="用英文阅读此页">EN <span>/ 中</span></a>
</nav></header>
<main id="main" class="error-main shell"><div class="error-visual" aria-hidden="true"><div class="error-orbit"></div>{visual}<i class="error-dot"></i></div>
<p class="eyebrow">{code} / {copy(*info['label'])}</p><h1>{copy(*info['title'])}</h1><p class="error-description">{copy(*info['description'])}</p>
<div class="error-actions">
<a class="button" href="{home}" data-error-language="en">Back to home <span aria-hidden="true">↗</span></a>
<a class="button" href="{home}zh/" data-error-language="zh">回到首页 <span aria-hidden="true">↗</span></a>
<a class="text-link" href="{home}#work" data-error-language="en">Explore my work →</a>
<a class="text-link" href="{home}zh/#work" data-error-language="zh">看看我的项目 →</a></div>
<p class="error-contact">{copy('Need a hand?', '需要帮忙？')} <a href="mailto:jingwen.hu@exabyte.org.cn">{copy('Let me know', '给我写信')}</a></p></main>
<footer class="error-footer shell"><p>{copy('A little code. A little music. A lot of curiosity.', '一点代码，一点音乐，满满的好奇心。')}</p><a href="https://github.com/hujingwen1025">GitHub ↗</a></footer>
<script>{script}</script></body></html>'''


def write_error_pages(public, site_url):
    for code in ERRORS:
        for lang, prefix in (("en", ""), ("zh", "zh/")):
            (public / f"{prefix}{code}.html").write_text(page(code, lang, site_url), encoding="utf-8")
