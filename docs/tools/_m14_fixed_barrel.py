"""Stage fixed standard barrels for the four imported M14 items.
Usage: python docs/tools/_m14_fixed_barrel.py --output DIR [--apply]
Preserves the technical normal barrel visual, removes length choices from UI.
"""
import argparse, hashlib, json, re, shutil, subprocess
from pathlib import Path
from _integrate_m14_family import find_item_block, matching

p = argparse.ArgumentParser()
p.add_argument('--output', type=Path, required=True)
p.add_argument('--apply', action='store_true')
a = p.parse_args()
root = Path(__file__).resolve().parents[2]
a.output.mkdir(parents=True, exist_ok=True)
source = root / 'items.lua'
items = source.read_text(encoding='utf-8')
hashes = {'items.lua': hashlib.sha256(source.read_bytes()).hexdigest()}

def lock(text):
    at = text.index("'SlotType', \"Barrel\"")
    start = text.rfind("PlaceObj('WeaponComponentSlot'", 0, at)
    end = matching(text, text.index('(', start))
    old = text[start:end]
    assert 'JAZZ_BarrelNormal' in old
    new = """PlaceObj('WeaponComponentSlot', {
            'SlotType', "Barrel",
            'Modifiable', false,
            'AvailableComponents', { "JAZZ_BarrelNormal" },
            'DefaultComponent', "JAZZ_BarrelNormal",
        })"""
    return text[:start] + new + text[end:]

for wid in ('M14SAW', 'M21', 'MK14EBR', 'JAZZ_M14_MkIII'):
    start, end = find_item_block(items, wid)
    items = items[:start] + lock(items[start:end]) + items[end:]
    rel = 'InventoryItem/' + wid + '.lua'
    path = root / rel
    hashes[rel] = hashlib.sha256(path.read_bytes()).hexdigest()
    out = a.output / rel; out.parent.mkdir(exist_ok=True)
    out.write_text(lock(path.read_text(encoding='utf-8')), encoding='utf-8')
(a.output / 'items.lua').write_text(items, encoding='utf-8')
(a.output / 'source-hashes.json').write_text(json.dumps(hashes, indent=2))
print('STAGED fixed normal barrel: M14SAW, M21, MK14EBR, JAZZ_M14_MkIII')
if a.apply:
    check=subprocess.run(['powershell','-NoProfile','-Command',
        'Get-Process JA3,JA3Debug,Ged -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Id'],capture_output=True,text=True)
    assert not check.stdout.strip(), 'Close game and editor before applying'
    backup=a.output/'backup'; backup.mkdir(exist_ok=True)
    for rel, digest in hashes.items():
        dest=root/rel
        assert hashlib.sha256(dest.read_bytes()).hexdigest()==digest, 'Source changed: '+rel
    for rel in hashes:
        dest=root/rel; old=backup/rel; old.parent.mkdir(parents=True,exist_ok=True)
        assert not old.exists(), 'Backup already exists; inspect before another apply'
        shutil.copy2(dest,old); shutil.copy2(a.output/rel,dest)
    print('APPLIED items and four companions; metadata registration unchanged')
