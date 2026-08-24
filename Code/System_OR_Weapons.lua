-- some slots attach to the visual objects of other slots
SlotDependencies = {
	["Muzzle"] = "Barrel",
	["Bipod"] = "Barrel",
	["Side"] = "Barrel",
	["Sightsf"] = "Barrel",
}

if FirstLoad then

	MapVar("g_SuppressionApplyThread", {})

    g_SuppressionApplyQueue = false
end

function QueueSuppressionApplication(unit, wp_dmg, effect)
    if not g_SuppressionApplyQueue then
        g_SuppressionApplyQueue = { head = 1 }
    end
    if not g_SuppressionApplyThread or not IsValidThread(g_SuppressionApplyThread) then
        g_SuppressionApplyThread = CreateGameTimeThread(function()
            while true do
                local queue = g_SuppressionApplyQueue
                local head = queue and (queue.head or 1) or 1
                local entry = queue and queue[head]
                if entry then
                    queue[head] = nil
                    queue.head = head + 1
                    if queue.head > 32 and queue.head * 2 > #queue then
                        local compact, n = { head = 1 }, 0
                        for i = queue.head, #queue do
                            n = n + 1
                            compact[n] = queue[i]
                        end
                        g_SuppressionApplyQueue = compact
                    end
                    local u, dmg, status_effect = entry.unit, entry.damage or 0, entry.effect
                    if IsValid(u) then
						Sleep(10)
                        if dmg > 0 then
                            local old_wp = u.WillPoints
                            u.WillPoints = Max(0, old_wp - dmg)
                            if u.WillPoints ~= old_wp then
                                u:ApplySuppressionStatus()
                            end
                        end
                        if status_effect and not u:IsDead() then
                            u:AddStatusEffect(status_effect)
                        end
                    end
                    Sleep(10)
                else
                    if queue then
                        queue.head = 1
                        for i = #queue, 1, -1 do
                            queue[i] = nil
                        end
                    end
                    -- Idle: wake rarely. Queue inserts do not Wakeup; up to ~200ms lag is fine for WP FX.
                    Sleep(200)
                end
            end
        end)
    end

    local apply_suppression = IsValid(unit) and not HasPerk(unit, "Psycho") and wp_dmg and wp_dmg > 0
    local apply_effect = IsValid(unit) and type(effect) == "string" and effect ~= ""
    if apply_suppression or apply_effect then
        table.insert(g_SuppressionApplyQueue, {
            unit = unit,
            damage = apply_suppression and wp_dmg or 0,
            effect = apply_effect and effect or nil,
        })
    end
end

function JAZZ_QueueStatusEffectApplication(unit, effect)
    QueueSuppressionApplication(unit, 0, effect)
end

-- JAZZ-COMBAT-002: miss→graze chance, curve ((100-cth)/100)^2
-- Base cap 25 (orange-band honesty). Within CLOSE_TILES, cap lerps up to CLOSE_CAP (old 50)
-- at point-blank — hidden from UI; player only sees solid CTH.
JAZZ_MISS_GRAZE_CAP = 25
JAZZ_MISS_GRAZE_CLOSE_CAP = 50
JAZZ_MISS_GRAZE_CLOSE_TILES = 8

function JAZZ_CalcMissGrazeCap(dist_tiles)
	dist_tiles = Max(0, tonumber(dist_tiles) or 0)
	if dist_tiles >= JAZZ_MISS_GRAZE_CLOSE_TILES then
		return JAZZ_MISS_GRAZE_CAP
	end
	-- 0 tiles → CLOSE_CAP (50); CLOSE_TILES → CAP (25)
	return JAZZ_MISS_GRAZE_CLOSE_CAP
		- MulDivRound(JAZZ_MISS_GRAZE_CLOSE_CAP - JAZZ_MISS_GRAZE_CAP, dist_tiles, JAZZ_MISS_GRAZE_CLOSE_TILES)
end

function JAZZ_CalcMissGrazeChance(shot_cth, dist_tiles)
	shot_cth = Clamp(tonumber(shot_cth) or 0, 0, 100)
	if shot_cth <= 0 then
		return 0
	end
	local cap = JAZZ_CalcMissGrazeCap(dist_tiles)
	if cap <= 0 then
		return 0
	end
	local miss_pct = 100 - shot_cth
	return Min(cap, (cap * miss_pct * miss_pct) / 10000)
end

-- Cover graze proportional to cover CTH bonus; full cover → 100%.
function JAZZ_CalcCoverGrazeChance(attacker, target, attack_pos, weapon, attack_args)
	if not IsKindOf(target, "Unit") or not attack_pos then
		return 0
	end
	if target:HasStatusEffect("Exposed") or not target:IsAware() then
		return 0
	end
	if target.aim_action_id then
		return 0
	end
	if attack_args and (attack_args.melee_attack or (attack_args.action_id and CombatActions[attack_args.action_id] and CombatActions[attack_args.action_id].ActionType == "Melee Attack")) then
		return 0
	end
	if IsKindOf(weapon, "Firearm") and weapon:HasComponent("IgnoreCoverCtHWhenFullyAimed") and IsFullyAimedAttack(attack_args) then
		return 0
	end
	local cover, _, coverage = target:GetCoverPercentage(attack_pos)
	if not cover then
		return 0
	end
	local cover_mod = Presets.ChanceToHitModifier and Presets.ChanceToHitModifier.Default and Presets.ChanceToHitModifier.Default.RangeAttackTargetStanceCover
	-- Fallbacks match RangeAttackTargetStanceCover params (owner soften 2026-08-05).
	local exposed_value = cover_mod and cover_mod:ResolveValue("ExposedCover") or -12
	local full_value = cover_mod and cover_mod:ResolveValue("Cover") or -45
	if IsKindOf(attacker, "Unit") and CheckSightCondition(attacker, target, const.usObscured) then
		local dust = const.EnvEffects.DustStormCoverCTHPenalty or 0
		exposed_value = exposed_value + dust
		full_value = full_value + dust
	end
	if full_value >= 0 then
		return 0
	end
	local cover_cth = InterpolateCoverEffect(coverage, full_value, exposed_value)
	if cover_cth >= exposed_value then
		return 0
	end
	return Clamp(MulDivRound(-cover_cth, 100, -full_value), 0, 100)
end

local function compile_ignore_colliders(killed_colliders, colliders)
	if #(killed_colliders or empty_table) == 0 then
		return colliders
	end
	local list = table.icopy(killed_colliders)
	if IsValid(colliders) then
		table.insert_unique(list, colliders)
	else
		for _, obj in ipairs(colliders) do
			table.insert_unique(list, obj)
		end
	end
	return list
end

local function find_first_hit(attack_results, hit_obj)
	for si, shot in ipairs(attack_results.shots) do
		for hi, hit in ipairs(shot.hits) do
			if hit.obj == hit_obj then
				return hit
			end
		end
	end
end

function Firearm:GetOverwatchConeParam(param)
	if param == "Angle" then
		return self.OverwatchAngle
	elseif param == "MinRange" then
		--return IsKindOfClasses(self, "MachineGun") and self.WeaponRange or Max(2,MulDivRound(self.WeaponRange, 20, 100))
		return IsKindOfClasses(self, "BrowningM2HMG") and self.WeaponRange or self.BulletDropRange--Max(2,MulDivRound(self.WeaponRange, 20, 100))
	elseif param == "MaxRange" then
		--return IsKindOfClasses(self, "MachineGun") and self.WeaponRange or MulDivRound(self.WeaponRange, 80, 100)
		return MulDivRound(self.WeaponRange, 80, 100)	
	end
	assert(false, string.format("unknown Overwatch parameter '%s'", param))
end

local function CaliberModPropsCombo()
	local items = ClassModifiablePropsNonTranslatableCombo(g_Classes.Firearm)
	-- filter by category
	for i = #items, 1, -1 do
		local meta = Firearm:GetPropertyMetadata(items[i])
		if meta.category ~= "Caliber" then
			table.remove(items, i)
		end
	end
	return items
end

function FirearmBase:GetAutofireShots(action)
	if type(action) == "string" then
		action = CombatActions[action]
	end
	local shots = action:ResolveValue("num_shots") or 1
	-- ExtraBurstShots intentionally disabled: shot counts come only from BurstShots/AutoShots.
	-- WEAPONS-003: no AutoFire → AutoShots=0. Heavy MGs (BrowningM2HMG, MG42, …) still fire via
	-- MGBurstFire only — must not return 0 (anim plays, ExecFirearmAttacks gets empty shots).
	-- LMGs with authored AutoShots keep the longer MGBurst length; else BurstShots.
	-- Component-gated auto (M2Carbine + JAZZ_Autofire): modes appear via EnableFullAuto/EnableBurst
	-- while preset may still have AutoShots/BurstShots=0 until authored — derive from CyclicRPM.
	local function shots_from_rpm(divisor, min_v, max_v)
		local rpm = self.CyclicRPM or 0
		if rpm <= 0 then
			return nil
		end
		return Max(min_v, Min(max_v, DivRound(rpm, divisor)))
	end
	if action.id == "AutoFire" or action.id == "AbakanAutoFire" then
		-- AN94: CyclicRPM=1800 is hyperburst-only; authored AutoShots is sustained length (6).
		shots = self.AutoShots
		if not shots or shots <= 0 then
			shots = action:ResolveValue("num_shots") or shots_from_rpm(100, 3, 14) or 5
		end
	elseif action.id == "AbakanBurst" then
		shots = self.BurstShots
		if not shots or shots <= 0 then
			shots = action:ResolveValue("num_shots") or 2
		end
		local lim = self.BurstLimiter or 0
		if lim > 0 then
			shots = Min(shots, lim)
		end
	elseif action.id == "MGBurstFire" then
		local auto = self.AutoShots or 0
		shots = (auto > 0) and auto or (self.BurstShots or shots)
	elseif action.id == "JAZZ_LargeAutoFire" then
		local auto = self.AutoShots or 0
		if auto <= 0 then
			auto = shots_from_rpm(100, 3, 14) or 5
		end
		shots = auto * 2
	elseif action.id == "BurstFire" or action.id == "JAZZ_Zipper" then
		shots = self.BurstShots
		if not shots or shots <= 0 then
			shots = shots_from_rpm(200, 2, 8) or 3
		end
		local lim = self.BurstLimiter or 0
		if lim > 0 then
			shots = Min(shots, lim)
		end
	elseif action.id == "JAZZ_SmgStorm" then
		local burst = self.BurstShots or 0
		if burst <= 0 then
			burst = shots_from_rpm(200, 2, 8) or 3
		end
		shots = burst * 2
	elseif action.id == "GrizzlyPerk" then
		-- Bayun / UNITS-006: 2× Long Burst (MGBurstFire) length; full damage (dmg_penalty=0 on CA).
		local auto = self.AutoShots or 0
		local long_burst = (auto > 0) and auto or (self.BurstShots or 1)
		shots = Max(1, long_burst) * 2
	end
	return Max(1, shots or 1)
end

-- Jazz_Perk_Nervous / Jazz_Perk_Buzz shot-count helpers (shared by CombatAction GetAutofireShots call sites).
-- UNITS-006: Nervous uses stacked bonus shots (cap 10), not flat +2.
-- Peek-only consume: stack is cleared in Jazz_Perk_Nervous OnUnitAttack after the consumer autofire.
-- Idempotent for Execute→GetActionResults (same base or already-boosted value must not double-add).
function Jazz_ApplyNamedPerkAutofireShots(unit, num_shots)
	if not unit or not num_shots then
		return num_shots
	end
	if HasPerk(unit, "Jazz_Perk_Buzz") then
		num_shots = MulDivRound(num_shots, 150, 100)
	end
	if HasPerk(unit, "Jazz_Perk_Nervous") then
		local bonus = 0
		if type(Jazz_NervousGetBonusShots) == "function" then
			bonus = Jazz_NervousGetBonusShots(unit)
		end
		local last_base = tonumber(unit:GetEffectValue("Jazz_NervousLastBaseShots"))
		local last_out = tonumber(unit:GetEffectValue("Jazz_NervousLastOutShots"))
		if last_base and last_out then
			if num_shots == last_out and (last_out - last_base) == bonus then
				return num_shots
			end
			if num_shots == last_base then
				return last_out
			end
		end
		local out = num_shots + bonus
		unit:SetEffectValue("Jazz_NervousLastBaseShots", num_shots)
		unit:SetEffectValue("Jazz_NervousLastOutShots", out)
		num_shots = out
	end
	return num_shots
end


function FirearmGetGroupingBase(item)
	return item:GetProperty("Grouping") or item.Grouping or 10
end

function FirearmGetGrouping(item)
	local factory = item:GetFactoryResource()
	local max_res = item:GetMaxResource() or factory
	local curr_res = item:GetCurrentResource() or max_res

	if max_res <= 0 then max_res = 1 end
	if factory <= 0 then factory = 1 end

	-- Permille multipliers: condition and remaining repair headroom.
	local condition_permille = Clamp(MulDivRound(curr_res, 1000, max_res), 0, 1000)
	local repair_permille = Clamp(800 + MulDivRound(200, max_res, factory), 100, 1000)
	return MulDivRound(MulDivRound(FirearmGetGroupingBase(item), condition_permille, 1000), repair_permille, 1000)
end

function FirearmBase:GetConditionPercent()
	local max_res = self:GetMaxResource()
	if max_res <= 0 then max_res = 1 end
	return Clamp(MulDivRound(self:GetCurrentResource(), 100, max_res), 0, 100)
end

-- JAZZ-WEAPONS-002 / HOTFIX-003: keyword tiers must follow WeaponResource %, not the
-- stale Condition field vs InventoryItemDef.Condition (which hid Unjam on jams).
function FirearmBase:IsCondition(condition_type)
	return IsConditionType(self:GetConditionPercent(), 100, condition_type)
end

-- JamScore scale 0..1000 matches ReliabilityCheck roll; display % = DivRound(score, 10).
-- Reliability authored range is 5..95. At Rel 95 the platform base jam is 0 even with
-- Poor/Crafted ammo. Below that, positive BaseJamChance is scaled by unreliability so
-- high-Rel guns are not washed out by ammo BaseJam floors. Negative BaseJamChance
-- remains a quality bonus. Serviceable base risk is still capped at 10% later.
-- Read via GetProperty so ammo/component AddModifier ("ammo") applies.
local function JazzGetBaseJamScore(item)
	local reliability = Clamp(item:GetProperty("Reliability") or 50, 5, 95)
	local base_jam = item:GetProperty("BaseJamChance") or 0
	if reliability >= 95 then
		return 0
	end
	local reliability_score = Max(0, 100 - reliability)
	local score
	if base_jam >= 0 then
		local scaled = MulDivRound(base_jam, reliability_score, 95)
		score = Max(reliability_score, scaled)
	else
		score = reliability_score + base_jam
	end
	return Clamp(score, 0, 100)
end

-- Soft additive decile curve shared by current condition and permanent max-resource wear.
-- Mid steps stay playable after ordinary repair; only zero resource hits 100%.
-- When both ratios are worn, only the worse step is full and the other is halved
-- so mid/mid stacks do not explode under rain ×2.
local function JazzGetJamResourcePenalty(resource_percent)
	resource_percent = Clamp(resource_percent or 0, 0, 100)
	if resource_percent <= 0 then
		return 1000
	elseif resource_percent < 10 then
		return 450
	elseif resource_percent < 20 then
		return 320
	elseif resource_percent < 30 then
		return 230
	elseif resource_percent < 40 then
		return 160
	elseif resource_percent < 50 then
		return 110
	elseif resource_percent < 60 then
		return 80
	elseif resource_percent < 70 then
		return 60
	elseif resource_percent < 80 then
		return 55
	elseif resource_percent < 90 then
		return 50
	elseif resource_percent < 100 then
		return 10
	end
	return 0
end

function FirearmBase:GetBaseJamChanceRaw()
	local item = self.parent_weapon or self

	local resource = item:GetCurrentResource() or 1
	local max_resource = item:GetMaxResource() or item:GetFactoryResource() or 1000
	local factory = item:GetFactoryResource() or max_resource
	if max_resource <= 0 or factory <= 0 then
		return 1000
	end

	local condition_percent = Clamp(MulDivRound(resource, 100, max_resource), 0, 100)
	local permanent_percent = Clamp(MulDivRound(max_resource, 100, factory), 0, 100)
	if condition_percent <= 0 or permanent_percent <= 0 then
		return 1000
	end

	local condition_penalty = JazzGetJamResourcePenalty(condition_percent)
	local permanent_penalty = JazzGetJamResourcePenalty(permanent_percent)
	local raw_chance = JazzGetBaseJamScore(item)
		+ Max(condition_penalty, permanent_penalty)
		+ DivRound(Min(condition_penalty, permanent_penalty), 2)

	-- "Normal condition" guard: even the least reliable gun with bad ammunition
	-- stays at or below 10% before weather while both resource ratios are >= 80%.
	if condition_percent >= 80 and permanent_percent >= 80 then
		raw_chance = Min(raw_chance, 100)
	end
	-- Serviceability softener: up to -50 JamScore (-5%) at 100% Min(condition, permanent).
	-- Quadratic in service so near-perfect guns drop ~5pp while mid wear keeps most risk.
	local service = Min(condition_percent, permanent_percent)
	local service_discount = MulDivRound(50, service * service, 10000)
	raw_chance = Max(0, raw_chance - service_discount)
	-- Soft ceiling while any resource remains: display 100% only at fully broken.
	if condition_percent > 0 and permanent_percent > 0 then
		raw_chance = Min(raw_chance, 990)
	end

	if (GameState.RainHeavy or GameState.RainLight) and not item.indoors then
		raw_chance = MulDivRound(raw_chance, 100 + const.EnvEffects.RainJamChanceMod, 100)
	end

	return Clamp(raw_chance, 0, 1000)
end

function FirearmBase:GetJamChance(attacker)
	local jam_chance = self:GetBaseJamChanceRaw()
	if not attacker then
		return jam_chance
	end

	-- Mechanical cuts jam proportionally (strong for mechanics); mercs get a small flat secondary.
	if IsMerc(attacker) then
		jam_chance = jam_chance - MulDivRound(jam_chance, attacker.Mechanical or 0, 120)
		jam_chance = jam_chance - DivRound(
			(attacker.Marksmanship or 0) + (attacker.Wisdom or 0) + attacker:GetLevel(),
			6)
	else
		jam_chance = jam_chance - MulDivRound(jam_chance, attacker.Mechanical or 0, 150)
	end

	return Clamp(jam_chance, 0, 1000)
end

function FirearmBase:GetDisplayJamChancePercent(attacker)
	local score = attacker and self:GetJamChance(attacker) or self:GetBaseJamChanceRaw()
	return DivRound(score, 10)
end

function FirearmBase:GetBaseDegradePerShot()
	return self.DegradePerShot or const.Weapons.DegradePerShot
end

function FirearmBase:ReliabilityCheck(attacker, num_shots)
	local item = self.parent_weapon or self
	local resource = item:GetCurrentResource() or 1
	local max_resource = item:GetMaxResource() or item:GetFactoryResource() or 1000
	if max_resource <= 0 then max_resource = 1 end

	num_shots = num_shots or 1
	local loss = item:GetBaseDegradePerShot() or 1
	local jammed = false
	local fired_count = num_shots

	if not attacker.infinite_condition then
		local jam_chance = item:GetJamChance(attacker)

		if (GameState.RainHeavy or GameState.DustStorm or GameState.FireStorm) and not attacker.indoors then
			loss = MulDivRound(loss, 130, 100)
		elseif GameState.RainLight and not attacker.indoors then
			loss = MulDivRound(loss, 110, 100)
		end

		-- Single-shot attacks keep the historical half-rate; burst/auto roll once
		-- per intended bullet so jam risk scales with queue length (WEAPONS-011).
		if num_shots == 1 then
			jam_chance = DivRound(jam_chance, 2)
		end

		fired_count = 0
		if item.num_safe_attacks and item.num_safe_attacks > 0 then
			fired_count = num_shots
		else
			for _ = 1, num_shots do
				local jam_roll = attacker:Random(1000)
				if jam_roll < jam_chance then
					jammed = true
					break
				end
				fired_count = fired_count + 1
			end
		end

		resource = Max(0, resource - fired_count * loss)
	end

	item.WeaponResource = resource
	local condition_percent = MulDivRound(resource, 100, max_resource)
	return jammed, condition_percent, fired_count
end

-- Compat / ReloadLua: same contract as System_WeaponResourceMaintenance.RepairJammed.
-- resource = absolute WeaponResource, or nil to clear jam only (never pass Condition %).
function FirearmBase:RepairJammed(resource, unit_owner)
	self.jammed = false
	if type(resource) == "number" then
		local max = self:GetMaxResource() or self:GetFactoryResource() or 1
		if max <= 0 then max = 1 end
		self.WeaponResource = Clamp(resource, 0, max)
	end
	NetUpdateHash("WeaponUnjam", self.class, self.id, self.WeaponResource or 0, self:GetMaxResource() or 0)
	if unit_owner then
		CreateFloatingText(unit_owner, T(123820160317, "Unjammed"))
		Msg("InventoryChange", unit_owner)
		if IsKindOf(unit_owner, "Unit") then unit_owner:RecalcUIActions() end
		ObjModified(unit_owner)
		PlayFX("UnjamWeapon", "start", unit_owner, self.class)
	end
end

function Firearm:PrecalcAmmoUse(attacker, num, prediction, isShotgun)
	local fired = num
	local jammed, condition, fired_count
	if not prediction then
		jammed, condition, fired_count = self:ReliabilityCheck(attacker, num)
		if jammed then
			-- Jam on attempting shot i → shots 1..i-1 already left the barrel.
			if (fired_count or 0) > 0 then
				fired = fired_count
			else
				fired = false
			end
		end
	end

	local ammo_type = self.ammo and self.ammo.class
	if fired == false or (not attacker.infinite_ammo and not self.ammo) then
		fired = false
	elseif type(fired) == "number" and self.ammo and self.ammo.Amount < fired and isShotgun ~= true then
		fired = self.ammo.Amount
		if fired <= 0 then
			fired = false
		end
	elseif isShotgun == true and self.ammo and self.ammo.Amount < 1 then
		fired = false
	end

	return fired, jammed, condition, ammo_type
end

-- Vanilla ApplyAmmoUse skips ammo debit when jammed (elseif). Partial mid-burst
-- jam must consume the rounds that already fired, then Jam the weapon.
function Firearm:ApplyAmmoUse(attacker, fired, jammed, condition)
	local weapon = self.parent_weapon or self
	local prev = weapon.Condition
	weapon.Condition = condition or prev
	NetUpdateHash("WeaponAmmoUse", weapon.class, weapon.id, prev, weapon.Condition)
	if prev ~= condition then
		Msg("ItemChangeCondition", self, prev, condition, attacker)
	end

	local fired_count = type(fired) == "number" and fired or 0
	if fired_count > 0 and not attacker.infinite_ammo and not attacker:HasStatusEffect("ManningEmplacement") then
		assert(self.ammo and self.ammo.Amount >= fired_count)
		self.ammo.Amount = Max(0, self.ammo.Amount - fired_count)
		if IsMerc(attacker) and self.ammo.Amount <= 0 then
			if g_Combat and g_Combat.out_of_ammo and not self:AmmoInSquad(attacker) then
				g_Combat.out_of_ammo[self.class] = true
			end
			Msg("OutOfAmmo", attacker, self, fired_count, jammed)
		end
		CreateRealTimeThread(function()
			WaitMsg("CombatActionEnd")
			if not g_Combat or g_Combat:ShouldEndCombat() or not IsMerc(attacker) then return end
			local amount = self.ammo.Amount
			local reloadOptions = GetReloadOptionsForWeapon(self, attacker)
			if not next(reloadOptions) and amount <= 0 then
				PlayVoiceResponse(attacker, "NoAmmo")
			elseif self.MagazineSize >= 5 then
				if self.low_ammo_checked and amount <= (self.MagazineSize / 4) then
					PlayVoiceResponse(attacker, "AmmoLow")
					self.low_ammo_checked = false
				end
			end
		end)
	end

	if jammed then
		self:Jam(attacker)
	end

	if jammed or not self.ammo or self.ammo.Amount <= 0 then
		Msg("InventoryChange", attacker)
	end
	ObjModified(self)
	if weapon ~= self then
		ObjModified(weapon)
	end
end

-- COMBAT-006: enemies in the BulletHell aim cone (LOS + OverwatchAngle, full WeaponRange).
-- Used for cone-wide Will suppression — not only the CTH-resolved primary.
local function JazzCollectBulletHellConeEnemies(attacker, weapon, aim_pos, step_pos, stance)
	if not attacker or not weapon or not IsPoint(aim_pos) then
		return {}
	end
	local origin = step_pos or attacker:GetOccupiedPos() or attacker:GetPos()
	if not origin then
		return {}
	end
	local params = weapon.GetAreaAttackParams
		and weapon:GetAreaAttackParams("BulletHell", attacker, aim_pos, origin, stance)
	local cone_angle = (params and params.cone_angle) or weapon.OverwatchAngle or 0
	if cone_angle <= 0 then
		return {}
	end
	local max_tiles = (params and params.max_range) or 0
	local ca = CombatActions and CombatActions.BulletHell
	if ca and ca.GetMaxAimRange then
		max_tiles = Max(max_tiles, ca:GetMaxAimRange(attacker, weapon) or 0)
	end
	max_tiles = Max(max_tiles, weapon.WeaponRange or 0)
	if max_tiles <= 0 then
		return {}
	end
	local enemies = GetEnemies(attacker) or empty_table
	local any, losValues = CheckLOS(
		enemies,
		origin,
		max_tiles * const.SlabSizeX,
		stance or attacker.stance,
		cone_angle,
		CalcOrientation(origin, aim_pos),
		false
	)
	if not any then
		return {}
	end
	local out = {}
	for i, los in ipairs(losValues or empty_table) do
		local u = enemies[i]
		if los and u and IsValidTarget(u) then
			out[#out + 1] = u
		end
	end
	return out
end

function Firearm:GetAttackResults(action, attack_args)
	PauseInfiniteLoopDetection("CTHCalc")
	-- unpack some params & init default values
	local attacker = attack_args.obj
	local anim = attack_args.anim
	local prediction = attack_args.prediction
	local lof_idx = table.find(attack_args.lof, "target_spot_group", attack_args.target_spot_group or "Torso")
	local lof_data = attack_args.lof and attack_args.lof[lof_idx or 1]
	local target = attack_args.target or lof_data.target_pos
	local target_pos = lof_data.target_pos or (IsValid(target) and target:GetPos())
	if not target_pos:IsValidZ() then
		target_pos = target_pos:SetTerrainZ()
	end
	local target_unit = IsKindOf(target, "Unit") and target
	local applies_tracer_mark = self.ammo and table.find(self.ammo.AppliedEffects or empty_table, "MarkedTraccers")
	local aoe_target_pos = target_unit and target_unit:GetPos() or target_pos -- target_pos is where the shot lands. For AOE attacks we want the object position.
	assert(target)
	assert(target_pos)

	local num_shots = attack_args.num_shots or 0
	local suppressionbonus = attack_args.suppressionbonus or 100
	-- UNITS-006 Batch4 Grom: GL/mortar/AT Will suppression ×2
	if type(Jazz_ApplyGromSuppression) == "function" then
		suppressionbonus = Jazz_ApplyGromSuppression(attacker, suppressionbonus)
	end
	-- UNITS-006 HawksEye: sniper Will suppression ×2
	if type(Jazz_ApplyHawksEyeSuppression) == "function" then
		suppressionbonus = Jazz_ApplyHawksEyeSuppression(attacker, suppressionbonus)
	end

	local seed = Unit:Random()
	local random = BraidRandomCreate(seed)

    --print(lof_data.action_id)

	local aoe_params = attack_args.aoe_params or (attack_args.aoe_action_id and self:GetAreaAttackParams(attack_args.aoe_action_id, attacker, aoe_target_pos, attack_args.step_pos ))
	local consumed_ammo = attack_args.consumed_ammo
	if not consumed_ammo then
		consumed_ammo = 1
		consumed_ammo = Max(consumed_ammo, num_shots)
		consumed_ammo = Max(consumed_ammo, aoe_params and aoe_params.used_ammo or 0)
	end

	-- Cone far-point: vanilla AlwaysHits AOE needed a terrain target at max cone range.
	-- BulletHell is real CTH projectiles — do not push target_pos to SetTerrainZ(far).
	-- That leftover made CalcShotVectors / LoF aim at dirt at WeaponRange (rays eat
	-- ground; even "hit" rolls never connect). VovaVist still AlwaysHits AOE.
	if action.id == "JAZZ_VovaVist" then
		local push = aoe_params or self:GetAreaAttackParams(action.id, attacker, target_pos, attack_args.step_pos)
		if push and push.max_range then
			local dir = (target_pos - attack_args.step_pos):SetZ(0)
			if dir:Len2D() > 0 then
				local far = attack_args.step_pos + SetLen2D(dir, push.max_range * const.SlabSizeX)
				if not far:IsValidZ() then
					far = far:SetTerrainZ()
				end
				target_pos = far
				if not target_unit then
					target = far
				end
			end
		end
	end

	local shot_attack_args = table.copy(attack_args)
	shot_attack_args.ignore_smoke = true
	shot_attack_args.num_shots = num_shots
	shot_attack_args.target_pos = target_pos
	shot_attack_args.target_spot_group = shot_attack_args.target_spot_group or target_unit and g_DefaultShotBodyPart
	shot_attack_args.aim = shot_attack_args.aim or 0
	shot_attack_args.damage_bonus = shot_attack_args.damage_bonus or 0
	shot_attack_args.stealth_kill_chance = shot_attack_args.stealth_kill_chance or 0
	shot_attack_args.stealth_bonus_crit_chance = shot_attack_args.stealth_bonus_crit_chance or 0
	shot_attack_args.prediction = prediction
	shot_attack_args.occupied_pos = shot_attack_args.occupied_pos or attacker:GetOccupiedPos()
	shot_attack_args.can_use_covers = false
	shot_attack_args.output_collisions = true
	shot_attack_args.additional_colliders = target -- Non-units (such as mines) need to be added manually.
	shot_attack_args.require_los = nil

	local fired, jammed, condition, ammo_type = self:PrecalcAmmoUse(attacker, consumed_ammo, prediction)
	--Проверка на шотганы
--	if action.id == "Buckshot" then 
--		--fired = shot_attack_args.num_shots 
--		fired, jammed, condition, ammo_type = self:PrecalcAmmoUse(attacker, consumed_ammo, prediction, true)
--	end


--	if  action.id ~= "Buckshot" then 
		if type(fired) == "number" and num_shots > 0 then
			num_shots = Min(fired, num_shots)
			shot_attack_args.num_shots = fired
		end
--	end

-- JAZZ-WEAPONS-006: pellet count from BuckshotProjectiles (ammo-modifiable), not AutoShots.
-- WEAPONS-011: DoubleBarrel may jam after the first shell — keep one pellet packet per fired shell.
if IsKindOf(self, "Shotgun") then
	local pellets = self.BuckshotProjectiles or 1
	if action.id == "DoubleBarrel" then
		local shells = type(fired) == "number" and Max(fired, 0) or 2
		num_shots = pellets * shells
	else
		num_shots = pellets
	end
end

-- PrecalcAmmoUse returns shells consumed, while shotgun num_shots is the pellet
-- packet. Keep the copied args in sync after restoring the packet size, otherwise
-- DoubleBarrel consumes two shells but downstream execution only sees two shots.
shot_attack_args.num_shots = num_shots



	local cth, baseCth, modifiers
	local cth_action = shot_attack_args.used_action_id and CombatActions[shot_attack_args.used_action_id] or action
	if action.AlwaysHits then
		cth = 100
	elseif action.id == "BulletHell" and target_unit then
		-- Honest CTH at the unit's distance, not the far cone edge (min=max=WeaponRange).
		local cth_args = table.copy(shot_attack_args)
		local unit_pos = target_unit:GetPos()
		if unit_pos and not unit_pos:IsValidZ() then
			unit_pos = unit_pos:SetTerrainZ()
		end
		cth_args.target_pos = unit_pos
		cth, baseCth, modifiers = attacker:CalcChanceToHit(target_unit, cth_action, cth_args)
	elseif attack_args.chance_to_hit then
		cth, modifiers = attack_args.chance_to_hit, attack_args.chance_to_hit_modifiers
	else
		cth, baseCth, modifiers = attacker:CalcChanceToHit(target, cth_action, shot_attack_args)
	end
	local attack_results = {
		weapon = self,
		fired = fired,
		jammed = jammed,
		condition = condition,
		chance_to_hit = cth,
		chance_to_hit_modifiers = modifiers,
		stealth_attack = shot_attack_args.stealth_attack,
		stealth_kill_chance = shot_attack_args.stealth_kill_chance,
		attack_roll = shot_attack_args.attack_roll,
		crit_roll = shot_attack_args.crit_roll,
		ammo_type = ammo_type,
		aim = shot_attack_args.aim,
		dmg_breakdown = shot_attack_args.damage_breakdown and {} or false
	}

	attack_results.crit_chance = attacker:CalcCritChance(self, target, action, shot_attack_args, shot_attack_args.step_pos)

	-- attack/crit rolls
	if prediction then
		if shot_attack_args.multishot then
			attack_results.attack_roll = {}
			attack_results.crit_roll = {}
			for i = 1, num_shots do
				attack_results.attack_roll[i] = 0
				attack_results.crit_roll[i] = 101
			end
		else
			attack_results.attack_roll = 0
			attack_results.crit_roll = 101
		end
		
		if shot_attack_args.stealth_kill_chance > 0 then
			shot_attack_args.stealth_kill_roll = 101
		end
	else
		if shot_attack_args.multishot then
			if type(attack_results.attack_roll) ~= "table" then
				attack_results.attack_roll = {}
				for i = 1, num_shots do
					attack_results.attack_roll[i] = 1 + random(100)
				end
			end
			if type(attack_results.crit_roll) ~= "table" then
				attack_results.crit_roll = {}
				for i = 1, num_shots do
					attack_results.crit_roll[i] = 1 + random(100)
				end
			end
		else
			attack_results.attack_roll = shot_attack_args.attack_roll or (1 + random(100))
			attack_results.crit_roll = shot_attack_args.crit_roll or (1 + random(100))
		end
		if shot_attack_args.stealth_kill_chance > 0 then
			shot_attack_args.stealth_kill_roll = shot_attack_args.stealth_kill_roll or (1 + random(100))
		end
	end

	-- direct shots
	local step_pos3D = shot_attack_args.step_pos:IsValidZ() and shot_attack_args.step_pos or shot_attack_args.step_pos:SetTerrainZ()
	local distAttackerToTarget = step_pos3D:Dist(target_pos)
	local miss_graze_dist_tiles = Max(0, distAttackerToTarget / const.SlabSizeX)
	local dispersion = self:GetMaxDispersion(distAttackerToTarget)
	local max_range = shot_attack_args.range
	if not max_range then
		max_range = Max(MulDivRound(self.WeaponRange, 150, 100), 20) * const.SlabSizeX
	end
	max_range = Max(max_range, distAttackerToTarget + const.SlabSizeX)
	-- Dump already has targeting LoF; do not floor execute rays to 100 tiles.
	local dump_reuse = attack_args.jazz_ai_dump
	if not prediction then
		if dump_reuse then
			max_range = distAttackerToTarget + 8 * const.SlabSizeX
			max_range = Max(max_range, distAttackerToTarget + const.SlabSizeX)
		else
			max_range = Max(max_range, 100 * const.SlabSizeX)
		end
	end
	shot_attack_args.range = max_range

	local stealth_kill
	local roll = attack_results.attack_roll
	local miss, crit
	if shot_attack_args.multishot then
		miss, crit = true, false -- initial values, actual calculation will happen below based on shot results
	else
		crit = attack_results.crit_roll <= attack_results.crit_chance
		miss = roll > attack_results.chance_to_hit
	end

	local target_hit = false
	local out_of_range = true

	local num_hits, total_damage, friendly_fire_dmg, hit_objs = 0, 0, 0, {}
	local unit_damage = {}

	if not miss and shot_attack_args.stealth_kill_chance > 0 then
		stealth_kill = shot_attack_args.stealth_kill_roll <= shot_attack_args.stealth_kill_chance
	end

	local shot_lof_data = shot_attack_args.lof and shot_attack_args.lof[1]
	attack_results.step_pos = shot_lof_data and shot_lof_data.step_pos or shot_attack_args.step_pos
	attack_results.lof_pos1 = shot_lof_data and shot_lof_data.lof_pos1 or attack_results.step_pos -- segment start point (unit center)
	attack_results.attack_pos = shot_lof_data and shot_lof_data.attack_pos or attack_results.step_pos -- weapon shot pos
	attack_results.shots = {}
	attack_results.hit_objs = hit_objs
	attack_results.stealth_kill = stealth_kill
	attack_results.clear_attacks = 0

	-- count num hits and misses and precalc shot vectors for them
	local sfHit = 0x10000
	local sfCrit = 0x20000
	local sfLeading = 0x40000
	local sfAllowGrazing = 0x80000
	local sfCthMask = 0xFF
	local sfRollMask = 0xFF00
	local sfRollOffset = 8
	local num_hits, num_misses, num_grazing = 0, 0, 0
	local shots_data = {}

	shot_attack_args.deployed =
		shot_attack_args.deployed
		or g_Overwatch and g_Overwatch[attacker] and g_Overwatch[attacker].permanent
	-- JAZZ-WEAPONS-006: buckshot pellets are a simultaneous packet, not a recoil queue.
	-- Every pellet uses the same first-bullet CTH (no retention^(i-1)).
	local pellet_pack = action.id == "Buckshot"
		or action.id == "DoubleBarrel"
		or action.id == "CancelShotCone"
		or action.id == "BuckshotBurst"
	local recoil_profile =
		JAZZ_CTHGetRecoilProfile(self, attacker, shot_attack_args.stance, action, shot_attack_args)
	attack_results.recoil_profile = pellet_pack and false or recoil_profile
	attack_results.shot_cth = {}

	for i = 1, num_shots do
		local shot_miss, shot_crit
		local shot_cth = JAZZ_CTHGetBulletChance(
			attack_results.chance_to_hit,
			pellet_pack and 1 or i,
			pellet_pack and nil or recoil_profile,
			attack_results.chance_to_hit > 0
		)

		shot_cth = attacker:CallReactions_Modify("OnCalcShotChanceToHit", shot_cth, attacker, target, i, num_shots)
		if target_unit then
			shot_cth = target_unit:CallReactions_Modify("OnCalcShotChanceToHit", shot_cth, attacker, target, i, num_shots)
		end
		shot_cth = Clamp(
			math.floor(shot_cth + 0.5),
			attack_results.chance_to_hit > 0 and JAZZ_CTH_VALID_SHOT_FLOOR or 0,
			100
		)
		attack_results.shot_cth[i] = shot_cth
		if shot_attack_args.multishot then
			roll = attack_results.attack_roll[i]
			shot_miss = roll > shot_cth
			shot_crit = (not shot_miss) and (attack_results.crit_roll[i] <= attack_results.crit_chance)
			-- update global miss/crit for the attack
			miss = miss and shot_miss
			crit = crit or shot_crit
		else
			shot_miss = (not stealth_kill or i > 1) and roll > shot_cth
			shot_crit = crit and (i == 1)
		end
		-- Jazz_Perk_Lucky (UNITS-006): if CTH>=70% and miss → reroll once per shot
		if shot_miss and attacker and HasPerk(attacker, "Jazz_Perk_Lucky") and shot_cth >= 70 then
			local reroll = 1 + InteractionRand(100, "Jazz_Perk_Lucky")
			if shot_attack_args.multishot and attack_results.attack_roll then
				attack_results.attack_roll[i] = reroll
			else
				roll = reroll
			end
			shot_miss = reroll > shot_cth
			if shot_attack_args.multishot then
				miss = miss and shot_miss
				shot_crit = (not shot_miss) and (attack_results.crit_roll[i] <= attack_results.crit_chance)
				crit = crit or shot_crit
			else
				shot_crit = crit and (i == 1)
			end
		end

		local data = band(shot_cth, sfCthMask)
		data = bor(data, band(shift(roll, sfRollOffset), sfRollMask))
		data = bor(data, shot_miss and 0 or sfHit)
		data = bor(data, shot_crit and sfCrit or 0)
		data = bor(data, (shot_attack_args.multishot or (i == 1)) and sfLeading or 0)
		-- JAZZ-COMBAT-002: miss→graze ^2 curve; cap 25, rises toward 50 under 8 tiles
		if shot_miss and shot_cth > 0 then
			local miss_graze_chance = JAZZ_CalcMissGrazeChance(shot_cth, miss_graze_dist_tiles)
			local miss_span = 100 - shot_cth
			local graze_band = MulDivRound(miss_span, miss_graze_chance, 100)
			if graze_band > 0 and roll < shot_cth + graze_band then
				data = bor(data, sfAllowGrazing)
				num_grazing = num_grazing + 1
			end
		end
		shots_data[i] = data
		num_hits = num_hits + (shot_miss and 0 or 1)
		num_misses = num_misses + (shot_miss and 1 or 0)
		if not prediction then
			NetUpdateHash("FirearmShot", attacker, target, shot_attack_args.action_id, shot_attack_args.stance, self.class, self.id, self == shot_attack_args.weapon, shot_attack_args.occupied_pos, shot_attack_args.step_pos, shot_attack_args.angle, shot_attack_args.anim, shot_attack_args.can_use_covers, shot_attack_args.ignore_smoke, shot_attack_args.penetration_class, shot_attack_args.range, shot_cth, roll, shot_miss)
		end
	end
	
	-- burst distribution simulation
	local precalc_shots, anyHitsTarget
	if not prediction and not dump_reuse then
		local hit_target_pts, miss_target_pts, disp_origin, disp_dir
		local lof_data 
		if shot_lof_data then
			lof_data = shot_lof_data
		else
			lof_data = { target_pos = target_pos, lof_pos1 = attack_results.lof_pos1 }
		end

		local vector_tries = 20
		for i = 1, vector_tries do
			hit_target_pts, miss_target_pts, anyHitsTarget, disp_origin, disp_dir = self:CalcShotVectors(attacker, action.id, target, 
				shot_attack_args, lof_data, 20*guic, guim, guim, num_hits, num_misses, num_grazing)
			if (#hit_target_pts + #miss_target_pts) >= (num_hits + num_misses) then break end
		end
		
		-- use old code as fallback in case all 20 tries have failed (this shouldn't really happen)	
		if (#hit_target_pts + #miss_target_pts) < (num_hits + num_misses) then
			--assert(false, "simulated burst distribition precomputation failed, falling back to randomized miss vectors")
		else
			-- assign target points to shots based on desired outcome
			precalc_shots = {}
			for i = 1, num_shots do
				local shot_miss = band(shots_data[i], sfHit) == 0
				local allow_grazing = band(shots_data[i], sfAllowGrazing) ~= 0
				local shot_vector
				if shot_miss then
					if allow_grazing then
						local idx = table.find(hit_target_pts, "accurate", false)
						if idx then
							shot_vector = table.remove(hit_target_pts, idx)
						end
					end
					if not shot_vector then
						shot_vector = table.remove(miss_target_pts)
					end
					if not shot_vector then -- fallback
						shot_vector = table.remove(hit_target_pts)
					end
				else
					local idx = table.find(hit_target_pts, "accurate", true)
					shot_vector = table.remove(hit_target_pts, idx)
					if not shot_vector then -- fallback
						shot_vector = table.remove(miss_target_pts)
					end
				end
				
				local shot_target_pos = shot_vector.target_pos
				local shot_attack_pos = shot_vector.attack_pos
				-- JAZZ-WEAPONS-007: true misses on non-pellet queues climb with effective_recoil.
				-- Hits and graze stay on CalcShotVectors placement; CTH unchanged.
				-- BulletHell cone spray already fans aim points — climb would throw rays into the sky.
				if not pellet_pack and shot_miss and not allow_grazing and recoil_profile
					and action.id ~= "BulletHell" then
					local aim = (lof_data and lof_data.target_pos) or target_pos
					local lof1 = shot_vector.lof_pos1 or attack_results.lof_pos1
					local climbed = JAZZ_CTHBuildRecoilClimbMissPos(aim, lof1, i, recoil_profile, attacker)
					if climbed then
						shot_target_pos = climbed
					end
				end
				precalc_shots[i] = {
					lof_pos1 = shot_vector.lof_pos1,
					attack_pos = shot_attack_pos,
					target_pos = shot_target_pos,
					shot_data = shots_data[i],
					shot_idx = i,
					dispersion = shot_vector.idx,
				}
			end
			-- Pellet packet may keep vanilla tight→wide sort; rifle queues keep CTH index order.
			if pellet_pack then
				table.sort(precalc_shots, function(a, b)
					return a.dispersion < b.dispersion
				end)
			end
		end
	end

	-- COMBAT-006: fan MISS aim points across the cone at muzzle/chest height.
	-- Hit vectors stay on the resolved unit (honest CTH magdump). Spraying hits too
	-- sent every round into empty dirt — vanilla OverwriteShots was cosmetic for AlwaysHits.
	if action.id == "BulletHell" and precalc_shots and #precalc_shots > 0 then
		local origin = attack_results.lof_pos1 or attack_results.attack_pos or shot_attack_args.step_pos
		if origin then
			local halfAngle = DivRound(self.OverwatchAngle or 0, 2)
			if halfAngle > 0 then
				local newAngle = halfAngle
				local angleStep = MulDivRound(self.OverwatchAngle, 2, #precalc_shots)
				local origin_z = origin:IsValidZ() and origin:z()
				for _, ps in ipairs(precalc_shots) do
					local shot_miss = ps.shot_data and band(ps.shot_data, sfHit) == 0
					if shot_miss and ps.target_pos then
						local rotated = RotateAxis(ps.target_pos, point(0, 0, 4096), newAngle, origin)
						if origin_z then
							rotated = rotated:SetZ(origin_z)
						end
						ps.target_pos = rotated
					end
					if abs(newAngle) >= halfAngle then
						angleStep = -angleStep
					end
					newAngle = newAngle + angleStep
				end
			end
		end
		-- Always mark so ExecFirearmAttacks does not re-run vanilla OverwriteShots on hits.
		attack_results.jazz_bh_arc_sprayed = true
	end

	local misses
	local precalc_damage_data = {}
	local killed_colliders = {}

	local suppression_CTH = attack_results.chance_to_hit + suppressionbonus
	--print('suppressionbonus='..suppressionbonus)

	-- Build once per attack: filtering g_Units every shot is O(shots * units).
	local suppression_enemies, attacker_is_psycho, target_is_psycho, target_will_damage
	local bh_cone_enemies
	local slab = const.SlabSizeX
	local near_range = 5 * slab
	if not prediction then
		attacker_is_psycho = HasPerk(attacker, "Psycho")
		target_is_psycho = IsValid(target_unit) and HasPerk(target_unit, "Psycho")
		local target_sid = target and target.session_id
		local attacker_sid = attacker.session_id
		local attacker_side = attacker.team and attacker.team.side
		suppression_enemies = {}
		for _, u in ipairs(g_Units) do
			if u.HireStatus ~= "Dead"
				and u.session_id ~= target_sid
				and u.session_id ~= attacker_sid
				and IsKindOf(u, "Unit")
				and u.team and u.team.side ~= attacker_side
			then
				suppression_enemies[#suppression_enemies + 1] = u
			end
		end
		-- willDamage ≈ (Damage/10) * (0.4 + 0.6 * sqrt(CTH/100)); integer isqrt of cth*100 ≈ 10*sqrt(cth).
		local c = Max(suppression_CTH, 1)
		local target_sq = 100 * c
		local lo, hi = 0, 1000
		while lo < hi do
			local mid = DivRound(lo + hi + 1, 2)
			if mid * mid <= target_sq then
				lo = mid
			else
				hi = mid - 1
			end
		end
		local f_x100 = Clamp(lo, 10, 200)
		target_will_damage = MulDivRound(
			Max(self.Damage, 1),
			40 + MulDivRound(60, f_x100, 100),
			1000)
		target_will_damage = MulDivRound(target_will_damage, suppressionbonus, 100)
		if action.id == "BulletHell" then
			bh_cone_enemies = JazzCollectBulletHellConeEnemies(
				attacker, self, target_pos, attack_args.step_pos, shot_attack_args.stance)
			if target_unit and IsValidTarget(target_unit) then
				local seen = false
				for _, u in ipairs(bh_cone_enemies) do
					if u == target_unit then
						seen = true
						break
					end
				end
				if not seen then
					bh_cone_enemies[#bh_cone_enemies + 1] = target_unit
				end
			end
		end
	end

	local jazz_hit_lof_cache
	for i = 1, num_shots do
	
		-- clear dead collide units
		local precalc_shot = precalc_shots and precalc_shots[i]
		local shot_data = precalc_shot and precalc_shot.shot_data or shots_data[i]
		
		local shot_cth, shot_miss, shot_crit, allow_grazing
		shot_cth = band(shot_data, sfCthMask)
		shot_miss = band(shot_data, sfHit) == 0
		shot_crit = band(shot_data, sfCrit) ~= 0
		allow_grazing = band(shot_data, sfAllowGrazing) ~= 0
		roll = shift(band(shot_data, sfRollMask), -sfRollOffset)


		if shot_cth > 100 then shot_cth = 0 end

		--print("shot_cth"..shot_cth)
		--print("distance"..distAttackerToTarget / const.SlabSizeX)
	

		--print(shot_attack_args.target_spot_group)

		--chance to shot in random body part (spread within the same CTH; not recoil)
		--print(shot_cth)
		if (shot_cth < 90 or pellet_pack) and not prediction then 
			local rand = random(shot_cth)
			if shot_attack_args.target_spot_group == "Head" then 
				if rand < 10 then 
					rand = random(shot_cth)
					if rand < 3 then shot_attack_args.target_spot_group = "Neck"
					elseif rand < 50 then shot_attack_args.target_spot_group = "Arms"
					else shot_attack_args.target_spot_group = "Torso"
					end
				end
			elseif shot_attack_args.target_spot_group == "Torso" then 
				if rand < 20 then 
					rand = random(shot_cth)
					if rand < 10 then shot_attack_args.target_spot_group = "Head"
					elseif rand < 50 then shot_attack_args.target_spot_group = "Arms"
					elseif rand < 70 then shot_attack_args.target_spot_group = "Groin"	
					elseif rand < 90 then shot_attack_args.target_spot_group = "Legs"	
					else shot_attack_args.target_spot_group = "Torso"													
					end
				end
			elseif shot_attack_args.target_spot_group == "Arms" then 
				if rand < 10 then 
					rand = random(shot_cth)
					if rand < 5 then shot_attack_args.target_spot_group = "Head"
					else shot_attack_args.target_spot_group = "Torso"													
					end
				end
			elseif shot_attack_args.target_spot_group == "Groin" then 
				if rand < 10 then 
					rand = random(shot_cth)
					if rand < 50 then shot_attack_args.target_spot_group = "Legs"
					else shot_attack_args.target_spot_group = "Torso"													
					end
				end
			elseif shot_attack_args.target_spot_group == "Legs" then 
				if rand < 10 then 
					rand = random(shot_cth)
					if rand < 50 then shot_attack_args.target_spot_group = "Groin"
					else shot_attack_args.target_spot_group = "Torso"													
					end
				end
			end
		

		--	attack_data.target_spot_group = hit_data.target_spot_group
		
		--	local lof_idx = table.find(attack_data.lof, "target_spot_group", attack_data.target_spot_group)
		--	local lof_data = attack_data.lof[lof_idx or 1]
		--	hit_data = attack_data.outside_attack_area_lof or attack_data.lof and attack_data.lof[lof_idx or 1]
		--	hit_data.target_pos = miss_target_pos or lof_data.target_pos
		--	hit_data.attack_pos = lof_data.attack_pos
		end
			--print(shot_attack_args.target_spot_group)


		local leading_shot = band(shots_data[i], sfLeading) ~= 0
		local dmg_target = (leading_shot and not shot_miss) and target or false

		--print(leading_shot)

		


		local attack_data, miss_target_pos, hit_data
		if precalc_shot then
			shot_attack_args.attack_pos = precalc_shot.attack_pos
			shot_attack_args.seed = attacker:Random()
			shot_attack_args.ignore_los = attack_args.ignore_los
			shot_attack_args.inside_attack_area_check = attack_args.inside_attack_area_check
			shot_attack_args.forced_hit_on_eye_contact = attack_args.forced_hit_on_eye_contact
			local shot_target
			if action.id == "BulletHell" then
				-- Hits: LoF the resolved unit (body vectors). Misses: chest-height cone fan;
				-- do not ignore the primary (vanilla miss path + far dirt = nobody ever connects).
				if shot_miss then
					shot_target = precalc_shot.target_pos
					miss_target_pos = precalc_shot.target_pos
					shot_attack_args.ignore_colliders = compile_ignore_colliders(killed_colliders, attack_args.ignore_colliders)
					shot_attack_args.ignore_los = true
					shot_attack_args.inside_attack_area_check = false
					shot_attack_args.forced_hit_on_eye_contact = false
				else
					shot_target = attack_args.target_dummy or (IsValid(target) and target) or precalc_shot.target_pos
					shot_attack_args.ignore_colliders = compile_ignore_colliders(killed_colliders, attack_args.ignore_colliders)
				end
			elseif shot_miss then
				shot_target = precalc_shot.target_pos
				miss_target_pos = precalc_shot.target_pos
				if not allow_grazing then
					shot_attack_args.ignore_colliders = compile_ignore_colliders(killed_colliders, target_unit)
				end
				shot_attack_args.ignore_los = true
				shot_attack_args.inside_attack_area_check = false
				shot_attack_args.forced_hit_on_eye_contact = false
			else
				shot_target = attack_args.target_dummy or (IsValid(target) and target) or precalc_shot.target_pos
				shot_attack_args.ignore_colliders = compile_ignore_colliders(killed_colliders, attack_args.ignore_colliders)
			end
			-- Dump execute: targeting LoF already exists. Do not GetLoFData per bullet.
			if dump_reuse and shot_miss then
				attack_data, miss_target_pos = Jazz_SyntheticMissAttackData(
					attacker, precalc_shot, shot_attack_args, miss_target_pos, max_range)
			elseif dump_reuse then
				if not jazz_hit_lof_cache then
					jazz_hit_lof_cache = Jazz_ReuseTargetingAttackData(
						shot_attack_args, attacker, target, precalc_shot)
					if config.JAZZ_AIPerfLog then
						printf("[JAZZ-AI-PERF] SkipShotLoF unit=%s reuse=%s",
							attacker and attacker.unitdatadef_id or "?",
							tostring(not not jazz_hit_lof_cache))
					end
				end
				attack_data = jazz_hit_lof_cache
			else
				attack_data = GetLoFData(attacker, shot_target, shot_attack_args)
			end
		elseif shot_miss then
			if not prediction then -- don't simulate misses for prediction, dispersion uses synced random and executing it from UI code will desync	
				

				local lof_idx = table.find(shot_attack_args.lof, "target_spot_group", shot_attack_args.target_spot_group)
				local lof_data = shot_attack_args.outside_attack_area_lof or shot_attack_args.lof[lof_idx or 1]
				local lof_pos1 = lof_data.lof_pos1
				local miss_tries = 0
				while (not misses or (#misses.clear + #misses.obstructed == 0)) and miss_tries < 8 do
					miss_tries = miss_tries + 1
					misses = self:CalcMissVectors(attacker, action.id, target, lof_pos1, lof_data.target_pos, dispersion)
					dispersion = dispersion + 20*guic -- try shooting wider next time to avoid infinitely retrying to find miss vectors very close to the target
				end
				if not misses or (#misses.clear + #misses.obstructed == 0) then
					miss_target_pos = lof_data.target_pos
				else
					miss_target_pos = self:PickMissTargetPos(attacker, misses, roll, shot_cth)
				end
				-- JAZZ-WEAPONS-007: fallback miss path also climbs for non-pellet queues.
				if not pellet_pack and not allow_grazing and recoil_profile
					and action.id ~= "BulletHell" then
					local aim = (lof_data and lof_data.target_pos) or target_pos
					local climbed = JAZZ_CTHBuildRecoilClimbMissPos(aim, lof_pos1, i, recoil_profile, attacker)
					if climbed then
						miss_target_pos = climbed
					end
				end
				-- extend the shot vector to the max range to make sure the bullet doesn't despawn right after passing by the missed target
				local v = miss_target_pos - lof_pos1
				miss_target_pos = lof_pos1 + SetLen(v, max_range - const.SlabSizeX)
				shot_attack_args.fire_relative_point_attack = false
				shot_attack_args.ignore_colliders = compile_ignore_colliders(killed_colliders, target_unit)
				shot_attack_args.seed = attacker:Random()
				shot_attack_args.ignore_los = true
				shot_attack_args.inside_attack_area_check = false
				shot_attack_args.forced_hit_on_eye_contact = false
				if dump_reuse then
					attack_data, miss_target_pos = Jazz_SyntheticMissAttackData(
						attacker, nil, shot_attack_args, miss_target_pos, max_range)
				else
					attack_data = GetLoFData(attacker, miss_target_pos, shot_attack_args)
				end


			end
		else

			shot_attack_args.fire_relative_point_attack = attack_args.fire_relative_point_attack
			shot_attack_args.ignore_colliders = compile_ignore_colliders(killed_colliders, attack_args.ignore_colliders)
			local target_dummy = attack_args.target_dummy or target
			shot_attack_args.seed = prediction and 0 or attacker:Random()
			shot_attack_args.ignore_los = attack_args.ignore_los
			shot_attack_args.inside_attack_area_check = attack_args.inside_attack_area_check
			shot_attack_args.forced_hit_on_eye_contact = attack_args.forced_hit_on_eye_contact
			if dump_reuse then
				attack_data = Jazz_ReuseTargetingAttackData(shot_attack_args, attacker, target_dummy, nil)
			else
				attack_data = GetLoFData(attacker, target_dummy, shot_attack_args)
			end
		end
		if attack_data then
			local lof_idx
			lof_idx = lof_idx or table.find(attack_data.lof, "target_spot_group", shot_attack_args.target_spot_group)
			hit_data = attack_data.outside_attack_area_lof or attack_data.lof and attack_data.lof[lof_idx or 1]
		else
			local lof_idx = table.find(shot_attack_args.lof, "target_spot_group", shot_attack_args.target_spot_group)
			local lof_data = shot_attack_args.outside_attack_area_lof or shot_attack_args.lof[lof_idx or 1]
			hit_data = {
				obj = attacker,
				hits = empty_table,
				target_pos = miss_target_pos or lof_data.target_pos,
				attack_pos = lof_data.attack_pos
			}
		end

		-- Only used for logging, the modifier isn't displayed anywhere as the
		-- crosshair uses another check.
		if not shot_miss and ((not precalc_shots and hit_data.stuck) or (precalc_shots and not anyHitsTarget)) then
			attack_results.chance_to_hit = 0
			attack_results.obstructed = true
			local mods = attack_results.chance_to_hit_modifiers or {}
			mods[#mods + 1] = {
				{
					id = "NoLineOfFire",
					name = T(604792341662, "No Line of Fire"),
					value = 0
				}
			}
		end

		--if not shot_attack_args.lof and not aoe_params or not fired or jammed or shot_attack_args.chance_only then
		-- WEAPONS-011: mid-burst jam keeps jammed=true with partial fired; only abort when no rounds left the barrel.
		if not fired or (shot_attack_args.chance_only and not shot_attack_args.damage_breakdown) then
			ResumeInfiniteLoopDetection("CTHCalc")
			return attack_results
		end


		

		hit_data.target = dmg_target
		hit_data.critical = shot_crit
		hit_data.record_breakdown = i == 1 and attack_results.dmg_breakdown or false -- Record mods of the first shot only.




		for k, v in pairs(shot_attack_args) do
			if not hit_data[k] then
				hit_data[k] = v		
			end
		end			
		
		if shot_miss and IsValid(target) then			
			for _, hit in ipairs(hit_data.hits) do
				if hit.obj == target then
					if allow_grazing then
						hit.grazing = true
						hit.grazed_miss = true
					else
						hit.stray = true
					end
				end
			end
		end

		-- JAZZ-COMBAT-002: strip C++ smoke/gas LoF grazing; keep miss→graze flags
		for _, hit in ipairs(hit_data.hits) do
			if hit.grazing and not hit.grazed_miss then
				hit.grazing = nil
			end
		end

		self:BulletCalcDamage(hit_data)

		if shot_attack_args.chance_only then  
			ResumeInfiniteLoopDetection("CTHCalc")
			return attack_results 
		end -- Quick out to avoid calculating other shots when we only wanted the dmg breakdown.

		-- gather hit stats for logging
		local shot_target_hit = false


		for _, hit in ipairs(hit_data.hits) do
			local hit_obj = hit.obj
			if IsKindOf(hit_obj, "Unit") and not hit_obj:IsDead() then
				num_hits = num_hits + 1
				if not hit_objs[hit_obj] then
					hit_objs[#hit_objs + 1] = hit_obj
					hit_objs[hit_obj] = true
				end
				
				
				if hit_obj == dmg_target and hit.grazing then
					stealth_kill = false
					shot_attack_args.stealth_kill_roll = -100
				end	
				
				if stealth_kill and hit_obj == dmg_target then
					hit.damage = MulDivRound(target:GetTotalHitPoints(), 125, 100)
					hit.stealth_kill = true
				end
				total_damage = total_damage + hit.damage
				if not attacker:IsOnEnemySide(hit_obj) then
					friendly_fire_dmg = friendly_fire_dmg + hit.damage
				end
				unit_damage[hit_obj] = (unit_damage[hit_obj] or 0) + hit.damage
				if hit_obj == target_unit then
					shot_target_hit = true
				end
				if shot_attack_args.stealth_bonus_crit_chance > 0 and hit.critical then
					hit.stealth_crit = true
				end
			elseif IsKindOf(hit_obj, "Trap") then
				if hit_obj == target then
					shot_target_hit = true
				end
			end
			
			-- presim damage tracking
			if IsKindOf(hit_obj, "CombatObject") then
				local dmg_data = precalc_damage_data[hit_obj] or {}
				precalc_damage_data[hit_obj] = dmg_data
				local hp, temp_hp = hit_obj:PrecalcDamageTaken(hit.damage, dmg_data.hp, dmg_data.temp_hp)
				dmg_data.hp = hp
				dmg_data.temp_hp = temp_hp
				if hp <= 0 then
					table.insert_unique(killed_colliders, hit_obj)
				end
			elseif IsKindOfClasses(hit_obj, "Destroyable", "Trap") then
				table.insert_unique(killed_colliders, hit_obj)
			end
		end
		target_hit = target_hit or shot_target_hit
		out_of_range = out_of_range and shot_attack_args.outside_attack_area
		--print(hit_data)
		

		attack_results.shots[i] = { 
			miss = shot_miss,
			cth = shot_cth,
			roll = roll,
			attack_pos = hit_data.attack_pos,
			target_pos = hit_data.target_pos,
			stuck_pos = hit_data.stuck_pos or hit_data.lof_pos2 or hit_data.target_pos,
			hits = {},
			target_hit = shot_target_hit,
			out_of_range = shot_attack_args.outside_attack_area,
			shot_target = not shot_miss and target_unit,
            cth_loss_per_shot = shot_attack_args.cth_loss_per_shot,
			allyHit = hit_data.allyHit,
			ammo_type = ammo_type,
			clear_attacks = hit_data.clear_attacks,
		}
		if hit_data.allyHit then
			if attack_results.allyHit and attack_results.allyHit ~= hit_data.allyHit then
				attack_results.allyHit = "multiple"
			else
				attack_results.allyHit = hit_data.allyHit
			end
		end
		attack_results.clear_attacks = attack_results.clear_attacks + (hit_data.clear_attacks or 0)
		for _, hit in ipairs(hit_data.hits) do
			hit.direct_shot = true
			hit.shot_idx = i
			hit.weapon = self
			if hit.obj or hit.terrain then
				table.insert(attack_results, hit) -- store in attack_results to obey the convention of returning hits in the array part of the results
				table.insert(attack_results.shots[i].hits, hit) -- also store in the shot description for convenience
			end
		end

		--suppression
		if (action.id == "MGBurstFire") then 
			--suppression_CTH = suppression_CTH * 1.2
		end


		if not prediction then
			if fired and applies_tracer_mark and shot_cth > 0 and IsValid(target_unit) and not target_unit:IsDead() then
				JAZZ_QueueStatusEffectApplication(target_unit, "MarkedTraccers")
			end

			if target_will_damage and target_will_damage > 0
				and action.id ~= "BulletHell"
				and IsValid(target_unit) and target_unit.team and target_unit.team.side ~= attacker.team.side
			then
				if attacker_is_psycho then
					attacker.WillPoints = Min(attacker.MaxWillPoints, attacker.WillPoints + target_will_damage)
				end
				if not target_is_psycho then
					QueueSuppressionApplication(target_unit, target_will_damage)
				end
			end

			local hits = hit_data.hits
			-- BulletHell dumps Will on the whole cone after the burst (below); skip near-hit splash.
			if action.id ~= "BulletHell" and hits and #hits > 0 and suppression_enemies and #suppression_enemies > 0 then
				local damage = Max(self.Damage, 1)
				for _, hit in ipairs(hits) do
					local hit_pos = hit.pos or hit_data.target_pos
					if hit_pos then
						for _, unit in ipairs(suppression_enemies) do
							local dist = unit:GetPos():Dist2D(hit_pos)
							if dist < near_range then
								local clamped = Clamp(DivRound(4 * slab - dist, slab), 0, 4)
								-- nearDamage ≈ (Damage/10) * clamped * 0.15
								local nearDamage = MulDivRound(MulDivRound(damage * clamped * 15, 1, 1000), suppressionbonus, 100)
								if nearDamage > 0 then
									if attacker_is_psycho then
										attacker.WillPoints = Min(attacker.MaxWillPoints, attacker.WillPoints + nearDamage)
									end
									if not HasPerk(unit, "Psycho") then
										QueueSuppressionApplication(unit, nearDamage)
									end
								end
							end
						end
					end
				end
			end
		end

	end

	-- COMBAT-006: one Will dump per cone enemy, same total as a primary under 15–30 shots.
	if not prediction and action.id == "BulletHell" and bh_cone_enemies
		and target_will_damage and target_will_damage > 0 and num_shots > 0 then
		local cone_will = target_will_damage * num_shots
		if attacker_is_psycho and #bh_cone_enemies > 0 then
			attacker.WillPoints = Min(attacker.MaxWillPoints, attacker.WillPoints + cone_will)
		end
		for _, unit in ipairs(bh_cone_enemies) do
			if IsValid(unit) and not unit:IsDead() then
				QueueSuppressionApplication(unit, cone_will)
			end
		end
	end

	attack_results.miss = miss
	attack_results.crit = crit

	if num_shots > 0 and IsValid(target) then
		--[[if miss == target_hit then
			DbgClearTexts()
			DbgClearVectors()
			for _, shot in ipairs(attack_results.shots) do
				DbgAddVector(shot.attack_pos, shot.target_pos - shot.attack_pos, const.clrYellow)
				DbgAddText(string.format("cth: %d, roll: %d (%s)", shot.cth, shot.roll, (shot.roll <= shot.cth) and "hit" or "miss"), shot.target_pos + point(0, 0, guim), const.clrWhite)
				for _, hit in ipairs(shot.hits) do
					DbgAddVector(hit.pos, point(0, 0, 2*guim), const.clrGreen)
				end
			end
			WaitNextFrame()
		end--]]
		--assert(miss ~= target_hit)
	end

	

	-- aoe damage
	local targetHitProjectile = target_hit
	if aoe_params then
		local damage_override = GetAoeDamageOverride(shot_attack_args, attacker, self, shot_attack_args.damage_bonus)
		aoe_params.prediction = shot_attack_args.prediction
		local hits, aoe_total_damage, aoe_friendly_fire_dmg = GetAreaAttackResults(aoe_params, shot_attack_args.aoe_damage_bonus, shot_attack_args.applied_status, damage_override)
		attack_results.area_hits = hits
		total_damage = total_damage + aoe_total_damage
		friendly_fire_dmg = friendly_fire_dmg + aoe_friendly_fire_dmg

		for _, hit in ipairs(hits) do
			hit.weapon = self
			if IsKindOf(hit.obj, "CombatObject") and not hit.obj:IsDead() then
				if IsKindOf(hit.obj, "Unit") and hit.damage > 0 then
					unit_damage[hit.obj] = (unit_damage[hit.obj] or 0) + hit.damage
				end
				local objIsTarget = hit.obj == target
				hit.obj_is_target = objIsTarget
				target_hit = target_hit or (objIsTarget)
				if not hit_objs[hit.obj] then
					hit_objs[#hit_objs + 1] = hit.obj
					hit_objs[hit.obj] = true
					num_hits = num_hits + 1
				else
					-- find the first hit on this target, fold the damage there, reset the damage to 0 so it doesn't get processed in FireSpread
					local direct_hit = find_first_hit(attack_results, hit.obj)
					if direct_hit then
						direct_hit.damage = direct_hit.damage + hit.damage
						hit.damage = 0
					end
				end
			end
		end

	end

	attack_results.num_hits = num_hits
	attack_results.total_damage = total_damage
	attack_results.friendly_fire_dmg = friendly_fire_dmg
	attack_results.target_hit = target_hit
	attack_results.target_hit_projectile = targetHitProjectile
	attack_results.out_of_range = out_of_range
	attack_results.unit_damage = unit_damage
	CompileKilledUnits(attack_results)

	if not prediction then
		--print("Firearm_GetAttackResults", attack_results.fired, attack_results.miss, attack_results.target_hit, attack_results.num_hits)
		NetUpdateHash("Firearm_GetAttackResults", attack_results.fired, attack_results.miss, attack_results.target_hit, attack_results.num_hits)
		g_LastAttackResults = attack_results
		-- Cosmetic buckshot FX after hash; CalcBuckshotScatter uses AsyncRand (not attacker:Random).
		if aoe_params and (shot_attack_args.buckshot_scatter_fx or 0) > 0 then
			attack_results.cosmetic_hits = self:CalcBuckshotScatter(attacker, action, attack_results.attack_pos, target_pos, shot_attack_args.buckshot_scatter_fx, aoe_params)
		end
	end
	ResumeInfiniteLoopDetection("CTHCalc")
	return attack_results
end




function FirearmBase:Unjam(unit)
	local factory = self:GetFactoryResource() or 1000
	local max = self:GetMaxResource()    
	if max <= 0 then max = 1 end
	if factory <= 0 then factory = 1 end

	-- Проверка успеха починки
	local diff = (100 - MulDivRound(self.WeaponResource or 0, 100, max)) / 10 + (100 - (self.Reliability or 50)) / 10 + (self.Deterioration or 0)
	local pass = RollSkillCheck(unit, "Mechanical", diff, 50)

	local amount = unit:Random(100 - unit.Mechanical)
	self.num_safe_attacks = Max(self.num_safe_attacks, const.Weapons.JamFixNumSafeAttacks)

	if pass then
		self.jammed = false
		CreateFloatingText(unit, T(123820160317, "Unjammed"))
		CombatLog("important", T{255429864106, "Jammed weapon was <em>fixed</em> by <DisplayName> (<Mechanical> Mechanical)", unit})
		Msg("InventoryChange", unit)
		if IsKindOf(unit, "Unit") then unit:RecalcUIActions() end
		ObjModified(unit)
		PlayFX("UnjamWeapon", "start", unit, self.class)
		return
	end

	-- Урон при неудаче (JamScore-style percent loss of max resource)
	local condLoss = Clamp(DivRound(amount, 10), 1, 3)
	local loss = MulDivRound(max, condLoss, 100) 

	--print("jam debug")
	--print(max,loss,condLoss,amount)

	self.WeaponResourceMax = Max(1, max - loss)
	self.WeaponResource = Min(self.WeaponResource or 0, self.WeaponResourceMax)

	local newConditionPercent = MulDivRound(self.WeaponResource, 100, self.WeaponResourceMax)
	NetUpdateHash("WeaponUnjam", self.class, self.id, self.WeaponResource, self.WeaponResourceMax)

	if self.WeaponResourceMax <= 1 or newConditionPercent <= 0 then
		CombatLog("important", T{759078917029, "<DisplayName> has <em>broken</em> a jammed weapon in attempt to fix it (<Mechanical> Mechanical)", unit})
		Msg("InventoryChange", unit)
		if IsKindOf(unit, "Unit") then unit:RecalcUIActions() end
		ObjModified(unit)
		PlayFX("BrokeWeapon", "start", unit)
		return
	end

	-- Неудачно, но не сломано
	if IsKindOf(unit, "Unit") then
		CreateFloatingText(unit, T(456744290565, "Jammed"))
	end

	CombatLog("important", T{890000000000250, "Jammed weapon was <em>damaged in attempt to fix</em> by <DisplayName> (<Mechanical> Mechanical): <condLoss> condition lost", SubContext(unit, {condLoss = condLoss})})
	Msg("InventoryChange", unit)
	if IsKindOf(unit, "Unit") then unit:RecalcUIActions() end
	ObjModified(unit)
	self.jammed = false
	PlayFX("UnjamWeapon", "start", unit, self.class)
end



TFormat.bullets =  function(context_obj, bullets, max, icon)
	icon = icon or "<image UI/Icons/Rollover/ammo_placeholder 1400>"
	bullets = bullets or GetBulletCount(context_obj)
	if not bullets then return T(994336406701, "<image UI/Icons/Hud/ammo_infinite>") end
	local max = max or context_obj and context_obj.MagazineSize or context_obj.MaxStacks
	local text = bullets == 0 and "<error><bullets></error>" or "<bullets>"
	if not max then
		return T{370913997359, text, bullets = bullets, icon = icon}
	else
		if bullets > 0 then
			if context_obj and context_obj.MagazineSize and context_obj.ammo.colorStyle and bullets ~= 0 then	
			--	text = T{"<style <ammocolor> ><text></style>/<style InventoryItemsCountMax><max></style>", ammocolor = context_obj.ammo.colorStyle, text = text}
				text = Untranslated("<style " .. context_obj.ammo.colorStyle .. ">" .. text .. "</style>/<style InventoryItemsCountMax><max></style>")
				--text = "<style "..context_obj.ammo.colorStyle..">"..text.."</style>" .. "/<style InventoryItemsCountMax><max></style>"
			else
				text = Untranslated(text .. "/<style InventoryItemsCountMax><max></style>")
			end
		else
			text = Untranslated(text .. "/<style InventoryItemsCountMax><max></style>")
		end
		return T{text, bullets = bullets, max = max or 0, icon = icon}
	end		 
end

-- JAZZ-INV-001: storage (SquadBag/SectorStash) shows Amount only; loadout keeps cur/max.
-- Keep this override storage-aware so a Mod Editor metadata rewrite that drops
-- System_InventoryStacks.lua cannot bring back "/10000" on bag tiles.
function InventoryStack:GetItemSlotUI()
	local storage = (rawget(_G, "JazzIsStorageStackUI") and JazzIsStorageStackUI(self))
		or ((not rawget(_G, "JazzIsStorageStackUI")) and rawget(self, "MaxStacks") == (rawget(const, "JazzStorageStackMax") or 10000))
	if storage then
		if self.colorStyle then
			return Untranslated("<style " .. self.colorStyle .. ">" .. self.Amount .. "<valign bottom 0></style>")
		end
		return Untranslated("<style InventoryItemsCount>" .. self.Amount .. "<valign bottom 0></style>")
	end
	local max = (rawget(_G, "JazzGetPersonalMaxStacks") and JazzGetPersonalMaxStacks(self)) or self.MaxStacks
	if self.colorStyle then
		return Untranslated("<style " .. self.colorStyle .. ">" .. self.Amount .. "<valign bottom 0><style " .. self.colorStyle .. ">/" .. max .. "</style>")
	end
	return T{709831548750, "<style InventoryItemsCount><cur><valign bottom 0><style InventoryItemsCountMax>/<max></style>",
		cur = self.Amount, max = max}
end


function SetpieceShoot.ExecThread(state, Actors, TargetType, TargetUnits, TargetBodyPart, TargetPos, NumShots, ShotInterval, InitialDelay, AnimSpeed, TargetOffset, NumMisses)
	local target_pt, target_obj = SetpieceShoot.ResolveTargetPt(state, TargetType, TargetUnits, TargetBodyPart, TargetPos)
	
	for _, actor in ipairs(Actors) do
		actor:SetCommand("SetpieceAimAt", target_pt)
	end
	-- wait aiming
	while true do
		local done = true
		for _, actor in ipairs(Actors) do
			done = done and actor.command == "SetpieceIdle"
		end
		if done then break end
		WaitMsg("SetpieceUnitAimed", 100)
	end
	
	local threads = SetpieceShootThreads
	for _, actor in ipairs(Actors) do
		if IsValidThread(threads[actor]) then
			DeleteThread(threads[actor])
			threads[actor] = nil
		end
		threads[actor] = CreateGameTimeThread(function()
			local weapon = actor:GetActiveWeapons("Firearm") or actor:GetActiveWeapons("RocketLauncher")
			local zooka = IsKindOf(weapon, "RocketLauncher")
			if not weapon then
				StoreErrorSource(actor, string.format("SetpieceShoot trying to fire an unsupported weapon of class '%s' for actor '%s'", weapon and weapon.class or "(nil)", actor.unitdatadef_id or actor.class))
				return
			end
			local ordnance, target_points
			local is_missed = {}
			
			local attack_data, lof_data
			if IsValid(target_obj) then
				attack_data = actor:ResolveAttackParams("SingleShot", target_obj, {target = target_obj, target_spot_group = TargetBodyPart})
				lof_data = attack_data.lof and attack_data.lof[1]
				target_pt = lof_data and lof_data.target_pos or target_pt
			else
				attack_data = actor:ResolveAttackParams("SingleShot", target_pt)
				if not attack_data.anim then
					attack_data.anim = actor:GetAttackAnim("SingleShot", actor.stance)
				end
			end
			actor:SetPos(attack_data.step_pos)
			local visual_obj = weapon:GetVisualObj(actor)
			
			if zooka then
				ordnance = weapon.ammo
				if not ordnance then
					-- find suitable ammo to fire
					for name, class in sorted_pairs(ClassDescendants("Ordnance")) do
						if class.Caliber == weapon.Caliber then
							ordnance = class
						end
					end
				end
				if not ordnance then
					StoreErrorSource(actor, string.format("SetpieceShoot unable to find suitable ordnance to fire from weapon of class '%s' for actor '%s'", weapon.class, actor.unitdatadef_id or actor.class))
					return
				end
			elseif IsValid(target_obj) then
				-- prepare target points in advance using CalcShotVectors
				local step_pos = attack_data.step_pos or actor:GetPos()
				local lof_pos1 = lof_data and lof_data.lof_pos1 or step_pos
				local num_misses = NumMisses or 0
				local num_hits = NumShots - num_misses
				local shot_attack_args = {target_spot_group = TargetBodyPart, stance = actor.stance, step_pos = step_pos}
				local lof_data = {lof_pos1 = lof_pos1, target_pos = target_pt}
				local hit_vectors, miss_vectors = Firearm:CalcShotVectors(actor, "SingleShot", target_obj, shot_attack_args, lof_data, 20*guic, guim, guim, num_hits, num_misses, 0)				
				local lowest
				target_points = {}
				for _, hit in ipairs(hit_vectors) do
					table.insert(target_points, hit.target_pos)
					if not lowest or (hit.target_pos:z() < lowest:z()) then
						lowest = hit.target_pos
					end
				end
				for _, miss in ipairs(miss_vectors) do
					table.insert(target_points, miss.target_pos)
					is_missed[point_pack(miss.target_pos)] = true
					if not lowest or (miss.target_pos:z() < lowest:z()) then
						lowest = miss.target_pos
					end
				end
				while #target_points < NumShots do -- fallback
					table.insert(target_points, target_pt)
					if not lowest or (target_pt:z() < lowest:z()) then
						lowest = target_pt
					end
				end
				table.sort(target_points, function(a, b) return lowest:Dist(a) < lowest:Dist(b) end)
			elseif TargetOffset and TargetOffset > 0 then
				-- prepare target points in advance by adding target offset
				local dir = (target_pt - actor:GetPos()):SetZ(0)
				if dir:Len2D2() > 0 then
					target_points = {}
					for i = 1, NumShots do
						local z = InteractionRand(TargetOffset, "Setpiece")
						local angle = InteractionRand(360*60, "Setpiece")
						target_points[i] = target_pt + RotateAxis(point(0, 0, z), dir, angle)
					end
				end
			end
			
			Sleep(InitialDelay)
			if IsValid(actor) then
				actor:SetAnimSpeedModifier(AnimSpeed*10)
			end
			for si = 1, NumShots do
				if not IsValid(actor) then break end
				local shot_target_pt = target_points and target_points[si] or target_pt
				actor:SetState(attack_data.anim, 0, 0)
				--Sleep(actor:TimeToMoment(1, "hit") or 0)
				if visual_obj then
					assert(visual_obj:IsValidPos())
					local projectile_spawn_pos = GetWeaponSpotPos(visual_obj, "Muzzle")
					local action_dir = SetLen(shot_target_pt - projectile_spawn_pos, 4096)
					local fx_target = visual_obj.parts.Muzzle or visual_obj.parts.Barrel or visual_obj
					PlayFX("WeaponFire", "start", visual_obj, fx_target, projectile_spawn_pos, action_dir)
					if zooka then
						local dist = projectile_spawn_pos:Dist(shot_target_pt)
						local time = MulDivRound(dist, 1000, const.Combat.RocketVelocity)
						local trajectory = {
							{ pos = projectile_spawn_pos, t = 0 }, 
							{ pos = shot_target_pt, t = time },
						}
						local attaches = visual_obj:GetAttaches("OrdnanceVisual")
						local projectile
						if attaches then
							projectile = attaches[1] 
							projectile:Detach()
						else
							projectile = PlaceObject("OrdnanceVisual", {fx_actor_class = ordnance.class})
							local angle = CalcOrientation(projectile_spawn_pos, shot_target_pt)
							projectile:SetAngle(angle)
						end
						weapon:UpdateRocket()
						PlayFX("RocketFire", "start", projectile)
						
						--projectile:ChangeEntity(ordnance.Entity or "MilitaryCamp_Grenade_01")
						--projectile.fx_actor_class = ordnance.class
						
						local rotation_axis = RotateAxis(axis_x, axis_z, CalcOrientation(shot_target_pt, projectile_spawn_pos))
						CreateGameTimeThread(function()
							AnimateThrowTrajectory(projectile, trajectory, rotation_axis, 0)
							DoneObject(projectile)
						end)
					else
						local hit
						if is_missed[point_pack(shot_target_pt)] then
							hit = {
								distance = shot_target_pt:Dist(projectile_spawn_pos),
								pos = shot_target_pt,
								shot_dir = action_dir,
								setpiece = true,
							}
						else
							hit = {
								obj = target_obj,
								distance = shot_target_pt:Dist(projectile_spawn_pos),
								pos = shot_target_pt,
								shot_dir = action_dir,
								spot_group = TargetBodyPart,
								setpiece = true,
							}
						end
						CreateGameTimeThread(Firearm.ProjectileFly, Firearm, actor, projectile_spawn_pos, shot_target_pt, action_dir, const.Combat.BulletVelocity, {hit})
					end
				end
				Sleep(actor:TimeToAnimEnd())
				if si < NumShots and ShotInterval > 0 and not zooka then
					actor:RestoreAiming(shot_target_pt)
					Sleep(ShotInterval)
				end
			end
			if IsValid(actor) then
				actor:SetAnimSpeedModifier(1000)
			end
			threads[actor] = nil
			Msg("SetpieceShootDone")
		end)
	end
	
	while true do
		local all_done = true
		for _, actor in ipairs(Actors) do
			local thread = threads[actor]
			if IsValidThread(thread) then
				all_done = false
				break
			end
		end
		if all_done then break end
		WaitMsg("SetpieceShootDone", 100)
	end
	
	-- go back to aiming anims
	for _, actor in ipairs(Actors) do
		threads[actor] = nil
		if IsValid(actor) then
			actor:RestoreAiming(target_pt)
		end
	end
end


function Firearm:GetAreaAttackParams(action_id, attacker, target_pos, step_pos, stance)
	local params = { 
		attacker = attacker,
		weapon = self,
		target_pos = target_pos,
		step_pos = step_pos,
		used_ammo = 1,
		damage_mod = 100,
		attribute_bonus = 0,
		dont_destroy_covers = true,
	}
	if attacker then
		params.step_pos = step_pos or attacker:IsValidPos() and (GetPassSlab(attacker) or attacker:GetPos())
		params.stance = stance or attacker.stance
	end
	--if action_id == "Buckshot" or action_id == "DoubleBarrel" or action_id == "BuckshotBurst" or action_id == "CancelShotCone" then
	--	self:FillConeAttackAoeParams(params, attacker)
	--else
	if action_id == "EyesOnTheBack" then
		local effect = attacker:GetStatusEffect("EyesOnTheBack")
		params.cone_angle = effect and (effect:ResolveValue("cone_angle")*60)
		params.min_range = self:GetOverwatchConeParam("MinRange")
		params.max_range = self:GetOverwatchConeParam("MaxRange")
	elseif action_id == "Overwatch" or action_id == "MGRotate" or action_id == "MGSetup" then
		params.cone_angle = self.OverwatchAngle
		params.cone_angle = Max(params.cone_angle,1)
		if self.emplacement_weapon then
			params.min_distance_2d = const.EmplacementWeaponMinDistance2D
		end
		params.min_range = self:GetOverwatchConeParam("MinRange")
		params.max_range = self:GetOverwatchConeParam("MaxRange")
	elseif action_id == "BulletHell" or action_id == "DanceForMe" or action_id == "JAZZ_TargetSweep"  then
		params.cone_angle = self.OverwatchAngle
		params.min_range = self:GetOverwatchConeParam("MinRange")
		params.max_range = self:GetOverwatchConeParam("MaxRange")
		elseif action_id == "JAZZ_VovaVist" then
		params.cone_angle = self.OverwatchAngle * 2
		params.min_range = self:GetOverwatchConeParam("MinRange")
		params.max_range = self:GetOverwatchConeParam("MaxRange")
	elseif action_id == "FireFlare" then	
		params.min_range = self.ammo and self.ammo.AreaOfEffect or 0
		params.max_range = self.ammo and self.ammo.AreaOfEffect or 0
	end
	
	return params
end


function BaseWeapon:PrecalcDamageAndStatusEffects(attacker, target, attack_pos, damage, hit, effect, attack_args, record_breakdown, action, prediction)
	local base_damage = damage
	if IsKindOf(target, "Unit") then
		local seed = target:Random()
		local random = BraidRandomCreate(seed)

		local effects = EffectsTable(effect)
		-- Thermal / IgnoreGrazingHitsWhenFullyAimed: cover graze only (JAZZ-COMBAT-002)
		local ignoreCoverGraze = IsFullyAimedAttack(attack_args) and self:HasComponent("IgnoreGrazingHitsWhenFullyAimed")
		
		-- JAZZ-COMBAT-002: cover graze ∝ cover CTH bonus (cap 100%); no fog/dust/smoke env graze
		local chance = 0
		if not hit.aoe and not hit.melee_attack and not ignoreCoverGraze and not hit.grazed_miss then
			chance = JAZZ_CalcCoverGrazeChance(attacker, target, attack_pos, self, attack_args)
			if chance > 0 then
				hit.grazing_reason = "cover"
			end
		end
		
		if not hit.grazed_miss then
			if not prediction then
				local grazing_roll = random(100)
				if grazing_roll < chance then
					hit.grazing = true
				else
					hit.grazing = nil
					hit.grazing_reason = false
				end
			elseif chance ~= 0 then
				hit.grazing = true
			end
		end
		-- grazing hits (cover / miss→graze) cant crit
		if hit.grazing then
			hit.critical = nil
		end
		--local ignore_armor = hit.aoe or IsKindOf(self, "MeleeWeapon")
		local ignore_armor = false
		-- Order/method of damage buff calculations might need a revision. The are quite a few now and they seem to be added arbitrary.
		if not hit.stray or hit.aoe then
			local data = {
				breakdown = record_breakdown or {},
				effects = {},
				base_damage = damage,
				damage_add = 0,
				damage_percent = 100,
				ignore_armor = false,
				ignore_body_part_damage = {},
				action_id = action and action.id,	
				weapon = self,
				prediction = prediction,
				critical = hit.critical,
				critical_damage = const.Weapons.CriticalDamage,
			}
			local mod_attack_args = attack_args or {}
			local mod_hit_data = hit or {}
			local action_id = action and action.id
			Msg("GatherDamageModifications", attacker, target, action_id, self, mod_attack_args, mod_hit_data, data) -- only called for non-stray hits (no misses)
			if IsKindOf(attacker, "Unit") then
				attacker:CallReactions("OnCalcDamageAndEffects", attacker, target, action, self, mod_attack_args, mod_hit_data, data)
			end
			if IsKindOf(target, "Unit") then
				target:CallReactions("OnCalcDamageAndEffects", attacker, target, action, self, mod_attack_args, mod_hit_data, data)
			end
			damage = Max(0, MulDivRound(data.base_damage + data.damage_add, data.damage_percent, 100))
			if data.critical then
				damage = Max(0, MulDivRound(damage, 100 + data.critical_damage, 100))
			end
			hit.critical = data.critical
			for _, effect in ipairs(data.effects) do
				EffectTableAdd(effects, effect)
			end
			ignore_armor = ignore_armor or data.ignore_armor
							
			local part_def = hit.spot_group and Presets.TargetBodyPart.Default[hit.spot_group]
			if part_def then
				if not data.ignore_body_part_damage[part_def.id] then
					damage = MulDivRound(damage, 100 + part_def.damage_mod, 100)
					if record_breakdown then record_breakdown[#record_breakdown + 1] = { name = part_def.display_name, value = part_def.damage_mod } end
				end
				EffectTableAdd(effects, part_def.applied_effect)
			end
            
			local dist = attacker and attacker:GetDist(target)/const.SlabSizeX or 0
			if (attacker and IsKindOf(self, "Firearm") and self.BulletDropRange) then
				local damage_mod = GetRangeDamageReduction(self, ((dist)*const.SlabSizeX), attacker, action) - 100
				--print(GetRangeAccuracy(self, ((dist - self.BulletDropRange)*const.SlabSizeX)))
				--print("damage reduction")
				local effect_def = CharacterEffectDefs.DamageReduction
				damage = MulDivRound(damage, 100 + damage_mod, 100)
				if record_breakdown then record_breakdown[#record_breakdown + 1] = { name = effect_def.DisplayName, value = damage_mod } end
			end
			
		else
			damage = MulDivRound(damage, 50, 100)
		end
	
		hit.damage = damage
		target:ApplyHitDamageReduction(hit, self, hit.spot_group or g_DefaultShotBodyPart, nil, ignore_armor, record_breakdown)
		if hit.grazing then
			hit.effects = {}
			hit.damage = Max(1, MulDivRound(hit.damage, const.Combat.GrazingHitDamage, 100))
		else
			hit.effects = effects
		end
	else
		--apply dmg mod for non units
		local obj_dmg_mod = (not hit.ignore_obj_damage_mod and self:HasMember("ObjDamageMod")) and self.ObjDamageMod or 100
		if obj_dmg_mod ~= 100 then
			damage = MulDivRound(damage, obj_dmg_mod, 100)
			if record_breakdown then record_breakdown[#record_breakdown + 1] = { name = T{360767699237, "<em><DisplayName></em> damage modifier to objects", self}, value = obj_dmg_mod } end
		end
		if HasPerk(attacker, "CollateralDamage") and IsKindOfClasses(self, "HeavyWeapon", "MachineGun") then
			local collateralDamage = CharacterEffectDefs.CollateralDamage
			local damageBonus = collateralDamage:ResolveValue("objectDamageMod")
			damage = MulDivRound(damage, 100 + damageBonus, 100)
			if record_breakdown then record_breakdown[#record_breakdown + 1] = { name = collateralDamage.DisplayName, value = damageBonus } end
		end
		--apply armor for non units (same scale as unit DR: class + 0.1×bonus)
		local pen_class = GetAttackPenetrationClass(self)
		local armor_class = target and target.armor_class or 0
		--if self.PenetrationClass then self.PenetrationClass = self.PenetrationClass - 1 end
		if pen_class >= armor_class then
			hit.damage = damage or 0
			hit.armor_prevented = 0
		else
			hit.damage = 0
			hit.armor_prevented = damage or 0
		end
		if record_breakdown then 
			local armor_prevented
			if pen_class >= armor_class then
				armor_prevented = 0
			else
				armor_prevented = base_damage or 0
			end
			if hit.damage > (base_damage/2) then
				record_breakdown[#record_breakdown + 1] = { name = T(478438763504, "Armor (Pierced)") }
			else
				record_breakdown[#record_breakdown + 1] = { name = T(360312988514, "Armor"), value = -hit.armor_prevented }
			end
		end
	end
end



--function FirearmBase:GetRolloverType()
--	return self.ItemType or self.RolloverClassTemplate or self.WeaponType
--end

-- Scrap overrides live in GetScrapParts.lua (loads later). Do not redefine here.

local suppression_levels = {
	{debuff = 80, effect = "suppressionPinned"},
	{debuff = 45, effect = "suppressionHeavy2"},
	{debuff = 30, effect = "suppressionHeavy"},
	{debuff = 15, effect = "suppressionMedium"},
	{debuff = 5, effect = "suppressionLight"},
}

local JazzDemoMishapClasses = {
	PipeBomb = true,
	ShapedCharge = true,
}

--- Smoothstep 0..100 → 0..100 (3t²−2t³). No step at ¼ / ½ range.
local function JazzMishapSmoothstepX100(t)
	t = Clamp(t, 0, 100)
	return MulDivRound(MulDivRound(t, t, 100), 300 - 2 * t, 100)
end

function MishapProperties:GetMishapSkillProfile()
	if JazzDemoMishapClasses[self.class] or IsKindOf(self, "ThrowableTrapItem") then
		return "Demo", 60
	end
	if IsKindOfClasses(self, "HeavyWeapon", "FlareGun", "GrenadeLauncher", "RocketLauncher", "Mortar") then
		return "AimedHeavy", 50
	end
	return "ThrowGrenade", 50
end

function MishapProperties:GetMishapSkillBlend(attacker)
	local dex = attacker.Dexterity or 50
	local expl = attacker.Explosives or 50
	local ms = attacker.Marksmanship or 50
	local str = attacker.Strength or 50
	local profile = self:GetMishapSkillProfile()
	if profile == "Demo" then
		return DivRound(expl * 3 + dex, 4)
	elseif profile == "AimedHeavy" then
		return DivRound(ms * 2 + expl, 3)
	end
	-- Throw: Strength (also owns range) + Dexterity + Explosives. No threshold remap.
	return DivRound(str + dex * 2 + expl * 2, 5)
end

--- Thrown: Strength interpolates BaseRange→ThrowMaxRange (`Grenade:GetMaxAimRange`).
--- GL/rocket/mortar: authored WeaponRange. No attacker → item ThrowMaxRange.
function MishapProperties:GetMishapFullRange(attacker)
	if IsKindOfClasses(self, "HeavyWeapon", "FlareGun", "GrenadeLauncher", "RocketLauncher", "Mortar") then
		return (self.WeaponRange or 12) * const.SlabSizeX
	end
	local tiles
	if IsKindOf(attacker, "Unit") and self.GetMaxAimRange then
		tiles = self:GetMaxAimRange(attacker)
		if type(tiles) == "number" and HasPerk(attacker, "Throwing") then
			local def = CharacterEffectDefs and CharacterEffectDefs.Throwing
			local extra = def and def.ResolveValue and def:ResolveValue("RangeIncrease")
			if extra then
				tiles = tiles + extra
			end
		end
	end
	if type(tiles) ~= "number" or tiles <= 0 then
		tiles = self.ThrowMaxRange or self.BaseRange or self.WeaponRange or 12
	end
	return tiles * const.SlabSizeX
end

function MishapProperties:GetEffectiveMishapDist(attacker, target)
	local physical = 0
	if IsPoint(target) then
		physical = attacker:GetDist(target)
	elseif IsValid(target) then
		physical = attacker:GetDist(target)
	end
	local ref = self:GetMishapFullRange(attacker)
	local dist = physical
	for _, data in ipairs(suppression_levels) do
		if attacker:HasStatusEffect(data.effect) then
			dist = dist + MulDivRound(ref, data.debuff, 100)
			break
		end
	end
	local inaccurate = attacker:GetStatusEffect("Inaccurate")
	if inaccurate then
		local stacks = inaccurate.stacks or 1
		dist = dist + MulDivRound(ref, stacks * 20, 100)
	end
	return dist
end

function MishapProperties:GetMishapCapTiles()
	return Max(2 * (self.MaxMishapRange or 4), 8)
end

function MishapProperties:GetMishapChance(attacker, target, async)
	local blend = Clamp(self:GetMishapSkillBlend(attacker), 0, 100)
	local dist_eff = self:GetEffectiveMishapDist(attacker, target)
	local ref = Max(self:GetMishapFullRange(attacker), 1)
	-- t = 0 at the attacker, 100 at personal max (Strength throw / WeaponRange).
	-- Smoothstep: no ¼-safe cliff and no mid-range dump to 100%.
	local t_x100 = Min(100, MulDivRound(dist_eff, 100, ref))
	local s_x100 = JazzMishapSmoothstepX100(t_x100)
	-- blend 100 → 40% at max; blend 50 → 70%; blend 0 → 100%. Floor 25%.
	local far_c = Clamp(100 - MulDivRound(blend, 60, 100), 25, 100)
	return Min(100, MulDivRound(s_x100, far_c, 100))
end

--- Deterministic Min/Max deviation bounds (no RNG). band = "min" | "max".
--- Scatter (min): skill still tightens. Mishap (max): a real miss — skill already
--- cut the chance and must not shrink the landing to 1–2 tiles.
function MishapProperties:GetMishapDeviationBounds(unit, target, band)
	local blend = self:GetMishapSkillBlend(unit)
	local dist_eff = self:GetEffectiveMishapDist(unit, target)
	local dist_tiles = DivRound(dist_eff, const.SlabSizeX)

	local full_tiles = Max(DivRound(self:GetMishapFullRange(unit), const.SlabSizeX), 1)
	local half_tiles = Max(DivRound(full_tiles, 2), 1)
	local scatter_tiles
	if dist_tiles <= half_tiles then
		scatter_tiles = MulDivRound(dist_tiles, full_tiles, half_tiles)
	else
		-- half → full_tiles intensity; full → full_tiles * 125/100
		local over = dist_tiles - half_tiles
		local extra = MulDivRound(full_tiles, 25, 100)
		scatter_tiles = full_tiles + MulDivRound(over, extra, half_tiles)
	end

	local min_range, max_range, dist_mod_x100, skill_mod_x100
	if band == "min" then
		skill_mod_x100 = Clamp(100 - blend, 10, 100)
		min_range = 1 * const.SlabSizeX
		max_range = (self.MinMishapRange or 2) * const.SlabSizeX
		dist_mod_x100 = Clamp(MulDivRound(scatter_tiles, 100, 10), 40, 200)
	else
		-- Mishap: no skill shrink. Floor so RandRange cannot land 1–2 tiles off.
		skill_mod_x100 = 100
		local max_tiles = self.MaxMishapRange or 4
		local min_tiles = Max(4, Max(self.MinMishapRange or 1, DivRound(max_tiles, 2)))
		if min_tiles > max_tiles then
			min_tiles = max_tiles
		end
		min_range = min_tiles * const.SlabSizeX
		max_range = max_tiles * const.SlabSizeX
		dist_mod_x100 = Clamp(MulDivRound(scatter_tiles, 100, 8), 100, 400)
	end

	local min_dev = MulDivRound(MulDivRound(min_range, dist_mod_x100, 100), skill_mod_x100, 100)
	local max_dev = MulDivRound(MulDivRound(max_range, dist_mod_x100, 100), skill_mod_x100, 100)
	if max_dev < min_dev then
		max_dev = min_dev
	end

	local cap = self:GetMishapCapTiles() * const.SlabSizeX
	min_dev = Min(min_dev, cap)
	max_dev = Min(max_dev, cap)
	if max_dev < min_dev then
		max_dev = min_dev
	end
	return min_dev, max_dev
end

local function JazzMishapDeviationVector(self, unit, target, band)
	local min_dev, max_dev = self:GetMishapDeviationBounds(unit, target, band)
	local deviation = unit:RandRange(min_dev, max_dev)
	return Rotate(point(deviation, 0, 0), unit:Random(360 * 60))
end

function MishapProperties:GetMishapDeviationVector(unit, target)
	return JazzMishapDeviationVector(self, unit, target, "max")
end

function MishapProperties:GetMishapDeviationVectorMin(unit, target)
	return JazzMishapDeviationVector(self, unit, target, "min")
end

function MishapProperties:GetMishapDeviationVectorMax(unit, target)
	return JazzMishapDeviationVector(self, unit, target, "max")
end

--- Aim UI reliability 0..100 for GetCTHColor: mixes mishap% with Min-band scatter size.
--- reliability = (100 − mishap%) × (100 − scatter_risk%) / 100
--- scatter_risk = mid(MinBounds) / CapTiles (0..100). No RNG.
function MishapProperties:GetMishapAimReliability(attacker, target)
	local chance = self:GetMishapChance(attacker, target, "async")
	local min_lo, min_hi = self:GetMishapDeviationBounds(attacker, target, "min")
	local mid = DivRound(min_lo + min_hi, 2)
	local cap = Max(self:GetMishapCapTiles() * const.SlabSizeX, 1)
	local scatter_risk = Clamp(MulDivRound(mid, 100, cap), 0, 100)
	local reliability = MulDivRound(100 - chance, 100 - scatter_risk, 100)
	return Clamp(reliability, 0, 100), chance, scatter_risk
end

--- Shared scatter/mishap resolver for grenades and heavy weapons.
--- @return point, boolean mishap_flag
function MishapProperties:ApplyImpactDeviation(attacker, target_pos, attack_args, opts)
	opts = opts or empty_table
	if attack_args.prediction or attack_args.explosion_pos then
		return target_pos, false
	end

	local chance = self:GetMishapChance(attacker, target_pos)
	local is_mishap = CheatEnabled("AlwaysMiss") or attacker:Random(100) < chance
	local max_tries = opts.max_tries or 1
	local resolved = target_pos

	for _ = 1, max_tries do
		local dv = is_mishap and self:GetMishapDeviationVectorMax(attacker, target_pos)
			or self:GetMishapDeviationVectorMin(attacker, target_pos)
		local deviate_pos = target_pos + dv
		if opts.validate_pos then
			local ok = opts.validate_pos(deviate_pos)
			if ok then
				resolved = deviate_pos
				break
			end
		else
			resolved = deviate_pos
			break
		end
	end

	if is_mishap and opts.action then
		attacker:ShowMishapNotification(opts.action)
	end
	return resolved, is_mishap
end

function Firearm:GetMaxDispersion(dist, mod)
	-- generated by online curve fitter: direct (float) form commented out, scaled (int) variant below
	--local td = (dist*1.0) / const.SlabSizeX
	-- return round((-0.0009*td*td + 0.125*td + 0.546) * const.SlabSizeX, 1)
	-- modified formula with reduced weights: round((-0.00045*td*td + 0.0625*td + 0.546) * const.SlabSizeX, 1)
	--local value =((-9 * dist * dist) / const.SlabSizeX + 1250 * dist + 5460 * const.SlabSizeX) / 10000
	--local r = Clamp(self.Recoil / 45, 0, 1)
	local recoil = self.Recoil * 2 or 1

	local value =(MulDivRound(-9, dist * dist, 2) / const.SlabSizeX + 625 * dist + 5460 * const.SlabSizeX) / 10000
	if mod then
		value = MulDivRound(value, mod, 100)
	end
	local max = 70*guic
	if recoil ~= 0 then
		value = MulDivRound(value, 100 + recoil, 100)
		max = MulDivRound(max, 100 + recoil, 100)
		--value = MulDivRound(value, 100 + self.InaccurateSpreadModifier, 100)
		--max = MulDivRound(max, 100 + self.InaccurateSpreadModifier, 100)
	end
	return Min(value, max)
end

-- FAMAS: ShootAP is 5 for cheaper SingleShot; keep AutoFire / LargeAuto at previous AP (+1).
g_JAZZ_FAMAS_AutoAPWrapped = rawget(_G, "g_JAZZ_FAMAS_AutoAPWrapped") or false

local function JazzWrapFAMASAutoAP()
	if rawget(_G, "g_JAZZ_FAMAS_AutoAPWrapped") then
		return
	end
	if not CombatActions then
		return
	end
	for _, id in ipairs({ "AutoFire", "JAZZ_LargeAutoFire" }) do
		local action = CombatActions[id]
		if action and action.GetAPCost then
			local base = action.GetAPCost
			action.GetAPCost = function(self, unit, args)
				local cost = base(self, unit, args)
				if cost and cost > 0 then
					local weapon = self:GetAttackWeapons(unit, args)
					if IsKindOf(weapon, "FAMAS") then
						return cost + (const.Scale.AP or 1000)
					end
				end
				return cost
			end
		end
	end
	rawset(_G, "g_JAZZ_FAMAS_AutoAPWrapped", true)
end

-- BulletHell (Spike signature):
-- 1) GetUIState: accept AbakanAutoFire / JAZZ_LargeAutoFire (vanilla only AutoFire/MGBurstFire).
-- 2) COMBAT-006 v2: FirearmAttack + real multishot projectiles (CTH/Will), cone-arc LoF, no AlwaysHits AOE.
local function JazzFirearmHasBulletHellAutofire(weapon)
	local atts = weapon and weapon.AvailableAttacks
	if not atts then
		return false
	end
	return table.find(atts, "AutoFire")
		or table.find(atts, "MGBurstFire")
		or table.find(atts, "AbakanAutoFire")
		or table.find(atts, "JAZZ_LargeAutoFire")
end

local function JazzWrapBulletHellAutofireGate(action)
	if type(action.GetUIState) ~= "function" or rawget(action, "JazzAutofireGateWrapped") then
		return
	end
	local base = action.GetUIState
	action.GetUIState = function(self, units, args)
		local state, reason = base(self, units, args)
		if state ~= "disabled" or reason ~= AttackDisableReasons.WrongWeapon then
			return state, reason
		end
		local unit = units and units[1]
		if not unit then
			return state, reason
		end
		local weapon1 = self:GetAttackWeapons(unit, args)
		if not JazzFirearmHasBulletHellAutofire(weapon1) then
			return state, reason
		end
		if not weapon1.ammo or weapon1.ammo.Amount < self:ResolveValue("min_ammo") then
			return "disabled", AttackDisableReasons.OutOfAmmo
		end
		local cost = self:GetAPCost(unit, args)
		if cost < 0 then
			return "disabled"
		end
		if not unit:UIHasAP(cost) then
			return "disabled"
		end
		return "enabled"
	end
	rawset(action, "JazzAutofireGateWrapped", true)
end

local function JazzInstallBulletHellProjectiles()
	local action = CombatActions and CombatActions.BulletHell
	if not action then
		return
	end
	JazzWrapBulletHellAutofireGate(action)

	action.AlwaysHits = false

	-- Vanilla min=max=WeaponRange snaps the cone to max range (AlwaysHits leftover).
	-- Honest CTH uses GetMaxAimRange as the physical cap; min 0 lets nearby units be valid.
	if not rawget(action, "JazzAimRangeWrapped") then
		action.GetMinAimRange = function(self, unit, weapon)
			return 0
		end
		rawset(action, "JazzAimRangeWrapped", true)
	end

	if rawget(action, "JazzProjectileResultsWrapped") then
		return
	end
	action.GetActionResults = function(self, unit, args)
		local args = table.copy(args)
		args.weapon = args.weapon or self:GetAttackWeapons(unit, args)
		if not args.weapon or not args.weapon.ammo then
			return
		end
		args.num_shots = Clamp(args.weapon.ammo.Amount, self:ResolveValue("min_ammo"), self:ResolveValue("max_ammo"))
		args.multishot = true
		args.suppressionbonus = args.suppressionbonus or 200
		-- Prediction/UI: resolve a unit in the cone so CTH is vs that unit at their range,
		-- not vs the far cone aim point (vanilla min=max=WeaponRange → honest CTH 0%).
		args.chance_to_hit = nil
		args.chance_to_hit_modifiers = nil
		if IsPoint(args.target) then
			local aoeParams = args.weapon:GetAreaAttackParams(self.id, unit)
			if aoeParams then
				local attackData = unit:ResolveAttackParams(self.id, args.target, {})
				local attackerPos = attackData.step_pos
				local attackerPos3D = attackerPos:IsValidZ() and attackerPos or attackerPos:SetTerrainZ()
				local targetAngle = CalcOrientation(attackerPos, args.target)
				local distance = Clamp(attackerPos3D:Dist(args.target), aoeParams.min_range * const.SlabSizeX, aoeParams.max_range * const.SlabSizeX)
				local enemies = GetEnemies(unit)
				local maxValue, losValues = CheckLOS(enemies, attackerPos, distance, attackData.stance, aoeParams.cone_angle, targetAngle, false)
				if maxValue then
					for i, los in ipairs(losValues) do
						if los and enemies[i] and IsValidTarget(enemies[i]) then
							args.target = enemies[i]
							break
						end
					end
				end
			end
		end
		-- No AOE damage / vanilla Suppressed — cone-wide Will after the burst.
		args.aoe_action_id = false
		args.aoe_params = false
		args.applied_status = false
		args.aoe_damage_bonus = nil
		args.aoe_fx_action = nil
		local attack_args = unit:PrepareAttackArgs(self.id, args)
		attack_args.aoe_action_id = false
		attack_args.aoe_params = false
		attack_args.applied_status = false
		local results = attack_args.weapon:GetAttackResults(self, attack_args)
		return results, attack_args
	end
	rawset(action, "JazzProjectileResultsWrapped", true)
end

-- PERF-003: vanilla CalcMissVectors does GetLoFData on 50 sample points per miss.
-- On 513 maps that stalls Dump/player fire (M3 Fanning). Cheap ring, no LoF probe.
JAZZ_AI_PERF_CHEAP_MISS_MAP_TILES = 256
g_JAZZ_FirearmCalcMissVectorsBase = rawget(_G, "g_JAZZ_FirearmCalcMissVectorsBase") or false
g_JAZZ_FirearmCalcMissVectorsFn = rawget(_G, "g_JAZZ_FirearmCalcMissVectorsFn") or false
g_JAZZ_FirearmFireBulletBase = rawget(_G, "g_JAZZ_FirearmFireBulletBase") or false
g_JAZZ_FirearmFireBulletFn = rawget(_G, "g_JAZZ_FirearmFireBulletFn") or false
g_JAZZ_FirearmProjectileFlyBase = rawget(_G, "g_JAZZ_FirearmProjectileFlyBase") or false
g_JAZZ_FirearmProjectileFlyFn = rawget(_G, "g_JAZZ_FirearmProjectileFlyFn") or false

function Jazz_MapTileSpan()
	local sx, sy = terrain.GetMapSize()
	local slab = const.SlabSizeX or 1
	local tx = sx and DivRound(sx, slab) or 0
	local ty = sy and DivRound(sy, slab) or 0
	return Max(tx, ty)
end

-- Terrain-follow unit pos is 2D (invalid Z). collision.Collide / :z() asserts on JA3Debug.
function Jazz_EnsurePointHasZ(pt)
	if not IsPoint(pt) then
		return pt
	end
	if pt:IsValidZ() then
		return pt
	end
	return pt:SetTerrainZ()
end

-- PERF-004: Dump must not call GetLoFData. One cheap torso/muzzle ray:
-- terrain or unpenetrable solid → stuck (no target hit); otherwise inject the target.
function Jazz_DumpUnitAimPos(unit)
	if not IsValid(unit) then
		return false
	end
	if unit.GetSpotBeginIndex and unit.GetSpotLocPos then
		local idx = unit:GetSpotBeginIndex("Torso")
		if type(idx) == "number" and idx >= 0 then
			local pos = unit:GetSpotLocPos(idx)
			if IsPoint(pos) then
				return Jazz_EnsurePointHasZ(pos)
			end
		end
	end
	local pos = (unit.GetVisualPos and unit:GetVisualPos()) or unit:GetPos()
	return Jazz_EnsurePointHasZ(pos)
end

function Jazz_DumpAttackerAimPos(attacker, weapon)
	if IsKindOf(weapon, "Firearm") and weapon.GetVisualObj then
		local vis = weapon:GetVisualObj(attacker)
		if IsValid(vis) and vis.GetSpotBeginIndex and vis.GetSpotLocPos then
			local idx = vis:GetSpotBeginIndex("Muzzle")
			if type(idx) == "number" and idx >= 0 then
				local pos = vis:GetSpotLocPos(idx)
				if IsPoint(pos) then
					return Jazz_EnsurePointHasZ(pos)
				end
			end
		end
	end
	return Jazz_DumpUnitAimPos(attacker)
end

-- Dest-end heightmap graze (target standing on a slope). Do not ignore
-- origin-adjacent hits: a rock in front of the muzzle is a real blocker.
local function Jazz_DumpNearDest(hit, dest)
	if not IsPoint(hit) or not IsPoint(dest) then
		return true
	end
	local slab = const.SlabSizeX or guim
	local margin = Max(guim, DivRound(slab, 3))
	return hit:Dist(dest) <= margin
end

local function Jazz_DumpOriginFootHit(hit, origin)
	if not IsPoint(hit) or not IsPoint(origin) then
		return false
	end
	local slab = const.SlabSizeX or guim
	local margin = Max(guim, DivRound(slab, 3))
	if hit:Dist(origin) > margin then
		return false
	end
	local oz, hz = origin:z(), hit:z()
	if not oz or not hz then
		return true
	end
	return hz + guim < oz
end

-- Entity/slab rocks are not heightmap: IntersectSegment misses them (L4).
-- First N tiles along the 2D shot that are impassable and not a pit → blocked.
JAZZ_DUMP_CHEAP_IMPASSABLE_SLABS = 3

local function Jazz_DumpCheapImpassableOnLine(origin, dest)
	if not IsPoint(origin) or not IsPoint(dest) then
		return true, origin, "bad_pos"
	end
	if type(terrain.IsPassable) ~= "function" then
		return false, dest, "no_api"
	end
	local slab = const.SlabSizeX or guim
	local dist2d = origin:Dist2D(dest)
	if dist2d <= slab / 2 then
		return false, dest, "close"
	end
	local dir = point(dest:x() - origin:x(), dest:y() - origin:y(), 0)
	if dir:Len() <= 0 then
		return false, dest, "close"
	end
	local origin_h = type(terrain.GetHeight) == "function" and terrain.GetHeight(origin)
		or origin:z()
	local max_steps = rawget(_G, "JAZZ_DUMP_CHEAP_IMPASSABLE_SLABS") or 3
	local steps = Min(max_steps, Max(1, DivRound(dist2d, slab) - 1))
	for step = 1, steps do
		local along = slab * step
		if along >= dist2d - slab / 2 then
			break
		end
		local pt = Jazz_EnsurePointHasZ(origin + SetLen(dir, along))
		local okp, pass = pcall(terrain.IsPassable, pt)
		if okp and pass == false then
			local pt_h = type(terrain.GetHeight) == "function" and terrain.GetHeight(pt)
				or pt:z()
			-- Pit/drop: ground much lower than shooter; bullets can fly over.
			if not (origin_h and pt_h and pt_h + guim < origin_h) then
				return true, Jazz_EnsurePointHasZ(pt), "impassable"
			end
		end
	end
	return false, dest, "clear"
end

-- Returns blocked, origin, dest, stuck_pos, reason
function Jazz_DumpCheapLineOfFire(attacker, target, weapon)
	local origin = Jazz_DumpAttackerAimPos(attacker, weapon)
	local dest = Jazz_DumpUnitAimPos(target)
	if not IsPoint(origin) or not IsPoint(dest) or origin:Dist(dest) <= 0 then
		return true, origin, dest, origin, "bad_pos"
	end
	if type(terrain.IntersectSegment) == "function" then
		local ok, hit = pcall(terrain.IntersectSegment, origin, dest)
		if ok and IsPoint(hit) and not Jazz_DumpNearDest(hit, dest)
			and not Jazz_DumpOriginFootHit(hit, origin) then
			return true, origin, dest, Jazz_EnsurePointHasZ(hit), "terrain"
		end
	end
	local blocked, stuck_pos, reason = Jazz_DumpCheapImpassableOnLine(origin, dest)
	if blocked then
		return true, origin, dest, stuck_pos or origin, reason or "impassable"
	end
	-- Bodies on the segment (allies in LoF): vanilla GetLoFData marks stuck, no target hit.
	local rad = Max(guim, DivRound(const.SlabSizeX or guim, 2))
	if type(SegmentIntersectsSphere) == "function" then
		for _, other in ipairs(g_Units or empty_table) do
			if IsValid(other) and other ~= attacker and other ~= target
				and not other:IsDead() then
				local p = Jazz_DumpUnitAimPos(other)
				if IsPoint(p) then
					local ok, hit = pcall(SegmentIntersectsSphere, origin, dest, p, rad)
					if ok and hit then
						return true, origin, dest, Jazz_EnsurePointHasZ(p), "unit"
					end
				end
			end
		end
	end
	return false, origin, dest, dest, "clear"
end

function Jazz_DumpCheapLineBlocked(attacker, target, weapon)
	local blocked = Jazz_DumpCheapLineOfFire(attacker, target, weapon)
	return not not blocked
end

function Jazz_DumpApplyCheapExecuteHits(lof, attacker, target, weapon)
	if not lof then
		return lof, true
	end
	local blocked, origin, dest, stuck_pos = Jazz_DumpCheapLineOfFire(attacker, target, weapon)
	if IsPoint(origin) then
		lof.lof_pos1 = origin
		lof.attack_pos = origin
		lof.step_pos = Jazz_EnsurePointHasZ(lof.step_pos or origin)
	end
	if IsPoint(dest) then
		lof.target_pos = dest
		lof.lof_pos2 = dest
	end
	if blocked then
		lof.stuck = true
		lof.hits = {}
		lof.stuck_pos = stuck_pos or lof.stuck_pos or dest
		return lof, true
	end
	lof.stuck = false
	lof.stuck_pos = dest or lof.stuck_pos
	if IsValid(target) and IsPoint(origin) and IsPoint(dest) then
		lof.hits = {{
			obj = target,
			pos = dest,
			distance = origin:Dist(dest),
			spot_group = lof.target_spot_group or "Torso",
		}}
	end
	return lof, false
end

-- Cheap miss LoF: valid attack/stuck points without GetLoFData. ProjectileFly needs stuck_pos.
function Jazz_SyntheticMissAttackData(attacker, precalc_shot, shot_attack_args, miss_target_pos, max_range)
	local origin = (precalc_shot and (precalc_shot.lof_pos1 or precalc_shot.attack_pos))
		or (shot_attack_args and (shot_attack_args.attack_pos or shot_attack_args.step_pos))
	local dest = miss_target_pos or (precalc_shot and (precalc_shot.lof_pos2 or precalc_shot.target_pos))
	origin = Jazz_EnsurePointHasZ(origin)
	dest = Jazz_EnsurePointHasZ(dest)
	if not IsPoint(origin) or not IsPoint(dest) then
		return false, miss_target_pos
	end
	local v = dest - origin
	local slab = const.SlabSizeX or 1
	if v:Len() > 0 and max_range and max_range > slab then
		dest = origin + SetLen(v, max_range - slab)
	end
	local attack_pos = Jazz_EnsurePointHasZ((precalc_shot and precalc_shot.attack_pos) or origin)
	local lof = {
		obj = attacker,
		step_pos = (shot_attack_args and shot_attack_args.step_pos) or origin,
		lof_pos1 = origin,
		attack_pos = attack_pos,
		target_pos = dest,
		lof_pos2 = dest,
		stuck_pos = dest,
		hits = {},
		target_spot_group = shot_attack_args and shot_attack_args.target_spot_group,
	}
	return { lof = { lof } }, dest
end

-- Execute hit LoF on large maps: cheap terrain/slab ray (PERF-004), not GetLoFData.
-- A second GetLoFData even at dist+8 stalls on M3 waterfall mesh.
function Jazz_ReuseTargetingAttackData(shot_attack_args, attacker, target, precalc_shot)
	local lof_list = shot_attack_args and shot_attack_args.lof
	local lof_idx = lof_list and table.find(lof_list, "target_spot_group", shot_attack_args.target_spot_group)
	local lof = lof_list and lof_list[lof_idx or 1]
	lof = lof or (shot_attack_args and shot_attack_args.outside_attack_area_lof)
	local weapon = shot_attack_args and shot_attack_args.weapon
	if lof then
		if not IsPoint(lof.step_pos) then
			lof.step_pos = (shot_attack_args and shot_attack_args.step_pos)
				or lof.attack_pos or lof.lof_pos1
		end
		lof.step_pos = Jazz_EnsurePointHasZ(lof.step_pos)
		lof.attack_pos = Jazz_EnsurePointHasZ(lof.attack_pos)
		lof.target_pos = Jazz_EnsurePointHasZ(lof.target_pos)
		lof.lof_pos1 = Jazz_EnsurePointHasZ(lof.lof_pos1)
		lof.lof_pos2 = Jazz_EnsurePointHasZ(lof.lof_pos2)
		lof.stuck_pos = Jazz_EnsurePointHasZ(lof.stuck_pos or lof.target_pos or lof.attack_pos)
		Jazz_DumpApplyCheapExecuteHits(lof, attacker, target, weapon)
		return { lof = { lof }, stuck = lof.stuck }
	end
	local origin = (precalc_shot and (precalc_shot.lof_pos1 or precalc_shot.attack_pos))
		or (shot_attack_args and (shot_attack_args.attack_pos or shot_attack_args.step_pos))
	local dest = (precalc_shot and precalc_shot.target_pos)
		or (IsValid(target) and target:GetVisualPos())
		or (IsValid(target) and target:GetPos())
		or (shot_attack_args and shot_attack_args.target_pos)
	origin = Jazz_EnsurePointHasZ(origin)
	dest = Jazz_EnsurePointHasZ(dest)
	if not IsPoint(origin) or not IsPoint(dest) then
		return false
	end
	lof = {
		obj = attacker,
		step_pos = (shot_attack_args and shot_attack_args.step_pos) or origin,
		lof_pos1 = origin,
		attack_pos = (precalc_shot and precalc_shot.attack_pos) or origin,
		target_pos = dest,
		lof_pos2 = dest,
		stuck_pos = dest,
		hits = {},
		target_spot_group = shot_attack_args and shot_attack_args.target_spot_group,
	}
	Jazz_DumpApplyCheapExecuteHits(lof, attacker, target, weapon)
	return { lof = { lof }, stuck = lof.stuck }
end

function Jazz_EnsureShotStuckPos(shot)
	if not shot then
		return shot
	end
	if IsPoint(shot.attack_pos) then
		shot.attack_pos = Jazz_EnsurePointHasZ(shot.attack_pos)
	end
	if not IsPoint(shot.stuck_pos) then
		shot.stuck_pos = shot.target_pos or shot.attack_pos
	end
	if IsPoint(shot.stuck_pos) then
		shot.stuck_pos = Jazz_EnsurePointHasZ(shot.stuck_pos)
	end
	if IsPoint(shot.target_pos) then
		shot.target_pos = Jazz_EnsurePointHasZ(shot.target_pos)
	end
	return shot
end

-- AimTarget needs lof.step_pos; StartFireAnim needs attack_args.anim.
-- Dump skips GetLoFData, which normally fills both.
function Jazz_EnsureAttackArgsLofStepPos(attack_args, attacker)
	if not attack_args then
		return attack_args
	end
	if IsValid(attacker) and attacker.GetAttackAnim then
		attack_args.stance = attack_args.stance or attacker.stance or "Standing"
		if type(attack_args.anim) ~= "string" then
			attack_args.anim = attacker:GetAttackAnim(attack_args.action_id, attack_args.stance)
		end
	end
	local origin = attack_args.step_pos
	if not IsPoint(origin) and IsValid(attacker) then
		origin = (attacker.GetOccupiedPos and attacker:GetOccupiedPos()) or attacker:GetPos()
	end
	if not IsPoint(origin) then
		return attack_args
	end
	if not origin:IsValidZ() then
		origin = origin:SetTerrainZ()
	end
	attack_args.step_pos = attack_args.step_pos or origin
	local lof_list = attack_args.lof
	if not lof_list then
		return attack_args
	end
	for _, lof in ipairs(lof_list) do
		if lof and not IsPoint(lof.step_pos) then
			lof.step_pos = origin
		end
	end
	return attack_args
end

-- PERF-003: vanilla ProjectileFly collision.Collide on 513 maps stalls DumpFire
-- after CheapShotVectors (M3 Fanning, all-miss). Skip vegetation query; cap fly sleep.
function Jazz_CheapProjectileFly(self, attacker, start_pt, end_pt, dir, speed, hits, target, attack_args)
	if not IsPoint(start_pt) then
		return
	end
	start_pt = Jazz_EnsurePointHasZ(start_pt)
	if not IsPoint(end_pt) then
		end_pt = start_pt
	else
		end_pt = Jazz_EnsurePointHasZ(end_pt)
	end
	dir = SetLen(dir or (end_pt - start_pt), 4096)
	speed = speed or const.Combat.BulletVelocity or 50000
	hits = hits or empty_table
	NetUpdateHash("ProjectileFly", attacker, start_pt, end_pt, dir, speed, hits)

	local fx_actor = false
	if IsKindOf(attacker, "Unit") then
		fx_actor = attacker:CallReactions_Modify("OnUnitChooseProjectileFxActor", fx_actor)
	end
	local projectile = PlaceObject("FXBullet")
	projectile.fx_actor_class = fx_actor
	projectile:SetGameFlags(const.gofAlwaysRenderable)
	projectile:SetPos(start_pt)
	local axis, angle = OrientAxisToVector(1, dir)
	projectile:SetAxis(axis)
	projectile:SetAngle(angle)
	PlayFX("Spawn", "start", projectile)
	local dist = start_pt:Dist(end_pt)
	local fly_time = Min(MulDivRound(dist, 1000, speed), 400)
	projectile:SetPos(end_pt, fly_time)
	Sleep(fly_time)

	local context = {
		attacker = attacker,
		target = target,
		dir = dir,
		target_hit = false,
		last_unit_hit = false,
		water_hit = false,
		fx_target = false,
	}
	for _, hit in ipairs(hits) do
		if hit and hit.pos then
			self:BulletHit(projectile, hit, context)
		end
	end
	if IsValid(target) and not context.target_hit then
		PlayFX("TargetMissed", "start", target)
	end
	PlayFX("Spawn", "end", projectile, false)
	DoneObject(projectile)
end

function Jazz_CheapFirearmMissVectors(attacker, target, attack_pos, target_pos, dispersion)
	if not target_pos then
		return { clear = {}, obstructed = {} }
	end
	if not target_pos:IsValidZ() then
		target_pos = target_pos:SetTerrainZ()
	end
	if attack_pos and not attack_pos:IsValidZ() then
		attack_pos = attack_pos:SetTerrainZ()
	end
	local dir
	if attack_pos then
		dir = target_pos - attack_pos
	end
	if not dir or dir:Len() == 0 then
		dir = Rotate(point(guim, 0, 0), IsValid(attacker) and attacker:GetAngle() or 0)
	end
	dir = SetLen(dir, guim)
	local off = Max(35 * guic, dispersion or (35 * guic))
	local clear = {}
	for i = 1, 8 do
		clear[i] = target_pos + RotateAxis(point(0, 0, off), dir, (i - 1) * 45 * 60)
	end
	return { clear = clear, obstructed = {} }
end

-- PERF-003: do not wrap player/AI CalcMissVectors. Dump skips that path via jazz_ai_dump.
-- Uninstall leftover map-span wrap from earlier PERF-003 experiments.
function Jazz_UninstallFirearmCalcMissVectorsWrap()
	local cls = (g_Classes and g_Classes.Firearm) or Firearm
	if type(cls) ~= "table" then
		return false
	end
	local ourFn = rawget(_G, "g_JAZZ_FirearmCalcMissVectorsFn")
	local base = rawget(_G, "g_JAZZ_FirearmCalcMissVectorsBase")
	if type(base) == "function" and (cls.CalcMissVectors == ourFn or type(ourFn) == "function") then
		if cls.CalcMissVectors == ourFn then
			cls.CalcMissVectors = base
		end
	end
	rawset(_G, "g_JAZZ_FirearmCalcMissVectorsFn", false)
	return true
end

function Jazz_InstallFirearmFireBulletStuckPosWrap()
	local cls = (g_Classes and g_Classes.Firearm) or Firearm
	if type(cls) ~= "table" then
		return false
	end
	local current = cls.FireBullet
	local ourFn = rawget(_G, "g_JAZZ_FirearmFireBulletFn")
	if type(current) ~= "function" then
		return false
	end
	if ourFn and current == ourFn then
		return true
	end
	if current ~= ourFn then
		rawset(_G, "g_JAZZ_FirearmFireBulletBase", current)
	elseif not rawget(_G, "g_JAZZ_FirearmFireBulletBase") then
		return false
	end
	local function wrap(self, attacker, shot, threads, results, attack_args)
		Jazz_EnsureShotStuckPos(shot)
		local base = rawget(_G, "g_JAZZ_FirearmFireBulletBase")
		return base(self, attacker, shot, threads, results, attack_args)
	end
	rawset(_G, "g_JAZZ_FirearmFireBulletFn", wrap)
	cls.FireBullet = wrap
	return true
end

function Jazz_InstallFirearmProjectileFlyWrap()
	local cls = (g_Classes and g_Classes.Firearm) or Firearm
	if type(cls) ~= "table" then
		return false
	end
	local current = cls.ProjectileFly
	local ourFn = rawget(_G, "g_JAZZ_FirearmProjectileFlyFn")
	if type(current) ~= "function" then
		return false
	end
	if ourFn and current == ourFn then
		return true
	end
	if current ~= ourFn then
		rawset(_G, "g_JAZZ_FirearmProjectileFlyBase", current)
	elseif not rawget(_G, "g_JAZZ_FirearmProjectileFlyBase") then
		return false
	end
	local function wrap(self, attacker, start_pt, end_pt, dir, speed, hits, target, attack_args)
		if IsPoint(start_pt) then
			start_pt = Jazz_EnsurePointHasZ(start_pt)
		end
		if not IsPoint(end_pt) and IsPoint(start_pt) then
			end_pt = start_pt
		elseif IsPoint(end_pt) then
			end_pt = Jazz_EnsurePointHasZ(end_pt)
		end
		if attack_args and attack_args.jazz_ai_dump then
			if config.JAZZ_AIPerfLog then
				printf("[JAZZ-AI-PERF] CheapProjectileFly unit=%s",
					attacker and attacker.unitdatadef_id or "?")
			end
			return Jazz_CheapProjectileFly(self, attacker, start_pt, end_pt, dir, speed, hits, target, attack_args)
		end
		local base = rawget(_G, "g_JAZZ_FirearmProjectileFlyBase")
		return base(self, attacker, start_pt, end_pt, dir, speed, hits, target, attack_args)
	end
	rawset(_G, "g_JAZZ_FirearmProjectileFlyFn", wrap)
	cls.ProjectileFly = wrap
	return true
end

Jazz_UninstallFirearmCalcMissVectorsWrap()
Jazz_InstallFirearmFireBulletStuckPosWrap()
Jazz_InstallFirearmProjectileFlyWrap()

function OnMsg.ClassesBuilt()
	JazzWrapFAMASAutoAP()
	JazzInstallBulletHellProjectiles()
	Jazz_UninstallFirearmCalcMissVectorsWrap()
	Jazz_InstallFirearmFireBulletStuckPosWrap()
	Jazz_InstallFirearmProjectileFlyWrap()
end

function OnMsg.ModsReloaded()
	JazzInstallBulletHellProjectiles()
	Jazz_UninstallFirearmCalcMissVectorsWrap()
	Jazz_InstallFirearmFireBulletStuckPosWrap()
	Jazz_InstallFirearmProjectileFlyWrap()
end
