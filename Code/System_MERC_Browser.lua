-- M.E.R.C. PDA browser tab + PDAMERCBrowser class (JAZZ-UI-MERC-001).
-- Fork of AME browser pattern. Declares wrap flags at file load; injects tab/mode after DataLoaded.
-- Chains MercCanContact / PDAUrl / DockBrowserTab after AME (outermost wrap).

g_JAZZ_MERC_BrowserInstalled = rawget(_G, "g_JAZZ_MERC_BrowserInstalled") or false
g_JAZZ_MERC_MercCanContactBase = rawget(_G, "g_JAZZ_MERC_MercCanContactBase") or false
g_JAZZ_MERC_MercCanContactFn = rawget(_G, "g_JAZZ_MERC_MercCanContactFn") or false
g_JAZZ_MERC_PDAUrlBase = rawget(_G, "g_JAZZ_MERC_PDAUrlBase") or false
g_JAZZ_MERC_PDAUrlWrapped = rawget(_G, "g_JAZZ_MERC_PDAUrlWrapped") or false
g_JAZZ_MERC_PDAUrlFn = rawget(_G, "g_JAZZ_MERC_PDAUrlFn") or false
g_JAZZ_MERC_DockBase = rawget(_G, "g_JAZZ_MERC_DockBase") or false
g_JAZZ_MERC_DockFn = rawget(_G, "g_JAZZ_MERC_DockFn") or false

DefineClass.PDAMERCBrowser = {
	__parents = { "PDAAIMBrowser" },
}

function JAZZ_MERC_GetOrgLabel(merc)
	return Untranslated("M.E.R.C.")
end

function JAZZ_MERC_GetStatusLabel(merc)
	local hs = merc and merc.HireStatus
	if not hs then
		return Untranslated("—")
	end
	return Untranslated(tostring(hs))
end

function JAZZ_MERC_GetDepartureReasonText(ud)
	if not ud then
		return false
	end
	if ud.HireStatus == "Dead" then
		return T(890000000009907, "<style PDAMercPrice_Dead>Killed in action</style>")
	end
	if ud.HireStatus == "MIA" then
		return T(890000000009908, "Missing in action")
	end
	return false
end

function PDAMERCBrowser:Open()
	self.show_bio = AIMBrowserSection == "bio"
	XDialog.Open(self)
	local autoSelectMerc = false
	local mode_param = GetDialogModeParam(self.parent) or GetDialogModeParam(GetDialog("PDADialog")) or GetDialog("PDADialog").context
	if mode_param and mode_param.select_merc then
		autoSelectMerc = mode_param.select_merc
	end
	RunWhenXWindowIsReady(self, function()
		if self.window_state == "destroying" then return end
		self:SetFilter(CurrentMERCFilter or 1, autoSelectMerc)
		self.idMercList:SetFocus()
	end)
end

function PDAMERCBrowser:SetFilter(id, auto_select)
	CurrentMERCFilter = id
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

function PDAMERCBrowser:UpdateSelectedFilter()
	local mercsPerFilter = {}
	local filterContainer = self:ResolveId("idFilters")
	local buttonIdx = 1
	for i, f in ipairs(filterContainer) do
		if IsKindOf(f, "XTextButton") then
			local list = GetFilteredMERCMercs(buttonIdx)
			local enabled = #list > 0
			f:SetEnabled(enabled)
			local shouldBeSelected = buttonIdx == self.current_filter
			f:SetSelected(enabled and shouldBeSelected)
			if not enabled and shouldBeSelected then
				local filterAll = table.find(GetMERCScreenFilters(), "nameString", "all")
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

function PDAMERCBrowser:OnShortcut(shortcut, ...)
	if shortcut == "LeftShoulder" or shortcut == "RightShoulder" then
		local currentFilter = self.current_filter
		if shortcut == "LeftShoulder" then
			currentFilter = currentFilter - 1
		else
			currentFilter = currentFilter + 1
		end
		local filtersArray = GetMERCScreenFilters()
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

local function lEnsureMercTabData()
	local tabData = rawget(_G, "PDABrowserTabData")
	if type(tabData) ~= "table" then
		return
	end
	if not table.find(tabData, "id", "merc") then
		local ameIdx = table.find(tabData, "id", "ame")
		local aimIdx = table.find(tabData, "id", "aim") or 1
		local insertAt = (ameIdx or aimIdx) + 1
		table.insert(tabData, insertAt, {
			id = "merc",
			DisplayName = T(890000000009906, "M.E.R.C."),
		})
	end
	local browserClass = rawget(_G, "PDABrowser")
	if type(browserClass) == "table" then
		browserClass.InternalModes = table.concat(table.map(tabData, "id"), ", ")
	end
end

local function lEnsureMercTabState()
	local apply = rawget(_G, "JAZZ_MERC_ApplyTabLock")
	if type(apply) == "function" then
		apply()
		return
	end
	local tabState = rawget(_G, "PDABrowserTabState")
	if type(tabState) ~= "table" then
		return
	end
	local unlocked = rawget(_G, "JAZZ_MERC_IsUnlocked") and JAZZ_MERC_IsUnlocked()
	if not tabState.merc then
		tabState.merc = { locked = not unlocked }
	else
		tabState.merc.locked = not unlocked
	end
	ObjModified("pda browser tabs")
end

local function lFindNodeWithMode(node, mode, depth)
	depth = depth or 0
	if type(node) ~= "table" or depth > 14 then
		return false
	end
	if node.mode == mode then
		return node
	end
	if node[1] then
		for _, child in ipairs(node) do
			local found = lFindNodeWithMode(child, mode, depth + 1)
			if found then
				return found
			end
		end
	end
	return false
end

local function lFindModeHost(node, depth)
	depth = depth or 0
	if type(node) ~= "table" or depth > 14 then
		return false
	end
	for _, child in ipairs(node) do
		if type(child) == "table" and (child.mode == "aim" or child.mode == "ame") then
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

local function lInjectMercXTemplateMode()
	local pda = rawget(_G, "XTemplates") and XTemplates.PDABrowser
	if not pda then
		return
	end
	if lFindNodeWithMode(pda, "merc", 0) then
		return
	end
	local host = lFindModeHost(pda, 0)
	if not host then
		return
	end
	local mode = PlaceObj("XTemplateMode", {
		"mode", "merc",
	}, {
		PlaceObj("XTemplateTemplate", {
			"__template", "PDAMERCBrowser",
			"Id", "idBrowserContent",
		}),
		PlaceObj("XTemplateWindow", {
			"__class", "VirtualCursorManager",
			"Reason", "Browser",
		}),
	})
	table.insert(host, mode)
end

--- Init shelf Available + world NotMet; Affiliation MERC. Idempotent after account.initialized.
function JAZZ_MERC_InitRoster(force)
	local ensure = rawget(_G, "JAZZ_MERC_EnsureAccount")
	local account = type(ensure) == "function" and ensure() or rawget(_G, "gv_JAZZ_MERC_Account")
	if not account then
		return
	end
	if account.initialized and not force then
		lEnsureMercTabState()
		return
	end
	local unitData = rawget(_G, "gv_UnitData")
	local shelf = rawget(_G, "JAZZ_MERC_SHELF_IDS") or {}
	local world = rawget(_G, "JAZZ_MERC_WORLD_IDS") or {}
	account.met = account.met or {}
	if type(unitData) == "table" then
		for _, id in ipairs(shelf) do
			local ud = unitData[id]
			if ud then
				ud.Affiliation = "MERC"
				local hs = ud.HireStatus
				if hs ~= "Hired" and hs ~= "Dead" and hs ~= "MIA" and hs ~= "Retired" then
					ud.HireStatus = "Available"
					ObjModified(ud)
				end
			end
		end
		for _, id in ipairs(world) do
			local ud = unitData[id]
			if ud then
				ud.Affiliation = "MERC"
				local hs = ud.HireStatus
				if hs ~= "Hired" and hs ~= "Dead" and hs ~= "MIA" and hs ~= "Retired" then
					if account.met[id] then
						ud.HireStatus = "Available"
					else
						ud.HireStatus = "NotMet"
					end
					ObjModified(ud)
				elseif hs == "Hired" or hs == "Available" then
					account.met[id] = true
				end
			end
		end
	end
	account.initialized = true
	lEnsureMercTabState()
end

local function lInstallMercCanContactWrap()
	local installed = rawget(_G, "g_JAZZ_MERC_MercCanContactFn")
	local current = rawget(_G, "MercCanContact")
	if installed and current == installed then
		return true
	end
	if type(current) ~= "function" then
		return false
	end
	-- Chain: current may already be AME wrap.
	rawset(_G, "g_JAZZ_MERC_MercCanContactBase", current)
	local base = current
	local wrap = function(merc)
		if merc and merc.Affiliation == "MERC" then
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
		return base(merc)
	end
	rawset(_G, "g_JAZZ_MERC_MercCanContactFn", wrap)
	rawset(_G, "MercCanContact", wrap)
	return true
end

local function lMercUrlSlug(filter)
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

local function lMercUrlNick(unit_id)
	local ud = unit_id and gv_UnitData[unit_id]
	if not ud then
		return tostring(unit_id or "")
	end
	local nick = ud.Nick
	local englishText = rawget(_G, "TDevModeGetEnglishText")
	if nick and type(englishText) == "function" then
		local ok, text = pcall(englishText, nick)
		if ok and type(text) == "string" and text ~= "" then
			local slug = text:gsub("%s+", "%%20"):gsub("[^%w%%%-._~]", "-")
			return slug
		end
	end
	return tostring(ud.session_id or unit_id):gsub("%s+", "%%20")
end

local function lBuildMercPDAUrl(browserContent)
	local filters = GetMERCScreenFilters()
	local filter = filters[browserContent.current_filter]
	if not filter then
		return Untranslated("http://www.merc.com/")
	end
	local url = Untranslated("http://www.merc.com/Roster/") .. Untranslated(lMercUrlSlug(filter))
	local selectedUnit = browserContent.selected_merc
	if selectedUnit then
		url = url .. Untranslated("/" .. lMercUrlNick(selectedUnit))
	end
	return url
end

local function lInstallReassertWrap(cfg)
	local ourFn = rawget(_G, cfg.ourFnKey)
	local current = cfg.getCurrent()
	if ourFn and current == ourFn then
		if cfg.wrappedKey then
			rawset(_G, cfg.wrappedKey, true)
		end
		return true
	end
	if type(current) ~= "function" then
		return false
	end
	if current ~= ourFn then
		rawset(_G, cfg.baseKey, current)
	elseif not rawget(_G, cfg.baseKey) then
		return false
	end
	local wrap = cfg.buildWrap(current)
	rawset(_G, cfg.ourFnKey, wrap)
	cfg.setCurrent(wrap)
	if cfg.wrappedKey then
		rawset(_G, cfg.wrappedKey, true)
	end
	return true
end

local function lInstallPDAUrlWrap()
	local tformat = rawget(_G, "TFormat")
	if type(tformat) ~= "table" or type(tformat.PDAUrl) ~= "function" then
		return false
	end
	return lInstallReassertWrap({
		ourFnKey = "g_JAZZ_MERC_PDAUrlFn",
		baseKey = "g_JAZZ_MERC_PDAUrlBase",
		wrappedKey = "g_JAZZ_MERC_PDAUrlWrapped",
		getCurrent = function()
			return tformat.PDAUrl
		end,
		setCurrent = function(fn)
			tformat.PDAUrl = fn
		end,
		buildWrap = function(base)
			return function(context_obj)
				local pda = GetDialog("PDADialog")
				if pda then
					local content = pda:ResolveId("idContent")
					local mercBrowser = IsKindOf(content, "PDABrowser") and content
					local browserContent = mercBrowser and mercBrowser.idBrowserContent
					-- PDAMERCBrowser is KindOf PDAAIMBrowser — check MERC before AME/AIM.
					if IsKindOf(browserContent, "PDAMERCBrowser") then
						return lBuildMercPDAUrl(browserContent)
					end
				end
				if type(base) == "function" then
					return base(context_obj)
				end
				return Untranslated("http://www.merc.com/")
			end
		end,
	})
end

local function lInstallDockWrap()
	return lInstallReassertWrap({
		ourFnKey = "g_JAZZ_MERC_DockFn",
		baseKey = "g_JAZZ_MERC_DockBase",
		getCurrent = function()
			return rawget(_G, "DockBrowserTab")
		end,
		setCurrent = function(fn)
			rawset(_G, "DockBrowserTab", fn)
		end,
		buildWrap = function(base)
			return function(tab)
				if type(base) ~= "function" then
					return
				end
				base(tab)
				-- When docking aim, also dock merc IF unlocked (AME already docks ame).
				if tab == "aim" then
					local unlocked = rawget(_G, "JAZZ_MERC_IsUnlocked") and JAZZ_MERC_IsUnlocked()
					if unlocked then
						base("merc")
						local tabState = rawget(_G, "PDABrowserTabState")
						if type(tabState) == "table" then
							if tabState.merc then
								tabState.merc.locked = false
							else
								tabState.merc = { locked = false }
							end
							ObjModified("pda browser tabs")
						end
					end
				end
			end
		end,
	})
end

local function lMaybeDockMerc()
	if not (rawget(_G, "JAZZ_MERC_IsUnlocked") and JAZZ_MERC_IsUnlocked()) then
		return
	end
	local dock = rawget(_G, "DockBrowserTab")
	if type(dock) == "function" then
		dock("merc")
	end
end

local function lInstallMercBrowser()
	lEnsureMercTabData()
	lInjectMercXTemplateMode()
	if not rawget(_G, "g_JAZZ_MERC_BrowserInstalled") then
		rawset(_G, "g_JAZZ_MERC_BrowserInstalled", true)
	end
	lInstallMercCanContactWrap()
	lInstallDockWrap()
	lInstallPDAUrlWrap()
	lEnsureMercTabState()
end

function OnMsg.ClassesPostprocess()
	lEnsureMercTabData()
end

function OnMsg.DataLoaded()
	-- Delayed so AME wraps install first when both listen to DataLoaded.
	local delayed = rawget(_G, "DelayedCall")
	local install = function()
		lInstallMercBrowser()
		lInjectMercXTemplateMode()
	end
	if type(delayed) == "function" then
		delayed(0, install)
	else
		install()
	end
end

function OnMsg.ModsReloaded()
	local contactFn = rawget(_G, "g_JAZZ_MERC_MercCanContactFn")
	local contactBase = rawget(_G, "g_JAZZ_MERC_MercCanContactBase")
	if contactFn and rawget(_G, "MercCanContact") == contactFn and type(contactBase) == "function" then
		rawset(_G, "MercCanContact", contactBase)
	end
	local pdaFn = rawget(_G, "g_JAZZ_MERC_PDAUrlFn")
	local pdaBase = rawget(_G, "g_JAZZ_MERC_PDAUrlBase")
	local tformat = rawget(_G, "TFormat")
	if type(tformat) == "table" and pdaFn and tformat.PDAUrl == pdaFn and type(pdaBase) == "function" then
		tformat.PDAUrl = pdaBase
	end
	local dockFn = rawget(_G, "g_JAZZ_MERC_DockFn")
	local dockBase = rawget(_G, "g_JAZZ_MERC_DockBase")
	if dockFn and rawget(_G, "DockBrowserTab") == dockFn and type(dockBase) == "function" then
		rawset(_G, "DockBrowserTab", dockBase)
	end
	rawset(_G, "g_JAZZ_MERC_BrowserInstalled", false)
	rawset(_G, "g_JAZZ_MERC_MercCanContactFn", false)
	rawset(_G, "g_JAZZ_MERC_MercCanContactBase", false)
	rawset(_G, "g_JAZZ_MERC_DockFn", false)
	rawset(_G, "g_JAZZ_MERC_DockBase", false)
	rawset(_G, "g_JAZZ_MERC_PDAUrlWrapped", false)
	rawset(_G, "g_JAZZ_MERC_PDAUrlFn", false)
	rawset(_G, "g_JAZZ_MERC_PDAUrlBase", false)
	local delayed = rawget(_G, "DelayedCall")
	if type(delayed) == "function" then
		delayed(0, lInstallMercBrowser)
	else
		lInstallMercBrowser()
	end
end

function OnMsg.NewGame()
	local delayed = rawget(_G, "DelayedCall")
	local boot = function()
		local ensure = rawget(_G, "JAZZ_MERC_EnsureAccount")
		if type(ensure) == "function" then
			ensure()
		end
		JAZZ_MERC_InitRoster(true)
		lEnsureMercTabState()
		-- Do NOT dock merc until unlocked.
	end
	if type(delayed) == "function" then
		delayed(0, boot)
	else
		boot()
	end
end

function OnMsg.LoadGame()
	local delayed = rawget(_G, "DelayedCall")
	local boot = function()
		local ensure = rawget(_G, "JAZZ_MERC_EnsureAccount")
		if type(ensure) == "function" then
			ensure()
		end
		JAZZ_MERC_InitRoster(false)
		-- Speck welcome for pre-MERC / mid-campaign saves (Mail also hooks LoadGame).
		local migrate = rawget(_G, "JAZZ_MERC_MigrateWelcomeFromSave")
		if type(migrate) == "function" then
			migrate()
		end
		lEnsureMercTabState()
		lMaybeDockMerc()
	end
	if type(delayed) == "function" then
		delayed(0, boot)
	else
		boot()
	end
end

local function lSwitchPDABrowserToMerc()
	local getDlg = rawget(_G, "GetDialog")
	local pda = type(getDlg) == "function" and getDlg("PDADialog")
	if not pda then
		return false
	end
	if pda.Mode ~= "browser" and pda.SetMode then
		pda:SetMode("browser", { browser_page = "merc" })
	end
	local dlg = pda.idContent
	if not dlg or type(dlg.SetMode) ~= "function" then
		return false
	end
	-- Instance may predate merc-mode inject; XDialog ignores unknown InternalModes.
	if type(dlg.InternalModes) == "string" and not string.find(dlg.InternalModes, "merc", 1, true) then
		dlg.InternalModes = dlg.InternalModes .. ", merc"
	end
	if dlg.Mode ~= "merc" then
		dlg:SetMode("merc")
	end
	return dlg.Mode == "merc"
end

function JAZZ_MERC_OpenSite()
	if not (rawget(_G, "JAZZ_MERC_IsUnlocked") and JAZZ_MERC_IsUnlocked()) then
		return false
	end
	lEnsureMercTabData()
	lInjectMercXTemplateMode()
	lEnsureMercTabState()
	lMaybeDockMerc()
	local getDlg = rawget(_G, "GetDialog")
	local openDlg = rawget(_G, "OpenDialog")
	local getIGI = rawget(_G, "GetInGameInterface")
	local pda = type(getDlg) == "function" and getDlg("PDADialog")
	if not pda and type(openDlg) == "function" then
		local igi = type(getIGI) == "function" and getIGI()
		-- Same pattern as vanilla OpenIMPPage / OpenBobbyRayPage: then force submode.
		pda = openDlg("PDADialog", igi, { Mode = "browser", mode_param = { browser_page = "merc" } })
	end
	if not pda then
		return false
	end
	if lSwitchPDABrowserToMerc() then
		return true
	end
	-- Content may spawn on the next frame after OpenDialog from satellite.
	local delayed = rawget(_G, "DelayedCall")
	if type(delayed) == "function" then
		delayed(0, lSwitchPDABrowserToMerc)
	end
	return true
end

function OnMsg.BrowserOpened()
	lEnsureMercTabState()
	lInstallPDAUrlWrap()
	lInstallDockWrap()
	local hints = rawget(_G, "TutorialHintsState")
	if hints and hints.LandingPageShown then
		lMaybeDockMerc()
	end
end
