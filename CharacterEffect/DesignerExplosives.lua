UndefineClass('DesignerExplosives')
DefineClass.DesignerExplosives = {
	__parents = { "Perk" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",


	object_class = "Perk",
	Parameters = {
		PlaceObj('PresetParamNumber', {
			'Name', "hoursToProduce",
			'Value', 168,
			'Tag', "<hoursToProduce>",
		}),
		PlaceObj('PresetParamNumber', {
			'Name', "amountToProduce",
			'Value', 2,
			'Tag', "<amountToProduce>",
		}),
		PlaceObj('PresetParamNumber', {
			'Name', "nextProductionTime",
			'Tag', "<nextProductionTime>",
		}),
		PlaceObj('PresetParamPercent', {
			'Name', "craft_discount",
			'Value', 30,
			'Tag', "<craft_discount>",
		}),
	},
	unit_reactions = {
		PlaceObj('UnitReaction', {
			Event = "OnNewHour",
			Handler = function (self, target)
				if target.HireStatus ~= "Hired" then return end

				local next_production = self:ResolveValue("nextProductionTime")
				-- Saves that loaded the broken CE rewrite may lack nextProductionTime.
				if not next_production or next_production == 0 then
					self:SetParameter("nextProductionTime", Game.CampaignTime + self:ResolveValue("hoursToProduce") * const.Scale.h)
					return
				end
				if Game.CampaignTime < next_production or gv_Squads[target.Squad].water_travel then return end

				local amountToProduce = self:ResolveValue("amountToProduce")
				local item_name = amountToProduce > 1 and g_Classes["ShapedCharge"].DisplayNamePlural or g_Classes["ShapedCharge"].DisplayName
				self:SetParameter("nextProductionTime", Game.CampaignTime + self:ResolveValue("hoursToProduce") * const.Scale.h)

				local slots = { "Handheld A", "Handheld B", "Inventory" }
				local canPlaceError, amountLeft
				local amountToPlace = amountToProduce
				for _, slot in ipairs(slots) do
					canPlaceError, amountLeft = CanPlaceItemInInventory("ShapedCharge", amountToPlace, target, slot)
					if not canPlaceError then
						PlaceItemInInventory("ShapedCharge", amountToPlace, target, nil, nil, slot)
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
					PlaceItemInInventory("ShapedCharge", amountToPlace, gv_Squads[target.Squad].CurrentSector)
					text = text .. T(447763084369, " Some were placed in the sector stash.")
					CombatLog("important", text)
				else
					CombatLog("important", text)
				end
			end,
		}),
	},
	DisplayName = T(890000000009885, --[[ModItemCharacterEffectCompositeDef DesignerExplosives DisplayName]] "Конструктор взрывчатки"),
	Description = T(890000000009886, --[[ModItemCharacterEffectCompositeDef DesignerExplosives Description]] "Каждые <hoursToProduce> ч производит <amountToProduce> кумулятивных заряда. Может крафтить их через «Изготовление взрывчатки». Крафт патронов и взрывчатки: −<craft_discount>% Parts."),
	OnAdded = function (self, obj)
		self:SetParameter("nextProductionTime", Game.CampaignTime + self:ResolveValue("hoursToProduce") * const.Scale.h)
	end,
	Icon = "UI/Icons/Perks/DesignerExplosives",
	Tier = "Personal",
}
