# -*- coding: utf-8 -*-
"""Restore critical Code/vanillunique entries dropped by Mod Editor from metadata.lua."""
from __future__ import annotations

import re
import subprocess
from pathlib import Path

ROOT = Path(r"C:/Users/SsAnd/AppData/Roaming/Jagged Alliance 3/Mods/jazz")
META = ROOT / "metadata.lua"

CRITICAL_CODE = [
    "Code/VanillaDesyncFixes.lua",
    "Code/System_WeaponComponent_Set.lua",
    "Code/MeleeWeapon.lua",
    "Code/System_InventoryStacks.lua",
    "Code/System_DisposableLaunchers.lua",
    "Code/System_ReloadStyle.lua",
    "Code/System_WeaponResourceMaintenance.lua",
    "Code/System_WeaponRemovableModify.lua",
]

VANILLA_UNIQUE = [
    "Auto5_quest.lua",
    "Galil_FlagHill.lua",
    "GoldenGun.lua",
    "LionRoar.lua",
    "TexRevolver.lua",
    "Winchester_Quest.lua",
]


def extract_code_block(text: str) -> tuple[str, str, str]:
    m = re.search(r"('code',\s*\{)(.*?)(\n\t\},)", text, re.S)
    if not m:
        raise SystemExit("code block not found")
    return m.group(1), m.group(2), m.group(3)


def list_entries(body: str) -> list[str]:
    return re.findall(r'"([^"]+)"', body)


def main() -> None:
    text = META.read_text(encoding="utf-8")
    head = subprocess.check_output(
        ["git", "-C", str(ROOT), "show", "HEAD:metadata.lua"],
        text=True,
        encoding="utf-8",
    )
    _, head_body, _ = extract_code_block(head)
    head_entries = list_entries(head_body)
    head_pos = {e: i for i, e in enumerate(head_entries)}

    prefix, body, suffix = extract_code_block(text)
    entries = list_entries(body)
    present = set(entries)

    # Drop flat vanillunique aliases introduced by editor (keep HEAD paths).
    for name in VANILLA_UNIQUE:
        flat = f"InventoryItem/{name}"
        if flat in present:
            entries = [e for e in entries if e != flat]
            present.discard(flat)

    # Ensure vanillunique paths from HEAD.
    for name in VANILLA_UNIQUE:
        path = f"InventoryItem/vanillunique/{name}"
        if path not in present:
            # insert near other InventoryItem entries if possible
            insert_at = len(entries)
            for i, e in enumerate(entries):
                if e.startswith("InventoryItem/"):
                    insert_at = i
                    break
            entries.insert(insert_at, path)
            present.add(path)

    # Restore critical Code files in HEAD-relative order after a stable anchor.
    for path in CRITICAL_CODE:
        if path in present:
            continue
        # Find best previous HEAD neighbor already present in WT
        hi = head_pos.get(path, 0)
        prev = None
        for j in range(hi - 1, -1, -1):
            if head_entries[j] in present:
                prev = head_entries[j]
                break
        if prev is None:
            entries.insert(0, path)
        else:
            idx = entries.index(prev) + 1
            entries.insert(idx, path)
        present.add(path)

    # Rebuild body with original indentation style (tab + two tabs for entries)
    lines = []
    for e in entries:
        lines.append(f'\t\t"{e}",')
    new_body = "\n" + "\n".join(lines) + "\n\t"
    # Keep trailing structure: body in original was "\n\t\t\"...\",\n\t"
    # extract used (.*?) between { and \n\t}, — rebuild similarly
    new_body = "\n" + "\n".join(lines)

    new_text = text[: text.find(prefix) + len(prefix)] + new_body + "\n\t" + text[text.find(prefix) + len(prefix) + len(body) :]
    # Safer: re.sub the block
    new_text = re.sub(
        r"('code',\s*\{)(.*?)(\n\t\},)",
        lambda m: m.group(1) + new_body + m.group(3),
        text,
        count=1,
        flags=re.S,
    )

    # Sanity
    _, body2, _ = extract_code_block(new_text)
    got = set(list_entries(body2))
    missing = [p for p in CRITICAL_CODE if p not in got]
    if missing:
        raise SystemExit(f"still missing: {missing}")
    for name in VANILLA_UNIQUE:
        if f"InventoryItem/vanillunique/{name}" not in got:
            raise SystemExit(f"missing vanillunique {name}")
        if f"InventoryItem/{name}" in got:
            raise SystemExit(f"flat alias still present {name}")

    META.write_text(new_text, encoding="utf-8")
    print("OK restored critical code + vanillunique paths")
    print("code count", len(list_entries(body2)))


if __name__ == "__main__":
    main()
