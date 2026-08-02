-- JAZZ-IMP-001: Mimicry / Veteran / Sniper hooks + IMP personal perk pool.

g_JAZZ_ImpPersonalPerksWrapped = rawget(_G, "g_JAZZ_ImpPersonalPerksWrapped") or false
g_JAZZ_ImpPersonalPerksBase = rawget(_G, "g_JAZZ_ImpPersonalPerksBase") or false
g_JAZZ_UnitSquadHasMercEvalBase = rawget(_G, "g_JAZZ_UnitSquadHasMercEvalBase") or false
g_JAZZ_UnitSquadHasMercEvalWrapped = rawget(_G, "g_JAZZ_UnitSquadHasMercEvalWrapped") or false
g_JAZZ_UnitHasPerkCheckBase = rawget(_G, "g_JAZZ_UnitHasPerkCheckBase") or false
g_JAZZ_UnitHasPerkCheckWrapped = rawget(_G, "g_JAZZ_UnitHasPerkCheckWrapped") or false
g_JAZZ_UnitHasStatCheckBase = rawget(_G, "g_JAZZ_UnitHasStatCheckBase") or false
g_JAZZ_UnitHasStatCheckWrapped = rawget(_G, "g_JAZZ_UnitHasStatCheckWrapped") or false

local JAZZ_IMP_DIALOGUE_PERKS = {
	Negotiator = true,
	Scoundrel = true,
	Psycho = true,
}

local JAZZ_IMP_EXTRA_PERSONAL = {
	"Jazz_Perk_Mimicry",
	"Jazz_Perk_Veteran",
	"Jazz_Perk_Sniper",
}

function JazzIsDialogueSocialPerk(perk)
	return perk and JAZZ_IMP_DIALOGUE_PERKS[perk] or false
end

--- Dialogue-only: Mimicry satisfies Negotiator/Scoundrel/Psycho conversation gates.
function JazzPassesDialoguePerkGate(unit, perk)
	if not perk then
		return false
	end
	if HasPerk(unit, perk) then
		return true
	end
	if JazzIsDialogueSocialPerk(perk) and HasPerk(unit, "Jazz_Perk_Mimicry") then
		return true
	end
	return false
end

local function JazzImpInstallPersonalPerksWrap()
	if rawget(_G, "g_JAZZ_ImpPersonalPerksWrapped") then
		return
	end
	local base = rawget(_G, "ImpGetPersonalPerks")
	if type(base) ~= "function" then
		return
	end
	rawset(_G, "g_JAZZ_ImpPersonalPerksBase", base)
	rawset(_G, "g_JAZZ_ImpPersonalPerksWrapped", true)
	function ImpGetPersonalPerks()
		local list = table.copy(g_JAZZ_ImpPersonalPerksBase() or empty_table)
		for _, id in ipairs(JAZZ_IMP_EXTRA_PERSONAL) do
			-- Skip until CharacterEffectDefs is ready (IMP UI reads Icon/DisplayName/Description).
			if CharacterEffectDefs and CharacterEffectDefs[id] and not table.find(list, id) then
				list[#list + 1] = id
			end
		end
		return list
	end
end

local function JazzImpInstallDialogueConditionWraps()
	if UnitHasPerk and not rawget(_G, "g_JAZZ_UnitHasPerkCheckWrapped") then
		local base = UnitHasPerk.UnitCheck
		if type(base) == "function" then
			rawset(_G, "g_JAZZ_UnitHasPerkCheckBase", base)
			rawset(_G, "g_JAZZ_UnitHasPerkCheckWrapped", true)
			function UnitHasPerk:UnitCheck(unit, obj, context)
				if JazzIsDialogueSocialPerk(self.HasPerk) then
					return JazzPassesDialoguePerkGate(unit, self.HasPerk)
				end
				return g_JAZZ_UnitHasPerkCheckBase(self, unit, obj, context)
			end
		end
	end

	if UnitSquadHasMerc and not rawget(_G, "g_JAZZ_UnitSquadHasMercEvalWrapped") then
		local base = UnitSquadHasMerc.__eval
		if type(base) == "function" then
			rawset(_G, "g_JAZZ_UnitSquadHasMercEvalBase", base)
			rawset(_G, "g_JAZZ_UnitSquadHasMercEvalWrapped", true)
			function UnitSquadHasMerc:__eval(obj, context)
				local perk = self.HasPerk
				if not JazzIsDialogueSocialPerk(perk) then
					return g_JAZZ_UnitSquadHasMercEvalBase(self, obj, context)
				end
				local saved = HasPerk
				rawset(_G, "HasPerk", function(unit, id)
					if id == perk then
						return JazzPassesDialoguePerkGate(unit, id)
					end
					return saved(unit, id)
				end)
				local ok, result = pcall(g_JAZZ_UnitSquadHasMercEvalBase, self, obj, context)
				rawset(_G, "HasPerk", saved)
				if not ok then
					error(result)
				end
				return result
			end
		end
	end

	if UnitHasStat and not rawget(_G, "g_JAZZ_UnitHasStatCheckWrapped") then
		local base = UnitHasStat.UnitCheck
		if type(base) == "function" then
			rawset(_G, "g_JAZZ_UnitHasStatCheckBase", base)
			rawset(_G, "g_JAZZ_UnitHasStatCheckWrapped", true)
			function UnitHasStat:UnitCheck(unit, obj, context)
				if not self.Stat then
					return false
				end
				if unit:IsDead() then
					return false
				end
				local stat = unit[self.Stat] or 0
				if HasPerk(unit, "Jazz_Perk_Veteran") then
					stat = stat + 10
				end
				local result = self:CompareOp(stat, context)
				local textContext = SubContext(unit, { stat = stat, threshold = self.Amount })
				context = context or empty_table
				if result and self.SuccessText and not context.no_log then
					CombatLog("important", T{self.SuccessText, textContext})
				end
				if not result and self.FailText and not context.no_log then
					CombatLog("important", T{self.FailText, textContext})
				end
				if not context.no_log then
					CombatLog("debug", "Skill check of " .. self.Amount .. " " .. self.Stat .. " by " .. (unit.unitdatadef_id or unit.class) .. " " .. tostring(result) .. " (" .. stat .. ")")
				end
				return result
			end
		end
	end
end

function OnMsg.ClassesBuilt()
	JazzImpInstallPersonalPerksWrap()
	JazzImpInstallDialogueConditionWraps()
end

function OnMsg.ModsReloaded()
	JazzImpInstallPersonalPerksWrap()
	JazzImpInstallDialogueConditionWraps()
end

JazzImpInstallPersonalPerksWrap()
JazzImpInstallDialogueConditionWraps()
