"""JAZZ-WEAPON-FAL-FAMILY-001: retune the classic FNFAL and fix FAL magazine icons.

Edits items.lua and the matching companions as one transaction:

  * FNFAL moves to Bobby Ray tier 2 and loses reliability (REQ-001)
  * its Stock slot gains the folding Para pair and drops JAZZ_StockLight (REQ-002)
  * JAZZ_StockLightFolded / _UnFolded stop pointing both FNFAL visuals at the
    same vanilla entity and use the new FNFAL_ParaStk_* pair (REQ-003)
  * the two removable FAL magazines stop borrowing Galil and M16 icons (REQ-006)

  python docs/tools/_apply_fal_family.py [--apply]

Dry-run by default. Run with the game and Mod Editor closed.
"""
import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

FNFAL_FIELDS = [
    ("'Reliability', 65,", "'Reliability', 55,"),
    ("'Cost', 7250,", "'Cost', 6300,"),
    ("'Tier', 3,", "'Tier', 2,"),
    ("'BaseJamChance', -10,", "'BaseJamChance', 0,"),
]
FNFAL_COMPANION_FIELDS = [
    ("Reliability = 65,", "Reliability = 55,"),
    ("Cost = 7250,", "Cost = 6300,"),
    ("Tier = 3,", "Tier = 2,"),
    ("BaseJamChance = -10,", "BaseJamChance = 0,"),
]
STOCK_SLOT_OLD = """\t\t\t\t\t\t\t\t"JAZZ_StockNormal",
\t\t\t\t\t\t\t\t"JAZZ_StockHeavy",
\t\t\t\t\t\t\t\t"JAZZ_StockLight",
"""
STOCK_SLOT_NEW = """\t\t\t\t\t\t\t\t"JAZZ_StockNormal",
\t\t\t\t\t\t\t\t"JAZZ_StockLightUnFolded",
\t\t\t\t\t\t\t\t"JAZZ_StockLightFolded",
"""
STOCK_SLOT_COMPANION_OLD = """\t\t\t\t"JAZZ_StockNormal",
\t\t\t\t"JAZZ_StockHeavy",
\t\t\t\t"JAZZ_StockLight",
"""
STOCK_SLOT_COMPANION_NEW = """\t\t\t\t"JAZZ_StockNormal",
\t\t\t\t"JAZZ_StockLightUnFolded",
\t\t\t\t"JAZZ_StockLightFolded",
"""
MAG_ICONS = {
    'JAZZ_MagLarge_20_30_FAL': ('UI/Icons/Upgrades/galil_magazine_large',
                                'UI/Icons/Upgrades/fnfal_mag_ergo_large'),
    'JAZZ_MagNormalFine_FAL': ('UI/Icons/Upgrades/m16_magazine',
                               'UI/Icons/Upgrades/fnfal_mag_ergo_normal'),
}
STOCK_VISUALS = {
    'JAZZ_StockLightUnFolded': 'FNFAL_ParaStk_unfld',
    'JAZZ_StockLightFolded': 'FNFAL_ParaStk_fld',
}

changes = []


def block_bounds(text, head, terminator):
    start = text.find(head)
    if start < 0:
        raise SystemExit('anchor not found: %s' % head)
    end = text.find(terminator, start + len(head))
    return start, (end if end > 0 else len(text))


def patch_span(text, start, end, old, new, label, expect=1):
    span = text[start:end]
    hits = span.count(old)
    if hits == 0 and new in span:
        changes.append((label, 'already applied'))
        return text
    if hits != expect:
        raise SystemExit('%s: expected %d occurrence(s) of %r, found %d' % (label, expect, old, hits))
    changes.append((label, '%d replacement(s)' % hits))
    return text[:start] + span.replace(old, new, expect) + text[end:]


def patch_items(text):
    # classic FNFAL weapon block
    start, end = block_bounds(text, '\'Id\', "FNFAL",', '\'Id\', "')
    for old, new in FNFAL_FIELDS:
        text = patch_span(text, start, end, old, new, 'items/FNFAL %s' % old.strip(', '))
    start, end = block_bounds(text, '\'Id\', "FNFAL",', '\'Id\', "')
    text = patch_span(text, start, end, STOCK_SLOT_OLD, STOCK_SLOT_NEW, 'items/FNFAL Stock slot')

    # folding stock visuals: both currently reuse WeaponAttA_StockFNFal_01
    for comp, entity in STOCK_VISUALS.items():
        start, end = block_bounds(text, 'id = "%s",' % comp, 'id = "%s",' % comp)
        head = text.rfind('PlaceObj(\'ModItemWeaponComponent\', {', 0, start)
        old = ('ApplyTo = "FNFAL",\n\t\t\t\t\t\t\t\tEntity = "WeaponAttA_StockFNFal_01",')
        new = ('ApplyTo = "FNFAL",\n\t\t\t\t\t\t\t\tEntity = "%s",' % entity)
        text = patch_span(text, head, start, old, new, 'items/%s visual' % comp)

    # removable magazine icons
    for item, (old_icon, new_icon) in MAG_ICONS.items():
        start, end = block_bounds(text, '\'Id\', "%s",' % item, '\'Id\', "')
        text = patch_span(text, start, end, '\'Icon\', "%s",' % old_icon,
                          '\'Icon\', "%s",' % new_icon, 'items/%s icon' % item)
    return text


def patch_companions(apply):
    targets = {
        'InventoryItem/FNFAL.lua': FNFAL_COMPANION_FIELDS + [
            (STOCK_SLOT_COMPANION_OLD, STOCK_SLOT_COMPANION_NEW)],
        'InventoryItem/JAZZ_MagLarge_20_30_FAL.lua': [
            ('Icon = "UI/Icons/Upgrades/galil_magazine_large",',
             'Icon = "UI/Icons/Upgrades/fnfal_mag_ergo_large",')],
        'InventoryItem/JAZZ_MagNormalFine_FAL.lua': [
            ('Icon = "UI/Icons/Upgrades/m16_magazine",',
             'Icon = "UI/Icons/Upgrades/fnfal_mag_ergo_normal",')],
    }
    for rel, pairs in targets.items():
        path = ROOT / rel
        text = path.read_text(encoding='utf-8')
        for old, new in pairs:
            label = '%s %s' % (rel, old.splitlines()[0].strip())
            if old not in text:
                changes.append((label, 'already applied' if new in text else 'MISSING'))
                if new not in text:
                    raise SystemExit('%s: pattern not found' % label)
                continue
            text = text.replace(old, new, 1)
            changes.append((label, '1 replacement'))
        if apply:
            path.write_text(text, encoding='utf-8')


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--apply', action='store_true')
    a = p.parse_args()

    items = ROOT / 'items.lua'
    text = items.read_text(encoding='utf-8')
    patched = patch_items(text)
    patch_companions(a.apply)
    if a.apply and patched != text:
        items.write_text(patched, encoding='utf-8')

    width = max(len(c[0]) for c in changes)
    for label, note in changes:
        print('  %-*s  %s' % (width, label, note))
    print('APPLIED' if a.apply else 'DRY RUN - nothing written')


if __name__ == '__main__':
    sys.exit(main())
