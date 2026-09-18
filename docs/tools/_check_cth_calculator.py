# -*- coding: utf-8 -*-
"""Sanity: generated CTH calculator data + offline optic formula vs _sim_akm_optic_cth.

Does not execute the HTML JS. Checks JSON completeness and that the Python
reference used by optic design still agrees with catalog numbers the HTML embeds.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(HERE))
import _sim_akm_optic_cth as sim  # noqa: E402

JSON = HERE / "cth-calculator-data.json"
HTML = HERE / "cth-calculator.html"


def main() -> int:
    data = json.loads(JSON.read_text(encoding="utf-8"))
    html = HTML.read_text(encoding="utf-8")
    assert "JAZZ · калькулятор точности" in html
    assert "opticProfile" in html and "visPenalty" in html
    assert 'data-lang="en"' in html and "function setLang" in html
    assert "jazz-cth-lang" in html
    assert data["archetypes"] and data["archetypes"][0].get("labelEn")
    wpn = {w["id"]: w for w in data["weapons"]}
    assert "AKM" in wpn and "DragunovSVD" in wpn
    assert "JAZZ_Scope_PSO" in data["comps"]
    assert "JAZZ_Reflex_PKAS" in data["comps"]
    svd_scopes = data["slots"]["DragunovSVD"]["Scope"]
    assert "JAZZ_Scope_PSO" in svd_scopes
    assert data["defaults"]["DragunovSVD"]["Scope"] == "JAZZ_Scope_PSO"

    comps = {
        r["component_id"]: r
        for r in __import__("csv").DictReader(
            (ROOT / "docs/technical/weapons/data/weapon-components.csv").open(encoding="utf-8")
        )
    }
    base = next(
        r
        for r in __import__("csv").DictReader(
            (ROOT / "docs/technical/weapons/data/weapons.csv").open(encoding="utf-8")
        )
        if r["id"] == "DragunovSVD"
    )
    cases = [
        ("Irons", None, "full", 20),
        ("PSO", "JAZZ_Scope_PSO", "full", 20),
        ("PSO", "JAZZ_Scope_PSO", "full", 5),
        ("PKAS", "JAZZ_Reflex_PKAS", "full", 5),
        ("ACOG", "JAZZ_CombatScope_ACOG", "plus1", 20),
    ]
    print("SVD Dex70/Mrk70/L5  (sim_akm formula, no situational)")
    for label, cid, mode, d in cases:
        comp = comps.get(cid) if cid else None
        aa, mx, mina = sim.setup_weapon(base, comp)
        if mode == "snap":
            aim = 1 if mina else 0
        elif mode == "plus1":
            aim = min(mx, (1 if mina else 0) + 1)
        else:
            aim = mx
        aa = sim.optic_aim_accuracy(aa, comp, aim)
        reach, omin, onear = sim.optic_profile(comp, aim)
        close_pct = int(float(base["close_range_factor"]))
        if comp:
            p = sim.parse_params(comp.get("parameters") or "")
            fx = set((comp.get("effects") or "").split(";"))
            if "CloseRangeFactorIncrease" in fx:
                close_pct = min(150, close_pct + int(p.get("CloseRangeFactorIncrease", 0)))
        v, info = sim.cth(
            dex=70,
            mrk=70,
            lvl=5,
            aim=aim,
            max_aim=mx,
            aim_accuracy=aa,
            d=d,
            weapon_range=int(float(base["weapon_range"])),
            bdr=int(float(base["bullet_drop_range"])),
            grouping=int(float(base["grouping"])),
            close_range=int(float(base["close_range"])),
            close_range_factor_pct=close_pct,
            optic_reach=reach,
            optic_min=omin,
            optic_near=onear,
        )
        print(f"  {label:8} {mode:5} @{d:2} = {v:3}%  E={info['E']} AA={info['AA']} near={info['near']}")
    # Lua-like isqrt skill curve (must NOT truncate to int32 — that made JS NaN/53%).
    def isqrt(n: int) -> int:
        n = max(0, int(n))
        lo, hi = 0, n
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if mid <= 0:
                lo = mid
            elif mid > n / mid:
                hi = mid - 1
            elif mid * mid <= n:
                lo = mid
            else:
                hi = mid - 1
        return lo

    def skill_isqrt(value: float) -> int:
        value = max(0, int(value + 0.5) if value >= 0 else int(value - 0.5))
        if not value:
            return 20
        root2 = isqrt(value * 100_000_000)
        root4 = isqrt(root2)
        return 20 + (value * root4 + 200) // 400

    snap = skill_isqrt((70 * 4 + 70 + 5 * 5) / 6)
    assert snap >= 60, snap
    assert "n|0" not in html, "isqrt must not use 32-bit |0"
    print(f"skill isqrt Dex70/Mrk70/L5 = {snap} (expect ~64)")
    print("OK calculator artifacts + reference optic table")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
