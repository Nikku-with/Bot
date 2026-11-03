# NikBot — architecture (padhne ke liye, 5 min)

Ek file, 24 sections. Neeche har section ka kaam aur "kahan hai" — file me
section numbers `# 01 ·` ... `# 24 ·` se marked hain.

```
01 CONFIG        TOKEN · OWNER_ID · SUDO_IDS · nik_config.json loader · paths
02 STORAGE       Store() class — nik_data/nikbot.json (atomic write)
03 EMOJI         EMOJI_IDS — 324 premium emoji document ids (tere packs se)
04 STYLE         smallcaps · fancy · zalgo · bar · SPIN · load_card · card/hbox
05 ANIMATION     animate() · progress_bar() · ANIM_HY/LOAD/WAVE
06 TG LAYER      raw_api() · rich_blocks() · send_card() · say() · kb()
07 REGISTRY      @cmd(...) · ALIAS · resolve() (alias + typo)
07b CLUSTER      claim_once() — 10-20 bots, ek hi jawab
07c REQLOG       reqlog() — [REQ 0042] ✓ ping 18.4ms · u:777 · c:grup
08 ROUTER        router() · cb_router() — ek handler, saare commands
09 MENUS         menu pages · category cards · menu_kb()
10 CORE          start · menu · help · ping · id · whois · prefix · sudo ...
11 PROFILE       setname / setdesc / setshortdesc / setpfp / delpfp / loops
12 BOT MANAGER   addtoken · tokens · bots · check (token pool)
13 HOSTER        upload · run · apps · stopapp · applog · pip · sh
14 GROUP ADMIN   ban · kick · mute · warn · purge · pin · promote · lock ...
15 PROTECTION    antilink · antiflood · welcome · captcha · autoreact
16 NOTES         save/get/notes/clear · filters
17 GUARD         har group msg par: filter · antilink · antiflood · react
18 FUN · 18b     8ball · dice · rps · ship · slots · TTT · quiz · hangman · emojirain
19 UTILITY       calc · hash · qr · morse · weather · wiki · translate · tts ...
20 MEDIA         song/video (yt-dlp) · lyrics · sticker · toimg · topdf
21 ANIMATIONS    hy · gm · gn · love · slap · dance ... + custom .anim
22 AI            ai (text) · imagine (image) · define · summarize
23 GLOBAL        gban · ungban · gbanlist · blacklist
24 RUNNER        build_app() · health server · on_error · --check
```

## Design rules (ye kabhi nahi tootni chahiye)

1. **Ek command = ek jawab.** Cluster claim + cooldown.
2. **Rich fail → plain.** Kabhi khaali message nahi. 3 fail ke baad rich off.
3. **Koi khali block nahi.** Ek row wali table → paragraph/quote.
4. **Font/emoji consistent** — `smallcaps()` headings, `mono()` commands.
5. **Owner-only cheezein** (`.sh`, `.restart`, `.setname`) — sirf OWNER_ID/SILENT_OWNER.

## Multi-bot kaise chalta hai

* `.addtoken` → token pool me add (getMe se validate).
* `.setname` / `.setpfp` / `.nameloop` → **pool ke har bot** par apply.
* Ek hi command par ek hi bot jawab de — `claim_once()` `nik_data/claims/*.lock`
  par `os.O_EXCL` se atomic claim karta hai (TTL 1.6s).
* `.cluster off` → saare bots jawab denge (debug ke liye).

## Naya command add karna (10 second)

```python
@cmd("hello", aliases=("hl",), cat="fun", desc="hello bolta hai", usage="hello <name>")
async def c_hello(update, ctx, args):
    await say(update, "👋 hi <b>%s</b>" % esc(args or "dost"))
```

Bas. Menu, help, page count — sab automatic (registry se banta hai).

## Config (3 jagah se aa sakta hai)

1. `NikBot.py` top pe `TOKEN` / `OWNER_ID` / `SUDO_IDS`
2. `nik_config.json` (same folder) — `{"token": "...", "owner_id": 0, "sudo_ids": []}`
3. env — `NIK_TOKEN`, `NIK_OWNER`, `NIK_SUDO`, `NIK_PREMIUM`, `NIK_RICH`

Priority: env > json > file. Andar se status: `.config`.
Runtime tweak: `.setvar cluster off|on` · `prefix` · `premium` · `rich` · `maxwarn`.

## Version support

| Cheez | Support |
|---|---|
| python | 3.10 → 3.14 (Termux tested) |
| PTB | **21.6 aur 22.8 dono** — `_patch_tg_kwargs()` jo kwarg us version me nahi hai, chup-chaap hata deta hai |
| Defaults | 21.x `telegram.Defaults`, 22.x `telegram.ext.Defaults` — auto-detect |
| slowmode | 21.x `set_chat_slow_mode_delay`, 22.x raw `setChatSlowModeDelay` |

Pehli baar chalane se pehle: `python NikBot.py --doctor` — python/PTB/token/packages/internet
sab ek table me. Kuch missing ho to wahi line bata degi.

## Test

```bash
python NikBot.py --check          # 183 commands, 13 categories, meta check
python audit/test_bot.py          # 56/56 — prefix, alias, typo, cluster, menu, cards
```
