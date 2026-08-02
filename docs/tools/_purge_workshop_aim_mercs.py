# -*- coding: utf-8 -*-
"""One-shot / idempotent purge of six Steam Workshop AIM mercs (historical cleanup).

Removes ModItemFolder blocks from jazz-units items.lua (paren-depth safe),
companions, workshop-only voices opus, metadata entries, WorkshopMerc CSV rows,
design/docs/tools artifacts, and the Samuel cumbersome exception.

Safe to re-run: missing pieces are skipped.
"""
from __future__ import annotations

import re
import shutil
import subprocess
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

MODS = Path(r"C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods")
JAZZ = MODS / "jazz"
JU = MODS / "jazz-units"

MERC_IDS = [
    "Merc_AnnieDubois",
    "Merc_CarolThompson",
    "Merc_HectorSanchez",
    "Merc_JerrySinclair",
    "Merc_MildredPatterson",
    "Merc_SamuelNkosi",
]
RELATED_IDS = MERC_IDS + [
    "Merc_AnnieDubois_Perk",
    "Merc_CarolThompson_Perk",
    "Merc_CarolThompson_Item",
    "Merc_CarolThompson10",
    "Merc_CarolThompson30",
    "Merc_CarolThompson60",
    "Merc_HectorSanchez_Perk",
    "Merc_HectorSanchez10",
    "Merc_HectorSanchez30",
    "Merc_HectorSanchez60",
    "Merc_JerrySinclair_Perk",
    "Merc_JerrySinclair_40mmTB",
    "Merc_JerrySinclair10",
    "Merc_JerrySinclair30",
    "Merc_JerrySinclair60",
    "Merc_MildredPatterson_Bookworm",
    "Merc_MildredPatterson_SkillMag",
    "Merc_MildredPatterson10",
    "Merc_MildredPatterson30",
    "Merc_MildredPatterson60",
    "Merc_SamuelNkosi_Perk",
    "Merc_SamuelNkosi10",
    "Merc_SamuelNkosi30",
    "Merc_SamuelNkosi60",
]
RELATED_RE = re.compile("|".join(re.escape(x) for x in RELATED_IDS))
PORTRAIT_STEMS = ["Annie", "Carol", "Hector", "Jerry", "Mildred", "Samuel"]


def find_folder_span(text: str, merc_id: str) -> tuple[int, int] | None:
    pat = re.compile(r"^(\t\tPlaceObj\('ModItemFolder',\s*\{\s*)$", re.M)
    start = None
    for m in pat.finditer(text):
        after = text[m.end() : m.end() + 200]
        if re.search(r"'name',\s*\"%s\"" % re.escape(merc_id), after):
            start = m.start()
            break
    if start is None:
        return None

    paren = text.find("(", start)
    depth_paren = 0
    in_str = False
    str_ch = ""
    esc = False
    in_line_comment = False
    in_block_comment = False
    j = paren
    n = len(text)
    while j < n:
        ch = text[j]
        nxt = text[j + 1] if j + 1 < n else ""
        if in_line_comment:
            if ch == "\n":
                in_line_comment = False
            j += 1
            continue
        if in_block_comment:
            if ch == "]" and nxt == "]":
                in_block_comment = False
                j += 2
                continue
            j += 1
            continue
        if in_str:
            if esc:
                esc = False
                j += 1
                continue
            if ch == "\\":
                esc = True
                j += 1
                continue
            if ch == str_ch:
                in_str = False
            j += 1
            continue
        if ch == "-" and nxt == "-":
            if j + 3 < n and text[j + 2 : j + 4] == "[[":
                in_block_comment = True
                j += 4
                continue
            in_line_comment = True
            j += 2
            continue
        if ch in ("'", '"'):
            in_str = True
            str_ch = ch
            j += 1
            continue
        if ch == "(":
            depth_paren += 1
        elif ch == ")":
            depth_paren -= 1
            if depth_paren == 0:
                end = j + 1
                if end < n and text[end] == ",":
                    end += 1
                if end < n and text[end] == "\n":
                    end += 1
                return start, end
        j += 1
    raise RuntimeError("unclosed PlaceObj for " + merc_id)


def find_matching_close(text: str, open_idx: int) -> int:
    assert text[open_idx] == "{"
    depth = 0
    i = open_idx
    n = len(text)
    in_str = False
    str_ch = ""
    esc = False
    in_line_comment = False
    in_block_comment = False
    while i < n:
        ch = text[i]
        nxt = text[i + 1] if i + 1 < n else ""
        if in_line_comment:
            if ch == "\n":
                in_line_comment = False
            i += 1
            continue
        if in_block_comment:
            if ch == "]" and nxt == "]":
                in_block_comment = False
                i += 2
                continue
            i += 1
            continue
        if in_str:
            if esc:
                esc = False
                i += 1
                continue
            if ch == "\\":
                esc = True
                i += 1
                continue
            if ch == str_ch:
                in_str = False
            i += 1
            continue
        if ch == "-" and nxt == "-":
            if i + 3 < n and text[i + 2 : i + 4] == "[[":
                in_block_comment = True
                i += 4
                continue
            in_line_comment = True
            i += 2
            continue
        if ch in ("'", '"'):
            in_str = True
            str_ch = ch
            i += 1
            continue
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                return i + 1
        i += 1
    raise RuntimeError("unbalanced brace")


def remove_moditem_folders(items_text: str) -> tuple[str, list[str]]:
    t_ids: list[str] = []
    spans = []
    for merc_id in MERC_IDS:
        span = find_folder_span(items_text, merc_id)
        if not span:
            print("skip missing folder", merc_id)
            continue
        a, b = span
        spans.append((a, b, merc_id))
        t_ids.extend(re.findall(r"\bT\((\d{6,})", items_text[a:b]))
        print("folder", merc_id, b - a, "chars")
    for a, b, merc_id in sorted(spans, key=lambda x: -x[0]):
        items_text = items_text[:a] + items_text[b:]
        print("removed", merc_id)
    return items_text, sorted(set(t_ids))


def scrub_metadata(path: Path) -> int:
    if not path.exists():
        return 0
    text = path.read_text(encoding="utf-8")
    orig = text
    lines = text.splitlines(keepends=True)
    out: list[str] = []
    removed = 0
    for line in lines:
        if ("WorkshopMercs/" in line or RELATED_RE.search(line)) and (
            re.search(r'^\s*"[^"]+",\s*$', line) or "WorkshopMercs/" in line
        ):
            removed += 1
            continue
        out.append(line)
    text = "".join(out)

    result = []
    i = 0
    while True:
        idx = text.find("PlaceObj('ModResourcePreset'", i)
        if idx < 0:
            result.append(text[i:])
            break
        result.append(text[i:idx])
        brace = text.find("{", idx)
        close = find_matching_close(text, brace)
        end = close
        if end < len(text) and text[end] == ")":
            end += 1
        if end < len(text) and text[end] == ",":
            end += 1
        if end < len(text) and text[end] == "\n":
            end += 1
        block = text[idx:end]
        if RELATED_RE.search(block):
            removed += 1
        else:
            result.append(block)
        i = end
    text = "".join(result)
    if text != orig:
        path.write_text(text, encoding="utf-8", newline="\n")
    print(path, "removed", removed)
    return removed


def scrub_csv(path: Path, t_ids: set[str]) -> int:
    text = path.read_text(encoding="utf-8")
    out = []
    n = 0
    for line in text.splitlines(keepends=True):
        drop = False
        if ",WorkshopMerc" in line or line.rstrip().endswith(",WorkshopMerc"):
            drop = True
        else:
            m = re.match(r"^(\d+),", line)
            if m and (m.group(1) in t_ids or RELATED_RE.search(line)):
                drop = True
        if drop:
            n += 1
            continue
        out.append(line)
    path.write_text("".join(out), encoding="utf-8", newline="\n")
    print(path.name, "csv removed", n)
    return n


def main() -> int:
    ju_items = JU / "items.lua"
    text = ju_items.read_text(encoding="utf-8")
    new_text, t_ids = remove_moditem_folders(text)
    if new_text != text:
        if new_text.count("{") - new_text.count("}") != 0:
            raise SystemExit("brace imbalance after folder removal — abort write")
        if new_text.count("(") - new_text.count(")") != 0:
            raise SystemExit("paren imbalance after folder removal — abort write")
        ju_items.write_text(new_text, encoding="utf-8", newline="\n")
    t_id_set = set(t_ids)

    scrub_metadata(JU / "metadata.lua")
    scrub_metadata(JAZZ / "metadata.lua")

    or_unit = JAZZ / "Code" / "System_OR_Unit.lua"
    or_text = or_unit.read_text(encoding="utf-8")
    old = (
        'if slot ~= "Inventory" and item:IsCumbersome() and not '
        '(item:IsKindOf("MachineGun") and HasPerk(self, "Merc_SamuelNkosi_Perk")) then'
    )
    new = 'if slot ~= "Inventory" and item:IsCumbersome() then'
    if old in or_text:
        or_unit.write_text(or_text.replace(old, new), encoding="utf-8", newline="\n")
        print("patched System_OR_Unit.lua")

    scrub_csv(JAZZ / "Russian.csv", t_id_set)
    scrub_csv(JAZZ / "English.csv", t_id_set)

    del_list: list[Path] = []
    for mid in MERC_IDS:
        del_list.append(JU / "UnitData" / f"{mid}.lua")
        del_list.append(JU / "Code" / "WorkshopMercs" / f"{mid}_Voices.lua")
    del_list += [
        JU / "InventoryItem" / "Merc_CarolThompson_Item.lua",
        JU / "InventoryItem" / "Merc_JerrySinclair_40mmTB.lua",
        JU / "Images" / "WorkshopMercs",
        JU / "Code" / "WorkshopMercs",
        JAZZ / "Images" / "WorkshopMercs",
        JAZZ / "Code" / "WorkshopMercs",
    ]
    for stem in PORTRAIT_STEMS:
        del_list.append(JU / "MercPortraits" / f"{stem}.png")
        del_list.append(JU / "MercPortraits" / f"{stem}_Big.png")
        del_list.append(JU / "MercPortraits" / "_wip" / "_raw" / f"{stem}_Big_cut.png")
        del_list.append(JU / "MercPortraits" / "_wip" / "_raw" / f"{stem}_UI_cut.png")
    for p in (JAZZ / "CharacterEffect").glob("Merc_*.lua"):
        del_list.append(p)
    del_list.append(JU / "MercPortraits" / "_wip" / "workshop_ui_overzoom_backup")
    del_list.append(JU / "MercPortraits" / "_wip" / "_raw" / "workshop")

    design = JAZZ / "docs" / "design" / "mercs-ja12"
    for slug in [
        "annie-dubois",
        "carol-thompson",
        "hector-sanchez",
        "jerry-sinclair",
        "mildred-patterson",
        "samuel-nkosi",
    ]:
        del_list.append(design / f"{slug}.md")
    del_list += [
        design / "_workshop_otherguy_sheet_targets.md",
        design / "_workshop_loot_diff.txt",
        design / "_face-source" / "workshop",
        JAZZ / "docs" / "tools" / "_donors" / "workshop_merc_en",
    ]
    tools = JAZZ / "docs" / "tools"
    for name in [
        "_import_workshop_aim_mercs.py",
        "_finish_workshop_aim_mercs.py",
        "_import_workshop_merc_vr_and_loc.py",
        "_seed_workshop_merc_loc.py",
        "_fix_workshop_merc_en_from_sources.py",
        "_fix_workshop_merc_ru_from_sources.py",
        "_apply_workshop_aim_sheet.py",
        "_apply_workshop_snype_ru.py",
        "_audit_workshop_snype_en_ru.py",
        "_audit_workshop_sj_merc_voices_loc.py",
        "_process_workshop_ui_portraits.py",
        "_process_workshop_merc_portraits.py",
        "_diff_workshop_loot.py",
        "_patch_workshop_merc_loc.py",
    ]:
        del_list.append(tools / name)

    for p in del_list:
        if not p.exists():
            continue
        if p.is_dir():
            shutil.rmtree(p)
        else:
            p.unlink()
        print("deleted", p)

    remaining = (JU / "items.lua").read_text(encoding="utf-8")
    voices = JU / "voices"
    opus_removed = 0
    if voices.exists() and t_id_set:
        for tid in sorted(t_id_set):
            if re.search(r"\b" + tid + r"\b", remaining):
                continue
            for p in voices.glob(f"{tid}.opus"):
                p.unlink()
                opus_removed += 1
    print("orphan opus removed", opus_removed)

    readme = design / "README.md"
    if readme.exists():
        rt = readme.read_text(encoding="utf-8")
        rt2 = re.sub(
            r"\n## Workshop AIM \(imported, stubs\).*?\n## High / Medium / Low",
            "\n## High / Medium / Low",
            rt,
            count=1,
            flags=re.S,
        )
        if rt2 != rt:
            readme.write_text(rt2, encoding="utf-8", newline="\n")

    print("brace diff ju items", remaining.count("{") - remaining.count("}"))
    print("done")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
