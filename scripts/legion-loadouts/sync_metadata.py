#!/usr/bin/env python3
"""Sync jazz-units metadata.affected_resources for JAZZ-UNITS-003 generated LootDefs."""
from __future__ import annotations

import argparse
import re
from pathlib import Path

UNITS = Path(__file__).resolve().parents[2].parent / "jazz-units"
ITEMS = UNITS / "items.lua"
META = UNITS / "metadata.lua"


def loot_ids_from_items() -> set[str]:
    text = ITEMS.read_text(encoding="utf-8")
    return set(re.findall(r'id = "(JAZZ_Gen[^"]+)"', text))


def resource_block(loot_id: str) -> str:
    return (
        "\t\tPlaceObj('ModResourcePreset', {\n"
        "\t\t\t'Class', \"LootDef\",\n"
        f"\t\t\t'Id', \"{loot_id}\",\n"
        "\t\t\t'ClassDisplayName', \"LootDef\",\n"
        "\t\t}),"
    )


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-bump", action="store_true", help="Do not bump version_minor/last_changes")
    args = ap.parse_args()

    needed = loot_ids_from_items()
    text = META.read_text(encoding="utf-8")
    existing = set(re.findall(r"'Id',\s*\"(JAZZ_Gen[^\"]+)\"", text))
    missing = sorted(needed - existing)
    print(f"needed={len(needed)} existing_gen={len(existing)} missing={len(missing)}")
    if missing:
        m = re.search(r"'affected_resources',\s*\{", text)
        if not m:
            raise SystemExit("affected_resources not found")
        start = m.end()
        depth = 1
        i = start
        while i < len(text) and depth:
            if text[i] == "{":
                depth += 1
            elif text[i] == "}":
                depth -= 1
            i += 1
        close = i - 1
        insert = "\n".join(resource_block(x) for x in missing) + "\n"
        text = text[:close] + insert + text[close:]

    if not args.no_bump:
        def bump_minor(match: re.Match) -> str:
            num = int(re.search(r"\d+", match.group(0)).group(0))
            return f"'version_minor', {num + 1}"

        text, n = re.subn(r"'version_minor',\s*\d+", bump_minor, text, count=1)
        if n != 1:
            raise SystemExit("version_minor bump failed")
        text, n = re.subn(
            r"'last_changes',\s*\"[^\"]*\"",
            "'last_changes', \"JAZZ-UNITS-003: Legion loadout generator recipes to LootDef\"",
            text,
            count=1,
        )
        if n != 1:
            raise SystemExit("last_changes update failed")

    META.write_text(text, encoding="utf-8")
    print(f"Updated {META} (+{len(missing)} resources, bump={not args.no_bump})")


if __name__ == "__main__":
    main()
