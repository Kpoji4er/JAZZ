# Static smoke for JAZZ-STRATEGY-025 local rest (city/bunker/outpost).
# Run from jazz/: python docs/tools/_check_legion_rest_025.py

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def must(cond: bool, msg: str, fails: list[str]) -> None:
    if not cond:
        fails.append(msg)


def main() -> int:
    fails: list[str] = []
    src = read(ROOT / "Code" / "Guardpost_Patrols.lua")

    must("lSectorIsLocalRestSite" in src, "lSectorIsLocalRestSite missing", fails)
    must("lNearestLocalRestSite" in src, "lNearestLocalRestSite missing", fails)
    must("lOutpostCanAffordTopUp" in src, "lOutpostCanAffordTopUp missing", fails)
    must("lPickRestTarget" in src, "lPickRestTarget missing", fails)
    must("sector.Bunker" in src, "bunker rest gate missing", fails)
    must('sector.City ~= "none"' in src or "sector.City and sector.City ~= \"none\"" in src, "city rest gate missing", fails)
    must("lRegularRoles[squad_state.role]" in src and "lPickRestTarget" in src, "regular-only pick wiring missing", fails)
    must("at_rest = lSectorIsLocalRestSite" in src, "AssignReady off-outpost rest missing", fails)
    must("lOutpostCanAffordTopUp(root, region, outpost, squad, squad_state)" in src, "wounded top-up gate unused", fails)
    must('going_home_for_topup and "return_wounded"' in src, "return_wounded only for home top-up missing", fails)

    # Top-up must still require home sector (existing guard + begin-rest at_home).
    must("squad.CurrentSector ~= squad_state.home_sector" in src, "lTryTopUpSquad home gate missing", fails)
    must("at_home and outpost and lRegularRoles" in src, "BeginBaseRest top-up at_home gate missing", fails)

    ru = read(ROOT / "Russian.csv")
    en = read(ROOT / "English.csv")
    for lid, needle in (
        ("890000000001434", "returning to rest at"),
        ("890000000001641", "wounded at <sector>"),
        ("890000000001642", "retreating wounded to <target>"),
        ("890000000001644", "resting and refitting at <sector>"),
    ):
        must(lid in ru, f"RU missing {lid}", fails)
        must(lid in en, f"EN missing {lid}", fails)
        must(needle in en, f"EN text for {lid} stale", fails)

    wiki = read(ROOT / "docs" / "wiki" / "legion-global-ai.md")
    must("ближайш" in wiki, "wiki missing nearest rest wording", fails)
    must("город" in wiki and "бункер" in wiki, "wiki missing city/bunker rest", fails)

    if fails:
        print("FAIL STRATEGY-025 static:")
        for f in fails:
            print(" -", f)
        return 1
    print("OK STRATEGY-025 static checks")
    return 0


if __name__ == "__main__":
    sys.exit(main())
