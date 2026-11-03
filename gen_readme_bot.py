import os
import sys

os.environ.setdefault("NIK_TOKEN", "1:X")
sys.path.insert(0, "/home/user/repo")
import NikBot as U  # noqa: E402

cats = U._by_cat()
L = []
L.append("## 🤖 MAIN BOT — `NikBot.py` (single file)\n")
L.append("Ek zip: **userbot** (`Nik_userbot.py`, %d cmds) + **main bot** (`NikBot.py`, %d cmds)."
         % (278, len(U.COMMANDS)))
L.append("Token/owner file ke top pe ya `nik_config.json` me — koi `.env` nahi.\n")

L.append("### ⚙️ Config — sirf 3 line\n")
L.append("```python")
L.append("# NikBot.py ke top pe (line ~95):")
L.append('TOKEN     = "123456:ABC..."     # @BotFather se')
L.append("OWNER_ID  = 123456789           # tera id")
L.append("SUDO_IDS  = [111, 222]          # optional")
L.append("```")
L.append("Ya file edit kiye bina — `nik_config.json` (same folder):\n")
L.append("```json")
L.append('{"token": "123456:ABC...", "owner_id": 123456789, "sudo_ids": [111]}')
L.append("```")
L.append("Ya env: `NIK_TOKEN`, `NIK_OWNER`, `NIK_SUDO`, `NIK_PREMIUM`, `NIK_RICH`.")
L.append("Priority → **env > nik_config.json > file ki value**. Andar se check: `.config`\n")

L.append("### 🧾 Request log (kahnakimkb jaisa smart CLI)\n")
L.append("Har command ka ek hi line — stdout + `nik_data/logs/nikbot.log`:\n")
L.append("```")
L.append("[REQ 0042] ✓ ping         │   18.4ms │ u:777 Nik            │ c:-100123 grup · ok")
L.append("```")
L.append("`.reqlog` → last N + avg/slowest latency. `--check` → self test.\n")

L.append("### Prefix engine\n")
L.append("| Input | Kya hota hai |")
L.append("|---|---|")
L.append("| `•ping` `.ping` `/ping` `!ping` | chaaro chalte hain |")
L.append("| `.prefix off` | `ping` · `Ping` · `PING` bina prefix |")
L.append("| `.prefix set •.!` | custom |")
L.append("| `pign` → `ping` | typo bhi chal jata hai |\n")

L.append("### Bot profile — sab bots par ek saath\n")
L.append("| Cmd | Method |")
L.append("|---|---|")
L.append("| `.setname Nik Bot` | `setMyName` |")
L.append("| `.setdesc …` | `setMyDescription` |")
L.append("| `.setshortdesc …` | `setMyShortDescription` |")
L.append("| `.setpfp` (photo reply) | `setMyProfilePhoto` |")
L.append("| `.delpfp` | photo remove |")
L.append("| `.nameloop 30 \\| Nik \\| NIK` | auto-rotate |\n")

L.append("### Games (button wale)\n")
L.append("`.ttt` 2-player grid · `.quiz` 4 options · `.hangman` letter guess · "
         "`.emojirain` animation · `.slots` · `.8ball` · `.ship` · `.rps` · `.dice/.dart/.bowl`\n")

L.append("### Commands (%d) — category wise\n" % len(U.COMMANDS))
L.append("| Category | Cmds | Commands |")
L.append("|---|---|---|")
for key in U.MENU_ORDER:
    cmds = cats.get(key, [])
    if not cmds:
        continue
    L.append("| %s | %d | %s |" % (U.CATEGORIES.get(key, key), len(cmds),
                                   " ".join("`%s`" % c.name for c in cmds)))
L.append("")

open("/tmp/readme_bot.md", "w", encoding="utf-8").write("\n".join(L))
print("ok lines:", len(L), "| cmds:", len(U.COMMANDS))
