"""Replace audited families while preserving every other registry/art entry verbatim."""
import argparse
import hashlib
import json
import shutil
from pathlib import Path

p = argparse.ArgumentParser(__doc__)
p.add_argument('--baseline', type=Path, required=True)
p.add_argument('--family', type=Path, required=True)
p.add_argument('--old-graphs', type=Path, required=True)
p.add_argument('--new-graphs', type=Path, required=True)
p.add_argument('--old-captures', type=Path, required=True)
p.add_argument('--new-captures', type=Path, nargs='+', required=True)
p.add_argument('--output', type=Path, required=True)
a = p.parse_args()
read = lambda path: json.loads(path.read_text(encoding='utf-8'))
old, new = read(a.baseline / 'registry.json'), read(a.family / 'registry.json')
changed = set(new['weapons'])
assert changed <= set(old['weapons'])
assert not a.output.exists(), 'Use a new immutable output directory'
layers = {k: v for k, v in old['layers'].items() if v['signature'].split('|')[0] not in changed}
preserved = set(layers)
layers.update(new['layers'])
weapons = dict(old['weapons']); weapons.update(new['weapons'])
merged = dict(old, layers=layers, weapons=weapons)
for name in ['layers', 'graphs', 'references']:
    (a.output / name).mkdir(parents=True, exist_ok=True)
for ident, layer in layers.items():
    if not layer['image']:
        continue
    src = (a.baseline if ident in preserved else a.family) / 'layers' / (ident + '.png')
    dst = a.output / 'layers' / src.name
    shutil.copy2(src, dst)
    assert hashlib.sha256(dst.read_bytes()).digest() == hashlib.sha256(src.read_bytes()).digest()
for weapon in weapons:
    src = (a.new_graphs if weapon in changed else a.old_graphs) / (weapon + '.json')
    shutil.copy2(src, a.output / 'graphs' / src.name)
rows = []
for directory in [a.old_captures, *a.new_captures]:
    receipt = read(directory / 'capture-report.json')
    assert receipt['phase'] == 'done' and receipt['disposed']
    for row in receipt['rows']:
        if directory == a.old_captures and row['weapon'] in changed:
            continue
        row = dict(row)
        if row.get('image'):
            row['image'] = str((directory / row['image']).resolve())
        rows.append(row)
(a.output / 'references/capture-report.json').write_text(json.dumps(
    {'phase': 'done', 'disposed': True, 'errors': [], 'rows': rows}), encoding='utf-8')
(a.output / 'registry.json').write_text(json.dumps(merged, ensure_ascii=False, indent=2), encoding='utf-8')
report = {'changed_families': sorted(changed), 'preserved_families': len(weapons) - len(changed),
          'preserved_layers': len(preserved), 'total_layers': len(layers), 'art_byte_verified': True}
(a.output / 'merge-verification.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
print(json.dumps(report))
