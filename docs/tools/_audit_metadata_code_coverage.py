# -*- coding: utf-8 -*-
"""Audit: intended Code/**/*.lua must be in metadata.code AND items.lua ModItemCode.

Editor SaveDef rebuilds metadata.code from ModItems. A Code file only in
metadata.code is dropped on the next resave. Dormant/source-only files stay
on ALLOW_UNLISTED (keep in sync with docs/technical/systems/file-coverage.md).

Also imported by _validate_items_quick.py (hard gate after items/metadata edits).
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

ALLOW_UNLISTED = {
    "Code/AIPolicyAttackAP.lua",  # dormant, empty
    "Code/AimHiringScreen_Template.lua",  # dormant template
    "Code/CodeSounds_SMG.lua",  # empty stub; other CodeSounds_* are loaded
    "Code/EmptySquadFix.lua",  # dormant
    "Code/PatrollingFix.lua",  # dormant
    "Code/Savefix.lua",  # dormant
    "Code/System_AME_Browser_Template.lua",  # source-only → ModItemXTemplate
    "Code/System_MERC_Browser_Template.lua",  # source-only → ModItemXTemplate PDAMERCBrowser
    "Code/WeaponIconBake.lua",  # dormant JAZZ-UI-001 path E bake; chips are path B
}

CRIT = [
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
    "Code/System_Medicine_MED006.lua",
]

CODE_BLOCK_RE = re.compile(r"('code',\s*\{)(.*?)(\n\t\},)", re.S)
MODITEM_CODE_RE = re.compile(r"'CodeFileName',\s*\"(Code/[^\"]+)\"")


def collect(root: Path) -> dict:
    meta_path = root / "metadata.lua"
    items_path = root / "items.lua"
    code_dir = root / "Code"
    out: dict = {
        "error": "",
        "disk": [],
        "meta": [],
        "items": set(),
        "unexpected_miss_meta": [],
        "unexpected_miss_items": [],
        "meta_not_in_items": [],
        "items_not_in_meta": [],
        "extra_in_meta": [],
        "allowed_miss": [],
        "stale_allow": [],
        "dups": [],
        "tracked_unexpected": [],
    }
    if not meta_path.exists() or not code_dir.is_dir():
        out["error"] = f"{root}: metadata.lua or Code/ missing"
        return out
    text = meta_path.read_text(encoding="utf-8-sig")
    m = CODE_BLOCK_RE.search(text)
    if not m:
        out["error"] = "metadata 'code' block not found"
        return out
    listed = re.findall(r'"([^"]+)"', m.group(2))
    listed_set = set(listed)
    code_listed = [p for p in listed if p.startswith("Code/")]
    disk = sorted(p.relative_to(root).as_posix() for p in code_dir.rglob("*.lua"))
    disk_set = set(disk)
    items_text = items_path.read_text(encoding="utf-8-sig") if items_path.exists() else ""
    moditems = set(MODITEM_CODE_RE.findall(items_text))

    missing_from_meta = sorted(disk_set - listed_set)
    missing_from_items = sorted(disk_set - moditems)
    out["disk"] = disk
    out["meta"] = code_listed
    out["items"] = moditems
    out["allowed_miss"] = sorted(p for p in missing_from_meta if p in ALLOW_UNLISTED)
    out["unexpected_miss_meta"] = sorted(p for p in missing_from_meta if p not in ALLOW_UNLISTED)
    out["unexpected_miss_items"] = sorted(p for p in missing_from_items if p not in ALLOW_UNLISTED)
    out["stale_allow"] = sorted(ALLOW_UNLISTED - disk_set)
    out["extra_in_meta"] = sorted(p for p in listed_set if p.startswith("Code/") and p not in disk_set)
    out["meta_not_in_items"] = sorted(
        p for p in code_listed if p not in moditems and p not in ALLOW_UNLISTED
    )
    out["items_not_in_meta"] = sorted(p for p in moditems if p not in listed_set)

    seen: dict[str, int] = {}
    for p in code_listed:
        seen[p] = seen.get(p, 0) + 1
    out["dups"] = sorted((p, n) for p, n in seen.items() if n > 1)

    try:
        import subprocess

        tracked = subprocess.check_output(
            ["git", "ls-files", "Code"], cwd=root, text=True, encoding="utf-8"
        ).splitlines()
        tracked = [t.replace("\\", "/") for t in tracked if t.endswith(".lua")]
        out["tracked_unexpected"] = sorted(
            t for t in tracked if t not in listed_set and t not in ALLOW_UNLISTED
        )
    except Exception:
        out["tracked_unexpected"] = []
    return out


def coverage_problems(root: Path) -> list[str]:
    """Short FAIL lines for _validate_items_quick.py."""
    data = collect(root)
    if data["error"]:
        return [data["error"]]
    problems: list[str] = []
    for p in data["unexpected_miss_items"]:
        problems.append(
            f"items.lua ModItemCode missing {p} (editor SaveDef will drop it from metadata.code)"
        )
    for p in data["unexpected_miss_meta"]:
        if p not in data["unexpected_miss_items"]:
            problems.append(f"metadata.code missing {p}")
    for p in data["meta_not_in_items"]:
        if p not in data["unexpected_miss_items"]:
            problems.append(
                f"metadata.code has {p} without ModItemCode (next editor resave drops it)"
            )
    for p in data["items_not_in_meta"]:
        if p not in data["unexpected_miss_meta"]:
            problems.append(f"ModItemCode {p} not in metadata.code (stale SaveDef?)")
    for p in data["extra_in_meta"]:
        problems.append(f"metadata.code EXTRA {p} (not on disk)")
    for p in data["stale_allow"]:
        problems.append(f"stale ALLOW_UNLISTED {p}")
    for p, n in data["dups"]:
        problems.append(f"metadata.code duplicate x{n} {p}")
    return problems


def main() -> int:
    data = collect(ROOT)
    if data["error"]:
        print(f"FAIL: {data['error']}")
        return 1
    print(f"disk Code/**/*.lua: {len(data['disk'])}")
    print(f"metadata Code/ entries: {len(data['meta'])}")
    print(f"items.lua ModItemCode Code/: {len(data['items'])}")
    print(f"unlisted (allow dormant/source-only): {len(data['allowed_miss'])}")
    for p in data["allowed_miss"]:
        print(f"  ALLOW {p}")
    print(f"UNEXPECTED missing from metadata.code: {len(data['unexpected_miss_meta'])}")
    for p in data["unexpected_miss_meta"]:
        print(f"  MISS {p}")
    print(f"UNEXPECTED missing from items.lua ModItemCode: {len(data['unexpected_miss_items'])}")
    for p in data["unexpected_miss_items"]:
        print(f"  ITEMS_MISS {p}")
    print(f"metadata.code without ModItemCode: {len(data['meta_not_in_items'])}")
    for p in data["meta_not_in_items"]:
        print(f"  META_ONLY {p}")
    if data["stale_allow"]:
        print(f"stale ALLOW_UNLISTED (not on disk): {len(data['stale_allow'])}")
        for p in data["stale_allow"]:
            print(f"  STALE_ALLOW {p}")
    print(f"IN metadata but not on disk: {len(data['extra_in_meta'])}")
    for p in data["extra_in_meta"]:
        print(f"  EXTRA {p}")
    print("--- critical ---")
    disk_set = set(data["disk"])
    listed_set = set(data["meta"])
    items_set = data["items"]
    for c in CRIT:
        meta_ok = "OK" if c in listed_set else "MISS"
        items_ok = "OK" if c in items_set else "MISS"
        disk_ok = "OK" if c in disk_set else "MISS"
        print(f"  {c}: meta={meta_ok} items={items_ok} disk={disk_ok}")
    if data["dups"]:
        print(f"DUPLICATE Code entries: {len(data['dups'])}")
        for p, n in data["dups"]:
            print(f"  DUP x{n} {p}")
    print(f"tracked unexpected unlisted: {len(data['tracked_unexpected'])}")
    for p in data["tracked_unexpected"]:
        print(f"  TRACKED_MISS {p}")

    fail = (
        data["unexpected_miss_meta"]
        or data["unexpected_miss_items"]
        or data["meta_not_in_items"]
        or data["items_not_in_meta"]
        or data["extra_in_meta"]
        or data["tracked_unexpected"]
        or data["stale_allow"]
        or data["dups"]
    )
    if fail:
        print("RESULT: FAIL")
        return 1
    print("RESULT: OK — intended Code/*.lua are in metadata.code and items.lua ModItemCode")
    return 0


if __name__ == "__main__":
    sys.exit(main())
