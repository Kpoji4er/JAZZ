"""Verify original-icon tonal proximity and unchanged v2 framing/alpha."""
import argparse,json
from pathlib import Path
import numpy as np
from PIL import Image,ImageFilter
from calibrate_color import statistics,STAGED,ROOT
from content_scope import disabled_ids

p=argparse.ArgumentParser(__doc__)
p.add_argument('--before',type=Path,required=True)
p.add_argument('--outline-expanded',action='store_true')
a=p.parse_args()
manifest=json.loads((STAGED/'manifest.json').read_text(encoding='utf-8'))
profiles=json.loads((STAGED.parent/'color-profiles.json').read_text(encoding='utf-8'))
rows=[r for r in manifest['rows'] if r.get('icon') and r['weapon'] not in disabled_ids()]
comparisons=[]
for row in rows:
    before=a.before/row['icon'];after=STAGED/row['icon']
    with Image.open(before) as old,Image.open(after) as new:
        assert old.size==new.size,row['icon']
        old_alpha=np.asarray(old.getchannel('A'));new_alpha=np.asarray(new.getchannel('A'))
        if a.outline_expanded:
            assert np.all(new_alpha>=old_alpha),row['icon']
            limit=np.asarray(old.getchannel('A').filter(ImageFilter.MaxFilter(3)))
            assert np.all((new_alpha<=16)|(limit>0)),row['icon']
        else:
            assert np.array_equal(old_alpha,new_alpha),row['icon']
    if row['label']=='default' and row['weapon'] in profiles['profiles']:
        reference=ROOT/profiles['profiles'][row['weapon']]['reference'].removeprefix('Mod/e6L4ECj/')
        target,_=statistics(reference,3);v2,_=statistics(before,3);v3,_=statistics(after,3)
        comparisons.append({'weapon':row['weapon'],'before_error':float(np.mean(abs(v2-target))),
                            'after_error':float(np.mean(abs(v3-target)))})
before_error=float(np.mean([r['before_error'] for r in comparisons]))
after_error=float(np.mean([r['after_error'] for r in comparisons]))
assert after_error<before_error*.5,(before_error,after_error)
report={'status':'PASS','checked_dimensions_and_outline':len(rows),'outline_expanded':a.outline_expanded,'references':len(comparisons),
        'mean_luminance_quantile_error_before':before_error,'mean_luminance_quantile_error_after':after_error,
        'improved_weapons':sum(r['after_error']<r['before_error'] for r in comparisons),'comparisons':comparisons}
(STAGED.parent/'color-verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in report.items() if k!='comparisons'}))
