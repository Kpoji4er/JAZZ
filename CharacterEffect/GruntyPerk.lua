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
	DisplayName = T(562334332352, --[[ModItemCharacterEffectCompositeDef GruntyPerk DisplayName]] "Überraschung"),
	Description = T(742416202176, --[[ModItemCharacterEffectCompositeDef GruntyPerk Description]] "<em>Attacks</em> the <em>closest</em> enemy with a firearm when <em>combat starts</em>, if possible.\nCan't be used with Heavy Weapons."),
	Icon = "UI/Icons/Perks/GruntyPerk",
	Tier = "Personal",
}

