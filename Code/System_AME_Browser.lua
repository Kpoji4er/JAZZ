-- AME PDA browser tab + PDAAIMEBrowser class (JAZZ-UNITS-005).
-- Declares wrap flags at file load; injects tab/mode after DataLoaded.

g_JAZZ_AME_BrowserInstalled = rawget(_G, "g_JAZZ_AME_BrowserInstalled") or false
g_JAZZ_MercCanContactBase = rawget(_G, "g_JAZZ_MercCanContactBase") or false
g_JAZZ_PDAUrlBase = rawget(_G, "g_JAZZ_PDAUrlBase") or false
g_JAZZ_AME_PDAUrlWrapped = rawget(_G, "g_JAZZ_AME_PDAUrlWrapped") or false
g_JAZZ_AME_PDAUrlFn = rawget(_G, "g_JAZZ_AME_PDAUrlFn") or false
g_JAZZ_AME_DockBase = rawget(_G, "g_JAZZ_AME_DockBase") or false
g_JAZZ_AME_DockFn = rawget(_G, "g_JAZZ_AME_DockFn") or false
g_JAZZ_AME_DockWrap = rawget(_G, "g_JAZZ_AME_DockWrap") or false -- legacy alias; prefer DockBase/DockFn

DefineClass.PDAAIMEBrowser = {
	__parents = { "PDAAIMBrowser" },
}

function PDAAIMEBrowser:Open()
	self.show_bio = AIMBrowserSection == "bio"
	XDialog.Open(self)
	local autoSelectMerc = false
	local mode_param = GetDialogModeParam(self.parent) or GetDialogModeParam(GetDialog("PDADialog")) or GetDialog("PDADialog").context
	if mode_param and mode_param.select_merc then
		autoSelectMerc = mode_param.select_merc
	end
	RunWhenXWindowIsReady(self, function()
		if self.window_state == "destroying" then return end
		self:SetFilter(CurrentAMEFilter or 5, autoSelectMerc)
		self.idMercList:SetFocus()
	end)
end

function PDAAIMEBrowser:SetFilter(id, auto_select)
	CurrentAMEFilter = id
	self.current_filter = id
	self:UpdateSelectedFilter()
	local mercToSelect
	if auto_select then
		mercToSelect = table.find_value(self.idMercList, "context", gv_UnitData[auto_select])
		mercToSelect = mercToSelect and mercToSelect.context
	end
	if not mercToSelect then
		mercToSelect = self.idMercList.context and self.idMercList.context[1]
	end
	self:SetSelectedMerc(mercToSelect and mercToSelect.session_id)
	if not (auto_select and mercToSelect) then
		self.idMercList:ScrollTo(0, 0)
	end
	ObjModified("pda_url")
end

function PDAAIMEBrowser:UpdateSelectedFilter()
	local mercsPerFilter = {}
	local filterContainer = self:ResolveId("idFilters")
	local buttonIdx = 1
	for i, f in ipairs(filterContainer) do
		if IsKindOf(f, "XTextButton") then
			local list = GetFilteredAMEMercs(buttonIdx)
			local enabled = #list > 0
			f:SetEnabled(enabled)
			local shouldBeSelected = buttonIdx == self.current_filter
			f:SetSelected(enabled and shouldBeSelected)
			if not enabled and shouldBeSelected then
				local filterAll = table.find(GetAMEScreenFilters(), "nameString", "all")
				if buttonIdx ~= filterAll then
					self:SetFilter(filterAll)
				end
				break
			end
			mercsPerFilter[buttonIdx] = list
			buttonIdx = buttonIdx + 1
		end
	end
	self.idMercList.KeepSelectionOnRespawn = false
	self.idMercList:SetContext(mercsPerFilter[self.current_filter] or {})
	self.idMercList.KeepSelectionOnRespawn = true
end

function PDAAIMEBrowser:OnShortcut(shortcut, ...)
	if shortcut == "LeftShoulder" or shortcut == "RightShoulder" then
		local currentFilter = self.current_filter
		if shortcut == "LeftShoulder" then
			currentFilter = currentFilter - 1
		else
			currentFilter = currentFilter + 1
		end
		local filtersArray = GetAMEScreenFilters()
		if currentFilter <= 0 then currentFilter = #filtersArray end
		if currentFilter > #filtersArray then currentFilter = 1 end
		local filterPreset = filtersArray[currentFilter]
		local filterButtonContainer = self.idFilters
		local filterButton = filterPreset and table.find_value(filterButtonContainer, "context", filterPreset)
		if IsKindOf(filterButton, "XTextButton") and filterButton.enabled then
			self:SetFilter(currentFilter)
		end
	end
	return XDialog.OnShortcut(self, shortcut, ...)
end

local function lEnsureAmeTabData()
	if not PDABrowserTabData then
		return
	end
	if not table.find(PDABrowserTabData, "id", "ame") then
		local aimIdx = table.find(PDABrowserTabData, "id", "aim") or 1
		table.insert(PDABrowserTabData, aimIdx + 1, {
			id = "ame",
			DisplayName = T(890000000005000, "A.M.E. Exchange"),
		})
	end
	if IsKindOf(PDABrowser, "PDABrowser") or rawget(_G, "PDABrowser") then
		PDABrowser.InternalModes = table.concat(table.map(PDABrowserTabData, "id"), ", ")
	end
end

local function lEnsureAmeTabState()
	if not PDABrowserTabState then
		return
	end
	if not PDABrowserTabState.ame then
		PDABrowserTabState.ame = { locked = false }
	else
		PDABrowserTabState.ame.locked = false
	end
	ObjModified("pda browser tabs")
end

local function lInjectAmeXTemplateMode()
	local pda = rawget(_G, "XTemplates") and XTemplates.PDABrowser
	if not pda then
		return
	end
	-- XTemplates.PDABrowser is a nested tree; find XContentTemplate children list.
	local function walk(node, depth)
		if type(node) ~= "table" or depth > 12 then
			return false
		end
		if node.mode == "ame" then
			return true
		end
		local kids = node
		if node[1] then
			for _, child in ipairs(node) do
				if walk(child, depth + 1) then
					return true
				end
			end
		end
		return false
	end
	if walk(pda, 0) then
		return
	end
	-- Append mode by cloning aim-mode structure if present.
	local function findContentTemplate(node, depth)
		if type(node) ~= "table" or depth > 12 then
			return false
		end
		if node.Id == "idBrowserContent" or (node.__class == "XContentTemplate") then
			return node
		end
		for _, child in ipairs(node) do
			local found = findContentTemplate(child, depth + 1)
			if found then
				return found
			end
		end
		-- also scan named fields
		for k, v in pairs(node) do
			if type(k) == "string" and type(v) == "table" then
				local found = findContentTemplate(v, depth + 1)
				if found then
					return found
				end
			end
		end
		return false
	end
	-- Prefer inserting into the window that already hosts XTemplateMode entries.
	local function findModeHost(node, depth)
		if type(node) ~= "table" or depth > 14 then
			return false
		end
		local hasAim = false
		for _, child in ipairs(node) do
			if type(child) == "table" and child.mode == "aim" then
				hasAim = true
				break
			end
		end
		if hasAim then
			return node
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
	local mode = PlaceObj("XTemplateMode", {
		"mode", "ame",
	}, {
		PlaceObj("XTemplateTemplate", {
			"__template", "PDAAIMEBrowser",
			"Id", "idBrowserContent",
		}),
		PlaceObj("XTemplateWindow", {
			"__class", "VirtualCursorManager",
			"Reason", "Browser",
		}),
	})
	table.insert(host, mode)
end

local function lInstallMercCanContactWrap()
	if rawget(_G, "g_JAZZ_MercCanContactBase") then
		return
	end
	local base = rawget(_G, "MercCanContact")
	if type(base) ~= "function" then
		return
	end
	rawset(_G, "g_JAZZ_MercCanContactBase", base)
	function MercCanContact(merc)
		if merc and merc.Affiliation == "AME" then
			if Platform.demo then
				return "disabled", T(697751324120, "Not available in Demo")
			end
			if merc.HireStatus == "Available" or merc.HireStatus == "Retired" then
				return "enabled"
			end
			if merc.HireStatus == "Dead" or merc.HireStatus == "MIA" then
				return false
			end
			if merc.HireStatus == "Hired" then
				if not merc.HiredUntil then
					return false
				end
				local mercContractLeft = merc.HiredUntil - Game.CampaignTime
				local leftInDays = mercContractLeft / const.Scale.day
				if leftInDays > 5 then
					return "TooEarly"
				end
				return "enabled"
			end
			return false
		end
		return g_JAZZ_MercCanContactBase(merc)
	end
end

local function lAmeUrlSlug(filter)
	if not filter then
		return "All"
	end
	if filter.urlSlug then
		return filter.urlSlug
	end
	local ns = filter.nameString
	if ns == "hired" then
		return "My%20Team"
	end
	if type(ns) == "string" and ns ~= "" then
		return ns:sub(1, 1):upper() .. ns:sub(2)
	end
	return "All"
end

local function lAmeUrlNick(unit_id)
	local ud = unit_id and gv_UnitData[unit_id]
	if not ud then
		return tostring(unit_id or "")
	end
	-- Prefer engine Nick resolve; fall back to session id (ASCII).
	local nick = ud.Nick
	if nick and type(_InternalTranslate) == "function" then
		local ok, text = pcall(_InternalTranslate, nick)
		if ok and type(text) == "string" and text ~= "" then
			return text:gsub("%s+", "%%20")
		end
	end
	return tostring(ud.session_id or unit_id):gsub("%s+", "%%20")
end

local function lBuildAmePDAUrl(browserContent)
	local filters = GetAMEScreenFilters()
	local filter = filters[browserContent.current_filter]
	if not filter then
		return Untranslated("http://www.ame-exchange.net/")
	end
	local url = Untranslated("http://www.ame-exchange.net/Roster/") .. Untranslated(lAmeUrlSlug(filter))
	local selectedUnit = browserContent.selected_merc
	if selectedUnit then
		url = url .. Untranslated("/" .. lAmeUrlNick(selectedUnit))
	end
	return url
end

local function lInstallPDAUrlWrap()
	if not TFormat or type(TFormat.PDAUrl) ~= "function" then
		return false
	end
	-- Already outer wrapper and still hooked.
	if rawget(_G, "g_JAZZ_AME_PDAUrlWrapped") and TFormat.PDAUrl == rawget(_G, "g_JAZZ_AME_PDAUrlFn") then
		return true
	end
	local current = TFormat.PDAUrl
	local ourFn = rawget(_G, "g_JAZZ_AME_PDAUrlFn")
	-- Capture base only when current is not our wrap (avoid nesting).
	if current ~= ourFn then
		rawset(_G, "g_JAZZ_PDAUrlBase", current)
	elseif not rawget(_G, "g_JAZZ_PDAUrlBase") then
		return false
	end
	local function wrap(context_obj)
		local pda = GetDialog("PDADialog")
		if pda then
			local content = pda:ResolveId("idContent")
			local mercBrowser = IsKindOf(content, "PDABrowser") and content
			local browserContent = mercBrowser and mercBrowser.idBrowserContent
			-- Must check AME before falling through: PDAAIMEBrowser is KindOf PDAAIMBrowser.
			if IsKindOf(browserContent, "PDAAIMEBrowser") then
				return lBuildAmePDAUrl(browserContent)
			end
		end
		local base = g_JAZZ_PDAUrlBase
		if type(base) == "function" then
			return base(context_obj)
		end
		return Untranslated("http://www.ame-exchange.net/")
	end
	rawset(_G, "g_JAZZ_AME_PDAUrlFn", wrap)
	TFormat.PDAUrl = wrap
	rawset(_G, "g_JAZZ_AME_PDAUrlWrapped", true)
	return true
end

local function lInstallDockWrap()
	local ourFn = rawget(_G, "g_JAZZ_AME_DockFn")
	if ourFn and DockBrowserTab == ourFn then
		return true
	end
	local current = rawget(_G, "DockBrowserTab")
	if type(current) ~= "function" then
		return false
	end
	-- Capture vanilla/base only when current is not already our wrap (avoid nesting).
	if current ~= ourFn then
		rawset(_G, "g_JAZZ_AME_DockBase", current)
		-- Keep legacy name for any leftover callers / assert stacks.
		rawset(_G, "g_JAZZ_AME_DockWrap", current)
	elseif not rawget(_G, "g_JAZZ_AME_DockBase") then
		return false
	end
	local function wrap(tab)
		local base = g_JAZZ_AME_DockBase
		if type(base) ~= "function" then
			return
		end
		base(tab)
		-- Landing OnDelete restores only aim(+imp). Keep AME docked whenever AIM is.
		if tab == "aim" then
			base("ame")
		end
	end
	rawset(_G, "g_JAZZ_AME_DockFn", wrap)
	DockBrowserTab = wrap
	return true
end

local function lInstallAmeBrowser()
	lEnsureAmeTabData()
	lInjectAmeXTemplateMode()
	if not rawget(_G, "g_JAZZ_AME_BrowserInstalled") then
		lInstallMercCanContactWrap()
		rawset(_G, "g_JAZZ_AME_BrowserInstalled", true)
	end
	-- Always (re)assert wraps that can be wiped / nested on ModsReloaded.
	lInstallDockWrap()
	-- Always (re)assert PDAUrl wrap: PDAAIMEBrowser is KindOf PDAAIMBrowser, so a missing
	-- wrap falls through to AIM ActiveFiles + localized specialization names.
	lInstallPDAUrlWrap()
	lEnsureAmeTabState()
end

function OnMsg.ClassesPostprocess()
	lEnsureAmeTabData()
end

function OnMsg.DataLoaded()
	lInstallAmeBrowser()
	-- Template may register after first DataLoaded pass via ModItemXTemplate.
	lInjectAmeXTemplateMode()
end

function OnMsg.ModsReloaded()
	-- Unwrap before reinstall so we do not nest old wraps as base.
	local pdaFn = rawget(_G, "g_JAZZ_AME_PDAUrlFn")
	local pdaBase = rawget(_G, "g_JAZZ_PDAUrlBase")
	if TFormat and pdaFn and TFormat.PDAUrl == pdaFn and type(pdaBase) == "function" then
		TFormat.PDAUrl = pdaBase
	end
	local dockFn = rawget(_G, "g_JAZZ_AME_DockFn")
	local dockBase = rawget(_G, "g_JAZZ_AME_DockBase") or rawget(_G, "g_JAZZ_AME_DockWrap")
	if dockFn and DockBrowserTab == dockFn and type(dockBase) == "function" then
		DockBrowserTab = dockBase
	end
	rawset(_G, "g_JAZZ_AME_BrowserInstalled", false)
	rawset(_G, "g_JAZZ_AME_DockFn", false)
	rawset(_G, "g_JAZZ_AME_DockBase", false)
	rawset(_G, "g_JAZZ_AME_DockWrap", false)
	rawset(_G, "g_JAZZ_AME_PDAUrlWrapped", false)
	rawset(_G, "g_JAZZ_AME_PDAUrlFn", false)
	rawset(_G, "g_JAZZ_PDAUrlBase", false)
	lInstallAmeBrowser()
end

function OnMsg.NewGame()
	lEnsureAmeTabState()
	DockBrowserTab("ame")
end

function OnMsg.LoadGame()
	lEnsureAmeTabState()
	DockBrowserTab("ame")
end

function OnMsg.BrowserOpened()
	lEnsureAmeTabState()
	lInstallPDAUrlWrap()
	lInstallDockWrap()
	-- If landing is not shown (returning players / mid-campaign), keep tab visible.
	if TutorialHintsState and TutorialHintsState.LandingPageShown then
		DockBrowserTab("ame")
	end
end
