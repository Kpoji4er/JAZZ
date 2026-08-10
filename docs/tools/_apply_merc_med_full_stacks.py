# -*- coding: utf-8 -*-
"""Merc starting kits: Bandage stack 10, kits to MaxStacks.

Only touches ModItemLootDef with group = \"Mercs\" in jazz-units/items.lua.
- JAZZ_Bandage -> stack_min/max = 10 (where present; does not add)
- FirstAidKit  -> stack_min/max = 5  (MaxStacks)
- Medkit       -> stack_min/max = 10 (MaxStacks)
- Reanimationsset -> stack_min/max = 15 (MaxStacks)

Idempotent. Leaves drop_chance / other fields intact.
"""
from __future__ import annotations

from pathlib import Path
import re

UNITS = Path(r"C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz-units\items.lua")

# item Id -> full stack size (MaxStacks in jazz InventoryItem)
FULL = {
    "JAZZ_Bandage": 10,  # intentional merc kit size (item MaxStacks=30)
    "FirstAidKit": 5,
    "Medkit": 10,
    "Reanimationsset": 15,
}


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
    raise RuntimeError(f"unbalanced ModItemLootDef at {start}")


def patch_entry_inner(inner: str, stack: int) -> tuple[str, bool]:
    """Rewrite stack_min/max inside a LootEntryInventoryItem body; return (new, changed)."""
    orig = inner
    if re.search(r"stack_min\s*=", inner):
        inner = re.sub(r"stack_min\s*=\s*\d+", f"stack_min = {stack}", inner)
    else:
        # insert after item = "..."
        inner = re.sub(
            r'(item\s*=\s*"[^"]+")',
            rf"\1, stack_min = {stack}, stack_max = {stack}",
            inner,
            count=1,
        )
        # if we already injected both, skip separate max
        if re.search(r"stack_max\s*=", orig):
            pass
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
    stats = {k: 0 for k in FULL}
    stats["lootdefs"] = 0
    out = []
    last = 0

    for start in starts:
        end = block_end(text, start)
        block = text[start:end]
        out.append(text[last:start])
        if 'group = "Mercs"' not in block:
            out.append(block)
            last = end
            continue

        stats["lootdefs"] += 1
        new_block = block

        for item, stack in FULL.items():
            # compact one-liner and multiline PlaceObj('LootEntryInventoryItem', { ... })
            pattern = re.compile(
                rf"(PlaceObj\('LootEntryInventoryItem',\s*\{{)([^}}]*?item\s*=\s*\"{item}\"[^}}]*?)(\}})",
                re.S,
            )

            def repl(m: re.Match, _stack=stack, _item=item) -> str:
                head, inner, tail = m.group(1), m.group(2), m.group(3)
                patched, changed = patch_entry_inner(inner, _stack)
                if changed:
                    stats[_item] += 1
                return head + patched + tail

            new_block = pattern.sub(repl, new_block)

        out.append(new_block)
        last = end

    out.append(text[last:])
    new_text = "".join(out)
    if new_text == text:
        print("no changes")
    else:
        # preserve CRLF if source used it (Windows Mod Editor files)
        nl = "\r\n" if "\r\n" in text else "\n"
        UNITS.write_text(new_text.replace("\r\n", "\n").replace("\n", nl), encoding="utf-8")
        print("wrote", UNITS)
    print(stats)


if __name__ == "__main__":
    main()
