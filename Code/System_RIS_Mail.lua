-- R.I.S. mail: delayed queue (welcome + Legion briefs), tab lock (JAZZ-UI-RIS-001).
-- Desk sends at most one notification every RIS_DISPATCH_SPACING_H campaign hours.
-- Items become eligible at their own ready_at (welcome ~2h; baseline brief ~7h; raises ~5h after event).

GameVar("gv_JAZZ_RIS", function()
	return {
		schema_version = 3,
		welcome_sent = false,
		welcome_read = false,
		last_mailed_tier = 0,
		mod_awake_at = false,
		mail_queue = {},
		next_dispatch_at = 0,
		kills = {},
		met_types = {},
		obits_sent = {},
		battles = {},
		dossiers = {},
		quest_met = {},
		strategy_observed = {},
		strategy_delivered = {},
		strategy_delivery_order = {},
		next_strategy_at = 0,
		strategy_catchup_done = false,
		strategy_major_delivery_baseline = {},
		-- legacy fields kept for old saves (ignored once queue is live)
		welcome_due_at = false,
	}
end)

g_JAZZ_RIS_MarkEmailWrapped = rawget(_G, "g_JAZZ_RIS_MarkEmailWrapped") or false
g_JAZZ_RIS_MarkEmailBase = rawget(_G, "g_JAZZ_RIS_MarkEmailBase") or false
g_JAZZ_RIS_MarkEmailFn = rawget(_G, "g_JAZZ_RIS_MarkEmailFn") or false
g_JAZZ_RIS_BrowserInstalled = rawget(_G, "g_JAZZ_RIS_BrowserInstalled") or false

-- Mail desk timing / email ids (behavior constants — do not retune in refactor waves).
local RIS_STATE_SCHEMA = 3
local RIS_LEGACY_AAR_SCHEMA = 2
local RIS_WELCOME_ID = "RIS_Welcome"
local RIS_WELCOME_DELAY_H = 2
local RIS_BASELINE_BRIEF_DELAY_H = 7
local RIS_RAISE_BRIEF_DELAY_H = 5
local RIS_FIELD_NOTE_DELAY_H = 5
local RIS_DISPATCH_SPACING_H = 5
local RIS_STRATEGY_SPACING_H = 24
local RIS_SIGHTING_ID = "RIS_UnitSighting"
local RIS_ELITE_OBIT_ID = "RIS_EliteObit"
local RIS_NPC_OBIT_ID = "RIS_NpcObit"
local RIS_BRIEF_TIERS = { 11, 12, 13, 21, 22, 23, 24, 25, 31, 32, 33 }
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
local RIS_STRATEGY_MATERIALS = {}
local RIS_STRATEGY_INDEX = {}
for index, material_id in ipairs(RIS_STRATEGY_ORDER) do
	RIS_STRATEGY_MATERIALS[RIS_STRATEGY_EMAILS[material_id]] = material_id
	RIS_STRATEGY_INDEX[material_id] = index
end

local function lHour()
	local constants = rawget(_G, "const")
	return (constants and constants.Scale and constants.Scale.h) or (60 * 60 * 1000)
end

local function lNow()
	local game = rawget(_G, "Game")
	return game and game.CampaignTime or 0
end

local function lIsStableT(value)
	local isT = rawget(_G, "IsT")
	if type(isT) == "function" then
		local ok, translated = pcall(isT, value)
		if not ok or not translated then
			return false
		end
	end
	local getId = rawget(_G, "TGetID")
	if type(getId) == "function" then
		local ok, id = pcall(getId, value)
		return ok and type(id) == "number" and id ~= 0
	end
	return type(value) == "table" and type(value[1]) == "number"
end

local function lDisplayRefFromUnitData(id)
	if type(id) ~= "string" or id == "" then
		return false
	end
	local questBank = rawget(_G, "JAZZ_RIS_QUEST_DOSSIERS")
	local card = type(questBank) == "table" and questBank[id]
	if card and card.title then
		return card.title
	end
	local unitData = rawget(_G, "gv_UnitData")
	local unit = type(unitData) == "table" and unitData[id]
	if unit then
		local pick = unit.Nick
		if not pick or pick == "" then
			pick = unit.Name
		end
		if pick and pick ~= "" and pick ~= id then
			return pick
		end
	end
	local classes = rawget(_G, "g_Classes")
	local class = type(classes) == "table" and classes[id]
	if class then
		local pick = class.Nick
		if not pick or pick == "" then
			pick = class.Name
		end
		if pick and pick ~= "" and pick ~= id then
			return pick
		end
	end
	return false
end

local function lNormalizeDisplayRef(value, fallback_id)
	if lIsStableT(value) then
		return value
	end
	if type(value) == "string" and value ~= "" and value ~= fallback_id then
		return value
	end
	return lDisplayRefFromUnitData(fallback_id)
end

local function lNpcIdFromObitKey(key)
	if type(key) ~= "string" then
		return false
	end
	return string.match(key, "^npc:(.+)$")
		or string.match(key, "^elite:session:(.+)$")
		or false
end

local function lFallbackRef(field)
	local extra = rawget(_G, "JAZZ_RIS_EXTRA")
	local value = type(extra) == "table" and extra[field]
	if lIsStableT(value) then
		return value
	end
	if field == "legacy_contact" then
		local ui = rawget(_G, "JAZZ_RIS_UI")
		value = type(ui) == "table" and ui.section_legion
		return lIsStableT(value) and value or false
	end
	return false
end

local function lRawContextId(value)
	if type(value) == "string" then
		return value
	end
	if type(value) == "table"
		and value.untranslated
		and type(value[1]) == "string"
	then
		return value[1]
	end
	return false
end

local function lStrategyMaterialFromRow(item)
	if type(item) ~= "table" then
		return false
	end
	if RIS_STRATEGY_INDEX[item.material_id] then
		return item.material_id
	end
	local email_id = item.email_id or item.email
	if RIS_STRATEGY_MATERIALS[email_id] then
		return RIS_STRATEGY_MATERIALS[email_id]
	end
	if type(item.key) == "string" then
		local material_id = string.match(item.key, "^strategy_(strategy_.+)$")
		if RIS_STRATEGY_INDEX[material_id] then
			return material_id
		end
	end
	return false
end

local function lAppendStrategyOrder(st, material_id)
	for _, existing in ipairs(st.strategy_delivery_order) do
		if existing == material_id then
			return false
		end
	end
	st.strategy_delivery_order[#st.strategy_delivery_order + 1] = material_id
	return true
end

local function lMigrateStrategyState(st)
	local now = lNow()
	local received_materials = {}
	local inbox_checked = false
	for email_id, material_id in pairs(RIS_STRATEGY_MATERIALS) do
		if st.strategy_observed[material_id] == nil
			and st.strategy_observed[email_id] ~= nil
		then
			st.strategy_observed[material_id] = st.strategy_observed[email_id]
		end
		if st.strategy_delivered[material_id] == nil
			and st.strategy_delivered[email_id] ~= nil
		then
			st.strategy_delivered[material_id] = st.strategy_delivered[email_id]
		end
	end

	local clean_order = {}
	local seen_order = {}
	for _, stored_id in ipairs(st.strategy_delivery_order) do
		local material_id = RIS_STRATEGY_MATERIALS[stored_id] or stored_id
		if type(material_id) == "string" and not seen_order[material_id] then
			seen_order[material_id] = true
			clean_order[#clean_order + 1] = material_id
			if RIS_STRATEGY_INDEX[material_id]
				and not st.strategy_delivered[material_id]
			then
				st.strategy_delivered[material_id] = now
			end
		end
	end
	st.strategy_delivery_order = clean_order

	local get_received = rawget(_G, "GetReceivedEmails")
	local raw_received = rawget(_G, "gv_ReceivedEmails")
	local inbox_newest_first = false
	if type(raw_received) == "table" or type(get_received) == "function" then
		local ok, received = true, raw_received
		if type(received) ~= "table" then
			ok, received = pcall(get_received)
			inbox_newest_first = true
		end
		if ok and type(received) == "table" then
			inbox_checked = true
			st.strategy_delivery_order = {}
			seen_order = {}
			-- Raw gv_ReceivedEmails is oldest-first; GetReceivedEmails returns a
			-- reversed copy. In both cases rebuild archive rows oldest-first.
			local first = inbox_newest_first and #received or 1
			local last = inbox_newest_first and 1 or #received
			local step = inbox_newest_first and -1 or 1
			for index = first, last, step do
				local email = received[index]
				local material_id = type(email) == "table"
					and RIS_STRATEGY_MATERIALS[email.id]
				if material_id then
					local first_receipt = not received_materials[material_id]
					received_materials[material_id] = true
					local delivered_at = tonumber(email.time) or now
					local stored_at = tonumber(st.strategy_delivered[material_id])
					if first_receipt or not stored_at or delivered_at < stored_at then
						st.strategy_delivered[material_id] = delivered_at
					end
					if not seen_order[material_id] then
						seen_order[material_id] = true
						st.strategy_delivery_order[#st.strategy_delivery_order + 1] = material_id
					end
				end
			end
		end
	end

	if inbox_checked then
		for _, material_id in ipairs(RIS_STRATEGY_ORDER) do
			if st.strategy_delivered[material_id]
				and not received_materials[material_id]
			then
				-- The inbox is authoritative. Older code could write delivery state
				-- even when ReceiveEmail deferred or rejected the message.
				st.strategy_delivered[material_id] = nil
			end
		end
	end

	local next_strategy_at = inbox_checked and 0
		or (tonumber(st.next_strategy_at) or 0)
	for _, material_id in ipairs(RIS_STRATEGY_ORDER) do
		local observed_at = st.strategy_observed[material_id]
		if observed_at ~= nil and observed_at ~= false then
			st.strategy_observed[material_id] = tonumber(observed_at) or now
		end
		local delivered_at = st.strategy_delivered[material_id]
		if delivered_at ~= nil and delivered_at ~= false then
			local numeric_delivered_at = tonumber(delivered_at)
			if not numeric_delivered_at then
				numeric_delivered_at = now
			end
			if delivered_at ~= numeric_delivered_at then
				delivered_at = numeric_delivered_at
				st.strategy_delivered[material_id] = delivered_at
			end
			local first_observed_at = tonumber(st.strategy_observed[material_id])
			if not first_observed_at or delivered_at < first_observed_at then
				st.strategy_observed[material_id] = delivered_at
			end
			if not seen_order[material_id] then
				seen_order[material_id] = true
				st.strategy_delivery_order[#st.strategy_delivery_order + 1] = material_id
			end
			next_strategy_at = math.max(
				next_strategy_at,
				delivered_at + RIS_STRATEGY_SPACING_H * lHour()
			)
		end
	end
	local delivered_order = {}
	for _, material_id in ipairs(st.strategy_delivery_order) do
		if st.strategy_delivered[material_id] then
			delivered_order[#delivered_order + 1] = material_id
		end
	end
	st.strategy_delivery_order = delivered_order
	st.next_strategy_at = next_strategy_at
end

local function lMigrateQueue(st)
	for _, item in ipairs(st.mail_queue) do
		if type(item) == "table" then
			local key = item.key
			local emailId = item.email_id or item.email
			item.email_id = item.email_id or item.email
			local isSighting = item.kind == "meet"
				or emailId == RIS_SIGHTING_ID
				or (type(key) == "string" and string.match(key, "^meet_"))
			if isSighting then
				item.kind = "meet"
				item.email_id = item.email_id or item.email or RIS_SIGHTING_ID
				local oldContext = type(item.context) == "table" and item.context or false
				item.type_id = lRawContextId(item.type_id)
					or (oldContext and lRawContextId(oldContext.type_id))
					or (type(key) == "string"
						and string.match(key, "^meet_(JAZZ_Legion_.+)$"))
				if item.type_id then
					item.key = "meet_" .. item.type_id
				end
				if type(item.context) == "table" then
					item.context.unit_title = nil
					item.context.dossier = nil
					if not next(item.context) then
						item.context = nil
					end
				end
				if item.type_id then
					-- Older code unlocked the contact at enqueue time. A pending
					-- sighting proves it has not reached the inbox yet.
					st.met_types[item.type_id] = nil
				end
			elseif item.kind == "obit"
				or emailId == RIS_ELITE_OBIT_ID
				or emailId == RIS_NPC_OBIT_ID
			then
				item.kind = "obit"
				local oldContext = type(item.context) == "table" and item.context or false
				local obitKey = lRawContextId(item.obit_key)
					or (type(key) == "string" and string.match(key, "^obit_(.+)$"))
				local npcId = lRawContextId(item.npc_id)
					or (oldContext and lRawContextId(oldContext.npc_id))
					or lNpcIdFromObitKey(obitKey)
				if not obitKey and npcId then
					obitKey = emailId == RIS_ELITE_OBIT_ID
						and ("elite:session:" .. npcId)
						or ("npc:" .. npcId)
				end
				item.obit_key = obitKey
				if obitKey then
					item.key = "obit_" .. obitKey
				end
				local oldName = item.name_ref or (oldContext and (oldContext.name_ref or oldContext.name))
				local stableOldName = lIsStableT(oldName) and oldName or false
				item.name_ref = lDisplayRefFromUnitData(npcId)
					or stableOldName
					or lFallbackRef("legacy_opponent")
					or (type(oldName) == "string" and oldName ~= "" and oldName)
				if oldContext then
					oldContext.name = nil
					oldContext.name_ref = nil
					oldContext.npc_id = nil
					oldContext.obit_key = nil
					if not next(oldContext) then
						item.context = nil
					end
				end
			end
			if item.kind == "obit" and item.obit_key then
				-- Older code set this at enqueue time. A surviving queue row proves
				-- the email has not actually reached the inbox yet.
				st.obits_sent[item.obit_key] = nil
			end
		end
	end
	local seen = {}
	local index = 1
	while index <= #st.mail_queue do
		local item = st.mail_queue[index]
		local key = type(item) == "table"
			and (item.kind == "meet" or item.kind == "obit")
			and item.key
		if key and seen[key] then
			table.remove(st.mail_queue, index)
		else
			if key then
				seen[key] = true
			end
			index = index + 1
		end
	end
end

local function lMigrateReceivedContexts(st)
	local getReceived = rawget(_G, "GetReceivedEmails")
	if type(getReceived) ~= "function" then
		return false
	end
	local ok, received = pcall(getReceived)
	if not ok or type(received) ~= "table" then
		return false
	end
	local changed = false
	for _, email in ipairs(received) do
		if type(email) == "table" and email.id == RIS_SIGHTING_ID then
			local oldContext = type(email.context) == "table" and email.context or {}
			local typeId = lRawContextId(oldContext.type_id) or nil
			local bank = rawget(_G, "JAZZ_RIS_DOSSIERS")
			local card = type(bank) == "table" and typeId and bank[typeId]
			if typeId and not st.met_types[typeId] then
				st.met_types[typeId] = true
				changed = true
			end
			local unitTitle = card and card.title
				or (lIsStableT(oldContext.unit_title) and oldContext.unit_title)
				or lFallbackRef("legacy_contact")
			if unitTitle and (
				oldContext.unit_title ~= unitTitle
				or oldContext.type_id ~= typeId
				or oldContext.dossier ~= nil
				or type(email.context) ~= "table"
			) then
				email.context = {
					type_id = typeId,
					unit_title = unitTitle,
				}
				changed = true
			end
		elseif type(email) == "table"
			and (email.id == RIS_ELITE_OBIT_ID or email.id == RIS_NPC_OBIT_ID)
		then
			local oldContext = type(email.context) == "table" and email.context or {}
			local obitKey = lRawContextId(oldContext.obit_key) or nil
			local npcId = lRawContextId(oldContext.npc_id)
				or lNpcIdFromObitKey(obitKey)
				or nil
			if not obitKey and npcId then
				obitKey = email.id == RIS_ELITE_OBIT_ID
					and ("elite:session:" .. npcId)
					or ("npc:" .. npcId)
			end
			if obitKey and not st.obits_sent[obitKey] then
				st.obits_sent[obitKey] = true
				changed = true
			end
			local stableName = lDisplayRefFromUnitData(npcId)
				or (lIsStableT(oldContext.name) and oldContext.name)
				or lFallbackRef("legacy_opponent")
				or (type(oldContext.name) == "string" and oldContext.name ~= ""
					and oldContext.name)
			if stableName and (
				oldContext.name ~= stableName
				or type(email.context) ~= "table"
			) then
				email.context = {
					name = stableName,
					npc_id = npcId,
					obit_key = obitKey,
				}
				changed = true
			end
		end
	end
	for index = #st.mail_queue, 1, -1 do
		local item = st.mail_queue[index]
		local already_received = type(item) == "table"
			and (
				(item.kind == "meet" and item.type_id and st.met_types[item.type_id])
				or (item.kind == "obit"
					and item.obit_key
					and st.obits_sent[item.obit_key])
			)
		if already_received then
			table.remove(st.mail_queue, index)
			changed = true
		end
	end
	local modified = rawget(_G, "ObjModified")
	if changed and type(modified) == "function" then
		modified(rawget(_G, "gv_ReceivedEmails") or received)
		modified("jazz_ris")
	end
	return changed
end

local function lMigrateStrategyQueue(st)
	local chosen, chosen_at, chosen_index
	local network_delivered = not not st.strategy_delivered.strategy_network
	for _, item in ipairs(st.mail_queue) do
		local material_id = lStrategyMaterialFromRow(item)
		if material_id then
			local observed_at = tonumber(st.strategy_observed[material_id])
				or tonumber(item.ready_at)
				or 0
			if not tonumber(st.strategy_observed[material_id]) then
				st.strategy_observed[material_id] = observed_at
			end
			item.key = "strategy_" .. material_id
			item.kind = "strategy"
			item.material_id = material_id
			item.email_id = RIS_STRATEGY_EMAILS[material_id]
			item.ready_at = math.max(
				observed_at,
				tonumber(st.next_strategy_at) or 0
			)
			-- Queued strategy prose always resolves from JAZZ_RIS_STRATEGY.
			item.context = nil
			item.title = nil
			item.body = nil
			local order_index = RIS_STRATEGY_INDEX[material_id]
			local eligible = not st.strategy_delivered[material_id]
				and (network_delivered or material_id == "strategy_network")
			if eligible and (
				not chosen
				or observed_at < chosen_at
				or (observed_at == chosen_at and order_index < chosen_index)
			) then
				chosen = item
				chosen_at = observed_at
				chosen_index = order_index
			end
		end
	end

	for index = #st.mail_queue, 1, -1 do
		local item = st.mail_queue[index]
		if lStrategyMaterialFromRow(item) and item ~= chosen then
			table.remove(st.mail_queue, index)
		end
	end
end

local function lMigrateBattles(st)
	for _, entry in ipairs(st.battles) do
		if type(entry) == "table" then
			local version = tonumber(entry.record_version or entry.version)
			local knownLegacy = (version and version < 2)
				or (not version and (
					entry.legacy
					or entry.kind == "legacy"
					or entry.title ~= nil
					or entry.body ~= nil
					or (entry.kind == nil
						and (tonumber(entry.schema_version) or 0) <= RIS_LEGACY_AAR_SCHEMA)
				))
			if knownLegacy then
				entry.schema_version = RIS_STATE_SCHEMA
				entry.record_version = 1
				entry.version = 1
				entry.kind = "legacy"
				entry.legacy = true
				-- Plain prose and translated location labels cannot follow a language switch.
				entry.title = nil
				entry.body = nil
				entry.sector_name = nil
			end
		end
	end
end

--- Idempotent old-save/reload migration for the R.I.S. campaign state.
function JAZZ_RIS_MigrateState()
	local st = rawget(_G, "gv_JAZZ_RIS")
	if type(st) ~= "table" then
		st = {}
		rawset(_G, "gv_JAZZ_RIS", st)
	end

	local aliases = {
		mail_queue = "queue",
		obits_sent = "obits",
	}
	for _, key in ipairs({
		"mail_queue",
		"kills",
		"met_types",
		"dossiers",
		"obits_sent",
		"battles",
		"quest_met",
		"strategy_observed",
		"strategy_delivered",
		"strategy_delivery_order",
		"strategy_major_delivery_baseline",
	}) do
		if type(st[key]) ~= "table" then
			local alias = aliases[key]
			st[key] = alias and type(st[alias]) == "table" and st[alias] or {}
		end
	end
	if type(st.next_dispatch_at) ~= "number" then
		st.next_dispatch_at = 0
	end
	if type(st.next_strategy_at) ~= "number" then
		st.next_strategy_at = 0
	end
	if type(st.strategy_catchup_done) ~= "boolean" then
		st.strategy_catchup_done = false
	end

	lMigrateStrategyState(st)
	lMigrateQueue(st)
	lMigrateReceivedContexts(st)
	lMigrateStrategyQueue(st)
	lMigrateBattles(st)
	local schema_version = tonumber(st.schema_version)
	if not schema_version or schema_version < RIS_STATE_SCHEMA then
		st.schema_version = RIS_STATE_SCHEMA
	elseif st.schema_version ~= schema_version then
		st.schema_version = schema_version
	end
	return st
end

local function lState()
	return JAZZ_RIS_MigrateState()
end

local function lBriefEmailId(tier)
	return string.format("RIS_LegionBrief_%d", tier)
end

local function lResolveBriefEmail(tier)
	tier = tonumber(tier)
	if not tier then
		return false, false
	end
	local emails = rawget(_G, "Emails")
	local emailId = lBriefEmailId(tier)
	if type(emails) == "table" and emails[emailId] then
		return emailId, tier
	end
	for i = #RIS_BRIEF_TIERS, 1, -1 do
		local t = RIS_BRIEF_TIERS[i]
		if t <= tier and type(emails) == "table" and emails[lBriefEmailId(t)] then
			return lBriefEmailId(t), t
		end
	end
	return false, false
end

local function lHasAnyLegionBriefMail()
	local getReceivedEmails = rawget(_G, "GetReceivedEmails")
	if type(getReceivedEmails) ~= "function" then
		return false
	end
	for _, email in ipairs(getReceivedEmails()) do
		if type(email.id) == "string" and string.match(email.id, "^RIS_LegionBrief_") then
			return true
		end
	end
	return false
end

local function lQueueHasKey(st, key)
	for _, item in ipairs(st.mail_queue) do
		if item.key == key then
			return true
		end
	end
	return false
end

--- Update an existing pending row (same key): earlier ready_at wins; tier/email may refresh.
local function lRefreshQueuedItem(st, item)
	for _, row in ipairs(st.mail_queue) do
		if row.key == item.key then
			if item.ready_at and (not row.ready_at or item.ready_at < row.ready_at) then
				row.ready_at = item.ready_at
			end
			if item.tier then
				row.tier = item.tier
				row.email_id = item.email_id
			end
			return true
		end
	end
	return false
end

local function lEnqueue(st, item)
	if not st or not item or not item.key or not item.email_id then
		return false
	end
	if lQueueHasKey(st, item.key) then
		lRefreshQueuedItem(st, item)
		return false
	end
	st.mail_queue[#st.mail_queue + 1] = item
	return true
end

--- Shared desk enqueue surface. Strategy callers provide only stable ids/times;
--- localized title/body always resolve from the current-language content bank.
function JAZZ_RIS_EnqueueMail(item)
	if type(item) ~= "table" then
		return false
	end
	local st = lState()
	if not st then
		return false
	end
	if item.kind ~= "strategy" then
		return lEnqueue(st, item)
	end

	local material_id = lStrategyMaterialFromRow(item)
	if not material_id or st.strategy_delivered[material_id] then
		return false
	end
	local clean = {
		key = "strategy_" .. material_id,
		kind = "strategy",
		material_id = material_id,
		email_id = RIS_STRATEGY_EMAILS[material_id],
		ready_at = tonumber(item.ready_at) or lNow(),
	}
	local existing = false
	for index = #st.mail_queue, 1, -1 do
		local row = st.mail_queue[index]
		if lStrategyMaterialFromRow(row) then
			if row.key == clean.key and not existing then
				existing = row
			else
				table.remove(st.mail_queue, index)
			end
		end
	end
	if existing then
		existing.kind = clean.kind
		existing.material_id = clean.material_id
		existing.email_id = clean.email_id
		existing.ready_at = clean.ready_at
		existing.context = nil
		existing.title = nil
		existing.body = nil
		return false
	end
	return lEnqueue(st, clean)
end

--- First queue index with ready_at <= now (FIFO among due items).
local function lPickDueIndex(st, now)
	for i, item in ipairs(st.mail_queue) do
		local strategy_blocked = item.kind == "strategy"
			and now < (tonumber(st.next_strategy_at) or 0)
		if (tonumber(item.ready_at) or 0) <= now and not strategy_blocked then
			return i
		end
	end
	return false
end

local function lBumpDispatch(st, now)
	st.next_dispatch_at = now + RIS_DISPATCH_SPACING_H * lHour()
end

function JAZZ_RIS_IsWelcomeRead()
	local st = lState()
	if st and st.welcome_read then
		return true
	end
	local getReceivedEmails = rawget(_G, "GetReceivedEmails")
	if type(getReceivedEmails) == "function" then
		for _, email in ipairs(getReceivedEmails()) do
			if email.id == RIS_WELCOME_ID and email.read then
				if st then
					st.welcome_read = true
					st.welcome_sent = true
				end
				return true
			end
		end
	end
	return false
end

function JAZZ_RIS_ApplyTabLock()
	local tabState = rawget(_G, "PDABrowserTabState")
	if type(tabState) ~= "table" then
		return
	end
	local unlocked = JAZZ_RIS_IsWelcomeRead()
	if tabState.ris then
		tabState.ris.locked = not unlocked
	else
		tabState.ris = { locked = not unlocked }
	end
	ObjModified("pda browser tabs")
end

local function lEnsureAwake(st)
	if not st.mod_awake_at then
		st.mod_awake_at = lNow()
	end
	return st.mod_awake_at
end

--- Schedule welcome + baseline supply brief (usually T1-1) after mod awake / NewGame.
function JAZZ_RIS_EnsureStartupQueue()
	local st = lState()
	if not st then
		return
	end
	local awake = lEnsureAwake(st)
	if not st.welcome_sent and not lQueueHasKey(st, "welcome") then
		local getReceivedEmails = rawget(_G, "GetReceivedEmails")
		if type(getReceivedEmails) == "function" then
			for _, email in ipairs(getReceivedEmails()) do
				if email.id == RIS_WELCOME_ID then
					st.welcome_sent = true
					break
				end
			end
		end
	end
	local emails = rawget(_G, "Emails")
	if not st.welcome_sent
		and not lQueueHasKey(st, "welcome")
		and type(emails) == "table"
		and emails[RIS_WELCOME_ID]
	then
		lEnqueue(st, {
			key = "welcome",
			kind = "welcome",
			email_id = RIS_WELCOME_ID,
			ready_at = awake + RIS_WELCOME_DELAY_H * lHour(),
		})
	end
	-- Baseline brief: current tier once, ~7h after awake (fixes missing T1-1).
	local getTier = rawget(_G, "JAZZ_GetLegionTier")
	local current = (type(getTier) == "function" and tonumber(getTier())) or 11
	local emailId, tier = lResolveBriefEmail(current)
	local briefKey = emailId and ("brief_" .. tostring(tier)) or false
	local already = (tonumber(st.last_mailed_tier) or 0) >= (tier or 0) and lHasAnyLegionBriefMail()
	if emailId and briefKey and not already and not lQueueHasKey(st, briefKey) then
		-- Poisoned saves marked last_mailed without inbox: still queue.
		if (tonumber(st.last_mailed_tier) or 0) >= tier and not lHasAnyLegionBriefMail() then
			st.last_mailed_tier = 0
		end
		if (tonumber(st.last_mailed_tier) or 0) < tier then
			lEnqueue(st, {
				key = briefKey,
				kind = "brief",
				email_id = emailId,
				tier = tier,
				ready_at = awake + RIS_BASELINE_BRIEF_DELAY_H * lHour(),
			})
		end
	end
end

local function lContextForEmail(ctx)
	if type(ctx) ~= "table" then
		return false
	end
	local out = {}
	for k, v in pairs(ctx) do
		if k == "type_id" or k == "npc_id" or k == "obit_key" then
			out[k] = v
		elseif type(v) == "string" then
			out[k] = Untranslated(v)
		else
			out[k] = v
		end
	end
	return out
end

local function lDeliveryContext(item)
	if item.kind == "meet" then
		local bank = rawget(_G, "JAZZ_RIS_DOSSIERS")
		local card = type(bank) == "table" and bank[item.type_id]
		local title = card and card.title or lFallbackRef("legacy_contact")
		if not title then
			return false, false
		end
		if not card then
			-- A removed archetype from an old save must not block the desk forever
			-- or become a new stable contact under an obsolete id.
			item.type_id = nil
		end
		-- A still-valid type_id stays as hidden stable context for future migrations.
		return lContextForEmail({
			type_id = item.type_id,
			unit_title = title,
		}), true
	end
	if item.kind == "obit" then
		local npcId = lNpcIdFromObitKey(item.obit_key)
		local nameRef = lNormalizeDisplayRef(item.name_ref, npcId)
		if not nameRef then
			return false, "drop"
		end
		return lContextForEmail({
			name = nameRef,
			npc_id = npcId,
			obit_key = item.obit_key,
		}), true
	end
	return lContextForEmail(item.context), true
end

local function lMarkStrategyDelivered(st, item, now)
	local material_id = lStrategyMaterialFromRow(item)
	if not material_id or st.strategy_delivered[material_id] then
		return false
	end
	st.strategy_observed[material_id] = tonumber(st.strategy_observed[material_id]) or now
	st.strategy_delivered[material_id] = now
	lAppendStrategyOrder(st, material_id)
	st.next_strategy_at = math.max(
		tonumber(st.next_strategy_at) or 0,
		now + RIS_STRATEGY_SPACING_H * lHour()
	)
	local modified = rawget(_G, "ObjModified")
	if type(modified) == "function" then
		modified("jazz_ris")
	end
	return true
end

local function lReceivedEmailCount(email_id)
	local getReceived = rawget(_G, "GetReceivedEmails")
	if type(getReceived) ~= "function" then
		return false
	end
	local ok, received = pcall(getReceived)
	if not ok or type(received) ~= "table" then
		return false
	end
	local count = 0
	for _, email in ipairs(received) do
		if type(email) == "table" and email.id == email_id then
			count = count + 1
		end
	end
	return count
end

local function lDeliver(st, item)
	local receiveEmail = rawget(_G, "ReceiveEmail")
	local emails = rawget(_G, "Emails")
	if type(receiveEmail) ~= "function" or type(emails) ~= "table" or not emails[item.email_id] then
		return false
	end
	local ctx, contextReady = lDeliveryContext(item)
	if contextReady == "drop" then
		-- Do not leak an internal id or a literal placeholder from an unrecoverable old row.
		return true
	end
	if not contextReady then
		return false
	end
	local beforeCount = lReceivedEmailCount(item.email_id)
	if ctx then
		receiveEmail(item.email_id, ctx)
	else
		receiveEmail(item.email_id)
	end
	local afterCount = lReceivedEmailCount(item.email_id)
	if beforeCount ~= false and afterCount ~= false and afterCount <= beforeCount then
		local preset = emails[item.email_id]
		if beforeCount == 0 or (preset and preset.repeatable) then
			return false
		end
	end
	if item.kind == "welcome" then
		st.welcome_sent = true
		JAZZ_RIS_ApplyTabLock()
	elseif item.kind == "brief" and item.tier then
		st.last_mailed_tier = Max(tonumber(st.last_mailed_tier) or 0, item.tier)
	elseif item.kind == "meet" and item.type_id then
		st.met_types[item.type_id] = true
		ObjModified("jazz_ris")
	elseif item.kind == "obit" and item.obit_key then
		st.obits_sent[item.obit_key] = true
	elseif item.kind == "strategy" then
		lMarkStrategyDelivered(st, item, lNow())
	end
	return true
end

local function lDispatchOne(st, item, now)
	if not lDeliver(st, item) then
		-- Put back at front if preset missing (retry later).
		table.insert(st.mail_queue, 1, item)
		lBumpDispatch(st, now)
		return false
	end
	lBumpDispatch(st, now)
	return true
end

local function lAskStrategyObserver(is_load_catchup)
	local poll = rawget(_G, "JAZZ_RIS_PollStrategySignals")
	if type(poll) == "function" then
		return poll(not not is_load_catchup)
	end
	local update = rawget(_G, "JAZZ_RIS_UpdateStrategyQueue")
	if type(update) == "function" then
		return update(not not is_load_catchup)
	end
	return false
end

--- Drain at most one eligible item when the desk spacing slot is free.
function JAZZ_RIS_ProcessMailQueue(is_load_catchup)
	local st = lState()
	if not st then
		return false
	end
	lAskStrategyObserver(is_load_catchup)
	JAZZ_RIS_EnsureStartupQueue()
	local now = lNow()
	if rawget(_G, "g_Combat") then
		return false
	end
	if now < (tonumber(st.next_dispatch_at) or 0) then
		return false
	end
	local idx = lPickDueIndex(st, now)
	if not idx then
		return false
	end
	local item = table.remove(st.mail_queue, idx)
	local delivered = lDispatchOne(st, item, now)
	if delivered then
		lAskStrategyObserver(false)
	end
	return delivered
end

function JAZZ_RIS_EnqueueLegionBrief(tier, delay_h)
	tier = tonumber(tier)
	if not tier then
		return false
	end
	local st = lState()
	if not st then
		return false
	end
	local emailId, resolved = lResolveBriefEmail(tier)
	if not emailId then
		return false
	end
	if (tonumber(st.last_mailed_tier) or 0) >= resolved and lHasAnyLegionBriefMail() then
		return false
	end
	delay_h = tonumber(delay_h) or RIS_RAISE_BRIEF_DELAY_H
	lEnqueue(st, {
		key = "brief_" .. tostring(resolved),
		kind = "brief",
		email_id = emailId,
		tier = resolved,
		ready_at = lNow() + delay_h * lHour(),
	})
	return true
end

function JAZZ_RIS_OnTierRaised(new_tier)
	new_tier = tonumber(new_tier)
	if not new_tier then
		return
	end
	JAZZ_RIS_EnqueueLegionBrief(new_tier, RIS_RAISE_BRIEF_DELAY_H)
end

--- First confirmed contact queues a short card; full dossier still requires the kill threshold.
function JAZZ_RIS_EnqueueUnitSighting(type_id, delay_h)
	if type(type_id) ~= "string" or not string.match(type_id, "^JAZZ_Legion_") then
		return false
	end
	local st = lState()
	if not st then
		return false
	end
	if st.met_types[type_id] or lQueueHasKey(st, "meet_" .. type_id) then
		return false
	end
	local bank = rawget(_G, "JAZZ_RIS_DOSSIERS")
	local card = type(bank) == "table" and bank[type_id]
	if not card then
		return false
	end
	local emails = rawget(_G, "Emails")
	if type(emails) ~= "table" or not emails[RIS_SIGHTING_ID] then
		return false
	end
	delay_h = tonumber(delay_h) or RIS_FIELD_NOTE_DELAY_H
	lEnqueue(st, {
		key = "meet_" .. type_id,
		kind = "meet",
		email_id = RIS_SIGHTING_ID,
		type_id = type_id,
		ready_at = lNow() + delay_h * lHour(),
	})
	return true
end

local function lDisplayRefKey(value)
	local getId = rawget(_G, "TGetID")
	if lIsStableT(value) and type(getId) == "function" then
		local id = getId(value)
		if id then
			return "t:" .. tostring(id)
		end
	end
	if type(value) == "string" and value ~= "" then
		return "name:" .. value
	end
	if type(value) == "table" and value[1] then
		return "t:" .. tostring(value[1])
	end
	return false
end

function JAZZ_RIS_EnqueueEliteObit(name, delay_h, stable_key)
	local nameRef = lNormalizeDisplayRef(name)
	if not nameRef then
		return false
	end
	local st = lState()
	if not st then
		return false
	end
	local refKey = stable_key and tostring(stable_key) or lDisplayRefKey(nameRef)
	if not refKey then
		return false
	end
	local obit_key = "elite:" .. refKey
	if st.obits_sent[obit_key] or lQueueHasKey(st, "obit_" .. obit_key) then
		return false
	end
	local emails = rawget(_G, "Emails")
	if type(emails) ~= "table" or not emails[RIS_ELITE_OBIT_ID] then
		return false
	end
	delay_h = tonumber(delay_h) or RIS_FIELD_NOTE_DELAY_H
	lEnqueue(st, {
		key = "obit_" .. obit_key,
		kind = "obit",
		email_id = RIS_ELITE_OBIT_ID,
		obit_key = obit_key,
		ready_at = lNow() + delay_h * lHour(),
		name_ref = nameRef,
	})
	return true
end

function JAZZ_RIS_EnqueueNpcObit(session_id, name, delay_h)
	if type(session_id) ~= "string" or session_id == "" then
		return false
	end
	local st = lState()
	if not st then
		return false
	end
	local keys = rawget(_G, "JAZZ_RIS_KEY_NPCS")
	local questBank = rawget(_G, "JAZZ_RIS_QUEST_DOSSIERS")
	local is_key = (type(keys) == "table" and keys[session_id])
		or (type(questBank) == "table" and questBank[session_id])
	if not is_key then
		return false
	end
	local obit_key = "npc:" .. session_id
	if st.obits_sent[obit_key] or lQueueHasKey(st, "obit_" .. obit_key) then
		return false
	end
	local emails = rawget(_G, "Emails")
	if type(emails) ~= "table" or not emails[RIS_NPC_OBIT_ID] then
		return false
	end
	local nameRef = lNormalizeDisplayRef(name, session_id)
	if not nameRef then
		return false
	end
	delay_h = tonumber(delay_h) or RIS_FIELD_NOTE_DELAY_H
	lEnqueue(st, {
		key = "obit_" .. obit_key,
		kind = "obit",
		email_id = RIS_NPC_OBIT_ID,
		obit_key = obit_key,
		ready_at = lNow() + delay_h * lHour(),
		name_ref = nameRef,
	})
	return true
end

--- LoadGame / awake: queue missing current brief (delayed), do not dump a pack.
function JAZZ_RIS_CatchUpBriefs()
	local st = lState()
	if not st then
		return
	end
	JAZZ_RIS_EnsureStartupQueue()
	local getTier = rawget(_G, "JAZZ_GetLegionTier")
	local current = type(getTier) == "function" and tonumber(getTier()) or false
	if not current then
		return
	end
	local last = tonumber(st.last_mailed_tier) or 0
	if current > last or (current == last and not lHasAnyLegionBriefMail()) then
		if current == last and not lHasAnyLegionBriefMail() then
			st.last_mailed_tier = 0
		end
		-- Old save jumped ahead: one brief for current, eligible after baseline delay from awake.
		local emailId, tier = lResolveBriefEmail(current)
		if emailId and (tonumber(st.last_mailed_tier) or 0) < tier then
			local awake = lEnsureAwake(st)
			local ready = Max(awake + RIS_BASELINE_BRIEF_DELAY_H * lHour(), lNow())
			-- If already past baseline window, still respect desk spacing via queue (ready now).
			if last > 0 and current > last then
				ready = lNow() + RIS_RAISE_BRIEF_DELAY_H * lHour()
			end
			lEnqueue(st, {
				key = "brief_" .. tostring(tier),
				kind = "brief",
				email_id = emailId,
				tier = tier,
				ready_at = ready,
			})
		end
	end
end

function JAZZ_RIS_OnWelcomeRead()
	local st = lState()
	if st then
		st.welcome_read = true
		st.welcome_sent = true
	end
	JAZZ_RIS_ApplyTabLock()
	lAskStrategyObserver(false)
	local dockBrowserTab = rawget(_G, "DockBrowserTab")
	if type(dockBrowserTab) == "function" then
		dockBrowserTab("ris")
	end
end

local function lMaybeUnlock(uniqueId)
	local getReceivedEmail = rawget(_G, "GetReceivedEmail")
	local mail = type(getReceivedEmail) == "function" and getReceivedEmail(uniqueId)
	if not mail or mail == rawget(_G, "empty_table") then
		return
	end
	if mail.id == RIS_WELCOME_ID and mail.read then
		JAZZ_RIS_OnWelcomeRead()
	end
end

local function lInstallMarkEmailWrap()
	local netSyncEvents = rawget(_G, "NetSyncEvents")
	if type(netSyncEvents) ~= "table" or type(netSyncEvents.MarkEmailAsRead) ~= "function" then
		return
	end
	if rawget(_G, "g_JAZZ_RIS_MarkEmailWrapped")
		and netSyncEvents.MarkEmailAsRead == rawget(_G, "g_JAZZ_RIS_MarkEmailFn")
	then
		return
	end
	rawset(_G, "g_JAZZ_RIS_MarkEmailBase", netSyncEvents.MarkEmailAsRead)
	local base = rawget(_G, "g_JAZZ_RIS_MarkEmailBase")
	local function wrap(uniqueId, val)
		base(uniqueId, val)
		if val then
			lMaybeUnlock(uniqueId)
		end
	end
	rawset(_G, "g_JAZZ_RIS_MarkEmailFn", wrap)
	netSyncEvents.MarkEmailAsRead = wrap
	rawset(_G, "g_JAZZ_RIS_MarkEmailWrapped", true)
end

local function lEnsureRisTabData()
	local tabData = rawget(_G, "PDABrowserTabData")
	if type(tabData) ~= "table" then
		return
	end
	if not table.find(tabData, "id", "ris") then
		local aimIdx = table.find(tabData, "id", "aim") or 1
		local ameIdx = table.find(tabData, "id", "ame")
		local insertAt = (ameIdx or aimIdx) + 1
		table.insert(tabData, insertAt, {
			id = "ris",
			DisplayName = T(890000000006920, "R.I.S."),
		})
	end
	local browser = rawget(_G, "PDABrowser")
	if browser then
		browser.InternalModes = table.concat(table.map(tabData, "id"), ", ")
	end
end

function OnMsg.DataLoaded()
	JAZZ_RIS_MigrateState()
	lInstallMarkEmailWrap()
	lEnsureRisTabData()
	if rawget(_G, "JAZZ_RIS_InstallBrowser") then
		JAZZ_RIS_InstallBrowser()
	end
	JAZZ_RIS_ApplyTabLock()
end

function OnMsg.ModsReloaded()
	JAZZ_RIS_MigrateState()
	lInstallMarkEmailWrap()
	lEnsureRisTabData()
	if rawget(_G, "JAZZ_RIS_InstallBrowser") then
		JAZZ_RIS_InstallBrowser()
	end
	JAZZ_RIS_ApplyTabLock()
end

function OnMsg.NewGame()
	DelayedCall(0, function()
		JAZZ_RIS_MigrateState()
		local st = lState()
		if st then
			st.mod_awake_at = lNow()
			st.welcome_sent = false
			st.welcome_read = false
			st.last_mailed_tier = 0
			st.mail_queue = {}
			st.next_dispatch_at = 0
			st.welcome_due_at = false
			st.strategy_observed = {}
			st.strategy_delivered = {}
			st.strategy_delivery_order = {}
			st.next_strategy_at = 0
			st.strategy_catchup_done = false
			st.strategy_major_delivery_baseline = {}
			st.schema_version = math.max(
				tonumber(st.schema_version) or RIS_STATE_SCHEMA,
				RIS_STATE_SCHEMA
			)
		end
		JAZZ_RIS_EnsureStartupQueue()
		JAZZ_RIS_ApplyTabLock()
	end)
end

function OnMsg.LoadGame()
	DelayedCall(0, function()
		JAZZ_RIS_MigrateState()
		JAZZ_RIS_EnsureStartupQueue()
		JAZZ_RIS_CatchUpBriefs()
		JAZZ_RIS_ProcessMailQueue(true)
		JAZZ_RIS_ApplyTabLock()
	end)
end

function OnMsg.CombatEnd()
	local delayed = rawget(_G, "DelayedCall")
	if type(delayed) == "function" then
		delayed(0, JAZZ_RIS_ProcessMailQueue, false)
	else
		JAZZ_RIS_ProcessMailQueue(false)
	end
end

function OnMsg.SatelliteTick()
	JAZZ_RIS_ProcessMailQueue()
end

function OnMsg.OpenSatelliteView()
	JAZZ_RIS_ProcessMailQueue()
end
