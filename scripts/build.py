#!/usr/bin/env python3
"""Build both readable, static language editions. Python standard library only."""
from pathlib import Path
from html import escape
from urllib.parse import urlsplit
import argparse

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
SITE_URL = "https://williamhu.tech"


def L(en, zh):
    return {"en": en, "zh": zh}


def icon(name, cls=""):
    paths = {
        "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
        "external": '<path d="M7 17 17 7M7 7h10v10"/>',
        "code": '<path d="m8 7-5 5 5 5m8-10 5 5-5 5m-3-13-2 16"/>',
        "music": '<path d="M9 18V5l11-2v13M9 8l11-2"/><ellipse cx="6" cy="18" rx="3" ry="2"/><ellipse cx="17" cy="16" rx="3" ry="2"/>',
        "play": '<rect x="3" y="5" width="18" height="14" rx="3"/><path d="m10 9 5 3-5 3Z"/>',
        "ball": '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3v18M5.5 5.5c8 1 8 12 0 13m13-13c-8 1-8 12 0 13"/>',
        "chess": '<path d="M6 20h12l-1-4H8l-1-3 3-2-2-3 3-5h5l2 6-3 7M10 6h2"/>',
        "mail": '<rect x="3" y="5" width="18" height="14" rx="3"/><path d="m3 7 9 6 9-6"/>',
        "github": '<path d="M9 20c-4 1-4-2-6-2m12 4v-4c0-1-.3-2-1-2 3-.4 6-1.5 6-6 0-1.5-.5-2.5-1.5-3.5.4-1 .4-2.3-.2-3.5-1.5 0-3 1-3.5 1.5a13 13 0 0 0-6 0C8 4 6.5 3 5 3c-.6 1.2-.6 2.5-.2 3.5C3.8 7.5 3.3 8.5 3.3 10c0 4.5 3 5.6 6 6-.7.5-1 1.5-1 2v4"/>',
        "search": '<circle cx="10.5" cy="10.5" r="6.5"/><path d="m16 16 5 5"/>',
        "spark": '<path d="m12 2 2.8 7.2L22 12l-7.2 2.8L12 22l-2.8-7.2L2 12l7.2-2.8Z"/>',
    }
    return f'<svg class="icon {cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{paths[name]}</svg>'


def link(url, text, cls="text-link", symbol="external", label=""):
    aria = f' aria-label="{escape(label, quote=True)}"' if label else ""
    return f'<a class="{cls}" href="{escape(url, quote=True)}" target="_blank" rel="noopener noreferrer"{aria}>{text}{icon(symbol)}</a>'


FEATURES = [
    dict(id="resona", name="Resona", category=L("AI × MUSIC", "AI × 音乐"),
         title=L("Music that moves<br>with you.", "让音乐，<br>随你而变。"),
         desc=L("A space where sound and software meet. I co-created Resona, an adaptive music application that combines continuously generated audio with an AI agent for personalizing the experience.", "在这里，声音与软件相遇。我参与共同创作了 Resona：它将持续生成的声音与 AI 智能体结合，让每个人都能调整自己的聆听体验。"),
         points=L(["Procedural sound, binaural beats, and ambient layers", "An AI agent for interface and sound customization", "Personal workspaces with saved preferences"], ["程序生成的声音、双耳节拍与环境音层", "可调整界面与声音的 AI 智能体", "支持保存偏好的个人工作空间"]),
         tech="Python / Flask / Web Audio", role=L("Co-created · Exabyte Technologies", "共同创作 · Exabyte Technologies"), repo="Exabyte-Technologies/Resona"),
    dict(id="whaos", name="WhaOS", category=L("AI × THE WEB", "AI × 网页"),
         title=L("An idea becomes<br>a little app.", "把一个想法，<br>变成一个应用。"),
         desc=L("What if a browser felt like a desktop you could build on? WhaOS is my AI-powered web operating system, with built-in tools and an app generator that turns prompts into new experiences.", "如果浏览器也能成为一个可以不断扩展的桌面呢？我制作的 WhaOS 是一个 AI 驱动的网页操作系统，既有内置工具，也能通过提示词生成新的应用体验。"),
         points=L(["A desktop with movable application windows", "Built-in notes, calculator, and web tools", "AI app generation through a server-side API"], ["支持移动应用窗口的桌面", "内置笔记、计算器与网页工具", "通过服务端 API 实现 AI 应用生成"]),
         tech="JavaScript / HTML / CSS", role=L("Personal project", "个人项目"), repo="hujingwen1025/WhaOS"),
    dict(id="rhythm", name="Rhythm Cook", category=L("MUSIC × PLAY", "音乐 × 游戏"),
         title=L("A little rhythm.<br>A lot of chopping.", "跟上节奏，<br>切出好心情。"),
         desc=L("My love of music, turned into a playful browser game. Watch the chef, learn the rhythm, and slice ingredients on the beat. The soundtrack is synthesized live, right in the browser.", "把对音乐的喜爱，做成一个有趣的网页游戏。看厨师示范、记住节奏，再踩着拍子切食材。连背景音乐也是浏览器实时合成的。"),
         points=L(["20 levels with increasingly intricate rhythms", "Original synthesized soundtracks and SVG ingredients", "Timing feedback, combos, and saved progress"], ["20 个关卡，节奏逐步变得复杂", "实时合成的配乐与 SVG 食材", "节奏反馈、连击与进度保存"]),
         tech="JavaScript / Web Audio / SVG", role=L("Personal project", "个人项目"), repo="hujingwen1025/Rhythm-Cook"),
    dict(id="sonora", name="Sonora / 声息", category=L("SOUND EXPLORATION", "声音探索"),
         title=L("Room to slow down.", "给自己一点放慢的空间。"),
         desc=L("A continuous sound space for relaxation and focus. Synthesized noise, binaural beats, and algorithmic instruments adapt to feedback without interrupting playback.", "为放松与专注制作的连续声音空间。合成噪音、双耳节拍和算法乐器可以根据反馈调整，而不用中断播放。"),
         points=L(["Layered, browser-generated audio", "Feedback-driven sound adjustments"], ["分层的浏览器生成音频", "根据反馈实时调整声音"]),
         tech="Python / Flask / Web Audio", role=L("Personal project", "个人项目"), repo="hujingwen1025/Sonora"),
    dict(id="academy", name="CAICP Academy", category=L("LEARNING TOOLS", "学习工具"),
         title=L("Make learning click.", "让知识真正被理解。"),
         desc=L("An independent bilingual learning site for CAICP preparation, with structured lessons, interactive labs, practice, and a mistake notebook. Progress stays in the learner’s browser.", "一个独立制作的 CAICP 双语备考学习网站，包含系统课程、交互实验、练习与错题本。学习进度保存在使用者自己的浏览器中。"),
         points=L(["English and Simplified Chinese lessons", "Interactive labs and spaced review"], ["英语与简体中文课程", "交互实验与间隔复习"]),
         tech="HTML / CSS / JavaScript", role=L("Personal project · Independent resource", "个人项目 · 独立学习资源"), repo="hujingwen1025/CAICP-Academy"),
    dict(id="dorm", name="Dorm Pass Manager", category=L("EVERYDAY SYSTEMS", "日常管理系统"),
         title=L("Less friction.<br>More clarity.", "少一点繁琐，<br>多一点清晰。"),
         desc=L("An Exabyte application for managing dorm passes, approvals, and sign-ins. It brings a multi-step process into one role-based system with live updates.", "Exabyte 的宿舍通行管理应用，将通行申请、审批与签到整合进同一个系统，支持角色权限与实时更新。"),
         points=L(["Multi-stage approvals and role-based access", "Kiosk and mobile sign-in workflows"], ["多阶段审批与角色权限", "自助终端及移动端签到流程"]),
         tech="Python / Flask / JavaScript / MySQL", role=L("Exabyte Technologies project", "Exabyte Technologies 项目"), repo="Exabyte-Technologies/Dorm-Pass-Manager"),
]

# These are substantive public repositories, not a claim of sole authorship.
REPOS = [
    ("Neuorise", "hujingwen1025/Neuorise", "music", "music", L("Adaptive music generation shaped by questionnaires and listener feedback.", "结合问卷与聆听反馈，探索自适应音乐生成。"), "Python · AI", "personal"),
    ("WB App Store", "Exabyte-Technologies/WB-App-Store", "tools exabyte", "code", L("A web-based interface for browsing and managing Mac apps, built on mas-cli.", "基于 mas-cli，以网页界面浏览与管理 Mac 应用。"), "JavaScript · Electron", "org"),
    ("Printer Manager", "hujingwen1025/Printer-Manager", "tools", "code", L("A self-contained printing and scanning appliance for Linux servers and NAS devices.", "面向 Linux 服务器与 NAS 的一体化打印、扫描管理工具。"), "Python · Django · Docker", "personal"),
    ("Hivemind Print Farm", "Exabyte-Technologies/Hivemind-Print-Farm", "tools exabyte", "code", L("A project for coordinating multiple 3D printers with optimized print queues.", "通过优化打印队列，协调多台 3D 打印机的项目。"), L("3D printing", "3D 打印"), "org"),
    ("1001 Libraries", "hujingwen1025/1001-Libraries-Website", "community", "spark", L("A website for the “From Books to Hearts” library initiative.", "为“From Books to Hearts”图书馆倡议制作的网站。"), "HTML · CSS", "personal"),
    (L("Chinese Citation Generator", "中文参考文献生成器"), "hujingwen1025/Keystone-Chinese-Reference-Generator", "education tools", "code", L("A utility for formatting Chinese references and citations.", "用于整理中文参考文献与引用格式的工具。"), L("Citation tools", "引用工具"), "personal"),
    (L("Recycling Awareness", "回收意识网站"), "hujingwen1025/Keystone-Recycle-Website", "community", "spark", L("A website encouraging more thoughtful recycling habits.", "倡导更有意识的垃圾回收习惯的网站。"), "HTML · CSS", "personal"),
    ("FRC Library Installer", "hujingwen1025/FRC-Library-Installer", "tools education", "code", L("A vendor-library installation project for FIRST Robotics Competition development.", "面向 FIRST Robotics Competition 开发的供应商库安装项目。"), L("Robotics tools", "机器人开发工具"), "personal"),
    ("AI Machines", "hujingwen1025/AI-Machines", "education", "spark", L("Explorations based on Google Teachable Machine.", "基于 Google Teachable Machine 的探索项目。"), L("Machine learning", "机器学习"), "personal"),
    ("KeyShare", "hujingwen1025/KeyShare", "tools", "code", L("A front-end and back-end system in my public project collection.", "我的公开项目集中的一个前后端系统。"), "Python", "personal"),
    ("Remote Tic Tac Toe", "hujingwen1025/Remote-Tic-Tac-Toe", "games", "chess", L("A two-player online tic-tac-toe game with a spectator view.", "支持两人在线对局及观战的井字棋游戏。"), "Python · Flask", "personal"),
    ("Super Duper Captcha", "hujingwen1025/Super-Duper-Captcha", "tools", "spark", L("An experimental animated CAPTCHA exploring a deliberately tricky visual puzzle.", "通过刻意设计的复杂视觉谜题，探索动态验证码的实验项目。"), "Python", "personal"),
    ("ManageBac Grade Hider", "hujingwen1025/ManageBac-Grade-Hider", "tools", "code", L("A browser extension for hiding grade displays in ManageBac.", "用于隐藏 ManageBac 成绩显示的浏览器扩展。"), "JavaScript · Chrome", "personal"),
    ("Power School Aesthetics", "hujingwen1025/Power-School-Aesthetics", "tools", "code", L("A userscript that changes the look of the PowerSchool interface.", "调整 PowerSchool 界面外观的用户脚本。"), "JavaScript · CSS", "personal"),
    ("Website Downloader", "hujingwen1025/websitedownloader", "tools", "code", L("An upstream-based website downloader in my repository collection; original work credited to Ahmad Ibrahiim.", "我的仓库收藏中一个基于上游项目的网站下载工具；原作署名为 Ahmad Ibrahiim。"), "Node.js · Socket.IO", "adapted"),
    (L("West 6 Website", "West 6 网站"), "hujingwen1025/West-6-Website", "community", "code", L("A community website project in my public repository collection.", "我的公开仓库集中的一个社区网站项目。"), L("Website", "网站"), "personal"),
    ("Exabyte Website", "Exabyte-Technologies/Exabyte-Website", "exabyte", "code", L("The public source repository for Exabyte’s official website.", "Exabyte 官方网站的公开源代码仓库。"), "HTML · CSS", "org"),
    (L("JuYuanQin Website", "聚缘琴科技网站"), "Exabyte-Technologies/JuYuanQin-Site", "exabyte", "code", L("A technology-company website in the Exabyte organization’s public portfolio.", "Exabyte 组织公开项目集中的一个科技公司网站。"), "HTML · CSS", "org"),
]

COPY = {
    "title": L("William Hu — Code, music & curiosity", "William Hu · 胡竞文 — 代码、音乐与好奇心"),
    "description": L("Meet William Hu (Jingwen Hu): programmer, founder of Exabyte Technologies, piano enthusiast, and creative collaborator. Explore projects in AI, music, learning, and everyday tools.", "认识 William Hu（胡竞文）：程序开发者、Exabyte Technologies 创始人、钢琴爱好者与创意协作者。探索他在 AI、音乐、学习及日常工具领域的项目。"),
    "skip": L("Skip to content", "跳转到正文"),
    "nav": L(["About", "Work", "Beyond code", "Connect"], ["关于我", "作品", "代码之外", "联系"]),
    "menu": L("Open navigation", "展开导航"), "close": L("Close navigation", "收起导航"),
    "lang": L("Read this website in Chinese", "阅读英文版网站"),
    "eyebrow": L("A CURIOUS MIND. A WORK IN PROGRESS.", "保持好奇，不断创造。"),
    "hi": L("Hi, I’m", "你好，我是"), "name": L("William.", "William。"),
    "intro": L("I write code, play piano, and turn the occasional<br class=\"desktop-break\"> “what if?” into something real.", "我写代码、弹钢琴，也喜欢把偶尔冒出的<br class=\"desktop-break\">“如果可以呢？”变成真实的作品。"),
    "work_cta": L("Explore my work", "看看我的作品"), "about_cta": L("A little about me", "认识一下我"),
    "hero_note": L("PROGRAMMER / FOUNDER / CREATOR", "程序开发 / 创业 / 创作"),
    "scroll": L("SCROLL TO GET TO KNOW ME", "向下滚动，认识更多面的我"),
    "hero_chip": L("Made of curiosity.", "好奇心制造。"),
    "code_comment": L("# a little about me", "# 一点关于我"),
    "about_kicker": L("01 / THE PERSON BEHIND THE PROJECTS", "01 / 作品背后的我"),
    "about_title": L("A few different interests.<br>One curious person.", "兴趣有很多。<br>好奇心，始终如一。"),
    "about_text": L("I’m William Hu, also known as Jingwen Hu / 胡竞文. I like the point where a small idea becomes something you can actually use, hear, or play with.", "我是 William Hu，中文名胡竞文，也叫 Jingwen Hu。我喜欢看一个小想法慢慢变成真正能使用、聆听或一起玩的东西。"),
    "about_text2": L("Sometimes that means building an AI-powered tool. Sometimes it means sitting at the piano, editing a video, or making something with other people. I enjoy the process of figuring things out, especially together.", "有时是制作一个 AI 工具，有时是坐在钢琴前、剪一段视频，或与别人共同完成一个项目。我享受探索问题的过程，尤其是和别人一起探索。"),
    "skill_title": L("MY EVERYDAY TOOLKIT", "我的常用工具箱"),
    "primary": L("My first language for building", "我最常用的开发语言"),
    "also": L("I also work with", "也使用这些语言"),
    "about_aside": L("The best part?<br>There’s always more to learn.", "最有意思的是？<br>总有新的东西可以学。"),
    "work_kicker": L("02 / SELECTED WORK", "02 / 精选作品"),
    "work_title": L("Ideas, brought to life.", "把想法，做出来。"),
    "work_intro": L("A few things I’ve built and worked on. Different forms, same instinct: explore an idea and make it useful.", "一些我制作或参与的项目。形式各不相同，但都源于同一个想法：探索一种可能，然后让它变得有用。"),
    "repo": L("Explore the repository", "查看项目仓库"),
    "illustration": L("Concept illustration · not an application screenshot", "概念插画 · 非应用截图"),
    "more_features": L("More ways to put an idea to work.", "让想法发挥作用的更多方式。"),
    "music_note": L("My music projects explore sound, personalization, and everyday wellbeing; they do not establish clinical outcomes.", "我的音乐项目探索声音、个性化与日常身心体验，并不代表已证实的临床效果。"),
    "org_kicker": L("03 / BUILDING TOGETHER", "03 / 一起创造"),
    "org_title": L("Small ideas.<br>Shared ambition.", "从小想法出发。<br>向共同目标前进。"),
    "org_text": L("I founded Exabyte Technologies around a simple idea: technology should be safer, more convenient, and more approachable. It’s a home for projects that bring that idea into everyday life.", "我创立 Exabyte Technologies，源于一个简单的想法：科技应该更加安全、方便，也更容易接近。我们通过一个个项目，让这样的想法走进日常生活。"),
    "org_text2": L("Our public work spans music experiences, useful software, printing tools, and websites. The projects here belong to the organization’s portfolio; shared work is credited as shared work.", "我们的公开项目涉及音乐体验、实用软件、打印工具及网站。这里展示的是组织的项目集；共同完成的作品，也会明确标注为合作成果。"),
    "org_visit": L("Visit Exabyte", "访问 Exabyte 官网"), "org_github": L("Exabyte on GitHub", "Exabyte 的 GitHub"),
    "org_words": L(["Safer.", "Simpler.", "Closer to everyone."], ["更安全。", "更方便。", "让每个人都能接近。"]),
    "life_kicker": L("04 / BEYOND THE KEYBOARD", "04 / 键盘之外"),
    "life_title": L("There’s more to me<br>than a browser tab.", "生活，不止一个<br>浏览器标签页。"),
    "life_intro": L("The things I make are only part of the picture. These are a few things I enjoy just as much.", "作品只是我的一部分。这些事情，也让我乐在其中。"),
    "directory_kicker": L("05 / KEEP EXPLORING", "05 / 继续探索"),
    "directory_title": L("The rest of the rabbit hole.", "好奇心，还有下一站。"),
    "directory_intro": L("More public projects, experiments, and shared work. Follow a thread that interests you.", "更多公开项目、实验与合作作品。从你感兴趣的方向开始探索。"),
    "search": L("Search projects, ideas, or tools", "搜索项目、想法或工具"),
    "search_label": L("Search the project directory", "搜索项目目录"),
    "filters_label": L("Filter projects by category", "按类别筛选项目"),
    "categories": L(["All work", "AI & music", "Learning", "Tools", "Play", "Community", "Exabyte"], ["全部作品", "AI 与音乐", "学习", "工具", "游戏", "社区", "Exabyte"]),
    "empty_title": L("No projects on this trail.", "这条路上暂时没有项目。"),
    "empty_text": L("Try another word or explore a different category.", "换个关键词，或看看其他类别。"),
    "reset": L("Show all projects", "显示全部项目"),
    "result": L("{count} projects to explore", "共 {count} 个项目"),
    "result_singular": L("{count} project to explore", "共 {count} 个项目"),
    "roles": L({"personal": "Personal repository", "org": "Exabyte project", "adapted": "Upstream-based project"}, {"personal": "个人仓库", "org": "Exabyte 项目", "adapted": "基于上游的项目"}),
    "contact_kicker": L("06 / SAY HELLO", "06 / 打个招呼"),
    "contact_title": L("Good things start<br>with a conversation.", "好的开始，<br>往往是一次交流。"),
    "contact_text": L("An idea to share? Something to build together?<br>I’m always happy to meet curious people.", "有想分享的点子？或者一起完成一个项目？<br>我很乐意认识同样充满好奇心的你。"),
    "email": L("Email me", "给我写邮件"),
    "footer": L("A little code. A little music. A lot of curiosity.", "一点代码，一点音乐，还有很多好奇心。"),
    "back": L("Back to top", "回到顶部"),
}


def localized(value, lang):
    return value[lang] if isinstance(value, dict) and "en" in value else value


def art(kind, lang):
    """Decorative, intentionally abstract project visuals, not counterfeit UI."""
    labels = {
        "resona": L("Sound, shaped around you", "让声音，围绕你展开"),
        "whaos": L("An open space for ideas", "给想法一个开放的空间"),
        "rhythm": L("Find your rhythm", "找到你的节奏"),
        "sonora": L("A softer kind of space", "一片柔和的声音空间"),
        "academy": L("Connect the dots", "把知识串联起来"),
        "dorm": L("Everything in its place", "让流程井井有条"),
    }
    if kind in ("resona", "sonora"):
        bars = "".join(f'<i style="--h:{h}%;--i:{i}"></i>' for i, h in enumerate([16,25,38,28,55,78,52,35,69,94,66,45,30,56,82,100,76,47,62,37,21,43,65,35,19,28,15]))
        inner = f'<div class="sound-orbit orbit-a"></div><div class="sound-orbit orbit-b"></div><div class="sound-orbit orbit-c"></div><div class="sound-core">{icon("music")}</div><div class="waveform">{bars}</div>'
    elif kind == "whaos":
        inner = '<div class="desktop-paper paper-back"></div><div class="desktop-paper paper-front"><div class="window-dots"><i></i><i></i><i></i></div><div class="app-grid">' + "".join(f'<span>{icon(x)}</span>' for x in ["code", "music", "chess", "spark"]) + '</div><div class="prompt-line"><span>+</span><i></i><b>↗</b></div></div><div class="cursor-shape"></div>'
    elif kind == "rhythm":
        inner = '<div class="chopping-board"><div class="slice slice-1"></div><div class="slice slice-2"></div><div class="slice slice-3"></div><div class="carrot"></div><div class="knife"><i></i></div></div><div class="beat-track"><i></i><i></i><i></i><i></i><span>♪</span></div><div class="rhythm-spark">✳</div>'
    elif kind == "academy":
        inner = '<div class="learning-lines"></div><div class="learning-node node-a">{ }</div><div class="learning-node node-b">Σ</div><div class="learning-node node-c">01</div><div class="learning-node node-d">↗</div>'
    else:
        inner = '<div class="pass-card pass-back"></div><div class="pass-card pass-front"><span class="pass-avatar"></span><div class="pass-lines"><i></i><i></i></div><div class="pass-check">✓</div><div class="pass-code">' + '<i></i>' * 16 + '</div></div><div class="pass-route"><i></i><i></i><i></i></div>'
    return f'<div class="project-art art-{kind}" aria-hidden="true">{inner}<span class="art-label">{labels[kind][lang]}</span><span class="art-corner">↗</span></div>'


def feature(p, lang, index, compact=False):
    v = lambda x: localized(x, lang)
    points = "".join(f'<li>{escape(t)}</li>' for t in v(p["points"]))
    illustration = f'<div class="{"compact-art" if compact else "mobile-art"}">{art(p["id"], lang)}</div>'
    return f'''<article class="{'feature-card' if compact else 'story-step'}" {('data-reveal' if compact else f'data-scene="{index}"')} id="project-{p['id']}">
      {illustration if compact else ''}
      <div class="feature-copy"><div class="project-category"><span class="project-name">{p['name']}</span>{v(p['category'])}</div>
      <h3>{v(p['title'])}</h3><p>{v(p['desc'])}</p><ul class="feature-points">{points}</ul>
      <div class="project-tech">{p['tech']}</div><div class="project-role">{v(p['role'])}</div>
      {link('https://github.com/' + p['repo'], COPY['repo'][lang], label=COPY['repo'][lang] + ' — ' + p['name'])}</div>{illustration if not compact else ''}
    </article>'''


def page(lang):
    c = {key: value[lang] for key, value in COPY.items()}
    zh = lang == "zh"
    prefix = "../" if zh else ""
    other = "../" if zh else "zh/"
    nav = "".join(f'<a href="#{anchor}">{title}</a>' for anchor, title in zip(["about", "work", "beyond", "connect"], c["nav"]))
    story = "".join(feature(p, lang, i) for i, p in enumerate(FEATURES[:3]))
    scenes = "".join(f'<div class="scene-panel {"is-active" if i == 0 else ""}" data-panel="{i}">{art(p["id"], lang)}</div>' for i, p in enumerate(FEATURES[:3]))
    compact = "".join(feature(p, lang, i, True) for i, p in enumerate(FEATURES[3:]))
    filters = "".join(f'<button type="button" class="filter-button {"is-selected" if i == 0 else ""}" data-filter="{key}" aria-pressed="{str(i == 0).lower()}">{name}</button>' for i, (key, name) in enumerate(zip(["all", "music", "education", "tools", "games", "community", "exabyte"], c["categories"])))
    repos = ""
    for name, repo, tags, symbol, desc, tech, role in REPOS:
        name, desc, tech = [localized(x, lang) for x in (name, desc, tech)]
        repos += f'''<article class="repo-card" data-tags="{tags}"><div class="repo-top"><span class="repo-icon">{icon(symbol)}</span><span class="repo-role">{c['roles'][role]}</span></div>
          <h3>{escape(name)}</h3><p>{escape(desc)}</p><div class="repo-bottom"><span>{escape(tech)}</span>{link('https://github.com/'+repo, f'<span class="sr-only">{escape(name)} — GitHub</span>', 'repo-link')}</div></article>'''
    interests = [
        ("piano", "music", L("Piano & music", "钢琴与音乐"), L("Away from the screen, I enjoy spending time at the piano. Music is something I enjoy playing, listening to, and exploring through code.", "离开屏幕，我也享受坐在钢琴前的时光。演奏、聆听，或用代码探索声音，都是我享受音乐的方式。"), L("A different kind of keyboard.", "另一种键盘。")),
        ("sports", "ball", L("A little time on the court", "球场上的时间"), L("Soccer and basketball are a good reason to step outside, move around, and enjoy being part of a team.", "足球和篮球让我有理由走到户外、动起来，也享受和队友一起配合的乐趣。"), L("Less screen. More movement.", "少一点屏幕，多一点运动。")),
        ("video", "play", L("Stories in motion", "流动的故事"), L("I like making and editing videos: finding a sequence, a cut, or a small detail that makes an idea come across.", "我喜欢制作、剪辑视频：寻找合适的顺序、剪切点，或一个能让想法被理解的小细节。"), L("A new way to tell an idea.", "用另一种方式表达想法。")),
        ("games", "chess", L("One more round?", "再来一局？"), L("Chess, UNO, and board games bring out another side of my curiosity. A little strategy and good company go a long way.", "国际象棋、UNO 和桌游，让好奇心有了另一种出口。一点策略，再加上合拍的朋友，就足够有趣。"), L("Good company. Good games.", "好朋友，好游戏。")),
    ]
    life = ""
    for kind, symbol, title, desc, foot in interests:
        life += f'<article class="interest-card interest-{kind}" data-reveal><div class="interest-visual" aria-hidden="true">{interest_art(kind, symbol)}</div><div class="interest-copy"><h3>{title[lang]}</h3><p>{desc[lang]}</p><span>{foot[lang]}</span></div></article>'
    return f'''<!doctype html>
<html lang="{'zh-Hans' if zh else 'en'}">
<head>
  <meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="color-scheme" content="light"><meta name="theme-color" content="#f8f7f4">
  <title>{c['title']}</title><meta name="description" content="{escape(c['description'], quote=True)}">
  <link rel="canonical" href="{SITE_URL}/{'zh/' if zh else ''}"><link rel="alternate" hreflang="en" href="{SITE_URL}/"><link rel="alternate" hreflang="zh-Hans" href="{SITE_URL}/zh/"><link rel="alternate" hreflang="x-default" href="{SITE_URL}/">
  <meta property="og:type" content="website"><meta property="og:title" content="{c['title']}"><meta property="og:description" content="{escape(c['description'], quote=True)}">
  <meta property="og:locale" content="{'zh_CN' if zh else 'en_US'}"><meta property="og:locale:alternate" content="{'en_US' if zh else 'zh_CN'}">
  <meta property="og:url" content="{SITE_URL}/{'zh/' if zh else ''}"><meta property="og:site_name" content="William Hu"><meta property="og:image" content="{SITE_URL}/assets/social{'-zh' if zh else ''}.png"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:alt" content="{'William Hu — 代码 / 音乐 / 好奇心' if zh else 'William Hu — Code / Music / Curiosity'}">
  <meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{c['title']}"><meta name="twitter:description" content="{escape(c['description'], quote=True)}"><meta name="twitter:image" content="{SITE_URL}/assets/social{'-zh' if zh else ''}.png">
  <link rel="icon" href="{prefix}assets/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="{prefix}assets/style.css">
  <script src="{prefix}assets/site.js" defer></script>
</head>
<body data-language="{lang}">
  <a class="skip-link" href="#main">{c['skip']}</a><div class="reading-progress" aria-hidden="true"><span></span></div>
  <header class="site-header"><div class="nav-shell"><a class="wordmark" href="#top" aria-label="William Hu"><span>W<span class="brand-dot">.</span></span><span class="wordmark-name">William Hu</span></a>
    <nav id="navigation" class="navigation" aria-label="{'主导航' if zh else 'Main navigation'}">{nav}</nav>
    <div class="nav-actions"><a class="language-link" href="{other}" lang="{'en' if zh else 'zh-Hans'}" hreflang="{'en' if zh else 'zh-Hans'}" aria-label="{c['lang']}"><span class="{'muted' if zh else 'current'}">EN</span><span class="lang-divider">/</span><span class="{'current' if zh else 'muted'}">中</span></a>
    <button class="menu-toggle" type="button" aria-controls="navigation" aria-expanded="false" aria-label="{c['menu']}" data-open-label="{c['menu']}" data-close-label="{c['close']}" hidden><span></span><span></span></button></div>
  </div></header>
  <main id="main">
    <section class="hero container" id="top" aria-labelledby="hero-heading"><div class="hero-copy"><div class="eyebrow hero-enter">{c['eyebrow']}</div>
      <h1 id="hero-heading" class="hero-enter"><span class="hero-greeting">{c['hi']}</span><br><span class="hero-name">{c['name']}</span><svg class="name-underline" viewBox="0 0 400 22" aria-hidden="true"><path d="M4 15Q165 0 396 9"/></svg></h1>
      <p class="hero-description hero-enter">{c['intro']}</p><div class="hero-links hero-enter"><a href="#work" class="button button-blue">{c['work_cta']}{icon('arrow')}</a><a class="text-link" href="#about">{c['about_cta']}{icon('arrow')}</a></div></div>
      <div class="hero-composition hero-enter" aria-hidden="true"><div class="composition-grid"></div><div class="composition-orbit"></div><div class="code-note"><div class="window-dots"><i></i><i></i><i></i></div><div class="code-lines"><span class="code-dim">{c['code_comment']}</span><br><span class="code-blue">while</span> curious:<br>&nbsp;&nbsp;explore()<br>&nbsp;&nbsp;create()<br>&nbsp;&nbsp;<span class="code-blue">repeat</span>()<span class="code-caret"></span></div><span class="note-corner">↗</span></div><div class="vinyl"><div class="vinyl-rings"></div><div class="vinyl-label">{icon('music')}<i></i></div></div><div class="hero-piano"><div class="piano-keys">{''.join('<i></i>' for _ in range(12))}</div></div><div class="curiosity-chip">{icon('spark')}{c['hero_chip']}</div><div class="composition-cross">+</div><div class="composition-dot"></div></div>
      <div class="hero-bottom"><span>{c['hero_note']}</span><a href="#about">{c['scroll']}<span class="scroll-arrow">↓</span></a></div>
    </section>
    <section class="about-section section container" id="about" aria-labelledby="about-heading"><div class="section-kicker" data-reveal>{c['about_kicker']}</div><div class="about-grid"><div data-reveal><h2 id="about-heading">{c['about_title']}</h2><div class="about-prose"><p>{c['about_text']}</p><p>{c['about_text2']}</p></div><p class="handwritten">{c['about_aside']}</p></div><aside class="toolkit" data-reveal><div class="toolkit-header">{icon('code')}<span>{c['skill_title']}</span></div><div class="primary-language"><span>Py</span><div><h3>Python</h3><p>{c['primary']}</p></div></div><p class="also-label">{c['also']}</p><div class="language-tags"><span>JavaScript</span><span>Swift</span><span>C++</span><span>AppleScript</span><span>HTML & CSS</span></div><div class="toolkit-lines" aria-hidden="true"><i></i><i></i><i></i><i></i></div></aside></div></section>
    <section class="work-section section" id="work" aria-labelledby="work-heading"><div class="container"><div class="section-heading" data-reveal><div class="section-kicker">{c['work_kicker']}</div><h2 id="work-heading">{c['work_title']}</h2><p>{c['work_intro']}</p></div><div class="project-story"><div class="story-copy">{story}</div><div class="story-visual"><div class="sticky-scene"><div class="scene-stack">{scenes}</div><div class="scene-footer"><span>{c['illustration']}</span><div class="scene-markers" aria-hidden="true"><i class="is-active"></i><i></i><i></i></div></div></div></div></div><h3 class="more-feature-heading" data-reveal>{c['more_features']}</h3><div class="feature-grid">{compact}</div><p class="music-note">{c['music_note']}</p></div></section>
    <section class="organization-section" id="exabyte" aria-labelledby="org-heading"><div class="container org-grid"><div data-reveal><div class="section-kicker">{c['org_kicker']}</div><div class="organization-name">{icon('spark')}Exabyte Technologies</div><h2 id="org-heading">{c['org_title']}</h2><p>{c['org_text']}</p><p class="org-secondary">{c['org_text2']}</p><div class="org-links">{link('https://exabyte.org.cn', c['org_visit'], 'button button-light')}{link('https://github.com/Exabyte-Technologies', c['org_github'])}</div></div><div class="org-visual" data-reveal><div class="exabyte-mark" aria-hidden="true"><div></div><div></div><div></div><div></div></div><div class="org-values">{''.join(f'<span>{word}</span>' for word in c['org_words'])}</div><span class="org-caption">EXABYTE / TECHNOLOGIES</span></div></div></section>
    <section class="life-section section container" id="beyond" aria-labelledby="life-heading"><div class="section-heading" data-reveal><div class="section-kicker">{c['life_kicker']}</div><h2 id="life-heading">{c['life_title']}</h2><p>{c['life_intro']}</p></div><div class="interests-grid">{life}</div></section>
    <section class="directory-section section" id="explore" aria-labelledby="directory-heading"><div class="container"><div class="section-heading" data-reveal><div class="section-kicker">{c['directory_kicker']}</div><h2 id="directory-heading">{c['directory_title']}</h2><p>{c['directory_intro']}</p></div><div class="directory-controls" hidden><label class="search-field">{icon('search')}<span class="sr-only">{c['search_label']}</span><input id="project-search" type="search" placeholder="{c['search']}" autocomplete="off" maxlength="200"></label><div class="filter-list" role="group" aria-label="{c['filters_label']}">{filters}</div></div><p class="result-count" role="status" aria-live="polite" aria-atomic="true" data-template="{c['result']}" data-singular="{c['result_singular']}">{c['result'].replace('{count}', str(len(REPOS)))}</p><div class="repo-grid">{repos}</div><div class="empty-state" hidden><span aria-hidden="true">↗</span><h3>{c['empty_title']}</h3><p>{c['empty_text']}</p><button class="text-link reset-search" type="button">{c['reset']}{icon('arrow')}</button></div></div></section>
    <section class="contact-section section container" id="connect" aria-labelledby="contact-heading"><div class="contact-spark" aria-hidden="true">{icon('spark')}</div><div class="section-kicker" data-reveal>{c['contact_kicker']}</div><h2 id="contact-heading" data-reveal>{c['contact_title']}</h2><p data-reveal>{c['contact_text']}</p><a class="email-link" href="mailto:jingwen.hu@exabyte.org.cn" aria-label="{c['email']}: jingwen.hu@exabyte.org.cn">jingwen.hu@exabyte.org.cn{icon('external')}</a><div class="contact-socials">{link('https://github.com/hujingwen1025', 'GitHub', 'text-link', 'github')}{link('https://github.com/Exabyte-Technologies', 'Exabyte Technologies')}</div></section>
  </main><footer class="site-footer container"><div><span class="footer-name">William Hu<span>.</span></span><p>{c['footer']}</p></div><a href="#top" class="back-top">{c['back']}<span aria-hidden="true">↑</span></a></footer>
</body></html>'''


def interest_art(kind, symbol):
    if kind == "piano":
        return '<div class="mini-piano"><div class="piano-keys">' + '<i></i>' * 14 + '</div></div><span class="floating-note">♪</span><span class="floating-note note-two">♫</span>'
    if kind == "sports":
        return '<div class="court-lines"></div><div class="basketball">' + icon('ball') + '</div><div class="ball-shadow"></div>'
    if kind == "video":
        return '<div class="video-frame">' + icon('play') + '<div class="video-timeline"><i></i><i></i><i></i></div></div><span class="video-cross">+</span>'
    return '<div class="game-board"></div><div class="game-piece">' + icon('chess') + '</div><div class="game-disc"></div>'


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--site-url", default=SITE_URL, help="Public URL for canonical, social, and sitemap metadata")
    args = parser.parse_args()
    parsed_url = urlsplit(args.site_url)
    if (parsed_url.scheme != "https" or not parsed_url.netloc or parsed_url.query or parsed_url.fragment
            or parsed_url.username or parsed_url.password or any(ch.isspace() for ch in args.site_url)
            or any(ch in args.site_url for ch in '<>\"\'')):
        parser.error("--site-url must be a public HTTPS URL without credentials, a query, or a fragment")
    SITE_URL = args.site_url.rstrip("/")
    (PUBLIC / "zh").mkdir(parents=True, exist_ok=True)
    (PUBLIC / "assets").mkdir(exist_ok=True)
    (PUBLIC / "index.html").write_text(page("en"), encoding="utf-8")
    (PUBLIC / "zh" / "index.html").write_text(page("zh"), encoding="utf-8")
    sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
    for suffix in ("/", "/zh/"):
        sitemap += f'<url><loc>{escape(SITE_URL + suffix)}</loc><xhtml:link rel="alternate" hreflang="en" href="{escape(SITE_URL)}/"/><xhtml:link rel="alternate" hreflang="zh-Hans" href="{escape(SITE_URL)}/zh/"/></url>\n'
    (PUBLIC / "sitemap.xml").write_text(sitemap + "</urlset>\n", encoding="utf-8")
    (PUBLIC / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {SITE_URL}/sitemap.xml\n", encoding="utf-8")
    print(f"Built 2 languages, {len(FEATURES)} featured projects, {len(REPOS)} directory projects.")
