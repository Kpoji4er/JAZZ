-- R.I.S. Phase B PDA site: Bulletin / Dossiers / Battle reports (JAZZ-UI-RIS-001).

g_JAZZ_RIS_BrowserInstalled = rawget(_G, "g_JAZZ_RIS_BrowserInstalled") or false
g_JAZZ_RIS_Section = rawget(_G, "g_JAZZ_RIS_Section") or "bulletin"

local function lUI()
	return rawget(_G, "JAZZ_RIS_UI") or empty_table
end

local function lState()
	return rawget(_G, "gv_JAZZ_RIS")
end

local function lThreshold()
	return rawget(_G, "JAZZ_RIS_KILL_THRESHOLD") or 3
end

function JAZZ_RIS_SetSection(section)
	rawset(_G, "g_JAZZ_RIS_Section", section or "bulletin")
	ObjModified("jazz_ris")
end

--- Walk UI tree for Id (ResolveId often misses nested XText under XScrollArea).
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
	if type(_InternalTranslate) == "function" then
		return _InternalTranslate(t)
	end
	return tostring(t)
end

function JAZZ_RIS_BuildBulletinText()
	local ui = lUI()
	local lines = {}
	lines[#lines + 1] = lTranslate(ui.supply_header)
	lines[#lines + 1] = ""
	local latest
	if type(GetReceivedEmails) == "function" then
		for _, email in ipairs(GetReceivedEmails()) do
			if type(email.id) == "string" and string.match(email.id, "^RIS_LegionBrief_") then
				latest = email
				break
			end
		end
	end
	if latest and Emails and Emails[latest.id] then
		local preset = Emails[latest.id]
		lines[#lines + 1] = lTranslate(preset.title)
		lines[#lines + 1] = ""
		lines[#lines + 1] = lTranslate(preset.body)
	else
		lines[#lines + 1] = lTranslate(ui.empty_bulletin)
	end
	lines[#lines + 1] = ""
	lines[#lines + 1] = lTranslate(ui.mail_archive)
	lines[#lines + 1] = ""
	local any = false
	if type(GetReceivedEmails) == "function" then
		for _, email in ipairs(GetReceivedEmails()) do
			if type(email.id) == "string" and string.match(email.id, "^RIS_") then
				any = true
				local preset = Emails and Emails[email.id]
				local title = preset and lTranslate(preset.title) or email.id
				local mark = email.read and "[x]" or "[ ]"
				lines[#lines + 1] = string.format("%s %s", mark, title)
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
	local quest = rawget(_G, "JAZZ_RIS_QUEST_DOSSIERS") or empty_table
	for id, card in sorted_pairs(quest) do
		local unlocked = st and st.quest_met and st.quest_met[id]
		if id == "Legion" then
			unlocked = unlocked or (st and next(st.kills or empty_table))
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
	local bank = rawget(_G, "JAZZ_RIS_DOSSIERS") or empty_table
	local thresh = lThreshold()
	for id, card in sorted_pairs(bank) do
		local kills = st and st.kills and (tonumber(st.kills[id]) or 0) or 0
		local unlocked = (st and st.dossiers and st.dossiers[id])
			or (st and st.met_types and st.met_types[id])
			or kills >= thresh
		if unlocked then
			any = true
			lines[#lines + 1] = lTranslate(card.title)
			lines[#lines + 1] = lTranslate(card.body)
			lines[#lines + 1] = ""
		elseif kills > 0 then
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

function JAZZ_RIS_BuildReportsText()
	local ui = lUI()
	local st = lState()
	if not st or type(st.battles) ~= "table" or #st.battles == 0 then
		return lTranslate(ui.empty_reports)
	end
	local lines = {}
	for _, battle in ipairs(st.battles) do
		lines[#lines + 1] = tostring(battle.title or "")
		local meta = {}
		if battle.sector_name and battle.sector_name ~= "" then
			meta[#meta + 1] = tostring(battle.sector_name)
		elseif battle.sector then
			meta[#meta + 1] = tostring(battle.sector)
		end
		if battle.quest_linked and type(battle.quest_ids) == "table" and #battle.quest_ids > 0 then
			meta[#meta + 1] = "quest:" .. table.concat(battle.quest_ids, ",")
		elseif type(battle.quest_ids) == "table" and #battle.quest_ids > 0 then
			meta[#meta + 1] = "job:" .. table.concat(battle.quest_ids, ",")
		end
		if #meta > 0 then
			lines[#lines + 1] = "[" .. table.concat(meta, " | ") .. "]"
		end
		lines[#lines + 1] = ""
		lines[#lines + 1] = tostring(battle.body or "")
		lines[#lines + 1] = ""
		lines[#lines + 1] = "-----"
		lines[#lines + 1] = ""
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

local function lInjectRisMode()
	local pda = rawget(_G, "XTemplates") and XTemplates.PDABrowser
	if not pda then
		return
	end
	local function findRisMode(node, depth)
		if type(node) ~= "table" or depth > 14 then
			return false
		end
		if node.mode == "ris" then
			return node
		end
		for _, child in ipairs(node) do
			local found = findRisMode(child, depth + 1)
			if found then
				return found
			end
		end
		return false
	end
	-- Always replace the ris mode so OnPress / layout fixes apply on ModsReloaded.
	local existing = findRisMode(pda, 0)
	local function findModeHost(node, depth)
		if type(node) ~= "table" or depth > 14 then
			return false
		end
		for _, child in ipairs(node) do
			if type(child) == "table" and child.mode == "aim" then
				return node
			end
		end
		for _, child in ipairs(node) do
			local host = findModeHost(child, depth + 1)
			if host then
				return host
			end
		end
		return false
	end
	local host = findModeHost(pda, 0)
	if not host then
		return
	end
	if existing then
		local idx = table.find(host, existing)
		if idx then
			table.remove(host, idx)
		end
	end
	local ui = lUI()
	local mode = PlaceObj("XTemplateMode", {
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
					"Text", ui.site_title or T(890000000006920, "R.I.S."),
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
					"Text", ui.tab_bulletin or T(890000000006920, "Bulletin"),
					"Margins", box(0, 0, 8, 0),
					"OnPress", function(self)
						JAZZ_RIS_RefreshPage(self, "bulletin")
					end,
				}),
				PlaceObj("XTemplateWindow", {
					"__class", "XTextButton",
					"Translate", true,
					"Text", ui.tab_dossiers or T(890000000006920, "Dossiers"),
					"Margins", box(0, 0, 8, 0),
					"OnPress", function(self)
						JAZZ_RIS_RefreshPage(self, "dossiers")
					end,
				}),
				PlaceObj("XTemplateWindow", {
					"__class", "XTextButton",
					"Translate", true,
					"Text", ui.tab_reports or T(890000000006920, "Battle reports"),
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
			PlaceObj("XTemplateWindow", {
				"__class", "VirtualCursorManager",
				"Reason", "Browser",
			}),
		}),
	})
	table.insert(host, mode)
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
