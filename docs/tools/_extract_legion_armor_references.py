"""Extract only vanilla Legion clothing references to a fresh offline directory."""
import argparse,subprocess,json,hashlib,re
from pathlib import Path
p=argparse.ArgumentParser()
for key in ('game-root','hpk','output'):p.add_argument('--'+key,type=Path,required=True)
p.add_argument('--roster',type=Path)
a=p.parse_args();names=json.loads(a.roster.read_text())['unique_bodies'] if a.roster else [f'Faction_Legion_Top_{i:02d}' for i in range(1,11)];a.output.mkdir(parents=True,exist_ok=False);manifest=[]
for pack in ('Meshes','Skeletons','BinAssets'):
 archive=a.game_root/'Packs'/f'{pack}.hpk'
 lines=subprocess.check_output([str(a.hpk),'list',str(archive)],text=True).splitlines()
 members=[v for v in lines if (any(v.startswith(name+'_') for name in names) and v.endswith('.hgm')) or v=='Male_mesh.hgskel' or (any(v.startswith('Materials\\Materials#'+name+'_') for name in names) and v.endswith('.mtlbin'))]
 dest=a.output/pack
 if not members:raise RuntimeError('No expected references in '+pack)
 for member in members:assert (dest/member).resolve().is_relative_to(dest.resolve())
 subprocess.run([str(a.hpk),'extract',str(archive),str(dest),*members],capture_output=True,check=True)
 for member in members:
  file=dest/member
  manifest.append({'archive':archive.name,'member':member,'bytes':file.stat().st_size,'sha256':hashlib.sha256(file.read_bytes()).hexdigest()})
s=(a.game_root/'ModTools/Src/Data/AppearancePreset.lua').read_text(encoding='utf8');presets=[]
for block in s.split("PlaceObj('AppearancePreset', {")[1:]:
 if re.search(r'\bBody = "Faction_Legion_Top_',block):
  row={}
  for key in ('id','Body','Armor','Pants'):
   match=re.search(r'\b'+key+r' = "([^"]+)"',block);row[key]=match.group(1) if match else ''
  presets.append(row)
(a.output/'manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf8')
(a.output/'appearance-map.json').write_text(json.dumps(presets,indent=2),encoding='utf8')
print('Extracted',len(manifest),'files;',sum(v['bytes'] for v in manifest),'bytes;',len(presets),'presets')
