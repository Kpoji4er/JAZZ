# Rewrite squad-role-icons.md paths after Enemy/ subfolder reorg.
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
p = ROOT / "docs" / "technical" / "systems" / "squad-role-icons.md"
t = p.read_text(encoding="utf-8")

for name in ("legion", "army", "adonis", "rebels", "smugglers"):
    t = t.replace(f"SquadsIcons/Enemy/{name}.png", f"SquadsIcons/Enemy/_shields/{name}.png")

factions = ("legion", "army", "adonis", "rebels", "smugglers")
roles = (
    "BASE",
    "GARRISON",
    "PATROL",
    "RECON",
    "QRF",
    "SUPPLY",
    "SHIPMENT",
    "REINFORCE",
    "SUPPORT",
    "RETRIBUTION",
    "RECRUITER",
    "MANPOWER",
    "TAX",
)
for f in factions:
    for r in roles:
        old = f"SquadsIcons/Enemy/{f}_{r}_squad.png"
        new = f"SquadsIcons/Enemy/{f}/{f}_{r}_squad.png"
        t = t.replace(old, new)

t = t.replace(
    "Mod/e6L4ECj/SquadsIcons/Enemy/<file>.png",
    "Mod/e6L4ECj/SquadsIcons/Enemy/<faction>/<faction>_<ROLE>_squad.png",
)

old_extra = (
    "Доп. варианты щитов (не ролевые): `army2.png`, `army3.png`, `rebels2.png`, "
    "`rebels3.png`, `enemy_squad.png`, `nazi.png`."
)
new_extra = (
    "Доп. варианты щитов (не ролевые): `_shields/army2.png`, `_shields/army3.png`, "
    "`_shields/rebels2.png`, `_shields/rebels3.png`; прочее: `_misc/enemy_squad.png`, `_misc/nazi.png`."
)
t = t.replace(old_extra, new_extra)

needle = "Ассеты: [`SquadsIcons/Enemy/`](../../../SquadsIcons/Enemy/)"
note = (
    needle
    + "\n\nРаскладка: `_shields/` (пустые щиты), `<faction>/` (ролевые PNG), `_misc/` (прочее)."
)
if "Раскладка:" not in t:
    t = t.replace(needle, note)

# Filename convention line
t = t.replace(
    "Имена файлов: `<faction>_<ROLE>_squad.png`",
    "Имена файлов: `<faction>/<faction>_<ROLE>_squad.png`",
)

p.write_text(t, encoding="utf-8")
print(f"OK {p.relative_to(ROOT).as_posix()}")
