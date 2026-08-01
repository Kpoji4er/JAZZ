# -*- coding: utf-8 -*-
"""Safe purge: only AdditionalCosts Type / Ingredients item — never ModItem Id."""
from __future__ import annotations

import argparse
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ITEMS = ROOT / "items.lua"
BAK = ROOT / "items.lua.bak_legacy_parts"

# Restore from bak first if present and current looks corrupted (duplicate Parts ids from bad purge).
def looks_corrupted(text: str) -> bool:
    # Bad purge turned OpticalLens/Microchip Ids into Parts.
    return bool(re.search(r"'Id',\s*\"Parts\",\s*\n\s*'object_class',\s*\"MiscItem\",\s*\n\s*'Icon',\s*\"UI/Icons/Items/optical_lens\"", text))


def safe_replace(text: str) -> tuple[str, dict[str, int]]:
    counts = {"FineSteelPipe": 0, "OpticalLens": 0, "Microchip": 0}

    def repl_type(match: re.Match[str]) -> str:
        old = match.group(2)
        counts[old] += 1
        new = "JAZZ_BarrelParts" if old == "FineSteelPipe" else "Parts"
        return f"{match.group(1)}{new}{match.group(3)}"

    # 'Type', "FineSteelPipe"  OR  "Type", "FineSteelPipe"
    text = re.sub(
        r"(['\"]Type['\"],\s*['\"])(FineSteelPipe|OpticalLens|Microchip)(['\"])",
        repl_type,
        text,
    )
    # Ingredients: item = "FineSteelPipe" or 'item', "FineSteelPipe"
    text = re.sub(
        r"(['\"]item['\"],\s*['\"])(FineSteelPipe|OpticalLens|Microchip)(['\"])",
        repl_type,
        text,
    )
    return text, counts


def dormant_legacy_defs(text: str) -> str:
    """Force legacy resource defs out of shops if still present as own Id."""
    for legacy_id in ("FineSteelPipe", "OpticalLens", "Microchip"):
        pattern = (
            rf"(PlaceObj\('ModItemInventoryItemCompositeDef',\s*\{{"
            rf"(?:(?!PlaceObj\().)*?'Id',\s*\"{legacy_id}\","
            rf"(?:(?!PlaceObj\().)*?)('CanAppearInShop',\s*)true"
        )
        text, n = re.subn(pattern, rf"\1\2false", text, count=1, flags=re.S)
        print(f"dormant shop {legacy_id}: {n}")
    return text


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--restore-bak", action="store_true")
    args = parser.parse_args()

    if args.restore_bak or looks_corrupted(ITEMS.read_text(encoding="utf-8")):
        if not BAK.exists():
            raise SystemExit("missing items.lua.bak_legacy_parts")
        shutil.copy2(BAK, ITEMS)
        print("restored from bak_legacy_parts")

    text = ITEMS.read_text(encoding="utf-8")
    text, counts = safe_replace(text)
    text = dormant_legacy_defs(text)
    print("type/item replacements:", counts)
    for old in ("FineSteelPipe", "OpticalLens", "Microchip"):
        # Remaining quoted ids that are NOT inside T() comments — still report Id lines
        ids = re.findall(rf"'Id',\s*\"{old}\"", text)
        print(f"still has ModItem Id {old}: {len(ids)}")
        print(f"Type leftovers {old}:", len(re.findall(rf"'Type',\s*\"{old}\"", text)))

    if args.apply:
        with ITEMS.open("w", encoding="utf-8", newline="\n") as handle:
            handle.write(text)
        print("applied")
    else:
        print("dry-run")


if __name__ == "__main__":
    main()
