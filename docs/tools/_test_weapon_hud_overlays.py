"""Offline Lua regression: real HUD callback width and legacy overlay cleanup.

Requires lupa. This exercises Lua with UI doubles, not a live combat acceptance.
"""
from pathlib import Path
from lupa import LuaRuntime

root = Path(__file__).resolve().parents[2]
items = (root / "items.lua").read_text(encoding="utf-8")
pos = items.index("local sideButtonsSize")
start = items.rfind("'run_after', function", 0, pos)
indent = items[items.rfind("\n", 0, start) + 1:start]
end = items.index("\n" + indent + "end,", pos)
callback = items[start + len("'run_after', "):end] + "\nend"
lua = LuaRuntime()
lua.execute('''
function box(...) return {...} end
function IsKindOf(o, kind) return o and o.firearm or false end
function GetReloadOptionsForWeapon() return {} end
function GetBulletCount() return 1 end
HUDButtonHeight = 75
Selection = {{}}
function JazzResolveFoldStockAction() return foldState ~= "hidden", foldState end
function JazzResolveFlashlightAction() return flashState ~= "hidden", flashState end
function image()
 return {SetImage=function() end, SetMinHeight=function() end, SetMaxHeight=function() end,
 SetMaxWidth=function(self,w) self.MaxWidth=w end}
end
function weapon(large)
 return {IsLargeItem=function() return large end, Icon="test"}
end
function child() return {idIcon=image(),idWarningText=image(),idFrame={}} end
''')
lua.globals().callback = lua.eval(callback)
lua.execute('''
for _,fold in ipairs({"hidden","enabled","disabled"}) do
 for _,flash in ipairs({"hidden","enabled","disabled"}) do
  foldState,flashState=fold,flash
  local visible=fold~="hidden" or flash~="hidden"
  local extra=visible and 27 or 0
  for _,large in ipairs({false,true}) do
   local c=child(); callback(c,{},weapon(large),1,1,1)
   assert(c.idIcon.MaxWidth+extra==(large and 154 or 77), "single HUD expanded")
  end
  local a,b=child(),child()
  callback(a,{},weapon(false),1,1,2); callback(b,{},weapon(false),2,2,2)
  assert(a.idIcon.MaxWidth+b.idIcon.MaxWidth+extra==154,"dual HUD expanded")
 end
end
''')
lua.execute((root / "Code/WeaponAttachChips.lua").read_text(encoding="utf-8"))
lua.execute('''
local badge={SetVisible=function(self,v) self.visible=v end}
local row={children=4,DeleteChildren=function(self) self.children=0 end,
 SetFoldWhenHidden=function(self,v) self.fold=v end,SetVisible=function(self,v) self.visible=v end}
local layers={}
local host={idJazzAttachChips=row,idModIcon=badge,idJazzNativeWeaponLayers=layers}
assert(JazzAttachChips_Apply(host,{firearm=true})==false)
assert(row.children==0 and row.visible==false and row.fold==true)
assert(badge.visible==false and host.idJazzNativeWeaponLayers==layers)
local fresh={}
assert(JazzAttachChips_Apply(fresh,{firearm=true})==false and next(fresh)==nil)
assert(JazzAttachChips_Apply(nil,nil)==false)
''')
compile_lua = lua.eval("function(s) local f,e=load(s); assert(f,e) end")
compile_lua(items)
compile_lua((root / "metadata.lua").read_text(encoding="utf-8"))
print("PASS: 27 width cases; fresh/legacy overlays; native layers preserved; Lua syntax")
