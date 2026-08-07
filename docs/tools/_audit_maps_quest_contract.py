#!/usr/bin/env python3
"""Static contract audit for JAZZ-QUESTS-001."""

from __future__ import annotations

import argparse
import csv
import io
from pathlib import Path

from lupa import LuaRuntime


CORE_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_MAPS_ROOT = CORE_ROOT.parent / "jazz-maps"


class Audit:
    def __init__(self) -> None:
        self.failures: list[str] = []

    def count(self, text: str, fragment: str, expected: int, label: str) -> None:
        actual = text.count(fragment)
        if actual != expected:
            self.failures.append(f"{label}: expected {expected}, found {actual}")

    def contains(self, text: str, fragment: str, label: str) -> None:
        if fragment not in text:
            self.failures.append(f"{label}: missing {fragment!r}")

    def absent(self, text: str, fragment: str, label: str) -> None:
        if fragment in text:
            self.failures.append(f"{label}: stale fragment remains: {fragment!r}")


def unit_marker_block(text: str, handle: int) -> str:
    terminator = f"}}, nil, {handle})"
    end = text.find(terminator)
    if end < 0:
        raise ValueError(f"UnitMarker handle {handle} not found")
    start = text.rfind("PlaceObj('UnitMarker', {", 0, end)
    if start < 0:
        raise ValueError(f"UnitMarker start for handle {handle} not found")
    return text[start : end + len(terminator)]


def read_runtime_csv(path: Path) -> dict[str, dict[str, str]]:
    text = path.read_text(encoding="utf-8-sig")
    lines = text.splitlines(keepends=True)
    if not lines or lines[0].strip() != "sep=,":
        raise ValueError(f"{path}: invalid JA3 localization prefix")
    reader = csv.DictReader(io.StringIO("".join(lines[1:])))
    rows: dict[str, dict[str, str]] = {}
    for row in reader:
        loc_id = row["ID"]
        if loc_id in rows:
            raise ValueError(f"{path}: duplicate localization ID {loc_id}")
        rows[loc_id] = row
    return rows


def audit_lua_syntax(audit: Audit, paths: tuple[Path, ...]) -> None:
    lua = LuaRuntime(unpack_returned_tuples=True)
    compile_lua = lua.eval(
        "function(source, name) "
        "local chunk, err = load(source, name, 't'); "
        "return chunk ~= nil, err "
        "end"
    )
    for path in paths:
        ok, error = compile_lua(path.read_text(encoding="utf-8-sig"), f"@{path}")
        if not ok:
            audit.failures.append(f"Lua syntax {path}: {error}")


def audit_items(audit: Audit, maps_root: Path) -> None:
    items = (maps_root / "items.lua").read_text(encoding="utf-8")
    required = (
        ('gv_Sectors.P17.conflict.locked = false', "P17 conflict unlock"),
        ('Text = T(890000000013004, --[[ModItemQuestsDef RescueHerMan Text]]', "safe J7 localization ID"),
        ('AssignToGroup = "BarrySeal_Recruit"', "Barry recruitment conversation"),
        ('Merc = "Merc_BarrySeal"', "Barry recruitment merc ID"),
        ('TargetUnit = "BarrySeal_Recruit"', "Barry recruitment target"),
        ('Prop = "SuppliesDelivered"', "supply delivery state"),
        ('Name = "BarryJoined"', "Barry joined variable"),
        ('ParamId = "TCE_HostageDead"', "RescueTeam failure transition"),
        ('TargetUnit = "Rebel_Hostage"', "living hostage check"),
        ('Name = "AdvancePaid"', "Dead Pigs advance guard"),
        ('Name = "InjuredRebel1_Healed"', "first wounded variable"),
        ('Name = "InjuredRebel2_Healed"', "second wounded variable"),
        ('Name = "InjuredRebel3_Healed"', "third wounded variable"),
        ('DisplayName = T(890000000013000, --[[ModItemQuestsDef Jazz_Alkatraz DisplayName]]', "Alkatraz title"),
        ('ItemId = "BigDiamond"', "Psycho reward"),
    )
    for fragment, label in required:
        audit.contains(items, fragment, label)
    raiders_anchor = items.find('ParamId = "TCE_RaidersConversation"')
    if raiders_anchor < 0:
        audit.failures.append("RescueHerMan required sector: TCE_RaidersConversation is missing")
    else:
        raiders_block = items[raiders_anchor : raiders_anchor + 220]
        audit.contains(raiders_block, 'QuestId = "RescueHerMan"', "RescueHerMan TCE owner")
        audit.contains(raiders_block, '"J7"', "RescueHerMan required sector")
        audit.absent(raiders_block, '"I3"', "RescueHerMan stale required sector")
    audit.absent(items, "M3_UnderControl", "stale Outlook state")
    audit.absent(items, "T(706580608154, --[[ModItemQuestsDef RescueHerMan Text]]", "reused vanilla J7 localization ID")
    audit.count(items, "setpiece = \"EncounterHerman\"", 2, "J7 EncounterHerman sector events")

    ammo_pair = (
        '\'Icon\', "Mod/FhNNYd/Images/Inventory_Images/AmmoCrate.png",\n'
        '\t\t\'SubIcon\', "Mod/FhNNYd/Images/Inventory_Images/AmmoCrate.png",'
    )
    mines_pair = (
        '\'Icon\', "Mod/FhNNYd/Images/Inventory_Images/MinesBox.png",\n'
        '\t\t\'SubIcon\', "Mod/FhNNYd/Images/Inventory_Images/MinesBox.png",'
    )
    audit.count(items, ammo_pair, 1, "AmmoBox icon pair")
    audit.count(items, mines_pair, 1, "MinesBox icon pair")

    kiki = (maps_root / "UnitData" / "JAZZ_Ernie_Locals_M2_SaveMyFamily_Woman.lua").read_text(encoding="utf-8")
    audit.contains(kiki, "\timmortal = true,", "Kiki immortality companion")
    audit.contains(kiki, "\tImportantNPC = true,", "Kiki important-NPC companion")


def audit_maps(audit: Audit, maps_root: Path) -> None:
    i2 = (maps_root / "Maps" / "qTn3d4w" / "objects.lua").read_text(encoding="utf-8")
    for handle, flag in (
        (1024982262, "InjuredRebel1_Healed"),
        (1867495034, "InjuredRebel2_Healed"),
        (1798783903, "InjuredRebel3_Healed"),
    ):
        block = unit_marker_block(i2, handle)
        audit.count(block, f'Vars = set( "{flag}" )', 1, f"I2 {flag} despawn")
        audit.count(block, f'Prop = "{flag}"', 1, f"I2 {flag} effect")
        audit.absent(block, 'Prop = "InjuredRebels_Healed"', f"I2 {flag} legacy effect")

    m4 = (maps_root / "Maps" / "cd6xgVh" / "objects.lua").read_text(encoding="utf-8")
    for handle in (1762735104, 1096301347, 1357517504, 1850438412, 1304007795):
        block = unit_marker_block(m4, handle)
        audit.count(block, '"M4"', 1, f"M4 payoff marker {handle}")
        audit.absent(block, '"M3"', f"M4 payoff marker {handle} stale sector")

    k4 = (maps_root / "Maps" / "gsSMikN" / "objects.lua").read_text(encoding="utf-8")
    for handle in (1582649701, 1288904357, 1221271075, 1703579100, 1799057228):
        block = unit_marker_block(k4, handle)
        audit.count(block, '"K4"', 1, f"K4 payoff marker {handle}")
        audit.absent(block, '"M4"', f"K4 payoff marker {handle} stale sector")

    j7 = (maps_root / "Maps" / "qJApdx" / "objects.lua").read_text(encoding="utf-8")
    herman = unit_marker_block(j7, 1153589772)
    audit.contains(herman, '"HermanShaking"', "Herman shaking group")
    audit.contains(herman, '"Herman"', "Herman setpiece group")

    k5 = (maps_root / "Maps" / "YWtYj6q" / "objects.lua").read_text(encoding="utf-8")
    barry = unit_marker_block(k5, 2107001001)
    for fragment, label in (
        ('"BarrySeal_Recruit"', "Barry marker group"),
        ('BarryJoined = false', "Barry marker not-yet-joined gate"),
        ('SuppliesDelivered = true', "Barry marker delivery gate"),
        ('Vars = set( "BarryJoined" )', "Barry marker despawn"),
        ('\'UnitDataDefId\', "Merc_BarrySeal"', "Barry marker UnitData"),
    ):
        audit.contains(barry, fragment, label)

    k6 = (maps_root / "Maps" / "bVp47D" / "objects.lua").read_text(encoding="utf-8")
    expected_units = ("ThugCutter", "ThugCutter", "ThugGoon_Stronger", "ThugSniper")
    for index, (handle, unit_id) in enumerate(zip(range(2107001002, 2107001006), expected_units), start=1):
        block = unit_marker_block(k6, handle)
        audit.contains(block, '"DeadPigs_Reinforcements"', f"K6 reinforcement {index} group")
        audit.contains(block, "'Side', \"ally\"", f"K6 reinforcement {index} side")
        audit.contains(block, "Accepted = true", f"K6 reinforcement {index} accepted gate")
        audit.contains(block, "PigsDead = false", f"K6 reinforcement {index} alive gate")
        audit.contains(block, f'\'UnitDataDefId\', "{unit_id}"', f"K6 reinforcement {index} UnitData")
        audit.absent(block, '\n\t\t"Pigs",', f"K6 reinforcement {index} enemy group")


def audit_localization(audit: Audit, core_root: Path, maps_root: Path) -> None:
    modtexts = (maps_root / "ModTextsMaps.csv").read_text(encoding="utf-8-sig")
    for loc_id in range(890000000013000, 890000000013010):
        audit.count(modtexts, f"{loc_id},", 1, f"ModTexts quest ID {loc_id}")
    audit.absent(modtexts, "706580608154,", "stale RescueHerMan ModTexts row")

    russian = read_runtime_csv(core_root / "Russian.csv")
    english = read_runtime_csv(core_root / "English.csv")
    if russian.keys() != english.keys():
        audit.failures.append("Russian.csv and English.csv localization ID sets differ")
    for loc_id in (str(value) for value in range(890000000013000, 890000000013010)):
        for language, rows in (("Russian", russian), ("English", english)):
            row = rows.get(loc_id)
            if not row or not row.get("Translation"):
                audit.failures.append(f"{language} runtime localization missing ID {loc_id}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--core-root", type=Path, default=CORE_ROOT)
    parser.add_argument("--maps-root", type=Path, default=DEFAULT_MAPS_ROOT)
    args = parser.parse_args()

    audit = Audit()
    try:
        maps_root = args.maps_root.resolve()
        audit_lua_syntax(
            audit,
            (
                maps_root / "items.lua",
                maps_root / "InventoryItem" / "JazzQuestItem_AmmoBox.lua",
                maps_root / "InventoryItem" / "JazzQuestItem_MinesBox.lua",
                maps_root / "UnitData" / "JAZZ_Ernie_Locals_M2_SaveMyFamily_Woman.lua",
                maps_root / "Maps" / "qTn3d4w" / "objects.lua",
                maps_root / "Maps" / "cd6xgVh" / "objects.lua",
                maps_root / "Maps" / "gsSMikN" / "objects.lua",
                maps_root / "Maps" / "qJApdx" / "objects.lua",
                maps_root / "Maps" / "YWtYj6q" / "objects.lua",
                maps_root / "Maps" / "bVp47D" / "objects.lua",
            ),
        )
        audit_items(audit, maps_root)
        audit_maps(audit, maps_root)
        audit_localization(audit, args.core_root.resolve(), maps_root)
    except (OSError, UnicodeError, ValueError, csv.Error) as exc:
        audit.failures.append(str(exc))

    if audit.failures:
        for failure in audit.failures:
            print(f"FAIL: {failure}")
        print(f"JAZZ-QUESTS-001 audit failed: {len(audit.failures)} issue(s)")
        return 1
    print("JAZZ-QUESTS-001 static contract: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
