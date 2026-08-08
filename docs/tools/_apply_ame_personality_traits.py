#!/usr/bin/env python3
"""Apply sparse AME personality traits (~12/60) to UnitData companions + items.lua.

Canon map: JAZZ-UNITS-005 (personality sparsity). Common combat traits are preserved.
Dry-run by default; pass --apply to write.

Usage (from jazz/):
  python -B docs/tools/_apply_ame_personality_traits.py
  python -B docs/tools/_apply_ame_personality_traits.py --apply
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
UNITS = ROOT.parent / "jazz-units"

# Exactly 12 slots (~20%). One Personality-tier perk each; no Mimicry/Veteran.
PERSONALITY: dict[int, str] = {
    1: "Negotiator",
    3: "Negotiator",
    6: "Loner",
    11: "Psycho",
    14: "Scoundrel",
    21: "Pessimist",
    32: "Stealthy",
    38: "Optimist",
    39: "Psycho",
    47: "Scoundrel",
    50: "Optimist",
    56: "Stealthy",
}

PERSONALITY_SET = frozenset(PERSONALITY.values())
COMMON_TRAITS = frozenset(
    {
        "AutoWeapons",
        "CQCTraining",
        "HeavyWeaponsTraining",
        "NightOps",
        "Teacher",
        "Throwing",
    }
)


def slot_id(n: int) -> str:
    return f"JAZZ_AME_{n:02d}"


def parse_perks_companion(text: str) -> list[str]:
    m = re.search(r"StartingPerks\s*=\s*\{([^}]*)\}", text, re.S)
    if not m:
        return []
    return re.findall(r'"([^"]+)"', m.group(1))


def merge_perks(existing: list[str], personality: str) -> list[str]:
    common = [p for p in existing if p in COMMON_TRAITS]
    # Drop any previous personality; keep commons in stable order.
    out = list(common)
    if personality not in out:
        out.append(personality)
    return out


def render_companion_perks(perks: list[str]) -> str:
    if not perks:
        return "\tStartingPerks = {},"
    lines = ["\tStartingPerks = {"]
    for p in perks:
        lines.append(f'\t"{p}",')
    lines.append("\t},")
    return "\n".join(lines)


def patch_companion(path: Path, personality: str, apply: bool) -> tuple[list[str], list[str]]:
    text = path.read_text(encoding="utf-8")
    old = parse_perks_companion(text)
    new = merge_perks(old, personality)
    if old == new:
        return old, new
    repl = render_companion_perks(new)
    new_text, n = re.subn(r"StartingPerks\s*=\s*\{[^}]*\}", repl, text, count=1, flags=re.S)
    if n != 1:
        raise RuntimeError(f"{path.name}: StartingPerks replace failed (n={n})")
    if apply:
        path.write_text(new_text, encoding="utf-8", newline="\n")
    return old, new


def items_unit_span(text: str, uid: str) -> tuple[int, int] | None:
    """Return [start, end) of ModItemUnitDataCompositeDef for uid inside items.lua."""
    id_pat = re.compile(rf"'Id',\s*\"{re.escape(uid)}\"")
    m = id_pat.search(text)
    if not m:
        return None
    # Walk back to PlaceObj('ModItemUnitDataCompositeDef'
    start = text.rfind("PlaceObj('ModItemUnitDataCompositeDef'", 0, m.start())
    if start < 0:
        return None
    # Find matching close of this PlaceObj — naive brace depth from first '{' after PlaceObj
    brace_at = text.find("{", start)
    if brace_at < 0:
        return None
    depth = 0
    i = brace_at
    while i < len(text):
        ch = text[i]
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                # include trailing ),
                end = i + 1
                if end < len(text) and text[end] == ")":
                    end += 1
                if end < len(text) and text[end] == ",":
                    end += 1
                return start, end
        i += 1
    return None


def parse_perks_items_block(block: str) -> list[str]:
    m = re.search(r"'StartingPerks',\s*\{([^}]*)\}", block, re.S)
    if not m:
        return []
    return re.findall(r"'([^']+)'", m.group(1))


def render_items_perks(perks: list[str]) -> str:
    if not perks:
        return ""
    inner = "\n".join(f"\t\t\t\t'{p}'," for p in perks)
    return f"\t\t\t\t'StartingPerks', {{\n{inner}\n\t\t\t\t}},\n"


def patch_items(text: str, uid: str, personality: str) -> tuple[str, list[str], list[str]]:
    span = items_unit_span(text, uid)
    if not span:
        raise RuntimeError(f"items.lua: missing ModItem for {uid}")
    a, b = span
    block = text[a:b]
    old = parse_perks_items_block(block)
    new = merge_perks(old, personality)
    if old == new and ("'StartingPerks'" in block or not new):
        return text, old, new

    perk_blob = render_items_perks(new)
    if "'StartingPerks'" in block:
        new_block, n = re.subn(
            r"'StartingPerks',\s*\{[^}]*\},?\n?",
            perk_blob,
            block,
            count=1,
            flags=re.S,
        )
        if n != 1:
            raise RuntimeError(f"items.lua {uid}: StartingPerks replace failed")
    else:
        # Insert before Specialization (always present on AME)
        if "'Specialization'" not in block:
            raise RuntimeError(f"items.lua {uid}: no Specialization to anchor insert")
        new_block = block.replace(
            "\t\t\t\t'Specialization'",
            perk_blob + "\t\t\t\t'Specialization'",
            1,
        )
    return text[:a] + new_block + text[b:], old, new


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    if len(PERSONALITY) != 12:
        print(f"FAIL: expected 12 personality slots, got {len(PERSONALITY)}", file=sys.stderr)
        return 1

    items_path = UNITS / "items.lua"
    items_text = items_path.read_text(encoding="utf-8")
    changed = 0

    print(f"{'APPLY' if args.apply else 'DRY-RUN'}: {len(PERSONALITY)} AME personality slots")
    for slot, perk in sorted(PERSONALITY.items()):
        uid = slot_id(slot)
        comp = UNITS / "UnitData" / f"{uid}.lua"
        if not comp.is_file():
            print(f"FAIL: missing {comp}", file=sys.stderr)
            return 1
        old_c, new_c = patch_companion(comp, perk, args.apply)
        items_text, old_i, new_i = patch_items(items_text, uid, perk)
        mark = "CHANGE" if old_c != new_c or old_i != new_i else "ok"
        if mark == "CHANGE":
            changed += 1
        print(f"  {uid}: {mark} companion {old_c} -> {new_c}; items {old_i} -> {new_i}")

    if args.apply:
        items_path.write_text(items_text, encoding="utf-8", newline="\n")
        print(f"Wrote {items_path} ({changed} slots changed)")
    else:
        print(f"Would change {changed} slots (pass --apply)")

    # Static assert: no personality outside map after apply
    if args.apply:
        for n in range(1, 61):
            uid = slot_id(n)
            perks = parse_perks_companion((UNITS / "UnitData" / f"{uid}.lua").read_text(encoding="utf-8"))
            unexpected = [p for p in perks if p in PERSONALITY_SET and PERSONALITY.get(n) != p]
            if unexpected:
                print(f"FAIL: {uid} unexpected personality {unexpected}", file=sys.stderr)
                return 1
            if n in PERSONALITY and PERSONALITY[n] not in perks:
                print(f"FAIL: {uid} missing {PERSONALITY[n]}", file=sys.stderr)
                return 1
        print("OK: companions match personality map")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
