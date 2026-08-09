"""Dump Villa Sentry + Attacker squad sizes/composition from jazz-units items.lua."""
import re
from pathlib import Path

path = Path(__file__).resolve().parents[2] / ".." / "jazz-units" / "items.lua"
path = path.resolve()
text = path.read_text(encoding="utf-8")

ids = [
    "JAZZ_Legion_SentrySquad_AroundVilla",
    "JAZZ_Legion_VillaAttackers_K3",
    "JAZZ_Legion_VillaAttackers_K5",
    "JAZZ_Legion_VillaAttackers_L3",
    "JAZZ_Legion_VillaAttackers_L4",
    "JAZZ_Legion_VillaAttackers_L5",
]

for sid in ids:
    idx = text.find(f'id = "{sid}"')
    if idx < 0:
        print(sid, "NOT FOUND")
        continue
    start = text.rfind("PlaceObj('ModItemEnemySquads'", 0, idx)
    block = text[start:idx]
    units_m = re.search(r"Units = \{(.*)\},\s*\n\t\t\t\t(?:comment|displayName|group)", block, re.S)
    units = units_m.group(1) if units_m else block
    slot_blocks = re.split(r"PlaceObj\('EnemySquadUnit',", units)[1:]
    print("=" * 60)
    print(sid)
    tmin = tmax = 0
    for i, sb in enumerate(slot_blocks, 1):
        cm = re.search(r"'UnitCountMin',\s*(\d+).*?'UnitCountMax',\s*(\d+)", sb, re.S)
        types = re.findall(
            r"'unitType',\s*\"([^\"]+)\"(?:,\s*\n\s*'spawnWeight',\s*(\d+))?",
            sb,
        )
        if not cm:
            continue
        lo, hi = int(cm.group(1)), int(cm.group(2))
        tmin += lo
        tmax += hi
        pool = ", ".join(f"{t.split('_')[-1]}" + (f"*{w}" if w else "") for t, w in types)
        print(f"  [{i}] {lo}-{hi}: {pool}")
    print(f"  TOTAL: {tmin}-{tmax} (mid ~{(tmin + tmax) / 2:.0f})")

# Sector sums (Init = Sentry + Attacker_X)
print("\n" + "=" * 60)
print("SECTOR Init totals (Sentry + Attacker)")
sectors = {
    "K3": "JAZZ_Legion_VillaAttackers_K3",
    "K5": "JAZZ_Legion_VillaAttackers_K5",
    "L3": "JAZZ_Legion_VillaAttackers_L3",
    "L4": "JAZZ_Legion_VillaAttackers_L4",
    "L5": "JAZZ_Legion_VillaAttackers_L5",
}

def squad_range(sid: str):
    idx = text.find(f'id = "{sid}"')
    start = text.rfind("PlaceObj('ModItemEnemySquads'", 0, idx)
    block = text[start:idx]
    units_m = re.search(r"Units = \{(.*)\},\s*\n\t\t\t\t(?:comment|displayName|group)", block, re.S)
    units = units_m.group(1) if units_m else block
    tmin = tmax = 0
    for sb in re.split(r"PlaceObj\('EnemySquadUnit',", units)[1:]:
        cm = re.search(r"'UnitCountMin',\s*(\d+).*?'UnitCountMax',\s*(\d+)", sb, re.S)
        if cm:
            tmin += int(cm.group(1))
            tmax += int(cm.group(2))
    return tmin, tmax

smin, smax = squad_range("JAZZ_Legion_SentrySquad_AroundVilla")
for sec, aid in sectors.items():
    amin, amax = squad_range(aid)
    print(f"  {sec}: Sentry {smin}-{smax} + {aid.split('_')[-1]} {amin}-{amax} = {smin+amin}-{smax+amax}")
