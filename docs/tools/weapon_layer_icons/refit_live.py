"""Rebuild all active UI icons from unchanged full-size capture RGBA."""
import json,shutil,argparse
from pathlib import Path
from PIL import Image,ImageDraw
from icon_layout import ROOT,RECIPE,target_size,render
from content_scope import disabled_ids

p=argparse.ArgumentParser(__doc__)
p.add_argument('--backup',type=Path,required=True)
a=p.parse_args()
staged=ROOT/'docs/design/weapon-layer-icons/live/staged'
manifest=json.loads((staged/'manifest.json').read_text(encoding='utf-8'))
catalog={r['id']:r for r in json.loads((staged.parent/'catalog.json').read_text(encoding='utf-8'))['weapons']}
disabled=disabled_ids();count=0
samples=['AKM','AK74','M4A1','Colt1911','HiPower','DesertEagle','MP5A2','BrowningM2HMG']
sheet=Image.new('RGB',(990,len(samples)*200),(37,41,47));draw=ImageDraw.Draw(sheet)
draw.text((15,5),'Original icon                       Previous capture                       Corrected capture',fill='white')
a.backup.mkdir(parents=True,exist_ok=True)
if not (a.backup/'manifest.json').exists(): shutil.copy2(staged/'manifest.json',a.backup/'manifest.json')
for row in manifest['rows']:
    if not row.get('icon') or row['weapon'] in disabled:continue
    path=staged/row['icon'];old=Image.open(path).convert('RGBA')
    saved=a.backup/row['icon'];saved.parent.mkdir(parents=True,exist_ok=True)
    if not saved.exists():shutil.copy2(path,saved)
    old=Image.open(saved).convert('RGBA')
    size=target_size(catalog[row['weapon']])
    with Image.open(staged/row['rgba']) as source: result=render(source,size,row['weapon'])
    result.save(path)
    row['icon_size']=list(size);row['icon_recipe']=RECIPE['version'];count+=1
    if row['label']=='default' and row['weapon'] in samples:
        y=samples.index(row['weapon'])*200+25
        ref=ROOT/str(catalog[row['weapon']]['icon']).removeprefix('Mod/e6L4ECj/')
        if ref.is_file():
            with Image.open(ref) as im:sheet.paste(im,(0,y),im.convert('RGBA'))
        sheet.paste(old,(330,y),old);sheet.paste(result,(660,y),result)
        draw.text((15,y+166),row['weapon'],fill='white')
manifest['style']['output_recipe']=RECIPE
manifest['style']['size']='original Icon: 324x165 or 162x110'
manifest['style']['color']='Fixed original-icon tone profile per weapon; all configurations reuse default calibration. See ../color-profiles.json.'
manifest['style']['outline_px']=RECIPE['outline_px']
manifest['style']['framing']='Per-configuration alpha bounds, aspect preserved; 8px large / 5px small padding. profile_crops retained as v1 history only.'
(staged/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
sheet.save(staged.parent/'size-tone-comparison.png')
print(json.dumps({'rebuilt':count,'recipe':RECIPE}))
