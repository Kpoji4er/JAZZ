"""Refresh contact sheets and measure actual silhouette occupancy for output recipe v2."""
import json
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
from icon_layout import ROOT
from content_scope import disabled_ids

staged=ROOT/'docs/design/weapon-layer-icons/live/staged'
data=json.loads((staged/'manifest.json').read_text(encoding='utf-8'))
rows=[r for r in data['rows'] if r['weapon'] not in disabled_ids() and r.get('icon')]
font=ImageFont.truetype('arial.ttf',14)
report=[]
for kind in ['defaults','variants']:
    selected=[r for r in rows if (r['label']=='default')==(kind=='defaults')]
    for start in range(0,len(selected),24):
        sheet=Image.new('RGB',(1360,1290),(32,36,42));draw=ImageDraw.Draw(sheet)
        for i,r in enumerate(selected[start:start+24]):
            x=i%4*340;y=i//4*215
            draw.rectangle((x+4,y+4,x+336,y+171),fill=(45,49,55) if i%2==0 else (218,219,221))
            with Image.open(staged/r['icon']) as im:
                sheet.paste(im,(x+(340-im.width)//2,y+5+(165-im.height)//2),im)
                b=im.getchannel('A').point(lambda a:255 if a>16 else 0).getbbox()
                report.append({'weapon':r['weapon'],'label':r['label'],'size':list(im.size),'bounds':b})
            draw.text((x+8,y+174),r['weapon'],font=font,fill='white')
            draw.text((x+8,y+194),r['label'].replace('JAZZ_','')[:42],font=font,fill=(180,190,200))
        sheet.save(staged/'sheets'/f'{kind}-{start//24+1:02}.jpg',quality=92)
(staged.parent/'refit-verification.json').write_text(json.dumps({'recipe':data['style']['output_recipe']['version'],'rows':report},indent=2),encoding='utf-8')
print('Reviewed output records:',len(report))
