"""Blender -- --blend FILE --output JSON. Physical exterior-side regression.
The old audit agreed with source normals even when open exterior faces pointed
inward. Check known outer lower-receiver panels against lateral position instead.
This is a targeted regression, not proof of every face or normal-map convention.
"""
import argparse,json,sys
from pathlib import Path
import bpy
p=argparse.ArgumentParser();p.add_argument('--blend',required=True);p.add_argument('--output',type=Path,required=True)
a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);bpy.ops.wm.open_mainfile(filepath=a.blend,use_scripts=False);rows=[]
for suffix in ('Short','Standard','Long'):
 o=bpy.data.objects['JAZZ_HK416_'+suffix]
 faces=[f for f in o.data.polygons if o.data.materials[f.material_index].name=='HK416_416_lower' and abs(f.center.x)>.014 and abs(f.normal.x)>.9 and -.16<f.center.y<.04 and .05<f.center.z<.14]
 outward=sum(f.center.x*f.normal.x>0 for f in faces);assert len(faces)>300 and outward/len(faces)>.9,(suffix,outward,len(faces))
 rows.append({'entity':o.name,'sample_faces':len(faces),'outward':outward,'pass':True})
o=bpy.data.objects['JAZZ_HK416_Magazine'];faces=[f for f in o.data.polygons if abs(f.normal.x)>.9 and abs(f.center.x)>.009]
assert len(faces)>400 and all(f.center.x*f.normal.x>0 for f in faces)
rows.append({'entity':o.name,'sample_faces':len(faces),'outward':len(faces),'pass':True})
a.output.write_text(json.dumps(rows,indent=2));print('PASS physical exterior checks',len(rows))
