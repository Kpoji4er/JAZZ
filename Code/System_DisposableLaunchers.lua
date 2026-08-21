-- JAZZ-WEAPONS-005: launcher plus embedded ordnance is one consumable item.

local VanillaIsWeaponAvailableForReload = IsWeaponAvailableForReload
function IsWeaponAvailableForReload(weapon, ammoForWeapon)
	if weapon and weapon.DisposableLauncher then
		return false, AttackDisableReasons.NoAmmo
	end
	if ammoForWeapon then
		local live = {}
		for _, ammo in ipairs(ammoForWeapon) do
			if ammo and (ammo.Amount or 0) > 0 then
				live[#live + 1] = ammo
			end
		end
		ammoForWeapon = live
	end
	return VanillaIsWeaponAvailableForReload(weapon, ammoForWeapon)
end

local VanillaReloadWeapon = UnitInventory.ReloadWeapon
function UnitInventory:ReloadWeapon(weapon, ...)
	if weapon and weapon.DisposableLauncher then
		return false
	end
	return VanillaReloadWeapon(self, weapon, ...)
end

function RocketLauncher:Reload(ammo, suspend_fx, delayed_fx, max_add)
	if self.DisposableLauncher then
		return false, false, false
	end
	local prev, played_fx, change = Firearm.Reload(self, ammo, suspend_fx, delayed_fx, max_add)
	self:UpdateRocket()
	return prev, played_fx, change
end

local function LoadEmbeddedOrdnance(launcher)
	if not launcher.DisposableLauncher or launcher.ammo or not launcher.EmbeddedOrdnance then
		return
	end
	local ordnance = PlaceInventoryItem(launcher.EmbeddedOrdnance)
	if not ordnance then
		return
	end
	ordnance.Amount = 1
	launcher.ammo = ordnance
	ObjModified(launcher)
end

function OnMsg.ItemAdded(owner, item)
	if IsKindOf(item, "RocketLauncher") then
		LoadEmbeddedOrdnance(item)
	end
end

local function SpawnSpentTube(attacker, launcher)
	local debris = PlaceObject("WeaponVisual")
	debris:ChangeEntity(launcher.Entity)
	debris.fx_actor_class = launcher:GetFxClass()

	local pos = attacker:GetPos()
	if not pos:IsValidZ() then
		pos = pos:SetTerrainZ()
	end
	local offset = Rotate(point(-30 * guic, 0, 0), attacker:GetAngle())
	debris:SetPos((pos + offset):SetTerrainZ())
	debris:SetAngle(attacker:GetAngle())
	return debris
end

function OnMsg.OnAttack(attacker, action, target, results, attack_args)
	local launcher = attack_args and attack_args.weapon
	if not launcher or not launcher.DisposableLauncher or not results or not results.fired then
		return
	end
	if not launcher.ammo or launcher.ammo.Amount > 0 then
		return
	end

	local slot_name = attacker:GetItemSlot(launcher)
	if not slot_name or not attacker:RemoveItem(slot_name, launcher) then
		return
	end

	SpawnSpentTube(attacker, launcher)
	if launcher.ammo then
		DoneObject(launcher.ammo)
		launcher.ammo = false
	end
	attacker:UpdateOutfit()
	DoneObject(launcher)
	Msg("InventoryChange", attacker)
end
