"""Regression: actual vanilla cabinet gate, absent vs occupied blocked slot.

--game-root DIR --module FILE. Demonstrates original bug before testing fix.
"""
import argparse,re
from pathlib import Path
from lupa import LuaRuntime
from _integrate_m14_family import matching
p=argparse.ArgumentParser();p.add_argument('--game-root',type=Path,required=True);p.add_argument('--module',type=Path,required=True);a=p.parse_args()
root=Path(__file__).resolve().parents[2];lua=LuaRuntime(unpack_returned_tuples=True)
lua.execute('''
empty_table={}; WeaponComponents={}; WeaponComponentBlockPairs={}; DefineClass={}; ModifyWeaponDlg={}
function UndefineClass() end
function T(id,text) return text end
function PlaceObj(c,p) for i=1,#p,2 do if type(p[i])=="string" then p[p[i]]=p[i+1] end end return p end
function table.find(t,val) for i,v in ipairs(t) do if v==val then return i end end end
function table.find_value(t,key,val) for _,v in ipairs(t) do if v[key]==val then return v end end end
''')
items=(root/'items.lua').read_text(encoding='utf-8-sig')
for name in ('JAZZ_BarrelNormal','JAZZ_BarrelShort','JAZZ_BarrelLong'):
 at=items.index('id = "'+name+'"');start=items.rfind("PlaceObj('ModItemWeaponComponent'",0,at);end=matching(items,items.index('(',start));lua.globals().WeaponComponents[name]=lua.execute('return '+items[start:end])
engine=(a.game_root/'ModTools/Src/Lua/UI/ModifyWeaponDlg.lua').read_text(encoding='utf-8')
def function(text,name):
 start=text.index('function '+name+'(');end=text.find('\nfunction ',start+10);return text[start:end if end!=-1 else len(text)]
for name in ('GetComponentsBlockedByComponent','GetComponentBlocksAnyOfAttachedSlots','ModifyWeaponDlg:CanModifySlot'):lua.execute(function(engine,name))
for name in ('M4A1','M16A4'):lua.execute((root/'InventoryItem'/(name+'.lua')).read_text(encoding='utf-8'))
lua.execute('''
function case(name)
 local w={class=name,components={},ComponentSlots=DefineClass[name].ComponentSlots}
 for _,s in ipairs(w.ComponentSlots) do w.components[s.SlotType]=s.DefaultComponent or "" end
 local dlg=setmetatable({context={weapon=w},GetChangesCost=function() return {},true,true end},{__index=ModifyWeaponDlg})
 return w,dlg,table.find_value(w.ComponentSlots,"SlotType","Barrel")
end
for _,name in ipairs({"M4A1","M16A4"}) do
 local w,d,s=case(name);local ok,why=d:CanModifySlot(s,"JAZZ_BarrelShort")
 assert(not ok and why=="blocked","Original bug must reproduce")
end
''')
module=a.module.read_text(encoding='utf-8-sig');start=module.index('function GetComponentBlocksAnyOfAttachedSlots(');end=module.index('local VanillaCanModifySlot',start);lua.execute(module[start:end])
lua.execute('''
for _,name in ipairs({"M4A1","M16A4"}) do
 local w,d,s=case(name)
 assert(d:CanModifySlot(s,"JAZZ_BarrelShort"))
 assert(d:CanModifySlot(s,"JAZZ_BarrelNormal"))
 w.components.Side2="real_attachment"
 local ok,why,part=d:CanModifySlot(s,"JAZZ_BarrelShort")
 assert(not ok and why=="blocked" and part=="real_attachment")
 w.components.Side2="";assert(d:CanModifySlot(s,"JAZZ_BarrelShort"))
 table.insert(w.ComponentSlots,{SlotType="Side2",DefaultComponent="default_attachment"})
 w.components.Side2="default_attachment";assert(d:CanModifySlot(s,"JAZZ_BarrelShort"))
end
''')
print('PASS: reproduced original preview block; fixed missing/empty/default slots; occupied slot still blocks, both AR15s')
