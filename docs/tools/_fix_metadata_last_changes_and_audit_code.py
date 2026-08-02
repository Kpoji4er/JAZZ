"""Fix raw newline in metadata.lua last_changes; audit metadata.code paths vs disk/git."""
from __future__ import annotations

import os
import re
import subprocess
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
META = os.path.join(ROOT, "metadata.lua")


def main() -> int:
    with open(META, "rb") as f:
        data = f.read()

    broken = b"recoil\n- Fix weapon jam"
    fixed = b"recoil\\n- Fix weapon jam"
    count = data.count(broken)
    print(f"broken_pattern_count={count}")
    if count == 1:
        data = data.replace(broken, fixed, 1)
        with open(META, "wb") as f:
            f.write(data)
        print("WROTE: escaped raw newline in last_changes first bullet")
    elif count == 0:
        print("OK: broken raw-newline pattern already absent")
    else:
        print(f"FAIL: expected 0 or 1 broken patterns, got {count}", file=sys.stderr)
        return 1

    # Verify last_changes string has no raw newlines
    marker = b"'last_changes', "
    i = data.find(marker)
    if i < 0:
        print("FAIL: last_changes marker missing", file=sys.stderr)
        return 1
    assert data[i + len(marker) : i + len(marker) + 1] == b'"'
    j = i + len(marker) + 1
    while j < len(data):
        if data[j : j + 1] == b"\\":
            j += 2
            continue
        if data[j : j + 1] == b'"':
            break
        if data[j : j + 1] in (b"\n", b"\r"):
            print(f"FAIL: raw newline still in last_changes at {j}", file=sys.stderr)
            return 1
        j += 1
    else:
        print("FAIL: closing quote for last_changes not found", file=sys.stderr)
        return 1
    print(f"last_changes_ok length={j - (i + len(marker) + 1)}")

    text = data.decode("utf-8")
    m = re.search(r"'code'\s*,\s*\{", text)
    if not m:
        print("FAIL: no 'code' block", file=sys.stderr)
        return 1
    start = m.end()
    depth = 1
    i = start
    while i < len(text) and depth:
        c = text[i]
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
        i += 1
    block = text[start : i - 1]
    paths = re.findall(r'"([^"]+)"', block)
    print(f"code_entries={len(paths)}")

    git_list = (
        subprocess.check_output(["git", "ls-files", "-z"], cwd=ROOT).split(b"\0")
    )
    git_map = {p.decode("utf-8").lower(): p.decode("utf-8") for p in git_list if p}

    disk: dict[str, str] = {}
    skip_prefixes = (".git/", "docs/", ".agents/", ".cursor/", "node_modules/")
    for dirpath, _dirnames, filenames in os.walk(ROOT):
        base = os.path.relpath(dirpath, ROOT).replace("\\", "/")
        if base == ".":
            base = ""
        if any((base + "/").startswith(p) for p in skip_prefixes):
            continue
        for fn in filenames:
            rel = fn if not base else f"{base}/{fn}"
            disk[rel.lower()] = rel

    missing: list[str] = []
    case_mm: list[tuple[str, str | None, str | None]] = []
    ok = 0
    mas_entries: list[str] = []
    for p in paths:
        pl = p.lower()
        if "mas36" in pl:
            mas_entries.append(p)
        disk_exact = disk.get(pl)
        git_exact = git_map.get(pl)
        full = os.path.join(ROOT, *p.split("/"))
        exists = os.path.isfile(full)
        if not exists and not disk_exact:
            missing.append(p)
        elif (git_exact and git_exact != p) or (disk_exact and disk_exact != p):
            case_mm.append((p, git_exact, disk_exact))
        else:
            ok += 1

    print(f"OK={ok}")
    print(f"MISSING={len(missing)}")
    for p in missing:
        print(f"  MISSING {p}")
    print(f"CASE_MISMATCH={len(case_mm)}")
    for p, g, d in case_mm:
        print(f"  CASE meta={p!r} git={g!r} disk={d!r}")
    print(f"MAS36_ENTRIES={mas_entries}")

    # MAS36 proof
    for name in ("MAS36.lua", "Mas36.lua", "mas36.lua"):
        full = os.path.join(ROOT, "InventoryItem", name)
        # os.path.isfile is case-insensitive on Windows; use disk map
        exact = disk.get(f"inventoryitem/{name}".lower())
        print(f"disk_lookup {name!r} -> {exact!r} isfile={os.path.isfile(full)}")

    idx = subprocess.check_output(
        ["git", "ls-files", "-s", "--", "InventoryItem/MAS36.lua", "InventoryItem/Mas36.lua"],
        cwd=ROOT,
        text=True,
    )
    print("git_index:\n" + (idx.strip() or "(empty)"))

    # Show metadata InventoryItem/MAS* lines
    for line in text.splitlines():
        if "InventoryItem/" in line and "as36" in line.lower():
            print("META_PATH_LINE:", line.strip())

    # Lua parse smoke: unfinished string near last_changes must not occur
    # Approximate: if first 20 lines contain an odd number of unescaped " in last_changes line only
    lines = text.splitlines()
    print(f"metadata_line8_prefix={lines[7][:80]!r}" if len(lines) > 7 else "short")
    return 0 if not missing else 2


if __name__ == "__main__":
    raise SystemExit(main())
