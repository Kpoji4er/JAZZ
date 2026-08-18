# -*- coding: utf-8 -*-
"""Patch Trauma* CE companions for MED-006 effective-tier helpers + metadata load."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def patch_metadata() -> None:
    meta_path = ROOT / "metadata.lua"
    text = meta_path.read_text(encoding="utf-8")
    if "System_Medicine_MED006.lua" in text:
        print("metadata: already present")
        return
    needle = '"Code/Systems_Medicine.lua",'
    insert = needle + '\n\t\t"Code/System_Medicine_MED006.lua",'
    if needle not in text:
        raise SystemExit("metadata needle missing")
    meta_path.write_text(text.replace(needle, insert, 1), encoding="utf-8")
    print("metadata: inserted MED006")


def write(name: str, body: str) -> None:
    path = ROOT / "CharacterEffect" / name
    path.write_text(body.strip() + "\n", encoding="utf-8", newline="\n")
    print("wrote", name)


def main() -> None:
    patch_metadata()

    write(
        "TraumaLegsHeavy.lua",
        r"""
UndefineClass('TraumaLegsHeavy')
DefineClass.TraumaLegsHeavy = {
	__parents = { "JazzTraumaEffect" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",
	object_class = "JazzTraumaEffect",
	Parameters = {
		PlaceObj('PresetParamNumber', {
			'Name', "move_ap_modifier",
			'Value', 150,
			'Tag', "<move_ap_modifier>",
		}),
	},
	unit_reactions = {
		PlaceObj('UnitReaction', {
			Event = "OnEndTurn",
			Handler = function(self, target)
				JazzTraumaHeavyPainRamp(target)
			end,
		}),
		PlaceObj('UnitReaction', {
			Event = "OnCalcMoveModifier",
			Handler = function(self, target, value, action)
				JazzTraumaPainOnZoneUse(target, "Legs")
				return value + JazzTraumaResolveNum(self, target, JazzTraumaLegsMoveAp, "move_ap_modifier")
			end,
		}),
		PlaceObj('UnitReaction', {
			Event = "OnCalcFreeMove",
			Handler = function(self, target, data)
				if not JazzTraumaBlocksFreeMove or JazzTraumaBlocksFreeMove(self, target) then
					data.add = 0
					data.mul = 0
				end
			end,
		}),
		PlaceObj('UnitReaction', {
			Event = "OnBeginTurn",
			Handler = function(self, target)
				if not JazzTraumaBlocksFreeMove or JazzTraumaBlocksFreeMove(self, target) then
					target:RemoveStatusEffect("FreeMove")
				end
			end,
		}),
	},
	DisplayName = T(890000000010110, "Leg Trauma (Heavy)"),
	Description = T(890000000010111, "Move cost <color EmStyle>+<move_ap_modifier>%</color>. Almost immobile. +3 Pain when moving; +1 Pain/turn if unused."),
	OnAdded = function(self, obj)
		Msg("UnitAPChanged", obj)
	end,
	OnRemoved = function(self, obj)
		Msg("UnitAPChanged", obj)
	end,
	type = "Debuff",
	Icon = "Mod/e6L4ECj/Icons/StatusEffects/TraumaLegsHeavy.png",
	Shown = true,
	ShownSatelliteView = true,
	HasFloatingText = true,
}
""",
    )

    write(
        "TraumaLegsMedium.lua",
        r"""
UndefineClass('TraumaLegsMedium')
DefineClass.TraumaLegsMedium = {
	__parents = { "JazzTraumaEffect" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",
	object_class = "JazzTraumaEffect",
	Parameters = {
		PlaceObj('PresetParamNumber', {
			'Name', "move_ap_modifier",
			'Value', 50,
			'Tag', "<move_ap_modifier>",
		}),
	},
	unit_reactions = {
		PlaceObj('UnitReaction', {
			Event = "OnCalcMoveModifier",
			Handler = function(self, target, value, action)
				if self.class == "TraumaLegsMedium" then
					JazzTraumaPainOnZoneUse(target, "Legs")
				end
				return value + JazzTraumaResolveNum(self, target, JazzTraumaLegsMoveAp, "move_ap_modifier")
			end,
		}),
		PlaceObj('UnitReaction', {
			Event = "OnCalcFreeMove",
			Handler = function(self, target, data)
				if not JazzTraumaBlocksFreeMove or JazzTraumaBlocksFreeMove(self, target) then
					data.add = 0
					data.mul = 0
				end
			end,
		}),
		PlaceObj('UnitReaction', {
			Event = "OnBeginTurn",
			Handler = function(self, target)
				if not JazzTraumaBlocksFreeMove or JazzTraumaBlocksFreeMove(self, target) then
					target:RemoveStatusEffect("FreeMove")
				end
			end,
		}),
	},
	DisplayName = T(890000000010108, "Leg Trauma (Medium)"),
	Description = T(890000000010109, "Move cost <color EmStyle>+<move_ap_modifier>%</color>. No Free Move / sprint. +2 Pain when moving."),
	OnAdded = function(self, obj)
		Msg("UnitAPChanged", obj)
	end,
	OnRemoved = function(self, obj)
		Msg("UnitAPChanged", obj)
	end,
	type = "Debuff",
	Icon = "Mod/e6L4ECj/Icons/StatusEffects/TraumaLegsMedium.png",
	Shown = true,
	ShownSatelliteView = true,
	HasFloatingText = true,
}
""",
    )

    write(
        "TraumaArmsHeavy.lua",
        r"""
UndefineClass('TraumaArmsHeavy')
DefineClass.TraumaArmsHeavy = {
	__parents = { "JazzTraumaEffect" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",
	object_class = "JazzTraumaEffect",
	Parameters = {
		PlaceObj('PresetParamPercent', {
			'Name', "cth_penalty",
			'Value', 50,
			'Tag', "<cth_penalty>%",
		}),
	},
	unit_reactions = {
		PlaceObj('UnitReaction', {
			Event = "OnEndTurn",
			Handler = function(self, target)
				JazzTraumaHeavyPainRamp(target)
			end,
		}),
		PlaceObj('UnitReaction', {
			Event = "OnFirearmAttackStart",
			Handler = function(self, target, attacker, attack_target, action, attack_args)
				if target == attacker then
					JazzTraumaPainOnZoneUse(attacker, "Arms")
				end
			end,
		}),
		PlaceObj('UnitReaction', {
			Event = "OnCalcChanceToHit",
			Handler = function(self, target, attacker, action, attack_target, weapon1, weapon2, data)
				if target == attacker then
					ApplyCthModifier_Add(self, data, -JazzTraumaResolveNum(self, attacker, JazzTraumaArmsCthPenalty, "cth_penalty"))
				end
			end,
		}),
	},
	DisplayName = T(890000000010104, "Arm Trauma (Heavy)"),
	Description = T(890000000010105, "Severe accuracy penalty <color EmStyle><cth_penalty>%</color>. Nearly unable to fight. +3 Pain when using arms; +1 Pain/turn if unused."),
	type = "Debuff",
	Icon = "Mod/e6L4ECj/Icons/StatusEffects/TraumaArmsHeavy.png",
	Shown = true,
	ShownSatelliteView = true,
	HasFloatingText = true,
}
""",
    )

    write(
        "TraumaArmsMedium.lua",
        r"""
UndefineClass('TraumaArmsMedium')
DefineClass.TraumaArmsMedium = {
	__parents = { "JazzTraumaEffect" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",
	object_class = "JazzTraumaEffect",
	Parameters = {
		PlaceObj('PresetParamPercent', {
			'Name', "cth_penalty",
			'Value', 20,
			'Tag', "<cth_penalty>%",
		}),
	},
	unit_reactions = {
		PlaceObj('UnitReaction', {
			Event = "OnFirearmAttackStart",
			Handler = function(self, target, attacker, attack_target, action, attack_args)
				if target == attacker then
					JazzTraumaPainOnZoneUse(attacker, "Arms")
				end
			end,
		}),
		PlaceObj('UnitReaction', {
			Event = "OnCalcChanceToHit",
			Handler = function(self, target, attacker, action, attack_target, weapon1, weapon2, data)
				if target == attacker then
					ApplyCthModifier_Add(self, data, -JazzTraumaResolveNum(self, attacker, JazzTraumaArmsCthPenalty, "cth_penalty"))
				end
			end,
		}),
	},
	DisplayName = T(890000000010102, "Arm Trauma (Medium)"),
	Description = T(890000000010103, "Accuracy penalty <color EmStyle><cth_penalty>%</color>. +2 Pain when using arms."),
	type = "Debuff",
	Icon = "Mod/e6L4ECj/Icons/StatusEffects/TraumaArmsMedium.png",
	Shown = true,
	ShownSatelliteView = true,
	HasFloatingText = true,
}
""",
    )

    write(
        "TraumaRibsHeavy.lua",
        r"""
UndefineClass('TraumaRibsHeavy')
DefineClass.TraumaRibsHeavy = {
	__parents = { "JazzTraumaEffect" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",
	object_class = "JazzTraumaEffect",
	Parameters = {
		PlaceObj('PresetParamNumber', {
			'Name', "APLoss",
			'Value', 5,
			'Tag', "<APLoss>",
		}),
	},
	unit_reactions = {
		PlaceObj('UnitReaction', {
			Event = "OnEndTurn",
			Handler = function(self, target)
				JazzTraumaHeavyPainRamp(target)
			end,
		}),
		PlaceObj('UnitReaction', {
			Event = "OnCalcStartTurnAP",
			Handler = function(self, target, value)
				JazzTraumaPainOnZoneUse(target, "Ribs")
				return value - JazzTraumaResolveNum(self, target, JazzTraumaRibsApLoss, "APLoss") * const.Scale.AP
			end,
		}),
		PlaceObj('UnitReaction', {
			Event = "OnCalcFreeMove",
			Handler = function(self, target, data)
				if not JazzTraumaBlocksFreeMove or JazzTraumaBlocksFreeMove(self, target) then
					data.add = 0
					data.mul = 0
				end
			end,
		}),
		PlaceObj('UnitReaction', {
			Event = "OnBeginTurn",
			Handler = function(self, target)
				if not JazzTraumaBlocksFreeMove or JazzTraumaBlocksFreeMove(self, target) then
					target:RemoveStatusEffect("FreeMove")
				end
			end,
		}),
	},
	DisplayName = T(890000000010116, "Rib Trauma (Heavy)"),
	Description = T(890000000010117, "Start-of-turn AP <color EmStyle>-<APLoss></color>. Combat-ineffective. +3 Pain at turn start; +1 Pain/turn if unused. No Tiredness."),
	OnAdded = function(self, obj)
		Msg("UnitAPChanged", obj)
	end,
	OnRemoved = function(self, obj)
		Msg("UnitAPChanged", obj)
	end,
	type = "Debuff",
	Icon = "Mod/e6L4ECj/Icons/StatusEffects/TraumaRibsHeavy.png",
	Shown = true,
	ShownSatelliteView = true,
	HasFloatingText = true,
}
""",
    )

    write(
        "TraumaRibsMedium.lua",
        r"""
UndefineClass('TraumaRibsMedium')
DefineClass.TraumaRibsMedium = {
	__parents = { "JazzTraumaEffect" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",
	object_class = "JazzTraumaEffect",
	Parameters = {
		PlaceObj('PresetParamNumber', {
			'Name', "APLoss",
			'Value', 2,
			'Tag', "<APLoss>",
		}),
	},
	unit_reactions = {
		PlaceObj('UnitReaction', {
			Event = "OnCalcStartTurnAP",
			Handler = function(self, target, value)
				if self.class == "TraumaRibsMedium" then
					JazzTraumaPainOnZoneUse(target, "Ribs")
				end
				return value - JazzTraumaResolveNum(self, target, JazzTraumaRibsApLoss, "APLoss") * const.Scale.AP
			end,
		}),
		PlaceObj('UnitReaction', {
			Event = "OnCalcFreeMove",
			Handler = function(self, target, data)
				if not JazzTraumaBlocksFreeMove or JazzTraumaBlocksFreeMove(self, target) then
					data.add = 0
					data.mul = 0
				end
			end,
		}),
		PlaceObj('UnitReaction', {
			Event = "OnBeginTurn",
			Handler = function(self, target)
				if not JazzTraumaBlocksFreeMove or JazzTraumaBlocksFreeMove(self, target) then
					target:RemoveStatusEffect("FreeMove")
				end
			end,
		}),
	},
	DisplayName = T(890000000010114, "Rib Trauma (Medium)"),
	Description = T(890000000010115, "Start-of-turn AP <color EmStyle>-<APLoss></color>. No Free Move. +2 Pain at the start of the turn. No Tiredness."),
	OnAdded = function(self, obj)
		Msg("UnitAPChanged", obj)
	end,
	OnRemoved = function(self, obj)
		Msg("UnitAPChanged", obj)
	end,
	type = "Debuff",
	Icon = "Mod/e6L4ECj/Icons/StatusEffects/TraumaRibsMedium.png",
	Shown = true,
	ShownSatelliteView = true,
	HasFloatingText = true,
}
""",
    )

    write(
        "TraumaHeadHeavy.lua",
        r"""
UndefineClass('TraumaHeadHeavy')
DefineClass.TraumaHeadHeavy = {
	__parents = { "JazzTraumaEffect" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",
	object_class = "JazzTraumaEffect",
	Parameters = {
		PlaceObj('PresetParamPercent', {
			'Name', "cth_penalty",
			'Value', 40,
			'Tag', "<cth_penalty>%",
		}),
		PlaceObj('PresetParamNumber', {
			'Name', "sight_modifier",
			'Value', -50,
			'Tag', "<sight_modifier>",
		}),
	},
	unit_reactions = {
		PlaceObj('UnitReaction', {
			Event = "OnEndTurn",
			Handler = function(self, target)
				JazzTraumaHeavyPainRamp(target)
			end,
		}),
		PlaceObj('UnitReaction', {
			Event = "OnFirearmAttackStart",
			Handler = function(self, target, attacker, attack_target, action, attack_args)
				if target == attacker then
					JazzTraumaPainOnZoneUse(attacker, "Head")
				end
			end,
		}),
		PlaceObj('UnitReaction', {
			Event = "OnCalcChanceToHit",
			Handler = function(self, target, attacker, action, attack_target, weapon1, weapon2, data)
				if target == attacker then
					ApplyCthModifier_Add(self, data, -JazzTraumaResolveNum(self, attacker, JazzTraumaHeadCthPenalty, "cth_penalty"))
				end
			end,
		}),
		PlaceObj('UnitReaction', {
			Event = "OnCalcSightModifier",
			Handler = function(self, target, value, observer, other, step_pos, darkness)
				if target == observer then
					return value + JazzTraumaResolveNum(self, target, JazzTraumaHeadSightModifier, "sight_modifier")
				end
			end,
		}),
	},
	DisplayName = T(890000000010122, "Head Trauma (Heavy)"),
	Description = T(890000000010123, "Severe sight/accuracy loss. Nearly combat-ineffective. +3 Pain when aiming or firing; +1 Pain/turn if unused."),
	type = "Debuff",
	Icon = "Mod/e6L4ECj/Icons/StatusEffects/TraumaHeadHeavy.png",
	Shown = true,
	ShownSatelliteView = true,
	HasFloatingText = true,
}
""",
    )

    write(
        "TraumaHeadMedium.lua",
        r"""
UndefineClass('TraumaHeadMedium')
DefineClass.TraumaHeadMedium = {
	__parents = { "JazzTraumaEffect" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",
	object_class = "JazzTraumaEffect",
	Parameters = {
		PlaceObj('PresetParamPercent', {
			'Name', "cth_penalty",
			'Value', 15,
			'Tag', "<cth_penalty>%",
		}),
		PlaceObj('PresetParamNumber', {
			'Name', "sight_modifier",
			'Value', -20,
			'Tag', "<sight_modifier>",
		}),
	},
	unit_reactions = {
		PlaceObj('UnitReaction', {
			Event = "OnFirearmAttackStart",
			Handler = function(self, target, attacker, attack_target, action, attack_args)
				if target == attacker then
					JazzTraumaPainOnZoneUse(attacker, "Head")
				end
			end,
		}),
		PlaceObj('UnitReaction', {
			Event = "OnCalcChanceToHit",
			Handler = function(self, target, attacker, action, attack_target, weapon1, weapon2, data)
				if target == attacker then
					ApplyCthModifier_Add(self, data, -JazzTraumaResolveNum(self, attacker, JazzTraumaHeadCthPenalty, "cth_penalty"))
				end
			end,
		}),
		PlaceObj('UnitReaction', {
			Event = "OnCalcSightModifier",
			Handler = function(self, target, value, observer, other, step_pos, darkness)
				if target == observer then
					return value + JazzTraumaResolveNum(self, target, JazzTraumaHeadSightModifier, "sight_modifier")
				end
			end,
		}),
	},
	DisplayName = T(890000000010120, "Head Trauma (Medium)"),
	Description = T(890000000010121, "Sight and accuracy penalties. +2 Pain when aiming or firing."),
	type = "Debuff",
	Icon = "Mod/e6L4ECj/Icons/StatusEffects/TraumaHeadMedium.png",
	Shown = true,
	ShownSatelliteView = true,
	HasFloatingText = true,
}
""",
    )


if __name__ == "__main__":
    main()
