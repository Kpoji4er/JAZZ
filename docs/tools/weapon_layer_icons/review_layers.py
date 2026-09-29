"""Compare isolated native layers with their complete reference photograph.

Search layer order for small pilots only. This is visual evidence, not a universal
ordering rule or proof that every dependency combination is covered.
"""
import argparse
import itertools
import json
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw
from process_live import extract
from icon_layout import render


def composite(images,order,size):
    out=Image.new('RGBA',size)
    for key in order:out.alpha_composite(images[key])
    return out


def main():
    p=argparse.ArgumentParser(__doc__);p.add_argument('--capture',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    report=json.loads((a.capture/'capture-report.json').read_text(encoding='utf-8'))
    assert report['phase']=='done' and all(r['status']=='captured' for r in report['rows'])
    a.output.mkdir(parents=True,exist_ok=True)
    images={}
    for row in report['rows']:
        im,bbox,_=extract(a.capture,row)
        if not bbox:raise ValueError('Empty native layer: '+row['label'])
        images[row['label']]=im;im.save(a.output/(row['label']+'.png'))
    reference=images.pop('default');keys=sorted(images)
    if len(keys)>7:raise ValueError('Pilot order search limited to seven layers')
    small={k:v.resize((324,165),Image.Resampling.LANCZOS) for k,v in images.items()}
    ref=np.asarray(reference.resize((324,165),Image.Resampling.LANCZOS)).astype(float)
    premul=lambda x:np.concatenate([x[...,:3]*x[...,3:4]/255,x[...,3:4]],axis=2)
    target=premul(ref);mask=ref[...,3]>16
    scores=[]
    for order in itertools.permutations(keys):
        arr=np.asarray(composite(small,order,(324,165))).astype(float)
        score=float(np.abs(premul(arr)-target)[mask].mean());scores.append((score,order))
    score,order=min(scores)
    result=composite(images,order,reference.size);result.save(a.output/'composed.png')
    weapon=report['rows'][0]['weapon'];full_icon=render(reference,(324,165),weapon);layer_icon=render(result,(324,165),weapon)
    full_icon.save(a.output/'reference-icon.png');layer_icon.save(a.output/'composed-icon.png')
    sheet=Image.new('RGB',(1000,180*(len(keys)+2)),(38,42,46));draw=ImageDraw.Draw(sheet)
    for i,(label,im) in enumerate([('Complete native reference',reference),('Composed isolated layers',result)]+[(k,images[k]) for k in order]):
        thumb=im.copy();thumb.thumbnail((950,160));sheet.paste(thumb,(25,180*i+20),thumb);draw.text((8,180*i+3),label,fill='white')
    sheet.save(a.output/'review.png')
    metrics={'weapon':weapon,'components':report['rows'][0]['components'],'best_back_to_front':order,
             'reference_mask_premultiplied_mae_255':round(score,3),'layer_count':len(keys),
             'camera_restored':report['original_camera']==report['restored_camera'],
             'light_restored':report['restored_light'],'render_restored':report['original_render']==report['restored_render'],
             'disposed':report['disposed'],'inventory_pause_restored':report.get('inventory_pause_restored'),
             'acceptance':'pilot comparison only; broader composition/dependency acceptance pending'}
    (a.output/'verification.json').write_text(json.dumps(metrics,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(metrics,ensure_ascii=True))

if __name__=='__main__':main()
