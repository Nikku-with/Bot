# -*- coding: utf-8 -*-
"""Rich UI preview — actual blocks se Telegram-jaisa HTML render."""
import os, sys, html
sys.path.insert(0, "/home/user/repo")
os.environ.setdefault("API_ID", "1")
os.environ.setdefault("API_HASH", "0123456789abcdef0123456789abcdef")
os.environ.setdefault("OWNER_ID", "1")
import Nik_userbot as U
from telethon.tl import types


def flat(rt):
    return U._rt_flat(rt) if rt is not None else ""


def render_text(rt, accent=""):
    """RichText → html (premium emoji ko chip ki tarah dikhao)."""
    out, t = [], type(rt)
    if rt is None:
        return ""
    if t is types.TextPlain:
        return html.escape(rt.text)
    if t is types.TextEmpty:
        return ""
    if t is types.TextConcat:
        return "".join(render_text(x) for x in rt.texts)
    if t is types.TextCustomEmoji:
        return '<span class="emo">%s</span>' % html.escape(rt.alt)
    if t is types.TextBold:
        return "<b>%s</b>" % render_text(rt.text)
    if t is types.TextItalic:
        return "<i>%s</i>" % render_text(rt.text)
    if t is types.TextStrike:
        return "<s>%s</s>" % render_text(rt.text)
    if t is types.TextUnderline:
        return "<u>%s</u>" % render_text(rt.text)
    if t is types.TextSpoiler:
        return '<span class="sp">%s</span>' % render_text(rt.text)
    if t is types.TextFixed:
        return "<code>%s</code>" % render_text(rt.text)
    if t is types.TextUrl:
        return '<a href="%s">%s</a>' % (html.escape(rt.url), render_text(rt.text))
    if t is types.TextMath:
        return "<code>%s</code>" % html.escape(rt.source)
    inner = getattr(rt, "text", None)
    return render_text(inner) if inner is not None else ""


def render_blocks(blocks):
    out = []
    for b in blocks:
        n = type(b).__name__
        if n in ("PageBlockTitle", "PageBlockHeading1"):
            out.append('<h1>%s</h1>' % render_text(b.text))
        elif n == "PageBlockKicker":
            out.append('<div class="kick">%s</div>' % render_text(b.text))
        elif n == "PageBlockSubtitle":
            out.append('<div class="subtitle">%s</div>' % render_text(b.text))
        elif n in ("PageBlockHeader", "PageBlockSubheader"):
            out.append('<h3 class="hdr">%s</h3>' % render_text(b.text))
        elif n.startswith("PageBlockHeading") and n != "PageBlockHeading1":
            lvl = int(n[-1])
            size = {1: 26, 2: 22, 3: 19, 4: 17, 5: 16, 6: 15}[lvl]
            out.append('<div class="head" style="font-size:%dpx">%s</div>'
                       % (size, render_text(b.text)))
        elif n == "PageBlockParagraph":
            out.append('<p>%s</p>' % render_text(b.text))
        elif n == "PageBlockDivider":
            out.append('<hr>')
        elif n == "PageBlockMath":
            out.append('<div class="math">%s</div>' % html.escape(b.source))
        elif n == "PageBlockPreformatted":
            out.append('<pre>%s</pre>' % html.escape(flat(b.text)))
        elif n == "PageBlockBlockquote":
            out.append('<blockquote>%s</blockquote>' % render_text(b.text))
        elif n == "PageBlockPullquote":
            out.append('<div class="pull">%s</div>' % render_text(b.text))
        elif n == "PageBlockDetails":
            out.append('<details><summary>%s</summary>%s</details>'
                       % (render_text(b.title), render_blocks(b.blocks)))
        elif n == "PageBlockList":
            items = []
            for it in b.items:
                box = ('<span class="cb">✔</span>' if getattr(it, "checked", None)
                       else '<span class="cb">☐</span>') if getattr(it, "checkbox", None) else "•"
                items.append("<li>%s %s</li>" % (box, render_text(getattr(it, "text", None))))
            out.append("<ul>%s</ul>" % "".join(items))
        elif n == "PageBlockOrderedList":
            items = []
            for k, it in enumerate(b.items, 1):
                items.append("<li>%s. %s</li>" % (getattr(it, "num", None) or k,
                                                  render_text(getattr(it, "text", None))))
            out.append('<ol class="plain">%s</ol>' % "".join(items))
        elif n == "PageBlockTable":
            rows = []
            for r in b.rows:
                cells = []
                for c in r.cells:
                    cls = "th" if getattr(c, "header", None) else "td"
                    st = []
                    if getattr(c, "align_center", None):
                        st.append("text-align:center")
                    if getattr(c, "align_right", None):
                        st.append("text-align:right")
                    if getattr(c, "colspan", None):
                        st.append("grid-column:span %d" % c.colspan)
                    cells.append('<div class="cell %s" style="%s">%s</div>'
                                 % (cls, ";".join(st), render_text(c.text)))
                rows.append('<div class="row">%s</div>' % "".join(cells))
            out.append('<div class="table%s">%s</div>'
                       % (" striped" if getattr(b, "striped", None) else "", "".join(rows)))
        elif n == "PageBlockButtonRow":
            btns = []
            for btn in b.buttons:
                style = getattr(btn, "style", None)
                cls = "b-blue"
                if style is not None:
                    if getattr(style, "bg_danger", None):
                        cls = "b-red"
                    elif getattr(style, "bg_success", None):
                        cls = "b-green"
                    elif getattr(style, "link", None):
                        cls = "b-link"
                btns.append('<div class="btn %s">%s</div>' % (cls, render_text(btn.text)))
            out.append('<div class="btns">%s</div>' % "".join(btns))
        elif n in ("PageBlockPhoto", "PageBlockVideo", "PageBlockAudio", "PageBlockDocument"):
            icon = {"PageBlockPhoto": "🖼", "PageBlockVideo": "🎬",
                    "PageBlockAudio": "🎵", "PageBlockDocument": "📄"}[n]
            cap = getattr(getattr(b, "caption", None), "text", None)
            out.append('<div class="media">%s <span>%s</span></div>'
                       % (icon, render_text(cap) if cap is not None else n))
        elif n == "PageBlockThinking":
            out.append('<div class="think">%s</div>' % render_text(b.text))
        elif n == "PageBlockFooter":
            out.append('<div class="foot">%s</div>' % render_text(b.text))
    return "\n".join(out)


def page(name, text, subtitle=""):
    docs = set()
    blocks = U._ui_blocks(text, docs)
    row = U._ui_buttons(text, docs)
    if row is not None:
        if blocks and type(blocks[-1]).__name__ == "PageBlockDivider":
            blocks = blocks[:-1] + [row]
        else:
            blocks = blocks + [row]
    return ('<section class="card"><div class="chatname">%s</div>%s</section>'
            % (html.escape(name), render_blocks(blocks)))


CSS = """
*{box-sizing:border-box}
body{margin:0;padding:28px 16px 60px;background:#0e1621;
     font-family:-apple-system,'Segoe UI',Roboto,sans-serif;color:#e9edf2}
.wrap{max-width:620px;margin:0 auto}
.note{background:#17212b;border:1px solid #24313d;border-radius:12px;
      padding:12px 16px;margin-bottom:18px;color:#8fa3b8;font-size:13px;line-height:1.55}
.note b{color:#62a9e8}
.card{background:#17212b;border-radius:14px;padding:18px 20px 20px;
      margin:16px 0;box-shadow:0 2px 14px rgba(0,0,0,.35)}
.chatname{font-size:11px;color:#5f7488;letter-spacing:.12em;
          text-transform:uppercase;margin-bottom:10px}
h1{font-size:27px;font-weight:800;margin:2px 0 14px;line-height:1.25;
   letter-spacing:-.01em}
.head{font-weight:700;margin:18px 0 8px;color:#fff}
.hdr{font-size:15px;font-weight:700;margin:14px 0 6px;color:#dbe6f0}
.kick{font-size:12px;letter-spacing:.18em;text-transform:uppercase;
      color:#62a9e8;font-weight:700;margin-bottom:6px}
.subtitle{font-size:17px;color:#9fb2c6;margin:-6px 0 14px}
p{margin:9px 0;line-height:1.62;font-size:15px;color:#c9d6e3}
hr{border:0;border-top:1px solid #24313d;margin:18px 0}
.table{border:1px solid #2b3a48;border-radius:10px;overflow:hidden;margin:12px 0}
.row{display:grid;grid-template-columns:1fr 1fr;border-bottom:1px solid #223040}
.row:last-child{border-bottom:0}
.striped .row:nth-child(even){background:#1b2733}
.cell{padding:9px 12px;font-size:14px;color:#c2d0de;border-right:1px solid #223040;
      overflow-wrap:anywhere}
.cell:last-child{border-right:0}
.cell.th{background:#1e2c3a;font-weight:700;color:#eaf2fa}
.btns{display:flex;flex-direction:column;gap:8px;margin-top:16px}
.btn{text-align:center;padding:11px 14px;border-radius:22px;font-weight:700;
     font-size:15px;letter-spacing:.02em}
.b-blue{background:#3390ec;color:#fff}
.b-green{background:#2f7d4f;color:#e8fff2}
.b-red{background:#7d3a37;color:#ffe9e7}
.b-link{background:transparent;color:#62a9e8;border:1px solid #2b3a48}
blockquote{margin:10px 0;padding:10px 14px;border-left:3px solid #3ea6ff;
           background:#182432;border-radius:0 8px 8px 0;color:#c05cf0;
           font-size:15px;line-height:1.72}
.pull{margin:12px 0;padding:12px 16px;border-left:4px solid #62a9e8;
      font-size:17px;font-style:italic;color:#dce8f3}
pre{background:#0f1922;border:1px solid #223040;border-radius:10px;padding:12px;
    overflow:auto;font-size:13px;color:#a9e0b6}
code{background:#223040;padding:1px 6px;border-radius:5px;font-size:13px;color:#ffd28a}
.math{background:#0f1922;border:1px solid #223040;border-radius:8px;
      padding:10px 14px;font-family:monospace;color:#9fd4ff;margin:10px 0}
ul,ol{margin:10px 0;padding-left:22px;line-height:1.75;color:#c9d6e3}
ol.plain{list-style:none;padding-left:0}
.cb{color:#5ad07a;font-size:14px}
details{margin:12px 0;background:#1b2733;border:1px solid #24313d;
        border-radius:10px;padding:10px 14px}
summary{cursor:pointer;font-weight:700;color:#9fd4ff}
a{color:#62a9e8}
.media{display:flex;align-items:center;gap:10px;background:#0f1922;
       border:1px solid #223040;border-radius:12px;padding:14px;margin:12px 0;
       font-size:14px;color:#8fa3b8}
.emo{font-size:1.15em;filter:saturate(1.2)}
.think{background:#1b2733;border-left:3px solid #7a5cff;padding:10px 14px;
       border-radius:0 8px 8px 0;color:#b9aaff;font-style:italic}
.foot{color:#6b8098;font-size:13px;margin-top:10px}\npre{background:#1b2733;border:1px solid #2b3a48;border-radius:8px;\n    padding:9px 12px;font-size:13.5px;color:#a8e6c0;overflow-x:auto;\n    font-family:ui-monospace,Menlo,monospace;margin:7px 0}
"""


def build():
    parts = [
        '<div class="wrap">',
        '<div class="note">Ye <b>asli generated blocks</b> ka render hai — jo '
        'Telegram me article ke roop me dikhega (wahi blocks, wahi emoji, wahi buttons). '
        'Premium account hone par bot ka har card aisa aayega.</div>',
        page("। .menu  (page 1/4)", U.MENU_PAGES[0]),
        page("। .m24  (voice chat)", U.build_vc_menu()),
        page("। .m6  (group mod)", U.build_category_menu(5)),
        page("। .menu  (index · saare pages)", U.build_menu_index()),
        page("। .help music  (code block + headings)", U.guide_music()),
        page("। .addbot  (login flow)", U.guide_addbot()),
    ]
    parts.append("</div>")
    return ("<!doctype html><html><head><meta charset='utf-8'>"
            "<title>Nik Userbot — article UI</title><style>%s</style></head>"
            "<body>%s</body></html>" % (CSS, "\n".join(parts)))


open("/home/user/repo/ui_preview.html", "w", encoding="utf-8").write(build())
print("ui_preview.html written")
