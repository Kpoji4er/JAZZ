"""Compare declared component visuals with photographed part graphs; review queue, not auto-fix."""
import argparse
import json
from pathlib import Path

p=argparse.ArgumentParser(__doc__)
p.add_argument('--catalog',type=Path,required=True)
p.add_argument('--manifest',type=Path,required=True)
p.add_argument('--output',type=Path,required=True)
a=p.parse_args()
catalog={w['id']:w for w in json.loads(a.catalog.read_text(encoding='utf-8'))['weapons']}
rows=json.loads(a.manifest.read_text(encoding='utf-8'))['rows']
queue=[];checked=0
for row in rows:
    if row['status']!='captured' or not row.get('requested_component'):continue
    slot=next((s for s in catalog[row['weapon']]['slots'] if s['slot']==row['requested_slot']),None)
    option=next((o for o in slot['options'] if o['id']==row['requested_component']),None) if slot else None
    if not option:continue
    actual={p['entity'] for p in row['parts']}
    expected={v['entity'] for v in option['visuals'] if v['entity']}
    missing=expected-actual
    checked+=1
    if missing:
        queue.append({'weapon':row['weapon'],'label':row['label'],
            'declared_but_not_in_parts':sorted(missing),'parts':row['parts'],
            'icon':row.get('icon'),'interpretation':'Requires dependency/geometry review; not automatically a broken asset.'})
result={'checked_single_slot_rows':checked,'review_queue':queue,
    'note':'Declared matching visual entities compared with actual vis.parts. Host substitutions and dependency overrides may be intentional.'}
a.output.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(f'{checked} component graphs checked; {len(queue)} discrepancies queued')
