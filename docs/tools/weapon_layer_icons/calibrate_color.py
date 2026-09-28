"""Derive fixed family tone profiles from the original native weapon icons.

No geometry matching or per-variant auto exposure: one default-capture profile
is reused for every configuration of the same weapon.
"""
import hashlib,json
from pathlib import Path
import numpy as np
from PIL import Image,ImageFilter
from icon_layout import ROOT
from content_scope import disabled_ids

STAGED=ROOT/'docs/design/weapon-layer-icons/live/staged'
QUANTILES=[5,15,30,50,70,85,95,99]
SMOOTH_METAL={'DesertEagle','HiPower'}

def smooth_metal_curve(x,y):
    # Bound contrast amplification: histogram knots amplified highlight noise
    # by up to 13x on these silver pistols. Fit one smooth monotonic curve.
    best=None
    for gamma in np.linspace(.7,2.2,151):
        base=np.asarray(x)**gamma
        gain=float(np.clip(np.dot(base,y)/np.dot(base,base),.45,min(1.2,2.0/gamma)))
        error=float(np.mean((gain*base-y)**2))
        if best is None or error<best[0]:best=(error,gamma,gain)
    _,gamma,gain=best
    xp=np.linspace(0,1,257)
    return xp.tolist(),np.clip(gain*xp**gamma,0,1).tolist(),{'method':'bounded-power','gamma':float(gamma),'gain':gain,'max_slope':float(gamma*gain)}

def statistics(path,erosion):
    with Image.open(path) as image:
        rgba=image.convert('RGBA')
        mask=np.asarray(rgba.getchannel('A').filter(ImageFilter.MinFilter(erosion)))>240
        rgb=np.asarray(rgba)[...,:3][mask].astype(np.float32)/255
    if len(rgb)<40:raise ValueError('Insufficient opaque reference pixels')
    lum=rgb@np.array([.2126,.7152,.0722])
    sat=(rgb.max(axis=1)-rgb.min(axis=1))/np.maximum(rgb.max(axis=1),.01)
    chromatic=sat[(sat>.18)&(lum>.06)]
    return np.percentile(lum,QUANTILES),float(np.median(chromatic)) if len(chromatic)>20 else None

def main():
    catalog={r['id']:r for r in json.loads((STAGED.parent/'catalog.json').read_text(encoding='utf-8'))['weapons']}
    defaults={r['weapon']:r for r in json.loads((STAGED/'manifest.json').read_text(encoding='utf-8'))['rows'] if r['label']=='default' and r.get('rgba') and r['weapon'] not in disabled_ids()}
    profiles={};missing=[];fallback_curves=[]
    for weapon,row in defaults.items():
        original=str(catalog[weapon]['icon'])
        reference=ROOT/original.removeprefix('Mod/e6L4ECj/')
        if not original.startswith('Mod/e6L4ECj/') or not reference.is_file():
            missing.append(weapon);continue
        source=STAGED/row['rgba']
        x,ss=statistics(source,7);y,ts=statistics(reference,3)
        # Fixed monotonic luminance curve, preserving endpoints and relative hue.
        xp=[0.0];yp=[0.0]
        for xv,yv in zip(x,y):
            if xv>xp[-1]+.002 and xv<.998:
                xp.append(float(xv));yp.append(float(yv))
        xp.append(1.0);yp.append(1.0)
        saturation=float(np.clip(ts/ss,.65,1.05)) if ts and ss else 1.0
        profiles[weapon]={'source_luma':xp,'target_luma':yp,'saturation':saturation,
                          'reference':original,'reference_sha256':hashlib.sha256(reference.read_bytes()).hexdigest()}
        fallback_curves.append(np.interp(np.linspace(0,1,33),xp,yp))
        if weapon in SMOOTH_METAL:
            xp,yp,fit=smooth_metal_curve(x,y)
            profiles[weapon].update(source_luma=xp,target_luma=yp,smooth_fit=fit)
    # Weapons without a local original use the median measured relationship.
    common=np.linspace(0,1,33)
    fallback={'source_luma':common.tolist(),'target_luma':np.median(fallback_curves,axis=0).tolist(),
              'saturation':float(np.median([p['saturation'] for p in profiles.values()]))}
    output={'version':3,'quantiles':QUANTILES,'profiles':profiles,'fallback':fallback,'fallback_weapons':missing}
    (STAGED.parent/'color-profiles.json').write_text(json.dumps(output,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({'references':len(profiles),'fallback_weapons':missing}))

if __name__=='__main__':main()
