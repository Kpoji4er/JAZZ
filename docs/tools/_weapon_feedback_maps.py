"""Decode installed DDS for exact material review, including BC5 Z reconstruction.

--assets DIR --output DIR --entity NAME (repeatable). No installed writes.
"""
import argparse, io, json, struct
from pathlib import Path
import xml.etree.ElementTree as ET
import numpy as np
from PIL import Image

def read_dds(path,normal=False):
    raw=bytearray(path.read_bytes())
    if raw[84:88]==b'DX10':
        fmt=struct.unpack_from('<I',raw,128)[0]
        struct.pack_into('<I',raw,128,{72:71,75:74,78:77,99:98}.get(fmt,fmt))
    arr=np.array(Image.open(io.BytesIO(raw)).convert('RGBA'))
    if normal:
        xy=arr[:,:,:2].astype(float)/127.5-1
        arr[:,:,2]=np.rint((np.sqrt(np.maximum(0,1-np.sum(xy*xy,axis=2)))+1)*127.5).astype(np.uint8)
    return arr

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--assets',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
    p.add_argument('--textures',type=Path,help='Prefer staged replacements from this directory')
    p.add_argument('--entity',action='append',required=True);a=p.parse_args()
    a.output.mkdir(parents=True,exist_ok=True)
    report=json.loads((a.output/'bindings.json').read_text()) if (a.output/'bindings.json').exists() else {}
    slots={'BaseColorMap':'Base','NormalMap':'Normal','RMMap':'RM','AOMap':'AO'}
    for entity in a.entity:
        ent=ET.parse(a.assets/'Entities'/(entity+'.ent'))
        refs=ent.findall('.//material');assert len(refs)==1,(entity,len(refs))
        mat=ET.parse(a.assets/'Entities'/refs[0].get('file'))
        report[entity]={}
        for node in mat.getroot().iter():
            if node.tag not in slots:continue
            key=slots[node.tag];source=a.assets/'Entities/Textures'/node.get('Name')
            if a.textures and (a.textures/source.name).exists():source=a.textures/source.name
            arr=read_dds(source,key=='Normal')
            Image.fromarray(arr).save(a.output/(entity+'_'+key+'.png'))
            report[entity][key]=str(source)
    (a.output/'bindings.json').write_text(json.dumps(report,indent=2))
    print('DECODED',len(report),'materials')

if __name__=='__main__':main()
