"""Blender HK416 candidate: --reference-blend FILE --source DIR --build DIR --game-root DIR.
Source diffuse/normal unchanged; explicit legacy Super roughness adaptation.
"""
import argparse,json,sys,math
from pathlib import Path
import bpy,bmesh,numpy as np
from mathutils import Matrix,Vector
sys.path.insert(0,str(Path(__file__).resolve().parent))
from _export_m14_family_assets import load_hge,pixels,save_tga,assign_hge_maps
from _prepare_weapon_open_surfaces import prepare_export_mesh
from _ja3_mesh_prepare import triangulate_without_custom_normals
from _render_ak103_icon import build_compositor
p=argparse.ArgumentParser()
for k in ('reference-blend','source','build','game-root'):p.add_argument('--'+k,type=Path,required=True)
a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
for n in ('Textures','clean','rigged','previews'):(a.build/n).mkdir(parents=True,exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(a.reference_blend),use_scripts=False);hge=load_hge(a.game_root)
sources=list(bpy.data.objects);created={};report={'entities':{},'materials':{},'material_adaptation':'painted dielectric (metal=0), perceptual roughness=(2/(100*gloss+2))^0.25; original CO/NM; runtime review required'}
transform=Matrix(((0,-1,0,0),(1,0,0,-.06),(0,0,1,.04),(0,0,0,1)))
def copy_join(names,name):
 obs=[]
 for source in names:
  o=source.copy();o.data=source.data.copy();o.hide_render=False;o.hide_viewport=False;bpy.context.collection.objects.link(o);o.hide_set(False);o.data.transform(o.matrix_world);o.matrix_world=Matrix.Identity(4);o.data.transform(transform);obs.append(o)
 assert obs,name
 bpy.ops.object.select_all(action='DESELECT')
 for o in obs:o.select_set(True)
 bpy.context.view_layer.objects.active=obs[0]
 if len(obs)>1:bpy.ops.object.join()
 o=obs[0];o.name=name;created[name]=o;return o
for variant,ref in [('Short','416D10'),('Standard','416D145'),('Long','416D20')]:
 copy_join([o for o in sources if o.type=='MESH' and o.name.startswith(ref+'_') and o.get('source_p3d')==ref+'.p3d' and o.get('module')!='Stock'],'JAZZ_HK416_'+variant)
copy_join([o for o in sources if o.type=='MESH' and o.get('source_p3d')=='416D145.p3d' and o.get('module')=='Stock'],'JAZZ_HK416_Stock')
# CTR is a separate authored material section in the ST6 reference.
ctr=[o for o in sources if o.type=='MESH' and o.get('source_p3d')=='416D10_ST6.p3d' and any('ctr' in m.name.lower() for m in o.data.materials)]
copy_join(ctr,'JAZZ_HK416_StockCTR')
# Owner archive STANAG geometry; preserve its UV. Fit top centre to authored magazine proxy.
v=[];uv=[];faces=[];fuv=[]
for line in (a.source/'model_24.obj').read_text().splitlines():
 q=line.split()
 if q and q[0]=='v':v.append(tuple(map(float,q[1:4])))
 elif q and q[0]=='vt':uv.append(tuple(map(float,q[1:3])))
 elif q and q[0]=='f':
  faces.append([int(t.split('/')[0])-1 for t in q[1:]]);fuv.append([int(t.split('/')[1])-1 for t in q[1:]])
vv=np.array(v);mid=(vv.min(0)+vv.max(0))/2;feed_z=vv[:,2].min()
# This detached OBJ is upside down: its straight feed section is at minimum Z.
# Rotate 180 degrees about the lateral axis relative to the previous candidate.
# The straight section enters the well; the curved section points toward muzzle.
feed=vv[vv[:,2]<feed_z+.04];feed_x=(feed[:,0].min()+feed[:,0].max())/2
points=[(float(y-mid[1]),float(x-feed_x-.04),float(feed_z-z+.102)) for x,y,z in v]
mesh=bpy.data.meshes.new('STANAG');mesh.from_pydata(points,[],faces);mesh.update();layer=mesh.uv_layers.new(name='UVMap')
for poly,ids in zip(mesh.polygons,fuv):
 for loop,i in zip(poly.loop_indices,ids):layer.data[loop].uv=uv[i]
mag=bpy.data.objects.new('JAZZ_HK416_Magazine',mesh);bpy.context.collection.objects.link(mag);created[mag.name]=mag
mat=bpy.data.materials.new('STANAG_HeavyDuty_co.tga');mag.data.materials.append(mat)
for o in sources:
 if o.type=='MESH':bpy.data.objects.remove(o,do_unlink=True)
files={f.name.lower():f for f in a.source.glob('*.png')};converted={}
for o in created.values():
 for index,old in enumerate(o.data.materials):
  if old.name not in converted:
   name=old.name;prefix=name.lower().rsplit('_co',1)[0]
   def find(kind):
    matches=[f for n,f in files.items() if n in (prefix+'_'+kind+'.png',prefix+'_'+kind+'.tga.png')]
    return matches[0] if matches else None
   base=find('co');normal=find('nohq') or find('normals');gloss=find('gloss');assert base and normal and gloss,(name,base,normal,gloss)
   bc=pixels(base);nm=pixels(normal);g=pixels(gloss)[:,:,0];rm=np.ones_like(bc);rm[:,:,0]=(2/(100*g+2))**.25;rm[:,:,1]=rm[:,:,0];rm[:,:,2]=0
   maps={'Base':bc,'Normal':nm,'RM':rm};ao=find('as')
   if ao:
    arr=pixels(ao);arr[:,:,:3]=arr[:,:,1:2];maps['AO']=arr
   images={key:save_tga('HK416_'+prefix+'_'+key,arr,a.build/'Textures',key=='Base') for key,arr in maps.items()}
   for im in images.values():im.source='FILE';im.reload()
   new=bpy.data.materials.new('HK416_'+prefix);new.use_nodes=True;nodes=new.node_tree.nodes;links=new.node_tree.links;bs=nodes.get('Principled BSDF')
   for key,im in images.items():
    n=nodes.new('ShaderNodeTexImage');n.image=im
    if key=='Base':links.new(n.outputs['Color'],bs.inputs['Base Color']);nodes.active=n
    elif key=='Normal':t=nodes.new('ShaderNodeNormalMap');links.new(n.outputs['Color'],t.inputs['Color']);links.new(t.outputs['Normal'],bs.inputs['Normal'])
    elif key=='RM':t=nodes.new('ShaderNodeSeparateColor');links.new(n.outputs['Color'],t.inputs['Color']);links.new(t.outputs['Red'],bs.inputs['Roughness']);links.new(t.outputs['Blue'],bs.inputs['Metallic'])
   assign_hge_maps(hge,new,images);converted[name]=new;report['materials'][name]={'base':base.name,'normal':normal.name,'gloss':gloss.name}
  o.data.materials[index]=converted[old.name]
for name,o in created.items():
 triangulate_without_custom_normals(o);issues=prepare_export_mesh(o,strict=False)
 bad={i['triangle'] for i in issues if i['kind'] in ('degenerate','zero_normal') and i.get('triangle') is not None}
 if bad:
  bm=bmesh.new();bm.from_mesh(o.data);bm.faces.ensure_lookup_table();bmesh.ops.delete(bm,geom=[bm.faces[i] for i in bad],context='FACES');bm.to_mesh(o.data);bm.free()
 assert not prepare_export_mesh(o)
 origin=bpy.data.objects.new(name+'_Origin',None);bpy.context.collection.objects.link(origin);o.parent=origin
 s=o.hge_obj_settings;s.entity=name;s.mesh='Mesh';s.state='idle';s.lod=1;s.ignore=False;o.hge_export=True
 if name.split('_')[-1] in ('Short','Standard','Long'):
  muzzle=min(v.co.y for v in o.data.vertices)
  spots={'Magazine':(0,0,0),'Stock':(0,0,0),'Barrel':(0,0,0),'Scope':(0,-.05,.145),'Mount':(0,-.05,.145),'Under':(0,-.24,.077),'Side':(-.033,-.25,.11),'Muzzle':(0,muzzle,.105),'MuzzleTip':(0,muzzle,.105),'Trigger':(0,0,.015),'Hand_l_grip':(0,-.24,.09)}
  for label,pos in spots.items():
   sp=bpy.data.objects.new(label,None);bpy.context.collection.objects.link(sp);sp.parent=o;sp.location=pos;sp.hge_obj_settings.spot_name=label
 report['entities'][name]={'triangles':len(o.data.polygons),'custom_normals':o.data.has_custom_normals,'removed_degenerate':len(bad)}
bpy.ops.wm.save_as_mainfile(filepath=str(a.build/'clean/HK416.blend'))
for name,o in created.items():
 bpy.ops.object.select_all(action='DESELECT');o.select_set(True);o.parent.select_set(True)
 for child in o.children:child.select_set(True)
 with hge.ObjectNamesExportContext(bpy.context):bpy.ops.export_scene.fbx(filepath=str(a.build/'rigged'/(name+'.fbx')),use_selection=True,axis_forward='Y',axis_up='Z',apply_scale_options='FBX_SCALE_ALL',object_types={'MESH','EMPTY'},use_custom_props=True,add_leaf_bones=False,bake_anim=False)
bpy.ops.wm.save_as_mainfile(filepath=str(a.build/'rigged/HK416_JA3.blend'))
(a.build/'build-report.json').write_text(json.dumps(report,indent=2))
scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.device='CPU';scene.cycles.samples=24;scene.render.film_transparent=True;scene.render.image_settings.color_mode='RGBA';scene.view_settings.view_transform='Standard'
cam=scene.camera;cam.data.type='ORTHO';cam.data.ortho_scale=1.12;target=Vector((0,-.15,0));cam.location=target+Vector((-2,0,.12));cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler()
build_compositor(scene)
for variant in ('Short','Standard','Long'):
 for ctr in (False,True):
  for o in created.values():o.hide_render=o.name not in ('JAZZ_HK416_'+variant,'JAZZ_HK416_StockCTR' if ctr else 'JAZZ_HK416_Stock','JAZZ_HK416_Magazine')
  for icon in (False,True):
   scene.use_nodes=icon;scene.render.resolution_x=324 if icon else 1400;scene.render.resolution_y=165 if icon else 650;scene.render.filepath=str(a.build/'previews'/('HK416_'+variant+('_CTR' if ctr else '')+('_icon' if icon else '_pbr')+'.png'));bpy.ops.render.render(write_still=True)
print('HK416_BUILD',len(created),'entities')
