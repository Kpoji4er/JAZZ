# -*- coding: utf-8 -*-
"""Generate Legion line-troop weapon availability map by JAZZ_Legion_Tier from weapons.csv."""
from __future__ import annotations

import csv
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CSV = ROOT / "docs/technical/weapons/data/weapons.csv"
OUT = ROOT / "docs/design/legion-weapon-availability-by-tier.md"

# Family tags for gossip (object_class → bucket)
BUCKET = {
    "Pistol": "Пистолеты / револьверы",
    "Revolver": "Пистолеты / револьверы",
    "SubmachineGun": "ПП",
    "AssaultRifle": "Штурмовые",
    "AssaultRifle_ShortBarrel": "Штурмовые",
    "BattleRifle": "Боевые винтовки",
    "Rifle": "Винтовки",
    "SniperRifle": "Снайперские",
    "MachineGun": "Пулемёты",
    "Shotgun": "Дробовики",
    "Carbine": "Карабины",
}


def main():
    by = defaultdict(lambda: defaultdict(list))
    with CSV.open(encoding="utf-8", newline="") as f:
        for r in csv.DictReader(f):
            tl = (r.get("tier_label") or "").strip()
            if "-" not in tl:
                continue
            a, b = tl.split("-", 1)
            if not (a.isdigit() and b.isdigit()):
                continue
            key = int(a) * 10 + int(b)
            if key not in (11, 12, 13, 21, 22, 23, 24, 25, 31, 32, 33):
                continue
            wid = (r.get("id") or "").strip()
            name = (r.get("display_name") or wid).strip()
            oc = (r.get("object_class") or "").strip()
            bucket = BUCKET.get(oc, oc or "Прочее")
            by[key][bucket].append(f"`{wid}` ({name})" if name != wid else f"`{wid}`")

    lines = [
        "# Legion weapon availability by equipment tier",
        "",
        "Design + R.I.S. copy checklist. **Line troops only** (Assault / Front / Flanker / Gunner / Heavy).",
        "Elites and sergeants/leaders use the same primary pools filtered by role tags, but R.I.S. supply briefs talk about the **new unlock band**, not named elites.",
        "",
        "Source: `docs/technical/weapons/data/weapons.csv` `tier_label` (`X-Y` → Amount `XY`).",
        "Runtime arch bands: **11–13** = arch1; **21–25** = arch2 (+ ~1% arch1 remnant); **31–33** = arch3 only.",
        "Heavy launchers (`RPG7`/`M72LAW`, `M79`, mortar) are **not** laddered by `tier_label` — fixed LootDefs.",
        "",
        "Generator: `docs/tools/_gen_legion_weapon_availability_map.py`.",
        "Briefs: `docs/design/ris-legion-tier-briefs.md` + `docs/tools/_rewrite_ris_legion_briefs.py`.",
        "",
    ]
    for key in sorted(by):
        arch, sub = divmod(key, 10)
        lines.append(f"## Tier {key} (arch {arch}-{sub})")
        lines.append("")
        for bucket in sorted(by[key]):
            items = ", ".join(by[key][bucket])
            lines.append(f"- **{bucket}:** {items}")
        lines.append("")

    OUT.write_text("\n".join(lines), encoding="utf-8")
    print("wrote", OUT, "tiers", sorted(by))


if __name__ == "__main__":
    main()
