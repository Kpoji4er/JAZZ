#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Full-replace metadata.lua last_changes for a Steam Workshop upload.

Does not bump Revision. Writes one physical Lua line with \\n escapes only
(no raw LF/CR inside the quotes). Changelog text must not contain { or }
(metadata.lua brace-balance gate) or unescaped double quotes.

After an editor SaveDef of metadata.lua, run
`python docs/tools/_validate_items_quick.py`. If Code files dropped, restore
with `python docs/tools/_restore_dropped_metadata_code.py --from-items`
(requires those files to exist as ModItemCode in items.lua).

Default notes: docs/tools/_steam_last_changes_since_aug12.txt
(bullets after Steam window 12 Aug 2026 through today).

Older draft kept: _steam_last_changes_since_aug8.txt.

  python docs/tools/_replace_steam_last_changes.py --apply
  python docs/tools/_replace_steam_last_changes.py --text-file notes.txt --apply
"""
from __future__ import annotations

import argparse
import codecs
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_METADATA = ROOT / "metadata.lua"
DEFAULT_TEXT = Path(__file__).with_name("_steam_last_changes_since_aug12.txt")

LAST_CHANGES_RE = re.compile(r"('last_changes',\s*\")((?:\\.|[^\"\\])*)(\")")


def to_lua_string(text: str) -> str:
    if "{" in text or "}" in text:
        raise SystemExit("changelog must not contain { or } (metadata brace balance)")
    if "\r" in text:
        raise SystemExit("changelog contains CR")
    if '"' in text:
        raise SystemExit('changelog must not contain " — they break the Lua short string')
    return text.replace("\\", "\\\\").replace("\n", "\\n")


def load_text(path: Path) -> str:
    raw = path.read_text(encoding="utf-8-sig")
    return raw.replace("\r\n", "\n").replace("\r", "\n").strip("\n")


def replace_last_changes(metadata: Path, changelog: str, apply: bool) -> int:
    lua_val = to_lua_string(changelog)
    raw = metadata.read_bytes()
    has_bom = raw.startswith(codecs.BOM_UTF8)
    text = raw.decode("utf-8-sig")
    matches = list(LAST_CHANGES_RE.finditer(text))
    if len(matches) != 1:
        raise SystemExit(f"{metadata}: expected 1 last_changes string, found {len(matches)}")
    m = matches[0]
    patched = text[: m.start(2)] + lua_val + text[m.end(2) :]
    m2 = re.search(r"'last_changes', \"", patched)
    if not m2:
        raise SystemExit("last_changes open quote lost")
    end = patched.find('"', m2.end())
    if end < 0:
        raise SystemExit("last_changes close quote lost")
    chunk = patched[m2.end() : end]
    if "\n" in chunk or "\r" in chunk:
        raise SystemExit("raw newline leaked into last_changes")
    print(f"last_changes chars={len(changelog)} lua_escapes={len(lua_val)} lines={changelog.count(chr(10)) + 1}")
    if not apply:
        print("dry-run (pass --apply to write)")
        print("--- preview head ---")
        print("\n".join(changelog.split("\n")[:12]))
        return 0
    payload = patched.encode("utf-8")
    if has_bom:
        payload = codecs.BOM_UTF8 + payload
    metadata.write_bytes(payload)
    print(f"updated: {metadata}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--metadata", type=Path, default=DEFAULT_METADATA)
    ap.add_argument("--text-file", type=Path, default=DEFAULT_TEXT)
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()
    if not args.text_file.exists():
        raise SystemExit(f"missing changelog file: {args.text_file}")
    changelog = load_text(args.text_file)
    return replace_last_changes(args.metadata, changelog, args.apply)


if __name__ == "__main__":
    raise SystemExit(main())
