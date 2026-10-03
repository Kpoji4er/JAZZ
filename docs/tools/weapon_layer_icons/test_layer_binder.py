"""Offline ownership/lifecycle checks for the native image binder."""
from pathlib import Path
from lupa import LuaRuntime
root=Path(__file__).parent
lua=LuaRuntime(unpack_returned_tuples=True)
lua.execute('''
function RGBA(...) return table.concat({...},",") end
function RGB(r,g,b) return RGBA(r,g,b,255) end
function box(...) return {...} end
function point(...) return {...} end
UIL={missing=false}
function UIL.RequestImage() end
function UIL.MeasureImage(path) return UIL.missing and 0 or 1296,660 end
XWindow={created=0,deleted=0}
function XWindow:new(props,parent)
 self.created=self.created+1
 props.children={};props.parent=parent;parent.children[#parent.children+1]=props
 function props:delete() self.window_state="destroying";XWindow.deleted=XWindow.deleted+1 end
 function props:Open() self.window_state="open" end
 function props:SetVisible(value) self.Visible=value end
 function props:SetEnabled(value) self.enabled=value end
 return props
end
XImage={}
XControl=XWindow
function XImage:new(props,parent) parent.children[#parent.children+1]=props;return props end
img={children={},ImageColor="original-color",DisabledImageColor="original-disabled",ImageFit="smallest",window_state="open"}
function img:SetImageColor(value) self.ImageColor=value end
function img:SetDisabledImageColor(value) self.DisabledImageColor=value end
function img:GetEnabled() return true end
selector={}
function selector.resolve(_,item)
 if not item or not item.key then return nil end
 return {key=item.key,width=324,height=165,bounds={400,200,1000,450},layers={{id="body",image="body.png"},{id=item.key,image=item.key..".png"}}}
end
''')
lua.globals().binder=lua.execute((root/'layer_binder.lua').read_text(encoding='utf-8-sig'))
lua.execute('''
assert(binder.bind(img,{key="A"},{},selector))
assert(XWindow.created==1 and XWindow.deleted==0)
local group=img.children[1]
assert(#group.children==4 and group.Visible)
assert(group.children[1].EffectType=="glow" and group.children[2].EffectType=="glow")
assert(group.children[3].EffectType=="none" and group.children[4].EffectType=="none")
assert(binder.bind(img,{key="A"},{},selector))
assert(XWindow.created==1)
assert(binder.bind(img,{key="B"},{},selector))
assert(XWindow.created==2 and XWindow.deleted==1)
assert(binder.bind(img,{key="A"},{},selector))
assert(XWindow.created==3 and XWindow.deleted==2)
UIL.missing=true
assert(not binder.bind(img,{key="A"},{},selector))
assert(XWindow.deleted==3 and img.ImageColor=="original-color" and img.DisabledImageColor=="original-disabled")
UIL.missing=false
assert(binder.bind(img,{key="A"},{},selector))
assert(not binder.bind(img,nil,{},selector))
assert(XWindow.deleted==4 and img.ImageColor=="original-color")
binder.clear(img);assert(XWindow.deleted==4)
assert(binder.bind(img,{key="A"},{},selector))
img:SetImageColor("new-context-color")
assert(not binder.bind(img,nil,{},selector))
assert(img.ImageColor=="new-context-color","fallback overwrote new context tint")
img.window_state="destroying"
assert(not binder.bind(img,{key="A"},{},selector))
''')
print('PASS: layer ownership, A/B/A, stable key, missing image, nil context, color restoration, glow-before-color ordering')

# Existing UI survives a Lua reload; transparent replacement groups must not
# overwrite the original tint retained by the oldest color pass.
lua.execute('''
local orphan={ImageColor=RGBA(255,255,255,0),DisabledImageColor=RGBA(255,255,255,0)}
function orphan:SetImageColor(v) self.ImageColor=v end
function orphan:SetDisabledImageColor(v) self.DisabledImageColor=v end
for i=1,2 do
 local tint=i==1 and "saved-color" or RGBA(255,255,255,0)
 local disabled=i==1 and "saved-disabled" or RGBA(255,255,255,0)
 local group={Id="idJazzNativeWeaponLayers",{ImageColor=tint,DisabledImageColor=disabled}}
 function group:delete() for j=#orphan,1,-1 do if orphan[j]==self then table.remove(orphan,j) end end end
 orphan[i]=group
end
binder.clear(orphan)
assert(#orphan==0 and orphan.ImageColor=="saved-color" and orphan.DisabledImageColor=="saved-disabled")
''')
print('PASS: hot-reload orphan groups removed and original tints recovered')
