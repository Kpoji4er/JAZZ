import bpy, importlib.util, math, numpy as np
from pathlib import Path
from mathutils import Matrix,Vector
import argparse,sys
parser=argparse.ArgumentParser()
parser.add_argument('--build',type=Path,required=True)
parser.add_argument('--game-root',type=Path,required=True)
args=parser.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
out=args.build
game=args.game_root

spec=importlib.util.spec_from_file_location('mosin_hge',game/'ModTools/BlenderExport.py')
hge=importlib.util.module_from_spec(spec);spec.loader.exec_module(hge)
hge.SETTINGS.update(version='71',game='Zulu',appid='Jagged Alliance 3',mtl_prop_0_visible=True,mtl_prop_0_name='Unit',enable_colliders=True);hge.register()
bpy.ops.wm.read_factory_settings(use_empty=True)
tex=out/'Textures';tex.mkdir(exist_ok=True)
def pixels(path):
    im=bpy.data.images.load(str(path),check_existing=False);im.colorspace_settings.name='Non-Color';im.scale(2048,2048)
    a=np.empty(2048*2048*4,np.float32);im.pixels.foreach_get(a);bpy.data.images.remove(im);return a.reshape(-1,4)
def save(name,a,color=False):
    im=bpy.data.images.new(name,width=2048,height=2048,alpha=True);im.colorspace_settings.name='sRGB' if color else 'Non-Color'
    im.pixels.foreach_set(a.ravel());im.file_format='TARGA_RAW';im.filepath_raw=str(tex/(name+'.tga'));im.save();return im
for variant,prefix,parts in [('1891','Mosin1891',[1]),('M38','MosinM38',[2,3,4]),('Obrez','MosinNagantObrez',[0])]:
    name='MOSIN_'+variant;src=out/variant/'source'
    images={key:save(name+'_'+key,pixels(src/(prefix+'_'+suffix+'.png')),key=='Base') for key,suffix in [('Base','BaseColor'),('Normal','Normal'),('AO','AO')]}
    r=pixels(src/(prefix+'_Roughness.png'));m=pixels(src/(prefix+'_Metallic.png'));rm=np.ones_like(r);rm[:,0]=r[:,0];rm[:,1]=0;rm[:,2]=m[:,0];images['RM']=save(name+'_RM',rm)
    mat=bpy.data.materials.new(name);mat.use_nodes=True;n=mat.node_tree.nodes;l=mat.node_tree.links;bsdf=n.get('Principled BSDF')
    for key,im in images.items():
        t=n.new('ShaderNodeTexImage');t.image=im
        if key=='Base':l.new(t.outputs['Color'],bsdf.inputs['Base Color'])
        elif key=='Normal':
            normal=n.new('ShaderNodeNormalMap');l.new(t.outputs['Color'],normal.inputs[1]);l.new(normal.outputs[0],bsdf.inputs['Normal'])
        elif key=='RM':
            channels=n.new('ShaderNodeSeparateColor');l.new(t.outputs[0],channels.inputs[0]);l.new(channels.outputs[0],bsdf.inputs['Roughness']);l.new(channels.outputs[2],bsdf.inputs['Metallic'])
    hge.add_material_props(mat)
    for prop in hge.MATERIAL_PROPERTIES:
        if prop.settings_name:
            key={'base_color':'Base','normal_map':'Normal','roughness_metallic_map':'RM','ambient_occlusion_map':'AO'}.get(prop.settings_name)
            mat[prop.id]=images[key].filepath_raw if key in images else '' if prop.map else getattr(mat.hgm_settings,prop.settings_name)
    objects=[]
    # Normalize OBJ coordinates directly, rather than depending on importer rotation.
    rotation=Matrix.Rotation(math.pi,4,'Z') if variant=='Obrez' else Matrix.Rotation(math.pi/2,4,'X')
    grip=Vector((0,-.09,-.04)) if variant=='Obrez' else Vector((0,-.06,-.15 if variant=='M38' else -.10))
    transform=rotation@Matrix.Translation(-grip)@Matrix.Scale(.01,4)
    # Translation is expressed in meters after source scaling.
    transform=Matrix.Translation(-(rotation@grip))@rotation@Matrix.Scale(.01,4)
    for idx in parts:
        bpy.ops.wm.obj_import(filepath=str(src/f'model_{idx}.obj'));o=bpy.context.object
        o.data.transform(transform);o.matrix_world=Matrix.Identity(4);o.data.materials.clear();o.data.materials.append(mat);objects.append(o)
    bpy.ops.object.select_all(action='DESELECT')
    for o in objects:o.select_set(True)
    bpy.context.view_layer.objects.active=objects[0]
    if len(objects)>1:bpy.ops.object.join()
    o=bpy.context.object;o.name=name
    tri=o.modifiers.new('Triangulate','TRIANGULATE');tri.keep_custom_normals=True;bpy.ops.object.modifier_apply(modifier=tri.name)
    origin=bpy.data.objects.new(name+'_Origin',None);bpy.context.collection.objects.link(origin);o.parent=origin
    st=o.hge_obj_settings;st.entity=name;st.mesh='Mesh';st.state='idle';st.lod=1;st.ignore=False;o.hge_export=True
    muzzle_y=min(v.co.y for v in o.data.vertices)
    for spot,point in {'Muzzle':(0,muzzle_y,.06 if variant!='Obrez' else .04),'Barrel':(0,0,0),'Hand_l_grip':(0,-.07 if variant=='Obrez' else -.22,-.01),'Trigger':(0,-.02,-.025),'Magazine':(0,-.08,-.04)}.items():
        empty=bpy.data.objects.new(name+'_'+spot,None);bpy.context.collection.objects.link(empty);empty.parent=o;empty.location=point;empty.hge_obj_settings.spot_name=spot
s=bpy.context.scene;s.unit_settings.system='METRIC';s.unit_settings.scale_length=1
bpy.ops.wm.save_as_mainfile(filepath=str(out/'MOSIN_JAZZ.blend'))
with hge.ObjectNamesExportContext(bpy.context):
    bpy.ops.export_scene.fbx(filepath=str(out/'MOSIN_JAZZ.fbx'),axis_forward='Y',axis_up='Z',apply_scale_options='FBX_SCALE_ALL',object_types={'MESH','EMPTY'},use_custom_props=True,add_leaf_bones=False,bake_anim=False)
print('Exported all three Mosin configurations; ammunition props and bayonet excluded.')
