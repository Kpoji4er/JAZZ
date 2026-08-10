"""Baseline Ernie enemy counts: satellite InitialSquads + map UnitMarkers.

Writes docs/design/ernie-garrison-baseline.md (snapshot before full rework).
"""
from __future__ import annotations

import re
from collections import defaultdict
from pathlib import Path

MAPS_ITEMS = Path(r"C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz-maps\items.lua")
UNITS_ITEMS = Path(r"C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz-units\items.lua")
MAPS_ROOT = Path(r"C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz-maps\Maps")
OUT = Path(r"C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz\docs\design\ernie-garrison-baseline.md")

ERNIE = [
    "M1", "M2", "M3", "M4", "M5", "M6",
    "I2", "I3", "I4", "I5", "I6", "I6_Underground", "I7",
    "J4", "J5", "J6", "J7",
    "K3", "K4", "K5", "K6",
    "L1", "L2", "L3", "L4", "L5", "L6", "L6_Underground", "L7",
]

LIST_KEYS = (
    "InitialSquads",
    "EnemySquadsList",
    "StrongEnemySquadsList",
    "ExtraDefenderSquads",
)

# Target bands locked in chat 2026-08-10 (owner).
TARGETS = {
    "default_garrison": "20–30",
    "filler": "22–26",
    "hub_story": "~35–45",
    "spice": "+3–6",
    "map_only": "0 Init (map markers)",
}


def list_field(body: str, key: str) -> list[str]:
    m = re.search(rf"'{key}',\s*\{{(.*?)\}},", body, re.S)
    if not m:
        return []
    return re.findall(r'"([^"]+)"', m.group(1))


def parse_sectors(items: str) -> dict[str, dict]:
    sat_re = re.compile(r"PlaceObj\('SatelliteSector',\s*\{(.*?)\n\t+\}\),", re.S)
    out: dict[str, dict] = {}
    seen: set[tuple] = set()
    for m in sat_re.finditer(items):
        body = m.group(1)
        id_m = re.search(r"'Id',\s*\"([^\"]+)\"", body)
        if not id_m or id_m.group(1) not in ERNIE:
            continue
        sid = id_m.group(1)
        comment = re.search(r"'comment',\s*\"([^\"]*)\"", body)
        # ModItemSector comment is outside SatelliteSector — keep display
        display = re.search(r"'display_name',\s*T\(\d+,\s*(?:--\[\[[^\]]*\]\]\s*)?\"([^\"]*)\"", body)
        if sid not in out:
            out[sid] = {
                "display": display.group(1) if display else "",
                "lists": defaultdict(list),
                "map": None,
            }
        map_m = re.search(r"'Map',\s*\"([^\"]+)\"", body)
        if map_m:
            out[sid]["map"] = map_m.group(1)
        if display and not out[sid]["display"]:
            out[sid]["display"] = display.group(1)
        for key in LIST_KEYS:
            for sq in list_field(body, key):
                pair = (sid, key, sq)
                if pair in seen:
                    continue
                seen.add(pair)
                out[sid]["lists"][key].append(sq)
    # ModItemSector comments
    for m in re.finditer(
        r"PlaceObj\('ModItemSector',\s*\{(.*?)\n\t+\}\),",
        items,
        re.S,
    ):
        body = m.group(1)
        sid_m = re.search(r"'sectorId',\s*\"([^\"]+)\"", body)
        if not sid_m or sid_m.group(1) not in ERNIE:
            continue
        sid = sid_m.group(1)
        c = re.search(r"'comment',\s*\"([^\"]*)\"", body)
        if c and sid in out:
            out[sid]["comment"] = c.group(1)
    return out


def squad_size(units_text: str, sid: str) -> int | None:
    needle = f'id = "{sid}"'
    pos = 0
    while True:
        i = units_text.find(needle, pos)
        if i < 0:
            return None
        start = units_text.rfind("PlaceObj('ModItemEnemySquads'", 0, i)
        if start < 0:
            pos = i + 1
            continue
        # id is at end of block; Units before id
        block = units_text[start:i]
        if "'UnitCountMin'" not in block and "UnitCountMin" not in block:
            pos = i + 1
            continue
        counts = [int(x) for x in re.findall(r"'UnitCountMin',\s*(\d+)", block)]
        return sum(counts) if counts else None


def map_enemy_count(map_id: str | None) -> tuple[int, int, int]:
    """Return (enemy_markers, ally_markers, total_unit_markers) from map.bin.lua-ish files."""
    if not map_id:
        return (0, 0, 0)
    folder = MAPS_ROOT / map_id
    if not folder.is_dir():
        return (0, 0, 0)
    # Prefer largest .lua dump / objects
    candidates = list(folder.glob("*.lua")) + list(folder.glob("**/*.lua"))
    text = ""
    best = 0
    for p in candidates:
        try:
            t = p.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        if len(t) > best:
            best = len(t)
            text = t
    if not text:
        return (0, 0, 0)

    # UnitMarker with Side / Groups — count enemy-ish
    enemy = 0
    ally = 0
    total = 0
    for m in re.finditer(r"PlaceObj\('UnitMarker',\s*\{(.*?)\}\s*,?\s*\)", text, re.S):
        block = m.group(1)
        total += 1
        side = re.search(r"'Side',\s*\"([^\"]+)\"", block) or re.search(
            r"Side\s*=\s*\"([^\"]+)\"", block
        )
        s = side.group(1) if side else ""
        if s in ("enemy1", "enemy2", "enemy", "Enemy", "Legion"):
            enemy += 1
        elif s in ("ally", "player1", "Player", "neutral"):
            ally += 1
        else:
            # Banter groups / defenders often enemy without Side string — check UnitData
            ud = re.search(r"'UnitData',\s*\"([^\"]+)\"", block) or re.search(
                r"UnitDataId\s*=\s*\"([^\"]+)\"", block
            )
            if ud and re.search(r"Legion|Army|Adonis|Thug|Pirate|Hyena", ud.group(1), re.I):
                enemy += 1
            elif ud and re.search(r"Rebel|Militia|Civilian|Herman|Kiki|Bastien", ud.group(1), re.I):
                ally += 1
    # Fallback: count UnitMarker appearances if PlaceObj form differs
    if total == 0:
        total = len(re.findall(r"UnitMarker", text))
    return (enemy, ally, total)


def vanilla_size(vanilla_text: str, sid: str) -> int | None:
    blocks = list(re.finditer(r"PlaceObj\('EnemySquads',\s*\{(.*?)^\}\)", vanilla_text, re.S | re.M))
    for m in blocks:
        block = m.group(1)
        idm = re.search(r'\bid\s*=\s*"([^"]+)"', block)
        if not idm or idm.group(1) != sid:
            continue
        mins = [int(x) for x in re.findall(r"'UnitCountMin',\s*(\d+)", block)]
        return sum(mins)
    return None


def main() -> None:
    maps_items = MAPS_ITEMS.read_text(encoding="utf-8")
    units = UNITS_ITEMS.read_text(encoding="utf-8")
    vanilla_path = Path(
        r"F:\SteamLibrary\steamapps\common\Jagged Alliance 3\ModTools\Src\Data\EnemySquads.lua"
    )
    vanilla = vanilla_path.read_text(encoding="utf-8") if vanilla_path.exists() else ""

    sectors = parse_sectors(maps_items)
    size_cache: dict[str, int | None] = {}

    def get_size(sq: str) -> int | None:
        if sq in size_cache:
            return size_cache[sq]
        n = squad_size(units, sq)
        if n is None and vanilla:
            n = vanilla_size(vanilla, sq)
            if n is not None:
                size_cache[sq] = n
                return n
            size_cache[sq] = None
            return None
        size_cache[sq] = n
        return n

    lines: list[str] = []
    lines.append("# Ernie garrison baseline (pre-rework)")
    lines.append("")
    lines.append("Snapshot before full Ernie / Legion squad rework. **Do not treat as target design.**")
    lines.append("")
    lines.append("## Locked targets (owner 2026-08-10)")
    lines.append("")
    lines.append("| Band | N |")
    lines.append("| --- | --- |")
    lines.append(f"| Typical starting garrison (one Init) | {TARGETS['default_garrison']} |")
    lines.append(f"| Filler coastal (e.g. M5) | {TARGETS['filler']} |")
    lines.append(f"| Hub / story seed (I5, I7) | {TARGETS['hub_story']} |")
    lines.append(f"| Extra / spice (if any) | {TARGETS['spice']} |")
    lines.append(f"| M1–M3 | {TARGETS['map_only']} |")
    lines.append("")
    lines.append("Policy: with Legion Global AI, static `InitialSquads` = starting garrisons or quest packs — not the living army. Living pressure = AI (patrol / reinforce / QRF).")
    lines.append("")
    lines.append("## Counts by sector")
    lines.append("")
    lines.append(
        "| Sector | Name | Init sum | Init packs | Patrol/Strong/Extra | Map enemies≈ | Notes |"
    )
    lines.append("| --- | --- | ---: | --- | --- | ---: | --- |")

    for sid in ERNIE:
        info = sectors.get(sid, {"display": "", "lists": {}, "map": None, "comment": ""})
        lists = info.get("lists") or {}
        init = lists.get("InitialSquads") or []
        other = []
        for k in ("EnemySquadsList", "StrongEnemySquadsList", "ExtraDefenderSquads"):
            for sq in lists.get(k) or []:
                other.append(f"{k}:{sq}")

        init_parts = []
        init_sum = 0
        unknown = False
        for sq in init:
            n = get_size(sq)
            if n is None:
                init_parts.append(f"{sq}(?)")
                unknown = True
            else:
                init_parts.append(f"{sq}({n})")
                init_sum += n

        map_e, map_a, map_t = map_enemy_count(info.get("map"))
        name = info.get("display") or ""
        note = info.get("comment") or ""
        if not init and map_e:
            note = (note + "; " if note else "") + "map-only enemies"
        if unknown:
            note = (note + "; " if note else "") + "some squad sizes from vanilla or missing"

        init_cell = str(init_sum) if init else "0"
        if unknown and init:
            init_cell = f"≥{init_sum}+?"

        packs = ", ".join(init_parts) if init_parts else "—"
        other_s = ", ".join(other) if other else "—"
        map_cell = str(map_e) if map_e else ("0" if info.get("map") else "?")

        lines.append(
            f"| {sid} | {name} | {init_cell} | {packs} | {other_s} | {map_cell} | {note} |"
        )

    lines.append("")
    lines.append("## Notes on measurement")
    lines.append("")
    lines.append(
        "- **Init sum** = sum of `UnitCountMin` over referenced `ModItemEnemySquads` in `jazz-units` "
        "(fallback: vanilla `EnemySquads.lua` if ID not in jazz-units)."
    )
    lines.append(
        "- **Map enemies≈** = `UnitMarker` with enemy-ish Side / Legion-like UnitData on the sector map dump "
        "(approximate; triggers/spawns may add more)."
    )
    lines.append(
        "- I7 Patrol/Strong/Extra are **pools**, not all spawned at once — do not add them to Init sum."
    )
    lines.append(
        "- Regenerated by `docs/tools/_ernie_garrison_baseline.py`."
    )
    lines.append("")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("wrote", OUT)
    print("\n".join(lines[lines.index("## Counts by sector") :]))


if __name__ == "__main__":
    main()
