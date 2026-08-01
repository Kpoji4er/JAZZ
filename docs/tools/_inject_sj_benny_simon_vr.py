# -*- coding: utf-8 -*-
"""Inject missing ModItemVoiceResponse for Jazz_Benny / Jazz_Simon into items.lua.

UnitData companions already load via metadata.code, but VoiceResponse presets were
orphaned in metadata without items.lua bodies → silent mercs.

Inserts folders after Jazz_Grom folder (or appends before TranslatedVoices root).
Then run: _expand_ja2_merc_vr_full.py --only benny,simon
          _ship_ja2_merc_voices.py --only benny,simon

Usage (jazz/):
  python docs/tools/_inject_sj_benny_simon_vr.py --dry-run
  python docs/tools/_inject_sj_benny_simon_vr.py
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

JU = Path(r"C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz-units")
ITEMS = JU / "items.lua"

UNITS = ("Jazz_Benny", "Jazz_Simon")


def empty_vr(uid: str) -> str:
    return (
        f"\t\t\t\tPlaceObj('ModItemVoiceResponse', {{\n"
        f'\t\t\t\t\tgroup = "MercenariesOld",\n'
        f'\t\t\t\t\tid = "{uid}",\n'
        f"\t\t\t\t}}),"
    )


def folder_block(uid: str) -> str:
    # Minimal folder: VR only (UnitData already via companion CodeFileName).
    return (
        f"\t\t\tPlaceObj('ModItemFolder', {{\n"
        f"\t\t\t\t'name', \"{uid}\",\n"
        f"\t\t\t}}, {{\n"
        f"{empty_vr(uid)}\n"
        f"\t\t\t}}),"
    )


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    items = ITEMS.read_text(encoding="utf-8")
    missing = [u for u in UNITS if f'id = "{u}"' not in items and f"'id', \"{u}\"" not in items]
    if not missing:
        print("OK: Benny/Simon VR already in items.lua")
        return 0

    blocks = "\n".join(folder_block(u) for u in missing)
    # Insert after Jazz_Grom folder close — find Jazz_Rothman folder (follows Grom)
    anchor = "\t\t\tPlaceObj('ModItemFolder', {\n\t\t\t\t'name', \"Jazz_Rothman\","
    if anchor not in items:
        anchor = "PlaceObj('ModItemTranslatedVoices', {\n\t\t'name', \"TranslatedVoices\",\n\t\t'language', \"Any\",\n\t\t'translatedVoicesFolder'"
        if anchor not in items:
            print("FAIL: no insert anchor")
            return 1
        items = items.replace(anchor, blocks + "\n\t" + anchor, 1)
    else:
        items = items.replace(anchor, blocks + "\n" + anchor, 1)

    print(f"Inject VR folders: {missing}")
    if args.dry_run:
        print("DRY: not written")
        return 0
    ITEMS.write_text(items, encoding="utf-8")
    print("Wrote", ITEMS)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
