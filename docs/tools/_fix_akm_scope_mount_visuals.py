# -*- coding: utf-8 -*-
"""Add missing AKM dovetail→rail Mount visuals on western scopes that lack ApplyTo=AKM."""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, "docs/tools")
from _apply_attach_001 import placeobj_blocks, prop, atomic_write

ROOT = Path(__file__).resolve().parents[2]
ITEMS = ROOT / "items.lua"

# Same adapter used by ACOG / Scout / western reflex on AKM.
AKM_MOUNT_VISUAL = """\
\t\t\t\t\t\t\t\tPlaceObj('WeaponComponentVisual', {
\t\t\t\t\t\t\t\t\tEntity = "WeaponAttA_MountAK47",
\t\t\t\t\t\t\t\t\tSlot = "Mount",
\t\t\t\t\t\t\t\t\tApplyTo = "AKM",
\t\t\t\t\t\t\t\t}),
"""

# Scopes that can go on AKM but currently miss AKM Mount visual.
TARGETS = {
    "JAZZ_Scope_12x",
    "JAZZ_Scope_6x",
    "JAZZ_NightScope",
}


def has_akm_mount(block_text: str) -> bool:
    for m in re.finditer(r"PlaceObj\('WeaponComponentVisual', \{(.*?)\}\),", block_text, re.S):
        chunk = m.group(1)
        if (
            'ApplyTo = "AKM"' in chunk
            and 'Slot = "Mount"' in chunk
            and "WeaponAttA_MountAK47" in chunk
        ):
            return True
    return False


def ensure_akm_mount(block_text: str) -> tuple[str, bool]:
    if has_akm_mount(block_text):
        return block_text, False
    # Insert after Visuals = { opening, before first visual OR after first scope visual.
    # Prefer: after the generic Scope entity visual (no ApplyTo), before weapon-specific mounts.
    m = re.search(r"(Visuals = \{\n)", block_text)
    if not m:
        raise ValueError("no Visuals block")
    # Find first PlaceObj('WeaponComponentVisual' that already has Slot = Mount — insert before it
    mount_idx = block_text.find('Slot = "Mount"')
    if mount_idx != -1:
        # walk back to PlaceObj start of that visual
        start = block_text.rfind("PlaceObj('WeaponComponentVisual'", 0, mount_idx)
        if start != -1:
            return block_text[:start] + AKM_MOUNT_VISUAL + block_text[start:], True
    # else append before closing of Visuals
    close = block_text.rfind("\n\t\t\t\t\t\t},")
    # Visuals close is typically after all visuals — find `Visuals = {` then matching
    # Safer: insert right after first visual's closing `}),`
    first_vis_end = re.search(
        r"PlaceObj\('WeaponComponentVisual', \{[\s\S]*?\t\t\t\t\t\t\t\t\}\),",
        block_text,
    )
    if first_vis_end:
        i = first_vis_end.end()
        return block_text[:i] + "\n" + AKM_MOUNT_VISUAL + block_text[i:], True
    raise ValueError("could not find insertion point")


def main() -> int:
    text = ITEMS.read_text(encoding="utf-8")
    changed = 0
    for block in reversed(placeobj_blocks(text, "ModItemWeaponComponent")):
        cid = prop(block.text, "id")
        if cid not in TARGETS:
            continue
        new, did = ensure_akm_mount(block.text)
        if did:
            text = text[: block.start] + new + text[block.end :]
            changed += 1
            print("added AKM Mount visual ->", cid)
        else:
            print("already has AKM Mount ->", cid)
    if changed:
        atomic_write(ITEMS, text)
    print("changed", changed)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
