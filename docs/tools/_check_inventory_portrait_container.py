"""Evaluate the real SquadsAndMercs template and check portrait-list ownership."""
from pathlib import Path
from lupa import LuaRuntime
root=Path(__file__).resolve().parents[2]
s=(root/'items.lua').read_text(encoding='utf-8')
pos=s.index('id = "SquadsAndMercs",');a=s.rfind("PlaceObj('ModItemXTemplate'",0,pos);b=s.index("PlaceObj('ModItemXTemplate'",pos)
lua=LuaRuntime()
lua.execute("""function PlaceObj(class,props,children) return {class=class,props=props,children=children or {}} end
function box() return {} end;function point() return {} end;function RGBA() return 0 end
function RGB() return 0 end;function T() return '' end;function set() return {} end
""")
lua.globals().tree=lua.execute('return '+s[a:b].rstrip().rstrip(','))
lua.execute("""ids={};function walk(n,depth)
local p=n.props or {};for i=1,#p do
 if p[i]=='Id' and (p[i+1]=='idContainer' or p[i+1]=='idPartyLayout') then ids[#ids+1]={p[i+1],depth,n} end
 if type(p[i])=='table' and p[i].class then walk(p[i],depth+1) end
end
for _,child in ipairs(n.children or {}) do walk(child,depth+1) end end
walk(tree,0)
""")
ids=lua.globals().ids
found=[(ids[i][1],ids[i][2]) for i in range(1,len(ids)+1)]
assert found.count(('idPartyLayout',4))==1 and found.count(('idContainer',6))==3,found
for i in range(1,len(ids)+1):
    if ids[i][1]=='idContainer':
        children=ids[i][3]['children']
        assert children[1]['class']=='XTemplateForEach'
print('PASS actual portrait template: distinct outer layout, three conditional direct portrait lists')
