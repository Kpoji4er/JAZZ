"""Calibrate smooth native-layer family tones against original inventory icons.

Uses current full default captures, not old capture-series histograms. A bounded
power curve avoids local contrast spikes on worn metal; every family part shares
one curve. Alpha, geometry, alignment and source photography remain unchanged.
"""
import argparse,hashlib,json
from pathlib import Path
import numpy as np
from PIL import Image,ImageFilter,ImageDraw
from process_live import extract
from icon_layout import ROOT,fit,colorize,target_size
from content_scope import disabled_ids

def stats(im,erosion):
 a=np.asarray(im.convert('RGBA'));mask=np.asarray(im.getchannel('A').filter(ImageFilter.MinFilter(erosion)))>240
 rgb=a[...,:3][mask].astype(float)/255
 if len(rgb)<40:raise ValueError('not enough opaque pixels')
 lum=rgb@np.array([.2126,.7152,.0722]);sat=(rgb.max(1)-rgb.min(1))/np.maximum(rgb.max(1),.01)
 chroma=sat[(sat>.18)&(lum>.06)]
 return np.percentile(lum,[10,25,50,75,90,97]),float(np.median(chroma)) if len(chroma)>20 else None

def curve(x,y):
 best=None
 for gamma in np.linspace(.7,1.8,111):
  base=x**gamma;gain=float(np.clip(np.dot(base,y)/np.dot(base,base),.35,min(1.4,1.8/gamma)))
  error=float(np.mean((gain*base-y)**2))
  if best is None or error<best[0]:best=error,float(gamma),gain
 error,gamma,gain=best
 xp=np.linspace(0,1,257)
 return {'source_luma':xp.tolist(),'target_luma':np.clip(gain*xp**gamma,0,1).tolist(),'fit':{'gamma':gamma,'gain':gain,'quantile_rmse':error**.5}}

def main():
 p=argparse.ArgumentParser(__doc__);p.add_argument('--catalog',type=Path,required=True);p.add_argument('--captures',type=Path,nargs='+',required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
 catalog={w['id']:w for w in json.loads(a.catalog.read_text(encoding='utf-8'))['weapons']}
 defaults={}
 for directory in a.captures:
  receipt=json.loads((directory/'capture-report.json').read_text(encoding='utf-8'));assert receipt['phase']=='done'
  for row in receipt['rows']:
   if row['status']=='captured' and row['label']=='default' and not row.get('layer'):defaults[row['weapon']]=(directory,row)
 profiles={};missing=[];raw={};refs={}
 for weapon,(directory,row) in defaults.items():
  if weapon in disabled_ids()|{'DebugAuto','UnderslungGrenadeLauncher'}:continue
  path=catalog[weapon]['icon'];ref=ROOT/path.removeprefix('Mod/e6L4ECj/')
  if not path.startswith('Mod/e6L4ECj/') or not ref.exists():missing.append(weapon);continue
  source,_,digest=extract(directory,row);reference=Image.open(ref).convert('RGBA')
  x,ss=stats(source,7);y,ts=stats(reference,3)
  profile=curve(x,y);profile.update(saturation=float(np.clip(ts/ss,.65,1.05)) if ts and ss else 1.0,reference=path,reference_sha256=hashlib.sha256(ref.read_bytes()).hexdigest(),source_sha256=digest)
  profiles[weapon]=profile;raw[weapon]=source;refs[weapon]=reference
 fallback=curve(np.linspace(.05,.95,6),np.median([np.interp(np.linspace(.05,.95,6),v['source_luma'],v['target_luma']) for v in profiles.values()],axis=0));fallback['saturation']=float(np.median([v['saturation'] for v in profiles.values()]))
 output={'version':4,'method':'smooth per-family calibration from current native default captures','profiles':profiles,'fallback':fallback,'fallback_weapons':missing}
 a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(output,ensure_ascii=False,indent=2),encoding='utf-8')
 weapons=[w for w in ['AK74','AK103','M4A1','P226','P38','DesertEagle','HiPower','M2Carbine'] if w in raw]
 sheet=Image.new('RGB',(1030,len(weapons)*190),(38,42,46));d=ImageDraw.Draw(sheet)
 for n,w in enumerate(weapons):
  d.text((10,n*190+3),w+' | original / previous curve / smooth native curve',fill='white')
  variants=[refs[w],fit(colorize(raw[w],w),target_size(catalog[w])),fit(colorize(raw[w],w,profiles=output),target_size(catalog[w]))]
  for i,im in enumerate(variants):sheet.paste(im,(i*340+(340-im.width)//2,n*190+22+(165-im.height)//2),im)
 sheet.save(a.output.with_suffix('.png'))
 print(json.dumps({'profiles':len(profiles),'fallback':missing}))
if __name__=='__main__':main()
