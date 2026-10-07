"""Prepare SCAR family from owner-supplied scene, not rejected reconstruction.

Blender --background SOURCE.blend --python SCRIPT -- --build DIR --textures DIR
Source component coordinates remain rigid within each recovered assembly.
"""
import argparse
import json
import math
import sys
from pathlib import Path
import bpy
import bmesh
from mathutils import Matrix, Vector

p=argparse.ArgumentParser()
p.add_argument('--build',type=Path,required=True)
p.add_argument('--textures',type=Path,required=True)
a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
a.build.mkdir(parents=True,exist_ok=True)
original={o.name:o for o in bpy.context.scene.objects if o.type=='MESH'}
materials={}
def material(prefix):
    if prefix in materials:return materials[prefix]
    m=bpy.data.materials.new(prefix);m.use_nodes=True
    n,l=m.node_tree.nodes,m.node_tree.links;b=n.get('Principled BSDF')
    def image(kind,space):
        t=n.new('ShaderNodeTexImage');t.image=bpy.data.images.load(str(a.textures/f'{prefix}_{kind}.tga'),check_existing=True)
        t.image.colorspace_settings.name=space;return t.outputs['Color']
    l.new(image('BaseColor','sRGB'),b.inputs['Base Color'])
    nm=n.new('ShaderNodeNormalMap');l.new(image('Normal','Non-Color'),nm.inputs['Color']);l.new(nm.outputs['Normal'],b.inputs['Normal'])
    sep=n.new('ShaderNodeSeparateColor');l.new(image('RM','Non-Color'),sep.inputs['Color']);l.new(sep.outputs['Red'],b.inputs['Roughness']);l.new(sep.outputs['Blue'],b.inputs['Metallic'])
    materials[prefix]=m;return m

def extract(index,name,prefix,bounds):
    src=original[f'model_{index}'];o=src.copy();o.data=src.data.copy();bpy.context.scene.collection.objects.link(o)
    o.name=name;o.data.transform(src.matrix_world);o.matrix_world=Matrix.Identity(4)
    bm=bmesh.new();bm.from_mesh(o.data)
    def inside(v):return all(bounds[i][0]<v.co[i]<bounds[i][1] for i in range(3))
    crossing=[f for f in bm.faces if any(inside(v) for v in f.verts) and not all(inside(v) for v in f.verts)]
    assert not crossing,(name,'selection cuts source geometry',len(crossing))
    bmesh.ops.delete(bm,geom=[f for f in bm.faces if not all(inside(v) for v in f.verts) or f.calc_area()<1e-7],context='FACES_ONLY')
    bmesh.ops.delete(bm,geom=[v for v in bm.verts if not v.link_faces],context='VERTS')
    assert bm.faces,name
    bm.to_mesh(o.data);bm.free();o.data.materials.clear();o.data.materials.append(material(prefix))
    return o

def bbox(o):
    return [Vector([fn(v.co[i] for v in o.data.vertices) for i in range(3)]) for fn in (min,max)]
def canonical(parts,kind):
    lo,hi=bbox(parts['Upper'])
    if kind=='H':
        center=(lo.z+hi.z)/2
        matrix=Matrix(((0,-1,0,hi.y),(0,0,1,-center),(-1,0,0,lo.x),(0,0,0,1)))
    elif kind=='L':
        center=(lo.y+hi.y)/2
        matrix=Matrix(((-1,0,0,hi.x),(0,-1,0,center),(0,0,1,-hi.z),(0,0,0,1)))
    else:
        center=(lo.z+hi.z)/2
        matrix=Matrix(((1,0,0,-lo.x),(0,0,1,-center),(0,-1,0,lo.y),(0,0,0,1)))
    for o in parts.values():o.data.transform(matrix)
    return parts
def duplicate(o,name):
    c=o.copy();c.data=o.data.copy();c.name=name;bpy.context.scene.collection.objects.link(c);return c

Hbox=((48,80),(0,110),(-2,10))
H=canonical({name:extract(i,'H_'+name,mat,Hbox) for i,name,mat in [
    (0,'Upper','upper_scarh'),(1,'Stock','stock'),(3,'RearSight','acc_fn_rearsight'),
    (4,'Common','scar_common'),(7,'Lower','scar_lower'),(8,'Magazine','magazine_scarh_oem'),(11,'Muzzle','acc_muzzledevices1')]},'H')
Lbox=((-60,30),(-16,-4),(30,60))
L=canonical({name:extract(i,'L_'+name,mat,Lbox) for i,name,mat in [
    (13,'Upper','upper_scarl'),(3,'RearSight','acc_fn_rearsight'),(4,'Common','scar_common'),
    (14,'Lower','scar_lower'),(15,'Magazine','magazine_stanag_fn'),(11,'Muzzle','acc_muzzledevices1')]},'L')
# Shared stock seats against the same rear receiver datum, with no per-part nudges.
L['Stock']=duplicate(H['Stock'],'L_Stock')
allbox=((-1000,1000),(-1000,1000),(-1000,1000))
SSR=canonical({name:extract(i,'SSR_'+name,mat,allbox) for i,name,mat in [
    (32,'Upper','upper_ssr'),(36,'Stock','stock_ssr'),(34,'StockPlate','upper_ssr')]},'SSR')
for name in ('Common','Lower','Magazine','RearSight','Muzzle'):
    SSR[name]=duplicate(H[name],'SSR_'+name)
families={'H':H,'L':L,'SSR':SSR}
for obj in original.values():bpy.data.objects.remove(obj,do_unlink=True)

# Source-library units are centimetres. One common rigid frame puts rear rail
# at X=0, rail top at Z=0; export will set the trigger origin for every variant.
for kind,parts in families.items():
    for name,o in parts.items():o['source_part']=name;o['source_family']=kind
    report={name:{'min_cm':list(bbox(o)[0]),'max_cm':list(bbox(o)[1]),'faces':len(o.data.polygons)} for name,o in parts.items()}
    (a.build/f'{kind}-parts.json').write_text(json.dumps(report,indent=2))

scene=bpy.context.scene
scene.render.engine='BLENDER_EEVEE_NEXT';scene.render.resolution_x=1500;scene.render.resolution_y=650;scene.render.resolution_percentage=100
scene.view_settings.view_transform='Standard';scene.world.use_nodes=True;scene.world.node_tree.nodes['Background'].inputs[1].default_value=.45
for name,loc,power in [('Key',(0,-150,180),200000),('Fill',(0,150,100),100000)]:
    ld=bpy.data.lights.new(name,'AREA');ld.energy=power;ld.size=180
    ob=bpy.data.objects.new(name,ld);scene.collection.objects.link(ob);ob.location=loc;ob.rotation_euler=(-ob.location).to_track_quat('-Z','Y').to_euler()
c=bpy.data.cameras.new('Review');c.type='ORTHO';c.ortho_scale=115
cam=bpy.data.objects.new('Review',c);scene.collection.objects.link(cam);scene.camera=cam
cam.location=(20,-200,-6);cam.rotation_euler=(Vector((20,0,-6))-cam.location).to_track_quat('-Z','Y').to_euler()
for kind,parts in families.items():
    for family,objects in families.items():
        for o in objects.values():o.hide_render=family!=kind
    scene.render.filepath=str(a.build/f'{kind}-materials.png');bpy.ops.render.render(write_still=True)
bpy.ops.wm.save_as_mainfile(filepath=str(a.build/'SCAR-family-source.blend'))
