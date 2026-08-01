# -*- coding: utf-8 -*-
"""Import missing ModItemVoiceResponse from standalone workshop mods into jazz-units,
fix CombatAction Icon leftovers, and seed RU/EN localization for merc T-ids.

Usage (jazz/):
  python docs/tools/_import_workshop_merc_vr_and_loc.py --dry-run
  python docs/tools/_import_workshop_merc_vr_and_loc.py --apply
"""
from __future__ import annotations

import argparse
import csv
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

JAZZ = Path(r"C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz")
JU = Path(r"C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz-units")
MODS = JAZZ.parent

sys.path.insert(0, str(JAZZ / "docs" / "tools"))
from _loc_csv_io import load_rows, write_rows  # noqa: E402

# merc_id -> workshop folder name / mod id
WORKSHOP = {
    "Merc_AnnieDubois": ("Merc_ Annie Dubois", "sH5nmG", "Annie"),
    "Merc_CarolThompson": ("Merc_ Carol Thompson", "Q6ivSk4", "Carol"),
    "Merc_HectorSanchez": ("Merc_ Hector Sanchez", "jkp5GEJ", "Hector"),
    "Merc_JerrySinclair": ("Merc_ Jerry Sinclair", "E5rtcCe", "Jerry"),
    "Merc_MildredPatterson": ("Merc_ Mildred Patterson", "QkMtGCa", "Mildred"),
    "Merc_SamuelNkosi": ("Merc_ Samuel Nkosi", "HgzATh3", "Samuel"),
}

MISSING_VR = [
    "Merc_AnnieDubois",
    "Merc_CarolThompson",
    "Merc_JerrySinclair",
    "Merc_SamuelNkosi",
]

# CombatAction lives in jazz (e6L4ECj); passive perk icons ship under Images/WorkshopMercs.
ICON_FIX = {
    "Merc_AnnieDubois": "Mod/e6L4ECj/Images/WorkshopMercs/Annie_Perk_Passive.png",
    "Merc_CarolThompson": "Mod/e6L4ECj/Images/WorkshopMercs/Carol_Perk_Passive.png",
    "Merc_HectorSanchez": "Mod/e6L4ECj/Images/WorkshopMercs/Hector_Perk_Passive.png",
    "Merc_JerrySinclair": "Mod/e6L4ECj/Images/WorkshopMercs/Jerry_Perk_Passive.png",
    "Merc_MildredPatterson": "Mod/e6L4ECj/Images/WorkshopMercs/Mildred_Perk_Passive.png",
    "Merc_SamuelNkosi": "Mod/e6L4ECj/Images/WorkshopMercs/Samuel_Perk_Passive.png",
}


def extract_vr_block(items_text: str, merc_id: str) -> str | None:
    for m in re.finditer(r"PlaceObj\('ModItemVoiceResponse',", items_text):
        window = items_text[m.start() : m.start() + 200000]
        mid = re.search(r'id\s*=\s*"([^"]+)"', window)
        if not mid or mid.group(1) != merc_id:
            continue
        # include through id line and closing }),
        end_rel = mid.end()
        rest = window[end_rel:]
        close = re.search(r"\s*\}\)\s*,?", rest)
        if not close:
            return None
        block = window[: end_rel + close.end()]
        # normalize trailing comma
        block = block.rstrip()
        if not block.endswith(","):
            if block.endswith("})"):
                block = block + ","
        return block
    return None


def has_vr(items_text: str, merc_id: str) -> bool:
    for m in re.finditer(r"PlaceObj\('ModItemVoiceResponse',", items_text):
        window = items_text[m.start() : m.start() + 200000]
        mid = re.search(r'id\s*=\s*"([^"]+)"', window)
        if mid and mid.group(1) == merc_id:
            return True
    return False


def find_insert_point_after_unitdata(items_text: str, merc_id: str) -> int | None:
    """Insert VR after ModItemUnitDataCompositeDef for merc (before folder close)."""
    # Find UnitData def with this Id
    pat = re.compile(
        rf"PlaceObj\('ModItemUnitDataCompositeDef',\s*\{{[\s\S]*?'Id',\s*\"{re.escape(merc_id)}\"",
    )
    m = pat.search(items_text)
    if not m:
        return None
    # Find end of this UnitData PlaceObj — match braces from start
    start = m.start()
    i = items_text.find("{", start)
    depth = 0
    for j in range(i, len(items_text)):
        c = items_text[j]
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                # expect }),
                end = j + 1
                if items_text[end : end + 2] == "),":
                    end += 2
                elif items_text[end : end + 1] == ")":
                    end += 1
                    if items_text[end : end + 1] == ",":
                        end += 1
                return end
    return None


def collect_t_entries_from_blobs(blobs: list[str]) -> dict[str, str]:
    """tid -> source text from T(id, --[[...]] \"text\") or T(id, --[[...]] 'text')."""
    out: dict[str, str] = {}
    # Double-quoted
    pat_dq = re.compile(
        r'T\((\d+)\s*,\s*--\[\[[^\]]*\]\]\s*"((?:\\.|[^"\\])*)"',
        re.S,
    )
    # Single-quoted (Carol Bio style)
    pat_sq = re.compile(
        r"T\((\d+)\s*,\s*--\[\[[^\]]*\]\]\s*'((?:\\.|[^'\\])*)'",
        re.S,
    )
    for blob in blobs:
        if not blob:
            continue
        for m in pat_dq.finditer(blob):
            tid, text = m.group(1), m.group(2)
            text = text.replace('\\"', '"').replace("\\n", "\n").replace("\\\\", "\\")
            out[tid] = text
        for m in pat_sq.finditer(blob):
            tid, text = m.group(1), m.group(2)
            text = text.replace("\\'", "'").replace("\\n", "\n").replace("\\\\", "\\")
            out[tid] = text
    return out


def load_csv_map(path: Path) -> dict[str, dict[str, str]]:
    if not path.exists():
        return {}
    sep, fieldnames, rows_list, by_id = load_rows(path)
    return {"_sep": sep, "_fields": fieldnames, **by_id}


def write_csv(path: Path, sep: str | None, fieldnames: list[str], rows: dict[str, dict[str, str]], order: list[str]) -> None:
    # Keep existing order, append new — parse with multiline-safe reader.
    if path.exists():
        sep_existing, fieldnames_existing, old_list, _ = load_rows(path)
        sep = sep if sep is not None else sep_existing
        fieldnames = list(fieldnames_existing or fieldnames)
    else:
        fieldnames = list(fieldnames)
        old_list = []
    old_rows = []
    seen = set()
    for row in old_list:
        i = (row.get("ID") or "").strip()
        if not i:
            continue
        if i in rows:
            new = rows[i]
            for k in fieldnames:
                if k in new and new[k] not in (None, ""):
                    row[k] = new[k]
            old_rows.append(row)
            seen.add(i)
        else:
            old_rows.append(row)
            seen.add(i)
    for i in order:
        if i in seen:
            continue
        r = rows[i]
        old_rows.append({k: r.get(k, "") for k in fieldnames})
        seen.add(i)

    write_rows(path, sep, fieldnames, old_rows)


def load_workshop_loc(folder: Path) -> dict[str, tuple[str, str]]:
    """tid -> (en_text, ru_text) from workshop csv if present."""
    out: dict[str, tuple[str, str]] = {}
    for name in ("English.csv", "Russian.csv", "Localization.csv"):
        p = folder / name
        if not p.exists():
            continue
        _, _, _, by_id = load_rows(p)
        for tid, row in by_id.items():
            src = row.get("Text") or ""
            tr = row.get("Translation") or ""
            en, ru = out.get(tid, ("", ""))
            # Heuristic: if file is English, Translation may be EN or empty; Text is source
            if "English" in name:
                en = tr or src or en
                if not ru:
                    ru = ""
            elif "Russian" in name:
                ru = tr or ru
                en = src or en
            else:
                en = src or en
                ru = tr or ru
            out[tid] = (en, ru)
    return out


def looks_cyrillic(s: str) -> bool:
    return bool(re.search(r"[\u0400-\u04FF]", s or ""))


def collect_cyrillic_t_map(root: Path) -> dict[str, str]:
    """tid -> Cyrillic T() text from all lua under root (plus Russian.csv)."""
    out: dict[str, str] = {}
    if not root.exists():
        return out
    for p in root.rglob("*.lua"):
        blob = p.read_text(encoding="utf-8", errors="replace")
        for tid, text in collect_t_entries_from_blobs([blob]).items():
            if looks_cyrillic(text):
                out[tid] = text
    for tid, (_en, ru) in load_workshop_loc(root).items():
        if looks_cyrillic(ru):
            out[tid] = ru
    return out


def fix_combat_action_icons(apply: bool) -> list[str]:
    logs = []
    for merc, icon in ICON_FIX.items():
        path = JAZZ / "Code" / "WorkshopMercs" / f"{merc}_CombatAction.lua"
        if not path.exists():
            logs.append(f"SKIP missing {path.name}")
            continue
        text = path.read_text(encoding="utf-8")
        new, n = re.subn(
            r'Icon\s*=\s*"Mod/[^"]+"',
            f'Icon = "{icon}"',
            text,
            count=1,
        )
        # Also fix if already path wrong
        if n == 0 and icon not in text:
            logs.append(f"WARN no Icon= in {path.name}")
            continue
        if new == text:
            logs.append(f"OK already {merc}")
            continue
        # verify target icon exists
        rel = icon.replace("Mod/Dv3mFVN/", "")
        disk = JU / rel if (JU / rel).exists() else JAZZ / rel
        # Images may live in jazz
        if not disk.exists():
            disk = JAZZ / rel
        if not disk.exists():
            # try jazz Images path
            alt = JAZZ / "Images" / "WorkshopMercs" / Path(icon).name
            if alt.exists():
                icon2 = f"Mod/Dv3mFVN/Images/WorkshopMercs/{alt.name}"
                # jazz package id is not Dv3mFVN - wait jazz-units is Dv3mFVN?
                new = re.sub(r'Icon\s*=\s*"Mod/[^"]+"', f'Icon = "{icon}"', text, count=1)
            logs.append(f"WARN icon file missing for {merc}: {icon} (still rewiring path)")
        logs.append(f"FIX Icon {merc} -> {icon}")
        if apply:
            path.write_text(new, encoding="utf-8")
    return logs


def ensure_carol_meta_code(meta: str) -> tuple[str, bool]:
    if "UnitData/Merc_CarolThompson.lua" in meta:
        return meta, False
    # insert after Carol Voices line
    needle = '"Code/WorkshopMercs/Merc_CarolThompson_Voices.lua",'
    if needle not in meta:
        return meta, False
    insert = needle + '\n\t\t"UnitData/Merc_CarolThompson.lua",'
    return meta.replace(needle, insert, 1), True


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument(
        "--skip-sj",
        action="store_true",
        help="Skip Benny/Simon/Grom chat opus fill (workshop loc/VR only).",
    )
    args = ap.parse_args()
    apply = args.apply and not args.dry_run

    ju_items_path = JU / "items.lua"
    ju_items = ju_items_path.read_text(encoding="utf-8")

    # 1) Import missing VR
    for merc in MISSING_VR:
        if has_vr(ju_items, merc):
            print(f"VR already present: {merc}")
            continue
        folder_name, _wid, _stem = WORKSHOP[merc]
        src = MODS / folder_name / "items.lua"
        if not src.exists():
            print(f"FAIL no workshop items for {merc}: {src}")
            continue
        src_text = src.read_text(encoding="utf-8", errors="replace")
        block = extract_vr_block(src_text, merc)
        if not block:
            print(f"FAIL no VR block in workshop for {merc}")
            continue
        # Rewrite any leftover Mod/wid paths inside VR? usually none
        for _m, (_fn, wid, _) in WORKSHOP.items():
            block = block.replace(f"Mod/{wid}/", "Mod/Dv3mFVN/")
        insert_at = find_insert_point_after_unitdata(ju_items, merc)
        if insert_at is None:
            print(f"FAIL no UnitData insert point for {merc}")
            continue
        # Indent block with one tab to match folder contents style used by Hector
        # Workshop blocks often start at col0 PlaceObj — keep as-is after newline
        injection = "\n" + block + "\n"
        print(f"INSERT VR {merc} at {insert_at} bytes={len(block)}")
        if apply:
            ju_items = ju_items[:insert_at] + injection + ju_items[insert_at:]

    if apply:
        ju_items_path.write_text(ju_items, encoding="utf-8")
        print("Wrote jazz-units/items.lua")

    # 2) Carol metadata code
    meta_path = JU / "metadata.lua"
    meta = meta_path.read_text(encoding="utf-8")
    meta2, changed = ensure_carol_meta_code(meta)
    print(f"Carol UnitData meta.code: {'ADD' if changed else 'OK'}")
    if apply and changed:
        meta_path.write_text(meta2, encoding="utf-8")

    # 3) CombatAction icons
    for line in fix_combat_action_icons(apply):
        print(line)

    # 4) Localization: collect all T ids for workshop mercs from ju items + companions + jazz CE/CA
    # Reload items if applied
    if apply:
        ju_items = ju_items_path.read_text(encoding="utf-8")

    tid_text: dict[str, str] = {}
    tid_ru_hint: dict[str, str] = {}

    for merc, (folder_name, wid, stem) in WORKSHOP.items():
        blobs = []
        # jazz-units folder slice: from ModItemFolder name to next folder
        m = re.search(
            rf"PlaceObj\('ModItemFolder',\s*\{{\s*'name',\s*\"{re.escape(merc)}\"",
            ju_items,
        )
        if m:
            start = m.start()
            nxt = re.search(r"\n\t\tPlaceObj\('ModItemFolder',", ju_items[start + 10 :])
            end = start + 10 + nxt.start() if nxt else start + 100000
            blobs.append(ju_items[start:end])
        ud = JU / "UnitData" / f"{merc}.lua"
        if ud.exists():
            blobs.append(ud.read_text(encoding="utf-8", errors="replace"))
        for p in (JAZZ / "CharacterEffect").glob(f"{merc}*"):
            blobs.append(p.read_text(encoding="utf-8", errors="replace"))
        for p in (JAZZ / "Code" / "WorkshopMercs").glob(f"{merc}*"):
            blobs.append(p.read_text(encoding="utf-8", errors="replace"))
        # workshop source for EN/RU
        ws = MODS / folder_name
        if (ws / "items.lua").exists():
            blobs.append((ws / "items.lua").read_text(encoding="utf-8", errors="replace"))
        entries = collect_t_entries_from_blobs(blobs)
        tid_text.update(entries)
        wloc = load_workshop_loc(ws)
        for tid, (en, ru) in wloc.items():
            if tid in entries or tid in tid_text:
                if en and not looks_cyrillic(en):
                    tid_text[tid] = en
                if looks_cyrillic(ru):
                    tid_ru_hint[tid] = ru
        # Prefer Cyrillic T() embedded in Merc_* lua (Carol ships RU in body)
        for tid, text in collect_cyrillic_t_map(ws).items():
            if tid in entries or tid in tid_text or tid in tid_ru_hint:
                tid_ru_hint[tid] = text

    # Also pull workshop Russian if Text is English and Translation Russian
    for merc, (folder_name, wid, stem) in WORKSHOP.items():
        ws = MODS / folder_name
        for csv_name, lang in (("Russian.csv", "ru"), ("English.csv", "en")):
            p = ws / csv_name
            if not p.exists():
                continue
            _, _, _, by_id = load_rows(p)
            for tid, row in by_id.items():
                if tid not in tid_text and tid not in collect_t_entries_from_blobs(
                    [(ws / "items.lua").read_text(encoding="utf-8", errors="replace")]
                    if (ws / "items.lua").exists()
                    else []
                ):
                    # only merc-related ids we already know
                    continue
                src = row.get("Text") or ""
                tr = row.get("Translation") or ""
                if lang == "ru" and looks_cyrillic(tr):
                    tid_ru_hint[tid] = tr
                if lang == "en" and (tr or src) and not looks_cyrillic(tr or src):
                    tid_text[tid] = tr or src

    # Filter to tids that appear in ju workshop merc content only
    ju_merc_tids: set[str] = set()
    for merc in WORKSHOP:
        m = re.search(
            rf"PlaceObj\('ModItemFolder',\s*\{{\s*'name',\s*\"{re.escape(merc)}\"",
            ju_items,
        )
        if m:
            start = m.start()
            nxt = re.search(r"\n\t\tPlaceObj\('ModItemFolder',", ju_items[start + 10 :])
            end = start + 10 + nxt.start() if nxt else start + 120000
            ju_merc_tids.update(re.findall(r"T\((\d+)\s*,", ju_items[start:end]))
        ud = JU / "UnitData" / f"{merc}.lua"
        if ud.exists():
            ju_merc_tids.update(re.findall(r"T\((\d+)\s*,", ud.read_text(encoding="utf-8", errors="replace")))
        for p in (JAZZ / "CharacterEffect").glob(f"{merc}*"):
            ju_merc_tids.update(re.findall(r"T\((\d+)\s*,", p.read_text(encoding="utf-8", errors="replace")))

    # Fallback RU from local aggregate JAZZ_Otherguy when Merc_* has none
    otherguy = MODS / "JAZZ_Otherguy"
    if otherguy.exists():
        og_ru = collect_cyrillic_t_map(otherguy)
        n_og = 0
        for tid, text in og_ru.items():
            if tid in ju_merc_tids and tid not in tid_ru_hint:
                tid_ru_hint[tid] = text
                n_og += 1
        print(f"Otherguy RU donors applied to merc tids: {n_og}/{len(og_ru)}")

    # Load existing jazz csv
    ru_path = JAZZ / "Russian.csv"
    en_path = JAZZ / "English.csv"

    def existing_ids(path: Path) -> set[str]:
        if not path.exists():
            return set()
        _, _, _, by_id = load_rows(path)
        return set(by_id)

    ru_have = existing_ids(ru_path)
    en_have = existing_ids(en_path)

    new_ru: dict[str, dict[str, str]] = {}
    new_en: dict[str, dict[str, str]] = {}
    patch_ru: dict[str, dict[str, str]] = {}
    order = []
    invent_notes = []

    for tid in sorted(ju_merc_tids, key=int):
        src = tid_text.get(tid, "")
        if not src:
            # try from ju items directly one more time for this tid
            m = re.search(rf'T\({tid}\s*,\s*--\[\[[^\]]*\]\]\s*"((?:\\.|[^"\\])*)"', ju_items, re.S)
            if not m:
                m = re.search(rf"T\({tid}\s*,\s*--\[\[[^\]]*\]\]\s*'((?:\\.|[^'\\])*)'", ju_items, re.S)
            if m:
                src = m.group(1).replace('\\"', '"').replace("\\'", "'")
        if not src:
            continue
        ru = tid_ru_hint.get(tid, "")
        en = src
        if looks_cyrillic(src) and not ru:
            ru = src
            # EN invent from workshop English if any; else leave invent flag
            en = tid_text.get(tid, src) if not looks_cyrillic(tid_text.get(tid, "")) else ""
            if not en or looks_cyrillic(en):
                # try workshop English.csv Text
                en = ""
        if looks_cyrillic(src) and looks_cyrillic(en):
            en = ""
        if not looks_cyrillic(src) and not ru:
            ru = tid_ru_hint.get(tid, "")

        if tid not in en_have:
            if not en:
                # invent: keep Russian as placeholder only if we must — skip invent EN from RU for now use src if latin
                if not looks_cyrillic(src):
                    en = src
                else:
                    invent_notes.append(f"EN invent needed {tid}")
                    en = src  # temporary: ship RU text in EN only as last resort marked
            new_en[tid] = {
                "ID": tid,
                "Text": src if not looks_cyrillic(src) else en,
                "Translation": en,
                "VoiceActor": "",
                "Context": "WorkshopMerc",
            }
            order.append(tid)
        if tid not in ru_have:
            if not ru:
                if looks_cyrillic(src):
                    ru = src
                else:
                    # invent RU = copy EN (technical) — note
                    invent_notes.append(f"RU invent=EN copy {tid}")
                    ru = en or src
            new_ru[tid] = {
                "ID": tid,
                "Text": src if not looks_cyrillic(src) else (en or src),
                "Translation": ru,
                "VoiceActor": "",
                "Context": "WorkshopMerc",
            }
            if tid not in order:
                order.append(tid)
        elif looks_cyrillic(ru):
            # Prefer source RU over existing EN-copy invent
            patch_ru[tid] = {
                "ID": tid,
                "Text": src if not looks_cyrillic(src) else (en or src),
                "Translation": ru,
                "VoiceActor": "",
                "Context": "WorkshopMerc",
            }

    print(
        f"Loc to add: RU={len(new_ru)} EN={len(new_en)} "
        f"RU patch-from-source={len(patch_ru)} invent_notes={len(invent_notes)}"
    )
    print(
        "For full EN-copy replacement (Merc_* + JAZZ_Otherguy VR pairing) use "
        "docs/tools/_fix_workshop_merc_ru_from_sources.py"
    )
    for n in invent_notes[:20]:
        print(" ", n)
    if invent_notes[20:]:
        print(f"  ... +{len(invent_notes)-20} more")

    if apply and (new_ru or new_en or patch_ru):
        # Append using simple approach: read all, merge, write
        def merge_csv(
            path: Path,
            additions: dict[str, dict[str, str]],
            patches: dict[str, dict[str, str]] | None = None,
        ) -> None:
            sep, fields, rows, by_id = load_rows(path)
            have = set(by_id)
            if patches:
                for r in rows:
                    tid = (r.get("ID") or "").strip()
                    if tid not in patches:
                        continue
                    old = r.get("Translation") or ""
                    new_tr = patches[tid].get("Translation") or ""
                    if looks_cyrillic(new_tr) and not looks_cyrillic(old):
                        r["Translation"] = new_tr
                        nt = patches[tid].get("Text") or ""
                        if nt and not looks_cyrillic(nt):
                            r["Text"] = nt
            for tid, r in additions.items():
                if tid in have:
                    continue
                rows.append({k: r.get(k, "") for k in fields})
            write_rows(path, sep, fields, rows)

        if new_ru or patch_ru:
            merge_csv(ru_path, new_ru, patch_ru)
            print(f"Updated {ru_path}")
        if new_en:
            merge_csv(en_path, new_en)
            print(f"Updated {en_path}")

    # 5) Generate g_VoiceVariations for Benny/Simon/Grom chat+VR if missing?
    # Jazz mercs don't use VV — game resolves Voices/<tid>.opus by T-id.
    # But chat hire lines missing opus — ship by duplicating Selection opus.
    if args.skip_sj:
        print("\nSJ chat voice fill: skipped (--skip-sj)")
        print("\nDone.", "APPLY" if apply else "DRY-RUN")
        return 0

    print("\nSJ chat voice fill (Benny/Simon/Grom):")
    vdir = JU / "voices"
    for merc, chat_missing_note in (
        ("Jazz_Benny", True),
        ("Jazz_Simon", True),
        ("Jazz_Grom", True),
    ):
        # find VR Selection tid as donor
        donor = None
        for m in re.finditer(r"PlaceObj\('ModItemVoiceResponse',", ju_items):
            win = ju_items[m.start() : m.start() + 50000]
            mid = re.search(r'id\s*=\s*"([^"]+)"', win)
            if not mid or mid.group(1) != merc:
                continue
            body = win[: mid.start()]
            sm = re.search(r"Selection\s*=\s*TConcat\(\{\s*T\((\d+),", body)
            if sm:
                donor = sm.group(1)
            break
        chat_tids = re.findall(
            rf"T\((\d+),\s*--\[\[[^\]]*voice:{re.escape(merc)}\]\]",
            ju_items,
        )
        # also from UnitData
        ud = JU / "UnitData" / f"{merc}.lua"
        if ud.exists():
            chat_tids += re.findall(
                rf"T\((\d+),\s*--\[\[[^\]]*voice:{re.escape(merc)}\]\]",
                ud.read_text(encoding="utf-8", errors="replace"),
            )
        chat_tids = sorted(set(chat_tids))
        if not donor:
            print(f"  {merc}: no Selection donor")
            continue
        donor_path = vdir / f"{donor}.opus"
        if not donor_path.exists():
            print(f"  {merc}: donor missing {donor}")
            continue
        filled = 0
        for tid in chat_tids:
            dest = vdir / f"{tid}.opus"
            if dest.exists() and dest.stat().st_size > 50:
                continue
            print(f"  {merc}: copy {donor} -> {tid}")
            if apply:
                dest.write_bytes(donor_path.read_bytes())
            filled += 1
        print(f"  {merc}: filled {filled} chat lines from Selection {donor}")

    print("\nDone.", "APPLY" if apply else "DRY-RUN")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
