"""Blender: --references DIR --textures DIR --output DIR.
Reconstruct editable NIArms reference assemblies with authored face bindings.
Preview only: source diffuse, no invented metallic map or runtime install.
"""
import argparse,json,sys
from pathlib import Path
import bpy,bmesh
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parent))
from _read_hk416_mlod import read
from _ja3_mesh_prepare import triangulate_without_custom_normals
from _prepare_weapon_open_surfaces import prepare_export_mesh
p=argparse.ArgumentParser()
for k in ('references','textures','output'):p.add_argument('--'+k,type=Path,required=True)
a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);a.output.mkdir(parents=True,exist_ok=True)
bpy.ops.wm.read_factory_settings(use_empty=True)
scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.device='CPU';scene.cycles.samples=16
scene.render.resolution_x=1200;scene.render.resolution_y=480;scene.render.resolution_percentage=100
scene.render.film_transparent=True;scene.view_settings.view_transform='Standard';scene.view_settings.look='None'
world=bpy.data.worlds.new('ReviewWorld');world.use_nodes=True;world.node_tree.nodes.get('Background').inputs['Strength'].default_value=.5;scene.world=world
cam_data=bpy.data.cameras.new('AssemblyCamera');cam_data.type='ORTHO';camera=bpy.data.objects.new('AssemblyCamera',cam_data);scene.collection.objects.link(camera);scene.camera=camera
for pos in [(1,-2,2),(-1,1,1)]:
 light=bpy.data.lights.new('ReviewLight','AREA');light.energy=100;light.size=2;o=bpy.data.objects.new('ReviewLight',light);scene.collection.objects.link(o);o.location=pos;o.rotation_euler=(-o.location).to_track_quat('-Z','Y').to_euler()
textures={p.name.lower():p for p in a.textures.glob('*.png')};materials={};report={}
for path in sorted(a.references.glob('*.p3d')):
 r=read(path);variant=path.stem;groups={};missing=set();parts=[]
 proxyfaces={i for n,s in r['selections'].items() if n.lower().startswith('proxy:') or n=='zasleh' for i in s['faces']}
 selections={n:set(v['faces']) for n,v in r['selections'].items()}
 for i,f in enumerate(r['faces']):
  if i in proxyfaces or not f['texture']:continue
  tex=Path(f['texture'].replace('\\','/')).stem
  module='Body'
  for label,slot in [('416_light Stock','Stock'),('416_SBRBarrel','Barrel'),('Break','Muzzle'),('Frontpost','FrontSight'),('Rearsight','RearSight')]:
   if i in selections.get(label,set()):module=slot;break
  groups.setdefault((module,tex),[]).append(f)
 for (module,tex),faces in groups.items():
  ids=sorted({i for f in faces for i in f['vertices']});mapping={old:i for i,old in enumerate(ids)}
  # Source weapon X longitudinal, Y vertical, Z lateral -> Blender Z vertical.
  points=[(r['vertices'][i][0],r['vertices'][i][2],r['vertices'][i][1]) for i in ids]
  # MLOD uses the opposite visible-face convention. The Y/Z reflection already
  # changes handedness: reversing indices again made open exterior panels face
  # inward. Keep corner order and UV pairing; outward recalc handles closed shells.
  mesh=bpy.data.meshes.new(variant+'_'+module+'_'+tex);mesh.from_pydata(points,[],[[mapping[i] for i in f['vertices']] for f in faces]);mesh.update()
  uv=mesh.uv_layers.new(name='UVMap')
  for poly,f in zip(mesh.polygons,faces):
   for loop,coord in zip(poly.loop_indices,f['uv']):uv.data[loop].uv=coord
  obj=bpy.data.objects.new(mesh.name,mesh);scene.collection.objects.link(obj);parts.append(obj);obj['source_p3d']=path.name;obj['module']=module;obj['material_binding']='authored P3DM face';obj['export_ready']=False
  imagepath=textures.get((tex+'.png').lower()) or textures.get((tex+'.tga.png').lower())
  if tex not in materials:
   mat=bpy.data.materials.new(tex);mat.use_nodes=True;n=mat.node_tree.nodes;b=n.get('Principled BSDF');b.inputs['Roughness'].default_value=.65
   if imagepath:
    image=bpy.data.images.load(str(imagepath),check_existing=True);image.colorspace_settings.name='sRGB';node=n.new('ShaderNodeTexImage');node.image=image;mat.node_tree.links.new(node.outputs['Color'],b.inputs['Base Color'])
   else:missing.add(tex);b.inputs['Base Color'].default_value=(.5,0,.5,1)
   materials[tex]=mat
  obj.data.materials.append(materials[tex])
  # Preserve authored hard boundaries with disconnected topology, not custom normals.
  sharp={tuple(sorted((mapping[x],mapping[y]))) for x,y in r['sharp_edges'] if x in mapping and y in mapping}
  for edge in mesh.edges:edge.use_edge_sharp=tuple(sorted(edge.vertices)) in sharp
  bpy.ops.object.select_all(action='DESELECT');obj.select_set(True);bpy.context.view_layer.objects.active=obj
  split=obj.modifiers.new('Authored hard boundaries','EDGE_SPLIT');split.use_edge_angle=False;split.use_edge_sharp=True
  bpy.ops.object.modifier_apply(modifier=split.name)
  obj['authored_sharp_edges']=len(sharp)
  triangulate_without_custom_normals(obj);issues=prepare_export_mesh(obj,strict=False)
  bad={issue['triangle'] for issue in issues if issue['kind'] in ('degenerate','zero_normal') and issue.get('triangle') is not None}
  if bad:
   bm=bmesh.new();bm.from_mesh(obj.data);bm.faces.ensure_lookup_table();bmesh.ops.delete(bm,geom=[bm.faces[i] for i in bad],context='FACES');bm.to_mesh(obj.data);bm.free()
  obj['removed_degenerate_faces']=len(bad)
  issues=prepare_export_mesh(obj);assert not issues,(obj.name,issues)
 bounds=[o.matrix_world@Vector(v) for o in parts for v in o.bound_box];lo=Vector([min(v[k] for v in bounds) for k in range(3)]);hi=Vector([max(v[k] for v in bounds) for k in range(3)]);target=(lo+hi)/2
 cam_data.ortho_scale=max(hi.x-lo.x,(hi.z-lo.z)*2.5)*1.15;camera.location=target+Vector((0,-2,.15));camera.rotation_euler=(target-camera.location).to_track_quat('-Z','Y').to_euler()
 scene.render.filepath=str(a.output/(variant+'_assembly.png'));bpy.ops.render.render(write_still=True)
 report[variant]={'objects':[o.name for o in parts],'modules':sorted({o['module'] for o in parts}),'missing_textures':sorted(missing),'bounds_min':list(lo),'bounds_max':list(hi),'preview_material':'diffuse only; roughness placeholder, no final RM','proxies_excluded':len(proxyfaces)}
 for o in parts:o.hide_render=True;o.hide_set(True)
bpy.ops.wm.save_as_mainfile(filepath=str(a.output/'HK416_authored_assemblies.blend'))
(a.output/'assemblies.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print('PASS assemblies',len(report))
