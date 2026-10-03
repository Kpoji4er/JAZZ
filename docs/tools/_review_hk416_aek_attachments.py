"""Blender -- --hk-build DIR --aek-build DIR --assets DIR --reference DIR --out DIR.
Real decoded attachment geometry at export spots; flat diagnostic colours.
Workbench backface culling exposes missing exterior panels. Does not install.
"""
import argparse,json,sys,xml.etree.ElementTree as ET
from pathlib import Path
import bpy
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parent))
from _build_weapon_attachment_fit_scene import add_mesh,material
p=argparse.ArgumentParser()
for k in ('hk-build','aek-build','assets','reference','out'):p.add_argument('--'+k,type=Path,required=True)
a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);a.out.mkdir(parents=True,exist_ok=True);report=[]
for variant in ('Short','Standard','Long','971','973S'):
 hk=variant in ('Short','Standard','Long');entity='JAZZ_HK416_'+variant if hk else 'JAZZ_AEK'+variant
 bpy.ops.wm.open_mainfile(filepath=str(a.hk_build/'clean/HK416.blend' if hk else a.aek_build/'clean/AEK.blend'),use_scripts=False)
 keep={entity,'JAZZ_HK416_Stock','JAZZ_HK416_Magazine'} if hk else {entity,entity+'_Stock',entity+'_Magazine'}
 gray=material('Body',(.28,.3,.33));green=material('Optic',(.15,.55,.2));orange=material('Under',(.8,.25,.05));blue=material('Laser',(.08,.25,.8))
 for ob in bpy.context.scene.objects:
  if ob.type=='MESH':
   ob.hide_render=ob.name not in keep
   if not ob.hide_render:ob.data.materials.clear();ob.data.materials.append(gray)
 xml=(a.hk_build/'mod-assets-stage/Entities' if hk else a.assets/'Entities')/(entity+'.ent')
 spots={}
 for n in ET.parse(xml).findall('.//attach'):
  x,y,z=map(float,n.get('spot_pos').split(','));spots[n.get('name')]=Vector((-y/100,-x/100,z/100))
 optics=add_mesh(a.reference/'Geometry/WeaponAttA_ScopeCOG_mesh.json','Optic',spots['Scope'],green)
 attachments=[optics]
 if hk:
  attachments+=[add_mesh(a.reference/'Geometry/WeaponAttA_GrenadeLauncherM14_mesh.json','M203',spots['Under'],orange),add_mesh(a.reference/'Geometry/WeaponAttA_SideLaser_mesh.json','Laser',spots['Side'],blue)]
 report.append({'entity':entity,'attachments':[{'name':o.name,'spot':list(o.location),'min':[min((o.matrix_world@v.co)[i] for v in o.data.vertices) for i in range(3)],'max':[max((o.matrix_world@v.co)[i] for v in o.data.vertices) for i in range(3)]} for o in attachments]})
 sc=bpy.context.scene;sc.render.engine='BLENDER_WORKBENCH';sc.display.shading.light='STUDIO';sc.display.shading.color_type='MATERIAL';sc.display.shading.show_backface_culling=True;sc.display.shading.show_shadows=True
 sc.render.resolution_x=1400;sc.render.resolution_y=700;sc.render.resolution_percentage=100;sc.render.film_transparent=False;sc.use_nodes=False
 sc.render.image_settings.file_format='PNG';sc.view_settings.view_transform='Standard'
 cam=bpy.data.objects.new('FitCamera',bpy.data.cameras.new('FitCamera'));sc.collection.objects.link(cam);sc.camera=cam;cam.data.type='ORTHO';cam.data.ortho_scale=1.13
 center=Vector((0,-.13,.055))
 for label,direction in [('side',(-2,0,.02)),('rear',(-2,1.2,.8))]:
  cam.location=center+Vector(direction);cam.rotation_euler=(center-cam.location).to_track_quat('-Z','Y').to_euler();sc.render.filepath=str(a.out/(entity+'-'+label+'.png'));bpy.ops.render.render(write_still=True)
(a.out/'fit-report.json').write_text(json.dumps(report,indent=2));print('DONE',len(report),'assemblies')
