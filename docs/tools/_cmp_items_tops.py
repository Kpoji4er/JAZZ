# -*- coding: utf-8 -*-
from pathlib import Path
import re

def count_top(path):
    t = Path(path).read_text(encoding="utf-8")
    # top-level PlaceObj after return { — lines starting with tab PlaceObj
    tops = re.findall(r"(?m)^\tPlaceObj\('([^']+)'", t)
    folders = [m for m in re.findall(r"(?m)^\tPlaceObj\('ModItemFolder',\s*\{\s*\n\t\t'name',\s*\"([^\"]+)\"", t)]
    print(path, "top PlaceObj", len(tops), "top folders", len(folders))
    print("  types", {k: tops.count(k) for k in sorted(set(tops))})
    print("  first folders", folders[:15])
    return tops, folders

count_top("items.lua")
count_top("items.lua.bak_legacy_parts")
# Did write convert CRLF?
b = Path("items.lua").read_bytes()
print("items CRLF count", b.count(b"\r\n"), "LF-only approx", b.count(b"\n") - b.count(b"\r\n"))
b2 = Path("items.lua.bak_legacy_parts").read_bytes()
print("bak CRLF", b2.count(b"\r\n"), "LF-only", b2.count(b"\n") - b2.count(b"\r\n"))
b3 = Path("metadata.lua").read_bytes()
print("meta BOM", b3[:3], "CRLF", b3.count(b"\r\n"))
