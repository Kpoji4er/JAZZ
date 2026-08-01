# -*- coding: utf-8 -*-
from pathlib import Path
import subprocess

def nest_sample(path: str, needle: str, before: int = 5, after: int = 15) -> None:
    lines = Path(path).read_text(encoding="utf-8").splitlines()
    for i, line in enumerate(lines):
        if needle in line:
            print(f"--- {path} @{i+1} ---")
            for j in range(max(0, i - before), min(len(lines), i + after)):
                print(f"{j+1}: {lines[j]}")
            return
    print(path, "needle not found", needle)


nest_sample("items.lua", 'id = "MeleeAttack"')
nest_sample("items.lua.bak_legacy_parts", 'id = "MeleeAttack"')
nest_sample("items.lua", 'id = "Reload"')

raw = subprocess.check_output(["git", "show", "HEAD:metadata.lua"])
print("HEAD meta BOM", raw[:3] == b"\xef\xbb\xbf", "len", len(raw))
print("HEAD Reload resource", b"'Id', \"Reload\"" in raw)
cur = Path("metadata.lua").read_bytes()
print("CUR meta BOM", cur[:3] == b"\xef\xbb\xbf", "len", len(cur))
print("CUR Reload resource", b"'Id', \"Reload\"" in cur)
print("resource presets HEAD/CUR", raw.count(b"ModResourcePreset"), cur.count(b"ModResourcePreset"))

# Strip BOM test file? just report if ModDef parse would see BOM char
text = Path("metadata.lua").read_text(encoding="utf-8")
print("first char ord", ord(text[0]), "is BOM", text[0] == "\ufeff")
