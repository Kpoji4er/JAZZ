function Unit:UpdateGasMaskVisibility()
	if self:GetItemInSlot("Head", "GasMaskBase") or self:GetItemInSlot("HeadGear", "GasMaskBase")  then
		AppearanceObject.EquipGasMask(self)
	else
		AppearanceObject.UnequipGasMask(self)
	end
end

local WeaponAttachSpots = {
	Hand = { "Weaponr", "Weaponl" },
	Shoulder = { "Weaponrb", "Weaponlb" },
	Leg = { "Weaponrs", "Weaponls" },
	Mortar = { "Mortar", "Mortar" },
	LegKnife = { "Weaponrknife", "Weaponlknife" },
	ShoulderKnife = { "Weaponrbknife", "Weaponlbknife" },
}

BlockedSpotsVariants = {
	["Weaponrknife"] = "Weaponrs",
	["Weaponlknife"] = "Weaponls",
}

local HolsterAttachSpots = {
	Weaponrb = true,
	Weaponlb = true,
	Weaponrs = true,
	Weaponls = true,
	Weaponrknife = true,
	Weaponlknife = true,
	Weaponrbknife = true,
	Weaponlbknife = true,
}

local mkoffset = point(0,0,30*guic)
local WeaponAttachOffset =
{	-- spot - animation - offset
	Weaponr = {
		["mk_Standing_Aim_Forward"] = mkoffset,
		["mk_Standing_Aim_Down"] = mkoffset,
		["mk_Left_Aim_Start"] = mkoffset,
		["mk_Right_Aim_Start"] = mkoffset,
		["mk_Standing_Fire"] = mkoffset,
	},
}

local MortarDrawnAnims = {
	nw_Standing_MortarIdle = true,
	nw_Standing_MortarEnd = true,
	nw_Standing_MortarLoad = true,
	nw_Standing_MortarFire = true,
}

local function GetItemAttachSpot(unit, item, equip_index, holster, avatar)
	local slot
	if holster == nil then
		if equip_index ~= 1 and equip_index ~= 2 then
			holster = true
		else
			local anim = unit:GetStateText()
			if item.WeaponType == "Mortar" then
				if MortarDrawnAnims[anim] then
					return -- the mortar command will handle it
				end
				holster = true
			elseif (avatar or unit):HasStatusEffect("ManningEmplacement") then
				holster = true
			else
				local starts_with = string.starts_with
				if starts_with(anim, "nw_") then
					holster = true
				elseif starts_with(anim, "gr_") then
					holster = true
				elseif starts_with(anim, "civ_") then
					holster = true
				elseif starts_with(anim, "mk_") then
					if item.WeaponType ~= "MeleeWeapon" then
						holster = true
					end
				end
			end
		end
	end
	if holster then
		slot = item.HolsterSlot
		if not WeaponAttachSpots[slot] then
			slot = item.HandSlot == "OneHanded" and "Leg" or "Shoulder"
		end
		for i, component in pairs(item.components) do
			local visuals = (WeaponComponents[component] or empty_table).Visuals or empty_table
			local idx = table.find(visuals, "ApplyTo", item.class)
			if idx then
				local component_data = visuals[idx]
				local override_holster_slot = component_data.OverrideHolsterSlot
				if override_holster_slot == "Sholder" then
					slot = "Shoulder"
					break
				elseif override_holster_slot == "Leg" then
					slot = "Leg"
				end
			end
		end
	else
		slot = "Hand"
	end
	if slot == "Leg" then
		if IsKindOf(item, "MeleeWeapon") then
			slot = "LegKnife"
		end
	elseif slot == "Shoulder" then
		if IsKindOf(item, "MeleeWeapon") then
			slot = "ShoulderKnife"
		end
	end
	local spot = WeaponAttachSpots[slot][(equip_index == 2 or equip_index == 4) and 2 or 1]
	return spot
end

local function GetItemSpotAttachment(unit, spot, attach)
	local item = attach.weapon
	local attach_axis, attach_angle, attach_offset, attach_state
	if HolsterAttachSpots[spot] then
		if attach:HasSpot("Holster") then
			local offset = GetWeaponRelativeSpotPos(attach, "Holster")
			if offset then
				attach_offset = -offset
			end
			if IsKindOf(item, "RPG7") then
				attach_axis = axis_z
				attach_angle = 180*60
				attach_offset = RotateAxis(attach_offset, attach_axis, attach_angle)
			end
		end
	else
		local spot_offset_by_anim = WeaponAttachOffset[spot]
		local anim = unit:GetStateText()
		if spot_offset_by_anim then
			attach_offset = spot_offset_by_anim[anim]
		end
		if spot == "Weaponr" and IsKindOf(item, "MeleeWeapon") then
			if unit.gender == "Female" then
				if IsKindOf(item, "MacheteWeapon") then
					attach_axis = axis_x
					attach_angle = 180*60
				elseif anim == "mk_Standing_Aim_Forward"  then
					attach_axis = axis_x
					attach_angle = 90*60
					attach_offset = point(0*guic,-30*guic,0*guic)
				end
			elseif	 IsKindOf(item, "MacheteWeapon") then
				attach_offset = false
			end
		end
	end
	if attach_offset then
		attach_offset = MulDivRound(attach_offset, attach:GetScale(), 100)
	end
	if item and item.WeaponType == "Mortar" then
		attach_state = "packed"
	end
	return attach_axis or axis_x, attach_angle or 0, attach_offset, attach_state
end

local function AttachVisualItem(unit, spot, attach)
	local attach_axis, attach_angle, attach_offset, attach_state = GetItemSpotAttachment(unit, spot, attach)
	unit:Attach(attach, unit:GetSpotBeginIndex(spot))
	attach:SetAttachAxis(attach_axis or axis_x)
	attach:SetAttachAngle(attach_angle or 0)
	attach:SetAttachOffset(attach_offset or point30)
	if attach_state and attach:GetStateText() ~= attach_state then
		attach:SetState(attach_state)
	end
end

function AttachVisualItems(obj, attaches, crossfading, holster, avatar)
	if not attaches or #attaches == 0 then
		return
	end
	local hidden
	if IsKindOf(obj, "Unit") then
		local part_in_combat = g_Combat and obj.team and obj.team.side ~= "neutral"
		if not part_in_combat then
			if obj:GetCommandParam("weapon_anim_prefix") == "civ_" or obj:GetCommandParam("weapon_anim_prefix", "Idle") == "civ_" then
				hidden = true
			end
		end
		if obj.carry_flare then
			hidden = not obj.visible
		end
		-- make sure we're not hiding weapons setup by a setpiece
		for _, attach in ipairs(attaches) do
			if IsKindOfClasses(attach, WeaponVisualClasses) and attach.weapon and obj:GetItemSlot(attach.weapon) == "SetpieceWeapon" then
				hidden = false
				break
			end
		end
	end
	if hidden then
		for _, attach in ipairs(attaches) do
			attach:ClearHierarchyEnumFlags(const.efVisible)
		end
		return
	end
	local custom_equip = obj.action_visual_weapon
	if custom_equip or (IsKindOf(obj, "Unit") and obj.carry_flare) then
		holster = true
	end
	for i = #attaches, 1, -1 do
		local attach = attaches[i]
		if IsKindOfClasses(attach, WeaponVisualClasses) and attach.custom_equip and attach ~= custom_equip and (attach.equip_index or 5) > 4 then
			DoneObject(attach)
			table.remove(attaches, i)
		end
	end
	local wait_crossfade, grip_modify
	local spot_attach = {}
	table.sort(attaches, function(o1, o2) return o1.equip_index < o2.equip_index end)
	for _, attach in ipairs(attaches) do
		local item = attach.weapon
		local spot
		local cur_spot = attach:GetAttachSpotName()
		if attach == custom_equip then
			spot = WeaponAttachSpots["Hand"][1] or cur_spot
		elseif item then
			spot = GetItemAttachSpot(obj, item, attach.equip_index, holster, avatar) or cur_spot
		end
		if spot then
			if spot ~= cur_spot and crossfading and not HolsterAttachSpots[spot] then
				wait_crossfade = true
			else
				AttachVisualItem(obj, spot, attach)
			end
			spot_attach[spot] = attach -- prefer displaying the other set weapon attaches
			if item and item.class == "Gewehr98" and spot == "Weaponr" then
			--	grip_modify = true
			end
		end
	end
	local channel = const.AnimChannel_RightHandGrip
	if grip_modify then
		if GetStateName(obj:GetAnim(channel)) ~= "ar_RHand_AltGrip_Rifles" then
			obj:SetAnimMask(channel, "RightHand")
			obj:SetAnim(channel, "ar_RHand_AltGrip_Rifles")
			obj:SetAnimWeight(channel, 1000)
		end
	else
		obj:ClearAnim(channel)
	end

	-- update visibility
	local blocked_spots = (avatar or obj).blocked_spots
	local flare = IsKindOf(obj, "Unit") and obj.carry_flare and obj.visible
	for _, attach in ipairs(attaches) do
		local spot = attach:GetAttachSpotName()
		local is_blocked = blocked_spots and (blocked_spots[spot] or blocked_spots[BlockedSpotsVariants[spot]])
		if is_blocked or spot_attach[spot] ~= attach then
			if flare and IsKindOf(attach, "GrenadeVisual") and attach.fx_actor_class == "FlareStick" then
				attach:SetHierarchyEnumFlags(const.efVisible)
			else
				attach:ClearHierarchyEnumFlags(const.efVisible)
			end
		else
			attach:SetHierarchyEnumFlags(const.efVisible)
			attach:SetContourOuterOccludeRecursive(true)
		end
		local parts = attach.parts
		if parts then
			local is_holstered = attach.equip_index ~= 1 and attach.equip_index ~= 2
			if parts.Bipod and parts.Bipod:HasState("folded") then
				local bipod_state = not is_holstered and IsKindOf(obj, "Unit") and (obj.stance == "Prone" or obj:HasStatusEffect("BipodUnfolded")) and "idle" or "folded"
				if parts.Bipod:GetStateText() ~= bipod_state then
					parts.Bipod:SetState(bipod_state)
				end
			end
			if parts.Under and parts.Under:HasState("folded") then
				local bipod_state = not is_holstered and IsKindOf(obj, "Unit") and (obj.stance == "Prone" or obj:HasStatusEffect("BipodUnfolded")) and "idle" or "folded"
				if parts.Under:GetStateText() ~= bipod_state then
					parts.Under:SetState(bipod_state)
				end
			end
			if parts.Barrel and parts.Barrel:HasState("folded") then
				local bipod_state = not is_holstered and IsKindOf(obj, "Unit") and (obj.stance == "Prone" or obj:HasStatusEffect("BipodUnfolded")) and "idle" or "folded"
				if parts.Barrel:GetStateText() ~= bipod_state then
					parts.Barrel:SetState(bipod_state)
				end
			end
		end
	end
	return wait_crossfade
end