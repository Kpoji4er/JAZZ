"""Offline QA roster from JAZZ Legion UnitData and its actual appearance overrides."""
import argparse,re,json
from pathlib import Path
from _integrate_sr3m import matching
ROOT=Path(__file__).resolve().parents[2];UNITS=ROOT.parent/'jazz-units'
p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);p.add_argument('--game-root',type=Path,required=True);a=p.parse_args()
text=(a.game_root/'ModTools/Src/Data/AppearancePreset.lua').read_text(encoding='utf8').replace("PlaceObj('AppearancePreset',","PlaceObj('ModItemAppearancePreset',")+'\n'+(UNITS/'items.lua').read_text(encoding='utf8');presets={}
for m in re.finditer(r"PlaceObj\('ModItemAppearancePreset',",text):
 start=text.index('(',m.start());block=text[m.start():matching(text,start)]
 def field(name):
  found=re.search(r'\b'+name+r'\s*=\s*"([^"]*)"',block);return found.group(1) if found else ''
 uid=field('id')
 if uid:presets[uid]={k:field(k) for k in ('Body','Armor','Pants','Hip','Chest','Head','Hat','Hat2')}
rows=[];missing=[]
for file in sorted((UNITS/'UnitData').glob('JAZZ_Legion_*.lua')):
 source=file.read_text(encoding='utf8')
 for uid in dict.fromkeys(re.findall(r"'Preset',\s*\"([^\"]+)\"",source)):
  if uid not in presets:missing.append({'unit':file.stem,'preset':uid});continue
  rows.append({'unit':file.stem,'preset':uid,**presets[uid],'runtime_fit':'NOT_RUN'})
a.output.parent.mkdir(parents=True,exist_ok=True)
a.output.write_text(json.dumps({'source':'jazz-units/UnitData/JAZZ_Legion_* + jazz-units/items.lua ModItemAppearancePreset','combinations':rows,'unresolved':missing,'unique_bodies':sorted({v['Body'] for v in rows})},indent=2),encoding='utf8')
print('Resolved',len(rows),'unit/preset combinations;',len({v['preset'] for v in rows}),'presets;',len({v['Body'] for v in rows}),'bodies; unresolved',len(missing))
print(sorted({v['Body'] for v in rows}))
if missing:raise SystemExit(1)
