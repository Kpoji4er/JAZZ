"""Restore the three Mosin Barrel components if they vanished from items.lua.

The weapon still lists JAZZ_Mosin1891 / M38 / Obrez, but a concurrent items.lua
rewrite can drop the ModItemWeaponComponent records. This puts the last committed
definitions back in front of JAZZ_BarrelsDefs. Dry-run unless --apply.

python docs/tools/_restore_mosin_barrels.py [--apply]
"""
import argparse
import hashlib
import shutil
from pathlib import Path

from lupa import LuaRuntime

from _integrate_sr3m import ROOT, write

IDS = ("JAZZ_Mosin1891", "JAZZ_MosinM38", "JAZZ_MosinObrez")
MARKER = "\t\t\t\tPlaceObj('ModItemWeaponComponent', {\n\t\t\t\t\tDisplayName = T(467118505377, --[[ModItemWeaponComponent JAZZ_BarrelsDefs DisplayName]] \"Заводской ствол\"),"
BLOCK = """\t\t\t\tPlaceObj('ModItemWeaponComponent', { id = "JAZZ_Mosin1891", group = "Barrel", Slot = "Barrel", Cost = 100, Icon = "UI/Icons/Upgrades/default_barrel",
 DisplayName = T(761915302104, "Винтовка образца 1891 года"),
 ModificationEffects = { "JAZZ_MosinMass", "JAZZ_MosinDamageDelta", "JAZZ_MosinCritDelta" },
 Parameters = { PlaceObj('PresetParamNumber', { 'Name', "MosinMass", 'Value', 55, 'Tag', "<MosinMass>" }),
PlaceObj('PresetParamNumber', { 'Name', "MosinDamageDelta", 'Value', 0, 'Tag', "<MosinDamageDelta>" }),
PlaceObj('PresetParamNumber', { 'Name', "MosinCritDelta", 'Value', 0, 'Tag', "<MosinCritDelta>" }) }, Visuals = {},
}),
				PlaceObj('ModItemWeaponComponent', { id = "JAZZ_MosinM38", group = "Barrel", Slot = "Barrel", BlockSlots = { "Scope" }, Cost = 100, Icon = "UI/Icons/Upgrades/default_barrel",
 DisplayName = T(761915302105, "Карабин М38"),
 ModificationEffects = { "JAZZ_MosinMass", "JAZZ_MosinDamageDelta", "JAZZ_MosinCritDelta", "IncreaseShotAP", "BarrelRangeReduce", "ReduceAimAccuracy15Percent", "BarrelGroupingReduce", "BarrelBulletDropReduce", "CloseRangeDecrease", "CloseRangeFactorIncrease", "BarrelRecoilIncrease" },
 Parameters = { PlaceObj('PresetParamNumber', { 'Name', "MosinMass", 'Value', 34, 'Tag', "<MosinMass>" }),
PlaceObj('PresetParamNumber', { 'Name', "MosinDamageDelta", 'Value', -2, 'Tag', "<MosinDamageDelta>" }),
PlaceObj('PresetParamNumber', { 'Name', "MosinCritDelta", 'Value', 0, 'Tag', "<MosinCritDelta>" }),
PlaceObj('PresetParamNumber', { 'Name', "ShotAP", 'Value', -1, 'Tag', "<ShotAP>" }),
PlaceObj('PresetParamNumber', { 'Name', "BarrelRangeReduce", 'Value', 14, 'Tag', "<BarrelRangeReduce>" }),
PlaceObj('PresetParamNumber', { 'Name', "AimAccuracyPercent", 'Value', 85, 'Tag', "<AimAccuracyPercent>" }),
PlaceObj('PresetParamNumber', { 'Name', "BarrelGroupingReduce", 'Value', 95, 'Tag', "<BarrelGroupingReduce>" }),
PlaceObj('PresetParamNumber', { 'Name', "BulletDropReduce", 'Value', 85, 'Tag', "<BulletDropReduce>" }),
PlaceObj('PresetParamNumber', { 'Name', "CloseRangeDecrease", 'Value', 4, 'Tag', "<CloseRangeDecrease>" }),
PlaceObj('PresetParamNumber', { 'Name', "CloseRangeFactorIncrease", 'Value', 10, 'Tag', "<CloseRangeFactorIncrease>" }),
PlaceObj('PresetParamNumber', { 'Name', "BarrelRecoilIncrease", 'Value', 2, 'Tag', "<BarrelRecoilIncrease>" }) }, Visuals = {},
}),
				PlaceObj('ModItemWeaponComponent', { id = "JAZZ_MosinObrez", group = "Barrel", Slot = "Barrel", BlockSlots = { "Scope" }, Cost = 100, Icon = "UI/Icons/Upgrades/default_barrel",
 DisplayName = T(761915302106, "Обрез"), Description = T(761915302107, "Укороченные ствол и ложа без полноценного приклада. Быстрее стреляет и удобнее навскидку вблизи, но значительно хуже прицельно и на дистанции."),
 ModificationEffects = { "JAZZ_MosinMass", "JAZZ_MosinDamageDelta", "JAZZ_MosinCritDelta", "IncreaseShotAP", "BarrelRangeReduce", "ReduceAimAccuracy15Percent", "BarrelGroupingReduce", "BarrelBulletDropReduce", "CloseRangeDecrease", "CloseRangeFactorIncrease", "BarrelRecoilIncrease", "DecreaseMaxAimActions" },
 Parameters = { PlaceObj('PresetParamNumber', { 'Name', "MosinMass", 'Value', 18, 'Tag', "<MosinMass>" }),
PlaceObj('PresetParamNumber', { 'Name', "MosinDamageDelta", 'Value', -8, 'Tag', "<MosinDamageDelta>" }),
PlaceObj('PresetParamNumber', { 'Name', "MosinCritDelta", 'Value', -15, 'Tag', "<MosinCritDelta>" }),
PlaceObj('PresetParamNumber', { 'Name', "ShotAP", 'Value', -3, 'Tag', "<ShotAP>" }),
PlaceObj('PresetParamNumber', { 'Name', "BarrelRangeReduce", 'Value', 42, 'Tag', "<BarrelRangeReduce>" }),
PlaceObj('PresetParamNumber', { 'Name', "AimAccuracyPercent", 'Value', 31, 'Tag', "<AimAccuracyPercent>" }),
PlaceObj('PresetParamNumber', { 'Name', "BarrelGroupingReduce", 'Value', 78, 'Tag', "<BarrelGroupingReduce>" }),
PlaceObj('PresetParamNumber', { 'Name', "BulletDropReduce", 'Value', 38, 'Tag', "<BulletDropReduce>" }),
PlaceObj('PresetParamNumber', { 'Name', "CloseRangeDecrease", 'Value', 14, 'Tag', "<CloseRangeDecrease>" }),
PlaceObj('PresetParamNumber', { 'Name', "CloseRangeFactorIncrease", 'Value', 25, 'Tag', "<CloseRangeFactorIncrease>" }),
PlaceObj('PresetParamNumber', { 'Name', "BarrelRecoilIncrease", 'Value', 10, 'Tag', "<BarrelRecoilIncrease>" }),
PlaceObj('PresetParamNumber', { 'Name', "MaxAimActionsDecrease", 'Value', 2, 'Tag', "<MaxAimActionsDecrease>" }) }, Visuals = {},
}),
"""


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--apply", action="store_true")
    p.add_argument("--backup", type=Path,
                   default=ROOT.parent.parent / "JaWeapons/Weapons/_mosin_jazz_build/barrel-restore-backup")
    args = p.parse_args()
    path = ROOT / "items.lua"
    items = path.read_text(encoding="utf-8-sig")
    companion = (ROOT / "InventoryItem/Mosin.lua").read_text(encoding="utf-8")
    for ident in IDS:
        assert f'"{ident}"' in companion and f'"{ident}"' in items, ident
        present = f'id = "{ident}"' in items
        print(f"{ident}: weapon lists it; component def {'present' if present else 'MISSING'}")
    if all(f'id = "{ident}"' in items for ident in IDS):
        print("Nothing to restore.")
        return
    assert MARKER in items, "JAZZ_BarrelsDefs anchor missing"
    assert items.count(MARKER) == 1
    new_items = items.replace(MARKER, BLOCK + MARKER, 1)
    for ident in IDS:
        assert new_items.count(f'id = "{ident}"') == 1, ident
    assert 'BlockSlots = { "Scope" }' in new_items
    LuaRuntime().compile(new_items)
    print("Scope blocked on M38/Obrez; long rifle has no BlockSlots.")
    if not args.apply:
        print("Dry run. Re-run with --apply, game and Mod Editor closed.")
        return
    args.backup.mkdir(parents=True, exist_ok=True)
    stamp = args.backup / f"items.lua.{hashlib.sha256(path.read_bytes()).hexdigest()[:12]}"
    if not stamp.exists():
        shutil.copy2(path, stamp)
    tmp = path.with_name("items.lua.mosin-restore-tmp")
    write(tmp, new_items)
    tmp.replace(path)
    print("wrote items.lua")


if __name__ == "__main__":
    main()
