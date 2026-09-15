#!/usr/bin/env python3
"""Remap leftover vanilla HotDiamonds IDs in jazz-maps outposts, events, quests.

Follow-up to JAZZ-QUESTS-002: Wave A+B landmark quests are already remapped, but
TargetSectors / sector Events / outpost helper quests still cite old IDs after
the maps grid move.

Idempotent. Does not touch descr_id, SectorImages paths, Jazz_*/JAZZ_* Ernie
quests, maps-local I2/I3, crocodile patrol I18/I19, or Pantagruel E16.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

CORE = Path(__file__).resolve().parents[2]
DEFAULT_MAPS = CORE.parent / "JAZZ Maps"
if not (DEFAULT_MAPS / "items.lua").is_file():
    DEFAULT_MAPS = CORE.parent / "jazz-maps"

# Exact TargetSectors lists (ModItem + CampaignPreset copies).
TARGET_LISTS: list[tuple[str, str]] = [
    (
        """					'TargetSectors', {
						"E16",
						"F19",
						"D18",
						"D17",
						"B13",
						"B12",
					},""",
        """					'TargetSectors', {
						"G22",
						"K21",
						"D18",
						"F28",
						"A26",
						"A25",
					},""",
    ),
    (
        """					'TargetSectors', {
						"D6",
						"D7",
						"E6",
						"A2",
						"A3",
						"B3",
					},""",
        """					'TargetSectors', {
						"E14",
						"E15",
						"E11",
						"A4",
						"A3",
						"C6",
					},""",
    ),
    (
        """					'TargetSectors', {
						"J13",
						"J14",
						"F13",
						"K15",
						"A2",
						"P17",
						"O16",
					},""",
        """					'TargetSectors', {
						"J13",
						"J14",
						"G25",
						"K15",
						"A4",
						"P17",
						"O16",
					},""",
    ),
    (
        """					'TargetSectors', {
						"N13",
						"N12",
						"O13",
						"O16",
						"I18",
						"I19",
						"F13",
						"G10",
					},""",
        """					'TargetSectors', {
						"N13",
						"N12",
						"O13",
						"O16",
						"I18",
						"I19",
						"G25",
						"L15",
					},""",
    ),
]

# Single-entry swaps inside already-partially-remapped lists.
TARGET_ENTRY_SWAPS: list[tuple[str, str]] = [
    ('"D10"', '"D18"'),  # E10 Camp Savane leftover Grand Prix
    ('"C11"', '"C14"'),  # D18 Grand Prix leftover gas station
    ('"G27"', '"G25"'),  # sheet stub Chalet → authored G25
]


def brace_block(text: str, start: int) -> tuple[int, int]:
    depth = 0
    started = False
    i = start
    while i < len(text):
        if text[i] == "{":
            started = True
            depth += 1
        elif text[i] == "}":
            depth -= 1
            if started and depth <= 0:
                return start, i
        i += 1
    return start, len(text) - 1


def iter_moditem_blocks(text: str, kind: str) -> list[tuple[int, int, str, str]]:
    marker = f"PlaceObj('{kind}',"
    out: list[tuple[int, int, str, str]] = []
    start = 0
    while True:
        idx = text.find(marker, start)
        if idx < 0:
            break
        body_start = idx + len(marker)
        nxt = re.search(r"\n[\t ]*PlaceObj\('ModItem", text[body_start:])
        body_end = body_start + nxt.start() if nxt else len(text)
        body = text[body_start:body_end]
        mid = re.search(r"\bid\s*=\s*\"([^\"]+)\"", body)
        if mid:
            out.append((idx, body_end, mid.group(1), body))
        start = body_end
    return out


def remap_ordered(pairs: dict[str, str]) -> list[tuple[str, str]]:
    return sorted(pairs.items(), key=lambda kv: (-len(kv[0]), kv[0]))


def replace_sector_refs(body: str, pairs: dict[str, str]) -> tuple[str, int]:
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
                (rf"(SectorName\(\\'){re.escape(old)}(\\'\))", rf"\g<1>{new}\2"),
                (rf"(SectorName\('){re.escape(old)}('\))", rf"\g<1>{new}\2"),
                (
                    rf"\b((?:Sector|sector_id|SectorID|source_sector_id|guardpost_sector_id)\s*=\s*\"){re.escape(old)}(\")",
                    rf"\g<1>{new}\2",
                ),
                (rf"(\bgv_Sectors\.){re.escape(old)}(\b)", rf"\g<1>{new}\2"),
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


# Quest / conversation scoped remaps (vanilla outpost/city IDs that QUESTS-002
# did not cover because they were not in the landmark table).
QUEST_REMAPS: dict[str, dict[str, str]] = {
    "HunterHunted": {
        "F7": "E10",
        "G10": "L15",
        "F23": "D18",
        "F19": "K21",
        "E16": "G22",
    },
    "05_TakeDownMajor": {
        "F19": "K21",
        "F23": "D18",
        "E16": "G22",
        # F7 skipped: E10 already present in the same TCE
    },
    "04_Betrayal": {
        "F7": "E10",
        "F23": "D18",
        "G10": "L15",
        "E16": "G22",
        "F19": "K21",
    },
    "ReduceSavannaCampStrength": {
        "F7": "E10",
        "G6": "G13",
        "E6": "E9",
        "E7": "E11",
    },
    "ReduceBarrierCampStrength": {"G10": "L15"},
    "ReduceCrossroadsCampStrength": {"C11": "C14", "B9": "C12"},
    "ReduceBienChienCampStrength": {"F19": "K21"},
    "Larry": {"F7": "E10"},
    "TheTwelveChairs": {"F7": "E10", "G10": "L15", "F23": "D18", "I1": "K4"},
    "ChienSauvage": {"E16": "G22"},
    "PierreDefeated": {"F19": "K21"},
    "CampBienChien": {"F19": "K21"},
    "Landsbach": {"C11": "C14", "F23": "D18"},
    "CorazonCaptureMine": {"I18": "H31"},
    "GrimerHamlet_copy": {"I19": "H32"},
    "Sanatorium": {"I19": "H32"},
    "Emails": {"G10": "L15"},
}

CONV_REMAPS: dict[str, dict[str, str]] = {
    "Pierre_2": {"F19": "K21"},
}

MODTEXT_LINE_HINTS: dict[str, dict[str, str]] = {
    "Larry": {"F7": "E10"},
    "TheTwelveChairs": {"F7": "E10", "G10": "L15", "F23": "D18", "I1": "K4"},
    "PierreDefeated": {"F19": "K21"},
    "ChienSauvage": {"E16": "G22"},
    "Landsbach": {"C11": "C14", "F23": "D18"},
    "CorazonCaptureMine": {"I18": "H31"},
    "GrimerHamlet": {"I19": "H32"},
    "Sanatorium": {"I19": "H32"},
}


def patch_target_lists(text: str) -> tuple[str, int]:
    n = 0
    for old, new in TARGET_LISTS:
        c = text.count(old)
        if c:
            text = text.replace(old, new)
            n += c
    return text, n


def patch_target_entries(text: str) -> tuple[str, int]:
    """Swap leftover entries only inside TargetSectors { } blocks."""
    n_total = 0

    def repl(m: re.Match[str]) -> str:
        nonlocal n_total
        block = m.group(0)
        new = block
        for old, nxt in TARGET_ENTRY_SWAPS:
            c = new.count(old)
            if c:
                new = new.replace(old, nxt)
                n_total += c
        return new

    text = re.sub(
        r"'TargetSectors',\s*\{[^{}]*\}",
        repl,
        text,
    )
    return text, n_total


def _rewrite_satellite_events(text: str, sector_id: str, old: str, new: str) -> tuple[str, int]:
    n = 0
    marker = f"'Id', \"{sector_id}\""
    pieces: list[str] = []
    last = 0
    start = 0
    while True:
        idx = text.find(marker, start)
        if idx < 0:
            pieces.append(text[last:])
            break
        p = text.rfind("PlaceObj('SatelliteSector'", 0, idx)
        if p < 0:
            start = idx + len(marker)
            continue
        _, end = brace_block(text, p + len("PlaceObj('SatelliteSector'"))
        body = text[p : end + 1]
        new_body, c = re.subn(
            rf'(sector_id = )"{re.escape(old)}"',
            rf'\1"{new}"',
            body,
        )
        n += c
        pieces.append(text[last:p])
        pieces.append(new_body)
        last = end + 1
        start = end + 1
    return "".join(pieces), n


def patch_self_events(text: str) -> tuple[str, int]:
    n = 0
    text, c = _rewrite_satellite_events(text, "A4", "A2", "A4")
    n += c
    text, c = _rewrite_satellite_events(text, "F13", "E9", "F13")
    n += c
    text, c = _rewrite_satellite_events(text, "L15", "G10", "L15")
    n += c
    return text, n


def patch_scoped_moditems(text: str) -> tuple[str, dict[str, int]]:
    counts: dict[str, int] = {}
    blocks = iter_moditem_blocks(text, "ModItemQuestsDef")
    blocks += iter_moditem_blocks(text, "ModItemConversation")
    blocks.sort(key=lambda b: b[0], reverse=True)
    for start, end, obj_id, body in blocks:
        marker_slice = text[start : start + 40]
        if "ModItemQuestsDef" in marker_slice:
            pairs = QUEST_REMAPS.get(obj_id)
            marker = "PlaceObj('ModItemQuestsDef',"
        elif "ModItemConversation" in marker_slice:
            pairs = CONV_REMAPS.get(obj_id)
            marker = "PlaceObj('ModItemConversation',"
        else:
            continue
        if not pairs:
            continue
        new_body, n = replace_sector_refs(body, pairs)
        if n:
            counts[obj_id] = counts.get(obj_id, 0) + n
            body_start = start + len(marker)
            text = text[:body_start] + new_body + text[end:]
    return text, counts


def patch_emails_chalet(text: str) -> tuple[str, int]:
    """Second F13 in Emails city-OR is leftover vanilla Chalet, not refugee camp."""
    old = """									PlaceObj('SectorCheckOwner', {
										sector_id = "H19",
									}),
									PlaceObj('SectorCheckOwner', {
										sector_id = "D11",
									}),
									PlaceObj('SectorCheckOwner', {
										sector_id = "F13",
									}),
									PlaceObj('SectorCheckOwner', {
										sector_id = "A26",
									}),"""
    new = """									PlaceObj('SectorCheckOwner', {
										sector_id = "H19",
									}),
									PlaceObj('SectorCheckOwner', {
										sector_id = "D11",
									}),
									PlaceObj('SectorCheckOwner', {
										sector_id = "G25",
									}),
									PlaceObj('SectorCheckOwner', {
										sector_id = "A26",
									}),"""
    if old not in text:
        return text, 0
    return text.replace(old, new), text.count(old)


def drop_duplicate_major_f7(text: str) -> tuple[str, int]:
    """05_TakeDownMajor already checks E10; leftover F7 block would double-count."""
    pat = re.compile(
        r"\n\t+\t+PlaceObj\('ConditionalEffect', \{\n"
        r"\t+\t+'Conditions', \{\n"
        r"\t+\t+PlaceObj\('SectorCheckOwner', \{\n"
        r"\t+\t+sector_id = \"E10\",\n"
        r"\t+\t+\}\),\n"
        r"\t+\t+\},\n"
        r"\t+\t+'Effects', \{\n"
        r"\t+\t+PlaceObj\('QuestSetVariableNum', \{\n"
        r"\t+\t+Amount = 5,\n"
        r"\t+\t+Prop = \"Reputation\",\n"
        r"\t+\t+QuestId = \"05_TakeDownMajor\",\n"
        r"\t+\t+\}\),\n"
        r"\t+\t+\},\n"
        r"\t+\t+\}\),",
        re.M,
    )
    # After F7→ skipped, the F7 block remains. Remove it explicitly.
    f7_pat = re.compile(
        r"\n(\t+)PlaceObj\('ConditionalEffect', \{\n"
        r"\1\t'Conditions', \{\n"
        r"\1\t\tPlaceObj\('SectorCheckOwner', \{\n"
        r"\1\t\t\tsector_id = \"F7\",\n"
        r"\1\t\t\}\),\n"
        r"\1\t\},\n"
        r"\1\t'Effects', \{\n"
        r"\1\t\tPlaceObj\('QuestSetVariableNum', \{\n"
        r"\1\t\t\tAmount = 5,\n"
        r"\1\t\t\tProp = \"Reputation\",\n"
        r"\1\t\t\tQuestId = \"05_TakeDownMajor\",\n"
        r"\1\t\t\}\),\n"
        r"\1\t\},\n"
        r"\1\}\),",
    )
    text2, n = f7_pat.subn("\n", text)
    return text2, n


def patch_modtexts(raw: str) -> tuple[str, int]:
    total = 0
    lines = raw.splitlines(keepends=True)
    out: list[str] = []
    for line in lines:
        new_line = line
        for hint, pairs in MODTEXT_LINE_HINTS.items():
            if hint not in line:
                continue
            for old, new in remap_ordered(pairs):
                pat = re.compile(rf"SectorName\('{re.escape(old)}'\)")
                new_line, n = pat.subn(f"SectorName('{new}')", new_line)
                total += n
        out.append(new_line)
    return "".join(out), total


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--maps-root", type=Path, default=DEFAULT_MAPS)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    if not args.check and not args.apply:
        args.check = True

    maps = args.maps_root.resolve()
    items_path = maps / "items.lua"
    modtexts_path = maps / "ModTextsMaps.csv"
    items = items_path.read_text(encoding="utf-8")

    new_items, n_lists = patch_target_lists(items)
    new_items, n_entries = patch_target_entries(new_items)
    new_items, n_events = patch_self_events(new_items)
    new_items, qcounts = patch_scoped_moditems(new_items)
    new_items, n_emails = patch_emails_chalet(new_items)
    new_items, n_drop = drop_duplicate_major_f7(new_items)

    raw_bytes = modtexts_path.read_bytes()
    bom = raw_bytes.startswith(b"\xef\xbb\xbf")
    raw = raw_bytes.decode("utf-8-sig")
    new_mod, mt_count = patch_modtexts(raw)
    if bom:
        new_mod = "\ufeff" + new_mod

    print(f"mode={'apply' if args.apply else 'check'} maps_root={maps}")
    print(f"target_lists={n_lists} target_entries={n_entries} self_events={n_events}")
    print(f"quest_conv_blocks={len(qcounts)} replacements={sum(qcounts.values())} drop_f7={n_drop} emails_chalet={n_emails}")
    for qid, n in sorted(qcounts.items(), key=lambda kv: (-kv[1], kv[0])):
        print(f"  {qid}: {n}")
    print(f"modtexts_sectorname_replacements={mt_count}")

    if args.apply:
        if new_items != items:
            items_path.write_text(new_items, encoding="utf-8", newline="\n")
            print(f"wrote {items_path}")
        else:
            print(f"unchanged {items_path}")
        new_mod_bytes = new_mod.encode("utf-8")
        if new_mod_bytes.lstrip(b"\xef\xbb\xbf") != raw_bytes.lstrip(b"\xef\xbb\xbf"):
            modtexts_path.write_bytes(new_mod_bytes)
            print(f"wrote {modtexts_path}")
        else:
            print(f"unchanged {modtexts_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
