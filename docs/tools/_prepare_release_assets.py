"""Prepare independently extractable ZIP parts for GitHub's per-asset limit.

Canonical package archives remain intact. Distribution entries extend the suite
manifest; every ZIP entry keeps its path and bytes. No concatenation is needed.
"""
import argparse
import hashlib
import json
import zipfile
from pathlib import Path

LIMIT=2*1024**3
TARGET=1536*1024**2

def sha(path):
    with path.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()

def record(path):
    return {'artifact':path.name,'sha256':sha(path),'bytes':path.stat().st_size}

def distribute(path,limit=LIMIT,target=TARGET):
    if path.stat().st_size < limit:return [record(path)]
    parts=[]
    with zipfile.ZipFile(path) as source:
        groups=[[]];size=0
        names=set()
        for entry in source.infolist():
            if entry.filename in names:raise ValueError('duplicate archive path')
            names.add(entry.filename)
            estimate=entry.compress_size+2*len(entry.filename.encode('utf-8'))+256
            if estimate>=target:raise ValueError('single entry exceeds safe part budget: '+entry.filename)
            if size+estimate>target:
                groups.append([]);size=0
            groups[-1].append(entry);size+=estimate
        for index,group in enumerate(groups,1):
            dest=path.with_name(f'{path.stem}-part{index:02d}.zip')
            with zipfile.ZipFile(dest,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as output:
                for entry in group:
                    # Clone stable metadata, never mutate the source ZipInfo.
                    info=zipfile.ZipInfo(entry.filename,entry.date_time)
                    info.compress_type=zipfile.ZIP_DEFLATED
                    info.create_system=3;info.external_attr=0o644<<16
                    output.writestr(info,source.read(entry))
            if dest.stat().st_size>=limit:raise ValueError('part exceeds GitHub limit')
            parts.append(record(dest))
    return parts

def prepare(manifest_path,out,verify=False):
    manifest=json.loads(manifest_path.read_text(encoding='utf-8'))
    rows=[]
    for package in manifest['packages']:
        path=out/package['artifact']
        if sha(path)!=package['sha256']:raise ValueError('canonical archive checksum mismatch')
        rows.append({'package':package['name'],'artifacts':distribute(path)})
    if verify:
        if rows!=manifest.get('distribution'):raise ValueError('distribution manifest mismatch')
    else:
        manifest['distribution']=rows
        manifest_path.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    assets=[a for row in rows for a in row['artifacts']]
    (out/'SHA256SUMS').write_text(''.join(f"{a['sha256']}  {a['artifact']}\n" for a in assets),encoding='ascii')
    (out/'release-assets.txt').write_text(''.join(a['artifact']+'\n' for a in assets),encoding='utf-8')
    print(json.dumps({'packages':len(rows),'assets':len(assets),'verified':verify}),flush=True)

if __name__=='__main__':
    p=argparse.ArgumentParser(__doc__)
    p.add_argument('--manifest',type=Path,required=True)
    p.add_argument('--out-dir',type=Path,required=True)
    p.add_argument('--verify',action='store_true')
    a=p.parse_args();prepare(a.manifest,a.out_dir,a.verify)
