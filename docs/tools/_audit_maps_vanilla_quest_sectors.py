#!/usr/bin/env python3
"""Inventory jazz-maps vanilla quest clones that still cite pre-remap sector IDs.

Helper for JAZZ-QUESTS-002. Read-only by default; use --strict to exit 1 when
in-scope Wave A+B quests still have stale landmark refs.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

CORE = Path(__file__).resolve().parents[2]
DEFAULT_MAPS = CORE.parent / "jazz-maps"

# vanilla HotDiamonds landmark → jazz-maps authored sector
LANDMARK_REMAP = {
    "A2": "A4",
    "A11": "B15",
    "A20": "B28",
    "B2": "C6",
    "B12": "A25",
    "B13": "A26",
    "B16": "D22",
    "C5": "D9",
    "C7": "E15",
    "D7": "E15",
    "D8": "E16",
    "D10": "F23",
    "E9": "F13",
    "F5": "G9",
    "H2": "I5",
    "H3": "I6",
    "H4": "I7",
    "H7": "H14",  # Fleatown-area mine; NOT Camp du Crocodile
    "I3": "J7",  # runtime Emerald Coast; sheet M7 is a stub
}

CROCODILE_VANILLA = "H14"
CROCODILE_MAPS = "P17"
ERNIE_LOCAL_KEEP = frozenset({"I2", "I3"})  # doctor / road on maps grid

IN_SCOPE_QUESTS = frozenset(
    {
        "DiamondRed",
        "RefugeeBlues",
        "FaithHealing",
        "JoseFamily",
        "Evidence",
        "Sanatorium",
        "HunterHunted",
        "NeverHitAGirl",
        "MiddleOfNowhere",
        "MiddleOfXWhere",
        "Landsbach",
        "U-Bahn",
        "U-Bahn_Helpers",
        "TreasureHunting",
        "Elliot",
        "05_TakeDownMajor",
        "YoungHearts",
        "RebelManifesto",
        "PantragruelWatch",
        "PantagruelRebels",
        "PantagruelLostAndFound",
        "PantagruelDramas",
        "PantagruelClinic",
        "Smiley",
        "RescueBiff",
        "04_Betrayal",
        "CorazonCaptureMine",
        "PierreDefeated",
        "Larry",
        "TheTwelveChairs",
        "GlobalCivilians",
        "_GroupsAttacked",
        "Emails",
    }
)


def sector_hits(block: str, sector: str) -> bool:
    return bool(
        re.search(
            rf"(SectorName\(\\'{sector}\\'\)|SectorName\('{sector}'\)|"
            rf"\bSector = \"{sector}\"|"
            rf"\bsector_id = \"{sector}\"|\bSectorID = \"{sector}\"|"
            rf"\bsource_sector_id = \"{sector}\"|"
            rf"\bguardpost_sector_id = \"{sector}\"|"
            rf"\bgv_Sectors\.{sector}\b|"
            rf"requiredSectors = \{{[^}}]*\"{sector}\"|"
            rf"Sectors = \{{[^}}]*\"{sector}\")",
            block,
        )
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--maps-root", type=Path, default=DEFAULT_MAPS)
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit 1 if any in-scope Wave A+B quest still has stale landmark refs",
    )
    args = parser.parse_args()
    items_path = args.maps_root.resolve() / "items.lua"
    text = items_path.read_text(encoding="utf-8")
    blocks = text.split("PlaceObj('ModItemQuestsDef',")[1:]

    rows: list[tuple[str, list[str]]] = []
    crocodile_journal: list[str] = []
    ernie_local: list[tuple[str, list[str]]] = []

    for block in blocks:
        match = re.search(r"\bid\s*=\s*\"([^\"]+)\"", block)
        if not match:
            continue
        quest_id = match.group(1)
        stale = sorted(
            sector for sector in LANDMARK_REMAP if sector_hits(block, sector)
        )
        if quest_id == "Elliot" and sector_hits(block, CROCODILE_VANILLA):
            crocodile_journal.append(quest_id)
        if stale:
            if quest_id.startswith("Jazz_") or quest_id.startswith("JAZZ_"):
                local = sorted(s for s in stale if s in ERNIE_LOCAL_KEEP)
                remote = [s for s in stale if s not in ERNIE_LOCAL_KEEP]
                if local:
                    ernie_local.append((quest_id, local))
                if remote:
                    rows.append((quest_id, remote))
            else:
                # Mine quests may correctly keep H14 after H7→H14; only H7 is stale.
                if "H14" in stale and quest_id != "Elliot":
                    # H14 alone after remap is OK for mine contexts.
                    stale = [s for s in stale if s != "H14"]
                if stale:
                    rows.append((quest_id, stale))

    print(f"maps_root={items_path.parent}")
    print(f"vanilla_quests_with_stale_landmark_refs={len(rows)}")
    for quest_id, stale in rows:
        mapped = ", ".join(f"{s}->{LANDMARK_REMAP[s]}" for s in stale)
        print(f"  {quest_id}: {mapped}")
    if crocodile_journal:
        print(
            "crocodile_journal_stale "
            f"(need {CROCODILE_VANILLA}->{CROCODILE_MAPS}): "
            + ", ".join(crocodile_journal)
        )
    if ernie_local:
        print("ernie_local_keep_candidates (do not remap I2/I3 blindly):")
        for quest_id, sectors in ernie_local:
            print(f"  {quest_id}: {', '.join(sectors)}")

    if args.strict:
        in_scope_stale = [qid for qid, _ in rows if qid in IN_SCOPE_QUESTS]
        if in_scope_stale or crocodile_journal:
            print(
                "STRICT FAIL: "
                + ", ".join(in_scope_stale + [f"Elliot:{CROCODILE_VANILLA}" for _ in crocodile_journal])
            )
            return 1
        print("STRICT OK: in-scope Wave A+B landmark refs remapped")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
