# -*- coding: utf-8 -*-
"""Remove StartingPerks Spiritual from JAZZ_Legion_* UnitData (companion + items.lua).

Spiritual guarantees min accuracy on hopeless attacks (through terrain).
Does not touch rebels, thugs, mercs, or vanilla Legion* ids.

  python docs/tools/_strip_jazz_legion_spiritual.py
"""
from __future__ import annotations

import re
from pathlib import Path

JAZZ = Path(__file__).resolve().parents[2]
UNITS = JAZZ.parent / "jazz-units"
SPIRIT_LINE = re.compile(r'^[ \t]*"Spiritual",?[ \t]*\r?\n', re.M)
ID_RE = re.compile(r"""['\"]Id['\"],\s*['\"](JAZZ_Legion_[^'\"]+)['\"]""")


def strip_spirit(text: str) -> tuple[str, int]:
    new, n = SPIRIT_LINE.subn("", text)
    return new, n


def read_text(path: Path) -> tuple[str, str]:
    raw = path.read_bytes()
    nl = "\r\n" if b"\r\n" in raw else "\n"
    return raw.decode("utf-8").replace("\r\n", "\n").replace("\r", "\n"), nl


def write_text(path: Path, text: str, nl: str) -> None:
    data = text.replace("\n", nl).encode("utf-8")
    path.write_bytes(data)


def companion_pass() -> list[str]:
    log = []
    ud = UNITS / "UnitData"
    for path in sorted(ud.glob("JAZZ_Legion_*.lua")):
        raw, nl = read_text(path)
        new, n = strip_spirit(raw)
        if n:
            write_text(path, new, nl)
            log.append(f"{path.name}: -{n}")
    return log


def items_pass() -> list[str]:
    path = UNITS / "items.lua"
    text, nl = read_text(path)
    needle = "PlaceObj('ModItemUnitDataCompositeDef'"
    out: list[str] = []
    i = 0
    n_units = 0
    n_lines = 0
    while True:
        j = text.find(needle, i)
        if j < 0:
            out.append(text[i:])
            break
        out.append(text[i:j])
        brace = text.find("{", j)
        if brace < 0:
            raise SystemExit("no { after ModItemUnitDataCompositeDef")
        depth = 0
        k = brace
        while k < len(text):
            c = text[k]
            if c == "{":
                depth += 1
            elif c == "}":
                depth -= 1
                if depth == 0:
                    k += 1
                    break
            k += 1
        block = text[j:k]
        uid = ID_RE.search(block)
        if uid:
            new, n = strip_spirit(block)
            if n:
                n_units += 1
                n_lines += n
                block = new
        out.append(block)
        i = k
    write_text(path, "".join(out), nl)
    return [f"items.lua: {n_units} JAZZ_Legion units, -{n_lines} Spiritual lines"]


def leftover() -> list[str]:
    hits = []
    for path in (UNITS / "UnitData").glob("JAZZ_Legion_*.lua"):
        if "Spiritual" in path.read_text(encoding="utf-8"):
            hits.append(path.name)
    return hits


def main() -> int:
    if not (UNITS / "items.lua").is_file():
        print(f"missing {UNITS / 'items.lua'}")
        return 1
    for line in companion_pass():
        print(line)
    for line in items_pass():
        print(line)
    left = leftover()
    if left:
        print("FAIL leftover companions:", ", ".join(left))
        return 1
    print("OK no Spiritual on JAZZ_Legion_* companions")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
