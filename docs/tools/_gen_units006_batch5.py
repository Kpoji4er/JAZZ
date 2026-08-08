# -*- coding: utf-8 -*-
"""Generate UNITS-006 batch5 HARD/satellite + batch6 §D CE companions + sync.

Run from jazz root:
  python docs/tools/_gen_units006_batch5.py
Then:
  python docs/tools/_validate_items_quick.py

Cyrillic MUST use \\u escapes in this file.
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

# id, group, icon, name_id, desc_id, RU name, EN name, RU desc, EN desc, reactions_key
PERKS: list[tuple] = [
    (
        "Jazz_Perk_Rothman",
        "Perk-Personal",
        "Mod/e6L4ECj/Perks/Personal/Rothman.png",
        890000000002431,
        890000000002432,
        "\u042f \u0432\u0430\u0441 \u043d\u0430\u0443\u0447\u0443 \u0440\u0430\u0431\u043e\u0442\u0430\u0442\u044c!",
        "I'll Teach You to Work!",
        "\u041f\u043e\u043a\u0430 \u0420\u043e\u0442\u043c\u0430\u043d \u0432 \u0441\u0435\u043a\u0442\u043e\u0440\u0435 \u0441 \u0448\u0430\u0445\u0442\u043e\u0439: \u0434\u043e\u0445\u043e\u0434 \u0448\u0430\u0445\u0442\u044b +10\u2026+40% (\u0441\u0438\u043b\u044c\u043d\u0435\u0435 \u043f\u0440\u0438 \u043d\u0438\u0437\u043a\u043e\u0439 loyalty).",
        "While Rothman garrisons a mine sector: mine income +10\u2026+40% (stronger at low loyalty).",
        "empty",
    ),
    (
        "Jazz_Perk_Ira",
        "Perk-Personal",
        "Mod/e6L4ECj/Perks/Personal/Ira.png",
        890000000001900,
        890000000001901,
        "\u041d\u0430\u0440\u043e\u0434\u043d\u044b\u0439 \u043a\u043e\u043c\u0430\u043d\u0434\u0438\u0440",
        "People's Commander",
        "\u041c\u0438\u043b\u0438\u0446\u0438\u044f, \u043a\u043e\u0442\u043e\u0440\u0443\u044e \u043e\u0431\u0443\u0447\u0430\u0435\u0442 \u0410\u0439\u0440\u0430, \u043f\u043e\u043b\u0443\u0447\u0430\u0435\u0442 +20 \u043a \u0441\u043b\u0443\u0447\u0430\u0439\u043d\u043e\u0439 \u043e\u0441\u043d\u043e\u0432\u043d\u043e\u0439 \u0445\u0430\u0440\u0430\u043a\u0442\u0435\u0440\u0438\u0441\u0442\u0438\u043a\u0435 (helper; op call-site soft).",
        "Militia Ira trains gains +20 to a random primary stat (helper; op call-site soft).",
        "empty",
    ),
    (
        "Jazz_Perk_Miguel",
        "Perk-Personal",
        "Mod/e6L4ECj/Perks/Personal/Miguel.png",
        890000000003200,
        890000000003201,
        "\u041a\u043e\u043c\u0430\u043d\u0434\u0430\u043d\u0442\u0435",
        "El Comandante",
        "\u0410\u0443\u0440\u0430 30: \u0435\u0441\u043b\u0438 \u041c\u0438\u0433\u0435\u043b\u044c \u043d\u0430 \u043d\u043e\u0433\u0430\u0445 \u2014 \u0441\u043e\u044e\u0437\u043d\u0438\u043a\u0438 +30 Will / +15 CTH; \u0435\u0441\u043b\u0438 \u0441\u0431\u0438\u0442 \u2014 \u221230 Will / \u221215 CTH.",
        "Aura 30: while Miguel is up, allies get +30 Will / +15 CTH; while downed, \u221230 Will / \u221215 CTH.",
        "miguel",
    ),
    (
        "Jazz_Perk_Biff",
        "Perk-Personal",
        "Mod/e6L4ECj/Perks/Personal/Biff.png",
        890000000002800,
        890000000002801,
        "\u0412\u0435\u0440\u0431\u043e\u0432\u043a\u0430 MERC",
        "MERC Recruitment Drive",
        "\u0411\u0438\u0444\u0444 \u043c\u043e\u0436\u0435\u0442 \u043d\u0430\u0431\u0438\u0440\u0430\u0442\u044c \u043f\u043b\u0430\u0442\u043d\u044b\u0445 \u0442\u0440\u0443\u043f\u0435\u0440\u043e\u0432 MERC (\u043f\u0435\u0440\u0435\u043c\u0435\u0449\u0435\u043d\u0438\u0435/\u043e\u0445\u0440\u0430\u043d\u0430; \u0435\u0436\u0435\u0434\u043d\u0435\u0432\u043d\u0430\u044f \u043e\u043f\u043b\u0430\u0442\u0430). \u041f\u043e\u043b\u043d\u0430\u044f \u044d\u043a\u043e\u043d\u043e\u043c\u0438\u043a\u0430 \u0442\u0440\u0443\u043f\u0435\u0440\u043e\u0432 \u2014 soft-cut.",
        "Biff can raise paid MERC troopers (move/guard; daily pay). Full trooper economy soft-cut.",
        "empty",
    ),
    (
        "Jazz_Perk_Cord",
        "Perk-Personal",
        "Mod/e6L4ECj/Perks/Personal/Cord.png",
        890000000004400,
        890000000004401,
        "\u0422\u0438\u0445\u0438\u0439 \u0440\u0435\u043c\u043e\u043d\u0442",
        "Quiet Repair",
        "\u0412 \u0433\u043e\u0440\u043e\u0434\u0441\u043a\u043e\u043c \u0441\u0435\u043a\u0442\u043e\u0440\u0435: \u0440\u0435\u043c\u043e\u043d\u0442 \u0431\u044b\u0441\u0442\u0440\u0435\u0435 (\u221215% \u0432\u0440\u0435\u043c\u0435\u043d\u0438) \u0438 \u0434\u0435\u0448\u0435\u0432\u043b\u0435 (\u221210% Parts). \u0422\u0440\u0435\u0431\u043e\u0432\u0430\u043d\u0438\u0435 \u0431\u0430\u0440\u0430 \u2014 soft.",
        "In a city sector: repairs are faster (\u221215% time) and cheaper (\u221210% Parts). Bar POI gate soft.",
        "empty",
    ),
    (
        "Jazz_Perk_Conrad",
        "Perk-Personal",
        "Mod/e6L4ECj/Perks/Personal/Conrad.png",
        890000000002200,
        890000000002201,
        "\u0421\u0442\u0440\u043e\u0433\u0438\u0439 \u0438\u043d\u0441\u0442\u0440\u0443\u043a\u0442\u043e\u0440",
        "Strict Instructor",
        "\u041a\u0430\u043a \u0442\u0440\u0435\u043d\u0435\u0440: Leadership \u0441\u0447\u0438\u0442\u0430\u0435\u0442\u0441\u044f \u043d\u0435 \u043d\u0438\u0436\u0435 90 (\u0441\u043a\u043e\u0440\u043e\u0441\u0442\u044c TrainMilitia / TrainMercs).",
        "As a trainer, Leadership is treated as at least 90 (TrainMilitia / TrainMercs pace).",
        "empty",
    ),
    (
        "Jazz_Perk_Meat",
        "Perk-Personal",
        "Mod/e6L4ECj/Perks/Personal/Meat.png",
        890000000005050,
        890000000005051,
        "\u0422\u043e\u043b\u0441\u0442\u043e\u043a\u043e\u0436\u0438\u0439",
        "Thick-Skinned",
        "\u0412\u043e\u043b\u044f \u043d\u0435 \u043f\u0430\u0434\u0430\u0435\u0442 \u043e\u0442 \u043c\u043e\u0440\u0430\u043b\u0438. \u0423\u0440\u043e\u043d \u043f\u043e Will \u043f\u0435\u0440\u0435\u0445\u043e\u0434\u0438\u0442 \u0432 Grit. \u041d\u0435 \u043f\u043e\u0434\u0430\u0432\u043b\u044f\u0435\u0442\u0441\u044f.",
        "Will never drops from morale. Will-point damage converts to Grit. Unsuppressible.",
        "meat",
    ),
    (
        "Jazz_Perk_Carlos",
        "Perk-Personal",
        "Mod/e6L4ECj/Perks/Personal/Carlos.png",
        890000000005052,
        890000000005053,
        "\u0422\u0438\u0445\u0430\u044f \u0442\u0435\u043d\u044c",
        "Quiet Shadow",
        "\u041e\u0431\u043d\u0430\u0440\u0443\u0436\u0435\u043d\u0438\u0435 \u0438\u0434\u0451\u0442 \u043d\u0430 33% \u043c\u0435\u0434\u043b\u0435\u043d\u043d\u0435\u0435. \u041f\u0440\u043e\u0432\u0430\u043b \u0441\u043a\u0440\u044b\u0442\u043e\u0433\u043e \u0443\u0431\u0438\u0439\u0441\u0442\u0432\u0430 \u0441 50% \u0448\u0430\u043d\u0441\u043e\u043c \u043e\u0441\u0442\u0430\u0432\u043b\u044f\u0435\u0442 Hidden.",
        "Detection builds 33% slower. A failed stealth kill has a 50% chance to keep him Hidden.",
        "empty",
    ),
    (
        "InnerInfo_JAZZ",
        "Perk-Personal",
        "UI/Icons/Perks/InnerInfo",
        890000000000446,
        391831963748,
        "\u0421\u0435\u043a\u0440\u0435\u0442\u043d\u044b\u0435 \u0434\u0430\u043d\u043d\u044b\u0435",
        "Inside Info",
        "\u041f\u043e\u043b\u0443\u0447\u0430\u0435\u0442 \u0431\u043e\u043b\u044c\u0448\u0435 \u0440\u0430\u0437\u0432\u0435\u0434\u0434\u0430\u043d\u043d\u044b\u0445 \u043f\u0440\u0438 \u0445\u0430\u043a\u0438\u043d\u0433\u0435. \u0413\u043e\u0440\u043e\u0434\u0441\u043a\u0430\u044f \u043e\u043f\u0435\u0440\u0430\u0446\u0438\u044f \u0437\u0430\u0440\u0430\u0431\u043e\u0442\u043a\u0430 ($2000 / 2 \u0434\u043d\u044f) \u2014 soft-cut \u0434\u043e ECON-001.",
        "Gains more intel from hacks. City money-making op ($2000 / 2 days) soft-cut pending ECON-001.",
        "inner",
    ),
    (
        "DesignerExplosives",
        "Perk-Personal",
        "UI/Icons/Perks/DesignerExplosives",
        890000000009885,
        890000000009886,
        "\u041a\u043e\u043d\u0441\u0442\u0440\u0443\u043a\u0442\u043e\u0440 \u0432\u0437\u0440\u044b\u0432\u0447\u0430\u0442\u043a\u0438",
        "Explosives Designer",
        "\u041c\u043e\u0436\u0435\u0442 \u043a\u0440\u0430\u0444\u0442\u0438\u0442\u044c \u0433\u0440\u0430\u043d\u0430\u0442\u044b. \u041a\u0440\u0430\u0444\u0442 \u043f\u0430\u0442\u0440\u043e\u043d\u043e\u0432/\u0433\u0440\u0430\u043d\u0430\u0442 \u0441\u0442\u043e\u0438\u0442 \u043d\u0430 30% \u043c\u0435\u043d\u044c\u0448\u0435 Parts.",
        "Can craft grenades. Ammo/grenade craft Parts cost \u221230%.",
        "empty",
    ),
    (
        "Nazdarovya",
        "Perk-Personal",
        "UI/Icons/Perks/Nazdarovya",
        890000000009887,
        890000000009888,
        "\u041d\u0430\u0437\u0434\u0430\u0440\u043e\u0432\u044c\u0435",
        "Nazdarovya",
        "\u0421\u0442\u0430\u043a\u0438 \u22645: \u043b\u0435\u0447\u0435\u043d\u0438\u0435/\u0431\u043e\u043b\u044c/\u221215 CTH/+20 melee; \u043f\u043e\u0445\u043c\u0435\u043b\u044c\u0435 8\u201310\u0447 (3\u0447/\u0441\u0442\u0430\u043a). Hangover retune soft.",
        "Stacks \u22645: heal/pain/\u221215 CTH/+20 melee; hangover 8\u201310h (3h/stack). Hangover retune soft.",
        "empty",
    ),
    (
        "DangerClose",
        "Perk-Personal",
        "UI/Icons/Perks/DangerClose",
        890000000009889,
        890000000009890,
        "\u041e\u043f\u0430\u0441\u043d\u0430\u044f \u0431\u043b\u0438\u0437\u043e\u0441\u0442\u044c",
        "Danger Close",
        "\u041f\u043e \u0446\u0435\u043b\u044f\u043c \u22658 \u043a\u043b\u0435\u0442\u043e\u043a: +40% \u0443\u0440\u043e\u043d\u0430 \u0438 +2 Bleeding (\u0431\u0435\u0437 \u0448\u0442\u0440\u0430\u0444\u0430 \u0441\u0442\u0438\u043c\u043e\u0432 \u2014 soft).",
        "Vs targets \u22658 tiles: +40% damage and +2 Bleeding (stim pen removal soft).",
        "danger",
    ),
    (
        "ExplodingPalm",
        "Perk-Personal",
        "UI/Icons/Perks/ExplodingPalm",
        890000000009891,
        890000000009892,
        "\u0412\u0437\u0440\u044b\u0432\u043d\u0430\u044f \u043b\u0430\u0434\u043e\u043d\u044c",
        "Exploding Palm",
        "\u0423\u0434\u0430\u0440\u044b \u043a\u0443\u043b\u0430\u043a\u043e\u043c: \u0441\u0442\u0430\u0442\u0443\u0441\u044b \u043f\u043e HP. Satellite trauma heal +30%; \u0441\u043e\u043f\u0440\u043e\u0442\u0438\u0432\u043b\u0435\u043d\u0438\u0435 \u0438\u043d\u0444\u0435\u043a\u0446\u0438\u0438 (partial).",
        "Fist hits apply HP-tier statuses. Satellite trauma heal +30%; infection resist (partial).",
        "palm",
    ),
    (
        "NaturalHealing",
        "Perk-Personal",
        "UI/Icons/Perks/NaturalHealing",
        890000000009893,
        890000000009894,
        "\u0415\u0441\u0442\u0435\u0441\u0442\u0432\u0435\u043d\u043d\u043e\u0435 \u0438\u0441\u0446\u0435\u043b\u0435\u043d\u0438\u0435",
        "Natural Healing",
        "\u041a\u0440\u0430\u0444\u0442 joints \u0438 sat/combat-\u044d\u0444\u0444\u0435\u043a\u0442\u044b \u043f\u043e \u043b\u0438\u0441\u0442\u0443 (recipes soft-cut).",
        "Crafts joints plus sat/combat effects per sheet (recipes soft-cut).",
        "empty",
    ),
    (
        "Jazz_Perk_Benny",
        "Perk-Personal",
        "UI/Icons/Perks/DesignerExplosives",
        890000000009920,
        890000000009921,
        "\u0412\u0430\u043c \u043f\u043e\u0441\u044b\u043b\u043a\u0430",
        "Package for You",
        "\u0410\u043a\u0442\u0438\u0432: \u043f\u0440\u0438\u043c\u0430\u043d\u043a\u0430-\u0434\u0435\u043a\u043e\u0439 \u22648 (\u0446\u0435\u043b\u044c \u0441 \u043d\u0438\u0437\u043a\u0438\u043c Will); \u0432\u0437\u0440\u044b\u0432 \u043f\u0440\u0438 \u043f\u043e\u0434\u0445\u043e\u0434\u0435. CombatAction soft-cut \u2014 helpers \u0433\u043e\u0442\u043e\u0432\u044b.",
        "Active: decoy lure \u22648 (lowest-Will target); explodes on arrival. CombatAction soft-cut \u2014 helpers ready.",
        "empty",
    ),
    (
        "Jazz_Perk_Simon",
        "Perk-Personal",
        "UI/Icons/Perks/HawksEye",
        890000000009922,
        890000000009923,
        "\u0410\u0431\u0441\u043e\u043b\u044e\u0442\u043d\u044b\u0439 \u0441\u043d\u0430\u0439\u043f\u0435\u0440",
        "Absolute Sniper",
        "\u0410\u043a\u0442\u0438\u0432: \u0438\u0434\u0435\u0430\u043b\u044c\u043d\u044b\u0439 \u0432\u044b\u0441\u0442\u0440\u0435\u043b \u0441 \u043e\u043f\u0442\u0438\u043a\u043e\u0439 \u22654\u00d7; \u043f\u0435\u0440\u0435\u0437\u0430\u0440\u044f\u0434\u043a\u0430 \u043f\u043e \u0443\u0431\u0438\u0439\u0441\u0442\u0432\u0443. CombatAction soft-cut \u2014 helpers \u0433\u043e\u0442\u043e\u0432\u044b.",
        "Active: perfect shot with \u22654\u00d7 optic; recharges on kill. CombatAction soft-cut \u2014 helpers ready.",
        "empty",
    ),
]

STATUSES: list[tuple] = [
    (
        "Jazz_MiguelAuraUp",
        "StatusEffect",
        "UI/Hud/Status effects/accuracy",
        890000000009895,
        890000000009896,
        "\u041a\u043e\u043c\u0430\u043d\u0434\u0430\u043d\u0442\u0435 (+)",
        "Comandante (+)",
        "+15 CTH \u0438 +30 Will, \u043f\u043e\u043a\u0430 \u041c\u0438\u0433\u0435\u043b\u044c \u0432 \u0430\u0443\u0440\u0435 \u0438 \u043d\u0430 \u043d\u043e\u0433\u0430\u0445.",
        "+15 CTH and +30 Will while Miguel is up in aura.",
        "up",
    ),
    (
        "Jazz_MiguelAuraDown",
        "StatusEffect",
        "UI/Hud/Status effects/injured",
        890000000009897,
        890000000009898,
        "\u041a\u043e\u043c\u0430\u043d\u0434\u0430\u043d\u0442\u0435 (\u2212)",
        "Comandante (\u2212)",
        "\u221215 CTH \u0438 \u221230 Will, \u043f\u043e\u043a\u0430 \u041c\u0438\u0433\u0435\u043b\u044c \u0441\u0431\u0438\u0442 \u0432 \u0430\u0443\u0440\u0435.",
        "\u221215 CTH and \u221230 Will while Miguel is downed in aura.",
        "down",
    ),
]


def reaction_block(key: str) -> str:
    if key == "miguel":
        return """\tunit_reactions = {
\t\tPlaceObj('UnitReaction', {
\t\t\tEvent = "OnBeginTurn",
\t\t\tHandler = function (self, target)
\t\t\t\tif type(Jazz_MiguelRefreshAura) == "function" then
\t\t\t\t\tJazz_MiguelRefreshAura()
\t\t\t\tend
\t\t\tend,
\t\t}),
\t},
"""
    if key == "meat":
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
    if key == "inner":
        return """\tunit_reactions = {
\t\tPlaceObj('UnitReaction', {
\t\t\tEvent = "OnHackIntelDsicovered",
\t\t\tHandler = function (self, target)
\t\t\t\tlocal discoveredFor = DiscoverIntelForRandomSector(2, "no notification")
\t\t\t\tif discoveredFor then
\t\t\t\t\tCombatLog("important", T{312197955233, "Livewire used her custom PDA to discover additional Intel for <em><SectorName(sectorId)></em>", sectorId = discoveredFor})
\t\t\t\tend
\t\t\tend,
\t\t}),
\t},
"""
    if key == "danger":
        return """\tParameters = {
\t\tPlaceObj('PresetParamNumber', {
\t\t\t'Name', "minRange",
\t\t\t'Value', 8,
\t\t\t'Tag', "<minRange>",
\t\t}),
\t\tPlaceObj('PresetParamNumber', {
\t\t\t'Name', "damageBonus",
\t\t\t'Value', 40,
\t\t\t'Tag', "<damageBonus>",
\t\t}),
\t},
\tunit_reactions = {
\t\tPlaceObj('UnitReaction', {
\t\t\tEvent = "OnCalcDamageAndChance",
\t\t\tHandler = function (self, target, attacker, action, attack_target, weapon1, weapon2, data)
\t\t\t\tif target ~= attacker or not data or not IsKindOf(attack_target, "Unit") then
\t\t\t\t\treturn
\t\t\t\tend
\t\t\t\tlocal dist = DivRound(attacker:GetDist(attack_target), const.SlabSizeX)
\t\t\t\tlocal min_r = self:ResolveValue("minRange") or 8
\t\t\t\tif dist < min_r then
\t\t\t\t\treturn
\t\t\t\tend
\t\t\t\tlocal bonus = self:ResolveValue("damageBonus") or 40
\t\t\t\tdata.base_damage = MulDivRound(data.base_damage or data.damage or 0, 100 + bonus, 100)
\t\t\tend,
\t\t}),
\t},
"""
    if key == "palm":
        return """\tunit_reactions = {
\t\tPlaceObj('UnitReaction', {
\t\t\tEvent = "OnCalcHealAmount",
\t\t\tHandler = function (self, target, patient, medic, medkit, data)
\t\t\t\tif target ~= medic or not data then
\t\t\t\t\treturn
\t\t\t\tend
\t\t\t\t-- Soft: +30% heal when treating (trauma-specific ops deferred).
\t\t\t\tdata.heal_modifier = MulDivRound(data.heal_modifier or 100, 130, 100)
\t\t\tend,
\t\t}),
\t},
"""
    if key == "up":
        return """\tunit_reactions = {
\t\tPlaceObj('UnitReaction', {
\t\t\tEvent = "OnCalcChanceToHit",
\t\t\tHandler = function (self, target, attacker, action, attack_target, weapon1, weapon2, data)
\t\t\t\tif target ~= attacker then
\t\t\t\t\treturn
\t\t\t\tend
\t\t\t\tApplyCthModifier_Add(self, data, 15)
\t\t\tend,
\t\t}),
\t\tPlaceObj('UnitReaction', {
\t\t\tEvent = "StatusEffectAdded",
\t\t\tHandler = function (self, target, id)
\t\t\t\tif id ~= self.class then
\t\t\t\t\treturn
\t\t\t\tend
\t\t\t\tif type(target.WillPoints) == "number" and type(target.MaxWillPoints) == "number" then
\t\t\t\t\ttarget.WillPoints = Min(target.MaxWillPoints, target.WillPoints + 30)
\t\t\t\tend
\t\t\tend,
\t\t}),
\t},
"""
    if key == "down":
        return """\tunit_reactions = {
\t\tPlaceObj('UnitReaction', {
\t\t\tEvent = "OnCalcChanceToHit",
\t\t\tHandler = function (self, target, attacker, action, attack_target, weapon1, weapon2, data)
\t\t\t\tif target ~= attacker then
\t\t\t\t\treturn
\t\t\t\tend
\t\t\t\tApplyCthModifier_Add(self, data, -15)
\t\t\tend,
\t\t}),
\t\tPlaceObj('UnitReaction', {
\t\t\tEvent = "StatusEffectAdded",
\t\t\tHandler = function (self, target, id)
\t\t\t\tif id ~= self.class then
\t\t\t\t\treturn
\t\t\t\tend
\t\t\t\tif type(target.WillPoints) == "number" then
\t\t\t\t\ttarget.WillPoints = Max(0, target.WillPoints - 30)
\t\t\t\tend
\t\t\tend,
\t\t}),
\t},
"""
    return "\tunit_reactions = {},\n"


def write_ce(class_id: str, parents: str, icon: str, name_id: int, desc_id: int, ru_n: str, ru_d: str, key: str, extra: str = "") -> None:
    ru_n_esc = ru_n.replace("\\", "\\\\").replace('"', '\\"')
    ru_d_esc = ru_d.replace("\\", "\\\\").replace('"', '\\"')
    params = reaction_block(key)
    text = (
        f"UndefineClass('{class_id}')\n"
        f"DefineClass.{class_id} = {{\n"
        f'\t__parents = {{ "{parents}" }},\n'
        f'\t__generated_by_class = "ModItemCharacterEffectCompositeDef",\n\n\n'
        f'\tobject_class = "{parents}",\n'
        f"{params}"
        f"{extra}"
        f"\tDisplayName = T({name_id}, --[[ModItemCharacterEffectCompositeDef {class_id} DisplayName]] \"{ru_n_esc}\"),\n"
        f"\tDescription = T({desc_id}, --[[ModItemCharacterEffectCompositeDef {class_id} Description]] \"{ru_d_esc}\"),\n"
        f'\tIcon = "{icon}",\n'
    )
    if parents == "Perk":
        text += '\tTier = "Personal",\n'
    else:
        text += (
            '\ttype = "Buff",\n'
            '\tlifetime = "Until End of Turn",\n'
            "\tRemoveOnEndCombat = true,\n"
            "\tShown = true,\n"
        )
    text += "}\n"
    (CE / f"{class_id}.lua").write_text(text, encoding="utf-8", newline="\n")
    print("wrote", class_id)


def ensure_meta_code(paths: list[str]) -> None:
    meta = META.read_text(encoding="utf-8")
    changed = False
    anchor = '"Code/System_NamedPerks_006_Batch4.lua",'
    for p in paths:
        token = f'"{p}",'
        if token in meta:
            continue
        if anchor in meta:
            meta = meta.replace(anchor, anchor + "\n\t\t" + token, 1)
        else:
            meta = meta.replace(
                '"Code/System_NamedPerks_006.lua",',
                '"Code/System_NamedPerks_006.lua",\n\t\t' + token,
                1,
            )
        changed = True
        print("meta +", p)
        anchor = token
    # CE companions
    ce_anchor = '"CharacterEffect/BuildingConfidence.lua",'
    for p in paths:
        if not p.startswith("CharacterEffect/"):
            continue
        token = f'"{p}",'
        if token in meta:
            continue
        if ce_anchor in meta:
            meta = meta.replace(ce_anchor, ce_anchor + "\n\t\t" + token, 1)
            changed = True
            print("meta CE +", p)
            ce_anchor = token
    if changed:
        META.write_text(meta, encoding="utf-8", newline="\n")


def sync_items(class_ids: list[tuple[str, str]]) -> None:
    text = ITEMS.read_text(encoding="utf-8")
    cursor = "BuildingConfidence"
    for class_id, group in class_ids:
        path = CE / f"{class_id}.lua"
        cid, props = extract_define_props(path)
        assert cid == class_id
        props_items = companion_props_to_items(props)
        block = build_moditem(class_id, group, props_items)
        span = find_moditem_span(text, class_id)
        if span:
            text = text[: span[0]] + block + text[span[1] :]
            print("replaced ModItem", class_id)
        else:
            cur = find_moditem_span(text, cursor)
            if not cur:
                # fallback: Jazz_Perk_Rothman
                cur = find_moditem_span(text, "Jazz_Perk_Rothman")
            if not cur:
                raise SystemExit(f"insert cursor missing for {class_id}")
            text = text[: cur[1]] + block + text[cur[1] :]
            print("inserted ModItem", class_id)
        cursor = class_id
    ITEMS.write_text(text, encoding="utf-8", newline="\n")


def main() -> None:
    loc_rows: dict[str, tuple[str, str, str]] = {}
    class_ids: list[tuple[str, str]] = []

    for class_id, group, icon, name_id, desc_id, ru_n, en_n, ru_d, en_d, key in PERKS:
        loc_rows[str(name_id)] = (ru_n, en_n, f"jazz:CharacterEffect/{class_id}.lua")
        loc_rows[str(desc_id)] = (ru_d, en_d, f"jazz:CharacterEffect/{class_id}.lua")
        write_ce(class_id, "Perk", icon, name_id, desc_id, ru_n, ru_d, key)
        class_ids.append((class_id, group))

    for class_id, group, icon, name_id, desc_id, ru_n, en_n, ru_d, en_d, key in STATUSES:
        loc_rows[str(name_id)] = (ru_n, en_n, f"jazz:CharacterEffect/{class_id}.lua")
        loc_rows[str(desc_id)] = (ru_d, en_d, f"jazz:CharacterEffect/{class_id}.lua")
        write_ce(class_id, "StatusEffect", icon, name_id, desc_id, ru_n, ru_d, key)
        class_ids.append((class_id, group))

    sync_items(class_ids)

    meta_paths = [
        "Code/System_NamedPerks_006_Batch5.lua",
        "Code/System_NamedPerks_006_Batch6.lua",
        "CharacterEffect/DesignerExplosives.lua",
        "CharacterEffect/Nazdarovya.lua",
        "CharacterEffect/DangerClose.lua",
        "CharacterEffect/ExplodingPalm.lua",
        "CharacterEffect/NaturalHealing.lua",
        "CharacterEffect/Jazz_Perk_Benny.lua",
        "CharacterEffect/Jazz_Perk_Simon.lua",
        "CharacterEffect/Jazz_MiguelAuraUp.lua",
        "CharacterEffect/Jazz_MiguelAuraDown.lua",
    ]
    ensure_meta_code(meta_paths)

    upsert_csv(RU, loc_rows, "ru")
    upsert_csv(EN, loc_rows, "en")
    print("loc rows", len(loc_rows))
    print("OK gen batch5/6")


if __name__ == "__main__":
    main()
