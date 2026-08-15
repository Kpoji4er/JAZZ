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
		PlaceObj('PresetParamNumber', {
			'Name', "hoursToProduce",
			'Value', 96,
			'Tag', "<hoursToProduce>",
		}),
		PlaceObj('PresetParamNumber', {
			'Name', "amountToProduce",
			'Value', 7,
			'Tag', "<amountToProduce>",
		}),
		PlaceObj('PresetParamNumber', {
			'Name', "nextProductionTime",
			'Tag', "<nextProductionTime>",
		}),
	},
	Comment = "Scope: sniper OW 1 AP keep leftover; PinDown min 1; sniper suppress ×2; biscuits 96h×7 + hire",
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
		PlaceObj('UnitReaction', {
			Event = "OnNewHour",
			Handler = function (self, target)
				if target.HireStatus ~= "Hired" then return end

				local next_production = self:ResolveValue("nextProductionTime")
				if not next_production or next_production == 0 then
					self:SetParameter("nextProductionTime", Game.CampaignTime + self:ResolveValue("hoursToProduce") * const.Scale.h)
					return
				end
				local squad = target.Squad and gv_Squads[target.Squad]
				if Game.CampaignTime < next_production or (squad and squad.water_travel) then return end

				local amountToProduce = self:ResolveValue("amountToProduce")
				local cookie = g_Classes["Cookie"]
				local item_name = cookie and (amountToProduce > 1 and cookie.DisplayNamePlural or cookie.DisplayName) or Untranslated("Cookie")
				self:SetParameter("nextProductionTime", Game.CampaignTime + self:ResolveValue("hoursToProduce") * const.Scale.h)

				local slots = { "Handheld A", "Handheld B", "Inventory" }
				local canPlaceError, amountLeft
				local amountToPlace = amountToProduce
				for _, slot in ipairs(slots) do
					canPlaceError, amountLeft = CanPlaceItemInInventory("Cookie", amountToPlace, target, slot)
					if not canPlaceError then
						PlaceItemInInventory("Cookie", amountToPlace, target, nil, nil, slot)
						if not amountLeft then
							break
						else
							amountToPlace = amountLeft
						end
					end
				end

				local text = T{318623454402, "<merc> produced <amount> <item_name>.", merc = target.Nick, amount = amountToProduce, item_name = item_name}
				if canPlaceError or (amountLeft and amountLeft > 0) then
					amountToPlace = amountToPlace or amountToProduce
					if squad and squad.CurrentSector then
						PlaceItemInInventory("Cookie", amountToPlace, squad.CurrentSector)
						text = text .. T(447763084369, " Some were placed in the sector stash.")
					end
					CombatLog("important", text)
				else
					CombatLog("important", text)
				end
			end,
		}),
	},
	DisplayName = T(890000000009869, --[[ModItemCharacterEffectCompositeDef HawksEye DisplayName]] "Ястребиный глаз"),
	Description = T(890000000009870, --[[ModItemCharacterEffectCompositeDef HawksEye Description]] "Со снайперской винтовкой: Overwatch за <overwatchCostOverwrite> ОД (остальные ОД остаются). Pin Down / Focus Fire — мин. <pindownCostOverwrite> ОД. Снайперские выстрелы дают ×2 подавления. Каждые <hoursToProduce> ч — <amountToProduce>× Печенье. При найме тоже печёт печенье (перезарядка сигнатур)."),
	OnAdded = function (self, obj)
		self:SetParameter("nextProductionTime", Game.CampaignTime + self:ResolveValue("hoursToProduce") * const.Scale.h)
	end,
	Icon = "UI/Icons/Perks/HawksEye",
	Tier = "Personal",
}
