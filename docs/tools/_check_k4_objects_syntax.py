"""Static syntax sanity check for K4 objects.lua."""
from __future__ import annotations

import re
from pathlib import Path

MAP = Path(r"C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz-maps\Maps\gsSMikN\objects.lua")


def balance(text: str) -> None:
    pairs = {")": "(", "}": "{", "]": "["}
    opens = set(pairs.values())
    stack: list[tuple[str, int]] = []
    i, n, line = 0, len(text), 1
    while i < n:
        c = text[i]
        if c == "\n":
            line += 1
            i += 1
            continue
        if c == "-" and i + 1 < n and text[i + 1] == "-":
            nl = text.find("\n", i)
            if nl < 0:
                break
            i = nl
            continue
        if c in ("'", '"'):
            q = c
            i += 1
            while i < n:
                if text[i] == "\\":
                    i += 2
                    continue
                if text[i] == q:
                    i += 1
                    break
                if text[i] == "\n":
                    line += 1
                i += 1
            continue
        if c in opens:
            stack.append((c, line))
        elif c in pairs:
            if not stack or stack[-1][0] != pairs[c]:
                raise SystemExit(f"unbalanced {c} at line {line}, stack={stack[-5:]}")
            stack.pop()
        i += 1
    if stack:
        raise SystemExit(f"unclosed {stack[:8]} leftover={len(stack)}")


def main() -> None:
    text = MAP.read_text(encoding="utf-8")
    orphans = [i + 1 for i, line in enumerate(text.splitlines()) if re.match(r"^,\s*nil,", line)]
    if orphans:
        raise SystemExit(f"orphan closers at {orphans}")
    if "PlaceObj('UnitDataSpawnDef'" in text:
        raise SystemExit("bad UnitDataSpawnDef class still present")
    wave = text.count("VillaSiege_Wave2")
    if wave != 25:
        raise SystemExit(f"VillaSiege_Wave2 count {wave}")
    if not text.rstrip().endswith("LoadPersistFlagTables()"):
        raise SystemExit("file does not end with LoadPersistFlagTables()")
    balance(text)
    print("K4 objects.lua syntax ok")
    print("lines", text.count("\n"))
    print("VillaSiege_Wave2", wave)


if __name__ == "__main__":
    main()
