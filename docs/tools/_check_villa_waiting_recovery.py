"""Run real K4 module and vanilla EnterConflict against isolated campaign fixtures."""
from pathlib import Path
from lupa import LuaRuntime

root = Path(__file__).resolve().parents[2]
game = Path((root/'.ja3-root.local').read_text().strip())
source = (game/'ModTools/Src/Lua/Satellite/SatelliteConflict.lua').read_text(encoding='utf-8')
enter = source[source.index('function EnterConflict('):source.index('function EnemyWantsToWait(')]
lua = LuaRuntime()
lua.execute('''
empty_table={}; OnMsg={}; Game={CampaignTime=0}; const={Scale={h=60,min=1},Satellite={SectorTravelTimeBase=100,SectorTravelTime=1000,SectorTravelTimeEnemy=1000,SectorTravelTimeWater=1000}}; gv_CurrentSectorId='K4'
function GameVar(k,f) _G[k]=f() end
function SatelliteSquadWaitInSector(s,t) s.wait_in_sector=t end
function AnyNonWaitingConflict() for _,id in ipairs(g_ConflictSectors) do if gv_Sectors[id].conflict and not gv_Sectors[id].conflict.waiting then return true end end return false end
function table.remove_value(t,v) for i=#t,1,-1 do if t[i]==v then table.remove(t,i) end end end
function procall(f,...) return f(...) end
function IsKindOf(u) return u.is_unit end
function Msg() end
function ObjModified() end
function UpdateEntranceAreasVisibility() end
function ExecuteSectorEvents() end
function GetSquadsInSectorCombined() return {} end
function IsConflictMode(id) return gv_Sectors[id].conflict end
function EnemyWantsToWait() return false end -- Distant columns outside vanilla threshold.
function PauseCampaignTime() paused=true end
function ResumeCampaignTime() paused=false end
function GetSectorSquadsFromSide(id)
 local out={}
 for _,s in pairs(gv_Squads) do
  if s.CurrentSector==id and s.Side=='enemy1' then out[#out+1]=s end
 end
 return out
end
function SendSatelliteSquadOnRoute(s,target)
 routes=routes+1;s.route={{target}}
end
function GenerateEnemySquad(def,sector)
 generated=generated+1
 local id=100+generated
 gv_Squads[id]={UniqueId=id,CurrentSector=sector,Side='enemy1',enemy_squad_def=def,units={'enemy'}}
 return id
end
function ForceEnterConflictEffect(s,mode,...)
 EnterConflict(s,nil,mode,...)
end
function setup()
 gv_Quests={Jazz_VillaCounterAttack={Given=true}}
 gv_Sectors={K4={Id='K4',Side='player1'},K3={Id='K3',Side='enemy1'},I7={Side='enemy1'}}
 gv_Squads={[1]={UniqueId=1,CurrentSector='K3',Side='enemy1',units={'enemy'},enemy_squad_def='JAZZ_Legion_VillaAttackers_K3'}}
 gv_CustomQuestIdToSquadId={};g_ConflictSectors={};g_Units={};g_Combat=false;gv_JAZZ_VillaDepartureWaits={};Game.CampaignTime=0
 gv_Squads[2]={UniqueId=2,Side='player1',CurrentSector='K4',units={'merc'}}
 generated=0;routes=0;paused=false
end
''')
lua.execute(enter)
lua.execute((root.parent/'jazz-maps/Code/System_VillaCounterAttack.lua').read_text(encoding='utf-8'))
lua.execute('''
setup();Jazz_VillaCounterAttack_Start()
assert(generated==1 and routes==2 and not gv_Sectors.K4.conflict and not paused)
assert(gv_Squads[2].wait_in_sector and gv_JAZZ_VillaDepartureWaits[2])
Jazz_VillaCounterAttack_Start();assert(generated==1 and routes==2)
Game.CampaignTime=180;OnMsg.SatelliteTick();assert(gv_Squads[2].wait_in_sector>Game.CampaignTime)
-- Rebuild unsaved tags; clear only the old artificial conflict, no victory event.
g_JAZZ_VillaAttackSquadIds=false;g_JAZZ_VillaAttackDefs=false
EnterConflict(gv_Sectors.K4,nil,'defend',true,true,'InitialConflict','force')
assert(paused)
OnMsg.LoadGame()
assert(generated==1 and routes==2 and g_JAZZ_VillaAttackSquadIds[1] and not paused)
assert(not gv_Sectors.K4.conflict and not gv_Sectors.K4.ForceConflict)
-- Arrival before native conflict must retain the hold.
gv_Squads[101].CurrentSector='K4';gv_Squads[101].route=false
OnMsg.SatelliteTick();assert(gv_Squads[2].wait_in_sector)
EnterConflict(gv_Sectors.K4,nil,'defend')
OnMsg.SatelliteTick()
assert(paused and gv_Sectors.K4.conflict and gv_Squads[2].wait_in_sector)
gv_Quests.Jazz_VillaCounterAttack.SiegeCombat=true;g_Combat={}
OnMsg.SatelliteTick();assert(gv_Squads[2].wait_in_sector)
gv_Quests.Jazz_VillaCounterAttack.Completed=true
OnMsg.SatelliteTick();assert(not gv_Squads[2].wait_in_sector)
g_Combat=false
setup();gv_Sectors.K5={Id='K5',conflict={waiting=false}};g_ConflictSectors={'K5'}
EnterConflict(gv_Sectors.K4,nil,'defend',true,true,'InitialConflict','force')
Jazz_VillaCounterAttack_Start();assert(paused and not gv_Sectors.K4.conflict)
-- Preserve a map-spawned enemy encounter.
setup();g_Units={{is_unit=true,IsDead=function() return false end,team={side='enemy1'}}}
EnterConflict(gv_Sectors.K4,nil,'defend',true,true,'InitialConflict','force')
Jazz_VillaCounterAttack_Start();assert(paused and gv_Sectors.K4.conflict)
for _,flag in ipairs({'Completed','Failed','SiegeCombat'}) do
 setup();gv_Quests.Jazz_VillaCounterAttack[flag]=true
 OnMsg.LoadGame();assert(generated==0 and routes==0)
end
-- Restore earlier waits, release on cancellation, respect a replacement wait.
setup();gv_Squads[2].wait_in_sector=5000;Jazz_VillaCounterAttack_Start()
gv_Quests.Jazz_VillaCounterAttack.Failed=true;OnMsg.SatelliteTick()
assert(gv_Squads[2].wait_in_sector==5000)
setup();Jazz_VillaCounterAttack_Start();gv_Squads[2].wait_in_sector=7777
gv_Quests.Jazz_VillaCounterAttack.Completed=true;OnMsg.SatelliteTick()
assert(gv_Squads[2].wait_in_sector==7777)
setup();Jazz_VillaCounterAttack_Start()
for _,s in pairs(gv_Squads) do s.route=false end
OnMsg.SatelliteTick();assert(not gv_Squads[2].wait_in_sector)
setup();gv_CustomQuestIdToSquadId.VillaAttackers_Ernie=777
Jazz_VillaCounterAttack_Start();assert(generated==0)
''')
# Execute the actual core travel calculation: unchanged baseline and scoped x5.
travel=(root/'Code/SatelliteSquad.lua').read_text(encoding='utf-8')
travel=travel[travel.index('function GetSectorTravelTime('):travel.index('function NetSyncEvents.SetArrivingMercSector(')]
lua.execute('''
function AreAdjacentSectors() return true end
function IsSectorUnderground() return false end
function SectorTravelBlocked() return false end
function AreSectorsSameCity() return false end
function HasRoad() return false end
function IsRiverSector() return false end
function DivCeil(a,b) return math.ceil(a/b) end
function MulDivRound(a,b,c) return math.floor(a*b/c+0.5) end
SectorTerrainTypes={Plain={TravelMod=100}}
''')
lua.execute(travel)
lua.execute('''
setup();Jazz_VillaCounterAttack_Start()
gv_Sectors.I7.TerrainType='Plain';gv_Sectors.K4.TerrainType='Plain'
gv_UnitData={enemy={Squad=101}}
local total,a,b=GetSectorTravelTime('I7','K4',nil,{'enemy'},nil,nil,'enemy1')
assert(total==400 and a==200 and b==200)
gv_Squads[101].enemy_squad_def='OrdinaryEnemy'
assert(GetSectorTravelTime('I7','K4',nil,{'enemy'},nil,nil,'enemy1')==2000)
gv_Squads[101].enemy_squad_def='JAZZ_Legion_VillaAttackers_Ernie'
gv_Quests.Jazz_VillaCounterAttack.Completed=true
assert(GetSectorTravelTime('I7','K4',nil,{'enemy'},nil,nil,'enemy1')==2000)
''')
print('PASS: no prep conflict; owned waits/recovery/release; real enemies/other conflicts; scoped Ernie x5')
