"""Targeted static-runtime tests for the R.I.S. Lua contract.

The harness executes the real Lua files in lupa with a deliberately small JA3
stub. It does not replace live-game acceptance; it protects visibility gates,
two-stage dossier unlocks, and Lua syntax from regression.
"""

from __future__ import annotations

from pathlib import Path

from lupa import LuaRuntime


ROOT = Path(__file__).resolve().parents[2]
RIS_LUA_FILES = (
    "System_RIS_Mail.lua",
    "System_RIS_Content.lua",
    "System_RIS_Combat.lua",
    "System_RIS_Browser.lua",
    "System_RIS_Strategy.lua",
)


def _source(name: str) -> str:
    return (ROOT / "Code" / name).read_text(encoding="utf-8-sig")


def test_lua_syntax() -> None:
    lua = LuaRuntime(unpack_returned_tuples=True)
    load = lua.eval(
        "function(source, name) "
        "local chunk, err = load(source, name); "
        "return chunk ~= nil, err "
        "end"
    )
    for name in RIS_LUA_FILES:
        ok, error = load(_source(name), f"@Code/{name}")
        assert ok, f"{name}: {error}"


def test_strategy_visibility_gates() -> None:
    lua = LuaRuntime(unpack_returned_tuples=True)
    lua.execute(
        r'''
OnMsg = {}
Game = { CampaignTime = 1000 }
gv_JAZZ_RIS = {
	strategy_observed = {},
	strategy_delivered = {},
	strategy_delivery_order = {},
	strategy_major_delivery_baseline = {},
	mail_queue = {},
	next_strategy_at = 0,
	met_types = { JAZZ_Legion_Test = true },
	kills = {},
	welcome_read = false,
}
gv_Squads = {}
gv_Sectors = {}
gv_JAZZ_LegionAI = { squads = {}, regions = {}, outposts = {} }
Regions = {}
strategy_received = {}

function JAZZ_RIS_MigrateState()
	return gv_JAZZ_RIS
end

function JAZZ_RIS_EnqueueMail(item)
	gv_JAZZ_RIS.mail_queue[#gv_JAZZ_RIS.mail_queue + 1] = item
	return true
end

function GetReceivedEmails()
	return strategy_received
end

function IsSquadTravelling(squad)
	return squad and squad.travelling or false
end

function IsSectorRevealed(sector)
	return sector and sector.revealed or false
end

function ObjModified()
end

function DelayedCall(_, fn, ...)
	return fn(...)
end
'''
    )
    lua.execute(_source("System_RIS_Strategy.lua"))
    lua.execute(
        r'''
local st = gv_JAZZ_RIS

gv_Sectors.H1 = { Id = "H1", Side = "enemy1", discovered = false, revealed = false }
gv_Squads.tax_hidden = { UniqueId = "tax_hidden", CurrentSector = "H1", travelling = false }
gv_JAZZ_LegionAI.squads.tax_hidden = {
	region_id = "R0",
	role = "tax",
	state = "ready_for_orders",
}
gv_JAZZ_LegionAI.regions.R0 = {
    reports = {
        [1] = {
            id = 1,
            target_sector = "H1",
            delivered = true,
            generic = false,
        },
    },
}
JAZZ_RIS_PollStrategySignals(false)
assert(st.strategy_observed.strategy_villages == nil,
	"hidden collector leaked a Strategy observation")
assert(st.strategy_observed.strategy_eyes == nil,
    "hidden delivered recon report leaked a Strategy observation")

gv_Squads.tax_hidden.travelling = true
JAZZ_RIS_PollStrategySignals(false)
assert(st.strategy_observed.strategy_villages == 1000,
	"visible travelling collector was not observed")

gv_Squads.recon = { UniqueId = "recon", CurrentSector = "H1", travelling = true }
gv_JAZZ_LegionAI.squads.recon = {
    region_id = "R0",
    role = "recon",
    state = "returning",
    task = {
        task_type = "return_with_intel",
        report = { target_sector = "H1", generic = false },
    },
}
JAZZ_RIS_PollStrategySignals(false)
assert(st.strategy_observed.strategy_eyes == 1000,
    "visible returning recon squad was not observed")

gv_Squads.qrf_hidden = { UniqueId = "qrf_hidden", CurrentSector = "H1", travelling = false }
gv_JAZZ_LegionAI.squads.qrf_hidden = {
	region_id = "R0",
	role = "qrf",
	state = "ready_for_orders",
}
JAZZ_RIS_PollStrategySignals(false)
assert(st.strategy_observed.strategy_answer == nil,
	"hidden response squad leaked a Strategy observation")

gv_Sectors.H1.discovered = true
gv_Sectors.H1.revealed = true
JAZZ_RIS_PollStrategySignals(false)
assert(st.strategy_observed.strategy_answer == 1000,
	"response squad in a revealed sector was not observed")

gv_Sectors.P1 = { Id = "P1", Side = "player1", discovered = true, revealed = true }
gv_Squads.patrol = { UniqueId = "patrol", CurrentSector = "P1", travelling = false }
gv_JAZZ_LegionAI.squads.patrol = {
	region_id = "R0",
	role = "patrol",
	state = "working",
	task = { task_type = "patrol_dwell" },
}
JAZZ_RIS_PollStrategySignals(false)
assert(st.strategy_observed.strategy_roads == 1000,
	"patrol in player-held ground was not observed")

gv_Sectors.H2 = { Id = "H2", Side = "enemy1", discovered = false, revealed = false }
gv_Squads.late = { UniqueId = "late", CurrentSector = "H2", travelling = false }
gv_JAZZ_LegionAI.squads.late = {
	region_id = "R1",
	role = "garrison",
	state = "ready_for_orders",
}
gv_JAZZ_LegionAI.outposts.O1 = {
	region_id = "R1",
	major_delivery_done = true,
}
Regions.R1 = { id = "R1", LateAwakenMinTier = 2 }
JAZZ_RIS_PollStrategySignals(false)
assert(st.strategy_observed.strategy_sleep == nil,
	"hidden headquarters delivery leaked an Awakening observation")

gv_Squads.late.travelling = true
JAZZ_RIS_PollStrategySignals(false)
assert(st.strategy_observed.strategy_sleep == 1000,
	"visible post-delivery district activity was not observed")

st.strategy_observed.strategy_sleep = nil
gv_Sectors.H3 = { Id = "H3", Side = "enemy1", discovered = true, revealed = true }
gv_Sectors.H4 = { Id = "H4", Side = "enemy1", discovered = true, revealed = true }
gv_Squads.already_visible = {
    UniqueId = "already_visible",
    CurrentSector = "H3",
    travelling = false,
}
gv_JAZZ_LegionAI.squads.already_visible = {
    region_id = "R2",
    role = "garrison",
    state = "ready_for_orders",
}
gv_JAZZ_LegionAI.outposts.O2 = {
    region_id = "R2",
    major_delivery_done = false,
}
Regions.R2 = { id = "R2", LateAwakenMinTier = 2 }
JAZZ_RIS_PollStrategySignals(false)
gv_JAZZ_LegionAI.outposts.O2.major_delivery_done = true
JAZZ_RIS_PollStrategySignals(false)
assert(st.strategy_observed.strategy_sleep == nil,
    "hidden headquarters delivery reused pre-existing visible activity")
JAZZ_RIS_PollStrategySignals(false)
assert(st.strategy_observed.strategy_sleep == nil,
    "unchanged pre-delivery activity unlocked Awakening")
gv_Squads.already_visible.CurrentSector = "H4"
JAZZ_RIS_PollStrategySignals(false)
assert(st.strategy_observed.strategy_sleep == 1000,
    "post-delivery movement did not unlock Awakening")

local pending = 0
for _, row in ipairs(st.mail_queue) do
	if row.kind == "strategy" then
		pending = pending + 1
	end
end
assert(pending <= 1, "more than one Strategy row entered the desk queue")

st.strategy_observed.strategy_network = nil
st.welcome_read = true
st.met_types = {}
st.kills = {}
st.last_mailed_tier = 11
strategy_received = {}
JAZZ_RIS_PollStrategySignals(false)
assert(st.strategy_observed.strategy_network == nil,
    "stale last_mailed_tier unlocked Network without a received brief")
strategy_received = { { id = "RIS_LegionBrief_11" } }
JAZZ_RIS_PollStrategySignals(false)
assert(st.strategy_observed.strategy_network == 1000,
    "received supply brief did not unlock Network")
'''
    )


def test_mail_migration_and_desk() -> None:
    lua = LuaRuntime(unpack_returned_tuples=True)
    lua.execute(
        r'''
OnMsg = {}
Game = { CampaignTime = 1000 }
const = { Scale = { h = 100 } }
empty_table = {}
Emails = {
	RIS_MajorStrategy_Network = {},
	RIS_MajorStrategy_Response = {},
	RIS_TestOrdinary = {},
	RIS_UnitSighting = {},
	RIS_EliteObit = {},
	RIS_NpcObit = {},
}
received = {}
gv_ReceivedEmails = received
PDABrowserTabState = { ris = { locked = false } }

function GameVar(name, factory)
	if rawget(_G, name) == nil then
		rawset(_G, name, factory())
	end
end

function GetReceivedEmails()
	return received
end

function ReceiveEmail(id, context)
	received[#received + 1] = { id = id, context = context, read = false }
end

function Untranslated(value)
	return { value, untranslated = true }
end

function T(value, text)
    if type(value) == "table" then
        return value
    end
    return { value, text }
end

function IsT(value)
    return type(value) == "table"
        and (type(value[1]) == "number" or value.untranslated or value.user_text)
end

function TGetID(value)
    return type(value) == "table" and type(value[1]) == "number" and value[1] or false
end

function Max(a, b)
	return math.max(a, b)
end

function ObjModified()
end

JAZZ_RIS_DOSSIERS = {
	JAZZ_Legion_Test = { title = { 9010 } },
}
JAZZ_RIS_EXTRA = {
    legacy_contact = { 9001 },
    legacy_opponent = { 9002 },
}
gv_UnitData = {
    LegacyNpc = { Name = { 9003 } },
    LegacyElite = { Name = { 9004 } },
}
'''
    )
    lua.execute(_source("System_RIS_Mail.lua"))
    lua.execute(
        r'''
gv_JAZZ_RIS = {
	schema_version = 1,
	welcome_sent = true,
	welcome_read = true,
	last_mailed_tier = 0,
	mod_awake_at = 0,
	next_dispatch_at = 0,
	next_strategy_at = 0,
	strategy_catchup_done = false,
	mail_queue = {
		{
			key = "meet_JAZZ_Legion_Test",
			kind = "meet",
			email_id = "RIS_UnitSighting",
			type_id = "JAZZ_Legion_Test",
			ready_at = 5000,
			context = {
				unit_title = "frozen translation",
				dossier = "frozen body",
			},
		},
           {
               key = "legacy_elite_notice",
               kind = "obit",
               email_id = "RIS_EliteObit",
               context = {
                   name = "frozen opponent",
                   npc_id = "LegacyElite",
               },
           },
        {
            key = "obit_elite:session:LegacyElite",
            kind = "obit",
            email_id = "RIS_EliteObit",
            obit_key = "elite:session:LegacyElite",
            name_ref = gv_UnitData.LegacyElite.Name,
            ready_at = 600,
        },
        {
            key = "strategy_strategy_network",
            kind = "strategy",
            material_id = "strategy_network",
            email_id = "RIS_MajorStrategy_Network",
            ready_at = 500,
        },
	},
	kills = {},
	met_types = { JAZZ_Legion_Test = true },
	dossiers = {},
	obits_sent = { ["elite:session:LegacyElite"] = true },
	battles = {
		{
			title = "old translated title",
			body = "old translated body",
			sector_id = "A1",
		},
	},
	quest_met = {},
	strategy_observed = {},
	strategy_delivered = { strategy_network = 500 },
	strategy_delivery_order = { "strategy_network" },
	strategy_major_delivery_baseline = {},
}

local st = JAZZ_RIS_MigrateState()
assert(st.schema_version == 3, "R.I.S. state did not migrate to schema 3")
assert(st.mail_queue[1].context == nil,
	"migrated sighting row retained a frozen translation")
assert(not st.met_types.JAZZ_Legion_Test,
    "queued sighting retained an enqueue-time contact unlock")
assert(st.mail_queue[2].context == nil
    and st.mail_queue[2].key == "obit_elite:session:LegacyElite"
    and st.mail_queue[2].obit_key == "elite:session:LegacyElite"
    and st.mail_queue[2].name_ref == gv_UnitData.LegacyElite.Name,
    "migrated obituary row did not recover its stable identity")
assert(not st.obits_sent["elite:session:LegacyElite"],
    "queued obituary remained marked as already received")
assert(not st.met_types.JAZZ_Legion_Test,
    "queued sighting retained its legacy enqueue-time contact flag")
assert(#st.mail_queue == 3,
    "duplicate stable field-mail rows survived migration")
assert(not st.strategy_delivered.strategy_network
    and #st.strategy_delivery_order == 0
    and st.next_strategy_at == 0,
    "queued Strategy mail retained pre-receipt delivery state")
assert(st.battles[1].kind == "legacy"
	and st.battles[1].title == nil
	and st.battles[1].body == nil,
	"legacy AAR retained translated prose")

st.mail_queue = {}
received = {
    { id = "RIS_MajorStrategy_Network", time = 100, read = true },
}
gv_ReceivedEmails = received
st.strategy_observed = {}
st.strategy_delivered = {}
st.strategy_delivery_order = {}
st.next_strategy_at = 0
JAZZ_RIS_MigrateState()
st.strategy_observed.strategy_answer = 900
JAZZ_RIS_EnqueueMail({
	kind = "strategy",
	material_id = "strategy_answer",
	ready_at = 1000,
})
JAZZ_RIS_EnqueueMail({
	key = "ordinary",
	kind = "field",
	email_id = "RIS_TestOrdinary",
	ready_at = 1000,
})

g_Combat = {}
assert(not JAZZ_RIS_ProcessMailQueue(false),
    "R.I.S. desk marked mail delivered while vanilla would defer it")
assert(#received == 1 and not st.strategy_delivered.strategy_answer,
    "combat-time mail changed receipt or Strategy state")
g_Combat = false

assert(JAZZ_RIS_ProcessMailQueue(false), "due ordinary mail was not delivered")
assert(received[2] and received[2].id == "RIS_TestOrdinary",
	"blocked Strategy row prevented ordinary R.I.S. mail")
assert(st.next_dispatch_at == 1500, "shared five-hour desk spacing was not applied")
assert(st.strategy_delivered.strategy_network == 100
    and not st.strategy_delivered.strategy_answer,
	"Strategy mail ignored its separate cooldown")

Game.CampaignTime = 2500
assert(JAZZ_RIS_ProcessMailQueue(false), "eligible Strategy mail was not delivered")
assert(received[3] and received[3].id == "RIS_MajorStrategy_Response",
	"wrong Strategy Email preset was delivered")
assert(st.strategy_delivered.strategy_answer == 2500,
	"Strategy delivery time was not recorded")
assert(st.strategy_delivery_order[1] == "strategy_network"
    and st.strategy_delivery_order[2] == "strategy_answer",
	"Strategy archive order was not recorded")
assert(st.next_strategy_at == 4900, "24-hour Strategy cooldown was not applied")

Game.CampaignTime = 5000
st.next_dispatch_at = 0
assert(JAZZ_RIS_EnqueueUnitSighting("JAZZ_Legion_Test", 0),
	"sighting row was not queued")
assert(not st.met_types.JAZZ_Legion_Test,
	"contact card unlocked before sighting delivery")
assert(JAZZ_RIS_ProcessMailQueue(false), "sighting mail was not delivered")
assert(st.met_types.JAZZ_Legion_Test,
	"contact card did not unlock on sighting delivery")
assert(received[4].context.unit_title == JAZZ_RIS_DOSSIERS.JAZZ_Legion_Test.title
    and received[4].context.type_id == "JAZZ_Legion_Test",
	"sighting context did not resolve at delivery time")

Game.CampaignTime = 5500
st.next_dispatch_at = 0
st.mail_queue[#st.mail_queue + 1] = {
    key = "meet_JAZZ_Legion_Removed",
    kind = "meet",
    email_id = "RIS_UnitSighting",
    type_id = "JAZZ_Legion_Removed",
    ready_at = 0,
}
assert(JAZZ_RIS_ProcessMailQueue(false)
    and received[5].context.unit_title == JAZZ_RIS_EXTRA.legacy_contact
    and received[5].context.type_id == nil,
    "removed legacy sighting blocked the desk or leaked its obsolete id")

Game.CampaignTime = 6000
st.next_dispatch_at = 0
assert(JAZZ_RIS_EnqueueEliteObit("Named hostile", 0, "named-hostile"),
    "elite obituary row was not queued")
assert(not st.obits_sent["elite:named-hostile"],
    "obituary was marked received at enqueue time")
g_Combat = {}
assert(not JAZZ_RIS_ProcessMailQueue(false)
    and not st.obits_sent["elite:named-hostile"],
    "deferred obituary was marked received during combat")
g_Combat = false
assert(JAZZ_RIS_ProcessMailQueue(false)
    and st.obits_sent["elite:named-hostile"],
    "obituary receipt was not recorded after inbox delivery")

received = {
    {
        id = "RIS_MajorStrategy_Network",
        read = true,
        time = 50,
    },
    {
        id = "RIS_MajorStrategy_Response",
        read = true,
        time = 100,
    },
    {
        id = "RIS_UnitSighting",
        read = true,
        time = 200,
        context = {
            type_id = Untranslated("JAZZ_Legion_Test"),
            unit_title = "frozen contact",
            dossier = "frozen dossier",
        },
    },
    {
        id = "RIS_NpcObit",
        read = true,
        time = 300,
        context = {
            name = "frozen opponent",
            npc_id = "LegacyNpc",
        },
    },
    {
        id = "RIS_EliteObit",
        read = true,
        time = 400,
        context = {
            name = "frozen elite",
            obit_key = "elite:session:LegacyElite",
        },
    },
    {
        id = "RIS_UnitSighting",
        read = true,
        time = 500,
        context = {
            unit_title = Untranslated("frozen unidentified contact"),
            dossier = Untranslated("frozen unidentified dossier"),
        },
    },
}
gv_ReceivedEmails = received
st.mail_queue = {
    { kind = "meet", type_id = "JAZZ_Legion_Test", ready_at = 1 },
    {
        kind = "obit",
        npc_id = "LegacyElite",
        obit_key = "elite:session:LegacyElite",
        ready_at = 1,
    },
}
st.strategy_observed = {}
st.strategy_delivered = {}
st.strategy_delivery_order = {}
st.next_strategy_at = 0
st.met_types = {}
st.obits_sent = {}
JAZZ_RIS_MigrateState()
assert(#st.mail_queue == 0,
    "received field mail was left duplicated in the pending queue")
assert(st.strategy_delivered.strategy_answer == 100
    and st.strategy_delivered.strategy_network == 50
    and st.strategy_delivery_order[1] == "strategy_network"
    and st.strategy_delivery_order[2] == "strategy_answer"
    and st.next_strategy_at == 2500,
    "Strategy inbox migration ignored the original delivery timestamp")
assert(received[3].context.unit_title == JAZZ_RIS_DOSSIERS.JAZZ_Legion_Test.title
    and received[3].context.type_id == "JAZZ_Legion_Test"
    and received[3].context.dossier == nil,
    "received sighting retained frozen prose after migration")
assert(received[4].context.name == gv_UnitData.LegacyNpc.Name
    and received[4].context.obit_key == "npc:LegacyNpc",
    "received obituary did not re-resolve its stable UnitData name")
assert(received[5].context.name == gv_UnitData.LegacyElite.Name
    and received[5].context.npc_id == "LegacyElite",
    "received elite obituary did not recover its session id")
assert(received[6].context.unit_title == JAZZ_RIS_EXTRA.legacy_contact
    and received[6].context.type_id == nil
    and received[6].context.dossier == nil,
    "unidentified legacy sighting retained an Untranslated frozen name")
assert(st.met_types.JAZZ_Legion_Test
    and st.obits_sent["npc:LegacyNpc"]
    and st.obits_sent["elite:session:LegacyElite"],
    "received field mail did not reconcile delivery state")
'''
    )


def test_dossier_delivery_gate() -> None:
    lua = LuaRuntime(unpack_returned_tuples=True)
    lua.execute(
        r'''
OnMsg = {}
empty_table = {}
gv_JAZZ_RIS = {
	kills = {},
	met_types = {},
	quest_met = {},
	battles = {},
}
JAZZ_RIS_KILL_THRESHOLD = 3
JAZZ_RIS_UI = {
	section_quest = "KEY",
	section_legion = "LEGION",
	empty_dossiers = "EMPTY",
	kills_progress = "KILLS <count>/3",
	dossier_locked = "LOCKED",
}
JAZZ_RIS_DOSSIERS = {
	JAZZ_Legion_Test = { title = "TYPE", body = "FULL BODY" },
}
JAZZ_RIS_QUEST_DOSSIERS = {}

function JAZZ_RIS_MigrateState()
	return gv_JAZZ_RIS
end

function sorted_pairs(rows)
	return next, rows, nil
end

function _InternalTranslate(value)
	return value
end

function T(value, text)
	if type(value) == "table" then
		local template = value[1]
		if type(template) == "string" then
			return string.gsub(template, "<count>", tostring(value.count or ""))
		end
		return template
	end
	return text or value
end

function ObjModified()
end
'''
    )
    lua.execute(_source("System_RIS_Browser.lua"))
    lua.execute(
        r'''
local st = gv_JAZZ_RIS

st.kills.JAZZ_Legion_Test = 1
local before_delivery = JAZZ_RIS_BuildDossiersText()
assert(not string.find(before_delivery, "TYPE", 1, true),
	"contact card appeared before its sighting mail was delivered")

st.kills.JAZZ_Legion_Test = 3
local threshold_before_delivery = JAZZ_RIS_BuildDossiersText()
assert(not string.find(threshold_before_delivery, "TYPE", 1, true),
	"full dossier appeared before its sighting mail was delivered")

st.met_types.JAZZ_Legion_Test = true
st.kills.JAZZ_Legion_Test = 2
local short_card = JAZZ_RIS_BuildDossiersText()
assert(string.find(short_card, "TYPE", 1, true), "delivered contact card stayed hidden")
assert(not string.find(short_card, "FULL BODY", 1, true),
	"full dossier appeared before the third confirmed kill")

st.kills.JAZZ_Legion_Test = 3
local full_card = JAZZ_RIS_BuildDossiersText()
assert(string.find(full_card, "FULL BODY", 1, true),
	"third confirmed kill did not reveal the full dossier")
'''
    )


def test_combat_autoresolve_snapshot() -> None:
    lua = LuaRuntime(unpack_returned_tuples=True)
    lua.execute(
        r'''
OnMsg = {}
empty_table = {}
Game = { CampaignTime = 3000, id = "test" }
GameState = {}
gv_CurrentSectorId = "A1"
gv_JAZZ_RIS = {
    kills = {},
    battles = {},
    dossiers = {},
    quest_met = {},
}
gv_Sectors = {
    A1 = { Id = "A1", Side = "enemy1", CombatHeat = 0 },
    B1 = { Id = "B1", Side = "enemy1", CombatHeat = 0 },
    D1 = { Id = "D1", Side = "enemy1", CombatHeat = 0 },
}
gv_Squads = {
    P = {
        UniqueId = "P",
        Side = "player1",
        CurrentSector = "A1",
        units = { "p1", "p2" },
    },
    E = {
        UniqueId = "E",
        Side = "enemy1",
        CurrentSector = "A1",
        units = { "e1", "e2" },
    },
    PB = {
        UniqueId = "PB",
        Side = "player1",
        CurrentSector = "B1",
        units = { "pb1" },
    },
    EB = {
        UniqueId = "EB",
        Side = "enemy1",
        CurrentSector = "B1",
        units = { "eb1" },
    },
    PD = {
        UniqueId = "PD",
        Side = "player1",
        CurrentSector = "D1",
        units = { "pd1" },
    },
    ED = {
        UniqueId = "ED",
        Side = "enemy1",
        CurrentSector = "D1",
        units = { "ed1" },
    },
}
gv_UnitData = {
    p1 = {
        session_id = "p1",
        class = "Merc",
        Squad = "P",
        HitPoints = 50,
        MaxHitPoints = 100,
    },
    p2 = {
        session_id = "p2",
        class = "Merc",
        Squad = "P",
        HitPoints = 100,
        MaxHitPoints = 100,
    },
    e1 = {
        session_id = "e1",
        class = "JAZZ_Legion_Test",
        Squad = "E",
        Name = "Enemy One",
        elite = true,
        HitPoints = 100,
        MaxHitPoints = 100,
    },
    e2 = {
        session_id = "e2",
        class = "JAZZ_Legion_Test",
        Squad = "E",
        Name = "Enemy Two",
        elite = true,
        HitPoints = 100,
        MaxHitPoints = 100,
    },
    pb1 = {
        session_id = "pb1",
        class = "Merc",
        Squad = "PB",
        HitPoints = 100,
        MaxHitPoints = 100,
    },
    eb1 = {
        session_id = "eb1",
        class = "Enemy",
        Squad = "EB",
        HitPoints = 100,
        MaxHitPoints = 100,
    },
    pd1 = {
        session_id = "pd1",
        class = "Merc",
        Squad = "PD",
        HitPoints = 100,
        MaxHitPoints = 100,
    },
    ed1 = {
        session_id = "ed1",
        class = "Enemy",
        Squad = "ED",
        HitPoints = 100,
        MaxHitPoints = 100,
    },
}
map_units = {}

function MapVar(name, value)
    rawset(_G, name, value)
end

function JAZZ_RIS_MigrateState()
    return gv_JAZZ_RIS
end

function GetSquadsInSector(sector_id)
    if sector_id == "B1" then
        return { gv_Squads.PB }, { gv_Squads.EB }
    end
    if sector_id == "D1" then
        return { gv_Squads.PD }, { gv_Squads.ED }
    end
    return { gv_Squads.P }, { gv_Squads.E }
end

function GetAllUnits()
    return map_units
end

function IsValid()
    return true
end

function ObjModified()
end
'''
    )
    lua.execute(_source("System_RIS_Combat.lua"))
    lua.execute(
        r'''
OnMsg.ConflictStart("A1")
assert(g_JAZZ_RIS_CombatSnaps.A1.player_start == 2,
    "satellite conflict missed friendly auto-resolve participants")
assert(g_JAZZ_RIS_CombatSnaps.A1.enemy_start == 2,
    "satellite conflict missed hostile auto-resolve participants")

map_units = {
    {
        session_id = "p1",
        class = "Merc",
        team = { player_team = true, side = "player1" },
        HitPoints = 50,
        MaxHitPoints = 100,
    },
    {
        session_id = "p2",
        class = "Merc",
        team = { player_team = true, side = "player1" },
        HitPoints = 100,
        MaxHitPoints = 100,
    },
    {
        session_id = "e1",
        class = "JAZZ_Legion_Test",
        team = { player_enemy = true, side = "enemy1" },
        HitPoints = 100,
        MaxHitPoints = 100,
    },
    {
        session_id = "e2",
        class = "JAZZ_Legion_Test",
        team = { player_enemy = true, side = "enemy1" },
        HitPoints = 100,
        MaxHitPoints = 100,
    },
}
OnMsg.CombatStart()
assert(g_JAZZ_RIS_CombatSnaps.A1.player_start == 2
    and g_JAZZ_RIS_CombatSnaps.A1.enemy_start == 2,
    "satellite and tactical views double-counted the same session ids")

OnMsg.ConflictStart("B1")
assert(g_JAZZ_RIS_CombatSnaps.A1 and g_JAZZ_RIS_CombatSnaps.B1,
    "a concurrent conflict replaced another sector's snapshot")
OnMsg.ConflictEnd(gv_Sectors.B1, false, true, false, "auto-resolve", false, true)
local remote = gv_JAZZ_RIS.battles[1]
assert(remote.sector_id == "B1"
    and remote.player_start == 1
    and remote.enemy_start == 1,
    "remote auto-resolve imported units from the loaded tactical map")
assert(g_JAZZ_RIS_CombatSnaps.A1,
    "resolving a remote conflict discarded the loaded sector snapshot")
local battle_count = #gv_JAZZ_RIS.battles
OnMsg.ConflictStart("B1")
OnMsg.ConflictEnd(gv_Sectors.B1, false, true, false, "auto-resolve", false, true)
assert(#gv_JAZZ_RIS.battles == battle_count + 1,
    "a new same-time conflict was mistaken for a duplicate ConflictEnd")
OnMsg.ConflictEnd(gv_Sectors.B1, false, true, false, "auto-resolve", false, true)
assert(#gv_JAZZ_RIS.battles == battle_count + 1,
    "a repeated ConflictEnd created a duplicate AAR")
OnMsg.ConflictEnd(gv_Sectors.D1, false, true, true, "auto-resolve", false, true)
assert(gv_JAZZ_RIS.battles[1].sector_id == "D1"
    and gv_JAZZ_RIS.battles[1].player_start == 1
    and gv_JAZZ_RIS.battles[1].enemy_start == 1,
    "missed ConflictStart fallback emitted an empty AAR")
map_units = {}

gv_UnitData.e1.HitPoints = 0
OnMsg.UnitDiedOnSector(gv_UnitData.e1, "A1")
gv_UnitData.p2.HitPoints = 60
gv_UnitData.e2.HitPoints = 40

OnMsg.ConflictEnd(gv_Sectors.A1, false, true, false, false, true, true)
local aar = gv_JAZZ_RIS.battles[1]
assert(aar and not aar.autoResolve,
    "surviving-merc auto-resolve branch was not reproduced")
OnMsg.AutoResolvedConflict("A1")
assert(aar.autoResolve,
    "AutoResolvedConflict did not repair the surviving-merc AAR marker")
assert(aar.player_start == 2 and aar.enemy_start == 2,
    "auto-resolve AAR lost starting strengths")
assert(aar.player_kia == 0 and aar.enemy_kia == 1,
    "auto-resolve AAR lost satellite death events")
assert(aar.player_wia == 1 and aar.enemy_wia == 1,
    "auto-resolve AAR lost surviving wounded units")
assert(#aar.elites == 2
    and aar.elites[1].fate == "killed"
    and aar.elites[2].fate == "wounded",
    "auto-resolve AAR lost named-opponent fates")
assert(gv_JAZZ_RIS.kills.JAZZ_Legion_Test == 1,
    "auto-resolve kill did not advance the confirmed-kill dossier count")
'''
    )


def test_combat_two_phase_tactical_snapshot() -> None:
    lua = LuaRuntime(unpack_returned_tuples=True)
    lua.execute(
        r'''
OnMsg = {}
empty_table = {}
Game = { CampaignTime = 4000, id = "test" }
GameState = {}
gv_CurrentSectorId = "C1"
gv_JAZZ_RIS = {
    kills = {},
    battles = {},
    dossiers = {},
    quest_met = {},
}
gv_Sectors = {
    C1 = { Id = "C1", Side = "enemy1", CombatHeat = 0 },
}
gv_Squads = {}
gv_UnitData = {}
gv_Quests = { UNRELATED = {} }
Quests = { UNRELATED = {} }

function combat_unit(id, side, hp)
    return {
        session_id = id,
        class = side == "player1" and "Merc" or "JAZZ_Legion_Test",
        team = {
            player_team = side == "player1",
            player_enemy = side == "enemy1",
            side = side,
        },
        HitPoints = hp,
        MaxHitPoints = 100,
    }
end

p1 = combat_unit("p1", "player1", 100)
p2 = combat_unit("p2", "player1", 100)
e1 = combat_unit("e1", "enemy1", 100)
e2 = combat_unit("e2", "enemy1", 100)
e2.Name = "Second phase officer"
e2.elite = true
e3 = combat_unit("e3", "enemy1", 50)
e3.Name = "Remaining commander"
e3.elite = true
e4 = combat_unit("e4", "enemy1", 100)
e4.conflict_ignore = true
map_units = { p1, e1 }
quest_active = true
elite_obits = 0

function MapVar(name, value)
    rawset(_G, name, value)
end

function JAZZ_RIS_MigrateState()
    return gv_JAZZ_RIS
end

function GetSquadsInSector()
    return {}, {}
end

function GetAllUnits()
    return map_units
end

function GetQuestsAssociatedWithSector()
    if quest_active then
        return {
            {
                preset = { id = "Q1" },
                state = { Clues = 3 },
                notes = { { Text = { 7005, "Collected <Clues> clues" } } },
            },
        }
    end
    return {}
end

function GetActiveQuest()
    return "UNRELATED"
end

function IsValid()
    return true
end

function ObjModified()
end

function JAZZ_RIS_EnqueueEliteObit()
    elite_obits = elite_obits + 1
end
'''
    )
    lua.execute(_source("System_RIS_Combat.lua"))
    lua.execute(
        r'''
OnMsg.CombatStart()
e1.HitPoints = 0
OnMsg.UnitDiedOnSector(e1, "C1")
map_units = { p1 }
OnMsg.CombatEnd()

map_units = { p1, p2, e2, e3, e4 }
OnMsg.CombatStart()
assert(g_JAZZ_RIS_CombatSnaps.C1.player_start == 2
    and g_JAZZ_RIS_CombatSnaps.C1.enemy_start == 3,
    "second tactical phase replaced or duplicated cumulative forces")

p1.HitPoints = 60
e2.HitPoints = 0
e2.team.player_enemy = false
e2.team.side = "enemyNeutral"
OnMsg.UnitDiedOnSector(e2, "C1")
map_units = { p1, p2, e3 }
OnMsg.CombatEnd()
e3.team.player_enemy = false
e3.team.side = "enemyNeutral"
quest_active = false
OnMsg.ConflictEnd(gv_Sectors.C1, false, true, true, false, false, false)

local aar = gv_JAZZ_RIS.battles[1]
assert(aar
    and aar.player_start == 2
    and aar.enemy_start == 3,
    "two-phase AAR lost cumulative starting forces")
assert(aar.player_kia == 0
    and aar.enemy_kia == 2
    and aar.player_wia == 1
    and aar.enemy_wia == 0,
    "two-phase AAR lost cumulative KIA/WIA")
assert(aar.hostiles_remain == true,
    "living map-placed hostile was omitted from the final warning")
assert(#aar.quest_ids == 1 and aar.quest_ids[1] == "Q1",
    "AAR lost its sector quest or imported an unrelated active quest")
assert(aar.quest_params.Q1.Clues == 3,
    "AAR did not preserve language-neutral quest-note parameters")
assert(#aar.elites == 2
    and aar.elites[1].fate == "killed"
    and aar.elites[2].fate == "threat",
    "named-opponent fate used an old wound or changed with post-capture diplomacy")
assert(elite_obits == 1,
    "recorded enemy side was ignored when queuing a death notice")
assert(gv_JAZZ_RIS.kills.JAZZ_Legion_Test == 2,
    "two-phase deaths did not advance confirmed-kill counters exactly once")
'''
    )


def test_legacy_aar_reconstruction() -> None:
    lua = LuaRuntime(unpack_returned_tuples=True)
    lua.execute(
        r'''
OnMsg = {}
empty_table = {}
gv_JAZZ_RIS = {}
gv_Sectors = {
    A1 = { Id = "A1" },
}
gv_UnitData = {
    NPC = {
        session_id = "NPC",
        Name = { 7002, "Current opponent name" },
    },
}
Quests = {
    Q1 = { DisplayName = { 7001, "Recovered assignment" } },
    Q2 = { DisplayName = { 7003, "Parameterized assignment" } },
}
JAZZ_RIS_EXTRA = {
    legacy_title = "ARCHIVED",
    legacy_body = "Partial record from <sector>.",
    legacy_body_time = "Partial timed record from <sector> at <time>.",
    auto_resolve = "REMOTE",
}
JAZZ_RIS_AAR = {
    headlines = {
        ["win|mid"] = { "RECOVERED WIN" },
    },
    quest = {
        one = "ASSIGNMENT <quest>: <note>",
        one_nonote = "ASSIGNMENT <quest>",
        many = "ASSIGNMENTS <quests>",
        active = "ACTIVE <quest>",
        none = "NO ASSIGNMENT",
    },
    forces = "FORCES <player>/<enemy>",
    character = {
        win = "OUTCOME WIN",
        loss = "OUTCOME LOSS",
        retreat = "OUTCOME RETREAT",
    },
    losses = "LOSSES <pkia>/<pwia>/<ekia>/<ewia>",
    sector = { line = "SECTOR <sector>" },
    weather = { default = "WEATHER" },
    intensity = { mid = "INTENSITY" },
    elite = { threat = "OPPONENT <name>" },
    closing = { noise = "CLOSE" },
}

function JAZZ_RIS_MigrateState()
    return gv_JAZZ_RIS
end

function GetSectorName()
    return "Alpha"
end

function _InternalTranslate(value)
    if type(value) == "table" and type(value[1]) == "number" then
        return value[2]
    end
    return value
end

function T(value, text)
    if type(value) ~= "table" then
        return { value, text }
    end
    local template = value[1]
    local result = type(template) == "table"
        and tostring(template[2] or "")
        or tostring(template or "")
    for key, replacement in pairs(value) do
        if type(key) == "string" then
            if type(replacement) == "table" then
                replacement = replacement[2] or replacement[1] or ""
            end
            result = string.gsub(result, "<" .. key .. ">", tostring(replacement))
        end
    end
    return result
end

function FormatCampaignTime()
    return "D3-H4"
end

function ObjModified()
end
'''
    )
    lua.execute(_source("System_RIS_Browser.lua"))
    lua.execute(
        r'''
local title, body = JAZZ_RIS_RenderBattle({
    kind = "legacy",
    sector_id = "A1",
    time = 123,
    outcome = "win",
    quest_ids = { "Q1" },
    quest_linked = false,
    player_start = 3,
    enemy_start = 4,
    player_kia = 0,
    player_wia = 1,
    enemy_kia = 3,
    enemy_wia = 1,
    autoResolve = true,
})
assert(title == "RECOVERED WIN",
    "legacy AAR ignored its preserved outcome")
assert(string.find(body, "Alpha", 1, true)
    and string.find(body, "Recovered assignment", 1, true),
    "legacy AAR ignored preserved sector or quest references")
assert(string.find(body, "D3-H4", 1, true)
    and string.find(body, "ACTIVE Recovered assignment", 1, true),
    "legacy AAR ignored preserved time or active-quest provenance")
assert(string.find(body, "FORCES 3/4", 1, true)
    and string.find(body, "LOSSES 0/1/3/1", 1, true)
    and string.find(body, "OUTCOME WIN", 1, true)
    and string.find(body, "REMOTE", 1, true),
    "legacy AAR ignored preserved combat facts")

local _, current_body = JAZZ_RIS_RenderBattle({
    record_version = 2,
    sector_id = "A1",
    outcome = "win",
    headline_key = "win|mid",
    headline_index = 1,
    weather_key = "default",
    intensity_key = "mid",
    character_key = "win",
    closing_key = "noise",
    quest_ids = { "Q2" },
    quest_sources = { Q2 = "badge" },
    quest_notes = { Q2 = { 7004, "Collected <Clues> clues" } },
    quest_params = { Q2 = { Clues = 3 } },
    quest_linked = true,
    player_start = 1,
    enemy_start = 1,
    player_kia = 0,
    player_wia = 0,
    enemy_kia = 0,
    enemy_wia = 0,
    elites = {
        {
            handle = "session:NPC",
            session_id = "NPC",
            name_ref = "Frozen old-language name",
            fate = "threat",
        },
    },
})
assert(string.find(current_body, "Current opponent name", 1, true)
    and not string.find(current_body, "Frozen old-language name", 1, true),
    "AAR preferred frozen prose over a current stable UnitData name")
assert(string.find(current_body, "Collected 3 clues", 1, true),
    "AAR rendered a quest note without its captured substitution values")
'''
    )


def main() -> int:
    tests = (
        test_lua_syntax,
        test_strategy_visibility_gates,
        test_mail_migration_and_desk,
        test_dossier_delivery_gate,
        test_combat_autoresolve_snapshot,
        test_combat_two_phase_tactical_snapshot,
        test_legacy_aar_reconstruction,
    )
    for test in tests:
        test()
        print(f"PASS {test.__name__}")
    print(f"PASS R.I.S. targeted contract ({len(tests)} tests)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
