from pathlib import Path
import re
import sys

MAP = {
    1: "Negotiator",
    3: "Negotiator",
    6: "Loner",
    11: "Psycho",
    14: "Scoundrel",
    21: "Pessimist",
    32: "Stealthy",
    38: "Optimist",
    39: "Psycho",
    47: "Scoundrel",
    50: "Optimist",
    56: "Stealthy",
}
P = set(MAP.values())
root = Path(__file__).resolve().parents[2].parent / "jazz-units" / "UnitData"
hits = 0
for n in range(1, 61):
    t = (root / f"JAZZ_AME_{n:02d}.lua").read_text(encoding="utf-8")
    m = re.search(r"StartingPerks\s*=\s*\{([^}]*)\}", t, re.S)
    ps = re.findall(r'"([^"]+)"', m.group(1) if m else "")
    pers = [p for p in ps if p in P]
    if n in MAP:
        assert pers == [MAP[n]], (n, pers, MAP[n])
        hits += 1
    else:
        assert not pers, (n, pers)
print(f"OK companions personality {hits}/12")

items = (root.parent / "items.lua").read_text(encoding="utf-8")
for n, perk in MAP.items():
    uid = f"JAZZ_AME_{n:02d}"
    i = items.find(f"'Id', \"{uid}\"")
    assert i >= 0, uid
    chunk = items[i : i + 2500]
    assert f"'{perk}'" in chunk, (uid, perk)
print("OK items.lua personality samples")
