UndefineClass('Zoophobic')
DefineClass.Zoophobic = {
	__parents = { "Perk" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",


	object_class = "Perk",
	unit_reactions = {
		PlaceObj('UnitReaction', {
			Event = "OnUnitAttack",
			Handler = function (self, target, attacker, action, attack_target, results, attack_args)
				if target == attack_target and attacker.species ~= "Human" and not results.miss and not target:HasStatusEffect("ZoophobiaChecked") then
					CombatLog("debug", T{Untranslated("<em>Zoophobic</em> proc on <unit>"), unit = target.Name})
					self:SetParameter("active", true)
				end
			end,
		}),
		PlaceObj('UnitReaction', {
			Event = "OnCalcPersonalMorale",
			Handler = function (self, target, value)
				if self:ResolveValue("active") then
					return value - 1
				end
			end,
		}),
		PlaceObj('UnitReaction', {
			Event = "OnCombatEnd",
			Handler = function (self, target)
				self:SetParameter("active", false)
			end,
		}),
		PlaceObj('UnitReaction', {
			Event = "OnSatelliteTick",
			Handler = function (self, target)
				self:SetParameter("active", false)
			end,
		}),
	},
	DisplayName = T(619689762390, "Зоофобия"),
	Description = T(467565005573, "<GameTerm('Morale')> снижается, если этого персонажа <em>атакует</em> <em>животное</em>."),
	Icon = "UI/Icons/Perks/Zoophobic",
	Tier = "Quirk",
}

