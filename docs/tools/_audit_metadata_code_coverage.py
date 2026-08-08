# -*- coding: utf-8 -*-
"""Audit: every Code/**/*.lua on disk must appear in metadata.lua 'code' load list."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
META = ROOT / "metadata.lua"
CODE_DIR = ROOT / "Code"
ITEMS = ROOT / "items.lua"

# Intentionally not in metadata.code (dormant / source-only / empty stubs).
# Keep in sync with docs/technical/systems/file-coverage.md.
ALLOW_UNLISTED = {
    "Code/AIPolicyAttackAP.lua",  # dormant, empty
    "Code/AimHiringScreen_Template.lua",  # dormant template
    "Code/CodeSounds_SMG.lua",  # empty stub; other CodeSounds_* are loaded
    "Code/EmptySquadFix.lua",  # dormant
    "Code/PatrollingFix.lua",  # dormant
    "Code/Savefix.lua",  # dormant
    "Code/System_AME_Browser_Template.lua",  # source-only → ModItemXTemplate
}


def main() -> int:
    text = META.read_text(encoding="utf-8")
    m = re.search(r"('code',\s*\{)(.*?)(\n\t\},)", text, re.S)
    if not m:
        print("FAIL: metadata 'code' block not found")
        return 1
    listed = re.findall(r'"([^"]+)"', m.group(2))
    listed_set = set(listed)
    code_listed = [p for p in listed if p.startswith("Code/")]

    disk = sorted(p.relative_to(ROOT).as_posix() for p in CODE_DIR.rglob("*.lua"))
    disk_set = set(disk)

    missing_from_meta = sorted(disk_set - listed_set)
    allowed_miss = sorted(p for p in missing_from_meta if p in ALLOW_UNLISTED)
    unexpected_miss = sorted(p for p in missing_from_meta if p not in ALLOW_UNLISTED)
    stale_allow = sorted(ALLOW_UNLISTED - disk_set)
    extra_in_meta = sorted(p for p in listed_set if p.startswith("Code/") and p not in disk_set)

    items_text = ITEMS.read_text(encoding="utf-8") if ITEMS.exists() else ""
    moditems = set(re.findall(r"'CodeFileName',\s*\"(Code/[^\"]+)\"", items_text))

    print(f"disk Code/**/*.lua: {len(disk)}")
    print(f"metadata Code/ entries: {len(code_listed)}")
    print(f"items.lua ModItemCode Code/: {len(moditems)}")
    print(f"unlisted (allow dormant/source-only): {len(allowed_miss)}")
    for p in allowed_miss:
        print(f"  ALLOW {p}")
    print(f"UNEXPECTED missing from metadata.code: {len(unexpected_miss)}")
    for p in unexpected_miss:
        print(f"  MISS {p}")
    if stale_allow:
        print(f"stale ALLOW_UNLISTED (not on disk): {len(stale_allow)}")
        for p in stale_allow:
            print(f"  STALE_ALLOW {p}")
    print(f"IN metadata but not on disk: {len(extra_in_meta)}")
    for p in extra_in_meta:
        print(f"  EXTRA {p}")

    crit = [
        "Code/System_ReloadStyle.lua",
        "Code/System_InventoryStacks.lua",
        "Code/System_UnitInventory.lua",
        "Code/System_DisposableLaunchers.lua",
        "Code/System_WeaponRemovableModify.lua",
        "Code/System_WeaponResourceMaintenance.lua",
        "Code/System_WeaponComponent_Set.lua",
        "Code/VanillaDesyncFixes.lua",
        "Code/MeleeWeapon.lua",
        "Code/InventoryUI.lua",
        "Code/System_OR_Weapons.lua",
    ]
    print("--- critical ---")
    for c in crit:
        meta_ok = "OK" if c in listed_set else "MISS"
        disk_ok = "OK" if c in disk_set else "MISS"
        print(f"  {c}: meta={meta_ok} disk={disk_ok}")

    # Duplicates in load list
    seen = {}
    dups = []
    for p in code_listed:
        seen[p] = seen.get(p, 0) + 1
    for p, n in sorted(seen.items()):
        if n > 1:
            dups.append((p, n))
    if dups:
        print(f"DUPLICATE Code entries: {len(dups)}")
        for p, n in dups:
            print(f"  DUP x{n} {p}")

    # git-tracked Code files must also be listed (catches unlisted tracked orphans)
    try:
        import subprocess

        tracked = subprocess.check_output(
            ["git", "ls-files", "Code"], cwd=ROOT, text=True, encoding="utf-8"
        ).splitlines()
        tracked = [t.replace("\\", "/") for t in tracked if t.endswith(".lua")]
        tracked_unexpected = sorted(
            t for t in tracked if t not in listed_set and t not in ALLOW_UNLISTED
        )
        print(f"git-tracked Code lua: {len(tracked)}")
        print(f"tracked unexpected unlisted: {len(tracked_unexpected)}")
        for p in tracked_unexpected:
            print(f"  TRACKED_MISS {p}")
    except Exception as e:
        tracked_unexpected = []
        print(f"git ls-files skipped: {e}")

    if unexpected_miss or extra_in_meta or tracked_unexpected or stale_allow:
        print("RESULT: FAIL")
        return 1
    print("RESULT: OK — all intended Code/*.lua are in metadata.code")
    return 0


if __name__ == "__main__":
    sys.exit(main())
