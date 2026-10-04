-- JAZZ-WEAPON-RAIL-001: one FNFAL. The tactical handguard renames the gun.
-- Calls FirearmBase.SetWeaponComponent; does not wrap it again.

local TAC = "JAZZ_FNFAL_TacHandguard"
local CLASSIC = {
	Reliability = 55,
	Recoil = 43,
	AimAccuracy = 13,
	WeaponRange = 56,
	BaseJamChance = 0,
}
local TACTICAL = {
	Reliability = 70,
	Recoil = 36,
	AimAccuracy = 14,
	WeaponRange = 57,
	BaseJamChance = -15,
}

function JAZZ_FALApplyPresentation(weapon)
	if not weapon or weapon.class ~= "FNFAL" then
		return
	end
	local tac = weapon.components and weapon.components.Handguard == TAC
	local stats = tac and TACTICAL or CLASSIC
	local source = tac and JAZZ_FNFAL_Tactical or FNFAL
	if source then
		weapon.DisplayName = source.DisplayName
		weapon.DisplayNamePlural = source.DisplayNamePlural
		weapon.Icon = source.Icon
	end
	for stat, value in pairs(stats) do
		weapon[stat] = value
	end
end

function FNFAL:Setcomponents(components)
	self.components = components
	JAZZ_FALApplyPresentation(self)
end

function FNFAL:SetWeaponComponent(slot, id, is_init)
	FirearmBase.SetWeaponComponent(self, slot, id, is_init)
	JAZZ_FALApplyPresentation(self)
	if ObjModified then
		ObjModified(self)
	end
end
