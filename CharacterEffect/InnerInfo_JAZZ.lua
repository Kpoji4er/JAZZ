UndefineClass('InnerInfo_JAZZ')
DefineClass.InnerInfo_JAZZ = {
	__parents = { "Perk" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",


	comment = "Фаза",
	object_class = "Perk",
	unit_reactions = {
		PlaceObj('UnitReaction', {
			Event = "OnUnitEnterMapVisual",
			Handler = function (self, target)
				local sector = gv_Sectors[gv_CurrentSectorId]
				if target.HireStatus ~= "Hired" or not sector or not sector.intel_discovered then
					return
				end

				CreateGameTimeThread(function()
					local playVr
					while GetInGameInterfaceMode() == "IModeDeployment" do
						Sleep(20)
					end
					for _, unit in ipairs(g_Units) do
						if unit:IsOnEnemySide(target) then
							unit:RevealTo(target.team)
							unit.innerInfoRevealed = true
							playVr = true
							break
						end
					end
					if playVr then
						Sleep(2000)
						PlayVoiceResponse(target, "PersonalPerkSubtitled")
					end
				end)
			end,
		}),
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
	DisplayName = T(890000000000446, --[[ModItemCharacterEffectCompositeDef InnerInfo_JAZZ DisplayName]] "Секретные данные"),
	Description = T(391831963748, --[[ModItemCharacterEffectCompositeDef InnerInfo_JAZZ Description]] "Получает больше разведданных при хакинге. Городская операция заработка ($2000 / 2 дня) — soft-cut до ECON-001."),
	Icon = "UI/Icons/Perks/InnerInfo",
	Tier = "Personal",
}
