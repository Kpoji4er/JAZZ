# -*- coding: utf-8 -*-
"""Audit Jazz_Perk_* CharacterEffect vs SignatureAbilities CombatAction companions."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ITEMS = ROOT / "items.lua"
CE_DIR = ROOT / "CharacterEffect"


def main() -> int:
    text = ITEMS.read_text(encoding="utf-8")
    ce_files = {p.stem for p in CE_DIR.glob("Jazz_Perk_*.lua")}

    # Split ModItemCombatAction blocks roughly by PlaceObj boundary.
    ca_ids: dict[str, dict] = {}
    for m in re.finditer(
        r"PlaceObj\('ModItemCombatAction',\s*\{(.*?)\n\t+\}\),",
        text,
        re.S,
    ):
        block = m.group(1)
        mid = re.search(r'\bid\s*=\s*"(Jazz_Perk_[^"]+)"', block)
        if not mid:
            continue
        pid = mid.group(1)
        # Stub: GetUIState body is ONLY `return "hidden"` (no enabled path).
        hidden = bool(
            re.search(
                r'GetUIState\s*=\s*function\s*\([^)]*\)\s*'
                r'return\s*"hidden"\s*'
                r'end,',
                block,
            )
        )
        show = re.search(r'ShowIn\s*=\s*"([^"]*)"', block)
        atype = re.search(r'ActionType\s*=\s*"([^"]*)"', block)
        ca_ids[pid] = {
            "hidden_ui": hidden,
            "ShowIn": show.group(1) if show else None,
            "ActionType": atype.group(1) if atype else None,
        }

    # Aura status CE — no SignatureAbilities CA expected.
    skip_missing = {"Jazz_Perk_OfficerAuraInfluence"}
    missing = sorted((ce_files - set(ca_ids)) - skip_missing)
    present = sorted(ce_files & set(ca_ids))
    hidden = [p for p in present if ca_ids[p]["hidden_ui"] and p != "Jazz_Perk_00"]
    bad_show = [
        p
        for p in present
        if ca_ids[p]["ShowIn"] not in (None, "SignatureAbilities")
    ]

    print(f"CE files: {len(ce_files)}")
    print(f"CombatAction companions: {len(ca_ids)}")
    print(f"Missing CombatAction: {len(missing)}")
    for p in missing:
        print(f"  - {p}")
    print(f"Present but GetUIState hidden stub: {len(hidden)}")
    for p in hidden:
        print(f"  - {p} ActionType={ca_ids[p]['ActionType']} ShowIn={ca_ids[p]['ShowIn']}")
    if bad_show:
        print(f"Bad ShowIn: {bad_show}")
    return 0 if not missing and not hidden else 1


if __name__ == "__main__":
    raise SystemExit(main())
