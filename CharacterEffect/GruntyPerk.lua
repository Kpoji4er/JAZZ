UndefineClass('GruntyPerk')
DefineClass.GruntyPerk = {
	__parents = { "Perk" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",


	comment = "Хряпти",
	object_class = "Perk",
	unit_reactions = {
		PlaceObj('UnitReaction', {
			Event = "OnCombatStarting",
			Handler = function (self, target, load_game)
				if load_game then return end
				
				local enemy = target:GetClosestEnemy()
				if enemy then
					local weapon = target:GetActiveWeapons()
					if IsKindOf(weapon, "Firearm") and not IsKindOf(weapon, "HeavyWeapon") then
						local action = target:GetDefaultAttackAction("ranged")
						local args = {target = enemy, gruntyPerk = true}
						LockCameraMovement("grunty perk")
						StartCombatAction(action.id, target, 0, args)
					end
				end
			end,
		}),
	},
	DisplayName = T(562334332352, --[[ModItemCharacterEffectCompositeDef GruntyPerk DisplayName]] "Юберрашунг"),
	Description = T(742416202176, --[[ModItemCharacterEffectCompositeDef GruntyPerk Description]] "<em>Атакует</em> <em>ближайшего</em> противника из огнестрельного оружия <em>в начале боя</em> (если есть возможность).\n\nНеприменимо к тяжелому оружию."),
	Icon = "UI/Icons/Perks/GruntyPerk",
	Tier = "Personal",
}

