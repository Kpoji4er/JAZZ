-- Player-facing recruit stock helpers for militia (roadmap 7c / JAZZ-STRATEGY-011).
-- Accrual lives in Guardpost_Patrols region_state.poi_recruits; Operation consume hook is morning Q.

JAZZ_MilitiaRecruitsPerTraining = 4

local function lRegionStateForSector(sector_id)
	local region = GetRegionForSector and GetRegionForSector(sector_id)
	local region_id = region and (region.id or region.Id)
	local root = gv_JAZZ_LegionAI
	if type(root) ~= "table" or not region_id then
		return false, false
	end
	return root.regions and root.regions[region_id], region
end

function JAZZ_GetSectorRecruits(sector_id)
	local region_state = lRegionStateForSector(sector_id)
	if not region_state then
		return 0
	end
	return region_state.poi_recruits and region_state.poi_recruits[sector_id] or 0
end

--- Consume up to `amount` recruits from sector stock. Returns true if fully paid.
function JAZZ_TryConsumeSectorRecruits(sector_id, amount)
	amount = math.floor(tonumber(amount) or 0)
	if amount <= 0 then
		return true
	end
	local region_state = lRegionStateForSector(sector_id)
	if not region_state then
		return false
	end
	region_state.poi_recruits = region_state.poi_recruits or {}
	local have = region_state.poi_recruits[sector_id] or 0
	if have < amount then
		return false
	end
	region_state.poi_recruits[sector_id] = have - amount
	return true
end

-- Optional soft gate: if MilitiaTraining operation exists, require recruits to start.
-- Exact vanilla ID/confirmation is morning Q; wrap only when present.
local function lInstallMilitiaRecruitGate()
	if not SectorOperations then
		return
	end
	local op = SectorOperations.MilitiaTraining or SectorOperations.TrainMilitia
	if not op or op.jazz_recruit_gate then
		return
	end
	op.jazz_recruit_gate = true
	local base_can = op.CanPerform
	if type(base_can) == "function" then
		op.CanPerform = function(self, sector, ...)
			local ok, reason = base_can(self, sector, ...)
			if not ok then
				return ok, reason
			end
			local sector_id = type(sector) == "table" and (sector.Id or sector.id) or sector
			local need = JAZZ_MilitiaRecruitsPerTraining or 4
			if JAZZ_GetSectorRecruits(sector_id) < need then
				return false, T(890000000001640, "Not enough local recruits")
			end
			return true
		end
	end
	local base_complete = op.Complete or op.OnComplete
	if type(base_complete) == "function" then
		local key = op.Complete and "Complete" or "OnComplete"
		op[key] = function(self, sector, ...)
			local sector_id = type(sector) == "table" and (sector.Id or sector.id) or sector
			JAZZ_TryConsumeSectorRecruits(sector_id, JAZZ_MilitiaRecruitsPerTraining or 4)
			return base_complete(self, sector, ...)
		end
	end
end

function OnMsg.ModsReloaded()
	lInstallMilitiaRecruitGate()
end

function OnMsg.LoadGame()
	lInstallMilitiaRecruitGate()
end
