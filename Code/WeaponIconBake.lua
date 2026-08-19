-- DORMANT — JAZZ-UI-001 path E. Not listed in metadata.code / ModItemCode.
-- Inventory uses chips (WeaponAttachChips.lua). Do not re-add this file to the
-- load list: top-level code redirects g_HgnvCompressPath and prints [JAZZ-UI-001].
--
-- JAZZ-UI-001: side-view baked inventory icons with attachments.
-- Goal: weapon only on TRANSPARENT background.
-- Capture -> wepicon25_<hash>.raw.png -> jazz_wepicon_hook.cmd (via ImportImage/AsyncExec) -> .png
-- AsyncExec is sandboxed; we permanently point g_HgnvCompressPath at our hook.cmd (set during Loading).

local CacheReady = {}
local CacheFailed = {}
local Queued = {}
local Busy = false
local DirReady = false
local CACHE_PREFIX = "wepicon25_"

local real_ConvertToOSPath = ConvertToOSPath
local HookInstalled = false
local HookCmdVirtual = false

do
	local hook_virtual = (CurrentModPath or "") .. "Code/jazz_wepicon_hook.cmd"
	print("[JAZZ-UI-001] Loading=", tostring(rawget(_G, "Loading")), "hook=", hook_virtual)
	local ok, err = pcall(function()
		g_HgnvCompressPath = hook_virtual
	end)
	if ok then
		HookInstalled = true
		HookCmdVirtual = hook_virtual
		print("[JAZZ-UI-001] g_HgnvCompressPath -> hook.cmd OK")
	else
		print("[JAZZ-UI-001] g_HgnvCompressPath assign FAILED:", err)
	end
end

local function RunKeyViaImportImage(raw_os)
	if not HookInstalled then
		return false, "hook-not-installed"
	end
	if not (ModItemDecalEntity and ModItemDecalEntity.ImportImage) then
		return false, "no-ImportImage"
	end
	local stub_ged = { ShowMessage = function(_, title, msg)
		print("[JAZZ-UI-001] ImportImage msg:", title, msg)
	end }
	-- ImportImage is called with stub as self, so ValidateImage must live on stub.
	local stub = {
		GetProperty = function()
			return raw_os
		end,
		GetTextureFileName = function()
			return "jazz_wepicon_stub.dds"
		end,
		ValidateImage = function()
			return true
		end,
	}
	local ok, err = pcall(function()
		-- Runs: "<g_HgnvCompressPath>" -dds10 ... "<raw_os>" "<texture_output>"
		-- Our hook.cmd sees .raw.png and keys it.
		ModItemDecalEntity.ImportImage(stub, stub_ged, "DiffusePath", "AppData/Editor/", "AppData/Editor/")
	end)
	if not ok then
		return false, err
	end
	return true
end

function JazzWeaponIcon_IsFirearm(item)
	return IsKindOfClasses(item, "Firearm", "HeavyWeapon") and not IsKindOf(item, "InventoryStack")
end

function JazzWeaponIcon_IsCachePath(path)
	return type(path) == "string" and string.find(path, "AppData/Editor/", 1, true) == 1
		and string.find(path, CACHE_PREFIX, 1, true)
		and not string.find(path, "%.raw%.png$", 1)
end

local function FileExistsUil(vpath)
	if (vpath or "") == "" then
		return false
	end
	local uil = rawget(_G, "UIL")
	if uil and uil.RequestImage then
		uil.RequestImage(vpath)
	end
	if uil and uil.MeasureImage then
		local w, h = uil.MeasureImage(vpath)
		if (w or 0) > 0 and (h or 0) > 0 then
			return true
		end
	end
	return false
end

local function UnloadVPath(vpath)
	local uil = rawget(_G, "UIL")
	if uil and uil.UnloadImage and vpath then
		uil.UnloadImage(vpath)
	end
end

local function EnsureDir()
	if DirReady then
		return true
	end
	local stub = string.format("AppData/Editor/%s/%sstub.png", CurrentModId, CACHE_PREFIX)
	local dir_path = SplitPath(stub)
	local stub_ged = { ShowMessage = function() end }
	if not (ModItemDecalEntity and ModItemDecalEntity.CreateDirectory) then
		return false
	end
	if not ModItemDecalEntity:CreateDirectory(stub_ged, dir_path, "WeaponIconCache") then
		return false
	end
	DirReady = true
	print("[JAZZ-UI-001] cache dir ready:", dir_path)
	return true
end

function JazzWeaponIcon_Fingerprint(weapon)
	if not weapon then
		return false
	end
	local parts = { weapon.class or "?" }
	local slots = {}
	for slot in pairs(weapon.components or empty_table) do
		slots[#slots + 1] = slot
	end
	table.sort(slots)
	for _, slot in ipairs(slots) do
		parts[#parts + 1] = slot .. "=" .. tostring(weapon.components[slot] or "")
	end
	return table.concat(parts, "|")
end

function JazzWeaponIcon_VirtualPath(fingerprint)
	return string.format("AppData/Editor/%s/%s%s.png", CurrentModId, CACHE_PREFIX, tostring(xxhash(fingerprint)))
end

local function RawCapturePath(vpath)
	return string.gsub(vpath, "%.png$", ".raw.png")
end

function JazzWeaponIcon_IsStockConfig(weapon)
	if not weapon then
		return true
	end
	local slots = weapon.ComponentSlots
	-- Runtime instances can lose the slots table; fall back to class preset.
	if (not slots or #slots == 0) and g_Classes and weapon.class and g_Classes[weapon.class] then
		slots = g_Classes[weapon.class].ComponentSlots
	end
	if not slots or #slots == 0 then
		return true
	end
	for _, slot in ipairs(slots) do
		local cur = weapon.components and weapon.components[slot.SlotType] or ""
		local def = slot.DefaultComponent or ""
		if cur ~= def then
			return false
		end
	end
	return true
end

function JazzWeaponIcon_HasBakedIcon(weapon)
	return JazzWeaponIcon_Resolve(weapon) and true or false
end

function JazzWeaponIcon_ApplyToXImage(img, path)
	if not img or (path or "") == "" then
		return
	end
	if img.SetBaseColorMap then
		img:SetBaseColorMap(false)
	end
	img:SetImage(path, true)
	if not JazzWeaponIcon_IsCachePath(path) then
		return
	end
	-- Vanilla OnContextUpdate often sets ImageFit("width"); keep uniform scale for baked PNGs.
	if img.SetImageFit then
		img:SetImageFit("largest")
	end
	local uil = rawget(_G, "UIL")
	if uil and uil.RequestImage then
		uil.RequestImage(path)
	end
	if uil and uil.MeasureImage then
		local w, h = uil.MeasureImage(path)
		if (w or 0) > 0 and (h or 0) > 0 then
			img.src_rect = box(0, 0, w, h)
			img:InvalidateMeasure()
			img:Invalidate()
		end
	end
end

function JazzWeaponIcon_Invalidate(weapon)
	local fp = JazzWeaponIcon_Fingerprint(weapon)
	if not fp then
		return
	end
	CacheReady[fp] = nil
	CacheFailed[fp] = nil
	local vpath = JazzWeaponIcon_VirtualPath(fp)
	UnloadVPath(vpath)
	UnloadVPath(RawCapturePath(vpath))
end

function JazzWeaponIcon_WipeMemoryCache()
	CacheReady = {}
	CacheFailed = {}
	Queued = {}
	print("[JAZZ-UI-001] memory cache wiped")
end

function JazzWeaponIcon_Resolve(weapon)
	if not JazzWeaponIcon_IsFirearm(weapon) or JazzWeaponIcon_IsStockConfig(weapon) then
		return false
	end
	local fp = JazzWeaponIcon_Fingerprint(weapon)
	if not fp then
		return false
	end
	local vpath = JazzWeaponIcon_VirtualPath(fp)
	-- Trust session memory: UIL.MeasureImage often misses right after HUD respawn (merc switch).
	if CacheReady[fp] then
		return vpath
	end
	if FileExistsUil(vpath) then
		CacheReady[fp] = true
		return vpath
	end
	return false
end

local function SetupSideCamera(vis)
	local bbox = vis:GetObjectBBox()
	if not bbox then
		return false
	end
	local center = bbox:Center()
	local sx, sy, sz = bbox:sizexyz()
	local extent = Max(sx, Max(sy, sz))
	if extent <= 0 then
		extent = 2 * guim
	end
	local cam_pos = center + point(0, MulDivRound(extent, 900, 1000), MulDivRound(extent, 120, 1000))
	if not cameraRTS.IsActive() then
		cameraRTS.Activate(1)
	end
	SetCamera(cam_pos, center, nil, nil, nil, 0)
	return true
end

local function ScreenBoxAroundVis(vis, pad_frac)
	local bbox = vis:GetObjectBBox()
	if not bbox or not GameToScreen then
		return false
	end
	local c = bbox:Center()
	local sx, sy, sz = bbox:sizexyz()
	local hx, hy, hz = sx / 2, sy / 2, sz / 2
	local min_sx, min_sy, max_sx, max_sy = false, false, false, false
	for _, dx in ipairs({ -1, 1 }) do
		for _, dy in ipairs({ -1, 1 }) do
			for _, dz in ipairs({ -1, 1 }) do
				local ok, sp = GameToScreen(c + point(dx * hx, dy * hy, dz * hz))
				if ok and sp then
					local x, y = sp:xy()
					min_sx = min_sx and Min(min_sx, x) or x
					min_sy = min_sy and Min(min_sy, y) or y
					max_sx = max_sx and Max(max_sx, x) or x
					max_sy = max_sy and Max(max_sy, y) or y
				end
			end
		end
	end
	if not min_sx then
		return false
	end
	local screen = UIL.GetScreenSize()
	local sw, sh = screen:xy()
	local pad_x = MulDivRound(max_sx - min_sx, pad_frac or 20, 100)
	local pad_y = MulDivRound(max_sy - min_sy, pad_frac or 20, 100)
	min_sx = Max(0, min_sx - pad_x)
	min_sy = Max(0, min_sy - pad_y)
	max_sx = Min(sw - 1, max_sx + pad_x)
	max_sy = Min(sh - 1, max_sy + pad_y)
	if max_sx <= min_sx or max_sy <= min_sy then
		return false
	end
	return box(min_sx, min_sy, max_sx, max_sy)
end

local function PlaceBakeBackdrop(base_pos)
	local bg = PlaceObject("WeaponModCMTPlane")
	if not IsValid(bg) then
		return false
	end
	-- Magenta chroma key (olive #504633 keys into wood/metal and eats the silhouette).
	bg:SetColorModifier(RGB(255, 0, 255))
	if bg.SetSIModulation then
		bg:SetSIModulation(0) -- unlit: avoids circular "sun" hotspot from PointLights
	end
	bg:SetAxis(point(0, 4096, 4096))
	bg:SetAngle(180 * 60)
	bg:SetPos(base_pos + point(0, -2800, 0))
	local max_scale = bg.GetMaxScale and bg:GetMaxScale() or 500
	bg:SetScale(Min(500, max_scale))
	bg:SetGameFlags(const.gofAlwaysRenderable)
	bg:SetEnumFlags(const.efVisible)
	return bg
end

local function PlaceSoftLight(base_pos, off, intensity)
	local light = PlaceObject("PointLight")
	if not IsValid(light) then
		return false
	end
	light:SetPos(base_pos + off)
	if light.SetIntensity then
		light:SetIntensity(intensity or 45)
	end
	if light.SetColor then
		light:SetColor(RGB(220, 215, 205))
	end
	if light.SetCastShadows then
		light:SetCastShadows(false)
	end
	return light
end

local function DoDedicatedBake(weapon)
	if not JazzWeaponIcon_IsFirearm(weapon) then
		return false, "nonfirearm"
	end
	if JazzWeaponIcon_IsStockConfig(weapon) then
		return false, "stock-config"
	end
	local map = GetMap and GetMap() or ""
	if (map or "") == "" then
		return false, "no-map"
	end
	if GetDialog("ModifyWeaponDlg") then
		return false, "modify-open"
	end
	if not EnsureDir() then
		return false, "no-dir"
	end
	if not WaitCaptureScreenshot then
		return false, "no-capture-api"
	end
	if not HookInstalled then
		return false, "hook-not-installed"
	end

	local fp = JazzWeaponIcon_Fingerprint(weapon)
	local vpath = JazzWeaponIcon_VirtualPath(fp)
	local raw_vpath = RawCapturePath(vpath)
	local final_os = real_ConvertToOSPath(vpath)
	local raw_os = real_ConvertToOSPath(raw_vpath)

	UnloadVPath(vpath)
	UnloadVPath(raw_vpath)

	print("[JAZZ-UI-001] dedicated capture -", raw_vpath)
	print("[JAZZ-UI-001] raw_os=", raw_os)

	local clone = weapon:UIClone()
	local vis = clone:CreateVisualObj("JazzWeaponIconBake")
	if not IsValid(vis) then
		return false, "no-visual"
	end
	clone:UpdateVisualObj(vis)
	if clone.UpdateColorMod then
		clone:UpdateColorMod(vis)
	end

	local base_pos = point(0, 0, 140 * guim)
	if IsValid(g_Cabinet) then
		base_pos = g_Cabinet:GetPos() + point(0, 0, 40 * guim)
	end

	local pivot = PlaceObject("FakeOriginObject")
	if IsValid(pivot) then
		pivot:SetPos(base_pos)
	end
	vis:SetPos(base_pos)
	vis:SetAngle(90 * 60)
	vis:SetScale(100)
	vis:SetForcedLOD(0)
	vis:SetGameFlags(const.gofAlwaysRenderable)
	vis:SetEnumFlags(const.efVisible)
	if IsValid(pivot) then
		pivot:Attach(vis)
	end

	local backdrop = PlaceBakeBackdrop(base_pos)
	local lights = {}
	local function add_light(off, intensity)
		local light = PlaceSoftLight(base_pos, off, intensity)
		if light then
			lights[#lights + 1] = light
		end
	end
	-- Soft key/fill in front of weapon only (camera is +Y); keep spill off the rear plane.
	add_light(point(MulDivRound(guim, 6, 10), MulDivRound(guim, 10, 10), MulDivRound(guim, 5, 10)), 38)
	add_light(point(-MulDivRound(guim, 5, 10), MulDivRound(guim, 7, 10), MulDivRound(guim, 3, 10)), 22)

	local cam_params = { GetCamera() }
	local hr_changed, pass_suspended = false, false
	local old_lm = CurrentLightmodel and CurrentLightmodel[1]
	local lm_changed = false
	local capture_err

	local function cleanup()
		UnlockCamera("JazzWeaponIconBake")
		if lm_changed and old_lm then
			SetLightmodel(1, old_lm, 0)
		end
		if hr_changed then
			table.restore(hr, "JazzWeaponIconBake")
		end
		local hid = editor and editor.HiddenManually
		if hid then
			editor.HiddenManually = setmetatable({}, weak_keys_meta)
			for obj in pairs(hid) do
				if IsValid(obj) then
					GameToolsShowObject(obj)
				end
			end
		end
		if pass_suspended then
			ResumePassEdits("JazzWeaponIconBake", true)
		end
		for _, light in ipairs(lights) do
			if IsValid(light) then
				DoneObject(light)
			end
		end
		if IsValid(backdrop) then
			DoneObject(backdrop)
		end
		if IsValid(vis) then
			DoneObject(vis)
		end
		if IsValid(pivot) then
			DoneObject(pivot)
		end
		SetCamera(unpack_params(cam_params))
	end

	local ok, err = pcall(function()
		LockCamera("JazzWeaponIconBake")

		if LightmodelPresets and LightmodelPresets.WeaponModification then
			SetLightmodel(1, LightmodelPresets.WeaponModification, 0)
			lm_changed = true
		elseif SetLightmodel then
			SetLightmodel(1, "WeaponModification", 0)
			lm_changed = true
		end

		table.change(hr, "JazzWeaponIconBake", {
			EnablePostProcVignette = 0,
			EnableContourOuter = 0,
			EnableContourInner = 0,
			EnableObjectMarking = 0,
			EnableScreenSpaceReflections = 0,
			EnablePostprocess = 0,
			RenderTerrain = 0,
			RenderBillboards = 0,
			RenderSky = 0,
			RenderClutter = 0,
			RenderRain = 0,
			AutoExposureMode = 0,
			NearZ = 1,
			ObjectLODCapMin = 0,
		})
		hr_changed = true

		editor.HiddenManually = editor.HiddenManually or setmetatable({}, weak_keys_meta)
		SuspendPassEdits("JazzWeaponIconBake", true)
		pass_suspended = true
		MapForEach("map", "attached", false, "CObject", nil, const.efVisible, function(obj)
			if obj == vis or obj == pivot or obj == backdrop then
				return
			end
			for _, light in ipairs(lights) do
				if obj == light then
					return
				end
			end
			local parent = obj.GetParent and obj:GetParent()
			if parent == vis or parent == pivot then
				return
			end
			if not editor.HiddenManually[obj] then
				editor.HiddenManually[obj] = true
				GameToolsHideObject(obj)
			end
		end)
		GameToolsShowObject(vis)
		if IsValid(backdrop) then
			GameToolsShowObject(backdrop)
		end
		for _, light in ipairs(lights) do
			GameToolsShowObject(light)
		end
		for _, part in pairs(vis.parts or empty_table) do
			if IsValid(part) then
				GameToolsShowObject(part)
			end
		end

		SetupSideCamera(vis)
		WaitNextFrame(5)

		local src_box = ScreenBoxAroundVis(vis, 30)
		local capture_opts = { interface = false, alpha = true }
		if src_box then
			capture_opts.src = src_box
			-- WriteScreenshot stretches src -> width/height. Keep the same aspect or proportions break.
			local bw, bh = src_box:sizex(), src_box:sizey()
			if (bw or 0) < 1 then
				bw = 1
			end
			if (bh or 0) < 1 then
				bh = 1
			end
			local max_w, max_h = 512, 256
			local out_w, out_h
			if bw * max_h >= bh * max_w then
				out_w = max_w
				out_h = Max(1, MulDivRound(bh, max_w, bw))
			else
				out_h = max_h
				out_w = Max(1, MulDivRound(bw, max_h, bh))
			end
			capture_opts.width = out_w
			capture_opts.height = out_h
			print("[JAZZ-UI-001] capture src box", tostring(src_box), "out", out_w, "x", out_h)
		end

		capture_err = WaitCaptureScreenshot(raw_os, capture_opts)
		if capture_err == "no file written" then
			capture_err = WaitCaptureScreenshot(raw_vpath, capture_opts)
		end
		if capture_err then
			capture_opts.alpha = false
			capture_err = WaitCaptureScreenshot(raw_os, capture_opts)
		end
	end)

	cleanup()

	if not ok then
		return false, err
	end
	if capture_err then
		return false, capture_err
	end

	print("[JAZZ-UI-001] running key via hook.cmd / ImportImage-")
	local key_ok, key_err = RunKeyViaImportImage(raw_os)
	if not key_ok then
		print("[JAZZ-UI-001] key invoke failed:", key_err)
		return false, "key-invoke:" .. tostring(key_err)
	end

	-- Hook may need a moment; also UIL must re-request the new file.
	Sleep(300)
	UnloadVPath(vpath)
	local uil = rawget(_G, "UIL")
	if uil and uil.RequestImage then
		uil.RequestImage(vpath)
	end
	WaitNextFrame(5)

	if not FileExistsUil(vpath) then
		print("[JAZZ-UI-001] final missing. Check AppData/Editor/" .. tostring(CurrentModId) .. "/wepicon_hook.log")
		print("[JAZZ-UI-001] expected final_os=", final_os)
		return false, "final-missing-after-key"
	end

	print("[JAZZ-UI-001] transparent icon ready", vpath)
	return true, vpath
end

local function RefreshInventory(weapon)
	if InventoryUIRespawn then
		InventoryUIRespawn()
	end
	if weapon then
		ObjModified(weapon)
	end
end

local function ResolveLiveWeapon(weapon, item_id)
	if item_id and g_ItemIdToItem then
		local live = g_ItemIdToItem[item_id]
		if JazzWeaponIcon_IsFirearm(live) then
			return live
		end
	end
	if JazzWeaponIcon_IsFirearm(weapon) then
		return weapon
	end
	return false
end

function JazzWeaponIcon_QueueDedicatedBake(weapon)
	if not weapon or not JazzWeaponIcon_IsFirearm(weapon) then
		return
	end
	if JazzWeaponIcon_IsStockConfig(weapon) then
		return
	end
	local fp = JazzWeaponIcon_Fingerprint(weapon)
	if not fp or Queued[fp] or Busy then
		return
	end
	local item_id = weapon.id
	Queued[fp] = true
	Busy = true
	CreateRealTimeThread(function()
		local guard = 0
		while GetDialog("ModifyWeaponDlg") and guard < 600 do
			Sleep(100)
			guard = guard + 1
		end
		Sleep(200)
		local live = ResolveLiveWeapon(weapon, item_id)
		local ok, success, detail
		if not live then
			ok, success, detail = true, false, "weapon-unresolved:" .. tostring(item_id)
		else
			ok, success, detail = pcall(DoDedicatedBake, live)
		end
		Queued[fp] = nil
		Busy = false
		if ok and success then
			CacheReady[fp] = true
			CacheFailed[fp] = nil
			print("[JAZZ-UI-001] dedicated baked", fp, "->", JazzWeaponIcon_VirtualPath(fp))
			RefreshInventory(live or weapon)
		else
			CacheFailed[fp] = true
			print("[JAZZ-UI-001] dedicated bake failed:", fp, ok and detail or success)
		end
	end)
end

function JazzWeaponIcon_UnstickModifyUI()
	if HideInWorldCombatUI then
		HideInWorldCombatUI(false, "JazzWeaponIconBake")
	end
	if HideCombatUI then
		HideCombatUI(false)
	end
	local desk = terminal and terminal.desktop
	if desk and desk.SetMouseCapture then
		desk:SetMouseCapture(false)
	end
	local dlg = GetDialog("ModifyWeaponDlg")
	if dlg then
		dlg:SetVisible(true)
	end
	UnlockCamera("JazzWeaponIconBake")
	print("[JAZZ-UI-001] UnstickModifyUI done")
end

-- Path B (2026-07-30): inventory shows attachment chips, not baked silhouette.
-- Keep bake helpers available for experiments; do not override GetItemUIIcon or queue.
JazzWeaponIcon_BakeEnabled = false

local OldGetItemUIIcon = InventoryItem.GetItemUIIcon
function FirearmBase:GetItemUIIcon()
	if JazzWeaponIcon_BakeEnabled then
		local baked = JazzWeaponIcon_Resolve(self)
		if baked then
			return baked
		end
		if not JazzWeaponIcon_IsStockConfig(self) then
			JazzWeaponIcon_QueueDedicatedBake(self)
		end
	end
	return OldGetItemUIIcon(self)
end

function OnMsg.WeaponModifiedSuccessSync(weapon, ...)
	if not JazzWeaponIcon_BakeEnabled or not weapon then
		return
	end
	JazzWeaponIcon_Invalidate(weapon)
	JazzWeaponIcon_QueueDedicatedBake(weapon)
end
