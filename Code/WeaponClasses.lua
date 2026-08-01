UndefineClass('Pistol')
UndefineClass('Revolver')
UndefineClass('SniperRifle')
UndefineClass('SubmachineGun')
UndefineClass('Shotgun')
UndefineClass('AssaultRifle')
UndefineClass('MachineGun')
UndefineClass('FlareGun')
UndefineClass('MacheteWeapon')
UndefineClass('RocketLauncher')
UndefineClass('GrenadeLauncher')
UndefineClass('Mortar')

DefineClass.Pistol = { __parents = { "Firearm", }, WeaponType = "Pistol", ImpactForce = -1, }
DefineClass.Autopistol = { __parents = { "Firearm", }, WeaponType = "Autopistol", ImpactForce = -1, }
DefineClass.Revolver = { __parents = { "Firearm", }, WeaponType = "Revolver", ImpactForce = 0, }
DefineClass.SniperRifle = { __parents = { "Firearm", }, WeaponType = "Sniper", ImpactForce = 0, }
DefineClass.SubmachineGun = { __parents = { "Firearm", }, WeaponType = "SMG", ImpactForce = 0, }
DefineClass.Shotgun = { __parents = { "Firearm", }, WeaponType = "Shotgun", ImpactForce = 2, }
DefineClass.Carbine = { __parents = { "Firearm", }, WeaponType = "Carbine", ImpactForce = 1, }
DefineClass.AssaultRifle = { __parents = { "Firearm", }, WeaponType = "AssaultRifle", ImpactForce = 1, }
DefineClass.BattleRifle = { __parents = { "Firearm", }, WeaponType = "BattleRifle", ImpactForce = 2, }
DefineClass.LightMachineGun = { __parents = { "Firearm", },  WeaponType = "LightMachineGun", ImpactForce = 2, }
DefineClass.MachineGun = { __parents = { "Firearm", }, WeaponType = "MachineGun", ImpactForce = 2, }
DefineClass.FlareGun = { __parents = { "Firearm", "MishapProperties" }, WeaponType = "FlareGun" }
DefineClass.MacheteWeapon = { __parents = { "MeleeWeapon" }, WeaponType = "MeleeWeapon" }


DefineClass.RocketLauncher = { 
	__parents = {"HeavyWeapon"}, 
	properties = {
		{ category = "Combat", id = "BackfireRange", editor = "number", min = 0, default = 3, template = true, },
		{ category = "Combat", id = "BackfireConeAngle", editor = "number", min = 0, scale = "deg", default = 30*60, template = true, },
		{ category = "Combat", id = "BackfireDamage", editor = "number", min = 0, default = 10, template = true, },
		{ category = "Combat", id = "DisposableLauncher", editor = "bool", default = false, template = true, },
		{ category = "Combat", id = "EmbeddedOrdnance", editor = "text", default = false, template = true, },
	},
	trajectory_type = "line", 
	WeaponType = "MissileLauncher", 
	RolloverClassTemplate = "HeavyWeapon",
}

DefineClass.GrenadeLauncher = { __parents = {"HeavyWeapon"}, trajectory_type = "parabola", WeaponType = "GrenadeLauncher", RolloverClassTemplate = "HeavyWeapon"}
DefineClass.Mortar = { __parents = {"HeavyWeapon"}, trajectory_type = "bombard", WeaponType = "Mortar", RolloverClassTemplate = "HeavyWeapon"}


function GrenadeLauncher:GetBaseDegradePerShot()
	return self.DegradePerShot or const.Weapons.DegradePerShot_GrenadeLauncher
end

function RocketLauncher:GetBaseDegradePerShot()
	return self.DegradePerShot or const.Weapons.DegradePerShot_RocketLauncher
end

function Mortar:GetBaseDegradePerShot()
	return self.DegradePerShot or const.Weapons.DegradePerShot_Mortar
end


function RocketLauncher:UpdateRocket()
	local visual_obj = self.visual_obj
	if not IsValid(visual_obj) then return end
	
	visual_obj:DestroyAttaches("OrdnanceVisual")
	if self.ammo and self.ammo.Amount > 0 then
		local rocket = PlaceObject("OrdnanceVisual", {fx_actor_class = self.ammo.class})
		visual_obj:Attach(rocket, visual_obj:GetSpotBeginIndex("Muzzle"))
	end
end

function RocketLauncher:OnUnloadWeapon()
	self:UpdateRocket()
end

function RocketLauncher:Reload(...)
	Firearm.Reload(self, ...)
	self:UpdateRocket()
end

function RocketLauncher:UpdateVisualObj(...)
	Firearm.UpdateVisualObj(self, ...)
	self:UpdateRocket()
end

local WeaponTypePrefix = {
	["Handgun"] = "hg_",
	["Pistol"] = "hg_",
	["Autopistol"] = "hg_",
	["Revolver"] = "hg_",
	["FlareGun"] = "hg_",
	["MissileLauncher"] = "hw_",
	["Mortar"] = "nw_",
	["MeleeWeapon"] = "mk_",
}

function GetWeaponAnimPrefix(weapon, weapon2)
	if not weapon or weapon.IsUnarmed then
		return "nw_"
	elseif weapon2 then
		if next(weapon.subweapons) then
			for slot, sub in pairs(weapon.subweapons) do
				if sub == weapon2 then
					weapon2 = nil
					break
				end
			end
		end
		if weapon2 then
			return "dw_"
		end
	end
	return WeaponTypePrefix[weapon.WeaponType] or "ar_"
end