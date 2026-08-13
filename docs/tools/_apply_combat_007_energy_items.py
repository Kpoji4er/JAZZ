# docs/tools/_apply_combat_007_energy_items.py
"""Insert/update JAZZ-COMBAT-007 energy ladder ModItems in items.lua + metadata code list."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ITEMS = ROOT / "items.lua"
META = ROOT / "metadata.lua"

CODE_ENTRY = '\t\t"Code/System_EnergyLadder.lua",'
CE_FILES = [
	"CharacterEffect/Fit.lua",
	"CharacterEffect/Winded.lua",
	"CharacterEffect/Fatigued.lua",
	"CharacterEffect/Tired.lua",
	"CharacterEffect/Exhausted.lua",
	"CharacterEffect/WellRested.lua",
	"CharacterEffect/FreeMove.lua",
]

# Minimal ModItem stubs: editor loads companion .lua via UndefineClass/DefineClass.
# Full logic lives in CharacterEffect/*.lua; items.lua registers the ModItem IDs.


def _ce_block(ce_id: str, body: str) -> str:
	return f"""\
		PlaceObj('ModItemCharacterEffectCompositeDef', {{
			'Id', "{ce_id}",
{body}
		}}),
"""


FIT = _ce_block(
	"Fit",
	"""\
			'Parameters', {
				PlaceObj('PresetParamNumber', {
					'Name', "ap_gain",
					'Value', 1,
					'Tag', "<ap_gain>",
				}),
				PlaceObj('PresetParamPercent', {
					'Name', "fm_mul",
					'Value', 120,
					'Tag', "<fm_mul>",
				}),
				PlaceObj('PresetParamNumber', {
					'Name', "opening_fm_turns",
					'Value', 1,
					'Tag', "<opening_fm_turns>",
				}),
				PlaceObj('PresetParamNumber', {
					'Name', "opening_fm_bonus",
					'Value', 2,
					'Tag', "<opening_fm_bonus>",
				}),
			},
			'object_class', "StatusEffect",
			'unit_reactions', {
				PlaceObj('UnitReaction', {
					Event = "OnCalcStartTurnAP",
					Handler = function (self, target, value)
						return value + self:ResolveValue("ap_gain") * const.Scale.AP
					end,
				}),
				PlaceObj('UnitReaction', {
					Event = "OnCalcFreeMove",
					Handler = function (self, target, data)
						data.mul = MulDivRound(data.mul or 100, self:ResolveValue("fm_mul") or 120, 100)
						local add = JazzEnergyOpeningFmBonus(target, self)
						if add > 0 then
							data.add = (data.add or 0) + add
						end
					end,
				}),
			},
			'DisplayName', T(890000000013100, --[[ModItemCharacterEffectCompositeDef Fit DisplayName]] "Fit"),
			'Description', T(890000000013101, --[[ModItemCharacterEffectCompositeDef Fit Description]] "Maximum AP <em>+<ap_gain></em>. Free Move <em>x<fm_mul>%</em>. First <em><opening_fm_turns></em> combat turn(s): extra <em>+<opening_fm_bonus></em> Free Move."),
			'AddEffectText', T(890000000013118, --[[ModItemCharacterEffectCompositeDef Fit AddEffectText]] "<em><DisplayName></em> feels fit"),
			'type', "Buff",
			'Icon', "Mod/e6L4ECj/Icons/StatusEffects/Fit.png",
			'Shown', true,
			'ShownSatelliteView', true,
			'HasFloatingText', true,""",
)

WINDED = _ce_block(
	"Winded",
	"""\
			'Parameters', {
				PlaceObj('PresetParamPercent', {
					'Name', "fm_mul",
					'Value', 100,
					'Tag', "<fm_mul>",
				}),
			},
			'object_class', "StatusEffect",
			'unit_reactions', {
				PlaceObj('UnitReaction', {
					Event = "OnCalcFreeMove",
					Handler = function (self, target, data)
						data.mul = MulDivRound(data.mul or 100, self:ResolveValue("fm_mul") or 100, 100)
					end,
				}),
			},
			'DisplayName', T(890000000013102, --[[ModItemCharacterEffectCompositeDef Winded DisplayName]] "Winded"),
			'Description', T(890000000013103, --[[ModItemCharacterEffectCompositeDef Winded Description]] "Slightly worn from travel. Free Move at baseline (<em><fm_mul>%</em>). No AP penalty. Rest in Sat View to recover."),
			'AddEffectText', T(890000000013119, --[[ModItemCharacterEffectCompositeDef Winded AddEffectText]] "<em><DisplayName></em> is winded"),
			'type', "Debuff",
			'Icon', "Mod/e6L4ECj/Icons/StatusEffects/Winded.png",
			'Shown', true,
			'ShownSatelliteView', true,
			'HasFloatingText', true,""",
)

FATIGUED = _ce_block(
	"Fatigued",
	"""\
			'Parameters', {
				PlaceObj('PresetParamPercent', {
					'Name', "fm_mul",
					'Value', 75,
					'Tag', "<fm_mul>",
				}),
			},
			'object_class', "StatusEffect",
			'unit_reactions', {
				PlaceObj('UnitReaction', {
					Event = "OnCalcFreeMove",
					Handler = function (self, target, data)
						data.mul = MulDivRound(data.mul or 100, self:ResolveValue("fm_mul") or 75, 100)
					end,
				}),
			},
			'DisplayName', T(890000000013104, --[[ModItemCharacterEffectCompositeDef Fatigued DisplayName]] "Fatigued"),
			'Description', T(890000000013105, --[[ModItemCharacterEffectCompositeDef Fatigued Description]] "Free Move reduced to <em><fm_mul>%</em>. No AP penalty yet. Rest in Sat View to recover."),
			'AddEffectText', T(890000000013120, --[[ModItemCharacterEffectCompositeDef Fatigued AddEffectText]] "<em><DisplayName></em> is fatigued"),
			'type', "Debuff",
			'Icon', "Mod/e6L4ECj/Icons/StatusEffects/Fatigued.png",
			'Shown', true,
			'ShownSatelliteView', true,
			'HasFloatingText', true,""",
)

TIRED = _ce_block(
	"Tired",
	"""\
			'Parameters', {
				PlaceObj('PresetParamNumber', {
					'Name', "ap_loss",
					'Value', -1,
					'Tag', "<ap_loss>",
				}),
				PlaceObj('PresetParamPercent', {
					'Name', "fm_mul",
					'Value', 50,
					'Tag', "<fm_mul>",
				}),
				PlaceObj('PresetParamNumber', {
					'Name', "duration",
					'Value', 12,
					'Tag', "<duration>",
				}),
			},
			'object_class', "StatusEffect",
			'unit_reactions', {
				PlaceObj('UnitReaction', {
					Event = "OnCalcStartTurnAP",
					Handler = function (self, target, value)
						return value + self:ResolveValue("ap_loss") * const.Scale.AP
					end,
				}),
				PlaceObj('UnitReaction', {
					Event = "OnCalcFreeMove",
					Handler = function (self, target, data)
						data.mul = MulDivRound(data.mul or 100, self:ResolveValue("fm_mul") or 50, 100)
					end,
				}),
			},
			'DisplayName', T(299677471612, --[[ModItemCharacterEffectCompositeDef Tired DisplayName]] "Tired"),
			'Description', T(890000000013106, --[[ModItemCharacterEffectCompositeDef Tired Description]] "Maximum AP <em><ap_loss></em>. Free Move <em><fm_mul>%</em>. Recover by resting in Sat View."),
			'type', "Debuff",
			'Icon', "UI/Hud/Status effects/tired",
			'Shown', true,
			'ShownSatelliteView', true,
			'HasFloatingText', true,""",
)

EXHAUSTED = _ce_block(
	"Exhausted",
	"""\
			'Parameters', {
				PlaceObj('PresetParamNumber', {
					'Name', "ap_loss",
					'Value', -2,
					'Tag', "<ap_loss>",
				}),
				PlaceObj('PresetParamNumber', {
					'Name', "duration",
					'Value', 12,
					'Tag', "<duration>",
				}),
			},
			'object_class', "StatusEffect",
			'unit_reactions', {
				PlaceObj('UnitReaction', {
					Event = "OnBeginTurn",
					Handler = function (self, target)
						target:ConsumeAP(-self:ResolveValue("ap_loss") * const.Scale.AP)
					end,
				}),
				PlaceObj('UnitReaction', {
					Event = "OnCalcFreeMove",
					Handler = function (self, target, data)
						data.max = 0
						data.mul = 0
					end,
				}),
			},
			'DisplayName', T(707410221892, --[[ModItemCharacterEffectCompositeDef Exhausted DisplayName]] "Exhausted"),
			'Description', T(890000000013107, --[[ModItemCharacterEffectCompositeDef Exhausted Description]] "AP penalty <em><ap_loss></em> at turn start. No Free Move. Cannot travel until rested in Sat View."),
			'OnAdded', function (self, obj)
				obj:AddStatusEffectImmunity("FreeMove", self.class)
			end,
			'OnRemoved', function (self, obj)
				obj:RemoveStatusEffectImmunity("FreeMove", self.class)
			end,
			'type', "Debuff",
			'Icon', "UI/Hud/Status effects/exhausted",
			'Shown', true,
			'ShownSatelliteView', true,
			'HasFloatingText', true,""",
)

WELLRESTED = _ce_block(
	"WellRested",
	"""\
			'Parameters', {
				PlaceObj('PresetParamNumber', {
					'Name', "ap_gain",
					'Value', 2,
					'Tag', "<ap_gain>",
				}),
				PlaceObj('PresetParamPercent', {
					'Name', "fm_mul",
					'Value', 120,
					'Tag', "<fm_mul>",
				}),
				PlaceObj('PresetParamNumber', {
					'Name', "opening_fm_turns",
					'Value', 3,
					'Tag', "<opening_fm_turns>",
				}),
				PlaceObj('PresetParamNumber', {
					'Name', "opening_fm_bonus",
					'Value', 2,
					'Tag', "<opening_fm_bonus>",
				}),
			},
			'object_class', "StatusEffect",
			'unit_reactions', {
				PlaceObj('UnitReaction', {
					Event = "OnCalcStartTurnAP",
					Handler = function (self, target, value)
						return value + self:ResolveValue("ap_gain") * const.Scale.AP
					end,
				}),
				PlaceObj('UnitReaction', {
					Event = "OnCalcFreeMove",
					Handler = function (self, target, data)
						data.mul = MulDivRound(data.mul or 100, self:ResolveValue("fm_mul") or 120, 100)
						local add = JazzEnergyOpeningFmBonus(target, self)
						if add > 0 then
							data.add = (data.add or 0) + add
						end
					end,
				}),
			},
			'DisplayName', T(789783285719, --[[ModItemCharacterEffectCompositeDef WellRested DisplayName]] "Well Rested"),
			'Description', T(890000000013108, --[[ModItemCharacterEffectCompositeDef WellRested Description]] "Maximum AP <em>+<ap_gain></em>. Free Move <em>x<fm_mul>%</em>. First <em><opening_fm_turns></em> combat turns: extra <em>+<opening_fm_bonus></em> Free Move."),
			'AddEffectText', T(353089370853, --[[ModItemCharacterEffectCompositeDef WellRested AddEffectText]] "<em><DisplayName></em> is well rested"),
			'RemoveEffectText', T(945859256424, --[[ModItemCharacterEffectCompositeDef WellRested RemoveEffectText]] "<em><DisplayName></em> is no longer well rested"),
			'type', "Buff",
			'Icon', "UI/Hud/Status effects/well_rested",
			'Shown', true,
			'ShownSatelliteView', true,
			'HasFloatingText', true,""",
)

FREEMOVE = _ce_block(
	"FreeMove",
	"""\
			'object_class', "CharacterEffect",
			'unit_reactions', {
				PlaceObj('UnitReaction', {
					Event = "OnCombatActionEnd",
					Handler = function (self, target)
						if target.free_move_ap <= 0 then
							target:RemoveStatusEffect("FreeMove")
						end
					end,
				}),
			},
			'Conditions', {
				PlaceObj('CheckExpression', {
					Expression = function (self, obj)
						local cap = rawget(const, "utExhausted") or 4
						return g_Combat and (obj.Tiredness or 0) < cap
					end,
				}),
				PlaceObj('CheckExpression', {
					Expression = function (self, obj)
						if not IsGameRuleActive("HeavyWounds") then return true end
						local wounds = obj:GetStatusEffect("Wounded")
						local max_wounds = GameRuleDefs.HeavyWounds:ResolveValue("MaxWoundsEffect")
						return not wounds or wounds.stacks < max_wounds
					end,
				}),
			},
			'DisplayName', T(574672731472, --[[ModItemCharacterEffectCompositeDef FreeMove DisplayName]] "Free Move"),
			'Description', T(824694494336, --[[ModItemCharacterEffectCompositeDef FreeMove Description]] "Move without spending AP. Removed after attacking or after moving the allowed distance (based on <agility>)."),
			'OnAdded', function (self, obj)
				if not IsKindOf(obj, "Unit") then return end
				local cur_free_ap = obj.free_move_ap
				local free_ap = Max(0, MulDivRound(obj.Agility - 40, const.Scale.AP, 10))
				local data = {min = 0, max = 999, add = 0, mul = 100}
				if obj.team and obj.team.player_enemy then
					data.mul = PercentModifyByDifficulty(GameDifficulties[Game.game_difficulty]:ResolveValue("freeMoveBonus"))
				end
				obj:CallReactions("OnCalcFreeMove", data)
				free_ap = MulDivRound(free_ap + data.add * const.Scale.AP, data.mul, 100)
				free_ap = Clamp(free_ap, data.min*const.Scale.AP, data.max*const.Scale.AP)
				if IsGameRuleActive("HeavyWounds") then
					local wounds = obj:GetStatusEffect("Wounded")
					if wounds and wounds.stacks >= 1 then
						local max_wounds = GameRuleDefs.HeavyWounds:ResolveValue("MaxWoundsEffect")
						local per_wound_percent = GameRuleDefs.HeavyWounds:ResolveValue("FreeMoveLost")
						free_ap = Max(0, free_ap - MulDivRound(free_ap, Min(wounds.stacks, max_wounds)*per_wound_percent, 100))
					end
				end
				local prev_ap = obj.ActionPoints
				obj:GainAP(free_ap - cur_free_ap)
				if obj.ActionPoints > prev_ap then
					obj.free_move_ap = free_ap
					Msg("UnitAPChanged", obj)
					ObjModified(obj)
				end
			end,
			'OnRemoved', function (self, obj)
				if IsKindOf(obj, "Unit") then
					obj:ConsumeAP(obj.free_move_ap)
					obj.free_move_ap = 0
					Msg("UnitAPChanged", obj, self.class)
				end
			end,
			'type', "Buff",
			'Icon', "UI/Hud/Status effects/mobility",
			'RemoveOnEndCombat', true,
			'Shown', true,""",
)

CODE_ITEM = """\
		PlaceObj('ModItemCode', {
			'name', "System_EnergyLadder",
			'CodeFileName', "Code/System_EnergyLadder.lua",
		}),
"""

BLOCKS = [CODE_ITEM, FIT, WINDED, FATIGUED, TIRED, EXHAUSTED, WELLRESTED, FREEMOVE]


def _remove_existing(text: str) -> str:
	# Remove prior COMBAT-007 energy ModItems if re-run (non-greedy by Id marker).
	for ce_id in ("Fit", "Winded", "Fatigued", "Tired", "Exhausted", "WellRested", "FreeMove"):
		start = text.find(f"\t\tPlaceObj('ModItemCharacterEffectCompositeDef', {{\n\t\t\t'Id', \"{ce_id}\",")
		if start < 0:
			# alternate indent
			start = text.find(f"'Id', \"{ce_id}\",\n\t\t\t'Parameters'")
			if start < 0:
				continue
			# walk back to PlaceObj
			start = text.rfind("PlaceObj('ModItemCharacterEffectCompositeDef'", 0, start)
			if start < 0:
				continue
			# include leading tabs
			while start > 0 and text[start - 1] in "\t":
				start -= 1
		# find matching close at same indent level: \t\t}),
		depth = 0
		i = start
		end = -1
		while i < len(text):
			if text.startswith("PlaceObj(", i):
				depth += 1
				i += 8
				continue
			if text.startswith("}),", i):
				depth -= 1
				i += 3
				if depth == 0:
					# consume trailing newline
					if i < len(text) and text[i] == "\n":
						i += 1
					end = i
					break
				continue
			i += 1
		if end > start:
			text = text[:start] + text[end:]
	# System_EnergyLadder ModItemCode
	start = text.find("\t\tPlaceObj('ModItemCode', {\n\t\t\t'name', \"System_EnergyLadder\",")
	if start >= 0:
		end = text.find("\t\t}),\n", start)
		if end >= 0:
			end = end + len("\t\t}),\n")
			text = text[:start] + text[end:]
	return text


def _insert_after_gasmask(text: str) -> str:
	anchor = "\t\tPlaceObj('ModItemCode', {\n\t\t\t'name', \"System_GasMask\","
	idx = text.find(anchor)
	if idx < 0:
		raise SystemExit("anchor System_GasMask not found in items.lua")
	# find end of that PlaceObj
	end = text.find("\t\t}),\n", idx)
	if end < 0:
		raise SystemExit("end of System_GasMask ModItem not found")
	end = end + len("\t\t}),\n")
	blob = "".join(BLOCKS)
	return text[:end] + blob + text[end:]


def _patch_metadata() -> None:
	text = META.read_text(encoding="utf-8")
	if "Code/System_EnergyLadder.lua" not in text:
		# insert after System_GasMask.lua in code list
		needle = '\t\t"Code/System_GasMask.lua",\n'
		if needle not in text:
			raise SystemExit("metadata code list: System_GasMask.lua not found")
		extra = needle + CODE_ENTRY + "\n"
		for f in CE_FILES:
			extra += f'\t\t"{f}",\n'
		text = text.replace(needle, extra, 1)
	# ModResourcePreset entries
	for ce_id in ("Fit", "Winded", "Fatigued", "Tired", "Exhausted", "WellRested", "FreeMove"):
		marker = f"'Id', \"{ce_id}\""
		if f"CharacterEffectCompositeDef\",\n\t\t\t{marker}" in text or f"'Id', \"{ce_id}\",\n\t\t\t'ClassDisplayName', \"Character effect\"" in text:
			continue
		# simpler: if Id already present as CharacterEffectCompositeDef skip
		if re.search(rf"Class', \"CharacterEffectCompositeDef\",\s*'Id', \"{ce_id}\"", text):
			continue
		insert = f"""\
		PlaceObj('ModResourcePreset', {{
			'Class', "CharacterEffectCompositeDef",
			'Id', "{ce_id}",
			'ClassDisplayName', "Character effect",
		}}),
"""
		anchor = "\t\tPlaceObj('ModResourcePreset', {\n\t\t\t'Class', \"CharacterEffectCompositeDef\",\n\t\t\t'Id', \"Weight_5Class\","
		aidx = text.find(anchor)
		if aidx < 0:
			raise SystemExit("Weight_5Class ModResourcePreset not found")
		aend = text.find("\t\t}),\n", aidx) + len("\t\t}),\n")
		text = text[:aend] + insert + text[aend:]
	META.write_text(text, encoding="utf-8")


def main() -> None:
	text = ITEMS.read_text(encoding="utf-8")
	text = _remove_existing(text)
	text = _insert_after_gasmask(text)
	ITEMS.write_text(text, encoding="utf-8")
	_patch_metadata()
	print("OK: energy ladder ModItems + metadata")


if __name__ == "__main__":
	main()
