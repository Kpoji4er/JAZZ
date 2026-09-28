"""Blender geometry-only comparison of decoded vanilla magazines; --source DIR --output BLEND.
Each magazine keeps its scale; arranged side by side for a profile inspection.
"""
import argparse,json,sys
from pathlib import Path
import bpy
p=argparse.ArgumentParser();p.add_argument('--source',type=Path);p.add_argument('--output')
p.add_argument('--blend');p.add_argument('--target')
a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
if a.blend:bpy.ops.wm.open_mainfile(filepath=a.blend)
else:bpy.ops.wm.read_factory_settings(use_empty=True)
files=[a.source] if a.source.is_file() else sorted(a.source.glob('*_mesh.hgm.json'))
for index,path in enumerate(files):
 d=json.loads(path.read_text());verts=[];faces=[]
 for sub in d['meshes']:
  b=sub.get('bbox') or d['bbox'];c=[(b[i]+b[i+3])/2 for i in range(3)];offset=len(verts)
  verts.extend((-(v[1]+c[1]),-(v[0]+c[0])+index*.18,v[2]+c[2]) for v in sub['vertices'])
  faces.extend(tuple(i+offset for i in f) for f in sub['faces'])
 mesh=bpy.data.meshes.new(path.stem);mesh.from_pydata(verts,[],faces);mesh.update()
 if a.target:
  obj=bpy.data.objects[a.target];obj.data=mesh
 else:
  obj=bpy.data.objects.new(path.stem,mesh);bpy.context.collection.objects.link(obj)
 print(index,path.name)
bpy.ops.wm.save_as_mainfile(filepath=a.output)
