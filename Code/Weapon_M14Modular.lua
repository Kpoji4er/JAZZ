-- JAZZ-WEAPON-M14M21-001: one M14SAW. The sniper kit presents it as M21.
-- Calls FirearmBase.SetWeaponComponent; does not wrap it again.

JAZZ_M14_SNIPER_KIT = rawget(_G, "JAZZ_M14_SNIPER_KIT") or "JAZZ_M14_SniperKit"
JAZZ_M14_ART = rawget(_G, "JAZZ_M14_ART") or "JAZZ_Scope_M21_ART"

local KIT = JAZZ_M14_SNIPER_KIT
local ART = JAZZ_M14_ART
local SNIPER_ATTACKS = { "SingleShot", "JAZZ_JokerShot", "JAZZ_Bullseye" }

local function copy_list(source)
	local copy = {}
	for index, value in ipairs(source or empty_table) do
		copy[index] = value
	end
	return copy
end

function JAZZ_M14ApplyPresentation(weapon)
	if not weapon or weapon.class ~= "M14SAW" or not M14SAW then
		return
	end
	local kit = weapon.components and weapon.components.Conversion == KIT
	local base = kit and SniperRifle or BattleRifle
	local preset = kit and M21 or M14SAW
	weapon.object_class = kit and "SniperRifle" or "BattleRifle"
	if base then
		weapon.WeaponType = base.WeaponType
		weapon.ImpactForce = base.ImpactForce
	end
	local ancestors = {}
	for name, value in pairs(M14SAW.__ancestors or empty_table) do
		ancestors[name] = value
	end
	ancestors.SniperRifle = kit or nil
	ancestors.BattleRifle = (not kit) or nil
	weapon.__ancestors = ancestors
	weapon.AvailableAttacks = kit and copy_list(SNIPER_ATTACKS) or copy_list(M14SAW.AvailableAttacks)
	weapon.AimAccuracy = kit and 12 or M14SAW.AimAccuracy
	weapon.Grouping = kit and 45 or M14SAW.Grouping
	weapon.AutoShots = kit and 0 or M14SAW.AutoShots
	weapon.BurstShots = kit and 0 or M14SAW.BurstShots
	weapon.WeaponSizeClass = kit and "Long" or M14SAW.WeaponSizeClass
	if preset then
		weapon.DisplayName = preset.DisplayName
		weapon.DisplayNamePlural = preset.DisplayNamePlural
		weapon.Icon = preset.Icon
	end
end

function JAZZ_M14MigrateM21(weapon)
	if not weapon or weapon.class ~= "M21" then
		return
	end
	weapon.components = weapon.components or {}
	weapon.components.Conversion = KIT
	if weapon.components.Rail == "JAZZ_Rail_M21" then
		weapon.components.Rail = nil
	end
	if (weapon.components.Scope or "") == "" then
		weapon.components.Scope = ART
	end
	weapon.class = "M14SAW"
	if g_Classes and g_Classes.M14SAW then
		setmetatable(weapon, g_Classes.M14SAW)
	end
	JAZZ_M14ApplyPresentation(weapon)
end

function M14SAW:Setcomponents(components)
	self.components = components
	JAZZ_M14ApplyPresentation(self)
end

function M14SAW:SetWeaponComponent(slot, id, is_init)
	local had_scope = self.components and (self.components.Scope or "") ~= ""
	FirearmBase.SetWeaponComponent(self, slot, id, is_init)
	local kit = self.components and self.components.Conversion == KIT
	if kit and slot == "Conversion" and not had_scope and (self.components.Scope or "") == "" then
		FirearmBase.SetWeaponComponent(self, "Scope", ART, is_init)
	end
	JAZZ_M14ApplyPresentation(self)
	if ObjModified then
		ObjModified(self)
	end
end

function M14SAW:UpdateVisualObj(vis)
	JAZZ_M14ApplyPresentation(self)
	vis = vis or self.visual_obj
	if not IsValid(vis) or vis.weapon ~= self then
		return
	end
	FirearmBase.UpdateVisualObj(self, vis)
end
