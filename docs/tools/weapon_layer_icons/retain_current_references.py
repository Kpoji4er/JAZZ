"""Keep old photographs only when their native signatures still exist after a model edit."""
import argparse
import json
from pathlib import Path

p = argparse.ArgumentParser(__doc__)
p.add_argument('--captures', type=Path, required=True)
p.add_argument('--graphs', type=Path, required=True)
p.add_argument('--output', type=Path, required=True)
p.add_argument('--ids', nargs='+', required=True)
a = p.parse_args()
allowed = {}
magazines = {}
for weapon in a.ids:
    rows = json.loads((a.graphs / (weapon + '.json')).read_text(encoding='utf-8'))['rows']
    allowed[weapon] = {d['signature'] for row in rows for d in row['layer_graph'] if d['entity']}
    magazines[weapon] = {}
    for row in rows:
        component = row['components'].get('Magazine')
        magazines[weapon].setdefault(component, set()).update(
            d['signature'] for d in row['layer_graph'] if d['spot'] == 'Magazine')
receipt = json.loads((a.captures / 'capture-report.json').read_text(encoding='utf-8'))
assert receipt['phase'] == 'done' and receipt['disposed']
kept = []
for row in receipt['rows']:
    weapon = row['weapon']
    if weapon not in allowed:
        continue
    if row.get('layer_signature'):
        if row['layer_signature'] not in allowed[weapon]:
            continue
    elif not all(d['signature'] in allowed[weapon] for d in row.get('layer_graph', []) if d['entity']):
        continue
    elif any(d['signature'] not in magazines[weapon].get(row['components'].get('Magazine'), set())
             for d in row.get('layer_graph', []) if d['spot'] == 'Magazine'):
        continue
    row = dict(row)
    if row.get('image'):
        row['image'] = str((a.captures / row['image']).resolve())
    kept.append(row)
receipt['rows'] = kept
a.output.mkdir(parents=True, exist_ok=True)
(a.output / 'capture-report.json').write_text(json.dumps(receipt, ensure_ascii=False), encoding='utf-8')
print(json.dumps({'retained_rows': len(kept), 'weapons': a.ids}))
