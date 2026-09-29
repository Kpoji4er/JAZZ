"""Plan native captures for moving parents and model-specific mount prerequisites."""
import argparse,json
from pathlib import Path
from content_scope import disabled_ids

def plan(catalog):
    tasks=[]
    excluded=disabled_ids()|{'DebugAuto','UnderslungGrenadeLauncher'}
    for weapon in catalog['weapons']:
        if weapon['id'] in excluded:continue
        slots={s['slot']:s for s in weapon['slots']}
        children=[s for s in ('Bipod','Muzzle','Sightsf','Side') if s in slots and slots[s].get('modifiable',True)]
        barrel=slots.get('Barrel')
        if barrel and barrel.get('modifiable',True) and children:
            for option in barrel['options']:
                if option['id']==barrel.get('default'):continue
                prerequisites={'Barrel':option['id']}
                if weapon['id'] in ('M4A1','M16A4'):prerequisites['Handguard']='JAZZ_Handguard_RIS'
                tasks.append({'weapon':weapon['id'],'prerequisites':prerequisites,'variants':children})
        if weapon['id'] in ('M4A1','M16A4'):
            tasks.append({'weapon':weapon['id'],'prerequisites':{'Handguard':'JAZZ_Handguard_RIS'},'variants':['Side','Under']})
    return tasks

if __name__=='__main__':
    p=argparse.ArgumentParser(__doc__);p.add_argument('--catalog',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    tasks=plan(json.loads(a.catalog.read_text(encoding='utf-8-sig')))
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps({'tasks':tasks},indent=2),encoding='utf-8')
    print(json.dumps({'batches':len(tasks),'weapons':len({t['weapon'] for t in tasks})}))
