# -*- coding: utf-8 -*-
"""Generate UNITS-006 batch4 §B JA12 CE companions + sync items/metadata/loc.

Run from jazz root:
  python docs/tools/_gen_units006_batch4.py
Then validate:
  python docs/tools/_validate_items_quick.py

Cyrillic MUST use \\u escapes in this file (Write tool corrupts raw Cyrillic in .py).
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _apply_units006_batch2_items_loc import (  # type: ignore
    companion_props_to_items,
    extract_define_props,
    find_moditem_span,
    build_moditem,
    upsert_csv,
)

CE = ROOT / "CharacterEffect"
ITEMS = ROOT / "items.lua"
META = ROOT / "metadata.lua"
RU = ROOT / "Russian.csv"
EN = ROOT / "English.csv"

# Reuse existing CE loc IDs (update in place). Never touch VR 6300-6599.
PERKS: list[tuple[str, str, int, int, str, str, str, str]] = [
    # id, icon_path_suffix, name_id, desc_id, RU name, EN name, RU desc, EN desc
    (
        "Jazz_Perk_Flo",
        "Flo",
        890000000003000,
        890000000003001,
        "\u0422\u0435\u043e\u0440\u0435\u0442\u0438\u0447\u0435\u0441\u043a\u0438 \u043f\u043e\u0434\u043a\u043e\u0432\u0430\u043d\u0430",
        "Book-Smart Dealer",
        "\u041f\u043e\u043a\u0430 \u0424\u043b\u043e \u0432 \u043e\u0442\u0440\u044f\u0434\u0435: \u221212% \u043a \u0446\u0435\u043d\u0435 \u043f\u043e\u043a\u0443\u043f\u043a\u0438 (Bobby Ray) \u0438 +12% \u043a \u043f\u0440\u043e\u0434\u0430\u0436\u0435/\u043e\u0431\u043d\u0430\u043b\u0438\u0447\u0438\u0432\u0430\u043d\u0438\u044e. \u0421\u043a\u043b\u0430\u0434\u044b\u0432\u0430\u0435\u0442\u0441\u044f \u0441 Negotiator (\u043d\u0435 \u0443\u043c\u043d\u043e\u0436\u0430\u0435\u0442).",
        "While Flo is in a player squad: \u221212% buy (Bobby Ray) and +12% sell/cash-in. Additive with Negotiator (does not multiply).",
    ),
    (
        "Jazz_Perk_Static",
        "Static",
        890000000004100,
        890000000004101,
        "\u0421\u043e\u0431\u0440\u0430\u043b \u043d\u0430 \u043a\u043e\u043b\u0435\u043d\u043a\u0435",
        "Jury-Rigged",
        "\u0420\u0435\u043c\u043e\u043d\u0442 \u0438 \u043a\u0440\u0430\u0444\u0442 \u0421\u0442\u0430\u0442\u0438\u043a\u0430 \u0441\u0442\u043e\u044f\u0442 \u043d\u0430 \u22125% Parts \u0437\u0430 \u0443\u0440\u043e\u0432\u0435\u043d\u044c (\u043c\u0430\u043a\u0441. \u221225%).",
        "Static's repair/craft Parts cost \u22125% per level (cap \u221225%).",
    ),
    (
        "Jazz_Perk_Cougar",
        "Cougar",
        890000000003100,
        890000000003101,
        "\u041c\u044f\u0433\u043a\u0430\u044f \u043b\u0430\u043f\u0430",
        "Soft Paw",
        "\u0412\u044b\u0441\u0442\u0440\u0435\u043b\u044b \u041f\u0443\u043c\u044b \u043d\u0430 33% \u0442\u0438\u0448\u0435. \u0421\u043a\u0440\u044b\u0442\u043e\u0435 \u0443\u0431\u0438\u0439\u0441\u0442\u0432\u043e \u0434\u0430\u0451\u0442 Inspired 1\u00d7/\u0445\u043e\u0434 (\u043d\u0435 \u0432\u043e\u0437\u0432\u0440\u0430\u0442 \u041e\u0414).",
        "Cougar's shots are 33% quieter. Stealth Kill grants Inspired 1\u00d7/turn (not an AP refund).",
    ),
    (
        "Jazz_Perk_Grace",
        "Grace",
        890000000005039,
        890000000005040,
        "\u0422\u043e\u0447\u043d\u044b\u0439 \u0431\u0440\u043e\u0441\u043e\u043a",
        "Sure Throw",
        "\u041f\u0435\u0440\u0432\u044b\u0439 \u0431\u0440\u043e\u0441\u043e\u043a \u043d\u043e\u0436\u0430 \u0437\u0430 \u0445\u043e\u0434 \u0430\u0432\u0442\u043e\u043c\u0430\u0442\u0438\u0447\u0435\u0441\u043a\u0438 \u043f\u043e\u043f\u0430\u0434\u0430\u0435\u0442 \u043f\u043e \u0446\u0435\u043b\u0438 \u0432 \u226412 \u043a\u043b\u0435\u0442\u043e\u043a.",
        "First knife throw each turn auto-hits a target within \u226412 tiles.",
    ),
    (
        "Jazz_Perk_Kulba",
        "Kulba",
        890000000005035,
        890000000005036,
        "\u041e\u0440\u0443\u0436\u0435\u0439\u043d\u0438\u043a \u0441\u0442\u0430\u0440\u043e\u0439 \u0437\u0430\u043a\u0430\u043b\u043a\u0438",
        "Old-School Gunsmith",
        "\u0410\u043c\u0435\u0440\u0438\u043a\u0430\u043d\u0441\u043a\u0438\u0435 \u0430\u0432\u0442\u043e\u043c\u0430\u0442\u044b (M3/Thompson/M4/M16/BAR/M60/M14/M1 carbine \u0438 \u0440\u043e\u0434\u0441\u0442\u0432\u0435\u043d\u043d\u0438\u043a\u0438) \u0434\u0430\u044e\u0442 \u221250% \u043e\u0442\u0434\u0430\u0447\u0438.",
        "US autos (M3/Thompson/M4/M16/BAR/M60/M14/M1 carbine family) have \u221250% recoil.",
    ),
    (
        "Jazz_Perk_Carlos",
        "Carlos",
        890000000005052,
        890000000005053,
        "\u0422\u0438\u0445\u0430\u044f \u0442\u0435\u043d\u044c",
        "Quiet Shadow",
        "\u041e\u0431\u043d\u0430\u0440\u0443\u0436\u0435\u043d\u0438\u0435 \u0438\u0434\u0451\u0442 \u043d\u0430 33% \u043c\u0435\u0434\u043b\u0435\u043d\u043d\u0435\u0435. \u041f\u0440\u043e\u0432\u0430\u043b \u0441\u043a\u0440\u044b\u0442\u043e\u0433\u043e \u0443\u0431\u0438\u0439\u0441\u0442\u0432\u0430 \u043c\u043e\u0436\u0435\u0442 \u043e\u0441\u0442\u0430\u0432\u0438\u0442\u044c \u0432 \u0441\u043a\u0440\u044b\u0442\u043d\u043e\u0441\u0442\u0438 (partial).",
        "Detection builds 33% slower. A failed stealth kill may keep him Hidden (partial).",
    ),
    (
        "Jazz_Perk_Highball",
        "Highball",
        890000000004200,
        890000000004201,
        "\u041f\u043e\u043b\u0435\u0432\u043e\u0439 \u0445\u0438\u043c\u0438\u043a",
        "Field Chemist",
        "\u041b\u0435\u0447\u0435\u043d\u0438\u0435 \u00b150%, \u0435\u0441\u043b\u0438 \u0440\u044f\u0434\u043e\u043c (\u22645) \u0441\u043e\u044e\u0437\u043d\u0438\u043a-\u0432\u0440\u0430\u0447 \u0441 Medical\u226580 / \u0432 \u043e\u0442\u0440\u044f\u0434\u0435 \u043d\u0430 \u0441\u043f\u0443\u0442\u043d\u0438\u043a\u0435.",
        "Healing \u00b150% if an ally doctor with Medical\u226580 is within 5 tiles / in the sat squad.",
    ),
    (
        "Jazz_Perk_Meat",
        "Meat",
        890000000005050,
        890000000005051,
        "\u0422\u043e\u043b\u0441\u0442\u043e\u043a\u043e\u0436\u0438\u0439",
        "Thick-Skinned",
        "\u0412\u043e\u043b\u044f \u043d\u0435 \u043f\u0430\u0434\u0430\u0435\u0442 \u043e\u0442 \u043c\u043e\u0440\u0430\u043b\u0438. \u0423\u0440\u043e\u043d \u043f\u043e Will \u043f\u0435\u0440\u0435\u0445\u043e\u0434\u0438\u0442 \u0432 Grit. \u041d\u0435 \u043f\u043e\u0434\u0430\u0432\u043b\u044f\u0435\u0442\u0441\u044f (partial).",
        "Will never drops from morale. Will-point damage converts to Grit. Unsuppressible (partial).",
    ),
    (
        "Jazz_Perk_Ricochet",
        "Ricochet",
        890000000004600,
        890000000004601,
        "\u0420\u0438\u043a\u043e\u0448\u0435\u0442",
        "Ricochet",
        "\u0411\u043b\u0438\u0436\u043d\u0438\u0439 \u0431\u043e\u0439: \u0447\u0430\u0441\u0442\u044c \u0443\u0440\u043e\u043d\u0430 \u043f\u0435\u0440\u0435\u0445\u043e\u0434\u0438\u0442 \u043d\u0430 \u0432\u0440\u0430\u0433\u0430 \u0432 \u22641 \u043a\u043b\u0435\u0442\u043a\u0435 \u043e\u0442 \u0446\u0435\u043b\u0438.",
        "Melee hits splash partial damage to an enemy within \u22641 tile of the target.",
    ),
    (
        "Jazz_Perk_Monk",
        "Monk",
        890000000003800,
        890000000003801,
        "\u041c\u0430\u0441\u043a\u0438\u0440\u043e\u0432\u043a\u0430",
        "Camouflage",
        "\u0410\u043a\u0442\u0438\u0432: \u0431\u0435\u0441\u0448\u0443\u043c\u043d\u043e\u0435 \u0441\u043a\u0440\u044b\u0442\u043e\u0435 \u0443\u0431\u0438\u0439\u0441\u0442\u0432\u043e \u043f\u0440\u0438 CTH>70% \u0432\u0441\u0435\u0433\u0434\u0430; \u043f\u0435\u0440\u0435\u0437\u0430\u0440\u044f\u0434\u043a\u0430 \u043f\u043e\u0441\u043b\u0435 \u0443\u0431\u0438\u0439\u0441\u0442\u0432\u0430 (signature TBD).",
        "Active: silenced stealth kill always if CTH>70%; recharges on kill (signature TBD).",
    ),
    (
        "Jazz_Perk_Horg",
        "Horg",
        890000000003600,
        890000000003601,
        "\u0422\u044f\u0436\u0451\u043b\u0430\u044f \u0440\u0443\u043a\u0430",
        "Heavy Hand",
        "\u0410\u043a\u0442\u0438\u0432: \u0438\u0434\u0435\u0430\u043b\u044c\u043d\u044b\u0439 \u0432\u044b\u0441\u0442\u0440\u0435\u043b 40mm/\u041f\u0422\u0420; \u043f\u0435\u0440\u0435\u0437\u0430\u0440\u044f\u0434\u043a\u0430 \u043f\u043e\u0441\u043b\u0435 \u0443\u0431\u0438\u0439\u0441\u0442\u0432\u0430 (signature TBD).",
        "Active: perfect 40mm/AT shot; recharges on kill (signature TBD).",
    ),
    (
        "Jazz_Perk_Manuel",
        "Manuel",
        890000000003700,
        890000000003701,
        "\u041f\u043e\u0434 \u043f\u0440\u0438\u043a\u0440\u044b\u0442\u0438\u0435\u043c",
        "Under Cover",
        "\u0410\u043a\u0442\u0438\u0432: \u0433\u0430\u0440\u0430\u043d\u0442\u0438\u0440\u043e\u0432\u0430\u043d\u043d\u043e\u0435 \u0441\u043a\u0440\u044b\u0442\u043e\u0435 \u0443\u0431\u0438\u0439\u0441\u0442\u0432\u043e \u043f\u0438\u0441\u0442\u043e\u043b\u0435\u0442\u043e\u043c/SMG/\u0431\u043b\u0438\u0436\u043d\u0438\u043c \u0431\u0435\u0437 \u0440\u0430\u0441\u043a\u0440\u044b\u0442\u0438\u044f; CD \u043f\u043e \u0443\u0431\u0438\u0439\u0441\u0442\u0432\u0443 (signature TBD).",
        "Active: guaranteed pistol/SMG/melee stealth kill without reveal; CD on kill (signature TBD).",
    ),
    (
        "Jazz_Perk_Hitman",
        "Hitman",
        890000000005031,
        890000000005032,
        "\u0412\u044b\u0440\u0443\u0431\u0438\u0442\u044c",
        "Take Out",
        "\u0410\u043a\u0442\u0438\u0432: \u043c\u0435\u0442\u043a\u0430 always-see \u0431\u0435\u0437 \u0448\u0442\u0440\u0430\u0444\u0430 \u0437\u0440\u0435\u043d\u0438\u044f \u043a CTH; \u043f\u0435\u0440\u0435\u0437\u0430\u0440\u044f\u0434\u043a\u0430 \u043f\u043e\u0441\u043b\u0435 \u0443\u0431\u0438\u0439\u0441\u0442\u0432\u0430 (signature TBD).",
        "Active: mark always-see with no vision CTH penalty; recharges on kill (signature TBD).",
    ),
    (
        "Jazz_Perk_Bull",
        "Bull",
        890000000004300,
        890000000004301,
        "\u0413\u0440\u0443\u0434\u043d\u0430\u044f \u043a\u043b\u0435\u0442\u043a\u0430",
        "Rib Cage",
        "\u0423\u0434\u0430\u0440\u044b \u043a\u0443\u043b\u0430\u043a\u043e\u043c: \u0442\u0440\u0430\u0432\u043c\u0430 \u043f\u043e \u0447\u0430\u0441\u0442\u0438 \u0442\u0435\u043b\u0430. +2 \u0441\u043b\u043e\u0442\u0430 \u043f\u043e\u0434 \u043f\u0430\u0442\u0440\u043e\u043d\u044b/\u0433\u0440\u0430\u043d\u0430\u0442\u044b (inventory TBD).",
        "Fist hits apply body-part trauma. +2 ammo/grenade inventory slots (inventory TBD).",
    ),
    (
        "Jazz_Perk_Iggy",
        "Iggy",
        890000000004825,
        890000000004826,
        "\u0421\u043e\u0432\u0435\u0441\u0442\u044c \u0434\u0435\u0437\u0435\u0440\u0442\u0438\u0440\u0430",
        "Deserter's Conscience",
        "\u0420\u0430\u0437\u0431\u0440\u043e\u0441 \u043c\u0438\u043d\u043e\u043c\u0451\u0442\u0430 \u221233% (helper; bombard scatter soft-wired).",
        "Mortar scatter \u221233% (helper; bombard scatter soft-wired).",
    ),
    (
        "Jazz_Perk_Grom",
        "Grom",
        890000000002400,
        890000000002401,
        "\u0410\u0440\u0442\u043f\u043e\u0434\u0433\u043e\u0442\u043e\u0432\u043a\u0430",
        "Artillery Prep",
        "\u0413\u0440\u0430\u043d\u0430\u0442\u043e\u043c\u0451\u0442/\u043c\u0438\u043d\u043e\u043c\u0451\u0442/\u041f\u0422\u0420 \u0434\u0430\u044e\u0442 \u0432\u0434\u0432\u043e\u0435 \u043f\u043e\u0434\u0430\u0432\u043b\u0435\u043d\u0438\u0435 Will.",
        "GL/mortar/AT attacks apply double Will suppression.",
    ),
]


def reaction_block(class_id: str) -> str:
    if class_id == "Jazz_Perk_Cougar":
        return """\tunit_reactions = {
\t\tPlaceObj('UnitReaction', {
\t\t\tEvent = "OnUnitAttack",
\t\t\tHandler = function (self, target, attacker, action, attack_target, results, attack_args)
\t\t\t\tif target ~= attacker or not results then
\t\t\t\t\treturn
\t\t\t\tend
\t\t\t\tif results.stealth_kill and type(Jazz_CougarOnStealthKill) == "function" then
\t\t\t\t\tJazz_CougarOnStealthKill(attacker)
\t\t\t\tend
\t\t\tend,
\t\t}),
\t},
"""
    if class_id == "Jazz_Perk_Grace":
        return """\tunit_reactions = {
\t\tPlaceObj('UnitReaction', {
\t\t\tEvent = "OnCalcChanceToHit",
\t\t\tHandler = function (self, target, attacker, action, attack_target, weapon1, weapon2, data)
\t\t\t\tif target ~= attacker or not data or not action then
\t\t\t\t\treturn
\t\t\t\tend
\t\t\t\tif action.id ~= "KnifeThrow" and action.id ~= "ThrowKnife" then
\t\t\t\t\treturn
\t\t\t\tend
\t\t\t\tif attacker:GetEffectValue("Jazz_GraceKnifeUsed") then
\t\t\t\t\treturn
\t\t\t\tend
\t\t\t\tif not IsKindOf(attack_target, "Unit") then
\t\t\t\t\treturn
\t\t\t\tend
\t\t\t\tlocal dist = DivRound(attacker:GetDist(attack_target), const.SlabSizeX)
\t\t\t\tif dist <= 12 then
\t\t\t\t\tApplyCthModifier_Add(self, data, 100)
\t\t\t\t\tdata.min = 100
\t\t\t\tend
\t\t\tend,
\t\t}),
\t\tPlaceObj('UnitReaction', {
\t\t\tEvent = "OnUnitAttack",
\t\t\tHandler = function (self, target, attacker, action, attack_target, results, attack_args)
\t\t\t\tif target ~= attacker or not action then
\t\t\t\t\treturn
\t\t\t\tend
\t\t\t\tif action.id == "KnifeThrow" or action.id == "ThrowKnife" then
\t\t\t\t\tattacker:SetEffectValue("Jazz_GraceKnifeUsed", true)
\t\t\t\tend
\t\t\tend,
\t\t}),
\t},
"""
    if class_id == "Jazz_Perk_Ricochet":
        return """\tunit_reactions = {
\t\tPlaceObj('UnitReaction', {
\t\t\tEvent = "OnUnitAttack",
\t\t\tHandler = function (self, target, attacker, action, attack_target, results, attack_args)
\t\t\t\tif target ~= attacker or not results or results.miss then
\t\t\t\t\treturn
\t\t\t\tend
\t\t\t\tif not action or action.ActionType ~= "Melee Attack" then
\t\t\t\t\treturn
\t\t\t\tend
\t\t\t\tif not IsKindOf(attack_target, "Unit") then
\t\t\t\t\treturn
\t\t\t\tend
\t\t\t\tlocal dmg = results.total_damage or results.dealt_damage or 0
\t\t\t\tif type(dmg) ~= "number" or dmg <= 0 then
\t\t\t\t\treturn
\t\t\t\tend
\t\t\t\tlocal splash = Max(1, MulDivRound(dmg, 35, 100))
\t\t\t\tlocal slab = const.SlabSizeX
\t\t\t\tfor _, u in ipairs(g_Units or empty_table) do
\t\t\t\t\tif IsValid(u) and u ~= attack_target and not u:IsDead() and attacker:IsOnEnemySide(u) then
\t\t\t\t\t\tif DivRound(attack_target:GetDist(u), slab) <= 1 then
\t\t\t\t\t\t\tu:TakeDirectDamage(splash)
\t\t\t\t\t\t\tbreak
\t\t\t\t\t\tend
\t\t\t\t\tend
\t\t\t\tend
\t\t\tend,
\t\t}),
\t},
"""
    if class_id == "Jazz_Perk_Meat":
        return """\tunit_reactions = {
\t\tPlaceObj('UnitReaction', {
\t\t\tEvent = "OnCalcPersonalMorale",
\t\t\tHandler = function (self, target, value)
\t\t\t\tif type(value) == "number" and value < 0 then
\t\t\t\t\treturn 0
\t\t\t\tend
\t\t\tend,
\t\t}),
\t},
"""
    if class_id == "Jazz_Perk_Highball":
        return """\tunit_reactions = {
\t\tPlaceObj('UnitReaction', {
\t\t\tEvent = "OnCalcHealAmount",
\t\t\tHandler = function (self, target, patient, medic, medkit, data)
\t\t\t\tif target ~= medic or not data then
\t\t\t\t\treturn
\t\t\t\tend
\t\t\t\tlocal ok = false
\t\t\t\tlocal slab = const.SlabSizeX
\t\t\t\tfor _, u in ipairs(medic.team and medic.team.units or empty_table) do
\t\t\t\t\tif u ~= medic and IsValid(u) and not u:IsDead() and (u.Medical or 0) >= 80 then
\t\t\t\t\t\tif DivRound(medic:GetDist(u), slab) <= 5 then
\t\t\t\t\t\t\tok = true
\t\t\t\t\t\t\tbreak
\t\t\t\t\t\tend
\t\t\t\t\tend
\t\t\t\tend
\t\t\t\tif ok then
\t\t\t\t\tlocal roll = 50 + InteractionRand(101, "Jazz_Perk_Highball")
\t\t\t\t\tdata.heal_modifier = MulDivRound(data.heal_modifier or 100, roll, 100)
\t\t\t\tend
\t\t\tend,
\t\t}),
\t},
"""
    return "\tunit_reactions = {},\n"


def icon_path(suffix: str) -> str:
    return f"Mod/e6L4ECj/Perks/Personal/{suffix}.png"


def main() -> None:
    loc_rows: dict[str, tuple[str, str, str]] = {}

    for class_id, icon, name_id, desc_id, ru_n, en_n, ru_d, en_d in PERKS:
        loc_rows[str(name_id)] = (ru_n, en_n, f"jazz:CharacterEffect/{class_id}.lua")
        loc_rows[str(desc_id)] = (ru_d, en_d, f"jazz:CharacterEffect/{class_id}.lua")

        params = reaction_block(class_id)
        ru_n_esc = ru_n.replace("\\", "\\\\").replace('"', '\\"')
        ru_d_esc = ru_d.replace("\\", "\\\\").replace('"', '\\"')
        text = (
            f"UndefineClass('{class_id}')\n"
            f"DefineClass.{class_id} = {{\n"
            f'\t__parents = {{ "Perk" }},\n'
            f'\t__generated_by_class = "ModItemCharacterEffectCompositeDef",\n\n\n'
            f'\tobject_class = "Perk",\n'
            f"{params}"
            f"\tDisplayName = T({name_id}, --[[ModItemCharacterEffectCompositeDef {class_id} DisplayName]] \"{ru_n_esc}\"),\n"
            f"\tDescription = T({desc_id}, --[[ModItemCharacterEffectCompositeDef {class_id} Description]] \"{ru_d_esc}\"),\n"
            f'\tIcon = "{icon_path(icon)}",\n'
            f'\tTier = "Personal",\n'
            f"}}\n"
        )
        (CE / f"{class_id}.lua").write_text(text, encoding="utf-8", newline="\n")
        print("wrote", class_id)

    text = ITEMS.read_text(encoding="utf-8")
    for class_id, *_ in PERKS:
        path = CE / f"{class_id}.lua"
        cid, props = extract_define_props(path)
        assert cid == class_id
        props_items = companion_props_to_items(props)
        block = build_moditem(class_id, "Perk-Personal", props_items)
        span = find_moditem_span(text, class_id)
        if not span:
            raise SystemExit(f"ModItem missing for {class_id}")
        text = text[: span[0]] + block + text[span[1] :]
        print("replaced ModItem", class_id)
    ITEMS.write_text(text, encoding="utf-8", newline="\n")

    meta = META.read_text(encoding="utf-8")
    code_path = '"Code/System_NamedPerks_006_Batch4.lua",'
    if code_path not in meta:
        meta = meta.replace(
            '"Code/System_NamedPerks_006_Batch3.lua",',
            '"Code/System_NamedPerks_006_Batch3.lua",\n\t\t' + code_path,
            1,
        )
        if code_path not in meta:
            meta = meta.replace(
                '"Code/System_NamedPerks_006.lua",',
                '"Code/System_NamedPerks_006.lua",\n\t\t' + code_path,
                1,
            )
        print("meta code + Batch4")
    META.write_text(meta, encoding="utf-8", newline="\n")

    upsert_csv(RU, loc_rows, "ru")
    upsert_csv(EN, loc_rows, "en")
    print("loc rows", len(loc_rows))
    print("OK gen batch4")


if __name__ == "__main__":
    main()
