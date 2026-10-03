"""Read-only audit of weapon material changes since --since (default 2026-09-15).
Uses Git history plus working tree; excludes character materials. Writes JSON
with exact material/map inventory, DDS/mip integrity, RM channel and NM statistics.
Numerical checks cannot certify normal-map Y sign or compatibility with mesh bake.
"""
import argparse
import hashlib
import io
import json
from pathlib import Path
import struct
import subprocess
import xml.etree.ElementTree as ET

import numpy as np
from PIL import Image

PREFIXES=('AKR_', 'M16R_', 'M4R_', 'MK14EBR_', 'MOSIN_', 'SR3M_', 'L42A1_',
          'JAZZ_M14_', 'JAZZ_VZ58_', 'JAZZ_VektorR4_', 'JAZZ_FNFAL_', 'FNFAL_',
          'CAR15_', 'M16A1_', 'M16A2_', 'M16A4_', 'M4A1_')


def dds(p):
    data=p.read_bytes()
    assert data[:4]==b'DDS ', p
    h,w=struct.unpack_from('<II',data,12); n=max(1,struct.unpack_from('<I',data,28)[0])
    code=data[84:88].decode(); dx=struct.unpack_from('<I',data,128)[0] if code=='DX10' else None
    block=8 if code=='DXT1' or dx in (71,72,80,81) else 16
    assert code in ('DXT1','DXT3','DXT5','ATI2','BC5U') or dx in (71,72,74,75,77,78,80,81,83,84,95,96,98,99),(p,code,dx)
    expected=(148 if code=='DX10' else 128)+sum(max(1,(max(1,w>>i)+3)//4)*max(1,(max(1,h>>i)+3)//4)*block for i in range(n))
    assert expected==len(data),(p,len(data),expected)
    return {'width':w,'height':h,'mips':n,'complete_mips':n==max(w,h).bit_length(),
            'fourcc':code,'dxgi':dx,'srgb':dx in (72,75,78,99), 'sha256':hashlib.sha256(data).hexdigest()}


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--assets',type=Path,required=True);ap.add_argument('--since',default='2026-09-15')
    ap.add_argument('--output',type=Path,required=True);a=ap.parse_args()
    def git(*args):return subprocess.check_output(['git','-C',str(a.assets),*args],text=True).splitlines()
    changed=set(git('log','--since='+a.since,'--format=','--name-only','--','Entities/Materials'))
    changed.update(git('diff','--name-only','HEAD','--','Entities/Materials'))
    changed.update(git('ls-files','--others','--exclude-standard','--','Entities/Materials'))
    selected={x for x in changed if Path(x).name.startswith(PREFIXES) and (a.assets/x).is_file()}
    entities=set(git('log','--since='+a.since,'--format=','--name-only','--','Entities'))
    entities.update(git('diff','--name-only','HEAD','--','Entities'))
    entities.update(git('ls-files','--others','--exclude-standard','--','Entities'))
    entity_refs={}
    for rel in sorted(entities):
        if not rel.endswith('.ent') or not Path(rel).name.startswith(tuple(x.rstrip('_') for x in PREFIXES)) or not (a.assets/rel).is_file():continue
        refs=[(Path('Entities')/n.get('file')).as_posix() for n in ET.parse(a.assets/rel).getroot().iter('material')]
        entity_refs[rel]=refs;selected.update(refs)
    materials=sorted(selected)
    report={'since':a.since,'entities':entity_refs,'materials':materials,'maps':{},'issues':[],
            'limits':['Y sign and mesh/bake compatibility require source or runtime verification; no automatic flip.',
                      'RM G mismatch is a packing deviation, not proof of visible shader failure.']}
    for rel in materials:
        for node in ET.parse(a.assets/rel).getroot().iter():
            name=node.get('Name')
            if not name or not name.endswith('.dds'):continue
            key=node.tag+':'+name
            if key in report['maps']:
                report['maps'][key]['materials'].append(rel);continue
            row={'name':name,'type':node.tag,'materials':[rel]};report['maps'][key]=row
            try:
                p=a.assets/'Entities/Textures'/name; row['dds']=dds(p)
                fallback=p.parent/'Fallbacks'/name;row['fallback']=dds(fallback)
                # Pillow lacks BC1/BC3 sRGB enums; block bits decode identically.
                # Relabel a memory-only header, retaining the on-disk color metadata.
                raw=bytearray(p.read_bytes())
                if row['dds']['srgb']:
                    struct.pack_into('<I',raw,128,{72:71,75:74,78:77,99:98}[row['dds']['dxgi']])
                with Image.open(io.BytesIO(raw)) as im: v=np.array(im.convert('RGB'))
                if not row['dds']['complete_mips'] or not row['fallback']['complete_mips']:
                    report['issues'].append({'map':key,'issue':'incomplete mip chain'})
                if node.tag in ('RMMap','NormalMap','AOMap') and row['dds']['srgb']:
                    report['issues'].append({'map':key,'issue':'numeric map stored as sRGB'})
                if node.tag=='RMMap':
                    rg=np.abs(v[:,:,0].astype(np.int16)-v[:,:,1].astype(np.int16))
                    row['channels']={c:{'min':int(v[:,:,i].min()),'max':int(v[:,:,i].max()),'mean':float(v[:,:,i].mean())} for i,c in enumerate('RGB')}
                    row['rg_mean_difference']=float(rg.mean());row['rg_p99_difference']=float(np.percentile(rg,99))
                    if rg.mean()>3 or np.percentile(rg,99)>12:
                        report['issues'].append({'map':key,'issue':'roughness not duplicated in G'})
                if node.tag=='NormalMap':
                    xy=v[:,:,:2].astype(np.float32)/127.5-1
                    row['xy_rms']=float(np.sqrt(np.mean(xy**2)))
                    row['xy_length_over_1_05_fraction']=float(np.mean(np.sum(xy**2,axis=2)>1.05))
                    row['zero_xy_fraction']=float(np.mean(np.all(v[:,:,:2]==0,axis=2)))
                    row['y_convention']='unverified; not inferable from DDS statistics'
                    if row['xy_length_over_1_05_fraction']>.05:
                        report['issues'].append({'map':key,'issue':'more than 5% XY vectors exceed unit disk; investigate encoding'})
            except Exception as exc:
                report['issues'].append({'map':key,'issue':'read/header failure','detail':str(exc)})
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(report,indent=2),encoding='utf-8')
    counts={}
    for x in report['issues']:counts[x['issue']]=counts.get(x['issue'],0)+1
    print(json.dumps({'materials':len(materials),'unique_map_bindings':len(report['maps']),'issues':counts,'output':str(a.output)}))


if __name__=='__main__':main()
