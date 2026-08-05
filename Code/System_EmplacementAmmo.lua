-- Remap cut vanilla .50 ammo templates on MachineGunEmplacement to JAZZ calibers.
-- BrowningM2HMG uses JAZZ_Caliber_50BMG; map objects often still set ammo_template="_50BMG_Basic".
-- Vanilla Firearm:Reload does not reject caliber mismatch, but ImpactForce / cut ammo are wrong.

local JAZZ_EMPLACEMENT_AMMO_REMAP = {
	_50BMG_Basic = "JAZZ_AMMO_50BMG_Basic",
	_50BMG_HE = "JAZZ_AMMO_50BMG_API_HEI",
	_50BMG_Incendiary = "JAZZ_AMMO_50BMG_APIT",
	_50BMG_SLAP = "JAZZ_AMMO_50BMG_APIT",
}

g_JAZZ_EmplacementAmmoWrapped = rawget(_G, "g_JAZZ_EmplacementAmmoWrapped") or false
g_JAZZ_EmplacementAmmoUpdateBase = rawget(_G, "g_JAZZ_EmplacementAmmoUpdateBase") or false

local function lInstallEmplacementAmmoRemap()
	if rawget(_G, "g_JAZZ_EmplacementAmmoWrapped") then
		return
	end
	local cls = rawget(_G, "MachineGunEmplacement")
	if type(cls) ~= "table" then
		return
	end
	local base = cls.Update
	if type(base) ~= "function" then
		return
	end
	rawset(_G, "g_JAZZ_EmplacementAmmoUpdateBase", base)
	rawset(_G, "g_JAZZ_EmplacementAmmoWrapped", true)

	function MachineGunEmplacement:Update()
		local mapped = JAZZ_EMPLACEMENT_AMMO_REMAP[self.ammo_template]
		if mapped and InventoryItemDefs[mapped] then
			self.ammo_template = mapped
		elseif self.ammo_template and self.weapon_template then
			local weapon_def = InventoryItemDefs[self.weapon_template]
			local ammo_def = InventoryItemDefs[self.ammo_template]
			if weapon_def and ammo_def and ammo_def.Caliber ~= weapon_def.Caliber then
				local ammos = GetAmmosWithCaliber and GetAmmosWithCaliber(weapon_def.Caliber, "sort")
				local pick = ammos and ammos[1]
				if pick and pick.id and InventoryItemDefs[pick.id] then
					self.ammo_template = pick.id
				end
			end
		end
		return g_JAZZ_EmplacementAmmoUpdateBase(self)
	end
end

function OnMsg.ModsReloaded()
	lInstallEmplacementAmmoRemap()
end

function OnMsg.ClassesBuilt()
	lInstallEmplacementAmmoRemap()
end

lInstallEmplacementAmmoRemap()
