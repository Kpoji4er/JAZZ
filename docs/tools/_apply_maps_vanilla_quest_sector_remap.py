#!/usr/bin/env python3
"""Apply JAZZ-QUESTS-002 vanilla quest sector remaps in jazz-maps (idempotent).

Remaps HotDiamonds landmark IDs inside ModItemQuestsDef / selected conversations
and ModTextsMaps.csv. Does not touch ModItemSector, satellite images, descr_id,
jazz-nomaps, or Jazz_*/JAZZ_* Ernie-local quests.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

CORE = Path(__file__).resolve().parents[2]
DEFAULT_MAPS = CORE.parent / "jazz-maps"

# vanilla → maps (table + runtime Emerald Coast I3→J7)
LANDMARK_REMAP: dict[str, str] = {
    "A2": "A4",
    "A11": "B15",
    "A20": "B28",
    "B2": "C6",
    "B12": "A25",
    "B13": "A26",
    "B16": "D22",
    "C5": "D9",
    "C7": "E15",
    "D7": "E15",
    "D8": "E16",
    "D10": "F23",
    "E9": "F13",
    "F5": "G9",
    "H2": "I5",
    "H3": "I6",
    "H4": "I7",
    "H7": "H14",  # Fleatown mine journal; logic may already be H14
    "I3": "J7",  # Emerald Coast runtime (not sheet M7)
}

CROCODILE_REMAP = {"H14": "P17"}  # Elliot journal / crocodile only

# Wave A+B from JAZZ-QUESTS-002 (+ Elliot journal fix)
IN_SCOPE_QUESTS = frozenset(
    {
        "DiamondRed",
        "RefugeeBlues",
        "FaithHealing",
        "JoseFamily",
        "Evidence",
        "Sanatorium",
        "HunterHunted",
        "NeverHitAGirl",
        "MiddleOfNowhere",
        "MiddleOfXWhere",
        "Landsbach",
        "U-Bahn",
        "U-Bahn_Helpers",
        "TreasureHunting",
        "Elliot",
        "05_TakeDownMajor",
        "YoungHearts",
        "RebelManifesto",
        "PantragruelWatch",
        "PantagruelRebels",
        "PantagruelLostAndFound",
        "PantagruelDramas",
        "PantagruelClinic",
        "Smiley",
        "RescueBiff",
        "04_Betrayal",
        "CorazonCaptureMine",
        "PierreDefeated",
        "Larry",
        "TheTwelveChairs",
        "GlobalCivilians",
        "_GroupsAttacked",
        "Emails",
    }
)

IN_SCOPE_CONVERSATIONS = frozenset(
    {
        "Pierre_2",
        "FlagHill_Corazon_1",
    }
)

# Field / list patterns that carry sector IDs (not descr_id / image paths).
FIELD_KEYS = (
    "Sector",
    "sector_id",
    "SectorID",
    "source_sector_id",
    "guardpost_sector_id",
)


def is_custom_ernie(quest_id: str) -> bool:
    return quest_id.startswith("Jazz_") or quest_id.startswith("JAZZ_")


def iter_moditem_blocks(text: str, kind: str) -> list[tuple[int, int, str, str]]:
    """Return (start, end, id, body) for PlaceObj('kind', ...) sibling-bounded blocks."""
    marker = f"PlaceObj('{kind}',"
    out: list[tuple[int, int, str, str]] = []
    start = 0
    while True:
        idx = text.find(marker, start)
        if idx < 0:
            break
        body_start = idx + len(marker)
        # Presets are indented inside nested PlaceObj trees.
        nxt = re.search(r"\n[\t ]*PlaceObj\('ModItem", text[body_start:])
        body_end = body_start + nxt.start() if nxt else len(text)
        body = text[body_start:body_end]
        mid = re.search(r"\bid\s*=\s*\"([^\"]+)\"", body)
        if mid:
            out.append((idx, body_end, mid.group(1), body))
        start = body_end
    return out


def remap_ordered(pairs: dict[str, str]) -> list[tuple[str, str]]:
    # Longer IDs first so A20 is not eaten by A2, etc.
    return sorted(pairs.items(), key=lambda kv: (-len(kv[0]), kv[0]))


def replace_sector_refs(body: str, pairs: dict[str, str]) -> tuple[str, int]:
    """Replace typed sector references; skip descr_id lines."""
    total = 0
    lines = body.splitlines(keepends=True)
    out_lines: list[str] = []
    for line in lines:
        if "descr_id" in line or "SectorImages/" in line:
            out_lines.append(line)
            continue
        new_line = line
        for old, new in remap_ordered(pairs):
            if old == new:
                continue
            patterns = [
                # items.lua often escapes quotes: SectorName(\'A2\')
                (
                    rf"(SectorName\(\\'){re.escape(old)}(\\'\))",
                    rf"\g<1>{new}\2",
                ),
                # ModTexts / rare unescaped: SectorName('A2')
                (
                    rf"(SectorName\('){re.escape(old)}('\))",
                    rf"\g<1>{new}\2",
                ),
                (
                    rf"\b((?:{'|'.join(FIELD_KEYS)})\s*=\s*\"){re.escape(old)}(\")",
                    rf"\g<1>{new}\2",
                ),
                (
                    rf"(\bgv_Sectors\.){re.escape(old)}(\b)",
                    rf"\g<1>{new}\2",
                ),
                # quoted list entries in requiredSectors / Sectors / effect_target_sector_ids
                (
                    rf"(?<![A-Za-z0-9_])(\"){re.escape(old)}(\")(?![A-Za-z0-9_])",
                    rf"\g<1>{new}\2",
                ),
            ]
            for pat, repl in patterns:
                new_line, n = re.subn(pat, repl, new_line)
                total += n
        out_lines.append(new_line)
    return "".join(out_lines), total


def remap_quest_block(quest_id: str, body: str) -> tuple[str, int]:
    pairs = dict(LANDMARK_REMAP)
    if quest_id == "Elliot":
        pairs.update(CROCODILE_REMAP)
    # TreasureHunting / CorazonCaptureMine / mine contexts: do NOT map H14→P17
    # (H14 already means mine after H7→H14).
    return replace_sector_refs(body, pairs)


def remap_conversation_block(conv_id: str, body: str) -> tuple[str, int]:
    pairs = dict(LANDMARK_REMAP)
    # FlagHill Mfumu's Mine: keep H14; fix bad SectorCheckOwner P17→H14 for that lead.
    if conv_id == "FlagHill_Corazon_1":
        fixed = body
        # Only the Mfumu / Lead_RuinsMine phrase wrongly uses P17 as owner check.
        bad = (
            "PlaceObj('SectorCheckOwner', {\n"
            "\t\t\t\t\t\t\t\tNegate = true,\n"
            "\t\t\t\t\t\t\t\tparam_bindings = false,\n"
            '\t\t\t\t\t\t\t\tsector_id = "P17",\n'
            "\t\t\t\t\t\t\t}),\n"
            "\t\t\t\t\t\t},\n"
            "\t\t\t\t\t\tEffects = {\n"
            "\t\t\t\t\t\t\tPlaceObj('SectorGrantIntel', {\n"
            "\t\t\t\t\t\t\t\tparam_bindings = false,\n"
            '\t\t\t\t\t\t\t\tsector_id = "H14",\n'
            "\t\t\t\t\t\t\t}),\n"
            "\t\t\t\t\t\t\tPlaceObj('QuestSetVariableBool', {\n"
            '\t\t\t\t\t\t\t\tProp = "Lead_RuinsMine",\n'
        )
        good = bad.replace('sector_id = "P17"', 'sector_id = "H14"', 1)
        n_fix = 0
        if bad in fixed:
            fixed = fixed.replace(bad, good, 1)
            n_fix = 1
        elif good in fixed or (
            'Prop = "Lead_RuinsMine"' in fixed
            and re.search(
                r'Lead_RuinsMine[\s\S]{0,400}?sector_id = "H14"',
                fixed,
            )
            is None
            and 'sector_id = "P17"' not in fixed.split('Lead_RuinsMine')[0][-200:]
        ):
            # already fixed or different formatting — continue with A2 remap
            pass
        remapped, n = replace_sector_refs(fixed, pairs)
        return remapped, n + n_fix
    return replace_sector_refs(body, pairs)


def patch_items(text: str) -> tuple[str, dict[str, int]]:
    counts: dict[str, int] = {}
    # Process from end so offsets stay valid.
    blocks = iter_moditem_blocks(text, "ModItemQuestsDef")
    blocks += iter_moditem_blocks(text, "ModItemConversation")
    blocks.sort(key=lambda b: b[0], reverse=True)

    for start, end, obj_id, body in blocks:
        kind_is_quest = text.startswith("PlaceObj('ModItemQuestsDef'", start) or (
            "ModItemQuestsDef" in text[start : start + 40]
        )
        # Detect kind from marker at start
        marker_slice = text[start : start + 40]
        if "ModItemQuestsDef" in marker_slice:
            if is_custom_ernie(obj_id) or obj_id not in IN_SCOPE_QUESTS:
                continue
            new_body, n = remap_quest_block(obj_id, body)
        elif "ModItemConversation" in marker_slice:
            if obj_id not in IN_SCOPE_CONVERSATIONS:
                continue
            new_body, n = remap_conversation_block(obj_id, body)
        else:
            continue
        if n:
            counts[obj_id] = counts.get(obj_id, 0) + n
            # body is text[body_start:end] where body_start = start+len(marker)
            # Reconstruct carefully: we stored body as after marker
            marker = (
                "PlaceObj('ModItemQuestsDef',"
                if "ModItemQuestsDef" in marker_slice
                else "PlaceObj('ModItemConversation',"
            )
            body_start = start + len(marker)
            text = text[:body_start] + new_body + text[end:]
    return text, counts


def patch_modtexts(csv_path: Path) -> tuple[str, int]:
    """Replace SectorName('OLD') in ModTextsMaps without rewriting CSV quoting."""
    raw_bytes = csv_path.read_bytes()
    bom = raw_bytes.startswith(b"\xef\xbb\xbf")
    raw = raw_bytes.decode("utf-8-sig")
    total = 0
    lines = raw.splitlines(keepends=True)
    out: list[str] = []
    for line in lines:
        pairs = dict(LANDMARK_REMAP)
        # Crocodile journal only — never remap Fleatown mine H14 in ModTexts.
        if "Elliot" in line:
            pairs.update(CROCODILE_REMAP)
        new_line = line
        for old, new in remap_ordered(pairs):
            if old == new:
                continue
            pat = re.compile(rf"SectorName\('{re.escape(old)}'\)")
            new_line, n = pat.subn(f"SectorName('{new}')", new_line)
            total += n
        out.append(new_line)
    text = "".join(out)
    if bom:
        text = "\ufeff" + text
    return text, total


def sector_hits_in_body(body: str, sector: str) -> bool:
    pats = [
        rf"SectorName\(\\'{re.escape(sector)}\\'\)",
        rf"SectorName\('{re.escape(sector)}'\)",
        rf"\bSector = \"{re.escape(sector)}\"",
        rf"\bsector_id = \"{re.escape(sector)}\"",
        rf"\bSectorID = \"{re.escape(sector)}\"",
        rf"\bsource_sector_id = \"{re.escape(sector)}\"",
        rf"\bguardpost_sector_id = \"{re.escape(sector)}\"",
        rf"\bgv_Sectors\.{re.escape(sector)}\b",
        rf"requiredSectors = \{{[^}}]*\"{re.escape(sector)}\"",
        rf"Sectors = \{{[^}}]*\"{re.escape(sector)}\"",
    ]
    return any(re.search(p, body) for p in pats)


def residual_stale(text: str) -> list[tuple[str, list[str]]]:
    rows: list[tuple[str, list[str]]] = []
    for _s, _e, qid, body in iter_moditem_blocks(text, "ModItemQuestsDef"):
        if is_custom_ernie(qid) or qid not in IN_SCOPE_QUESTS:
            continue
        stale = []
        check = dict(LANDMARK_REMAP)
        if qid == "Elliot":
            check.update(CROCODILE_REMAP)
        for old in check:
            if sector_hits_in_body(body, old):
                # After H7→H14, H14 is correct for mine quests — not stale.
                if old == "H14" and qid != "Elliot":
                    continue
                stale.append(old)
        if stale:
            rows.append((qid, sorted(stale, key=lambda x: (-len(x), x))))
    return rows


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--maps-root", type=Path, default=DEFAULT_MAPS)
    parser.add_argument(
        "--check",
        action="store_true",
        help="Dry-run: report counts / residual; exit 1 if stale remain after simulated apply",
    )
    parser.add_argument("--apply", action="store_true", help="Write patched files")
    args = parser.parse_args()
    if not args.check and not args.apply:
        args.check = True

    maps = args.maps_root.resolve()
    items_path = maps / "items.lua"
    modtexts_path = maps / "ModTextsMaps.csv"

    items = items_path.read_text(encoding="utf-8")
    new_items, item_counts = patch_items(items)
    new_modtexts, mt_count = patch_modtexts(modtexts_path)

    residual = residual_stale(new_items)
    mode = "apply" if args.apply else "check"
    print(f"mode={mode} maps_root={maps}")
    print(f"items_blocks_touched={len(item_counts)} replacements={sum(item_counts.values())}")
    for qid, n in sorted(item_counts.items(), key=lambda kv: (-kv[1], kv[0])):
        print(f"  {qid}: {n}")
    print(f"modtexts_sectorname_replacements={mt_count}")
    print(f"residual_stale_quests={len(residual)}")
    for qid, stale in residual:
        print(f"  {qid}: {', '.join(stale)}")

    if args.apply:
        if new_items != items:
            items_path.write_text(new_items, encoding="utf-8", newline="\n")
            print(f"wrote {items_path}")
        else:
            print(f"unchanged {items_path}")
        old_mod = modtexts_path.read_bytes()
        new_mod_bytes = new_modtexts.encode("utf-8")
        # patch_modtexts may prefix U+FEFF; encode keeps it as UTF-8 BOM
        if new_mod_bytes != old_mod and new_mod_bytes.lstrip(b"\xef\xbb\xbf") != old_mod.lstrip(
            b"\xef\xbb\xbf"
        ):
            modtexts_path.write_bytes(new_mod_bytes)
            print(f"wrote {modtexts_path}")
        else:
            print(f"unchanged {modtexts_path}")

    if residual:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
