"""Read-only verification of the installed AK-103 (JAZZ-WEAPON-AK103-001).

    python docs/tools/_check_ak103.py

Checks only what static analysis can prove: Lua compiles, the ModItem in
items.lua matches the companion, every entity resolves to a mesh, material,
DDS and fallback, the component visuals exist, and the icon matches the
accepted AK74/AKM geometry. Does not replace a run in JA3.
"""

import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

from PIL import Image
from lupa import LuaRuntime

ROOT = Path(__file__).resolve().parents[2]
ASSETS = ROOT.parent / "jazz_assets"
WEAPON = "AK103"
ENTITY = "AKR_" + WEAPON
ENTITIES = [ENTITY, ENTITY + "_Handguard", ENTITY + "_Magazine", ENTITY + "_Muzzle",
            ENTITY + "_Stock", ENTITY + "_StockFolded"]
VISUAL_SLOTS = {
    "JAZZ_MagNormal": ENTITY + "_Magazine",
    "JAZZ_Handguard": ENTITY + "_Handguard",
    "JAZZ_DefMuzzle": ENTITY + "_Muzzle",
    "JAZZ_StockLightUnFolded": ENTITY + "_Stock",
    "JAZZ_StockLightFolded": ENTITY + "_StockFolded",
}
ICON_SIZE = (324, 165)

failures = []


def check(label, condition, detail=""):
    if condition:
        print(f"  ok    {label}")
    else:
        failures.append(f"{label} {detail}".strip())
        print(f"  FAIL  {label} {detail}".rstrip())


def main():
    print("Lua compiles")
    texts = {}
    for rel, base in [("items.lua", ROOT), ("metadata.lua", ROOT),
                      (f"InventoryItem/{WEAPON}.lua", ROOT),
                      ("items.lua", ASSETS), ("metadata.lua", ASSETS)]:
        path = base / rel
        texts[path] = path.read_text(encoding="utf-8")
        try:
            LuaRuntime().compile(texts[path])
            check(f"{base.name}/{rel}", True)
        except Exception as exc:  # noqa: BLE001 - report, do not abort the audit
            check(f"{base.name}/{rel}", False, str(exc))

    items = texts[ROOT / "items.lua"]
    companion = texts[ROOT / f"InventoryItem/{WEAPON}.lua"]

    print("ModItem matches companion")
    block = items[items.index(f"'Id', \"{WEAPON}\""):]
    for field in ("Damage", "WeaponRange", "AimAccuracy", "ShootAP", "CyclicRPM",
                  "MagazineSize", "Cost", "Tier", "RestockWeight", "Noise", "Recoil"):
        want = re.search(r"^\t" + field + r" = ([^,\n]+),", companion, re.M)
        got = re.search(r"'" + field + r"', ([^,\n]+),", block)
        check(field, bool(want and got) and want[1] == got[1],
              f"companion={want and want[1]} moditem={got and got[1]}")

    print("Weapon contract")
    check("object_class AssaultRifle", 'object_class = "AssaultRifle"' in companion)
    check("caliber 7.62x39", 'Caliber = "JAZZ_Caliber_762x39"' in companion)
    check("fxClass AKM", 'fxClass = "AKM"' in companion)
    check("HolsterSlot Shoulder", 'HolsterSlot = "Shoulder"' in companion)
    check("no ModifyRightHandGrip (pistol grip present)",
          "ModifyRightHandGrip" not in companion)
    check("entity bound", f'Entity = "{ENTITY}"' in companion)
    check("registered in metadata.code",
          f'"InventoryItem/{WEAPON}.lua"' in texts[ROOT / "metadata.lua"])

    print("Component visuals")
    for component, entity in VISUAL_SLOTS.items():
        pattern = (r'ApplyTo = "' + WEAPON + r'", Entity = "' + entity + '"')
        check(component, bool(re.search(pattern, items)))

    print("Entity resources")
    asset_meta = texts[ASSETS / "metadata.lua"]
    for ent in ENTITIES:
        path = ASSETS / "Entities" / (ent + ".ent")
        if not path.is_file():
            check(ent, False, "missing .ent")
            continue
        missing = []
        for node in ET.parse(path).findall(".//mesh") + ET.parse(path).findall(".//material"):
            rel = node.attrib["file"]
            if not (ASSETS / "Entities" / rel).is_file():
                missing.append(rel)
        for node in ET.parse(path).findall(".//material"):
            mtl = ET.parse(ASSETS / "Entities" / node.attrib["file"])
            for tag in mtl.getroot().iter():
                name = tag.get("Name")
                if not name:
                    continue
                for folder in ("Textures", "Textures/Fallbacks"):
                    if not (ASSETS / "Entities" / folder / name).is_file():
                        missing.append(f"{folder}/{name}")
        registered = f'"{ent}"' in asset_meta and f'"Entities/{ent}.lua"' in asset_meta
        check(ent, not missing and registered and (ASSETS / "Entities" / (ent + ".lua")).is_file(),
              ("missing " + ", ".join(missing)) if missing else ("not registered" if not registered else ""))

    print("Icon")
    icon = ROOT / f"WeaponIcons/{WEAPON}.png"
    if icon.is_file():
        image = Image.open(icon).convert("RGBA")
        box = image.getchannel("A").getbbox()
        content = (box[2] - box[0], box[3] - box[1])
        reference = Image.open(ROOT / "WeaponIcons/AK74.png").convert("RGBA")
        ref_box = reference.getchannel("A").getbbox()
        ref_content = (ref_box[2] - ref_box[0], ref_box[3] - ref_box[1])
        check("size 324x165", image.size == ICON_SIZE, str(image.size))
        check("content close to AK74",
              abs(content[0] - ref_content[0]) <= 20 and abs(content[1] - ref_content[1]) <= 20,
              f"{content} vs AK74 {ref_content}")
        check("outline darker than slot", outline_value(image) < 40, f"{outline_value(image):.1f} vs bg 42")
    else:
        check("icon present", False)

    print()
    if failures:
        print(f"FAIL: {len(failures)} problem(s)")
        for line in failures:
            print("  -", line)
        return 1
    print(f"PASS: {WEAPON} Lua/ModItem equality, {len(ENTITIES)} entities, "
          f"{len(VISUAL_SLOTS)} visual bindings, DDS/fallback pairs, icon vs AK74. "
          "Not a substitute for a run in JA3.")
    return 0


def outline_value(image):
    """Mean brightness of the dilated silhouette ring composited on #2a2a2a."""
    import numpy as np
    from PIL import ImageFilter

    data = np.array(image).astype(float)
    rgb, alpha = data[..., :3], data[..., 3] / 255.0
    composited = rgb * alpha[..., None] + 42.0 * (1 - alpha[..., None])
    solid = alpha > 0.9
    grown = np.array(
        Image.fromarray((solid * 255).astype("uint8")).filter(ImageFilter.MaxFilter(9))
    ) > 127
    ring = grown & ~solid
    return float(composited[ring].mean())


if __name__ == "__main__":
    sys.exit(main())
