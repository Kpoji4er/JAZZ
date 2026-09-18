-- JAZZ-APPEAR-001: equipped Torso/Head visuals, JAZZ Legion only.
-- No item AttachEntries: those would also affect mercs using the same item.
g_JAZZ_LegionArmorHook = rawget(_G, "g_JAZZ_LegionArmorHook") or false
g_JAZZ_LegionArmorParts = rawget(_G, "g_JAZZ_LegionArmorParts") or setmetatable({}, { __mode = "k" })
g_JAZZ_LegionHatParts = rawget(_G, "g_JAZZ_LegionHatParts") or setmetatable({}, { __mode = "k" })

local function Color(r, g, b)
	return { r, g, b }
end

local armor_entities = {
	JazzArmor_TwaronLight = { Male = "JAZZ_TwaronLight_Male" },
	JazzArmor_TwaronMedium = { Male = "JAZZ_TwaronMedium_Male" },
	JazzArmor_TwaronFull = { Male = "JAZZ_TwaronFull_Male" },
	JazzArmor_GuardianLight = { Male = "JAZZ_GuardianLight_Male" },
	JazzArmor_GuardianMedium = { Male = "JAZZ_GuardianMedium_Male" },
	JazzArmor_GuardianFull = { Male = "JAZZ_GuardianFull_Male" },
	JazzArmor_ZylonLight = { Male = "JAZZ_ZylonLight_Male" },
	JazzArmor_ZylonMedium = { Male = "JAZZ_ZylonMedium_Male" },
	JazzArmor_ZylonFull = { Male = "JAZZ_ZylonFull_Male" },
	JazzArmor_ImprovisedCuirass = { Male = "JAZZ_ImprovisedCuirass_Male" },
	JazzArmor_Chainmail = { Male = "JAZZ_Chainmail_Male" },
	JazzArmor_TireBrigantine = { Male = "JAZZ_TireBrigantine_Male" },
	JazzArmor_TireArmor = { Male = "JAZZ_TireArmor_Male" },
	JazzArmor_FlakM1955 = { Male = "EquipmentMale_FlackVest", colors = { Color(61, 74, 46) } },
	JazzArmor_FlakM69 = { Male = "EquipmentMale_FlackVest", colors = { Color(78, 88, 52) } },
	JazzArmor_IBALight = {
		Male = "EquipmentMale_InterceptorVest_01",
		colors = { Color(52, 58, 48), Color(120, 120, 110), Color(0, 0, 0) },
	},
	JazzArmor_IBA = {
		Male = "EquipmentMale_InterceptorVest_02",
		colors = { Color(58, 72, 38), Color(40, 52, 28), Color(120, 120, 110) },
	},
	JazzArmor_IBAFull = {
		Male = "EquipmentMale_InterceptorVest_02",
		colors = { Color(42, 54, 30), Color(28, 38, 22), Color(120, 120, 110) },
	},
}

-- Hats use parts.Hat (Head spot), never the face mesh in parts.Head.
local hat_entities = {
	JazzArmor_UniformCap = {
		Male = "FactionMale_Hat_05", hide_hair = true,
		colors = { Color(58, 72, 38), Color(0, 0, 0), Color(0, 0, 0) },
	},
	JazzArmor_ConstructionHelmet = {
		Male = "Construction_Helmet_01", hide_hair = true,
		colors = { Color(200, 160, 20) },
	},
	JazzArmor_AdrianHelmet = {
		Male = "JungleCamp_GraveyardHelmet_02", hide_hair = true,
		colors = { Color(88, 98, 92) },
	},
	JazzArmor_SovietHelm = {
		Male = "FactionMale_Hat_09", hide_hair = true,
		colors = { Color(70, 78, 58), Color(70, 78, 58), Color(70, 78, 58) },
	},
	JazzArmor_M1Helm = {
		Male = "FactionMale_Hat_09", hide_hair = true,
		colors = { Color(61, 74, 46), Color(61, 74, 46), Color(48, 36, 26) },
	},
	JazzArmor_Stahlhelm = {
		Male = "EquipmentMale_WW2Helmet", hide_hair = true,
		colors = { Color(72, 78, 62), Color(48, 52, 42), Color(48, 52, 42) },
	},
	JazzArmor_PASGTHelm = {
		Male = "FactionMale_Hat_08", hide_hair = true,
		colors = { Color(61, 74, 46), Color(0, 0, 0), Color(61, 74, 46) },
	},
	JazzArmor_6b7Helm = {
		Male = "FactionMale_Hat_10", hide_hair = true,
		colors = { Color(55, 68, 42), Color(40, 48, 32), Color(40, 48, 32) },
	},
	JazzArmor_TwaronHelm = {
		Male = "FactionMale_Hat_10", hide_hair = true,
		colors = { Color(48, 78, 42), Color(32, 52, 30), Color(32, 52, 30) },
	},
	JazzArmor_TwaronHelmHeavy = {
		Male = "FactionMale_Hat_10", hide_hair = true,
		colors = { Color(40, 66, 36), Color(32, 52, 30), Color(32, 52, 30) },
	},
	JazzArmor_ZylonHelm = {
		Male = "FactionMale_Hat_11", hide_hair = true,
		colors = { Color(58, 72, 38) },
	},
	JazzArmor_ZylonHelmHeavy = {
		Male = "FactionMale_Hat_11", hide_hair = true,
		colors = { Color(58, 72, 38) },
	},
	JazzArmor_GuardianHelm = {
		Male = "FactionMale_Hat_10", hide_hair = true,
		colors = { Color(78, 80, 82), Color(52, 54, 56), Color(52, 54, 56) },
	},
	JazzArmor_GuardianHelmHeavy = {
		Male = "FactionMale_Hat_10", hide_hair = true,
		colors = { Color(58, 60, 62), Color(52, 54, 56), Color(52, 54, 56) },
	},
}

local function CollectEntities(map)
	local dest = {}
	for _, entry in pairs(map) do
		for key, value in pairs(entry) do
			if (key == "Male" or key == "Female") and type(value) == "string" then
				dest[value] = true
			end
		end
	end
	return dest
end

local managed_armor = CollectEntities(armor_entities)
local managed_hats = CollectEntities(hat_entities)

local function IsLegion(unit)
	local id = unit and unit.unitdatadef_id
	return IsValid(unit) and IsKindOf(unit, "Unit") and type(id) == "string"
		and id:sub(1, 12) == "JAZZ_Legion_"
end

local function TintPart(part, colors)
	if not part or not colors then return end
	local rgb = rawget(_G, "RGB")
	local set_mat = part.SetColorizationMaterial
	if type(rgb) ~= "function" or type(set_mat) ~= "function" then return end
	for i = 1, 3 do
		local c = colors[i]
		if type(c) == "table" then
			set_mat(part, i, rgb(c[1], c[2], c[3]), 0, 0)
		end
	end
end

local function SetHairHidden(unit, hide)
	local hair = unit.parts and unit.parts.Hair
	if not IsValid(hair) then return end
	if type(hair.SetVisible) == "function" then
		hair:SetVisible(not hide)
	elseif type(hair.SetOpacity) == "function" then
		hair:SetOpacity(hide and 0 or 100)
	end
end

local function CreateMappedPart(unit, part_name, entity, colors, colorize_baseline)
	local part = PlaceObject("AppearanceObjectPart")
	part:ChangeEntity(entity)
	part:ClearEnumFlags(const.efCollision | const.efWalkable | const.efApplyToGrids)
	if unit:GetGameFlags(const.gofRealTimeAnim) ~= 0 then
		part:SetGameFlags(const.gofRealTimeAnim)
	end
	unit.parts[part_name] = part
	unit:ApplyPartSpotAttachments(part_name)
	if colorize_baseline then
		unit:ColorizePart(part_name)
	else
		TintPart(part, colors)
	end
	return part
end

local function ResolveEntry(unit, slot, map)
	if not IsLegion(unit) then return end
	local item = unit:GetItemInSlot(slot, "Armor")
	local entry = item and map[item.class]
	if not entry then return end
	local entity = entry[unit.gender]
	if entity and not IsValidEntity(entity) then entity = nil end
	if not entity then return end
	return entity, entry.colors, entry.hide_hair, item.class
end

local function PartEntity(part)
	return IsValid(part) and type(part.GetEntity) == "function" and part:GetEntity()
end

local function ApplyMapped(unit, cache, slot, part_name, map, managed, baseline_key)
	if not IsValid(unit) or not unit.parts then return end
	local state = cache[unit]
	local current = unit.parts[part_name]
	if not state and PartEntity(current) and managed[current:GetEntity()] then
		local presets = rawget(_G, "AppearancePresets") or {}
		local preset = presets[unit.Appearance]
		state = {
			part = current,
			entity = current:GetEntity(),
			baseline = preset and preset[baseline_key],
		}
		cache[unit] = state
	end
	if state and (current ~= state.part or not IsValid(state.part)) then
		cache[unit] = nil
		state = nil
	end
	local entity, colors, hide_hair, item_class = ResolveEntry(unit, slot, map)
	if not entity then
		if state then
			DoneObject(state.part)
			unit.parts[part_name] = nil
			cache[unit] = nil
			if state.baseline and IsValidEntity(state.baseline) then
				CreateMappedPart(unit, part_name, state.baseline, nil, true)
			end
			if part_name == "Hat" then SetHairHidden(unit, false) end
		end
		return
	end
	if state and state.entity == entity then
		if state.item ~= item_class then
			TintPart(current, colors)
			state.item = item_class
		end
		if hide_hair then SetHairHidden(unit, true) end
		return
	end
	local baseline = IsValid(current) and current:GetEntity()
	if state then baseline = state.baseline end
	if IsValid(current) then DoneObject(current) end
	unit.parts[part_name] = nil
	local part = CreateMappedPart(unit, part_name, entity, colors)
	cache[unit] = { part = part, baseline = baseline, entity = entity, item = item_class }
	if hide_hair then SetHairHidden(unit, true) end
end

local function ApplyVisuals(unit)
	ApplyMapped(unit, g_JAZZ_LegionArmorParts, "Torso", "Armor", armor_entities, managed_armor, "Armor")
	ApplyMapped(unit, g_JAZZ_LegionHatParts, "Head", "Hat", hat_entities, managed_hats, "Hat")
end

local function InstallArmorHook()
	local unit_class = rawget(_G, "Unit")
	if type(unit_class) ~= "table" or type(unit_class.UpdateItemAppearance) ~= "function" then return end
	local hook = g_JAZZ_LegionArmorHook
	if hook and hook.owner == unit_class then
		-- Never capture a second/foreign wrapper on the same live class.
		-- Refresh the callback for code reload; existing wrapper remains unique.
		hook.apply = ApplyVisuals
		return
	end
	hook = { owner = unit_class, base = unit_class.UpdateItemAppearance, apply = ApplyVisuals,
		busy = setmetatable({}, { __mode = "k" }) }
	hook.wrapper = function(self, ...)
		if hook.busy[self] then return hook.base(self, ...) end
		hook.busy[self] = true
		local result = table.pack(pcall(hook.base, self, ...))
		hook.busy[self] = nil
		if not result[1] then error(result[2], 0) end
		hook.apply(self)
		return table.unpack(result, 2, result.n)
	end
	unit_class.UpdateItemAppearance = hook.wrapper
	rawset(_G, "g_JAZZ_LegionArmorHook", hook)
end

local function QueueArmorUpdate(unit)
	if not IsLegion(unit) then return end
	local update = rawget(_G, "UpdateItemAppearanceDelayed")
	if type(update) == "function" then update(unit) end
end

function OnMsg.ItemAdded(unit, item, slot)
	if slot == "Torso" or slot == "Head" then QueueArmorUpdate(unit) end
end

function OnMsg.ItemRemoved(unit, item, slot)
	if slot == "Torso" or slot == "Head" then QueueArmorUpdate(unit) end
end

function OnMsg.InventoryChange(unit)
	QueueArmorUpdate(unit)
end

function OnMsg.ClassesBuilt()
	InstallArmorHook()
end

function OnMsg.ModsReloaded()
	InstallArmorHook()
end

function OnMsg.LoadGame()
	InstallArmorHook()
	for _, unit in ipairs(rawget(_G, "g_Units") or {}) do QueueArmorUpdate(unit) end
end

InstallArmorHook()
