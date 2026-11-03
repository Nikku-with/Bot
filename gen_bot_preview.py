#!/usr/bin/env python3
"""NikBot ka visual preview — asli functions se HTML."""
import html
import os
import sys

os.environ.setdefault("NIK_TOKEN", "1:PREVIEW")
sys.path.insert(0, "/home/user/repo")
import NikBot as U  # noqa: E402

CSS = """
*{box-sizing:border-box}
body{margin:0;background:#0c131b;color:#dfe9f3;font-family:-apple-system,'Segoe UI',Roboto,sans-serif}
.wrap{max-width:980px;margin:0 auto;padding:26px 18px 60px}
h1{font-size:30px;margin:0 0 4px;letter-spacing:.5px}
.sub{color:#7c93aa;font-size:14px;margin-bottom:22px}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:16px}
@media(max-width:760px){.grid{grid-template-columns:1fr}}
.card{background:#131d28;border:1px solid #22303f;border-radius:16px;padding:6px 8px;
      font-size:15px;line-height:1.65;white-space:pre-wrap;word-break:break-word;
      box-shadow:0 10px 24px rgba(0,0,0,.35)}
.card b{color:#fff}
.card .lbl{color:#6c8299;font-size:12.5px;padding:4px 8px 0}
.card code{background:#0d1620;border:1px solid #22303f;border-radius:6px;padding:1px 6px;
           color:#a8e6c0;font-family:ui-monospace,Menlo,monospace;font-size:13px}
.card i{color:#93a7bb}
.card tg-emoji{font-style:normal}
.badge{display:inline-block;background:#1b3348;color:#6fb7ff;border-radius:99px;
       padding:2px 10px;font-size:12px;margin-right:6px;margin-bottom:10px}
.strip{display:flex;gap:10px;flex-wrap:wrap;margin:6px 0 20px}
.frame{background:#101a24;border:1px solid #22303f;border-radius:12px;padding:8px 12px;
       font-family:ui-monospace,Menlo,monospace;font-size:13px;color:#8ee6b8;white-space:pre}
.tbl{width:100%;border-collapse:collapse;font-size:14px;margin:8px 0 22px}
.tbl td,.tbl th{border-bottom:1px solid #1e2b39;padding:7px 8px;text-align:left}
.tbl th{color:#7c93aa;font-weight:600;font-size:12.5px;text-transform:uppercase;letter-spacing:.6px}
.dot{color:#54d68a}
.no{color:#ff7b7b}
footer{color:#54697e;font-size:13px;margin-top:28px;text-align:center}
"""


def card(title, body, cls=""):
    return ("<div class='lbl'>%s</div><div class='card %s'>%s</div>"
            % (title, cls, body))


def main() -> None:
    parts = ["<div class='wrap'>",
             "<h1>⚡ NIK BOT <span style='color:#54d68a'>·</span> v1.0</h1>",
             "<div class='sub'>single-file main bot · %d commands · %d categories · "
             "rich ↔ plain dual UI · premium emoji · cluster mode</div>"
             % (len(U.COMMANDS), len(U.CATEGORIES))]

    parts.append("<span class='badge'>rich card</span>"
                 "<span class='badge'>plain fallback</span>"
                 "<span class='badge'>prefix engine</span>"
                 "<span class='badge'>10-20 bots = 1 reply</span>"
                 "<span class='badge'>entry animations</span>")

    # animation strip
    parts.append("<h3 style='color:#9fb6cc;font-size:15px;margin:18px 0 6px'>entry animation (hy)</h3>")
    parts.append("<div class='strip'>")
    for fr in ["⚡", "⚡ ✨", "〔 ⚡ ✨ 〕", "〔 ⚡ ✨ 〕 " + U.smallcaps("nik bot online")]:
        parts.append("<div class='frame'>%s</div>" % html.escape(fr))
    parts.append("</div>")

    parts.append("<h3 style='color:#9fb6cc;font-size:15px;margin:6px 0 6px'>loader (song)</h3>")
    parts.append("<div class='strip'>")
    for ph, pct in (("search", 24), ("fetch", 58), ("send", 92)):
        parts.append("<div class='frame'>%s</div>"
                     % html.escape(U.load_card(ph, "kesariya", 3, pct)))
    parts.append("</div>")

    parts.append("<div class='grid'>")
    parts.append(card("menu · page 1/2", U.build_menu_page(0)))
    parts.append(card("menu · page 2/2", U.build_menu_page(1)))
    parts.append(card("category · fun", U.build_category("fun")))
    parts.append(card("start · welcome", U.card("ɴɪᴋ ʙᴏᴛ", [
        ("welcome", ["👤 <b>Nik</b>", "🆔 <code>777</code>",
                     "💠 " + U.smallcaps("owner") + " · @Nikkkwa"]),
        ("quick", ["<code>%smenu</code> · full panel" % U.prefixes()[0],
                   "<code>%shelp</code> · command detail" % U.prefixes()[0],
                   "<code>%sping</code> · speed check" % U.prefixes()[0]])],
        footer="ᴘᴏᴡᴇʀᴇᴅ ʙʏ @Nikkkwa", icon="⚡")))
    parts.append("</div>")

    # prefix table
    parts.append("<h3 style='color:#9fb6cc;font-size:15px;margin:26px 0 6px'>prefix engine</h3>")
    rows = [("•ping", "• dot prefix", "yes"),
            (".ping", ". dot prefix", "yes"),
            ("/ping", "/ slash", "yes"),
            ("ping · Ping · PING", "bina prefix (prefix off)", "yes"),
            ("p → ping", "alias", "yes"),
            ("pign → ping", "typo bhi chal jaye", "yes"),
            ("hello dosto", "normal chat — ignore", "no")]
    parts.append("<table class='tbl'><tr><th>input</th><th>matlab</th><th>chalti hai</th></tr>")
    for a, b, ok in rows:
        parts.append("<tr><td><code>%s</code></td><td>%s</td><td class='%s'>%s</td></tr>"
                     % (html.escape(a), b, "dot" if ok == "yes" else "no",
                        "✔" if ok == "yes" else "—"))
    parts.append("</table>")

    # categories
    parts.append("<h3 style='color:#9fb6cc;font-size:15px;margin:6px 0 6px'>categories</h3>")
    cats = U._by_cat()
    parts.append("<table class='tbl'><tr><th>category</th><th>cmds</th><th>examples</th></tr>")
    for key in U.MENU_ORDER:
        cmds = cats.get(key, [])
        if not cmds:
            continue
        ex = ", ".join(c.name for c in cmds[:7])
        parts.append("<tr><td>%s</td><td>%d</td><td><code>%s</code></td></tr>"
                     % (html.escape(U.CATEGORIES.get(key, key)), len(cmds), html.escape(ex)))
    parts.append("</table>")

    parts.append("<footer>ᴘᴏᴡᴇʀᴇᴅ ʙʏ @Nikkkwa · Nik Bot v1.0</footer></div>")
    out = ("<!doctype html><html><head><meta charset='utf-8'>"
           "<title>Nik Bot — preview</title><style>%s</style></head><body>%s</body></html>"
           % (CSS, "\n".join(parts)))
    open("/home/user/repo/bot_preview.html", "w", encoding="utf-8").write(out)
    print("bot_preview.html written")


main()
