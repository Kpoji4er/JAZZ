"""Blender: --source-build DIR --output DIR. Split HK416 source into review modules.
Preserve source files; no runtime writes. Explicit unresolved material/UV gate.
"""
import argparse,hashlib,json,sys
from pathlib import Path
import bpy,bmesh
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parent))
from _ja3_mesh_prepare import prepare_export_mesh,mesh_has_custom_normals
from _inspect_weapon_source import world_bbox,setup_render
p=argparse.ArgumentParser();p.add_argument('--source-build',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);a.output.mkdir(parents=True,exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(a.source_build/'clean/Source.blend'),use_scripts=False)
original=[o for o in bpy.context.scene.objects if o.type=='MESH']
report={'installed':False,'status':'MODULE_REVIEW','sources':{},'objects':[],'material_workflow':'specular-gloss; conversion pending','excluded_from_export':['model_17 (no UV)','model_25 (different scale, candidate duplicate model_21)']}
for f in (a.source_build/'source').iterdir():
 if f.is_file():report['sources'][f.name]=hashlib.sha256(f.read_bytes()).hexdigest()
for im in bpy.data.images:
 f=a.source_build/'source'/Path(im.filepath.replace('\\','/')).name
 if f.exists():im.filepath=str(f)
for o in original:
 o.data.transform(o.matrix_world);o.matrix_world.identity()
 o['source_object']=o.name;o['export_ready']=False
 bm=bmesh.new();bm.from_mesh(o.data)
 bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-7)
 bm.to_mesh(o.data);bm.free()
 issues=prepare_export_mesh(o)
 row={'name':o.name,'uv':bool(o.data.uv_layers),'issues':issues,'custom_normals':mesh_has_custom_normals(o.data),'parts':[]}
 bpy.ops.object.select_all(action='DESELECT');o.select_set(True);bpy.context.view_layer.objects.active=o
 bpy.ops.object.mode_set(mode='EDIT');bpy.ops.mesh.select_all(action='SELECT');bpy.ops.mesh.separate(type='LOOSE');bpy.ops.object.mode_set(mode='OBJECT')
 parts=list(bpy.context.selected_objects)
 for j,part in enumerate(sorted(parts,key=lambda x:len(x.data.polygons),reverse=True)):
  part.name=row['name']+f'_part{j:03d}';part['source_object']=row['name'];part['export_ready']=False
  lo,hi=world_bbox([part]);part.hide_render=True
  row['parts'].append({'name':part.name,'faces':len(part.data.polygons),'min':list(lo),'max':list(hi)})
 report['objects'].append(row)
setup_render(480,'OBJECT');scene=bpy.context.scene
cam_data=bpy.data.cameras.new('ModuleCamera');cam_data.type='ORTHO';cam=bpy.data.objects.new('ModuleCamera',cam_data);scene.collection.objects.link(cam);scene.camera=cam
for row in report['objects']:
 parts=[bpy.data.objects[p['name']] for p in row['parts']]
 for o in parts:o.hide_render=False;o.color=(.45,.48,.52,1)
 lo,hi=world_bbox(parts);target=(lo+hi)/2;span=max(hi-lo);cam_data.ortho_scale=span*1.15;cam_data.clip_end=max(100,span*10)
 cam.location=target+Vector((0,-3,.5))*span;cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler()
 scene.render.filepath=str(a.output/(row['name']+'.png'));bpy.ops.render.render(write_still=True)
 for o in parts:o.hide_render=True
bpy.ops.wm.save_as_mainfile(filepath=str(a.output/'HK416_modules_review.blend'))
(a.output/'modules.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print('HK416 REVIEW',len(report['objects']),'source meshes',sum(len(r['parts']) for r in report['objects']),'islands')
