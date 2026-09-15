"""Decode extracted weapon LOD0 meshes through the existing HGM reader."""
import argparse,subprocess,json
from pathlib import Path
p=argparse.ArgumentParser()
p.add_argument('--reference',type=Path,required=True)
p.add_argument('--reader',type=Path,required=True)
p.add_argument('--cached',action='store_true',help='Reuse already decoded JSON from this extraction')
a=p.parse_args();out=a.reference/'Geometry';out.mkdir(exist_ok=True);report=[]
for src in sorted((a.reference/'Meshes').glob('*.hgm')):
    if src.stem.endswith(('.1','.2','.3')):continue
    dest=out/(src.stem+'.json')
    result=subprocess.CompletedProcess([],0,'','') if a.cached and dest.exists() else subprocess.run([str(a.reader),str(src),str(dest)],capture_output=True,text=True)
    if result.returncode==0:
        data=json.loads(dest.read_text());objdir=a.reference/'OBJ';objdir.mkdir(exist_ok=True)
        # Calibrated HGM-to-Blender axes: (-Y,-X,Z), metre units. Vertex
        # quantization is relative to each mesh's bounding-box centre.
        with (objdir/(src.stem+'.obj')).open('w') as f:
            f.write('# Geometry reference only; metres; no UV/material round-trip.\n')
            offset=1
            for n,mesh in enumerate(data['meshes']):
                b=mesh['bbox'] or data['bbox'];c=[(b[i]+b[i+3])*.5 for i in range(3)]
                f.write(f'o {src.stem}_{n}\n')
                for v in mesh['vertices']:
                    x,y,z=[v[i]+c[i] for i in range(3)]
                    f.write(f'v {-y:.8f} {-x:.8f} {z:.8f}\n')
                for face in mesh['faces']:f.write('f '+' '.join(str(i+offset) for i in reversed(face))+'\n')
                offset+=len(mesh['vertices'])
    report.append({'mesh':src.name,'ok':result.returncode==0,'error':result.stderr[-1500:] if result.returncode else ''})
(a.reference/'decode-report.json').write_text(json.dumps(report,indent=2))
print(f'Decoded {sum(r["ok"] for r in report)}/{len(report)} LOD0 meshes; see decode-report.json for failures')
