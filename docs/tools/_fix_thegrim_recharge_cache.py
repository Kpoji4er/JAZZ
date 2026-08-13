# -*- coding: utf-8 -*-
"""UNITS-006 Reaper TheGrim: fix 5-kill recharge (g_PresetParamCache + wrap reinstall).

Runtime fix lives in Code/System_NamedPerks.lua:
- Jazz_EnsureTheGrimRechargeOnKill → cache.recharge_on_kill = 5
- lInstallTheGrimMultiKillRecharge reinstalls wraps if ModsReloaded dropped them

This script bumps metadata + refreshes tool README note.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
META = ROOT / "metadata.lua"
TECH = ROOT / "docs/technical/systems/units-progression-specializations.md"
README = ROOT / "docs/tools/README.md"


def bump_meta() -> None:
    text = META.read_text(encoding="utf-8")
    m = re.search(r"'version',\s*(\d+)", text)
    ver = int(m.group(1)) + 1
    text = re.sub(r"'version',\s*\d+", f"'version', {ver}", text, count=1)
    bullet = (
        "- UNITS-006: Reaper TheGrim — fix 5-kill CD (PresetParamCache + wrap reinstall) "
        "[no new game]\\n"
    )
    m2 = re.search(r"'last_changes',\s*\"", text)
    i = m2.end()
    if "TheGrim — fix 5-kill CD" not in text[i : i + 200]:
        text = text[:i] + bullet + text[i:]
    META.write_text(text, encoding="utf-8")
    print(f"metadata version -> {ver}")


def patch_docs() -> None:
    if TECH.exists():
        t = TECH.read_text(encoding="utf-8")
        t2, n = re.subn(
            r"- \*\*Reaper `TheGrim`:\*\*[^\n]+",
            "- **Reaper `TheGrim`:** stock crit + Panic ≤8 on signature kill; CD needs **5** kills "
            "(`Jazz_TheGrimKillsToRecharge`; `g_PresetParamCache.recharge_on_kill=5` via "
            "`Jazz_EnsureTheGrimRechargeOnKill`; multi-kill hold in `UpdateSignatureRecharges`). "
            "Tooltip shows `done/need`.",
            t,
            count=1,
        )
        if n:
            TECH.write_text(t2, encoding="utf-8")
            print("updated technical")

    entry = (
        "| `_fix_thegrim_recharge_cache.py` | Reaper TheGrim: docs/meta bump for "
        "`g_PresetParamCache` + wrap-reinstall fix (runtime in System_NamedPerks). |\n"
    )
    rt = README.read_text(encoding="utf-8")
    if "_fix_thegrim_recharge_cache.py" not in rt:
        if "| `_apply_thegrim_recharge_5kills.py`" in rt:
            rt = rt.replace(
                "| `_apply_thegrim_recharge_5kills.py`",
                entry + "| `_apply_thegrim_recharge_5kills.py`",
            )
        else:
            rt += "\n" + entry
        README.write_text(rt, encoding="utf-8")


def main() -> None:
    bump_meta()
    patch_docs()
    print("OK TheGrim cache/wrap fix documented")


if __name__ == "__main__":
    main()
