"""Rebuild only Desert Eagle/Hi-Power after smoothing their fixed tone profiles."""
import json,shutil,argparse
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw
from icon_layout import ROOT,render

p=argparse.ArgumentParser(__doc__)
p.add_argument('--backup',type=Path,required=True)
a=p.parse_args()
staged=ROOT/'docs/design/weapon-layer-icons/live/staged'
rows=json.loads((staged/'manifest.json').read_text(encoding='utf-8'))['rows']
sheet=Image.new('RGB',(510,280),(45,49,55));draw=ImageDraw.Draw(sheet)
draw.text((8,5),'Original                  Previous                    Smooth',fill='white')
count=0
for row in rows:
    if row['weapon'] not in ['DesertEagle','HiPower'] or not row.get('icon'):continue
    path=staged/row['icon'];backup=a.backup/row['icon'];backup.parent.mkdir(parents=True,exist_ok=True)
    if not backup.exists():shutil.copy2(path,backup)
    with Image.open(path) as image:old=image.convert('RGBA')
    with Image.open(staged/row['rgba']) as source:new=render(source,tuple(row['icon_size']),row['weapon'])
    assert np.array_equal(np.asarray(old.getchannel('A')),np.asarray(new.getchannel('A')))
    new.save(path);count+=1
    if row['label']=='default':
        y=25+['DesertEagle','HiPower'].index(row['weapon'])*125
        ref=ROOT/'WeaponIcons'/('Deagle.png' if row['weapon']=='DesertEagle' else 'Hipower.png')
        with Image.open(ref) as original:sheet.paste(original,(0,y),original.convert('RGBA'))
        with Image.open(backup) as previous:sheet.paste(previous,(170,y),previous)
        sheet.paste(new,(340,y),new)
sheet.save(staged.parent/'silver-pistols-comparison.png')
print(json.dumps({'rebuilt':count,'alpha_and_size':'unchanged'}))
