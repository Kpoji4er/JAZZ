"""Idempotent test-unit graph for JAZZ-APPEAR-001 vanilla Torso/Head mappings.

python docs/tools/_install_vanilla_armor_visuals.py
python docs/tools/_install_vanilla_armor_visuals.py --apply
Requires the game/editor closed for --apply. Does not rewrite the runtime Lua map.
"""
import argparse
import re
import subprocess
from pathlib import Path
from lupa import LuaRuntime
from _integrate_sr3m import add_metadata

ROOT = Path(__file__).resolve().parents[2]
UNITS = ROOT.parent / "jazz-units"

TORSO = ("FlakM1955", "FlakM69", "IBALight", "IBA", "IBAFull")
HEAD = (
    "UniformCap", "ConstructionHelmet", "AdrianHelmet", "SovietHelm", "M1Helm",
    "Stahlhelm", "PASGTHelm", "6b7Helm", "TwaronHelm", "TwaronHelmHeavy",
    "ZylonHelm", "ZylonHelmHeavy", "GuardianHelm", "GuardianHelmHeavy",
)

def rows():
    for item in TORSO:
        yield item, "Torso"
    for item in HEAD:
        yield item, "Head"

def make_companion(template, uid, armor, slot, label):
    text = (
        template
        .replace("JAZZ_Legion_ArmorTest", uid)
        .replace("JazzArmor_ImprovisedCuirass", armor)
        .replace("cuirass + MP40", label + " + MP40")
    )
    if slot == "Head":
        text = text.replace('TryEquip(items, "Torso", "Armor")', 'TryEquip(items, "Head", "Armor")')
    return text

def already_registered(items_text, uid):
    return f"'Id', \"{uid}\"" in items_text or f'Id = "{uid}"' in items_text

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    running = subprocess.run(
        [
            "powershell", "-NoProfile", "-Command",
            "Get-Process JA3,JA3Debug,ged -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Id",
        ],
        capture_output=True, text=True,
    )
    if args.apply:
        assert not running.stdout.strip(), "Game/editor is open; cannot install over its loaded data"
    items_path = UNITS / "items.lua"
    meta_path = UNITS / "metadata.lua"
    before = {items_path: items_path.read_bytes(), meta_path: meta_path.read_bytes()}
    items_text = before[items_path].decode("utf-8-sig")
    meta_text = before[meta_path].decode("utf-8-sig")
    template = (UNITS / "UnitData/JAZZ_Legion_ArmorTest.lua").read_text(encoding="utf-8-sig")
    lua = LuaRuntime()
    writes = {}
    added = []
    for item, slot in rows():
        uid = "JAZZ_Legion_ArmorTest_" + item
        armor = "JazzArmor_" + item
        companion = make_companion(template, uid, armor, slot, item)
        lua.compile(companion)
        writes[UNITS / "UnitData" / (uid + ".lua")] = companion.encode()
        if already_registered(items_text, uid):
            continue
        props = companion[companion.index("    comment ="):companion.rfind("}")]
        props = re.sub(r"^    (\w+) = ", r"    '\1', ", props, flags=re.M)
        record = (
            "PlaceObj('ModItemUnitDataCompositeDef', {\n"
            "    'Group', \"JAZZ Tests\",\n"
            f"    'Id', \"{uid}\",\n"
            + props
            + "}),"
        )
        pos = items_text.rfind("}")
        items_text = items_text[:pos] + record + "\n" + items_text[pos:]
        meta_text = add_metadata(meta_text, "code", [f'"UnitData/{uid}.lua"'])
        meta_text = add_metadata(
            meta_text,
            "affected_resources",
            [
                "PlaceObj('ModResourcePreset', { 'Class', \"UnitDataCompositeDef\", "
                f"'Id', \"{uid}\", 'ClassDisplayName', \"Unit\" }})"
            ],
        )
        added.append(uid)
    lua.compile(items_text)
    lua.compile(meta_text)
    writes[items_path] = items_text.encode("utf-8")
    writes[meta_path] = meta_text.encode("utf-8")
    if not args.apply:
        print("PASS compile; would add", len(added), "ModItems;", len(writes), "files")
        return
    for path, data in before.items():
        assert path.read_bytes() == data, "Concurrent edit " + str(path)
    for path, data in writes.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        assert path.read_bytes() == data
    print("INSTALLED", len(added), "new ModItems;", len(list(rows())), "companions written")

if __name__ == "__main__":
    main()
