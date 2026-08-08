-- JAZZ-UNITS-006 Batch5 HARD/satellite: Rothman/Ira/Miguel/Biff/Livewire/Barry/Thor
-- + cheap §C leftovers. Install from System_NamedPerks_006.lua (do not overwrite OnMsg here).

g_JAZZ_NamedPerks006Batch5Wrapped = rawget(_G, "g_JAZZ_NamedPerks006Batch5Wrapped") or false
g_JAZZ_BarryCraftBase_ItemsCalc = rawget(_G, "g_JAZZ_BarryCraftBase_ItemsCalc") or false
g_JAZZ_CordOpsBase_Time = rawget(_G, "g_JAZZ_CordOpsBase_Time") or false
g_JAZZ_ConradOpsBase_Time = rawget(_G, "g_JAZZ_ConradOpsBase_Time") or false
g_JAZZ_RothmanMineBase = rawget(_G, "g_JAZZ_RothmanMineBase") or false
g_JAZZ_CarlosRemoveHiddenBase = rawget(_G, "g_JAZZ_CarlosRemoveHiddenBase") or false
g_JAZZ_MeatSuppressionBase = rawget(_G, "g_JAZZ_MeatSuppressionBase") or false

local PRIMARY_STATS = {
	"Health",
	"Agility",
	"Dexterity",
	"Strength",
	"Wisdom",
	"Leadership",
	"Marksmanship",
	"Mechanical",
	"Explosives",
	"Medical",
}

local function lIsPlayerSide(side)
	return side == "player1" or side == "player2"
end

function Jazz_SectorHasRothman(sector_id)
	if not sector_id or not gv_Squads then
		return false
	end
	for _, squad in pairs(gv_Squads) do
		if squad and lIsPlayerSide(squad.Side) and squad.CurrentSector == sector_id then
			for _, uid in ipairs(squad.units or empty_table) do
				local u = gv_UnitData and gv_UnitData[uid]
				if not u and g_Units then
					u = g_Units[uid]
				end
				if u and HasPerk(u, "Jazz_Perk_Rothman") and not (u.IsDead and u:IsDead()) then
					return true
				end
			end
		end
	end
	return false
end

-- Loyalty-scaled mine income boost while Rothman garrisons the mine sector.
-- Bonus% = 10 + MulDivRound(Max(0, 100 - loyalty), 30, 100)  → ~10% @100 loyalty, ~40% @0.
function Jazz_RothmanMineBonusPercent(sector_id)
	if not Jazz_SectorHasRothman(sector_id) then
		return 0
	end
	local sector = gv_Sectors and gv_Sectors[sector_id]
	if not sector or not sector.Mine then
		return 0
	end
	local loyalty = GetCityLoyalty and (GetCityLoyalty(sector.City) or 50) or 50
	return 10 + MulDivRound(Max(0, 100 - loyalty), 30, 100)
end

function Jazz_IraApplyMilitiaTrainBonus(unit)
	if not unit or not HasPerk then
		return false
	end
	-- Caller must verify Ira trained this militia; applies +20 to a random primary.
	local stat = PRIMARY_STATS[1 + InteractionRand(#PRIMARY_STATS, "Jazz_Perk_Ira")]
	local cur = unit[stat] or 0
	if type(cur) ~= "number" then
		return false
	end
	unit[stat] = Clamp(cur + 20, 0, 100)
	return true, stat
end

function Jazz_FindMiguel()
	for _, u in ipairs(g_Units or empty_table) do
		if IsValid(u) and HasPerk(u, "Jazz_Perk_Miguel") then
			return u
		end
	end
	return false
end

local function lMiguelIsDowned(u)
	if not u or u:IsDead() then
		return true
	end
	if u.IsDowned and u:IsDowned() then
		return true
	end
	if u.HasStatusEffect and (u:HasStatusEffect("Unconscious") or u:HasStatusEffect("KnockDown")) then
		return true
	end
	return false
end

function Jazz_MiguelRefreshAura()
	local miguel = Jazz_FindMiguel()
	if not miguel then
		return
	end
	local up = not lMiguelIsDowned(miguel)
	local buff = up and "Jazz_MiguelAuraUp" or "Jazz_MiguelAuraDown"
	local other = up and "Jazz_MiguelAuraDown" or "Jazz_MiguelAuraUp"
	local slab = const.SlabSizeX
	for _, u in ipairs(g_Units or empty_table) do
		if IsValid(u) and u ~= miguel and not u:IsDead() and miguel.team and u.team == miguel.team then
			if DivRound(miguel:GetDist(u), slab) <= 30 then
				if u:HasStatusEffect(other) then
					u:RemoveStatusEffect(other)
				end
				if not u:HasStatusEffect(buff) then
					u:AddStatusEffect(buff)
				end
			else
				u:RemoveStatusEffect("Jazz_MiguelAuraUp")
				u:RemoveStatusEffect("Jazz_MiguelAuraDown")
			end
		end
	end
end

function Jazz_BarryCraftDiscountPercent(unit)
	if unit and HasPerk(unit, "DesignerExplosives") then
		return 30
	end
	return 0
end

function Jazz_CordInBarCity(merc)
	if not merc then
		return false
	end
	if not HasPerk(merc, "Jazz_Perk_Cord") then
		return false
	end
	local squad_id = merc.Squad
	local squad = squad_id and gv_Squads and gv_Squads[squad_id]
	local sector_id = squad and squad.CurrentSector
	local sector = sector_id and gv_Sectors and gv_Sectors[sector_id]
	if not sector then
		return false
	end
	-- Soft: any city sector (bar POI gate deferred).
	return sector.City and sector.City ~= "none"
end

function Jazz_ConradEffectiveLeadership(merc)
	local ldr = (merc and merc.Leadership) or 0
	if merc and HasPerk(merc, "Jazz_Perk_Conrad") then
		return Max(ldr, 90)
	end
	return ldr
end

local TRAIN_OPS = {
	TrainMilitia = true,
	MilitiaTraining = true,
	TrainMercs = true,
	TrainStats = true,
	Teacher = true,
}

local REPAIR_OPS = {
	RepairItems = true,
	Repair = true,
}

function Jazz_InstallNamedPerks006Batch5()
	-- Ira hook may need SectorOperations after first wrap attempt.
	if rawget(_G, "g_JAZZ_NamedPerks006Batch5Wrapped") then
		Jazz_InstallIraMilitiaTrainHook()
		return
	end

	-- Rothman: loyalty-scaled mine income while garrisoned.
	local mine = rawget(_G, "_GetMineIncome")
	if type(mine) == "function" and not rawget(_G, "g_JAZZ_RothmanMineBase") then
		rawset(_G, "g_JAZZ_RothmanMineBase", mine)
		rawset(_G, "_GetMineIncome", function(sector_id, showEvenIfUnowned)
			local income = g_JAZZ_RothmanMineBase(sector_id, showEvenIfUnowned)
			if type(income) ~= "number" or income <= 0 then
				return income
			end
			local bonus = Jazz_RothmanMineBonusPercent(sector_id)
			if bonus > 0 then
				income = MulDivRound(income, 100 + bonus, 100)
			end
			return income
		end)
	end

	-- Barry: CraftAmmo / CraftExplosives Parts −30%.
	local calc = rawget(_G, "SectorOperation_ItemsCalcRes")
	if type(calc) == "function" and not rawget(_G, "g_JAZZ_BarryCraftBase_ItemsCalc") then
		rawset(_G, "g_JAZZ_BarryCraftBase_ItemsCalc", calc)
		rawset(_G, "SectorOperation_ItemsCalcRes", function(sector_id, operation_id)
			local parts = g_JAZZ_BarryCraftBase_ItemsCalc(sector_id, operation_id)
			if type(parts) ~= "number" or parts <= 0 then
				return parts
			end
			local mercs = GetOperationProfessionals and GetOperationProfessionals(sector_id, operation_id) or empty_table
			if operation_id == "CraftAmmo" or operation_id == "CraftExplosives" then
				local best = 0
				for _, merc in ipairs(mercs) do
					best = Max(best, Jazz_BarryCraftDiscountPercent(merc))
				end
				if best > 0 then
					parts = Max(0, MulDivRound(parts, 100 - best, 100))
				end
			elseif REPAIR_OPS[operation_id] then
				for _, merc in ipairs(mercs) do
					if Jazz_CordInBarCity(merc) then
						parts = Max(0, MulDivRound(parts, 90, 100))
						break
					end
				end
			end
			return parts
		end)
	end

	-- Cord / Conrad: satellite op time.
	local base_ops = rawget(_G, "GetOperationTimeLeft")
	if type(base_ops) == "function" and not rawget(_G, "g_JAZZ_CordOpsBase_Time") then
		rawset(_G, "g_JAZZ_CordOpsBase_Time", base_ops)
		rawset(_G, "GetOperationTimeLeft", function(merc, operation_id, ...)
			local t = g_JAZZ_CordOpsBase_Time(merc, operation_id, ...)
			if type(t) ~= "number" then
				return t
			end
			if Jazz_CordInBarCity(merc) and REPAIR_OPS[operation_id] then
				t = MulDivRound(t, 85, 100)
			end
			if merc and HasPerk(merc, "Jazz_Perk_Conrad") and TRAIN_OPS[operation_id] then
				local ldr = merc.Leadership or 0
				if ldr < 90 and ldr > 0 then
					-- Treat Leadership as floor 90 for training pace.
					t = MulDivRound(t, ldr, 90)
				end
			end
			return t
		end)
	end

	-- Meat: Will-point damage → Grit; skip suppression application.
	if type(QueueSuppressionApplication) == "function" and not rawget(_G, "g_JAZZ_MeatSuppressionBase") then
		rawset(_G, "g_JAZZ_MeatSuppressionBase", QueueSuppressionApplication)
		rawset(_G, "QueueSuppressionApplication", function(unit, wp_dmg, effect)
			if IsValid(unit) and HasPerk(unit, "Jazz_Perk_Meat") then
				local dmg = tonumber(wp_dmg) or 0
				if dmg > 0 and unit.ApplyTempHitPoints then
					unit:ApplyTempHitPoints(dmg)
				end
				-- Unsuppressible: drop status_effect from queue path.
				return
			end
			return g_JAZZ_MeatSuppressionBase(unit, wp_dmg, effect)
		end)
	end

	-- Carlos: failed stealth kill may keep Hidden (50%).
	if Unit and type(Unit.RemoveStatusEffect) == "function" and not rawget(_G, "g_JAZZ_CarlosRemoveHiddenBase") then
		rawset(_G, "g_JAZZ_CarlosRemoveHiddenBase", Unit.RemoveStatusEffect)
		function Unit:RemoveStatusEffect(id, ...)
			if id == "Hidden" and HasPerk(self, "Jazz_Perk_Carlos") then
				if self.GetEffectValue and self:GetEffectValue("Jazz_CarlosKeepHidden") then
					self:SetEffectValue("Jazz_CarlosKeepHidden", nil)
					if InteractionRand(100, "Jazz_Perk_Carlos") < 50 then
						return
					end
				end
			end
			return g_JAZZ_CarlosRemoveHiddenBase(self, id, ...)
		end
	end

	if Unit and type(Unit.OnAttack) == "function" and not rawget(Unit, "JazzUnits006CarlosWrapped") then
		local base = Unit.OnAttack
		function Unit:OnAttack(action, target, results, attack_args, ...)
			local ret = base(self, action, target, results, attack_args, ...)
			if HasPerk(self, "Jazz_Perk_Carlos") and results and attack_args then
				local chance = attack_args.stealth_kill_chance or 0
				if chance > 0 and not results.stealth_kill then
					self:SetEffectValue("Jazz_CarlosKeepHidden", true)
				end
			end
			if type(Jazz_DangerCloseOnAttack) == "function" then
				Jazz_DangerCloseOnAttack(self, action, target, results, attack_args)
			end
			if type(Jazz_SimonOnKillCharge) == "function" then
				Jazz_SimonOnKillCharge(self, results, target)
			end
			return ret
		end
		rawset(Unit, "JazzUnits006CarlosWrapped", true)
	end

	-- Ira: militia she trains gains +20 random primary on op Complete.
	Jazz_InstallIraMilitiaTrainHook()

	rawset(_G, "g_JAZZ_NamedPerks006Batch5Wrapped", true)
end

function Jazz_SectorHasIraTrainer(sector)
	local sector_id = type(sector) == "table" and (sector.Id or sector.id) or sector
	if not sector_id then
		return false
	end
	local mercs = GetOperationProfessionals and GetOperationProfessionals(sector_id, "MilitiaTraining") or empty_table
	if not next(mercs) then
		mercs = GetOperationProfessionals and GetOperationProfessionals(sector_id, "TrainMilitia") or empty_table
	end
	for _, merc in ipairs(mercs) do
		if merc and HasPerk(merc, "Jazz_Perk_Ira") and not (merc.IsDead and merc:IsDead()) then
			return true
		end
	end
	-- Garrison fallback: Ira present in sector squads.
	for _, squad in pairs(gv_Squads or empty_table) do
		if squad and lIsPlayerSide(squad.Side) and squad.CurrentSector == sector_id then
			for _, uid in ipairs(squad.units or empty_table) do
				local u = gv_UnitData and gv_UnitData[uid]
				if u and HasPerk(u, "Jazz_Perk_Ira") and not (u.IsDead and u:IsDead()) then
					return true
				end
			end
		end
	end
	return false
end

function Jazz_IraBoostMilitiaInSector(sector)
	if not Jazz_SectorHasIraTrainer(sector) then
		return
	end
	local sector_id = type(sector) == "table" and (sector.Id or sector.id) or sector
	local sector_obj = (type(sector) == "table" and sector) or (gv_Sectors and gv_Sectors[sector_id])
	local squad_id = sector_obj and sector_obj.militia_squad_id
	local squad = squad_id and gv_Squads and gv_Squads[squad_id]
	if not squad then
		return
	end
	for _, uid in ipairs(squad.units or empty_table) do
		local u = gv_UnitData and gv_UnitData[uid]
		if u and not u.Jazz_IraTrainedBonus then
			local ok = Jazz_IraApplyMilitiaTrainBonus(u)
			if ok then
				u.Jazz_IraTrainedBonus = true
			end
		end
	end
end

function Jazz_InstallIraMilitiaTrainHook()
	if rawget(_G, "g_JAZZ_IraMilitiaHook") or not SectorOperations then
		return
	end
	local op = SectorOperations.MilitiaTraining or SectorOperations.TrainMilitia
	if not op then
		return
	end
	rawset(_G, "g_JAZZ_IraMilitiaHook", true)
	local base_complete = op.Complete or op.OnComplete
	if type(base_complete) ~= "function" then
		return
	end
	local key = op.Complete and "Complete" or "OnComplete"
	local prev = op[key]
	op[key] = function(self, sector, ...)
		local ret = prev(self, sector, ...)
		if type(Jazz_IraBoostMilitiaInSector) == "function" then
			Jazz_IraBoostMilitiaInSector(sector)
		end
		return ret
	end
end

function Jazz_DangerCloseOnAttack(attacker, action, target, results, attack_args)
	if not attacker or not HasPerk(attacker, "DangerClose") or not results or results.miss then
		return
	end
	if not IsKindOf(target, "Unit") then
		return
	end
	local dist = DivRound(attacker:GetDist(target), const.SlabSizeX)
	if dist < 8 then
		return
	end
	-- Soft partial: mark bleed stacks if status exists; damage bonus is via CE reaction when present.
	if CharacterEffectDefs and CharacterEffectDefs.Bleeding and target.AddStatusEffect then
		target:AddStatusEffect("Bleeding")
		target:AddStatusEffect("Bleeding")
	end
end

function Jazz_NamedPerks006Batch5OnCombatStart()
	Jazz_MiguelRefreshAura()
end

function Jazz_NamedPerks006Batch5OnTurnStart()
	Jazz_MiguelRefreshAura()
end
