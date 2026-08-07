-- R.I.S. Phase B PDA site: Bulletin / Dossiers / Battle reports (JAZZ-UI-RIS-001).

g_JAZZ_RIS_BrowserInstalled = rawget(_G, "g_JAZZ_RIS_BrowserInstalled") or false
g_JAZZ_RIS_Section = rawget(_G, "g_JAZZ_RIS_Section") or "bulletin"

local RIS_AAR_RECORD_VERSION = 2

local function lUI()
	return rawget(_G, "JAZZ_RIS_UI") or rawget(_G, "empty_table") or {}
end

local function lState()
	local migrate = rawget(_G, "JAZZ_RIS_MigrateState")
	if type(migrate) == "function" then
		return migrate()
	end
	return rawget(_G, "gv_JAZZ_RIS")
end

local function lThreshold()
	return rawget(_G, "JAZZ_RIS_KILL_THRESHOLD") or 3
end

function JAZZ_RIS_SetSection(section)
	rawset(_G, "g_JAZZ_RIS_Section", section or "bulletin")
	ObjModified("jazz_ris")
end

--- Walk UI/template trees for Id (ResolveId often misses nested XText under XScrollArea).
local function lFindWindowById(win, id, depth)
	depth = depth or 0
	if not win or type(win) ~= "table" or depth > 16 then
		return
	end
	if win.Id == id then
		return win
	end
	for _, child in ipairs(win) do
		local found = lFindWindowById(child, id, depth + 1)
		if found then
			return found
		end
	end
end

local function lFindNodeWithMode(node, mode, depth)
	depth = depth or 0
	if type(node) ~= "table" or depth > 14 then
		return false
	end
	if node.mode == mode then
		return node
	end
	for _, child in ipairs(node) do
		local found = lFindNodeWithMode(child, mode, depth + 1)
		if found then
			return found
		end
	end
	return false
end

--- Prefer the window that already hosts XTemplateMode entries (look for aim sibling).
local function lFindModeHost(node, depth)
	depth = depth or 0
	if type(node) ~= "table" or depth > 14 then
		return false
	end
	for _, child in ipairs(node) do
		if type(child) == "table" and child.mode == "aim" then
			return node
		end
	end
	for _, child in ipairs(node) do
		local host = lFindModeHost(child, depth + 1)
		if host then
			return host
		end
	end
	return false
end

local function lRisBrowserContent(btn)
	-- Button → HList (tabs) → idBrowserContent
	return btn and btn.parent and btn.parent.parent
end

function JAZZ_RIS_RefreshPage(btn, section)
	section = section or rawget(_G, "g_JAZZ_RIS_Section") or "bulletin"
	JAZZ_RIS_SetSection(section)
	local root = lRisBrowserContent(btn)
	if not root then
		return
	end
	local page = root.ResolveId and root:ResolveId("idRISPage")
	page = page or lFindWindowById(root, "idRISPage")
	if not page then
		local scroll = (root.ResolveId and root:ResolveId("idRISScroll")) or lFindWindowById(root, "idRISScroll")
		page = scroll and ((scroll.ResolveId and scroll:ResolveId("idRISPage")) or lFindWindowById(scroll, "idRISPage"))
	end
	if page and page.SetText then
		page:SetText(JAZZ_RIS_BuildPageText(section))
		if page.Invalidate then
			page:Invalidate()
		end
	end
end

local function lTranslate(t)
	if not t then
		return ""
	end
	if type(t) == "string" then
		return t
	end
	local translate = rawget(_G, "_InternalTranslate")
	if type(translate) == "function" then
		local ok, text = pcall(translate, t)
		if ok and text then
			return text
		end
	end
	return tostring(t)
end

local function lStrategyCard(material_id)
	local bank = rawget(_G, "JAZZ_RIS_STRATEGY")
	if type(bank) ~= "table" then
		return false
	end
	for _, card in pairs(bank) do
		if type(card) == "table" and card.design_id == material_id then
			return card
		end
	end
	return false
end

local function lAppendStrategyArchive(lines, st)
	if type(st) ~= "table"
		or type(st.strategy_delivered) ~= "table"
		or type(st.strategy_delivery_order) ~= "table"
	then
		return false
	end
	local cards = {}
	local seen = {}
	for _, material_id in ipairs(st.strategy_delivery_order) do
		if st.strategy_delivered[material_id] and not seen[material_id] then
			local card = lStrategyCard(material_id)
			if card and card.title and card.body then
				seen[material_id] = true
				cards[#cards + 1] = card
			end
		end
	end
	if #cards == 0 then
		return false
	end

	local extra = rawget(_G, "JAZZ_RIS_EXTRA")
	local heading = type(extra) == "table" and extra.strategy_heading
	if not heading then
		return false
	end
	lines[#lines + 1] = ""
	lines[#lines + 1] = lTranslate(heading)
	lines[#lines + 1] = ""
	for index, card in ipairs(cards) do
		lines[#lines + 1] = lTranslate(card.title)
		lines[#lines + 1] = ""
		lines[#lines + 1] = lTranslate(card.body)
		if index < #cards then
			lines[#lines + 1] = ""
		end
	end
	return true
end

function JAZZ_RIS_BuildBulletinText()
	local ui = lUI()
	local st = lState()
	local lines = {}
	local getReceivedEmails = rawget(_G, "GetReceivedEmails")
	local emails = rawget(_G, "Emails")
	lines[#lines + 1] = lTranslate(ui.supply_header)
	lines[#lines + 1] = ""
	local latest
	if type(getReceivedEmails) == "function" then
		for _, email in ipairs(getReceivedEmails()) do
			if type(email.id) == "string" and string.match(email.id, "^RIS_LegionBrief_") then
				latest = email
				break
			end
		end
	end
	if latest and type(emails) == "table" and emails[latest.id] then
		local preset = emails[latest.id]
		lines[#lines + 1] = lTranslate(preset.title)
		lines[#lines + 1] = ""
		lines[#lines + 1] = lTranslate(preset.body)
	else
		lines[#lines + 1] = lTranslate(ui.empty_bulletin)
	end
	lAppendStrategyArchive(lines, st)
	lines[#lines + 1] = ""
	lines[#lines + 1] = lTranslate(ui.mail_archive)
	lines[#lines + 1] = ""
	local any = false
	if type(getReceivedEmails) == "function" then
		for _, email in ipairs(getReceivedEmails()) do
			if type(email.id) == "string"
				and string.match(email.id, "^RIS_")
				and not string.match(email.id, "^RIS_MajorStrategy_")
			then
				local preset = type(emails) == "table" and emails[email.id]
				if preset and preset.title then
					any = true
					local title = preset.title
					if type(email.context) == "table" then
						title = T{ preset.title, email.context }
					end
					local mark = email.read and "[x]" or "[ ]"
					lines[#lines + 1] = string.format("%s %s", mark, lTranslate(title))
				end
			end
		end
	end
	if not any then
		lines[#lines + 1] = lTranslate(ui.empty_bulletin)
	end
	return table.concat(lines, "\n")
end

function JAZZ_RIS_BuildDossiersText()
	local ui = lUI()
	local st = lState()
	local lines = {}
	local any = false
	lines[#lines + 1] = lTranslate(ui.section_quest)
	lines[#lines + 1] = ""
	local empty = rawget(_G, "empty_table") or {}
	local quest = rawget(_G, "JAZZ_RIS_QUEST_DOSSIERS") or empty
	for id, card in sorted_pairs(quest) do
		local unlocked = st and st.quest_met and st.quest_met[id]
		if id == "Legion" then
			unlocked = unlocked or (st and next(st.kills or empty))
		end
		if unlocked then
			any = true
			lines[#lines + 1] = lTranslate(card.title)
			lines[#lines + 1] = lTranslate(card.body)
			lines[#lines + 1] = ""
		end
	end
	lines[#lines + 1] = lTranslate(ui.section_legion)
	lines[#lines + 1] = ""
	local bank = rawget(_G, "JAZZ_RIS_DOSSIERS") or empty
	local thresh = lThreshold()
	for id, card in sorted_pairs(bank) do
		local kills = st and st.kills and (tonumber(st.kills[id]) or 0) or 0
		local full = kills >= thresh
		local met = st and st.met_types and st.met_types[id]
		if met and full then
			any = true
			lines[#lines + 1] = lTranslate(card.title)
			lines[#lines + 1] = lTranslate(card.body)
			lines[#lines + 1] = ""
		elseif met then
			any = true
			local prog = T{ ui.kills_progress, count = tostring(kills) }
			lines[#lines + 1] = string.format("%s — %s", lTranslate(card.title), lTranslate(prog))
			lines[#lines + 1] = lTranslate(ui.dossier_locked)
			lines[#lines + 1] = ""
		end
	end
	if not any then
		return lTranslate(ui.empty_dossiers)
	end
	return table.concat(lines, "\n")
end

local function lIsStableT(value)
	local isT = rawget(_G, "IsT")
	if type(isT) == "function" then
		return isT(value)
	end
	return type(value) == "table" and type(value[1]) == "number"
end

local function lFormat(template, values)
	if not template then
		return false
	end
	local makeT = rawget(_G, "T")
	if type(makeT) ~= "function" then
		return template
	end
	local args = { template }
	for key, value in pairs(type(values) == "table" and values or {}) do
		args[key] = value
	end
	return makeT(args)
end

local function lAppendParagraph(parts, text)
	text = lTranslate(text)
	if text == "" then
		return
	end
	if #parts > 0 then
		parts[#parts + 1] = ""
	end
	parts[#parts + 1] = text
end

local function lBattleSectorId(entry)
	return type(entry) == "table" and (entry.sector_id or entry.sector) or false
end

local function lResolveSectorName(entry)
	local sectorId = lBattleSectorId(entry)
	if not sectorId then
		return ""
	end
	local sectors = rawget(_G, "gv_Sectors")
	local sector = type(sectors) == "table" and sectors[sectorId]
	local getSectorName = rawget(_G, "GetSectorName")
	if sector and type(getSectorName) == "function" then
		local ok, name = pcall(getSectorName, sector)
		if ok then
			name = lTranslate(name)
			if name ~= "" then
				return name
			end
		end
	end
	-- The sector grid code is the only allowed player-facing raw-id fallback.
	return tostring(sectorId)
end

local function lResolvePoi(entry)
	if not lIsStableT(entry and entry.poi_ref) then
		return false
	end
	local poi = lTranslate(entry.poi_ref)
	return poi ~= "" and poi or false
end

local function lResolveQuestRows(entry)
	local ids = type(entry.quest_ids) == "table" and entry.quest_ids or {}
	local presets = rawget(_G, "Quests")
	local rows = {}
	if type(presets) ~= "table" then
		return rows, #ids
	end
	for index, id in ipairs(ids) do
		local preset = presets[id]
		local display = preset and (preset.DisplayName or preset.display_name)
		if lIsStableT(display) then
			local name = lTranslate(display)
			if name ~= "" then
				local sources = type(entry.quest_sources) == "table" and entry.quest_sources or {}
				local notes = type(entry.quest_notes) == "table" and entry.quest_notes or {}
				rows[#rows + 1] = {
					name = name,
					source = sources[id] or sources[index],
					note = lIsStableT(notes[id] or notes[index]) and lTranslate(notes[id] or notes[index])
						or false,
				}
			end
		end
	end
	return rows, #ids
end

local function lAppendSector(parts, aar, entry)
	if type(aar.sector) ~= "table" then
		return
	end
	local sector = lResolveSectorName(entry)
	if sector == "" then
		return
	end
	local poi = lResolvePoi(entry)
	if poi and aar.sector.poi then
		lAppendParagraph(parts, lFormat(aar.sector.poi, { sector = sector, poi = poi }))
	elseif aar.sector.line then
		lAppendParagraph(parts, lFormat(aar.sector.line, { sector = sector }))
	end
end

local function lAppendQuest(parts, aar, entry)
	if type(aar.quest) ~= "table" then
		return
	end
	local rows, rawCount = lResolveQuestRows(entry)
	if rawCount == 0 then
		lAppendParagraph(parts, aar.quest.none)
		return
	end
	-- IDs without a currently available DisplayName are intentionally omitted.
	if #rows == 0 then
		return
	end
	if #rows == 1 then
		local row = rows[1]
		if row.source == "active" and not entry.quest_linked then
			lAppendParagraph(parts, lFormat(aar.quest.active, { quest = row.name }))
		elseif row.note and row.note ~= "" then
			lAppendParagraph(parts, lFormat(aar.quest.one, { quest = row.name, note = row.note }))
		else
			lAppendParagraph(parts, lFormat(aar.quest.one_nonote, { quest = row.name }))
		end
		return
	end
	local names = {}
	for _, row in ipairs(rows) do
		names[#names + 1] = row.name
	end
	lAppendParagraph(parts, lFormat(aar.quest.many, { quests = table.concat(names, "; ") }))
end

local function lDisplayRefText(value, row)
	if lIsStableT(value) then
		local text = lTranslate(value)
		return text ~= "" and text or false
	end
	if type(value) == "string"
		and value ~= ""
		and value ~= row.session_id
		and value ~= row.unit_id
		and value ~= tostring(row.handle or "")
	then
		return value
	end
	return false
end

local function lResolveEliteName(row)
	local stored = row.name_ref or row.name
	local name = lIsStableT(stored) and lDisplayRefText(stored, row) or false
	if name then
		return name
	end
	local id = row.session_id or row.unit_id
	local unitData = rawget(_G, "gv_UnitData")
	local unit = type(unitData) == "table" and id and unitData[id]
	if unit then
		name = lDisplayRefText((unit.Nick ~= "" and unit.Nick) or unit.Name, row)
		if name then
			return name
		end
	end
	local classes = rawget(_G, "g_Classes")
	local class = type(classes) == "table" and row.unit_id and classes[row.unit_id]
	if class then
		name = lDisplayRefText((class.Nick ~= "" and class.Nick) or class.Name, row)
		if name then
			return name
		end
	end
	-- Last resort for unique proper names that never had a localization reference.
	return lDisplayRefText(stored, row)
end

local function lAppendElites(parts, aar, entry)
	if type(aar.elite) ~= "table" or type(entry.elites) ~= "table" then
		return
	end
	local rows = {}
	for _, row in ipairs(entry.elites) do
		if type(row) == "table" then
			rows[#rows + 1] = row
		end
	end
	table.sort(rows, function(a, b)
		return tostring(a.handle or "") < tostring(b.handle or "")
	end)
	for _, row in ipairs(rows) do
		local name = lResolveEliteName(row)
		local template = aar.elite[row.fate or "threat"] or aar.elite.threat
		if name and template then
			lAppendParagraph(parts, lFormat(template, { name = name }))
		end
	end
end

local function lResolveHeadline(aar, entry)
	if type(aar.headlines) ~= "table" then
		return false
	end
	local key = entry.headline_key
	if type(key) ~= "string" then
		key = tostring(entry.outcome or "win") .. "|" .. tostring(entry.intensity_key or "mid")
	end
	local bank = aar.headlines[key] or aar.headlines["win|mid"]
	if type(bank) ~= "table" or #bank == 0 then
		return false
	end
	local index = tonumber(entry.headline_index) or 1
	index = ((math.max(1, math.floor(index)) - 1) % #bank) + 1
	return bank[index]
end

local function lRenderLegacyBattle(entry)
	local extra = rawget(_G, "JAZZ_RIS_EXTRA")
	if type(extra) ~= "table" then
		return "", ""
	end
	local aar = rawget(_G, "JAZZ_RIS_AAR")
	local outcome = entry.outcome
	if outcome ~= "win" and outcome ~= "loss" and outcome ~= "retreat" then
		outcome = entry.isRetreat and "retreat"
			or (entry.playerWon == true and "win")
			or (entry.playerWon == false and "loss")
			or false
	end
	local title = extra.legacy_title
	if outcome and type(aar) == "table" then
		title = lResolveHeadline(aar, {
			outcome = outcome,
			headline_key = outcome .. "|mid",
			headline_index = 1,
		}) or title
	end
	local sector = lResolveSectorName(entry)
	local parts = {}
	lAppendParagraph(parts, lFormat(extra.legacy_body, { sector = sector }))
	if type(aar) == "table" then
		lAppendQuest(parts, aar, entry)
		if entry.player_start ~= nil and entry.enemy_start ~= nil then
			lAppendParagraph(parts, lFormat(aar.forces, {
				player = tostring(tonumber(entry.player_start) or 0),
				enemy = tostring(tonumber(entry.enemy_start) or 0),
			}))
		end
		if outcome then
			local character = type(aar.character) == "table"
				and (aar.character[outcome] or aar.character.win)
			lAppendParagraph(parts, character)
		end
		if entry.player_kia ~= nil
			and entry.player_wia ~= nil
			and entry.enemy_kia ~= nil
			and entry.enemy_wia ~= nil
		then
			lAppendParagraph(parts, lFormat(aar.losses, {
				pkia = tostring(tonumber(entry.player_kia) or 0),
				pwia = tostring(tonumber(entry.player_wia) or 0),
				ekia = tostring(tonumber(entry.enemy_kia) or 0),
				ewia = tostring(tonumber(entry.enemy_wia) or 0),
			}))
		end
		if entry.autoResolve or entry.auto_resolve then
			lAppendParagraph(parts, extra.auto_resolve)
		end
	end
	return lTranslate(title), table.concat(parts, "\n")
end

--- Render one language-neutral AAR snapshot in the currently selected language.
function JAZZ_RIS_RenderBattle(entry)
	if type(entry) ~= "table" then
		return "", ""
	end
	local version = tonumber(entry.record_version or entry.version) or 0
	if entry.legacy or entry.kind == "legacy" or version < RIS_AAR_RECORD_VERSION then
		return lRenderLegacyBattle(entry)
	end
	local aar = rawget(_G, "JAZZ_RIS_AAR")
	if type(aar) ~= "table" then
		return lRenderLegacyBattle(entry)
	end
	local headline = lResolveHeadline(aar, entry)
	if not headline then
		return lRenderLegacyBattle(entry)
	end

	local parts = {}
	lAppendSector(parts, aar, entry)
	lAppendQuest(parts, aar, entry)
	local weather = type(aar.weather) == "table"
		and (aar.weather[entry.weather_key] or aar.weather.default)
	lAppendParagraph(parts, weather)
	local intensity = type(aar.intensity) == "table"
		and (aar.intensity[entry.intensity_key] or aar.intensity.mid)
	lAppendParagraph(parts, intensity)
	lAppendParagraph(parts, lFormat(aar.forces, {
		player = tostring(tonumber(entry.player_start) or 0),
		enemy = tostring(tonumber(entry.enemy_start) or 0),
	}))

	local extra = rawget(_G, "JAZZ_RIS_EXTRA")
	if entry.hostiles_remain then
		lAppendParagraph(parts, type(extra) == "table" and extra.hostiles_remain or false)
	else
		local character = type(aar.character) == "table"
			and (aar.character[entry.character_key] or aar.character[entry.outcome] or aar.character.win)
		lAppendParagraph(parts, character)
	end
	lAppendParagraph(parts, lFormat(aar.losses, {
		pkia = tostring(tonumber(entry.player_kia) or 0),
		pwia = tostring(tonumber(entry.player_wia) or 0),
		ekia = tostring(tonumber(entry.enemy_kia) or 0),
		ewia = tostring(tonumber(entry.enemy_wia) or 0),
	}))
	if entry.autoResolve or entry.auto_resolve then
		lAppendParagraph(parts, type(extra) == "table" and extra.auto_resolve or false)
	end
	lAppendElites(parts, aar, entry)
	local closing = type(aar.closing) == "table"
		and (aar.closing[entry.closing_key] or aar.closing.noise)
	lAppendParagraph(parts, closing)
	return lTranslate(headline), table.concat(parts, "\n")
end

function JAZZ_RIS_BuildReportsText()
	local ui = lUI()
	local st = lState()
	if not st or type(st.battles) ~= "table" or #st.battles == 0 then
		return lTranslate(ui.empty_reports)
	end
	local lines = {}
	for _, battle in ipairs(st.battles) do
		local title, body = JAZZ_RIS_RenderBattle(battle)
		if title ~= "" or body ~= "" then
			lines[#lines + 1] = title
			lines[#lines + 1] = ""
			lines[#lines + 1] = body
			lines[#lines + 1] = ""
			lines[#lines + 1] = "-----"
			lines[#lines + 1] = ""
		end
	end
	if #lines == 0 then
		return lTranslate(ui.empty_reports)
	end
	return table.concat(lines, "\n")
end

function JAZZ_RIS_BuildPageText(section)
	section = section or rawget(_G, "g_JAZZ_RIS_Section") or "bulletin"
	if section == "dossiers" then
		return JAZZ_RIS_BuildDossiersText()
	end
	if section == "reports" then
		return JAZZ_RIS_BuildReportsText()
	end
	return JAZZ_RIS_BuildBulletinText()
end

local function lBuildRisModeTemplate()
	local ui = lUI()
	return PlaceObj("XTemplateMode", {
		"mode", "ris",
	}, {
		PlaceObj("XTemplateWindow", {
			"Id", "idBrowserContent",
			"IdNode", true,
			"LayoutMethod", "VList",
			"Padding", box(16, 16, 16, 16),
			"Background", RGBA(18, 28, 36, 220),
		}, {
			PlaceObj("XTemplateWindow", {
				"LayoutMethod", "HList",
				"HAlign", "center",
				"Margins", box(0, 0, 0, 12),
			}, {
				PlaceObj("XTemplateWindow", {
					"__class", "XImage",
					"Image", "Mod/e6L4ECj/Icons/PDA/RIS_Mark.png",
					"ImageFit", "smallest",
					"MinWidth", 96,
					"MinHeight", 104,
					"MaxWidth", 96,
					"MaxHeight", 104,
					"Margins", box(0, 0, 16, 0),
				}),
				PlaceObj("XTemplateWindow", {
					"__class", "XText",
					"Translate", true,
					"TextStyle", "PDABrowserText",
					"Text", ui.site_title or T(890000000011000, "Recon Intelligence Services"),
					"VAlign", "center",
				}),
			}),
			PlaceObj("XTemplateWindow", {
				"LayoutMethod", "HList",
				"HAlign", "center",
				"Margins", box(0, 0, 0, 10),
			}, {
				PlaceObj("XTemplateWindow", {
					"__class", "XTextButton",
					"Translate", true,
					"Text", ui.tab_bulletin or T(890000000011001, "Field bulletin"),
					"Margins", box(0, 0, 8, 0),
					"OnPress", function(self)
						JAZZ_RIS_RefreshPage(self, "bulletin")
					end,
				}),
				PlaceObj("XTemplateWindow", {
					"__class", "XTextButton",
					"Translate", true,
					"Text", ui.tab_dossiers or T(890000000011002, "Dossiers"),
					"Margins", box(0, 0, 8, 0),
					"OnPress", function(self)
						JAZZ_RIS_RefreshPage(self, "dossiers")
					end,
				}),
				PlaceObj("XTemplateWindow", {
					"__class", "XTextButton",
					"Translate", true,
					"Text", ui.tab_reports or T(890000000011003, "After-action reports"),
					"OnPress", function(self)
						JAZZ_RIS_RefreshPage(self, "reports")
					end,
				}),
			}),
			PlaceObj("XTemplateWindow", {
				"__class", "XScrollArea",
				"Id", "idRISScroll",
				"IdNode", true,
				"Width", 900,
				"MaxHeight", 520,
				"HAlign", "center",
				"LayoutMethod", "VList",
				"VScroll", "idRISScrollBar",
			}, {
				PlaceObj("XTemplateWindow", {
					"__class", "XText",
					"Id", "idRISPage",
					"Translate", false,
					"TextStyle", "PDABrowserText",
					"TextHAlign", "left",
					"HandleMouse", false,
					"OnLayoutComplete", function(self)
						-- Only seed empty page; section switches use JAZZ_RIS_RefreshPage.
						if (self:GetText() or "") == "" then
							self:SetText(JAZZ_RIS_BuildPageText())
						end
					end,
				}),
			}),
			PlaceObj("XTemplateWindow", {
				"__class", "XScrollBar",
				"Id", "idRISScrollBar",
				"IdNode", false,
				"Dock", "right",
				"Target", "idRISScroll",
			}),
		}),
		-- PDA bottom ActionBar Close (same as AIM/AME modes).
		PlaceObj("XTemplateWindow", nil, {
			PlaceObj("XTemplateTemplate", {
				"__template", "PDAGenericCloseAction",
			}),
		}),
		PlaceObj("XTemplateWindow", {
			"__class", "VirtualCursorManager",
			"Reason", "Browser",
		}),
	})
end

local function lInjectRisMode()
	local templates = rawget(_G, "XTemplates")
	local pda = type(templates) == "table" and templates.PDABrowser
	if not pda then
		return
	end
	-- Always replace the ris mode so OnPress / layout fixes apply on ModsReloaded.
	local existing = lFindNodeWithMode(pda, "ris", 0)
	local host = lFindModeHost(pda, 0)
	if not host then
		return
	end
	if existing then
		local idx = table.find(host, existing)
		if idx then
			table.remove(host, idx)
		end
	end
	table.insert(host, lBuildRisModeTemplate())
	rawset(_G, "g_JAZZ_RIS_BrowserInstalled", true)
end

function JAZZ_RIS_InstallBrowser()
	lInjectRisMode()
end

function OnMsg.DataLoaded()
	JAZZ_RIS_InstallBrowser()
end

function OnMsg.ModsReloaded()
	-- Allow re-inject if template tree was rebuilt without ris mode.
	rawset(_G, "g_JAZZ_RIS_BrowserInstalled", false)
	JAZZ_RIS_InstallBrowser()
end
