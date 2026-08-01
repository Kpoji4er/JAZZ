# -*- coding: utf-8 -*-
"""Replace Cyrillic leaks in jazz English.csv for workshop AIM mercs with real EN.

Source priority for English Translation/Text:
  1. Standalone `Merc_*` workshop packs — non-Cyrillic T() bodies (Annie/Hector/… EN)
  2. Cached donor TSV under `docs/tools/_donors/workshop_merc_en/<MercId>.tsv`
     (Carol: extracted from Steam Workshop `3023246026` ModContent.hpk — AppData
     `Merc_ Carol Thompson` was re-saved with RU baked into T() bodies)
  3. Optional `--extract DIR` (unpacked Steam/HPK or fresh Merc_* copy)
  4. Hand invents `CAROL_EN` from `_seed_workshop_merc_loc.py` (hire/UI only)
  5. Same-T-id / VR-category pairing against Otherguy short-folder aliases when EN

Does not invent machine-translated combat VR. Marks invents in the summary.

Usage (jazz/):
  python docs/tools/_fix_workshop_merc_en_from_sources.py --dry-run
  python docs/tools/_fix_workshop_merc_en_from_sources.py --apply
  python docs/tools/_fix_workshop_merc_en_from_sources.py --cache-extract DIR --merc Merc_CarolThompson
"""
from __future__ import annotations

import argparse
import csv
import io
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

JAZZ = Path(r"C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz")
JU = Path(r"C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz-units")
MODS = JAZZ.parent
DONOR_DIR = JAZZ / "docs" / "tools" / "_donors" / "workshop_merc_en"

MERCS = {
    "Merc_AnnieDubois": "Merc_ Annie Dubois",
    "Merc_CarolThompson": "Merc_ Carol Thompson",
    "Merc_HectorSanchez": "Merc_ Hector Sanchez",
    "Merc_JerrySinclair": "Merc_ Jerry Sinclair",
    "Merc_MildredPatterson": "Merc_ Mildred Patterson",
    "Merc_SamuelNkosi": "Merc_ Samuel Nkosi",
}

CYR = re.compile(r"[\u0400-\u04FF]")
T_ANY = re.compile(
    r"T\((\d+)\s*,\s*--\[\[[^\]]*\]\]\s*(['\"])((?:\\.|(?!\2).)*)\2",
    re.S,
)

sys.path.insert(0, str(JAZZ / "docs" / "tools"))
from _loc_csv_io import load_rows, write_rows  # noqa: E402
from _seed_workshop_merc_loc import CAROL_EN  # noqa: E402


def looks_cyrillic(s: str) -> bool:
    return bool(CYR.search(s or ""))


def unescape(s: str, q: str) -> str:
    s = s.replace("\\n", "\n").replace("\\\\", "\\")
    return s.replace('\\"', '"') if q == '"' else s.replace("\\'", "'")


def parse_t(blob: str) -> dict[str, str]:
    out: dict[str, str] = {}
    for m in T_ANY.finditer(blob or ""):
        out[m.group(1)] = unescape(m.group(3), m.group(2))
    return out


def folder_slice(items: str, merc: str) -> str:
    m = re.search(
        rf"PlaceObj\('ModItemFolder',\s*\{{\s*'name',\s*\"{re.escape(merc)}\"",
        items,
    )
    if not m:
        return ""
    start = m.start()
    nxt = re.search(r"\n\t\tPlaceObj\('ModItemFolder',", items[start + 10 :])
    end = start + 10 + nxt.start() if nxt else start + 250000
    return items[start:end]


def collect_lua_en_map(root: Path) -> dict[str, str]:
    """tid -> English text from all lua under root (skip Cyrillic bodies)."""
    out: dict[str, str] = {}
    if not root.exists():
        return out
    paths = list(root.rglob("*.lua"))
    if (root / "items.lua").exists() and (root / "items.lua") not in paths:
        paths.append(root / "items.lua")
    for p in paths:
        for tid, text in parse_t(p.read_text(encoding="utf-8", errors="replace")).items():
            if text and not looks_cyrillic(text):
                out[tid] = text
    return out


def load_donor_tsv(merc: str) -> dict[str, str]:
    path = DONOR_DIR / f"{merc}.tsv"
    if not path.exists():
        return {}
    out: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line or line.startswith("#") or "\t" not in line:
            continue
        tid, text = line.split("\t", 1)
        tid = tid.strip()
        if tid and text and not looks_cyrillic(text):
            out[tid] = text.replace("\\n", "\n").replace("\\t", "\t")
    return out


def write_donor_tsv(merc: str, mapping: dict[str, str]) -> Path:
    DONOR_DIR.mkdir(parents=True, exist_ok=True)
    path = DONOR_DIR / f"{merc}.tsv"
    lines = ["# tid\tenglish", f"# merc={merc}"]
    for tid in sorted(mapping, key=lambda x: int(x)):
        text = mapping[tid].replace("\\", "\\\\").replace("\t", "\\t").replace("\n", "\\n")
        lines.append(f"{tid}\t{text}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def ju_active_for_merc(ju_items: str, merc: str) -> dict[str, str]:
    blob = folder_slice(ju_items, merc)
    ud = JU / "UnitData" / f"{merc}.lua"
    if ud.exists():
        blob += "\n" + ud.read_text(encoding="utf-8", errors="replace")
    for p in (JAZZ / "CharacterEffect").glob(f"{merc}*"):
        blob += "\n" + p.read_text(encoding="utf-8", errors="replace")
    for p in (JAZZ / "Code" / "WorkshopMercs").glob(f"{merc}*"):
        blob += "\n" + p.read_text(encoding="utf-8", errors="replace")
    return parse_t(blob)


def extract_vr(blob: str, merc: str) -> dict[str, list[tuple[str, str]]]:
    out: dict[str, list[tuple[str, str]]] = {}
    for m in re.finditer(r"PlaceObj\('ModItemVoiceResponse',", blob):
        win = blob[m.start() : m.start() + 500000]
        mid = re.search(r'id\s*=\s*"([^"]+)"', win)
        if not mid or mid.group(1) != merc:
            continue
        for km in re.finditer(r"(\w+)\s*=\s*TConcat\(\{\s*([\s\S]*?)\}\s*\)", win):
            ordered: list[tuple[str, str]] = []
            for tm in T_ANY.finditer(km.group(2)):
                ordered.append((tm.group(1), unescape(tm.group(3), tm.group(2))))
            if ordered:
                out[km.group(1)] = ordered
        break
    return out


def build_en_donors(
    merc: str, ws_folder: str, ju_items: str, extract: Path | None
) -> dict[str, tuple[str, str]]:
    """jazz_tid -> (english, source_tag)."""
    donors: dict[str, tuple[str, str]] = {}

    def add(tid: str, text: str, tag: str, *, overwrite: bool = False) -> None:
        if not tid or not text or looks_cyrillic(text):
            return
        if tid in donors and not overwrite:
            return
        donors[tid] = (text, tag)

    # 1) Merc_* pack (EN when not RU-baked)
    ws = MODS / ws_folder
    for tid, text in collect_lua_en_map(ws).items():
        add(tid, text, "Merc_*")

    # 2) Cached donor TSV
    for tid, text in load_donor_tsv(merc).items():
        add(tid, text, "donor-tsv", overwrite=True)

    # 3) Explicit extract dir
    if extract and extract.exists():
        for tid, text in collect_lua_en_map(extract).items():
            add(tid, text, "extract", overwrite=True)

    # 4) Hand invents (Carol hire/UI)
    if merc == "Merc_CarolThompson":
        for tid, text in CAROL_EN.items():
            add(tid, text, "CAROL_EN-invent", overwrite=False)

    # 5) VR index pairing: donor EN line -> jazz tid when IDs differ
    ju_vr = extract_vr(ju_items, merc)
    donor_blobs = []
    if ws.exists() and (ws / "items.lua").exists():
        donor_blobs.append(
            ("Merc_*", (ws / "items.lua").read_text(encoding="utf-8", errors="replace"))
        )
    if extract and (extract / "items.lua").exists():
        donor_blobs.append(
            (
                "extract",
                (extract / "items.lua").read_text(encoding="utf-8", errors="replace"),
            )
        )
    # Rebuild VR from donor TSV texts is N/A; pair from extract/Merc items
    for label, blob in donor_blobs:
        dvr = extract_vr(blob, merc)
        for key in set(ju_vr) & set(dvr):
            for (jtid, _jtext), (_dtid, dtext) in zip(ju_vr[key], dvr[key]):
                if looks_cyrillic(dtext):
                    continue
                add(
                    jtid,
                    dtext,
                    f"{label}/VR:{key}",
                    overwrite=(label == "extract"),
                )

    return donors


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument(
        "--extract",
        type=Path,
        help="Unpacked Steam/HPK or Merc_* copy with English T() bodies",
    )
    ap.add_argument(
        "--cache-extract",
        type=Path,
        help="Write donor TSV from extract DIR (non-Cyrillic T()) then exit",
    )
    ap.add_argument(
        "--merc",
        default="Merc_CarolThompson",
        help="Merc id for --cache-extract (default Merc_CarolThompson)",
    )
    args = ap.parse_args()

    if args.cache_extract:
        merc = args.merc
        mapping = collect_lua_en_map(args.cache_extract)
        path = write_donor_tsv(merc, mapping)
        print(f"Cached {len(mapping)} EN T-ids -> {path}")
        return 0

    apply = bool(args.apply) and not args.dry_run
    ju_items = (JU / "items.lua").read_text(encoding="utf-8", errors="replace")
    en_path = JAZZ / "English.csv"
    ru_path = JAZZ / "Russian.csv"
    en_sep, en_fields, en_rows, en_by = load_rows(en_path)
    ru_sep, ru_fields, ru_rows, ru_by = load_rows(ru_path)

    by_merc: dict[str, dict[str, int]] = {}
    source_counts: dict[str, int] = {}
    invent_ids: list[str] = []
    samples: list[str] = []
    total_fixed = total_remain = total_already = 0

    for merc, ws_folder in MERCS.items():
        extract = args.extract if merc == "Merc_CarolThompson" or args.extract else None
        # If default Carol extract path exists and no --extract, use cached TSV only
        donors = build_en_donors(merc, ws_folder, ju_items, extract)
        active = ju_active_for_merc(ju_items, merc)
        stats = {"fixed": 0, "already": 0, "remain": 0, "missing": 0}

        for tid, _src in sorted(active.items(), key=lambda x: int(x[0])):
            row = en_by.get(tid)
            old = (row or {}).get("Translation") or ""
            donor = donors.get(tid)

            if row and not looks_cyrillic(old):
                stats["already"] += 1
                total_already += 1
                continue

            if donor:
                en_text, tag = donor
                stats["fixed"] += 1
                total_fixed += 1
                source_counts[tag.split("/")[0]] = (
                    source_counts.get(tag.split("/")[0], 0) + 1
                )
                if "invent" in tag:
                    invent_ids.append(tid)
                if len(samples) < 12:
                    samples.append(f"{merc} {tid} <- {tag}: {en_text[:70]!r}")
                if apply:
                    if row:
                        row["Text"] = en_text
                        row["Translation"] = en_text
                        row["Context"] = row.get("Context") or "WorkshopMerc"
                    else:
                        new = {k: "" for k in en_fields}
                        new["ID"] = tid
                        new["Text"] = en_text
                        new["Translation"] = en_text
                        new["Context"] = "WorkshopMerc"
                        en_rows.append(new)
                        en_by[tid] = new
                    # Keep Russian.csv Text latin when it was Cyrillic
                    ru_row = ru_by.get(tid)
                    if ru_row and looks_cyrillic(ru_row.get("Text") or ""):
                        ru_row["Text"] = en_text
                continue

            if not row:
                stats["missing"] += 1
            else:
                stats["remain"] += 1
                total_remain += 1

        by_merc[merc] = stats

    print("=== Workshop merc EN from sources ===")
    for merc, st in by_merc.items():
        print(
            f"{merc}: fixed={st['fixed']} already_EN={st['already']} "
            f"remain_CYR={st['remain']} missing={st['missing']}"
        )
    print(
        f"\nTOTAL fixed={total_fixed} already_EN={total_already} "
        f"remain_CYR={total_remain}"
    )
    print(f"Source tags: {source_counts}")
    if invent_ids:
        print(f"INVENT marked ({len(invent_ids)}): {', '.join(invent_ids)}")
    for s in samples:
        print(" ", s)

    # Spot-check Carol after apply path
    carol_active = ju_active_for_merc(ju_items, "Merc_CarolThompson")
    carol_cyr = 0
    for tid in carol_active:
        tr = (en_by.get(tid) or {}).get("Translation") or ""
        # After dry-run, en_by still has old values unless we simulate
        if not apply:
            donor = build_en_donors(
                "Merc_CarolThompson",
                MERCS["Merc_CarolThompson"],
                ju_items,
                args.extract,
            ).get(tid)
            if donor:
                tr = donor[0]
            elif tr and not looks_cyrillic(tr):
                pass
        if looks_cyrillic(tr):
            carol_cyr += 1
    print(f"\nSpot-check Carol EN Cyrillic remaining (projected): {carol_cyr}")

    if apply:
        write_rows(en_path, en_sep, en_fields, en_rows)
        write_rows(ru_path, ru_sep, ru_fields, ru_rows)
        print(f"\nWrote {en_path.name} (+ synced RU Text where Cyrillic)")
    else:
        print("\nDRY-RUN (pass --apply to write)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
