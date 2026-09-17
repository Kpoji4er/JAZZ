"""Lua-harness: actual vanilla Update plus JAZZ emplacement wrapper.

Not an in-game test. Requires lupa and .ja3-root.local.
"""
from pathlib import Path
from lupa import LuaRuntime

root = Path(__file__).resolve().parents[2]
game = Path((root / ".ja3-root.local").read_text().strip())
candidates = (
    game / "ModTools/Src/Lua/Tactical/Emplacement.lua",
    game / "Lua/Tactical/Emplacement.lua",
)
vanilla_path = next((path for path in candidates if path.is_file()), None)
if vanilla_path is None:
    raise FileNotFoundError("Emplacement.lua not found under " + str(game))
vanilla = vanilla_path.read_text(encoding="utf-8")
update = vanilla[vanilla.index("function MachineGunEmplacement:Update()"):vanilla.index("function MachineGunEmplacement:GetEnemyUnitsInArea(")]
jazz = (root / "Code/System_EmplacementAmmo.lua").read_text(encoding="utf-8")
lua = LuaRuntime(unpack_returned_tuples=True)
lua.execute('''
MachineGunEmplacement = {}
Unit = false
OnMsg = {}
const = {SlabSizeX=1200}
editor = false
function IsEditorActive() return editor end
function Clamp(v,a,b) return math.min(math.max(v,a),b) end
function Max(a,b) return (a > b) and a or b end
function ObjModified() end
function DoneObject() end
function table.copy(t) local r={} for k,v in pairs(t) do r[k]=v end return r end
function table.find(t,key,v) for i,o in ipairs(t) do if o[key]==v then return i end end end
g_Classes = {MachineGunEmplacement={properties={{id="target_dist"}}}}
InventoryItemDefs = {BrowningM2HMG={Caliber="JAZZ_Caliber_50BMG"}, JAZZ_AMMO_50BMG_Basic={}}
function PlaceInventoryItem(id)
  if id == "JAZZ_AMMO_50BMG_Basic" then return {class=id} end
  return {class=id, MagazineSize=100, WeaponRange=95,
    GetOverwatchConeParam=function(self,p) return p=="MinRange" and 14 or 95 end,
    GetVisualObj=function() return false end,
    Reload=function(self,ammo) self.ammo=ammo end}
end
function MachineGunEmplacement:GetPos() return 0 end
function MachineGunEmplacement:GetAngle() return 0 end
function MachineGunEmplacement:SetProperty(k,v)
  self[k]=v
  if k=="target_dist" and not self.updating then self:Update() end
end
function make_emplacement(distance)
  return setmetatable({class="MachineGunEmplacement",weapon_template="BrowningM2HMG",
    ammo_template="_50BMG_Basic",target_dist=distance,interaction_visuals={}},
    {__index=MachineGunEmplacement})
end
''')
lua.execute(update)
lua.execute(jazz)
run = lua.eval('function(d) local e=make_emplacement(d); e:Update(); local first=e.target_dist; e.interaction_visuals={}; e:Update(); return first,e.target_dist,e.ammo_template end')
for distance, expected in [(91200, 114000), (1, 114000), (999999, 114000), (16800, 114000)]:
    first, second, ammo = run(distance)
    assert (first, second) == (expected, expected), (distance, first, second, expected)
    assert ammo == "JAZZ_AMMO_50BMG_Basic"
print("PASS MaxRange for every authored dist, repeated Update, ammo remap")

lua.execute("""
empty_table={}; guim=1000
function point(x) return x end
function Rotate(x) return x end
function GetStepPositionsInArea() return {},{} end
function CreateAOETilesSector() return false end
function MachineGunEmplacement:GetValidInteractionPositions() return {} end
editor=true
local e=make_emplacement(91200); e:Update(); assert(e.target_dist==16800)
editor=false
local nested=make_emplacement(91200); nested.updating=true
nested:Update(); assert(nested.updating==false and nested.target_dist==16800)
assert(Jazz_EmplacementConeDist(make_emplacement(false))==false) -- weapon not created yet
local e=make_emplacement(false); e:Update(); assert(e.target_dist==114000)
local base_calls=0
MachineGunEmplacement.EndInteraction=function() base_calls=base_calls+1 end
function RotateRadius(dist) return dist end
OnMsg.ClassesBuilt()
local wrapper=MachineGunEmplacement.EndInteraction
OnMsg.ClassesBuilt(); assert(wrapper==MachineGunEmplacement.EndInteraction)
local unit={count=0,EnterEmplacement=function(self) self.count=self.count+1 end,
 RecalcUIActions=function() end,UpdateOutfit=function() end,
 QueueCommand=function(self,cmd,action,ap,args) self.target=args.target end}
local e=make_emplacement(91200); e:Update(); e:EndInteraction(unit)
assert(unit.target==114000 and unit.count==1 and base_calls==0)
assert(Jazz_EmplacementConeAngle()==2700)
""")
print("PASS editor/reentrant guards, missing-distance fallback, EndInteraction range and wrapper idempotence")
print("PASS emplacement cone angle is 45 degrees (2700 minutes)")
