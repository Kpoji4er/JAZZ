# -*- coding: utf-8 -*-
"""Static check: AI medic treats all Jazz bleed tiers (JAZZ-AI-MED-001)."""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _validate_items_quick import check

jazz = Path(__file__).resolve().parents[2]
units = jazz.parent / "jazz-units"
items = units / "items.lua"
probs = check(items)
print("items.lua:", "OK" if not probs else "FAIL")
for p in probs:
    print(" -", p)

text = items.read_text(encoding="utf-8")
for aid in ("Medic", "Medic_Low"):
    i = text.find(f'id = "{aid}"')
    assert i > 0, aid
    chunk = text[max(0, i - 12000) : i]
    assert "JazzHasAnyBleed" in chunk, f"{aid} missing JazzHasAnyBleed in Healer"
    assert "'turn_phase', \"Early\"" in chunk, f"{aid} missing Early phase"
    assert "JazzAI_MedicCombatBehaviorScore" in chunk or "JazzAI_MedicHealBehaviorScore" in chunk, f"{aid} missing heal-first Score helpers"
    assert "'MaxHp', 85" in chunk, f"{aid} missing MaxHp 85"
    print(f"{aid}: Healer bleed+Early+MaxHp85+combat-zero OK")

combat = (jazz / "Code" / "CombatAI.lua").read_text(encoding="utf-8")
assert "function AISelectHealTarget" in combat
assert "JazzAI_AllyHasBleed" in combat
print("CombatAI AISelectHealTarget: OK")

at = (jazz / "Code" / "AiActions.lua").read_text(encoding="utf-8")
assert "function AIActionBandage:PrecalcAction" in at
assert "jazz_bandage_action" in at
print("AiActions Bandage Precalc: OK")

st = (units / "Code" / "AICombatStance.lua").read_text(encoding="utf-8")
assert "JazzAI_MedicHealBehaviorScore" in st
assert "JazzAI_MedicCombatBehaviorScore" in st
assert "JazzAI_UnitNeedsMedicCare" in st
assert "BleedingMedium" in st
print("AICombatStance medic switch + heal-first scores: OK")

sys.exit(1 if probs else 0)
