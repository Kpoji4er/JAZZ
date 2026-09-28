"""Build staged RGBA icons/contact sheets from live beauty + silhouette captures.

No game writes. Pillow/numpy; keep originals and recipe for replay after mount edits.
"""
import argparse
import csv
import hashlib
import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from icon_layout import render, target_size, RECIPE
from content_scope import disabled_ids


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def save(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')


def extract(directory, row):
    path = directory / row['image']
    beauty = np.array(Image.open(path).convert('RGB')).astype(float)
    white = np.array(Image.open(path.with_stem(path.stem+'-white')).convert('RGB')).astype(float)
    background = np.array(Image.open(path.with_stem(path.stem+'-background')).convert('RGB')).astype(float)
    # WeaponModCMTPlane supplies a black silhouette, NOT an additive white composite.
    # A 6% floor rejects small temporal/background noise; full coverage at 85%.
    coverage = np.max((background-white)/np.maximum(background, 1), axis=2)
    alpha = np.clip((coverage-.06)/.79, 0, 1)
    # Decontaminate only anti-aliased black-background edges; no per-weapon grading.
    rgb = np.clip(beauty/np.maximum(alpha[..., None], .15), 0, 255)
    rgb[alpha == 0] = 0
    rgba = Image.fromarray(np.dstack((rgb, alpha*255)).astype('uint8'), 'RGBA')
    bbox = rgba.getchannel('A').point(lambda x: 255 if x >= 128 else 0).getbbox()
    return rgba, bbox, hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser=argparse.ArgumentParser(__doc__)
    parser.add_argument('--catalog', type=Path, required=True)
    parser.add_argument('--captures', type=Path, nargs='+', required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--profile-manifest',type=Path,help='Reuse locked crop profiles when recapturing a subset')
    args=parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    for folder in ['rgba', 'icons', 'sheets']:
        (args.output/folder).mkdir(exist_ok=True)
    catalog={r['id']: r for r in read(args.catalog)['weapons']}
    cache_path=args.output/'manifest.json'
    cache_time=cache_path.stat().st_mtime if cache_path.exists() else 0
    cached={(r['weapon'],r['label']):r for r in read(cache_path)['rows']} if cache_path.exists() else {}
    latest={}
    reports=[]
    for directory in args.captures:
        report=read(directory/'capture-report.json')
        reports.append({'directory':directory.name,'phase':report['phase'],
            'camera_restored':report.get('original_camera')==report.get('restored_camera'),
            'recipe':report['recipe']})
        for row in report['rows']:
            latest[(row['weapon'], row['label'])]=(directory, row)
    manifest=[]
    for (weapon,label),(directory,row) in latest.items():
        item=dict(row)
        item['source_batch']=directory.name
        item['issues']=[]
        parent=catalog[weapon]['parents'][0]
        item['profile']='pistol' if parent in ['Pistol','Autopistol','Revolver','FlareGun'] else 'long'
        if parent in ['Mortar','RocketLauncher'] or weapon=='BrowningM2HMG': item['profile']='heavy'
        if item['profile']=='long' and row.get('camera_distance',1500)!=1500:
            item['profile']='long-'+str(row['camera_distance'])
        if row['status']=='captured':
            try:
                source=directory/row['image']
                previous=cached.get((weapon,label),{})
                inputs=[source,source.with_stem(source.stem+'-white'),source.with_stem(source.stem+'-background')]
                digest=hashlib.sha256(source.read_bytes()).hexdigest()
                can_reuse=(previous.get('source_batch')==directory.name and previous.get('source_sha256')==digest
                    and 'mean_rgb' in previous and previous.get('rgba')
                    and (args.output/previous['rgba']).exists() and all(p.stat().st_mtime<=cache_time for p in inputs))
                if can_reuse:
                    rgba=Image.open(args.output/previous['rgba'])
                    bbox=previous['bounds_px']
                else:
                    rgba,bbox,digest=extract(directory,row)
                item.update(bounds_px=bbox,source_sha256=digest)
                arr=np.asarray(rgba)
                solid=arr[...,3]>230
                item['solid_pixels']=int(solid.sum())
                item['mean_rgb']=round(float(arr[...,:3][solid].mean()),2) if solid.any() else 0
                if item['mean_rgb']<12:item['issues'].append('very-dark-beauty')
                if bbox is None: item['issues'].append('empty-silhouette')
                elif min(bbox[0],bbox[1],rgba.width-bbox[2],rgba.height-bbox[3])<12:
                    item['issues'].append('touches-capture-edge')
                if bbox and (bbox[2]-bbox[0]<25 or bbox[3]-bbox[1]<12):
                    item['issues'].append('suspiciously-small')
                out=f'{weapon}__{label}.png'
                if not can_reuse:rgba.save(args.output/'rgba'/out)
                item['rgba']='rgba/'+out
            except Exception as err:
                item['issues'].append('processing-error: '+str(err))
        else:
            item['issues'].append(row['status'])
        manifest.append(item)
    # Shared crop per class profile. Identical camera and placement across variants.
    profiles={}
    for profile in sorted({r['profile'] for r in manifest}):
        boxes=[r['bounds_px'] for r in manifest if r['profile']==profile and r.get('bounds_px') and not r['issues']]
        if not boxes: continue
        left=min(b[0] for b in boxes);top=min(b[1] for b in boxes)
        right=max(b[2] for b in boxes);bottom=max(b[3] for b in boxes)
        width=max(right-left+48, (bottom-top+48)*324/165)
        height=width*165/324
        cx=(left+right)/2;cy=(top+bottom)/2
        profiles[profile]=[round(cx-width/2),round(cy-height/2),round(cx+width/2),round(cy+height/2)]
    if args.profile_manifest:
        profiles=read(args.profile_manifest)['style']['profile_crops']
    for row in manifest:
        if 'rgba' not in row or row['profile'] not in profiles: continue
        if row['weapon'] in disabled_ids(): continue
        size=target_size(catalog[row['weapon']])
        with Image.open(args.output/row['rgba']) as source:
            outline=render(source,size,row['weapon'])
        row['icon']='icons/'+Path(row['rgba']).name
        row['icon_size']=list(size)
        row['icon_recipe']=RECIPE['version']
        outline.save(args.output/row['icon'])
    save(args.output/'manifest.json', {'schema':1,'catalog_count':len(catalog),'sources':reports,
        'style':{'size':'original Icon: 324x165 or 162x110','outline_px':RECIPE['outline_px'],'output_recipe':RECIPE,'profile_crops':profiles,
        'lighting':'LightmodelPreset defaults, Default LUT, EV+1, white sun1000 az90 alt40; fixed time/fog/bloom',
        'recipe_label_correction':'Early source report labels say Day clone. Engine table.copy(Preset) returned {}, so actual photographed base was LightmodelPreset defaults. Explicit-default replay verified in ../lighting-consistency.json.',
        'alpha':'silhouette background ratio, floor .06, full .85','color':'Original-icon per-weapon tone profile; color-profiles.json; per-configuration alpha bounds'},
        'rows':manifest})
    fontpath=Path('C:/Windows/Fonts/arial.ttf')
    font=ImageFont.truetype(str(fontpath),15) if fontpath.exists() else ImageFont.load_default()
    small=ImageFont.truetype(str(fontpath),12) if fontpath.exists() else font
    sets={'defaults':[r for r in manifest if r['label']=='default'],
          'variants':[r for r in manifest if r['label']!='default']}
    for kind,rows in sets.items():
        for start in range(0,len(rows),24):
            subset=rows[start:start+24]
            canvas=Image.new('RGB',(4*340,6*215),(32,36,42));draw=ImageDraw.Draw(canvas)
            for index,row in enumerate(subset):
                x=index%4*340;y=index//4*215
                draw.rectangle((x+4,y+4,x+336,y+171),fill=(66,70,78) if index%2==0 else (218,219,221))
                if row.get('icon'):
                    icon=Image.open(args.output/row['icon'])
                    canvas.paste(icon,(x+8,y+5),icon)
                draw.text((x+8,y+174),row['weapon'],font=font,fill=(245,245,245))
                text=row['label'].replace('JAZZ_','')
                draw.text((x+8,y+194),text[:45],font=small,fill=(235,120,110) if row['issues'] else (180,185,193))
            canvas.save(args.output/'sheets'/f'{kind}-{start//24+1:02}.jpg',quality=92)
    summary={'weapons':len(catalog),'defaults':len(sets['defaults']),'variants':len(sets['variants']),
        'captured':sum(r['status']=='captured' for r in manifest),
        'icons':sum('icon' in r for r in manifest),
        'flagged':[{'weapon':r['weapon'],'label':r['label'],'issues':r['issues']} for r in manifest if r['issues']],
        'missing_defaults':sorted(set(catalog)-{r['weapon'] for r in sets['defaults']})}
    save(args.output/'verification.json',summary)
    print(json.dumps(summary,ensure_ascii=True))


if __name__=='__main__': main()
