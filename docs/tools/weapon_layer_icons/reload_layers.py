"""Reload the scoped installed UI and verify both serialized HUD callbacks.

Reads the preserved metadata load order. Optional image reload is limited to
named pilot families to avoid requesting the entire arsenal into GPU memory.
Run only after photography and installation have finished.
"""
import argparse,json
from pathlib import Path
from lupa import LuaRuntime
from install_layers import lua
from live import evaluate,quote

p=argparse.ArgumentParser(__doc__);p.add_argument('--repo',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--library',type=Path);p.add_argument('--reload-weapons',nargs='*',default=[]);a=p.parse_args()
l=LuaRuntime();l.execute('function PlaceObj(c,p,ch) return p end')
t=l.execute((a.repo/'metadata.lua').read_text(encoding='utf-8-sig'));metadata={t[i]:t[i+1] for i in range(1,len(t),2)}
images=[]
if a.library:
 r=json.loads((a.library/'registry.json').read_text(encoding='utf-8'))
 images=[x['image'] for x in r['layers'].values() if x['image'] and x['signature'].split('|')[0] in a.reload_weapons]
settings=lua({'code':list(metadata['code'].values()),'version':metadata['version'],'images':images,'output':a.output.resolve().with_suffix('.verification.json').as_posix()})
body='''CreateRealTimeThread(function()
 local ign=SafeEvalStart("native-layer-roundtrip")
 local settings=%s
 local ok,err=pcall(function()
  local mod=Mods.e6L4ECj
  if mod.version~=settings.version then error("unexpected editor revision") end
  mod.code=settings.code
  mod:UnloadItems();mod:LoadItems()
  if mod:IsItemsFileModified() then error("external timestamp mismatch") end
  ReloadLua()
  local callbacks=0
  local function visit(node)
   if node.comment=="weapon" and type(node.run_after)=="function" and GetFuncSourceString(node.run_after):find("JazzWeaponIcon_BindItemImage",1,true) then callbacks=callbacks+1 end
   for _,child in ipairs(node) do if type(child)=="table" then visit(child) end end
  end
  mod:ForEachModItem(function(item) if IsKindOf(item,"ModItemXTemplate") and item.id=="UIWeaponDisplay" then visit(item) end end)
  if callbacks~=2 then error("HUD callback roundtrip failed") end
  for _,path in ipairs(settings.images) do UIL.ReloadImage(path) end
 end)
 SafeEvalEnd(ign,"native-layer-roundtrip")
 local _,text=LuaToJSON({status=ok and "PASS" or "FAIL",error=not ok and tostring(err) or nil,version=settings.version,code_count=#settings.code,reloaded_images=#settings.images,callbacks=ok and 2 or nil})
 AsyncStringToFile(settings.output,text)
end);return "roundtrip scheduled"
'''%settings
evaluate(body,a.output)
