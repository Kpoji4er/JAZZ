local RegenerateLegionLootVar
function RegenerateLegionLoot() RegenerateLegionLootVar = true end

function OnMsg.OpenSatelliteView()
	if RegenerateLegionLootVar then
		_RegenerateLegionLoot()
	end
end

local function IsLegionUnitData(unitdata)
	return unitdata
		and not unitdata.IsMercenary
		and not unitdata:IsDead()
		and unitdata.Affiliation == "Legion"
end

-- Legacy sector-enemy path (kept for reference / alternate callers). Legion-only.
function ___RegenerateLegionLoot()
	for _, sector in sorted_pairs(gv_Sectors) do
		local squads = sector.enemy_squads
		for _, squad in ipairs(squads or empty_table) do
			for _, unit_id in ipairs(squad.units or empty_table) do
				local unitdata = gv_UnitData[unit_id]
				if IsLegionUnitData(unitdata) and not unitdata:IsNPC() then
					unitdata:ForEachItem(function(item, slot_name)
						unitdata:RemoveItem(slot_name, item)
					end)
					unitdata:CreateStartingEquipment(unitdata.randomization_seed)
					unitdata.innerInfoRevealed = false
				end
			end
		end
	end
	RegenerateLegionLootVar = false
end

-- JAZZ-UNITS-004: only Legion. Pre-004 wiped every gv_Squads unit (incl. player mercs).
function _RegenerateLegionLoot()
	for _, squad in ipairs(gv_Squads) do
		for _, unit_id in ipairs(squad.units or empty_table) do
			local unitdata = gv_UnitData[unit_id]
			if IsLegionUnitData(unitdata) then
				local unit = g_Units[unit_id]
				if unit then
					unit:ForEachItem(function(item, slot)
						unit:RemoveItem(slot, item)
					end)
					unit:CreateStartingEquipment(unitdata.randomization_seed)
				end
				unitdata:ForEachItem(function(item, slot_name)
					unitdata:RemoveItem(slot_name, item)
				end)
				unitdata:CreateStartingEquipment(unitdata.randomization_seed)
			end
		end
	end
	RegenerateLegionLootVar = false
end
