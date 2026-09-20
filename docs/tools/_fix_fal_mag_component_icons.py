"""JAZZ-WEAPON-FAL-FAMILY-001: point the FAL magazine components at FAL art.

The loose magazine items were already corrected, but the matching
ModItemWeaponComponent entries still showed Galil and M16 magazines in the
weapon modification list. Both are retargeted at the vanilla FAL magazine
icons, so the slot list and the inventory item now show the same picture.

Only the component-level Icon inside the named block is touched; the identical
strings used by unrelated Galil and M16 components are left alone. The script
states the value it wants rather than the value it expects, so it is safe to
re-run.
"""
import os
import re
import sys
from pathlib import Path

ITEMS = Path('items.lua')
HEAD = "PlaceObj('ModItemWeaponComponent', {"
WANT = {
    'JAZZ_MagLarge_20_30_FAL': 'UI/Icons/Upgrades/fnfal_mag_ergo_large',
    'JAZZ_MagNormalFine_FAL': 'UI/Icons/Upgrades/fnfal_mag_ergo_normal',
}


def main():
    # byte level round trip: items.lua is CRLF and must stay CRLF
    text = ITEMS.read_bytes().decode('utf-8')
    lines = re.split(r'(?<=\n)', text)
    changed = 0

    for target, want in WANT.items():
        end = next((i for i, l in enumerate(lines)
                    if re.match(r'^\s*id = "%s",\s*$' % target, l)), None)
        if end is None:
            sys.exit('block not found: %s' % target)
        start = next(i for i in range(end, -1, -1) if HEAD in lines[i])

        # the component's own fields are the shallowest Icon lines in the block;
        # anything deeper belongs to a nested WeaponComponentVisual
        icons = [i for i in range(start, end) if re.match(r'^\s+Icon = "', lines[i])]
        if not icons:
            sys.exit('no Icon line in %s' % target)
        depth = min(len(l) - len(l.lstrip()) for l in (lines[i] for i in icons))
        own = [i for i in icons if len(lines[i]) - len(lines[i].lstrip()) == depth]
        if len(own) != 1:
            sys.exit('%s: expected one component-level Icon, got %d' % (target, len(own)))

        i = own[0]
        have = re.search(r'Icon = "([^"]*)"', lines[i]).group(1)
        if have == want:
            print('%-26s already %s' % (target, want))
            continue
        lines[i] = lines[i].replace('"%s"' % have, '"%s"' % want)
        changed += 1
        print('%-26s %s -> %s' % (target, have, want))

    if changed:
        tmp = ITEMS.with_suffix('.lua.tmp')
        tmp.write_bytes(''.join(lines).encode('utf-8'))
        os.replace(tmp, ITEMS)
    print('CHANGED=%d' % changed)


if __name__ == '__main__':
    main()
