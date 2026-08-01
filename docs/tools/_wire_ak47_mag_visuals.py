# -*- coding: utf-8 -*-
"""Wire J_AK47_Mag onto AK47 magazine comps that lack a dedicated mesh.

Custom entity J_AK47 does not accept vanilla WeaponAttA_MagazineAK47_* attaches.
Only J_AK47_Mag exists in jazz_assets — use it for Normal/Large/Quick until
dedicated meshes exist.

Do NOT force J_AK47_Mag on MagDrum: AK47 drum intentionally uses AKM's
WeaponAttA_MagazineRPK74_03 (owner: temporary until custom drum).
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ITEMS = ROOT / "items.lua"
sys.path.insert(0, str(ROOT / "docs" / "tools"))
from _apply_attach_001 import placeobj_blocks, prop

ENTITY = "J_AK47_Mag"
WEAPON = "AK47"
# From InventoryItem/AK47.lua Magazine AvailableComponents — exclude MagDrum
COMPS = [
    "JAZZ_MagNormal",
    "JAZZ_MagLarge_30_40",
    "JAZZ_MagLarge_30_45",
    "JAZZ_MagQuick_AK",
]
VISUAL_TEMPLATE = (
    "\t\t\t\t\t\t\t\tPlaceObj('WeaponComponentVisual', {\n"
    f'\t\t\t\t\t\t\t\t\tApplyTo = "{WEAPON}",\n'
    f'\t\t\t\t\t\t\t\t\tEntity = "{ENTITY}",\n'
    "\t\t\t\t\t\t\t\t\tSlot = \"Magazine\",\n"
    "\t\t\t\t\t\t\t\t\tparam_bindings = false,\n"
    "\t\t\t\t\t\t\t\t}),\n"
)


def patch_block(block: str) -> tuple[str, str]:
    """Return (new_block, action)."""
    # Find Visuals table
    m = re.search(r"Visuals\s*=\s*\{", block)
    if not m:
        # insert Visuals before group/id
        insert_at = None
        for key in ("group =", "id ="):
            i = block.rfind(key)
            if i >= 0:
                insert_at = i
                break
        if insert_at is None:
            return block, "no-visuals-no-anchor"
        visuals = "Visuals = {\n" + VISUAL_TEMPLATE + "\t\t\t\t\t\t\t},\n\t\t\t\t\t\t\t"
        return block[:insert_at] + visuals + block[insert_at:], "inserted-visuals"

    start = m.end() - 1
    depth, i = 0, start
    end = None
    while i < len(block):
        ch = block[i]
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                end = i
                break
        i += 1
    if end is None:
        return block, "unclosed-visuals"

    body = block[start + 1 : end]
    # Find ApplyTo AK47 entries and set Entity
    changed = False

    def repl_entry(vm: re.Match) -> str:
        nonlocal changed
        entry = vm.group(0)
        if f'ApplyTo = "{WEAPON}"' not in entry and f"ApplyTo = '{WEAPON}'" not in entry:
            return entry
        new_entry, n = re.subn(
            r'Entity\s*=\s*"[^"]*"',
            f'Entity = "{ENTITY}"',
            entry,
            count=1,
        )
        if n:
            changed = True
            return new_entry
        # no Entity line — insert after ApplyTo
        changed = True
        return re.sub(
            rf'(ApplyTo\s*=\s*"{WEAPON}",\n)',
            rf'\1\t\t\t\t\t\t\t\t\tEntity = "{ENTITY}",\n',
            entry,
            count=1,
        )

    new_body, n_sub = re.subn(
        r"PlaceObj\('WeaponComponentVisual',\s*\{.*?\}\),",
        repl_entry,
        body,
        flags=re.S,
    )
    has_ak = f'ApplyTo = "{WEAPON}"' in new_body
    if not has_ak:
        # append AK47 visual before closing
        new_body = new_body.rstrip() + "\n" + VISUAL_TEMPLATE
        changed = True
        action = "added-ak47"
    elif changed:
        action = "rewrote-entity"
    else:
        action = "already-ok"

    if not changed and has_ak:
        # verify entity already correct
        for vm in re.finditer(
            r"PlaceObj\('WeaponComponentVisual',\s*\{(.*?)\}\),",
            new_body,
            flags=re.S,
        ):
            if f'ApplyTo = "{WEAPON}"' in vm.group(1):
                em = re.search(r'Entity\s*=\s*"([^"]+)"', vm.group(1))
                if em and em.group(1) == ENTITY:
                    return block, "already-ok"
        action = "already-ok"

    return block[: start + 1] + new_body + block[end:], action


def main() -> int:
    apply = "--apply" in sys.argv
    text = ITEMS.read_text(encoding="utf-8")
    blocks = list(placeobj_blocks(text, "ModItemWeaponComponent"))
    replacements: list[tuple[int, int, str]] = []
    for b in blocks:
        cid = prop(b.text, "id")
        if cid not in COMPS:
            continue
        new_text, action = patch_block(b.text)
        print(f"{cid}: {action}")
        if new_text != b.text:
            replacements.append((b.start, b.end, new_text))

    if not replacements:
        print("nothing to write")
        return 0
    if not apply:
        print("dry-run; pass --apply")
        return 0

    parts = []
    cursor = 0
    for start, end, repl in sorted(replacements):
        parts.append(text[cursor:start])
        parts.append(repl)
        cursor = end
    parts.append(text[cursor:])
    new = "".join(parts)
    tmp = ITEMS.with_suffix(".lua.tmp_ak47_mag")
    tmp.write_text(new, encoding="utf-8")
    tmp.replace(ITEMS)

    from _validate_items_quick import check

    problems = check(ITEMS) + check(ROOT / "metadata.lua")
    if problems:
        print("FAIL validate")
        for p in problems:
            print(" -", p)
        return 1
    print("OK wrote + validated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
