-- M.E.R.C. world-gated meet glue (JAZZ-UI-MERC-001).
-- Marks Jazz_Biff / Larry / Larry_Clean / Smiley as met → Available on MERC site (unless Hired).

g_JAZZ_MERC_WorldHooksInstalled = rawget(_G, "g_JAZZ_MERC_WorldHooksInstalled") or false

function JAZZ_MERC_MarkMet(id)
	if not id then
		return false
	end
	local isWorld = rawget(_G, "JAZZ_MERC_IsWorldId")
	if type(isWorld) == "function" and not isWorld(id) then
		-- Still allow explicit mark for roster ids; ignore unknown ids.
		local roster = rawget(_G, "JAZZ_MERC_IsRosterId")
		if type(roster) == "function" and not roster(id) then
			return false
		end
	end
	local ensure = rawget(_G, "JAZZ_MERC_EnsureAccount")
	local account = type(ensure) == "function" and ensure() or rawget(_G, "gv_JAZZ_MERC_Account")
	if not account then
		return false
	end
	account.met = account.met or {}
	account.met[id] = true
	-- Larry / Larry_Clean are paired personas — meeting one unlocks listing for both.
	if id == "Larry" then
		account.met.Larry_Clean = true
	elseif id == "Larry_Clean" then
		account.met.Larry = true
	end
	local unitData = rawget(_G, "gv_UnitData")
	local function lOpen(open_id)
		local ud = unitData and unitData[open_id]
		if not ud then
			return
		end
		if ud.Affiliation ~= "MERC" then
			ud.Affiliation = "MERC"
		end
		if ud.HireStatus == "NotMet" or ud.HireStatus == false or not ud.HireStatus then
			ud.HireStatus = "Available"
			ObjModified(ud)
		elseif ud.HireStatus ~= "Hired" and ud.HireStatus ~= "Dead" and ud.HireStatus ~= "MIA" and ud.HireStatus ~= "Retired" then
			if ud.HireStatus ~= "Available" then
				ud.HireStatus = "Available"
				ObjModified(ud)
			end
		end
	end
	lOpen(id)
	if id == "Larry" then
		lOpen("Larry_Clean")
	elseif id == "Larry_Clean" then
		lOpen("Larry")
	end
	return true
end

local function lMaybeMarkFromUnit(unit_or_id)
	local id = unit_or_id
	if type(unit_or_id) == "table" then
		id = unit_or_id.session_id or unit_or_id.class or unit_or_id.unitdatadef_id
	end
	if not id then
		return
	end
	local isWorld = rawget(_G, "JAZZ_MERC_IsWorldId")
	if type(isWorld) == "function" and isWorld(id) then
		JAZZ_MERC_MarkMet(id)
	end
end

function OnMsg.UnitJoinedPlayerSquad(squad_id, unit_id)
	lMaybeMarkFromUnit(unit_id)
end

function OnMsg.MercHired(merc_id, price, days, alreadyHired)
	lMaybeMarkFromUnit(merc_id)
end

function OnMsg.MercHireStatusChanged(unitData, oldStatus, newStatus)
	if not unitData then
		return
	end
	local id = unitData.session_id
	local isWorld = rawget(_G, "JAZZ_MERC_IsWorldId")
	if type(isWorld) ~= "function" or not isWorld(id) then
		return
	end
	if newStatus == "Hired" or newStatus == "Available" then
		JAZZ_MERC_MarkMet(id)
	end
end

-- Best-effort: some recruit flows create/update UnitData without the msgs above.
function OnMsg.SatelliteUnitDataCreated(unit_data)
	if unit_data and unit_data.HireStatus == "Hired" then
		lMaybeMarkFromUnit(unit_data)
	end
end

rawset(_G, "g_JAZZ_MERC_WorldHooksInstalled", true)
