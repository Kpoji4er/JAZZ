-- HaveABlast (Red): toggle retaliate with grenade on hit OR miss; inventory pull if none in hands.
-- Incoming blast −50% while toggled ON: CharacterEffect/HaveABlast.lua (once-flag).

g_JAZZ_AttackReactionHaveABlastWrapped = rawget(_G, "g_JAZZ_AttackReactionHaveABlastWrapped") or false
g_JAZZ_AttackReactionHaveABlastBase = rawget(_G, "g_JAZZ_AttackReactionHaveABlastBase") or false

local JazzHaveABlastThrowSlots = {
	{ action = "ThrowGrenadeA", slot = "Handheld A", x = 1, y = 1 },
	{ action = "ThrowGrenadeB", slot = "Handheld A", x = 2, y = 1 },
	{ action = "ThrowGrenadeC", slot = "Handheld B", x = 1, y = 1 },
	{ action = "ThrowGrenadeD", slot = "Handheld B", x = 2, y = 1 },
}

local function JazzIsThrowableCombatGrenade(item)
	return IsKindOf(item, "Grenade") and not IsKindOf(item, "ThrowableTrapItem") and not IsKindOf(item, "Flare")
end

--- Prefer equipped throw slots; else pull one grenade from Inventory into a free hand slot.
function Jazz_PerkHaveABlastAttackAndWeapon(unit)
	if not IsKindOf(unit, "Unit") then
		return
	end
	for _, entry in ipairs(JazzHaveABlastThrowSlots) do
		local action = CombatActions[entry.action]
		local weapon = action and action:GetAttackWeapons(unit)
		if weapon and JazzIsThrowableCombatGrenade(weapon) then
			return action, weapon
		end
	end

	local inv_grenade
	unit:ForEachItemInSlot("Inventory", function(item)
		if not inv_grenade and JazzIsThrowableCombatGrenade(item) then
			inv_grenade = item
		end
	end)
	if not inv_grenade then
		return
	end

	for _, entry in ipairs(JazzHaveABlastThrowSlots) do
		local action = CombatActions[entry.action]
		if action and not action:GetAttackWeapons(unit) then
			local slot = entry.slot
			if unit:CanAddItem(slot, inv_grenade, entry.x, entry.y) then
				unit:RemoveItem("Inventory", inv_grenade)
				unit:AddItem(slot, inv_grenade, entry.x, entry.y)
				local weapon = action:GetAttackWeapons(unit)
				if weapon then
					return action, weapon
				end
			end
		end
	end
end

local function JazzHaveABlastShouldRetaliate(target, attacker, results, can_retaliate, teamPlaying)
	if not can_retaliate or not IsKindOf(target, "Unit") or not IsKindOf(attacker, "Unit") then
		return false
	end
	if teamPlaying == target.team then
		return false
	end
	if results and results.melee_attack then
		return false
	end
	if not HasPerk(target, "HaveABlast") then
		return false
	end
	if not target:GetEffectValue("HaveABlast") then
		return false
	end
	if target.stance == "Prone" or target:HasStatusEffect("KnockDown") then
		return false
	end
	-- Hit or miss (vanilla AttackReaction is hit-only via `not results.miss`).
	return true
end

local function lInstallAttackReactionHaveABlast()
	if rawget(_G, "g_JAZZ_AttackReactionHaveABlastWrapped") then
		return
	end
	local base = rawget(_G, "AttackReaction")
	if type(base) ~= "function" then
		return
	end
	rawset(_G, "g_JAZZ_AttackReactionHaveABlastBase", base)
	rawset(_G, "g_JAZZ_AttackReactionHaveABlastWrapped", true)

	function AttackReaction(action, attack_args, results, can_retaliate)
		local attacker = attack_args and attack_args.obj
		local target = attack_args and attack_args.target
		local teamPlaying = g_Combat and g_Teams[g_Combat.team_playing]
		local can = can_retaliate
			and action
			and (action.id ~= "CancelShot")
			and not (attack_args and attack_args.stealth_attack)
			and not (attack_args and attack_args.opening_attack)
			and not (attack_args and attack_args.opportunity_attack)

		local want_blast = JazzHaveABlastShouldRetaliate(target, attacker, results, can, teamPlaying)
		-- Suppress vanilla hit-only HaveABlast for this call (we handle hit+miss ourselves).
		if want_blast then
			target:SetEffectValue("HaveABlast", nil)
		end

		local ret = g_JAZZ_AttackReactionHaveABlastBase(action, attack_args, results, can_retaliate)

		if want_blast and IsValid(target) and not target:IsDead() then
			target:SetEffectValue("HaveABlast", true)
			target:Retaliate(
				attacker,
				CharacterEffectDefs.HaveABlast and CharacterEffectDefs.HaveABlast.DisplayName,
				Jazz_PerkHaveABlastAttackAndWeapon
			)
		end
		return ret
	end
end

function OnMsg.ModsReloaded()
	lInstallAttackReactionHaveABlast()
end

function OnMsg.DataLoaded()
	lInstallAttackReactionHaveABlast()
end

lInstallAttackReactionHaveABlast()
