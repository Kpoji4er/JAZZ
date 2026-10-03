"""Blender: simplify an approved Meshy torso and fit it using the native shirt envelope.

--input GLB --item TireBrigantine|TireArmor|LeatherArmor --shirt JSON --output DIR
Writes a separate 18k-triangle source; never changes the high-detail original.
"""
import argparse, json, runpy, sys
from pathlib import Path
import bpy, bmesh

p=argparse.ArgumentParser(description=__doc__)
for key in ('input','shirt','output'): p.add_argument('--'+key,type=Path,required=True)
p.add_argument('--item',choices=['TireBrigantine','TireArmor','LeatherArmor'],required=True)
p.add_argument('--triangles',type=int,default=18000)
a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
a.output.mkdir(parents=True,exist_ok=True)
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=str(a.input.resolve()))
objects=[o for o in bpy.context.scene.objects if o.type=='MESH']
bpy.ops.object.select_all(action='DESELECT')
for o in objects:o.select_set(True)
bpy.context.view_layer.objects.active=objects[0]
bpy.ops.object.join();o=bpy.context.object
bpy.ops.object.transform_apply(location=True,rotation=True,scale=True)
before=sum(len(f.vertices)-2 for f in o.data.polygons)
if o.data.has_custom_normals:bpy.ops.mesh.customdata_custom_splitnormals_clear()
bm=bmesh.new();bm.from_mesh(o.data)
bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-7)
bm.to_mesh(o.data);bm.free()
dec=o.modifiers.new('Game budget','DECIMATE');dec.ratio=min(1,a.triangles/before)
bpy.ops.object.modifier_apply(modifier=dec.name)
tools=Path(__file__).resolve().parent;sys.path.insert(0,str(tools))
from _ja3_mesh_prepare import prepare_export_mesh
prepare_export_mesh(o)
after=sum(len(f.vertices)-2 for f in o.data.polygons)
assert after<=a.triangles*1.05,(before,after)
reduced=a.output/'reduced.glb'
bpy.ops.export_scene.gltf(filepath=str(reduced),export_format='GLB',use_selection=True)
(a.output/'reduction.json').write_text(json.dumps({'item':a.item,'input':str(a.input),'before':before,'after':after,'method':'local decimation; retained UV/material maps','runtime':'NOT_RUN'},indent=2))
dimensions={'TireBrigantine':(.49,.39,.52,1.00),'TireArmor':(.69,.42,.61,.97),'LeatherArmor':(.48,.37,.49,1.03)}
w,d,h,z=dimensions[a.item]
sys.argv=['fit','--','--input',str(reduced),'--shirt',str(a.shirt),'--output',str(a.output),'--width',str(w),'--depth',str(d),'--height',str(h),'--zmin',str(z)]
runpy.run_path(str(tools/'_fit_meshy_6b3_armor.py'),run_name='__main__')
