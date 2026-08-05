# -*- coding: utf-8 -*-
"""Apply Medic Healer-first behavior: combat behaviors score 0 when heal needed."""
from pathlib import Path

units = Path(__file__).resolve().parents[2].parent / "jazz-units" / "items.lua"
text = units.read_text(encoding="utf-8")

# Shared Score snippets (call jazz-units AICombatStance helpers)
COMBAT_SCORE = """'Score', function (self, unit, proto_context, debug_data)
\t\t\t\t\t\tif JazzAI_MedicCombatBehaviorScore then
\t\t\t\t\t\t\treturn JazzAI_MedicCombatBehaviorScore(self, unit)
\t\t\t\t\t\tend
\t\t\t\t\t\treturn self.Weight
\t\t\t\t\tend,"""

HEALER_SCORE = """'Score', function (self, unit, proto_context, debug_data)
\t\t\t\t\t\t-- JAZZ-AI-MED-001: exclusive Healer when bleed / HP < 85%
\t\t\t\t\t\tif JazzAI_MedicHealBehaviorScore then
\t\t\t\t\t\t\treturn JazzAI_MedicHealBehaviorScore(self, unit)
\t\t\t\t\t\tend
\t\t\t\t\t\tfor _, ally in ipairs(unit.team.units) do
\t\t\t\t\t\t\tif not ally:IsDead() then
\t\t\t\t\t\t\t\tlocal bleeding = (JazzHasAnyBleed and JazzHasAnyBleed(ally))
\t\t\t\t\t\t\t\t\tor ally:HasStatusEffect("Bleeding")
\t\t\t\t\t\t\t\t\tor ally:HasStatusEffect("BleedingMedium")
\t\t\t\t\t\t\t\t\tor ally:HasStatusEffect("BleedingHeavy")
\t\t\t\t\t\t\t\tif bleeding or ally.HitPoints < MulDivRound(ally.MaxHitPoints, 85, 100) then
\t\t\t\t\t\t\t\t\treturn self.Weight
\t\t\t\t\t\t\t\tend
\t\t\t\t\t\t\tend
\t\t\t\t\t\tend
\t\t\t\t\t\treturn 0
\t\t\t\t\tend,"""

OLD_HEALER_SCORE = """'Score', function (self, unit, proto_context, debug_data)
\t\t\t\t\t\t-- JAZZ-AI-MED-001: bleed-first (all Jazz tiers) or HP < 85%
\t\t\t\t\t\tfor _, ally in ipairs(unit.team.units) do
\t\t\t\t\t\t\tif not ally:IsDead() then
\t\t\t\t\t\t\t\tlocal bleeding = (JazzHasAnyBleed and JazzHasAnyBleed(ally))
\t\t\t\t\t\t\t\t\tor ally:HasStatusEffect("Bleeding")
\t\t\t\t\t\t\t\t\tor ally:HasStatusEffect("BleedingMedium")
\t\t\t\t\t\t\t\t\tor ally:HasStatusEffect("BleedingHeavy")
\t\t\t\t\t\t\t\tif bleeding or ally.HitPoints < MulDivRound(ally.MaxHitPoints, 85, 100) then
\t\t\t\t\t\t\t\t\treturn self.Weight
\t\t\t\t\t\t\t\tend
\t\t\t\t\t\t\tend
\t\t\t\t\t\tend
\t\t\t\t\t\treturn 0
\t\t\t\t\tend,"""

def patch_medic_block(block: str, is_full_medic: bool) -> str:
    # Replace Healer Score
    if OLD_HEALER_SCORE not in block:
        raise SystemExit("Healer Score block not found")
    block = block.replace(OLD_HEALER_SCORE, HEALER_SCORE, 1)

    # Healer turn_phase Normal -> Early
    block = block.replace("'turn_phase', \"Normal\",", "'turn_phase', \"Early\",", 1)

    # Healer Weight bump (Medic has Weight 200; Medic_Low may lack Weight)
    if "'BiasId', \"Healer\"," in block:
        if is_full_medic:
            block = block.replace(
                "'BiasId', \"Healer\",\n\t\t\t\t\t'Weight', 200,",
                "'BiasId', \"Healer\",\n\t\t\t\t\t'Weight', 1000,",
                1,
            )
        else:
            # Medic_Low: insert Weight after BiasId Healer
            block = block.replace(
                "'BiasId', \"Healer\",\n\t\t\t\t\t'Fallback', false,",
                "'BiasId', \"Healer\",\n\t\t\t\t\t'Weight', 1000,\n\t\t\t\t\t'Fallback', false,",
                1,
            )

    # Standard: add combat Score + reorder signatures (Bandage Priority first)
    old_std_sigs_medic = """PlaceObj('StandardAI', {
\t\t\t\t\t'BiasId', \"Standard\",
\t\t\t\t\t'EndTurnPolicies', {
\t\t\t\t\t\tPlaceObj('AIPolicyDealDamage', {
\t\t\t\t\t\t\t'Weight', 20,
\t\t\t\t\t\t}),
\t\t\t\t\t\tPlaceObj('AIPolicyTakeCover', nil),
\t\t\t\t\t\tPlaceObj('AIPolicyWeaponRange', {
\t\t\t\t\t\t\t'RangeMin', 60,
\t\t\t\t\t\t\t'RangeMax', 100,
\t\t\t\t\t\t}),
\t\t\t\t\t},
\t\t\t\t\t'SignatureActions', {
\t\t\t\t\t\tPlaceObj('AIActionMobileShot', {
\t\t\t\t\t\t\t'Priority', true,
\t\t\t\t\t\t\t'NotificationText', \"\",
\t\t\t\t\t\t}),
\t\t\t\t\t\tPlaceObj('AIActionBandage', {
\t\t\t\t\t\t\t'RequiredKeywords', {
\t\t\t\t\t\t\t\t\"Heal\",
\t\t\t\t\t\t\t},
\t\t\t\t\t\t\t'CanUseMod', 1000,
\t\t\t\t\t\t}),
\t\t\t\t\t},
\t\t\t\t\t'TakeCoverChance', 50,
\t\t\t\t}),"""

    new_std_sigs_medic = """PlaceObj('StandardAI', {
\t\t\t\t\t'BiasId', \"Standard\",
\t\t\t\t\t""" + COMBAT_SCORE + """
\t\t\t\t\t'EndTurnPolicies', {
\t\t\t\t\t\tPlaceObj('AIPolicyDealDamage', {
\t\t\t\t\t\t\t'Weight', 20,
\t\t\t\t\t\t}),
\t\t\t\t\t\tPlaceObj('AIPolicyTakeCover', nil),
\t\t\t\t\t\tPlaceObj('AIPolicyWeaponRange', {
\t\t\t\t\t\t\t'RangeMin', 60,
\t\t\t\t\t\t\t'RangeMax', 100,
\t\t\t\t\t\t}),
\t\t\t\t\t},
\t\t\t\t\t'SignatureActions', {
\t\t\t\t\t\tPlaceObj('AIActionBandage', {
\t\t\t\t\t\t\t'Priority', true,
\t\t\t\t\t\t\t'RequiredKeywords', {
\t\t\t\t\t\t\t\t\"Heal\",
\t\t\t\t\t\t\t},
\t\t\t\t\t\t\t'MaxHp', 85,
\t\t\t\t\t\t\t'BleedingWeight', 300,
\t\t\t\t\t\t\t'SelfHealMod', 100,
\t\t\t\t\t\t\t'CanUseMod', 1000,
\t\t\t\t\t\t}),
\t\t\t\t\t\tPlaceObj('AIActionMobileShot', {
\t\t\t\t\t\t\t'NotificationText', \"\",
\t\t\t\t\t\t}),
\t\t\t\t\t},
\t\t\t\t\t'TakeCoverChance', 50,
\t\t\t\t}),"""

    old_std_sigs_low = """PlaceObj('StandardAI', {
\t\t\t\t\t'BiasId', \"Standard\",
\t\t\t\t\t'EndTurnPolicies', {
\t\t\t\t\t\tPlaceObj('AIPolicyDealDamage', {
\t\t\t\t\t\t\t'Weight', 20,
\t\t\t\t\t\t}),
\t\t\t\t\t\tPlaceObj('AIPolicyTakeCover', nil),
\t\t\t\t\t\tPlaceObj('AIPolicyWeaponRange', {
\t\t\t\t\t\t\t'RangeMin', 60,
\t\t\t\t\t\t\t'RangeMax', 100,
\t\t\t\t\t\t}),
\t\t\t\t\t},
\t\t\t\t\t'SignatureActions', {
\t\t\t\t\t\tPlaceObj('AIActionMobileShot', {
\t\t\t\t\t\t\t'Priority', true,
\t\t\t\t\t\t\t'NotificationText', \"\",
\t\t\t\t\t\t}),
\t\t\t\t\t},
\t\t\t\t\t'TakeCoverChance', 50,
\t\t\t\t}),"""

    new_std_sigs_low = """PlaceObj('StandardAI', {
\t\t\t\t\t'BiasId', \"Standard\",
\t\t\t\t\t""" + COMBAT_SCORE + """
\t\t\t\t\t'EndTurnPolicies', {
\t\t\t\t\t\tPlaceObj('AIPolicyDealDamage', {
\t\t\t\t\t\t\t'Weight', 20,
\t\t\t\t\t\t}),
\t\t\t\t\t\tPlaceObj('AIPolicyTakeCover', nil),
\t\t\t\t\t\tPlaceObj('AIPolicyWeaponRange', {
\t\t\t\t\t\t\t'RangeMin', 60,
\t\t\t\t\t\t\t'RangeMax', 100,
\t\t\t\t\t\t}),
\t\t\t\t\t},
\t\t\t\t\t'SignatureActions', {
\t\t\t\t\t\tPlaceObj('AIActionBandage', {
\t\t\t\t\t\t\t'Priority', true,
\t\t\t\t\t\t\t'RequiredKeywords', {
\t\t\t\t\t\t\t\t\"Heal\",
\t\t\t\t\t\t\t},
\t\t\t\t\t\t\t'MaxHp', 85,
\t\t\t\t\t\t\t'BleedingWeight', 300,
\t\t\t\t\t\t\t'SelfHealMod', 100,
\t\t\t\t\t\t\t'CanUseMod', 1000,
\t\t\t\t\t\t}),
\t\t\t\t\t\tPlaceObj('AIActionMobileShot', {
\t\t\t\t\t\t\t'NotificationText', \"\",
\t\t\t\t\t\t}),
\t\t\t\t\t},
\t\t\t\t\t'TakeCoverChance', 50,
\t\t\t\t}),"""

    if is_full_medic:
        if old_std_sigs_medic not in block:
            raise SystemExit("Medic Standard block not found")
        block = block.replace(old_std_sigs_medic, new_std_sigs_medic, 1)
    else:
        if old_std_sigs_low not in block:
            raise SystemExit("Medic_Low Standard block not found")
        block = block.replace(old_std_sigs_low, new_std_sigs_low, 1)

    # Healer Bandage: SelfHealMod 100
    old_heal_bandage = """PlaceObj('AIActionBandage', {
\t\t\t\t\t\t\t'Priority', true,
\t\t\t\t\t\t\t'RequiredKeywords', {
\t\t\t\t\t\t\t\t\"Heal\",
\t\t\t\t\t\t\t},
\t\t\t\t\t\t\t'MaxHp', 85,
\t\t\t\t\t\t\t'BleedingWeight', 300,
\t\t\t\t\t\t\t'CanUseMod', 1000,
\t\t\t\t\t\t}),"""
    new_heal_bandage = """PlaceObj('AIActionBandage', {
\t\t\t\t\t\t\t'Priority', true,
\t\t\t\t\t\t\t'RequiredKeywords', {
\t\t\t\t\t\t\t\t\"Heal\",
\t\t\t\t\t\t\t},
\t\t\t\t\t\t\t'MaxHp', 85,
\t\t\t\t\t\t\t'BleedingWeight', 300,
\t\t\t\t\t\t\t'SelfHealMod', 100,
\t\t\t\t\t\t\t'CanUseMod', 1000,
\t\t\t\t\t\t}),"""
    if old_heal_bandage not in block:
        raise SystemExit("Healer Bandage block not found")
    block = block.replace(old_heal_bandage, new_heal_bandage, 1)

    # HealingRange policy SelfHealMod
    if is_full_medic:
        block = block.replace(
            """PlaceObj('AIPolicyHealingRange', {
\t\t\t\t\t\t\t'Weight', 300,
\t\t\t\t\t\t\t'MaxHp', 85,
\t\t\t\t\t\t\t'BleedingWeight', 300,
\t\t\t\t\t\t\t'CanUseMod', 1000,
\t\t\t\t\t\t}),""",
            """PlaceObj('AIPolicyHealingRange', {
\t\t\t\t\t\t\t'Weight', 300,
\t\t\t\t\t\t\t'MaxHp', 85,
\t\t\t\t\t\t\t'BleedingWeight', 300,
\t\t\t\t\t\t\t'SelfHealMod', 100,
\t\t\t\t\t\t\t'CanUseMod', 1000,
\t\t\t\t\t\t}),""",
            1,
        )
    else:
        block = block.replace(
            """PlaceObj('AIPolicyHealingRange', {
\t\t\t\t\t\t\t'Weight', 50,
\t\t\t\t\t\t\t'MaxHp', 85,
\t\t\t\t\t\t\t'BleedingWeight', 300,
\t\t\t\t\t\t\t'CanUseMod', 1000,
\t\t\t\t\t\t}),""",
            """PlaceObj('AIPolicyHealingRange', {
\t\t\t\t\t\t\t'Weight', 50,
\t\t\t\t\t\t\t'MaxHp', 85,
\t\t\t\t\t\t\t'BleedingWeight', 300,
\t\t\t\t\t\t\t'SelfHealMod', 100,
\t\t\t\t\t\t\t'CanUseMod', 1000,
\t\t\t\t\t\t}),""",
            1,
        )

    if is_full_medic:
        # CloseToTeammates / SeekEnemy / RetreatAI combat scores
        block = block.replace(
            """PlaceObj('PositioningAI', {
\t\t\t\t\t'BiasId', \"CloseToTeammates\",
\t\t\t\t\t'OnActivationBiases', {""",
            """PlaceObj('PositioningAI', {
\t\t\t\t\t'BiasId', \"CloseToTeammates\",
\t\t\t\t\t""" + COMBAT_SCORE + """
\t\t\t\t\t'OnActivationBiases', {""",
            1,
        )
        block = block.replace(
            """PlaceObj('CustomAI', {
\t\t\t\t\t'BiasId', \"SeekEnemy\",
\t\t\t\t\t'Label', \"FallBack - Seek Enemy\",""",
            """PlaceObj('CustomAI', {
\t\t\t\t\t'BiasId', \"SeekEnemy\",
\t\t\t\t\t""" + COMBAT_SCORE + """
\t\t\t\t\t'Label', \"FallBack - Seek Enemy\",""",
            1,
        )
        block = block.replace(
            """PlaceObj('RetreatAI', {
\t\t\t\t\t'Weight', 20,
\t\t\t\t\t'EndTurnPolicies', {""",
            """PlaceObj('RetreatAI', {
\t\t\t\t\t'Weight', 20,
\t\t\t\t\t""" + COMBAT_SCORE + """
\t\t\t\t\t'EndTurnPolicies', {""",
            1,
        )
        # Archetype-level Bandage Priority + SelfHealMod
        block = block.replace(
            """PlaceObj('AIActionBandage', {
\t\t\t\t\t'RequiredKeywords', {
\t\t\t\t\t\t\"Heal\",
\t\t\t\t\t},
\t\t\t\t\t'MaxHp', 85,
\t\t\t\t\t'BleedingWeight', 300,
\t\t\t\t\t'CanUseMod', 1000,
\t\t\t\t}),""",
            """PlaceObj('AIActionBandage', {
\t\t\t\t\t'Priority', true,
\t\t\t\t\t'RequiredKeywords', {
\t\t\t\t\t\t\"Heal\",
\t\t\t\t\t},
\t\t\t\t\t'MaxHp', 85,
\t\t\t\t\t'BleedingWeight', 300,
\t\t\t\t\t'SelfHealMod', 100,
\t\t\t\t\t'CanUseMod', 1000,
\t\t\t\t}),""",
            1,
        )
        # Drop enemy OptLoc WeaponRange while heal stance relies on HealingRange
        block = block.replace(
            """PlaceObj('AIPolicyWeaponRange', {
\t\t\t\t\t'Weight', 5,
\t\t\t\t}),""",
            """PlaceObj('AIPolicyWeaponRange', {
\t\t\t\t\t'Weight', 0,
\t\t\t\t}),""",
            1,
        )

    return block


def extract_and_replace(aid: str, is_full: bool):
    global text
    needle = "\n\t\t\tid = \"%s\",\n\t\t})," % aid
    i = text.find(needle)
    if i < 0:
        raise SystemExit(f"{aid} id line not found")
    start = text.rfind("PlaceObj('ModItemAIArchetype'", 0, i)
    if start < 0:
        raise SystemExit(f"{aid} PlaceObj start not found")
    end = i + len(needle)
    old = text[start:end]
    new = patch_medic_block(old, is_full)
    if new == old:
        raise SystemExit(f"{aid} unchanged — patch failed")
    text = text[:start] + new + text[end:]
    print(f"patched {aid}: {len(old)} -> {len(new)}")


extract_and_replace("Medic", True)
extract_and_replace("Medic_Low", False)

units.write_text(text, encoding="utf-8")
print("OK wrote", units)
