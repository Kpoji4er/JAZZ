#!/usr/bin/env python3
"""Static MED-001 audit for immediate, one-shot Pain AP refunds."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8-sig")


def require(text: str, needle: str, label: str, errors: list[str]) -> None:
    if needle not in text:
        errors.append(f"{label}: missing {needle!r}")


def effect_block(items: str, effect_id: str, next_effect_id: str) -> str:
    start_marker = f"\t\t\tPlaceObj('ModItemCharacterEffectCompositeDef', {{\n\t\t\t\t'Id', \"{effect_id}\""
    end_marker = f"\t\t\tPlaceObj('ModItemCharacterEffectCompositeDef', {{\n\t\t\t\t'Id', \"{next_effect_id}\""
    start = items.find(start_marker)
    end = items.find(end_marker, start + 1)
    if start < 0 or end < 0:
        raise ValueError(f"cannot isolate items.lua effect block {effect_id}")
    return items[start:end]


def main() -> int:
    errors: list[str] = []
    medicine = read("Code/Systems_Medicine.lua")
    pain = read("CharacterEffect/Pain.lua")
    analgesia = read("CharacterEffect/Analgesia.lua")
    items = read("items.lua")

    try:
        pain_item = effect_block(items, "Pain", "Analgesia")
        analgesia_item = effect_block(items, "Analgesia", "TraumaArmsLight")
    except ValueError as exc:
        errors.append(str(exc))
        pain_item = analgesia_item = ""

    for text, label in ((pain, "Pain companion"), (pain_item, "Pain items.lua")):
        require(text, 'self:SetParameter("jazz_ap_penalty_applied", applied)', label, errors)
        require(text, 'self:SetParameter("jazz_ap_penalty_turn",', label, errors)
        require(text, 'target:HasStatusEffect("Analgesia")', label, errors)
        require(text, "return value - penalty", label, errors)

    for text, label in ((analgesia, "Analgesia companion"), (analgesia_item, "Analgesia items.lua")):
        require(text, "OnAdded", label, errors)
        require(text, 'rawget(_G, "JazzRefundPainStartTurnAP")', label, errors)
        require(text, "refund_ap(obj)", label, errors)

    require(medicine, "function JazzRefundPainStartTurnAP(unit)", "medicine helper", errors)
    require(medicine, 'pain:SetParameter("jazz_ap_penalty_applied", 0)', "medicine helper", errors)
    require(medicine, 'pain:SetParameter("jazz_ap_penalty_turn", -1)', "medicine helper", errors)
    require(medicine, "penalty_turn ~= combat.current_turn", "medicine helper", errors)
    require(medicine, "unit.ActionPoints = Max(0, unit.ActionPoints + refund)", "medicine helper", errors)

    helper_match = re.search(
        r"function JazzRefundPainStartTurnAP\(unit\)(.*?)\nend",
        medicine,
        re.S,
    )
    if not helper_match:
        errors.append("medicine helper: function body not found")
    elif ":GainAP(" in helper_match.group(1):
        errors.append("medicine helper: GainAP would incorrectly block the refund under prepared attacks/downed state")

    # Pure contract checks: a tracked penalty is consumed once; a stale turn
    # and a post-start Pain stack have no refundable marker.
    def refund_once(ap: int, marker: int, marker_turn: int, turn: int) -> tuple[int, int]:
        refund = marker if marker > 0 and marker_turn == turn else 0
        return max(0, ap + refund), 0

    ap, marker = refund_once(5, 3, 7, 7)
    if (ap, marker) != (8, 0):
        errors.append("model: exact current-turn refund failed")
    ap, marker = refund_once(ap, marker, 7, 7)
    if (ap, marker) != (8, 0):
        errors.append("model: repeated analgesia granted AP")
    ap, marker = refund_once(5, 3, 6, 7)
    if (ap, marker) != (5, 0):
        errors.append("model: stale turn marker granted AP")
    ap, marker = refund_once(5, 0, 7, 7)
    if (ap, marker) != (5, 0):
        errors.append("model: post-start Pain granted AP")

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("MED-001 Analgesia AP audit passed: companion/items parity, current-turn marker, one-shot direct refund.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
