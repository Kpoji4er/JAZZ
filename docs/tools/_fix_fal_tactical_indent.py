"""JAZZ-WEAPON-FAL-FAMILY-001: restore the indentation of the tactical FAL block.

The item was inserted with its PlaceObj header at column zero while the body
and closing brace kept the surrounding tab depth. check-generated-sync.ps1
matches a ModItem by requiring the opening and closing braces to share an
indent, so the block was invisible to the audit even though it parses fine.
"""
import os
import re
import sys
from pathlib import Path

ITEMS = Path('items.lua')
TARGET = 'JAZZ_FNFAL_Tactical'
HEAD = "PlaceObj('ModItemInventoryItemCompositeDef', {"


def main():
    text = ITEMS.read_bytes().decode('utf-8')
    lines = re.split(r'(?<=\n)', text)

    idx = next((i for i, l in enumerate(lines)
                if re.match(r"^\s*'Id', \"%s\",\s*$" % TARGET, l)), None)
    if idx is None:
        sys.exit('item not found: %s' % TARGET)
    head = next(i for i in range(idx, -1, -1) if HEAD in lines[i])

    # the body is already at the right depth; borrow it from the Id line
    want = re.match(r'^[\t ]*', lines[idx]).group(0)[:-1]
    have = re.match(r'^[\t ]*', lines[head]).group(0)
    if have == want:
        print('indent already correct (%d chars)' % len(want))
        return
    lines[head] = want + lines[head].lstrip()
    tmp = ITEMS.with_suffix('.lua.tmp')
    tmp.write_bytes(''.join(lines).encode('utf-8'))
    os.replace(tmp, ITEMS)
    print('line %d: indent %d -> %d chars' % (head + 1, len(have), len(want)))


if __name__ == '__main__':
    main()
