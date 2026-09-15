"""Restore AK74/AKM visuals from the pre-import backup, preserving other work.

Usage: python docs/tools/_restore_legacy_ak_visuals.py --build <AK build>
Does not reload or save the running editor. Reload from disk before editor save.
"""
import argparse
import re
from pathlib import Path
from lupa import LuaRuntime
from _integrate_sr3m import ROOT, matching

p = argparse.ArgumentParser()
p.add_argument('--build', type=Path, required=True)
a = p.parse_args()
backup = a.build / 'integration-backup/jazz'
current = (ROOT / 'items.lua').read_text(encoding='utf-8-sig')
old = (backup / 'items.lua').read_text(encoding='utf-8-sig')

def blocks(text, kind):
    for m in re.finditer(r"PlaceObj\('" + kind + "'", text):
        end = matching(text, text.index('(', m.start()))
        yield m.start(), end, text[m.start():end]

def ident(block):
    return re.search(r"(?:'Id',\s*|\bid\s*=\s*)\"([^\"]+)\"", block)[1]

def slot(text):
    return next(b for _, _, b in blocks(text, 'WeaponComponentSlot') if re.search(r"'SlotType',\s*\"Muzzle\"", b))

changes = {}
for weapon in ('AK74', 'AKM'):
    path = ROOT / f'InventoryItem/{weapon}.lua'
    text = path.read_text(encoding='utf-8-sig')
    prior = (backup / path.relative_to(ROOT)).read_text(encoding='utf-8-sig')
    text = text.replace(f'Entity = "AKR_{weapon}"', f'Entity = "{weapon}"')
    text = text.replace(slot(text), slot(prior))
    changes[path] = text
    begin, end, block = next(x for x in blocks(current, 'ModItemInventoryItemCompositeDef') if ident(x[2]) == weapon)
    original = next(b for _, _, b in blocks(old, 'ModItemInventoryItemCompositeDef') if ident(b) == weapon)
    block = block.replace(f"'Entity', \"AKR_{weapon}\"", f"'Entity', \"{weapon}\"")
    block = block.replace(slot(block), slot(original))
    current = current[:begin] + block + current[end:]

old_components = {ident(b): b for _, _, b in blocks(old, 'ModItemWeaponComponent')}
count = 0
for begin, end, block in reversed(list(blocks(current, 'ModItemWeaponComponent'))):
    original = old_components.get(ident(block))
    if not original:
        continue
    for vs, ve, visual in reversed(list(blocks(block, 'WeaponComponentVisual'))):
        m = re.search(r'ApplyTo\s*=\s*"(AK74|AKM)"', visual)
        if not m or 'AKR_' not in visual:
            continue
        weapon = m[1]
        visual_slot = re.search(r'Slot\s*=\s*"([^"]+)"', visual)[1]
        donors = [v for _, _, v in blocks(original, 'WeaponComponentVisual') if re.search(r'ApplyTo\s*=\s*"'+weapon+'"', v) and re.search(r'Slot\s*=\s*"'+visual_slot+'"', v)]
        assert len(donors) <= 1
        replacement = donors[0] if donors else ''
        if not donors:
            comma = re.match(r'\s*,', block[ve:])
            if comma:
                ve += comma.end()
        block = block[:vs] + replacement + block[ve:]
        count += 1
    current = current[:begin] + block + current[end:]
changes[ROOT / 'items.lua'] = current
payloads = {}
for path, text in changes.items():
    LuaRuntime().compile(text)
    payloads[path] = text.replace('\r\n', '\n').replace('\n', '\r\n').encode('utf-8')
for weapon in ('AK74', 'AKM'):
    path = ROOT / f'WeaponIcons/{weapon}.png'
    payloads[path] = (backup / path.relative_to(ROOT)).read_bytes()
before = {path: path.read_bytes() for path in payloads}
import hashlib
for path, raw in before.items():
    dest = a.build / 'visual-rollback-backup' / path.relative_to(ROOT)
    dest = dest.with_name(dest.name + '.' + hashlib.sha256(raw).hexdigest()[:12])
    dest.parent.mkdir(parents=True, exist_ok=True)
    if not dest.exists():
        dest.write_bytes(raw)
for path, raw in payloads.items():
    assert path.read_bytes() == before[path], f'Concurrent edit: {path}'
    path.write_bytes(raw)
print(f'Restored AK74/AKM bodies, muzzle slots, icons and {count} module visuals; new AKs preserved.')
