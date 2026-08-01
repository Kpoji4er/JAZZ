# -*- coding: utf-8 -*-
"""Replace EN-copy invents in jazz Russian.csv for workshop AIM mercs with real RU.

Source priority for Russian Translation:
  1. Standalone workshop mods (`Merc_ Annie Dubois`, …) — Cyrillic T() / Russian.csv
  2. Local aggregate `JAZZ_Otherguy` (author Kpoji4er) — Cyrillic T() when Merc_* has none
  3. Match by same T-id, VoiceResponse category index, then named UnitData/perk fields
     (Otherguy often uses different T-ids for Name/Nick/Bio/Title)

Also patches English.csv when Translation is Cyrillic and a hand invent exists
(`CAROL_EN` from `_seed_workshop_merc_loc.py`).

Does not touch Benny/Simon/Grom. Merc_* Steam packs are EN-only except Carol;
Otherguy is the practical RU donor for the other five.

Usage (jazz/):
  python docs/tools/_fix_workshop_merc_ru_from_sources.py --dry-run
  python docs/tools/_fix_workshop_merc_ru_from_sources.py --apply
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
OTHERGUY = MODS / "JAZZ_Otherguy"

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


def load_csv_loc(folder: Path) -> dict[str, str]:
    """tid -> preferred Russian from CSV Translation if Cyrillic."""
    out: dict[str, str] = {}
    for name in ("Russian.csv", "Localization.csv"):
        p = folder / name
        if not p.exists():
            continue
        _, _, _, by_id = load_rows(p)
        for tid, row in by_id.items():
            tr = row.get("Translation") or ""
            if tid and looks_cyrillic(tr):
                out[tid] = tr
    return out


def collect_lua_map(root: Path) -> dict[str, str]:
    out: dict[str, str] = {}
    if not root.exists():
        return out
    for p in root.rglob("*.lua"):
        out.update(parse_t(p.read_text(encoding="utf-8", errors="replace")))
    return out


def extract_vr(blob: str, merc: str) -> dict[str, list[tuple[str, str]]]:
    out: dict[str, list[tuple[str, str]]] = {}
    for m in re.finditer(r"PlaceObj\('ModItemVoiceResponse',", blob):
        win = blob[m.start() : m.start() + 500000]
        mid = re.search(r'id\s*=\s*"([^"]+)"', win)
        if not mid or mid.group(1) != merc:
            continue
        body = win[: mid.end() + 80]
        for km in re.finditer(r"(\w+)\s*=\s*TConcat\(\{\s*([\s\S]*?)\}\s*\)", body):
            ordered: list[tuple[str, str]] = []
            for tm in T_ANY.finditer(km.group(2)):
                ordered.append((tm.group(1), unescape(tm.group(3), tm.group(2))))
            if ordered:
                out[km.group(1)] = ordered
        break
    return out


FIELD_PAT = re.compile(
    r"[\"']?(Name|Nick|AllCapsNick|Bio|Title|DisplayName|Description|NamePlural)[\"']?\s*=\s*T\((\d+)\s*,\s*--\[\[[^\]]*\]\]\s*(['\"])((?:\\.|(?!\3).)*)\3",
    re.S,
)


def extract_named_fields(blob: str) -> dict[str, tuple[str, str]]:
    """field -> (tid, text). Last win for duplicates."""
    out: dict[str, tuple[str, str]] = {}
    for m in FIELD_PAT.finditer(blob or ""):
        out[m.group(1)] = (m.group(2), unescape(m.group(4), m.group(3)))
    return out


def package_blob(root: Path, merc: str, items_text: str = "") -> str:
    blob = folder_slice(items_text, merc) if items_text else ""
    if not blob and items_text:
        m2 = re.search(
            rf"PlaceObj\('ModItemUnitDataCompositeDef',\s*\{{[\s\S]*?'Id',\s*\"{re.escape(merc)}\"",
            items_text,
        )
        if m2:
            blob = items_text[m2.start() : m2.start() + 50000]
    for sub in ("UnitData", "CharacterEffect", "InventoryItem", "Code"):
        d = root / sub
        if not d.exists():
            continue
        for p in d.glob(f"{merc}*"):
            blob += "\n" + p.read_text(encoding="utf-8", errors="replace")
    if root == JU:
        for p in (JAZZ / "CharacterEffect").glob(f"{merc}*"):
            blob += "\n" + p.read_text(encoding="utf-8", errors="replace")
        for p in (JAZZ / "Code" / "WorkshopMercs").glob(f"{merc}*"):
            blob += "\n" + p.read_text(encoding="utf-8", errors="replace")
    return blob


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


def build_ru_donors(
    merc: str, ws_folder: str, ju_items: str, og_items: str
) -> dict[str, tuple[str, str]]:
    """jazz_tid -> (russian, source_tag)."""
    donors: dict[str, tuple[str, str]] = {}

    def add(tid: str, text: str, tag: str, *, overwrite: bool = False) -> None:
        if not tid or not looks_cyrillic(text):
            return
        if tid in donors and not overwrite:
            return
        donors[tid] = (text, tag)

    ws = MODS / ws_folder
    ws_map = collect_lua_map(ws)
    ws_map.update(load_csv_loc(ws))
    for tid, text in ws_map.items():
        add(tid, text, "Merc_*")

    og_map: dict[str, str] = {}
    if OTHERGUY.exists():
        # Prefer merc-scoped blobs from Otherguy items + companions
        og_slice = folder_slice(og_items, merc)
        og_map.update(parse_t(og_slice))
        for lst in extract_vr(og_items, merc).values():
            for tid, text in lst:
                og_map[tid] = text
        ud = OTHERGUY / "UnitData" / f"{merc}.lua"
        if ud.exists():
            og_map.update(parse_t(ud.read_text(encoding="utf-8", errors="replace")))
        for p in (OTHERGUY / "CharacterEffect").glob(f"{merc}*"):
            og_map.update(parse_t(p.read_text(encoding="utf-8", errors="replace")))
        for p in (OTHERGUY / "InventoryItem").glob(f"{merc}*"):
            og_map.update(parse_t(p.read_text(encoding="utf-8", errors="replace")))
        for p in (OTHERGUY / "Code").glob(f"{merc}*"):
            og_map.update(parse_t(p.read_text(encoding="utf-8", errors="replace")))
        og_map.update(load_csv_loc(OTHERGUY))

    for tid, text in og_map.items():
        add(tid, text, "JAZZ_Otherguy")

    # VR index pairing: donor RU line -> jazz tid (when IDs differ)
    ju_vr = extract_vr(ju_items, merc)
    ws_vr = extract_vr(
        (ws / "items.lua").read_text(encoding="utf-8", errors="replace")
        if (ws / "items.lua").exists()
        else "",
        merc,
    )
    og_vr = extract_vr(og_items, merc) if OTHERGUY.exists() else {}

    for label, donor_vr in (("Merc_*", ws_vr), ("JAZZ_Otherguy", og_vr)):
        for key in set(ju_vr) & set(donor_vr):
            for (jtid, _jtext), (_dtid, dtext) in zip(ju_vr[key], donor_vr[key]):
                # Merc_* wins over Otherguy for same jazz tid
                if label == "Merc_*":
                    add(jtid, dtext, f"Merc_*/VR:{key}", overwrite=True)
                else:
                    add(jtid, dtext, f"JAZZ_Otherguy/VR:{key}", overwrite=False)

    # Named UnitData / perk fields: Otherguy often uses different T-ids
    ju_fields = extract_named_fields(package_blob(JU, merc, ju_items))
    ws_fields = extract_named_fields(
        package_blob(ws, merc, (ws / "items.lua").read_text(encoding="utf-8", errors="replace") if (ws / "items.lua").exists() else "")
    )
    og_fields = extract_named_fields(
        package_blob(OTHERGUY, merc, og_items) if OTHERGUY.exists() else ""
    )
    for label, donor_fields in (("Merc_*", ws_fields), ("JAZZ_Otherguy", og_fields)):
        for field, (jtid, _jtext) in ju_fields.items():
            if field not in donor_fields:
                continue
            _dtid, dtext = donor_fields[field]
            if not looks_cyrillic(dtext):
                continue
            if label == "Merc_*":
                add(jtid, dtext, f"Merc_*/field:{field}", overwrite=True)
            else:
                add(jtid, dtext, f"JAZZ_Otherguy/field:{field}", overwrite=False)

    return donors


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    apply = bool(args.apply) and not args.dry_run

    ju_items = (JU / "items.lua").read_text(encoding="utf-8", errors="replace")
    og_items = (
        (OTHERGUY / "items.lua").read_text(encoding="utf-8", errors="replace")
        if (OTHERGUY / "items.lua").exists()
        else ""
    )

    ru_path, en_path = JAZZ / "Russian.csv", JAZZ / "English.csv"
    ru_sep, ru_fields, ru_rows, ru_by = load_rows(ru_path)
    en_sep, en_fields, en_rows, en_by = load_rows(en_path)

    patched_ru = 0
    already_ru = 0
    remain_en_copy = 0
    missing_ru = 0
    patched_en = 0
    by_merc: dict[str, dict[str, int]] = {}
    source_counts: dict[str, int] = {}
    samples: list[str] = []

    for merc, ws_folder in MERCS.items():
        stats = {"got_ru": 0, "already": 0, "remain": 0, "missing": 0}
        active = ju_active_for_merc(ju_items, merc)
        donors = build_ru_donors(merc, ws_folder, ju_items, og_items)

        for tid, src in sorted(active.items(), key=lambda x: int(x[0])):
            row = ru_by.get(tid)
            old = (row or {}).get("Translation") or ""
            donor = donors.get(tid)

            if row and looks_cyrillic(old):
                already_ru += 1
                stats["already"] += 1
                # Still fix Text to latin EN when possible
                if apply and looks_cyrillic(row.get("Text") or ""):
                    en_row = en_by.get(tid)
                    en_tr = (en_row or {}).get("Translation") or ""
                    if en_tr and not looks_cyrillic(en_tr):
                        row["Text"] = en_tr
                    elif src and not looks_cyrillic(src):
                        row["Text"] = src
                    elif tid in CAROL_EN:
                        row["Text"] = CAROL_EN[tid]
                continue

            if donor:
                ru_text, tag = donor
                source_counts[tag.split("/")[0]] = (
                    source_counts.get(tag.split("/")[0], 0) + 1
                )
                patched_ru += 1
                stats["got_ru"] += 1
                if len(samples) < 12:
                    samples.append(f"{merc} {tid} <- {tag}: {ru_text[:60]!r}")
                if apply:
                    en_row = en_by.get(tid)
                    en_tr = (en_row or {}).get("Translation") or ""
                    text_field = ""
                    if en_tr and not looks_cyrillic(en_tr):
                        text_field = en_tr
                    elif src and not looks_cyrillic(src):
                        text_field = src
                    elif tid in CAROL_EN:
                        text_field = CAROL_EN[tid]
                    else:
                        text_field = (row or {}).get("Text") or src
                    if row:
                        row["Translation"] = ru_text
                        if text_field and not looks_cyrillic(text_field):
                            row["Text"] = text_field
                        row["Context"] = row.get("Context") or "WorkshopMerc"
                    else:
                        new = {k: "" for k in ru_fields}
                        new["ID"] = tid
                        new["Text"] = text_field
                        new["Translation"] = ru_text
                        new["Context"] = "WorkshopMerc"
                        ru_rows.append(new)
                        ru_by[tid] = new
                continue

            # No donor: keep EN-copy / missing
            if not row:
                missing_ru += 1
                stats["missing"] += 1
            else:
                remain_en_copy += 1
                stats["remain"] += 1

        by_merc[merc] = stats

    # English.csv: CAROL_EN hand invents where EN is still Cyrillic
    for tid, en_text in CAROL_EN.items():
        row = en_by.get(tid)
        if not row:
            continue
        old = row.get("Translation") or ""
        if looks_cyrillic(old) or old != en_text:
            patched_en += 1
            if apply:
                row["Text"] = en_text
                row["Translation"] = en_text
                row["Context"] = row.get("Context") or "WorkshopMerc"
            # Keep Russian.csv Text in sync for these IDs
            ru_row = ru_by.get(tid)
            if apply and ru_row and looks_cyrillic(ru_row.get("Text") or ""):
                ru_row["Text"] = en_text

    print("=== Workshop merc RU from sources ===")
    for merc, st in by_merc.items():
        print(
            f"{merc}: got_real_RU={st['got_ru']} already_RU={st['already']} "
            f"remain_EN_copy={st['remain']} missing={st['missing']}"
        )
    print(
        f"\nTOTAL got_real_RU={patched_ru} already_RU={already_ru} "
        f"remain_EN_copy={remain_en_copy} missing={missing_ru}"
    )
    print(f"Source tags: {source_counts}")
    print(f"EN CAROL_EN patches: {patched_en}")
    for s in samples:
        print(" ", s)

    if apply:
        write_rows(ru_path, ru_sep, ru_fields, ru_rows)
        write_rows(en_path, en_sep, en_fields, en_rows)
        print(f"\nWrote {ru_path.name} + {en_path.name}")
    else:
        print("\nDRY-RUN (pass --apply to write)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
