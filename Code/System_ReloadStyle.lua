-- JAZZ-WEAPONS-004: per-round reloads for tube, break-action, and revolver firearms.
-- CombatAction.Reload UI/AP is a full ModItem replace in items.lua; this file owns helpers + Unit.ReloadAction.
-- Top-up must cap transfer at 1 round: vanilla Firearm:Reload fills MagSize in one call;
-- breaking UnitInventory:ReloadWeapon's stack loop alone does not limit rounds transferred.

local JazzPerRoundStyles = {
	Tube = true,
	Break = true,
	Revolver = true,
}

-- Optional 4th arg max_add: temporarily clamp the source stack so vanilla Reload
-- cannot pull more than that many rounds (used by WEAPONS-004 Top up).
local VanillaFirearmReload = Firearm.Reload
function Firearm:Reload(ammo, suspend_fx, delayed_fx, max_add)
	local reserved = 0
	if max_add and max_add > 0 and ammo and ammo.Amount and ammo.Amount > max_add then
		reserved = ammo.Amount - max_add
		ammo.Amount = max_add
	end
	local prev_ammo, played_fx, change = VanillaFirearmReload(self, ammo, suspend_fx, delayed_fx)
	if reserved > 0 and ammo then
		ammo.Amount = (ammo.Amount or 0) + reserved
	end
	return prev_ammo, played_fx, change
end

local JazzReloadStyleByWeaponId = {
	Auto5 = "Tube",
	Auto5_quest = "Tube",
	DoubleBarrelShotgun = "Break",
	Ithaca = "Tube",
	M1897 = "Tube",
	R870 = "Tube",
	SPAS12 = "Tube",
	Stoeger = "Break",
	Winchester1894 = "Tube",
	Winchester_Quest = "Tube",
	Colt38Special = "Revolver",
	ColtAnaconda = "Revolver",
	ColtM1917 = "Revolver",
	ColtPeacemaker = "Revolver",
	Korth = "Revolver",
	MR73 = "Revolver",
	RSH12 = "Revolver",
	SWModel10 = "Revolver",
	SWModel19 = "Revolver",
	SWModel29 = "Revolver",
	TexRevolver = "Revolver",
	Webley = "Revolver",
}

function OnMsg.ClassesBuilt()
	for weapon_id, reload_style in pairs(JazzReloadStyleByWeaponId) do
		local weapon_class = g_Classes[weapon_id]
		if weapon_class then
			weapon_class.ReloadStyle = reload_style
		end
	end
end

function JazzResolveReloadWeapon(unit, args)
	local weapon
	if args and args.item_id then
		local alternate_slot = unit.current_weapon == "Handheld A" and "Handheld B" or "Handheld A"
		weapon = unit:FindWeaponInSlotById(unit.current_weapon, args.item_id)
			or unit:FindWeaponInSlotById(alternate_slot, args.item_id)
			or unit:FindWeaponInSlotById("Inventory", args.item_id)
	end
	if not weapon then
		if args and args.pos then
			weapon = unit:GetItemAtPackedPos(args.pos)
		else
			weapon = unit:GetWeaponByDefIdOrDefault("Firearm", args and args.weapon, args and args.pos, args and args.item_id)
		end
	end
	return weapon
end

function Firearm:GetReloadUnitAP()
	local magazine_size = Max(1, self.MagazineSize or 1)
	return Max(const.Scale.AP, DivCeil(self.ReloadAP, magazine_size))
end

function Firearm:IsPerRoundReload()
	local bullets = self.ammo and self.ammo.Amount or 0
	return JazzPerRoundStyles[self.ReloadStyle] and bullets > 0 and bullets < self.MagazineSize
end

local VanillaReloadAction = Unit.ReloadAction
function Unit:ReloadAction(action_id, cost_ap, args)
	local weapon = JazzResolveReloadWeapon(self, args)
	if not weapon or not weapon:IsPerRoundReload() then
		return VanillaReloadAction(self, action_id, cost_ap, args)
	end

	local ammo
	if args and args.target then
		ammo = self:GetItem(args.target)
		if not ammo then
			local bag = self.Squad and GetSquadBagInventory(self.Squad)
			ammo = bag and bag:GetItem(args.target)
		end
	end
	self:ReloadWeapon(weapon, ammo, args and args.delayed_fx, nil, "one_round")
end
