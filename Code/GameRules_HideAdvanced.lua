-- Hide all vanilla Advanced Game Rules from New Game / Options.
-- Rules stay in GameRuleDefs so IsGameRuleActive still works for old saves;
-- players cannot enable them on a new run under JAZZ.

function OnMsg.DataLoaded()
	ForEachPreset("GameRuleDef", function(rule)
		if rule.advanced then
			rule.show_in_new_game = false
			rule.option = false
		end
	end)
end

-- PROGRESSION-001. Hidden engine rules provide native save/lobby serialization;
-- two cycling rows expose mutually exclusive choices instead of 13 checkboxes.
local START_TIERS = { 11, 12, 13, 21, 22, 23, 24, 25, 31, 32, 33 }
local CLOCK_SPEEDS = { 0, 1, 2, 4 }
local START_TITLE = T(718927001001, "Starting world tier")
local CLOCK_TITLE = T(718927001002, "Tier progression")
local START_HELP = T(718927001003, "Choose the initial Legion tier for the whole world. Equipment and all strategic systems linked to this tier start at the selected level. This does not complete quests or grant money or mercenary equipment. Click to cycle through tiers.")
local CLOCK_HELP = T(718927001004, "Campaign uses the usual mainland, mine and story milestones. Timed modes advance through every tier up to T3-3 without those milestones. At x1, each step takes 7 days in T1 and 30 in T2/T3 with JAZZ Maps, or 3 and 14 days without maps. x2 and x4 shorten these intervals. The next step starts counting from your chosen tier. Click to cycle through modes.")
local CLOCK_NAMES = {
	[0] = T(718927001005, "Campaign"),
	[1] = T(718927001006, "Timed x1"),
	[2] = T(718927001007, "Timed x2"),
	[4] = T(718927001008, "Timed x4"),
}

local function lEditable()
	return not Game and NewGameObj and (not netInGame or NetIsHost())
end

local function lUpdateChoice(self)
	local rules = (Game or NewGameObj or empty_table).game_rules or empty_table
	local start, speed = JAZZ_GetLegionCampaignSettings(rules)
	local is_start = self.Id == "idJAZZ_LegionStart"
	self.idName:SetText(is_start and START_TITLE or CLOCK_TITLE)
	self.idOnOff:SetText(is_start and Untranslated(string.format("T%d-%d", math.floor(start / 10), start % 10)) or CLOCK_NAMES[speed])
	self:SetRolloverTitle(is_start and START_TITLE or CLOCK_TITLE)
	self:SetRolloverText(is_start and START_HELP or CLOCK_HELP)
	self:SetEnabled(not not lEditable())
end

local function lChooseNext(self)
	if not lEditable() then return end
	local rules = NewGameObj.game_rules
	local start, speed = JAZZ_GetLegionCampaignSettings(rules)
	local is_start = self.Id == "idJAZZ_LegionStart"
	local choices = is_start and START_TIERS or CLOCK_SPEEDS
	local value = is_start and start or speed
	local prefix = is_start and "JAZZ_LegionStart" or "JAZZ_LegionClock"
	local index = table.find(choices, value) or 1
	for _, option in ipairs(choices) do rules[prefix .. option] = nil end
	local next_value = choices[index % #choices + 1]
	-- Absence means the unmodified default, also for old saves and quick starts.
	if next_value ~= choices[1] then rules[prefix .. next_value] = true end
	lUpdateChoice(self)
	if netInGame and NetIsHost() then
		local context = GetDialog(self):ResolveId("node").idSubMenu.context
		CreateRealTimeThread(function(player_id)
			NetCall("rfnPlayerMessage", player_id, "lobby-info", { start_info = NewGameObj, no_scroll = true })
		end, context and context.invited_player_id)
	end
end

local function lInstallLegionChoices()
	if not rawget(_G, "GameRuleDefs") or not rawget(_G, "XTemplates") then return end
	for _, group in ipairs({ { "JAZZ_LegionStart", START_TIERS }, { "JAZZ_LegionClock", CLOCK_SPEEDS } }) do
		for i = 2, #group[2] do
			local id = group[1] .. group[2][i]
			if not GameRuleDefs[id] then
				PlaceObj("GameRuleDef", { id = id, group = "Default", show_in_new_game = false, option = false })
			end
		end
	end
	local template = XTemplates.NewGameMenuGameRules
	if not template then return end
	for _, entry in ipairs(template) do
		if entry.Id == "idJAZZ_LegionStart" then return end
	end
	-- Insert ahead of Advanced Rules; retain the existing templates and style.
	for i, id in ipairs({ "idJAZZ_LegionStart", "idJAZZ_LegionClock" }) do
		table.insert(template, 2 + i, PlaceObj("XTemplateTemplate", {
			"__template", "NewGameBoolEntry",
			"__context", function() return {} end,
			"Id", id,
			"IdNode", true,
			"OnContextUpdate", lUpdateChoice,
			"OnPress", lChooseNext,
		}))
	end
end

function OnMsg.DataLoaded()
	lInstallLegionChoices()
end

function OnMsg.ModsReloaded()
	lInstallLegionChoices()
end
