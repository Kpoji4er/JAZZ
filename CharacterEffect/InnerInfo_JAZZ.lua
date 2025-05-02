UndefineClass('InnerInfo_JAZZ')
DefineClass.InnerInfo_JAZZ = {
	__parents = { "Perk" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",


	comment = "Фаза",
	object_class = "Perk",
	unit_reactions = {
		PlaceObj('UnitReaction', {
			Event = "OnCheckIntelVisible",
			Handler = function (self, target)
				return gv_CurrentSectorId and gv_Sectors[gv_CurrentSectorId].intel_discovered
			end,
		}),
		PlaceObj('UnitReaction', {
			Event = "OnHackIntelDsicovered",
			Handler = function (self, target)
				local discoveredFor = DiscoverIntelForRandomSector(2, "no notification")
				if discoveredFor then
					CombatLog("important", T{312197955233, "Livewire used her custom PDA to discover additional Intel for <em><SectorName(sectorId)></em>", sectorId = discoveredFor})
				end
			end,
		}),
	},
	DisplayName = T(380316218017, --[[ModItemCharacterEffectCompositeDef InnerInfo_JAZZ DisplayName]] "Секретные данные"),
	Description = T(391831963748, --[[ModItemCharacterEffectCompositeDef InnerInfo_JAZZ Description]] "Получает больше разведданных при хакинге\nОткрывает операцию по заработку денег в городском секторе (Пока недоступно)"),
	Icon = "UI/Icons/Perks/InnerInfo",
	Tier = "Personal",
}

