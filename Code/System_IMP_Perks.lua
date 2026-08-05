-- JAZZ-IMP-001: Mimicry / Veteran / Sniper hooks + IMP personal perk pool + perk UI fixes.

g_JAZZ_ImpPersonalPerksWrapped = rawget(_G, "g_JAZZ_ImpPersonalPerksWrapped") or false
g_JAZZ_ImpPersonalPerksBase = rawget(_G, "g_JAZZ_ImpPersonalPerksBase") or false
g_JAZZ_UnitSquadHasMercEvalBase = rawget(_G, "g_JAZZ_UnitSquadHasMercEvalBase") or false
g_JAZZ_UnitSquadHasMercEvalWrapped = rawget(_G, "g_JAZZ_UnitSquadHasMercEvalWrapped") or false
g_JAZZ_UnitHasPerkCheckBase = rawget(_G, "g_JAZZ_UnitHasPerkCheckBase") or false
g_JAZZ_UnitHasPerkCheckWrapped = rawget(_G, "g_JAZZ_UnitHasPerkCheckWrapped") or false
g_JAZZ_UnitHasStatCheckBase = rawget(_G, "g_JAZZ_UnitHasStatCheckBase") or false
g_JAZZ_UnitHasStatCheckWrapped = rawget(_G, "g_JAZZ_UnitHasStatCheckWrapped") or false
g_JAZZ_ImpCalcAnswersBase = rawget(_G, "g_JAZZ_ImpCalcAnswersBase") or false
g_JAZZ_ImpCalcAnswersWrapped = rawget(_G, "g_JAZZ_ImpCalcAnswersWrapped") or false
g_JAZZ_ImpPerksLayoutPatched = rawget(_G, "g_JAZZ_ImpPerksLayoutPatched") or false

local JAZZ_IMP_DIALOGUE_PERKS = {
	Negotiator = true,
	Scoundrel = true,
	Psycho = true,
}

-- Personal IMP pool extras (Personality). Sniper is Perk-Specialization → tactical grid.
local JAZZ_IMP_EXTRA_PERSONAL = {
	"Jazz_Perk_Mimicry",
	"Jazz_Perk_Veteran",
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

--- Drop false/empty tactical slots from ImpCalcAnswers (vanilla always inserts 2 slots).
function JazzSanitizeImpPerks(perks)
	if type(perks) ~= "table" then
		return perks
	end
	if type(perks.tactical) == "table" then
		local cleaned = {}
		for _, entry in ipairs(perks.tactical) do
			if type(entry) == "table" and type(entry.perk) == "string" and entry.perk ~= "" then
				cleaned[#cleaned + 1] = entry
			end
		end
		perks.tactical = cleaned
	end
	if type(perks.personal) == "table" and perks.personal.perk == false then
		perks.personal = {}
	end
	return perks
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

local function JazzImpInstallCalcAnswersWrap()
	if rawget(_G, "g_JAZZ_ImpCalcAnswersWrapped") then
		return
	end
	local base = rawget(_G, "ImpCalcAnswers")
	if type(base) ~= "function" then
		return
	end
	rawset(_G, "g_JAZZ_ImpCalcAnswersBase", base)
	rawset(_G, "g_JAZZ_ImpCalcAnswersWrapped", true)
	function ImpCalcAnswers(...)
		local stats, perks = g_JAZZ_ImpCalcAnswersBase(...)
		return stats, JazzSanitizeImpPerks(perks)
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

-- Tactical specialization grid: vanilla uses 5 cols (2 rows for ~10 presets).
-- Jazz_Perk_Sniper adds an 11th → 3rd row overlaps Prev/Done. Prefer 6 cols (still 2 rows).
local JAZZ_IMP_TACTICAL_COLS = 6

--- Personal perk row: vanilla HList @ spacing 46 overflows after Mimicry/Veteran.
--- Keep HList (HWrap stole clicks from the tactical Grid below). Tighten spacing only.
local function JazzImpWalkPatchPersonalHList(node, depth)
	if type(node) ~= "table" or (depth or 0) > 48 then
		return false
	end
	-- Prefer the HList that directly hosts the "personal perks" ForEach comment.
	local has_personal_foreach = false
	for _, v in ipairs(node) do
		if type(v) == "table" and v.comment == "personal perks" then
			has_personal_foreach = true
			break
		end
	end
	if has_personal_foreach and node.LayoutMethod == "HList" and (node.LayoutHSpacing or 0) >= 40 then
		node.LayoutHSpacing = 12
		return true
	end
	-- Fallback: first HList with spacing 46 (vanilla personal row; never touch Grid).
	if node.LayoutMethod == "HList" and node.LayoutHSpacing == 46 then
		node.LayoutHSpacing = 12
		return true
	end
	for _, v in ipairs(node) do
		if type(v) == "table" and JazzImpWalkPatchPersonalHList(v, (depth or 0) + 1) then
			return true
		end
	end
	for k, v in pairs(node) do
		if type(k) ~= "number" and type(v) == "table" and JazzImpWalkPatchPersonalHList(v, (depth or 0) + 1) then
			return true
		end
	end
	return false
end

--- Tactical Grid: tighter H spacing + 6-column placement (no HWrap — click-safe).
local function JazzImpWalkPatchTacticalGrid(node, depth)
	if type(node) ~= "table" or (depth or 0) > 48 then
		return false
	end
	if node.LayoutMethod == "Grid" and (node.LayoutHSpacing or 0) >= 40 and node.UniformColumnWidth then
		node.LayoutHSpacing = 18
		node.LayoutVSpacing = math.min(node.LayoutVSpacing or 10, 6)
		for _, child in ipairs(node) do
			if type(child) == "table" and type(child.run_after) == "function" and not child.jazz_imp_cols_patched then
				local base = child.run_after
				local cols = JAZZ_IMP_TACTICAL_COLS
				child.run_after = function(c, context, item, i, n, last)
					base(c, context, item, i, n, last)
					-- Integer-safe column/row (vanilla used i-(i-1)/5*5).
					local idx = (type(i) == "number" and i or 1) - 1
					local col = (idx % cols) + 1
					local row = math.floor(idx / cols) + 1
					if c.SetGridX then
						c:SetGridX(col)
					end
					if c.SetGridY then
						c:SetGridY(row)
					end
				end
				child.jazz_imp_cols_patched = true
			end
		end
		return true
	end
	for _, v in ipairs(node) do
		if type(v) == "table" and JazzImpWalkPatchTacticalGrid(v, (depth or 0) + 1) then
			return true
		end
	end
	for k, v in pairs(node) do
		if type(k) ~= "number" and type(v) == "table" and JazzImpWalkPatchTacticalGrid(v, (depth or 0) + 1) then
			return true
		end
	end
	return false
end

function JazzImpPatchPersonalPerksLayout()
	local xt = rawget(_G, "XTemplates") and XTemplates.PDAImpResultMerc
	if not xt then
		return
	end
	-- Undo a prior HWrap mistake if still present on personal row.
	local function undo_hwrap(node, depth)
		if type(node) ~= "table" or (depth or 0) > 48 then
			return false
		end
		if node.LayoutMethod == "HWrap" and (node.LayoutHSpacing == 20 or node.LayoutHSpacing == 12) then
			-- Only revert if this looks like the personal host (has personal ForEach child).
			for _, v in ipairs(node) do
				if type(v) == "table" and v.comment == "personal perks" then
					node.LayoutMethod = "HList"
					node.LayoutHSpacing = 12
					return true
				end
			end
		end
		for _, v in ipairs(node) do
			if type(v) == "table" and undo_hwrap(v, (depth or 0) + 1) then
				return true
			end
		end
		for k, v in pairs(node) do
			if type(k) ~= "number" and type(v) == "table" and undo_hwrap(v, (depth or 0) + 1) then
				return true
			end
		end
		return false
	end
	undo_hwrap(xt, 0)
	JazzImpWalkPatchPersonalHList(xt, 0)
	JazzImpWalkPatchTacticalGrid(xt, 0)
	rawset(_G, "g_JAZZ_ImpPerksLayoutPatched", true)
end

function JazzImpInstallAll()
	JazzImpInstallPersonalPerksWrap()
	JazzImpInstallCalcAnswersWrap()
	JazzImpInstallDialogueConditionWraps()
	JazzImpPatchPersonalPerksLayout()
	if g_ImpTest and g_ImpTest.final and g_ImpTest.final.perks then
		JazzSanitizeImpPerks(g_ImpTest.final.perks)
	end
	if g_ImpTest and g_ImpTest.result and g_ImpTest.result.perks then
		JazzSanitizeImpPerks(g_ImpTest.result.perks)
	end
end

function OnMsg.ClassesBuilt()
	JazzImpInstallAll()
end

function OnMsg.DataLoaded()
	JazzImpPatchPersonalPerksLayout()
end

function OnMsg.ModsReloaded()
	JazzImpInstallAll()
end

JazzImpInstallAll()
