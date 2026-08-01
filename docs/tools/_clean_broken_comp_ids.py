# -*- coding: utf-8 -*-
"""Safe cleanup of broken DefaultComponent 'su' and empty AvailableComponents entries."""
from pathlib import Path
import re
import sys
sys.path.insert(0, "docs/tools")
from _apply_attach_001 import matching_paren, prop, placeobj_blocks

ROOT = Path(".")


def clean_slot(block: str) -> tuple[str, int]:
    changed = 0
    # Remove DefaultComponent "su"
    new, n = re.subn(r"\n([ \t]*)'DefaultComponent',\s*\"su\",", "", block)
    changed += n
    # Remove AvailableComponents entries that are empty / only comma / contain newline
    def repl_list(m):
        nonlocal changed
        body = m.group(1)
        ids = re.findall(r'"([^"]*)"', body)
        keep = [i for i in ids if i and i.strip() not in {",", "su"} and "\n" not in i and "\t" not in i]
        if len(keep) != len(ids):
            changed += len(ids) - len(keep)
        if not keep:
            return m.group(0)  # leave empty list braces as-is structurally
        # rebuild with same indent style as first entry
        indent = "\n\t\t\t\t\t\t\t\t"
        inner = "".join(f'{indent}"{i}",' for i in keep) + "\n\t\t\t\t\t\t\t"
        return "'AvailableComponents', {" + inner + "}"

    new2 = re.sub(
        r"'AvailableComponents',\s*\{(.*?)\}",
        repl_list,
        new,
        flags=re.S,
    )
    return new2, changed


def clean_file(text: str) -> tuple[str, int]:
    total = 0
    for block in reversed(placeobj_blocks(text, "WeaponComponentSlot")):
        new, n = clean_slot(block.text)
        if n:
            text = text[:block.start] + new + text[block.end:]
            total += n
    return text, total


def main():
    items = Path("items.lua")
    t, n = clean_file(items.read_text(encoding="utf-8"))
    items.write_text(t, encoding="utf-8", newline="\n")
    print("items cleaned", n)
    cn = 0
    for p in Path("InventoryItem").glob("*.lua"):
        t0 = p.read_text(encoding="utf-8")
        t1, n = clean_file(t0)
        if n:
            p.write_text(t1, encoding="utf-8", newline="\n")
            cn += n
            print(" ", p.name, n)
    print("companions cleaned", cn)


if __name__ == "__main__":
    main()
