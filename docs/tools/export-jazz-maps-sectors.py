#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Export ModItemSector rows from jazz-maps items.lua (+ metadata index).

Does NOT recurse Maps/. Reads only items.lua / metadata.lua.

Usage (from jazz/):
  python docs/tools/export-jazz-maps-sectors.py
  python docs/tools/export-jazz-maps-sectors.py --maps-root ../jazz-maps --out ../jazz-maps/docs/content/data

Outputs:
  sectors-runtime.json
  sectors-runtime.csv
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from pathlib import Path

MODITEM_SPLIT = re.compile(r"PlaceObj\(\s*'ModItemSector'\s*,\s*\{")
FIELD_STR = re.compile(r"'(%s)'\s*,\s*\"((?:\\.|[^\"])*)\"" % "|".join(
    ("comment", "mapName", "campaignId", "sectorId")
))
DISPLAY_NAME = re.compile(
    r"'display_name'\s*,\s*T\(\s*\d+\s*,\s*\"((?:\\.|[^\"])*)\"\s*\)"
)
LABEL1 = re.compile(r"'Label1'\s*,\s*\"((?:\\.|[^\"])*)\"")
CITY = re.compile(r"'City'\s*,\s*\"((?:\\.|[^\"])*)\"")
WEATHER = re.compile(r"'WeatherZone'\s*,\s*\"((?:\\.|[^\"])*)\"")
META_ID = re.compile(r"'Id'\s*,\s*\"HotDiamonds_([^\"]+)\"")


def unescape(s: str) -> str:
    return s.replace('\\"', '"').replace("\\n", "\n")


def parse_moditem_block(block: str) -> dict | None:
    fields: dict[str, str] = {}
    for key, val in FIELD_STR.findall(block):
        fields[key] = unescape(val)
    sector_id = fields.get("sectorId")
    if not sector_id:
        return None
    dn = DISPLAY_NAME.search(block)
    label = LABEL1.search(block)
    city = CITY.search(block)
    weather = WEATHER.search(block)
    underground = sector_id.endswith("_Underground") or "_Underground" in sector_id
    return {
        "sectorId": sector_id,
        "mapName": fields.get("mapName", ""),
        "campaignId": fields.get("campaignId", ""),
        "comment": fields.get("comment", ""),
        "display_name": unescape(dn.group(1)) if dn else "",
        "Label1": unescape(label.group(1)) if label else "",
        "City": unescape(city.group(1)) if city else "",
        "WeatherZone": unescape(weather.group(1)) if weather else "",
        "underground": underground,
    }


def parse_items(items_path: Path) -> list[dict]:
    text = items_path.read_text(encoding="utf-8", errors="replace")
    parts = MODITEM_SPLIT.split(text)
    rows: list[dict] = []
    seen: set[str] = set()
    for part in parts[1:]:
        # truncate at next top-level-ish ModItem close heuristic: next PlaceObj('Mod
        end = part.find("PlaceObj('Mod")
        block = part if end < 0 else part[:end]
        # also stop at nested SatelliteSector end — fields we need are near the start
        block = block[:8000]
        row = parse_moditem_block(block)
        if not row:
            continue
        sid = row["sectorId"]
        if sid in seen:
            continue
        seen.add(sid)
        rows.append(row)
    rows.sort(key=lambda r: (r["underground"], r["sectorId"]))
    return rows


def parse_metadata_ids(meta_path: Path) -> set[str]:
    text = meta_path.read_text(encoding="utf-8", errors="replace")
    return set(META_ID.findall(text))


def sector_sort_key(sid: str):
    m = re.match(r"^([A-P])(\d+)(_Underground)?$", sid)
    if not m:
        return (99, 0, sid)
    return (ord(m.group(1)) - ord("A"), int(m.group(2)), 1 if m.group(3) else 0, sid)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--maps-root",
        type=Path,
        default=Path(__file__).resolve().parents[3] / "jazz-maps",
        help="Path to jazz-maps package root",
    )
    ap.add_argument(
        "--out",
        type=Path,
        default=None,
        help="Output directory (default: <maps-root>/docs/content/data)",
    )
    args = ap.parse_args()
    maps_root: Path = args.maps_root.resolve()
    out_dir: Path = (args.out or (maps_root / "docs" / "content" / "data")).resolve()
    items = maps_root / "items.lua"
    meta = maps_root / "metadata.lua"
    if not items.is_file():
        print(f"ERROR: missing {items}", file=sys.stderr)
        return 1
    rows = parse_items(items)
    meta_ids = parse_metadata_ids(meta) if meta.is_file() else set()
    for row in rows:
        row["in_metadata"] = row["sectorId"] in meta_ids
    out_dir.mkdir(parents=True, exist_ok=True)
    json_path = out_dir / "sectors-runtime.json"
    csv_path = out_dir / "sectors-runtime.csv"
    payload = {
        "source": str(items).replace("\\", "/"),
        "campaign": "HotDiamonds",
        "count": len(rows),
        "surface": sum(1 for r in rows if not r["underground"]),
        "underground": sum(1 for r in rows if r["underground"]),
        "sectors": rows,
    }
    json_path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    fields = [
        "sectorId",
        "mapName",
        "display_name",
        "comment",
        "Label1",
        "City",
        "WeatherZone",
        "underground",
        "in_metadata",
        "campaignId",
    ]
    with csv_path.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        for r in sorted(rows, key=lambda x: sector_sort_key(x["sectorId"])):
            w.writerow(r)
    missing_meta = [r["sectorId"] for r in rows if not r["in_metadata"]]
    orphan_meta = sorted(meta_ids - {r["sectorId"] for r in rows})
    print(f"Wrote {json_path}")
    print(f"Wrote {csv_path}")
    print(
        f"ModItemSector={len(rows)} surface={payload['surface']} "
        f"underground={payload['underground']}"
    )
    if missing_meta:
        print(f"WARN items without metadata Id: {len(missing_meta)}")
    if orphan_meta:
        print(f"WARN metadata HotDiamonds_* without ModItem parse: {len(orphan_meta)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
