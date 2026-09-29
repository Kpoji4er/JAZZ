"""Count configuration domains without materializing their Cartesian product.

This is an upper bound, not an assertion that all combinations are compatible.
"""
import argparse
import json
import math
from pathlib import Path
from content_scope import disabled_ids


def audit(catalog):
    excluded=disabled_ids() | {'DebugAuto', 'UnderslungGrenadeLauncher'}
    rows=[]
    for weapon in catalog['weapons']:
        if weapon['id'] in excluded:continue
        domains={}
        for slot in weapon['slots']:
            values={slot.get('default') or ''}
            if slot.get('modifiable',True):
                values.update(o['id'] for o in slot['options'])
                if slot.get('empty'):values.add('')
            domains[slot['slot']]=sorted(values)
        rows.append({'weapon':weapon['id'],'domains':domains,
                     'upper_bound':math.prod(len(v) for v in domains.values())})
    return {'schema':1,'meaning':'upper bound before runtime compatibility and visual-equivalence deduplication',
            'excluded':sorted(excluded),'weapon_count':len(rows),
            'upper_bound':sum(r['upper_bound'] for r in rows),
            'weapons':sorted(rows,key=lambda r:(-r['upper_bound'],r['weapon']))}


if __name__=='__main__':
    p=argparse.ArgumentParser(__doc__);p.add_argument('--catalog',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    report=audit(json.loads(a.catalog.read_text(encoding='utf-8-sig')))
    a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({k:v for k,v in report.items() if k!='weapons'},ensure_ascii=True))
