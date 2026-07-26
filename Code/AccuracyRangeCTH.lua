function GetRangeAccuracy(weapon, distance, unit, action)
	local weapon_range

	if unit and action then
		weapon_range = action:GetMaxAimRange(unit, weapon)
	end

	weapon_range = weapon_range or weapon.WeaponRange or weapon:GetProperty("WeaponRange")

	if not weapon_range or weapon_range <= 1 then
		return 100
	end

	local effective_range = weapon.BulletDropRange or weapon:GetProperty("BulletDropRange") or weapon_range / 2

	if IsKindOf(unit, "UnitBase") then
		weapon_range = unit:CallReactions_Modify("OnUnitGetWeaponRange", weapon_range, weapon, action)
	end

	if not weapon_range or weapon_range <= 1 then
		return 100
	end

	effective_range = Max(1, Min(effective_range, weapon_range - 1))

	local tiles = distance * 1.0 / const.SlabSizeX

	local grouping = FirearmGetGrouping(weapon) or 88
	local min_acc = 0
	local curve_mult = 1.8

	local bulletdrop_acc = Max(min_acc + 1, Min(99, grouping))

	local drop_t = effective_range * 1.0 / weapon_range
	drop_t = Max(0.01, Min(0.99, drop_t))

	local log_num = (100 - bulletdrop_acc) * 1.0 / (100 - min_acc)
	log_num = Max(0.01, Min(0.99, log_num))

	local power = math.log(log_num) / math.log(drop_t)
	power = power * curve_mult

	local t = tiles * 1.0 / weapon_range
	t = Max(0, t)

	local acc = 100 - (100 - min_acc) * (t ^ power)
	acc = floatfloor(acc,0)
	if acc ~= acc then
		print("GetRangeAccuracy NAN", weapon.class, weapon_range, effective_range, grouping, bulletdrop_acc, drop_t, log_num, power, t)
		return 0
	end

	--print(weapon.class, weapon_range, effective_range, grouping, bulletdrop_acc, drop_t, log_num, power, t, acc)

	return Max(0, Min(100, acc))
end

function GetRangeDamageReduction(weapon, distance, unit, action)
	local weapon_range

	if unit and action then
		weapon_range = action:GetMaxAimRange(unit, weapon)
	end

	weapon_range = weapon_range or weapon.WeaponRange or weapon:GetProperty("WeaponRange")

	if not weapon_range or weapon_range <= 1 then
		return 100
	end

	local effective_range = weapon.BulletDropRange or weapon:GetProperty("BulletDropRange") or weapon_range / 2

	if IsKindOf(unit, "UnitBase") then
		weapon_range = unit:CallReactions_Modify("OnUnitGetWeaponRange", weapon_range, weapon, action)
	end

	if not weapon_range or weapon_range <= 1 then
		return 100
	end

	effective_range = Max(1, Min(effective_range, weapon_range - 1))

	local tiles = distance * 1.0 / const.SlabSizeX

	local grouping = 88
	local min_acc = 1
	local curve_mult = 1.8

	local bulletdrop_acc = Max(min_acc + 1, Min(99, grouping))

	local drop_t = effective_range * 1.0 / weapon_range
	drop_t = Max(0.01, Min(0.99, drop_t))

	local log_num = (100 - bulletdrop_acc) * 1.0 / (100 - min_acc)
	log_num = Max(0.01, Min(0.99, log_num))

	local power = math.log(log_num) / math.log(drop_t)
	power = power * curve_mult

	local t = tiles * 1.0 / weapon_range
	t = Max(0, t)

	local acc = 100 - (100 - min_acc) * (t ^ power)
	acc = floatfloor(acc,0)
	if acc ~= acc then
		print("GetRangeAccuracy NAN", weapon.class, weapon_range, effective_range, grouping, bulletdrop_acc, drop_t, log_num, power, t)
		return 0
	end

	--print(weapon.class, weapon_range, effective_range, grouping, bulletdrop_acc, drop_t, log_num, power, t, acc)

	return Max(0, Min(100, acc))
end

function oldGetRangeAccuracy(weapon, distance, unit, action)
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

	weapon_range = weapon_range or weapon.WeaponRange or weapon:GetProperty("WeaponRange")
	effective_range = weapon.BulletDropRange or weapon:GetProperty("BulletDropRange") or weapon_range / 2


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