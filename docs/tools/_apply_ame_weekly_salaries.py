# Apply AME StartingSalary from owner weekly bands (JA3 week ~= StartingSalary * 7).
# Irregular floor ~50/wk; typical ~100-1000; specialists max ~2000/wk; specialists < Igor/Barry weekly.
from __future__ import annotations

import re
from pathlib import Path

UNITS = Path(r"C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz-units\UnitData")
ITEMS = Path(r"C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz-units\items.lua")

# Weekly targets -> StartingSalary = round(weekly / 7)
# Irregulars: 50-350/wk -> 7-50
# Fighters:   400-750/wk -> 57-107
# Hardened:   750-1000/wk -> 107-143
# Specialists by role up to 2000/wk -> <=286; ceiling below Igor(450)/Barry(470)

TIER_WEEKLY = {
    "Irregulars": (50, 350),
    "Fighters": (400, 750),
    "Hardened": (750, 1000),
}

SPEC_WEEKLY = {
    "Mechanic": (1100, 1400),
    "Sapper": (1200, 1500),
    "Sniper": (1400, 1700),
    "Medic": (1500, 1800),
    "Instructor": (1700, 2000),
}

IGOR_DAILY = 450
BARRY_DAILY = 470
SPEC_CEILING_DAILY = min(IGOR_DAILY, BARRY_DAILY) - 1  # 449


def weekly_to_daily(w: int) -> int:
    return max(1, int(round(w / 7)))


def lerp(a: float, b: float, t: float) -> float:
    return a + (b - a) * t


def parse_field(text: str, name: str):
    m = re.search(rf'{name}\s*=\s*"([^"]+)"', text)
    return m.group(1) if m else None


def parse_salary(text: str):
    m = re.search(r"StartingSalary\s*=\s*(\d+)", text)
    return int(m.group(1)) if m else None


def set_salary(text: str, value: int) -> str:
    return re.sub(r"StartingSalary\s*=\s*\d+", f"StartingSalary = {value}", text, count=1)


def tier_salaries(ids_sorted: list[str], wmin: int, wmax: int) -> dict[str, int]:
    n = len(ids_sorted)
    out = {}
    for i, uid in enumerate(ids_sorted):
        t = 0 if n == 1 else i / (n - 1)
        weekly = int(round(lerp(wmin, wmax, t)))
        out[uid] = weekly_to_daily(weekly)
    return out


def main():
    ames = []
    for p in sorted(UNITS.glob("JAZZ_AME_*.lua")):
        t = p.read_text(encoding="utf-8")
        ames.append(
            {
                "path": p,
                "id": p.stem,
                "text": t,
                "old": parse_salary(t),
                "tier": parse_field(t, "AMECategory"),
                "role": parse_field(t, "AMERole"),
            }
        )

    by_tier: dict[str, list] = {}
    for a in ames:
        by_tier.setdefault(a["tier"] or "?", []).append(a)

    new_map: dict[str, int] = {}

    for tier, (wmin, wmax) in TIER_WEEKLY.items():
        group = sorted(by_tier.get(tier, []), key=lambda a: (a["old"] or 0, a["id"]))
        new_map.update(tier_salaries([a["id"] for a in group], wmin, wmax))

    specs = by_tier.get("Specialists", [])
    by_role: dict[str, list] = {}
    for a in specs:
        by_role.setdefault(a["role"] or "?", []).append(a)

    for role, (wmin, wmax) in SPEC_WEEKLY.items():
        group = sorted(by_role.get(role, []), key=lambda a: (a["old"] or 0, a["id"]))
        role_map = tier_salaries([a["id"] for a in group], wmin, wmax)
        for uid, daily in role_map.items():
            if daily > SPEC_CEILING_DAILY:
                daily = SPEC_CEILING_DAILY
            # also enforce weekly<=2000
            daily = min(daily, weekly_to_daily(2000))
            new_map[uid] = daily

    # Write UnitData companions
    for a in ames:
        sal = new_map[a["id"]]
        new_text = set_salary(a["text"], sal)
        if new_text != a["text"]:
            a["path"].write_text(new_text, encoding="utf-8", newline="\n")
        a["new"] = sal

    # Sync items.lua ModItem blocks ('Id', "JAZZ_AME_NN")
    items = ITEMS.read_text(encoding="utf-8")
    changed = 0
    for uid, sal in new_map.items():
        pattern = re.compile(
            rf"('Id',\s*\"{uid}\")([\s\S]{{0,5000}}?)('StartingSalary',\s*)\d+",
            re.M,
        )

        def sub(m, sal=sal):
            nonlocal changed
            changed += 1
            return f"{m.group(1)}{m.group(2)}{m.group(3)}{sal}"

        items, c = pattern.subn(sub, items, count=1)
        if c != 1:
            print("WARN items miss", uid, "count", c)

    ITEMS.write_text(items, encoding="utf-8", newline="\n")

    sals = [a["new"] for a in ames]
    print("Igor daily", IGOR_DAILY, "weekly", IGOR_DAILY * 7)
    print("Barry daily", BARRY_DAILY, "weekly", BARRY_DAILY * 7)
    print("AME daily min/med/max", min(sals), sorted(sals)[len(sals) // 2], max(sals))
    print("AME weekly min/med/max", min(sals) * 7, sorted(sals)[len(sals) // 2] * 7, max(sals) * 7)
    print("items StartingSalary updates", changed)
    for tier in ["Irregulars", "Fighters", "Hardened", "Specialists"]:
        xs = [a["new"] for a in ames if a["tier"] == tier]
        print(f"  {tier}: daily {min(xs)}-{max(xs)} weekly {min(xs)*7}-{max(xs)*7}")
    for a in sorted(ames, key=lambda x: x["new"]):
        print(f"{a['id']} {a['old']}->{a['new']} (wk {a['new']*7}) {a['tier']}/{a['role']}")


if __name__ == "__main__":
    main()
