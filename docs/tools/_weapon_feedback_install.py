"""Stage/apply audited weapon feedback resources with complete backup and hashes.

--build DIR [--apply]. Staging snapshots originals; apply refuses drift/running game.
Existing registrations/material references remain unchanged. No mass regeneration.
"""
import argparse,hashlib,json,shutil,struct,subprocess
from pathlib import Path
from PIL import Image
from lupa import LuaRuntime
ROOT=Path(__file__).resolve().parents[2];SUITE=ROOT.parent
def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def main():
    p=argparse.ArgumentParser();p.add_argument('--build',type=Path,required=True);p.add_argument('--apply',action='store_true')
    p.add_argument('--refresh-icons',action='store_true',help='Refresh inspected icons after installation; preserve the original backup')
    a=p.parse_args();b=a.build
    if a.refresh_icons:
        assert a.apply,'Icon refresh requires --apply'
        running=subprocess.run(['powershell','-NoProfile','-Command','Get-Process JA3,JA3Debug,Ged -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Id'],capture_output=True,text=True)
        assert not running.stdout.strip(),'Game/editor is running'
        manifest=json.loads((b/'install-manifest.json').read_text())
        for rel,h in manifest.items():
            assert digest(SUITE/rel)==h['after'] and digest(b/'install-backup'/rel)==h['before'],rel
        icons={rel:b/'icons'/Path(rel).name for rel in manifest if rel.startswith('jazz/WeaponIcons/')}
        for rel,source in icons.items():
            im=Image.open(source);assert im.mode=='RGBA' and im.size==(324,165)
            box=im.getchannel('A').getbbox();assert box[0]>0 and box[2]<324,('Clipped outline',rel,box)
        previous={rel:(SUITE/rel).read_bytes() for rel in icons}
        try:
            for rel,source in icons.items():
                shutil.copy2(source,SUITE/rel);assert digest(SUITE/rel)==digest(source)
                shutil.copy2(source,b/'install-stage'/rel);manifest[rel]['after']=digest(source)
        except Exception:
            for rel,data in previous.items():(SUITE/rel).write_bytes(data)
            raise
        (b/'install-manifest.json').write_text(json.dumps(manifest,indent=2));print('REFRESHED',len(icons),'icons; original backups preserved');return
    if not a.apply:
        sources={};reports=json.loads((b/'compiled-report.json').read_text());assert len(reports)==4 and all(r['pass'] for r in reports)
        from _ja3_mesh_prepare import audit_triangles
        from _decode_vz58_hgm import decode
        for r in reports:
            name=r['entity'];source=b/'ExportedEntities/Meshes'/(name+'_Mesh.m.hgm')
            d=decode(source)
            for sub in d['meshes']:assert not audit_triangles(sub['vertices'],sub['faces'],name=name),name
            sources['jazz_assets/Entities/Meshes/'+source.name]=source
        for source in (b/'candidate-maps/dds').rglob('*.dds'):
            rel=source.relative_to(b/'candidate-maps/dds');raw=source.read_bytes();assert raw[:4]==b'DDS '
            h,w=struct.unpack_from('<II',raw,12)
            old=SUITE/'jazz_assets/Entities/Textures'/rel
            assert (h,w)==struct.unpack_from('<II',old.read_bytes(),12),('Texture resolution changed',rel)
            assert max(h,w)<=(64 if 'Fallbacks' in rel.parts else 4096)
            sources['jazz_assets/Entities/Textures/'+rel.as_posix()]=source
        for name in ('M4A1','AK103','M14','M21','MK14EBR','VZ58','VektorR4'):
            source=b/'icons'/(name+'.png');im=Image.open(source);assert im.size==(324,165) and im.mode=='RGBA'
            assert im.getchannel('A').getextrema()==(0,255)
            sources['jazz/WeaponIcons/'+source.name]=source
        assert (ROOT/'items.lua').read_bytes()==(b/'components/items-before.lua').read_bytes(),'Concurrent items change'
        assert (SUITE/'jazz_assets/Entities/JAZZ_M14.ent').read_bytes()==(b/'components/JAZZ_M14-before.ent').read_bytes()
        LuaRuntime().compile((b/'components/items.lua').read_text(encoding='utf-8'))
        sources['jazz/items.lua']=b/'components/items.lua'
        sources['jazz_assets/Entities/JAZZ_M14.ent']=b/'components/JAZZ_M14.ent'
        stage=b/'install-stage';manifest={}
        for rel,source in sources.items():
            target=SUITE/rel;assert target.is_file(),('Not an existing resource',rel)
            dest=stage/rel;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(source,dest)
            manifest[rel]={'before':digest(target),'after':digest(dest)}
        (b/'install-manifest.json').write_text(json.dumps(manifest,indent=2));print('STAGED',len(manifest),'existing files');return
    running=subprocess.run(['powershell','-NoProfile','-Command','Get-Process JA3,JA3Debug,Ged -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Id'],capture_output=True,text=True)
    assert not running.stdout.strip(),'Close game/editor before installation'
    manifest=json.loads((b/'install-manifest.json').read_text());backup=b/'install-backup';assert not backup.exists(),'Refuse to overwrite backup'
    for rel,h in manifest.items():
        assert digest(SUITE/rel)==h['before'],('Concurrent edit',rel)
        assert digest(b/'install-stage'/rel)==h['after'],('Staging changed',rel)
    for rel in manifest:
        dest=backup/rel;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(SUITE/rel,dest)
    try:
        for rel in manifest:shutil.copy2(b/'install-stage'/rel,SUITE/rel)
        for rel,h in manifest.items():assert digest(SUITE/rel)==h['after'] and digest(backup/rel)==h['before'],rel
    except Exception:
        for rel in manifest:shutil.copy2(backup/rel,SUITE/rel)
        raise
    (b/'installation.json').write_text(json.dumps({'installed_files':len(manifest),'all_installed_and_backup_hashes_verified':True,'runtime_verified':False},indent=2))
    print('INSTALLED',len(manifest),'files with verified backup')
if __name__=='__main__':main()
