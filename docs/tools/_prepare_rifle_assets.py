"""Stage named JA3 rifle resources without writing to active mods.

python docs/tools/_prepare_rifle_assets.py --build <build> --prefix L42A1
  --entities L42A1 L42A1_Scope --export-root <ExportedEntities> --game-root <JA3_ROOT>
"""
import argparse
import hashlib
import shutil
import subprocess
from pathlib import Path
import xml.etree.ElementTree as ET

def stage(build, export, game, prefix, entities):
    out=build/'mod-assets-stage'/'Entities';out.mkdir(parents=True,exist_ok=True)
    names={}
    suffixes={'BaseColorMap':'Base','NormalMap':'Norm','RMMap':'RM','RoughnessMetallicMap':'RM',
              'AOMap':'AO','AmbientOcclusionMap':'AO','SpecialMap':'SPEC','SIMap':'SI','ColorizationMap':'Color'}
    for entity in entities:
        tree=ET.parse(export/(entity+'.ent'));tree.getroot().set('name',entity)
        for lod in tree.findall('.//lod'):
            for source in list(lod.findall('src')):lod.remove(source)
        for mesh in tree.findall('.//mesh'):
            path=Path(mesh.attrib['file']);target=out/path
            assert target.resolve().is_relative_to(out.resolve())
            target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(export/path,target)
        for node in tree.findall('.//material'):
            rel=Path(node.attrib['file']);material=ET.parse(export/rel)
            for tag in material.getroot().iter():
                old=tag.get('Name')
                if not old:continue
                assert tag.tag in suffixes,(tag.tag,old)
                source=export/'Textures'/old
                key=(suffixes[tag.tag],hashlib.sha256(source.read_bytes()).hexdigest())
                if key not in names:
                    name=f'{prefix}_{len(names)+1}_{suffixes[tag.tag]}.dds';names[key]=name
                    target=out/'Textures'/name;target.parent.mkdir(parents=True,exist_ok=True)
                    cvt=game/'ModTools/hgimgcvt.exe'
                    subprocess.run([str(cvt),str(source),str(target),'--truncate','2048'],check=True,capture_output=True)
                    fallback=out/'Textures/Fallbacks'/name;fallback.parent.mkdir(parents=True,exist_ok=True)
                    subprocess.run([str(cvt),str(target),str(fallback),'--truncate','64'],check=True,capture_output=True)
                tag.set('Name',names[key])
            target=out/rel;target.parent.mkdir(parents=True,exist_ok=True);material.write(target,encoding='utf-8',xml_declaration=True)
        tree.write(out/(entity+'.ent'),encoding='utf-8',xml_declaration=True)
        (out/(entity+'.lua')).write_text(f'EntityData["{entity}"] = {{ editor_artset = "Mods" }}\n',encoding='utf-8')
    print(f'Staged {len(entities)} entities and {len(names)} shared texture/fallback pairs in {out}')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--build',required=True,type=Path);p.add_argument('--export-root',required=True,type=Path)
    p.add_argument('--game-root',required=True,type=Path);p.add_argument('--prefix',required=True);p.add_argument('--entities',nargs='+',required=True)
    a=p.parse_args();stage(a.build,a.export_root,a.game_root,a.prefix,a.entities)
