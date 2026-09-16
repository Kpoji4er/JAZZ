"""MED-008: protected quest actors, lethal ordinary actors; isolated Lua harness."""
from pathlib import Path
from lupa import LuaRuntime

source = (Path(__file__).resolve().parents[2] / 'Code/Systems_Medicine.lua').read_text(encoding='utf-8')
body = source[source.index('local function lJazzInfectionProtected('):source.index('function JazzWoundInfectedProgressOnNewHour(')]
timer = source[source.index('function JazzInitWoundInfectedProgressTimer('):source.index('-- Instance template props')]
lua = LuaRuntime()
lua.execute('''
Game={CampaignTime=100}; const={Scale={h=60}}; JazzWoundInfectedCheckIntervalHours=16
JazzWoundInfectedSurviveChance=40
function IsValid(u) return u.live end
function T(t) return t end
function CombatLog() logs=logs+1 end
function Msg() end
function NetUpdateHash() end
function ObjModified() end
function RemoveUnitFromSquad() removed=removed+1 end
function CheckGameOver() end
function JazzClearWoundInfected() cleared=cleared+1 end
function lJazzWoundInfectedTargets(u) return g_Units[u.session_id],gv_UnitData[u.session_id] end
function make(live)
 local e={SetParameter=function(self,k,v) self[k]=v end}
 return {session_id='x',HitPoints=50,HireStatus='Hired',live=live,
  IsDead=function() return false end, Random=function() return roll end,
  GetStatusEffect=function() return e end,
  Die=function(self) died=died+1; self.HitPoints=0 end}
end
function setup()
 logs=0;died=0;removed=0;cleared=0;roll=99
 u=make(true);ud=make(false);g_Units={x=u};gv_UnitData={x=ud};gv_Squads={}
end
''')
lua.execute(timer + body)
lua.execute('''
for _,flag in ipairs({'ImportantNPC','villain','immortal'}) do
 for _,where in ipairs({'live','data'}) do
  setup(); local obj=where=='live' and u or ud; obj[flag]=true
  assert(JazzWoundInfectedResolveProgressCheck(ud)=='protected')
  assert(JazzKillMercFromInfection(u)==false)
  assert(died==0 and logs==0 and removed==0 and ud.HitPoints==50 and u.HitPoints==50)
  assert(u:GetStatusEffect().next_check_time==1060)
  assert(ud:GetStatusEffect().next_check_time==1060)
 end
end
setup();g_Units={};ud.ImportantNPC=true
assert(JazzWoundInfectedResolveProgressCheck(ud)=='protected' and removed==0)
setup(); assert(JazzWoundInfectedResolveProgressCheck(u)=='death' and died==1)
setup();g_Units={};assert(JazzWoundInfectedResolveProgressCheck(ud)=='death')
assert(ud.HitPoints==0 and ud.HireStatus=='Dead' and removed==1)
setup();ud.ImportantNPC=true;ud.IsMercenary=true
assert(JazzWoundInfectedResolveProgressCheck(u)=='death' and died==1)
setup();ud.ImportantNPC=true;ud.Squad=1;gv_Squads[1]={Side='player1'}
assert(JazzWoundInfectedResolveProgressCheck(u)=='death' and died==1)
setup();ud.IsMercenary=true;ud.immortal=true
assert(JazzWoundInfectedResolveProgressCheck(u)=='protected')
setup();roll=0;assert(JazzWoundInfectedResolveProgressCheck(u)=='survive' and cleared==1)
setup();u.IsDead=function() return true end
assert(JazzWoundInfectedResolveProgressCheck(u)==false and died==0)
''')
print('PASS: quest/immortal protection, twin timers, ordinary/player deaths, recovery, dead guard')
