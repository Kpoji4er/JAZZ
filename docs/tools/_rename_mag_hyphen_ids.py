# -*- coding: utf-8 -*-
"""Rename JAZZ MagBelt/MagDrum public ids: hyphen → underscore (DefineClass-safe).

Touches: items.lua, metadata.lua, InventoryItem/*.lua (+ filenames),
InventoryItem weapon companions AvailableComponents, docs/tools canon lists.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ITEMS = ROOT / "items.lua"
META = ROOT / "metadata.lua"
INV = ROOT / "InventoryItem"

# Only MagBelt / MagDrum capacity ranges historically used hyphens.
ID_RE = re.compile(r"\b(JAZZ_Mag(?:Belt|Drum)_[A-Za-z0-9_-]*-[A-Za-z0-9_-]*)\b")


def collect_ids(text: str) -> list[str]:
    return sorted(set(ID_RE.findall(text)))


def map_id(old: str) -> str:
    return old.replace("-", "_")


def rewrite_text(text: str, mapping: dict[str, str]) -> str:
    # Longest first to avoid partial collisions (none expected with full-token replace).
    for old in sorted(mapping, key=len, reverse=True):
        text = text.replace(old, mapping[old])
    return text


def fix_companion(path: Path, new_id: str) -> str:
    text = path.read_text(encoding="utf-8")
    # Ensure DefineClass("Id", { ... }) form (no dotted hyphen).
    text = re.sub(
        rf"^UndefineClass\([\"'].*?[\"']\)\s*\nDefineClass(?:\.[A-Za-z0-9_-]+|\"[^\"]+\"|'[^']+')\s*=?\s*\{{",
        f'UndefineClass("{new_id}")\nDefineClass("{new_id}", {{',
        text,
        count=1,
        flags=re.M,
    )
    # Close with }) if still bare }
    stripped = text.rstrip()
    if stripped.endswith("}") and not stripped.endswith("})"):
        text = stripped[:-1] + "})\n"
    if "RemovableComponentId" not in text:
        # Insert before closing
        text = text.rstrip()
        if text.endswith("})"):
            text = text[:-2] + f'\tRemovableComponentId = "{new_id}",\n}})\n'
        elif text.endswith("}"):
            text = text[:-1] + f'\tRemovableComponentId = "{new_id}",\n}}\n'
    return text


def main() -> int:
    apply = "--apply" in sys.argv
    items_text = ITEMS.read_text(encoding="utf-8")
    meta_text = META.read_text(encoding="utf-8")
    ids = sorted(set(collect_ids(items_text) + collect_ids(meta_text)))
    # also from InventoryItem filenames
    for p in INV.glob("JAZZ_Mag*.lua"):
        if "-" in p.stem:
            ids.append(p.stem)
    ids = sorted(set(ids))
    mapping = {old: map_id(old) for old in ids if "-" in old}
    print(f"ids to rename: {len(mapping)}")
    for old, new in mapping.items():
        print(f"  {old} -> {new}")
    if not mapping:
        return 0
    if not apply:
        print("dry-run; pass --apply")
        return 0

    # items + metadata
    for path, text in ((ITEMS, items_text), (META, meta_text)):
        new = rewrite_text(text, mapping)
        tmp = path.with_suffix(path.suffix + ".tmp_hyphen")
        tmp.write_text(new, encoding="utf-8")
        tmp.replace(path)
        print("wrote", path.name)

    # InventoryItem companions with hyphen names
    for old, new in mapping.items():
        src = INV / f"{old}.lua"
        if not src.exists():
            print("missing companion", src.name)
            continue
        body = fix_companion(src, new)
        body = rewrite_text(body, mapping)
        dst = INV / f"{new}.lua"
        tmp = dst.with_suffix(".lua.tmp_hyphen")
        tmp.write_text(body, encoding="utf-8", newline="\n")
        tmp.replace(dst)
        if src.resolve() != dst.resolve():
            src.unlink()
        print("companion", old, "->", new)

    # All other InventoryItem/*.lua (weapon options)
    for path in sorted(INV.glob("*.lua")):
        if path.stem in mapping.values() or path.stem.replace("-", "_") in mapping.values():
            # already handled
            if "-" in path.stem:
                continue
        original = path.read_text(encoding="utf-8")
        if not any(old in original for old in mapping):
            continue
        path.write_text(rewrite_text(original, mapping), encoding="utf-8", newline="\n")
        print("rewrote", path.name)

    # CSV / design / tools (best-effort string replace)
    for rel in (
        "docs/technical/weapons/data/weapon-components.csv",
        "docs/technical/weapons/data/weapon-component-options.csv",
        "docs/technical/weapons/data/weapon-component-effects.csv",
        "docs/design/magazine-tiers.md",
        "docs/design/attachments-by-category.md",
        "docs/tools/_rebalance_magazine_tiers.py",
        "docs/tools/_list_mag_profiles.py",
        "docs/tools/_split_mag_families.py",
        "docs/tools/_gen_removable_attachment_items.py",
    ):
        path = ROOT / rel
        if not path.exists():
            continue
        original = path.read_text(encoding="utf-8")
        if not any(old in original for old in mapping):
            continue
        path.write_text(rewrite_text(original, mapping), encoding="utf-8", newline="\n")
        print("docs", rel)

    print("done")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
