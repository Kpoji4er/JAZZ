"""Blender AEK author-PBR build. --batch-root DIR --build NEW_DIR --game-root DIR.
Creates two complete configurations with native magazines and movable stocks.
Input OBJ/PNG files remain untouched; no active mod writes.
"""
import argparse,hashlib,json,math,sys
from pathlib import Path
import bpy,bmesh,numpy as np
from mathutils import Matrix,Vector
sys.path.insert(0,str(Path(__file__).resolve().parent))
from _export_m14_family_assets import load_hge,pixels,save_tga,assign_hge_maps
from _prepare_weapon_open_surfaces import prepare_export_mesh
from _weapon_material_finish import separate_hard_edges
from _render_ak103_icon import build_compositor
p=argparse.ArgumentParser()
for k in ('batch-root','build','game-root'):p.add_argument('--'+k,type=Path,required=True)
a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
for folder in ('clean','rigged','Textures','previews'):(a.build/folder).mkdir(parents=True,exist_ok=True)
bpy.ops.wm.read_factory_settings(use_empty=True);hge=load_hge(a.game_root)
report={'materials':{},'entities':{},'sources':{},'configurations':{}}
def material(source,prefix,name):
 maps={k:pixels(source/(prefix+'_'+suffix+'.png')) for k,suffix in [('Base','BaseColor'),('Normal','Normal'),('Rough','Roughness'),('Metal','Metallic')]}
 rm=np.ones_like(maps['Base']);rm[:,:,0]=maps['Rough'][:,:,0];rm[:,:,1]=rm[:,:,0];rm[:,:,2]=maps['Metal'][:,:,0]
 # pixels() reads encoded source bytes as Non-Color; save_tga preserves them.
 # Decoding sRGB here darkens the saved TGA a second time in the game shader.
 images={k:save_tga(name+'_'+k,v,a.build/'Textures',k=='Base') for k,v in {'Base':maps['Base'],'Normal':maps['Normal'],'RM':rm}.items()}
 # Preview must read the saved sRGB file, not the generated image's raw buffer.
 images['Base'].source='FILE';images['Base'].reload()
 mat=bpy.data.materials.new(name);mat.use_nodes=True;nodes=mat.node_tree.nodes;links=mat.node_tree.links;bsdf=nodes.get('Principled BSDF')
 for k,im in images.items():
  node=nodes.new('ShaderNodeTexImage');node.image=im
  if k=='Base':links.new(node.outputs['Color'],bsdf.inputs['Base Color']);nodes.active=node
  elif k=='Normal':
   nm=nodes.new('ShaderNodeNormalMap');links.new(node.outputs['Color'],nm.inputs['Color']);links.new(nm.outputs['Normal'],bsdf.inputs['Normal'])
  else:
   sep=nodes.new('ShaderNodeSeparateColor');links.new(node.outputs['Color'],sep.inputs['Color']);links.new(sep.outputs['Red'],bsdf.inputs['Roughness']);links.new(sep.outputs['Blue'],bsdf.inputs['Metallic'])
 assign_hge_maps(hge,mat,images);report['materials'][name]=prefix
 return mat

objects={};assemblies={}
for variant in ('971','973S'):
 folder='23_AEK_971_Assault_Rifle' if variant=='971' else '22_AEK_-_973S';source=a.batch_root/folder/'source'
 for f in source.iterdir():
  if f.suffix.lower() in ('.obj','.png'):report['sources'][folder+'/'+f.name]=hashlib.sha256(f.read_bytes()).hexdigest()
 if variant=='971':
  # Existing source measures 0.95488 m. Keep the ~0.96 m author proportions.
  scale=.96/(.477429777383804+.477445989847183)
  transform=Matrix(((scale,0,0,0),(0,0,scale,-.155*scale),(0,-scale,0,-.005*scale),(0,0,0,1)))
  sources=[('model_0.obj','aektexture_blue.001','Blue'),('model_1.obj','aektexture_red.002','Red')]
 else:
  scale=.96/96.2772483825684
  transform=Matrix(((0,-scale,0,2.02*scale),(scale,0,0,-43.5*scale),(0,0,scale,-228*scale),(0,0,0,1)))
  sources=[('model_0.obj','31_AEK','Main')]
 pieces={'Body':[],'Magazine':[],'Stock':[]}
 for filename,prefix,suffix in sources:
  before=set(bpy.data.objects);bpy.ops.wm.obj_import(filepath=str(source/filename));o=next(o for o in bpy.data.objects if o not in before and o.type=='MESH')
  o.data.transform(o.matrix_world);o.matrix_world=Matrix.Identity(4)
  mat=material(source,prefix,'JAZZ_AEK'+variant+'_'+suffix);o.data.materials.clear();o.data.materials.append(mat)
  for f in o.data.polygons:f.material_index=0
  bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-7)
  bm.verts.ensure_lookup_table();bm.faces.ensure_lookup_table();remaining=set(bm.verts);groups={k:set() for k in pieces}
  while remaining:
   v=remaining.pop();group={v};todo=[v]
   while todo:
    v=todo.pop()
    for e in v.link_edges:
     other=e.other_vert(v)
     if other in remaining:remaining.remove(other);group.add(other);todo.append(other)
   mn=Vector([min(v.co[i] for v in group) for i in range(3)]);mx=Vector([max(v.co[i] for v in group) for i in range(3)])
   part='Body'
   if variant=='971':
    if suffix=='Blue' and mx.y>.10:part='Magazine'
    elif suffix=='Red' and mn.z>.221:part='Stock'
   else:
    if mn.z<217 and mn.x>18 and mx.x<35:part='Magazine'
    elif mn.x>48.5:part='Stock'
   groups[part].update(f.index for v in group for f in v.link_faces)
  bm.to_mesh(o.data);bm.free()
  for part,ids in groups.items():
   if not ids:continue
   mesh=o.data.copy();cut=bmesh.new();cut.from_mesh(mesh);cut.faces.ensure_lookup_table()
   bmesh.ops.delete(cut,geom=[f for f in cut.faces if f.index not in ids],context='FACES')
   bmesh.ops.delete(cut,geom=[v for v in cut.verts if not v.link_faces],context='VERTS');cut.to_mesh(mesh);cut.free()
   obj=bpy.data.objects.new('AEK'+variant+'_'+part+'_'+suffix,mesh);bpy.context.collection.objects.link(obj);mesh.transform(transform);pieces[part].append(obj)
  bpy.data.objects.remove(o,do_unlink=True)
 parts={}
 for part,obs in pieces.items():
  assert obs,part
  bpy.ops.object.select_all(action='DESELECT')
  for o in obs:o.select_set(True)
  bpy.context.view_layer.objects.active=obs[0]
  if len(obs)>1:bpy.ops.object.join()
  o=obs[0];o.name='JAZZ_AEK'+variant+('' if part=='Body' else '_'+part)
  assert not prepare_export_mesh(o),o.name
  separate_hard_edges(o)
  assert not prepare_export_mesh(o),o.name
  parts[part]=o
 folded=parts['Stock'].copy();folded.data=folded.data.copy();bpy.context.collection.objects.link(folded);folded.name='JAZZ_AEK'+variant+'_StockFolded'
 if variant=='971':
  pivot=transform@Vector((-.02,-.06,.223));folded.data.transform(Matrix.Translation(pivot)@Matrix.Rotation(math.pi,4,'Z')@Matrix.Translation(-pivot))
 else:folded.data.transform(Matrix.Translation(Vector((0,-.19,0))))
 assert not prepare_export_mesh(folded)
 parts['StockFolded']=folded
 points=[v.co for o in parts.values() if o!=folded for v in o.data.vertices]
 miny=min(v.y for v in points);maxy=max(v.y for v in points)
 bore=transform@Vector((0,-.0735,-.47744599)) if variant=='971' else transform@Vector((-23.674,2.02,236.55))
 spots={'Magazine':(0,0,0),'Stock':(0,0,0),'Barrel':(0,0,0),'Muzzle':tuple(bore),'MuzzleTip':tuple(bore),'Trigger':(0,-.03,.005),'Hand_l_grip':(0,-.29,.025),'Scope':(0,-.09,.105),'Mount':(0,-.09,.105),'General':(0,-.09,.105)}
 report['configurations'][variant]={'length_m':maxy-miny,'spots':spots,'scale':scale}
 for part,o in parts.items():
  origin=bpy.data.objects.new(o.name+'_Origin',None);bpy.context.collection.objects.link(origin);o.parent=origin
  s=o.hge_obj_settings;s.entity=o.name;s.mesh='Mesh';s.state='idle';s.lod=1;s.ignore=False;o.hge_export=True
  if part=='Body':
   for name,loc in spots.items():
    sp=bpy.data.objects.new(name,None);bpy.context.collection.objects.link(sp);sp.parent=o;sp.location=loc;sp.hge_obj_settings.spot_name=name
  objects[o.name]=o;o.data.calc_loop_triangles();report['entities'][o.name]={'triangles':len(o.data.loop_triangles),'custom_normals':o.data.has_custom_normals}
 assemblies[variant]=parts
bpy.ops.wm.save_as_mainfile(filepath=str(a.build/'clean/AEK.blend'))
for name,o in objects.items():
 bpy.ops.object.select_all(action='DESELECT');o.select_set(True);o.parent.select_set(True)
 for child in o.children:child.select_set(True)
 with hge.ObjectNamesExportContext(bpy.context):
  bpy.ops.export_scene.fbx(filepath=str(a.build/'rigged'/(name+'.fbx')),use_selection=True,axis_forward='Y',axis_up='Z',apply_scale_options='FBX_SCALE_ALL',object_types={'MESH','EMPTY'},use_custom_props=True,add_leaf_bones=False,bake_anim=False)
bpy.ops.wm.save_as_mainfile(filepath=str(a.build/'rigged/AEK_JA3.blend'))
(a.build/'build-report.json').write_text(json.dumps(report,indent=2))
# Side/top and folded inspection use author base color; no painting or rebaking.
scene=bpy.context.scene;scene.render.engine='BLENDER_WORKBENCH';scene.display.shading.color_type='TEXTURE';scene.display.shading.light='STUDIO';scene.display.shading.show_cavity=True;scene.render.film_transparent=True;scene.render.image_settings.color_mode='RGBA';scene.view_settings.view_transform='Standard'
cam=bpy.data.cameras.new('Camera');cam.type='ORTHO';cam.ortho_scale=1.08;ob=bpy.data.objects.new('Camera',cam);scene.collection.objects.link(ob);scene.camera=ob
for variant,parts in assemblies.items():
 for folded in (False,True):
  shown=[parts['Body'],parts['Magazine'],parts['StockFolded' if folded else 'Stock']]
  for o in objects.values():o.hide_render=o not in shown
  for label,direction in [('left',Vector((-2,0,0))),('right',Vector((2,0,0))),('top',Vector((0,0,2)))]:
   center=Vector((0,-.17,.0));ob.location=center+direction;ob.rotation_euler=(-direction).to_track_quat('-Z','Y').to_euler()
   scene.render.resolution_x=1400;scene.render.resolution_y=650;scene.render.resolution_percentage=100;scene.render.filepath=str(a.build/'previews'/f'{variant}-{folded}-{label}.png');bpy.ops.render.render(write_still=True)
print('AEK_BUILD',json.dumps(report['entities']))
