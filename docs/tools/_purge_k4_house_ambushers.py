"""Purge K4 (gsSMikN) HouseAmbushers+Legion AdvanceTo UnitMarkers; keep Adonis.

Also insert ~25 VillaSiege_Wave2 UnitMarkers gated by Jazz_VillaCounterAttack.Wave2Spawn,
cloned from a removed HouseAmbushers template (positions near villa edges).
"""
from __future__ import annotations

import re
from pathlib import Path

MAP = Path(r"C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz-maps\Maps\gsSMikN\objects.lua")

WAVE2_UNITS = [
    "JAZZ_Legion_AssaultT1_Roughneck",
    "JAZZ_Legion_FrontT1_Marauder",
    "JAZZ_Legion_FrontT1_Rifleman",
    "JAZZ_Legion_AssaultT2_ShockTrooper",
    "JAZZ_Legion_FrontT2_Raider",
    "JAZZ_Legion_FrontT2_Ambusher",
    "JAZZ_Legion_GunnerT1_Gunner",
    "JAZZ_Legion_AssaultT1_Grenadier",
    "JAZZ_Legion_FlankerT1_Warden",
    "JAZZ_Legion_FrontT1_Bonemaker",
]


def extract_unit_markers(text: str) -> list[tuple[int, int, str]]:
    """Return (start, end, body) for each PlaceObj('UnitMarker', {...}),"""
    out = []
    needle = "PlaceObj('UnitMarker',"
    i = 0
    while True:
        start = text.find(needle, i)
        if start < 0:
            break
        brace = text.find("{", start)
        depth = 0
        j = brace
        while j < len(text):
            c = text[j]
            if c == "{":
                depth += 1
            elif c == "}":
                depth -= 1
                if depth == 0:
                    j += 1
                    break
            j += 1
        # trailing ),
        end = j
        if text[end : end + 2] == "),":
            end += 2
        elif text[end : end + 1] == ")":
            end += 1
        # include following newline if present
        if end < len(text) and text[end] == "\n":
            end += 1
        body = text[start:end]
        out.append((start, end, body))
        i = end
    return out


def is_old_siege(body: str) -> bool:
    if "HouseAmbushers" not in body:
        return False
    if "AdvanceTo" not in body:
        return False
    if "EmmaAndCorazon" not in body:
        return False
    # Legion group string
    if "'Legion'" not in body and '"Legion"' not in body:
        return False
    # Keep Adonis WorldFlip house ambushers
    if "Adonis" in body:
        return False
    return True


def parse_pos(body: str) -> tuple[int, int, int] | None:
    m = re.search(r"'Pos',\s*point\((\d+),\s*(\d+),\s*(\d+)\)", body)
    if not m:
        return None
    return int(m.group(1)), int(m.group(2)), int(m.group(3))


def make_wave2_marker(handle: int, unit: str, x: int, y: int, z: int) -> str:
    return f"""PlaceObj('UnitMarker', {{
	Groups = {{
		"VillaSiege_Wave2",
		"Legion",
	}},
	Routine = "AdvanceTo",
	RoutineArea = "EmmaAndCorazon",
	Side = "enemy1",
	UnitDataSpawnDefs = {{
		PlaceObj('UnitDataSpawnDef', {{
			'UnitDef', "{unit}",
		}}),
	}},
	Spawn_Conditions = {{
		PlaceObj('QuestIsVariableBool', {{
			QuestId = "Jazz_VillaCounterAttack",
			Vars = set( "Wave2Spawn" ),
		}}),
	}},
	handle = {handle},
	Pos = point({x}, {y}, {z}),
}}),
"""


def main() -> None:
    text = MAP.read_text(encoding="utf-8")
    markers = extract_unit_markers(text)
    print(f"UnitMarkers total: {len(markers)}")

    to_remove = []
    templates = []
    for start, end, body in markers:
        if is_old_siege(body):
            to_remove.append((start, end, body))
            pos = parse_pos(body)
            if pos:
                templates.append(pos)

    print(f"Old siege to remove: {len(to_remove)}")
    if not to_remove:
        raise SystemExit("nothing to purge — check filter")

    # Remove from end so indices stay valid
    for start, end, _ in sorted(to_remove, key=lambda t: t[0], reverse=True):
        text = text[:start] + text[end:]

    # Collect existing handles to avoid collision
    handles = {int(h) for h in re.findall(r"'?handle'?\s*=\s*(\d+)", text)}
    next_h = max(handles) + 1 if handles else 1900000000

    # Place Wave2 near first N template positions (or synthetic ring)
    n_wave = 25
    positions = templates[:n_wave]
    if len(positions) < n_wave:
        # pad from average
        if positions:
            ax = sum(p[0] for p in positions) // len(positions)
            ay = sum(p[1] for p in positions) // len(positions)
            az = positions[0][2]
        else:
            ax, ay, az = 140000, 140000, 7000
        while len(positions) < n_wave:
            i = len(positions)
            positions.append((ax + (i % 5) * 2400, ay + (i // 5) * 2400, az))

    wave_blocks = []
    for i in range(n_wave):
        x, y, z = positions[i]
        unit = WAVE2_UNITS[i % len(WAVE2_UNITS)]
        wave_blocks.append(make_wave2_marker(next_h + i, unit, x, y, z))

    # Append before final closing of objects file — find last PlaceObj or end of return
    insert_at = text.rfind("\n")
    # Prefer after last UnitMarker-ish content: append near end before empty trailing
    # Many maps end with `}` of root — find last `}),\n` cluster
    # Safest: insert after first remaining content following purge — search for Emma marker and insert after a block near villa
    anchor = text.find("EmmaAndCorazon")
    if anchor < 0:
        raise SystemExit("EmmaAndCorazon not found for Wave2 insert anchor")
    # find end of that PlaceObj
    # Insert wave markers at end of file before last `}` if present
    m_end = re.search(r"\n\}\s*$", text)
    if m_end:
        insert_at = m_end.start()
        text = text[:insert_at] + "\n" + "".join(wave_blocks) + text[insert_at:]
    else:
        text = text + "\n" + "".join(wave_blocks)

    MAP.write_text(text, encoding="utf-8")
    print(f"wrote {MAP}")
    print(f"Wave2 markers inserted: {n_wave} handles {next_h}..{next_h + n_wave - 1}")


if __name__ == "__main__":
    main()
