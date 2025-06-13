UndefineClass('HeavyWeaponsTraining')
DefineClass.HeavyWeaponsTraining = {
	__parents = { "Perk" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",


	object_class = "Perk",
	unit_reactions = {
		PlaceObj('UnitReaction', {
			Event = "OnCalcAPCost",
			Handler = function (self, target, current_ap, action, weapon, aim)
				if IsKindOfClasses(weapon, "HeavyWeapon", "MachineGun") then
					local reduction = self:ResolveValue("ap_cost_reduction") * const.Scale.AP
					local minCost = self:ResolveValue("min_ap_cost") * const.Scale.AP
					return Max(minCost, current_ap - reduction)
				end
			end,
		}),
	},
	DisplayName = T(575851829180, --[[ModItemCharacterEffectCompositeDef HeavyWeaponsTraining DisplayName]] "Heavy Weapons"),
	Description = T(662768584689, --[[ModItemCharacterEffectCompositeDef HeavyWeaponsTraining Description]] "Уменьшен расход <em>ОД</em> на атаки из <em>тяжелого вооружения</em> и <em>пулеметов</em> и приведение его в <GameTerm('Setup')>.\nПервые 2 выстрела из пулеметов производятся без отдачи."),
	Icon = "UI/Icons/Perks/HeavyWeaponsTraining",
	Tier = "Specialization",
}

