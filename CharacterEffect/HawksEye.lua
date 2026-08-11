UndefineClass('HawksEye')
DefineClass.HawksEye = {
	__parents = { "Perk" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",


	object_class = "Perk",
	Parameters = {
		PlaceObj('PresetParamNumber', {
			'Name', "pindownCostOverwrite",
			'Value', 1,
			'Tag', "<pindownCostOverwrite>",
		}),
		PlaceObj('PresetParamNumber', {
			'Name', "overwatchCostOverwrite",
			'Value', 1,
			'Tag', "<overwatchCostOverwrite>",
		}),
	},
	Comment = "Scope: OW/PinDown 1 AP with snipers; biscuits; sniper suppress ×2",
	unit_reactions = {
		PlaceObj('UnitReaction', {
			Event = "OnMercHired",
			Handler = function (self, target, price, days, alreadyHired)
				if days > 0 then
					local canPlaceError = CanPlaceItemInInventory("Cookie", days, target)
					if canPlaceError then
						CombatLog("important", T(667077082306, "Scope has baked some biscuits. Unfortunately the inventory is full. "))
						return
					end
					CombatLog("important", T(754424382903, "Scope has baked some biscuits"))
					PlaceItemInInventory("Cookie", days, target)
				end
			end,
		}),
	},
	DisplayName = T(890000000009869, --[[ModItemCharacterEffectCompositeDef HawksEye DisplayName]] "Ястребиный глаз"),
	Description = T(890000000009870, --[[ModItemCharacterEffectCompositeDef HawksEye Description]] "Со снайперской винтовкой: Overwatch за <overwatchCostOverwrite> ОД (остальные ОД остаются). Pin Down / Focus Fire — мин. <pindownCostOverwrite> ОД. Снайперские выстрелы дают ×2 подавления. При найме печёт печенье (перезарядка сигнатур)."),
	Icon = "UI/Icons/Perks/HawksEye",
	Tier = "Personal",
}
