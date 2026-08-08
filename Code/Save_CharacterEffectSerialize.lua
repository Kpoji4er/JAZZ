-- HOTFIX: CharacterEffect with no non-default props serializes as
-- PlaceCharacterEffect('Id', ) which is invalid Lua and blocks save load.
-- Vanilla CharacterEffect:__toluacode always emits the comma; empty
-- ObjPropertyListToLuaCode then leaves a dangling ')'.
-- Mid-combat suppressionPinned often has only default CampaignTimeAdded.

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

-- Recover saves already written with PlaceCharacterEffect('Id', ).
g_JAZZ_LoadGameSessionDataSanitizeWrapped = rawget(_G, "g_JAZZ_LoadGameSessionDataSanitizeWrapped") or false
g_JAZZ_LoadGameSessionDataSanitizeBase = rawget(_G, "g_JAZZ_LoadGameSessionDataSanitizeBase") or false

local function lSanitizeCharacterEffectPlaceCalls(data)
	if type(data) ~= "string" then
		return data
	end
	-- PlaceCharacterEffect('Foo', )  →  PlaceCharacterEffect('Foo', {})
	return data:gsub("PlaceCharacterEffect%('([%w_]+)',%s*%)", "PlaceCharacterEffect('%1', {})")
end

local function lJazzLoadGameSessionData(data, metadata)
	data = lSanitizeCharacterEffectPlaceCalls(data)
	local base = rawget(_G, "g_JAZZ_LoadGameSessionDataSanitizeBase")
	return base(data, metadata)
end

local function lInstallLoadSanitize()
	local current = rawget(_G, "LoadGameSessionData")
	if current == lJazzLoadGameSessionData then
		return
	end
	if type(current) ~= "function" then
		return
	end
	-- Re-chain on every ModsReloaded so we stay outside CommonLib's sprocall wrap.
	rawset(_G, "g_JAZZ_LoadGameSessionDataSanitizeBase", current)
	rawset(_G, "g_JAZZ_LoadGameSessionDataSanitizeWrapped", true)
	rawset(_G, "LoadGameSessionData", lJazzLoadGameSessionData)
end

function OnMsg.ModsReloaded()
	lInstallLoadSanitize()
end

function OnMsg.Autorun()
	lInstallLoadSanitize()
end

lInstallLoadSanitize()
