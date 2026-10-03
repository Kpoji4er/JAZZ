"""Execute production convoy functions with deterministic engine stubs (requires lupa).

Run from jazz: python docs/tools/_check_convoy_lifecycle.py
Does not open or mutate a game save. Engine integration remains a live-test concern.
"""
from pathlib import Path
import re
from lupa import LuaRuntime

ROOT = Path(__file__).resolve().parents[2]
SOURCE = (ROOT / "Code/Guardpost_Patrols.lua").read_text(encoding="utf-8")


def function(name):
    start = SOURCE.index(f"local function {name}(")
    end = re.search(r"\n(?:local )?function ", SOURCE[start + 1:])
    return SOURCE[start:start + 1 + end.start() if end else len(SOURCE)].replace(
        "local function ", "function ", 1)


lua = LuaRuntime()
assert lua.eval("function(s) local f,e=load(s); return e end")(SOURCE) is None
lua.execute('''
empty_table = {}; Min = math.min; Max = math.max
function sorted_pairs(t)
  local keys = {}; for k in pairs(t) do keys[#keys+1] = k end
  table.sort(keys); local n = 0
  return function() n=n+1; local k=keys[n]; if k then return k,t[k] end end
end
function lNow() return now end
function lHourScale() return 1 end
function ObjModified() end
function JAZZ_IsLegionSide(s) return s == 'enemy1' end
function IsSquadTravelling(s) return s.travel end
function IsConflictMode(s) return conflicts[s] end
function lPayloadMoney(p) return p and p.money or 0 end
function lSetRoute(s,t)
  routes=routes+1
  if s.CurrentSector == t then return 'arrived' end
  if path then s.travel=true; return true end
  return false
end
function lGetRegionPreset(id) return {} end
function lAddMajorMoney(r,region,n) r.major.money=r.major.money+n end
function lClearTaggedMoneyCargo() end
function lNoteMajorDelivery() end
function lSyncSharedOutpostResources() end
function lGatherRecruitCargoIds(s,ids) return ids or {} end
function lStripRecruitedUnits(s,ids) return #ids,{} end
function lAddMajorManpower(r,region,n) r.major.manpower=r.major.manpower+n end
function lBeginReturn(r,s,st)
  if s.CurrentSector == st.home_sector then
    st.task=false; st.state='resting'
  else
    st.task={task_type='return',target_sector=st.home_sector}; st.state='returning'
  end
end
function RemoveSquad(s) removed=removed+1; gv_Squads[s.UniqueId]=nil end
function lConfig(r,key,default) return default end
function MulDivRound(a,b,c) return math.floor(a*b/c+0.5) end
function lOutpostMoneyCapacity() return 120000 end
function lIsNeediestSupplyOutpost() return true end
function lIsNeediestManpowerOutpost() return true end
function lHasAvoidPlayerRoute() return path end
function lEnsureMoneyCargo() return true end
function lRecruitUnitTemplate() return 'Recruit' end
function lAddRecruitUnitsToSquad() return {'recruit1','recruit2'} end
function lEscortUnitTemplates() return {} end
function lSpawnManaged() spawned=spawned+1; return false end
function reset()
  now=24; routes=0; removed=0; spawned=0; path=false; conflicts={}
  gv_SatelliteView=true; gv_CurrentSectorId='A20'; gv_Squads={}
  gv_Sectors={A20={Side='enemy1'}, B2={Side='enemy1'}}
  root={major={hq_sector='A20',money=100000,manpower=100},squads={},
    outposts={B2={sector_id='B2',region_id='new',enabled=true,money=0,manpower=0}}}
end
function add(id,role,state,home,task,payload)
  local s={UniqueId=id,CurrentSector='A20',units={}}
  local st={role=role,state=state,home_sector=home or 'A20',region_id='new',
    task=task or false,payload=payload or {},missions_left=1}
  gv_Squads[id]=s; root.squads[id]=st; return s,st
end
''')
for name in ("lIsMajorInboundConvoyTask", "lStartMajorConvoyUnloading", "lOnSquadArrived",
             "lRetireSquad", "lMaintainConvoys", "lTickMajorConvoyHandling", "lActiveRole",
             "lFindIdleHomeRole", "lTrySupplyConvoy", "lTryManpowerConvoy"):
    lua.execute(function(name))

CASES = {
    "delivery and return credit cargo only once": '''
reset()
local s,st=add(1,'supply','working','B2',
 {task_type='supply',target_sector='B2',phase='unloading',hold_until=now},{money=12000})
s.CurrentSector='B2'; lTickMajorConvoyHandling(root)
assert(root.outposts.B2.money==12000 and st.payload.money==0 and st.home_sector=='A20')
assert(st.task.task_type=='return')
s.CurrentSector='A20'; lOnSquadArrived(root,s,st)
lMaintainConvoys(root); lTickMajorConvoyHandling(root)
assert(root.outposts.B2.money==12000 and root.major.money==100000)
assert(st.state=='resting')
reset(); root.outposts.B2.enabled=false
local s,st=add(1,'manpower','orphaned','B2',
 {task_type='manpower',target_sector='B2'}, {manpower=2,recruited_ids={'a','b'}})
lMaintainConvoys(root); lMaintainConvoys(root)
assert(root.major.manpower==102 and st.payload.manpower==0 and #st.payload.recruited_ids==0)
''',
    "blocked loading retries and departs": '''
reset()
local s,st=add(1,'supply','working','B2',
  {task_type='supply',target_sector='B2',phase='loading',hold_until=now},{money=12000})
for i=1,48 do
 lTickMajorConvoyHandling(root)
 assert(st.state=='working' and st.task.phase=='loading' and st.payload.money==12000)
 now=now+1
end
assert(routes==48); path=true; lTickMajorConvoyHandling(root)
assert(st.state=='en_route' and st.task.hold_until==nil and s.travel)
''',
    "old orphan and return recover": '''
reset()
local s,st=add(1,'supply','orphaned','B2',
 {task_type='supply',target_sector='B2',phase='en_route'},{money=12000})
lMaintainConvoys(root); assert(st.state=='orphaned' and st.payload.money==12000)
path=true; lMaintainConvoys(root); assert(st.state=='en_route' and s.travel)
reset()
local s,st=add(1,'shipment','orphaned','B2',{task_type='return',target_sector='B2'})
path=true; lMaintainConvoys(root); assert(st.state=='returning' and s.travel)
''',
    "captured destination refunds once": '''
reset(); root.outposts.B2.enabled=false
local s,st=add(1,'supply','working','B2',
 {task_type='supply',target_sector='B2',phase='loading',hold_until=now},{money=12000})
lMaintainConvoys(root)
assert(st.home_sector=='A20' and st.state=='resting' and st.payload.money==0)
assert(root.major.money==112000)
lMaintainConvoys(root); assert(root.major.money==112000)
''',
    "arrival does not extend unloading": '''
reset()
local s,st=add(1,'supply','en_route','B2',{task_type='supply',target_sector='B2'})
s.CurrentSector='B2'; lOnSquadArrived(root,s,st)
assert(st.task.hold_until==36)
now=30; lOnSquadArrived(root,s,st); assert(st.task.hold_until==36)
''',
    "legacy HQ pile bounded and idempotent": '''
reset()
for i=1,40 do add(i,i%2==0 and 'supply' or 'manpower','resting') end
lMaintainConvoys(root); assert(removed==38 and root.squads[1] and root.squads[2])
lMaintainConvoys(root); assert(removed==38)
for i=41,60 do add(i,i%2==0 and 'supply' or 'manpower','ready_for_orders') end
lMaintainConvoys(root); assert(removed==58)
''',
    "cargo and active escorts preserved": '''
reset(); add(1,'supply','resting'); add(2,'supply','resting',nil,nil,{money=500})
add(3,'manpower','resting'); add(4,'manpower','resting',nil,nil,{manpower=2})
add(5,'manpower','resting',nil,nil,{recruited_ids={'r'}})
local s=add(6,'supply','resting'); s.travel=true
add(7,'shipment','resting'); add(8,'major','resting')
add(9,'supply','working','B2',{task_type='supply',target_sector='B2',phase='loading'})
add(10,'supply','resting','B2')
lMaintainConvoys(root); assert(removed==0)
''',
    "battle tactical and lost HQ protected": '''
for _,mode in ipairs({'conflict','tactical','captured'}) do
 reset(); add(1,'supply','resting'); add(2,'supply','resting')
 if mode=='conflict' then conflicts.A20=true
 elseif mode=='tactical' then gv_SatelliteView=false
 else gv_Sectors.A20.Side='player1' end
 lMaintainConvoys(root); assert(removed==0)
end
''',
    "no route means no ordinary supply spawn": '''
reset(); lTrySupplyConvoy(root,{}, {region_id='new'},root.outposts.B2)
assert(spawned==0 and root.major.money==100000)
''',
    "active delivery blocks reuse for both roles": '''
for _,role in ipairs({'supply','manpower'}) do
 reset(); path=true
 add(1,role,'working','B2',{task_type=role,target_sector='B2'})
 local s,st=add(2,role,'ready_for_orders')
 local fn=role=='supply' and lTrySupplyConvoy or lTryManpowerConvoy
 assert(not fn(root,{}, {region_id='new'},root.outposts.B2))
 assert(st.home_sector=='A20' and st.state=='ready_for_orders' and spawned==0)
end
''',
    "reuse adopts recipient region and charges once": '''
for _,role in ipairs({'supply','manpower'}) do
 reset(); path=true
 local s,st=add(1,role,'ready_for_orders'); st.region_id='old'
 local fn=role=='supply' and lTrySupplyConvoy or lTryManpowerConvoy
 assert(fn(root,{}, {region_id='new'},root.outposts.B2))
 assert(st.region_id=='new' and st.home_sector=='B2' and st.state=='working')
 assert(not fn(root,{}, {region_id='new'},root.outposts.B2))
 assert(spawned==0)
 if role=='supply' then assert(root.major.money==88000)
 else assert(root.major.manpower==98) end
end
''',
}
for name, case in CASES.items():
    lua.execute(case)
    print(f"PASS: {name}")
print(f"PASS: Lua syntax and {len(CASES)} convoy lifecycle scenarios (offline engine stubs)")
