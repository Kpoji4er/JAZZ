# -*- coding: utf-8 -*-
"""Annotate bobby_weapon_prices.json with CanAppearInShop action needed."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
INV = ROOT / "InventoryItem"
AUDIT = ROOT / ".tmp/bobby_weapon_prices.json"


def companion_cas(wid: str) -> tuple[str, str]:
    """Return (state, relpath): state in true|false|unset|missing."""
    paths = list(INV.rglob(f"{wid}.lua"))
    if not paths:
        return "missing", ""
    rel = str(paths[0].relative_to(ROOT)).replace("\\", "/")
    t = paths[0].read_text(encoding="utf-8", errors="replace")
    m = re.search(r"CanAppearInShop\s*=\s*(true|false)", t)
    if not m:
        return "unset", rel
    return m.group(1), rel


def main() -> None:
    rows = json.loads(AUDIT.read_text(encoding="utf-8"))
    set_false = 0
    for r in rows:
        state, path = companion_cas(r["id"])
        r["cas_now"] = state
        r["cas_path"] = path
        if r["shop"] == "bobby":
            r["cas_action"] = "keep"
            if state == "false":
                r["cas_label"] = "warn: false but in Bobby plan"
            elif state == "true":
                r["cas_label"] = "ok true"
            elif state == "unset":
                r["cas_label"] = "ok unset(in shop)"
            else:
                r["cas_label"] = "missing file"
            continue

        # out of Bobby → need false
        if state == "false":
            r["cas_action"] = "ok_false"
            r["cas_label"] = "уже false"
        else:
            r["cas_action"] = "SET_FALSE"
            set_false += 1
            if state == "true":
                r["cas_label"] = "SET false (сейчас true)"
            elif state == "unset":
                r["cas_label"] = "SET false (пропа нет, в shop)"
            else:
                r["cas_label"] = "SET false (нет файла?)"

    AUDIT.write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"SET_FALSE needed: {set_false}")
    print("---")
    for r in sorted(rows, key=lambda x: (x["shop"], x["tier"], x["id"])):
        if r["cas_action"] == "SET_FALSE":
            print(f"{r['cas_label']:32} {r['shop']:12} {r['tier']:7} {r['id']:24} {r['name']}")


if __name__ == "__main__":
    main()
