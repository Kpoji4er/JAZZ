# Normalize Ernie island Min/MaxFlareCarriers to 12/15 in jazz-maps items.lua
from __future__ import annotations

import re
from pathlib import Path

ITEMS = Path(r"C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz-maps\items.lua")

ERNIE = {
    "M1", "M2", "M3", "M4", "M5", "M6",
    "I2", "I3", "I4", "I5", "I6", "I6_Underground", "I7",
    "J4", "J5", "J6", "J7",
    "K3", "K4", "K5", "K6",
    "L1", "L2", "L3", "L4", "L5", "L6", "L6_Underground", "L7",
}

MIN_V, MAX_V = 12, 15

text = ITEMS.read_text(encoding="utf-8")

# Match SatelliteSector PlaceObj blocks (both ModItemSector nested and CampaignPreset)
# Pattern: PlaceObj('SatelliteSector', { ... }),
sat_re = re.compile(
    r"PlaceObj\('SatelliteSector',\s*\{(.*?)\n(\t+)\}\),",
    re.S,
)

changed = []
unchanged = []
added = []


def patch_block(body: str, indent: str) -> tuple[str, str]:
    """Return (new_body, action)."""
    id_m = re.search(r"'Id',\s*\"([^\"]+)\"", body)
    if not id_m:
        return body, "skip"
    sid = id_m.group(1)
    if sid not in ERNIE:
        return body, "skip"

    new_body = body
    has_min = re.search(r"'MinFlareCarriers',\s*\d+", new_body)
    has_max = re.search(r"'MaxFlareCarriers',\s*\d+", new_body)

    if has_min:
        new_body = re.sub(r"'MinFlareCarriers',\s*\d+", f"'MinFlareCarriers', {MIN_V}", new_body, count=1)
    if has_max:
        new_body = re.sub(r"'MaxFlareCarriers',\s*\d+", f"'MaxFlareCarriers', {MAX_V}", new_body, count=1)

    if has_min and has_max:
        old_min = int(re.search(r"'MinFlareCarriers',\s*(\d+)", body).group(1))
        old_max = int(re.search(r"'MaxFlareCarriers',\s*(\d+)", body).group(1))
        if old_min == MIN_V and old_max == MAX_V:
            return new_body, "already"
        return new_body, f"set {sid} {old_min}-{old_max} -> {MIN_V}-{MAX_V}"

    # insert missing fields after InterestingSector / ForceConflict / TerrainType / display_name
    insert = f"\n{indent}\t'MinFlareCarriers', {MIN_V},\n{indent}\t'MaxFlareCarriers', {MAX_V},"
    # prefer after InterestingSector
    for anchor in (
        r"('InterestingSector',\s*true,)",
        r"('ForceConflict',\s*true,)",
        r"('TerrainType',\s*\"[^\"]+\",)",
        r"('WeatherZone',\s*\"[^\"]+\",)",
        r"('City',\s*\"[^\"]+\",)",
        r"('Label1',\s*\"[^\"]+\",)",
        r"('display_name',\s*T\([^)]+\),)",
        r"('Map',\s*\"[^\"]+\",)",
    ):
        m = re.search(anchor, new_body)
        if m:
            # if one of min/max exists, only add the missing one(s) carefully
            pos = m.end()
            to_add = ""
            if not has_min:
                to_add += f"\n{indent}\t'MinFlareCarriers', {MIN_V},"
            if not has_max:
                to_add += f"\n{indent}\t'MaxFlareCarriers', {MAX_V},"
            new_body = new_body[:pos] + to_add + new_body[pos:]
            return new_body, f"add {sid} {MIN_V}-{MAX_V} (was partial={bool(has_min or has_max)})"

    # fallback: after Id line
    m = re.search(r"('Id',\s*\"[^\"]+\",)", new_body)
    if m:
        pos = m.end()
        to_add = ""
        if not has_min:
            to_add += f"\n{indent}\t'MinFlareCarriers', {MIN_V},"
        if not has_max:
            to_add += f"\n{indent}\t'MaxFlareCarriers', {MAX_V},"
        new_body = new_body[:pos] + to_add + new_body[pos:]
        return new_body, f"add-fallback {sid}"

    return body, "fail"


out = []
last = 0
for m in sat_re.finditer(text):
    body, indent = m.group(1), m.group(2)
    new_body, action = patch_block(body, indent)
    out.append(text[last : m.start(1)])
    out.append(new_body)
    last = m.end(1)
    if action.startswith("set ") or action.startswith("add"):
        changed.append(action)
    elif action == "already":
        unchanged.append(re.search(r"'Id',\s*\"([^\"]+)\"", body).group(1))
    elif action == "fail":
        changed.append("FAIL " + (re.search(r"'Id',\s*\"([^\"]+)\"", body).group(1) if re.search(r"'Id'", body) else "?"))

out.append(text[last:])
new_text = "".join(out)

if new_text == text and not changed:
    # still write report
    print("No textual change produced")
else:
    ITEMS.write_text(new_text, encoding="utf-8")

print("CHANGED:")
for c in changed:
    print(" ", c)
print(f"ALREADY ok ({len(unchanged)} blocks):", sorted(set(unchanged)))

# verify Ernie coverage: each id should appear with 12/15 at least twice ideally
for sid in sorted(ERNIE):
    hits = list(re.finditer(rf"'Id',\s*\"{re.escape(sid)}\"", new_text))
    print(f"  {sid}: SatelliteSector-ish Id hits={len(hits)}")
