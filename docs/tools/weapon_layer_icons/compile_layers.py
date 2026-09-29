"""Compile photographed native parts into a compact configuration-layer registry.

Read-only to installed mods. Requires completed capture receipts and actual catalog.
Parent signatures prevent using muzzle/side layers on an unphotographed parent.
"""
import argparse
import hashlib
import json
import re
from collections import defaultdict
from pathlib import Path
from process_live import extract
from icon_layout import colorize,target_size
from content_scope import disabled_ids

DEPENDENCIES={'Bipod':'Barrel','Muzzle':'Barrel','Sightsf':'Barrel','Side':'Barrel'}
Z={'Magazine':10,'Bipod':12,'Under':15,'Barrel':18,'Scope':20,'General':30,'__host':40,'Handguard':50,'Stock':60,'Muzzle':70,'Sightsf':75,'Side':80}

def read(path):return json.loads(path.read_text(encoding='utf-8-sig'))
def token(signature):return hashlib.sha256(signature.encode()).hexdigest()[:20]
def graph(row):return {d['spot']:d for d in row['layer_graph'] if d['entity']}
def entities(row):return {k:v['entity'] for k,v in graph(row).items()}
def context(row):return json.dumps(row.get('prerequisites') or {},sort_keys=True)


def compile_registry(catalog,captures,output,only=None,snapshot=False,graphs=None):
    output.mkdir(parents=True,exist_ok=True);(output/'layers').mkdir(exist_ok=True)
    previous_registry=read(output/'registry.json') if (output/'registry.json').exists() else {'layers':{}}
    tone_path=Path(__file__).resolve().parents[2]/'design/weapon-layer-icons/live/layer-color-profiles.json'
    tones=read(tone_path)
    excluded=disabled_ids()|{'DebugAuto','UnderslungGrenadeLauncher'}
    catalog={w['id']:w for w in catalog['weapons'] if w['id'] not in excluded and (not only or w['id'] in only)}
    full=[];photos={};baselines={};contexts={};issues=[]
    observed=defaultdict(lambda:defaultdict(set))
    native_rows=defaultdict(list)
    if graphs:
        for path in graphs.glob('*.json'):
            if path.stem not in catalog:continue
            for row in read(path)['rows']:
                native_rows[path.stem].append(row)
                for slot,value in (row['components'] or {}).items():observed[path.stem][slot].add(value)
    for directory in captures:
        receipt=read(directory/'capture-report.json')
        if receipt['phase']!='done' and not snapshot:raise ValueError('Capture still running: '+str(directory))
        for row in receipt['rows']:
            weapon=row['weapon']
            if weapon not in catalog:continue
            if row['status']=='error':issues.append({'weapon':weapon,'capture':row['label'],'error':row.get('error')});continue
            if row.get('layer_signature') and row['status'] in ('captured','reused-layer'):
                if not row.get('layer_entity'):continue # Native placeholder, no geometry.
                photos.setdefault(row['layer_signature'],(directory,row))
            elif not row.get('layer') and row['status']=='captured':
                full.append((directory,row))
                if not row.get('requested_slot'):
                    contexts[(str(directory),weapon,context(row))]=row
                    if not row.get('prerequisites') and (weapon not in baselines or row.get('camera_distance',1500)>baselines[weapon].get('camera_distance',1500)):
                        baselines[weapon]=row
    cameras={w:r.get('camera_distance',1500) for w,r in baselines.items()}
    registry={'revision':'native-layers-v4','layers':{},'weapons':{}}
    cache_path=output/'processing-cache.json';cache=read(cache_path) if cache_path.exists() else {}
    recipe=hashlib.sha256((Path(__file__).with_name('process_live.py').read_bytes()+Path(__file__).with_name('icon_layout.py').read_bytes()+tone_path.read_bytes())).hexdigest()
    # Keep full-resolution coordinates: final crop is shared by all selected layers.
    for signature,(directory,row) in photos.items():
        if row.get('camera_distance',1500)!=cameras.get(row['weapon'],1500):continue
        ident=token(signature);path=output/'layers'/(ident+'.png')
        source=directory/row['image']
        stamp=recipe+str([(p.stat().st_mtime_ns,p.stat().st_size) for p in (source,source.with_stem(source.stem+'-white'),source.with_stem(source.stem+'-background'))])
        cached=cache.get(ident,{})
        if path.exists() and cached.get('stamp')==stamp:
            bbox=cached['bounds']
        else:
            raw,bbox,_=extract(directory,row)
            bbox=raw.getchannel('A').point(lambda a:255 if a>16 else 0).getbbox()
            if bbox:
                colorize(raw,row['weapon'],profiles=tones).save(path)
                cache[ident]={'stamp':stamp,'bounds':list(bbox)}
        if not bbox:
            extent=list(map(int,re.findall(r'-?\d+',row.get('layer_bounds',''))))
            if len(extent)==6 and (extent[0]==extent[3] or extent[2]==extent[5]):
                registry['layers'][ident]={'image':False,'bounds':False,'z':Z.get(row['layer'],45),'signature':signature,'invisible_reason':'native geometry has zero projected extent'}
                continue
            issues.append({'weapon':row['weapon'],'capture':row['label'],'error':'empty layer'});continue
        if min(bbox[0],bbox[1],1296-bbox[2],660-bbox[3])<8:
            issues.append({'weapon':row['weapon'],'capture':row['label'],'error':'layer touches capture edge','bounds':list(bbox)})
        registry['layers'][ident]={'image':'Mod/e6L4ECj/WeaponIcons/Live/Layers/'+path.name,'bounds':list(bbox),'z':Z.get(row['layer'],45),'signature':signature}
    cache_path.write_text(json.dumps(cache),encoding='utf-8')
    for weapon,base in baselines.items():
        definition=catalog[weapon];width,height=target_size(definition)
        slots=[];rules={}
        for slot in definition['slots']:
            if not isinstance(slot['slot'],str) or not slot['slot']:continue
            default=base['components'].get(slot['slot'],slot.get('default') or '')
            options={default}
            if slot.get('modifiable',True):
                options.update(o['id'] for o in slot['options'])
                if slot.get('empty'):options.add('')
            # A component blocked by another installed module can become empty
            # even when its editor slot does not allow manual removal (AUG grip).
            if '' in observed[weapon][slot['slot']] or any(r['weapon']==weapon and r['components'].get(slot['slot'])=='' for _,r in full):options.add('')
            slots.append({'slot':slot['slot'],'default':default,'options':{o:True for o in sorted(options)},'blocked_slots':{o['id']:o['blocked_slots'] for o in slot['options'] if o.get('blocked_slots')}})
            rules[slot['slot']]={default:{}}
            if '' in options and default:
                original=next((o for o in slot['options'] if o['id']==default),None)
                rules[slot['slot']]['']={v['spot']:False for v in original['visuals'] if v['spot'] in entities(base)} if original else {}
        for child,parent in sorted(DEPENDENCIES.items()):
            ci=next((i for i,s in enumerate(slots) if s['slot']==child),None);pi=next((i for i,s in enumerate(slots) if s['slot']==parent),None)
            if ci is not None and pi is not None and pi>ci:slots.append(slots.pop(ci))
        registry['weapons'][weapon]={'width':width,'height':height,'camera_distance':cameras[weapon],'slots':slots,'rules':rules,'base':entities(base),'art':{}}
    for directory,row in full:
        weapon=row['weapon'];profile=registry['weapons'].get(weapon)
        if not profile:continue
        base=baselines[weapon];host=row['entity'];g=graph(row)
        changed=row.get('requested_slot');cid=row.get('requested_component','')
        if changed:
            origin=contexts.get((str(directory),weapon,context(row)),base)
            before=entities(origin);after=entities(row)
            effect={k:after.get(k,False) for k in sorted(before.keys()|after.keys()) if before.get(k)!=after.get(k)}
            previous=profile['rules'].setdefault(changed,{}).get(cid)
            if previous is not None and previous!=effect:
                issues.append({'weapon':weapon,'component':cid,'error':'context-dependent visual delta','previous':previous,'candidate':effect})
            else:profile['rules'][changed][cid]=effect
        if row.get('camera_distance',1500)!=profile['camera_distance']:continue
        art=profile['art'].setdefault(host,{})
        for spot,detail in g.items():
            ident=token(detail['signature'])
            if ident not in registry['layers']:continue
            when={}
            # Parent signature already includes entity, transform and color.
            # Stat-only component aliases with the same native parent need no
            # duplicate photograph or artificial component-ID restriction.
            if spot=='__host' and detail['signature']!=graph(base)['__host']['signature']:
                when={k:v for k,v in row['components'].items() if v!=base['components'].get(k)}
            candidate={'id':ident,'when':when}
            if spot!='__host':
                parent=detail['parent_spot'];candidate.update(parent=parent,parent_id=token(g[parent]['signature']))
            choices=art.setdefault(spot,{}).setdefault(detail['entity'],[])
            if candidate not in choices:choices.append(candidate)
    for weapon,p in registry['weapons'].items():
        for s in p['slots']:
            missing=set(s['options'])-p['rules'][s['slot']].keys()
            if missing:
                # Some slots reject installation on the default fore-end. Infer
                # their entity delta only from native graph pairs with identical
                # remaining effective components (for example RIS + side light).
                pairs=defaultdict(dict)
                for row in native_rows[weapon]:
                    components=row['components'] or {}
                    key=json.dumps({k:v for k,v in components.items() if k!=s['slot']},sort_keys=True)
                    pairs[key][components.get(s['slot'],'')]=row
                for cid in sorted(missing):
                    for group in pairs.values():
                        before=group.get(s['default']);after=group.get(cid)
                        if before and after:
                            left=entities(before);right=entities(after)
                            p['rules'][s['slot']][cid]={k:right.get(k,False) for k in sorted(left.keys()|right.keys()) if left.get(k)!=right.get(k)}
                            break
                missing=set(s['options'])-p['rules'][s['slot']].keys()
            if missing:issues.append({'weapon':weapon,'slot':s['slot'],'error':'missing component rules','components':sorted(missing)})
        # Native geometry can omit a module on a particular parent even while
        # the logical component remains installed (SW Model 10 short barrel).
        # Preserve observed effective state exactly; never invent absent art.
        overrides=[]
        for row in native_rows[weapon]:
            predicted=dict(p['base'])
            values={s['slot']:row['components'].get(s['slot'],s['default']) for s in p['slots']}
            for s in p['slots']:
                for spot,entity in p['rules'][s['slot']].get(values[s['slot']],{}).items():
                    if entity:predicted[spot]=entity
                    else:predicted.pop(spot,None)
            actual=entities(row)
            delta={spot:actual.get(spot,False) for spot in predicted.keys()|actual.keys() if predicted.get(spot)!=actual.get(spot)}
            if delta:
                entry={'when':values,'parts':delta}
                if entry not in overrides:overrides.append(entry)
        if overrides:p['overrides']=overrides
    for weapon in sorted(set(catalog)-set(registry['weapons'])):issues.append({'weapon':weapon,'error':'missing default capture'})
    for ident,layer in registry['layers'].items():
        if ident in previous_registry['layers']:layer['z']=previous_registry['layers'][ident]['z']
    (output/'registry.json').write_text(json.dumps(registry,ensure_ascii=False,indent=2),encoding='utf-8')
    result={'weapons':len(registry['weapons']),'layers':len(registry['layers']),'references':len(full),'issues':issues,'status':'SNAPSHOT' if snapshot else 'REVIEW_REQUIRED'}
    (output/'build-report.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(result,ensure_ascii=True))
    return registry

if __name__=='__main__':
    p=argparse.ArgumentParser(__doc__);p.add_argument('--catalog',type=Path,required=True);p.add_argument('--captures',type=Path,nargs='+',required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--only',nargs='*');p.add_argument('--graphs',type=Path);p.add_argument('--snapshot',action='store_true');a=p.parse_args()
    compile_registry(read(a.catalog),a.captures,a.output,set(a.only) if a.only else None,a.snapshot,a.graphs)
