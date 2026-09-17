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
g_JAZZ_EndEmplacementInteractionWrapped = rawget(_G, "g_JAZZ_EndEmplacementInteractionWrapped") or false
g_JAZZ_EndEmplacementInteractionBase = rawget(_G, "g_JAZZ_EndEmplacementInteractionBase") or false

-- COMBAT-009 MinRange is 50% BDR so handheld Overwatch can plant close.
-- Vanilla MachineGun had MinRange == MaxRange == WeaponRange, so emplacement
-- Update resetting target_dist to MinRange kept full length. After COMBAT-009
-- that reset (and map sliders saved at the new minimum) left every stationary
-- MG short; MGRotate is hidden on the gun so the cone stuck. Combat cone is
-- always the gun MaxRange / WeaponRange — not the map slider, not sight.
function Jazz_EmplacementConeDist(obj)
	if not obj then
		return nil
	end
	local weapon = obj.weapon
	local slab = const.SlabSizeX or 1
	if not weapon then
		return obj.target_dist
	end
	local max_tiles = weapon.WeaponRange or 0
	if type(weapon.GetOverwatchConeParam) == "function" then
		max_tiles = Max(weapon:GetOverwatchConeParam("MaxRange") or 0, max_tiles)
	end
	if max_tiles < 1 then
		return obj.target_dist
	end
	return max_tiles * slab
end

-- Engine OverwatchAngle unit is minutes of a degree. COMBAT-009 would squeeze
-- a MaxRange emplacement cone to the MG class strip (~2°); owner wants 45°.
function Jazz_EmplacementConeAngle()
	return 45 * 60
end

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
		-- Vanilla recreates the weapon and resets the authored target to MinRange.
		-- Combat cone is gun MaxRange, not the map slider.
		local preserve_dist = not self.updating and not IsEditorActive()
		local prev_dist = self.target_dist
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
		local result = g_JAZZ_EmplacementAmmoUpdateBase(self)
		if preserve_dist then
			self.target_dist = prev_dist
			local dist = Jazz_EmplacementConeDist(self)
			if dist then
				self.target_dist = dist
			end
		end
		return result
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

local function lInstallEndEmplacementInteractionWrap()
	if rawget(_G, "g_JAZZ_EndEmplacementInteractionWrapped") then
		return
	end
	local cls = rawget(_G, "MachineGunEmplacement")
	if type(cls) ~= "table" or type(cls.EndInteraction) ~= "function" then
		return
	end
	rawset(_G, "g_JAZZ_EndEmplacementInteractionBase", cls.EndInteraction)
	rawset(_G, "g_JAZZ_EndEmplacementInteractionWrapped", true)

	function MachineGunEmplacement:EndInteraction(unit)
		if unit and unit.EnterEmplacement then
			unit:EnterEmplacement(self, false)
		end
		if unit and unit.RecalcUIActions then
			unit:RecalcUIActions(true)
		end
		if unit and unit.UpdateOutfit then
			unit:UpdateOutfit()
		end
		local dist = Jazz_EmplacementConeDist(self)
		if not dist then
			return g_JAZZ_EndEmplacementInteractionBase(self, unit)
		end
		local target = RotateRadius(dist, self:GetAngle(), self)
		if unit and unit.QueueCommand then
			unit:QueueCommand("MGTarget", "MGSetup", 0, { target = target })
		end
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
			local dist = Jazz_EmplacementConeDist(obj) or (10 * guim)
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
	lInstallEndEmplacementInteractionWrap()
end

function OnMsg.ClassesBuilt()
	lInstallEmplacementAmmoRemap()
	lInstallEnterEmplacementWrap()
	lInstallEndEmplacementInteractionWrap()
end

function OnMsg.LoadGame()
	lQueueEmplacementReseat("load")
end

function OnMsg.EnterSector()
	lQueueEmplacementReseat("enter-sector")
end

lInstallEmplacementAmmoRemap()
lInstallEnterEmplacementWrap()
lInstallEndEmplacementInteractionWrap()
