#!/usr/bin/env python3
"""Wire Legion schematic Portrait paths into UnitData companions + items.lua."""

from __future__ import annotations

import json
import re
from pathlib import Path

JAZZ = Path(__file__).resolve().parents[2]
UNITS = JAZZ.parent / "jazz-units"
CATALOG = JAZZ / "docs/design/_legion-unit-portraits/catalog.json"


def main() -> int:
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    id_to_file = {u["id"]: u["file"] for u in catalog["units"]}
    ud_dir = UNITS / "UnitData"
    items_path = UNITS / "items.lua"

    changed_ud = []
    for uid, fname in id_to_file.items():
        path = f"Mod/Dv3mFVN/EnemyPortraits/Legion/{fname}"
        f = ud_dir / f"{uid}.lua"
        text = f.read_text(encoding="utf-8")
        new, n = re.subn(
            r'Portrait\s*=\s*"[^"]+"',
            f'Portrait = "{path}"',
            text,
            count=1,
        )
        if n != 1:
            raise SystemExit(f"Portrait replace fail {uid}: {n}")
        if new != text:
            f.write_text(new, encoding="utf-8", newline="\n")
            changed_ud.append(uid)

    items_text = items_path.read_text(encoding="utf-8")
    out = items_text
    touched = 0
    for uid, fname in id_to_file.items():
        path = f"Mod/Dv3mFVN/EnemyPortraits/Legion/{fname}"
        pat = re.compile(
            rf"('Id'\s*,\s*\"{re.escape(uid)}\"[\s\S]{{0,2500}}?'Portrait'\s*,\s*)\"[^\"]*\"",
            re.M,
        )
        out2, n = pat.subn(rf'\1"{path}"', out, count=1)
        if n != 1:
            raise SystemExit(f"items Portrait replace fail {uid}: {n}")
        if out2 != out:
            touched += 1
        out = out2

    if out != items_text:
        items_path.write_text(out, encoding="utf-8", newline="\n")

    print(f"UnitData changed: {len(changed_ud)}")
    print(f"items blocks touched: {touched}")
    for sample in (
        "JAZZ_Legion_FrontT3_Sniper",
        "JAZZ_Legion_Recruit",
        "JAZZ_Legion_HeavyT2_Grenadier",
        "JAZZ_Legion_GunnerT1_Gunner",
    ):
        t = (ud_dir / f"{sample}.lua").read_text(encoding="utf-8")
        m = re.search(r'Portrait\s*=\s*"([^"]+)"', t)
        print(f"  {sample} -> {m.group(1) if m else None}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
