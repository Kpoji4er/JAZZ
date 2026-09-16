"""Extract vanilla weapon/attachment geometry and materials for offline fitting.

Archives remain untouched. Textures are not guessed from binary material data.
"""
import argparse,subprocess,json,hashlib
from pathlib import Path
p=argparse.ArgumentParser()
for key in ('game-root','hpk','output'):p.add_argument('--'+key,type=Path,required=True)
p.add_argument('--resume',action='store_true',help='Resume extraction in this tool-owned output directory')
a=p.parse_args();a.output.mkdir(parents=True,exist_ok=a.resume);manifest=[]
for pack in ('Meshes','Skeletons','BinAssets'):
    archive=a.game_root/'Packs'/f'{pack}.hpk'
    lines=subprocess.check_output([str(a.hpk),'list',str(archive)],text=True).splitlines()
    members=[]
    for member in lines:
        name=member.replace('\\','/').rsplit('/',1)[-1].removeprefix('Materials#')
        if name.startswith(('Weapon_','WeaponAtt')) and name.endswith(('.hgm','.hgskel','.mtlbin')):members.append(member)
    if not members:continue
    dest=a.output/pack
    for member in members:assert (dest/member).resolve().is_relative_to(dest.resolve())
    # Keep Windows command lines bounded even with the complete weapon set.
    for offset in range(0,len(members),80):
        subprocess.run([str(a.hpk),'extract','--force',str(archive),str(dest),*members[offset:offset+80]],capture_output=True,check=True)
    for member in members:
        file=dest/member
        manifest.append({'archive':archive.name,'member':member,'bytes':file.stat().st_size,'sha256':hashlib.sha256(file.read_bytes()).hexdigest()})
(a.output/'manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
print(f'Extracted {len(manifest)} files, {sum(v["bytes"] for v in manifest):,} bytes to {a.output}')
