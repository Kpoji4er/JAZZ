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

-- UndefineClass('FlareGun') drops vanilla methods. Area-aim targeting calls
-- ValidatePos; FireFlare uses GetAttackResults (not Firearm bullet LoF).
function FlareGun:GetBaseDamage()
	return 0
end

function FlareGun:ValidatePos(explosion_pos)
	return explosion_pos
end

function FlareGun:GetAttackResults(action, attack_args)
	local attacker = attack_args.obj
	local prediction = attack_args.prediction
	local stealth_kill
	local lof_idx = table.find(attack_args.lof, "target_spot_group", attack_args.target_spot_group or "Torso")
	local lof_data = (attack_args.lof or empty_table)[lof_idx or 1]
	local target_pos = attack_args.target_pos or lof_data and lof_data.target_pos or (IsValid(attack_args.target) and attack_args.target:GetPos())
	if not target_pos then
		return {}
	end
	if not target_pos:IsValidZ() then
		target_pos = target_pos:SetTerrainZ()
	end

	if not self.ammo or self.ammo.Amount <= 0 then
		return {}
	end

	local mishap
	if not prediction and IsKindOf(self, "MishapProperties") then
		local chance = self:GetMishapChance(attacker, target_pos)
		if CheatEnabled("AlwaysMiss") or attacker:Random(100) < chance then
			local dv = self:GetMishapDeviationVector(attacker, target_pos)
			mishap = true
			target_pos = target_pos + dv
			attacker:ShowMishapNotification(action)
		end
	end

	local jammed, condition = false, false
	if prediction then
		attack_args.jam_roll = 0
		attack_args.condition_roll = 0
	else
		attack_args.jam_roll = attack_args.jam_roll or (1 + attacker:Random(100))
		attack_args.condition_roll = attack_args.condition_roll or (1 + attacker:Random(100))
		jammed, condition = self:ReliabilityCheck(attacker, 1, attack_args.jam_roll, attack_args.condition_roll)
	end

	if jammed then
		return { jammed = true, condition = condition }
	end
	local aoe_params = self:GetAreaAttackParams(action.id, attacker, target_pos)
	aoe_params.stealth_kill = stealth_kill
	if attack_args.stealth_attack then
		aoe_params.stealth_attack_roll = not prediction and attacker:Random(100) or 100
	end

	aoe_params.prediction = prediction
	aoe_params.step_pos = target_pos
	local results = GetAreaAttackResults(aoe_params)
	results.ordnance = self.ammo
	results.weapon = self
	results.jammed = jammed
	results.condition = condition
	results.fired = not jammed and 1
	results.mishap = mishap
	results.explosion_pos = target_pos
	return results
end


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

function RocketLauncher:Reload(ammo, suspend_fx, delayed_fx, max_add)
	if self.DisposableLauncher then
		return false, false, false
	end
	local prev, played_fx, change = Firearm.Reload(self, ammo, suspend_fx, delayed_fx, max_add)
	self:UpdateRocket()
	return prev, played_fx, change
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