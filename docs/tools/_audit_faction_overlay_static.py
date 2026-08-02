"""Static checks for JAZZ-STRATEGY-014 faction matrix (no game runtime)."""
from __future__ import annotations

import ast
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OVERLAY = ROOT / "Code" / "FactionOverlay.lua"


def fail(msg: str) -> None:
    print(f"FAIL: {msg}")
    sys.exit(1)


def main() -> None:
    text = OVERLAY.read_text(encoding="utf-8")
    for name in (
        "JAZZ_GetFactionRelation",
        "JAZZ_AreFactionsHostile",
        "JAZZ_SetSectorOwnerFaction",
        "JAZZ_GetSectorOwnerFaction",
        "JAZZ_SetSquadFaction",
        "JAZZ_FactionMayAttackPlayerOnSat",
        "JAZZ_SquadsAreHostile",
        "gv_JAZZ_FactionOverlay",
    ):
        if name not in text:
            fail(f"missing {name}")

    # Locked pairs must appear in source comments/branches.
    required_tokens = (
        'pair("player", "rebels")',
        'pair("adonis", "army")',
        'pair("legion", "adonis")',
        'pair("legion", "player")',
        'pair("adonis", "player")',
        "lWorldFlip()",
        'rawget(_G, "Team")',
    )
    for tok in required_tokens:
        if tok not in text:
            fail(f"missing locked-default token: {tok}")

    # Load registration
    meta = (ROOT / "metadata.lua").read_text(encoding="utf-8")
    if 'Code/FactionOverlay.lua' not in meta:
        fail("FactionOverlay not in metadata.code")
    items = (ROOT / "items.lua").read_text(encoding="utf-8")
    if "FactionOverlay" not in items:
        fail("FactionOverlay ModItemCode missing in items.lua")

    # STRATEGY-018 hooks
    patrols = (ROOT / "Code" / "Guardpost_Patrols.lua").read_text(encoding="utf-8")
    for tok in (
        "lAvoidPlayerRoles",
        "lHasAvoidPlayerRoute",
        "g_JAZZ_RouteAvoidPlayer",
        'hold_for_path',
        'owner_faction',
    ):
        if tok not in patrols:
            fail(f"Guardpost_Patrols missing {tok}")

    sat = (ROOT / "Code" / "SatelliteSquad.lua").read_text(encoding="utf-8")
    if "g_JAZZ_RouteAvoidPlayer" not in sat:
        fail("SatelliteSquad missing avoid-player gate")
    if "JAZZ_SquadsAreHostile" not in sat:
        fail("SatelliteSquad missing faction-war conflict gate")

    print("OK: STRATEGY-014/018 static matrix + pathing hooks present")


if __name__ == "__main__":
    main()
