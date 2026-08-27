-- JAZZ-AI-BARK-001: floating combat barks over visible enemy AI.
-- After-decision only. Does not change scores, dest, AP, or directives.

MapVar("JazzAI_CombatBarks", false)

-- Grenade Execute bark lives in AiActions.lua (single wrap). Stale flags from
-- the old second wrap must not survive ReloadLua or they look "still installed".
if rawget(_G, "g_JAZZ_AIActionThrowGrenadeExecuteWrapped") then
	rawset(_G, "g_JAZZ_AIActionThrowGrenadeExecuteWrapped", false)
end
if rawget(_G, "g_JAZZ_AIActionThrowGrenadeExecuteBase") then
	rawset(_G, "g_JAZZ_AIActionThrowGrenadeExecuteBase", false)
end
g_JAZZ_UnitSwapActiveWeaponWrapped = rawget(_G, "g_JAZZ_UnitSwapActiveWeaponWrapped") or false
g_JAZZ_UnitSwapActiveWeaponBase = rawget(_G, "g_JAZZ_UnitSwapActiveWeaponBase") or false

local DIR_EVENT = {
	HoldLine = "order_hold",
	Push = "order_push",
	Envelop = "order_envelop",
	FallBack = "order_fallback",
	FocusFire = "order_focus",
	OccupyBuildings = "order_buildings",
	OccupyHeights = "order_heights",
	TakeCover = "order_cover",
	LowVisHold = "order_lowvis",
	GoHidden = "order_hidden",
}

local ARCH_EVENT = {
	Panicked = "arch_panic",
	Deserter = "arch_desert",
	Berserk = "arch_berserk",
	Medic = "arch_medic",
	Medic_Low = "arch_medic",
	Melee = "arch_melee",
}

local WPN_EVENT = {
	rifle = "wpn_rifle",
	shotgun = "wpn_shotgun",
	mg = "wpn_mg",
	sidearm = "wpn_sidearm",
	gl = "wpn_gl",
	rocket = "wpn_rocket",
	sniper = "wpn_sniper",
	melee = "wpn_melee",
}

local function JazzAI_BarkNewState()
	return {
		turn = false,
		teams = {},
		unit_act = {},
		once = {},
		last_wpn = {},
	}
end

local function JazzAI_BarkEnsure()
	if type(JazzAI_CombatBarks) ~= "table" then
		JazzAI_CombatBarks = JazzAI_BarkNewState()
	end
	return JazzAI_CombatBarks
end

local function JazzAI_BarkTeamKey(unit)
	local team = unit and unit.team
	if not team then
		return false
	end
	return team.side or team.handle or tostring(team)
end

local function JazzAI_BarkIsEnemy(unit)
	if not IsValid(unit) or unit:IsDead() then
		return false
	end
	if unit:HasStatusEffect("Unconscious") then
		return false
	end
	local team = unit.team
	if not team or team.player_team or team.player_ally then
		return false
	end
	return not not team.player_enemy
end

local function JazzAI_BarkVisible(unit)
	local pov = GetPoVTeam and GetPoVTeam()
	if not pov and GetCameraPOVTeam then
		pov = GetCameraPOVTeam()
	end
	if not pov or not HasVisibilityTo then
		return false
	end
	return not not HasVisibilityTo(pov, unit)
end

local function JazzAI_BarkFast()
	return rawget(_G, "g_FastForwardSpeed") == "Fast"
end

local function JazzAI_BarkResetTurn(st)
	local turn = g_Combat and g_Combat.current_turn
	if st.turn ~= turn then
		st.turn = turn
		st.teams = {}
		st.unit_act = {}
	end
end

local function JazzAI_BarkVoice(unit, event)
	if type(event) == "string" and string.sub(event, 1, 6) == "order_" then
		local r = JazzAI_OfficerAuraRadius and JazzAI_OfficerAuraRadius(unit) or 0
		if r == 15 then
			return "boss"
		end
		return "officer"
	end
	local id = tostring(unit.unitdatadef_id or "")
	if string.find(id, "_T1_", 1, true) then
		return "t1"
	end
	if string.find(id, "_T4_", 1, true) then
		return "t4"
	end
	return "t2"
end

function JazzAI_BarkWeaponClass(weapon)
	if not weapon then
		return false
	end
	if IsKindOf(weapon, "MeleeWeapon") then
		return "melee"
	end
	if IsKindOf(weapon, "GrenadeLauncher") then
		return "gl"
	end
	if IsKindOf(weapon, "MachineGun") or IsKindOf(weapon, "LightMachineGun") then
		return "mg"
	end
	if IsKindOf(weapon, "SniperRifle") then
		return "sniper"
	end
	if IsKindOf(weapon, "Shotgun") then
		return "shotgun"
	end
	if IsKindOf(weapon, "Pistol") or IsKindOf(weapon, "Revolver") then
		return "sidearm"
	end
	if IsKindOf(weapon, "RocketLauncher") or IsKindOf(weapon, "HeavyWeapon") then
		return "rocket"
	end
	if IsKindOf(weapon, "Firearm") then
		return "rifle"
	end
	return false
end

local function JazzAI_BarkActiveClass(unit)
	if not unit or not unit.GetActiveWeapons then
		return false
	end
	return JazzAI_BarkWeaponClass(unit:GetActiveWeapons())
end

local function JazzAI_BarkName(obj)
	if not obj then
		return false
	end
	if type(obj.Nick) == "string" and obj.Nick ~= "" then
		return obj.Nick
	end
	if obj.GetDisplayName then
		return obj:GetDisplayName()
	end
	return false
end

local function JazzAI_BarkFacts(unit, ctx)
	ctx = ctx or empty_table
	local target = ctx.target
	local pos = ctx.pos
	local indoor = false
	if IsValid(target) then
		indoor = not not target.indoors
	elseif pos and AICheckIndoors then
		local ok, v = pcall(AICheckIndoors, pos)
		indoor = ok and not not v
	else
		indoor = not not unit.indoors
	end
	local speaker_in = not not unit.indoors
	local high = false
	local tz
	if IsValid(target) and target.GetPos then
		local tp = target:GetPos()
		tz = tp and tp:z()
	elseif IsPoint(pos) then
		tz = pos:z()
	elseif pos and stance_pos_unpack then
		local _x, _y, z = stance_pos_unpack(pos)
		tz = z
	end
	local sp = unit:GetPos()
	if sp and tz and (sp:z() or 0) > tz then
		high = true
	end
	local houses = JazzAI_ShouldOccupyBuildings and not not JazzAI_ShouldOccupyBuildings(unit)
	return {
		["in"] = indoor,
		out = not indoor,
		into = (not speaker_in) and indoor,
		high = high,
		houses = houses,
	}
end

local function JazzAI_BarkLineOk(line, facts)
	local tags = line.tags
	if type(tags) ~= "table" then
		return true
	end
	for _, tag in ipairs(tags) do
		if not facts[tag] then
			return false
		end
	end
	return true
end

local function JazzAI_BarkPick(unit, event, ctx)
	local slot = JazzAI_CombatBarkBank and JazzAI_CombatBarkBank[event]
	if not slot then
		return false
	end
	local lines = slot[JazzAI_BarkVoice(unit, event)]
	if not lines or #lines == 0 then
		return false
	end
	local facts = JazzAI_BarkFacts(unit, ctx)
	local pool = {}
	for _, line in ipairs(lines) do
		if JazzAI_BarkLineOk(line, facts) then
			pool[#pool + 1] = line
		end
	end
	if #pool == 0 then
		return false
	end
	local n = #pool
	local r = unit:Random(n)
	if type(r) ~= "number" then
		r = 0
	end
	return pool[(r % n) + 1]
end

local function JazzAI_BarkText(line, ctx)
	local en = line.en
	if ctx and ctx.name and string.find(en, "<name>", 1, true) then
		return T{ line.id, en, name = ctx.name }
	end
	return T(line.id, en)
end

function JazzAI_TryCombatBark(unit, event, ctx)
	if not event or not JazzAI_BarkIsEnemy(unit) then
		return false
	end
	if JazzAI_BarkFast() or not JazzAI_BarkVisible(unit) then
		return false
	end
	local st = JazzAI_BarkEnsure()
	JazzAI_BarkResetTurn(st)
	local handle = unit.handle or tostring(unit)
	local tkey = JazzAI_BarkTeamKey(unit)
	if not tkey then
		return false
	end
	if st.unit_act[handle] then
		return false
	end
	local team = st.teams[tkey]
	if not team then
		team = { count = 0, events = {} }
		st.teams[tkey] = team
	end
	if team.count >= 2 or team.events[event] then
		return false
	end
	local line = JazzAI_BarkPick(unit, event, ctx)
	if not line then
		return false
	end
	CreateFloatingText(unit, JazzAI_BarkText(line, ctx))
	st.unit_act[handle] = true
	team.count = team.count + 1
	team.events[event] = true
	return true
end

function JazzAI_BarkOnDirective(unit, prev, directive, entry)
	if not directive or prev == directive then
		return false
	end
	local event = DIR_EVENT[directive]
	if not event then
		return false
	end
	local ctx = {}
	if directive == "FocusFire" then
		local tgt = entry and entry.focus_target
		local name = JazzAI_BarkName(tgt)
		if name then
			ctx.name = name
			ctx.target = tgt
		else
			event = "order_focus_anon"
		end
	end
	return JazzAI_TryCombatBark(unit, event, ctx)
end

function JazzAI_BarkOnArchetype(unit, archetype)
	local event = ARCH_EVENT[archetype]
	if not event then
		return false
	end
	local st = JazzAI_BarkEnsure()
	local handle = unit.handle or tostring(unit)
	local once = st.once[handle] or {}
	if once[event] then
		return false
	end
	local ok = JazzAI_TryCombatBark(unit, event, empty_table)
	if ok then
		once[event] = true
		st.once[handle] = once
	end
	return ok
end

function JazzAI_BarkOnWeaponSwap(unit, old_class)
	local new_class = JazzAI_BarkActiveClass(unit)
	local st = JazzAI_BarkEnsure()
	local handle = unit.handle or tostring(unit)
	st.last_wpn[handle] = new_class or false
	if not old_class or not new_class or old_class == new_class then
		return false
	end
	local event = WPN_EVENT[new_class]
	if not event then
		return false
	end
	return JazzAI_TryCombatBark(unit, event, empty_table)
end

local function JazzAI_NadeEvent(grenade)
	if not grenade then
		return false
	end
	if IsKindOf(grenade, "Flare") then
		return "nade_flare"
	end
	local t = grenade.aoeType or "none"
	if t == "smoke" then
		return "nade_smoke"
	end
	if t == "fire" then
		return "nade_fire"
	end
	if t == "teargas" or t == "toxicgas" then
		return "nade_gas"
	end
	return "nade_frag"
end

function JazzAI_BarkOnGrenade(unit, grenade, target_pos)
	local event = JazzAI_NadeEvent(grenade)
	if not event then
		return false
	end
	return JazzAI_TryCombatBark(unit, event, { pos = target_pos })
end

local function JazzAI_DestTiles(unit, dest)
	if not dest then
		return 0
	end
	local context = unit.ai_context
	local from = context and context.unit_stance_pos
	if from and stance_pos_dist and const.SlabSizeX then
		local dist = stance_pos_dist(from, dest)
		if type(dist) == "number" then
			return DivRound(dist, const.SlabSizeX)
		end
	end
	if not stance_pos_unpack then
		return 0
	end
	local x, y = stance_pos_unpack(dest)
	local pos = unit:GetPos()
	if not pos or not x then
		return 0
	end
	return DivRound(pos:Dist2D(point(x, y)), const.SlabSizeX)
end

function JazzAI_BarkTryDest(unit)
	if not JazzAI_BarkIsEnemy(unit) then
		return false
	end
	local context = unit.ai_context
	local dest = context and context.best_dest
	if not dest then
		return false
	end
	local tiles = JazzAI_DestTiles(unit, dest)
	local directive = JazzAI_GetTeamDirective and JazzAI_GetTeamDirective(unit)
	if directive == "FallBack" then
		return false
	end
	local slot = JazzAI_GetUnitActSlot and JazzAI_GetUnitActSlot(unit)
	local kind = slot and slot.kind
	local probe = JazzAI_UnitIsRecontactProbe and JazzAI_UnitIsRecontactProbe(unit)
	if (kind == "press" or directive == "Push") and tiles >= 6 then
		return JazzAI_TryCombatBark(unit, "seq_press", { pos = dest })
	end
	if (directive == "Envelop" or probe) and tiles >= 6 then
		return JazzAI_TryCombatBark(unit, "seq_flank", { pos = dest })
	end
	if tiles >= 12 then
		return JazzAI_TryCombatBark(unit, "move_long", { pos = dest })
	end
	return false
end

local function JazzAI_InstallBarkWrappers()
	-- nade_* barks: JazzAI_BarkOnGrenade from AiActions Execute wrap only.
	local unit_cls = rawget(_G, "Unit")
	if type(unit_cls) == "table" and type(unit_cls.SwapActiveWeapon) == "function"
		and not rawget(_G, "g_JAZZ_UnitSwapActiveWeaponWrapped")
	then
		rawset(_G, "g_JAZZ_UnitSwapActiveWeaponBase", unit_cls.SwapActiveWeapon)
		rawset(_G, "g_JAZZ_UnitSwapActiveWeaponWrapped", true)
		function Unit:SwapActiveWeapon(...)
			local reason = select(1, ...)
			local oldc = JazzAI_BarkActiveClass(self)
			local res = g_JAZZ_UnitSwapActiveWeaponBase(self, ...)
			if reason == "AIEquipWeapon" then
				local st = JazzAI_BarkEnsure()
				local handle = self.handle or tostring(self)
				st.last_wpn[handle] = JazzAI_BarkActiveClass(self) or false
			else
				JazzAI_BarkOnWeaponSwap(self, oldc)
			end
			return res
		end
	end
end

function OnMsg.CombatStart()
	JazzAI_CombatBarks = JazzAI_BarkNewState()
end

function OnMsg.CombatEnd()
	JazzAI_CombatBarks = false
end

JazzAI_InstallBarkWrappers()

function OnMsg.ModsReloaded()
	JazzAI_InstallBarkWrappers()
end

function OnMsg.ClassesBuilt()
	JazzAI_InstallBarkWrappers()
end

-- JAZZ-AI-BARK-BANK-BEGIN
-- Generated by docs/tools/_emit_aibark_runtime.py. Do not edit by hand.
JazzAI_CombatBarkBank = {
	["order_hold"] = {
		["boss"] = {
			{ id = 890000000020157, en = "Stay put! Don't push!", tags = {  } },
			{ id = 890000000020158, en = "Nobody moves!", tags = {  } },
			{ id = 890000000020159, en = "Yard's ours. Sit.", tags = { "out" } },
			{ id = 890000000020160, en = "Don't go in yet", tags = {  } },
			{ id = 890000000020161, en = "Let them come to us", tags = {  } },
		},
		["officer"] = {
			{ id = 890000000020162, en = "Hold.", tags = {  } },
			{ id = 890000000020163, en = "Don't go in.", tags = {  } },
			{ id = 890000000020164, en = "Here.", tags = {  } },
			{ id = 890000000020165, en = "We wait.", tags = {  } },
			{ id = 890000000020166, en = "Sit tight.", tags = {  } },
		},
	},
	["order_push"] = {
		["boss"] = {
			{ id = 890000000020167, en = "Move, you dogs!", tags = {  } },
			{ id = 890000000020168, en = "Hit 'em already!", tags = {  } },
			{ id = 890000000020169, en = "We go at them!", tags = {  } },
			{ id = 890000000020170, en = "Don't stand. Hit!", tags = {  } },
			{ id = 890000000020171, en = "Hit them while they're up!", tags = {  } },
		},
		["officer"] = {
			{ id = 890000000020172, en = "I said move.", tags = {  } },
			{ id = 890000000020173, en = "Now. Into them.", tags = {  } },
			{ id = 890000000020174, en = "We go.", tags = {  } },
			{ id = 890000000020175, en = "On them. Now.", tags = {  } },
			{ id = 890000000020176, en = "Don't wait.", tags = {  } },
		},
	},
	["order_envelop"] = {
		["boss"] = {
			{ id = 890000000020177, en = "Around back, not the front!", tags = {  } },
			{ id = 890000000020178, en = "Through the yards!", tags = { "out" } },
			{ id = 890000000020179, en = "Come in from the sides!", tags = {  } },
			{ id = 890000000020180, en = "Not the street. Behind!", tags = { "out" } },
			{ id = 890000000020181, en = "Around the houses!", tags = { "houses" } },
		},
		["officer"] = {
			{ id = 890000000020182, en = "Around back.", tags = {  } },
			{ id = 890000000020183, en = "Not in a bunch.", tags = {  } },
			{ id = 890000000020184, en = "From the edge.", tags = {  } },
			{ id = 890000000020185, en = "Go around.", tags = {  } },
			{ id = 890000000020186, en = "Not straight in.", tags = {  } },
		},
	},
	["order_fallback"] = {
		["boss"] = {
			{ id = 890000000020187, en = "Get back!", tags = {  } },
			{ id = 890000000020188, en = "Down or you're next!", tags = {  } },
			{ id = 890000000020189, en = "We're pulling out!", tags = {  } },
			{ id = 890000000020190, en = "Back, if you're whole!", tags = {  } },
			{ id = 890000000020191, en = "We need you alive!", tags = {  } },
		},
		["officer"] = {
			{ id = 890000000020192, en = "We're out.", tags = {  } },
			{ id = 890000000020193, en = "Back. Alive.", tags = {  } },
			{ id = 890000000020194, en = "Leaving.", tags = {  } },
			{ id = 890000000020195, en = "Back.", tags = {  } },
			{ id = 890000000020196, en = "Enough.", tags = {  } },
		},
	},
	["order_focus"] = {
		["boss"] = {
			{ id = 890000000020197, en = "All of you — <name>!", tags = {  } },
			{ id = 890000000020198, en = "<name>. Nobody else.", tags = {  } },
			{ id = 890000000020199, en = "On <name>. Shoot!", tags = {  } },
			{ id = 890000000020200, en = "Drop <name>!", tags = {  } },
			{ id = 890000000020201, en = "Only <name>, I said!", tags = {  } },
		},
		["officer"] = {
			{ id = 890000000020202, en = "<name>. Everyone.", tags = {  } },
			{ id = 890000000020203, en = "Only <name>.", tags = {  } },
			{ id = 890000000020204, en = "<name>.", tags = {  } },
			{ id = 890000000020205, en = "Fire. <name>.", tags = {  } },
			{ id = 890000000020206, en = "<name>. Drop him.", tags = {  } },
		},
	},
	["order_focus_anon"] = {
		["boss"] = {
			{ id = 890000000020207, en = "That one. Hit him!", tags = {  } },
			{ id = 890000000020208, en = "Stop spraying!", tags = {  } },
			{ id = 890000000020209, en = "One man. All of you!", tags = {  } },
			{ id = 890000000020210, en = "This one. Only this!", tags = {  } },
			{ id = 890000000020211, en = "Don't spray. One!", tags = {  } },
		},
		["officer"] = {
			{ id = 890000000020212, en = "That one. All of you.", tags = {  } },
			{ id = 890000000020213, en = "Don't split it.", tags = {  } },
			{ id = 890000000020214, en = "One of them.", tags = {  } },
			{ id = 890000000020215, en = "This one.", tags = {  } },
			{ id = 890000000020216, en = "Don't spray.", tags = {  } },
		},
	},
	["order_buildings"] = {
		["boss"] = {
			{ id = 890000000020217, en = "Inside! Windows!", tags = {  } },
			{ id = 890000000020218, en = "Off the yard. Inside!", tags = {  } },
			{ id = 890000000020219, en = "Into the houses!", tags = {  } },
			{ id = 890000000020220, en = "From the windows!", tags = {  } },
			{ id = 890000000020221, en = "Not the yard. Inside!", tags = {  } },
		},
		["officer"] = {
			{ id = 890000000020222, en = "Inside.", tags = {  } },
			{ id = 890000000020223, en = "From the windows.", tags = {  } },
			{ id = 890000000020224, en = "Indoors.", tags = {  } },
			{ id = 890000000020225, en = "Off the yard.", tags = {  } },
			{ id = 890000000020226, en = "Windows.", tags = {  } },
		},
	},
	["order_heights"] = {
		["boss"] = {
			{ id = 890000000020227, en = "Up the roof!", tags = {  } },
			{ id = 890000000020228, en = "Drop them from up there!", tags = {  } },
			{ id = 890000000020229, en = "Up the hill!", tags = {  } },
			{ id = 890000000020230, en = "Roofs are ours!", tags = {  } },
			{ id = 890000000020231, en = "Up, come on!", tags = {  } },
		},
		["officer"] = {
			{ id = 890000000020232, en = "Up.", tags = {  } },
			{ id = 890000000020233, en = "From the hill.", tags = {  } },
			{ id = 890000000020234, en = "Roofs.", tags = {  } },
			{ id = 890000000020235, en = "Higher.", tags = {  } },
			{ id = 890000000020236, en = "From above.", tags = {  } },
		},
	},
	["order_cover"] = {
		["boss"] = {
			{ id = 890000000020237, en = "Belly down!", tags = {  } },
			{ id = 890000000020238, en = "Down, bullets flying!", tags = {  } },
			{ id = 890000000020239, en = "To the dirt!", tags = {  } },
			{ id = 890000000020240, en = "Get behind!", tags = {  } },
			{ id = 890000000020241, en = "Heads down!", tags = {  } },
		},
		["officer"] = {
			{ id = 890000000020242, en = "Down.", tags = {  } },
			{ id = 890000000020243, en = "Don't pop up.", tags = {  } },
			{ id = 890000000020244, en = "To the dirt.", tags = {  } },
			{ id = 890000000020245, en = "Get down.", tags = {  } },
			{ id = 890000000020246, en = "Don't show.", tags = {  } },
		},
	},
	["order_lowvis"] = {
		["boss"] = {
			{ id = 890000000020247, en = "Don't walk into that dark!", tags = {  } },
			{ id = 890000000020248, en = "Stay. Let 'em show.", tags = {  } },
			{ id = 890000000020249, en = "Not into the black!", tags = {  } },
			{ id = 890000000020250, en = "Wait. Let them show.", tags = {  } },
			{ id = 890000000020251, en = "Quiet. We stay.", tags = {  } },
		},
		["officer"] = {
			{ id = 890000000020252, en = "Stay put.", tags = {  } },
			{ id = 890000000020253, en = "No heroes.", tags = {  } },
			{ id = 890000000020254, en = "Wait for light.", tags = {  } },
			{ id = 890000000020255, en = "Don't go in.", tags = {  } },
			{ id = 890000000020256, en = "Quiet.", tags = {  } },
		},
	},
	["order_hidden"] = {
		["boss"] = {
			{ id = 890000000020257, en = "Into the dark. Quiet!", tags = {  } },
			{ id = 890000000020258, en = "Stay hidden!", tags = {  } },
			{ id = 890000000020259, en = "Don't show yourselves!", tags = {  } },
			{ id = 890000000020260, en = "In the grass. Down!", tags = { "out" } },
			{ id = 890000000020261, en = "Shh. Vanish.", tags = {  } },
		},
		["officer"] = {
			{ id = 890000000020262, en = "Into cover.", tags = {  } },
			{ id = 890000000020263, en = "Quiet.", tags = {  } },
			{ id = 890000000020264, en = "Don't show.", tags = {  } },
			{ id = 890000000020265, en = "Stay hidden.", tags = {  } },
			{ id = 890000000020266, en = "Vanish.", tags = {  } },
		},
	},
	["arch_panic"] = {
		["t1"] = {
			{ id = 890000000020267, en = "Please—", tags = {  } },
			{ id = 890000000020268, en = "I wanna go home", tags = {  } },
			{ id = 890000000020269, en = "Mama—", tags = {  } },
			{ id = 890000000020270, en = "Don't shoot—", tags = {  } },
			{ id = 890000000020271, en = "I don't want this", tags = {  } },
		},
		["t2"] = {
			{ id = 890000000020272, en = "They'll walk over us!", tags = {  } },
			{ id = 890000000020273, en = "We're not staying. Go!", tags = {  } },
			{ id = 890000000020274, en = "This is a butcher shop", tags = {  } },
			{ id = 890000000020275, en = "They'll drop us", tags = {  } },
			{ id = 890000000020276, en = "Time to go", tags = {  } },
		},
		["t4"] = {
			{ id = 890000000020277, en = "Damn it—", tags = {  } },
			{ id = 890000000020278, en = "Not now", tags = {  } },
			{ id = 890000000020279, en = "Bad", tags = {  } },
			{ id = 890000000020280, en = "Not here", tags = {  } },
			{ id = 890000000020281, en = "Enough", tags = {  } },
		},
	},
	["arch_desert"] = {
		["t1"] = {
			{ id = 890000000020282, en = "I wanna live", tags = {  } },
			{ id = 890000000020283, en = "Fight it yourselves", tags = {  } },
			{ id = 890000000020284, en = "I'm taking off", tags = {  } },
			{ id = 890000000020285, en = "I still wanna live", tags = {  } },
			{ id = 890000000020286, en = "I've seen enough blood", tags = {  } },
		},
		["t2"] = {
			{ id = 890000000020287, en = "I'm through", tags = {  } },
			{ id = 890000000020288, en = "I've done my share", tags = {  } },
			{ id = 890000000020289, en = "Find someone else", tags = {  } },
			{ id = 890000000020290, en = "I'm leaving", tags = {  } },
			{ id = 890000000020291, en = "You go on without me", tags = {  } },
		},
		["t4"] = {
			{ id = 890000000020292, en = "Find another fool", tags = {  } },
			{ id = 890000000020293, en = "Nothing left for me here", tags = {  } },
			{ id = 890000000020294, en = "Job's done", tags = {  } },
			{ id = 890000000020295, en = "I'm out", tags = {  } },
			{ id = 890000000020296, en = "Not my fight", tags = {  } },
		},
	},
	["arch_berserk"] = {
		["t1"] = {
			{ id = 890000000020297, en = "I'll kill you!", tags = {  } },
			{ id = 890000000020298, en = "Aaah! Come here!", tags = {  } },
			{ id = 890000000020299, en = "I'll tear you all!", tags = {  } },
			{ id = 890000000020300, en = "Blood! More!", tags = {  } },
			{ id = 890000000020301, en = "Can't stop me!", tags = {  } },
		},
		["t2"] = {
			{ id = 890000000020302, en = "I'll drop you all!", tags = {  } },
			{ id = 890000000020303, en = "Stop hiding!", tags = {  } },
			{ id = 890000000020304, en = "Coming for you!", tags = {  } },
			{ id = 890000000020305, en = "Cut them down!", tags = {  } },
			{ id = 890000000020306, en = "Nobody lives!", tags = {  } },
		},
		["t4"] = {
			{ id = 890000000020307, en = "All of you.", tags = {  } },
			{ id = 890000000020308, en = "Coming.", tags = {  } },
			{ id = 890000000020309, en = "I'll finish it.", tags = {  } },
			{ id = 890000000020310, en = "Enough waiting.", tags = {  } },
			{ id = 890000000020311, en = "Forward.", tags = {  } },
		},
	},
	["arch_medic"] = {
		["t1"] = {
			{ id = 890000000020312, en = "Easy", tags = {  } },
			{ id = 890000000020313, en = "I'll stop the blood", tags = {  } },
			{ id = 890000000020314, en = "I'll bind it", tags = {  } },
			{ id = 890000000020315, en = "Don't jerk. You're alive", tags = {  } },
			{ id = 890000000020316, en = "Stay down. I'm here", tags = {  } },
		},
		["t2"] = {
			{ id = 890000000020317, en = "Don't jerk", tags = {  } },
			{ id = 890000000020318, en = "Shut up and you'll live", tags = {  } },
			{ id = 890000000020319, en = "Binding. Don't yell", tags = {  } },
			{ id = 890000000020320, en = "You'll live", tags = {  } },
			{ id = 890000000020321, en = "Hold on. I'll close it", tags = {  } },
		},
		["t4"] = {
			{ id = 890000000020322, en = "Lie still.", tags = {  } },
			{ id = 890000000020323, en = "Don't get in the way.", tags = {  } },
			{ id = 890000000020324, en = "Quiet.", tags = {  } },
			{ id = 890000000020325, en = "Alive. Stay down.", tags = {  } },
			{ id = 890000000020326, en = "Hands.", tags = {  } },
		},
	},
	["arch_melee"] = {
		["t1"] = {
			{ id = 890000000020327, en = "I'll cut you!", tags = {  } },
			{ id = 890000000020328, en = "Closer—", tags = {  } },
			{ id = 890000000020329, en = "Knife, knife!", tags = {  } },
			{ id = 890000000020330, en = "I'm coming in!", tags = {  } },
			{ id = 890000000020331, en = "Save the rounds. Cutting", tags = {  } },
		},
		["t2"] = {
			{ id = 890000000020332, en = "Easier up close", tags = {  } },
			{ id = 890000000020333, en = "On the knife", tags = {  } },
			{ id = 890000000020334, en = "Point blank", tags = {  } },
			{ id = 890000000020335, en = "Enough shooting. Cut", tags = {  } },
			{ id = 890000000020336, en = "Going in close", tags = {  } },
		},
		["t4"] = {
			{ id = 890000000020337, en = "Close in.", tags = {  } },
			{ id = 890000000020338, en = "Enough shooting.", tags = {  } },
			{ id = 890000000020339, en = "Knife.", tags = {  } },
			{ id = 890000000020340, en = "Point blank.", tags = {  } },
			{ id = 890000000020341, en = "Closer.", tags = {  } },
		},
	},
	["nade_flare"] = {
		["t1"] = {
			{ id = 890000000020342, en = "Burn, damn you!", tags = {  } },
			{ id = 890000000020343, en = "Faces into the light!", tags = {  } },
			{ id = 890000000020344, en = "Light, light!", tags = {  } },
			{ id = 890000000020345, en = "Burn in their eyes!", tags = {  } },
			{ id = 890000000020346, en = "So we can see!", tags = {  } },
		},
		["t2"] = {
			{ id = 890000000020347, en = "In their eyes", tags = {  } },
			{ id = 890000000020348, en = "Come out, you bastards", tags = {  } },
			{ id = 890000000020349, en = "Lit them", tags = {  } },
			{ id = 890000000020350, en = "Now we see", tags = {  } },
			{ id = 890000000020351, en = "No more hiding", tags = {  } },
		},
		["t4"] = {
			{ id = 890000000020352, en = "Light.", tags = {  } },
			{ id = 890000000020353, en = "They'll show.", tags = {  } },
			{ id = 890000000020354, en = "Burn.", tags = {  } },
			{ id = 890000000020355, en = "Eyes.", tags = {  } },
			{ id = 890000000020356, en = "I see.", tags = {  } },
		},
	},
	["nade_smoke"] = {
		["t1"] = {
			{ id = 890000000020357, en = "Into the smoke!", tags = {  } },
			{ id = 890000000020358, en = "They won't see", tags = {  } },
			{ id = 890000000020359, en = "We hide in the smoke", tags = {  } },
			{ id = 890000000020360, en = "Hide in the smoke!", tags = {  } },
			{ id = 890000000020361, en = "So they don't see!", tags = {  } },
		},
		["t2"] = {
			{ id = 890000000020362, en = "I'll cover us", tags = {  } },
			{ id = 890000000020363, en = "Through the smoke", tags = {  } },
			{ id = 890000000020364, en = "Cover the yard", tags = { "out" } },
			{ id = 890000000020365, en = "We go under the smoke", tags = {  } },
			{ id = 890000000020366, en = "They can't see. Go", tags = {  } },
		},
		["t4"] = {
			{ id = 890000000020367, en = "Smoke. Then we go.", tags = {  } },
			{ id = 890000000020368, en = "Covered. Go.", tags = {  } },
			{ id = 890000000020369, en = "Smoke.", tags = {  } },
			{ id = 890000000020370, en = "Cover it.", tags = {  } },
			{ id = 890000000020371, en = "We go.", tags = {  } },
		},
	},
	["nade_frag"] = {
		["t1"] = {
			{ id = 890000000020372, en = "Here, you bastards!", tags = {  } },
			{ id = 890000000020373, en = "Catch!", tags = {  } },
			{ id = 890000000020374, en = "That's for you!", tags = {  } },
			{ id = 890000000020375, en = "Catch this!", tags = {  } },
			{ id = 890000000020376, en = "This one's gonna bang!", tags = {  } },
		},
		["t2"] = {
			{ id = 890000000020377, en = "It's in the air!", tags = {  } },
			{ id = 890000000020378, en = "Down — not you", tags = {  } },
			{ id = 890000000020379, en = "At their feet", tags = {  } },
			{ id = 890000000020380, en = "Clearing the yard", tags = { "out" } },
			{ id = 890000000020381, en = "Into the bunch", tags = {  } },
		},
		["t4"] = {
			{ id = 890000000020382, en = "At their feet.", tags = {  } },
			{ id = 890000000020383, en = "For them.", tags = {  } },
			{ id = 890000000020384, en = "There.", tags = {  } },
			{ id = 890000000020385, en = "Clearing.", tags = {  } },
			{ id = 890000000020386, en = "Bang.", tags = {  } },
		},
	},
	["nade_fire"] = {
		["t1"] = {
			{ id = 890000000020387, en = "Burn!", tags = {  } },
			{ id = 890000000020388, en = "Heat for them!", tags = {  } },
			{ id = 890000000020389, en = "I'm torching the house!", tags = { "in" } },
			{ id = 890000000020390, en = "Fire, fire!", tags = {  } },
			{ id = 890000000020391, en = "Let them fry!", tags = {  } },
		},
		["t2"] = {
			{ id = 890000000020392, en = "Torching the yard", tags = { "out" } },
			{ id = 890000000020393, en = "Fire on them!", tags = {  } },
			{ id = 890000000020394, en = "Let them run", tags = {  } },
			{ id = 890000000020395, en = "Lighting the house", tags = { "in" } },
			{ id = 890000000020396, en = "It'll get hot", tags = {  } },
		},
		["t4"] = {
			{ id = 890000000020397, en = "Burn it.", tags = {  } },
			{ id = 890000000020398, en = "Fire.", tags = {  } },
			{ id = 890000000020399, en = "The house.", tags = { "in" } },
			{ id = 890000000020400, en = "Heat.", tags = {  } },
			{ id = 890000000020401, en = "Burn.", tags = {  } },
		},
	},
	["nade_gas"] = {
		["t1"] = {
			{ id = 890000000020402, en = "Let them choke!", tags = {  } },
			{ id = 890000000020403, en = "Filth for them!", tags = {  } },
			{ id = 890000000020404, en = "Cough, you bastards!", tags = {  } },
			{ id = 890000000020405, en = "Breathe that!", tags = {  } },
			{ id = 890000000020406, en = "They'll spit blood!", tags = {  } },
		},
		["t2"] = {
			{ id = 890000000020407, en = "Let them drink it", tags = {  } },
			{ id = 890000000020408, en = "Spoiling the yard", tags = { "out" } },
			{ id = 890000000020409, en = "They don't get air", tags = {  } },
			{ id = 890000000020410, en = "They'll cough themselves out", tags = {  } },
			{ id = 890000000020411, en = "The filth's in the air", tags = {  } },
		},
		["t4"] = {
			{ id = 890000000020412, en = "Breathe.", tags = {  } },
			{ id = 890000000020413, en = "The yard.", tags = { "out" } },
			{ id = 890000000020414, en = "Cough.", tags = {  } },
			{ id = 890000000020415, en = "Filth.", tags = {  } },
			{ id = 890000000020416, en = "That's it.", tags = {  } },
		},
	},
	["wpn_rifle"] = {
		["t1"] = {
			{ id = 890000000020417, en = "Grabbing the long one!", tags = {  } },
			{ id = 890000000020418, en = "Long one in hand!", tags = {  } },
			{ id = 890000000020419, en = "The short one's useless", tags = {  } },
			{ id = 890000000020420, en = "Switching to the far one!", tags = {  } },
			{ id = 890000000020421, en = "Grabbing a gun!", tags = {  } },
		},
		["t2"] = {
			{ id = 890000000020422, en = "Long gun", tags = {  } },
			{ id = 890000000020423, en = "Long one back", tags = {  } },
			{ id = 890000000020424, en = "This one reaches farther", tags = {  } },
			{ id = 890000000020425, en = "Switching guns", tags = {  } },
			{ id = 890000000020426, en = "This one reaches", tags = {  } },
		},
		["t4"] = {
			{ id = 890000000020427, en = "Long one.", tags = {  } },
			{ id = 890000000020428, en = "Farther.", tags = {  } },
			{ id = 890000000020429, en = "Back on.", tags = {  } },
			{ id = 890000000020430, en = "Gun.", tags = {  } },
			{ id = 890000000020431, en = "Taking it.", tags = {  } },
		},
	},
	["wpn_shotgun"] = {
		["t1"] = {
			{ id = 890000000020432, en = "Grabbing buckshot!", tags = {  } },
			{ id = 890000000020433, en = "Grabbing the short mean one!", tags = {  } },
			{ id = 890000000020434, en = "Into the house!", tags = { "into" } },
			{ id = 890000000020435, en = "Switching. Up close!", tags = {  } },
			{ id = 890000000020436, en = "I'll take the door!", tags = { "into" } },
		},
		["t2"] = {
			{ id = 890000000020437, en = "Buckshot", tags = {  } },
			{ id = 890000000020438, en = "Up close now", tags = {  } },
			{ id = 890000000020439, en = "Putting the short one on", tags = {  } },
			{ id = 890000000020440, en = "Into the house", tags = { "into" } },
			{ id = 890000000020441, en = "Better up close", tags = {  } },
		},
		["t4"] = {
			{ id = 890000000020442, en = "Buckshot.", tags = {  } },
			{ id = 890000000020443, en = "Up close.", tags = {  } },
			{ id = 890000000020444, en = "Short one.", tags = {  } },
			{ id = 890000000020445, en = "Into the house.", tags = { "in" } },
			{ id = 890000000020446, en = "Putting it on.", tags = {  } },
		},
	},
	["wpn_mg"] = {
		["t1"] = {
			{ id = 890000000020447, en = "Setting the belt!", tags = {  } },
			{ id = 890000000020448, en = "Belt in hand!", tags = {  } },
			{ id = 890000000020449, en = "Grabbing the long mean one!", tags = {  } },
			{ id = 890000000020450, en = "Switching. Street's mine!", tags = { "out" } },
			{ id = 890000000020451, en = "I'll hold them all!", tags = {  } },
		},
		["t2"] = {
			{ id = 890000000020452, en = "Setting the belt", tags = {  } },
			{ id = 890000000020453, en = "Setting the long one", tags = {  } },
			{ id = 890000000020454, en = "This covers the street", tags = { "out" } },
			{ id = 890000000020455, en = "This holds the yard", tags = { "out" } },
			{ id = 890000000020456, en = "Switching to the long one", tags = {  } },
		},
		["t4"] = {
			{ id = 890000000020457, en = "Belt.", tags = {  } },
			{ id = 890000000020458, en = "The long one.", tags = {  } },
			{ id = 890000000020459, en = "The street.", tags = { "out" } },
			{ id = 890000000020460, en = "The yard's mine.", tags = { "out" } },
			{ id = 890000000020461, en = "Mine.", tags = {  } },
		},
	},
	["wpn_sidearm"] = {
		["t1"] = {
			{ id = 890000000020462, en = "Short one from the pocket!", tags = {  } },
			{ id = 890000000020463, en = "Short one in hand!", tags = {  } },
			{ id = 890000000020464, en = "Long one's jammed—", tags = {  } },
			{ id = 890000000020465, en = "Switching to the quick one!", tags = {  } },
			{ id = 890000000020466, en = "Short one into the house!", tags = { "into" } },
		},
		["t2"] = {
			{ id = 890000000020467, en = "Pulling the short one", tags = {  } },
			{ id = 890000000020468, en = "From the pocket", tags = {  } },
			{ id = 890000000020469, en = "Faster this way", tags = {  } },
			{ id = 890000000020470, en = "Short one up close", tags = {  } },
			{ id = 890000000020471, en = "Long one later", tags = {  } },
		},
		["t4"] = {
			{ id = 890000000020472, en = "Short one.", tags = {  } },
			{ id = 890000000020473, en = "Pocket.", tags = {  } },
			{ id = 890000000020474, en = "Quick.", tags = {  } },
			{ id = 890000000020475, en = "Close.", tags = {  } },
			{ id = 890000000020476, en = "Got it.", tags = {  } },
		},
	},
	["wpn_gl"] = {
		["t1"] = {
			{ id = 890000000020477, en = "Grabbing the short one!", tags = {  } },
			{ id = 890000000020478, en = "Short one in hand!", tags = {  } },
			{ id = 890000000020479, en = "Through the window!", tags = { "into" } },
			{ id = 890000000020480, en = "Switching. At the door!", tags = { "into" } },
			{ id = 890000000020481, en = "Hitting the house!", tags = { "in" } },
		},
		["t2"] = {
			{ id = 890000000020482, en = "Putting the short one on", tags = {  } },
			{ id = 890000000020483, en = "Under the barrel now", tags = {  } },
			{ id = 890000000020484, en = "This one at the window", tags = { "into" } },
			{ id = 890000000020485, en = "I'll take the door", tags = { "into" } },
			{ id = 890000000020486, en = "Hitting the house", tags = { "in" } },
		},
		["t4"] = {
			{ id = 890000000020487, en = "Short one.", tags = {  } },
			{ id = 890000000020488, en = "Under the barrel.", tags = {  } },
			{ id = 890000000020489, en = "Window.", tags = { "into" } },
			{ id = 890000000020490, en = "Door.", tags = { "into" } },
			{ id = 890000000020491, en = "House.", tags = { "in" } },
		},
	},
	["wpn_rocket"] = {
		["t1"] = {
			{ id = 890000000020492, en = "Grabbing the pipe!", tags = {  } },
			{ id = 890000000020493, en = "The big one in hand!", tags = {  } },
			{ id = 890000000020494, en = "Back, this bangs!", tags = {  } },
			{ id = 890000000020495, en = "Switching. House comes down!", tags = { "in" } },
			{ id = 890000000020496, en = "This one off the shoulder!", tags = {  } },
		},
		["t2"] = {
			{ id = 890000000020497, en = "Grabbing the pipe", tags = {  } },
			{ id = 890000000020498, en = "Pipe's going up", tags = {  } },
			{ id = 890000000020499, en = "Putting the heavy one on", tags = {  } },
			{ id = 890000000020500, en = "That house comes down", tags = { "in" } },
			{ id = 890000000020501, en = "Off the shoulder", tags = {  } },
		},
		["t4"] = {
			{ id = 890000000020502, en = "Pipe.", tags = {  } },
			{ id = 890000000020503, en = "Heavy.", tags = {  } },
			{ id = 890000000020504, en = "Coming down.", tags = {  } },
			{ id = 890000000020505, en = "The house.", tags = { "in" } },
			{ id = 890000000020506, en = "Shoulder.", tags = {  } },
		},
	},
	["wpn_sniper"] = {
		["t1"] = {
			{ id = 890000000020507, en = "Grabbing the long eye!", tags = {  } },
			{ id = 890000000020508, en = "Long one in hand!", tags = {  } },
			{ id = 890000000020509, en = "I'll go prone and shoot!", tags = {  } },
			{ id = 890000000020510, en = "Switching. From the hill!", tags = { "high" } },
			{ id = 890000000020511, en = "Don't breathe. Aiming!", tags = {  } },
		},
		["t2"] = {
			{ id = 890000000020512, en = "Putting the long one on", tags = {  } },
			{ id = 890000000020513, en = "This one from the hill", tags = { "high" } },
			{ id = 890000000020514, en = "Down. Shooting", tags = {  } },
			{ id = 890000000020515, en = "I can reach from here", tags = {  } },
			{ id = 890000000020516, en = "One. Then quiet", tags = {  } },
		},
		["t4"] = {
			{ id = 890000000020517, en = "Long one.", tags = {  } },
			{ id = 890000000020518, en = "The hill.", tags = { "high" } },
			{ id = 890000000020519, en = "Down.", tags = {  } },
			{ id = 890000000020520, en = "One.", tags = {  } },
			{ id = 890000000020521, en = "Quiet.", tags = {  } },
		},
	},
	["wpn_melee"] = {
		["t1"] = {
			{ id = 890000000020522, en = "Knife's out!", tags = {  } },
			{ id = 890000000020523, en = "Dropped the gun. Cutting!", tags = {  } },
			{ id = 890000000020524, en = "Iron in hand!", tags = {  } },
			{ id = 890000000020525, en = "No rounds. Knife!", tags = {  } },
			{ id = 890000000020526, en = "Switching. Closer!", tags = {  } },
		},
		["t2"] = {
			{ id = 890000000020527, en = "On the knife", tags = {  } },
			{ id = 890000000020528, en = "Gun aside", tags = {  } },
			{ id = 890000000020529, en = "Iron", tags = {  } },
			{ id = 890000000020530, en = "This one up close", tags = {  } },
			{ id = 890000000020531, en = "Cut", tags = {  } },
		},
		["t4"] = {
			{ id = 890000000020532, en = "Knife.", tags = {  } },
			{ id = 890000000020533, en = "Gun down.", tags = {  } },
			{ id = 890000000020534, en = "Iron.", tags = {  } },
			{ id = 890000000020535, en = "Close.", tags = {  } },
			{ id = 890000000020536, en = "Cut.", tags = {  } },
		},
	},
	["mg_setup"] = {
		["t1"] = {
			{ id = 890000000020537, en = "I'm sitting here", tags = {  } },
			{ id = 890000000020538, en = "From this corner!", tags = {  } },
			{ id = 890000000020539, en = "Setting up. Cover me", tags = {  } },
			{ id = 890000000020540, en = "Sitting here. Street's mine", tags = { "out" } },
			{ id = 890000000020541, en = "Legs down!", tags = {  } },
		},
		["t2"] = {
			{ id = 890000000020542, en = "I'll take the street", tags = { "out" } },
			{ id = 890000000020543, en = "Goes here", tags = {  } },
			{ id = 890000000020544, en = "From the corner", tags = {  } },
			{ id = 890000000020545, en = "I'll shut the yard", tags = { "out" } },
			{ id = 890000000020546, en = "Sat. Street's mine", tags = { "out" } },
		},
		["t4"] = {
			{ id = 890000000020547, en = "This street's mine.", tags = { "out" } },
			{ id = 890000000020548, en = "Here.", tags = {  } },
			{ id = 890000000020549, en = "Corner.", tags = {  } },
			{ id = 890000000020550, en = "Sat.", tags = {  } },
			{ id = 890000000020551, en = "Yard's mine.", tags = { "out" } },
		},
	},
	["seq_press"] = {
		["t1"] = {
			{ id = 890000000020552, en = "I'm going at them!", tags = {  } },
			{ id = 890000000020553, en = "I'm going in!", tags = {  } },
			{ id = 890000000020554, en = "Don't stand. After me!", tags = {  } },
			{ id = 890000000020555, en = "Stay with me!", tags = {  } },
			{ id = 890000000020556, en = "We go!", tags = {  } },
		},
		["t2"] = {
			{ id = 890000000020557, en = "Going in", tags = {  } },
			{ id = 890000000020558, en = "Running at them", tags = {  } },
			{ id = 890000000020559, en = "Forward", tags = {  } },
			{ id = 890000000020560, en = "Don't wait", tags = {  } },
			{ id = 890000000020561, en = "I'll go first", tags = {  } },
		},
		["t4"] = {
			{ id = 890000000020562, en = "In.", tags = {  } },
			{ id = 890000000020563, en = "Forward.", tags = {  } },
			{ id = 890000000020564, en = "At them.", tags = {  } },
			{ id = 890000000020565, en = "Going.", tags = {  } },
			{ id = 890000000020566, en = "I'm first.", tags = {  } },
		},
	},
	["seq_flank"] = {
		["t1"] = {
			{ id = 890000000020567, en = "I'll come from the side!", tags = {  } },
			{ id = 890000000020568, en = "Not the front. Around!", tags = {  } },
			{ id = 890000000020569, en = "I'll go around them!", tags = {  } },
			{ id = 890000000020570, en = "Running the edge!", tags = {  } },
			{ id = 890000000020571, en = "With me, from the side!", tags = {  } },
		},
		["t2"] = {
			{ id = 890000000020572, en = "The side", tags = {  } },
			{ id = 890000000020573, en = "Around", tags = {  } },
			{ id = 890000000020574, en = "Not the front", tags = {  } },
			{ id = 890000000020575, en = "The edge", tags = {  } },
			{ id = 890000000020576, en = "Around them", tags = {  } },
		},
		["t4"] = {
			{ id = 890000000020577, en = "The side.", tags = {  } },
			{ id = 890000000020578, en = "Around.", tags = {  } },
			{ id = 890000000020579, en = "Not the front.", tags = {  } },
			{ id = 890000000020580, en = "The edge.", tags = {  } },
			{ id = 890000000020581, en = "Around.", tags = {  } },
		},
	},
	["move_long"] = {
		["t1"] = {
			{ id = 890000000020582, en = "It's far. I'm running!", tags = {  } },
			{ id = 890000000020583, en = "I'll get there!", tags = {  } },
			{ id = 890000000020584, en = "Don't wait. I'm going!", tags = {  } },
			{ id = 890000000020585, en = "Watch. Across the yard!", tags = { "out" } },
			{ id = 890000000020586, en = "Crossing now!", tags = {  } },
		},
		["t2"] = {
			{ id = 890000000020587, en = "Sprinting", tags = {  } },
			{ id = 890000000020588, en = "I'll get there", tags = {  } },
			{ id = 890000000020589, en = "Crossing", tags = {  } },
			{ id = 890000000020590, en = "Closing in", tags = {  } },
			{ id = 890000000020591, en = "It's far. Still going", tags = {  } },
		},
		["t4"] = {
			{ id = 890000000020592, en = "Sprint.", tags = {  } },
			{ id = 890000000020593, en = "I'll get there.", tags = {  } },
			{ id = 890000000020594, en = "Running.", tags = {  } },
			{ id = 890000000020595, en = "Closer.", tags = {  } },
			{ id = 890000000020596, en = "It's far. Going.", tags = {  } },
		},
	},
}
-- JAZZ-AI-BARK-BANK-END
