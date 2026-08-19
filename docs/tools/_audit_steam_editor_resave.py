"""Audit Steam editor resave damage vs HEAD."""
from __future__ import annotations

import importlib.util
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def run(*args: str) -> str:
    return subprocess.check_output(args, cwd=ROOT, text=True, encoding="utf-8", errors="replace")


def main() -> None:
    meta = (ROOT / "metadata.lua").read_text(encoding="utf-8-sig")
    title = re.search(r"'title',\s*\"([^\"]+)\"", meta)
    # ModDef versions are after dependencies block closes — take last top-level-ish:
    # Prefer fields that appear after \"dependencies\"
    dep_end = meta.find("'dependencies'")
    tail = meta[dep_end:] if dep_end >= 0 else meta
    # first version_* after dependencies section that is NOT inside nested PlaceObj — heuristic: lines at 1 tab
    maj = re.search(r"\n\t'version_major',\s*(\d+)", tail)
    mn = re.search(r"\n\t'version_minor',\s*(\d+)", tail)
    ver = re.search(r"\n\t'version',\s*(\d+)", tail)
    print("title:", title.group(1) if title else "?")
    print(
        "moddef version:",
        f"{maj.group(1) if maj else '0(default)'}.{mn.group(1) if mn else '?'}-{ver.group(1) if ver else '?'}",
    )

    names = run("git", "diff", "--name-only", "--", "CharacterEffect", "InventoryItem").splitlines()
    print(f"companion_files_changed: {len(names)}")

    lost_resolve = []
    en_to_ru = []
    lost_jazz_comment = []
    for rel in names:
        diff = run("git", "diff", "--", rel)
        if re.search(r"^-function \w+:ResolveValue", diff, re.M):
            lost_resolve.append(rel)
        if re.search(r"^-.*-- JAZZ", diff, re.M):
            lost_jazz_comment.append(rel)
        # DisplayName/Description fallback switched to Cyrillic
        if re.search(r"^\+.*DisplayName = T\(.*[А-Яа-яЁё]", diff, re.M) or re.search(
            r"^\+.*Description = T\(.*[А-Яа-яЁё]", diff, re.M
        ):
            if re.search(r"^-.*DisplayName = T\(.*[A-Za-z]", diff, re.M) or re.search(
                r"^-.*Description = T\(.*[A-Za-z]", diff, re.M
            ):
                en_to_ru.append(rel)

    print(f"lost_ResolveValue: {len(lost_resolve)}")
    for p in lost_resolve:
        print("  ", p)
    print(f"lost_JAZZ_comment_lines_in: {len(lost_jazz_comment)}")
    for p in lost_jazz_comment[:20]:
        print("  ", p)
    print(f"EN_fallback_to_RU_DisplayName_or_Description: {len(en_to_ru)}")
    for p in en_to_ru[:25]:
        print("  ", p)
    if len(en_to_ru) > 25:
        print(f"  ... +{len(en_to_ru) - 25} more")

    # FreeMove specifically
    fm = run("git", "diff", "--", "CharacterEffect/FreeMove.lua")
    print("\nFreeMove evidence:")
    print("  lost ResolveValue:", bool(re.search(r"^-function FreeMove:ResolveValue", fm, re.M)))
    print("  lost JazzFormatFreeMoveDescription:", "JazzFormatFreeMoveDescription" in fm and "-function" in fm)
    print("  Exhausted comment removed:", bool(re.search(r"^-.*JAZZ-COMBAT-007", fm, re.M)))

    items = run("git", "diff", "--stat", "--", "items.lua", "metadata.lua")
    print("\nitems/metadata:\n" + items)

    spec = importlib.util.spec_from_file_location(
        "jazz_code_cov", Path(__file__).with_name("_audit_metadata_code_coverage.py")
    )
    if spec and spec.loader:
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        probs = mod.coverage_problems(ROOT)
        print(f"\ncode_load_problems: {len(probs)}")
        for p in probs:
            print("  ", p)
        if probs:
            raise SystemExit(
                "FAIL: metadata.code / ModItemCode coverage "
                "(run _restore_dropped_metadata_code.py --from-items)"
            )


if __name__ == "__main__":
    main()
