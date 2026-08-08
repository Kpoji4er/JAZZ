UndefineClass('InnerInfo_JAZZ')
DefineClass.InnerInfo_JAZZ = {
	__parents = { "Perk" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",


	object_class = "Perk",
	unit_reactions = {
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
	DisplayName = T(890000000000446, --[[ModItemCharacterEffectCompositeDef InnerInfo_JAZZ DisplayName]] "Секретные данные"),
	Description = T(391831963748, --[[ModItemCharacterEffectCompositeDef InnerInfo_JAZZ Description]] "Получает больше разведданных при хакинге. Городская операция заработка ($2000 / 2 дня) — soft-cut до ECON-001."),
	Icon = "UI/Icons/Perks/InnerInfo",
	Tier = "Personal",
}
