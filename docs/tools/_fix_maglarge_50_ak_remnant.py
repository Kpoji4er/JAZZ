# -*- coding: utf-8 -*-
"""Fix items.lua: remove broken MagLarge_50_AK remnant (id = }),) and audit similar."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ITEMS = ROOT / "items.lua"
sys.path.insert(0, str(ROOT / "docs" / "tools"))


def main() -> int:
    text = ITEMS.read_text(encoding="utf-8")
    # Pattern: PlaceObj WeaponComponent whose id line is corrupt `id = }),`
    # Match from PlaceObj start that contains the AK MagLarge_50 comment through id = }),
    pat = re.compile(
        r"PlaceObj\('ModItemWeaponComponent',\s*\{"
        r"(?:(?!PlaceObj\('ModItemWeaponComponent').)*?"
        r'comment = "Mag family AK — split from JAZZ_MagLarge_50",'
        r"(?:(?!PlaceObj\('ModItemWeaponComponent').)*?"
        r"id = \}\),?\s*\n",
        re.S,
    )
    m = pat.search(text)
    if not m:
        # fallback: any id = }),
        print("AK-specific block not matched; trying generic id = }),")
        # find line and walk back to PlaceObj
        idx = text.find("id = }),")
        if idx < 0:
            print("no id = }), found")
            return 1
        start = text.rfind("PlaceObj('ModItemWeaponComponent'", 0, idx)
        end = idx + len("id = }),")
        while end < len(text) and text[end] in "\r\n":
            end += 1
        text2 = text[:start] + text[end:]
    else:
        print(f"removing AK MagLarge_50 block chars={m.end()-m.start()} at L{text[:m.start()].count(chr(10))+1}")
        text2 = text[: m.start()] + text[m.end() :]

    # Audit remaining corruptions
    bad = []
    for i, ln in enumerate(text2.splitlines(), 1):
        s = ln.strip()
        if re.match(r"^id\s*=\s*\}\),?\s*$", s):
            bad.append(i)
        if re.search(r'id\s*=\s*$', s):
            bad.append(i)
    print("remaining corrupt id lines:", bad)

    from _validate_items_quick import missing_comma_before_placeobj, check

    # write
    if "--apply" in sys.argv:
        tmp = ITEMS.with_suffix(".lua.tmp_fix_ak50")
        tmp.write_text(text2, encoding="utf-8")
        tmp.replace(ITEMS)
        print("wrote items.lua")
        problems = []
        for name in ("items.lua", "metadata.lua"):
            problems.extend(check(ROOT / name))
        if problems:
            print("FAIL validate")
            for p in problems:
                print(" -", p)
            return 1
        print("OK validate")
    else:
        print("dry-run; pass --apply")
        # still show comma check on proposed text
        mc = missing_comma_before_placeobj(text2, "items.lua")
        print("missing commas in result:", mc)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
