"""Check real files/coverage/alpha/recipe and record explicit limitations of a capture."""
import argparse
import hashlib
import json
from pathlib import Path
from PIL import Image

p=argparse.ArgumentParser(__doc__)
p.add_argument('--catalog',type=Path,required=True)
p.add_argument('--staged',type=Path,required=True)
p.add_argument('--captures',type=Path,nargs='+',required=True)
a=p.parse_args()
catalog=json.loads(a.catalog.read_text(encoding='utf-8'))['weapons']
manifest=json.loads((a.staged/'manifest.json').read_text(encoding='utf-8'))
names=json.loads((a.staged/'name-matrix.json').read_text(encoding='utf-8'))
expected={(w['id'],'default') for w in catalog}
for w in catalog:
    for s in w['slots']:
        for o in s['options']:
            if o['id']!=s['default']:expected.add((w['id'],s['slot']+'-'+o['id']))
        if s['empty'] and s['default']:expected.add((w['id'],s['slot']+'-empty'))
actual={(r['weapon'],r['label']) for r in manifest['rows']}
errors=[];checks=[]
for row in manifest['rows']:
    if row['status']!='captured':continue
    for key in ['icon','rgba']:
        if key not in row or not (a.staged/row[key]).is_file():errors.append(f'{row["weapon"]}/{row["label"]}: missing {key}')
    if not row.get('icon'):continue
    with Image.open(a.staged/row['icon']) as im:
        if im.mode!='RGBA' or im.size!=tuple(row.get('icon_size',[324,165])):errors.append(row['icon']+': wrong format')
        if im.mode=='RGBA':
            extrema=im.getchannel('A').getextrema()
            if extrema!=(0,255):errors.append(row['icon']+': missing solid or transparent alpha')
            bbox=im.getchannel('A').point(lambda value:255 if value>16 else 0).getbbox()
            if bbox and min(bbox[0],bbox[1],im.width-bbox[2],im.height-bbox[3])==0:
                errors.append(row['icon']+': visible alpha touches final icon edge')
    if row.get('requested_slot') and (row['components'].get(row['requested_slot']) or '') != (row.get('requested_component') or ''):
        errors.append(row['icon']+': requested component mismatch')
for directory in a.captures:
    r=json.loads((directory/'capture-report.json').read_text(encoding='utf-8'))
    checks.append({'batch':directory.name,'phase':r['phase'],
        'camera_restored':r.get('original_camera')==r.get('restored_camera'),
        'captured':sum(x['status']=='captured' for x in r['rows']),
        'failures':[x for x in r['rows'] if x['status']!='captured']})
    if r['phase']!='done' or r.get('original_camera')!=r.get('restored_camera'):errors.append(directory.name+': incomplete lifecycle')
    if 'restored_render' in r:
        if r['original_render']!=r['restored_render'] or not r['restored_light'] or not r['disposed']:
            errors.append(directory.name+': state restoration mismatch')
if {r['id'] for r in names['rows']}!={r['id'] for r in catalog}:errors.append('name matrix differs from live catalog')
cleanup_path=a.staged.parent/'cleanup.json'
cleanup=None
if cleanup_path.exists():
    wrapper=json.loads(cleanup_path.read_text(encoding='utf-8'))
    result=wrapper['body']['result']
    cleanup,_=json.JSONDecoder().raw_decode(result.removeprefix('OK: '))
    if cleanup['capture_area_objects']:errors.append('temporary objects remain in capture area')
    reference=json.loads((a.captures[0]/'capture-report.json').read_text(encoding='utf-8'))
    if cleanup['camera']!=reference['original_camera']:errors.append('final camera differs from capture baseline')
else:errors.append('final cleanup probe missing')
result={'catalog_count':len(catalog),'expected_single_slot_configurations':len(expected),
    'manifest_configurations':len(actual),'missing':sorted(expected-actual),'additional_configurations':sorted(actual-expected),
    'errors':errors,'batches':checks,'cleanup':cleanup,'limits':['single-slot changes relative to defaults, not all combinations',
    'UI legality not established by direct component setter','mount geometry provisional','staged only; not installed'],
    'pass':not errors and not expected-actual}
(a.staged/'integrity.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'pass':result['pass'],'weapons':len(catalog),'expected':len(expected),
    'configurations':len(actual),'missing':len(expected-actual),'additional':len(actual-expected),
    'errors':errors},ensure_ascii=True))
raise SystemExit(0 if result['pass'] else 1)
