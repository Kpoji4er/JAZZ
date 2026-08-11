UndefineClass('Drunk')
DefineClass.Drunk = {
	__parents = { "CharacterEffect" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",


	object_class = "CharacterEffect",
	Parameters = {
		PlaceObj('PresetParamNumber', {
			'Name', "melee_damage_flat",
			'Value', 20,
			'Tag', "<melee_damage_flat>",
		}),
		PlaceObj('PresetParamNumber', {
			'Name', "range_cth_mod",
			'Value', -15,
			'Tag', "<range_cth_mod>",
		}),
		PlaceObj('PresetParamNumber', {
			'Name', "hoursPerStack",
			'Value', 3,
			'Tag', "<hoursPerStack>",
		}),
		PlaceObj('PresetParamNumber', {
			'Name', "nextDecayTime",
			'Tag', "<nextDecayTime>",
		}),
	},
	Comment = "Nazdarovya intoxication: stacks ≤5; sat debt 3h/stack",
	unit_reactions = {
		PlaceObj('UnitReaction', {
			Event = "OnCalcChanceToHit",
			Handler = function (self, target, attacker, action, attack_target, weapon1, weapon2, data)
				if target ~= attacker or not action or action.ActionType ~= "Ranged Attack" then
					return
				end
				local stacks = self.stacks or 1
				local per = self:ResolveValue("range_cth_mod") or -15
				ApplyCthModifier_Add(self, data, stacks * per, T{776394275735, "Perk: <name>", name = self.DisplayName})
			end,
		}),
		PlaceObj('UnitReaction', {
			Event = "OnCalcDamageAndEffects",
			Handler = function (self, target, attacker, attack_target, action, weapon, attack_args, hit, data)
				if target ~= attacker or not action or action.ActionType ~= "Melee Attack" then
					return
				end
				local stacks = self.stacks or 1
				local flat = self:ResolveValue("melee_damage_flat") or 20
				local bonus = stacks * flat
				data.base_damage = (data.base_damage or 0) + bonus
				data.breakdown[#data.breakdown + 1] = { name = self.DisplayName, value = bonus }
			end,
		}),
		PlaceObj('UnitReaction', {
			Event = "OnNewHour",
			Handler = function (self, target)
				local next_decay = self:ResolveValue("nextDecayTime")
				local hours = self:ResolveValue("hoursPerStack") or 3
				if not next_decay or next_decay == 0 then
					self:SetParameter("nextDecayTime", Game.CampaignTime + hours * const.Scale.h)
					return
				end
				if Game.CampaignTime < next_decay then
					return
				end
				target:RemoveStatusEffect("Drunk", 1)
				local left = target:GetStatusEffect("Drunk")
				if left then
					left:SetParameter("nextDecayTime", Game.CampaignTime + hours * const.Scale.h)
				end
			end,
		}),
	},
	DisplayName = T(356009705485, --[[ModItemCharacterEffectCompositeDef Drunk DisplayName]] "Inebriated"),
	Description = T(890000000009889, --[[ModItemCharacterEffectCompositeDef Drunk Description]] "Опьянение (стаки ≤5): −15 точности дальнего боя и +20 урона в ближнем бою за стак. Спадает по 1 стаку каждые 3 часа."),
	AddEffectText = T(464514537198, --[[ModItemCharacterEffectCompositeDef Drunk AddEffectText]] "<DisplayName> is drunk"),
	RemoveEffectText = T(456783400197, --[[ModItemCharacterEffectCompositeDef Drunk RemoveEffectText]] "<DisplayName> is no longer drunk"),
	OnAdded = function (self, obj)
		obj:RemoveStatusEffect("Conscience_Sinful")
		obj:RemoveStatusEffect("Conscience_Guilty")
		local hours = self:ResolveValue("hoursPerStack") or 3
		local next_decay = self:ResolveValue("nextDecayTime")
		if not next_decay or next_decay == 0 then
			self:SetParameter("nextDecayTime", Game.CampaignTime + hours * const.Scale.h)
		end
	end,
	Icon = "UI/Hud/Status effects/drunk",
	max_stacks = 5,
	RemoveOnEndCombat = false,
	Shown = true,
	ShownSatelliteView = true,
	HasFloatingText = true,
}
