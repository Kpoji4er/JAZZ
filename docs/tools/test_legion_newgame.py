"""Executable Lua contract tests for PROGRESSION-001 (requires Python lupa)."""
from pathlib import Path
from lupa import LuaRuntime

ROOT = Path(__file__).resolve().parents[2]
BOOT = r'''
empty_table = {}; const = {Scale={day=86400,h=3600}}; OnMsg={}
Max=math.max; Min=math.min; sorted_pairs=pairs
function table.find(t,v) for i,x in ipairs(t) do if x==v then return i end end end
Game={CampaignTime=1000000,game_rules={}}; nomaps=false
gv_Sectors={}; gv_Quests={JAZZ_LegionTier={JAZZ_Legion_Tier=11}}
Groups={}; events={}; loot=0; mail=0
function GameVar(k,f) _G[k]=f() end
function JAZZ_NoMapsIsActive() return nomaps end
function QuestGetState(k) return gv_Quests[k] end
function GetQuestVar(k,v) return gv_Quests[k] and gv_Quests[k][v] end
function SetQuestVar(q,k,v) q[k]=v end
function RegenerateLegionLoot() loot=loot+1 end
function JAZZ_RIS_OnTierRaised() mail=mail+1 end
function Msg(...) events[#events+1]={...} end
function T(id,text) return text end
function Untranslated(x) return x end
'''


def runtime():
    lua = LuaRuntime(unpack_returned_tuples=True)
    lua.execute(BOOT)
    lua.execute((ROOT / 'Code/LegionTierProgression.lua').read_text(encoding='utf-8-sig'))
    return lua


TIERS = [11, 12, 13, 21, 22, 23, 24, 25, 31, 32, 33]
cases = 0
for nomaps in (False, True):
    for speed in (1, 2, 4):
        for start in TIERS:
            lua = runtime()
            g = lua.globals()
            g.nomaps = nomaps
            g.Game.game_rules[f'JAZZ_LegionStart{start}'] = True
            g.Game.game_rules[f'JAZZ_LegionClock{speed}'] = True
            g.OnMsg.NewGame()
            assert g.JAZZ_GetLegionTier() == start
            assert len(g.events) == 0 and g.mail == 0 and g.loot == 0
            now = g.Game.CampaignTime
            elapsed = 0
            for index in range(TIERS.index(start), len(TIERS)-1):
                outgoing = TIERS[index]
                days = (3 if outgoing < 20 else 14) if nomaps else (7 if outgoing < 20 else 30)
                elapsed += days * 86400 // speed
                g.Game.CampaignTime = now + elapsed - 1
                g.JAZZ_UpdateLegionTierProgression()
                assert g.JAZZ_GetLegionTier() == outgoing
                g.Game.CampaignTime += 1
                g.JAZZ_UpdateLegionTierProgression()
                assert g.JAZZ_GetLegionTier() == TIERS[index+1]
                count = len(g.events)
                g.JAZZ_UpdateLegionTierProgression()
                assert len(g.events) == count
                cases += 1
            g.Game.CampaignTime = now + 10000*86400
            g.JAZZ_UpdateLegionTierProgression()
            assert g.JAZZ_GetLegionTier() == 33
            assert g.JAZZ_ComputeLegionTimedTier(now-1, now, start, speed, nomaps) == start
            assert g.JAZZ_ComputeLegionTimedTier(now+10000*86400, now, start, speed, nomaps) == 33

for nomaps in (False, True):
    for start in TIERS:
        lua = runtime(); g = lua.globals(); g.nomaps = nomaps
        g.Game.game_rules[f'JAZZ_LegionStart{start}'] = True
        g.OnMsg.NewGame()
        assert g.JAZZ_GetLegionTier() == start
        days = (3 if start < 20 else 14) if nomaps else (7 if start < 20 else 30)
        g.Game.CampaignTime += days * 86400
        g.JAZZ_UpdateLegionTierProgression()
        cap = {1: 13, 2: 25, 3: 33}[start//10]
        assert g.JAZZ_GetLegionTier() == min(start+1, cap)
        cases += 1

lua = runtime()
lua.execute(r'''
-- Real QuestGetState creates state lazily: tier must exist before initial squads.
local read_quest=QuestGetState
function QuestGetState(id)
  if not gv_Quests[id] then gv_Quests[id]={} end
  return gv_Quests[id]
end
gv_Quests={}; Game.game_rules.JAZZ_LegionStart31=true
OnMsg.NewGame(); assert(gv_Quests.JAZZ_LegionTier.JAZZ_Legion_Tier==31)
QuestGetState=read_quest; Game.game_rules={}; gv_Quests.JAZZ_LegionTier.JAZZ_Legion_Tier=11
-- Campaign major transitions reset the sub timer after a raised start.
Game.game_rules.JAZZ_LegionStart13=true; OnMsg.NewGame()
gv_Sectors.A1={Id="A1",Side="player1",Passability="Land"}
JAZZ_UpdateLegionTierForMaps(); assert(JAZZ_GetLegionTier()==21)
Game.CampaignTime=Game.CampaignTime+30*86400
JAZZ_UpdateLegionTierForMaps(); assert(JAZZ_GetLegionTier()==22)
-- Bootstrap: both states were seeded even before NoMaps became active.
Game.game_rules={JAZZ_LegionStart24=true,JAZZ_LegionClock2=true}
gv_Quests.JAZZ_LegionTier=nil; OnMsg.NewGame()
assert(gv_JAZZ_LegionTierNoMaps.start_tier==24)
nomaps=true; gv_Quests.JAZZ_LegionTier={JAZZ_Legion_Tier=11}
events={}; JAZZ_UpdateLegionTierProgression()
assert(JAZZ_GetLegionTier()==24 and #events==0)
Game.CampaignTime=Game.CampaignTime+7*86400
JAZZ_UpdateLegionTierProgression(); assert(JAZZ_GetLegionTier()==25 and #events==1)
-- Existing save: no NewGame handler, default rules do not reinitialize its tier.
Game.game_rules={}; nomaps=false; gv_Sectors={}
gv_JAZZ_LegionTierMaps={schema=1,major=2,major_started_at=Game.CampaignTime}
gv_Quests.JAZZ_LegionTier.JAZZ_Legion_Tier=24
OnMsg.LoadGame(); assert(JAZZ_GetLegionTier()==24)
-- Time mode ignores early mainland/mine/story unlocks.
Game.game_rules={JAZZ_LegionClock1=true}; gv_Quests.JAZZ_LegionTier.JAZZ_Legion_Tier=11
OnMsg.NewGame()
for i=1,5 do gv_Sectors["A"..i]={Side="player1",Mine=true} end
gv_Quests["04_Betrayal"]={WorldFlipDone=true}
JAZZ_UpdateLegionTierProgression(); assert(JAZZ_GetLegionTier()==11)
nomaps=true; JAZZ_UpdateLegionTierProgression(); assert(JAZZ_GetLegionTier()==11)
''')

# UI callbacks and rule registration, including install twice and guest guard.
lua.execute(r'''
Game=false; NewGameObj={game_rules={}}; netInGame=false
GameRuleDefs={}; XTemplates={NewGameMenuGameRules={{},{},{},{}}}
function PlaceObj(class, props)
  local obj=props
  if class=="XTemplateTemplate" then obj={} for i=1,#props,2 do obj[props[i]]=props[i+1] end end
  if class=="GameRuleDef" then GameRuleDefs[obj.id]=obj end
  return obj
end
function NetIsHost() return false end
function ForEachPreset() end
''')
lua.execute((ROOT/'Code/GameRules_HideAdvanced.lua').read_text(encoding='utf-8-sig'))
lua.execute(r'''
OnMsg.DataLoaded(); OnMsg.ModsReloaded()
assert(#XTemplates.NewGameMenuGameRules==6)
assert(GameRuleDefs.JAZZ_LegionStart33 and GameRuleDefs.JAZZ_LegionClock4)
local function noop() end
local row={Id="idJAZZ_LegionStart",idName={SetText=noop},idOnOff={SetText=noop},SetRolloverTitle=noop,SetRolloverText=noop,SetEnabled=noop}
local entry=XTemplates.NewGameMenuGameRules[3]
for i=1,10 do entry.OnPress(row) end
local tier=JAZZ_GetLegionCampaignSettings(NewGameObj.game_rules); assert(tier==33)
entry.OnPress(row); tier=JAZZ_GetLegionCampaignSettings(NewGameObj.game_rules); assert(tier==11)
row.Id="idJAZZ_LegionClock"; entry=XTemplates.NewGameMenuGameRules[4]
for _,expected in ipairs({1,2,4,0}) do entry.OnPress(row) local _,speed=JAZZ_GetLegionCampaignSettings(NewGameObj.game_rules) assert(speed==expected) end
netInGame=true; entry.OnPress(row)
local _,speed=JAZZ_GetLegionCampaignSettings(NewGameObj.game_rules); assert(speed==0)
''')
print(f'PASS: {cases} timer/campaign boundaries; initialization, bootstrap, old saves, event deduplication, UI cycle/install/guest guard')
