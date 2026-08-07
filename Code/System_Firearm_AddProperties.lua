FirearmProperties.properties[#FirearmProperties.properties+1] = {
    category = "New Weapon System - Autofire",
    id = "Recoil",
    name = "Recoil",
    help = "Accuracy retention loss for follow-up bullets; lower is easier to control",
    editor = "number",
    default = 100,
    template = true,
    min = 0,
    max = 100,
    modifiable = true
}

FirearmProperties.properties[#FirearmProperties.properties+1] = {
    category = "New Weapon System - Reload",
    id = "ReloadStyle",
    name = "Reload Style",
    help = "Magazine reloads fully; Tube, Break, and Revolver can top up one round when partially loaded.",
    editor = "choice",
    items = { "Magazine", "Tube", "Break", "Revolver" },
    default = "Magazine",
    template = true,
    modifiable = false
}

FirearmProperties.properties[#FirearmProperties.properties+1] = {
    category = "New Weapon System",
    id = "MaxAimActions",
    name = "Max Aim Actions",
    help = "Количество кликов прицеливания",
    editor = "number",
    template = true,
    min = 0,
    max = 10,
    modifiable = true
}


FirearmProperties.properties[#FirearmProperties.properties+1] = {
    category = "New Weapon System - Autofire",
    id = "BurstShots",
    name = "BurstShots",
    help = "Количество патрон в короткой очереди",
    editor = "number",
    default = 3,
    template = true,
    min = 0,
    max = 20,
    modifiable = true
}

FirearmProperties.properties[#FirearmProperties.properties+1] = {
    category = "New Weapon System - Autofire",
    id = "AutoShots",
    name = "AutoShots",
    help = "Количество патрон в длинной очереди",
    editor = "number",
    default = 10,
    template = true,
    min = 0,
    max = 25,
    modifiable = true
}

-- JAZZ-WEAPONS-006: pellet base for Shotgun multishot (ammo CaliberModification target).
-- Not AutoShots — that stays WEAPONS-003 autofire length.
FirearmProperties.properties[#FirearmProperties.properties+1] = {
    category = "Caliber",
    id = "BuckshotProjectiles",
    name = "Buckshot Projectiles",
    help = "Base pellet count per shell; 12g ammo multiplies this (Buckshot ×9, Birdshot ×20).",
    editor = "number",
    default = 1,
    template = true,
    min = 0,
    max = 40,
    modifiable = true
}

FirearmProperties.properties[#FirearmProperties.properties+1] = {
    category = "New Weapon System - Physical Recoil",
    id = "WeaponMass",
    name = "Weapon Mass",
    help = "Authored unloaded weapon mass in tenths of a kilogram; used to calibrate base recoil.",
    editor = "number",
    default = 35,
    template = true,
    min = 1,
    max = 200,
    modifiable = true
}

FirearmProperties.properties[#FirearmProperties.properties+1] = {
    category = "New Weapon System - Physical Recoil",
    id = "CyclicRPM",
    name = "Cyclic RPM",
    help = "Authored cyclic rate of fire; source for burst and autofire shot counts.",
    editor = "number",
    default = 0,
    template = true,
    min = 0,
    max = 2000,
    modifiable = true
}

FirearmProperties.properties[#FirearmProperties.properties+1] = {
    category = "New Weapon System - Physical Recoil",
    id = "WeaponSizeClass",
    name = "Weapon Size Class",
    help = "Editor-only physical size proxy used to calibrate base recoil.",
    editor = "choice",
    items = { "Compact", "Carbine", "Rifle", "Long" },
    default = "Rifle",
    template = true,
    modifiable = true
}

FirearmProperties.properties[#FirearmProperties.properties+1] = {
    category = "New Weapon System - Physical Recoil",
    id = "BurstLimiter",
    name = "Burst Limiter",
    help = "Mechanical burst cutoff; 0 means no cutoff.",
    editor = "number",
    default = 0,
    template = true,
    min = 0,
    max = 8,
    modifiable = true
}



--deprecated
--FirearmProperties.properties[#FirearmProperties.properties+1] = {
--    category = "New Weapon System",
--    id = "EffectiveRange",
--    name = "EffectiveRange",
--    help = "Расстояние 100% точности",
--    editor = "number",
--    default = 0,
--    template = true,
--    min = -10,
--    max = 50,
--    modifiable = true
--}

--FirearmProperties.properties[#FirearmProperties.properties+1] = {
--    category = "New Weapon System",
--    id = "Deterioration",
--    name = "Deterioration",
--    help = "Уровень износа",
--    editor = "number",
--    default = 0,
--    template = false,
--    min = 0,
--    max = 100,
--    modifiable = false
--}

FirearmProperties.properties[#FirearmProperties.properties+1] = {
    category = "New Weapon System",
    id = "OverwatchAngle",
    name = "Overwatch Angle",
    help = "overwatch area cone angle",
    editor = "number",
    default = 2400,
    template = true,
    scale = "deg",
    slider = true,
    min = 1,
    max = 5400,
    modifiable = true
}


FirearmProperties.properties[#FirearmProperties.properties+1] = {
    category = "New Weapon System",
    id = "CloseRange",
    name = "Close Range",
    help = "Tiles of near inefficiency (0 = none). Barrel components shift this; optic MinRange stacks on top.",
    editor = "number",
    default = 0,
    template = true,
    min = 0,
    max = 40,
    modifiable = true
}

FirearmProperties.properties[#FirearmProperties.properties+1] = {
    category = "New Weapon System",
    id = "CloseRangeFactor",
    name = "Close Range Factor",
    help = "CTH multiplier at distance 0 as percent (100 = neutral; >100 = CQB buff). Lerps to 100% at CloseRange tiles. Runtime clamp 25..150.",
    editor = "number",
    default = 100,
    template = true,
    min = 25,
    max = 150,
    modifiable = true
}

FirearmProperties.properties[#FirearmProperties.properties+1] = {
    category = "New Weapon System",
    id = "BulletDropRange",
    name = "Bullet Drop Range",
    help = "Дальность падения пули",
    editor = "number",
    default = 0,
    template = true,
    min = 0,
    max = 100,
    modifiable = true
}

FirearmProperties.properties[#FirearmProperties.properties+1] = {
    category = "New Weapon System",
    id = "Grouping",
    name = "Grouping",
    help = "Кучность",
    editor = "number",
    default = 0,
    template = true,
    min = 0,
    max = 1000,
    modifiable = true
}

FirearmProperties.properties[#FirearmProperties.properties+1] = {
    category = "New Weapon System",
    id = "BaseJamChance",
    name = "Jam Chance",
    help = "JamScore units (10 ≈ 1%): positive values set a fault-risk floor against (100 - Reliability), negative values reduce that reliability risk; serviceable base is capped at 10%",
    editor = "number",
    default = 0,
    template = true,
    min = -100,
    max = 100,
    modifiable = true
}

FirearmProperties.properties[#FirearmProperties.properties+1] = {
    category = "New Weapon System",
    id = "PenetrationBonus",
    name = "Penetration Bonus",
    help = "Бонус к пробитию брони",
    editor = "number",
    default = 0,
    template = true,
    min = -100,
    max = 100,
    modifiable = true
}

WeaponComponent.properties[#WeaponComponent.properties+1] = {
    category = "General",
    id = "ChipIcon",
    name = "Chip Icon",
    help = "Миниатюра для inventory/HUD chips (JAZZ-UI-001). Пара к Icon: кабинет моддинга = Icon, тайл = ChipIcon.",
    editor = "ui_image",
    template = true,
    default = "",
    image_preview_size = 40,
}

WeaponComponent.properties[#WeaponComponent.properties+1] = {
    category = "Scope Visuals",
    id = "ReticleInner",
    name = "Reticle Inner",
    help = "Сетка прицела",
    editor = "ui_image",
    template = true,
    default =  "",
    image_preview_size = 75
}

WeaponComponent.properties[#WeaponComponent.properties+1] = {
    category = "Scope Visuals",
    id = "ReticleInnerSub",
    name = "Reticle Inner (Sub)",
    help = "Сетка прицела (для доп прицела)",
    editor = "ui_image",
    template = true,
    default =  "",
    image_preview_size = 75
}

WeaponComponent.properties[#WeaponComponent.properties+1] = {
    category = "Scope Visuals",
    id = "ReticleOuter",
    name = "Reticle Outer",
    help = "Обводка прицела",
    editor = "ui_image",
    default = 0,
    template = true,
    default =  "",
    image_preview_size = 75
}

FirearmProperties.properties[#FirearmProperties.properties+1] = {
    category = "New Weapon Condition",
    id = "WeaponResource",
    name = "Weapon Resource",
    help = "Ресурс оружия",
    editor = "number",
    default = 1000,
    template = true,
    min = 0,
    max = 50000,
    modifiable = true
}




FirearmProperties.properties[#FirearmProperties.properties+1] = {
    category = "New Weapon Condition",
    id = "WeaponResourceMax",
    name = "Weapon Resource",
    help = "Ресурс оружия Макс",
    editor = "number",
    default = -1,
    template = false,
    min = -1,
    max = 50000,
    modifiable = true
}
FirearmProperties.properties[#FirearmProperties.properties+1] = {
    category = "New Weapon Condition",
    id = "DegradePerShot",
    name = "Degrade per shot",
    help = "Деградация за выстрел",
    editor = "number",
    default = 1,
    template = true,
    min = 1,
    max = 10,
    modifiable = true
}


WeaponComponentVisual.properties[#WeaponComponentVisual.properties+1] = {
    id = "WeaponName",
    name = "Weapon Name",
    help = "Изменение названия оружия",
    editor = "text",
    default = "",
}

WeaponComponentVisual.properties[#WeaponComponentVisual.properties+1] = {
    id = "WeaponIconMod",
    name = "WeaponIcon Mod",
    help = "Доп иконка модификации",
    editor = "ui_image",
    default = 0,
    template = true,
    default =  "",
    image_preview_size = 75
}

InventoryItemProperties.properties[#InventoryItemProperties.properties+1] = {
    category = "General",
    id = "UnitSubStat",
    name = "Unit Stat (Second)",
    help = "Unit Properties stat.",
    editor = "choice",
    items = function (self) return GetUnitStatsCombo() end,
    default = false,
    template = true,

}



SetPropMeta("BobbyRayShopItemProperties", "Tier", "max", 10)
SetPropMeta("BobbyRayShopItemProperties", "ShopStackSize", "max", 500)

-- PrepareShopItemsForRestock does `item.Tier <= unlocked_tier` (number). String Tier
-- (e.g. Tier = "5" in a companion) Asserts during BobbyRayStoreRestock.
local function JazzCoerceBobbyRayNumericTiers()
	local foreach = rawget(_G, "ForEachPreset")
	if type(foreach) ~= "function" then
		return
	end
	foreach("InventoryItemCompositeDef", function(preset)
		local item = g_Classes and preset and g_Classes[preset.id]
		if item and type(item.Tier) == "string" then
			local n = tonumber(item.Tier)
			if n then
				item.Tier = n
			end
		end
	end)
end

function OnMsg.ClassesBuilt()
	JazzCoerceBobbyRayNumericTiers()
end

function OnMsg.DataLoaded()
	JazzCoerceBobbyRayNumericTiers()
end



local function JazzInventoryDefProperty(class_id, prop, fallback)
	local def = InventoryItemDefs and class_id and InventoryItemDefs[class_id]
	if not def then
		return fallback
	end
	local val = rawget(def, prop)
	if type(val) ~= "number" then
		local ok, prop_val = pcall(def.GetProperty, def, prop)
		if ok then
			val = prop_val
		end
	end
	if type(val) == "number" then
		return val
	end
	return fallback
end

function InventoryItem:GetMaxResource()
	return JazzInventoryDefProperty(self.class, "Condition", 100)
end

function InventoryItem:GetMaxCondition()
	return JazzInventoryDefProperty(self.class, "Condition", 100)
end

function InventoryItem:GetFactoryResource()
	return JazzInventoryDefProperty(self.class, "Condition", 100)
end

function FirearmBase:GetFactoryResource()
	local val = JazzInventoryDefProperty(self.class, "WeaponResource", nil)
	if type(val) == "number" and val > 0 then
		return val
	end
	return 1000
end

function InventoryItem:GetCurrentResource()
    return self.Condition
end


function FirearmBase:GetMaxResource()
    local WeaponResourceMax = 0
    if self.WeaponResourceMax and self.WeaponResourceMax >= 0 then
        WeaponResourceMax = self.WeaponResourceMax
    else
        WeaponResourceMax = self:GetFactoryResource()
    end
	return WeaponResourceMax 
end

function FirearmBase:GetCurrentResource()
	return self.WeaponResource or self:GetFactoryResource()
end

function Inventory:ItemModifyCondition(item, amount)
	if not item:HasCondition() then
		return
	end
	local prev = item.Condition
	local newValue = Max(0, item.Condition + amount)
	item.Condition = newValue
	Msg("InventoryChange", self)
	if prev~=newValue then
		Msg("ItemChangeCondition", item, prev, newValue, self)
	end	

    if item.WeaponResource then
        item.WeaponResource = MulDivRound(item:GetMaxResource(), newValue, 100)
     end
    if item.ArmorResource then 
        item.ArmorResource = MulDivRound(item:GetMaxResource(), newValue, 100)
    end



	ObjModified(item)
	ObjModified(self)
	
	return newValue
end

function Firearm:CanAutofire()
	return table.find(self.AvailableAttacks, "AutoFire") or self:HasComponent("EnableFullAuto")
end

function Firearm:CanBurstfire()
	return table.find(self.AvailableAttacks, "BurstFire") or self:HasComponent("EnableBurst")
end



--Add property to weapon modification menu
function GetWeaponModifyProperties(item)		
	local statList = {}
	local dmgPreset = Presets.WeaponPropertyDef.Default.Damage
	statList[#statList + 1] = { max = dmgPreset.max_progress, bind_to = dmgPreset.bind_to }
	
	local baseAttack = item.GetBaseAttack and item:GetBaseAttack(false, "force")
	local baseAction = baseAttack and CombatActions[baseAttack]
	local baseAttackPreset = Presets.WeaponPropertyDef.Default.ShootAP
	local base_attack_name = baseAction and (baseAction.DisplayNameShort or baseAction.DisplayName) or ""
	statList[#statList + 1] = {
		GetShootAP = function(it)
			return baseAttackPreset:GetProp(it or item)/const.Scale.AP
		end,
		Getbase_ShootAP = function(it)
			return baseAttackPreset:Getbase_Prop(it or item)/const.Scale.AP
		end,
		max = 10,
		display_name = T{310685041358, "Attack Cost (<Name>)", Name = base_attack_name},
		id = "ShootAP",
		reverse_bar = true,
		description = baseAttackPreset.description
	}

	local rangePreset = Presets.WeaponPropertyDef.Default.WeaponRange
	statList[#statList + 1] = { max = rangePreset.max_progress, bind_to = rangePreset.bind_to }

	local GroupingPreset = Presets.WeaponPropertyDef.Default.Grouping
	statList[#statList + 1] = { max = GroupingPreset.max_progress, bind_to = GroupingPreset.bind_to }

	if (item.BulletDropRange or 0) > 0 then
		local effRange = Presets.WeaponPropertyDef.Default.BulletDropRange
		statList[#statList + 1] = { max = effRange.max_progress, bind_to = effRange.bind_to }
	end

	local aimAcc = Presets.WeaponPropertyDef.Default.AimAccuracy
	statList[#statList + 1] = { max = aimAcc.max_progress, bind_to = aimAcc.bind_to }

	local MaxAimActions = Presets.WeaponPropertyDef.Default.MaxAimActions
	statList[#statList + 1] = { max = MaxAimActions.max_progress, bind_to = MaxAimActions.bind_to }

	local critPreset = item.owner and Presets.WeaponPropertyDef.Default.CritChance or Presets.WeaponPropertyDef.Default.MaxCritChance
	local weaponModDlg = GetDialog("ModifyWeaponDlg").idModifyDialog
	local unit_id = weaponModDlg.context.owner
	statList[#statList + 1] = {
		GetCritChance = function(it)
			return critPreset:GetProp(it or item, unit_id)
		end,
		Getbase_CritChance = function(it)
			return critPreset:Getbase_Prop(it or item, unit_id)
		end,
		max = critPreset.max_progress,
		display_name = critPreset.display_name,
		id = "CritChance",
		description = critPreset.description
	}

	-- Recoil/burst bars: do not gate only on GetBaseAttack (often SingleShot).
	-- Component-gated select-fire (M2Carbine/Mini14) keeps semi AvailableAttacks until
	-- EnableBurst/EnableFullAuto, but still authors Recoil/BurstShots/AutoShots.
	local base_id = baseAction and baseAction.id
	local can_burst = item.CanBurstfire and item:CanBurstfire()
	local can_auto = item.CanAutofire and item:CanAutofire()
	local has_burst_shots = (item.BurstShots or 0) > 0
	local has_auto_shots = (item.AutoShots or 0) > 0
	local show_recoil = base_id == "AutoFire" or base_id == "BurstFire" or base_id == "MGBurstFire"
		or can_burst or can_auto or has_burst_shots or has_auto_shots
	if show_recoil then
		local recoil = Presets.WeaponPropertyDef.Default.Recoil
		if recoil and (item.Recoil or 0) > 0 then
			statList[#statList + 1] = { max = recoil.max_progress, bind_to = recoil.bind_to }
		end
		if can_burst or has_burst_shots or base_id == "BurstFire" or base_id == "MGBurstFire" then
			local BurstShots = Presets.WeaponPropertyDef.Default.BurstShots
			if BurstShots then
				statList[#statList + 1] = { max = BurstShots.max_progress, bind_to = BurstShots.bind_to }
			end
		end
	end

	if can_auto or has_auto_shots or table.find(item.AvailableAttacks, "AutoFire") then
		local AutoShots = Presets.WeaponPropertyDef.Default.AutoShots
		if AutoShots then
			statList[#statList + 1] = { max = AutoShots.max_progress, bind_to = AutoShots.bind_to }
		end
	end

	local Reliability = Presets.WeaponPropertyDef.Default.Reliability
	statList[#statList + 1] = { max = Reliability.max_progress, bind_to = Reliability.bind_to }

	local Noise = Presets.WeaponPropertyDef.Default.Noise
	statList[#statList + 1] = { max = Noise.max_progress, bind_to = Noise.bind_to }

	return statList
end

--[[
function GetWeaponComponentDescription(componentPreset)
	local data = GetWeaponComponentDescriptionData(componentPreset)
	local lines = {}

    local headerText = _InternalTranslate(
        T{987654321, "<style WeaponModHeader><DisplayName></style>", componentPreset}
      )
      table.insert(lines, { display = Untranslated(headerText) })

	if componentPreset.Description then
		lines[#lines + 1] = T{componentPreset.Description, componentPreset}
	end
	
	local indices = {}
	for modName, mod in sorted_pairs(data) do
		local text = Untranslated("<bullet_point> " .. _InternalTranslate(mod.display, mod))
		lines[#lines + 1] = text
		
		local effect = WeaponComponentEffects[modName]
		if effect then
			indices[text] = effect.SortKey
		end
	end
	
	if #lines == 0 then
		return T(575725466022, "No changes")
	end
	
	table.sort(lines, function(a, b)
		local indexA = indices[a] or 0
		local indexB = indices[b] or 0
		return indexA < indexB
	end)
	
	return table.concat(lines, "\n"), data
end
]]

-- Inventory weapon card: CloseRange lives in RolloverInventoryWeaponBase (RolloverPropTextRight),
-- same block as Grouping / BulletDropRange / JamChance / Noise — not AdditionalHint bullets.
-- Prefer component Factor boost (resolved − base_*), matching barrel effect phrasing
-- («на 12»), not Factor−100 (Ithaca short: 102 → +2 hides +12).
local function JAZZ_GetWeaponCloseRangeNum(weapon, id, default)
	local value
	if weapon.GetProperty then
		value = weapon:GetProperty(id)
	end
	if value == nil then
		value = weapon[id]
	end
	if value == nil then
		return default
	end
	return tonumber(value) or default
end

-- Returns name_t, value_t for the inventory rollover row, or nil when the row should hide.
function JAZZ_GetWeaponCloseRangeRolloverTexts(weapon)
	if not weapon or not IsKindOf(weapon, "FirearmProperties") then
		return
	end
	local close_range = Max(0, JAZZ_GetWeaponCloseRangeNum(weapon, "CloseRange", 0))
	local factor = Clamp(JAZZ_GetWeaponCloseRangeNum(weapon, "CloseRangeFactor", 100), 25, 150)
	-- Runtime only lerps when CloseRange > 0 (see AccuracyRangeCTH).
	if close_range <= 0 then
		return
	end
	local base_factor = tonumber(weapon["base_CloseRangeFactor"])
	if base_factor == nil then
		base_factor = factor
	end
	local factor_boost = factor - base_factor
	local name = T(982641736210, "Ближняя зона")
	if factor_boost > 0 then
		return name, T{
			890000000001937,
			"+<bonus> (<tiles> кл.)",
			bonus = factor_boost,
			tiles = close_range,
		}
	end
	if factor == 100 then
		return
	end
	if factor > 100 then
		return name, T{
			890000000001937,
			"+<bonus> (<tiles> кл.)",
			bonus = factor - 100,
			tiles = close_range,
		}
	end
	return name, T{
		890000000001938,
		"−<penalty>% (<tiles> кл.)",
		penalty = 100 - factor,
		tiles = close_range,
	}
end

function JAZZ_ShouldShowWeaponCloseRangeRollover(weapon)
	local name = JAZZ_GetWeaponCloseRangeRolloverTexts(weapon)
	return not not name
end
