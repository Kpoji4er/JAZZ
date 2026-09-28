"""JAZZ-WEAPON-SR3M-001: open the SR3M Scope, Side and Muzzle slots in one transaction.

python docs/tools/_apply_sr3m_slots.py --backup <folder> [--apply]

Rewrites `ComponentSlots` in both representations at once - the `SR3M` ModItem inside
items.lua and the generated companion InventoryItem/SR3M.lua - because either one alone
does not survive the next editor save.

No `WeaponComponentVisual ApplyTo="SR3M"` is written. Every listed optic and side device
already carries a default visual aimed at the `Scope` / `Side` spot, which is how the
other Picatinny hosts such as M4A1 work; an override here would only duplicate it.
`JAZZ_IronSight` is deliberately absent: it has no default visual and the SR3M carries
its own irons on the mesh, so the slot defaults to empty instead.
Dry-run by default. Requires the game and Mod Editor closed.
"""
import argparse
import hashlib
import re
import shutil
from pathlib import Path

from _integrate_sr3m import ROOT, matching, write

# Verified on the built rail: every entry seats on the receiver Picatinny with at most a
# small rearward overhang. Aimpoint5000, NightScope and Scope_Scout are excluded - the
# first buries its integral mount 14 mm into the cover, the others overhang 4-6 cm.
SCOPE = ['JAZZ_Reflex_Closed', 'JAZZ_Reflex_Eotech', 'JAZZ_Reflex_M68',
         'JAZZ_CombatScope_2x', 'JAZZ_CombatScope_ACOG']
# Dovetail-only optics stay out: the SR3M has no side mount of any kind.
FORBIDDEN = ['JAZZ_Scope_PSO', 'JAZZ_CombatScope_1P29', 'JAZZ_NightScope_NSPU',
             'JAZZ_Reflex_Cobra', 'JAZZ_Reflex_PKAS', 'AKSeriaMount']
SIDE = ['JAZZ_Flashlight', 'JAZZ_FlashlightOff', 'JAZZ_FlashlightDot',
        'JAZZ_LaserDot', 'JAZZ_UVDot']


def slot(indent, slot_type, components, default=None, can_be_empty=False, modifiable=True):
    lines = [f"{indent}PlaceObj('WeaponComponentSlot', {{",
             f'{indent}\t\'SlotType\', "{slot_type}",']
    if can_be_empty:
        lines.append(f"{indent}\t'CanBeEmpty', true,")
    if not modifiable:
        lines.append(f"{indent}\t'Modifiable', false,")
    lines.append(f"{indent}\t'AvailableComponents', {{")
    lines += [f'{indent}\t\t"{c}",' for c in components]
    lines.append(f'{indent}\t}},')
    if default:
        lines.append(f'{indent}\t\'DefaultComponent\', "{default}",')
    lines.append(f'{indent}}}),')
    return '\n'.join(lines) + '\n'


def slots_block(indent):
    """Scope first, as on M4A1; Side before Stock; Muzzle no longer locked."""
    body = slot(indent, 'Scope', SCOPE, can_be_empty=True)
    body += slot(indent, 'Magazine', ['JAZZ_MagNormal'], 'JAZZ_MagNormal', modifiable=False)
    body += slot(indent, 'Handguard', ['JAZZ_Handguard'], 'JAZZ_Handguard', modifiable=False)
    body += slot(indent, 'Muzzle', ['JAZZ_DefMuzzle'], 'JAZZ_DefMuzzle')
    body += slot(indent, 'Side', SIDE, can_be_empty=True)
    body += slot(indent, 'Stock', ['JAZZ_StockLightFolded', 'JAZZ_StockLightUnFolded'],
                 'JAZZ_StockLightUnFolded', modifiable=False)
    return body


def replace_slots(text, start, key, indent, closing):
    at = text.index(key, start)
    open_brace = text.index('{', at)
    end = matching(text, open_brace, '{', '}')
    return text[:open_brace] + '{\n' + slots_block(indent) + closing + text[end:]


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--backup', type=Path, required=True)
    p.add_argument('--apply', action='store_true')
    args = p.parse_args()

    items_path = ROOT / 'items.lua'
    companion_path = ROOT / 'InventoryItem/SR3M.lua'
    items = items_path.read_text(encoding='utf-8')
    companion = companion_path.read_text(encoding='utf-8')

    for ident in SCOPE + SIDE + ['JAZZ_DefMuzzle']:
        assert re.search(r'\bid\s*=\s*"' + ident + '"', items), 'Missing component: ' + ident
    assert "'Id', \"SR3M\"" in items

    where = items.index('\'Id\', "SR3M"')
    start = items.rfind("PlaceObj('ModItemInventoryItemCompositeDef'", 0, where)
    new_items = replace_slots(items, start, "'ComponentSlots'", '\t' * 6, '\t' * 5 + '}')
    new_companion = replace_slots(companion, 0, 'ComponentSlots =', '\t' * 2, '\t}')

    for name, text in (('items.lua', new_items), ('InventoryItem/SR3M.lua', new_companion)):
        for ident in FORBIDDEN:
            block = text[text.index('SR3M'):]
            assert ident not in slots_block('\t'), (name, 'dovetail optic leaked', ident)
        assert '"Scope"' in text and '"Side"' in text

    print('Scope :', ', '.join(SCOPE), '(CanBeEmpty, no default -> native irons stay)')
    print('Side  :', ', '.join(SIDE), '(CanBeEmpty)')
    print('Muzzle: JAZZ_DefMuzzle default, Modifiable no longer false')
    print('Visuals: none added; components use their existing default Scope/Side visuals')
    if not args.apply:
        print('\nDry run. Re-run with --apply, game and Mod Editor closed.')
        return

    args.backup.mkdir(parents=True, exist_ok=True)
    for path, text in ((items_path, new_items), (companion_path, new_companion)):
        stamp = args.backup / f'{path.name}.{hashlib.sha256(path.read_bytes()).hexdigest()[:12]}'
        if not stamp.exists():
            shutil.copy2(path, stamp)
        write(path, text)
        print('wrote', path.relative_to(ROOT))
    print('\nDone. Reload the mod from disk and check the editor message panel.')


if __name__ == '__main__':
    main()
