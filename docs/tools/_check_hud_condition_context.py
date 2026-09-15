"""Exercise the HUD condition context without mutating its item (Lua harness)."""
from pathlib import Path
import re
from lupa import LuaRuntime

root = Path(__file__).resolve().parents[2]
text = (root / "items.lua").read_text(encoding="utf-8")
matches = re.findall(r"'Id', \"idCondText\",\s*'__context', (function\s*\(parent, context\).*?end),", text, re.S)
assert len(matches) == 1, "HUD condition context absent or ambiguous"
lua = LuaRuntime(unpack_returned_tuples=True)
lua.execute('function SubContext(parent, values) return setmetatable(values, {__index=parent}) end')
callback = lua.eval(matches[0])
for percent in (0, 43, 100):
    item = lua.eval(f'{{Condition=87, WeaponResource=430, GetConditionPercent=function() return {percent} end}}')
    context = callback(None, item)
    assert context.Condition == percent
    assert item.Condition == 87 and item.WeaponResource == 430
    assert context.WeaponResource == 430
print("PASS HUD condition 0/43/100; source item unchanged")
