-- JAZZ-UNITS-006 §C Batch3 helpers (Spike/TagTeam/Buns/HawksEye).
-- Install is called from System_NamedPerks_006.lua (do not overwrite OnMsg here).

g_JAZZ_NamedPerks006Batch3Wrapped = rawget(_G, "g_JAZZ_NamedPerks006Batch3Wrapped") or false
g_JAZZ_BunsDamagedTargets = rawget(_G, "g_JAZZ_BunsDamagedTargets") or {}

function Jazz_TagTeamAllyPinDown(attacker, attack_target)
	if not attacker or not attack_target or not g_Pindown then
		return false
	end
	for _, ally in ipairs(attacker.team and attacker.team.units or empty_table) do
		if ally ~= attacker and IsValid(ally) and not ally:IsDead() then
			local pd = g_Pindown[ally]
			if pd then
				local t = pd.target
				if t == attack_target or (IsValid(t) and t == attack_target) then
					return true
				end
			end
		end
	end
	return false
end

function Jazz_BunsTargetDamagedByAlly(attacker, attack_target)
	if not attacker or not attack_target then
		return false
	end
	local bag = rawget(_G, "g_JAZZ_BunsDamagedTargets")
	if type(bag) ~= "table" then
		return false
	end
	local key = attack_target.handle or tostring(attack_target)
	local entry = bag[key]
	return entry and entry ~= attacker
end

function Jazz_BunsMarkDamaged(attacker, attack_target, results)
	if not attacker or not attack_target or not results or results.miss then
		return
	end
	local dmg = results.total_damage or results.dealt_damage or 0
	if type(dmg) ~= "number" or dmg <= 0 then
		dmg = 0
		for _, hit in ipairs(results.hits or empty_table) do
			if hit and type(hit.damage) == "number" and hit.damage > 0 then
				dmg = dmg + hit.damage
			end
		end
	end
	if dmg <= 0 then
		return
	end
	local bag = rawget(_G, "g_JAZZ_BunsDamagedTargets")
	if type(bag) ~= "table" then
		bag = {}
		rawset(_G, "g_JAZZ_BunsDamagedTargets", bag)
	end
	local key = attack_target.handle or tostring(attack_target)
	if not bag[key] then
		bag[key] = attacker
	end
end

function Jazz_ApplyHawksEyeSuppression(attacker, suppressionbonus)
	if not attacker or not HasPerk(attacker, "HawksEye") then
		return suppressionbonus
	end
	local w = attacker.GetActiveWeapons and attacker:GetActiveWeapons("Firearm")
	if w and IsKindOf(w, "SniperRifle") then
		return (suppressionbonus or 100) * 2
	end
	return suppressionbonus
end

function Jazz_InstallNamedPerks006Batch3()
	if rawget(_G, "g_JAZZ_NamedPerks006Batch3Wrapped") then
		return
	end

	local bh = CombatActions and CombatActions.BulletHell
	if bh then
		local params = bh.Parameters or {}
		local has = false
		for _, p in ipairs(params) do
			if p and p.Name == "recharge_on_kill" then
				p.Value = 1
				has = true
				break
			end
		end
		if not has then
			params[#params + 1] = PlaceObj("PresetParamNumber", {
				"Name", "recharge_on_kill",
				"Value", 1,
				"Tag", "<recharge_on_kill>",
			})
			bh.Parameters = params
		end
	end

	-- Track damage for Buns via Unit.OnAttack reaction-style wrap of ExecAttack results path.
	if type(Unit.OnAttack) == "function" and not rawget(Unit, "JazzUnits006BunsWrapped") then
		local base = Unit.OnAttack
		function Unit:OnAttack(action, target, results, attack_args, ...)
			local ret = base(self, action, target, results, attack_args, ...)
			if type(Jazz_BunsMarkDamaged) == "function" and IsKindOf(target, "Unit") then
				Jazz_BunsMarkDamaged(self, target, results)
			end
			return ret
		end
		rawset(Unit, "JazzUnits006BunsWrapped", true)
	elseif not rawget(Unit, "JazzUnits006BunsWrapped") then
		-- Fallback: wrap FirearmAttack return path is too invasive; Buns CE still works if MapVar filled elsewhere.
		rawset(Unit, "JazzUnits006BunsWrapped", true)
	end

	rawset(_G, "g_JAZZ_NamedPerks006Batch3Wrapped", true)
end

function Jazz_NamedPerks006Batch3OnCombatStart()
	rawset(_G, "g_JAZZ_BunsDamagedTargets", {})
end

function Jazz_NamedPerks006Batch3OnTurnStart()
	rawset(_G, "g_JAZZ_BunsDamagedTargets", {})
end
