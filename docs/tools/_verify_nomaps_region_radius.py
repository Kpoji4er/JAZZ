#!/usr/bin/env python3
"""Static verify NoMaps auto-region Voronoi / coverage (COMPAT-006 + COMPAT-007)."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
NOMAPS = ROOT.parent / "jazz-nomaps" / "Code" / "NoMaps_Autonomy.lua"


def main() -> int:
    if not NOMAPS.is_file():
        print(f"FAIL: missing {NOMAPS}")
        return 1
    text = NOMAPS.read_text(encoding="utf-8")
    errors: list[str] = []

    m = re.search(r"local\s+AUTO_REGION_RADIUS\s*=\s*(\w+)", text)
    if not m or m.group(1) != "false":
        errors.append("AUTO_REGION_RADIUS must be false (unbounded Voronoi, COMPAT-007)")

    if "local AI_REGION_REV = 2" not in text:
        errors.append("AI_REGION_REV = 2 missing (COMPAT-007 rebuild)")

    if "ai_region_rev" not in text:
        errors.append("ai_region_rev GameVar / wiring missing")

    if re.search(r"best_dist\s*<=\s*8\b", text):
        errors.append("legacy Chebyshev <= 8 still present")

    # Assign must allow unbounded (not radius) OR keep optional cap.
    if "not radius or best_dist <= radius" not in text:
        errors.append("assign must support unbounded radius (not radius or best_dist <= radius)")

    # Soft refresh must collect all tracked outposts before one Voronoi pass.
    refresh = re.search(
        r"local function lRefreshTrackedAutoRegions\(root\)(.*?)\nlocal function ",
        text,
        re.S,
    )
    if not refresh:
        refresh = re.search(
            r"local function lRefreshTrackedAutoRegions\(root\)(.*?)local function lApplyRegionRev",
            text,
            re.S,
        )
    body = refresh.group(1) if refresh else ""
    if "lAssignSectorsToOutposts({ outpost_id })" in body:
        errors.append("lRefreshTrackedAutoRegions still assigns per single outpost")
    if "lAssignSectorsToOutposts(outposts)" not in body:
        errors.append("lRefreshTrackedAutoRegions must Voronoi across outposts list")

    if "function lApplyRegionRev" not in text and "local function lApplyRegionRev" not in text:
        errors.append("lApplyRegionRev missing")

    if errors:
        print("FAIL:")
        for e in errors:
            print(f"  - {e}")
        return 1
    print("OK: COMPAT-007 unbounded region Voronoi static checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
