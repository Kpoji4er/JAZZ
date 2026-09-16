"""Regression: AP callbacks must not send strategic UnitData to tactical listeners."""
from pathlib import Path
import re
from lupa import LuaRuntime
root=Path(__file__).resolve().parents[2]
items=(root/'items.lua').read_text(encoding='utf-8')
count=0
for p in (root/'CharacterEffect').glob('Trauma*.lua'):
    source=p.read_text(encoding='utf-8')
    if 'Msg("UnitAPChanged", obj)' not in source: continue
    pos=items.index("'Id', "+chr(34)+p.stem+chr(34))
    end=items.find("PlaceObj('ModItem",pos)
    block=items[pos:end]
    lua=LuaRuntime()
    lua.execute("""DefineClass={}; function UndefineClass() end
function PlaceObj() return {} end;function T() return '' end
function IsKindOf(obj,kind) return obj and obj.kind==kind end
calls=0;function Msg(event,obj) assert(event=='UnitAPChanged');obj:UpdateNumOverwatchAttacks();calls=calls+1 end
unit={kind='Unit',UpdateNumOverwatchAttacks=function() end};data={kind='UnitData'}
""")
    lua.execute(source)
    effect=lua.globals().DefineClass[p.stem]
    for cb in ('OnAdded','OnRemoved'):
        effect[cb](effect,lua.globals().data)
        effect[cb](effect,lua.globals().unit)
    assert lua.globals().calls==2,p.stem
    assert block.count('if IsKindOf(obj, "Unit") then')==2,p.stem
    count+=1
assert count==6,count
print('PASS six trauma effects: Unit-only AP callbacks, UnitData safe, generated guards present')
