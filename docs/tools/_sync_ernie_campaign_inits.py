# -*- coding: utf-8 -*-
"""Sync HotDiamonds CampaignPreset InitialSquads for Ernie UNITS-007 / baseline.

Canon for overflow + locked hubs = ModItemSector InitialSquads.
CampaignPreset nested SatelliteSector often still has pre-UNITS-007 overflow
(empty/missing defs → ghost [0] squads + rollover assert).

Also clears baseline map-only Init: I6 / J6 / L7 / K4 / K6.

Safety:
- Campaign edits ONLY inside ModItemCampaignPreset HotDiamonds
  (between PlaceObj('ModItemCampaignPreset' … and id = \"HotDiamonds\").
- ModItem clears ONLY via 'sectorId' before that campaign block.
- Never cross into the next sector: no second 'Id'/'sectorId' between
  anchor and InitialSquads.
- Replacement text does NOT include a trailing comma (file keeps the original ,).
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

MAPS = Path(r"C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz-maps\items.lua")

SYNC_SECTORS = {
    "M4",
    "M5",
    "M6",
    "I2",
    "I3",
    "I4",
    "I5",
    "I7",
    "J5",
    "K3",
    "K5",
    "L1",
    "L2",
    "L3",
    "L4",
    "L5",
    "L6",
    "L6_Underground",
}
CLEAR_INIT = {"I6", "J6", "L7", "K4", "K6"}
ALL = SYNC_SECTORS | CLEAR_INIT

# Between anchor and InitialSquads: allow anything except another sector Id/sectorId
_BETWEEN_ID = r"(?:(?!'Id', \")[\s\S])*?"
_BETWEEN_SECTOR = r"(?:(?!'sectorId', \")[\s\S])*?"


def find_hotdiamonds_span(text: str) -> tuple[int, int]:
    start = text.find("PlaceObj('ModItemCampaignPreset'")
    if start < 0:
        raise RuntimeError("ModItemCampaignPreset not found")
    end = text.find('id = "HotDiamonds"', start)
    if end < 0:
        raise RuntimeError("HotDiamonds id not found after CampaignPreset")
    return start, end


def _parse_packs(inner: str) -> list[str]:
    return re.findall(r'"([^"]+)"', inner)


def moditem_init(text: str, sid: str, mod_end: int) -> list[str] | None:
    m = re.search(
        rf"'sectorId', \"{re.escape(sid)}\"{_BETWEEN_SECTOR}'InitialSquads', \{{([\s\S]*?)\}}",
        text[:mod_end],
    )
    if not m:
        return None
    return _parse_packs(m.group(1))


def campaign_init(camp: str, sid: str) -> list[str] | None:
    m = re.search(
        rf"'Id', \"{re.escape(sid)}\"{_BETWEEN_ID}'InitialSquads', \{{([\s\S]*?)\}}",
        camp,
    )
    if not m:
        return None
    return _parse_packs(m.group(1))


def format_init_body(ids: list[str], indent: str) -> str:
    if not ids:
        return "'InitialSquads', {}"
    inner = "\n".join(f'{indent}\t"{i}",' for i in ids)
    return f"'InitialSquads', {{\n{inner}\n{indent}}}"


def replace_init(
    text: str,
    region_start: int,
    region_end: int,
    kind: str,
    sid: str,
    new_ids: list[str],
) -> tuple[str, int]:
    region = text[region_start:region_end]
    if kind == "campaign":
        pat = re.compile(
            rf"'Id', \"{re.escape(sid)}\"{_BETWEEN_ID}('InitialSquads', \{{[\s\S]*?\}})"
        )
    else:
        pat = re.compile(
            rf"'sectorId', \"{re.escape(sid)}\"{_BETWEEN_SECTOR}('InitialSquads', \{{[\s\S]*?\}})"
        )
    m = pat.search(region)
    if not m:
        return text, 0
    abs_start = region_start + m.start(1)
    abs_end = region_start + m.end(1)
    line_start = text.rfind("\n", 0, abs_start) + 1
    ind_m = re.match(r"(\t*)", text[line_start:abs_start])
    ind = ind_m.group(1) if ind_m else "\t\t\t\t\t"
    repl = format_init_body(new_ids, ind)
    return text[:abs_start] + repl + text[abs_end:], 1


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    raw = MAPS.read_bytes()
    nl = b"\r\n" if b"\r\n" in raw else b"\n"
    text = raw.decode("utf-8")
    camp_start, camp_end = find_hotdiamonds_span(text)
    print(f"HotDiamonds campaign span [{camp_start}, {camp_end})")

    plans: list[tuple[str, list[str] | None, list[str]]] = []
    for sid in sorted(ALL):
        cur = moditem_init(text, sid, camp_start)
        if sid in CLEAR_INIT:
            target: list[str] = []
        else:
            if cur is None:
                print(f"WARN no ModItemSector Init for {sid}")
                continue
            target = list(cur)
        camp_cur = campaign_init(text[camp_start:camp_end], sid)
        plans.append((sid, cur, target))
        print(f"plan {sid}: ModItem {cur} | Campaign {camp_cur} -> target {target}")

    if not args.apply:
        print("dry-run")
        return 0

    n_mod = n_camp = 0
    for sid, cur, target in plans:
        if sid in CLEAR_INIT or (cur is not None and cur != target):
            text, n = replace_init(text, 0, camp_start, "moditem", sid, target)
            n_mod += n
            print(f"ModItem {sid}: {n}")

        text, n = replace_init(text, camp_start, camp_end, "campaign", sid, target)
        n_camp += n
        print(f"Campaign {sid}: {n}")

    if "},," in text or "},,," in text:
        print("ERROR: stacked },, introduced — abort write")
        return 2

    # Recompute span (offsets unchanged if only substitutions of similar size, but
    # still re-find for safety).
    camp_start2, camp_end2 = find_hotdiamonds_span(text)
    expected = {
        "I5": ["LegionErnieVillage"],
        "J5": ["LegionDefenders_Shooters_Easy_Ernie"],
        "K3": ["JAZZ_Legion_SentrySquad_AroundVilla", "JAZZ_Legion_VillaAttackers_K3"],
        "K5": ["JAZZ_Legion_SentrySquad_AroundVilla", "JAZZ_Legion_VillaAttackers_K5"],
        "L6": ["LegionErnie_Medium_Forest_A", "LegionExtra_Ernie_Flankers"],
        "I7": ["FortressPierre", "FortressDefenders"],
        "I6": [],
        "J6": [],
        "L7": [],
        "K4": [],
        "K6": [],
    }
    for sid, want in expected.items():
        got_m = moditem_init(text, sid, camp_start2)
        got_c = campaign_init(text[camp_start2:camp_end2], sid)
        if got_m != want and not (want == [] and got_m in (None, [])):
            # CLEAR: None (no block) or [] both OK for ModItem after clear → we always
            # leave an empty {} block, so got_m should be [].
            if want == [] and got_m == []:
                pass
            elif want and got_m != want:
                print(f"ERROR: ModItem {sid}={got_m} want {want} — abort write")
                return 3
        if want and got_c is not None and got_c != want:
            print(f"ERROR: Campaign {sid}={got_c} want {want} — abort write")
            return 4
        if want == [] and got_c not in (None, []):
            print(f"ERROR: Campaign {sid} still {got_c} — abort write")
            return 5

    MAPS.write_bytes(text.replace("\r\n", "\n").replace("\n", nl.decode("ascii")).encode("utf-8"))
    print(f"written mod={n_mod} camp={n_camp}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
