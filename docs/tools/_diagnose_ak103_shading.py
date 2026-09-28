"""Blender offline shading comparisons; never installs or modifies source.

blender --background --python this.py -- --blend FILE --out DIR
Renders body/stock from both sides with original, neutral, X/Y-inverted normals.
Also records image bindings. No custom normals authored.
"""
import argparse
import json
import sys
from pathlib import Path

import bpy
from mathutils import Vector

p = argparse.ArgumentParser(description=__doc__)
p.add_argument('--blend', type=Path, required=True)
p.add_argument('--out', type=Path, required=True)
a = p.parse_args(sys.argv[sys.argv.index('--')+1:])
a.out.mkdir(parents=True, exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(a.blend), use_scripts=False)
scene = bpy.context.scene
scene.render.engine = 'BLENDER_EEVEE_NEXT'
scene.render.resolution_x = 1200
scene.render.resolution_y = 720
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = 'PNG'
scene.render.film_transparent = False
scene.view_settings.view_transform = 'AgX'
if scene.world is None:
    scene.world = bpy.data.worlds.new('DiagnosticWorld')
scene.world.use_nodes = True
scene.world.node_tree.nodes['Background'].inputs[0].default_value = (.08,.08,.08,1)
scene.world.node_tree.nodes['Background'].inputs[1].default_value = .6
for ob in list(scene.objects):
    if ob.type in {'CAMERA','LIGHT'}:
        bpy.data.objects.remove(ob, do_unlink=True)
for name, pos, power, size in [('key',(1,-.3,1.2),100,.8),('fill',(-1,0,.5),65,1),('rim',(0,.8,.8),80,.8)]:
    light = bpy.data.lights.new(name,'AREA'); light.energy=power; light.size=size
    ob=bpy.data.objects.new(name,light); scene.collection.objects.link(ob); ob.location=pos
    ob.rotation_euler=(-ob.location).to_track_quat('-Z','Y').to_euler()
cam=bpy.data.objects.new('camera',bpy.data.cameras.new('camera'))
scene.collection.objects.link(cam); scene.camera=cam; cam.data.type='ORTHO';cam.data.clip_start=.001
parts={n:bpy.data.objects[n] for n in ('AKR_AK103','AKR_AK103_Stock')}
bindings={}
adjust=[]
for name,obj in parts.items():
    bindings[name]=[]
    for mat in obj.data.materials:
        nodes=mat.node_tree.nodes; links=mat.node_tree.links
        for n in list(nodes):
            if n.type=='TEX_IMAGE' and n.image:
                n.image.filepath=bpy.path.abspath(n.image.filepath)
                bindings[name].append({'label':n.label,'image':n.image.filepath,'colorspace':n.image.colorspace_settings.name})
            if n.type=='NORMAL_MAP':
                old=n.inputs['Color'].links[0].from_socket
                vec=nodes.new('ShaderNodeVectorMath');vec.operation='MULTIPLY_ADD'
                links.new(old,vec.inputs[0]);links.new(vec.outputs[0],n.inputs['Color'])
                adjust.append((n,vec))
(a.out/'bindings.json').write_text(json.dumps(bindings,indent=2))
for name,obj in parts.items():
    for ob in scene.objects:
        if ob.type=='MESH':ob.hide_render=ob!=obj
    pts=[obj.matrix_world@v.co for v in obj.data.vertices]
    center=(Vector(tuple(min(v[i] for v in pts) for i in range(3)))+Vector(tuple(max(v[i] for v in pts) for i in range(3))))/2
    span=.58 if name=='AKR_AK103' else .31
    for side,x in [('right',1),('left',-1)]:
        cam.location=center+Vector((x,.1,.2)).normalized()*2
        cam.rotation_euler=(center-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=span
        for variant,mul,add,strength in [('original',(1,1,1),(0,0,0),1),('neutral',(1,1,1),(0,0,0),0),('flip_y',(1,-1,1),(0,1,0),1),('flip_x',(-1,1,1),(1,0,0),1)]:
            for normal,vec in adjust:
                normal.inputs['Strength'].default_value=strength
                vec.inputs[1].default_value=mul;vec.inputs[2].default_value=add
            scene.render.filepath=str(a.out/f'{name}_{side}_{variant}.png')
            bpy.ops.render.render(write_still=True)
for normal,vec in adjust:
    normal.inputs['Strength'].default_value=1
    vec.inputs[1].default_value=(1,1,1);vec.inputs[2].default_value=(0,0,0)
visible=[]
for ob in scene.objects:
    if ob.type=='MESH':
        ob.hide_render=not ob.name.startswith('AKR_AK103') or ob.name.endswith('StockFolded')
        if not ob.hide_render:visible.append(ob)
pts=[ob.matrix_world@v.co for ob in visible for v in ob.data.vertices]
center=(Vector(tuple(min(v[i] for v in pts) for i in range(3)))+Vector(tuple(max(v[i] for v in pts) for i in range(3))))/2
for side,x in [('right',1),('left',-1)]:
    cam.location=center+Vector((x,.1,.2)).normalized()*2
    cam.rotation_euler=(center-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=1.05
    scene.render.filepath=str(a.out/f'assembled_{side}.png')
    bpy.ops.render.render(write_still=True)
print('DONE diagnostic only; source untouched')
