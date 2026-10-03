"""Stage author textures for VZ58/R4/AK103 without artistic adjustments.

--weapons ROOT --game-root ROOT --assets ROOT --build NEW_DIR
Uses original extracted PNGs and the original AK103 native UV atlases. No install.
RM = (roughness,roughness,metallic). Normal XY are neither flipped nor attenuated.
Wire stock has no author PBR set: retains initial import constants and AO.
"""
import argparse
import json
from pathlib import Path
import shutil
import struct
import subprocess
import xml.etree.ElementTree as ET
import numpy as np
from PIL import Image
from _reimport_weapon_rm import sha
from _audit_recent_weapon_textures import dds


def main():
    p=argparse.ArgumentParser(description=__doc__)
    for n in ('weapons','game-root','assets','build'):p.add_argument('--'+n,type=Path,required=True)
    a=p.parse_args();a.build.mkdir(parents=True,exist_ok=False)
    report={'kind':'author-textures','files':[],'maps':[],'guards':{},'applied':False}
    source_root=a.weapons/'_vz58_jazz_20260926/source'
    tgas=a.build/'tga';tgas.mkdir()
    tex=a.assets/'Entities/Textures'
    sets=[]
    def add_png(folder,prefix,normal,base,rm,ao=None):
        paths=list(folder.glob(prefix+'*.png'))
        def find(*parts):
            matches=[p for p in paths if any(s in p.name[len(prefix):] for s in parts)]
            assert len(matches)==1,(prefix,parts,matches)
            return matches[0]
        maps={'NormalMap':(normal,[find('Normal','_Nor','_No.png')]),
              'BaseColorMap':(base,[find('Base','_Bas','_Ba.png')]),
              'RMMap':(rm,[find('Rough','_Rou','_Ro.png'),find('Metal','_Met','_Me.png')])}
        if ao:maps['AOMap']=(ao,[find('AmbientOcclusion')])
        sets.append(maps)
    for key,folder,prefix in [
        (1,'classic','SA_vz.58_(TextureReady)_Steel_Body'),
        (4,'modern','Attatchemnts'),(7,'modern','Stock,Grip_CZX'),
        (10,'classic','SA_vz.58_(TextureReady)_Wood_Front'),
        (13,'modern','Gun_Expert_Foregrip'),
        (16,'classic','SA_vz.58_(TextureReady)_Mag_and_Bullet'),
        (19,'modern','Mag_Grip'),
        (25,'classic','SA_vz.58_(TextureReady)_Wood_Back_Stock'),
        (28,'modern','SA_vz.58_Suppressor')]:
        add_png(source_root/folder,prefix,f'JAZZ_VZ58_{key}_Norm.dds',f'JAZZ_VZ58_{key+1}_Base.dds',f'JAZZ_VZ58_{key+2}_RM.dds')
    add_png(a.weapons/'_r4_jazz_20260926/source','R4_low_R4_',
        'JAZZ_VektorR4_1_Norm.dds','JAZZ_VektorR4_3_Base.dds','JAZZ_VektorR4_4_RM.dds','JAZZ_VektorR4_2_AO.dds')
    native=a.weapons/'_ak103_native_20260926/Textures'
    for start,prefix in [(0,'NativeAtlas'),(3,'Handguard_NativeAtlas'),
                         (6,'mag_ak_762x39_izhmash_103'),(10,'Muzzlebrake'),(13,'Stock')]:
        has_ao=start==6
        row={}
        for kind,idx,suffix in [('NormalMap',start,'Normal'),('BaseColorMap',start+1+has_ao,'Base'),('RMMap',start+2+has_ao,'RM')]:
            tag={'Normal':'Norm','Base':'Base','RM':'RM'}[suffix]
            row[kind]=(f'AKR_AK103_{idx}_{tag}.dds',[native/f'AKR_AK103_{prefix}_{suffix}.tga'])
        if has_ao:row['AOMap']=('AKR_AK103_7_AO.dds',[native/f'AKR_AK103_{prefix}_AO.tga'])
        sets.append(row)
    wire=a.weapons/'_vz58_jazz_20260926/Textures'
    sets.append({kind:(f'JAZZ_VZ58_{idx}_{suffix}.dds',[wire/f'JAZZ_VZ58_Wire_{suffix}.tga'])
                 for kind,idx,suffix in [('AOMap',22,'AO'),('BaseColorMap',23,'Base'),('RMMap',24,'RM')]})
    names={name for group in sets for name,_ in group.values()}
    referenced=set()
    for prefix in ('JAZZ_VZ58','JAZZ_VektorR4','AKR_AK103'):
        for mat in (a.assets/'Entities/Materials').glob(prefix+'*.mtl'):
            report['guards'][str(mat.relative_to(a.assets))]=sha(mat)
            referenced.update(n.get('Name') for n in ET.parse(mat).getroot().iter() if n.get('Name'))
        for folder,ext in [('Entities','ent'),('Entities/Meshes','hgm')]:
            for mesh in (a.assets/folder).glob(prefix+'*.'+ext):report['guards'][str(mesh.relative_to(a.assets))]=sha(mesh)
    assert names==referenced,(names-referenced,referenced-names)
    for group in sets:
        for kind,(name,paths) in group.items():
            target=tex/name;meta=dds(target);size=(meta['width'],meta['height'])
            inputs=[];arrays=[]
            for src in paths:
                inputs.append({'path':str(src.relative_to(a.weapons)),'sha256':sha(src)})
                with Image.open(src) as im:arrays.append(np.array(im.convert('RGB').resize(size,Image.Resampling.LANCZOS)))
            values=arrays[0].copy()
            if kind=='RMMap':
                values[:,:,1]=values[:,:,0]
                if len(arrays)==2:values[:,:,2]=arrays[1][:,:,0]
            tga=tgas/Path(name).with_suffix('.tga');Image.fromarray(values).save(tga,compression=None)
            assert tga.read_bytes()[2]==2
            full=a.build/'staged/Entities/Textures'/name;full.parent.mkdir(parents=True,exist_ok=True)
            if kind=='NormalMap':
                cmd=[str(a.game_root/'ModTools/AssetsProcessor/hgnvcompress.exe'),'-normal','-nocuda','-bc5',str(tga),str(full)]
            else:
                cmd=[str(a.game_root/'ModTools/hgimgcvt.exe'),str(tga),str(full),'--compression','BC1','--alpha','0','--mips',str(meta['mips'])]
            result=subprocess.run(cmd,capture_output=True,text=True)
            assert result.returncode==0 and full.exists(),result.stdout+result.stderr
            data=bytearray(full.read_bytes())
            if data[84:88]==b'DX10':
                struct.pack_into('<I',data,128,83 if kind=='NormalMap' else 72 if kind=='BaseColorMap' else 71)
                full.write_bytes(data)
            output=dds(full);assert output['complete_mips'] and (output['width'],output['height'])==size
            # Verify orientation and channel transfer against actual decoded output.
            import io
            memory=bytearray(full.read_bytes())
            if kind=='BaseColorMap' and memory[84:88]==b'DX10':struct.pack_into('<I',memory,128,71)
            with Image.open(io.BytesIO(memory)) as im:decoded=np.array(im.convert('RGB')).astype(np.int16)
            channels=2 if kind=='NormalMap' else 3
            err=np.abs(decoded[:,:,:channels]-values[:,:,:channels].astype(np.int16))
            assert float(err.mean())<8,(name,float(err.mean()))
            fallback=full.parent/'Fallbacks'/name;fallback.parent.mkdir(exist_ok=True)
            subprocess.run([str(a.game_root/'ModTools/hgimgcvt.exe'),str(full),str(fallback),'--truncate',str(min(64,max(size)))],check=True,capture_output=True)
            assert dds(fallback)['complete_mips']
            report['maps'].append({'name':name,'kind':kind,'sources':inputs,'mean_compression_error':float(err.mean()),
                                  'normal_strength':1 if kind=='NormalMap' else None,'flip_green':False,'after':output})
            for src in (full,fallback):
                rel=src.relative_to(a.build/'staged');old=a.assets/rel;backup=a.build/'backup'/rel
                backup.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(old,backup)
                report['files'].append({'path':str(rel),'before':sha(old),'after':sha(src)})
            print('STAGED',name,flush=True)
    (a.build/'manifest.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    print('PASS',len(report['maps']),'maps',len(report['files']),'files')


if __name__=='__main__':main()
