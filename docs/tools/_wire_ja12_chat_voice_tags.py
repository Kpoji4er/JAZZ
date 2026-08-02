# -*- coding: utf-8 -*-
"""Add voice:Jazz_* comments to WIP AIM-chat T() lines missing them.

Targets Offline/GreetingAndOffer/ConversationRestart/IdleLine/PartingWords/
RehireIntro/RehireOutro ChatMessage lines in UnitData companions + items.lua.

Usage (jazz/):
  python docs/tools/_wire_ja12_chat_voice_tags.py --dry-run
  python docs/tools/_wire_ja12_chat_voice_tags.py --apply
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

JU = Path(r"C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz-units")
CHAT_FIELDS = (
    "Offline",
    "GreetingAndOffer",
    "ConversationRestart",
    "IdleLine",
    "PartingWords",
    "RehireIntro",
    "RehireOutro",
)

# Compact WIP lines, e.g.:
#   Offline = { PlaceObj('ChatMessage', { 'Text', T(890…, "Laura offline.") }) },
#   'Offline', { PlaceObj('ChatMessage', { 'Text', T(890…, "Eskimo offline.") }) },
_RE_LINE = re.compile(
    r"(?P<prefix>(?:'|\")?(?P<field>"
    + "|".join(CHAT_FIELDS)
    + r")(?:'|\")?\s*,?\s*=?\s*\{\s*PlaceObj\(\s*'ChatMessage'\s*,\s*\{\s*'Text'\s*,\s*T\()"
    r"(?P<tid>\d+)\s*,\s*"
    r"(?!\[\[)"  # not already a comment-bearing form starting oddly
    r"(?P<body>(?:--\[\[[^\]]*\]\]\s*)?)"
    r"(?P<quote>[\"'])(?P<text>.*?)(?P=quote)",
)


def wire_text(text: str, unit: str) -> tuple[str, int]:
    n = 0

    def repl(m: re.Match) -> str:
        nonlocal n
        if f"voice:{unit}" in (m.group("body") or ""):
            return m.group(0)
        if m.group("body") and "--[[" in m.group("body"):
            return m.group(0)
        n += 1
        field = m.group("field")
        comment = (
            f"--[[ModItemUnitDataCompositeDef {unit} Text {field} "
            f"ChatMessage voice:{unit}]] "
        )
        return (
            f"{m.group('prefix')}{m.group('tid')}, {comment}"
            f"{m.group('quote')}{m.group('text')}{m.group('quote')}"
        )

    return _RE_LINE.sub(repl, text), n


def _unit_ok(unit: str, only: set[str]) -> bool:
    if not only:
        return True
    slug = unit.replace("Jazz_", "").lower()
    return slug in {o.lower().replace("jazz_", "") for o in only}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--only", type=str, default="")
    args = ap.parse_args()
    apply = args.apply and not args.dry_run
    only = {s.strip() for s in args.only.split(",") if s.strip()}

    total = 0
    for path in sorted((JU / "UnitData").glob("Jazz_*.lua")):
        unit = path.stem
        if not _unit_ok(unit, only):
            continue
        raw = path.read_text(encoding="utf-8", errors="replace")
        wired, n = wire_text(raw, unit)
        if n:
            print(f"{path.name}: {n}")
            total += n
            if apply:
                path.write_text(wired, encoding="utf-8")

    items = JU / "items.lua"
    raw = items.read_text(encoding="utf-8", errors="replace")
    parts = re.split(r"(PlaceObj\('ModItemUnitDataCompositeDef',\s*\{)", raw)
    out = [parts[0]]
    file_n = 0
    i = 1
    while i < len(parts):
        head = parts[i]
        body = parts[i + 1] if i + 1 < len(parts) else ""
        chunk = head + body
        idm = re.search(r"'Id',\s*\"(Jazz_[^\"]+)\"", chunk) or re.search(
            r'id = "(Jazz_[^"]+)"', chunk
        )
        if idm and _unit_ok(idm.group(1), only):
            wired, n = wire_text(chunk, idm.group(1))
            file_n += n
            chunk = wired
        out.append(chunk)
        i += 2
    if file_n:
        print(f"items.lua: {file_n}")
        total += file_n
        if apply:
            items.write_text("".join(out), encoding="utf-8")

    print(f"TOTAL {total} mode={'APPLY' if apply else 'DRY-RUN'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
