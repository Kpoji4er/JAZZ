-- HOTFIX: CharacterEffect with no non-default props serializes as
-- PlaceCharacterEffect('Id', ) which is invalid Lua and blocks save load.
-- Vanilla CharacterEffect:__toluacode always emits the comma; empty
-- ObjPropertyListToLuaCode then leaves a dangling ')'.
-- Mid-combat suppressionPinned often has only default CampaignTimeAdded.
--
-- AsyncFileToString returns pstr userdata (type() ~= "string"). Do NOT
-- gate on type=="string" / tostring — use string.gsub on the blob directly
-- (vanilla already uses string.starts_with on the same value).
--
-- CommonLib wraps LoadGameSessionData and becomes the visible global; we
-- stay in its closed-over orig when we wrap first. Also gate via
-- GameSpecificLoadCallback so sanitize always runs on each load.

g_JAZZ_CharEffectSerialize_LoadWrapped = rawget(_G, "g_JAZZ_CharEffectSerialize_LoadWrapped") or false
g_JAZZ_CharEffectSerialize_LoadBase = rawget(_G, "g_JAZZ_CharEffectSerialize_LoadBase") or false
g_JAZZ_CharEffectSerialize_GSCBWrapped = rawget(_G, "g_JAZZ_CharEffectSerialize_GSCBWrapped") or false
g_JAZZ_CharEffectSerialize_GSCBBase = rawget(_G, "g_JAZZ_CharEffectSerialize_GSCBBase") or false

local PATTERN = "PlaceCharacterEffect%('([%w_]+)',%s*%)"
local REPL = "PlaceCharacterEffect('%1', {})"

local function lSanitize(data)
	if data == nil then
		return data
	end
	local fixed, count
	local ok, err = pcall(function()
		fixed, count = string.gsub(data, PATTERN, REPL)
	end)
	if not ok then
		print("[JAZZ] Save sanitize: gsub failed:", err)
		return data
	end
	if (count or 0) > 0 then
		print(string.format("[JAZZ] Save sanitize: fixed %d empty PlaceCharacterEffect props", count))
	end
	return fixed
end

local function lInstallCharacterEffectTolua()
	local cls = rawget(_G, "CharacterEffect")
	if type(cls) ~= "table" then
		return
	end
	function CharacterEffect:__toluacode(indent, pstr, GetPropFunc)
		if not pstr then
			local props = ObjPropertyListToLuaCode(self, indent, GetPropFunc) or "{}"
			return string.format("PlaceCharacterEffect('%s', %s)", self.class, props)
		end
		pstr:appendf("PlaceCharacterEffect('%s', ", self.class)
		local len = #pstr
		ObjPropertyListToLuaCode(self, indent, GetPropFunc, pstr)
		if #pstr == len then
			pstr:append("{}")
		end
		return pstr:append(")")
	end
end

local function lJazzLoadGameSessionData(data, metadata)
	data = lSanitize(data)
	local base = rawget(_G, "g_JAZZ_CharEffectSerialize_LoadBase")
	return base(data, metadata)
end

local function lJazzGameSpecificLoadCallback(folder, metadata)
	local base = rawget(_G, "g_JAZZ_CharEffectSerialize_GSCBBase")
	local prev = rawget(_G, "LoadGameSessionData")
	rawset(_G, "LoadGameSessionData", function(data, meta)
		return prev(lSanitize(data), meta)
	end)
	local ok, err = pcall(base, folder, metadata)
	rawset(_G, "LoadGameSessionData", prev)
	if not ok then
		return err
	end
	return err
end

local function lInstallLoadSanitize()
	-- Wrap once so CommonLib can close over us without Jazz↔CL recursion.
	if rawget(_G, "g_JAZZ_CharEffectSerialize_LoadWrapped") then
		return
	end
	local current = rawget(_G, "LoadGameSessionData")
	if type(current) ~= "function" or current == lJazzLoadGameSessionData then
		return
	end
	rawset(_G, "g_JAZZ_CharEffectSerialize_LoadBase", current)
	rawset(_G, "g_JAZZ_CharEffectSerialize_LoadWrapped", true)
	rawset(_G, "LoadGameSessionData", lJazzLoadGameSessionData)
	print("[JAZZ] Save sanitize: LoadGameSessionData wrapped")
end

local function lInstallGSCB()
	if rawget(_G, "g_JAZZ_CharEffectSerialize_GSCBWrapped") then
		return
	end
	local current = rawget(_G, "GameSpecificLoadCallback")
	if type(current) ~= "function" or current == lJazzGameSpecificLoadCallback then
		return
	end
	rawset(_G, "g_JAZZ_CharEffectSerialize_GSCBBase", current)
	rawset(_G, "g_JAZZ_CharEffectSerialize_GSCBWrapped", true)
	rawset(_G, "GameSpecificLoadCallback", lJazzGameSpecificLoadCallback)
	print("[JAZZ] Save sanitize: GameSpecificLoadCallback wrapped")
end

local function lInstall()
	lInstallCharacterEffectTolua()
	lInstallLoadSanitize()
	lInstallGSCB()
end

function OnMsg.ClassesBuilt()
	lInstallCharacterEffectTolua()
end

function OnMsg.ModsReloaded()
	lInstall()
end

function OnMsg.Autorun()
	lInstall()
end

lInstall()
