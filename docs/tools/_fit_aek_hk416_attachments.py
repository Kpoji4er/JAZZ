"""Stage/apply post-release attachment fit. --build DIR [--apply].

Updates existing class visual methods and five AEK mount visuals. No asset edits.
Requires closed game/editor, preserves source bytes, backs up and checks hashes.
"""
import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path

from _integrate_sr3m import ROOT
from _integrate_vz58 import component_block

p = argparse.ArgumentParser(description=__doc__)
p.add_argument('--build', type=Path, required=True)
p.add_argument('--apply', action='store_true')
a = p.parse_args()
a.build.mkdir(parents=True, exist_ok=True)
receipt = a.build / 'fit-install.json'
sha = lambda raw: hashlib.sha256(raw).hexdigest()

if a.apply:
    r = json.loads(receipt.read_text())
    assert not r['applied']
    running = subprocess.run(['powershell', '-NoProfile', '-Command',
        'Get-Process JA3,JA3Debug -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Id'],
        capture_output=True, text=True).stdout.strip()
    assert not running, 'Close game/editor before apply'
    for rel, hashes in r['files'].items():
        assert sha((ROOT / rel).read_bytes()) == hashes['before'], rel
        assert sha((a.build / 'stage' / rel).read_bytes()) == hashes['after'], rel
    for rel in r['files']:
        backup = a.build / 'backup' / rel
        assert not backup.exists()
        backup.parent.mkdir(parents=True, exist_ok=True)
        backup.write_bytes((ROOT / rel).read_bytes())
    try:
        for rel, hashes in r['files'].items():
            (ROOT / rel).write_bytes((a.build / 'stage' / rel).read_bytes())
            assert sha((ROOT / rel).read_bytes()) == hashes['after']
    except Exception:
        for rel in r['files']:
            (ROOT / rel).write_bytes((a.build / 'backup' / rel).read_bytes())
        raise
    r['applied'] = True
    receipt.write_text(json.dumps(r, indent=2))
    print('APPLIED', len(r['files']), 'files')
    raise SystemExit

changes = {}
for name in ('HK416', 'AEK'):
    rel = 'Code/Weapon_' + name + 'Modular.lua'
    s = (ROOT / rel).read_text(encoding='utf-8-sig')
    assert 'Post-release attachment fit' not in s
    if name == 'HK416':
        addition = '''
    -- Post-release attachment fit: absolute millimetres, never accumulated.
    local under = vis.parts and vis.parts.Under
    if IsValid(under) and self.components.Under == "JAZZ_GrenadeLauncher" then
        under:SetAttachOffset(point(60, 0, 0))
    end
    local side = vis.parts and vis.parts.Side
    if IsValid(side) then
        -- Native devices mount on top by default; roll onto the right rail.
        side:SetAttachAxis(point(4096, 0, 0))
        side:SetAttachAngle(-5400)
    end
'''
    else:
        addition = '''
    -- Post-release attachment fit: AKM adapter, with taller 973S receiver.
    local mount = vis.parts and vis.parts.Mount
    local scope = vis.parts and vis.parts.Scope
    if IsValid(mount) and mount:GetEntity() == "WeaponAttA_MountAK47" then
        local lift = configuration(self) == "973S" and 28 or 0
        mount:SetAttachOffset(point(13, 0, -40 + lift))
        if IsValid(scope) then scope:SetAttachOffset(point(0, 0, 26 + lift)) end
    end
'''
    anchor = '    FirearmBase.UpdateVisualObj(self, vis)\n'
    assert s.count(anchor) == 1
    changes[rel] = s.replace(anchor, anchor + addition, 1)

items = (ROOT / 'items.lua').read_text(encoding='utf-8-sig')
for ident in ('JAZZ_Reflex_Closed', 'JAZZ_Reflex_Eotech', 'JAZZ_Reflex_M68',
              'JAZZ_CombatScope_2x', 'JAZZ_CombatScope_ACOG'):
    lo, hi = component_block(items, ident)
    block = items[lo:hi]
    assert not re.search(r'ApplyTo\s*=\s*"AEK971"', block)
    visual = '\nPlaceObj(\'WeaponComponentVisual\', {ApplyTo = "AEK971", Entity = "WeaponAttA_MountAK47", Slot = "Mount", param_bindings = false}),'
    block, n = re.subn(r'Visuals\s*=\s*\{', lambda m: m[0] + visual, block, count=1)
    assert n == 1
    items = items[:lo] + block + items[hi:]
changes['items.lua'] = items
files = {}
for rel, text in changes.items():
    before = (ROOT / rel).read_bytes()
    newline = '\r\n' if b'\r\n' in before else '\n'
    raw = text.replace('\r\n', '\n').replace('\n', newline).encode('utf-8')
    if before.startswith(b'\xef\xbb\xbf'):
        raw = b'\xef\xbb\xbf' + raw
    target = a.build / 'stage' / rel
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(raw)
    files[rel] = {'before': sha(before), 'after': sha(raw)}
receipt.write_text(json.dumps({'files': files, 'applied': False}, indent=2))
print('STAGED', len(files), 'files')
