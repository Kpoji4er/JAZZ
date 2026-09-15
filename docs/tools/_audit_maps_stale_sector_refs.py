#!/usr/bin/env python3
"""Audit jazz-maps TargetSectors / quests / effects for leftover vanilla HotDiamonds IDs."""

from __future__ import annotations

import re
from collections import defaultdict
from pathlib import Path

CORE = Path(__file__).resolve().parents[2]
MAPS = CORE.parent / "JAZZ Maps"
if not (MAPS / "items.lua").exists():
    MAPS = CORE.parent / "jazz-maps"
JA3 = Path(r"C:\Users\23ser\Downloads\JaggedAlliance3Modding-main\JaggedAlliance3Modding-main")

LANDMARK = {
    "A2": "A4",
    "A11": "B15",
    "A20": "B28",
    "B2": "C6",
    "B12": "A25",
    "B13": "A26",
    "B16": "D28",  # rift runtime (sheet D22 missing)
    "C5": "D9",
    "C7": "E15",
    "D7": "E15",
    "D8": "E16",
    "D10": "D18",  # Grand Prix runtime (sheet F23 missing)
    "E9": "F13",
    "F5": "G9",
    "F7": "E10",  # Camp Savane
    "G10": "L15",  # Camp La Barrière
    "H2": "I5",
    "H3": "I6",
    "H4": "I7",
    "H7": "H14",
    "H14": "P17",  # crocodile; mine is H7→H14
    "I1": "K4",
    "I2": "M4",
    "I3": "J7",
    "E16": "G22",  # Camp Chien Sauvage
    "F19": "H29",  # Camp Bien Chien island in atlas
}


def brace_block(text: str, start: int) -> tuple[int, int]:
    depth = 0
    started = False
    i = start
    while i < len(text):
        if text[i] == "{":
            started = True
            depth += 1
        elif text[i] == "}":
            depth -= 1
            if started and depth <= 0:
                return start, i
        i += 1
    return start, len(text) - 1


def parse_string_list(block: str, key: str) -> list[str]:
    m = re.search(rf"'{key}',\s*\{{([^}}]*)\}}", block)
    if not m:
        return []
    return re.findall(r'"([^"]+)"', m.group(1))


def field(block: str, key: str) -> str | None:
    m = re.search(rf"'{key}',\s*\"([^\"]*)\"", block)
    return m.group(1) if m else None


def display_name(block: str) -> str:
    m = re.search(r"'display_name',\s*T\(\d+,\s*(?:--\[\[[^\]]*\]\]\s*)?\"([^\"]*)\"", block)
    return m.group(1) if m else ""


def iter_placeobj(text: str, kind: str):
    marker = f"PlaceObj('{kind}'"
    start = 0
    while True:
        idx = text.find(marker, start)
        if idx < 0:
            break
        _, end = brace_block(text, idx + len(marker))
        yield idx, end + 1, text[idx : end + 1]
        start = end + 1


def parse_vanilla_sectors(path: Path) -> dict[str, dict]:
    text = path.read_text(encoding="utf-8")
    out = {}
    for _s, _e, block in iter_placeobj(text, "SatelliteSector"):
        sid = field(block, "Id")
        if not sid:
            continue
        out[sid] = {
            "id": sid,
            "map": field(block, "Map") or "",
            "name": display_name(block),
            "guardpost": "'Guardpost', true" in block,
            "targets": parse_string_list(block, "TargetSectors"),
        }
    return out


def parse_maps_moditems(text: str) -> list[dict]:
    rows = []
    for s, e, block in iter_placeobj(text, "ModItemSector"):
        sid = field(block, "sectorId")
        if not sid:
            continue
        sat = block
        rows.append(
            {
                "kind": "ModItemSector",
                "sid": sid,
                "map": field(block, "mapName") or "",
                "comment": field(block, "comment") or "",
                "name": display_name(sat),
                "guardpost": "'Guardpost', true" in sat,
                "targets": parse_string_list(sat, "TargetSectors"),
                "start": s,
            }
        )
    return rows


def parse_campaign_sectors(text: str) -> list[dict]:
    # CampaignPreset HotDiamonds nested SatelliteSector copies
    rows = []
    for s, e, block in iter_placeobj(text, "SatelliteSector"):
        sid = field(block, "Id")
        if not sid:
            continue
        rows.append(
            {
                "kind": "CampaignSatelliteSector",
                "sid": sid,
                "map": field(block, "Map") or "",
                "comment": "",
                "name": display_name(block),
                "guardpost": "'Guardpost', true" in block,
                "targets": parse_string_list(block, "TargetSectors"),
                "start": s,
            }
        )
    return rows


def quest_id(block: str) -> str:
    m = re.search(r"\bid\s*=\s*\"([^\"]+)\"", block)
    return m.group(1) if m else "?"


SECTOR_PAT = re.compile(
    r"(?:SectorName\(\\'([A-P]\d{1,2}(?:_Underground)?)\\'\)|"
    r"SectorName\('([A-P]\d{1,2}(?:_Underground)?)'\)|"
    r"\b(?:Sector|sector_id|SectorID|source_sector_id|guardpost_sector_id)\s*=\s*\"([A-P]\d{1,2}(?:_Underground)?)\"|"
    r"\bgv_Sectors\.([A-P]\d{1,2}(?:_Underground)?)\b|"
    r"\"([A-P]\d{1,2}(?:_Underground)?)\")"
)


def collect_quest_refs(block: str) -> set[str]:
    found = set()
    for m in SECTOR_PAT.finditer(block):
        for g in m.groups():
            if g:
                found.add(g)
    return found


def main() -> int:
    import sys

    sys.stdout.reconfigure(encoding="utf-8")
    vanilla = parse_vanilla_sectors(JA3 / "Data" / "CampaignPreset.lua")
    maps_text = (MAPS / "items.lua").read_text(encoding="utf-8")
    mod = parse_maps_moditems(maps_text)
    camp = parse_campaign_sectors(maps_text)

    print("=== Guardpost / TargetSectors (ModItemSector) ===")
    for row in mod:
        if not row["targets"] and not row["guardpost"]:
            continue
        stale = [t for t in row["targets"] if t in LANDMARK]
        flag = " GUARDPOST" if row["guardpost"] else ""
        print(
            f"{row['sid']:6} {row['name'] or row['comment']!r:40}{flag} "
            f"targets={row['targets']} stale={stale}"
        )

    print("\n=== Vanilla name match for maps guardposts ===")
    by_name = defaultdict(list)
    for sid, v in vanilla.items():
        if v["name"]:
            by_name[v["name"].lower()].append(v)
    for row in mod:
        if not row["guardpost"]:
            continue
        hits = by_name.get((row["name"] or "").lower(), [])
        if hits:
            v = hits[0]
            print(
                f"maps {row['sid']} {row['name']!r} <- vanilla {v['id']} "
                f"v_targets={v['targets']} maps_targets={row['targets']} "
                f"same={row['targets']==v['targets']}"
            )
        else:
            print(f"maps {row['sid']} {row['name']!r} NO vanilla name match")

    print("\n=== CampaignPreset TargetSectors diffs vs ModItem ===")
    camp_tg = {(r["sid"], tuple(r["targets"])) for r in camp if r["targets"]}
    mod_tg = {(r["sid"], tuple(r["targets"])) for r in mod if r["targets"]}
    print(f"campaign lists={len(camp_tg)} moditem lists={len(mod_tg)}")

    print("\n=== Quests with LANDMARK keys ===")
    for _s, _e, block in iter_placeobj(maps_text, "ModItemQuestsDef"):
        qid = quest_id(block)
        refs = collect_quest_refs(block)
        stale = sorted(r for r in refs if r.split("_")[0] in LANDMARK)
        if stale:
            print(f"{qid}: {stale}")

    print("\n=== effect_target_sector_ids ===")
    for m in re.finditer(
        r"effect_target_sector_ids\s*=\s*\{([^}]*)\}", maps_text
    ):
        ids = re.findall(r'"([^"]+)"', m.group(1))
        stale = [t for t in ids if t in LANDMARK]
        if ids:
            line = maps_text[: m.start()].count("\n") + 1
            print(f"L{line}: {ids} stale={stale}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
