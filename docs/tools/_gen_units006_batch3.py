# -*- coding: utf-8 -*-
"""Generate UNITS-006 batch3 CE companions + sync items/metadata/loc/showcase hooks.

Run from jazz root:
  python docs/tools/_gen_units006_batch3.py
Then validate:
  python docs/tools/_validate_items_quick.py
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

# Loc IDs: DO NOT use 6300-6599 (VoiceResponses). Free block audited at gen time.
LOC_START = 890000000009861

PERKS: list[tuple[str, str, str, str, str, str]] = [
    # id, icon_suffix, RU name, EN name, RU desc, EN desc
    (
        "MakeThemBleed",
        "MakeThemBleed",
        "Пусть кровоточат",
        "Make Them Bleed",
        "Удары в пах и по животным вызывают кровотечение. +10% урона за каждого врага с кровотечением в зоне видимости (макс. +50%).",
        "Groin and animal hits cause bleeding. +10% damage per bleeding enemy in sight (cap +50%).",
    ),
    (
        "DedicatedCamper",
        "DedicatedCamper",
        "Оседлый стрелок",
        "Dedicated Camper",
        "Пока не сдвинулся с места в этом ходу: +25% урона. Если атака нанесла ≥25 урона — +15 Силы воли (Grit).",
        "While stationary this turn: +25% damage. Dealing ≥25 damage grants +15 Grit.",
    ),
    (
        "TagTeam",
        "TagTeam",
        "Парный заход",
        "Tag Team",
        "+15% точности по целям под Pin Down союзника.",
        "+15% chance to hit vs targets under an ally's Pin Down.",
    ),
    (
        "BunsPerk",
        "BunsPerk",
        "Добить",
        "Finish Them",
        "+10% точности по целям, которых в этом ходу уже ранил союзник.",
        "+10% chance to hit vs targets already damaged by an ally this turn.",
    ),
    (
        "HawksEye",
        "HawksEye",
        "Ястребиный глаз",
        "Hawk's Eye",
        "Pin Down / Focus Fire стоит 1 ОД. Снайперские атаки дают вдвое больше подавления. Печенье прилагается.",
        "Pin Down / Focus Fire costs 1 AP. Sniper attacks apply double suppression. Biscuits included.",
    ),
    (
        "Spotter",
        "Spotter",
        "Наводчик",
        "Spotter",
        "Pin Down помечает цель (Marked). Следующее попадание по помеченной цели — гарантированный крит.",
        "Pin Down marks the target. The next hit on a marked Spotter target is a guaranteed crit.",
    ),
    (
        "HaveABlast",
        "HaveABlast",
        "Взрывной характер",
        "Have a Blast",
        "Переключатель: контратака гранатой. Получает только 50% урона от собственных взрывов.",
        "Toggle: retaliate with a grenade. Takes only 50% damage from own blasts.",
    ),
    (
        "KillingWind",
        "KillingWind",
        "Убийственный ветер",
        "Killing Wind",
        "Если атака задевает ≥2 целей — +8 Grit. Тяжёлая броня даёт половину штрафа Free Move; громоздкое оружие не штрафует FM.",
        "Hitting ≥2 targets grants +8 Grit. Heavy armor Free Move penalty halved; cumbersome weapons ignore FM penalty.",
    ),
    (
        "BuildingConfidence",
        "BuildingConfidence",
        "Уверенность растёт",
        "Building Confidence",
        "На 2-м ходу боя и каждом 3-м ходу — Inspired. Лечение ±10% за уровень (макс. ±50%) в бою и на спутнике.",
        "Inspired on combat turn 2 and every 3rd turn. Healing ±10% per level (cap ±50%) in combat and satellite.",
    ),
    (
        "SidneyPerk",
        "SidneyPerk",
        "Самодовольство",
        "Smug",
        "+2 ОД в начале хода, пока не промахнётся и не получит урон.",
        "+2 AP at turn start until a miss or taking damage.",
    ),
    (
        "BulletHell",
        "BulletHell",
        "Адский ливень",
        "Bullet Hell",
        "Конусный dump 15–30 пуль с обычным CTH и подавлением Will. Перезарядка способности — после убийства.",
        "Cone dump of 15–30 rounds with normal CTH and Will suppression. Ability recharges on kill.",
    ),
    (
        "OnMyTarget",
        "OnMyTarget",
        "По моей цели",
        "On My Target",
        "Отряд атакует отмеченную цель. Стоимость: 10 ОД.",
        "Squad attacks the marked target. Cost: 10 AP.",
    ),
]


def reaction_block(class_id: str) -> str:
    if class_id == "MakeThemBleed":
        return """\tunit_reactions = {
\t\tPlaceObj('UnitReaction', {
\t\t\tEvent = "OnCalcDamageAndEffects",
\t\t\tHandler = function (self, owner, attacker, target, action, weapon, attack_args, hit, data)
\t\t\t\tif owner ~= attacker or not data then
\t\t\t\t\treturn
\t\t\t\tend
\t\t\t\tlocal n = 0
\t\t\t\tfor _, u in ipairs(attacker:GetVisibleEnemies() or empty_table) do
\t\t\t\t\tif IsValid(u) and not u:IsDead() then
\t\t\t\t\t\tif u:HasStatusEffect("Bleeding") or u:HasStatusEffect("BleedingMedium") or u:HasStatusEffect("BleedingHeavy") then
\t\t\t\t\t\t\tn = n + 1
\t\t\t\t\t\tend
\t\t\t\t\tend
\t\t\t\tend
\t\t\t\tlocal bonus = Min(50, n * 10)
\t\t\t\tif bonus > 0 then
\t\t\t\t\tdata.damage_percent = (data.damage_percent or 100) + bonus
\t\t\t\tend
\t\t\tend,
\t\t}),
\t},
"""
    if class_id == "DedicatedCamper":
        return """\tunit_reactions = {
\t\tPlaceObj('UnitReaction', {
\t\t\tEvent = "OnBeginTurn",
\t\t\tHandler = function (self, target)
\t\t\t\ttarget:SetEffectValue("Jazz_CamperOrigin", target:GetPos())
\t\t\tend,
\t\t}),
\t\tPlaceObj('UnitReaction', {
\t\t\tEvent = "OnCalcDamageAndEffects",
\t\t\tHandler = function (self, owner, attacker, target, action, weapon, attack_args, hit, data)
\t\t\t\tif owner ~= attacker or not data then
\t\t\t\t\treturn
\t\t\t\tend
\t\t\t\tlocal origin = attacker:GetEffectValue("Jazz_CamperOrigin")
\t\t\t\tlocal moved = attack_args and attack_args.unit_moved
\t\t\t\tif not moved and origin and attacker:GetPos() == origin then
\t\t\t\t\tdata.damage_percent = (data.damage_percent or 100) + 25
\t\t\t\tend
\t\t\tend,
\t\t}),
\t\tPlaceObj('UnitReaction', {
\t\t\tEvent = "OnUnitAttack",
\t\t\tHandler = function (self, target, attacker, action, attack_target, results, attack_args)
\t\t\t\tif target ~= attacker or not results then
\t\t\t\t\treturn
\t\t\t\tend
\t\t\t\tlocal dmg = results.total_damage or results.dealt_damage or 0
\t\t\t\tif type(dmg) ~= "number" or dmg <= 0 then
\t\t\t\t\tfor _, hit in ipairs(results.hits or empty_table) do
\t\t\t\t\t\tif hit and type(hit.damage) == "number" then
\t\t\t\t\t\t\tdmg = dmg + hit.damage
\t\t\t\t\t\tend
\t\t\t\t\tend
\t\t\t\tend
\t\t\t\tif dmg >= 25 then
\t\t\t\t\tattacker:ApplyTempHitPoints(15)
\t\t\t\tend
\t\t\tend,
\t\t}),
\t},
"""
    if class_id == "TagTeam":
        return """\tunit_reactions = {
\t\tPlaceObj('UnitReaction', {
\t\t\tEvent = "OnCalcChanceToHit",
\t\t\tHandler = function (self, target, attacker, action, attack_target, weapon1, weapon2, data)
\t\t\t\tif target ~= attacker then
\t\t\t\t\treturn
\t\t\t\tend
\t\t\t\tif type(Jazz_TagTeamAllyPinDown) == "function" and Jazz_TagTeamAllyPinDown(attacker, attack_target) then
\t\t\t\t\tApplyCthModifier_Add(self, data, 15)
\t\t\t\tend
\t\t\tend,
\t\t}),
\t},
"""
    if class_id == "BunsPerk":
        return """\tunit_reactions = {
\t\tPlaceObj('UnitReaction', {
\t\t\tEvent = "OnCalcChanceToHit",
\t\t\tHandler = function (self, target, attacker, action, attack_target, weapon1, weapon2, data)
\t\t\t\tif target ~= attacker then
\t\t\t\t\treturn
\t\t\t\tend
\t\t\t\tif type(Jazz_BunsTargetDamagedByAlly) == "function" and Jazz_BunsTargetDamagedByAlly(attacker, attack_target) then
\t\t\t\t\tApplyCthModifier_Add(self, data, 10)
\t\t\t\tend
\t\t\tend,
\t\t}),
\t},
"""
    if class_id == "Spotter":
        return """\tunit_reactions = {
\t\tPlaceObj('UnitReaction', {
\t\t\tEvent = "OnUnitAttack",
\t\t\tHandler = function (self, target, attacker, action, attack_target, results, attack_args)
\t\t\t\tif target ~= attacker or not action then
\t\t\t\t\treturn
\t\t\t\tend
\t\t\t\tif action.id == "PinDown" and IsKindOf(attack_target, "Unit") and not attack_target:IsDead() then
\t\t\t\t\tattack_target:AddStatusEffect("Marked")
\t\t\t\t\tattack_target:SetEffectValue("Jazz_SpotterCritPending", true)
\t\t\t\tend
\t\t\tend,
\t\t}),
\t\tPlaceObj('UnitReaction', {
\t\t\tEvent = "OnCalcCritChance",
\t\t\tHandler = function (self, target, attacker, attack_target, action, weapon, data)
\t\t\t\tif target ~= attacker or not data or not IsKindOf(attack_target, "Unit") then
\t\t\t\t\treturn
\t\t\t\tend
\t\t\t\tif attack_target:GetEffectValue("Jazz_SpotterCritPending") then
\t\t\t\t\tdata.crit_chance = 100
\t\t\t\tend
\t\t\tend,
\t\t}),
\t\tPlaceObj('UnitReaction', {
\t\t\tEvent = "OnUnitAttack",
\t\t\tHandler = function (self, target, attacker, action, attack_target, results, attack_args)
\t\t\t\tif not IsKindOf(attack_target, "Unit") then
\t\t\t\t\treturn
\t\t\t\tend
\t\t\t\tif attack_target:GetEffectValue("Jazz_SpotterCritPending") and results and not results.miss then
\t\t\t\t\t-- Consume after a resolved hit by anyone.
\t\t\t\t\tlocal hits = results.hits or results
\t\t\t\t\tlocal hit_ok = results.crit or results.high_accuracy
\t\t\t\t\tif not hit_ok then
\t\t\t\t\t\tfor _, hit in ipairs(results.hits or empty_table) do
\t\t\t\t\t\t\tif hit and not hit.miss then
\t\t\t\t\t\t\t\thit_ok = true
\t\t\t\t\t\t\t\tbreak
\t\t\t\t\t\t\tend
\t\t\t\t\t\tend
\t\t\t\t\tend
\t\t\t\t\tif hit_ok then
\t\t\t\t\t\tattack_target:SetEffectValue("Jazz_SpotterCritPending", nil)
\t\t\t\t\tend
\t\t\t\tend
\t\t\tend,
\t\t}),
\t},
"""
    if class_id == "HaveABlast":
        return """\tunit_reactions = {
\t\tPlaceObj('UnitReaction', {
\t\t\tEvent = "OnCalcDamageAndEffects",
\t\t\tHandler = function (self, owner, attacker, target, action, weapon, attack_args, hit, data)
\t\t\t\tif owner ~= target or not data then
\t\t\t\t\treturn
\t\t\t\tend
\t\t\t\tlocal self_blast = attacker == target
\t\t\t\tif not self_blast and attack_args and attack_args.explosion_pos then
\t\t\t\t\tself_blast = attacker == owner
\t\t\t\tend
\t\t\t\tif self_blast and (IsKindOf(weapon, "Grenade") or (action and action.ActionType == "Ranged Attack" and weapon and weapon.class and string.find(weapon.class, "Grenade"))) then
\t\t\t\t\tdata.damage_percent = MulDivRound(data.damage_percent or 100, 50, 100)
\t\t\t\tend
\t\t\tend,
\t\t}),
\t},
"""
    if class_id == "KillingWind":
        return """\tunit_reactions = {
\t\tPlaceObj('UnitReaction', {
\t\t\tEvent = "OnUnitAttack",
\t\t\tHandler = function (self, target, attacker, action, attack_target, results, attack_args)
\t\t\t\tif target ~= attacker or not results then
\t\t\t\t\treturn
\t\t\t\tend
\t\t\t\tlocal hit_units = {}
\t\t\t\tfor _, hit in ipairs(results.hits or empty_table) do
\t\t\t\t\tlocal obj = hit and (hit.obj or hit.unit)
\t\t\t\t\tif IsKindOf(obj, "Unit") and not obj:IsDead() then
\t\t\t\t\t\thit_units[obj] = true
\t\t\t\t\tend
\t\t\t\tend
\t\t\t\tlocal n = 0
\t\t\t\tfor _ in pairs(hit_units) do
\t\t\t\t\tn = n + 1
\t\t\t\tend
\t\t\t\tif n >= 2 then
\t\t\t\t\tattacker:ApplyTempHitPoints(8)
\t\t\t\tend
\t\t\tend,
\t\t}),
\t},
"""
    if class_id == "BuildingConfidence":
        return """\tunit_reactions = {
\t\tPlaceObj('UnitReaction', {
\t\t\tEvent = "OnBeginTurn",
\t\t\tHandler = function (self, target)
\t\t\t\tif not g_Combat then
\t\t\t\t\treturn
\t\t\t\tend
\t\t\t\tlocal turn = g_Combat.current_turn or 1
\t\t\t\tif turn == 2 or (turn > 0 and turn % 3 == 0) then
\t\t\t\t\ttarget:AddStatusEffect("Inspired")
\t\t\t\tend
\t\t\tend,
\t\t}),
\t},
"""
    if class_id == "SidneyPerk":
        return """\tunit_reactions = {
\t\tPlaceObj('UnitReaction', {
\t\t\tEvent = "OnCombatStarted",
\t\t\tHandler = function (self, target, load_game)
\t\t\t\ttarget:SetEffectValue("Jazz_SidneySmug", true)
\t\t\tend,
\t\t}),
\t\tPlaceObj('UnitReaction', {
\t\t\tEvent = "OnBeginTurn",
\t\t\tHandler = function (self, target)
\t\t\t\tif target:GetEffectValue("Jazz_SidneySmug") then
\t\t\t\t\ttarget:GainAP(2 * const.Scale.AP)
\t\t\t\tend
\t\t\tend,
\t\t}),
\t\tPlaceObj('UnitReaction', {
\t\t\tEvent = "OnUnitAttack",
\t\t\tHandler = function (self, target, attacker, action, attack_target, results, attack_args)
\t\t\t\tif target == attacker and results and results.miss then
\t\t\t\t\tattacker:SetEffectValue("Jazz_SidneySmug", nil)
\t\t\t\tend
\t\t\tend,
\t\t}),
\t\tPlaceObj('UnitReaction', {
\t\t\tEvent = "OnDamageTaken",
\t\t\tHandler = function (self, target, attacker, dmg)
\t\t\t\tif dmg and dmg > 0 then
\t\t\t\t\ttarget:SetEffectValue("Jazz_SidneySmug", nil)
\t\t\t\tend
\t\t\tend,
\t\t}),
\t},
"""
    if class_id == "HawksEye":
        return """\tParameters = {
\t\tPlaceObj('PresetParamNumber', {
\t\t\t'Name', "pindownCostOverwrite",
\t\t\t'Value', 1,
\t\t\t'Tag', "<pindownCostOverwrite>",
\t\t}),
\t},
"""
    return "\tunit_reactions = {},\n"


def write_companion(class_id: str, icon: str, name_id: int, desc_id: int, ru_name: str) -> None:
    params = reaction_block(class_id)
    # HawksEye has Parameters instead of/in addition to empty reactions
    body = f"""UndefineClass('{class_id}')
DefineClass.{class_id} = {{
\t__parents = {{ "Perk" }},
\t__generated_by_class = "ModItemCharacterEffectCompositeDef",


\tobject_class = "Perk",
{params}\tDisplayName = T({name_id}, --[[ModItemCharacterEffectCompositeDef {class_id} DisplayName]] "{ru_name}"),
\tDescription = T({desc_id}, --[[ModItemCharacterEffectCompositeDef {class_id} Description]] ""),
\tIcon = "UI/Icons/Perks/{icon}",
\tTier = "Personal",
}}
"""
    # Fill description text into T() second arg for readability
    # Rebuild with proper description string (escaped)
    return  # filled below in main


def main() -> None:
    loc_rows: dict[str, tuple[str, str, str]] = {}
    loc_id = LOC_START
    id_map: dict[str, tuple[int, int]] = {}

    for class_id, icon, ru_n, en_n, ru_d, en_d in PERKS:
        name_id = loc_id
        desc_id = loc_id + 1
        loc_id += 2
        id_map[class_id] = (name_id, desc_id)
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
            f'\tIcon = "UI/Icons/Perks/{icon}",\n'
            f'\tTier = "Personal",\n'
            f"}}\n"
        )
        (CE / f"{class_id}.lua").write_text(text, encoding="utf-8", newline="\n")
        print("wrote", class_id)

    # Sync items.lua
    text = ITEMS.read_text(encoding="utf-8")
    # Insert after IcePerk if present else GrizzlyPerk
    anchor = "IcePerk" if find_moditem_span(text, "IcePerk") else "GrizzlyPerk"
    for class_id, *_ in PERKS:
        path = CE / f"{class_id}.lua"
        cid, props = extract_define_props(path)
        assert cid == class_id
        props_items = companion_props_to_items(props)
        block = build_moditem(class_id, "Perk-Personal", props_items)
        span = find_moditem_span(text, class_id)
        if span:
            text = text[: span[0]] + block + text[span[1] :]
            print("replaced ModItem", class_id)
        else:
            a_span = find_moditem_span(text, anchor)
            if not a_span:
                raise SystemExit(f"anchor {anchor} missing")
            text = text[: a_span[1]] + block + text[a_span[1] :]
            print("inserted ModItem", class_id)
            anchor = class_id
    ITEMS.write_text(text, encoding="utf-8", newline="\n")

    # metadata.code CharacterEffect paths
    meta = META.read_text(encoding="utf-8")
    for class_id, *_ in PERKS:
        path = f'"CharacterEffect/{class_id}.lua",'
        if path not in meta:
            needle = '"CharacterEffect/IcePerk.lua",'
            if needle in meta:
                meta = meta.replace(needle, needle + "\n\t\t" + path, 1)
            else:
                needle = '"CharacterEffect/GrizzlyPerk.lua",'
                meta = meta.replace(needle, needle + "\n\t\t" + path, 1)
            print("meta code +", class_id)
    # Code batch3 file
    code_path = '"Code/System_NamedPerks_006_Batch3.lua",'
    if code_path not in meta:
        meta = meta.replace(
            '"Code/System_NamedPerks_006.lua",',
            '"Code/System_NamedPerks_006.lua",\n\t\t' + code_path,
            1,
        )
        print("meta code + Batch3")
    META.write_text(meta, encoding="utf-8", newline="\n")

    upsert_csv(RU, loc_rows, "ru")
    upsert_csv(EN, loc_rows, "en")
    print("loc rows", len(loc_rows))
    print("OK gen batch3")


if __name__ == "__main__":
    main()
