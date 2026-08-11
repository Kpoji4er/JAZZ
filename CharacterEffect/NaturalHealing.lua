UndefineClass('NaturalHealing')
DefineClass.NaturalHealing = {
	__parents = { "Perk" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",


	object_class = "Perk",
	Parameters = {
		PlaceObj('PresetParamNumber', {
			'Name', "hoursToProduce",
			'Value', 48,
			'Tag', "<hoursToProduce>",
		}),
		PlaceObj('PresetParamNumber', {
			'Name', "amountToProduce",
			'Value', 1,
			'Tag', "<amountToProduce>",
		}),
		PlaceObj('PresetParamNumber', {
			'Name', "nextProductionTime",
			'Tag', "<nextProductionTime>",
		}),
		PlaceObj('PresetParamPercent', {
			'Name', "sat_debt_speed_percent",
			'Value', 15,
			'Tag', "<sat_debt_speed_percent>",
		}),
		PlaceObj('PresetParamNumber', {
			'Name', "willRestoreMin",
			'Value', 20,
			'Tag', "<willRestoreMin>",
		}),
		PlaceObj('PresetParamNumber', {
			'Name', "willRestoreMax",
			'Value', 25,
			'Tag', "<willRestoreMax>",
		}),
	},
	unit_reactions = {
		PlaceObj('UnitReaction', {
			Event = "OnNewHour",
			Handler = function (self, target)
				if target.HireStatus ~= "Hired" then return end

				local next_production = self:ResolveValue("nextProductionTime")
				if not next_production or next_production == 0 then
					self:SetParameter("nextProductionTime", Game.CampaignTime + self:ResolveValue("hoursToProduce") * const.Scale.h)
					return
				end
				if Game.CampaignTime < next_production then return end
				local squad = target.Squad and gv_Squads[target.Squad]
				if squad and squad.water_travel then return end

				local amountToProduce = self:ResolveValue("amountToProduce")
				local item_name = amountToProduce > 1 and g_Classes["HerbalMedicine"].DisplayNamePlural or g_Classes["HerbalMedicine"].DisplayName
				self:SetParameter("nextProductionTime", Game.CampaignTime + self:ResolveValue("hoursToProduce") * const.Scale.h)

				local slots = { "Inventory" }
				local canPlaceError, amountLeft
				local amountToPlace = amountToProduce
				for _, slot in ipairs(slots) do
					canPlaceError, amountLeft = CanPlaceItemInInventory("HerbalMedicine", amountToPlace, target, slot)
					if not canPlaceError then
						PlaceItemInInventory("HerbalMedicine", amountToPlace, target, nil, nil, slot)
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
						PlaceItemInInventory("HerbalMedicine", amountToPlace, squad.CurrentSector)
					end
					text = text .. T(447763084369, " Some were placed in the sector stash.")
					CombatLog("important", text)
				else
					CombatLog("important", text)
				end
			end,
		}),
		PlaceObj('UnitReaction', {
			Event = "OnUnitBandaged",
			Handler = function (self, target, healer, patient, hp_restored)
				if target ~= healer then return end
				if type(Jazz_NaturalHealingRestoreWill) == "function" then
					Jazz_NaturalHealingRestoreWill(healer, patient)
				end
			end,
		}),
	},
	DisplayName = T(890000000009893, --[[ModItemCharacterEffectCompositeDef NaturalHealing DisplayName]] "Естественное исцеление"),
	Description = T(890000000009894, --[[ModItemCharacterEffectCompositeDef NaturalHealing Description]] "Каждые <hoursToProduce> ч — <amountToProduce>× Herbal Medicine. В отряде на сателлите: восстановление травм, ожогов и HP-долга на <sat_debt_speed_percent>% быстрее (инфекции не затрагивает). При перевязке: +<willRestoreMin>–<willRestoreMax> силы воли пациенту."),
	OnAdded = function (self, obj)
		self:SetParameter("nextProductionTime", Game.CampaignTime + self:ResolveValue("hoursToProduce") * const.Scale.h)
	end,
	Icon = "UI/Icons/Perks/NaturalHealing",
	Tier = "Personal",
}
