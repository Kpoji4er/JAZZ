# -*- coding: utf-8 -*-
"""Static validation for ATTACH-001 / WEAPONS-002..005 wave."""
from __future__ import annotations

import csv
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
errors: list[str] = []
warns: list[str] = []


def ok(msg: str) -> None:
    print(f"PASS  {msg}")


def fail(msg: str) -> None:
    errors.append(msg)
    print(f"FAIL  {msg}")


def warn(msg: str) -> None:
    warns.append(msg)
    print(f"WARN  {msg}")


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def check_balance(name: str, text: str) -> None:
    brace = text.count("{") - text.count("}")
    bracket = text.count("[") - text.count("]")
    paren = text.count("(") - text.count(")")
    if brace != 0:
        fail(f"{name}: brace imbalance {brace}")
    else:
        ok(f"{name}: braces balanced")
    if bracket != 0:
        fail(f"{name}: bracket imbalance {bracket}")
    else:
        ok(f"{name}: brackets balanced")
    if paren != 0:
        warn(f"{name}: paren imbalance {paren} (known pre-existing if -12)")
    else:
        ok(f"{name}: parens balanced")


def check_code_loaded(names: list[str]) -> None:
    meta = read(ROOT / "metadata.lua")
    for name in names:
        if f'"{name}"' in meta or f"'{name}'" in meta:
            ok(f"metadata loads {name}")
        else:
            fail(f"metadata missing {name}")


def grab_prop(text: str, name: str) -> str | None:
    m = re.search(rf"{name}\s*=\s*([^\n,]+)", text)
    return m.group(1).strip().strip('"') if m else None


def main() -> int:
    items = read(ROOT / "items.lua")
    meta = read(ROOT / "metadata.lua")
    check_balance("items.lua", items)
    check_balance("metadata.lua", meta)

    # ATTACH MagSizeSet
    if 'id = "MagazineSizeSet"' in items and 'ModificationType = "Set"' in items:
        ok("MagazineSizeSet effect present")
    else:
        fail("MagazineSizeSet effect missing")
    if 'id = "JAZZ_MagLarge"' in items:
        fail("generic JAZZ_MagLarge still defined")
    else:
        ok("generic JAZZ_MagLarge removed")
    for cid in ("JAZZ_MagLarge_50", "JAZZ_MagLarge_28", "JAZZ_MagLarge_30_45"):
        if f'id = "{cid}"' in items:
            ok(f"{cid} defined")
        else:
            fail(f"{cid} missing")
    mag_mult = re.findall(r'id = "(JAZZ_Mag[^"]+)".{0,1800}?MagazineSizeMultiplier', items, re.S)
    if mag_mult:
        fail(f"live Mag* still use MagazineSizeMultiplier: {mag_mult[:8]}")
    else:
        ok("no JAZZ_Mag* MagazineSizeMultiplier")
    block = items[items.rfind("PlaceObj('ModItemWeaponComponent'", 0, items.find('id = "JAZZ_MagLarge_30_45"')) : items.find('id = "JAZZ_MagLarge_30_45"') + 40]
    if "MagazineSizeSet" in block and "'Value', 45" in block:
        ok("JAZZ_MagLarge_30_45 = Set(45)")
    else:
        fail("JAZZ_MagLarge_30_45 not absolute Set 45")

    check_code_loaded(
        [
            "Code/System_WeaponComponent_Set.lua",
            "Code/System_WeaponResourceMaintenance.lua",
            "Code/System_WeaponRemovableModify.lua",
            "Code/System_DisposableLaunchers.lua",
            "Code/System_ReloadStyle.lua",
        ]
    )
    set_lua = read(ROOT / "Code/System_WeaponComponent_Set.lua")
    if 'ModificationType == "Set"' in set_lua and "mul = 0" in set_lua:
        ok("SetWeaponComponent Set branch present")
    else:
        fail("SetWeaponComponent Set branch missing")

    # WEAPONS-003 anchors
    anchors = {
        "AK74": (14, 15),
        "AKM": (24, 26),
        "FNFAL": (42, 44),
    }
    for wid, (lo, hi) in anchors.items():
        t = read(ROOT / "InventoryItem" / f"{wid}.lua")
        r = int(grab_prop(t, "Recoil") or -1)
        if lo <= r <= hi:
            ok(f"{wid} Recoil={r} in [{lo},{hi}]")
        else:
            fail(f"{wid} Recoil={r} outside [{lo},{hi}]")
        for prop in ("WeaponMass", "CyclicRPM", "WeaponSizeClass", "BurstLimiter"):
            if grab_prop(t, prop) is None:
                fail(f"{wid} missing {prop}")
    cth = read(ROOT / "Code/AccuracyRangeCTH.lua")
    if "marks_factor" in cth and "shooter_factor" in cth and "0.5 * strength_factor + 0.5 * marks_factor" in cth:
        ok("CTH shooter_factor Marks 50/50")
    else:
        fail("CTH Marks shooter_factor missing")
    aw = read(ROOT / "CharacterEffect/AutoWeapons.lua")
    if "с 5" in aw or "5го" in aw or "5-го" in aw:
        fail("AutoWeapons still mentions 5th shot")
    else:
        ok("AutoWeapons text without 5th-shot claim")

    # 9x19 order
    micro = int(grab_prop(read(ROOT / "InventoryItem/MicroUZI.lua"), "Recoil") or 0)
    sterling = int(grab_prop(read(ROOT / "InventoryItem/Sterling.lua"), "Recoil") or 0)
    if micro > sterling:
        ok(f"9x19 MicroUZI({micro}) > Sterling({sterling})")
    else:
        fail(f"9x19 MicroUZI({micro}) !> Sterling({sterling})")

    m16 = read(ROOT / "InventoryItem/M16A2.lua")
    an94 = read(ROOT / "InventoryItem/AN94.lua")
    if grab_prop(m16, "BurstLimiter") == "3" and int(grab_prop(m16, "BurstShots") or 99) <= 3:
        ok("M16A2 BurstLimiter=3")
    else:
        fail("M16A2 BurstLimiter/BurstShots wrong")
    if grab_prop(an94, "BurstLimiter") == "2" and grab_prop(an94, "BurstShots") == "2":
        ok("AN94 BurstLimiter/BurstShots=2")
    else:
        fail("AN94 BurstLimiter/BurstShots wrong")

    # WEAPONS-005
    m72 = read(ROOT / "InventoryItem/M72LAW.lua")
    if "DisposableLauncher = true" in m72:
        ok("M72 DisposableLauncher=true")
    else:
        fail("M72 DisposableLauncher missing")
    if "M72 LAW" in m72:
        ok("M72 display name readable")
    else:
        warn("M72 display name check inconclusive")
    disp = read(ROOT / "Code/System_DisposableLaunchers.lua")
    if "SpawnSpentTube" in disp and "DisposableLauncher" in disp:
        ok("Disposable launcher runtime present")
    else:
        fail("Disposable launcher runtime incomplete")

    # WEAPONS-002
    maint = read(ROOT / "Code/System_WeaponResourceMaintenance.lua")
    for needle in (
        "GetRepairBarrelPartsCost",
        "DamageWeaponResourceMaxPercent",
        "JAZZ_IsRemovableWeaponComponent",
        "JAZZ_RemoveRemovableAttachment",
        "JAZZ_InstallRemovableAttachment",
        "FineSteelPipe",
        "GetDisplayJamChancePercent",
    ):
        if needle in maint:
            ok(f"WEAPONS-002 has {needle}")
        else:
            fail(f"WEAPONS-002 missing {needle}")
    if 'id = "JAZZ_BarrelParts"' in items or "JAZZ_BarrelParts" in items:
        ok("JAZZ_BarrelParts present in items")
    else:
        fail("JAZZ_BarrelParts missing from items")
    for legacy in ("FineSteelPipe", "OpticalLens", "Microchip"):
        type_hits = len(re.findall(rf"'Type',\s*\"{legacy}\"", items))
        item_hits = len(re.findall(rf"'item',\s*\"{legacy}\"", items))
        if type_hits or item_hits:
            fail(f"legacy cost leftovers {legacy}: Type={type_hits} item={item_hits}")
        else:
            ok(f"no craft Type/item leftovers for {legacy}")
    if re.search(r"'Id',\s*\"Parts\".{0,200}optical_lens", items, re.S):
        fail("corrupted Parts ModItem (optical_lens icon) — restore bak_legacy_parts")
    else:
        ok("Parts ModItem not corrupted by Id rewrite")
    rem = read(ROOT / "Code/System_WeaponRemovableModify.lua")
    if "ModifyWeaponDlg" in rem and "JAZZ_InstallRemovableAttachment" in rem:
        ok("ModifyWeapon removable hooks present")
    else:
        fail("ModifyWeapon removable hooks missing")
    if "JazzMoveItem_BeforeRemovable" in rem or ("function MoveItem" in rem and "JAZZ_InstallRemovableAttachment" in rem):
        ok("MoveItem DnD removable hooks present")
    else:
        fail("MoveItem DnD removable hooks missing")

    # WEAPONS-004
    reload = read(ROOT / "Code/System_ReloadStyle.lua")
    if "JazzPerRoundStyles" in reload and "JazzResolveReloadWeapon" in reload:
        ok("ReloadStyle helpers present")
    else:
        fail("ReloadStyle helpers missing")
    if "CombatActions.Reload" in reload:
        fail("ReloadStyle still patches CombatActions.Reload (should be ModItem full replace)")
    else:
        ok("ReloadStyle does not patch CombatActions.Reload")
    if 'id = "Reload"' in items and "IsPerRoundReload" in items and "GetReloadUnitAP" in items:
        ok("items.lua ModItemCombatAction Reload has per-round hooks")
    else:
        fail("items.lua missing ModItemCombatAction Reload per-round hooks")
    if re.search(r"'Class',\s*\"CombatAction\",\s*\n\s*'Id',\s*\"Reload\"", meta):
        ok("metadata registers CombatAction Reload")
    else:
        fail("metadata missing ModResourcePreset CombatAction Reload")
    for wid, style in (("R870", "Tube"), ("DoubleBarrelShotgun", "Break"), ("SWModel10", "Revolver")):
        t = read(ROOT / "InventoryItem" / f"{wid}.lua")
        if grab_prop(t, "ReloadStyle") == style or f'{wid} = "{style}"' in reload:
            ok(f"{wid} ReloadStyle={style}")
        else:
            fail(f"{wid} ReloadStyle!={style}")
    if 'Welrod = "Revolver"' in reload:
        fail("Welrod incorrectly tagged Revolver in runtime map")
    else:
        ok("Welrod not forced to Revolver in runtime map")

    # CSV columns
    with (ROOT / "docs/technical/weapons/data/weapons.csv").open(encoding="utf-8", newline="") as f:
        cols = next(csv.reader(f))
    for col in ("weapon_mass", "cyclic_rpm", "weapon_size_class", "burst_limiter", "reload_style"):
        if col in cols:
            ok(f"weapons.csv has {col}")
        else:
            fail(f"weapons.csv missing {col}")

    # Loc IDs used by wave
    ru = read(ROOT / "Russian.csv")
    en = read(ROOT / "English.csv")
    for loc_id in ("543656846802", "990002001", "990002010", "990002011", "990002012", "253479657834"):
        if loc_id in ru and loc_id in en:
            ok(f"loc {loc_id} in RU+EN")
        else:
            fail(f"loc {loc_id} missing RU/EN")

    print()
    print(f"Summary: {len(errors)} FAIL, {len(warns)} WARN")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
