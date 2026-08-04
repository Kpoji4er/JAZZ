# -*- coding: utf-8 -*-
"""Enemy loot: medicine stacks -> 1 (Bandage/Morphine/IFAK/Medkit/Surgical).

Skips ModItemLootDef with group = \"Mercs\". Idempotent.
Does not change drop_chance.
"""
from __future__ import annotations

from pathlib import Path
import re

UNITS = Path(r"C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz-units\items.lua")

ITEMS = (
    "JAZZ_Bandage",
    "JAZZ_Morphine",
    "JAZZ_SurgicalKit",
    "FirstAidKit",
    "Medkit",
)
STACK = 1


def block_end(text: str, start: int) -> int:
    i = text.find("{", start)
    depth = 0
    for j in range(i, len(text)):
        if text[j] == "{":
            depth += 1
        elif text[j] == "}":
            depth -= 1
            if depth == 0:
                k = j + 1
                if k < len(text) and text[k] == ")":
                    k += 1
                if k < len(text) and text[k] == ",":
                    k += 1
                return k
    raise RuntimeError(f"unbalanced at {start}")


def patch_entry_inner(inner: str, stack: int) -> tuple[str, bool]:
    orig = inner
    if re.search(r"stack_min\s*=", inner):
        inner = re.sub(r"stack_min\s*=\s*\d+", f"stack_min = {stack}", inner)
    else:
        inner = re.sub(
            r'(item\s*=\s*"[^"]+")',
            rf"\1, stack_min = {stack}, stack_max = {stack}",
            inner,
            count=1,
        )
        return inner, inner != orig

    if re.search(r"stack_max\s*=", inner):
        inner = re.sub(r"stack_max\s*=\s*\d+", f"stack_max = {stack}", inner)
    else:
        inner = re.sub(
            r"(stack_min\s*=\s*\d+)",
            rf"\1, stack_max = {stack}",
            inner,
            count=1,
        )
    return inner, inner != orig


def main() -> None:
    text = UNITS.read_text(encoding="utf-8")
    starts = [m.start() for m in re.finditer(r"PlaceObj\('ModItemLootDef', \{", text)]
    stats = {k: 0 for k in ITEMS}
    stats["lootdefs"] = 0
    out = []
    last = 0

    for start in starts:
        end = block_end(text, start)
        block = text[start:end]
        out.append(text[last:start])
        if 'group = "Mercs"' in block:
            out.append(block)
            last = end
            continue

        touched = False
        new_block = block
        for item in ITEMS:
            if f'item = "{item}"' not in new_block:
                continue
            pattern = re.compile(
                rf"(PlaceObj\('LootEntryInventoryItem',\s*\{{)([^}}]*?item\s*=\s*\"{item}\"[^}}]*?)(\}})",
                re.S,
            )

            def repl(m: re.Match, _item=item) -> str:
                nonlocal touched
                head, inner, tail = m.group(1), m.group(2), m.group(3)
                patched, changed = patch_entry_inner(inner, STACK)
                if changed:
                    stats[_item] += 1
                    touched = True
                return head + patched + tail

            new_block = pattern.sub(repl, new_block)

        if touched:
            stats["lootdefs"] += 1
        out.append(new_block)
        last = end

    out.append(text[last:])
    new_text = "".join(out)
    if new_text == text:
        print("no changes")
    else:
        nl = "\r\n" if "\r\n" in text else "\n"
        UNITS.write_text(new_text.replace("\r\n", "\n").replace("\n", nl), encoding="utf-8")
        print("wrote", UNITS)
    print(stats)


if __name__ == "__main__":
    main()
