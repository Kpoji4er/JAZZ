"""Stage M14 AK bipod visual; exercise actual vanilla UpdateVisualObj for M4.

--output DIR --game-root DIR. No installed writes. Exports items.lua and a report.
The Lua harness verifies data/attachment traversal, not native rendering or loaded mods.
"""
import argparse,json,re
from pathlib import Path
import xml.etree.ElementTree as ET
from lupa import LuaRuntime
from _integrate_m14_family import matching
root=Path(__file__).resolve().parents[2]
p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);p.add_argument('--game-root',type=Path,required=True);a=p.parse_args();a.output.mkdir(parents=True,exist_ok=True)
original=(root/'items.lua').read_bytes();text=original.decode('utf-8')
pattern=r'(ApplyTo = "M14SAW",\s*Entity = ")WeaponAttA_BipodM24("[,]\s*Slot = "Bipod")'
staged,count=re.subn(pattern,r'\g<1>WeaponAttA_BipodAK47\2',text);assert count==1,count
(a.output/'items.lua').write_bytes(staged.encode('utf-8'));(a.output/'items-before.lua').write_bytes(original)
# AK bipod clamps around the barrel axis, whereas M24's shoe attaches beneath it.
# A dedicated Under spot keeps M21's existing Bipod shoe placement unchanged.
staged,n=re.subn(r'(ApplyTo = "M14SAW",\s*Entity = "WeaponAttA_BipodAK47",\s*Slot = ")Bipod(")',r'\g<1>Under\2',staged);assert n==1
(a.output/'items.lua').write_bytes(staged.encode('utf-8'))
entity_path=root.parent/'jazz_assets/Entities/JAZZ_M14.ent'
entity=entity_path.read_bytes();updated,n=re.subn(rb'(<attach name="Under" spot_pos=")[^"]+',rb'\g<1>56.000,0.000,9.500',entity);assert n==1
(a.output/'JAZZ_M14.ent').write_bytes(updated);(a.output/'JAZZ_M14-before.ent').write_bytes(entity)
lua=LuaRuntime(unpack_returned_tuples=True)
lua.execute('''
empty_table={}; WeaponComponents={}; ComponentRemap={}; FirearmBase={}; DefineClass={}
function UndefineClass() end
function T(id,text) return text end
function PlaceObj(class,p)
 for i=1,#p,2 do if type(p[i])=="string" then p[p[i]]=p[i+1] end end
 if class=="WeaponComponentVisual" then
  function p:Match(w) return not self.ApplyTo or self.ApplyTo=="" or self.ApplyTo==w end
  function p:IsGeneric() return not self.ApplyTo or self.ApplyTo=="" end
 end
 return p
end
function table.copy(t) local r={} for k,v in pairs(t) do r[k]=v end return r end
function table.find(t,key,val) for i,v in ipairs(t) do if v[key]==val then return i end end end
function sorted_pairs(t) return pairs(t) end
function IsValid(o) return o and o.valid end
function DoneObject(o) if not o then return end o.valid=false for _,child in ipairs(o.children or {}) do DoneObject(child) end end
function FirearmBase:UpdateColorMod() end
SlotDependencies={Muzzle="Barrel",Bipod="Barrel",Side="Barrel",Sightsf="Barrel"}
EntitySpots={}
function PlaceObject()
 local o={valid=true,children={}}
 function o:ChangeEntity(e) self.entity=e end
 function o:GetEntity() return self.entity end
 function o:GetSpotBeginIndex(s) return EntitySpots[self.entity] and EntitySpots[self.entity][s] and s or -1 end
 function o:Attach(child,spot) child.parent=self;child.spot=spot;self.children[#self.children+1]=child end
 return o
end
''')
lua.execute((root/'InventoryItem/M4A1.lua').read_text(encoding='utf-8'))
# Evaluate complete component definitions, including every competing visual.
for cid in ('JAZZ_BarrelNormal','JAZZ_BarrelShort','JAZZ_BarrelLong','JAZZ_DefMuzzle','JAZZ_Bipod_Under'):
    needle='id = "'+cid+'"';at=staged.index(needle);start=staged.rfind("PlaceObj('ModItemWeaponComponent'",0,at);end=matching(staged,staged.index('(',start))
    lua.globals().WeaponComponents[cid]=lua.execute('return '+staged[start:end])
lua.execute('''
local m14,m21=0,0
for _,visual in ipairs(WeaponComponents.JAZZ_Bipod_Under.Visuals) do
 if visual.ApplyTo=="M14SAW" and visual.Entity~="" then
  assert(visual.Entity=="WeaponAttA_BipodAK47" and visual.Slot=="Under");m14=m14+1
 elseif visual.ApplyTo=="M21" and visual.Entity=="WeaponAttA_BipodM24" then
  assert(visual.Slot=="Bipod");m21=m21+1
 end
end
assert(m14==1 and m21==1)
''')
for path in (root.parent/'jazz_assets/Entities').glob('M4R_*.ent'):
    spots={n.get('name'):tuple(float(v)/100 for v in n.get('spot_pos').split(',')) for n in ET.parse(path).findall('.//attach')}
    lua.globals().EntitySpots[path.stem]=lua.table_from({name:lua.table_from(pos) for name,pos in spots.items()})
engine=(a.game_root/'ModTools/Src/Lua/Tactical/Weapon.lua').read_text(encoding='utf-8')
start=engine.index('function FirearmBase:UpdateVisualObj(vis)');end=engine.index('\nfunction ',start+10)
lua.execute(engine[start:end])
lua.execute('''
w=setmetatable({class="M4A1",components={Muzzle="JAZZ_DefMuzzle"},subweapons={},
 ComponentSlots={{SlotType="Muzzle"},{SlotType="Barrel"}}},{__index=FirearmBase})
vis=PlaceObject();vis:ChangeEntity("M4R_M4A1");vis.weapon=w;vis.parts={};vis.components={};w.visual_obj=vis
results={}
for _,id in ipairs({"JAZZ_BarrelNormal","JAZZ_BarrelShort","JAZZ_BarrelLong","JAZZ_BarrelShort","JAZZ_BarrelNormal"}) do
 w.components.Barrel=id;w:UpdateVisualObj(vis)
 assert(vis.parts.Barrel and vis.parts.Muzzle and IsValid(vis.parts.Muzzle))
 assert(vis.parts.Muzzle.parent==vis.parts.Barrel,"Muzzle did not follow barrel")
 results[#results+1]={id=id,entity=vis.parts.Barrel.entity,muzzle_parent=vis.parts.Muzzle.parent.entity}
end
''')
results=[dict(v.items()) for _,v in lua.globals().results.items()]
assert [r['entity'] for r in results][:3]==['M4R_M4A1_Barrel','M4R_M4A1_BarrelShort','M4R_M4A1_BarrelLong']
tips={}
for suffix in ('Barrel','BarrelShort','BarrelLong'):
    ent=ET.parse(root.parent/'jazz_assets/Entities'/('M4R_M4A1_'+suffix+'.ent'))
    tips[suffix]=float(next(n for n in ent.findall('.//attach') if n.get('name')=='Muzzle').get('spot_pos').split(',')[0])/100
assert tips['Barrel']-tips['BarrelShort']>.10
lua.compile(staged)
report={'M14_bipod_replacements':count,'M4_real_vanilla_method_harness':'PASS','M4_switch_sequence':results,'M4_local_muzzle_x_m':tips,'M4_shorter_m':tips['Barrel']-tips['BarrelShort'],'runtime_rendering_verified':False,'M4_change_required_by_static_evidence':False}
(a.output/'component-report.json').write_text(json.dumps(report,indent=2));print(json.dumps(report))
