# -*- coding: utf-8 -*-
"""Restore metadata.code + items.lua ModItemCode dropped by Mod Editor / Steam resave.

Compares current metadata.code to a git revision (default: parent of the Steam
Workshop rewrite) and re-inserts missing paths that still exist on disk, using
the historical neighbor order. Also adds matching ModItemCode rows in items.lua
so the next editor SaveDef does not drop them again.

Usage:
  python docs/tools/_restore_dropped_metadata_code.py
  python docs/tools/_restore_dropped_metadata_code.py --from-rev 8d7a1536
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
META = ROOT / "metadata.lua"
ITEMS = ROOT / "items.lua"

# Dormant / source-only: keep out of metadata.code even if a old revision listed them.
SKIP_RESTORE = {
    "Code/AIPolicyAttackAP.lua",
    "Code/AimHiringScreen_Template.lua",
    "Code/CodeSounds_SMG.lua",
    "Code/EmptySquadFix.lua",
    "Code/PatrollingFix.lua",
    "Code/Savefix.lua",
    "Code/System_AME_Browser_Template.lua",
    "Code/System_MERC_Browser_Template.lua",
    "Code/WeaponIconBake.lua",
}

CODE_BLOCK_RE = re.compile(r"('code',\s*\{)(.*?)(\n\t\},)", re.S)
MODITEM_CODE_RE = re.compile(r"'CodeFileName',\s*\"(Code/[^\"]+)\"")


def run_git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True, encoding="utf-8")


def read_text_nl(path: Path) -> tuple[str, str]:
    raw = path.read_bytes()
    nl = "\r\n" if b"\r\n" in raw else "\n"
    text = raw.decode("utf-8-sig").replace("\r\n", "\n").replace("\r", "\n")
    return text, nl


def write_text_nl(path: Path, text: str, nl: str) -> None:
    path.write_bytes(text.replace("\n", nl).encode("utf-8"))


def extract_code_entries(text: str) -> list[str]:
    m = CODE_BLOCK_RE.search(text)
    if not m:
        raise SystemExit("metadata 'code' block not found")
    return re.findall(r'"([^"]+)"', m.group(2))


def rebuild_code_block(text: str, entries: list[str]) -> str:
    lines = [f'\t\t"{e}",' for e in entries]
    new_body = "\n" + "\n".join(lines)

    def repl(m: re.Match[str]) -> str:
        return m.group(1) + new_body + m.group(3)

    new_text, n = CODE_BLOCK_RE.subn(repl, text, count=1)
    if n != 1:
        raise SystemExit("failed to rewrite metadata code block")
    return new_text


def merge_restore(current: list[str], historic: list[str], disk: set[str]) -> tuple[list[str], list[str]]:
    present = set(current)
    restored: list[str] = []
    out = list(current)
    # Insert each missing historic path after the nearest earlier historic neighbor
    # that is already in `out`. Fall back to nearest later neighbor, else append.
    hist_index = {e: i for i, e in enumerate(historic)}
    for path in historic:
        if path in present:
            continue
        if path in SKIP_RESTORE:
            continue
        if path not in disk:
            print(f"SKIP missing-on-disk {path}")
            continue
        hi = hist_index[path]
        insert_at = None
        for j in range(hi - 1, -1, -1):
            prev = historic[j]
            if prev in present:
                insert_at = out.index(prev) + 1
                break
        if insert_at is None:
            for j in range(hi + 1, len(historic)):
                nxt = historic[j]
                if nxt in present:
                    insert_at = out.index(nxt)
                    break
        if insert_at is None:
            insert_at = len(out)
        out.insert(insert_at, path)
        present.add(path)
        restored.append(path)
    return out, restored


def code_item_snippet(path: str, indent: str) -> str:
    name = Path(path).stem
    return (
        f"{indent}PlaceObj('ModItemCode', {{\n"
        f"{indent}\t'name', \"{name}\",\n"
        f"{indent}\t'CodeFileName', \"{path}\",\n"
        f"{indent}}}),\n"
    )


def placeobj_indent_before(text: str, idx: int) -> str:
    """Indent of the PlaceObj('ModItemCode' line, not the nested CodeFileName line."""
    place = text.rfind("PlaceObj('ModItemCode'", 0, idx + 1)
    if place < 0:
        line_start = text.rfind("\n", 0, idx) + 1
    else:
        line_start = text.rfind("\n", 0, place) + 1
    indent = ""
    while line_start + len(indent) < len(text) and text[line_start + len(indent)] in " \t":
        indent += text[line_start + len(indent)]
    return indent


def insert_moditem_codes(
    items_text: str, paths: list[str], historic: list[str]
) -> tuple[str, list[str]]:
    existing = set(MODITEM_CODE_RE.findall(items_text))
    added: list[str] = []
    text = items_text
    hist_index = {e: i for i, e in enumerate(historic)}
    for path in paths:
        if path in existing:
            continue
        needle = None
        hi = hist_index.get(path)
        if hi is not None:
            for j in range(hi - 1, -1, -1):
                prev = historic[j]
                if not prev.startswith("Code/"):
                    continue
                pat = f"'CodeFileName', \"{prev}\""
                if pat in text:
                    needle = pat
                    break
        if needle is None:
            for nxt in historic[hi + 1 :] if hi is not None else []:
                if not nxt.startswith("Code/"):
                    continue
                pat = f"'CodeFileName', \"{nxt}\""
                if pat in text:
                    needle = pat
                    break
        if needle is None:
            raise SystemExit(f"no items.lua sibling for {path}")
        idx = text.find(needle)
        close = text.find("}),", idx)
        if close < 0:
            raise SystemExit(f"cannot find ModItemCode closer after {needle}")
        insert_at = close + 3
        indent = placeobj_indent_before(text, idx)
        snippet = "\n" + code_item_snippet(path, indent)
        later = hi is not None and needle.split('"')[1] in historic[hi + 1 :]
        if later:
            place = text.rfind("PlaceObj('ModItemCode'", 0, idx)
            if place < 0:
                raise SystemExit(f"cannot find PlaceObj for later neighbor {needle}")
            insert_at = place
            snippet = code_item_snippet(path, indent)
        text = text[:insert_at] + snippet + text[insert_at:]
        existing.add(path)
        added.append(path)
    return text, added


def restore_from_items(current: list[str], items_text: str) -> tuple[list[str], list[str]]:
    """Re-insert metadata.code paths that still exist as ModItemCode after SaveDef drop."""
    wanted = MODITEM_CODE_RE.findall(items_text)
    present = set(current)
    out = list(current)
    restored: list[str] = []
    for path in wanted:
        if path in present:
            continue
        # Insert after previous wanted path that is already in `out`.
        insert_at = None
        wi = wanted.index(path)
        for j in range(wi - 1, -1, -1):
            prev = wanted[j]
            if prev in present:
                insert_at = out.index(prev) + 1
                break
        if insert_at is None:
            for j, e in enumerate(out):
                if e.startswith("Code/"):
                    insert_at = j
                    break
        if insert_at is None:
            insert_at = len(out)
        out.insert(insert_at, path)
        present.add(path)
        restored.append(path)
    return out, restored


def drop_flat_vanillunique(entries: list[str]) -> tuple[list[str], list[str]]:
    vanillunique = {Path(p).name for p in entries if p.startswith("InventoryItem/vanillunique/")}
    if not vanillunique:
        return entries, []
    dropped: list[str] = []
    kept: list[str] = []
    for e in entries:
        name = Path(e).name
        if e.startswith("InventoryItem/") and not e.startswith("InventoryItem/vanillunique/") and name in vanillunique:
            dropped.append(e)
            continue
        kept.append(e)
    return kept, dropped


def default_from_rev() -> str:
    # Parent of the Steam Workshop metadata rewrite if present, else HEAD~1.
    try:
        show = run_git("log", "--oneline", "-20", "--", "metadata.lua")
    except subprocess.CalledProcessError:
        return "HEAD~1"
    for line in show.splitlines():
        if "Steam Workshop" in line:
            sha = line.split()[0]
            return f"{sha}^"
    return "HEAD~1"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--from-rev", default="", help="git revision with the good code list")
    parser.add_argument(
        "--from-items",
        action="store_true",
        help="after editor SaveDef: restore metadata.code from items.lua ModItemCode",
    )
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    current_text, meta_nl = read_text_nl(META)
    current = extract_code_entries(current_text)
    items_text, items_nl = read_text_nl(ITEMS)

    if args.from_items:
        merged, restored = restore_from_items(current, items_text)
        print(f"restore from items.lua ModItemCode ({len(restored)} missing)")
        for p in restored:
            print(f"  + {p}")
        merged, dropped_flat = drop_flat_vanillunique(merged)
        if dropped_flat:
            print(f"dropped flat vanillunique aliases: {len(dropped_flat)}")
            for p in dropped_flat:
                print(f"  - {p}")
        if args.dry_run:
            print("dry-run: no write")
            return 0
        if restored or dropped_flat:
            write_text_nl(META, rebuild_code_block(current_text, merged), meta_nl)
            print("wrote metadata.lua")
        else:
            print("metadata.code already matches items.lua ModItemCode")
        return 0

    from_rev = args.from_rev or default_from_rev()
    print(f"restore from {from_rev}")

    historic_text = run_git("show", f"{from_rev}:metadata.lua")
    historic = extract_code_entries(historic_text)
    disk = {p.relative_to(ROOT).as_posix() for p in (ROOT / "Code").rglob("*.lua")}
    for folder in ("InventoryItem", "CharacterEffect", "Const", "Entities"):
        d = ROOT / folder
        if d.is_dir():
            disk |= {p.relative_to(ROOT).as_posix() for p in d.rglob("*.lua")}

    merged, restored = merge_restore(current, historic, disk)
    print(f"historic entries: {len(historic)}")
    print(f"current entries: {len(current)}")
    print(f"merged entries: {len(merged)}")
    print(f"restored: {len(restored)}")
    for p in restored:
        print(f"  + {p}")

    extra_current = [e for e in current if e not in set(historic)]
    if extra_current:
        print(f"kept current-only entries: {len(extra_current)}")
        for p in extra_current:
            print(f"  keep {p}")

    merged, dropped_flat = drop_flat_vanillunique(merged)
    if dropped_flat:
        print(f"dropped flat vanillunique aliases: {len(dropped_flat)}")
        for p in dropped_flat:
            print(f"  - {p}")

    code_restored = [p for p in restored if p.startswith("Code/")]
    new_items, items_added = insert_moditem_codes(items_text, code_restored, historic)
    print(f"items.lua ModItemCode added: {len(items_added)}")
    for p in items_added:
        print(f"  items + {p}")

    if args.dry_run:
        print("dry-run: no write")
        return 0

    write_text_nl(META, rebuild_code_block(current_text, merged), meta_nl)
    if items_added:
        write_text_nl(ITEMS, new_items, items_nl)
    print("wrote metadata.lua" + (" + items.lua" if items_added else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
