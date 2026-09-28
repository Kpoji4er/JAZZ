"""Apply/check only Mosin entries in Legion pools; preserve unrelated dirty data.

Default is dry-run, --apply writes existing LootDef only. No new IDs, companions
or metadata resources. --check fails if installed tables differ from the plan.
"""
import argparse
from collections import Counter
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'scripts/legion-loadouts'))
import generate as g
from run_static_tests import placeobj_blocks


def entries(block):
    return placeobj_blocks(block, 'LootEntryLootDef')


def mosin(entry):
    return 'loot_def = "JAZZ_GenW_Mosin_' in entry


def patch(text):
    weapons = g.load_weapons(g.load_json('weapon_tag_overrides.json'))
    comps = g.load_components()
    variants = g.expand_early_variants(g.load_json('early_variants.json'), weapons, comps)
    recipes = g.load_json('recipes.json')
    pools = {r['firearm']: r for r in recipes.values()}
    pools.update({r['cqb_secondary']['firearm']: g.recipe_for_cqb(r)
                  for r in recipes.values() if r.get('cqb_secondary')})
    changes = []
    for fid, recipe in pools.items():
        plan, combos = g.collect_firearm_plan(recipe, weapons, g.load_json('packages.json'), comps,
                                              g.load_json('caliber_ammo.json'), variants)
        canonical = entries(g.emit_firearm_from_plan(fid, plan))
        wanted = [e for e in canonical if mosin(e)]
        found = g.find_moditem_block(text, fid)
        if not found:
            # Existing baseline: recipe declares this pool but it is absent on
            # disk. Do not introduce a new unrelated CQB pool in a Mosin retier.
            assert fid == 'Ranger_CQB', f'Unexpected missing pool: {fid}'
            continue
        start, end = found
        original = text[start:end]
        existing = [e for e in entries(original) if mosin(e)]
        if existing == wanted:
            continue
        updated = original
        for entry in existing:
            # Remove the complete nested PlaceObj line range, including its
            # closing parenthesis/comma, without touching neighbouring entries.
            s = updated.index(entry)
            line = updated.rfind('\n', 0, s) + 1
            assert not updated[line:s].strip()
            e = s + len(entry)
            assert updated[e:e + 2] == '),'
            e += 2
            if updated[e:e + 1] == '\n':
                e += 1
            updated = updated[:line] + updated[e:]
        additions = list(wanted)
        fallback = []
        if any('unconditional fallback' in e for e in existing) and 'unconditional fallback' not in updated:
            fallback = [e for e in canonical if 'unconditional fallback' in e]
            assert len(fallback) == 1 and not mosin(fallback[0])
            additions += fallback
        tail = updated.rfind('\n')
        updated = updated[:tail] + ''.join('\n\t\t\t\t\t\t' + e + '),' for e in additions) + updated[tail:]
        # Strong scope guard: preserve every non-Mosin entry (only replace a
        # removed Mosin fallback with the generator's non-Mosin fallback).
        assert Counter(e for e in entries(updated) if not mosin(e)) == Counter(e for e in entries(original) if not mosin(e)) + Counter(fallback)
        for entry in wanted:
            cid = re.search(r'loot_def = "([^"]+)"', entry)[1]
            assert g.find_moditem_block(text, cid), f'Missing existing combo {cid}'
        text = text[:start] + updated + text[end:]
        changes.append(fid)
    for fid, ref in [('LegionT1_RifleBolt', 'RiflesBolt_Mosin'), ('LegionT1_RifleSniper', 'RiflesBolt_MosinScope')]:
        start, end = g.find_moditem_block(text, fid)
        block = text[start:end]
        candidates = [e for e in entries(block) if f'loot_def = "{ref}"' in e]
        assert len(candidates) == 1
        old = candidates[0]
        new, n = re.subn(r'Amount = \d+', 'Amount = 13', old)
        assert n == 1
        new = re.sub(r'comment = "T1(?:-\d)?"', 'comment = "T1-3"', new)
        if old != new:
            text = text[:start] + block.replace(old, new) + text[end:]
            changes.append(fid)
    return text, changes


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--apply', action='store_true')
    p.add_argument('--check', action='store_true')
    p.add_argument('--backup', type=Path, default=ROOT / 'tmp/mosin-loot-items-before.lua')
    args = p.parse_args()
    raw = g.ITEMS.read_bytes()
    original = raw.decode('utf-8').replace('\r\n', '\n')
    updated, changes = patch(original)
    again, repeats = patch(updated)
    assert again == updated and not repeats, 'Patch must be idempotent'
    print(f'{len(changes)} Mosin pool changes: ' + ', '.join(changes))
    if args.check:
        assert not changes, 'Installed Mosin loot differs from source plan'
        print('PASS: installed Mosin entries equal generated role/gate/weight plan; legacy gates=13')
    if args.apply and changes:
        backup = args.backup
        assert not backup.exists(), 'Preserve existing backup; inspect before a second transaction'
        backup.write_bytes(raw)
        assert g.ITEMS.read_bytes() == raw, 'Concurrent items.lua edit'
        newline = '\r\n' if b'\r\n' in raw else '\n'
        g.ITEMS.write_bytes(updated.replace('\n', newline).encode('utf-8'))
        print('Installed; metadata IDs and companion graph unchanged.')


if __name__ == '__main__':
    main()
