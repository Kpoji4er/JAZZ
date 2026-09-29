"""Exercise the real XImage adapter on a disposable UI window via live DAP.

Copies the selected library's textures only, never reloads UI hooks or game code.
Does not take screenshots or touch the active native capture camera.
"""
import argparse,json,shutil
from pathlib import Path
from install_layers import lua
from live import evaluate,quote

p=argparse.ArgumentParser(__doc__);p.add_argument('--library',type=Path,required=True);p.add_argument('--repo',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
registry=json.loads((a.library/'registry.json').read_text(encoding='utf-8'))
dest=a.repo/'WeaponIcons/Live/Layers';dest.mkdir(parents=True,exist_ok=True)
for ident,layer in registry['layers'].items():
 if layer['image']:shutil.copy2(a.library/'layers'/(ident+'.png'),dest/(ident+'.png'))
here=Path(__file__).parent
body='local function assert(v,m) if not v then error(m or "probe assertion failed") end return v end\nlocal registry='+lua(registry)+'\n'
for name in ('selector','binder'):
    body+='local '+name+'=assert(load('+quote((here/('layer_'+name+'.lua')).read_text(encoding='utf-8'))+',"layer-probe","t",_G))()\n'
body+='''
local img
local ok,result=pcall(function()
  assert(Platform.debug and GetMapName()=="ModEditor")
  for _,layer in pairs(registry.layers) do if layer.image then UIL.RequestImage(layer.image) end end
  Sleep(500)
  img=XImage:new({Image="Mod/e6L4ECj/WeaponIcons/AK74.png",Visible=false,ImageFit="smallest",HandleMouse=false},terminal.desktop)
  img:Open()
  local color=img.ImageColor
  local item={class="AK74",Entity="AK74",components={}}
  assert(binder.bind(img,item,registry,selector),"default not bound")
  local first=img:ResolveId("idJazzNativeWeaponLayers")
  assert(first and #first>0,"no native children")
  assert(binder.bind(img,item,registry,selector),"stable rebind failed")
  assert(img:ResolveId("idJazzNativeWeaponLayers")==first,"stable rebind recreated group")
  item.components.Scope="JAZZ_Reflex_PKAS"
  item.components.Magazine="JAZZ_MagLarge_30_45"
  item.components.Stock="JAZZ_StockLightUnFolded"
  assert(binder.bind(img,item,registry,selector),"combined not bound")
  local second=img:ResolveId("idJazzNativeWeaponLayers")
  assert(second and second~=first and #second==12,"combined children mismatch")
  img:SetEnabled(false)
  assert(not second:GetEnabled() and not second[1]:GetEnabled(),"disabled state did not propagate")
  img:SetEnabled(true)
  assert(second:GetEnabled() and second[1]:GetEnabled(),"enabled state did not restore")
  local previous_scale=second[1].ImageScale:x()
  img:SetImageScale(point(700,700))
  assert(binder.bind(img,item,registry,selector),"scaled rebind failed")
  local scaled=img:ResolveId("idJazzNativeWeaponLayers")
  assert(scaled~=second and scaled[1].ImageScale:x()<previous_scale,"parent image scale ignored")
  binder.clear(img)
  assert(img.ImageColor==color,"color not restored")
  assert(not binder.bind(img,nil,registry,selector),"nil context bound")
  return "PASS: real XImage default, stable binding, 6-part combined build, disabled/enabled, image scale, clear and original color"
end)
if img then binder.clear(img);img:delete() end
assert(ok,tostring(result))
return result
'''
a.output.parent.mkdir(parents=True,exist_ok=True);a.output.with_suffix('.lua').write_text(body,encoding='utf-8')
evaluate(body,a.output,True)
