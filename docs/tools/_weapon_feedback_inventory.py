"""Read actual component definitions and list selected weapons' visual graphs.

--output JSON; read-only, including defaults and every offered component.
"""
import argparse,json,re
from pathlib import Path
from lupa import LuaRuntime
from _integrate_m14_family import matching
p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);a=p.parse_args()
root=Path(__file__).resolve().parents[2];lua=LuaRuntime(unpack_returned_tuples=True)
source=(root/'docs/tools/_weapon_feedback_components.py').read_text(encoding='utf-8')
lua.execute(source.split("lua.execute('''",1)[1].split("''')",1)[0])
lua.execute('function point(...) return {...} end; function RGBA(...) return {...} end; RGB=RGBA')
s=(root/'items.lua').read_text(encoding='utf-8-sig');components={}
for m in re.finditer(r"PlaceObj\('ModItemWeaponComponent'",s):
 end=matching(s,s.index('(',m.start()));c=lua.execute('return '+s[m.start():end]);components[c.id]=c
report={}
for name in ('M4A1','M16A4','M14SAW','JAZZ_M14_MkIII','JAZZ_FNFAL_Tactical','Mosin','AK103'):
 lua.execute((root/'InventoryItem'/(name+'.lua')).read_text(encoding='utf-8-sig'));w=lua.globals().DefineClass[name];slots={}
 for _,slot in w.ComponentSlots.items():
  if not hasattr(slot,'SlotType') or not slot.SlotType:continue
  options={}
  for _,id in slot.AvailableComponents.items():
   c=components.get(id)
   if not c:continue
   visuals={}
   for _,v in (c.Visuals.items() if c.Visuals else []):
    if v.ApplyTo and v.ApplyTo not in ('',name):continue
    if v.Slot not in visuals or v.ApplyTo==name:
     visuals[v.Slot or '<missing>']={'entity':v.Entity,'specific':v.ApplyTo==name}
   options[id]={'visuals':visuals,'icon':c.Icon,'name':c.DisplayName}
  slots[slot.SlotType]={'default':slot.DefaultComponent,'options':options}
 report[name]={'entity':w.Entity,'slots':slots}
a.output.write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding='utf-8')
print('Wrote',a.output)
