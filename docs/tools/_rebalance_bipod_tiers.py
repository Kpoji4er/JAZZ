# -*- coding: utf-8 -*-
"""Bipod consolidate: one Bipod-slot ID + Under variants; unify prone bonuses.

Canon: docs/design/bipod-tiers.md
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _apply_attach_001 import placeobj_blocks, prop, atomic_write, list_region

ROOT = Path(__file__).resolve().parents[2]
ITEMS = ROOT / "items.lua"
META = ROOT / "metadata.lua"

KEEP = {"JAZZ_Bipod", "JAZZ_Bipod_Under", "JAZZ_Bipod_Galil"}
CUT = {
    "JAZZ_Bipod_MG42",
    "JAZZ_KSP_BIPOD",
    "JAZZ_FoldBipod",
    "JAZZ_UnfoldBipod",
}
MERGE_FROM = {
    "JAZZ_Bipod_MG42": {"MG42", "MG58"},
    "JAZZ_KSP_BIPOD": {"FNMAG"},
    "JAZZ_UnfoldBipod": {"U100", "RPD"},
}

BONUS, SHOTS, COST, DIFF = 10, 1, 50, 10

EFFECTS = (
    "ModificationEffects = {\n"
    '\t\t\t\t\t\t"AccuracyBonusProne",\n'
    '\t\t\t\t\t\t"ShotsBeforeRecoilProne",\n'
    "\t\t\t\t\t},"
)
PARAMS = (
    "Parameters = {\n"
    "\t\t\t\t\t\tPlaceObj('PresetParamNumber', {\n"
    '\t\t\t\t\t\t\t\'Name\', "bonus_cth_bipod",\n'
    f"\t\t\t\t\t\t\t'Value', {BONUS},\n"
    '\t\t\t\t\t\t\t\'Tag\', "<bonus_cth_bipod>",\n'
    "\t\t\t\t\t\t}),\n"
    "\t\t\t\t\t\tPlaceObj('PresetParamNumber', {\n"
    '\t\t\t\t\t\t\t\'Name\', "ShotsBeforeRecoilProne",\n'
    f"\t\t\t\t\t\t\t'Value', {SHOTS},\n"
    '\t\t\t\t\t\t\t\'Tag\', "<ShotsBeforeRecoilProne>",\n'
    "\t\t\t\t\t\t}),\n"
    "\t\t\t\t\t},"
)


def _field_span(text: str, name: str) -> tuple[int, int] | None:
    region = list_region(text, name)
    if region is None:
        return None
    m = re.search(rf"\b{re.escape(name)}\s*=\s*\{{", text)
    if not m:
        return None
    end = region[1]
    if end < len(text) and text[end] == ",":
        end += 1
    while end < len(text) and text[end] in " \t":
        end += 1
    if end < len(text) and text[end] == "\n":
        end += 1
    return m.start(), end


def _replace_field(text: str, name: str, replacement: str) -> str:
    span = _field_span(text, name)
    body = replacement if replacement.endswith("\n") else replacement + "\n"
    if span is None:
        if name == "Parameters":
            fx = _field_span(text, "ModificationEffects")
            if fx:
                return text[: fx[1]] + body + text[fx[1] :]
        return re.sub(
            r"(DisplayName = T\([^\n]+\),)",
            rf"\1\n\t\t\t\t\t{replacement}",
            text,
            count=1,
        )
    start, end = span
    return text[:start] + body + text[end:]


def visual_blocks(comp_text: str) -> list[str]:
    region = list_region(comp_text, "Visuals")
    if not region:
        return []
    body = comp_text[region[0] : region[1]]
    blocks = []
    for m in re.finditer(r"PlaceObj\('WeaponComponentVisual',", body):
        po = m.start()
        i = body.find("(", po)
        depth = 0
        j = i
        while j < len(body):
            if body[j] == "(":
                depth += 1
            elif body[j] == ")":
                depth -= 1
                if depth == 0:
                    blocks.append(body[po : j + 1])
                    break
            j += 1
    return blocks


def apply_to(vis: str) -> str | None:
    m = re.search(r'ApplyTo\s*=\s*"([^"]+)"', vis)
    return m.group(1) if m else None


def patch_keep(comp: str, cid: str) -> str:
    text = _replace_field(comp, "ModificationEffects", EFFECTS)
    text = _replace_field(text, "Parameters", PARAMS)
    if re.search(r"Cost = \d+,", text):
        text = re.sub(r"Cost = \d+,", f"Cost = {COST},", text, count=1)
    else:
        text = re.sub(
            r"(DisplayName = T\([^\n]+\),)",
            rf"\1\n\t\t\t\t\tCost = {COST},",
            text,
            count=1,
        )
    if re.search(r"ModificationDifficulty = -?\d+,", text):
        text = re.sub(
            r"ModificationDifficulty = -?\d+,",
            f"ModificationDifficulty = {DIFF},",
            text,
            count=1,
        )
    comment = {
        "JAZZ_Bipod": "Bipod — prone CTH+10 +1 shot before recoil",
        "JAZZ_Bipod_Under": "Bipod Under — prone CTH+10 +1 shot",
        "JAZZ_Bipod_Galil": "Bipod Galil Under — prone CTH+10 +1 shot",
    }[cid]
    if re.search(r'comment = "[^"]*"', text):
        text = re.sub(r'comment = "[^"]*"', f'comment = "{comment}"', text, count=1)
    else:
        text = re.sub(
            r"(\n\t\t\t\t\t(?:group|Slot) = )",
            f'\n\t\t\t\t\tcomment = "{comment}",\\1',
            text,
            count=1,
        )
    return text


def merge_visuals_into_main(text: str, blocks_by_id: dict[str, str]) -> str:
    main = next(
        b
        for b in placeobj_blocks(text, "ModItemWeaponComponent")
        if prop(b.text, "id") == "JAZZ_Bipod"
    )
    existing = {apply_to(v) for v in visual_blocks(main.text)}
    existing.discard(None)
    to_add: list[str] = []
    for donor_id, want_apply in MERGE_FROM.items():
        donor = blocks_by_id.get(donor_id)
        if not donor:
            print("WARN missing donor", donor_id)
            continue
        for vis in visual_blocks(donor):
            a = apply_to(vis)
            if a in want_apply and a not in existing:
                to_add.append(vis)
                existing.add(a)
                print("merge visual", a, "from", donor_id)
    if not to_add:
        return text
    region = list_region(main.text, "Visuals")
    assert region
    abs_close = main.start + region[1] - 1
    chunk = "".join(f"\n\t\t\t\t\t\t{v}," for v in to_add)
    return text[:abs_close] + chunk + "\n\t\t\t\t\t" + text[abs_close:]


def remap_refs(text: str) -> str:
    for cid in CUT:
        text = text.replace(f'"{cid}"', '"JAZZ_Bipod"')
        text = text.replace(
            f"'DefaultComponent', \"{cid}\"", "'DefaultComponent', \"JAZZ_Bipod\""
        )

    def dedupe_avail(m: re.Match) -> str:
        body = m.group(0)
        if "JAZZ_Bipod" not in body:
            return body
        lines = body.split("\n")
        out, seen = [], False
        for line in lines:
            if '"JAZZ_Bipod"' in line:
                if seen:
                    continue
                seen = True
            out.append(line)
        return "\n".join(out)

    return re.sub(
        r"'AvailableComponents',\s*\{[^}]*\}",
        dedupe_avail,
        text,
        flags=re.S,
    )


def remove_moditems(text: str, ids: set[str]) -> str:
    for b in reversed(placeobj_blocks(text, "ModItemWeaponComponent")):
        cid = prop(b.text, "id")
        if cid not in ids:
            continue
        end = b.end
        if end < len(text) and text[end] == ",":
            end += 1
        if end < len(text) and text[end] == "\n":
            end += 1
        text = text[: b.start] + text[end:]
        print("removed ModItem", cid)
    return text


def remove_metadata(ids: set[str]) -> None:
    mt = META.read_text(encoding="utf-8")
    for cid in ids:
        pat = re.compile(
            r"\t\tPlaceObj\('ModResourcePreset', \{\n"
            r"\t\t\t'Class', \"WeaponComponent\",\n"
            rf"\t\t\t'Id', \"{re.escape(cid)}\",\n"
            r"\t\t\t'ClassDisplayName', \"Weapon Component\",\n"
            r"\t\t\}\),\n"
        )
        mt, n = pat.subn("", mt)
        print("metadata", cid, n)
    atomic_write(META, mt)


def patch_companions() -> None:
    for rel in (
        "InventoryItem/U100.lua",
        "InventoryItem/RPD.lua",
        "InventoryItem/MG58.lua",
        "InventoryItem/MG42.lua",
        "InventoryItem/FNMAG.lua",
    ):
        p = ROOT / rel
        t = p.read_text(encoding="utf-8")
        t2 = remap_refs(t)
        if t2 != t:
            atomic_write(p, t2)
            print("companion", rel)


def main() -> int:
    text = ITEMS.read_text(encoding="utf-8")
    by_id = {
        prop(b.text, "id"): b.text
        for b in placeobj_blocks(text, "ModItemWeaponComponent")
        if prop(b.text, "id") in (KEEP | CUT)
    }
    text = merge_visuals_into_main(text, by_id)
    for b in reversed(placeobj_blocks(text, "ModItemWeaponComponent")):
        cid = prop(b.text, "id")
        if cid not in KEEP:
            continue
        text = text[: b.start] + patch_keep(b.text, cid) + text[b.end :]
        print("patched", cid)
    text = remap_refs(text)
    text = remove_moditems(text, CUT)
    atomic_write(ITEMS, text)
    remove_metadata(CUT)
    patch_companions()
    t = ITEMS.read_text(encoding="utf-8")
    for cid in CUT:
        if cid in t:
            print("LEFTOVER", cid)
            return 1
    print("OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
