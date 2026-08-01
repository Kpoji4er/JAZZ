# -*- coding: utf-8 -*-
from pathlib import Path

items = Path("items.lua").read_text(encoding="utf-8")
start = items.rfind("PlaceObj('ModItemCombatAction'", 0, items.find('id = "Reload"'))
# walk to matching close for this PlaceObj
i = start + len("PlaceObj('ModItemCombatAction'")
# find opening {
while items[i] != "{":
    i += 1
depth = 0
in_str = None
escape = False
long = False
j = i
while j < len(items):
    ch = items[j]
    if long:
        if items.startswith("]]", j):
            long = False
            j += 2
            continue
        j += 1
        continue
    if in_str:
        if escape:
            escape = False
        elif ch == "\\":
            escape = True
        elif ch == in_str:
            in_str = None
        j += 1
        continue
    if items.startswith("--[[", j):
        # long comment
        endc = items.find("]]", j + 4)
        j = endc + 2 if endc >= 0 else j + 4
        continue
    if items.startswith("--", j):
        nl = items.find("\n", j)
        j = nl + 1 if nl >= 0 else len(items)
        continue
    if ch in ("'", '"'):
        in_str = ch
        j += 1
        continue
    if items.startswith("[[", j):
        long = True
        j += 2
        continue
    if ch == "{":
        depth += 1
    elif ch == "}":
        depth -= 1
        if depth == 0:
            # expect ),
            end = j + 1
            while end < len(items) and items[end] in " \t\r\n":
                end += 1
            if items.startswith("),", end):
                end += 2
            block = items[start:end]
            print("block lines", block.count("\n") + 1)
            print("block chars", len(block))
            print("naive ()", block.count("(") - block.count(")"))
            print("naive {}", block.count("{") - block.count("}"))
            print("tail", repr(block[-80:]))
            print("head", repr(block[:80]))
            # write for lua check
            Path("docs/tools/_tmp_reload_block.lua").write_text("local x = " + block + "\nreturn x\n", encoding="utf-8")
            break
    j += 1
else:
    print("FAILED to find end, depth", depth)

# Also: can luajit/lua parse? try via python lupa if available, else tokenize
try:
    import subprocess, shutil
    lua = shutil.which("lua") or shutil.which("luajit")
    if lua:
        r = subprocess.run([lua, "-e", "assert(loadfile([[docs/tools/_tmp_reload_block.lua]]))"], capture_output=True, text=True)
        print("lua check", r.returncode, r.stderr[:500])
    else:
        print("no lua binary")
except Exception as e:
    print("lua err", e)
