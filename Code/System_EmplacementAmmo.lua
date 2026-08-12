-- Remap cut vanilla .50 ammo templates on MachineGunEmplacement to JAZZ calibers.
-- BrowningM2HMG uses JAZZ_Caliber_50BMG; map objects often still set ammo_template="_50BMG_Basic".
-- Vanilla Firearm:Reload does not reject caliber mismatch, but ImpactForce / cut ammo are wrong.
-- HOTFIX-004: reseat ManningEmplacement after load (weapon/visual may not exist in GameInit).

local JAZZ_EMPLACEMENT_AMMO_REMAP = {
	_50BMG_Basic = "JAZZ_AMMO_50BMG_Basic",
	_50BMG_HE = "JAZZ_AMMO_50BMG_API_HEI",
	_50BMG_Incendiary = "JAZZ_AMMO_50BMG_APIT",
	_50BMG_SLAP = "JAZZ_AMMO_50BMG_APIT",
}

g_JAZZ_EmplacementAmmoWrapped = rawget(_G, "g_JAZZ_EmplacementAmmoWrapped") or false
g_JAZZ_EmplacementAmmoUpdateBase = rawget(_G, "g_JAZZ_EmplacementAmmoUpdateBase") or false
g_JAZZ_EnterEmplacementWrapped = rawget(_G, "g_JAZZ_EnterEmplacementWrapped") or false
g_JAZZ_EnterEmplacementBase = rawget(_G, "g_JAZZ_EnterEmplacementBase") or false

local g_JAZZ_EmplacementReseatQueued = false

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

local function lInstallEnterEmplacementWrap()
	if rawget(_G, "g_JAZZ_EnterEmplacementWrapped") then
		return
	end
	local unit_cls = rawget(_G, "Unit")
	if type(unit_cls) ~= "table" or type(unit_cls.EnterEmplacement) ~= "function" then
		return
	end
	rawset(_G, "g_JAZZ_EnterEmplacementBase", unit_cls.EnterEmplacement)
	rawset(_G, "g_JAZZ_EnterEmplacementWrapped", true)

	function Unit:EnterEmplacement(obj, instant)
		if obj and not obj.weapon and type(obj.Update) == "function" then
			obj:Update()
		end
		local fire_pos = obj and obj.GetOperatePos and obj:GetOperatePos()
		if not obj or not obj.weapon or not fire_pos then
			if obj then
				self:AddStatusEffect("ManningEmplacement")
				self:SetEffectValue("hmg_emplacement", obj.handle)
				local sector = rawget(_G, "gv_CurrentSectorId")
				if sector then
					self:SetEffectValue("hmg_sector", sector)
				end
				obj.manned_by = self
				if obj.weapon then
					obj.weapon.owner = self.session_id
				end
			end
			return
		end
		return g_JAZZ_EnterEmplacementBase(self, obj, instant)
	end
end

function Jazz_ReseatMannedEmplacements(reason)
	local units = rawget(_G, "g_Units")
	if type(units) ~= "table" then
		return
	end
	local handle_to_object = rawget(_G, "HandleToObject") or {}
	local overwatch = rawget(_G, "g_Overwatch")
	for _, unit in ipairs(units) do
		if not IsValid(unit) or not unit.HasStatusEffect or not unit:HasStatusEffect("ManningEmplacement") then
			goto continue
		end
		if unit.IsDead and unit:IsDead() then
			goto continue
		end
		local handle = unit.GetEffectValue and unit:GetEffectValue("hmg_emplacement")
		local obj = handle and handle_to_object[handle]
		if not IsKindOf(obj, "MachineGunEmplacement") then
			goto continue
		end
		if not obj.weapon and type(obj.Update) == "function" then
			obj:Update()
		end
		if not obj.weapon then
			goto continue
		end
		unit:EnterEmplacement(obj, true)
		if unit.FlushCombatCache then
			unit:FlushCombatCache()
		end
		if unit.RecalcUIActions then
			unit:RecalcUIActions(true)
		end
		local ow = overwatch and overwatch[unit]
		local cmd = unit.command
		if (not ow or not ow.permanent) and (cmd == "Idle" or not cmd) then
			local dist = obj.target_dist
			local overwatch_ca = CombatActions and CombatActions.Overwatch
			if overwatch_ca and overwatch_ca.GetMaxAimRange then
				local max_range = overwatch_ca:GetMaxAimRange(unit, obj.weapon)
				if max_range then
					dist = Min(dist or (max_range * const.SlabSizeX), max_range * const.SlabSizeX)
				end
			end
			dist = dist or (10 * guim)
			local target = RotateRadius(dist, obj:GetAngle(), obj)
			if unit.QueueCommand then
				unit:QueueCommand("MGTarget", "MGSetup", 0, { target = target })
			end
		end
		::continue::
	end
end

local function lQueueEmplacementReseat(reason)
	if g_JAZZ_EmplacementReseatQueued then
		return
	end
	g_JAZZ_EmplacementReseatQueued = true
	CreateRealTimeThread(function()
		Sleep(50)
		g_JAZZ_EmplacementReseatQueued = false
		local fn = rawget(_G, "Jazz_ReseatMannedEmplacements")
		if type(fn) == "function" then
			fn(reason)
		end
	end)
end

function OnMsg.ModsReloaded()
	lInstallEmplacementAmmoRemap()
	lInstallEnterEmplacementWrap()
end

function OnMsg.ClassesBuilt()
	lInstallEmplacementAmmoRemap()
	lInstallEnterEmplacementWrap()
end

function OnMsg.LoadGame()
	lQueueEmplacementReseat("load")
end

function OnMsg.EnterSector()
	lQueueEmplacementReseat("enter-sector")
end

lInstallEmplacementAmmoRemap()
lInstallEnterEmplacementWrap()
