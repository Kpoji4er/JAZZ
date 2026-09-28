"""Read-only check of native AK103 staged graph, spots, DDS headers and icons."""
import argparse
import json
from pathlib import Path
import struct
import xml.etree.ElementTree as ET
from PIL import Image

p=argparse.ArgumentParser(description=__doc__)
p.add_argument('--build',type=Path,required=True)
p.add_argument('--assets',type=Path,default=Path(__file__).resolve().parents[2].parent/'jazz_assets')
a=p.parse_args();b=a.build;s=b/'mod-assets-stage'
names=['AKR_AK103'+x for x in ('','_Handguard','_Magazine','_Muzzle','_Stock','_StockFolded')]
report={'stage_only':True,'entities':{},'icons':{}}
for name in names:
    t=ET.parse(s/(name+'.ent'));old=ET.parse(a.assets/'Entities'/(name+'.ent'))
    assert t.getroot().get('name')==name and not t.findall('.//src')
    assert [x.attrib for x in t.findall('.//attach')]==[x.attrib for x in old.findall('.//attach')],name
    refs=[]
    for mesh in t.findall('.//mesh'):assert (s/mesh.get('file')).is_file()
    for material in t.findall('.//material'):
        mt=ET.parse(s/material.get('file'));assert len(mt.findall('.//Material'))==1
        for node in mt.getroot().iter():
            tex=node.get('Name')
            if not tex:continue
            assert tex.startswith('AKR_AK103_')
            for folder,limit in [('Textures',2048),('Textures/Fallbacks',64)]:
                raw=(s/folder/tex).read_bytes();assert raw[:4]==b'DDS ' and len(raw)>148
                h,w=struct.unpack_from('<II',raw,12);assert 0<max(h,w)<=limit
            refs.append(tex)
    report['entities'][name]={'spots_identical':True,'textures':refs}
for name,size in [('AK103_icon.png',(324,165)),('AK103_Magazine_icon.png',(100,100))]:
    with Image.open(b/name) as im:assert im.size==size;report['icons'][name]=list(im.size)
report['staged_files']=len([p for p in s.rglob('*') if p.is_file()])
(b/'stage-validation.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print('PASS: six entities, unchanged spots, named DDS/fallback headers, one material per entity, icons')
