"""Targeted static-runtime tests for the AME market and browser contract.

The harness executes the real Lua files in lupa with a small JA3 stub.  It
protects the 15-slot market, per-role soft guarantees, AME-only team filter,
mail-wrapper idempotence, and Lua syntax.  Live-game UI acceptance is still
required for the rendered PDA page.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path

from lupa import LuaRuntime


ROOT = Path(__file__).resolve().parents[2]
ROSTER_SCRIPT = ROOT / "docs" / "tools" / "_gen_ame_roster_60.py"
AME_LUA_FILES = (
    "System_AME_Browser.lua",
    "System_AME_Browser_Template.lua",
    "System_AME_Filters.lua",
    "System_AME_Mail.lua",
    "System_AME_Market.lua",
    "System_AME_Nationalities.lua",
)


def _source(name: str) -> str:
    return (ROOT / "Code" / name).read_text(encoding="utf-8-sig")


def _load_roster() -> list[dict]:
    spec = importlib.util.spec_from_file_location("ame_roster_contract", ROSTER_SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load AME roster: {ROSTER_SCRIPT}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    roster = module.ROSTER
    assert len(roster) == 60
    return roster


def test_lua_syntax() -> None:
    lua = LuaRuntime(unpack_returned_tuples=True)
    compile_lua = lua.eval(
        "function(source, name) "
        "local chunk, err = load(source, name); "
        "return chunk ~= nil, err "
        "end"
    )
    for name in AME_LUA_FILES:
        ok, error = compile_lua(_source(name), f"@Code/{name}")
        assert ok, f"{name}: {error}"


def _market_runtime() -> LuaRuntime:
    lua = LuaRuntime(unpack_returned_tuples=True)
    lua.execute(
        r'''
OnMsg = {}
const = { Scale = { day = 1 } }
Game = { id = 771, CampaignTime = 0, CampaignTimeStart = 0 }
gv_UnitData = {}
empty_table = {}

function T(_, text)
	return text
end

function GameVar(name, factory)
	rawset(_G, name, factory())
end

function ObjModified()
end

function DelayedCall(_, fn, ...)
	return fn(...)
end

function xxhash(...)
	local args = { ... }
	if args[#args] == "leave" then
		return -1
	end
	local value = 216613
	for _, part in ipairs(args) do
		local text = tostring(part)
		for i = 1, #text do
			value = (value * 167 + string.byte(text, i)) % 2147483647
		end
	end
	return value
end

function BraidRandom(seed, lo, hi)
	if seed == -1 then
		return hi
	end
	return lo + (seed % (hi - lo + 1))
end

function table.find(items, wanted)
	for i, value in ipairs(items or empty_table) do
		if value == wanted then
			return i
		end
	end
	return false
end

function table.ifilter(items, predicate)
	local result = {}
	for i, value in ipairs(items or empty_table) do
		if predicate(i, value) then
			result[#result + 1] = value
		end
	end
	return result
end
'''
    )
    units = lua.globals().gv_UnitData
    for slot, merc in enumerate(_load_roster(), 1):
        unit_id = f"JAZZ_AME_{slot:02d}"
        units[unit_id] = lua.table_from(
            {
                "session_id": unit_id,
                "Affiliation": "AME",
                "AMECategory": merc["cat"],
                "AMERole": merc["role"],
                "HireStatus": "NotMet",
            }
        )
    lua.execute(_source("System_AME_Market.lua"))
    return lua


def _market_snapshot() -> tuple[tuple[str, ...], tuple[str, ...]]:
    lua = _market_runtime()
    lua.execute(
        r'''
JAZZ_AME_InitMarket(true)

local function available_count()
	local count = 0
	for _, merc in pairs(gv_UnitData) do
		if merc.HireStatus == "Available" then
			count = count + 1
		end
	end
	return count
end

assert(available_count() == 15, "initial AME window is not exactly 15")

-- Build a window without any guaranteed role.  Counters at one mean this is
-- the next market cycle after the role disappeared.
local opened = 0
for _, merc in pairs(gv_UnitData) do
	merc.HireStatus = "NotMet"
end
for slot = 1, 60 do
	local merc = gv_UnitData[string.format("JAZZ_AME_%02d", slot)]
	if opened < 15
		and merc.AMERole ~= "Medic"
		and merc.AMERole ~= "Instructor"
		and merc.AMERole ~= "Sniper"
	then
		merc.HireStatus = "Available"
		opened = opened + 1
	end
end
assert(opened == 15, "test roster cannot form a non-guaranteed window")

gv_JAZZ_AME_Market.specialist_missing_ticks = {
	Medic = 1,
	Instructor = 1,
	Sniper = 1,
}
gv_JAZZ_AME_Market.next_tick_day = 14
Game.CampaignTime = 14
JAZZ_AME_MarketTick()

assert(available_count() == 15, "role guarantee drifted from the 15-slot target")
for _, role in ipairs({ "Medic", "Instructor", "Sniper" }) do
	local found = false
	for _, merc in pairs(gv_UnitData) do
		if merc.HireStatus == "Available" and merc.AMERole == role then
			found = true
			break
		end
	end
	assert(found, "missing guaranteed role: " .. role)
	assert(gv_JAZZ_AME_Market.specialist_missing_ticks[role] == 0,
		"guaranteed role counter was not reset: " .. role)
end

local hired
for _, merc in pairs(gv_UnitData) do
	if merc.HireStatus == "Available" then
		hired = merc
		break
	end
end
assert(hired, "test could not select a merc for hire protection")
hired.HireStatus = "Hired"

gv_JAZZ_AME_Market.next_tick_day = 28
Game.CampaignTime = 28
JAZZ_AME_MarketTick()
assert(hired.HireStatus == "Hired", "market rotation changed a hired merc")
assert(available_count() == 15, "market did not refill after a hire")

ame_test_available = {}
ame_test_terminal = {}
for id, merc in pairs(gv_UnitData) do
	if merc.HireStatus == "Available" then
		ame_test_available[#ame_test_available + 1] = id
	end
	local slot = gv_JAZZ_AME_Market.slots[id]
	if slot and slot.reason then
		ame_test_terminal[#ame_test_terminal + 1] = id .. ":" .. slot.reason
	end
end
table.sort(ame_test_available)
table.sort(ame_test_terminal)
'''
    )
    available = tuple(lua.globals().ame_test_available.values())
    terminal = tuple(lua.globals().ame_test_terminal.values())
    return available, terminal


def test_market_window_and_role_guarantees() -> None:
    first = _market_snapshot()
    second = _market_snapshot()
    assert first == second, "same game seed produced a different AME market"
    assert len(first[0]) == 15


def test_ame_team_filter() -> None:
    lua = LuaRuntime(unpack_returned_tuples=True)
    lua.execute(
        r'''
TFormat = {}
empty_table = {}
gv_UnitData = {
	ame_hired = { Affiliation = "AME", HireStatus = "Hired" },
	ame_open = { Affiliation = "AME", HireStatus = "Available" },
	aim_hired = { Affiliation = "AIM", HireStatus = "Hired" },
}
function T(_, text)
	return text
end
'''
    )
    lua.execute(_source("System_AME_Filters.lua"))
    lua.execute(
        r'''
assert(TFormat.AMEPlayerMercCount() == 1,
	"AME team counter included a non-AME hire")
local my_team = GetAMEScreenFilters()[6]
assert(my_team.func(gv_UnitData.ame_hired), "AME hire missing from My Team")
assert(not my_team.func(gv_UnitData.ame_open), "available AME listed in My Team")
assert(not my_team.func(gv_UnitData.aim_hired), "AIM hire leaked into AME My Team")
'''
    )


def test_mail_wrapper_is_idempotent() -> None:
    lua = LuaRuntime(unpack_returned_tuples=True)
    lua.execute(
        r'''
OnMsg = {}
empty_table = {}
base_calls = 0
NetSyncEvents = {
	MarkEmailAsRead = function()
		base_calls = base_calls + 1
	end,
}
function T(_, text)
	return text
end
function GetReceivedEmails()
	return empty_table
end
function ObjModified()
end
'''
    )
    source = _source("System_AME_Mail.lua")
    lua.execute(source)
    lua.execute("OnMsg.DataLoaded(); ame_first_wrapper = NetSyncEvents.MarkEmailAsRead")
    lua.execute(source)
    lua.execute(
        r'''
OnMsg.DataLoaded()
assert(NetSyncEvents.MarkEmailAsRead == ame_first_wrapper,
	"ModsReloaded nested the AME mail wrapper")
NetSyncEvents.MarkEmailAsRead("unrelated", true)
assert(base_calls == 1, "AME mail wrapper called its base more than once")

external_calls = 0
local external_base = NetSyncEvents.MarkEmailAsRead
NetSyncEvents.MarkEmailAsRead = function(...)
	external_calls = external_calls + 1
	return external_base(...)
end
OnMsg.ModsReloaded()
NetSyncEvents.MarkEmailAsRead("wrapped-by-another-mod", true)
assert(external_calls == 1, "AME reassert skipped an external mail wrapper")
assert(base_calls == 2, "AME reassert formed a recursive wrapper cycle")
'''
    )


def test_browser_wrappers_are_cycle_safe() -> None:
    lua = LuaRuntime(unpack_returned_tuples=True)
    lua.execute(
        r'''
OnMsg = {}
DefineClass = setmetatable({}, {
	__newindex = function(target, key, value)
		rawset(target, key, value)
		rawset(_G, key, value)
	end,
})
Platform = { demo = false }
Game = { CampaignTime = 0 }
const = { Scale = { day = 1 } }
PDABrowserTabData = { { id = "aim" } }
PDABrowserTabState = {}
PDABrowser = {}
XTemplates = {}
TFormat = {}

contact_base_calls = 0
pda_base_calls = 0
dock_base_calls = 0

function T(_, text)
	return text
end
function Untranslated(text)
	return text
end
function IsKindOf()
	return false
end
function ObjModified()
end
function GetDialog()
	return false
end

function MercCanContact()
	contact_base_calls = contact_base_calls + 1
	return "base-contact"
end
TFormat.PDAUrl = function()
	pda_base_calls = pda_base_calls + 1
	return "base-url"
end
function DockBrowserTab()
	dock_base_calls = dock_base_calls + 1
end

function table.find(items, key, wanted)
	if wanted == nil then
		wanted = key
		for i, value in ipairs(items) do
			if value == wanted then
				return i
			end
		end
		return false
	end
	for i, value in ipairs(items) do
		if value[key] == wanted then
			return i
		end
	end
	return false
end

function table.map(items, key)
	local result = {}
	for i, value in ipairs(items) do
		result[i] = value[key]
	end
	return result
end
'''
    )
    lua.execute(_source("System_AME_Browser.lua"))
    lua.execute(
        r'''
OnMsg.DataLoaded()
assert(MercCanContact({ Affiliation = "AME", HireStatus = "Available" }) == "enabled")
assert(MercCanContact({ Affiliation = "AIM" }) == "base-contact")
assert(TFormat.PDAUrl() == "base-url")
DockBrowserTab("ame")

local old_contact = MercCanContact
local old_pda = TFormat.PDAUrl
local old_dock = DockBrowserTab
external_contact_calls = 0
external_pda_calls = 0
external_dock_calls = 0
MercCanContact = function(...)
	external_contact_calls = external_contact_calls + 1
	return old_contact(...)
end
TFormat.PDAUrl = function(...)
	external_pda_calls = external_pda_calls + 1
	return old_pda(...)
end
DockBrowserTab = function(...)
	external_dock_calls = external_dock_calls + 1
	return old_dock(...)
end

contact_base_calls = 0
pda_base_calls = 0
dock_base_calls = 0
OnMsg.ModsReloaded()

assert(MercCanContact({ Affiliation = "AIM" }) == "base-contact")
assert(TFormat.PDAUrl() == "base-url")
DockBrowserTab("ame")
assert(external_contact_calls == 1 and contact_base_calls == 1,
	"MercCanContact reassert formed a wrapper cycle")
assert(external_pda_calls == 1 and pda_base_calls == 1,
	"PDAUrl reassert formed a wrapper cycle")
assert(external_dock_calls == 1 and dock_base_calls == 1,
	"DockBrowserTab reassert formed a wrapper cycle")
'''
    )


def test_browser_contract_markers() -> None:
    browser = _source("System_AME_Browser.lua")
    template = _source("System_AME_Browser_Template.lua")
    assert "TDevModeGetEnglishText" in browser
    assert "ud.session_id or unit_id" in browser
    assert '"idAMECategory"' in template
    assert '"idAMEPotential"' in template
    assert "JAZZ_AME_GetDepartureReasonText" in template


def main() -> int:
    tests = (
        test_lua_syntax,
        test_market_window_and_role_guarantees,
        test_ame_team_filter,
        test_mail_wrapper_is_idempotent,
        test_browser_wrappers_are_cycle_safe,
        test_browser_contract_markers,
    )
    for test in tests:
        test()
        print(f"PASS {test.__name__}")
    print(f"PASS AME targeted contract ({len(tests)} tests)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
