# -*- coding: utf-8 -*-
"""Load items.lua / metadata.lua in lupa with stubs — catches SYNTAX errors like the game."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


PRELUDE = r"""
local function stub(...)
  return {}
end
function PlaceObj(cls, props, children)
  return { _cls = cls, _props = props, _children = children }
end
function T(id, a, b) return a or id end
function Untranslated(x) return x end
function box(...) return {...} end
function RGBA(...) return {...} end
function RGB(...) return {...} end
function point(...) return {...} end
function range(...) return {...} end
function set(...) return {...} end
function pstr(...) return tostring(...) end
empty_table = {}
empty_func = function() end
-- Auto-stub unknown globals used as callables in data files
setmetatable(_G, {
  __index = function(t, k)
    local f = function(...) return {} end
    rawset(t, k, f)
    return f
  end
})
"""


def try_load(path: Path) -> str | None:
    from lupa import LuaRuntime

    lua = LuaRuntime(unpack_returned_tuples=True)
    src = path.read_text(encoding="utf-8")
    # strip BOM
    if src.startswith("\ufeff"):
        src = src[1:]
    try:
        lua.execute(PRELUDE + "\nlocal _result = " + src.lstrip() if src.lstrip().startswith("{") or src.lstrip().startswith("return") else PRELUDE + "\n" + src)
        # items.lua is `return { ... }` — lupa execute of return at top may not work;
        # wrap:
    except Exception as e:
        return str(e)
    return None


def try_load2(path: Path) -> str | None:
    from lupa import LuaRuntime

    lua = LuaRuntime(unpack_returned_tuples=True)
    src = path.read_text(encoding="utf-8")
    if src.startswith("\ufeff"):
        src = src[1:]
    # Convert `return X` into assignment so execute works
    body = src
    if body.lstrip().startswith("return"):
        body = "local __mod_items = " + body.lstrip()[len("return") :]
    try:
        lua.execute(PRELUDE + "\n" + body)
    except Exception as e:
        return str(e)
    return None


def main() -> int:
    failed = False
    for name in ("items.lua", "metadata.lua"):
        err = try_load2(ROOT / name)
        if err:
            failed = True
            print(f"FAIL {name}: {err}")
        else:
            print(f"OK {name} lupa load")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
