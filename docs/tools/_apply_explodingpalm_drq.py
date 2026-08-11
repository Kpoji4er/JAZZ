# -*- coding: utf-8 -*-
"""UNITS-006 DrQ ExplodingPalm: fist HP-tier statuses + sat debt +30% + infection block.

Rewrites CE companion + items ModItem; patches NamedPerks helpers / WoundInfected;
hides vanilla ExplodingPalm active CA; inserts Passive hotbar CA; loc + metadata.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ITEMS = ROOT / "items.lua"
META = ROOT / "metadata.lua"
CE = ROOT / "CharacterEffect" / "ExplodingPalm.lua"
NAMED = ROOT / "Code" / "System_NamedPerks.lua"
MED = ROOT / "Code" / "Systems_Medicine.lua"
EN = ROOT / "English.csv"
RU = ROOT / "Russian.csv"

DN_ID = "890000000009924"
DESC_ID = "890000000009892"

DESC_RU = (
    "Пассивно. Удары <em>голыми руками</em> по живому противнику в зависимости от "
    "его текущего HP: ≤20% — нокдаун и без сознания; ≤35% — контузия; ≤50% — травма рёбер; "
    "≤65% — травма рук; ≤80% — травма ног; иначе — травма паха (рёбра/«яйца»). "
    "В отряде на сателлите: восстановление травм, ожогов и HP-долга на "
    "<sat_debt_speed_percent>% быстрее; защищает от инфекции ран."
)
DESC_EN = (
    "Passive. <em>Unarmed</em> hits vs living foes scale with current HP: ≤20% knockdown + "
    "unconscious; ≤35% concussion; ≤50% rib trauma; ≤65% arm trauma; ≤80% leg trauma; "
    "else groin trauma (ribs/«eggs»). In the squad on satellite: trauma, burns, and HP debt "
    "recover <sat_debt_speed_percent>% faster; blocks wound infection."
)

CE_TEXT = f'''UndefineClass('ExplodingPalm')
DefineClass.ExplodingPalm = {{
	__parents = {{ "Perk" }},
	__generated_by_class = "ModItemCharacterEffectCompositeDef",


	object_class = "Perk",
	Parameters = {{
		PlaceObj('PresetParamPercent', {{
			'Name', "sat_debt_speed_percent",
			'Value', 30,
			'Tag', "<sat_debt_speed_percent>",
		}}),
	}},
	unit_reactions = {{
		PlaceObj('UnitReaction', {{
			Event = "OnUnitAttack",
			Handler = function (self, target, attacker, action, attack_target, results, attack_args)
				if target ~= attacker or not results or results.miss then
					return
				end
				if type(Jazz_ExplodingPalmOnUnarmedHit) == "function" then
					Jazz_ExplodingPalmOnUnarmedHit(attacker, action, attack_target, results, attack_args)
				end
			end,
		}}),
	}},
	DisplayName = T({DN_ID}, --[[ModItemCharacterEffectCompositeDef ExplodingPalm DisplayName]] "Взрывная ладонь"),
	Description = T({DESC_ID}, --[[ModItemCharacterEffectCompositeDef ExplodingPalm Description]] "{DESC_RU}"),
	Icon = "UI/Icons/Perks/ExplodingPalm",
	Tier = "Personal",
}}
'''

PASSIVE_CA = f"""\t\t\t\tPlaceObj('ModItemCombatAction', {{
\t\t\t\t\tActionType = "Passive",
\t\t\t\t\tActivePauseBehavior = "instant",
\t\t\t\t\tComment = "DrQ ExplodingPalm passive signature (id must match CE)",
\t\t\t\t\tConfigurableKeybind = false,
\t\t\t\t\tDisplayName = T(115026001164, --[[ModItemCombatAction ExplodingPalm DisplayName]] "<placeholder>"),
\t\t\t\t\tGetActionDescription = function (self, units)
\t\t\t\t\t\treturn GetSignatureActionDescription(self)
\t\t\t\t\tend,
\t\t\t\t\tGetActionDisplayName = function (self, units)
\t\t\t\t\t\treturn GetSignatureActionDisplayName(self)
\t\t\t\t\tend,
\t\t\t\t\tGetUIState = function (self, units, args)
\t\t\t\t\t\tlocal unit = units[1]
\t\t\t\t\t\tlocal cost = self:GetAPCost(unit, args)
\t\t\t\t\t\tif cost < 0 then return "hidden" end
\t\t\t\t\t\tif not unit:UIHasAP(cost) then return "disabled" end
\t\t\t\t\t\treturn "enabled"
\t\t\t\t\tend,
\t\t\t\t\tIcon = "UI/Icons/Hud/perk_exploding_palm",
\t\t\t\t\tIdDefault = "ExplodingPalmdefault",
\t\t\t\t\tIsAimableAttack = false,
\t\t\t\t\tKeybindingFromAction = "actionRedirectSignatureAbility",
\t\t\t\t\tRequireState = "any",
\t\t\t\t\tRun = function (self, unit, ap, ...)
\t\t\t\t\t\treturn false
\t\t\t\t\tend,
\t\t\t\t\tShowIn = "SignatureAbilities",
\t\t\t\t\tSortKey = 100,
\t\t\t\t\tgroup = "SignatureAbilities",
\t\t\t\t\tid = "ExplodingPalm",
\t\t\t\t}}),
"""

ITEMS_CE = f"""\t\t\t\tPlaceObj('ModItemCharacterEffectCompositeDef', {{
\t\t\t\t\t'Group', "Perk-Personal",
\t\t\t\t\t'Id', "ExplodingPalm",
\t\t\t\t\t'object_class', "Perk",
\t\t\t\t\t'Parameters', {{
\t\t\t\t\t\tPlaceObj('PresetParamPercent', {{
\t\t\t\t\t\t\t'Name', "sat_debt_speed_percent",
\t\t\t\t\t\t\t'Value', 30,
\t\t\t\t\t\t\t'Tag', "<sat_debt_speed_percent>",
\t\t\t\t\t\t}}),
\t\t\t\t\t}},
\t\t\t\t\t'unit_reactions', {{
\t\t\t\t\t\tPlaceObj('UnitReaction', {{
\t\t\t\t\t\t\tEvent = "OnUnitAttack",
\t\t\t\t\t\t\tHandler = function (self, target, attacker, action, attack_target, results, attack_args)
\t\t\t\t\t\t\t\tif target ~= attacker or not results or results.miss then
\t\t\t\t\t\t\t\t\treturn
\t\t\t\t\t\t\t\tend
\t\t\t\t\t\t\t\tif type(Jazz_ExplodingPalmOnUnarmedHit) == "function" then
\t\t\t\t\t\t\t\t\tJazz_ExplodingPalmOnUnarmedHit(attacker, action, attack_target, results, attack_args)
\t\t\t\t\t\t\t\tend
\t\t\t\t\t\t\tend,
\t\t\t\t\t\t}}),
\t\t\t\t\t}},
\t\t\t\t\t'DisplayName', T({DN_ID}, --[[ModItemCharacterEffectCompositeDef ExplodingPalm DisplayName]] "Взрывная ладонь"),
\t\t\t\t\t'Description', T({DESC_ID}, --[[ModItemCharacterEffectCompositeDef ExplodingPalm Description]] "{DESC_RU}"),
\t\t\t\t\t'Icon', "UI/Icons/Perks/ExplodingPalm",
\t\t\t\t\t'Tier', "Personal",
\t\t\t\t}}),
"""

HELPERS = r'''
--- DrQ ExplodingPalm: same sat squad (or self) has the perk.
function Jazz_SquadHasExplodingPalm(unit)
	if not unit then
		return false
	end
	if HasPerk(unit, "ExplodingPalm") then
		return true
	end
	local squad_id = unit.Squad
	local squad = squad_id and gv_Squads and gv_Squads[squad_id]
	if not squad then
		return false
	end
	for _, uid in ipairs(squad.units or empty_table) do
		local u = gv_UnitData and gv_UnitData[uid]
		if not u and g_Units then
			u = g_Units[uid]
		end
		if u and HasPerk(u, "ExplodingPalm") and not (u.IsDead and u:IsDead()) then
			return true
		end
	end
	return false
end

function Jazz_ExplodingPalmDebtHoursMul(unit)
	if not Jazz_SquadHasExplodingPalm(unit) then
		return 100
	end
	local pct = Jazz_NamedPerkParam(unit, "ExplodingPalm", "sat_debt_speed_percent", 30)
	return Max(1, 100 - (tonumber(pct) or 30))
end

function Jazz_ExplodingPalmDebtSpeedMul(unit)
	if not Jazz_SquadHasExplodingPalm(unit) then
		return 100
	end
	local pct = Jazz_NamedPerkParam(unit, "ExplodingPalm", "sat_debt_speed_percent", 30)
	return 100 + (tonumber(pct) or 30)
end

--- Combined sat debt mul: Thor NaturalHealing + DrQ ExplodingPalm (stack).
function Jazz_SatDebtHoursMul(unit)
	local mul = 100
	if type(Jazz_NaturalHealingDebtHoursMul) == "function" then
		mul = MulDivRound(mul, Jazz_NaturalHealingDebtHoursMul(unit), 100)
	end
	if type(Jazz_ExplodingPalmDebtHoursMul) == "function" then
		mul = MulDivRound(mul, Jazz_ExplodingPalmDebtHoursMul(unit), 100)
	end
	return Max(1, mul)
end

function Jazz_SatDebtSpeedMul(unit)
	local mul = 100
	if type(Jazz_NaturalHealingDebtSpeedMul) == "function" then
		mul = MulDivRound(mul, Jazz_NaturalHealingDebtSpeedMul(unit), 100)
	end
	if type(Jazz_ExplodingPalmDebtSpeedMul) == "function" then
		mul = MulDivRound(mul, Jazz_ExplodingPalmDebtSpeedMul(unit), 100)
	end
	return mul
end

function Jazz_SquadBlocksWoundInfected(unit)
	return Jazz_SquadHasExplodingPalm(unit)
end

local function lExplodingPalmIsUnarmedWeapon(weapon)
	if not weapon then
		return false
	end
	if weapon.IsUnarmed then
		return true
	end
	return IsKindOf(weapon, "UnarmedWeapon")
end

--- Successful bare-hand hit → status by target current HP%.
function Jazz_ExplodingPalmOnUnarmedHit(attacker, action, attack_target, results, attack_args)
	if not attacker or not HasPerk(attacker, "ExplodingPalm") then
		return false
	end
	if not IsKindOf(attack_target, "Unit") or (attack_target.IsDead and attack_target:IsDead()) then
		return false
	end
	if action and action.ActionType and action.ActionType ~= "Melee Attack" then
		return false
	end
	local weapon = attack_args and attack_args.weapon
	if not weapon and results then
		weapon = results.weapon
	end
	if not weapon and attacker.GetActiveWeapons then
		weapon = attacker:GetActiveWeapons()
	end
	if not lExplodingPalmIsUnarmedWeapon(weapon) then
		return false
	end
	local max_hp = Max(1, attack_target.MaxHitPoints or 1)
	local hp = attack_target.HitPoints or 0
	local pct = MulDivRound(hp, 100, max_hp)
	if pct <= 20 then
		attack_target:AddStatusEffect("KnockDown")
		attack_target:AddStatusEffect("Unconscious")
		return "ko"
	elseif pct <= 35 then
		if CharacterEffectDefs and CharacterEffectDefs.Concussion then
			attack_target:AddStatusEffect("Concussion")
		end
		return "concussion"
	elseif pct <= 50 then
		if type(JazzApplyTrauma) == "function" then
			JazzApplyTrauma(attack_target, "Ribs", "Medium")
		end
		return "ribs"
	elseif pct <= 65 then
		if type(JazzApplyTrauma) == "function" then
			JazzApplyTrauma(attack_target, "Arms", "Medium")
		end
		return "arms"
	elseif pct <= 80 then
		if type(JazzApplyTrauma) == "function" then
			JazzApplyTrauma(attack_target, "Legs", "Medium")
		end
		return "legs"
	else
		-- «яйцы» / groin → same trauma zone as Groinshot (Ribs).
		if type(JazzApplyTrauma) == "function" then
			JazzApplyTrauma(attack_target, "Ribs", "Light")
		end
		attack_target:AddStatusEffect("Pain")
		return "groin"
	end
end

'''

INSTALLER = r'''
g_JAZZ_ExplodingPalmSigHidden = rawget(_G, "g_JAZZ_ExplodingPalmSigHidden") or false

local function lInstallExplodingPalmPassiveOnly()
	-- If ModItem Passive CA already owns ExplodingPalm, leave hotbar icon alone.
	-- Otherwise hide leftover vanilla palm-strike smash.
	local ca = CombatActions and CombatActions.ExplodingPalm
	if not ca or rawget(_G, "g_JAZZ_ExplodingPalmSigHidden") then
		return
	end
	if ca.ActionType == "Passive" and ca.ShowIn == "SignatureAbilities" then
		rawset(_G, "g_JAZZ_ExplodingPalmSigHidden", true)
		return
	end
	ca.ShowIn = false
	ca.ActionType = "Passive"
	ca.GetUIState = function(self, units, args)
		return "hidden"
	end
	rawset(_G, "g_JAZZ_ExplodingPalmSigHidden", true)
end
'''


def upsert_csv(path: Path, tid: str, ru: str, en: str, source: str) -> None:
    text = path.read_text(encoding="utf-8")
    # Escape quotes in fields
    def esc(s: str) -> str:
        if any(c in s for c in ',"\n'):
            return '"' + s.replace('"', '""') + '"'
        return s

    row = f"{tid},{esc(ru)},{esc(en)},,{source}\n"
    pat = re.compile(rf"(?m)^{re.escape(tid)},.*$")
    if pat.search(text):
        text = pat.sub(row.rstrip("\n"), text, count=1)
    else:
        if not text.endswith("\n"):
            text += "\n"
        text += row
    path.write_text(text, encoding="utf-8")


def replace_items_ce(items: str) -> str:
    pat = re.compile(
        r"PlaceObj\('ModItemCharacterEffectCompositeDef', \{\s*"
        r"'Group', \"Perk-Personal\",\s*'Id', \"ExplodingPalm\",[\s\S]*?"
        r"'Tier', \"Personal\",\s*\}\),",
        re.M,
    )
    new_items, n = pat.subn(ITEMS_CE.rstrip() + "\n", items, count=1)
    if not n:
        raise SystemExit("ExplodingPalm CE ModItem not found")
    return new_items


def ensure_passive_ca(items: str) -> str:
    # Find existing ModItemCombatAction with id ExplodingPalm
    for m in re.finditer(
        r"PlaceObj\('ModItemCombatAction',\s*\{([\s\S]*?)\bid\s*=\s*\"ExplodingPalm\"",
        items,
    ):
        if 'ActionType = "Passive"' in m.group(1):
            print("Passive CA already present")
            return items
    needle = (
        "\t\t\t\tPlaceObj('ModItemCharacterEffectCompositeDef', {\n"
        "\t\t\t\t\t'Group', \"Perk-Personal\",\n"
        "\t\t\t\t\t'Id', \"ExplodingPalm\","
    )
    if needle not in items:
        raise SystemExit("needle for CA insert missing")
    print("Inserted Passive CA")
    return items.replace(needle, PASSIVE_CA + needle, 1)


def patch_named(text: str) -> str:
    if "function Jazz_SquadHasExplodingPalm" in text:
        print("NamedPerks helpers already present")
    else:
        anchor = "-- Soft lock EV −25% med consume"
        if anchor not in text:
            raise SystemExit("NamedPerks anchor missing")
        text = text.replace(anchor, HELPERS.strip() + "\n\n" + anchor, 1)
        print("Inserted ExplodingPalm helpers")

    if "function lInstallExplodingPalmPassiveOnly" not in text and "lInstallExplodingPalmPassiveOnly" not in text.split("lInstallNamedPerks006Ops")[0]:
        # Place local installer next to SteroidPunch hide (before Ops uses it).
        mark = "local function lInstallSteroidPunchPassiveOnly()"
        if mark not in text:
            raise SystemExit("SteroidPunch installer mark missing")
        text = text.replace(mark, INSTALLER.strip() + "\n\n" + mark, 1)
        print("Inserted ExplodingPalm CA installer")

    if "lInstallExplodingPalmPassiveOnly()" not in text:
        text = text.replace(
            "lInstallSteroidPunchPassiveOnly()\n\tlInstallSteroidBurningDotReduce()",
            "lInstallSteroidPunchPassiveOnly()\n\tlInstallExplodingPalmPassiveOnly()\n\tlInstallSteroidBurningDotReduce()",
            1,
        )
        print("Wired ExplodingPalm installer call")
    return text


def patch_medicine(text: str) -> str:
    # Prefer combined SatDebt mul if present; keep NaturalHealing fallback.
    old_speed = (
        "\t\tif type(Jazz_NaturalHealingDebtSpeedMul) == \"function\" then\n"
        "\t\t\trate = MulDivRound(rate, Jazz_NaturalHealingDebtSpeedMul(self), 100)\n"
        "\t\tend"
    )
    new_speed = (
        "\t\tlocal sat_mul = type(Jazz_SatDebtSpeedMul) == \"function\" and Jazz_SatDebtSpeedMul(self)\n"
        "\t\t\tor (type(Jazz_NaturalHealingDebtSpeedMul) == \"function\" and Jazz_NaturalHealingDebtSpeedMul(self))\n"
        "\t\tif type(sat_mul) == \"number\" then\n"
        "\t\t\trate = MulDivRound(rate, sat_mul, 100)\n"
        "\t\tend"
    )
    if "Jazz_SatDebtSpeedMul" not in text or old_speed in text:
        if old_speed in text:
            text = text.replace(old_speed, new_speed, 1)
            print("Patched UnitData:Tick sat debt speed")
    old_hours = (
        "\tif type(Jazz_NaturalHealingDebtHoursMul) == \"function\" then\n"
        "\t\thours = Max(1, MulDivRound(hours, Jazz_NaturalHealingDebtHoursMul(unit), 100))\n"
        "\tend"
    )
    new_hours = (
        "\tlocal sat_h = type(Jazz_SatDebtHoursMul) == \"function\" and Jazz_SatDebtHoursMul(unit)\n"
        "\t\tor (type(Jazz_NaturalHealingDebtHoursMul) == \"function\" and Jazz_NaturalHealingDebtHoursMul(unit))\n"
        "\tif type(sat_h) == \"number\" then\n"
        "\t\thours = Max(1, MulDivRound(hours, sat_h, 100))\n"
        "\tend"
    )
    if old_hours in text:
        text = text.replace(old_hours, new_hours, 1)
        print("Patched trauma hours mul")

    # WoundInfected block
    needle = "function JazzApplyWoundInfected(unit)\n\tif not unit then\n\t\treturn false\n\tend\n"
    insert = (
        "function JazzApplyWoundInfected(unit)\n"
        "\tif not unit then\n"
        "\t\treturn false\n"
        "\tend\n"
        "\tif type(Jazz_SquadBlocksWoundInfected) == \"function\" and Jazz_SquadBlocksWoundInfected(unit) then\n"
        "\t\treturn false\n"
        "\tend\n"
    )
    if "Jazz_SquadBlocksWoundInfected" not in text:
        if needle not in text:
            raise SystemExit("JazzApplyWoundInfected not found")
        text = text.replace(needle, insert, 1)
        print("Patched JazzApplyWoundInfected")
    else:
        print("WoundInfected block already present")
    return text


def patch_wounds_op(text: str) -> str:
    old = (
        "\tif type(Jazz_NaturalHealingDebtSpeedMul) == \"function\" then\n"
        "\t\tprogress = MulDivRound(progress, Jazz_NaturalHealingDebtSpeedMul(merc), 100)\n"
        "\tend"
    )
    new = (
        "\tlocal sat_mul = type(Jazz_SatDebtSpeedMul) == \"function\" and Jazz_SatDebtSpeedMul(merc)\n"
        "\t\tor (type(Jazz_NaturalHealingDebtSpeedMul) == \"function\" and Jazz_NaturalHealingDebtSpeedMul(merc))\n"
        "\tif type(sat_mul) == \"number\" then\n"
        "\t\tprogress = MulDivRound(progress, sat_mul, 100)\n"
        "\tend"
    )
    if old in text:
        return text.replace(old, new, 1)
    return text


def main() -> None:
    CE.write_text(CE_TEXT, encoding="utf-8", newline="\n")
    print("Wrote ExplodingPalm.lua")

    items = ITEMS.read_text(encoding="utf-8")
    items = replace_items_ce(items)
    items = ensure_passive_ca(items)
    ITEMS.write_text(items, encoding="utf-8")

    named = NAMED.read_text(encoding="utf-8")
    NAMED.write_text(patch_named(named), encoding="utf-8", newline="\n")

    med = MED.read_text(encoding="utf-8")
    MED.write_text(patch_medicine(med), encoding="utf-8", newline="\n")

    wounds = ROOT / "Code" / "System_Wounds_OperationHeal.lua"
    w = wounds.read_text(encoding="utf-8")
    w2 = patch_wounds_op(w)
    if w2 != w:
        wounds.write_text(w2, encoding="utf-8", newline="\n")
        print("Patched System_Wounds_OperationHeal")

    upsert_csv(EN, DN_ID, "Взрывная ладонь", "Exploding Palm", "jazz:CharacterEffect/ExplodingPalm.lua")
    upsert_csv(RU, DN_ID, "Взрывная ладонь", "Exploding Palm", "jazz:CharacterEffect/ExplodingPalm.lua")
    upsert_csv(EN, DESC_ID, DESC_RU, DESC_EN, "jazz:CharacterEffect/ExplodingPalm.lua")
    upsert_csv(RU, DESC_ID, DESC_RU, DESC_EN, "jazz:CharacterEffect/ExplodingPalm.lua")
    print("Loc updated")

    meta = META.read_text(encoding="utf-8")
    # CombatAction preset
    ca_marker = "'Id', \"ExplodingPalm\",\n\t\t\t'ClassDisplayName', \"Combat Actions\""
    if ca_marker not in meta:
        ce_preset = """\t\tPlaceObj('ModResourcePreset', {
\t\t\t'Class', "CharacterEffectCompositeDef",
\t\t\t'Id', "ExplodingPalm",
\t\t\t'ClassDisplayName', "Character effect",
\t\t}),"""
        ca_preset = """\t\tPlaceObj('ModResourcePreset', {
\t\t\t'Class', "CombatAction",
\t\t\t'Id', "ExplodingPalm",
\t\t\t'ClassDisplayName', "Combat Actions",
\t\t}),
"""
        if ce_preset not in meta:
            # try find any ExplodingPalm CE preset
            m = re.search(
                r"\t\tPlaceObj\('ModResourcePreset', \{\s*'Class', \"CharacterEffectCompositeDef\",\s*'Id', \"ExplodingPalm\",[\s\S]*?\}\),",
                meta,
            )
            if not m:
                raise SystemExit("metadata CE ExplodingPalm missing")
            meta = meta[: m.start()] + ca_preset + m.group(0) + meta[m.end() :]
        else:
            meta = meta.replace(ce_preset, ca_preset + ce_preset, 1)
        print("Inserted metadata CombatAction preset")

    m = re.search(r"'version',\s*(\d+)", meta)
    ver = int(m.group(1))
    meta = meta[: m.start(1)] + str(ver + 1) + meta[m.end(1) :]
    bullet = (
        "- UNITS-006: DrQ ExplodingPalm — unarmed HP-tier statuses; sat debt +30%; "
        "block WoundInfected; Passive hotbar [no new game]"
        + "\\"
        + "n"
    )
    meta = re.sub(r"('last_changes',\s*\")", lambda mm: mm.group(1) + bullet, meta, count=1)
    META.write_text(meta, encoding="utf-8")
    print(f"metadata version {ver} -> {ver + 1}")


if __name__ == "__main__":
    main()
