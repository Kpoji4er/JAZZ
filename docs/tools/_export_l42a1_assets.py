import bpy, importlib.util, math, numpy as np
from pathlib import Path
from mathutils import Matrix,Vector
import argparse,sys
parser=argparse.ArgumentParser()
parser.add_argument('--build',type=Path,required=True)
parser.add_argument('--game-root',type=Path,required=True)
parser.add_argument('--source',type=Path,required=True)
args=parser.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
out=args.build
game=args.game_root

spec=importlib.util.spec_from_file_location('rifle_hge',game/'ModTools/BlenderExport.py')
hge=importlib.util.module_from_spec(spec);spec.loader.exec_module(hge)
hge.SETTINGS.update(version='71',game='Zulu',appid='Jagged Alliance 3',mtl_prop_0_visible=True,mtl_prop_0_name='Unit',enable_colliders=True);hge.register()
bpy.ops.wm.open_mainfile(filepath=str(out/'L42A1_split_review.blend'))
tex=out/'Textures';tex.mkdir(exist_ok=True)
source=args.source
def pixels(path):
    im=bpy.data.images.load(str(path),check_existing=False);im.colorspace_settings.name='Non-Color'
    im.scale(2048,2048);a=np.empty(2048*2048*4,np.float32);im.pixels.foreach_get(a);bpy.data.images.remove(im);return a.reshape(-1,4)
def save(name,a,color=False):
    im=bpy.data.images.new(name,width=2048,height=2048,alpha=True)
    im.colorspace_settings.name='sRGB' if color else 'Non-Color';im.pixels.foreach_set(a.ravel());im.file_format='TARGA_RAW';im.filepath_raw=str(tex/(name+'.tga'));im.save();return im
for mat in [bpy.data.materials['L42A1_Body'],bpy.data.materials['L42A1_Lenses']]:
    body=mat.name.endswith('Body');pre=mat.name
    files={'Base':'DefaultMaterial_C.png' if body else 'GAP_2DAE05_Martens_Dries__C.png','Normal':'GAP_2DAE05_Martens_Dries_N.png','AO':'GAP_2DAE05_Martens_Dries_AO.png' if body else 'GAP_2DAE05_Martens_Dries__AO.png'}
    images={key:save(pre+'_'+key,pixels(source/fn),key=='Base') for key,fn in files.items() if body or key!='Normal'}
    rough=pixels(source/('DefaultMaterial_R.png' if body else 'GAP_2DAE05_Martens_Dries_R.png'))
    rm=np.ones_like(rough);rm[:,0]=rough[:,0];rm[:,1]=0;rm[:,2]=pixels(source/'GAP_2DAE05_Martens_Dries_M.png')[:,0] if body else 0
    images['RM']=save(pre+'_RM',rm)
    hge.add_material_props(mat)
    for prop in hge.MATERIAL_PROPERTIES:
        if prop.settings_name:
            key={'base_color':'Base','normal_map':'Normal','roughness_metallic_map':'RM','ambient_occlusion_map':'AO'}.get(prop.settings_name)
            mat[prop.id]=images[key].filepath_raw if key in images else '' if prop.map else getattr(mat.hgm_settings,prop.settings_name)
meshes=[o for o in bpy.context.scene.objects if o.type=='MESH']
transform=Matrix.Translation(Vector((0,-.1645,.014)))@Matrix.Rotation(-math.pi/2,4,'Z')
for o in meshes:
    o.data.transform(transform@o.matrix_world);o.matrix_world=Matrix.Identity(4);o.hide_render=False
for o in list(bpy.data.objects):
    if o.type!='MESH':bpy.data.objects.remove(o,do_unlink=True)
bpy.ops.object.select_all(action='DESELECT')
for name in ['L42A1_ScopeBody','L42A1_Lenses']:bpy.data.objects[name].select_set(True)
bpy.context.view_layer.objects.active=bpy.data.objects['L42A1_ScopeBody'];bpy.ops.object.join();scope=bpy.context.object;scope.name='L42A1_Scope'
root=bpy.data.objects['L42A1'];pivot=Vector((0,-.055,.068))
for o in [root,scope]:
    bpy.ops.object.select_all(action='DESELECT');o.select_set(True);bpy.context.view_layer.objects.active=o
    tri=o.modifiers.new('Triangulate','TRIANGULATE');tri.keep_custom_normals=True;bpy.ops.object.modifier_apply(modifier=tri.name)
    origin=bpy.data.objects.new(o.name+'_Origin',None);bpy.context.collection.objects.link(origin)
    point=pivot if o==scope else Vector();origin.location=point;o.data.transform(Matrix.Translation(-point));o.parent=origin;o.location=Vector()
    settings=o.hge_obj_settings;settings.entity=o.name;settings.mesh='Mesh';settings.state='idle';settings.lod=1;settings.ignore=False;o.hge_export=True
for name,point in {'Scope':pivot,'Muzzle':(0,-.714,.057),'Hand_l_grip':(0,-.2,-.012),'Trigger':(0,-.025,-.025),'Magazine':(0,-.09,-.025)}.items():
    o=bpy.data.objects.new(name,None);bpy.context.collection.objects.link(o);o.parent=root;o.location=point;o.hge_obj_settings.spot_name=name
bpy.context.scene.unit_settings.system='METRIC';bpy.context.scene.unit_settings.scale_length=1
bpy.ops.wm.save_as_mainfile(filepath=str(out/'L42A1_JAZZ.blend'))
with hge.ObjectNamesExportContext(bpy.context):
    bpy.ops.export_scene.fbx(filepath=str(out/'L42A1_JAZZ.fbx'),axis_forward='Y',axis_up='Z',apply_scale_options='FBX_SCALE_ALL',object_types={'MESH','EMPTY'},use_custom_props=True,add_leaf_bones=False,bake_anim=False)
print('Exported L42A1 and L42A1_Scope')
