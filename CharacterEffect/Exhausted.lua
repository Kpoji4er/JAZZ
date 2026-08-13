UndefineClass('Exhausted')
DefineClass.Exhausted = {
	__parents = { "StatusEffect" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",

	object_class = "StatusEffect",
	Parameters = {
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
	unit_reactions = {
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
	DisplayName = T(707410221892, --[[ModItemCharacterEffectCompositeDef Exhausted DisplayName]] "Exhausted"),
	Description = T(890000000013107, --[[ModItemCharacterEffectCompositeDef Exhausted Description]] "AP penalty <em><ap_loss></em> at turn start. No Free Move. Cannot travel until rested in Sat View."),
	OnAdded = function (self, obj)
		obj:AddStatusEffectImmunity("FreeMove", self.class)
	end,
	OnRemoved = function (self, obj)
		obj:RemoveStatusEffectImmunity("FreeMove", self.class)
	end,
	type = "Debuff",
	Icon = "UI/Hud/Status effects/exhausted",
	Shown = true,
	ShownSatelliteView = true,
	HasFloatingText = true,
}
