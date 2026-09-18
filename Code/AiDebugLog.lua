-- JAZZ-AI-DBG-001: final AI dest / attack lines in CombatLog (Snype) when AIDebugLog is on.

function JazzAI_DebugLogEnabled()
	local opts = rawget(_G, "CurrentModOptions")
	return opts and opts.AIDebugLog == true
end

function JazzAI_DebugStampAbort(context, reason)
	if context and reason then
		context.jazz_dbg_abort = reason
	end
end

local function lIsRu()
	local fn = rawget(_G, "GetLanguage")
	if type(fn) == "function" then
		local lang = fn()
		return lang == "Russian" or lang == "ru" or lang == "Ru"
	end
	return true
end

local function lSay(text)
	if not JazzAI_DebugLogEnabled() then
		return
	end
	if type(text) ~= "string" or text == "" then
		return
	end
	local clog = rawget(_G, "CombatLog")
	local untr = rawget(_G, "Untranslated")
	if type(clog) ~= "function" or type(untr) ~= "function" then
		return
	end
	clog("short", untr(text))
end

local function lAp(ap)
	local scale = (const.Scale and const.Scale.AP) or 1000
	return DivRound(tonumber(ap) or 0, scale)
end

local function lName(obj)
	if not obj then
		return "?"
	end
	local label = obj.Nick or obj.Name
	local tr = rawget(_G, "_InternalTranslate")
	if label and type(tr) == "function" then
		local ok, text = pcall(tr, label)
		if ok and type(text) == "string" and text ~= "" then
			return text
		end
	end
	return obj.unitdatadef_id or obj.class or "?"
end

local function lCth(value)
	if type(value) ~= "number" then
		return false
	end
	return tostring(floatfloor(value + 0.5))
end

local function lRole(unit)
	local infer = rawget(_G, "JazzAI_UnitRoleFamily")
	if type(infer) == "function" then
		local family = infer(unit)
		if type(family) == "string" and family ~= "" then
			return family
		end
	end
	local arch = unit and (unit.current_archetype or unit.archetype)
	if type(arch) == "table" then
		arch = arch.id
	end
	if type(arch) == "string" and arch ~= "" then
		return arch
	end
	return "-"
end

local function lDirective(unit, context)
	local getter = rawget(_G, "JazzAI_GetTeamDirective")
	if type(getter) == "function" then
		local dir = getter(unit)
		if type(dir) == "string" and dir ~= "" then
			return dir
		end
	end
	if context and type(context.jazz_directive) == "string" and context.jazz_directive ~= "" then
		return context.jazz_directive
	end
	return "-"
end

local function lStayPos(unit, context)
	if context and context.unit_stance_pos then
		return context.unit_stance_pos
	end
	if unit and type(GetPackedPosAndStance) == "function" then
		return GetPackedPosAndStance(unit)
	end
	return false
end

local function lTiles(from, dest)
	if not from or not dest or type(stance_pos_dist) ~= "function" then
		return 0
	end
	local scale = const.SlabSizeX or 1
	return DivRound(stance_pos_dist(from, dest), scale)
end

local function lDestWhy(unit, context, dest, stay, why_override)
	if type(why_override) == "string" and why_override ~= "" then
		return why_override
	end
	if context and context.jazz_stay_shot then
		return "stay-shot"
	end
	if context and context.jazz_break_los_ow_anchor then
		return "peel-OW"
	end
	local perch = rawget(_G, "JazzAI_ContextStayIsEgressPerch")
	if dest == stay and type(perch) == "function" and perch(context) then
		return "perch"
	end
	local hold = rawget(_G, "JazzAI_UnitHasSniperHoldKeyword")
	local targets = context and context.dest_target or empty_table
	if dest == stay and type(hold) == "function" and hold(unit) and targets[stay] then
		return "hold"
	end
	if context and context.can_heal then
		return "medic"
	end
	if dest and targets[dest] then
		return "to-shot"
	end
	if dest == stay then
		return "stay"
	end
	return "reposition"
end

local function lTargetBit(context, dest, target, cth)
	local tgt = target
	if not tgt and context and dest then
		tgt = (context.dest_target or empty_table)[dest]
	end
	if not tgt then
		return ""
	end
	local pct = cth
	if not pct and context and dest then
		pct = (context.dest_cth or empty_table)[dest]
	end
	local cth_s = lCth(pct)
	if lIsRu() then
		if cth_s then
			return " · цель " .. lName(tgt) .. " " .. cth_s .. "%"
		end
		return " · цель " .. lName(tgt)
	end
	if cth_s then
		return " · tgt " .. lName(tgt) .. " " .. cth_s .. "%"
	end
	return " · tgt " .. lName(tgt)
end

function JazzAI_DebugLogDest(unit, context, why_override)
	if not JazzAI_DebugLogEnabled() or not unit then
		return
	end
	context = context or unit.ai_context
	if not context then
		return
	end
	local dest = context.ai_destination or lStayPos(unit, context)
	local stay = lStayPos(unit, context)
	local tiles = lTiles(stay, dest)
	local why = lDestWhy(unit, context, dest, stay, why_override)
	local ap_now = lAp(unit.ActionPoints)
	local dest_ap = context.dest_ap and dest and context.dest_ap[dest]
	local ap_left = dest_ap and lAp(dest_ap) or ap_now
	local move
	if dest == stay or tiles <= 0 then
		move = lIsRu() and ("стоит " .. why) or ("stay " .. why)
	else
		move = lIsRu() and ("ход " .. tiles .. "т " .. why) or ("move " .. tiles .. "t " .. why)
	end
	local prefix = lIsRu() and "[ИИ] " or "[AI] "
	lSay(prefix .. lName(unit) .. " · " .. lRole(unit) .. "/" .. lDirective(unit, context)
		.. " · " .. move .. " · " .. (lIsRu() and "ОД " or "AP ") .. ap_now .. "→" .. ap_left
		.. lTargetBit(context, dest, nil, nil))
end

function JazzAI_DebugLogAttack(unit, context, info)
	if not JazzAI_DebugLogEnabled() or not unit then
		return
	end
	info = info or empty_table
	context = context or unit.ai_context or empty_table
	local action = info.action
	local action_id = info.id
	if not action_id and type(action) == "table" then
		action_id = action.id or action.class or action.BiasId
	end
	if type(action) == "string" then
		action_id = action
	end
	action_id = action_id or "?"
	local dest = info.dest or context.ai_destination
	local target = info.target
	local cth = info.cth
	if not cth and dest then
		cth = (context.dest_cth or empty_table)[dest]
	end
	local aim = info.aim
	local leftover_ap = info.leftover
	if leftover_ap == nil then
		leftover_ap = unit.ActionPoints
		if type(info.cost) == "number" then
			leftover_ap = Max(0, leftover_ap - info.cost)
		end
	end
	local leftover = lAp(leftover_ap)
	local bit = action_id
	if type(aim) == "number" then
		bit = bit .. (lIsRu() and (" приц" .. tostring(aim)) or (" aim" .. tostring(aim)))
	end
	local prefix = lIsRu() and "[ИИ] " or "[AI] "
	local left = lIsRu() and " · остаток " or " · left "
	lSay(prefix .. lName(unit) .. " · " .. bit .. lTargetBit(context, dest, target, cth) .. left .. leftover)
end

function JazzAI_DebugLogAbort(unit, context, did_attack)
	if did_attack or not JazzAI_DebugLogEnabled() or not unit then
		return
	end
	context = context or unit.ai_context
	local reason = context and context.jazz_dbg_abort
	if type(reason) ~= "string" or reason == "" then
		return
	end
	local prefix = lIsRu() and "[ИИ] " or "[AI] "
	local left = lIsRu() and "нет выстрела · остаток " or "no shot · left "
	lSay(prefix .. lName(unit) .. " · " .. left .. lAp(unit.ActionPoints) .. " · " .. reason)
end
