# -*- coding: utf-8 -*-
"""One-shot: cut JAZZ_MuzzleBooster from items/metadata/companions."""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _apply_attach_001 import placeobj_blocks, prop, atomic_write

ROOT = Path(__file__).resolve().parents[2]


def strip_cid(text: str, cid: str) -> tuple[str, int]:
    return re.subn(rf'\n(\t*)"{re.escape(cid)}",', "\n", text)


def main() -> int:
    items = ROOT / "items.lua"
    text = items.read_text(encoding="utf-8")

    removed = False
    for b in reversed(placeobj_blocks(text, "ModItemWeaponComponent")):
        if prop(b.text, "id") != "JAZZ_MuzzleBooster":
            continue
        end = b.end
        if text[end : end + 1] == ",":
            end += 1
        if text[end : end + 1] == "\n":
            end += 1
        text = text[: b.start] + text[end:]
        removed = True
        print("removed ModItem")
        break
    if not removed:
        raise SystemExit("ModItem JAZZ_MuzzleBooster not found")

    text, n = strip_cid(text, "JAZZ_MuzzleBooster")
    print("stripped AvailableComponents", n)

    old_def = "'DefaultComponent', \"JAZZ_MuzzleBooster\""
    new_def = "'DefaultComponent', \"JAZZ_Galil_Brake_Default\""
    c = text.count(old_def)
    print("DefaultComponent replacements", c)
    text = text.replace(old_def, new_def)
    atomic_write(items, text)

    for rel in ("InventoryItem/AR15.lua", "InventoryItem/M4Commando.lua"):
        p = ROOT / rel
        t = p.read_text(encoding="utf-8")
        t2, n = strip_cid(t, "JAZZ_MuzzleBooster")
        if n:
            atomic_write(p, t2)
            print("companion", rel, n)
        else:
            print("companion unchanged", rel)

    meta = ROOT / "metadata.lua"
    mt = meta.read_text(encoding="utf-8")
    pat = re.compile(
        r"\t\tPlaceObj\('ModResourcePreset', \{\n"
        r"\t\t\t'Class', \"WeaponComponent\",\n"
        r"\t\t\t'Id', \"JAZZ_MuzzleBooster\",\n"
        r"\t\t\t'ClassDisplayName', \"Weapon Component\",\n"
        r"\t\t\}\),\n"
    )
    mt2, n = pat.subn("", mt, count=1)
    if n != 1:
        raise SystemExit(f"metadata remove count={n}")
    atomic_write(meta, mt2)
    print("metadata removed")

    leftover = []
    for p in (items, meta, ROOT / "InventoryItem/AR15.lua", ROOT / "InventoryItem/M4Commando.lua"):
        t = p.read_text(encoding="utf-8")
        if "JAZZ_MuzzleBooster" in t:
            leftover.append(str(p))
    if leftover:
        raise SystemExit(f"leftover refs: {leftover}")
    print("ok: no leftover JAZZ_MuzzleBooster")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
