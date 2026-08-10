from __future__ import annotations

import re
from collections import defaultdict
from pathlib import Path

p = Path(r"F:\SteamLibrary\steamapps\common\Jagged Alliance 3\ModTools\Src\Data\EnemySquads.lua")
text = p.read_text(encoding="utf-8", errors="replace")
print("file", p, "chars", len(text))

# Sample first PlaceObj form
print("sample head:")
print(text[:800])

# Vanilla editor export ends each PlaceObj with `})` (no trailing comma).
blocks = list(re.finditer(r"PlaceObj\('EnemySquads',\s*\{(.*?)^\}\)", text, re.S | re.M))
print("PlaceObj EnemySquads blocks", len(blocks))

ids = []
for m in blocks:
    block = m.group(1)
    idm = re.search(r'\bid\s*=\s*"([^"]+)"', block)
    if not idm:
        continue
    sid = idm.group(1)
    group = re.search(r'\bgroup\s*=\s*"([^"]+)"', block)
    dn = re.search(r'displayName\s*=\s*T\(\s*\d+\s*,\s*"([^"]*)"', block)
    mins = [int(x) for x in re.findall(r"'UnitCountMin',\s*(\d+)", block)]
    if not mins:
        mins = [int(x) for x in re.findall(r"UnitCountMin\s*=\s*(\d+)", block)]
    types = re.findall(r"'unitType',\s*\"([^\"]+)\"", block)
    if not types:
        types = re.findall(r'unitType\s*=\s*"([^"]+)"', block)
    ids.append((sid, sum(mins), group.group(1) if group else "", dn.group(1) if dn else "", types))

print("total defs", len(ids))

# All unique groups
groups = sorted({g for _, _, g, _, _ in ids})
print("groups:", groups)

leg = []
for row in ids:
    sid, n, g, dn, types = row
    blob = " ".join([sid, g, dn] + types)
    if re.search(r"Legion|Fortress|Pierre|Ernie|Bastien|Hyena", blob, re.I):
        leg.append(row)

print("legion-ish", len(leg))

by_pref = defaultdict(list)
for sid, n, g, dn, types in sorted(leg, key=lambda x: x[0]):
    # family from name
    if sid.startswith("Legion"):
        parts = sid.split("_")
        pref = "_".join(parts[:2]) if len(parts) > 1 else sid
    else:
        pref = sid.split("_")[0]
    by_pref[pref].append((sid, n, g, dn, types))

out = Path(r"C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz\docs\tools\_vanilla_legion_squads.txt")
lines = []
for pref in sorted(by_pref):
    lines.append(f"\n## {pref} ({len(by_pref[pref])})")
    for sid, n, g, dn, types in by_pref[pref]:
        uniq = sorted(set(types))
        tip = ", ".join(uniq[:6])
        if len(uniq) > 6:
            tip += f" …+{len(uniq)-6}"
        lines.append(f"  {n:3}  {sid:48} [{g}] {dn}")
        if tip:
            lines.append(f"       units: {tip}")

out.write_text("\n".join(lines), encoding="utf-8")
print("wrote", out)
print("\n".join(lines[:120]))
print("... total lines", len(lines))
