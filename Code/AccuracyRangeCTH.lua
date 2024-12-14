function GetRangeAccuracy(weapon, distance, unit, action)
	local effective_range_acc = 100
	local point_blank_acc = 100
	
	local weapon_range
    local effective_range
	if unit and action then
		weapon_range = action:GetMaxAimRange(unit, weapon)
	end
	
	if not weapon_range then
		weapon_range = weapon.WeaponRange or weapon:GetProperty("WeaponRange")
        effective_range = weapon.BulletDropRange or weapon:GetProperty("BulletDropRange")
	end
	
	if IsKindOf(unit, "UnitBase") then
		weapon_range = unit:CallReactions_Modify("OnUnitGetWeaponRange", weapon_range, weapon, action)
	end

	--print(effective_range)

    if not effective_range then effective_range = weapon_range / 2 end

	local y0 = point_blank_acc
	local xm, ym = effective_range, effective_range_acc
	local xr = weapon_range
	local a, b, c = 0, 0, 0

	if distance / const.SlabSizeX <= xr then
		if distance / const.SlabSizeX <= xm then
			return effective_range_acc
		else
			-- second parabola
			a = MulDivRound(-ym, const.SlabSizeX, (xm-xr)*(xm-xr))
			b = MulDivRound(-2 * a, xm, const.SlabSizeX)
			c = MulDivRound(-a, xr*xr, const.SlabSizeX) - b*xr
		end
	else
		-- second parabola
			a = MulDivRound(-ym, const.SlabSizeX, (xm-xr)*(xm-xr))*1
			b = MulDivRound(-2 * a, xm, const.SlabSizeX)
			c = MulDivRound(-a, xr*xr, const.SlabSizeX) - b*xr
	end
	
	local part = MulDivRound(MulDivRound(a, distance, const.SlabSizeX), distance, const.SlabSizeX*const.SlabSizeX)
  --  print ("Distance "..distance / const.SlabSizeX)
  --  print ("EffectiveCTH"..part + MulDivRound(b, distance, const.SlabSizeX) + c)
	return part + MulDivRound(b, distance, const.SlabSizeX) + c
end

