#!/usr/bin/env python3
"""Build both readable, static language editions. Python standard library only."""
from pathlib import Path
from html import escape
from urllib.parse import urlsplit
import argparse
from error_pages import write_error_pages

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


LEGACY_FEATURES = [
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
    "wechat": L("Add me on WeChat", "添加我的微信"),
    "footer": L("A little code. A little music. A lot of curiosity.", "一点代码，一点音乐，还有很多好奇心。"),
    "back": L("Back to top", "回到顶部"),
}


def localized(value, lang):
    return value[lang] if isinstance(value, dict) and "en" in value else value


# The original six descriptions remain the source for the full project catalog.
FEATURES = [
    dict(id="resona-lite", name="Resona Lite", repo="Exabyte-Technologies/Resona-Lite",
         desc=L("A little space to reset. Ambient music made on your device, for rest, focus, and quiet moments.", "给自己一点放松的空间。在设备上生成环境音乐，陪伴休息、专注与安静时光。"),
         tech="React Native / Expo / Web Audio", role=L("Exabyte Technologies project", "Exabyte Technologies 项目"),
         points=L(["On-device audio and chord generation", "Listening moods, layer balance, and a sleep timer"], ["在设备上生成音频与和弦", "聆听模式、音层平衡与睡眠定时器"]),
         tags="music exabyte", image="resona-home.png", image2="resona-chords.png",
         caption=L("Home and chord controls, web preview", "首页与和弦控制，网页预览"),
         action=L("View on the App Store", "在 App Store 查看"), url="https://apps.apple.com/app/resona-lite/id6829783715"),
    dict(id="cubers", name="Cubers", repo="Exabyte-Technologies/Cubers",
         desc=L("Learn a puzzle, practice a turn, and find people to cube with. A place for learning, play, and community.", "学会一种新魔方，练习每一次转动，遇见一起玩的人。把学习、游戏与社区放在一起。"),
         tech="TypeScript / React Native / NestJS / Three.js", role=L("Exabyte Technologies project", "Exabyte Technologies 项目"),
         points=L(["Guided puzzle lessons and interactive 3D practice", "Play and community features in development"], ["分步魔方课程与交互式 3D 练习", "正在开发中的游戏与社区功能"]),
         tags="education games community exabyte", image="cubers-learn.jpg", image2="cubers-pathways.jpg",
         caption=L("Development preview with synthetic test progress", "开发预览，使用模拟测试进度"),
         status=L("In development", "开发中")),
    dict(**{**LEGACY_FEATURES[4], "desc": L("An independent bilingual learning space with lessons, interactive labs, practice, and a mistake notebook.", "一个独立制作的双语学习空间，包含课程、交互实验、练习与错题本。"),
         "tags": "education tools", "image": "academy-desktop.png", "caption": L("CAICP Academy, browser preview", "CAICP Academy，浏览器预览"),
         "action": L("Explore the website", "访问学习网站"), "url": "https://caicp.williamhu.tech/"}),
    dict(**{**LEGACY_FEATURES[5], "desc": L("One place for dorm passes, approvals, and sign-ins. A clearer way to keep an everyday process moving.", "把宿舍通行申请、审批与签到放在一起，让日常流程更加清晰。"),
         "tags": "tools exabyte", "image": "dorm-desktop.png", "caption": L("Public sign-in template preview", "公开登录界面模板预览")}),
]

COPY.update({
    "title": L("William Hu | Code, music & curiosity", "William Hu 胡竞文 | 代码、音乐与好奇心"),
    "intro": L("I write code, play piano, and enjoy making things.", "我写代码、弹钢琴，也享受创造的过程。"),
    "about_cta": L("Meet me", "认识我"),
    "about_title": L("Curiosity takes a few different forms.", "好奇心，不止一种模样。"),
    "about_text2": L("Away from code, you’ll find me at the piano, making and editing videos, playing soccer or basketball, or sitting down for chess, UNO, and board games. I like figuring things out, especially with other people.", "代码之外，我喜欢弹钢琴、制作和剪辑视频、踢足球和打篮球，也喜欢与朋友下国际象棋、玩 UNO 和桌游。我享受探索的过程，尤其是和别人一起探索。"),
    "skill_title": L("My everyday toolkit", "我的常用工具"),
    "work_title": L("A few things I’ve made.", "一些做出来的想法。"),
    "work_intro": L("Music, learning, and useful little systems. A selection of personal and shared work.", "音乐、学习，还有实用的日常系统。一些个人与合作作品。"),
    "life_title": L("Beyond code.", "代码之外。"),
    "directory_title": L("Follow your curiosity.", "从好奇的地方开始。"),
    "directory_intro": L("The full collection: products, experiments, and everyday tools.", "完整项目集：产品、实验，还有日常小工具。"),
    "org_title": L("Better things, built together.", "一起，把想法做好。"),
    "contact_title": L("Let’s say hello.", "打个招呼吧。"),
    "details": L("Project details", "项目详情"),
    "source": L("Source code", "源代码"),
    "tech": L("Made with", "使用技术"),
    "role": L("Attribution", "项目归属"),
    "all_projects": L("Explore all projects", "浏览全部项目"),
})

INTERESTS = [
    ("piano", "music", L("Piano & music", "钢琴与音乐"), L("Away from the screen, I enjoy spending time at the piano. Music is something I enjoy playing, listening to, and exploring through code.", "离开屏幕，我也享受坐在钢琴前的时光。演奏、聆听，或用代码探索声音，都是我享受音乐的方式。")),
    ("sports", "ball", L("Time on the court", "球场上的时间"), L("Soccer and basketball are a good reason to step outside, move around, and enjoy being part of a team.", "足球和篮球让我有理由走到户外、动起来，也享受和队友一起配合的乐趣。")),
    ("video", "play", L("Stories in motion", "流动的故事"), L("I like making and editing videos: finding a sequence, a cut, or a small detail that makes an idea come across.", "我喜欢制作、剪辑视频：寻找合适的顺序、剪切点，或一个能让想法被理解的小细节。")),
    ("games", "chess", L("One more round?", "再来一局？"), L("Chess, UNO, and board games bring out another side of my curiosity. A little strategy and good company go a long way.", "国际象棋、UNO 和桌游，让好奇心有了另一种出口。一点策略，再加上合拍的朋友，就足够有趣。")),
]


def catalog():
    projects = []
    originals = {p["repo"]: p for p in LEGACY_FEATURES}
    for p in FEATURES:
        projects.append({**p, "detail": originals.get(p["repo"], p), "anchor": "catalog-" + p["id"]})
    for p in LEGACY_FEATURES:
        if p["repo"] not in {f["repo"] for f in FEATURES}:
            tag = {"resona": "music exabyte", "whaos": "tools", "rhythm": "music games", "sonora": "music"}[p["id"]]
            projects.append({**p, "tags": tag, "detail": p, "anchor": "project-" + p["id"]})
    for name, repo, tags, symbol, desc, tech, role in REPOS:
        projects.append(dict(name=name, repo=repo, tags=tags, desc=desc, tech=tech.replace(" · ", " / ") if isinstance(tech, str) else tech,
                             role=role,
                             anchor="project-" + repo.split("/")[1].lower()))
    projects += [
        dict(name="Daylight", repo="Exabyte-Technologies/Daylight", tags="tools exabyte", role="org", tech="HTML / CSS / JavaScript",
             desc=L("A read-only ICS calendar viewer with month, week, day, and agenda views.", "只读 ICS 日历查看器，支持月、周、日及日程列表视图。"), anchor="project-daylight"),
        dict(name=L("William’s Calendar", "William 的日历"), repo="hujingwen1025/Williams-Calendar", tags="tools", role="personal", tech="React / Fastify / SQLite",
             desc=L("A personal calendar project for my own scheduling workflow.", "为自己的日程安排制作的个人日历项目。"), anchor="project-williams-calendar"),
    ]
    return projects


def project_details(p, lang):
    v = lambda x: localized(x, lang)
    role = v(p['role'])
    if role in ('personal', 'org', 'adapted'):
        role = COPY['roles'][lang][role]
    points = ''.join(f'<li>{escape(point)}</li>' for point in v(p.get('points', L([], []))))
    return f'<p>{v(p["desc"])}</p>{"<ul>" + points + "</ul>" if points else ""}<dl><div><dt>{COPY["tech"][lang]}</dt><dd>{escape(v(p["tech"]).replace(" · ", " / "))}</dd></div><div><dt>{COPY["role"][lang]}</dt><dd>{escape(role.replace(" · ", ", "))}</dd></div></dl>'


def feature(p, lang, prefix):
    v = lambda x: localized(x, lang)
    images = f'<img src="{prefix}assets/projects/{p["image"]}" width="{390 if p["id"] == "resona-lite" else 822 if p["id"] == "cubers" else 1440}" height="{844 if p["id"] == "resona-lite" else 1884 if p["id"] == "cubers" else 900}" alt="{escape(p["name"] + ": " + v(p["caption"]), quote=True)}" loading="lazy" decoding="async">'
    if p.get('image2'):
        images += f'<img src="{prefix}assets/projects/{p["image2"]}" width="{390 if p["id"] == "resona-lite" else 822}" height="{844 if p["id"] == "resona-lite" else 1884}" alt="" loading="lazy" decoding="async">'
    status = f'<p class="project-status">{v(p["status"])}</p>' if p.get('status') else ''
    action = link(p['url'], v(p['action'])) if p.get('url') else ''
    role = v(p['role']).replace(' · ', ', ')
    return f'''<article class="feature-card" id="project-{p['id']}">
      <figure class="project-figure"><div class="project-visual {'portrait-pair' if p.get('image2') else 'landscape'}">{images}</div><figcaption>{v(p['caption'])}</figcaption></figure>
      <div class="feature-copy"><h3>{p['name']}</h3>{status}<p>{v(p['desc'])}</p><p class="project-role">{escape(role)}</p>
      <div class="project-links">{action}{link('https://github.com/'+p['repo'], COPY['source'][lang], label=p['name'] + ': GitHub')}</div>
      <details class="project-details"><summary>{COPY['details'][lang]}</summary><div class="detail-body">{project_details(p, lang)}</div></details></div></article>'''


TOPICS = (
    ("technology", L("Technology", "科技"), L("I like figuring out how things work, then writing software that makes them a little easier to use.", "我喜欢弄清事物是如何运作的，再写一些软件，让它们用起来更顺手。"),
     L("My projects include learning tools and software for everyday workflows. The circuit board here lets you follow a signal from the chip to a contact at the edge.", "我的项目包括学习工具和解决日常问题的软件。试试这块电路板，看看信号怎样从芯片传到边缘的触点。"),
     L("Circuit board", "电路板"), (("project-academy", "CAICP Academy"), ("project-dorm", "Dorm Pass Manager")),
     """         .----------------------.
        / +++==[######]==+++   /|
       / ::: /@:::::@/  ::   / |
      / +++ /@:::::@/==+++  /  /
     /=====================/  /
     '---------------------' /"""),
    ("music", L("Music", "音乐"), L("I play piano, listen to music, and explore what happens when sound and code come together.", "我喜欢弹钢琴、听音乐，也喜欢探索声音与代码碰到一起会发生什么。"),
     L("That curiosity carries into Resona Lite and Rhythm Cook. Switch the pattern above the keys to see how moving the accents changes the rhythm.", "这份好奇心也延伸到了 Resona Lite 和 Rhythm Cook。切换琴键上方的节奏，看看重音的位置变化会带来怎样的效果。"),
     L("Piano and waveform", "钢琴与波形"), (("project-resona-lite", "Resona Lite"), ("project-rhythm", "Rhythm Cook")),
     """           ::      ##
       +++:  :++++#  #++   ++
      /|##||##||#|||##||#|/|
     / |##||##||#|||##||#|/ |
    /__|__||__||_|||__||_|/ /
    '====================='"""),
    ("cubing", L("Cubing", "魔方"), L("Cubing is a chance to take a puzzle apart in my head, one turn at a time.", "玩魔方时，我喜欢在脑海里把一个难题拆成一次次转动。"),
     L("Cubers brings that idea into guided lessons and interactive practice. Here, turn the top layer and rotate the whole cube to see where the pieces went.", "Cubers 把这种思路做成了分步课程和交互练习。在这里，可以转动顶层，再旋转整个魔方，看看方块移到了哪里。"),
     L("3×3 puzzle cube", "三阶魔方"), (("project-cubers", "Cubers"),),
     """            +++
         +++:::+++
      +++:::+++:::+++
      # | # | # | : |
      ==+===+===+---+
      # | # | # | : |
      ==+===+===+---+
      # | # | # | : |
      '---------+---'"""),
)


def topic_sections(lang):
    def t(en, zh):
        return zh if lang == "zh" else en

    def button(action, label, extra=""):
        return f'<button type="button" class="model-key" data-action="{action}"{extra}>{label}</button>'

    rotate = ''.join(button(action, glyph, f' aria-label="{label}"') for action, glyph, label in (
        ('left', '←', t('Rotate left', '向左旋转')), ('right', '→', t('Rotate right', '向右旋转')),
        ('up', '↑', t('Rotate up', '向上旋转')), ('down', '↓', t('Rotate down', '向下旋转')),
    ))
    view = button('view', t('Reset view', '重置视角'))
    motion = button('motion', t('Pause motion', '暂停动效'),
                    f' data-pause="{t("Pause motion", "暂停动效")}" data-play="{t("Play motion", "播放动效")}"')
    actions = {
        'technology': button('signal', t('Send a signal', '发送信号'), f' data-complete="{t("Signal reached the contact.", "信号已到达触点。")}"'),
        'music': button('steady', t('Steady', '均匀节拍'), ' aria-pressed="true"') + button('syncopated', t('Syncopated', '切分节奏'), ' aria-pressed="false"'),
        'cubing': button('turn', t('Turn top layer', '转动顶层'), f' data-complete="{t("Top layer turned.", "顶层已转动。")}"') + button('cube', t('Reset cube', '重置魔方'), f' data-complete="{t("Cube reset.", "魔方已重置。")}"'),
    }
    sections = []
    for key, title, intro, detail, caption, destinations, fallback in TOPICS:
        links = ''.join(f'<li><a href="#{anchor}">{name}{icon("arrow")}</a></li>' for anchor, name in destinations)
        sections.append(f'''<section class="topic-section" id="{key}" aria-labelledby="{key}-heading">
  <div class="container topic-grid">
    <div class="topic-copy"><h2 id="{key}-heading">{title[lang]}</h2><p class="topic-lead">{intro[lang]}</p>
      <p>{detail[lang]}</p><ul class="topic-links">{links}</ul></div>
    <figure class="topic-model" data-model="{key}">
      <div class="model-stage"><pre class="model-fallback" aria-hidden="true">{escape(fallback)}</pre><canvas class="model-canvas" aria-hidden="true" hidden></canvas></div>
      <div class="model-controls" hidden>
        <div class="model-actions" role="group" aria-label="{t('Model actions', '模型操作')}">{actions[key]}</div>
        <div class="model-view" role="group" aria-label="{t('View controls', '视角控制')}"><div class="model-directions">{rotate}</div>{view}{motion}</div>
        <p class="sr-only" role="status"></p>
      </div>
      <figcaption class="model-heading"><span>{caption[lang]}</span><span class="model-hint" hidden>{t('Drag to rotate', '拖动旋转')}</span></figcaption>
    </figure>
  </div>
</section>''')
    return '\n'.join(sections)


def jump_dialog(lang):
    zh = lang == 'zh'
    labels = L(['Home', 'About', 'Selected projects', 'Beyond code', 'Exabyte', 'Project catalog', 'Contact'],
               ['首页', '关于我', '精选项目', '代码之外', 'Exabyte', '项目目录', '联系'])
    sections = list(zip(['top', 'about', 'work', 'beyond', 'exabyte', 'explore', 'connect'], labels[lang]))
    sections[2:2] = [(key, title[lang]) for key, title, *_ in TOPICS]
    sections.extend((f'project-{p["id"]}', p['name']) for p in FEATURES)
    links = ''.join(f'<li><a href="#{anchor}">{escape(title)}{icon("arrow")}</a></li>' for anchor, title in sections)
    title = '跳转到章节' if zh else 'Jump to section'
    return f'''<dialog class="jump-dialog" id="section-jump" aria-labelledby="jump-heading">
  <div class="jump-heading"><h2 id="jump-heading">{title}</h2><button class="model-key jump-close" type="button">{'关闭' if zh else 'Close'}</button></div>
  <label class="search-field">{icon('search')}<span class="sr-only">{'搜索章节' if zh else 'Search sections'}</span><input type="search" placeholder="{'搜索章节或项目' if zh else 'Search sections or projects'}" autocomplete="off" autofocus></label>
  <p class="jump-empty" role="status" hidden>{'没有匹配的章节。' if zh else 'No matching sections.'}</p>
  <ul class="jump-results">{links}</ul>
</dialog>'''


def page(lang):
    c = {key: value[lang] for key, value in COPY.items()}
    zh = lang == "zh"
    prefix, other = ("../", "../") if zh else ("", "zh/")
    nav = ''.join(f'<a href="#{anchor}">{title}</a>' for anchor, title in zip(['about', 'work', 'beyond', 'connect'], c['nav']))
    nav += f'<a href="https://exabyte.org.cn/wecomadd">{c["wechat"]}</a>'
    filters = ''.join(f'<button type="button" class="filter-button {"is-selected" if i == 0 else ""}" data-filter="{key}" aria-pressed="{str(i == 0).lower()}">{name}</button>' for i, (key, name) in enumerate(zip(['all', 'music', 'education', 'tools', 'games', 'community', 'exabyte'], c['categories'])))
    repos = ''
    for p in catalog():
        name, desc = localized(p['name'], lang), localized(p['desc'], lang)
        short = desc.split('. ')[0].rstrip('.') + ('.' if not zh else '')
        repos += f'''<article class="repo-card" id="{p['anchor']}" data-tags="{p['tags']}"><details><summary><span class="repo-name">{escape(name)}</span><span class="repo-description">{escape(short)}</span><span class="details-symbol" aria-hidden="true">+</span></summary><div class="detail-body">{project_details(p.get('detail', p), lang)}{link('https://github.com/'+p['repo'], c['source'], label=name + ': GitHub')}</div></details></article>'''
    life = ''.join(f'<article class="interest-card" id="interest-{kind}"><div class="interest-title">{icon(symbol)}<h3>{title[lang]}</h3></div><p>{desc[lang]}</p></article>' for kind, symbol, title, desc in INTERESTS)
    head = f'''<!doctype html>
<html lang="{'zh-Hans' if zh else 'en'}">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="light"><meta name="theme-color" content="#f8fafc">
<title>{c['title']}</title><meta name="description" content="{escape(c['description'], quote=True)}">
<link rel="canonical" href="{SITE_URL}/{'zh/' if zh else ''}"><link rel="alternate" hreflang="en" href="{SITE_URL}/"><link rel="alternate" hreflang="zh-Hans" href="{SITE_URL}/zh/"><link rel="alternate" hreflang="x-default" href="{SITE_URL}/">
<meta property="og:type" content="website"><meta property="og:title" content="{c['title']}"><meta property="og:description" content="{escape(c['description'], quote=True)}">
<meta property="og:locale" content="{'zh_CN' if zh else 'en_US'}"><meta property="og:locale:alternate" content="{'en_US' if zh else 'zh_CN'}">
<meta property="og:url" content="{SITE_URL}/{'zh/' if zh else ''}"><meta property="og:site_name" content="William Hu"><meta property="og:image" content="{SITE_URL}/assets/social{'-zh' if zh else ''}.png"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:alt" content="{escape(c['intro'], quote=True)}">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{c['title']}"><meta name="twitter:description" content="{escape(c['description'], quote=True)}"><meta name="twitter:image" content="{SITE_URL}/assets/social{'-zh' if zh else ''}.png">
<link rel="icon" href="{prefix}assets/favicon.svg" type="image/svg+xml"><link rel="preload" href="{prefix}assets/fonts/familjen-grotesk-1.ttf" as="font" type="font/ttf" crossorigin><link rel="stylesheet" href="{prefix}assets/style.css">
<script src="{prefix}assets/site.js" defer></script><script src="{prefix}assets/glyph-models.js" defer></script>
</head><body data-language="{lang}">
<a class="skip-link" href="#main">{c['skip']}</a><div class="reading-progress" aria-hidden="true"><span></span></div>
<header class="site-header"><div class="nav-shell container"><a class="wordmark" href="#top" aria-label="William Hu"><span class="brand-mark" aria-hidden="true">W.</span><span>William Hu</span></a>
<nav id="navigation" class="navigation" aria-label="{'主导航' if zh else 'Main navigation'}">{nav}</nav>
<div class="nav-actions"><button class="model-key jump-trigger" type="button" aria-haspopup="dialog" aria-controls="section-jump" aria-label="{'跳转到章节' if zh else 'Jump to section'}" aria-keyshortcuts="Control+K Meta+K" hidden>{icon('search')}<span>{'跳转' if zh else 'Jump'}</span><kbd aria-hidden="true">Ctrl K</kbd></button><a class="language-link" href="{other}" lang="{'en' if zh else 'zh-Hans'}" hreflang="{'en' if zh else 'zh-Hans'}" aria-label="{c['lang']}"><span class="{'muted' if zh else 'current'}">EN</span><span aria-hidden="true"> / </span><span class="{'current' if zh else 'muted'}">中</span></a><button class="menu-toggle" type="button" aria-controls="navigation" aria-expanded="false" aria-label="{c['menu']}" data-open-label="{c['menu']}" data-close-label="{c['close']}" hidden><span></span><span></span></button></div></div></header>
{jump_dialog(lang)}
<main id="main">
<section class="hero" id="top" aria-labelledby="hero-heading"><div class="hero-field" aria-hidden="true"><canvas id="ascii-field"></canvas></div><div class="container hero-inner"><div class="intro-copy"><h1 id="hero-heading">{'你好，我是<br>William。' if zh else 'Hi, I’m<br>William.'}</h1><p class="hero-description">{c['intro']}</p><div class="hero-links"><a class="button button-blue" href="#about">{c['about_cta']}</a><a class="button" href="#work">{c['work_cta']}{icon('arrow')}</a></div></div></div></section>
'''
    body = f'''
<section class="about-section section" id="about" aria-labelledby="about-heading"><div class="container about-grid"><div class="about-copy"><h2 id="about-heading">{c['about_title']}</h2><div class="about-prose"><p>{c['about_text']}</p><p>{c['about_text2']}</p></div></div><aside class="toolkit"><h3>{c['skill_title']}</h3><div class="primary-language"><span class="language-code">Py</span><div><p>Python</p><p class="muted">{c['primary']}</p></div></div><p class="also-label">{c['also']}</p><ul class="language-tags">{''.join(f'<li>{x}</li>' for x in ['JavaScript', 'Swift', 'C++', 'AppleScript', 'HTML & CSS'])}</ul></aside></div></section>
{topic_sections(lang)}
<section class="work-section section" id="work" aria-labelledby="work-heading"><div class="container"><div class="section-heading split-heading"><h2 id="work-heading">{c['work_title']}</h2><p>{c['work_intro']}</p></div><div class="feature-grid">{''.join(feature(p, lang, prefix) for p in FEATURES)}</div><div class="section-tail"><p>{c['music_note']}</p><a class="text-link" href="#explore">{c['all_projects']}{icon('arrow')}</a></div></div></section>
<section class="life-section section" id="beyond" aria-labelledby="life-heading"><div class="container"><div class="section-heading split-heading"><h2 id="life-heading">{c['life_title']}</h2><p>{c['life_intro']}</p></div><div class="interests-grid">{life}</div></div></section>
<section class="organization-section section" id="exabyte" aria-labelledby="org-heading"><div class="container org-grid"><div><h2 id="org-heading">{c['org_title']}</h2><p class="organization-name">Exabyte Technologies</p></div><div class="org-copy"><p>{c['org_text']}</p><p>{c['org_text2']}</p><div class="org-links">{link('https://exabyte.org.cn', c['org_visit'])}{link('https://github.com/Exabyte-Technologies', c['org_github'])}</div></div></div></section>
<section class="directory-section section" id="explore" aria-labelledby="directory-heading"><div class="container"><div class="section-heading split-heading"><h2 id="directory-heading">{c['directory_title']}</h2><p>{c['directory_intro']}</p></div><div class="directory-controls" hidden><label class="search-field">{icon('search')}<span class="sr-only">{c['search_label']}</span><input id="project-search" type="search" placeholder="{c['search']}" autocomplete="off" maxlength="200"></label><div class="filter-list" role="group" aria-label="{c['filters_label']}">{filters}</div></div><p class="result-count" role="status" aria-live="polite" aria-atomic="true" data-template="{c['result']}" data-singular="{c['result_singular']}">{c['result'].replace('{count}', str(len(catalog())))}</p><div class="repo-grid">{repos}</div><div class="empty-state" hidden><h3>{c['empty_title']}</h3><p>{c['empty_text']}</p><button class="button reset-search" type="button">{c['reset']}</button></div></div></section>
<section class="contact-section section" id="connect" aria-labelledby="contact-heading"><div class="container contact-grid"><h2 id="contact-heading">{c['contact_title']}</h2><div><p>{c['contact_text']}</p><a class="email-link" href="mailto:jingwen.hu@exabyte.org.cn" aria-label="{c['email']}: jingwen.hu@exabyte.org.cn">jingwen.hu@exabyte.org.cn</a><div class="contact-socials">{link('https://github.com/hujingwen1025', 'GitHub', 'text-link', 'github')}{link('https://github.com/Exabyte-Technologies', 'Exabyte Technologies')}{link('https://exabyte.org.cn/wecomadd', c['wechat'])}</div></div></div></section>
</main><footer class="site-footer container"><div><a class="footer-name" href="#top">William Hu.</a><p>{c['footer']}</p></div><a href="#top" class="back-top">{c['back']}{icon('arrow')}</a></footer></body></html>'''
    return head + body


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
    write_error_pages(PUBLIC, SITE_URL)
    sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
    for suffix in ("/", "/zh/"):
        sitemap += f'<url><loc>{escape(SITE_URL + suffix)}</loc><xhtml:link rel="alternate" hreflang="en" href="{escape(SITE_URL)}/"/><xhtml:link rel="alternate" hreflang="zh-Hans" href="{escape(SITE_URL)}/zh/"/></url>\n'
    (PUBLIC / "sitemap.xml").write_text(sitemap + "</urlset>\n", encoding="utf-8")
    (PUBLIC / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {SITE_URL}/sitemap.xml\n", encoding="utf-8")
    print(f"Built 2 languages, {len(FEATURES)} featured projects, {len(catalog())} catalog projects, and 8 error pages.")
