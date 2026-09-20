"""JAZZ-WEAPON-FAL-FAMILY-001: seat the classic FAL frame stock.

The unfolded Para archive mesh never sat on Weapon_FNFAL's Stock spot, so the
unfolded visual goes back to vanilla WeaponAttA_StockFNFal_01 (the skeleton
already in the inspect screenshots). Default stock becomes the fold pair so
that skeleton is what actually folds.

Only the FNFAL Stock slot default and the ApplyTo=FNFAL / JAZZ_FNFAL_Tactical
unfolded Entity lines are touched.
"""
import os
import re
from pathlib import Path

ITEMS = Path('items.lua')
COMPANION = Path('InventoryItem/FNFAL.lua')
VANILLA = 'WeaponAttA_StockFNFal_01'
OLD = 'FNFAL_ParaStk_unfld'


def swap_entity(text):
    # only the unfolded Para entity, both ApplyTo targets
    return text.replace('Entity = "%s"' % OLD, 'Entity = "%s"' % VANILLA)


def set_default(text):
    # FNFAL companion / items block: Stock slot default Normal -> UnFolded
    return text.replace(
        "'DefaultComponent', \"JAZZ_StockNormal\",\n\t\t}),\n\t\tPlaceObj('WeaponComponentSlot', {\n\t\t\t'SlotType', \"Under\"",
        "'DefaultComponent', \"JAZZ_StockLightUnFolded\",\n\t\t}),\n\t\tPlaceObj('WeaponComponentSlot', {\n\t\t\t'SlotType', \"Under\"",
    )


def main():
    items = ITEMS.read_bytes().decode('utf-8')
    n_ent = items.count('Entity = "%s"' % OLD)
    items2 = swap_entity(items)
    # default only inside the FNFAL item, not tactical (tactical has no fold pair)
    pat = re.compile(
        r"('AvailableComponents', \{\s*"
        r'"JAZZ_StockNormal",\s*'
        r'"JAZZ_StockLightUnFolded",\s*'
        r'"JAZZ_StockLightFolded",\s*'
        r'\},\s*'
        r"'DefaultComponent', )\"JAZZ_StockNormal\"",
        re.S)
    items2, n_def = pat.subn(r'\1"JAZZ_StockLightUnFolded"', items2, count=1)
    if n_ent < 1:
        raise SystemExit('no unfolded Para entity lines in items.lua')
    if n_def != 1:
        raise SystemExit('FNFAL stock default not unique: %d' % n_def)
    tmp = ITEMS.with_suffix('.lua.tmp')
    tmp.write_bytes(items2.encode('utf-8'))
    os.replace(tmp, ITEMS)
    print('items.lua entity swaps=%d default=%d' % (n_ent, n_def))

    comp = COMPANION.read_text(encoding='utf-8')
    if "'DefaultComponent', \"JAZZ_StockNormal\"" not in comp:
        # companion uses different quote style
        pass
    comp2 = comp.replace(
        "'DefaultComponent', \"JAZZ_StockNormal\",\n\t\t}),\n\t\tPlaceObj('WeaponComponentSlot', {\n\t\t\t'SlotType', \"Under\"",
        "'DefaultComponent', \"JAZZ_StockLightUnFolded\",\n\t\t}),\n\t\tPlaceObj('WeaponComponentSlot', {\n\t\t\t'SlotType', \"Under\"",
    )
    if comp2 == comp:
        raise SystemExit('companion default not found')
    COMPANION.write_text(comp2, encoding='utf-8', newline='\n')
    print('companion default -> JAZZ_StockLightUnFolded')


if __name__ == '__main__':
    main()
