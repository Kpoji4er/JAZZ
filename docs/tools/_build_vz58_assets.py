"""Build VZ58 native modular entities from supplied OBJ/PBR archives.
Blender --background --python this.py -- --build DIR --game-root DIR
Reads build/source/{classic,modern}; exports FBX, previews, audit and native textures.
"""
import argparse,json,sys,math
from pathlib import Path
import bpy,bmesh,numpy as np
from mathutils import Matrix,Vector
sys.path.insert(0,str(Path(__file__).resolve().parent))
from _export_m14_family_assets import load_hge,pixels,save_tga,assign_hge_maps
from _prepare_weapon_open_surfaces import prepare_export_mesh
from _render_ak103_icon import build_compositor
from _weapon_material_finish import finish_material
p=argparse.ArgumentParser();p.add_argument('--build',type=Path,required=True);p.add_argument('--game-root',type=Path,required=True);a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
for sub in ['rigged','Textures','previews']:(a.build/sub).mkdir(exist_ok=True)
bpy.ops.wm.read_factory_settings(use_empty=True);hge=load_hge(a.game_root)
S=.845/(42.41209411621094+42.3818244934082)
M=Matrix(((S,0,0,0),(0,0,-S,-15*S),(0,S,0,7*S),(0,0,0,1)))
def point(x,y,z):return M@Vector((x,y,z))
spots={k:point(*v) for k,v in {'Stock':(0,-1,-19),'Handguard':(0,0,13),'Handgrip':(0,-7,-15),'Magazine':(0,-4,5),'Muzzle':(0,0,42.4),'Scope':(0,3.5,13),'Under':(0,-3.5,13),'Trigger':(0,-4,-9),'Hand_l_grip':(0,-4,13),'MuzzleTip':(0,0,42.4)}.items()}
materials={};report={'scale':S,'source_length_m':.845,'entities':{},'spots':{k:list(v) for k,v in spots.items()}}
def material(family,prefix,key,base_only=False):
 if key in materials:return materials[key]
 paths=sorted((a.build/'source'/family).glob(prefix+'*.png'))
 assert paths,(family,prefix)
 def lookup(tokens):return next((p for p in paths if any(t in p.name[len(prefix):] for t in tokens)),None)
 base=paths[0] if base_only else lookup(['Base','_Bas','_Ba.png']);normal=lookup(['Normal','_Nor','_No.png']);rough=lookup(['Rough','_Rou','_Ro.png']);metal=lookup(['Metal','_Met','_Me.png'])
 assert base,(prefix,paths)
 override=a.build/'material-overrides'/(key+'_Base.png')
 maps={'Base':pixels(override if override.exists() else base)};rm=np.ones_like(maps['Base']);rm[:,:,0]=pixels(rough)[:,:,0] if rough else .65;rm[:,:,1]=0;rm[:,:,2]=pixels(metal)[:,:,0] if metal else .7
 if override.exists():
  # Atlas overrides are authored sRGB. save_tga(color=True) expects linear pixels.
  rgb=maps['Base'][:,:,:3];maps['Base'][:,:,:3]=np.where(rgb<=.04045,rgb/12.92,((rgb+.055)/1.055)**2.4)
 if key in ('Wood','StockWood'):
  # Matte phenolic furniture; keep authored metal fittings' PBR unchanged.
  wood=rm[:,:,2]<.5
  rm[:,:,0][wood]=np.maximum(rm[:,:,0][wood],.72)
 maps['RM']=rm
 if base_only:
  # The wire-stock archive supplies one near-white scalar texture and no color/PBR set.
  # Keep it as occlusion; use explicit neutral gunmetal instead of a white albedo.
  maps['AO']=maps['Base'].copy();maps['Base']=np.ones_like(maps['AO']);maps['Base'][:,:,:3]=(.18,.19,.20)
 if normal:
  maps['Normal']=pixels(normal)
  if 'DirectX' in normal.name:maps['Normal'][:,:,1]=1-maps['Normal'][:,:,1]
  if key in ('Steel','Mag','Wood','StockWood'):
   maps['Normal'],maps['RM'],_=finish_material(maps['Normal'],maps['RM'],'vz58',key)
 images={k:save_tga('JAZZ_VZ58_'+key+'_'+k,v,a.build/'Textures',k=='Base') for k,v in maps.items()}
 mat=bpy.data.materials.new('JAZZ_VZ58_'+key);mat.use_nodes=True;nodes=mat.node_tree.nodes;links=mat.node_tree.links;shader=nodes.get('Principled BSDF')
 for kind,im in images.items():
  n=nodes.new('ShaderNodeTexImage');n.image=im
  if kind=='Base':links.new(n.outputs['Color'],shader.inputs['Base Color'])
  elif kind=='Normal':
   nm=nodes.new('ShaderNodeNormalMap');links.new(n.outputs['Color'],nm.inputs['Color']);links.new(nm.outputs['Normal'],shader.inputs['Normal'])
  elif kind=='RM':
   sep=nodes.new('ShaderNodeSeparateColor');links.new(n.outputs['Color'],sep.inputs['Color']);links.new(sep.outputs['Red'],shader.inputs['Roughness']);links.new(sep.outputs['Blue'],shader.inputs['Metallic'])
 assign_hge_maps(hge,mat,images);materials[key]=mat;return mat
mats={
 'Steel':material('classic','SA_vz.58_(TextureReady)_Steel_Body','Steel'),
 'Wood':material('classic','SA_vz.58_(TextureReady)_Wood_Front','Wood'),
 'StockWood':material('classic','SA_vz.58_(TextureReady)_Wood_Back_Stock','StockWood'),
 'Wire':material('classic','SA_vz.58_Metal_Stock','Wire',True),
 'Mag':material('classic','SA_vz.58_(TextureReady)_Mag_and_Bullet','Mag'),
 'StockModern':material('modern','Stock,Grip_CZX','StockModern'),
 'RIS':material('modern','Gun_Expert_Foregrip','RIS'),
 'Attachments':material('modern','Attatchemnts','Attachments'),
 'MagLoop':material('modern','Mag_Grip','MagLoop'),
 'Suppressor':material('modern','SA_vz.58_Suppressor','Suppressor')}
objects={}
def part(name,family,index,mat,slot=None,shift=0,predicate=None,island_filter=None):
 bpy.ops.wm.obj_import(filepath=str(a.build/'source'/family/f'model_{index}.obj'),forward_axis='Y',up_axis='Z');o=bpy.context.object;o.name='JAZZ_VZ58'+('_'+name if name!='Body' else '')
 bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.triangulate(bm,faces=list(bm.faces));bm.normal_update()
 # OBJ triangle-strip conversion emits degenerate linking faces. Remove them before any selection.
 bad=[f for f in bm.faces if f.calc_area()<1e-8];bmesh.ops.delete(bm,geom=bad,context='FACES_ONLY')
 if island_filter:
  pending=set(bm.faces);discard=[]
  while pending:
   seed=pending.pop();component={seed};todo=[seed]
   while todo:
    face=todo.pop()
    for edge in face.edges:
     for other in edge.link_faces:
      if other in pending:pending.remove(other);component.add(other);todo.append(other)
   vertices={v for f in component for v in f.verts}
   low=Vector(tuple(min(v.co[i] for v in vertices) for i in range(3)));high=Vector(tuple(max(v.co[i] for v in vertices) for i in range(3)))
   if not island_filter(low,high):discard.extend(component)
  bmesh.ops.delete(bm,geom=discard,context='FACES_ONLY')
 for v in bm.verts:v.co.y+=shift
 if predicate:
  bad=[f for f in bm.faces if not predicate(f.calc_center_median())];bmesh.ops.delete(bm,geom=bad,context='FACES_ONLY')
 loose=[v for v in bm.verts if not v.link_faces];bmesh.ops.delete(bm,geom=loose,context='VERTS')
 # OBJ splits geometric vertices at UV seams; independent normal recalculation
 # flips disconnected surface strips. Join only coincident source positions
 # (0.1 micrometre in game units); loop UVs remain independently stored.
 face_count=len(bm.faces);bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-5)
 assert len(bm.faces)==face_count,(name,'weld changed surface triangle count')
 bm.to_mesh(o.data);bm.free()
 assert len(o.data.polygons)>0,name
 o.data.transform(M);o.data.materials.clear();o.data.materials.append(mats[mat]);o.matrix_world=Matrix.Identity(4)
 for f in o.data.polygons:f.material_index=0
 prepare_export_mesh(o)
 loc=spots[slot] if slot else Vector((0,0,0));o.data.transform(Matrix.Translation(-loc));o.location=loc
 settings=o.hge_obj_settings;settings.entity=o.name;settings.mesh='Mesh';settings.state='idle';settings.lod=1;settings.ignore=False;o.hge_export=True
 o.data.calc_loop_triangles();report['entities'][o.name]={'source':f'{family}/model_{index}.obj','triangles':len(o.data.loop_triangles),'slot':slot,'origin':list(loc),'custom_normals':o.data.has_custom_normals,'uv_layers':len(o.data.uv_layers)};objects[name]=o;return o
# Lower display rifle is the P, centered -9.60989 source units; upper V +20.50681.
body=part('Body','classic',2,'Steel',shift=9.60988998413086,predicate=lambda c:c.y<10)
part('StockWood','classic',5,'StockWood','Stock',shift=9.60988998413086)
part('StockWire','classic',0,'Wire','Stock',shift=-20.50680923461914)
from _build_vz58_folding import folded_copy
objects['StockWireFolded'],fold_report=folded_copy(objects['StockWire'])
report['folding']=fold_report
part('HandguardWood','classic',3,'Wood','Handguard',shift=9.60988998413086,predicate=lambda c:c.y<8 and c.z>0)
part('GripWood','classic',3,'Wood','Handgrip',shift=9.60988998413086,predicate=lambda c:c.y<0 and c.z<0)
# Mounted magazine in Modernized is identical to classic P and already centered.
part('Magazine','modern',0,'Mag','Magazine')
part('MagLoop','modern',2,'MagLoop','Magazine')
part('StockModern','modern',5,'StockModern','Stock',island_filter=lambda lo,hi:not (lo.z>-19 and hi.y<-3.10))
part('GripModern','modern',5,'StockModern','Handgrip',island_filter=lambda lo,hi:lo.z>-19 and hi.y<-3.10)
part('HandguardRIS','modern',3,'RIS','Handguard')
# The little front retainer remains in both furniture variants.
part('Retainer','modern',4,'Wood')
part('Foregrip','modern',6,'Attachments','Under',predicate=lambda c:c.y<0)
part('Reflex','modern',6,'Attachments','Scope',predicate=lambda c:c.y>=0)
part('Suppressor','modern',7,'Suppressor','Muzzle')
# Retainer is already part of the wood handguard; merge it only into the RIS.
def join_into(dest,src):
 d=objects[dest];s=objects[src];bpy.ops.object.select_all(action='DESELECT');d.select_set(True);s.select_set(True);bpy.context.view_layer.objects.active=d;bpy.ops.object.join();del objects[src];report['entities'].pop('JAZZ_VZ58_'+src);prepare_export_mesh(d)
join_into('HandguardRIS','Retainer')
# Quick magazine is a complete native magazine plus its pull loop, never an AK mesh.
mag=objects['Magazine'];clone=mag.copy();clone.data=mag.data.copy();bpy.context.collection.objects.link(clone);clone.name='JAZZ_VZ58_MagQuick';objects['MagQuick']=clone
join_into('MagQuick','MagLoop');clone.hge_obj_settings.entity=clone.name
# Export each entity at its local origin; attachment coordinates restore the exact source assembly.
for key,o in objects.items():
 loc=o.location.copy();o.location=(0,0,0)
 origin=bpy.data.objects.new(o.name+'_Origin',None);bpy.context.collection.objects.link(origin);o.parent=origin
 if key=='Body':
  for name,where in spots.items():
   e=bpy.data.objects.new(name,None);bpy.context.collection.objects.link(e);e.parent=o;e.location=where;e.hge_obj_settings.spot_name=name
 if key=='Suppressor':
  e=bpy.data.objects.new('MuzzleTip',None);bpy.context.collection.objects.link(e);e.parent=o;e.location=point(0,0,58.89)-loc;e.hge_obj_settings.spot_name='MuzzleTip'
 bpy.ops.object.select_all(action='DESELECT');o.select_set(True);origin.select_set(True)
 for child in o.children:child.select_set(True)
 filename=a.build/'rigged'/(o.name+'.fbx')
 with hge.ObjectNamesExportContext(bpy.context):
  bpy.ops.export_scene.fbx(filepath=str(filename),use_selection=True,axis_forward='Y',axis_up='Z',apply_scale_options='FBX_SCALE_ALL',object_types={'MESH','EMPTY'},use_custom_props=True,add_leaf_bones=False,bake_anim=False)
 o.location=loc;o.data.calc_loop_triangles();report['entities'].setdefault(o.name,{}).update(triangles=len(o.data.loop_triangles),custom_normals=o.data.has_custom_normals)
bpy.ops.wm.save_as_mainfile(filepath=str(a.build/'rigged/VZ58_JA3.blend'))
(a.build/'build-report.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.samples=24;scene.render.film_transparent=True;scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGBA';scene.view_settings.view_transform='Standard';scene.view_settings.look='None'
scene.world=bpy.data.worlds.new('World');scene.world.use_nodes=True;scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.35
cam=bpy.data.cameras.new('Camera');cam.type='ORTHO';camera=bpy.data.objects.new('Camera',cam);scene.collection.objects.link(camera);scene.camera=camera
for i,offset in enumerate([(-1,-.5,1.5),(-.5,.5,1),(1,1,0)]):
 light=bpy.data.lights.new('Light'+str(i),'AREA');light.energy=25;light.size=1.5;o=bpy.data.objects.new(light.name,light);scene.collection.objects.link(o);o.location=Vector(offset);o.rotation_euler=(-o.location).to_track_quat('-Z','Y').to_euler()
configs={'wire-folded':['Body','StockWireFolded','HandguardWood','GripWood','Magazine'],'classic':['Body','StockWood','HandguardWood','GripWood','Magazine'],'wire':['Body','StockWire','HandguardWood','GripWood','Magazine'],'modern':['Body','StockModern','HandguardRIS','GripModern','MagQuick','Foregrip','Reflex','Suppressor']}
for config,names in configs.items():
 for name,o in objects.items():o.hide_render=name not in names
 pts=[o.matrix_world@Vector(v) for n,o in objects.items() if n in names for v in o.bound_box];target=Vector(tuple((min(v[i] for v in pts)+max(v[i] for v in pts))/2 for i in range(3)))
 for view,direction in [('side',(-2,0,.04)),('threequarter',(-2,-1,.65))]:
  scene.render.resolution_x=1400;scene.render.resolution_y=600;scene.render.resolution_percentage=100;cam.ortho_scale=1.12;camera.location=target+Vector(direction);camera.rotation_euler=(target-camera.location).to_track_quat('-Z','Y').to_euler();scene.render.filepath=str(a.build/'previews'/f'{config}-{view}.png');bpy.ops.render.render(write_still=True)
 if config=='classic':
  camera.location=target+Vector((-2,0,0));camera.rotation_euler=(target-camera.location).to_track_quat('-Z','Y').to_euler()
  build_compositor(scene);scene.render.resolution_x=324;scene.render.resolution_y=165;cam.ortho_scale=1.02;scene.render.filepath=str(a.build/'VZ58_icon.png');bpy.ops.render.render(write_still=True);scene.use_nodes=False
print('VZ58 export and previews complete')
