# -*- coding: utf-8 -*-
"""Fix CheckDifficulty PlaceObj to StoreAsTable=true format (FunctionObject).

Condition/CheckDifficulty inherit FunctionObject.StoreAsTable=true, so
  PlaceObj('CheckDifficulty', { 'Difficulty', "Normal" })
asserts: "Object was saved with StoreAsTable == false".

Correct form:
  PlaceObj('CheckDifficulty', { Difficulty = "Normal" })

Also sync jazz-maps CampaignPreset M4 InitialSquads to include Marksmen Extra
(matches ModItemSector / UNITS-007).
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

UNITS = Path(r"C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz-units\items.lua")
MAPS = Path(r"C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz-maps\items.lua")
APPLY_SCRIPT = Path(
    r"C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz\docs\tools\_apply_ernie_overflow_inits.py"
)

# Multiline PlaceObj block as authored by Ernie overflow apply / editor paste.
CHECK_DIFF_FALSE = re.compile(
    r"PlaceObj\('CheckDifficulty',\s*\{\s*'Difficulty',\s*\"([^\"]+)\"\s*,?\s*\}\)",
    re.M,
)


def fix_units(text: str) -> tuple[str, int]:
    def repl(m: re.Match[str]) -> str:
        diff = m.group(1)
        # Preserve indentation of the opening PlaceObj line roughly:
        # replace only the inner prop form; keep surrounding whitespace structure
        # by matching the exact PlaceObj call shape used in items.lua.
        return f"PlaceObj('CheckDifficulty', {{\n\t\t\t\t\t\t\t\t\t\tDifficulty = \"{diff}\",\n\t\t\t\t\t\t\t\t\t}})"

    # Safer: only rewrite the property line pair inside known blocks.
    # Pattern used in file:
    #   PlaceObj('CheckDifficulty', {
    #     'Difficulty', "Normal",
    #   }),
    pat = re.compile(
        r"(PlaceObj\('CheckDifficulty',\s*\{\s*)'Difficulty',\s*\"([^\"]+)\"(\s*,?\s*\})",
        re.M,
    )
    n = 0

    def repl2(m: re.Match[str]) -> str:
        nonlocal n
        n += 1
        return f"{m.group(1)}Difficulty = \"{m.group(2)}\"{m.group(3)}"

    return pat.sub(repl2, text), n


def fix_maps_campaign_m4(text: str) -> tuple[str, int]:
    """Only the HotDiamonds CampaignPreset nested M4 that still lists Outlook alone."""
    pat = re.compile(
        r"(T\(890000000001615, --\[\[[\s\S]*?\]\] \"The Outlook\"\),[\s\S]*?'InitialSquads', \{\s*)"
        r"\"LegionOutlook_Easy\",\s*"
        r"(\},)",
        re.M,
    )
    if not pat.search(text):
        return text, 0
    new_text, count = pat.subn(
        r'\1"LegionOutlook_Easy",\n\t\t\t\t\t\t"LegionExtra_Ernie_Marksmen",\n\t\t\t\t\t\2',
        text,
        count=1,
    )
    return new_text, count


def fix_apply_script(text: str) -> tuple[str, int]:
    old = "lines.append(f'\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\'Difficulty\\', \"{eng}\",')"
    new = "lines.append(f'\\t\\t\\t\\t\\t\\t\\t\\t\\t\\tDifficulty = \"{eng}\",')"
    if old not in text:
        if "Difficulty = \"{eng}\"" in text:
            return text, 0
        return text, 0
    return text.replace(old, new, 1), 1


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    units_raw = UNITS.read_bytes()
    maps_raw = MAPS.read_bytes()
    apply_raw = APPLY_SCRIPT.read_bytes()
    nl_u = b"\r\n" if b"\r\n" in units_raw else b"\n"
    nl_m = b"\r\n" if b"\r\n" in maps_raw else b"\n"
    nl_a = b"\r\n" if b"\r\n" in apply_raw else b"\n"

    units = units_raw.decode("utf-8")
    maps = maps_raw.decode("utf-8")
    apply_py = apply_raw.decode("utf-8")

    units2, n_cd = fix_units(units)
    maps2, n_m4 = fix_maps_campaign_m4(maps)
    apply2, n_gen = fix_apply_script(apply_py)

    print(f"CheckDifficulty rewrites: {n_cd}")
    print(f"CampaignPreset M4 InitialSquads sync: {n_m4}")
    print(f"_apply_ernie_overflow_inits.py generator fix: {n_gen}")

    left = len(
        re.findall(
            r"PlaceObj\('CheckDifficulty',\s*\{\s*'Difficulty',",
            units2,
        )
    )
    print(f"remaining false-style CheckDifficulty: {left}")

    if not args.apply:
        print("dry-run (pass --apply to write)")
        return 0

    def write(path: Path, text: str, nl: bytes) -> None:
        data = text.replace("\r\n", "\n").replace("\n", nl.decode("ascii")).encode("utf-8")
        path.write_bytes(data)

    write(UNITS, units2, nl_u)
    if n_m4:
        write(MAPS, maps2, nl_m)
    if n_gen:
        write(APPLY_SCRIPT, apply2, nl_a)
    print("written")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
