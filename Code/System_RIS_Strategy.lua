-- R.I.S. Major Strategy observer (JAZZ-UI-RIS-002).
-- Reads Legion AI campaign state only; all persistent writes stay in gv_JAZZ_RIS.

local RIS_NETWORK_MATERIAL = "strategy_network"
local RIS_STRATEGY_ORDER = {
	"strategy_network",
	"strategy_roads",
	"strategy_villages",
	"strategy_eyes",
	"strategy_answer",
	"strategy_cargo",
	"strategy_wounded",
	"strategy_red",
	"strategy_sleep",
}
local RIS_STRATEGY_EMAILS = {
	strategy_network = "RIS_MajorStrategy_Network",
	strategy_roads = "RIS_MajorStrategy_Roads",
	strategy_villages = "RIS_MajorStrategy_Villages",
	strategy_eyes = "RIS_MajorStrategy_Recon",
	strategy_answer = "RIS_MajorStrategy_Response",
	strategy_cargo = "RIS_MajorStrategy_Cargo",
	strategy_wounded = "RIS_MajorStrategy_Recovery",
	strategy_red = "RIS_MajorStrategy_Retribution",
	strategy_sleep = "RIS_MajorStrategy_Awakening",
}
local RIS_STRATEGY_INDEX = {}
local RIS_STRATEGY_MATERIALS = {}
for index, material_id in ipairs(RIS_STRATEGY_ORDER) do
	RIS_STRATEGY_INDEX[material_id] = index
	RIS_STRATEGY_MATERIALS[RIS_STRATEGY_EMAILS[material_id]] = material_id
end

local RIS_ROAD_ROLES = { patrol = true, mobile = true }
local RIS_VILLAGE_ROLES = { tax = true, recruiter = true }
local RIS_ANSWER_ROLES = { qrf = true, reinforce = true }
local RIS_CARGO_ROLES = { supply = true, shipment = true, manpower = true }
local RIS_VILLAGE_TASKS = {
	tax = true,
	tax_return = true,
	recruiter = true,
	recruiter_return = true,
}
local RIS_ANSWER_TASKS = { retake = true, qrf = true, reinforce = true }
local RIS_CARGO_TASKS = {
	supply = true,
	shipment = true,
	manpower = true,
	manpower_outbound = true,
	logistics = true,
}

local function lNow()
	local game = rawget(_G, "Game")
	return game and game.CampaignTime or 0
end

local function lState()
	local migrate = rawget(_G, "JAZZ_RIS_MigrateState")
	if type(migrate) == "function" then
		return migrate()
	end
	local st = rawget(_G, "gv_JAZZ_RIS")
	return type(st) == "table" and st or false
end

local function lKeyLess(a, b)
	local type_a, type_b = type(a), type(b)
	if type_a == type_b and (type_a == "number" or type_a == "string") then
		return a < b
	end
	local text_a, text_b = tostring(a), tostring(b)
	if text_a == text_b then
		return type_a < type_b
	end
	return text_a < text_b
end

local function lSortedKeys(rows)
	local keys = {}
	if type(rows) == "table" then
		for key in pairs(rows) do
			keys[#keys + 1] = key
		end
	end
	table.sort(keys, lKeyLess)
	return keys
end

local function lIsPlayerSide(side)
	return side == "player1" or side == "player2"
end

local function lSquadCurrentSector(squad_id)
	local squads = rawget(_G, "gv_Squads")
	local squad = type(squads) == "table" and squads[squad_id]
	return squad and squad.CurrentSector or false
end

local function lIsPlayerSector(sector_id)
	local sectors = rawget(_G, "gv_Sectors")
	local sector = type(sectors) == "table" and sector_id and sectors[sector_id]
	return sector and lIsPlayerSide(sector.Side) or false
end

local function lSquadObject(squad_id)
	local squads = rawget(_G, "gv_Squads")
	return type(squads) == "table" and squads[squad_id] or false
end

local function lIsSquadTravelling(squad)
	if type(squad) ~= "table" then
		return false
	end
	local is_travelling = rawget(_G, "IsSquadTravelling")
	if type(is_travelling) == "function" then
		local ok, travelling = pcall(is_travelling, squad)
		if ok then
			return not not travelling
		end
	end
	return type(squad.route) == "table" and next(squad.route) ~= nil
end

local function lIsSectorRevealed(sector_id)
	local sectors = rawget(_G, "gv_Sectors")
	local sector = type(sectors) == "table" and sector_id and sectors[sector_id]
	if not sector then
		return false
	end
	local is_revealed = rawget(_G, "IsSectorRevealed")
	if type(is_revealed) == "function" then
		local ok, revealed = pcall(is_revealed, sector)
		if ok then
			return not not revealed
		end
	end
	local revealed = rawget(_G, "g_RevealedSectors")
	return type(revealed) == "table" and revealed[sector_id] and sector.discovered or false
end

--- Match information the campaign map can expose: a moving enemy column, a
--- revealed sector, or direct presence in player-held ground. Hidden garrison
--- state must not unlock an intelligence paper by itself.
local function lIsSquadObservable(squad_id)
	local squad = lSquadObject(squad_id)
	if not squad then
		return false
	end
	if squad.always_visible or squad.arrival_squad or lIsSquadTravelling(squad) then
		return true
	end
	local sector_id = squad.CurrentSector
	return lIsPlayerSector(sector_id) or lIsSectorRevealed(sector_id)
end

local function lHasConfirmedContact(st)
	for _, value in pairs(type(st.met_types) == "table" and st.met_types or {}) do
		if value then
			return true
		end
	end
	for _, value in pairs(type(st.kills) == "table" and st.kills or {}) do
		if (tonumber(value) or 0) > 0 then
			return true
		end
	end
	return false
end

local function lHasReceivedSupplyBrief(st)
	local get_received = rawget(_G, "GetReceivedEmails")
	if type(get_received) == "function" then
		local ok, received = pcall(get_received)
		if ok and type(received) == "table" then
			for _, email in ipairs(received) do
				if type(email) == "table"
					and type(email.id) == "string"
					and string.match(email.id, "^RIS_LegionBrief_")
				then
					return true
				end
			end
			-- A readable inbox is authoritative. Old enqueue-time state must not
			-- reveal Network before a brief actually reaches the player.
			return false
		end
	end
	return (tonumber(st.last_mailed_tier) or 0) > 0
end

local function lWelcomeRead(st)
	local is_read = rawget(_G, "JAZZ_RIS_IsWelcomeRead")
	if type(is_read) == "function" then
		return not not is_read()
	end
	return not not st.welcome_read
end

local function lRecordObservation(material_id, observed_at)
	local st = rawget(_G, "gv_JAZZ_RIS")
	local previous = type(st) == "table"
		and type(st.strategy_observed) == "table"
		and tonumber(st.strategy_observed[material_id])
	if previous and previous <= observed_at then
		return false
	end
	return JAZZ_RIS_RecordStrategyObservation(material_id, observed_at)
end

local function lObserveNetwork(st, now)
	if lWelcomeRead(st) and (lHasConfirmedContact(st) or lHasReceivedSupplyBrief(st)) then
		return lRecordObservation(RIS_NETWORK_MATERIAL, now)
	end
	return false
end

local function lIsNonGenericReport(report, must_be_delivered)
	if type(report) ~= "table" or report.generic then
		return false
	end
	if must_be_delivered and not report.delivered then
		return false
	end
	return report.id ~= nil
		or report.target_sector ~= nil
		or report.target ~= nil
		or report.observed_at ~= nil
end

local function lObserveRowSignals(squad_id, row, now)
	if type(row) ~= "table" then
		return false
	end
	local changed = false
	local role = row.role
	local task = type(row.task) == "table" and row.task or false
	local task_type = task and task.task_type
	local current_sector = lSquadCurrentSector(squad_id)
	local observable = lIsSquadObservable(squad_id)

	-- A future patrol target is not observable. The managed squad must already
	-- stand in a player-held sector (including an immediate task arrival).
	if lIsPlayerSector(current_sector)
		and (RIS_ROAD_ROLES[role] or task_type == "patrol" or task_type == "patrol_dwell")
	then
		changed = lRecordObservation("strategy_roads", now) or changed
	end
	if observable and (RIS_VILLAGE_ROLES[role] or RIS_VILLAGE_TASKS[task_type]) then
		changed = lRecordObservation("strategy_villages", now) or changed
	end
	if observable
		and task_type == "return_with_intel"
		and lIsNonGenericReport(task.report, false)
	then
		changed = lRecordObservation("strategy_eyes", now) or changed
	end
	if observable and (RIS_ANSWER_ROLES[role] or RIS_ANSWER_TASKS[task_type]) then
		changed = lRecordObservation("strategy_answer", now) or changed
	end
	if observable and (RIS_CARGO_ROLES[role] or RIS_CARGO_TASKS[task_type]) then
		changed = lRecordObservation("strategy_cargo", now) or changed
	end
	if observable and (task_type == "return_wounded" or row.state == "wounded") then
		changed = lRecordObservation("strategy_wounded", now) or changed
	end
	if observable and (role == "major" or task_type == "major_response") then
		changed = lRecordObservation("strategy_red", now) or changed
	end
	return changed
end

local function lRegionPreset(region_id)
	local regions = rawget(_G, "Regions")
	if type(regions) ~= "table" or region_id == nil then
		return false
	end
	if regions[region_id] then
		return regions[region_id]
	end
	for _, key in ipairs(lSortedKeys(regions)) do
		local region = regions[key]
		if type(region) == "table" and (region.id == region_id or region.Id == region_id) then
			return region
		end
	end
	return false
end

local function lRegionObservableActivity(root, region_id)
	local activity = {}
	for _, squad_id in ipairs(lSortedKeys(root.squads)) do
		local row = root.squads[squad_id]
		if type(row) == "table"
			and row.region_id == region_id
			and row.state ~= "retired"
			and lIsSquadObservable(squad_id)
		then
			local squad = lSquadObject(squad_id)
			activity[tostring(squad_id)] = table.concat({
				tostring(squad and squad.CurrentSector or ""),
				lIsSquadTravelling(squad) and "moving" or "stationary",
			}, "|")
		end
	end
	return activity
end

local function lHasNewObservableActivity(previous, current)
	for squad_id, signature in pairs(current) do
		if previous[squad_id] ~= signature then
			return true
		end
	end
	return false
end

local function lPollAwakening(st, root, now)
	if type(root.outposts) ~= "table" then
		return false, false
	end
	local current_by_region = {}
	local region_ids = {}
	for _, outpost_id in ipairs(lSortedKeys(root.outposts)) do
		local outpost = root.outposts[outpost_id]
		local region_id = type(outpost) == "table" and outpost.region_id
		local preset = lRegionPreset(region_id)
		if preset and (tonumber(preset.LateAwakenMinTier) or 0) > 0 then
			local key = tostring(region_id)
			region_ids[key] = region_id
			current_by_region[key] = current_by_region[key] or not not outpost.major_delivery_done
		end
	end

	local changed = false
	local baseline = st.strategy_major_delivery_baseline
	for _, region_key in ipairs(lSortedKeys(current_by_region)) do
		local current = current_by_region[region_key]
		local previous = baseline[region_key]
		if not current then
			if previous == nil then
				baseline[region_key] = false
			end
		elseif previous ~= true then
			local activity = lRegionObservableActivity(root, region_ids[region_key])
			if type(previous) ~= "table" or not previous.delivery_seen then
				-- The delivery itself is hidden. Snapshot everything already visible
				-- and require a later appearance or movement before revealing it.
				baseline[region_key] = {
					delivery_seen = true,
					activity = activity,
				}
			elseif lHasNewObservableActivity(previous.activity or {}, activity) then
				changed = lRecordObservation("strategy_sleep", now) or changed
				baseline[region_key] = true
			else
				previous.activity = activity
			end
		end
	end
	return changed, true
end

local function lIsStrategyRow(row)
	if type(row) ~= "table" then
		return false
	end
	if RIS_STRATEGY_INDEX[row.material_id] or RIS_STRATEGY_MATERIALS[row.email_id] then
		return true
	end
	if type(row.key) == "string" then
		local material_id = string.match(row.key, "^strategy_(strategy_.+)$")
		return not not RIS_STRATEGY_INDEX[material_id]
	end
	return false
end

local function lNextObservedMaterial(st)
	if not st.strategy_delivered[RIS_NETWORK_MATERIAL] then
		return tonumber(st.strategy_observed[RIS_NETWORK_MATERIAL])
			and RIS_NETWORK_MATERIAL
			or false
	end

	local selected, selected_at, selected_index
	for index = 2, #RIS_STRATEGY_ORDER do
		local material_id = RIS_STRATEGY_ORDER[index]
		local observed_at = tonumber(st.strategy_observed[material_id])
		if observed_at and not st.strategy_delivered[material_id] then
			if not selected
				or observed_at < selected_at
				or (observed_at == selected_at and index < selected_index)
			then
				selected = material_id
				selected_at = observed_at
				selected_index = index
			end
		end
	end
	return selected or false
end

local function lPruneStrategyRows(st, keep_key)
	local kept = false
	local changed = false
	for index = #st.mail_queue, 1, -1 do
		local row = st.mail_queue[index]
		if lIsStrategyRow(row) then
			if keep_key and row.key == keep_key and not kept then
				kept = row
			else
				table.remove(st.mail_queue, index)
				changed = true
			end
		end
	end
	return kept, changed
end

--- Record a language-neutral material id at its earliest observed CampaignTime.
function JAZZ_RIS_RecordStrategyObservation(material_id, observed_at)
	if not RIS_STRATEGY_INDEX[material_id] then
		return false
	end
	local st = lState()
	if not st then
		return false
	end
	observed_at = tonumber(observed_at)
	if not observed_at then
		observed_at = lNow()
	end
	local previous = tonumber(st.strategy_observed[material_id])
	if previous and previous <= observed_at then
		return false
	end
	st.strategy_observed[material_id] = observed_at
	local modified = rawget(_G, "ObjModified")
	if type(modified) == "function" then
		modified("jazz_ris")
	end
	return true
end

--- Keep exactly one pending strategy row, with Network forced ahead of all others.
function JAZZ_RIS_UpdateStrategyQueue(is_load_catchup)
	local st = lState()
	if not st then
		return false
	end
	local material_id = lNextObservedMaterial(st)
	local key = material_id and ("strategy_" .. material_id) or false
	local existing, changed = lPruneStrategyRows(st, key)
	if not material_id then
		return changed
	end

	local observed_at = tonumber(st.strategy_observed[material_id]) or lNow()
	local ready_at = math.max(observed_at, tonumber(st.next_strategy_at) or 0)
	local email_id = RIS_STRATEGY_EMAILS[material_id]
	if existing then
		existing.key = key
		existing.kind = "strategy"
		existing.material_id = material_id
		existing.email_id = email_id
		existing.ready_at = ready_at
		existing.context = nil
		existing.title = nil
		existing.body = nil
		return changed
	end

	local enqueue = rawget(_G, "JAZZ_RIS_EnqueueMail")
	if type(enqueue) ~= "function" then
		return changed
	end
	return enqueue({
		key = key,
		kind = "strategy",
		material_id = material_id,
		email_id = email_id,
		ready_at = ready_at,
	}) or changed
end

--- Deterministically scan synced Legion AI state without mutating it.
function JAZZ_RIS_PollStrategySignals(is_load_catchup)
	local st = lState()
	if not st then
		return false
	end
	local now = lNow()
	local changed = false
	local root = rawget(_G, "gv_JAZZ_LegionAI")
	local scanned_awakening = false
	if type(root) == "table" then
		for _, squad_id in ipairs(lSortedKeys(root.squads)) do
			changed = lObserveRowSignals(squad_id, root.squads[squad_id], now) or changed
		end
		local awakening_changed
		awakening_changed, scanned_awakening = lPollAwakening(
			st,
			root,
			now
		)
		changed = awakening_changed or changed
	end
	changed = lObserveNetwork(st, now) or changed
	if is_load_catchup and scanned_awakening then
		st.strategy_catchup_done = true
	end
	return JAZZ_RIS_UpdateStrategyQueue(is_load_catchup) or changed
end

--- Detached copy for DAP inspection; callers cannot mutate campaign state through it.
function JAZZ_RIS_GetStrategyDiagnostics()
	local st = lState()
	if not st then
		return false
	end
	local out = {
		observed = {},
		delivered = {},
		delivery_order = {},
		pending = {},
		next_strategy_at = tonumber(st.next_strategy_at) or 0,
		catchup_done = not not st.strategy_catchup_done,
	}
	for key, value in pairs(st.strategy_observed) do
		out.observed[key] = value
	end
	for key, value in pairs(st.strategy_delivered) do
		out.delivered[key] = value
	end
	for index, value in ipairs(st.strategy_delivery_order) do
		out.delivery_order[index] = value
	end
	for _, row in ipairs(st.mail_queue) do
		if lIsStrategyRow(row) then
			out.pending[#out.pending + 1] = {
				key = row.key,
				kind = row.kind,
				material_id = row.material_id,
				email_id = row.email_id,
				ready_at = row.ready_at,
			}
		end
	end
	return out
end

local function lUpdateAfterSignal()
	local st = lState()
	if not st then
		return
	end
	lObserveNetwork(st, lNow())
	JAZZ_RIS_UpdateStrategyQueue(false)
end

local function lDelayedPoll(is_load_catchup, finish_new_game)
	local function poll()
		JAZZ_RIS_PollStrategySignals(is_load_catchup)
		if finish_new_game then
			local st = lState()
			if st then
				st.strategy_catchup_done = true
			end
		end
	end
	local delayed = rawget(_G, "DelayedCall")
	if type(delayed) == "function" then
		delayed(0, poll)
	else
		poll()
	end
end

function OnMsg.JAZZ_LegionAISquadManaged(squad_id, role)
	local root = rawget(_G, "gv_JAZZ_LegionAI")
	local row = type(root) == "table" and type(root.squads) == "table" and root.squads[squad_id]
	if type(row) == "table" then
		lObserveRowSignals(squad_id, row, lNow())
	else
		lObserveRowSignals(squad_id, { role = role }, lNow())
	end
	lUpdateAfterSignal()
end

function OnMsg.JAZZ_LegionAITaskAssigned(squad_id, task_type)
	local root = rawget(_G, "gv_JAZZ_LegionAI")
	local row = type(root) == "table" and type(root.squads) == "table" and root.squads[squad_id]
	if type(row) == "table" then
		lObserveRowSignals(squad_id, row, lNow())
	else
		lObserveRowSignals(squad_id, { task = { task_type = task_type } }, lNow())
	end
	lUpdateAfterSignal()
end

function OnMsg.JAZZ_LegionAIMajorResponse(squad_id)
	if lIsSquadObservable(squad_id) then
		lRecordObservation("strategy_red", lNow())
		lUpdateAfterSignal()
	end
end

function OnMsg.JAZZ_LegionAISquadRefit(squad_id)
	local root = rawget(_G, "gv_JAZZ_LegionAI")
	local row = type(root) == "table" and type(root.squads) == "table" and root.squads[squad_id]
	local task = type(row) == "table" and type(row.task) == "table" and row.task
	if type(row) == "table"
		and lIsSquadObservable(squad_id)
		and (row.state == "wounded" or (task and task.task_type == "return_wounded"))
	then
		lRecordObservation("strategy_wounded", lNow())
		lUpdateAfterSignal()
	end
end

function OnMsg.NewHour()
	JAZZ_RIS_PollStrategySignals(false)
end

function OnMsg.SatelliteTick()
	JAZZ_RIS_PollStrategySignals(false)
end

function OnMsg.OpenSatelliteView()
	JAZZ_RIS_PollStrategySignals(false)
end

function OnMsg.LoadGame()
	lDelayedPoll(true, false)
end

function OnMsg.ModsReloaded()
	lDelayedPoll(false, false)
end

function OnMsg.NewGame()
	lDelayedPoll(false, true)
end
