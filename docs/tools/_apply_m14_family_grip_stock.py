"""JAZZ-WEAPON-M14-FAMILY-001: wood grip + no vanilla Heavy/Plastic on M14/M21.

Sets ModifyRightHandGrip on M14SAW and M21. Remaps StockHeavy/StockLight
visuals for those IDs from WeaponAttA_StockM14_Heavy / _Plastic to
WeaponAttA_StockM14_Standard so the rifles keep a USGI wood stock until
JAZZ_M14 replaces the host.

  python docs/tools/_apply_m14_family_grip_stock.py [--apply]
"""
import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ITEMS = ROOT / 'items.lua'
COMPANIONS = [
    ROOT / 'InventoryItem' / 'M14SAW.lua',
    ROOT / 'InventoryItem' / 'M21.lua',
]
WEAPONS = ('M14SAW', 'M21')
BAD = ('WeaponAttA_StockM14_Heavy', 'WeaponAttA_StockM14_Plastic')
GOOD = 'WeaponAttA_StockM14_Standard'


def add_grip_items(text):
    for wid in WEAPONS:
        marker = '\'Id\', "%s",' % wid
        at = text.find(marker)
        if at < 0:
            raise SystemExit('missing %s in items.lua' % wid)
        hol = text.find('\'HolsterSlot\', "Shoulder",', at)
        nxt = text.find('\'AvailableAttacks\'', hol)
        chunk = text[hol:nxt]
        if 'ModifyRightHandGrip' in chunk:
            continue
        text = text[:hol] + '\'HolsterSlot\', "Shoulder",\n\t\t\t\t\t\'ModifyRightHandGrip\', true,' + text[hol + len('\'HolsterSlot\', "Shoulder",'):]
    return text


def add_grip_companion(text):
    if 'ModifyRightHandGrip' in text:
        return text
    return text.replace(
        '\tHolsterSlot = "Shoulder",\n',
        '\tHolsterSlot = "Shoulder",\n\tModifyRightHandGrip = true,\n',
        1,
    )


def remap_stock_visuals(text):
    pattern = re.compile(
        r"(PlaceObj\('WeaponComponentVisual',\s*\{(?:[^{}]|\{[^{}]*\})*?ApplyTo = \"(M14SAW|M21)\","
        r"(?:[^{}]|\{[^{}]*\})*?Entity = \")(WeaponAttA_StockM14_Heavy|WeaponAttA_StockM14_Plastic)(\")",
        re.S,
    )
    return pattern.sub(lambda m: m.group(1) + GOOD + m.group(4), text)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--apply', action='store_true')
    args = ap.parse_args()
    items = ITEMS.read_text(encoding='utf-8')
    new_items = remap_stock_visuals(add_grip_items(items))
    comps = []
    for path in COMPANIONS:
        comps.append((path, add_grip_companion(path.read_text(encoding='utf-8'))))
    print('items.lua delta', len(new_items) - len(items))
    print('heavy left', new_items.count('ApplyTo = "M14SAW",\n\t\t\t\t\t\t\t\tEntity = "WeaponAttA_StockM14_Heavy"'))
    print('plastic left', new_items.count('WeaponAttA_StockM14_Plastic'))
    if not args.apply:
        print('dry-run')
        return
    ITEMS.write_text(new_items, encoding='utf-8', newline='\n')
    for path, body in comps:
        path.write_text(body, encoding='utf-8', newline='\n')
        print('wrote', path.name)


if __name__ == '__main__':
    main()
