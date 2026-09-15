"""Run villa ExecuteCode records through vanilla dispatch in isolated Lua.

Uses lupa and installed ModTools source; this is a harness, not in-game evidence.
"""
from pathlib import Path
import re
from lupa import LuaRuntime

ROOT = Path(__file__).resolve().parents[2]
game = Path((ROOT / ".ja3-root.local").read_text().strip())
items = (ROOT.parent / "jazz-maps/items.lua").read_text(encoding="utf-8")
source = (game / "ModTools/Src/CommonLua/Classes/ClassDefs/ClassDef-Effects.generated.lua").read_text(encoding="utf-8")
dispatch = source[source.index("function ExecuteCode:__exec("):source.index("function ExecuteCode:__toluacode(")]
compiler_source = (game / "ModTools/Src/CommonLua/Core/ToLuaCode.lua").read_text(encoding="utf-8")
compiler = compiler_source[compiler_source.index("\nfunction CompileFunc("):compiler_source.index("--- Compiles an expression")]
lua = LuaRuntime(unpack_returned_tuples=True)
lua.execute('''
ExecuteCode = {Code = function() end, SaveAsText = false}
function ExecuteCode:GetPropertyMetadata() return {params=function() return "self, obj" end} end
FuncSource = {}
function string.split(s) return {s} end
printf = error
calls = {}
Mods = {FhNNYd = {env = {}}}
''')
lua.execute(compiler)
lua.execute(dispatch)
names = ["Jazz_VillaCounterAttack_Start", "Jazz_VillaCounterAttack_OnWave2", "Jazz_VillaCounterAttack_PushAdvanceToEmma"]
failed = []
for name in names:
    blocks = [m.group(1) for m in re.finditer(r"PlaceObj\('ExecuteCode',\s*(\{[^{}]*\})\)", items)
              if name + "()" in m.group(1)]
    assert len(blocks) == 1, (name, len(blocks))
    lua.execute(f'Mods.FhNNYd.env.{name} = function() calls["{name}"] = (calls["{name}"] or 0) + 1 end')
    effect = lua.eval('setmetatable(' + blocks[0] + ', {__index=ExecuteCode})')
    try:
        lua.eval('function(effect) return effect:__exec() end')(effect)
        assert lua.globals().calls[name] == 1, "effect never called its handler"
        print("PASS", name)
    except Exception as exc:
        failed.append(name)
        print("FAIL", name, str(exc))
raise SystemExit(bool(failed))
